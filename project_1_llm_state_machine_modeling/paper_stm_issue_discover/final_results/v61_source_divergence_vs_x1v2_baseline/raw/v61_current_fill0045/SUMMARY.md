# Evidence-Discovery Run Audit

- run id: `0e450e5c6c9d4841820c7d1fd2a888ea`
- run contract: `sha256:3e14b6f15acdca6968662f953f65fdfa0410ffaf7fa240e8c599dc3251a83530`
- status: `completed`
- scope: `diagnostic_subset`
- profile: `gpt-5.6-luna`
- source commit: `778212b03750470f0f32d10687e4d7116ed58fd9`
- source branch: `paper1/m1-method-v61-source-divergence`
- registry: `four-family-19-core.v1`
- pair count: `1`
- method cells: `1`
- method cost USD: `0.06164135999999999`

## Method Metrics

- method_cells: `1`
- eligible_method_cells: `1`
- method_cell_eligible_rate: `1.0`
- release_issue_count: `6`
- eligible_release_issue_count: `6`
- evidence_record_count: `18`
- witness_levels: `{'W1': 8, 'W0': 10}`
- d_levels: `{'D2': 6, 'D0': 2, 'D_UNRESOLVED': 10}`
- unresolved_or_error_records: `10`
- method_diagnostics: `0`
- predicate_execution_receipts: `28`
- executed_predicates: `['R2', 'S3']`
- execution_verdicts: `{'unsupported': 18, 'pass': 10}`
- coverage_accounting: `{'predicate_execution_coverage': {'executed_distinct_predicates': 2, 'registry_predicate_denominator': 19, 'executed_predicates': ['R2', 'S3'], 'basis': 'terminal PredicateExecutionReceipt records only; prompt appearance and plans do not count'}, 'w2_finding_coverage': {'w2_evidence_record_count': 0, 'w2_finding_record_count': 0, 'basis': 'method-owned evidence records and deterministic witness level'}, 'full_w2_ledger_coverage': {'status': 'pending_external_judge_mapping', 'reason': 'The method does not read ledger expectations; FULL/W2 ledger coverage is computed only after frozen external Judge expected mapping.', 'basis': 'method/evaluation physical isolation boundary'}}`

## Pair Status

| pair | method cells | eligible | errors | method USD |
|---|---:|---:|---:|---:|
| 0045 | 1 | 1 | 0 | 0.06164135999999999 |
