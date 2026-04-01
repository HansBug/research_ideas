# 面向机器人的经验证仿真 / Verified Simulation for Robotics

## 基本信息

- 标题：Verified Simulation for Robotics
- 中文标题：面向机器人的经验证仿真
- 作者：Ana Cavalcanti, Augusto Sampaio, Alvaro Miyazawa, Pedro Ribeiro, Madiel Conserva Filho, André Didier, Wei Li, Jon Timmis
- 发表：*Science of Computer Programming*, 174:1-37, 2019
- DOI：`10.1016/j.scico.2019.01.004`
- 链接：https://doi.org/10.1016/j.scico.2019.01.004
- 形式主义：`RoboSim`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：仿真 DSL / 设计-仿真一致性验证
- 工具/实现获取方式：原文明确把 `RoboSim` 定位为 tool-independent diagrammatic notation，并说明已用 `FDR` 对语义与案例做验证，且自动生成仿真代码是既定目标。
- 标准/格式获取方式：承载方式是 `RoboSim` 图形模型、显式 cycle 定义、输入/输出寄存器抽象和 `tock-CSP` 语义；原文未给通用 XML/JSON 标准。

## 简报

`RoboSim` 解决的问题不是“再画一张机器人状态机图”，而是“如何把设计模型和仿真模型真正接起来”。论文指出，机器人文献里常见做法是先画一张状态机，再去某个仿真器里手写一个 cyclic program；两者之间没有严格对应。`RoboSim` 的做法是专门为 simulation 写一套 state-machine notation：所有行为围绕 cycle 展开，引入 `exec` 标记、显式的 input/output registers、基于周期的调度和与 `RoboChart` 设计模型的 refinement/conformance 检查。

- 形式主义定位：面向机器人仿真的 cyclic state-machine DSL，而不是一般行为设计语言。
- 构造方式简述：以 module / controller / simulation machine 定义结构，用 inputs、outputs、`exec`、cycle period 和寄存器读写来约束每个仿真周期。
- 基础设施与场景简述：依托 `RoboChart`、`RoboSim`、`tock-CSP`、`FDR` 和工具支持，服务 obstacle avoidance、transport swarm 等仿真一致性检查。

```text
RoboChart design -> scheduling assumptions + RoboSim cycle model -> tock-CSP semantics -> FDR conformance check -> verified simulation
```

## 形式主义定义与核心对象

### 定义对象

论文中的 `RoboSim` 核心对象包括：

1. module / controller / simulation machine：定义仿真结构。
2. cycle period：显式定义控制周期。
3. input / output registers：以寄存器方式刻画 sensors、actuators 和 event occurrence。
4. `exec`：特殊标记事件，表示本周期内可继续执行直到再次需要等待下个周期。
5. design-to-simulation mapping：把 `RoboChart` 设计对象映射到 `RoboSim` 仿真对象。

### 核心抽象

根据论文对 cyclic simulation machine 的描述，可保守整理单个 `RoboSim` 仿真状态机为：

$$
RS = (S, s_0, I, O, V, T, p)
$$

上式中的符号逐项解释如下：

1. `S` 是仿真状态集合。
2. `s_0 \in S` 是初始状态。
3. `I` 是输入集合，对应读入的寄存器。
4. `O` 是输出集合，对应待写回的寄存器或 operation call。
5. `V` 是局部变量与 clocks。
6. `T` 是转移集合。
7. `p` 是 cycle period。

论文特别强调 `exec` 是唯一真正推进周期内控制流的触发，因此可写成：

$$
T \subseteq S \times \{\mathrm{exec}\} \times G \times S
$$

其中：

1. `\mathrm{exec}` 是每个周期内触发状态推进的标记事件。
2. `G` 是 guard 条件集合，可引用输入寄存器、局部变量和 clocks。
3. 输入事件在 `RoboSim` 中不再作为 trigger，而是被编码成布尔寄存器变量。

### 一个最小例子与通俗解释

论文用一个简单 obstacle avoidance 例子来解释：

