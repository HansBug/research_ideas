# Semantic targeted rereview

## Verdict

`FAIL` for this targeted rereview. This is an independent `subagent` proposal
and read-only review. It is not a human adjudication and does not replace the
authorized pane5 session.

- Role: `subagent:semantic-raw-first-full`
- Provider calls: `0`
- Method/Judge/rejudge calls: `0`
- Frozen raw and canonical files modified: `0`
- Blind proposal: `reviews/16_semantic_raw_first_full_proposal.json` and `.md`
- Blind proposal persisted at: `2026-08-29T09:48:47Z`
- Blind batch hash: `sha256:3f8e0b1022b3436ea15ffe082d6ba19e2cd8e97b10741b9dfb28022df59db63e`
- Blind proposal JSON hash: `sha256:b7ebe7109109b648223a44bd38bcb01a6ad6471d246c084c13bda03f5b01d48a`
- Canonical files were read only after proposal persistence:
  `derived/manual_adjudication_v2/v60_report_decisions.json:1` and
  `x1v2_report_decisions.json:1`.

## Raw-first coverage

The blind inventory closed raw identity for all `1271` current reports and
`512` baseline findings from `162 + 162` method cells. It recorded the author
NL/PlantUML path and file hash for every row. The actual independent semantic
source read covered `28/1783` rows: `16` current and `12` baseline. The other
`1755` rows remain explicit evidence gaps and are not covered by this review.
This report does not call the inventory a full semantic PASS.

All blind relation fields were `WITHHELD_BLIND`; they were not silently filled
with `NO_MATCH`. After persistence, the canonical rows and relevant
`reference/ledger.json` items were read for comparison.

## Target comparison

`F` and `P` mean canonical `FULL_MATCH` and `PARTIAL_MATCH`. A relation value
was not submitted in the blind proposal.

| side / pair / round / index | blind D/A, W | canonical D/A, validity, KNI, W | result |
|---|---|---|---|
| current / `0014/r1/0` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0014-01:F`, `EIS-0014-02:P` | agree |
| current / `0014/r1/1` | `D1`, `W1` | `D2`, `K`, `W1`; `EIS-0014-02:F`, `EIS-0014-01:P` | `I-SEM-001` |
| current / `0014/r1/4` | `D0`, `W1` | `D0`, `I`, `W1`; no positive relation | agree |
| current / `0014/r3/1` | `A0/NOT_A_DEFECT_CLAIM`, `W1` | `A0/NOT_A_DEFECT_CLAIM`, `I`, `W1`; no positive relation | agree |
| current / `0023/r1/0` | `D1`, `W1` | `D1`, `K`, `W1`; `INS-0023-01:P` | agree |
| current / `0023/r1/5` | `D2`, `W1` | `D2`, `K`, `W1`; `INS-0023-01/02/03:F` | agree |
| current / `0023/r1/6` | `D2`, `W1` | `D2`, `K`, `W1`; `INS-0023-01/02/03:F` | agree |
| current / `0029/r1/2` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0029-01:F` | agree |
| current / `0029/r1/6` | `D1`, `W1` | `D1`, `K`, `W1`; `EIS-0029-05:P` | agree |
| current / `0029/r1/23` | `D2`, `W1` | `D2`, `K`, `W1`; `DIFF-0029-06:P`, `EIS-0029-03/05:F`, `INS-0029-05:F` | agree |
| current / `0029/r1/25` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0029-04:F` | agree |
| current / `0049/r2/0` | `D2`, `W2` | `D2`, `K`, `W2`; `EIS-0049-01:F` | agree |
| current / `0049/r2/2` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0049-01:P`, `INS-0049-03:F` | agree |
| current / `0049/r2/21` | `A0/FALSE_POSITIVE`, `W2` | `A0/FALSE_POSITIVE`, `I`, `W2`; no positive relation | agree |
| current / `0053/r1/0` | `D2`, `W2` | `D2`, `K`, `W2`; `EIS-0053-01:F` | agree |
| current / `0053/r1/1` | `D2`, `W2` | `D2`, `K`, `W2`; `DIFF-0053-01:P`, `INS-0053-02:F` | agree |
| baseline / `0014/r1/0` | `D1`, `W1` | `D1`, `K`, `W1`; `VU-0014-01:P` | agree |
| baseline / `0014/r1/2` | `D1`, `W1` | `D2`, `K`, `W1`; `EIS-0014-02:F` | `I-SEM-002` |
| baseline / `0014/r1/3` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0014-04:F` | agree |
| baseline / `0023/r1/0` | `D2`, `W1` | `D1`, `K`, `W1`; `INS-0023-01:P` | `I-SEM-003` |
| baseline / `0023/r1/1` | `D2`, `W1` | `D2`, `K`, `W1`; `INS-0023-01/02/03:F` | agree |
| baseline / `0029/r1/1` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0029-03:F` | agree |
| baseline / `0029/r1/2` | `D2`, `W1` | `D1`, `K`, `W1`; `EIS-0029-03:P` | `I-SEM-004` |
| baseline / `0029/r1/6` | `D0`, `W1` | `D0`, `I`, `W1`; no positive relation | agree |
| baseline / `0049/r1/0` | `D2`, `W1` | `D2`, `K`, `W1`; `EIS-0049-01:F` | agree |
| baseline / `0049/r1/2` | `A0/FALSE_POSITIVE`, `W1` | `A0/FALSE_POSITIVE`, `I`, `W1`; no positive relation | agree |
| baseline / `0053/r1/0` | `D0`, `W1` | `D0`, `I`, `W1`; no positive relation | agree |
| baseline / `0053/r1/1` | `D2`, `W1` | `D2`, `K`, `W1`; `DIFF-0053-01:P`, `INS-0053-02:F` | agree |

