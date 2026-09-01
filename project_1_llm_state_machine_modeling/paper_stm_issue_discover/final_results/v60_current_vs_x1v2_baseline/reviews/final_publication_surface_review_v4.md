# Final publication-surface review v4

**Scope:** Paper1 current v4 versus X1v2 baseline v3 documentation, navigation,
manifest and provider-free recomputation. This review does not relabel canonical
decisions.

## Independent tracks

| Track | Reviewer | Initial result | Final result |
| --- | --- | --- | --- |
| A numeric/provenance | `01a05261-bfcb-7c60-b697-b146093725a3` | Canonical numbers PASS; manifest/link FAIL | PASS after link repair and manifest regeneration |
| B fairness | `01a05261-c0b9-79a1-9cbc-2a099331b0b0` | Canonical closure PASS; protocol/schema prose FAIL | PASS after protocol and field-description fixes |
| C docs/navigation/academic | `01a05261-c0f1-7591-933a-8349b1275b52` | Entry/manifest/link FAIL | PASS after surface, link and manifest fixes |

These are independent subagent QA tracks, not a claim of a new human
inter-rater experiment. The detailed records are
[Track A](./track_a_numeric_provenance_v4.md),
[Track B](./track_b_semantic_fairness_v4.md), and
[Track C](./track_c_docs_navigation_academic_v4.md).

## Checks and evidence

| Gate item | Final disposition | Evidence |
| --- | --- | --- |
| Current canonical closure | PASS | `build_current_reaudit_v4.py --validate-only`: `1271` reports, `162` cells, `184295` relations, `231` N, `291` I, `121` N groups |
| Baseline canonical closure | PASS | `validate_baseline_v3.py`: `512` reports, `233` reviewed non-K, `279` frozen K, `98` N groups, `95` I clusters |
| Fair numeric recomputation | PASS | `recompute_fair_comparison_v4.py --validate-only`: `1783` combined reports and `145` expected IDs |
| Publication surface | PASS | `final_results_archive._publication_file_manifest` now allowlists v4 report, current-v4/baseline-v3/fair layers, schemas and named v4 reviews; raw, reference, v2 and historical files remain archive-only |
| Relative links | PASS | Archive validator resolves the moved v3 historical report and the corrected release review link |
| Hash closure | PASS | Top-level archive and publication manifests were regenerated after all document edits; release exception records current bytes and SHA-256 |
| Shuorenhua fidelity | PASS | Existing `reviews/04_shuorenhua_fidelity_review.md` and `reviews/23_shuorenhua_final_rereview.md`, plus final reread of the v4 report/protocol, preserve all protected metrics, units, paths, protocol identities, limitations and responsibility boundaries |
| Execution boundary | PASS | No provider, method, Judge, 15x1 or 54x3 invocation; no raw/reference/canonical semantic decision change |

## Pane5 arbitration

The reviewers' initial FAILs were publication-layer defects, not evidence that
the canonical data were wrong. Pane5 selected the current v4 report as the only
paper-facing headline, retained the old full report under
`report/history/v3/`, and left the former path as a short historical index.
The I field is documented as `I_diagnostic_cluster` even where legacy JSON
keys remain `I_group` for compatibility. Supplemental citations remain
bounded: the report names the sources and states that this project's
same-side/same-pair/normative-obligation/source-root-cause/repair-intent rule is
an operationalization, not a verbatim rule from any single paper.

All discrepancies were closed by source-backed documentation edits,
deterministic recomputation, or explicit historical classification. No
canonical semantic label, raw artifact, reference ledger, method output or
Judge output was rewritten.

## Final evidence

The canonical headline is `current=1271`, `K/N/I=749/231/291`,
`D2/D1/D0/A0=721/259/120/171`, report precision `980/1271 = 77.10%`;
baseline is `512`, `312/105/95`, `342/75/85/10`, report precision
`417/512 = 81.45%`. FULL hit@1 is `310/435` versus `227/435`; hit@3 is
`119/145` versus `106/145`; hit@all is `86/145` versus `46/145`.
W-on-FULL-hits is current `197/113/0` and baseline `0/227/0`, with denominators
310 and 227. Current predicate usage/contribution is `825/1271` and `303/825`;
baseline is `N/A`, not zero.

## Final HEAD-specific gate closure (2026-08-31)

The fresh Track A/B/C reruns preserved their initial FAIL findings instead of
overwriting them. Pane5 resolved every finding at the publication/derived-index
layer:

