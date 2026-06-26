# 评价维度种子：S0-v2 智能体式 SLR 支持方法

## 1. 边界

本文件只冻结 PR-S0-v2 阶段的评价维度种子和后续 A5 接口，不冻结指标公式、阈值、统计协议或最终脚本。若某段需要精确公式，应移到 PR-A5。

S0-v2 后，评价中心从“工作流能否生成证据制品 / 报告”进一步收紧为：**研究者定义的 meta-model、可演化 dimension schema、字段级 content evidence、统计观察、candidate finding signals、researcher challenge / final adjudication、以及 process evidence 是否可审计、可复核、可降级、可评价**。

## 2. 维度种子

| 维度 | PR-S0-v2 定义 | 后续可能证据 | A5 接口 | 证据类型 |
|---|---|---|---|---|
| Review meta-model adequacy | topic / RQ / scope / meta-model 是否足以约束后续 dimension schema 与 finding heuristics。 | 研究者批准记录、scope 排除理由、seed-paper stress test。 | A5 冻结 meta-model 审计表。 | process evidence + 设计审计 |
| Dimension pattern stability / evolution | schema 是否随新论文、新类别和抽取失败有版本化修订；修订是否有触发原因、影响范围和冻结理由。 | schema version、change trigger、accepted/rejected/merged changes。 | A5 冻结 schema 演化统计与稳定条件。 | process evidence |
| Backfill completeness / cost | schema 变化后是否识别受影响论文并完成或显式豁免回填。 | impacted papers、backfill required/status、回填时间。 | A5 冻结 backfill completion / burden 统计。 | process evidence + content evidence |
| Field-level evidence accuracy | 字段值是否有可定位 source anchor，且 anchor 与字段语义一致。 | page/section/quote/table/artifact URL、人工核验样本、missing/uncertainty。 | A5 冻结 source-anchor 准确性、断链率、字段错误分类。 | content evidence |
| Missing / uncertainty handling | 缺失字段、不适用字段和证据不足是否被区分，而不是被 agent 猜测补齐。 | missing reason、not-applicable、uncertain、requires-review 标签。 | A5 冻结缺失/不确定性审计规则。 | content evidence |
| Statistical analysis correctness | 频次、分布、交叉表、趋势、coverage proxy 是否基于正确字段版本和纳入样本计算。 | analysis protocol、field-table version、统计脚本/表格、抽样复核。 | A5 冻结统计正确性检查与版本一致性检查。 | content evidence + analysis artifact |
| Candidate finding usefulness | candidate finding signal 是否相关、非平凡、可审计，并能引出有效 challenge。 | candidate ledger、finding type、support/counter evidence draft、人工评分。 | A5 冻结相关性、非平凡性、可操作性评分规程。 | content evidence + process evidence |
| Candidate-to-final transition quality | candidate 是否经过 challenge、counter-evidence、补证、降级、拒绝或 unresolved 裁决。 | accepted/downgraded/rejected/unresolved rate、challenge log。 | A5 冻结转移状态机与结果统计。 | process evidence + content evidence |
| Content/process evidence separation | target-domain findings 是否只由 content evidence 支撑，method-evaluation findings 是否只使用 process evidence。 | claim-evidence map、finding 类型标签、证据来源类型。 | A5 冻结跨证据类型误用检查。 | content evidence / process evidence 分层 |
| Transparency package completeness | 是否输出 claim-evidence map、排除理由、schema revision、audit log、类 PRISMA flow 与 limitation。 | transparency package 文件、检查清单、第三方复核。 | A5 冻结透明材料 completeness checklist。 | mixed artifact |
| Researcher challenge burden | 研究者质疑所需时间、交互轮次、阅读负担、补证请求和裁决成本。 | time log、interaction turns、manual edits、rejected suggestions。 | A5 冻结人机协同成本统计。 | process evidence |
| Pilot closure / feasibility | pilot 是否跑通 L0--L7，是否产出所有必要制品并暴露阻塞点。 | pilot run record、artifact completeness、blocked stages。 | A5 冻结 pilot closure gate；不得评价泛化。 | process evidence + artifact audit |
| Multi-user process metrics | 多名学生/研究者使用时的理解难点、schema 分歧、challenge 行为和失败模式。 | anonymized logs、consent/redaction report、inter-user variation。 | A5 冻结 process-data protocol 与伦理边界。 | process evidence |
| Cost / efficiency | token/API、运行时间、人工审计时间、backfill、失败重试和脱敏成本。 | run record、usage、time log、redaction report。 | A5 冻结成本统计口径；不预设正收益。 | process evidence |
| Coverage proxy | 种子论文恢复、已知条目召回、数据库重叠等覆盖代理。 | seed set、query log、screening ledger。 | A5 冻结 coverage proxy 计算；不得写完整覆盖。 | content/search artifact |

## 3. Target-domain 与 method-evaluation 的分工

| Finding 类型 | 支撑证据 | 可评价内容 | 禁止误用 |
|---|---|---|---|
| Target-domain research finding | 目标论文 content evidence、统计观察、counter-evidence、研究者裁决 | 字段证据准确性、统计正确性、主张强度、反例处理 | 不能用 process logs 或学生交互日志支撑。 |
| Method-evaluation finding | process evidence、pilot artifacts、interaction logs、cost、redaction report | 可用性、审计性、成本、失败模式、人机协同负担 | 不能当作目标领域文献结论。 |

## 4. PR-S0-v2 不做的事

- 不把上述维度写成已运行结果。
- 不冻结公式、阈值或统计显著性检验。
- 不比较“agent 是否优于人类完成完整 SLR”。
- 不声称质疑闭环必然提高质量。
- 不把 statistical observations 写成 final research findings。
- 不把 process evidence 用于 target-domain findings。
- 不声称完整覆盖或 PRISMA 合规。

## 5. A3 / A5 接力要求

| 后续 PR | 需要接走的内容 |
|---|---|
| A2 | 把 meta-model、dimension schema、evidence object、schema revision/backfill、candidate finding ledger、challenge/adjudication 和 process boundary 写成阶段契约。 |
| A3 | 把维度映射到具体 pilot / replay / prospective 场景、gold/silver facts、陷阱论文、审计子集和 finding 类型任务。 |
| A4 | 让工作流写出这些维度需要的 run record、evidence table、schema revision log、candidate finding ledger 和 transparency package。 |
| A5 | 冻结指标公式、阈值、统计协议、失败分类、伦理/脱敏政策和报告格式。 |
| A6 | 把评价维度映射到论文 RQ、实验表格、limitations 和 related-work positioning，不把计划中的评价义务写成结果。 |
