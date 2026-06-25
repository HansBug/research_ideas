# R3.1 PlantUML pre-SCXML normalization / recovery 摘要

本文件由 `python -m paper_stm_repair_conversion.cli recover-plantuml` 生成。它是 R3.1 conversion eligibility 证据，不是 Better STM repair 实验结果。

## 核心结论

- PlantUML 一手 pair 总数：1049；unique NL：999。
- 原始 PlantUML 官方 SCXML 已可转换：550；原始失败：499。
- all-rules 技术通过：476；其中低风险通过：468；主 eligibility 纳入：468；高风险仅 supplementary：8。
- normalization 后仍失败：23。
- LLMS-EMP cross-LLM gate：通过；ratio=1.429。
- 临时 v2 probe 的 250/499 只是早期 prototype estimate；本文件中的 production report 已取代该估计，论文主 claim 只能使用 low-risk / main eligibility 口径。
- source-level semantic preservation audit：审计 490 个 normalized candidates；通过 481；失败 9；低风险失败 0。

## 按 seed 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `llms-emp-stm-subset` | 60 | 33 | 27 | 24 | 19 | 19 | 3 |
| `unified-uml-multimodal-validation` | 989 | 517 | 472 | 452 | 449 | 449 | 20 |

## 按 seed class 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `llms_emp_cross_llm` | 60 | 33 | 27 | 24 | 19 | 19 | 3 |
| `unified_synthetic` | 989 | 517 | 472 | 452 | 449 | 449 | 20 |

## 按错误类别统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `A_non_plantuml_stm_directive` | 24 | 0 | 24 | 22 | 19 | 19 | 2 |
| `B_entry_do_exit_action_syntax` | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| `D_activity_or_pseudostate_syntax_mixed_in_state_diagram` | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| `E_quoted_transition_state_names` | 191 | 0 | 191 | 191 | 191 | 191 | 0 |
| `F_unquoted_state_names_with_spaces` | 270 | 1 | 269 | 258 | 258 | 258 | 11 |
| `Y_other_or_contextual` | 559 | 549 | 10 | 0 | 0 | 0 | 10 |

## 按 LLM 统计

| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Claude` | 10 | 9 | 1 | 1 | 0 | 0 | 0 |
| `DeepSeek` | 10 | 1 | 9 | 9 | 9 | 9 | 0 |
| `GPT-4` | 10 | 9 | 1 | 0 | 0 | 0 | 1 |
| `GPT-4o` | 10 | 9 | 1 | 1 | 0 | 0 | 0 |
| `Kimi` | 10 | 5 | 5 | 4 | 2 | 2 | 1 |
| `Llama` | 10 | 0 | 10 | 9 | 8 | 8 | 1 |
| `NA` | 989 | 517 | 472 | 452 | 449 | 449 | 20 |

## LLMS-EMP eligible_after 组成

| LLM | raw | naturally converted | recovered main | high-risk supplementary | eligible after | failed after | rescue share |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Claude` | 10 | 9 | 0 | 1 | 9 | 0 | 0.0 |
| `DeepSeek` | 10 | 1 | 9 | 0 | 10 | 0 | 0.9 |
| `GPT-4` | 10 | 9 | 0 | 0 | 9 | 1 | 0.0 |
| `GPT-4o` | 10 | 9 | 0 | 1 | 9 | 0 | 0.0 |
| `Kimi` | 10 | 5 | 2 | 2 | 7 | 1 | 0.286 |
| `Llama` | 10 | 0 | 8 | 1 | 8 | 1 | 1.0 |

解释：该表只说明 LLMS-EMP 在 conversion eligibility 层面恢复到可谨慎 aggregate 的平衡；不同 LLM 的 eligible_after 由 naturally-converted 与 recovered-main 的比例不同，不能直接当作原始 STM 质量同分布证据。

## recovered vs naturally-converted profile

| subset | count | avg states | avg transitions | avg transition label chars | hierarchy counts | avg alias count |
|---|---:|---:|---:|---:|---|---:|
| `naturally_converted` | 550 | 7.89 | 10.23 | 9.22 | `{'hierarchical': 28, 'flat': 522}` | 0.0 |
| `main_recovered` | 468 | 7.2 | 8.57 | 6.64 | `{'hierarchical': 9, 'flat': 459}` | 4.83 |

解释：recovered subset 是 normalized eligibility subset，不是原始生成分布的无偏代表；若后续论文引用，必须保留该限制。

## source-level semantic preservation audit

该审计逐项比较 raw PlantUML 与 normalized PlantUML 的状态声明、状态注释、迁移 source/target/label 与结构残留行；normalizer 新增的 alias declaration 会被反解回原始 label，非 PlantUML `stm` heading 与 normalizer comment 只作为语法修复痕迹忽略。它证明的是转换前规范化的 source-signature-preserving / 结构签名保持，不是定理级严格语义等价证明；任何低风险修复若未通过该审计，均不得进入主 eligibility。

| 指标 | 数量 |
|---|---:|
| audited_total | 490 |
| pass_total | 481 |
| fail_total | 9 |
| low_risk_fail_total | 0 |

| rule_id | audited | pass | fail |
|---|---:|---:|---:|
| `PUML.NORM.alias_multiword_endpoint` | 270 | 269 | 1 |
| `PUML.NORM.alias_quoted_endpoint` | 191 | 191 | 0 |
| `PUML.NORM.comment_dependency_arrow` | 3 | 0 | 3 |
| `PUML.NORM.comment_orphan_when` | 1 | 0 | 1 |
| `PUML.NORM.entry_do_exit_rewrite_or_loss` | 2 | 0 | 2 |
| `PUML.NORM.fork_join_decl_to_state` | 1 | 0 | 1 |
| `PUML.NORM.remove_stm_heading` | 22 | 21 | 1 |
| `PUML.NORM.stm_block_to_state` | 2 | 0 | 2 |

## 文件与证据

- JSON report: `plantuml_recovery_report.json`
- normalization ledger: `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/plantuml_normalization_ledger.jsonl`
- generator code commit: `0d0271505f2a3fbc11ab2654a0ea5d7d6a4da5f8`；该字段记录写出 report 前的 clean 代码提交，承载 report 的 artifact commit 可以是后续提交。
- generator worktree dirty: `False`
- canonical STM 不由 normalizer 直接生成；所有 recovered 判定均基于官方 PlantUML SCXML。
- full workdir archive: `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip`；report 中 `raw_candidate_path` / `normalized_candidate_path` / `structured_export_path` 对应 zip 内 member 路径。
