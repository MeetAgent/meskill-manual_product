# Workflow

## Source Audit

Start every task with a short source audit:

- Product/project name and intended audience.
- Document type: `user_manual`, `change_note`, `new_doc`, or `refresh_existing`.
- Target Feishu URL or Wiki token.
- Local truth sources: `CHANGELOG.md`, PRDs, existing draft Markdown, screenshots, test notes, and recent commits.
- Existing Feishu truth: run `docs +fetch` when the target document already exists.
- Image source status: real UI screenshots, real page crops, video frames, or concept diagrams.

## User Manual Flow

Use chapter-integrated updates. Fold new capabilities into the section where users naturally look for them.

Default order:

1. Reading note and customer/change-note links.
2. One-page capability overview.
3. Entry point or homepage.
4. Core feature modules.
5. Advanced workflows.
6. Failure handling and billing/limits.
7. Practical scenarios and support.

For capability additions, add operation guidance and constraints near the related workflow. Avoid a standalone "latest updates" section unless the user explicitly asks for it.

## Change Note Flow

Use newest-first ordering.

Each date/version section should contain:

- Update summary.
- Impacted modules.
- User-visible changes.
- Image anchors and captions.
- Usage advice.

Stable truth order:

1. Local `CHANGELOG.md`.
2. Recent `git log` / `git show` for user-visible changes that may be missing from changelog.
3. Existing Feishu document content.
4. User-provided notes and screenshots.

## Feishu Write Flow

For existing documents:

1. Write or update the local Markdown draft.
2. Prepare a media manifest.
3. Run `validate_doc_assets.py`.
4. Run `build_media_insert_commands.py --dry-run`.
5. Run `lark-cli docs +update ... --dry-run`.
6. Run the real overwrite update.
7. Run media insert commands from the manifest.
8. Run `docs +fetch` and `check_feishu_fetch.py`.
9. Run `wiki spaces get_node` and `check_wiki_node.py`.

Do not move the Wiki node after overwrite unless the user asks for a new location.

## New Document Flow

For new documents:

1. Create the Markdown and media manifest locally.
2. Create the Feishu doc under the requested parent Wiki node.
3. Insert media after the text is created.
4. Verify the parent node and resulting URL.
5. Save the new document token in a project profile if the user wants future updates.

## Common Failure Handling

- If overwrite succeeds but images are missing, re-run media insert from the manifest; do not rewrite text again unless needed.
- If a media anchor is not found, fetch the document and compare exact anchor text. Prefer stable full-sentence anchors over short repeated labels.
- If lark-cli rejects an image path, use a relative path from the current workspace.
- If fetch output does not expose enough media details, at minimum verify captions and key image anchors.
