# Paper Outline（R0 草案）

> 本文件只冻结论文结构和写作约束，不写最终正文，不引入结果数字。

## 1. Introduction

目标：用最短路径解释为什么从 `NL -> STM` 生成转向 `<NL, STM_0> -> STM_k` 修正。

应包含：

1. 控制系统状态机建模需要可检查、可执行、可修正的制品，而不只是描述性图。
2. 已有工作已经覆盖多种 `NL -> STM` 或邻近行为模型生成路线，因此本文不主张“首个生成”。
3. 实际瓶颈转向初始模型之后：如何发现缺陷、给出反馈、自动修正、避免回归并记录失败。
4. 本文研究 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。
5. Contributions 只写任务定义、修正协议、评价协议和证据框架；不写结果型提升 claim。

## 2. Background and Motivation

应覆盖：

1. 状态机模型的基本组成：states、transitions、events、guards、actions、variables、hierarchy。
2. 为什么描述性状态机不足以支撑 diagnostics / simulation / repair feedback。
3. `STM_0` 的来源：prior artifacts、弱 prompt、旧模型、学生 / 人工种子。
4. 失败模式示例：解析错误、guard/action 偏差、不可达状态、场景不匹配、过修、振荡。

## 3. Task Definition

对应 [task_boundary.md](./task_boundary.md) 与 [better_stm_definition.md](../experiment_design/better_stm_definition.md)。

应包含：

1. 输入：`NL` 与 `STM_0`。
2. 输出：`STM_k` 或 rejected / rollback / non-converged outcome。
3. no human-in-the-loop 仅限定 repair run 内部。
4. `Better(STM_k, STM_0 | NL, S, D, R)` 的最小判定框架。
5. 转换归因台账：原始种子、转换后 `STM_0`、修正后 `STM_k`。

## 4. Method

建议结构：

1. **Artifact intake and normalization**：记录来源、格式、转换风险；不主张通用转换器。
2. **Diagnostics and feedback construction**：parse / semantic / design / scenario diagnostics。
3. **Repair proposal generation**：基于结构化反馈产生候选修复。
4. **Acceptance, rejection, and rollback**：用冻结评价门处理候选。
5. **Failure-mode logging**：拒绝、回滚、振荡和不收敛作为结果对象。

写作约束：不要把 run record、工程模块拆分或 `fcstm` 工具名写成方法贡献。

## 5. Experimental Protocol

R0 只规划，R4/R6 冻结。

应包含：

1. seed 来源分层：prior artifact、弱 prompt、旧模型、学生 / 人工种子。
2. 同一组四例预演样本在 R3--R6 复用的原则。
3. 对照 / 消融：无修正种子、从 NL 重新生成、无结构化反馈自修正、可运行近似修正基线、转换感知分析。
4. metrics / gates：五条件、诊断计数、场景通过率、人工裁决、拒绝 / 回滚 / 振荡。
5. eligibility：schema invalid、partial run、provider failure 与人工补写必须进入排除或局限。

## 6. Results

R0 不写结果。后续 R6/R7 才能填写：

1. 初始缺陷分布。
2. 反馈来源覆盖。
3. 修正闭合、拒绝、回滚和不收敛。
4. `STM_0` vs `STM_k` 五条件台账。
5. 对照 / 消融和 seed 来源分析。

## 7. Related Work

应按角色组织，而不是把所有工作都写成被击败 baseline：

1. Natural-language to state-machine / behavior-model generation。
2. Formal / executable modeling and diagnostics。
3. Model repair, refinement, trace / oracle-guided synthesis。
4. LLM-based modeling with feedback, tool constraints, or agentic workflows。
5. State-machine artifact formats and executable representations。

写作约束：先承认 close works 的能力，再定位本文的 `<NL, STM_0> -> repair` task、可执行反馈和评价协议差异。

## 8. Threats to Validity

必须包含：

1. seed 来源偏差。
2. converter 信息损失。
3. 人工裁决主观性。
4. scenario suite 覆盖不足。
5. LLM provider drift。
6. baseline fairness 与不可运行 prior work。
7. `Better STM` 不等于 fully correct STM。

## 9. Limitations and Conclusion

应明确：

1. 不保证完整正确性或完整形式化验证。
2. 不声称通用多格式转换器。
3. 不把 `fcstm` / DSL 作为独立贡献。
4. 失败、回滚和不收敛是方法边界的一部分。
