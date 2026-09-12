# Track B: semantic and fairness review

**Reviewer:** `01a05261-c0b9-79a1-9cbc-2a099331b0b0`
**Mode:** independent, read-only subagent review; no provider, method, or Judge run
**Scope:** current v4, baseline v3, fair-comparison protocol/schema, report and canonical closure

## Final disposition

Canonical data: **PASS**. Publication documents before the fixes below: **FAIL**.
The findings were documentation/provenance issues and did not require changing any
canonical semantic decision.

| Check | Result | Evidence and disposition |
| --- | --- | --- |
| Protocol identity | PASS after fix | `derived/manual_adjudication_v4_current_reaudit/protocol_freeze_v4_current_reaudit.md:3-4` now names `issue-189-195-manual-evidence-v2` and identifies `current-reaudit-v4` as a layer; fair protocol maps it to baseline `issue-189-195-baseline-ni-v3`. |
| Decision order | PASS after fix | Current and baseline protocol now use `author-source fact -> D/A -> all expected relations -> validity/K/N/I`. |
| D/A and K/N/I closure | PASS | `derived/manual_adjudication_v4_current_reaudit/schema.md:28-30`, baseline protocol `:46-56`; current `1271` and baseline `512` rows each close over 145 expected relations with no invariant violation. |
| FULL/PARTIAL/NO | PASS after fix | Fair protocol now defines `NO_MATCH` as no admissible relation after complete evidence review; FULL is the only main hit and PARTIAL is supported coverage. |
| W and predicate independence | PASS | Fair protocol/report keep W independent of D/A, KNI and predicate; baseline predicate remains `not_applicable`, not zero. |
| N grouping and I diagnostics | PASS after fix | Fair schema `group_id` now allows N substantive groups or I diagnostic clusters and explicitly excludes I IDs from defect/group precision. |
| Baseline correction prose | PASS after fix | Baseline protocol now describes source-backed D/A corrections, including D0, A0/FALSE_POSITIVE and reviewed D1 cases, rather than only two source-refuted claims. |
| Current inherited review boundary | PASS | Current v4 README and `derived/fair_comparison_v4/reviews/independent_final_gate_review_v4.json` describe hash-revalidated inherited source-first evidence, not a new 1271-report blind inter-rater study. |

## Machine cross-check

The canonical projection remains `current=1271`, `K/N/I=749/231/291` and
`baseline=512`, `K/N/I=312/105/95`; both sides have 145 relations per report.
D/A-to-K/N/I invariants pass, and I relations are all `NO_MATCH`.

## Resolution

Pane5 accepted the source-backed document corrections, regenerated the top-level
manifests, and preserved all canonical JSON/TSV, raw, reference and historical
layers. This review is QA provenance, not a human inter-rater study.

## HEAD-specific independent rerun and closure (2026-08-31)

Reviewer `Track-B/offline-semantic-fairness-2026-08-31` rechecked all current
N/I, baseline v3, both protocols, fair schema and the paper report without
reading Track A/C conclusions. Canonical D/A-to-K/N/I closure, 145-relation
density, N grouping and baseline predicate N/A all passed. Three publication
FAILs were retained in this log:

1. the report-bound predicate headline disagreed with the saved summary;
2. current's `189` I diagnostic clusters had no report-to-cluster projection;
3. baseline protocol prose placed validity before the complete relation pass.

Pane5 resolved them by preserving `825/1271` and `303/825` as explicitly named
report-bound diagnostics, adding the Pydantic-backed
`current_i_diagnostic_clusters_v4.json` map (`291/291` reports, 189 same-pair
clusters), carrying those diagnostic IDs into the fair index, and correcting
the order to `source fact -> D/A -> all relations -> validity/K/N/I`. Every I
cluster is structurally marked non-defect and excluded from grouped precision.

Final validators pass for `1271/1271` current and `512/512` baseline reports;
there are no null I diagnostic pointers, and no canonical semantic decision was
changed. The retained I merge boundary remains a diagnostic sensitivity, not a
claim of 189 substantive defects.

## Publication-scope rerun before finalization (2026-08-31)

Reviewer `codex:track-b-semantic-fairness-readonly:a69ef442` independently
checked protocol identity, `source -> D/A -> all relations -> K/N/I`, dense
relation closure, FULL/PARTIAL/NO, W independence, N grouping, I non-grouping,
baseline predicate `not_applicable`, NADC limits and the manual-supervision
boundary. Canonical semantic data passed with zero closure violations across
current `1271 x 145` and baseline `512 x 145` relations. The reviewer suggested
the low-risk first-use expansion `NOT_A_DEFECT_CLAIM (NADC)`, now applied.

The only gate FAIL was the same expected pre-finalization manifest drift for
the edited report and fair README. The reviewer classified it as publication
provenance, not a D/A, relation, K/N/I or grouping error. Commands included the
three provider-free validators plus independent `jq` closure and one-to-one
group-membership checks. No file was edited by the reviewer and no provider,
method or Judge run occurred.

## Final predicate-publication narrow closure (2026-08-31)

Reviewer `codex:track-b-predicate-publication-narrow:a69ef442` confirmed that
current and fair publication summaries expose only the two report-bound ratios,
their status and their naming boundary. `method_terminal_execution`,
`registered_report_bound_predicate_ids`, `report_bound_completed_receipts`,
planned IDs and executed IDs are absent from all four publication summaries;
their historical provenance remains archive-only. Baseline predicate status is
`not_applicable`, explicitly not zero.

The same review reran current (`1271` reports, `184295` relations), baseline
(`512` reports, `233` reviewed non-K and `279` frozen K) and fair (`1783`
reports, `145` expected) validators. Protocol IDs, D/A-to-relation-to-K/N/I
closure, N grouping, I non-grouping and the inherited manual-supervision
boundary all passed. Current/fair mirrors and top-level manifests were
hash-consistent at review time. No semantic decision or experiment artifact
changed. Final result: **PASS**.
