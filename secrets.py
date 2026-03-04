#!/usr/bin/env python3
"""Keychain-backed key-value secret store.

Stores secrets in the macOS Keychain using the `security` CLI.
Service names are stored as ``bpm.<key>``; account is the current user.

Usage::

    # Store a secret
    python secrets.py set dockerhub_token brw_xxxxx

    # Retrieve a secret
    python secrets.py get dockerhub_token

    # List all keys
    python secrets.py list

    # Delete a key
    python secrets.py delete dockerhub_token
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SERVICE_PREFIX = "bpm."
_INDEX_SERVICE = "bpm.__index__"


def _user() -> str:
    return os.environ.get("USER", "")


def _svc(key: str) -> str:
    return f"{_SERVICE_PREFIX}{key}"


def _keychain_get(service: str) -> str | None:
    r = subprocess.run(
        ["security", "find-generic-password", "-a", _user(), "-s", service, "-w"],
        capture_output=True,
        text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else None


def _keychain_set(service: str, value: str) -> bool:
    _keychain_delete(service)
    r = subprocess.run(
        ["security", "add-generic-password", "-a", _user(), "-s", service, "-w", value],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def _keychain_delete(service: str) -> None:
    subprocess.run(
        ["security", "delete-generic-password", "-a", _user(), "-s", service],
        capture_output=True,
    )


def _index_get() -> list[str]:
    raw = _keychain_get(_INDEX_SERVICE)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []


def _index_save(keys: list[str]) -> None:
    _keychain_set(_INDEX_SERVICE, json.dumps(sorted(set(keys))))


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_set(key: str, value: str) -> None:
    """Store *value* under *key* in the Keychain."""
    if not _keychain_set(_svc(key), value):
        print(f"Error: failed to store key '{key}' in Keychain.", file=sys.stderr)
        sys.exit(1)
    keys = _index_get()
    if key not in keys:
        keys.append(key)
        _index_save(keys)
    print(f"Stored: {key}")


def cmd_get(key: str) -> None:
    """Retrieve and print the value stored under *key*."""
    value = _keychain_get(_svc(key))
    if value is None:
        print(f"Error: key '{key}' not found.", file=sys.stderr)
        sys.exit(1)
    print(value)


def cmd_list() -> None:
    """Print all stored key names."""
    keys = _index_get()
    if not keys:
        print("(no secrets stored)")
        return
    for k in sorted(keys):
        print(k)


def cmd_delete(key: str) -> None:
    """Remove *key* from the Keychain."""
    if _keychain_get(_svc(key)) is None:
        print(f"Error: key '{key}' not found.", file=sys.stderr)
        sys.exit(1)
    _keychain_delete(_svc(key))
    keys = _index_get()
    _index_save([k for k in keys if k != key])
    print(f"Deleted: {key}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

USAGE = """\
Usage:
  secrets.py set    <key> <value>   Store a secret in the macOS Keychain
  secrets.py get    <key>           Retrieve a secret from the Keychain
  secrets.py delete <key>           Remove a secret from the Keychain
  secrets.py list                   List all stored key names
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
