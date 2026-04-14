# CIF 3：监督控制器的模型驱动工程 / CIF 3: Model-Based Engineering of Supervisory Controllers

## 基本信息

- 标题：CIF 3: Model-Based Engineering of Supervisory Controllers
- 中文标题：CIF 3：监督控制器的模型驱动工程
- 作者：D. A. van Beek，W. J. Fokkink，D. Hendriks，A. Hofkamp，J. Markovski，J. M. van de Mortel-Fronczak，M. A. Reniers
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 575-580，2014
- DOI：`10.1007/978-3-642-54862-8_48`
- 链接：https://doi.org/10.1007/978-3-642-54862-8_48
- 形式主义：`Compositional Interchange Format (CIF 3) / supervisory-controller engineering toolset`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：automata-based supervisory-control language + integrated toolchain
- 工具/实现获取方式：原文明确说明 `CIF` tooling 可从 `cif.se.wtb.tue.nl` 获取，并以 `MIT` 开源许可发布。
- 标准/格式获取方式：承载方式是 `CIF` 文本语言、到 `Uppaal` 的模型转换、`Matlab/Simulink` 共仿真接口，以及符合 `IEC 61131-3` 的 `PLC` 代码生成。

## 简报

这篇论文的核心贡献，不只是“又一个 DES synthesis 工具”，而是把监督控制器的整条工程链压进同一套 automata-based language/toolset：建模、监督控制综合、仿真验证、形式验证、可视化、实时测试、到 PLC 代码生成都在 `CIF 3` 里连起来。它补的是 supervisory-control 工程基础设施，而不是某个单点算法。

- 形式主义定位：面向 supervisory controllers 的 automata-based language + integrated toolchain。
- 构造方式简述：`CIF` 建 plant / observer / requirement models，做 synthesis 与 validation，再经 `Uppaal` / `Simulink` / `PLC` 路线输出分析或实现产物。
- 基础设施与场景简述：依托 `CIF` 文本语言、Eclipse editor、simulator、synthesis、`Uppaal` transformation、visualization、real-time testing 和 `IEC 61131-3` code generation，服务工业监督控制工程。

```text
plant / observer / requirements -> CIF model -> synthesis / simulation / verification -> observer-based supervisor -> PLC code / deployed controller
```

## 形式主义定义与核心对象

### 定义对象

论文把监督控制器工程链拆成以下核心对象：

1. uncontrolled hybrid plant。
2. hybrid observer。
3. uncontrolled discrete-event plant abstraction。
4. discrete-event control requirements。
5. synthesized supervisory controller。
6. observer-based supervisor。

### 核心抽象

结合论文的流程图，可把它的工程主链保守整理为：

$$
S = \mathrm{Synth}(P_{de}, R)
$$

$$
Sup = O_h \parallel S
$$

上式中的符号逐项解释如下：

1. `P_{de}` 是 uncontrolled discrete-event plant。
2. `R` 是离散事件控制需求。
3. `\mathrm{Synth}` 是 supervisory controller synthesis。
4. `S` 是生成得到的离散事件 supervisory controller。
5. `O_h` 是 hybrid observer。
6. `Sup` 是最终的 observer-based supervisor。

论文还明确说明 `CIF` 语言本体建立在 networks of hybrid automata 之上。按照文中描述，可把一个 `CIF` 模型保守整理为：

$$
M = (\mathcal{A}, E, V, Init, Inv)
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是 automata 集合。
2. `E` 是 shared events 与同步机制。
3. `V` 是离散/连续变量集合。
4. `Init` 是初始条件。
5. `Inv` 是 invariants 与演化约束。
6. 这组符号是根据论文“CIF is based on networks of hybrid automata”做的保守归纳，不是原文直接给出的正式元组。

如果把整条工作流写成更完整的工程链，可压缩为：

$$
(P_h, O_h) \leadsto P_{de} \xrightarrow{\mathrm{Synth}(R)} S \xrightarrow{\mathrm{Validate/Verify}} Sup \xrightarrow{\mathrm{CodeGen}} Code
$$

