# 分层状态机化的车队机动描述框架 / A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions

## 基本信息

- 标题：A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions
- 中文标题：分层状态机化的车队机动描述框架
- 作者：Corvin Deboeser, Jordan Ivanchev, Thomas Braud, Alois Knoll, David Eckhoff, Alberto Sangiovanni-Vincentelli
- 发表：IEEE Access, 9:128393-128406, 2021（当前 `paper.pdf` 为 arXiv 预印本）
- DOI：`10.1109/ACCESS.2021.3106455`
- 链接：https://doi.org/10.1109/ACCESS.2021.3106455
- 形式主义：`SEAD` framework / Manoeuvre Design Language (`MDL`)
- 主类：📦
- 描述客体：🤝
- 所属领域：🌡️
- 论文角色：领域特化框架 / 机动描述语言
- 工具/实现获取方式：原文明确给出在线 manoeuvre catalogue，并说明 `MDL` 及其 simulation parser 已实现；文中脚注直接给出 `https://github.com/sead-framework/manoeuvre-catalogue`。
- 标准/格式获取方式：承载方式是图形化层次状态机视图与 `JSON`-based `MDL` 文件；`MDL` 受 Amazon States Language 启发。

## 简报

这篇论文要解决的不是普通自动驾驶控制律，而是“车队协同行为到底怎么描述才不乱”。作者观察到现有 platooning manoeuvre 描述常常需要每辆车一台状态机，读者必须手工同步多台状态机才能看懂，还会出现概念层次不统一、动作模式重复和抽象深度混乱的问题。`SEAD` 因此把车队机动统一收束到一套分层状态机框架里：底层是 action primitives，中层是 sub-manoeuvres，高层是 manoeuvres；控制视角固定在 platoon leader，而其他车辆通过 reactive state machine 被动响应。

- 形式主义定位：面向 autonomous vehicle platooning 的层次化 manoeuvre 描述框架与 `JSON MDL` 语言。
- 构造方式简述：以 idle states、action primitives、sub-manoeuvres、PME/RSM 分工和 `SIM WRAPPER` 联合构造。
- 基础设施与场景简述：依托 online manoeuvre catalogue、`MDL`、simulation parser 和 leader-perspective 建模流程，服务 platoon join / split / gap close / lane change 等协同机动。

```text
platoon 协同需求 -> idle states + primitives + sub-manoeuvres -> PME / RSM + MDL(JSON) -> simulation / manoeuvre library / 机动验证
```

## 形式主义定义与核心对象

### 定义对象

`SEAD` 的核心对象不是单车控制器，而是“从 platoon leader 视角组织的协同机动”。它把车辆当前角色、可执行动作、通信消息和 reusable manoeuvre pattern 都编进同一层次状态机骨架里。

### 核心抽象

结合论文对 idle states、primitives、sub-manoeuvres 和 `MDL` 的定义，可保守整理为：

$$
\mathcal{S} = (I, P, U, M, \Sigma, \delta, \Gamma)
$$

上式中的符号逐项解释如下：

1. `I` 是 idle state 集合。
2. `P` 是 action primitive 集合。
3. `U` 是 sub-manoeuvre 集合。
4. `M` 是 manoeuvre 集合。
5. `\Sigma` 是车辆间通信消息集合。
6. `\delta` 是 leader-perspective 下的状态转移关系。
7. `\Gamma` 是 `MDL` 的 machine-readable 描述。

论文给出的典型 idle states 可压成：

$$
I = \{\mathrm{FV}, \mathrm{PF}, \mathrm{PL}, \mathrm{WFV}, \mathrm{WPF}, \mathrm{WPL}, \mathrm{TPL}\}
$$

其中：

1. `FV` 是 free vehicle。
2. `PF` 是 platoon follower。
3. `PL` 是 platoon leader。
4. `WFV / WPF / WPL` 是等待外部动作或指令时的不稳定 idle state。
5. `TPL` 是 temporary platoon leader。

论文对消息原语也给出了固定口径：

$$
\Sigma = \{\mathrm{REQ}, \mathrm{ORD}, \mathrm{DN}, \mathrm{ABT}, \mathrm{ACK}, \mathrm{NACK}, \mathrm{TMPL\_SPLIT}\}
$$

这些符号逐项解释如下：

1. `REQ` 是请求消息。
2. `ORD` 是 leader 下发的命令。
3. `DN` 是完成确认。
4. `ABT` 是 abort。
5. `ACK / NACK` 是接受 / 拒绝。
6. `TMPL_SPLIT` 是强制 temporary leader 分裂并中止当前 manoeuvre 的特种消息。

论文还把 simultaneous manoeuvre 包装为 `SIM WRAPPER`，并明确指出它可被理解为 controlling parts 的 product state machine：

$$
\mathrm{SIM}(U_1,\dots,U_k) = \prod_{i=1}^{k} PME(U_i)
$$

