# Google Gemini 系列模型完整表

> 本文件维护 Google Gemini 系列模型完整表。摘要结论见 [SUMMARY.md](./SUMMARY.md#6-gemini-当前重点模型)。Gemini 模型 lifecycle 与 pricing 变化较快，实验前必须按精确 model ID 重查 [Gemini API models](https://ai.google.dev/gemini-api/docs/models) 与 [pricing](https://ai.google.dev/gemini-api/docs/pricing)。

## 1. Gemini 系列完整表（按发布时间降序）

| 发布时间/排序键 | 模型/系列 | 状态 | context / max output | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2026-09-02 | Gemini 3.8 Flash | Gateway B native profile 可用；严格 schema/canary 仍有限制 | 1M / 64K | 2026-12-31 前 $0.75/$3.75；2027-01-01 起 $1.50/$7.50；本轮实测渠道未取得可核验价卡 | [model card](https://deepmind.google/models/model-cards/gemini-3-8-flash) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2026-08-13 | Gemini 3.7 Flash | Gateway B native profile 可用；method smoke 已通过；严格 schema/canary 仍有限制 | 1M / 64K | 本轮实测渠道未取得可核验价卡；不据此解释为免费 | [model card](https://deepmind.google/models/model-cards/gemini-3-7-flash/) / [models](https://ai.google.dev/gemini-api/docs/models) |
| 2026-05-19 | Gemini 3.5 Flash / Gemini 3.5 Nano Banana | Flash `gemini-3.5-flash` 本轮核验；现有网关接入未通 | Flash：1M / 64K；Nano Banana 另核，不共用规格 | Flash 标准输入 $1.50 / 输出 $9，cache $0.15，存储 $1/1M tokens/hour；2026-09-06 | [Flash card](https://deepmind.google/models/model-cards/gemini-3-5-flash/) / [models](https://ai.google.dev/gemini-api/docs/models) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2025-12-17 | Gemini 3 Flash | preview/较新线 | 1,048K / 65K 级 | 按 Gemini 3 pricing | [Gemini 3](https://ai.google.dev/gemini-api/docs/gemini-3) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2025-11-18 | Gemini 3 Pro | preview/较新线 | 1,048K / 65K 级 | 按 Gemini 3 pricing | [Gemini 3](https://ai.google.dev/gemini-api/docs/gemini-3) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2025-07-22 | Gemini 2.5 Flash-Lite | GA/低价长上下文 | 1,048K / 65K 级 | 按 current pricing | [models](https://ai.google.dev/gemini-api/docs/models) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2025-06-17 | Gemini 2.5 Pro / Flash | GA/常用线 | 1,048K / 65K 级 | Pro/Flash 按 current pricing | [models](https://ai.google.dev/gemini-api/docs/models) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2025-02 | Gemini 2.0 Flash / Flash-Lite | historical / lifecycle 风险 | 1M / 8K 级 | 旧 Vertex/Gemini 计价 | [lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2024-05 | Gemini 1.5 Pro / Flash | historical/retired 风险 | 1M-2M 级历史长上下文 | 旧 Vertex 计价 | [lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2024-02 | Gemini 1.0 Pro / Vision | retired/historical | 32K 时代 | 旧 Vertex 计价 | [lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
