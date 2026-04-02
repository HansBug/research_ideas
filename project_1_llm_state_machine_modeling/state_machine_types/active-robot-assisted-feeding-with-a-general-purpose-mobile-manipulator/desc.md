# 面向主动喂食的通用移动机械臂状态机 / Active Robot-Assisted Feeding with a General-Purpose Mobile Manipulator

## 基本信息

- 标题：Active Robot-Assisted Feeding with a General-Purpose Mobile Manipulator: Design, Evaluation, and Lessons Learned
- 中文标题：面向主动喂食的通用移动机械臂状态机
- 作者：Daehyung Park, Yuuna Hoshi, Harshal P. Mahajan, Ho Keun Kim, Zackory Erickson, Wendy A. Rogers, Charles C. Kemp
- 发表：*Robotics and Autonomous Systems*, 124:103344, 2020
- DOI：`10.1016/j.robot.2019.103344`
- 链接：https://doi.org/10.1016/j.robot.2019.103344
- 形式主义：`Meal Assistance FSM`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：助餐机器人任务管理 / `FSM` 驱动的 active feeding controller
- 工具/实现获取方式：原文直接给出 `PR2`、web GUI、food-location estimator、mouth pose estimation、execution monitor、anomaly classifier、3D-printed bowl guard / wiping bar 等实现要素；未给统一代码仓库。
- 标准/格式获取方式：原文未给独立交换标准，主要承载方式是 task-layer `FSM`、motion primitive 参数、GUI 事件和 ROS 组件。

## 简报

这篇论文把助餐机器人高层控制整理成一套非常清楚的 `FSM`：用户通过 GUI 触发 `scooping/stabbing`、`wiping`、`delivery` 三类子任务，系统在各状态间依据正常事件 `TN` 或异常事件 `TA` 转移；低层则用参数化 motion primitives 驱动 `PR2` 实际完成取食、擦勺和送入口中。

- 形式主义定位：面向 assistive feeding 的任务管理 `FSM`，把用户命令、感知估计和异常处理压入同一状态机。
- 构造方式简述：task layer 用 `FSM` 编排子任务，functional layer 用 `{x_g, T_{\mathrm{Duration}}, \kappa}` 形式的 motion primitives 执行。
- 基础设施与场景简述：依托 `PR2`、web GUI、视觉食物估计、口部位姿估计和 anomaly monitor，服务重度上肢障碍用户的主动喂食任务。

```text
GUI 指令 -> Task Manager FSM -> 取食 / 擦勺 / 送入口中 -> 异常监测 -> 停止或纠正动作
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. task-layer `FSM`。
2. 三类主要子任务：`scooping/stabbing`、`wiping`、`delivery`。
3. 两类转移触发：正常 `TN` 与异常 `TA`。
4. motion primitive 参数集合 `{x_g, T_{\mathrm{Duration}}, \kappa}`。
5. `food-location estimator`、mouth pose estimator 和 anomaly detector。
6. `PR2` 机器人及其 bowl / utensil / wiping bar / GUI 交互系统。

### 核心抽象

按论文中的结构，可把高层助餐控制保守整理为：

$$
\mathcal{M} = (Q, q_0, F, \Sigma, \delta, \Theta, \mathcal{P})
$$

上式中的符号逐项解释如下：

1. `Q` 是 task-manager 的状态集合。
2. `q_0` 是 idle 初始状态。
3. `F` 是子任务完成或系统停止后的终止状态集合。
4. `\Sigma` 是 GUI 命令、成功/失败反馈和异常事件集合。
5. `\delta` 是状态转移关系。
6. `\Theta` 是动作参数集合。
7. `\mathcal{P}` 是感知与监测模块集合。

论文直接给出了 motion primitive 参数形式：

$$
\theta = \{x_g, T_{\mathrm{Duration}}, \kappa\}
$$

上式中的符号逐项解释如下：

1. `x_g \in \mathbb{R}^6` 是目标位姿，包含位置和姿态。
2. `T_{\mathrm{Duration}}` 是从起始位姿到目标位姿的执行时长。
3. `\kappa` 是运动类型，论文列出关节空间点到点、笛卡尔空间点到点、笛卡尔线性运动三类。

状态转移语义可写成：

$$
\delta(q, e) =
\begin{cases}
q', & e = T_N \\
q_{\mathrm{safe}}, & e = T_A
\end{cases}
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `e` 是当前触发事件。
3. `T_N` 是非异常转移触发。
4. `T_A` 是异常转移触发。
5. `q'` 是正常后继状态。
6. `q_{\mathrm{safe}}` 是停止或纠正动作状态。

