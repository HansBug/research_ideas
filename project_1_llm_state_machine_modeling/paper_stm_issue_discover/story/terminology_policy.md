# 术语政策

| 术语 | 本文含义 | 不应混同为 |
| --- | --- | --- |
| 作者 PlantUML | 被评模型的作者源，用于问题定位 | compiler 生成的 FCSTM 或 inspection facts |
| canonical source IR | 作者源的规范化表示与可追溯中间表示 | 新的规范义务来源 |
| FCSTM / native facts | 可执行闭包和确定性检查所需的模型、投影与事实 | 作者模型本身或 ledger answer |
| finding / report | 方法产生并发布的具体问题主张 | expected issue 或 Judge decision |
| expected issue | ledger 中预先存在的被评测条目 | 方法输出的 L 标签 |
| FULL / PARTIAL / NONE | Judge 给出的 report-to-expected relation | report validity 或 W 等级 |
| VALID_KNOWN / VALID_NOVEL / INVALID | Judge 的 report validity | expected relation；INVALID 进入 I/invalid-output 统计，ordinary FP 只是其中一类 |
| invalid report disposition | 被 source-first 评为 INVALID 的用户可见 report 记录；v60/current 为 291/1271 | 291 个独立领域缺陷或 291 条 ordinary false positive |
| report-level validity precision | `(K reports + N reports) / all reports`；current `980/1271 = 77.10%`，baseline `417/512 = 81.45%` | 无 projection 的反事实精度或跨输出粒度不变的语义精度 |
| D0 non-violation | source fact 成立但没有 surviving violated obligation；current I 为 120 | ordinary source-level false positive 或 conversion error |
| NADC (`NOT_A_DEFECT_CLAIM`) | A0 下报告未成立为作者模型缺陷的 disposition；current 为 118，其中 confirmed method-owned mechanisms 110、indeterminate 8 | 单一 lowering 根因或 baseline 中可直接比较的同构类别 |
| confirmed method-owned invalid | compiler-owned artifact、projection/trace boundary、runtime/evidence closure 和 confirmed lowering 类别的合计；current 为 110/291 | 包含 attribution-indeterminate 的 NADC 总量 118 |
| conversion-lowering confirmed | 同时有 source absence/semantic mismatch 与具体 lowering/loss/ownership 证据的 invalid attribution；v60 为 0 | 看到 FCSTM、loss code、identity-only trace 或 unsupported receipt |
| NO_RERUN | deny-by-default gate 的唯一当前结论；A/B/C 未同时满足时保留 v60 headline | “建议重跑”“可能重跑”或 conversion cost 的豁免 |
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
