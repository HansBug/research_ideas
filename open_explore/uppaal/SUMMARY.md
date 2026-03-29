# UPPAAL Collection Summary

本文件是 `open_explore/uppaal/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 谱系论文、分类分布、更新状态和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集的定位、边界和单论文目录要求。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、回填和一致性检查规范。
3. 再使用本文件查看当前统计、分类分布、论文清单和失败记录。
4. 若后续开始补单篇深度分析，再进入具体论文目录处理 `bibtex.bib`、`paper_content.txt` 与 `paper.pdf`。

## 收录边界回顾

为避免后续维护时误把 `uppaal/` 写成泛 timed automata 收藏夹，这里重申当前论文集的边界：

1. 优先收录 `UPPAAL` 本体、核心理论基础、关键算法/数据结构、扩展能力和代表性应用工作。
2. 历史前驱理论可以收录，但必须能清楚说明它与 `UPPAAL` / UDBM 技术脉络的直接关系。
3. 只在参考文献里提到 `UPPAAL`、正文没有实质贡献的论文，不应正式入账。

## 贡献类型 Emoji 口径

| Emoji | 类型 | 说明 |
|---|---|---|
| 🧱 | 核心算法/数据结构 | timed automata 语义、DBM、zone、symbolic state、核心验证算法 |
| ⚡ | 改进与扩展 | 抽象优化、状态空间削减、优先级、priced/strategy/statistical 等扩展 |
| 🛠️ | 工程/工具链 | 工具架构、建模语言、查询语言、教程、建模模式、用户指南 |
| 🧪 | 应用与案例 | 基于 `UPPAAL` 的具体系统、协议、软件或工业验证案例 |

## 检索关键词簇

### 当前推荐关键词簇

- `UPPAAL + timed automata + DBM/zone/federation/symbolic state`
- `UPPAAL + tutorial/user guide/modeling patterns/query language/verifyta`
- `UPPAAL + abstraction/extrapolation/priced/statistical/strategy/priority/reduction`
- `UPPAAL + case study/industrial/application` 再叠加具体系统或领域名

### 已观察到的高命中特征

- 标题直接出现 `UPPAAL`、`DBM`、`zone`、`difference bound matrix`、`tutorial`、`toolbox`
- 作者脉络与 `UPPAAL` 核心团队稳定重合，且正文直接讨论引擎、语言或案例
- 题目同时点出 `case study`、`industrial`、具体系统名与 `UPPAAL` 时，通常更值得补入 `🧪`
- thesis/教程类条目往往能同时补足技术脉络与工程语境

### 已观察到的低命中特征

- 只写 timed automata 或 real-time verification，但正文没有 `UPPAAL` 明确关联
- 只在 related work 里顺带提一次 `UPPAAL` 的应用论文
- 纯包装层、零散使用说明或无正式引用信息的材料
- 历史背景论文如果没有被 `UPPAAL` 技术线稳定引用，应谨慎纳入

### 检索倾向调整

- 下一轮应优先补 `🧪 应用与案例`，避免长期只收引擎和理论条目
- `⚡` 改进与扩展值得继续沿 `priced`、`strategy`、`statistical`、`game` 等分支扩张
- 官方作者、官方教程和代表性 case study 优先级高于泛背景论文
- 每次更新前先删减失效关键词，保持本节简洁

## 当前收录统计

- 已收录论文：**11** 篇
- 本轮新增论文：**11** 篇
- 基础材料齐全（`paper.pdf + bibtex.bib + paper_content.txt`）：**11** 篇
- 直接复用现成 `content.md` 作为 `paper_content.txt`：**9** 篇
- 使用 `tools/pdf_extractor.py` 补提取 `paper_content.txt`：**2** 篇
- 已完成单篇深度分析：**0** 篇
- 待补单篇深度分析：**11** 篇
- 本轮未纳入/待补证条目：**1** 条
- 含内嵌 `paper-*` 子目录的 thesis/合集条目：**2** 篇

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

### 🧱 核心算法/数据结构

| Key | 标题 | 年份 | 内容一句话简介 | 材料状态 | 目录 |
|---|---|---:|---|---|---|
| `ad90` | Automata for Modeling Real-Time Systems | 1990 | timed automata 语义源头，定义了后来 `UPPAAL` 持续依赖的 clocks / guards / resets 基本模型 | 🟢 基础材料齐全 | [ad90-timed-automata](./ad90-timed-automata/) |
| `dill89` | Timing Assumptions and Verification of Finite-State Concurrent Systems | 1990 | dense-time symbolic verification 的历史前驱，为后续 clock-constraint 表示提供早期语义线索 | 🟢 基础材料齐全 | [dill89-timing-assumptions](./dill89-timing-assumptions/) |
| `lpw95` | Model-Checking for Real-Time Systems | 1995 | 早期 `UPPAAL` symbolic model checking 的奠基论文，解释为何约束求解和状态空间搜索成为引擎核心 | 🟢 基础材料齐全 | [lpw95-real-time-model-checking](./lpw95-real-time-model-checking/) |
| `llpy97` | Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction | 1997 | 聚焦紧凑 DBM 存储与状态空间削减，是 UDBM `mingraph` 一线的重要理论来源 | 🟢 基础材料齐全 | [llpy97-compact-data-structure](./llpy97-compact-data-structure/) |
| `bengtsson02` | Clocks, DBMs and States in Timed Systems | 2002 | thesis 级系统总结 DBM 操作、normalization、存储与实现，是理解 UDBM 内核的关键入口；含 `paper-a` 到 `paper-e` 子目录导航 | 🟢 基础材料齐全 | [bengtsson02-clocks-dbms-states](./bengtsson02-clocks-dbms-states/) |
| `by04` | Timed Automata: Semantics, Algorithms and Tools | 2004 | 汇总 timed automata 的语义、算法与工具视角，为 `UPPAAL` 技术线提供紧凑总览 | 🟢 基础材料齐全 | [by04-semantics-algorithms-tools](./by04-semantics-algorithms-tools/) |

### ⚡ 改进与扩展

| Key | 标题 | 年份 | 内容一句话简介 | 材料状态 | 目录 |
|---|---|---:|---|---|---|
| `behrmann03` | Data Structures and Algorithms for the Analysis of Real Time Systems | 2003 | 从更高层综合说明 unions of zones、CDD、priced 方向与 `UPPAAL` 周边数据结构演进；含 `paper-intro` 与 `paper-a` 到 `paper-f` 子目录导航 | 🟢 基础材料齐全 | [behrmann03-real-time-data-structures](./behrmann03-real-time-data-structures/) |
| `bblp04` | Lower and Upper Bounds in Zone Based Abstractions of Timed Automata | 2004 | 讨论 zone abstraction 的上下界外推，是 `extrapolation` 能力链上的关键条目 | 🟢 基础材料齐全 | [bblp04-zone-based-abstractions](./bblp04-zone-based-abstractions/) |
| `dhlp06` | Model Checking Timed Automata with Priorities Using DBM Subtraction | 2006 | 以 DBM subtraction 支撑优先级 timed automata 分析，直接连接 federation 与差集操作需求 | 🟢 基础材料齐全 | [dhlp06-dbm-subtraction](./dhlp06-dbm-subtraction/) |

### 🛠️ 工程/工具链

| Key | 标题 | 年份 | 内容一句话简介 | 材料状态 | 目录 |
|---|---|---:|---|---|---|
| `lpy97` | UPPAAL in a Nutshell | 1997 | 早期 `UPPAAL` toolbox 总览，覆盖描述语言、模拟器、模型检查器和用户工作流 | 🟢 基础材料齐全 | [lpy97-uppaal-nutshell](./lpy97-uppaal-nutshell/) |
| `bdl04` | A Tutorial on Uppaal | 2004 | 面向建模语言、查询语言、工具界面和模式的系统教程，是工程使用入口文献 | 🟢 基础材料齐全 | [bdl04-uppaal-tutorial](./bdl04-uppaal-tutorial/) |

### 🧪 应用与案例

当前尚无正式入账条目。后续应优先补充来自官方团队、核心作者或高质量学术工作中的代表性 `UPPAAL` 应用案例。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal/`，新增 **11** 篇基础条目，并建立 `README.md`、`GUIDE.md`、`SUMMARY.md` 三个论文集核心文件；随后补入 `behrmann03` 与 `bengtsson02` 的 `paper-*` 子目录及父子导航 README | 只从既有 `UPPAAL/UDBM` 历史论文池挑选一份可用副本，优先完成基础入库，不额外扩新论文；有现成 `content.md` 的直接规范为 `paper_content.txt`，缺失 thesis 级正文的条目用 `tools/pdf_extractor.py` 补齐；对 thesis 型条目把原有拆分子论文与 `content_assets/` 一并带入 | 先搭建 `UPPAAL` 基础文库骨架，再补齐带内嵌子论文条目的父子导航结构，为后续沿专题继续深挖做准备 |

## 失败与阻塞记录

| Key | 标题 | 状态 | 原因 | 后续建议 |
|---|---|---|---|---|
| `rokicki93` | Representing and Modeling Digital Circuits | 本轮未纳入 | 当前未取得合法可用全文 PDF，且与 `UPPAAL` 论文集的直接关系更偏 DBM 历史引用背景，暂不作为正式条目入库 | 若后续找到合法全文且能明确其在 `UPPAAL/DBM` 技术链中的稳定价值，再单独复核是否纳入 |
