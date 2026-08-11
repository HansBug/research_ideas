# R5.5 -> R5.6 story / model scope handoff


> **R5.5.2 当前性提示：** 本 handoff 中 `blocked=3 / partial=41`、“3 个 blocked 进入 negative evidence”等状态数字是 R5.5.1 历史快照，已被 [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) supersede；当前 `llms-emp` 为 `16 converted / 44 partial / 0 blocked`。R5.6 仍应保留 T0 主线、T0.5 caveat 与 Digital Camera supplementary stress，但不得把本 handoff 的 blocked 数字当作当前状态。

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排；新增证据时只新增 key，不批量改旧 key。

## R5.5 -> R5.6 story / model scope handoff

### 1. boundary_decision

`proceed_with_supplementary` [clm-scope-boundary]

R5.5.1 历史理由：10 个 NL cluster 中 8 个为 T0、1 个为 T0.5、1 个为 T1；当时 60 个 pair 中 57 个可进入 `.fcstm` 级别，3 个 blocked 有负证据。R5.5.2 后 blocked 已恢复为 partial，但时间等级和 Digital Camera stress 判断不变。主实验应以 T0 离散状态机族为核心继续推进；T0.5 只作为 timer-like cue under event abstraction 的 caveat 样本单独标注。Digital Camera/T1 cluster 与 blocked pair 应进入 supplementary / stress / negative evidence，而不是主 claim 证据 [clm-scope-pair-counts][clm-scope-time-level][clm-scope-supplementary-negative]。

### 2. supporting_counts（R5.5.1 历史快照）

- pair status: `{'blocked': 3, 'converted': 16, 'partial': 41}`
- pair time level: `{'T0': 48, 'T0.5': 6, 'T1': 6}`
- cluster time level: `{'T0': 8, 'T0.5': 1, 'T1': 1}`
- story roles: `{'main_candidate': 53, 'negative_evidence': 3, 'supplementary_stress': 4}`
- partial ledger rows: `41`
- blocked rows: `3`

### 3. blocking_evidence

- 3 个 blocked 均为 `R5.LOSS.official_scxml_unavailable`，详见 [negative evidence report](./2026-06-28-23-18-32-negative-evidence-report.md)（内含 blocked probe 分析）[clm-scope-supplementary-negative][src-scope-negative-report]。
- Digital Camera cluster 含显式秒级执行时间与复杂 pseudo-state，应避免支撑 T0 主 claim [clm-scope-supplementary-negative]。
- 大量 partial 来自 conversion / representation attribution，不能计入 repair gain [clm-scope-candidate-risk][src-scope-partial-ledger]。

### 4. confidence

`medium`：一手 pair / R5 sweep / R3.1 recovery / R4.5 loss 证据较完整；但 time level 与 repair target taxonomy 仍需 R5.6/R5.7 正式冻结，因此 scope decision 不升级为 high [clm-scope-boundary]。

### 5. r5_7_candidate_summary

- `R45.LOSS.condition_like_label_lowered_as_event` 是主要 repair target 候选，但必须逐例有 NL 证据 [clm-scope-candidate-risk]。
- 层次 lowering、scope lifting、initial inference 默认是 representation caveat，不直接进入 repair target。
- blocked official SCXML unavailable 是 converter follow-up / negative evidence，不是 repair loop 能直接声称修复的问题。

### 6. recommended_next_action

