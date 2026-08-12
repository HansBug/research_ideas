# MDE / RE venue 直翻补漏

> ⭐ 本文件补的是 [se_motivation_survey.md](./se_motivation_survey.md) §5.1 自陈的缺口：⛔「**FSE、ISSTA、TSE、EMSE、MODELS、RE、REFSQ、ICSME 的 proceedings 页面一次都没直接翻过**」。⭐ 本轮直接翻了 MDE / RE 侧的 proceedings 目录，⛔ 不经 Web 搜索转手。
>
> ⛔ **本文件不是 systematic review。** ⭐ 所有「未见」只在 §1 覆盖表列出的 venue-年份内成立，⛔ 出了这个范围一律不作数。

## 0. 一句话结论

⭐ **在 MDE / RE 的 9 个 venue、43 个 venue-年份、3,740 条题录里，⛔「因保密 / 合规所以必须用本地或开源模型」这条论证极其罕见**：⛔ 全库只有 **2 篇**明确写出了这条因果——⭐ Hachm et al.（SAM 2025 @ MODELS-C，⭐ 措辞是「公司政策要求 on-premise」）与 ⭐ Hernández López, Földiák & Varró 的 Text2VQL（MODELS 2024 主会，⭐ 措辞是「专有 API 与工业模型的 IP 保护不相容」）。⛔ 其中**唯一读到全文的那篇是装饰**：Hachm et al. 全文 11 页，⛔ 该动机的全部词次集中在第 2 页的摘要与引言两段，⛔ 此后**零回指**，⛔ 连唯一的模型选型句都改用「to ensure consistency」当理由。⏳ Text2VQL 因 ACM DL 403 **未取得全文，⛔ 承重性未判定**（⭐ 但从摘要看它的技术路线直接由该动机推出，⭐ 结构上最像承重，⭐ 见 §2.2）。⭐ 与之对照，⭐ 同一批检索里 **SE 期刊侧（TSE / TOSEM / EMSE）这条论证是成立且反复出现的**，⭐ 至少 6 篇把它做成了承重（⭐ 日志分析与代码任务为主；⛔ 其中 5 篇为**摘要级**判定，⭐ 仅 Zhong et al. 由前一轮读过全文）。⭐⭐ **因此本轮最有用的产出不是「找到了支撑」，⛔ 而是一条边界**：⭐ 这条动机在 SE 侧有先例可援，⛔ 但在我们自己的投稿目标社区（MODELS / RE / REFSQ / SoSyM / REJ）里**尚未成为惯用论证**，⛔ 审稿人不会默认接受它。

⚠️ ⭐ **另有一条反向发现，⛔ 它比上面那条更该影响我们的写法**：⭐ MDE / RE 社区并非不用开源小模型——⭐ 本轮至少 3 篇用了（⭐ 含本地 Ollama 部署与 Qwen-14B）——⛔ 但它们给出的理由是 **transparency / reproducibility / accessibility**，⛔ **不是保密**。⭐ 逐字见 §2.4 与 §2.5。⛔ 也就是说，⭐ 在这个社区里「为什么用开源小模型」已经有一套**既有且不同**的标准答案；⛔ 我们若改用保密动机，⛔ 是在跟一个已被占据的位置竞争，⛔ 而不是在填空白。

## 1. 逐 venue 覆盖表

⭐ **入口**：DBLP 官方镜像 `dblp.uni-trier.de`（⚠️ ⛔ 主站 `dblp.org` 在本机全程 503 / 超时，⭐ 见 §5）。⭐ 每个 venue-年份取 DBLP 的完整题录列表作为**权威分母**，⛔ 不经搜索引擎。⭐ 摘要来自 Semantic Scholar `paper/search/bulk` 与 `paper/search/match`，⭐ Springer 系（REFSQ / SoSyM / REJ）改走 `rd.springer.com`（⛔ S2 对 Springer 的摘要字段被出版方 elide）。

### 1.1 MDE / RE 侧（本轮主任务）

| venue | 年份 | 入口 | 该年论文数 | LLM 题录 | 命中数 | 备注 |
| :-- | :-- | :-- | --: | --: | --: | :-- |
| MODELS 主会 | 2023 | `/db/conf/models/models2023` | 30 | 2 | 0 | |
| MODELS 主会 | 2024 | `/db/conf/models/models2024` | 26 | 3 | **1** | Text2VQL |
| MODELS 主会 | 2025 | `/db/conf/models/models2025` | 27 | 2 | 0 | |
| MODELS 主会 | 2026 | — | — | — | — | ⛔ 不存在：会议在 10 月，proceedings 未出 |
| MODELS-C（companion / 卫星会 / workshop） | 2023 | `models2023c` | 144 | 4 | 0 | |
| MODELS-C | 2024 | `models2024c` | 156 | 14 | 0 | |
| MODELS-C | 2025 | `models2025c` | 105 | 14 | **1** | Hachm et al.（SAM 2025） |
| RE | 2023 | `/db/conf/re/re2023` | 56 | 3 | 0 | |
| RE | 2024 | `/db/conf/re/re2024` | 60 | 11 | 0 | ⛔ 3 篇 GDPR 论文属「隐私即研究对象」，⛔ 不计 |
| RE | 2025 | `/db/conf/re/re2025` | 71 | 18 | 0 | ⛔ 同上，4 篇 |
| RE | 2026 | — | — | — | — | ⛔ 不存在：会议未办 |
| REFSQ | 2023 | `/db/conf/refsq/refsq2023` | 25 | 0 | 0 | ⛔ 该年零篇 LLM 论文 |
| REFSQ | 2024 | `refsq2024` | 22 | 1 | 0 | |
| REFSQ | 2025 | `refsq2025` | 29 | 7 | 0 | |
| REFSQ | 2026 | `refsq2026` | 23 | 2 | **2** | ⭐ 均为「开源小模型」但非保密动机 |
| SLE | 2023 / 2024 / 2025 / 2026 | `/db/conf/sle/sle20XX` | 20 / 20 / 18 / 13 | 1 / 1 / 0 / 1 | 0 | |
| MODELSWARD | 2023 / 2024 / 2025 / 2026 | `/db/conf/modelsward/…` | 32 / 43 / 51 / 62 | 1 / 4 / 3 / 9 | 0 | |
| STAF workshops（⭐ ECMFA 的实际归宿） | 2024 / 2025 | `/db/conf/staf/staf20XXw` | 10 / 33 | 1 / 11 | 0 | ⛔ 仅题录级 |
| SoSyM（期刊） | 2023–2026（vol. 22–25） | `/db/journals/sosym/sosymNN` | 98 / 75 / 91 / 45 | 3 / 3 / 1 / 1 | 0 | |
| REJ（期刊） | 2023–2026（vol. 28–31） | `/db/journals/re/reNN` | 26 / 24 / 9 / 11 | 0 / 0 / 2 / 3 | 0 | ⚠️ ⛔ vol. 30 DBLP 只索引了 4 期中的 2 期，⭐ 见 §5.3 |
| **ECMFA** | 2023–2026 | `/db/conf/ecmdafa/` | **0** | — | — | ⛔ **DBLP 上最后一届独立 proceedings 是 2018（ECMFA@STAF 2018）**，⛔ 此后无独立卷；⭐ 已改查 STAF workshops |

