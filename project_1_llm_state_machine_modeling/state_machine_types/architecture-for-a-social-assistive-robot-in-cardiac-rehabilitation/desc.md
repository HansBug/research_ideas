# 心脏康复中的社交辅助机器人架构 / Architecture for a Social Assistive Robot in Cardiac Rehabilitation

## 基本信息

- 标题：Architecture for a Social Assistive Robot in Cardiac Rehabilitation
- 中文标题：心脏康复中的社交辅助机器人架构
- 作者：Jonathan Casas, Nathalia Cespedes Gomez, Emmanuel Senft, Bahar Irfan, Luisa F. Gutierrez, Monica Rincon, Marcela Munera, Tony Belpaeme, Carlos A. Cifuentes
- 发表：*2018 IEEE 2nd Colombian Conference on Robotics and Automation (CCRA)*, pp. 1-6, 2018
- DOI：`10.1109/CCRA.2018.8588133`
- 链接：https://doi.org/10.1109/CCRA.2018.8588133
- 形式主义：`Cardiac Rehabilitation Social Robot FSM`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：心脏康复社交机器人监督器 / model-controller `FSM`
- 工具/实现获取方式：原文直接给出 `NAO` humanoid、`SARI` 应用接口、`Naoqi` framework、`DCM` 资源管理模块、PC/tablet 端应用和远程 `TCP/IP` 连接方式；未给公开代码仓库。
- 标准/格式获取方式：原文未给独立交换标准，主要承载方式是 `FSM` 状态图、behavior timeline、`Naoqi/DCM` 服务调用和由传感接口产生的 therapy events。

## 简报

这篇论文把心脏康复训练里的社交辅助职责压成了一张很典型的医疗场景 `FSM`。机器人不是一直主动说话，而是长期停留在 `Monitor`，根据病人姿态、主观疲劳评分和风险事件，在 `Motivation`、`Borg Scale`、`Warning`、`Emergency` 等状态间切换。它的价值不在于新自动机理论，而在于说明医疗康复中的“鼓励、监护、预警、求助”可以稳定落成显式监督器。

- 形式主义定位：面向 treadmill 心脏康复会话的社交机器人监督状态机，用来协调欢迎、持续监护、鼓励、姿态纠正、主观疲劳评估和异常求助。
- 构造方式简述：上层 `SARI` 汇总传感数据与事件，中层 `FSM` 决定当前干预状态，下层行为模块把状态转成 `NAO` 的 speech、motion、LED 和 tactile interactions。
- 基础设施与场景简述：依托 `NAO`、`Naoqi/DCM`、PC/tablet 端人机接口和康复监护数据流，服务真实心脏康复训练会话。

```text
病人生理/姿态事件 -> SARI -> Cardiac Rehab FSM -> behavior timeline -> NAO speech / motion / warning / assistance
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. `SARI`：接收传感数据和系统事件的人机接口。
2. `Robot Controller`：负责状态判定的监督层。
3. `Robot Model`：把状态映射成行为序列的执行层。
4. 状态集合：`Start`、`Welcome`、`Monitor`、`Motivation`、`Posture Correct`、`Borg Scale`、`Warning`、`Emergency`、`Farewell`、`Shutdown`。
5. 输入集合：病人生理监测、姿态纠正事件、Borg 主观疲劳询问、周期性鼓励定时器和人工确认。
6. 行为资源：speech synthesizer、motions、LEDs、tactile sensors、camera/audio manager。

### 核心抽象

按原文的 model-controller 结构，可将该监督器保守整理为：

$$
\mathcal{C} = (Q, \Sigma, \delta, q_0, F, B)
$$

上式中的符号逐项解释如下：

1. `Q` 是离散状态集合。
2. `\Sigma` 是来自 `SARI` 的输入事件与监护数据。
3. `\delta` 是状态转移函数。
4. `q_0 = \mathrm{Start}` 是初始状态。
5. `F` 是会话终止状态集合，至少包含 `Shutdown`。
6. `B` 是把状态映射为 `NAO` 行为序列的函数。

论文图 3 中的核心状态集合可以直接写为：

$$
Q = \{\mathrm{Start}, \mathrm{Welcome}, \mathrm{Monitor}, \mathrm{Motivation}, \mathrm{PostureCorrect}, \mathrm{BorgScale}, \mathrm{Warning}, \mathrm{Emergency}, \mathrm{Farewell}, \mathrm{Shutdown}\}
$$

上式中的符号逐项解释如下：

1. `Start` 负责初始化会话。
2. `Welcome` 对病人进行开场引导。
3. `Monitor` 是中心状态，持续以 `1 Hz` 接收并分析数据。
4. `Motivation` 周期性提供鼓励。
5. `PostureCorrect` 纠正头部下倾等风险姿态。
6. `BorgScale` 询问主观用力感。
7. `Warning` 对接近临界的身体指标进行确认。
8. `Emergency` 请求医护立即接管。
9. `Farewell` 结束会话。
10. `Shutdown` 关闭系统。

运行过程可以压缩为：

$$
q_{t+1} = \delta(q_t, x_t, e_t)
$$

上式中的符号逐项解释如下：

1. `q_t` 是时刻 `t` 的当前监督状态。
2. `x_t` 是当前收到的监护数据，如姿态、参数阈值和病人反馈。
3. `e_t` 是离散事件，如定时鼓励、Borg 询问或医护确认。
4. `q_{t+1}` 是下一时刻状态。

监护状态上的两类关键 guard 可保守写成：

$$
q_t = \mathrm{Monitor} \land x_t \in \mathrm{warning\_range} \Rightarrow q_{t+1} = \mathrm{Warning}
$$

$$
q_t = \mathrm{Monitor} \land x_t \in \mathrm{critical\_range} \Rightarrow q_{t+1} = \mathrm{Emergency}
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{warning\_range}` 表示接近病人物理档案临界值但尚未达到严重风险的参数区间。
2. `\mathrm{critical\_range}` 表示需要立即人工干预的风险区间。
3. 两条 guard 都只在 `Monitor` 中评估，体现其作为中心状态的语义。