### 一个最小例子与通俗解释

一个最小例子是“勺取一口食物并送到用户嘴边”：

1. 用户在 GUI 上点击 `Scooping/Stabbing`。
2. 机器人先进入取食初始化姿态。
3. food estimator 在碗内估计合适的取食位置。
4. 机器人执行 scooping 或 stabbing motion。
5. 若勺上食物过多，用户可点击 `CleanSpoon` 进入 wiping。
6. 用户再点击 `Feeding`，机器人将勺尖送到估计口部平面内默认 4 cm 处。
7. 若监测到异常声音或异常执行状态，则触发 `TA`，机器人撤回手臂并进入安全状态。

通俗地说，这个模型像一个“会看、会停、会擦勺的助餐流程机”：不是让机器人一次性执行长动作脚本，而是把每个助餐阶段都变成显式状态，异常时可以立即切到安全动作。

### 运行 / 接受 / 转移语义

任务层的运行语义可以压成：

$$
(q_t, e_t, \theta_t, p_t) \xrightarrow{\delta} (q_{t+1}, u_t)
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前任务状态。
2. `e_t` 是当前 GUI 事件或异常监测事件。
3. `\theta_t` 是当前动作原语参数。
4. `p_t` 是当前感知结果，如食物位置或嘴部位姿。
5. `q_{t+1}` 是下一状态。
6. `u_t` 是实际下发到机器人上的控制动作。

### 语义边界

这个模型的边界包括：

1. 它服务的是助餐任务，不是一般移动操作任务语言。
2. 高层 `FSM` 依赖底层视觉估计和机械臂控制正确运行。
3. 论文重点在执行安全与可用性，不是形式验证或复杂计划综合。
4. 任务结构相对固定，开放式餐桌整理或复杂多人交互不在其能力边界内。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 任务管理骨架 | `$\mathcal{M} = (Q, q_0, F, \Sigma, \delta, \Theta, \mathcal{P})$` | 把子任务、事件、动作参数和感知模块统一起来。 |
| 动作原语参数 | `$\theta = \{x_g, T_{\mathrm{Duration}}, \kappa\}$` | 低层执行不是黑箱，状态输出到具体 motion primitive 参数。 |
| 异常分支 | `$\delta(q,e)$` with `T_N/T_A` | 正常与异常事件通过两类触发改变状态流。 |
| 安全撤回 | `$e = T_A \Rightarrow q_{\mathrm{safe}}$` | 异常会强制系统进入停止或纠正动作。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | idle、取食、擦勺、送入口中、异常处理等阶段清晰。 |
| 事件 / 触发 | 强支持 | GUI 命令、用户停止、异常检测都直接触发转移。 |
| 守卫 / 数据 | 强支持 | 食物位置、口部位姿、异常判定和工具参数都进入执行。 |
| 层次 | 中等支持 | 论文主要是 task layer + functional layer，两层很清楚。 |
| 并发 / 同步 | 弱支持 | 重点是顺序助餐流程。 |
| 时间约束 | 弱支持 | `T_{\mathrm{Duration}}` 是动作时长，不是显式实时语义。 |
| 连续动态 / 随机性 | 中等支持 | 低层是连续运动，高层仍是离散状态切换。 |
| 可执行 / 可验证性 | 强执行、有限验证 | 真机用户实验充分，但非形式验证框架。 |

### 形式化问题与性质

