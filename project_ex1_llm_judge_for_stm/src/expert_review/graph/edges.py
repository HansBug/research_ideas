"""Pipeline 阶段顺序常量定义 —— 单一真理源。

**作用**：把 LLM-as-STM-Judge pipeline 的 3 个 stage（PREPARATION /
ANALYSIS / FINAL）以及每个 stage 内 agent 节点的标准名称固化为元组
常量，供：

1. :func:`graph.subgraphs.ordered_stage_groups` 输出执行顺序；
2. :func:`graph.runtime.run_expert_review_workflow` 在循环中按此顺序
   调度；
3. :mod:`agents.orchestrator` 的 ``PREPARATION_FANOUT`` /
   ``ANALYSIS_FANOUT`` / ``FINAL_FANIN`` 元组保持一致；
4. logging / debugging 时统一 stage 名展示。

**设计思路**：

* **常量元组而非 enum**：3 个 stage 的成员名稳定后改动罕见，用 tuple
  即可；不引入额外枚举类减少认知开销；
* **agent 名字纯字符串**：与具体 :mod:`graph.nodes` 中的
  ``run_*_node`` 函数松耦合，logging 与实际调度可分离；
* **历史变迁注释保留**：FINAL_STAGE 中原含的 ``"Disagreement Arbiter"``
  在 W3 ablation E1 验证 ΔHAI = +0.1556 后已删除，但保留中文注释作
  audit trail（issue I-6）。

**关键约束 / 不变式**：

* 3 个元组中的成员个数必须与 :mod:`graph.nodes` 中的
  ``run_*_node`` 函数实数对齐；增删 agent 必须同步两处；
* PREPARATION 内的 6 个 agent 中前 4 个（Contract Router / Input Analyst /
  Prediction Extractor / Reference Extractor）逻辑上无依赖，可并行；
  Evidence Regime Estimator 依赖 dossiers；Review Policy Builder 依赖前
  五者；
* ANALYSIS 内的 3 个 agent 中 traceability + pragmatic_quality 可与
  equivalence 并行（equivalence 仅在有 ref 时跑）。
"""

PREPARATION_STAGE = (
    "Contract Router",
    "Input Analyst",
    "Prediction Extractor",
    "Reference Extractor",
    "Evidence Regime Estimator",
    "Review Policy Builder",
)

ANALYSIS_STAGE = (
    "Traceability Agent",
    "Equivalence and Difference Agent",
    "Pragmatic Quality Agent",
)

FINAL_STAGE = (
    "Missing-Evidence Critic",
    # 注：原 "Disagreement Arbiter" 已在 W3 ablation 验证（E1）后删除——
    # 跳过 arbiter 整段后 ΔHAI = +0.1556（反向贡献），故移除。
    # arbitrate_trace_and_equivalence 调用与 arbiter 模块均已下线。
    # trace_conflict_count 信号现在由 deterministic_equivalence 直接维护。
    "Score Composer",
    "Final Synthesizer",
)

__all__ = ["ANALYSIS_STAGE", "FINAL_STAGE", "PREPARATION_STAGE"]