### 一个最小例子与通俗解释

一个最小例子可以用“跑步机训练中途出现风险姿态”来说明：

1. 会话启动后，`Start -> Welcome -> Monitor`。
2. `Monitor` 以 `1 Hz` 接收患者姿态和生理数据。
3. 当系统检测到病人持续低头时，触发 `PostureCorrect`。
4. 机器人播放语音并执行纠正姿势的动作。
5. 纠正行为结束后，系统回到 `Monitor` 继续观察。
6. 如果后续参数接近危险值，则改走 `Warning`；若已经严重异常，则直接进入 `Emergency`。

通俗地说，这个模型像“会说话的康复陪练 + 值班护士”。大多数时间它只看不打断，但一旦出现疲劳、姿态问题或风险阈值，就切到对应干预模式。

### 运行 / 接受 / 转移语义

其执行语义可保守写成：

$$
(q_t, x_t) \xrightarrow{\delta} q_{t+1} \xrightarrow{B(q_{t+1})} u_{t+1}
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前监督状态。
2. `x_t` 是本周期的观测数据。
3. `q_{t+1}` 是状态机根据事件与阈值决定的下一状态。
4. `u_{t+1}` 是行为模块生成的资源时间线，如语音、动作和灯光。

行为层的输出可进一步保守写成：

$$
B(q) = (\mathrm{speech}(q), \mathrm{motion}(q), \mathrm{led}(q), \mathrm{touch}(q))
$$

上式中的符号逐项解释如下：

1. `\mathrm{speech}(q)` 是当前状态绑定的话术。
2. `\mathrm{motion}(q)` 是身体动作或 gesture。
3. `\mathrm{led}(q)` 是灯光表现。
4. `\mathrm{touch}(q)` 主要在 `Emergency` 等状态用于人工确认或复位。

### 语义边界

这个模型的边界包括：

1. 它是针对固定康复流程的 session supervisor，不是通用社交机器人认知架构。
2. 连续的生理评估逻辑被抽成阈值事件，FSM 不直接建模连续动力学。
3. 原文中的转移主要是确定性的，作者也明确提出未来可改为概率化。
4. 它依赖外部传感接口和临床流程约束，不能脱离康复场景单独成立。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 监督器骨架 | `$\mathcal{C} = (Q, \Sigma, \delta, q_0, F, B)$` | 机器人由一张离散状态机和一层行为映射共同驱动。 |
| 核心状态集 | `$Q = \{\mathrm{Start}, \mathrm{Welcome}, \mathrm{Monitor}, \ldots, \mathrm{Shutdown}\}$` | 原文图 3 的会话状态被显式列举。 |
| 数据驱动转移 | `$q_{t+1} = \delta(q_t, x_t, e_t)$` | 监护数据和事件共同决定下一状态。 |
| 预警 guard | `$q_t=\mathrm{Monitor} \land x_t \in \mathrm{warning\_range} \Rightarrow q_{t+1}=\mathrm{Warning}$` | 接近阈值时不直接停机，而是先做确认性干预。 |
| 紧急 guard | `$q_t=\mathrm{Monitor} \land x_t \in \mathrm{critical\_range} \Rightarrow q_{t+1}=\mathrm{Emergency}$` | 严重异常会触发人工接管。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 欢迎、监护、鼓励、姿态纠正、预警、紧急等模式都很清晰。 |
| 事件 / 触发 | 强支持 | 周期定时、姿态事件、Borg 询问、异常参数和人工确认都会触发转移。 |
| 守卫 / 数据 | 强支持 | 生理数据是否接近临界值是核心 guard。 |
| 层次 | 中等支持 | 三层架构清晰，但 FSM 本体仍是单层 session supervisor。 |
| 并发 / 同步 | 弱支持 | 重点是单机器人单会话监督，不是并发多机协同。 |
| 时间约束 | 中等支持 | `Monitor` 以 `1 Hz` 分析数据，鼓励行为按约 `5` 分钟周期触发，但没有显式时钟语义。 |
| 连续动态 / 随机性 | 弱支持 | 连续生理变化存在，但被离散化成事件；当前版本无随机建模。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 已在真实 `CR` 会话中执行 `38` 分钟，但未接入形式验证工具。 |

