# Shuorenhua Targeted Docs Rereview

## Identity and scope

- reviewer role: `shuorenhua docs`
- deliverable: independent `subagent proposal`; this is not a final human signature or a canonical decision
- scene: `docs`, with README, protocol, report, review, and issue-facing archive subscenes
- mode: `audit-only`; level: `minimal`; scope: `in-place`
- provider calls: `0`; method/Judge execution: `0`; raw or canonical decision mutation: `0`
- corpus root: `final_results/v60_current_vs_x1v2_baseline/`
- overall targeted rereview result: `FAIL` for cross-document fidelity; `PASS` for shuorenhua style quality

## Protected spans established first

The following spans were fixed before reading the corpus for style judgment. They
are not rewrite targets:

- paths, links, commands, shell syntax, JSON pointers, file names, and line
  anchors, including `raw/`, `reference/`, `derived/`, `report/`, `reviews/`,
  `archive_manifest.json`, and `publication_manifest.json`
- exact identities and responsibility: `v60/current`, `X1v2 baseline`,
  `pane5`, `subagent`, `human`, `Judge`, `method`, issue `#189`, issue `#195`,
  and `final adjudication`
- exact numbers, fractions, percentages, deltas, units, and denominators:
  `54`, `3`, `145`, `435`, `39`, `117`, `1271`, `512`, `1783`, `310/435`,
  `211/435`, `981/1271`, `197/310`, `113/310`, `306/435`, `104/117`,
  `1165/1271`, `211/95/0`, and every other table value in the corpus
- statuses and enums: `FINAL`, `PROPOSAL`, `INDEPENDENT_REVIEW`, `PENDING`,
  `VALID_KNOWN`, `VALID_NOVEL`, `INVALID`, `K`, `N`, `I`, `D2/D1/D0/A0`,
  `W0/W1/W2`, `FULL_MATCH`, `PARTIAL_MATCH`, `NO_MATCH`, and
  `not_applicable`
- provenance and evidence terms: `human_confirmation`, `attestation`,
  `source_refs`, `raw/source evidence-read`, `artifact hash`, `terminal
  receipt`, `judge_association`, `full_report_ids`, `post_review_correction`,
  and the distinction between frozen Judge output and later manual review
- version, commit, run, model, hash, schema, and protocol identifiers, including
  `paper1.manual-adjudication.v2`,
  `issue-189-195-manual-evidence-v2`,
  `github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`,
  `66b5d71aecd73f6eeddac082037f7c34e04da057`, and all SHA-256 values
- negation, conditions, completion state, comparison direction, and scope
  qualifiers such as `only`, `not`, `尚未`, `不修改`, `不替代`, `current-only`,
  `historical`, and `after the two review passes`

## First-pass issue list

| Candidate | Initial classification | First-pass disposition |
| --- | --- | --- |
| Root README current summary versus the current Chinese report | fidelity candidate | numeric fidelity fails; open DOC-18-001 for the exact D/A, K/N/I, ledger, and precision mismatches |
| v2 README `FINAL` claims versus root/derived schema readiness claims | status-contract candidate | retain all status words; current authority chain passes |
| `reviews/01` old frozen-Judge metrics versus the current report | historical-scope candidate | preserve the labeled historical snapshot; current check passes |
| README protocol field-mapping link | link-integrity candidate | preserve the target and anchor; verify the relative path |
| `唯一稳定入口`, `机械复算`, `承重事实`, `倒灌`, `本体论`, `provider-free`, and repeated audit headings | possible style candidates | keep: these are technical or schema-facing terms in a formal docs corpus |
| greetings, praise, empty conclusions, narrator phrases, commercial jargon, or unsupported citations | style candidates | none found in the first pass; no standalone style finding opened |

## Corpus reread

The following current documents were read completely before the fidelity
comparison:

- `README.md:1-70`
- `SCHEMA.md:1-110`
- `derived/manual_adjudication_v2/README.md:1-64`
- `derived/superseded_judge_exposed_witness_review_v1/README.md:1-18`
- `derived/manual_adjudication_v2/protocol_freeze_v2.md:1-29`
- `derived/manual_adjudication_v2/schema.md:1-62`
- `report/v60_current_vs_x1v2_baseline_cn.md:1-119`
- every current Markdown review in `reviews/01` through `reviews/17`,
  including the historical/superseded qualifiers, targeted rereviews, and
  pane5 addenda; this file was excluded from its own corpus comparison

