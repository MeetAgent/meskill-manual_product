#!/usr/bin/env python3
"""Validate lark-cli wiki spaces get_node output against expected tokens."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def dig(data: dict, keys: list[str]) -> object:
    current: object = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def get_node_field(data: dict, field: str) -> object:
    return (
        dig(data, [field])
        or dig(data, ["node", field])
        or dig(data, ["data", "node", field])
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-json", required=True, help="JSON output from wiki spaces get_node")
    parser.add_argument("--expected-node-token", required=True)
    parser.add_argument("--expected-obj-token")
    parser.add_argument("--expected-parent-node-token")
    parser.add_argument("--expected-title")
    args = parser.parse_args()

    data = json.loads(Path(args.node_json).read_text(encoding="utf-8"))
    checks = {
        "node_token": args.expected_node_token,
        "obj_token": args.expected_obj_token,
        "parent_node_token": args.expected_parent_node_token,
        "title": args.expected_title,
    }
    errors: list[str] = []
    for field, expected in checks.items():
        if not expected:
            continue
        actual = get_node_field(data, field)
        if actual != expected:
            errors.append(f"{field}: expected {expected}, got {actual}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("OK: wiki node validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
