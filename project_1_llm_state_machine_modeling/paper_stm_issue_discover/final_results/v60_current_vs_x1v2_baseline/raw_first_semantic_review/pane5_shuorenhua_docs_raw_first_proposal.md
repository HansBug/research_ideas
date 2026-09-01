# Pane5 raw-first semantic review proposal

## 身份与范围

- reviewer role: `shuorenhua docs`
- deliverable: independent `subagent proposal`
- status: proposal only; not a final human signature and not a replacement for pane5 primary/final adjudication
- blind signature: `sha256:fa33eb0df1a072bb27a17f5e467c8b5e0908c0ad18bb870a2bb3d7abc83a8ec3`
- provider calls: `0`
- frozen raw mutation: `0`
- blind scope: `raw/v60_current`, `raw/x1v2_baseline`, `reference/x1v2_input_closure`, source inventory
- unblinded scope: `reference/predicate_registry.json`, `reference/current_source_catalog.json`, issue-facing protocol documents, and canonical audit files under `derived/manual_adjudication_v2`
- excluded from this review: current primary/proposal/frozen label as decision sources; no existing proposal was used to determine these findings

## Overall verdict

`FAIL` for release/fairness review. Four `I` findings remain open. The registry/source provenance and D/A/W/relation boundary checks pass as documented below. This verdict is an independent proposal for the main session to record, not a human sign-off.

All commands below assume the working directory is
`project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline`.

## Findings

### FAIL F-RAW-001: Common artifact closure identity is not symmetric

- severity: `I`
- C/I/M: `I`
- status: `FAIL`
- paths/evidence:
  - `final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/summary.json:1#/pair_receipts`
  - `final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/judge/composite-summary.json:1#/pair_receipts`
  - sample inputs: `raw/v60_current/judge/source_runs/77404499c3ac4511a218f0ad3f91c45b/inputs/0000.json:1#/artifact_closure/closure_hash` and `raw/x1v2_baseline/judge/source_runs/x1v2-full-r1-rest-05cf0da6/inputs/0000.json:1#/artifact_closure/closure_hash`
  - protocol basis: `discover_matrix/docs/protocol/semantic_judge_protocol.md:99-103`
- reason: The protocol requires the same pair's public artifact closure to have unchanged content, provenance, and hash across arms. The selected 54-pair x 3-round receipts report `artifact_closure_hash` mismatch for `162/162` corresponding cells. For pair `0000:r1`, the visible 13 artifact IDs, per-artifact SHA-256 list, metadata, and content compare byte-identically after excluding the stored closure hash, yet the stored closure hashes are `sha256:514231fe519ea9776625e6ff4b390c75ab34786efb8496e17c24f9a327c0c3b0` (current) and `sha256:8024454121f8e4e1ab41a5d8417c2d4eed9eab35d31c4888b60a65efbd864b47` (baseline). This is an identity/closure reproducibility defect even where the sampled visible payload is equal.
- basis: `semantic_judge_protocol.md:92` defines closure identity as a provider-free contract; `:99-103` requires the closure hash not to vary by arm. `serialized_input_hash` is deliberately not a finding here: it differs for `162/162` because the two arms contain different report payloads, while the common artifact closure is the object required to match.
- provider-free recheck/evidence:

  ```bash
  awk -F '\t' 'NR==FNR {c[$1 FS $2]=$3; s[$1 FS $2]=$4; next} {k=$1 FS $2; if (c[k]!=$3) ac++; if (s[k]!=$4) si++; n++} END {printf "cells=%d artifact_closure_mismatch=%d serialized_input_mismatch=%d\n",n,ac,si}' \
    <(jq -r '.pair_receipts[] | [.pair_id,.round,.artifact_closure_hash,.serialized_input_hash] | @tsv' raw/v60_current/judge/composite/summary.json) \
    <(jq -r '.pair_receipts[] | [.pair_id,.round,.artifact_closure_hash,.serialized_input_hash] | @tsv' raw/x1v2_baseline/judge/composite-summary.json)

  cmp <(jq -S -c '[.artifact_closure.artifacts[] | del(.sha256)]' raw/v60_current/judge/source_runs/77404499c3ac4511a218f0ad3f91c45b/inputs/0000.json) \
      <(jq -S -c '[.artifact_closure.artifacts[] | del(.sha256)]' raw/x1v2_baseline/judge/source_runs/x1v2-full-r1-rest-05cf0da6/inputs/0000.json)
  ```

  Expected output for the first command: `cells=162 artifact_closure_mismatch=162 serialized_input_mismatch=162`. The second command exits `0`; it is the sample control showing that the mismatch is in the recorded closure identity, not the visible artifact payload.