⭐ **MDE / RE 侧小计：1,455 条题录，137 条 LLM 信号题录，摘要获取 129/137（94.2%）。**

### 1.2 SE 期刊侧（顺带补齐，⭐ 用于做对照）

| venue | 卷 / 年份 | 论文数 | LLM 题录 | 摘要级命中 |
| :-- | :-- | --: | --: | --: |
| TSE | vol. 49–52 / 2023–2026 | 278 / 182 / 228 / 124 | 23 / 19 / 35 / 31 | 15 |
| TOSEM | vol. 32–35 / 2023–2026 | 161 / 223 / 242 / 168 | 19 / 37 / 51 / 35 | 17 |
| EMSE | vol. 28–31 / 2023–2026 | 153 / 163 / 178 / 185 | 6 / 14 / 22 / 38 | 5 |

⭐ **SE 期刊侧小计：2,285 条题录；⭐ 另经 S2 汇集 2,122 份摘要，⭐ 其中 590 篇 LLM 信号，⭐ 37 篇触发部署 / 保密信号。**

⭐ **全部合计：43 个 venue-年份，3,740 条 DBLP 题录。**

### 1.3 ⭐ 方法自检（⛔ 否则「零命中」没有说服力）

⛔ 一个只会返回零的扫描器，⛔ 它的零毫无意义。⭐ 故本轮用**已知阳性**做召回检验：⭐ [se_motivation_survey.md](./se_motivation_survey.md) 已认定为「本轮最实的一处」承重的 **Zhong et al., *Larger Is Not Always Better*（TOSEM, DOI 10.1145/3773287）**，⭐ 在本轮的 TOSEM 2025 扫描中**被独立命中**（⭐ 未参考前一轮结论）。⭐ 说明扫描口径能抓到该形态的论文，⛔ MDE / RE 侧的零不是工具失灵。

## 2. 命中论文逐篇

⭐ **判据先说死**（⛔ 跑之前定的，⛔ 不许事后放宽）：

- ⭐ **命中** = 标题或摘要里同时出现「LLM / 语言模型」信号**与**「本地部署 / 开源模型 / 保密 / 合规」信号，⭐ **且**后者是**选择模型的理由**。
- ⛔ **不算命中**：⛔ 隐私 / GDPR 是**研究对象**（如「用 LLM 抽取 GDPR 需求」）；⛔ 开源模型只是**实验里顺手多测的一个变量**。⭐ 这两类在 RE 2024 / 2025 里很多，⛔ 全部剔除，⛔ 逐条见 §3.2。
- ⭐ **承重 vs 装饰**：⭐ 承重 = 全文**有下游**（被再用于选型、消融、RQ、可接受性论证）；⭐ 装饰 = **只出现一次就再不回来**。⛔ **只看标题不判**。

### 2.1 ⭐⭐ Hachm, Le Calvar, Bruneliere, Tisi — *Towards LLM Agents for Model-Based Engineering: A Case in Transformation Selection*

| 字段 | 值 |
| :-- | :-- |
| Venue | **SAM 2025**（17th System Analysis and Modelling Conference），⭐ 与 MODELS 2025 同期，⭐ 收入 **MODELS-C 2025** 卷，pp. 421–431（⭐ 11 页 full paper，⛔ 非 short / position） |
| DOI | `10.1109/MODELS-C68889.2025.00061` · DBLP `conf/models/HachmCBT25` |
| 单位 / 资助 | IMT Atlantique, LS2N (UMR CNRS 6004), Nantes · EU KDT JU **MATISSE** 项目 (No. 101140216) |
| 读到什么程度 | ⭐ **全文**（作者版 PDF，11 页正文，41 篇参考文献） |
| 判定 | ⛔ **装饰** |

⭐ **逐字原句（全部两处，⛔ 没有第三处）**：

> ⭐ **Abstract（p2）**：“This is particularly challenging in industrial MBE environments where only medium-sized on-premise LLMs can be used due to company policies related to security or data privacy (for instance).”

> ⭐ **§I Introduction（p2）**：“In addition, industrial settings often come with strong security and privacy constraints regarding the use of LLMs. For this reason, companies may require the use of medium-size LLMs operating on-premise rather than more powerful, larger cloud-based ones. We are currently facing such constraints in the MATISSE project [10] where we want to develop LLM agents that support the MBE of Digital Twins for the industry.”

⭐ **承重性判定的依据是词频与位置，⛔ 不是印象**（⭐ 下表由我在提取出的全文文本上**亲自复算**，⛔ 非转述）：

| 词 | 全文次数 | 位置 |
| :-- | --: | :-- |
| `on-premise` | **2** | ⛔ 全在 **p2**（摘要 1 + §I 1） |
| `privacy` | **2** | ⛔ 全在 **p2** |
| `company polic` | **1** | ⛔ p2 |
| `confidential` / `locally` / `deploy` / `proprietary` | **0** | ⛔ 全文无 |
| `Llama` | 10 | §II / §IV / §V |

⛔⛔ **决定性的一处**：⭐ §V-A 实验设置里唯一的模型选型句是——

> “For our current evaluation, we rely on Llama 3.2:3B **to ensure consistency in all our experiments**.”

⛔ 它给出的理由是**实验一致性**，⛔ **不是** on-premise 约束。⭐ 也就是说，⛔ 连最该回指那条动机的地方都没有回指。⛔ §V 评估、§V-D threats to validity、§VI related work、§VII conclusion 全部零回指；⛔ 全文亦无任何部署细节（`GPU` / `Ollama` / `vLLM` / 量化 / endpoint 词频均为 0）。

⭐ **它对我们的价值**：⭐ 这是**目前唯一一条能引的、出自 MDE 正式会议论文的、明确写着「公司政策要求 on-premise」的句子**，⭐ 且带真实工业项目背景（MATISSE）。⛔ **但只能引作「他人也这么设定问题」，⛔ 不能引作「这条约束已被论证」**——⛔ 它自己都没论证，⛔ 一句引文之后就再没管过。⭐ 证据级别 **M**（⭐ 一手全文逐字 + 我方独立复算词频）。

### 2.2 ⏳ Hernández López, Földiák, Varró — *Text2VQL: Teaching a Model Query Language to Open-Source Language Models with ChatGPT*

