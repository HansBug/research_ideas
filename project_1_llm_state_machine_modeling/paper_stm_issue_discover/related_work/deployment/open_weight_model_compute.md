# 开源大模型算力需求全景

> **本文回答一个问题**：**给定一个显存包络，哪些开放权重模型真的装得进去。** ⛔ 它不论证 story，⛔ 不比较模型能力，不做选型建议——只把「多大、什么精度、官方说要几张卡」变成可查证的事实。服务 [SUMMARY.md](./SUMMARY.md) §17.5 第 1 件实证。
>
> **核验日**：2026-08-13。**一手证据来源**：Hugging Face Model API（`/api/models/{id}?blobs=true` 的逐文件 `size` 字段）、各仓库 `config.json`、各仓库 `README.md`（model card）原文。⛔ 所有权重体积均为**实测 shard 字节数**，⛔ 不是按参数量推算。
>
> ⚠️ **与本目录既有文件的分工**：[hardware_availability.md](./hardware_availability.md) 回答「**中国工业单位实际买得到多少显存**」（管制、国产卡规格、可得性）；本文回答「**给定显存能装多大的模型**」。两者的显存包络与 4-bit 系数口径**刻意保持一致**（见 §2.1）；⛔ 不要把本文当成硬件可得性的第二真源。

## 0. 一句话结论

**单卡各档的实际天花板（按「权重 + 30K 上下文 KV cache」计，判据见 §2.1）**：

⚠️ **右侧一列的口径**：「**非 4-bit 档**」= 该模型的**原生精度**，或厂商另发的**官方 8-bit（FP8）件**。⛔ 之所以不叫「BF16 档」，是因为一批旗舰**根本没有 BF16**（见下方第 1 条）；故每格额外注明「纯 BF16 天花板」以免混淆。

