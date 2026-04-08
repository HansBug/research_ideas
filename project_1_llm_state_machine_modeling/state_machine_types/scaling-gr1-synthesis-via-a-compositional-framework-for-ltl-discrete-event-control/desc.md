# 通过组合式框架扩展 GR(1) 综合用于 LTL 离散事件控制 / Scaling GR(1) Synthesis via a Compositional Framework for LTL Discrete Event Control

## 基本信息

- 标题：Scaling GR(1) Synthesis via a Compositional Framework for LTL Discrete Event Control
- 中文标题：通过组合式框架扩展 GR(1) 综合用于 LTL 离散事件控制
- 作者：Hernan Gagliardi, Victor Braberman, Sebastian Uchitel
- 发表：*Computer Aided Verification*, pp. 201-223, 2025
- DOI：`10.1007/978-3-031-98685-7_10`
- 链接：https://doi.org/10.1007/978-3-031-98685-7_10
- 形式主义：`LTS / GR(1) discrete event control / MTSA compositional synthesis`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：面向模块化离散事件系统的组合式 `GR(1)` 控制器综合方法
- 工具/实现获取方式：论文明确说明方法已实现到 `MTSA`，并以其显式状态 `GR(1)` 综合引擎为基础开展实验。
- 标准/格式获取方式：主承载是 labelled transition systems (`LTS`) 形式的模块化 plant、controllable / uncontrollable events、`GR(1)` 目标和 `MTSA` 中的组合式综合工件；不是独立交换标准。

## 简报

这篇论文补的是 reactive synthesis 和 DES supervisory control 之间很实用的一条桥。作者并不把整个模块化 plant 先完全并起来再做单体综合，而是迭代地挑选 plant 的子集、先求一个 weaker goal 下的 maximally permissive safe controller，再把受控子系统做等价压缩后回填，最后得到一组可并行运行的控制器。它的意义在于：`GR(1)` 这类通常被看作“逻辑综合后端”的东西，被真正拉进了模块化离散事件控制工作流。

- 形式主义定位：模块化 `LTS` 控制问题上的 `GR(1)` 综合方法路线，而不是新的语言或工具平台本体。
- 构造方式简述：`modular plant LTSs -> partial safe synthesis -> observational-equivalence quotient -> final live controller set`。
- 基础设施与场景简述：依托 `LTS`、`GR(1)`、controllable/uncontrollable events、synthesis observation equivalence 和 `MTSA`，适合大规模模块化离散事件控制。

