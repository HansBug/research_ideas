# R5 -> R6/R7：`llms-emp-stm-subset` 主实验 seed 交接

本文件把 R5 全量摸排后的方向性结论固定为后续阶段可执行的交接建议。完整 60 case 表和问题谱系见 [../seed_library_sweep/llms_emp_main_seed_analysis.md](../seed_library_sweep/llms_emp_main_seed_analysis.md)；机器事实源仍是 [../seed_library_sweep/sweep_report.json](../seed_library_sweep/sweep_report.json) 与 [../seed_library_sweep/archives/llms-emp-stm-subset_records.zip](../seed_library_sweep/archives/llms-emp-stm-subset_records.zip)。

## 1. 交接结论

`llms-emp-stm-subset` 是 R6/R7 的优先主池。它提供 60 个一手 `NL + LLM-generated PlantUML` pair，实际结构是 10 个唯一 NL × 6 个 LLM 输出。R5 中这 60 条的状态为：16 `converted`、41 `partial`、3 `blocked`。

## 2. 推荐 R6 首轮样本策略

R6 首轮目标是跑通真实 repair loop 和证据链，不是一次性覆盖全部 seed。建议选 12–18 条：

| 分层 | 建议数量 | 进入条件 | 用途 |
|---|---:|---|---|
| A-main | 4–6 | `converted`，loss_count=0，parse / inspect OK | 低转换噪声下验证 repair loop 基线 |
| B-main-with-caveat | 4–6 | `partial`，主要 caveat 是 condition/event/action 语义薄弱，且可由 NL 支撑修正目标 | 验证 feedback-driven repair 的核心价值 |
| C-analysis-only | 3–4 | hierarchy / cross-scope / normalization loss 较重 | 定性分析与 attribution；不轻易计入 repair gain |
| D-negative | 3 | `blocked_official_scxml_unavailable` | R8 negative evidence / converter follow-up |

首轮选样应覆盖至少 5 个唯一 NL、至少 4 个 LLM；同一 NL cluster 中不宜一次性选满 6 个输出，避免 clustered bias。

## 3. R7 必须冻结的规则

1. 以 10 个唯一 NL 为 cluster 做统计解释，60 个 pair 只作为 LLM-output-level 样本。
2. repair gain 只能从 pre-repair `.fcstm` 到 repaired `.fcstm` 计算。
3. reference `PlantUML` 与 checking 后结果不得作为 repair 输入。
4. `r3_1_normalization_replay`、HSM lowering、scope lifting、initial lowering 只能作 attribution，不能写成 repair improvement。
5. `condition_like_label_lowered_as_event` 只有在 NL 明确支持时才进入 guard/event repair target；否则只能作为表示 caveat。

## 4. 后置资源角色

| seed 源 | 后置角色 |
|---|---|
| `unified-uml-multimodal-validation` | stress / robustness / appendix，不作为主源 |
| `sefm-llm-state-machine` | qualitative / readable smoke case |
| `ttool-ai-smd-subset` | converter pressure / T0/SMD slicing follow-up |

## 5. 禁止主张

1. 不能声称 R5 已经执行真实 repair loop。
2. 不能声称 R5 已经生成 `STM_k`。
3. 不能把 57 条可导出 `.fcstm` 写成 repair 成功。
4. 不能把 60 条当成 60 个独立需求。
5. 不能把 conversion / normalization / lowering 的收益计入 repair gain。
