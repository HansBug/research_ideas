# paper story：从一次性生成转向反馈驱动状态机修正

## 0. 来源与当前性

| 字段 | 值 |
|---|---|
| 原始来源 | R0 `paper_story.md`，后在 R5 简化时折叠进 [README.md](./README.md) |
| 本轮恢复目的 | 恢复独立 paper story 入口，避免 thesis / gap / contribution 藏在 README 中 |
| 当前证据入口 | [model_scope.md](./model_scope.md)、[../STATUS.md](../STATUS.md)、[../reports/SUMMARY.md](../reports/SUMMARY.md)、[../pipeline/README.md](../pipeline/README.md)、[../experiment_design/README.md](../experiment_design/README.md) |
| 证据边界 | 当前仅有 seed readiness、conversion/profile/evaluation gate；尚无真实 repair-loop 主结果 |

## 1. 一句话 thesis

给定控制系统自然语言需求 `NL` 与初始状态机 `STM_0`，本文研究一个无人化、结构化反馈驱动的状态机修正任务：系统在诊断、场景反馈、候选修正、回归检查、接受 / 拒绝 / 回滚循环中，尝试得到相对于同一个 `STM_0` 更可检查、更可执行、更语义一致的候选状态机 `STM_k`，并完整记录成功、失败、回滚、振荡和不收敛。

安全英文骨架：

```text
We study feedback-driven repair of an initial state-machine artifact conditioned on natural-language requirements, rather than one-shot state-machine generation from text.
```

## 2. 背景判断：为什么不是 `NL -> STM` 生成论文

直接从自然语言生成状态机已经是拥挤方向。若继续主打 `NL -> STM`，论文会被拉回 prompt、模型选择、direct baseline 公平性和生成质量硬对比，而不容易突出本项目真正积累起来的 diagnostics、simulation、repair feedback 和 run audit 能力。

真实使用场景中，已有或可构造的初始状态机往往不是完全不可用，而是存在结构、语义、guard / action、行为场景或可执行性缺陷。一个更稳的研究问题是：**给定 `NL` 与 `STM_0`，系统能否自动发现缺陷、提出修正、检查回归、接受或回滚候选，从而得到更好的 `STM_k`。**

## 3. 核心 gap

> 本节是 story-level positioning hypothesis，用于指导 R7 related work 绑定；不能在没有文献引用和证据门的情况下直接搬入 Introduction / Related Work。

| 既有工作常见能力 | 本文关注的缺口 |
|---|---|
| 生成 state-machine-like / UML / SysML / behavior artifacts。 | 生成后 artifact 是否可机检、可执行、可诊断、可修正通常没有形成闭环。 |
| 使用 prompt 或 agent 分阶段生成模型。 | 结构化 feedback 是否能稳定减少缺陷、避免回归、记录失败模式仍需实证。 |
| 使用自然语言或示例辅助建模。 | 初始模型与需求之间的 semantic drift、guard / action 错误、场景行为缺陷需要可审计修复协议。 |
| 一次性人工审查或工具检查。 | 缺少 `diagnose -> repair -> regression -> accept / rollback` 的无人化循环与归因台账。 |

## 4. 方法洞察

本文的关键不是提出一个新 DSL，也不是换更强模型重新生成状态机，而是把初始状态机规范化为可机检、可执行的状态机制品，使系统可以自动产生结构化反馈，并将反馈纳入修正循环：

```text
<NL, STM_i> -> diagnostics / scenario feedback -> candidate repair -> regression checks -> accept / reject / rollback -> STM_{i+1}
```

该循环必须记录 rejected repair、oscillation、non-convergence、semantic drift 和 converter attribution，不能只报告成功样例。

## 5. 当前证据状态如何支撑 story

