# R3.1 PlantUML pre-SCXML normalization / recovery 摘要

本文件由 `python -m paper_stm_repair_conversion.cli recover-plantuml` 生成。它是 R3.1 conversion eligibility 证据，不是 Better STM repair 实验结果。

## 核心结论

- PlantUML 一手 pair 总数：1049；unique NL：999。
- 原始 PlantUML 官方 SCXML 已可转换：550；原始失败：499。
- all-rules 技术通过：488；其中低风险通过：480；主 eligibility 纳入：480；高风险仅 supplementary：8。
- normalization 后仍失败：11。
- LLMS-EMP cross-LLM gate：通过；ratio=1.429。
- 临时 v2 probe 的 250/499 只是早期 prototype estimate；本文件中的 production report 已取代该估计，论文主 claim 只能使用 low-risk / main eligibility 口径。

## 按 seed 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `llms-emp-stm-subset` | 60 | 33 | 27 | 25 | 20 | 20 | 2 |
| `unified-uml-multimodal-validation` | 989 | 517 | 472 | 463 | 460 | 460 | 9 |

## 按 seed class 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `llms_emp_cross_llm` | 60 | 33 | 27 | 25 | 20 | 20 | 2 |
| `unified_synthetic` | 989 | 517 | 472 | 463 | 460 | 460 | 9 |

## 按错误类别统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `A_non_plantuml_stm_directive` | 24 | 0 | 24 | 22 | 19 | 19 | 2 |
| `B_entry_do_exit_action_syntax` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `D_activity_or_pseudostate_syntax_mixed_in_state_diagram` | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| `E_quoted_transition_state_names` | 191 | 0 | 191 | 191 | 191 | 191 | 0 |
| `F_unquoted_state_names_with_spaces` | 279 | 2 | 277 | 270 | 270 | 270 | 7 |
| `Y_other_or_contextual` | 550 | 548 | 2 | 0 | 0 | 0 | 2 |

## 按 LLM 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Claude` | 10 | 9 | 1 | 1 | 0 | 0 | 0 |
| `DeepSeek` | 10 | 1 | 9 | 9 | 9 | 9 | 0 |
| `GPT-4` | 10 | 9 | 1 | 1 | 1 | 1 | 0 |
| `GPT-4o` | 10 | 9 | 1 | 1 | 0 | 0 | 0 |
| `Kimi` | 10 | 5 | 5 | 4 | 2 | 2 | 1 |
| `Llama` | 10 | 0 | 10 | 9 | 8 | 8 | 1 |
| `NA` | 989 | 517 | 472 | 463 | 460 | 460 | 9 |

## LLMS-EMP eligible_after 组成

| LLM | raw | naturally converted | recovered main | high-risk supplementary | eligible after | failed after | rescue share |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Claude` | 10 | 9 | 0 | 1 | 9 | 0 | 0.0 |
| `DeepSeek` | 10 | 1 | 9 | 0 | 10 | 0 | 0.9 |
| `GPT-4` | 10 | 9 | 1 | 0 | 10 | 0 | 0.1 |
| `GPT-4o` | 10 | 9 | 0 | 1 | 9 | 0 | 0.0 |
| `Kimi` | 10 | 5 | 2 | 2 | 7 | 1 | 0.286 |
| `Llama` | 10 | 0 | 8 | 1 | 8 | 1 | 1.0 |

解释：该表只说明 LLMS-EMP 在 conversion eligibility 层面恢复到可谨慎 aggregate 的平衡；不同 LLM 的 eligible_after 由 naturally-converted 与 recovered-main 的比例不同，不能直接当作原始 STM 质量同分布证据。

## recovered vs naturally-converted profile

| subset | count | avg states | avg transitions | avg transition label chars | hierarchy counts | avg alias count |
|---|---:|---:|---:|---:|---|---:|
| `naturally_converted` | 550 | 7.89 | 10.23 | 9.22 | `{'hierarchical': 28, 'flat': 522}` | 0.0 |
| `main_recovered` | 480 | 7.26 | 8.66 | 6.71 | `{'hierarchical': 10, 'flat': 470}` | 4.77 |

解释：recovered subset 是 normalized eligibility subset，不是原始生成分布的无偏代表；若后续论文引用，必须保留该限制。

## 文件与证据

- JSON report: `plantuml_recovery_report.json`
- normalization ledger: `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/plantuml_normalization_ledger.jsonl`
- generator code commit: `90f9ff0b772cd9b5c1b942950c8dfeec3df56f6b`；该字段记录写出 report 前的 clean 代码提交，承载 report 的 artifact commit 可以是后续提交。
- generator worktree dirty: `False`
- canonical STM 不由 normalizer 直接生成；所有 recovered 判定均基于官方 PlantUML SCXML。
