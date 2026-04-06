# PRISM-games：随机多玩家博弈模型检查器 / PRISM-games: A Model Checker for Stochastic Multi-Player Games

## 基本信息

- 标题：PRISM-games: A Model Checker for Stochastic Multi-Player Games
- 中文标题：PRISM-games：随机多玩家博弈模型检查器
- 作者：Taolue Chen，Vojtech Forejt，Marta Kwiatkowska，David Parker，Aistis Simaitis
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 185-191，2013
- DOI：`10.1007/978-3-642-36742-7_13`
- 链接：https://doi.org/10.1007/978-3-642-36742-7_13
- 形式主义：`SMG / PRISM-games / rPATL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：随机多玩家博弈的建模、验证与策略综合平台
- 工具/实现获取方式：原文直接给出 `PRISM-games` 网站 `http://www.prismmodelchecker.org/games/`，并说明其建立在 `PRISM` 代码库之上。
- 标准/格式获取方式：模型承载是扩展后的 `PRISM` guarded-command 语言，性质承载是 `rPATL`，策略可导出、导入并与原模型做产品化分析。

## 简报

这篇论文补的是 `PRISM` 家族里“多玩家、博弈、联盟和策略综合”这一支的明确平台位点。它把原本偏 `DTMC/MDP/PTA` 的单系统分析扩到 stochastic multi-player games，让用户不只问“性质是否成立”，还可以问“哪一方如何出策略，才能保证概率或收益界限成立”。

- 形式主义定位：`SMG` 的工具平台与属性语言基础设施，而不是新的博弈理论母文。
- 构造方式简述：用户用扩展的 `PRISM` 模型语言描述玩家、模块和概率迁移，再用 `rPATL` 写 coalition probability / reward 属性，由工具做验证与策略综合。
- 基础设施与场景简述：依托 `PRISM` 编辑器、模拟器、`rPATL` 算法和策略导出/回灌机制，适合协议、分布式协作/对抗和带收益指标的随机交互系统。

