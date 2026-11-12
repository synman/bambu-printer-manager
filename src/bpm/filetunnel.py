"""
`filetunnel` is a minimal, read-only client for the file tunnel on TLS port 6000 of the
H2 series and P2S (`BambuTunnelLocal`, the service Bambu Studio's Files panel uses).

It exists for one read: a member of the project the printer is running, which the
printer serves from memory even when the job's `.3mf` sits in the internal eMMC cache
that FTPS cannot see.  On an A1 or P1 this port is the camera, a different protocol.

Wire facts are in the node-kb-mcp `bambu-tcp-6000-protocol` and
`bambu-tcp-6000-command-reference` articles.  Only the login, the setup frame and one
`FILE_DOWNLOAD` of `mem:/16` are sent, nothing that writes.
"""

import hashlib
import json
import socket
import ssl
import struct
from typing import Any

_MAGIC_LOGIN = 0x0101013F
_MAGIC_CTRL = 0x0102013F
_CONTINUE = 1
_FILE_DOWNLOAD = 4
_MAX_MEMBER_BYTES = 8 * 1024 * 1024  # a plate image or config; stops a runaway stream


class FileTunnelError(RuntimeError):
    """The tunnel could not be opened, or a read was refused or failed its checksum."""


class FileTunnel:
    """
    One logged-in `:6000` session.  Use it as a context manager.

    Every socket operation times out after `timeout` seconds, so a printer that stops
    answering raises `FileTunnelError` instead of hanging the caller.
    """

    def __init__(
        self, hostname: str, access_code: str, port: int = 6000, timeout: float = 10.0
    ):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = (
            ssl.CERT_NONE
        )  # the printer's certificate is a weak-key leaf
        context.set_ciphers(
            "DEFAULT@SECLEVEL=0"
        )  # its key is below OpenSSL's default level
        self._frame_seq = 0
        self._sequence = 0
        self._sock = None
        try:
            self._sock = context.wrap_socket(
                socket.create_connection((hostname, port), timeout),
                server_hostname=hostname,
            )
            self._sock.settimeout(timeout)
            self._send(
                _MAGIC_LOGIN,
                b"bblp".ljust(8, b"\0") + access_code.encode().ljust(8, b"\0"),
            )
            self._receive()
            setup = {
                "sequence": 0,
                "mtype": 12291,
                "req": {
                    "t_av": 1,
                    "mtype": 12289,
                    "peer_t": 3,
                    "pid": "bpm",
                    "ver": "02.03.00.00",
                },
            }
            self._send(_MAGIC_CTRL, json.dumps(setup).encode())
            self._receive()
        except (OSError, ssl.SSLError, ValueError, struct.error) as e:
            self.close()
            raise FileTunnelError(f"tunnel open failed: {e}") from e

    def __enter__(self) -> "FileTunnel":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def _send(self, magic: int, payload: bytes) -> None:
        header = struct.pack("<IIII", len(payload), magic, self._frame_seq, 0)
        self._sock.sendall(header + payload)
        self._frame_seq += 1

    def _read(self, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            chunk = self._sock.recv(size - len(data))
            if not chunk:
                raise FileTunnelError("tunnel closed by the printer")
            data.extend(chunk)
        return bytes(data)

    def _receive(self) -> bytes:
        length, _magic, _seq, _zero = struct.unpack("<IIII", self._read(16))
        if length > _MAX_MEMBER_BYTES:
            raise FileTunnelError(f"frame of {length} bytes is too large")
        return self._read(length)

    def project_member(self, member: str) -> bytes:
        """
        One member of the project the printer is running or last ran, such as
        `Metadata/slice_info.config` or `Metadata/plate_1.png`.

        The printer serves only a few members this way: `plate_N.json`, `top_N.png`, the
        gcode and `project_settings.config` are refused.  Raises `FileTunnelError` on a
        refusal, a failed checksum, an oversized member, or a timeout.
        """
        self._sequence += 1
        param = json.dumps(
            {
                "sequence_id": 1,
                "version": 1,
                "peer_host": "studio",
                "command": "get_project_file",
                "file_rel_path": member,
            }
        ).encode()
        request = {
            "mtype": 12289,
            "cmdtype": _FILE_DOWNLOAD,
            "sequence": self._sequence,
            "req": {"path": "mem:/16", "offset": 0, "mem_dl_param_size": len(param)},
        }
        try:
            self._send(_MAGIC_CTRL, json.dumps(request).encode() + b"\n\n" + param)
            head = None
            data = bytearray()
            final: dict = {}
            while True:
                payload = self._receive()
                text, _, body = payload.partition(b"\n\n")
                reply = json.loads(text)
                if reply.get("sequence") != self._sequence or "result" not in reply:
                    continue  # a printer-initiated notification
                info = reply.get("reply", {})
                if head is None and "mem_dl_param_size" in info:
                    size = info["mem_dl_param_size"]
                    head = json.loads(body[:size])
                    data.extend(body[size:])
                else:
                    data.extend(body)
                if len(data) > _MAX_MEMBER_BYTES:
                    raise FileTunnelError(f"{member} is too large")
                final = info
                if reply["result"] != _CONTINUE:
                    break
        except (OSError, ssl.SSLError, ValueError, struct.error) as e:
            raise FileTunnelError(f"reading {member} failed: {e}") from e

        if head is None or head.get("err_no") != 0:
            raise FileTunnelError(
                f"{member} refused: err_no {None if head is None else head.get('err_no')}"
            )
        if hashlib.md5(data).hexdigest() != final.get("file_md5"):
            raise FileTunnelError(f"{member} failed its checksum")
        return bytes(data)
