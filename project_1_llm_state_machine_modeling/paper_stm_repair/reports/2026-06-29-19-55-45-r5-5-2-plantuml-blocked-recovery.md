# R5.5.2 PlantUML blocked recovery update

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位

本 report 记录 PR-R5.5.2 对 `llms-emp-stm-subset` 三个 PlantUML blocked 样例的转换前恢复结果。它**只覆盖 R5.5.2 的增量事实**：在不改 raw `pairs.jsonl` / 一手资源、不新增 parallel pipeline、不把 conversion recovery 计入 repair gain 的前提下，现有 PlantUML pre-SCXML normalization / recovery 环节让三个原 blocked 样例可经 official PlantUML SCXML 路径进入 `.fcstm` readiness 画像 [clm-r552-boundary][clm-r552-no-repair-gain]。

本 report supersede 旧 R5.5 main seed profile / negative evidence report 中关于 `llms-emp` blocked 数量与三个 blocked row 的当前性；旧 report 仍可用于理解 R5.5.1 前的历史画像、特征矩阵和方向性讨论，但当前状态数字必须以本 report 与当前 machine artifacts 为准 [clm-r552-status][src-r552-case]。

## 2. 核心结论

1. `llms-emp-stm-subset` 当前仍是 `60 = 10` 个唯一 NL cluster × `6` 个 LLM 输出；R5.5.2 后 pair 状态为 `converted=16 / partial=44 / blocked=0`，且 60 条 `canonical_status` 均为 `converted`、`parse_status=ok`、`inspect_status=ok` [clm-r552-status][cmd-r552-status]。
2. 三个原 blocked 样例 `0018`、`0028`、`0037` 均已变为 `partial`，但都带有 `R5.LOSS.r3_1_normalization_replay_not_repair`，因此只能说明 conversion readiness 恢复，不能写成 repair loop 修复收益 [clm-r552-targets][clm-r552-no-repair-gain]。
3. 与 R5.5 base matrix 相比，`llms-emp` 60 条中只有这三个目标样例发生状态变化：`blocked -> partial`；其余 57 条没有从 `converted/partial` 退化，关键 source trace 字段保持一致 [clm-r552-no-regression][cmd-r552-no-regression]。注意：一次完整重跑会刷新部分已是 `partial` 的派生 `.fcstm` / loss attribution，已观测到 `llms_emp_stm_results_0024` 的 `fcstm_sha256` 与 `r5_loss_codes` 发生非状态漂移；这不是新增 recovery target，也不改变其 `partial`/source trace 结论 [clm-r552-derived-drift]。
4. 全 seed sweep 的 pair 状态同步从 `converted=529 / partial=504 / blocked=23 / not_applicable=20 / needs_generation=2` 变为 `converted=529 / partial=508 / blocked=19 / not_applicable=20 / needs_generation=2`。除三个 `llms-emp` 目标外，`unified_uml_state_train_0265` 也因同一低风险 normalization 规则被 collateral 恢复为 partial；该 synthetic collateral 只能作为 conversion audit fact，不改变 paper 主 seed 定位 [clm-r552-global][cmd-r552-no-regression]。
5. 学术 story 的主边界不因此扩张：T0 离散 FSM/HSM/UML-SysML statechart artifacts 仍是主线；Digital Camera / T1 cluster 仍只能作为 supplementary stress，guard/action/time 的语义抽象问题仍留给 R5.7 / R6 之后逐例裁决 [clm-r552-scope]。

## 3. 三个恢复样例明细

| raw_pair_id | LLM | NL cluster | R5.5 base 状态 | R5.5.2 状态 | 本次触发的低风险规则 | 当前主要 caveat |
|---|---|---|---|---|---|---|
| `llms_emp_stm_results_0018` | GPT-4 | Digital Camera / T1 | `blocked` | `partial` | `PUML.NORM.alias_multiword_endpoint`、`PUML.NORM.transition_when_label` | 条件式 label 仍可能被 lowering 为 event；跨层级迁移、initial inference 与 source lifting caveat 仍在。 |
| `llms_emp_stm_results_0028` | Llama | Digital Camera / T1 | `blocked` | `partial` | `PUML.NORM.remove_stm_heading`、`PUML.NORM.remove_empty_transition_label` | 条件式 label 仍可能被 lowering 为 event；Digital Camera 仍是 supplementary stress。 |
| `llms_emp_stm_results_0037` | Kimi | Collision Avoidance / T0 | `blocked` | `partial` | `PUML.NORM.remove_stm_heading`、`PUML.NORM.alias_bracket_endpoint` | 仅恢复转换入口；并发/区域语义与后续 representation caveat 仍需 R5.7/R6 处理。 |