The archive README and reviews `05`-`17` clearly distinguish superseded v1
material, proposal-only work, targeted rereviews, and the accepted v2/v3
witness path. The protocol freeze and v2 README use stable technical language
and preserve the D/A, relation, W, and K/N/I boundaries. The main report is
readable as a formal technical report.
The failures below are cross-document authority, numeric snapshot, or release
surface problems, not word-choice problems.

## Fidelity diff findings

### FAIL DOC-18-001: Issue-facing root summary disagrees with the current report

- severity: `C`
- status: `FAIL`
- paths/evidence:
  - `README.md:28-40` says the current-result bullets are an index and links
    the full paired table to the formal report, but gives current
    `D2/D1/D0/A0 = 724/257/121/169`, `K/N/I = 750/231/290`, ledger
    `119/121/187`, and report precision `981/1271 = 77.18%` versus baseline
    `410/0/0/102`, `276/134/102`, `104/134/102`, and
    `410/512 = 80.08%`.
  - `report/v60_current_vs_x1v2_baseline_cn.md:29,33-37,49-57` gives the
    conflicting formal values: current report precision `980/1271 = 77.10%`,
    baseline `411/512 = 80.27%`; current D/A `721/259/120/171`, K/N/I
    `749/231/291`, ledger `119/121/189`; baseline D/A `408/3/2/99`, K/N/I
    `279/132/101`, ledger `104/132/101`.
- reason: The stable entry document presents exact headline counts and
  percentages while explicitly pointing readers to the formal report. The two
  issue-facing result surfaces therefore do not have one reproducible numeric
  authority. The discrepancy changes both sides' reported composition and
  precision, so it cannot be treated as wording or rounding.
- basis: The line-level pairs above differ in numerators, denominators, or both;
  the percentage differences (`77.18%` versus `77.10%`, and `80.08%` versus
  `80.27%`) are not rounding variants of the same fraction. This review does
  not infer which document is correct and does not read or alter canonical
  decisions; the owner must reconcile both surfaces against the provider-free
  recomputation before release.
- provider-free recheck/evidence:

  ```bash
  rg -n 'D2/D1/D0/A0|K/N/I|report-based precision|ledger-based precision|ledger N_group|ledger I_group' \
    project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md \
    project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md
  ```

  Observed mismatches include the exact pairs listed above. The command is a
  read-only text comparison and does not establish the canonical winner.
- disposition: `FAIL` for publication-facing numeric fidelity. Reconcile the
  README and report against the provider-free recomputation, update every
  dependent numerator/denominator/percentage together, and then rerun link and
  manifest checks. Do not fix this by silently changing a protected data file.
- repair commit: `PENDING`
- targeted re-review: `PENDING_FIX; not run`. After the owner-side numeric
  repair, rerun the extraction command, the manual-adjudication validator and
  recomputation command, then confirm the README/report pairs agree exactly.

### PASS DOC-18-002: Finality and readiness status now share one documented contract

- severity: `none`
- status: `PASS`
- paths/evidence:
  - `derived/manual_adjudication_v2/README.md:1-7,17-29` calls the package
    `最终人工监督裁定`, marks all listed files `FINAL`, and says all final
    labels have `attestation`.
  - `report/v60_current_vs_x1v2_baseline_cn.md:1-3,96-100` likewise calls
    the package final human-supervised truth and says every final record has
    `attestation`.
  - root `SCHEMA.md:3-6,31-35,89-97` identifies manual v2 as the main-result
    package, defines the FINAL status contract, and binds the publication
    surface through manifests.
  - `derived/manual_adjudication_v2/schema.md:52-64` defines the planned-scope
    and FINAL admission requirements without claiming that the current
    directory remains pre-FINAL.
- reason: The previous finality/readiness contradiction is absent from the
  current docs. The v2 README, protocol freeze, root SCHEMA, derived schema,
  and report now describe the same FINAL package and admission conditions.
- basis: `derived/manual_adjudication_v2/schema.md:52-64` separates the
  planned-scope contract from FINAL validation and lists the failure conditions;
  it no longer says that the current directory has not reached FINAL. The v2
  README marks the package files `FINAL` at
  `derived/manual_adjudication_v2/README.md:13-29`, and the protocol freeze
  records completed human confirmation at `protocol_freeze_v2.md:22-29`.
- provider-free recheck/evidence:

  ```bash
  rg -n '未完成|尚未|FINAL|最终人工|冻结 Judge|human_confirmation|attestation|当前目录尚未达到|当前主结果' \
    README.md SCHEMA.md derived/manual_adjudication_v2/README.md \
    derived/manual_adjudication_v2/protocol_freeze_v2.md \
    derived/manual_adjudication_v2/schema.md report/v60_current_vs_x1v2_baseline_cn.md
  ```

  Evidence pointers are the lines listed above. The status scan found no stale
  “current directory has not reached FINAL” readiness claim.
