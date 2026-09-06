# Baseline non-K manual adjudication v3

This is a versioned, provider-free evaluation layer for the frozen X1v2
baseline. It re-reviews the 233 reports that were non-K in v2 and leaves the
279 v2 K reports frozen. The old `derived/manual_adjudication_v2/` directory is
historical/superseded for this narrow non-K question and is neither overwritten
nor used as an independent review opinion.

Canonical artifacts:

- `inventory.json`: raw 162-cell/512-report census, pointers and hashes.
- `baseline_report_decisions_v3.json`: Pydantic-validated final decisions,
  one per original non-K report, with exact raw/source refs, D/A, 145 relations,
  reasons, bases, reviewer chain, and pane5 confirmation.
- `baseline_report_decisions_v3.tsv`: complete fixed-column mirror of the
  canonical decision fields.
- `baseline_relation_decisions_v3.json`: dense `233 x 145` relation rows.
- `baseline_n_groups_v3.json`: substantive N groups and separately named I
  diagnostic clusters. Every member has a partitioned source-ref record;
  singleton N groups carry one dedicated conservative non-merge record per
  pair-local neighboring final-N report. The map and membership are checked
  at report level.
- `baseline_combined_512_v3.json`: frozen v2 K rows plus v3 non-K rows.
- `summary_v3.json`: deterministic publication metrics, migrations, and
  by-round/by-pair tables. `recomputed_summary_v3.json` is the recompute copy.
- `reviews/arbitration_log_v3.json`: one addressable pane5 arbitration record
  for each of the 233 decisions, including all 146 disagreement records.
- `reviews/shuorenhua_process_v3.json` and `.md`: complete docs-scene process
  record with protected spans, first-pass issues, second-pass reread, and
  provider-free fidelity diff; the style reviewer does not assign semantic labels.
- `reviews/`: independent structural, numeric, semantic, academic, fairness,
  and shuorenhua review artifacts for this v3 layer.
- `archive_manifest_v3_baseline_ni.json` and
  `publication_manifest_v3_baseline_ni.json`: versioned input/output hashes,
  the superseded-v2 pointer, the execution boundary, and the explicit list of
  retained-but-excluded proposal files.

The proposal directory is deliberately broader than the canonical input set.
Only the exact pair-batch files listed in the v3 manifest are admissible
independent proposal inputs. `track_b_full_0000_0059.json`,
`track_b_full_legacy.json`, `track_b_0020_0059.json`, and
`raw_scope_probe_0000_0019.json` are retained for audit history or scope
diagnostics, but are excluded from v3 decisions because they are broad
envelopes, legacy v2-derived material, or probes. Their presence does not
expand the v3 reviewer scope.

Stable report identity is the composite `pair_id:round:original_report_id`
(for example `0040:r2:baseline_issue_3`), not a local finding index. Track B
may use a raw superset while blindness is maintained before K status is
disclosed; only the canonical non-K identity set enters final decisions.
Source-read hashes document complete author NL and PlantUML reads. A proposal
remains an independent subagent opinion and cannot supply pane5 human
confirmation.

Recompute and validate offline:

```bash
export PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_pane5_register_v3.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/rebuild_baseline_v3_from_pane5_register.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_baseline_n_groups_v3.py --decisions project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_baseline_v3_summary.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json
cp project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/summary_v3.json
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

The current canonical projection is `K=312`, `N=105`, `I=95` over the 512
combined reports (`K=33`, `N=105`, `I=95` in the reviewed non-K layer).  The
pane5 materializer contains an explicit source-backed correction table for
cross-instance relation errors and two D/A corrections; it is applied before
the rebuild and is idempotent under repeated runs.

The build and validation commands require all 233 rows to have two real blind
proposal opinions before they can produce a publishable layer. No provider,
method, or Judge call is part of this layer. The current-side predicate audit
is not copied into the baseline result; baseline predicate usage is explicitly
`not_applicable`.

The validator rejects duplicate members, cross-pair members, inconsistent
round flags, map entries that do not equal declared membership, and missing or
hash-invalid member source refs. A conservative singleton is not evidence of
one distinct defect; its pair-local non-merge records preserve the criteria
that were not established and the evidence used.