- disposition: quarantine the comparative fairness claim and any score comparison that relies on this closure identity until the closure builder/hash materialization is deterministically re-run or the hash contract is corrected and versioned. Do not silently replace the hashes in frozen raw.
- repair commit: `PENDING`; no repair was made by this subagent.
- targeted re-review: rerun the two commands above on all 162 cells; require `artifact_closure_mismatch=0`, exact equality of the common closure payload and its per-artifact hashes, then update the audit MANIFEST before a fresh independent review.

### FAIL F-RAW-002: Baseline method provenance is not symmetric with current

- severity: `I`
- C/I/M: `I`
- status: `FAIL`
- paths/evidence:
  - current: `raw/v60_current/method/method/0000/round-1.json:34404-34409#/source_provenance`, including branch `paper1/m-witness-discovery`, commit `66b5d71aecd73f6eeddac082037f7c34e04da057`, and `source_dirty=false`
  - baseline sample: `raw/x1v2_baseline/method/run1/0000-luna/record.json:1-107#/source_provenance` is absent; its `inputs` block at `:26-34` only records source paths, content hashes, and `truncated=false`
  - baseline aggregate: `raw/x1v2_baseline/judge/composite-summary.json:1#/source_provenance` is absent/null; baseline source-run manifests expose `source_root`/`source_root_hash` but no source commit
  - policy basis: `discover_matrix/docs/protocol/final_output_metrics_policy.md:5-12` and `method_provenance_policy.md:7-11`
- reason: The current method cells carry a reproducible repository revision and clean-state assertion in every cell, while the 162 baseline method records carry no `source_provenance`. Baseline run manifests preserve source-root paths and hashes, but not the source revision/branch or an equivalent provenance contract. This leaves the two arms with unequal evidence for which implementation produced the reports and weakens fair attribution of any observed difference.
- basis: The provenance policy requires exact source/run/prompt/schema/registry/input hashes for formal runs and distinguishes method provenance from content hashes. A content hash proves bytes of an input artifact; it does not identify the code revision that generated the baseline report.
- provider-free recheck/evidence:

  ```bash
  find raw/v60_current/method/method -name 'round-*.json' -print0 \
    | xargs -0 jq -s '{cells:length,nonempty:(map(select((.source_provenance // {})|length>0))|length)}'
  find raw/x1v2_baseline/method -path '*/record.json' -print0 \
    | xargs -0 jq -s '{cells:length,nonempty:(map(select((.source_provenance // {})|length>0))|length)}'
  ```

  Observed output: current `{ "cells": 162, "nonempty": 162 }`; baseline `{ "cells": 162, "nonempty": 0 }`.
- disposition: mark baseline provenance as an open reproducibility/fairness gap. Do not infer a commit from the source-root path or promote the legacy Judge run commit to method provenance.
- repair commit: `PENDING`; no repair was made by this subagent.
- targeted re-review: add an explicit baseline provenance record for every selected method cell, bind it in the archive MANIFEST, and re-run the count plus source-root/hash/commit consistency check. A new `I`-level review is required if provenance remains path-only.

### FAIL F-CANON-003: Canonical status documents contradict each other