- disposition: `PASS` as a non-finding. Preserve the distinction between
  subagent proposal and human adjudication; manifest finalization remains the
  separate DOC-18-004 release condition.
- repair commit: `N/A` (the owner-side schema update is present in the current
  worktree; no repair was made by this subagent).
- targeted re-review: `PASS` for the current authority chain; rerun the status
  scan and validator if any FINAL/readiness paragraph changes.

### PASS DOC-18-003: Review 01 now labels its historical metric snapshot

- severity: `none`
- status: `PASS`
- paths/evidence:
  - `reviews/01_numeric_recomputation_review.md:1` titles the document as
    `历史冻结 Judge v3.2 快照`.
  - `reviews/01_numeric_recomputation_review.md:9-23` labels the values as a
    frozen Judge v3.2 snapshot and preserves the old `306/435`, `104/117`,
    `721/444/106`, and `211/95/0` metrics without rewriting them.
  - `reviews/01_numeric_recomputation_review.md:11-12` explicitly says the
    snapshot does not replace the current v2 final human-supervised result;
    the current report is at `report/v60_current_vs_x1v2_baseline_cn.md:13-39`.
- reason: The previous snapshot-boundary ambiguity is closed in the current
  document. A reader can distinguish the historical arithmetic audit from the
  current report without changing any protected metric.
- basis: The title, result qualifier, and explicit non-substitution sentence
  now provide the same time-scope boundary that the later review documents use.
- provider-free recheck/evidence:

  ```bash
  rg -n '无数值差异|306/435|104/117|721/444/106|211/95/0|310/435|105/117|981/1271|197/113/0|历史|Historical|frozen|superseded' \
    reviews/01_numeric_recomputation_review.md reviews/06_x1v2_witness_data_integrity_review.md \
    reviews/07_x1v2_witness_semantic_metric_review.md reviews/08_x1v2_witness_blind_data_integrity_review.md \
    reviews/11_v60_invalid_manual_reaudit.md reviews/12_v60_valid_novel_posthoc_reaudit.md \
    report/v60_current_vs_x1v2_baseline_cn.md
  ```
- disposition: `PASS` as a non-finding. The historical values remain protected
  and are not presented as current headline data.
- repair commit: `N/A` (the owner-side documentation update is present in the
  current worktree; no repair was made by this subagent).
- targeted re-review: `PASS` for the current title/result/handoff boundary;
  rerun the cross-document metric diff if Review 01 or the current report
  changes.

### FAIL DOC-18-004: This appended review requires a publication-surface refresh

- severity: `M`
- status: `FAIL`
- paths/evidence:
  - `README.md:17-22,69-70` exposes the review log and the archive/publication
    manifests as part of the stable entry surface.
  - `SCHEMA.md:89-97` requires the review/provenance files and says the top-level
    manifests bind the entire archive publication surface.
  - `reviews/08_x1v2_witness_blind_data_integrity_review.md:40-47` records the
    same deferred-finalization rule for a review added after a manifest check.
  - both manifests currently list `reviews/13`-`reviews/18`, including this
    file, at `archive_manifest.json:14195-14196` and
    `publication_manifest.json:14200-14201`, with the pre-append size/hash
    `19406` / `sha256:4ba9e3930514afc46ac2c8aa6e476a556e89a3f4765d3af9b9ef7d1c786a73a6`.
    No manifest or source file was edited by this subagent.
- reason: Appending this final rereview changes this review file's byte count
  and SHA-256 after the manifests were generated. Until the owner regenerates
  both manifests, the listed publication surface does not describe the file
  being submitted. This is an operational release condition, not a reason to
  alter raw or canonical decisions during a docs review.
- basis: The archive's own README/SCHEMA require review files and manifests to
  be included together, and the existing review-08 addendum explicitly treats
  post-manifest reviews as pending finalization.
- provider-free recheck/evidence:

  ```bash
  git status --short -- reviews/18_shuorenhua_targeted_rereview.md \
    raw reference/x1v2_input_closure
  git diff --exit-code -- raw reference/x1v2_input_closure
  ```

  Expected/current evidence before this append: each manifest listed `25`
  review-related entries and included this file's pre-append hash. After this
  append, compare the manifest entry with `sha256sum` and `wc -c`; frozen
  raw/reference diff remains expected to exit `0`.
- disposition: `FAIL` for publication readiness until the normal manifest
  refresh is performed. No manifest repair is performed here.
