# Path 2 — 差异化路线决策报告（TODO 占位）

> **状态**：sprint 未开工。本文件作为 `dev/path2-differentiation` branch 的产出锚点占位，待 Phase 6 完成后由实验结果填充。
>
> **创建日期**：2026-05-26（v4.1 sprint 开工前）

## 接管入口

新 Claude / codex session 进入 `dev/path2-differentiation` branch 后，按以下顺序读：

1. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 路线规划与 §4.1 决策准则
2. [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md) — Path 2 接管指引（数据规则 / method 调用 / 5 个 intrinsic 指标 / report 字段定义 / **§11.3.0 三段论 framing**）
3. `method/STATUS.md`（待 Phase 0 创建后）

## Sprint Phase 进度（待 Phase 0 开工后更新）

| Phase | 状态 | 备注 |
| --- | --- | --- |
| 0 — 脚手架 + pyfcstm + source .env + gpt_client | 未开工 | 必须先在 main 上稳定 |
| 1 — SpecExtractor / Modeler / Repair 三 Agent | 未开工 | 共同基础 |
| 2 — pyfcstm 三类 deterministic 反馈源 | 未开工 | 共同基础 |
| 3 — ex1 ExpertReviewAgent 接入 + 全链路 smoke | 未开工 | 共同基础 |
| **5 — Path 2 quick experiment (sources/ 20 条 intrinsic)** | 未开工 | **本 branch 主任务** |
| 6 — 决策报告 + paper OUTLINE | 未开工 | 本文件最终内容由此环节产出 |
| 7 — 收口 + PR | 未开工 | 本 branch 提 PR 不合并，等用户综合决策 |

## 最终决策报告字段（占位，待 Phase 6 填充）

按 [PATH2_DIFFERENTIATION_GUIDE.md §8](./PATH2_DIFFERENTIATION_GUIDE.md) 产出要求：

1. **§1 实验配置**：sources/ T0 子集组成（3 桶分布）、LLM_MODEL 实际值、迭代轮数 N — TODO
2. **§2 主结果表**：A0_baseline (single-prompt) vs A4_ours 的 5 个 intrinsic（ParseRate / SemValidRate / SimRate / ReachabilityRate / JudgeScore）+ 5-metric mean — TODO
3. **§3 lift 分布**：按 3 桶（FSM / EFSM / HSM）拆分 lift — TODO
4. **§4 每个样本 detail**：20 条样本各自的 intrinsic 5 维分数 — TODO
5. **§5 信号判定**：按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S1/S2/S3/S4 归类 — TODO
6. **§6 confounders 列表**：API 失败 / 全轮 parse 失败 / judge 评分异常的样本 — TODO
7. **§7 Claude 的方向建议 + rationale**：写明依据，**不下结论，最终方向由用户拍板** — TODO
8. **§8 后续 paper 工作量预估**：若选 Path 2，1-2 个月内补的工作（手工标 reference / 扩 sources/ / intrinsic-F1 Pearson calibration / cross-vendor） — TODO

## paper §1 contributions（method 为主 + 强化 pyfcstm → 控制系统价值论证，参考 [GUIDE §11.3 + §11.3.0](./PATH2_DIFFERENTIATION_GUIDE.md)）

| # | 类别 | contribution | 对应 pyfcstm feature | 控制系统场景价值 |
| --- | --- | --- | --- | --- |
| 1 | **method** | In-loop deterministic feedback via speculative validation | `SimulationRuntime` DFS validation + `SimulationRuntimeDfsError` | 多模式切换 dead-end 识别 |
| 2 | **method** | Language-independent expression IR enables symbolic reasoning | `Expr` IR + `solver/` Z3 集成 + 跨 9 语言渲染 | 复杂数值守卫 + Z3 可达性 + 跨部署目标 |
| 3 | **method** | DSL-native aspect AOP + forced fault paths | `>> during before/after` + `!` forced transition | per-tick invariant + 强制 fault-recovery escape |
| 4 | **method** | Abstract action + read-only context for effector-agnostic STM synthesis | `enter abstract` + `@abstract_handler` + `ReadOnlyExecutionContext` | 硬件解耦 + handler 反射注入 |
| 5 | **evidence + enabling** | 20-case industrial control system NL benchmark + reference-free intrinsic + judge protocol | — | sources/ 9 真实工业领域 |

## Path 2 核心 framing 论证（来自 [GUIDE §11.3.0](./PATH2_DIFFERENTIATION_GUIDE.md)）

**三段论**：pyfcstm feature → LLM agent loop 能力 → 控制系统场景价值

**为什么 baseline 工具链（Umple / PlantUML / Mermaid / TTool / IEC 61499 / SysML）在控制系统场景不胜任**：不是它们不能"画"控制系统 STM，而是它们不在 generation loop 中暴露控制系统建模需要的 4 类 grounding signal（dead-end check / SMT 可达性 / cross-cutting + forced escape / hardware decoupling）。pyfcstm 在 fully-automated DSL toolchain 之内把这 4 类 signal 全部做齐 — 这是 Path 2 paper 的真正立论基础。
