# Track C: documentation, navigation and academic review

**Reviewer:** `01a05261-c0f1-7591-933a-8349b1275b52`
**Mode:** independent, read-only subagent review; no provider, method, or Judge run
**Scope:** recursive publication surface, links, manifest claims, academic boundaries and wording

## Initial findings and pane5 disposition

| Finding | Severity | Disposition |
| --- | --- | --- |
| Publication manifest listed raw/reference/v2 and historical files | High | Fixed in `final_results_archive.py`; the explicit allowlist now covers the v4 report, v4/v3/fair layers, schemas and named review records only. |
| Top-level manifest hashes were stale | High | Fixed by provider-free `final_results_archive finalize` after document edits. |
| Top-level SCHEMA named non-existent unversioned decision files and v2 validator | High | Fixed to the actual current-v4/baseline-v3 paths and current v4 validation command. |
| Historical report path was still a full duplicate headline | Medium | Full v3 report moved to `report/history/v3/`; the old path is now a short `Historical / superseded` index. |
| Active reports/story links used the old report path | Medium | `reports/README.md`, `story/paper_outline.md` and release facts ledger now point to the v4 report. |
| Release review link had one `..` too few | Medium | Fixed from `../../final_results/...` to `../../../final_results/...`. |
| Current protocol ID was ambiguous | Medium | Fixed by explicitly separating semantic protocol `issue-189-195-manual-evidence-v2` from `current-reaudit-v4` layer version. |
| Supplemental citations were compact | Low/Medium | Main report already states the supported boundaries and explicitly disclaims that the project operationalization is verbatim from any one paper. The final report review records this as a limitation rather than inventing bibliographic metadata. |

## PASS checks

- `SUMMARY.md`, project README and STATUS route readers to the final-results README;
  the final-results README routes to the v4 report and versioned canonical layers.
- The v4 report states zero new method/Judge/provider/15x1/54x3 runs and accurately
  distinguishes inherited current source-first revalidation from baseline v3 non-K review.
- Current/fair/baseline documents distinguish FULL/PARTIAL/NO, report precision,
  N substantive groups, I diagnostic clusters, W and baseline predicate N/A.
- Current publication links resolve after the fixes; historical version names remain
  in archive/provenance contexts.

## Resolution

Pane5 accepted the bounded documentation fixes, retained the historical report copy,
and re-ran link/path and manifest validation. The review is documentation QA and
academic citation-boundary review, not an inter-rater study and not a canonical label source.

## HEAD-specific independent rerun and closure (2026-08-31)

Reviewer `pane5:independent-track-c-docs-navigation-academic-v4` scanned 27 core
documents, all publication entries, the full archive manifest and active links.
Navigation and academic operationalization boundaries passed. The reviewer
retained FAIL findings for stale report hashes, predicate-unit mismatch,
baseline decision-order prose, excluded baseline proposal files on the top-level
publication surface, absolute-path review provenance, and two experiment-history
rows still labeled current.

The finalizer now excludes the baseline proposal directory and the two
absolute-path review records from the current publication allowlist; the latter
remain byte-preserved archive provenance. The inventory classifies the same
records as `archive provenance`. Historical v60/Judge and X1v2/Judge rows now
say `historical / superseded` and point directly to the v4 report. The old full
report remains under `report/history/v3/`, while its former path stays a short
historical redirect.

The requested Shuorenhua docs/public-writing rereview used minimal strength and
protected all metrics, paths, protocol IDs, responsibility statements and
limitations. It changed only the predicate-unit presentation and citation claim
mapping; its detailed fidelity record is in
`derived/fair_comparison_v4/reviews/shuorenhua_review_v4.{json,md}`. Final
tracked-only inventory, relative-link and publication/archive manifest checks
pass. This remains internal QA, not a new inter-rater study.
