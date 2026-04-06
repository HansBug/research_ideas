# 超越 WYSIWYG 的状态图开发 / Statechart Development Beyond WYSIWYG

## 基本信息

- 标题：Statechart Development Beyond WYSIWYG
- 中文标题：超越 WYSIWYG 的状态图开发
- 作者：Steffen Prochnow，Reinhard von Hanxleden
- 发表：*Model Driven Engineering Languages and Systems*，pp. 635-649，2007
- DOI：`10.1007/978-3-540-75209-7_43`
- 链接：https://doi.org/10.1007/978-3-540-75209-7_43
- 形式主义：`Statecharts / KIT / KIEL`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：statechart editing DSL + auto-layout modeling environment
- 工具/实现获取方式：论文明确说明原型工具为 `KIEL`（Kiel Integrated Environment for Layout），并在文中介绍其 `KIEL macro editor` 与 `KIT editor` 的实现与课堂使用。
- 标准/格式获取方式：核心承载方式是 `KIT`（Kiel statechart extension of dot）文本语言、`KIEL` 图形 editor、自动布局输出，以及对 `Esterel Studio`、`Stateflow` 和 `UML/XMI` 的导入/综合支持。

## 简报

这篇论文的重点，不是再争论 statecharts 有没有用，而是直接挑战“状态图必须靠 WYSIWYG 手工拖拽排版”这一默认前提。作者提出两条替代路线：一条是基于 production/macro 的结构化编辑，另一条是基于 `KIT` 的文本式、dialect-independent 状态图描述语言；两者都接到 `KIEL` 的自动布局引擎上，让建模者专注状态图结构，而不是不停腾挪框和线。

- 形式主义定位：statechart DSL 与编辑基础设施，而不是新的状态机母线。
- 构造方式简述：用 `KIT` 文本描述或 macro-based productions 操作状态图结构，再由 `KIEL` 自动布局并保持文本视图与图形视图同步。
- 基础设施与场景简述：依托 `KIT`、`KIEL macro editor`、auto-layout、`Statechart grammar`、`SNF` 和多 dialect import，服务 reactive embedded systems 中的大型 statechart 建模与维护。

```text
statechart structure intent -> KIT text or macro production -> KIEL parser / synthesizer -> auto-layouted graphical model -> synchronized editing and comprehension
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 传统 `WYSIWYG` 状态图编辑过程。
2. 基于 productions 的 macro-based editing。
3. 文本式状态图语言 `KIT`。
4. `KIEL` 自动布局与双视图同步环境。
5. `Statechart Normal Form (SNF)` 与不同布局策略。

### 核心抽象

论文明确说“the set of productions constitutes a Statechart grammar”，因此可直接把其编辑语法写成：

$$
G_{SC} = (N, \Sigma, P, S)
$$

上式中的符号逐项解释如下：

1. `N` 是非终结符集合，对应可进一步展开的状态图结构位置。
2. `\Sigma` 是终结符集合，对应具体状态图元素。
3. `P` 是 productions，也就是论文所说的 editing schemata。
4. `S` 是初始状态图结构。

论文对 macro-based editing 的核心动作可保守整理为：

$$
p : l \Rightarrow r,\qquad SC' = p(SC)
$$

上式中的符号逐项解释如下：

1. `p` 是某条 production / editing schema。
2. `l` 是当前选中 focus 处要匹配的左侧模式。
3. `r` 是应用后替换进去的右侧结构。
4. `SC` 是当前状态图。
5. `SC'` 是应用 production 后的新状态图。

论文还把传统编辑序列和新编辑序列对比得很清楚，可保守写成：

$$
Edit_{WYS} = create\_space \circ focus \circ apply \circ rearrange
$$

$$
Edit_{KIEL} = focus \circ apply
$$

上式中的符号逐项解释如下：

1. `create_space` 表示为新元素腾挪空间。
2. `focus` 表示选中待修改元素。
3. `apply` 表示执行编辑动作/production。
4. `rearrange` 表示人工重排布局。
5. 论文的核心主张，就是通过自动布局把前后两个布局相关步骤消掉。

对文本语言 `KIT`，结合论文描述可把其文本到模型的映射写成：

