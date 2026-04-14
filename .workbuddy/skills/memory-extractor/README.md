# CC 记忆提取器

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`memory-extractor` 是一个可移植技能，用于从最近轮次中提取持久的协作记忆。

它存储四类稳定记忆：`user`、`feedback`、`project` 和 `reference`。核心设计规则很简单：记住持久的偏好和约束，但不要存储应该从源代码重新读取的漂移代码事实。

## 最适合

- 捕获用户偏好
- 保存工作风格反馈
- 记录非代码项目约束
- 存储稳定的外部引用

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/memory_manifest.py`

## 快速开始

```bash
python3 ./scripts/memory_manifest.py --memory-root /path/to/memory
```

然后使用 `SKILL.md` 中的提取流程。

## 主机适配

- Claude Code: 强适配
- Codex: 强适配
- OpenClaw: 强适配