## 4. 当前计数快照

### 4.1 `llms-emp` 60 pair

| conversion_status | pairs |
|---|---:|
| `converted` | 16 |
| `partial` | 44 |
| `blocked` | 0 |

### 4.2 全 seed sweep pair

| status | pairs |
|---|---:|
| `converted` | 529 |
| `partial` | 508 |
| `blocked` | 19 |
| `not_applicable` | 20 |
| `needs_generation` | 2 |

### 4.3 PlantUML recovery report

| 指标 | 数量 |
|---|---:|
| PlantUML 一手 pair 总数 | 1049 |
| 原始官方 SCXML 已可转换 | 550 |
| 原始失败 | 499 |
| all-rules 技术通过 | 480 |
| low-risk / main eligibility 通过 | 470 |
| normalization 后仍失败 | 19 |
| `llms-emp-stm-subset` failed after | 0 |

## 5. 学术风险与禁止主张

1. 禁止把本次 `blocked -> partial` 写成 Better STM repair loop 的效果；它发生在 official SCXML 之前的 conversion readiness 层 [clm-r552-no-repair-gain]。
2. 禁止把 `partial` 直接写成语义正确。三个恢复样例均仍有 loss code 或 caveat；`partial` 的含义是“可进入后续资格审查 / 修正候选池”，不是“无损转换” [clm-r552-targets]。
3. 禁止用 synthetic collateral `unified_uml_state_train_0265` 影响 `llms-emp` 主 seed story；它只能说明 normalization 规则的全局副作用被记录并可审计 [clm-r552-global]。
4. R5.6 scope 可删除“`llms-emp` blocked negative evidence”作为当前事实，但不能删除 Digital Camera/T1 supplementary stress、conversion gain 不计 repair gain、guard/action/time 需后续裁决这些限制 [clm-r552-scope]。

## 6. 后续入口