The source-read D/A agreement is `24/28 = 85.71%`; the four mismatches are
listed below. The blind relation axis was withheld, so no relation-agreement
percentage is claimed. W agreement is `28/28 = 100.00%` at the reviewed rows;
this does not validate unreviewed rows or the batch attestation.

## Findings

### I-SEM-001: current initial-action ambiguity was upgraded from D1 to D2

- Severity: `I`.
- Record: `v60:0014:r1:issue:1`, raw
  `raw/v60_current/method/method/0014/round-1.json#/report_issue_clusters/1`.
- Canonical: the decision with that raw pointer in
  `derived/manual_adjudication_v2/v60_report_decisions.json:1` is
  `D2/VALID_KNOWN/K`, with `EIS-0014-02:F` and `EIS-0014-01:P`.
- Evidence: `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0014/nl.txt:8`
  requires `Entry/Accelerate`; `plantuml.puml:7` puts the text on the initial
  pseudo-state edge. It supports both a transition-effect reading and an
  entry-action reading, so the blind proposal recorded `D1/W1`.
- Reason: the canonical reason does not rebut the concrete second reading.
  The known relation may remain, but the D-level upgrade needs targeted
  evidence rather than a batch assertion.
- Disposition: `FAIL`; targeted D1/D2 rereview required. Repair commit:
  `N/A` (read-only reviewer). Targeted rereview after repair: `NOT RUN`.

### I-SEM-002: baseline Entry/Accelerate ambiguity was upgraded from D1 to D2

- Severity: `I`.
- Record: `x1v2:0014:r1:issue:2`, raw
  `raw/x1v2_baseline/method/run1/0014-luna/record.json#/parsed_output/issues/2`.
- Canonical: the decision for `0014:r1:baseline_issue_3` in
  `x1v2_report_decisions.json:1` is `D2/VALID_KNOWN/K`, `EIS-0014-02:F`.
- Evidence: NL `reference/x1v2_input_closure/pairs/0014/nl.txt:8` and
  PlantUML `plantuml.puml:7` use the same initial-edge label. The source does
  not resolve transition effect versus entry action.
- Reason: the canonical row lacks the required rebuttal of the second reading;
  the D-level change is not independently supported by the cited source.
- Disposition: `FAIL`; targeted D1/D2 rereview required. Repair commit:
  `N/A`. Targeted rereview after repair: `NOT RUN`.

### I-SEM-003: baseline PumpState action claim was upgraded from D2 to D1

- Severity: `I`.
- Record: `x1v2:0023:r1:issue:0`, raw
  `raw/x1v2_baseline/method/run1/0023-luna/record.json#/parsed_output/issues/0`.