其中：

1. `P_h` 是 uncontrolled hybrid plant。
2. `O_h` 负责把连续变量世界桥接到离散事件世界，并产生 timeout 等 virtual sensor events。
3. `Code` 是最终生成的 real-time control code。

### 一个最小例子与通俗解释

论文给了一个很清晰的抽象例子：

1. 先建 uncontrolled hybrid plant。
2. hybrid observer 监视连续状态，并在出现 timeout 或特定物理量组合时发出附加事件。
3. 再手工抽象出 uncontrolled discrete-event plant。
4. 结合 control requirements 自动综合监督控制器。
5. 把 controller 与 observer 合成 observer-based supervisor，再去做 simulation、verification 和 code generation。

通俗地说，`CIF 3` 像“把监督控制从数学综合扩成完整工程流水线”的语言平台。它不只会算 supervisor，还关心前面的建模和后面的部署。

### 运行 / 接受 / 转移语义

论文没有在本文内给出完整语法语义，但给出了几个决定性的执行语义支点：

1. `CIF` 基于 hybrid automata network。
2. 组件通过 shared events、monitor automata、shared variables 等方式交互。
3. 支持 urgent events、stochastic distributions、multi-assignments 与 functions。

围绕监督控制综合，其核心可保守写成：

$$
P_{de} \parallel S \models \mathrm{Safe}
$$

$$
P_{de} \parallel S \models \mathrm{Live}
$$

上式中的符号逐项解释如下：

1. `P_{de}` 是离散事件 plant 抽象。
2. `S` 是综合得到的 supervisor。
3. `\mathrm{Safe}` 代表 synthesis “safe by construction”的目标。
4. `\mathrm{Live}` 代表论文提到可额外做的 liveness verification。
5. 这里的记号是基于论文流程图做的保守整理。

### 语义边界

这篇论文的边界也很明确：

1. 它是 tool/framework paper，不是 `CIF` 语法语义的完整定义文。
2. 完整语言扩展和 transformation algorithms 需要回看文中引用的技术报告。
3. 工业可用性很强，但很多验证、转换与代码生成都依赖所支持的 `CIF` 子集。
4. 监督控制主线最强，对一般非 supervisory model-based engineering 的覆盖不是重点。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 综合步骤 | `$S = \mathrm{Synth}(P_{de}, R)$` | 从离散事件 plant 与需求自动生成 supervisor。 |
| 控制器拼接 | `$Sup = O_h \parallel S$` | 最终控制器是 observer 与 supervisor 的组合。 |
| 语言骨架 | `$M = (\mathcal{A}, E, V, Init, Inv)$` | `CIF` 本体是 automata-based language。 |
| 工程链 | `$(P_h, O_h) \leadsto P_{de} \xrightarrow{\mathrm{Synth}} S \xrightarrow{\mathrm{CodeGen}} Code$` | `CIF 3` 的价值在于覆盖完整监督控制工程链。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 基于 automata / hybrid automata network。 |
| 事件 / 触发 | 很强 | shared events、urgent events、controllable/uncontrollable events 都是一等对象。 |
| 守卫 / 数据 | 很强 | rich data types、functions、conditional updates、multi-assignments 都支持。 |
| 层次 | 中等支持 | 通过 parametrized process definition、instantiation、sub-scopes 与 import 提供结构化能力。 |
| 并发 / 同步 | 很强 | multi-party synchronization、monitor automata 与 shared-variable interaction 并存。 |
| 时间约束 | 很强 | 既覆盖 discrete-event supervisory control，也覆盖 hybrid observer / plant 侧的时间行为。 |
| 连续动态 / 随机性 | 中等支持 | 支持 hybrid automata、non-linear/discontinuous DAE 与 stochastic distributions。 |
| 可执行 / 可验证性 | 很强 | synthesis、simulation、visualization、`Uppaal` verification、testing、code generation 一体化。 |

### 形式化问题与性质

