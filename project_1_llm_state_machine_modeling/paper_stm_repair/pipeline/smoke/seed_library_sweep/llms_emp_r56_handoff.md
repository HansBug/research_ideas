# R5.5 -> R5.6 story / model scope handoff

## 1. boundary_decision

`proceed_with_supplementary`

理由：10 个 NL cluster 中 8 个为 T0、1 个为 T0.5、1 个为 T1；60 个 pair 中 57 个可进入 `.fcstm` 级别，3 个 blocked 有负证据。主实验可以围绕 T0/T0.5 离散状态机族继续推进，但 Digital Camera cluster 与 blocked pair 应进入 supplementary / stress / negative evidence，而不是主 claim 证据。

## 2. supporting_counts

- pair status: `{'blocked': 3, 'converted': 16, 'partial': 41}`
- pair time level: `{'T0': 48, 'T0.5': 6, 'T1': 6}`
- cluster time level: `{'T0': 8, 'T0.5': 1, 'T1': 1}`
- story roles: `{'main_candidate': 53, 'negative_evidence': 3, 'supplementary_stress': 4}`
- partial ledger rows: `41`
- blocked rows: `3`

## 3. blocking_evidence

- 3 个 blocked 均为 `R5.LOSS.official_scxml_unavailable`，详见 [llms_emp_blocked_probe.md](./llms_emp_blocked_probe.md)。
- Digital Camera cluster 含显式秒级执行时间与复杂 pseudo-state，应避免支撑 T0 主 claim。
- 大量 partial 来自 conversion / representation attribution，不能计入 repair gain。

## 4. confidence

`medium-high`：一手 pair / R5 sweep / R3.1 recovery / R4.5 loss 证据完整；但 time level 与 repair target taxonomy 仍需 R5.6/R5.7 正式冻结。

## 5. r5_7_candidate_summary

- `R45.LOSS.condition_like_label_lowered_as_event` 是主要 repair target 候选，但必须逐例有 NL 证据。
- 层次 lowering、scope lifting、initial inference 默认是 representation caveat，不直接进入 repair target。
- blocked official SCXML unavailable 是 converter follow-up / negative evidence，不是 repair loop 能直接声称修复的问题。

## 6. recommended_next_action

R5.6 应在 `story/model_scope.md` 中冻结 main / supplementary-stress / negative evidence 的模型范围，并把主实验 claim 限定到 T0/T0.5 离散状态机族；R5.7 再定义 guard/event/action/hierarchy 的 repair target。