- R5.5 收口：以本 report 更新 [STATUS.md](../STATUS.md)、[reports/SUMMARY.md](./SUMMARY.md) 与 PR #134 comment。
- R5.6：更新 paper story / model scope 时，应把 `llms-emp` 当前状态写成 `16 converted / 44 partial / 0 blocked`，并保留 T0 主线与 Digital Camera supplementary stress。
- R5.7/R6：优先处理 `condition_like_label_lowered_as_event`、层级 boundary lowering、并发/区域与 timer-like caveat；这些不是 R5.5.2 已解决的问题。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md` | 本 PR 工作树创建；提交后以本文件 git history 为准 | `2026-06-29 19:55:45 +0800` | R5.5.2 重新运行 PlantUML recovery、seed sweep 与 llms-emp profile 后形成新的当前事实：`llms-emp blocked=0`。 | 无 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json)、[sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) |

> 注：`plantuml_recovery_report.json` 与 `manifest.json` 中的 `generator_code_commit` 记录的是 clean generator 代码提交（生成 artifact 前的代码状态），而不是承载 artifact 的最终 commit；这是为了避免 report 自指 hash / artifact commit 递归问题。复核时应同时检查 `generator_worktree_dirty=false` 与当前 PR diff 中 artifact 文件是否同步提交。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-r552-case] | `case_matrix` | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | `jsonl` | 支撑 60 pair 当前状态、三个恢复样例与 source trace | `conversion_status`、`canonical_status`、`raw_pair_id in {0018,0028,0037}` |
| [src-r552-partial] | `partial_ledger` | [llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | `jsonl` | 支撑 44 条 partial 归因与 no-repair-gain caveat | `r5_loss_code`、`repair_contribution_allowed=false` |
| [src-r552-blocked] | `blocked_probe` | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) | `jsonl` | 支撑当前 `llms-emp blocked=0` | row count = 0 |
| [src-r552-recovery] | `plantuml_recovery_report` | [plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) | `json` | 支撑 official PlantUML recovery、rule ids 与 low-risk / main eligibility 统计 | `summary.by_seed.llms-emp-stm-subset.failed_after=0`、`items[pair_id]` |
| [src-r552-ledger] | `normalization_ledger` | [plantuml_normalization_ledger.jsonl](../pipeline/conversion/reports/plantuml_normalization_ledger.jsonl) | `jsonl` | 支撑每条 normalization 变更的 rule id/source locator/raw hash | rows with target `pair_id` |
| [src-r552-sweep] | `sweep_report` | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) | `json` | 支撑全 seed sweep 当前 pair 状态 | `summary.pair_status_counts` |
| [src-r552-index] | `records_index` | [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) | `json` | 支撑全局 no-regression 与 collateral unified row 定位 | `record_id`、`status`、`archive_path` |
| [src-r552-archive] | `record_archives` | [artifact archives](../pipeline/readiness_audit/artifact_archives/archives/) | `zip` | 支撑高基数 per-pair record 复验 | `llms-emp-stm-subset_records/*.json`、`unified-uml-multimodal-validation_records/*.json` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r552-boundary] | `R5.5.2-C0` | 本 report 只覆盖 PlantUML pre-SCXML recovery，不新增 pipeline、不修改 raw assets。 | `prohibition` | [src-r552-case] source hash fields；PR diff 不含 `corpora/.../assets/raw` / `pairs.jsonl`。 | [cmd-r552-no-regression] | `high` | 不能据此声称修正循环已运行。 |
| [clm-r552-status] | `R5.5.2-C1` | `llms-emp` 当前为 `converted=16 / partial=44 / blocked=0`。 | `count` | [src-r552-case] `conversion_status`；[src-r552-blocked] row count。 | [cmd-r552-status] | `high` | readiness 状态，不是最终实验结果。 |
| [clm-r552-targets] | `R5.5.2-C2` | 三个原 blocked 样例 `0018/0028/0037` 均恢复为 `partial`，canonical/parse/inspect 均可用。 | `trace` | [src-r552-case] rows by `raw_pair_id`；[src-r552-recovery] matching `items[pair_id]`。 | [cmd-r552-status] | `high` | `partial` 不等于语义无损。 |
| [clm-r552-no-regression] | `R5.5.2-C3` | 相对 R5.5 base，`llms-emp` 只有三个目标样例从 `blocked` 改为 `partial`，其余 57 条无状态退化且 source trace 不变。 | `trace` | `git show origin/paper1/r5.5-llms-emp-deep-profile:...case_matrix.jsonl` vs [src-r552-case]。 | [cmd-r552-no-regression] | `high` | 只比较 case matrix 的状态和 source trace 字段；不证明模型语义完全等价，也不承诺派生 `.fcstm` hash 完全不漂移。 |
| [clm-r552-derived-drift] | `R5.5.2-C3b` | 完整重跑中 `llms_emp_stm_results_0024` 出现非状态派生漂移：`fcstm_sha256` 与 `r5_loss_codes` 更新，但 `conversion_status=partial`、source trace 与 repair-gain 禁止口径不变。 | `trace` | R5.5 base case matrix vs [src-r552-case] row `llms_emp_stm_results_0024`。 | [cmd-r552-no-regression] 的补充 diff 检查 | `medium` | 这说明 no-regression gate 是“状态/source trace 不退化”，不是 bit-for-bit artifact freeze。`target_lifted_to_composite_boundary` 到 `composite_target_lowered_to_initial_child` 的归因方向变化对后续 repair target 可能有语义影响；R5.7/R6 若依赖 0024，应回到 raw STM/SCXML/FCSTM 做逐例复核。 |
| [clm-r552-global] | `R5.5.2-C4` | 全 seed sweep 当前为 `converted=529 / partial=508 / blocked=19 / not_applicable=20 / needs_generation=2`，其中 `unified_uml_state_train_0265` 是 collateral `blocked -> partial`。 | `count` | [src-r552-sweep] `summary.pair_status_counts`；[src-r552-index] record status diff。 | [cmd-r552-no-regression] | `high` | unified synthetic collateral 不进入主 seed claim。 |
| [clm-r552-recovery] | `R5.5.2-C5` | PlantUML recovery 后 `llms-emp-stm-subset.failed_after=0`，全局 low-risk/main eligibility 为 470。 | `count` | [src-r552-recovery] `summary.by_seed.llms-emp-stm-subset` 与 `summary.main_eligibility_included`。 | [cmd-r552-recovery] | `high` | conversion eligibility，不是 repair success。 |
| [clm-r552-no-repair-gain] | `R5.5.2-C6` | R5.5.2 recovery 不得计入 repair gain。 | `prohibition` | [src-r552-partial] `R5.LOSS.r3_1_normalization_replay_not_repair`；[src-r552-recovery] `conversion_contract`。 | [cmd-r552-status] | `high` | 后续 paper 只能把它写成输入可用性恢复。 |
| [clm-r552-scope] | `R5.5.2-C7` | 当前 scope 仍应保持 T0 主线 + Digital Camera supplementary stress；只是 `llms-emp` blocked negative evidence 不再作为当前事实。 | `decision` | [src-r552-case] `time_level`、`r5_6_story_role`、target rows；[src-r552-partial] caveat。 | [cmd-r552-status] | `medium` | R5.6/R5.7 仍需正式 story/protocol 冻结。 |

### A.4 复验命令

[cmd-r552-status]

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/src \
python -m paper_stm_repair_smoke.cli validate
python - <<'PY'
import json, collections
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile')
rows = [json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
print(collections.Counter(r['conversion_status'] for r in rows))
for pid in ['llms_emp_stm_results_0018','llms_emp_stm_results_0028','llms_emp_stm_results_0037']:
    print(pid, next(r for r in rows if r['raw_pair_id'] == pid)['conversion_status'])
PY
```

[cmd-r552-no-regression]

```bash
git show origin/paper1/r5.5-llms-emp-deep-profile:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl > /tmp/r5_5_llms_emp_case_matrix.baseline.jsonl
python - <<'PY'
import json
from pathlib import Path
from collections import Counter
base_path = Path('/tmp/r5_5_llms_emp_case_matrix.baseline.jsonl')
new_path = Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl')
target = {'llms_emp_stm_results_0018', 'llms_emp_stm_results_0028', 'llms_emp_stm_results_0037'}
rank = {'converted': 0, 'partial': 1, 'blocked': 2}
base = {json.loads(line)['raw_pair_id']: json.loads(line) for line in base_path.read_text(encoding='utf-8').splitlines() if line.strip()}
new = {json.loads(line)['raw_pair_id']: json.loads(line) for line in new_path.read_text(encoding='utf-8').splitlines() if line.strip()}
assert len(base) == 60 and len(new) == 60
assert set(base) == set(new)
assert {pid for pid, row in base.items() if row['conversion_status'] == 'blocked'} == target
for pid, old in base.items():
    cur = new[pid]
    for key in ['nl_sha256', 'stm0_sha256', 'source_sha256', 'nl_source_locator', 'stm_source_locator']:
        assert old.get(key) == cur.get(key), (pid, key)
    if pid not in target:
        assert rank[cur['conversion_status']] <= rank[old['conversion_status']], (pid, old['conversion_status'], cur['conversion_status'])
for pid in target:
    assert new[pid]['conversion_status'] == 'partial'
print('baseline:', Counter(row['conversion_status'] for row in base.values()))
print('current:', Counter(row['conversion_status'] for row in new.values()))
PY
```

[cmd-r552-recovery]

```bash
export PLANTUML_JAR=/tmp/paper1_tools/plantuml.jar
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_conversion.cli recover-plantuml \
  --reports-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports \
  --run-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir \
  --archive-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed \
  --run-id r5.5.2-plantuml-blocked-recovery \
  --created-at 2026-06-29T20:18:00+08:00
```
