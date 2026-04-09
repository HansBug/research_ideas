# 基于 MATLAB Simulink Stateflow 的监督控制理论教学工具箱 / An educational toolbox on supervisory control theory using MATLAB Simulink stateflow

## 基本信息

- 标题：An educational toolbox on supervisory control theory using MATLAB Simulink stateflow: From Theory to practice in one week
- 中文标题：基于 MATLAB Simulink Stateflow 的监督控制理论教学工具箱
- 作者：Claudius Jordan，Canlong Ma，Julien Provost
- 发表：*2017 IEEE Global Engineering Education Conference (EDUCON)*，pp. 632-639，2017
- DOI：`10.1109/EDUCON.2017.7942912`
- 链接：https://doi.org/10.1109/EDUCON.2017.7942912
- 形式主义：`Supervisory Control Theory / DFA / MATLAB Simulink Stateflow / MSCI`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：`Stateflow`-based supervisory-control teaching and implementation toolbox
- 工具/实现获取方式：原文明确说明 `MSCI` 建立在 `MATLAB Simulink`、`MATLAB Stateflow` 与 `DECK` 之上，用于把 `Stateflow` 模型转换成形式化表示、自动生成 supervisor 并封装成可执行 `Simulink` 闭环模型；论文未给独立公开仓库。
- 标准/格式获取方式：承载方式是 `Stateflow` chart、Simulink model、signal/event database、`DECK` 内部 `DFA` 表示与最终可执行控制单元；无独立中立交换标准。

## 简报

这篇论文补的是 supervisory-control 落到工业常用建模环境的一条桥：不是让学生和工程师直接在独立 `DES` 工具里画 automata，而是让他们在熟悉的 `MATLAB/Stateflow` 里建 plant、specification 和 technological constraints，再由 `MSCI` 自动完成形式化转换、supervisor synthesis 和可执行 Simulink 闭环拼装。它更像一个“教学与工程过渡层”。

- 形式主义定位：监督控制理论的 `Stateflow/Simulink` 工具载体，而不是新的状态机本体。
- 构造方式简述：`Stateflow plant/specification/constraints -> formal DFA -> DECK supervisor synthesis -> executable Simulink model`。
- 基础设施与场景简述：依托 `MATLAB`、`Stateflow`、`Simulink`、`DECK`、signals-events database 与 didactic platform，服务 supervisory-control 教学、实验台控制与工业接受度过渡。

