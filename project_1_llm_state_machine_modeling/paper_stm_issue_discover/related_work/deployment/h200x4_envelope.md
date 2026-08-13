# 4×H200 部署包络与能力定位

> **本文回答一个问题**：作者手头的 **4×H200（141 GB HBM3e/卡，共 564 GB 标称）** 里，能装下的最强开放权重模型是谁，它离前沿闭源还差多少。⛔ 本文不论证 story，⛔ 不做选型建议——只把「装不装得下、装下的实测多强、4-bit 掉不掉分、4 卡跑不跑得动」变成可查证的事实。服务 [SUMMARY.md](./SUMMARY.md) §0b。
>
> **核验日**：2026-08-13。**权重体积的一手来源**：Hugging Face Model API（`/api/models/{id}?blobs=true` 的逐文件 `size` 字段）与各仓库 `config.json` 原文。⛔ 所有体积均为**实测 shard 字节数**，⛔ 不是按参数量推算。
>
> ⚠️ **与本目录既有文件的分工**：[open_weight_model_compute.md](./open_weight_model_compute.md) 是**权重体积的主真源**（145 个仓库、141 行主表），本文**不重建那张表**，只追加本轮新探仓库并按 4×H200 这一个包络重算。[hardware_availability.md](./hardware_availability.md) 回答「中国工业单位实际买得到多少显存」。[benchmark_open_weights.md](./benchmark_open_weights.md) 是**能力分数的主真源**（AA-LCR 全表等）。⛔ 不要把本文当成这三者中任何一个的第二真源。
>
> ⚠️ **此前基于「单卡 24 GB」的分析在本文语境下已作废**——那个假设与作者实际可用算力不符。⛔ 但 [open_weight_model_compute.md](./open_weight_model_compute.md) 的单卡档表**依然有效且不必改**：它服务的是「中国工业单位买得到什么」这个不同的问题。

## 0. 一句话结论

✅ **六节全部闭合。** §1（实测体积）· §2（能力定位，AA 已提到 **M** 级）· §3（量化退化）· §4（工程可行性）· §5（件的归属）· §6（13 条待核缺口，含 **4 条未裁定的两源冲突**）。

**⭐ 「487 GB 内最强开源模型是谁」有三个答案，逐层收紧；⛔ 只报第一个是失真的**：

