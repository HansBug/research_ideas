# 主张、证据与边界映射

| claim ID | strongest defensible wording | 证据 | 不能推出 |
| --- | --- | --- | --- |
| CLM-PROBLEM | 本文研究 free-form NL 与分析中固定、带来源归属 STM 的定位问题发现。 | [paper story](./paper_story.md)、[scope](./model_scope.md)、[Wang 上游数据入口](../corpora/seed_library/llms-emp-stm-subset/assets/README.md)、[54-pair 范围规则](../selected_seed_examples/README.md)。 | 模型由人创作、本文生成/修复输入模型，或已实现所有 STM languages。 |
| CLM-NOVELTY | 本文提出并评估一个面向状态机的工作流：它比较 free-form NL 与分析期间保持不变、具有来源归属的既有 STM，并返回定位发现。 | [closest-work matrix](../related_work/closest_work_matrix.md) 的四字段协议、MCeT 全文和 IET 风险处置。 | “未发现先前工作”、scoped `first`、LLM/SMT/model checking/traceability/replay/人工 relation adjudication 首创，或 universal first/only；IET 四字段全文裁定未闭合时不写这些优先权主张。 |
| CLM-C1 | C1 提供保留来源的 executable working representation 与 deterministic inspect augmentation。 | FCSTM adapter/projection implementation、native projection audit、方法原则。 | 全语言语义保持或 C1 的独立 causal gain。 |
| CLM-C2 | C2 将适用候选连接到 literature-informed typed obligations 与 source-bound FCSTM-backend-native replay receipts。 | [19 条 predicate audit](../related_work/provenance/predicate_provenance.md)、registry、receipts。 | 19 条是完备 taxonomy，W2 自动为有效发现，或所有 W2 都是无界证明。 |
| CLM-RQ1 | current 在本案例研究的 FULL discovery coverage 高于 baseline，同时报告级 precision 低 `4.34 pp`。 | `combined_summary_v4.json`、[result inventory](./paper_result_inventory.md)。 | 跨语言、总体显著性或 C1/C2 因果效应。 |
| CLM-RQ2 | current FULL hits 中最高 W 为 `0/113/197`，12/19 predicate IDs 有 terminal receipt，8/19 有 report binding；`825/1271` 报告绑定行为附录诊断。 | canonical fair-comparison summary；current reaudit report decisions。 | candidate-level typed-plan closure、replay 成功率、极性比例、适用候选覆盖率、defect coverage、边际贡献或 baseline 等价零值。 |
| CLM-RQ3 | current 的 I boundary 与 cost eligibility 可审计；current `$7.18277320` 完整，baseline `$0.22523328` 不完整。 | attribution and cost audits。 | baseline 成本倍率、生产率或 deployment outcome。 |
