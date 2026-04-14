# CC 主动任务调度

> **来源说明**：本技能源自 GitHub 开源项目 [cc-harness-skills](https://github.com/badfy32/cc-harness-skills)，由 [qinjian0618](https://cnb.cool/qinjian0618) 进行中文化改造，并适配 [WorkBuddy](https://workbuddy.cc) 工具链。

`kairos-lite` 是一个可移植的主动智能体技能，用于定期检查和短暂的后台任务。

它提取主动模式的有用部分：计划、休眠、简报和过期。它有意避免假设永久守护进程或私有主机通知系统。

## 最适合

- 仓库巡逻任务
- 后续检查
- 简明风格状态消息
- 具有固定过期窗口的主动工作

## 包含文件

- `SKILL.md`
- `references/prompt-template.md`
- `references/source-notes.md`
- `scripts/job_spec.py`

## 快速开始

```bash
python3 ./scripts/job_spec.py \
  --name "daily-repo-check" \
  --prompt "总结仓库中的风险变更" \
  --schedule "0 9 * * 1-5"
```

然后将生成的任务规格映射到主机自动化流程。

## 主机适配

- Claude Code: 强适配
- Codex: 可行，但需要主机自动化支持
- OpenClaw: 强适配
