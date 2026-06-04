# DeepSeek 系列模型完整表

> 本文件维护 DeepSeek hosted API 与开放权重模型完整表。摘要结论见 [SUMMARY.md](./SUMMARY.md#7-deepseek-当前重点模型)。Hosted API 价格以 [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/) 为准；开放权重无统一 token 价。

## 1. DeepSeek 系列完整表（按发布时间降序）

| 发布时间/排序键 | 模型/系列 | 类型/状态 | context / max output | 官方价格/计价 | 来源 |
|---:|---|---|---:|---|---|
| 2026-04-24 | DeepSeek V4-Pro | hosted API 高质量线 | 1M / 384K | cache hit 0.003625；miss 0.435；output 0.87 | [release](https://api-docs.deepseek.com/news/news260424) / [pricing](https://api-docs.deepseek.com/quick_start/pricing/) |
| 2026-04-24 | DeepSeek V4-Flash | hosted API 性价比线 | 1M / 384K | cache hit 0.0028；miss 0.14；output 0.28 | [release](https://api-docs.deepseek.com/news/news260424) / [pricing](https://api-docs.deepseek.com/quick_start/pricing/) |
| 2026-04-24 | `deepseek-chat` / `deepseek-reasoner` | compatibility aliases | 1M / 384K | 同 V4-Flash；有退役/别名风险 | [first call](https://api-docs.deepseek.com/) / [updates](https://api-docs.deepseek.com/updates/) |
| 2025-09-29 | DeepSeek-V3.2-Exp | open-weight / experimental | 128K-1M 级，按 checkpoint | 开放权重无统一 token 价 | [news](https://api-docs.deepseek.com/news/news250929) |
| 2025-08-21 | DeepSeek-V3.1 | open-weight / hosted 历史线 | 128K 级 | 按 checkpoint / hosted 当前页 | [news](https://api-docs.deepseek.com/news/news250821) |
| 2025-05-28 | DeepSeek-R1-0528 | reasoning open-weight 更新 | 64K-128K 级 | 开放权重无统一 token 价 | [news](https://api-docs.deepseek.com/news/news250528) |
| 2025-03-25 | DeepSeek-V3-0324 | V3 更新线 | 128K 级 | 开放权重无统一 token 价 | [news](https://api-docs.deepseek.com/news/news250325) |
| 2025-01-20 | DeepSeek-R1 | reasoning baseline | 64K-128K 级 | 开放权重无统一 token 价；legacy hosted 另计 | [R1 release](https://api-docs.deepseek.com/news/news250120) |
| 2024-12 | DeepSeek-V3 | open-weight chat baseline | 128K 级 | 开放权重无统一 token 价 | [GitHub](https://github.com/deepseek-ai/DeepSeek-V3) |
| 2024-07 | DeepSeek-Coder-V2 | code baseline | 128K 级 | 开放权重无统一 token 价 | [GitHub](https://github.com/deepseek-ai/DeepSeek-Coder-V2) |
| 2024-05 | DeepSeek-V2 | historical open-weight | 128K 级 | 开放权重无统一 token 价 | [GitHub](https://github.com/deepseek-ai/DeepSeek-V2) |