- report-bound predicate diagnostics remain `825/1271` and `303/825`;
  method-execution and witness-audit counts stay in historical provenance and
  are not current publication-summary fields;
- all 291 current I reports map exactly once to 189 same-pair diagnostic
  clusters, with `substantive_defect=false` and
  `grouped_precision_unit=false`;
- baseline v3 decision-order and diagnostic-ratio prose now matches the
  mechanical closure;
- excluded proposals and absolute-path-only review provenance are archive-only;
  historical Judge rows are explicitly superseded;
- fair validation now checks every `publication_surface` hash, not only output
  and review hashes.

The resulting headline remains current `749/231/291`, baseline `312/105/95`,
FULL hit@1 `310/435` versus `227/435`, and report precision `980/1271` versus
`417/512`. Current and baseline decision/relation files, raw artifacts and the
reference ledger remained byte-identical. The only remaining sensitivities are
the conservative N merge boundary, diagnostic-only I clustering, inherited
current source-first review depth, and the baseline predicate-schema N/A
boundary; all are disclosed in the report.

Final execution boundary: `provider_calls=0`, `method_reruns=0`,
`judge_reruns=0`; no 15x1 or 54x3 run occurred.

## Final narrow review closure (2026-08-31)

| Track | Final reviewer | Result | Final scope |
| --- | --- | --- | --- |
| A numeric/provenance | `codex-track-a-narrow-readonly-20260831` | PASS | Four publication summaries, mirrors, 2982 archive entries, 90 publication entries, current/fair manifests, stable 1217-row inventory and headline arithmetic |
| B fairness | `codex:track-b-predicate-publication-narrow:a69ef442` | PASS | Predicate publication boundary, baseline N/A, protocol IDs, D/A-relation-K/N/I closure, N grouping, I non-grouping and manual-supervision scope |
| C docs/navigation/academic | `codex:track-c-final-narrow-readonly` | PASS | Unique route, historical markings, publication/archive split, 898 tracked Markdown files, 6142 relative links, DOI/title metadata and Shuorenhua fidelity |

The final current/fair publication summaries contain only `status`,
`report_bound_binding`,
`legacy_semantic_hit_marker_among_report_bound_bindings` and
`naming_boundary` for current predicate reporting. Historical method/witness
fields remain archive provenance. All three reviewers were read-only internal
QA tracks; they are not presented as a human inter-rater study. Their detailed
evidence and commands remain in the three track logs above.

## Post-review machine gate

The final provider-free run, after all review logs were written, produced:

| Check | Result |
| --- | --- |
| current v4 validator | PASS: `1271` reports, `184295` dense relations, `231` N reports, `291` I reports, `121` N groups |
| baseline v3 validator | PASS: `512` reports, `233` reviewed non-K, `279` frozen K, `98` N groups, `95` I clusters |
| fair recomputation | PASS: `1783` combined reports, `145` expected IDs |
| final-results archive validator | PASS |
| publication/release/archive tests | `20 passed`; only existing Pydantic `schema` shadow warnings |
| Markdown links | `0` invalid references in Paper1 |
| summary mirrors | current, baseline and fair pairs are byte-identical |
| protected evidence diff | empty for raw, reference and both sides' canonical decision/relation files relative to `4683524f203c6bd77f18a1a32aae8e9c53fdc399` |

This gate made no provider call and did not run method, Judge, 15x1 or 54x3. All validity,
relation, D/A, K/N/I and component-analysis decisions cited by this review were completed by
human adjudication; the machine checks only read those artifacts and recomputed their summaries.

## Final pane5 arbitration after wording review (2026-09-01)

The final pane5 review incorporated three independent read-only tracks. Track A
confirmed the canonical arithmetic and the distinction between `12/19` and
`8/19`; Track B confirmed the #189/#195 closure and the disjunctive FULL rule;
Track C confirmed navigation, citations, history labels and the final talk.
The only pre-finalizer findings were stale publication prose or hashes. Pane5
resolved them without changing canonical data: paper-facing text describes all
validity, relation, D/A, K/N/I and component-analysis decisions as completed by
human adjudication, while provider-free code only validates, closes fixed
records and recomputes numbers.

The current release surface remains one v4 headline report, current v4 and
baseline v3 canonical layers, fair v4, conversion attribution v1, required
schemas/reviews and the final handoff talk. Historical reports, old manual
judgment records, v2/v27/v46 materials and provenance-only artifacts remain
excluded from the current headline. Finalizer and fresh validators must be
rerun after this review entry so the top-level manifest hashes cover this exact
text.