```text
physical plant + signal database -> Stateflow automata -> formal DES model -> supervisor -> executable Simulink control loop
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. discrete-event system (`DES`)；
2. deterministic finite automaton (`DFA`)；
3. controllable / uncontrollable events；
4. `Stateflow` 建模入口与 `DECK` 形式化后端；
5. `MSCI` 生成的 executable Simulink closed-loop model。

### 核心抽象

论文直接给出 `DFA` 骨架：

$$
G = \langle Q, \Sigma, \delta, q_0, Q_m \rangle
$$

上式中的符号逐项解释如下：

1. `$Q$` 是有限状态集合。
2. `$\Sigma$` 是事件字母表。
3. `$\delta : Q \times \Sigma \to Q$` 是偏迁移函数。
4. `$q_0$` 是初始状态。
5. `$Q_m \subseteq Q$` 是 marked states 集合。

论文同时明确使用 controllable / uncontrollable 事件划分，可写成：

$$
\Sigma = \Sigma_c \uplus \Sigma_u
$$

上式中的符号逐项解释如下：

1. `$\Sigma_c$` 是由 supervisor 施加的 controllable events。
2. `$\Sigma_u$` 是由 plant 侧产生的 uncontrollable events。
3. 论文用信号上升沿/下降沿与 event queue 把物理 I/O 转成这两类事件。

结合文中工作流，可把 `MSCI` 的工程链保守整理为：

$$
\mathrm{MSCI}(M_{sf}, D) = \mathrm{SimulinkModel}(\mathrm{Synth}(\mathrm{DFA}(M_{sf}, D)))
$$

上式中的符号逐项解释如下：

1. `$M_{sf}$` 是 `Stateflow` 中的图形 automata 模型。
2. `$D$` 是 signal / event database。
3. `$\mathrm{DFA}(M_{sf}, D)$` 表示把图形模型转成正式 `DFA`。
4. `$\mathrm{Synth}$` 表示 `DECK` 上的 supervisor synthesis。
5. 输出是包含 supervisor、event queue 和 signal conversion 的 executable `Simulink` 模型。

### 一个最小例子与通俗解释

论文里的 didactic platform 很适合解释这条路：

1. 学生先在 `Plant`、`Specification`、`Technological_Constraints` 三个顶层 superstate 里建 `Stateflow` automata。
2. 例如某个 pusher 由 supervisor 发送 `start` 事件启动，本地控制器完成动作后再发 `done` 事件。
3. 若某处没有实体传感器，也可以用 virtual sensor 根据时间或其他信号推导出内部事件。
4. `MSCI` 最终把这些图形 automata 转成 formal supervisor，并封装进可执行 Simulink 闭环。

通俗地说，这个工具箱是在做“让人先按工业习惯画图，再自动补上监督控制理论需要的 formal machinery”，而不是让用户先学一门全新的 DES 工具语言。

### 运行 / 接受 / 转移语义

论文把物理闭环控制抽成：

$$
\mathrm{PlantSignals} \xrightarrow{\mathrm{Signal2Event}} \Sigma_u \xrightarrow{\mathrm{Supervisor}} \Sigma_c \xrightarrow{\mathrm{Event2Signal}} \mathrm{Actuation}
$$

这不是原文正式公式，而是对图 4 闭环结构的保守整理，强调：

1. 传感器信号先转成 uncontrollable events。
2. supervisor 根据事件队列更新离散状态。
3. controllable events 再被转回 actuator signals。

论文允许 timing 只出现在 `Technological_Constraints` 中，可写成：

$$
\mathrm{after}(T,\mathrm{sec})
$$

其中：

1. `$T$` 是等待秒数。
2. timing transitions 只允许用于 virtual sensors 与 local controllers。
3. 这样避免把 time 完整引入 supervisory-control 本体，减轻 state-space explosion。

### 语义边界

1. 论文主体仍是传统 supervisory-control，不是 timed automata 或 hybrid control 母型。
2. timing 只被局部地放进 `Technological_Constraints`，不是全系统时序语义。
3. 正确性高度依赖信号/事件映射数据库与控制单元同步假设。
4. 工具强调教学和落地可操作性，不是通用 DES 交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `DFA` 骨架 | `$G = \langle Q, \Sigma, \delta, q_0, Q_m \rangle$` | `MSCI/DECK` 的正式控制对象。 |
| 事件划分 | `$\Sigma = \Sigma_c \uplus \Sigma_u$` | supervisor 通过 controllable / uncontrollable 区分与 plant 交互。 |
| 工程链 | `$\mathrm{MSCI}(M_{sf}, D) = \mathrm{SimulinkModel}(\mathrm{Synth}(\mathrm{DFA}(M_{sf}, D)))$` | 图形模型经 formal synthesis 变成可执行控制单元。 |
| timing 约束 | `$\mathrm{after}(T,\mathrm{sec})$` | 时间被局部加入 virtual sensor / local controller，而非扩展整套 SCT 语义。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `Stateflow` chart 和 `DFA` 是建模主骨架。 |
| 事件 / 触发 | 很强 | rising/falling edge、virtual sensor event 和 local-controller event 都是一等对象。 |
| 守卫 / 数据 | 中等支持 | 主要依赖 `Stateflow` 标签和数据库约束，不追求 rich data semantics。 |
| 层次 | 中等支持 | 通过顶层 superstate 和 local controller 实现结构化分层。 |
| 并发 / 同步 | 中等支持 | didactic platform 支持多个 subsystem 并行，但理论主线仍是 DES supervisor。 |
| 时间约束 | 弱到中等支持 | 只在 `Technological_Constraints` 中通过 `after(T, sec)` 局部支持。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散事件控制。 |
| 可执行 / 可验证性 | 很强 | 自动转换、supervisor synthesis、可执行 Simulink 闭环一体化。 |

### 形式化问题与性质

1. 论文真正补出的，是 supervisory-control 到 `MATLAB/Stateflow` 工业环境的过渡层。
2. 它没有发明新的监督控制理论，而是把 modeling、formal synthesis 和 execution glue 在一个工具里串起来。
3. “只在局部允许时间语义”这点说明它非常强调工程可教、可控和避免爆炸。

## 构造方式与承载格式

### 建模入口

原文中的典型入口包括：

1. `Stateflow` 中的 `Plant`、`Specification`、`Technological_Constraints` 三个顶层 superstate；
2. signal / event database；
3. `CreateChart` 与 `CreateModel` 工作流；
4. `DECK` 负责的 formal conversion 与 synthesis。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Stateflow` chart；
2. signal / event database（可为 `CSV`）；
3. `DECK` 内部 formal automata 表示；
4. executable `Simulink` model；
5. `Modbus TCP` 等 plant-communication protocol。

