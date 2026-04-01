# UML 2.5.1 规范中的状态机 / OMG Unified Modeling Language (OMG UML), Version 2.5.1

## 基本信息

- 标题：OMG Unified Modeling Language (OMG UML), Version 2.5.1
- 中文标题：OMG UML 2.5.1 规范
- 作者：Object Management Group
- 发表：OMG Formal Specification, 2017
- DOI：原文未提供
- 链接：https://www.omg.org/spec/UML/2.5.1/PDF
- 形式主义：UML State Machine
- 主类：🧩
- 描述客体：🎛️
- 所属领域：💻
- 论文角色：标准规范
- 工具/实现获取方式：规范本身不附具体工具，但对应生态有广泛商业与开源建模工具。
- 标准/格式获取方式：规范正文以及 `UML.xmi`、`PrimitiveTypes.xmi`、`StandardProfile.xmi`、`UMLDI.xmi` 是标准获取入口。

## 简报

UML 2.5.1 把状态机放进更大的对象建模体系中，形成工程界最常见的标准化状态机语言之一。它不仅定义行为状态机，还定义协议状态机，并用 metamodel + XMI 把图形建模、模型交换和工具生态绑定起来。

- 形式主义定位：面向软件/系统建模的标准化层次状态机。
- 构造方式简述：图形建模 + metamodel + XMI；核心章节集中在 State Machines clause。
- 基础设施与场景简述：规范直接给出 machine-readable XMI，适合模型驱动开发、交换、代码生成和工具互操作。

```text
系统/软件行为需求 -> UML 状态机模型 -> UML metamodel/XMI -> 工具链交换/分析/代码生成
```

## 形式主义定义与核心对象

### 定义对象

UML 状态机用于描述 classifier、组件、接口或协议在事件驱动下的生命周期与交互约束。

### 核心抽象

规范在 State Machines 章节下集中定义：

1. Behavior State Machines
2. Protocol State Machines
3. StateMachine class / Region / Pseudostate / Transition / Trigger 等元模型元素

### 语义边界

UML 状态机比原始 `Statecharts` 更工程化、更对象化，但也更复杂。它适合标准建模和交换，不像 `SCXML` 那样直接面向执行，也不像 `Timed Automata` 那样直接面向实时判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 状态、区域、伪状态齐备。 |
| 事件 / 触发 | 强支持 | trigger、event、operation invocation 完整。 |
| 守卫 / 数据 | 支持 | guard、effect、entry/exit/do behavior 支持丰富。 |
| 层次 | 强支持 | 复合状态与 submachine state 明确。 |
| 并发 / 同步 | 支持 | regions 支持并发区域。 |
| 时间约束 | 部分支持 | 可借助事件/约束表达，但非显式时钟自动机。 |
| 连续动态 / 随机性 | 不支持 | 不面向连续动力学。 |
| 可执行 / 可验证性 | 部分支持 | 规范面向建模与交换，执行/验证依赖外部工具。 |

## 构造方式与承载格式

### 建模入口

主要入口是 UML 建模工具中的状态机图，也可直接操作 metamodel/XMI。

### 机器可处理承载方式

规范直接给出 machine-readable XMI，包括 `UML.xmi`、`PrimitiveTypes.xmi`、`StandardProfile.xmi` 和 `UMLDI.xmi`。

### 交换与互操作

互操作是该规范的核心价值之一。它用 OMG 标准与 XMI 把不同工具链之间的模型交换固定下来。

## 配套基础设施

- 建模/编辑工具：规范支持广泛 UML 建模工具生态。
- 解析/交换/元模型支持：XMI 是核心。
- 仿真/执行支持：规范本身不附执行器，但为工具实现提供统一元模型。
- 验证/分析支持：形式化/模型检查路线通常围绕该标准做翻译或语义收束。
- 代码生成/转换支持：大量 MDE 工具依赖该标准。
- 标准化或社区生态：OMG 正式标准，生态成熟。

## 适用场景与需求前提

### 适用场景

适用于软件架构建模、嵌入式系统设计、接口协议约束建模以及需要跨工具交换的状态机工程流程。

### 需求前提

1. 需要与类、组件、接口、操作等 UML 语境联动。
2. 需要标准化 metamodel 和交换格式。
3. 需要层次状态与并发区域。

### 不适用或高成本场景

若目标是最小化语义复杂度或直接进入可执行运行时，UML 规范本身会显得偏重。

## 与相邻形式主义的关系

相对 `Statecharts`，它更标准化、对象化；相对 `SCXML`，它更偏通用建模和交换；相对 `Protocol State Machine` 的同规范内子类，它区分了行为状态机与协议状态机两条用途。

## 与本研究的关系

### 对 Project 1 的价值

它是“标准/基础设施”价值最高的状态机类型之一，能够直接回答状态机如何标准化承载和交换。

### 作为目标形式主义还是中间表示

可作为目标形式主义，也可作为向 `SCXML`、验证语言或代码生成目标转换的上游中间表示。

### 对需求到模型生成的启发

若 `project_1` 需要接入 MDE 生态，UML 状态机是很强的落点；但生成时必须控制语义子集，避免过度复杂。

### 现实限制

完整 UML 状态机语义过重，自动生成和形式验证通常需要 profile、子集约束或再翻译。

## 重要的相关工作

### 奠基或前身工作

- Harel Statecharts。

### 同类型或同家族工作

- Behavior State Machines。
- Protocol State Machines。

### 标准 / 格式 / 工具链工作

- XMI、UMLDI、工具链互操作。

### 与本研究关系最紧的工作

- UML 状态机形式化、验证翻译和可执行 profile 路线。

## 文献分类总结

- 主类：🧩
- 描述客体：🎛️
- 所属领域：💻
- 形式主义：UML State Machine
- 论文角色：标准规范
- 核心功能：提供标准化的行为/协议状态机建模语义与元模型。
- 关键特性：层次状态、并发区域、触发/守卫/效果、协议状态机、XMI。
- 构造方式：图形建模 + UML metamodel + machine-readable XMI。
- 基础设施：OMG 正式规范、XMI、广泛工具生态。
- 适用场景：MDE、跨工具交换、系统/软件行为建模。
- 需求前提：需要与 UML 语境集成并重视标准互操作。
- 状态：🟢
