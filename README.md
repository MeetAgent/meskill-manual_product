# Aidea Product Docs

Aidea Product Docs is a Codex skill for creating and maintaining customer-facing product documentation in Feishu/Lark Wiki. It standardizes the workflow for user manuals, release notes, change notes, FAQ-style guides, and image-rich product walkthroughs.

The skill is designed for documentation work where the source of truth must be checked before publishing, media must be reinserted after Feishu overwrite updates, and real UI screenshots must not be confused with concept diagrams.

## What This Skill Covers

- Chapter-integrated user manuals.
- Newest-first user change notes and release notes.
- New Feishu Wiki documents.
- In-place refreshes of existing Feishu documents.
- Markdown drafts with media manifests.
- Image and caption QA before publishing.
- lark-cli update, media insert, fetch, and Wiki node validation workflows.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── document-patterns.md
│   ├── visual-standards.md
│   ├── lark-cli-recipes.md
│   ├── project-profiles/
│   │   └── aideaon-muse.example.yaml
│   └── templates/
│       ├── change-note-outline.md
│       ├── media-manifest.json
│       ├── project-profile.yaml
│       └── user-manual-outline.md
└── scripts/
    ├── validate_doc_assets.py
    ├── build_media_insert_commands.py
    ├── check_feishu_fetch.py
    └── check_wiki_node.py
```

## Typical Workflow

1. Identify the documentation type: `user_manual`, `change_note`, `new_doc`, or `refresh_existing`.
2. Read the relevant references:
   - `references/workflow.md`
   - `references/document-patterns.md`
   - `references/visual-standards.md`
   - `references/lark-cli-recipes.md`
3. Ground the document in current sources such as `CHANGELOG.md`, PRDs, existing Markdown drafts, screenshots, recent commits, and existing Feishu `docs +fetch` output.
4. Prepare a Markdown draft and media manifest.
5. Validate anchors, image dimensions, captions, and generated media insert commands.
6. For existing Feishu documents, run update dry-run, overwrite update, media reinsertion, fetch verification, and Wiki node verification.
7. Report what changed, what was validated, what was skipped, and what users will notice.

## Project Profiles

Use `references/templates/project-profile.yaml` to create a local project profile, and use `references/project-profiles/aideaon-muse.example.yaml` only as a public example.

Real project profiles often contain Feishu document URLs, Wiki node tokens, parent node tokens, or project-specific paths. Keep those files local and ignored. Do not commit real profile files to a public or shared repository.

## Media Manifest

Media manifests connect exact Markdown anchor sentences to image or file insertions. Each item should include:

- `selection`: one full sentence that appears exactly once in the Markdown draft.
- `file`: a relative path to the media file.
- `caption`: a user-readable caption.
- `image_type`: usually `real_ui` or `concept`.
- `main_image`: whether the item must satisfy the default `1600x1000` PNG requirement.
- `required_keywords`: optional keywords that must exist in the Markdown draft.

Start from `references/templates/media-manifest.json`.

## Validation Scripts

Run these commands from the repository root or from the workspace that contains your draft and assets.

Validate Markdown anchors, media paths, PNG dimensions, captions, and visual labels:

```bash
python3 scripts/validate_doc_assets.py \
  --root . \
  --markdown path/to/draft.md \
  --manifest path/to/media-manifest.json
```

Generate reviewable `lark-cli docs +media-insert` commands:

```bash
python3 scripts/build_media_insert_commands.py \
  --manifest path/to/media-manifest.json \
  --dry-run
```

Validate fetched Feishu document content:

```bash
python3 scripts/check_feishu_fetch.py \
  --fetch /tmp/doc-fetch.json \
  --expected-title "Product User Manual" \
  --required-keyword "用户可感知变化"
```

Validate Wiki node metadata:

```bash
python3 scripts/check_wiki_node.py \
  --node-json /tmp/wiki-node.json \
  --expected-node-token "$NODE_TOKEN" \
  --expected-title "Product User Manual"
```

## Feishu/Lark Publishing Notes

The default identity is:

```bash
--profile personal-feishu --as user
```

For existing documents, use this order:

1. `docs +update --dry-run`
2. real overwrite update
3. `docs +media-insert` for every media item
4. `docs +fetch` verification
5. `wiki spaces get_node` verification

Important constraints:

- `docs +update` overwrite removes existing media blocks; always reinsert media afterward.
- Use relative file paths with `docs +media-insert --file`.
- Keep target Wiki nodes stable unless the user explicitly asks to create or move a document.
- Check `lark-cli docs +update --help` before publishing because installed versions may use different overwrite flags.

## Visual Standards

- Final inserted main images should be `1600x1000` PNG unless the task explicitly chooses another format.
- Use `真实界面` only for screenshots or crops from real UI rendering.
- Use `概念示意` for handcrafted diagrams, flowcharts, simulated states, or explanatory visuals.
- Do not include login users, personal identifiers, Feishu editor chrome, empty placeholder cards, unreadable far-away UI, or misleading aspect ratios.
- Prefer feature-area crops over full-page screenshots unless the page-level layout is the point.

## Documentation Style

User manuals should integrate new capabilities into the chapter where users naturally look for them. Avoid disconnected "latest update" chapters unless requested.

Change notes should use newest-first ordering and group technical commits into user-visible outcomes. Each version or date section should explain the summary, impacted modules, user-visible changes, image notes, and usage advice.

## Safety Boundaries

- Do not commit real Feishu tokens, document URLs, private project profiles, login data, account screenshots, or generated local fetch output.
- Do not label handcrafted mockups as real UI.
- Do not run product build, typecheck, or e2e checks for documentation-only changes unless product code changed or screenshots require app verification.
- The scripts validate and generate commands; they do not automatically overwrite Feishu documents.
