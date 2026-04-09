# Workcraft：解释型图模型框架 / WORKCRAFT: framework for interpreted graphs

## 基本信息

- 标题：WORKCRAFT: framework for interpreted graphs
- 中文标题：Workcraft：解释型图模型框架
- 作者：`\mu Systems Group`
- 发表：DATE 2016 University Booth abstract，2016
- DOI：原文未提供
- 链接：https://past.date-conference.com/system/files/file/date16/ubooth/37940.pdf
- 形式主义：`interpreted graph models / Workcraft / plugin-based graph-model framework`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：plugin-based interpreted-graph modelling / simulation / analysis framework
- 工具/实现获取方式：原文明确给出 `http://workcraft.org/` 作为获取入口，并说明平台以插件方式支持多种 interpreted graph models。
- 标准/格式获取方式：承载对象是图结构本体、模型插件、backend tool adapters 与模型间转换链路；它不是单一标准格式。

## 简报

这篇短文的价值，不在于提出某一种新的状态机语言，而在于给出一个统一容纳 `Petri net`、`Signal Transition Graph`、`Finite State Machine`、`xMAS`、dataflow structure 等多种“解释型图模型”的通用框架。`Workcraft` 的核心思路是：很多并发系统模型共享静态图骨架，只是语义解释对象不同，因此可以在同一前端里编辑、仿真、分析，再按需要映射到等价 Petri 网或接到 `Petrify/Punf/MPSat` 等后端。

- 形式主义定位：interpreted-graph modelling framework，而不是新的图模型母型。
- 构造方式简述：统一图编辑前端 + plugin-defined semantics + model-to-model conversion + backend tool adapters。
- 基础设施与场景简述：依托 plugin 机制、图形编辑器、(co-)simulation、Petri-net-based analysis 与 `Petrify/Punf/MPSat` 等后端，服务并发系统、异步电路和 dataflow design。

