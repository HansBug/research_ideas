# Twelve-predicate functional smoke

Date: 2026-09-05. Purpose: check that predicate deletion and renumbering leave
the method runnable. This is not a quality evaluation, ablation, or main result.
No evaluation Judge was invoked; the method's own D assignment remains part of
its normal pipeline. No v61 artifact was read as an input or rewritten.

## Run identity

- Run: `30322c29f93a4e0588d2db27c9ec7d8d`.
- Source: clean commit `71774498d65f3e3a7df5a30fbd7128236756fc1f`.
- pyfcstm submodule: `901f30e981c29eb8e304b33d61985652d2e85b2e`.
- Registry: `four-family-12-core.v1`, hash `sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d`.
- Profile and observed model: `gpt-5.6-luna`; configured adapter: `openai-responses`.
- Selection: pairs 0002 and 0024, one round each, two workers.
- Time: 04:32:14 to 04:40:54 UTC. Both cells completed on their first cell attempt.
- Input: `pipeline/representation/reports/llms_emp_r45_java_60` under the paper workspace.
- Registration: [P1 smoke contract](https://github.com/HansBug/research_ideas/pull/203#issuecomment-5549193195).

Only this summary is versioned. Detailed records remain local under
`30322c29f93a4e0588d2db27c9ec7d8d/`, covered by the repository's `/runs/` ignore
rule; they are not included in the PR file diff or a fresh checkout.
The manifest records source provenance, exact input hashes, registry identity,
selection, and retry policy. The `llm/` tree retains prompts, raw responses,
observed model, usage, schema errors, and audit receipts. Credentials are not
included. Empty runtime lock files are not part of the saved evidence.

## Observed behavior

| Pair | Cell status | Published reports | Saved receipts | Terminal Boolean | Unsupported |
| --- | --- | --- | --- | --- | --- |
| 0002 | completed | 15 | 23 | 13 | 10 |
| 0024 | completed | 10 | 31 | 13 | 18 |
| Total | 2 completed | 25 | 54 | 26 | 28 |

Published-report counts come from `stage_outputs.publish.report_issue_count`
and `summary.json`, not the intermediate `model_output.issues` list. The 26
terminal receipts comprise 14 false/violation and 12 true/pass results. Neither
receipt counts nor report counts establish hit or precision.

All non-null receipt IDs belong to the current registry. Terminal execution
exercised G1, R1, R3, S1, S2, S3, S4, and V1. Renumbered R3 completed with a
true native state-retention result; V1 completed with a false stable-leaf
progress result. G3 was not exercised by these two samples; its current
contract and backend checks are in the separate provider-free test evidence.

The unsupported receipts remain explicit W1 candidates where binding, source
attribution, or the executable fragment is insufficient. For example, 0002
retains action/effect issues without a predicate, and its three nonterminal G1
plans lack the required fragment and artifact attribution. No old-ID lookup
error, backend-dispatch crash, cell error, or audit error was observed.

Two schema errors were repaired inside their original stages: a missing
`cardinality_bindings.0.basis` in 0002 grounding, and covered segment IDs without
matching contracts in 0024 extraction. Both stages subsequently succeeded.
0024 grounding also records two `exact_local_progress_satisfied` diagnostics:
the native state has outgoing transitions, so that local dead-end claim was
withheld. Its stage is `completed_with_diagnostics`; the cell is `completed`.

This smoke supports continued functional experimentation on the new registry.
It does not establish quality parity with v61 or behavior on every input.

A read-only comparison with the corresponding three v61 rounds found the same
input content and observed model. Of 26 current terminal receipts, 23 have a
historical match after version-aware ID mapping and element-ref ordering; all
23 verdicts agree. Published counts increased from 12/10/7 to 15 for 0002 and
8/6/8 to 10 for 0024, mainly through additional W1 obligations and overlapping
reports. This leaves report inflation unresolved, not a demonstrated backend
regression or quality improvement. Detailed comparison notes remain local in
the run directory; no additional provider call or evaluation was performed.

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
