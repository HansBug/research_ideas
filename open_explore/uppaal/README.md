# `uppaal/` 论文集 README

## 1. 论文集定位

`open_explore/uppaal/` 是一个面向 `UPPAAL` 谱系的专题论文集，用于系统沉淀 `UPPAAL` 相关的核心理论、关键算法与数据结构、工具工程能力演进，以及基于 `UPPAAL` 的代表性应用工作。

它当前位于 [open_explore/](../README.md) 下，而不是直接放入某个 `project_*`，原因是这类材料既服务博士研究中的形式化验证与状态机方向，也包含一部分尚未完全确定最终归属的基础技术脉络。

## 2. 设立宗旨与期望收获

单独建立本论文集，目标是先形成一个可持续扩张的 `UPPAAL` 基础文库，而不是零散保存几篇经典论文。这里期望持续沉淀的内容主要包括四类：

1. `UPPAAL` 核心算法/数据结构相关工作。
2. `UPPAAL` 改进与扩展相关工作。
3. `UPPAAL` 工程实现、工具链、教程与建模实践相关工作。
4. 基于 `UPPAAL` 的代表性软件/系统应用工作。

对后续博士研究而言，这个论文集主要服务三类需求：

1. 理解 `UPPAAL` 及其底层 timed automata / zone / DBM 技术脉络。
2. 为后续验证方法、验证剖面和工具链构思提供可靠背景材料。
3. 为后续寻找可复用的 `UPPAAL` 应用案例、建模模式和工程经验打基础。

## 3. 收录范围

本论文集优先收录以下论文：

1. 由 `UPPAAL` 核心作者、官方团队或紧密相关学术脉络产出的关键工作。
2. 直接解释 `UPPAAL` 核心语义、DBM/zone/federation 等关键数据结构、验证算法或符号状态表示的论文。
3. 直接提出 `UPPAAL` 相关能力扩展、状态空间优化、抽象改进、扩展语义或新分析能力的论文。
4. 直接面向 `UPPAAL` 建模语言、查询语言、工具架构、用户教程、建模模式或工程实践的论文。
5. 使用 `UPPAAL` 对具体软件、协议、控制系统或工业系统进行建模、验证、调度或分析，且应用贡献不是一句带过的论文。

本论文集原则上不应作为重点收录以下论文：

1. 只和一般 timed automata 有关，但和 `UPPAAL` 谱系没有稳定联系的普通背景论文。
2. 只在参考文献中顺带提到 `UPPAAL`，但正文没有形成实质性 `UPPAAL` 技术或应用贡献的论文。
3. 纯安装教程、零散博客、重复镜像、课程作业或无正式贡献说明的材料。
4. 对 `UPPAAL` 只有极远的历史背景意义、但缺少明确可追溯关联且无法稳定支撑后续工作的条目。

## 4. 纳入与排除判定标准

后续筛选时，至少从以下维度判断：

1. 研究对象
   - 纳入：`UPPAAL` 本体、其关键理论基础、核心引擎技术、扩展分支，或基于 `UPPAAL` 的具体应用系统。
   - 排除：和 `UPPAAL` 仅弱相关的泛 timed automata、泛模型检查或泛形式化方法论文。
2. 任务类型
   - 纳入：能够支撑核心算法理解、工具能力演进理解或应用案例积累的论文。
   - 排除：只是宽泛背景介绍，无法沉淀为稳定文库条目的论文。
3. 证据形态
   - 纳入：正文中能明确看到 `UPPAAL` 相关技术、工具、案例或应用贡献。
   - 降优先级：只有部分章节与 `UPPAAL` 有关，但仍值得留作补充背景。
4. 可提取性
   - 纳入：可获得 PDF 原文，并能生成质量可用的 `paper_content.txt`。
   - 排除：无法获取合法可用 PDF，或提取后仍不足以支持可靠整理。
5. 与本研究相关性
   - 纳入：能直接服务博士研究中的状态机建模、形式化验证、验证工具或案例积累。
   - 降优先级：仅提供一般背景，不能直接沉淀出后续可用知识点。

## 5. 官方入口索引

