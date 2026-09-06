# Semantic targeted rereview

## Verdict

**FAIL**

Role: `subagent:semantic-raw-first-targeted`.
This is a read-only, provider-free targeted rereview proposal. It is not a
human sign-off and it does not change canonical decisions, frozen raw, or
publication metrics.

The independent proposal was submitted before canonical decisions were read:

- proposal: `reviews/15_semantic_raw_first_targeted_proposal.md`
- proposal status: `PROPOSAL`
- proposal SHA-256 (excluding its `submission_hash` line): `f8f70457979c939b3eb039d69bf66ef710fc3376f2e935cff13397fc43c2cb72`
- blind flags: `reference_visible=false`, `primary_visible=false`
- provider calls: `0`
- method/Judge/rejudge/experiment calls: `0`

The FAIL verdict is based on semantic disagreements in the selected canonical
rows. The report is intentionally not a full-suite PASS: semantic coverage is
`16/1271` v60/current reports and `12/512` X1v2 findings, `28/1783` total.
The other `1755` records were inventory-only and remain semantically
unreviewed by this subagent.

## Review boundary and evidence

Before submitting the proposal, the reviewer read only the selected frozen raw
reports/method records, the corresponding author NL and PlantUML, the frozen
ledger, and the semantic protocol. After submission, canonical data was read
for the unblind comparison. No old reference label, old Judge result, or other
review conclusion was used to create the blind proposal.

Protocol anchors used in the rereview:

- `discover_matrix/docs/protocol/semantic_judge_protocol.md:40-54`: author-source fact first; A0 versus D0; deterministic D/A to K/N/I closure.
- `discover_matrix/docs/protocol/semantic_judge_protocol.md:69-71`: W is independent, `PARTIAL_MATCH` is not a hit or FP, and final `UNKNOWN`/`OUT_OF_SCOPE` is forbidden.
- `discover_matrix/docs/protocol/dtier_triage.md:10-28`: A0 is an evidence/attribution exit, and fact成立 but no violated obligation is D0.
- `discover_matrix/docs/protocol/dtier_triage.md:30-38`: D0/A0 must close to I; D2/D1 with positive relation closes to K.

Raw author-source evidence used for the principal findings:

- `reference/x1v2_input_closure/pairs/0029/nl.txt:4-6` distinguishes highway exit at `dist_to_exit<2` from whole-process completion at `auto_finished=true`.
- `reference/x1v2_input_closure/pairs/0029/plantuml.puml:15-17` contains both `cruise --> FinishState : dist_to_exit<2` and `lane_change --> exit_hwy : dist_to_exit<2`.
- `reference/x1v2_input_closure/pairs/0049/plantuml.puml:2-4` implements the `AutonomousMode` initial relation with a nested initial pseudostate, rather than a named `AutonomousMode --> InitialState` edge.
- `reference/x1v2_input_closure/pairs/0053/plantuml.puml:5-18` shows the three wrapper states and their initial edges; `nl.txt:2-5` supplies the three named operating substates.
- `reference/x1v2_input_closure/pairs/0023/nl.txt:3-5` requires PumpState first and separately describes WaterState/MethaneState transitions; `plantuml.puml:3-12` contains the authored structure.
- `reference/x1v2_input_closure/pairs/0014/nl.txt:3,9-10` and `plantuml.puml:20-26` separate an obstacle input transition from the required `EmergencyStopping` output signal.

Raw report pointers and hashes for every finding below are recorded in the
canonical `source_refs`; the canonical JSON is one physical line, so the
canonical location is cited as `...report_decisions.json:1` plus its JSON
pointer. Raw files are unchanged.

## Findings

### I-SEM-001: current retention evidence gap promoted to D2/K

- Severity: `I`
- Record: v60 proposal `v60:0014:r3:report:R0002`; canonical report ID `0014:r3:issue:1`.
- Canonical: `derived/manual_adjudication_v2/v60_report_decisions.json:1`, decision with `raw_json_pointer=/report_issue_clusters/1`; `strict_da=D2`, `validity=VALID_KNOWN`, `corrected_kni=K`, relation `EIS-0014-04=PARTIAL_MATCH`.
- Raw: `raw/v60_current/method/method/0014/round-3.json#/report_issue_clusters/1`; `observed` is “No supplied executable trace or native retention fact binds that interval and state behavior.” The author source is `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0014/nl.txt:9-10` and `plantuml.puml:14-17`.
- Reason: the report describes absence of supplied execution/retention evidence, not a false author-source fact. Under the protocol this is current-method analysis/representation debt (`A0/NOT_A_DEFECT_CLAIM`) unless a separate author-source retention violation is shown. At minimum, the canonical `D2` reason does not identify the author-source retention obligation. The blind proposal therefore gave `A0/NOT_A_DEFECT_CLAIM`, all `NO_MATCH`, and `W1`.
- Basis: proposal lines `41` and the raw pointer above; canonical reason/basis says only “a grounded violated obligation” and supplies no author-source retention locus beyond `state:Approaching:line:14`.
- Disposition: `needs semantic re-adjudication`; do not accept the canonical D2/K row without an explicit author-source obligation and report-owned fact closure.
- Repair commit: `N/A` in this read-only review.
- Targeted rereview: `FAIL / not rerun`; rerun after the canonical row is corrected and its relation is re-closed.

