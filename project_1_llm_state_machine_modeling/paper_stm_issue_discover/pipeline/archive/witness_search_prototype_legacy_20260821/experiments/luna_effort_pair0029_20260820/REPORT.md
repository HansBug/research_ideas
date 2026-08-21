# Luna Effort Probe on Pair 0029

## Summary and goal

This probe asks whether explicit reasoning effort changes `gpt-5.6-luna` issue-discovery quality, latency, and configured cost for the X1v2 baseline and our witness-search method. Pair `0029` was selected as a discriminating case with eight frozen ledger items spanning hierarchy, reachability, termination, internal consistency, and a D1 over-specification candidate.

The one-run result is not monotonic. X1v2 ranges from `2/8` to `5/8` ledger hits; our method holds `5/8` through `high` and reaches `6/8` at `xhigh` and `max`. The four ledger items `EIS-0029-01`, `EIS-0029-04`, `INS-0029-01`, and `INS-0029-05` are hit by our method at every tested setting. Higher effort is not automatically cleaner: our method is false-positive-free at `omitted` and `high`, but emits four false positives at `max`.

The tracked numeric source is [`metrics.json`](./metrics.json). It includes SHA-256 hashes for every ignored raw record used to build the table. Raw records remain under `runs/paper1/luna-effort-probe-20260820-v1/` and are intentionally excluded from Git.

## Experiment plan

1. Run one X1v2 cell and one witness-search cell for pair `0029` at each generator effort: omitted, `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
2. Keep the independent semantic judge fixed at `medium` so generator effort is the tested variable.
3. Measure exact ledger hits, emitted issues, false positives, token usage, elapsed time, and configured USD cost.
4. Preserve the provider default by sending no effort field in the omitted condition.

All 14 generator cells and all seven judge cells completed. No condition was excluded from the comparison.

## Setup

- Experiment date: `2026-08-20`.
- Pair: `0029`; denominator: eight frozen ledger items from `discover_matrix/ledger_v2/ledger.json`.
- Generator and judge profile: `gpt-5.6-luna`, adapter `openai-responses`.
- Judge effort: explicit `medium` for every condition.
- Generator calls per condition: X1v2 `1`; our method `5`.
- Pricing basis: configured OpenAI Standard short-context list prices, `$0.20/M` input and `$1.20/M` output. Relay billing may differ.
- Billing formula: input classes plus `output_tokens`; `reasoning_tokens` are already included in `output_tokens` and are not added again.

The omitted and explicit `medium` conditions use the same documented effective default but remain separate runs. Their output differences are therefore evidence of run-level sampling variation, not evidence that omission itself changes model capability.

## Results

### Aggregate quality and cost

`FP` is the judge's false-positive count among emitted issues. `Generation USD` includes X1v2 plus our method; `Judge USD` is reported separately because judge effort stayed fixed and retry/input volume varied by condition.

| Generator effort | X1v2 hits | X1v2 FP / emitted | Our hits | Our FP / emitted | Generation USD | Judge USD | Generation wall time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| omitted | 3/8 | 4/6 | 5/8 | 0/7 | 0.070827 | 0.007334 | 483.5 s |
| none | 3/8 | 6/9 | 5/8 | 5/12 | 0.060515 | 0.009291 | 346.7 s |
| low | 5/8 | 5/10 | 5/8 | 5/12 | 0.063677 | 0.026964 | 491.5 s |
| medium | 3/8 | 5/9 | 5/8 | 4/10 | 0.070272 | 0.009083 | 397.1 s |
| high | 2/8 | 5/8 | 5/8 | 0/7 | 0.091506 | 0.024274 | 816.1 s |
| xhigh | 4/8 | 1/7 | 6/8 | 2/10 | 0.131156 | 0.008626 | 1950.6 s |
| max | 5/8 | 0/5 | 6/8 | 4/13 | 0.178089 | 0.019037 | 3226.3 s |

Generation cost relative to explicit `none` is `1.05x` at `low`, `1.16x` at `medium`, `1.51x` at `high`, `2.17x` at `xhigh`, and `2.94x` at `max`. The comparison is within the same two-arm workload; raw X1v2 and method costs should not be compared as algorithmic efficiency because the method intentionally makes five model calls while X1v2 makes one.

### Exact ledger hits

| Effort | X1v2 hit IDs | Our-method hit IDs |
| --- | --- | --- |
| omitted | `EIS-0029-01`, `EIS-0029-02`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-03`, `EIS-0029-04`, `INS-0029-01`, `INS-0029-05` |
| none | `EIS-0029-02`, `EIS-0029-03`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-02`, `EIS-0029-04`, `INS-0029-01`, `INS-0029-05` |
| low | `DIFF-0029-06`, `EIS-0029-02`, `EIS-0029-03`, `EIS-0029-04`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-02`, `EIS-0029-04`, `INS-0029-01`, `INS-0029-05` |
| medium | `EIS-0029-02`, `EIS-0029-03`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-02`, `EIS-0029-04`, `INS-0029-01`, `INS-0029-05` |
| high | `DIFF-0029-06`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-03`, `EIS-0029-04`, `INS-0029-01`, `INS-0029-05` |
| xhigh | `DIFF-0029-06`, `EIS-0029-01`, `EIS-0029-03`, `EIS-0029-04` | `EIS-0029-01`, `EIS-0029-03`, `EIS-0029-04`, `EIS-0029-05`, `INS-0029-01`, `INS-0029-05` |
| max | `DIFF-0029-06`, `EIS-0029-02`, `EIS-0029-03`, `EIS-0029-04`, `INS-0029-01` | `EIS-0029-01`, `EIS-0029-03`, `EIS-0029-04`, `EIS-0029-05`, `INS-0029-01`, `INS-0029-05` |