以下链接已按 `2026-03-29` 核对，后续整理 `UPPAAL` 文库时应优先从这些官方入口反向追踪资料、源码、教程和案例。

官网与文档入口：

1. 官网主页：<https://uppaal.org/>
2. 功能总览：<https://uppaal.org/features/>
3. 文档入口：<https://uppaal.org/documentation>
4. 官方文档站：<https://docs.uppaal.org/>
5. 下载页：<https://uppaal.org/downloads/>
6. 案例页：<https://uppaal.org/casestudies/>
7. 团队页：<https://uppaal.org/team/>
8. 联系与支持页：<https://uppaal.org/contact/>
9. 版本变化页：<https://uppaal.org/changelog/>
10. `UPPAAL 5` 入口：<https://uppaal.org/uppaal5/>
11. 官方 pamphlet：<https://uppaal.org/texts/uppaal-pamphlet.pdf>
12. 官方 SMC tutorial：<https://uppaal.org/texts/uppaal-smc-tutorial.pdf>

官方支持与社区入口：

1. 官方 GitHub org：<https://github.com/UPPAALModelChecker>
2. 官方 GitHub Discussions：<https://github.com/orgs/UPPAALModelChecker/discussions>
3. 官方 Meta 仓库：<https://github.com/UPPAALModelChecker/UPPAAL-Meta>
4. Meta Issues：<https://github.com/UPPAALModelChecker/UPPAAL-Meta/issues>
5. Meta Discussions：<https://github.com/UPPAALModelChecker/UPPAAL-Meta/discussions>
6. 官方 Google Groups：<https://groups.google.com/forum/#!forum/uppaal>
7. 官方 Stack Overflow tag 入口：<https://stackoverflow.com/questions/tagged/uppaal>
8. 官方联系邮箱：`uppaal@cs.aau.dk`
9. 商业支持入口：<https://veriaal.dk/>

官方 GitHub org 当前公开仓库：

| 仓库 | 作用 |
|---|---|
| <https://github.com/UPPAALModelChecker/docs.uppaal.org> | 官方文档站源码 |
| <https://github.com/UPPAALModelChecker/libffi-build> | `libffi` 构建依赖 |
| <https://github.com/UPPAALModelChecker/python_dbm> | Python DBM 相关绑定/实验入口 |
| <https://github.com/UPPAALModelChecker/toolchains> | 官方构建工具链 |
| <https://github.com/UPPAALModelChecker/tracer> | 官方 trace interpreter |
| <https://github.com/UPPAALModelChecker/UCDD> | 官方 CDD 库 |
| <https://github.com/UPPAALModelChecker/UDBM> | 官方 DBM 库 |
| <https://github.com/UPPAALModelChecker/uls> | 官方 Language Server |
| <https://github.com/UPPAALModelChecker/uppaal-latex> | 官方 LaTeX package |
| <https://github.com/UPPAALModelChecker/uppaal-libs> | 官方动态库集合 |
| <https://github.com/UPPAALModelChecker/UPPAAL-Meta> | 官方 issue/roadmap/meta 入口 |
| <https://github.com/UPPAALModelChecker/utap> | 官方 timed automata parser |
| <https://github.com/UPPAALModelChecker/UUtils> | 官方 utility library |

## 6. 现有收录论文的作者关联主线

人物检索簇的起点不是官网 team 页面，而是当前文库 **11 个已收录顶层条目** 的 `bibtex.bib` 作者统计。官方 team / org 只用于交叉核验源码、案例和工具入口，不直接决定“核心人员”名单。

### 6.1 当前已形成稳定主线的作者