R5.6 应在 [archived experiment_design/scope/](../archive/r5_7_better_stm_snapshot/experiment_design/scope/) 中冻结 main / supplementary-stress / negative evidence 的模型范围，；当前 active scope 以 [../story/model_scope.md](../archive/r8_discover_repair_story/story/model_scope.md) 为准，`story/` 不再引用旧 scope 作为唯一事实源，不另建第二事实真源；主实验 claim 应限定到 T0 离散状态机族；T0.5 只作为 timer-like caveat under event abstraction 的补充样本，R5.7 再定义 guard/event/action/hierarchy 的 repair target [clm-scope-boundary][clm-scope-candidate-risk]。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_r56_handoff.md` | `ee35e44407c85835dc4f3ec669477e298d89cb8a` (2026-06-28 22:54:39 +0800) | `ee35e44407c85835dc4f3ec669477e298d89cb8a` (2026-06-28 22:54:39 +0800, scope handoff fact freeze) | `ee35e44407c85835dc4f3ec669477e298d89cb8a`：首次给出 `proceed_with_supplementary` 边界裁决、T0/T0.5/T1 计数、Digital Camera supplementary stress 与 blocked negative evidence 处理。 | `1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)；[llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)；[llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl)；[negative evidence report](./2026-06-28-23-18-32-negative-evidence-report.md) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-scope-case] | `case_matrix` | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | `jsonl` | 支撑 pair-level `conversion_status`、`time_level`、`r5_6_story_role` 与 blocked 数 | fields: `conversion_status`、`time_level`、`r5_6_story_role` |
| [src-scope-clusters] | `cluster_profiles` | [llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | `jsonl` | 支撑 cluster-level T0/T0.5/T1 和 Digital Camera supplementary stress | fields: `time_level`、`time_level_note`、`r5_6_story_role` |
| [src-scope-partial-ledger] | `partial_ledger` | [llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | `jsonl` | 支撑 partial attribution 和 R5.7 candidate-only 边界 | fields: `primary_attribution`、`attribution_confidence`、`r5_7_candidate_only` |
| [src-scope-blocked] | `blocked_probe` | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) | `jsonl` | 支撑 3 blocked 进入 negative evidence 的依据 | rows: `raw_pair_id in {0018,0028,0037}` |
| [src-scope-negative-report] | `negative_report` | [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | `md` | 人类可读 blocked caveat；机器事实仍回到 `blocked_probe` | `Claim-evidence map` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-scope-boundary] | `R5-SCOPE-C1` | boundary decision 为 `proceed_with_supplementary`。 | `decision` | `case_matrix` counts + `cluster_profiles` time profile + `blocked_probe` | [cmd-scope-summary] | `medium` | 这是对 scope decision 的置信度，不是对 repair effectiveness 的置信度。 |
| [clm-scope-pair-counts] | `R5-SCOPE-C2` | R5.5.1 历史 pair count 为 `blocked=3 / converted=16 / partial=41`；当前 R5.5.2 状态为 `blocked=0 / converted=16 / partial=44`；time level 仍为 `T0=48 / T0.5=6 / T1=6`。 | `historical_count + currentness` | 本 report 历史快照 + R5.5.2 recovery report；当前 `case_matrix` 仅支持 16/44/0。 | [cmd-scope-summary] 当前分支会输出 current status | `high` | pre-repair profile，不是最终实验结果；历史 blocked 不再是当前 blocked。 |
| [clm-scope-time-level] | `R5-SCOPE-C3` | cluster time level 为 `T0=8 / T0.5=1 / T1=1`。 | `count` | `cluster_profiles.time_level` | [cmd-scope-summary] | `high` | T0.5 是 timer-like cue under event abstraction，不是 timed automata 覆盖。 |
| [clm-scope-supplementary-negative] | `R5-SCOPE-C4` | Digital Camera / T1 进入 supplementary-stress；R5.5.1 历史 blocked 进入 negative evidence，但当前已恢复为 partial。 | `classification + currentness` | `cluster_profiles.r5_6_story_role`、历史 `blocked_probe`、R5.5.2 recovery report。 | [cmd-scope-summary] | `high` | supplementary / historical negative 不支撑 T0 主 claim；不得把历史 blocked 写成当前 blocked。 |
| [clm-scope-candidate-risk] | `R5-SCOPE-C5` | `condition_like_label_lowered_as_event` 只作为 R5.7 候选。 | `risk` | `partial_ledger` rows with `r5_loss_code=R45.LOSS.condition_like_label_lowered_as_event` | [cmd-scope-summary] | `medium` | 必须逐例有 NL 和 raw STM_0 证据后才可升级为 repair target。 |

### A.4 复验命令

```bash
# [cmd-scope-summary] CMD-SCOPE-1 / CMD-SCOPE-2 / CMD-SCOPE-3 / CMD-SCOPE-4 / CMD-SCOPE-5
python - <<'PY'
import json, collections, pathlib
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/llms_emp_profile')
case=[json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters=[json.loads(l) for l in (base/'llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
partial=[json.loads(l) for l in (base/'llms_emp_partial_attribution_ledger.jsonl').read_text().splitlines() if l.strip()]
blocked=[json.loads(l) for l in (base/'llms_emp_blocked_probe.jsonl').read_text().splitlines() if l.strip()]
print('pair_status', collections.Counter(r['conversion_status'] for r in case))
print('pair_time', collections.Counter(r['time_level'] for r in case))
print('pair_role', collections.Counter(r['r5_6_story_role'] for r in case))
print('cluster_time', collections.Counter(r['time_level'] for r in clusters))
print('cluster_role', collections.Counter(r['r5_6_story_role'] for r in clusters))
print('condition_like_candidate_rows', sum(1 for r in partial if r.get('r5_loss_code')=='R45.LOSS.condition_like_label_lowered_as_event'))
print('blocked_rows', len(blocked), [r['raw_pair_id'] for r in blocked])
PY
```
