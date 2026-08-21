# C3 覆盖审计：这轮调研漏了什么

> **它是层 4 三路里的第三路**（C1 事实核验 · C2 反驳 · **C3 覆盖**）。⛔ 它不判单条证据的对错，⭐ 它判**覆盖面**。
>
> ⭐ **它的输入**是 22 路调研（来源 C+D 的 16 路 + Q2 的 6 路）各自的 `search_log` 与 `gaps`，共 **17.4 万字符**；⭐ 审计员对入口声明做了**机械核对**（venue 名、检索入口、跨路重复来源、失败记录的 grep 计数）。
>
> **档位标记**：⭐ 「机械核对」栏为【实测】；⭐ 严重度与补法为【AI 建议·待确认】。

## ⛔⛔ 三条机械核对出来的硬事实

⭐ 后面每一节都引用它们。⛔ 它们是 grep 计数，⛔ 不是印象。

| 核对项 | 声称 | ⛔ 实测（全文 grep） |
| :-- | :-- | :-- |
| **结构化检索入口** | ICSE / FSE / ASE / ISSTA / TSE / TOSEM 等 venue 族 | ⛔ DBLP 仅 **2 处**、**都是元数据核对**（卷期、DBLP key），⛔ 从未用于枚举 venue；ACM DL 与 IEEE Xplore 的**全部 6+8 次出现都是 403 / 付费墙 / 取不到**；Scopus / Web of Science / Google Scholar **各 0 次**；`snowball` / 前向后向引用 **0 次** |
| **语种** | —— | ⛔ 非英文检索 **0 次**（CNKI / J-STAGE / eLibrary / 德俄印尼语关键词全 0）。⚠️ 出现的 2 处「中文」是对本地中文 `DESC.md` 做 grep，⛔ 不是中文文献检索 |
| **`gaps` 栏** | 每路都要写 | ⛔ **16 路 C+D 全部写了；Q2 的 6 路一路都没写**。⚠️ 而 Q2 恰恰是**唯一以空集为结论**的一侧 |

## ⛔ 已照改的三条（本轮就地更正）

| # | 指控 | 处置 |
| --: | :-- | :-- |
| 1 | ⛔⛔ **「在本轮覆盖的 venue 族内未见 X」这个 claim 形状不可写** —— ⭐ 覆盖的单位**根本不是 venue** | ⭐ 已改为**检索式口径**（附查询串表）。见 [c3_differentiation.md](../../c3_differentiation.md) §覆盖范围声明 与 [SUMMARY.md](./SUMMARY.md) §1 |
| 2 | ⛔ Q2 的 **63 未去重**（≥6 组跨路重复），⛔ 且它是**条件分母**（准入判据「三轴占住两根」使 (iii)-强/单轴的工作进不了分母 —— ⭐ **筛子决定了结论**） | ⭐ 已去重为 **52 篇**并明写条件分母含义。⭐ 顺带白捡一份判定者间一致性数据 |
| 3 | ⛔ 非英文检索 0 次，⚠️ 而语料本身多语 | ⭐ 已作为**未声明的语言边界**写进覆盖声明 |

## ⛔ 一条指控经核对**部分不成立**，须精确更正

⚠️ C3 §2.4 报「本地语料四分片 454 篇 vs 库里 679 个目录，**差 33% 未说明**」。

⛔ **核对结果：454 是过完边界门后的全部界内候选，覆盖率 100%。** 复算：`state_machine_types/SUMMARY.md` 的普通表共 **669 行**，其中界内 **454** · 界外 **215**（timed / Petri / CSP / CCS / process algebra / hybrid / probabilistic / stochastic / Markov / orthogonal）—— ⭐ 那 33% 是**边界门刻意剔除**的界外条目，⛔ 不是漏了。

⭐ **但这条指控有一个真实残留，⛔ 且是我自己工具的缺陷**：另有 **23 行**因**列数不足被静默跳过** —— ⭐ 它们是**综述表**（13 列 schema，普通表是 19 列），⛔ 而我的筛法要求 `len(cells) >= 19`。⚠️ 那 23 行里含 **10 篇跨形式主义综述**，其中两篇与 L2 高度相关：

