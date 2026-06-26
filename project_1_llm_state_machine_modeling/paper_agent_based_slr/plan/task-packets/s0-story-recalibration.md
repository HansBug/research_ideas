# PR-S0-v2 任务包：论文主线重新勘定

## 1. 目标

本 PR 是第二篇论文伞 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的阻塞性 PR-S0-v2。目标是把论文主线从旧的“自动化综述 / evidence-workflow / candidate finding workflow”重新勘定为：**面向软件工程 SLR/SMS 的 researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach**。

本 PR 只冻结论文主线、术语、主张边界、新颖性差异、评价义务和后续 PR 门槛；不实现运行时、不跑真实 LLM、不跑四个真实例子、不冻结最终指标公式。

## 2. 背景事实

| 事实 | 对 PR-S0-v2 的影响 |
|---|---|
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) 已完成 35 篇全文文本级 baseline，并发现 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻 | 不能写 first / fully automated / complete lifecycle / PRISMA-compliant SLR。 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) 导师讨论确认 meta-model 由使用者 researcher 定义，agent 只提出 candidate findings，final findings 需 evidence chain + researcher audit | 不能写 LLM 自动定义 meta-model 或 final findings。 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) 导师讨论把真实 SLR 压实为“收集论文 → 维度 pattern 驱动的论文分析 → statistical analysis 与 research finding 形成” | 必须把 dimension pattern lifecycle、field-level content evidence、statistical-analysis-vs-finding 分层、HITL gates 写进 story。 |
| 导师建议 survey-of-surveys 可放宽范围，用于提取 dimension pattern，是低复杂度工作 | survey-of-surveys 是 scaffold / pattern prior，不是 target evidence pool 或 tertiary review。 |
| 导师建议先设定主题 pilot，再让硕士生使用方法并收集 human-LLM interaction process data | pilot 只验证 closure / feasibility；学生数据只支撑 method-evaluation findings，需伦理、匿名化、脱敏和教学关系隔离边界。 |
| PR #97 仍 OPEN / 未合入 | 只能作为 snapshot / 分支局部证据，不能写成 `main` fact。 |

