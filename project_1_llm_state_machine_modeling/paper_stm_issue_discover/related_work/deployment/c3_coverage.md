# C3 · 覆盖审计

> 本文件只回答「漏了什么」。不核已有结论对不对（C1），不反驳结论（C2）。审计对象：[SUMMARY.md](./SUMMARY.md) 与五个分册（[regulatory_ledger.md](./regulatory_ledger.md)、[se_motivation_survey.md](./se_motivation_survey.md)、[mde_re_venue_scan.md](./mde_re_venue_scan.md)、[small_model_papers.md](./small_model_papers.md)、[counterarguments.md](./counterarguments.md)）+ [verification_log.md](./verification_log.md)。审计日期 2026-08-13。未读 `c1_*` / `c2_*`。

## 0. 一句话结论（最严重的覆盖缺口是什么）

**最严重的缺口不是那四条自陈缺口，而是「覆盖边界只为已被废弃的那条 story 写，没为新推荐的那条 story 写」。** [SUMMARY.md](./SUMMARY.md) §6 的四行覆盖表（MDE/RE、SE 会议、法规、检索工具）全部服务于**已被判定不成立的私域部署动机**；而 §3 推荐的两条新结论——「可复现性是社区已接受的标准答案」与「脚手架适用区间是弱模型」——其证据来自 [small_model_papers.md](./small_model_papers.md) 与 [counterarguments.md](./counterarguments.md)，**这两个分册的覆盖边界一行都没进 §6**。后果是：一个只读 SUMMARY 的读者（含导师、含 R1）会以为新推荐的动机站在与旧动机同等的证据基础上，而实际上它的支撑是 1 篇逐字 + 若干 preprint，且**最可能推翻它的那篇论文本轮根本没读**（[arXiv:2607.03691](https://arxiv.org/abs/2607.03691)）。

次严重的一条：**法域已收窄到中国，文献却全是英文。** 结论明说「剩下最硬的四条依据全在中国法域」，而中文学术文献（《软件学报》《计算机学报》《计算机研究与发展》等）**零覆盖**——在唯一能闭环的那个法域里，我们不知道别人是怎么论证的、有没有先例、先例是承重还是装饰。这是全轮最不对称的一处。

## 1. 未覆盖的证据族 / 检索角度（按对结论的影响排序）

### 1.1 🔴 反向雪球完全未做（最高性价比，直接决定两条主结论的支撑数）

**六个文件里没有任何一处记录「从关键论文的参考文献往回滚」或「从被引论文往外滚」。** 全部检索都是关键词驱动 + venue 目录直翻，唯一的例外是 [regulatory_ledger.md](./regulatory_ledger.md) §1.5b 顺着 IEC 61508-1 NOTE 5 找到 IEC 62443（而那一条恰恰是全轮最有价值的邻接命中之一——说明雪球有效）。

三个最该滚而没滚的点，各自直接落在一条承重结论上：

| 起点 | 滚哪个方向 | 它能补什么结论 |
| :-- | :-- | :-- |
| Angermeir ICSE'26 [arXiv:2510.25506](https://arxiv.org/abs/2510.25506) | **被引** | §3.1「可复现性是社区已接受的标准答案」——目前目标社区内逐字支撑只有 1 篇（见 §2.1）。引用它的后续论文正是「采纳了这条动机的人」，是把 1 抬到 ≥3 的最短路径 |
| Abdulkarim [arXiv:2604.00275](https://arxiv.org/abs/2604.00275) | **参考文献 + 被引** | §3.2 的唯一同任务域外部证据。它引了谁做 NL→状态机的前人工作 = 我们 related work 的骨架；引它的人 = 是否已有人复现或推翻那个 crossover |
| Chou / Aydemir / Dalpiaz REFSQ'26 [DOI](https://doi.org/10.1007/978-3-032-21423-2_23) | **参考文献** | 它是全轮对我们最不利的一篇（同任务、同模型档、结论相反），[mde_re_venue_scan.md](./mde_re_venue_scan.md) §6 第 3 条自己说「躲不掉，必须正面处理」。它的对比对象与基线选择是我们必须继承的比较框架 |

**为什么它是最高性价比**：Semantic Scholar 的 citations / references 端点本轮已用过且成功（[mde_re_venue_scan.md](./mde_re_venue_scan.md) §1.1），DBLP 镜像也可用。工具全在手上，缺的只是这一个动作。**工作量：1 个 agent、2–3 小时**（三个起点各滚一层，去重后估计 30–60 条候选，摘要级筛，命中的读全文）。

### 1.2 🔴 ICSE / ASE / FSE / ISSTA 的 venue 级扫库未做（自陈缺口，但严重性被低估）

自陈见 [SUMMARY.md](./SUMMARY.md) §6「该侧『未见』无证据力」与 [small_model_papers.md](./small_model_papers.md) §6.1 第 2 条。**但两处都把它当成「旧动机的缺口」，实际它现在是新结论的缺口**：

1. [small_model_papers.md](./small_model_papers.md) §4.9 主张存在一条**文献真空**（「2026 年前沿模型上做 self-refine 逐组件消融 + token 成本记账的 SE 实证一篇都没有」），并自己写明「主张这个空缺之前必须先做 venue 级扫库」。这条真空是我们方法学贡献的落点之一，**目前它没有资格被主张**。
2. §3.2 的「脚手架适用区间是弱模型」正是 ICSE / FSE / ASE 会发的那类实证结论。在这四个会上没扫过，就无法说这条主张是「与既有工作一致」还是「与既有工作冲突」。

**关键观察：这个缺口是 scope 决定，不是访问失败。** 同一套 DBLP 镜像 + Semantic Scholar 摘要管线在 MDE/RE 侧成功产出了 43 个 venue-年份 / 3,740 条题录，还做了已知阳性召回自检（[mde_re_venue_scan.md](./mde_re_venue_scan.md) §1.3）。把同一管线指向 `conf/icse` / `conf/kbse`（ASE）/ `conf/sigsoft`（FSE/ESEC）/ `conf/issta` 是**同一动作**，不需要新工具，也不受 ACM DL 403 影响（DBLP 给题录、S2 给摘要）。**工作量：1 个 agent、4–6 小时**（4 个 venue × 2023–2026，题录量约 2,000–2,500，摘要级扫 + 命中读全文）。

### 1.3 🔴 中文文献零覆盖（自陈一行，严重性完全没说）

[small_model_papers.md](./small_model_papers.md) §6.1 第 4 条只有一句「中文 / 非英文文献、工业界白皮书、工具报告完全未覆盖」，其余五个文件**一次都没提**。而结论层的处境使这条缺口变得不对称：

- [SUMMARY.md](./SUMMARY.md) §2.3 与 [counterarguments.md](./counterarguments.md) §1.3 都写明：**剩下最硬的依据全在中国法域**（保密法 / 等保 / 重要数据 / 军工资质）。
- 于是出现一个结构性空洞：**我们把动机收窄到中国法域，却完全没查中文学术社区在同一法域内是怎么论证的。** 中文 SE / 需求工程社区（《软件学报》《计算机学报》《计算机研究与发展》《计算机科学》、CCF 中文会议如 NASAC / 软件工程学术会议）恰恰是**最可能已经把「保密 → 本地部署 Qwen/GLM」写成承重动机**的地方，因为它的作者群直接受等保与保密法约束。
- 两种结果都有用：若**有**承重先例，那是 §4.3「保密动机尚未成为惯用论证」这条限定的直接反例，且给我们一批可引文献；若**没有**，那么「连中国法域内的作者都不这么论证」是一条比现在强得多的否定结论。

⚠️ 一条限定：中文先例**不能**用于 ICSE / FSE / ASE 投稿的「社区共识」论证（审稿人不在该社区）。它能用于两处：一是作为「该法域内的工程实践证据」；二是若最终改投中文期刊或国内会议，它变成主要支撑。

**工作量：1 个 agent、3–4 小时**（CNKI / 万方 / 维普对机器访问不友好，但知网的 CCF 中文期刊题录可经 DBLP 中文刊页与各刊官网目录页取得；建议先用《软件学报》与《计算机学报》官网目录页 + 期刊自建检索，2023–2026）。

### 1.4 🟠 工业界白皮书 / 行业调查未覆盖，而它正对着一条「答不上来」

[counterarguments.md](./counterarguments.md) §6 第 7 条自陈答不上「工业场景的举证」，§5.6 写「我们没有对应物」，并说「一份小规模从业者问卷是性价比最高的补强（但那是新工作量）」。**这个判断可能建立在一个假缺口上**——本轮从未检索非学术的公开调查，而这类数据大量存在且可引：

- Stack Overflow Developer Survey 的 AI 板块（含「组织是否限制 AI 工具」类题目）、JetBrains State of Developer Ecosystem、GitHub Octoverse。
- 咨询与厂商侧的企业 AI 治理调查（Gartner / Deloitte / McKinsey / Cisco Data Privacy Benchmark）——其中「因数据顾虑限制/禁止公共 GenAI 的企业比例」是常见题目。
- **可引性已被本轮自己证明**：[se_motivation_survey.md](./se_motivation_survey.md) §4.1 已确认「引一条新闻报道做保密动机的锚」在 TOSEM（CCF A 刊）上有先例（Kharpal 2023 / CNBC）。既然新闻可引，公开调查报告的引用门槛不会更高。

**影响的结论**：不改变任何已有判定，但可能把 §6 第 7 条从「答不上来」降级为「有二手行业数据支撑、无自有工业案例」。**工作量：1 个 agent、1–2 小时。**

### 1.5 🟠 LLM 提供方自身企业条款只到 🟡，而它们是「杀死原版 story」的刀刃

已覆盖的是**云平台**（Azure / AWS / GCP，[counterarguments.md](./counterarguments.md) §1.1 三行全 M 级，质量很高）。**未覆盖的是提供方自己的合同文本**：

| 对象 | 当前状态 | 它支撑哪条结论 |
| :-- | :-- | :-- |
| OpenAI Enterprise Privacy / Business Terms / DPA | [regulatory_ledger.md](./regulatory_ledger.md) §3.4 四条全 🟡，自陈「未逐字锚定条款号」 | §3.4「厂商侧合规能力已填掉必要性」——这是把 (c) 层判死的其中一刀 |
| Anthropic Commercial Terms / Usage Policy / Trust Center | 只取了 Public Sector FAQ **一页** | §2.1 反证 2（「ITAR data can be processed via Bedrock」）——单页单来源 |
| Azure abuse monitoring 保留期 | [counterarguments.md](./counterarguments.md) §7.3 第 1 条自标 **I 级**，「不要把 30 天写成当前官方承诺」 | 同上 |
| OpenAI FedRAMP 20x Class C 的字段术语 | [counterarguments.md](./counterarguments.md) §7.3 第 2 条自标 **S 级 / 待人工核验** | §2.1 反证 3——而 SUMMARY 把它当 🟢 事实句写 |

**补这条的方向可能对我方有利，这是它值得做的真正理由**：若逐字读下来发现 ZDR 是逐案审批、需签附加条款、且不覆盖 abuse monitoring 与 grounding 缓存（Google 侧已确认 Search grounding 存 3 天且无法关闭），那么「厂商措施已填掉私域部署的必要性」这条反证会从「已填掉」弱化为「填掉了默认路径、未填掉可得性」——即 §3.4 里那条 (i)「合规成本而非合规禁止」有了逐字依据。**工作量：1 个 agent、2 小时**（全部为公开页面，无付费墙；`aka.ms/dpa` 的 .docx 需下载解析）。

### 1.6 🟡 形式化方法社区（FM / CAV / TACAS / NFM / FormaliSE）与 ICST / ISSRE / SANER / MSR / ICSME 未直翻

[mde_re_venue_scan.md](./mde_re_venue_scan.md) §5.1 第 3 条自陈了后半段。前半段（形式化方法侧）**六个文件都没提**，而它是一个真实缺口：与我们最同构的一篇 VerIbmc（[arXiv:2606.16886](https://arxiv.org/abs/2606.16886)，本地小模型 + 符号验证器、逐模型消融）属于这一族且**只是 preprint、venue 未核**（[small_model_papers.md](./small_model_papers.md) §6.2 第 7 项）。若这一族里已有同类工作的正式发表版，它比现有全部 preprint 证据都更硬。

**影响**：§3.2 的证据分量（目前全靠 preprint）与 §4.9 的真空主张。**工作量：与 §1.2 合并做，追加 2–3 小时。**

### 1.7 🟡 EU AI Act 只查了条文、未查 recital 与 Commission guidelines；且「对我们不利」的那条监管动向是孤证

[regulatory_ledger.md](./regulatory_ledger.md) §2.2 对 AI Act 的覆盖是 Art. 2(1)/2(6)/2(8)/4(1)/6(1)(2)/78(1)(a) + Annex III，结论「不适用」。**未查的是 Art. 10（数据治理）/ Art. 11 + Annex IV（技术文档）/ Art. 12（logging）/ Art. 15（accuracy & robustness）/ Art. 17（QMS）/ Art. 43（合格评定），也未查任何 recital 与欧盟委员会的 high-risk classification guidelines。**

**先说不影响的部分**：这些条款的义务主体都是**高风险 AI 系统的提供者/部署者**，而我们的对象是「用 AI 工具去开发受监管软件」，形态错配与 §2.2 已给的判定同构，补查后**大概率仍是不覆盖**。所以它**不是**为了救活 (c) 层。

**真正值得查的只有一个点**：Art. 6(1) 的判据是「AI 系统作为 Annex I 立法覆盖产品的**安全部件**」。若 LLM 建模工具的产出被用作汽车 / 医疗产品的设计制品，该工具是否因此落入范围——这个边界问题在 recital 与委员会指南里可能有直接说法。它与另一件事同族：

⚠️ **[SUMMARY.md](./SUMMARY.md) §5 末尾那条「需要单独决定的事」（EASA NPA 2025-07(A) 的 "avoiding the double development and verification with AI tools"）目前是孤证**——1 条、征求意见稿、单一域（航空）、且出现在范围排除说明段。它是全轮唯一一条**方向对我们不利**的监管发现，而不利结论同样需要补证：单条支撑既无法确认它有多严重，也无法确认它是不是孤例。**该查的邻域**：FDA 关于 AI 用于器械/药品开发的指南、IMDRF 的 AI/ML 文件、UL 4600（自动驾驶安全案例中对工具的要求）、以及 EASA 自己的 AI Roadmap 2.0 与后续 NPA。**工作量：1 个 agent、2–3 小时。**

### 1.8 🟡 核电侧完全未查（唯一还可能把 (c) 层从「立不住」抬起来的候选）

已覆盖的受监管域：汽车（26262 / 21434 / TISAX / R155）、航空（DO-178C / DO-330 / DO-326A / Part-IS / EASA NPA）、轨交（EN 50128 / 50716）、医疗（62304 / 81001-5-1）、工控（62443-4-1）。**核电零覆盖**：IEC 61513、IEC 60880、IEC 62138、IAEA SSG-39、NRC RG 1.152 / 1.168 一条都没查。

**诚实的影响评估：低。** 已有五个域给出的形态完全一致（授权并规范 ≠ 禁止），第六个域大概率重复同一形态，且核电的 I&C 软件与我们的语料（BSN / Elevator / Microwave）距离最远。**但有一个具体检索点值得花 30 分钟**：核电 I&C 对「开发工具与开发环境」的分级隔离要求在业内以严格著称（IEC 60880 对工具的要求 + 核安全级网络的物理隔离惯例），若那里存在一条硬条款，它会是唯一能支撑「某个受监管域确实要求开发环境隔离」的成文依据——而这正是 (c) 层现在完全空缺的东西。**工作量：0.5–1 小时定点查 IEC 60880 与 IEC 61513 的目录 + Scope（preview PDF 路径已在 §4.1 验证可用）。**

### 1.9 🟡 非劣性检验的方法学出处未查（一条没被自陈的缺口）

[small_model_papers.md](./small_model_papers.md) §6.3 第 3 条记录「明确用非劣性检验框架的 SE 论文：没找到」，并正确指出「未拒绝原假设 ≠ 证明等价」，建议用 TOST 并事前声明 δ。**但它查的是「有没有 SE 论文这么做」，没查「这么做的方法学规范在哪」。** 而 [counterarguments.md](./counterarguments.md) §5.5「『相当』没有判据」正是 9 条答不上来之一，且被判为仓库 §3.5 第 4 条项下的 **C 级**风险。

现成可引的出处在 SE 之外：CONSORT 的 non-inferiority / equivalence trials 扩展、FDA 的非劣性试验指南、以及 TOST 的原始方法学文献（Schuirmann 1987 / Lakens 2017）。**这条的价值是把一个 C 级风险变成一个有出处的事前判据**，成本极低。**工作量：1 小时。**

### 1.10 ⚪ 明确判断为**不影响结论**的缺口（写出来避免无用功）

| 缺口 | 为什么不必补 |
| :-- | :-- |
| 法规侧 🔴 37 条付费墙条文 | 全部落在「已判定不覆盖」的标准里，且 §1.9 已把断言收窄到 clause/annex 级。补齐它们**最好的结果**也只是把「不覆盖」从目录级确认到条文级——而 (c) 层的死因不是这些条文，是四条反证。花钱买 ISO/IEC 全文对结论零增益 |
| arXiv API 429 / 全库枚举 | 本轮的实际检索路径（单篇 `abs` / `html` + DBLP + S2）已覆盖同一信息面。全库枚举只在做 systematic review 时必要，而已明确不做 systematic review |
| ACM DL 403 → Text2VQL 全文 | ⚠️ **它已经取得了**（Zenodo accepted version，见 §4.4）。SUMMARY 把它列为未读是错的，不是缺口 |
| 两用物项清单 700 余项条目穷举、各行业「重要数据」具体目录 | 只影响「若研究对象换成清单内受控装备则判定反转」这条**假设性**边界说明，不影响任何现有结论。ledger §2.1b 已把该反转判据写清 |
| 美国侧 air-gap 强制的进一步检索（CNSSI 1253 / Raise the Bar） | [counterarguments.md](./counterarguments.md) §1.2 已确认 32 CFR 117.18 是 risk-based 且无 air-gap 强制，并已决定把论证重心放在中国侧。继续查非公开材料是明知不可得 |
| DoD Cloud Computing SRG 原文 | 只影响条件 ⑦ 的条款号精度（现为 S 级）。而条件 ⑦ 的论证形状（IL6 准入条件 ≈ 私域隔离）不依赖具体条款号 |

## 2. 证据不足 3 条且未标注的结论（逐条）

口径：伞 PR §4.2 #1——分类式结论每类至少 3 篇**具名**支撑；不足 3 篇不打回，**但必须标注「仅 N 篇支撑」**。下表逐条给出实际具名支撑数与标注情况。

### 2.1 §3.1「可复现性是我们投稿目标社区已经接受的标准答案」→ 目标社区内实际 **1 篇**，未标注

[SUMMARY.md](./SUMMARY.md) §3.1 的措辞是「**这是我们投稿目标社区已经接受的标准答案**，不是新造」，§3 路径表则写「MDE/RE 社区至少 3 篇用了开源小模型…但给出的理由是 transparency / reproducibility / accessibility」。逐条回分册核这 3 篇：

| 被计入的论文 | 分册里的实际记载 | 能否支撑「理由是可复现性」 |
| :-- | :-- | :-- |
| REFSQ 2026 *From Online User Feedback*（[arXiv:2510.23055](https://arxiv.org/abs/2510.23055)） | 逐字「we focus on open, lightweight alternatives **to improve transparency and reproducibility**」 | ✅ **能**，这是唯一一条逐字直接支撑 |
| Pan et al. MODELS-C 2025（[arXiv:2503.22587](https://arxiv.org/abs/2503.22587)） | [mde_re_venue_scan.md](./mde_re_venue_scan.md) §2.4 逐字记载：`privacy` / `confidential` / `on-premise` / `sensitive` **全为 0**，只有部署事实（Ollama）与平价结论，**没有任何选型理由陈述** | ❌ **不能**。它证明的是「不挂动机也能发」，不是「理由是可复现性」 |
| Chou / Aydemir / Dalpiaz REFSQ 2026 | §1 动机段逐字含「on-premise deployment, which is particularly attractive for industrial settings with **privacy** or resource constraints」，§5.1 回指含「data **confidentiality**」 | ❌ **反向**。它的动机段明写 privacy；且 §6 结论收束改用纯效率口径，与「可复现性」也不同 |

⛔ **净结果：目标社区（MODELS / RE / REFSQ / SoSyM / REJ）内逐字支撑「可复现性/透明性作为选型理由」的 = 1 篇。** 另有 SE 会议侧 3 篇（Angermeir ICSE'26、Williams ICSE-NIER'26、Sallou ICSE-NIER'24）——但那是 ICSE 侧，不是「MDE/RE 目标社区」，把它们混入会使「目标社区已接受」这句话失真。**必须标注**：「目标社区内仅 1 篇逐字支撑；另有 ICSE 侧 3 篇支撑『可复现性是 SE 社区关切』这一更弱的命题」。

⚠️ 同一问题传导到 §5 建议表第 1 行：「依据：Angermeir ICSE'26 + **同社区 3 篇先例**」，强度标为「与既有工作一致的通行做法」。按上表，「同社区 3 篇」不成立。

### 2.2 §3.2「脚手架适用区间是弱模型」→ 号称「三条独立证据」，实为 **1 条外部证据 + 1 条区分论证 + 1 条自有数据**，未标注

SUMMARY §3.2 逐字：「三条独立证据同向」。逐条看性质：

| 条目 | 实际性质 | 是否为独立外部证据 |
| :-- | :-- | :-- |
| 1. Abdulkarim crossover | 外部证据，一手全文已核（[verification_log.md](./verification_log.md) §V2） | ✅ 是（但 preprint、n=8、2 模型、作者自陈后处理器污染幅度） |
| 2. Huang / Stroebl 与它不矛盾，因为是两类干预 | **这是一条区分论证（消解反证），不是支撑证据。** 它说的是「反面证据打不到我们」，不是「正面证据支持我们」 | ❌ 不是 |
| 3. 我们自己的数据（自我批判吃掉 79% token 而净收益 ≈ 0） | 自有数据，且它证明的是「自我批判无效」，不是「分解脚手架在弱模型上有效」 | ❌ 不是外部证据，且命题不同 |

⛔ **净结果：1 条外部证据，未标注。**

**更值得注意的是反向的漏计**：分册里有**两条更硬的证据没被 SUMMARY 纳入**——

- [small_model_papers.md](./small_model_papers.md) §4.6 VerIbmc 的**逐模型消融表**（Llama-3.1-8B +35 / Qwen2.5-7B +24 / GPT-OSS-20B +15 / Qwen2.5-32B +2 / GPT-OSS-120B +3），这是「脚手架收益随模型能力单调衰减」的**最干净直接测量**，且在形式化验证这个与我们同构的任务上。
- §4.2 TOSEM 的 Critique **符号反转**（GPT-4o 上 Java +0.28 / Python +0.75，o1-mini 上 −0.47 / −0.41）。

也就是说 SUMMARY 用了一组较弱的三条，而把分册里较强的两条留在了分册。**这不是「证据不足」，是「证据未被汇总」**——按「改真源不改派生物」的反面，这里是「结论出口没有把分册已有的事实带上」。

⛔ **同时漏计的是反向证据**：[small_model_papers.md](./small_model_papers.md) §4.3 Konstantinou 的复现研究在 **GPT-4o-mini**（一个弱/小模型）上发现朴素提示打败四条带执行反馈的流水线，且调用量只有一半。**这直接构成「脚手架适用区间是弱模型」的反例**，而 SUMMARY §3.2 一字未提。按仓库 §3.5，只汇总同向证据属选择性报告。

### 2.3 §2.1 四条反证 → 逐条来源数

| 反证 | 具名来源数 | 级别 | 标注情况 |
| :-: | :-: | :-- | :-- |
| **1** DoD GenAI.mil 跑商用模型处理 CUI（IL5）+ Azure IL6 | **4**（war.gov 三篇 release + Azure devblog；另有微软 compliance scope 表） | 🟢 / M（devblog 为 S） | ✅ 够 3 条，无需标注 |
| **2** Anthropic「ITAR data **can** be processed via AWS Bedrock」 | **1**（support.claude.com 单页） | 🟢 已核 | ⛔ **单来源单页，未标注** |
| **3** OpenAI API Platform 已取 FedRAMP 20x Class C | **1**（fedramp.gov marketplace FR2533155773） | ⚠️ [counterarguments.md](./counterarguments.md) §7.3 第 2 条自标 **S 级 / 待人工核验**（字段术语疑为站点改版新词） | ⛔ **单来源，且 SUMMARY 写成 🟢 事实句，与分册的 S 级标注冲突** |
| **4** 涉密下私域部署本身也不合规（保密法第三十一条(三)） | **1 条条文 + 我方推论**（「企业普通私有服务器仍属非涉密信息系统」这一步是我们自己的解释，无官方释义、无案例、无保密行政管理部门文件支撑） | 🟢 条文 M；推论为 I | ⛔ **未标注它含一步我方推论**。SUMMARY 把它写成「反直觉**致命**反例」，措辞强度高于证据 |

### 2.4 §1 Q1「三处独立自陈排除」→ 三处中 **两处同源**，独立性不成立；且实际可用的自陈排除多于三处

- IEC 61508-1:2010 §1.2 m) 与 EN 50716:2023 Introduction 的措辞，[regulatory_ledger.md](./regulatory_ledger.md) §1.8 自己写明「**与 IEC 61508-1 §1.2 m) 的措辞高度重合**——这不是巧合」（轨交标准派生自 IEC 61508）。**同源措辞不构成独立观测**。
- 真正独立的第三处是 ISO/SAE 21434 §1「does not prescribe specific technology or solutions」。
- 反过来，**ledger 里还有两处自陈排除没被计入**：IEC 62304 Introduction（「does not specify an organizational structure…」，line 69）与 DO-356A 官方描述（「does not provide guidelines concerning the structure of an individual organization…」，line 65）。用这两处替换 EN 50716，就能得到**三处真正独立**的自陈排除。
- **结论**：命题本身站得住，但「三处独立」这个说法要么改成「两处独立 + 一处同源确认」，要么换用 62304 / DO-356A 补足。

### 2.5 §2.1「(a) 不能用未获授权的商用端点（五条独立路径）」→ 五条中最宽的一条为 🟡，未在 SUMMARY 标注

ledger §0b 的 (a) 行列了 5 条路径，并明说「① 中国等保是**唯一不需要任何前置认定**的路径」——即五条里最宽、最可能被论文实际使用的那一条。而它的核验状态是 🟡：[regulatory_ledger.md](./regulatory_ledger.md) §2.4 自陈条文取自中科院合肥托管的可检索 PDF，openstd 官方预览为 JS 页不可取，并写明「**正式引用前必须人工在 openstd 官方预览页复核一次条款号**」。另外 5 条中的 ②③⑤ 都需前置认定（CDI / 受控技术数据 / 国家秘密）。SUMMARY 只写「五条独立路径」，未带这两条限定。

### 2.6 §4.3「3,740 条题录只有 2 篇写出这条因果」→ **分母混用**

3,740 = MDE/RE 侧 1,455 + SE 期刊侧 2,285（[mde_re_venue_scan.md](./mde_re_venue_scan.md) §1.1–1.3）。而「只有 2 篇写出这条因果」是**MDE/RE 侧**的结论——SE 期刊侧恰恰有 6 篇把它写进贡献句（§2.6）。**把 MDE/RE 侧的分子配上含 SE 侧的分母，使这个比率既低估了 SE 侧的密度、又夸大了 MDE/RE 侧的扫描规模。** 正确写法是「MDE/RE 侧 1,455 条题录、137 条 LLM 信号题录中只有 2 篇」。这与仓库「比率只能跨同类分母比」是同一类错误。

### 2.7 §3 路径表「含本地 Ollama 与 **Qwen-14B**」→ 沿用了分册明确警告过的误标

[mde_re_venue_scan.md](./mde_re_venue_scan.md) §2.3 限定 2 逐字警告：「它说的『Qwen-14B』**不是原版 Qwen-14B**，而是 **DeepSeek-R1-Distill-Qwen-14B**（论文脚注给出 HuggingFace 链接）…我们若引用它做『Qwen 级模型表现』的论据，**会引错对象**」。SUMMARY 路径表仍写「Qwen-14B」。这属于「查了但没用上那个事实」。

## 3. ⚠️ 覆盖边界表述问题

### 3.1 🔴 §6 的覆盖表只覆盖旧 story 的证据族，新 story 的两个证据族一行都没有

§6 四行 = MDE/RE 侧、SE 会议侧、法规、检索工具。**缺的是**：

| 缺的证据族 | 分册里已自陈的边界（应上到 §6 而没上） |
| :-- | :-- |
| 小模型 + 方法学补偿（[small_model_papers.md](./small_model_papers.md)，§3.2 的证据源） | §6.1 六条：非 systematic review、**CCF A 会议正文覆盖为零**、与我们同构的样本**只有 VerIbmc 一篇**、中文/白皮书零覆盖、时间窗 2023-06 至 2026-06、**样本质量方差极大**（并列 TSE/TOSEM 与「测试集仅 100 条合成样本」的 preprint）；§6.2 **18 项待核验** |
| 反方与预答（[counterarguments.md](./counterarguments.md)，§3.1 与 §4 的证据源） | §7.1 末：非 systematic review、机会性检索；§7.2 **13 行访问异常**；§7.3 **14 项 I 级 / 待核验，明写「不得写成事实句」** |

**后果具体而不抽象**：一个只读 SUMMARY 的读者不会知道 §3.2 的支撑主体是 2026 年 preprint（Abdulkarim / VerIbmc / Konstantinou / Sepidband 全部 preprint、venue 待核），也不会知道 §3.1 的一条支撑（Angermeir 的「推荐开源模型」）在分册里没有对应的逐字推荐句（见 §4.2）。

### 3.2 🔴 「MDE / RE 侧的『未见』有证据力」把标题-摘要级零命中升格成了一般证据力

[mde_re_venue_scan.md](./mde_re_venue_scan.md) §5.1 第 1 条逐字：

> 「⛔ **由此导出本轮最大的假阴性来源**：⛔ 一篇在正文某处写了『因为保密所以用本地模型』而**标题与摘要都没写**的论文，本轮**根本扫不到**…**故所有『零命中』严格说都是『标题与摘要层零命中』，不等于『正文层零命中』。**」

而 SUMMARY §6 该行的边界栏只写「这一侧的『未见』**有证据力**」。**这是限定丢失**：有证据力的是「标题与摘要层未见」，不是「未见」。修法很简单——把该栏改成「标题与摘要层的『未见』有证据力；正文层未覆盖（1,029 份摘要、非全文）」。

### 3.3 🔴 §6 说「两条已知未读」，实际未读项远多于两条

§6 只列 [arXiv:2607.03691](https://arxiv.org/abs/2607.03691) 与 Text2VQL 全文。**至少还有三类必须列**：

1. **Karmarkar et al., SANER 2024《Navigating Confidentiality in Test Automation》**（[DOI](https://doi.org/10.1109/SANER60148.2024.00041)）——[se_motivation_survey.md](./se_motivation_survey.md) §6.3 把它列为**最高优先级之一**并写明「保密写在标题里，**极可能是本轮最强的承重案例**」。它是全轮**唯一一篇标题即保密动机的正式发表 CCF B 论文**，而全文从未取得（IEEE 付费墙、无 preprint、程序页无摘要）。漏列它使 §6 的「未读」清单严重不完整。
2. [small_model_papers.md](./small_model_papers.md) §6.2 的 **18 项**待核验，其中第 1 项（TOSEM 正式版的模型集与数字）自陈「**这是我们最想引的一条**」而 ACM DL 403 未取得。
3. [counterarguments.md](./counterarguments.md) §7.3 的 **14 项** I 级 / 待核验。

### 3.4 🟠 Text2VQL 一行与分册直接冲突（SUMMARY **低报**了自己的覆盖）

- SUMMARY §6 逐字：「⏳ Text2VQL 全文（⛔ ACM DL 403，⛔ **承重性未判定**）」。
- [mde_re_venue_scan.md](./mde_re_venue_scan.md) §2.2 逐字：「读到什么程度 | **全文**（⛔ ACM DL 403，改由作者 Zenodo artifact [10.5281/zenodo.12742459](https://doi.org/10.5281/zenodo.12742459) 取得 accepted version；已将其摘要与出版方摘要逐字比对，归一化后完全一致）」，判定栏 = **装饰**，并给了三条决定性证据与我方独立复算的词频表。

⚠️ 分册内部也有一处同名不一致：§3.2 净命中说明写「§2.2 与 §2.3（**未判定**）」，而 §2.2 / §2.3 的判定栏都是**装饰**。两处需统一，且以 §2.2 / §2.3 的正文判定为准。

### 3.5 🟠 §1 Q1「这一族**在设计上**就不管这件事」丢掉了 ledger §1.9 的核验层级限定

ledger §1.9 逐字：「可断言的是『**clause 级 / annex 级**不存在保密条款』；⛔ **不能**断言埋在 `5.1.x` / `6.5.4.x` 这类深层编号里的**单条要求**也不存在」，并列出 5 条未核验条文。SUMMARY §1 的 Q1 行把结论表述为「这一族**在设计上**就不管这件事」——这是一条关于整个标准族设计意图的一般化断言，而支撑只有目录级/Scope 级覆盖 + 2 处独立自陈（见 §2.4）。**建议改为**「在 clause / annex 级不存在保密条款，且至少两处标准以 Scope 自陈把 security 排除在外」。

### 3.6 ✅ 做得好的部分（明确记下来，避免过度整改）

- §6 开头「本轮不是 systematic review，不得写成 systematic mapping study，**不得说『据我们所知不存在』**」——全轮**没有出现**任何一处「据我们所知不存在」式表述，六个文件均未违反。这条守住了。
- 每个分册各自的覆盖边界章节质量都高于 SUMMARY 的汇总：ledger §1.9 / §5、se_motivation §6.1、mde_re §5.1–5.3、small_model §6.1、counterarguments §7.2–7.3 都写明了范围限定与访问异常。**问题不在分册，在汇总环节的删减。**
- 访问异常一律记为「入口已定位 / 访问异常」而非「事实不存在」，符合仓库 §2 情报库原则；`⚪ 查无此法`（等保条例）与`⚪ 未公布`（工作秘密管理办法）的处理尤其干净。
- mde_re §1.3 的**已知阳性召回自检**（用前一轮认定的 Zhong et al. 检验扫描器能否命中）是一个应当推广到其他扫库的做法。

## 4. 该做未做的一手核验

### 4.1 🔴 §3.1（新推荐的主动机）零条一手核验记录

[verification_log.md](./verification_log.md) 的定位逐字是「只放**主 session 亲自取原文核过**的条目，不放 subagent 的转述」，全文只有 **V1**（Zadenoori 2% 句式）与 **V2**（Abdulkarim crossover）——**两条都服务于 §3.2**。而 §3.1「可复现性是社区已接受的标准答案」是 SUMMARY 推荐的**主动机**，其承重引文（Angermeir ICSE'26）**在 verification_log 里没有条目**。

⚠️ 加上一处口径不一致：[counterarguments.md](./counterarguments.md) 的级别定义是「**M** = 主 session **或 subagent** 取到一手原文逐字核过」，而 verification_log 的 M 只含主 session。**因此 counterarguments 里标 M 的 Angermeir 引文，未达 verification_log 的 M 标准**，而 SUMMARY 把它当作整条路线转向的依据。**该做**：主 session 亲自取 [arXiv:2510.25506](https://arxiv.org/abs/2510.25506) 全文，逐字核那两句，并补一条 V3。

### 4.2 🔴 「Angermeir 逐字推荐开源模型作缓解」——可得逐字不支持「推荐」

- SUMMARY §3 路径表逐字：「ICSE'26 Angermeir：85 篇 0 篇完全复现，唯一 LLM 特异的失败因素就是模型弃用，且**逐字推荐开源模型作缓解**」。
- [counterarguments.md](./counterarguments.md) §3 材料 ① 给出的两句逐字是：「**The only factor directly linked to LLMs was the usage of deprecated models, an issue exclusive to commercial models.**」与「**the hurdles towards deprecation for open source models are higher**」。

⛔ 第二句是一条**比较性事实陈述**（开源模型的弃用门槛更高），**不是一条建议句**。「逐字推荐」这个说法在现有材料里找不到对应文本。这是 §5 建议表第 1 行「依据」栏与 §3.1「社区已接受的标准答案」的关键一环，**必须回原文确认该文是否真有 recommendation 形态的句子**；若没有，措辞应改为「该文认定模型弃用是唯一 LLM 特异的复现失败因素，并指出开源模型的弃用门槛更高」。

### 4.3 🟠 verification_log §V2 读了全文，但漏掉了分册标为「必须解开才能引」的那处矛盾

[small_model_papers.md](./small_model_papers.md) §6.2 第 14 项逐字把它列为 级：Abdulkarim 论文内部**自相矛盾**——实验设置节写单提示基线用 **3-shot**（「aiming to improve upon the baseline accuracy」），框架定义节写它是 **2-shot**；并写明「**这个矛盾必须解开才能引**」，因为它决定「基线是否被有意加强」这条限定成立与否，从而决定 crossover 结论的分量方向。

而 [verification_log.md](./verification_log.md) §V2 是主 session 亲自读了该文全文并列了**五条限定**（preprint/n=8、后处理器污染、reasoning 轴自定义、任务不同、反过来伤我们），**其中没有 shot 数矛盾这一条**。⛔ 也就是说：一手核验做了，但漏了分册指名的阻塞项。**该做**：回该文比对两节措辞，把结论写进 V2。

### 4.4 🟠 等保 GB/T 22239-2019 条款号未按 ledger 自己的要求人工复核

ledger §2.4 自陈「⚠️ **正式引用前必须人工在 openstd 官方预览页复核一次条款号**」，且全表为 🟡。而 §0b 把这条路径描述为 (a) 层里**唯一不需要前置认定**的一条——即最宽、最可能被论文实际使用的那条。这项复核**未做**，SUMMARY 也未标注（见 §2.5）。

### 4.5 🟠 承重结论所依赖的厂商侧事实全为 🟡 / S / I，未做逐字核

见 §1.5 的表。要点：**杀死原版 story 的那几刀（ZDR / 区域驻留 / 默认不训练 / OpenAI FedRAMP 术语）本身的证据级别低于它们所推翻的结论所需的强度。** ledger §4.3「主 session 亲自复核的条款」清单里有 7 项，全部是**法条**（eCFR / acquisition.gov / npc.gov.cn / NIST PDF / Anthropic 支持页），**没有一项是厂商条款文本**。

### 4.6 🟡 Karmarkar SANER 2024 全文（唯一标题即保密的正式发表论文）

见 §3.3 第 1 项。它同时是 se_motivation §6.3 的高优先级待核项与 §7 落档（A−）的潜在改档因素——若它是承重-C，中口径下 CCF A/B 正式 venue 的承重篇数会从 2 变 3。**取得路径**：机构 IEEE 权限；或联系作者（TCS Research / Synopsys，作者邮箱通常在同作者的其他 arXiv 论文里可得）。

### 4.7 🟡 §3.2 的两条外部证据本身的 venue 状态未核

[small_model_papers.md](./small_model_papers.md) §6.2 第 7 项（VerIbmc venue 未核）与第 14 项（Abdulkarim venue 未核）。值得注意的是 [mde_re_venue_scan.md](./mde_re_venue_scan.md) §4.2 已经给出了**一套可用且已验证的核验规程**（DBLP 为准 + 确认该作者收录时间线最新 + arXiv comments 只能正向证明），并用它成功纠正了两处误判。**同一规程未被应用到 §3.2 的两条主证据上。**

## 5. 建议的补做清单（按性价比排序，注明工作量）

| # | 动作 | 它补哪条结论 | 工作量 | 性价比 |
| :-: | :-- | :-- | :-- | :-: |
| **1** | **就地修 SUMMARY §6**：把两个缺失证据族的边界补上（§3.1）；把 MDE/RE 行改成「标题与摘要层」（§3.2）；把「两条已知未读」扩成完整清单含 Karmarkar SANER'24（§3.3）；删掉 Text2VQL 那行的错误状态（§3.4）；给 Q1 补 clause 级限定（§3.5） | 覆盖边界的诚实性——**当前是最严重的问题** | **1–2 小时**，纯改文档，不需检索 | |
| **2** | **就地补标注**：§2 逐条按第 2 节结论标「仅 N 条支撑」；改「三条独立证据」为「1 条外部 + 1 条区分 + 1 条自有」；改「三处独立自陈排除」（或换用 62304 / DO-356A）；修 §4.3 的分母；改「Qwen-14B」为 DeepSeek-R1-Distill-Qwen-14B；把「逐字推荐开源模型」降为可得逐字支持的说法 | §1 / §2.1 / §3 / §4.3 全部结论的证据强度标注 | **1–2 小时**，纯改文档 | |
| **3** | **把分册已有的强证据搬进 §3.2**（VerIbmc 逐模型消融、TOSEM 符号反转），并把反向证据（Konstantinou 在 GPT-4o-mini 上朴素提示胜出）一并写入 | §3.2 从 1 条外部证据变 3 条，同时消除选择性报告风险 | **1 小时**，材料已在分册 | |
| **4** | **读 [arXiv:2607.03691](https://arxiv.org/abs/2607.03691)** | 它可能推翻 §3.2 与 small_model §4 整条链；不读它属选择性报告 | **1 小时** | |
| **5** | **反向雪球三个起点**（Angermeir 被引 / Abdulkarim 双向 / Chou 参考文献），见 §1.1 | §3.1 目标社区支撑从 1 抬到 ≥3；§3.2 的同域证据补强；最不利论文的比较框架 | **2–3 小时**，工具已验证可用 | |
| **6** | **主 session 一手核 Angermeir 两句 + 补 V3；顺带解开 Abdulkarim 的 3-shot/2-shot 矛盾并补进 V2**（§4.1 / §4.2 / §4.3） | 新主动机的承重引文首次获得一手记录；§3.2 的阻塞项解开 | **1.5 小时** | |
| **7** | **ICSE / ASE / FSE / ISSTA + FM 族 venue 级扫库**（复用 MDE/RE 那套 DBLP 镜像 + S2 管线），见 §1.2 / §1.6 | §3.2 的社区定位；small_model §4.9 的文献真空主张**目前无资格提出** | **6–9 小时**（1 个 agent） | |
| **8** | **中文文献首轮扫描**（《软件学报》《计算机学报》《计算机研究与发展》+ NASAC，2023–2026），见 §1.3 | 唯一能闭环的法域内的先例，有无都是可用结论 | **3–4 小时** | |
| **9** | **厂商条款逐字核**（OpenAI Business Terms / DPA / Enterprise Privacy、Anthropic Commercial Terms / Usage Policy、Azure DPA .docx），见 §1.5 | §3.4 与 §2.1 反证 2/3 的证据级别；**可能反向对我方有利** | **2 小时** | |
| **10** | **工业界公开调查扫描**（Stack Overflow / JetBrains / Cisco / Gartner 的「组织限制公共 GenAI 比例」题目），见 §1.4 | §5.6「工业举证」这条答不上来，可能是假缺口 | **1–2 小时** | |
| **11** | **非劣性检验方法学出处**（CONSORT non-inferiority 扩展 / TOST 原始文献），见 §1.9 | §5.5「『相当』无判据」这条 C 级风险变成有出处的事前判据 | **1 小时** | |
| **12** | **等保 GB/T 22239 条款号在 openstd 官方页人工复核**，见 §4.4 | (a) 层最宽那条路径的核验等级 🟡 → 🟢 | **0.5 小时**（需人工开浏览器） | |
| **13** | **不利监管动向补证**（FDA AI-in-development 指南 / IMDRF AI 文件 / UL 4600 / EASA AI Roadmap 2.0），见 §1.7 | EASA NPA 那条目前是孤证，无法判断严重性与是否孤例 | **2–3 小时** | |
| **14** | **核电侧定点查 IEC 60880 / IEC 61513 目录与 Scope**，见 §1.8 | 唯一还可能给 (c) 层提供成文依据的候选域；大概率仍为「不覆盖」 | **0.5–1 小时** | |
| **15** | **Karmarkar SANER'24 全文**（机构 IEEE 权限或联系作者），见 §4.6 | 唯一标题即保密的正式发表论文；可能改动 Q3 的中口径落档 | **依赖权限，动作本身 0.5 小时** | |
| — | ⚪ **不建议做**：买 ISO/IEC 付费全文补 🔴 37 条 · arXiv 全库枚举 · 两用物项清单 700 项穷举 · DoD SRG 原文 · 美国 air-gap 强制的进一步检索 · 各行业「重要数据」目录 | 见 §1.10 逐条理由 | — | — |

**一条总的观察**：第 1–6 项全部**不需要新检索**，只需改文档或用已在手的材料与工具，合计约 **8 小时**，而它们覆盖了本审计判定为最严重的全部问题（覆盖边界失真、支撑数未标注、强证据留在分册、反向证据未汇总、承重引文无一手记录）。真正需要新检索的第 7–15 项合计约 **20 小时**，且其中没有一项是「结论能不能立」的前提——它们改变的是**证据强度与可主张的范围**，不是结论方向。