- `Model Checking of Statechart Models: Survey and Research Directions`（2004）
- `Formalizing UML State Machines for Automated Verification — A Survey`（2023）

⛔ 而 [CONTINGENCY_L2.md](../../../archive/legacy_20260821/CONTINGENCY_L2.md) §4.1 层 1b **恰好警告过**这件事（逐字）：「`state_machine_types/*/survey.md`（10，跨形式主义综述，**单位收益最高**）；⛔ 只写 `desc.md` 的 glob 会漏掉 101 篇」。⭐ **我踩的正是这个坑的变体** —— ⛔ 不是 glob 漏了，是**列数检查**漏了。

## ⛔ 必补、⭐ 但归下一轮的四项

⛔ 本轮时间与预算不足，⭐ 逐条登记以免丢失。⚠️ **在前两项完成之前，相关谓词的「领域里没有对应检查」这类陈述不成立。**

### 1 ⛔ 必补 · 一致性测试 / 测试预言整个传统

⭐ **它是仿真族 6 条谓词的语义原产地** —— 「给输入序列、跑若干步、断言落在哪个状态 / 变量什么值 / 事件被不被消费 / 能不能停机」**就是** conformance testing 的定义性活动，⛔ 不是它的边角。

⛔ **一篇都没系统进入。** ⚠️ 而**四路互不相识的 agent 各自独立写下「这大概要到 test oracle / conformance testing 文献里找」**，⛔ 然后没有任何一路被派去找。

⭐ 补法：入口 DBLP 的 ICST / ISSTA / ICTSS / TAP / FATES / A-MOST 年度页 + Springer LNCS 的 ICTSS 系列；词簇 `conformance testing finite state machine` · `state verification sequence` · `test oracle expected state after input` · `ioco relation quiescence` · `all-transitions coverage criterion`。⭐ 特别指定取 Ammann & Offutt 第 7 章 graph coverage 与 Tretmans 的 ioco 定义。

### 2 ⛔ 必补 · 模型质量 / model smell / UML 缺陷分类学

⭐ **它是结构族 10 条谓词的天然出处** —— ⛔ 而结构族恰是本轮最惨的一族。

⛔ `model smell` 全文出现 **12 次**，**每一次都在「本分片没有 / 下一轮该换到这个方向」的语境里**；⛔ 从未有外部检索把它当轴打过。⚠️ **五路各自指过路。**

✅ **最高价值单点已取到**：**Torre et al. 的 UML 一致性规则** —— ⭐ TR（1605 行）与**博士论文（9022 行）**均已全文入手，见 [recovery_log.md](../../recovery_log.md)。

⛔⛔ **但本节上一版对它的描述被证伪，须更正**：⚠️ 原写「Torre et al. **JSS 2018**（含 **687→119** 条规则 + **106 位专家验证**）」—— ⭐ 取件后逐字核实，**那是把三篇论文的事实混成了一篇**：

| 篇 | 逐字事实 |
| :-- | :-- |
| **TR SCE-15-01** | **603 → 116**（「We then consolidated a set of **116** UML consistency rules」） |
| **博士论文 / JSS 2018** | **687 → 119**（「an initial set of **687** UML consistency rules … finally coalesced into **119**」） |
| **SQJ 2022** | ⭐ **106 位专家**，⛔ 且验的是 **116** 条（「**106 respondents** completed the questionnaire, resulting in a response rate of 23.3%」） |

⭐ **只有博士论文把三者统一。** ⛔ 引用时必须按篇分开说。

⚠️ **另两处元数据同样被证伪**（详见 [recovery_log.md](../../recovery_log.md)）：⛔ Salsa ASE 2001 的作者是 **Sims / Cleaveland / Butts / Ranville**（Reactive Systems + **Ford**），⛔ 既不是 Heimdahl 也不是 Heitmeyer；⭐ Bögli 那篇的真实标题是 **"Temporal Logics Meet Real-World Software Requirements: A Reality Check"**。

⭐ **另外**：原建议的头号入口 `squall.sce.carleton.ca` **已下线**（⚠️ DNS 解析到 IP 但 80 端口 filtered）—— ⭐ **这解释了前几路为什么卡住：URL 是对的，服务器不在公网了**。可用替代是 **Carleton Scholaris/DSpace**。

