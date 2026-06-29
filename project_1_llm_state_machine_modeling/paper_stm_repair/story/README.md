# story/ — 论文主线、任务边界与写作栅栏

本目录负责回答：第一篇论文到底讲什么、边界在哪里、哪些话能写、哪些话不能写。它不是最终论文正文，也不是实验事实真源；它把 `reports/`、`pipeline/`、`corpora/`、`experiment_design/` 中已冻结的证据，以及待冻结的证据门 / claim gate，转化为后续 R5.6/R5.7/R7 可继承的 paper story contract。

## 1. 当前一句话主线

给定控制系统自然语言需求 `NL` 与初始状态机 `STM_0`，本文研究是否可以通过无人化、结构化反馈驱动的检查、诊断、场景、仿真与修正循环，得到相对于同一个 `STM_0` 更可检查、更可执行、更语义一致的候选状态机 `STM_k`。

当前主线仍是 **`<NL, STM_0> -> STM_k` 的反馈驱动状态机修正**，不是一次性 `NL -> STM` 生成论文，也不是 `fcstm` / `pyfcstm` / DSL 论文。

## 2. 文件清单与阅读顺序

| 顺序 | 文件 | 读它是为了什么 | 不能把它当成什么 |
|---:|---|---|---|
| 1 | [paper_story.md](./paper_story.md) | 读 thesis、gap、method insight、贡献草案、当前证据状态和 reviewer risk。 | 不是最终 Introduction；不能把草案 claim 当实验证明。 |
| 2 | [task_boundary.md](./task_boundary.md) | 冻结 `<NL, STM_0> -> STM_k` 输入输出、方法内外、人类角色、停止/拒绝/回滚、conversion attribution。 | 不是最终 eligibility policy；R5.6/R5.7 仍需进一步冻结。 |
| 3 | [terminology_policy.md](./terminology_policy.md) | 冻结推荐术语、`fcstm` 弱化策略、禁止表达和自检 grep。 | 不是英文最终措辞；写作时仍需按目标 venue 调整。 |
| 4 | [claim_evidence_map.md](./claim_evidence_map.md) | 把可写 claim 映射到证据门、后续 PR 和安全降级写法。 | 不是 claim 已成立的证明。 |
| 5 | [paper_outline.md](./paper_outline.md) | 维护 R0/R5.5 之后的论文结构草案和后续填数入口。 | 不是最终 manuscript。 |

## 3. 与其他路径的边界

| 需要什么 | 先读哪里 | story 中的角色 |
|---|---|---|
| 当前研究状态和关键数字 | [../STATUS.md](../STATUS.md) | story 只引用，不复写完整总账。 |
| R5/R5.5 人类结论报告 | [../reports/SUMMARY.md](../reports/SUMMARY.md) | story 用其支撑边界和风险，不把 readiness 结果写成 repair 结果。 |
| 机器事实源 / JSONL / deterministic audit | [../pipeline/README.md](../pipeline/README.md) | story 只引用 machine source，不复制 row-level facts。 |
| 一手 seed / registry | [../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md) | story 用作 seed source 背景，不直接定义 eligibility。 |
| Better STM / scope / eligibility / protocols / metrics | [../experiment_design/README.md](../experiment_design/README.md) | story 不覆盖 experiment design 真源。 |
| 旧 R1 证据和历史检索 | [../evidence/README.md](../evidence/README.md)、[../archive/README.md](../archive/README.md) | 只作 provenance / negative evidence 背景。 |

## 4. 当前证据状态

| 主题 | 当前状态 | 证据入口 | 写作约束 |
|---|---|---|---|
| 主 seed 方向 | `llms-emp-stm-subset` 是当前优先主 seed 池，含 10 个唯一 NL × 6 个 LLM 输出。 | [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | 只能写 seed readiness / profile，不得写 repair loop 效果。 |
| 转换状态 | R5.5 画像中 60 pair / 10 cluster / 16 converted / 41 partial / 3 blocked。 | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | 转换成功率不是修正成功率。 |
| model scope handoff | T0 主线、T0.5 timer-like caveat、Digital Camera supplementary stress、blocked negative evidence 需要 R5.6 冻结。 | [../reports/2026-06-28-22-54-39-model-scope-handoff.md](../reports/2026-06-28-22-54-39-model-scope-handoff.md) | story 可预埋边界，但最终 scope 真源应在 `experiment_design/scope/`。 |
| Better STM | 定义已迁到 experiment design。 | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | 没有真实 `STM_0` vs `STM_k` 前，不得声称 Better STM 主结果。 |
| repair loop | 尚未真实运行。 | [../STATUS.md](../STATUS.md) | 不得写已经产生 `STM_k` 或证明 improvement。 |

## 5. 硬约束

1. 不把第一篇写成 `NL -> STM` 生成论文。
2. 不把 `fcstm` / `pyfcstm` / DSL 写成论文主贡献。
3. 不声称完整形式化验证、sound model checking 或 correctness guarantee。
4. 不把转换器、人工规范化或 seed construction 收益计入 repair-loop 贡献。
5. 不把失败、回滚、振荡、不收敛从结果中消失。
6. 不把 R5/R5.5 readiness / profile 数字写成 R6/R7 repair-loop 结果。

## 6. 后续维护纪律

1. R5.6 若冻结 model scope，必须同步更新 [task_boundary.md](./task_boundary.md)、[paper_story.md](./paper_story.md)、[claim_evidence_map.md](./claim_evidence_map.md) 和 [paper_outline.md](./paper_outline.md)。
2. R5.7 若冻结 eligibility，必须把可写 claim 的证据门从“计划”更新为具体文件路径。
3. R6/R8 若真实 repair loop 结果有限或失败，必须优先降级 story，而不是强行解释成成功。
4. 新增 story 文件必须从本 README 登记，并说明它与现有文件的边界。
