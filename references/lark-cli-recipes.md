# lark-cli Recipes

Default identity:

```bash
--profile personal-feishu --as user
```

## Fetch Existing Document

```bash
lark-cli docs +fetch \
  --api-version v2 \
  --profile personal-feishu \
  --as user \
  --doc "$DOC_URL" > /tmp/doc-fetch.json
```

## Overwrite Existing Document

Current lark-cli versions may expose either `--mode`/`--markdown` or `--command`/`--content` depending on installation. Check `lark-cli docs +update --help` first and use the installed flags.

Common v2 shape:

```bash
lark-cli docs +update \
  --api-version v2 \
  --profile personal-feishu \
  --as user \
  --doc "$DOC_URL" \
  --mode overwrite \
  --markdown @"$MARKDOWN" \
  --dry-run
```

Then run the same command without `--dry-run`.

## Insert Image

Use relative file paths:

```bash
lark-cli docs +media-insert \
  --profile personal-feishu \
  --as user \
  --doc "$DOC_URL" \
  --selection-with-ellipsis "$ANCHOR" \
  --file "relative/path/to/image.png" \
  --caption "$CAPTION" \
  --align center
```

For videos, add:

```bash
--type file --file-view preview
```

## Verify Wiki Node

```bash
lark-cli wiki spaces get_node \
  --profile personal-feishu \
  --as user \
  --params "{\"token\":\"$NODE_TOKEN\"}" \
  --jq '{node_token:.data.node.node_token,obj_token:.data.node.obj_token,parent_node_token:.data.node.parent_node_token,title:.data.node.title}'
```

## Known Issues

- `docs +update overwrite` removes existing image/media blocks. Reinsert media afterward.
- `docs +media-insert --file` may reject absolute paths. Run from the repo root and use relative paths.
- `--selection-with-ellipsis` inserts media at the top-level ancestor of the matched block. Avoid anchors inside table cells or callouts unless that behavior is intended.
