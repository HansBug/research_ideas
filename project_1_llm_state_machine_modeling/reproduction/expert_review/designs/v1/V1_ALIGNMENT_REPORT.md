# Expert Review V1 Alignment Report

本文档是 `Phase 6` 的版本级对齐报告与冻结说明。它服务于两件事：

1. 固定当前 `v1` 代码树在 `Phase 6` 收口后的真实状态。
2. 明确说明为什么当前版本**还不能冻结**，以及为什么已经打开下一阶段继续提分。

当前收口时间：`2026-04-16 21:48:23`

当前收口评测口径：`run_benchmark_iteration(llm_mode='off')`

## 1. 当前结论

- `Phase 6` 已完成其定位内的工作：冻结标准核验、路径收口、兼容边界清理、版本级对齐汇总。
- 当前 `v1` 运行时已经稳定落在 [`schemas/`](../../schemas/) + [`prompts/`](../../prompts/) + [`tools/`](../../tools/) + [`agents/`](../../agents/) + [`graph/`](../../graph/) + [`compatibility/`](../../compatibility/) 主干层次。
- `Phase 6` 没有继续改评分逻辑；其代码收口后 benchmark 指标与 `Phase 5 Round 0` 保持一致，没有出现明显回退。
- 当前版本**不满足冻结门槛**，因此不能宣告 `v1` 终止迭代；后续提分工作已转入 [TODO.md](./TODO.md) 中新增的 `Phase 7`。

## 2. Phase 演化总表

| Phase | 主要定位 | `HAI` | `RAS` | `SAS` | `PDS` | `normalized_mae` | `issue_f1` | `unsupported_claim_rate` | `ece` | `vv_role_coverage` |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `Phase 1` | 运行时骨架替换 | `66.58` | `60.82` | `62.51` | `87.50` | `0.2177` | `0.5810` | `0.5547` | `0.6857` | `0.5000` |
| `Phase 2` | contract / regime / policy 收口 | `66.12` | `60.30` | `61.84` | `87.50` | `0.2285` | `0.5924` | `0.5398` | `0.6909` | `0.5000` |
| `Phase 3` | equivalence 与 arbitration 主路径化 | `68.13` | `63.94` | `61.84` | `87.50` | `0.1772` | `0.5621` | `0.5704` | `0.6109` | `0.5000` |
| `Phase 4` | evidence discipline / summary-protocol 收口 | `78.62` | `74.76` | `75.02` | `93.75` | `0.1758` | `0.8202` | `0.1778` | `0.5302` | `0.7500` |
| `Phase 5` | 多智能体 graph 主路径与目录结构收敛 | `78.68` | `74.87` | `75.02` | `93.75` | `0.1751` | `0.8202` | `0.1778` | `0.5302` | `0.7500` |
| `Phase 6` | 冻结前核验与代码树收口 | `78.68` | `74.87` | `75.02` | `93.75` | `0.1751` | `0.8202` | `0.1778` | `0.5302` | `0.7500` |

当前演化观察：

1. 真正的大幅跃迁发生在 `Phase 4`，说明当前 reviewer 的主要质量提升来自 evidence discipline、summary/protocol regime awareness 与 calibration 收敛。
2. `Phase 5` 的主要收益不是继续拉高分数，而是在不牺牲指标的前提下完成真实多智能体 graph 主路径和目录结构收敛。
3. `Phase 6` 的定位是收口而不是提分；当前指标与 `Phase 5 Round 0` 一致，符合“没有明显回退”的要求。

## 3. 冻结门槛核验

停止标准见 [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md) 第 `14` 节。

| 指标 | 当前值 | 门槛 | 结果 |
|---|---:|---:|---|
| `HAI` | `78.68` | `>= 85` | `未达标` |
| `RAS` | `74.87` | `>= 88` | `未达标` |
| `SAS` | `75.02` | `>= 80` | `未达标` |
| `PDS` | `93.75` | `>= 78` | `达标` |
| `normalized_mae` | `0.1751` | `<= 0.08` | `未达标` |
| `issue_f1` | `0.8202` | `>= 0.75` | `达标` |
| `human_issue_coverage_recall` | `0.8500` | `>= 0.80` | `达标` |
| `equivalence_false_reject_rate` | `0.0000` | `<= 0.10` | `达标` |
| `unsupported_claim_rate` | `0.1778` | `<= 0.08` | `未达标` |
| `protocol_only_overclaim_rate` | `0.0000` | `<= 0.05` | `达标` |
| `ece` | `0.5302` | `<= 0.08` | `未达标` |
| `rerun_score_std` | `0.0000` | `<= 0.03` | `达标` |

稳定性门槛当前也**不成立**，因为第一层指标门槛本身还没有同时满足，更不可能满足“连续两轮完整验证都成立”的要求。

## 4. 当前 v1 的正式运行时定义

### 4.1 Prompt / Policy / Rubric