## 3. 允许修改范围

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/project_inventory.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/fact_drift_policy.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/**`
- PR #101 / PR #114 body 与 comments

## 4. 不在本 PR 中修改

| 路径或资产 | 原因 |
|---|---|
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/**` | PR-B0 已建立 baseline 文库；本 PR 只消费结论。 |
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/dataset_selection/**` | 场景选择属于后续 A3。 |
| `project_1_llm_state_machine_modeling/method/**` | 本 PR 不实现工作流代码。 |
| `runs/**` | 本 PR 不跑真实 LLM，不新增 run record。 |
| `.env` | 本 PR 不触发 provider 调用，也不修改密钥配置。 |
| PR #97 分支资产 | 仍按 OPEN / snapshot / 分支局部证据处理，不复制未合入资产。 |

## 5. 必须回答的问题

| 问题 | 文件落点 | 验收方式 |
|---|---|---|
| 新的一句话论文主线是什么？ | [../../story/paper_story.md](../../story/paper_story.md) | 必须同时体现 researcher-guided、pattern-evolving、evidence-backed、finding-oriented。 |
| 三阶段 SLR 如何转成 L0--L7 方法合同？ | [../../story/paper_story.md](../../story/paper_story.md)、[../../story/protocol.md](../../story/protocol.md) | 必须包含论文收集、dimension schema、field evidence、statistical analysis、candidate signal、challenge/adjudication。 |
| dimension pattern lifecycle 如何表达？ | [../../story/protocol.md](../../story/protocol.md)、[../../story/terminology_policy.md](../../story/terminology_policy.md) | 必须有 schema version、change trigger、impact analysis、backfill status。 |
| statistical analysis 与 research finding 如何拆分？ | [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md)、[../../story/paper_outline.md](../../story/paper_outline.md) | 禁止频次 / 分布 / 交叉表直接升级 final finding。 |
| content evidence 与 process evidence 如何分工？ | [../../story/terminology_policy.md](../../story/terminology_policy.md)、[../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | target-domain finding 只能由 content evidence 支撑；method-evaluation finding 才使用 process evidence。 |
| survey-of-surveys 如何定位？ | [../../story/protocol.md](../../story/protocol.md)、[../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) | 它是 scaffold / pattern prior，不是目标 evidence pool，不是 PRISMA tertiary review。 |
| pilot 与硕士生过程数据如何写？ | [../../story/paper_outline.md](../../story/paper_outline.md)、[../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) | pilot 只验证 feasibility；学生数据只评价方法，需 consent / anonymization / redaction。 |
| 文档是否足够干净、自包含？ | [../progress.md](../progress.md)、本任务包、各入口 README | 删除纯历史流水账；必要历史只保留为证据链接和当前事实来源。 |

## 6. 拒收检查

- 不能把第二篇写回 `sources` 语料 / 基准来源论文。
- 不能写智能体完全替代 SLR 专家。
- 不能写首次、完整自动化、PRISMA 合规、完整覆盖等被 baseline 调研击穿的强主张。
- 不能把统计分析直接写成 final research finding。
- 不能把 LLM/agent candidate signal 写成 final finding。
- 不能把 process evidence 或 student logs 用于 target-domain findings。
- 不能把 survey-of-surveys 写成目标 evidence pool、complete tertiary review 或 PRISMA-compliant tertiary review。
- 不能把 pilot / student process data 写成泛化证明或已完成结果。
- 不能让 human-in-the-loop 退化为末端 sign-off。
- 不能把 dimension pattern 写成一次性平铺字段表而无 revision/backfill。
- 不能把 PR #97 OPEN / 未合入资产写成 `main` 事实。
- 不能运行真实 LLM；后续真实运行必须 `source .env` 并保存 run record。

## 7. 验证命令

```bash
git status --short --branch
git diff --check
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr')
required = [
    root / 'README.md',
    root / 'story' / 'README.md',
    root / 'story' / 'paper_story.md',
    root / 'story' / 'protocol.md',
    root / 'story' / 'terminology_policy.md',
    root / 'story' / 'claim_evidence_map.md',
    root / 'story' / 'differential_novelty_matrix.md',
    root / 'story' / 'paper_outline.md',
    root / 'experiment_design' / 'evaluation_dimensions_seed.md',
    root / 'experiment_design' / 'reviewer_risk_register.md',
    root / 'plan' / 'README.md',
    root / 'plan' / 'progress.md',
    root / 'plan' / 'task-packets' / 's0-story-recalibration.md',
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, missing
print('paper_agent_based_slr PR-S0-v2 packet ok')
PY
# 强主张 / 旧叙事 grep 只作为人工审查线索，不是直接 pass/fail gate；
# 命中若位于禁止写法、风险、限制或 grep 规则本身语境，可判为通过。
rg -n -i "first automated|first agentic|complete coverage|PRISMA-compliant|LLM final|agent-generated final|process evidence supports target|student data shows|pilot proves|tertiary review|evidence package|证据包|finding-centered|研究发现为中心|report-generation|报告生成" \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/story \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/project_inventory.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/progress.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/task-packets/s0-story-recalibration.md
```

Mermaid 渲染验收需使用 no-sandbox 配置：

```bash
python - <<'PY'
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md')
text = p.read_text(encoding='utf-8')
start = text.index('```mermaid') + len('```mermaid')
end = text.index('```', start)
Path('/tmp/pr114_s0v2_method.mmd').write_text(text[start:end].strip() + '\n', encoding='utf-8')
PY
cat >/tmp/puppeteer-no-sandbox-pr114.json <<'JSON'
{"args":["--no-sandbox","--disable-setuid-sandbox"]}
JSON
mmdc -p /tmp/puppeteer-no-sandbox-pr114.json -i /tmp/pr114_s0v2_method.mmd -o /tmp/pr114_s0v2_method.svg
```

## 8. 完成标准

- [../../story/paper_story.md](../../story/paper_story.md) 能独立解释新 story、三阶段 SLR、L0--L7、G0--G6、方法图、候选贡献和禁用主张。
- [../../story/protocol.md](../../story/protocol.md) 明确 dimension lifecycle、statistical-analysis-to-finding 转移、content/process evidence 边界和 human gate contract。
- [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) 能约束摘要、引言、贡献和结论的主张强度。
- [../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) 能说明与强近邻的安全差异化。
- [../../story/paper_outline.md](../../story/paper_outline.md) 能指导后续 A2/A3/A5/A6 的方法、pilot、process evaluation 和写作。
- [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) 明确 pattern stability、backfill、field evidence、statistical correctness、candidate-to-final transition 和 process metrics。
- [../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) 登记统计/finding 混淆、证据类型混用、survey-of-surveys 误定位、pilot 过度外推、学生数据伦理等 C/I 风险。
- 当前 Markdown 以中文为主，必要英文仅作为术语锚点、论文 / 工具名、命令或文件路径出现。
- 当前 Markdown 应尽量干净、自包含：保留必要证据链接和当前合同，清除纯历史痕迹、过期状态和已修复 review 流水。
