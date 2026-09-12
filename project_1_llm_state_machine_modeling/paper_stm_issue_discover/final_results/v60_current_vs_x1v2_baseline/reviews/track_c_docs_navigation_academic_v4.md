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

## Publication-scope rerun before finalization (2026-08-31)

Reviewer `codex:track-c-docs-navigation-academic-shuorenhua-readonly` confirmed
the unique route `SUMMARY -> final-results README -> v4 report/versioned
canonical data`, the seven-line historical redirect, the archive-only status of
raw/reference/history/v2, and the single report on the publication surface.
Operationalization boundaries and the distinction between data, protocol
deduction and sensitivity also passed.

The reviewer retained four pre-finalization FAILs with exact evidence:

1. the edited report hash was stale in the fair, publication and archive manifests;
2. `pipeline/evidence_discovery/PREDICATE_REGISTRY.md` linked a non-existent sibling file;
3. supplemental academic references lacked complete discoverable identifiers;
4. the Shuorenhua record still claimed that old witness-audit values remained in the headline.

Pane5 fixed the link to the method registry truth source, added exact titles and
DOIs, and recorded removal of old witness details as a publication-scope choice
rather than a style edit. The manifest FAIL remains intentionally open until all
review records and the tracked-only inventory are regenerated. The review was
read-only and made no canonical-data or experiment change.

## Final navigation and academic narrow closure (2026-08-31)

Reviewer `codex:track-c-final-narrow-readonly` checked the final working tree.
`SUMMARY.md` routes to the final-results README, which names the v4 Chinese
report as the only paper headline. The publication manifest contains 90 files
and one report; raw, reference, v2, history and the historical redirect remain
archive-only. The archive manifest contains 2982 files.

An independent scan covered 898 tracked Markdown files and 6142 relative file
links with zero broken target. The main report and final publication review no
longer publish the old witness values; current predicate presentation contains
only `825/1271`, `303/825` and baseline `N/A`. All 12 cited DOI registrations
resolved, including the six supplemental titles. The project-specific grouping
rule remains labeled as an operationalization rather than a verbatim literature
definition.

The bounded Shuorenhua record preserves numbers, definitions, responsibility,
limitations and evidence paths, and identifies removal of old witness fields
as a publication-scope decision. Publication tests reported `7 passed`; all
publication, archive and fair-manifest hashes matched at review time. The
reviewer made no edit and recorded zero provider, method, Judge or experiment
run. Final result: **PASS**, with no unresolved in-scope evidence gap. The earlier
`88/2953` values remain only as a pre-finalization snapshot retained above; the
current HEAD surface is `90/2982`. All Judge, validity, relation, D/A, K/N/I and
component-analysis decisions are described as human adjudications; this track only
checks navigation, metadata and links.

## Post-fix HEAD-specific closure (2026-09-01)

Reviewer `01a05884-8317-7fa1-9564-9d259f0fbfbe` rechecked the current working
tree after the final talk and current-facing wording fixes. The unique route,
current/history boundaries, issue #189/#195 links, relative links, citation
metadata, and explicit human-adjudication wording all pass. The reviewer also
confirmed that the FULL definition must retain #195's disjunctive rule: same
defect instance, root cause, violated obligation, or a directly attributable
manifestation, with compatible source/context.

The earlier findings were publication-layer issues only: an untracked final
talk, stale relation wording, and stale manifest counts. The talk is now in the
tracked release set, relation wording is aligned with the issue source, and the
`90` publication / `2982` archive counts are the current manifest counts. The
paper-facing text calls validity, relation, D/A, K/N/I and component analysis
human adjudications; the evaluator only performs deterministic closure,
validation and arithmetic. No canonical data or experiment artifact changed.
Final disposition: **PASS after manifest finalization**.
