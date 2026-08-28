# 术语政策

| 术语 | 本文含义 | 不应混同为 |
| --- | --- | --- |
| 作者 PlantUML | 被评模型的作者源，用于问题定位 | compiler 生成的 FCSTM 或 inspection facts |
| canonical source IR | 作者源的规范化表示与可追溯中间表示 | 新的规范义务来源 |
| FCSTM / native facts | 可执行闭包和确定性检查所需的模型、投影与事实 | 作者模型本身或 ledger answer |
| finding / report | 方法产生并发布的具体问题主张 | expected issue 或 Judge decision |
| expected issue | ledger 中预先存在的被评测条目 | 方法输出的 L 标签 |
| FULL / PARTIAL / NONE | Judge 给出的 report-to-expected relation | report validity 或 W 等级 |
| VALID_KNOWN / VALID_NOVEL / INVALID | Judge 的 report validity | expected relation；仅 INVALID 进入 semantic FP |
| W0 / W1 / W2 | 方法 finding 的见证强度 | predicate usage 或 Judge 的有效性裁定 |
| D0 / D1 / D2 | 方法内问题裁定；D1/D2 才发布 | ledger 的 L0/L1/L2 |
| L0 / L1 / L2 | ledger 对陈述问题所需分析层级的分类 | 方法输出或 W/D 等级 |
| predicate usage | 指定计划集合中获得 terminal receipt 的谓词覆盖 | candidate 数、W2 finding 数或 W2-on-hits |
| Semantic Judge | 独立执行 issue #195 两阶段协议的判定器 | 方法 discovery、predicate backend 或 evaluator |

`v60/current` 是当前冻结方法臂，`X1v2 baseline` 是当前比较臂，不是方法迭代代次。`v46`、`v27-stream` 与 `v26` 是历史里程碑，只能在明确的 historical/provenance 语境中出现。
