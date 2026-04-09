# PNML 入门：Petri Net Markup Language 与 ISO/IEC 15909-2 / A Primer on the Petri Net Markup Language and ISO/IEC 15909-2

## 基本信息

- 标题：A primer on the Petri Net Markup Language and ISO/IEC 15909-2
- 中文标题：PNML 入门：Petri Net Markup Language 与 ISO/IEC 15909-2
- 作者：L. M. Hillah，E. Kindler，F. Kordon，L. Petrucci，N. Trèves
- 发表：*Petri Net Newsletter*，76，2009
- DOI：原文未提供
- 链接：https://www.pnml.org/papers/pnnl76.pdf
- 形式主义：`PNML / ISO/IEC 15909-2`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：📄 文档与数据交换
- 论文角色：交换格式 / 元模型标准导读
- 工具/实现获取方式：原文明确给出 `PNML` web pages、`RELAX NG` grammars 与 `PNML Framework` 作为实现入口；未绑定单一官方编辑器。
- 标准/格式获取方式：`ISO/IEC 15909-2`、`http://www.pnml.org/version-2009/grammar/...` 命名空间、`RELAX NG` 语法与 `EMF` 生成 API 共同构成格式获取入口。

## 简报

这篇论文的重要性不在于再定义一种 `Petri Net`，而在于把 `Petri Net` 家族的交换格式稳定成“可扩展元模型 + XML 语法 + 类型包”这一整套基础设施。它把 `Petri Net Document`、`pages`、`reference nodes`、`labels / attributes / graphics / toolspecific` 等核心概念压进统一 `PNML Core Model`，再说明如何把 `PT-Net`、`Symmetric Net` 和 `HLPNG` 映射成具体 XML。

- 形式主义定位：`Petri Net` 家族的标准交换格式与元模型承载，而不是新的网模型本体。
- 构造方式简述：先用 `UML` 元模型组织 `PNML Core Model` 与类型包，再映射到 `XML` 元素、属性、命名空间与 `RELAX NG` 语法。
- 基础设施与场景简述：依托 `ISO/IEC 15909-2`、`PNML` web pages、`RELAX NG`、`EMF/PNML Framework` 与 tool-specific extension，服务 Petri 网跨工具交换、持久化和后续分析链路。

```text
Petri net family -> PNML core metamodel + type package -> XML/RELAX NG document -> tool exchange / framework API / downstream analysis
```

## 形式主义定义与核心对象

### 定义对象

原文围绕以下对象定义 `PNML`：

1. `PetriNetDoc`，即一份包含一个或多个 net 的 `PNML Document`。
2. `PetriNet` 与 `Page`，负责组织层次结构。
3. `Object`，其核心子类包括 `PlaceNode`、`TransitionNode`、`Arc`、`RefPlace`、`RefTrans` 与 `Page`。
4. `Label`、`Annotation`、`Attribute`、`Graphics` 与 `ToolInfo`。
5. `PT-Net`、`SymmetricNet`、`HLPNG` 等类型包，以及对应的 `XML` 映射。

### 核心抽象

论文没有把 `PNML` 写成一个单一数学 tuple，而是通过 `PNML Core Model` 的 `UML` 元模型定义结构。结合文中的对象关系，可保守整理为：

$$
\mathcal{D}_{PNML} = (\mathcal{N}, \mathcal{P}, \mathcal{O}, \mathcal{L}, \mathcal{G}, \mathcal{T}, \tau)
$$

上式中的符号逐项解释如下：

1. `\mathcal{N}` 是 `PetriNet` 集合。
2. `\mathcal{P}` 是 `Page` 集合，允许形成层次页结构。
3. `\mathcal{O}` 是对象集合，包括 place、transition、arc 与 reference nodes。
4. `\mathcal{L}` 是 labels 集合，包括 annotations 与 attributes。
5. `\mathcal{G}` 是 graphics 信息。
6. `\mathcal{T}` 是 tool-specific information 集合。
7. `\tau : \mathcal{N} \to URI` 为每个 net 指派唯一的 type 标识。

对 arc 与 page 的核心结构约束，论文明确给出：

$$
\mathrm{page}(\mathrm{source}(a)) = \mathrm{page}(\mathrm{target}(a))
$$

上式中的符号逐项解释如下：

1. `a` 是一条 arc。
2. `source(a)` 与 `target(a)` 分别是其源节点与目标节点。
3. `page(\cdot)` 返回对象所在的 page。
4. 该约束表示一条 arc 只能连接同一 page 上的节点；跨页连接要靠 reference nodes。