- Canonical: the decision for `0023:r1:baseline_issue_1` in
  `x1v2_report_decisions.json:1` is `D1/VALID_KNOWN/K`, `INS-0023-01:P`.
- Evidence: the raw claim points to three initial targets; NL
  `reference/x1v2_input_closure/pairs/0023/nl.txt:3` says the system first
  enters PumpState, while PlantUML `:3-8` gives PumpState, WaterState, and
  MethaneState co-equal pseudo-state entries. The blind proposal treated that
  first-entry violation as D2.
- Reason: the canonical D1 needs a concrete surviving alternative reading of
  “first transitions to PumpState.” The source and ledger item
  `reference/ledger.json#/items/INS-0023-01` provide a direct obligation; the
  relation is currently only partial in canonical and must be reviewed with
  the D-level together.
- Disposition: `FAIL`; targeted D1/D2 and FULL/PARTIAL rereview required.
  Repair commit: `N/A`. Targeted rereview after repair: `NOT RUN`.

### I-SEM-004: baseline undefined exit target claim was downgraded from D2 to D1

- Severity: `I`.
- Record: `x1v2:0029:r1:issue:2`, raw
  `raw/x1v2_baseline/method/run1/0029-luna/record.json#/parsed_output/issues/2`.
- Canonical: the decision for `0029:r1:baseline_issue_3` in
  `x1v2_report_decisions.json:1` is `D1/VALID_KNOWN/K`, with
  `EIS-0029-03:P`.
- Evidence: raw points to `lane_change --> exit_hwy : dist_to_exit<2`;
  PlantUML `reference/x1v2_input_closure/pairs/0029/plantuml.puml:16-17`
  contains that edge but no authored `exit_hwy` state or continuation, while
  NL `:4` requires exiting the highway.
- Reason: the source gives a concrete undefined-target fact and a named exit
  obligation. Canonical D1/PARTIAL may be defensible only with a specific
  alternative reading explaining why the missing target is not the same
  expected defect; the current reason does not state it.
- Disposition: `FAIL`; targeted D1/D2 and relation rereview required. Repair
  commit: `N/A`. Targeted rereview after repair: `NOT RUN`.

## W and closure checks

The reviewed W values agree `28/28`: current W2 rows retain typed input, exact
artifact hash, terminal result, and receipt; baseline rows remain W1 and no
baseline predicate usage or W2 was inferred. The selected canonical invalid
rows have all `NO_MATCH` relations, so the mechanical invalid closure passes
for this selection. This does not settle rows whose D/A may change, because a
changed D2/D1 row must be relation-closed again.

No later Judge output was used to raise W. All source references in the 28
candidate rows resolve to existing files and in-range line spans; raw SHA-256
values match the persisted inventory.

## Disposition and targeted rereview

The four `I` findings above remain open. There is no repair commit because this
reviewer is read-only and did not modify canonical data. Targeted rereview
after repair is `NOT RUN`; the affected rows must be re-adjudicated and any
changed canonical JSON, dense relations, summaries, and manifests regenerated
before a follow-up reviewer can return `PASS`.

This report is not a global semantic PASS: `1755/1783` rows were not
independently source-read in this round.

## Reproduction commands

All commands are provider-free and read-only:

```bash
jq '.records | length' reviews/16_semantic_raw_first_full_proposal.json
jq '.decisions | length' derived/manual_adjudication_v2/v60_report_decisions.json
jq '.decisions | length' derived/manual_adjudication_v2/x1v2_report_decisions.json

jq '.decisions[] | select(.report_id=="0029:r1:baseline_issue_3") |
  {strict_da, a0_type, validity, corrected_kni, relations}' \
  derived/manual_adjudication_v2/x1v2_report_decisions.json

sha256sum reviews/16_semantic_raw_first_full_proposal.json \
  derived/manual_adjudication_v2/v60_report_decisions.json \
  derived/manual_adjudication_v2/x1v2_report_decisions.json
git diff --check
```

`shuorenhua` audit: scene `docs/status`, level `minimal`, scope `audit-only`.
Pass 1 protected all paths, hashes, IDs, numbers, enums, and evidence
relations. Pass 2 removed narrator/template phrasing without changing the
coverage qualification or technical spans.
