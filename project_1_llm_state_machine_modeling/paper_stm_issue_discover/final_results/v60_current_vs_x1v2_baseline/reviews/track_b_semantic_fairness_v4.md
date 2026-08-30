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