```text
guarded-command SMG -> rPATL property -> coalition-game reduction -> verification / strategy synthesis -> strategy-guided re-verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. turn-based stochastic multi-player game (`SMG`)。
2. player、state、probabilistic transition 与 strategy。
3. `rPATL` 性质语言。
4. strategy synthesis、strategy export/import 与 strategy implementation。
5. 基于 coalition game 的模型检查算法。

### 核心抽象

论文用自然语言定义 `SMG`，可保守整理为：

$$
G = (\Pi, S, turn, Act, \Delta, AP, L)
$$

上式中的符号逐项解释如下：

1. `\Pi` 是玩家集合。
2. `S` 是有限状态集合。
3. `turn:S \to \Pi` 指出每个状态由哪一名玩家控制。
4. `Act` 是各玩家可选动作或可触发迁移的集合。
5. `\Delta` 是概率迁移关系。
6. `AP` 和 `L` 分别是原子命题集合与状态标注。
7. 这组符号是依据论文对 turn-based SMG 的文字描述做的保守归纳。

论文直接给出了 `rPATL` 的核心语法：

$$
\varphi ::= \top \mid a \mid \neg \varphi \mid \varphi \land \varphi \mid \langle\langle C\rangle\rangle P_{\bowtie q}[\psi] \mid \langle\langle C\rangle\rangle R^r_{\bowtie x}[F^\star \varphi]
$$

$$
\psi ::= X\varphi \mid \varphi U \varphi \mid \varphi U^{\le k} \varphi \mid F\varphi \mid F^{\le k}\varphi \mid G\varphi \mid G^{\le k}\varphi
$$

上式中的符号逐项解释如下：

1. `C` 是 coalition，也就是玩家子集。
2. `P_{\bowtie q}` 表示概率约束。
3. `R^r_{\bowtie x}` 表示基于 reward structure `r` 的收益约束。
4. `F^\star` 表示 reachability 风格的奖励累计方式。
5. `X/U/F/G` 分别是 next、until、eventually、globally。
6. `k` 是步数上界。
7. 这些都是论文正文直接给出的 `rPATL` 语法骨架。

论文给出的示例性质也非常典型：

$$
\langle\langle \{1,2\} \rangle\rangle P_{\ge 0.75}[F^{\le 5}\ goal]
$$

上式中的符号逐项解释如下：

1. 玩家 `1` 与 `2` 组成联盟。
2. `F^{\le 5}\ goal` 表示在 `5` 步内最终到达 `goal`。
3. `P_{\ge 0.75}` 表示联盟要保证该事件概率至少为 `0.75`。
4. 这正是论文直接解释的例子。

### 一个最小例子与通俗解释

论文里的 futures market investor 模型就很适合做最小直觉例子：

1. 玩家有两个投资者和一个市场。
2. 投资者决定 invest / noinvest，市场决定是否 bar 某个投资者。
3. 股价按概率过程波动。
4. 于是我们不只问“最终会不会赚钱”，而是问“某个联盟有没有策略，能把收益或目标达成概率压到指定阈值以上”。

通俗地说，`PRISM-games` 把“随机系统验证”推进到“有多个参与方、他们可以合作或对抗、还要显式算策略”的层次。

### 运行 / 接受 / 转移语义

运行语义的关键点是：

1. 当前状态只允许一个玩家做选择，因此是 turn-based。
2. 该玩家从可用的概率迁移里选动作，随后按迁移分布进入下一状态。
3. 若写 `rPATL` 性质，工具先把联盟和其余玩家压成一个两方 coalition game，再做求值。
4. 若需要，还能把已综合的策略与原游戏做产品，继续验证其他性质。

### 语义边界

当前平台的边界也明确写在论文里：

1. 只支持 turn-based、perfect-information 的 `SMG`。
2. 对 concurrent games 和 partial information 只留作未来工作。
3. 对某些 reward 精确值性质，最优策略不是 memoryless，需要构造有限记忆随机更新策略。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `SMG` 骨架 | `$G = (\Pi, S, turn, Act, \Delta, AP, L)$` | 博弈模型是“玩家控制状态 + 概率迁移”的离散系统。 |
| 联盟概率性质 | `$\langle\langle C\rangle\rangle P_{\bowtie q}[\psi]$` | 询问联盟能否保证某个概率界。 |
| 联盟收益性质 | `$\langle\langle C\rangle\rangle R^r_{\bowtie x}[F^\star \varphi]$` | 询问联盟能否保证某种累计收益界。 |
| 示例性质 | `$\langle\langle \{1,2\} \rangle\rangle P_{\ge 0.75}[F^{\le 5}\ goal]$` | 玩家 `1` 和 `2` 合作保证 5 步内达成目标的概率下界。 |
| 策略类型 | `memoryless / finite-memory / finite-memory stochastic-update` | 工具支持多种综合结果承载方式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `SMG` 仍然是显式离散状态模型。 |
| 事件 / 触发 | 强支持 | guarded commands 与动作标签决定可发迁移。 |
| 守卫 / 数据 | 中等支持 | 依赖扩展 `PRISM` 语言的变量和 guard。 |
| 层次 | 不突出 | 重点不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 模块可同步，但论文主轴是多玩家控制而非层次并发语义。 |
| 时间约束 | 弱支持 | 本文主角是 `SMG`，不是实时博弈。 |
| 连续动态 / 随机性 | 很强 | 概率迁移和 reward 是核心。 |
| 可执行 / 可验证性 | 很强 | 有 GUI、simulator、strategy export/import 和 property re-check。 |

### 形式化问题与性质

1. `PRISM-games` 补的是“模型 + 属性 + 策略综合 + 策略后再验证”的闭环。
2. `rPATL` 是它的关键接口层，因为它把 coalition、概率和 reward 合在一起。
3. coalition-game reduction 说明工具底层仍把多玩家问题收束为更经典的两方博弈求解。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用扩展 `PRISM` 语言写模块、变量、guarded commands 和玩家归属。
2. 用 `rPATL` 写 coalition probability / reward 性质。
3. 运行模型检查并综合策略。
4. 导出、导入或实现该策略，再做后续验证。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 扩展的 `PRISM` guarded-command 模型；
2. `rPATL` 性质；
3. strategy 文件；
4. strategy product 后的新模型。

### 交换与互操作

这篇论文的互操作重点在于：

1. 直接复用 `PRISM` 既有 GUI 和 simulator。
2. 通过 strategy implementation，把“综合出的控制策略”转回模型级对象。
3. 在策略固定后对其他性质继续验证。

## 配套基础设施

- 建模/编辑工具：沿用 `PRISM` 图形界面和文本编辑体验。
- 解析/交换/元模型支持：扩展的 `PRISM` 语言、`rPATL`、策略文件导入导出。
- 仿真/执行支持：原文明确说明复用 `PRISM` simulator，并支持手动分析策略。
- 验证/分析支持：`rPATL` 模型检查、strategy synthesis、strategy-guided re-verification。
- 代码生成/转换支持：核心是 strategy-product 构造，而不是部署代码生成。
- 标准化或社区生态：依附 `PRISM` 生态与 `PRISM-games` 网站。

## 适用场景与需求前提

### 适用场景

适合安全协议、分布式协商、自治体协作/对抗、收益优化和多代理策略分析等场景。

### 需求前提

1. 系统能被抽成有限 turn-based stochastic game。
2. 需求关心 coalition 的概率/收益保证，而不是单体系统性质。
3. 玩家可见信息足以采用 perfect-information 语义。

### 不适用或高成本场景

若系统核心是连续物理过程、部分可观测博弈或真正并发出招的 game，这个版本的 `PRISM-games` 就不是最合适入口。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM 4.0` 是概率实时平台，而这里把平台外延到 multi-player games；相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，`Modest` 更像 umbrella 平台，而 `PRISM-games` 更聚焦 `SMG + rPATL + strategy`；相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，`Momba` 偏工作流层，而这里是具体博弈分析后端。

## 与本研究的关系

### 对 Project 1 的价值

它把状态机族谱系往“多参与方博弈化验证”方向扩了一步。若后续模型不再是单控制器，而是环境、系统和攻击者/协作者共同演化，那么这类平台就很关键。

### 作为目标形式主义还是中间表示

更像特定分析能力很强的后端平台，而不是统一中间表示。

### 对需求到模型生成的启发

1. 需求里若明确出现多个主体的合作/对抗目标，单一 `FSM/MDP` 往往不够。
2. 生成模型时需要保留 player ownership、reward structure 和 coalition 语义。
3. 验证结果不应只停留在 true/false，策略对象本身也应成为可回灌工件。

### 现实限制

它的表达力建立在博弈结构可有限化、玩家可见且 turn-based 的前提之上。

## 重要的相关工作

1. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：`PRISM` 概率实时平台锚点。
2. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：定量建模与验证平台。
3. [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)：`JANI` 与多后端工作流入口。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 归类理由：主贡献是 `SMG` 的建模、`rPATL` 验证和策略综合平台基础设施，而不是新的博弈母型定义论文。
