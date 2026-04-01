# 对 RSML-e 需求进行模型检查 / Model Checking RSML-e Requirements

## 基本信息

- 标题：Model Checking RSML-e Requirements
- 中文标题：对 RSML-e 需求进行模型检查
- 作者：Yunja Choi, Mats P. E. Heimdahl
- 发表：Proceedings of the 7th IEEE International Symposium on High Assurance Systems Engineering, 109-118, 2002
- DOI：`10.1109/HASE.2002.1173111`
- 链接：https://doi.org/10.1109/HASE.2002.1173111
- 形式主义：`RSML-e` / `NuSMV` translation framework
- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：验证工具链 / 翻译框架
- 工具/实现获取方式：原文明确给出 `Nimbus` simulator、`RSML-e -> NuSMV` translator 和 `PVS`/`NuSMV` 验证流程。
- 标准/格式获取方式：承载方式是 `RSML-e` 文本/图形规格、`NuSMV` 模块、`CTL/LTL` 性质；无独立行业交换标准。

## 简报

这篇论文的价值不在于重新定义 `RSML-e`，而在于把它真正推到“可例行验证”的程度。作者围绕 `RSML-e` 的层次状态变量、接口、宏和同步数据流语义，做了一条尽量保结构、尽量少人工干预的 `NuSMV` 翻译链，让需求分析阶段就能做 push-button model checking。

- 形式主义定位：面向高保证需求规格的状态机语言与自动验证桥接框架。
- 构造方式简述：用 `RSML-e` 写需求规格，用 translator 映射到 `NuSMV` 的 `VAR/ASSIGN/MODULE`，再用 `CTL/LTL` 检查性质。
- 基础设施与场景简述：依托 `Nimbus`、`NuSMV` 与 `PVS`，服务飞控等 safety-critical requirement analysis。

```text
控制需求 -> RSML-e state variables / interfaces / macros -> 自动翻译到 NuSMV -> CTL/LTL 验证
```

## 形式主义定义与核心对象

### 定义对象

论文把 `RSML-e` 看成一种同步数据流式的 requirements state machine language。它最核心的对象不是代码模块，而是输入变量、层次状态变量、输入输出接口、函数、宏和常量。

### 核心抽象

结合论文的语言说明，可保守整理为：

$$
R = (V_{in}, V_{st}, I_{in}, I_{out}, F, M, C)
$$

上式中的符号逐项解释如下：

1. `V_{in}` 是输入变量集合。
2. `V_{st}` 是状态变量集合，且可层次化组织。
3. `I_{in}` 是输入接口集合。
4. `I_{out}` 是输出接口集合。
5. `F` 是函数集合。
6. `M` 是宏集合。
7. `C` 是常量集合。

论文中 `RSML-e` 的表格语义可以压成：

$$
Table = \bigvee_j \bigwedge_i \phi_{ij}
$$

其中：

1. 每一列 `j` 表示一个 conjunction。
2. 每个单元 `\phi_{ij}` 可为真、假或 don't care。
3. 整张表表示这些列的析取。

论文还明确讨论了 `PREV` 和 `next` 的翻译选择，其关键映射可写成：

$$
next(x) := f(x, next(y))
$$

上式中的符号逐项解释如下：

1. `x` 表示当前变量的旧值。
2. `next(y)` 表示当前 step 中其他变量的新值。
3. 该映射把 `RSML-e` 中无 `PREV` 的表达式对应到 `NuSMV` 的 `next` 语义。

### 一个最小例子与通俗解释

论文用 `AltitudeStatus` 这个状态变量演示了整个思路：

1. `AltitudeStatus` 是 `PowerStatus.On` 的子状态变量。
2. 它可取 `Unknown / Above / Below / AltitudeBad` 等枚举值。
3. 是否进入 `Below`、`Above` 或 `AltitudeBad` 由 `EQUALS` 子句中的表格条件决定。
4. 输入/输出接口又能表达“消息来了怎么赋值”“每 200ms 何时发 fault message”。

通俗地说，`RSML-e` 像“把 Statecharts 的状态骨架、SCR 风格表格逻辑和环境接口规约拼在一起”的需求 DSL，而这篇论文做的事就是把它自动翻译成可检查的符号模型。

### 运行 / 接受 / 转移语义

论文强调 `RSML-e` 是同步数据流语义，没有内部 broadcast events。状态变量更新依据 next-state relation 和表格条件。一个典型翻译结果是：

$$
next(AltitudeStatus) := \mathrm{case}\ \cdots\ \mathrm{esac}
$$

其中：

1. `AltitudeStatus` 的下一值由表格条件分支选择。
2. 这些条件又可能依赖宏展开结果、接口状态和 `PREV` 值。

对宏的翻译，论文还给出子模块骨架：

$$
MODULE\ m(\cdots), \quad next(result) := condition
$$

也就是：

1. 每个宏或函数可变成 `NuSMV` 子模块。
2. `result` 变量记录该宏的计算值。

### 语义边界

这篇论文也明确了边界：

