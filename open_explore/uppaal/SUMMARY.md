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
- 扩展主线：`UPPAAL + abstraction/extrapolation/priced/statistical/strategy/game/priority/reduction`
- 工程主线：`UPPAAL + tutorial/user guide/modeling patterns/query language/verifyta/toolbox`
- 应用主线：`UPPAAL + case study/industrial/application + 具体系统名`
- 作者主线：`Kim Guldstrand Larsen`、`Wang Yi`、`Gerd Behrmann`、`Paul Pettersson`、`Alexandre David`、`Johan Bengtsson`
- 次级作者：`John Håkansson`、`Fredrik Larsson`、`Patricia Bouyer`、`Radek Pelánek`、`Rajeev Alur`、`David Dill`

### 已观察到的高命中特征

- 标题直接出现 `UPPAAL`、`DBM`、`zone`、`difference bound matrix`、`tutorial`、`toolbox`
- 核心作者名与 `UPPAAL` 技术词联用时，命中率明显高于只搜技术词
- `Alexandre David + Uppaal + priced`、`Johan Bengtsson + Uppaal + DBM`、`Gerd Behrmann + Uppaal + CDD` 这类“作者 + 分支词”组合对追踪演进脉络特别有效
- thesis/教程类条目往往能同时补足技术脉络与工程语境

### 已观察到的低命中特征

- 只写 timed automata 或 real-time verification，但正文没有 `UPPAAL` 明确关联
- 只在 related work 里顺带提一次 `UPPAAL` 的应用论文
- 只用工具名或只用作者名单独搜索，都容易造成噪声膨胀
- 历史背景论文如果没有被 `UPPAAL` 技术线稳定引用，应谨慎纳入

### 检索倾向调整

- 下一轮应优先补 `🧪 应用与案例`，避免长期只收引擎和理论条目
- `⚡` 改进与扩展值得继续沿 `priced`、`strategy`、`statistical`、`game` 等分支扩张
- 后续检索必须同步维护技术词簇和作者词簇，不再只靠题目关键词
- 每次更新前先删减失效关键词，保持本节简洁

## 年代分布与近年活动观察

