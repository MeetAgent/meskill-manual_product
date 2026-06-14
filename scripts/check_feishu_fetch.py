#!/usr/bin/env python3
"""Check fetched Feishu/Lark document output for required text and media hints."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_simple_yaml_list(text: str, key: str, doc_type: str | None = None) -> list[str]:
    """Extract a simple required_keywords list from the project profile template shape."""
    lines = text.splitlines()
    if key != "required_keywords":
        return []
    capture = False
    nested_capture = False
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "required_keywords:":
            capture = True
            nested_capture = doc_type is None
            continue
        if capture and stripped and not line.startswith(" ") and stripped != "required_keywords:":
            break
        if capture and doc_type and line.startswith("  ") and not line.startswith("    ") and stripped.endswith(":"):
            nested_capture = stripped == f"{doc_type}:"
            continue
        if capture and nested_capture and stripped.startswith("- "):
            result.append(stripped[2:].strip().strip('"').strip("'"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", required=True, help="docs +fetch output path")
    parser.add_argument("--profile", help="Optional project profile YAML path")
    parser.add_argument("--doc-type", choices=["user_manual", "change_note"])
    parser.add_argument("--expected-title")
    parser.add_argument("--required-keyword", action="append", default=[])
    parser.add_argument("--forbidden", action="append", default=[])
    parser.add_argument("--min-caption-count", type=int, default=0)
    parser.add_argument("--min-media-hints", type=int, default=0)
    args = parser.parse_args()

    text = load_text(Path(args.fetch))
    required = list(args.required_keyword)

    if args.profile:
        profile_text = load_text(Path(args.profile))
        required.extend(extract_simple_yaml_list(profile_text, "required_keywords", args.doc_type))
        if args.expected_title is None and args.doc_type:
            title_match = re.search(rf"{args.doc_type}:\n(?:    .+\n)*?    title: (.+)", profile_text)
            if title_match:
                args.expected_title = title_match.group(1).strip()

    errors: list[str] = []
    if args.expected_title and args.expected_title not in text:
        errors.append(f"expected title not found: {args.expected_title}")

    for keyword in required:
        if keyword and keyword not in text:
            errors.append(f"required keyword not found: {keyword}")

    for forbidden in args.forbidden:
        if forbidden and forbidden in text:
            errors.append(f"forbidden text found: {forbidden}")

    caption_count = text.lower().count("caption")
    if caption_count < args.min_caption_count:
        errors.append(f"caption count too low: expected >= {args.min_caption_count}, got {caption_count}")

    media_hints = text.count("image") + text.count("file_token") + text.count("media")
    if media_hints < args.min_media_hints:
        errors.append(f"media hints too low: expected >= {args.min_media_hints}, got {media_hints}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: fetch validation passed; captions={caption_count}, media_hints={media_hints}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