### I-SEM-002: current PumpState action claim overmatched to INS-0023-01

- Severity: `I`
- Record: v60 proposal `v60:0023:r1:report:R0001`; canonical `0023:r1:issue:0`.
- Canonical: `derived/manual_adjudication_v2/v60_report_decisions.json:1`, `raw_json_pointer=/report_issue_clusters/0`; `D2/K`, `INS-0023-01=FULL_MATCH`.
- Raw: `raw/v60_current/method/method/0023/round-1.json#/report_issue_clusters/0`; source `reference/x1v2_input_closure/pairs/0023/nl.txt:3` and `plantuml.puml:4,9`.
- Reason: the proposal claim is that no lifecycle action is supplied for PumpState. `INS-0023-01` is the distinct no-outgoing-transition/zero-behavior obligation. A state description (`PumpState: Pump Activated`) and the absence of an authored action do not by themselves establish the exact expected no-outgoing-transition defect identity. The raw-first proposal retained `D1/PARTIAL`; canonical promotes it to `D2/FULL` without an expected-specific repair-overlap explanation.
- Basis: proposal line `42`; ledger `reference/ledger.json#/items/INS-0023-01`; canonical relation pointer and raw pointer above.
- Disposition: `needs expected-specific relation re-adjudication`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-003: current termination finding changes D1/EIS to D2/INS

- Severity: `I`
- Record: v60 proposal `v60:0029:r1:report:R0007`; canonical `0029:r1:issue:9` with `raw_json_pointer=/report_issue_clusters/6`.
- Canonical: `derived/manual_adjudication_v2/v60_report_decisions.json:1`; `D2/K`, `EIS-0029-05=PARTIAL_MATCH`, `INS-0029-05=FULL_MATCH`.
- Raw: `raw/v60_current/method/method/0029/round-1.json#/report_issue_clusters/6`; author source `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0029/nl.txt:6,10` and `plantuml.puml` at the cited locations in the raw record.
- Reason: the raw-first reading found a real termination-related claim but also a surviving alternative interpretation of the shared `FinishState` scope, so proposed `D1` and the explicitly named EIS relation. The canonical row adds `INS-0029-05=FULL_MATCH` and upgrades D1 to D2. That upgrade requires an explicit explanation of why the alternate scope/termination reading is defeated; the canonical reason is generic (“grounded violated obligation”) and does not provide it.
- Basis: proposal line `46`; canonical relation array and canonical reason/basis at the JSON pointer above; ledger items `EIS-0029-05` and `INS-0029-05`.
- Disposition: `needs D1/D2 and expected-specific relation re-adjudication`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-004: current nested initial pseudostate is mislabeled D0 instead of A0

- Severity: `I`
- Record: v60 proposal `v60:0049:r2:report:R0022`; canonical `0049:r2:issue:30`.
- Canonical: `derived/manual_adjudication_v2/v60_report_decisions.json:1`, `raw_json_pointer=/report_issue_clusters/21`; `D0/INVALID/I`, no positive relations.
- Raw: `raw/v60_current/method/method/0049/round-2.json#/report_issue_clusters/21`; source `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0049/plantuml.puml:2-4` contains `state AutonomousMode { [*] --> InitialState }`.
- Reason: the report asserts that the complete transition inventory has no named edge `AutonomousMode -> InitialState`, but the demanded named-edge shape is not the author-source obligation: the nested initial pseudostate supplies the initial relation. The fact that the exact named edge is absent is true; the report's author-defect attribution is false. The protocol distinguishes this from D0: this is `A0/FALSE_POSITIVE`, not “fact established but no violated obligation.”
- W note: canonical `W2` is supported by raw `.../report_issue_clusters/21/receipt`, receipt `0049:r2:i33:receipt`, artifact hash `sha256:ada7f7f5faff1564cf05e4b8fe33375678bb3b3d8efec1a670401f7f1b1a510d`, and terminal result `false`. W2 does not rescue the invalid author-defect attribution.
- Basis: proposal line `51`; raw receipt object and canonical witness at the pointers above; protocol `semantic_judge_protocol.md:40-46`.
- Disposition: `correct D/A to A0/FALSE_POSITIVE; retain invalid all-NO closure and independently retain W2 if receipt validation passes`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### M-SEM-005: current 0053 relation set needs explicit duplicate/expected separation