$$
\gamma_{KIT} : Text_{KIT} \to Model_{SC}
$$

上式中的符号逐项解释如下：

1. `Text_{KIT}` 是 `KIT` 文本描述。
2. `Model_{SC}` 是对应的状态图内部模型。
3. `KIEL` 会保持 `KIT` 代码与图形模型的持续同步。

### 一个最小例子与通俗解释

论文给出的 `ABRO` 例子很适合作最小说明：

1. `KIT` 头部指定 model dialect 为 `Esterel Studio 5.0`。
2. `input A/B/R`、`output O` 定义信号。
3. `ABO { ... }` 及其内部嵌套表示层次状态。
4. `||` 表示并行区域。
5. `->` 表示 transition，没有 source 的 `->` 代表初始连接。

通俗地说，`KIT` 像“为状态图设计的一门结构化文本语法”，而 `KIEL` 则像“会自动把这门文本语言长成好看图形状态图的编辑器”。你写的是结构，布局交给工具。

### 运行 / 接受 / 转移语义

论文主体不重写 statecharts 的执行语义，而是聚焦其编辑与表示语义：

1. 文本和图形视图共享同一状态图数据结构。
2. `KIT` editor 修改文本时，`KIEL` 用 parser/synthesizer 重建图形模型。
3. macro editor 修改图形时，会依据底层 grammar 应用 productions。
4. 自动布局把结果规范到作者偏好的 `SNF` 风格。

若从工具链角度表达这两种入口，可保守写成：

$$
\mathrm{MacroEdit}(SC, p) \to SC' \to Layout(SC')
$$

$$
\mathrm{ParseKIT}(text) \to SC \to Layout(SC)
$$

其中：

1. `MacroEdit` 走 production 路线。
2. `ParseKIT` 走文本解析/综合路线。
3. 两条路线最终都进入自动布局与同步显示。

### 语义边界

论文也明确给出边界：

1. 它主要关心 statechart 的编辑与维护，不是完整验证平台。
2. `KIT` 目标是 concise、dialect-independent，但仍绑定到 `KIEL` 原型环境。
3. 论文强调 reactive embedded devices 语境，不把所有状态图工具都覆盖进去。
4. 评估重点是编辑速度与理解性，而不是工业级规模性能。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态图编辑语法 | `$G_{SC} = (N, \Sigma, P, S)$` | 对应论文明确提出的 `Statechart grammar`。 |
| production 应用 | `$p : l \Rightarrow r,\ SC' = p(SC)$` | 对应 macro-based editing 的核心机制。 |
| 编辑序列比较 | `$Edit_{WYS} = create\_space \circ focus \circ apply \circ rearrange$` 与 `$Edit_{KIEL} = focus \circ apply$` | 体现论文“把布局负担从建模者转给工具”的核心思想。 |
| `KIT` 映射 | `$\gamma_{KIT} : Text_{KIT} \to Model_{SC}$` | 对应 `KIT` 文本语言到状态图模型的同步综合。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 论文主体就是 statecharts 及其层次/并行结构。 |
| 事件 / 触发 | 中等支持 | 文本语言能表达 triggers，但论文重点在编辑方式。 |
| 守卫 / 数据 | 中等支持 | 通过不同 dialect 与状态图表达能力承载。 |
| 层次 | 很强 | hierarchy 是 `KIT` 和 auto-layout 的核心对象。 |
| 并发 / 同步 | 很强 | `||` 直接表达并行区域。 |
| 时间约束 | 取决于 dialect | 可导入 `Esterel/Stateflow/UML` 等不同方言，不单独扩展 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 中等到强 | `KIEL` 有仿真与 robustness checking，但论文主体更偏建模入口与编辑效率。 |

### 形式化问题与性质

1. 论文真正要解决的是 statechart 维护成本，而不是 statechart 表达力不足。
2. `KIT` 的价值在于它既不是某家厂商私有格式，也不是冗长 XML，而是为结构化编辑优化过的 concise language。
3. `macro-based editing + auto-layout` 说明状态图并不必然要靠手工拖拽和排版。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 在 `KIEL macro editor` 中通过 productions 直接操作状态图结构。
2. 在 `KIT editor` 中编写文本式状态图。
3. 通过 `KIEL` 自动布局生成图形视图。
4. 导入 `Esterel Studio`、`Stateflow` 或 `UML/XMI` 现有模型。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `KIT` 文本语言。
2. `KIEL` 图形模型与状态图数据结构。
3. `SableCC` 生成的 parser / synthesizer。
4. 自动布局器输出的图形状态图。

