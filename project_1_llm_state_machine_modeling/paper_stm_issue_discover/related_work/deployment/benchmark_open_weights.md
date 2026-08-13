# 开放权重模型 benchmark 表现

> **核验日期**：2026-08-13。**范围**：只写**开放权重侧**（⛔ 闭源前沿刻度由并行核验路负责，⛔ 本文件不重复）。**姊妹文件**：[open_weight_model_compute.md](./open_weight_model_compute.md)（算力与部署需求）。服务 [SUMMARY.md](./SUMMARY.md) §18。

## 证据级别约定

| 记号 | 含义 |
| :-- | :-- |
| **M** | 一手来源逐字核到（arXiv 正文 / 官方 model card / 官方方法学页 / 官方 repo / 官方 changelog） |
| **S** | 二手来源（第三方镜像榜、新闻稿、检索摘要、并行核验路转交而本人未回一手核对） |
| **I** | 推断或估计，⛔ 不得写成事实句 |
| **自报** | 模型开发方自己跑自己报 |
| **独立** | 第三方评测方运行（Artificial Analysis / 论文作者团队 / leaderboard 维护方） |
| ⏳ | 未披露 / 未查到 / 中断未查完，⛔ 留空不填 |

⛔ **本文件不填任何「差不多的数」。** §4 严格区分「查无来源」与「中断未查」。

---

## 0. 一句话结论

**在本研究实际消耗的两个能力维度上，24 GB 级可部署的开放权重模型与前沿闭源已基本平齐，长上下文推理这一维出现反超；⛔ 但仓库原有的两条口径都需要修正，⛔ 且结构化输出这一维缺一把长度对得上的刻度尺。**

六条可直接引用的核心事实：

