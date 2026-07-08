# conversion_artifact_trace

- JSON: [../../../../pipeline/evaluation/fixtures/source_trace/conversion_artifact_trace.json](../../../../pipeline/evaluation/fixtures/source_trace/conversion_artifact_trace.json)
- relation: `conversion_artifact`
- projection: `not_applicable`
- 关联 issue: `ISSUE.CONV.001`（#150 中 rejected conversion artifact）

本 fixture 表示 trace discrepancy 来自 conversion / lowering / normalization，而不是 source STM 本身。它必须 `source_level_claim_allowed=false` 且 `closure_claim_allowed=false`，不能计作 source-level repair gain。
