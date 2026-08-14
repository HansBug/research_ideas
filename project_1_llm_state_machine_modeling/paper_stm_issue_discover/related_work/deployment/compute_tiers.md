# 工业算力档位分层与各档可部署模型

> **本文回答一个问题**：**现实工业场景里一个单位实际会买到什么算力形态，每一档能部署多大的开放权重模型。** ⛔ 它是**实验与部署的可行性参照表**，⛔ 不是论文叙事材料——⛔ 不论证 motivation、⛔ 不论证「工业单位没有算力」、⛔ 不做选型建议。
>
> **核验日**：2026-08-13。
>
> ⚠️ **与本目录既有文件的分工**：[open_weight_model_compute.md](./open_weight_model_compute.md) 是**权重实测体积的主真源**（145 个 HF 仓库探测、141 行主表）；[h200x4_envelope.md](./h200x4_envelope.md) 是 **4×H200 单一包络**的细算与能力定位；[hardware_availability.md](./hardware_availability.md) 是**管制与国产卡规格**的主真源；[industrial_compute_evidence.md](./industrial_compute_evidence.md) 是**训推一体机品类与官方政策文件**的主真源；[h200x4_inference_perf.md](./h200x4_inference_perf.md) 回答「装下之后**跑不跑得完**」（吞吐与并发），⛔ 而本文只回答「**装不装得下**」。⛔ **本文不重建它们的任何一张表**，只把它们的既有实测数字按「一个单位实际会买什么」这条轴重新分档。⛔ 不要把本文当成上述任何一者的第二真源。
>
> **证据级别口径**（沿用本目录既有约定）：**M** = 官方一手来源逐字可查；**S** = 二级来源（新闻、第三方拆解、聚合站、预印本检索摘要）；**I** = 本文推断或计算。⛔ 标 **I** 的不得写成事实句。

## 0. 一句话结论

**分 7 档，显存总量从 24 GB 到约 2 TB，跨度约 85 倍。** 分档轴是**采购形态**（一个单位实际会下单买什么），⛔ 不是显存数——同一个显存总量可以由完全不同的可采购性、价格量级与软件栈达成，把它们并成一档会掩盖真正的约束。

| 档 | 代号 | 典型配置 | 显存总量 | 4-bit 可容总参上限（**I**） |
| :-- | :-- | :-- | --: | --: |
| **单卡工作站** | **T1** | 1 × 消费 / 工作站卡 | **24–96 GB** | 37B–148B |
| **单机多卡工作站** | **T2** | 2–4 × 工作站卡 | **48–384 GB** | 74B–593B |
| **单节点服务器** | **T3** | 4–8 × 数据中心卡 | **192–1128 GB** | 296B–1742B |
| **桌面 / 边缘一体机** | **T4a** | 厂商小整机（GB10 统一内存 · DGX Station） | **128 GB 统一内存 / 252 GB HBM** | 198B / 389B |
| **训推一体机** | **T4b** | 厂商整机（浪潮 / 华为 / 新华三 / 曙光；⏳ 联想未核，见 §5.1 第 11 条） | **192–1536 GB** | 296B–2372B |
| **国产加速卡节点** | **T5** | 1–2 台 Atlas 800I A2（8×64 GB） | **512 / 1024 GB** | 790B / 1581B |
| **小集群** | **T6** | 2–4 台节点 | **1024–4512 GB** | 1581B–6965B |

⭐ **4×H200 = 564 GB 落在 T3（单节点服务器）**，且是 T3 内的中高位——比 4×80 GB H100 节点（320 GB）大 76%，比 8×80 GB H100 节点（640 GB）小 12%。⛔ **它不属于任何「工作站」档**，也不是一体机形态。**该档能跑的最大开放权重模型是 `Mistral-Large-3-675B`**（官方作者件 NVFP4 实测 403.1 GB，权重预算 487 GB，余 84 GB）——⚠️ 但 NVFP4 内核是 Blackwell 原生而 H200 是 Hopper，这条风险见 §2.4 第 2 条。

**四条最容易搞错的事实**：

1. ⛔ **各档之间的边界不是显存，是可采购性。** T1 的 24 GB 与 T3 的 640 GB 之间**不存在**「多买几张卡就上去」的连续路径：中国大陆一侧，**数据中心级 NVIDIA GPU 在 2026 上半年对华出货为零**（**M**，§3），而 T1 的消费 / 工作站卡明确仍可出货。**跨档要换供应商、换指令集、换软件栈。**
2. ⛔ **「一体机」不是小档。** 官方可逐字引用的一体机显存跨 **192 GB 到 1536 GB**（**M**），最高档比标准 8×H100 节点还大 2.4 倍，且官方明写可「单机部署 DeepSeek 671B」。⛔ **把一体机当成「买不起服务器的替代品」是错的。**
3. ⛔ **MoE 的稀疏性一点不降常驻显存。** `Kimi K3` 2.8T 总参只激活 104B、且原生就是 MXFP4，权重仍是 **1560.9 GB 实测**——需要 T6（$1560.9 / 0.88 = 1774$ GB 标称，即 **≥ 4 台 Atlas 800I A2** 或 **≥ 13 张 H200**；⛔ 3 台 Atlas 800I A2 的 1536 GB **不够**）。分档只能按**总参**算。
4. ⛔ **「哪一档最常见」在企业侧查无严谨统计**（§4）。官方只有**政策目标句**与**国家级宏观总量**，⛔ **单位级算力画像那一层是空的**。⭐ **但存在两条真实、官方一手、机读的公开硬件分布可作上下界参照**：**MLPerf Inference** 的 per-submission `system_desc`（厂商送测侧的**上限**，含 `accelerator_memory_capacity` 字段，Apache-2.0）与 **Hugging Face 297,135 人自报本地硬件**（个人开发者侧的**下限**；⭐ 最流行的独立显卡是 **RTX 3060**，数据中心卡仅占 top-100 报告的 **~7.7%**）。⛔ **二者都不是企业样本**，⛔ 不得当成工业界分布——**这个区分是本节的全部要点**。

## 1. 算力档位分层表（配置 / 显存 / 可采购性 / 价格）

### 1.1 计算口径（⛔ 先读）

**权重预算**：$\mathrm{Budget} = 0.88 V$，其中 $V$ 为标称显存总量（GB）。系数 0.88 的来源：vLLM 默认 `gpu_memory_utilization = 0.92`（torch 可用上限），其中再留约 $0.04V$ 给激活 + CUDA graph + NCCL 通信缓冲。**KV cache 显式扣出**，按 30K 上下文、FP16 KV 逐模型实算。⛔ 该口径与 [open_weight_model_compute.md](./open_weight_model_compute.md) §2.1 完全一致，两文可直接互查。

**每参字节数**：BF16 = 2 · 8-bit ≈ 1.06 · 4-bit ≈ 0.57（实测锚点区间 0.55–0.62；校准：Qwen3-235B 官方 `Q4_K_M` 为 $142.2 / 235.1 = 0.605$、Qwen3-32B-AWQ 为 $19.3 / 32.8 = 0.589$）。⛔ **4-bit 系数只用于没有已发布量化件的模型**（标 `估`）；凡有实测量化件的一律用实测体积。

⛔ **MoE 的全部专家权重须常驻**，进公式的是**总参**而非激活参数——稀疏只降算力。