- repair commit: `PENDING`
- targeted re-review: `PENDING_FIX; not run`. After finalization, verify this
  file's bytes and SHA-256 in both manifests, run archive `validate`, resolve
  active Markdown links, and reread the final status contract from DOC-18-001
  through DOC-18-005.

### PASS DOC-18-005: README protocol field-mapping link resolves

- severity: `none`
- status: `PASS`
- paths/evidence:
  - `README.md:60-64` links to
    `../../discover_matrix/docs/protocol/semantic_judge_protocol.md#双侧-reviewer-输入映射`.
  - The target file exists at
    `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md`,
    and the target heading is present at line `76`.
- reason: The owner-side relative-link repair now lets the stable README reach
  the field-level mapping used to support the current/baseline input symmetry
  claim.
- basis: The provider-free Markdown link checker returns zero broken links;
  filesystem and heading checks confirm the intended target and anchor.
- provider-free recheck/evidence:

  ```bash
  python3 tools/check_md_links.py \
    project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline \
    --repo-slug HansBug/research_ideas --list
  test -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md
  rg -n '^### 双侧 reviewer 输入映射$' \
    project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md
  ```
- disposition: `PASS` as a non-finding. No repair is proposed by this
  subagent; the link and anchor are preserved.
- repair commit: `N/A` (owner-side repair already present; no repair made by
  this subagent)
- targeted re-review: `PASS` after the owner-side link repair; rerun the link
  checker if README path or protocol heading changes.

## Fidelity reread and diff result

The second, bidirectional reread checked each protected category against the
documents and then checked each finding back to its cited source lines. The
following remained faithful and received no finding:

- paths, commands, links, field names, schema names, issue numbers, roles, and
  technical terminology were not altered by this review
- the archive README correctly marks the Judge-exposed v1 directory as
  superseded provenance at `derived/superseded_judge_exposed_witness_review_v1/README.md:3-18`
- protocol D/A, relation, W, and K/N/I definitions remain stable at
  `derived/manual_adjudication_v2/protocol_freeze_v2.md:11-20` and
  `derived/manual_adjudication_v2/schema.md:27-54`
- reviews 05-10 preserve the v1/v2 isolation boundary, W correction, and
  provider-free scope; reviews 11-17 explicitly identify their audit,
  proposal, targeted-rereview, or final-result boundaries
- no new number, citation, institution, year, causal claim, human signature,
  provider result, or canonical label was introduced by this review

The fidelity diff fails on DOC-18-001 and DOC-18-004. DOC-18-005 is now a
resolved link pass. No
in-place prose rewrite is proposed because rewriting any of those protected
values would hide rather than resolve the authority/snapshot problem.

## Shuorenhua residual audit

- opening residual: no greeting, praise, or conclusion-first preamble in the
  reviewed docs; headings are functional
- summary residual: no empty `综上`, `总的来说`, or value-inflating close was
  found
- narrator residual: `后端确定性闭合`, `Judge 关联只在双审后`, and similar
  phrases state system behavior or ordering; they are not narrator padding
- abstract/style residual: `唯一稳定入口`, `承重事实`, `倒灌`, and
  `本体论` are project-specific technical shorthand. They can be retained in
  this docs corpus; changing them would risk semantic drift
- rhythm residual: repeated tables, numbered procedures, and
  provider-free/read-only declarations are audit structure, not artificial
  prose repetition
- residual result: `PASS` for shuorenhua style; no style-only finding or
  rewrite is proposed. Overall remains `FAIL` because DOC-18-001 and
  DOC-18-004 remain open; DOC-18-002, DOC-18-003, and DOC-18-005 are PASS
  non-findings.

## Verification performed

These provider-free checks were run after the final reread and fidelity diff:

- `rg -n '[[:blank:]]+$'
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reviews/18_shuorenhua_targeted_rereview.md`
  returned no lines.
- The current-summary scan over `README.md` and the report found the
  DOC-18-001 mismatch: README `981/1271` versus report `980/1271`, README
  baseline `410/512` versus report `411/512`, plus the D/A, K/N/I, and ledger
  composition mismatches cited at `DOC-18-001`.
- The residual style scan over the reviewed docs returned no forbidden/template
  phrases.
- `python3 tools/check_md_links.py
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
  --repo-slug HansBug/research_ideas --list` returned `失效引用 0 条（无）`;
  DOC-18-005 is a PASS.
- `rg -n 'reviews/(13|14|15|16|17|18)'
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/archive_manifest.json
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/publication_manifest.json`
- finds the paths in both manifests. A JSON entry comparison found that both
  still record the pre-append `reviews/18` size/hash `19406` /
  `sha256:4ba9e3930514afc46ac2c8aa6e476a556e89a3f4765d3af9b9ef7d1c786a73a6`,
  whereas the current file at that verification point was `24828` /
  `sha256:3c15079c8664df1359e9da8e561c407c81461828ab476c1912874375971de959`.
  The current digest changes again with any later edit; DOC-18-004 therefore
  remains pending owner-side manifest refresh.
