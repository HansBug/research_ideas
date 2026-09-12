# Changelog

## v4

- Added current source/hash/relation revalidation as
  `manual_adjudication_v4_current_reaudit`; no current class changed.
- Added a unified current-v4 versus baseline-v3 report index and provider-free
  metric recomputation.
- Kept the baseline v3 279 frozen K rows unchanged and exposed all 233
  non-K migration rows through `migration_index_v4.json`.
- Separated report precision, unique K expected IDs, N substantive groups,
  and I diagnostic clusters. I is never presented as a substantive defect
  count.
- Added independent artifact, numeric, fairness, academic, and final-gate
  review records with hashes in the fair-comparison manifest.
- No raw artifact, method/Judge implementation, provider result, or experiment
  input was modified.