对元模型到文档语法的承载映射，论文本质上在定义：

$$
\mu : \mathcal{M}_{PNML} \to \mathcal{X}_{PNML}
$$

上式中的符号逐项解释如下：

1. `\mathcal{M}_{PNML}` 是 `UML` 元模型中的概念集合。
2. `\mathcal{X}_{PNML}` 是 `XML` 元素、属性与 namespace 组成的具体语法对象。
3. `\mu` 把诸如 `PTMarking`、`PTAnnotation` 之类的元模型元素映射成 `<initialMarking>`、`<inscription>` 等 XML 元素。

### 一个最小例子与通俗解释

论文给出的例子是一个很小的 `P/T net`：

1. `<place id="p1">` 带 `<name>` 与 `<initialMarking>`。
2. `<transition id="t1">` 给出位置。
3. `<arc id="a1" source="p1" target="t1">` 用 `<inscription>` 表示权重。
4. 这些对象再挂上 `<graphics>` 与可选 `<toolspecific>` 信息。

通俗地说，`PNML` 像是“Petri 网的标准化装箱方式”。网的数学对象本体没有变，但所有 place、transition、arc、标签、图形位置和工具私有信息都被装进统一箱子里，别的工具只要认这个箱子，就能读写同一张网。

### 运行 / 接受 / 转移语义

`PNML` 本身不是新的运行语义，而是 Petri 网家族的承载格式。它最关键的“语义”是怎样保证不同工具对同一文档有一致理解：

1. 对象结构由 `PNML Core Model` 固定。
2. 具体网类型的 label 与约束由类型包补充。
3. `text` 与 `structure` 两种 annotation 表示方式共同支持 concrete syntax 与 abstract syntax tree。

论文强调 reference nodes 的扁平化语义，可保守写成：

$$
\mathrm{flat}(\mathcal{D}_{PNML}) = \mathcal{D}_{flat}
$$

上式中的符号逐项解释如下：

1. `\mathrm{flat}` 是将 reference nodes 合并回被引用节点的扁平化操作。
2. `\mathcal{D}_{PNML}` 是原始带页层次与 reference nodes 的文档。
3. `\mathcal{D}_{flat}` 是语义等价的扁平 Petri 网文档。

这条扁平化原则是 `PNML` 允许 hierarchy/reference、但又不破坏基础网语义的重要前提。

### 语义边界

这篇论文的边界很清楚：

1. 它定义的是交换与承载，不是 `Petri Net` 的行为语义新理论。
2. `PNML` 核心强项是 extensibility，不是强制所有工具采用同一图形界面或同一执行算法。
3. `tool-specific information` 被明确允许，但不能破坏基本文档可交换性。
4. `timed / stochastic / module` 等更强扩展在文中只给方向，不都属于 `ISO/IEC 15909-2` 的定稿范围。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 文档骨架 | `$\mathcal{D}_{PNML} = (\mathcal{N}, \mathcal{P}, \mathcal{O}, \mathcal{L}, \mathcal{G}, \mathcal{T}, \tau)$` | 统一 `PNML` 文档的核心对象。 |
| 同页连弧约束 | `$\mathrm{page}(\mathrm{source}(a)) = \mathrm{page}(\mathrm{target}(a))$` | 跨页连弧必须通过 reference nodes 表达。 |
| XML 映射 | `$\mu : \mathcal{M}_{PNML} \to \mathcal{X}_{PNML}$` | 元模型元素会被系统映射为 XML 语法元素。 |
| 扁平化 | `$\mathrm{flat}(\mathcal{D}_{PNML}) = \mathcal{D}_{flat}$` | hierarchy/reference 仍能还原成语义等价扁平网。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 不直接支持 | `PNML` 不重新定义状态机语义对象。 |
| 事件 / 触发 | 不直接支持 | 事件含义来自具体 Petri 网类型，而不是 `PNML` 核心。 |
| 守卫 / 数据 | 通过标签支持 | 高层网数据、条件、注释都通过 labels / type packages 承载。 |
| 层次 | 强支持 | pages、subpages 与 reference nodes 是核心结构。 |
| 并发 / 同步 | 间接支持 | 由 Petri 网本体负责，`PNML` 负责承载。 |
| 时间约束 | 可扩展支持 | timing/stochastic information 可以作为 annotation/type-package 扩展。 |
| 连续动态 / 随机性 | 不原生支持 | 需由具体 Petri 网类型扩展。 |
| 可执行 / 可验证性 | 强承载 | 重点是 exchange / persistence / downstream tooling，而非直接求解。 |

