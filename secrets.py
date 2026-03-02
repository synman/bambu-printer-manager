#!/usr/bin/env python3
"""Encrypted key-value secret store.

Stores secrets in ``~/.bpm_secrets`` as a JSON file where each value is
independently Fernet-encrypted using a key derived from a master password
via PBKDF2-HMAC-SHA256.

Master password is read from the ``BPM_SECRETS_PASS`` environment variable;
if not set, a prompt is shown (input is hidden via getpass).

Usage::

    # Store a secret
    python secrets.py set dockerhub_token brw_xxxxx

    # Retrieve a secret
    python secrets.py get dockerhub_token

    # List all keys (values are never printed)
    python secrets.py list

    # Delete a key
    python secrets.py delete dockerhub_token
"""

from __future__ import annotations

import base64
import getpass
import json
import os
import sys
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STORE_PATH = Path.home() / ".bpm_secrets"
PBKDF2_ITERATIONS = 480_000  # NIST SP 800-132 recommended minimum (2023)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte URL-safe base64 Fernet key from *password* + *salt*."""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def _get_password() -> str:
    """Return master password from env or interactive prompt."""
    pw = os.environ.get("BPM_SECRETS_PASS", "")
    if not pw:
        pw = getpass.getpass("Master password: ")
    if not pw:
        print("Error: master password must not be empty.", file=sys.stderr)
        sys.exit(1)
    return pw


def _load_store() -> dict:
    """Load the on-disk store, returning an empty structure if absent."""
    if not STORE_PATH.exists():
        return {}
    with STORE_PATH.open() as fh:
        return json.load(fh)


def _save_store(data: dict) -> None:
    """Persist the store (mode 0600 — owner read/write only)."""
    STORE_PATH.write_text(json.dumps(data, indent=2))
    STORE_PATH.chmod(0o600)


def _fernet(password: str, store: dict) -> Fernet:
    """Return a Fernet instance, creating and saving a salt if needed."""
    if "salt" not in store:
        store["salt"] = base64.b64encode(os.urandom(16)).decode()
        store.setdefault("entries", {})
        _save_store(store)
    salt = base64.b64decode(store["salt"])
    return Fernet(_derive_key(password, salt))


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_set(key: str, value: str) -> None:
    """Encrypt *value* and store it under *key*."""
    store = _load_store()
    pw = _get_password()
    f = _fernet(pw, store)
    store.setdefault("entries", {})[key] = f.encrypt(value.encode()).decode()
    _save_store(store)
    print(f"Stored: {key}")


def cmd_get(key: str) -> None:
    """Decrypt and print the value stored under *key*."""
    store = _load_store()
    if "entries" not in store or key not in store["entries"]:
        print(f"Error: key '{key}' not found.", file=sys.stderr)
        sys.exit(1)
    pw = _get_password()
    f = _fernet(pw, store)
    try:
        value = f.decrypt(store["entries"][key].encode()).decode()
    except InvalidToken:
        print("Error: wrong password or corrupted data.", file=sys.stderr)
        sys.exit(1)
    print(value)


def cmd_list() -> None:
    """Print all stored key names (values are never revealed)."""
    store = _load_store()
    keys = list((store.get("entries") or {}).keys())
    if not keys:
        print("(no secrets stored)")
        return
    for k in sorted(keys):
        print(k)


def cmd_delete(key: str) -> None:
    """Remove *key* from the store."""
    store = _load_store()
    entries: dict = store.get("entries", {})
    if key not in entries:
        print(f"Error: key '{key}' not found.", file=sys.stderr)
        sys.exit(1)
    del entries[key]
    store["entries"] = entries
    _save_store(store)
    print(f"Deleted: {key}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

USAGE = """\
Usage:
  secrets.py set    <key> <value>   Encrypt and store a secret
  secrets.py get    <key>           Decrypt and print a secret
  secrets.py delete <key>           Remove a secret
  secrets.py list                   List all stored key names

Master password via BPM_SECRETS_PASS env var or interactive prompt.
Store location: ~/.bpm_secrets  (chmod 600)
"""


def main() -> None:
    """CLI entry point."""
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        sys.exit(0)

    cmd = args[0].lower()

    if cmd == "set" and len(args) == 3:
        cmd_set(args[1], args[2])
    elif cmd == "get" and len(args) == 2:
        cmd_get(args[1])
    elif cmd == "delete" and len(args) == 2:
        cmd_delete(args[1])
    elif cmd == "list" and len(args) == 1:
        cmd_list()
    else:
        print(USAGE, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