The ledger meanings are grounded in `discover_matrix/ledger_v2/ledger.json`. In brief, our method's four all-setting hits cover the missing `AutonomousMode` hierarchy, missing composite-state default entries, unreachable collision avoidance, and ineffective termination. At `xhigh` and `max`, it additionally captures the cross-scope `FinishState` route (`EIS-0029-05`) while retaining the internal target inconsistency (`EIS-0029-03`). No our-method condition hits the D1 extra-edge item `DIFF-0029-06`.

### Token behavior

For X1v2, output tokens are `945` omitted, `1188` none, `1264` low, `1313` medium, `1055` high, `5153` xhigh, and `8713` max. The non-monotonic `high` value and the omitted/medium divergence show why effort must be treated as a soft budget rather than a deterministic token schedule.

For our method, total output tokens rise from `15,628` at `none` to `105,483` at `max`; reasoning-token detail rises from `0` to `88,038`. Exact per-arm usage and costs are in `metrics.json`.

## Analysis and limitations

The evidence supports three narrow conclusions. First, the new CLI and adapter path produces materially different usage profiles across effort settings. Second, our method is more stable than X1v2 on this pair's ledger coverage: it never falls below `5/8`, whereas X1v2 falls to `2/8` at `high`. Third, `xhigh` is the first setting in this probe to improve our-method coverage to `6/8`, but `max` adds cost without adding another hit and has more false positives.

The evidence does not establish an optimal global effort. This is one pair, one generation per setting, and one LLM judge pass per setting. There are no confidence intervals, `hit@3`, or `hit@all` estimates. Judge outputs are model assessments rather than human re-adjudication, and variable judge retries contribute noise to judge cost. Only Luna was exercised; Claude effort plumbing is covered by deterministic adapter tests but has no real-call result in this experiment.

A publication-grade follow-up should pre-register several representative pairs, run at least three independent generations per effort, keep judge inputs and judge effort fixed, and report `hit@1`, `hit@3`, `hit@all`, false-positive rate, cost, and latency together.

## Reproduction and QC

Regenerate the tracked metrics from the local raw records without calling a model:

```bash
LLM_CONFIG_FILE="${LLM_CONFIG_FILE:-../research_ideas/.llmconfig.yml}" \
PYTHONPATH=. python \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/witness_search_prototype/experiments/luna_effort_pair0029_20260820/summarize.py \
  --raw-root runs/paper1/luna-effort-probe-20260820-v1 \
  --profile gpt-5.6-luna \
  --output /tmp/luna-effort-pair0029-metrics.json

cmp /tmp/luna-effort-pair0029-metrics.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/witness_search_prototype/experiments/luna_effort_pair0029_20260820/metrics.json
```

The isolated worktree intentionally does not copy the private `.llmconfig.yml`; `LLM_CONFIG_FILE` points at the sibling primary worktree by default and can be overridden. The summarizer rejects model mismatches, missing pricing, wrong requested effort, a judge not fixed at `medium`, and any source file whose expected path is absent. `source_sha256` in `metrics.json` is the evidence bridge to the ignored raw artifacts.

## Sources

- [GPT-5.6 Luna model page](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [Reasoning effort deployment guidance](https://developers.openai.com/api/docs/guides/deployment-checklist#set-up-reasoningeffort)
- [Responses API spending controller: reasoning tokens are included in output totals](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api#limits-and-other-costs)
