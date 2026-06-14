# Visual Standards

## Default Size

Final inserted main images should be `1600x1000` PNG unless the user explicitly requests another ratio.

Allowed exceptions:

- Raw screenshots in `raw/` folders.
- Source images used to build final documentation images.
- Videos inserted as files with preview mode.

Do not put exceptions in the final media manifest unless the manifest explicitly marks them as non-main media.

## Real UI vs Concept Diagram

Use `真实界面` only when the image comes from:

- Real frontend rendering.
- Playwright locator screenshot.
- Browser or app screenshot of an actual UI state.
- Real page crop from an existing UI.

Use `概念示意` when the image is:

- Handcrafted.
- A flowchart.
- A simulated state.
- A stable explanatory diagram.

Never disguise a concept diagram as a real screenshot.

## Prohibited Final Image Content

Final customer-facing images must not contain:

- Login user names, avatars, account balances, or personal identifiers.
- Empty placeholder cards or blank galleries.
- Feishu editor toolbar, selection borders, or resize handles.
- Canvas select/pan toolbars unless the image is specifically documenting those controls.
- Huge blank canvas areas.
- Blurry far-away UI.
- Cropped text that changes the meaning.
- Wrong aspect-ratio examples, such as showing a 9:16 flow as a 16:9 horizontal card.

## Screenshot Cropping

Prefer feature-area crops:

- Result card.
- Dialog/modal body.
- Toolbar plus active dropdown.
- Storyboard panel.
- Split card group.
- Audit result panel.

Avoid full-page screenshots unless the section is about page-level navigation.

## 9:16 and 16:9 Rules

- Use vertical cards for 9:16 video and split previews.
- Use horizontal cards only for 16:9 video or landscape media.
- If a document compares both, label them clearly.
- For 9:16 full-screen behavior, state that the video remains centered at original ratio and is not stretched horizontally.

## Review Checklist

Before inserting media:

- `sips` or script confirms final image dimensions.
- `view_image` or visual inspection confirms no prohibited content.
- Captions match image type: `真实界面` or `概念示意`.
- Image content is large enough to read inside Feishu.
- Anchor sentence exists exactly once in Markdown.
