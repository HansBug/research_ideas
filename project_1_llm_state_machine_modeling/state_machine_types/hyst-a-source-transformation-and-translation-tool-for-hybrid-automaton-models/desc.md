# HYST：混成自动机模型的源转换与翻译工具 / HYST: A Source Transformation and Translation Tool for Hybrid Automaton Models

## 基本信息

- 标题：HYST: A Source Transformation and Translation Tool for Hybrid Automaton Models
- 中文标题：HYST：混成自动机模型的源转换与翻译工具
- 作者：Stanley Bak，Sergiy Bogomolov，Taylor T. Johnson
- 发表：*Proceedings of the 18th International Conference on Hybrid Systems: Computation and Control*，pp. 128-133，2015
- DOI：`10.1145/2728606.2728630`
- 链接：https://www.taylortjohnson.com/research/bak2015hscc.pdf
- 形式主义：`Hybrid Automata / HYST`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：hybrid-automata source transformer / cross-tool translator
- 工具/实现获取方式：原文明确说明 `HYST` 与 benchmark 可从 `http://www.verivital.com/hyst/` 获取。
- 标准/格式获取方式：输入承载是 `SpaceEx XML`，输出可生成 `Flow*`、`HyCreate`、`dReach` 等格式；原文本身不提供统一中立交换标准。

## 简报

这篇论文的核心贡献，是把“各家混成验证器都差不多在讲同一种 hybrid automaton 语义，但语法互不兼容”这个现实问题，做成了一个真正可用的翻译层。`HYST` 让你可以从 `SpaceEx XML` 出发，一键生成 `Flow*`、`HyCreate`、`dReach` 等工具输入，同时还能在中间 IR 上套 model transformation passes，比如 pseudo-invariants 或 time scaling。它补的是混成自动机工具线里的“跨工具桥接层”，而不是某个单点 verifier。

- 形式主义定位：面向 `Hybrid Automata` 的源转换与翻译基础设施，而不是新的混成自动机本体。
- 构造方式简述：输入 `SpaceEx XML`，解析为内部 IR，在 IR 上执行 model-to-model passes，再输出各目标工具的源格式。
- 基础设施与场景简述：依托 `SpaceEx` 作为源语言、Java IR、tool-specific printers 与 pseudo-invariant / time-scaling passes，服务 cross-tool benchmark、回归测试与研究原型复用。

```text
hybrid automaton in SpaceEx XML -> HYST IR -> transformation pass -> Flow* / HyCreate / dReach / other tool input
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `HYST`：

1. `Hybrid Automata` 模型。
2. `SpaceEx XML` 作为源格式。
3. `Flow*`、`HyCreate`、`dReach` 等目标工具格式。
4. 中间表示 `IR`。
5. model transformation passes。

### 核心抽象

论文默认采用与 `SpaceEx` 接近的混成自动机语义。可保守整理为：

$$
H = (Loc, X, Init, Flow, Inv, Trans)
$$

上式中的符号逐项解释如下：

1. `Loc` 是离散 modes / locations 集合。
2. `X` 是连续变量集合。
3. `Init` 是初始状态集合。
4. `Flow` 为每个 location 指派连续动力学。
5. `Inv` 为每个 location 指派不变式。
6. `Trans` 是带 guards 与 resets 的离散跳转集合。

`HYST` 的核心不在新语义，而在源到源映射。可保守写成：

$$
\mathcal{T}_{tool} : H_{SX} \to H_{tool}
$$

上式中的符号逐项解释如下：

1. `H_{SX}` 是按 `SpaceEx XML` 描述的源模型。
2. `H_{tool}` 是目标工具可接受的等价或保守等价模型。
3. `\mathcal{T}_{tool}` 是某个 specific backend printer 对应的翻译函数。

论文特别强调中间 passes 也是 model-to-model 转换。可写成：

$$
\mathcal{P} : H \mapsto H'
$$

并希望满足：

$$
H \sim H'
$$

上式中的符号逐项解释如下：

1. `\mathcal{P}` 是某个 transformation pass。
2. `H'` 是经过 pass 处理后的模型。
3. `\sim` 表示两者在目标 reachability / verification 语境下保持语义对应；例如 pseudo-invariant splitting 被论文描述为 bisimilar transformation。

