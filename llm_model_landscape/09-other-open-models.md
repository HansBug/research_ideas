# 其他常见开放权重/开源模型完整表

> 本文件维护 OpenAI gpt-oss、Kimi/Moonshot、Mistral、Gemma、Granite、Nemotron、Phi、GLM、InternLM、Baichuan、Yi、Falcon、GPT-J/GPT-Neo、CogVLM 等其他常见模型系列。摘要结论见 [SUMMARY.md](./SUMMARY.md#11-其他常见模型当前重点系列)。

## 1. 其他开源/开放权重与 baseline 高频系列（按发布时间降序）

> 若“发布时间/排序键”只写年份，表示本轮仅核验到年份级官方/模型卡证据；同年内部不表达严格发布时间先后，暂按 `proj1` baseline 相关性与当前研究关注度排序，后续维护应优先补精确 release 日期。

| 发布时间/排序键 | 系列 | 代表/最新可获取线 | context 概况 | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2026 | OpenAI gpt-oss | gpt-oss-120b / gpt-oss-20b | 按模型卡；开放权重/开源权重线 | 开放权重无统一 token 价；第三方托管另计 | [HF 120B](https://huggingface.co/openai/gpt-oss-120b) |
| 2026 | Kimi/Moonshot | Kimi-K2-Instruct / Kimi-K2-Thinking | 按模型卡/官方页 | 开放权重与 hosted API 需分开记录 | [Kimi K2](https://moonshotai.github.io/Kimi-K2/) / [HF K2 Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) / [HF K2 Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) |
| 2026 | NVIDIA Nemotron | Nemotron-3 Nano/Super 等 | 4K-1M，按 checkpoint | NIM/云托管按当前页 | [Nemotron](https://developer.nvidia.com/nemotron) / [Build](https://build.nvidia.com/nvidia) |
| 2026 | GLM/ChatGLM | GLM-4.7 / GLM-5 | 128K-200K/1M 版本并存 | Z.AI/BigModel API 另计 | [BigModel docs](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.7) / [pricing](https://docs.z.ai/guides/overview/pricing) |
| 2026 | DeepSeek open weights | V4 / V3.2 / R1 updates | 128K-1M 级，按 checkpoint | 开权重无统一价；hosted 见 V4 表 | [V4 release](https://api-docs.deepseek.com/news/news260424) / [V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3) / [R1](https://api-docs.deepseek.com/news/news250120) |
| 2026 | Mistral/Mixtral/Codestral | Large/Small/Magistral/Codestral 新线 | 128K-256K，按模型 | Mistral API 按当前页 | [models](https://docs.mistral.ai/models) / [pricing](https://docs.mistral.ai/platform/pricing/) |
| 2025 | Gemma | Gemma3 | 128K 级 | 开放权重无统一价；Vertex/AI Studio 另计 | [Gemma](https://ai.google.dev/gemma) / [HF Google](https://huggingface.co/google) |
| 2025 | Microsoft Phi | Phi-4/Phi-4-mini/multimodal | 16K-131K，按型号 | Azure AI Foundry / open weights | [Phi](https://azure.microsoft.com/en-us/products/phi/) / [HF Microsoft](https://huggingface.co/microsoft) |
| 2025 | IBM Granite | Granite 3.x/3.3 | 4K-128K 级，按 checkpoint | 开放权重/IBM 平台另计 | [IBM Granite](https://www.ibm.com/granite) / [HF IBM](https://huggingface.co/ibm-granite) |
| 2025 | InternLM | InternLM2.5/3 | 按 checkpoint | 开放权重无统一 token 价 | [GitHub](https://github.com/InternLM/InternLM) / [HF](https://huggingface.co/internlm) |
| 2025 | Baichuan | Baichuan-M1 / Baichuan2 | 按 checkpoint | 开放权重/平台计价不统一 | [GitHub](https://github.com/baichuan-inc/Baichuan2) / [HF](https://huggingface.co/baichuan-inc) |
| 2024 | Yi / 01.AI | Yi-1.5 / Yi-6B/34B | 4K-200K，按 checkpoint | 开放权重无统一 token 价 | [01.AI](https://www.01.ai/) / [HF](https://huggingface.co/01-ai) |
| 2024 | CogVLM | CogVLM2 | 视觉语言，按 checkpoint | 开放权重无统一 token 价 | [GitHub](https://github.com/THUDM/CogVLM) / [HF](https://huggingface.co/THUDM) |
| 2023 | Falcon | Falcon 7B/40B/180B/Mamba | 按 checkpoint | 开放权重无统一 token 价 | [HF TII](https://huggingface.co/tiiuae) |
| 2022 | GPT-J / GPT-Neo | GPT-J-6B、GPT-Neo | 历史小上下文 | 历史/开源 | [EleutherAI](https://github.com/EleutherAI/gpt-neox) / [HF GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b) |
