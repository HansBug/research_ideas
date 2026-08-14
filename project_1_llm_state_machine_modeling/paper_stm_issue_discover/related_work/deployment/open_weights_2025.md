# 2025 世代开放权重模型全谱

**核验日**：2026-08-13。**证据级别**：**M** = 官方一手（官方 blog / HF model card / HF API 实测 / `config.json`）· **S** = 二手（媒体、第三方镜像、社区测评）· **I** = 本文推断。

## 时间门（⛔ 先读，否则会误读本表的收录范围）

本表只收 **开放权重首次发布日在 2025-01-01 及以后** 的模型。

1. ⛔ **2024 年发布的一律排除**：Qwen2.5 全系、Llama 3.1 / 3.2 / 3.3、DeepSeek V3 原版（2024-12-25）、Mistral-Large-2411、Falcon3、gemma-2、Codestral-22B、Yi-1.5。它们在 [open_weight_model_compute.md](./open_weight_model_compute.md) §1.2 里有实测体积，本文不重复。
2. ⭐ **但其 2025 年的后续版本纳入**：DeepSeek-V3-0324 / V3.1 / V3.1-Terminus / V3.2-Exp / V3.2 / R1 全系纳入；`Llama-3_3-Nemotron-*`（NVIDIA 在 2025 年基于 Llama 3.3 重新剪枝训练并首次发布权重的模型）纳入。
3. ⚠️ **一个真实的边界案例，本文如实标注而不强行归档**：`microsoft/phi-4` 的 HF 仓库 `createdAt` 是 **2024-12-11**，官方发布也在 2024-12（Azure AI Foundry），⛔ 故 **Phi-4 基座本身不属 2025 世代**；但 **MIT 许可的可下载权重是 2025-01-08 才上 HF 的**（`microsoft/phi-4-gguf` 仓库 `createdAt` = 2025-01-08，**M**）。⇒ 本表把 **Phi-4 基座列为 2024，把 Phi-4 的五个 2025 衍生型（mini / multimodal / reasoning / reasoning-plus / mini-reasoning / mini-flash-reasoning）列为 2025**。
4. ⛔ **本表不收**：hosted-only 模型（Mistral Medium 3 的 2025 版、DeepSeek API 线）、纯视觉 / 语音 / embedding / reranker 模型。⚠️ 多模态 LLM（Gemma 3、Mistral Small 3.1/3.2、Voxtral、Step-3、Intern-S1、Command A Vision）**收录但标注**，因为纯文本负载下其 vision tower 是常驻但不产出价值的权重。

## 字段口径（⛔ 每个数字的确切含义）

| 字段 | 本文的确切含义 | ⚠️ 已知局限 |
| :-- | :-- | :-- |
| **官方发布日** | 官方 blog / 官方新闻稿 / model card 内的 changelog 日期 | ⭐ **与 HF `createdAt` 分列两栏，因为两者系统性不等** |
| **HF 建仓日** | HF API `createdAt`，即权重首次上传时间戳 | ⛔ **它不是发布日**。本轮实测四种情形：Llama 4 的 HF 建仓 **早于**官方公告 3–4 天；Gemma 3 的 4B 档早 **20 天**；Qwen3 早 2 天；Seed-OSS **同日**。⇒ 该字段是发布日的**下界** |
| **权重实测体积** | HF API 逐文件 `size` 合计，仅主权重集，单位 GB = $10^9$ 字节 | ⛔ **已剔除三类重复计数**：Mistral 的 `consolidated.safetensors` + 分片双份（不剔会得到 94.3 GB 这个虚高一倍的数）、GLM / ERNIE 的独立 MTP 模块、gpt-oss 的 `original/` 与 `metal/` 副本 |
| **总参 / 激活参** | 优先 card 明写值，否则 HF `safetensors.total` | ⛔ **显存按总参算，decode 速度看激活参**。MoE 全部专家权重须常驻，稀疏只降算力 |
| **原生精度** | 三重交叉：`config.json` 的 `quantization_config.quant_method` + HF safetensors dtype 普查 + card 原文 | ⛔ 单看任何一项都会错 |
| **context** | `config.json` 的 `max_position_embeddings` | ⚠️ **凡官方 blog 写「128K」而 config 写 40960 的，那个 128K 是 YaRN 外推**，不是原生窗口。Qwen3 全档就是这个情形 |

## 0. 一句话结论

⭐ **2025 世代对本项目的真实优势不是能力，是「配套齐全」**：官方量化件、官方 GGUF、vLLM/SGLang 稳定路径、社区量化件、公开 benchmark 数字，2025 世代基本都有；而 2026 世代的新模型里相当一部分只有 BF16 主仓库、只有 Blackwell 验证过的三方 NVFP4 件、或者根本没有 AA 分数。

**分档的四个答案**（⛔ 每个都带体积与件的归属）：

1. ⭐ **单卡 24 GB（T1 下沿，权重 + KV 预算 21.1 GB）**：**`openai/gpt-oss-20b` 13.8 GB + KV 1.4 = 15.2 GB**（21B / 3.6B 激活，原生 MXFP4 作者件，Apache-2.0，**余 5.9 GB**）。⚠️ 参数量更大的 `google/gemma-3-27b-it-qat-q4_0-gguf` **17.2 GB**（27B，**官方 QAT 件**）大概率也装得下，⛔ **但它的 KV@30K 未核**（滑窗 / 全局交错注意力，按全局算会严重高估），⇒ ⛔ **不可当成已验证的选项**。**`Qwen3-32B-AWQ` 装不进 24 GB**：19.3 + KV 7.3 = **26.6 GB**，超预算 5.5 GB，⇒ 它属下一档。
2. ⭐ **单卡 84–96 GB（T1 上沿）**：`openai/gpt-oss-120b` **65.2 GB + KV 2.1 = 67.3 GB**（117B / 5.1B 激活，原生 MXFP4，作者件，Apache-2.0），**官方 card 逐字背书「fit into a single 80GB GPU (like NVIDIA H100 or AMD MI300X)」**，⇒ 最低落进 **84 GB** 一档（余 6.6）。⛔ **但必须带走一条代价**：MXFP4 在 Hopper 上走 W4A16 回退，**省显存不省算力**（§3.3 有 vLLM 源码三条逐字）。⚠️ 同档另有 `Seed-OSS-36B` **72.3 GB**（⭐ **原生 512K context、RULER-128K 94.6 为本表最高**、BF16 无格式代价），⇒ **要长上下文就选它，要参数量就选 gpt-oss-120b。**
3. ⭐ **4×H200（权重预算 487 GB）**：`Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` **236.4 GB**（作者件、FP8 在 Hopper 原生、Apache-2.0、余量 250 GB）。若要更大，`zai-org/GLM-4.6-FP8` **354.9 GB**（MIT，作者件）。⛔ **`Qwen3-Coder-480B-A35B-Instruct-FP8` 是 482.1 GB，距 487 GB 只剩 4.9 GB，⛔ 不得据以选型。**
4. ⭐ **T5 国产 1024 GB 节点 / T4b 高档**：`moonshotai/Kimi-K2-Thinking` **594.2 GB**（1T 总参 / 32B 激活，**原生 INT4 QAT，作者件**）。⛔ 它是 2025 世代里「1T 级模型 + 单节点装得下」的唯一组合——同族的 `Kimi-K2-Instruct` FP8 是 **1029.2 GB**，⛔ 超出 1024 GB 节点的 0.88 预算（901 GB）。

⛔ **三条方向相反的事实，必须一起带走**：

1. ⛔ **2025 世代在 AA v4.1.1 上的分数很低，⛔ 且大多数还只是「估计值」。** ⭐ **本表 38 个有 v4.1.1 分的条目里，只有 12 个是 AA 实测，其余 26 个页面标 `Estimate (independent evaluation forthcoming)`——即 AA 并未真跑过。** 实测且最高的是 `GLM-4.7` = **34**；`gpt-oss-120b (high)` = 24 · `Llama 4 Maverick` = 14 · `Mistral-Large-3` = 16 · `Qwen3-Next-80B-A3B` = 17 · `Qwen3-32B` = 11 · `Gemma 3 27B` = 7。**几乎全部 DeepSeek、全部 Nemotron、全部 Kimi / MiniMax 都是估计值。** 对照闭源锚点 `Claude Opus 5 (max)` = **63.05**。⇒ **选 2025 世代是拿能力换生态成熟度，不是免费的。** 逐模型分数与陷阱见 §1.4。
2. ⛔ **「2025 世代生态更成熟」这个前提本身要分模型看。** Qwen3 / Gemma 3 / gpt-oss / Mistral Small 3.x / DeepSeek R1 确实齐全；⛔ 但 `Qwen3-Next`（混合注意力）、`Kimi-Linear`（线性注意力）、`Nemotron-*-v2`（Mamba 混合层）、`DeepSeek-V3.2`（DSA 稀疏注意力）这四类 2025 年新架构在推理引擎上的路径**并不比 2026 模型成熟**，因为它们各自引入了新算子。
3. ⛔ **官方量化件的覆盖极不均匀。** Qwen 一家就发了 FP8 + AWQ + GGUF 三条线；⛔ 而 **DeepSeek 官方在 2025 年零个 4-bit 件**、**Z.ai（zai-org）现代世代零个 4-bit 件**、**moonshotai 零个独立量化仓库**（INT4 直接在主仓库里）。⇒ 若部署条件要求 4-bit，这三家只能走三方件。

## 1. 全谱表（按发布时间降序）

### 1.1 ⛔ 先读：官方发布日与 HF 建仓日系统性不等

⭐ **本轮亲自核到四条官方发布日，与 HF `createdAt` 逐条比对，结论是「HF 建仓日普遍早于官方公告」**（**M**）：

