# split_transition_trace

- JSON: [../../../../pipeline/evaluation/fixtures/source_trace/split_transition_trace.json](../../../../pipeline/evaluation/fixtures/source_trace/split_transition_trace.json)
- relation: `split`
- projection: `partially_projectable`
- 关联 issue: `ISSUE.INTERNAL.001`

本 fixture 覆盖 raw/source transition 被拆为中间表示中的 transition / guard / effect 多个元素。它包含 `projection_detail`，明确只能支撑 partial localization，不能单独支撑 full closure。
