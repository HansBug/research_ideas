# normalized_guard_trace

- JSON: [../../../../pipeline/evaluation/fixtures/source_trace/normalized_guard_trace.json](../../../../../../pipeline/evaluation/fixtures/source_trace/normalized_guard_trace.json)
- relation: `normalized`
- projection: `projectable`
- 关联 issue: `ISSUE.GUARD.001`

本 fixture 覆盖 guard 从 `[door_closed == true]` 到 `door_closed` 的语义保持规范化。它必须包含 `normalization_report`，防止把 normalization 自身误当 repair gain。