### 一个最小例子与通俗解释

论文用 thermostat / heater 作为可视化示例：

1. 关闭加热时，温度按 `\dot{x}=-8x` 衰减。
2. 开启加热时，温度按 `\dot{x}=-8(x-30)` 靠近加热稳态。
3. 当温度过低或过高时，在两个 modes 间切换，并重置局部计时变量。
4. 同一个模型被 `HYST` 转成多种工具格式后，可以直接比较不同 reachability engine 的表现。

通俗地说，`HYST` 像“混成自动机的 Babel fish”。它不帮你做最终验证，但它让同一个模型能被不同 verifier 理解，还允许在翻译途中顺手做结构改写。

### 运行 / 接受 / 转移语义

论文在比较 `SpaceEx` 时给出其 reachability fixed point 形式：

$$
S_0 := post_c(Init), \quad S_{i+1} := S_i \cup post_c(post_d(S_i))
$$

上式中的符号逐项解释如下：

1. `Init` 是初始状态集合。
2. `post_c` 是连续后继算子。
3. `post_d` 是离散后继算子。
4. 该公式说明多种工具虽然实现细节不同，但都在做连续/离散后继的反复展开。

对 bounded reachability / safety，论文也默认关注如下问题：

$$
\exists \rho \in exec(H, T).\ \rho(T) \in Bad
$$

上式中的符号逐项解释如下：

1. `exec(H,T)` 是模型 `H` 在时间界 `T` 内的执行集合。
2. `Bad` 是不安全状态集合。
3. `Flow*`、`HyCreate`、`dReach` 等工具在具体表示法上不同，但都围绕这类可达性问题工作。

而 `HYST` 自己做的事情，可保守写成：

$$
H_{out} = Print_{tool}(\mathcal{P}_k \circ \cdots \circ \mathcal{P}_1(IR(Parse(H_{SX}))))
$$

上式中的符号逐项解释如下：

1. `Parse` 把 `SpaceEx XML` 解析成内部 `IR`。
2. `\mathcal{P}_i` 是若干 transformation pass。
3. `Print_{tool}` 把处理后的 IR 输出为目标工具源格式。

### 语义边界

这篇论文的边界非常明确：

1. 它不是统一所有混成工具的最终 interchange standard。
2. 当前输入源主要是 `SpaceEx XML`。
3. 组合网络的处理仍较依赖 `SpaceEx` 侧的 flattening。
4. 它解决的是“跨工具可用模型”的问题，不是“哪个 reachability algorithm 最优”的问题。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 混成自动机骨架 | `$H = (Loc, X, Init, Flow, Inv, Trans)$` | 固定 `HYST` 处理对象的基本结构。 |
| 工具翻译 | `$\mathcal{T}_{tool} : H_{SX} \to H_{tool}$` | 把 `SpaceEx` 源模型翻成具体后端工具格式。 |
| model pass | `$\mathcal{P} : H \mapsto H'$` | 在中间表示上做结构性改写。 |
| `SpaceEx` reachability skeleton | `$S_{i+1} := S_i \cup post_c(post_d(S_i))$` | 说明各工具共享的 reachability 直觉。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 保留 `Hybrid Automata` 的离散 locations。 |
| 事件 / 触发 | 强支持 | guards / resets / mode switches 会被完整翻译。 |
| 守卫 / 数据 | 很强 | 支持 flows、invariants、guards、resets 的跨格式落地。 |
| 层次 | 弱支持 | 主要依赖 `SpaceEx` 侧 flattening。 |
| 并发 / 同步 | 中等支持 | 网络组合可输入，但目标工具常需展平。 |
| 时间约束 | 很强 | 混成时间演化是核心。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 覆盖 affine 与 nonlinear dynamics，不涉及概率。 |
| 可执行 / 可验证性 | 很强 | 通过多工具输出让同一模型直接进入不同 reachability engine。 |

### 形式化问题与性质