| 模型 | 官方发布日（含来源） | HF 建仓日 | 差 |
| :-- | :-- | :-- | --: |
| **Llama 4 Scout / Maverick** | **2025-04-05** —— [Meta 官方 blog](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) | 2025-04-01（Maverick）/ 2025-04-02（Scout） | ⭐ **早 3–4 天** |
| **Qwen3 全档** | **2025-04-29** —— [Qwen 官方 blog](https://qwenlm.github.io/blog/qwen3/) | 2025-04-27（BF16）/ 2025-04-28（FP8） | 早 1–2 天 |
| **Gemma 3 全档** | **2025-03-12** —— [Google 官方 blog](https://blog.google/technology/developers/gemma-3/) | 2025-02-20（4B）/ 2025-03-01（12B、27B）/ 2025-03-10（1B） | ⛔ **4B 档早 20 天** |
| **Seed-OSS-36B** | **2025-08-20** —— [官方 card changelog](https://huggingface.co/ByteDance-Seed/Seed-OSS-36B-Instruct) 逐字 `[2025/08/20]🔥We release Seed-OSS-36B-Base … and Seed-OSS-36B-Instruct` | 2025-08-20 | ⭐ **同日** |
| **GLM-4.5 / Air** | **2025-07-28**（**S**，媒体一致：[Pandaily](https://pandaily.com/zhipu-ai-launches-glm-4-5-an-open-source-355-b-ai-model-aimed-at-ai-agents) · [DeepLearning.AI The Batch](https://www.deeplearning.ai/the-batch/zhipu-ai-z-ai-releases-open-weights-glm-4-5-models-that-perform-comparably-to-the-latest-from-claude-and-deepseek)；⛔ z.ai 官方 blog 页为 JS 空壳，抓取为空） | 2025-07-20 | ⛔ **早 8 天** |

⛔ **故本表的「官方日」列只在核到官方一手或多家一致二手时填写，其余一律留 `⏳ 未核`，并以 HF 建仓日作为下界**——⛔ **不代填、不按「大概那个月」猜**。

⚠️ **Gemma 3 的 20 天差距值得单独记**：它说明厂商会**先把权重传成私有仓库、公告日再翻公开**，⇒ ⛔ **拿 HF `createdAt` 当发布日会把「2025-03-01 之前」这条边界画错**。本表的时间门（2025-01-01）在这一点上是安全的，因为最早的 2025 条目（DeepSeek-R1，2025-01-20）距边界有 20 天。

### 1.2 2025 H2（12 月 → 7 月）

| 官方日 | HF 建仓 | 模型（HF id） | 总参 / 激活 | 架构（注意力） | 原生精度 | 权重实测 | context | 许可 |
| :-- | :-- | :-- | :-- | :-- | :-- | --: | --: | :-- |
| ⏳ | 2025-12-22 | [zai-org/GLM-4.7](https://huggingface.co/zai-org/GLM-4.7) | 353B（含 MTP 358.3B）/ 32B | MoE 160E/8，GQA 8 KV | BF16 | **705.6 GB**（+MTP 11.1） | 202,752 | MIT |
| ⏳ | 2025-12-22 | [zai-org/GLM-4.7-FP8](https://huggingface.co/zai-org/GLM-4.7-FP8) | 同上 | 同上 | **FP8**（作者件） | **354.9 GB** | 202,752 | MIT |
| ⏳ | 2025-12-04 | [nvidia/…Nemotron-3-Nano-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) | 31.6B / 3B | MoE 128E/6，**混合 Mamba** | BF16 | **63.2 GB** | 262,144 | ⛔ NVIDIA 自定义 |
| **2025-11-17**（card changelog） | 2025-12-01 | [deepseek-ai/DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2) | 685B（含 MTP）/ 37B | MoE 256E/8，**MLA + DSA 稀疏** | ⛔ **FP8**（block 128×128） | **689.5 GB** | 163,840 | MIT |
| ⏳ | 2025-11-28 | [deepseek-ai/DeepSeek-V3.2-Speciale](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Speciale) | 同上 | 同上 | ⛔ **FP8** | **689.5 GB** | 163,840 | MIT |
| ⏳ | 2025-11-28 | [mistralai/Mistral-Large-3-675B-Instruct-2512](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) | 675B | dense | ⛔ **FP8** | **681.5 GB** | ⏳ | Apache-2.0 |
| ⏳ | 2025-11-28 | […-2512-NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) | 675B | dense | **NVFP4**（作者件） | **403.1 GB** | ⏳ | Apache-2.0 |
| ⏳ | 2025-11-04 | [moonshotai/Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) | ⭐ **1T** / 32B | MoE 384E/8，**MLA** | ⭐ ⛔ **INT4 权重（QAT，原生）** | **594.2 GB** | 262,144 | ⛔ modified-MIT |
| ⏳ | 2025-10-31 | [mistralai/Ministral-3-14B-Reasoning-2512](https://huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512) | 13.9B | dense | BF16 | **27.9 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-10-31 | [mistralai/Ministral-3-8B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) | 8.9B | dense | ⛔ **FP8**（另有 `-BF16` 仓库） | **10.4 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-10-30 | [moonshotai/Kimi-Linear-48B-A3B-Instruct](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct) | 49.1B / 3B | MoE 256E，⚠️ **线性注意力** | BF16 | **98.2 GB** | ⏳ | MIT |
| ⏳ | 2025-10-22 | [MiniMaxAI/MiniMax-M2](https://huggingface.co/MiniMaxAI/MiniMax-M2) | 228.7B / ~10B | MoE 256E/8，GQA 8 KV | ⛔ **FP8**（原生） | **230.1 GB** | 196,608 | ⛔ 自定义 |
| ⏳ | 2025-10-10 | [inclusionAI/Ring-1T](https://huggingface.co/inclusionAI/Ring-1T) | ⭐ **999.7B** / ⏳ | MoE 256E/8，GQA 8 KV | BF16 | ⛔ **1999.4 GB** | 65,536 | MIT |
| ⏳ | 2025-10-02 | [inclusionAI/Ling-1T](https://huggingface.co/inclusionAI/Ling-1T) | ⭐ **999.7B** / ⏳ | MoE 256E/8，GQA 8 KV | BF16 | ⛔ **1999.4 GB** | 32,768 | MIT |
| ⏳ | 2025-09-29 | [deepseek-ai/DeepSeek-V3.2-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp) | 685B / 37B | MoE 256E/8，MLA + DSA | ⛔ **FP8** | **689.5 GB** | 163,840 | MIT |
| ⏳ | 2025-09-29 | [zai-org/GLM-4.6](https://huggingface.co/zai-org/GLM-4.6) | 352B（含 MTP 356.8B）/ 32B | MoE 160E/8，GQA 8 KV，92 层 | BF16 | **705.6 GB**（+8.0） | 202,752 | MIT |
| ⏳ | 2025-09-29 | [zai-org/GLM-4.6-FP8](https://huggingface.co/zai-org/GLM-4.6-FP8) | 358.5B / 32B | 同上 | **FP8**（`compressed-tensors`，作者件） | **354.9 GB** | 202,752 | MIT |
| ⏳ | 2025-09-28 | [mistralai/Mistral-Large-3](https://huggingface.co/mistralai/Mistral-Large-3) | 675B | dense（`consolidated` 格式） | BF16 | ⛔ **1352.0 GB** | ⏳ | Apache-2.0 |
| ⏳ | 2025-09-22 | [Qwen/Qwen3-Next-80B-A3B-Instruct-FP8](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct-FP8) | 81.3B / 3B | MoE 512E/10，⚠️ **混合注意力**，2 KV | **FP8**（作者件） | ⭐ **82.1 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-09-22 | [nvidia/NVIDIA-Nemotron-Nano-9B-v2-FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2-FP8) | 8.9B | **混合 Mamba**，56 层 | **FP8**（作者件） | **10.3 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-09-22 | [deepseek-ai/DeepSeek-V3.1-Terminus](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| ⏳ | 2025-09-18 | [openai/gpt-oss-safeguard-120b](https://huggingface.co/openai/gpt-oss-safeguard-120b) | 120B / 5.1B | MoE 128E/4，滑窗交错 | ⛔ **MXFP4**（原生） | **65.2 GB** | 131,072（YaRN ×32） | Apache-2.0 |
| ⏳ | 2025-09-18 | [openai/gpt-oss-safeguard-20b](https://huggingface.co/openai/gpt-oss-safeguard-20b) | 21.5B / 3.6B | MoE 32E/4，24 层 | ⛔ **MXFP4**（原生） | **13.8 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-09-17 | [inclusionAI/Ling-flash-2.0](https://huggingface.co/inclusionAI/Ling-flash-2.0) | 102.9B / ⏳ | MoE 256E/8，4 KV，32 层 | BF16 | **205.8 GB** | 32,768 | MIT |
| ⏳ | 2025-09-16 | [ibm-granite/granite-4.0-h-small](https://huggingface.co/ibm-granite/granite-4.0-h-small) | 32.2B | MoE 72E/10，**混合 Mamba** | BF16 | **64.4 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-09-16 | [ibm-granite/granite-4.0-h-tiny](https://huggingface.co/ibm-granite/granite-4.0-h-tiny) | 6.9B | MoE 64E/6，**混合 Mamba**，4 KV | BF16 | **13.9 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-09-16 | [ibm-granite/granite-4.0-h-micro](https://huggingface.co/ibm-granite/granite-4.0-h-micro) | 3.2B | dense **混合 Mamba**（`num_local_experts: 0`） | BF16 | **6.4 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-09-12 | [mistralai/Magistral-Small-2509](https://huggingface.co/mistralai/Magistral-Small-2509) | 24.0B | dense，8 KV，40 层 | BF16 | **48.0 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-09-09 | [Qwen/Qwen3-Next-80B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) | 81.3B / 3B | MoE 512E/10，⚠️ 混合注意力，2 KV | BF16 | **162.7 GB** | 262,144（可扩 1M YaRN） | Apache-2.0 |
| ⏳ | 2025-09-09 | [Qwen/Qwen3-Next-80B-A3B-Thinking](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Thinking) | 81.3B / 3B | 同上 | BF16 | **162.7 GB** | 262,144 | Apache-2.0 |
| **2025-09-09**（**S**，Wikipedia） | 2025-09-03 | [moonshotai/Kimi-K2-Instruct-0905](https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905) | ⭐ **1T** / 32B | MoE 384E/8，MLA | ⛔ **FP8** | ⛔ **1029.2 GB** | 262,144 | ⛔ modified-MIT |
| ⏳ | 2025-08-21 | [deepseek-ai/DeepSeek-V3.1](https://huggingface.co/deepseek-ai/DeepSeek-V3.1) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| ⏳ | 2025-08-21 | [nvidia/NVIDIA-Nemotron-Nano-12B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-12B-v2) | 12.3B | **混合 Mamba**，62 层，8 KV | BF16 | **24.6 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⭐ **2025-08-20**（官方 card） | 2025-08-20 | [ByteDance-Seed/Seed-OSS-36B-Instruct](https://huggingface.co/ByteDance-Seed/Seed-OSS-36B-Instruct) | 36.2B | dense，8 KV，64 层 | BF16 | **72.3 GB** | ⭐ **524,288（原生）** | Apache-2.0 |
| ⏳ | 2025-08-12 | [nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) | 8.9B | **混合 Mamba** | BF16 | **17.8 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-08-12 | [CohereLabs/command-a-reasoning-08-2025](https://huggingface.co/CohereLabs/command-a-reasoning-08-2025) | 111.1B | dense | BF16 | **222.1 GB** | ⏳ | ⛔ **CC-BY-NC-4.0（不可商用）** |
| ⏳ | 2025-08-10 | [baichuan-inc/Baichuan-M2-32B](https://huggingface.co/baichuan-inc/Baichuan-M2-32B) | 32.8B | dense | BF16 | **65.5 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-08-05 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 4.0B | dense，8 KV，36 层 | BF16 | **8.0 GB** | ⭐ **262,144** | Apache-2.0 |
| **2025-08-05**（**S**） | 2025-08-04 | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | ⭐ **117B** / 5.1B | MoE 128E/4，滑窗交错 | ⛔ **MXFP4**（MoE 权重，原生） | ⭐ **65.2 GB** | 131,072（YaRN ×32；原生 4,096） | Apache-2.0 |
| **2025-08-05**（**S**） | 2025-08-04 | [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | 21B / 3.6B | MoE 32E/4 | ⛔ **MXFP4**（原生） | ⭐ **13.8 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-07-31 | [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | 30.5B / 3B | MoE 128E/8，4 KV | BF16 | **61.1 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-31 | […-Instruct-FP8](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8) | 30.5B / 3B | 同上 | **FP8**（作者件） | **31.2 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-30 | [tencent/Hunyuan-7B-Instruct](https://huggingface.co/tencent/Hunyuan-7B-Instruct) | 7.5B | dense，8 KV，32 层 | BF16 | **15.0 GB** | 32,768 | ⛔ card 未标 license 字段 |
| ⏳ | 2025-07-30 | [google/gemma-3-270m-it](https://huggingface.co/google/gemma-3-270m-it) | ⭐ **0.27B** | dense（本表最小） | BF16 | ⭐ **0.5 GB** | ⏳（gated） | ⛔ Gemma Terms |
| ⏳ | 2025-07-28 | [Qwen/Qwen3-30B-A3B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507) | 30.5B / 3B | MoE 128E/8，4 KV，48 层 | BF16 | **61.1 GB** | ⭐ **262,144** | Apache-2.0 |
| ⏳ | 2025-07-28 | […-2507-FP8](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507-FP8) | 30.5B / 3B | 同上 | **FP8**（作者件） | **31.2 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-28 | [stepfun-ai/step3](https://huggingface.co/stepfun-ai/step3) | 321.0B / ⏳ | MoE，多模态 VL，61 层 | BF16 | **641.9 GB** | ⛔ config 无 `max_position_embeddings` | Apache-2.0 |
| ⏳ | 2025-07-28 | [CohereLabs/command-a-vision-07-2025](https://huggingface.co/CohereLabs/command-a-vision-07-2025) | 111.9B | dense 多模态 | ⚠️ **F16**（非 BF16） | **223.7 GB** | ⏳（gated） | ⛔ **CC-BY-NC-4.0** |
| **2025-07-28**（**S**） | 2025-07-20 | [zai-org/GLM-4.5](https://huggingface.co/zai-org/GLM-4.5) | 355B / 32B | MoE 160E/8 | BF16 | **716.7 GB**（含 MTP） | 131,072 | MIT |
| **2025-07-28**（**S**） | 2025-07-20 | [zai-org/GLM-4.5-FP8](https://huggingface.co/zai-org/GLM-4.5-FP8) | 355B / 32B | 同上 | **FP8**（作者件） | **361.3 GB** | 131,072 | MIT |
| **2025-07-28**（**S**） | 2025-07-20 | [zai-org/GLM-4.5-Air](https://huggingface.co/zai-org/GLM-4.5-Air) | 106B / 12B | MoE 128E/8 | BF16 | **220.9 GB** | 131,072 | MIT |
| **2025-07-28**（**S**） | 2025-07-20 | [zai-org/GLM-4.5-Air-FP8](https://huggingface.co/zai-org/GLM-4.5-Air-FP8) | 106B / 12B | 同上 | **FP8**（作者件） | **112.6 GB** | 131,072 | MIT |
| ⏳ | 2025-07-25 | [Qwen/Qwen3-235B-A22B-Thinking-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Thinking-2507) | 235.1B / 22B | MoE 128E/8，4 KV，94 层 | BF16 | **470.2 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-25 | [nvidia/Llama-3_3-Nemotron-Super-49B-v1_5](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1_5) | 49.9B | **NAS 剪枝 dense**（DeciLM），80 层 | BF16 | **99.7 GB** | 131,072（RoPE ×16） | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-07-24 | [internlm/Intern-S1](https://huggingface.co/internlm/Intern-S1) | 240.7B / ⏳ | MoE 128E/8 多模态，4 KV，94 层 | BF16 | **481.4 GB** | 65,536 | Apache-2.0 |
| ⏳ | 2025-07-24 | [internlm/Intern-S1-FP8](https://huggingface.co/internlm/Intern-S1-FP8) | 240.7B | 同上 | **FP8**（作者件） | **249.1 GB** | 65,536 | Apache-2.0 |
| ⏳ | 2025-07-22 | [Qwen/Qwen3-Coder-480B-A35B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct) | 480.2B / 35B | MoE 160E/8，8 KV，62 层 | BF16 | **960.3 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-22 | […-Instruct-FP8](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8) | 480.2B / 35B | 同上 | **FP8**（作者件） | ⚠️ **482.1 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-21 | [Qwen/Qwen3-235B-A22B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507) | 235.1B / 22B | MoE 128E/8，4 KV，94 层 | BF16 | **470.2 GB** | 262,144（可扩 1.01M YaRN） | Apache-2.0 |
| ⏳ | 2025-07-21 | […-2507-FP8](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8) | 235.1B / 22B | 同上 | **FP8**（作者件，block 128×128） | ⭐ **236.4 GB** | 262,144 | Apache-2.0 |
| ⏳ | 2025-07-18 | [mistralai/Magistral-Small-2507](https://huggingface.co/mistralai/Magistral-Small-2507) | 23.6B | dense，8 KV，40 层 | BF16 | **47.1 GB** | 40,960 | Apache-2.0 |
| **2025-07**（**S**，日未定） | 2025-07-11 | [moonshotai/Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) | ⭐ **1T** / 32B | MoE 384E/8，MLA（`kv_lora_rank: 512`） | ⛔ **FP8** | ⛔ **1029.2 GB** | 131,072 | ⛔ modified-MIT |
| 同上 | 2025-07-03 | [moonshotai/Kimi-K2-Base](https://huggingface.co/moonshotai/Kimi-K2-Base) | 1.026T / 32B | 同上，61 层 | ⛔ **FP8** | ⛔ **1029.2 GB** | 131,072 | ⛔ other |
| ⏳ | 2025-07-04 | [mistralai/Devstral-Small-2507](https://huggingface.co/mistralai/Devstral-Small-2507) | 23.6B | dense，8 KV，40 层 | BF16 | **47.1 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-07-01 | [mistralai/Voxtral-Small-24B-2507](https://huggingface.co/mistralai/Voxtral-Small-24B-2507) | 24.3B | dense **音频多模态** | BF16 | **48.5 GB** | 131,072 | Apache-2.0 |

### 1.3 2025 H1（6 月 → 1 月）

| 官方日 | HF 建仓 | 模型（HF id） | 总参 / 激活 | 架构（注意力） | 原生精度 | 权重实测 | context | 许可 |
| :-- | :-- | :-- | :-- | :-- | :-- | --: | --: | :-- |
| **2025-06-27**（card changelog `2025.6.27`） | 2025-06-25 | [tencent/Hunyuan-A13B-Instruct](https://huggingface.co/tencent/Hunyuan-A13B-Instruct) | 80.4B / **13B** | MoE 64E，8 KV，32 层 | BF16 | **160.8 GB** | 32,768 | ⛔ 腾讯自定义 |
| 同上 | 2025-06-26 | [tencent/Hunyuan-A13B-Instruct-FP8](https://huggingface.co/tencent/Hunyuan-A13B-Instruct-FP8) | 80.4B / 13B | 同上 | **FP8**（作者件） | **80.9 GB** | 32,768 | ⛔ 自定义 |
| 同上 | 2025-06-26 | [tencent/Hunyuan-A13B-Instruct-GPTQ-Int4](https://huggingface.co/tencent/Hunyuan-A13B-Instruct-GPTQ-Int4) | 80.4B / 13B | 同上 | ⭐ **GPTQ-INT4**（作者件，4 bit） | ⭐ **42.7 GB** | 32,768 | ⛔ 自定义 |
| ⏳ | 2025-06-28 | [baidu/ERNIE-4.5-300B-A47B-PT](https://huggingface.co/baidu/ERNIE-4.5-300B-A47B-PT) | 300.5B / **47B** | MoE，8 KV，54 层 | BF16 | **601.0 GB**（另有独立 `mtp/`） | 131,072 | Apache-2.0 |
| ⏳ | 2025-06-28 | [baidu/ERNIE-4.5-21B-A3B-PT](https://huggingface.co/baidu/ERNIE-4.5-21B-A3B-PT) | 21.9B / 3B | MoE，4 KV，28 层 | BF16 | **43.9 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-06-28 | [baidu/ERNIE-4.5-0.3B-PT](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT) | 0.36B | dense，2 KV，18 层 | BF16 | **0.7 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-06-19 | [mistralai/Mistral-Small-3.2-24B-Instruct-2506](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506) | 24.0B | dense **多模态**，8 KV，40 层 | BF16 | **48.0 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-06-19 | [microsoft/Phi-4-mini-flash-reasoning](https://huggingface.co/microsoft/Phi-4-mini-flash-reasoning) | 3.85B | ⚠️ **`Phi4FlashForCausalLM`**（混合），20 KV | BF16 | **7.7 GB** | ⭐ **262,144** | MIT |
| ⏳ | 2025-06-13 | [MiniMaxAI/MiniMax-M1-80k](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k) | 456.1B / **45.9B** | MoE 32E/2，⚠️ **闪电注意力**，80 层 | BF16 | ⛔ **912.2 GB** | ⭐ **10,240,000** | Apache-2.0 |
| ⏳ | 2025-06-05 | [MiniMaxAI/MiniMax-M1-40k](https://huggingface.co/MiniMaxAI/MiniMax-M1-40k) | 456.1B / 45.9B | 同上 | BF16 | ⛔ **912.2 GB** | ⭐ **10,240,000** | Apache-2.0 |
| ⏳ | 2025-06-12 | [google/gemma-3n-E2B-it](https://huggingface.co/google/gemma-3n-E2B-it) | 5.44B（**有效 2B**） | dense 边端多模态 | BF16 | **10.9 GB** | ⏳（gated） | ⛔ Gemma Terms |
| ⏳ | 2025-06-03 | [google/gemma-3n-E4B-it](https://huggingface.co/google/gemma-3n-E4B-it) | 7.85B（**有效 4B**） | dense 边端多模态 | BF16 | **15.7 GB** | ⏳（gated） | ⛔ Gemma Terms |
| ⏳ | 2025-06-04 | [mistralai/Magistral-Small-2506](https://huggingface.co/mistralai/Magistral-Small-2506) | 23.6B | dense，8 KV，40 层 | BF16 | **47.1 GB** | 40,960 | Apache-2.0 |
| ⏳ | 2025-05-29 | [deepseek-ai/DeepSeek-R1-0528-Qwen3-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B) | 8.2B | dense（**蒸馏 Qwen3**） | BF16 | **16.4 GB** | 131,072 | MIT |
| ⏳ | 2025-05-28 | [deepseek-ai/DeepSeek-R1-0528](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| ⏳ | 2025-05-14 | [rednote-hilab/dots.llm1.inst](https://huggingface.co/rednote-hilab/dots.llm1.inst) | 142.8B / **14B** | MoE 128E/6，⚠️ **32 KV 头（无 GQA 压缩）**，62 层 | BF16 | **285.6 GB** | 32,768 | MIT |
| ⏳ | 2025-05-13 | [nvidia/Llama-3_3-Nemotron-Super-49B-v1-FP8](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1-FP8) | 49.9B | NAS 剪枝 dense（DeciLM） | **FP8**（作者件） | **52.0 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-05-12 | [mistralai/Devstral-Small-2505](https://huggingface.co/mistralai/Devstral-Small-2505) | 23.6B | dense，8 KV，40 层 | BF16 | **47.1 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-05-01 | [Qwen/Qwen3-32B-AWQ](https://huggingface.co/Qwen/Qwen3-32B-AWQ) | 32.8B | dense，8 KV | ⭐ **AWQ-INT4**（作者件，4 bit） | ⭐ **19.3 GB** | 40,960 | Apache-2.0 |
| ⏳ | 2025-05-01 | [tiiuae/Falcon-H1-34B-Instruct](https://huggingface.co/tiiuae/Falcon-H1-34B-Instruct) | 33.6B | **混合 Mamba** | BF16 | **67.3 GB** | 262,144 | ⛔ Falcon LLM License |
| ⏳ | 2025-04-29 | [microsoft/Phi-4-mini-reasoning](https://huggingface.co/microsoft/Phi-4-mini-reasoning) | 3.84B | dense（Phi3 架构），8 KV | BF16 | **7.7 GB** | 131,072 | MIT |
| ⭐ **2025-04-29**（官方 blog） | 2025-04-28 | [Qwen/Qwen3-235B-A22B-FP8](https://huggingface.co/Qwen/Qwen3-235B-A22B-FP8) | 235.1B / 22B | MoE 128E/8，4 KV，94 层 | **FP8**（作者件） | **239.0 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-28 | [Qwen/Qwen3-32B-FP8](https://huggingface.co/Qwen/Qwen3-32B-FP8) | 32.8B | dense，8 KV，64 层 | **FP8**（作者件） | **34.3 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-28 | [Qwen/Qwen3-30B-A3B-FP8](https://huggingface.co/Qwen/Qwen3-30B-A3B-FP8) | 30.5B / 3B | MoE 128E/8，4 KV，48 层 | **FP8**（作者件） | **32.4 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-28 | [Qwen/Qwen3-14B-FP8](https://huggingface.co/Qwen/Qwen3-14B-FP8) | 14.8B | dense，8 KV，40 层 | **FP8**（作者件） | **16.3 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-28 | [Qwen/Qwen3-8B-FP8](https://huggingface.co/Qwen/Qwen3-8B-FP8) | 8.2B | dense，8 KV，36 层 | **FP8**（作者件） | **9.4 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B) | 235.1B / 22B | MoE 128E/8，4 KV，94 层 | BF16 | **470.2 GB** | ⚠️ **40,960**（blog 称 128K = YaRN） | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) | 32.8B | dense，8 KV，64 层 | BF16 | **65.5 GB** | ⚠️ **40,960**（同上） | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-30B-A3B](https://huggingface.co/Qwen/Qwen3-30B-A3B) | 30.5B / 3B | MoE 128E/8，4 KV，48 层 | BF16 | **61.1 GB** | ⚠️ **40,960** | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | 14.8B | dense，8 KV，40 层 | BF16 | **29.5 GB** | ⚠️ **40,960** | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8.2B | dense，8 KV，36 层 | BF16 | **16.4 GB** | ⚠️ **40,960** | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) | 4.0B | dense，8 KV，36 层 | BF16 | **8.0 GB** | 40,960（blog 称 32K） | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) | 2.03B | dense，8 KV，28 层 | BF16 | **4.1 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-04-27 | [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) | 0.75B | dense，8 KV，28 层 | BF16 | ⭐ **1.5 GB** | 40,960 | Apache-2.0 |
| ⏳ | 2025-04-17 | [microsoft/Phi-4-reasoning-plus](https://huggingface.co/microsoft/Phi-4-reasoning-plus) | 14.7B | dense，10 KV，40 层 | BF16 | **29.3 GB** | 32,768 | MIT |
| ⏳ | 2025-04-09 | [microsoft/Phi-4-reasoning](https://huggingface.co/microsoft/Phi-4-reasoning) | 14.7B | dense，10 KV，40 层 | BF16 | **29.3 GB** | 32,768 | MIT |
| ⏳ | 2025-04-07 | [nvidia/Llama-3_1-Nemotron-Ultra-253B-v1](https://huggingface.co/nvidia/Llama-3_1-Nemotron-Ultra-253B-v1) | **253.4B** | **NAS 剪枝 dense**（DeciLM），162 层 | BF16 | ⛔ **506.8 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⭐ **2025-04-05**（官方 blog） | 2025-04-02 | [meta-llama/Llama-4-Scout-17B-16E-Instruct](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) | 108.6B / **17B** | MoE **16E** 多模态 | BF16 | **217.3 GB** | ⚠️ ⏳（gated；blog 称 **10M**，但「pre-trained and post-trained with a **256K** context length」） | ⛔ Llama 4 社区许可（gated） |
| 同上 | 2025-04-01 | [meta-llama/Llama-4-Maverick-17B-128E-Instruct](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) | 401.6B / **17B** | MoE **128E** + 1 共享专家 | BF16 | ⛔ **803.2 GB** | ⏳（gated；card 称 1M） | ⛔ Llama 4 社区许可 |
| 同上 | 2025-04-01 | […-Instruct-FP8](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8) | 401.6B / 17B | 同上 | **FP8**（作者件） | **416.8 GB** | ⏳ | ⛔ 同上 |
| ⏳ | 2025-04-15 | [google/gemma-3-27b-it-qat-q4_0-unquantized](https://huggingface.co/google/gemma-3-27b-it-qat-q4_0-unquantized) | 27.4B | dense 多模态 | ⚠️ **BF16（QAT 后未量化）** | **54.9 GB** | ⏳（gated） | ⛔ Gemma Terms |
| ⏳ | 2025-04-08 | [google/gemma-3-12b-it-qat-q4_0-unquantized](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized) | 12.2B | dense 多模态 | ⚠️ **BF16（QAT 后未量化）** | **24.4 GB** | ⏳ | ⛔ Gemma Terms |
| ⏳ | 2025-03-24 | [deepseek-ai/DeepSeek-V3-0324](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324) | 685B / 37B | MoE 256E/8，MLA | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| ⭐ **2025-03-12**（官方 blog） | 2025-03-20 | [google/gemma-3-27b-it-qat-q4_0-gguf](https://huggingface.co/google/gemma-3-27b-it-qat-q4_0-gguf) | 27.4B | dense 多模态 | ⭐ **Q4_0（QAT，官方 GGUF）** | **17.2 GB**（+ mmproj 0.9） | ⏳ | ⛔ Gemma Terms |
| 同上 | 2025-03-12 | [google/gemma-3-12b-it-qat-q4_0-gguf](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-gguf) | 12.2B | dense 多模态 | ⭐ **Q4_0（QAT，官方 GGUF）** | ⭐ **8.1 GB**（+ mmproj 0.9） | ⏳ | ⛔ Gemma Terms |
| 同上 | 2025-03-12 | [google/gemma-3-4b-it-qat-q4_0-gguf](https://huggingface.co/google/gemma-3-4b-it-qat-q4_0-gguf) | 4.3B | dense 多模态 | ⭐ **Q4_0（QAT，官方 GGUF）** | ⭐ **4.0 GB**（含 mmproj） | ⏳ | ⛔ Gemma Terms |
| 同上 | 2025-03-10 | [google/gemma-3-1b-it](https://huggingface.co/google/gemma-3-1b-it) | 1.0B | dense（**纯文本**） | BF16 | **2.0 GB** | ⏳（gated） | ⛔ Gemma Terms |
| 同上 | 2025-03-01 | [google/gemma-3-27b-it](https://huggingface.co/google/gemma-3-27b-it) | 27.4B | dense 多模态，**滑窗/全局交错** | BF16 | **54.9 GB** | ⏳（gated；blog 称 128K） | ⛔ Gemma Terms |
| 同上 | 2025-03-01 | [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it) | 12.2B | dense 多模态 | BF16 | **24.4 GB** | ⏳（gated） | ⛔ Gemma Terms |
| 同上 | 2025-02-20 | [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) | 4.3B | dense 多模态 | BF16 | **8.6 GB** | ⏳（gated） | ⛔ Gemma Terms |
| ⏳ | 2025-03-16 | [nvidia/Llama-3_3-Nemotron-Super-49B-v1](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1) | 49.9B | **NAS 剪枝 dense**（DeciLM），80 层 | BF16 | **99.7 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-03-16 | [nvidia/Llama-3.1-Nemotron-Nano-8B-v1](https://huggingface.co/nvidia/Llama-3.1-Nemotron-Nano-8B-v1) | 8.03B | dense（Llama 架构），8 KV | BF16 | **16.1 GB** | 131,072 | ⛔ NVIDIA 自定义 |
| ⏳ | 2025-03-11 | [mistralai/Mistral-Small-3.1-24B-Instruct-2503](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) | 24.0B | dense **多模态**，8 KV，40 层 | BF16 | **48.0 GB** | 131,072 | Apache-2.0 |
| ⏳ | 2025-03-11 | [CohereLabs/c4ai-command-a-03-2025](https://huggingface.co/CohereLabs/c4ai-command-a-03-2025) | 111.1B | dense | BF16 | **222.1 GB** | ⏳ | ⛔ **CC-BY-NC-4.0（不可商用）** |
| **2025-03-06**（**S**） | 2025-03-05 | [Qwen/QwQ-32B](https://huggingface.co/Qwen/QwQ-32B) | 32.8B | dense（Qwen2 架构），8 KV，64 层 | BF16 | **65.5 GB** | 40,960 | Apache-2.0 |
| 同上 | 2025-03-05 | [Qwen/QwQ-32B-AWQ](https://huggingface.co/Qwen/QwQ-32B-AWQ) | 32.8B | 同上 | ⭐ **AWQ-INT4**（作者件，4 bit） | ⭐ **19.3 GB** | 40,960 | Apache-2.0 |
| ⏳ | 2025-02-24 | [microsoft/Phi-4-multimodal-instruct](https://huggingface.co/microsoft/Phi-4-multimodal-instruct) | 5.57B | dense **多模态**（含 speech/vision LoRA） | BF16 | **11.1 GB** | 131,072 | MIT |
| ⏳ | 2025-02-19 | [microsoft/Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | 3.84B | dense（Phi3 架构），8 KV，32 层 | BF16 | **7.7 GB** | 131,072 | MIT |
| **2025-01-30**（**S**） | 2025-01-28 | [mistralai/Mistral-Small-24B-Instruct-2501](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501) | 23.6B | dense（**纯文本**），8 KV，40 层 | BF16 | **47.1 GB** | 32,768 | Apache-2.0 |
| ⭐ **2025-01-20** | 2025-01-20 | [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1) | 685B / 37B | MoE 256E/8，**MLA** | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Zero](https://huggingface.co/deepseek-ai/DeepSeek-R1-Zero) | 684.5B / 37B | 同上，61 层 | ⛔ **FP8** | **688.6 GB** | 163,840 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) | 70.6B | dense（蒸馏 Llama 3.3） | BF16 | **141.1 GB** | 131,072 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-32B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B) | 32.8B | dense（蒸馏 Qwen2.5） | BF16 | **65.5 GB** | 131,072 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-14B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B) | 14.8B | dense（蒸馏），8 KV，48 层 | BF16 | **29.5 GB** | 131,072 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Llama-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B) | 8.03B | dense（蒸馏 Llama 3.1），8 KV | BF16 | **16.1 GB** | 131,072 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B) | 7.6B | dense（蒸馏） | BF16 | **15.2 GB** | 131,072 | MIT |
| 同上 | 2025-01-20 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) | 1.78B | dense（蒸馏），**2 KV**，28 层 | BF16 | ⭐ **3.6 GB** | 131,072 | MIT |
| ⏳ | 2025-01-13 | [internlm/internlm3-8b-instruct](https://huggingface.co/internlm/internlm3-8b-instruct) | 8.8B | dense | BF16 | **17.6 GB** | 32,768 | Apache-2.0 |
| ⏳ | 2025-01-12 | [MiniMaxAI/MiniMax-Text-01](https://huggingface.co/MiniMaxAI/MiniMax-Text-01) | 456.1B / **45.9B** | MoE 32E/2，闪电注意力 | BF16 | ⛔ **914.7 GB** | ⭐ **10,240,000** | ⛔ 自定义 |

### 1.4 benchmark 位置

⛔ **本节的证据级别低于 §1.2 / §1.3。** §1.2 / §1.3 的体积是我本人 HF API 实测（**M**）；⛔ **本节绝大多数数字是并行核验路逐字取自一手页面、我未回页复核，级别为 S★**。按 [CLAUDE.md](../../../../CLAUDE.md) §3.8 与「机械代理只能定位不能裁定」，**引用前必须逐条回原文，不得当 M 用**。⭐ 只有三条是我本人用 `tools/pdf_extractor.py` 提取一手 PDF 得到的（**M**）：Command A · Ling-1T · ERNIE-4.5。

#### 1.4.1 ⛔ 五条混比陷阱（⛔ 不看这一节就不要用下面任何数字）

1. ⛔ **AA 站点不保留历史版本分数——在架模型页被整体重刷成当前版本号。** 实测落差：`DeepSeek-R1-0528` 在 V2.x 期是 **68**、v4.1.1 是 **20**；`Nemotron-Super-49B-v1.5` 发布时 **64**、现 **9**（7 倍）；`Nemotron-Nano-9B-v2` 发布时 **43**、现 **9**。⛔ **这不是模型退步，是索引重基线。** ⇒ **任何历史 AA 数字都不得与本节同列比较。**
2. ⛔ **厂商 model card 里的 AA 数字是发布期口径，⛔ 不是当前口径，且不写版本号。** 最危险的实例：**`MiniMax-M2` 的 HF card 自报「AA Intelligence 61」，而 AA 当前页给 29——差 32 分。** 同卡的「AA-LCR 61」「MMLU-Pro 82（AA 口径）」「LCB 83（AA 口径）」同理，且 LCB **连版本都没标**。
3. ⛔ **v4.1.1 内部也不同质：38 条里 26 条是估计值。** ⛔ **陷阱在于页面顶部 summary 卡片写裸数字，只有 FAQ 段落才写 `(estimated)`**——⇒ **只读 summary 必然把估计值误当实测值。**
4. ⚠️ **v4.1 → v4.1.1 虽然评测项与权重完全未变（官方 changelog 逐字「contributing evaluations and their weights are unchanged from v4.1」），⛔ 但三项 grader 换成了 `GPT-5.6 Luna (medium)`**（HLE 12% + AA-Omniscience 12% + AA-LCR 6% = **30% 权重**）。⇒ ⚠️ 两版近似可比但⛔ **非严格同一口径**。
5. ⛔ **2025 世代的核心自报刻度已被 AA 逐出索引。** **MMLU-Pro / AIME 2025 / LiveCodeBench 三项在 v4.0（2026-01-06）从 Index 移除**，AA 明确把 MMLU-Pro 与 LiveCodeBench 列在「sit outside the Index score」；**IFBench 在 v4.1 因饱和移出**。⛔ **而本节大量 2025 模型的主刻度恰恰就是 MMLU-Pro 与 LiveCodeBench。** ⇒ **「用厂商自报的 MMLU-Pro 去推算它在当前 Index 上的位置」是不可能的。**

⛔ **另一条元事实：AA 官方从未就跨版本可比性发过任何正式声明。** v4.1 文章、changelog、methodology 页均未提及是否重跑旧模型、也未给跨版本比较指引。⇒ ⛔ 上面第 3 条「估计值 = 回填机制」是从页面标签**反推**的（**I**），不是 AA 明文政策。

#### 1.4.2 AA Index v4.1.1 分数（⛔ 全部 S★）

⭐ **`Est=否` 即 AA 实测，⛔ 只有这 12 个够格写「AA 实测」**：

| 模型 | v4.1.1 | Est | 模型 | v4.1.1 | Est |
| :-- | --: | :-: | :-- | --: | :-: |
| ⭐ **GLM-4.7** | ⭐ **34** | **否** | GLM-4.6（R / NT） | **29** / 23 | **否** / ⚠️估 |
| Kimi K2-Thinking | 33 | ⚠️估 | DeepSeek V3.2-Exp（R / NT） | 33 / 25 | ⚠️估 |
| DeepSeek V3.1-Terminus（R / NT） | 31 / 22 | ⚠️估 | MiniMax-M2 | 29 | ⚠️估 |
| gpt-oss-120b（high / low） | **24** / **15** | **否** | GLM-4.5 / GLM-4.5-Air | 20 / 17 | ⚠️估 |
| Kimi K2-Instruct | 20 | ⚠️估 | DeepSeek-R1-0528 | 20 | ⚠️估 |
| DeepSeek V3.1（R / NT） | 21 / 21 | ⚠️估 | MiniMax-M1-80k | 18 | ⚠️估 |
| Qwen3-235B-A22B-Instruct-2507 | 18 | ⚠️估 | Qwen3-Coder-480B-A35B | 18 | ⚠️估 |
| ⭐ **Qwen3-Next-80B-A3B** | **17** | **否** | ⭐ **Mistral-Large-3** | **16** | **否** |
| ⭐ **Mistral Small 3.1** | **15** | **否** | gpt-oss-20b（high） | 15 | S 级摘要 |
| ⭐ **Llama 4 Maverick** | **14** | **否** | QwQ-32B | 13 | ⚠️估 |
| Qwen3-235B-A22B（R / NT） | 13 / 11 | ⚠️估 | ⭐ **Qwen3-32B** | **11** | **否** |
| ⭐ **Mistral Small 3.2** | **11** | **否** | Magistral Small | 11 | ⚠️估 |
| ⭐ **Llama 4 Scout** | **10** | **否** | Qwen3-30B-A3B | 9 | ⚠️估 |
| Devstral Small | 9 | ⚠️估 | Nemotron-Nano-9B-v2 | 9 | ⚠️估 |
| Nemotron-Super-49B-v1.5 | 9 | ⚠️估 | Nemotron-Ultra-253B | 9 | ⚠️估 |
| ⭐ **Gemma 3 27B-it** | **7** | **否** | Mistral Small 3 (2501) | 7 | ⚠️估 |
| Command A (111B) | 7 | ⚠️估 | ⭐ **Gemma 3 12B-it** | **6** | **否** |
| Phi-4 (14B) | 5 | ⚠️估 | Granite-4.0-H-Small | 5 | ⚠️估 |
| Gemma 3 4B-it | 1 | ⚠️估 | Gemma 3n E4B-it | 1 | ⚠️估 |

⚠️ **一条反常但两页各自如此写的记录**：`Mistral Small 3.2` = **11** ⛔ **低于** `Mistral Small 3.1` = **15**，⛔ 且两者**都不是**估计值。本文不裁定，只登记。

⛔ **AA 侧的三个硬缺口**：① ⛔ **`gpt-oss` 的 medium effort 档 AA 根本不发布**（只有 high / low 两页，`-medium` 返回 404）⇒ 「三档分开」在 AA 侧只能给两档，第三档必须走官方 card（§1.4.3 已给全）；② **`DeepSeek-R1` 原始版（2025-01）在 v4.1.1 下无法定位**（`/models/deepseek-r1` 实为 0528，其余 slug 404）；③ **`Kimi K2-Instruct-0905` 无独立条目**（AA 只列 "Kimi K2"）。

⛔ **完全无 AA 条目的 10 个模型**：`Phi-4-reasoning` · `Phi-4-reasoning-plus` · `Phi-4-mini` · `Seed-OSS-36B` · `Hunyuan-A13B` · `ERNIE-4.5-300B-A47B` · `Ling-1T` · `Step-3` · `dots.llm1` · `Intern-S1`。

#### 1.4.3 厂商自报关键分（⛔ 全部「自报」，⛔ 逐条标出口径不可比之处）

⛔ **先读三条**：① 全部为**厂商自己跑自己报**，⛔ 非独立评测；② **LiveCodeBench（LCB）的版本 / 时间窗口不同即不可比**，本表逐条标注，未标者一律记「未标版本」；③ **SWE-bench Verified 的 scaffold 决定分数**，同一模型跨 scaffold 可差 20 分。

| 模型 | MMLU-Pro | GPQA-D | SWE-bench V（含 scaffold） | LCB（含版本 / 窗口） | 来源 |
| :-- | --: | --: | :-- | :-- | :-- |
| DeepSeek-R1（2501） | 84.0 (EM) | 71.5 | 49.2 | ⛔ 65.9（**无版本窗口**）⚠️ 同厂另卡写 63.5 (2408–2505) | [card](https://huggingface.co/deepseek-ai/DeepSeek-R1) |
| DeepSeek-R1-0528 | 85.0 | 81.0 | **57.6（Agentless）** | 73.3 (2408–2505) | [card](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528) |
| DeepSeek-V3.1（NT / R） | 83.7 / 84.8 | 74.9 / 80.1 | **66.0（agent mode）** | 56.4 / 74.8 (2408–2505) | [card](https://huggingface.co/deepseek-ai/DeepSeek-V3.1) |
| DeepSeek-V3.1-Terminus | 85.0 | 80.7 | 68.4 | ⛔ 74.9（未标窗口） | [card](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus) |
| DeepSeek-V3.2-Exp | 85.0 | 79.9 | 67.8 | ⛔ 74.1（未标窗口） | [card](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp) |
| ⛔ QwQ-32B | ⛔ **无任何厂商自报值** | 65.6 | ⏳ | 62.7（**v5**） | ⛔ card/blog 全是图片；数字取 [arXiv:2505.09388](https://arxiv.org/abs/2505.09388) 对照列 |
| Qwen3-235B-A22B（R / NT） | ⛔ 无（用 MMLU-Redux 替代） | 71.1 / 62.9 | ⛔ **无** | 70.7 / 35.3（**v5**） | [arXiv:2505.09388](https://arxiv.org/abs/2505.09388) |
| Qwen3-32B（R / NT） | ⛔ 无 | 68.4 / 54.6 | ⛔ **无** | 65.7 / 31.3（**v5**） | 同上 |
| Qwen3-30B-A3B（R / NT） | ⛔ 无 | 65.8 / 54.8 | ⛔ **无** | 62.6 / 29.8（**v5**） | 同上 |
| ⭐ Qwen3-235B-A22B-Instruct-2507 | **83.0** | 77.5 | ⛔ **无** | 51.8（**v6**） | ⭐ 另有 **RULER avg 92.5 / 128k 93.9 / 1M 84.5** · [card](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507) |
| Qwen3-Coder-480B-A35B | ⏳ | ⏳ | ⛔ **查不到**（见下方 E 条） | 44.93（**v6**）· Aider-Polyglot 60.40 | [arXiv:2603.00729](https://arxiv.org/html/2603.00729v1) |
| ⭐ Qwen3-Next-80B-A3B（I / T） | 80.6 / **82.7** | 72.9 / 77.2 | ⏳ | 56.6 / 68.7（**v6**） | ⭐ RULER avg **91.8** · [I](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) · [T](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Thinking) |
| Llama 4 Scout | 74.3 (0-shot) | 57.2 | ⛔ **无** | 32.8（**窗口 2024-10-01–2025-02-01**） | ⚠️ IT 表无 MMLU · [card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) |
| Llama 4 Maverick | 80.5 | 69.8 | ⛔ **无** | 43.4（同窗口） | ⛔ **LMArena 1417 属 `-03-26-Experimental`，⛔ 不是发布权重**；公开权重复测约第 32 名 |
| Mistral Small 3 (2501) | 66.3 (5-shot CoT) | ⛔ **只有 GPQA Main 45.3** | ⛔ 无 | ⛔ 无 | [card](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501) |
| ⭐ Mistral Small 3.1 | 66.76 | 45.96 | ⛔ 无 | ⛔ 无 | ⭐ **RULER 32K 93.96 / 128K 81.20** · LongBench v2 37.18 · [card](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) |
| Mistral Small 3.2 | 69.06 | 46.13 | ⛔ 无 | ⛔ 无 | [card](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506) |
| Magistral Small（1.0 / 2509） | ⏳ | ⛔ 68.2（**未标 Diamond**）/ 70.07 | ⛔ 无 | 55.8 **v5** / 47.4 **v6**；2509: 70.88 **v5** | [arXiv:2506.10910](https://arxiv.org/html/2506.10910v1) · [2509 card](https://huggingface.co/mistralai/Magistral-Small-2509) |
| Devstral Small（1.0 / 1.1） | ⛔ 无 | ⛔ 无 | ⭐ **46.8 / 53.6（均 OpenHands scaffold）** | ⛔ 无 | 其余学术榜全无 · [blog](https://mistral.ai/news/devstral) |
| ⛔ **Mistral-Large-3** | ⛔ **全部查不到** | ⛔ | | | [官方页](https://mistral.ai/news/mistral-3/) benchmark 表**全是图片**；HF 仓库 **401 gated**。**本轮唯一「AA 有实测分 16 但零个官方自报数字」的模型** |
| Gemma 3 27B-it | 67.5 | 42.4 | ⛔ 无 | ⛔ **29.7 (T6) vs 39.0 (T18) 同报告内互相矛盾，⛔ 且版本与窗口两处都没给** | ⭐ **RULER 32K 91.1 / 128K 66.0** · MRCR 128K 59.3 · Arena Elo 1338 · [arXiv:2503.19786](https://arxiv.org/html/2503.19786v1) |
| Gemma 3 12B / 4B-it | 60.6 / 43.6 | 40.9 / 30.8 | ⛔ 无 | 24.6–32.0 / 12.6–23.0（同矛盾） | RULER 80.3/57.1 · 同上 |
| Gemma 3n E4B-it | 50.6 | 23.7 | ⛔ 无 | 25.7（**v5**） | ⛔ **窗口仅 32K，无长上下文评测**；⚠️ **E2B (24.8) 在 GPQA-D 上高于 E4B (23.7)，厂商未解释** · [card](https://huggingface.co/google/gemma-3n-E4B-it) |
| GLM-4.5 / -Air | 84.6 / 81.4 | 79.1 / 75.0 (avg@8) | ⭐ **64.2 / 57.6（OpenHands v0.34.0，≤100 iter，T=0.6）** | 72.9 / 70.7（**窗口 2407–2501**，非 v5/v6 命名） | ⚠️ **HLE 论文 14.4 vs HF 小组件 8.32，厂商内部矛盾** · [arXiv:2508.06471](https://arxiv.org/html/2508.06471v1) |
| GLM-4.6 | 83.2 | 81.0 | 68.0 | 82.8（**v6**） | ⛔ 本体 card/blog 全是图片 / SPA 空壳；数字取 **Z.ai 自家 GLM-4.7 card 的对照列** |
| ⭐ **GLM-4.7** | 84.3 | ⭐ **85.7** | **73.8** | **84.9（v6）** | ⚠️ **TB-2.0 正文 41.0 vs HF 小组件 33.4，厂商内部矛盾** · [card](https://huggingface.co/zai-org/GLM-4.7) |
| Kimi K2-Instruct | 81.1 (EM) | 75.1 (avg@8) | ⛔ **Agentless 51.8 / Agentic 65.8 / 多次尝试 71.6——⛔ 同一模型跨度 20 分** | 53.7（**v6**，2408–2505） | ⭐ **这一行是「SWE 分必须带 scaffold」最好的例证** · [card](https://huggingface.co/moonshotai/Kimi-K2-Instruct) |
| Kimi K2-0905 | ⛔ 无 | ⛔ 无 | ⭐ **69.2 ± 0.63（5 次全量均值，自研 harness，⭐ 裁剪不可达 git 对象防泄漏）** | ⛔ 无 | Terminal-Bench **44.5 ± 2.03** · [card](https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905) |
| ⭐ Kimi K2-Thinking | 84.6 | ⭐ **84.5（no tools）** | 71.3（w/ tools） | 83.1（**v6**） | **HLE 23.9 → 44.9（w-tools）** · [card](https://huggingface.co/moonshotai/Kimi-K2-Thinking)（INT4） |
| MiniMax-M1-80k | 81.1 | 70.0 | ⚠️ **56.0（Agentless 两步定位，⛔ 486 题子集，丢 14 例）** | 65.0（2408–2505） | ⭐ **MRCR-128k 73.4 / 1M 56.2** · LongBench-v2 61.5 · [card](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k) |
| MiniMax-M2 | ⚠️ 82（标「AA 口径」） | ⚠️ 78 | ⭐ **69.4（R2E-Gym 风格 on OpenHands，128k，≤100 步，无 test-time scaling）** | ⛔ 83（**未标版本**） | ⛔ **该卡自报「AA Intelligence 61」，与 v4.1.1 的 29 差 32 分——本表最危险的混比陷阱** |
| ⭐ **gpt-oss-120b（low/med/high）** | ⏳ | ⭐ **67.1 / 73.1 / 80.1** | **47.9 / 52.6 / 62.4** | ⛔ **该卡完全没有 LCB** | AIME25 50.4/80.0/92.5 · HLE 5.2/8.6/14.9 · Codeforces Elo 1595/2205/2463 · [arXiv:2508.10925](https://arxiv.org/html/2508.10925v1) T3 = 官方 card |
| gpt-oss-20b（low/med/high） | ⏳ | 56.8 / 66.0 / 71.5 | 37.4 / 53.2 / 60.7 | ⛔ 同上无 | AIME25 37.1/72.1/91.7 · HLE 4.2/7.0/10.9 · 同上 |
| Nemotron-Nano-9B-v2 | ⛔ 无 | 64.0 | ⏳ | ⛔ 71.1（**未标版本**） | ⭐ RULER 128K 78.9 · [card](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) |
| Nemotron-Super-49B-v1.5 | 79.53 (CoT) | 71.97 | ⏳ | 73.58（**窗口 2410–2502**） | ⚠️ **卡片写 release 7/25/2025** · [card](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1_5) |
| Nemotron-Ultra-253B（On/Off） | ⛔ 无 | 76.01 / 56.60 | ⏳ | 66.31 / 29.03（**窗口 20240801–20250201**） | ⚠️ **BFCL V2 Live（⛔ 不是 v3）** · [card](https://huggingface.co/nvidia/Llama-3_1-Nemotron-Ultra-253B-v1) |
| Phi-4 (14B) | 70.4 | 56.1 | ⛔ 无 | ⛔ 无 | [arXiv:2412.08905](https://arxiv.org/html/2412.08905v1) T1（simple-evals，temp 0.5） |
| Phi-4-reasoning / -plus | 74.3 / 76.0 | 65.8 / 68.9 | ⛔ 无 | 53.8 / 53.1（**窗口 2024-08-01–2025-02-01**） | ⚠️ plus 比 plain 多生成约 50% token · [card](https://huggingface.co/microsoft/Phi-4-reasoning-plus) |
| Phi-4-mini (3.8B) | 52.8 (0-shot CoT) | 25.2 | ⛔ 无 | ⛔ 无 | [card](https://huggingface.co/microsoft/Phi-4-mini-instruct) |
| ⭐ Seed-OSS-36B-Instruct | 82.7 | 71.4 | ⚠️ **56.0 (OpenHands) vs 47.0 (AgentLess)——跨度 9 分** | 67.4（**v6**，2025/02–05） | ⭐ **RULER-128K 94.6**（本表最高）⚠️ 竞品列用「重测值(原报告值)」双写，常差 3–7 分 · [card](https://huggingface.co/ByteDance-Seed/Seed-OSS-36B-Instruct) |
| Hunyuan-A13B-Instruct | ⚠️ 67.23（**base 表，instruct 表无此项**） | 71.2 | ⛔ **无** | ⛔ 63.9（**未标版本**） | BFCL v3 78.3 · τ-Bench 54.7 · [card](https://huggingface.co/tencent/Hunyuan-A13B-Instruct) |
| ⭐ **ERNIE-4.5-300B-A47B** | ⭐ **78.4** | ⛔ **无** | ⛔ **无** | 38.8（**v6**，20240801–） | **M**（我本人 `pdf_extractor` 提取）· MMLU 86.5 · BBH 94.3 · [ERNIE 4.5 Tech Report](https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf) T5 ⚠️ **未上 arXiv** |
| ⭐ **Ling-1T** | ⭐ **82.04** | **72.98** | ⛔ **无** | 61.68（**窗口 2024-08–2025-05，454 题**） | **M**（我本人提取）· HLE 7.60 · [arXiv:2510.22115](https://arxiv.org/abs/2510.22115) T8（non-thinking）⛔ **arXiv HTML 版 §4.3 截断，必须走 PDF** |
| ⭐ **Command A (111B)** | ⭐ **69.6** | **50.8** | ⛔ **无** | 26.9（**v5**；Agentic 变体 32.9） | **M**（我本人提取）· **RULER 4k 97.2 → 128k 90.0 → 256k 84.6** · [arXiv:2504.00698](https://arxiv.org/abs/2504.00698) ⛔ **无 HTML 版、ar5iv 转换失败** |
| Step-3 | ⛔ **无** | 73.0 | ⛔ **无** | 67.1（**窗口 202408–202505**） | ⚠️ [arXiv:2507.19427](https://arxiv.org/abs/2507.19427) **只有解码成本/吞吐表，零质量分表** · [blog](https://chat.stepfun.com/research/en/step3) |
| dots.llm1.inst | 70.4 (EM) | 52.6 | ⛔ **无** | ⛔ 32.0（**未标版本**） | ⛔ HF card 本身无表 · [arXiv:2506.05767](https://arxiv.org/html/2506.05767v1) T5 |
| Granite-4.0-H-Small | 55.47 | 40.63 | ⛔ **无** | ⛔ **无** | ⚠️ **对比列全是 Granite 自家型号，⛔ 无任何外部模型** · [card](https://huggingface.co/ibm-granite/granite-4.0-h-small) |
| Intern-S1 | 83.5 | 77.3 | ⛔ **无** | ⛔ **无** | ChemBench 83.4 · [card](https://huggingface.co/internlm/Intern-S1) |

#### 1.4.4 ⛔ 单项缺口的分布（⛔ 这本身是一条可引的结论）

1. ⛔ **SWE-bench Verified 的缺席面极大。** **Meta（Llama 4 全线）· Google（Gemma 3 / 3n 全线）· Qwen（初代 + 2507 + Next 六张卡全无）· Phi-4 全家族 · Granite-4.0 · Command A · ERNIE-4.5 · Ling-1T · Step-3 · Intern-S1 · dots.llm1 · Hunyuan-A13B——一个都没报。** ⇒ ⛔ **想用 SWE-bench 横比 2025 世代是做不到的。**
2. ⛔ **MMLU-Pro 缺席**：QwQ-32B（**无任何厂商自报值**）· Qwen3 初代全线（后训练表用 **MMLU-Redux** 替代）· Nemotron-Nano-9B-v2 · Nemotron-Ultra-253B · Step-3 · Mistral Small 3 系无 SWE/LCB/AIME。
3. ⛔ **GPQA 缺席或口径不对**：ERNIE-4.5-300B（无）· Mistral Small 3（⛔ 只有 GPQA **Main** 45.3，无 Diamond）· Magistral 1.0（只写「GPQA」未标 Diamond）。
4. ⛔ **LCB 未标版本的 8 个**：Nemotron-Nano-9B-v2 · Hunyuan-A13B · dots.llm1 · MiniMax-M2 · DeepSeek-R1（原卡）· V3.1-Terminus · V3.2-Exp · Gemma 3 全线（⛔ 版本与窗口**都**没给，且报告内两表数字互相矛盾）。
5. ⛔ **「benchmark 表是图片」是本轮最主要的取数障碍，⛔ 且集中在中国厂商与 Mistral。** 命中：QwQ-32B（card + blog 全图）· Qwen3-Coder（SWE 表全图 + `qwen.ai` SPA 空壳，只返回单词 "Qwen"）· GLM-4.6（card + blog 全图 / SPA）· Mistral-Large-3（benchmark 表全是图片如 `4 Gpqa Diamond Accuracy`）。

#### 1.4.5 ⛔ 流传但拒绝登记的数字（⛔ 不得因为「网上都这么说」而回填）

1. ⛔ **`Qwen3-Coder-480B` 的 SWE-bench Verified 67.0 / 69.6@500turns**——检索摘要有，⛔ 但官方 blog 与 HF card 的 SWE 表全是图片、`qwen.ai/blog?id=qwen3-coder` 是 SPA 空壳，⇒ **未在任何亲自抓到的厂商页面上看到，按纪律不予登记。**
2. ⛔ **HF 页底部 "Evaluation results" widget 的数字全是社区提交，⛔ 非厂商自报**：`QwQ-32B` MMLU-Pro 69.07 · `V3.1-Terminus` GPQA 74.24 · `Gemma-3-27b` SWE-Pro 11.38 · `Command A` GPQA-D 50.51。⭐ **其中 `V3.1-Terminus` 的 74.24 与厂商自报 80.7 明显冲突，这正是「两类来源不可混」的现成例证。**
3. ⛔ **`Command A` 的 alphaxiv AI 生成概述**（MMLU 85.5 等）——⚠️ 虽与我 PDF 提取的一致，⛔ 但它是第三方转述，⇒ 已用一手 PDF 取代。

## 2. 按算力档归类（T1–T6）

### 2.1 ⛔ 判据（每个归档都由这一条产生，不看它就不要读下面的表）

**权重预算** $= 0.88 V$（$V$ = 标称显存总量），**KV cache 显式扣出**（30K 上下文、FP16 KV）。⛔ 该口径与 [compute_tiers.md](./compute_tiers.md) §1.1 和 [open_weight_model_compute.md](./open_weight_model_compute.md) §2.1 完全一致，三文可互查。⭐ **4×H200 一档不用 $0.88V$，直接用 [h200x4_envelope.md](./h200x4_envelope.md) 的细算结果 487 GB。**

⛔ **本节列出的是「能落进的最低档」**，即该模型**最小的可用官方件**所需的最小显存档。同一模型的 BF16 档往往要高 1–2 档，表中分行列出。

⛔ **四条会让本节失效的陷阱**：

1. ⛔ **表中标 `KV 未计入` 的行是乐观值。** 这些模型的 KV@30K 在上游未算出（`⏳`），本节按 KV = 0 归档；⇒ ⛔ **它们的真实档位可能高一档**。受影响最重的是 GQA 头数多、层数深的模型（`dots.llm1` 是 **32 个 KV 头**、62 层，KV 会很大）。
2. ⛔ **⚠️贴边（余量 < 10 GB）的格子不得据以选型。** 官方 issue [vllm-ascend#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 实测 DeepSeek-R1-W8A8 在 1024 GB 上 OOM，而按本口径它装得下——**真实常驻开销比 0.88 更重**。
3. ⛔ **T2 的显存总量不等于可用能力。** vLLM 官方警告逐字：无 NVLink 的多卡「**leverage pipeline parallelism instead of tensor parallelism**」，因为 TP 的 all-reduce 每层都做。消费卡与 PCIe 工作站卡多数无 NVLink。
4. ⛔ **T4a 的「128 GB」不是显存。** MegaCube / DGX Spark 的官方措辞是 `unified system memory`，CPU 与 GPU 共享；带宽 **273 GB/s** vs H200 的 **4.8 TB/s**，差 17.6×。⇒ ⛔ **按容量把它与 HBM 卡横比是错的**，它能装下 ≠ 它跑得动。

### 2.2 T1 单卡工作站（24–112 GB）

| 显存档 | 权重预算 | 2025 世代能落进的模型（体积 · 件的归属） |
| :-- | --: | :-- |
| **24 GB**（4090 / 5090 D v2） | **21.1 GB** | ⭐ **KV 已核者**：`gpt-oss-20b` 13.8+1.4 = **15.2**（余 5.9）· `Qwen3-8B-FP8` 9.4+4.1 = **13.5** · `Qwen3-8B` / `R1-0528-Qwen3-8B` 16.4+4.1 = **20.5** ⚠️贴边（余 0.6）。⚠️ **KV 未核者（⛔ 归档偏乐观）**：`gemma-3-27b-QAT-q4_0` **17.2** · `Qwen3-14B-FP8` 16.3 · `granite-4.0-h-tiny` 13.9 / `-micro` 6.4 · `Nemotron-Nano-9B-v2-FP8` 10.3 · `Ministral-3-8B(FP8)` 10.4 · `gemma-3n-E4B/E2B` 15.7 / 10.9 · Phi-4-mini 三型 7.7 · R1 蒸馏 1.5B/7B/8B 3.6 / 15.2 / 16.1 · `Qwen3-4B` 8.0 · `Qwen3-1.7B` 4.1 · `Qwen3-0.6B` 1.5 · `gemma-3-1b/270m` 2.0 / 0.5 · `ERNIE-4.5-0.3B` 0.7 |
| **32 GB**（5090 全球版） | **28.2 GB** | ⭐ **`Qwen3-32B-AWQ` / `QwQ-32B-AWQ` 19.3+7.3 = 26.6**（⭐ 作者 AWQ-INT4，余 1.6 ⚠️贴边）· `Qwen3-32B-Q4_K_M`（官方 GGUF）19.8+7.3 = **27.1** ⚠️贴边（余 1.1）· `QwQ-32B-q4_k_m` 19.9+7.3 = 27.2 ⚠️贴边 · `Qwen3-30B-A3B-Q4_K_M`（官方 GGUF）18.6+2.8 = **21.4**（余 6.8，本档最舒适）· `gemma-3-12b-it` 24.4（KV 未核）· `Nemotron-Nano-12B-v2` 24.6（KV 未核） |
| **48 GB**（RTX 6000 Ada / A6000 / MLU370-X8） | **42.2 GB** | `Qwen3-30B-A3B-Instruct-2507-FP8` / `Qwen3-Coder-30B-A3B-FP8` **31.2**（作者件）· `Qwen3-30B-A3B-FP8` 32.4 · `Qwen3-32B-FP8` 34.3 ⚠️贴边 · `Qwen3-14B` / `R1-Distill-Qwen-14B` 29.5 · Phi-4-reasoning(-plus) 29.3 · `Ministral-3-14B-Reasoning` 27.9 |
| **64 GB**（昇腾 910B 单卡） | **56.3 GB** | ⭐ **`Hunyuan-A13B-GPTQ-Int4` 42.7 GB**（⭐ 腾讯作者件，80B 总参 / 13B 激活）· `ERNIE-4.5-21B-A3B` 43.9 · Mistral Small 3.x / Devstral / Magistral 24B 系 47.1–48.5 · `Nemotron-Super-49B-v1-FP8` 52.0 · `gemma-3-27b-it` 54.9 ⚠️贴边 |
| **84 GB**（RTX 6000D 中国特供） | **73.9 GB** | ⭐ **`gpt-oss-120b` / `gpt-oss-safeguard-120b` 65.2 GB**（117B/5.1B，MXFP4 作者件）· `Seed-OSS-36B` 72.3（⭐ 原生 512K context）· `Qwen3-30B-A3B` / `Qwen3-Coder-30B-A3B` 61.1 · `Nemotron-3-Nano-30B-A3B` 63.2 · `granite-4.0-h-small` 64.4 · `Qwen3-32B` / `QwQ-32B` / `R1-Distill-Qwen-32B` / `Baichuan-M2-32B` 65.5 ⚠️贴边 · `Falcon-H1-34B` 67.3 |
| **96 GB**（RTX PRO 6000 Blackwell / Atlas 300I Duo） | **84.5 GB** | `Hunyuan-A13B-FP8` **80.9** ⚠️贴边（KV 未计入） |
| **112 GB**（Atlas 350 / Ascend 950PR） | **98.6 GB** | ⭐ **`Qwen3-Next-80B-A3B-Instruct-FP8` 82.1 GB**（81B 总参 / **3B 激活**，作者 FP8，262K 原生，余 13.7）⛔ **但昇腾不原生支持 FP8**，见 §3.3 |

⭐ **T1 一档的实质结论**：⛔ **2025 世代在 24 GB 上真正能跑的最强模型是 32B dense 的 4-bit 件**（`Qwen3-32B-AWQ` / 官方 `Q4_K_M`，19.3 / 19.8 GB），⛔ **而不是任何 MoE**——因为 MoE 的全部专家权重须常驻，`Qwen3-30B-A3B` 的 4-bit 也要 18.6 GB，与 32B dense 几乎一样大却只有 3B 激活。⇒ **在 24 GB 这一档，MoE 的稀疏优势换不到容量优势，只换到 decode 速度优势。**

### 2.3 T2 单机多卡（48–384 GB）· T3 单节点服务器（192–1128 GB）

| 档 | 权重预算 | 2025 世代能落进的最低档模型 |
| :-- | --: | :-- |
| **T2 · 192 GB**（4×48 或 2×96） | **169.0 GB** | `GLM-4.5-Air-FP8` **112.6**（作者件，106B/12B，余 51.1 ⭐ 舒适）· `Hunyuan-A13B-Instruct` 160.8 ⚠️贴边 · `Qwen3-Next-80B-A3B` BF16 162.7 ⚠️贴边 |
| **T2 · 384 GB**（4×96 Blackwell / 8×L40S） | **337.9 GB** | ⭐ **`Qwen3-235B-A22B-Instruct-2507-FP8` 236.4**（作者件，余 96.1）· `MiniMax-M2` **230.1**（原生 FP8）· `Intern-S1-FP8` 249.1 · `dots.llm1.inst` 285.6 · `GLM-4.5-Air` BF16 220.9 · Command A / A-Reasoning / A-Vision 222–224（⛔ 均 CC-BY-NC 不可商用） |
| **T3 · 564 GB**（⭐ 4×H200） | ⭐ **487.0 GB** | 见 §3 专章 |
| **T3 · 640 GB**（8×H100 = DGX H100） | **563.2 GB** | `Nemotron-Ultra-253B` 506.8（BF16，253B dense） |
| **T3 · 768 GB**（8×H20） | **675.8 GB** | ⭐ **`Kimi-K2-Thinking` 594.2**（1T/32B，原生 INT4 QAT 作者件，余 79.6）· `ERNIE-4.5-300B-A47B` 601.0 · `step3` 641.9 |
| **T3 · 1128 GB**（8×H200 = DGX H200） | **992.6 GB** | `MiniMax-M1` / `MiniMax-Text-01` BF16 912–915 · `Qwen3-Coder-480B` BF16 960.3 |

### 2.4 T4a 桌面一体机（128 / 252 GB）

⛔ **先读 §2.1 第 4 条**：128 GB 是 `unified system memory`，273 GB/s，⛔ 不是显存。

| 产品 | 权重预算 | 2025 世代模型 |
| :-- | --: | :-- |
| MegaCube / DGX Spark（128 GB 统一内存） | **112.6 GB** | `Kimi-Linear-48B-A3B` 98.2 · `Nemotron-Super-49B-v1(.5)` 99.7 · 以及全部 T1 档模型 |
| DGX Station（**252 GB HBM3e** + 496 GB LPDDR5X） | **221.8 GB**（仅 HBM） | `Ling-flash-2.0` 205.8 · `Llama-4-Scout` 217.3 ⚠️贴边 |

⚠️ **一条与官方标称的对照**：MegaCube 官方逐字 `"A single LinSeer MegaCube can support inference for 200B parameter models."`，⛔ 但未说明精度档与上下文长度。按本文口径 112.6 GB 预算在 4-bit 下可容 ~198B 总参——数字接近，⛔ **但不可当成互证**（**I**）。⚠️ 另一条官方逐字 `"Supports fine-tuning and inference for the Deepseek R1 70B model."` 指的正是本表里的 `DeepSeek-R1-Distill-Llama-70B`（141.1 GB BF16），⇒ **它在 112.6 GB 预算下必须走 4-bit**。

### 2.5 T4b 训推一体机 · T5 国产加速卡节点 · T6 小集群

| 档 | 权重预算 | 2025 世代模型 |
| :-- | --: | :-- |
| **T5 · 512 GB**（1 台 Atlas 800I A2 = 8×910B） | **450.6 GB** | ⭐ **`GLM-4.6-FP8` / `GLM-4.7-FP8` 354.9**（余 85.2）· `GLM-4.5-FP8` 361.3 · `Llama-4-Maverick-FP8` 416.8 · `Mistral-Large-3-NVFP4` 403.1（⛔ 格式，见 §3） |
| **T5 · 896 GB**（8×Atlas 350） | **788.5 GB** | ⭐ **`DeepSeek-R1` / `R1-0528` / `V3-0324` / `V3.1` / `V3.1-Terminus` FP8 688.6** · `DeepSeek-V3.2(-Exp/-Speciale)` 689.5 · `GLM-4.5/4.6/4.7` BF16 705.6–716.7 · `Mistral-Large-3-2512` FP8 681.5 |
| **T5 · 1024 GB**（1 台 Atlas A3 节点 = 8 NPU / 16 die） | **901.1 GB** | `Llama-4-Maverick` BF16 803.2 · 以上全部 |
| **T4b · 1536 GB**（浪潮 NF5868G8） | **1351.7 GB** | ⭐ **`Kimi-K2-Instruct` / `-Base` / `-0905` FP8 1029.2**（1T/32B，⛔ 这是 2025 世代 FP8 档里最大的一个） |
| **T6 · 2048 GB**（2 台 Atlas 800I A2 ×2） | **1802.2 GB** | `Mistral-Large-3` BF16 1352.0 |
| ⛔ **超出 T6 · 2048 GB** | — | ⛔ **`Ling-1T` / `Ring-1T` BF16 1999.4 GB**（999.7B 总参，⛔ **作者侧零量化件**）——它们在本仓库的任何档位下都装不下，需 ≥ 2272 GB |

⭐ **T5 一档有官方部署证据，⛔ 且它方向上不利于「算力不可得」叙事，必须一起摆出**：**671B MoE 在昇腾上的官方最低门槛是「2 台 Atlas 800I A2（16 × 64 GB = 1024 GB）跑 W8A8」**，MindIE 与 vLLM-Ascend 两条独立路径口径一致（**M**，见 [compute_tiers.md](./compute_tiers.md) §1.7）。⇒ ⛔ **DeepSeek-R1 级私域部署不需要 CloudMatrix384，两台国产整机就够。**

⛔ **但 T5 有一条格式硬约束会打掉本节一半的行：昇腾不原生支持 FP8。** 官方口径是 **W8A8 / W4A4**。⇒ ⛔ **上表里凡依赖官方 FP8 件的行（`GLM-4.x-FP8`、`DeepSeek-*` 全系、`Qwen3-*-FP8`、`MiniMax-M2`、`Kimi-K2` FP8 档、`Hunyuan-A13B-FP8`、`Intern-S1-FP8`）在 T5 上不可直接套用**，须走昇腾自己的 W8A8 量化路径重新出件。

## 3. 4×H200 可行性标注

### 3.1 ⛔ 两条判据，缺一不可

沿用 [h200x4_envelope.md](./h200x4_envelope.md) 与 [h200x4_inference_perf.md](./h200x4_inference_perf.md) 的口径：

1. **容量判据**：$V = 564$ GB 标称 → 权重预算 ⭐ **487 GB**（$0.92V = 518.88$，扣 20 GB 的 30K KV 上界与 12 GB 的激活 + CUDA graph + NCCL）。
2. ⭐ **格式判据（⛔ 这一条独立于容量，且更容易被漏）**：⛔ **H200 是 Hopper（compute capability 9.0），不是 Blackwell。** 把模型压小所依赖的 4-bit 浮点格式，其高性能内核多为 Blackwell 原生；在 Hopper 上走 Marlin 回退 —— **省显存不省速度**。

| 格式 | Hopper（H200）原生 | 依据（引自 [h200x4_envelope.md](./h200x4_envelope.md) §4.3） |
| :-- | :-: | :-- |
| **BF16** | ✅ | — |
| **FP8（e4m3）** | ✅ | Hopper 有 FP8 张量核；GLM-4.5 card 前置条件逐字要求「devices that natively support FP8 inference」并把 H200 列入 |
| **GPTQ / AWQ INT4** | ✅（Marlin 内核） | SGLang DeepSeek 表把 `AWQ` 与 `4× H200` 并列 |
| ⛔ **MXFP4** | ⚠️ **能跑，⛔ 但省显存不省算力** | ⭐ **本轮从 vLLM 源码裁定，⛔ 不再是「存疑」**，见 §3.3 |
| ⛔ **NVFP4** | ⛔ **非原生** | 五条官方逐字一致指向 Blackwell；Hopper 只有 Marlin 回退。⭐ 本轮另从 vLLM 文档拿到逐字，见 §3.3 |
| ⛔ **MXFP8** | ⛔ **存疑** | ⛔ SGLang 与 vLLM 两源冲突，上游未裁定。⚠️ **但 2025 世代零个 MXFP8 件，⇒ 这一行对本表不适用** |
| ⭐ **INT4（compressed-tensors QAT）** | ✅ | ⭐ **本轮新核到**：vLLM 官方 `Kimi-K2-Think` recipe 逐字 `"You can use 8x H200/H20 to launch this model"` ⇒ **INT4 QAT 在 Hopper 上是官方支持路径，⛔ 不需要 Blackwell** |

⭐ **一条对 2025 世代有利的结构性事实（本轮发现）**：**2025 世代基本上没赶上 FP4 那一波**——本表 100+ 个条目里，**NVFP4 官方件只有 1 个**（`Mistral-Large-3-675B-Instruct-2512-NVFP4`）、**MXFP8 官方件 0 个**、MXFP4 官方件 4 个（gpt-oss 四型）。⛔ 其余全是 BF16 / FP8 / INT4-AWQ / INT4-GPTQ，**而这四种在 Hopper 上都是原生的**。⇒ **「格式判据」这一条几乎不打击 2025 世代，而它打掉了 2026 世代容量排序的前三名**（`GLM-5.2-NVFP4` / `Motif-3-NVFP4` / `MiniMax-M3-MXFP8`）。**这是「稍早的模型对 4×H200 更友好」这个论点最硬的一条支撑，⛔ 且它与「生态成熟度」是两件独立的事。**

### 3.2 ✅ 可用（容量 ≤ 487 GB 且格式在 Hopper 原生）

| 模型 | 件 | 体积 | 余量 | 归属 | 许可 | AA v4.1.1 |
| :-- | :-- | --: | --: | :-- | :-- | --: |
| ⭐ **Qwen3-235B-A22B-Instruct-2507** | 作者 FP8 | **236.4** | ⭐ **245.2** | ✅ 作者 | Apache-2.0 | ⏳ |
| Qwen3-235B-A22B（2504 版） | 作者 FP8 | 239.0 | 242.6 | ✅ 作者 | Apache-2.0 | ⏳ |
| ⭐ **MiniMax-M2** | 原生 FP8 | **230.1** | 249.8 | ✅ 作者 | ⛔ 自定义 | ⏳ |
| **Intern-S1** | 作者 FP8 | 249.1 | 237.9 | ✅ 作者 | Apache-2.0 | ⏳ |
| dots.llm1.inst | BF16 | 285.6 | 201.4 | ✅ 作者 | MIT | ⏳ |
| ⭐ **step3**（本轮更正并入） | ⭐ **作者 FP8** | **327.6** | 159.4 | ✅ **作者** | **Apache-2.0** | ⏳ |
| ⭐ **GLM-4.6** / **GLM-4.7** | 作者 FP8 | **354.9** | 121.6 | ✅ 作者 | **MIT** | GLM-4.7 = **34.46** |
| **GLM-4.5** | 作者 FP8 | 361.3 | 115.2 | ✅ 作者 | **MIT** | ⏳ |
| Llama-4-Maverick | 作者 FP8 | 416.8 | 70.2 | ✅ 作者 | ⛔ 社区许可 | **14.48** ⛔ 极低 |
| Qwen3-235B-A22B-Thinking-2507 | BF16 | 470.2 | 11.4 | ✅ 作者 | Apache-2.0 | ⏳ |
| Qwen3-235B-A22B（2504） | BF16 | 470.2 | 11.4 | ✅ 作者 | Apache-2.0 | ⏳ |
| ⚠️ Intern-S1 | BF16 | 481.4 | **5.6** ⚠️贴边 | ✅ 作者 | Apache-2.0 | ⏳ |
| ⚠️ **Qwen3-Coder-480B-A35B** | 作者 FP8 | **482.1** | ⛔ **4.9** ⚠️贴边 | ✅ 作者 | Apache-2.0 | ⏳ |
| GLM-4.5-Air | 作者 FP8 / BF16 | 112.6 / 220.9 | 374.4 / 266.1 | ✅ 作者 | **MIT** | ⏳ |
| Llama-4-Scout | BF16 | 217.3 | 269.7 | ✅ 作者 | ⛔ 社区许可 | ⏳ |
| Ling-flash-2.0 | BF16 | 205.8 | 281.2 | ✅ 作者 | MIT | ⏳ |
| Hunyuan-A13B | 作者 FP8 / GPTQ-Int4 / BF16 | 80.9 / 42.7 / 160.8 | 舒适 | ✅ 作者 | ⛔ 自定义 | ⏳ |
| Qwen3-Next-80B-A3B | 作者 FP8 / BF16 | 82.1 / 162.7 | 舒适 | ✅ 作者 | Apache-2.0 | ⏳ |
| Seed-OSS-36B | BF16 | 72.3 | 舒适 | ✅ 作者 | Apache-2.0 | ⏳ |
| Command A / A-Reasoning / A-Vision | BF16 / F16 | 222–224 | 舒适 | ✅ 作者 | ⛔ **CC-BY-NC 不可商用** | ⏳ |
| Nemotron-Super-49B-v1(.5) | 作者 FP8 / BF16 | 52.0 / 99.7 | 舒适 | ✅ 作者 | ⛔ NVIDIA 自定义 | ⏳ |
| 全部 T1 / T2 档模型（Qwen3 全档、Mistral Small 3.x 全档、Gemma 3 全档、Phi-4 全档、granite-4.0、R1 蒸馏全档、Kimi-Linear、Falcon-H1、MiniMax 除 M1、ERNIE-4.5 除 300B、Ministral-3、Nemotron-Nano 全档、Baichuan-M2） | 各自最小件 | ≤ 249 | 舒适 | ✅ 作者 | 见 §1 | ⏳ |

⭐ **§3.2 的首选是 `Qwen3-235B-A22B-Instruct-2507-FP8`**：**作者件 · FP8 在 Hopper 原生 · Apache-2.0 真可商用 · 262K 原生 context · 余量 245 GB（可用于更长 KV 或更大 batch）**。⛔ 唯一遗憾是它没有 AA v4.1.1 分数（见 §6）。

### 3.3 ⚠️ 可用但慢（装得下，⛔ 但格式在 Hopper 上走回退）

| 模型 | 件 | 体积 | ⛔ 问题 |
| :-- | :-- | --: | :-- |
| ⛔ **gpt-oss-120b** / **-safeguard-120b** / **-20b** / **-safeguard-20b** | 原生 **MXFP4** | 65.2 / 13.8 | ⭐ **本轮裁定完成，⛔ 首版记为「两源冲突」是错的。** 见下方三条逐字 |
| ⛔ **Mistral-Large-3-675B-2512-NVFP4** | 作者 **NVFP4** | 403.1 | ⛔ **NVFP4 非 Hopper 原生。** vLLM `modelopt.md` 逐字：「**On GPUs without a supported native FP4 GEMM kernel, vLLM falls back to weight-only (W4A16) execution via Marlin and logs a warning; this may reduce throughput for compute-heavy workloads.**」⛔ 其 FP8 档是 681.5 GB，装不下 |

⭐ **MXFP4 在 Hopper 上的裁定（⛔ 更正首版）**：⛔ **它能跑，但 FP4 张量核不参与——权重在算之前被反量化，激活始终 BF16。** 三条逐字（全部取自 vLLM `main`，核验日 2026-08-13）：

1. 后端选择器 [`fused_moe/oracle/mxfp4.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/fused_moe/oracle/mxfp4.py) 的 `_get_priority_backends()` docstring 逐字：「SM100+ prefers DeepGEMM FP4 / TRTLLM MXFP8; **SM90 falls through to Triton_unfused or Marlin**」。⭐ **SM90 就是 Hopper。**
2. [`quantization/mxfp4.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/quantization/mxfp4.py) 注释逐字：「Canonical `mxfp4` checkpoints are weight-only W4A16 … preserve BF16 activations while **the fallback dequantizes only the weights**」；同文件 `get_supported_act_dtypes()` **硬返回 `[torch.bfloat16]`**。
3. 已合并 PR 的标题本身就是这个语义：[#23369 「bf16 x mxfp4 cutlass fused moe for gpt-oss on hopper」](https://github.com/vllm-project/vllm/pull/23369)。

⇒ ⭐ **对本项目的含义**：gpt-oss 的 **65.2 GB 是真的省下来了**（权重以 MXFP4 常驻），⛔ **但 MoE GEMM 的算力收益为零**。⛔ **且 Marlin 回退路径在 Hopper 上还有未关闭的崩溃 issue**：[#47769「MXFP4 MoE Marlin fallback crashes with illegal memory access on Hopper」](https://github.com/vllm-project/vllm/issues/47769)（**open**）。**另有一条会害人的过时建议：`VLLM_MXFP4_USE_MARLIN=1` 这个环境变量已从 `vllm/envs.py` 移除**（本轮 `grep MXFP4` 零命中），⇒ **照抄旧帖设它是无效的。**

⛔ **一条必须如实交代的取证缺口（⛔ 不要把它说成已闭合）**：**「Hopper 没有 FP4 张量核」这句话，在 NVIDIA 官方文档里找不到显式否定句。** 能引的只有正面陈述——「NVFP4 … **introduced with the NVIDIA Blackwell GPU architecture**」「Blackwell **fifth-generation Tensor Core** … implements NVFP4」（[NVIDIA 官方博客](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)）。⚠️ **更麻烦的是 TensorRT-LLM 文档有一句会被误读的话**：「The default PyTorch backend supports FP4 and FP8 quantization on the latest **Blackwell and Hopper** GPUs」——它讲的是 checkpoint 可加载 / 可量化，不是原生数学通路，**但字面上把 Hopper 与 FP4 放在一起了**。⇒ ⭐ **本文的裁定依据是引擎行为侧（vLLM / LLM Compressor 的 W4A16 回退，M 级实证），不是 NVIDIA 的否定句。**

⛔ **2025 世代受格式判据影响的条目一共只有 5 个**（4 个 MXFP4 + 1 个 NVFP4），⛔ **且 MXFP8 为零**。⇒ 与 2026 世代的对照见 §3.1。

### 3.4 ⛔ 不可用

**（a）⛔ 因容量超出 487 GB**（⛔ 且作者侧无更小的件）：

| 模型 | 最小可用件 | 体积 | 超预算 | ⛔ 有无更小的作者件 |
| :-- | :-- | --: | --: | :-- |
| ⛔ **DeepSeek-R1 / R1-0528 / R1-Zero / V3-0324 / V3.1 / V3.1-Terminus** | 原生 FP8 | **688.6** | **+201.6** | ⛔ **无。DeepSeek 官方 2025 年零个 4-bit 件** |
| ⛔ **DeepSeek-V3.2 / -Exp / -Speciale** | 原生 FP8 | **689.5** | +202.5 | ⛔ 同上无 |
| ⛔ **Kimi-K2-Instruct / -Base / -0905** | 原生 FP8 | **1029.2** | +542.2 | ⚠️ 有——但那是**另一个模型**（`Kimi-K2-Thinking` INT4 594.2），⛔ 仍超 107.2 GB |
| ⛔ **Kimi-K2-Thinking** | 原生 **INT4 QAT** | **594.2** | **+107.2** | ⛔ **它已经是 INT4 了。** `moonshotai` 名下零个独立量化仓库 |
| ⛔ **GLM-4.5 / 4.6 / 4.7（BF16 档）** | BF16 | 705.6–716.7 | +219–230 | ✅ 有——作者 FP8 354.9–361.3（见 §3.2） |
| ⚠️ **ERNIE-4.5-300B-A47B**（BF16 档） | BF16 | **601.0** | +114.0 | ⭐ **本轮核到作者 W4A8C8 件 `ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle` = 168.6 GB**，⛔ **但它是 Paddle 格式，⛔ 不是 HF / vLLM 直接可用的件**（`baidu` 名下另有 `-FP8-Paddle`）。⇒ ⛔ **按「作者件 + 引擎可用」双条件仍判不可用**，⚠️ 若接受 PaddlePaddle 栈则它装得下 |
| ⭐ ~~**step3**~~ **已移出本节** | ⭐ **作者 FP8** | **327.6 GB** | **余 159.4** | **本轮更正：`stepfun-ai/step3-fp8`（2025-07-31，Apache-2.0）实测 327.6 GB，⇒ 它装得下，已并入 §3.2。** ⛔ 首版把它列为「不可用 · BF16 641.9 GB · 更小件待核」是错的 |
| ⛔ **Nemotron-Ultra-253B** | BF16 | **506.8** | ⛔ **+19.8** ⚠️ **只差 19.8 GB** | ⏳ 待核作者 FP8 件（NVIDIA 为 Super-49B 发了 FP8，⛔ Ultra 本轮未核到） |
| ⛔ **Mistral-Large-3-2512** | 原生 FP8 | 681.5 | +194.5 | ⚠️ 有——NVFP4 403.1，⛔ 但格式判据否掉（§3.3） |
| ⛔ **Mistral-Large-3**（0928 版） | BF16 | **1352.0** | +865.0 | ⛔ 无 |
| ⛔ **Llama-4-Maverick（BF16 档）** | BF16 | 803.2 | +316.2 | ✅ 有——作者 FP8 416.8 |
| ⛔ **Qwen3-Coder-480B（BF16 档）** | BF16 | 960.3 | +473.3 | ✅ 有——作者 FP8 482.1 ⚠️贴边 |
| ⛔ **MiniMax-M1-40k / -80k / MiniMax-Text-01** | BF16 | 912.2–914.7 | +425–428 | ⛔ **无。** ⚠️ 注意 M1 是 **45.9B 激活参**，是本表激活参最多的模型之一 |
| ⛔ **Ling-1T / Ring-1T** | BF16 | ⛔ **1999.4** | ⛔ **+1512.4** | **无，作者侧零量化件。** 超预算 **4.1 倍** |

⛔ **本节最重要的一条否定事实，且它直接冲击「用 2025 世代」这个方案**：⛔ **DeepSeek R1 / V3.1 / V3.2 全系在 4×H200 上装不下，且 DeepSeek 官方在 2025 年一个 4-bit 件都没发。** ⇒ **想在 4×H200 上跑 DeepSeek 只能走三方件**（社区 AWQ / GPTQ / GGUF），**而那不是作者件**。⭐ **对照：Qwen 与 Z.ai 都发了作者 FP8，两家的旗舰都装得下。** ⇒ **在 4×H200 这个约束下，「选 Qwen3-235B 或 GLM-4.6」与「选 DeepSeek」不是同一类决策——后者要么换硬件，要么放弃作者件。**

**（b）⛔ 因许可不可商用**（容量与格式都没问题，⛔ 但用不了）：

`CohereLabs/c4ai-command-a-03-2025` · `command-a-reasoning-08-2025` · `command-a-vision-07-2025`，三者均 ⛔ **CC-BY-NC-4.0**。⚠️ **一条方向相反的对照必须一起给**：Cohere 在 **2026** 版 `command-a-plus-05-2026` 上改成了 **Apache-2.0**，⇒ ⛔ **「Command A 不可商用」这个判断只对 2025 版成立，不可外推。**

## 4. 生态成熟度对照

### 4.1 ⛔ 查法（⛔ 不看它就不要读下面的 ✅）

1. **vLLM**：拉 `main` 分支的 [`docs/models/supported_models.md`](https://raw.githubusercontent.com/vllm-project/vllm/main/docs/models/supported_models.md)（748 行），按 `config.json` 里的 `architectures[0]` **逐字符串精确匹配**。⭐ 该文件的两个 ✅ 列分别是 **LoRA** 与 **PP（pipeline parallelism）**，⛔ **不是「支持 / 不支持」**——⛔ 出现在表里就等于支持，两个 ✅ 是附加能力。**但文档页不是最硬的源**：并行核验路直接读了 [`vllm/model_executor/models/registry.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/models/registry.py)，**它有一个文档页里看不到的 `_PREVIOUSLY_SUPPORTED_MODELS` 字典，会写出「最后可用版本号」**——⇒ **这把「未列入」细化成了「曾支持、已移除、末版是哪个」**，见 §4.4。
2. **SGLang**：列 `main` 分支的 [`python/sglang/srt/models/`](https://github.com/sgl-project/sglang/tree/main/python/sglang/srt/models) 目录（**216 个 `.py` 模块**），按模块名匹配。⭐ **这是引擎自己的模型注册表，比文档页更硬**（文档页本轮 404，见 §6）。
3. **社区量化件**：见 §5.3 的查法与其模糊匹配局限。

⛔ **本节不回答「跑得多快」**，只回答「引擎认不认这个架构」。速度问题在 [h200x4_inference_perf.md](./h200x4_inference_perf.md)。

### 4.2 主表

| 模型 / 架构族 | `architectures[0]` | vLLM | SGLang 模块 | GGUF 命中 | AWQ 命中 | 备注 |
| :-- | :-- | :-: | :-- | --: | --: | :-- |
| **Qwen3 dense**（0.6B–32B、QwQ-32B） | `Qwen3ForCausalLM` / `Qwen2ForCausalLM` | ✅ LoRA+PP | `qwen3` / `qwen2` | ⭐ 336–515 | 26–65 | ⭐ **生态最成熟的一族** |
| **Qwen3 MoE**（30B-A3B、235B-A22B、Coder-480B） | `Qwen3MoeForCausalLM` | ✅ LoRA+PP | `qwen3_moe` | ⭐ **632** | 12–78 | ⭐ 同上 |
| ⚠️ **Qwen3-Next-80B-A3B** | `Qwen3NextForCausalLM` | ✅ LoRA+PP | `qwen3_next`（另有 `qwen3_next_mtp`） | 65 | ⏳ | ⚠️ **混合注意力是 2025 新算子**，两引擎都已收，⛔ 但社区件只有 65 |
| **DeepSeek R1 / V3.x** | `DeepseekV3ForCausalLM` | ✅ LoRA+PP（card 逐字列 `DeepSeek-V3`, `DeepSeek-R1`, `DeepSeek-V3.1`） | `deepseek_v2` / `deepseek` / `deepseek_nextn` | 185（32B 蒸馏） | ⭐ **192** + GPTQ 94 | ⭐ **社区量化最丰富的一族**（含 `amd` 官方 11 个） |
| ⭐ **Kimi K2 全系** | `DeepseekV3ForCausalLM`（⭐ **与 DeepSeek 同架构**） | ✅ 经 DeepSeek 路径 | `deepseek_v2`（⛔ 无独立 `kimi_k2` 模块） | ⛔ 21 | ⛔ **0** | **它复用 DeepSeek 的引擎路径，这是它最大的生态优势**；但量化件几乎没有 |
| **GLM-4.5 / 4.6 / 4.7** | `Glm4MoeForCausalLM` | ✅ LoRA+PP（card 逐字 `GLM-4.5, GLM-4.6, GLM-4.7`） | `glm4_moe`（+ `glm4_moe_nextn`） | 43 | 6–7 | ⭐ 两引擎都点名到 4.7 |
| **gpt-oss 全系** | `GptOssForCausalLM` | ✅ LoRA+PP（card 逐字 `openai/gpt-oss-120b`, `gpt-oss-20b`） | `gpt_oss` | 130 / **479** | — | ⚠️ MXFP4 在 Hopper 的裁定见 §3.3 |
| **Gemma 3 / 3n** | `Gemma3ForConditionalGeneration` | ✅ | `gemma3_causal` / `gemma3_mm` / `gemma3n_*` | **400** | 10 | ⭐ 官方 QAT GGUF 是加分项 |
| **Llama 4 Scout / Maverick** | `Llama4ForConditionalGeneration` | ✅ | `llama4` / `mllama4` | 40 | ⛔ **1** | ⛔ **AWQ 只有 1 个** |
| **Nemotron-H（Nano v2 / 3-Nano）** | `NemotronHForCausalLM` | ✅ LoRA+PP | `nemotron_h` / `nemotron_h_mtp` | ⏳ | ⏳ | ⚠️ 混合 Mamba 算子，两引擎都已收 |
| **Nemotron-Super / -Ultra** | `DeciLMForCausalLM` | ✅ LoRA+PP（card 逐字 `nvidia/Llama-3_3-Nemotron-Super-49B-v1`） | `nemotron_nas` | ⏳ | ⏳ | ⭐ NAS 剪枝架构已被两引擎收 |
| **Hunyuan-A13B** | `HunYuanMoEV1ForCausalLM` | ✅ LoRA+PP（card 逐字含 `-FP8` 变体） | `hunyuan` | ⛔ 14 | ⏳ | ⭐ 官方 GPTQ-Int4 弥补社区件少 |
| ⚠️ **Seed-OSS-36B** | `SeedOssForCausalLM` | ✅ LoRA+PP（card 逐字 `ByteDance-Seed/Seed-OSS-36B-Instruct`） | ⛔ **无模块** | 51 | 3 | ⛔ **vLLM 有、SGLang 没有**——单引擎依赖 |
| **Ling / Ring**（`BailingMoeV2`） | `BailingMoeV2ForCausalLM` | ✅ LoRA+PP（⚠️ card 举例是 `Ling-mini-2.0`，⛔ 不是 1T 档） | `bailing_moe` / `_linear` / `_nextn` | ⏳ | ⏳ | ⛔ 作者侧零量化件 |
| **ERNIE-4.5** | `Ernie4_5_MoeForCausalLM` | ✅ LoRA+PP（card 逐字含 21B 与 300B 两档） | `ernie4` / `ernie45_moe_vl` | ⏳ | ⏳ | ⭐ 两引擎点名到 300B |
| **Granite 4.0** | `GraniteMoeHybridForCausalLM` | ✅ LoRA+PP | `granitemoehybrid` | 25（⭐ **含官方 2 个**） | ⏳ | ⭐ 少数有官方 GGUF 的西方厂商 |
| **MiniMax-M2** | `MiniMaxM2ForCausalLM` | ✅ LoRA+PP | `minimax_m2` | 172 | 37 | ⭐ 生态良好 |
| **Intern-S1** | `InternS1ForConditionalGeneration` | ✅ LoRA+PP | `interns1` | ⏳ | ⏳ | — |
| **Falcon-H1** | `FalconH1ForCausalLM` | ✅ LoRA+PP | `falcon_h1` | ⏳ | ⏳ | ⛔ 许可非 Apache |
| **Kimi-Linear-48B-A3B** | `KimiLinearForCausalLM` | ⚠️ **只有 PP，⛔ LoRA 列为空** | `kimi_linear` | ⏳ | ⏳ | ⚠️ **线性注意力是 2025 新算子**；⛔ 若需 LoRA 微调，vLLM 当前不支持 |
| **Step-3** | `Step3VLForConditionalGeneration` | ✅ | `step3_vl` / `step3_vl_10b` | ⏳ | ⏳ | ⚠️ 多模态 |
| **Mistral Small 3.x / Ministral-3 / Magistral / Devstral / Large-3** | `MistralForCausalLM` / `Mistral3ForConditionalGeneration` | ✅ | `mistral` / `ministral3` / `mistral_large_3` | 49 | 4 | ⭐ 两引擎都有专门模块 |
| **Phi-4-mini / -reasoning** | `Phi3ForCausalLM` | ✅ LoRA+PP | `phi` / `phi3_small` | ⏳ | ⏳ | — |
| **Phi-4-multimodal** | `Phi4MMForCausalLM` | ✅ LoRA+PP | `phi4mm` | ⏳ | ⏳ | — |
| ⛔ **Phi-4-mini-flash-reasoning** | `Phi4FlashForCausalLM` | ⛔ **未列入** | ⛔ **无模块** | ⏳ | ⏳ | **两引擎都不认** |
| ⛔ **dots.llm1**（小红书） | `Dots1ForCausalLM` | ⛔ **未列入**（⚠️ 表里只有 `DotsOCRForCausalLM`） | ⛔ **无模块**（只有 `dots_ocr` / `dots_vlm`） | ⏳ | ⏳ | **两引擎都不认** |
| ⛔ **MiniMax-M1-40k / -80k / MiniMax-Text-01** | `MiniMaxM1ForCausalLM` / `MiniMaxText01ForCausalLM` | ⛔ **未列入**（⚠️ 表里只有 M2、M3、VL-01） | ⛔ **无模块**（只有 `minimax_m2` / `_m3` / `_vl_common`） | ⏳ | ⏳ | **两引擎都已把它们移出注册表** |

### 4.3 ⭐ 四条结论

1. ⭐ **「2025 世代生态成熟」这个论点大部分成立，⛔ 但有三个明确反例。** 两个独立引擎（vLLM 文档 + SGLang 模型注册表）**一致不支持** `dots.llm1`、`MiniMax-M1` / `MiniMax-Text-01`、`Phi-4-mini-flash-reasoning`。⛔ **两源独立一致，⇒ 这不是文档滞后，是真的没有路径。**
2. ⛔ **`MiniMax-M1` 的情形尤其要记：它曾经被支持过，现在被移出了。** 注册表里 M2、M3 都在，M1 与 Text-01 都不在。⇒ ⭐ **「2025 世代生态更成熟」这个假设有一个反向失效模式：老模型会被引擎淘汰。** ⛔ 这与「新模型还没被支持」是**方向相反**的风险，选型时两头都要查。
3. ⭐ **Kimi K2 有一个被低估的生态优势**：它的 `architectures[0]` 就是 `DeepseekV3ForCausalLM`，⇒ **它直接复用 DeepSeek 的引擎路径，不需要任何新算子**。⛔ 但它的量化件几乎为零（21 个 GGUF、**0 个 AWQ**）。⇒ ⛔ **「引擎支持」与「量化件可得」是两件独立的事，不能互相代替。**
4. ⚠️ **`Seed-OSS-36B` 是单引擎依赖**：vLLM 有 `SeedOssForCausalLM`，⛔ SGLang 的 216 个模块里没有对应项。⇒ ⛔ **它 512K 原生 context 这个优点要以「只有一条引擎路径」为代价。**

### 4.4 ⭐ 并行核验路的三条更正与补强（⛔ 更正 §4.2 / §4.3）

#### 4.4.1 ⭐ 「未列入」应细化为「曾支持、已移除、末版号」

⭐ **vLLM `registry.py` 有一个文档页看不到的 `_PREVIOUSLY_SUPPORTED_MODELS` 字典**，⇒ 首版 §4.2 里两条「⛔ 未列入」应更正为：

| 模型 | ⛔ 首版写法 | ⭐ 更正后 |
| :-- | :-- | :-- |
| **dots.llm1**（`Dots1ForCausalLM`） | ⛔「未列入」 | ⭐ **在 `_PREVIOUSLY_SUPPORTED_MODELS` 中，⭐ 最后可用版本 `v0.23.0`**；SGLang 侧 **issue 检索零命中**（连 PR 都没有）。**但 llama.cpp 有 `LLM_ARCH_DOTS1`** ⇒ **它不是完全没路，只剩 llama.cpp 一条** |
| **MiniMax-M1** / **MiniMax-Text-01** | ⛔「未列入」 | ⭐ **同在 `_PREVIOUSLY_SUPPORTED_MODELS`，末版 `v0.23.0`**；SGLang 侧 **PR #11466 已关闭、#8124 仍 open**；⛔ **llama.cpp 也无 arch（只有 `MINIMAX_M2` / `M3`）** ⇒ ⛔ **三引擎全线不可用，这是本表最坏的一格** |

⭐ **`Seed-OSS` 的单引擎依赖也拿到了机制**：SGLang 侧 **PR #30930 仍 open**（⛔ 不是「没人提」，是「提了没合」），⛔ 而 vLLM 侧有官方 recipe `Seed/Seed-OSS-36B.md`。⇒ **这个落差是「一家有官方 recipe、另一家 PR 挂着」，比首版说的「有 / 没有」更准。**

⚠️ **另一条首版没写的移除记录**：`Phi4MultimodalForCausalLM` **也在移除名单里（末版 `v0.12.0`）**；⚠️ 但 `Phi4MMForCausalLM`（即 `microsoft/Phi-4-multimodal-instruct` 实际用的那个）**仍在册**，⇒ ⛔ **两个名字只差两个字母，⛔ 不要混。**

#### 4.4.2 ⭐ llama.cpp 是被首版漏掉的第三条腿

⭐ 按 [`src/llama-arch.cpp`](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-arch.cpp) 的 `LLM_ARCH_*` 表（当前 **143 条**）核：

| 有 arch ✅ | 无 arch ⛔ |
| :-- | :-- |
| `QWEN3` · `QWEN3MOE` · `QWEN3NEXT` · `DEEPSEEK2`（R1 / V3.1 / **Kimi K2 全系走这条**）· ⭐ **`DEEPSEEK32`（V3.2 独立 arch）** · `LLAMA4` · `GEMMA3` · `GEMMA3N` · `MISTRAL3` · `GLM4_MOE`（另有 `GLM_DSA`）· `MINIMAX_M2` · `NEMOTRON_H` / `NEMOTRON_H_MOE` / `DECI`（Super）· `SEED_OSS` · `HUNYUAN_MOE` · `ERNIE4_5` / `ERNIE4_5_MOE` · `BAILINGMOE` / `BAILINGMOE2` · `GRANITE_HYBRID` · `PHI3` / `PHIMOE` · ⭐ **`DOTS1`** | ⛔ **Step-3**（只有 `STEP35` = Step-3.5）· ⛔ **Intern-S1**（只有 `INTERNLM2`）· ⛔ **MiniMax-M1 / Text-01** |

⭐ **另一条对 gpt-oss 有利的事实**：**ggml 有原生 `GGML_TYPE_MXFP4 = 39`** ⇒ **MXFP4 在 llama.cpp 侧是一等公民，⛔ 不是仿真。**

#### 4.4.3 ⛔ 需要特殊 flag / nightly / pin 版本的清单（⛔ 首版完全没写这一节）

⭐ **这一节直接反驳「2025 世代开箱即用」这个印象**——⛔ **最麻烦的几个恰恰是 2025 年的新架构。**

| 模型 | ⛔ 需要什么 |
| :-- | :-- |
| ⛔ **DeepSeek-V3.2（DSA）**——本批要求最多 | ① **nightly 轮子**（`--extra-index-url https://wheels.vllm.ai/nightly`）；② **手装 DeepGEMM** `@v2.1.1.post3 --no-build-isolation`（recipe 逐字「It is necessary for MQA logits computation」）；③ `--tokenizer-mode deepseek_v32` + `--tool-call-parser deepseek_v32`；④ ⛔ **Hopper 上有拓扑限制**：recipe 明确「**avoid using `-tp=8`** for DeepSeek-V3.2 with FlashMLA-Sparse」（TP=8 时每 rank 只有 16 头却被 pad 到 64），⭐ **推荐 Hopper TP=2**；⑤ ⚠️「Some users reported that the performance is better with `VLLM_USE_DEEP_GEMM=0`, e.g. **on H20 GPUs**」 |
| ⛔ **Qwen3-Next（GDN 混合注意力）** | `--compilation_config.cudagraph_mode=PIECEWISE`（规避 DP 模式下 `CUDA error: an illegal memory access`）；MoE 需自行 tune 并用 `VLLM_TUNED_CONFIG_FOLDER` 指入（否则日志报「Using default MoE config. **Performance might be sub-optimal!**」）；MTP 需 `--no-enable-chunked-prefill`。⛔ **三个 open issue**：[#25874 前缀缓存 × 混合注意力](https://github.com/vllm-project/vllm/issues/25874) · [#37035 MTP 负载下 `cudaErrorIllegalAddress`](https://github.com/vllm-project/vllm/issues/37035) · [#50046 GDN 在 torch.compile warmup 阶段 stride mismatch 崩溃](https://github.com/vllm-project/vllm/issues/50046) |
| ⛔ **MiniMax-M2** | ⛔ **需 nightly 或 pin 到特定 commit**——recipe 逐字「If you encounter **corrupted output** … upgrade to the nightly version (ensure it is a version after commit `cf3eacfe…`)」；另给 "verified version" `VLLM_COMMIT=0f3ce4c7…`；运行需 `--tool-call-parser minimax_m2 --reasoning-parser minimax_m2` |
| ⛔ **Nemotron（混合 Mamba）** | ⛔ **官方 recipe 走版本 pin 死的容器**（`vllm/vllm-openai:v0.12.0` 或 NGC `25.12.post1-py3`），⛔ **不是 pip 装**；需 `--trust-remote-code` + `--async-scheduling` + 显式 `--kv-cache-dtype`；FP8 路径要 `VLLM_USE_FLASHINFER_MOE_FP8=1` |
| ⛔ **gpt-oss** | CUDA 必须 **≥ 12.8**；⛔ PyTorch 缺 `+cu128` 后缀会报 `torch::nvtoolsext`；⛔ **`CUDA_HOME` 未设会产出乱码**（不是报错，⇒ 最危险的一种失败）；系统里有别的 Triton 会触发 `tl.language` 错误；**H100 上 TP1 用默认 `gpu-memory-utilization` 会 OOM**，TP2 需压到 0.95 以下 |
| **Seed-OSS** | 工具调用需 `--tool-call-parser seed_oss`；ROCm 需专门轮子 + `VLLM_ROCM_USE_AITER=1` |
| ⭐ **Kimi-K2-Thinking（INT4 QAT）** | ⭐ **官方 recipe 逐字「You can use 8x H200/H20 to launch this model」** ⇒ **INT4 QAT 走 compressed-tensors W4A16，⛔ 不需要 Blackwell**；需 `--reasoning-parser`。⚠️ SGLang 侧曾有 [#14677](https://github.com/sgl-project/sglang/issues/14677)（已关闭）——⛔ **那是 NVFP4 版的问题，⛔ 与 INT4 版不是一回事** |

⛔ **两条与非 Hopper 硬件相关、但方向上说明「新架构不稳」的 open issue**：[#40934 Qwen3-Next FP8 在 GB10 / sm_121 上仍失败](https://github.com/vllm-project/vllm/issues/40934) · [#41477 MXFP4 Triton kernel 用了 Hopper/SM10 专有 PTX，SM 12.1 直接失败且 Marlin 回退也踩坑](https://github.com/vllm-project/vllm/issues/41477)。

#### 4.4.4 ⛔ 两条官方部署文档的否定事实

1. ⛔ **`Gemma 3` · `Granite 4.0` · `Mistral Small 3.x` · `QwQ-32B` 在 vLLM 与 SGLang 两家都没有官方专属部署文档。** vLLM 只有 `Ministral-3` / `Mistral-Large-3` 页，SGLang 只有 `Mistral-Small-4` / `Devstral-2` 页；两家的 Gemma 专页都只覆盖 **Gemma 4**。⛔ **是「不需要」还是「未维护」，无法从文档判定。**
2. ⚠️ **SGLang 文档域名已从 `docs.sglang.ai` 301 到 `docs.sglang.io`，且旧路径 `supported_models/generative_models.html` 已 404**（现为 `docs/docs/supported-models/generative_models.mdx`，站点改走 Mintlify）。⇒ ⛔ **引用 SGLang 文档链接前必须重新核 URL。**

## 5. 官方量化件 vs 社区件清单

### 5.1 ⛔ 为什么这个区别是承重的

⭐ **作者件与三方件在三件事上不等价**：① **作者件的校准集与超参与训练侧一致**（QAT 件更是训练时就带上了量化），三方件是事后 PTQ；② **作者件的退化幅度厂商自己背书，三方件没有任何人背书**；③ **作者件的存在本身证明厂商在该格式上做过验证**，三方件的存在只证明有人跑过量化脚本。⇒ ⛔ **在论文里说「该模型有 4-bit 件」时，必须说清是谁发的。**

### 5.2 ⭐ 2025 世代的官方作者量化件全清单（⛔ 本轮逐个实测体积）

| 厂商 | 官方量化件 | 格式 | 实测体积 | ⭐ 备注 |
| :-- | :-- | :-- | --: | :-- |
| ⭐ **Qwen（覆盖最全，三条线）** | `Qwen3-235B-A22B-Instruct-2507-FP8` | FP8 block 128×128 | **236.4 GB** | ⭐ **Qwen 是唯一同时发 FP8 + AWQ + GGUF 三条线的厂商** |
| | `Qwen3-Coder-480B-A35B-Instruct-FP8` | FP8 | 482.1 GB | ⚠️ 4×H200 贴边 |
| | `Qwen3-235B-A22B-FP8` | FP8 | 239.0 GB | — |
| | `Qwen3-Next-80B-A3B-Instruct-FP8` | FP8 | 82.1 GB | ⭐ 单卡 112 GB 可容 |
| | `Qwen3-30B-A3B-Instruct-2507-FP8` / `Qwen3-Coder-30B-A3B-FP8` | FP8 | 31.2 GB | — |
| | `Qwen3-30B-A3B-FP8` / `Qwen3-32B-FP8` / `Qwen3-14B-FP8` / `Qwen3-8B-FP8` | FP8 | 32.4 / 34.3 / 16.3 / 9.4 GB | — |
| | ⭐ **`Qwen3-32B-AWQ`** / ⭐ **`QwQ-32B-AWQ`** | **AWQ-INT4**（4 bit） | **19.3 GB** | **本表唯一的官方 AWQ-INT4，且在 Hopper 上走 Marlin 原生** |
| | ⭐ **`Qwen3-32B-GGUF`** | 官方 GGUF | **Q4_K_M 19.8** / Q5_0 22.6 / Q5_K_M 23.2 / Q6_K 26.9 / Q8_0 34.8 GB | ⭐ 逐档实测 |
| | ⭐ **`Qwen3-30B-A3B-GGUF`** | 官方 GGUF | **Q4_K_M 18.6** / Q5_0 21.1 / Q5_K_M 21.7 / Q6_K 25.1 / Q8_0 32.5 GB | ⭐ 逐档实测 |
| | ⭐ **`Qwen3-14B-GGUF`** | 官方 GGUF | **Q4_K_M 9.0** / Q5_0 10.3 / Q5_K_M 10.5 / Q6_K 12.1 / Q8_0 15.7 GB | — |
| | ⭐ **`QwQ-32B-GGUF`** | 官方 GGUF | **q4_k_m 19.9** / q5_0 22.6 / q5_k_m 23.3 / q6_k 26.9 / q8_0 34.8 / **fp16 66.0**（17 分片） | — |
| | `Qwen3-4B-GGUF` / `Qwen3-8B-GGUF` | 官方 GGUF | 全档合计 15.8 GB / Q4_K_M 5.0 GB | — |
| ⭐ **Google（唯一发 QAT 件的）** | ⭐ **`gemma-3-27b-it-qat-q4_0-gguf`** | **Q4_0（QAT，非事后 PTQ）** | **17.2 GB**（+mmproj 0.9） | **QAT ≠ PTQ：量化在训练时就参与了** |
| | ⭐ **`gemma-3-12b-it-qat-q4_0-gguf`** / **`-4b-`** | Q4_0（QAT） | **8.1** / **4.0 GB** | — |
| | ⚠️ `gemma-3-27b/12b-it-qat-q4_0-unquantized` | ⚠️ **BF16** | 54.9 / 24.4 GB | ⛔ **名字里有 qat 但它是 BF16**——是「QAT 训完但未量化」的中间件，⛔ 不要误当量化件 |
| **Z.ai** | `GLM-4.7-FP8` / `GLM-4.6-FP8` | FP8（`compressed-tensors`） | **354.9 GB** | ⛔ **零 4-bit 件** |
| | `GLM-4.5-FP8` / `GLM-4.5-Air-FP8` | FP8 | 361.3 / **112.6 GB** | ⛔ 同上 |
| ⭐ **腾讯（三件套）** | ⭐ **`Hunyuan-A13B-Instruct-GPTQ-Int4`** | **GPTQ-INT4**（4 bit） | **42.7 GB** | **本表唯一的官方 GPTQ-INT4** |
| | `Hunyuan-A13B-Instruct-FP8` | FP8 | 80.9 GB | — |
| | ⭐ **`Hunyuan-A13B-Instruct-GGUF`** | 官方 GGUF | Q4_0 **45.4** / Q4_K_M **48.8** / Q8_0 85.4 GB | ⚠️ **注意官方 GGUF 的 Q4_K_M（48.8）比同厂 GPTQ-Int4（42.7）还大 6.1 GB** |
| **OpenAI** | `gpt-oss-120b` / `-20b` / `-safeguard-120b` / `-safeguard-20b` | ⛔ **原生 MXFP4**（不是「另发的量化件」，主仓库就是 MXFP4） | **65.2** / **13.8 GB** | ⛔ ⇒ **它们没有 BF16 配置，「BF16 显存」对它们不存在** |
| **Moonshot** | ⛔ **`Kimi-K2-Thinking` 主仓库即 INT4 QAT** | ⛔ **原生 INT4（QAT）** | **594.2 GB** | ⛔ **`moonshotai` 名下零个独立量化仓库** |
| **Meta** | `Llama-4-Maverick-17B-128E-Instruct-FP8` | FP8（fbgemm） | 416.8 GB | ⛔ **Scout 无 FP8 件** |
| **Mistral** | `Mistral-Large-3-675B-Instruct-2512-NVFP4` | ⛔ **NVFP4** | 403.1 GB | ⛔ 2025 世代唯一的 NVFP4 官方件；⛔ Hopper 非原生 |
| | `Ministral-3-8B-Instruct-2512`（主仓库） | ⛔ **原生 FP8** | 10.4 GB | ⚠️ 另有 `-BF16` 仓库 |
| | ⭐ **`Devstral-Small-2507_gguf`** | ⭐ **官方 GGUF** | **Q4_K_M 14.3** / Q5_K_M 16.8 / Q8_0 25.1 / BF16 47.2 GB | **本轮更正：Mistral 确实发官方 GGUF**，⛔ 首版把它列为「未核到」是错的 |
| | ⭐ **`Magistral-Small-2506_gguf`** / **`Devstral-Small-2505_gguf`** | 官方 GGUF | Magistral: 47.2（BF16）/ 25.1（Q8_0）；Devstral-2505 全档合计 116.7 GB | ⚠️ **Magistral-2506 只发了 BF16 与 Q8_0 两档，⛔ 无 Q4** |
| ⭐ **阶跃（StepFun）** | ⭐ **`step3-fp8`** | **FP8** | **327.6 GB** | **本轮更正：它装得进 4×H200**（见 §3.2 / §3.4） |
| **NVIDIA** | `Llama-3_3-Nemotron-Super-49B-v1-FP8` | FP8 | 52.0 GB | — |
| | `NVIDIA-Nemotron-Nano-9B-v2-FP8` | FP8 | 10.3 GB | — |
| **InternLM** | `Intern-S1-FP8` | FP8 | 249.1 GB | — |
| | ⭐ **`Intern-S1-GGUF`** | 官方 GGUF | 全档合计 **737.5 GB** | ⛔ **llama.cpp 无 `interns1` arch**（只有 `INTERNLM2`），⇒ ⏳ **视觉塔能否走 GGUF 待核验** |
| **IBM** | ⭐ `ibm-granite` 名下 **19 个 granite-4.0 GGUF 仓库** | 官方 GGUF | ⏳ 未逐档实测 | ⭐ **少数发官方 GGUF 的西方厂商**；granite-4.0 的 GGUF 生态出奇地厚（187 窄命中） |
| ⭐ **Qwen（补一条本轮新核到的）** | ⭐ **`Qwen3-Next-80B-A3B-Instruct-GGUF`**（2025-12-03 建仓） | 官方 GGUF | **Q4_K_M 48.4** / Q5_0 55.0 / Q5_K_M 56.7 / Q6_K 65.5 / Q8_0 84.8 / BF16 159.5 GB | **⇒ Qwen3-Next 的 Q4_K_M 48.4 GB 落进单卡 64 GB 档** |
| ⛔ **百度** | ⚠️ `ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle` **168.6 GB** · 另有 `-FP8-Paddle` | ⚠️ **W4A8C8** | **168.6 GB** | ⛔ **都是 Paddle 格式，⛔ 不是 HF / vLLM 直接可用的件**——⇒ 见 §3.4 |
| ⛔ **DeepSeek** | ⛔ **无。** 主仓库原生 FP8，⛔ **2025 年零个 4-bit 件** | — | — | 见 §5.4 |
| ⛔ **inclusionAI（Ling / Ring）** | ⚠️ **`inclusionAI` 名下有 24 个 int4 / fp8 / GGUF 仓库**，⛔ **但本轮未核到覆盖 `Ling-1T` / `Ring-1T` 的那一个** | — | ⏳ | ⛔ ⇒ **Ling-1T 的 1999.4 GB 目前无已核实的缩小路径**（⚠️ 有 `Ring-1T-FP8` 的 vLLM recipe 存在，体积未核） |
| ⛔ **ByteDance-Seed / MiniMax（M1）/ Cohere / tiiuae** | ⏳ **本轮未核到官方量化件**（⚠️ `ByteDance-Seed` 名下唯一命中与 Seed-OSS 无关；`rednote-hilab` 名下 **0**） | — | — | ⛔ 不等于「不存在」，见 §6 |
| **Microsoft** | ⭐ `microsoft` 名下 30 个量化仓库，含 `phi-4-gguf` | 官方 GGUF | 仓库总量 **211.4 GB**（⏳ 未拆逐档） | ⚠️ 该仓库建仓 **2025-01-08**，⭐ **正是 Phi-4 权重进 HF 的日子**（见时间门第 3 条） |

### 5.3 社区量化件丰富度（⛔ 含查法与其局限）

**查法**：`https://huggingface.co/api/models?search=<模型名>-GGUF&limit=100&skip=<n×100>`，翻页至返回 < 100 条或触到 1000 上限；⛔ **该 API 的 `search` 是模糊匹配，命中里包含微调衍生模型的 GGUF**，⇒ ⛔ **下表数字是上界，不是「该模型的量化件个数」**。⭐ 但它可以横比「哪些模型的社区关注度高」。

| 模型 | GGUF 命中 | 主要发布方（前 3） | AWQ 命中 | GPTQ 命中 |
| :-- | --: | :-- | --: | --: |
| **Qwen3-30B-A3B** | ⭐ **632** | mradermacher 212 · YOYO-AI 18 · elichen-skymizer 14 | 78（cyankiwi 16 · QuantTrio 5） | — |
| **QwQ-32B** | ⭐ **515** | mradermacher 223 · roleplaiapp 27 · BenevolenceMessiah 19 | 26 | — |
| **gpt-oss-20b** | **479** | mradermacher 211 · majentik 6 · DavidAU 5 | — | — |
| **gemma-3-27b** | **400** | mradermacher 167 · bartowski 10 · QrCode99 9 | 10 | — |
| **Qwen3-32B** | **336** | mradermacher 186 · unsloth 6 · bartowski 5 | 65 | 39 |
| **DeepSeek-R1-Distill-Qwen-32B** | **185** | roleplaiapp 41 · mradermacher 32 | — | — |
| ⭐ **DeepSeek-R1**（满血） | — | — | ⭐ **192**（radna 33 · **amd 11** · casperhansen 6） | **94**（nejumi 9 · OPEA 4） |
| **MiniMax-M2** | **172** | mradermacher 51 · bartowski 7 · unsloth 4 | 37（cyankiwi 8 · QuantTrio 5） | — |
| **gpt-oss-120b** | **130** | mradermacher 53 · bartowski 5 · **lmstudio-community 2** | — | — |
| **Qwen3-Next-80B** | **65** | mradermacher 20 · noctrex 4 · bartowski 2 | — | — |
| **Seed-OSS-36B** | **51** | mradermacher 24 · DevQuasar 3 | 3 | — |
| **Mistral-Small-3.2-24B** | **49** | mradermacher 18 · unsloth 1 · bartowski 1 | 4 | — |
| **GLM-4.5-Air** | **43** | mradermacher 12 · Beinsezii 4 · bartowski 3 | 6（cyankiwi 4） | — |
| **Llama-4-Scout** | **40** | mradermacher 14 · unsloth 1 · lmstudio-community 1 | — | — |
| **granite-4.0-h-small** | **25** | mradermacher 10 · ⭐ **ibm-granite 2（官方）** | — | — |
| ⛔ **Kimi-K2-Instruct** | ⛔ **21** | mradermacher 5 · KVCache-ai 2 · unsloth 2 | ⛔ **0** | — |
| ⛔ **Hunyuan-A13B** | ⛔ **14** | mradermacher 4 · bullerwins 1 · ubergarm 1 | — | — |
| ⛔ **Qwen3-Coder-480B** | — | — | ⛔ **5** | — |
| ⛔ **Llama-4-Maverick** | — | — | ⛔ **1**（kishizaki-sci） | — |
| ⛔ **GLM-4.6** | — | — | ⛔ **7**（cyankiwi 4 · QuantTrio 1） | — |

⭐ **三条结论**：

1. ⭐ **社区把 DeepSeek 的官方空缺补上了**：⛔ DeepSeek 官方零个 4-bit，但社区有 **192 个 AWQ + 94 个 GPTQ** 命中，**其中 `amd` 发了 11 个**（⇒ 芯片厂商自己在做，不只是个人爱好者）。⇒ ⛔ **「DeepSeek 在 4×H200 上跑不了」这个判断只在「必须用作者件」这个前提下成立。**
2. ⛔ **体量越大，社区件越少，⛔ 而这正是最需要量化的那一档。** `Kimi-K2-Instruct`（1029.2 GB）只有 21 个 GGUF 命中、**0 个 AWQ**；`Llama-4-Maverick` 只有 1 个 AWQ；`Qwen3-Coder-480B` 只有 5 个。⇒ **「社区会补上」这个假设在 400B+ 档不成立。**
3. ⭐ **`mradermacher` 一个人占了绝大多数 GGUF 命中**（每个模型 30%–45%）。⇒ ⚠️ **「社区量化件丰富」在很大程度上等于「有一个批量自动化的量化者」**，⛔ 这不是多方独立验证。真正需要看的是 **`unsloth` / `bartowski` / `lmstudio-community` 这三家有精选口径的**是否覆盖——上表里 `gpt-oss-120b`、`Llama-4-Scout`、`granite-4.0` 有 `lmstudio-community`，`Qwen3-32B` / `Mistral-Small-3.2` / `GLM-4.5-Air` / `Qwen3-Next-80B` 有 `unsloth` + `bartowski`。

### 5.4 ⛔ 三条否定事实（⛔ 本轮亲自核到，引用时不要软化）

1. ⛔ **DeepSeek 官方在 2025 年零个 4-bit 件。** 全系（R1 / R1-Zero / R1-0528 / V3-0324 / V3.1 / V3.1-Terminus / V3.2-Exp / V3.2 / V3.2-Speciale）主仓库均为原生 FP8，⛔ 无独立量化仓库。⚠️ 六个蒸馏模型是 BF16 dense，也不是量化件。
2. ⛔ **`zai-org` 现代世代零个 4-bit 件。** GLM-4.5 / 4.5-Air / 4.6 / 4.7 都只有 BF16 + 作者 FP8 两档。
3. ⛔ **`moonshotai` 名下零个独立量化仓库。** `Kimi-K2-Thinking` 的 INT4 直接在主仓库里；⇒ ⛔ **不存在「Kimi-K2-Instruct 的官方 4-bit 版」**，只存在「另一个已经是 INT4 的模型」。

## 6. 待核验与访问受限

### 6.1 本轮收录统计

| 项 | 数 |
| :-- | --: |
| **HF 仓库条目总数** | ⭐ **135** |
| 其中：基座 / 主仓库 | **106** |
| 其中：量化 / 精度变体（FP8 / AWQ / GPTQ-Int4 / NVFP4 / 官方 GGUF / QAT / BF16 副本） | **29** |
| 覆盖厂商（HF org） | **22** |
| 参数量跨度 | ⭐ **0.27B（`gemma-3-270m-it`）→ 999.7B（`Ling-1T` / `Ring-1T`）**，约 **3700 倍** |
| 体积跨度 | ⭐ **0.5 GB → 1999.4 GB**，约 **4000 倍** |
| 逐仓库实测体积（HF API 逐文件 `size` 合计） | ⭐ **135 / 135 全部实测**，⛔ 零个按参数量推算 |

**按厂商的条目数**（⭐ 反映各家发件密度，⛔ 不反映能力）：Qwen 29 · DeepSeek 16 · Mistral 14 · Google 12 · NVIDIA 9 · Z.ai 8 · Microsoft 6 · Moonshot 5 · MiniMax 4 · OpenAI 4 · 腾讯 4 · inclusionAI 3 · IBM 3 · Cohere 3 · InternLM 3 · 百度 3 · Meta 3 · ByteDance 2 · 百川 1 · 阶跃 1 · 小红书 1 · TII 1。

### 6.2 ⛔ 对结论有影响的缺口（按影响排序）

1. ⛔ **benchmark 是本轮证据级别最弱的一节，⛔ 但缺口的形状与首版所写不同——首版低估了覆盖面、同时漏掉了「估计值」这个真正的问题。** ⭐ 实际有 **38 个 AA v4.1.1 条目**（§1.4.2），**但其中 26 个是 AA 估计值、只有 12 个是实测**；另有 **10 个模型完全无 AA 条目**。**且本节几乎全部是 S★（并行核验路取自一手页面、我未回页复核），⇒ 引用前必须逐条回原文。** 只有 3 条是 **M**（Command A / Ling-1T / ERNIE-4.5，本人 `pdf_extractor` 提取一手 PDF）。⇒ **本文仍不做能力排序**，理由从「没有数字」改成「数字的证据级别与同质性不足以支撑排序」。部分模型在 [benchmark_open_weights.md](./benchmark_open_weights.md) 有 AA-LCR / SOB / LEDGER / LongBench Pro 分，**但那些是分项指标，不是 Index 总分，不可互换。**
2. ⛔ **两条待闭合的 benchmark 缺口**：① ⛔ **AA 官方 Version History 全文取不到**（methodology 页正文在 Harvey LAB-AA 段落处截断两次；`web.archive.org` 被 WebFetch 禁访；index 主页超 10 MB 上限）⇒ §1.4.1 的版本史表是 S★，未经官方全文核对；② **`Mistral-Large-3` 是唯一「AA 有实测分 16 但零个官方自报数字」的模型**（官方页 benchmark 表全是图片、HF 仓库 401 gated）。
3. ⛔ **官方发布日只核到 6 条**（Llama 4、Qwen3、Gemma 3、Seed-OSS 为 **M**；GLM-4.5、Mistral-Small-2501、QwQ-32B、gpt-oss、Kimi-K2-0905 为 **S**）。其余 **约 100 个条目的「官方日」列是 `⏳ 未核`**，只能用 HF 建仓日作下界。⛔ **§1.1 已实测该下界最大偏差 20 天**（Gemma 3 的 4B 档），⇒ **不得把 HF 建仓日当发布日引用。**
4. ⛔ **KV@30K 有约 40 个条目为 `⏳`**，§2 的档位归类对这些行按 KV = 0 处理，⇒ ⛔ **它们的真实档位可能高一档**。受影响最重的是 `dots.llm1`（**32 个 KV 头**、62 层，无 GQA 压缩）与 `MiniMax-M1`（80 层）。
5. ⛔ **gated 仓库的 context 取不到。** `google/gemma-3-*`（`gated: manual`）、`meta-llama/Llama-4-*`（`gated: manual`）、`CohereLabs/command-a-vision`（`gated: auto`）的 `config.json` 返回 HTTP 401，⇒ **`max_position_embeddings` 未核**。⚠️ Llama 4 blog 称 Scout 10M，⛔ 但同页逐字「pre-trained and post-trained with a **256K** context length」——⇒ **10M 是外推声明，不是训练窗口。**
6. ⭐ **MXFP4 在 Hopper 上的裁定本轮已闭合（⛔ 首版记为「两源冲突、不裁定」是错的）。** 从 vLLM `main` 源码拿到三条逐字（§3.3）：`SM90 falls through to Triton_unfused or Marlin` · `the fallback dequantizes only the weights` · `get_supported_act_dtypes()` 硬返回 `[torch.bfloat16]`。⇒ **省显存成立、⛔ 省算力不成立。** **仍未闭合的是另一件事**：**NVIDIA 官方文档里找不到「Hopper 无 FP4 张量核」的显式否定句**，只有正面陈述；⚠️ **且 TensorRT-LLM 文档有一句字面上把 Hopper 与 FP4 并列的话**。⇒ **该断言的依据是引擎行为侧，不是 NVIDIA 的否定句。** ⏳ 另：ModelOpt 的「NVFP4 inference requires Blackwell GPUs」在搜索摘要里出现，但两个 raw 路径均 404（仓库改名），**未取到逐字原文，不作已核验引用。**
7. ⚠️ **官方量化件本轮补核了六条，⛔ 但仍未核完。** ⭐ **本轮新核到并已并入 §5.2 的**：`stepfun-ai/step3-fp8` **327.6 GB**（改变了 §3.4 的裁定）· Mistral 三个官方 GGUF（`Devstral-2507_gguf` Q4_K_M **14.3 GB** 等）· `Qwen3-Next-80B-A3B-Instruct-GGUF`（Q4_K_M **48.4 GB**）· `Hunyuan-A13B-Instruct-GGUF`（Q4_K_M 48.8 GB）· `Intern-S1-GGUF`（全档 737.5 GB）· `ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle` **168.6 GB**（⛔ Paddle 格式）。**仍未核到的**：**`Nemotron-Ultra-253B` 的官方 FP8**（⚠️ NVIDIA 为 Super-49B 发了 FP8；**这一条最值得补——Ultra 的 BF16 是 506.8 GB，只超 4×H200 预算 19.8 GB，若存在官方 FP8 件它就落进 §3.2**）· **覆盖 `Ling-1T` / `Ring-1T` 的那个 int4 / fp8 件**（`inclusionAI` 名下有 24 个量化仓库、且存在 `Ring-1T-FP8` 的 vLLM recipe，但体积未核）· Seed-OSS / Baichuan-M2 / Falcon-H1 · `phi-4-gguf` 与 granite-4.0 GGUF 的逐档拆分。
8. ⚠️ **社区量化件计数有约 10 个模型为 `⏳`**（Nemotron 全系、ERNIE、Ling / Ring、Intern-S1、Falcon-H1、Kimi-Linear、Step-3、Phi-4 系）。⛔ 且已有的计数是**模糊匹配上界**，含微调衍生模型，⛔ 不是「该模型的量化件个数」。

### 6.3 ⛔ 访问受限与文档漂移记录

| 目标 | 症状 | 影响 |
| :-- | :-- | :-- |
| ⛔ [OpenAI gpt-oss 官方公告](https://openai.com/index/introducing-gpt-oss/) | **HTTP 403 Forbidden** | ⇒ gpt-oss 的官方发布日只能记 **S**（2025-08-05），⛔ 未拿到官方一手 |
| ⛔ [z.ai GLM-4.5 blog](https://z.ai/blog/glm-4.5) | **JS 空壳，抓取内容为空** | ⇒ GLM-4.5 的 2025-07-28 只能记 **S**（两家媒体一致） |
| ⛔ [Kimi K2 官方页](https://moonshotai.github.io/Kimi-K2/) | **只返回标题行，正文为空** | ⇒ Kimi K2 的确切发布日未核到，⛔ 只知在 2025-07 |
| ⛔ SGLang `docs/supported_models/generative_models.md` | **404**（文档路径已变） | ⭐ **改用 `python/sglang/srt/models/` 目录列举（216 模块），这比文档页更硬** |
| ⛔ GitHub code search API | **401 Requires authentication** | ⛔ 无法做跨仓库关键词搜索；已用目录列举替代 |
| ⛔ gated HF 仓库的 `config.json` | **401**（google / meta-llama / CohereLabs） | 见 §6.2 第 4 条 |
| ⛔ `MiniMaxAI/MiniMax-M2-GGUF` · `zai-org/GLM-4.5-Air-GGUF` | **401**（⇒ 仓库不存在） | ⭐ **这是一条有用的否定事实：MiniMax 与 Z.ai 都没有官方 GGUF** |
| ⛔ `mistralai/Mistral-Small-3.2-24B-Instruct-2506-FP8` | **401**（⇒ 不存在） | ⭐ 同上：Mistral Small 3.2 无官方 FP8 件 |
| ⛔ **AA 官方 Version History 全文** | methodology 页正文在 Harvey LAB-AA 段落处**截断两次**；`web.archive.org` **被 WebFetch 禁访**；index 主页**超 10 MB 上限** | ⇒ §1.4.1 的版本史表为 **S★**，⛔ 未经官方全文核对 |
| ⛔ **厂商 benchmark 表是图片** | QwQ-32B（card + blog 全图）· Qwen3-Coder（SWE 表全图）· GLM-4.6（card + blog 全图）· **Mistral-Large-3**（表全是图片，如 `4 Gpqa Diamond Accuracy`） | ⇒ ⛔ **本轮最主要的取数障碍**，见 §1.4.4 第 5 条 |
| ⛔ `qwen.ai/blog?id=qwen3-coder` | **SPA 空壳，只返回单词 "Qwen"** | ⇒ Qwen3-Coder 的 SWE 分拒绝登记（§1.4.5） |
| ⛔ arXiv HTML 版 | ⛔ **Ling 2.0 报告的 HTML 版在 §4.3 截断**（必须走 PDF）；⛔ **Command A 无 HTML 版、ar5iv 转换失败、`r.jina.ai` 403** | ⇒ 这两条改用 `tools/pdf_extractor.py` 提取原文（⭐ 因此级别为 **M**） |
| ⛔ AA `gpt-oss-*-medium` 单模型页 | **404**（AA 只发布 high / low 两档） | ⇒ 「三档分开」在 AA 侧只能给两档 |
| ⛔ GitHub `web.archive.org` / code search | 前者 WebFetch 禁访、后者 401 | ⇒ 历史版本与跨仓库检索两条路都不可用 |

### 6.4 ⛔ 本轮未覆盖的 2025 模型（⛔ 不是「不存在」，是没查）

`inclusionAI` 的中小档（`Ling-lite-1.5` / `Ring-lite` / `Ling-mini-2.0`）· `zai-org/GLM-4.5V`（多模态）· `Qwen3-Coder-Flash` · `nvidia/Nemotron-Nano-VL` 与 `Jet-Nemotron` · `CohereLabs/command-r7b` 系 · `OpenGVLab/InternVL3.5` 系 · `Motif-Technologies` 的 2025 档 · `tiiuae/Falcon-H1` 除 34B 的其余档 · `microsoft/MAI-*` · `LiquidAI/LFM2` 系 · `allenai/OLMo-2` / `OLMo-3` · `Zyphra/Zamba` · `apple/*` · `PleIAs` 等欧洲小厂 · `01-ai` 2025 档 · `THUDM/GLM-4-*` 2025 更新。

⛔ **一条明确的排除说明，⛔ 不是缺口**：**Mistral Medium 3（2025-05）没有开放权重**，它是 hosted-only；⇒ 按时间门第 4 条排除，**不要因为任务列表里写了「Mistral Medium」就去找它的权重**。⚠️ Mistral 的第一个开放权重 Medium 档是 **2026-03 的 `Mistral-Medium-3.5-128B`**，那超出本表时间门。同理 **Llama 4 Behemoth 从未发布权重**。

### 6.5 ⛔ 本文口径声明

1. ⛔ **本文不做能力排序。** §0 的四个「最强」全部是**在给定显存档下能装进去的最大 / 最合适的模型**，⛔ 不是「能力最强」——理由见 §6.2 第 1 条（**证据级别与同质性不足**，不是「没有数字」）。
2. ⛔ **本文的档位归类是容量判据的结果，⛔ 不是「跑得动」的结论。** 带宽、算子支持、KV 量化、并发数都可能让一个「装得下」的格子在实机上不可用（⭐ 有实测反例：vllm-ascend#1127）。
3. ⭐ **所有体积数字都是 HF API 逐文件实测，⛔ 零个按参数量推算。** 这是本文相对 §1.1 之外全部字段最硬的一点。
4. ⛔ **AA Index 数字一律带 v4.1.1 版本号。** ⛔ 同一个模型在 v4.0 与 v4.1.1 之间可差 8 分以上（实测：`Qwen3.6-27B` v4.0 = 46、v4.1.1 = 37.70），**跨版本数字不得比较**。
5. ⛔ **§1.4 的证据级别与 §1.2 / §1.3 不同，⛔ 不得混用。** §1.2 / §1.3 的体积、参数、精度、context、许可是 **M**（HF API 与 `config.json` 实测）；**§1.4 的 benchmark 数字绝大多数是 S★**。⇒ **在同一句话里同时引用两节的数字时，必须分别标级别。**

### 6.6 相对上一版的改动（⛔ 本轮就地更正了五处，⛔ 错误表述已删除不保留）

⛔ **按 [CLAUDE.md](../../../../CLAUDE.md) §3.6，更正一律就地改原件、不另发更正件。** 本节只记「改了什么、为什么改」，⛔ **不复述已删除的错误结论。**

| # | 位置 | 为什么改 |
| :-- | :-- | :-- |
| 1 | **§0 第 1 条 · §2.2 的 24 GB 与 32 GB 两行** | ⛔ **算术错误：首版把 `Qwen3-32B-AWQ`（19.3 GB）放进 24 GB 档，⛔ 漏算了它的 KV@30K = 7.3 GB。** 19.3 + 7.3 = **26.6 GB**，超 21.1 GB 预算 5.5 GB。⇒ 24 GB 档的答案换成 `gpt-oss-20b`（13.8 + 1.4 = 15.2，余 5.9），`Qwen3-32B-AWQ` 下移一档。⭐ **同时把该两行按「KV 已核 / KV 未核」分组**，因为混在一起看不出哪些归档是乐观值 |
| 2 | **§3.1 格式表 · §3.3** | ⭐ **MXFP4 在 Hopper 上的裁定从「⚠️ 两源冲突、不裁定」改为「能跑但省显存不省算力」**，依据是 vLLM `main` 源码三条逐字（后端选择器 docstring 的 `SM90 falls through to … Marlin`、量化层注释的 `the fallback dequantizes only the weights`、`get_supported_act_dtypes()` 硬返回 BF16）。⭐ 同时新增 **INT4 QAT 在 Hopper 原生**一行（官方 `Kimi-K2-Think` recipe 逐字 `8x H200/H20`） |
| 3 | **§3.2 · §3.4（a）** | ⭐ **`step3` 从「不可用」移入「可用」**：本轮核到作者件 `stepfun-ai/step3-fp8` = **327.6 GB**（Apache-2.0），装进 487 GB 预算余 159.4 GB。⛔ 首版写「BF16 641.9 GB · 更小件待核」是漏查。⚠️ 同时给 ERNIE-4.5-300B 补上 `W4A8C8-TP4-Paddle` = 168.6 GB，⛔ 但因 Paddle 格式**维持不可用判定** |
| 4 | **§0 第 1 条 · §6.2 第 1 条 · 新增 §1.4** | ⛔ **首版说「135 个条目只有 3 个有 AA v4.1.1 分」是低估。** 实际 **38 个条目有分**；⛔ **但真正的问题首版漏了——其中 26 个是 AA 估计值、只有 12 个是实测**，且页面顶部 summary 写裸数字、只有 FAQ 才写 `(estimated)`。⇒ 「不做能力排序」这个结论**不变**，⛔ 但理由从「没有数字」改成「证据级别与同质性不足」 |
| 5 | **§4.1 查法 · 新增 §4.4 · §5.2** | ⭐ **§4 的引擎结论方向不变，但三处被细化**：① vLLM `registry.py` 的 `_PREVIOUSLY_SUPPORTED_MODELS` 显示 `dots.llm1` 与 `MiniMax-M1` 是**「曾支持、已移除、末版 v0.23.0」**，⛔ 比首版写的「未列入」更准；② 补上 **llama.cpp 这条第三条腿**（⭐ `dots.llm1` 有 `DOTS1` arch ⇒ 它不是全无路）；③ ⛔ **首版说「Mistral 无官方 GGUF」是错的**——`Devstral-2507_gguf` / `Magistral-2506_gguf` / `Devstral-2505_gguf` 都存在，已逐档实测 |

### 6.7 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 | 建库并闭合六节。收 **135 个 HF 仓库条目**（106 基座 + 29 量化变体、22 厂商、参数量跨 3700 倍），⭐ **全部体积逐文件实测**。⭐ **§1.1 亲自核到 4 条官方发布日并与 HF `createdAt` 逐条比对，实测最大偏差 20 天**（Gemma 3 的 4B 档），⛔ 由此确立「HF 建仓日只是下界」这条口径。**§3.1 一条对 2025 世代有利的结构性发现：2025 世代没赶上 FP4 那一波**——NVFP4 官方件仅 1 个、MXFP8 **0** 个、MXFP4 4 个，⇒ 把 2026 世代容量排序前三名打掉的「Blackwell 格式判据」几乎不打击 2025 世代。⛔ **§3.4 一条冲击性否定事实：DeepSeek R1 / V3.1 / V3.2 全系在 4×H200 上装不下（688.6 GB vs 487 GB），且 DeepSeek 官方 2025 年零个 4-bit 件**；但 §5.3 发现社区补上了（192 AWQ + 94 GPTQ，含 `amd` 11 个）。**§4 用两个独立引擎注册表（vLLM 748 行文档 + SGLang 216 个模型模块）交叉核验，一致发现三个反例**：`dots.llm1`、`MiniMax-M1`/`Text-01`、`Phi-4-mini-flash-reasoning` 两边都不认；⛔ **其中 MiniMax-M1 是「曾被支持后被移出」，⇒ 「老模型生态更成熟」有一个方向相反的失效模式**。发现 Kimi K2 的 `architectures[0]` 就是 `DeepseekV3ForCausalLM`（⇒ 复用 DeepSeek 引擎路径，零新算子），但它 **0 个 AWQ**。**§5.2 逐个实测官方量化件**：Qwen 是唯一同发 FP8+AWQ+GGUF 三条线的厂商；Google 是唯一发 QAT 件的（`gemma-3-27b` Q4_0 = **17.2 GB**）；腾讯 `Hunyuan-A13B-GPTQ-Int4` = **42.7 GB** 是唯一官方 GPTQ-INT4。**三条否定事实**：DeepSeek / zai-org / moonshotai 各自零个 4-bit 独立仓库。**§6.2 登记最大缺口：135 个条目只有 3 个有 AA v4.1.1 实测分**，⇒ 本文不做能力排序。记录 8 条访问受限（OpenAI blog 403 · z.ai 与 Kimi 官方页 JS 空壳 · SGLang 文档 404 · GitHub code search 401 · gated 仓库 401 · 4 个 401 证明的「官方件不存在」）|
