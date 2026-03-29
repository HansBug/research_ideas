# UPPAAL 理论与技术文库总账

本文件是 `open_explore/uppaal_tech/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 理论与技术条目、分类分布、双维材料状态、更新状态和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集的定位、官方入口、作者主线和状态口径。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、回填和一致性检查规范。
3. 若任务涉及生成或重写单篇 `desc.md`，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 再使用本文件查看当前统计、状态分布、统一论文表和失败记录。
5. 若后续开始补单篇深度分析，再进入具体论文目录处理 `bibtex.bib`、`paper_content.txt` 与 `paper.pdf`。

## 收录边界回顾

为避免后续维护时误把 `uppaal_tech/` 写成泛 timed automata 收藏夹，这里重申当前论文集的边界：

1. 优先收录 `UPPAAL` 本体、核心理论基础、关键算法/数据结构、扩展能力和工程工具链工作。
2. 历史前驱理论可以收录，但必须能清楚说明它与 `UPPAAL` / UDBM 技术脉络的直接关系。
3. 应用与案例条目已迁移到同级文库 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md) 单独维护，不再在本文件正式入账。
4. 只在参考文献里提到 `UPPAAL`、正文没有实质贡献的论文，不应正式入账。

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
12. 官方 `SMC` tutorial：<https://uppaal.org/texts/uppaal-smc-tutorial.pdf>
13. 官方 `TRON` manual：<https://uppaal.org/texts/tron-manual.pdf>
14. `TRON` 功能页：<https://uppaal.org/features/#tron>

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

谱系相关扩展入口：

这部分不属于 `UPPAALModelChecker` 官方 org，但对 `timed I/O automata / ECDAR` 线的源码核验和后续扩库很重要，应与官网入口一起维护。

1. `ECDAR` 主页：<https://www.ecdar.net/>
2. `ECDAR` GitHub org：<https://github.com/Ecdar>
3. `ECDAR` 主仓库：<https://github.com/Ecdar/ECDAR>
4. `j-Ecdar`：<https://github.com/Ecdar/j-Ecdar>
5. `Reveaal`：<https://github.com/Ecdar/Reveaal>
6. `Ecdar-GUI`：<https://github.com/Ecdar/Ecdar-GUI>
7. `Ecdar-test`：<https://github.com/Ecdar/Ecdar-test>

## 贡献类型 Emoji 口径

| Emoji | 类型 | 说明 |
|---|---|---|
| 🧱 | 核心算法/数据结构 | timed automata 语义、DBM、zone、symbolic state、核心验证算法 |
| ⚡ | 改进与扩展 | 抽象优化、状态空间削减、优先级、priced/strategy/statistical 等扩展 |
| 🛠️ | 工程/工具链 | 工具架构、建模语言、查询语言、教程、建模模式、用户指南 |

`🧪 应用与案例` 已迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)，因此本总账只维护 `🧱 / ⚡ / 🛠️` 三类技术条目。

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

- 技术主线：`UPPAAL + timed automata + DBM/zone/federation/unification sharing/symbolic state/timed I/O automata/dynamic extrapolation`
- 扩展主线：`UPPAAL + guided synthesis/priced/cost-optimal/Tiga/statistical model checking/stochastic hybrid systems/stochastic hybrid games/compact strategies/SOS/importance splitting/randomized reachability/randomized refinement/MCTS/Coshy`
- 工程主线：`UPPAAL + architecture/implementation/tutorial/TRON/online testing/T-Uppaal/relativized ioco/timed trace inclusion/ECDAR/compositional verification`
- 作者主线：`Kim Guldstrand Larsen`、`Alexandre David`、`Marius Mikučionis`、`Ulrik Nyman`、`Axel Legay`、`Andrzej Wąsowski`、`Peter Gjøl Jensen`
- 分支作者：`Brian Nielsen`、`Thomas Hune`、`Sean Sedwards`、`Andrej Kiviriga`、`Pranav Ashok`
- 应用主线：已迁出到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)，本文件不再继续展开

### 已观察到的高命中特征

- 标题直接出现 `UPPAAL`、`TRON`、`online testing`、`timed I/O automata`、`SMC`、`stochastic hybrid systems`、`compact strategies`、`SOS`
- `作者名 + 分支词 + pdf/site:uppaal.org` 的检索效果显著提升，尤其是 `Kim Guldstrand Larsen`、`Marius Mikucionis`、`Ulrik Nyman` 这几条线
- `uppaal.org/texts/`、Aalborg / VBN / Dagstuhl / EPTCS 等官方或机构直链 PDF 命中率明显高于只搜 DOI
- `ECDAR / TIOA` 相关条目里，`ecdar.net` 与 `github.com/Ecdar` 能直接提供源码核验入口
- `TRON / online testing` 相关条目里，官方 `TRON manual` 与 `features/#tron` 对判断“只有运行版还是有源码”很关键

### 已观察到的低命中特征

- 只写 `hybrid systems`、`planning`、`Monte Carlo Tree Search`，但不带 `UPPAAL / ECDAR / timed automata`
- 只写 `model-based testing`，却不带 `TRON / online testing / timed trace inclusion / relativized ioco`
- 只在 related work 里顺带提一次 `UPPAAL` 的概率验证或博弈验证论文
- 只用工具名或只用作者名单独搜索，都容易造成噪声膨胀
- 只有教程页、案例页、安装说明而没有正式论文正文的条目，不适合直接正式入账

### 检索倾向调整

- 当前文库已经补上 `2001-2012` 的 `guided synthesis / TRON / SHS` 与 `2019` 的 `compact strategies / SOS`，下一轮应继续定点补缺口而不是泛泛扩年份
- `⚡` 改进与扩展仍是当前主干，后续应继续沿 `importance splitting / planning-guided exploration / UPPAAL 5 / shield synthesis` 扩张
- `2016-2018` 仍偏空，应优先补这段过渡期的核心技术条目，而不是只继续堆 `2020s`
- 应用检索线已迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)，本文件后续只保留必要的技术侧分流说明
- 每次更新前先删减失效关键词，保持本节简洁

## 技术演进时间线与近年活动观察

