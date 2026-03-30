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

以下入口已按 `2026-03-30` 核对，后续扩库、查源码、查模型、查支持渠道时应优先从这里反推。

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

- 技术主线：`UPPAAL + timed automata + DBM/zone/federation/unification sharing/symbolic state/timed I/O automata/dynamic extrapolation/bounded DBM/clock-state construction`
- 扩展主线：`UPPAAL + symmetry reduction/guided synthesis/priced/cost-optimal/priced timed games/discount-optimality/CORA/timed games/Tiga/game-based testing/statistical model checking/distributed SMC/Control-SMC/stochastic hybrid systems/stochastic hybrid games/compact strategies/SOS/importance splitting/randomized reachability/randomized refinement/MCTS/disjoint activity/urgent partial order reduction/guaranteed control synthesis/continuous systems/multi-weighted logics/GPU acceleration/Coshy/TATL/EADG/vertex merge/expansion abstraction`
- 工程主线：`UPPAAL + architecture/implementation/tutorial/TRON/online testing/T-Uppaal/relativized ioco/timed trace inclusion/ECDAR/compositional verification/UPPAAL PORT/component-based/local time/Buchi/mutation-based testing/fault localisation/diabolic completion/Yggdrasil/FMI/FMU/co-simulation/WCET/binary programs/hardware timing`
- 作者主线：`Kim Guldstrand Larsen`、`Alexandre David`、`Marius Mikučionis`、`Ulrik Nyman`、`Axel Legay`、`Paul Pettersson`、`Marco Muñiz`、`Nicolaj Ø. Jensen`
- 分支作者：`Brian Nielsen`、`Anders Hessel`、`Uli Fahrenberg`、`John Håkansson`、`Florian Lorber`、`E. J. Njor`
- 应用主线：已迁出到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)，本文件不再继续展开

### 已观察到的高命中特征

- 标题直接出现 `UPPAAL`、`ECDAR`、`TRON`、`timed I/O automata`、`priced timed`、`symmetry reduction`、`SMC`、`partial order reduction`、`clock state construction`、`FMI/FMU`、`co-simulation`、`WCET`、`continuous systems`、`multi-weighted logics`、`TATL`
- `作者名 + 分支词 + pdf/site:uppaal.org` 的检索效果显著提升，尤其是 `Kim Guldstrand Larsen`、`Ulrik Nyman`、`Marius Mikucionis`、`Nicolaj Ø. Jensen`、`Marco Muñiz` 这几条线
- `uppaal.org/texts/`、Aalborg / VBN / Dagstuhl / EPTCS 等官方或机构直链 PDF 命中率明显高于只搜 DOI
- `ECDAR / TIOA` 相关条目里，`ecdar.net` 与 `github.com/Ecdar` 能直接提供源码核验入口
- `TRON / online testing` 相关条目里，官方 `TRON manual` 与 `features/#tron` 对判断“只有运行版还是有源码”很关键；`Uppaal` 新近性能论文则常把实现线索藏在 reproducibility package 或 artifact 说明里
- `CONCUR / FORMATS / EPTCS / ICECCS / LNCS CPS` 上的条目如果标题直接出现 `FMI/FMU / ATL / abstractions / EADG / guaranteed control synthesis / WCET`，往往对应 `UPPAAL` 在异构协同、复杂硬件时序与更强博弈逻辑上的延展线

### 已观察到的低命中特征

- 只写 `hybrid systems`、`planning`、`Monte Carlo Tree Search`、`FMI` 或 `WCET`，但不带 `UPPAAL / ECDAR / timed automata`
- 只写 `model-based testing`，却不带 `TRON / online testing / timed trace inclusion / relativized ioco`
- 只写 `component-based design`、`Buchi games` 或 `GPU model checking`，但不带 `UPPAAL PORT / ECDAR / stochastic timed automata`
- 只在 related work 里顺带提一次 `UPPAAL` 的概率验证或博弈验证论文
- 只用工具名或只用作者名单独搜索，都容易造成噪声膨胀
- 只有教程页、案例页、安装说明而没有正式论文正文的条目，不适合直接正式入账

### 检索倾向调整

- 当前文库已经把 `time-optimal testing / priced timed games / CORA scheduling / adaptive testing / discount-optimality / strategy evaluation / ECDAR fault localisation / UPPAAL-native conformance / FMI-FMU co-simulation / WUPPAAL WCET / guaranteed continuous-system synthesis / multi-weighted logics / TATL` 这些支线正式补入，总体策略应转成“补缺口 + 补断代”
- `⚡` 改进与扩展仍是当前主干，后续应继续沿 `importance splitting / planning-guided exploration / UPPAAL 5 / shield synthesis / timed ATL` 扩张
- `2015-2019` 已不再是近乎空白的断层，但 `2016` 与 `2018` 的理论/统计现代化条目仍偏空，应继续定点补 `importance splitting / UPPAAL 5 / SMC modernisation`
- 应用检索线已迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md)，本文件后续只保留必要的技术侧分流说明
- 每次更新前先删减失效关键词，保持本节简洁

## 技术演进时间线与近年活动观察

- 当前已收录顶层条目已经覆盖 `1990-2025`，不再只停留在 `1990-2015` 的早中期奠基阶段。
- 当前技术主线已经可以拆成“理论奠基 -> 架构与状态压缩 -> testing / priced games / component-based 分叉 -> specification theory / ECDAR -> SMC / strategy evaluation -> co-simulation / WCET / continuous control / multi-resource logics -> testing 工程化回流 -> randomized / planning / bounded reconstruction -> GPU / Coshy / TATL”这几段。
- 官方 changelog 仍显示后续版本持续发布：`2023-06-21` 的 `UPPAAL 5.0.0`、`2023-12-11` 的 `UPPAAL 5.1.0-beta5`、`2025-07-04` 的 `UPPAAL 5.1.0-b5-COSHY`。
- 官方 GitHub org 也显示近期仍有源码活动：`UDBM`、`utap`、`uppaal-libs`、`docs.uppaal.org` 在 `2025-2026` 仍有更新。
- 当前最明显的技术缺口已收窄到 `2016` 与 `2018` 的理论/统计现代化层，尤其是 `importance splitting`、更系统的 `UPPAAL 5` 技术论文和若干现代搜索/抽象优化条目。

### 技术演进线总表

| 阶段 | 时间范围 | 主线主题 | 关键问题 | 代表条目 | 当前判断 |
|---|---|---|---|---|---|
| 理论前史与引擎奠基 | `1990-1997` | timed automata 语义、symbolic model checking、compact DBM | 如何用 clocks / guards / resets / symbolic states 表示 dense-time reachability | `ad90`、`lpw95`、`llpy97`、`lpy97` | 基础骨架已经清楚，后续主要是按引用关系回看源头 |
| 架构重构与状态压缩 | `2001-2004` | architecture、implementation、DBM / zone / federation / symmetry reduction | 如何把理论底盘做成可扩展引擎，并同时压缩约束表示与对称重复状态 | `behrmann01`、`bengtsson02`、`behrmann03`、`bblp04`、`hendriks04`、`bdl04` | 这是当前文库最完整的一段，也是后续继续补链的基准骨架 |
| 测试、博弈、代价优化与组件建模分叉 | `2003-2009` | `TRON`、time-optimal testing、priced timed games、`CORA`、`Tiga`、`UPPAAL PORT` | 如何从验证走向 test generation、optimal scheduling、controller synthesis 与 component-based local-time 建模 | `mikucionis03`、`hessel04`、`bouyer04`、`behrmann05`、`cassez05`、`david08`、`hakansson08`、`fahrenberg09` | 这一段现在已经不再只是“testing 支线”，而是把 priced/game/testing/component 四条早期扩展线都接起来了 |
| 规范理论化与组合验证环境 | `2010-2013` | `TIOA`、specification theory、`ECDAR`、Büchi timed specs、compositional verification | 如何定义 refinement / consistency / quotient / liveness contract，并把它做成组件级验证环境 | `david10-ecdar-env`、`david10-method`、`david10-spec`、`nyman10`、`david12-ecdar`、`david13-rtspec` | 这是当前“理论最完整且实现可追”的一段，适合继续沿作者线深挖 |
| 统计模型检查、代价分析与策略评价 | `2011-2015` | `SMC`、distributed SMC、`UPPAAL-SMC`、priced PTA、expected cost、strategy evaluation、`Stratego` | 如何把概率、代价、混杂与策略后评价接入 `UPPAAL`，并把大量采样扩到分布式环境 | `david11-smc`、`bulychev11`、`bulychev12`、`bulychev12-smc`、`david12-shs`、`david14-*`、`david15-*` | 主线已经清楚，但向近年现代版本过渡时仍缺中间段 |
| 跨工具协同、复杂时序与连续/多资源外推 | `2015-2019` | `FMI-FMU`、co-simulation、`WUPPAAL`、continuous-system `Tiga`、multi-weighted logics | 如何让 `UPPAAL` 进入异构协同仿真、二进制硬件时序分析、连续控制与多资源 branching-time 逻辑 | `bogomolov15`、`cassez17`、`nyman17-fmu`、`jensen19-mwlogic`、`lecoent19-tiga` | 说明 `2015-2019` 并非空档，而是 `UPPAAL` 向异构协同、复杂硬件时序和更强控制/逻辑能力外推的阶段 |
| 测试工程化与故障定位回流 | `2017-2020` | mutation-based testing、fault localisation、`UPPAAL` 原生 conformance | 如何把 `ECDAR` testing 推进成 IDE 工作流，并把 conformance checking 重新压回 `UPPAAL` verifier | `nyman17`、`gundersen18`、`njor20` | 这条线现在已经从理论 testing 扩展到工程化与 verifier 复用，后续仍可继续补 `Yggdrasil` 相关材料 |
| 结构感知压缩与现代搜索 | `2012-2023` | disjoint activity、urgent POR、randomized analysis、`MCTS`、dynamic extrapolation、bounded reconstruction | 如何压缩 interleavings，并在 planning、现代 `XTA` 抽象和在线恢复之间继续推进 | `muniz12`、`muniz20`、`kiviriga20-randref`、`kiviriga21-randreach`、`jensen22-mcts`、`lu22`、`jensen23-dynext` | 说明 `UPPAAL` 近年不只做查询语言，也在继续推进引擎能力和在线工作流 |
| 仍待补的过渡缺口 | `2016-2018` | `UPPAAL 5`、importance splitting、过渡期现代化 | 如何把 `SMC / Stratego` 进一步推到更现代的搜索与统计框架，并补齐 `2016` 与 `2018` 之间仍缺的理论层节点 | `importance-splitting-line` | 这段已不再整体空白，但 `importance splitting / UPPAAL 5` 仍是下一轮最值得定点补齐的缺口 |
| 混成防护、异构加速与更强博弈逻辑 | `2024-2025` | GPU-SMC、`Coshy`、`TATL` | 如何把 `SMC` 推到 GPU，把 shielding 做成新近分支，并把 `TCTL/Tiga` 推进到更强的 timed ATL symbolic 验证 | `muniz24`、`brorholt25-coshy`、`jensen25` | 说明 `UPPAAL` 技术线没有停在零几年，近年仍在持续演进且仍有强理论新作 |

