# R5.5 -> R5.6 story / model scope handoff

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_r56_handoff.md` | `ee35e44407c85835dc4f3ec669477e298d89cb8a` (2026-06-28 22:54:39 +0800) | `ee35e44407c85835dc4f3ec669477e298d89cb8a` (2026-06-28 22:54:39 +0800, scope handoff fact freeze) | `ee35e44407c85835dc4f3ec669477e298d89cb8a`：首次给出 `proceed_with_supplementary` 边界裁决、T0/T0.5/T1 计数、Digital Camera supplementary stress 与 blocked negative evidence 处理。 | `1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)；[llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)；[llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl)；[negative evidence report](./2026-06-28-23-18-32-negative-evidence-report.md) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## R5.5 -> R5.6 story / model scope handoff

### 1. boundary_decision

`proceed_with_supplementary`

理由：10 个 NL cluster 中 8 个为 T0、1 个为 T0.5、1 个为 T1；60 个 pair 中 57 个可进入 `.fcstm` 级别，3 个 blocked 有负证据。主实验可以围绕 T0/T0.5 离散状态机族继续推进，但 Digital Camera cluster 与 blocked pair 应进入 supplementary / stress / negative evidence，而不是主 claim 证据。

### 2. supporting_counts

- pair status: `{'blocked': 3, 'converted': 16, 'partial': 41}`
- pair time level: `{'T0': 48, 'T0.5': 6, 'T1': 6}`
- cluster time level: `{'T0': 8, 'T0.5': 1, 'T1': 1}`
- story roles: `{'main_candidate': 53, 'negative_evidence': 3, 'supplementary_stress': 4}`
- partial ledger rows: `41`
- blocked rows: `3`

### 3. blocking_evidence

- 3 个 blocked 均为 `R5.LOSS.official_scxml_unavailable`，详见 [llms_emp_blocked_probe.md](./2026-06-28-23-18-32-negative-evidence-report.md)。
- Digital Camera cluster 含显式秒级执行时间与复杂 pseudo-state，应避免支撑 T0 主 claim。
- 大量 partial 来自 conversion / representation attribution，不能计入 repair gain。

### 4. confidence

`medium-high`：一手 pair / R5 sweep / R3.1 recovery / R4.5 loss 证据完整；但 time level 与 repair target taxonomy 仍需 R5.6/R5.7 正式冻结。

### 5. r5_7_candidate_summary

- `R45.LOSS.condition_like_label_lowered_as_event` 是主要 repair target 候选，但必须逐例有 NL 证据。
- 层次 lowering、scope lifting、initial inference 默认是 representation caveat，不直接进入 repair target。
- blocked official SCXML unavailable 是 converter follow-up / negative evidence，不是 repair loop 能直接声称修复的问题。

### 6. recommended_next_action

R5.6 应在 `story/model_scope.md` 中冻结 main / supplementary-stress / negative evidence 的模型范围，并把主实验 claim 限定到 T0/T0.5 离散状态机族；R5.7 再定义 guard/event/action/hierarchy 的 repair target。