- severity: `I`
- C/I/M: `I`
- status: `FAIL`
- paths/evidence:
  - `derived/manual_adjudication_v2/README.md:1-12` says the review is unfinished and that records without real human primary, independent, and final-adjudicator confirmation may only be `PROPOSAL`/`INDEPENDENT_REVIEW`; `:20-29` marks the decision files and review log as pending
  - `derived/manual_adjudication_v2/summary.json:1#/review_status` is `FINAL` and `#/human_supervised_session` is `true`
  - `derived/manual_adjudication_v2/review_log.json:1#/entries` contains `1783` entries, all `review_status=FINAL`, `human_confirmation=true`, and `independent_reviewer_role=subagent_proposal`; all have `primary_visible=false` and `reference_visible=false`
  - `derived/manual_adjudication_v2/human_supervised_authorization.json:1#/independent_reviewer_policy` explicitly says the independent reviewer is a subagent proposal
- reason: The package simultaneously presents itself as unfinished/non-final and as final human-confirmed output. The review log correctly preserves the independent reviewer as `subagent_proposal`, but the README's stated finality condition requires a real human independent confirmation. A downstream reader cannot determine from these files whether `FINAL` means human-supervised adjudication is complete or whether the entries remain proposal-only.
- basis: The README is the issue-facing long-term document for artifact status; the JSON files are canonical data. Their status contract must agree before the package can be used as a formal result. The user's review constraint also requires this subagent's output to remain explicitly proposal-only.
- provider-free recheck/evidence:

  ```bash
  jq -r '[.entries[] | .review_status] | group_by(.) | map({status:.[0],n:length})' derived/manual_adjudication_v2/review_log.json
  jq -r '[.entries[] | .independent_reviewer_role] | group_by(.) | map({role:.[0],n:length})' derived/manual_adjudication_v2/review_log.json
  jq -r '.review_status, .human_supervised_session' derived/manual_adjudication_v2/summary.json
  ```

  Observed output: `FINAL` for all `1783` review entries; `subagent_proposal` for all `1783`; summary `FINAL` and `true`.
- disposition: block formal release of this audit package until the owner chooses one status contract and updates the issue-facing README, canonical JSON status fields, and MANIFEST together. Preserve the subagent identity; do not convert it into an independent human signature.
- repair commit: `PENDING`; no repair was made by this subagent.
- targeted re-review: review the status contract against the actual human-supervised workflow, rerun the provider-free status query, then have a human reviewer specifically re-review the finality wording and sign the resulting document change.

### FAIL F-CANON-004: Per-entry attestation required by the canonical validator is absent

- severity: `I`
- C/I/M: `I`
- status: `FAIL`
- paths/evidence:
  - `derived/manual_adjudication_v2/review_log.json:1#/entries[*]` contains `1783` entries, and every entry is missing the required `attestation` field
  - validator contract: `scripts/evaluation/validate_manual_adjudication.py:336-355` requires `attestation` in every review entry and rejects the directory at `:345` when it is absent
  - the separate `derived/manual_adjudication_v2/human_supervised_authorization.json:1` does not satisfy a per-entry `review_log.json` field requirement
- reason: The canonical review package cannot pass its own structured supporting-file validator because all `1783` review entries omit `attestation`. Other per-entry fields such as `human_confirmation`, `confirmed_at`, and `blind_event_sequence` are present, but that does not satisfy the validator's complete attestation contract. This is an evidence-chain defect independent of whether the entries' substantive decisions are correct.
- basis: `validate_manual_adjudication.py:336-355` defines the required per-entry field set and the non-empty attestation check. The provider-free validator run ended with `ValueError: review_log entry lacks human/blind review attestation fields` at `:345`.
- provider-free recheck/evidence:

  ```bash
  jq -r '["primary_reviewer_id","independent_reviewer_id","final_adjudicator_id","human_confirmation","human_supervised_session","review_status","submission_hash","confirmed_at","confirmation_basis","independent_submission_at","primary_submission_at","blind_event_sequence","attestation","human_supervised_authorization"] as $required | [.entries[] | ($required - (keys) | join(","))] | group_by(.) | map({missing:.[0],count:length})' derived/manual_adjudication_v2/review_log.json
  PYTHONPATH=evaluation/src python scripts/evaluation/validate_manual_adjudication.py --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
  ```

  Observed output: `[{"missing":"attestation","count":1783}]`; the validator exits `1` with `review_log entry lacks human/blind review attestation fields`.
