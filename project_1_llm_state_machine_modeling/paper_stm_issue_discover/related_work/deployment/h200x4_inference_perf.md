# 4×H200 推理性能核验：哪个候选能把一代次跑完

> **本文只回答一个工程问题**：在 **4×H200（141 GB/卡，共 564 GB，4-way NVLink）** 上，哪些候选开放权重模型能以可接受的速度与并发跑完 paper1 的一代次实验。⛔ 本文不谈 motivation、不谈论文叙事、不做能力分数比较——能力定位归 [h200x4_envelope.md](./h200x4_envelope.md) §2，权重体积归其 §1，格式内核归其 §4.3。
>
> **核验日**：2026-08-13。**一手来源**：各仓库官方 `config.json` 原文（`curl .../raw/main/config.json`）、官方 model card、vLLM `recipes` 仓库 yaml、NVIDIA H200 官方规格页；第三方实测均标注来源与硬件。⛔ 本文不编造任何 tok/s、KV 配置或并发数；拿不到的一律标 ⏳。
>
> ⚠️ **与 [h200x4_envelope.md](./h200x4_envelope.md) 的分工**：那份文档回答「装不装得下」，本文回答「装下之后跑不跑得完」。⛔ 两份文档的 KV 数字口径不同（辨析见 §1.3），不要交叉引用同一列。

## 0. 一句话结论（哪个候选实验可行、哪个不可行）

⭐⭐ **用户给的假设方向反了。** `DeepSeek V4-Flash-0731` 不是「能部署但推理性能不高、无法承受并发」的那一个，⭐ **它是四个候选里最快、并发余量最大的那一个**；⛔ 真正「能部署但不适合做实验」的是 **`GLM-4.7-FP8`** 与 **`GLM-5.2`**。

机制一句话：**决定 4×H200 上快慢的不是模型总参数量，而是「每 token 激活参数量」与「每 token KV 字节数」这两个量，而这两个量恰好在 V4-Flash 上双双最小、在 GLM 两代上双双最大。**

| 候选 | 激活参数/token | KV 字节/token | 30K 下最大并发 | 一代次墙钟估算 | 判定 |
| :-- | --: | --: | --: | :-- | :-- |
| ⭐ **DeepSeek V4-Flash-0731** | **13B**（官方） | ⭐ **48.4 KiB** | ⭐ **228**（FP8 KV 457） | ⭐ **3.3 – 7.1 h** | ⭐ 可行，余量最大 |
| **MiniMax M2.7** | **10B**（官方） | 248.0 KiB | 36（FP8 KV 72） | **11.2 – 12.9 h** | ✅ 可行 |
| ⛔ **GLM-4.7-FP8** | ⚠️ **~32B**（本文推算） | ⛔ **368.0 KiB** | ⛔ **6.8**（FP8 KV 13.6） | ⛔ **8.5 – 24.0 h**（区间宽到无法排期） | ⛔ 勉强可行，不建议 |
| ⛔⛔ **GLM-5.2-NVFP4** | ⚠️ ~39B（本文推算） | 87.8 KiB | 15.6（FP8 KV 31.2） | ⛔ 拒绝估算 | ⛔⛔ **不可行** |

⛔ **`GLM-5.2-NVFP4` 判为不可行的理由与性能无关，是格式**：其 card 逐字只写 `Test Hardware: NVIDIA B200`，而 NVFP4 在 Hopper 上没有原生张量核（[h200x4_envelope.md](./h200x4_envelope.md) §4.3 有六条逐字）。⛔ 在 Hopper 上它走 Marlin 回退——**省显存不省速度**，而它同时是四个候选里激活参数最多的（~39B）。⛔ 两头都占最差，且没有任何 H200 实测。**不要为它做墙钟估算，任何数字都是编的。**

### 0.1 ⭐⭐ 先纠一条负载前提：任务书低估输入约 22%，且**输出才是瓶颈**

⭐ 本文没有沿用「3621 次 × 30K 输入」这个估算，而是**直接从 v46-full 的 3637 份 run record 里把 usage 字段全量聚合出来**（逐份读 `runs/paper1/matrix-v46-full/*/*/records/*llm-call-completed/record.json` 的 `input_tokens` / `output_tokens` / `system_prompt_sha256` / `system_prompt_chars`）。实测结果：

| 量 | 任务书估算 | ⭐ v46-full 实测 | 差 |
| :-- | :-- | :-- | :-- |
| LLM 调用次数 | 3621 | **3637** | +0.4% |
| 单次输入 | 25–30K tok | ⭐ **均值 36.4K tok**（中位 33.9K，p90 62.9K，max 201.7K） | ⛔ **+21% ~ +46%** |
| 总输入 | ~108.6M tok | ⭐ **132.4M tok**（GLM-4.7 tokenizer 口径） | +22% |
| 总输出 | 未给 | ⭐ **~18.5M tok**（Anthropic 计 17.4M；GLM tokenizer 估 19.8M） | — |

⛔⛔ **而任务书那句「我们的负载是 30K 输入，prefill 是主要成本」是错的。** 输入 132M / 输出 18.5M 看起来是 7.2:1，⛔ 但按聚合吞吐算，**prefill 的单 token 成本比 decode 低 8–55 倍**，所以按时间算反过来：**decode 占总墙钟 51%–89%，六个估算档位里有五个超过 68%**（逐档见 §4.2）。⭐ **这条颠倒直接改变结论**：它意味着 KV 容量（决定并发上限，从而决定 decode 聚合吞吐）比 prefill 算力更承重——**而 KV 恰好是 GLM-4.7 的死穴、V4-Flash 的强项**。

### 0.2 ⭐ prefix caching：收益是「省 36.9% 的 prefill」，⛔ 不是「省 36.9% 的墙钟」（端到端 4%–17%）

⭐ **一条比预期更强的实测事实**：v46-full 全部 3637 次调用里，**每个角色的 `system_prompt_sha256` 只有唯一一个取值**——即 system prompt 在同角色内**逐字节相同**，全实验只有 **5 个不同前缀**。这是 prefix caching 的理想形态（§2.4 给逐角色 token 数）。

⛔ **但收益上限被两件事夹住**：① 常量前缀只占总输入的 **36.9%**（48.9M / 132.4M），因为 user prompt 侧（制品、需求、反馈）本身平均就有 23K tok；② prefill 本来只占墙钟的 11%–49%。⭐ **两者相乘：prefix caching 对端到端墙钟的收益是 4.2%–17.4%，即省 0.5–0.7 小时**，⛔ 不是文献里常引的「TTFT 降 7 倍」——那个 7 倍是**单请求冷热对比**，与批量离线作业无关（§2.4 逐条辨析）。

**结论**：prefix caching 该开（vLLM 默认就是开的，§2.4），⛔ 但**它不是成败关键**。真正决定成败的是 §1 那张 KV 表。

## 1. 逐模型 KV footprint 与并发上限

### 1.1 算法与逐字段出处（⛔ 每个数字都能回到 `config.json`）

**常规 GQA / MQA**：每 token 每序列的 KV 字节数 $B = 2 \cdot L \cdot H_{kv} \cdot d_h \cdot s$，其中 $s$ 为每元素字节数（BF16/FP16 取 2，FP8 取 1），前导 2 是 K 与 V 两份。

**MLA（DeepSeek 系与 GLM-5.x）**：只缓存压缩潜变量与 rope 分量，$B = L \cdot (r_{kv} + d_{rope}) \cdot s$，⛔ **没有前导 2**（K 与 V 共用同一潜变量），⛔ 也**不乘头数**。⭐ 这就是 MLA 与 GQA 差一个数量级的原因，必须分开算。

30K 上下文取 $T = 30{,}000$。⚠️ 所有数字均为 **batch = 1 单序列**；⛔ KV 随并发线性放大，这正是末列的算法。

