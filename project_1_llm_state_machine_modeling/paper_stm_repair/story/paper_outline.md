# paper outline draft（R0 草案）

## 0. 说明

本文件只冻结第一篇论文的大纲方向和写作约束，不写最终正文。后续 PR-R7 必须根据 R1--R6 的真实证据重写或降级。

## 1. Abstract

- 背景：控制系统需求到状态机 artifact 后，实际使用需要可检查、可执行、可修正。
- 问题：一次性生成模型往往留下语义、guard/action、行为场景和可执行性缺陷。
- 方法：给定 `<NL, STM_0>`，使用 diagnostics、scenario feedback、repair 和 regression checks 构成无人化修正循环。
- 结果：只在 R6 后填写真实结果；若无充分证据，不写强提升。
- 限制：报告失败、回滚、振荡、转换损失和人工裁决边界。

## 2. Introduction

1. 控制系统状态机建模的现实需求：不仅要生成图，还要可机检、可执行、可复核。
2. 旧 `NL -> STM` 生成路线的局限：初始 artifact 质量不稳，且后续缺少闭环修正。
3. 新任务定义：`<NL, STM_0> -> STM_k / Better STM`。
4. 方法直觉：结构化 diagnostics + scenario feedback + accept/reject/rollback。
5. 贡献列表：任务定义、修正协议、Better STM 操作化、seed / converter / baseline 重排、实证评价。
6. 明确非贡献：不主张新 DSL，不主张完整形式化验证，不主张首个 `NL -> STM`。

## 3. Background and Motivation

- 状态机 artifact 的描述性与可执行性差异。
- 轻量语义增强对 diagnostics / simulation / repair feedback 的必要性。
- seed 来源：prior artifact、弱 prompt、旧模型、学生或人工建模。
- Motivating example：后续由 R2/R4 提供，不在 R0 构造。

## 4. Task Definition

- 输入输出形式：`NL`、`STM_0`、`STM_k`、diagnostics ledger、scenario ledger、repair ledger。
- 方法内外边界：seed construction 在方法外，repair loop 在方法内。
- no-human-in-the-loop 限定：只限定 repair run 内。
- Better STM 最小必要条件。

## 5. Method

- Artifact normalization into a machine-checkable executable representation。
- Diagnostics sources：parse / semantic / design / scenario feedback。
- Repair proposal generation。
- Regression checks、accept / reject / rollback。
- Failure logging：rejected repair、oscillation、non-convergence。
- Conversion attribution：原始种子、规范化 `STM_0`、修正后 `STM_k`。

## 6. Experimental Design

- 数据来源与 seed registry：由 R1/R2 冻结。
- 四例预演与主实验样本区分。
- RQ1--RQ6。
- 指标与评价门：由 R4/R6 冻结。
- 对照 / 消融：no-repair seed、regenerate-from-NL、no structured feedback、可运行 repair baseline、converter-aware analysis。

## 7. Results

R0 不写结果。R6 后再填：缺陷类型分布、feedback source 覆盖、修正闭合 / 回归 / 拒绝 / 振荡 / 不收敛、`STM_0` vs `STM_k` 五条件台账、seed 来源影响、转换损失与归因。

## 8. Related Work

- LLM / NLP for model generation from requirements。
- State-machine / behavior model synthesis and repair。
- Model checking / simulation / executable modeling feedback。
- LLM self-refinement and agentic repair。
- 本文定位：不在 `NL -> STM` direct generation 上硬刚，而研究初始 artifact 之后的反馈驱动修正。

## 9. Threats and Limitations

- seed 来源偏差。
- 转换器信息损失。
- LLM provider drift。
- 人工裁决一致性。
- 轻量诊断不等于完整形式化验证。
- 小样本预演与主实验边界。

## 10. Conclusion

只在证据闭合后写。核心应回到：反馈驱动修正任务、结构化 feedback 的作用、失败模式和后续可扩展方向。
