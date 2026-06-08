# Qwen 系列模型完整表

> 本文件维护 Qwen hosted API 与开放权重模型的完整表。摘要结论见 [SUMMARY.md](./SUMMARY.md#8-qwen-当前重点模型)。

## 1. Qwen 系列专项表（按发布时间降序）

本轮核验结论：Hugging Face `Qwen` 官方 org 中未找到 `Qwen3.7` 开放权重模型；但 Qwen Cloud 侧已有 `qwen3.7-max` 与 `qwen3.7-plus` hosted API。因此实验记录要区分“开放权重 Qwen”与“Qwen 官方 hosted API”。

| 发布时间/排序键 | 系列 | 代表模型 | context / max output | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2026-06-01 | Qwen3.7 hosted | `qwen3.7-plus` | 1M；Max Input 991.80K；Max Output 65.53K | list 0.4/0.08 cache/1.6；页面有折扣价 | [Plus](https://www.qwencloud.com/models/qwen3.7-plus) |
| 2026-05-21 | Qwen3.7 hosted | `qwen3.7-max` | 1M；Max Input 991.80K；Max Output 65.53K | list 2.5/0.5 cache/7.5；页面有折扣价 | [Max](https://www.qwencloud.com/models/qwen3.7-max) |
| 2026-04-23 | Qwen3.6 | Qwen3.6-35B-A3B / 27B | 262,144 原生、可扩 1,010,000 | 开放权重无统一 token 价；API 另计 | [HF 35B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) / [HF 27B](https://huggingface.co/Qwen/Qwen3.6-27B) |
| 2026-02-15 | Qwen3.5 | Qwen3.5-397B-A17B / 122B-A10B / 35B-A3B / 27B | 多数 262,144 原生、可扩 1,010,000；hosted 1M | 开放权重无统一 token 价；API 另计 | [HF 397B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) / [HF 35B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B) |
| 2025-07-22 | Qwen3-Coder | Qwen3-Coder-480B-A35B / 30B-A3B / Next | 262,144 原生；材料称可扩到 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen3-coder/) / [HF 480B](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct) |
| 2025-04-29 | Qwen3 | Qwen3-235B-A22B / 30B-A3B | 32,768 原生；YaRN 到 131,072；部分后续线到 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen3/) / [HF 235B](https://huggingface.co/Qwen/Qwen3-235B-A22B) |
| 2025-01-26 | Qwen2.5-1M | Qwen2.5-14B/7B-Instruct-1M | up to 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen2.5-1m/) |
| 2024-09-19 | Qwen2.5 | Qwen2.5-72B-Instruct | 131,072 / 8,192 | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen2.5/) / [HF](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) |
