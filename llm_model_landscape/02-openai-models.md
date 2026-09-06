# OpenAI / GPT 系列模型完整表

> 本文件维护 OpenAI GPT / reasoning / Codex 相关模型的完整表。摘要结论见 [SUMMARY.md](./SUMMARY.md#4-openai-gpt-当前重点模型)。价格默认为 USD / 1M tokens；以 OpenAI 官方 [models](https://developers.openai.com/api/docs/models) 与 [pricing](https://developers.openai.com/api/docs/pricing) 页面为准。

## 1. OpenAI / GPT 系列完整表（按发布时间降序）

| 发布时间/排序键 | 模型/系列 | 状态 | context / max output | 输入 / cached / 输出价 | 来源 |
|---:|---|---|---:|---:|---|
| 2026-07-09 | `gpt-5.6-luna` | 高吞吐、低价 GPT-5.6；2026-09-06 核验 | 1,050,000 / 128,000；max input 922,000 | 0.20 / 0.02 / 1.20；cache write 0.25；输入 >272K：0.40 / 0.04 / 1.80，write 0.50 | [model](https://developers.openai.com/api/docs/models/gpt-5.6-luna) / [pricing](https://developers.openai.com/api/docs/pricing) / [changelog](https://developers.openai.com/api/docs/changelog) |
| 2026-04-23 | `gpt-5.5` | 当前 GPT 强线 | 1,050K / 128K | 5 / 0.5 / 30；长上下文价另列 | [model](https://developers.openai.com/api/docs/models/gpt-5.5) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-03-17 | `gpt-5.4-mini` | 低价 GPT-5.4 线 | 400K / 128K | 0.75 / 0.075 / 4.5 | [model](https://developers.openai.com/api/docs/models/gpt-5.4-mini) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-03-05 | `gpt-5.4` | GPT-5.4 线 | 1,050K / 128K | 2.5 / 0.25 / 15；长上下文价另列 | [model](https://developers.openai.com/api/docs/models/gpt-5.4) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-02-05 | `gpt-5.3-codex` | Codex 专项 | 400K / 128K | 1.75 / 0.175 / 14 | [model](https://developers.openai.com/api/docs/models/gpt-5.3-codex) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-11-13 | `gpt-5.1` | GPT-5.1 线 | 400K / 128K | 1.25 / 0.125 / 10 | [model](https://developers.openai.com/api/docs/models/gpt-5.1) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-08 | GPT-5 / GPT-5-mini / GPT-5-nano | GPT-5 历史线 | 400K / 128K | GPT-5 1.25/0.125/10；mini/nano 更低 | [models](https://developers.openai.com/api/docs/models) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-04-16 | o3 / o4-mini | reasoning 线 | 200K / 100K | o3 2/0.5/8；o4-mini 1.1/0.275/4.4 | [models](https://developers.openai.com/api/docs/models) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-04-14 | GPT-4.1 / GPT-4.1-mini / GPT-4.1-nano | 长上下文 GPT-4.1 线 | 1,047K / 32K | GPT-4.1 2/0.5/8；mini/nano 更低 | [models](https://developers.openai.com/api/docs/models) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2024-07-18 | GPT-4o mini | baseline 高频低价历史线 | 128K / 16K | 0.15 / 0.075 / 0.6 | [model](https://developers.openai.com/api/docs/models/gpt-4o-mini) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2024-05-13 | GPT-4o | baseline 高频历史线 | 128K / 16K | 2.5 / 1.25 / 10 | [model](https://developers.openai.com/api/docs/models/gpt-4o) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2023-03 | GPT-4 / GPT-4 Turbo / GPT-3.5 Turbo | legacy/historical | 8K-128K 历史线 | legacy 价；不建议新 baseline | [models](https://developers.openai.com/api/docs/models) / [deprecations](https://developers.openai.com/api/docs/deprecations) |
| 2022 | text-davinci / code-davinci / older Codex | retired/historical | 历史小上下文 | retired；仅相关工作背景 | [deprecations](https://developers.openai.com/api/docs/deprecations) |