上式中的符号逐项解释如下：

1. `U_i` 是第 `i` 个 sub-manoeuvre。
2. `PME(U_i)` 是该 sub-manoeuvre 的 proactive controlling part。
3. `\prod` 表示它们在 leader 侧组合成乘积状态机。
4. 反应式部分则分散在各参与车辆的 `RSM` 中执行。

### 一个最小例子与通俗解释

论文给出的 `GAPCLOSE` 子机动非常适合作为最小例子：

1. platoon leader `A` 发送 `ORD_GAPCLOSE` 给 temporary leader `B`。
2. `B` 执行 `GAPCLOSE`，把 headway 调整到目标车距。
3. 若成功，`B` 发送 `DN_GAPCLOSE`，随后回到稳定 follower idle state。
4. 若超时，`A` 发送 `ABT` 并更新 platoon information；`B` 则转成 `PL` 并分裂出去。

通俗地说，`SEAD` 把“多车协同机动”拆成一组可复用的小协议块。每个协议块既规定物理动作，也规定消息往返、超时和失败后的角色回退，因此读者只需要站在 leader 视角看一条主线，就能理解整套机动。

### 运行 / 接受 / 转移语义

论文的核心运行直觉是：manoeuvre 从 leader 发起，其他车辆通过 reactive state machine 响应。可保守写成：

$$
\delta(i, p, \sigma) = i'
$$

其中：

1. `i \in I` 是当前 idle state。
2. `p \in P \cup U \cup M` 是 primitive、sub-manoeuvre 或 manoeuvre。
3. `\sigma \in \Sigma^*` 是当前通信与事件上下文。
4. `i'` 是执行后的新 idle state 或中间等待态。

对 sub-manoeuvre，论文强调所有参与者在 success 或 abort 上都必须落到已定义结果，可保守压成：

$$
\forall v \in participants(U),\ \exists r_v \in \{\mathrm{RS}, \mathrm{RA}_1, \dots\}
$$

$$
\text{abort}(v_i) \Rightarrow \forall v_j \neq v_i,\ \text{terminate}(v_j, r_j)
$$

上式中的符号逐项解释如下：

1. `participants(U)` 是参与子机动 `U` 的车辆集合。
2. `r_v` 是车辆 `v` 的已定义结束结果，如 success `RS` 或某类 abort。
3. 若某车辆触发 abort，其他参与车辆也必须在通信或超时驱动下终止到某个定义好的结果。
4. 这正是论文用来保证 Stability 的设计约束。

### 语义边界

`SEAD` 的边界也很明确：

1. 它建模的是 platooning layer 的协同行为，而不是 longitudinal / lateral continuous controller。
2. 它默认底层存在可靠通信与 regulation layer。
3. 它强调 leader perspective，因此不追求把每辆车的本地状态机都显式展开给人看。
4. 它不是通用协议自动机，而是强领域化的 vehicle platoon manoeuvre DSL。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 框架骨架 | `$\mathcal{S} = (I, P, U, M, \Sigma, \delta, \Gamma)$` | `SEAD` 同时编码角色状态、动作原语、子机动和机读语言。 |
| idle states | `$I = \{\mathrm{FV}, \mathrm{PF}, \mathrm{PL}, \mathrm{WFV}, \mathrm{WPF}, \mathrm{WPL}, \mathrm{TPL}\}$` | 车辆角色和等待态被固定成统一口径。 |
| 消息集合 | `$\Sigma = \{\mathrm{REQ}, \mathrm{ORD}, \mathrm{DN}, \mathrm{ABT}, \mathrm{ACK}, \mathrm{NACK}, \mathrm{TMPL\_SPLIT}\}$` | manoeuvre 协同明确依赖一套消息原语。 |
| simultaneous wrapper | `$\mathrm{SIM}(U_1,\dots,U_k) = \prod_{i=1}^{k} PME(U_i)$` | 同步机动由 leader 侧 controlling parts 的乘积状态机描述。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | idle state、idle super-state、sub-manoeuvre、manoeuvre 层次明确。 |
| 事件 / 触发 | 强支持 | `REQ / ORD / DN / ABT / ACK / NACK` 和 timeout 是主触发。 |
| 守卫 / 数据 | 部分支持 | 主要围绕角色、机动结果、消息和 platoon info，而不是复杂数据更新。 |
| 层次 | 强支持 | primitives -> sub-manoeuvres -> manoeuvres -> PME/RSM/LLI 层次清晰。 |
| 并发 / 同步 | 强支持 | `SIM WRAPPER` 把多子机动组合成 product state machine。 |
| 时间约束 | 部分支持 | timeout 是显式一等对象，但不是 clock automata 级时间语义。 |
| 连续动态 / 随机性 | 不支持 | 连续控制下沉到 regulation layer。 |
| 可执行 / 可验证性 | 强支持 | `MDL` 可机读，simulation system 解析后生成执行代码。 |