| 包络 | 4-bit 档天花板 | 非 4-bit 档天花板 |
| :-- | :-- | :-- |
| **单张 24 GB** | **~31B 总参**：[GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash) 的 `Q4_K` GGUF **18.2 GB**（⚠️ 由 ggml-org 发布，非 Z.ai 官方件）。**若只认模型作者自己发的量化件，天花板是 [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) 的 21B 总参 / 13.8 GB 原生 MXFP4** | **~21B 总参**：gpt-oss-20b（原生 MXFP4，13.8 GB）。纯 BF16 天花板只到 **8B**（Qwen3-8B 16.4 GB） |
| **单张 48 GB** | **~36B 总参（有实测量化件）**：[nvidia/Qwen3.6-35B-A3B-NVFP4](https://huggingface.co/nvidia/Qwen3.6-35B-A3B-NVFP4) **23.4 GB**、[Qwen3.5-27B-GPTQ-Int4](https://huggingface.co/Qwen/Qwen3.5-27B-GPTQ-Int4) **30.2 GB**。⚠️ 若接受 0.57 B/参估算，可到 **~49B**（Kimi-Linear-48B-A3B 27.9 估、Nemotron-Super-49B 28.5 估），但这两个都**没有已发布的 4-bit 件** | **~33B 总参**：[Qwen3-32B-FP8](https://huggingface.co/Qwen/Qwen3-32B-FP8) **34.3 GB**（⚠️ 34.3 + KV 7.3 = 41.6，预算 42.2，**极贴边**）· [Qwen3-Coder-30B-A3B-FP8](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8) **31.2 GB** 更稳。纯 BF16 天花板只到 **14B**（Ministral-3-14B 27.9 GB）；Mistral-Small-3.2-24B BF16 的 48.0 GB **刚好装不下** |
| **单张 64 GB（昇腾 910B）** | **~80B 总参**：[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF) 官方 `Q4_K_M` **48.4 GB** + KV 2.8 GB = 51.2 ≤ 56.3 ✅ | **~36B 总参**：[Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) **37.5 GB** + KV 2.3 = 39.8 ✅。纯 BF16 天花板到 **24B**（Mistral-Small-3.2-24B 48.0 + 4.6 = 52.6 ✅） |
| **单张 80 GB** | **~117B 总参**：[gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) 原生 MXFP4 **65.2 GB**——且这是**官方逐字背书**的配置（"fit into a single 80GB GPU"） | **同为 117B**（⛔ 该模型原生就是 MXFP4，它没有 BF16 配置）。纯 BF16 天花板到 **32B**（Nemotron-3.5-Lightning-30B-A3B 65.8 GB，官方明示 1× H100；GLM-4.7-Flash 62.4 GB）；**Qwen3-32B BF16 的 65.5 + KV 7.3 = 72.8 装不下** |
| **单张 96 GB** | **~128B 总参**：[Ling-3.0-flash-int4](https://huggingface.co/inclusionAI/Ling-3.0-flash-int4) **77.0 GB**（官方件）；[Mistral-Small-4-119B-NVFP4](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-NVFP4) **70.8 GB** 亦可 | **~80B 总参**：[Qwen3-Coder-Next-FP8](https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8) **80.4 GB** + KV 2.8 = 83.2（⚠️ 预算 84.5，**极贴边**）。纯 BF16 天花板到 **36B**（Qwen3.6-35B-A3B 71.9 GB） |

⛔ **三条最容易搞错的事实**：

1. ⛔ **一批旗舰模型没有 BF16 配置可选**，因为它们**原生发布就是量化的**：gpt-oss 全系（MXFP4）、DeepSeek V3/V3.1/V3.2/R1（FP8）、DeepSeek V4 Pro/Flash（**FP4 + FP8 混合**）、Kimi K2-Instruct（FP8）、Kimi K2-Thinking（**INT4 QAT**）、Kimi K3（**MXFP4 QAT**）、MiniMax M2 全系（FP8）、Mistral 2512/2603 世代（FP8）、Intern-S1-Pro（FP8）。⛔ **给它们编一个「BF16 显存数」是编造一个不存在的配置**。完整清单见 §3。
2. ⛔ **8×80 GB H100 节点（640 GB）装不下 DeepSeek-V3/V3.2**：FP8 权重实测 **689.5 GB**，已超过整节点名义显存。DeepSeek 官方 demo 用的就是 `--nnodes 2 --nproc-per-node 8`（**16 卡**）。这条被 GLM-4.5 官方部署表独立印证：355B BF16 要 `H100 × 16 / H200 × 8`。
3. ⛔ **MoE 的「激活参数量」与显存无关**：Kimi K2 只激活 32B，但 **1026B 总参必须全部常驻**，FP8 下 1029.2 GB。显存一律按**总参**算。

**收录规模**：共探测 **145 个 HF 仓库**，**143 个成功取到实测数据**（⛔ 2 个返回 401：`deepseek-ai/DeepSeek-V4`（该名下无公开仓库，实际发布的是 `-Pro` / `-Flash` 两个）与 `nvidia/Nemotron-3-Super-120B-A12B-BF16`）；§1.2 主表收 **141 行**，覆盖 **20 个模型系列**（DeepSeek / Qwen / Llama / Mistral / gpt-oss / GLM / Kimi / Gemma / Nemotron / Phi / InternLM / Yi / MiniMax / Baichuan / Falcon / Cohere / Granite / Ling / Step / Hunyuan）。⛔ **官方最小部署配置**：**11 个系列有可逐字引用的明确说法**，**其余只给了 `--tp N` 示例命令或干脆未给**（逐条如实记录见 §4）。

## 1. 全景表

### 1.1 口径说明（⛔ 先读，否则会误读表里的每一个数字）

| 字段 | 本文的确切含义 | ⚠️ 已知局限 |
| :-- | :-- | :-- |
| **HF 仓库创建日** | HF API 的 `createdAt` 字段，即权重首次上传的时间戳 | ⚠️ **它不等于官方发布日**。实测两种情形都有：gpt-oss 仓库创建 2025-08-04、官方公告 2025-08-05（差 1 天）；而 gemma-4 仓库创建 2026-03-11、官方公告 **2026-04-02**（差 3 周，先私有暂存后公开）。故本字段是发布日的**下界**，不是发布日本身 |
| **总参 / 激活参** | 优先取 model card 明写值；否则取 HF `safetensors.total` | ⚠️ 原生量化模型的 `safetensors.total` 会把打包后的元素数当参数数报，与 card 值可能不一致；本表以 card 为准并注明 |
| **权重体积** | **实测**：该仓库主权重集（`model-*-of-*.safetensors` / `consolidated*.safetensors`）的 `size` 字段合计，单位 GB = $10^9$ 字节 | ⛔ **已剔除三类重复计数**：`original/` 与 `metal/` 副本（gpt-oss 的仓库总量 195.7 GB 里有 **3 份同样的权重**，真实主集只有 65.2 GB）、Mistral 的 `consolidated` + 分片双份、GLM 的独立 `mtp.safetensors`（投机解码模块，可不加载） |
| **原生发布精度** | 三重交叉：`config.json` 的 `quantization_config.quant_method` + HF safetensors 的 dtype 普查 + model card 原文 | ⛔ 单看任何一项都会错 |
| **context** | `config.json` 的 `max_position_embeddings`；与 card 声明不一致时两者都列 | ⚠️ **凡 card 写「natively X, extensible to Y」的，Y 一律是 YaRN / RoPE 外推**，不是原生窗口 |
| **KV@30K** | 按 30,000 token、FP16 KV 计：$\mathrm{KV} = 2 \cdot L \cdot H_{kv} \cdot d_h \cdot 2 \cdot T$ 字节；MLA 类模型改按 $(\mathrm{kv\_lora\_rank} + \mathrm{qk\_rope\_head\_dim}) \cdot L \cdot 2 \cdot T$ | ⛔ **这是上界，不是实测**。对滑窗注意力模型（gemma 系、gpt-oss）严重高估——gemma-4-31B 的 27.5 GB 是把全部 60 层当全局注意力算的，而它实际是局部/全局交错。混合 Mamba 模型（Nemotron-H、Falcon-H1）同理偏高 |

⛔ **本表不含**：hosted-only 模型（Qwen3.8-Max、GLM Coding Plan、DeepSeek API 线）、纯视觉/语音模型、embedding / reranker、7B 以下小模型（除标杆）。

### 1.2 主表（按 HF 仓库创建日降序）

| HF 创建日 | 模型（HF id） | 总参 / 激活参 | 架构 | 原生精度 | 权重实测 | context | KV@30K | 许可证 |
| ---: | :-- | :-- | :-- | :-- | ---: | ---: | ---: | :-- |
| 2026-08-10 | [inclusionAI/Ling-3.0-tiny](https://huggingface.co/inclusionAI/Ling-3.0-tiny) | 7.9B / — | MoE 128E/8 | BF16 | **15.8 GB** | 131,072 | 0.8 GB | MIT |
| 2026-08-08 | [Qwen/Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) | **2446B** / 95B | MoE 512E/10 | BF16 | **4892.4 GB** | 262,144（可扩 1,010,000 YaRN） | ⏳ | ⛔ **`qwen3.8-max` 自定义** |
| 2026-08-08 | [Qwen/Qwen3.8-2.4T-A95B-FP8](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8) | 2446B / 95B | MoE 512E/10 | FP8（官方量化件） | **2496.1 GB** | 同上 | ⏳ | 同上 |
| 2026-08-04 | [nvidia/…Nemotron-3.5-Lightning-30B-A3B-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4) | 31.6B / 3B | MoE 128E/6 混合 | **NVFP4**（ModelOpt） | **21.6 GB** | 1,048,576 | 1.5 GB | OpenMDW-1.1 |
| 2026-08-04 | [inclusionAI/Ling-3.0-flash-int4](https://huggingface.co/inclusionAI/Ling-3.0-flash-int4) | 127.5B / — | MoE 512E/8 | **INT4**（compressed-tensors） | **77.0 GB** | 262,144 | 1.4 GB | MIT |
| 2026-08-04 | [inclusionAI/Ling-3.0-flash-fp4](https://huggingface.co/inclusionAI/Ling-3.0-flash-fp4) | 127.5B / — | 同上 | FP4 | **70.4 GB** | 262,144 | 1.4 GB | MIT |
| 2026-08-04 | [inclusionAI/Ling-3.0-flash-fp8](https://huggingface.co/inclusionAI/Ling-3.0-flash-fp8) | 127.5B / — | 同上 | FP8 | **128.4 GB** | 262,144 | 1.4 GB | MIT |
| 2026-08-02 | [inclusionAI/Ling-3.0-flash](https://huggingface.co/inclusionAI/Ling-3.0-flash) | 127.5B / — | MoE 512E/8，MLA | BF16 | **255.0 GB** | 262,144 | 1.4 GB | MIT |
| 2026-08-01 | [nvidia/…Nemotron-3.5-Lightning-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) | 31.6B / 3B | MoE 128E/6 混合 | BF16 | **65.8 GB** | 262,144（NVFP4 版标 1M） | 1.5 GB | OpenMDW-1.1 |
| 2026-07-31 | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | 284B / 13B | MoE 256E/6 | ⛔ **FP4 + FP8 混合** | **166.9 GB** | 1,048,576 | 2.5 GB ⚠️ | MIT |
| 2026-07-04 | [tencent/Hy3-FP8](https://huggingface.co/tencent/Hy3-FP8) | 298.8B / — | MoE 192E/8 | FP8 | **299.9 GB** | 262,144（card 写 256K） | 9.2 GB | Apache-2.0 |
| 2026-07-02 | [tencent/Hy3](https://huggingface.co/tencent/Hy3) | 298.8B / — | MoE 192E/8 | BF16 | **597.6 GB** | 262,144 | 9.2 GB | Apache-2.0 |
| 2026-06-22 | [Qwen/Qwen-AgentWorld-35B-A3B](https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B) | 34.7B / 3B | MoE 256E/8 | BF16 | **69.3 GB** | 262,144 | ~2.3 GB | Apache-2.0 |
| 2026-06-22 | [nvidia/Qwen3.6-27B-NVFP4](https://huggingface.co/nvidia/Qwen3.6-27B-NVFP4) | 27.8B / — | dense | NVFP4 | **21.9 GB** | 262,144 | 7.3 GB | Apache-2.0 |
| 2026-06-16 | [zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) | **753.3B** / 40B | MoE 256E/8，DSA + MLA | BF16 | **1506.7 GB** | 1,048,576 | 2.5 GB | MIT |
| 2026-06-16 | [zai-org/GLM-5.2-FP8](https://huggingface.co/zai-org/GLM-5.2-FP8) | 753.3B / 40B | 同上 | FP8 | **755.6 GB** | 1,048,576 | 2.5 GB | MIT |
| 2026-06-13 | [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | **2.8T** / 104B | MoE 896E/16，KDA + Gated MLA | ⛔ **MXFP4 权重 / MXFP8 激活（QAT）** | **1560.9 GB** | 1,048,576 | 3.0 GB | ⛔ `kimi-k3` 自定义 |
| 2026-06-05 | [CohereLabs/North-Mini-Code-1.0](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) | 30.5B / — | MoE 128E/8 | BF16 | **61.0 GB** | 500,000 | 2.8 GB | Apache-2.0 |
| 2026-06-04 | [google/gemma-4-31B-it-qat-w4a16-ct](https://huggingface.co/google/gemma-4-31B-it-qat-w4a16-ct) | 31.3B / — | dense | **W4A16（QAT）** | **23.3 GB** | 262,144 | ≤27.5 GB ⚠️ | Apache-2.0 |
| 2026-05-27 | [stepfun-ai/Step-3.7-Flash-NVFP4](https://huggingface.co/stepfun-ai/Step-3.7-Flash-NVFP4) | 201.4B / — | MoE | NVFP4 | **124.4 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2026-05-27 | [nvidia/Qwen3.6-35B-A3B-NVFP4](https://huggingface.co/nvidia/Qwen3.6-35B-A3B-NVFP4) | 36.0B / 3B | MoE 256E/8 | NVFP4 | **23.4 GB** | 262,144 | 2.3 GB | Apache-2.0 |
| 2026-05-23 | [google/gemma-4-12B-it](https://huggingface.co/google/gemma-4-12B-it) | 12.0B / — | dense 多模态 | BF16 | **23.9 GB** | 262,144（card 写 256K） | ≤11.0 GB ⚠️ | Apache-2.0 |
| 2026-05-23 | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | 201.4B / — | MoE | BF16 | **402.7 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2026-05-18 | [CohereLabs/command-a-plus-05-2026-fp8](https://huggingface.co/CohereLabs/command-a-plus-05-2026-fp8) | 218.8B / — | MoE 128E/8 | FP8 | **225.0 GB** | 200,000 | 3.7 GB | Apache-2.0 |
| 2026-05-11 | [CohereLabs/command-a-plus-05-2026-bf16](https://huggingface.co/CohereLabs/command-a-plus-05-2026-bf16) | 218.8B / — | MoE 128E/8 | BF16 | **437.5 GB** | 200,000 | 3.7 GB | Apache-2.0（相比 2025 版 command-a 的 CC-BY-NC 是**放开**） |
| 2026-04-22 | [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | **1.6T** / 49B | MoE 384E/6，CSA + HCA | ⛔ **FP4 + FP8 混合**（专家 FP4，其余多为 FP8） | **864.7 GB** | 1,048,576 | 3.5 GB ⚠️ | MIT |
| 2026-04-22 | [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash) | 284B / 13B | MoE 256E/6 | ⛔ **FP4 + FP8 混合** | **159.6 GB** | 1,048,576 | 2.5 GB ⚠️ | MIT |
| 2026-04-21 | [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) | 27.8B / — | dense | BF16 | **55.6 GB** | 262,144（可扩 1,010,000 YaRN） | 7.3 GB | Apache-2.0 |
| 2026-04-21 | [Qwen/Qwen3.6-27B-FP8](https://huggingface.co/Qwen/Qwen3.6-27B-FP8) | 27.8B / — | dense | FP8 | **30.9 GB** | 同上 | 7.3 GB | Apache-2.0 |
| 2026-04-15 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | 36.0B / 3B | MoE 256E/8 | BF16 | **71.9 GB** | 262,144（可扩 1,010,000 YaRN） | 2.3 GB | Apache-2.0 |
| 2026-04-15 | [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) | 36.0B / 3B | MoE 256E/8 | FP8 | **37.5 GB** | 同上 | 2.3 GB | Apache-2.0 |
| 2026-04-09 | [MiniMaxAI/MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) | 228.7B / ~10B | MoE 256E/8 | ⛔ **FP8**（block 128×128，dynamic） | **230.1 GB** | 204,800 | 7.1 GB | ⛔ 自定义 |
| 2026-04-03 | [zai-org/GLM-5.1](https://huggingface.co/zai-org/GLM-5.1) | 753.9B / 40B | MoE 256E/8 | BF16 | **1507.7 GB** | 202,752 | 2.5 GB | MIT |
| 2026-04-02 | [nvidia/Gemma-4-31B-IT-NVFP4](https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4) | 31.3B / — | dense | NVFP4 | **32.6 GB** | 262,144 | ≤27.5 GB ⚠️ | Apache-2.0 |
| 2026-03-31 | [mistralai/Mistral-Medium-3.5-128B](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) | 127.7B / — | dense | ⛔ **FP8**（static） | **133.6 GB** | 262,144 | ⏳ | ⛔ 自定义 |
| 2026-03-11 | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) | 31.3B / — | dense 多模态 | BF16 | **62.5 GB** | 262,144（card 写 256K） | ≤27.5 GB ⚠️ | Apache-2.0（相比 Gemma 1–3 的 Gemma Terms 是**放开**） |
| 2026-03-11 | [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it) | 26.5B / 3.8B | MoE 128E | BF16 | **51.6 GB** | 262,144 | ≤6.9 GB ⚠️ | Apache-2.0 |
| 2026-03-03 | [mistralai/Mistral-Small-4-119B-2603-NVFP4](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-NVFP4) | 119.4B / — | MoE 128E/4，MLA | NVFP4 | **70.8 GB** | ⏳ | 0.6 GB | Apache-2.0 |
| 2026-03-03 | [Qwen/Qwen3.5-27B-GPTQ-Int4](https://huggingface.co/Qwen/Qwen3.5-27B-GPTQ-Int4) | 27.8B / — | dense | **GPTQ-INT4** | **30.2 GB** ⚠️ | 262,144 | 7.3 GB | Apache-2.0 |
| 2026-03-02 | [google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it) | 8.0B（有效 4.5B） | dense 边端 | BF16 | **16.0 GB** | 131,072 | ⏳ | Apache-2.0 |
| 2026-02-25 | [Qwen/Qwen3.5-27B-FP8](https://huggingface.co/Qwen/Qwen3.5-27B-FP8) | 27.8B / — | dense | FP8 | **30.9 GB** | 262,144 | 7.3 GB | Apache-2.0 |
| 2026-02-24 | [Qwen/Qwen3.5-122B-A10B](https://huggingface.co/Qwen/Qwen3.5-122B-A10B) | 125.1B / 10B | MoE 256E/8 | BF16 | **250.2 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2026-02-24 | [Qwen/Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B) | 36.0B / 3B | MoE 256E/8 | BF16 | **71.9 GB** | 262,144 | 2.3 GB | Apache-2.0 |
| 2026-02-24 | [Qwen/Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B) | 27.8B / — | dense | BF16 | **55.6 GB** | 262,144 | 7.3 GB | Apache-2.0 |
| 2026-02-16 | [Qwen/Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | 403.4B / 17B | MoE 512E/10 | BF16 | **806.8 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2026-02-12 | [MiniMaxAI/MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5) | 228.7B / ~10B | MoE 256E/8 | ⛔ **FP8** | **230.1 GB** | 196,608 | 7.1 GB | ⛔ 自定义 |
| 2026-02-11 | [zai-org/GLM-5](https://huggingface.co/zai-org/GLM-5) | **753.9B** / 40B | MoE 256E/8，DSA + MLA | BF16 | **1507.7 GB** | 202,752 | 2.5 GB | MIT |
| 2026-02-11 | [zai-org/GLM-5-FP8](https://huggingface.co/zai-org/GLM-5-FP8) | 753.9B / 40B | 同上 | FP8 | **756.2 GB** | 202,752 | 2.5 GB | MIT |
| 2026-02-02 | [internlm/Intern-S1-Pro](https://huggingface.co/internlm/Intern-S1-Pro) | ⏳（MoE 512E/8） | MoE | ⛔ **FP8** | **919.0 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2026-02-01 | [Qwen/Qwen3-Coder-Next-FP8](https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8) | 79.7B / 3B | MoE 512E/10 | FP8 | **80.4 GB** | 262,144 | 2.8 GB | Apache-2.0 |
| 2026-01-30 | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 79.7B / 3B | MoE 512E/10 | BF16 | **159.4 GB** | 262,144 | 2.8 GB | Apache-2.0 |
| 2026-01-28 | [tiiuae/Falcon-H1R-7B-FP8](https://huggingface.co/tiiuae/Falcon-H1R-7B-FP8) | 7.6B / — | 混合 Mamba | FP8 | **8.4 GB** | 262,144 | ⏳ | ⛔ Falcon LLM License |
| 2026-01-23 | [mistralai/Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 119.4B / — | MoE 128E/4，MLA | ⛔ **FP8**（static） | **120.9 GB** | 1,048,576（card 写 256K） | 0.6 GB | Apache-2.0 |
| 2026-01-19 | [zai-org/GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash) | 31.2B / — | MoE 64E/4，MLA | BF16 | **62.4 GB** | 202,752 | 1.5 GB | MIT |
| 2026-01-13 | [baichuan-inc/Baichuan-M3-235B](https://huggingface.co/baichuan-inc/Baichuan-M3-235B) | 235.1B / — | MoE 128E/8 | BF16 | **470.2 GB** | 40,960 | 5.4 GB | Apache-2.0 |
| 2026-01-13 | [baichuan-inc/Baichuan-M3-235B-GPTQ-INT4](https://huggingface.co/baichuan-inc/Baichuan-M3-235B-GPTQ-INT4) | 235.1B / — | 同上 | **GPTQ-INT4** | **124.5 GB** | 40,960 | 5.4 GB | Apache-2.0 |
| 2025-12-22 | [zai-org/GLM-4.7](https://huggingface.co/zai-org/GLM-4.7) | 353B（含 MTP 358.3B）/ 32B | MoE 160E/8 | BF16 | **705.6 GB**（+ MTP 11.1 GB） | 202,752 | 10.5 GB | MIT |
| 2025-12-22 | [zai-org/GLM-4.7-FP8](https://huggingface.co/zai-org/GLM-4.7-FP8) | 同上 | 同上 | FP8 | **354.9 GB**（+ MTP 7.2 GB） | 202,752 | 10.5 GB | MIT |
| 2025-12-04 | [nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) | 31.6B / 3B | MoE 128E/6 混合 | BF16 | **63.2 GB** | 262,144 | 1.5 GB | ⛔ NVIDIA 自定义 |
| 2025-12-01 | [deepseek-ai/DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2) | 685B（含 MTP）/ 37B | MoE 256E/8，MLA + DSA | ⛔ **FP8**（block 128×128） | **689.5 GB** | 163,840 | 2.0 GB | MIT |
| 2025-11-28 | [deepseek-ai/DeepSeek-V3.2-Speciale](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Speciale) | 同上 | 同上 | ⛔ **FP8** | **689.5 GB** | 163,840 | 2.0 GB | MIT |
| 2025-11-28 | [mistralai/Mistral-Large-3-675B-Instruct-2512](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) | 675B | dense（Mistral `consolidated` 格式） | ⛔ **FP8** | **681.5 GB** | ⏳ | ⏳ | Apache-2.0 |
| 2025-11-28 | […-2512-NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) | 675B | 同上 | **NVFP4** | **403.1 GB** | ⏳ | ⏳ | Apache-2.0 |
| 2025-11-04 | [moonshotai/Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) | **1T** / 32B | MoE 384E/8，MLA | ⛔ **INT4 权重（QAT）** | **594.2 GB** | 262,144（card 写 256K） | 2.0 GB | ⛔ modified-MIT |
| 2025-10-31 | [mistralai/Ministral-3-14B-Reasoning-2512](https://huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512) | 13.9B / — | dense | BF16 | **27.9 GB** | 262,144 | 4.6 GB | Apache-2.0 |
| 2025-10-31 | [mistralai/Ministral-3-8B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) | 8.9B / — | dense | ⛔ **FP8**（另有 `-BF16` 仓库） | **10.4 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2025-10-30 | [moonshotai/Kimi-Linear-48B-A3B-Instruct](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct) | 49.1B / 3B | MoE 256E，线性注意力 | BF16 | **98.2 GB** | ⏳ | 0.9 GB | MIT |
| 2025-10-22 | [MiniMaxAI/MiniMax-M2](https://huggingface.co/MiniMaxAI/MiniMax-M2) | 228.7B / ~10B | MoE 256E/8 | ⛔ **FP8** | **230.1 GB** | 196,608 | 7.1 GB | ⛔ 自定义 |
| 2025-09-29 | [deepseek-ai/DeepSeek-V3.2-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp) | 685B / 37B | MoE 256E/8，MLA + DSA | ⛔ **FP8** | **689.5 GB** | 163,840 | 2.0 GB | MIT |
| 2025-09-29 | [zai-org/GLM-4.6](https://huggingface.co/zai-org/GLM-4.6) | 352B（含 MTP 356.8B） | MoE 160E/8 | BF16 | **705.6 GB**（+ 8.0 GB） | 202,752 | 10.5 GB | MIT |
| 2025-09-28 | [mistralai/Mistral-Large-3](https://huggingface.co/mistralai/Mistral-Large-3) | 675B | dense | BF16（`consolidated` 格式） | **1352.0 GB** | ⏳ | ⏳ | Apache-2.0 |
| 2025-09-22 | [deepseek-ai/DeepSeek-V3.1-Terminus](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | 2.0 GB | MIT |
| 2025-09-18 | [openai/gpt-oss-safeguard-120b](https://huggingface.co/openai/gpt-oss-safeguard-120b) | 120B / 5.1B | MoE 128E/4 | ⛔ **MXFP4** | **65.2 GB** | 131,072（YaRN factor 32） | 2.1 GB | Apache-2.0 |
| 2025-09-16 | [ibm-granite/granite-4.0-h-small](https://huggingface.co/ibm-granite/granite-4.0-h-small) | 32.2B / — | MoE 72E/10 混合 | BF16 | **64.4 GB** | 131,072 | 4.6 GB | Apache-2.0 |
| 2025-09-12 | [mistralai/Magistral-Small-2509](https://huggingface.co/mistralai/Magistral-Small-2509) | 24.0B / — | dense | BF16 | **48.0 GB** | 131,072 | 4.6 GB | Apache-2.0 |
| 2025-09-09 | [Qwen/Qwen3-Next-80B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) | 81.3B / 3B | MoE 512E/10 混合注意力 | BF16 | **162.7 GB** | 262,144（可扩 1M YaRN） | 2.8 GB | Apache-2.0 |
| 2025-09-03 | [moonshotai/Kimi-K2-Instruct-0905](https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905) | **1T** / 32B | MoE 384E/8，MLA | ⛔ **FP8** | **1029.2 GB** | 262,144 | 2.0 GB | ⛔ modified-MIT |
| 2025-08-21 | [deepseek-ai/DeepSeek-V3.1](https://huggingface.co/deepseek-ai/DeepSeek-V3.1) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | 2.0 GB | MIT |
| 2025-08-12 | [CohereLabs/command-a-reasoning-08-2025](https://huggingface.co/CohereLabs/command-a-reasoning-08-2025) | 111.1B / — | dense | BF16 | **222.1 GB** | ⏳ | ⏳ | ⛔ **CC-BY-NC-4.0（不可商用）** |
| 2025-08-12 | [nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) | 8.9B / — | 混合 Mamba | BF16 | **17.8 GB** | 131,072 | ⏳ | ⛔ NVIDIA 自定义 |
| 2025-08-10 | [baichuan-inc/Baichuan-M2-32B](https://huggingface.co/baichuan-inc/Baichuan-M2-32B) | 32.8B / — | dense | BF16 | **65.5 GB** | 131,072 | 7.3 GB | Apache-2.0 |
| 2025-08-04 | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | **117B** / 5.1B | MoE 128E/4 | ⛔ **MXFP4**（MoE 权重） | **65.2 GB** | 131,072（YaRN factor 32，原生 4,096） | 2.1 GB | Apache-2.0 |
| 2025-08-04 | [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | 21B / 3.6B | MoE 32E/4 | ⛔ **MXFP4** | **13.8 GB** | 131,072 | 1.4 GB | Apache-2.0 |
| 2025-07-31 | [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | 30.5B / 3B | MoE 128E/8 | BF16 | **61.1 GB** | 262,144 | 2.8 GB | Apache-2.0 |
| 2025-07-31 | […-FP8](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8) | 30.5B / 3B | 同上 | FP8 | **31.2 GB** | 262,144 | 2.8 GB | Apache-2.0 |
| 2025-07-28 | [Qwen/Qwen3-30B-A3B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507) | 30.5B / 3B | MoE 128E/8 | BF16 | **61.1 GB** | 262,144 | 2.8 GB | Apache-2.0 |
| 2025-07-25 | [Qwen/Qwen3-235B-A22B-Thinking-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Thinking-2507) | 235.1B / 22B | MoE 128E/8 | BF16 | **470.2 GB** | 262,144 | 5.4 GB | Apache-2.0 |
| 2025-07-25 | [nvidia/Llama-3_3-Nemotron-Super-49B-v1_5](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1_5) | 49.9B / — | NAS 剪枝 dense | BF16 | **99.7 GB** | 131,072（RoPE factor 16） | ⏳ | ⛔ NVIDIA 自定义 |
| 2025-07-22 | [Qwen/Qwen3-Coder-480B-A35B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct) | 480.2B / 35B | MoE 160E/8 | BF16 | **960.3 GB** | 262,144 | ⏳ | Apache-2.0 |
| 2025-07-21 | [Qwen/Qwen3-235B-A22B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507) | 235.1B / 22B | MoE 128E/8 | BF16 | **470.2 GB** | 262,144（可扩 1,010,000 YaRN） | 5.4 GB | Apache-2.0 |
| 2025-07-20 | [zai-org/GLM-4.5](https://huggingface.co/zai-org/GLM-4.5) | 355B / 32B | MoE 160E/8 | BF16 | **716.7 GB**（含 MTP） | 131,072 | 10.5 GB | MIT |
| 2025-07-20 | [zai-org/GLM-4.5-FP8](https://huggingface.co/zai-org/GLM-4.5-FP8) | 355B / 32B | 同上 | FP8 | **361.3 GB** | 131,072 | 10.5 GB | MIT |
| 2025-07-20 | [zai-org/GLM-4.5-Air](https://huggingface.co/zai-org/GLM-4.5-Air) | 106B / 12B | MoE 128E/8 | BF16 | **220.9 GB** | 131,072 | 5.3 GB | MIT |
| 2025-07-20 | [zai-org/GLM-4.5-Air-FP8](https://huggingface.co/zai-org/GLM-4.5-Air-FP8) | 106B / 12B | 同上 | FP8 | **112.6 GB** | 131,072 | 5.3 GB | MIT |
| 2025-07-11 | [moonshotai/Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) | **1T** / 32B | MoE 384E/8，MLA | ⛔ **FP8** | **1029.2 GB** | 131,072（card 写 128K） | 2.0 GB | ⛔ modified-MIT |
| 2025-07-04 | [mistralai/Devstral-Small-2507](https://huggingface.co/mistralai/Devstral-Small-2507) | 23.6B / — | dense | BF16 | **47.1 GB** | 131,072 | 4.6 GB | Apache-2.0 |
| 2025-06-19 | [mistralai/Mistral-Small-3.2-24B-Instruct-2506](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506) | 24.0B / — | dense 多模态 | BF16 | **48.0 GB** | 131,072 | 4.6 GB | Apache-2.0 |
| 2025-06-13 | [MiniMaxAI/MiniMax-M1-80k](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k) | 456.1B / 45.9B | MoE 32E/2，闪电注意力 | BF16 | **912.2 GB** | 10,240,000 | ⏳ | Apache-2.0 |
| 2025-05-29 | [deepseek-ai/DeepSeek-R1-0528-Qwen3-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B) | 8.2B / — | dense（蒸馏） | BF16 | **16.4 GB** | 131,072 | 4.1 GB | MIT |
| 2025-05-28 | [deepseek-ai/DeepSeek-R1-0528](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | 2.0 GB | MIT |
| 2025-05-01 | [Qwen/Qwen3-32B-AWQ](https://huggingface.co/Qwen/Qwen3-32B-AWQ) | 32.8B / — | dense | **AWQ-INT4** | **19.3 GB** | 40,960 | 7.3 GB | Apache-2.0 |
| 2025-05-01 | [tiiuae/Falcon-H1-34B-Instruct](https://huggingface.co/tiiuae/Falcon-H1-34B-Instruct) | 33.6B / — | 混合 Mamba | BF16 | **67.3 GB** | 262,144 | ⏳ | ⛔ Falcon LLM License |
| 2025-04-28 | [Qwen/Qwen3-32B-FP8](https://huggingface.co/Qwen/Qwen3-32B-FP8) | 32.8B / — | dense | FP8 | **34.3 GB** | 40,960 | 7.3 GB | Apache-2.0 |
| 2025-04-27 | [Qwen/Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B) | 235.1B / 22B | MoE 128E/8 | BF16 | **470.2 GB** | 40,960（32,768 原生 + YaRN 到 131,072） | 5.4 GB | Apache-2.0 |
| 2025-04-27 | [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) | 32.8B / — | dense | BF16 | **65.5 GB** | 40,960（32,768 原生 + YaRN 到 131,072） | 7.3 GB | Apache-2.0 |
| 2025-04-27 | [Qwen/Qwen3-30B-A3B](https://huggingface.co/Qwen/Qwen3-30B-A3B) | 30.5B / 3B | MoE 128E/8 | BF16 | **61.1 GB** | 40,960 | 2.8 GB | Apache-2.0 |
| 2025-04-27 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8.2B / — | dense | BF16 | **16.4 GB** | 40,960 | 4.1 GB | Apache-2.0 |
| 2025-04-17 | [microsoft/Phi-4-reasoning-plus](https://huggingface.co/microsoft/Phi-4-reasoning-plus) | 14.7B / — | dense | BF16 | **29.3 GB** | 32,768 | 5.7 GB | MIT |
| 2025-04-02 | [meta-llama/Llama-4-Scout-17B-16E-Instruct](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) | 108.6B / 17B | MoE 16E | BF16 | **217.3 GB** | ⏳（card 称 10M） | ⏳ | ⛔ Llama 4 社区许可（仓库 gated） |
| 2025-04-01 | [meta-llama/Llama-4-Maverick-17B-128E-Instruct](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) | 401.6B / 17B | MoE 128E | BF16 | **803.2 GB** | ⏳（card 称 1M） | ⏳ | ⛔ Llama 4 社区许可 |
| 2025-04-01 | […-FP8](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8) | 401.6B / 17B | 同上 | FP8 | **416.8 GB** | ⏳ | ⏳ | 同上 |
| 2025-03-24 | [deepseek-ai/DeepSeek-V3-0324](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | 2.0 GB | MIT |
| 2025-03-11 | [mistralai/Mistral-Small-3.1-24B-Instruct-2503](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) | 24.0B / — | dense 多模态 | BF16 | **48.0 GB** | 131,072 | 4.6 GB | Apache-2.0 |
| 2025-03-11 | [CohereLabs/c4ai-command-a-03-2025](https://huggingface.co/CohereLabs/c4ai-command-a-03-2025) | 111.1B / — | dense | BF16 | **222.1 GB** | ⏳ | ⏳ | ⛔ **CC-BY-NC-4.0（不可商用）** |
| 2025-03-01 | [google/gemma-3-27b-it](https://huggingface.co/google/gemma-3-27b-it) | 27.4B / — | dense 多模态 | BF16 | **54.9 GB** | ⏳（gated） | ⏳ | ⛔ Gemma Terms |
| 2025-03-01 | [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it) | 12.2B / — | dense 多模态 | BF16 | **24.4 GB** | ⏳ | ⏳ | ⛔ Gemma Terms |
| 2025-02-20 | [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) | 4.3B / — | dense 多模态 | BF16 | **8.6 GB** | ⏳ | ⏳ | ⛔ Gemma Terms |
| 2025-01-20 | [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | 2.0 GB | MIT |
| 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) | 70.6B / — | dense（蒸馏 Llama） | BF16 | **141.1 GB** | 131,072 | 9.2 GB | MIT |
| 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-32B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B) | 32.8B / — | dense（蒸馏 Qwen） | BF16 | **65.5 GB** | 131,072 | 7.3 GB | MIT |
| 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B) | 7.6B / — | dense（蒸馏） | BF16 | **15.2 GB** | 131,072 | ⏳ | MIT |
| 2025-01-13 | [internlm/internlm3-8b-instruct](https://huggingface.co/internlm/internlm3-8b-instruct) | 8.8B / — | dense | BF16 | **17.6 GB** | 32,768 | ⏳ | Apache-2.0 |
| 2025-01-12 | [MiniMaxAI/MiniMax-Text-01](https://huggingface.co/MiniMaxAI/MiniMax-Text-01) | 456.1B / 45.9B | MoE 32E/2 | BF16 | **914.7 GB** | 10,240,000 | ⏳ | ⛔ 自定义 |
| 2024-12-25 | [deepseek-ai/DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8**（官方只发 FP8，提供转 BF16 脚本） | **688.6 GB** | 163,840 | 2.0 GB | MIT（模型许可另附） |
| 2024-12-14 | [tiiuae/Falcon3-10B-Instruct](https://huggingface.co/tiiuae/Falcon3-10B-Instruct) | 10.3B / — | dense | BF16 | **20.6 GB** | 32,768 | ⏳ | ⛔ Falcon LLM License |
| 2024-12-11 | [microsoft/phi-4](https://huggingface.co/microsoft/phi-4) | 14.7B / — | dense | BF16 | **29.3 GB** | 16,384 | 5.7 GB | MIT |
| 2024-11-26 | [meta-llama/Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) | 70.6B / — | dense | BF16 | **141.1 GB** | ⏳（gated，card 称 128K） | ~9.2 GB ⚠️ | ⛔ Llama 3.3 社区许可 |
| 2024-11-14 | [mistralai/Mistral-Large-Instruct-2411](https://huggingface.co/mistralai/Mistral-Large-Instruct-2411) | 122.6B / — | dense | BF16 | **245.2 GB** | 131,072 | ⏳ | ⛔ MRL（研究许可） |
| 2024-11-06 | [Qwen/Qwen2.5-Coder-32B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct) | 32.8B / — | dense | BF16 | **65.5 GB** | 32,768 | 7.3 GB | Apache-2.0 |
| 2024-10-15 | [mistralai/Ministral-8B-Instruct-2410](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410) | 8.0B / — | dense | BF16 | **16.0 GB** | 32,768 | ⏳ | ⛔ MRL |
| 2024-09-18 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 3.2B / — | dense | BF16 | **6.4 GB** | ⏳ | ⏳ | ⛔ Llama 3.2 社区许可 |
| 2024-09-17 | [Qwen/Qwen2.5-32B-Instruct](https://huggingface.co/Qwen/Qwen2.5-32B-Instruct) | 32.8B / — | dense | BF16 | **65.5 GB** | 32,768 | 7.3 GB | Apache-2.0 |
| 2024-09-16 | [Qwen/Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) | 72.7B / — | dense | BF16 | **145.4 GB** | 32,768 | ⏳ | ⛔ Qwen License |
| 2024-07-20 | [meta-llama/Llama-3.1-405B-Instruct-FP8](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8) | 405.9B / — | dense | FP8（fbgemm） | **487.2 GB** | ⏳ | ⏳ | ⛔ Llama 3.1 社区许可 |
| 2024-07-18 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 8.0B / — | dense | BF16 | **16.1 GB** | ⏳ | ⏳ | 同上 |
| 2024-07-16 | [meta-llama/Llama-3.1-405B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct) | 405.9B / — | dense | BF16 | **811.7 GB** | ⏳ | ⏳ | 同上 |
| 2024-07-16 | [meta-llama/Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) | 70.6B / — | dense | BF16 | **141.1 GB** | ⏳ | ~9.2 GB ⚠️ | 同上 |
| 2024-06-24 | [google/gemma-2-27b-it](https://huggingface.co/google/gemma-2-27b-it) | 27.2B / — | dense | BF16 | **54.5 GB** | ⏳ | ⏳ | ⛔ Gemma Terms |
| 2024-06-04 | [THUDM/glm-4-9b-chat](https://huggingface.co/THUDM/glm-4-9b-chat) | 9.4B / — | dense | BF16 | **18.8 GB** | ⏳ | ⏳ | ⛔ GLM-4 许可 |
| 2024-05-29 | [mistralai/Codestral-22B-v0.1](https://huggingface.co/mistralai/Codestral-22B-v0.1) | 22.2B / — | dense | BF16 | **44.5 GB** | 32,768 | ⏳ | ⛔ MNPL（非生产） |
| 2024-05-10 | [01-ai/Yi-1.5-34B-Chat](https://huggingface.co/01-ai/Yi-1.5-34B-Chat) | 34.4B / — | dense | BF16 | **68.8 GB** | 4,096 | ⏳ | Apache-2.0 |

**GGUF（llama.cpp / CPU-GPU 混合部署）实测体积**：

| GGUF 仓库 | 发布方 | Q4_K_M | Q5_K_M | Q8_0 | F16/BF16 |
| :-- | :-- | ---: | ---: | ---: | ---: |
| [Qwen/Qwen3-235B-A22B-GGUF](https://huggingface.co/Qwen/Qwen3-235B-A22B-GGUF) | Qwen 官方 | **142.2 GB** | 166.8 GB | 249.9 GB | — |
| [Qwen/Qwen3-Coder-Next-GGUF](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF) | Qwen 官方 | **48.4 GB** | 56.7 GB | 84.8 GB | 159.5 GB |
| [Qwen/Qwen3-8B-GGUF](https://huggingface.co/Qwen/Qwen3-8B-GGUF) | Qwen 官方 | **5.0 GB** | 5.9 GB | 8.7 GB | — |
| [ggml-org/GLM-4.7-Flash-GGUF](https://huggingface.co/ggml-org/GLM-4.7-Flash-GGUF) | ⚠️ ggml-org（llama.cpp 上游，非 Z.ai） | **18.2 GB**（`Q4_K`） | — | 31.8 GB | — |
| [ggml-org/…Nemotron-3.5-Lightning-30B-A3B-GGUF](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF) | ⚠️ ggml-org（但 NVIDIA 官方 card 主动链接它） | **25.4 GB** | — | 35.0 GB | 65.9 GB（另有 NVFP4 变体 22.5 GB） |

⚠️ **`Qwen/Qwen3.5-27B-GPTQ-Int4` 是个反直觉的例子**：它 **30.2 GB** 反而只比同模型的 FP8 版（30.9 GB）小 0.7 GB。原因在 dtype 普查里看得很清楚——它有 **10.7B 参数仍是 BF16**（只有 17.1B 走 INT4 打包）。⛔ **「INT4」这个标签不保证体积是 BF16 的四分之一**，必须看实测。

## 2. 部署包络对照表

### 2.1 判据（⛔ 每个 ✅ / ❌ 都由这一条产生，不看它就不要读下面的表）

令名义显存总量为 $V$（GB）。本文要求 $W + \mathrm{KV}(30\mathrm{K}) \le 0.88 \, V$，其中 $W$ 是 §1 的**实测权重体积**，$\mathrm{KV}(30\mathrm{K})$ 是 §1.1 公式算出的 30K 上下文 KV cache（FP16）。系数 **0.88** 的来源：vLLM 默认 `gpu_memory_utilization = 0.92`，即 torch 只能用 $0.92V$；其中还要留激活、CUDA graph、NCCL 通信缓冲，本文按 $0.04V$ 估，于是权重 + KV 的预算是 $0.88V$。

**与 [hardware_availability.md](./hardware_availability.md) §3.1 的关系**：那里用的是单参数捷径 $P_{\max} = V \times 0.88 / b$（$b = 0.57$ B/参，实测锚点区间 0.55–0.62），把 KV **也压进了 0.88 里**。本文把 KV **显式扣出来**，故本文在长上下文格子上**更保守**；⛔ 两者不矛盾，是同一口径的粗/细两档。4-bit 系数 0.57 在本文**只用于没有官方量化件的模型**（表中标 `(估)`）；凡有实测量化件的一律用实测值。实测校准：Qwen3-235B 的官方 `Q4_K_M` 为 142.2 GB ÷ 235.1B = **0.605 B/参**；Qwen3-32B-AWQ 为 19.3 ÷ 32.8 = **0.589 B/参**——均落在 0.55–0.62 区间内，该系数成立。

**这个判据能复现三处官方数字，可信度不是自证**：

| 官方说法 | 本文判据的计算 | 是否一致 |
| :-- | :-- | :-- |
| gpt-oss-120b card：「fit into a single 80GB GPU」 | 65.2 + 2.1 = 67.3 ≤ 80 × 0.88 = 70.4 | ✅ |
| GLM-4.5 card：BF16「H100 × 16 / H200 × 8」 | 716.7 + 10.5 = 727.2，需 ≥ 826 GB 名义 ⇒ 16×80 = 1280 ✅ / 8×141 = 1128 ✅；⛔ 8×80 = 640 ❌ | ✅ 完全对上 |
| Nemotron-3.5-Lightning card：「1× H100 80GB」且 256K 为 memory-bound | 65.8 + 1.5 = 67.3 ≤ 70.4 | ✅ |

⛔ **一条反向实测必须一起带走**：[hardware_availability.md](./hardware_availability.md) §3.4 记录了官方仓库 issue 报告 **DeepSeek-R1-W8A8 在 2×8×64 GB（1024 GB）上 OOM**，⛔ 而按本文判据它装得下。**说明真实常驻开销比 0.88 更重，本文在贴边格子上偏乐观**。表里凡标 贴边的格子都不要据以选型。

### 2.2 单卡档

| 包络 | 预算 $0.88V$ | 能跑（4-bit 档，括号内为实测体积 GB） | 能跑（非 4-bit 档：原生精度或官方 FP8 件） |
| :-- | ---: | :-- | :-- |
| **1×24 GB**（RTX 5090D V2 / 4090D，中国合法在售） | 21.1 | **GLM-4.7-Flash Q4_K（18.2）= 31.2B 总参**（⚠️ 非官方件）· Qwen3-30B-A3B（17.4 估）· North-Mini-Code-1.0（17.4 估）· Mistral-Small-3.2-24B（13.7 估）· phi-4（8.4 估）· Ministral-3-14B（7.9 估）· gemma-4-12B（6.8 估）· Qwen3-8B Q4_K_M（**5.0** 官方） | **gpt-oss-20b（13.8，原生 MXFP4，21B 总参）** · Ministral-3-8B-Instruct-2512 FP8（10.4）· Falcon-H1R-7B-FP8（8.4）· Qwen3-8B BF16（16.4）· Ling-3.0-tiny（15.8）· DeepSeek-R1-Distill-Qwen-7B（15.2） |
| **1×32 GB**（RTX 5090 非中国版 / 昇腾 910B4） | 28.2 | **Qwen3.6-35B-A3B NVFP4（23.4）= 36B 总参** · Qwen3.6-27B NVFP4（21.9，⚠️ 21.9 + KV 7.3 = 29.2 **超预算 1 GB**）· Nemotron-3.5-Lightning NVFP4（21.6 + 1.5 = 23.1 ✅）· Qwen3-32B AWQ（19.3 + 7.3 = 26.6 ✅）· gemma-4-31B QAT w4a16（权重 23.3 ✅，但 KV 上界 27.5 会把它顶出预算——**该上界对滑窗模型严重高估，实际大概率可跑，本文无实测不下判断**） | **gpt-oss-20b（13.8）**；纯 BF16 档仍只到 8B 级 |
| **2×24 = 48 GB** | 42.2 | **Kimi-Linear-48B-A3B（27.9 估）= 49B 总参** · Nemotron-Super-49B（28.5 估）· Qwen3.5-27B-GPTQ-Int4（**30.2** 官方） | **Qwen3-32B-FP8（34.3，⚠️ +7.3 = 41.6 极贴边）= 32.8B 总参** · Qwen3-Coder-30B-A3B-FP8（31.2 + 2.8 = 34.0 ✅，更稳）· Qwen3.6-27B-FP8（30.9）· Ministral-3-14B BF16（27.9）· phi-4 BF16（29.3）；Mistral-Small-3.2-24B BF16（48.0）**装不下** |
| **1×64 GB**（昇腾 910B / 壁仞 BR100） | 56.3 | **Qwen3-Coder-Next Q4_K_M（48.4 官方）= 79.7B 总参**（本档上限）· Qwen3-Next-80B-A3B（46.2 估）· Llama-3.3-70B（39.9 估）· gemma-4-31B QAT（23.3 + KV 上界 27.5 = 50.8 ✅） | **Qwen3.6-35B-A3B-FP8（37.5 + 2.3 = 39.8）= 36B 总参**（本档上限）· Mistral-Small-3.2-24B BF16（48.0 + 4.6 = 52.6）· Devstral-Small-2507 BF16（47.1）· Magistral-Small-2509 BF16（48.0） |
| **1×80 GB**（H100 / A100 80G） | 70.4 | **gpt-oss-120b（65.2）= 117B 总参** —— 官方逐字背书 · GLM-4.5-Air（62.7 估）· Llama-4-Scout（62.1 估）· ⚠️ Mistral-Small-4-119B NVFP4（70.8 + 0.6 = 71.4，**超预算 1 GB**；`gpu_memory_utilization=0.92` 下可过） | **gpt-oss-120b（65.2，原生 MXFP4）= 117B**（本档上限）· Nemotron-3.5-Lightning BF16（65.8，官方明示 1× H100）· Nemotron-3-Nano-30B（63.2）· GLM-4.7-Flash BF16（62.4）· granite-4.0-h-small（64.4）· North-Mini-Code-1.0（61.0）· Falcon-H1-34B（67.3）· Yi-1.5-34B（68.8）；⛔ **Qwen3-32B BF16（65.5 + KV 7.3 = 72.8）装不下**；Qwen-AgentWorld-35B-A3B（69.3 + 2.3 = 71.6）**也差 1.2 GB 装不下** |
| **1×96 GB**（H20 / RTX PRO 6000 / 昇腾 950DT） | 84.5 | **Ling-3.0-flash-int4（77.0 官方）= 127.5B 总参**（本档上限）· Ling-3.0-flash-fp4（70.4）· Mistral-Small-4-119B NVFP4（70.8）· Qwen3.5-122B-A10B（71.2 估） | **Qwen3-Coder-Next-FP8（80.4 + 2.8 = 83.2，⚠️ 极贴边）= 79.7B 总参**（本档上限）· Qwen3.6/3.5-35B-A3B BF16（71.9）· Qwen3-32B BF16（65.5）· Baichuan-M2-32B（65.5）· DeepSeek-R1-Distill-Qwen-32B（65.5） |

### 2.3 多卡档

| 包络 | 预算 $0.88V$ | 能跑（4-bit 档） | 能跑（非 4-bit 档：原生精度或官方 FP8 件） |
| :-- | ---: | :-- | :-- |
| **2×64 = 128 GB** | 112.6 | Ling-3.0-flash-int4（77.0）· Ling-3.0-flash-fp4（70.4）；⛔ Baichuan-M3-235B GPTQ-INT4（124.5）与 Step-3.7-Flash NVFP4（124.4）**均超预算** | Kimi-Linear-48B BF16（98.2 + 0.9 = 99.1）· Nemotron-Super-49B（99.7）；⛔ **GLM-4.5-Air-FP8 的权重 112.6 正好等于预算，加 KV 5.3 后超 5.3 GB，装不下**；Mistral-Small-4-119B FP8（120.9）超 |
| **2×80 = 160 GB** | 140.8 | Baichuan-M3-235B GPTQ-INT4（**124.5** 官方）= 235B 总参 · Step-3.7-Flash NVFP4（124.4）= 201B · MiniMax-M2.x（130.5 估）= 229B · command-a-plus（124.8 估）= 219B | Mistral-Small-4-119B FP8（120.9）· Mistral-Medium-3.5-128B FP8（133.6）；⛔ Llama-3.3-70B BF16（141.1 + 9.2）**装不下** |
| **4×64 = 256 GB** | 225.3 | Qwen3-235B-A22B Q4_K_M（**142.2** 官方）= 235B · GLM-4.7→4bit（201.2 估）= 353B · Hy3（170.4 估）= 299B · **DeepSeek-V4-Flash（159.6 原生）= 284B** | Llama-3.3-70B BF16（141.1）· Qwen2.5-72B（145.4）· Qwen3-Coder-Next BF16（159.4）· Qwen3-Next-80B BF16（162.7）· Llama-4-Scout BF16（217.3）· Command A 2025 BF16（222.1）；⛔ **GLM-4.5-Air BF16（220.9 + 5.3 = 226.2）与 command-a-plus-FP8（225.0 + 3.7 = 228.7）都差 1–4 GB 装不下**——这两个正是「按权重看似刚好、加 KV 就爆」的典型 |
| **4×80 = 320 GB** | 281.6 | Qwen3-Coder-480B（273.6 估）= 480B · Llama-3.1-405B（231.4 估）· Qwen3.5-397B-A17B（229.7 估） | MiniMax-M2/M2.5/M2.7 FP8（230.1）· Mistral-Large-2411 BF16（245.2）· Ling-3.0-flash BF16（255.0）；⛔ Hy3-FP8（299.9）超 |
| **8×64 = 512 GB**（1 台 Atlas 800I A2 = 8×64） | 450.6 | GLM-5.x（429.2 估）= 753B · **Mistral-Large-3 NVFP4（403.1 官方）= 675B** · Llama-4-Maverick FP8（416.8） | Hy3-FP8（299.9 + 9.2 = 309.1）· GLM-4.7-FP8（354.9 + MTP 7.2 + KV 10.5）· GLM-4.5-FP8（361.3 + 10.5 = 371.8）· Step-3.7-Flash BF16（402.7）· command-a-plus BF16（437.5 + 3.7 = 441.2，⚠️ ratio 0.98 极贴边） |
| **8×80 = 640 GB**（标准 H100 节点） | 563.2 | 同上；⛔ Kimi-K2-Thinking INT4（594.2）**超预算 31 GB**，需 8×96 或 8×H200 | Llama-4-Maverick FP8（416.8）· Qwen3-235B BF16（470.2）· Llama-3.1-405B-FP8（487.2）；⛔ **DeepSeek-V3/V3.2 FP8（689.5）装不下** |
| **8×96 = 768 GB**（8×H20 / 8×950DT） | 675.8 | Kimi-K2-Thinking INT4（594.2 + 2.0 = 596.2）；⛔ DeepSeek-V4-Pro（864.7 原生）超 | ⛔ Mistral-Large-3 FP8（权重 681.5）**超 5.7 GB**；DeepSeek-V3.2 FP8（689.5 + 2.0 = 691.5）**超 15.7 GB**——**两者都是极贴边的「差一点」，不要当成能跑**；若丢掉 DeepSeek 的 MTP 模块（约 14 GB）则 V3.2 转为可能，但本文按仓库完整主权重集计，不做这种裁剪假设 |
| **8×141 = 1128 GB**（8×H200 单节点） | 992.6 | 几乎全部 4-bit 档 | **DeepSeek-V3.x / R1 FP8（689.5）· GLM-5.x-FP8（756.2）· Mistral-Large-3 FP8（681.5）· Intern-S1-Pro FP8（919.0）· Qwen3-Coder-480B BF16（960.3）· Llama-3.1-405B BF16（811.7）· Qwen3.5-397B BF16（806.8）· MiniMax-M1 BF16（912.2）**；⛔ Kimi-K2 FP8（1029.2）**装不下** |
| **16×64 = 1024 GB**（2 台 Atlas 800I A2） | 901.1 | GLM-5.x-FP8（756.2）· DeepSeek-V4-Pro（864.7 原生） | **DeepSeek-V3.x FP8（689.5）**——这一格有**昇腾官方部署证据**，见 [hardware_availability.md](./hardware_availability.md) §4.5（⚠️ 官方口径是 W8A8，且同节点有过 OOM 报告）· GLM-5-FP8（756.2）· Mistral-Large-3 FP8（681.5）；Intern-S1-Pro（919.0）超 |
| **16×80 = 1280 GB** | 1126.4 | — | Kimi-K2-Instruct FP8（1029.2）· GLM-4.7 BF16（716.7）；⛔ Mistral-Large-3 BF16（1352.0）超 |
| ⛔ **> 1280 GB 才装得下的** | — | ⛔ Kimi-K3 MXFP4（1560.9，需 ≥ 1774 GB 名义）· Qwen3.8-FP8（2496.1，需 ≥ 2836 GB） | ⛔ **Mistral-Large-3 BF16（1352.0）· GLM-5.x BF16（1506.7）· Kimi-K3（1560.9）· Qwen3.8 BF16（4892.4，需 ≥ 5560 GB ≈ 70 张 80 GB 卡）** |

⛔ **两条对「MoE 更省显存」的直接反驳**：

1. ⛔ **DeepSeek-V4-Flash 有 284B 总参但只激活 13B**，原生 FP4+FP8 混合下 **159.6 GB**——它的**显存**和一个 80B BF16 模型同级，⛔ 但绝不是和 13B 同级。
2. ⛔ **Kimi-K3 有 2.8T 总参、只激活 104B，且原生就是 MXFP4**，⛔ 权重仍是 **1560.9 GB**：需要 **≥ 1774 GB 名义显存**，即至少 **16×141 GB H200 或 28×64 GB 昇腾**。稀疏只降算力，一点不降常驻显存。

## 3. ⛔ 原生量化模型清单（它们没有 BF16 配置）

⛔ **下表的模型，官方发布的**就是**量化权重。⛔ 给它们报「BF16 显存」等于报一个官方从未发布的配置。**

| 模型 | 原生精度 | 权重实测 | 依据（逐字） | ⚠️ 有无更高精度路径 |
| :-- | :-- | ---: | :-- | :-- |
| **gpt-oss-120b / 20b / safeguard-120b / safeguard-20b** | **MXFP4**（MoE 权重） | 65.2 / 13.8 / 65.2 / — GB | card：「The models were post-trained with MXFP4 quantization of the MoE weights」；并明说「**All evals were performed with the same MXFP4 quantization**」 | ⛔ 官方无 BF16 版；社区有 `unsloth/gpt-oss-20b-BF16` 反量化件（非官方） |
| **DeepSeek-V3 / V3-0324 / R1 / R1-0528 / V3.1 / V3.1-Terminus / V3.2 / V3.2-Exp / V3.2-Speciale** | **FP8**（e4m3，block 128×128，dynamic） | 688.6–689.5 GB | V3 card 逐字：「Since FP8 training is natively adopted in our framework, **we only provide FP8 weights**」 | 官方提供 `fp8_cast_bf16.py` 转换脚本；⛔ 转出约 1.37 TB，且非官方发布件 |
| **DeepSeek-V4-Pro / V4-Flash / V4-Flash-0731** | ⛔ **FP4 + FP8 混合** | 864.7 / 159.6 / 166.9 GB | card 脚注逐字：「FP4 + FP8 Mixed: **MoE expert parameters use FP4 precision; most other parameters use FP8**」 | 另有 `-Base` 仓库标 **FP8 Mixed**；⛔ 无 BF16 |
| **Kimi-K2-Instruct / -0905** | **FP8** | 1029.2 GB | `config.json`：`quant_method: fp8, weight_block_size [128,128]` | ⛔ 未见官方 BF16 |
| **Kimi-K2-Thinking** | ⛔ **INT4 权重（QAT）** | 594.2 GB | card §4 逐字：「applying INT4 weight-only quantization to the MoE components… **All benchmark results are reported under INT4 precision**」 | card 明说可用 `compressed-tensors` 官方库解包成 FP8/BF16；⛔ 但官方不发那个件 |
| **Kimi-K3** | ⛔ **MXFP4 权重 / MXFP8 激活（QAT）** | 1560.9 GB | card §4 逐字：「Kimi K3 applies quantization-aware training from the SFT stage onward, using **MXFP4 weights with MXFP8 activations**」；规格表 `Quantization` 行同 | ⛔ 无 |
| **MiniMax-M2 / M2.1 / M2.5 / M2.7** | **FP8**（block 128×128，dynamic） | 230.1 GB | `config.json`：`quant_method: fp8, fmt: float8_e4m3fn` | ⛔ 未见官方 BF16 |
| **Mistral-Large-3-675B-Instruct-2512** | **FP8** | 681.5 GB | 体积 681.5 ÷ 675B ≈ 1.01 B/参 ⇒ FP8；card 推荐「in FP8 or NVFP4」 | 另有 `mistralai/Mistral-Large-3` 仓库为 BF16（1352.0 GB） |
| **Mistral-Small-4-119B-2603** | **FP8**（static） | 120.9 GB | `config.json`：`quant_method: fp8, activation_scheme: static` | 有官方 NVFP4（70.8 GB）；⛔ 未见 BF16 |
| **Mistral-Medium-3.5-128B** | **FP8**（static） | 133.6 GB | 同上 | ⛔ 未见 |
| **Ministral-3-8B-Instruct-2512** | **FP8** | 10.4 GB | 同上 | **有**官方 `-BF16` 仓库 |
| **Intern-S1-Pro** | **FP8** | 919.0 GB | HF 元数据报 `quant_method: fp8` | 有官方 `internlm/Intern-S1-Pro-BF16` 仓库 |
| **Falcon-H1R-7B-FP8** | **FP8**（ModelOpt） | 8.4 GB | `quant_method: modelopt` | 同系列有 BF16 版 |

**反面例子（⛔ 不属本清单）**：Qwen 全系、GLM 全系、gemma 全系、Llama 全系（除 FP8 变体）、Cohere、Ling、Hy3、Step、Baichuan、Nemotron 的**主仓库都是 BF16**，FP8 / INT4 / NVFP4 是**另开仓库**的官方量化件。对它们讲「BF16 显存」是合法的。

## 4. 官方最小部署配置汇总（⛔ 含「官方未给」的如实记录）

**分三档记录**：**A = 官方给了明确的卡型 × 卡数或显存下限**；**B = 官方只给了 `--tp N` 之类的示例命令**（⚠️ 那是「我们这么跑过」，⛔ 不是「最少要这么多」）；**C = card 内未给任何部署硬件信息**。

### 4.1 A 档：有明确硬件门槛（逐字可引）

| 模型 | 官方原文（逐字） | 来源 |
| :-- | :-- | :-- |
| **gpt-oss-120b** | 「for production, general purpose, high reasoning use cases that **fit into a single 80GB GPU** (like NVIDIA H100 or AMD MI300X) (117B parameters with 5.1B active parameters)」；另：「MXFP4 quantization… making `gpt-oss-120b` **run on a single 80GB GPU**」 | [model card](https://huggingface.co/openai/gpt-oss-120b) |
| **gpt-oss-20b** | 「the `gpt-oss-20b` model **run within 16GB of memory**」；并称可在 consumer hardware 上微调 | [model card](https://huggingface.co/openai/gpt-oss-20b) |
| **GLM-4.5 / GLM-4.5-Air** | card 内有完整表格。**基础可用档**：GLM-4.5 BF16 = `H100 x 16 / H200 x 8`；GLM-4.5 FP8 = `H100 x 8 / H200 x 4`；GLM-4.5-Air BF16 = `H100 x 4 / H200 x 2`；GLM-4.5-Air FP8 = `H100 x 2 / H200 x 1`。**满 128K 上下文档各翻一倍**：GLM-4.5 BF16 = `H100 x 32 / H200 x 16` 等。⛔ 另有一条硬性前置：「**Server memory must exceed `1T`** to ensure normal model loading and operation」（指主机内存，不是显存） | [model card](https://huggingface.co/zai-org/GLM-4.5) |
| **Mistral-Large-3-675B** | 「[FP8] on **a single node of B200s or H200s**」；「[NVFP4] on **a single node of H100s or A100s**」；并明确「The Mistral Large 3 Instruct FP8 format can be used on **one 8xH200 node**」 | [model card](https://huggingface.co/mistralai/Mistral-Large-3) |
| **Nemotron-3.5-Lightning-30B-A3B** | 规格表逐字：「**Single-GPU Deployment**: 1× H100 80GB (or 1× A100 80GB)」；「**Context Length**: Up to 1M tokens (**for single H100 deployment, we use 256K**)」。并给硬件×上下文矩阵：`1× H100 80GB → 256K (memory-bound)`、`8× H100 TP8+EP → 1M`、`1× GB200 → 1M`、`1× B200 → 1M`。还明说「On a single H100, BF16 is **memory-bound to ~256K**」 | [model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) |
| **Command A+ (05-2026)** | card 内三精度表：BF16 = `4 x B200` / `8 x H100`；FP8 = `2 x B200` / `4 x H100`；W4A4 = `1 x B200` / `2 x H100`。上下文 128K，输出 64K | [model card](https://huggingface.co/CohereLabs/command-a-plus-05-2026-bf16) |
| **Step-3.7-Flash** | 「**Minimum unified memory / VRAM: 120 GB** (e.g., Mac Studio, NVIDIA DGX Station, AMD Ryzen AI Max+ 395)」 | [model card](https://huggingface.co/stepfun-ai/Step-3.7-Flash) |
| **Qwen3-235B-A22B-Instruct-2507**（仅 1M 档） | 「To effectively process a 1 million token context, users will require approximately **1000 GB of total GPU memory**. This accounts for model weights, KV-cache storage, and peak activation memory demands.」 | [model card](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507) |
| **DeepSeek-V3**（官方 demo 口径） | 官方 DeepSeek-Infer demo 命令逐字：`torchrun --nnodes 2 --nproc-per-node 8 generate.py … --config configs/config_671B.json` ⇒ **16 卡两节点**。⛔ card 未给单卡显存下限 | [model card](https://huggingface.co/deepseek-ai/DeepSeek-V3) |
| **Ling-3.0-flash** | 「On **80GB cards (H100 / H800)** use `--tp 8` with the same flags」；另给 `--tensor-parallel-size 4` 的 vLLM 示例 | [model card](https://huggingface.co/inclusionAI/Ling-3.0-flash) |
| ⚠️ **gemma-4 全系**（只到定性档） | 「targeting deployment scenarios from **mobile and edge devices (E2B, E4B)** to **consumer GPUs and workstations (12B, 26B A4B, 31B)**」 | [model card](https://huggingface.co/google/gemma-4-31B-it) |

### 4.2 B 档：只有示例命令，⛔ 没有最小门槛

| 模型 | 官方示例（逐字） | ⛔ 为什么不算最小配置 |
| :-- | :-- | :-- |
| **GLM-5 / GLM-5.1 / GLM-5.2** | `vllm serve zai-org/GLM-5 --tensor-parallel-size 8 --gpu-memory-utilization 0.85`；`sglang … --tp-size 8` | ⛔ 未说卡型，8 张 40 GB 与 8 张 141 GB 都能写成 `--tp 8` |
| **GLM-4.7 / GLM-4.7-FP8** | `vllm serve zai-org/GLM-4.7-FP8 --tensor-parallel-size 4`；`sglang … --tp-size 8` | ⛔ 同上；且 4.7 的 card 已**不再带 4.5 那张硬件表**——官方信息量在这一代是**倒退**的 |
| **Qwen3.5 / Qwen3.6 / Qwen3.8 全系** | 「create an API endpoint with maximum context length 262,144 tokens using **tensor parallel on 8 GPUs**」+ `--tp-size 8` / `--tensor-parallel-size 8` | ⛔ 8 卡是给满 256K 上下文的示例，不是下限。card 只给降级指引：「If you encounter out-of-memory (OOM) errors, consider **reducing the context window**」 |
| **Qwen3-Next-80B-A3B** | 「maximum context length 256K tokens using **tensor parallel on 4 GPUs**」+ `--tp-size 4` | ⛔ 同上 |
| **Mistral-Small-4-119B-2603** | `vllm serve … --max-model-len 262144 --tensor-parallel-size 2 --gpu_memory_utilization 0.8` | ⛔ 未说卡型；但 `-tp 2` 是本表最低的官方示例之一 |
| **DeepSeek-V3.2-Exp** | `python -m sglang.launch_server … --tp 8 --dp 8 --enable-dp-attention` | ⛔ `--tp 8 --dp 8` 在 dp-attention 语义下的实际卡数取决于框架版本，本文不替官方解释 |
| **Tencent Hy3 / Hy3-FP8** | `--tensor-parallel-size 8` / `--tp-size 8` | ⛔ 无卡型 |
| **Baichuan-M3-235B** | `--tensor-parallel-size 8` | ⛔ 无卡型 |
| **Step-3.7-Flash**（除 A 档那条 120 GB 外） | `--tensor-parallel-size 8` / `4` | — |

### 4.3 ⛔ C 档：card 内查不到任何部署硬件信息

⛔ **以下模型的 model card 里没有卡型、卡数或显存下限**（均已逐字检索 `GPU` / `VRAM` / `H100` / `H200` / `A100` / `MI300` / `memory` / `tp` / `node` 等模式）：

| 模型 | ⛔ card 内的替代说法 |
| :-- | :-- |
| **Kimi-K2-Instruct / -0905 / K2-Thinking / K3** | ⛔ 只写「Deployment examples can be found in the **Model Deployment Guide** (`docs/deploy_guidance.md`)」或链向 vLLM recipes / SGLang cookbook。card 本身不给硬件门槛 |
| **MiniMax-M2 / M2.1 / M2.5 / M2.7** | ⛔ 只有一句定性：「Simpler capacity planning with smaller per-request memory and steadier tail latency」 |
| **granite-4.0-h-small** | ⛔ card 只写**训练**用的 GB200 NVL72 集群，不提推理硬件 |
| **Qwen3 / Qwen2.5 的 32B 及以下档** | ⛔ card 给的 `--tp 8` 示例是给 235B / 480B 那一档的；32B 及以下没有独立的最小配置说明 |
| ⛔ **Llama 3.1 / 3.2 / 3.3 / Llama 4 全系** | ⛔ **仓库 gated（`gated: manual`），本轮无法读取 `config.json` 与 card 正文（HTTP 401）**。文件体积可从 API 拿到（已入 §1 表），但 context、KV 结构、部署建议**均未核验**——**这是「未核验」，不是「官方未给」，两者必须分开说** |
| ⛔ **gemma-2 / gemma-3 全系** | ⛔ 同上（`gated: manual`），context 与部署信息未核验 |
| **Command A（2025 版）** | ⛔ `gated: auto`，card 正文本轮未取 |
| **Intern-S1-Pro** | ⛔ 本轮未取到明确硬件说明 |
| **Mistral-Medium-3.5-128B / Ministral-3 全系 / Magistral-Small / Devstral** | ⛔ 本轮未见明确硬件门槛 |
| **Kimi-Linear-48B-A3B / North-Mini-Code-1.0 / Falcon-H1 系 / Yi / phi-4 / internlm3 / Baichuan-M2 / Nemotron-3-Nano / MiniMax-M1 / MiniMax-Text-01 / Ling-3.0-tiny** | ⛔ 未见 |

**统计**：**A 档 11 个系列**（gpt-oss、GLM-4.5、Mistral-Large-3、Nemotron-3.5、Command A+、Step-3.7、Qwen3-235B（仅 1M 档）、DeepSeek-V3（demo 口径）、Ling-3.0、gemma-4（仅定性））；**B 档 9 个系列**；⛔ **C 档 ≥ 14 个系列 / 家族查不到官方最小部署配置**，⛔ 其中 **Llama 与 gemma 两大家族是因为仓库 gated 而无法核验**，不是「官方没写」。

## 5. 许可证可商用性

| 分档 | 模型 | ⚠️ 说明 |
| :-- | :-- | :-- |
| **Apache-2.0 / MIT（OSI 认可，无附加限制）** | Qwen2.5 / Qwen3 / Qwen3.5 / Qwen3.6 全系（Apache-2.0，⚠️ **Qwen2.5-72B 除外**）· **gemma-4 全系**（Apache-2.0）· **Command A+ 05-2026**（Apache-2.0）· Tencent Hy3（Apache-2.0）· Step-3.7-Flash（Apache-2.0）· Baichuan-M2 / M3（Apache-2.0）· granite-4.0（Apache-2.0）· Intern-S1-Pro（Apache-2.0）· Mistral 2512/2603 世代多数（Apache-2.0）· Yi-1.5（Apache-2.0）· internlm3（Apache-2.0）· MiniMax-M1（Apache-2.0）· **gpt-oss 全系**（Apache-2.0）· **DeepSeek V3.x / R1 / V4 全系**（MIT）· **GLM-4.5/4.6/4.7/5/5.1/5.2 全系**（MIT）· Ling-3.0 全系（MIT）· Kimi-Linear（MIT）· phi-4（MIT） | 这一档是**真正可商用**的。两处值得注意的**放开**：gemma-4 从 Gemma Terms 改成 Apache-2.0；Command A 从 CC-BY-NC 改成 Apache-2.0 |
| ⚠️ **自定义许可（多数允许商用，但有附加条款，需逐条读）** | ⛔ **Qwen3.8-2.4T-A95B**（`license_name: qwen3.8-max`——**Qwen 旗舰这一代脱离了 Apache-2.0**）· Kimi-K2 系（`modified-mit`）· **Kimi-K3**（`kimi-k3` 自定义）· MiniMax-M2 系（自定义）· **Nemotron 全系**（`openmdw-1.1` / NVIDIA Open Model License）· Falcon 全系（Falcon LLM License）· Qwen2.5-72B（Qwen License）· Mistral-Medium-3.5（自定义）· MiniMax-Text-01（自定义）· glm-4-9b（GLM-4 许可） | ⛔ **不要因为「开放权重」就假定可商用**。`modified-mit` / OpenMDW 一般允许商用但加了署名或负责任使用条款；Falcon License 与 Qwen License 有额外限制 |
| ⛔ **社区许可（有 MAU 阈值 / 命名要求）** | Llama 3.1 / 3.2 / 3.3 / Llama 4 全系 | ⛔ Meta 社区许可含月活阈值与「Built with Llama」署名等要求 |
| ⛔ **Gemma Terms（source-available，非 OSI）** | gemma-2 / gemma-3 全系 | gemma-4 起已改 Apache-2.0；⛔ 但 2/3 代仍受 Gemma Terms |
| ⛔ **明确不可商用** | ⛔ **Command A（`c4ai-command-a-03-2025`、`command-a-reasoning-08-2025`）= CC-BY-NC-4.0** · **Mistral-Large-Instruct-2411 = MRL（研究许可）** · **Ministral-8B-Instruct-2410 = MRL** · **Codestral-22B-v0.1 = MNPL（非生产许可）** | ⛔ 这四个在任何商业或生产语境下都不能用。尤其 Command A：2026 版已放开成 Apache-2.0，但 2025 版仍是 NC——**同名系列跨代许可完全不同** |

⛔ **一条元事实**：2026 年的许可趋势**不是单向放开**。放开侧：gemma-4、Command A+ 都从受限许可改成 Apache-2.0。⛔ 收紧侧：**Qwen 的 2.4T 旗舰 Qwen3.8 脱离了 Apache-2.0**，改成自定义 `qwen3.8-max` 许可——而同代的 Qwen3.6 / Qwen3.5 中小档仍是 Apache-2.0。**同一厂商内部按规模分档发许可**，选型时不能按「厂商惯例」推断。

## 6. 核验方法、来源与待核验项

### 6.1 核验方法（可复现）

1. **权重体积**：`GET https://huggingface.co/api/models/{id}?blobs=true`，对返回的 `siblings[]` 逐项取 `size`，再**按文件名分类**求和：
   - `primary` = 根目录 `model.safetensors` 或 `model-NNNNN-of-NNNNN.safetensors`（⚠️ Qwen3.5 / 3.6 用的是 `model.safetensors-NNNNN-of-NNNNN.safetensors` 这种非常规命名，⛔ 朴素正则会漏）
   - ⛔ `consolidated*` = Mistral 自家格式的**第二份副本**，⛔ 不计入（除 `Mistral-Large-3` 系列——它**只有** consolidated 格式，此时计入）
   - ⛔ 子目录 `original/`、`metal/` = **同一权重的另一份编码**，⛔ 不计入
   - 独立的 `mtp.safetensors`（GLM 4.6 / 4.7）= 投机解码模块，单列不并入
2. **原生精度**：三重交叉——`config.json` 的 `quantization_config.quant_method` + HF `safetensors.parameters` 的 dtype 普查（`F8_E4M3` / `U8` / `I32` / `BF16` 各占多少）+ model card 原文。⛔ **单看任何一项都会错**：⛔ 例如 DeepSeek-V4-Pro 的 `config.json` 只写 `quant_method: fp8`，而 dtype 普查显示 1572.8B 参数走 `I8` 打包——只有 card 脚注「MoE expert parameters use FP4」能解释这个矛盾。
3. **部署配置**：抓 `README.md` 原文，按 `H100|H200|B200|A100|MI300|GPU|VRAM|memory|tp-size|tensor-parallel|nnodes|single node` 等模式逐行检索，命中行逐字摘录。⛔ 未命中即记 C 档。
4. **KV cache**：从 `config.json` 取 `num_hidden_layers` / `num_key_value_heads` / `head_dim`（或 MLA 的 `kv_lora_rank` + `qk_rope_head_dim`）现算，公式见 §1.1。

### 6.2 ⛔ 待核验与已知缺口

| # | 缺口 | ⛔ 影响 |
| --: | :-- | :-- |
| 1 | ⛔ **Llama 与 gemma-2/3 全系仓库 gated（`gated: manual`）**，`config.json` 与 card 正文返回 HTTP 401 | ⛔ 这两族的 **context、KV 结构、部署建议均未核验**；权重体积可从 API 拿到（可信）。表中 Llama-3.x 的 KV 值标 是按公开架构参数（L80 / kv8 / hd128）**推算**的，未经官方 `config.json` 证实 |
| 2 | ⛔ **HF `createdAt` ≠ 官方发布日** | 已在 §1.1 说明。本轮只对 gemma-4（官方 2026-04-02）、GLM-5（官方 2026-02）、GLM-5.2 开放权重（官方 2026-06-16）做了独立核对，⛔ **其余系列的官方发布日一律未核验**，表中只能读作「不早于该日」 |
| 3 | ⛔ **KV@30K 是上界，不是实测** | ⛔ 滑窗 / 混合注意力模型（gemma 系、gpt-oss、Nemotron-H、Falcon-H1、Qwen3-Next、Kimi-Linear）被**系统性高估**。最极端是 gemma-4-31B 的 27.5 GB——按全局注意力算的，与其局部/全局交错设计不符（card 明写「hybrid attention mechanism that interleaves local sliding window attention with full global attention」）。涉及这几族的包络格子应视为**偏悲观** |
| 4 | ⛔ **DeepSeek-V4 的 KV 无法按常规公式算** | card 称其 CSA + HCA 在 1M 上下文下只用 V3.2 的 **10% KV**；⛔ 本文按 `kv_heads=1, head_dim=512` 的朴素公式给的 2.5 / 3.5 GB **不代表其真实机制**，已标 |
| 5 | ⛔ **Intern-S1-Pro / Mistral-Large-3 / Step-3.7 的总参与 context 缺官方明值** | ⛔ Mistral 的 `consolidated` 格式无 HF `safetensors` 元数据，参数量只能由仓库名（675B）与体积反推；Intern-S1-Pro 无 `safetensors.total` |
| 6 | ⛔ **本文没有一条实机 OOM / 吞吐实测** | ⛔ 全部是**静态容量核算**。而 [hardware_availability.md](./hardware_availability.md) §3.4 已记录一次真实 OOM（DeepSeek-R1-W8A8 在 1024 GB 上），说明贴边格子不可信。**不要拿本文的 ✅ 当部署承诺** |
| 7 | ⛔ **国产卡的实际可跑性未核** | §2 只按显存容量算。⛔ 而 [hardware_availability.md](./hardware_availability.md) §4.6 记录**昇腾不原生支持 FP8**——意味着本文所有「FP8 原生」的格子在昇腾上**需要先转精度**，转完体积翻倍，包络结论随之变。寒武纪 / 摩尔线程 / 海光同理未核。另注意 [hardware_availability.md](./hardware_availability.md) §2.2.2 的提醒：寒武纪 MLU370-X8 与摩尔线程 S4000 的「48 GB」是 LPDDR5 级、昇腾 Atlas 300I Duo 的「96 GB」是 LPDDR4X（408 GB/s）——**容量进得去不等于跑得动** |
| 8 | ⏳ **表中 ⏳ 标记的字段** | ⏳ context / KV 未取到（多因 gated 或 `consolidated` 格式无元数据）。⛔ **未编造任何一个** |
| 9 | ⚠️ **4-bit 档「(估)」格子用的是 0.57 B/参** | 该系数已用两个官方量化件校准（0.589 / 0.605 B/参，见 §2.1）；⛔ 但对**嵌入层不量化**的模型会低估——实测反例：gemma-4-31B QAT w4a16 是 **0.745 B/参**（4.3B 参数留在 BF16）、Nemotron-3.5-Lightning 的 `Q4_K_M` 是 **0.80 B/参**。**小模型的「(估)」格子偏乐观** |

### 6.3 主要来源

全部为一手：**HF Model API**（逐文件 `size`、`safetensors` dtype 普查、`config.json`、`createdAt` / `lastModified`）· **各仓库 model card 原文**（§4 的每条逐字引用均可在对应 card 内检索到）· **官方 blog**（仅用于 §6.2 #2 的三次发布日核对：[Gemma 4 launch](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)、[Gemma 4 Apache-2.0](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html)）。⛔ **未使用任何第三方聚合站、评测榜或博客的显存 / 参数 / 部署数字。**

### 6.4 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 12:30:00 | 建库。探测 145 个 HF 仓库、143 个成功取到权重体积 / dtype 普查 / 架构参数，主表收 141 行；建立 §2 包络判据并用 gpt-oss / GLM-4.5 / Nemotron-3.5 三处官方数字交叉验证；建立 §3 原生量化清单（13 组）与 §4 三档部署配置台账（A 档 11 / B 档 9 / ⛔ C 档 ≥ 14）；记录 9 条待核验缺口 |
