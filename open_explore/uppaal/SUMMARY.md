# UPPAAL 文库总账

本文件是 `open_explore/uppaal/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 谱系论文、分类分布、双维材料状态、更新状态和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集的定位、官方入口、作者主线和状态口径。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、回填和一致性检查规范。
3. 再使用本文件查看当前统计、状态分布、统一论文表和失败记录。
4. 若后续开始补单篇深度分析，再进入具体论文目录处理 `bibtex.bib`、`paper_content.txt` 与 `paper.pdf`。

## 收录边界回顾

为避免后续维护时误把 `uppaal/` 写成泛 timed automata 收藏夹，这里重申当前论文集的边界：

1. 优先收录 `UPPAAL` 本体、核心理论基础、关键算法/数据结构、扩展能力和代表性应用工作。
2. 历史前驱理论可以收录，但必须能清楚说明它与 `UPPAAL` / UDBM 技术脉络的直接关系。
3. 只在参考文献里提到 `UPPAAL`、正文没有实质贡献的论文，不应正式入账。

## 官方入口速查

以下入口已按 `2026-03-29` 核对，后续扩库、查源码、查模型、查支持渠道时应优先从这里反推。

官网与文档：

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

官方支持与 GitHub：

1. GitHub org：<https://github.com/UPPAALModelChecker>
2. Org Discussions：<https://github.com/orgs/UPPAALModelChecker/discussions>
3. Meta 仓库：<https://github.com/UPPAALModelChecker/UPPAAL-Meta>
4. Meta Issues：<https://github.com/UPPAALModelChecker/UPPAAL-Meta/issues>
5. Meta Discussions：<https://github.com/UPPAALModelChecker/UPPAAL-Meta/discussions>
6. Google Groups：<https://groups.google.com/forum/#!forum/uppaal>
7. Stack Overflow tag：<https://stackoverflow.com/questions/tagged/uppaal>
8. 商业支持：<https://veriaal.dk/>
9. 联系邮箱：`uppaal@cs.aau.dk`

官方 org 当前公开仓库：

1. <https://github.com/UPPAALModelChecker/docs.uppaal.org>
2. <https://github.com/UPPAALModelChecker/libffi-build>
3. <https://github.com/UPPAALModelChecker/python_dbm>
4. <https://github.com/UPPAALModelChecker/toolchains>
5. <https://github.com/UPPAALModelChecker/tracer>
6. <https://github.com/UPPAALModelChecker/UCDD>
7. <https://github.com/UPPAALModelChecker/UDBM>
8. <https://github.com/UPPAALModelChecker/uls>
9. <https://github.com/UPPAALModelChecker/uppaal-latex>
10. <https://github.com/UPPAALModelChecker/uppaal-libs>
11. <https://github.com/UPPAALModelChecker/UPPAAL-Meta>
12. <https://github.com/UPPAALModelChecker/utap>
13. <https://github.com/UPPAALModelChecker/UUtils>

## 贡献类型 Emoji 口径

| Emoji | 类型 | 说明 |
|---|---|---|
| 🧱 | 核心算法/数据结构 | timed automata 语义、DBM、zone、symbolic state、核心验证算法 |
| ⚡ | 改进与扩展 | 抽象优化、状态空间削减、优先级、priced/strategy/statistical 等扩展 |
| 🛠️ | 工程/工具链 | 工具架构、建模语言、查询语言、教程、建模模式、用户指南 |
| 🧪 | 应用与案例 | 基于 `UPPAAL` 的具体系统、协议、软件或工业验证案例 |

## 双维材料状态口径

### 内容详细程度

| Emoji | 级别 | 含义 |
|---|---|---|
| 🟢 | 复现级 | 核心数据结构、算法流程、关键规则或实验设置足够细，原则上可据论文复现主要方法 |
| 🟩 | 较完整 | 主线、关键结构和主要步骤明确，但仍需结合工具经验或其他材料补少量细节 |
| 🟨 | 中等 | 方法轮廓和主要机制清楚，但缺少若干关键公式、伪代码、参数或工程信息 |
| 🟧 | 概览级 | 主要停留在工具介绍、总体思路或经验总结层，难以直接据此复现 |
| 🟥 | 细节不足 | 信息过少、正文不完整或缺少关键部分，短期内无法据此稳定复现 |

### 实现可获取程度

这里的“实现”默认严格指源码级实现。单纯可下载的安装包、二进制、文档站、在线服务和案例模型，不等于实现源码可获取。

| Emoji | 级别 | 含义 |
|---|---|---|
| 🟢 | 论文对应实现源码直达 | 能拿到与论文主题直接对应的核心源码库或实现仓库，且不是只有二进制 |
| 🟩 | 核心实现源码线直达 | 能拿到同一技术线的核心源码，但不保证是论文同期精确快照 |
| 🟨 | 部分实现源码可得 | 只能拿到部分源码、子库、解析器、辅助组件或相关实现片段，主实现仍不完整 |
| 🟧 | 仅可执行/可使用版本可得 | 只能拿到二进制、安装包、可运行工具、文档或示例，源码本体未公开 |
| 🟥 | 暂未获取实现源码 | 当前没有找到可用源码线索 |

## 检索关键词簇

### 当前推荐关键词簇

- 技术主线：`UPPAAL + timed automata + DBM/zone/federation/symbolic state`
- 扩展主线：`UPPAAL + priced/cost-optimal/timed games/Tiga/statistical model checking/SMC/Stratego/expected cost/controller synthesis`
- 工程主线：`UPPAAL + architecture/implementation/UPPAAL 4.0/tool architecture/implementation secrets`
- 作者主线：`Kim Guldstrand Larsen`、`Alexandre David`、`Gerd Behrmann`、`Wang Yi`、`Paul Pettersson`
- 分支作者：`Axel Legay`、`Didier Lime`、`Marius Mikučionis`、`Peter Gjøl Jensen`、`Danny Bøgsted Poulsen`
- 应用主线：当前仍保留，但本轮继续后置

### 已观察到的高命中特征

- 标题直接出现 `UPPAAL`、`Tiga`、`SMC`、`Stratego`、`timed games`、`priced timed automata`、`expected cost`
- `作者名 + 分支词` 的检索效果显著提升，例如 `Alexandre David + UPPAAL + Stratego`、`Kim Guldstrand Larsen + UPPAAL + statistical model checking`
- `SMC / Tiga / Stratego` 相关条目里，作者个人主页直链 PDF 的命中率明显高于只搜 DOI
- 工具演进类材料常以 `architecture`、`implementation`、`4.0`、`developing over` 这类标题信号出现

### 已观察到的低命中特征

- 只写 `timed games` 或 `statistical model checking`，但正文没有 `UPPAAL` 明确关联
- 只在 related work 里顺带提一次 `UPPAAL` 的概率验证或博弈验证论文
- 只用工具名或只用作者名单独搜索，都容易造成噪声膨胀
- 只有教程页、案例页、安装说明而没有正式论文正文的条目，不适合直接正式入账

### 检索倾向调整

- 当前文库已经覆盖 `1990-2015` 的核心技术演进，下一轮应优先补 `2016-2022` 的后续扩展
- `⚡` 改进与扩展已成当前主干，后续应继续沿 `SMC / Stratego / controller synthesis / importance splitting` 扩张
- `🧪 应用与案例` 仍然为空，但按当前用户要求继续后置，不抢本轮优先级
- 每次更新前先删减失效关键词，保持本节简洁

## 年代分布与近年活动观察

- 当前已收录顶层条目已经覆盖 `1990-2015`，不再只停留在 `1990-2006` 的早期奠基阶段。
- 这一轮新补的 12 篇条目，基本补齐了 `2001-2015` 的核心扩展链：`cost-optimality -> architecture/implementation -> timed games/Tiga -> SMC -> Stratego`。
- 官方 changelog 仍显示后续版本持续发布：`2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5`、`2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
- 官方 GitHub org 也显示近期仍有源码活动：`UDBM` 更新到 `2025-07-03`，`utap` 更新到 `2025-10-24`，`uppaal-libs` 更新到 `2026-03-16`。
- 当前文库之外，仍已核到至少 `2018` 的 `20 Years of UPPAAL Enabled Industrial Model-Based Validation and Beyond` 和 `2022` 的 `Importance Splitting in Uppaal`，说明 `2016-2022` 仍有明显技术缺口待补。

