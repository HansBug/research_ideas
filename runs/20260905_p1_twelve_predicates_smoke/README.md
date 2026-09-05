# Twelve-predicate smoke and v61 comparison

Date: 2026-09-05. Purpose: check that predicate deletion and renumbering leave
the method runnable, then investigate unexpected behavior on matched v61 inputs.
This is a descriptive diagnostic, not a scored quality evaluation, ablation,
or main result. The completed sample is 10 cells: the initial two plus eight
follow-up cells, not ten additional cells.
No evaluation Judge was invoked; the method's own D assignment remains part of
its normal pipeline. No v61 artifact was read as an input or rewritten.

## Run identity

Initial smoke:

- Run: `30322c29f93a4e0588d2db27c9ec7d8d`.
- Source: clean commit `71774498d65f3e3a7df5a30fbd7128236756fc1f`.
- pyfcstm submodule: `901f30e981c29eb8e304b33d61985652d2e85b2e`.
- Registry: `four-family-12-core.v1`, hash `sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d`.
- Profile and observed model: `gpt-5.6-luna`; configured adapter: `openai-responses`.
- Selection: pairs 0002 and 0024, one round each, two workers.
- Time: 04:32:14 to 04:40:54 UTC. Both cells completed on their first cell attempt.
- Input: `pipeline/representation/reports/llms_emp_r45_java_60` under the paper workspace.
- Registration: [P1 smoke contract](https://github.com/HansBug/research_ideas/pull/203#issuecomment-5549193195).

Follow-up: two independently launched one-round batches, each selecting
0002/0024/0009/0034 with two workers and the same input root, profile, registry,
and submodule. Both started at clean source
`835e299a8927964816cd958a4da6f6c794ee53c1`; method source, `utils/`, and pyfcstm
have no diff from the initial smoke revision. Selection and scope were recorded
in the [follow-up contract](https://github.com/HansBug/research_ideas/pull/203#issuecomment-5552116591).

| Batch | Run ID | UTC interval | Cells |
| --- | --- | --- | --- |
| Initial | `30322c29f93a4e0588d2db27c9ec7d8d` | 04:32:14-04:40:54 | 2 |
| Batch 1 | `8f264ec47610400abb965071d08ff84d` | 13:25:38-13:47:27 | 4 |
| Batch 2 | `b732e204f8bf4ff4a3869220789fe4ad` | 13:48:10-14:07:39 | 4 |

Only this summary is versioned. Initial detailed records remain local under
`30322c29f93a4e0588d2db27c9ec7d8d/`; follow-up records are under
`../20260905_p1_twelve_predicates_smoke_followup/batch1/<run-id>/` and
`../20260905_p1_twelve_predicates_smoke_followup/batch2/<run-id>/`.
All are covered by the repository's `/runs/` ignore rule and are absent from
the PR file diff and a fresh checkout. The follow-up directory also retains the
read-only `compare.py` and generated `comparison.json`, including cell hashes,
matched/unmatched receipts, and published-report inventories.
The manifest records source provenance, exact input hashes, registry identity,
selection, and retry policy. The `llm/` tree retains prompts, raw responses,
observed model, usage, schema errors, and audit receipts. Credentials are not
included. Empty runtime lock files are not part of the saved evidence.

## Completion and execution

| Batch | Cell status | Published reports | Saved receipts | Terminal Boolean | Unsupported |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 completed | 25 | 54 | 26 | 28 |
| Batch 1 | 4 completed | 36 | 106 | 45 | 61 |
| Batch 2 | 4 completed | 33 | 96 | 44 | 52 |
| Total | 10 completed | 94 | 256 | 115 | 141 |

Published-report counts come from `stage_outputs.publish.report_issue_count`
and `report_issue_clusters`, not the intermediate `model_output.issues` list.
Published reports comprise 29 W2 and 65 W1; the 115 terminal receipts comprise
61 false/violation and 54 true/pass results. Intermediate evidence-record W2
counts are not published-report W2 counts.

All non-null receipt IDs belong to the current registry. Terminal execution
exercised 11 of 12 predicates: S1-S5, G1/G3, R1-R3, and V1. G2 was not exercised.
New G3 returned true on 0009 in both follow-ups; new R3 and V1 also executed.
0034's three R2 checks returned false/true/true in both follow-ups, agreeing
with the corresponding checks in all three v61 rounds. No old-ID lookup error
or backend-dispatch crash was observed.

All ten cells are eligible with zero cell/audit errors and no whole-cell retry.
The 52 recorded stage calls succeeded; 13 schema-validation failure events
were corrected within their original stages. Batch 2 / 0024 grounding had one
300-second provider timeout, recovered by the existing transport retry policy
(one scheduled record and one recovery record, not two failures).
Unsupported evidence and local-progress diagnostics remain recorded rather
than crashing the cell. The initial 0024 local-progress diagnostics withheld
two claims on states with outgoing transitions. Completion does not establish
that every obligation was successfully grounded or correctly adjudicated.
Configured cost estimates are $0.119003 initial, $0.294683 batch 1, and
$0.203394 batch 2; the follow-up estimate is $0.498077, not a relay invoice.

## Matched v61 comparison

The historical comparator is the three frozen v61 rounds for each selected
pair, under `final_results/v61_source_divergence_vs_x1v2_baseline/raw/v61_current/method/method/`
in the paper workspace. Its source is
`ea6141607037d6daabe7df6826fc7c90dab7a12b`, with method source identical to the
pre-P1 base `4f74a2b60b3ecfde1ce0a83f466f8ff64f78433c`.
All eight input-content hashes agree. Context manifests agree after removing
their hash and normalizing only the checkout-root path. Historical and current
observed models are `gpt-5.6-luna` with matching configured context/output limits.

| Pair | v61 reports r1/r2/r3 | Current initial/batch 1/batch 2 | v61 published W2 | Current published W2 |
| --- | --- | --- | --- | --- |
| 0002 | 12 / 10 / 7 | 15 / 8 / 10 | 6 / 6 / 6 | 7 / 6 / 6 |
| 0024 | 8 / 6 / 8 | 10 / 12 / 7 | 2 / 2 / 1 | 2 / 2 / 1 |
| 0009 | 9 / 10 / 11 | not run / 9 / 9 | 2 / 2 / 2 | not run / 1 / 2 |
| 0034 | 10 / 10 / 11 | not run / 7 / 7 | 1 / 1 / 2 | not run / 1 / 1 |

Of 115 current terminal receipts, 93 match a historical terminal receipt on
pair, version-mapped predicate, and full typed inputs (element-ref order is
normalized). All 93 verdicts agree; the other 22 have no exact historical
input match and are not counted as either agreement or disagreement. Matching
uses old G4 -> G3, R4 -> R3, and V4 -> V1 after excluding retired IDs, so old
G3/R3/V1 cannot collide with current names. This is a receipt-level check with
repeated inputs, not 93 independent tests of quality equivalence.

The existing full-v61 label-only audit is also relevant: all 1,114 terminal
receipts among 2,436 saved receipts belong to retained predicates. Retired S6
accounts for seven nonterminal receipts and no terminal result. This supports
the narrow conclusion that deleting the seven predicates does not remove an
existing v61 terminal witness; it does not prove unchanged future generation.

## Expected variation and unexpected losses

| Observation | Saved evidence and mechanism | Assessment |
| --- | --- | --- |
| Initial report inflation does not persist uniformly | 0002 falls from 15 to 8/10; its two extra effect claims disappear. Its six stable W2 themes remain. 0024 varies 10/12/7; extra signal-as-variable claims and individual guard reports overlap other obligations and do not persist. | Consistent with variable contract splitting and grounding, not evidence of a uniform inflation regression. Counts alone do not establish precision. |
| 0009 collision guard repeatedly loses W2 | v61 uses `dist_to_rear<5 and vel>30` and publishes W2 in all three rounds. Follow-ups use `dist_to_rear<5 and vel>30 km/h` and `dist_to_rear<5 & vel>30`; both fail the native FCSTM logical-expression parser, so this same issue remains W1 in both runs. | A repeated loss of executable evidence on a retained S5 obligation, not an intended consequence of removing a predicate. Batch 2's second W2 is another guard; the aggregate W2 count hides this loss. |
| 0034 cardinality report is absent twice | All three v61 rounds publish the InMotion 0-versus-3 substate report. Both follow-ups select `explicit_named_members` in the contract but supply exact `direct_child_states` bindings; no agreeing owner binding is selected, and the frontier records `owner_candidate_count=0`, unresolved. Three individual containment reports remain. | A reproducible-in-this-sample binding-domain mismatch suppresses one report. This may overlap the same underlying defect as containment, so a report loss is not automatically a lost ledger hit. |
| 0024 batch 2 suppresses a correctly detected entry-action issue | S4 for Accelerating/entry/Accelerate returns false, matching v61. The saved D prompt explicitly includes verdict `false`, the counterexample, and reason "The exact action is not attached to the native FCSTM entry lifecycle slot." D nevertheless says the receipt establishes that Accelerate exists, assigns not-established/rebutting-survives, and the issue is not published. | An actual semantic-adjudication error after correct deterministic detection. Missing source attribution also lowers W, but cannot explain D reversing the supplied fact. v61 publishes this issue in all three rounds, including once as W1. |

The last case is obligation `0024:r1:i12`, contract
`NL-CONTRACT-NL8-ACTION-1`, in batch 2. Its exact input/output are retained in
`llm/method/0024/round-1/d-adjudication/cell-attempt-1/audit.jsonl` under that run.
The dossier projection did not omit or invert the false verdict. The
cardinality failures are in each 0034 cell's saved frontier checks and D
decisions. The S5 guard spellings and refusal reasons are in each 0009 cell;
an offline native-parser check confirms that only the historical spelling
parses among these three strings.

Code comparison localizes the risks: `backends/source_static.py` retains the
same S4/S5 implementations and guard parser; `semantics/frontier.py` retains
the same cardinality-domain matching/fallback logic; the D dossier projection
in `semantics/workflow.py` is unchanged. P1 does change shared prompt text and
routing, and generated contracts/bindings differ. The diagnostic therefore
identifies existing failure mechanisms exercised by current outputs, but does
not isolate whether P1 prompts, ordinary sampling, or provider changes caused
their increased occurrence. Unchanged downstream code is not proof of an
unchanged end-to-end distribution.

Secondary presentation variability also remains: batch 1 / 0024 publishes a
W2 entry-action report with a stale "Grounding remains unresolved" title;
batch 2 / 0002 adds a suspicious owner/self default-entry W1 claim. Similar
title/scope patterns already occur in v61. These are review concerns, not
newly adjudicated INVALID reports. Other action/effect claims also appear and
disappear; stable report totals must not be read as identical issue sets.

## Risk assessment and limits

- Runtime migration: no observed dispatch, ID-mapping, or matched-Boolean
  regression. The smoke supports functional use of the 12-predicate registry,
  not complete input or G2 coverage.
- End-to-end discovery: not a clean quality-parity result. Two repeated
  binding/evidence losses and one false-receipt misreading can affect W2
  support or final reports. They expose general pipeline failure modes, but
  ten selected cells cannot estimate their population frequency or prove a
  P1-caused systematic performance decrease.
- Paper evidence: the selected-12 vocabulary claim is not contradicted by
  these observations. Claims of unchanged hit/precision, lossless semantic
  adjudication, or an always-preserved report set are not supported. Frozen
  v61 raw/derived results, manifests, and metrics remain untouched; this smoke
  does not replace or relabel the implementation that produced them.
- No evaluation Judge or ledger matching was run. Under the current protocol,
  precision is `(VALID_KNOWN + VALID_NOVEL) / all reports`; W1 and duplicate
  reports are not automatically false positives. No new hit/precision number
  or statistical equivalence claim follows from this comparison.
- The four pairs are purposively selected; 0024/0034 share the train-system
  NL but have different model representations. The v61 calls were on September
  3 UTC and these calls on September 5. Matching model labels do not guarantee
  an immutable provider snapshot. This is not a contemporaneous randomized
  old/new comparison.

The ten-cell diagnostic is complete; no further live cells, method changes,
Judge calls, or v61 reruns were made. Additional undirected cells are not the
most informative next step: the saved guard/domain and false-receipt dossiers
already identify concrete failure paths for a separately scoped investigation.

## Invocation

Python: `/home/zhangshaoang/oo-projects/research_ideas/venv/bin/python`.
`LLM_CONFIG_FILE` selected the sibling checkout's profile configuration;
`PYTHONPATH` selected this checkout's method, evaluation, judge, paper,
pyfcstm, and repository roots. Only the method CLI was executed:

```text
python -m paper_stm_method.cli
  --report-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60
  --output-dir runs/20260905_p1_twelve_predicates_smoke
  --profile gpt-5.6-luna --rounds 1
  --pair-id 0002 --pair-id 0024 --workers 2 --allow-live
```

For each follow-up batch, the same invocation used:

```text
  --output-dir runs/20260905_p1_twelve_predicates_smoke_followup/batchN
  --profile gpt-5.6-luna --rounds 1
  --pair-id 0002 --pair-id 0024 --pair-id 0009 --pair-id 0034
  --workers 2 --allow-live
  --predecessor-snapshot runs/20260905_p1_twelve_predicates_smoke/30322c29f93a4e0588d2db27c9ec7d8d
```

`batchN` was respectively `batch1` and `batch2`; each has its own run manifest
and uses local round 1. A prior `--rounds 2` command was rejected during CLI
argument validation before any provider call or output initialization; the
accepted values are 1 and 3. The correction did not alter the CLI or budget.