### 3 ⚠️ 建议补 · 控制 / 自动化工程共同体自己的文献

⛔ IFAC 只试过一篇（撞 ScienceDirect 后放弃）；RESS **0 次**；IEEE CASE **0 次**；IECON **0 次**；⛔ **WODES 0 次**（⚠️ 而它是监督控制 / DES 的主场，⭐ 本轮 Supremica 那条证据正是从这条线来的）。

⭐ **为什么重要**：本研究的语料是**控制系统**。「这类检查在领域里反复出现」这句话，⭐ **最强的说法人是这个领域自己**，⛔ 不是软工会议。⚠️ 而制造/产线自动化、过程工业 SIS、机械安全 e-stop 三个方向全部空集，⛔ 理由都是「可及文献要么走 timed automata、要么是厂商/博客」—— ⭐ 这个判断只在 CS 检索面上成立。

⭐ 补法：**IFAC-PapersOnLine（2015+）在 ScienceDirect 上是开放获取的**（⚠️ 本轮撞的是 2008 年前不开放的那批）。

### 4 ⛔ 必补 · 「这个缺陷真的发生了」这一侧

⛔ 全文 `prevalence` **0 次** · `发生率` 1 次（且是「没找到」）· `empirical study` 1 次 · `bug study` **0 次**。⭐ 唯一成功的频次数据**全部落在 BMC 三条**，⛔ 结构族与仿真族一条频次数据都没有。

⭐ **为什么重要**：「某工具把它做成 Error 级规则」是**弱形式**的普遍性（有人认为该查）；「在 N 个真实模型里这类缺陷出现了 M 次」是**强形式**（确实会错）。⛔ 现在 19 条里只有 3 条有强形式，⚠️ 且都是最不需要论证的那 3 条。

⭐ 补法：① 开源模型语料实证（Lindholmen dataset · models-db · GenMyModel 语料）配 `defect` / `smell` / `violation frequency`；② ⭐ **变异算子分类学**（Stateflow / EFSM mutation operators —— ⭐ 其算子表本身就是「工程界认为哪些地方会错」的经验编码，⛔ 且直接命中 `effect_declared` 的方向维度）。

## ✅ 最伤覆盖声明的一条：**伪缺口** —— ⭐ **已闭合（2026-08-12）**

⭐ **两条已全部取到全文**，⛔ 且原诊断的错因逐条查清。⭐ 回收还顺带取到另外 7 篇付费墙论文（10 个目标 9 个成功），⛔ 并**证伪了三处元数据**。详见 [recovery_log.md](../../recovery_log.md)。

⚠️ 下面保留原始指控的记述，⛔ 因为它说明了**这类缺陷长什么样**：

⚠️ C3 逐字核实出**两个实例** —— ⛔ 同一份 PDF，一路取到了、另一路把它登记成头号缺口，⛔ **两路互不知道**：

| 论文 | 一路记 | ⭐ 另一路记 |
| :-- | :-- | :-- |
| **Heimdahl & Leveson TSE 1996** | 「konkuk 镜像握手报 `KEY_USAGE_BIT_INCORRECT`，无法取全文，故没写进 findings」+ 称它是「**最值得优先补的一条**」 | ⭐ 「konkuk 镜像，**`curl -k` 绕过证书链问题** → `pdftotext -layout` → **1148 行**」 |
| **Dwyer ICSE 1999** | 「免费 PDF 是 CCITT 扫描图，tesseract 未安装，OCR 走不通，**故未提交该条目**」 | ⭐ **另外四路**都抽出了正文，其中一路：「用 `pdf_extractor -m text` 即可解出（含 Table 1 的 Absence 85 / Universality 119 / Total 555）」—— ⛔ **那个「需要 OCR」的诊断本身是错的** |

⛔⛔ **它意味着：一部分自报「未见」其实是「本路的工具没跑对，而同一轮别路已经拿到了」。** ⭐ 任何形如「在本轮覆盖内未见 X」的 claim，⛔ **必须先把这类伪缺口清掉** —— ⚠️ 否则它陈述的是**工具状态**而不是**文献状态**。

