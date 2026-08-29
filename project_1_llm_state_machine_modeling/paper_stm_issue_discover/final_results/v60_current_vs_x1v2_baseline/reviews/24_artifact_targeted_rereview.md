# Artifact / Release Targeted Rereview

Status: **FAIL**

Reviewer: `subagent:artifact-targeted-rereview`. This is an independent,
provider-free, read-only review. It did not modify frozen raw or canonical
decisions and did not run `finalize`, because that command rewrites release
metadata.

## Passed Checks

Commands were run from `project_1_llm_state_machine_modeling/paper_stm_issue_discover`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src:scripts/evaluation python - <<'PY'
# Fresh build_manual_inventory equality; Pydantic + exact raw-ID closure;
# JSON/TSV mirror; dense relation uniqueness; canonical MANIFEST hashes;
# repository-relative source-ref path closure; raw/reference Git diff.
PY
PYTHONPATH=evaluation/src python -m paper_stm_evaluation.final_results_archive validate --archive-root final_results/v60_current_vs_x1v2_baseline --repository-root ..
```

- Fresh inventory equals `derived/manual_adjudication_v2/inventory.json`:
  v60/current `162` cells and `1271` reports (`415/446/410`); X1v2 baseline
  `162` cells and `512` reports (`173/163/176`).
- `validate_decision_set` completed exact frozen raw-ID closure for
  `1271/1271` v60 decisions and `512/512` X1v2 decisions. Pydantic parsing
  and each JSON/TSV mirror passed.
- `relation_decisions.json` has exactly `258535` rows and `258535` unique
  `(report_id, expected_id)` keys, equal to `(1271 + 512) * 145`.
- `derived/manual_adjudication_v2/MANIFEST` is `FINAL`, has the correct report
  counts and no blockers; all of its listed canonical file SHA-256 hashes
  match current bytes (`0` mismatches).
- All `2,076,456` report/relation source-reference occurrences resolve to
  `571` unique, existing archive-relative paths: `0` absolute, `0` escaping
  the archive and `0` missing.
- `git diff --name-only` reports no changes under frozen `raw/` or
  `reference/`.
- v2 `MANIFEST` is Git-trackable and currently tracked: the `.gitignore`
  allow rule applies and `git ls-files --error-unmatch` succeeds.

## Finding

`ART24-I001` (`I`, release manifest closure): the newest recompute/review
artifacts have not been followed by a top-level archive finalization.
`final_results_archive validate` fails with:

```text
ValueError: manifest mismatch: .../derived/manual_adjudication_v2/MANIFEST
```

Both [archive_manifest.json](../archive_manifest.json:1) and
[publication_manifest.json](../publication_manifest.json:1) have 11 stale
entries. The shared mismatches are:

```text
derived/manual_adjudication_v2/MANIFEST
derived/manual_adjudication_v2/calibration_report.json
derived/manual_adjudication_v2/pane5_targeted_re_review.json
derived/manual_adjudication_v2/reference_ledger_aggregate.json
derived/manual_adjudication_v2/reviewer_input_projection.jsonl
derived/manual_adjudication_v2/reviewer_projection_audit.json
derived/manual_adjudication_v2/reviewer_unblind_mapping.json
report/v60_current_vs_x1v2_baseline_cn.md
reviews/20_academic_postfix.md
reviews/20_fairness_raw_first_postfix.md
reviews/20_semantic_raw_first_projection_postfix.md
```

Reason and basis: the two release manifests retain old SHA-256 values (and
some old sizes) for these currently present files, while the v2 MANIFEST
itself is internally consistent. Consequently neither top-level archive nor
publication manifest currently describes the release tree that readers would
clone.

Disposition: `PENDING_FIX`. No finalize repair commit is present in this
review snapshot. Once all review/report files are stable, run:

```text
PYTHONPATH=evaluation/src python -m paper_stm_evaluation.final_results_archive finalize --archive-root final_results/v60_current_vs_x1v2_baseline
PYTHONPATH=evaluation/src python -m paper_stm_evaluation.final_results_archive validate --archive-root final_results/v60_current_vs_x1v2_baseline --repository-root ..
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/validate_manual_adjudication.py --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

Targeted rereview result: **FAIL pending `ART24-I001`**. No C or M finding
was found in the reviewed scope; the release-level I finding blocks PASS.
## Targeted Manifest Rereview (2026-08-29)

Status: **PASS**

Scope was limited to `ART24-I001`. This rereview was provider-free and
read-only; it did not modify raw or canonical decision data.

Commands from `project_1_llm_state_machine_modeling/paper_stm_issue_discover`:

```text
PYTHONPATH=evaluation/src python -m paper_stm_evaluation.final_results_archive validate --archive-root final_results/v60_current_vs_x1v2_baseline --repository-root ../..
```

Result: `final-results archive validation passed`.

Independent per-entry SHA-256 and byte-size comparison found:

- `archive_manifest.json`: `2851` included files, `0` mismatches.
- `publication_manifest.json`: `2852` included files, `0` mismatches.
- Both manifests contain and correctly hash
  `derived/manual_adjudication_v2/MANIFEST` and
  `reviews/24_artifact_targeted_rereview.md`.

`ART24-I001` disposition: **FIXED; targeted rereview PASS**. The prior stale
top-level manifest entries were removed by finalization. No new C/I/M finding
was observed in this limited manifest scope.
