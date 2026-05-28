# Path 1 — 硬刚路线决策报告

> **状态**：Phase 4a（数据选样）✅ 完成。Phase 4b（reference IR 手工标注 + run_path1.py 实验）进行中。Phase 6 由实验结果填充本文件主体。
>
> **创建日期**：2026-05-26（v4.1 sprint 开工前）
>
> **更新**：2026-05-27 数据选样收口（323 sample × codex 自动评审 + 后处理 bd_final 分布修正）

## 接管入口

新 Claude / codex session 进入 `dev/path1-hard-comparison` branch 后，按以下顺序读：

1. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 路线规划与 §4.1 决策准则
2. [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md) — Path 1 接管指引（数据规则 / method 调用 / 评测协议 / report 字段定义）
3. [selection/README.md](./selection/README.md) — 数据选样工作区接管入口（断点续 / retry / aggregate 流程）
4. [selection/SELECTION_REPORT.md](./selection/SELECTION_REPORT.md) — 候选 15 + 备选 15 选样最终报告（含 emoji 表格 + rationale）
5. `../method/STATUS.md` — 共同基础进度

## Sprint Phase 进度

| Phase | 状态 | 备注 |
| --- | --- | --- |
| 0 — 脚手架 + pyfcstm + source .env + gpt_client | ✅ 完成 | PR #11 已 merge 到 main |
| 1 — SpecExtractor / Modeler / Repair 三 Agent | ✅ 完成 | PR #11 |
| 2 — pyfcstm 三类 deterministic 反馈源 | ✅ 完成 | PR #11 (parse + sem + sim with scenariogen) |
| 3 — eval/ 评测基础设施（双 LLM 初审 + 人类签字） | ✅ 完成 | PR #11 (`eval/PROTOCOL.md` + 67 row 演习跑通) |
| **4a — sources/ T0+🟢 候选选样** | ✅ **完成** | **见 [selection/SELECTION_REPORT.md](./selection/SELECTION_REPORT.md) — 323 sample × codex (gpt-5.5) 全文阅读评审 + post-hoc bd_final 后处理；候选 15 + 备选 15 落定** |
| 4b — reference IR 手工标注 + run_path1.py 实验 | 🔁 待开工 | 把候选 15 落到 `eval/data/sources_path1.parquet` + 手工写 ref_components.json + 跑 A0_strong / A_full_ours |
| 5 — 双 LLM annotator 评审 + 人类签字 | 待 4b | |
| 6 — 决策报告 + paper OUTLINE | 待 5 | 本文件最终内容由此环节产出 |
| 7 — 收口 + PR | 本 branch 提 PR 不合并，等用户综合决策 | |

## Phase 4a 数据选样收口（2026-05-27）

**核心方法学**：选样准则 = stress-test on baseline-documented-weakest components，方法独立（只引 Apvrille 2025 §IV-C 报告的 baseline F1 数字 actions=0.34 / guards=0.42 / hierarchical=~0.5），不引用 fcstm 任何能力，防 reviewer 攻 cherry-pick。

**评分维度（6 维 × 0-3 分）**：

- **H** Hierarchical / composite states — baseline hierarchical F1 弱区
- **G** Guarded arithmetic — baseline guards F1=0.23-0.42
- **A** Non-trivial actions — baseline actions F1=0.00-0.34（最弱列）
- **F** Fault recovery / global escape
- **bd** Baseline-trap density — 基于 6 类 trap 信号（T1 cross-section / T2 implicit-domain / T3 implicit-action-prose / T4 multivar-guard / T5 composite-internal / T6 global-cross-cutting），后处理只用 T2/T4/T5/T6（NL 内容信号），T1/T3（NL 结构信号）codex 过度 flag 不入 bd 公式
- **ft** pyfcstm primitive 独占优势强度 — C1 speculative-DFS / C2 Expr-IR / C3 forced-aspect / C4 abstract-action

**最终分布**（n=323）：

| 维度 | ⚪ 0 | 🟡 1 | 🟢 2 | 💎 3 |
|---|---:|---:|---:|---:|
| H | 51% | 22% | 9% | 18% |
| G | 3% | 6% | 28% | 63% |
| A | 0% | 0% | 38% | 62% |
| F | 38% | 17% | 25% | 19% |
| **bd_final** (T2/T4/T5/T6) | 12% | 39% | 21% | 28% |
| **ft** | 7% | 27% | 33% | 33% |

bd_final 后处理修复了 codex raw bd 的 73% 顶格饱和（→ 28%，平滑梯度）；ft 完美分布无饱和。

**候选 Top-15 领域分布**：✈️×3（UAV/航天）/ ⚙️×4（通用机器人）/ 🏭×2 / 🌡️×2 / 🩺×1 / 🅿️×1 / 🚆×1 / 🚗×1 — 跨 8 个领域分散，无单一行业垄断。

**Backup-15** 含长时旋翼 UAS / DARPA Urban Challenge Odin / Mars helicopter hybrid autonomy / multilayer safety FSM 等深 HSM 案例，方向定后正式 paper 阶段扩样备用。

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