⭐ **配套的结构性发现**：付费墙**不是随机噪声，⛔ 它与证据强度正相关**。失败记录打中的是 Heitmeyer TOSEM 1996 · Heimdahl & Leveson TSE 1996 · Torre et al. JSS 2018 · Autili TSE 2015 · Vu/Haxthausen SCP 2017 · Bögli FormaliSE 2025 · Lange & Chaudron 系 · Salsa ASE 2001 —— ⛔ **每一条都被某一路评为该谓词的最强候选**。⭐ 结果是证据表被系统性地向「开放获取的、较新的、arXiv 的、工具文档的」那一侧倾斜。

✅ **该补法已执行，⭐ 10 个目标 9 个取到全文**（见 [recovery_log.md](../../recovery_log.md)）。⭐ 唯一真缺口是 Lange, Chaudron & Muskens, IEEE Software 2006 —— ⛔ 8 条入口逐条在册，⭐ 且其内容与已取到的博士论文重叠，实质不构成缺口。

⭐⭐ **回收顺带产出三条可复用结论，⛔ 其中一条推翻了本节的一个前提**：⛔ 「Unpaywall / OpenAlex 的 `best_oa_location`」这一步**并不可靠** —— ⚠️ Autili 那条**三大聚合器齐报 `CLOSED` 且三家都错了**，⭐ 破局靠 **OpenAIRE API** 的 `originalId` 字段（⛔ 那是三家都丢掉的）。⭐ 另两条：⛔ 下载后必须 `file` + `pdfinfo` 双查（本轮抓到两类伪 PDF：DTIC 的 1408 字节维护页 · Zenodo 的 763 字节反爬页）；⚠️ Unpaywall 对占位邮箱直接 HTTP 422。

## ⚠️ 三条「没坦白的少于 3 篇支撑」

⭐ 各路已坦白的不重复（`cardinality` 0 · `terminates` 半边 · 医疗域为零）。⛔ 以下是**没坦白的**：

1. ⛔ **`initial_target` 的 6 个来源里同行评议为零** —— ⚠️ 全是商业工具文档、行业规范、开源实现与方法学；⛔ 呈现为「6 个互相独立来源、跨 3 类主体」而**未说明学术出处为 0**。⭐ 真实图景：学术侧 2 条（其中一条是 1987 年的 Harel），工程侧 6 条。⛔ **这个构成必须写进表**，⚠️ 否则审稿人一查就是「你们最基础的一条谓词全靠 MathWorks 文档」。
2. ⚠️ **Dwyer 1999 的同一行在两条谓词上被重复计为独立来源** —— ⭐ 已由标识符归一部分修掉（`invariant` 文献侧 31→28），⛔ 但**跨谓词共用**这一层仍未在表里显式标注。⭐ Dwyer 在全文出现 **41 次**，被至少 **5 条谓词**各自当作独立来源之一。
3. ⚠️ **四个本地分片的零命中不是四次独立观测** —— ⛔ 它们取自**同一个库的四个切片**。⭐ 应合并计为**一次库级观测**。

## ⛔ Q2 特有：(iii) 那一侧的补检索**正在跑**

⛔ 详见 [c3_differentiation.md](../../c3_differentiation.md) 开头〈更正 3〉与末尾〈目标措辞〉。⭐ 两路补检索：**assurance case / GSN**（⭐ 形状最近，⛔ 被负责路自己声明为未查）+ **(iii) 的四类成熟形态**（形式化 witness / RV verdict / rule provenance / 可复现失败用例）。

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | ⭐ 伪缺口与付费墙回收完成（10 个目标 9 个全文）；⛔ 本节对 Torre 的描述被证伪并更正（687→119 与 106 专家不在同一篇）；⛔ 「Unpaywall/OpenAlex 的 best_oa_location」这一步被证明不可靠。 |
| 2026-08-12 | 建立。记录 C3 的三条机械硬事实、已照改的三条、经核对部分不成立的一条（含我自己工具的列数检查缺陷）、必补但归下一轮的四项、伪缺口与付费墙偏置、三条未坦白的弱支撑。 |