| 作者 | 当前收录篇数 | 当前关联条目 | 当前形成的联系 | 后续优先扩张方向 |
|---|---:|---|---|---|
| `Kim Guldstrand Larsen` | 6 | `bblp04`、`bdl04`、`dhlp06`、`llpy97`、`lpw95`、`lpy97` | 贯穿早期模型检查、紧凑 DBM、教程与优先级扩展，是当前文库最强主线 | `UPPAAL + zones/priced/strategy/statistical` |
| `Wang Yi` | 4 | `by04`、`llpy97`、`lpw95`、`lpy97` | 连接早期模型检查、紧凑数据结构与语义综述，是 timed automata 主干线的重要作者 | `UPPAAL + semantics/algorithms/symbolic state` |
| `Paul Pettersson` | 4 | `dhlp06`、`llpy97`、`lpw95`、`lpy97` | 同时覆盖早期引擎、DBM 存储优化与 priorities 扩展，适合继续追踪工具能力演化 | `UPPAAL + priority/federation/reduction` |
| `Gerd Behrmann` | 3 | `bblp04`、`bdl04`、`behrmann03` | 把 tutorial、zone abstraction 与 thesis 级数据结构总结连成了一条连续线 | `UPPAAL + CDD/abstraction/tool architecture` |
| `Alexandre David` | 2 | `bdl04`、`dhlp06` | 当前文库中连接 tutorial、priorities 与后续扩展分支的关键桥接作者 | `UPPAAL + priced/strategy/game` |
| `Johan Bengtsson` | 2 | `bengtsson02`、`by04` | 连接 DBM thesis 与语义综述，是理解 UDBM 内核与工具语义的核心入口之一 | `UPPAAL + DBM/federation/implementation` |

### 6.2 当前已出现但仍属补充线索的作者

| 作者 / 别名 | 当前关联条目 | 关系定位 | 检索使用方式 |
|---|---|---|---|
| `John Håkansson` / `John Haakansson` | `dhlp06` | `DBM subtraction + priorities` 的定向作者线索 | 与 `UPPAAL + priority/subtraction` 联用 |
| `Fredrik Larsson` | `llpy97` | 紧凑 DBM 与状态空间削减的共作者 | 与 `UPPAAL + compact DBM/mingraph` 联用 |
| `Patricia Bouyer` | `bblp04` | zone abstraction / extrapolation 分支共作者 | 与 `UPPAAL + abstraction/extrapolation` 联用 |
| `Radek Pelánek` / `Radek Pelanek` | `bblp04` | zone abstraction 分支共作者，检索时需兼顾重音与 ASCII 写法 | 与 `UPPAAL + zone abstraction` 联用 |
| `Rajeev Alur` | `ad90` | timed automata 理论前驱作者 | 只在明确追踪 `UPPAAL` 理论源头时纳入检索 |
| `David Dill` / `David L. Dill` | `ad90`、`dill89` | dense-time verification / clock constraints 的历史前驱作者 | 只在明确追踪 `UPPAAL` 技术前史时纳入检索 |

后续检索时，默认先从这条“文库内部作者主线”出发，再用官方 team 与 org 做补充，而不是反过来。新的 team 成员或官方贡献者，只有在已收录或待收录论文中形成稳定作者链后，才提升为“核心人员”。

默认检索写法是“作者名 + UPPAAL + 分支词”，例如：

1. `Kim G. Larsen + UPPAAL + zones`
2. `Paul Pettersson + UPPAAL + federation`
3. `Alexandre David + UPPAAL + priced`
4. `Johan Bengtsson + UPPAAL + DBM`
5. `Gerd Behrmann + UPPAAL + CDD`

### 6.3 作者年代与持续性观察

当前文库里的正式顶层条目，时间主要集中在 `1990-2006`。但这不代表 `UPPAAL` 在后续二十年里没有继续演化。按 `2026-03-29` 对官方站点、官方 GitHub org 与 DBLP 的核验结果，至少可以确认：