1. 这篇论文最有价值的地方，是把 assistive feeding 从“长脚本”变成了可干预、可异常打断的显式状态机。
2. `TN/TA` 二分转移非常适合后续做安全型需求抽取。
3. motion primitive 参数化说明高层状态机和低层轨迹生成之间可以有清晰接口。
4. 对 `project_1` 来说，这类任务特别适合“需求句子 -> 子任务状态 -> 异常转移”式建模。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 用户通过 GUI 选择子任务。
2. task manager 根据按钮事件进入对应状态。
3. low-level motion primitives 根据感知结果实例化参数。
4. anomaly monitor 在执行期间持续观察并可能触发 `TA`。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. task-layer `FSM`。
2. motion primitive 参数集合。
3. web GUI 与状态显示。
4. ROS 组件间的 `JSON` 双向通信接口。

### 交换与互操作

互操作重点在：

1. GUI 与任务层状态机交互。
2. 感知层把食物位置和口部位姿提供给执行层。
3. anomaly detector 将异常直接反馈到状态机。
4. bowl / utensil / wiping bar 的物理约束也通过状态流程得到体现。

## 配套基础设施

- 建模/编辑工具：web GUI、task manager、状态显示界面。
- 解析/交换/元模型支持：ROS 组件通信、`JSON` 双向接口、状态与反馈记录。
- 仿真/执行支持：`PR2`、多种 utensil、3D-printed bowl guard / wiping bar、food estimator、mouth pose estimator。
- 验证/分析支持：执行监视器、anomaly classifier、10 名健全者和 9 名运动障碍用户实验。
- 代码生成/转换支持：原文未强调自动代码生成，主要是状态机调度和参数化运动执行。
- 标准化或社区生态：依托 ROS / assistive robotics / PR2 研究生态。

## 适用场景与需求前提

### 适用场景

适合 assistive feeding、上肢障碍辅助进食、需要用户可干预且强调执行安全的移动机械臂服务任务。

### 需求前提

1. 任务可拆成少数固定阶段。
2. 食物位置和用户口部位姿能被稳定估计。
3. 机械臂和工具安装关系可预注册。
4. 异常中止与人工介入是必须保留的需求。

### 不适用或高成本场景

若食物形态高度不可预测、用户姿态快速变化、环境拥挤或需要复杂双人协同，仅靠该 `FSM` 会面临较高感知和执行成本。

## 与相邻形式主义的关系

相对一般 `SMACH` 或 `RAFCON` 任务流程，它更专注于助餐任务和异常安全；相对普通 manipulation `FSM`，它显式引入了 `TN/TA` 双通道和动作原语参数；相对行为树，这里更强调阶段性完成与安全中止，而不是持续 tick 重评估。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合作为 `project_1` 的控制需求抽取样本，因为任务边界、异常边界和人机交互边界都很清楚。

### 作为目标形式主义还是中间表示

对助餐这一类专用服务任务，它可以直接作为目标形式主义；对更大系统，它更适合作为上层任务监督器的中间表示。

### 对需求到模型生成的启发

1. GUI 按钮和异常事件都可直接转成状态机事件。
2. 任务说明里的“如果勺子上食物太多则擦勺”非常适合状态分支。
3. 低层动作参数应作为状态输出接口，而不是塞到状态名里。
4. 安全需求最好显式变成异常转移，而不是仅写成注释。

### 现实限制

其成功高度依赖底层感知、工具安装和 `PR2` 能力栈；若这些前提不成立，高层 `FSM` 也无法独立保证效果。

## 重要的相关工作

- `My Spoon`、`Bestic`、`Mealtime partner`：论文作为传统被动喂食设备对比。
- `MealBuddy`：文中直接借鉴其 wiping bar 思路。
- 机器人助餐 anomaly detection / execution monitoring 工作：论文把它们整合进运行时安全链路。
- `PR2` assistive robotics 路线：作为整个平台基础。

## 文献分类总结

- 这是一篇 `📦` 类专用任务控制条目，核心是助餐任务状态机与安全执行链，而不是一般理论 `FSM`。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；语境是 assistive robotics，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“专用服务任务如何被压成 GUI 事件驱动 + 异常可中止的状态机”。
