# Evaluation Dimensions Seed：PR-S0 评价维度种子

## 1. 边界

本文件只冻结 PR-S0 阶段的评价维度种子和后续 A5 接口，不冻结指标公式、阈值、统计协议或最终脚本。若某段需要精确公式，应移到 PR-A5。

PR-S0 后，评价中心从“workflow 是否能生成证据包 / 报告”收紧为：**researcher-defined meta-model、finding patterns、candidate findings、evidence chain、researcher challenge loop 与 final finding decision 是否可审计、可复核、可降级**。

## 2. 维度种子

| 维度 | PR-S0 定义 | 后续可能证据 | A5 接口 |
|---|---|---|---|
| Meta-model / schema usefulness | researcher-instantiated meta-model 是否帮助结构化抽取、编码和 finding proposal。 | schema coverage、字段缺失、researcher approval log。 | A5 冻结 schema coverage 与实例化质量评估。 |
| Finding relevance / usefulness | candidate finding 是否与 researcher 的 RQ 和领域问题相关、有研究意义、非平凡且可审计。 | domain researcher rating、finding type coverage、非平凡性评分。 | A5 冻结 finding-level 人工评价 rubric。 |
| Traceability / 可追踪性 | candidate / final finding 能否回溯到 search、screening、extraction、coding、evidence locator 和 audit status。 | finding-to-source chain、断链记录。 | A5 冻结断链率、定位错误率。 |
| Factuality / 事实准确性 | metadata、venue、DOI、抽取字段、证据定位是否与来源一致。 | gold / silver facts、人工核验样本。 | A5 冻结字段级准确率和错误分类。 |
| Hallucination / unsupported finding | 不存在论文、错误来源、无证据 finding、过度综合、scope 过宽。 | trap papers、unsupported finding log、overclaim taxonomy。 | A5 冻结 hallucination / overclaim taxonomy、拦截率、残余错误。 |
| Screening consistency | 纳排决策与理由在重复运行 / 人工抽检 / 多 agent 下是否稳定。 | screening ledger、分歧裁决。 | A5 冻结 agreement / adjudication 统计。 |
| Extraction / coding consistency | 抽取字段和编码标签是否稳定、可解释、可裁决。 | extraction table、coding decision、uncertain 标记。 | A5 冻结字段级/标签级一致性。 |
| Challenge effectiveness | researcher challenge 是否导致补证、找反例、修订、降级、unresolved 或接受。 | challenge log、revision / downgrade / unresolved / accepted count。 | A5 冻结 challenge outcome 和 stop-condition 统计。 |
| Transparency / 透明报告 | 是否能生成 PRISMA-style flow、排除理由、协议偏离日志和 finding status ledger。 | report artifacts、exclusion ledger、challenge/revision ledger。 | A5 冻结透明报告 checklist；不得写 PRISMA-compliant。 |
| Coverage proxy | known-item recall、seed recovery、database overlap 等覆盖代理。 | seed set、database result overlap。 | A5 冻结 proxy 计算口径；不得写 complete coverage。 |
| Cost / efficiency | agent 时间、token / API cost、人工审计时间、challenge 修订成本、失败重试成本。 | run record、usage、人工审计日志。 | A5 冻结成本统计口径。 |
| Audit effectiveness | human audit / researcher challenge gates 拦截了多少错误，留下多少残余问题。 | audit log、false positive、false negative。 | A5 冻结拦截率、误报率、残余 unsupported finding 率。 |

## 3. PR-S0 不做的事

- 不把上述维度写成已运行结果。
- 不冻结公式或阈值。
- 不比较人类最终 SLR 与 agent 输出谁更好。
- 不声称 challenge loop 必然提高 quality。
- 不把 candidate finding 写成 final finding。
- 禁止声称 complete coverage。
- 禁止声称 PRISMA-compliant。

## 4. A3 / A5 接力要求

| 后续 PR | 需要接走的内容 |
|---|---|
| A2 | 把 meta-model、executable schema、candidate finding、challenge log 和 finding status 写成 stage contract。 |
| A3 | 把维度映射到具体 replay / prospective scenarios、gold / silver facts、trap papers、audit subset 和 finding-type tasks。 |
| A4 | 让 workflow 写出这些维度需要的 run record / finding-centered evidence package 字段。 |
| A5 | 冻结指标公式、阈值、统计协议、失败分类和报告格式。 |
| A6 | 把评价维度映射到论文 RQ、实验表格和 limitations，不把 planned obligation 写成结果。 |
