# `uppaal_tech/` 论文集 README

## 1. 论文集定位

`open_explore/uppaal_tech/` 是一个面向 `UPPAAL` 谱系的理论与技术专题论文集，用于系统沉淀 `UPPAAL` 相关的核心理论、关键算法与数据结构、能力扩展，以及工具工程能力演进。

它当前位于 [open_explore/](../README.md) 下，而不是直接放入某个 `project_*`，原因是这类材料既服务博士研究中的形式化验证与状态机方向，也包含一部分尚未完全确定最终归属的基础技术脉络。

基于 `UPPAAL` 的具体软件/系统/协议应用工作，现已拆分到同级文库 [uppaal_apps/README.md](../uppaal_apps/README.md) 中单独维护，不再与本技术文库混放。

## 2. 设立宗旨与期望收获

单独建立本论文集，目标是先形成一个可持续扩张的 `UPPAAL` 理论与技术基础文库，而不是零散保存几篇经典论文。这里期望持续沉淀的内容主要包括三类：

1. `UPPAAL` 核心算法/数据结构相关工作。
2. `UPPAAL` 改进与扩展相关工作。
3. `UPPAAL` 工程实现、工具链、教程与建模实践相关工作。

对后续博士研究而言，这个论文集主要服务三类需求：

1. 理解 `UPPAAL` 及其底层 timed automata / zone / DBM 技术脉络。
2. 为后续验证方法、验证剖面和工具链构思提供可靠背景材料。
3. 为后续再向 [uppaal_apps/README.md](../uppaal_apps/README.md) 扩展应用文库时提供稳定的技术主线与人物主线坐标。

## 3. 收录范围

本论文集优先收录以下论文：

1. 由 `UPPAAL` 核心作者、官方团队或紧密相关学术脉络产出的关键工作。
2. 直接解释 `UPPAAL` 核心语义、DBM/zone/federation 等关键数据结构、验证算法或符号状态表示的论文。
3. 直接提出 `UPPAAL` 相关能力扩展、状态空间优化、抽象改进、扩展语义或新分析能力的论文。
4. 直接面向 `UPPAAL` 建模语言、查询语言、工具架构、用户教程、建模模式或工程实践的论文。

本论文集原则上不应作为重点收录以下论文：

1. 只和一般 timed automata 有关，但和 `UPPAAL` 谱系没有稳定联系的普通背景论文。
2. 只在参考文献中顺带提到 `UPPAAL`，但正文没有形成实质性 `UPPAAL` 技术或应用贡献的论文。
3. 主要贡献落在具体系统/协议/工业案例验证上的应用论文，这类条目应转入 [uppaal_apps/README.md](../uppaal_apps/README.md)。
4. 纯安装教程、零散博客、重复镜像、课程作业或无正式贡献说明的材料。
5. 对 `UPPAAL` 只有极远的历史背景意义、但缺少明确可追溯关联且无法稳定支撑后续工作的条目。

## 4. 纳入与排除判定标准

后续筛选时，至少从以下维度判断：

1. 研究对象
   - 纳入：`UPPAAL` 本体、其关键理论基础、核心引擎技术、扩展分支和工具工程路线。
   - 排除：和 `UPPAAL` 仅弱相关的泛 timed automata、泛模型检查或泛形式化方法论文，以及以应用案例为主的条目。
2. 任务类型
   - 纳入：能够支撑核心算法理解、工具能力演进理解或技术时间线整理的论文。
   - 排除：只是宽泛背景介绍，无法沉淀为稳定文库条目的论文。
3. 证据形态
   - 纳入：正文中能明确看到 `UPPAAL` 相关技术、工具、方法或工程贡献。
   - 降优先级：只有部分章节与 `UPPAAL` 有关，但仍值得留作补充背景。
4. 可提取性
   - 纳入：可获得 PDF 原文，并能生成质量可用的 `paper_content.txt`。
   - 排除：无法获取合法可用 PDF，或提取后仍不足以支持可靠整理。
5. 与本研究相关性
   - 纳入：能直接服务博士研究中的状态机建模、形式化验证、验证工具或技术脉络积累。
   - 降优先级：仅提供一般背景，不能直接沉淀出后续可用知识点。