1. `RoboChart` 设计里，`Moving -> Turning -> Moving` 是功能逻辑。
2. 但仿真器真正做的是循环：读寄存器、执行控制逻辑、写回寄存器、等待一个周期。
3. 在 `RoboSim` 中，`obstacle` 不再是 transition trigger，而是像 `$obstacle` 这样的寄存器值。
4. 状态推进只在 `exec` 到来时检查。
5. 因而“设计里的事件触发”被精化成“周期性采样 + 寄存器条件 + 显式调度”。

通俗地说，`RoboSim` 不是让机器人“看见事件就立刻跳状态”，而是让仿真器在每个采样周期都问一次：“本周期读到了什么？哪些状态现在该推进？写回什么输出？”

### 运行 / 接受 / 转移语义

论文给出的仿真周期骨架可以浓缩为：

$$
\mathrm{Cycle}(p) = \mathrm{registerRead};\ \mathrm{Execute}^{*};\ \mathrm{registerWrite};\ \mathrm{wait}(p)
$$

上式中的符号逐项解释如下：

1. `\mathrm{registerRead}` 表示周期开始时读取传感器/输入寄存器。
2. `\mathrm{Execute}^{*}` 表示在本周期内执行零次或多次可立即推进的状态转移。
3. `\mathrm{registerWrite}` 表示把输出/operation call 写回寄存器。
4. `\mathrm{wait}(p)` 表示等待下一个采样周期。

单步执行可保守写成：