- Severity: `M`
- Record: v60 proposal `v60:0053:r1:report:R0001`; canonical `0053:r1:issue:0`.
- Canonical: `derived/manual_adjudication_v2/v60_report_decisions.json:1`, `raw_json_pointer=/report_issue_clusters/0`; `D2/K`, both `DIFF-0053-01=FULL_MATCH` and `EIS-0053-01=FULL_MATCH`.
- Raw: `raw/v60_current/method/method/0053/round-1.json#/report_issue_clusters/0`; source `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0053/plantuml.puml:5-18`, `nl.txt:2-5`.
- Reason: the report clearly concerns the missing PumpControl entry structure and the proposal linked EIS-0053-01. The canonical addition of DIFF-0053-01 may be valid, but it must show two distinct expected-specific obligations rather than treating a single structural claim as two hits. The canonical relation reasons are generic and do not expose the distinct property/locus/repair overlap for both ledger items.
- Basis: proposal line `52`; canonical two relation objects at the pointer above; ledger `reference/ledger.json#/items/DIFF-0053-01` and `#/items/EIS-0053-01`.
- Disposition: `accept only after expected-specific relation evidence is made explicit; otherwise split/partial one relation`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-006: baseline obstacle-signal row is D1 in the blind read but D2 in canonical

- Severity: `I`
- Record: proposal `x1v2:0014:r1:issue:0`; canonical report `0014:r1:baseline_issue_1`, raw pointer `/parsed_output/issues/0`.
- Canonical: `derived/manual_adjudication_v2/x1v2_report_decisions.json:1`; `D2/K`, `VU-0014-01=FULL_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0014-luna/record.json#/parsed_output/issues/0`; source `reference/x1v2_input_closure/pairs/0014/nl.txt:3` and `plantuml.puml:20-26`.
- Reason: the source does support the distinction between the incoming obstacle trigger (`plantuml.puml:21`) and the required `EmergencyStopping` output signal (`nl.txt:3`, description at line 26). However, the report wording is broader than the exact syntax defect, and the blind proposal recorded a surviving alternative reading (`D1/PARTIAL`). Canonical `D2/FULL` needs a concrete explanation that the alternative effect/label reading is defeated, not only “grounded violated obligation.”
- Basis: proposal line `59`; canonical relation and raw/source hashes in canonical `source_refs`.
- Disposition: `needs D1/D2 and FULL/PARTIAL targeted arbitration`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-007: baseline Entry/Accelerate D-level upgrade lacks the ambiguity analysis

- Severity: `I`
- Record: proposal `x1v2:0014:r1:issue:2`; canonical `0014:r1:baseline_issue_2`, raw pointer `/parsed_output/issues/1`.
- Canonical: `derived/manual_adjudication_v2/x1v2_report_decisions.json:1`; `D2/K`, `VU-0014-01=FULL_MATCH` as represented in the canonical relation.
- Raw: `raw/x1v2_baseline/method/run1/0014-luna/record.json#/parsed_output/issues/1`; source `reference/x1v2_input_closure/pairs/0014/nl.txt:8` and `plantuml.puml:7`.
- Reason: initial pseudostate labels are exactly the protocol's known syntax/behavior ambiguity. The blind proposal used `D1` because `Entry/Accelerate` can be read as a behavior-equivalent label on the sole entry edge. Canonical `D2` does not write the required concrete second-reading rebuttal, so the D-level upgrade is not independently supported.
- Basis: proposal line `60`; `semantic_judge_protocol.md:109` and raw/source pointers above.
- Disposition: `needs D1/D2 targeted arbitration; do not use canonical D2 distribution until resolved`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### C-SEM-008: baseline PumpControl initial-entry issue changed from K/FULL to N

