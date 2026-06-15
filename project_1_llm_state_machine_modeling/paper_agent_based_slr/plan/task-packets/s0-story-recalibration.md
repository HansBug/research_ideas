# PR-S0 任务包：story 重新勘定与 claim 边界重写

## 1. 范围

本 PR 是 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的阻塞性 PR-S0，承接已合入的 PR-A0 / PR-B0 / PR-S0-pre 以及 PR [#112](https://github.com/HansBug/research_ideas/pull/112) 的正式导师讨论记录，负责把第二篇论文的 story、novelty matrix、claim boundary、RQ 和 experiment obligation 重新勘定。

本 PR 的目标不是继续扩 baseline 搜索，也不是实现 agent runtime；它的目标是把 B0 已经击穿的宽泛自动化 story 收紧为 **researcher-guided, finding-oriented, auditable agentic SLR support workflow** 的论文主线，并把所有后续 PR-A2 / PR-A3 / PR-A5 / PR-A6 的前提条件重新冻结。

## 2. 允许修改文件

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/**`
- PR #101 body / comments

## 3. 本 PR 不修改

| 路径或资产 | 不修改理由 |
|---|---|
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/**` | baseline 文库已在 PR-B0 冻结，本 PR 只消费其结论，不回改 baseline 总账。 |
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/dataset_selection/**` | 场景选择与样本设计属于后续 PR-A3，不在 story re-calibration 本轮完成。 |
| `project_1_llm_state_machine_modeling/method/**` | 本 PR 仍是 story / claim / outline 冻结，不实现 workflow 代码。 |
| `runs/**` | 不跑真实 LLM，不新增运行记录。 |
| `.env` | 不触发 provider 调用，也不改本地密钥配置。 |
| PR #97 分支资产 | 仍按 OPEN / snapshot / 分支局部证据使用，不复制未合入资产。 |

## 4. 必需证据

- PR [#101](https://github.com/HansBug/research_ideas/pull/101)：第二篇 agent-based SLR 伞 PR。
- PR [#112](https://github.com/HansBug/research_ideas/pull/112)：2026-06-15 正式导师讨论，已归档到 `project_1_llm_state_machine_modeling/talks/`。
- [2026-06-15 正式导师讨论记录](../../../talks/2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md)：meta-model scaffold、candidate finding、challenge loop、final finding 边界与 PR-S0 硬门槛。
- [PR-B0 / baseline 总账](../../baselines/SUMMARY.md)：35 篇全文文本级近邻 review、D1--D7 与全 CCF discovery 结论。
- [PR-A0 story / claim-evidence 基线](../../story/paper_story.md)、[../../story/claim_evidence_map.md](../../story/claim_evidence_map.md)、[../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md)：A0 原 story 的安全边界与待重写位置。

## 5. 拒收检查

- 不能把第二篇继续写回 `sources` corpus / benchmark-source landscape paper。
- 不能写 agent 完全替代 SLR 专家。
- 不能写首次、完整自动化、PRISMA-compliant、complete coverage 或其他被 B0 打穿的强 claim。
- 不能把 `candidate finding` 直接写成 `final finding`，除非证据链和 researcher audit 已显式闭合。
- 不能把 PR #97 OPEN / 未合入资产写成 `main` fact。
- 不能把 PR-S0 的任务扩展成完整 protocol / log schema / examples、survey-of-surveys 或 scaffold 目录落地；这些只可作为后续子 PR。
- 不能运行真实 LLM；如后续真实运行必须 `source .env` 并保留 run record。

## 6. 验证命令

```bash
git status --short --branch
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
    root / 'evidence' / 'README.md',
    root / 'evidence' / 'project_inventory.md',
    root / 'experiment_design' / 'README.md',
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

## 7. Review gate

三路 reviewer 必须重点挑战：

1. 是否仍然保留宽泛自动化 SLR / 首次 / 完整覆盖 的旧 story。
2. 是否把 `candidate finding` / `final finding` 边界写清楚。
3. 是否把 PR-S0 误写成后续 scaffold / protocol / schema / examples 的全部落地。
4. 是否真正把 B0 的 baseline 结论和 PR #112 的导师讨论落到 `story / claim / outline / novelty matrix` 的重写，而不是只改措辞。
5. 是否仍能清楚解释 A2 / A3 / A5 / A6 的后续 gate。

## 8. PR-S0 完成标准

- `paper_story.md` 重新写成比 A0 更收紧、可审计、可降级的 story。
- `claim_evidence_map.md` 显式拆分可写 / 谨慎 / 禁止 claim。
- `differential_novelty_matrix.md` 反映 B0 + PR #112 对旧 story 的击穿。
- `paper_outline.md` 与实验义务保持一致，不再围绕被打穿的宽泛自动化叙事。
- 必要时更新 `experiment_design/reviewer_risk_register.md` 和 `plan/progress.md`，但不引入真实运行或 code-level 改动。
