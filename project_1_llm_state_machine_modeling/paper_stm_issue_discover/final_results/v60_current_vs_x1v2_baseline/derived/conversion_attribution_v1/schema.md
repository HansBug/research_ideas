# Attribution schema

`report_attribution_v1.json` has one record per current v4 `canonical_class=I` report, exactly 291 records. Each record carries raw report identity/hash, source refs/hash, source-owned and derived facts, compiler ownership, trace/lowering/backend refs, one primary attribution, optional secondary diagnostics, metric role and review status.

Primary attribution is exactly one of: `CONVERSION_LOWERING_CONFIRMED`, `COMPILER_OWNED_ARTIFACT_CONFIRMED`, `PROJECTION_TRACE_BOUNDARY_CONFIRMED`, `RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED`, `SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED`, `D0_NONVIOLATION_CONFIRMED`, `ATTRIBUTION_INDETERMINATE`. The first category is empty in v1 because no report met the concrete source-absence/semantic-mismatch plus per-claim lowering/loss evidence gate.

`i_attribution_summary_v1.json#/precision_gap` stores the arithmetic, side-specific D0/ordinary-FP/NADC rate decomposition. It is descriptive only; it does not redefine precision or supply a counterfactual. `confirmed_method_owned_invalid_total` excludes the 8 indeterminate records, while `nadc_disposition_total` includes them.