- 当前已收录顶层条目全部集中在 `1990-2006`，这只能代表 `UPPAAL` 的早期奠基期与第一轮扩展期。
- 官方 changelog 已明确记录后续仍在持续发布：`2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5`、`2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
- 官方 GitHub org 也显示近期仍有源码活动：`UDBM` 更新到 `2025-07-03`，`utap` 更新到 `2025-10-24`，`uppaal-libs` 更新到 `2026-03-16`。
- 当前文库之外，已核到的后续代表条目至少包括：`2012` 的 `UPPAAL-SMC`、`2015` 的 `Uppaal Stratego`、`2018` 的 `20 Years of UPPAAL Enabled Industrial Model-Based Validation and Beyond`、`2022` 的 `Importance Splitting in Uppaal`。
- 因此，下一轮扩张不能只沿 `1990-2006` 继续补老论文，而应优先补齐 `SMC / Stratego / Tiga / 工业验证 / 现代工具链` 的年代缺口。

## 现有收录论文作者关联

以下作者关系只基于当前 **11 个顶层条目** 的 `bibtex.bib` 统计；`paper-*` 子目录当前不单独重复计数。后续扩库时，应先沿这张作者关系表追踪，再去官方入口核验源码、案例和工具实现。

这里的“继续沿该作者线扩张判断”是**检索价值推断**，表示继续顺着该作者找 `UPPAAL` 后续工作时的预期收益，不是对作者个人职业状态的断言。

### 核心作者主线

| 作者 | 频次 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 年份 | 最近性判断 | 继续沿该作者线扩张判断 | 当前关联条目 |
|---|---:|---|---|---|---|---|
| `Kim Guldstrand Larsen` | 6 | `1995-2006` | `2022` | 🟢 近年仍有直接延展 | 🟢 高 | `bblp04`、`bdl04`、`dhlp06`、`llpy97`、`lpw95`、`lpy97` |
| `Wang Yi` | 4 | `1995-2006` | `2006` | 🟧 当前核验主要停在早期主线 | 🟧 低 | `by04`、`llpy97`、`lpw95`、`lpy97` |
| `Paul Pettersson` | 4 | `1995-2006` | `2013` | 🟨 2010s 仍有延展 | 🟨 中等 | `dhlp06`、`llpy97`、`lpw95`、`lpy97` |
| `Gerd Behrmann` | 3 | `2003-2006` | `2007` | 🟧 中后期扩展后趋缓 | 🟨 中低 | `bblp04`、`bdl04`、`behrmann03` |
| `Alexandre David` | 2 | `2004-2006` | `2015` | 🟨 2010s 仍有明显扩展 | 🟩 较高 | `bdl04`、`dhlp06` |
| `Johan Bengtsson` | 2 | `2002-2004` | `2004` | 🟥 当前核验基本停在早期 | 🟥 低 | `bengtsson02`、`by04` |

### 补充作者与历史前驱

| 作者 / 别名 | 当前关联条目 | 关系定位 | 年代观察 | 检索建议 |
|---|---|---|---|---|
| `John Håkansson` / `John Haakansson` | `dhlp06` | `DBM subtraction + priorities` 的定向作者线索 | 当前核验主要落在 `2006` 附近 | 与 `UPPAAL + priority/subtraction` 联用 |
| `Fredrik Larsson` | `llpy97` | 紧凑 DBM 与状态空间削减的共作者 | 当前核验主要落在早期 DBM 主线 | 与 `UPPAAL + compact DBM/mingraph` 联用 |
| `Patricia Bouyer` | `bblp04` | zone abstraction / extrapolation 分支共作者 | 更适合作为扩展分支作者入口，而非 `UPPAAL` 主干线核心人名 | 与 `UPPAAL + abstraction/extrapolation` 联用 |
| `Radek Pelánek` / `Radek Pelanek` | `bblp04` | zone abstraction 分支共作者，检索时需兼顾重音与 ASCII 写法 | 当前核验主要落在 `2004` 左右的 abstraction 条目 | 与 `UPPAAL + zone abstraction` 联用 |
| `Rajeev Alur` | `ad90` | timed automata 理论前驱作者 | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 理论源头时纳入 |
| `David Dill` / `David L. Dill` | `ad90`、`dill89` | dense-time verification / clock constraints 的历史前驱作者 | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 技术前史时纳入 |

## 当前收录统计

- 已收录顶层条目：**11** 篇
- 本轮新增顶层条目：**11** 篇
- 含内嵌 `paper-*` 子目录的 thesis/合集条目：**2** 篇
- 内容详细程度：
  - `🟢 复现级`：**2** 篇
  - `🟩 较完整`：**6** 篇
  - `🟨 中等`：**2** 篇
  - `🟧 概览级`：**1** 篇
  - `🟥 细节不足`：**0** 篇
- 实现可获取程度：
  - `🟢 论文对应实现源码直达`：**1** 篇
  - `🟩 核心实现源码线直达`：**1** 篇
  - `🟨 部分实现源码可得`：**5** 篇
  - `🟧 仅可执行/可使用版本可得`：**2** 篇
  - `🟥 暂未获取实现源码`：**2** 篇
- 本轮未纳入/待补证条目：**1** 条

说明：`behrmann03` 与 `bengtsson02` 下的 `paper-*` 子目录当前作为父条目的辅助阅读单元存在，不单独计入以上顶层统计。

## 分类分布

| 分类 | 篇数 | 占比 | 说明 |
|---|---:|---:|---|
| 🧱 核心算法/数据结构 | 6 | 54.5% | 以 timed automata、DBM、zone、symbolic verification 主线为主 |
| ⚡ 改进与扩展 | 3 | 27.3% | 以抽象改进、优先级和更高层 symbolic 结构扩展为主 |
| 🛠️ 工程/工具链 | 2 | 18.2% | 以 `UPPAAL` toolbox、教程和建模实践入口为主 |
| 🧪 应用与案例 | 0 | 0.0% | 当前为空，后续应优先补齐 |
| **合计** | **11** | **100.0%** | - |

## 论文清单

### 🧱 / ⚡ / 🛠️ 统一总表

| 类型 | Key | 标题 | 年份 | 内容一句话简介 | 内容详细程度 | 实现可获取程度 | 源码线索 | 目录 |
|---|---|---|---:|---|---|---|---|---|
| 🧱 | `ad90` | Automata for Modeling Real-Time Systems | 1990 | timed automata 语义源头，定义了后来 `UPPAAL` 持续依赖的 clocks / guards / resets 基本模型 | 🟩 较完整 | 🟥 暂未获取实现源码 | 作为理论源头保留；当前无直接源码线索 | [ad90-timed-automata](./ad90-timed-automata/) |
| 🧱 | `dill89` | Timing Assumptions and Verification of Finite-State Concurrent Systems | 1990 | dense-time symbolic verification 的历史前驱，为后续 clock-constraint 表示提供早期语义线索 | 🟨 中等 | 🟥 暂未获取实现源码 | 作为历史前驱保留；当前无直接源码线索 | [dill89-timing-assumptions](./dill89-timing-assumptions/) |
| 🧱 | `lpw95` | Model-Checking for Real-Time Systems | 1995 | 早期 `UPPAAL` symbolic model checking 的奠基论文，解释为何约束求解和状态空间搜索成为引擎核心 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方有可下载工具线，但当前未见对应模型检查核心源码公开 | [lpw95-real-time-model-checking](./lpw95-real-time-model-checking/) |
| 🧱 | `llpy97` | Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction | 1997 | 聚焦紧凑 DBM 存储与状态空间削减，是 UDBM `mingraph` 一线的重要理论来源 | 🟢 复现级 | 🟩 核心实现源码线直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供同一技术线的核心 DBM 源码 | [llpy97-compact-data-structure](./llpy97-compact-data-structure/) |
| 🧱 | `bengtsson02` | Clocks, DBMs and States in Timed Systems | 2002 | thesis 级系统总结 DBM 操作、normalization、存储与实现，是理解 UDBM 内核的关键入口；含 `paper-a` 到 `paper-e` 子目录导航 | 🟢 复现级 | 🟢 论文对应实现源码直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[python_dbm](https://github.com/UPPAALModelChecker/python_dbm) 直接对应 DBM 实现主题 | [bengtsson02-clocks-dbms-states](./bengtsson02-clocks-dbms-states/) |
| 🧱 | `by04` | Timed Automata: Semantics, Algorithms and Tools | 2004 | 汇总 timed automata 的语义、算法与工具视角，为 `UPPAAL` 技术线提供紧凑总览 | 🟨 中等 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uls](https://github.com/UPPAALModelChecker/uls) 等组件源码可得，但完整工具主实现未公开 | [by04-semantics-algorithms-tools](./by04-semantics-algorithms-tools/) |
| ⚡ | `behrmann03` | Data Structures and Algorithms for the Analysis of Real Time Systems | 2003 | 从更高层综合说明 unions of zones、CDD、priced 方向与 `UPPAAL` 周边数据结构演进；含 `paper-intro` 与 `paper-a` 到 `paper-f` 子目录导航 | 🟩 较完整 | 🟨 部分实现源码可得 | [UCDD](https://github.com/UPPAALModelChecker/UCDD)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 可得，但 thesis 覆盖整条能力线不全有源码 | [behrmann03-real-time-data-structures](./behrmann03-real-time-data-structures/) |
| ⚡ | `bblp04` | Lower and Upper Bounds in Zone Based Abstractions of Timed Automata | 2004 | 讨论 zone abstraction 的上下界外推，是 `extrapolation` 能力链上的关键条目 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 能提供底层 DBM 源码，但该条目的完整外推实现未直出 | [bblp04-zone-based-abstractions](./bblp04-zone-based-abstractions/) |
| ⚡ | `dhlp06` | Model Checking Timed Automata with Priorities Using DBM Subtraction | 2006 | 以 DBM subtraction 支撑优先级 timed automata 分析，直接连接 federation 与差集操作需求 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供底层 DBM 技术线源码，但 priorities 主实现未直接公开 | [dhlp06-dbm-subtraction](./dhlp06-dbm-subtraction/) |
| 🛠️ | `lpy97` | UPPAAL in a Nutshell | 1997 | 早期 `UPPAAL` toolbox 总览，覆盖描述语言、模拟器、模型检查器和用户工作流 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方有文档与工具可用版本，但当前未见对应早期 toolbox 完整源码公开 | [lpy97-uppaal-nutshell](./lpy97-uppaal-nutshell/) |
| 🛠️ | `bdl04` | A Tutorial on Uppaal | 2004 | 面向建模语言、查询语言、工具界面和模式的系统教程，是工程使用入口文献 | 🟩 较完整 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer)、[uls](https://github.com/UPPAALModelChecker/uls)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 等组件源码可得，但完整工具未全部开源 | [bdl04-uppaal-tutorial](./bdl04-uppaal-tutorial/) |

### 🧪 应用与案例

当前尚无正式入账条目。后续应优先补充来自官方团队、核心作者或高质量学术工作中的代表性 `UPPAAL` 应用案例。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal/`，新增 **11** 篇基础条目，并建立 `README.md`、`GUIDE.md`、`SUMMARY.md` 三个论文集核心文件；随后补入 `behrmann03` 与 `bengtsson02` 的 `paper-*` 子目录及父子导航 README | 只从既有 `UPPAAL/UDBM` 历史论文池挑选一份可用副本，优先完成基础入库，不额外扩新论文；有现成 `content.md` 的直接规范为 `paper_content.txt`，缺失 thesis 级正文的条目用 `tools/pdf_extractor.py` 补齐；对 thesis 型条目把原有拆分子论文与 `content_assets/` 一并带入 | 先搭建 `UPPAAL` 基础文库骨架，再补齐带内嵌子论文条目的父子导航结构，为后续沿专题继续深挖做准备 |
| 2026-03-29 | 重构 `README.md`、`GUIDE.md`、`SUMMARY.md` 的文库口径，新增官方入口索引、作者主线与双维材料状态体系 | 不再以“文件齐不齐”作为主状态，而是改成“内容详细程度 + 实现可获取程度”；同时把 `🧱 / ⚡ / 🛠️` 合并进统一论文表 | 为后续沿官方 org、官方 docs、核心作者和技术分支系统扩库做准备 |
| 2026-03-29 | 补充作者年代观察与近年活动判断，并把“实现可获取程度”重定义为严格的源码标准 | 把“当前文库作者”与“较新年份的直接 `UPPAAL` 工作”显式关联，同时把二进制下载与源码实现彻底分开 | 为后续优先补 `2010s/2020s` 的 `SMC / Stratego / Tiga / 工业案例 / 现代工具链` 缺口做准备 |

## 失败与阻塞记录

| Key | 标题 | 状态 | 原因 | 后续建议 |
|---|---|---|---|---|
| `rokicki93` | Representing and Modeling Digital Circuits | 本轮未纳入 | 当前未取得合法可用全文 PDF，且与 `UPPAAL` 论文集的直接关系更偏 DBM 历史引用背景，暂不作为正式条目入库 | 若后续找到合法全文且能明确其在 `UPPAAL/DBM` 技术链中的稳定价值，再单独复核是否纳入 |