### 形式化问题与性质

1. 论文真正给出的不是聊天脚本，而是一张临床会话监督器。
2. `Monitor` 作为中心状态，说明应用型状态机可以长期驻留于“观察”而不是“动作”。
3. `Warning` 与 `Emergency` 的分层体现了医疗风险处理中的渐进式干预。
4. 原文明确指出当前转移是确定性的，未来计划引入基于事件概率分布的转移策略。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先观察传统康复会话，抽取医护的三类职责：motivation、monitoring、assistance。
2. 以这些职责为核心确定离散状态。
3. 把传感接口送来的监护数据和系统事件接到 `Monitor`。
4. 再为每个状态绑定行为时间线和 `NAO` 资源。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. 心脏康复 `FSM` 状态图。
2. `SARI` 事件和数据接口。
3. behavior timeline 资源编排。
4. `Naoqi` 服务调用与 `DCM` 资源控制。
5. PC/tablet 到 `NAO` 的远程 `TCP/IP` 会话。

### 交换与互操作

互操作重点在：

1. 传感接口先把数据送入 `SARI`。
2. `FSM` 从 `SARI` 读取数据并决定下一状态。
3. 状态结果交给 behavior module 生成 speech/motion timeline。
4. `Naoqi/DCM` 再把这些高层行为映射到 `NAO` 的硬件资源。

## 配套基础设施

- 建模/编辑工具：原文主要以三层架构图、FSM 图和 behavior timeline 表示，未给专用图形建模器。
- 解析/交换/元模型支持：`SARI`、`Naoqi` API、`DCM` 资源管理和远程 `TCP/IP` 接口。
- 仿真/执行支持：`NAO` humanoid 平台、camera/audio manager、speech synthesis、LED、tactile sensors。
- 验证/分析支持：真实 `CR` 会话中的 `38` 分钟运行和状态触发统计。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 `NAO` 机器人生态和心脏康复监护流程。

## 适用场景与需求前提

### 适用场景

适合 treadmill 或类似节律性康复训练中，需要机器人长期陪伴、持续监护并在少数关键时刻主动干预的会话型医疗场景。

### 需求前提

1. 康复流程可以抽成离散的会话阶段。
2. 系统能稳定获取姿态、生理参数或病人反馈。
3. 允许机器人通过语音、动作和灯光进行社交干预。
4. 现场仍有专业人员在需要时接管。

### 不适用或高成本场景

如果临床场景高度开放、病人状态变化非常复杂、且无法稳定获得结构化监护信号，这种确定性 `FSM` 很快会变得过于僵硬。

## 与相邻形式主义的关系

相对一般的对话管理器，它更强调医疗监护 guard 而不是语言轮次；相对行为树，它更适合表达会话级监督和中心监护状态；相对更一般的护理机器人架构，它是一个更窄但更可执行的 therapy supervisor。

## 与本研究的关系

### 对 Project 1 的价值

它很好地展示了医疗需求文本中的“持续监护”“定时鼓励”“异常预警”“立即求助”如何稳定映射到一张显式状态图。

### 作为目标形式主义还是中间表示

对具体康复系统来说，它可以直接作为可执行监督器；对更复杂的医疗机器人体系来说，它也可以作为更大行为系统中的中间控制层。

### 对需求到模型生成的启发

1. 需求里的临床角色职责可以直接转成状态机模式名。
2. “监护”和“干预”应分离，避免把所有行为都摊平为一步步脚本。
3. 阈值事件和主观量表都可以变成 guard，而不只是注释。
4. 会话型应用状态机通常需要一个常驻中心状态，如 `Monitor`。

### 现实限制

论文只验证了单次真实会话和较小的状态集，复杂患者差异、长期个性化适应和概率性转移仍需进一步研究。

## 重要的相关工作

- `SARI` 传感接口：为本文提供事件与监护数据入口。
- `NAO / Naoqi / DCM`：构成具体行为执行与硬件资源层。
- 心脏康复中的 `Borg Scale` 和姿态风险管理：为状态机 guard 提供临床依据。
- socially assistive robotics 在康复中的既有研究：构成本文应用背景。

## 文献分类总结

- 这是一篇 `📦` 类医疗应用状态机条目，核心是会话监督和社交干预逻辑，而不是新的自动机理论。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景是具身康复机器人与人体监护闭环，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“临床会话职责如何落成可执行监督状态机”的应用证据。