### 4.1 与同级应用文库的关系

当前 `UPPAAL` 相关材料按“技术本体”和“应用案例”两条线分开维护：

1. [uppaal_tech/README.md](./README.md)
   - 只收录 `UPPAAL` 本体技术，包括 `🧱` 核心算法/数据结构、`⚡` 改进与扩展、`🛠️` 工程/工具链。
2. [uppaal_apps/README.md](../uppaal_apps/README.md)
   - 只收录基于 `UPPAAL` 的具体系统、协议、软件和工业应用。

如果一篇论文同时包含技术方法和案例验证，默认按主要贡献中心放置：

1. 若主贡献是 `UPPAAL` 本身的新能力、新算法、新数据结构或新工程组件，归入本技术文库。
2. 若主贡献是利用 `UPPAAL` 去验证某个系统、协议、控制器或工业场景，归入应用文库，并在需要时在两边互相交叉引用。

## 5. 官方入口索引

以下链接已按 `2026-03-30` 核对，后续整理 `UPPAAL` 理论与技术文库时应优先从这些官方入口反向追踪资料、源码、教程和案例。

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
12. 官方 `SMC` tutorial：<https://uppaal.org/texts/uppaal-smc-tutorial.pdf>
13. 官方 `TRON` manual：<https://uppaal.org/texts/tron-manual.pdf>
14. `TRON` 功能页：<https://uppaal.org/features/#tron>

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

谱系相关扩展入口：

这部分不属于 `UPPAALModelChecker` 官方 org，但对 `timed I/O automata / ECDAR` 线的源码核验和后续扩库很重要，应与官网入口一起维护。

1. `ECDAR` 主页：<https://www.ecdar.net/>
2. `ECDAR` GitHub org：<https://github.com/Ecdar>
3. `ECDAR` 主仓库：<https://github.com/Ecdar/ECDAR>
4. `j-Ecdar`：<https://github.com/Ecdar/j-Ecdar>
5. `Reveaal`：<https://github.com/Ecdar/Reveaal>
6. `Ecdar-GUI`：<https://github.com/Ecdar/Ecdar-GUI>
7. `Ecdar-test`：<https://github.com/Ecdar/Ecdar-test>

## 6. 现有收录论文的作者关联主线

人物检索簇的起点不是官网 team 页面，而是当前文库 **70 个已收录顶层条目** 的 `bibtex.bib` 作者统计。官方 team / org 只用于交叉核验源码、案例和工具入口，不直接决定“核心人员”名单。

### 6.1 当前已形成稳定主线的作者

这里的“角色判断”不是按官网头衔写的，而是根据当前 `70` 个顶层条目里作者跨越了哪些技术分支、是否出现在关键转折论文上、以及是否贯穿多个年代综合判断出来的。

