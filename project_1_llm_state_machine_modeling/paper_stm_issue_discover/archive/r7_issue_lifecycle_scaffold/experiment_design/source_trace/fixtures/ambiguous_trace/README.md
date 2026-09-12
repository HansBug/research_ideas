# ambiguous_trace

- JSON: [../../../../pipeline/evaluation/fixtures/source_trace/ambiguous_trace.json](../../../../../../pipeline/evaluation/fixtures/source_trace/ambiguous_trace.json)
- relation: `ambiguous`
- projection: `unprojectable`
- 关联 issue: `ISSUE.EXPR.001`（candidate-only）

本 fixture 表示一个中间元素可能对应多个 raw/source transition origin。它必须 `source_level_claim_allowed=false` 且 `closure_claim_allowed=false`，不能作为 confirmed repair-eligible issue 的 closure 主证据。