## 现有收录论文作者关联

以下作者关系只基于当前 **23 个顶层条目** 的 `bibtex.bib` 统计；`paper-*` 子目录当前不单独重复计数。后续扩库时，应先沿这张作者关系表追踪，再去官方入口核验源码、案例和工具实现。

这里的“继续沿该作者线扩张判断”是**检索价值推断**，表示继续顺着该作者找 `UPPAAL` 后续工作时的预期收益，不是对作者个人职业状态的断言。

### 核心作者主线

| 作者 | 频次 | 角色判断 | 主要贡献方向 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 年份 | 最近性判断 | 继续沿该作者线扩张判断 | 代表关联条目 |
|---|---:|---|---|---|---|---|---|---|
| `Kim Guldstrand Larsen` | 16 | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / tutorial / Tiga / SMC / Stratego` | `1995-2015` | `2022` | 🟢 近年仍有直接延展 | 🟢 高 | `lpw95`、`llpy97`、`bdl04`、`behrmann07`、`david11-smc`、`david15` |
| `Alexandre David` | 12 | 中后期扩展主线整合者 | `architecture / Tiga / SMC / expected cost / Stratego` | `2002-2015` | `2015` | 🟩 当前文库已覆盖到 2010s 后段 | 🟢 高 | `behrmann02`、`behrmann07`、`david11-*`、`david14`、`david15` |
| `Gerd Behrmann` | 8 | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / UPPAAL 4.0 / evolution survey` | `2002-2011` | `2011` | 🟨 中期主线已较完整 | 🟨 中等 | `behrmann02`、`behrmann03`、`behrmann06`、`behrmann07`、`behrmann11` |
| `Wang Yi` | 8 | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations` | `1995-2011` | `2011` | 🟨 早期到中期主线较完整 | 🟨 中等 | `lpw95`、`llpy97`、`by04`、`behrmann02`、`behrmann06`、`behrmann11` |
| `Paul Pettersson` | 7 | `DBM / engine / priority` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities` | `1995-2011` | `2013` | 🟨 2010s 仍有延展 | 🟨 中等 | `lpw95`、`llpy97`、`behrmann02-secrets`、`behrmann06`、`dhlp06`、`behrmann11` |
| `Axel Legay` | 4 | `SMC / optimization` 分支关键协作者 | `statistical model checking / priced models / expected-cost optimization` | `2011-2014` | `2014` | 🟨 2010s 分支作者 | 🟩 较高 | `david11-statistical`、`david11-smc`、`bulychev12`、`david14` |
| `Johan Bengtsson` | 3 | `DBM` 数据结构专题化奠基作者 | `clocks / DBMs / states / DBM internals / implementation detail` | `2002-2004` | `2004` | 🟥 当前核验基本停在早期 | 🟥 低 | `bengtsson02`、`behrmann02-secrets`、`by04` |