- 当前已收录顶层条目已经覆盖 `1990-2025`，不再只停留在 `1990-2015` 的早中期奠基阶段。
- 当前技术主线已经可以拆成“理论奠基 -> 架构与数据结构固化 -> testing / games 分叉 -> specification theory / ECDAR -> SMC / Stratego -> randomized / planning / modern abstractions / Coshy”这几段。
- 官方 changelog 仍显示后续版本持续发布：`2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5`、`2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
- 官方 GitHub org 也显示近期仍有源码活动：`UDBM`、`utap`、`uppaal-libs`、`docs.uppaal.org` 在 `2025-2026` 仍有更新。
- 当前最明显的技术缺口仍是 `2016-2018`，尤其是 `importance splitting`、更系统的 `UPPAAL 5` 技术论文和若干现代搜索/抽象优化条目。

### 技术演进线总表

| 阶段 | 时间范围 | 主线主题 | 关键问题 | 代表条目 | 当前判断 |
|---|---|---|---|---|---|
| 理论前史与引擎奠基 | `1990-1997` | timed automata 语义、symbolic model checking、compact DBM | 如何用 clocks / guards / resets / symbolic states 表示 dense-time reachability | `ad90`、`lpw95`、`llpy97`、`lpy97` | 基础骨架已经清楚，后续主要是按引用关系回看源头 |
| 架构重构与数据结构专题化 | `2001-2004` | architecture、implementation、DBM / zone / federation / CDD | 如何把理论底盘做成可扩展引擎，并压缩状态空间与约束表示 | `behrmann01`、`bengtsson02`、`behrmann03`、`bblp04`、`bdl04` | 这是当前文库最完整的一段，也是后续继续补链的基准骨架 |
| 测试与博弈工具化 | `2003-2008` | `TRON`、online testing、timed games、`Tiga` | 如何从验证走向 on-the-fly testing 与 controller synthesis | `mikucionis03`、`larsen04-online`、`cassez05`、`behrmann07`、`hessel08` | 支线已经成形，但源码开放性明显弱于 `DBM / ECDAR` 线 |
| 规范理论化与组合验证 | `2010-2013` | `TIOA`、specification theory、`ECDAR`、compositional verification | 如何定义 refinement / consistency / quotient，并把它做成组件级验证框架 | `david10-method`、`david10-spec`、`david12-ecdar`、`david13-rtspec` | 这是当前“理论最完整且实现可追”的一段，适合继续沿作者线深挖 |
| 统计模型检查与策略优化 | `2011-2015` | `SMC`、priced PTA、expected cost、`Stratego` | 如何把概率、代价与优化能力接入 `UPPAAL` | `david11-smc`、`david12-shs`、`david14`、`david15-smc`、`david15-stratego` | 主线已经清楚，但向近年现代版本过渡时仍缺中间段 |
| 过渡空档与待补带 | `2016-2018` | `UPPAAL 5`、importance splitting、过渡期现代化 | 如何把 `SMC / Stratego` 进一步推到更现代的搜索与统计框架 | `importance-splitting-line` | 这是当前最明显的时间缺口，下一轮应优先定点补齐 |
| 紧凑策略与混成博弈回潮 | `2019` | compact strategies、`SOS`、stochastic hybrid games | 如何在 stochastic / hybrid 场景下同时兼顾 safe、optimal、small | `ashok19-sos`、`larsen19-compact` | 已经有定题点，但仍需继续追其后续实现与扩展 |
| 随机化、规划、现代抽象与新近混成扩展 | `2020-2025` | randomized analysis、`MCTS`、dynamic extrapolation、`Coshy` | 如何在可扩展性、规划能力、现代 `XTA` 抽象和 hybrid shielding 之间继续推进 | `kiviriga20-randref`、`kiviriga21-randreach`、`jensen22-mcts`、`jensen23-dynext`、`brorholt25-coshy` | 说明 `UPPAAL` 技术线没有停在零几年，近年仍在持续演进 |

## 现有收录论文作者关联

以下作者关系只基于当前 **45 个顶层条目** 的 `bibtex.bib` 统计；`paper-*` 子目录当前不单独重复计数。后续扩库时，应先沿这张作者关系表追踪，再去官方入口核验源码、案例和工具实现。

这里的“继续沿该作者线扩张判断”是**检索价值推断**，表示继续顺着该作者找 `UPPAAL` 后续工作时的预期收益，不是对作者个人职业状态的断言。

### 核心作者主线

| 作者 | 频次 | 角色判断 | 主要贡献方向 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 年份 | 最近性判断 | 继续沿该作者线扩张判断 | 代表关联条目 |
|---|---:|---|---|---|---|---|---|---|
| `Kim Guldstrand Larsen` | 36 | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / Tiga / SMC / Stratego / TRON / ECDAR / modern extensions` | `1995-2025` | `2025` | 🟢 早期到近年全程贯穿 | 🟢 高 | `lpw95`、`behrmann07`、`mikucionis03`、`david13`、`larsen19`、`brorholt25` |
| `Alexandre David` | 21 | 中后期扩展主线整合者 | `architecture / Tiga / SMC / expected cost / Stratego / TIOA / SHS` | `2001-2015` | `2015` | 🟨 文库内高频但近年直接条目暂止于 `2015` | 🟢 高 | `behrmann02`、`david10-*`、`david11-*`、`david12-*`、`david14`、`david15-*` |
| `Axel Legay` | 11 | `SMC + specification theory` 桥接作者 | `statistical model checking / priced models / timed I/O specification / optimization / SHS` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接延展 | 🟢 高 | `david10-*`、`david11-*`、`david12-*`、`david13`、`david14`、`goorden23` |
| `Gerd Behrmann` | 11 | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / UPPAAL 4.0 / evolution survey` | `2001-2011` | `2011` | 🟨 中期工程主线已较完整 | 🟨 中等 | `amnell01`、`behrmann02-*`、`behrmann03`、`behrmann06`、`behrmann07`、`behrmann11` |
| `Marius Mikučionis` / `Marius Mikucionis` | 9 | `TRON -> SMC -> Stratego -> Coshy` 纵向桥接作者 | `online testing / statistical model checking / strategy synthesis / hybrid shielding` | `2003-2025` | `2025` | 🟢 横跨早期测试线和近年扩展线 | 🟢 高 | `mikucionis03`、`larsen04-*`、`hessel08`、`mikucionis10`、`david12-shs`、`brorholt25` |
| `Paul Pettersson` | 9 | `DBM / engine / testing` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities / TRON` | `1995-2011` | `2011` | 🟨 更偏历史骨干作者 | 🟨 中等 | `lpw95`、`llpy97`、`amnell01`、`hessel08`、`dhlp06`、`behrmann11` |
| `Wang Yi` | 9 | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations / DBM` | `1995-2011` | `2011` | 🟨 早期到中期主线较完整 | 🟨 中等 | `lpw95`、`llpy97`、`amnell01`、`by04`、`behrmann02`、`behrmann06` |
| `Ulrik Nyman` | 8 | `ECDAR / TIOA / randomized analysis` 主线组织者 | `specification theory / refinement / compositional verification / randomized analysis / planning` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接论文 | 🟢 高 | `david10-*`、`david12-ecdar`、`david13`、`kiviriga20`、`kiviriga21`、`jensen22` |
| `Andrzej Wąsowski` | 6 | `ECDAR` 规范理论与新近扩展连接者 | `timed I/O specification / quotient / compositional verification / Coshy 协作线` | `2010-2025` | `2025` | 🟢 近年仍有直接条目 | 🟢 高 | `david10-*`、`david12-ecdar`、`david13`、`goorden23`、`brorholt25` |
| `Peter Gjøl Jensen` | 5 | `optimization -> planning -> hybrid synthesis` 桥接作者 | `expected cost / Stratego / MCTS / dynamic extrapolation / Coshy` | `2014-2025` | `2025` | 🟢 近年仍有连续新作 | 🟢 高 | `david14`、`david15-stratego`、`jensen22`、`jensen23`、`brorholt25` |

### 分支协作者与历史前驱

| 作者 / 别名 | 当前关联条目 | 角色判断 | 主要贡献方向 | 年代观察 | 检索建议 |
|---|---|---|---|---|---|
| `Brian Nielsen` | `mikucionis03`、`larsen04-*`、`hessel08` | `TRON / online testing` 分支关键协作者 | `model-based testing / timed trace inclusion / relativized ioco / online testing` | 当前文库直接覆盖 `2003-2008` | 与 `UPPAAL + TRON/online testing/timed trace inclusion` 联用 |
| `Thomas Hune` | `amnell01`、`hune01` | 早期 `guided synthesis` 线作者 | `guided synthesis / control programs / early tool planning` | 当前文库直接覆盖 `2001` | 与 `UPPAAL + guided synthesis/control` 联用 |
| `Sean Sedwards` | `david12-shs` | `SHS / SMC` 分支补强作者 | `stochastic hybrid systems / simulation semantics / statistical analysis` | 当前文库直接覆盖 `2012` | 与 `UPPAAL + stochastic hybrid systems/SMC` 联用 |
| `Pranav Ashok` / `Jan Křetínský` / `Adrien Le Coënt` / `Jakob Haahr Taankvist` / `Maximilian Weininger` | `ashok19-sos` | `compact strategies / hybrid MDP` 分支作者群 | `safe-optimal-small strategies / stochastic hybrid games / hybrid MDP` | 当前文库直接覆盖 `2019` | 与 `UPPAAL + SOS/compact strategies/stochastic hybrid games` 联用 |
| `Andrej Kiviriga` | `kiviriga20`、`kiviriga21`、`jensen22` | `randomized analysis / planning` 新近主线作者 | `randomized refinement / randomized reachability / MCTS` | 当前文库直接覆盖 `2020-2022` | 与 `UPPAAL + randomized reachability/refinement/MCTS` 联用 |
| `Nicolaj Ø. Jensen` | `jensen23` | `modern XTA abstraction` 新近作者 | `dynamic extrapolation / extended timed automata / static analysis` | 当前文库当前只覆盖 `2023`，但方向明显对接现代引擎优化 | 与 `UPPAAL + dynamic extrapolation/XTA` 联用 |
| `Martijn A. Goorden` | `goorden23` | `TIOA` 规范理论补完作者 | `complete specification theory / ECDAR` | 当前文库当前只覆盖 `2023`，适合继续追 `ECDAR` 理论后续 | 与 `UPPAAL + timed I/O automata/specification theory` 联用 |
| `Asger Horn Brorholt` | `brorholt25` | `Coshy` 新近作者 | `automatic shield synthesis / hybrid systems / compact shields` | 当前文库当前只覆盖 `2025`，但非常新，后续继续扩张概率高 | 与 `UPPAAL + Coshy/hybrid shield synthesis` 联用 |
| `Didier Lime` | `cassez05`、`behrmann07`、`david14` | `timed games -> Tiga -> optimization` 分支协作者 | `timed games / controller synthesis / cost analysis` | 当前文库已直接覆盖到 `2014` | 与 `UPPAAL + timed games/Tiga/cost` 联用 |
| `Johan Bengtsson` | `bengtsson02`、`behrmann02-secrets`、`by04` | `DBM` 数据结构专题化奠基作者 | `clocks / DBMs / states / DBM internals / implementation detail` | 当前文库主要落在 `2002-2004` | 与 `UPPAAL + DBM/implementation` 联用 |
| `Patricia Bouyer` / `Radek Pelánek` | `bblp04` | zone abstraction 外推分支外部关键合作者 | `lower-upper bound extrapolation / zone abstraction` | 当前文库主要落在 `2004` | 与 `UPPAAL + abstraction/extrapolation` 联用 |
| `Rajeev Alur` | `ad90` | 理论前史奠基者 | `timed automata semantics` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 理论源头时纳入 |
| `David Dill` / `David L. Dill` | `ad90`、`dill89` | dense-time verification 前史奠基者 | `timing assumptions / clock constraints / symbolic verification` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 技术前史时纳入 |

## 当前收录统计

- 已收录顶层条目：**45** 篇
- 本轮新增顶层条目：**0** 篇（本次仅做文库拆分与文档重构）
- 含内嵌 `paper-*` 子目录的 thesis/合集条目：**2** 篇
- 已完成 `desc.md` 的顶层条目：**1** 篇
- 内容详细程度：
  - `🟢 复现级`：**4** 篇
  - `🟩 较完整`：**24** 篇
  - `🟨 中等`：**9** 篇
  - `🟧 概览级`：**8** 篇
  - `🟥 细节不足`：**0** 篇
- 实现可获取程度：
  - `🟢 论文对应实现源码直达`：**3** 篇
  - `🟩 核心实现源码线直达`：**5** 篇
  - `🟨 部分实现源码可得`：**12** 篇
  - `🟧 仅可执行/可使用版本可得`：**22** 篇
  - `🟥 暂未获取实现源码`：**3** 篇
- 本轮未纳入/待补证条目：**2** 条
- 已记录环境级阻塞：**1** 条

说明：`behrmann03` 与 `bengtsson02` 下的 `paper-*` 子目录当前作为父条目的辅助阅读单元存在，不单独计入以上顶层统计。

## 分类分布

| 分类 | 篇数 | 占比 | 说明 |
|---|---:|---:|---|
| 🧱 核心算法/数据结构 | 8 | 17.8% | 已覆盖 timed automata、DBM、zone、specification theory、dynamic extrapolation 等主线 |
| ⚡ 改进与扩展 | 23 | 51.1% | 已覆盖 guided synthesis、priced/cost-optimal、timed games、Tiga、SMC、SHS、Stratego、randomized analysis、MCTS、compact strategies、Coshy |
| 🛠️ 工程/工具链 | 14 | 31.1% | 已覆盖 architecture、implementation、tutorial、`UPPAAL 4.0`、`TRON/testing`、`ECDAR/SMC` 工程入口与路线综述 |
| **合计** | **45** | **100.0%** | - |

说明：应用类条目已迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md) 单独维护。

## 单篇 `DESC` 对齐口径

后续单篇 `desc.md` 统一遵循 [DESC_GUIDE.md](./DESC_GUIDE.md)。

本总表中的三列：

1. `问题简述`
2. `方法简述`
3. `解决点简述`

是单篇 `desc.md` 开头三条一句话简述的压缩版。也就是说：

1. `SUMMARY.md` 负责全局速览。
2. `desc.md` 负责把单篇的问题、方法和解决点展开讲清楚。

## 论文清单

### 🧱 / ⚡ / 🛠️ 统一总表（按年份升序，含问题/方法/解决点简述）

| 类型 | Key | 标题 | 年份 | 问题简述 | 方法简述 | 解决点简述 | 内容详细程度 | 实现可获取程度 | 源码线索 | 目录 |
|---|---|---|---:|---|---|---|---|---|---|---|
| 🧱 | `ad90` | Automata for Modeling Real-Time Systems | 1990 | 实时系统缺少统一时钟自动机模型 | 定义 clocks/guards/resets 的 timed automata 语义 | 奠定 `UPPAAL` 全部时钟自动机底座 | 🟩 较完整 | 🟥 暂未获取实现源码 | 作为理论源头保留；当前无直接源码线索 | [ad90-timed-automata](./ad90-timed-automata/) |
| 🧱 | `dill89` | Timing Assumptions and Verification of Finite-State Concurrent Systems | 1990 | dense-time 并发验证缺少可操作约束表示 | 用 timing assumptions 与 symbolic clock constraints | 提供 clock-constraint 前史基础 | 🟨 中等 | 🟥 暂未获取实现源码 | 作为历史前驱保留；当前无直接源码线索 | [dill89-timing-assumptions](./dill89-timing-assumptions/) |
| 🧱 | `lpw95` | Model-Checking for Real-Time Systems | 1995 | real-time reachability 穷举验证代价过高 | symbolic states + constraint solving + on-the-fly | 立起早期 `UPPAAL` 验证核心 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方有可下载工具线，但当前未见对应模型检查核心源码公开 | [lpw95-real-time-model-checking](./lpw95-real-time-model-checking/) |
| 🧱 | `llpy97` | Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction | 1997 | DBM 存储大且状态空间膨胀 | compact DBM + state-space reduction | 降低 `UDBM/UPPAAL` 内存与搜索成本 | 🟢 复现级 | 🟩 核心实现源码线直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供同一技术线的核心 DBM 源码 | [llpy97-compact-data-structure](./llpy97-compact-data-structure/) |
| 🛠️ | `lpy97` | UPPAAL in a Nutshell | 1997 | 工具功能、语义与工作流难整体把握 | 系统总览 description/simulator/checker 流程 | 给出早期完整工具结构与使用入口 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方有文档与工具可用版本，但当前未见对应早期 toolbox 完整源码公开 | [lpy97-uppaal-nutshell](./lpy97-uppaal-nutshell/) |
| 🛠️ | `amnell01` | UPPAAL - Now, Next, and Future | 2001 | 早期 `UPPAAL` 能力边界与路线不清 | 官方路线综述与能力盘点 | 明确 early roadmap 与技术议程 | 🟧 概览级 | 🟨 部分实现源码可得 | 可沿 [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 追同代核心组件源码线，但论文本身无实现直链 | [amnell01-uppaal-now-next-future](./amnell01-uppaal-now-next-future/) |
| ⚡ | `behrmann01` | Efficient Guiding Towards Cost-Optimality in UPPAAL | 2001 | timed reachability 缺少代价最优能力 | 引入 cost-guided symbolic search | 打开 priced/cost-optimal 主线 | 🟩 较完整 | 🟥 暂未获取实现源码 | 论文可得；当前未见与该分支直接对应的公开源码线 | [behrmann01-cost-optimality-uppaal](./behrmann01-cost-optimality-uppaal/) |
| ⚡ | `hune01` | Guided Synthesis of Control Programs Using Uppaal | 2001 | control synthesis 难与 timed analysis 衔接 | 用 `UPPAAL` 分析结果引导控制程序合成 | 把合成问题接入 `UPPAAL` 技术线 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前仅能核到论文与工具历史材料；guided synthesis 对应实现源码未见公开 | [hune01-guided-synthesis-control-programs-uppaal](./hune01-guided-synthesis-control-programs-uppaal/) |
| 🛠️ | `bdly02` | New UPPAAL Architecture | 2002 | 旧引擎架构不利于扩展与组件化 | 重构模块化架构与引擎分层 | 为后续组件化演进打底 | 🟨 中等 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 等组件源码可得 | [behrmann02-new-uppaal-architecture](./behrmann02-new-uppaal-architecture/) |
| 🧱 | `bengtsson02` | Clocks, DBMs and States in Timed Systems | 2002 | DBM 语义、操作与存储缺少系统说明 | thesis 级系统整理 `DBM/normalization/storage` | 成为 `UDBM` 内核理解主入口 | 🟢 复现级 | 🟢 论文对应实现源码直达 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[python_dbm](https://github.com/UPPAALModelChecker/python_dbm) 直接对应 DBM 实现主题 | [bengtsson02-clocks-dbms-states](./bengtsson02-clocks-dbms-states/) |
| 🛠️ | `bbdlpy02` | UPPAAL Implementation Secrets | 2003 | 引擎实现选择与性能来源不透明 | 拆解实现细节、表示和优化技巧 | 解释 `UPPAAL` 工程效率从何而来 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer) 等组件源码可得 | [behrmann02-uppaal-implementation-secrets](./behrmann02-uppaal-implementation-secrets/) |
| ⚡ | `behrmann03` | Data Structures and Algorithms for the Analysis of Real Time Systems | 2003 | 单一 DBM 表示难覆盖更复杂分析需求 | 系统整理 zones/CDD/priced 数据结构与算法 | 扩展 real-time analysis 数据结构版图 | 🟩 较完整 | 🟨 部分实现源码可得 | [UCDD](https://github.com/UPPAALModelChecker/UCDD)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 可得，但 thesis 覆盖整条能力线不全有源码 | [behrmann03-real-time-data-structures](./behrmann03-real-time-data-structures/) |
| ⚡ | `david03-share` | Unification \& Sharing in Timed Automata Verification | 2003 | 符号状态和约束重复造成存储浪费 | unification \& sharing 复用状态与约束 | 压缩表示并提升验证效率 | 🟨 中等 | 🟨 部分实现源码可得 | 可沿 [UDBM](https://github.com/UPPAALModelChecker/UDBM) 与 [utap](https://github.com/UPPAALModelChecker/utap) 追底层符号表示和解析器源码，但论文对应优化实现未完整公开 | [david03-unification-sharing-timed-automata-verification](./david03-unification-sharing-timed-automata-verification/) |
| 🛠️ | `mikucionis03-tron` | Online On-the-Fly Testing of Real-time Systems | 2003 | 实时系统测试难在线利用模型 | on-the-fly testing + timed trace inclusion | 把验证能力扩到实时在线测试 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [downloads](https://uppaal.org/downloads/) 可追运行工具线，但 `TRON` 核心源码未见公开 | [mikucionis03-online-on-the-fly-testing-real-time-systems](./mikucionis03-online-on-the-fly-testing-real-time-systems/) |
| ⚡ | `bblp04` | Lower and Upper Bounds in Zone Based Abstractions of Timed Automata | 2004 | zone abstraction 的精度与终止性难平衡 | lower/upper bound extrapolation | 稳定化 zone abstraction 理论 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 能提供底层 DBM 源码，但该条目的完整外推实现未直出 | [bblp04-zone-based-abstractions](./bblp04-zone-based-abstractions/) |
| 🛠️ | `bdl04` | A Tutorial on Uppaal | 2004 | 用户缺少系统建模与查询指导 | 教程化组织 language/query/interface/patterns | 成为工程使用入口文献 | 🟩 较完整 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer)、[uls](https://github.com/UPPAALModelChecker/uls)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 等组件源码可得，但完整工具未全部开源 | [bdl04-uppaal-tutorial](./bdl04-uppaal-tutorial/) |
| 🧱 | `by04` | Timed Automata: Semantics, Algorithms and Tools | 2004 | timed automata 语义算法工具脉络分散 | 统一综述 semantics + algorithms + tools | 压缩整理 timed automata/`UPPAAL` 骨架 | 🟨 中等 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uls](https://github.com/UPPAALModelChecker/uls) 等组件源码可得，但完整工具主实现未公开 | [by04-semantics-algorithms-tools](./by04-semantics-algorithms-tools/) |
| 🛠️ | `larsen04-online` | Online Testing of Real-time Systems Using Uppaal | 2004 | online testing 缺少可执行工具链 | `TRON` workflow + verdict 执行链 | 让 testing 分支工具化落地 | 🟨 中等 | 🟧 仅可执行/可使用版本可得 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [features/#tron](https://uppaal.org/features/#tron) 可核验能力线，但核心源码未见公开 | [larsen04-online-testing-real-time-systems-using-uppaal](./larsen04-online-testing-real-time-systems-using-uppaal/) |
| 🛠️ | `larsen04-status` | Online Testing of Real-time Systems using Uppaal: Status and Future Work | 2004 | `TRON` 当前状态与后续缺口不清 | status review + future-work mapping | 明确 testing 分支议程 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 当前能核到论文与官方测试文档，但未见对应源码公开 | [larsen04-online-testing-status-future-work](./larsen04-online-testing-status-future-work/) |
| ⚡ | `cdfll05` | Efficient On-the-fly Algorithms for the Analysis of Timed Games | 2005 | timed games on-the-fly analysis 效率不足 | 高效 on-the-fly timed-game 算法 | 成为 `Tiga` 的关键理论前置 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前未见 timed-games 核心源码公开；可沿 `Tiga` 工具线与官方文档反查 | [cassez05-analysis-of-timed-games](./cassez05-analysis-of-timed-games/) |
| 🛠️ | `behrmann06` | UPPAAL 4.0 | 2006 | 新一代工具能力需要统一对外说明 | 版本快照式整理 language/engine/workflow | 标记 `UPPAAL 4.0` 整合阶段 | 🟧 概览级 | 🟨 部分实现源码可得 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 提供部分源码线索 | [behrmann06-uppaal-4](./behrmann06-uppaal-4/) |
| ⚡ | `dhlp06` | Model Checking Timed Automata with Priorities Using DBM Subtraction | 2006 | priority timed automata 缺少可操作符号差集 | 用 DBM subtraction 支撑 priority analysis | 打通 priorities/federation 分析路径 | 🟩 较完整 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供底层 DBM 技术线源码，但 priorities 主实现未直接公开 | [dhlp06-dbm-subtraction](./dhlp06-dbm-subtraction/) |
| ⚡ | `bcdfll07` | UPPAAL-Tiga: Time for Playing Games! | 2007 | timed-game controller synthesis 缺少工具支撑 | 把 timed games 工具化为 `UPPAAL-Tiga` | 博弈/控制分支正式成型 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 当前未见 `Tiga` 核心源码公开；可沿官方 `Tiga` 历史工具线与文档反查 | [behrmann07-uppaal-tiga](./behrmann07-uppaal-tiga/) |
| 🛠️ | `hessel08-tron` | Testing Real-Time Systems Using UPPAAL | 2008 | testing 理论与工具实践资料分散 | 系统整理 offline/online testing 与 relativized ioco | 成为 `TRON/testing` 标准综述 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [features/#tron](https://uppaal.org/features/#tron) 可核验方法线，但源码未见公开 | [hessel08-testing-real-time-systems-using-uppaal](./hessel08-testing-real-time-systems-using-uppaal/) |
| 🛠️ | `david10-method` | Methodologies for Specification of Real-Time Systems Using Timed I/O Automata | 2010 | 实时组件规约缺少可执行方法学 | `TIOA` 的 refinement/abstraction/quotient workflow | 给出 `ECDAR` 工程方法入口 | 🟨 中等 | 🟩 核心实现源码线直达 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 提供该方法线的开源工具入口 | [david10-methodologies-timed-io-automata](./david10-methodologies-timed-io-automata/) |
| 🧱 | `david10-spec` | Timed I/O automata: a complete specification theory for real-time systems | 2010 | real-time component specification theory 不完整 | 补全 refinement/consistency/composition/quotient 理论 | 奠定 `ECDAR` 形式化核心 | 🟩 较完整 | 🟩 核心实现源码线直达 | [ECDAR](https://github.com/Ecdar/ECDAR) 与 [Reveaal](https://github.com/Ecdar/Reveaal) 提供同一规范理论/检查线的开源实现入口 | [david10-timed-io-automata-complete-specification-theory](./david10-timed-io-automata-complete-specification-theory/) |
| 🛠️ | `mikucionis10-tron` | Online Testing of Real-time Systems | 2010 | 实时 online testing 缺少完整模型算法工具说明 | thesis 级整理生成/执行/verdict 框架 | 成为 testing 分支最完整单篇入口 | 🟢 复现级 | 🟧 仅可执行/可使用版本可得 | 当前能核到论文、手册与运行版能力线，但 `TRON` 论文对应源码未见公开 | [mikucionis10-online-testing-real-time-systems](./mikucionis10-online-testing-real-time-systems/) |
| 🛠️ | `bdlpy11` | Developing UPPAAL over 15 years | 2011 | 15 年演进脉络分散难整体理解 | 工程与历史 retrospective | 总结 branch splitting 与成熟过程 | 🟧 概览级 | 🟨 部分实现源码可得 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 与官方文档站可作为对应工程线索 | [behrmann11-developing-uppaal-over-15-years](./behrmann11-developing-uppaal-over-15-years/) |
| ⚡ | `dllmpvw11` | Statistical Model Checking for Networks of Priced Timed Automata | 2011 | priced timed automata 缺少 statistical analysis | 对 `NPTA/PTA` 做 statistical model checking | 连接概率分析与代价分析 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 SMC 文档、教程与工具线可用，但对应扩展核心源码未见公开 | [david11-smc-priced-timed-automata](./david11-smc-priced-timed-automata/) |
| ⚡ | `dllmw11` | Time for Statistical Model Checking of Real-time Systems | 2011 | 穷举验证难覆盖随机实时行为 | 将 `SMC` 引入 real-time systems | 奠定 `UPPAAL-SMC` 主线 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 官方 SMC 文档、教程与工具线可用，但核心源码未见公开 | [david11-statistical-model-checking-real-time](./david11-statistical-model-checking-real-time/) |
| ⚡ | `bdllmp12` | Checking \& Distributing Statistical Model Checking | 2012 | `SMC` 计算规模受单机限制 | distributed statistical model checking | 扩大实验规模与算力利用 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前可沿官方 SMC 工具线追运行版本，但分布式扩展源码未见公开 | [bulychev12-distributed-statistical-model-checking](./bulychev12-distributed-statistical-model-checking/) |
| ⚡ | `david12-ecdar` | Compositional verification of real-time systems using Ecdar | 2012 | component verification 难以组合扩展 | `ECDAR` 中的 compositional verification 工具链 | 让组合验证可直接操作 | 🟩 较完整 | 🟢 论文对应实现源码直达 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 直接对应 `ECDAR` 工具线 | [david12-compositional-verification-ecdar](./david12-compositional-verification-ecdar/) |
| ⚡ | `david12-shs` | Statistical Model Checking for Stochastic Hybrid Systems | 2012 | stochastic hybrid systems 难做穷举验证 | 把 `SMC` 扩到 stochastic hybrid semantics | 将 `SMC` 推向 hybrid systems | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前能核到论文、SMC 工具线与教程，但论文对应 `SHS` 扩展源码未见公开 | [david12-statistical-model-checking-stochastic-hybrid-systems](./david12-statistical-model-checking-stochastic-hybrid-systems/) |
| 🧱 | `david13-rtspec` | Real-time specifications | 2013 | specification theory 的规则和语义分散 | 系统整理 operators、闭包与工具语义 | 成为 `TIOA/ECDAR` 标准参考 | 🟩 较完整 | 🟩 核心实现源码线直达 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 构成对应实现主线 | [david13-real-time-specifications](./david13-real-time-specifications/) |
| ⚡ | `djlllst14` | On Time with Minimal Expected Cost! | 2014 | 不确定实时系统缺少 expected-cost 优化 | 把 expected-cost 查询接入 `SMC/optimization` | 为 `Stratego` 优化铺路 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 可沿 `SMC / Stratego` 工具线追可运行版本，但核心优化源码未见公开 | [david14-minimal-expected-cost](./david14-minimal-expected-cost/) |
| 🛠️ | `david15-smc` | Uppaal SMC tutorial | 2015 | `SMC` 查询语义与用法难掌握 | 教程化讲解 stochastic semantics 与 query patterns | 提供 `SMC` 工程使用入口 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方 [SMC tutorial](https://uppaal.org/texts/uppaal-smc-tutorial.pdf) 与 [downloads](https://uppaal.org/downloads/) 可得，但核心源码未公开 | [david15-uppaal-smc-tutorial](./david15-uppaal-smc-tutorial/) |
| ⚡ | `djlmt15` | Uppaal Stratego | 2015 | 策略生成与优化缺少统一工具 | 支持 strategy generation/comparison/optimization | 策略优化分支工具化成形 | 🟧 概览级 | 🟧 仅可执行/可使用版本可得 | 官方文档与工具线可追，但 `Stratego` 核心源码未见公开 | [david15-uppaal-stratego](./david15-uppaal-stratego/) |
| ⚡ | `ashok19-sos` | SOS: Safe, Optimal and Small Strategies for Hybrid Markov Decision Processes | 2019 | hybrid MDP 策略难同时安全最优且紧凑 | safe optimal small strategy synthesis | 定题 compact strategy / hybrid MDP | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前可核到论文与相关工具分支，但 `SOS` 对应源码未见公开 | [ashok19-sos-safe-optimal-small-strategies-hybrid-markov-decision-processes](./ashok19-sos-safe-optimal-small-strategies-hybrid-markov-decision-processes/) |
| ⚡ | `larsen19-compact` | Synthesis of Safe, Optimal and Compact Strategies for Stochastic Hybrid Games (Invited Paper) | 2019 | stochastic hybrid games 需要 safe/optimal/compact controllers | 概括 compact strategy synthesis 路线 | 为 `SOS/Coshy` 线定型 | 🟨 中等 | 🟧 仅可执行/可使用版本可得 | 当前能核到论文与官方 `Coshy` 线索，但对应策略合成源码未见公开 | [larsen19-synthesis-safe-optimal-compact-strategies-stochastic-hybrid-games](./larsen19-synthesis-safe-optimal-compact-strategies-stochastic-hybrid-games/) |
| ⚡ | `kiviriga20-randref` | Randomized Refinement Checking of Timed I/O Automata | 2020 | symbolic refinement 检查扩展性不足 | randomized walk / falsification-style refinement | 提高 `TIOA` refinement 可扩展性 | 🟩 较完整 | 🟩 核心实现源码线直达 | 可沿 [ECDAR](https://github.com/Ecdar/ECDAR) 与 [Reveaal](https://github.com/Ecdar/Reveaal) 追 `TIOA` 检查实现主线 | [kiviriga20-randomized-refinement-checking-tioa](./kiviriga20-randomized-refinement-checking-tioa/) |
| ⚡ | `kiviriga21-randreach` | Randomized Reachability Analysis in Uppaal: Fast Error Detection in Timed Systems | 2021 | rare errors 难快速发现 | randomized reachability / fast falsification | 引入轻量 error-detection 工作流 | 🟩 较完整 | 🟧 仅可执行/可使用版本可得 | 当前可沿 [downloads](https://uppaal.org/downloads/) 与 [documentation](https://docs.uppaal.org/) 追工具能力，但 randomized reachability 主实现源码未见公开 | [kiviriga21-randomized-reachability-analysis-uppaal](./kiviriga21-randomized-reachability-analysis-uppaal/) |
| ⚡ | `jensen22-mcts` | Monte Carlo Tree Search for Priced Timed Automata | 2022 | priced timed automata 规划搜索代价高 | `Monte Carlo Tree Search` | 把 planning search 接到 PTA 分析 | 🟨 中等 | 🟧 仅可执行/可使用版本可得 | 当前未见论文对应 `MCTS` 扩展源码公开；至多能沿 [downloads](https://uppaal.org/downloads/) 追主工具可运行版本 | [jensen22-monte-carlo-tree-search-priced-timed-automata](./jensen22-monte-carlo-tree-search-priced-timed-automata/) |
| ⚡ | `goorden23-tioa` | Timed I/O Automata: It is never too late to complete your timed specification theory | 2023 | 旧 `TIOA` 理论与实现仍不完整 | 补全证明并给出新开源实现 | 补齐新一代 `ECDAR` 规范线 | 🟢 复现级 | 🟢 论文对应实现源码直达 | 论文明确指向开源 [ECDAR](https://github.com/Ecdar/ECDAR)；同 org 还有 [Reveaal](https://github.com/Ecdar/Reveaal) 与 [j-Ecdar](https://github.com/Ecdar/j-Ecdar) | [goorden23-timed-io-automata-never-too-late](./goorden23-timed-io-automata-never-too-late/) |
| ⚡ | `jensen23-dynext` | Dynamic Extrapolation in Extended Timed Automata | 2023 | extended timed automata 抽象过粗且开销高 | 面向 `XTA` 的 dynamic extrapolation | 收紧现代 `UPPAAL` 抽象精度 | 🟩 较完整 | 🟨 部分实现源码可得 | 当前可拿到 [utap](https://github.com/UPPAALModelChecker/utap) / [UDBM](https://github.com/UPPAALModelChecker/UDBM) 等子库源码，但 dynamic extrapolation 主实现未公开 | [jensen23-dynamic-extrapolation-extended-timed-automata](./jensen23-dynamic-extrapolation-extended-timed-automata/) |
| ⚡ | `brorholt25-coshy` | Uppaal Coshy: Automatic Synthesis of Compact Shields for Hybrid Systems | 2025 | hybrid safety 需要自动 compact shields | automatic synthesis of compact shields | 把 `UPPAAL` 扩到 `Coshy` shielding | 🟨 中等 | 🟧 仅可执行/可使用版本可得 | 官方 [features](https://uppaal.org/features/) 与 [changelog](https://uppaal.org/changelog/) 已出现 `COSHY` 线索，但当前未见对应源码仓库公开 | [brorholt25-uppaal-coshy](./brorholt25-uppaal-coshy/) |

## 与应用文库的关系

当前 `UPPAAL` 应用与案例条目不再在本技术总账中占位，而是统一迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md) 单独维护。

分流原则如下：

1. 若主贡献是 `UPPAAL` 本体的新能力、新抽象、新算法、新工程组件，保留在本文件。
2. 若主贡献是利用 `UPPAAL` 验证具体系统、协议、控制器或工业对象，转入应用文库。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化原始 `open_explore/uppaal/`（现 `open_explore/uppaal_tech/`），新增 **11** 篇基础条目，并建立 `README.md`、`GUIDE.md`、`SUMMARY.md` 三个论文集核心文件；随后补入 `behrmann03` 与 `bengtsson02` 的 `paper-*` 子目录及父子导航 README | 只从既有 `UPPAAL/UDBM` 历史论文池挑选一份可用副本，优先完成基础入库，不额外扩新论文；有现成 `content.md` 的直接规范为 `paper_content.txt`，缺失 thesis 级正文的条目用 `tools/pdf_extractor.py` 补齐；对 thesis 型条目把原有拆分子论文与 `content_assets/` 一并带入 | 先搭建 `UPPAAL` 基础文库骨架，再补齐带内嵌子论文条目的父子导航结构，为后续沿专题继续深挖做准备 |
| 2026-03-29 | 重构 `README.md`、`GUIDE.md`、`SUMMARY.md` 的文库口径，新增官方入口索引、作者主线与双维材料状态体系 | 不再以“文件齐不齐”作为主状态，而是改成“内容详细程度 + 实现可获取程度”；同时把 `🧱 / ⚡ / 🛠️` 合并进统一论文表 | 为后续沿官方 org、官方 docs、核心作者和技术分支系统扩库做准备 |
| 2026-03-29 | 补充作者年代观察与近年活动判断，并把“实现可获取程度”重定义为严格的源码标准 | 把“当前文库作者”与“较新年份的直接 `UPPAAL` 工作”显式关联，同时把二进制下载与源码实现彻底分开 | 为后续优先补 `2010s/2020s` 的 `SMC / Stratego / Tiga / 现代工具链` 缺口做准备 |
| 2026-03-29 | 新增 **12** 篇 `2001-2015` 的核心技术/扩展条目，补齐 `cost-optimality / architecture / Tiga / SMC / Stratego` 主链 | 只收录 PDF 实际下载成功且已生成 `paper_content.txt` 的条目；本轮继续后置应用类，优先围绕核心作者和技术分支做全网补链 | 把文库直接覆盖范围从 `1990-2006` 扩展到 `1990-2015`，让 `UPPAAL` 演进脉络初步成形 |
| 2026-03-29 | 调整作者画像与论文清单维护口径，补充“角色判断 / 主要贡献方向”，并把统一论文表改为按年份升序维护 | 作者分析继续以现有已收录论文为主证据，不以 team 页替代；统一论文表按年份升序、同年按 `Key` 稳定排序 | 让后续扩库同时具备“技术时间线”和“人物贡献线”两条可直接复用的导航 |
| 2026-03-29 | 新增 **11** 篇 `2010-2025` 的核心技术/扩展条目，补入 `timed I/O automata / ECDAR / randomized analysis / MCTS / dynamic extrapolation / Coshy` 主线 | 只把 `PDF` 实际下载成功且已生成 `paper_content.txt` 的条目正式入账；实现可获取程度同步按“源码优先、二进制降级”重判，并把 `ECDAR` 相关开源入口写回官方索引 | 把文库直接覆盖范围从 `1990-2015` 延展到 `1990-2025`，让 `UPPAAL` 的近年演进不再断在 `Stratego` 之前 |
| 2026-03-29 | 新增 **11** 篇 `2001-2019` 的核心技术/扩展条目，补入 `UPPAAL now-next-future / guided synthesis / unification & sharing / TRON online testing / stochastic hybrid systems / compact strategies` 主线，并把 `README.md`、`GUIDE.md`、`SUMMARY.md` 全部回填到 **45** 篇口径 | 只把 `PDF` 实际下载成功且已生成 `paper_content.txt` 的条目正式入账；其中 `amnell01`、`hune01`、`mikucionis10` 三篇早期 PDF 的 `text` 抽取质量不足，当前先用 `pdftotext -layout` 回填正文，后续若要做深度抽取再在具备 `tesseract` 的环境重跑 `ocr` | 把 `guided synthesis -> TRON/testing -> SHS -> compact strategies` 这条链补齐，并同步修正作者主线、关键词簇、分类统计与统一总表 |
| 2026-03-29 | 把原 `uppaal/` 文库重命名为 `uppaal_tech/`，并新增同级 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)；同时把本总账的“技术演进线”整理成阶段表 | 不新增论文，只做文库拆分、入口重定向、边界收紧和总账结构重构；应用条目后续统一转入 `uppaal_apps/` | 让 `UPPAAL` 本体技术与应用案例彻底分流，并把技术时间线固定为可持续维护的表格 |
| 2026-03-29 | 新增 [DESC_GUIDE.md](./DESC_GUIDE.md)，并把统一论文表改造成 `问题简述 / 方法简述 / 解决点简述` 三列口径 | 这一轮不补单篇 `desc.md`，只先把单篇写作规范与总账压缩字段对齐，同时要求后续单篇分析优先把“立足问题 / 核心方法 / 解决点”讲清楚 | 让后续单篇 `desc.md` 与总账形成同一套问题-方法-解决点语言，避免只留模糊摘要式记录 |
| 2026-03-29 | 为 [ad90-timed-automata](./ad90-timed-automata/) 首次补写 `desc.md`，并同步强化 [DESC_GUIDE.md](./DESC_GUIDE.md) 对“方法展开层次”的要求 | 单篇分析严格按 [DESC_GUIDE.md](./DESC_GUIDE.md) 组织，重点补清 dense-time 建模动机、timed automata 运行语义、region 抽象、不可判定性证明思路与 `DTMA` 规格子类的作用；同时把 `DESC_GUIDE` 明确升级为要求写出对象 / 规则 / 过程 / 差异层 | 先拿最早条目验证更细的 `desc.md` 模板是否真的能把“问题 / 方法 / 解决点”讲透，再决定后续批量铺开 |
| 2026-03-29 | 为仓库级 [AGENTS.md](../../AGENTS.md) / `CLAUDE.md` 补充 GitHub 友好的数学公式写法规范，并把 [DESC_GUIDE.md](./DESC_GUIDE.md) 与 [ad90-timed-automata/desc.md](./ad90-timed-automata/desc.md) 改成 `$...$ / $$...$$` 口径 | 明确规定行内公式用 `$...$`，展示公式必须写成“`$$` + 恰好一行公式体 + `$$`”，避免多行块公式导致 GitHub 渲染异常；同时把 `ad90` 中关键定义、构造和判定问题改写为单行公式块 | 让后续 `desc.md` 在保留形式化精度的同时，仍能稳定在 GitHub 上直接渲染和阅读 |

## 失败与阻塞记录

| Key | 标题 | 状态 | 原因 | 后续建议 |
|---|---|---|---|---|
| `rokicki93` | Representing and Modeling Digital Circuits | 本轮未纳入 | 当前未取得合法可用全文 PDF，且与 `UPPAAL` 论文集的直接关系更偏 DBM 历史引用背景，暂不作为正式条目入库 | 若后续找到合法全文且能明确其在 `UPPAAL/DBM` 技术链中的稳定价值，再单独复核是否纳入 |
| `importance-splitting-line` | `UPPAAL SMC` 的 importance splitting / importance sampling 候选条目 | 待补证 | 已定位到论文线索，但暂未取得稳定可下载 PDF，因此未正式入账 | 下轮优先从 `Kim Guldstrand Larsen / Marius Mikucionis / Axel Legay + importance splitting` 继续检索 |
| `ocr-runtime` | `OCR` 提取运行时依赖 | 环境阻塞 | 当前环境缺少系统级 `tesseract`，因此 `amnell01`、`hune01`、`mikucionis10` 暂用 `pdftotext -layout` 回填 `paper_content.txt` | 后续若进入单篇深读且文本质量仍不足，应在具备 `tesseract` 的环境重新用 `tools/pdf_extractor.py -m ocr` 抽取 |