1. 官方 changelog 仍记录到 `2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5` 和 `2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
2. 官方 GitHub org 中 `UDBM`、`docs.uppaal.org`、`utap`、`uppaal-libs` 等仓库在 `2025-2026` 仍有更新。
3. `UPPAAL` 论文线在当前文库之外还能确认到 `2012` 的 `UPPAAL-SMC`、`2015` 的 `Uppaal Stratego`、`2018` 的 `20 Years of UPPAAL Enabled Industrial Model-Based Validation and Beyond`、`2022` 的 `Importance Splitting in Uppaal` 等后续工作。

因此，后续维护时不能只把现有作者当作“早期史料作者名单”，还要把他们分成“近年仍有明确延展”“2010s 仍有中期扩展”“当前核验主要停在早期主线”三类。

下表中的“继续沿该作者线扩张概率”是**检索价值推断**，表示继续追这个作者线能否大概率找到 `2007+ / 2010s / 2020s` 的后续 `UPPAAL` 工作，不是对作者个人职业状态的断言。

| 作者 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 相关年份 | 最近性判断 | 继续沿该作者线扩张概率 | 备注 |
|---|---|---|---|---|---|
| `Kim Guldstrand Larsen` | `1995-2006` | `2022` | 🟢 近年仍有直接延展 | 🟢 高 | 已核到 `2018` 的工业回顾和 `2022` 的 `Importance Splitting in Uppaal` |
| `Alexandre David` | `2004-2006` | `2015` | 🟨 2010s 仍有明显扩展 | 🟩 较高 | 已核到 `2012` 的 `UPPAAL-SMC`、`2015` 的 `Uppaal Stratego` |
| `Paul Pettersson` | `1995-2006` | `2013` | 🟨 2010s 仍有延展 | 🟨 中等 | 已核到 `2013` 的 `Verifying MARTE/CCSL Mode Behaviors Using UPPAAL` |
| `Gerd Behrmann` | `2003-2006` | `2007` | 🟧 中后期扩展后趋缓 | 🟨 中低 | 已核到 `2007` 的 `UPPAAL-Tiga`，当前未继续核到更晚的直接代表条目 |
| `Wang Yi` | `1995-2006` | `2006` | 🟧 当前核验主要停在早期主线 | 🟧 低 | 已核到 `2006` 的 `UPPAAL 4.0`，但本轮未继续核到更晚直接条目 |
| `Johan Bengtsson` | `2002-2004` | `2004` | 🟥 当前核验基本停在早期 | 🟥 低 | 当前直接主线主要仍落在 thesis 与早期综述阶段 |

这个判断对后续扩库的直接含义是：

1. 不能因为现有文库偏 `1990-2006`，就误判 `UPPAAL` 后续缺少新工作。
2. 下一轮应优先补 `2012-2023` 的 `SMC / Stratego / Tiga / 工业案例 / 现代工具链` 条目。
3. 作者关键词簇维护时，应同时记录“作者名 + 年代窗口”，而不是只留一串人名。

## 7. 本论文集下文件说明

本论文集默认包含以下核心文件：

1. [README.md](./README.md)
   - 入口说明文件。
   - 解释论文集定位、收录边界、官方入口、作者主线、状态口径和推荐阅读顺序。
2. [GUIDE.md](./GUIDE.md)
   - AI 工作操作规范。
   - 规定检索、筛选、目录维护、[SUMMARY.md](./SUMMARY.md) 回填、失败处理和一致性检查方式。
3. [SUMMARY.md](./SUMMARY.md)
   - 当前论文集的总账。
   - 记录统计、分类分布、双维材料状态、论文清单、更新日志和失败/阻塞记录。

AI 在开始具体工作前，推荐阅读顺序为：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. 若目标条目是 thesis/合集型父路径，先读该目录自己的 `README.md`
5. 目标论文目录下的 `bibtex.bib`
6. 目标论文目录下的 `paper_content.txt`
7. 需要深入具体拆分主题时，再进入对应 `paper-*` 子目录的 `README.md` 与 `paper_content.txt`
8. 必要时核对 `paper.pdf`

## 8. 单论文路径约束

本论文集下每个单论文目录默认至少应包含：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`

默认规则如下：

1. 若已有高质量 `content.md`，允许复制并规范命名为 `paper_content.txt`。
2. 若没有现成正文提取物，则必须优先使用 `tools/pdf_extractor.py` 基于 `paper.pdf` 生成 `paper_content.txt`。
3. 若原始条目本身带有稳定的 `paper-*` 子论文拆分路径，应一并搬入，并为父目录补 `README.md` 说明父子关系和推荐阅读顺序。
4. 这类 `paper-*` 子目录当前默认视为父条目的辅助阅读单元，不单独计入 [SUMMARY.md](./SUMMARY.md) 的顶层论文数；若后续要把某个子论文提升为独立正式条目，再为其单独补 `bibtex.bib` 并单独入账。
5. 当前基础文库阶段不强制要求每篇都立即补齐 `desc.md`；但后续若开始单篇深度整理，应在遵守本论文集规范的前提下再补写派生文件。