1. `HYST` 的关键工程价值，是把“研究中的模型变换技巧”从单个 verifier 中抽出来，变成通用 pass。
2. 论文用 pseudo-invariants 演示了这种 pass 的好处：同一结构改写能同时改进多个工具的 reachable-set 表现。
3. 对 benchmarking 来说，它让“算法差异”和“输入模型写法差异”更容易被分开。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 `SpaceEx XML` 写或导出混成自动机。
2. 用 `HYST` 解析成内部 IR。
3. 选择目标工具与可选 pass。
4. 生成 `Flow*`、`HyCreate`、`dReach` 等输入文件并运行后端。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `SpaceEx XML` 源模型。
2. `HYST` 的 Java IR。
3. tool-specific 输出格式：`Flow*`、`HyCreate`、`dReach` 等。
4. time-scaling、pseudo-invariant 等 pass 的参数化配置。

### 交换与互操作

这篇论文的互操作重点就是翻译链本身：

1. `SpaceEx XML` 被当作事实上的源承载。
2. 各目标工具的输入 printer 在同一 IR 上实现。
3. 一些目标工具需要的 identity reset 或保留关键字改名，也通过 pass 自动完成。

## 配套基础设施

- 建模/编辑工具：源端默认是 `SpaceEx` 生态与其 XML 格式。
- 解析/交换/元模型支持：`HYST` Java IR、parsers、printers 与转换 passes。
- 仿真/执行支持：`HYST` 自己不执行 reachability，而是把模型送到 `Flow*`、`HyCreate`、`dReach` 等后端。
- 验证/分析支持：支持为多个 verifier 快速生成可跑模型，并用于 regression / correctness checking。
- 代码生成/转换支持：核心能力就是 source-to-source translation 与 model-to-model passes。
- 标准化或社区生态：`verivital` 站点、示例 benchmark 与 `SpaceEx` / `Flow*` / `dReach` 等工具构成联合生态。

## 适用场景与需求前提

### 适用场景

适合需要跨多个 hybrid verifier 做对比、回归测试、benchmark 共享，或希望把通用模型改写一次性复用到多个后端的场景。

### 需求前提

1. 模型能够表达为 `SpaceEx` 近似的 hybrid automaton 语义。
2. 目标关注点是 reachability / safety，而不是统一运行时执行。
3. 团队愿意接受一个“翻译层 + 多后端”的工具链。
4. 若模型是 automata network，需接受可能的 flattening 成本。

### 不适用或高成本场景

如果目标只是单一工具的单一模型，或者系统语义明显超出 `Hybrid Automata` / `SpaceEx` 输入骨架，`HYST` 的收益会下降。

## 与相邻形式主义的关系

相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)、[phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)、[flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md) 这些单点 verifier，`HYST` 不是新的 reachability engine，而是桥接层；相对 [reachability-computation-for-hybrid-systems-with-ariadne/desc.md](../reachability-computation-for-hybrid-systems-with-ariadne/desc.md)，它不强调开放数值框架本身，而强调跨工具 source transformation。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续 `project_1` 选择 `Hybrid Automata` 作为某类需求的目标形式主义，真正工程化时不能只盯一个 verifier，还需要准备模型互操作和转换层。

### 作为目标形式主义还是中间表示

`HYST` 本身不是目标形式主义，而是让 `Hybrid Automata` 在多个验证后端间流通的基础设施。

### 对需求到模型生成的启发

1. 生成阶段若能统一输出到某个稳定源格式，例如 `SpaceEx XML`，后续工具接入成本会明显下降。
2. 一些结构性修复可以先在翻译层完成，而不是对每个 verifier 单独重写。
3. 比较不同验证后端时，最好先统一输入模型来源，避免把建模差异误判成算法差异。

### 现实限制

它不能替代 verifier 本身；若目标工具语义差异过大，翻译只能做到保守近似而不是完全透明。

## 重要的相关工作

- [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：当前最重要的源格式母线之一。
- [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：早期 polyhedral hybrid verifier 主线。
- [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：非线性混成系统后端之一。
- [reachability-computation-for-hybrid-systems-with-ariadne/desc.md](../reachability-computation-for-hybrid-systems-with-ariadne/desc.md)：开放 hybrid reachability framework 代表。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