### 形式化问题与性质

1. `SEAD` 最关键的设计不是增加更多状态，而是通过 Standardisation / Encapsulation / Abstraction / Decoupling 压缩阅读和复用成本。
2. 相比“每车一台状态机”，它把控制主线固定在 leader 视角，其他车辆用 reactive machine 隐含执行。
3. `SIM WRAPPER` 的 product-state 解释让 simultaneous manoeuvre 不再只是口头并行。
4. `MDL` 把 manoeuvre 描述从图形草图推进到真正 machine-readable artefact。

## 构造方式与承载格式

### 建模入口

建模入口按层次组织：

1. `Action primitives`：如 `MTP`、`SH`、`BFV`、`BPL`、`W`、`SND`、`UPI`。
2. `Sub-manoeuvres`：如 `GAPCLOSE`、`LC_BPF`、`ATTACH`。
3. `Manoeuvres`：把多个 sub-manoeuvres 串接或并行组合。

### 机器可处理承载方式

机器可处理承载是 `JSON`-based `MDL`：

1. 每个 `MDL` 文件有唯一 ID / action ID。
2. 文件按固定语法描述 manoeuvre 或 sub-manoeuvre。
3. simulation system 会解析 `MDL` 并生成按 `SEAD` 框架执行所需的代码。

### 交换与互操作

`SEAD` 的互操作重点在：

1. `MDL` 与 graphical representation 之间可双向转换。
2. manoeuvre catalogue 作为共享库。
3. platooning system / simulation system 直接消费 `MDL`。

## 配套基础设施

- 建模/编辑工具：论文提出 graphical editor 路线，并已给出 manoeuvre catalogue。
- 解析/交换/元模型支持：`MDL` 基于 `JSON`，受 Amazon States Language 启发。
- 仿真/执行支持：simulation system 解析 `MDL` 并生成执行代码。
- 验证/分析支持：通过统一 manoeuvre 描述与角色结果定义，便于进一步做比较、优化与稳定性分析。
- 代码生成/转换支持：`MDL -> simulation code` 是原文明确给出的链路。
- 标准化或社区生态：当前更接近研究社区内的统一描述规范，而非行业通行标准。

## 适用场景与需求前提

### 适用场景

适合 autonomous highway / platooning 场景中的 join、split、gap close、lane change、merge 等协同机动设计与比较。

### 需求前提

1. 车辆角色和协同机动可以离散化成有限个 idle states 与 sub-manoeuvres。
2. 底层存在可用的 V2V 通信与 regulation layer。
3. 协同过程可按 leader-issued orders 和 follower reactions 组织。
4. 需要 machine-readable manoeuvre library，而不是只要论文图示。

### 不适用或高成本场景

若问题核心是连续控制稳定性证明、传感融合或单车轨迹优化，`SEAD` 本身不够；若通信极不可靠，还需要在原框架上补更多 timeout / recovery 机制。

## 与相邻形式主义的关系

相对“每参与者一台 FSM”的传统 manoeuvre 图，`SEAD` 更强调 leader perspective 和解耦；相对 `Communicating Finite-State Machines`，它更强领域化，并把物理 primitives、角色状态和 `MDL` 一起收进模型；相对一般 HSM，它的抽象层次直接面向 platoon protocol reuse。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很好地说明了“应用型状态机模型”怎样从多个散乱状态图演化成可比较、可复用、可机读的统一框架。对 `project_1` 来说，这正是状态机输出工件在领域落地时会遇到的问题。

### 作为目标形式主义还是中间表示

对 platooning manoeuvre synthesis，这可以直接作为目标形式主义；在更一般的研究链中，它也可以作为从抽象协同需求到领域执行框架之间的中间表示。

### 对需求到模型生成的启发

1. 领域特化状态机不一定追求通用表达力，而是先统一角色、动作原语和失败结果。
2. 同一机动可拆成 reusable sub-manoeuvre，再由高层 manoeuvre 组合。
3. 要让状态机真正服务工程比较和仿真，machine-readable 载体是必要条件。

## 重要的相关工作

- 论文综述的大量 platooning manoeuvre 图：说明现状主要是“多车多图、难同步阅读”。
- `Communicating Finite-State Machines` 与 interaction protocol 思路：构成其消息协同的背景。
- Amazon States Language：`MDL` 在语法和结构上直接借鉴了它的 machine-readable 风格。

## 文献分类总结

- 这是一篇典型的 `📦` 类领域状态机框架论文，核心不是抽象自动机理论，而是把 platoon manoeuvre 描述固化成可比较、可机读、可复用的工件。
- 其建模对象是多车协同协议与交互流程，因此记为 `🤝`；场景属于智能车辆与 CPS，因此记为 `🌡️`。
- 对 `project_1` 而言，它是“专用领域状态机怎样形成稳定建模口径”的高价值案例。
