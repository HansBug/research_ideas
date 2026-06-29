# paper outline draft（R0 草案）

## 0. 说明

本文件只冻结第一篇论文的大纲方向和写作约束，不写最终正文。后续 PR-R7 必须根据 R1--R8 的真实证据重写或降级；R5.5 当前只提供 seed profile / readiness / conversion pressure，R5.6 只冻结 model scope / claim boundary，二者都不提供 repair-loop 主结果。

## 1. Abstract

- 背景：控制系统需求到状态机 artifact 后，实际使用需要可检查、可执行、可修正。
- 问题：一次性生成模型往往留下语义、guard/action、行为场景和可执行性缺陷。
- 方法：给定 `<NL, STM_0>`，使用 diagnostics、scenario feedback、repair 和 regression checks 构成无人化修正循环。
- 结果：只在 R6 后填写真实结果；若无充分证据，不写强提升。
- 范围：主线限定在 T0 离散 FSM / HSM / EFSM-lite / 离散 UML-SysML statechart 子集；T0.5 / T1-ish 仅作 caveat 或 supplementary stress。
- 限制：报告失败、回滚、振荡、转换损失、人工裁决边界，并禁止外推到 timed / hybrid / arbitrary UML / protocol FSM。

## 2. Introduction

1. 控制系统状态机建模的现实需求：不仅要生成图，还要可机检、可执行、可复核。
2. 旧 `NL -> STM` 生成路线的局限：初始 artifact 质量不稳，且后续缺少闭环修正。
3. 新任务定义：`<NL, STM_0> -> STM_k / Better STM`。
4. R5.6 模型范围：T0 离散 FSM / HSM / EFSM-lite / 离散 UML-SysML statechart 子集，明确 T0.5 / T1-ish / arbitrary UML 的降级角色。
5. 方法直觉：结构化 diagnostics + scenario feedback + accept/reject/rollback。
6. 贡献列表：任务定义、修正协议、Better STM 操作化、seed / converter / baseline 重排、实证评价。
7. 明确非贡献：不主张新 DSL，不主张完整形式化验证，不主张首个 `NL -> STM`，不主张 timed automata / arbitrary UML repair。

## 3. Background and Motivation

- 状态机 artifact 的描述性与可执行性差异。
- 轻量语义增强对 diagnostics / simulation / repair feedback 的必要性。
- seed 来源：prior artifact、弱 prompt、旧模型、学生或人工建模。
- Motivating example：后续由 R2/R4 提供，不在 R0 构造。

## 4. Task Definition

- 输入输出形式：`NL`、`STM_0`、`STM_k`、diagnostics ledger、scenario ledger、repair ledger。
- 方法内外边界：seed construction 在方法外，repair loop 在方法内。
- no-human-in-the-loop 限定：只限定 repair run 内。
- 模型范围：引用 [model_scope.md](./model_scope.md)，把 main / caveat / supplementary-stress / excluded 作为任务定义的一部分而不是实验后解释。
- Better STM 最小必要条件。

## 5. Method

- Artifact normalization into a machine-checkable executable representation。
- Diagnostics sources：parse / semantic / design / scenario feedback。
- Repair proposal generation。
- Regression checks、accept / reject / rollback。
- Failure logging：rejected repair、oscillation、non-convergence。
- Conversion attribution：原始种子、规范化 `STM_0`、修正后 `STM_k`。

## 6. Experimental Design

- 数据来源与 seed registry：R1/R2/R5.5 已形成 `llms-emp-stm-subset` 主 seed 方向；R5.6 已冻结 model scope；最终 eligibility 仍待 R5.7 / R7 冻结。
- Scope matrix：主结果只面向 T0 离散 FSM / HSM / EFSM-lite / 离散 UML-SysML statechart 子集；T0.5 timer-like cue 作 caveat；Digital Camera / T1-ish 作 supplementary stress。
- 四例预演与主实验样本区分。
- RQ1--RQ6。
- 指标与评价门：由 R4/R6/R8 冻结。
- 对照 / 消融：no-repair seed、regenerate-from-NL、no structured feedback、可运行 repair baseline、converter-aware analysis。

## 7. Results（后续主结果；当前只允许 pre-repair characterization）

R0/R5.5 不写 repair 结果，也不写 `STM_0 -> STM_k` 改善结论。R5.5 只能作为 `Pre-repair readiness characterization, not repair outcome`：具体 10 NL cluster、6 LLM 输出和 conversion status 均以 [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) 与 [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) 为 canonical source。R6/R8 后再填：缺陷类型分布、feedback source 覆盖、修正闭合 / 回归 / 拒绝 / 振荡 / 不收敛、`STM_0` vs `STM_k` 五条件台账、seed 来源影响、转换损失与归因。

## 8. Related Work

- LLM / NLP for model generation from requirements。
- State-machine / behavior model synthesis and repair。
- Model checking / simulation / executable modeling feedback。
- LLM self-refinement and agentic repair。
- 本文定位：不在 `NL -> STM` direct generation 上硬刚，而研究初始 artifact 之后的反馈驱动修正。

## 9. Threats and Limitations

- seed 来源偏差，尤其 `llms-emp` 60 pair 只是 10 个唯一 NL × 6 个模型输出，不是 60 个独立需求。
- 转换器信息损失，以及 conversion / normalization / lowering 不计 repair gain。
- T0/T0.5/T1 与 FSM/HSM/EFSM-lite/statechart 子集的范围限制；不能外推到 timed automata、hybrid automata、arbitrary UML 或 protocol FSM。
- LLM provider drift。
- 人工裁决一致性。
- 轻量诊断不等于完整形式化验证。
- 小样本预演与主实验边界。

## 10. Conclusion

只在证据闭合后写。核心应回到：反馈驱动修正任务、结构化 feedback 的作用、失败模式和后续可扩展方向。
