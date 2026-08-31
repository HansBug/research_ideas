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
| predicate execution usage | registry 中产生至少一条 terminal receipt 的 distinct predicate-ID 覆盖；v60 为 12/19 | candidate 数、W2 finding 数、report-bound binding rows 或 W2-on-hits |
| report-bound predicate IDs | 至少绑定到一条最终 report-bound finding 的 distinct predicate-ID presence；v60 为 8/19 | terminal receipt 总数、W2 数、legacy `semantic_hit` marker 或缺陷类型覆盖 |
| report-bound binding ratio | 绑定记录行数 / 全部 report；v60 为 825/1271 | distinct predicate-ID usage 或 8/19 |
| legacy semantic-hit marker ratio | 绑定记录中继承 `coverage_class=semantic_hit` 的行数 / 绑定记录；v60 为 303/825 | terminal-false receipt、W2 或 8 个谓词的贡献数 |
| Semantic Judge | 独立执行 issue #195 两阶段协议的判定器 | 方法 discovery、predicate backend 或 evaluator |

`v60/current` 是当前冻结方法臂，`X1v2 baseline` 是当前比较臂，不是方法迭代代次。`v46`、`v27-stream` 与 `v26` 是历史里程碑，只能在明确的 historical/provenance 语境中出现。

逐条属性/输入审计与详细谓词能力审计属于内部 evaluation-only 材料，不是 paper1 主叙事。paper1 只描述谓词作为可复核证据后端，不把内部审计映射写成方法输入或完整覆盖承诺。