```text
modular plant LTSs -> subset safe synthesis -> quotient / abstraction -> compositional controller set -> parallel control of original plant
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 作为 plant 模块的 labelled transition systems (`LTS`)。
2. controllable / uncontrollable event 分区。
3. `GR(1)` 形式的 `LTL` 控制目标。
4. legal controller、winning states、safe controller 和 live controller。
5. synthesis observation equivalence 与 quotient LTS。

### 核心抽象

论文首先把离散事件系统写成：

$$
M = (S, \Sigma, \to, \hat{s})
$$

上式中的符号逐项解释如下：

1. `$S$` 是有限状态集合。
2. `$\Sigma$` 是事件标签集合。
3. `$\to \subseteq S \times \Sigma \times S$` 是转移关系。
4. `$\hat{s}$` 是初始状态。

两个模块的并行组合写成：

$$
M_1 \parallel M_2 = (S_1 \times S_2, \Sigma_1 \cup \Sigma_2, \to_{1\parallel2}, (\hat{s}_1,\hat{s}_2))
$$

上式中的符号逐项解释如下：

1. `$S_1 \times S_2$` 是组合状态空间。
2. 共享事件需要同步发生，局部事件各自独立推进。
3. 这正是 modular DES control 中导致状态爆炸的来源。

控制问题定义为：

$$
E = \langle M, \Sigma_c, \varphi \rangle
$$

上式中的符号逐项解释如下：

1. `$M$` 是 plant 的模块集合或其组合语义。
2. `$\Sigma_c \subseteq \Sigma$` 是 controllable events。
3. `$\Sigma_u = \Sigma \setminus \Sigma_c$` 是 uncontrollable events。
4. `$\varphi$` 是控制目标，论文聚焦其 `GR(1)` 片段。

论文给出的 `GR(1)` 结构是：

$$
\varphi = \bigwedge_{i \in n}\Box\Diamond \phi_i \Rightarrow \bigwedge_{j \in m}\Box\Diamond \gamma_j
$$

上式中的符号逐项解释如下：

1. `$\phi_i$` 是环境侧 recurrence assumptions。
2. `$\gamma_j$` 是系统侧 recurrence guarantees。
3. 整体仍属于 `LTL`，但限制在 `GR(1)` 这一工程上可解的子片段。

对解的条件，论文要求 controller `C` 至少满足：

$$
C \text{ is legal for } M \land M \parallel C \text{ is deadlock-free} \land \forall \pi \in Traces_\omega(M\parallel C).\ \pi \models \varphi
$$

上式中的符号逐项解释如下：

1. `legal` 表示 controller 不得禁掉 plant 可发生的 uncontrollable events。
2. `deadlock-free` 表示闭环系统不能被控制器卡死。
3. `Traces_\omega` 是无限 traces 集合。
4. `$\pi \models \varphi$` 表示每条闭环无限行为都满足目标。

### 一个最小例子与通俗解释

可以把它理解成若干个相互交互的离散控制模块：

1. 每个模块都是一个 `LTS`，有本地事件和共享事件。
2. 如果先把全部模块做笛卡尔积，状态空间会迅速爆炸。
3. 论文的做法是先挑一个子集，只对这个子集求一个 safe controller。
4. 然后把这个受控子集压缩成更小的代表对象，再继续和其他模块组合。

通俗地说，这像“边合成控制器，边把已经管住的那部分 plant 重新打包变小”。因此最终不是得到一个巨大 monolithic controller，而是一组可以并行运行的控制器。

### 运行 / 接受 / 转移语义

论文的方法链可保守写成：

$$
\langle M,\Sigma_c,\varphi\rangle \xrightarrow{\mathrm{partial\ safe\ synthesis}} (M',C_{safe}) \xrightarrow{\mathrm{quotient}} \cdots \xrightarrow{\mathrm{final\ live\ step}} \{C_1,\ldots,C_k\}
$$

上式中的符号逐项解释如下：

1. 初始输入是模块化 control problem。
2. `partial safe synthesis` 先在 weaker goal 下求 safe controllers。
3. `quotient` 使用 synthesis observation equivalence 隐去局部事件并缩小子系统。
4. 最后一步补 live controller，得到并行控制器集合。

论文特别强调：由于一般 `GR(1)` control problems 不一定存在 maximally permissive solution，因此 safe controller 和 live controller 被刻意拆成两步。

### 语义边界

1. 论文处理的是模块化离散事件控制，不是 dense-time 或连续控制。
2. 前提对象是 deterministic `LTS` plant，而不是富数据程序或图形 DSL。
3. 目标公式限制在 `GR(1)` 片段。
4. 组合式优势来自 plant 的模块结构；如果模型天然是单体，收益会变小。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTS` 骨架 | `$M=(S,\Sigma,\to,\hat{s})$` | 每个 plant 模块的基本对象。 |
| 并行组合 | `$M_1 \parallel M_2$` | 模块化 plant 的组合语义来源。 |
| 控制问题 | `$E=\langle M,\Sigma_c,\varphi\rangle$` | 论文统一讨论的合成对象。 |
| `GR(1)` 结构 | `$\bigwedge \Box\Diamond \phi_i \Rightarrow \bigwedge \Box\Diamond \gamma_j$` | 可工程求解的 `LTL` 子片段。 |
| 解条件 | `$C$ legal, $M\parallel C$ deadlock-free, $\forall \pi.\ \pi\models\varphi$` | controller 被接受的最小标准。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 基础对象就是离散 `LTS` 状态机。 |
| 事件 / 触发 | 很强 | controllable / uncontrollable events 是主角。 |
| 守卫 / 数据 | 弱支持 | 主线在事件控制与逻辑目标，不在富数据守卫。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 很强 | 模块并行组合与共享事件同步是问题核心。 |
| 时间约束 | 不支持 | 不是 timed synthesis。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic 控制线。 |
| 可执行 / 可验证性 | 很强 | 已在 `MTSA` 中实现，并与 monolithic 和 symbolic 后端作比较。 |

### 形式化问题与性质

1. 论文真正补的是 `GR(1)` 在 modular DES control 上的组合式求解路线。
2. 它把“求一个最终 controller”拆成“逐步构造 safe pieces + 最后一跳补 live guarantees”。
3. 这类拆分非常适合大规模工业控制，因为模块边界通常天然存在。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 一组 deterministic `LTS` 形式的 plant 模块。
2. controllable / uncontrollable event 分区。
3. `GR(1)` 形式的 `LTL` 目标。
4. `MTSA` 中的模块化综合工作流。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `LTS`。
2. parallel composition。
3. synthesis observation equivalence 和 quotient `LTS`。
4. 最终 controller set。

### 交换与互操作