```text
static graph structure -> plugin-defined interpretation -> editing / simulation -> optional conversion to Petri net -> backend analysis / synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. interpreted graph model。
2. 图形前端编辑与模拟环境。
3. plugin-based model taxonomy。
4. 模型间转换。
5. 外部 backend tools。

### 核心抽象

原文没有给出统一数学元组；以下写法是根据“静态图骨架 + 额外语义实体”的描述做的保守整理：

$$
\mathcal{I} = (G, \Sigma, \mu)
$$

上式中的符号逐项解释如下：

1. `G` 是静态图结构。
2. `\Sigma` 是与该图关联的语义状态载体，例如 token、信号值、执行步或数据流标记。
3. `\mu` 是把 `G` 与 `\Sigma` 结合起来的解释规则。
4. 论文把这类对象统称为 interpreted graph models。

把 `Workcraft` 平台自身保守写成：

$$
\mathcal{W} = (\mathcal{P}, \mathcal{C}, \mathcal{B})
$$

上式中的符号逐项解释如下：

1. `\mathcal{P}` 是 plugin 集合，每个 plugin 定义一种图模型及其编辑/分析逻辑。
2. `\mathcal{C}` 是 model-to-model conversion 机制。
3. `\mathcal{B}` 是外部 backend adapters，例如 `Petrify`、`Punf`、`MPSat`。
4. 这反映了原文“同一框架 + 插件 + 转换 + 后端”的工程组织。

### 一个最小例子与通俗解释

论文给出的直觉最小例子就是“不同模型共享图形骨架”：

1. 用户可以在同一前端里画 `FSM`、`Petri net` 或 `Signal Transition Graph`。
2. 某些模型可直接分析，某些则先转换成等价 `Petri net` 再分析。
3. 后端工具负责更具体的综合或验证任务。

通俗地说，`Workcraft` 像一个“并发模型工作台底座”。你先画图，再由插件告诉系统“这张图该按哪种语义解释”，最后再决定要不要把它送去某个专用验证器。

### 运行 / 接受 / 转移语义

论文没有统一的运行语义，而是强调不同 interpreted graph models 可共享基础设施。对某个模型实例 `\mathcal{I}`，可保守写成：

$$
\mathcal{I} \xrightarrow{\mathcal{C}} N_P \xrightarrow{\mathcal{B}} Result
$$

上式中的符号逐项解释如下：

1. `\mathcal{I}` 是某个 interpreted graph model。
2. `\mathcal{C}` 是可选转换，把模型映射到行为等价的 `Petri net` 或其他分析友好形式。
3. `N_P` 是目标分析模型。
4. `\mathcal{B}` 是外部 backend tool。
5. `Result` 是仿真、验证、综合或分析结果。

### 语义边界

1. 这篇文章是框架介绍，不是某单一模型的完整语义定义。
2. 平台能做什么，高度依赖已安装 plugins 和 backend tools。
3. 论文篇幅很短，重点在平台范围与模型族谱，不在具体算法。
4. 它是“工作台底座”条目，不宜误读成单一 `STG` 或 `Petri net` 母文。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| interpreted graph 骨架 | `$\mathcal{I} = (G, \Sigma, \mu)$` | 静态图骨架需要配语义状态与解释规则。 |
| 平台骨架 | `$\mathcal{W} = (\mathcal{P}, \mathcal{C}, \mathcal{B})$` | `Workcraft` 由插件、转换和后端三层组成。 |
| 分析链 | `$\mathcal{I} \xrightarrow{\mathcal{C}} N_P \xrightarrow{\mathcal{B}} Result$` | 平台允许直接分析，也允许先转换再分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `FSM`、`Petri net`、`STG` 等都可作为插件模型。 |
| 事件 / 触发 | 中等支持 | 取决于具体插件。 |
| 守卫 / 数据 | 中等支持 | 由各模型插件自行定义。 |
| 层次 | 中等支持 | 取决于模型族；框架本身不是层次状态机语言。 |
| 并发 / 同步 | 很强 | 整个平台明显偏并发系统设计。 |
| 时间约束 | 弱支持 | 本文并不聚焦显式时钟模型。 |
| 连续动态 / 随机性 | 弱支持 | 不是主线。 |
| 可执行 / 可验证性 | 很强 | 视觉编辑、(co-)simulation、分析与 backend integration 都已到位。 |

### 形式化问题与性质

1. 文章的核心不是某条算法，而是“如何让多种 graph-based formalisms 共用同一工作台”。
2. interpreted graph 这一抽象非常适合文库里区分“模型本体”和“统一载体”。
3. 它是 `Workcraft` / `STG asynchronous-circuit tooling` 静态挂接口径里更通用的框架锚点。

## 构造方式与承载格式

### 建模入口

论文中直接列出的建模入口包括：

1. Directed Graph。
2. Finite State Machine。
3. Petri Net。
4. Policy Net。
5. Structured Occurrence Net。
6. Finite State Transducer。
7. Signal Transition Graph。
8. Conditional Partial Order Graph。
9. Digital Circuit。
10. Dataflow Structure。
11. xMAS Circuit。

### 机器可处理承载方式

机器可处理承载方式包括：

1. plugin-defined model data。
2. 图编辑前端。
3. model conversion pipeline。
4. backend tool adapters。

### 交换与互操作

1. 互操作是本文核心：不同模型可以互转，常见终点是 `Petri net`。
2. backend tools 通过适配器接入，而非写死在单一模型里。
3. 这让 Workcraft 更像 modelling workbench，而不是单一 verifier。

## 配套基础设施

- 建模/编辑工具：统一图形编辑前端。
- 解析/交换/元模型支持：plugin 机制与模型间转换链。
- 仿真/执行支持：(co-)simulation。
- 验证/分析支持：可映射到 `Petrify`、`Punf`、`MPSat` 等后端。
- 代码生成/转换支持：重点是 model conversion 与 synthesis backend 桥接。
- 标准化或社区生态：`workcraft.org`、插件族谱和异步电路/并发系统工具链共同构成生态。

## 适用场景与需求前提

### 适用场景

适合需要在多种 graph-based formalisms 之间切换、比较或桥接的并发系统设计场景，尤其适合异步电路、Petri/STG 与 dataflow family 的统一工作台需求。

### 需求前提

1. 建模对象最好本身具有明确的静态图骨架。
2. 期望从统一图形前端出发，再选不同分析后端。
3. 团队接受 plugin + backend adapter 这种平台式组织。

### 不适用或高成本场景

如果目标只是一种单一 DSL 的深度语义或专用验证器，那么 `Workcraft` 的平台抽象会显得过宽。

## 与相邻形式主义的关系

相对 [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)，本文更通用，介绍的是 `Workcraft` 平台本体，而不是某条 mutex-aware `STG` flow；相对 [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)，`SNAKES` 更像高层 Petri 原型库，而 `Workcraft` 更偏统一工作台；相对 [snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md](../snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md)，两者都偏 graph-based workbench，但 `Workcraft` 更强调 interpreted graph family 与异步电路后端。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们，很多状态机/并发模型之间其实共享“静态图 + 动态解释”这一更高层公共骨架。
2. 对 `project_1` 来说，这类平台条目有助于思考未来是否需要统一的中间编辑/可视化载体，而不是一开始就把语言写死。
3. 若后续要比较不同状态机家族的工程可用性，`Workcraft` 这种统一工作台是很有价值的基础设施证据。

### 作为目标形式主义还是中间表示

更像统一建模/验证工作台和执行载体，而不是目标形式主义。

### 对需求到模型生成的启发

1. 同一份需求可能最终落成多种图模型，平台化载体能减少前端重复投入。
2. 若未来要做“一个前端，多条后端”，`Workcraft` 提供了很直接的工程参照。

### 现实限制

这篇 booth abstract 非常短，能稳定提炼的是平台范围、插件谱系与后端桥接逻辑；更细的单模型语义仍需回到相应插件或专题论文。

## 重要的相关工作

1. [design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md](../design-and-verification-of-speed-independent-circuits-with-arbitration-in-workcraft/desc.md)：`Workcraft` 在具体 `STG` 异步电路流上的应用条目。
2. [petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md](../petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md)：`Workcraft` 经常调用的异步综合后端。
3. [snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md](../snoopy-a-tool-to-design-and-animate-simulate-graph-based-formalisms/desc.md)：另一条 graph-based workbench 证据线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