1. 时间变量和数值变量需要抽象，不能无损直接塞进有限状态模型。
2. 模型检查目标是需求规格，不是完整实现代码。
3. 论文力求保留 `RSML-e` 结构，但仍需在时间、数值和接口上做自动抽象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 规格骨架 | `$R = (V_{in}, V_{st}, I_{in}, I_{out}, F, M, C)$` | `RSML-e` 由变量、接口、函数和宏组成。 |
| 表格语义 | `$Table = \bigvee_j \bigwedge_i \phi_{ij}$` | `EQUALS` 表格本质是 DNF 条件。 |
| next 翻译 | `$next(x) := f(x, next(y))$` | `PREV`/当前值被映射到 `NuSMV` 的 next-state 语义。 |
| 性质语言 | `$\varphi \in CTL \cup LTL$` | 用户在 `NuSMV` 中用 `CTL/LTL` 表达需求性质。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 层次状态变量是语言核心。 |
| 事件 / 触发 | 强支持 | 状态变化由表格条件、接口消息和 reset 类条件触发。 |
| 守卫 / 数据 | 强支持 | 表格、宏、函数和接口条件共同构成复杂 guard。 |
| 层次 | 强支持 | 父子状态变量提供比传统 Statecharts 更简单的层次语义。 |
| 并发 / 同步 | 部分支持 | 强调同步数据流 step 语义，但非通用并发编程模型。 |
| 时间约束 | 部分支持 | 支持时间相关表达式，但翻译到 `NuSMV` 时需抽象。 |
| 连续动态 / 随机性 | 不支持 | 聚焦离散需求规格。 |
| 可执行 / 可验证性 | 强支持 | `Nimbus` 可执行，`NuSMV/PVS` 可验证。 |

### 形式化问题与性质

1. `RSML-e` 去掉了内部 broadcast events，语义比传统 `Statecharts` 更收束。
2. 输入/输出接口是第一等对象，因此可直接写环境交互性质。
3. 翻译目标是“尽量保结构”，让 counterexample 对工程师可读。
4. 抽象重点在时间、接口和数值变量，而不是盲目大规模手工建模缩减。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `STATE_VARIABLE` 定义。
2. `IN_INTERFACE / OUT_INTERFACE` 规格。
3. `TABLE`、`MACRO`、`FUNCTION`。
4. `PREV_STEP`、时间表达式和消息相关表达式。

### 机器可处理承载方式

机器可处理承载是两层：

1. `RSML-e` 规格文本与 `Nimbus` 的图形视图。
2. 翻译后的 `NuSMV` 模块、变量和赋值语句。

### 交换与互操作

论文的“交换”不是行业中立格式，而是研究型验证互操作：`RSML-e -> NuSMV` 和 `RSML-e -> PVS`。

## 配套基础设施

- 建模/编辑工具：`Nimbus`。
- 解析/交换/元模型支持：translator 自动把 `RSML-e` 映射到 `NuSMV` 和 `PVS` 输入语言。
- 仿真/执行支持：`Nimbus simulator` 用于早期行为评估。
- 验证/分析支持：`NuSMV` 提供 `CTL/LTL` model checking，`PVS` 提供定理证明路线。
- 代码生成/转换支持：本文聚焦验证翻译，不直接做代码生成。
- 标准化或社区生态：生态集中于高保证需求工程与 NASA/飞控场景，不是通用工业标准。

## 适用场景与需求前提

### 适用场景

适合飞控、嵌入式控制、高保证系统等需求分析阶段，希望在实现前就做状态机级验证的场景。

### 需求前提

1. 需求能整理成有限状态变量和表格化条件。
2. 系统与环境之间的消息接口需要被显式建模。
3. 希望 counterexample 能回映到原始需求结构。
4. 能接受时间和数值变量在验证时被自动抽象。

### 不适用或高成本场景

如果目标是直接部署执行、表达连续物理过程或开放交换标准，`RSML-e + NuSMV` 这条线不是最自然的最终工件。

## 与相邻形式主义的关系

相对 `RSML/Statecharts`，它去掉内部广播事件并强化接口规格；相对 `SpecTRM-RL`，它更突出自动翻译与模型检查；相对原生 `NuSMV`，它更贴近需求工程师的状态/接口视角。

## 与本研究的关系

### 对 Project 1 的价值

它几乎直接命中 `project_1` 的关键问题：怎样把自然语言控制需求先收束成结构化状态机需求，再接入验证器，而不是直接跳到代码或平面状态图。

### 作为目标形式主义还是中间表示

更适合作为高可信需求侧中间表示，以及通往验证工件的前端载体。

### 对需求到模型生成的启发

如果未来要让 LLM 生成“可验证的需求状态机”，`RSML-e` 这种由层次状态变量、接口和表格组成的结构，比随意生成图形状态图更稳。

### 现实限制

时间/数值抽象仍是瓶颈；它更适合 requirements verification，而不是最终执行平台。

## 重要的相关工作

### 奠基或前身工作

- `RSML`
- `Statecharts`
- `SCR` 风格表格逻辑

### 同类型或同家族工作

- `SpecTRM-RL`
- `PVS`-based requirements verification
- 需求到模型检查器的自动翻译路线

### 标准 / 格式 / 工具链工作

- `Nimbus`
- `NuSMV`
- `PVS`

### 与本研究关系最紧的工作

- 它把“需求状态机”与“按键式自动验证”连成了真实工作流，是需求到模型闭环里极强的先例。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`RSML-e` / `NuSMV` translation framework
- 论文角色：验证工具链 / 翻译框架
- 核心功能：把高保证需求状态机规格自动翻译到可模型检查的符号模型。
- 关键特性：层次状态变量、接口规格、表格逻辑、自动抽象、`CTL/LTL` 验证。
- 构造方式：`RSML-e` 文本/图形规格 + translator + `NuSMV` 模块。
