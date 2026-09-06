# Artifact Post-Fix Review 21

Status: FAIL (subagent independent proposal only; not a final decision)

Scope: current frozen-arm manifests, `derived/manual_adjudication_v2`, top-level
archive/publication manifests, canonical JSON/TSV, and their provider-free validators.
No provider was called. No frozen raw or canonical artifact was modified. Earlier
artifact reviews were not used as evidence.

## Result Summary

- C findings: none.
- I findings: 3.
- M findings: none.
- Data-structure checks passed: both source-arm manifests, `162 + 162` cells,
  `1271 + 512` decisions, `1783 x 145 = 258535` dense relations, both JSON/TSV
  mirrors, and the sealed reviewer projection.
- Publication readiness fails because the inner manual MANIFEST is stale, the two
  top manifests are stale, and listed publication files are not Git-tracked.

## Passing Evidence

| Check | Independent result | Evidence pointer / command |
| --- | --- | --- |
| Raw arm hashes | PASS. `raw/v60_current` has 1508 listed files and `raw/x1v2_baseline` has 842; zero byte/hash mismatches. The two inventory/inner-manifest source hashes equal current SHA-256: `8c2105dd7025f360500709e25ac9b483b907fdd91a3c39144798158ca1a25ba0` and `8e9fa28071ba4acbbc0483c5ba84029ac69e7d0a618311ec85f7992081b374d0`. | `raw/v60_current/archive_manifest.json`, `raw/x1v2_baseline/archive_manifest.json`; independent SHA-256 scan; raw re-enumeration logic at `scripts/evaluation/validate_manual_adjudication.py:126-185`. |
| Raw universe | PASS. Inventory declares current/baseline cells `162/162`, reports `1271/512`, and total items `1783`. | `derived/manual_adjudication_v2/inventory.json` (`/cells`, `/reports`, `/items`); validator contract at `validate_manual_adjudication.py:704-711`. |
| Canonical JSON/TSV | PASS. `v60_report_decisions.json/.tsv` have 1271 rows; X1v2 equivalents have 512. Pydantic loading plus `validate_tsv_mirror` accepted both exact 21-column projections. | `derived/manual_adjudication_v2/v60_report_decisions.{json,tsv}` and `x1v2_report_decisions.{json,tsv}`; mirror comparison at `evaluation/src/paper_stm_evaluation/manual_adjudication.py:679-738`. |
| Dense relation closure | PASS. Every one of 1783 decisions has 145 relations; nested and flat key sets are equal and every flat row matched side, relation, reason, basis, source refs, and owned-field refs. Count: `1783 x 145 = 258535`. | `derived/manual_adjudication_v2/relation_decisions.json`; full closure rules at `validate_manual_adjudication.py:744-774`. |
| Sealed reviewer projection | PASS. Validator accepted 2642 rows: 1321 rows per sealed arm, 859 padding slots, 1783 projected reports, `provider_calls=0`, equal pair/round/slot universes, zero forbidden-key violations, and unblind-map closure. | `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`, `reviewer_projection_audit.json`, `reviewer_unblind_mapping.json`; `validate_reviewer_projection` at `validate_manual_adjudication.py:428-551`. |
| Validator unit tests | PASS. `14 passed in 0.66s`. | `pytest -q pipeline/evidence_discovery/tests/test_manual_adjudication_v2.py pipeline/evidence_discovery/tests/test_final_results_archive.py` with the project and evaluation source roots on `PYTHONPATH`. |

## Findings

### I-21-01: Manual canonical MANIFEST has a stale calibration hash

- Paths: `derived/manual_adjudication_v2/MANIFEST:1`, pointer
  `/canonical_files/calibration_report.json`; target
  `derived/manual_adjudication_v2/calibration_report.json`.
- Reason: the MANIFEST records
  `sha256:7a19846aded114cd08eaa4bccf343833672a042d8444df57e03d1f6b8c27a03d`,
  while the present target hashes to
  `sha256:8301ffb95c76d7ba0d1882c36a807d04e49c42343b5fdbd536d9c3e2092cfe6d`.
  The other 76 MANIFEST entries matched their current files.
- Basis: the mandatory inner integrity gate iterates every listed canonical file
  and raises on a mismatch at `validate_manual_adjudication.py:676-701`.
- Reproduction:

