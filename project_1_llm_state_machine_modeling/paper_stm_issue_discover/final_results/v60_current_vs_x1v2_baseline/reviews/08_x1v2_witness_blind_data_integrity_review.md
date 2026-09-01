# X1v2 v2 Blind Witness Audit: Independent Data-Integrity Review

## Scope

This provider-free review independently checked the accepted X1v2 v2 witness-audit data chain in the final-results archive. It covered the 162 frozen X1v2 method records, input closure, v2 blind packet, reviewer batches and decisions, final witness audit, adjudication record, selected Judge composite/results used only after review for expected-row aggregation, full-hit aggregation, active Markdown links, and manifests.

No provider call, model execution, relabeling, raw-artifact edit, code edit, or audit-data edit was performed. The superseded v1 material was not consulted; it remains superseded provenance and is outside this review.

## Methods

1. Enumerated all `raw/x1v2_baseline/method/**/record.json` files; recomputed each record SHA-256; derived every original finding key, JSON pointer, report ID, and field digest directly from `parsed_output.issues`.
2. Checked the v2 packet's 512 work items against that raw universe, including exact keys, record paths/hashes, pointers, `issue`/`reason`/`where` values and SHA-256 values, and hash-verified NL/PlantUML closure objects. The reviewer-visible packet payload was scanned for Judge association/path/hash, validity, expected-relation, and ledger leakage.
3. Verified the twelve batches form an exact, non-duplicated partition of the packet. Their only extra association field is `judge_association: null`; after removing that null placeholder, every item equals its packet item.
4. Reconciled all primary and secondary decisions to the same 512 keys, confirmed distinct reviewer IDs, compared both decisions with every final-audit record, and checked the zero-disagreement/adjudication path.
5. Only after the blind-review checks, resolved the 162 composite `pair_receipts` to their selected Judge result files, verified result hashes, reconstructed all expected rows, and recomputed the FULL-only maximum-W aggregation from `full_report_ids` alone. `partial_report_ids` were not used to set a row maximum.
6. Verified listed bytes and SHA-256 values in both raw-side manifests, the top-level archive manifest, and the publication manifest. Resolved all active local Markdown links outside the explicitly superseded v1 directory.

## Results

| Check | Independent result |
| --- | --- |
| Frozen method cells / distinct method cells | 162 / 162 |
| Frozen findings / distinct audit keys | 512 / 512 |
| Packet, batch, primary, secondary, final-audit coverage | 512 each, exact same key set |
| Packet Judge leakage | None; no association field or Judge-derived value in reviewer payloads |
| Primary and secondary reviewer IDs | Distinct singleton IDs |
| W-level disagreements / adjudications | 0 / 0 |
| Final finding-level W0/W1/W2 | 0 / 512 / 0 |
| Selected composite Judge cells | 162, exact method-cell set, all selected-result hashes match |
| Expected-row closure | 435 rows |
| FULL rows and FULL-only max W0/W1/W2 | 211; 0 / 211 / 0 |
| L2 FULL rows and max W0/W1/W2 | 46; 0 / 46 / 0 |
| W2 among all expected rows | 0 / 435 |
| Active local Markdown links checked | 49 checked, 0 broken |

Every final-audit work item preserves the blind packet's raw record pointer/hash, finding pointer, field hashes, and NL/PlantUML closure pointers/hashes. The final audit adds the non-null Judge association only after the two decisions; each attached primary/secondary decision is byte-for-byte the corresponding decision-batch entry. The expected-row audit contains all 435 selected Judge expected outcomes, and each row's supporting reports are exactly its `full_report_ids`.

## Finding And Fix

The X1v2 raw evidence chain and v2 blind-review/aggregation chain pass the requested data-integrity checks. However, the archive is not yet release-manifest clean:

- `raw/x1v2_baseline/archive_manifest.json` verifies all 842 listed entries, and `raw/v60_current/archive_manifest.json` verifies all 1,508 listed entries.
- Top-level [`archive_manifest.json`](../archive_manifest.json) has nine stale document entries: `README.md`, `SCHEMA.md`, the report, and reviews 01 and 03--07.
- [`publication_manifest.json`](../publication_manifest.json) has ten stale entries, including the README, schema, top-level archive manifest, recomputed summary, both side manifests, report, and reviews 01/03/04. It also predates reviews 05--07 and therefore cannot yet attest to the complete current publication surface.
- This review was deliberately added after the manifest check and is not listed by either existing final manifest; this is another expected consequence of deferring the finalization step.

This does not alter or invalidate the raw X1v2 record hashes, blind packet, decisions, final audit, or FULL-only W aggregation verified above. It does mean the archive-level and publication-level immutable-release claims cannot be accepted until the documented finalization step regenerates both manifests after all reviews, including this one, are in place. No fix was applied here because the requested scope prohibits modifying audit data or raw artifacts.

## Conclusion

The accepted v2 X1v2 witness audit is internally consistent and reproducible from the frozen 162-cell/512-finding raw evidence chain. The blind packet has no Judge-derived reviewer exposure, the dual review has exact independent coverage with zero disagreements, and the requested 435/211/46/0 maximum-W closures recompute exactly using only `full_report_ids`.

The remaining release-integrity action is manifest refresh, not witness-audit correction.

## Limitations

This was a structural and cryptographic data-integrity review. It did not reassess the substantive correctness of the primary or secondary W1 judgments, rerun the historical Judge, invoke any provider, or inspect the superseded v1 materials. Link checking covered active local Markdown destinations; external URLs were not fetched.

## Pane5 Resolution Addendum

The independent semantic review subsequently identified one common W1 error, so the published W distribution and adjudication counts above are historical observations, not the accepted final values. The accepted v3 audit preserves both blind W1 decisions and records one bounded `post_review_correction` for `0036:r1:0036:r1:baseline_issue_4`; its final finding-level distribution is `W0/W1/W2 = 1/511/0`, while the FULL-only counts remain `0/211/0` and L2 remains `0/46/0`. The final validator now checks the correction's allowlisted key, its archive-relative independent-review path, that path's existence and audit-key reference, and exact equality between the correction log and final audit. The later finalization refreshes all manifests after this addendum is present.
