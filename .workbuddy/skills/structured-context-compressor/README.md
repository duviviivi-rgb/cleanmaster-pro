# CC 上下文压缩器

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`structured-context-compressor` 是一个可移植的连续性摘要技能，用于长编码会话。

它不是模糊的自由形式摘要，而是生成一个九部分工件，保留请求、文件、错误、用户消息、待处理工作、当前工作和下一步对齐步骤。

## 最适合

- 长编码对话
- 智能体交接
- 上下文压力后的继续
- 保留用户修正和约束

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/render_template.py`

## 快速开始

```bash
python3 ./scripts/render_template.py
```

然后使用 `SKILL.md` 中的工作流填充生成的结构。

## 主机适配

- Claude Code: 强适配
- Codex: 强适配
- OpenClaw: 强适配