- disposition: quarantine the canonical audit package from formal release until the owner supplies or explicitly removes the per-entry attestation requirement through a versioned contract change. Do not synthesize attestations, human signatures, or final decisions in this proposal.
- repair commit: `PENDING`; no repair was made by this subagent.
- targeted re-review: after a contract-consistent repair, rerun the missing-field query and the canonical validator; require exit `0`, then recheck the README/JSON status contract from `F-CANON-003` without changing the preserved `subagent_proposal` identity.

## PASS checks / non-findings

### PASS P-INPUT-001: Raw current/baseline source inputs are symmetric

- status: `PASS`
- C/I/M: `none` (PASS)
- evidence: both arms contain `54` pairs and `162` pair-round cells; NL hashes match `162/162`, PlantUML hashes match `162/162`, and `truncated` flags match `162/162`. The source inventory has `162` references over `54` unique inventory items with `0` hash mismatches. Current method provenance is non-empty in `162/162`; the asymmetry is recorded separately as `F-RAW-002`.
- disposition: no finding against raw source content. Keep the closure and source inventory frozen.

### PASS P-PROV-002: Predicate registry and source catalog provenance close

- status: `PASS`
- C/I/M: `none` (PASS)
- evidence: `reference/predicate_registry.json:1-103` contains the 19-predicate registry with family counts `structure/topology/trajectory/bounded_verification = 6/4/4/5`; `reference/current_source_catalog.json:1-360` contains `28` source IDs and `40` catalog path occurrences (`16` unique paths). `derived/manual_adjudication_v2/predicate_source_provenance.json:1#/rows` has `19/19` non-empty provenance rows, and all referenced catalog IDs resolve. The provider-free `predicate_witness_audit.json` keeps current predicate rows separate and marks baseline predicate usage `not_applicable`, rather than treating it as zero usage.
- boundary check: `semantic_judge_protocol.md:17-57,75-95` and `semantic_judge_issue_195.snapshot.md:15-49,67-90` preserve the D/A, W, relation, K/N/I and issue #189/#195 separation. In particular, W does not decide validity/relation/hit/FP; `PARTIAL_MATCH` is supported-only; D0/A0 close to INVALID/I; D2/D1 plus positive relation close to VALID_KNOWN/K; D2/D1 plus all NO_MATCH close to VALID_NOVEL/N. Requirement-relative containment, direct-member cardinality, initial vertex, event consumer coverage, orthogonal concurrency, hierarchy priority, and trace delta remain non-predicate boundaries.
- disposition: `PASS`; no registry or source-catalog repair proposed by this review.
- evidence command:

  ```bash
  jq '[.rows[] | select((.source_provenance|length)==0)]|length' derived/manual_adjudication_v2/predicate_source_provenance.json
  jq '[.sources[].paths[]] | {total:length,unique:(unique|length)}' reference/current_source_catalog.json
  jq '.sides.x1v2_baseline' derived/manual_adjudication_v2/predicate_witness_audit.json
  ```

  Expected output: `0`, `{ "total": 40, "unique": 16 }`, and baseline status `not_applicable`.

## shuorenhua docs review record