- contract 理解入口：[`prompts/contract_router.py`](../../prompts/contract_router.py)
- policy prompt：[`prompts/review_policy.py`](../../prompts/review_policy.py)
- extraction prompts：[`prompts/extraction.py`](../../prompts/extraction.py)
- analysis prompts：
  - [`prompts/traceability.py`](../../prompts/traceability.py)
  - [`prompts/equivalence.py`](../../prompts/equivalence.py)
  - [`prompts/quality_review.py`](../../prompts/quality_review.py)
  - [`prompts/missing_evidence.py`](../../prompts/missing_evidence.py)
  - [`prompts/arbitration.py`](../../prompts/arbitration.py)
- synthesis prompt：[`prompts/synthesis.py`](../../prompts/synthesis.py)
- deterministic policy packet 与 regime-sensitive score semantics：[`tools/policy_library.py`](../../tools/policy_library.py)
- 最终维度定义与 rubric weight 组装：[`agents/review_policy_builder.py`](../../agents/review_policy_builder.py)

当前正式维度为：

1. `notation_syntax`
2. `semantic_completeness`
3. `behavioral_consistency`
4. `requirement_traceability`
5. `pragmatic_clarity`
6. `evidence_discipline`

### 4.2 Agent 角色

当前真实主路径中的 agent 角色以 [`graph/runtime.py`](../../graph/runtime.py) 为准：

1. `Contract Router`
2. `Evidence Regime Estimator`
3. `Input Analyst`
4. `Prediction Extractor`
5. `Reference Extractor`
6. `Review Policy Builder`
7. `Traceability Agent`
8. `Equivalence and Difference Agent`
9. `Pragmatic Quality Agent`
10. `Missing-Evidence Critic`
11. `Disagreement Arbiter`
12. `Score Composer`
13. `Final Synthesizer`

这些角色不再只是文档命名，而是当前运行时真实会记录 `Agent context trimming` 与 `fan-out / fan-in` 的主路径节点。

### 4.3 Graph / Compatibility / Shared Root Files

- 正式编排主入口：[`graph/runtime.py`](../../graph/runtime.py)
- 条件边与阶段组织：[`graph/edges.py`](../../graph/edges.py)、[`graph/subgraphs.py`](../../graph/subgraphs.py)、[`graph/nodes.py`](../../graph/nodes.py)
- 对外兼容层：[`compatibility/legacy_api.py`](../../compatibility/legacy_api.py)
- 共享对外 schema：[`schema.py`](../../schema.py)
- 共享工具与环境辅助：[`inventory.py`](../../inventory.py)、[`utils.py`](../../utils.py)
- LLM provider 壳层：[`agent.py`](../../agent.py)

`Phase 6` 已删除仅用于测试 re-export 的旧临时文件 `expert_review_v1_runtime.py`；测试现已直接引用正式模块，而不是再通过兼容中转文件拿 helper。

## 5. Phase 6 收口动作

`Phase 6` 当前真正做过的代码收口包括：

1. 删除 `expert_review_v1_runtime.py`，去掉“测试 helper 通过旧运行时中转层暴露”的旁路。
2. 把 [`test_review.py`](../../test_review.py) 改成直接引用正式模块：
   - [`agents/input_analyst.py`](../../agents/input_analyst.py)
   - [`tools/artifact_probe.py`](../../tools/artifact_probe.py)
   - [`tools/dossier_merge.py`](../../tools/dossier_merge.py)
   - [`compatibility/legacy_api.py`](../../compatibility/legacy_api.py)
3. 从 [`agent.py`](../../agent.py) 移除 `heuristic_expert_review()`，把历史兼容 API 收敛到 [`compatibility/legacy_api.py`](../../compatibility/legacy_api.py)。
4. 更新模块说明文档，使当前目录导航与代码组织说明回到真实状态，而不是停留在 `Phase 1/2` 之前的根层单文件印象。

## 6. 回归验证

当前已完成的验证：

1. `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
2. `AIROUTER_API_KEY= FINDCG_API_KEY= MIAOCG_API_KEY= PYTHONPATH=project_1_llm_state_machine_modeling/reproduction python -m expert_review ...`
3. `PYTHONPATH=project_1_llm_state_machine_modeling/reproduction python - <<'PY' ... run_benchmark_iteration(llm_mode='off') ... PY`

验证结论：

1. 模块测试全部通过。
2. CLI 入口在 deterministic 模式下可以正常返回结构化结果。
3. benchmark 指标与 `Phase 5 Round 0` 保持一致，当前没有观察到明显回退。

## 7. 冻结说明与 Phase 7 入口

冻结结论：**当前版本不冻结。**

原因不是结构还没收干净，而是核心对齐指标仍明显达不到冻结门槛，尤其是：

1. `RAS`
2. `SAS`
3. `normalized_mae`
4. `unsupported_claim_rate`
5. `ece`

因此后续入口已经明确切到 [TODO.md](./TODO.md) 中新增的 `Phase 7`。`Phase 7` 的主要目标不是继续做树形清理，而是继续提分，重点针对：

1. `record-level` partial-heavy 样例仍偏高分。
2. `summary-level` 高分 public row 仍偏保守。
3. `protocol-only` taxonomy 语言仍偏 record-style。
4. `unsupported_claim_rate` 与 `ece` 仍远高于冻结门槛。
