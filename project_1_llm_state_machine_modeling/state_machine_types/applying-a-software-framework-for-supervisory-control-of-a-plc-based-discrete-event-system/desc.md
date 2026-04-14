# 将监督控制软件框架应用于基于 PLC 的离散事件系统 / Applying a Software Framework for Supervisory Control of a PLC-Based Discrete Event System

## 基本信息

- 标题：Applying a Software Framework for Supervisory Control of a PLC-Based Discrete Event System
- 中文标题：将监督控制软件框架应用于基于 PLC 的离散事件系统
- 作者：B. Curto，V. Moreno，C. Fernández-Caramés，R. Alves，A. Chehayeb
- 发表：*Proceedings of the 6th International Conference on Informatics in Control, Automation and Robotics*，pp. 262-267，2009
- DOI：`10.5220/0002211502620267`
- 链接：https://doi.org/10.5220/0002211502620267
- 形式主义：`DFSA-based supervisory-control framework / PLC service repository`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：PLC supervisory-control framework / service-level supervision infrastructure
- 工具/实现获取方式：原文给出的实现对象是 `PLC + conveyor belt + IMC 110` 工业单元，未给独立公开仓库或下载入口。
- 标准/格式获取方式：主承载是 `DFSA` plant/specification、synchronous parallel composition、service repository 和 PLC 运行逻辑；不是中立交换标准。

## 简报

这篇论文的重要性不在提出新的 `DES` 形式主义，而在把监督控制从“只在理论里综合 controller”往“PLC 上可维护、可改任务、少改代码的软件框架”推进了一步。作者的核心判断是：工艺变化时，不应该每次都重写 PLC 业务代码；更好的做法是把功能服务和 supervision 分层，服务实现尽量稳定，真正变化的是外部请求这些服务的顺序，以及由监督器临时禁止哪些输入事件。

- 形式主义定位：这是 `SCT + DFSA + PLC` 的执行基础设施条目，不是新的自动机母型。
- 构造方式简述：`plant DFSA + modular specifications -> synchronous composition supervisor -> event gating -> service repository on PLC`。
- 基础设施与场景简述：依托 `DFSA`、`SCT`、service repository、外部接口与 PLC 设备层，服务制造单元和经常换任务顺序的柔性生产场景。