### 交换与互操作

这条路线的互操作重点在于：

1. `KIT` 与图形视图的双向同步。
2. 不同 statechart dialect 到 `KIEL` 的导入。
3. 自动布局让不同来源的模型收束到统一阅读风格。

## 配套基础设施

- 建模/编辑工具：`KIEL macro editor`、`KIT editor`、图形浏览器。
- 解析/交换/元模型支持：`KIT` parser/synthesizer、`SableCC`、`UML/XMI` 导入、`Stateflow/Esterel` 兼容。
- 仿真/执行支持：`KIEL` 提供动态 focus-and-context visualization 与仿真支持。
- 验证/分析支持：automatic checking framework 可检查 robustness rules。
- 代码生成/转换支持：可从文本 `KIT` 综合图形模型，也可从文本 Esterel 程序综合图形 `SSM`。
- 标准化或社区生态：依托 Kiel 大学 `KIEL` 原型环境与课堂持续使用。

## 适用场景与需求前提

### 适用场景

适合大型 statechart 的创建、增量修改、维护和教学，尤其适合那些已经被 WYSIWYG 拖拽排版成本拖慢的 reactive embedded systems 建模场景。

### 需求前提

1. 团队愿意把“图形即最终真相”转成“结构优先，布局自动生成”的工作方式。
2. 状态图规模足够大，大到人工排版已成为明显负担。
3. 需要在不同 statechart dialect 之间保持一定互操作性。
4. 可以接受研究型原型工具而不是商业成熟 IDE。

### 不适用或高成本场景

如果团队极度依赖手工视觉微调、或必须完全依附某个商用 IDE 的原生格式，`KIT/KIEL` 这条结构优先路线会引入额外迁移成本。

## 与相邻形式主义的关系

相对 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)，这篇论文不是再讲 `Statecharts` 理论母线，而是讲如何更高效地编辑它们；相对 [synccharts-a-visual-representation-of-reactive-behaviors/desc.md](../synccharts-a-visual-representation-of-reactive-behaviors/desc.md)，`SyncCharts` 更像新的状态图方言，而 `KIT` 更像跨方言的文本入口；相对 [repast-simphony-statecharts/desc.md](../repast-simphony-statecharts/desc.md)，后者更强调运行时与代码生成，而这里更强调建模入口、自动布局和维护效率。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 很关键，因为它说明“状态机应该长什么样”不只是语义问题，也是编辑问题。若未来让 LLM 生成状态图，直接生成一种结构优先、可自动布局、可跨方言映射的文本 DSL，往往比让模型直接画一张终态图更可维护。

### 作为目标形式主义还是中间表示

`KIT` 很适合做中间表示或编辑层 DSL；`KIEL` 则更像承载该表示的工程化入口。

### 对需求到模型生成的启发

1. LLM 生成状态图时，最好优先生成结构化文本而不是只生成图像布局。
2. 自动布局能显著降低后续人类整理成本，是“生成可用模型”的一部分。
3. 若研究目标需要支持多种状态图方言，dialect-independent 文本入口非常有价值。

### 现实限制

这条路线强在建模和维护，不直接解决验证后端或工业部署问题。

## 重要的相关工作

1. [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)：状态图理论母线。
2. [synccharts-a-visual-representation-of-reactive-behaviors/desc.md](../synccharts-a-visual-representation-of-reactive-behaviors/desc.md)：另一条状态图/同步反应式方言线。
3. [repast-simphony-statecharts/desc.md](../repast-simphony-statecharts/desc.md)：更强调执行与运行时观测的 statechart 基础设施。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Statecharts / KIT / KIEL`
- 论文角色：statechart editing DSL + auto-layout modeling environment
- 归类理由：论文主体是 `KIT` 这一文本化 statechart DSL 及其 `KIEL` 编辑基础设施，而不是新的状态机母线。
