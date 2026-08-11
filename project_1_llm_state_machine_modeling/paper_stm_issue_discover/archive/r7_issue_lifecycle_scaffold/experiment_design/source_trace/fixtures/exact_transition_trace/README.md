# exact_transition_trace

- JSON: [../../../../pipeline/evaluation/fixtures/source_trace/exact_transition_trace.json](../../../../../../pipeline/evaluation/fixtures/source_trace/exact_transition_trace.json)
- relation: `exact`
- projection: `projectable`
- 关联 issue: `ISSUE.GUARD.001`

本 fixture 表示 raw/source transition `T_move` 与中间表示 transition `fcstm.T_move` 一一对应。它可支持后续 closure evidence 的 trace 层定位，但不单独证明 issue 已闭合。
