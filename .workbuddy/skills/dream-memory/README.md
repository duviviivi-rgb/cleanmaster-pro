# CC 梦境记忆

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`dream-memory` 是一个可移植的记忆整合技能，用于编码智能体。

它将最近的日志、会话记录和现有记忆文件转换为更简短、更稳定的长期记忆集合。该工作流灵感来自公开的 `CC` 梦境风格记忆通道，但已重写以避免私有运行时依赖。

## 最适合

- 夜间记忆清理
- 合并重复的记忆笔记
- 将相对日期转换为绝对日期
- 保持 `MEMORY.md` 简短且对提示词友好

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/dream_memory.py`

## 快速开始

```bash
python3 ./scripts/dream_memory.py \
  --memory-root /path/to/memory \
  --transcripts-dir /path/to/transcripts
```

然后使用 `SKILL.md` 中的工作流和 `references/prompt-template.md` 中的提示词模板。

## 主机适配

- Claude Code: 强适配
- Codex: 强适配
- OpenClaw: 强适配
