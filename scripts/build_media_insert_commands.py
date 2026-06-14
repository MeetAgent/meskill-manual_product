#!/usr/bin/env python3
"""Generate lark-cli docs +media-insert commands from a media manifest."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


def q(value: str) -> str:
    return shlex.quote(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Media manifest JSON path")
    parser.add_argument("--doc-url", help="Override document URL from manifest")
    parser.add_argument("--profile", default="personal-feishu")
    parser.add_argument("--as-user", default="user", choices=["user", "bot"])
    parser.add_argument("--dry-run", action="store_true", help="Add lark-cli --dry-run to generated commands")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    doc_url = args.doc_url or manifest.get("doc_url")
    if not doc_url:
        print("manifest.doc_url is required unless --doc-url is provided", file=sys.stderr)
        return 1

    default_align = manifest.get("default_align", "center")
    items = manifest.get("items", [])
    if not items:
        print("manifest.items is empty", file=sys.stderr)
        return 1

    for item in items:
        media_type = item.get("type", "image")
        align = item.get("align", default_align)
        command = [
            "lark-cli",
            "docs",
            "+media-insert",
            "--profile",
            args.profile,
            "--as",
            args.as_user,
            "--doc",
            doc_url,
            "--selection-with-ellipsis",
            item["selection"],
            "--file",
            item["file"],
            "--caption",
            item["caption"],
            "--align",
            align,
        ]
        if media_type != "image":
            command.extend(["--type", media_type])
        if item.get("file_view"):
            command.extend(["--file-view", item["file_view"]])
        if args.dry_run:
            command.append("--dry-run")
        print(" ".join(q(part) for part in command))

    return 0


if __name__ == "__main__":
    sys.exit(main())
