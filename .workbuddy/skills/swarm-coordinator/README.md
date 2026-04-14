# CC 群体协调器

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`swarm-coordinator` 是一个可移植的多智能体协调技能，适用于对于单个单体智能体循环来说太大或太嘈杂的任务。

它保持协调器专注于规划和综合，而有界工作者处理研究、实现和验证。该技能打包组织模式，而不是主机特定的群体运行时。

## 最适合

- 广泛的代码库探索
- 跨文件 bug 搜索
- 并行审查或研究通道
- 需要在实现前进行显式综合的任务

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/task_board.py`

## 快速开始

```bash
python3 ./scripts/task_board.py \
  --goal "调查不稳定的 CI 失败" \
  --worker research \
  --worker implementation \
  --worker verification
```

然后使用 `SKILL.md` 中的协调器工作流。

## 主机适配

- Claude Code: 强适配
- Codex: 强适配
- OpenClaw: 适合轻量级或手动协调的群体
