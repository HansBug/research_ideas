# A2 Sonnet 5 全量复现实验：事前登记

登记日期：2026-09-09，Sonnet method 调用前。该批次是对已有 15-pair Sonnet5 pilot 的全量确认，不把 pilot 结果当作最终 C-2 证据。

## 1. 研究问题与解释边界

在相同冻结输入、相同台账和相同独立 Luna v3.11 judge 下，关闭整套 predicate-guided evidence mechanism 后，报告覆盖、FULL hit、precision 和跨轮稳定性相对 Sonnet full ours 如何变化？本实验估计的是整套机制的净差异，不拆分 predicate vocabulary、prompt guidance、binding、compiler/backend 或 execution receipt 的单独因果贡献。

Sonnet 5 是压力配置：它用于提高潜在幻觉差异的可见性，不代表总体模型分布，也不构成模型排名。最终解释必须同时披露 Sonnet 与 pane9 冻结 full/baseline 的来源身份和时间差异。

## 2. 固定条件

| 项目 | 冻结值 |
| --- | --- |
| method profile | `claude-sonnet-5` |
| ablation | `no-predicates` |
| scope | 54 frozen pairs × 3 rounds = 162 method cells |
| method workers | 16 |
| transport retries | 8 |
| judge profile | `gpt-5.6-luna` |
| judge protocol | `semantic-judge.two-stage.v3.11` |
| judge workers | 8 |
| judge settings | 2 validity readings, arbitration, trigger `any`, `relation_first`, closure `full` |
| ledger | frozen `discover_matrix/ledger_v2/ledger.json` (145 entries; 435 expected-round units) |
| publication rule | method-owned D0/UNRESOLVED never enters published reports; judge D0 is an independent outcome |

Full Sonnet and baseline controls are read-only from pane9's complete E2 Sonnet archive (`54 × 3` per arm); no observed-result reselection or re-generation is allowed. The 15-pair pilot and raw-inspect-direct stress remain exploratory evidence only.

## 3. Ablation boundary

`no-predicates` disables predicate prompt guidance and generation, candidate routing, typed predicate binding, compiler/backend execution, execution receipts, and receipt-based filtering. It retains obligations, grounding, FCSTM/source representations, inspection and static/model facts, ordinary semantic binding, candidate construction, D/publication gates, deduplication, and source/contract safeguards. Thus the comparison is a joint mechanism ablation, not a backend-only intervention.

## 4. Outcomes

Primary: report precision `(K+N)/(K+N+I)` and FULL hit@1 over 435 expected-round units. Secondary: hit@3, hit@all, report count, K/N/I, strict D1/D2-only precision, invalid-report rate, pair-level coverage, and cross-round consistency. Report pair-level and aggregate values; use the nine frozen NL clusters for paired bootstrap/sensitivity, without treating reports or expected units as independent observations.

## 5. Evidence and failure policy

Every cell preserves source/input/prompt/schema/model hashes, complete stage receipts, raw outputs, usage, retries, failures/recovery, eligibility and method receipt. Judge inputs, prompts, raw responses and verdict receipts are stored separately under the run directory. Provider failures and irreparable schema failures are recorded as terminal diagnostics; internal budget/gate/unsupported-evidence conditions downgrade with artifacts and never silently remove a pair from the planned denominator. No result-driven retry or manual confirmation is introduced.

## 6. Claim limits and reviewer challenges

The intended claim is conditional: under the frozen Sonnet stress configuration, the complete predicate-guided mechanism changes the precision/coverage trade-off relative to its joint ablation. The experiment cannot identify which subcomponent caused a difference, cannot generalize from Sonnet to all backbones, and cannot use the raw-direct stress as a same-input causal control. A reviewer may challenge model-specificity, source/version mismatch with pane9 controls, judge dependence, one-draw stochasticity, and the compound nature of A2; these are addressed by freezing the full 54×3 grid, using one judge protocol, preserving all artifacts, reporting cluster-paired uncertainty and explicit limitations. Any null or reversed result narrows the claim rather than being treated as a failed experiment.
