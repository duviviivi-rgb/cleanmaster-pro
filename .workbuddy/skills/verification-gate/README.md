# CC 验证关卡

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`verification-gate` 是一个可移植的只读审查技能，用于检查实现是否真正完成。

它设计用于编码看起来完成后的时刻：收集上下文、检查更改内容，并强制进行单独的验证通道，将结果标记为已验证、未验证或失败。

## 最适合

- 实现后验证
- 检查测试是否真正运行
- 报告完成前的边界情况审查
- 防止乐观的虚假完成消息

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/verification_context.py`

## 快速开始

```bash
python3 ./scripts/verification_context.py --repo /path/to/repo
```

然后从 `SKILL.md` 运行验证器工作流。

## 主机适配

- Claude Code: 强适配
- Codex: 强适配
- OpenClaw: 可行，但在主机支持单独验证器通道时最强