- scene: `docs`; subscene: issue-facing audit/review documentation; mode: annotation/audit-only; tier: no actionable Tier 1 or Tier 2 style hit; level: `minimal`; scope: `in-place`.
- protected spans recorded before the first independent proposal:
  - identities and responsibility: `shuorenhua docs`, `subagent proposal`, `main session`, `final human adjudication`, `v60_current`, `x1v2_baseline`, and issue `#189`/`#195`
  - paths and commands: every path, line anchor, JSON pointer, shell command, `jq`, `find`, `awk`, `cmp`, and `PYTHONPATH=evaluation/src` invocation in this file
  - fields, statuses, and terminology: `artifact_closure_hash`, `serialized_input_hash`, `source_provenance`, `review_status`, `human_confirmation`, `independent_reviewer_role`, `primary_visible`, `reference_visible`, `PASS`, `FAIL`, `PENDING`, `FINAL`, `D/A/W`, `relation`, `K/N/I`, `PARTIAL_MATCH`, `not_applicable`, and `source_dirty`
  - quantities and exact identifiers: `54`, `162`, `19/19`, `28`, `40`, `16`, `1783`, all `sha256:` values, the current commit `66b5d71aecd73f6eeddac082037f7c34e04da057`, and the blind signature `sha256:fa33eb0df1a072bb27a17f5e467c8b5e0908c0ad18bb870a2bb3d7abc83a8ec3`
  - protocol meanings and evidence relationships: closure identity, method provenance, predicate provenance, D/A/W and relation boundaries, and the mapping from each finding to its raw/reference evidence
- first-pass issue list:
  - fixed audit labels (`reason`, `basis`, `disposition`, `repair commit`, `targeted re-review`) and repeated finding headings are schema-facing fields, not removable template prose; disposition: keep
  - `Overall verdict`, `PASS checks / non-findings`, and `Handoff` are functional navigation labels; disposition: keep
  - `This verdict is an independent proposal...` and the explicit `subagent proposal` wording state authorship and authority; disposition: keep
  - `weakens fair attribution` and `block formal release` are evidence-based risk/disposition language tied to the listed provenance/status facts; disposition: keep, with no stronger claim added
  - no unsupported citation, praise, narrator explanation, empty conclusion, or business-jargon phrase was found that could be removed without changing the audit contract; no standalone shuorenhua style finding is opened
- fidelity reread after the first pass:
  - all protected paths, commands, JSON pointers, counts, hashes, statuses, issue numbers, protocol terms, and reviewer identities remain byte-for-byte represented in the original proposal sections
  - each FAIL claim still points to an observed raw/reference field and its provider-free command; no claim was weakened or strengthened by the docs review record
  - no new implementation, provider result, source revision, human signature, label, or canonical decision was introduced; the added text records review method and disposition only
  - the raw-first boundary remains explicit: canonical/reference material is listed as unblinded scope only after the blind signature, and this file remains proposal-only
- second-pass residual audit:
  - opening: direct proposal title; no removable greeting or conclusion-first preamble
  - summary: headings are functional; no empty `综上`/`overall` conclusion remains beyond the evidence-backed verdict
  - narrator/abstract judgment: no `this shows`-style explanation is needed; `weakens fair attribution` remains because it names the documented risk, not a style flourish
  - rhythm: repeated field order is intentional and makes findings comparable; changing it would reduce retrieval/review consistency
  - result: `PASS` for shuorenhua docs quality; no residual rewrite is proposed. The overall artifact review remains `FAIL` solely because `F-RAW-001`, `F-RAW-002`, `F-CANON-003`, and `F-CANON-004` are open `I` findings.
- shuorenhua evidence commands:

  ```bash
  git diff --check -- raw_first_semantic_review/pane5_shuorenhua_docs_raw_first_proposal.md
  rg -n 'subagent proposal|sha256:|artifact_closure_hash|source_provenance|review_status|#189|#195|repair commit|targeted re-review' raw_first_semantic_review/pane5_shuorenhua_docs_raw_first_proposal.md
  git diff -- raw/v60_current raw/x1v2_baseline reference/x1v2_input_closure
  ```

  Evidence pointer: this section and the finding sections above in `raw_first_semantic_review/pane5_shuorenhua_docs_raw_first_proposal.md`; the last command must remain empty for frozen raw/reference input paths.

## Handoff

This file is the `shuorenhua docs` subagent proposal for the main session. The main session may accept, reject, or amend each finding after its own authorized review. It must preserve the distinction between this proposal and final human adjudication. No repair commit was created here; all four FAIL findings therefore have `repair_commit=PENDING` and require the targeted re-reviews above.