### 形式化问题与性质

1. `PNML` 把 “任何 Petri 网都可看成带标签有向图” 固定成了元模型前提。
2. `Annotation` 与 `Attribute` 的区分，使文本信息、抽象语法树和图形属性能分别建模。
3. reference nodes + flattening 让 hierarchy 与语义等价性兼容。
4. `tool-specific information` 机制说明标准并不拒绝工具私有扩展，但要求明确标记。

## 构造方式与承载格式

### 建模入口

原文的建模入口不是某个单一 GUI，而是：

1. `PNML Core Model` 的 `UML` 元模型。
2. 针对 `PT-Net`、`SymmetricNet`、`HLPNG` 的类型包。
3. 由元模型映射出的 `XML` 元素、属性与 namespace。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PNML` XML 文档。
2. `RELAX NG` 语法。
3. `namespace URI` 与类型标识。
4. 可选 `toolspecific` 扩展。
5. `PNML Framework` 生成的 `EMF` API。

### 交换与互操作

这篇论文的核心就在互操作：

1. 不同 Petri 网类型通过独立 type package 扩展同一 core model。
2. 不同工具可通过 text / structure / toolspecific 三层信息共存。
3. `RELAX NG` 与 `EMF` 让“文档校验”和“程序 API”两条线同时具备。

## 配套基础设施

- 建模/编辑工具：原文不绑定单一编辑器，但默认围绕多工具交换场景组织。
- 解析/交换/元模型支持：`UML` 元模型、`XML` 映射、`RELAX NG` 语法和 namespace 机制是主干。
- 仿真/执行支持：标准本身不定义执行器。
- 验证/分析支持：标准本身不定义验证器，但显式面向后续工具链互操作。
- 代码生成/转换支持：文中提到 `SVG/XSLT` 和 `EMF` API 这类下游转换可能性。
- 标准化或社区生态：`ISO/IEC 15909-2`、PNML web pages、`PNML Framework` 和后续 `Part 3` 讨论构成持续生态。

## 适用场景与需求前提

### 适用场景

适合 `Petri Net` 家族跨工具交换、模型持久化、可追溯归档、LLM 生成结果标准化落盘，以及要把不同分析器串起来的场景。

### 需求前提

1. 模型本体已经是某种 `Petri Net` 或其高层变体。
2. 团队需要稳定的机读交换格式，而不是只保存一张图片。
3. 标签、图形信息和工具私有信息需要分层管理。
4. 后续工具愿意遵循同一 namespace / grammar 约束。

### 不适用或高成本场景

如果目标只是单工具内部临时建模，或者模型本体根本不是网结构，那么引入 `PNML` 会显得偏重。

## 与相邻形式主义的关系

相对 [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)，本文讲的是交换载体而不是 Petri 网语义本体；相对 [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md) 与 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，它更像这些工具线的中立文件承载；相对 [scxml-state-machine-notation-for-control-abstraction/desc.md](../scxml-state-machine-notation-for-control-abstraction/desc.md)，二者都在做“把图形行为模型落成标准文本格式”，只是对象家族不同。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果未来 `project_1` 要输出 `Petri Net` 或高层网模型，完全可以把“生成结果”直接落到标准化文档，而不是停留在图或伪代码层。

### 作为目标形式主义还是中间表示

更适合作为目标交付格式和交换中间层，而不是语义分析本体。

### 对需求到模型生成的启发

1. 生成时要把 place、transition、arc、labels、graphics、tool-specific information 分层。
2. 生成器最好同时知道 core model 和具体 type package，而不是只会吐 XML 标签。
3. 若后续想做跨工具验证或修复，标准化承载比工具私有格式更稳。

### 现实限制

`PNML` 只能解决“怎么装”，不能解决“这个网的语义到底是什么、适不适合验证什么”。

## 重要的相关工作

- [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)：`Petri Net` 本体与分析母线。
- [coloured-petri-nets/desc.md](../coloured-petri-nets/desc.md)：高层 `Petri Net` 变体的语义入口。
- [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)：基于 `CPN` 的成熟工具线。
- [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：时间扩展网模型的 IDE / verifier 代表。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：📄 文档与数据交换
- 形式主义：`PNML / ISO/IEC 15909-2`
- 论文角色：交换格式 / 元模型标准导读