⚠️ **一条使全表在贴边格子上偏乐观的反向实测**：官方仓库 issue [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 报告 **DeepSeek-R1-W8A8 在 2×8×64 GB（1024 GB）上 OOM**，而按本口径它装得下。**真实常驻开销比 0.88 更重**（**S** 实测 · **I** 推断）。⛔ 凡标 ⚠️ 贴边的格子不得据以选型。

### 1.2 T1 单卡工作站

| 配置 | 显存 | 类型 | 中国大陆可采购性（2026-08） | 价格量级 | 级别 |
| :-- | --: | :-- | :-- | :-- | :-- |
| RTX 4090 | **24 GB** | GDDR6X，384-bit（⛔ **官方页不给 GB/s**） | ⛔ 全球版非中国版；4090D 为合规特供 | **MSRP $1,599**（官方新闻稿） | **M** |
| ⭐ **RTX 5090 D v2**（中国特供） | **24 GB** | GDDR7，**384 位**（⚠️ 官网**不给** GB/s；1344 GB/s 仅见媒体，**S**） | ✅ **合法在售**——属 NVIDIA 10-Q 自称的 "uncontrolled … gaming and workstation GPUs"；官网列出合作伙伴「华硕、七彩虹、耕升、影驰、技嘉、映众、微星、索泰、万丽」 | ⭐ **「￥16,499 元起」**（**NVIDIA 中国官网**） | ⭐ **M**（容量 / 位宽 / 价格 / 在售）· **M** 类别 |
| RTX 5090（全球版） | **32 GB** | GDDR7，512-bit，**1792 GB/s** | ⛔ 非中国版；灰市有 | **MSRP $1,999**（官方公告） | **M** |
| **RTX 6000 Ada Generation** | **48 GB** | GDDR6 **ECC**，384-bit，**960 GB/s**，300W | ⏳ 工作站类别名义可出货，具体型号未核 | ⛔ **NVIDIA 官方不公布价格** | **M** |
| RTX A6000（Ampere） | **48 GB** | GDDR6 ECC，384-bit，**768 GB/s**，300W | ⏳ 同上 | ⛔ 官方不公布 | **M** |
| **RTX 6000D**（中国特供） | **84 GB** | GDDR7，448-bit，~1398 GB/s | ⚠️ 曾在售；据报**市场失败并被中方禁 / 劝退**（⛔ 该判定的官方依据**至今未找到**，见 [hardware_availability.md](./hardware_availability.md) §7.2 第 10 条） | 约 **¥50,000**（**S**） | S ⚠️ |
| **RTX PRO 6000 Blackwell Workstation** | **96 GB** | GDDR7 **ECC**，512-bit，**1792 GB/s**，600W | ⛔ 非中国版 | ⛔ **NVIDIA 官方不公布价格**（购买路径为 "Buy Now" → NVIDIA Marketplace / "Find a Partner"） | **M** |
| **昇腾 910B 单卡** | **64 GB** | HBM | ✅ 国产，中方鼓励 | ⛔ 无公开价格 | **M**（经官方软件文档；⛔ 硬件规格页不公布） |
| Atlas 350 加速卡（Ascend 950PR） | 112 GB | HBM @ 1.4 TB/s | ✅ 国产新一代 | ⛔ 无公开价格 | **M** |
| ⚠️ Atlas 300I Duo | 96 或 48 GB | **LPDDR4X，仅 408 GB/s** | ✅ 国产在售 | ⛔ 无公开价格 | **M** |
| 寒武纪 MLU370-X8 | 48 GB | **LPDDR5，614 GB/s** | ✅ 国产 | ⛔ 无公开价格 | **M** |
| 摩尔线程 MTT S4000 | 48 GB | ⚠️ 类型未标，768 GB/s | ✅ 国产 | ⛔ 无公开价格 | **M** |

⛔ **一条容量数字会掩盖的事实**：**Atlas 300I Duo 的「96 GB」是 LPDDR4X（408 GB/s）、寒武纪与摩尔线程的「48 GB」是 LPDDR5 / GDDR 级**——⛔ **容量与 HBM 卡相同但带宽差一个量级**，对 decode 吞吐影响很大（**I**）。⛔ **不能只按容量选型。**

⛔ **除华为外，国产卡厂商普遍不公布显存规格**：壁仞在产品线、摩尔线程 S5000、海光全线、寒武纪 590/690 均为「官方未公布」或「查无官方来源」。**能拿到官方出处的国产卡显存数字只有四条**（华为间接经软件文档、寒武纪 MLU370-X8、摩尔线程 S4000、天数智芯智铠100）。

### 1.3 T2 单机多卡工作站

| 配置 | 显存总量 | 中国大陆可采购性 | 价格量级 | 级别 |
| :-- | --: | :-- | :-- | :-- |
| 2 × 24 GB（5090D V2 / 4090D） | **48 GB** | ✅ 合法 | ~¥33,000（按发布价 ×2，**I**） | S · I |
| 2 × 32 GB（5090 全球版） | 64 GB | ⛔ 非中国版 | ~$3,998（按 MSRP ×2，**I**） | **M** MSRP · I |
| 4 × 24 GB | **96 GB** | ✅ 合法 | ~¥66,000（**I**） | S · I |
| 2 × 48 GB（L40S / RTX 6000 Ada） | **96 GB** | ⏳ L40S 属数据中心线，对华受限 | ⛔ 官方不公布 | **M** 规格 |
| 4 × 48 GB | **192 GB** | ⏳ 同上 | ⛔ 官方不公布 | **M** 规格 |
| 2 × 96 GB（RTX PRO 6000 Blackwell） | 192 GB | ⛔ 非中国版 | ⛔ 官方不公布 | **M** 规格 |
| 4 × 96 GB（RTX PRO 6000 Blackwell） | **384 GB** | ⛔ 非中国版 | ⛔ 官方不公布 | **M** 规格 |
| 4 × 昇腾 910B（64 GB） | **256 GB** | ✅ 国产 | ⛔ 无公开价格 | **M** · I |

⛔ **T2 有一条官方警告必须带走：无 NVLink 的多卡不要跑 TP。** vLLM 逐字（[Parallelism and Scaling](https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html)）：「if the GPUs on the node **do not have NVLINK** interconnect (e.g. L40S), **leverage pipeline parallelism instead of tensor parallelism** for higher throughput and lower communication overhead」，理由是「TP incurs significant communication overhead because of **all-reduce being performed after every layer**」。**消费卡与 PCIe 工作站卡在多数配置下无 NVLink**，故 T2 的实际可用性远低于其显存总量暗示的水平（**M** 官方警告 · **I** 对本档的推论）。

### 1.4 T3 单节点服务器

| 配置 | 单卡显存 / 类型 / 带宽（官方） | 显存总量 | 中国大陆可采购性（2026-08） | 价格 | 级别 |
| :-- | :-- | --: | :-- | :-- | :-- |
| 4 × L40S | 48 GB GDDR6 ECC，**864 GB/s**，350W | 192 GB | ⛔ 数据中心线 | ⛔ 官方不公布 | **M** 规格 |
| 8 × L40S | 同上 | **384 GB** | ⛔ 同上 | ⛔ 官方不公布 | **M** 规格 |
| 4 × A100 80GB SXM | 80 GB HBM2e，**2039 GB/s**，400W | 320 GB | ⛔ **2022-10 起需许可**；存量合法可继续用 | ⛔ 官方不公布 | **M** |
| 4 × H100 SXM | 80 GB **HBM3**，**3.35 TB/s** | **320 GB** | ⛔ 同上 | ⛔ 官方不公布 | **M** |
| 8 × H100 SXM = **1 台 DGX H100** | 同上 | **640 GB** | ⛔ 断供，仅存量 | ⛔ 官方不公布 | **M**（⭐ 官方文档逐字「8 x NVIDIA H100 GPUs that provide **640 GB total GPU memory**」） |
| 8 × H100 NVL | **94 GB** HBM3，**3938 GB/s** | 752 GB | ⛔ 同上 | ⛔ 官方不公布 | **M** |
| ⭐ **4 × H200 SXM** | 141 GB **HBM3e**，**4.8 TB/s** | ⭐ **564 GB** | ⚠️ 2026-01-15 起 case-by-case；**2026-02 起确有发证，但截至 2026-04-26 收入为零、能否入境未知** | ⛔ 官方不公布 | **M** |
| 8 × H200 SXM = **1 台 DGX H200** | 同上 | **1128 GB** | ⛔ 对华数据中心 Hopper 出货为零 | ⛔ 官方不公布 | **M**（⭐ 官方文档逐字「8 x NVIDIA H200 GPUs that provide **1,128 GB total GPU memory**」） |
| 8 × H20 | ⚠️ 96 GB HBM3（⏳ **待核验**，⛔ 官方数据表未找到） | **768 GB** | ⚠️ 仅存量（2024–2025-04 及 2025-07 后曾合法在华销售，单季销售额曾达 46 亿美元） | ⛔ 官方不公布 | **M**（销售额）· S ⚠️（96 GB 规格） |

⭐⭐ **「4 卡」与「8 卡」都是 NVIDIA 官方认定的形态，本档的分档轴由官方逐字背书**（**M**，本轮核到）：[H100 页](https://www.nvidia.com/en-us/data-center/h100/) 的 Server Options 逐字 `"NVIDIA HGX H100 Partner and NVIDIA-Certified Systems™ with 4 or 8 GPUs"`；[H200 页](https://www.nvidia.com/en-us/data-center/h200/) 逐字 `"NVIDIA HGX™ H200 partner and NVIDIA-Certified Systems™ with 4 or 8 GPUs"`。⭐ **且 4-GPU H200 基板是一个真实 SKU**：[Lenovo Press LP1611](https://lenovopress.lenovo.com/lp1611-thinksystem-sr675-v3-server) 列出 `"ThinkSystem NVIDIA HGX H200 141GB 700W 4-GPU Board"`（⚠️ 该 feature code 于 2026-07-28 标注 withdrawn from marketing），同页 SR675 V3 逐字 `"Supports up to 8x double-wide or single-wide PCIe GPUs or 4x SXM5 GPUs"`。

⛔ **但这两页都只给单卡容量，不给任何聚合总量**——⇒ **564 GB / 640 GB / 1128 GB 这些数字不出自 GPU 产品页**，只能引 DGX 官方 User Guide（见表内）或自行计算（**I**）。⚠️ **对照**：[HGX 页](https://www.nvidia.com/en-us/data-center/hgx/) 对 Blackwell 世代**确实给聚合 Total Memory**（HGX B300 = `"8x NVIDIA Blackwell Ultra SXM"` + `"2.1 TB"`；HGX B200 = `"1.4 TB"`），⛔ **但只列 8-GPU、无 4-GPU 变体**，且 H100 / H200 条目已从该页移除。

⭐ **4×H200 在本档的精确预算**：$V = 564$ GB 标称 → $0.92V = 518.88$ → 扣 20 GB（30K KV 上界）与 12 GB（激活 + CUDA graph + NCCL）→ **权重预算 487 GB**。⛔ 该细算及其能力定位见 [h200x4_envelope.md](./h200x4_envelope.md)，本文不重复。

⛔ **本档的核心事实（NVIDIA 10-Q 逐字，报告期止 2026-04-26，M）**：「**No shipments of Data Center Hopper products to China occurred during the quarter**, compared with $4.6 billion in the first quarter of fiscal year 2026.」以及「we were **effectively foreclosed from competing in China's data center computing/compute market**」。⛔ **即整个 T3 的 NVIDIA 路径在中国大陆 2026 上半年不是「能买到的东西」**，只有存量与国产替代（T5）。来源：[NVIDIA 10-Q（SEC EDGAR）](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000052/nvda-20260426.htm)。

### 1.5 T4a 桌面 / 边缘一体机

| 产品 | 内存（⚠️ 见下方口径警告） | 带宽 | 官方标称可跑 | 价格 | 级别 |
| :-- | --: | --: | :-- | :-- | :-- |
| **新华三 LinSeer MegaCube**（GB10 Grace Blackwell） | **128GB LPDDR5x**（`unified addressing`） | **273 GB/s** | 逐字 `"A single LinSeer MegaCube can support inference for 200B parameter models."` · `"Supports fine-tuning and inference for the Deepseek R1 70B model."` · 双机级联 `"up to 405B parameters, such as Llama 3.1 405B"` | ⛔ **官方页无价**（仅询价入口）；**¥36,999** 为京东挂牌 + 媒体 | **M** 规格 · **S** 价格 |
| **NVIDIA DGX Spark**（GB10） | **128 GB LPDDR5x**，逐字 `"coherent unified system memory"`，256-bit | **273 GB/s** | `"Up to 1 PFLOP FP4"`；GB10 TDP 140 W，整机电源 240 W | ⛔ **官方页无价** | **M** |
| **NVIDIA DGX Station**（Blackwell Ultra） | ⭐ **GPU 252 GB HBM3e** + CPU 496 GB LPDDR5X，概述逐字 `"748 GB of coherent memory"` | GPU **7.1 TB/s** · CPU 396 GB/s · NVLink-C2C 900 GB/s | 整机功耗 1,600 W | ⛔ **官方页无价** | **M** |

⛔⛔ **本档最容易被误用的一条口径**：**MegaCube 与 DGX Spark 的「128 GB」官方措辞是 `unified system memory` / `unified addressing`，⛔ 不是「显存 / VRAM」**——CPU 与 GPU 共享同一池。⚠️ **带宽 273 GB/s vs H200 的 4.8 TB/s 差约 17.6×**，⇒ ⛔ **把它与 HBM 卡按容量横比是错的**（**I**）。同理 **DGX Station 的「748 GB」不是显存**：真 HBM 只有 **252 GB**，其余 496 GB 是 LPDDR5X（396 GB/s）。

⛔ **一条必须记下的产品线更正**：**LinSeer MegaCube 不是训推一体机**，它是**桌面级 GB10 迷你工作站**，与新华三「灵犀 Cube 大模型一体机」（§1.6）**是不同产品线**，⛔ 不可混为一档。规格逐字取自[官方**英文**产品页](https://www.h3c.com/en/Products_and_Solutions/IntelligentTerminalProducts/MegaCube/)——⚠️ **中文页为 JS 空壳，抓取为空**。

⚠️ **「单台 200B」与本文口径的关系只能作弱旁证**：128 GB 的 0.88 预算为 112.6 GB，4-bit 下可容 ~198B 总参——数字接近，但官方未说明精度档与上下文长度，⛔ 不可当成互证（**I**）。

来源：[DGX Spark 官方产品页](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) · [DGX Spark 官方硬件文档](https://docs.nvidia.com/dgx/dgx-spark/hardware.html)（逐字 `"128 GB LPDDR5x unified system memory, 256-bit interface, 4266 MHz, 273 GB/s bandwidth"`）· [DGX Station 官方产品页](https://www.nvidia.com/en-us/products/workstations/dgx-station/)。

### 1.6 T4b 训推一体机（厂商整机）

⛔ **不存在「典型显存」这一个数**——官方与厂商材料给出的是一条跨约 8 倍的连续谱。

| 档位 | 产品 | 显存 | 官方标称可跑 | 价格量级 | 级别 |
| :-- | :-- | --: | :-- | :-- | :-- |
| 入门 | 华为 FusionCube A3000 DS 版 **Lite** = 1 台 Atlas 800 3000（含 4 × Atlas 300I Duo） | **192 或 384 GB LPDDR4X** | 1.5B / 7B / 14B 蒸馏轻量版 | ⛔ 未公开 | 卡规格 **M** · 整机组合 **S** |
| 中档 | 华为 FusionCube A3000 DS 版 **Pro** = 1 × Atlas 800I A2 | ⛔ **官方产品页未公布** | DeepSeek-R1-Distill-Qwen-32B、Llama-70B；70B 3300 token/s、32B 4940 token/s | ⛔ 未公开 | **S** |
| 高档 | 华为 FusionCube A3000 DS 版 **Ultra** = 2 × Atlas 800I A2 | ⛔ 同上未公布（⇒ 1024 GB，**I**） | DeepSeek-R1 / V3 **671B**，1911 token/s | ⛔ 未公开 | **S** |
| 高档 | **浪潮信息 元脑 R1 NF5688G7** | 「**1128GB HBM3e**」，「显存带宽高达 **4.8TB/s**」 | 满足「671B 模型 FP8 精度下不低于 800GB 显存容量的需求」；「单机可支持20-30用户并发」 | ⛔ 未公开 | **M** |
| 高档 | **浪潮信息 元脑 R1 NF5868G8** | 「高达 **1536GB** 显存容量」，「单机支持16张标准PCIe双宽卡」 | 「在FP16/BF16精度下**单机部署DeepSeek 671B模型**」 | ⛔ 未公开 | **M** |
| 软件档 | 浪潮信息 元脑企智 EPAI 一体机（五版本） | ⛔ 未公布 | 内置 7 个主流基础大模型 | 约二三十万至 200 万元（⛔ 媒体转述） | **S** |
| 国产栈 | 中科曙光 DeepSeek 超融合一体机（SothisAI 3.0） | ⛔⛔ **未核定**——**sugon.com 全域不可达**（7 次尝试全部 `Socket is closed`），⛔ **不得写成「官方未公布」** | 10 亿级推理至 1000 亿级训练；适配 DeepSeek-R1-671B | 150–350 万元（⛔ **据头豹研究院测算**，见 §1.9） | **S** |
| 一体机 | **联想万全大模型训推一体解决方案** | ⛔ **官方页加速卡型号、卡数、显存、模型规模、价格五项全无**，只给硬件平台名「联想问天 WA7880a G3、WA5480 G3/G5 等」 | 另一官方页唯一规格性数字：「从 7B 到 671B 满血版本的不同容量参数模型」 | ⛔ 未公开 | **M**（「五项全无」这一否定事实） |
| 多款型 | 新华三一体机（纯享版 / 使能版，六大款型 12 款产品） | ⛔ **官方新闻页不给机箱、卡数与显存** | 「覆盖**14B 至 671B** 规模」；纯享旗舰版 671B「真实并发数＞32@15 Tokens/s」 | ⛔ 未公开 | **M**（款型与并发）· ⛔ 显存未公布 |

**官方可逐字引用的显存数字只有三条**（全表里唯一打开了官方页的）：① 华为 [Atlas 300I Duo 官方规格](https://e.huawei.com/cn/products/computing/ascend/atlas-300i-duo)「LPDDR4X 96GB或48GB」/ 408 GB/s / 280 TOPS INT8 / 150W；② 浪潮 [NF5688G7](https://www.ieisystem.com/about/news/16778.html) = 1128GB HBM3e / 4.8TB/s；③ 同页 NF5868G8 = 「高达 1536GB」。

⭐ **一条结构性事实，本身可引**：**国产一体机的官方材料普遍以「能跑哪个模型 + 并发 / token/s」为售卖口径，⛔ 而不公布显存与卡数。** 华为官方 [Atlas 800I A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800i-a2)的技术规格表逐字含「4U AI服务器」「4 * 鲲鹏920」「32个DDR4内存插槽」「可选NPU全互联机型，整机互联带宽392GB/s」「4个热插拔2.6kW电源模块」，⛔ **通篇不含 NPU 型号、单卡显存、整机显存与算力数值**；新华三[官方新闻页](https://www.h3c.com/cn/d_202502/2356580_30008_0.htm)同样不给机箱、卡数与显存；**联想一体机官方页更是加速卡型号、卡数、显存、模型规模、价格五项全无**（均 **M**）。⇒ **即使拿到官方来源，也无法从官方材料反推某单位买到的具体算力形态**——这是「单位级算力画像不可得」的一条**结构性原因**，而不只是检索不力。**三家厂商（华为 / 新华三 / 联想）独立一致**，⛔ 故这不是个别厂商的习惯。

⚠️ **联想的情形还多一层，值得单独记**：联想在**服务器**层面**公布单卡显存**（141 GB / 94 GB / 80 GB / 48 GB，见 §1.4），⛔ **但从不公布聚合总量**——[Lenovo Press LP1611](https://lenovopress.lenovo.com/lp1611-thinksystem-sr675-v3-server) 全文最接近聚合的只有一句定性话 `"allows for a larger combined memory footprint for bigger batch sizes"`。⇒ ⛔ **本文全表的「显存总量」一列（含 4×H200 = 564 GB）都是按单卡容量×卡数计算的结果，⛔ 不是厂商写下的字**（**I**）。

⚠️ **入门档的档位划分不是显存决定的**（**I**，⛔ 官方未如此表述）：Lite 档 192–384 GB 装得下 70B，但官方把它钉在 1.5B / 7B / 14B——**更可能是 LPDDR4X 的 408 GB/s 带宽不够**，而非容量不足。

⛔ **「一体机」品类的官方地位**：工信部《关于开展普惠算力赋能中小企业发展专项行动的通知》（**工信厅通信〔2026〕14 号**，成文 2026-03-27）逐字把「按需建设部署边缘数据中心、**训推一体机**等边缘算力设施」写进任务，并逐字承认「针对中小企业在**算力获取**、应用落地和能力提升中的**难点**」（**M**，[miit.gov.cn 原文](https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2026/art_58259bfb30924d6bb225b82b66d1008d.html)）。⛔ **该文件不给任何算力数字**，也不说工业单位有多少卡。

### 1.7 T5 国产加速卡节点

| 配置 | 显存总量 | 可采购性 | 价格 | 级别 |
| :-- | --: | :-- | :-- | :-- |
| **1 台 Atlas 800I A2 = 8 × 昇腾 910B（64 GB）** | **512 GB** | ✅ 国产整机；「设计所能买到的最大常规单机」这一档 | ⛔ 无公开价格 | **M**（官方措辞 `Atlas 800I A2 (8*64G)`） |
| **1 台 Atlas A3 节点 = 8 NPU / 16 die（`64GB × 16`）= 2 台 Atlas 800I A2 等效** | **1024 GB** | ✅ 国产；**这正是官方 671B 部署的最低门槛档** | ⛔ 无公开价格 | **M** |
| 8 × Atlas 350（112 GB HBM） | 896 GB | ✅ 国产新一代 | ⛔ 无公开价格 | **M** 规格 · I |

⭐ **本档有官方部署证据，⛔ 这是一条方向上不利于「算力不可得」叙事的事实，必须一起摆出**：**671B MoE 在昇腾上的官方最低门槛是「2 台 Atlas 800I A2（16 × 64 GB = 1024 GB）跑 W8A8」**，且 **MindIE 与 vLLM-Ascend 两条独立路径口径一致**（**M**）。来源：[Ascend ModelZoo DeepSeek-R1 README](https://gitee.com/ascend/ModelZoo-PyTorch/blob/master/MindIE/LLM/DeepSeek/DeepSeek-R1/README.md) · [vllm-ascend Qwen3-Dense.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/tutorials/models/Qwen3-Dense.md)。⛔ **即 671B 级私域部署不需要 CloudMatrix384，两台国产整机就够。**

⛔ **本档的两条硬约束**：① **昇腾不原生支持 FP8**（已被报告的生态瓶颈，见 [hardware_availability.md](./hardware_availability.md) §4.6）——故 §2 表里凡依赖官方 FP8 件的行**在本档不可直接套用**，官方口径是 W8A8 / W4A4；② 官方 issue [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 报告该 1024 GB 配置在实机上会 OOM，即**贴边而非宽裕**（**S**，但在官方仓库内）。

⚠️ **一条与国产卡显存直接相关的管制事实**（**M**）：2024-12-02 生效的 3A090.c 把「当时在产的全部 HBM」纳入管制，BIS 明说目的是 "slow PRC attempts to indigenize advanced AI chip production"。⛔ **故国产卡的显存容量不是纯技术变量，它受 HBM 进口通道约束。**

### 1.8 T6 小集群

| 配置 | 显存总量 | 可采购性 | 级别 |
| :-- | --: | :-- | :-- |
| 2 台 Atlas 800I A2 | **1024 GB** | ✅ 国产（= T5 的 Atlas A3 节点等效） | **M** |
| 4 台 Atlas 800I A2 | **2048 GB** | ✅ 国产 | **M** · I |
| 2 台 8×H100 节点 | 1280 GB | ⛔ 断供，仅存量 | **M** |
| 2 台 8×H200 节点 | 2256 GB | ⛔ 出货为零 | **M** |
| 4 台 8×H200 节点 | 4512 GB | ⛔ 同上 | **M** |
| ⛔ Atlas 900 A3 SuperPoD / CloudMatrix384（384 封装 × 128 GB） | **48 TB**（官方口径） | ⛔ **超大规模云基础设施，非设计所层级** | **M** 显存 |
| ⛔ Atlas 950 SuperPoD（1024 × 96 GB @ 4.0 TB/s） | **96 TB** | ⛔ 同上 | **M** 显存 |

⛔ **SuperPoD 两行不属于本文的分档轴**：它们是**云 / 国家级智算中心**形态，⛔ 不是任何单位「会买一台」的东西。列出只为标明上界，⛔ **严禁用它们论证单位级可得性**。

### 1.9 价格：⛔ 一条否定事实先行

⛔⛔ **NVIDIA 对专业卡与数据中心卡一律不公布价格。** 本轮逐一打开官方产品页与官方 datasheet PDF 核实：**RTX PRO 6000 Blackwell · RTX 6000 Ada · RTX A6000 · L40S · L40 · A100 · H100 · H200 共 8 款，官方页面与 datasheet 全部不含任何美元价格**，购买路径统一是 "Find a Partner" / "Talk with an NVIDIA Partner" / "Buy Now → NVIDIA Marketplace" / footer "Where to Buy"（**M**）。⛔ **DGX 与 HGX 同样不公布任何价格**：[DGX Platform 页](https://www.nvidia.com/en-us/data-center/dgx-platform/)无美元数字，CTA 为 "Talk to Us" / "Get DGX"；[HGX 页](https://www.nvidia.com/en-us/data-center/hgx/)亦无价格。

⇒ **T1 的消费卡档是全表唯一有官方价格的一档**，T2–T6 的价格量级**在官方渠道不可得**（**M** 否定事实）。

| 项 | 官方价格 | 来源 | 级别 |
| :-- | :-- | :-- | :-- |
| GeForce RTX 5090（32 GB） | **$1,999**（2026-01-30 上市） | [GeForce 官方公告](https://www.nvidia.com/en-us/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/) 逐字 "starting at $1,999" · [官方新闻稿](https://nvidianews.nvidia.com/news/nvidia-blackwell-geforce-rtx-50-series-opens-new-world-of-ai-computer-graphics)二次确认 | **M** |
| GeForce RTX 4090（24 GB） | **$1,599**（2022-10-12 上市） | [官方新闻稿](https://nvidianews.nvidia.com/news/nvidia-delivers-quantum-leap-in-performance-introduces-new-era-of-neural-rendering-with-geforce-rtx-40-series) 逐字 | **M** |
| ⭐ **RTX 5090 D v2（中国特供，24 GB）** | ⭐ **「￥16,499 元起」** —— **NVIDIA 中国官网自己标价，页面出现两次** | [nvidia.cn RTX 5090 D v2](https://www.nvidia.cn/geforce/graphics-cards/50-series/rtx-5090-d-v2/)。同页官方逐字：显存「24 GB GDDR7」、位宽「384 位」、CUDA「21760」、加速频率「2.41」GHz、总功耗「575」W、建议系统功率「1000」W | ⭐ **M** |
| RTX 6000D（中国特供，84 GB） | 约 **¥50,000** | ⛔ 二级来源 | **S** |
| 新华三 LinSeer MegaCube（128 GB） | ⛔ **官方页无价**（逐字仅 `"reach out to our sales team for a tailored quote"`）；**¥36,999** = 京东挂牌 + IT之家等媒体 | [官方英文页](https://www.h3c.com/en/Products_and_Solutions/IntelligentTerminalProducts/MegaCube/) | **M**（无价这一事实）· **S**（金额） |
| 浪潮 元脑企智 EPAI 一体机 | ⛔ **官方新闻稿逐字无任何金额、无卡数、无显存**，只给「基础版、标准版、高级版、创新版和集群版五个版本」；约二三十万至 200 万元 = 媒体（数智前线等） | [ieisystem 官方新闻](https://www.ieisystem.com/about/news/15635.html)。⚠️ **该发布是 2024-09/10（2024 中国算力大会，郑州），⛔ 不是 2025 年** | **M**（无价）· **S**（金额） |
| 训推一体机价格谱 | **华为 FusionCube A3000 200–500 万 · 新华三灵犀 Cube 100–400 万 · 中科曙光 150–350 万 · 浪潮元脑 R1 50–200 万 · 云从 80–250 万**；2025 年整体 50–500 万 | ⛔ **据头豹研究院测算**（《2025年中国大模型一体机行业研究》厂商价格对比表，自述数据来源为「专家访谈、企业公告、头豹研究院」），入口 [fxbaogao.com/detail/4952520](https://www.fxbaogao.com/detail/4952520)。⛔ **原报告未逐字读到** | ⛔ **S / 低** |
| 昇腾 Atlas 800I A2 / Atlas 350 / 全部国产卡 | ⛔ **官方与渠道均不挂牌** | [华为官方产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800i-a2)与[昇腾社区服务器页](https://www.hiascend.com/hardware/ai-server)只有「项目咨询 / 查找经销商」；第三方分销全部标「面议」 | **S**（各渠道一致的元事实） |
| ⛔ 网传「昇腾 8 卡整机百万元量级」 | ⛔ **无可靠公开来源** | — | ⛔ 低等级线索，不得引用 |
| 学术测算档位（⚠️ 非厂商价） | RTX 5090-32GB ≈ **$2,000** · A100-80GB ≈ **$15,000**；SME 档「sub-30B deployments are feasible on a **single consumer-grade RTX 5090 ($2k)**」 | [arXiv:2509.18101](https://arxiv.org/html/2509.18101v3) 逐字 | **S**（预印本，⛔ 无正式 venue） |

⚠️ **两条使用限制**：① ⛔ GeForce 产品页的价格模块是**占位符**（`$XXX.00` / `$XXX.XX`），⛔ 不能作为价格来源——上表的 $1,999 / $1,599 取自官方新闻稿与官方公告文章；② ⛔ **arXiv:2509.18101 的价格表是学术测算，⛔ 不是厂商报价**，且它测的是**自己的假设配置**，⛔ 不得说成中国工业企业的实测采购价。

⛔ **两条本轮发现的官方文档漂移，引用时必须标版本**：① **H100 PCIe 已从现行产品页消失**（当前页只有 SXM 与 NVL 两列），其 80 GB HBM2e / 2000 GB/s 只能回 2022 年的 [PCIe Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf) 取；② **HGX H100 / H200 已从 HGX 页移除**（该页现在只有 Rubin NVL8 / HGX B300 / HGX B200），⛔ 且 `dgx-h100/` 与 `dgx-h200/` 两个 URL 均返回 DGX Platform 通用页、页内不提这两款——⇒ **DGX H100/H200 的 640 GB / 1128 GB 只能引 [官方 User Guide](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)，不能引「当前官方产品页」**（**M**）。

⚠️ **另两条「官方页比 datasheet 少信息」的陷阱**：**RTX 6000 Ada 与 RTX A6000 的产品页根本没有带宽行**，960 GB/s 与 768 GB/s **只在 datasheet PDF 里**；RTX PRO 6000 的 1792 GB/s 也不在专业卡总览页上。⛔ 只查产品页会误判为「官方未公布」。⚠️ 而 **RTX 4090 的显存带宽在所访问的 NVIDIA 官方页面上确实没有 GB/s 数字**（只有 384-bit），本文按查无处理，⛔ 不代填。

## 2. 各档可部署模型（4-bit / 8-bit / BF16 三口径）

### 2.1 ⛔ 先读三条口径，否则会误读本节每一个数字

1. ⛔ **「8-bit 档」在本节的含义是「厂商另发的官方 FP8 件，或原生就是 FP8/MXFP8 的发布件」**，⛔ 不是我们自己按 1.06 B/参推算的假想配置。凡用系数推算的一律标 `估`。
2. ⛔ **一批旗舰模型根本没有 BF16 配置**，因为它们**原生发布就是量化的**：gpt-oss 全系（MXFP4）、DeepSeek V3/V3.1/V3.2/R1（FP8）、DeepSeek V4 Pro/Flash（FP4+FP8 混合）、Kimi K2-Instruct（FP8）、K2-Thinking / K2.5 / K2.6 / K2.7（INT4 QAT）、Kimi K3（MXFP4 QAT）、MiniMax M2 全系（FP8）、Mistral 2512/2603 世代（FP8）、Intern-S1-Pro（FP8）。⛔ **给它们编一个「BF16 显存数」是编造一个官方从未发布的配置。**
3. ⛔ **「件的归属」会改变答案。** 同一档下「只按容量」与「必须是模型作者自己发的量化件」是两个不同的天花板；本节凡差异显著处**两个都给**。⚠️ 判定：**作者** = 该模型发布方自己的 HF 组织；**三方** = NVIDIA / AMD / RedHatAI / unsloth / ggml-org 等，⛔ 无论多权威都不是作者。

### 2.2 主表：按显存总量的三口径天花板

| 显存总量 | 所属档 | 预算 $0.88V$ | **4-bit 天花板** | **8-bit（官方 FP8 件）天花板** | **BF16 天花板** |
| --: | :-- | --: | :-- | :-- | :-- |
| **24 GB** | T1 | 21.1 | **~31B**：[GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash) `Q4_K` **18.2**（⚠️ ggml-org 发布，非作者件）。⛔ 只认作者件则为 **21B**：[gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) 原生 MXFP4 **13.8** | **~8B**：[Ministral-3-8B-2512-FP8](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) **10.4** | **8B**：Qwen3-8B **16.4** |
| **32 GB** | T1 | 28.2 | **~36B**：[nvidia/Qwen3.6-35B-A3B-NVFP4](https://huggingface.co/nvidia/Qwen3.6-35B-A3B-NVFP4) **23.4** · Qwen3-32B-AWQ **19.3**（+KV 7.3 = 26.6 ✅） | ~8B（同上） | **8B** |
| **48 GB** | T1 / T2 | 42.2 | **~36B 官方件**：[Qwen3.5-27B-GPTQ-Int4](https://huggingface.co/Qwen/Qwen3.5-27B-GPTQ-Int4) **30.2**。⚠️ 接受系数估算可到 **~49B**（Kimi-Linear-48B-A3B 27.9 估），但**无已发布 4-bit 件** | **~33B**：[Qwen3-32B-FP8](https://huggingface.co/Qwen/Qwen3-32B-FP8) **34.3**（⚠️ +KV 7.3 = 41.6 **极贴边**）· Qwen3-Coder-30B-A3B-FP8 **31.2** 更稳 | **14B**：Ministral-3-14B **27.9**。⛔ Mistral-Small-3.2-24B BF16 的 48.0 **刚好装不下** |
| **64 GB** | T1（昇腾 910B） | 56.3 | **~80B**：[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF) 官方 `Q4_K_M` **48.4** | **~36B**：[Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8) **37.5** | **24B**：Mistral-Small-3.2-24B **48.0** |
| **80 GB** | T3（单卡 H100/A100） | 70.4 | **~117B**：[gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) 原生 MXFP4 **65.2**——**官方逐字背书** "fit into a single 80GB GPU" | 同为 **117B**（⛔ 该模型无 BF16 档） | **32B**：Nemotron-3.5-Lightning-30B-A3B **65.8**（官方明示 1×H100）。⛔ **Qwen3-32B BF16 的 65.5+KV 7.3 = 72.8 装不下** |
| **96 GB** | T1 / T2 | 84.5 | **~128B**：[Ling-3.0-flash-int4](https://huggingface.co/inclusionAI/Ling-3.0-flash-int4) **77.0**（作者件） | **~80B**：[Qwen3-Coder-Next-FP8](https://huggingface.co/Qwen/Qwen3-Coder-Next-FP8) **80.4**（⚠️ +KV 2.8 = 83.2 **极贴边**） | **36B**：Qwen3.6-35B-A3B **71.9** |
| **128 GB** | T4a | 112.6 | **~128B**：Ling-3.0-flash-int4 **77.0** · Ling-3.0-flash-fp4 **70.4**。⛔ Baichuan-M3-235B-GPTQ-INT4（124.5）与 Step-3.7-Flash-NVFP4（124.4）**均超预算** | **~80B**：Qwen3-Coder-Next-FP8 **80.4**。⛔ GLM-4.5-Air-FP8 的权重 **112.6 正好等于预算**，加 KV 5.3 后超，**装不下** | **49B**：Nemotron-Super-49B **99.7** · Kimi-Linear-48B **98.2** |
| **192 GB** | T2 / T3 / T4b | 169.0 | **~235B**：[Baichuan-M3-235B-GPTQ-INT4](https://huggingface.co/baichuan-inc) **124.5**（官方件）· Step-3.7-Flash-NVFP4 **124.4** = 201B。⚠️ DeepSeek-V4-Flash-0731（166.9 + KV 2.5 = 169.4）**超 0.4 GB，极贴边** | **~128B**：Mistral-Medium-3.5-128B-FP8 **133.6** · Ling-3.0-flash-fp8 **128.4** | **80B**：Qwen3-Next-80B-A3B **162.7** · Qwen3-Coder-Next **159.4** |
| **256 GB** | T2（4×910B） | 225.3 | **~353B**：GLM-4.7→4bit **201.2 估** · Qwen3-235B `Q4_K_M` **142.2**（官方）· **DeepSeek-V4-Flash 159.6（原生 FP4+FP8）= 284B** | **~128B**：Mistral-Medium-3.5-128B-FP8 **133.6** · Ling-3.0-flash-fp8 **128.4** = 127.5B · Mistral-Small-4-119B-FP8 **120.9**。⛔ MiniMax-M2.7 FP8（230.1）与 command-a-plus-FP8（225.0 + KV 3.7 = 228.7）**均超** | **111B**：Command A 2025 **222.1** · Llama-4-Scout **217.3** = 109B。⛔ GLM-4.5-Air BF16（220.9 + KV 5.3 = 226.2）**差 1 GB 装不下** |
| **320 GB** | T3（4×80G） | 281.6 | **~480B**：Qwen3-Coder-480B **273.6 估** · Llama-3.1-405B **231.4 估** · Qwen3.5-397B-A17B-GPTQ-Int4 **235.7**（官方件） | **~229B**：MiniMax-M2/M2.5/M2.7 原生 FP8 **230.1** | **127.5B**：Ling-3.0-flash **255.0** · Mistral-Large-2411 **245.2** = 123B。⛔ Hy3-FP8（299.9）超 |
| **384 GB** | T2 / T3 / T4b | 337.9 | **~480B**：Qwen3-Coder-480B **273.6 估**；官方件天花板 **397B**（Qwen3.5-397B-GPTQ-Int4 **235.7**）。⛔ Nemotron-3-Ultra-550B-NVFP4（352.3）与 Mistral-Large-3-NVFP4（403.1）**均超** | **~299B**：[tencent/Hy3-FP8](https://huggingface.co/tencent/Hy3-FP8) **299.9**（+KV 9.8 = 309.7） | **127.5B**：Ling-3.0-flash **255.0**。⛔ Step-3.7-Flash BF16（402.7）与 Command A+ BF16（437.5）均超 |
| **512 GB** | **T5**（1 台 Atlas 800I A2） | 450.6 | **~753B**：GLM-5.x **429.2 估** · **[Mistral-Large-3-675B-NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) 403.1（官方作者件）= 675B** | **~402B**：Llama-4-Maverick-FP8 **416.8** · Qwen3.5-397B-FP8 **406.2** = 397B。⛔ Qwen3-Coder-480B-FP8（482.1）超 | **219B**：command-a-plus BF16 **437.5**（⚠️ +KV 3.7 = 441.2，ratio 0.98 **极贴边**）· Step-3.7-Flash **402.7** = 201B |
| ⭐ **564 GB** | ⭐ **T3（4×H200）** | **487**（主判据） | **675B 作者件**：Mistral-Large-3-675B-NVFP4 **403.1**。**只按容量**则为三方 [nvidia/GLM-5.2-NVFP4](https://huggingface.co/nvidia/GLM-5.2-NVFP4) **464.8**（⚠️ 贴边 + ⛔ NVFP4 内核 Blackwell 原生） | **~480B**：Qwen3-Coder-480B-FP8 **482.1**（⚠️ 余 4.9 GB，**极贴边**）· Qwen3.5-397B-FP8 **406.2** 更稳 | **235B**：Qwen3-235B-A22B **470.2**（余 16.8） · Command A+ **437.5** = 219B |
| **640 GB** | T3（8×80G） | 563.2 | **~753B**：GLM-5.x **429.2 估**；官方件 **675B**（Mistral-Large-3-NVFP4 403.1）。⛔ Kimi-K2-Thinking INT4（594.2）**超 31 GB** | **~480B**：Qwen3-Coder-480B-FP8 **482.1** · Llama-3.1-405B-FP8 **487.2** = 405B。⛔ **DeepSeek-V3/V3.2 FP8（689.5）装不下** | **235B**：Qwen3-235B **470.2** |
| **768 GB** | T3（8×H20） | 675.8 | **~1026B**：Kimi-K2-Thinking INT4 **594.2** · Kimi-K2.6 INT4 **595.2**。⛔ DeepSeek-V4-Pro（864.7 原生 FP4）超 | **~405B**：Llama-3.1-405B-FP8 **487.2**。⛔ Mistral-Large-3-FP8（681.5，**超 5.7**）与 DeepSeek-V3.2-FP8（689.5，**超 15.7**）**都是极贴边的「差一点」，不要当成能跑** | **235B**：Qwen3-235B **470.2**。⛔ GLM-4.7 BF16（716.7）超 |
| **896 GB** | T5（8×Atlas 350） | 788.5 | **~1026B**：Kimi-K2.x INT4 **594–595** · [amd/Kimi-K2.6-MXFP4](https://huggingface.co/amd/Kimi-K2.6-MXFP4) **559.0**（三方） | **~753B**：GLM-5.x-FP8 **756.2** · DeepSeek-V3.x FP8 **689.5** = 671B · Mistral-Large-3-FP8 **681.5** = 675B。⛔ Intern-S1-Pro FP8（919.0）超 | **353B**：GLM-4.7 **716.7**。⛔ Llama-3.1-405B BF16（811.7）与 Qwen3.5-397B BF16（806.8）**均超** |
| **1024 GB** | **T5 / T6**（1 台 Atlas A3 = 2 台 800I A2） | 901.1 | DeepSeek-V4-Pro **864.7**（原生 FP4）· GLM-5.x **429.2 估** = 753B | **~753B**：GLM-5-FP8 **756.2** · **DeepSeek-V3.x FP8 689.5 = 671B——⭐ 这一格有昇腾官方部署证据**（⚠️ 官方口径是 **W8A8** 而非 FP8，见 §2.4） | **405B**：Llama-3.1-405B **811.7** · MiniMax M3 **854.2** · Qwen3.5-397B **806.8** = 397B |
| **1128 GB** | T3（8×H200）/ T4b（NF5688G7） | 992.6 | 几乎全部 4-bit 档。⛔ Kimi K3 MXFP4（1560.9）超 | **~919B**：Intern-S1-Pro FP8 **919.0**。⛔ Kimi-K2-Instruct FP8（1029.2）**装不下** | **480B**：Qwen3-Coder-480B **960.3** · MiniMax-M1 **912.2** |
| **1280 GB** | T6（2 台 8×H100） | 1126.4 | **1026B**：Kimi-K2.x INT4 **594–595**。⛔ Kimi K3 MXFP4（1560.9）**超 434.5 GB** | **1026B**：Kimi-K2-Instruct FP8 **1029.2** | **353B**：GLM-4.7 **716.7**。⛔ Mistral-Large-3 BF16（1352.0）超 |
| **1536 GB** | **T4b（浪潮 NF5868G8）** | 1351.7 | ⚠️ 系数估算上限 **~2371B**；实测最大实例 **1026B**（Kimi-K2.x INT4 595.2）。⛔ **Kimi K3 MXFP4（1560.9）仍超 209 GB** | **1026B**：Kimi-K2-Instruct FP8 **1029.2**。⛔ Qwen3.8-FP8（2496.1）超 | **550B**：Nemotron-3-Ultra-550B-A55B **1121.1**。⛔ **Mistral-Large-3 BF16 的 1352.0 差 0.3 GB 装不下**——本表最极端的「差一点」 |
| **2048 GB** | T6（4 台 Atlas 800I A2） | 1802.2 | **⭐ 2.8T 总参**：[Kimi K3](https://huggingface.co/moonshotai/Kimi-K3) MXFP4 QAT **1560.9**（本表首次装下它的一档）· Qwen3.8-2.4T 4-bit **1394 估** | **1026B**：Kimi-K2-Instruct FP8 **1029.2**。⛔ Qwen3.8-FP8（2496.1）超 | **753B**：GLM-5.x **1506.7** · Mistral-Large-3 **1352.0** = 675B |
| ⛔ **超出本文全部档** | ⛔ — | — | ⛔ **无**：已知开放权重模型的 4-bit 档在 2048 GB 处全部装下（最大即 Kimi K3 的 1560.9） | ⛔ Qwen3.8-2.4T-A95B-FP8 **2496.1**，需 ≥ **2836 GB** 标称 | ⛔ Qwen3.8-2.4T-A95B BF16 **4892.4**，需 ≥ **5560 GB** ≈ **70 张 80 GB 卡** |

### 2.3 逐档的一句话答案

| 档 | 该档能跑的**最大**开源模型（按总参，取有已发布件的实例） |
| :-- | :-- |
| **T1 单卡 24 GB** | **GLM-4.7-Flash 31B**（`Q4_K` 18.2，⚠️ 非作者件）；作者件天花板 **gpt-oss-20b 21B** |
| **T1 单卡 64 GB（昇腾 910B）** | **Qwen3-Coder-Next 80B**（官方 `Q4_K_M` 48.4） |
| **T1 单卡 96 GB** | **Ling-3.0-flash 127.5B**（官方 INT4 77.0） |
| **T2 双卡 48 GB** | **Qwen3.5-27B**（官方 GPTQ-Int4 30.2）；系数估算可到 ~49B 但无件 |
| **T2 四卡 96 GB** | **Ling-3.0-flash 127.5B** |
| **T2 四卡 384 GB（4×RTX PRO 6000）** | **Qwen3.5-397B-A17B**（官方 GPTQ-Int4 235.7） |
| **T3 4×80 GB（H100/A100）** | **Qwen3-Coder-480B**（273.6 估）；官方件 **Qwen3.5-397B** |
| ⭐ **T3 4×H200（564 GB）** | ⭐ **Mistral-Large-3-675B**（官方作者件 NVFP4 **403.1**，余 84 GB）。只按容量则 **GLM-5.2**（三方 NVFP4 464.8，⚠️ 贴边 + Blackwell 内核风险） |
| **T3 8×80 GB（640 GB）** | **Mistral-Large-3-675B**。⛔ Kimi-K2-Thinking 超 31 GB |
| **T3 8×H200（1128 GB）** | **Kimi-K2.x 1026B**（官方 INT4 QAT **595.2**）· 8-bit 档 **Intern-S1-Pro**（FP8 919.0）· BF16 档 **Qwen3-Coder-480B**（960.3） |
| **T4a 128 GB 桌面机**（MegaCube / DGX Spark） | **Ling-3.0-flash 127.5B**（官方 INT4 77.0）。⚠️ 带宽仅 273 GB/s，⛔ 容量同档不等于可用 |
| **T4a DGX Station（252 GB HBM3e）** | 预算 $0.88 \times 252 = 221.8$ ⇒ **Qwen3-235B**（官方 `Q4_K_M` **142.2**）· DeepSeek-V4-Flash（原生 159.6）= 284B（**I**，本文按同一口径外推，⛔ 无官方部署背书） |
| **T4b 浪潮 NF5688G7（1128 GB）** | 同 8×H200 档 |
| **T4b 浪潮 NF5868G8（1536 GB）** | **Kimi-K2-Instruct 1026B**（FP8 1029.2）· BF16 档 **Nemotron-3-Ultra-550B** |
| **T5 1 台 Atlas 800I A2（512 GB）** | **Mistral-Large-3-675B**（NVFP4 403.1）——⚠️ **但昇腾不原生支持 FP8/NVFP4，见 §2.4** |
| **T5 1 台 Atlas A3（1024 GB）** | **DeepSeek-V3.x 671B**——⭐ **本表唯一有硬件厂商侧官方部署教程的格子**（W8A8，MindIE 与 vLLM-Ascend 两条独立路径口径一致）。⚠️ 模型作者侧的容量背书是另一类证据，见 80 GB 档的 gpt-oss-120b |
| **T6 4 台 Atlas 800I A2（2048 GB）** | ⭐ **Kimi K3，2.8T 总参**（MXFP4 QAT 1560.9） |

### 2.4 ⛔ 四条会让上表失效的陷阱

1. ⛔ **昇腾（T5）不原生支持 FP8。** 已被报告的生态瓶颈（见 [hardware_availability.md](./hardware_availability.md) §4.6）。⇒ 上表 512 / 1024 / 896 GB 三格的 **8-bit 列不可直接照搬**，昇腾官方口径是 **W8A8 / W4A4**，而 671B 的官方门槛正是 W8A8。同理 NVFP4 / MXFP4 件在昇腾上的内核路径**未核**。
2. ⛔⛔ **NVFP4 / MXFP8 内核是 Blackwell 原生，而 H100 / H200 是 Hopper（cc 9.0）。** [Motif-3-NVFP4](https://huggingface.co/Motif-Technologies/Motif-3-NVFP4) 的 card 逐字「NVFP4 requires NVFP4-capable hardware (NVIDIA Blackwell / B200)」——**该件在 T3 的 Hopper 档整体失效**。⇒ 上表凡 NVFP4 行在 T3 上都带这个风险，⛔ 包括 4×H200 那一格的 GLM-5.2（其 card 只写 "Test Hardware: B200"）。详见 [h200x4_envelope.md](./h200x4_envelope.md) §4.3。
3. ⛔ **贴边格子不可据以选型。** 上表标 ⚠️ 极贴边的格子（Qwen3-32B-FP8 @48 GB、Qwen3-Coder-Next-FP8 @96 GB、Qwen3-Coder-480B-FP8 @564 GB、command-a-plus @512 GB）余量均 < 5 GB，而官方 issue [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 已实测 1024 GB 上 OOM 一例——**真实常驻开销比 0.88 重**。
4. ⛔ **「多买一张卡」补不上的差距是存在的。** AA-LCR 前八名的开放权重模型里有三个（Kimi K2.6 · K2.7-Code · Inkling）**已经是官方最小精度档、没有降级余地**：K2.6 需 ≥ 681.7 GB 标称（≥ 5 张 H200），Inkling 需 ≥ 666.8 GB。⇒ 它们**恰好卡在常规节点形态之间的空隙里**：4×H200（预算 487）不够、**需 ≥ 5 张**，即只能上 8 卡节点——而 8 卡档在中国大陆的 NVIDIA 路径已断供；国产侧则是 1 台 Atlas 800I A2（预算 450.6）不够、**2 台才够**（**I**，算术见 [h200x4_envelope.md](./h200x4_envelope.md) §1.3）。

## 3. 出口管制对各档的影响

### 3.1 逐档裁定

| 档 | 中国大陆能否买到（2026-08） | 裁定依据 | 级别 |
| :-- | :-- | :-- | :-- |
| **T1 消费 / 工作站卡（24 GB）** | ✅ **能买到，且是唯一明确无争议的一档** | NVIDIA 10-Q 逐字：「we were able to **ship uncontrolled products to China, such as gaming and workstation GPUs**」 | **M**（类别）· S（具体型号与容量） |
| **T1 中国特供大显存工作站卡（RTX 6000D，84 GB）** | ⚠️ **状态不明**——曾在售，据报市场失败并被中方禁 / 劝退，⛔ **该判定的官方依据至今未找到** | 同上 10-Q 把 "workstation GPUs" 列进可出货类别；⛔ 禁售一侧只有二级报道 | S ⚠️ |
| **T1 全球版大显存工作站卡（RTX PRO 6000 96 GB / RTX 5090 32 GB）** | ⛔ **非中国版**；灰市有 | 规格未通过 3A090 Note 2 的豁免路径（TPP / performance density / 带宽门槛） | S · I |
| **T2 多卡消费卡工作站** | ✅ **能买到**（= T1 卡的多份），⛔ **但多数配置无 NVLink** | 同 T1 | **M** 类别 · **I** 互联推论 |
| **T3 A100 / H100 / A800 / H800 节点** | ⛔ **买不到。** 2022-10-07 起 A100/H100 需许可；**2023-11-17 起降级版 A800 / H800 一并落网** | Federal Register 原文（经 govinfo.gov 逐字核） | **M** |
| **T3 H20 节点（8×96 GB = 768 GB）** | ⚠️ **只有存量。** 2024–2025-04 及 2025-07 后曾合法在华销售（单季 46 亿美元），2025-04-09 起需许可；据报被中方劝退 / 禁于国家资金数据中心 | NVIDIA 申报（销售额，**M**）· 中方禁令（**S** ⚠️，Reuters 双匿名消息源） | **M** / S ⚠️ |
| ⭐ **T3 H200 节点（含 4×H200）** | ⚠️ **名义放宽、实际未落地。** 2026-01-15 起 case-by-case 放宽（TPP<21000 **且** DRAM 带宽<6500 GB/s）；2026-02 起 USG 确有发证；⛔ **但截至 2026-04-26 收入为零、能否入境未知**；且 2026-01-14 据报中方拦下 H200 入境 | 10-Q 逐字：「To date, we have **not generated any revenue** under the H200 licensing program, and **do not yet know whether any imports will be allowed into China**」 | **M** / S ⚠️（中方拦下） |
| **T3 B200 / GB200 / GB300 节点** | ⛔ **买不到。** 超 21000 TPP / 6500 GB/s 门槛，不符合放宽条件 | 按官方阈值验算 | **I** |
| **T4a/T4b 训推一体机（国产栈）** | ✅ **能买到，且被官方文件点名推荐** | 工信厅通信〔2026〕14 号逐字把「训推一体机」写进任务 | **M** |
| ⚠️ **T4b 用 NVIDIA 卡的一体机（如浪潮 NF5688G7 1128GB HBM3e）** | ⚠️ **取决于其用的是哪种卡。** 1128 GB HBM3e = 8×141 GB，即 H200 档；⛔ 该整机在中国大陆的现实可得性受 T3 的同一条约束 | ⛔ 浪潮官方新闻页不点卡型；1128 GB HBM3e 对应 8×H200 是**本文推断** | **M**（显存数字）· **I**（卡型推断） |
| **T5 国产加速卡节点（昇腾 Atlas 800I A2 / A3）** | ✅ **能买到，且中方对国家资金项目实为强制** | 据报 2025-11 起国家资金数据中心只用国产芯片 | **M**（产品存在）· S ⚠️（强制一侧） |
| **T6 小集群** | ⛔ NVIDIA 路径同 T3（买不到）· ✅ **国产路径可行**（多台 Atlas 800I A2） | 同上 | **M** / S ⚠️ |

### 3.2 归纳成三句话

1. ⛔ **「买不到」的是 T3 的全部 NVIDIA 数据中心档**（A100 / H100 / A800 / H800 / H20 新增 / B200 系），以及 T1/T2 的全球版大显存工作站卡。**最硬的一条证据是 NVIDIA 自己的季报**：「**No shipments of Data Center Hopper products to China occurred during the quarter**」（期止 2026-04-26，**M**）。
2. ⚠️ **「只能买降级版」的是 T1 的消费卡档。** 合规路径是把**带宽与 AI TOPS 压到 3A090 Note 2 的门槛下**——RTX 5090D V2 把带宽从 1792 压到 1344 GB/s、AI TOPS 从 3352 压到 2375、**显存从 32 GB 砍到 24 GB**（**S**）。⇒ **降级的代价直接落在显存上**，这是 T1 的 24 GB 上限的由来（**I**）。
3. ✅ **「只能用国产卡」的是 T5 与国家资金项目下的 T3/T6。** 若 2025-11 的报道成立，任何拿国家资金的数据中心项目只许用国产 AI 芯片（**S** ⚠️），而型号研制单位 / 设计所正是这类主体（**I**）。

### 3.3 ⛔ 四条方向相反的事实，不得省略

⛔ **按 [talks/GUIDE.md](../../../../talks/GUIDE.md) §9 的方向性松紧一致原则，不利于「算力不可得」一侧的证据同样要写满。**

1. ⛔ **管制管出口，不管存量使用。** BIS 2026-05-31 指南逐字确认 bona fide 数据中心运营方**不因该指南被要求停止**已有先进计算项目的 use / storage / disposal / servicing（**M**）。A100 在 2022-10 前对华自由销售多年，**存量是合法的**（**I**）。
2. ⛔ **存量里确实有 > 640 GB 的节点。** 一台 8×H20 = 768 GB，4-bit 下 ~1186B，**比 8×80 GB H100 节点还宽**（**I**；⏳ 依赖 H20 = 96 GB 这个**待核验**数字）。⇒ **「中国工业单位不可能有 640 GB 级节点」是错的。**
3. ⛔ **671B MoE 在国产生态上有官方成功部署，门槛只有两台整机。** ⇒ 「国产卡跑不了大 MoE」是错的；「跑得了但要 384 卡超节点」也是错的。
4. ⛔ **32B 档在昇腾上是官方一等公民。** Qwen3-32B 的 BF16 / W8A8 / W4A4 均**单节点即可**，Atlas 300I Duo 用 W8A8SC + TP4 都有官方教程（**M**）。⇒ 「国产卡跑不了这一档」是错的。

**合起来的诚实表述**：**约束不在「显存买不到」，而在「以什么身份、走什么渠道、在什么合规前提下买」**（**I**）。

## 4. 哪一档最常见

### 4.1 分层答案：⛔ 企业侧查无严谨统计，⭐ 但存在两条可引的公开硬件配置分布

⛔ **「**工业企业**私有化部署实际用哪一档」至今查无严谨统计**——本目录已核过两轮（[hardware_availability.md](./hardware_availability.md) §5、[industrial_compute_evidence.md](./industrial_compute_evidence.md) §2–§5），本轮第三次复核，该结论不变。⛔ 具体地：

1. ⛔ **不存在**「X% 中国工业企业已私有化部署 LLM」或「工业企业平均可用 X 张卡」这类权威口径。官方只有**政策目标句**（工信部 14 号文：「显著降低中小企业获取、使用算力门槛」）与**国家级宏观总量**（信通院：788 EFLOPS FP16、1085 万标准机架、2.1 万张推理卡）——⛔ **中间那一层，单位级算力画像，是空的。**
2. ⛔ **IDC / Gartner / Forrester 的 on-prem 硬件档位拆分不存在。** 一个研究聚合页自己就标注了这个缺口：「no new 2025-2026 surveys from Gartner, Forrester, or IDC specifying on-premises splits」。
3. ⛔ **军工 / 航天 / 涉密单位的本地 LLM 部署实证：零篇可引学术文献。** 全部命中都是技术博客、厂商方案页或安全内参。
4. ⛔ **RE 领域零命中**「因保密只能本地部署」的工业案例。
5. ⛔ **「工业单位只能本地部署，而本地算力只有 X」这句完整表述，没有任何来源把两半话说全。** 隐私那一半到处都有；算力那一半**只出现在基准 / 测算论文自己的配置表里**，而那些论文测的是**自己的实验机**，⛔ 不是任何真实工业单位的存量。

⛔ **严禁用国家级聚合量论证单位级可得性**——本目录已因此栽过一次（[revision_log.md](./revision_log.md)）。⛔ 也**不得反过来断言「工业单位普遍只有单卡」**，那句话同样没有来源。

⭐ **但本轮找到了两条真实、官方一手、机读可复算的公开硬件配置分布**（§4.2）。⛔ **二者都不是企业侧样本**，只能作为**上下界参照**：MLPerf 是「厂商愿意展示的上限」，Hugging Face 自报是「个人开发者的实际下限」。⇒ ⛔ **原先那句一刀切的「查无来源」应按本节分层表述，不得再简写成一句。**

### 4.2 ⭐ 两条真实可引的公开硬件配置分布（⛔ 均非企业侧）

#### 4.2.1 MLPerf Inference（MLCommons）——⭐ 机读、Apache-2.0、含显存字段

[结果页](https://mlcommons.org/benchmarks/inference-datacenter/) 的 Closed division 有 `Accelerator and Count` 列，⛔ **但该页本身不列显存**。显存在 **per-submission 的 `system_desc` JSON** 里，字段名为 `accelerator_memory_capacity`，本轮逐字核到三例（均 **M**）：

| 提交 | 逐字字段 |
| :-- | :-- |
| [v5.1 NVIDIA `B200-SXM-180GBx8_TRT.json`](https://raw.githubusercontent.com/mlcommons/inference_results_v5.1/main/closed/NVIDIA/systems/B200-SXM-180GBx8_TRT.json) | `accelerator_memory_capacity` **"180 GB"** · `accelerator_memory_configuration` "HBM3e" · `accelerators_per_node` **8** · `host_memory_capacity` "2 TB" · `system_type` "datacenter" |
| [v6.0 Lenovo `SR680aV4.json`](https://raw.githubusercontent.com/mlcommons/inference_results_v6.0/main/closed/Lenovo/systems/SR680aV4.json) | "ThinkSystem SR680a V4 (8x B300-SXM-270GB, TensorRT)" · `accelerator_memory_capacity` **"270 GB"** · 8 卡 · host "3 TB" |
| v6.0 Lenovo `SE100.json` | "ThinkEdge SE100" · `accelerator_model_name` "N/A" · `accelerators_per_node` **"0"** · `accelerator_memory_capacity` "N/A" · `system_type` **"edge"** ⇒ ⭐ **edge 分区存在纯 CPU 提交** |

最新轮次 **v6.0**（[repo](https://api.github.com/repos/mlcommons/inference_results_v6.0) 建于 2026-03-26、末次 push 2026-05-03），closed 分区 **24 家提交方**（AMD / ASUSTeK / Cisco / CoreWeave / Dell / GATEOverflow / GigaComputing / Google / HPE / Intel / Krai / Lambda / Lenovo / MangoBoost / MiTAC / NVIDIA / Nebius / Netweb / ORACLE / Quanta / RedHat / Supermicro 等）；上一轮 [v5.1 公告](https://mlcommons.org/2025/09/mlperf-inference-v5-1-results/)（2025-09-09，27 家）。

⛔⛔ **适用边界，必须与数字一起引用**：**提交方是厂商与云商，⛔ 不是企业用户**；NVIDIA 在 v6.0 只送 B200 / B300 / GB200 / GB300，**全是当代旗舰，分布严重偏高端**。⇒ 它支撑「送测系统的显存配置分布」，⛔ **不支撑「企业实际买了哪一档」**。

⏳ **本轮只抽样 3 份，未做全量分布。** 复算路径已确认可行：遍历 `closed/*/systems/*.json` 取 `accelerator_memory_capacity` × `accelerators_per_node`，schema 跨 v5.1 / v6.0 一致，许可 Apache-2.0。

#### 4.2.2 Hugging Face 自报本地硬件（n = 297,135）——⭐ 本轮最有价值的发现

来源：[huggingface.co/blog/clem/hardwaresetupsonhf](https://huggingface.co/blog/clem/hardwaresetupsonhf)，`"Published May 6, 2026"`，作者 handle `clem`（⚠️ **页面本身不写全名，本文不断言其身份**）。配套数据集 [clem/100_most_popular_hardware_setups_on_HF](https://huggingface.co/datasets/clem/100_most_popular_hardware_setups_on_HF)，**Apache-2.0**，快照日 `"Thursday, April 30, 2026"`。

逐字（均 **M**）：

- `"297,135 users who voluntarily filled in the local hardware section of their HF profile"`；`"The top 100 setups only cover 47% of all 297,135 reporters."`
- ⭐ `"The single most popular discrete GPU isn't the 4090 or the 5090 — it's the RTX 3060 at 4,737 users"`
- top-100 共 140,141 份报告的分桶（方法学致谢 `"Jordan Nanos at SemiAnalysis"`）：**discrete GPU 60,120（43%）· SoC/APU 50,077（36%）· CPU-only 17,841（13%）· combo 12,103（8.6%）**
- ⛔ **数据中心卡占比极低**：H100 / A100 / H200 / V100 / T4 / L4 / L40s / RTX 6000 Ada / RTX PRO 6000 WS / A6000 / GB10 **合计 `"10,792 users"`**，即 `"~7.7% of top-100 reports"`（⚠️ 作者自述被低估，因共享集群卡通常不写进个人 profile）。GB10（DGX Spark）排 **#36、1,241 人**
- Top 6：Apple M4 6,377 · Apple M4 Pro 6,207 · Apple M1 Pro 4,815 · **NVIDIA RTX 3060 4,737** · Apple M1 4,499 · **NVIDIA RTX 4090 4,398**

⛔⛔ **官方自述的边界，必须一起带走**：`"The data is self-reported and opt-in (biased toward HF-engaged local-AI builders)"`；用户通常只填一台机器；云与集群被低估；各厂商标签粒度不一。⇒ 它是**个人开发者本地机器的便利样本**，⛔ **不是企业私有化部署**。可支撑「社区侧本地推理主要跑在 12–24 GB 消费卡与 Apple 统一内存上」，⛔ **不可支撑「企业用哪一档」**。

⭐ **这条与 §4.3 的学术分布相互独立却同向**：两者的众数都落在**消费级单卡**，⛔ 但两者都不是工业单位样本，**同向不构成对企业侧的证明**。

#### 4.2.3 ⛔ 两条确认不存在的

1. ⛔ **Stack Overflow Developer Survey 无本地 / 硬件题。** [2025 版](https://survey.stackoverflow.co/2025/) 首次加入 LLM 题，但是**使用**题（`"Which LLM models for AI tools have you used for development work in the past year…"`），⛔ 无本地 vs API 拆分、无 GPU / VRAM 题（规模 49,000+ 份 / 177 国 / 62 题）。[2026 版已开放但结果未发布](https://stackoverflow.blog/2026/06/23/the-2026-developer-survey-is-now-open-for-human-developers-only/)；⭐ 问卷本体已公开在 [github.com/StackExchange/Survey](https://github.com/StackExchange/Survey)，**可事前查有无硬件题，不必等结果**。
2. ⛔ **Ollama 无官方遥测或硬件统计。** 流传的「按 pull count 推断 7B–8B 档占优」是第三方博客解读，⛔ 不可引。

### 4.3 ⚠️ 学术论文自报硬件（⛔ 不是工业界分布）

⚠️ **以下是文献实践分布，n = 10，来自 [hardware_availability.md](./hardware_availability.md) §6.2 的逐字核验表**（SE / MDE / RE 及邻近领域，明确以算力可得性而非隐私作为选小模型理由的论文）。⛔ **它回答的是「研究者在什么硬件上做实验」，⛔ 不回答「工业单位有什么硬件」。**

| 显存档 | 论文数 | 具体 |
| :-- | --: | :-- |
| **单卡 24 GB** | **4** | RTX A5000 24GB（TOSEM'25 #204）· RTX 3090 24GB（AI-SQE'26）· L4 24GB + RTX 3090 24GB（JSS 236:112815）· RTX 4090 24GB（JSS 230:112574） |
| 单卡 6–8 GB | 2 | RTX 4050 6GB（REFSQ'26）· RTX3070 8GB（MSR'25，同文另有 A100 80GB） |
| 单卡 80 GB（A100 / H100） | 2 | A100 PCIe 80GB（MSR'25）· H100（arXiv:2604.06946，Azure ML，⛔ 非受限） |
| 双卡 48 GB | 1 | 2 × L40S 48GB（InstruBPM） |
| 8 × 40 GB | 1 | 8 × A100 40GB（TOSEM'25 #78，⛔ 非受限） |
| ⛔ 未给出 | 1 | arXiv:2605.15865（只写 "quantized versions (e.g., GGUF)"） |

⚠️ **上表各行相加为 11 而非 10**：MSR'25 那一篇同时报告了 laptop RTX3070 8GB 与 A100 PCIe 80GB 两台机器，**在两行里各计一次**。⛔ 不是统计错误，但引用时必须说明。

⭐ **众数是单卡 24 GB（4/10）**，且**本批最强的承重论文用的正是这一档**——Weyssow et al., TOSEM 2025 把算力约束做成独立成节的组织轴，逐字：「a software engineer with access to only a **single consumer GPU (e.g., 24GB of VRAM)** may find full fine-tuning impractical」（**M**）。

⚠️ **三条必须随这张表带走的限定**：① **n = 10，且是本目录按「以算力为理由」这一条件筛出来的**，⛔ 不是该领域论文的随机样本，⛔ 存在选择偏差；② 它反映的是**学术实验机**，而学术实验机与工业存量之间**没有任何已核验的对应关系**；③ 表内 3 篇（8×A100、单卡 H100、A100 80GB）**自身就不是受限配置**，⛔ 把它们算进「受限档」是错的。

### 4.4 ⚠️ 一条元事实：为什么企业那一层查不到，不只是检索不力

⭐ **国产一体机的官方材料普遍以「能跑哪个模型 + 并发 / token/s」为售卖口径，⛔ 而不公布显存与卡数**（华为 Atlas 800I A2 官方页、新华三官方新闻页、联想一体机官方页**三家独立一致**，均逐字核实，**M**，见 §1.6）。⇒ **即使拿到了官方来源，也无法从官方材料反推某单位买到的具体算力形态。** 这是「单位级算力画像不可得」的一条**结构性原因**（**I**），⛔ 而不只是我们检索不到。

⭐ **另一条结构性原因**：唯一测到**部署数量**的全球实测研究（[arXiv:2505.02502](https://arxiv.org/abs/2505.02502)）测的是**公网可达**的自托管 LLM 服务（320,102 个，中国 56,593 个），严格说它是「**暴露面**」而非「部署量」——⛔ **真正的企业内网部署恒不在其样本内**。这既是它的局限，也恰好说明**内网部署规模不可测**。

⭐ **把三条合起来看，§4.2 的两条分布为什么必然测不到企业**：**MLPerf** 的样本是**自愿送测的厂商**（愿意公开配置的正是想卖机器的人）；**HF 自报** 的样本是**opt-in 的个人 local-AI builders**（企业机器不写在个人 profile 里，作者自己也说共享集群卡被低估）；**arXiv:2505.02502** 的样本是**公网暴露面**（内网部署恒不可见）。⇒ ⛔ **三条各自的采样机制都系统性排除企业内网**——这不是三次巧合，⛔ **企业侧的空白是结构性的，不是等更多调查就能填上的**（**I**）。

## 5. 待核验与访问受限

### 5.1 ⛔ 对结论有影响的缺口（按影响排序）

| # | 缺口 | 影响哪一格 | 现状 |
| --: | :-- | :-- | :-- |
| 1 | **H20 = 96 GB** 的官方数据表 | T3 的 768 GB 档，以及 §3.3 第 2 条「存量里有 > 640 GB 节点」这条反向论据 | ⛔ **NVIDIA 官方数据表未找到**；只有聚合站、经销商页、百科（**S**） |
| 2 | **RTX 6000D（84 GB）被中方禁 / 劝退** 的官方依据 | T1 的 84 GB 档可采购性判定 | ⛔ **至今未找到**（登记于 [hardware_availability.md](./hardware_availability.md) §7.2 第 10 条） |
| 3 | **训推一体机的显存与卡数** | T4b 全档 | ⛔ **华为 Atlas 800I A2、新华三一体机的官方页均确认「未公布」**——这是**已核实的否定事实**，不是未核（**M**） |
| 4 | **昇腾 910B1/B2/B3 = 64 GB、B4 = 32 GB 的分档表** | T1 / T5 的单卡容量 | ⏳ 仅见 CSDN / 云厂商文档 / 知乎，⛔ **无华为官方分档表** |
| 5 | **NVFP4 / MXFP4 件在昇腾上的内核路径** | §2.4 第 1 条，T5 的 4-bit 列 | ⏳ 未核 |
| 6 | **DeepSeek-V4-Flash 的 FP4 部分在 Hopper 上的内核路径** | 4×H200 那一格的首选件 | ⏳ 未核（登记于 [h200x4_envelope.md](./h200x4_envelope.md) §6.1） |
| 7 | **浪潮 NF5688G7 的 1128GB HBM3e 用的是哪种卡** | §3.1 该行的可采购性 | ⛔ **官方新闻页不点卡型**；「= 8×H200」是本文推断（**I**） |
| 8 | **RTX 4090 的显存带宽（GB/s）** | T1 表 | ⛔ 所访问的 NVIDIA 官方页面均无该数字（只有 384-bit），本文按查无处理 |
| 9 | 寒武纪 590/690、海光 DCU、壁仞在产品线、摩尔线程 S5000 的显存 | T1 国产卡行 | ⛔ **官方未公布**或**查无官方来源** |
| 10 | 结构化输出 × 量化档的退化数据 | ⛔ 影响全部 4-bit 列对本项目负载的适用性 | ⛔ **公开文献零数据**（真实空白，非漏检；见 [h200x4_envelope.md](./h200x4_envelope.md) §3.4）——**只能自测** |
| 11 | ⛔⛔ **中科曙光官方是否公布显存：未核定** | §1.6 曙光行 | ⛔ **sugon.com 全域不可达**，实际尝试 6 个 URL（`/cut?id=2547`、`/product/lists?category_id=27` 的 https 与 http、`/solution/details?id=211`、站点根）+ Bash `curl`，**7 次全部 `Socket is closed`**。⛔ **故不得写成「官方未公布」**——这是**访问失败**，不是否定事实。搜索层见到产品线 X785-G30 / X795-G30 / W760-G30 / X745-G30 与 SothisAI 3.0，⛔ 摘要中无任何显存数字（**S**） |
| 12 | **MLPerf Inference 的全量显存分布** | §4.2.1 | ⏳ **schema 与入口已确认（M），但只抽样 3 份，未做全量遍历。** 复算路径：遍历 `closed/*/systems/*.json` 取 `accelerator_memory_capacity` × `accelerators_per_node`，Apache-2.0 |
| 13 | Lenovo Press LP1611 的 GPU adapters 完整表格 | §1.4 单卡显存列表的完整性 | ⏳ 抓取被截断，未逐字读全；如需完整列表应取 [lp1611.pdf](https://lenovopress.lenovo.com/lp1611.pdf) |
| 14 | RTX 5090D（**老款 32 GB**）的 nvidia.cn 官方标价 | §1.9 | ⏳ 未单独核（媒体称同为 ¥16,499，**S**）。⚠️ ⛔ **不要与已核到官方价的 5090 D **v2**（24 GB）混为一条** |
| 15 | 头豹研究院《2025年中国大模型一体机行业研究》原报告 | §1.9 的一体机价格谱（含曙光 150–350 万） | ⏳ **只见搜索摘要，原报告未逐字读到**。⛔ 引用前须取原件 |
| 16 | HF 硬件博客作者 `clem` 的真实身份 | §4.2.2 的来源署名 | ⛔ **页面本身不写全名**，本文只记 handle，⛔ 不断言身份 |

### 5.2 ⛔ 访问受限与文档漂移记录

1. ⛔ **`federalregister.gov` 与 `ecfr.gov`** 对本机直连返回 **302 → `unblock.federalregister.gov`**，故管制条款改用 **govinfo.gov** 的官方 Federal Register HTML 全文。⚠️ **口径后果**：本文（及 [hardware_availability.md](./hardware_availability.md)）给出的是「各 IFR 当时颁布的文本」，⛔ **不是 eCFR 现行合并文本**。
2. ⛔ **`resources.nvidia.com` 的两个 datasheet 入口取不到**：`en-us-tensor-core/...` **302 跳回 `nvidia.com/`**；`en-us-hopper-architecture/...` 返回 200 但**被 cookie 同意横幅挡住，正文只有 cookie 提示**。
3. ⛔ **`marketplace.nvidia.com` 两个 URL 均 60 秒超时**，未取到任何内容——故「NVIDIA Marketplace 上是否有 RTX PRO 6000 的标价」**本轮未能核实**。
4. ⚠️ **官方文档已漂移（详见 §1.9）**：H100 PCIe 从现行产品页消失；A100 的 40 GB 两档规格行已从产品页移除（只能回 2021-06 的 datasheet PDF）；HGX H100/H200 从 HGX 页移除；`dgx-h100/` 与 `dgx-h200/` 两个 URL 返回通用页。⇒ ⛔ **引用这些数字必须标文档版本与日期，不能写成「当前官方页」。**
5. ⛔ **中文学术库（CNKI / 万方 / 维普）本轮无法访问**，故 §4 的「军工 / 涉密单位本地部署」方向仍是零覆盖，⛔ 不能据此断言该方向的文献不存在。
6. ⛔⛔ **`sugon.com` 全域不可达**（7 次尝试，见 §5.1 第 11 条）。⛔ **这是本文唯一一处「整个厂商无法核验」的空白**，⛔ 必须与「已核实为官方未公布」（华为 / 新华三 / 联想）区别对待。
7. ⛔ **新华三 MegaCube 中文官方页为 JS 空壳**，抓取为空；§1.5 的规格逐字引用取自**英文**官方页。
8. ⚠️ **`nvidia.cn` 对 RTX 5090 D v2 给出官方人民币价**，⛔ 而 `nvidia.com` 的 GeForce 产品页价格模块是 `$XXX` 占位符——⇒ **同一厂商的中英文站价格披露口径不同**，引用时必须写清取自哪个站（**M**）。

### 5.3 ⛔ 本文口径声明

1. ⛔ **本文不是权重体积、管制条款、能力分数的第二真源**。凡数字均来自 §1 顶部列出的四个主真源文件，本文只做**重新分档与三口径归并**。若发现与主真源不一致，**以主真源为准**并回报。
2. ⛔ **全表的 ✅ / ⛔ 判定只回答「装不装得下」**，⛔ 不回答「跑得快不快」「效果好不好」「该选哪个」。带宽差一个量级的容量相同的卡（LPDDR4X 96 GB vs HBM3e 141 GB）在本表里看起来同档，⛔ **实际不可互换**。⇒ 吞吐与并发另见 [h200x4_inference_perf.md](./h200x4_inference_perf.md)，能力分数另见 [h200x4_envelope.md](./h200x4_envelope.md) §2。
3. ⛔ **本文不论证 motivation。** §3 与 §4 只记录管制事实与「查无来源」，⛔ 不得被引用来支撑「工业单位没有算力」这类命题——§3.3 的四条反向事实与 §4.1 的五条否定发现同等承重。

### 5.4 更新日志

| 时间 | 改动 |
| :-- | :-- |
| 2026-08-13 | 建档。7 档分层（T1–T6）；三口径天花板主表覆盖 22 个显存档；NVIDIA 官方规格与 MSRP 逐条核验（8 款专业卡确认「官方不公布价格」这一否定事实，DGX H100/H200 的 640/1128 GB 取到官方 User Guide 逐字，并记录 H100 PCIe / HGX H100·H200 / DGX H100·H200 产品页已下线或换代这一文档漂移）；出口管制逐档裁定 + 四条反向事实；「哪一档最常见」如实记为**查无严谨来源**，只给 n=10 的学术论文自报硬件分布并标明它不是工业界分布。补入第二轮核验：**§4 由一刀切的「查无来源」改为分层表述**——新增 §4.2 两条真实官方一手分布（MLPerf `system_desc` 的 `accelerator_memory_capacity` 字段 · HF 297,135 人自报本地硬件），并确认 Stack Overflow 调查无硬件题、Ollama 无官方遥测；T4a 补 DGX Spark / DGX Station 官方规格并加「unified memory ≠ 显存」口径警告；**MegaCube 更正为桌面级产品线、非训推一体机**；**RTX 5090 D v2 的 ¥16,499 升级为 M 级（nvidia.cn 官方标价）**；一体机价格谱改按头豹研究院正确署名；T3 补 NVIDIA 官方「4 or 8 GPUs」逐字与 Lenovo 4-GPU HGX H200 基板 SKU；补记「厂商公布单卡容量但从不公布聚合总量」这一元事实（华为 / 新华三 / 联想三家一致）。⛔ **曙光因 sugon.com 全域不可达而未核定**，登记为 §5.1 第 11 条。 |