## 9. 材料状态口径

本论文集中的“材料状态”不再表示“文件齐不齐”，而是改为两个维度：

1. **内容详细程度**
2. **实现可获取程度**

### 9.1 内容详细程度

| Emoji | 级别 | 含义 |
|---|---|---|
| 🟢 | 复现级 | 核心数据结构、算法流程、关键规则或实验设置足够细，原则上可据论文复现主要方法 |
| 🟩 | 较完整 | 主线、关键结构和主要步骤明确，但仍需结合工具经验或其他材料补少量细节 |
| 🟨 | 中等 | 方法轮廓和主要机制清楚，但缺少若干关键公式、伪代码、参数或工程信息 |
| 🟧 | 概览级 | 主要停留在工具介绍、总体思路或经验总结层，难以直接据此复现 |
| 🟥 | 细节不足 | 信息过少、正文不完整或缺少关键部分，短期内无法据此稳定复现 |

### 9.2 实现可获取程度

这里的“实现”默认**严格指源码级实现**。单纯的官方二进制、安装包、可执行文件、在线服务、文档站、教程页或案例模型，不应被视为“实现源码可获取”，最多只能记为“仅可执行/可使用版本可得”。

| Emoji | 级别 | 含义 |
|---|---|---|
| 🟢 | 论文对应实现源码直达 | 能拿到与论文主题直接对应的核心源码库或实现仓库，且不是只有二进制 |
| 🟩 | 核心实现源码线直达 | 能拿到同一技术线的核心源码，但不保证是论文同期精确快照 |
| 🟨 | 部分实现源码可得 | 只能拿到部分源码、子库、解析器、辅助组件或相关实现片段，主实现仍不完整 |
| 🟧 | 仅可执行/可使用版本可得 | 只能拿到二进制、安装包、可运行工具、文档或示例，源码本体未公开 |
| 🟥 | 暂未获取实现源码 | 当前没有找到可用源码线索 |

## 10. AI 工作入口提示

进入本论文集时，默认应按以下方式工作：

1. 先读 [README.md](./README.md)，理解 `UPPAAL` 文库的边界、官方入口、作者主线和状态口径。
2. 再读 [GUIDE.md](./GUIDE.md)，确认本轮工作流程、检索规则和回填规范。
3. 再看 [SUMMARY.md](./SUMMARY.md)，掌握当前已有积累、作者分布、分类缺口和失败历史。
4. 如果目标目录是带内嵌子论文的父路径，先读该目录自己的 `README.md`，确认 thesis 与 `paper-*` 子目录的关系。
5. 然后再按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时）` 的顺序工作。
6. 只有在需要深入某个拆分主题时，才进入对应 `paper-*` 子目录继续读其 `README.md` 与 `paper_content.txt`。
7. 完成单篇目录后，必须回写 [SUMMARY.md](./SUMMARY.md)，不能只增加文件而不入账。

## 11. 后续 AI 应优先做什么、避免做什么

优先做的事：

1. 扩充 `🧪 应用与案例` 类条目，补足当前偏基础技术、偏引擎内部的结构失衡。
2. 围绕现有文库里的高频作者主线继续补齐重要扩展工作，如 priced、strategy、statistical 或 game-based 分支。
3. 在新增条目时同步评定双维材料状态，而不是只写“有无 PDF”。
4. 在检索时同时维护“技术关键词簇”和“作者关键词簇”。
5. 重点补齐 `2007+ / 2010s / 2020s` 的 `UPPAAL` 后续工作，避免文库长期停留在早期奠基阶段。

应避免的事：

1. 把本论文集写成“所有 timed automata 论文”的大杂烩。
2. 只因某篇论文和 DBM 或 timed automata 有一点关系，就直接归入 `UPPAAL` 文库。
3. 只复制 PDF，不补 `paper_content.txt` 和 `bibtex.bib`。
4. 在文档中写入外部本地绝对路径或把外部文件路径直接当成仓库引用。