- Severity: `C`
- Record: proposal `x1v2:0023:r1:issue:0`; canonical `0023:r1:baseline_issue_1`, raw pointer `/parsed_output/issues/0`.
- Canonical: `derived/manual_adjudication_v2/x1v2_report_decisions.json:1`; `D2/VALID_NOVEL/N`, all relations `NO_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0023-luna/record.json#/parsed_output/issues/0`; source `reference/x1v2_input_closure/pairs/0023/nl.txt:3` and `plantuml.puml:2-12`.
- Reason: the raw source has three initial edges inside PumpControl (`plantuml.puml:4,6,8`), while NL explicitly says the system first transitions to PumpState (`nl.txt:3`). This is a direct known ledger relation to `INS-0023-01` under the blind proposal, not a novel no-match report. Canonical N contradicts the author-source fact and changes a K unit into N, affecting hit and ledger composition.
- Basis: proposal line `62`; `reference/ledger.json#/items/INS-0023-01`; canonical relation closure at the pointer above.
- Disposition: `C finding; re-adjudicate as at least VALID_KNOWN with FULL/PARTIAL relation if the cited ledger obligation remains unchanged`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### C-SEM-009: baseline cruise-to-FinishState claim incorrectly closed as A0/I

- Severity: `C`
- Record: proposal `x1v2:0029:r1:issue:1`; canonical `0029:r1:baseline_issue_2`, raw pointer `/parsed_output/issues/1`.
- Canonical: `derived/manual_adjudication_v2/x1v2_report_decisions.json:1`; `A0/FALSE_POSITIVE/INVALID/I`, all relations `NO_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/1`; raw claim is the `cruise --> FinishState : dist_to_exit<2` defect. Author source contains the exact edge at `reference/x1v2_input_closure/pairs/0029/plantuml.puml:15`, the local `exit_hwy` alternative at `:17`, and the distinct completion obligation at `nl.txt:4-6`.
- Reason: the report's fact is present in the author source and its semantic concern is supported by the same-condition/different-target inconsistency captured by ledger `EIS-0029-03`. It is not a false-positive attribution. The canonical A0/I closure therefore discards a qualifying known defect and can change K_hit and both precision compositions.
- Basis: proposal line `64`; raw record issue pointer; source lines above; `reference/ledger.json#/items/EIS-0029-03`.
- Disposition: `C finding; correct away from A0/FALSE_POSITIVE and rerun relation/validity closure`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-010: baseline undefined exit_hwy claim incorrectly closed as A0/I

- Severity: `I`
- Record: proposal `x1v2:0029:r1:issue:2`; canonical `0029:r1:baseline_issue_3`, raw pointer `/parsed_output/issues/2`.
- Canonical: `derived/manual_adjudication_v2/x1v2_report_decisions.json:1`; `A0/FALSE_POSITIVE/INVALID/I`, all relations `NO_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/2`; source `reference/x1v2_input_closure/pairs/0029/plantuml.puml:16-17` contains the undefined `exit_hwy` target; the relevant highway-exit obligation is `nl.txt:4`.
- Reason: the report points to a real author-source target and explains that no target state or continuation is authored. That is not a false-positive claim. The exact ledger relation may be `FULL_MATCH` or `PARTIAL_MATCH` after expected-specific repair-overlap review, but canonical A0/I is not supported by the raw evidence.
- Basis: proposal line `65`; raw/source pointers above; canonical all-NO relation closure.
- Disposition: `needs D1/D2 and FULL/PARTIAL arbitration; remove A0 unless source evidence disproves the claim`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### C-SEM-011: baseline collision-avoidance AND finding changed from D0/I to D2/N

- Severity: `C`
- Record: proposal `x1v2:0029:r1:issue:6`; canonical `0029:r1:baseline_issue_7`, raw pointer `/parsed_output/issues/6`.
- Canonical: `D2/VALID_NOVEL/N`, all relations `NO_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/6`; source `reference/x1v2_input_closure/pairs/0029/nl.txt:12-13` and `plantuml.puml:31-34`.
- Reason: both NL and PlantUML enumerate the three inactive conditions conjunctively. The blind read found no established violated obligation and proposed `D0/I`, not a valid novel defect. Canonical D2/N asserts a violated obligation without identifying why the explicit conjunctive reading is defeated. Because D2/N and D0/I differ in both D/A and publication class, this is a critical denominator and semantic-result finding.
- Basis: proposal line `66`; raw/source pointers above; canonical closure at `/decisions` row `report_id=0029:r1:baseline_issue_7`.
- Disposition: `C finding; require explicit obligation/alternative-reading arbitration before retaining D2/N`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

### I-SEM-012: baseline wrapper/concurrency claim changed from D0 to A0