### 分支协作者与历史前驱

| 作者 / 别名 | 当前关联条目 | 角色判断 | 主要贡献方向 | 年代观察 | 检索建议 |
|---|---|---|---|---|---|
| `Didier Lime` | `cassez05`、`behrmann07`、`david14` | `timed games -> Tiga -> optimization` 分支协作者 | `timed games / controller synthesis / cost analysis` | 当前文库已直接覆盖到 `2014` | 与 `UPPAAL + timed games/Tiga/cost` 联用 |
| `Marius Mikučionis` / `Marius Mikucionis` | `david11-smc`、`david11-statistical`、`david15` | `SMC / Stratego` 中后期扩展作者 | `statistical model checking / stochastic analysis / strategy synthesis` | 当前文库已直接覆盖 `2011-2015` | 与 `UPPAAL + SMC/Stratego/statistical` 联用 |
| `Peter Gjøl Jensen` / `Peter G. Jensen` | `david14`、`david15` | `optimization / Stratego` 关键协作者 | `expected cost / optimization / strategy synthesis` | 当前文库已直接覆盖 `2014-2015` | 与 `UPPAAL + Stratego/expected cost` 联用 |
| `Danny Bøgsted Poulsen` / `Danny Bogsted Poulsen` | `bulychev12`、`david11-smc` | `distributed SMC` 协作者 | `distributed statistical model checking` | 当前文库已直接覆盖 `2011-2012` | 与 `UPPAAL + distributed statistical model checking` 联用 |
| `Zheng Wang` | `david11-statistical`、`david11-smc` | `SMC / priced timed automata` 协作者 | `NPTA / priced SMC` | 当前文库已直接覆盖 `2011` | 与 `UPPAAL + SMC/priced timed automata` 联用 |
| `John Håkansson` / `John Haakansson` | `behrmann06`、`dhlp06` | `priorities / DBM subtraction` 定向贡献者 | `priority timed automata / DBM subtraction` | 当前文库主要落在 `2006` | 与 `UPPAAL + priority/subtraction` 联用 |
| `Patricia Bouyer` | `bblp04` | zone abstraction 外推分支外部关键合作者 | `lower-upper bound extrapolation / zone abstraction` | 当前文库主要落在 `2004` | 与 `UPPAAL + abstraction/extrapolation` 联用 |
| `Radek Pelánek` / `Radek Pelanek` | `bblp04` | zone abstraction 外推分支外部关键合作者 | `zone abstraction / extrapolation` | 当前文库主要落在 `2004` | 与 `UPPAAL + zone abstraction` 联用 |
| `Rajeev Alur` | `ad90` | 理论前史奠基者 | `timed automata semantics` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 理论源头时纳入 |
| `David Dill` / `David L. Dill` | `ad90`、`dill89` | dense-time verification 前史奠基者 | `timing assumptions / clock constraints / symbolic verification` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 技术前史时纳入 |