| 证据层 | 当前已有 | 对 story 的作用 | 禁止过度解释 |
|---|---|---|---|
| seed registry | R5.5 snapshot：`llms-emp-stm-subset` 为一手 `<NL, LLM-generated STM_0>` 主 seed 池候选；canonical source 见 [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。 | 支撑“可围绕同一 NL 多模型初始制品做比较”的实验机会。 | 不等于主实验已完成。 |
| readiness / conversion | R5.5 snapshot：conversion status 见 [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) 与 main seed profile report。 | 暴露真实 seed 的转换压力和缺陷谱系。 | 不能把 converted 数字写成 repair success。 |
| R5.6 model scope | [model_scope.md](./model_scope.md) 冻结主线为 T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集；EFSM-lite 只是当前无独立样例的候选范围上限；T0.5 只作 caveat，Digital Camera / T1-ish 只作 supplementary stress。 | 支撑后续 R5.7/R6/R7 在明确模型边界内定义 taxonomy、protocol 和 eligibility。 | 不外推到 timed automata、hybrid automata、arbitrary UML 或 protocol FSM；不把 EFSM-lite 写成已有独立数据覆盖。 |
| selected smoke | 四例静态 `<NL, STM_0, fcstm>` smoke 输入。 | 支撑工程链路冒烟，不是最终实验集合。 | 不能把四例当主结论。 |
| evaluation gate | Better STM checklist / human rubric schema / dry-run examples。 | 支撑后续 repair-loop 评价设计。 | 目前不是结果裁决。 |
| negative evidence | blocked / partial / conversion attribution。 | 支撑 honest limitations 和 scope 决策。 | 不能隐藏 blocked / partial。 |

## 6. 贡献草案（仍需 R6/R7 证据闭合）

| 贡献草案 | 当前证据状态 | 后续证据门 |
|---|---|---|
| 定义 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | story / task boundary 已恢复，R5.5 提供主 seed 池画像；R5.6 已在 [model_scope.md](./model_scope.md) 冻结 model scope / claim boundary。 | R5.7 冻结 repair target taxonomy；R7 写作时不可扩大为 `NL -> STM` 或 timed / arbitrary UML repair。 |
| 提出无人化 repair run 协议：诊断、场景反馈、候选修正、回归检查、接受 / 拒绝 / 回滚。 | 当前仅定义边界与评价门；真实 loop 尚未运行。 | R6/R8 必须有真实 repair ledger、回归、拒绝/回滚证据。 |
| 操作化 Better STM，区分转换规范化收益与修正循环收益。 | Better STM 定义已迁入 `experiment_design/quality_model/`。 | 需要同一 `STM_0` 下的 before/after 诊断、场景和裁决。 |
| 将 prior artifact 重排为 seed source、converter pressure、error taxonomy 和有限对照。 | seed registry、reports、conversion profile 已有。 | R5.7 eligibility 和 R6/R7 对照矩阵仍需冻结。 |

## 7. Claims to make / be careful / avoid

### 7.1 可以谨慎写的 claim

- We frame / study feedback-driven repair of initial state-machine artifacts conditioned on NL requirements.
- We build an auditable pipeline that separates seed construction, normalization/conversion, and repair-loop effects.
- The R5/R5.5 seed audit reveals nontrivial conversion and modeling defects that motivate a repair-oriented protocol.

### 7.2 必须降级的 claim

- “结构化反馈能提升状态机质量”只能在 R6/R8 有真实数据后写；当前只能写 “is designed to support / will be evaluated through”。
- “Better STM” 当前是评价目标和定义，不是已经证明的结果。
- “无人化”只限定 repair run 内，benchmark design、reference adjudication 和 post-hoc audit 可有人类参与。

### 7.3 禁止 claim

1. 不写“首个 / 最强 `NL -> STM` 方法”。
2. 不写“提出新 DSL / fcstm 是核心贡献”。
3. 不写“完整形式化验证 / model checking 保证正确”。
4. 不写“自动修正一定提升质量”或“outperform all baselines”。
5. 不写“baseline 已经无须比较”。
6. 不把 run record、日志或复现工程本身写成论文方法贡献。

## 8. 当前未闭合风险

| 风险 | 需要后续 PR 闭合 |
|---|---|
| T0 主线、T0.5 timer-like caveat 与 T1/supplementary model scope 已在 R5.6 冻结，但 R5.7 仍需把这些边界转成 repair target taxonomy 和 eligibility 前置条件。 | R5.7 taxonomy / R7 eligibility |
| 哪些 pair / cluster 可进入主实验仍需资格冻结。 | R5.7 eligibility / protocol |
| 修正循环是否稳定有效尚未实证。 | R6/R8 真实 repair loop |
| Better STM 是否成立尚无主结果。 | 真实 `STM_0` vs `STM_k`、场景、诊断与人工/结构化裁决 |
| 转换和修正贡献容易混淆。 | 三阶段归因：原始制品 -> 规范化 `STM_0` -> `STM_k` |

## 9. R0 story 的可迭代性说明

R0 的稳定部分是导师定调后的研究对象和边界：第一篇论文应围绕反馈驱动状态机修正，而不是一次性 `NL -> STM` 生成。可调整部分是证据强度、样本纳入、对照方式和最终写作力度。

后续 PR 的实证结果具有回填和校准权：若 R5.6/R5.7/R6/R8 发现某类 seed 无法可靠转换、某类诊断反馈效果有限、或某个 RQ 证据不足，应优先更新 [claim_evidence_map.md](./claim_evidence_map.md)、[paper_outline.md](./paper_outline.md) 和本文件，而不是为了维护早期草案强行解释实验结果。