```bash
PYTHONWARNINGS=ignore \
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

  Actual result: `ValueError: MANIFEST hash mismatch: calibration_report.json`.
- Disposition: repair required before release. Regenerate the manual derived
  manifest deterministically after its canonical inputs are stable; do not edit
  frozen raw. This reviewer made no repair commit.
- Targeted re-review: the command above must return
  `{"status": "PASS", "decision_counts": {"v60_current": 1271, "x1v2_baseline": 512}}`.

### I-21-02: Top archive and publication manifests are stale for three listed review files

- Paths: `archive_manifest.json:14225-14235` and
  `publication_manifest.json:14230-14240`.
- Reason: each manifest records pre-change byte/hash pairs for the same three
  files, so neither manifest closes over the current archive:

| Path | Manifest bytes / SHA-256 | Actual bytes / SHA-256 |
| --- | --- | --- |
| `reviews/20_academic_postfix.md` | `6641`, `23005319068b2a454c70c365ce31dd4700cddbf297d6158a9c430065f2cb7b63` | `9835`, `9eb2652ac5a05387e0bab3d23b5373e66734df20d1e515de492a54624c174138` |
| `reviews/20_fairness_raw_first_postfix.md` | `5435`, `9a6f950a529fa804ff265bcdae4872b47fdccdae0b51dc0df1c67d247d90b52b` | `9047`, `d7cc48ee8135a973378084725ce742abc28cd45da7a6fd1814dc418c7686bc66` |
| `reviews/20_semantic_raw_first_projection_postfix.md` | `4460`, `9086653f1af6808d2ed983f45f9613305a7cd3b1068d8e4eaa26c58bb4b60460` | `6794`, `15893d070c1e30a7f9f655a2c437080ba15e459a6321270d824a2672d789eaad` |

  This proposal, `reviews/21_artifact_postfix.md`, was written after those
  manifests and is also absent from both current `included_files` lists; the
  required finalization must therefore repair both the stale entries and this
  coverage gap.

- Basis: top validation checks every listed byte count and SHA-256 before
  recomputation (`evaluation/src/paper_stm_evaluation/final_results_archive.py:811-824`)
  and requires publication coverage of the current tree (`:836-847`). The
  independent full scans found `0/1508` and `0/842` raw-arm mismatches, but
  `3/2843` archive-manifest mismatches and `3/2844` publication-manifest
  mismatches.
- Reproduction:

```bash
PYTHONWARNINGS=ignore \
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline \
  --repository-root "$PWD"
```

  Actual result: `ValueError: manifest mismatch: .../reviews/20_academic_postfix.md`.
- Disposition: repair required before release. Once all review records,
  including this proposal, have reached their intended contents, regenerate
  `archive_manifest.json` and then `publication_manifest.json` with the
  provider-free `finalize` command. This reviewer made no repair commit.
- Targeted re-review: the validation command above must print
  `final-results archive validation passed`, and independent scans must show
  zero mismatches for both top manifests.

### I-21-03: Publication-listed artifacts are not Git tracking-ready

- Paths: `.gitignore:992`; `publication_manifest.json:40`; and the 144 paths
  under `derived/manual_adjudication_v2/` listed by the publication manifest.
- Reason: comparison of `publication_manifest.json` against `git ls-files`
  found 169 listed but untracked paths: 144 manual-adjudication artifacts, 17
  review records, and 8 `raw_first_semantic_review/` artifacts. The bare
  `MANIFEST` ignore rule actively ignores the validator-required
  `derived/manual_adjudication_v2/MANIFEST`; ordinary `git add` therefore
  omits it. The two top manifests declare that file at
  `archive_manifest.json:35` and `publication_manifest.json:40`.
- Basis: a clone of the tracked state would lack the formal manual manifest,
  which is mandatory input to `validate_manual_adjudication.py:676-701` and
  listed as release content. This is a reproducibility and release-integrity
  problem, not a raw-data defect.
- Reproduction:

```bash
git check-ignore -v \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/MANIFEST
git status --short --untracked-files=all -- \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

  Actual ignore evidence: `.gitignore:992:MANIFEST`.
- Disposition: repair required before release. Add a narrow post-rule unignore
  for this required path (or use an explicit durable tracking policy), stage
  every publication-listed artifact, and commit the final manifests only after
  their hashes have been regenerated. This reviewer made no repair commit.
- Targeted re-review: compare the publication-manifest path set with
  `git ls-files`; the difference must be empty. Also run
  `git check-ignore -v --no-index <manual-MANIFEST-path>` and require no match,
  so future `git add` cannot silently omit the file.

## Repair Order and Offline Re-Review

This is a proposed repair sequence for the owning session, not an action taken
by this reviewer:

```bash
# After all intended canonical/manual inputs are stable; this rewrites derived outputs.
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2

# After all review files are also stable; this rewrites only top-level release manifests.
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 -m paper_stm_evaluation.final_results_archive finalize \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline

# Then run the two validation commands in I-21-01 and I-21-02.
```

The final targeted re-review must also repeat the raw-arm hash scan, the
JSON/TSV exact-mirror check, the 258535 relation closure, the sealed projection
validator, and the Git path-set comparison. Until then this proposal remains
FAIL.