## 当前收录统计

- 已收录顶层条目：**23** 篇
- 本轮新增顶层条目：**12** 篇
- 含内嵌 `paper-*` 子目录的 thesis/合集条目：**2** 篇
- 内容详细程度：
  - `🟢 复现级`：**2** 篇
  - `🟩 较完整`：**13** 篇
  - `🟨 中等`：**3** 篇
  - `🟧 概览级`：**5** 篇
  - `🟥 细节不足`：**0** 篇
- 实现可获取程度：
  - `🟢 论文对应实现源码直达`：**1** 篇
  - `🟩 核心实现源码线直达`：**1** 篇
  - `🟨 部分实现源码可得`：**9** 篇
  - `🟧 仅可执行/可使用版本可得`：**9** 篇
  - `🟥 暂未获取实现源码`：**3** 篇
- 本轮未纳入/待补证条目：**1** 条

说明：`behrmann03` 与 `bengtsson02` 下的 `paper-*` 子目录当前作为父条目的辅助阅读单元存在，不单独计入以上顶层统计。

## 分类分布

| 分类 | 篇数 | 占比 | 说明 |
|---|---:|---:|---|
| 🧱 核心算法/数据结构 | 6 | 26.1% | 以 timed automata、DBM、zone、symbolic verification 主线为主 |
| ⚡ 改进与扩展 | 11 | 47.8% | 已覆盖 priced/cost-optimal、timed games、Tiga、SMC、Stratego 等主线 |
| 🛠️ 工程/工具链 | 6 | 26.1% | 已覆盖 architecture、implementation、tutorial、`UPPAAL 4.0` 与 evolution survey |
| 🧪 应用与案例 | 0 | 0.0% | 当前仍为空，按本轮目标继续后置 |
| **合计** | **23** | **100.0%** | - |

## 论文清单

### 🧱 / ⚡ / 🛠️ 统一总表（按年份升序）