1. **≤32B 档最高分模型是 `Muse Glimmer 30B`**（Meta，29.6B dense，**Apache-2.0**，2026-08-10 发布，131,072+ 原生上下文）。它在 **AA-LCR（长上下文推理）得 80.0**，**高于** `GPT-5.6 Terra`（79.7）、`GPT-5.5`（79.0）、`Gemini 3.1 Pro`（79.0）、`Claude Opus 5`（75.7）；⛔ 仅落后 AA-LCR 榜首 `Muse Spark 1.2`（83.3）**3.3 分**。
2. **指令遵循（IFBench）**：`Muse Glimmer 30B` **77.0** > `Gemma4-31B` 76.0 > `Qwen3.6-27B` 70.8（**M**，⛔ Meta 自报）。⛔ 前沿侧数字本轮未核，故该维度的绝对差距留 ⏳；并行核验路转交的比值为 **≈0.97**（**S**）。
3. **仓库那条「GLM-4.7 结构化输出 0.830 vs GPT-5.4 0.825」——一手来源我找到了，⛔ 因此「业界无此 benchmark、来源断链」这个判断被推翻。** 出处是 **[arXiv:2604.25359](https://arxiv.org/abs/2604.25359)「The Structured Output Benchmark」（SOB）**，v1 2026-04-28，text 模态 **Value Accuracy** 表：`GLM-4.7` **0.830**（第 1）· `Qwen3.5-35B` **0.828**（第 2）· `GPT-5.4` **0.825**（第 3）。⛔ **两个数字逐字为真**。**但「反超」这个结论不成立**，三条理由见 §3 的 SOB 词条。
4. ⛔ **总分差距是口径错配放大出来的**：Artificial Analysis Intelligence Index v4.1.1 的权重是 **Agents 34% + Coding 24% + Scientific Reasoning 24% + General 18%**，其中 **AA-LCR 只占 6%**（**M**，官方方法学页）。「~30B 差 25 分」的大头落在我们的流水线**根本不执行**的能力上（⛔ 不用工具、不跑终端、不写补丁）。
5. **最相关的那个榜上，`Qwen3.6-27B` 反而是最强的**：**LEDGER**（[arXiv:2606.13100](https://arxiv.org/abs/2606.13100)，唯一同时测「≈100K 长上下文 + 严格 JSON schema + 数值落地」的公开榜）里，`Qwen3.6-27B` 在四个被测模型中**两项都最强**（单 KPI 91.4 recall / 综合 31 KPI 77.2 recall），论文原文称它「is the only model strong on both」。⛔ **但 LEDGER 一个前沿闭源模型都没测**，⛔ 故它不能用来算开放权重 vs 前沿的差距。
6. ⛔ **`gpt-oss` 在我们这两个维度上是最弱的开放权重候选之一，且其 128K 上下文确认为外推**：`config.json` 实测 **`"rope_scaling": {"rope_type": "yarn", "factor": 32.0, "original_max_position_embeddings": 4096}`**（**M**）——即从 **4,096** base 做 **32×** YaRN。四个独立来源一致指向它弱：AA-LCR **33.3**（20b）/ **51.0**（120b）· SOB text Value Accuracy **0.693**（全场最低）· SOB 统一榜 **73.2% / JSON Pass 84.5%**（均全场最低）· LongBench Pro **44.66**（20b）/ 52.61（120b）。

---

## 1. 逐模型得分表（开放权重侧）

⛔ **本节头号纪律：不同配置的分数不放同一列比。** 每张表都标了配置口径；⛔ 跨表比较**默认不可比**。

### 1.1 AA-LCR 全表（长上下文推理，~100K token）

**来源与级别**：⛔ AA 官方 leaderboard 是 SPA，⛔ WebFetch 只拿到骨架（官方页仅文字确认榜首三名）。逐模型分数取自**两个独立镜像**，二者均自述数据源为 Artificial Analysis：[BenchLM](https://benchlm.ai/benchmarks/lcr)（快照 **2026-08-13**，164 模型）与 [CtrlAltDebrief](https://ctrlaltdebrief.com/tools/benchmarks/lcr)（快照 **2026-08-12**，343 模型）。**级别 S**。两镜像在全部重合项上一致（取整差内），且 [Meta 官方卡片](https://huggingface.co/meta-models/Muse-Glimmer-30B) 独立给出其中三个值（80.0 / 68.3 / 73.3）完全吻合，三源交叉。

**配置**：AA 口径 pass@1 / 3 repeats / 温度（非推理 0、推理 0.6）/ ⛔ 不许用工具 / 需 ≥128K 窗口。下表默认取**推理开启**档，括号内为同源其他档。⛔ **评测方为独立（AA），非厂商自报。**

| 模型 | 总参 / 激活 | AA-LCR | 其他档（同源） |
| :-- | :-- | --: | :-- |
| `MiniMax M3` | ⏳ | **80.3** | — |
| `Muse Glimmer 30B` | **29.6B dense** | **80.0** | — |
| `GLM-5.2` | ⏳ | 76.7 | ⛔ 关 **45** |
| `Kimi K2.6` | ⏳ | 76.7 | — |
| `MiniMax M2.7` | ⏳ | 75.3 | — |
| `Kimi K2.7 Code` | ⏳ | 75.0 | — |
| `Hy3`（Tencent） | ⏳ | 74.7 | — |
| `Inkling`（Thinking Machines） | ⏳ | 73.3 | — |
| `Qwen3.6-27B` | **27B dense** | **73.3** | ⛔ 关 **64** |
| `Kimi K2.5` | ⏳ | 73.0 | ⛔ 关 65 |
| `Qwen3.5 397B-A17B` | 397B / 17B | 72.7 | ⛔ 关 62 |
| `Qwen3.5-27B` | **27B** | **72.3** | — |
| `GLM-5` | ⏳ | 70.7 | — |
| `Qwen3.5-122B-A10B` | 122B / 10B | 70.3 | — |
| `Step 3.7 Flash` | ⏳ | 69.7 | — |
| `Inkling-Small` | ⏳ | 69.3 | — |
| `Qwen3.5-35B-A3B` | 35B / 3B | 68.3 | — |
| `Gemma 4 31B` | **31B** | **68.3** | — |
| `GLM-5.1` | ⏳ | 68.0 | — |
| `GLM-4.7` | 355B / 32B | **68.0** | — |
| `Ling 3.0 Flash` | ⏳ | 67.0 | — |
| `Nemotron 3 Ultra` | ⏳ | 67.0 | — |
| `Qwen3.6-35B-A3B` | 35B / 3B | 66.7 | — |
| `Hy3 Preview` | ⏳ | 66.7 | — |
| `Mistral Medium 3.5 128B` | 128B | 65.3 | — |
| `Gemma 4 26B-A4B` | **26B / 4B** | 61.7 | — |
| `Gemma 4 12B` | 12B | 61.7 | — |
| `Nemotron 3 Super 100B` | 100B | 60.3 | — |
| `Step 3.5 Flash` | ⏳ | 60.3 | — |
| `Nemotron 3 Super 120B-A12B` | 120B / 12B | 60.3 | — |
| `DeepSeek V3.1 (Reasoning)` | 671B / 37B | 56.7 | — |
| `DeepSeek-R1` | 671B / 37B | 56.7 | — |
| ⛔ `GPT-OSS 120B` | 117B / 5.1B | ⛔ **51.0** | — |
| `Llama 4 Maverick` | 400B / 17B | 50.0 | — |
| `Nemotron 3.5 Lightning 30B-A3B NVFP4` | **30B / 3B** | ⛔ 49.2 | — |
| `Command A+` | ⏳ | 48.7 | — |
| `Mistral Small 4` | ⏳ | 47.3 | — |
| `DeepSeek V3.1` | 671B / 37B | 46.7 | — |
| `DeepSeek V3.2` | ⏳ | 42.7 | — |
| `Nemotron 3 Nano Omni 30B-A3B` | 30B / 3B | 40.7 | — |
| `GLM-4.7-Flash` | ⏳ | 40.7 | — |
| `Trinity-Large-Preview`（Arcee） | ⏳ | 38.3 | — |
| `Nemotron 3 Nano 30B` | **30B** | ⛔ 37.3 | — |
| `MiMo-V2-Flash`（Xiaomi） | ⏳ | 35.0 | — |
| ⛔ `GPT-OSS 20B` | 21B / 3.6B | ⛔ **33.3** | — |
| `DeepSeek V3` | 671B / 37B | 31.7 | — |
| `Llama 4 Scout` | 109B / 17B | 30.3 | — |
| `GLM-4.6` | ⏳ | 28.3 | — |
| `Ling 2.6 Flash` | ⏳ | 28.0 | — |
| `Ministral 3 8B` | 8B | 25.3 | — |
| `Ministral 3 14B` | **14B** | 25.0 | — |
| `Llama 3.1 405B` | 405B | 24.7 | — |
| `Ultravox v0.6 Llama 3.3 70B` | 70B | 15.7 | — |
| ⛔ `Exaone 4.0 32B` | **32B** | ⛔ **9.0** | — |
| ⛔ `DeepSeek R1 Distill Qwen 32B` | **32B** | ⛔ **8.3** | — |
| ⛔ `Gemma 3 27B` | **27B** | ⛔ **6.3** | — |
| `Granite-4.0-1B` | 1B | 6.0 | — |
| ⛔ `Phi-4` | **14B** | ⛔ **0.0** | ⚠️ 16K 窗口，达不到 128K 门槛 |

⚠️ **一条必须随表带走的口径警告**：⛔ 表底那批 0.0 / 6.0 / 6.3 / 8.3 / 9.0 **多半不是「推理很差」，而是「窗口不够或处理不了 100K 输入」**（**I**）。AA-LCR 明文要求 ≥128K 窗口，而 `Phi-4` 只有 16K。把这些数当能力信号读会得出错误结论。

⚠️ **镜像可以差得很远**：第三个镜像 [llm-registry](https://llm-registry.com/benchmark/lcr) 的快照窗口是 **2026-02-16 至 2026-03-16**（仅 30 模型），给出 `Mistral Small 4` **71.2%** 为当时最强开源——⛔ 与上表的 **47.3** 严重冲突。该站自带 beta 免责声明。**结论：镜像必须交叉，单一镜像不可信。**

### 1.2 SOB 结构化输出（取值准确率）

**来源与级别**：**M**，[arXiv:2604.25359](https://arxiv.org/abs/2604.25359) 正文 + [Interfaze leaderboard](https://interfaze.ai/leaderboards/structured-output-benchmark)。⛔ **不是厂商自报**（一个团队跑了全部模型），⛔ **但办榜方有自家参赛模型**（`Interfaze-Beta`），且论文未作利益冲突披露。

**配置（**M**）**：温度 **0.0** · max output **2,048** · ⛔ **不开 reasoning**（`GPT-5` / `GPT-5-Mini` / `Gemini-3.1-Pro` / `Gemini-3-Flash-Preview` / `DS-R1-Distill-32B` 无法完全关闭，取最低档，作者自承这几个「get a small reasoning advantage the others do not get」）· ⛔ **主设定不开 constrained decoding**，schema 只写在 prompt 里 · 开放权重走 vLLM 张量并行。

#### （a）论文版 · text 模态 Value Accuracy（n = 5,000，21 模型）

| 名次 | 模型 | 权重 | Value Acc |
| --: | :-- | :-- | --: |
| 1 | `GLM-4.7` | **开放权重** | **0.830** |
| 2 | `Qwen3.5-35B` | **开放权重** | **0.828** |
| 3 | `GPT-5.4` | 闭源 | 0.825 |
| 4 | `Gemini-2.5-Flash` | 闭源 | 0.822 |
| 5 | ⛔ `Interfaze-Beta` | ⛔ 办榜方自家 | 0.821 |
| 6 | `Qwen3-235B` | 开放权重 | 0.811 |
| 7 | `GPT-4.1` | 闭源 | 0.811 |
| 8 | `Claude-Sonnet-4.6` | 闭源 | 0.809 |
| 9 | `Gemma-3-27B` | **≤32B** | **0.803** |
| 10 | `Gemini-3-Flash-Preview` | 闭源 | 0.800 |
| 11 | `Gemma-4-31B` | **≤32B** | 0.798 |
| 12 | `Phi-4` | **≤32B** | 0.798 |
| 13 | `GPT-5` | 闭源 | 0.795 |
| 14 | `GPT-5-Mini` | 闭源 | 0.779 |
| 15 | `Qwen3-30B` | **≤32B** | 0.778 |
| 16 | `Nemotron-3-Nano-30B` | **≤32B** | 0.774 |
| 17 | `DS-R1-Distill-32B` | **≤32B** | 0.773 |
| 18 | `IBM-Granite-4.0` | 开放权重 | 0.761 |
| 19 | `Schematron-8B` | **≤32B** | 0.754 |
| 20 | `Ministral-3-14B` | **≤32B** | 0.724 |
| 21 | ⛔ `GPT-OSS-20B` | ≤32B | ⛔ **0.693** |

#### （b）现役 leaderboard 版 · 跨模态统一榜（29 模型，⛔ 未标更新日）

| 名次 | 模型 | 权重 | Overall | Value Acc | JSON Pass |
| --: | :-- | :-- | --: | --: | --: |
| 1 | `GPT-5.4` | 闭源 | **87.0%** | 79.8% | **99.3%** |
| 2 | `Gemini-3.1-Pro` | 闭源 | 86.9% | **82.0%** | 96.6% |
| 3 | `GLM-5.1` | 开放权重 | 86.6% | **80.6%** | 97.5% |
| 4 | `Claude-Opus-4.7` | 闭源 | 86.4% | 78.7% | 99.3% |
| 5 | `Claude-Sonnet-5` | 闭源 | 86.2% | 79.3% | 98.4% |
| 6 | `GLM-4.7` | 开放权重 | 86.1% | **80.4%** | 96.5% |
| 7 | `Qwen3.5-35B` | 开放权重 | 86.1% | **80.1%** | 96.9% |
| 8 | ⛔ `Interfaze-Beta` | ⛔ 办榜方自家 | 86.0% | 80.5% | 96.6% |
| 9 | `GPT-5.5` | 闭源 | 86.0% | 79.5% | 97.8% |
| 10 | `Gemini-2.5-Flash` | 闭源 | 86.0% | 79.6% | 97.2% |
| 11 | `Qwen3-235B` | 开放权重 | 85.7% | 78.6% | 97.8% |
| 14 | `DeepSeek-V4-Pro` | ⏳ | 85.3% | 79.6% | 96.0% |
| 15 | `Kimi-2.6` | 开放权重 | 85.3% | 79.1% | 96.4% |
| 18 | `Gemma-3-27B` | **≤32B** | 84.7% | 77.7% | 96.9% |
| 19 | `Qwen3-30B` | **≤32B** | 84.2% | 75.3% | 98.3% |
| 20 | `Nemotron-3-Nano-30B` | **≤32B** | 84.1% | 74.7% | 98.7% |
| 22 | `Gemma-4-31B` | **≤32B** | 83.3% | 77.8% | 94.3% |
| 24 | `Schematron-8B` | **≤32B** | 83.2% | ⛔ 73.1% | 98.7% |
| 25 | `IBM-Granite-4.0` | 开放权重 | 83.2% | 73.6% | 98.3% |
| 26 | `Phi-4` | **≤32B** | 83.1% | 78.7% | 96.9% |
| 27 | `DS-R1-Distill-32B` | **≤32B** | 82.7% | 74.7% | 96.0% |
| 28 | `Ministral-3-14B` | **≤32B** | 77.8% | 70.0% | 90.6% |
| 29 | ⛔ `GPT-OSS-20B` | ≤32B | ⛔ **73.2%** | ⛔ 66.7% | ⛔ 84.5% |

⛔ 上表省略了纯闭源的第 12、13、16、17、21、23 名（本文件只管开放权重侧，但保留了 §2 计算差距所需的闭源锚点）。模态领先者：text **84.5% `Gemini-3.1-Pro`** · image **67.2% `Gemma-4-31B`**（开放权重）· audio **23.7% `Gemini-2.5-Flash`**。

⛔ **（a）与（b）不可混比**：前者是 text 模态 21 模型，后者是跨模态加权 29 模型。同一模型两表数字不同（`GLM-4.7` 0.830 → 0.804），⛔ 这是**口径差**不是模型变化。

### 1.3 LEDGER（长上下文 + 结构化输出，唯一同时测两者的表）

**来源与级别**：**M**，[arXiv:2606.13100](https://arxiv.org/abs/2606.13100) Table 3，PDF 经 [tools/pdf_extractor.py](../../../../tools/pdf_extractor.py) 提取后逐行读出。**独立**（Artefact Research Center，⛔ 非任何被测模型的开发方），⛔ **非厂商自报**。

**配置（**M**）**：对话式任务给整份 OCR 年报（**≈100k token**），抽单个 KPI 输出 JSON `(found, value, unit_scale, page)`；综合任务一次抽全部 31 个 KPI。匹配容差 **±0.05%**；`recall = 正确值 / 真值数`（⛔ 不作答记 miss）、`precision = 正确 / 尝试数`。评测子集 494 报告 / 13,519 单元 / 10,000 问题。⏳ 温度与 thinking 档位论文未披露。

| 模型 | 总参 / 激活 | 对话式单 KPI R | P | 综合 31 KPI R | P |
| :-- | :-- | --: | --: | --: | --: |
| `Qwen3.6-27B` | **27B dense** | **91.4** | **93.5** | **77.2** | **85.7** |
| `Ministral-3-14B` | 14B | 87.9 | 88.6 | ⛔ **41.4** | ⛔ 43.6 |
| `gpt-oss-20b` | 21B / 3.6B | 85.3 | 86.8 | 65.7 | 73.2 |
| ⛔ `Nemotron-3-Nano-30B` | 30B / 3B | ⛔ **15.0** | ⛔ 15.3 | 65.5 | 78.0 |

**论文自己点出的核心现象（逐字）**：「single-value extraction capability does **not** transfer」——`Ministral` 单值任务第二（87.9%）却在结构化抽取上**塌到 41.4%**（大量幻觉单元）；反过来 `Nemotron` 单值任务近乎无用（有系统性 unit-scaling 错误）却在 schema 约束下**回到 65.5%**。「`Qwen3.6-27B` is the only model strong on both, and **no model exceeds 80% recall**」。

⛔ **必须随这张表带走的两条限定**：⛔ ① **没有任何前沿闭源模型参与**，所以它**不能**回答「开放权重 vs 前沿差多少」；② `Muse Glimmer 30B` **也没被测过**（它 2026-08-10 才发布，LEDGER 是 2026-06），故本轮无法在最相关的榜上比较两个 ≤32B 候选。**这是一条明确的后续动作**：LEDGER 代码 MIT、数据 CC-BY-4.0，自己跑一次即可判（见 §4.3）。

### 1.4 LongBench Pro（长上下文，8k–256k 分档，规则判分，⛔ 代次较旧）

**来源与级别**：**M**，[arXiv:2601.02872v1](https://arxiv.org/html/2601.02872v1)（中科院信工所 / UCAS / 北航 / 小红书）。**独立**，⛔ 非厂商自报。**配置**：每模型跑 3 次、默认参数（无指定则温度 1.0）；thinking 输出预算 32k（256k 窗口模型）或 8k，非 thinking 上限 1k；超长样本从中间截断。格式 `非thinking / thinking`，论文默认报 thinking。**纯规则判分，⛔ 不用 LLM judge。**

| 模型 | 类型 | 窗口 | Overall | Extreme | Hard | Moderate | Easy |
| :-- | :-- | :-- | --: | --: | --: | --: | --: |
| `DeepSeek-V3.2` | Mixed | 160k | 51.67 / **67.82** | 44.27 | 67.73 | 75.08 | 85.02 |
| `Qwen3-235B-A22B-Thinking-2507` | Thinking | 256k | **66.97** | 43.39 | 67.10 | 75.12 | 83.55 |
| `DeepSeek-V3.1` | Mixed | 128k | 51.39 / 66.22 | 42.68 | 62.22 | 73.53 | 85.72 |
| `Qwen3-Next-80B-A3B-Thinking` | Thinking | 256k | 63.95 | 42.47 | 61.46 | 69.23 | 81.90 |
| `Qwen3-235B-A22B-Instruct-2507` | Instruct | 256k | 52.51 / 63.77 | 43.24 | 58.60 | 68.15 | 82.98 |
| `DeepSeek-R1-0528` | Thinking | 128k | 61.89 | 41.49 | 53.68 | 66.53 | 82.67 |
| `Qwen3-Next-80B-A3B-Instruct` | Instruct | 256k | 51.54 / 60.76 | 40.47 | 54.74 | 64.16 | 80.84 |
| `DeepSeek-R1` | Thinking | 128k | 60.07 | 40.76 | 53.39 | 58.83 | 82.44 |
| `Qwen3-30B-A3B-Thinking-2507` | Thinking | 256k | **59.68** | 40.47 | 52.76 | 62.55 | 79.64 |
| `GLM-4.6` | Mixed | 198k | 45.85 / 58.21 | 38.88 | 48.92 | 60.95 | 79.78 |
| `DeepSeek-V3-0324` | Instruct | 128k | 51.70 / 56.71 | 38.69 | 46.20 | 57.14 | 79.20 |
| `Kimi-K2-Instruct-0905` | Instruct | 256k | 50.09 / 55.53 | 38.25 | 43.75 | 57.33 | 77.29 |
| `GLM-4.5` | Mixed | 128k | 43.04 / 55.48 | 37.94 | 47.38 | 55.13 | 76.55 |
| `Qwen3-30B-A3B-Instruct-2507` | Instruct | 256k | 43.84 / **54.52** | 37.05 | 44.04 | 56.47 | 75.59 |
| `MiniMax-M2` | Thinking | 192k | 53.21 | 34.98 | 42.58 | 59.92 | 72.20 |
| ⛔ `GPT-OSS-120B` | Thinking | 128k | ⛔ 52.61 | 35.40 | 44.97 | 50.66 | 74.06 |
| `Qwen3-32B` | Mixed | 128k | 40.28 / **51.12** | 36.45 | 42.24 | 46.18 | 72.80 |
| `Qwen3-4B-Thinking-2507` | Thinking | 256k | 50.10 | 35.31 | 40.99 | 47.66 | 70.53 |
| `Qwen3-14B` | Mixed | 128k | 37.11 / 47.14 | 33.66 | 38.41 | 39.03 | 69.55 |
| `Ministral-3-14B-Instruct-2512` | Instruct | 256k | 40.14 / 45.80 | 31.66 | 37.48 | 39.35 | 67.56 |
| `Qwen3-4B-Instruct-2507` | Instruct | 256k | 36.78 / 45.68 | 31.09 | 36.96 | 39.69 | 67.82 |
| `MiniMax-Text-01` | Instruct | 4M | 41.14 / 45.00 | 33.78 | 38.02 | 40.82 | 61.92 |
| ⛔ `GPT-OSS-20B` | Thinking | 128k | ⛔ **44.66** | 31.59 | 35.89 | 39.33 | 65.05 |
| `Ministral-3-8B-Instruct-2512` | Instruct | 256k | 37.80 / 44.46 | 31.86 | 34.99 | 35.26 | 67.14 |
| `Qwen3-8B` | Mixed | 128k | 33.41 / 44.34 | 33.50 | 37.10 | 30.16 | 67.08 |
| `Qwen2.5-72B-Instruct` | Instruct | 128k | 39.64 / 44.09 | 31.71 | 36.45 | 31.03 | 67.80 |
| `Qwen3-4B` | Mixed | 128k | 31.26 / 40.82 | 30.69 | 34.07 | 31.27 | 59.85 |
| `Llama-3.1-405B-Instruct` | Instruct | 128k | 40.07 / 40.66 | 29.81 | 34.09 | 29.22 | 61.36 |
| `Mistral-Small-3.2-24B-Instruct-2506` | Instruct | 128k | 37.32 / 39.87 | 29.77 | 31.76 | 27.74 | 61.22 |
| `Magistral-Small-2509` | Thinking | 128k | 38.40 | 30.52 | 32.92 | 29.44 | 54.25 |
| `Gemma-3-27B-It` | Instruct | 128k | 36.14 / **37.34** | 27.78 | 30.56 | 24.53 | 57.81 |
| `Mistral-Large-Instruct-2411` | Instruct | 128k | 31.69 / 36.25 | 28.65 | 29.42 | 25.62 | 53.65 |
| `Ministral-3-3B-Instruct-2512` | Instruct | 256k | 30.18 / 34.54 | 26.70 | 30.23 | 25.60 | 49.65 |
| `Llama-3.3-70B-Instruct` | Instruct | 128k | 31.89 / 33.69 | 24.32 | 28.59 | 22.61 | 51.94 |
| `Llama-3.1-70B-Instruct` | Instruct | 128k | 31.53 / 32.12 | 23.93 | 28.04 | 21.44 | 48.46 |
| `Gemma-3-12B-It` | Instruct | 128k | 32.16 / **31.92** | 25.74 | 28.02 | 22.61 | 45.48 |
| `Gemma-3-4B-It` | Instruct | 128k | 21.76 / **21.20** | 18.72 | 19.87 | 13.85 | 28.66 |
| `Llama-3.1-8B-Instruct` | Instruct | 128k | 21.09 / **20.06** | 19.68 | 17.99 | 12.32 | 26.28 |
| `Ministral-8B-Instruct-2410` | Instruct | 128k | 17.56 / **14.43** | 15.06 | 13.98 | 9.89 | 16.84 |
| `Llama-3.2-3B-Instruct` | Instruct | 128k | 15.71 / **12.58** | 15.57 | 10.48 | 7.17 | 14.35 |

**三条论文自己给出的结论**：① **长上下文调优比参数量更重要**——`Qwen3-30B-A3B-Instruct-2507`（54.52）**高于**更大的 `Qwen3-32B`（51.12）；`Qwen3-4B-Instruct-2507`（45.68）高于 `Qwen3-8B`（44.34）· ⛔ ② **部分小模型开 thinking 反而掉分**（`Gemma-3-12B` −0.24、`Gemma-3-4B` −0.56、`Llama-3.1-8B` −1.03、`Ministral-8B` −3.13、`Llama-3.2-3B` −3.13）· ③ 上限很低：即便最强模型在 Extreme 档 Pass@3 也只到 10.68。

⛔ **代次限定**：最新模型是 `Qwen3` / `GLM-4.6` / `DeepSeek-V3.2` 一代（2026-01）。⛔ **没有** `Qwen3.5` / `Qwen3.6` / `GLM-4.7+` / `Muse Glimmer`。本表的差距**只对 2026-01 那一代成立**，不可外推到当前代次。

### 1.5 官方卡片对照（⛔ 厂商自报，但两家互测）

这是本轮唯一拿到的**同档三模型正面对照**，且是**两家厂商各自的官方卡片**——⛔ 因此能直接量出自报偏差。来源：[meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B)（**M**，⛔ 自报）· [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B)（**M**，自报）。**配置**：Meta 列用 **High Reasoning**，两个对照模型标为 **Thinking Mode**；Qwen 自报列为 thinking 模式（卡片建议 temperature 1.0 / top_p 0.95 / top_k 20，数学与编程 benchmark 用 max output 81,920）。

| Benchmark | `Muse Glimmer-30B`（Meta 报） | `Gemma4-31B`（Meta 报） | `Qwen3.6-27B`（Meta 报） | `Qwen3.6-27B`（Qwen **自己**报） | ⚠️ 两家差 |
| :-- | --: | --: | --: | --: | :-- |
| **AA-LCR** | **80.0** | 68.3 | **73.3** | ⏳ 未报 | **与 AA 镜像三值全部吻合** |
| **IFBench** | **77.0** | 76.0 | 70.8 | ⏳ 未报 | — |
| **SWE-bench Verified** | 76.0 | 66.6 | **77.2** | **77.2** | 一致 |
| **SWE-bench Pro** | **51.2** | 36.9 | 50.2 | **53.5** | ⛔ **3.3** |
| **Terminal-Bench** | 51.7（2.1 terminus2） | 43.4 | 60.7（2.1 terminus2） | **59.3（2.0）** | ⛔ **版本 + harness 双重不同，不可比** |
| **GPQA Diamond** | 83.5（AA 口径） | **85.7** | 84.2（AA 口径） | **87.8** | ⛔ **3.6** |
| **HLE** | 22.0（AA text） | **23.6** | 23.1（AA text） | **24.0** | ⛔ 0.9 |
| **AIME 2026** | **94.7** | 89.2 | 94.1 | **94.1** | 一致 |
| **MMMU Pro** | 74 | 73 | 75 | **75.8** | ⛔ 0.8 |
| **SciCode** | **43.6** | 43.4 | 39.8 | ⏳ 未报 | — |
| **𝜏³-Banking** | **23.5** | 15.1 | 16.7 | ⏳ 未报 | — |
| **OSWorld-Verified** | 65.9 | 58.5 | **75.6** | ⏳ 未报 | — |
| **MCP Atlas (Public)** | **75.5** | 54.2 | 62.5 | ⏳ 未报 | — |
| **DeepSearch QA** | **74.6** | 61.7 | 71.1 | ⏳ 未报 | — |
| **Gaia2** | **43.3** | 36.4 | 40.0 | ⏳ 未报 | — |
| **GDPVal-AA v2** | 953 | 811 | **1141** | ⏳ 未报 | ⛔ Elo 口径，非百分比 |
| **WildClawBench** | **47.6** | 37.6 | 43.2 | **43.2** | 一致 |
| **SkillsBench** | 44.3（with skills） | 32.4 | **46.6**（with skills） | 48.2（Avg5） | ⛔ 口径不同 |
| **Charxiv Reasoning** | **78.8** | 77.7 | 78.4 | ⏳ 未报 | — |
| **ScreenSpot Pro** | 75.4 | 75.9 | **76.1** | ⏳ 未报 | — |
| **OmniDocBench v1.5** | 75.8 | 72.5 | **77.8** | ⏳ 未报 | — |
| **Beam128K** | **65.1** | 58.2 | 63.0 | ⏳ 未报 | — |
| **MMLU-Pro** | ⏳ 未报 | ⏳ | ⏳ | **86.2** | ⛔ 该榜已事实退役（§4.2） |
| **MMLU-Redux** | ⏳ 未报 | ⏳ | ⏳ | **93.5** | — |
| **LiveCodeBench v6** | ⏳ 未报 | ⏳ | ⏳ | **83.9** | ⛔ 该榜已事实冻结（§4.2） |
| **SuperGPQA** | ⏳ 未报 | ⏳ | ⏳ | **66.0** | — |
| **HMMT Feb 26** | ⏳ 未报 | ⏳ | ⏳ | **84.3** | — |
| **IMOAnswerBench** | ⏳ 未报 | ⏳ | ⏳ | **80.8** | — |
| **NL2Repo** | ⏳ 未报 | ⏳ | ⏳ | **36.2** | — |
| **SWE-bench Multilingual** | ⏳ 未报 | ⏳ | ⏳ | **71.3** | — |
| **C-Eval** | ⏳ 未报 | ⏳ | ⏳ | **91.4** | — |

**三条从这张表直接得到的结论**：

1. **Meta 报的 AA-LCR 三个值（80.0 / 68.3 / 73.3）与两个 AA 镜像完全吻合**——说明 Meta 是**引用 AA 的独立评测**而非自跑。同理 `GPQA Diamond (AA)` 与 `HLE Text (AA)` 也明确标了 AA 口径。这三个数的可信度因此**高于一般自报**。
2. ⛔ **同一模型、同一 benchmark，两家厂商差 3.6 分**（GPQA-D：Meta 报 Qwen **84.2** / Qwen 自报 **87.8**），⛔ 其次 SWE-bench Pro 差 **3.3** 分。方向一致：**各家报自己的偏高**。这就是「厂商自报必须标注」的具体代价。
3. ⛔ **Terminal-Bench 两个数不可混列**：Qwen 自报 **59.3（2.0）**，Meta 报 **60.7（2.1 terminus2）**——⛔ 版本与 harness 都不同。并行核验路转交：**同一模型换脚手架分数可差近 2 倍**（**S**）。

### 1.6 `gpt-oss` 专项（⛔ 三个 effort 档必须分开）

来源：[openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) 与 [技术报告 arXiv:2508.10925](https://arxiv.org/abs/2508.10925)（**M**，⛔ 自报）。发布 **2025-08-05**，**Apache-2.0**。参数：120b 为 **117B 总参 / 5.1B 激活**（36 层，128 experts，top-4）；20b 为 **21B 总参 / 3.6B 激活**（24 层，32 experts）。

⛔ **上下文外推已确认（**M**）**：`config.json` 实测 `"rope_scaling": {"rope_type": "yarn", "factor": 32.0, "original_max_position_embeddings": 4096}`——即 131,072 = **4,096 × 32** 的 YaRN 外推。⛔ **是否在扩展窗口上做过训练，技术报告本轮未读全文，留 ⏳。**

**本文件不复制 gpt-oss 的官方自报分数表**（⛔ 那些是短上下文数学与代码榜，⛔ 与本研究两个相关维度无关）。**与本研究相关的四个独立来源一致指向它弱**：

| 维度 | gpt-oss-120b | gpt-oss-20b | 来源与级别 |
| :-- | --: | --: | :-- |
| AA-LCR（长上下文推理） | ⛔ **51.0** | ⛔ **33.3** | **S**，镜像 ×2 |
| SOB text Value Accuracy | ⏳ 未测 | ⛔ **0.693（全场最低）** | **M**，独立 |
| SOB 统一榜 Overall / JSON Pass | ⏳ 未测 | ⛔ **73.2% / 84.5%（均全场最低）** | **M**，独立 |
| LongBench Pro | ⛔ 52.61 | ⛔ **44.66** | **M**，独立 |
| LEDGER 综合 31 KPI | ⏳ 未测 | 65.7 R / 73.2 P | **M**，独立 |

**这条结论不依赖 YaRN 判据是否成立**——四个互相独立的评测方在四个不同 benchmark 上给出同向结果。但也要记一条反向事实：在 **LEDGER 综合抽取**上 `gpt-oss-20b`（65.7）**高于** `Ministral-3-14B`（41.4），⛔ 所以它不是在所有结构化任务上都垫底。

---

## 2. ≤32B 档专表（本研究的部署条件内档位）

**判据**：「≤32B」按**总参数量**判，⛔ 不按激活参数——因为 24 GB 部署约束吃的是总参数（权重必须全部驻留）。故 `Qwen3.6-35B-A3B`（35B 总参）、`GLM-4.7`（355B 总参 / 32B 激活）、`MiniMax M3`、`GLM-5.1` **都不算** ≤32B，⛔ 尽管它们激活参数很小。

### 2.1 ≤32B 候选横表（按 AA-LCR 降序）

| 模型 | 总参 | 架构 | 原生上下文 | 许可 | 发布 | AA-LCR | SOB text VA | SOB 统一 VA | LongBench Pro | LEDGER 综合 R |
| :-- | :-- | :-- | :-- | :-- | :-- | --: | --: | --: | --: | --: |
| `Muse Glimmer 30B` | **29.6B** | Dense + ViT | **131,072+** | **Apache-2.0** | 2026-08-10 | **80.0** | ⏳ 未测 | ⏳ 未测 | ⏳ 未测 | ⛔ **未测** |
| `Qwen3.6-27B` | **27B** | Dense 混合 | **262,144** | **Apache-2.0** | 2026-04 | **73.3** | ⏳ 未测 | ⏳ 未测 | ⏳ 未测 | **77.2** |
| `Qwen3.5-27B` | 27B | ⏳ | ⏳ | ⏳ | 2026-02-15 | 72.3 | ⏳ | ⏳ | ⏳ | ⏳ |
| `Gemma 4 31B` | 31B | ⏳ | ⏳ | ⏳ | ⏳ | 68.3 | 0.798 | 77.8 | ⏳ | ⏳ |
| `Gemma 4 26B-A4B` | 26B / 4B | MoE | ⏳ | ⏳ | ⏳ | 61.7 | ⏳ | ⏳ | ⏳ | ⏳ |
| ⛔ `Nemotron 3.5 Lightning 30B-A3B` | 30B / 3B | MoE | ⏳ | ⏳ | ⏳ | ⛔ 49.2 | ⏳ | ⏳ | ⏳ | ⏳ |
| ⛔ `Nemotron 3 Nano 30B` | 30B | ⏳ | ⏳ | ⏳ | ⏳ | ⛔ 37.3 | 0.774 | 74.7 | ⏳ | 65.5 |
| ⛔ `gpt-oss-20b` | 21B / 3.6B | MoE | ⛔ **4,096 → 131,072 YaRN 32×** | Apache-2.0 | 2025-08-05 | ⛔ **33.3** | ⛔ **0.693** | ⛔ **66.7** | ⛔ 44.66 | 65.7 |
| ⛔ `Exaone 4.0 32B` | 32B | ⏳ | ⏳ | ⏳ | ⏳ | ⛔ **9.0** | ⏳ | ⏳ | ⏳ | ⏳ |
| ⛔ `DS-R1-Distill-Qwen-32B` | 32B | Dense | ⏳ | ⏳ | 2025-01 | ⛔ **8.3** | 0.773 | 74.7 | ⏳ | ⏳ |
| ⛔ `Gemma-3-27B-it` | 27B | Dense | 128K | Gemma | 2025-03 | ⛔ **6.3** | **0.803** | **77.7** | 37.34 | ⏳ |
| ⛔ `Phi-4` | 14B | Dense | ⛔ **16K** | MIT | 2024-12 | ⛔ **0.0** | 0.798 | **78.7** | ⏳ | ⏳ |
| `Ministral-3-14B` | 14B | Dense | 256K | ⏳ | 2025-12 | 25.0 | 0.724 | 70.0 | 45.80 | ⛔ 41.4 |
| `Qwen3-32B` | 32B | Dense | 128K | Apache-2.0 | 2025-04-29 | ⏳ 未测 | ⏳ | ⏳ | **51.12** | ⏳ |
| `Qwen3-30B-A3B-Thinking-2507` | 30B / 3B | MoE | 256K | Apache-2.0 | 2025-07 | ⏳ 未测 | ⏳ | ⏳ | **59.68** | ⏳ |
| `Qwen3-30B`（SOB 记法） | 30B | MoE | ⏳ | Apache-2.0 | 2025 | ⏳ 未测 | 0.778 | 75.3 | 54.52 | ⏳ |
| `Mistral-Small-3.2-24B` | 24B | Dense | 128K | Apache-2.0 | 2025-06 | ⏳ 未测 | ⏳ | ⏳ | 39.87 | ⏳ |
| `Magistral-Small-2509` | 24B | Dense | 128K | ⏳ | 2025-09 | ⏳ 未测 | ⏳ | ⏳ | 38.40 | ⏳ |
| `Schematron-8B` | 8B | Dense | ⏳ | ⏳ | ⏳ | ⏳ 未测 | 0.754 | ⛔ 73.1 | ⏳ | ⏳ |

⛔ **这张表最重要的一件事是它的空格**：**没有任何一个 ≤32B 模型在全部五个 benchmark 上都有分。** 两个最强候选 `Muse Glimmer 30B` 与 `Qwen3.6-27B` **在任何一个 benchmark 上都没有同时出现过**（除了 AA-LCR）。⛔ 所以「≤32B 档谁最强」这个问题，**本轮只能在 AA-LCR 这一个维度上回答**。

### 2.2 ≤32B 档最强模型的规格（**M**，官方卡片）

| 项 | `Muse Glimmer 30B` | `Qwen3.6-27B` |
| :-- | :-- | :-- |
| 参数 | **~29.6B**（含 ~1.8B ViT-G/14 视觉编码器） | **27B**（HF 模型树计 28B，BF16） |
| 架构 | **Dense** Causal Transformer + Perception Encoder，**52 层**；GQA 32 query / 2 KV；`[Local, Local, Local, Global]` 注意力、滑窗 **2,048**；RoPE 仅用于 local 层、$\theta = 500{,}000$；vocab 202,048 | **Dense**，**64 层**，hidden 5120，FFN 17408；混合布局 `16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))`；带视觉编码器；vocab 248,320 |
| 原生上下文 | **131,072+** | **262,144**，可扩至 1,010,000 |
| 许可 | **Apache-2.0**（未改动） | **Apache-2.0** |
| 发布 | **2026-08-10** | **2026-04**（collection 更新 Apr 22） |
| 知识截止 | **2026-01-04** | ⏳ 卡片未列 |
| thinking | **Controllable Effort 四档**（low / medium / high / xhigh，经 system prompt 设置）；卡片建议 coding 与 agentic 用 high 或 xhigh | **默认开启**，输出 `<think>...</think>`；可用 `chat_template_kwargs: {"enable_thinking": False}` 关闭；⛔ Qwen3 的 `/think` `/nothink` 软开关**不再官方支持**；新增 `preserve_thinking` 保留历史轮推理 |
| 量化档 | 全精度 64 GB · `K-Quant-Dynamic` targeting **32 GB**、降 **0.2%** · `K-Quant-17GB` targeting **24 GB**、降 **1.0%**（均为 15 个 benchmark 上准确率平均降幅，⛔ 自报） | ⏳ 卡片未给官方量化档 |
| 推荐采样 | ⏳ 卡片未给完整表 | thinking：temp 1.0 / top_p 0.95 / top_k 20 / min_p 0 · 精确编程（WebDev）：temp 0.6 · 非 thinking：temp 0.7 / top_p 0.80 / presence_penalty 1.5 |
| max output 建议 | ⏳ | 多数查询 **32,768**；复杂数学/编程 benchmark **81,920** |

**两条对本研究直接有用的规格事实**：

1. **两个候选的原生窗口都远超我们 30K 的负载**（262K 与 131K），⛔ **都不需要 YaRN 外推**。⚠️ `Qwen3.6-27B` 卡片同时警告：超原生长度时框架用的是 static YaRN，「potentially impacting performance on shorter texts」——但我们在 30K，触不到这条。
2. ⛔ **对照 `gpt-oss-20b`**：它的 131,072 是从 **4,096** base 做 **32×** YaRN 得到的（**M**，`config.json`）。我们 30K 的负载已经是其 base 窗口的 **7.3 倍**——⛔ 完全落在外推区。这与它在四个 benchmark 上一致偏弱是同向的（但**不构成因果证明**，**I**）。

### 2.3 ≤32B vs 前沿的逐维度差距

⛔ 前沿侧数字来自本文件 §1 表内的闭源锚点（AA-LCR 为 **S** 级镜像、SOB 为 **M** 级）。⛔ 闭源侧的完整核验由并行核验路负责。

| 维度 | benchmark | 前沿参照 | 最强 ≤32B | ⛔ 绝对差 | 比值 |
| :-- | :-- | --: | --: | --: | --: |
| **长上下文推理** | AA-LCR | `Muse Spark 1.2` **83.3**（榜首） | `Muse Glimmer 30B` **80.0** | **3.3** | **0.960** |
| 同上，⛔ 只比 OpenAI / Anthropic / Google | AA-LCR | `GPT-5.6 Terra` **79.7**（三家最高） | `Muse Glimmer 30B` **80.0** | **−0.3（反超）** | **1.004** |
| 同上，⛔ 仓库先前推荐的模型 | AA-LCR | `Muse Spark 1.2` 83.3 | `Qwen3.6-27B` **73.3** | ⛔ **10.0** | ⛔ **0.880** |
| **结构化输出取值** | SOB text VA | `GPT-5.4` **0.825** | `Gemma-3-27B` **0.803** | **0.022** | **0.973** |
| **结构化输出取值** | SOB 统一 VA | `Gemini-3.1-Pro` **82.0** | `Phi-4` **78.7** | **3.3** | **0.960** |
| **结构化输出总分** | SOB 统一 Overall | `GPT-5.4` **87.0** | `Gemma-3-27B` **84.7** | **2.3** | **0.974** |
| 指令遵循（词法） | IFBench | ⏳ **前沿侧未核** | `Muse Glimmer 30B` **77.0** | ⏳ | ⏳（转交值 ≈0.97，**S**） |
| 长上下文（⛔ 旧代次） | LongBench Pro | `Gemini-2.5-Pro` **73.42** | `Qwen3-32B` **51.12** | ⛔ **22.3** | ⛔ **0.696** |
| **长上下文 + 结构化（组合）** | LEDGER | ⛔ **无前沿模型参与** | `Qwen3.6-27B` **77.2 R** | ⛔ **无法计算** | ⛔ **无法计算** |
| ⛔ 总分 | AA Index v4.1.1 | ⏳ 未核 | `Qwen3.6-27B` **37.70**（**S**） | ⏳ | ⛔ **约 0.60**（**S**） |

**回答「相关维度 vs 总分，差距谁大」——⛔ 总分差距显著更大，差别在 1.6 倍以上**：相关维度比值 **0.96 ~ 1.004**，⛔ 而总分比值 **约 0.60**（**S**），我们**不做**的维度（转交值：工具调用 0.40、CritPt 0.04、AA-Omniscience 净分**变号**——前沿 +37、≤32B 全为负）差得更多。**机制解释（**M**）**：AA Index v4.1.1 把 **58% 权重压在 Agents + Coding** 上，而 AA-LCR **只占 6%**。

⛔ **反向限定必须同等写满**（按 [SUMMARY.md](./SUMMARY.md) §18.2 第 2、3 条）：

1. ⛔ **换榜结论就翻转**：LongBench Pro 上 ≤32B 比值只有 **0.696**（差 22.3 分），⛔ 与 AA-LCR 的 0.960 相差极大。该表代次旧（无 `Qwen3.5+`），但**这恰恰说明单一榜不足以定 $G$**。若 $G$ 取 22.3，而我们的 $\Delta_{\max} \approx 35$，仍勉强可行，但余量从「充裕」变成「紧」。
2. ⛔ **AA-LCR 的 0.96 依赖 thinking 开启**：关掉推理，`Qwen3.6-27B` 从 73 掉到 **64**、`GLM-5.2` 从 77 掉到 **45**、`Kimi K2.5` 从 73 掉到 65。⛔ 我们的流水线若不开 thinking，这个维度的优势不成立。
3. ⛔ **AA-LCR 的逐模型数字是 S 级**（⛔ 官方页 SPA），论文正式引用前需要一手来源。
4. ⛔ **`Muse Glimmer 30B` 的 80.0 有一条不便的成因**：AA-LCR 榜首 `Muse Spark 1.2` 与它**同属 Meta**，且 Glimmer 是用 Spark 输出做 logit distillation 训出来的（**S**，新闻稿）。⛔ 所以这 3.3 分不是「开放权重整体追上了前沿」，而是「一家厂商把自己的前沿模型蒸馏进了 30B」。这对我们**照样有用**（我们只需要能部署的模型够强），但**表述上不能写成通用规律**。

---

## 3. 我实际用到的 benchmark 词条

⛔ **只写我本轮核过一手来源的五个。** 其余（HumanEval / MBPP / BigCodeBench / SWE-bench 各变体 / RULER / LongBench v2 / ∞Bench / NIAH / IFEval / BFCL / LMArena 等）⛔ **本轮未查完**，见 §4。

### 3.1 AA-LCR — Artificial Analysis Long Context Reasoning

| 字段 | 内容 |
| :-- | :-- |
| 全名与缩写 | Artificial Analysis Long Context Reasoning（**AA-LCR**） |
| 官方来源 | 发布文 [Announcing AA-LCR](https://artificialanalysis.ai/articles/announcing-aa-lcr) · leaderboard [AA-LCR](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning) · 方法学 [intelligence-benchmarking](https://artificialanalysis.ai/methodology/intelligence-benchmarking) · 数据集 [ArtificialAnalysis/AA-LCR](https://huggingface.co/datasets/ArtificialAnalysis/AA-LCR)（题面 Apache-2.0） |
| 发布年份与版本 | **2025-08-05**。⛔ benchmark 本身无版本号；作为 Intelligence Index 成分，当前所属版本为 **v4.1.1**（2026-08-06）；**grader 换过**（见「已知问题」） |
| 规模 | **M** **100 题**，取自 **30 个文档集 / 234 份文档 / 2,979,757 token**；每题配套文档集平均 **99,325 token**（cl100k_base）；需 **≥128K 上下文窗口**才能被评分。类目与题数：Company Documents **63** / Government Consultations **11** / Industry Reports **8** / Legal **6** / Marketing **6** / Academia **5** / Survey Reports **1** |
| 评分方式 | **M** 开放式作答的 **pass/fail**（⛔ 无部分分），由 LLM 做等价判定，**pass@1，3 次 repeat**，满分 100（百分比）。**不许用工具**。在 Intelligence Index v4.1.1 中权重 **6%**。温度：非推理 0、推理 0.6；max output：非推理 16,384、推理取厂商披露上限 |
| **反映什么能力** | **长上下文推理**（⛔ **不是**长上下文检索）。判据是官方原文的两条硬要求：**Multi-document reasoning**（答案需跨多份文档）+ **Multi-step reasoning**（答案不直接出现在文档里、必须被推出来）。建集目标明确写为「replicate real knowledge work」，并以 NIAH 为反面参照。场景举例：跨公司报告比财务指标、在法律文件里追踪实体、从政务征询里归并政策立场 |
| 人类基线与建集 | **M** AA 研究员 + 十余名短期合约本科生出题与校验；出题时**只给非前沿模型**（GPT-4o-mini / Llama-3.1-70B / Gemini 1.5 Flash）校准难度，刻意避免「对着特定前沿模型做对抗筛选」；人类单次作答典型落在 **40–60%**；每道保留题都**至少被一名人类答对**；⛔ 未通过验证的题「revised or discarded」 |
| 运行方 | **独立**——AA 自留全部数据集副本、自跑、自建 harness（Stirrup）与 sandbox、统一温度/token/重试设置，⛔ **不采用厂商提交分数**（**M**，方法学页） |
| ⚠️ **已知问题** | **未饱和**（榜首 83.3%），⛔ 但头部拥挤：前三跨 2.0 分、前十跨 4.3 分（**S**）· **对 reasoning 开关极敏感**：`GPT-5` minimal −49pp（76→27）· `GPT-5.2` 关 −37pp（79→42）· `GLM-5.2` 关 −32pp（77→45）· `Qwen3.6-27B` 关 −9pp（73→64）——**不标档位的 AA-LCR 数字没有意义** · **grader 换过**：2026-08-06 从 `Qwen3 235B A22B 2507 Non-Reasoning` 换成 `GPT-5.6 Luna (medium)`，官方**未说明是否回填重跑历史分数**（**M**，[changelog](https://artificialanalysis.ai/changelog)）→ 跨该日期比较有隐患 · **官方 leaderboard 是 SPA**，逐模型分数只能从镜像取（**S**），且镜像间可严重冲突 · **≥128K 窗口门槛**会让窗口不够的模型拿低分，那不是能力信号 · **grader 是 LLM**，本身是独立误差源 · ⏳ **污染**：官方未讨论；题面在 HF 公开（Apache-2.0），故 2025-08 之后训练的模型存在污染可能（**I**） |
| 发布日基线 | **M** `o3` 69%（另处 69.3%）· `Grok 4` 68% · `Qwen3 235B 2507 Reasoning` 67% · 下界 `LG Exaone 4.0 32B` **14.0%**。官方同时指出：**大窗口的非推理模型可以打败推理模型**（GPT-4.1 1M 窗口胜 DeepSeek R1 与 o1-mini） |

### 3.2 SOB — The Structured Output Benchmark

**这是仓库那条「0.830 vs 0.825」的一手来源**——⛔ 因此「业界无此 benchmark、来源断链」的判断**被推翻**。

| 字段 | 内容 |
| :-- | :-- |
| 全名与缩写 | The Structured Output Benchmark（**SOB**） |
| 官方来源 | 论文 [arXiv:2604.25359](https://arxiv.org/abs/2604.25359)（v1，**2026-04-28**，cs.CL / cs.AI，19 页 4 图 11 表，投 NeurIPS 2026）· 全文 [HTML](https://arxiv.org/html/2604.25359v1) · leaderboard [Interfaze SOB](https://interfaze.ai/leaderboards/structured-output-benchmark) · 介绍文 [Interfaze blog](https://interfaze.ai/blog/introducing-structured-output-benchmark) |
| 作者与机构 | Singh, Khurdula, Khemlani, Agarwal。⛔ **arXiv abs 页未列任何机构**；论文正文联系地址为 `interfaze.ai`，归属 **JigsawStack, Inc.**；代码在 JigsawStack GitHub org，数据集由 `interfaze-ai` 发布在 HF |
| 规模 | **M** 共 **5,324** 条 = text **5,000**（源自 HotpotQA 多跳 QA，从 25,091 条语料抽样，平均 **919 token**）+ image **209**（olmOCR-bench 处理的 PDF，7 类文档，平均 **527** token）+ audio **115**（AMI 会议语料 gold 转写，平均 **7,373** token）。**21 个模型**（audio 20，`Phi-4` 因 16K 窗口被排除）；现役 leaderboard 已扩到 **29 个模型**。⚠️ **三个模态全部以文本形式喂给模型**（图走 OCR markdown、音频走 gold 转写）——所以它测的**不是**视觉或 ASR |
| 评分方式 | **M** 主指标 **Value Accuracy** = 「Exact leaf-value match」，即真值叶路径中预测值精确匹配的比例，满分 1.0；路径带具体数组下标，⛔ **顺序错即该叶记 0**。门指标 **JSON Pass Rate** = 可解析 + 根为 dict/list + `jsonschema.validate` 通过。结构检查不过则语义分**归零**；聚合按 schema 复杂度加权（easy 1.0 / medium 2.0 / hard 3.0）；text 覆盖门 0.95、image/audio 0.90；**有 LLM judge**（阈值 60/100）用于语义等价与数组对齐 |
| 评测配置 | **M** 温度 **0.0** · max output **2,048** · ⛔ **不开 reasoning**（五个模型无法完全关闭，取最低档，作者自承它们「get a small reasoning advantage the others do not get」）· **主设定不开 constrained decoding**，schema 只写在 prompt 里 · 开放权重走 vLLM 张量并行，8B–358B |
| **反映什么能力** | **结构化输出的取值保真度**（⛔ 不只是 schema 合规），兼带**短上下文信息抽取**。它的立论正是「形式已解决、内容没解决」：多数模型 JSON Pass 95%+，但 Value Accuracy 低 **15–30 个百分点**；最紧的 `GLM-5.1` 差 16.9pp，`Schematron-8B` JSON Pass 98.7% 而 Value Accuracy 全场最低 73.1% |
| ⛔ **利益冲突** | ⛔ **不是厂商各自自报**（一个团队跑了全部模型），**但是有自家参赛模型的一方在办榜**：`Interfaze-Beta` 名列榜上（论文第 8 名、被 Key Finding 8 点名夸奖「within 0.015 of GPT-5.4」），而论文**未作任何利益冲突披露、无资助声明**。引用必须连带说明 |
| ⚠️ **已知问题** | ⛔ **真值残留错误率约 3%**（作者自述，基于 5 组 100 条抽样估计；image/audio 为全人工复核）——**这比榜首前三名的 0.005 跨度大 6 倍** · **无置信区间、无跨轮方差、无显著性检验** · **无污染讨论**，而 text 部分（占 94% 记录、主导加权总分）源自 **HotpotQA（2018）**，长期公开、极可能进过预训练语料 · **JSON Pass Rate 已饱和**（29 个模型里 25 个 ≥ 94%）——引用结构化输出能力时**不要引 JSON Pass Rate** · exact match 惩罚语义等价（"USA" vs "United States"）· 数组一律视为**有序** · constrained-decoding 消融**只测了 3 个模型**（audio, n=115）：Value Accuracy 变动 −0.007 ~ +0.033，而 JSON Pass 变动更大且**方向不一致**（`Gemini-2.5-Flash` 0.860→0.956，而 `GPT-5.4` 0.869→**0.808**）· audio 结果是**上界**（gold 转写不含 ASR 误差） |
| ⛔ **对我们的代理质量：差** | ⛔ text 任务平均 **919 token**，**与我们 30K 的负载差 30 倍**；且主设定不开 constrained decoding，而我们五个 LLM 调用全部走 schema 约束的 `tool_use` |
| **仓库那条观察的裁定** | **数字逐字为真**：text 模态 Value Accuracy 第 1 `GLM-4.7` **0.830**、第 3 `GPT-5.4` **0.825**。⛔ **但「反超」不成立**，三条独立理由：① **第 2 名是另一个开放权重模型** `Qwen3.5-35B` **0.828**，所以这不是「开放权重反超闭源」而是「前三名里两个是开放权重」；② **前三跨度 0.005 < 作者自承的 3% 真值噪声**，噪声大 6 倍；③ **换口径就翻转**——同一 benchmark 的跨模态总分上 `GPT-5.4` **0.870** > `GLM-4.7` **0.861**（论文），现役 leaderboard 上 Value Accuracy `Gemini-3.1-Pro` **82.0** > `GLM-5.1` 80.6 > `GLM-4.7` 80.4。**修正后的表述**：不得写「反超」或「$G < 0$」，应写 **$G \approx 0$ 且统计上不可分辨** |

### 3.3 LEDGER

**本轮找到的、与我们流水线形状最接近的 benchmark**：长上下文（≈100K token）**加**严格 JSON 结构化输出**加**可判定的数值落地真值，三件事同时测。⛔ **仓库此前未记录过它。**

| 字段 | 内容 |
| :-- | :-- |
| 全名与缩写 | **LEDGER** = Long-context Evaluation of Documents for Grounded Extraction and Retrieval |
| 官方来源 | 论文 [arXiv:2606.13100](https://arxiv.org/abs/2606.13100)（v1，**2026-06-11**，cs.CL，5 页 1 图，DOI `10.48550/arXiv.2606.13100`）· 代码 [artefactory/LEDGER](https://github.com/artefactory/LEDGER)（**MIT**）· 数据 [HF collection](https://huggingface.co/collections/artefactory/ledger)（**CC-BY-4.0**）· ⛔ 无 leaderboard |
| 作者与机构 | Moslonka, de Vitry, Garnier, Randrianarivo, Malherbe — **Artefact Research Center**（Paris）/ MICS CentraleSupélec Université Paris-Saclay / Ardian。**独立**（⛔ 非任何被测模型的开发方） |
| 规模 | **M** 语料 **4,999** 份 OCR 年报、**738** 家公司、FY **2009–2024**、**691,858** 页、**631M** token、**118,048** 条 KPI 标签与自然语言问题、**2,054,279** 条 qrels；每份报告平均 **126,274 token**（cl100k_base）、中位 **124** 页。评测子集：**494 份报告 / 13,519 条 KPI 真值 / 10,000 个问题**（27.2 KPI/报告）。OCR 由 DeepSeek-OCR-2 做成页对齐 Markdown（表格渲成 HTML/LaTeX） |
| 三个任务（难度递增） | ① **页级检索**：`(question, report) → 相关页`，基线 BM25 / SPLADE / ColBERT · ② **对话式长上下文抽取**：给整份 OCR 报告（≈100k token），抽出**一个**指定 KPI，输出**结构化 JSON 对象** `(found, value, unit_scale, page)` · ③ **综合抽取**：`report → all KPIs`，一次抽出**全部 31 个 KPI** |
| 评分方式 | **M** 抽取任务：`recall = 正确值 / 真值数`（⛔ **不作答记为 miss**）、`precision = 正确 / 尝试数`（不作答与不可验证的多余项排除）；匹配容差 **±0.05%**；满分 100（百分比）。论文明确：单 KPI 任务的 recall **等同于**长上下文文献里的 exact-match accuracy。检索任务：Recall@k / MRR（binary rel≥1）+ nDCG（graded 0/1/2）。无人工评分（人工只用于 OCR 审计与 qrels 抽检） |
| **反映什么能力** | **长上下文推理 + 长上下文检索 + 结构化输出 + 数值落地（grounding）**，四者耦合。这正是本研究流水线的负载形状。论文的动机也贴合：「critical window to assess these reports before market opens is very short, generally of one hour」 |
| 检索基线（**M**） | 页级检索**极难**：`ColBERT` MRR 仅 **0.475**（Recall@5 0.370）· `SPLADE` 0.386（0.272）· `BM25` 0.324（0.265）。论文结论：⛔ 「dense numerical pages heavily defeat off-the-shelf retrievers」 |
| ⛔ **致命局限** | ⛔ **只评了 4 个模型，且全是开放权重**——`Qwen3.6-27B` / `Ministral-3-14B` / `gpt-oss-20b` / `Nemotron-3-Nano-30B`。**一个前沿闭源模型都没有**（参考文献里出现 `Gemini 3.1 Pro`，但只作为生成问题模板的工具，不是被测对象），因此 LEDGER **不能**用来算「开放权重 vs 前沿」的差距 · **`Muse Glimmer 30B` 也未被测**（2026-08-10 才发布） |
| ⚠️ **已知问题** | OCR 质量已量化：15 名标注者审 ~1,150 张财务表，**81.5%** 表格对齐正确，273 张三重编码得 87.2% 完全一致 / 91.3% 两两一致 / **Fleiss $\kappa = 0.81$**；论文称数字抽取「近乎完美」但复杂表布局对齐可能次优 · ⚠️ **qrels 由 LLM judge（`Qwen 3.6`）打 0/1/2 分**，仅 **60 对**经领域专家抽检（**91.6%** 一致），多标注者研究「planned for a future version」 · **问题模板由 `Gemini 3.1 Pro` 生成** · 美国为主、市场反应数据限 2017–2022 · **无污染讨论**：年报与 XBRL 均长期公开，老年份很可能进过预训练（**I**）· 真值来自 XBRL / Yahoo Finance / Alpha Vantage 三级瀑布，论文自承「may contain restatements or vendor errors」· ⏳ **饱和**：远未饱和（天花板 77.2% recall），论文称「establishing the task as an open challenge」 |

### 3.4 LongBench Pro

| 字段 | 内容 |
| :-- | :-- |
| 全名与缩写 | LongBench Pro。⚠️ **与 2023 年的 LongBench、2024 年的 LongBench v2 是不同数据集**，不可混引 |
| 官方来源 | 论文 [arXiv:2601.02872v1](https://arxiv.org/html/2601.02872v1)（**2026-01-06**，cs.CL）。⏳ repo 与 leaderboard 本轮未核 |
| 作者与机构 | Chen, Wu, Jia, Gao, Fu, Zhang, Hu — 中科院信息工程研究所 / UCAS 网安学院 / 北航人工智能学院 / 小红书。**独立** |
| 规模 | **M** **1,500** 样本 = 5 样本 × 25 二级任务 × 2 语言 × **6 个长度档（8k / 16k / 32k / 64k / 128k / 256k）**；**11** 个一级任务类；中英双语；长度用 Qwen tokenizer 计，文档接受目标档 **±20%**；文档为「Fully Natural」的真实网页文档（新闻/医学/科学/文学/法律/教育；含报告、表格、代码、对话、列表、**JSON**）。评测了 **46** 个模型 |
| 正交三维 | **Context Requirement**：Full（证据散落多处远距 span）vs Partial（局部检索）· **Length**：六档 · **Difficulty**：四档，由**模型表现**而非人工评级决定（Extreme = 高档五模型最多 1 个答对；摘要类 >0.65 记正确） |
| 评分方式 | **M** **纯规则判分，⛔ 不用 LLM judge**（这是它相对 AA-LCR 的独特优势）：NDCG@k（检索排序）/ pairwise accuracy（排序）/ accuracy（多选）/ F1 / SubEM / 摘要 `0.5·SemSim + 0.5·ROUGE-L`（取 3 参考的最大）。答案自 `[Answer]` 标记后自动抽取。全部指标落在 [0,1]，报均值 ×100。每模型跑 **3 次**，报均值 + **Best-of-N** + **Pass@N** |
| 评测配置 | **M** 默认参数（无指定则温度 1.0）；thinking 输出预算 **32k**（256k 窗口模型）或 **8k**，非 thinking 上限 **1k**；超长样本**从中间截断** |
| **反映什么能力** | **长上下文推理**，且**按长度档与难度档分层**——⛔ 这是它相对 AA-LCR 的独特价值（AA-LCR 固定在 ~100K、无长度分层）。它有 **32k 档**，正好覆盖我们 30K 的实际负载。同时覆盖检索排序、多选、抽取式 QA、摘要等多种题型 |
| 关键结论 | **长上下文调优比参数量更重要**：`Qwen3-30B-A3B-Instruct-2507`（54.52）**高于**更大的 `Qwen3-32B`（51.12）；`Qwen3-4B-Instruct-2507`（45.68）高于 `Qwen3-8B`（44.34）· `Gemini-2.5-Pro` 在 256k 档 71.77 vs 8k 档 74.50，作者称「remarkable length insensitivity」，⛔ 而多数模型随长度下降 · **部分小模型开 thinking 反而掉分**（见 §1.4）· 上限低：最强模型在 Extreme 档 Pass@3 仅 **10.68** |
| ⚠️ **已知问题** | ⛔ **无污染讨论**，而文档来自公开互联网 · **五个前沿模型同时充当出题 drafter 与难度校准高档**（`Gemini-2.5-Pro` / `GPT-5` / `Claude-4-Sonnet` / `DeepSeek-V3.2` / `Qwen3-235B-Thinking`）→ 有「专挑对这几个模型难的题」的选择性风险（**I**）· 每格仅 **5** 样本，长度档比较约建立在 125 样本上 · 质量审计：抽 300 条得属性正确率 **99.3%**、答案正确率 **97.3%**，残余误差对总分影响约 **0.96** · **逐模型 × 长度档的数据只在热力图里**，正文未给表 · **代次已旧**：最新模型为 `Qwen3` / `GLM-4.6` / `DeepSeek-V3.2` 一代，无 `Qwen3.5+` · 摘要用 SemSim/ROUGE-L 是粗代理 · 未饱和（榜首 73.42） |

### 3.5 ExtractBench

| 字段 | 内容 |
| :-- | :-- |
| 全名与缩写 | **ExtractBench** |
| 官方来源 | 论文 [arXiv:2602.12247v2](https://arxiv.org/html/2602.12247v2)（**2026-02-13**，cs.LG，KDD 2026 Jeju，CC BY 4.0）· 代码 [ContextualAI/extract-bench](https://github.com/ContextualAI/extract-bench)（**MIT**）· ⛔ 无 leaderboard |
| 作者与机构 | Ferguson, Pennington, Beghian, Mohan, Kiela, Agrawal, Nguyen — **Contextual AI**（Mountain View）。独立于被测模型开发方 |
| 规模 | **M** **35 文档 / 5 schema / 2,076 页 / 12,867 个可评字段**；67.9 标注小时（3 名标注者）。域分布（文档/页/真值/键数/深度）：SEC 10-K/Q 7 / 422 / 9,071 / **369** / 4 · Resumes 7 / 21 / 1,007 / 31 / 4 · Credit agreements 10 / 1,368 / 269 / 13 / 3 · Sports 5 / 15 / 522 / 12 / 6 · Research papers 6 / 250 / 1,998 / 16 / 5。单文档 gold JSON 平均 token：Research **25,366** · 10-K/Q **24,418** · Sports 3,416 · Resumes 3,222 · Credit 883 |
| 评分方式 | **M** **Valid JSON**（可解析且过 schema 校验，报 x/35）+ **字段级 pass rate**（⛔ 非法输出记 0 但**留在分母**）+ `Acc (Valid)`（只在合法输出上算）。schema 解析成类型化 AST 后与 gold/pred 联合遍历；每节点挂 metric（`string_exact` / `string_case_insensitive` / `string_fuzzy` Levenshtein 0.8 / `string_semantic` LLM / `integer_exact` / `number_exact` / `number_tolerance` / `boolean_exact` / `array_llm`）；**三态区分 present / null / MISSING**，从而把「漏掉」与「幻觉」分开；对象数组走 LLM 语义对齐、产出数组级 P/R/F1。**有 LLM judge**：Gemini 2.5 Flash、阈值 0.7 |
| 评测配置 | **M** 各 provider 原生多模态 API、**默认参数**、zero-shot prompt；prompt 把 schema 作为「JSON Template」给出并要求「ONLY valid JSON」 |
| **反映什么能力** | **复杂 schema 结构化输出 + 长文档抽取 + 幻觉抑制**。深度 3–6、单 schema 最多 **369 个键**——⛔ 比我们的 `AssertionScript` 复杂得多，属**上界参照**而非同档对比。但单文档 gold JSON 约 24–25K token，**长度与我们同量级** |
| 核心结果 | ⛔ **6 个前沿闭源模型在 SEC 10-K/Q 域上 pass rate 全为 0.0%**（该域占全部字段评测的 **84%**，15,498/18,516）；总体 pass rate **4.6%**（844/18,516），排除 10-K/Q 后 **28.0%**；总体 Valid JSON 仅 **107/210 = 51%** |
| **对我们最要紧的一条** | ⛔ **打开 provider 的 structured-output 强约束后，Valid JSON 反而从 51% 掉到 37%**（77/210）；Resume schema 从 26/42 合法直接掉到 **0/42**（被所有 provider 拒绝）。失败构成（103 次非法）：空响应 **41** · 尾逗号 **31** · PDF 页数超限 20 · JSON 截断 9 · 上下文超限 2。**这条与 [CLAUDE.md](../../../../CLAUDE.md) §11「schema validator 的准入边界」与 §10「阶段化流水线的失败处理」直接相关**——外部证据支持「强约束会把一部分格逼死」 |
| ⛔ **局限** | ⛔ **一个开放权重模型都没测**（只有 6 个闭源）——故它与 LEDGER **零交集**，两者合起来仍算不出开放权重 vs 前沿 · 英文、美国文档为主、仅 5 域、35 文档「sized for diagnosis rather than statistical power」· 3 名标注者但**未报标注者间一致性** · 作者自承 `Acc (Valid)` 来自「biased sample」（较易的那些）· 合成简历「may under-represent real-world diversity」· **无污染讨论**，而 SEC 文件 / 信贷协议 / 论文全是长期公开网页 · 未饱和（极度未饱和，总体 4.6%） |

---

## 4. 未查完与访问受限

### 4.1 ⛔ 中断未查（⛔ **不是**「查无来源」——是根本没查）

⛔ 本轮两次因写盘中断，⛔ 以下模块**完全未核**。**不得当作不存在或为空。**

1. ⛔ **代码 / 主体性 benchmark 完整词条**：HumanEval（+EvalPlus）· MBPP（+）· BigCodeBench · LiveCodeBench 各版本 · SWE-bench full / Lite / **Verified** / Multimodal / Multilingual / Pro · SWE-Lancer · Aider Polyglot · TAU-bench / tau2-bench · Terminal-Bench 官方论文 · OSWorld / WebArena / GAIA。⛔ 尤其 **SWE-bench 的 solution-leakage 研究**与 **HumanEval 污染研究**未查。
2. ⛔ **其余长上下文 benchmark**：RULER · LongBench / LongBench v2 · ∞Bench（InfiniteBench）· NIAH（⛔ 含「NIAH 过于简单」的批评来源）· HELMET · MRCR · Fiction.liveBench · LongProc。唯一旁证：LEDGER 与 LongBench Pro 均引用 [RULER](https://openreview.net/forum?id=kIoBbc76Sy)（COLM 2024, Hsieh et al., NVIDIA）与「Lost in the Middle」（[arXiv:2307.03172](https://arxiv.org/abs/2307.03172)）作为长上下文评测标准参照（**M**，两篇论文的参考文献）。
3. ⛔ **指令遵循 / 函数调用 / 偏好**：IFEval · **IFBench 官方来源与题目数**（⛔ 我只有它的三个自报分数，没有它的词条）· BFCL 各版本与评分机制 · JSONSchemaBench 词条 · LMArena / Chatbot Arena Elo · Arena-Hard(-v2) · MT-Bench。唯一旁证：[JSONSchemaBench](https://arxiv.org/abs/2501.10868) 被 SOB 明确点名为「只测 schema 合规、不测取值」的前作（**M**，SOB 正文）。
4. ⛔ **通用知识 / 数学 benchmark 词条**：本文件不需要它们（⛔ 不测长上下文也不测结构化输出），但若 §2.3 要补总分构成，MMLU-Pro / GPQA-D / HLE / AIME / CritPt / AA-Omniscience 的完整词条仍缺。
5. ⛔ **西方系开放权重模型的其余逐模型分数**：Llama 3.x / 4 官方卡片（⛔ 含 LMArena 实验版争议事件的一手来源）· Mistral 各线官方分 · Gemma 2/3 官方分 · Nemotron 官方分 · Phi-4 官方分 · InternLM · Command R / A。本文件的这些模型分数**全部来自第三方评测方**（AA 镜像 / SOB / LongBench Pro），一个官方卡片都没读到。
6. ⛔ **`gpt-oss` 是否在扩展窗口上训练过**：YaRN 配置已确认（**M**），⛔ 但是否做过长上下文续训需读 [arXiv:2508.10925](https://arxiv.org/abs/2508.10925) 全文，未读。
7. ⛔ **中国系模型的官方技术报告**：GLM-4.7 / GLM-5.x 的官方 benchmark 表 · Kimi K2/K3 · MiniMax M2/M3 · DeepSeek V4 · Qwen3.5 各档。本文件的这些分数同样只来自第三方。

### 4.2 并行核验路转交、⛔ 本人未回一手核对（**S**，⛔ 引用前必须逐条回原文）

⛔ 按 [CLAUDE.md](../../../../CLAUDE.md) §3.8 与仓库记忆「机械代理只能定位不能裁定」，⛔ 以下由并行核验路交回的事实**我没有亲自回一手来源核对**，不得当作 M 级：

1. ⛔ **四个常用 benchmark 已事实退役或冻结**：**MMLU-Pro** · **AIME 2025** · **LiveCodeBench** · **Aider Polyglot**。⛔ **判据是「榜上最新模型的发布日」，不是页面能否打开**——其中三个页面完全正常、无任何停更标识。**对本文件的直接影响**：`Qwen3.6-27B` 官方卡片报的 `MMLU-Pro 86.2` 与 `LiveCodeBench v6 83.9`（**M**，自报）都落在这份清单上，**不可用它们做当前代次横向对比**（前沿模型可能根本没上榜）。一条**独立的同向旁证**（**M**）：AA Intelligence Index **v4.1.1 的九个成分里没有 MMLU-Pro、没有 AIME、没有 LiveCodeBench**——AA 把 MMLU-Pro 与 LiveCodeBench 明确列在「sit outside the Index score」。
2. ⛔ **结构化输出 / JSON schema 遵循：业界没有现成刻度尺**。最接近的 **IFBench 是词法约束**（关键词出现次数、编号列表格式），⛔ **不涉及 schema 一致性**，且已被移出 AA Index。**我本轮的独立发现与此一致**：SOB 是唯一直接测取值保真的公开榜，但其 text 任务平均只 **919 token**（与我们差 30 倍）、主设定不开 constrained decoding、由有自家参赛模型的一方运营、真值噪声 3%；长度对得上的 **ExtractBench** 与 **LEDGER** **各只覆盖一半模型、零交集**。**故该维度只能自建评测**——而这恰是本研究可以主张的贡献之一，不是缺陷。
3. ⛔ **AA Index 跨版本不可比**：`Qwen3.6-27B` 在 **v4.0 = 46 分、v4.1.1 = 37.70 分**，⛔ 差 **8 分以上**。引用任何 AA Index 数字**必须带版本号**。
4. ⛔ **Terminal-Bench 上脚手架必须与分数一起引用**：⛔ 同一模型换脚手架分数可差**近 2 倍**。我本轮拿到的同向旁证（**M**）：`Qwen3.6-27B` 在 Terminal-Bench **2.0** 报 59.3（Qwen 自报）、在 **2.1 terminus2** 报 60.7（Meta 报）——版本与 harness 双重不同。AA 口径为 Terminus 2 + E2B sandbox + 250 episodes 上限 + 2 小时超时（**M**）。
5. **逐基准差距结构高度不均**（比值 = ≤32B / 前沿）：**AA-LCR 0.97**（30B 档有反超）· **IFBench ≈0.97** · GPQA-D **0.90** · ⛔ **总分 0.60** · ⛔ 工具调用 **0.40** · CritPt **0.04** · **AA-Omniscience 净分变号**（前沿 **+37**，≤32B **全为负**）。我本轮独立算出的 AA-LCR 比值是 **0.960**（80.0 / 83.3），与转交的 0.97 同量级。
6. ⛔ **`Muse Glimmer 30B` 是用 `Muse Spark` 输出做 logit distillation 训出来的**（**S**，新闻稿）。⛔ 这条影响 §2.3 结论 4 的表述，需回 Meta 官方方法学报告核。

### 4.3 ⛔ 访问受限（已定位入口，⛔ 内容取不到）

| 目标 | 异常类型 | 已做的降级 |
| :-- | :-- | :-- |
| ⛔ [AA-LCR 官方 leaderboard](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning) | ⛔ **SPA / JS 渲染**，WebFetch 只拿到骨架（图表标注「29 of 496 models」，但身份与分数不在文本里）。官方页仅文字确认榜首三名 | 改用两个镜像交叉 + Meta 卡片三值验证，⛔ 全部降级为 **S** |
| ⛔ [llm-registry AA-LCR](https://llm-registry.com/benchmark/lcr) | ⛔ 表格与图表均显示 "Loading…" 占位 | ⛔ 弃用；仅记录其快照窗口（2026-02/03）与冲突值作为「镜像不可靠」的证据 |
| ⛔ [Qwen3.6-27B 官方博客](https://qwen.ai/blog?id=qwen3.6-27b) | ⛔ 页面只返回单词 "Qwen"（SPA 壳） | 改用 [HF model card](https://huggingface.co/Qwen/Qwen3.6-27B)（**M**，拿到完整 benchmark 表） |
| ⛔ [Meta Muse Glimmer 研究博客](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model) | ⛔ **benchmark 表在图片里**，只有 alt text | 改用 [HF model card](https://huggingface.co/meta-models/Muse-Glimmer-30B)（**M**，拿到完整表） |
| ⛔ [LEDGER PDF](https://arxiv.org/pdf/2606.13100) | ⛔ WebFetch 只拿到 FlateDecode 压缩流 | 用 [tools/pdf_extractor.py](../../../../tools/pdf_extractor.py) text 模式提取后**逐行读全文 5 页**，Table 3 直接读出（**M**） |
| ⛔ [Interfaze SOB leaderboard](https://interfaze.ai/leaderboards/structured-output-benchmark) | 内容可取，⛔ 但**未标最后更新日** | ⛔ 已在 §1.2 标注「未标更新日」 |

⛔ **一条纪律**：以上全部为「入口已定位 / ⛔ 内容待人工核验 / 访问异常类型已记录」，**未据此断言任何事实不存在**。

### 4.4 建议的后续动作（按 ROI 排序）

1. **自己在 LEDGER 上跑 `Muse Glimmer 30B`**。理由：LEDGER 是唯一同时测长上下文 + 结构化输出的公开榜、代码 MIT / 数据 CC-BY-4.0、而它缺的恰好是当前最强 ≤32B 模型。这一次运行同时解决两件事：① §2.1 里「两个最强候选除 AA-LCR 外无共同 benchmark」的悬置；② §4.2 第 2 条「该维度只能自建评测」的一半工作量（有现成 harness 可复用）。
2. **补核 §4.2 那六条 S 级事实**。⛔ 它们目前支撑着 §2.3 的核心结论（尤其第 1、3、5 条）。
3. **给 AA-LCR 找一手来源**（AA 的 API 需 key，或直接联系 AA），⛔ 否则本文件最承重的那张表永远是 S 级。
4. **把「30K token + 严格 schema」做成自建评测**。现成模板：ExtractBench 的三态设计（present / null / **MISSING**，把漏掉与幻觉分开）+ LEDGER 的 `(found, value, unit_scale, page)` 结构 + LEDGER 的 ±0.05% 容差判定。两者许可（MIT / CC-BY-4.0）都允许复用。
5. **决定 `Qwen3.6-27B` 与 `Muse Glimmer 30B` 之间选谁前，先看 §2.1 的空格**：⛔ 目前两条证据方向相反——AA-LCR 上 Glimmer 高 **6.7 分**，而 LEDGER 上 Qwen 是四模型中唯一两项都强的（⛔ Glimmer 未测）。**本轮无法裁定。**

### 4.5 统计

| 项 | 数 |
| :-- | --: |
| 给出完整词条的 benchmark | **5**（AA-LCR / SOB / LEDGER / LongBench Pro / ExtractBench） |
| 出现在得分表中的开放权重模型（去重） | 约 **75** |
| 其中 ≤32B 档 | **19**（§2.1） |
| ⛔ **厂商自报的分数** | ⛔ **§1.5 全表 + §1.6 的 gpt-oss 规格**——即本文件所有来自官方卡片的数据 |
| **独立评测方运行的分数** | §1.1（AA）· §1.2（SOB 作者，⛔ 有 COI）· §1.3（LEDGER 作者）· §1.4（LongBench Pro 作者）· §3.5（ExtractBench 作者） |
| ⛔ 表内 ⏳ 单元 | ⛔ 约 **90** 处（主要是 §2.1 的缺测格与 §1.1 的参数量） |
| ⛔ 中断未查完的模块 | ⛔ **7 类**（§4.1） |
| ⛔ 转交但未回一手核对的事实 | ⛔ **6 条**（§4.2） |

### 4.6 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 | 初版（开放权重侧）。五个 benchmark 完整词条 · 六张逐模型得分表 · **找到仓库那条「0.830 vs 0.825」的一手来源**（[arXiv:2604.25359](https://arxiv.org/abs/2604.25359)），⛔ 推翻「业界无此 benchmark」的判断，但同时判定「反超」结论不成立 · **新找到三个仓库此前未记录的高相关 benchmark**（**LEDGER** / **ExtractBench** / **LongBench Pro**）· **新找到 ≤32B 档更强候选 `Muse Glimmer 30B`**（AA-LCR 上高于 `Qwen3.6-27B` **6.7 分**）· **确认 `gpt-oss` 131,072 = 4,096 × 32 YaRN 外推**（`config.json` 实测）· 因两次中断，§4.1 所列七类模块未查完 |