| 模型 | 注意力族 | $L$ | 关键字段（`config.json` 逐字） |
| :-- | :-- | --: | :-- |
| `DeepSeek-V4-Flash-0731` | MLA-like + 压缩 + SWA | **43** | `num_key_value_heads: 1`、`head_dim: 512`、`qk_rope_head_dim: 64`、`q_lora_rank: 1024`、`o_lora_rank: 1024`、⚠️ `sliding_window: 128`、⚠️ `compress_ratios`（46 项，取值 `{4: 21次, 128: 20次, 0: 5次}`）、`index_head_dim: 128` / `index_n_heads: 64` / `index_topk: 512` |
| `MiniMax-M2.7` | ⭐ **纯 GQA，无混合层** | **62** | `num_key_value_heads: 8`、`head_dim: 128`、⭐ `attn_type_list` 共 62 项**全为 `1`** |
| `GLM-4.7-FP8` | ⛔ **纯 GQA，92 层** | **92** | `num_key_value_heads: 8`、`head_dim: 128`、`num_attention_heads: 96`、`num_nextn_predict_layers: 1` |
| `GLM-5.2`（NVFP4 与 FP8 件同构） | MLA + DSA | **78** | `kv_lora_rank: 512`、`qk_rope_head_dim: 64`、`qk_nope_head_dim: 192`、`v_head_dim: 256`、`layer_types` 共 78 项**全为 `deepseek_sparse_attention`**、`indexer_types` = `full` 21 / `shared` 57、`index_topk: 2048` |

⭐ **两条只有读 `config.json` 才能发现的事**：

1. ⭐ **`MiniMax-M2.7` 的 `attn_type_list` 62 项全是 `1`**——即**没有** MiniMax 早期 Text-01 那种线性/lightning 注意力层，**全部是 softmax 全注意力**。⛔ 所以**不能给它打「混合注意力折扣」**，它的 248 KiB/token 是实打实的。⚠️ 注意这与 [h200x4_envelope.md](./h200x4_envelope.md) §1.4 讲的 `MiniMax M3`（有 MSA 稀疏注意力）**不是同一件事**，⛔ 不要把 M3 的折扣挪给 M2.7。
2. ⭐ **`nvidia/GLM-5.2-NVFP4` 的量化块里直接写了 KV 方案**：`quantization_config.kv_cache_scheme = {"dynamic": false, "num_bits": 8, "type": "float"}`——即**该件自带 FP8 KV cache**，⛔ 而作者件 `zai-org/GLM-5.2-FP8` 的量化块里**没有** `kv_cache_scheme`。两件的 KV 占用差一倍。

### 1.2 逐模型 KV 表与 30K 下的最大并发

⚠️ **末两列的算法**：最大并发 $= \mathrm{KV\ budget} / (B \cdot T)$，向下取整前保留一位小数。⛔ 这是**纯容量上限**，⛔ 不是「实测能稳定跑到的并发」——后者还受调度、算力与延迟阈值限制，见 §2。

| 模型 | 公式 | $B$（字节/token） | KiB/token | KV@30K | 本文 KV 预算 | ⭐ 最大并发 | FP8 KV 下 |
| :-- | :-- | --: | --: | --: | --: | --: | --: |
| ⭐ `DeepSeek-V4-Flash-0731` | $43 \cdot 576 \cdot 2$ | **49,536** | ⭐ **48.4** | **1.486 GB**（1.384 GiB） | 340 GB | ⭐ **228.8** | ⭐ **457.6** |
| `MiniMax-M2.7` | $2 \cdot 62 \cdot 8 \cdot 128 \cdot 2$ | 253,952 | 248.0 | **7.619 GB**（7.095 GiB） | 277 GB | **36.4** | 72.7 |
| ⛔ `GLM-4.7-FP8` | $2 \cdot 92 \cdot 8 \cdot 128 \cdot 2$ | ⛔ **376,832** | ⛔ **368.0** | ⛔ **11.305 GB**（10.529 GiB） | ⛔ 77 GB | ⛔⛔ **6.8** | ⛔ 13.6 |
| `GLM-5.2` | $78 \cdot 576 \cdot 2$ | 89,856 | 87.8 | **2.696 GB**（2.511 GiB） | 42 GB | 15.6 | 31.2 |

⛔⛔ **本表最重要的一格是 `GLM-4.7-FP8` 的 6.8。** 它意味着在给定的 77 GB KV 预算下，4×H200 上**同时只能容纳 6 条 30K 序列**。⭐ 这与官方口径完全同向：`zai-org/GLM-4.5` 的 model card 在给出 `H200 x 4` 那一档时，前置条件第 3 条逐字就是「Inference **batch size does not exceed 8**」（[h200x4_envelope.md](./h200x4_envelope.md) §4.1 已逐字核验）。⛔ **即「4 卡能跑 GLM」和「4 卡能以实验所需的并发跑 GLM」是两件事，而官方自己把 batch 上限写在了 8。**

⭐ **反过来，`DeepSeek-V4-Flash` 的 228 意味着 KV 对它根本不是约束**——它的瓶颈只会是算力，而算力上它的激活参数也是最小档之一（13B）。⭐ **两个维度同时最宽，这就是 §0 结论的全部来源。**

**可折扣项（⛔ 本文一律不折扣，故上表是上界）**：

1. ⭐ `DeepSeek-V4-Flash` 的 `compress_ratios` 显示 46 个位置中有 **20 个用 128× 压缩、21 个用 4× 压缩**，另有 `sliding_window: 128`。⚠️ 若这些确为逐层 KV 压缩比，其真实 KV 会**远低于** 48.4 KiB/token。⭐ 官方 card 侧的同向说法：V4 系「**10% of V3.2's KV cache at 1M context**」（[LMSYS Day-0 博客](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)转述架构，核验日 2026-08-13）。⛔ 本文按未压缩的 MLA 上界记账，⛔ 故 228 这个并发数**偏保守**。
2. `GLM-5.2` 的 DSA indexer 需额外缓存索引键（`index_head_dim: 128`，21 个 `full` 层）：按 FP8 估约 **2,688 字节/token**，相对 89,856 只占 3.0%，⛔ 本文并入误差不单列。
3. 两个模型都有 MTP 层（`num_nextn_predict_layers: 1`；M2.7 是 `num_mtp_modules: 3`）。⛔ 开投机解码时 MTP 层也要 KV，⛔ 上表未计。

### 1.3 ⚠️ 与 `h200x4_envelope.md` §1 的口径差异（⛔ 必须知道，否则会读出矛盾）

⛔ 两份文档的 KV 列**不一致，且都不是错的**——它们是两个口径：

| 模型 | 本文 KV@30K | envelope §1 KV@30K | 差异原因 |
| :-- | --: | --: | :-- |
| `DeepSeek-V4-Flash` | **1.486 GB** | 2.5 ⚠️ | ⏳ **未裁定**。本文按 $L=43$ 的 MLA 上界算；envelope 侧标了 ⚠️。⛔ 两者对结论无影响（1.5 与 2.5 GB 对 340 GB 预算都是零头，并发从 228 降到 136 仍远超需求） |
| `MiniMax-M2.7` | 7.619 GB | 7.1 | ✅ 同一算法，⛔ 只是 GB 与 GiB 之差（7.619 GB = 7.095 GiB） |
| `GLM-4.7-FP8` | 11.305 GB | 10.5 | ✅ 同上（11.305 GB = 10.529 GiB） |
| `GLM-5.2` | 2.696 GB | 2.7 | ✅ 同上 |

⛔⛔ **另有一处必须点出的口径问题，它会把 GLM-4.7 的并发上限算错一倍**：任务书给的 `GLM-4.7-FP8` 权重 430 GB 取自 vLLM recipe 的 `vram_minimum_gb: 430`，⛔ **而那是「最小显存需求」，不是纯权重字节数**。envelope §1.2 实测的 shard 字节数是 **354.9 GB（+MTP 7.2）= 362.1 GB**。按 envelope §1.1 的主判据反算：$0.92 \times 564 - 362.1 - 12 = 144.8$ GB KV 预算，⛔ **是 77 GB 的 1.9 倍**，对应并发 **12.8**（FP8 KV 下 25.6）。

⭐ **本文两个都报，并在 §4 的墙钟里把它做成上下界**：悲观档用 77 GB（recipe 口径，含未知常驻开销），乐观档用 144.8 GB（实测权重口径）。⛔ **不要只报一个**——它们相差一倍，而这一倍直接决定 GLM-4.7 是 9 小时还是 24 小时。

## 2. 实测吞吐（prefill / decode / TTFT / prefix caching）

### 2.1 先立标尺：H200 官方规格与 roofline 上限（⛔ 用来判断实测数字是否可信，不用来代替实测）