## 现有收录论文作者关联

以下作者关系只基于当前 **70 个顶层条目** 的 `bibtex.bib` 统计；`paper-*` 子目录当前不单独重复计数。后续扩库时，应先沿这张作者关系表追踪，再去官方入口核验源码、案例和工具实现。

这里的“继续沿该作者线扩张判断”是**检索价值推断**，表示继续顺着该作者找 `UPPAAL` 后续工作时的预期收益，不是对作者个人职业状态的断言。

### 核心作者主线

| 作者 | 频次 | 角色判断 | 主要贡献方向 | 当前文库覆盖年份 | 当前核验到的较新 `UPPAAL` 年份 | 最近性判断 | 继续沿该作者线扩张判断 | 代表关联条目 |
|---|---:|---|---|---|---|---|---|---|
| [Kim Guldstrand Larsen](https://kgl.cs.aau.dk/) | 56 | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / priced games / Tiga / SMC / TRON / ECDAR / modern abstractions` | `1995-2025` | `2025` | 🟢 早期到近年全程贯穿 | 🟢 高 | `lpw95`、`bouyer04`、`behrmann07`、`bogomolov15`、`lecoent19-tiga`、`muniz24`、`jensen25` |
| [Alexandre David](https://homes.cs.aau.dk/~adavid/) | 27 | 中后期扩展主线整合者 | `game-based testing / architecture / ECDAR / SMC / strategy evaluation / TIOA / SHS` | `2001-2015` | `2015` | 🟨 文库内高频但近年直接条目暂止于 `2015` | 🟢 高 | `david08`、`david10-*`、`bulychev12-smc`、`david12-*`、`david14-*`、`david15-*` |
| [Axel Legay](https://www.uclouvain.be/en/people/axel.legay) | 16 | `SMC + specification theory` 桥接作者 | `statistical model checking / priced models / timed I/O specification / optimization / SHS / distributed SMC / co-simulation` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接延展 | 🟢 高 | `david10-*`、`bulychev11`、`bulychev12-smc`、`david11-*`、`nyman17-fmu`、`goorden23` |
| [Gerd Behrmann](https://dblp.org/pid/39/5834) | 13 | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / CORA / symmetry-aware engine / UPPAAL 4.0 / evolution survey` | `2001-2011` | `2011` | 🟨 中期工程主线已较完整 | 🟨 中等 | `amnell01`、`behrmann02-*`、`behrmann03`、`behrmann05`、`behrmann06`、`behrmann11` |
| [Marius Mikučionis](https://people.cs.aau.dk/~marius/cv.html) / [Marius Mikucionis](https://people.cs.aau.dk/~marius/cv.html) | 15 | `TRON -> SMC -> POR/GPU -> Coshy` 纵向桥接作者 | `online testing / statistical model checking / co-simulation / urgent POR / GPU-SMC / strategy synthesis / hybrid shielding` | `2004-2025` | `2025` | 🟢 横跨早期测试线和近年扩展线 | 🟢 高 | `larsen04-*`、`bogomolov15`、`lecoent19-tiga`、`muniz20`、`muniz24`、`brorholt25` |
| [Paul Pettersson](https://www.es.mdu.se/staff/166-Paul_Pettersson) | 13 | `DBM / engine / component-modeling / testing` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities / PORT / TRON / testing` | `1995-2011` | `2011` | 🟨 更偏历史骨干作者 | 🟨 中等 | `lpw95`、`llpy97`、`hessel04`、`hakansson08`、`hessel08`、`dhlp06` |
| [Ulrik Nyman](https://vbn.aau.dk/en/persons/ulrik-nyman) | 13 | `ECDAR / timed-spec / testing / randomized analysis` 主线组织者 | `specification theory / refinement / mutation-based testing / fault localisation / compositional verification / randomized analysis / planning / co-simulation` | `2010-2023` | `2023` | 🟢 `2020s` 仍有直接论文 | 🟢 高 | `david10-*`、`nyman10`、`nyman17`、`nyman17-fmu`、`gundersen18`、`kiviriga20`、`jensen22` |
| [Wang Yi](https://user.it.uu.se/~wangyi/) | 10 | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations / DBM` | `1995-2011` | `2011` | 🟨 早期到中期主线较完整 | 🟨 中等 | `lpw95`、`llpy97`、`amnell01`、`by04`、`behrmann02`、`behrmann06` |
| [Andrzej Wąsowski](https://www.itu.dk/~wasowski/) | 8 | `ECDAR` 规范理论与新近扩展连接者 | `timed I/O specification / quotient / compositional verification / liveness contracts / Coshy 协作线` | `2010-2025` | `2025` | 🟢 近年仍有直接条目 | 🟢 高 | `david10-*`、`nyman10`、`david12-ecdar`、`david13`、`goorden23`、`brorholt25` |
| [Peter Gjøl Jensen](https://vbn.aau.dk/en/persons/pgj/) | 7 | `optimization -> co-simulation / WCET -> abstraction / GPU-SMC -> hybrid synthesis` 桥接作者 | `expected cost / FMI-FMU co-simulation / WCET / dynamic extrapolation / GPU-SMC / compact shields` | `2014-2025` | `2025` | 🟢 近年仍有连续新作 | 🟢 高 | `david14`、`bogomolov15`、`cassez17`、`nyman17-fmu`、`jensen23`、`muniz24`、`brorholt25` |

### 分支协作者与历史前驱

| 作者 / 别名 | 当前关联条目 | 角色判断 | 主要贡献方向 | 年代观察 | 检索建议 |
|---|---|---|---|---|---|
| [Brian Nielsen](https://homes.cs.aau.dk/~bnielsen/) | `hessel04`、`larsen04-*`、`david08`、`hessel08`、`nyman17` | `TRON / adaptive testing / mutation testing` 分支关键协作者 | `model-based testing / timed trace inclusion / relativized ioco / game-based testing / mutation-based testing` | 当前文库直接覆盖 `2004-2017` | 与 `UPPAAL + TRON/online testing/game-based testing/mutation-based testing` 联用 |
| [Arne Skou](https://homes.cs.aau.dk/~ask/) | `hessel04`、`hessel08`、`david12-ecdar` | `testing / conformance / compositional verification` 分支关键协作者 | `real-time testing / conformance / compositional verification / ECDAR` | 当前文库直接覆盖 `2004-2012`，跨越早期 testing 到后续 compositional verification | 与 `UPPAAL + testing/conformance/compositional verification` 联用 |
| [Anders Hessel](https://hessel.tech/) | `hessel04`、`hessel08` | `time-optimal / survey-style testing` 分支作者 | `offline test generation / time-optimal testing / testing survey` | 当前文库直接覆盖 `2004-2008` | 与 `UPPAAL + time-optimal testing/test-case generation` 联用 |
| [Marco Muñiz](https://homes.cs.aau.dk/~muniz/) | `muniz12`、`muniz20`、`muniz24` | `结构感知压缩 -> urgent POR -> GPU-SMC` 分支作者 | `disjoint activity / urgent partial order reduction / GPU-SMC` | 当前文库直接覆盖 `2012-2025`，且跨越三次明显代际更新 | 与 `UPPAAL + disjoint activity/partial order reduction/GPU-SMC` 联用 |
| [Uli Fahrenberg](https://dblp.org/pid/89/5538) | `fahrenberg09` | infinite-run priced optimization 分支作者 | `discount-optimality / infinite runs / corner-point abstraction` | 当前文库当前只覆盖 `2009`，但它补上了 priced PTA 的长期运行最优语义 | 与 `UPPAAL + priced timed automata/discount-optimal infinite runs` 联用 |
| [John Håkansson](https://dblp.org/pid/09/6977) / [Jan Carlson](https://www.es.mdu.se/staff/40-Jan_Carlson) | `hakansson08` | `UPPAAL PORT / component-based design` 分支作者 | `component-based design / local time / PORT / SaveCCM` | 当前文库当前只覆盖 `2008`，但方向明显对接嵌入式组件建模 | 与 `UPPAAL PORT/component-based/local time/SaveCCM` 联用 |
| [Martijn Hendriks](https://dblp.org/pid/h/MartijnHendriks) / [Peter Niebert](https://dblp.org/pid/n/PeterNiebert) / [Frits Vaandrager](https://fvaan.nl/) | `hendriks04` | `symmetry reduction` 分支关键作者 | `scalarset / state swaps / canonical representative / symmetry reduction` | 当前文库当前只覆盖 `2004`，但这是状态压缩线的重要节点 | 与 `UPPAAL + symmetry reduction/scalarset/canonical representative` 联用 |
| [Thomas Hune](https://dblp.org/search/author?q=Thomas%20Hune) | `amnell01`、`hune01` | 早期 `guided synthesis` 线作者 | `guided synthesis / control programs / early tool planning` | 当前文库直接覆盖 `2001` | 与 `UPPAAL + guided synthesis/control` 联用 |
| [Sean Sedwards](https://dblp.org/pid/26/5698) | `david12-shs` | `SHS / SMC` 分支补强作者 | `stochastic hybrid systems / simulation semantics / statistical analysis` | 当前文库直接覆盖 `2012` | 与 `UPPAAL + stochastic hybrid systems/SMC` 联用 |
| [Danny Bøgsted Poulsen](https://vbn.aau.dk/en/persons/dannybpoulsen/) | `bulychev12-smc`、`david11-*`、`david12-shs`、`david15-smc-tutorial` | `UPPAAL-SMC` 工程化与教程化高频协作者 | `statistical model checking / stochastic semantics / distributed SMC / tutorialization` | 当前文库直接覆盖 `2011-2015`，是 `SMC` 中期成形阶段的高频作者 | 与 `UPPAAL + SMC/stochastic semantics/distributed/tutorial` 联用 |
| [Peter Bulychev](https://dblp.org/search/author?q=Peter%20Bulychev) | `bulychev11`、`bulychev12-*` | 早期 `UPPAAL-SMC` 核心扩展作者 | `distributed parametric SMC / priced timed automata / early SMC implementation` | 当前文库直接覆盖 `2011-2012`，集中在 `UPPAAL-SMC` 形成初期 | 与 `UPPAAL + distributed statistical model checking/priced timed automata` 联用 |
| [Zheng Wang](https://www.hipeac.net/~wangzheng/) | `bulychev12-smc`、`david11-*` | `UPPAAL-SMC` 性能与语义补强作者 | `stochastic semantics / priced timed automata / performance-oriented SMC` | 当前文库直接覆盖 `2011-2012`，落在 `SMC` 语义与性能优化节点上 | 与 `UPPAAL + stochastic semantics/priced timed automata/SMC` 联用 |
| [Pranav Ashok](https://dblp.org/pid/200/8227) / [Jan Křetínský](https://www7.in.tum.de/~kretinsk/) / [Adrien Le Coënt](https://dblp.org/pid/172/2815) / [Jakob Haahr Taankvist](https://dblp.org/search/author?q=Jakob%20Haahr%20Taankvist) / [Maximilian Weininger](https://dblp.org/search/author?q=Maximilian%20Weininger) | `ashok19-sos`、`lecoent19-tiga` | `compact strategies / continuous control synthesis` 分支作者群 | `safe-optimal-small strategies / stochastic hybrid games / hybrid MDP / guaranteed control synthesis` | 当前文库直接覆盖 `2019`，且已连起 compact strategies 与连续控制合成两条紧邻分支 | 与 `UPPAAL + SOS/compact strategies/continuous systems/Tiga` 联用 |
| [Andrej Kiviriga](https://dblp.org/search/author?q=Andrej%20Kiviriga) | `kiviriga20`、`kiviriga21`、`jensen22` | `randomized analysis / planning` 新近主线作者 | `randomized refinement / randomized reachability / MCTS` | 当前文库直接覆盖 `2020-2022` | 与 `UPPAAL + randomized reachability/refinement/MCTS` 联用 |
| [Nicolaj Ø. Jensen](https://vbn.aau.dk/en/persons/noje/) | `jensen23`、`jensen25` | `modern XTA abstraction -> timed ATL` 新近作者 | `dynamic extrapolation / extended timed automata / TATL / EADG / abstractions` | 当前文库直接覆盖 `2023-2025`，而且已经从抽象优化延伸到更强的 timed game logic | 与 `UPPAAL + dynamic extrapolation/TATL/EADG` 联用 |
| [Martijn A. Goorden](https://dblp.org/search/author?q=Martijn%20A.%20Goorden) | `goorden23` | `TIOA` 规范理论补完作者 | `complete specification theory / ECDAR` | 当前文库当前只覆盖 `2023`，适合继续追 `ECDAR` 理论后续 | 与 `UPPAAL + timed I/O automata/specification theory` 联用 |
| [Asger Horn Brorholt](https://vbn.aau.dk/en/persons/asgerhb/) | `brorholt25` | `Coshy` 新近作者 | `automatic shield synthesis / hybrid systems / compact shields` | 当前文库当前只覆盖 `2025`，但非常新，后续继续扩张概率高 | 与 `UPPAAL + Coshy/hybrid shield synthesis` 联用 |
| [Franck Cassez](https://franck44.github.io/publications/) | `bouyer04`、`cassez05`、`cassez17` | `priced timed games -> WCET` 分支作者 | `priced timed games / timed games / WCET / binary-program analysis` | 当前文库直接覆盖 `2004-2017`，把早期 timed games 与后续 `WUPPAAL` 连了起来 | 与 `UPPAAL + timed games/priced timed games/WCET` 联用 |
| [Didier Lime](https://dblp.org/pid/94/6720) | `cassez05`、`behrmann07`、`david14`、`jensen25` | `timed games -> Tiga -> optimization -> TATL` 分支协作者 | `timed games / controller synthesis / cost analysis / timed ATL` | 当前文库已直接覆盖到 `2025`，说明该线并未停留在早期 `Tiga` 阶段 | 与 `UPPAAL + timed games/Tiga/TATL` 联用 |
| [Emmanuel Fleury](https://dblp.org/search/author?q=Emmanuel%20Fleury) | `bouyer04`、`cassez05`、`behrmann07` | `priced timed games -> Tiga` 分支协作者 | `priced timed games / timed games / controller synthesis` | 当前文库直接覆盖 `2004-2007`，正好卡在 `priced timed games -> Tiga` 过渡带 | 与 `UPPAAL + timed games/priced timed games/controller synthesis` 联用 |
| [Florian Lorber](https://dblp.org/pid/117/5464.html) / [Christian Ovesen](https://dblp.org/search/author?q=Christian%20Ovesen) / [E. J. Njor](https://people.compute.dtu.dk/emjn/) | `gundersen18`、`njor20` | `ECDAR -> UPPAAL-native conformance testing` 工程分支作者群 | `fault localisation / conformance testing / diabolic completion / Yggdrasil` | 当前文库直接覆盖 `2018-2020`，正好串起 testing 工程化回流线 | 与 `UPPAAL + conformance testing/Ecdar/diabolic completion/Yggdrasil` 联用 |
| [Johan Bengtsson](https://dblp.org/search/author?q=Johan%20Bengtsson) | `bengtsson02`、`behrmann02-secrets`、`by04` | `DBM` 数据结构专题化奠基作者 | `clocks / DBMs / states / DBM internals / implementation detail` | 当前文库主要落在 `2002-2004` | 与 `UPPAAL + DBM/implementation` 联用 |
| [Patricia Bouyer](https://www.lmf.cnrs.fr/Annuaire/Patricia.Bouyer/) / [Radek Pelánek](https://www.fi.muni.cz/~xpelanek/) | `bblp04`、`bouyer04` | zone abstraction 与 priced timed games 外推分支关键合作者 | `lower-upper bound extrapolation / zone abstraction / priced timed games` | 当前文库主要落在 `2004`，但已同时覆盖抽象与最优策略两条 priced 线 | 与 `UPPAAL + abstraction/priced timed games/extrapolation` 联用 |
| [Rajeev Alur](https://www.cis.upenn.edu/~alur/) | `ad90` | 理论前史奠基者 | `timed automata semantics` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 理论源头时纳入 |
| [David Dill](https://theory.stanford.edu/~dill/) / [David L. Dill](https://theory.stanford.edu/~dill/) | `ad90`、`dill89` | dense-time verification 前史奠基者 | `timing assumptions / clock constraints / symbolic verification` | 属于理论前史，不应用来判断 `UPPAAL` 近年是否仍活跃 | 只在追踪 `UPPAAL` 技术前史时纳入 |

## 当前收录统计

- 已收录顶层条目：**70** 篇
- 本轮新增顶层条目：**5** 篇（本次补收 `FMI-FMU co-simulation / WUPPAAL WCET / continuous-system Tiga / branching multi-weighted logics` 等 `2015-2019` 条目）
- 含内嵌 `paper-*` 子目录的 thesis/合集条目：**2** 篇
- 已完成 `desc.md` 的顶层条目：**70** 篇（`70/70`）
- 内容详细程度：
  - `🟢 复现级`：**6** 篇
  - `🟩 较完整`：**45** 篇
  - `🟨 中等`：**11** 篇
  - `🟧 概览级`：**8** 篇
  - `🟥 细节不足`：**0** 篇
- 实现可获取程度：
  - `🟢 论文对应实现源码直达`：**5** 篇
  - `🟩 核心实现源码线直达`：**8** 篇
  - `🟨 部分实现源码可得`：**16** 篇
  - `🟧 仅可执行/可使用版本可得`：**33** 篇
  - `🟥 暂未获取实现源码`：**8** 篇
- 本轮未纳入/待补证条目：**2** 条
- 已记录环境级阻塞：**1** 条

说明：`behrmann03` 与 `bengtsson02` 下的 `paper-*` 子目录当前作为父条目的辅助阅读单元存在，不单独计入以上顶层统计。

## 分类分布

| 分类 | 篇数 | 占比 | 说明 |
|---|---:|---:|---|
| 🧱 核心算法/数据结构 | 9 | 12.9% | 已覆盖 timed automata、DBM、zone、specification theory、bounded clock-state reconstruction 等主线 |
| ⚡ 改进与扩展 | 40 | 57.1% | 已覆盖 symmetry reduction、priced/timed games、SMC、strategy evaluation、continuous-system synthesis、multi-weighted logics、Büchi timed specs、urgent POR、GPU-SMC、compact strategies、Coshy、`TATL` |
| 🛠️ 工程/工具链 | 21 | 30.0% | 已覆盖 architecture、implementation、tutorial、`TRON/testing`、`UPPAAL PORT`、`ECDAR` environment、fault localisation、co-simulation、`WUPPAAL` 与 `UPPAAL` 原生 conformance testing |
| **合计** | **70** | **100.0%** | - |

说明：应用类条目已迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md) 单独维护。

## 单篇 `DESC` 对齐口径

后续单篇 `desc.md` 统一遵循 [DESC_GUIDE.md](./DESC_GUIDE.md)。

当前 **70** 个顶层条目已经全部完成首轮 `desc.md` 覆盖；`paper-*` 子目录仍按父条目辅助阅读单元维护，不单独计入这里的顶层 `desc` 统计。

本总表中的三列：

1. `问题简述`
2. `方法简述`
3. `解决点简述`

是单篇 `desc.md` 开头三条一句话简述的压缩版。也就是说：

1. `SUMMARY.md` 负责全局速览。
2. `desc.md` 负责把单篇的问题、方法和解决点展开讲清楚。

## 论文清单

### 🧱 / ⚡ / 🛠️ 统一总表（按年份升序，状态列压缩为 emoji）

表格口径补充如下：

1. `详度` 列只写一个 emoji，具体含义看本文件前面的“内容详细程度”口径表。
2. `实现` 列只写一个 emoji，具体含义看本文件前面的“实现可获取程度”口径表。
3. 每行的文字性依据与源码入口统一放在 `源码线索` 列，不再把解释重复写进状态单元格。
4. `链接` 列统一使用短链接 `[paper](相对路径)`，避免目录名把表格撑宽。

| 类型 | Key | 标题 | 年份 | 问题简述 | 方法简述 | 解决点简述 | 详度 | 实现 | 源码线索 | 链接 |
|---|---|---|---:|---|---|---|---|---|---|---|
| 🧱 | `ad90` | Automata for Modeling Real-Time Systems | 1990 | 实时系统缺少统一时钟自动机模型 | 定义 clocks/guards/resets 的 timed automata 语义 | 奠定 `UPPAAL` 全部时钟自动机底座 | 🟩 | 🟥 | 作为理论源头保留；当前无直接源码线索 | [paper](./ad90-timed-automata/) |
| 🧱 | `dill89` | Timing Assumptions and Verification of Finite-State Concurrent Systems | 1990 | dense-time 并发验证缺少可操作约束表示 | 用 timing assumptions 与 symbolic clock constraints | 提供 clock-constraint 前史基础 | 🟨 | 🟥 | 作为历史前驱保留；当前无直接源码线索 | [paper](./dill89-timing-assumptions/) |
| 🧱 | `lpw95` | Model-Checking for Real-Time Systems | 1995 | real-time reachability 穷举验证代价过高 | symbolic states + constraint solving + on-the-fly | 立起早期 `UPPAAL` 验证核心 | 🟩 | 🟧 | 官方有可下载工具线，但当前未见对应模型检查核心源码公开 | [paper](./lpw95-real-time-model-checking/) |
| 🧱 | `llpy97` | Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction | 1997 | DBM 存储大且状态空间膨胀 | compact DBM + state-space reduction | 降低 `UDBM/UPPAAL` 内存与搜索成本 | 🟢 | 🟩 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供同一技术线的核心 DBM 源码 | [paper](./llpy97-compact-data-structure/) |
| 🛠️ | `lpy97` | UPPAAL in a Nutshell | 1997 | 工具功能、语义与工作流难整体把握 | 系统总览 description/simulator/checker 流程 | 给出早期完整工具结构与使用入口 | 🟧 | 🟧 | 官方有文档与工具可用版本，但当前未见对应早期 toolbox 完整源码公开 | [paper](./lpy97-uppaal-nutshell/) |
| 🛠️ | `amnell01` | UPPAAL - Now, Next, and Future | 2001 | 早期 `UPPAAL` 能力边界与路线不清 | 官方路线综述与能力盘点 | 明确 early roadmap 与技术议程 | 🟧 | 🟨 | 可沿 [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 追同代核心组件源码线，但论文本身无实现直链 | [paper](./amnell01-uppaal-now-next-future/) |
| ⚡ | `behrmann01` | Efficient Guiding Towards Cost-Optimality in UPPAAL | 2001 | timed reachability 缺少代价最优能力 | 引入 cost-guided symbolic search | 打开 priced/cost-optimal 主线 | 🟩 | 🟥 | 论文可得；当前未见与该分支直接对应的公开源码线 | [paper](./behrmann01-cost-optimality-uppaal/) |
| ⚡ | `hune01` | Guided Synthesis of Control Programs Using Uppaal | 2001 | control synthesis 难与 timed analysis 衔接 | 用 `UPPAAL` 分析结果引导控制程序合成 | 把合成问题接入 `UPPAAL` 技术线 | 🟩 | 🟧 | 当前仅能核到论文与工具历史材料；guided synthesis 对应实现源码未见公开 | [paper](./hune01-guided-synthesis-control-programs-uppaal/) |
| 🛠️ | `bdly02` | New UPPAAL Architecture | 2002 | 旧引擎架构不利于扩展与组件化 | 重构模块化架构与引擎分层 | 为后续组件化演进打底 | 🟨 | 🟨 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 等组件源码可得 | [paper](./behrmann02-new-uppaal-architecture/) |
| 🧱 | `bengtsson02` | Clocks, DBMs and States in Timed Systems | 2002 | DBM 语义、操作与存储缺少系统说明 | thesis 级系统整理 `DBM/normalization/storage` | 成为 `UDBM` 内核理解主入口 | 🟢 | 🟢 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[python_dbm](https://github.com/UPPAALModelChecker/python_dbm) 直接对应 DBM 实现主题 | [paper](./bengtsson02-clocks-dbms-states/) |
| 🛠️ | `bbdlpy02` | UPPAAL Implementation Secrets | 2003 | 引擎实现选择与性能来源不透明 | 拆解实现细节、表示和优化技巧 | 解释 `UPPAAL` 工程效率从何而来 | 🟩 | 🟨 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer) 等组件源码可得 | [paper](./behrmann02-uppaal-implementation-secrets/) |
| ⚡ | `behrmann03` | Data Structures and Algorithms for the Analysis of Real Time Systems | 2003 | 单一 DBM 表示难覆盖更复杂分析需求 | 系统整理 zones/CDD/priced 数据结构与算法 | 扩展 real-time analysis 数据结构版图 | 🟩 | 🟨 | [UCDD](https://github.com/UPPAALModelChecker/UCDD)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 可得，但 thesis 覆盖整条能力线不全有源码 | [paper](./behrmann03-real-time-data-structures/) |
| ⚡ | `david03-share` | Unification \& Sharing in Timed Automata Verification | 2003 | 符号状态和约束重复造成存储浪费 | unification \& sharing 复用状态与约束 | 压缩表示并提升验证效率 | 🟨 | 🟨 | 可沿 [UDBM](https://github.com/UPPAALModelChecker/UDBM) 与 [utap](https://github.com/UPPAALModelChecker/utap) 追底层符号表示和解析器源码，但论文对应优化实现未完整公开 | [paper](./david03-unification-sharing-timed-automata-verification/) |
| 🛠️ | `mikucionis03-tron` | Online On-the-Fly Testing of Real-time Systems | 2003 | 实时系统测试难在线利用模型 | on-the-fly testing + timed trace inclusion | 把验证能力扩到实时在线测试 | 🟩 | 🟧 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [downloads](https://uppaal.org/downloads/) 可追运行工具线，但 `TRON` 核心源码未见公开 | [paper](./mikucionis03-online-on-the-fly-testing-real-time-systems/) |
| ⚡ | `bblp04` | Lower and Upper Bounds in Zone Based Abstractions of Timed Automata | 2004 | zone abstraction 的精度与终止性难平衡 | lower/upper bound extrapolation | 稳定化 zone abstraction 理论 | 🟩 | 🟨 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 能提供底层 DBM 源码，但该条目的完整外推实现未直出 | [paper](./bblp04-zone-based-abstractions/) |
| 🛠️ | `bdl04` | A Tutorial on Uppaal | 2004 | 用户缺少系统建模与查询指导 | 教程化组织 language/query/interface/patterns | 成为工程使用入口文献 | 🟩 | 🟨 | [utap](https://github.com/UPPAALModelChecker/utap)、[tracer](https://github.com/UPPAALModelChecker/tracer)、[uls](https://github.com/UPPAALModelChecker/uls)、[UDBM](https://github.com/UPPAALModelChecker/UDBM) 等组件源码可得，但完整工具未全部开源 | [paper](./bdl04-uppaal-tutorial/) |
| ⚡ | `bouyer04` | Optimal Strategies in Priced Timed Game Automata | 2004 | priced timed games 缺少真正的最优策略语义与可计算边界 | 给 timed games 叠加 price，并分析 run-based/state-based optimality 与累计代价扩状态归约 | 为 `UPPAAL` priced timed games / optimal-control 路线补上最优性理论框架 | 🟩 | 🟥 | 当前未见论文对应的 priced timed game 求解源码；主要仍停留在理论框架与后续工具线引用 | [paper](./bouyer04-optimal-strategies-priced-timed-game-automata/) |
| 🧱 | `by04` | Timed Automata: Semantics, Algorithms and Tools | 2004 | timed automata 语义算法工具脉络分散 | 统一综述 semantics + algorithms + tools | 压缩整理 timed automata/`UPPAAL` 骨架 | 🟨 | 🟨 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uls](https://github.com/UPPAALModelChecker/uls) 等组件源码可得，但完整工具主实现未公开 | [paper](./by04-semantics-algorithms-tools/) |
| ⚡ | `hendriks04` | Adding Symmetry Reduction to Uppaal | 2004 | 大量对称进程会让 `UPPAAL` 重复探索本质等价状态 | `scalarset + state swaps + canonical representative` | 把 symmetry reduction 真正接进 `UPPAAL` 的 symbolic state | 🟩 | 🟨 | 当前可沿 [UDBM](https://github.com/UPPAALModelChecker/UDBM) 与 [utap](https://github.com/UPPAALModelChecker/utap) 核验同代符号引擎底层，但 symmetry prototype 未见独立公开源码 | [paper](./hendriks04-adding-symmetry-reduction-uppaal/) |
| ⚡ | `hessel04` | Time-Optimal Real-Time Test Case Generation Using Uppaal | 2004 | 实时测试缺少可执行的时间最优生成与统一 coverage 编码 | 以 `DIEOU-TA` 为规格类，把 test purpose / coverage 目标编码为 `UPPAAL` reachability，并取 fastest diagnostic trace | 把 `UPPAAL` reachability / A* 能力改造成离线时间最优测试生成器 | 🟩 | 🟧 | 可沿官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 testing 论文链核验方法线，但论文对应生成器源码未见公开 | [paper](./hessel04-time-optimal-real-time-test-case-generation-uppaal/) |
| 🛠️ | `larsen04-online` | Online Testing of Real-time Systems Using Uppaal | 2004 | online testing 缺少可执行工具链 | `TRON` workflow + verdict 执行链 | 让 testing 分支工具化落地 | 🟨 | 🟧 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [features/#tron](https://uppaal.org/features/#tron) 可核验能力线，但核心源码未见公开 | [paper](./larsen04-online-testing-real-time-systems-using-uppaal/) |
| 🛠️ | `larsen04-status` | Online Testing of Real-time Systems using Uppaal: Status and Future Work | 2004 | `TRON` 当前状态与后续缺口不清 | status review + future-work mapping | 明确 testing 分支议程 | 🟧 | 🟧 | 当前能核到论文与官方测试文档，但未见对应源码公开 | [paper](./larsen04-online-testing-status-future-work/) |
| ⚡ | `behrmann05` | Optimal Scheduling Using Priced Timed Automata | 2005 | `UPPAAL` 缺少把真实 scheduling / planning 稳定映射到 cost-optimal reachability 的方法 | 用 priced timed automata 统一建模任务、资源和代价，并在 `UPPAAL CORA` 中做 priced symbolic search 与 branch-and-bound | 把 `UPPAAL` cost-optimal 技术线推进成可复用的调度/规划工具链 | 🟩 | 🟧 | 当前可沿 `UPPAAL CORA` 历史文献与官网下载入口追可运行工具，但 `CORA` 主实现源码未见公开 | [paper](./behrmann05-optimal-scheduling-priced-timed-automata/) |
| ⚡ | `cdfll05` | Efficient On-the-fly Algorithms for the Analysis of Timed Games | 2005 | timed games on-the-fly analysis 效率不足 | 高效 on-the-fly timed-game 算法 | 成为 `Tiga` 的关键理论前置 | 🟩 | 🟧 | 当前未见 timed-games 核心源码公开；可沿 `Tiga` 工具线与官方文档反查 | [paper](./cassez05-analysis-of-timed-games/) |
| 🛠️ | `behrmann06` | UPPAAL 4.0 | 2006 | 新一代工具能力需要统一对外说明 | 版本快照式整理 language/engine/workflow | 标记 `UPPAAL 4.0` 整合阶段 | 🟧 | 🟨 | [utap](https://github.com/UPPAALModelChecker/utap)、[UDBM](https://github.com/UPPAALModelChecker/UDBM)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 提供部分源码线索 | [paper](./behrmann06-uppaal-4/) |
| ⚡ | `dhlp06` | Model Checking Timed Automata with Priorities Using DBM Subtraction | 2006 | priority timed automata 缺少可操作符号差集 | 用 DBM subtraction 支撑 priority analysis | 打通 priorities/federation 分析路径 | 🟩 | 🟨 | [UDBM](https://github.com/UPPAALModelChecker/UDBM) 提供底层 DBM 技术线源码，但 priorities 主实现未直接公开 | [paper](./dhlp06-dbm-subtraction/) |
| ⚡ | `bcdfll07` | UPPAAL-Tiga: Time for Playing Games! | 2007 | timed-game controller synthesis 缺少工具支撑 | 把 timed games 工具化为 `UPPAAL-Tiga` | 博弈/控制分支正式成型 | 🟧 | 🟧 | 当前未见 `Tiga` 核心源码公开；可沿官方 `Tiga` 历史工具线与文档反查 | [paper](./behrmann07-uppaal-tiga/) |
| ⚡ | `david08` | A Game-Theoretic Approach to Real-Time System Testing | 2008 | 早期 testing 过度依赖 output urgency / isolated outputs，难处理更真实的时序不确定输出 | 用 `Timed I/O Game Automata` + `tioco` + `UPPAAL-TIGA` winning strategy，把 test case 改成自适应博弈策略 | 把实时测试从固定轨迹生成推进到 game-based adaptive testing | 🟩 | 🟧 | 当前可沿 `TIGA` 历史工具线与 testing 文献核验能力，但论文对应策略生成实现未见公开源码 | [paper](./david08-game-theoretic-approach-real-time-system-testing/) |
| 🛠️ | `hakansson08` | Component-Based Design and Analysis of Embedded Systems with UPPAAL PORT | 2008 | component model flatten 后会丢掉结构与局部时间信息 | `UPPAAL PORT + local time + read-execute-write + SaveCCM` | 让组件化实时系统能直接保持结构地分析 | 🟨 | 🟧 | 当前可沿 [downloads](https://uppaal.org/downloads/) 与历史论文追 `UPPAAL PORT` 工具线，但 PORT 对应源码未见公开 | [paper](./hakansson08-uppaal-port-component-based-design-analysis/) |
| 🛠️ | `hessel08-tron` | Testing Real-Time Systems Using UPPAAL | 2008 | testing 理论与工具实践资料分散 | 系统整理 offline/online testing 与 relativized ioco | 成为 `TRON/testing` 标准综述 | 🟩 | 🟧 | 官方 [TRON manual](https://uppaal.org/texts/tron-manual.pdf) 与 [features/#tron](https://uppaal.org/features/#tron) 可核验方法线，但源码未见公开 | [paper](./hessel08-testing-real-time-systems-using-uppaal/) |
| ⚡ | `fahrenberg09` | Discount-Optimal Infinite Runs in Priced Timed Automata | 2009 | priced timed automata 长期偏向有限路径最优，infinite runs 的折扣最优语义与可算性不清楚 | 为 infinite runs 定义 discounted price，并用 corner-point abstraction 把问题归约到有限 weighted graph | 把 `UPPAAL` priced timed automata 优化线从有限 reachability 推进到无限运行最优 | 🟩 | 🟥 | 当前未见论文对应的折扣最优 PTA 求解源码；更像后续工具与理论工作的基础条目 | [paper](./fahrenberg09-discount-optimal-infinite-runs-priced-timed-automata/) |
| 🛠️ | `david10-ecdar-env` | ECDAR: An Environment for Compositional Design and Analysis of Real Time Systems | 2010 | `TIOA` 理论若没有可执行环境就难支撑组合验证工作流 | `ECDAR` 环境实现 refinement/consistency/composition/conjunction/quotient | 把 `TIOA/ECDAR` 做成可建模可验证的工具入口 | 🟨 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 提供该环境主线的开源入口 | [paper](./david10-ecdar-environment-compositional-design-analysis/) |
| 🛠️ | `david10-method` | Methodologies for Specification of Real-Time Systems Using Timed I/O Automata | 2010 | 实时组件规约缺少可执行方法学 | `TIOA` 的 refinement/abstraction/quotient workflow | 给出 `ECDAR` 工程方法入口 | 🟨 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 提供该方法线的开源工具入口 | [paper](./david10-methodologies-timed-io-automata/) |
| 🧱 | `david10-spec` | Timed I/O automata: a complete specification theory for real-time systems | 2010 | real-time component specification theory 不完整 | 补全 refinement/consistency/composition/quotient 理论 | 奠定 `ECDAR` 形式化核心 | 🟩 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR) 与 [Reveaal](https://github.com/Ecdar/Reveaal) 提供同一规范理论/检查线的开源实现入口 | [paper](./david10-timed-io-automata-complete-specification-theory/) |
| 🛠️ | `mikucionis10-tron` | Online Testing of Real-time Systems | 2010 | 实时 online testing 缺少完整模型算法工具说明 | thesis 级整理生成/执行/verdict 框架 | 成为 testing 分支最完整单篇入口 | 🟢 | 🟧 | 当前能核到论文、手册与运行版能力线，但 `TRON` 论文对应源码未见公开 | [paper](./mikucionis10-online-testing-real-time-systems/) |
| 🛠️ | `bdlpy11` | Developing UPPAAL over 15 years | 2011 | 15 年演进脉络分散难整体理解 | 工程与历史 retrospective | 总结 branch splitting 与成熟过程 | 🟧 | 🟨 | [UDBM](https://github.com/UPPAALModelChecker/UDBM)、[utap](https://github.com/UPPAALModelChecker/utap)、[uppaal-libs](https://github.com/UPPAALModelChecker/uppaal-libs) 与官方文档站可作为对应工程线索 | [paper](./behrmann11-developing-uppaal-over-15-years/) |
| ⚡ | `bulychev11` | Distributed Parametric and Statistical Model Checking | 2011 | 大规模仿真、顺序检验和参数扫面会被单机时间拖住 | master/slave + batch/buffer + distributed parametric sweep | 把 `UPPAAL-SMC` 推到 cluster 并行与参数探索 | 🟩 | 🟧 | 当前可沿 [downloads](https://uppaal.org/downloads/) 与官方 SMC 文档追工具线，但 distributed/parametric 扩展源码未见公开 | [paper](./bulychev11-distributed-parametric-statistical-model-checking/) |
| ⚡ | `dllmpvw11` | Statistical Model Checking for Networks of Priced Timed Automata | 2011 | priced timed automata 缺少 statistical analysis | 对 `NPTA/PTA` 做 statistical model checking | 连接概率分析与代价分析 | 🟩 | 🟧 | 官方 SMC 文档、教程与工具线可用，但对应扩展核心源码未见公开 | [paper](./david11-smc-priced-timed-automata/) |
| ⚡ | `dllmw11` | Time for Statistical Model Checking of Real-time Systems | 2011 | 穷举验证难覆盖随机实时行为 | 将 `SMC` 引入 real-time systems | 奠定 `UPPAAL-SMC` 主线 | 🟩 | 🟧 | 官方 SMC 文档、教程与工具线可用，但核心源码未见公开 | [paper](./david11-statistical-model-checking-real-time/) |
| ⚡ | `bdllmp12` | Checking \& Distributing Statistical Model Checking | 2012 | `SMC` 计算规模受单机限制 | distributed statistical model checking | 扩大实验规模与算力利用 | 🟩 | 🟧 | 当前可沿官方 SMC 工具线追运行版本，但分布式扩展源码未见公开 | [paper](./bulychev12-distributed-statistical-model-checking/) |
| ⚡ | `bulychev12-smc` | UPPAAL-SMC: Statistical Model Checking for Priced Timed Automata | 2012 | `UPPAAL` 缺少覆盖随机、代价与混杂行为的统一统计模型检查工具线 | 给 `NPTA/PTA` 定义 stochastic race semantics，并支持 hypothesis testing、estimation/comparison、expected value 与 `WMTL<=` monitors | 把 `UPPAAL-SMC` 从分散能力推进成正式工具分支 | 🟩 | 🟧 | 官方 [SMC tutorial](https://uppaal.org/texts/uppaal-smc-tutorial.pdf) 与 [downloads](https://uppaal.org/downloads/) 可核验工具可用性，但主引擎源码未直接公开 | [paper](./bulychev12-uppaal-smc-priced-timed-automata/) |
| ⚡ | `david12-ecdar` | Compositional verification of real-time systems using Ecdar | 2012 | component verification 难以组合扩展 | `ECDAR` 中的 compositional verification 工具链 | 让组合验证可直接操作 | 🟩 | 🟢 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 直接对应 `ECDAR` 工具线 | [paper](./david12-compositional-verification-ecdar/) |
| ⚡ | `david12-shs` | Statistical Model Checking for Stochastic Hybrid Systems | 2012 | stochastic hybrid systems 难做穷举验证 | 把 `SMC` 扩到 stochastic hybrid semantics | 将 `SMC` 推向 hybrid systems | 🟩 | 🟧 | 当前能核到论文、SMC 工具线与教程，但论文对应 `SHS` 扩展源码未见公开 | [paper](./david12-statistical-model-checking-stochastic-hybrid-systems/) |
| ⚡ | `muniz12` | Timed Automata with Disjoint Activity | 2012 | 周期系统明明顺序活动却被并行组合制造大量 interleavings | `Active(A)`、sequentialisable、`·` 与 `#` 组合算子 | 把特定周期系统的验证复杂度从二次降到线性 | 🟩 | 🟧 | 当前未见 disjoint-activity 对应公开实现；可沿后续 `urgent POR` 论文与官方引擎线追踪 | [paper](./muniz12-timed-automata-with-disjoint-activity/) |
| ⚡ | `nyman10` | New Results on Timed Specifications | 2012 | 原有 `TIOA/ECDAR` 规格理论对 liveness、Büchi 目标与 non-Zeno 保证还不够 | 把 `SOTFTR` 推成 zone-based Büchi timed games，并与 safety 组合 | 让 `ECDAR` 能表达 liveness/non-Zeno contract | 🟩 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 提供该规范理论主线的开源实现入口 | [paper](./nyman10-new-results-on-timed-specifications/) |
| 🧱 | `david13-rtspec` | Real-time specifications | 2013 | specification theory 的规则和语义分散 | 系统整理 operators、闭包与工具语义 | 成为 `TIOA/ECDAR` 标准参考 | 🟩 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR)、[j-Ecdar](https://github.com/Ecdar/j-Ecdar)、[Reveaal](https://github.com/Ecdar/Reveaal) 构成对应实现主线 | [paper](./david13-real-time-specifications/) |
| ⚡ | `david14-gamestrategies` | Verification and Performance Evaluation of Timed Game Strategies | 2014 | `UPPAAL-TIGA` 能合成策略，但合成后缺少统一的后验证与性能评价流程 | 一条路把 zone-based strategy 翻译成 controller TA，另一条路把策略直接接入扩展后的 `MC/SMC` 引擎 | 把 synthesis、verification 与 performance evaluation 串成 `Control-SMC` 工作流 | 🟩 | 🟧 | 可沿 `TIGA / SMC / Stratego` 文献与官方下载入口追功能线，但论文对应策略评价实现未见公开源码 | [paper](./david14-verification-performance-evaluation-timed-game-strategies/) |
| ⚡ | `djlllst14` | On Time with Minimal Expected Cost! | 2014 | 不确定实时系统缺少 expected-cost 优化 | 把 expected-cost 查询接入 `SMC/optimization` | 为 `Stratego` 优化铺路 | 🟩 | 🟧 | 可沿 `SMC / Stratego` 工具线追可运行版本，但核心优化源码未见公开 | [paper](./david14-minimal-expected-cost/) |
| 🛠️ | `bogomolov15` | Co-Simulation of Hybrid Systems with SpaceEx and Uppaal | 2015 | `UPPAAL` 与 `SpaceEx` 原生语义和仿真内核不兼容，难以在一个统一工作流里联合运行 | 把两边模型导出为 `FMI` 的 `FMU`，再用满足 determinacy 的 co-simulation master algorithm 按步协同推进 | 把 `UPPAAL` 正式接入标准化异构协同仿真链路 | 🟩 | 🟧 | 论文给出 `FMI/FMU` 集成路线与宿主算法，但当前未见对应集成实现源码公开 | [paper](./bogomolov15-cosimulation-hybrid-systems-spaceex-uppaal/) |
| 🛠️ | `david15-smc` | Uppaal SMC tutorial | 2015 | `SMC` 查询语义与用法难掌握 | 教程化讲解 stochastic semantics 与 query patterns | 提供 `SMC` 工程使用入口 | 🟧 | 🟧 | 官方 [SMC tutorial](https://uppaal.org/texts/uppaal-smc-tutorial.pdf) 与 [downloads](https://uppaal.org/downloads/) 可得，但核心源码未公开 | [paper](./david15-uppaal-smc-tutorial/) |
| ⚡ | `djlmt15` | Uppaal Stratego | 2015 | 策略生成与优化缺少统一工具 | 支持 strategy generation/comparison/optimization | 策略优化分支工具化成形 | 🟧 | 🟧 | 官方文档与工具线可追，但 `Stratego` 核心源码未见公开 | [paper](./david15-uppaal-stratego/) |
| 🛠️ | `cassez17` | WUPPAAL: Computation of Worst-Case Execution-Time for Binary Programs with UPPAAL | 2017 | 二进制程序的 `WCET` 既受输入路径影响，又受 pipeline/cache 等复杂硬件时序影响，传统分析链难以既精确又通用 | 把程序运行抽象成带注释执行树，再用扩展版 `UPPAAL` 对“程序树 + 硬件 timed automata”做最长时间路径搜索 | 把 `UPPAAL` 式 `WCET` 分析推广成面向任意二进制语言和硬件的模块化框架 | 🟩 | 🟥 | 论文明确落到 `WUPPAAL` 工具链，但当前未见稳定公开源码仓库 | [paper](./cassez17-wuppaal-wcet-binary-programs-uppaal/) |
| 🛠️ | `nyman17-fmu` | Integrating Tools: Co-simulation in UPPAAL Using FMI-FMU | 2017 | 现有协同方案多把 `UPPAAL` 当外部 `FMU` 用，仍缺能让 `UPPAAL SMC` 直接吃进 `FMU` 并做统计时序分析的统一语义 | 扩展 `UPPAAL` 支持动态链接外部 `C` 库和 `FMI-FMU`，再把 master algorithm 编码成 timed automata | 把 `FMU` 真正内化为 `UPPAAL SMC` 可分析组件，打开 bounded `MITL` 统计验证入口 | 🟩 | 🟧 | 论文给出 `FMI-FMU` 内化与 `UPPAAL SMC` 语义路线，但对应集成实现源码未见公开 | [paper](./nyman17-integrating-tools-cosimulation-fmi-fmu/) |
| ⚡ | `nyman17` | Mutation-Based Test-Case Generation with Ecdar | 2017 | bounded SMT/BMC 变异测试慢且不自适应 | `Ecdar` unbounded refinement + strategy-driven adaptive testing | 更快生成 timed mutation tests，并减少 inconclusive | 🟩 | 🟨 | [ECDAR](https://github.com/Ecdar/ECDAR) 与 [Ecdar-test](https://github.com/Ecdar/Ecdar-test) 可追底座源码，但论文整体工作流源码未完整公开 | [paper](./nyman17-mutation-based-test-case-generation-ecdar/) |
| 🛠️ | `gundersen18` | Effortless Fault Localisation: Conformance Testing of Real-Time Systems in Ecdar | 2018 | `Ecdar` 若不能直接连接 conformance testing 与 fault localisation，工程落地仍不足 | 把 `MBMT`、refinement-based adaptive testing、primary fail、并行执行与 real/sim time 模式整合进新版 `Ecdar` IDE | 把 `Ecdar` 推进成建模、验证、测试、故障定位一体化平台 | 🟩 | 🟩 | [ECDAR](https://github.com/Ecdar/ECDAR)、[Ecdar-test](https://github.com/Ecdar/Ecdar-test) 与相关 org 仓库可直接追该工程线源码 | [paper](./gundersen18-effortless-fault-localisation-ecdar/) |
| ⚡ | `ashok19-sos` | SOS: Safe, Optimal and Small Strategies for Hybrid Markov Decision Processes | 2019 | hybrid MDP 策略难同时安全最优且紧凑 | safe optimal small strategy synthesis | 定题 compact strategy / hybrid MDP | 🟩 | 🟧 | 当前可核到论文与相关工具分支，但 `SOS` 对应源码未见公开 | [paper](./ashok19-sos-safe-optimal-small-strategies-hybrid-markov-decision-processes/) |
| ⚡ | `jensen19-mwlogic` | Model Checking and Synthesis for Branching Multi-Weighted Logics | 2019 | `UPPAAL` 相关优化/博弈模型常同时涉及时间、代价、能量等多资源，传统逻辑难同时表达 branching-time 与多资源硬约束 | 定义带多非负权重的 Kripke/game 结构与扩展 `CTL`，用 `cut` 与常数边界获得可判定模型检查，再把 reachability synthesis 编码成 dependency graph 的最小不动点问题 | 把多资源 branching-time 逻辑推进到有明确复杂度边界和 on-the-fly synthesis 算法的状态 | 🟩 | 🟥 | 当前未见论文对应的 branching multi-weighted model checker / synthesizer 公开源码 | [paper](./jensen19-model-checking-synthesis-branching-multi-weighted-logics/) |
| ⚡ | `larsen19-compact` | Synthesis of Safe, Optimal and Compact Strategies for Stochastic Hybrid Games (Invited Paper) | 2019 | stochastic hybrid games 需要 safe/optimal/compact controllers | 概括 compact strategy synthesis 路线 | 为 `SOS/Coshy` 线定型 | 🟨 | 🟧 | 当前能核到论文与官方 `Coshy` 线索，但对应策略合成源码未见公开 | [paper](./larsen19-synthesis-safe-optimal-compact-strategies-stochastic-hybrid-games/) |
| ⚡ | `lecoent19-tiga` | Guaranteed Control Synthesis for Continuous Systems in Uppaal Tiga | 2019 | `Uppaal Tiga` 擅长整数化 timed game，但直接离散连续系统会丢掉两次采样之间的安全保证 | 把 sampled switched system 的连续动力学用 set-based Euler tube 包进整数上下界函数，再让 `Tiga` 在这些安全包络上做策略合成 | 把 `Uppaal Tiga` 从离散近似控制推进到对连续系统有 guaranteed safety 的控制合成 | 🟩 | 🟧 | 当前可沿 `Tiga / Stratego` 功能线核验可运行能力，但论文级实现源码未见公开 | [paper](./lecoent19-guaranteed-control-synthesis-continuous-systems-uppaal-tiga/) |
| ⚡ | `kiviriga20-randref` | Randomized Refinement Checking of Timed I/O Automata | 2020 | symbolic refinement 检查扩展性不足 | randomized walk / falsification-style refinement | 提高 `TIOA` refinement 可扩展性 | 🟩 | 🟩 | 可沿 [ECDAR](https://github.com/Ecdar/ECDAR) 与 [Reveaal](https://github.com/Ecdar/Reveaal) 追 `TIOA` 检查实现主线 | [paper](./kiviriga20-randomized-refinement-checking-tioa/) |
| ⚡ | `muniz20` | Urgent Partial Order Reduction for Extended Timed Automata | 2020 | timed automata 长期难以直接套用经典 POR | 只在 zero-time urgent states 上做 stubborn-set reduction，并结合 zone 与读写分析 | 把 partial-order reduction 真正做进现代 `Uppaal` `XTA` 里 | 🟩 | 🟨 | 论文给出 reproducibility package `DEIS-Tools/upor`，但 `Uppaal` 主工具对应 feature 的完整源码快照未直接公开 | [paper](./muniz20-urgent-partial-order-reduction-extended-timed-automata/) |
| 🛠️ | `njor20` | Conformance Testing in UPPAAL: A diabolic approach | 2020 | conformance testing 仍主要依赖专门工具，尚未直接复用 `UPPAAL` verifier 主线 | 用 angelic/demonic completion、diabolic completion、kill-state reachability 与 `Yggdrasil` 把 non-conformance 改写成 `UPPAAL` reachability | 把 `UPPAAL` verifier 重新解释成 conformance checker 与 test-case generator | 🟩 | 🟥 | 论文提到基于 `UPPAAL` Java library 与 `Yggdrasil` 生成流程，但当前未见稳定公开源码仓库 | [paper](./njor20-conformance-testing-uppaal-diabolic-approach/) |
| ⚡ | `kiviriga21-randreach` | Randomized Reachability Analysis in Uppaal: Fast Error Detection in Timed Systems | 2021 | rare errors 难快速发现 | randomized reachability / fast falsification | 引入轻量 error-detection 工作流 | 🟩 | 🟧 | 当前可沿 [downloads](https://uppaal.org/downloads/) 与 [documentation](https://docs.uppaal.org/) 追工具能力，但 randomized reachability 主实现源码未见公开 | [paper](./kiviriga21-randomized-reachability-analysis-uppaal/) |
| ⚡ | `jensen22-mcts` | Monte Carlo Tree Search for Priced Timed Automata | 2022 | priced timed automata 规划搜索代价高 | `Monte Carlo Tree Search` | 把 planning search 接到 PTA 分析 | 🟨 | 🟧 | 当前未见论文对应 `MCTS` 扩展源码公开；至多能沿 [downloads](https://uppaal.org/downloads/) 追主工具可运行版本 | [paper](./jensen22-monte-carlo-tree-search-priced-timed-automata/) |
| 🧱 | `lu22` | Bounded DBM-based clock state construction for timed automata in Uppaal | 2022 | 在线恢复目标 `DBM` 状态时，直接回放历史会让恢复序列越跑越长 | `O-phase + C-phase` 的 bounded clock-state reconstruction | 把恢复序列长度压成只依赖时钟数的有界构造 | 🟢 | 🟢 | 论文明确给出 `Uppyyl simulator`、`uppyyl-state-constructor` 与实验仓库等 GitHub 入口 | [paper](./lu22-bounded-dbm-clock-state-construction-uppaal/) |
| ⚡ | `goorden23-tioa` | Timed I/O Automata: It is never too late to complete your timed specification theory | 2023 | 旧 `TIOA` 理论与实现仍不完整 | 补全证明并给出新开源实现 | 补齐新一代 `ECDAR` 规范线 | 🟢 | 🟢 | 论文明确指向开源 [ECDAR](https://github.com/Ecdar/ECDAR)；同 org 还有 [Reveaal](https://github.com/Ecdar/Reveaal) 与 [j-Ecdar](https://github.com/Ecdar/j-Ecdar) | [paper](./goorden23-timed-io-automata-never-too-late/) |
| ⚡ | `jensen23-dynext` | Dynamic Extrapolation in Extended Timed Automata | 2023 | extended timed automata 抽象过粗且开销高 | 面向 `XTA` 的 dynamic extrapolation | 收紧现代 `UPPAAL` 抽象精度 | 🟩 | 🟨 | 当前可拿到 [utap](https://github.com/UPPAALModelChecker/utap) / [UDBM](https://github.com/UPPAALModelChecker/UDBM) 等子库源码，但 dynamic extrapolation 主实现未公开 | [paper](./jensen23-dynamic-extrapolation-extended-timed-automata/) |
| ⚡ | `brorholt25-coshy` | Uppaal Coshy: Automatic Synthesis of Compact Shields for Hybrid Systems | 2025 | hybrid safety 需要自动 compact shields | automatic synthesis of compact shields | 把 `UPPAAL` 扩到 `Coshy` shielding | 🟨 | 🟧 | 官方 [features](https://uppaal.org/features/) 与 [changelog](https://uppaal.org/changelog/) 已出现 `COSHY` 线索，但当前未见对应源码仓库公开 | [paper](./brorholt25-uppaal-coshy/) |
| ⚡ | `jensen25` | On-The-Fly Symbolic Algorithm for Timed ATL with Abstractions | 2025 | 多方 timed game 上的 `TATL` 验证比 `TCTL/Tiga` 更强也更难，现有 symbolic 算法覆盖和效率都不够 | 用 `EADG` 编码 `TATL`，定义 `Forceable / Unavoidable` 值函数，把 inclusion checking 推广为 vertex merge，并进一步用 expansion abstraction 消掉 zone inclusion 检查 | 给出首个面向 `TATL` 的 on-the-fly symbolic `Uppaal` 算法，并把实现推进到显著快于朴素方法 | 🟢 | 🟢 | 论文提供 reproducibility package `10.5281/zenodo.15195408`，并说明功能将进入后续 `Uppaal` 发布线 | [paper](./jensen25-on-the-fly-symbolic-algorithm-timed-atl-abstractions/) |
| ⚡ | `muniz24` | GPU Accelerating Statistical Model Checking for Extended Timed Automata | 2025 | `NSXTA` 的 `SMC` 在 CPU/cluster 上时间和能耗成本都高 | CUDA `SMAcc` + JIT/Polish notation/weakest preconditions/shared memory | 把 `UPPAAL` 风格 `SMC` 推到 GPU 平台 | 🟩 | 🟨 | 论文明确有 `SMAcc` prototype，但未像 `lu22` 那样稳定给出完整公开仓库；当前更接近部分实现线索可追 | [paper](./muniz24-gpu-accelerating-smc-extended-timed-automata/) |
## 与应用文库的关系

当前 `UPPAAL` 应用与案例条目不再在本技术总账中占位，而是统一迁移到 [uppaal_apps/SUMMARY.md](../uppaal_apps/SUMMARY.md) 单独维护。

分流原则如下：

1. 若主贡献是 `UPPAAL` 本体的新能力、新抽象、新算法、新工程组件，保留在本文件。
2. 若主贡献是利用 `UPPAAL` 验证具体系统、协议、控制器或工业对象，转入应用文库。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-30 | 新增 **5** 篇 `2015-2019` 的核心技术/扩展条目，补入 `FMI-FMU co-simulation / WUPPAAL WCET / guaranteed continuous-system synthesis / branching multi-weighted logics` 主线，并把 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 回填到 **70** 篇口径 | 只把 `PDF` 实际下载成功且已生成 `paper_content.txt` 的条目正式入账；本轮新增顶层条目全部同步补齐 `bibtex.bib + desc.md`，并按统一双维状态口径回填统计与论文表 | 把原本偏薄的 `2015-2019` 段推进成包含异构协同、二进制时序分析、连续控制与多资源逻辑的过渡阶段 |
| 2026-03-30 | 新增 **10** 篇 `2004-2025` 的核心技术/扩展条目，补入 `time-optimal testing / priced timed games / CORA scheduling / adaptive testing / discount-optimality / UPPAAL-SMC formalization / strategy evaluation / ECDAR fault localisation / UPPAAL-native conformance / TATL` 主线，并把 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 全部回填到 **65** 篇口径 | 只把 `PDF` 实际下载成功且已生成 `paper_content.txt` 的条目正式入账；所有新增顶层条目同步补齐 `bibtex.bib + desc.md`，并按“内容详细程度 + 实现可获取程度”双维口径统一重判；统一论文表同时校正为全局按年份升序、同年按 `Key` 稳定排序 | 把文库从“核心骨架 + 近年抽象优化”推进成同时覆盖 testing、priced/game、SMC、conformance 与 `TATL` 新算法的更完整技术时间线 |
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
| 2026-03-29 | 修正 [ad90-timed-automata/desc.md](./ad90-timed-automata/desc.md) 的 GitHub 数学渲染兼容性问题，并把限制回写到 [DESC_GUIDE.md](./DESC_GUIDE.md) 与仓库级 [AGENTS.md](../../AGENTS.md) | 去掉 `\left / \right / \operatorname` 等已知易炸宏，把展示公式统一改成单行公式体；同时把“不用哪些宏、用什么替代”写成后续单篇整理的硬规则 | 让后续 `UPPAAL` 文库里的形式化公式既保留精度，又能稳定在 GitHub 页面直接渲染 |
| 2026-03-29 | 为仓库级 [AGENTS.md](../../AGENTS.md) / `CLAUDE.md` 补充 GitHub 友好的数学公式写法规范，并把 [DESC_GUIDE.md](./DESC_GUIDE.md) 与 [ad90-timed-automata/desc.md](./ad90-timed-automata/desc.md) 改成 `$...$ / $$...$$` 口径 | 明确规定行内公式用 `$...$`，展示公式必须写成“`$$` + 恰好一行公式体 + `$$`”，避免多行块公式导致 GitHub 渲染异常；同时把 `ad90` 中关键定义、构造和判定问题改写为单行公式块 | 让后续 `desc.md` 在保留形式化精度的同时，仍能稳定在 GitHub 上直接渲染和阅读 |
| 2026-03-29 | 批量补齐其余 **44** 个顶层条目的 `desc.md`，使顶层条目达到 **45/45** 首轮 `desc` 覆盖，并同步回写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 的维护口径 | 新增条目不变，只补单篇展开版说明；统一按 [DESC_GUIDE.md](./DESC_GUIDE.md) 写出“问题 / 方法 / 解决点”三条开头简述，并补一轮 `论文定位 / 立足问题 / 核心方法 / 解决了什么问题 / 实现与材料 / 对本研究的启发` 结构 | 让当前 `uppaal_tech/` 不再只有总表摘要，而是对每个顶层条目都有可继续深化的单篇入口，同时把“未来新增顶层条目默认同步补 desc”固定下来 |
| 2026-03-29 | 新增 **10** 篇 `2004-2025` 的核心技术/扩展条目，补入 `symmetry reduction / UPPAAL PORT / ECDAR environment / distributed SMC / Büchi timed specifications / mutation-based testing / urgent POR / bounded DBM reconstruction / GPU-SMC` 主线，并把 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 全部回填到 **55** 篇口径 | 只把 `PDF` 实际下载成功且已生成 `paper_content.txt` 的条目正式入账；所有新增顶层条目同步补齐 `desc.md`，并按“内容详细程度 + 实现可获取程度”双维口径统一重判；同时补齐 `bulychev11` 缺失的 `year` 元数据以保证后续统计稳定 | 把文库从“早期骨架 + 近年抽象优化”推进成同时覆盖结构压缩、组件工程、规范理论、分布式与异构 `SMC`、现代 `POR` 的完整技术时间线 |

## 失败与阻塞记录

| Key | 标题 | 状态 | 原因 | 后续建议 |
|---|---|---|---|---|
| `rokicki93` | Representing and Modeling Digital Circuits | 本轮未纳入 | 当前未取得合法可用全文 PDF，且与 `UPPAAL` 论文集的直接关系更偏 DBM 历史引用背景，暂不作为正式条目入库 | 若后续找到合法全文且能明确其在 `UPPAAL/DBM` 技术链中的稳定价值，再单独复核是否纳入 |
| `importance-splitting-line` | `UPPAAL SMC` 的 importance splitting / importance sampling 候选条目 | 待补证 | 已定位到论文线索，但暂未取得稳定可下载 PDF，因此未正式入账 | 下轮优先从 `Kim Guldstrand Larsen / Marius Mikucionis / Axel Legay + importance splitting` 继续检索 |
| `ocr-runtime` | `OCR` 提取运行时依赖 | 环境阻塞 | 当前环境缺少系统级 `tesseract`，因此 `amnell01`、`hune01`、`mikucionis10` 暂用 `pdftotext -layout` 回填 `paper_content.txt` | 后续若进入单篇深读且文本质量仍不足，应在具备 `tesseract` 的环境重新用 `tools/pdf_extractor.py -m ocr` 抽取 |
