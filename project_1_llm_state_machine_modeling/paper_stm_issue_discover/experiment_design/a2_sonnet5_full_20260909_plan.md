# A2 Sonnet-5 全量复核计划（2026-09-09）

2026-09-10 范围澄清：下文“配套引导”仅指当前 `no-predicates` 实际关闭的谓词词汇、路由、参数绑定和执行专属探针等；不包含仍保留的需求义务、普通 grounding、检查事实和语义评估。不是全部上游机制的消融。完整结果与可比性限制见[全量报告](../reports/2026-09-10-a2-sonnet5-full-results.md)。

本轮固定评估整个谓词机制及其配套引导与 backend 的联合消融。method 使用 `claude-sonnet-5`、`no-predicates`、54 个冻结 pair、3 个 round 和 16 workers；输入、prompt、run contract、source commit 与 A2 protocol 保持同一正式 run。provider failure 只允许在原格内恢复，失败 receipt 必须保留并记录，不能从分母静默删除。

method 的准入条件是 162 个 pair-round cell 全部具有真实、结构化且通过 schema 的 eligible receipt。达到该条件后，Judge 对同一 162 个 method cell 全量运行，不使用 15-pair 子集或单 round 代理结果。

Judge 固定为 `gpt-5.6-luna`、8 workers、validity readings=2、validity arbitration、`relation_first`、`full` closure；每个 round 使用完整 54-pair 集合。Judge 输出保留输入 manifest、included/excluded 及排除原因、prompt、raw output、usage、失败/恢复审计，并按 round、pair 和总体计算 reports、K/N/I、precision、strict precision、FULL hit。

比较对象为同一 Sonnet-5 条件下的 full ours 与 baseline（E2 已冻结结果），以及 A2 no-predicates。A2 结果用于检验“谓词及其配套机制是否降低幻觉并提升 report precision”的联合效应；若差异不显著，只报告估计值、区间与机制证据，不把无差异改写成等效或因果证明。

## 验收

- method：54 pairs、3 rounds、162 cells、162 eligible，失败格保留恢复记录。
- judge：每个 round 恰好 54 pair 输入；总计 162 个 pair-round，所有 eligible method cell 均纳入。
- 指标：reports、K/N/I、precision、strict precision、FULL hit，分别给出 round、pair、总体层级。
- 证据：run manifest、输入 hash、模型配置、raw receipt、usage、错误/重试、恢复记录和最终报告均写入独立 run 目录。
