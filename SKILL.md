---
name: aidea-product-docs
description: Create and update Aidea product/project documentation for Feishu/Lark Wiki, including user manuals, user change notes, release notes, changelog-to-document synthesis, screenshot and diagram standards, lark-cli overwrite updates, media reinsertion, and Wiki node validation. Use when Codex needs to produce or maintain customer-facing product docs with images, captions, Feishu docs +update/+media-insert workflows, or project-specific documentation profiles.
---

# Aidea Product Docs

Use this skill to create or update customer-facing Aidea product documentation in Feishu/Lark Wiki. Supported documents include user feature manuals, user change notes, release notes, FAQ-style guides, and image-rich product walkthroughs.

## Workflow

1. Identify the document type:
   - `user_manual`: chapter-integrated user feature manual.
   - `change_note`: date/version-ordered user change note or release note.
   - `new_doc`: a new Feishu Wiki document.
   - `refresh_existing`: overwrite an existing Feishu document in place.
2. Read the project profile when available. Use `references/project-profiles/aideaon-muse.example.yaml` only as a public example; do not assume every task is Aideaon Muse. Keep real project profiles in local ignored files.
3. Read the relevant references:
   - `references/workflow.md` for end-to-end Feishu update flow.
   - `references/document-patterns.md` for manual and change-note structure.
   - `references/visual-standards.md` before creating or selecting images.
   - `references/lark-cli-recipes.md` before running lark-cli commands.
4. Ground the content in current sources. Prefer local `CHANGELOG.md`, recent `git log` / `git show`, existing Feishu `docs +fetch`, PRDs, screenshots, and explicit user notes. Do not rely only on the current Feishu page when updating release notes.
5. Prepare a local Markdown draft and a media manifest. Every image anchor must be unique in the Markdown, and every media item must have a user-readable caption.
6. Validate locally with scripts before writing to Feishu:
   - `scripts/validate_doc_assets.py`
   - `scripts/build_media_insert_commands.py --dry-run`
7. For existing Feishu documents, update in this order:
   - `docs +update --dry-run`
   - `docs +update` with overwrite mode
   - `docs +media-insert` from the manifest
   - `docs +fetch` verification
   - `wiki spaces get_node` verification
8. Report validation results, skipped checks, and user-visible changes. For documentation-only work, do not run product build/typecheck/e2e unless product code changed or screenshots require app verification.

## Defaults

- Default Feishu identity: `--profile personal-feishu --as user`.
- Default image standard: final inserted main images are `1600x1000` PNG.
- Default update style for user manuals: integrate new capabilities into existing chapters instead of adding a disconnected update chapter.
- Default update style for change notes: newest date first, with version range, summary, impacted modules, user-visible changes, usage advice, and image notes.
- Default write safety: scripts may validate and generate commands, but they must not automatically overwrite Feishu documents.

## Hard Rules

- `docs +update --mode/--command overwrite` removes existing media blocks. Always reinsert media after overwrite.
- Use relative file paths with `docs +media-insert --file`; current lark-cli rejects unsafe absolute paths.
- Do not label a handcrafted mockup as `真实界面`. Use `概念示意` or omit the image when a real UI state cannot be captured.
- Do not include login user information, empty placeholder cards, Feishu editor chrome, canvas select/pan toolbars, or unreadable far-away screenshots in final customer-facing images.
- Keep target Wiki nodes stable unless the user explicitly asks to create or move a document.

## Scripts

- `scripts/validate_doc_assets.py`: validate Markdown anchors, media manifest, image size, caption quality, and visual-label consistency.
- `scripts/build_media_insert_commands.py`: generate reviewable `lark-cli docs +media-insert` commands from a manifest.
- `scripts/check_feishu_fetch.py`: validate fetched Feishu document content against profile expectations.
- `scripts/check_wiki_node.py`: validate Wiki node metadata against expected tokens.

## Delivery Notes

Final responses should include: changed/generated files, main documentation changes, media count and visual checks, Feishu write/fetch/node validation, unexecuted checks with reasons, README/CHANGELOG decision, and user-facing impact.