$$
(s, \sigma, \iota) \xrightarrow{\mathrm{exec}} (s', \sigma', \omega) \iff \exists\, (s,\mathrm{exec},g,s') \in T,\ g(\sigma,\iota)
$$

上式中的符号逐项解释如下：

1. `s`、`s'` 是当前与下一仿真状态。
2. `\sigma`、`\sigma'` 是本地变量与 clocks 环境。
3. `\iota` 是本周期刚读入的输入寄存器值。
4. `\omega` 是待写出的输出寄存器值。
5. `g(\sigma,\iota)` 决定在当前周期内是否可以推进该转移。

设计与仿真的关系则被表述为 refinement / conformance：

$$
\llbracket RS \rrbracket \sqsubseteq \llbracket D \rrbracket_{\mathrm{sched}}
$$

其中：

1. `D` 是 `RoboChart` 设计模型。
2. `\llbracket D \rrbracket_{\mathrm{sched}}` 是补入 scheduling assumptions 后的设计语义。
3. `RS` 只有在满足该 refinement 时，才算是设计的 sound simulation。

### 语义边界

`RoboSim` 的边界同样很清楚：

1. 它是 simulation notation，不直接替代 design notation。
2. 它强调 cyclic execution，因此与纯事件驱动状态机不同。
3. 它主要处理离散采样仿真，不直接覆盖连续物理环境模型。
4. 它的关键价值在 design-simulation traceability，而不是单独提高仿真逼真度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 仿真骨架 | `$RS = (S, s_0, I, O, V, T, p)$` | 仿真模型由状态、寄存器、周期和转移共同定义。 |
| 周期控制流 | `$\mathrm{Cycle}(p)=\mathrm{registerRead};\mathrm{Execute}^{*};\mathrm{registerWrite};\mathrm{wait}(p)$` | 明确给出每个仿真周期在做什么。 |
| 单步推进 | `$(s,\sigma,\iota)\xrightarrow{\mathrm{exec}}(s',\sigma',\omega)$` | `exec` 是周期内唯一驱动状态推进的触发。 |
| 一致性目标 | `$\llbracket RS \rrbracket \sqsubseteq \llbracket D \rrbracket_{\mathrm{sched}}$` | 仿真要对设计模型保持 refinement。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 依然用 state machine 表达仿真逻辑。 |
| 事件 / 触发 | 重解释 | 设计事件在仿真中被编码为寄存器变量，推进由 `exec` 驱动。 |
| 守卫 / 数据 | 强支持 | guards 直接读取寄存器和本地变量。 |
| 层次 | 支持 | 沿用模块/控制器/状态机分层，并可引用设计结构。 |
| 并发 / 同步 | 部分支持 | 支持组合设计，但论文重点在 cyclic machine 的语义与验证。 |
| 时间约束 | 强支持 | 通过周期 `p`、cycle semantics 与 clocks 表达仿真时间。 |
| 连续动态 / 随机性 | 不支持 | 物理环境与连续动力学不是本体重点。 |
| 可执行 / 可验证性 | 强验证 | 核心目标就是把 simulation 变成可验证对象。 |

### 形式化问题与性质

1. `RoboSim` 不是简单把 `RoboChart` 再画一遍，而是把 event-driven design 重写成 cycle-driven simulation。
2. 它显式解决了设计图通常不会写清的三件事：周期、寄存器清除/保留、同周期内调度。
3. 论文把“sound simulation”从工程直觉变成了 refinement 问题。
4. 这让后续自动生成 simulator-specific code 有了稳定的中间表示。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 定义 module、controller 和 simulation machine。
2. 为 module/controller/machine 明确 cycle period 约束。
3. 把设计里的 events/operations 重写为 inputs/outputs。
4. 以 `exec` 标记周期内可推进的控制位置。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. `RoboSim` 图形模型。
2. 基于寄存器的输入/输出表示。
3. `tock-CSP` 语义模型。

### 交换与互操作

`RoboSim` 的互操作重点在：

1. 与 `RoboChart` 设计模型建立映射与一致性检查。
2. 作为 simulator-independent 中间表示，后续面向不同仿真器生成代码。
3. 通过 `FDR` 检查 design-simulation refinement。

## 配套基础设施

- 建模/编辑工具：论文说明已有工具支持，并把 `RoboSim` 作为 diagrammatic notation 使用。
- 解析/交换/元模型支持：完整 metamodel、well-formedness conditions、input/output/event 重解释规则。
- 仿真/执行支持：目标是自动生成仿真代码；论文已把 cycle semantics 固定下来。
- 验证/分析支持：`tock-CSP`、`FDR`、design-simulation conformance checking。
- 代码生成/转换支持：自动生成仿真代码是明确目标，ARGoS 路线在文中被提及为进行中工作。
- 标准化或社区生态：研究型 notation，核心价值在工具无关与可验证性。

## 适用场景与需求前提

### 适用场景

适合需要证明“仿真程序没有偏离设计模型”的机器人开发场景，尤其是仿真周期、事件缓存与调度细节会影响结果的场合。

### 需求前提

1. 已有较抽象的设计模型，如 `RoboChart`。
2. 仿真是周期性的，而非纯异步事件驱动。
3. 团队关心 design-simulation consistency，而不只是仿真能跑。
4. 传感器、执行器和事件可抽象为寄存器读写。

### 不适用或高成本场景

若项目只做快速一次性仿真、不关心 traceability，`RoboSim` 可能显得过重；如果核心难点在连续物理建模，它也不是主要答案。

## 与相邻形式主义的关系

相对 `RoboChart`，它不是设计语言而是仿真语言；相对 `Stateflow` / 一般 simulator scripting，它更小、更受控，并以 design conformance 为中心；相对 `RobotML`、`rFSM`、`SmartSoft` 之类 DSL，它把 formal semantics 和 design-simulation relation 放在更核心的位置。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很重要，因为它说明状态机建模不仅有“设计态”语言，也需要“仿真态”语言，两者不能简单混为一谈。

### 作为目标形式主义还是中间表示

它更适合作为中间表示，尤其适合作为“设计模型到仿真代码”之间的受控桥梁。

### 对需求到模型生成的启发

1. 从需求自动生成状态机后，如果还要做仿真验证，最好再落一层专门的仿真中间表示。
2. 设计里的事件和仿真里的寄存器并不是同一件事，必须显式转换。
3. 只有把 scheduling assumptions 写进模型，仿真结果才真正可追溯。

## 重要的相关工作

- `RoboChart`：是其直接对应的设计语言。
- `Stateflow`、`Simulink`、`Webots`、`V-REP`、`ARGoS`：代表更一般的仿真环境与语言。
- `RobotML`、`rFSM`、`SmartSoft`、`GenoM`：代表邻近的机器人 DSL 或执行语言路线。

## 文献分类总结

- 这是一篇 `📦` 类高价值条目，重点在仿真 DSL 与 design-simulation 一致性验证，而不是单独提出新的机器人控制理论。
- 其描述客体是机器人控制/仿真行为逻辑，因此记为 `🎛️`；论文语境是机器人/CPS 工程，因此记为 `🌡️`。
- 对 `project_1` 来说，它补上了“状态机设计模型之后，如何进入可验证仿真模型”的关键中间层。