### 交换与互操作

这篇论文的互操作重点在工程接线而不在开放标准：

1. 用户在 `Stateflow` 中建模。
2. `DECK` 做形式化处理和 supervisor synthesis。
3. `Simulink` 负责与真实系统闭环通信。

## 配套基础设施

- 建模/编辑工具：`MATLAB Stateflow`。
- 解析/交换/元模型支持：signal / event database、`DECK` formal conversion。
- 仿真/执行支持：包含 `Signal-to-Event`、`Event-queuer`、`Event-to-Signal` 的 executable Simulink control unit。
- 验证/分析支持：supervisor synthesis 与 syntax/database concordance checking。
- 代码生成/转换支持：重点不是独立代码生成，而是生成可执行 `Simulink` 闭环模型。
- 标准化或社区生态：依托 `MATLAB/Simulink/Stateflow` 与 supervisory-control 教学/实验平台生态。

## 适用场景与需求前提

### 适用场景

适合 supervisory-control 教学、实验平台控制、以及希望利用 `MATLAB/Stateflow` 降低 DES 建模门槛的工业过渡场景。

### 需求前提

1. 控制问题应主要是离散事件 supervisory-control。
2. 物理接口必须能稳定映射成 signals 和 events。
3. 团队接受 `MATLAB/Stateflow/Simulink` 作为建模与执行环境。
4. 若使用 timing，只能接受局部化的 timing transitions，而不是全局 dense-time semantics。

### 不适用或高成本场景

若问题核心是混成动力学、复杂概率控制，或需要开放的独立标准格式，这条 `MSCI` 路线并不理想。

## 与相邻形式主义的关系

相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，`Supremica` 是独立 supervisory-control IDE，本文则是把 supervisory-control 嵌到 `MATLAB/Stateflow`；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，`CIF 3` 更偏完整 automata-based engineering platform，本文更轻量、更偏教学/工业接受度过渡；相对 [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)，那篇在讲 `Stateflow` 语言语义，这篇在讲如何拿 `Stateflow` 当 supervisory-control 建模入口。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机目标形式主义的选择不仅看理论，还要看工程团队是否愿意使用那套环境。
2. 对控制系统需求到状态机建模而言，`Stateflow` 这类已有工业接受度的载体很重要。
3. 若未来 LLM 生成的模型要进入实际工程流程，这种“formal backend + industrial front-end” 组合值得重点关注。

### 局限

1. 它更像过渡层和教学工具，而不是开放标准。
2. 对时间、数据和复杂并发的支持刻意收束。

## 重要的相关工作

1. [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)：成熟 supervisory-control IDE。
2. [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)：更完整的 supervisory-control engineering platform。
3. [an-operational-semantics-for-stateflow/desc.md](../an-operational-semantics-for-stateflow/desc.md)：`Stateflow` 本体语义基础。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`Supervisory Control Theory / DFA / MATLAB Simulink Stateflow / MSCI`
- 论文角色：`Stateflow`-based supervisory-control teaching and implementation toolbox
- 归类理由：论文主体是在 `MATLAB/Stateflow/Simulink` 上搭 supervisory-control 运行载体与教学/工程流程，核心贡献显然属于执行载体与工具链基础设施。
