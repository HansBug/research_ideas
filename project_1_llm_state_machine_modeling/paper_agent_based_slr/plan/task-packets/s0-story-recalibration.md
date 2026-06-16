# PR-S0 任务包：论文主线重新勘定

## 1. 目标

本 PR 是第二篇论文伞 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的阻塞性 PR-S0。目标是把论文主线从“LLM / 智能体自动化综述”收紧为：**面向软件工程 SLR/SMS 的研究者引导、发现导向、可审计智能体式支持工作流**。

本 PR 只冻结论文主线、术语、主张边界、新颖性差异、评价义务和后续 PR 门槛；不实现运行时、不跑真实 LLM、不跑四个真实例子、不冻结最终指标公式。

## 2. 背景事实

| 事实 | 对 PR-S0 的影响 |
|---|---|
| PR-B0 已完成 35 篇全文文本级基线调研，并发现 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻 | 不能继续写“首次智能体式 SLR”或“已有工作没有自动化综述工作流” |
| 2026-06-15 导师讨论明确：元模型应由使用本文方法的研究者基于脚手架设定 | 不能写成作者预设通用软件工程本体，也不能写成 LLM 自动定义可靠元模型 |
| 导师讨论强调 SLR 不只是整理文献，还要形成研究发现 | 后续方法必须围绕候选研究发现、证据链、质疑、修订、降级和最终接受来组织 |
| PR #97 仍 OPEN / 未合入 | 只能作为快照 / 分支局部证据，不能写成 `main` 已有事实 |

## 3. 允许修改范围

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/**`
- PR #101 / PR #114 body 与 comments

## 4. 不在本 PR 中修改

| 路径或资产 | 原因 |
|---|---|
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/**` | 基线文库已由 PR-B0 建立；本 PR 只消费结论 |
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/dataset_selection/**` | 场景选择属于后续 PR-A3 |
| `project_1_llm_state_machine_modeling/method/**` | 本 PR 不实现工作流代码 |
| `runs/**` | 本 PR 不跑真实 LLM，不新增运行记录 |
| `.env` | 本 PR 不触发 provider 调用，也不修改密钥配置 |
| PR #97 分支资产 | 仍按 OPEN / 快照 / 分支局部证据处理，不复制未合入资产 |

## 5. 必须回答的问题

| 问题 | 文件落点 | 验收方式 |
|---|---|---|
| 新的一句话论文主线是什么？ | [../../story/paper_story.md](../../story/paper_story.md) | 必须同时体现研究者引导、发现导向、可审计、智能体支持四个要素 |
| 哪些主张可以写、哪些必须谨慎、哪些禁止？ | [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) | 必须区分可写 / 待补证 / 禁止 / 依赖快照证据 |
| 与强近邻的差异化是什么？ | [../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) | 必须正面对齐 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 |
| 术语如何避免误读？ | [../../story/terminology_policy.md](../../story/terminology_policy.md) | 必须定义元模型、候选研究发现、最终研究发现、研究者审计、质疑闭环 |
| 后续 RQ 和评价义务如何接走？ | [../../story/paper_outline.md](../../story/paper_outline.md)、[../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | 必须映射到可追踪性、事实准确性、无证据支撑研究发现、审计拦截、覆盖代理、透明报告和成本 |
| 文档是否足够干净、自包含？ | [../progress.md](../progress.md)、本任务包、各入口 README、[../../evidence/project_inventory.md](../../evidence/project_inventory.md) | 应删除纯历史流水账；必要历史只保留为证据链接和当前事实来源；旧 A0 / B0 / PR #97 信息必须标清证据层级 |

## 6. 拒收检查

- 不能把第二篇写回 `sources` 语料 / 基准来源论文。
- 不能写智能体完全替代 SLR 专家。
- 不能写首次、完整自动化、PRISMA 合规、完整覆盖等被基线调研击穿的强主张。
- 不能把候选研究发现直接写成最终研究发现。
- 不能把 PR #97 OPEN / 未合入资产写成 `main` 事实。
- 不能把 PR-S0 扩展成完整协议、日志 schema、示例、survey-of-surveys 或脚手架实现。
- 不能把历史 PR review 过程堆成当前正文；当前 Markdown 应以自包含合同和最新结论为主。
- 不能让证据盘点停留在旧 A0 口径；[../../evidence/project_inventory.md](../../evidence/project_inventory.md) 必须包含 PR-S0 与 2026-06-15 导师定调入口。
- 不能运行真实 LLM；后续真实运行必须 `source .env` 并保存运行记录。

## 7. 验证命令

```bash
git status --short --branch
git diff --check origin/paper2/agent-based-slr-umbrella...HEAD
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr')
required = [
    root / 'README.md',
    root / 'story' / 'README.md',
    root / 'story' / 'paper_story.md',
    root / 'story' / 'paper_outline.md',
    root / 'story' / 'claim_evidence_map.md',
    root / 'story' / 'differential_novelty_matrix.md',
    root / 'story' / 'terminology_policy.md',
    root / 'experiment_design' / 'evaluation_dimensions_seed.md',
    root / 'experiment_design' / 'reviewer_risk_register.md',
    root / 'plan' / 'README.md',
    root / 'plan' / 'progress.md',
    root / 'plan' / 'task-packets' / 's0-story-recalibration.md',
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, missing
print('paper_agent_based_slr PR-S0 packet ok')
PY
```

## 8. 完成标准

- [../../story/paper_story.md](../../story/paper_story.md) 能独立解释论文主线、任务边界、方法阶段、Mermaid 方法总览图、候选贡献和禁止主张。
- [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) 能独立约束摘要、引言、贡献和结论的主张强度。
- [../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) 能独立说明与强近邻的差异化边界。
- [../../story/paper_outline.md](../../story/paper_outline.md) 能指导后续 A2/A3/A5/A6 的方法、场景、评价和写作。
- [../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) 明确哪些风险会影响学术叙事、证据链或实验可靠性。
- 当前 Markdown 以中文为主，必要英文仅作为术语锚点、论文 / 工具名、命令或文件路径出现。
- 当前 Markdown 应尽量干净、自包含：保留必要证据链接和当前合同，清除纯历史痕迹、过期状态和已修复 review 流水。
