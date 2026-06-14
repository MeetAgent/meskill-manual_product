# Document Patterns

## User Feature Manual

Use this pattern for docs that teach users how to use a product.

Recommended sections:

1. Title and reading note.
2. Customer/change-note links.
3. One-page capability overview.
4. Entry points and first action.
5. Feature modules in user workflow order.
6. Advanced flows and recovery paths.
7. Failure, billing, limits, or compatibility notes.
8. Practical scenarios.
9. Support and feedback.

Writing rules:

- Speak to external users. Avoid internal API names, test ids, state-machine details, and implementation labels.
- Explain when to use a feature, what the next user action is, and what to watch for.
- Put new capabilities into the existing chapter where they belong.
- Keep old feature names only when users still see them.

## User Change Note / Release Note

Use this pattern for versioned customer-facing updates.

Recommended structure:

1. Title, time range, and reading method.
2. Update record table with date, version range, changelog, and user impact.
3. Date sections in descending order.
4. For each date: summary, impacted modules, user-visible changes, images, usage advice.

Writing rules:

- Keep only user-visible changes.
- Group technical commits into user-facing outcomes.
- Mention behavior, entry points, limitations, and required user action.
- Do not list internal refactors unless they changed visible stability or reliability.

## Image Anchor Pattern

Use one full sentence before each image:

- `下图展示首页 Launch 的主要操作入口。`
- `下图展示 Reel 顶部的 Style 入口与视觉风格选择。`
- `下图展示 Ad Audit 的检测结果和处理建议。`

Do not use generic anchors like `如下图` or `截图如下`; they are hard to target safely.

## Captions

Captions should explain:

- Whether the image is a real UI screenshot or concept diagram.
- Which user step it supports.
- What the user should do next.

Good:

- `真实界面：选中图片后可进入 Reel，将当前图片作为视频参考素材。`
- `概念示意：生成失败后按归因类型选择重试、换图或调整内容。`

Bad:

- `截图1`
- `效果图`
- `如下`
