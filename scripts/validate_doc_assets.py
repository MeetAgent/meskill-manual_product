#!/usr/bin/env python3
"""Validate Aidea product doc Markdown anchors and media assets."""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path


BAD_CAPTIONS = {"截图1", "截图2", "示意图1", "效果图", "如下", "图片"}
BAD_MARKDOWN_SNIPPETS = [
    "<mention-doc",
    "截图1",
    "截图2",
    "示意图1",
]


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON manifest: {path}: {exc}") from exc


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", header[16:24])


def is_truthy(value: object, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", required=True, help="Markdown draft path")
    parser.add_argument("--manifest", required=True, help="Media manifest JSON path")
    parser.add_argument("--root", default=".", help="Workspace root for relative file paths")
    parser.add_argument("--expected-width", type=int, default=1600)
    parser.add_argument("--expected-height", type=int, default=1000)
    parser.add_argument("--allow-concept", action="store_true", help="Allow concept images in manifest")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    markdown_path = (root / args.markdown).resolve()
    manifest_path = (root / args.manifest).resolve()
    markdown = markdown_path.read_text(encoding="utf-8")
    manifest = load_json(manifest_path)
    items = manifest.get("items", [])

    errors: list[str] = []
    warnings: list[str] = []

    if not items:
        errors.append("manifest.items is empty")

    for snippet in BAD_MARKDOWN_SNIPPETS:
        if snippet in markdown:
            warnings.append(f"markdown contains discouraged snippet: {snippet}")

    seen_selection: set[str] = set()
    for index, item in enumerate(items, 1):
        prefix = f"items[{index}]"
        selection = str(item.get("selection", "")).strip()
        filename = str(item.get("file", "")).strip()
        caption = str(item.get("caption", "")).strip()
        image_type = str(item.get("image_type", "")).strip()
        main_image = is_truthy(item.get("main_image"), default=True)

        if not selection:
            errors.append(f"{prefix}: selection is empty")
        elif selection in seen_selection:
            errors.append(f"{prefix}: duplicated selection: {selection}")
        else:
            seen_selection.add(selection)
            count = markdown.count(selection)
            if count != 1:
                errors.append(f"{prefix}: selection must appear exactly once in markdown, found {count}: {selection}")

        if not filename:
            errors.append(f"{prefix}: file is empty")
        else:
            path = (root / filename).resolve()
            try:
                path.relative_to(root)
            except ValueError:
                errors.append(f"{prefix}: file must be inside root and relative-safe: {filename}")
                path = None
            if path and not path.exists():
                errors.append(f"{prefix}: file not found: {filename}")
            elif path and main_image:
                try:
                    width, height = png_size(path)
                    if (width, height) != (args.expected_width, args.expected_height):
                        errors.append(
                            f"{prefix}: expected {args.expected_width}x{args.expected_height} PNG, got {width}x{height}: {filename}"
                        )
                except ValueError as exc:
                    errors.append(f"{prefix}: main image must be PNG: {filename} ({exc})")

        if not caption:
            errors.append(f"{prefix}: caption is empty")
        elif caption in BAD_CAPTIONS:
            errors.append(f"{prefix}: caption is too generic: {caption}")

        if "真实界面" in caption and image_type and image_type != "real_ui":
            errors.append(f"{prefix}: caption says 真实界面 but image_type is {image_type}")
        if "概念示意" in caption and image_type == "real_ui":
            errors.append(f"{prefix}: caption says 概念示意 but image_type is real_ui")
        if image_type == "concept" and not args.allow_concept:
            warnings.append(f"{prefix}: concept image present; ensure it is not labeled as real UI")

        for keyword in item.get("required_keywords", []) or []:
            if str(keyword) not in markdown:
                errors.append(f"{prefix}: required keyword missing from markdown: {keyword}")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(items)} media item(s) validated against {markdown_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