| 类型 | Key | 标题 | 年份 | 内容一句话简介 | 内容详细程度 | 实现可获取程度 | 源码线索 | 目录 |
|---|---|---|---:|---|---|---|---|---|
| 🧱 | `ad90` | Automata for Modeling Real-Time Systems | 1990 | timed automata 语义源头，定义了后来 `UPPAAL` 持续依赖的 clocks / guards / resets 基本模型 | 🟩 较完整 | 🟥 暂未获取实现源码 | 作为理论源头保留；当前无直接源码线索 | [ad90-timed-automata](./ad90-timed-automata/) |
| 🧱 | `dill89` | Timing Assumptions and Verification of Finite-State Concurrent Systems | 1990 | dense-time symbolic verification 的历史前驱，为后续 clock-constraint 表示提供早期语义线索 | 🟨 中等 | 🟥 暂未获取实现源码 | 作为历史前驱保留；当前无直接源码线索 | [dill89-timing-assumptions](./dill89-timing-assumptions/) |
| 🧱 | `lpw95` | Model-Checking for Real-Time Systems | 1995 | 早期 `UPPAAL` symbolic model checking 的奠基论文，解释为何约束求解和状态空间搜索成为引擎核心 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方有可下载工具线，但当前未见对应模型检查核心源码公开 | [lpw95-real-time-model-checking](./lpw95-real-time-model-checking/) |
| 🧱 | `llpy97` | Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction | 1997 | 聚焦紧凑 DBM 存储与状态空间削减，是 UDBM `mingraph` 一线的重要理论来源 | 🟢 复现级 | 🟩 核心实现源码线直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供同一技术线的核心 DBM 源码 | [llpy97-compact-data-structure](./llpy97-compact-data-structure/) |
| 🛠️ | `lpy97` | UPPAAL in a Nutshell | 1997 | 早期 `UPPAAL` toolbox 总览，覆盖描述语言、模拟器、模型检查器和用户工作流 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方有文档与工具可用版本，但当前未见对应早期 toolbox 完整源码公开 | [lpy97-uppaal-nutshell](./lpy97-uppaal-nutshell/) |
| ⚡ | `behrmann01` | Efficient Guiding Towards Cost-Optimality in UPPAAL | 2001 | 把代价最优可达性正式引入 `UPPAAL` 技术线，是 priced / cost-optimal 分支的早期关键节点 | 🟩 较完整 | 🟥 暂未获取实现源码 | 论文可得；当前未见与该分支直接对应的公开源码线 | [behrmann01-cost-optimality-uppaal](./behrmann01-cost-optimality-uppaal/) |
| 🛠️ | `bdly02` | New UPPAAL Architecture | 2002 | 介绍新一代 `UPPAAL` 模型检查引擎架构，是后续组件化与工具演进的重要工程节点 | 🟨 中等 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 等组件源码可得 | [behrmann02-new-uppaal-architecture](./behrmann02-new-uppaal-architecture/) |
| 🧱 | `bengtsson02` | Clocks, DBMs and States in Timed Systems | 2002 | thesis 级系统总结 DBM 操作、normalization、存储与实现，是理解 UDBM 内核的关键入口；含 `paper-a` 到 `paper-e` 子目录导航 | 🟢 复现级 | 🟢 论文对应实现源码直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[python_dbm](https://github.com/UPPAALModelChecker/python_dbm) 直接对应 DBM 实现主题 | [bengtsson02-clocks-dbms-states](./bengtsson02-clocks-dbms-states/) |
| 🛠️ | `bbdlpy02` | UPPAAL Implementation Secrets | 2003 | 系统解释引擎内部实现选择与性能技巧，是理解 `UPPAAL` 工程细节的关键条目 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer) 等组件源码可得 | [behrmann02-uppaal-implementation-secrets](./behrmann02-uppaal-implementation-secrets/) |
| ⚡ | `behrmann03` | Data Structures and Algorithms for the Analysis of Real Time Systems | 2003 | 从更高层综合说明 unions of zones、CDD、priced 方向与 `UPPAAL` 周边数据结构演进；含 `paper-intro` 与 `paper-a` 到 `paper-f` 子目录导航 | 🟩 较完整 | 🟨 部分实现源码可得 | [UCDD](https://github.com/UPPAALModelChecker/UCDD)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 可得，但 thesis 覆盖整条能力线不全有源码 | [behrmann03-real-time-data-structures](./behrmann03-real-time-data-structures/) |
| ⚡ | `bblp04` | Lower and Upper Bounds in Zone Based Abstractions of Timed Automata | 2004 | 讨论 zone abstraction 的上下界外推，是 `extrapolation` 能力链上的关键条目 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 能提供底层 DBM 源码，但该条目的完整外推实现未直出 | [bblp04-zone-based-abstractions](./bblp04-zone-based-abstractions/) |
| 🛠️ | `bdl04` | A Tutorial on Uppaal | 2004 | 面向建模语言、查询语言、工具界面和模式的系统教程，是工程使用入口文献 | 🟩 较完整 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer)、[uls](https://github.com/UPPAALModelChecker/uls)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 等组件源码可得，但完整工具未全部开源 | [bdl04-uppaal-tutorial](./bdl04-uppaal-tutorial/) |
| 🧱 | `by04` | Timed Automata: Semantics, Algorithms and Tools | 2004 | 汇总 timed automata 的语义、算法与工具视角，为 `UPPAAL` 技术线提供紧凑总览 | 🟨 中等 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uls](https://github.com/UPPAALModelChecker/uls) 等组件源码可得，但完整工具主实现未公开 | [by04-semantics-algorithms-tools](./by04-semantics-algorithms-tools/) |
| ⚡ | `cdfll05` | Efficient On-the-fly Algorithms for the Analysis of Timed Games | 2005 | 给出 timed games 分析的高效 on-the-fly 算法，是后续 `UPPAAL-Tiga` 的关键理论前置 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前未见 timed-games 核心源码公开；可沿 `Tiga` 工具线与官方文档反查 | [cassez05-analysis-of-timed-games](./cassez05-analysis-of-timed-games/) |
| 🛠️ | `behrmann06` | UPPAAL 4.0 | 2006 | `UPPAAL 4.0` 官方工具快照，标记语言、引擎与工具工作流进入新的整合阶段 | 🟧 概览级 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 提供部分源码线索 | [behrmann06-uppaal-4](./behrmann06-uppaal-4/) |
| ⚡ | `dhlp06` | Model Checking Timed Automata with Priorities Using DBM Subtraction | 2006 | 以 DBM subtraction 支撑优先级 timed automata 分析，直接连接 federation 与差集操作需求 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供底层 DBM 技术线源码，但 priorities 主实现未直接公开 | [dhlp06-dbm-subtraction](./dhlp06-dbm-subtraction/) |
| ⚡ | `bcdfll07` | UPPAAL-Tiga: Time for Playing Games! | 2007 | 把 timed games/controller synthesis 能力工具化为 `UPPAAL-Tiga`，标志博弈分支正式成形 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 当前未见 `Tiga` 核心源码公开；可沿官方 `Tiga` 历史工具线与文档反查 | [behrmann07-uppaal-tiga](./behrmann07-uppaal-tiga/) |
| 🛠️ | `bdlpy11` | Developing UPPAAL over 15 years | 2011 | 从工程与历史角度回顾 `UPPAAL` 15 年演进，是理解技术分支分化与工具成熟度的综述入口 | 🟧 概览级 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 与官方文档站可作为对应工程线索 | [behrmann11-developing-uppaal-over-15-years](./behrmann11-developing-uppaal-over-15-years/) |
| ⚡ | `dllmpvw11` | Statistical Model Checking for Networks of Priced Timed Automata | 2011 | 将 `SMC` 扩展到 NPTA / priced 模型，形成概率与代价分析结合的关键一步 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 SMC 文档、教程与工具线可用，但对应扩展核心源码未见公开 | [david11-smc-priced-timed-automata](./david11-smc-priced-timed-automata/) |
| ⚡ | `dllmw11` | Time for Statistical Model Checking of Real-time Systems | 2011 | 把 statistical model checking 正式引入 real-time 系统分析，是 `UPPAAL-SMC` 分支的奠基条目 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 SMC 文档、教程与工具线可用，但核心源码未见公开 | [david11-statistical-model-checking-real-time](./david11-statistical-model-checking-real-time/) |
| ⚡ | `bdllmp12` | Checking & Distributing Statistical Model Checking | 2012 | 通过分布式框架扩展 statistical model checking 的实验规模与算力利用能力 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前可沿官方 SMC 工具线追运行版本，但分布式扩展源码未见公开 | [bulychev12-distributed-statistical-model-checking](./bulychev12-distributed-statistical-model-checking/) |
| ⚡ | `djlllst14` | On Time with Minimal Expected Cost! | 2014 | 将 expected cost 目标纳入 `SMC / optimization` 线，为后续 `Stratego` 优化提供直接技术延展 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 可沿 `SMC / Stratego` 工具线追可运行版本，但核心优化源码未见公开 | [david14-minimal-expected-cost](./david14-minimal-expected-cost/) |
| ⚡ | `djlmt15` | Uppaal Stratego | 2015 | 把策略生成、优化、比较与性能分析工具化为 `Uppaal Stratego`，标志策略优化分支正式成形 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方文档与工具线可追，但 `Stratego` 核心源码未见公开 | [david15-uppaal-stratego](./david15-uppaal-stratego/) |

### 🧪 应用与案例

当前尚无正式入账条目。按本轮目标，应用类仍继续后置；下一轮若核心技术脉络进一步补齐后，再单独扩充。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal/`，新增 **11** 篇基础条目，并建立 `README.md`、`GUIDE.md`、`SUMMARY.md` 三个论文集核心文件；随后补入 `behrmann03` 与 `bengtsson02` 的 `paper-*` 子目录及父子导航 README | 只从既有 `UPPAAL/UDBM` 历史论文池挑选一份可用副本，优先完成基础入库，不额外扩新论文；有现成 `content.md` 的直接规范为 `paper_content.txt`，缺失 thesis 级正文的条目用 `tools/pdf_extractor.py` 补齐；对 thesis 型条目把原有拆分子论文与 `content_assets/` 一并带入 | 先搭建 `UPPAAL` 基础文库骨架，再补齐带内嵌子论文条目的父子导航结构，为后续沿专题继续深挖做准备 |
| 2026-03-29 | 重构 `README.md`、`GUIDE.md`、`SUMMARY.md` 的文库口径，新增官方入口索引、作者主线与双维材料状态体系 | 不再以“文件齐不齐”作为主状态，而是改成“内容详细程度 + 实现可获取程度”；同时把 `🧱 / ⚡ / 🛠️` 合并进统一论文表 | 为后续沿官方 org、官方 docs、核心作者和技术分支系统扩库做准备 |
| 2026-03-29 | 补充作者年代观察与近年活动判断，并把“实现可获取程度”重定义为严格的源码标准 | 把“当前文库作者”与“较新年份的直接 `UPPAAL` 工作”显式关联，同时把二进制下载与源码实现彻底分开 | 为后续优先补 `2010s/2020s` 的 `SMC / Stratego / Tiga / 工业案例 / 现代工具链` 缺口做准备 |
| 2026-03-29 | 新增 **12** 篇 `2001-2015` 的核心技术/扩展条目，补齐 `cost-optimality / architecture / Tiga / SMC / Stratego` 主链 | 只收录 PDF 实际下载成功且已生成 `paper_content.txt` 的条目；本轮继续后置应用类，优先围绕核心作者和技术分支做全网补链 | 把文库直接覆盖范围从 `1990-2006` 扩展到 `1990-2015`，让 `UPPAAL` 演进脉络初步成形 |
| 2026-03-29 | 调整作者画像与论文清单维护口径，补充“角色判断 / 主要贡献方向”，并把统一论文表改为按年份升序维护 | 作者分析继续以现有已收录论文为主证据，不以 team 页替代；统一论文表按年份升序、同年按 `Key` 稳定排序 | 让后续扩库同时具备“技术时间线”和“人物贡献线”两条可直接复用的导航 |

## 失败与阻塞记录

| Key | 标题 | 状态 | 原因 | 后续建议 |
|---|---|---|---|---|
| `rokicki93` | Representing and Modeling Digital Circuits | 本轮未纳入 | 当前未取得合法可用全文 PDF，且与 `UPPAAL` 论文集的直接关系更偏 DBM 历史引用背景，暂不作为正式条目入库 | 若后续找到合法全文且能明确其在 `UPPAAL/DBM` 技术链中的稳定价值，再单独复核是否纳入 |