| 作者 | 当前收录篇数 | 角色判断 | 主要贡献方向 | 代表关联条目 | 后续优先扩张方向 |
|---|---:|---|---|---|---|
| [Kim Guldstrand Larsen](https://kgl.cs.aau.dk/) | 56 | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / priced games / Tiga / SMC / TRON / ECDAR / modern abstractions` | `lpw95`、`bouyer04`、`behrmann07`、`bogomolov15`、`lecoent19-tiga`、`jensen25` | `UPPAAL + importance splitting/UPPAAL 5/TATL/Coshy/GPU-SMC` |
| [Alexandre David](https://homes.cs.aau.dk/~adavid/) | 27 | 中后期扩展主线整合者 | `architecture / game-based testing / ECDAR / SMC / strategy evaluation / TIOA / SHS` | `behrmann02`、`david08`、`david10-*`、`bulychev12-smc`、`david14-*`、`david15-*` | `Alexandre David + UPPAAL + SMC/ECDAR/game/testing` |
| [Axel Legay](https://www.uclouvain.be/en/people/axel.legay) | 16 | `SMC + specification theory` 桥接作者 | `statistical model checking / priced models / timed I/O specification / optimization / SHS / distributed SMC / co-simulation` | `david10-*`、`bulychev11`、`bulychev12-smc`、`david11-*`、`nyman17-fmu`、`goorden23` | `Axel Legay + UPPAAL + statistical/specification theory` |
| [Gerd Behrmann](https://dblp.org/pid/39/5834) | 13 | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / symmetry-aware engine / CORA / UPPAAL 4.0 / evolution survey` | `amnell01`、`behrmann02-*`、`behrmann03`、`behrmann05`、`behrmann06`、`behrmann11` | `Gerd Behrmann + UPPAAL + architecture/CORA/engine/history` |
| [Marius Mikučionis](https://people.cs.aau.dk/~marius/cv.html) / [Marius Mikucionis](https://people.cs.aau.dk/~marius/cv.html) | 15 | `TRON -> SMC -> POR/GPU -> Coshy` 纵向桥接作者 | `online testing / statistical model checking / co-simulation / urgent POR / GPU-SMC / strategy synthesis / hybrid shielding` | `larsen04-*`、`bogomolov15`、`lecoent19-tiga`、`muniz20`、`muniz24`、`brorholt25` | `Marius Mikučionis + UPPAAL + TRON/SMC/POR/GPU/Coshy` |
| [Paul Pettersson](https://www.es.mdu.se/staff/166-Paul_Pettersson) | 13 | `DBM / engine / component-modeling / testing` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities / PORT / TRON / testing` | `lpw95`、`llpy97`、`hessel04`、`hakansson08`、`hessel08`、`dhlp06` | `Paul Pettersson + UPPAAL + DBM/PORT/testing` |
| [Ulrik Nyman](https://vbn.aau.dk/en/persons/ulrik-nyman) | 13 | `ECDAR / timed-spec / testing / randomized analysis` 主线组织者 | `timed I/O automata / Büchi timed specifications / mutation-based testing / fault localisation / compositional verification / randomized analysis / planning / co-simulation` | `david10-*`、`nyman10`、`nyman17`、`nyman17-fmu`、`gundersen18`、`jensen22` | `Ulrik Nyman + UPPAAL + ECDAR/testing/randomized` |
| [Wang Yi](https://user.it.uu.se/~wangyi/) | 10 | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations / DBM` | `lpw95`、`llpy97`、`amnell01`、`by04`、`behrmann02`、`behrmann06` | `Wang Yi + UPPAAL + semantics/engine/history` |
| [Andrzej Wąsowski](https://www.itu.dk/~wasowski/) | 8 | `ECDAR` 规范理论与新近扩展连接者 | `timed I/O specification / quotient / compositional verification / liveness contracts / Coshy 协作线` | `david10-*`、`nyman10`、`david12-ecdar`、`david13`、`goorden23`、`brorholt25` | `Andrzej Wąsowski + UPPAAL + ECDAR/Coshy` |
| [Peter Gjøl Jensen](https://vbn.aau.dk/en/persons/pgj/) | 7 | `optimization -> co-simulation / WCET -> abstraction / GPU-SMC -> hybrid synthesis` 桥接作者 | `expected cost / FMI-FMU co-simulation / WCET / dynamic extrapolation / GPU-SMC / compact shields` | `david14`、`bogomolov15`、`cassez17`、`nyman17-fmu`、`jensen23`、`muniz24` | `Peter Gjøl Jensen + UPPAAL + abstraction/GPU/Coshy` |

### 6.2 当前已出现但仍属补充线索的作者

| 作者 / 别名 | 当前关联条目 | 角色判断 | 主要贡献方向 | 检索使用方式 |
|---|---|---|---|---|
| [Brian Nielsen](https://homes.cs.aau.dk/~bnielsen/) | `hessel04`、`larsen04-*`、`david08`、`hessel08`、`nyman17` | `TRON / adaptive testing / mutation testing` 分支关键协作者 | `model-based testing / timed trace inclusion / relativized ioco / game-based testing / mutation-based testing` | 与 `UPPAAL + TRON/online testing/game-based testing/mutation-based testing` 联用 |
| [Arne Skou](https://homes.cs.aau.dk/~ask/) | `hessel04`、`hessel08`、`david12-ecdar` | `testing / conformance / compositional verification` 分支关键协作者 | `real-time testing / conformance / compositional verification / ECDAR` | 与 `UPPAAL + testing/conformance/compositional verification` 联用 |
| [Anders Hessel](https://hessel.tech/) | `hessel04`、`hessel08` | `time-optimal / survey-style testing` 分支作者 | `offline test generation / time-optimal testing / testing survey` | 与 `UPPAAL + time-optimal testing/test-case generation` 联用 |
| [Marco Muñiz](https://homes.cs.aau.dk/~muniz/) | `muniz12`、`muniz20`、`muniz24` | `结构感知压缩 -> urgent POR -> GPU-SMC` 分支作者 | `disjoint activity / urgent partial order reduction / GPU-SMC` | 与 `UPPAAL + disjoint activity/partial order reduction/GPU-SMC` 联用 |
| [Uli Fahrenberg](https://dblp.org/pid/89/5538) | `fahrenberg09` | infinite-run priced optimization 分支作者 | `discount-optimality / infinite runs / corner-point abstraction` | 与 `UPPAAL + priced timed automata/discount-optimal infinite runs` 联用 |
| [John Håkansson](https://dblp.org/pid/09/6977) / [Jan Carlson](https://www.es.mdu.se/staff/40-Jan_Carlson) | `hakansson08` | `UPPAAL PORT / component-based design` 分支作者 | `component-based design / local time / PORT / SaveCCM` | 与 `UPPAAL PORT/component-based/local time/SaveCCM` 联用 |
| [Martijn Hendriks](https://dblp.org/pid/h/MartijnHendriks) / [Peter Niebert](https://dblp.org/pid/n/PeterNiebert) / [Frits Vaandrager](https://fvaan.nl/) | `hendriks04` | `symmetry reduction` 分支关键作者 | `scalarset / state swaps / canonical representative / symmetry reduction` | 与 `UPPAAL + symmetry reduction/scalarset/canonical representative` 联用 |
| [Thomas Hune](https://dblp.org/search/author?q=Thomas%20Hune) | `amnell01`、`hune01` | 早期 `guided synthesis` 线作者 | `guided synthesis / control programs / early tool planning` | 与 `UPPAAL + guided synthesis/control` 联用 |
| [Sean Sedwards](https://dblp.org/pid/26/5698) | `david12-shs` | `SHS / SMC` 分支补强作者 | `stochastic hybrid systems / simulation semantics / statistical analysis` | 与 `UPPAAL + stochastic hybrid systems/SMC` 联用 |
| [Danny Bøgsted Poulsen](https://vbn.aau.dk/en/persons/dannybpoulsen/) | `bulychev12-smc`、`david11-*`、`david12-shs`、`david15-smc-tutorial` | `UPPAAL-SMC` 工程化与教程化高频协作者 | `statistical model checking / stochastic semantics / distributed SMC / tutorialization` | 与 `UPPAAL + SMC/stochastic semantics/distributed/tutorial` 联用 |
| [Peter Bulychev](https://dblp.org/search/author?q=Peter%20Bulychev) | `bulychev11`、`bulychev12-*` | 早期 `UPPAAL-SMC` 核心扩展作者 | `distributed parametric SMC / priced timed automata / early SMC implementation` | 与 `UPPAAL + distributed statistical model checking/priced timed automata` 联用 |
| [Zheng Wang](https://www.hipeac.net/~wangzheng/) | `bulychev12-smc`、`david11-*` | `UPPAAL-SMC` 性能与语义补强作者 | `stochastic semantics / priced timed automata / performance-oriented SMC` | 与 `UPPAAL + stochastic semantics/priced timed automata/SMC` 联用 |
| [Pranav Ashok](https://dblp.org/pid/200/8227) / [Jan Křetínský](https://www7.in.tum.de/~kretinsk/) / [Adrien Le Coënt](https://dblp.org/pid/172/2815) / [Jakob Haahr Taankvist](https://dblp.org/search/author?q=Jakob%20Haahr%20Taankvist) / [Maximilian Weininger](https://dblp.org/search/author?q=Maximilian%20Weininger) | `ashok19-sos`、`lecoent19-tiga` | `compact strategies / continuous control synthesis` 分支作者群 | `safe-optimal-small strategies / stochastic hybrid games / hybrid MDP / guaranteed control synthesis` | 与 `UPPAAL + SOS/compact strategies/stochastic hybrid games/continuous systems/Tiga` 联用 |
| [Andrej Kiviriga](https://dblp.org/search/author?q=Andrej%20Kiviriga) | `kiviriga20`、`kiviriga21`、`jensen22` | `randomized analysis / planning` 新近主线作者 | `randomized refinement / randomized reachability / MCTS` | 与 `UPPAAL + randomized reachability/refinement/MCTS` 联用 |
| [Nicolaj Ø. Jensen](https://vbn.aau.dk/en/persons/noje/) | `jensen23`、`jensen25` | `modern XTA abstraction -> timed ATL` 新近作者 | `dynamic extrapolation / extended timed automata / TATL / EADG / abstractions` | 与 `UPPAAL + dynamic extrapolation/TATL/EADG` 联用 |
| [Martijn A. Goorden](https://dblp.org/search/author?q=Martijn%20A.%20Goorden) | `goorden23` | `TIOA` 规范理论补完作者 | `complete specification theory / ECDAR` | 与 `UPPAAL + timed I/O automata/specification theory` 联用 |
| [Asger Horn Brorholt](https://vbn.aau.dk/en/persons/asgerhb/) | `brorholt25` | `Coshy` 新近作者 | `automatic shield synthesis / hybrid systems / compact shields` | 与 `UPPAAL + Coshy/hybrid shield synthesis` 联用 |
| [Franck Cassez](https://franck44.github.io/publications/) | `bouyer04`、`cassez05`、`cassez17` | `priced timed games -> WCET` 分支作者 | `priced timed games / timed games / WCET / binary-program analysis` | 与 `UPPAAL + timed games/priced timed games/WCET` 联用 |
| [Didier Lime](https://dblp.org/pid/94/6720) | `cassez05`、`behrmann07`、`david14`、`jensen25` | `timed games -> Tiga -> optimization -> TATL` 分支协作者 | `timed games / controller synthesis / cost analysis / timed ATL` | 与 `UPPAAL + timed games/Tiga/TATL` 联用 |
| [Emmanuel Fleury](https://dblp.org/search/author?q=Emmanuel%20Fleury) | `bouyer04`、`cassez05`、`behrmann07` | `priced timed games -> Tiga` 分支协作者 | `priced timed games / timed games / controller synthesis` | 与 `UPPAAL + timed games/priced timed games/controller synthesis` 联用 |
| [Florian Lorber](https://dblp.org/pid/117/5464.html) / [Christian Ovesen](https://dblp.org/search/author?q=Christian%20Ovesen) / [E. J. Njor](https://people.compute.dtu.dk/emjn/) | `gundersen18`、`njor20` | `ECDAR -> UPPAAL-native conformance testing` 工程分支作者群 | `fault localisation / conformance testing / diabolic completion / Yggdrasil` | 与 `UPPAAL + conformance testing/Ecdar/diabolic completion/Yggdrasil` 联用 |
| [Johan Bengtsson](https://dblp.org/search/author?q=Johan%20Bengtsson) | `bengtsson02`、`behrmann02-secrets`、`by04` | `DBM` 数据结构专题化奠基作者 | `clocks / DBMs / states / DBM internals / implementation detail` | 与 `UPPAAL + DBM/implementation` 联用 |
| [Patricia Bouyer](https://www.lmf.cnrs.fr/Annuaire/Patricia.Bouyer/) / [Radek Pelánek](https://www.fi.muni.cz/~xpelanek/) | `bblp04`、`bouyer04` | zone abstraction 与 priced timed games 外推分支关键合作者 | `lower-upper bound extrapolation / zone abstraction / priced timed games` | 与 `UPPAAL + abstraction/priced timed games/extrapolation` 联用 |
| [Rajeev Alur](https://www.cis.upenn.edu/~alur/) | `ad90` | 理论前史奠基者 | `timed automata semantics` | 只在明确追踪 `UPPAAL` 理论源头时纳入检索 |
| [David Dill](https://theory.stanford.edu/~dill/) / [David L. Dill](https://theory.stanford.edu/~dill/) | `ad90`、`dill89` | dense-time verification 前史奠基者 | `timing assumptions / clock constraints / symbolic verification` | 只在明确追踪 `UPPAAL` 技术前史时纳入检索 |

后续检索时，默认先从这条“文库内部作者主线”出发，再用官方 team 与 org 做补充，而不是反过来。新的 team 成员或官方贡献者，只有在已收录或待收录论文中形成稳定作者链后，才提升为“核心人员”。

默认检索写法是“作者名 + UPPAAL + 分支词”，例如：

1. `Kim Guldstrand Larsen + UPPAAL + importance splitting`
2. `Marius Mikucionis + UPPAAL + TRON/online testing`
3. `Ulrik Nyman + UPPAAL + ECDAR/randomized reachability`
4. `Axel Legay + UPPAAL + statistical model checking/specification theory`
5. `Pranav Ashok + Kim Guldstrand Larsen + UPPAAL + compact strategies`

### 6.3 作者年代与持续性观察

当前文库里的正式顶层条目现在已经覆盖 `1990-2025`。这一轮新增后，文库已经不再只是 `cost-optimality -> architecture -> Tiga -> SMC -> Stratego -> modern extensions` 这条单线，而是把 `time-optimal testing / priced timed games / CORA scheduling / game-based adaptive testing / discount-optimal infinite runs / UPPAAL-SMC formalization / strategy evaluation / ECDAR fault localisation / UPPAAL-native conformance testing / TATL + EADG + abstraction` 这些此前断开的分支也接了进来。按 `2026-03-30` 对官方站点、官方 GitHub org、`ECDAR` 站点与公开论文线的核验结果，至少可以确认：

1. 官方 changelog 仍记录到 `2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5` 和 `2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
2. 官方 GitHub org 中 `UDBM`、`docs.uppaal.org`、`utap`、`uppaal-libs` 等仓库在 `2025-2026` 仍有更新。
3. 当前文库已经直接覆盖到 `2025` 的 `Uppaal Coshy`、`GPU-SMC` 与 `TATL` 新算法；并且 `2015-2019` 已补入 `FMI-FMU co-simulation / WUPPAAL WCET / guaranteed continuous-system synthesis / multi-weighted logics`，但 `2016` 与 `2018` 的理论/统计现代化层仍偏空，`importance splitting`、更系统的 `UPPAAL 5` 技术论文、若干现代搜索/抽象优化线仍未补齐。

因此，后续维护时不能再把现有作者简单看成“早期史料作者名单”，而要区分：

1. 当前文库里已经覆盖到 `2010s/2020s` 的持续主线作者。
2. 当前文库里主要还是早期 / 中期，但对理解技术底盘仍不可替代的作者。
3. 只在单一分支上起到“关键断点补链”作用的作者。

下表中的“继续沿该作者线扩张概率”是**检索价值推断**，表示继续追这个作者线能否大概率找到 `2007+ / 2010s / 2020s` 的后续 `UPPAAL` 工作，不是对作者个人职业状态的断言。

| 作者 | 角色判断 | 主要贡献方向 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 相关年份 | 最近性判断 | 继续沿该作者线扩张概率 | 备注 |
|---|---|---|---|---|---|---|---|
| [Kim Guldstrand Larsen](https://kgl.cs.aau.dk/) | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / Tiga / SMC / Stratego / TRON / symmetry reduction / ECDAR / modern extensions` | `1995-2025` | `2025` | 🟢 早期到近年全程贯穿 | 🟢 高 | 当前最强主线检索入口，继续补 `importance splitting / UPPAAL 5 / Coshy / GPU-SMC` 时仍应优先追他 |
| [Alexandre David](https://homes.cs.aau.dk/~adavid/) | 中后期扩展主线整合者 | `architecture / Tiga / SMC / expected cost / Stratego / TIOA / SHS` | `2001-2015` | `2015` | 🟨 文库内高频但近年直接条目暂止于 `2015` | 🟢 高 | 虽然近年不再直接高频出现，但多个后续分支仍沿着其方法线展开 |
| [Ulrik Nyman](https://vbn.aau.dk/en/persons/ulrik-nyman) | `ECDAR / timed-spec / testing / randomized analysis` 主线组织者 | `specification theory / refinement / mutation-based testing / compositional verification / randomized analysis / planning` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接论文 | 🟢 高 | 继续追 `ECDAR -> Büchi/liveness -> testing -> randomized -> planning` 时优先级很高 |
| [Axel Legay](https://www.uclouvain.be/en/people/axel.legay) | `SMC + specification theory` 桥接作者 | `statistical model checking / priced models / timed I/O specification / optimization / SHS` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接延展 | 🟢 高 | 是把 `SMC` 线与 `ECDAR/TIOA` 线接起来的关键人物 |
| [Andrzej Wąsowski](https://www.itu.dk/~wasowski/) | `ECDAR` 规范理论与新近扩展连接者 | `timed I/O specification / quotient / compositional verification / Coshy 协作线` | `2010-2025` | `2025` | 🟢 近年仍有直接条目 | 🟢 高 | 文库已证明他不是一次性协作者，而是贯穿 `ECDAR -> Coshy` 的稳定作者 |
| [Peter Gjøl Jensen](https://vbn.aau.dk/en/persons/pgj/) | `optimization -> abstraction / GPU-SMC -> hybrid synthesis` 桥接作者 | `expected cost / dynamic extrapolation / GPU-SMC / compact shields` | `2014-2025` | `2025` | 🟢 近年仍有连续新作 | 🟢 高 | 当前很适合继续追 `abstraction / GPU / shield synthesis` 线 |
| [Marius Mikučionis](https://people.cs.aau.dk/~marius/cv.html) | `TRON -> SMC -> POR/GPU -> Coshy` 纵向桥接作者 | `online testing / statistical model checking / urgent POR / GPU-SMC / strategy synthesis / hybrid shielding` | `2004-2025` | `2025` | 🟢 横跨早期测试线和近年扩展线 | 🟢 高 | 如果想摸清 `UPPAAL` 从 testing 到 modern stochastic/hybrid 的演进，这个人必须持续追 |
| [Gerd Behrmann](https://dblp.org/pid/39/5834) | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / UPPAAL 4.0 / evolution survey` | `2001-2011` | `2011` | 🟨 中期工程主线已较完整 | 🟨 中等 | 更适合补历史骨架，不一定再带来很多 `2020s` 新条目 |
| [Paul Pettersson](https://www.es.mdu.se/staff/166-Paul_Pettersson) | `DBM / engine / component-modeling / testing` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities / PORT / TRON` | `1995-2011` | `2011` | 🟨 更偏历史骨干作者 | 🟨 中等 | 对 `DBM / federation / PORT / testing` 补链仍有价值 |
| [Wang Yi](https://user.it.uu.se/~wangyi/) | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations / DBM` | `1995-2011` | `2011` | 🟨 早期到中期主线较完整 | 🟨 中等 | 主要用于巩固 `UPPAAL` 理论底盘 |

对当前文库中更偏分支性的作者，还应额外注意：

1. `Brian Nielsen`：当前文库覆盖 `2004-2017`，集中在 `TRON / online testing / mutation-based testing / relativized ioco`；更像 testing 分支的关键作者，而不是全局总主线作者，但继续补 testing 线时价值很高。
2. `Thomas Hune`：当前文库覆盖 `2001`，主要出现在 `guided synthesis` 和早期路线综述里；更适合补早期控制合成和工具规划脉络。
3. `Sean Sedwards`：当前文库只直接覆盖 `2012`，但刚好卡在 `stochastic hybrid systems` 这条关键过渡线上；属于“分支窄但关键”的作者。
4. `Marco Muñiz`：当前文库直接覆盖 `2012-2025`，正好串起 `disjoint activity -> urgent POR -> GPU-SMC` 这条结构感知性能线，是近年值得继续追的明确分支作者。
5. `John Håkansson / Jan Carlson`：当前文库只直接覆盖 `2008` 的 `UPPAAL PORT`，但这条组件建模与 local-time 线非常特别，适合后续定点补 component-based design 分支。
6. `Pranav Ashok / Jan Křetínský / Adrien Le Coënt / Jakob Haahr Taankvist / Maximilian Weininger`：当前文库在 `2019` 已同时覆盖 `SOS` 与 `continuous-system Tiga` 两个紧邻节点，适合继续沿 `compact strategies / stochastic hybrid games / guaranteed control synthesis` 追后续工作。

这个判断对后续扩库的直接含义是：

1. 当前文库已经不再只停留在 `1990-2015`，而是形成了到 `2025` 的连续技术脉络。
2. 下一轮优先缺口应从“泛泛补 `2010s/2020s`”切换为“定点补 `2016` 与 `2018` 仍偏空的理论/统计现代化层，尤其是 `importance splitting`、更现代的搜索/抽象优化与 `UPPAAL 5` 相关论文”。
3. 作者关键词簇维护时，应同时记录“作者名 + 角色判断 + 主要贡献方向 + 年代窗口”，而不是只留一串人名。

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
4. [DESC_GUIDE.md](./DESC_GUIDE.md)
   - 单篇 `desc.md` 的专项规范。
   - 固定“问题 / 方法 / 解决点”三条主线的写法，并要求 `desc.md` 开头先给出三条一句话简述。

AI 在开始具体工作前，推荐阅读顺序为：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. 若任务是生成或重写单篇 `desc.md`，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)
5. 若目标条目是 thesis/合集型父路径，先读该目录自己的 `README.md`
6. 目标论文目录下的 `bibtex.bib`
7. 目标论文目录下的 `paper_content.txt`
8. 需要深入具体拆分主题时，再进入对应 `paper-*` 子目录的 `README.md` 与 `paper_content.txt`
9. 必要时核对 `paper.pdf`

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
5. 当前 **70** 个顶层条目已经全部补齐首轮 `desc.md`。后续新增顶层条目时，默认应在同一轮内同步补齐 `desc.md`；对 `paper-*` 子目录则继续以父目录 `README.md` 与父级 `desc.md` 为主，只有在该子论文要升级为独立正式条目时，才单独补 `bibtex.bib` 并单独写自己的 `desc.md`。

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

1. 先读 [README.md](./README.md)，理解 `UPPAAL` 理论与技术文库的边界、官方入口、作者主线和状态口径。
2. 再读 [GUIDE.md](./GUIDE.md)，确认本轮工作流程、检索规则和回填规范。
3. 再看 [SUMMARY.md](./SUMMARY.md)，掌握当前已有积累、作者分布、分类缺口和失败历史。
4. 如果任务是生成或重写单篇 `desc.md`，先读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
5. 如果目标目录是带内嵌子论文的父路径，先读该目录自己的 `README.md`，确认 thesis 与 `paper-*` 子目录的关系。
6. 然后再按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时）` 的顺序工作。
7. 只有在需要深入某个拆分主题时，才进入对应 `paper-*` 子目录继续读其 `README.md` 与 `paper_content.txt`。
8. 完成单篇目录后，必须回写 [SUMMARY.md](./SUMMARY.md)，不能只增加文件而不入账。

## 11. 后续 AI 应优先做什么、避免做什么

优先做的事：

1. 继续补 `2016` 与 `2018` 仍偏空的核心技术/扩展条目，优先沿 `importance splitting`、更系统的 `UPPAAL 5` 论文、现代搜索/抽象优化、`controller synthesis / shield synthesis` 等方向推进。
2. 围绕现有文库里的高频作者主线继续补齐重要扩展工作，尤其是 `Kim Guldstrand Larsen`、`Marius Mikučionis`、`Ulrik Nyman`、`Axel Legay`、`Marco Muñiz`、`Peter Gjøl Jensen`、`Andrzej Wąsowski` 相关的后续条目。
3. 在新增条目时同步评定双维材料状态，而不是只写“有无 PDF”。
4. 在检索时同时维护“技术关键词簇”和“作者关键词簇”，并回写作者的角色判断、主要贡献方向和年代窗口。
5. 如果检索命中的条目主贡献明显是案例验证或系统应用，应直接转入 [uppaal_apps/README.md](../uppaal_apps/README.md) 处理，而不是继续塞回本技术文库。

应避免的事：

1. 把本论文集写成“所有 timed automata 论文”的大杂烩。
2. 只因某篇论文和 DBM 或 timed automata 有一点关系，就直接归入 `UPPAAL` 理论与技术文库。
3. 只复制 PDF，不补 `paper_content.txt` 和 `bibtex.bib`。
4. 在文档中写入外部本地绝对路径或把外部文件路径直接当成仓库引用。