- Severity: `I`
- Record: proposal `x1v2:0053:r1:issue:0`; canonical `0053:r1:baseline_issue_1`, raw pointer `/parsed_output/issues/0`.
- Canonical: `A0/FALSE_POSITIVE/INVALID/I`, all relations `NO_MATCH`.
- Raw: `raw/x1v2_baseline/method/run1/0053-luna/record.json#/parsed_output/issues/0`; source `reference/x1v2_input_closure/pairs/0053/nl.txt:2-5` and `plantuml.puml:5-18`.
- Reason: the source fact that PumpRegion, WaterRegion, and MethaneRegion are wrappers is true. The blind proposal judged that the NL does not uniquely prohibit wrappers/concurrency, so it chose `D0`. Canonical A0 says the fact itself is false, which is not supported by the source. The distinction matters even though both close to I.
- Basis: proposal line `69`; raw/source pointers above; canonical A0 subtype and reason.
- Disposition: `needs D0 versus A0/FALSE_POSITIVE arbitration; do not silently treat a true structural fact as false`.
- Repair commit: `N/A`.
- Targeted rereview: `FAIL / not rerun`.

## Covered rows without a canonical blocker

The following covered rows did not produce an independent blocker in this
targeted comparison, although they are not a full-suite endorsement:

- current: `v60:0014:r1:report:R0001`, `v60:0014:r1:report:R0002`, `v60:0014:r1:report:R0005`, `v60:0023:r1:report:R0006`, `v60:0023:r1:report:R0007`, `v60:0029:r1:report:R0003`, `v60:0029:r1:report:R0024`, `v60:0029:r1:report:R0026`, `v60:0049:r2:report:R0001`, `v60:0049:r2:report:R0003`, `v60:0053:r1:report:R0002`.
- baseline: `x1v2:0014:r1:issue:3`, `x1v2:0023:r1:issue:1`, `x1v2:0049:r1:issue:0`, `x1v2:0049:r1:issue:2`, `x1v2:0053:r1:issue:1`.

For these rows, the canonical D/A, validity, relation direction, and W level
were compatible with the targeted proposal at the reviewed granularity. Any
additional canonical positive relation not explicitly named by the proposal
still requires the dense expected-specific evidence in the canonical relation
object; this review does not convert it into a global PASS.

## Closure and W checks

- The canonical files contain `1271` current decisions and `512` baseline
  decisions, all marked `FINAL` with `human_confirmation=true`; this review
  does not independently certify those batch attestations.
- The selected invalid canonical rows inspected above have all `NO_MATCH`
  relations, so the mechanical invalid closure itself is not the finding; the
  findings are about whether the rows should have been invalid.
- `W` is independent of semantic validity. The selected `0049:r2:issue:30`
  canonical `W2` has a raw receipt, typed inputs, exact artifact hash and
  terminal `false`, so this rereview does not downgrade it merely because its
  D/A is disputed.
- No baseline predicate usage or baseline W2 was inferred. The baseline rows
  remain independently assessed on the W axis.
- No finding here uses a later Judge result to create evidence.

## Required disposition and targeted rereview status

The findings above have no repair commit because this subagent is explicitly
read-only and was not authorized to edit canonical data. Therefore every
finding is currently `FAIL / targeted rereview not rerun`. A maintainer must
re-adjudicate the affected raw rows, regenerate affected canonical relation
rows and derived summaries, then run a targeted rereview against the changed
rows. The unreviewed `1755` records must not be described as independently
semantically reviewed by this report.

## Reproduction commands

All commands are provider-free and read-only:

```bash
sed '/^submission_hash:/d' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reviews/15_semantic_raw_first_targeted_proposal.md \
  | sha256sum

jq '.decisions | length' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/v60_report_decisions.json
jq '.decisions | length' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/x1v2_report_decisions.json

jq '.decisions[] | select(.report_id=="0029:r1:baseline_issue_2") |
  {strict_da, a0_type, validity, corrected_kni, relations}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/x1v2_report_decisions.json

nl -ba project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/x1v2_input_closure/pairs/0029/nl.txt
nl -ba project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/x1v2_input_closure/pairs/0029/plantuml.puml
```

## Shuorenhua audit

Scene: `docs/status`; level: `minimal`; scope: `audit-only`.

Pass 1 retained all protected spans: report IDs, pair/round numbers, JSON
pointers, paths, protocol names, D/A labels, relation labels, K/N/I labels,
W levels, issue IDs, hashes, and commands. It also checked that `28/1783` is
not presented as full coverage and that `FAIL` is not softened into PASS.

Pass 2 checked residual AI-template language, unsupported generalization,
unattributed “research shows” claims, and accidental use of proposal labels as
canonical facts. No protected technical span was changed by that pass.

Final review hash (provider-free): to be recorded by the maintainer after any
subsequent edits; this file is not a canonical adjudication dataset.
