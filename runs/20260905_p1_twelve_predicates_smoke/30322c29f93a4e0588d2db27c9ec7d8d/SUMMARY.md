# Evidence-Discovery Run Audit

- run id: `30322c29f93a4e0588d2db27c9ec7d8d`
- run contract: `sha256:ef5ac749baf9aeea07d135e0939f9f91b1fe409373535ffc1b5503c9a5bd3707`
- status: `completed`
- scope: `diagnostic_subset`
- profile: `gpt-5.6-luna`
- source commit: `71774498d65f3e3a7df5a30fbd7128236756fc1f`
- source branch: `paper1/p1-twelve-predicates`
- registry: `four-family-12-core.v1`
- pair count: `2`
- method cells: `2`
- method cost USD: `0.11900268`

## Method Metrics

- method_cells: `2`
- eligible_method_cells: `2`
- method_cell_eligible_rate: `1.0`
- release_issue_count: `25`
- eligible_release_issue_count: `25`
- evidence_record_count: `42`
- witness_levels: `{'W2': 13, 'W1': 29}`
- d_levels: `{'D2': 31, 'D1': 6, 'D0': 5}`
- unresolved_or_error_records: `0`
- method_diagnostics: `0`
- predicate_execution_receipts: `54`
- executed_predicates: `['G1', 'R1', 'R3', 'S1', 'S2', 'S3', 'S4', 'V1']`
- execution_verdicts: `{'violation': 14, 'unsupported': 28, 'pass': 12}`
- coverage_accounting: `{'predicate_execution_coverage': {'executed_distinct_predicates': 8, 'registry_predicate_denominator': 12, 'executed_predicates': ['G1', 'R1', 'R3', 'S1', 'S2', 'S3', 'S4', 'V1'], 'basis': 'terminal PredicateExecutionReceipt records only; prompt appearance and plans do not count'}, 'w2_finding_coverage': {'w2_evidence_record_count': 13, 'w2_finding_record_count': 13, 'basis': 'method-owned evidence records and deterministic witness level'}, 'full_w2_ledger_coverage': {'status': 'pending_external_judge_mapping', 'reason': 'The method does not read ledger expectations; FULL/W2 ledger coverage is computed only after frozen external Judge expected mapping.', 'basis': 'method/evaluation physical isolation boundary'}}`

## Pair Status

| pair | method cells | eligible | errors | method USD |
|---|---:|---:|---:|---:|
| 0002 | 1 | 1 | 0 | 0.055852080000000005 |
| 0024 | 1 | 1 | 0 | 0.0631506 |