⭐ **官方规格**（[NVIDIA H200 产品页](https://www.nvidia.com/en-us/data-center/h200/)，核验日 2026-08-13）：

| 规格 | H200 SXM | H200 NVL |
| :-- | :-- | :-- |
| FP8 Tensor Core | `3,958 TFLOPS` | `3,341 TFLOPS` |
| BF16 Tensor Core | `1,979 TFLOPS` | `1,671 TFLOPS` |
| 显存 / 带宽 | `141GB` / `4.8TB/s` | `141GB` / `4.8TB/s` |
| 最大 TDP | `Up to 700W` | `Up to 600W` |

⛔⛔ **两条必须随规格带走的官方注脚**：① Tensor Core 那几行都挂着脚注 2 = **`With sparsity`**，⛔ 即 `3,958 TFLOPS` 是**稀疏**口径，**稠密约为其一半 ≈ 1,979 TFLOPS/卡**；② 表头挂脚注 1 = 「**Preliminary specifications. May be subject to change.**」。⛔ 本文一律用稠密口径。

**由此得 4×H200 SXM 的 roofline**：稠密 FP8 算力 $= 4 \times 1{,}979 = 7{,}916$ TFLOPS；聚合显存带宽 $= 4 \times 4.8 = 19.2$ TB/s。**prefill 上限** $= 7{,}916 \times 10^{12} / (2 \cdot P_{act})$ tok/s；**BS=1 的 decode 上限** $= 19.2 \times 10^{12} / P_{act}$ step/s（FP8 权重按 1 字节/参数）。

⭐ **激活参数量 $P_{act}$（本文按官方 `config.json` 字段逐层推算，仅线性层）**：

| 模型 | 每层注意力 | 每 MoE 层 | ⭐ 激活合计 | 官方/框架侧对照 |
| :-- | --: | --: | --: | :-- |
| `MiniMax M2.7` | 44.0M | 113.2M | ⭐ **9.8B** | ⭐ vLLM recipe 逐字「230B total / 10B active」 → **吻合** |
| `DeepSeek V4-Flash` | 195.3M | 176.2M | **16.0B** | ⚠️ recipe 逐字 `parameter_count: "284B"` / `active_parameters: "13B"` → 本文推算偏高 3B（MLA 的 lora 结构本文估得粗），⭐ **以官方 13B 为准** |
| `GLM-4.7` | 136.3M | 212.3M | ⚠️ **~32.0B** | ⏳ **无官方激活参数披露**，本文推算 |
| `GLM-5.2` | 165.0M | 339.7M | ⚠️ **~39.0B** | ⏳ 同上 |

⛔⛔ **这张表是全文的因果核心**：`GLM-4.7` 的激活参数是 `MiniMax M2.7` 的 **3.3 倍**，`GLM-5.2` 是 **4.0 倍**。⭐ **而激活参数同时决定 prefill 的 FLOPs 与 decode 的显存读取量**——即它在两个阶段**同向**放大成本，⛔ 没有一个阶段能补偿另一个。

| 模型 | prefill 理论上限（100% MFU） | BS=1 decode 理论上限（100% 带宽利用） |
| :-- | --: | --: |
| `MiniMax M2.7` | 405.9K tok/s | 1,969 step/s |
| `DeepSeek V4-Flash` | 247.8K tok/s | 1,202 step/s |
| `GLM-4.7` | 123.7K tok/s | 600 step/s |
| `GLM-5.2` | 101.4K tok/s | 492 step/s |

⛔ **这四个数字是上限，不是预测**。真实 serving 栈的 MFU 通常在 5%–15%（下面的实测正好落在这个带里，这就是本文用它们做交叉校验的方式）。

### 2.2 ⭐ 拿到的 H200 级实测（三条，逐条注明硬件与局限）

#### A. ⭐⭐ `MiniMax-M2.5` FP8 on **4×H200 SXM** —— 唯一一条**卡数完全对得上**的第三方实测

来源：[Millstone AI · MiniMax-M2.5 FP8 4x H200 SXM](https://www.millstoneai.com/inference-benchmark/minimax-m2-5-fp8-4x-h200-sxm)，报告日 **2026-02-14**，核验日 2026-08-13。**引擎 vLLM**，成功率 `100.0% across 3.3K requests`。测试口径逐字：「Context lengths from 1K - 192K tokens. Concurrency from 1 - 8 requests. 1024 output tokens per request.」+「**No prompt caching. No speculative decoding. Full-precision KV cache.**」

⭐ **32K 上下文那一档几乎就是我们的负载**（我们均值 36.4K）：

| 指标 | 1 请求 | 8 请求 | 18 请求 |
| :-- | --: | --: | --: |
| TTFT | **1.3 s** | 5.2 s | 7.8 s |
| 单用户生成速度 | **81 tok/s** | 47 tok/s | 25 tok/s |
| ⭐ 聚合输出（推算 = 单用户 × 并发） | 81 | 376 | ⭐ **450 tok/s** |

其官方给出的 32K 档**容量结论逐字**：`Capacity: 18 requests`（判据 `TTFT <8s, >15 tok/s`）。另有全局聚合输出吞吐三点：`1K/8req = 498.5 tok/s`、⭐ `32K/8req = 247.1 tok/s`、`128K/8req = 60.8 tok/s`；`Scaling: 6.4× from 1 to 8 concurrent requests`。

**prefill**：该页给的是 `Prefill Speed (per user, peak values)`：并发 1 时 `30,433 tok/s`（峰值出现在 8K），并发 8 时 `29,138 tok/s`。⛔⛔ **「per user」这个标签与 roofline 矛盾**：若真是每用户 29,138、并发 8 则聚合 233K tok/s = **57% MFU**，⛔ 对一个真实 serving 栈不可信。⭐ **本文因此不用这一列，改用 TTFT 反解**：$32{,}768 / 1.3\,\mathrm{s} = 25{,}206$ tok/s，对应 **6.2% MFU**——落在合理带内。⛔ **凡引用 30,433 这个数的，都要先解决这个标签歧义。**

⚠️ **四条局限**：① 测的是 **M2.5 不是 M2.7**（两者均 230B、FP8 件体积同为 230.1 GB 量级，本文当同类外推，⛔ 但这是外推）；② ⏳ **未给 vLLM 版本号**；③ ⏳ **未给 `--tensor-parallel-size`**，只写「4x H200 SXM」；④ ⭐ **明确关掉了 prompt caching 与投机解码、且用满精度 KV**——⛔ 这意味着它是**下界**，我们开这三项后会更快。

#### B. ⭐ `GLM-4.6-FP8` **TP4** on H200 —— GLM 族唯一的 4 卡实测（⛔ 是 4.6 不是 4.7）

来源：[GPUStack Performance Lab · Optimizing GLM-4.x Throughput on NVIDIA H200](https://docs.gpustack.ai/2.0/performance-lab/glm-4.x/h200/)，核验日 2026-08-13。硬件 `8 × NVIDIA H200 SXM` 单节点，⭐ **但 TP4 配置只用其中 4 张**（该页头部表格自己写「optimized figures doubled since TP4 uses half the GPUs」）。引擎版本明确：`vLLM v0.11.0`、`SGLang v0.5.3`、`TensorRT-LLM v1.0.0`（⛔ TRT-LLM 对 GLM-4.6 `not supported`）。

⭐ **两个对我们最有用的格子**：

| 场景 | 配置 | 实测 | ⭐ 反解出的量 |
| :-- | :-- | :-- | :-- |
| ⭐ **32K 输入** | SGLang FP8 **tp 4**，100 prompts × `32000 in / 100 out`，并发 100 | 时长 **262.58 s**，总吞吐 `12,223.53 tok/s`，输出 `36.95 tok/s`，**mean TTFT 129,699 ms** | ⭐ **聚合 prefill = $100 \times 32000 / 262.58 = 12{,}186$ tok/s**（**9.9% MFU**） |
| ShareGPT 短上下文 | SGLang FP8 `tp 4`，1000 prompts，并发 1000 | 输出 `3,416.25 tok/s`，总 `7,081.34 tok/s`，mean TPOT `256.43 ms` | 短上下文下 KV 不是约束，聚合 decode 可达 3.4K tok/s |

⭐ **交叉校验成立**：`GLM-4.6` 与 `MiniMax M2.7` 的实测 prefill 比为 $12{,}186 / 25{,}206 = 0.48$，⭐ 而两者激活参数比为 $9.8 / 32.0 = 0.31$——⛔ 不完全相等（GLM 侧并发 100 摊薄了固定开销、MFU 更高），⭐ **但方向与量级一致，说明两条独立来源互相支持。**

⛔ **必须一起读的那个数**：**mean TTFT 129.7 秒**。即在 32K 输入、并发 100 下，GLM-4.6 的首 token 要等两分钟。⛔ 对交互式服务这是不可用，⚠️ 对我们的**离线批量**作业则无关——我们不在乎 TTFT，只在乎聚合吞吐。⭐ **这条区分很重要：不要把交互式基准的「不可用」结论直接搬到批量作业上。**

⚠️ **局限**：① **测的是 GLM-4.6，不是 4.7**（两者同为 `Glm4MoeForCausalLM`、总参 357B vs 358B、本文推算激活参数同为 ~32B，本文当同类外推）；② 该页自己声明结果是「a local rather than global optimum」；③ ⛔ **未开 MTP 投机解码**，而 GLM-4.7 官方 4×H200 recipe 是默认开的（见 §2.3）。

#### C. ⭐⭐ `DeepSeek-V4-Flash` on **H200 TP=4** —— 直接命中 30K 提示长度的官方栈实测

来源：[LMSYS Org · DeepSeek-V4 on Day 0（SGLang + Miles）](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)，核验日 2026-08-13。**设置逐字**：「B200 Pro (1.6T) at TP=8; **H200 Flash (285B) at TP=4**.」+「**Single-batch decode, OSL=4096, on a 30K-token prefix** truncated from *Dream of the Red Chamber*.」+「Decode throughput is `1000 / TPOT (ms)`」

⭐⭐ **实测值**：H200 上 decode 从 **266 tok/s**（4K 上下文）降到 **240 tok/s**（900K 上下文），降幅「under 10%」。⭐ **这是 BS=1 的单序列速度，且提示长度就是 30K**——与我们的负载对得上得离奇。

⚠️ **三条必须带走的限定**：

1. ⛔ **含投机解码**。SGLang 侧配置逐字 `EAGLE 3/1/4 (num-steps=3, eagle-topk=1, num-draft-tokens=4)`，accept length ≈ 2.5。⛔ **但在 H200 Flash 上它退化为 MTP-1（accept ≈ 1.92）**，原因逐字：`num_speculative_tokens >= 2` 时触发 `paged_mqa_logits_metadata` 断言。⭐ **故 266 tok/s 里约有 1.92× 来自投机解码，裸 decode ≈ 138 step/s**（= roofline 1,202 的 **11.5%**，落在合理带内 ✅）。
2. ⛔ **它是 SGLang 自己的数字，不是中立第三方**；⛔ 且 ⏳ **未给 SGLang 版本号**。
3. ⛔⛔ **完全没有 prefill / TTFT 数字**。该页对长上下文 TTFT 只有定性描述（context parallelism「makes long-context TTFT scale here」）。⭐ **这是本文最大的证据缺口**，直接影响 §4 对 V4-Flash 的估算（见 §5.1 第 1 条）。

**另有两条同页面的相关事实**：Flash Compressor 内核在 H200 上「reaches up to **80% of peak memory bandwidth**」且比朴素 PyTorch 实现快「more than 10x」；HiSparse 把非活跃 C4 KV 卸载到主机内存可把长上下文服务吞吐提到「**up to 3x**」（⚠️ 该 3x 是在 **2×B200** 上测的 `200K-input / 20K-output`，⛔ 不是 H200 的 30K 档）。

### 2.3 投机解码：⭐ 这是唯一一个能把 decode 成本按倍数砍下来的杠杆

⛔ 因为 §0.1 已证明 decode 占墙钟 51%–89%（六档里五档 >68%），⭐ **投机解码的收益直接乘在瓶颈上**，比 prefix caching 重要得多。逐候选的官方支持情况：

| 模型 | 官方投机解码方案 | 官方逐字 | 在 Hopper 上的状态 |
| :-- | :-- | :-- | :-- |
| ⭐ `GLM-4.7-FP8` | 内建 MTP | recipe 4×H200 启动命令含 `--speculative-config.method mtp --speculative-config.num_speculative_tokens 1`；调优提示逐字「**MTP acceptance:** 1 speculative token gives **~90%+ acceptance** and best throughput」 | ✅ **官方 4×H200 命令默认开启** |
| ⭐ `DeepSeek V4-Flash-0731` | MTP / **DSpark** | card 逐字 `--speculative-config '{"method":"dspark","num_speculative_tokens":7,...}'`；recipe `default_mode: mtp`，且注「2 draft tokens (**1 on Hopper**)」 | ⚠️ **Hopper 上 MTP 被限到 1 个 draft token**；⏳ DSpark（7 tokens）在 H200 上的实测未见 |
| `MiniMax M2.7` | ⏳ 未见官方投机配置 | — | ⏳ 未核 |
| `GLM-5.2` | `num_nextn_predict_layers: 1`（有 MTP 层） | — | ⛔ 无 H200 实测 |

⭐ **`GLM-4.7` 的「~90%+ acceptance @ 1 draft token」是官方一手数字**（[vLLM recipes `models/zai-org/GLM-4.7.yaml`](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-4.7.yaml)）。按 accept rate $a$ 与 1 个 draft token，decode 加速比 $= 1 + a \approx 1.9$。⭐ **这是 GLM-4.7 唯一的翻身机会**，也是 §4 里它乐观档与悲观档差 2.8 倍的主要来源。

⛔⛔ **一条对 `DeepSeek V4-Flash` 的具体风险**：LMSYS 逐字记录了它在 **H200 上无法用 ≥2 个 draft token**（`paged_mqa_logits_metadata` 断言），⛔ 而 card 推荐的 DSpark 配置是 `num_speculative_tokens: 7`。⭐ **即 V4-Flash 在 Hopper 上拿不到它在 Blackwell 上的全部投机收益**，⛔ §4 的估算已按 Hopper 的 MTP-1 口径处理，⛔ 不要按 DSpark-7 算。

### 2.4 ⭐⭐ prefix caching：我们这份常量 prompt 的实际可缓存量（实测，非估算）

#### 2.4.1 ⭐ 前缀有多大：逐角色精确 token 数

⭐ 本文把 v46-full 里 5 个角色的 system prompt 原文取出，**用三个候选模型自己的 `tokenizer.json` 逐字编码**（`curl .../resolve/main/tokenizer.json` + `tokenizers` 库），得到精确 token 数——⛔ 不是按字符数估的：

| 角色 | system prompt 字符 | 调用次数 | GLM-4.7 | MiniMax M2.7 | DeepSeek V4-Flash |
| :-- | --: | --: | --: | --: | --: |
| ⭐ `requirement_splitter` | **94,722** | 774 | ⭐ **21,534** | 21,515 | 22,300 |
| `assertion_converter` | 70,455 | **1,154** | 15,890 | 15,842 | 16,526 |
| `requirement_reviewer` | 51,129 | 773 | 11,026 | 11,072 | 11,402 |
| `assertion_reviewer` | 37,923 | 612 | 8,025 | 8,041 | 8,342 |
| `result_adjudicator` | 7,208 | 324 | 1,446 | 1,435 | 1,465 |
| ⭐ **可缓存前缀合计** | — | **3,637** | ⭐ **48,907,278** | 48,878,966 | 50,724,914 |
| **占总输入** | — | — | ⭐ **36.9%** | 37.0% | 35.4% |

⚠️ **两处与任务书的差异，据实登记**：① 任务书说 splitter system prompt 是 **95,589** 字符，⭐ **v46-full 实测是 94,722** 字符（`system_prompt_chars` 字段，774 次调用**全部相同**）。差 867 字符，⏳ 未查因（可能取自另一代次或另一变体）。② 任务书说单次输入 25–30K token——⭐ **按开放模型的 tokenizer 算，splitter 的 system prompt 本身就有 21.5K token**，⛔ 加上 user 侧后单次远超 30K。

⭐ **一条对我们有利的意外发现**：这份 prompt 在开放模型 tokenizer 上**比在 Anthropic tokenizer 上更省**——94,722 字符 → GLM-4.7 只用 21,534 token（**4.40 字符/token**），⛔ 而 Anthropic 侧的 `input_tokens` 回归出的口径约 **2.55 字符/token**。全实验总输入因此从 Anthropic 计的 **163.1M** 降到 GLM 口径的 **132.4M**（**0.81×**）。⭐ **换到开放模型跑，输入 token 账面直接少 19%。**

#### 2.4.2 ⭐⭐ 前缀命中的确定性：全实验只有 5 个不同前缀，且逐字节相同

⭐ **实测**：3,637 次调用中，`system_prompt_sha256` 在**每个角色内只有唯一取值**（`requirement_splitter` 774 次同一个 hash、`assertion_converter` 1,154 次同一个、以此类推），`system_prompt_chars` 亦然。⭐ **即前缀不是「大致相同」而是「逐字节相同」**，这一点很关键——vLLM 官方设计文档逐字要求「We only cache **full blocks**」且 hash 沿父块链接，故「a match requires the **entire preceding sequence to be identical**」（[vLLM · Automatic Prefix Caching 设计文档](https://docs.vllm.ai/en/stable/design/prefix_caching/)，核验日 2026-08-13）。⛔ **一个空格之差就会在块边界上丢命中**——⭐ 而我们的 hash 证明不存在这个问题。

⭐ **默认即开**：vLLM `CacheConfig` 里逐字 `enable_prefix_caching: bool = True`（[vLLM API 文档 · config/cache](https://docs.vllm.ai/en/latest/api/vllm/config/cache.html)，核验日 2026-08-13）。⛔ 所以**不需要额外开关**；反而要注意**不要误关**：`GLM-4.7` recipe 里出现过 `--no-enable-prefix-caching`，⚠️ **但那只在 AMD ROCm 的 8 卡配置里**，⛔ 其 4×H200 命令没有这一项。

⚠️ **候选侧的显式旁证**：`DeepSeek-V4-Flash` recipe 里 `--enable-prefix-caching` 出现 4 次，⛔ **但全部在 DGX Spark (GB10) 的 `extra_args` 块里**，⛔ **不是 H200 块**——所以它对 H200 只能算「默认开且官方未禁用」，⛔ 不能说成「官方在 H200 上验证过前缀缓存」。

#### 2.4.3 ⛔⛔ 收益到底有多大：⛔ 不要引「7 倍」，那不是我们的场景

⛔ 网上流传的两类数字必须分开：

| 口径 | 数字 | 来源与设置 | ⛔ 适用于我们吗 |
| :-- | :-- | :-- | :-- |
| ⛔ **单请求冷热对比** | TTFT `4.3 s → 0.6 s`（≈7×）；输出吞吐 `427 → 1,513 tok/s`（+254%） | [Jarvislabs · vLLM Optimization Techniques](https://jarvislabs.ai/blog/vllm-optimization-techniques)，Qwen3-32B、~10,000 token 提示，**第二次发同一请求** | ⛔⛔ **不适用**。它测的是「同一请求发两遍」的第二遍，⛔ 而且**只改善 TTFT**，我们的离线批量作业不看 TTFT |
| ⭐ **并发下受控 A/B** | vLLM **吞吐 +13.3%**、TPOT +9.8%（TensorRT-LLM 同实验 +34.7% / +20.9%） | [SqueezeBits · vLLM vs TensorRT-LLM #12: Automatic Prefix Caching](https://blog.squeezebits.com/vllm-vs-tensorrtllm-12-automatic-prefix-caching-38189)，**共享 system prompt 数据集**、多个输入长度与并发档 | ⭐ **这才是我们的场景**：稳定并发 + 共享前缀 |

⭐ **本文的收敛估算**：可缓存前缀占输入 36.9% → prefill 时间最多省 36.9%；而 prefill 只占墙钟 11%–49%（§4.2）→ ⭐ **端到端墙钟收益 4.2%–17.4%**，与 SqueezeBits 那条 +13.3% 同量级、略低（因为我们的共享比例只有 36.9%，而非全 prompt 共享）。

⛔⛔ **所以对「这一项可能决定成败」这个预期，答案是否**：它值得开（默认已开、零成本、不改输出），⛔ 但它省下的是**不到一小时**，⛔ 而候选之间的差距是**十几个小时**。⭐ **真正决定成败的是 §1 的 KV 表与 §2.1 的激活参数表。**

⚠️ **一条会吃掉收益的已知交互**：vLLM 上同时开 chunked prefill 与 prefix caching 曾被报告即使命中率 94.5% 仍 TTFT 恶化（[vLLM issue #8223](https://github.com/vllm-project/vllm/issues/8223)）。⏳ 该 issue 的当前状态与是否已修**本文未核**，⛔ 但因为我们不看 TTFT，风险等级低。

## 3. 「能部署但不适合做实验」的具体判据与候选

### 3.1 ⭐ 三条判据（⛔ 「装得下」不在其中）

⭐ 一个候选**能部署**只需要「权重 ≤ 预算」；⭐ 而**适合做实验**要同时过三道，⛔ 缺一条就不适合：

| 判据 | 定义 | 为什么它是硬的 |
| :-- | :-- | :-- |
| **J1 · 并发容量** | $\mathrm{KV\ budget} / (B \cdot T) \ge$ 目标并发 | ⭐ decode 聚合吞吐 ≈ 单序列速度 × 并发。⛔ 并发被 KV 卡死，decode 就被卡死，⛔ 而 decode 占墙钟 51%–89%，六档里五档 >68% |
| **J2 · 每 token 成本** | 激活参数 $P_{act}$ 越大，prefill 的 FLOPs 与 decode 的显存读取量**同向**放大 | ⛔ 没有一个阶段能补偿另一个；⛔ 也不能靠「总参数量小」救 |
| **J3 · 格式内核在 Hopper 原生** | 权重格式在 cc 9.0 上有原生张量核，⛔ 不是 Marlin 一类回退 | ⛔ 回退**省显存不省速度**：它让模型装得下，⛔ 却不让它跑得快 |

⛔⛔ **J3 是最容易被「装得下」这个结论掩盖的一条**，[h200x4_envelope.md](./h200x4_envelope.md) §4.3 已把六条官方逐字列全。⭐ **本文把它升级成准入判据**：过不了 J3 的候选，其容量表上的 ✅ 没有性能含义。

### 3.2 ⚠️ 先纠正一个常见误推：「大 MoE 在低并发下效率差」——⛔ 主语是**激活参数多**的 MoE，不是**总参数多**的 MoE

⭐ 文献侧的机制是清楚的：MoE 的 decode 是**显存带宽受限**，且瓶颈在**专家权重搬运**而非计算。关键点是算术强度（arithmetic intensity）：稠密模型里一次权重加载被整个 batch 摊薄，⛔ 而 MoE 里 gate 把 batch 切给不同专家，权重复用只发生在共享同一专家的 token 之间；专家越多越细粒度，碎片化越严重、算术强度越低。⭐ 形式化地说，MoE 专家层的有效算术强度随 $bs \cdot \lambda$（$\lambda = N_{active}/N_{total}$）而非 $bs$ 增长，⛔ **故即使在大 batch 下专家层仍是 memory-bound，且它同时是延迟的主导项**。

⛔ **同时存在一个反向张力（batching paradox）**：batch 越大，被激活的**专家并集**越大，稀疏性收益被抵消——⛔ 于是要么在 BS=1 付「每 token 搬一次权重」的代价，要么在大 batch 下几乎激活整个模型。有实测报告为满足 25 ms SLO 时**中位 decode 迭代有 42% 花在从 HBM 取激活专家权重上**。

⚠️ **出处与核验等级**：以上机制取自 [MoE-Gen（arXiv 2503.09716）](https://arxiv.org/html/2503.09716v1)、[Lynx（arXiv 2411.08982）](https://arxiv.org/html/2411.08982)、[XShare（arXiv 2602.07265）](https://arxiv.org/html/2602.07265) 与 [Cohere · Why MoE Models Get More From Speculative Decoding](https://cohere.com/blog/mixture-of-experts-models-get-more-from-speculative-decoding)，核验日 2026-08-13。⛔⛔ **本文只核到检索摘要层，未逐字回原文 PDF 对照**，⛔ 故这四条按 **S 级（二手）** 记账，⛔ 不得当作 M 级引用。⭐ **但下面的裁定不依赖它们**——裁定的承重证据是 §2.1 的 roofline 与 §2.2 的三条实测。

⭐⭐ **由此得出的关键纠正**：上述机制里，「慢」的自变量始终是**每 token 实际搬运的权重量**，⛔ 而那由 $P_{act}$ 决定，**不由总参数量决定**。⭐ 所以在我们这四个候选里：

- ⭐ `DeepSeek V4-Flash`（284B 总 / **13B 激活**）与 `MiniMax M2.7`（230B 总 / **10B 激活**）属于**低激活 MoE**，⭐ 它们恰恰是**受这个问题影响最小**的那一类。
- ⛔ `GLM-4.7`（~**32B 激活**）与 `GLM-5.2`（~**39B 激活**）才是受影响最重的，⛔ **而它们的总参数量反而更小**（358B / 与 V4-Flash 同量级）。

⛔⛔ **所以「V4-Flash 是大 MoE 所以慢」这个推理链在这一组候选上是反的。** ⭐ 实测同向：V4-Flash 在 H200 TP=4 上 BS=1 decode **266 tok/s**（§2.2-C），⛔ 而这已经**高于** MiniMax M2.5 在 4×H200 上 32K 单请求的 **81 tok/s**（§2.2-A）——⚠️ 两者口径不同（前者含 1.92× 投机、后者明确关闭投机；前者 SGLang、后者 vLLM），⭐ **但即便把投机除掉，V4-Flash 的 138 step/s 仍高于 81。**

### 3.3 ⛔ 逐候选裁定

| 候选 | J1 并发 | J2 激活参数 | J3 Hopper 原生 | 裁定 | ⭐ 判据落点 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| ⭐ `DeepSeek V4-Flash-0731` | ⭐ **228**（余量 6×） | ⭐ **13B**（最小档） | ⚠️ **FP4+FP8 混合，⏳ FP4 内核路径未核** | ⭐ **可行** | ⭐ J1/J2 双优；⭐ J3 有 §2.2-C 的 H200 TP=4 实测**反证它确实跑得动 Hopper** |
| `MiniMax M2.7` | **36** | ⭐ **10B**（最小） | ✅ **原生 FP8**，Hopper 有 FP8 张量核 | ✅ **可行** | ⭐ 三条全过，且是唯一有**卡数完全对齐**的第三方实测 |
| ⛔ `GLM-4.7-FP8` | ⛔⛔ **6.8**（官方自己写 batch ≤ 8） | ⛔ **~32B**（3.3×） | ✅ 原生 FP8 | ⛔ **能部署，不适合** | ⛔ **J1 与 J2 同时最差**；⭐ 唯一翻身点是 MTP（~90% accept） |
| ⛔⛔ `GLM-5.2-NVFP4` | 15.6 | ⛔ **~39B**（4.0×） | ⛔⛔ **NVFP4 非 Hopper 原生**；card 逐字 `Test Hardware: NVIDIA B200` | ⛔⛔ **不可行** | ⛔ **J3 直接否掉**；⛔ 且 J2 最差；⛔ 零 H200 实测 |

#### ⛔ 为什么 `GLM-4.7-FP8` 是「能部署但不适合做实验」的标准样本

⭐ 它**完全能部署**——[vLLM recipes `GLM-4.7.yaml`](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-4.7.yaml) 有一节逐字写着 `### Tensor Parallel + MTP (FP8 on 4xH200)`，`h200: verified`，`Hardware: 4x-8x H200 (FP8)`。⛔ **但三件事叠起来让它不适合做我们这个实验**：

1. ⛔⛔ **J1 被 KV 卡死。** 368 KiB/token 是四个候选里最高的（是 V4-Flash 的 **7.6 倍**），而它的权重又最大 → **KV 预算最小 × 单序列 KV 最大**，两头相乘得到并发 6.8。⭐ 官方自证：GLM-4.5 card 给 `H200 x 4` 那一档时前置条件逐字「batch size does not exceed 8」。
2. ⛔ **J2 使 prefill 也最慢。** 实测 12,186 tok/s（§2.2-B），⛔ 只有 MiniMax 的 **48%**。
3. ⛔ **不确定度本身就是问题。** §4 给出的区间是 **8.5 – 24.0 h**，⭐ 而这 2.8 倍的宽度不是估算粗糙，⛔ **是三个未定项的真实乘积**：KV 预算 77 还是 144.8 GB（§1.3）、FP8 KV 能否开、MTP 实际 accept 多少。⛔ **一个无法排期的候选，即使均值可接受也不该选**——它会让「跑一代次」变成「可能今晚出、也可能明晚出」。

⛔ **另有一条容易被忽略的主机侧门槛**：GLM-4.5 card 逐字「**Server memory must exceed `1T`**」（[h200x4_envelope.md](./h200x4_envelope.md) §4.1 已核）。⛔ 这是**主机内存**不是显存，⛔ 若那台 4 卡机只有 512 GB 内存，按官方口径连加载都不保证。⏳ GLM-4.7 是否沿用该门槛未见明文。

### 3.4 ⭐ 反过来：哪个候选在 4×H200 上吞吐**明确够用**

⭐ **`MiniMax M2.7` 是唯一一个「卡数、精度、上下文档位全部对齐」的实测背书候选**：[Millstone 的报告标题本身就是 `4x H200 SXM (FP8)`](https://www.millstoneai.com/inference-benchmark/minimax-m2-5-fp8-4x-h200-sxm)，32K 档给出 `Capacity: 18 requests` 与聚合 450 tok/s，且**是在关闭 prompt caching、关闭投机解码、满精度 KV** 的条件下测的——⭐ **即这是下界，我们把这三项打开只会更好。** ⛔ 唯一的外推是 M2.5 → M2.7。

⭐ **`DeepSeek V4-Flash-0731` 的背书更强也更弱**：更强的地方是它的实测**提示长度正好 30K、卡数正好 TP=4、硬件正好 H200**（§2.2-C）；⛔ 更弱的地方是**只有 decode 一个数、没有 prefill/TTFT**，且来自 SGLang 自己。⭐ 但它还有一条独立的官方旁证：`h200: verified` 出现在其 vLLM recipe 的 `hardware` 白名单里，且**推荐部署逐字**是「single-node DP + EP with `--data-parallel-size 4` … uses **4 of 8 GPUs per replica on H200**/B200/B300」——⭐ **即官方把「4 张 H200 跑一个副本」写成了推荐形态**，⛔ 不是勉强可跑。

⛔ **一条不要过度解读的事**：`--max-num-seqs 512` 出现在其 recipe 里，⛔ **但那是 AMD MI355X 的示例命令**，⛔ 不是 H200 的实测并发。⭐ 我们对它的并发信心来自 §1.2 的 KV 算术（228），⛔ 不来自这个参数。

## 4. 端到端墙钟估算（含假设与不确定度）

### 4.1 ⛔ 先把假设摆全（⛔ 每一条都能被单独推翻，⛔ 不要只引结论数字）

**负载（⭐ 实测，非假设）**：3,637 次调用；总输入 **132.2 / 132.4 / 143.3M token**（M2.7 / GLM-4.7 / V4-Flash 各自 tokenizer）；常量前缀 **48.9 / 48.9 / 50.7M**（36.9% / 36.9% / 35.4%）；总输出 **~18.5M token**（⚠️ 取 Anthropic 计 17.4M 与 GLM tokenizer 估 19.8M 的中值）。

**A1 · prefill 速率取值**：

| 模型 | 取值 | 来源与不确定度 |
| :-- | --: | :-- |
| `MiniMax M2.7` | **25,000 tok/s** | ⭐ 由 Millstone `32K / 1 req` 的 `TTFT = 1.3 s` 反解（$32768/1.3 = 25{,}206$）。⚠️ 不确定度 ±20%：TTFT 含调度与首块开销；⛔ 且是 M2.5 外推到 M2.7 |
| `GLM-4.7-FP8` | **12,186 tok/s** | ⭐ 由 GPUStack `32K in × 100 prompts / 262.58 s` 直接反解。⚠️ ±15%：⛔ 测的是 GLM-4.6 且未开 MTP（⭐ MTP 主要加速 decode，对 prefill 影响小） |
| `DeepSeek V4-Flash` | ⚠️ **20,000 tok/s** | ⛔⛔ **无任何实测，这是本文最弱的一个数**。构造方式：取另两条实测的 MFU 区间（6.2%–9.9%）乘它的 roofline 247.8K → **15.4K–24.5K tok/s**，取中值 20K。⚠️ 不确定度 **±25%**，⛔ 且未计 FP4 在 Hopper 上可能的反量化开销（见 §5.1） |

**A2 · decode 聚合吞吐取值**（= 单序列速度 × 有效并发）：

| 模型 | 保守档 | 乐观档 | 依据 |
| :-- | :-- | :-- | :-- |
| `MiniMax M2.7` | **450 tok/s**（18 并发 × 25） | **500 tok/s**（36 并发） | ⭐ 保守档是 Millstone 32K 实测三点之一（`18 req → 25 tok/s/user`）。⭐ 乐观档按 KV 上限 36 并发外推，⛔ **只加 11%**——因为该页实测 $8 \to 18$ 并发时聚合仅从 376 涨到 450（2.25× 并发换 1.20× 吞吐），⛔ **已明显饱和** |
| `GLM-4.7-FP8` | ⛔ **245 tok/s**（7 并发 × 35，BF16 KV，无 MTP） | **774 tok/s**（13 并发 × 35 × 1.7 MTP，FP8 KV） | ⚠️ 单序列 35 tok/s 取自 GPUStack 的 TPOT 区间（低并发 18.11 ms → 55 tok/s；高并发 144–256 ms → 4–7 tok/s）中的 30K 档插值，⛔ **这一步是本档最大的软点**。并发按 §1.3 的两个 KV 口径分档；MTP 1.7× 由官方「~90%+ acceptance @ 1 draft token」推得 |
| `DeepSeek V4-Flash` | **1,000 tok/s**（batch 32） | **2,500 tok/s**（batch 64） | ⭐ 锚点是实测 BS=1 = **266 tok/s**（含 1.92× 投机）。⚠️ 上界由「全专家激活」roofline 约束：读全部 166.9 GB 权重需 $166.9/19{,}200 = 8.7$ ms → **115 step/s**，故 batch $B$ 下聚合上限 $= 115B$（B=32 → 3,680；B=64 → 7,360）。⛔ 取其 27%–34% 作为实际值，⛔ **这个折扣系数是本文自己定的，无实测支撑** |

**A3 · 两种时间模型**：**串行合计** $= t_{prefill} + t_{decode}$（悲观，假设两阶段不重叠）；**重叠下界** $= \max(t_{prefill}, t_{decode})$（乐观，假设 continuous batching 完全重叠）。⭐ 真实值落在两者之间，⭐ 而因为 decode 普遍占主导，⛔ 两者差距不大（≤ 30%）。

**A4 · ⛔ 未计入的成本**（⛔ 故下表全部偏乐观）：模型加载与预热（TP=4 下加载 166–430 GB 权重通常 5–20 分钟）、`flashinfer_autotune`、失败重试、schema 解析失败后的原地重试、编排层串行依赖（⭐ **本实验是多阶段流水线，同一格内 splitter → reviewer → converter 有序，⛔ 无法把 3,637 次调用全铺平**）。⛔⛔ **最后这一条可能是最大的低估源**：若编排层的并发度低于 A2 假设的 batch，decode 时间会成比例放大。

### 4.2 ⭐ 结果表

| 候选 | 档 | prefill | decode | ⭐ 串行合计 | 重叠下界 | decode 占比 | 含 prefix cache |
| :-- | :-- | --: | --: | --: | --: | --: | --: |
| ⭐ **DeepSeek V4-Flash** | 乐观 | 1.99 h | **2.06 h** | ⭐ **4.05 h** | 2.06 h | 51% | ⭐ **3.34 h** |
| ⭐ **DeepSeek V4-Flash** | 保守 | 1.99 h | 5.14 h | ⭐ **7.13 h** | 5.14 h | 72% | 6.42 h |
| ⛔ `GLM-4.7-FP8` | 乐观 | 3.02 h | 6.64 h | 9.66 h | 6.64 h | 69% | **8.54 h** |
| `MiniMax M2.7` | 乐观 | 1.47 h | 10.28 h | **11.75 h** | 10.28 h | 88% | **11.20 h** |
| `MiniMax M2.7` | 保守 | 1.47 h | 11.42 h | **12.89 h** | 11.42 h | 89% | 12.35 h |
| ⛔⛔ `GLM-4.7-FP8` | 保守 | 3.02 h | ⛔ **20.98 h** | ⛔⛔ **23.99 h** | 20.98 h | 87% | 22.88 h |
| ⛔⛔ `GLM-5.2-NVFP4` | — | ⏳ | ⏳ | ⛔⛔ **拒绝估算** | — | — | — |

⭐ **朴素基线臂**（324 次 × ~30K = 9.7M token 输入，输出量极小）：V4-Flash **0.13 h** · M2.7 **0.11 h** · GLM-4.7 **0.22 h**。⭐ **一律只占主臂的 7% 以下，⛔ 它不是任何候选的约束。**

### 4.3 ⭐ 三条从表里读出来的结论

1. ⭐⭐ **decode 占墙钟 51%–89%（六个档位里五个 >68%）**，⛔ 故「prefill 是主要成本」这个前提在**任何一档下都不成立**。⭐ 优化顺序应是：**投机解码 > 提高并发（等价于省 KV）> prefix caching > prefill 算力**。
2. ⭐ **prefix caching 的端到端收益 4.2%–17.4%**（省 0.5–0.7 h）。⭐ 上限出现在 V4-Flash 乐观档——⛔ 恰恰因为那一档 decode 已经很快、prefill 占比升到 49%。⛔ **即 prefix caching 越有用的场合，恰是总时间已经最短的场合**，⛔ 它救不了慢的那一头。
3. ⛔⛔ **`GLM-4.7` 的区间宽度（8.5 – 24.0 h，2.8×）本身就是拒绝它的理由。** ⭐ 分解：KV 预算 77 vs 144.8 GB 贡献 1.9×、MTP 是否生效贡献 1.7×，二者相乘 3.2×（部分被 prefill 抵消到 2.8×）。⛔ **两个未定项都不是估算精度问题，是「没实测过」**——⛔ 而且**都只能在那台机器上跑一次才知道**。

### 4.4 ⚠️ 不确定度总账（⛔ 不要把上表当预测，它是量级）

| 不确定源 | 影响面 | 量级 | 能否事先消除 |
| :-- | :-- | :-- | :-- |
| ⛔⛔ 编排层实际并发度（A4 末条） | **全部候选的 decode** | ⛔ 可能 **2–5×** | ⭐ **能**：读一遍 `discover` 的编排代码，数清同一时刻在飞的调用数上限。⛔ **本文未做，这是最该先补的一项** |
| ⛔ V4-Flash 无 prefill 实测 | V4-Flash 的 1.99 h | ±25% | ⏳ 只能实测 |
| ⛔ V4-Flash 大 batch decode 折扣系数自定 | V4-Flash 的 2.06–5.14 h | ⛔ **2.5×**（该行区间全部由它产生） | ⏳ 只能实测 |
| ⛔ GLM-4.7 的 KV 预算口径（§1.3） | GLM-4.7 并发 | 1.9× | ⭐ 能：启动后读 vLLM 日志里的 KV cache 块数 |
| ⛔ GLM-4.7 MTP 实际 accept | GLM-4.7 decode | 1.7× | ⭐ 能：vLLM 会打印 accept rate |
| ⚠️ M2.5 → M2.7 外推 | M2.7 全部数字 | ⚠️ ±20% 猜测 | ⏳ 只能实测 |
| ⚠️ 输出 token 总量（17.4M vs 19.8M） | 全部 decode | ±7% | ⭐ 能：换 tokenizer 重算一次 |

## 5. 待核验与访问受限

### 5.1 ⛔ 本轮的核心缺口（按对结论的影响排序）

1. ⛔⛔ **`DeepSeek V4-Flash` 在 H200 上的 prefill / TTFT 完全缺失。** LMSYS 那页只给 decode（`Decode throughput is 1000 / TPOT (ms)`），⛔ 对长上下文 TTFT 只有定性描述。⭐ 而 §4 给它的 prefill 1.99 h 是**用别人的 MFU 反推的**，⛔ 是全表最弱的一个数。**补法**：`vllm bench serve --random-input-len 30000 --random-output-len 2000` 在目标机上跑一次即可。
2. ⛔⛔ **FP4 权重在 Hopper 上的内核路径未核。** V4-Flash 的 `expert_dtype: "fp4"` 是**原生混合精度**（`config.json` 逐字），⛔ 而 Hopper（cc 9.0）没有原生 FP4 张量核。⚠️ **反向证据是强的**：LMSYS 明确在 **H200 TP=4** 上测出了 266 tok/s，⭐ 说明它确实跑得动；⛔ **但 decode 是带宽受限的（FP4 存储反而有利），prefill 是算力受限的（反量化开销会直接吃掉它）**。⛔ **所以「decode 有实测」不能推出「prefill 没问题」**——这正好是缺口 1 的原因。
3. ⛔⛔ **编排层的真实并发度未核。** §4 的 A2 假设我们能同时在飞 18–64 个请求，⛔ 但本实验是**多阶段有序流水线**（一格内 splitter → reviewer → converter → adjudicator 串行）。⛔ 若实际在飞请求数只有个位数，**全部候选的 decode 时间要乘 2–5 倍**。⭐ **这是最该先补且最容易补的一项**：读一遍 `discover` 的编排代码数并发上限即可，⛔ 本文未做。
4. ⛔ **`GLM-4.7` 的两个 1.9× / 1.7× 未定项**（KV 预算口径、MTP 实际 accept），见 §4.4。⭐ 两者都能在启动后从 vLLM 日志直接读到。
5. ⚠️ **M2.5 → M2.7 的外推未验证。** Millstone 测的是 M2.5；⏳ 两者 `config.json` 的层数/头数是否一致本文**只核了 M2.7**（62 层、8 KV 头、128 head_dim），⛔ **未取 M2.5 的 config 对照**。若 M2.5 层数不同，KV 与吞吐都要重算。
6. ⚠️ **`GLM-4.7` 的主机内存门槛未核。** GLM-4.5 card 逐字要求 `Server memory must exceed 1T`；⏳ GLM-4.7 是否沿用未见明文。⛔ 这是**主机内存**，若那台机只有 512 GB，按官方口径连加载都不保证。
7. ⏳ **`MiniMax M2.7` 是否支持投机解码未核。** 若支持，它的 decode（占其墙钟 88%）可能再降 1.5–2×，⭐ **足以把它从 11.8 h 拉到 6–8 h**，与 V4-Flash 拉近。⛔ 本文按不支持处理，⛔ 故对它偏保守。
8. ⏳ **prefix caching 与 DSA / 压缩 KV 的兼容性未核。** V4-Flash 有 `sliding_window: 128` 与逐层压缩、GLM-5.2 全层是 `deepseek_sparse_attention`；⛔ vLLM 官方设计文档**未提**这些注意力族下前缀缓存的限制（本文已直接问过该页）。⏳ 未知它是否降级或失效。
9. ⏳ **Millstone 那条 `Prefill Speed (per user)` 的标签歧义未裁定**（§2.2-A）。⛔ 本文绕开它改用 TTFT 反解，⛔ 但若该列真是聚合值，M2.7 的 prefill 应上调 20%（对结论无影响，因为 decode 主导）。
10. ⏳ **`vllm issue #8223`（chunked prefill × prefix caching 恶化 TTFT）的当前状态未核。** ⛔ 对我们风险低（不看 TTFT），⛔ 但若它同时影响吞吐则需重估。

### 5.2 ⚠️ 证据等级登记

| 事实 | 级别 | 说明 |
| :-- | :-: | :-- |
| 全部 `config.json` 字段（层数 / KV 头 / head_dim / `kv_lora_rank` / `attn_type_list` / `layer_types` / `kv_cache_scheme`） | **M** | `curl .../raw/main/config.json` 原文，核验日 2026-08-13 |
| H200 规格（`3,958 TFLOPS` 含稀疏 / `4.8TB/s` / `141GB`） | **M** | NVIDIA 官方产品页；⚠️ 该页自标 `Preliminary specifications` |
| v46-full 的 3,637 次调用 token 与 `system_prompt_sha256` 统计 | **M** | 本仓库 run record 全量聚合，可复现（§5.3） |
| 5 个 system prompt 的精确 token 数 | **M** | 用各模型官方 `tokenizer.json` 逐字编码 |
| `MiniMax-M2.5` 4×H200 实测三表 | **S** | 第三方（Millstone）；⛔ 无 vLLM 版本、无 TP 设置；⛔ 是 M2.5 |
| `GLM-4.6-FP8` TP4 H200 实测 | **S** | 第三方（GPUStack）；⭐ 有引擎版本；⛔ 是 GLM-4.6 |
| `DeepSeek V4-Flash` H200 TP=4 decode 266→240 tok/s | **S** | SGLang 自家博客；⛔ 无版本号 |
| vLLM `enable_prefix_caching = True` 默认、块级精确前缀匹配 | **M** | vLLM 官方 API 文档与设计文档 |
| 官方 4×H200 recipe（GLM-4.7 `4xH200` + MTP、MiniMax `4x H200`、V4-Flash `h200: verified`） | **M** | vLLM `recipes` 仓库 yaml 逐字 |
| MoE 低算术强度 / batching paradox / 42% decode 迭代取权重 | ⚠️ **S** | ⛔ **只核到检索摘要层，未回原文 PDF 逐字对照** |
| 激活参数量 `GLM-4.7 ~32B` / `GLM-5.2 ~39B` | ⚠️ **I** | ⛔ **本文按 `config.json` 自行推算，无官方披露**。⭐ 同法算 M2.7 得 9.8B 对官方 10B、V4-Flash 得 16.0B 对官方 13B，⛔ **故该方法有 +23% 的高估倾向** |
| §4 全部墙钟数字 | ⚠️ **I** | ⛔ **是估算不是实测**，假设见 §4.1，不确定度见 §4.4 |

### 5.3 核验方法（可复现）

```bash
# KV 相关字段（本文全部 config 事实的来源）
curl -s https://huggingface.co/zai-org/GLM-4.7-FP8/raw/main/config.json | python3 -m json.tool
curl -s https://huggingface.co/MiniMaxAI/MiniMax-M2.7/raw/main/config.json | python3 -m json.tool
curl -s https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/raw/main/config.json | python3 -m json.tool
curl -s https://huggingface.co/nvidia/GLM-5.2-NVFP4/raw/main/config.json | python3 -m json.tool

# 官方 4×H200 recipe
curl -sL https://raw.githubusercontent.com/vllm-project/recipes/main/models/zai-org/GLM-4.7.yaml
curl -sL https://raw.githubusercontent.com/vllm-project/recipes/main/models/MiniMaxAI/MiniMax-M2.7.yaml
curl -sL https://raw.githubusercontent.com/vllm-project/recipes/main/models/deepseek-ai/DeepSeek-V4-Flash.yaml

# v46-full 负载全量聚合（3637 份 record，约 814 MB）
find runs/paper1/matrix-v46-full -type d -name "*llm-call-completed" | wc -l
# 逐份读 input_tokens / output_tokens / system_prompt_sha256 / system_prompt_chars 并按 role 汇总

# 前缀 token 精确计数
pip install tokenizers
curl -sL https://huggingface.co/zai-org/GLM-4.7-FP8/resolve/main/tokenizer.json -o tok.json
# Tokenizer.from_file('tok.json').encode(system_prompt).ids 取长度
```

⭐ **在目标机上应当先跑的两条**（⛔ 它们能一次性消掉 §5.1 的第 1、4 项）：

```bash
# 30K 输入 / 2K 输出，逐并发档扫，直接读 prefill 与聚合 decode
vllm bench serve --model <MODEL> --dataset-name random \
  --random-input-len 30000 --random-output-len 2000 \
  --num-prompts 64 --max-concurrency 8   # 再扫 16 / 32 / 64

# 前缀复用的 A/B（⛔ 基线必须显式关掉，因为默认是开的）
vllm bench serve --dataset-name prefix_repetition \
  --prefix-repetition-prefix-len 21534 --prefix-repetition-suffix-len 15000 \
  --prefix-repetition-num-prefixes 5 --prefix-repetition-output-len 2000
# 对照组加 --no-enable-prefix-caching
```

⚠️ **上面第二条的参数不是随手填的**：`prefix-len 21534` 就是 §2.4.1 实测的 splitter system prompt token 数，`num-prefixes 5` 就是全实验的不同前缀个数。

### 5.4 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 | 建档。§1 四候选 KV footprint 与 30K 并发上限（全部回 `config.json`）；§2 三条 H200 级实测（Millstone 4×H200 / GPUStack TP4 / LMSYS H200 TP=4）+ roofline 交叉校验 + prefix caching 实测量化；§3 三条准入判据与逐候选裁定，⭐ **纠正「大 MoE 慢」的主语误置**；§4 端到端墙钟六档估算；§5 十条缺口。⭐ **两条对任务书前提的纠正**：负载输入被低估 22%（实测 132.4M 而非 108.6M）、⭐ **decode 而非 prefill 是瓶颈（占 51%–89%）**。 |