这篇论文的互操作重点不在中立格式，而在 `MTSA` 内部把模块化 `DES plant`、`GR(1)` 目标和综合结果串成统一工作流；同时论文还提到可通过已有翻译把问题送向 `Strix`、`Spectra` 等 symbolic synthesis backend 做比较。

## 配套基础设施

- 建模/编辑工具：`MTSA`。
- 解析/交换/元模型支持：`LTS`、模块组合、quotient 和 observation equivalence 工件。
- 仿真/执行支持：最终结果是一组可并行运行的 controllers。
- 验证/分析支持：safe synthesis、live synthesis、winning-state reasoning 和组合式规模化实验。
- 代码生成/转换支持：重点是合成控制器，不是部署代码生成。
- 标准化或社区生态：`MTSA`、`GR(1)` synthesis 和模块化 DES control 研究线构成其生态。

## 适用场景与需求前提

### 适用场景

适合工厂离散事件控制、协议式协调控制、模块化设备逻辑和其他天然可拆成多个 `LTS` 模块的大规模离散控制问题。

### 需求前提

1. plant 需能拆成 deterministic `LTS` 模块。
2. 事件需能清楚分成 controllable / uncontrollable。
3. 控制目标最好能落在 `GR(1)` 片段。
4. 模块化结构确实存在，否则组合式收益有限。

### 不适用或高成本场景

如果需求核心是 dense-time、连续物理过程、概率环境或复杂数值守卫，仅靠本文这条 `LTS + GR(1)` 组合式路线通常不够。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 更像 `GR(1)` 通用后端，而本文聚焦模块化离散事件控制的组合式求解；相对 [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md) 与 [a-multi-paradigm-language-for-reactive-synthesis/desc.md](../a-multi-paradigm-language-for-reactive-synthesis/desc.md)，那两篇更偏前端规格语言，这篇更偏 plant-side synthesis workflow；相对 [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)，`MTSA` 是工作台本体，而本文是在其上新增的组合式 `GR(1)` 合成能力。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明离散控制状态机在后端不一定只能做验证，也可以直接走综合路线。
2. 对“需求到控制状态机”主线很有启发，因为 `GR(1)` 目标能直接从结构化需求抽取。
3. 组合式 plant 视角还提示我们：LLM 生成时可以先生成模块化子状态机，再交给后端组合。

### 作为目标形式主义还是中间表示

更适合作为离散控制综合后端的方法路线，而不是面向工程师的长期前端建模语言。

### 对需求到模型生成的启发

1. 若需求天然分模块，生成阶段应尽量保留模块边界，而不是过早拍平。
2. controllable / uncontrollable 事件分区必须在需求结构化时就明确出来。
3. 若目标是可综合性，限制到 `GR(1)` 往往比追求一般 `LTL` 更现实。

### 现实限制

它依赖 deterministic `LTS`、模块化 plant 和 `GR(1)` 片段三个前提；超出这些边界后，组合式收益和正确性条件都需要重审。

## 重要的相关工作

### 奠基或前身工作

- `DES supervisory control` 与 `LTL/GR(1)` 综合两条母线。
- `MTSA` 的模块化行为建模与分析工作流。

### 同类型或同家族工作

- [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` 综合后端。
- [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)：工程化 reactive-spec 前端。

### 标准 / 格式 / 工具链工作

- [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)：`MTSA` 工作台本体。
- [a-multi-paradigm-language-for-reactive-synthesis/desc.md](../a-multi-paradigm-language-for-reactive-synthesis/desc.md)：可与后端综合衔接的规格输入层。

### 与本研究关系最紧的工作

- 当我们希望从结构化需求直接得到控制状态机时，这篇展示了如何把模块化 plant 与 `GR(1)` 目标接到真正可扩展的综合链。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`LTS / GR(1) discrete event control / MTSA compositional synthesis`
- 论文角色：面向模块化离散事件系统的组合式 `GR(1)` 控制器综合方法
- 核心功能：通过部分安全综合、等价压缩和最终 live 补全，把大规模模块化 `DES` 控制问题拆成可扩展的组合式 `GR(1)` 综合流程。
- 关键特性：模块化 `LTS` plant、controllable / uncontrollable events、safe vs live 分离、synthesis observation equivalence、`MTSA` 实现。
- 构造方式：`modular LTSs -> partial safe synthesis -> quotient abstraction -> final controller set`。
- 基础设施：`MTSA`、`GR(1)` synthesis engine、模块化 `DES` 工作流。
- 适用场景：大规模模块化离散事件控制、工业自动化和事件协调控制。
- 需求前提：plant 需能拆成 deterministic `LTS` 模块，事件需可控性分区清晰，目标宜落在 `GR(1)`。
- 状态：🟢 直接可用