- `git diff --exit-code --
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/x1v2_input_closure`
  returned exit `0`. Evidence path: `raw/`, `reference/x1v2_input_closure/`,
  and this file at `reviews/18_shuorenhua_targeted_rereview.md`.

## Handoff

This is a read-only, provider-free `shuorenhua docs` subagent proposal for the
main session. It must not be converted into a final human signature. Repair
commits for DOC-18-001/004 are `PENDING`; DOC-18-002/003/005 have no repair.
Targeted re-review instructions are attached to each finding. Frozen raw and
canonical decisions remain untouched.

## Final rereview append (current worktree)

### Completion record

- reviewer: independent `shuorenhua docs` subagent proposal, not a human
  signature and not a canonical decision
- skill execution: `docs` scene; `audit-only`, `minimal`, `in-place`; the
  skill's protected-spans, README/issue-facing, positive-style, operation, and
  read-back requirements were applied before this append
- protected spans retained: all paths/anchors/commands, raw and canonical
  status terms, issue `#189/#195`, D/A/relation/W/K/N/I rules, numbers and
  denominators, provenance/attestation roles, hashes, and scope/negation
  qualifiers listed at `:13-43`
- first-pass list: completed at `:45-54`; the README/report numeric candidate
  was reopened after the literal second-pass comparison exposed the mismatch
- second reread/fidelity diff: README, root SCHEMA, both archive READMEs,
  derived schema and protocol, the main report, current Markdown reviews,
  both manifests, and issue-facing/provenance wording were reread. The
  cross-document diff is recorded in DOC-18-001 through DOC-18-005.
- provider calls: `0`; method/Judge execution: `0`; raw mutation: `0`;
  canonical-decision mutation: `0`

### Final result and open findings

- `FAIL` overall for cross-document/release fidelity.
- `PASS` for shuorenhua style and document voice: no greeting/praise,
  conclusion padding, commercial jargon, unsupported citation, or
  inappropriate narrator voice requires an in-place rewrite.
- `FAIL / C / DOC-18-001`: `README.md:33-35` conflicts with
  `report/v60_current_vs_x1v2_baseline_cn.md:29,33-37,51-57` on current and
  baseline D/A, K/N/I, group composition, and report/ledger precision. The
  disposition is `PENDING` owner-side reconciliation against provider-free
  recomputation; repair commit `PENDING`; targeted re-review `PENDING_FIX`.
- `FAIL / M / DOC-18-004`: this append invalidates the pre-append
  `reviews/18` bytes/SHA-256 recorded by both top-level manifests at
  `archive_manifest.json:14195-14196` and
  `publication_manifest.json:14200-14201`. The disposition is manifest
  regeneration only after all accepted edits; repair commit `PENDING`;
  targeted re-review `PENDING_FIX`.
- `PASS / none / DOC-18-002`, `DOC-18-003`, and `DOC-18-005`: the FINAL
  authority chain, historical Review 01 scope marker, and README protocol
  mapping link currently pass. They require no repair by this subagent.

### Final provider-free verification instructions

```bash
archive=project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline

rg -n 'D2/D1/D0/A0|K/N/I|report-based precision|ledger-based precision|ledger N_group|ledger I_group' \
  "$archive/README.md" "$archive/report/v60_current_vs_x1v2_baseline_cn.md"

python3 tools/check_md_links.py "$archive" --repo-slug HansBug/research_ideas --list

sha256sum "$archive/reviews/18_shuorenhua_targeted_rereview.md"
wc -c "$archive/reviews/18_shuorenhua_targeted_rereview.md"
rg -n -C 3 'reviews/18_shuorenhua_targeted_rereview.md' \
  "$archive/archive_manifest.json" "$archive/publication_manifest.json"

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py \
  --directory "$archive/derived/manual_adjudication_v2"

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py \
  --directory "$archive/derived/manual_adjudication_v2"

git diff --exit-code -- "$archive/raw" "$archive/reference/x1v2_input_closure"
```

Expected evidence at submission: link checking returns zero broken links;
raw/reference diff exits `0`; DOC-18-001 remains open until the recomputation
selects and documents a single numeric surface; DOC-18-004 remains open until
both manifest entries equal this file's final byte count and SHA-256. The
validator/recomputation commands are targeted owner-side re-review evidence
and were not rerun by this docs-only subagent after identifying DOC-18-001.