| 字段 | 值 |
| :-- | :-- |
| Venue | **MODELS 2024 主会**，pp. 13–24（⭐ 本轮唯一一条落在 MODELS **主会**的命中） |
| DOI | `10.1145/3640310.3674091` · DBLP `conf/models/LopezFV24` |
| ⭐ 作者 | José Antonio Hernández López, Máté Földiák, **Dániel Varró** |
| 读到什么程度 | ⭐ **全文**（⛔ ACM DL 403，⭐ 改由作者 Zenodo artifact [10.5281/zenodo.12742459](https://doi.org/10.5281/zenodo.12742459) 取得 accepted version；⭐ 已将其摘要与出版方摘要逐字比对，⭐ 归一化后完全一致） |
| 判定 | ⛔ **装饰** |

⚠️ ⭐ **作者身份本来提高了这条的分量**：⭐ Dániel Varró 是 MDE 社区的核心人物之一，⭐ 也是本文所用查询语言 VIATRA / VQL 生态的主要作者。⛔ **但读完全文后，⛔ 这条依然只能判装饰。**

⭐ **IP 动机的全部两处（⛔ 没有第三处，⛔ 都在第 1 页）**：

> ⭐ **Abstract**：“Since the technology is proprietary and accessible solely through an API, its use may be incompatible with the strict protection of intellectual properties in industrial models. While there are open-source LLM alternatives, they often lack the power of proprietary models and require extensive data fine-tuning to realize their full potential.”

> ⭐ **§1 Introduction**：“Nevertheless, these proprietary LLMs are only accessible exclusively through an API, which inevitably creates barriers for new research and progress. Moreover, its use might conflict with the strict protection of intellectual properties in industrial models.”

⭐ **词频（⭐ 我方独立复算，⚠️ ⭐ 已做连字符与 ﬁ/ﬂ 合字归一化——⛔ 不归一化会漏计，⭐ 见 §5.2 末条）**：

| 词 | 次数 | 位置 |
| :-- | --: | :-- |
| `intellectual propert` | **2** | ⛔ 全在 **p1**（Abstract 1 + §1 1） |
| `industrial` | **2** | ⛔ 即上述两句，⛔ 无其他出现 |
| `privacy` / `confidential` / `on-premise` / `secur*` / `sensitive` / `locally` | **0** | ⛔ 全文均无 |
| `proprietar*` | 12 | ⭐ 其余 10 次均为中性描述（⛔ 如「用专有模型造合成数据集」） |

⛔⛔ **三条决定性证据**：

1. ⛔ **§5 Discussion 自己列出了它要讨论什么，⛔ IP 不在其中**：“In this section, we delve into various implications and limitations of our work. Specifically, we explore how engineers can use the fine-tuned LLMs and how this approach can be extended to other model query languages. Additionally, we discuss limitations concerning the prompt strategy, as well as considerations regarding model and data licenses.”
2. ⚠️ ⛔ **§5 确实提了一个法律问题，⛔ 但那是另一件事**——⭐ 是 OpenAI ToS 禁止用其输出训练竞品（“Use Output to develop models that compete with OpenAI”），⛔ 与「工业模型的 IP 保密」无关。⛔ **不要把这两者混为一条。**
3. ⛔ **§6.1 与 §7 重述「用小开源模型」这个目标时，⛔ 把 IP 理由剥掉了**：§7 逐字为「…harnesses the generation capabilities of powerful proprietary models to guide small open-source models in the text-to-VQL task.」⛔ 纯工具性表述，⛔ 无动机。

⭐ **三条 RQ 逐字**（⛔ 全部只问合成数据集质量与微调增益，⛔ 无一涉及部署 / 保密）：RQ1 查询是否符合自然语言规约；RQ2 合成数据集的复杂度与语言覆盖；RQ3 微调后相对基座模型的提升幅度。⭐ 实验用的是 **DeepSeek Coder 1b / 7b、CodeLlama 7b**（⭐ 数据集生成侧用 ChatGPT）。⭐ 核心 claim：“the fine-tuned versions of the open-source models significantly outperform the base models, **with one achieving performance comparable to ChatGPT**.”

⭐⭐ **对我们的用法**：⭐ 这是 **MODELS 主会**上一条干净的「⭐ 微调后的开源小模型可与 ChatGPT 打平」的先例（⭐ 与 §2.4 相互印证）。⛔ 但它**不能**用来支撑「保密动机已被论证」——⛔ 它自己 9 页正文里一次都没回头看那个动机。⭐ 证据级别 **M**。

⭐ **摘要逐字**：

> “Since the technology is proprietary and accessible solely through an API, its use may be incompatible with the strict protection of intellectual properties in industrial models. While there are open-source LLM alternatives, they often lack the power of proprietary models and require extensive data fine-tuning to realize their full potential. Furthermore, open-source datasets tailored for MDE tasks are scarce, posing challenges for training such models effectively.”

⭐ **为什么它值得继续追**：⭐ 这是**结构上最像承重的一条**——⛔ 摘要里那句 IP 保护不是随口一提，⭐ 它直接推出了整篇论文的技术路线（⭐ 用 ChatGPT 合成数据集 → ⭐ 参数高效微调 DeepSeek Coder 1b / 7b 与 CodeLlama 7b → ⭐ 让开源小模型能写 VQL 查询）。⭐ 若「IP 保护」这句被抽掉，⛔「为什么不直接用 GPT-4 写 VQL」就没有答案了。⚠️ ⛔ **但这只是从摘要推断的结构，⛔ 不是读到正文的判定**——⛔ 按本文件自定的判据，⛔ 未读全文一律标「未判定」。⭐ 证据级别 **S**（⭐ 摘要逐字属 M，⛔ 承重性推断属 I）。

### 2.3 ⏳ Chou, Aydemir, Dalpiaz — *A Comparative Study of Large and Small Language Models for Domain Model Extraction*

| 字段 | 值 |
| :-- | :-- |
| Venue | **REFSQ 2026**（Springer LNCS 16497），pp. 336–351 |
| DOI | `10.1007/978-3-032-21423-2_23` · DBLP `conf/refsq/ChouAD26` |
| ⭐ 作者 | Cheng Yi Chou, Fatma Başak Aydemir, **Fabiano Dalpiaz**（⭐ 均 Utrecht University） |
| 读到什么程度 | ⭐ **全文 16 页**（⭐ 经 Dalpiaz 个人主页自存版取得，⛔ Springer 付费墙已绕过） |
| 判定 | ⛔ **装饰**（⭐ 但比 §2.2 强半档：⭐ 有 1 次实质回指） |

⚠️ ⭐ **作者身份关键**：⭐ Fabiano Dalpiaz 是 RE 社区在「用户故事 → 概念模型」这条线上的代表性学者，⭐ 而文中作为基线的 **Visual Narrator 正是他自己的工具**。⛔ 这不是外围比较，⛔ 而是该子领域权威给出的自家基准对照。

⭐⭐ **§1 Introduction 那段是本轮在整个 MDE / RE 侧找到的最好的一段动机文字，⭐ 逐字全录**（⭐ 它把 on-premise、privacy、开放性、可控性一次说全）：

> “Owing to their reduced parameter count and narrower training scope, SLMs can exhibit more predictable behavior and lower hallucination rates in constrained domains. Their lighter computational footprint enables cost-efficient fine-tuning and **on-premise deployment, which is particularly attractive for industrial settings with privacy or resource constraints**. Moreover, SLMs are often open, less bound to contractual limitations and specific deployment platforms… These characteristics position SLMs as a promising alternative for scenarios where transparency, controllability, and efficiency are critical.”

⭐ **唯一的回指在 §5.1 Implications for practice**（⭐ 逐字）：

> “However, industrial adoption requires attention to **data confidentiality**, explainability, and validation workflows to ensure that generated models remain trustworthy and compliant with organizational standards. In such cases, **SLMs have an advantage over LLMs for resource consumption, ease of on-premise deployment, and more predictable behavior**.”

⭐ **词频（⭐ 我方独立复算，⭐ 已做合字归一）**：`privacy` **1**（§1）、`on-premise` **2**（§1 + §5.1）、`confidential` **1**（§5.1）、`locally` **1**（§3.1）；⛔ `intellectual propert` / `proprietar` / `secur*` / `sensitive` 均为 **0**。

⛔ **为什么仍判装饰**：⛔ 5 条 RQ 全部只问「完整性 / 有效性 / 错误剖面」，⛔ 无一涉及隐私或部署；⛔ §3.3 评估设计、§4 结果、§5.2 threats to validity 全部零提及；⛔ **§6 Conclusions 收束时把隐私动机整个丢掉了**，⭐ 改用纯效率口径：“The SLMs demonstrate competitive performance, thereby serving as practical alternatives **where computational efficiency is a priority**.”

⚠️⚠️ **两条必须带走的事实，⛔ 都对我们不利**：

1. ⛔ **结论是小模型没赢，⛔ 而且连十年前的规则式方法都没赢**。⭐ §4.1 逐字：“It is remarkable how, although the variants of VN are from a decade ago, they are still up-to-part (if not better) than the examined SLMs.” ⭐ §6 逐字：“GPT-o1 performs consistently better than the other models… The SLMs demonstrate competitive performance…**yet, they do not outperform the lightweight, NLP-based Visual Narrator**.”
2. ⚠️ ⛔ **它说的「Qwen-14B」不是原版 Qwen-14B**，⭐ 而是 **DeepSeek-R1-Distill-Qwen-14B**（⭐ 论文脚注给出 HuggingFace 链接）。⛔ 摘要里简称成「Qwen-14B」有歧义；⛔ 我们若引用它做「Qwen 级模型表现」的论据，⛔ 会引错对象。

⭐ 证据级别 **M**（⭐ 全文逐字 + 我方独立复算词频）。

⭐ **摘要逐字（关键段）**：

> “[Context and Motivation] Large language models can derive conceptual models from textual requirements, offering an off-the-shelf alternative to traditional rule-based and machine-learning-based methods. [Question/Problem] Comparative evidence on the validity and completeness of different large and smaller language models for the domain model derivation task remains limited. [Principal ideas/Results] We compare GPT-o1, Llama3-8B, and Qwen-14B with the rule-based Visual Narrator using nine datasets containing user stories and their corresponding domain models. … GPT-o1 outperformed the smaller language models and matched or exceeded Visual Narrator in most tasks. Small language models produced competitive but less consistent results, revealing efficiency–accuracy trade-offs.”

⭐⭐ **这篇与我们的关系最近，⛔ 而且是个警告**：⭐ 它的设定几乎就是我们的设定——⭐ **需求文本 → 领域模型**，⭐ 比的是 **GPT-o1 vs Llama3-8B vs Qwen-14B**（⭐⭐ 连 Qwen 都对上了）。⛔ 但它的结论是「**GPT-o1 outperformed the smaller language models**」「⛔ small language models produced **competitive but less consistent** results」。⛔ 也就是说：⛔ **在离我们最近的这个 RE venue 上，⛔ 已经有人比过一轮，⛔ 而结论不是平手，⛔ 是小模型更差且更不稳。** ⛔ 且它摘要里给出的框架是 **efficiency–accuracy trade-off**，⛔ **不是隐私**。⭐ 证据级别 **M**（⭐ 摘要逐字）。

### 2.4 ⭐ Pan et al. — *LLM-enabled Instance Model Generation*（MODELS-C 2025）

| 字段 | 值 |
| :-- | :-- |
| DOI | `10.1109/MODELS-C68889.2025.00082` · arXiv [2503.22587](https://arxiv.org/abs/2503.22587) · DBLP `conf/models/PanPZWK25` |
| 读到什么程度 | ⭐ **全文**（arXiv HTML，42.8k 字符） |
| 判定 | ⛔ **不是保密动机命中**；⭐ 但它是一条**平价主张（parity claim）**的先例 |

⛔ **`privacy` 在正文出现 0 次**（⚠️ ⛔ 全文文本里那 1 次是 arXiv 页脚的「Copyright · Privacy · Accessibility」，⛔ **不属于论文**——⛔ 这种页脚污染很容易被误计成命中，⭐ 我逐条看了上下文才排除）。⛔ `confidential` / `on-premise` / `sensitive` 均为 0。

⭐ 但它**确实做了本地部署**，⭐ 且**确实给出了平价结论**：

> ⭐ “The Llama 3.1 models (4-bit quantized) were downloaded and deployed locally using Ollama [20].”

> ⭐⭐ “…it helps to narrow the performance gap between large-scale commercial Large Language Models and smaller, open-source models that can be deployed locally.”

> ⭐⭐ “However, Llama 3.1-70B achieved a semantic recall comparable to GPT-4o, **demonstrating the feasibility of applying the proposed method even with locally deployed, smaller-scale open-source LLMs**.”

⭐⭐ **这条对我们极其有用，⛔ 但用法和我们原先设想的不同**：⭐ 它证明**在 MODELS 社区里，「用方法把开源小模型抬到与 SOTA 平价」这个主张是可以发表的**，⭐ 而且**根本不需要挂保密动机**——⛔ 它一个 privacy 字都没写。⭐ 也就是说，⭐ 路线 2 的**效果层主张**在这个社区有先例；⛔ 而我们原本以为必须先立住的**动机层**，⛔ 可能根本不是发表的必要条件。

### 2.5 ⭐ *From Online User Feedback to Requirements*（REFSQ 2026）

| 字段 | 值 |
| :-- | :-- |
| DOI | arXiv [2510.23055](https://arxiv.org/abs/2510.23055) · DBLP `conf/refsq/…26` |
| 读到什么程度 | ⭐ **全文**（arXiv HTML，46.6k 字符） |
| 判定 | ⛔ **不是保密动机命中**；⭐ 它给出的是**另一套**理由 |

⛔ `privacy` 正文 0 次（⛔ 同样只有 arXiv 页脚那一次）。⭐ 它用了「five lightweight open-source LLMs」，⭐ 理由逐字是：

> ⭐⭐ “While many recent works rely on proprietary models such as GPT [8, 33], we focus on open, lightweight alternatives **to improve transparency and reproducibility**.”

> ⭐ “…They differ in size and reasoning capability but **can all be executed locally**. The aim was to examine their performance and behavior rather than identify the best model.”

⭐⭐ **这是 §0 那条反向发现的直接证据**：⭐ RE 社区选开源小模型时的**标准理由是可复现性与透明性**，⛔ 不是保密。

### 2.6 ⭐ SE 期刊侧的对照组（⭐ 这条动机在**那边**是成立的）

⭐ 同一套判据下，⭐ TSE / TOSEM / EMSE 里有一批**真·承重**（⛔ 除 Zhong et al. 由前一轮读过全文外，⛔ 其余 5 篇**均为摘要级判定、未读全文**，⛔ 故只能标注为「摘要级承重」）：

| 论文 | venue | 逐字动机句 | 形态 |
| :-- | :-- | :-- | :-- |
| Zhong et al., *Larger Is Not Always Better* | **TOSEM**（DOI 10.1145/3773287） | “Recent methods emphasize using Large Language Models (LLMs) for automated logging statement generation, but these present **privacy and resource issues, hindering their suitability for enterprise use**.” → 结论“These findings highlight SOLMs as a **privacy-preserving**…alternative” | ⭐ 承重（⭐ 前一轮已读全文，⭐ 判为承重-Q） |
| *Unsupervised, Accurate, and Efficient Log Parsing Using Smaller Open-Source LLMs*（LibreLog） | **TOSEM**（DOI 10.1145/3796239） | “…face three issues: … (3) **privacy risks with commercial models**. We present LibreLog, an unsupervised approach **using open-source LLMs to enhance privacy** and reduce cost while achieving state-of-the-art accuracy.” | ⭐ 承重（⭐ 贡献句本身就是它） |
| Xu et al., *FlexFL* | **TSE**（DOI 10.1109/TSE.2025.3553363） | “…they are built upon proprietary LLMs, which are, although powerful, **confronted with risks in data privacy**. To address these limitations, we propose … FlexFL, which can … effectively work with **open-source LLMs**.” | ⭐ 承重 |
| Zhang et al., *SemanticLog* | **TSE**（DOI 10.1109/TSE.2025.3625121） | “…they typically rely on online APIs (e.g., ChatGPT), **raising privacy concerns** … SemanticLog … powered by **open-source LLMs** … while **maintaining better capability of log data privacy protection**.” | ⭐ 承重 |
| Zhang et al., *The Power of Small LLMs*（MASDP） | **TSE**（DOI 10.1109/TSE.2025.3632508） | “…most multi-agent systems still rely on large LLMs, leading to high computational costs and **data privacy risks**. **Small LLMs provide a resource-efficient and privacy-preserving alternative**; however, directly replacing them … leads to considerable performance degradation.” | ⭐⭐ 承重，⭐ **且与我们的处境同形**（⛔ 承认直接替换会掉点，⭐ 再用方法补回来） |
| *When Fine-Tuning LLMs Meets Data Privacy*（联邦学习修程序） | **TOSEM**（DOI 10.1145/3733599） | “…obtaining such data from various industries is hindered by data privacy concerns, as **companies are reluctant to share their proprietary codebases**.” | ⭐ 承重 |

⭐⭐ **MASDP（TSE 2026）那条最值得抄结构**：⭐ 它公开承认「小模型直接换上去会显著掉点」，⛔ 然后把论文定位成「⭐ 用方法学补偿这个掉点」。⭐ 这正是路线 2 若要成立所需要的叙事骨架，⭐ 而且它已经在 CCF A 刊上过审。

## 3. ⛔ 否定结果

### 3.1 ⭐⭐ 短语级清点（⛔ 这是本轮最硬的一块证据）

⭐ 在 MDE / RE 侧汇集到的 **1,029 份摘要**（⭐ 含 MODELS / MODELS-C / RE / REFSQ / SLE / MODELSWARD / SoSyM / REJ，2023–2026）上做**逐字符串**清点，⛔ 不做语义判断：

| 短语 | 命中论文数 | 其中与 LLM 相关 |
| :-- | --: | :-- |
| `on-premise` / `on-prem` | **2** | ⭐ **1**（⛔ 仅 Hachm et al.；⛔ 另 1 篇是油气数字孪生，与 LLM 无关） |
| `company polic` | **1** | ⭐ 1（⛔ 仅 Hachm et al.） |
| `small language model` | **1** | ⭐ 1（⛔ 仅 REFSQ 2026 那篇比较研究） |
| `open-source llm` | **3** | ⭐ 3（⛔ Text2VQL / REFSQ 2025 情感抽取 / REFSQ 2026 用户反馈） |
| `self-host` | **0** | — |
| `air-gap` | **0** | — |
| `locally deploy` / `deployed locally` / `run locally` / `local deployment` | **0** | — |
| `data never leaves` | **0** | — |
| `cannot be sent` / `not be sent` | **0** | — |
| `sovereign` | **0** | — |
| `data residency` | **0** | — |
| `open-weight` | **0** | — |
| `corporate polic` / `internal polic` | **0** | — |

⛔ **也就是说：在 MDE / RE 四年的摘要里，「self-hosted」「air-gapped」「本地部署」「数据不出域」「数据主权」「open-weight」这六类说法，一次都没有出现过。**

### 3.2 ⛔ 被我剔除的「假命中」（⛔ 剔除理由必须写出来，⛔ 否则等于放宽判据）

⭐ 关键词扫描在 MDE / RE 侧原始触发 **17 条**，⛔ 其中 **12 条**按 §2 开头的判据剔除：

| 类型 | 条数 | 条目 | ⛔ 剔除理由 |
| :-- | --: | :-- | :-- |
| ⛔ **隐私 / 合规是研究对象** | 8 | RE 2024 *Requirements Satisfiability with In-Context Learning*、RE 2024 *Enhancing Legal Compliance and Regulation Analysis*、RE 2024 *Rethinking Legal Compliance Automation*、RE 2025 *Generating Privacy Stories*、RE 2025 *LLM-assisted Extraction of Regulatory Requirements (GDPR)*、RE 2025 *Recommending Security Requirements*、REJ 2026 *Addressing trust requirements…chatbot*、MODELS-C 2025 *Coupling LLMs and MDE…BPMN Artifacts*（⭐「ensuring data privacy」是 BPM 建模的领域难点） | ⛔ 这些是「⭐ 用 LLM 处理隐私需求」，⛔ 不是「⛔ 因隐私而换模型」。⛔ 二者方向相反，⛔ 混为一谈会把一个繁荣的子领域误算成对我们的支撑 |
| ⛔ **开源 / 闭源只是实验变量** | 3 | MODELS 2025 *Accurate and Consistent Graph Model Generation*、MODELS-C 2025 *A comparison of different LLMs for UML class diagrams*、REFSQ 2025 *How Effectively Do LLMs Extract Feature-Sentiment Pairs* | ⛔ 摘要里 open / proprietary 并列出现，⛔ 但只是「多测了几个模型」，⛔ 无任何选型理由 |
| ⛔ **保密动机存在但与 LLM 部署无关** | 1 | SoSyM 2025 *Repeat, reorder, rephrase*（“…especially when internal workflows of organizations have to be treated **confidentially**”） | ⭐ 保密是真的，⛔ 但它论证的是「⭐ 所以要做数据增强而非扩大数据集」，⛔ 与用哪个模型无关 |

⛔ **净命中：MDE / RE 侧 17 − 12 = 5 条**，⭐ 即 §2.1（装饰）、§2.2 与 §2.3（未判定）、§2.4 与 §2.5（非保密动机）。⛔ **承重且属保密动机的：0 条。**

### 3.3 ⛔ 确实翻完且为零的 venue-年份

⭐ 以下 venue-年份**逐条题录翻完**，⛔ 保密 / 本地部署动机命中数为 **0**：

- ⛔ **MODELS 主会 2023、2025**（⛔ 2024 有 1 条 = Text2VQL）
- ⛔ **MODELS-C 2023、2024**（⛔ 2025 有 1 条）
- ⛔ **RE 2023、2024、2025 全部三届**（⛔ 187 篇，⛔ 32 篇 LLM 论文，⛔ **一条都没有**）
- ⛔ **REFSQ 2023、2024、2025**（⛔ 2026 的 2 条均非保密动机）
- ⛔ **SLE 2023–2026 全部四届**
- ⛔ **MODELSWARD 2023–2026 全部四届**
- ⛔ **SoSyM vol. 22–25 全部四卷**
- ⛔ **REJ vol. 28–31 全部四卷**（⚠️ ⛔ vol. 30 索引不全，⭐ 见 §5.3）
- ⛔ **STAF workshops 2024、2025**（⛔ 仅题录级）

⭐⭐ **RE 会议那条最值得单独说**：⭐ 三届 187 篇、32 篇 LLM 论文，⛔ **零条**把保密当作换模型的理由——⛔ 而 RE 恰恰是**最该出现这条论证**的地方（⭐ 需求就是企业机密的典型载体）。⭐ 这个零本身就是一条可写进论文的观察。

## 4. 两条一手核验的结果

### 4.1 ⭐⭐ Falcão & Canedo「78 人调查」：⭐ **一手来源找到了，⛔ 前一轮的「查无一手」应当撤销**

⭐ **完整题录**（⭐ 我方经 **Crossref + DBLP + 出版方页面**三处独立核过，⛔ 非转述）：

> ⭐ Falcão, Fabiano Damasceno Sousa; Canedo, Edna Dias. *Investigating Software Development Teams Members' Perceptions of Data Privacy in the Use of Large Language Models (LLMs)*. In **Proceedings of the XXIII Brazilian Symposium on Software Quality (SBQS 2024)**, Salvador, Bahia, Brazil, Nov 5–8, 2024. ACM, pp. **373–382**. DOI [10.1145/3701625.3701675](https://doi.org/10.1145/3701625.3701675).

| 核验面 | 结果 |
| :-- | :-- |
| **Crossref**（⭐ DOI 注册机构，⭐ 我方直查） | ⭐ 标题、双作者、venue、pages 373–382、publisher ACM、日期 2024-11-05 **全部吻合** |
| **DBLP**（⭐ 我方直查镜像 API） | ⭐ `conf/sbqs/FalcaoC24`，type = *Conference and Workshop Papers*，⭐ 另有配套 Zenodo 补充材料条目 |
| **SBC/SOL 出版方页面**（⭐ 我方直查） | ⭐ 摘要逐字：“**We conducted a survey with 78 ICT practitioners from five regions of the country.**” |
| 补充材料 | ⭐ Zenodo [10.5281/zenodo.13139492](https://zenodo.org/records/13139492)（⭐ CC-BY，⭐ 含问卷与应答者原始数据） |

⚠️ ⛔ **但引用时必须带三条限定，⛔ 否则会失真**：

1. ⛔ 原文口径是「**ICT practitioners**」，⛔ 不是「software practitioners」；⛔ 二手转述把它窄化了。
2. ⛔ 这是**巴西**研究，⛔ 样本取自巴西五个大区，⛔ 法律参照系是 **LGPD** 而非 GDPR；⛔ 结论里「现行立法不足以保护隐私」指的是 LGPD。⛔ 当跨国普适结论引用即为失真。
3. ⛔ 主题是「**数据隐私顾虑**」，⛔ 不是宽泛的「LLM 使用风险」；⛔ 且它**没有**量化「组织禁止把设计制品发给第三方 LLM 的比例」——⛔ [se_motivation_survey.md](./se_motivation_survey.md) §覆盖边界第 2 条**依然成立**。

⛔ **另记一条假线索**：⛔ 某次搜索摘要把该文作者列成「E. Canedo, A. T. Calazans, A. J. Cerqueira, P. Costa, E. T. S. Masson」——⛔ **错的**；⭐ 按 DOI 精确查 Crossref / DBLP / SOL 三处，⭐ 作者恒为 Falcão + Canedo 两人。⭐ 这正好印证「⛔ 搜索摘要不能当一手来源」。

⭐ **顺带发现**：⭐ 同一对作者 2026 年在 **EMSE** 上还有一篇 *Evaluating foundation model integration strategies for detecting PII in Java software engineering pipelines*（DOI 10.1007/s10664-026-10919-y），⭐ 用的是 **open-weight LLM**，⭐ 且它在本轮 EMSE 扫描中被独立命中。

### 4.2 ⭐ 三篇 arXiv 的真实录用状态：⛔ **前一轮的判断有两处需要更正**

| arXiv | 结论 | Venue / DOI | 判据 |
| :-- | :-- | :-- | :-- |
| **2412.02789**（Llama for Code Refinement） | ⭐ **已正式录用** | **SANER 2025**, pp. 681–692, DOI `10.1109/SANER64311.2025.00070`，DBLP `conf/saner/CaumartinQCPLC25` | ⭐ DBLP 有 *Conference and Workshop Papers* 类型条目 |
| **2510.21443**（Does Model Size Matter?） | ⛔ **纯 preprint** | ⛔ 仅 `10.48550/ARXIV.2510.21443` | ⭐ DBLP 该作者 12 条记录里它只以 *CoRR* 出现；⭐⭐ 且**同一份列表已收录该作者 REFSQ 2026 与 2026-07 的 CoRR**，⛔ 说明不是收录延迟，⛔ 是确实未发表 |
| **2511.11125**（RAPID Programs） | ⭐ **已正式录用** | **ICSE-SEIP 2026**, pp. 248–258, DOI `10.1145/3786583.3786869`，DBLP `conf/icse-seip/FaresH26` | ⭐ DBLP 会议条目 + ACM proceedings DOI 同族 |

⛔⛔ **关于 2511.11125 的页眉，⛔ 前一轮「方法论对、具体假设错」**：

- ⭐ **方法论正确**：⛔ 那个页眉**确实**不能当录用证据。⭐ 它是未填完的 acmart 模板——⛔ DOI 写着 `XXXXXXX.XXXXXXX`，⛔ ISBN 是样例串 `978-1-4503-XXXX-X/2018/06`，⛔ 版权行残留 `2018©`。
- ⛔ **具体假设错了**：⛔ 前一轮推理「ICSE 2025 在 Rio，所以 48th 有问题」——⛔ **反了**。⭐ **ICSE 2025 = 第 47 届，在 Ottawa；⭐ ICSE 2026 = 第 48 届，在 Rio de Janeiro，2026-04-12–18**。⛔ 页眉里「48th + Rio + April 12–18」三项对应的**正是 ICSE 2026**，⛔ 作者只写错了年份那一位（⛔ 还把 Janeiro 拼成 Janieiro）。
- ⭐ **而它最终确实被录用了**——⛔ 但这个结论来自 DBLP 与 ACM DOI，⛔ **与那个页眉无关**。⭐ 这恰好是个漂亮的反例：⛔ 页眉的可信度为零，⛔ 哪怕结果碰巧是对的。

⭐⭐ **跨三篇的一条方法论教训（⛔ 值得写进核验规程）**：⛔ 第 1 篇**没有 comments 字段**，⛔ 第 3 篇 comments 写的是「**Submitted to**」，⛔ 但两篇**都已正式发表**。⛔ 故 **arXiv comments 只能正向证明**（⭐ 写了「Accepted at」就是录用），⛔ **不能反向证明**；⭐ 判「是否 preprint」必须以 DBLP 为准，⛔ 且要先确认该作者的 DBLP 收录时间线是最新的（⭐ 本次对第 2 篇即用其 2026-07 的条目验证了这一点），⛔ 否则「DBLP 上没有」可能只是收录延迟。

⭐ **对 [se_motivation_survey.md](./se_motivation_survey.md) 的回写建议**：⭐ §References [3] 应保留「preprint」标注；⛔ [4] 应从「录用状态待核验」改为 **SANER 2025**；⛔ 第 30 行 Fares & Herbold 那条应从「未见录用证据」改为 **ICSE-SEIP 2026 已录用**。⚠️ ⭐ 后者会**提高**该条承重-D 的分量（⛔ 从投稿变成 CCF A 会正式论文）。

## 5. 覆盖边界与访问受限记录

### 5.1 ⛔ 「未见 X」的有效范围

⛔ 本文件所有否定陈述，⛔ **只在 §1 覆盖表列出的 43 个 venue-年份内成立**。⛔ 具体地：

1. ⛔ 结论建立在 **DBLP 题录（3,740 条，完整）+ 摘要（MDE/RE 侧 1,029 份、SE 期刊侧 2,122 份）** 之上，⛔ **不是全文**。⛔ 一篇在正文某处写了「因为保密所以用本地模型」而**标题与摘要都没写**的论文，⛔ 本轮**扫不到**。⛔ 这是本轮最大的假阴性来源，⛔ 无法用现有手段消除。
2. ⛔ MDE / RE 侧的 LLM 论文摘要覆盖率是 **129/137（94.2%）**；⛔ 缺的 8 条见 §5.3。
3. ⛔ 本轮**未覆盖**：⛔ ICSE 主会、FSE、ASE、ISSTA、ICSME、SANER、MSR、ICST 的 proceedings，⛔ 以及 IST / JSS / SCP 等期刊。⛔ 对这些 venue 本文件**不下任何结论**。
4. ⛔ STAF workshops（2024 / 2025）**只做了题录级扫描**，⛔ 未取摘要；⛔ 其「零命中」证据力弱于其他 venue。
5. ⛔ §2.6 的 SE 期刊承重判定**均为摘要级**（⛔ 除 Zhong et al. 由前一轮读过全文），⛔ 未逐篇读全文；⛔ 按本文件自定判据，⛔ 它们严格说应标「摘要级推断」。

### 5.2 ⛔ 访问受限记录

| 资源 | 状态 | 影响 |
| :-- | :-- | :-- |
| `dblp.org` 主站 | ⛔ **全程 503 / 连接超时** | ⭐ 已改用官方镜像 `dblp.uni-trier.de`（⭐ 全部成功）；⛔ `dblp.dagstuhl.de` 亦超时 |
| **OpenAlex API** | ⛔ **429，日额度耗尽**（⛔ 共享出口 IP，⛔ 「Insufficient budget…Resets at midnight UTC」） | ⛔ 放弃该路线，⭐ 改用 Semantic Scholar |
| **arXiv API** | ⛔ 未使用（⭐ 前一轮已知 429） | ⭐ 改用单篇 `arxiv.org/abs` 与 `arxiv.org/html`（⭐ 均成功） |
| **ACM DL** (`dl.acm.org`) | ⛔ **403（Cloudflare）** | ⛔ **Text2VQL 全文未取得**，⛔ 故 §2.2 只能标「仅摘要」 |
| `link.springer.com` | ⛔ **返回 3,038 字节拦截页** | ⭐ 已绕行 `rd.springer.com`（⭐ 全部 14 篇成功） |
| **HAL** (`hal.science`) | ⛔ **Anubis 反爬（PoW 挑战）** | ⭐ 已绕过并取得 Hachm et al. 全文 |
| **SCITEPRESS** | ⛔ 未取得摘要 | ⛔ MODELSWARD 2 篇缺摘要 |
| **Semantic Scholar** | ⚠️ ⛔ **静默限流**：⛔ 批量请求时返回 `{"data":[]}` 而非 429 | ⛔⛔ **这一条差点造成误判**——⭐ 首轮 39 篇单篇查询**全部返回 0 结果**，⛔ 看起来像「这些论文不存在」；⭐ 加上 HTTP 码检测与重试后**全部 39 篇命中**。⛔ 若不做这一步，⛔ 本文件会凭空多出 39 条假否定 |

### 5.3 ⛔ 已知数据缺口

1. ⛔ **REJ vol. 30（2025）在 DBLP 上只索引了 4 期中的 2 期**（⭐ 仅 Number 1 与 Number 4），⛔ 故 DBLP 计数 9 篇偏低；⭐ Semantic Scholar 同年给出 18 篇，⭐ 摘要扫描已覆盖到 18 篇这一侧。⛔ **该卷的 DBLP 分母不可用于任何比例计算。**
2. ⛔ **摘要未取得的 8 条 MDE / RE LLM 论文**：⭐ 其中 5 条（SoSyM ×3、REJ ×2）实际已由 Springer 侧以变体标题取得摘要并参与扫描；⛔ **真正缺的是 2 条 MODELSWARD**（*Integrating LLMs with Enterprise Architecture…A Case Study* 2025、*Scalable Microservices for LLM-vs-LLM Interaction in Board Games* 2026），⛔ 与 1 条题录归一化差异。⚠️ ⭐ 前者是「工业 case study」，⛔ 属**本轮最可能藏着命中的缺口**，⛔ 应在下一轮补。
3. ⛔ **ECMFA 2023–2026 不存在独立 proceedings**：⭐ DBLP `conf/ecmdafa` 最后一届是 **ECMFA@STAF 2018**。⛔ 这不是访问失败，⛔ 是该 venue 已并入 STAF / SoSyM。
4. ⛔ **MODELS 2026 与 RE 2026 的 proceedings 尚未出版**（⭐ 会议分别在 2026 年 10 月与下半年），⛔ 故 2026 年这两个 venue 的「零」是**不适用**，⛔ 不是「未见」。

### 5.4 ⭐ 复现方式

⭐ 全部原始产物在 `/tmp/vscan/`（⛔ 临时目录，⛔ 未入库）：⭐ `raw_*.html` 为 DBLP 原始页，⭐ `titles_*.txt` 为逐 venue 完整题录，⭐ `s2/`、`s2j/`、`single2.json`、`springer_full.json` 为摘要，⭐ `scan.py` / `absscan.py` / `finalscan.py` / `jscan.py` 为扫描脚本。⭐ Hachm et al. 全文在 `/tmp/hachm25/paper_content.txt`。⚠️ ⛔ 这些是一次性调研产物，⛔ 按 [CLAUDE.md](../../../../CLAUDE.md) §9 不入库；⛔ 若需长期保留，⭐ 应先把结论抽象进本文件与 [SUMMARY.md](./SUMMARY.md)，⛔ 而不是把脚本搬进仓库。

## 6. ⭐ 对 Q3 与 story 的直接影响

⭐ 本轮只回答 [SUMMARY.md](./SUMMARY.md) 的 **Q3**（⭐ SE / MDE / RE 文献怎么引出工业保密背景、⛔ 是承重还是装饰）的 MDE / RE 那一半。⭐ 结论按其 §1 档位判据：

| 判据要件 | 本轮结果 |
| :-- | :-- |
| ⭐ A 档要求「SE 文献里 ≥3 篇把类似论证用作**承重**」 | ⭐ **SE 期刊侧满足**（⭐ §2.6 列了 6 篇，⛔ 其中 5 篇为摘要级判定）；⛔ **MDE / RE 侧为 0** |
| ⛔ MDE / RE 侧承重篇数 | ⛔ **0**（⭐ 唯一明确写出该因果的 Hachm et al. 判为装饰） |

⭐ **三条可直接用的建议**（⛔ 仅建议，⛔ 本轮不改 [../../story/](../../story/)）：

1. ⭐ **保密动机可以写，⛔ 但必须引 SE 侧、⛔ 不能引 MDE/RE 侧**。⭐ 最好的三条是 TOSEM 的 Zhong et al. 与 LibreLog、⭐ TSE 的 MASDP。⛔ 若在 MODELS / RE 投稿时声称「这是本社区的共识动机」，⛔ 审稿人只需翻三年目录就能反驳。
2. ⭐⭐ **认真考虑不把保密当主动机。** ⭐ §2.4 证明「用方法把开源小模型抬到与 SOTA 平价」在 MODELS 上**不挂保密也能发**；⛔ 而 §2.5 证明这个社区选开源小模型的既有理由是**可复现性与透明性**。⭐ 后者对我们是**更便宜**的动机——⛔ 它不需要我们去论证任何法规或企业政策（⛔ 而 Q1 / Q2 至今为空），⭐ 且与「可断言可追溯」的卖点天然同向。
3. ⚠️ ⛔ **§2.3 那篇 REFSQ 2026 必须在 related work 里正面处理，⛔ 躲不掉。** ⭐ 它在**同一个 venue 族、同一个任务（需求→领域模型）、同一批模型（含 Qwen）**上已经比过一轮，⛔ 结论是小模型「competitive but less consistent」且被 GPT-o1 压过。⛔ 我们若主张平价，⛔ 就是在直接反驳一篇 REFSQ 论文，⛔ 需要比它更强的证据；⛔ 而 [README.md](./README.md) 已记录主臂 `hit@1` **60.4%** vs 朴素基线 **76.2%**（⛔ Δ = −15.82pp），⛔ 目前**拿不出**这个证据。

---

## §References

⭐ 本节只列本文件正文引用过、且**我方已核到一手题录**的条目。⛔ 未核实项一律不列。

[1] Hachm, Z., Le Calvar, T., Bruneliere, H., Tisi, M. (2025). *Towards LLM Agents for Model-Based Engineering: A Case in Transformation Selection.* SAM 2025 @ MODELS-C 2025, pp. 421–431. DOI: [10.1109/MODELS-C68889.2025.00061](https://doi.org/10.1109/MODELS-C68889.2025.00061) · 全文: [HAL hal-05228415](https://hal.science/hal-05228415)

[2] Hernández López, J. A., Földiák, M., Varró, D. (2024). *Text2VQL: Teaching a Model Query Language to Open-Source Language Models with ChatGPT.* MODELS 2024, pp. 13–24. DOI: [10.1145/3640310.3674091](https://doi.org/10.1145/3640310.3674091)

[3] Chou, C. Y., Aydemir, F. B., Dalpiaz, F. (2026). *A Comparative Study of Large and Small Language Models for Domain Model Extraction.* REFSQ 2026, LNCS, pp. 336–351. DOI: [10.1007/978-3-032-21423-2_23](https://doi.org/10.1007/978-3-032-21423-2_23)

[4] Pan, F., Petrovic, N., Zolfaghari, V., Wen, L., Knoll, A. (2025). *LLM-enabled Instance Model Generation.* MODELS-C 2025. DOI: [10.1109/MODELS-C68889.2025.00082](https://doi.org/10.1109/MODELS-C68889.2025.00082) · arXiv: [2503.22587](https://arxiv.org/abs/2503.22587)

[5] (2026). *From Online User Feedback to Requirements: Evaluating Large Language Models for Classification and Specification Tasks.* REFSQ 2026. arXiv: [2510.23055](https://arxiv.org/abs/2510.23055)

[6] Zhong, R., Li, Y., Yu, G., Gu, W., Kuang, J., Huo, Y., Lyu, M. R. (2025). *Larger Is Not Always Better: Exploring Small Open-source Language Models in Logging Statement Generation.* TOSEM. DOI: [10.1145/3773287](https://doi.org/10.1145/3773287)

[7] (2026). *Unsupervised, Accurate, and Efficient Log Parsing Using Smaller Open-Source Large Language Models* (LibreLog). TOSEM. DOI: [10.1145/3796239](https://doi.org/10.1145/3796239)

[8] Xu, C., Liu, Z., Ren, X., Zhang, G., Liang, M., Lo, D. (2025). *FlexFL: Flexible and Effective Fault Localization With Open-Source Large Language Models.* TSE. DOI: [10.1109/TSE.2025.3553363](https://doi.org/10.1109/TSE.2025.3553363) · arXiv: [2411.10714](https://arxiv.org/abs/2411.10714)

[9] Zhang, ?, et al. (2026). *SemanticLog: Towards Effective and Efficient Large-Scale Semantic Log Parsing.* TSE. DOI: [10.1109/TSE.2025.3625121](https://doi.org/10.1109/TSE.2025.3625121)

[10] Zhang, J., Liao, J., Tang, J., Zhao, X. (2026). *The Power of Small LLMs: A Multi-Agent for Code Generation via Dynamic Precaution Tuning.* TSE. DOI: [10.1109/TSE.2025.3632508](https://doi.org/10.1109/TSE.2025.3632508)

[11] (2025). *When Fine-Tuning LLMs Meets Data Privacy: An Empirical Study of Federated Learning in LLM-Based Program Repair.* TOSEM. DOI: [10.1145/3733599](https://doi.org/10.1145/3733599) · arXiv: [2412.01072](https://arxiv.org/abs/2412.01072)

[12] Falcão, F. D. S., Canedo, E. D. (2024). *Investigating Software Development Teams Members' Perceptions of Data Privacy in the Use of Large Language Models (LLMs).* SBQS 2024, ACM, pp. 373–382. DOI: [10.1145/3701625.3701675](https://doi.org/10.1145/3701625.3701675) · 补充材料: [Zenodo 10.5281/zenodo.13139492](https://zenodo.org/records/13139492)

[13] Caumartin, G., Qin, Q., Chatragadda, S., Panjrolia, J., Li, H., Costa, D. E. (2025). *Exploring the Potential of Llama Models in Automated Code Refinement: A Replication Study.* SANER 2025, pp. 681–692. DOI: [10.1109/SANER64311.2025.00070](https://doi.org/10.1109/SANER64311.2025.00070) · arXiv: [2412.02789](https://arxiv.org/abs/2412.02789)

[14] Fares, ?, Herbold, S. (2026). *Utilizing LLMs for Industrial Process Automation: A Case Study on Modifying RAPID Programs.* ICSE-SEIP 2026, pp. 248–258. DOI: [10.1145/3786583.3786869](https://doi.org/10.1145/3786583.3786869) · arXiv: [2511.11125](https://arxiv.org/abs/2511.11125)

[15] Zadenoori, M. A., De Martino, V., Dabrowski, J., et al. (2025). *Does Model Size Matter? A Comparison of Small and Large Language Models for Requirements Classification.* ⛔ **arXiv preprint，⛔ 本轮核实为未发表**. arXiv: [2510.21443](https://arxiv.org/abs/2510.21443)

[16] Falcão, F. D. S., Canedo, E. D. (2026). *Evaluating foundation model integration strategies for detecting PII in Java software engineering pipelines.* Empirical Software Engineering 31(6):184. DOI: [10.1007/s10664-026-10919-y](https://doi.org/10.1007/s10664-026-10919-y)
