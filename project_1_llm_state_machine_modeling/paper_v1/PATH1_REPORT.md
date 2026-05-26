# Path 1 — 硬刚路线决策报告（TODO 占位）

> **状态**：sprint 未开工。本文件作为 `dev/path1-hard-comparison` branch 的产出锚点占位，待 Phase 6 完成后由实验结果填充。
>
> **创建日期**：2026-05-26（v4.1 sprint 开工前）

## 接管入口

新 Claude / codex session 进入 `dev/path1-hard-comparison` branch 后，按以下顺序读：

1. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 路线规划与 §4.1 决策准则
2. [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md) — Path 1 接管指引（数据规则 / method 调用 / 评测协议 / report 字段定义）
3. `method/STATUS.md`（待 Phase 0 创建后）

## Sprint Phase 进度（待 Phase 0 开工后更新）

| Phase | 状态 | 备注 |
| --- | --- | --- |
| 0 — 脚手架 + pyfcstm + source .env + gpt_client | 未开工 | 必须先在 main 上稳定 |
| 1 — SpecExtractor / Modeler / Repair 三 Agent | 未开工 | 共同基础 |
| 2 — pyfcstm 三类 deterministic 反馈源 | 未开工 | 共同基础 |
| 3 — ex1 ExpertReviewAgent 接入 + 全链路 smoke | 未开工 | 共同基础 |
| **4 — 数据准备 + Path 1 quick experiment** | 未开工 | **本 branch 主任务** |
| 6 — 决策报告 + paper OUTLINE | 未开工 | 本文件最终内容由此环节产出 |
| 7 — 收口 + PR | 未开工 | 本 branch 提 PR 不合并，等用户综合决策 |

## 最终决策报告字段（占位，待 Phase 6 填充）

按 [PATH1_HARD_COMPARISON_GUIDE.md §8](./PATH1_HARD_COMPARISON_GUIDE.md) 产出要求：

1. **§1 实验配置**：T0 子集组成、LLM_MODEL 实际值、迭代轮数 N — TODO
2. **§2 主结果表**：A0_strong (structure_event Hybrid on GPT-5.5) vs A4_ours 的 7 类组件 P/R/F1 + overall-F1（aggregate TP/FP/FN，**不是 macro-F1** — 见 §6.2）— TODO
3. **§3 lift 分布**：每个 case 单独的 lift 数据 — TODO
4. **§4 信号判定**：按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S1/S2/S3/S4 归类 — TODO
5. **§5 confounders 列表**：API 失败 / 全轮 parse 失败 / token 截断的样本 — TODO
6. **§6 Claude 的方向建议 + rationale**：写明依据，**不下结论，最终方向由用户拍板** — TODO
7. **§7 后续 paper 工作量预估**：若选 Path 1，1-2 个月内补 llms_emp / ttool-ai / IEC 61499 等更强 baseline 对照 — TODO

## paper §1 contributions（method 为主，参考 [GUIDE §11.3](./PATH1_HARD_COMPARISON_GUIDE.md)）

| # | 类别 | contribution |
| --- | --- | --- |
| 1 | **method** | In-loop deterministic feedback via speculative validation |
| 2 | **method** | Language-independent expression IR enables symbolic reasoning without codegen |
| 3 | **method** | DSL-native aspect AOP + forced fault paths |
| 4 | **method** | Abstract action + read-only context for effector-agnostic STM synthesis |
| 5 | **evidence** | Empirical demonstration on structure_event_driven T0 subset over Hybrid baseline |