1. 论文最重要的贡献，是把 supervisory-control 的“综合算法”扩成“从 plant 到部署”的统一工程流程。
2. `CIF` 不是只为离散事件模型服务，hybrid observer 和 hybrid plant 也是链路中的一部分。
3. 它和 `Supremica` 这类工具的差异，在于更强调完整的 language/toolchain integration。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 用 `CIF` 文本语言编 plant、observer、requirements 等模型。
2. 用 editor 做 syntax/type checking。
3. 进行 synthesis、simulation、verification、visualization。
4. 视需要导向 `Uppaal`、`Matlab/Simulink` 或 `PLC` code generation。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `CIF` 文本模型。
2. `Uppaal` 转换产物。
3. `Matlab/Simulink` S-function interface。
4. 符合 `IEC 61131-3` 的 `PLC` 代码。

### 交换与互操作

这篇论文的互操作重点在于：

1. `CIF -> Uppaal` 做验证。
2. `CIF <-> Matlab/Simulink` 做共仿真。
3. `CIF -> PLC code` 做工业部署。
4. 通过 model transformations、external functions 与 co-simulation 保持工具链开放性。

## 配套基础设施

- 建模/编辑工具：Eclipse-based textual editor。
- 解析/交换/元模型支持：syntax highlighting、background syntax/type checking、多种 model transformations。
- 仿真/执行支持：simulator、interactive visualization、real-time testing。
- 验证/分析支持：supervisory controller synthesis、liveness verification、`Uppaal` transformation。
- 代码生成/转换支持：`Matlab/Simulink` 共仿真与 `IEC 61131-3 PLC` code generation。
- 标准化或社区生态：`MIT` licensed `CIF` tooling、`Uppaal`、`Matlab/Simulink` 与 `PLC` 生态。

## 适用场景与需求前提

### 适用场景

适合工业监督控制、离散事件控制器综合、带 hybrid observer 的 CPS 控制工程，尤其是 MRI、baggage handling、printer 等工业自动化场景。

### 需求前提

1. 系统能被分解为 plant / observer / requirements / supervisor 这条控制工程链。
2. 控制目标适合 supervisory-control synthesis。
3. 团队愿意使用 automata-based textual language，而不是只画图。
4. 若要部署到 PLC/industrial stack，需要接受对应工具链约束。

### 不适用或高成本场景

如果需求更像开放式程序行为建模、而不是监督控制工程，`CIF 3` 的完整链条可能偏重。

## 与相邻形式主义的关系

相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，`CIF 3` 更强调完整建模-验证-部署链，而不只是 large-scale DES synthesis；相对 [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)，`BIP` 强在 layered component composition，`CIF` 强在 supervisory-controller engineering pipeline；相对 [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)，`UPP2SF` 是单桥接工具，而 `CIF 3` 是一整套语言与工具链。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 未来要把“生成-验证-修复”闭环落到工业控制场景，单有状态机本体还不够，最好同时考虑 observer、simulation、verification 和 deployment carrier。

### 作为目标形式主义还是中间表示

对工业监督控制问题，它可以是直接目标语言；对更一般的控制需求，它也可以作为靠近部署的工程中间表示。

### 对需求到模型生成的启发

1. 需求建模时应尽早区分 plant、observer、requirements 和 controller。
2. “虚拟传感器事件”这类 observer 机制，对把连续世界桥接到离散控制世界很重要。
3. 若要走工业落地路线，语言和工具链最好从一开始就考虑 code generation 与 co-simulation。

### 现实限制

它是一套偏重 supervisory-control 的工程平台，不是面向所有状态机需求的通用低门槛前端。

## 重要的相关工作

- [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)：大规模 DES supervisory-control IDE。
- [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)：另一条 component-based real-time engineering framework。
- [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)：验证后端到实现载体的桥接路线。
- [timed-controller-synthesis-an-industrial-case-study/desc.md](../timed-controller-synthesis-an-industrial-case-study/desc.md)：监督控制/实时综合在工业案例中的另一条落地路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`Compositional Interchange Format (CIF 3) / supervisory-controller engineering toolset`
- 论文角色：automata-based supervisory-control language + integrated toolchain
