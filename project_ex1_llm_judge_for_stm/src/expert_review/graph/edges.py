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