| 约束 | 答案 | v4.1.1 总分 | 件与体积 | ⛔ 问题 |
| :-- | :-- | ---: | :-- | :-- |
| ① 只按容量 | `GLM-5.2` | **52.64** | 三方 [nvidia/GLM-5.2-NVFP4](https://huggingface.co/nvidia/GLM-5.2-NVFP4) **464.8 GB** | ⛔ 三方件 · ⛔ 贴边 · ⛔⛔ **NVFP4 内核是 Blackwell 原生，card 只写「Test Hardware: B200」** |
| ② + 必须作者件 | `DeepSeek V4-Flash-0731` | **51.77** | 作者 [deepseek-ai/…-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) **166.9 GB**，MIT | ⭐ 余量 320 GB · ⏳ 其 FP4 部分在 Hopper 上的内核路径未核 · ⛔ **幻觉净分 −14.3（负）** |
| ③ + 格式在 Hopper 安全 + 有官方 4×H200 说法 | ⭐ `MiniMax M2.7` | **38.87** | 作者原生 **FP8 230.1 GB** | ⭐ vLLM recipe 逐字 `You can use 4x H200/H20/H100` · ⛔ 自定义许可 |

⛔⛔ **①②③ 之间差 13.8 分，而这个落差不是能力问题，是「格式内核是否 Blackwell 专属」造成的。** H200 是 **Hopper（cc 9.0）**，⛔ 不是 Blackwell；而把 400B+ 模型压进 487 GB 所依赖的 NVFP4 / MXFP8，其高性能内核官方一致指向 Blackwell（§4.3 有六条逐字）。⛔ **`Motif-3-NVFP4`（总分 47.4、186.9 GB）因此整体失效**——其 card 逐字「NVFP4 requires NVFP4-capable hardware (NVIDIA Blackwell / B200)」，而它的 BF16 档是 629.7 GB，也装不下。

**与前沿闭源的差距**：`Claude Opus 5 (max)` = **63.05**（**M** 级，官方数据集）。① 差 **10.41 分、比值 0.835**；② 差 **11.28 分、比值 0.821**；③ 差 **24.18 分、比值 0.616**。⭐ **参照：≤32B 档的 `Qwen3.6-27B` 是 37.70，差 25.35 分、比值 0.598。** ⛔⛔ **注意第 ③ 层（0.616）几乎回到了 ≤32B 档的水平（0.598）**——即**若坚持「作者件 + Hopper 原生格式 + 官方已验证 4 卡」三条，4×H200 相对单卡小模型的能力增益几乎被吃光**。⭐ 放宽到第 ② 层（只要作者件、接受 FP4 内核未核）才能拿到「差距减半」。

⛔⛔ **五条最容易搞错的事实**：

1. ⛔⛔ **「按总分挑最强」是错的挑法，因为幻觉维度的符号会变。** `Claude Opus 5` 的 **AA-Omniscience 净分 = +37.1**；装得下的模型里 `GLM-5.2` 是 **+4.4**（⛔ 比值 **0.119**，全维度最差），⛔ 而总分第 2 的 `DeepSeek V4-Flash` 是 **−14.3**——**符号相反**。⭐ 这一维度权重 **12%（是 AA-LCR 的两倍）**，且直接对应我们的核心失败模式（判定器凭空报缺陷）。⛔ **本包络下最该担心的是这个，不是总分。** 详见 §2.4。
2. ⭐ **反过来，在我们最承重的 AA-LCR 上，装得下的模型已经反超前沿**：`MiniMax M3` **80.3** vs Opus 5 **75.7**（反超 4.6）· `GLM-5.2` **76.7**（反超 1.0）· `DeepSeek V4-Flash` 74.3（差 1.4，比值 0.982）。⛔ **但 AA-LCR 只占 Index 权重 6%**，⛔ 只报这一条是失真的。
3. ⛔ **「必须靠 4-bit 才装得下」这个前提在本包络下不成立。** 首选的 `DeepSeek V4-Flash-0731` 是**原生混合精度**、`MiniMax M3` 走**官方 MXFP8（8-bit）**、`Qwen3.5-397B` 走**官方 FP8**。⛔ 4-bit 退化风险**只对 GLM-5 / 5.1 / 5.2 这三个「官方 FP8 装不下、必须走三方 NVFP4」的候选适用**（见 §3）。
4. ⛔ **DeepSeek 从未发布过任何官方 4-bit 权重。** 穷举 `deepseek-ai` 名下**全部 102 个仓库**，用 `int4|awq|gptq|nvfp4|fp4|4bit|w4a|mxfp4|int8|w8a8|bnb` 匹配仓库名，**命中 0**。V3.x / R1 是原生 FP8（689.5 GB，⛔ 装不下），V4 系是原生 FP4+FP8 混合（⚠️ **这是原生精度，不是额外发的量化件**）。⛔ 而 `DeepSeek V3.2` 在本包络下**不值得追**：总分只有 **32.80**（且是 AA 估算值），⛔ **低于一堆装得下的模型**。
5. ⛔ **被显存挡在门外的是「差距不是钱能补的那部分」。** ⛔ 开放权重全场第一的 `Kimi K3`（总分 **59.70**，只差 Opus 5 **3.35** 分）需要 1560.9 GB，⛔ **超预算 3.2 倍**；`DeepSeek V4-Pro`（**53.00**）需要 864.7 GB 且**已经是 FP4**；`Kimi K2.5/K2.6/K2.7-Code` 三代的官方原生 INT4 **一律 595.2 GB**，⛔ 超预算 108 GB 且**没有更小的官方档**（`moonshotai` 名下零个独立量化仓库）。⛔ **稀疏一点不降常驻显存**：K3 只激活 104B。

**本轮探测规模**：共探测 **35 个 HF 仓库**，其中 **30 个是 [open_weight_model_compute.md](./open_weight_model_compute.md) 未收录的新仓库**；**29 个成功取到实测体积**，⛔ 1 个返回 401（`moonshotai/Kimi-K2.7`，该名下公开的是 `-Code` 变体）。

## 1. 逐模型能否装下（实测体积表）

### 1.1 判据（⛔ 每个 ✅ / ❌ 都由这一条产生）

**主判据（本文口径）**：$V = 564$ GB 标称。$0.92V = 518.88$ GB（vLLM 默认 `gpu_memory_utilization = 0.92`，即 torch 可用上限）。扣 **20 GB**（30K 上下文 KV cache 的上界预留）与 **12 GB**（激活 + CUDA graph + NCCL 通信缓冲），得**权重预算 $= 518.88 - 20 - 12 = 486.88 \approx 487$ GB**。

**副判据（[open_weight_model_compute.md](./open_weight_model_compute.md) §2.1 口径，用于交叉验证）**：要求 $W + \mathrm{KV}(30\mathrm{K}) \le 0.88V = 496.32$ GB。⛔ 两个判据**不是同一条**：主判据给 KV 留固定 20 GB 额度，副判据按逐模型实算 KV。本文对每个候选**同时报两个结论**；两者不一致时以更保守的为准并显式标出。

**KV@30K 的算法**：GQA 类按 $\mathrm{KV} = 2 \cdot L \cdot H_{kv} \cdot d_h \cdot 2 \cdot T$ 字节；MLA 类按 $(\mathrm{kv\_lora\_rank} + \mathrm{qk\_rope\_head\_dim}) \cdot L \cdot 2 \cdot T$。$T = 30{,}000$，FP16 KV。⛔ **这是上界**，对滑窗 / 混合注意力模型系统性高估。

⚠️ **一条必须随判据带走的反向实测**：[hardware_availability.md](./hardware_availability.md) §3.4 记录官方仓库 issue 报告 **DeepSeek-R1-W8A8 在 2×8×64 GB（1024 GB）上 OOM**，⛔ 而按本文判据它装得下。**真实常驻开销比 0.92 系数更重，本文在贴边格子上偏乐观。** 表中标 ⚠️ 贴边的格子不要据以选型。

### 1.2 装得下（$W \le 487$ GB）

⚠️ **「件的归属」一列是本表最承重的字段**，口径：**作者** = 该模型发布方自己的 HF 组织；**三方** = NVIDIA / AMD / Intel / RedHatAI / unsloth / ggml-org 等他方，⛔ **无论它多权威都不是作者**。⚠️ 一个边界情形：`AngelSlim` 是腾讯自家的压缩工具链组织，本文记为「作者旁系」并单独标注。

| 模型 | 件（HF id） | 精度 | 权重实测 | KV@30K | $W \le 487$ | $W$+KV ≤ 496.3 | 件的归属 | AA-LCR |
| :-- | :-- | :-- | ---: | ---: | :-: | :-- | :-- | ---: |
| **MiniMax M3** | [MiniMaxAI/MiniMax-M3-MXFP8](https://huggingface.co/MiniMaxAI/MiniMax-M3-MXFP8) | **MXFP8** | **443.7** | 3.7 | ✅ | ✅ 447.4 | **作者** | **80.3** |
| MiniMax M3 | [nvidia/MiniMax-M3-NVFP4](https://huggingface.co/nvidia/MiniMax-M3-NVFP4) | NVFP4 | **250.1** | 3.7 | ✅ | ✅ 253.8 | ⚠️ 三方（NVIDIA） | 80.3 ⚠️ |
| **Muse Glimmer 30B** | [meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) | BF16 | **59.6** | ⏳ | ✅ | ✅ | **作者（Meta）** | **80.0** |
| **GLM-5.2** | [nvidia/GLM-5.2-NVFP4](https://huggingface.co/nvidia/GLM-5.2-NVFP4) | **NVFP4** | **464.8** | 2.7 | ✅ | ✅ 467.5 ⚠️ 贴边 | ⛔ **三方（NVIDIA）** | **76.7** |
| **GLM-5** | [nvidia/GLM-5-NVFP4](https://huggingface.co/nvidia/GLM-5-NVFP4) | NVFP4 | **460.8** | 2.7 | ✅ | ✅ 463.5 ⚠️ 贴边 | ⛔ 三方（NVIDIA） | 70.7 |
| **MiniMax M2.7** | [MiniMaxAI/MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) | FP8（原生） | **230.1** | 7.1 | ✅ | ✅ 237.2 | **作者** | **75.3** |
| **Hy3**（腾讯） | [tencent/Hy3-FP8](https://huggingface.co/tencent/Hy3-FP8) | FP8 | **299.9** | 9.8 | ✅ | ✅ 309.7 | **作者** | **74.7** |
| Hy3 | [AngelSlim/Hy3-GPTQ-Int4](https://huggingface.co/AngelSlim/Hy3-GPTQ-Int4) | GPTQ-INT4 | **166.4** | 9.8 | ✅ | ✅ 176.2 | ⚠️ 作者旁系（腾讯 AngelSlim） | 74.7 ⚠️ |
| **Qwen3.5-397B-A17B** | [Qwen/…-FP8](https://huggingface.co/Qwen/Qwen3.5-397B-A17B-FP8) | **FP8** | **406.2** | 3.7 | ✅ | ✅ 409.9 | **作者** | **72.7** |
| Qwen3.5-397B-A17B | [Qwen/…-GPTQ-Int4](https://huggingface.co/Qwen/Qwen3.5-397B-A17B-GPTQ-Int4) | **GPTQ-INT4** | **235.7** | 3.7 | ✅ | ✅ 239.4 | **作者** | 72.7 ⚠️ |
| Qwen3.6-27B | [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) | BF16 | 55.6 | 7.3 | ✅ | ✅ | 作者 | 73.3 |
| Qwen3.5-122B-A10B | [Qwen/…-GPTQ-Int4](https://huggingface.co/Qwen/Qwen3.5-122B-A10B-GPTQ-Int4) | GPTQ-INT4 | **78.9** | ⏳ | ✅ | ✅ | 作者 | 70.3 |
| Step 3.7 Flash | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | BF16 | 402.7 | ⏳ | ✅ | ✅ | 作者 | 69.7 |
| **Inkling-Small** | [thinkingmachines/Inkling-Small-NVFP4](https://huggingface.co/thinkingmachines/Inkling-Small-NVFP4) | NVFP4 | **166.3** | ⏳ | ✅ | ✅ | **作者** | **69.3** |
| Ling 3.0 Flash | [inclusionAI/Ling-3.0-flash](https://huggingface.co/inclusionAI/Ling-3.0-flash) | BF16 | 255.0 | 1.4 | ✅ | ✅ | 作者 | 67.0 |
| **Nemotron 3 Ultra 550B** | [nvidia/…-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4) | NVFP4 | **352.3** | ⏳ | ✅ | ✅ | **作者（NVIDIA 即作者）** | **67.0** |
| GLM-4.7 | [zai-org/GLM-4.7-FP8](https://huggingface.co/zai-org/GLM-4.7-FP8) | FP8 | 354.9（+MTP 7.2） | 10.5 | ✅ | ✅ 372.6 | 作者 | 68.0 |
| GLM-4.5 | [zai-org/GLM-4.5-FP8](https://huggingface.co/zai-org/GLM-4.5-FP8) | FP8 | 361.3 | 10.5 | ✅ | ✅ 371.8 | 作者 | ⏳ |
| Mistral Large 3 675B | [mistralai/…-2512-NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) | NVFP4 | **403.1** | ⏳ | ✅ | ✅ | **作者** | ⏳ |
| Qwen3-Coder-480B | [Qwen/…-FP8](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8) | FP8 | **482.1** | 7.6 | ✅ ⚠️ 余 4.9 | ✅ 489.7 ⚠️ 极贴边 | 作者 | ⏳ |
| Qwen3-235B-A22B | [Qwen/Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B) | BF16 | 470.2 | 5.4 | ✅ ⚠️ 余 16.8 | ✅ 475.6 | 作者 | ⏳ |
| Command A+ | [CohereLabs/…-bf16](https://huggingface.co/CohereLabs/command-a-plus-05-2026-bf16) | BF16 | 437.5 | 3.7 | ✅ | ✅ 441.2 | 作者 | 48.7 |
| Llama 4 Maverick | [meta-llama/…-FP8](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8) | FP8 | 416.8 | ⏳ | ✅ | ✅ | 作者 | 50.0 |
| ⭐ **DeepSeek V4-Flash-0731** | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | **FP4+FP8（原生）** | **166.9** | 2.5 ⚠️ | ✅ ⭐ 余 320 | ✅ 169.4 | **作者** | **74.3** |
| DeepSeek V4-Flash（旧档） | [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash) | FP4+FP8（原生） | 159.6 | 2.5 ⚠️ | ✅ | ✅ | 作者 | 74.3 ⚠️ |
| ⭐ **Motif 3** | [Motif-Technologies/Motif-3-NVFP4](https://huggingface.co/Motif-Technologies/Motif-3-NVFP4) | **NVFP4** | **186.9** | ⏳ | ✅ | ✅ | **作者** | ⏳ |
| gpt-oss-120b | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | MXFP4（原生） | 65.2 | 2.1 | ✅ | ✅ | 作者 | ⛔ 51.0 |
| GLM-5.1 | [nvidia/GLM-5.1-NVFP4](https://huggingface.co/nvidia/GLM-5.1-NVFP4) | NVFP4 | **465.9** | 2.7 | ✅ | ✅ 468.6 ⚠️ 贴边 | ⛔ 三方（NVIDIA） | 68.0 |
| Inkling-Small（BF16 档） | [thinkingmachines/Inkling-Small](https://huggingface.co/thinkingmachines/Inkling-Small) | BF16 | 527.4 | ⏳ | ⛔ ❌ | ⛔ ❌ | 作者 | 69.3 |

⚠️ **AA-LCR 列标 ⚠️ 的行**：该分数是**在别的精度档测的**，⛔ 不是在这一行的精度档测的。AA 不披露每个 provider 的量化档，故**同一模型不同量化件共用一个分数是本表最大的证据缺口**——这正是 §3 要回答的问题。

### 1.3 ⛔ 装不下（$W > 487$ GB）

| 模型 | 最小可得件 | 精度 | 权重实测 | 超预算 | 归属 | AA-LCR | ⛔ 有没有更小的官方档 |
| :-- | :-- | :-- | ---: | ---: | :-- | ---: | :-- |
| ⛔ **Kimi K2.6** | [moonshotai/Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6) | **INT4 QAT（原生）** | **595.2** | **+108.2** | 作者 | **76.7** | ⛔ **无**。`moonshotai` 名下**零个独立量化仓库**，INT4 就在主仓库里。三方 [amd/Kimi-K2.6-MXFP4](https://huggingface.co/amd/Kimi-K2.6-MXFP4) 是 **559.0 GB**，⛔ 仍超 72 GB |
| ⛔ **Kimi K2.7-Code** | [moonshotai/Kimi-K2.7-Code](https://huggingface.co/moonshotai/Kimi-K2.7-Code) | INT4 QAT（原生） | **595.2** | +108.2 | 作者 | 75.0 | ⛔ 同上 |
| ⛔ **Kimi K2.5** | [moonshotai/Kimi-K2.5](https://huggingface.co/moonshotai/Kimi-K2.5) | INT4 QAT（原生） | **595.2** | +108.2 | 作者 | 73.0 | ⛔ 同上 |
| ⛔ **Inkling** | [thinkingmachines/Inkling-NVFP4](https://huggingface.co/thinkingmachines/Inkling-NVFP4) | **NVFP4** | **581.5** | +94.5 | **作者** | **73.3** | ⛔ 无。BF16 是 1894.2 GB。⚠️ 但 `Inkling-Small-NVFP4`（166.3 GB，AA-LCR 69.3）装得下 |
| ⛔ **GLM-5.2** | [zai-org/GLM-5.2-FP8](https://huggingface.co/zai-org/GLM-5.2-FP8) | FP8 | 755.6 | +268.6 | 作者 | 76.7 | ⚠️ **作者侧无 4-bit**（`zai-org` 名下唯一的 int4 仓库是 2023 年 `chatglm-6b-int4` 一类）。必须走三方 NVFP4（464.8 GB，见 §1.2） |
| ⛔ **DeepSeek V3.2** | [deepseek-ai/DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2) | FP8（原生） | **689.5** | +202.5 | 作者 | ⛔ **42.7** | ⛔ **无任何官方 4-bit**（102 个仓库穷举，命中 0） |
| ⛔ DeepSeek V3.1 / R1 | 各主仓库 | FP8（原生） | 688.6 | +201.6 | 作者 | 46.7 / 56.7 | ⛔ 同上 |
| ⛔ **DeepSeek V4-Pro** | [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | FP4+FP8（原生） | **864.7** | +377.7 | 作者 | ⏳ | ⛔ **它已经是 FP4 了**，没有更小的档 |
| ⛔ **Kimi K3** | [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | **MXFP4 QAT（原生）** | **1560.9** | **+1073.9** | 作者 | ⏳ | ⛔ **它已经是 MXFP4 了**。超预算 **3.2 倍** |
| ⛔ MiniMax M3（BF16 档） | [MiniMaxAI/MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3) | BF16 | 854.2 | +367.2 | 作者 | 80.3 | ✅ 有——MXFP8 443.7 GB（见 §1.2） |
| ⛔ Nemotron 3 Ultra（BF16 档） | [nvidia/…-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16) | BF16 | 1121.1 | +634.1 | 作者 | 67.0 | ✅ 有——NVFP4 352.3 GB |
| ⛔ Qwen3.5-397B（BF16 档） | [Qwen/Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | BF16 | 806.8 | +319.8 | 作者 | 72.7 | ✅ 有——FP8 406.2 / INT4 235.7 |
| ⛔ Mistral Large 3（FP8 档） | [mistralai/…-2512](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) | FP8 | 681.5 | +194.5 | 作者 | ⏳ | ✅ 有——NVFP4 403.1 GB |
| ⛔ **Qwen3.8-2.4T** | [Qwen/…-FP8](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8) | FP8 | **2496.1** | +2009.1 | 作者 | ⏳ | ⛔ 无 4-bit。需 ≥ 2836 GB 标称 |
| ⛔ Kimi K2-Thinking | [moonshotai/Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) | INT4 QAT（原生） | 594.2 | +107.2 | 作者 | ⏳ | ⛔ 无 |
| ⛔ Intern-S1-Pro | [internlm/Intern-S1-Pro](https://huggingface.co/internlm/Intern-S1-Pro) | FP8 | 919.0 | +432.0 | 作者 | ⏳ | ⏳ 未查 |

⛔ **本节最重要的一件事**：**AA-LCR 前八名的开放权重模型里，有三个（Kimi K2.6 76.7 · Kimi K2.7-Code 75.0 · Inkling 73.3）被显存挡在门外，且它们都已经是官方最小精度档，没有降级余地。** ⛔ 这不是「多买一张卡」能解决的差距——K2.6 需要 ≥ 681.7 GB 标称（按 §1.1 主判据反解 $(595.2+20+12)/0.92$，即 ≥ 5 张 H200），Inkling 需要 ≥ 666.8 GB（同样 ≥ 5 张）。

### 1.4 `MiniMax M3` 的补充事实（⛔ 四条会影响可用性的坑）

⚠️ **口径先摆正**：`MiniMax M3` 是本包络下 **AA-LCR（长上下文推理）** 的上限（80.3），⛔ **但不是 AA Index 总分的上限**——总分它只排第 4（45.40，见 §2.3）。⛔ **而且它带四条必须一起交付的限制**（均取自 [官方 card](https://huggingface.co/MiniMaxAI/MiniMax-M3) 与 HF 元数据，核验日 2026-08-13），⛔ 其中第 4 条可能直接否掉它：

1. ⛔ **许可证不是 Apache/MIT**：HF 元数据为 `license: other` / `license_name: minimax-community`。⛔ 不要按「开放权重即可商用」处理，需逐条读社区许可。⚠️ 对照：`Muse Glimmer 30B` 是 **Apache-2.0**、`Qwen3.5-397B` 全档是 **Apache-2.0**、`Hy3` 是 **Apache-2.0**——若许可是硬约束，首选应换成这三个之一。
2. ⚠️ **它是原生多模态模型**（`pipeline_tag: image-text-to-text`，card 逐字「MiniMax-M3 is a native multimodal model with 1M context」）。我们的负载是纯文本，⛔ 这意味着有一部分权重（vision tower / projector）在我们的用法下是常驻但不产出价值的。⚠️ MXFP8 件的 `quantization_config.ignored_layers` 明确列出 `vision_tower` / `multi_modal_projector` / `patch_merge_mlp` **不参与量化**——即这些模块仍是 BF16，是 443.7 GB 里的一部分。
3. ⚠️ **我表里的 KV@30K = 3.7 GB 是按 GQA 公式算的上界，对它系统性高估**：card 逐字「M3 is powered by MiniMax Sparse Attention (MSA)… Compared with GQA, MSA dramatically reduces the attention compute and memory footprint」。⛔ 真实 KV 更小，故余量比表里的 39.6 GB 更宽——但**本文不替官方给一个 MSA 下的实测 KV 数字**。

4. ⛔⛔ **它的 MXFP8 内核可能是 Blackwell 专属，⛔ 而 H200 是 Hopper。** SGLang 逐字：「The MXFP8 kernels are **Blackwell-only**, so **Hopper (H200) serves the full-precision bfloat16 build**」——⛔ 按该口径 H200 只能跑它的 BF16（**854.2 GB**），⛔ 而那装不下。⚠️ vLLM 侧有相反暗示但说的是 8×H200。⛔ **两源冲突，本文不裁定**，详见 §4.3。

**规格补记**（card 逐字）：「~428B parameters and ~23B activated parameters」；1M context；「9× prefill and 15× decode speedups compared to M2 at 1M context」。

## 2. 装得下者的能力定位（逐维度，非只总分）

### 2.1 ⛔ 先读：本节数字的来源与它的边界

⚠️ **本节不重新核验能力分数**，一律**引用** [benchmark_open_weights.md](./benchmark_open_weights.md) 作为主真源，按 [CLAUDE.md](../../../../CLAUDE.md) 「抄进仓库 = 建第二真源」的纪律，本文只做**按 487 GB 包络的筛选与排序**，⛔ 不新增事实断言。凡本文出现的 AA-LCR 数字，其证据级别、镜像来源与已知问题**以那份文件的 §1.1 与 §3.1 为准**。

⛔ **两条必须随本节带走的口径警告**：

1. ⛔ **AA Index 跨版本不可比**：同一个 `Qwen3.6-27B` 在 **v4.0 = 46 分、v4.1.1 = 37.70 分**，差 **8 分以上**。本节所有总分**必须带版本号**；⛔ 版本不明的数字不得参与比较。
2. ⛔ **AA-LCR 的数字依赖 thinking 开启**：关掉推理，`GLM-5.2` 从 76.7 掉到 **45**、`Qwen3.6-27B` 从 73.3 掉到 **64**、`Kimi K2.5` 从 73.0 掉到 65。⛔ **不标档位的 AA-LCR 数字没有意义**；本节默认取推理开启档。

### 2.2 AA-LCR（长上下文推理）——⭐ 对我们最承重的那个维度

**这一维度对我们最承重**（负载是 30K 上下文）。⚠️ 本小节先单独看它，⛔ 但**不要停在这里**——§2.4 会给出总分与其余七个维度，⛔ 而那里的结论方向相反。

| 侧 | 模型 | AA-LCR | 备注 |
| :-- | :-- | ---: | :-- |
| ⭐ **开放·装得下** | **MiniMax M3**（MXFP8 443.7 GB） | **80.3** | ⭐ **开放权重全场榜首** |
| 开放·装得下 | Muse Glimmer 30B（BF16 59.6 GB） | **80.0** | Apache-2.0 |
| **闭源前沿** | `Muse Spark 1.2` | **83.3** | AA-LCR 全榜榜首 |
| 闭源前沿 | `GPT-5.6 Terra` | 79.7 | OpenAI 侧最高 |
| 闭源前沿 | `GPT-5.5` | 79.0 | — |
| 闭源前沿 | `Gemini 3.1 Pro` | 79.0 | — |
| 闭源前沿 | `Claude Opus 5` | 75.7 | — |

**差距计算（AA-LCR）**：

| 对照 | 前沿 | 装得下的最强 | 绝对差 | 比值 |
| :-- | ---: | ---: | ---: | ---: |
| vs 全榜榜首 `Muse Spark 1.2` | 83.3 | **80.3** | **3.0** | **0.964** |
| vs OpenAI 最高 `GPT-5.6 Terra` | 79.7 | **80.3** | ⭐ **−0.6（反超）** | **1.008** |
| vs `Claude Opus 5` | 75.7 | **80.3** | ⭐ **−4.6（反超）** | **1.061** |
| vs `Gemini 3.1 Pro` | 79.0 | **80.3** | ⭐ **−1.3（反超）** | **1.016** |

⛔ **这一维度的结论必须谨慎表述**：**在 4×H200 装得下的模型里，长上下文推理已经不落后于前沿闭源**——它反超了 OpenAI / Anthropic / Google 三家的最高分，只落后 Meta 自家的 `Muse Spark 1.2` 3.0 分。⛔ **但这不等于「开放权重整体追上了前沿」**：[benchmark_open_weights.md](./benchmark_open_weights.md) §2.3 已记录一条不便的成因——`Muse Glimmer 30B` 的 80.0 来自用 `Muse Spark 1.2` 输出做 logit distillation（**S** 级，新闻稿），即「一家厂商把自己的前沿模型蒸馏进了 30B」。⚠️ `MiniMax M3` 的 80.3 是否有类似成因，⏳ **本轮未核**。

### 2.3 AA Index v4.1.1 总分：装得下者的完整排序

⭐ **本轮把 AA 的证据级别从 S 提到了 M。** 并行核验路绕过了 SPA 骨架问题：`artificialanalysis.ai` 的 Next.js flight payload **内嵌完整数据集**，从 [/evaluations/humanitys-last-exam](https://artificialanalysis.ai/evaluations/humanitys-last-exam)（10.6 MB）重建 99 个 chunk 后解析出 **563 模型 × 134 字段**。⭐ **这是官方站点自己的数据，不是镜像**。并做了三重验证：① 用官方 methodology 的十项权重对 **149 个 measured 模型重算总分，平均绝对误差 0.12 分、最大 0.76 分**；② 最小二乘反解权重得 `.203/.136/.160/.079/.059/.123/.059/.067/.082/.041`，与官方 `.20/.14/.16/.08/.06/.12/.06/.06/.08/.04` 逐项吻合（和 1.0089）——⭐ **这同时证明了数据集版本确实是 v4.1.1**；③ 与真镜像 [ctrlaltdebrief](https://ctrlaltdebrief.com/tools/benchmarks/intelligence_index) 的 22 个重叠模型**逐值一致、零数值冲突**。

⛔ **五个待核参考点全部证实**：`Opus 5 (max)` 63.05 → 63.1 ✅ · `GPT-5.6 Sol (max)` 60.93 → 60.9 ✅ · `Fable 5` 62.07 → 62.1 ✅ · `Kimi K3 (max)` 59.70 ✅ · `Qwen3.6-27B` 37.70 ✅。

**⭐ 装得下（$W \le 487$ GB）的模型，按 v4.1.1 总分降序**（全部 **M** 级）：

| # | 模型 | v4.1.1 总分 | 可用件与体积 | 件的归属 | 许可 | ⚠️ |
| --: | :-- | ---: | :-- | :-- | :-- | :-- |
| 1 | **GLM-5.2** | ⭐ **52.64** | nvidia NVFP4 **464.8** | ⛔ **三方** | MIT | ⛔ 三方件 + 贴边（467.5/496.3） |
| 2 | **DeepSeek V4-Flash-0731** | ⭐ **51.77** | 原生 FP4+FP8 **166.9** | ✅ **作者** | **MIT** | ⭐ **余量 320 GB** |
| 3 | **Motif 3** | **47.4** | 作者 NVFP4 **186.9** | ✅ **作者** | **MIT** | ⭐ 纯文本（非多模态） |
| 4 | **MiniMax M3** | **45.40** | 作者 MXFP8 **443.7** | ✅ 作者 | ⛔ 自定义 | ⚠️ 多模态 |
| 5 | Hy3（腾讯） | 42.21 | 作者 FP8 **299.9** | ✅ 作者 | Apache-2.0 | — |
| 6 | GLM-5.1 | 40.97 | nvidia NVFP4 **465.9** | ⛔ 三方 | MIT | ⛔ 贴边 |
| 7 | GLM-5 | 40.55 | nvidia NVFP4 **460.8** | ⛔ 三方 | MIT | ⛔ **AA 估算值** |
| 8 | MiniMax M2.7 | 38.87 | 原生 FP8 **230.1** | ✅ 作者 | ⛔ 自定义 | — |
| 9 | Nemotron 3 Ultra 550B | 38.32 | 作者 NVFP4 **352.3** | ✅ 作者 | ⛔ OpenMDW | — |
| 10 | Ling 3.0 Flash | 37.82 | BF16 **255.0** | ✅ 作者 | MIT | — |
| 11 | Qwen3.6-27B | 37.70 | BF16 **55.6** | ✅ 作者 | Apache-2.0 | ⭐ 最小 |
| 12 | Muse Glimmer 30B | 35.06 | BF16 **59.6** | ✅ 作者 | Apache-2.0 | — |
| 13 | GLM-4.7 | 34.46 | 作者 FP8 **354.9** | ✅ 作者 | MIT | — |
| 14 | Qwen3.5-397B-A17B | 34.26 | 作者 FP8 **406.2** / INT4 **235.7** | ✅ 作者 | Apache-2.0 | — |
| 15 | Qwen3.5-122B-A10B | 32.85 | 作者 INT4 **78.9** | ✅ 作者 | Apache-2.0 | — |
| 16 | Step 3.7 Flash | 30.90 | BF16 **402.7** | ✅ 作者 | Apache-2.0 | — |
| 17 | Mistral Medium 3.5 | 30.39 | 原生 FP8 **133.6** | ✅ 作者 | ⛔ 自定义 | — |
| 18 | gpt-oss-120b | 24.13 | 原生 MXFP4 **65.2** | ✅ 作者 | Apache-2.0 | — |
| 19 | Command A+ | 22.77 | BF16 **437.5** | ✅ 作者 | Apache-2.0 | — |
| 20 | Mistral Large 3 675B | 15.92 | 作者 NVFP4 **403.1** | ✅ 作者 | Apache-2.0 | ⛔ 分数极低 |
| 21 | Llama 4 Maverick | 14.48 | 作者 FP8 **416.8** | ✅ 作者 | ⛔ 社区许可 | ⛔ 分数极低 |

**⛔ 装不下的高分模型**（说明「差距不是钱能补的那部分」）：

| 模型 | v4.1.1 总分 | 最小件 | 超预算 | ⚠️ |
| :-- | ---: | ---: | ---: | :-- |
| ⛔ **Kimi K3 (max)** | **59.70** | 1560.9（原生 MXFP4） | +1073.9 | ⛔ 开放权重全场第一，⛔ 但需 ≥ 1774 GB |
| ⛔ **DeepSeek V4-Pro** | **53.00** | 864.7（原生 FP4+FP8） | +377.7 | ⛔ 已是 FP4，无更小档 |
| ⛔ Kimi K2.6 | 45.14 | 595.2 | +108.2 | ⛔ 已是 INT4 QAT |
| ⛔ Kimi K2.7 Code | 43.02 | 595.2 | +108.2 | ⛔ 同上 |
| ⛔ Inkling | 42.29 | 581.5（作者 NVFP4） | +94.5 | ⚠️ 但 `Inkling-Small` 41.2 装得下（166.3 GB） |
| ⛔ Kimi K2.5 | 36.02 | 595.2 | +108.2 | — |
| ⛔ Kimi K2 Thinking | 33.49 | 594.2 | +107.2 | ⛔ AA 估算值 |
| ⛔ DeepSeek V3.2 | 32.80 | 689.5 | +202.5 | ⛔ AA 估算值。⛔ **分数低于一堆装得下的模型** |

⛔ **两个「看起来开放其实不是」的高分模型**：`Qwen3.8 Max` **58.08** 与 `Muse Spark 1.2` **56.76** 在 AA 的元数据里 `is_open_weights = False`。⚠️ 注意 `Qwen3.8 Max`（hosted-only）与 HF 上的 `Qwen/Qwen3.8-2.4T-A95B`（开放权重、自定义许可、2496.1 GB）**不是同一个东西**，⛔ 不要混。

⛔ **四个模型的总分是 AA 估算值，不是实测**：`GLM-5`（40.55）· `Kimi K2 Thinking`（33.49）· `DeepSeek V3.2`（32.80）· `DeepSeek V3.2-Speciale`（22.61）。它们的三个 agentic 成分（τ³-Banking / Terminal-Bench v2.1 / GDPval）**全为空**，⛔ 而这占 v4.1.1 权重的 **50%**。⛔ **不可与 measured 模型同精度比较。**

### 2.4 ⭐ 与前沿闭源的差距（总分 + 逐维度）

**闭源锚点（v4.1.1，max effort 档，M 级）**：`Claude Opus 5 (max)` **63.05** · `Claude Fable 5` **62.07** · `GPT-5.6 Sol (max)` **60.93** · `GPT-5.6 Terra (max)` **56.58** · `Gemini 3.1 Pro Preview` **47.74**。⛔ 注意 `GPT-5.6 Terra (max)` 是 **56.58**，⛔ 不要与 `Sol` 的 60.93 混。

**总分差距**：

| 对照 | 前沿 | 装得下的最强 | 绝对差 | 比值 |
| :-- | ---: | ---: | ---: | ---: |
| vs `Claude Opus 5 (max)`，⛔ 不限件的归属 | 63.05 | **GLM-5.2 52.64** | **10.41** | **0.835** |
| vs `Claude Opus 5 (max)`，⭐ **只认作者件** | 63.05 | **DeepSeek V4-Flash-0731 51.77** | **11.28** | **0.821** |
| vs `GPT-5.6 Sol (max)` | 60.93 | GLM-5.2 52.64 | 8.29 | 0.864 |
| vs `Gemini 3.1 Pro Preview` | 47.74 | GLM-5.2 52.64 | ⭐ **−4.90（反超）** | **1.103** |
| ⚠️ 参照：**≤32B 档**（旧包络） | 63.05 | Qwen3.6-27B 37.70 | ⛔ **25.35** | ⛔ **0.598** |

⭐ **这是本文对 story 最有用的一个数字**：把包络从 ≤32B 放到 4×H200，**总分差距从 25.35 分（比值 0.598）收到 10.41 分（比值 0.835）**——⛔ 但**没有消除**。

**⭐ 逐维度差距（vs `Claude Opus 5 (max)`）**：

| 维度 | 权重 | Opus 5 (max) | **GLM-5.2** | 差 / 比值 | **DeepSeek V4-Flash** | 差 / 比值 | **MiniMax M3** |
| :-- | ---: | ---: | ---: | :-- | ---: | :-- | ---: |
| **总分 v4.1.1** | 100% | **63.05** | **52.64** | 10.41 / **0.835** | **51.77** | 11.28 / **0.821** | 45.40 |
| ⭐ **AA-LCR**（长文档推理） | 6% | 75.7 | **76.7** | ⭐ **−1.0 / 1.013** | 74.3 | 1.4 / **0.982** | ⭐ **80.3**（−4.6 / **1.061**） |
| ⛔ **AA-Omni 净分**（幻觉） | 12% | **+37.1** | **+4.4** | ⛔ **32.7 / 0.119** | ⛔ **−14.3** | ⛔ **51.4 / 符号相反** | +1.4 |
| **HLE** | 12% | 54.9 | 41.1 | 13.8 / 0.749 | 38.6 | 16.3 / 0.703 | 39.0 |
| **GPQA Diamond** | 6% | 93.2 | 89.5 | 3.7 / **0.960** | 90.8 | 2.4 / **0.974** | 92.9 |
| **CritPt** | 6% | 29.1 | 20.9 | 8.2 / 0.718 | 16.6 | 12.5 / 0.570 | ⛔ 3.7 |
| **SciCode** | 8% | 55.7 | 50.5 | 5.2 / 0.907 | 49.2 | 6.5 / 0.883 | 45.4 |
| **Terminal-Bench v2.1**（工具） | 16% | 89.1 | 77.9 | 11.2 / 0.874 | 78.7 | 10.4 / 0.883 | ⛔ 65.2 |
| **τ³-Banking**（工具） | 14% | 42.1 | 34.6 | 7.5 / 0.822 | 39.4 | ⭐ 2.7 / **0.936** | ⛔ 15.3 |
| **GDPval-AA v2**（Elo） | 20% | 1848.8 | 1506.1 | 342.7 / 0.815 | 1558.4 | 290.4 / 0.843 | 1388.6 |
| ⛔ **IFBench** | ⛔ **0%** | ⛔ **未跑** | 73.3 † | ⛔ **不可比** | ⛔ 未跑 | ⛔ 不可比 | 82.9 † |

⛔⛔ **两条必须一起交付的结论**：

1. ⭐ **在我们最承重的 AA-LCR 上，装得下的模型已经不落后于前沿**：`GLM-5.2` **反超** Opus 5 **1.0 分**、`MiniMax M3` **反超 4.6 分**、`DeepSeek V4-Flash` 只差 **1.4 分**（比值 0.982）。
2. ⛔⛔ **但幻觉维度是灾难性的，且它的权重是 AA-LCR 的两倍。** Opus 5 的 AA-Omniscience 净分是 **+37.1**，而装得下的最强模型 `GLM-5.2` 只有 **+4.4**（比值 **0.119**），`DeepSeek V4-Flash` 是 **−14.3**——⛔ **符号都是反的**。⭐ 这一维度直接对应我们的核心失败模式（判定器凭空报出不存在的缺陷），⛔ **它是本包络下最该担心的事，不是总分。**

⭐ **一个此前不知道的结构性事实：487 GB 包络跨过了幻觉的符号边界。** ⛔ 在 ≤32B 档，AA-Omniscience 净分**全部为负**。而在本包络内，**`GLM-5.2` +4.4 · `MiniMax M3` +1.4 · `GLM-5.1` +0.8 · `MiniMax M2.7` +0.8 · `GLM-5` +0.3 转正**，⛔ 而 `DeepSeek V4-Flash` −14.3 · `Hy3` −18.5 · `Qwen3.5-397B` −30.8 · `Muse Glimmer 30B` −32.9 **仍为负**。⭐ **即包络内同时存在符号两侧的模型，选谁在这个维度上差 50 分以上。** ⛔ 这条使「按总分挑最强」成为**错误的挑法**——`DeepSeek V4-Flash` 总分第 2 但幻觉为负，`GLM-5.2` 总分第 1 且幻觉为正。

⛔ **一条对任务前提的硬性更正：IFBench 这个维度问不了。** IFBench 已在 **v4.1 因饱和被移出 Index**，⛔ 它**不是 v4.1.1 的成分**（权重 0%）。实测覆盖边界：**447 个模型有 IFBench 分，最新发布日恰为 2026-07-09**，其后发布的模型一律为空——⛔ **`Claude Opus 5` / `Kimi K3` / `Qwen3.8 Max` / `DeepSeek V4` 全系都没有 IFBench 分**。⛔ 表中 † 标记的值属 **v4.0 时代测量**，与 v4.1.1 无版本对应关系，⛔ **不得与任何 v4.1.1 数字混比**。⚠️ 这不是取数失败，是**评测已退役**。

⛔ **一条比「跨版本不可比」更细的警告**：v4.1 → v4.1.1 **只换了 grader、没动成分与权重**（官方 changelog 逐字「contributing evaluations and their weights are unchanged from v4.1」），但 **HLE / AA-LCR / AA-Omniscience 三项的 grader 统一换成 `GPT-5.6 Luna (medium)`**（分别替换 GPT-4o (Aug '24) / Qwen3 235B A22B 2507 Non-Reasoning / Gemini 3 Flash Preview）。⛔ **所以即便 v4.1 与 v4.1.1 之间，这三项也不严格可比。**

### 2.5 ⛔ 一条贯穿全表的结构性提醒

AA Index v4.1.1 的类别权重是 **Agents 34% + Coding 24% + Scientific Reasoning 24% + General 18%**，其中 **AA-LCR 只占 6%**、而 **GDPval-AA v2 一项就占 20%**（**M**，官方 methodology）。⛔ **所以总分差距的大头落在我们的流水线根本不执行的能力上**（不用工具、不跑终端、不写补丁——⭐ 九个成分里**只有 GDPval 与 τ³-Banking 两项允许用工具**，合计 34%）。⭐ **报告总分差距时必须同时报逐维度差距，否则是失真的**——⛔ 反向亦然：只报 AA-LCR 的反超而不报幻觉维度的 0.119，同样是失真，⛔ **而且是更危险的那一种失真**。

## 3. 量化退化证据

### 3.0 ⭐ 一句话答案

⭐ **4-bit 权重量化不会吃掉大模型的能力，这个判断有足够证据支撑（12 个模型、48 个跨档对照，其中 20 个来自模型作者一手）：671B+ 级上掉分 0–3%，且规模越大越鲁棒。** ⛔ **但真正的雷不是权重量化，是 KV cache 量化**——`W4KV8` 基本无损而 `W8KV4` 掉 **20 点以上**。⛔⛔ **而我们承重的「结构化输出」维度在公开文献里没有任何一条对口数据**，见 §3.4。

### 3.1 权重量化的实测掉分（⛔ 只列作者一手，M 级）

⭐ **直接命中长上下文的一条**：**`Hy3` 的作者旁系件 [AngelSlim/Hy3-GPTQ-Int4](https://huggingface.co/AngelSlim/Hy3-GPTQ-Int4) 给出了 BF16 vs GPTQ-Int4 在 AA_LCR 上的对照：73.4 → 71.6，掉 1.80 分（−2.45%）。** ⭐ 这是本轮找到的**唯一一条作者侧公布的「4-bit × 长上下文」对照**。

| 模型 | 规模 | BF16 | 4-bit | benchmark | 掉分 |
| :-- | :-- | ---: | ---: | :-- | ---: |
| ⭐ **Hy3** | 295B | **73.4** | GPTQ-Int4 **71.6** | ⭐ **AA_LCR（长上下文）** | **−1.80（−2.45%）** |
| Hy3 | 295B | 79.1 | 77.2 | mcp_atlas（工具调用） | −1.90（−2.40%） |
| Hy3 | 295B | 78.0 | 77.0 | SWE-bench Verified | −1.00 |
| Hy3 | 295B | 57.9 | ⛔ 54.7 | swe-pro | ⛔ −3.20（−5.53%） |
| Hy3 | 295B | 57.9 | ⭐ **58.6** | nl2repo | ⭐ **+0.70（反向）** |
| ⭐ **Nemotron 3 Ultra** | 550B | **65.4** | NVFP4 **65.5** | ⭐ **AA-LCR** | ⭐ **+0.10** |
| Nemotron 3 Ultra | 550B | 94.7 | 94.0 | ⭐ **RULER 1M** | −0.70（−0.74%） |
| Nemotron 3 Ultra | 550B | 44.4 | ⛔ 41.4 | BrowseComp | ⛔ −3.00（−6.76%） |
| Ling-3.0-flash | 124B/5.1B | 74.49 | INT4 72.20 | IFBench | −2.29（−3.07%） |
| Ling-3.0-flash | 124B/5.1B | 84.97 | INT4 83.65 | GPQA-d | −1.32 |
| Ling-3.0-flash | 124B/5.1B | 84.97 | ⛔ **FP4** 82.42 | GPQA-d | ⛔ −2.55（**FP4 比 INT4 更差**） |
| ⛔ Ring-mini-linear-2.0 | 16.4B/**1.6B** | 73.65 | GPTQ-Int4 ⛔ 66.56 | AIME25 | ⛔ **−7.09（−9.63%）** |

⭐ **按模型聚合的规模效应（S 级趋势，⛔ 不是定律——不同模型用的量化方法不同）**：

| 模型 | 激活规模 | n | 均值掉分 | 最差 |
| :-- | :-- | --: | ---: | ---: |
| ⛔ Ring-mini-linear-2.0 | **1.6B** | 4 | ⛔ **−6.53%** | −9.63% |
| Ring-flash-linear-2.0 | 6.1B | 3 | −3.14% | −5.27% |
| Ling-3.0-flash | 5.1B | 4 | −2.74% | −4.58% |
| ⭐ **Hy3** | **295B 总参** | 7 | **−1.95%** | −5.53% |
| ⭐ **Nemotron 3 Ultra** | **550B 总参** | 5 | ⭐ **−1.49%** | −6.76% |

⭐ **我们要装的正是 400B+ 级，落在最鲁棒的一端。**

⚠️ **`Nemotron 3 Ultra` 那一组偏乐观必须注明**：其 card 逐字说该模型「pre-trained using an **NVFP4 recipe**」——⛔ **NVFP4 是它的主场**，不代表把一个 BF16 训出来的模型压到 4-bit。

⚠️ **NVIDIA 的 FP8→NVFP4 对照（n=14，均值 −0.10%，最差 −1.33%）在噪声级**，⛔ 但**口径要注意**：这批的基线绝大多数是 **FP8 而非 BF16**，⛔ 所以「FP8→NVFP4 几乎无损」**不等于**「BF16→NVFP4 几乎无损」——BF16→FP8 那一段的损失被排除在计算之外了。⭐ 唯一用**真 BF16 基线**的是 `nvidia/Qwen3.6-35B-A3B-NVFP4`（n=4，均值 **−0.18%**，AA-LCR **0.00**）。

### 3.2 ⭐ 长上下文：30K 落在安全带内

⭐ **最直接命中我们 30K 负载的一条（M 级，一手 + 开源可复现）**：[Red Hat / Neural Magic 的 RULER 4K–128K 研究](https://developers.redhat.com/articles/2024/02/03/how-well-do-quantized-models-handle-long-context-tasks)（Kurtić / Kurtz / Marques / Alistarh，末次更新 2025-09-23）逐字：

> 「INT W4A16 …**>99.5% accuracy recovery**」（4K–64K 区间）；128K 处才掉到「**85% (8B) and 88% (70B)**」

⭐ **30K 落在 >99.5% 的那一段。** ⚠️ 且作者自己指出 128K 处「even unquantized models perform poorly (average scores below 65 for both sizes)」，故那里的 recovery「becomes inherently **noisy**」。

⛔ **但有一条方向相反的学术反证，必须一起看**：[arXiv:2505.20276](https://arxiv.org/abs/2505.20276)（EMNLP 2025 main，9.7K 样本 × 5 模型 × 5 量化档）给出全任务平均 Δ：FP8 **−0.2%** · GPTQ-int8 −0.8% · AWQ-int4 −1.8% · GPTQ-int4 **−2.7%** · ⛔ BNB-nf4 **−6.9%**；⛔ 而在 **RULER（64K+128K 聚合）** 上 GPTQ-int4 让 Llama-3.1-8B 掉 **−21.2%**、Qwen-2.5-72B 掉 **−10.3%**（⭐ 又一次规模效应）。

⭐ **两者在「8-bit 无损、4K–8K 无损」上完全一致**（该论文明确写 4-bit 在 128K 处平均掉 23%，而 **8K 处所有量化档与 BF16 相当**）；⛔ 分歧只在 64K–128K 的量级，⛔ **本文不消解该分歧，如实登记。** ⚠️ 另注意该论文摘要里那个 **−59%** 的数字出处是 OneRuler + Llama-3.1-70B + BNB-nf4，⛔ 且**同一配置在其 Appendix C.2 里写的是 66%**——⛔ 论文内部不一致。

⚠️ **一个会让人把 context rot 记在量化头上的方法学陷阱**（[arXiv:2509.14391 Q-ROAR](https://arxiv.org/abs/2509.14391)）：同一篇里结论随指标翻转——GovReport 困惑度 gap 从 2048 处 +0.107 扩到 32768 处 +0.644（支持「长上下文更严重」），⛔ 但 5-shot 准确率 gap 从 4K 的 6.69 分**缩小到** 32K 的 0.39 分，⛔ 原因是 **FP16 自己从 70.83 掉到 63.71**、塌向了量化模型。⭐ **故任何「长上下文量化退化更严重」的主张，必须说明是绝对差、相对差，还是扣除全精度基线自身塌陷后的净差。**

### 3.3 ⛔⛔ 真正的雷：KV cache 量化，不是权重量化

⭐ **这是本轮最重要的发现，且它改变了风险的落点。** [arXiv:2402.18158](https://arxiv.org/abs/2402.18158)（清华 NICS，11 个模型族，125M–180B）§7 三条逐字分野：

1. **权重量化**：「Long texts (≥4k) are more sensitive to Weight-only and KV Cache Quantization than short texts (<4k)」
2. **权重-激活量化**：⛔ **相反**——长文本上**没有**额外退化
3. **KV cache 量化**：⛔ 长上下文上**最脆弱**，同 bit width 下明显低于权重量化

其 Appendix B.3 Table 7（LongEval 16K）：

| 模型 | FP16 | W8KV8 | ⭐ W4KV8 | ⛔ **W8KV4** |
| :-- | ---: | ---: | ---: | ---: |
| Vicuna-7B | 57.80 | 56.40 | ⭐ **59.60** | ⛔ **37.00** |
| Vicuna-13B | 41.60 | 40.80 | 36.40 | ⛔ **29.00** |

⭐⭐ **`W4KV8` 基本无损（甚至 +1.8），⛔ 而 `W8KV4` 掉 20 点以上。位宽花在哪里，比花多少更重要。** ⭐ **对我们的直接含义：权重可以压到 4-bit，⛔ 但 KV cache 必须留在 8-bit 或以上。**

⛔ **一条同向但更悲观、且与厂商数据冲突的单篇证据**（[arXiv:2606.09864](https://arxiv.org/pdf/2606.09864) Table 22，Qwen-2.5-7B-Instruct，IFEval N=541）：KV 量到 **8-bit** 就让 `Pass_strict` 从 69.50 掉到 **59.89**（−9.6 点），约 **1/4** 原本通过的 prompt 违反约束（`CondFlip` 23.14）；6-bit 直接塌到 **16.82%**。⛔ **限定必须写满**：单篇 preprint、**未被独立复现**、塌陷阈值**高度 model-specific**（Mistral-7B 在 4-bit KV 只 15.2% flip，Gemma-2-9B 撑到 3-bit）。⛔⛔ **且它与 NVIDIA 在 FP8 KV 下测出的 IFBench/τ² 全部正常直接冲突——「8-bit KV 是否安全」目前两边矛盾，⛔ 本文不裁定。**

⚠️ **一条必须随 §3.1 那些漂亮 AA-LCR 数字带走的推断（I 级，⛔ 未实测确认）**：NVIDIA 的部署示例普遍带 `--kv-cache-dtype fp8`（在 GLM-5.2 / DeepSeek-V4-Pro / Qwen3.6-35B / Qwen3.5-122B / Nemotron 的命令里均可验证），即**权重 4-bit + KV 8-bit**——正是上表里「基本无损」的那个组合。⛔ 但各 card **未明确写出评测时用的 KV 精度**，⛔ 故这是推断不是事实。

### 3.4 ⛔⛔ 结构化输出：这个维度没有任何对口数据

⛔⛔ **没有任何一篇论文或厂商报告，把「JSON schema 合规率」或「tool-call 结构合法率」当作因变量、把量化档位当作自变量。** ⚠️ 这是经定向检索确认的**真实空白**，⛔ 不是没搜到。

⛔ **且 IFEval / IFBench 不是它的合法代理**，三条理由：① **测的不是同一件事**——IFEval 测「输出满不满足自然语言里说的格式约束」，schema 合规是「能不能被校验器通过」，⛔ 后者在约束解码下几乎恒为 100%；② **IFEval 已饱和**——[llm-quant-bench](https://github.com/yrougy/llm-quant-bench) 明确因为「9B+ 模型贴天花板，量化差异淹没在噪声里」而**弃用 IFEval**，⛔ 故「IFEval 没掉」很可能是**测不出来**而非没退化；③ **机制上合法性被搬出了模型侧**——vLLM structured outputs / XGrammar / Outlines 在 logits 上做 mask，⛔ 权重精度不参与语法状态机，量化只影响**字段语义正确性**。⛔ **但这第 ③ 条是机制推论，⛔ 没有任何研究做过「量化档位 × 是否开约束解码」的 2×N 对照。**

⛔ **两条看起来很吓人但不能用的数字**（⛔ 不要引用）：① [arXiv:2411.15399](https://arxiv.org/abs/2411.15399) 报 Llama3.1-8b BFCL **63.04% → q4_0 20.43%**——⛔ **全精度跑 HF transformers、量化跑 llama.cpp GGUF，框架 / chat template / tool-call parser 全不同**，而 BFCL 是 AST 匹配、对输出外壳极度敏感（其 q8_0 也掉 18.7 点，⛔ 与所有其他文献矛盾）。② llm-quant-bench 报 Qwen3.5-9B BFCL −17.9pp——⛔ 实测只 **250 样本**（95% CI ≈ ±5.9pp），4 个模型里 1 个反向，⛔ 且**所有档位都开 q4_0 KV cache**（正是 §3.3 的致命混淆）。⭐ 该库真正的结论是：**只有跌破 3-bit（IQ2/IQ1）才出现 10–18 点塌陷，Q4–Q8 区间基本不掉。**

⭐ **最大规模一手数据的结论是「指令遵循和知识类一样」**（[arXiv:2411.02355](https://arxiv.org/html/2411.02355v3)，Neural Magic/RedHat，50 万+ 次评测，ACL 2025）：Llama-3.1-8B W4A16 逐项 recovery —— **IFEval 98.00%** vs MMLU 5-shot **97.95%**，⭐ 几乎一模一样；掉得最狠的是 MuSR（83.18%）与 MMLU-Pro（93.63%）。⛔ **但有一篇结论相反**：[arXiv:2409.11055](https://arxiv.org/html/2409.11055v1) 测同一个 Llama-3.1-8B 4-bit，IFEval 50.09 → GPTQ **44.81（−5.28）**，⛔ 掉幅约为 MMLU 的两倍。⛔ **同一模型同一档位，一手说 −1.5、第三方说 −5.28，⛔ 任何单点引用都能被另一篇反驳。**

### 3.5 ⭐ 对本包络的收敛结论

⛔ **本包络的首选配置不需要 4-bit**：`DeepSeek V4-Flash-0731` 是**原生混合精度**（166.9 GB）、`Hy3` 走**官方 FP8**（299.9 GB）、`MiniMax M2.7` 走**原生 FP8**（230.1 GB）、`Qwen3.5-397B` 走**官方 FP8**（406.2 GB）。⭐ **而 FP8 这一档在全部证据里都是最安全的**：arXiv:2505.20276 给的全任务平均 Δ 是 **−0.2%**。

⛔ 4-bit 退化风险**只对下面这些「非 4-bit 装不下」的候选适用**：

| 候选 | 为什么必须 4-bit | 4-bit 件 | 归属 | ⚠️ 风险 |
| :-- | :-- | :-- | :-- | :-- |
| **GLM-5.2**（AA-LCR 76.7） | 官方 FP8 是 755.6 GB，超预算 268.6 | [nvidia/GLM-5.2-NVFP4](https://huggingface.co/nvidia/GLM-5.2-NVFP4) 464.8 GB | ⛔ **三方** | ⛔ 双重风险：既是 4-bit，又是非作者件，⛔ 且 467.5 GB 贴边 |
| **GLM-5**（AA-LCR 70.7） | 同上 | [nvidia/GLM-5-NVFP4](https://huggingface.co/nvidia/GLM-5-NVFP4) 460.8 GB | ⛔ 三方 | ⛔ 同上 |
| Mistral Large 3 675B | 官方 FP8 是 681.5 GB | [mistralai/…-NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) 403.1 GB | **作者** | ⚠️ 是 4-bit，但**作者件**，且官方 card 明确背书 NVFP4 用法 |

### 3.6 ⭐⭐ 一条决定性的否定结论：对已经是 4-bit 的模型，再量化一次也不缩小

⛔ **本轮追查了 NVIDIA 对那几个「装不下的高分模型」的 NVFP4 件，结果是它们一点没变小**——⭐ 这使 §1.3 的「装不下」判定**在全部已知量化路径上都成立**，⛔ 不是「没找够件」造成的假象：

| 模型 | 原生件 | NVIDIA NVFP4 件 | 变化 | 结论 |
| :-- | ---: | ---: | :-- | :-- |
| ⛔ **Kimi K2.6**（总分 45.14） | 595.2（INT4 QAT） | [nvidia/Kimi-K2.6-NVFP4](https://huggingface.co/nvidia/Kimi-K2.6-NVFP4) **595.2** | ⛔ **完全相同** | ⛔ 仍超预算 108.2 |
| ⛔ **Kimi K2.7-Code**（43.02） | 595.2（INT4 QAT） | [nvidia/…-NVFP4](https://huggingface.co/nvidia/Kimi-K2.7-Code-NVFP4) **595.2** | ⛔ 完全相同 | ⛔ 仍超 108.2 |
| ⛔⛔ **DeepSeek V4-Pro**（**53.00**） | 864.7（FP4+FP8） | [nvidia/DeepSeek-V4-Pro-NVFP4](https://huggingface.co/nvidia/DeepSeek-V4-Pro-NVFP4) ⛔ **913.1** | ⛔⛔ **反而大了 48.4 GB** | ⛔ 仍超 426.1 |
| ⚠️ Qwen3.5-397B-A17B（34.26） | 806.8（BF16） | [nvidia/…-NVFP4](https://huggingface.co/nvidia/Qwen3.5-397B-A17B-NVFP4) **251.2** | ✅ 缩到 31% | ✅ 装得下（⛔ 但作者 FP8 406.2 也装得下，不必用三方件） |

⭐⭐ **`DeepSeek V4-Pro` 那一行是本表最有说服力的一条：把一个已经是 FP4 的模型再走一遍 NVFP4 流程，权重反而涨了 48.4 GB**（因为 scale / 元数据开销叠加，且部分层被留在更高精度）。⛔ **这证明「再压一压就装下了」对已经原生 4-bit 的模型是无效的想法。**

⚠️ **一条方法论提醒**：本文 §1 表里凡 AA-LCR 标 ⚠️ 的行，都是**拿高精度档的分数标在低精度档的件上**。⛔ AA 不披露每个 provider 的量化档，所以「`nvidia/GLM-5.2-NVFP4` 的 AA-LCR 是 76.7」这句话**严格说没有证据**——76.7 是「GLM-5.2」这个模型名的分数，⛔ 不是那个 NVFP4 件的分数。⭐ **这是本文最大的单一证据缺口。** ⚠️ 不过 §3.1 已给出**同向的量级估计**：NVIDIA 自己测的 `GLM-5.2` FP8→NVFP4 在 AA-LCR 上是 **69.38 → 70.13（+0.75）**，⛔ 即该件相对其 FP8 基线**没有掉**（⛔ 但注意 69.38 这个 FP8 基线本身与 AA 官方口径的 76.7 不同源，⛔ 两套数字不可交叉相减）。

## 4. 工程可行性（专家并行 / 互联 / 官方实例）

### 4.1 ✅ 官方明确点名「4×H200」的实例（⭐ 本轮亲自逐字核验）

⭐ **`zai-org/GLM-4.5` 的 model card 里有一张官方硬件表，明确写着 4×H200 可跑 GLM-4.5 FP8。** 本轮直接取 card 原文（`curl -s https://huggingface.co/zai-org/GLM-4.5/raw/main/README.md`，9670 字节）逐行核验，逐字如下（**M** 级，一手）：

表一，前置说明逐字「We provide **minimum and recommended configurations** for "full-featured" model inference」：

| Model | Precision | GPU Type and Count | Test Framework |
| :-- | :-- | :-- | :-- |
| GLM-4.5 | BF16 | `H100 x 16 / H200 x 8` | sglang |
| **GLM-4.5** | **FP8** | ⭐ **`H100 x 8 / H200 x 4`** | sglang |
| GLM-4.5-Air | BF16 | `H100 x 4 / H200 x 2` | sglang |
| GLM-4.5-Air | FP8 | `H100 x 2 / H200 x 1` | sglang |

⛔ **但必须连同表二一起读，否则会过度乐观**。表二的前置说明逐字「Under the configurations in the table below, the models can utilize their **full 128K context length**」：

| Model | Precision | GPU Type and Count | Test Framework |
| :-- | :-- | :-- | :-- |
| GLM-4.5 | BF16 | `H100 x 32 / H200 x 16` | sglang |
| **GLM-4.5** | **FP8** | ⛔ **`H100 x 16 / H200 x 8`** | sglang |
| GLM-4.5-Air | BF16 | `H100 x 8 / H200 x 4` | sglang |
| GLM-4.5-Air | FP8 | `H100 x 4 / H200 x 2` | sglang |

⭐ **所以官方的准确说法是：4×H200 能跑 GLM-4.5 FP8（权重 361.3 GB），但跑不到它的满 128K 上下文——满上下文要 8×H200。** ⚠️ **这条对我们是好消息**：我们的负载是 **30K**，远低于 128K，落在表一那一档。⛔ 但它同时说明**「装得下」与「满上下文可用」是两件事**，本文 §1 的所有 ✅ 都只声明 30K 档。

**表一同时列出的四条前置条件（逐字，⛔ 缺一条结论就不成立）**：

1. 「All models use MTP layers and specify `--speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4`」
2. 「The `cpu-offload` parameter is **not** used.」
3. ⚠️ 「Inference **batch size does not exceed 8**.」
4. 「All are executed on devices that **natively support FP8 inference**, ensuring both weights and cache are in FP8 format.」
5. ⚠️ 「**Server memory must exceed `1T`**」——⛔ 这是**主机内存**，不是显存。4×H200 的机器若只有 512 GB 内存，⛔ 按官方口径连加载都不保证。

⚠️ ⭐ **一条本轮新发现的、必须写进判据的事实：KV 随 batch 线性放大，而本文 §1 的 KV@30K 全部是 batch = 1。** 主 session 给的 20 GB KV 额度，对 `MiniMax M3`（batch=1 时 3.7 GB）意味着 **batch 上限约 5**；对 `Hy3`（9.8 GB）意味着 **batch 约 2**。⛔ **不要把 §1 的 ✅ 读成「能以任意并发跑」。**

⛔ **一条同向的官方警告，说明贴边格子确实会炸**：同一份 card 逐字「If you're using **8x H100 GPUs** and encounter **insufficient memory** when running the GLM-4.5 model, you'll need `--cpu-offload-gb 16` (only applicable to vLLM).」——**8×H100 = 640 GB、权重只有 361.3 GB，官方仍预告了会不够用**。⛔ 这与 [hardware_availability.md](./hardware_availability.md) §3.4 那条 DeepSeek-R1-W8A8 在 1024 GB 上 OOM 的记录同向：⛔ **静态容量核算系统性偏乐观。**

### 4.2 ⭐ 其它官方点名 4×H200 的实例（框架侧 recipe）

⭐ **除 GLM-4.5 外，另有两条官方 4×H200 记录，且其中一条正好命中 400+ GB 区间**：

| 模型 | 精度 | 官方逐字 | 卡数 | 来源 | 级别 |
| :-- | :-- | :-- | ---: | :-- | :-: |
| ⭐ **GLM-4.7** | **FP8** | `### Tensor Parallel + MTP (FP8 on 4xH200)` + `--tensor-parallel-size 4`；yaml `vram_minimum_gb: 430`；`**Hardware:** 4x-8x H200 (FP8)` | **4** | [vLLM recipes `models/zai-org/GLM-4.7.yaml`](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-4.7.yaml) | **M** |
| ⭐ **MiniMax M2 / M2.1 / M2.5 / M2.7** | FP8 | `You can use **4x H200**/H20/H100 or 4x A100/A800 GPUs to launch this model.` + `Note that pure TP8 is not supported. To run the model with >4 GPUs, please use DP+EP or TP+EP` | **4** | [vLLM recipes `MiniMax/MiniMax-M2.md`](https://github.com/vllm-project/recipes/blob/main/MiniMax/MiniMax-M2.md) | **M** |
| DeepSeek-R1 / V3 / V3.1 | W4A8 / AWQ / MXFP4 / NVFP4 | `W4A8 / AWQ / MXFP4 / NVFP4 → 8× H20/H100, **4× H200**; …` | **4** | [SGLang cookbook DeepSeek 硬件表](https://docs.sglang.io/llms-full.txt) | **M** |
| DeepSeek-V3.2 | NVFP4 | `**Hardware**: Minimum 8x H100/H200 80GB GPUs (BF16) or **3x H200** (NVFP4 variant).`；yaml `vram_minimum_gb: 403` | 3 | [vLLM recipes `DeepSeek-V3.2.yaml`](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V3.2.yaml) | **M** |

⭐ **`GLM-4.7-FP8` 是本轮找到的唯一一条「400+ GB 权重 + 官方 4×H200」的实例**（`vram_minimum_gb: 430`，与我们的 487 GB 预算同量级）。**M** 级，且它是 vLLM 官方 recipe 而非用户配置。

**全仓机械统计**（`vllm-project/recipes` 全部 `.md` + `.yaml`，按 `N×H200` 模式）：`8xh200` **82 次** · `4xh200` **26 次** · `1xh200` 18 · `2xh200` 15 · `16xh200` 4 · `3xh200` 1。SGLang `llms-full.txt` 同法：`8xh200` 27 · `4xh200` 13 · `1xh200` 9 · `2xh200` 5 · `16xh200` 1。⚠️ **即 4×H200 不是罕见配置，但它在 400+ GB 档是罕见的。**

### 4.3 ⛔⛔ 本轮最重要的发现：一批「装得下」的件的内核是 Blackwell 专属

⛔⛔ **H200 是 Hopper（compute capability 9.0），不是 Blackwell。** 而 §1.2 里相当一部分「装得下」的件依赖的量化格式，其高性能内核是 **Blackwell 原生**的。⛔ **这使「按容量算装得下」与「在这四张卡上跑得动」出现真实分歧**，逐条逐字如下：

| 件 | 官方逐字 | ⛔ 对 4×H200 的含义 |
| :-- | :-- | :-- |
| ⛔ **`Motif-3-NVFP4`**（186.9 GB，总分 47.4） | card 逐字：「NVFP4 requires **NVFP4-capable hardware** (NVIDIA Blackwell / B200)」；「this 314B checkpoint serves on **two B200 GPUs** on a single node — that is the **validated** deployment configuration」 | ⛔ **明确排除 H200**。⚠️ 其 BF16 档是 629.7 GB，⛔ 也装不下。**故 Motif 3 在本包络下整体失效** |
| ⛔ **`MiniMaxAI/MiniMax-M3-MXFP8`**（443.7 GB，总分 45.40） | SGLang 逐字：「The **MXFP8 kernels are Blackwell-only**, so **Hopper (H200) serves the full-precision bfloat16 build** `MiniMaxAI/MiniMax-M3`. … it runs at `--tp 8` (the bf16 weights need a full 8-GPU node)」 | ⛔ **按 SGLang 口径，H200 只能跑它的 BF16（854.2 GB），⛔ 而那装不下。** ⚠️ 但见下方冲突记录 |
| ⛔ `nvidia/GLM-5.2-NVFP4`（464.8 GB，总分 52.64） | card 逐字只写「**Test Hardware:** NVIDIA B200」 | ⛔ **官方未在 H200 上验证过**。⛔ vLLM 侧 GLM-5.2 的 H200 格是 `--tp 8`（FP8，893 GB），⛔ 无 4 卡格 |
| ⛔ `nvidia/MiniMax-M3-NVFP4`（250.1 GB） | card 逐字「**Test Hardware:** NVIDIA Blackwell B200」 | ⛔ 同上 |
| ⛔ `nvidia/Nemotron-3-Ultra-550B-NVFP4`（352.3 GB，总分 38.32） | card 逐字「**Minimum GPU Requirement** \| 4xGB200, 4xB200, 4x GB300, 4x B300, **8xH100**」；「Single-node: 4× B200」 | ⛔ **4 卡档只给 Blackwell；非 Blackwell 要 8 卡** |
| ⛔ `thinkingmachines/Inkling-NVFP4` | vLLM yaml 逐字「featured configuration is 4x GB200 … **On Hopper, NVFP4 uses TP8 on H200**」 | ⛔ 4 卡只属 GB200；H200 要 8 卡（且它 581.5 GB 本就装不下） |
| ⚠️ `Mistral-Large-3-NVFP4`（403.1 GB，⛔ 总分仅 15.92） | vLLM yaml 逐字「NVFP4 weights on 4xB200 (use for <64K context; **B200-native, Marlin fallback on A100/H100**)」 | ⚠️ **有 Hopper 回退路径（Marlin）**，⛔ 但官方 4 卡格仍只给 B200 |

⛔ **一处必须原样保留的两源冲突（⛔ 本文不裁定）**：SGLang 说 MXFP8 内核 Blackwell-only；⛔ 而 vLLM 的 `MiniMax-M3.yaml` 在 mxfp8 变体的注释里写「**H200 (1128 GB node) has the headroom and keeps the full window**」，且该变体**没有** `supported_hardware` 白名单（对比其 mxfp4 变体明确写了 `supported_hardware: [mi355x]`）。⛔ **两边都没有给「H200 上 MXFP8 走什么内核路径」的正面陈述**，⛔ 故本文不判定 `MiniMax-M3-MXFP8` 在 H200 上能否跑，只登记冲突。⚠️ 另注意 vLLM 那条注释说的是 **8×H200（1128 GB）**，⛔ 不是 4×H200。

⭐ **由此得出「格式在 Hopper 上安全」的筛选**，这是比 §2.3 的纯容量排序更实用的一张表：

| 格式 | Hopper（H200）原生支持 | 依据 |
| :-- | :-: | :-- |
| **BF16** | ✅ | — |
| **FP8（e4m3）** | ✅ | Hopper 有 FP8 张量核；GLM-4.5 card 前置条件第 4 条即要求「devices that natively support FP8 inference」并把 H200 列入 |
| **GPTQ / AWQ INT4** | ✅（Marlin 内核） | SGLang DeepSeek 表把 `AWQ` 与 `4× H200` 并列 |
| ⚠️ **MXFP4** | ⚠️ 部分 | gpt-oss-120b 官方背书单张 80 GB H100，⛔ 但 vLLM 对 M3 的 mxfp4 变体写 `supported_hardware: [mi355x]` |
| ⛔ **NVFP4** | ⛔ 非原生 | 上表五条逐字，⛔ 一致指向 Blackwell；Hopper 只有 Marlin 回退（省显存不省速度） |
| ⛔ **MXFP8** | ⛔ 存疑 | ⛔ 两源冲突，见上 |

⭐ **在「装得下 + 作者件 + 格式在 Hopper 安全 + 有官方 4×H200 说法」四条全满足下，最强的是 `MiniMax M2.7`（总分 38.87、AA-LCR 75.3、原生 FP8 230.1 GB）**——vLLM 官方 recipe 逐字写着 `You can use 4x H200/H20/H100`。⚠️ 次选 `GLM-4.7-FP8`（34.46、354.9 GB，官方 `4xH200` recipe）。⚠️ **若只要求前三条（不要求官方已点名 4 卡），则 `Hy3-FP8`（42.21、299.9 GB、Apache-2.0、纯 FP8）更强。**

### 4.4 专家并行的 4 卡可行性 ✅（⛔ 不是阻碍）

⭐ **整除约束全部过关，且「专家数必须被卡数整除」这个担心本身是多余的**——vLLM 源码逐字（[`fused_moe/expert_map_manager.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/fused_moe/expert_map_manager.py)）：

```
base_experts = global_num_experts // ep_size
remainder = global_num_experts % ep_size
local_num_experts = base_experts + 1 if ep_rank < remainder else base_experts
```

⭐ **默认 EP 路径显式分摊余数**，⛔ 只有开 **EPLB** 才要求整除（[`fused_moe/layer.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/fused_moe/layer.py) 逐字「EPLB currently only supports even distribution of experts across ranks」）。真正的硬断言是两条：`assert self.intermediate_size % tp_size == 0`（[`fused_moe/config.py`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/fused_moe/config.py)）与「Total number of attention heads must be divisible by tensor parallel size」（[`config/model.py`](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）。

**逐候选对 TP=4 / EP=4 验算（`config.json` 实测）**：

| 模型 | 专家数 | `moe_intermediate_size` | `num_attention_heads` | `num_key_value_heads` | TP=4 / EP=4 |
| :-- | ---: | ---: | ---: | ---: | :-- |
| MiniMax M3 | 128 | 3072 | 64 | 4 | ✅ 全整除 |
| GLM-4.7 | 160 | 1536 | 96 | 8 | ✅ |
| GLM-5.2 | 256 | 2048 | 64 | 64（MLA） | ✅ |
| DeepSeek V3.2 | 256 | 2048 | 128 | 128（MLA） | ✅ |
| **Kimi K2** | **384** | 2048 | 64 | 64（MLA） | ✅ ⭐ **384/4 = 96** |
| Nemotron 3 Ultra | 512 | 5120 | 64 | ⚠️ **2** | ⚠️ KV 头 2 < 4，走复制路径 |
| Hy3 | 192 | 1536 | 64 | 8 | ✅ |
| Inkling | 256 | 3072 | 64 | 8 | ✅ |

⛔ **vLLM 与 SGLang 均未规定 EP 的最小卡数**——两边文档全文都没有「EP requires at least N GPUs」这类表述。vLLM 逐字只说 `EP_SIZE = TP_SIZE × DP_SIZE`（[Expert Parallel Deployment](https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment.html)）。⚠️ **但 SGLang 有一条真约束**（[Expert Parallelism](https://docs.sglang.io/docs/advanced_features/expert_parallelism)）逐字：「DeepEP, Mooncake, NIXL-EP, ascend_fuseep, pplx and MORI **only support cases where `ep_size = tp_size`**」——即 4 卡上想用高性能 all-to-all 后端，必须 `--tp 4 --ep 4`。

### 4.5 互联：⭐ 4 卡 H200 + 564 GB 是 NVIDIA 自己定义的产品形态

⭐ **NVIDIA 官网只列两个 H200 型号，⛔ 不存在独立的「H200 PCIe」——NVL 就是 PCIe 形态**（[nvidia.com/en-us/data-center/h200](https://www.nvidia.com/en-us/data-center/h200/)）：

| 规格 | H200 SXM | H200 NVL |
| :-- | :-- | :-- |
| 显存 | `141GB` | `141GB` |
| 显存带宽 | `4.8TB/s` | `4.8TB/s` |
| 互联 | `NVLink: 900GB/s` | `900GB/s per GPU`（`2- or 4-way NVLink bridge`） |
| PCIe | `PCIe Gen5: 128GB/s` | `PCIe Gen5: 128GB/s` |
| 形态 | `SXM` | `PCIe / Dual-slot air-cooled` |
| TDP | `Up to 700W` | `Up to 600W` |

⭐ **两者显存都是 141 GB，故 $4 \times 141 = 564$ GB 成立。**

⭐⭐ **NVIDIA 官方博客逐字用的就是 564 GB 这个数**（[Deploying NVIDIA H200 NVL at Scale](https://developer.nvidia.com/blog/deploying-nvidia-h200-nvl-at-scale-with-new-enterprise-reference-architecture/)）：

> 「The H200 NVL introduces support for a new **4-way NVLink interconnect**, delivering up to **1.8 TB/s** of bandwidth and a **combined 564 GB of HBM3e memory** — 3x the memory compared to H100 NVL in a 2-way NVLink configuration.」

⭐ **即「4 卡 H200 + NVLink + 564 GB」不是拼凑配置，而是 NVIDIA 自己命名并背书的一档产品形态。** ⛔ 但该博客**未把任何模型规模与 4-way 配置绑定**，且其参考架构本身是每节点 8 GPU。

⛔ **一条必须带走的官方警告：无 NVLink 的多卡不要跑 TP。** vLLM 逐字（[Parallelism and Scaling](https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html)）：「if the GPUs on the node **do not have NVLINK** interconnect (e.g. L40S), **leverage pipeline parallelism instead of tensor parallelism** for higher throughput and lower communication overhead」。原因 vLLM 也写了：「TP incurs significant communication overhead because of **all-reduce being performed after every layer**」——以 GLM-4.7 的 92 层为例，TP=4 下每 token 至少 92×2 次集合通信，而 NVLink 900 GB/s 与 PCIe Gen5 128 GB/s 相差约 **7 倍**（NVIDIA 自己的措辞就是 `7x faster than PCIe Gen5`）。⭐ **所以这四张卡必须有 NVLink（SXM 或 4-way NVL bridge），⛔ 纯 PCIe 的四卡应改用 PP 而非 TP。**

⏳ **未取到**：4-GPU HGX H200 基板的官方规格（NVIDIA HGX 页已改版，只剩 Rubin / Blackwell）；4 卡 SXM（NVSwitch）vs 4 卡 NVL bridge 在 TP=4 下的官方实测对比；H200 官方 datasheet PDF（`resources.nvidia.com/...h200` 返回 302 跳首页，⛔ 入口已定位、内容待人工核验）。

### 4.6 ⚠️ 昇腾线索的修正

⚠️ **主 session 给的「2 台 8×64GB = 1024 GB 跑 W8A8」这个说法接近但表述需修正。** 官方逐字（[SGLang Ascend NPU · DeepSeek-V3.2](https://docs.sglang.io/docs/hardware-platforms/ascend-npus/model-deployment/tutorials/deepseek_v3_2)）：

> 「The W8A8 variant (694.47GB) can be deployed on **16 × 64GB of device memory** (`--tp-size 16`), which corresponds to **one full A3 node (8 cards, 16 dies) or two A2 nodes**.」
>
> 「This is the **minimum recommended configuration**.」

⭐ **修正：官方主口径是「16 × 64 GB = 1024 GB、`--tp-size 16`」，其物理形态可以是*一台* A3 节点（8 卡 16 die）**或**两台 A2 节点。「2 台 8×64GB」只对应 A2 那一种落法，⛔ 不是唯一说法。** 数字 1024 GB / W8A8 / 「minimum recommended configuration」三点均核实通过（**M**）。

### 4.7 ⭐ 一句话工程结论

⭐ **没有已知的硬阻碍：整除、EP、互联三层全部过关。** 专家数（128/160/192/256/384/512 全可被 4 整除，⭐ 且 vLLM 默认 EP 路径本就分摊余数）、`moe_intermediate_size` 与注意力头数在 TP=4 下全整除；4-way NVLink 是 NVIDIA 自己定义的产品形态、其官方文案用的正是 `combined 564 GB of HBM3e` 与 `1.8 TB/s`；⭐ 而 `GLM-4.7-FP8`（官方 `vram_minimum_gb: 430`）就有 vLLM 官方 recipe 写着 `### Tensor Parallel + MTP (FP8 on 4xH200)`。

⛔ **真正的风险不在「跑不跑得起来」，而在三处**：

1. ⛔⛔ **能把模型压到这个区间的精度格式往往是 Blackwell 专属**（§4.3）。⛔ 这是本轮最实质的发现：它把 §2.3 容量排序里的前三名（GLM-5.2 / Motif 3 / MiniMax M3）**全部打上问号**。
2. ⛔ **KV cache 余量被挤干**：GLM-4.5 官方就是用同一个 `H200 x 4` 格区分「跑得动」与「用满 128K」，后者要 8 卡。4×H200 减掉 430 GB 只剩约 134 GB。⚠️ 叠加 §4.1 那条 batch ≤ 8 的前置条件，⛔ **并发是被显存直接换掉的**。
3. ⛔ **它落在两家框架的 validated matrix 之外**：⛔ **SGLang 的 H200 格无一例外是 `--tp 8`**（GLM-5.2 FP8 h200 → `--tp 8` `verified: true`），⛔ **4-GPU 格只给 GB200 / GB300 / B300**。外加 GLM-4.5 card 那条容易被忽略的主机侧门槛 `Server memory must exceed 1T`。

## 5. 官方量化件 vs 社区量化件清单

⭐ **这一节是本文对研究最承重的部分**：区分「模型作者自己发布的量化件」与「他方发布的量化件」。⛔ 理由是**只有作者件能被引用为「该模型在这个精度下的官方配置」**；三方件的精度、校准集、被量化层的选择都由第三方决定，⛔ 且作者不为其能力背书。

### 5.1 判定口径

| 归属 | 判据 | 本轮实例 |
| :-- | :-- | :-- |
| ✅ **作者件** | 量化仓库与主模型仓库**同属一个 HF 组织** | `MiniMaxAI/*-MXFP8` · `Qwen/*-FP8` · `Qwen/*-GPTQ-Int4` · `zai-org/*-FP8` · `mistralai/*-NVFP4` · `thinkingmachines/*-NVFP4` · `inclusionAI/Ling-3.0-*-int4/fp4/fp8` · `tencent/Hy3-FP8` · `nvidia/Nemotron-*-NVFP4`（⚠️ NVIDIA 是 Nemotron 的作者，此处它是作者不是三方） |
| ⚠️ **作者旁系** | 同一公司但不同 HF 组织的专职压缩团队 | `AngelSlim/Hy3-GPTQ-Int4`（腾讯自家压缩工具链）——⚠️ 本文单列，⛔ 不与作者件合并 |
| ⛔ **三方件** | 他方组织发布，⛔ 无论多权威 | `nvidia/GLM-5.2-NVFP4`（464.8）· `nvidia/GLM-5.1-NVFP4`（465.9）· `nvidia/GLM-5-NVFP4`（460.8）· `nvidia/MiniMax-M3-NVFP4`（250.1）· `nvidia/Qwen3.5-397B-A17B-NVFP4`（251.2）· `nvidia/Kimi-K2.6-NVFP4`（⛔ 595.2）· `nvidia/Kimi-K2.7-Code-NVFP4`（⛔ 595.2）· `nvidia/DeepSeek-V4-Pro-NVFP4`（⛔ 913.1）· `amd/Kimi-K2.6-MXFP4`（⛔ 559.0）· `Intel/*` · `RedHatAI/*` · `unsloth/*` · `ggml-org/*` · `bartowski/*` · `mlx-community/*` |

⚠️ **NVIDIA 在本表里出现在两种身份上，⛔ 不要混**：对 **Nemotron 系列它是作者**（`nvidia/NVIDIA-Nemotron-*` 是原始模型）；⛔ 对 GLM / MiniMax / Qwen / Kimi / DeepSeek 它只是**第三方量化方**。⚠️ 判据是「该组织有没有发布这个模型的原始权重」，⛔ 不是「这个组织权威不权威」。

### 5.2 ⛔ 关键否定结论（本轮最硬的三条事实）

| # | 结论 | 核验方式（可复现） |
| --: | :-- | :-- |
| 1 | ⛔ **DeepSeek 从未发布任何官方 4-bit / INT4 / AWQ / GPTQ / NVFP4 权重** | `GET https://huggingface.co/api/models?author=deepseek-ai&limit=1000` → **102 个仓库**，用 `int4\|awq\|gptq\|nvfp4\|fp4\|4bit\|w4a\|mxfp4\|int8\|w8a8\|bnb` 匹配 `id`，⛔ **命中 0**。⚠️ V4 系的 FP4 是**原生混合精度写在主仓库里**，不是额外发的量化件 |
| 2 | ⛔ **Z.ai（GLM）在 GLM-4.5 之后的世代没有发布过任何 4-bit 件** | 同法查 `author=zai-org`：唯一命中的 int4 仓库是 `chatglm-6b-int4` / `chatglm2-6b-int4` / `codegeex2-6b-int4` / `cogvlm2-*-int4` 一类的 **2023 代产物**。⛔ GLM-4.7 / 5 / 5.1 / 5.2 的 4-bit **全部只能走三方**（`nvidia/GLM-5.2-NVFP4` 等） |
| 3 | ⛔ **Moonshot（Kimi）名下零个独立量化仓库** | 同法查 `author=moonshotai`：19 个仓库，⛔ 无任何 `-INT4` / `-FP8` / `-NVFP4` 独立件。K2-Thinking / K2.5 / K2.6 / K2.7-Code 的 **INT4 QAT 就在主仓库里**（`I32` 打包，595.2 GB），K3 的 MXFP4 同理。⛔ **没有更小的官方档可降** |

### 5.3 ✅ 装得下的候选里，哪些走的是作者件

| 模型 | 首选件 | 归属 | ⚠️ 若只认作者件，会失去什么 |
| :-- | :-- | :-- | :-- |
| ⭐⭐ **DeepSeek V4-Flash-0731**（总分 51.77，⭐ 作者件里最高） | **原生 FP4+FP8 166.9 GB** | ✅ **作者** | ⭐ **无损失，且余量 320 GB**。⛔ 三方 `nvidia/DeepSeek-V4-Pro-NVFP4` 反而是 913.1 GB（§3.6） |
| ⛔ **Motif 3**（总分 47.4） | 作者 NVFP4 186.9 GB | ✅ 作者 | ⛔ 归属无问题，⛔ **但 card 逐字要求 Blackwell / B200**，⛔ 其 BF16 档 629.7 GB 装不下 → **在 H200 上整体失效**（§4.3） |
| **MiniMax M3** | MXFP8 443.7 GB | ✅ **作者** | ⚠️ 归属无问题，⛔ **但 MXFP8 内核可能 Blackwell 专属**（§4.3 两源冲突）。⚠️ 更省显存的 `nvidia/MiniMax-M3-NVFP4`（250.1 GB）是三方件且 Test HW 为 B200 |
| **Qwen3.5-397B-A17B** | FP8 406.2 / GPTQ-Int4 235.7 | ✅ **作者（两档都是）** | 无损失。⭐ **本表里唯一「作者同时发了 8-bit 与 4-bit」的大档模型** |
| **Hy3** | FP8 299.9 GB | ✅ 作者 | ⚠️ INT4 档（166.4 GB）是作者旁系 AngelSlim |
| **MiniMax M2.7** | FP8 230.1（原生） | ✅ 作者 | 无损失 |
| **Mistral Large 3 675B** | NVFP4 403.1 GB | ✅ 作者 | 无损失 |
| **Inkling-Small** | NVFP4 166.3 GB | ✅ 作者 | 无损失 |
| **Nemotron 3 Ultra 550B** | NVFP4 352.3 GB | ✅ 作者（NVIDIA 即作者） | 无损失 |
| **Muse Glimmer 30B** | BF16 59.6 GB | ✅ 作者 | 无损失（⛔ 不需要量化） |
| ⛔ **GLM-5.2** | NVFP4 464.8 GB | ⛔ **三方** | ⛔ **整个候选失效**——作者侧最小件是 FP8 755.6 GB，⛔ 装不下。**要用 GLM-5.2 就必须接受三方件** |
| ⛔ **GLM-5** | NVFP4 460.8 GB | ⛔ 三方 | ⛔ 同上 |

### 5.4 ⭐ 按约束逐层收紧的推论（⛔ 与 §0 的三层答案一致）

| 硬约束组合 | 最强候选 | v4.1.1 总分 | 件与体积 |
| :-- | :-- | ---: | :-- |
| 只要装得下 | `GLM-5.2` | **52.64** | ⛔ 三方 NVFP4 464.8 |
| ＋必须作者件 | ⭐ **`DeepSeek V4-Flash-0731`** | **51.77** | 原生 FP4+FP8 **166.9**，MIT |
| ＋许可须 OSI（Apache/MIT） | ⭐ **同上**（MIT 已满足） | **51.77** | 同上 |
| ＋格式须在 Hopper 原生（⛔ 排除 NVFP4/MXFP8/未核 FP4） | **`Hy3-FP8`** | **42.21** | 作者 FP8 **299.9**，Apache-2.0 |
| ＋官方已点名 4×H200 | ⭐ **`MiniMax M2.7`** | **38.87** | 原生 FP8 **230.1**，⛔ 自定义许可 |
| ＋官方 4×H200 且许可须 OSI | **`GLM-4.7-FP8`** | **34.46** | 作者 FP8 **354.9**，MIT，官方 `vram_minimum_gb: 430` |

⛔ **两条对论文表述直接有用的推论**：

1. ⛔ **「作者件」这条约束在本包络下代价很小**（52.64 → 51.77，仅 0.87 分），⛔ **但「Hopper 原生格式」这条代价很大**（51.77 → 42.21，掉 9.56 分）。⭐ **所以论文里若要讲部署可行性，承重的限制是硬件世代而不是件的归属。**
2. ⚠️ **`Qwen3.5-397B-A17B` 是唯一同时满足「作者件 + Apache-2.0 + 装得下 + 大档 + 作者同时发了 8-bit 与 4-bit 两档」五条的模型**（FP8 406.2 / GPTQ-Int4 235.7），⛔ 但它的总分只有 **34.26**、⛔ 幻觉净分 **−30.8**。⛔ **可部署性最好的那个不是能力最好的那个。**

## 6. 待核验与访问受限

### 6.1 ⛔ 本轮的核心缺口（按对结论的影响排序）

| # | 缺口 | ⛔ 影响 |
| --: | :-- | :-- |
| 1 | ⛔⛔ **「结构化输出 × 量化档」在公开文献里完全没有数据** | ⛔ 这是**真实空白而非漏检**（§3.4）。⛔ 我们的负载恰恰是严格 JSON schema，⛔ 且 IFEval/IFBench 不是合法代理（测的不是同一件事、已饱和、且合法性被约束解码搬出了模型侧）。⭐ **这一项只能自测**：在真实 30K + schema 负载上跑 FP8 与 4-bit 两档的**字段级指标**（schema 校验通过率、枚举越界率、必填缺失率、字段语义正确率），差异对照代次内方差判断可归因性 |
| 2 | ⛔⛔ **量化件与能力分数无法对应** | AA 不披露 provider 的量化档，故「`nvidia/GLM-5.2-NVFP4` 的 AA-LCR = 76.7」**没有证据**。⛔ 本文 §1 表凡标 ⚠️ 的 AA-LCR 格子都是**跨精度档挪用**。⚠️ §3.1 给了同向量级估计，⛔ 但两套数字不可交叉相减 |
| 3 | ⛔⛔ **`MiniMax-M3-MXFP8` 在 H200 上能否跑，两源冲突未裁定** | ⛔ SGLang 说 MXFP8 内核 Blackwell-only、Hopper 只能跑 BF16（854.2 GB，装不下）；⛔ vLLM yaml 注释假定 H200 可跑但说的是 **8×H200**。⛔ **这直接决定 §2.3 的第 4 名是否有效** |
| 4 | ⛔ **「8-bit KV 是否安全」两源冲突未裁定** | ⛔ arXiv:2606.09864 报 8-bit KV 让 IFEval 严格通过率掉 9.6 点；⛔ 而 NVIDIA 在 FP8 KV 下测出的 IFBench/τ² 全部正常。⛔ 前者是**未被复现的单篇 preprint** 且阈值高度 model-specific |
| 5 | ⛔ **64K–128K 上 4-bit 掉多少，两源量级冲突** | ⛔ Red Hat RULER 说 128K 处 85–88% recovery；⛔ arXiv:2505.20276 说 GPTQ-int4 在 RULER 64K+128K 聚合上掉 21.2%。⭐ **两者在「30K 安全」上一致**，⛔ 故该冲突不影响本包络的结论 |
| 6 | ⛔ **本文没有一条实机运行证据** | ⛔ 全部为 HF API 静态核算 + 官方文档引用。而 [hardware_availability.md](./hardware_availability.md) §3.4 已记录一次真实 OOM（DeepSeek-R1-W8A8 在 1024 GB 上），⛔ 且 GLM-4.5 官方 card 自己预告 8×H100（640 GB）跑 361.3 GB 权重仍可能不够。⛔ **贴边格子（GLM-5.2-NVFP4 467.5 · Qwen3-Coder-480B 489.7）不可信** |
| 7 | ⚠️ **MiniMax M3 的 AA-LCR 80.3 是否来自蒸馏前沿模型，未核** | ⚠️ 已知同榜的 `Muse Glimmer 30B` 的 80.0 确实来自蒸馏 `Muse Spark 1.2`。⛔ 若 M3 亦然，则「开放权重追上前沿」的表述需要相应收窄 |
| 8 | ⏳ **部分候选的 KV@30K 未算** | ⏳ Muse Glimmer 30B · Step 3.7 Flash · Inkling-Small · Nemotron 3 Ultra · Mistral Large 3 · Llama 4 Maverick · Motif 3 · Qwen3.5-122B 的 KV 未取到（多因 `config.json` 结构嵌套或 gated）。⛔ **未编造任何一个** |
| 9 | ⚠️ **§1 的全部 KV@30K 都是 batch = 1** | ⚠️ KV 随 batch 线性放大；主 session 的 20 GB 额度对 `MiniMax M3` 意味着 batch 上限约 5、对 `Hy3` 约 2。⛔ **不要把 ✅ 读成「能以任意并发跑」**（§4.1） |
| 10 | ⚠️ **MiniMax M3 的 KV 是高估** | card 明写 MSA「dramatically reduces… memory footprint」相对 GQA。⛔ 本文按 GQA 公式给的 3.7 GB 是**上界** |
| 11 | ⏳ **`DeepSeek V4-Flash` 的 FP4 部分在 Hopper 上的内核路径未核** | ⛔ 这影响 §0 第 ② 层答案。⚠️ 一条同向线索：SGLang 的 DeepSeek 硬件表把 `W4A8 / AWQ / MXFP4 / NVFP4` 与 `4× H200` 并列（针对 R1/V3），⛔ 但那不是 V4 |
| 12 | ⏳ **AA 官方 REST API 受限** | `GET /api/v2/data/llms/models` → **HTTP 401 `{"error":"API key is required"}`**。⛔ 记为**访问受限**；⭐ 已通过官方页内嵌 payload 绕过，⛔ 未降级为二手 |
| 13 | ⏳ **4-GPU HGX H200 基板的官方规格未取到** | NVIDIA HGX 页已改版只剩 Rubin / Blackwell。⛔ 4 卡 SXM（NVSwitch）vs 4 卡 NVL bridge 在 TP=4 下的官方实测对比亦未取到 |

### 6.2 ⛔ 访问受限记录

| 对象 | 症状 | 处理 |
| :-- | :-- | :-- |
| ⛔ `moonshotai/Kimi-K2.7` | HTTP 401 | ⛔ 记为**访问受限**，不是「不存在」。该名下公开的是 `Kimi-K2.7-Code`（已入表，595.2 GB） |
| ⛔ Llama / gemma-2 / gemma-3 全系 | `gated: manual`，`config.json` 与 card 正文 401 | 沿用 [open_weight_model_compute.md](./open_weight_model_compute.md) §6.2 #1 的处理：**体积可信（API 可取），context / KV / 部署建议未核验** |
| ⏳ `artificialanalysis.ai` 官方 leaderboard | SPA / JS 渲染，WebFetch 只拿骨架 | 见 [benchmark_open_weights.md](./benchmark_open_weights.md) §5：改用两镜像交叉，⛔ 全部降级为 **S** 级 |

### 6.3 核验方法（可复现）

```bash
# 权重体积：逐文件 size 求和，只计根目录主权重集
curl -s "https://huggingface.co/api/models/{id}?blobs=true" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
      print(sum(s.get('size') or 0 for s in d['siblings'] \
        if s['rfilename'].endswith('.safetensors') and '/' not in s['rfilename'] \
        and not s['rfilename'].startswith('consolidated') and 'mtp' not in s['rfilename'].lower())/1e9)"

# 穷举某组织有无官方量化件
curl -s "https://huggingface.co/api/models?author={org}&limit=1000" \
  | grep -oE '"id":"[^"]+"' | grep -iE 'int4|awq|gptq|nvfp4|fp4|4bit|w4a|mxfp4|w8a8|bnb'

# 精度与架构参数
curl -s "https://huggingface.co/{id}/raw/main/config.json"
```

⛔ **未使用任何第三方聚合站、评测榜或博客的显存 / 参数 / 部署数字。** 能力分数一律引用 [benchmark_open_weights.md](./benchmark_open_weights.md)，⛔ 本文不新增能力事实断言。

### 6.4 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 16:40:00 | 建库并闭合五节。按 4×H200 = 564 GB / 权重预算 487 GB 重算包络；新探 **29 个 HF 仓库**（28 成功 / ⛔ 1 个 401）。⛔ **四条否定事实**：DeepSeek 102 个仓库零 4-bit · zai-org 现代世代零 4-bit · moonshotai 零独立量化仓库 · ⭐ **对已是 4-bit 的模型再做 NVFP4 不缩小**（Kimi K2.6 前后同为 595.2；⛔ DeepSeek V4-Pro 反而从 864.7 涨到 913.1）。⭐ **AA 证据级别从 S 提到 M**：并行路从官方页内嵌 flight payload 解出 563 模型 × 134 字段，用官方权重表重算 149 个模型（平均误差 0.12 分）反证版本确为 v4.1.1，五个待核锚点全中。⭐ **§0 给出三层答案**（容量 GLM-5.2 52.64 / 作者件 DeepSeek V4-Flash-0731 51.77 / +Hopper 安全 MiniMax M2.7 38.87），与 Opus 5 (max) 63.05 的比值分别 0.835 / 0.821 / 0.616。⛔⛔ **两条颠覆性发现**：① **幻觉维度是最差维度**（比值 0.119，且 V4-Flash 为负），⛔ 使「按总分挑」成为错误挑法；② **NVFP4/MXFP8 内核是 Blackwell 原生而 H200 是 Hopper**，六条官方逐字，⛔ 使容量排序前三名全部打问号、`Motif 3` 整体失效。⭐ **§4.1 亲自逐字核验 GLM-4.5 card 的 `H200 x 4`**，并发现它只属「跑得动」表、满 128K 要 8 卡，另发现 batch≤8 与主机内存 ≥1T 两条前置条件。⭐ 找到唯一 400+ GB 的官方 4×H200 实例：GLM-4.7-FP8（`vram_minimum_gb: 430`）。⭐ **§3 收敛：权重 4-bit 掉 0–3% 且规模越大越鲁棒，30K 落在 RULER >99.5% recovery 带内；⛔ 真正的雷是 KV cache 量化（W4KV8 无损 vs W8KV4 掉 20+ 点）。** ⛔⛔ **§3.4 登记一条真实文献空白：结构化输出 × 量化档零数据。** 记录 13 条待核缺口，含 4 条**未裁定的两源冲突** |
