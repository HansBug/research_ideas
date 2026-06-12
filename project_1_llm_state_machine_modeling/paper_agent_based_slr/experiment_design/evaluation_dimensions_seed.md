# Evaluation Dimensions Seed：A0 评价维度种子

## 1. 边界

本文件只冻结 A0 阶段的评价维度种子和后续 A5 接口，不冻结指标公式、阈值、统计协议或最终脚本。若某段需要精确公式，应移到 PR-A5。

## 2. 维度种子

| 维度 | A0 定义 | 后续可能证据 | A5 接口 |
|---|---|---|---|
| Traceability / 可追踪性 | 报告级 claim 能否回溯到 search、screening、extraction、coding、evidence locator 和 audit status。 | claim-to-source chain、断链记录。 | A5 冻结断链率、定位错误率。 |
| Factuality / 事实准确性 | metadata、venue、DOI、抽取字段、证据定位是否与来源一致。 | gold / silver facts、人工核验样本。 | A5 冻结字段级准确率和错误分类。 |
| Hallucination / unsupported claim | 不存在论文、错误来源、无证据 claim、过度综合。 | trap papers、unsupported claim log。 | A5 冻结 hallucination taxonomy、拦截率、残余错误。 |
| Screening consistency | 纳排决策与理由在重复运行 / 人工抽检 / 多 agent 下是否稳定。 | screening ledger、分歧裁决。 | A5 冻结 agreement / adjudication 统计。 |
| Extraction / coding consistency | 抽取字段和编码标签是否稳定、可解释、可裁决。 | extraction table、coding decision、uncertain 标记。 | A5 冻结字段级/标签级一致性。 |
| Transparency / 透明报告 | 是否能生成 PRISMA-style flow、排除理由、协议偏离日志。 | report artifacts、exclusion ledger。 | A5 冻结透明报告 checklist。 |
| Coverage proxy | known-item recall、seed recovery、database overlap 等覆盖代理。 | seed set、database result overlap。 | A5 冻结 proxy 计算口径。 |
| Cost / efficiency | agent 时间、token / API cost、人工审计时间、失败重试成本。 | run record、usage、人工审计日志。 | A5 冻结成本统计口径。 |
| Audit effectiveness | human audit gates 拦截了多少错误，留下多少残余问题。 | audit log、false positive、false negative。 | A5 冻结拦截率、误报率、残余 unsupported claim 率。 |

## 3. A0 不做的事

- 不把上述维度写成已运行结果。
- 不冻结公式或阈值。
- 不比较人类最终 SLR 与 agent 输出谁更好。
- 禁止声称 complete coverage。
- 禁止声称 PRISMA-compliant。

## 4. A3 / A5 接力要求

| 后续 PR | 需要接走的内容 |
|---|---|
| A3 | 把维度映射到具体 replay / prospective scenarios、gold / silver facts、trap papers 和 audit subset。 |
| A4 | 让 workflow 写出这些维度需要的 run record / evidence package 字段。 |
| A5 | 冻结指标公式、阈值、统计协议、失败分类和报告格式。 |