```text
external request -> supervisor checks enabled input event -> plant DFSA transition -> PLC service execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 用 `DFSA` 描述 plant。
2. 用一个或多个 `DFSA` 描述 restrictions / specifications。
3. 用 synchronous parallel composition 得到 supervised behavior。
4. 在 PLC 软件层把 supervision 与 service functionality 分离。

### 核心抽象

论文直接把 plant 写成 deterministic finite state automaton：

$$
G = (X, \Sigma_G, f_G, \Gamma_G, x_0, X_m)
$$

上式中的符号逐项解释如下：

1. `$X$` 是状态集合。
2. `$\Sigma_G$` 是 plant 的事件集合。
3. `$f_G : X \times \Sigma_G \to X$` 是状态转移函数。
4. `$\Gamma_G : X \to 2^{\Sigma_G}$` 是 active-event function。
5. `$x_0$` 是初始状态。
6. `$X_m$` 是 marked states，表示某项任务完成。

restriction / specification 也写成同类 `DFSA`：

$$
H = (Y, \Sigma_H, f_H, \Gamma_H, y_0, Y_m)
$$

上式中的符号逐项解释如下：

1. `$Y$` 是 specification 的状态集合。
2. `$\Sigma_H$` 是 specification 相关事件。
3. `$f_H$` 与 `$\Gamma_H$` 分别是状态转移函数和 active-event function。
4. `$y_0$` 是初始状态。
5. `$Y_m$` 是 marked states。

论文采用的监督组合对象是 synchronous parallel composition：

$$
G \parallel H = Ac(X \times Y,\ \Sigma_G \cup \Sigma_H,\ f_{G\parallel H},\ \Gamma_{G\parallel H},\ (x_0,y_0),\ X_m \times Y_m)
$$

上式中的符号逐项解释如下：

1. `$Ac(\cdot)$` 表示只取从初始状态可达的 accessible 部分。
2. `$X \times Y$` 是组合状态空间。
3. `$\Sigma_G \cup \Sigma_H$` 是组合后的事件字母表。
4. `$f_{G\parallel H}$` 是同步并行下的组合转移函数。
5. `$\Gamma_{G\parallel H}$` 是组合后的 active-event function。
6. marked states 只有在 plant 和 specification 都接受时才成立。

framework 层的核心思想则可保守整理成：

$$
A = G \cup H_1 \cup \cdots \cup H_k,\qquad S = G \parallel H_1 \parallel \cdots \parallel H_k
$$

上式中的符号逐项解释如下：

1. `$H_1,\ldots,H_k$` 是多个 modular specifications。
2. `$A$` 表示框架内部维护的 automata 集合。
3. `$S$` 表示真正起监督作用的同步组合结果。
4. 外部请求的可控输入事件只有在 `$S$` 当前状态允许时才会传给 plant 并触发服务。

### 一个最小例子与通俗解释

论文的 case study 是 conveyor belt：

1. plant `G` 同时描述 manual / automatic mode、传送带移动状态和 emergency stop 状态。
2. 两个 restrictions `H_1`、`H_2` 分别规定：未完成 homing 之前，不能执行到目标位置的移动，也不能切到 automatic mode。
3. 外部系统请求服务时，会先把对应事件发给 supervisor。
4. 若该事件在组合自动机里当前不可用，服务就不会执行，因此 PLC 业务代码本身不用为每种任务变化重写。

通俗地说，这个框架想做的是“把 PLC 功能服务做成积木，把 supervision 做成闸门”。服务代码尽量不动，真正变化的是哪些服务现在准许调用。

### 运行 / 接受 / 转移语义

框架级运行语义可以保守写成：

$$
e_i \in \Sigma_c \Rightarrow e_i \text{ 先经 } \Gamma_A \text{ 判定是否可用，再进入 } f_A
$$

上式中的符号逐项解释如下：

1. `$e_i$` 是外部触发的可控输入事件。
2. `$\Sigma_c$` 是 controllable events。
3. `$\Gamma_A$` 负责看当前 plant/specification 组合状态下这个事件是否启用。
4. 若允许，则再交由组合自动机的转移函数推进状态，并触发对应服务执行。

论文的监督目标仍然是经典 `SCT` 式约束：

$$
L(S) \subseteq L(G)
$$

上式中的符号逐项解释如下：

1. `$L(G)$` 是 plant 行为语言。
2. `$L(S)$` 是 supervised system 的行为语言。
3. supervision 通过临时禁用输入事件，把行为限制在满足 specification 的子语言内。
4. 论文的创新在于把这个 restriction 落到 service-oriented PLC framework。

### 语义边界

1. 论文主体是 `DFSA + SCT` 的 PLC 框架，不是新的 `DES` 本体。
2. 关注的是服务调用顺序的 supervision，而不是复杂数据流或连续控制。
3. case study 证明了技术可行性，但生态明显偏工程实验室级实现。
4. 形式语义主要落在离散事件层，时间行为只体现为 PLC 同步扫描背景。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| plant `DFSA` | `$G = (X, \Sigma_G, f_G, \Gamma_G, x_0, X_m)$` | 被监督对象的离散事件模型。 |
| specification `DFSA` | `$H = (Y, \Sigma_H, f_H, \Gamma_H, y_0, Y_m)$` | 用 restriction 建模不允许的服务顺序。 |
| 同步组合 | `$G \parallel H = Ac(\cdots)$` | 监督通过同步 composition 生效。 |
| framework 核心 | `$S = G \parallel H_1 \parallel \cdots \parallel H_k$` | 多个模块化 specification 可以并行约束同一 plant。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接用 `DFSA` 描述设备模式与服务约束。 |
| 事件 / 触发 | 很强 | supervision 的核心就是对输入事件进行启用/禁用。 |
| 守卫 / 数据 | 弱支持 | 主体是离散事件与服务顺序，不是复杂数据。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 支持多个 specification 与 plant 的同步组合，但不主打高并发语义。 |
| 时间约束 | 弱支持 | 只有 PLC 扫描与设备动作背景，不是 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 纯离散事件 supervision。 |
| 可执行 / 可验证性 | 很强 | 直接面向 PLC 与实际 conveyor-belt 单元实现。 |

### 形式化问题与性质

1. 这篇论文真正补的是 supervisory-control 的软件框架层，而不是单次 controller synthesis 算法。
2. 它强调 service implementation 与 supervision policy 解耦，这对工业维护很重要。
3. modular specifications `H_i` 的做法也符合后续 supervisory-control 工具链常见工程口径。
4. 对本论文集而言，它是 `PLC deployment / service-level supervisory framework` 的一个较早支点。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. plant `DFSA`。
2. 一个或多个 restrictions `DFSA`。
3. service repository 与外部请求接口。
4. PLC 设备层动作实现。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `DFSA` 状态图。
2. synchronous parallel composition。
3. active-event function。
4. PLC 上的服务调用逻辑。

### 交换与互操作

论文没有给独立交换标准；互操作重点在“外部请求接口 -> supervisor -> plant/service execution”这条框架链路，而非开放文件格式。

## 配套基础设施

- 建模/编辑工具：原文没有给专用建模器，主要依赖 `DFSA` 建模与 PLC 编程环境。
- 解析/交换/元模型支持：基于 `DFSA`、active-event function 与 synchronous composition 的轻量建模口径。
- 仿真/执行支持：真实 `PLC + conveyor belt + IMC 110` 单元。
- 验证/分析支持：由 `SCT` 的组合模型保证服务调用顺序不违背 restrictions。
- 代码生成/转换支持：论文更像框架设计与手工实现，不是自动代码生成器。
- 标准化或社区生态：依托 `SCT`、`DFSA` 与 `PLC` 工业控制实践。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 工业单元已有一组较稳定的 PLC 功能服务，但任务流程经常变化。
2. 重点约束是服务调用顺序、安全模式切换、homing / mode switching 之类的离散逻辑。
3. 希望 supervision 和业务实现解耦，以降低维护成本。

### 需求前提

1. 系统必须能较稳定地抽象成 `DFSA`。
2. 可控输入事件与不可控内部事件的边界需要明确。
3. 约束最好能表达成 modular specifications，而不是复杂数值优化目标。
4. PLC 工程栈允许把服务调用包装成离散事件。

### 不适用或高成本场景

若系统严重依赖连续控制、复杂数据处理或强分布式异步交互，仅靠这种 `DFSA + PLC service` 框架会显得过窄。

## 与相邻形式主义的关系

相对 [plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md](../plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md)，那篇更偏 `Supremica -> Structured Text` 自动代码生成，这篇更早且更强调 service repository 框架；相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，这篇没有大型 symbolic synthesis 基础设施，而是把 supervision 和 PLC 服务层解耦；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，本文更偏具体 PLC 服务框架，而不是完整模型驱动工程工作台。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `FSM/DFSA` 线不仅有模型本体，还有较早的工业执行框架证据。
2. 若以后要把自动生成出的控制模型真正下放到工业执行环境，service-level gating 是很现实的一层。
3. 它也提醒我们，很多工程落地并不要求复杂新语言，关键是把控制逻辑和服务实现分层。

### 作为目标形式主义还是中间表示

更适合作为执行基础设施和落地框架，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 需求若天然可写成“哪些服务可在什么前提下调用”，就很适合先生成 `DFSA + specifications`。
2. 约束可以优先结构化为 modular restrictions，而不是混成一个大 supervisor。
3. 如果最终部署目标是 PLC，需求阶段就应尽量明确 controllable / uncontrollable event 边界。

### 现实限制

它证明了框架可行，但缺少后续那种成熟 IDE、开放工具链和自动代码生成生态，因此更像基础实践支点而不是现代主流平台。

## 重要的相关工作

### 奠基或前身工作

- Ramadge-Wonham `SCT` 母线。
- 基于 `DFSA` 的离散事件监督控制建模。

### 同类型或同家族工作

- [plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md](../plc-implementation-of-symbolic-modular-supervisory-controllers/desc.md)
- [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)

### 标准 / 格式 / 工具链工作

- `PLC`、service repository、同步 composition supervisor 是本文核心基础设施。

### 与本研究关系最紧的工作

- [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)
- [overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md](../overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md)

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`DFSA-based supervisory-control framework / PLC service repository`
- 论文角色：PLC supervisory-control framework / service-level supervision infrastructure
- 核心功能：把 `SCT` 的事件禁用逻辑嵌入 service-oriented PLC 软件框架，降低任务变化时的重编程成本。
- 关键特性：`DFSA`、modular specifications、synchronous composition、service repository、event gating、PLC execution。
- 构造方式：`plant DFSA + restrictions DFSA + synchronous composition + service execution framework`。
- 基础设施：PLC、外部接口、supervisor、service repository、conveyor-belt case study。
- 适用场景：柔性制造单元、任务顺序频繁变化但基础服务相对稳定的工业控制系统。
