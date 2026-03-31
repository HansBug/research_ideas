问题一句话：本文验证的是基于 `ROS` 的机器人应用节点通信与调度行为，核心问题是队列大小、`callAvailable()` 超时和发布频率等参数组合会不会导致消息丢失、队列溢出或高优先级/低优先级控制消息异常饥饿。
方法一句话：作者把 `ROS` 的 publisher-subscriber、callback queue、`spinOnce`/`callAvailable()` 以及 `Kobuki` 机器人中的 `SafetyController` 和 `Multiplexer` 建成 timed automata，并用 `UPPAAL` 穷举参数组合。
验证收获一句话：论文不仅定位了安全控制器队列溢出会导致传感器事件丢失，还证明在某些参数下 `RandomWalker` 的控制消息永远到不了底盘，说明 `ROS` 应用的实时性问题可以直接通过形式模型暴露出来。

## 基本信息

- 标题：Formal Verification of ROS-Based Robotic Applications Using Timed-Automata
- 中文标题：基于 timed automata 的 `ROS` 机器人应用形式化验证
- 作者：Raju Halder、José Proença、Nuno Macedo、André Santos
- 单位：HASLab / INESC TEC、Universidade do Minho、Indian Institute of Technology Patna
- 发表：FormaliSE 2017 / IEEE/ACM Workshop on Formal Methods in Software Engineering
- DOI：`10.1109/FORMALISE.2017.9`
- 链接：[DOI](https://doi.org/10.1109/FORMALISE.2017.9)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：基于 `ROS` 的 `Kobuki` 机器人控制节点通信与调度行为
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供公开 `UPPAAL` 模型仓库；论文公开，但未给独立 timed automata 工程下载入口。
- 案例/数据获取方式：案例来自 `Kobuki` 机器人应用与其 `ROS` 节点代码结构；原文未整理出独立可直接下载的实验配置包。

## 简报

这篇论文验证的不是某个机器人路径规划算法，而是 `ROS` 中最容易被忽视的一层基础机制：消息是怎样排队的、谁先被调度、超时怎么影响 callback 处理。因为这层机制直接决定“安全消息会不会丢”和“控制命令会不会永远发不出去”。

- 系统：`ROS` 节点通信语义，以及 `Kobuki` 机器人的 `SafetyController` / `Multiplexer`。
- 特点：显式保留 publisher-subscriber 队列、callback queue、`spinOnce`、`callAvailable()` timeout。
- 规模：`Kobuki` 案例至少覆盖 wheel / bumper / cliff 三类安全传感器队列，以及 `SafetyController-Update`、`SafetyController-Publisher`、`Multiplexer` 等模块。
- 模型：用 timed automata 建模消息发送、队列入队/出队、callback 处理和节点时钟行为。
- 性质：队列是否溢出、传感器消息是否最终反映到安全状态、`RandomWalker` 消息是否能到达电机。
- 方法：先建通用 `ROS` 通信模型，再实例化到 `Kobuki`，然后系统性扫参数。
- 结果：确定了若干会导致安全消息丢失或低优先级控制消息长期饥饿的参数区域。

`ROS 通信/队列语义 -> timed automata 模型 -> 参数化队列与 timeout 验证 -> 定位 Kobuki 中的消息丢失与饥饿问题`

## 论文定位

这是很典型的“机器人应用实时语义验证”论文。它验证的重点不是机器人任务逻辑本身，而是 `ROS` 中节点通信、队列和调度参数如何影响实时响应，因此更适合归入 `⏱️` 主轴。与 [uppaal_tech/README.md](../uppaal_tech/README.md) 的关系上，它仍然是强应用论文，因为最终落在 `Kobuki` 物理机器人系统，而不是单纯讨论 `UPPAAL` 语言或算法。

## 验证对象与问题背景

### 系统与场景

被验证对象是基于 `ROS` 的机器人应用，具体案例是 `Kobuki` 机器人。`ROS` 为机器人提供消息中间件、节点组织与 callback 处理机制，但这些机制是否满足实时安全要求并不是天然有保证的。

### 系统组成与运行机制

论文先给出通用 `ROS` publisher-subscriber 模型，再进入 `Kobuki` 案例：

1. **Publisher / Subscriber / Channel**
   - 消息先进入 channel queue，再进入 subscriber queue。
2. **Callback Queue**
   - `spinOnce` / `callAvailable()` 驱动 callback 执行。
3. **SafetyController**
   - 订阅 wheel-drop、bumper、cliff 等安全传感器。
4. **Multiplexer**
   - 对多个控制源进行优先级仲裁，最终向底盘发送速度命令。

### 验证边界

本文验证的是**节点通信、排队和 callback 调度层**，不是路径规划、地图构建或连续动力学控制器。

### 核心问题

`ROS` 的灵活性意味着开发者可以自行设置：

1. 发布频率；
2. subscriber queue 大小；
3. callback queue 处理速率；
4. `callAvailable()` timeout。

这些参数一旦设置不当，就会出现：

1. 传感器消息被新消息覆盖；
2. callback queue 堵塞；
3. 低优先级命令长期无法生效；
4. 安全逻辑实际看不到本该看到的事件。

### 研究动机

作者要回答的不是“机器人会不会撞墙”，而是“在 `ROS` 中，参数和中间件机制会不会让安全逻辑根本来不及反应”。

## 模型与形式化建模

### 通用 `ROS` 建模

论文把 `ROS` 通信抽象成几个核心机制：

1. publisher 向 channel queue 发布；
2. channel queue 将消息转发到 subscriber queue；
3. subscriber queue 再把 callback 请求压入 callback queue；
4. `callAvailable()` 周期性处理 callback queue 中任务。

这一层建模已经足以分析 overflow、timeout 和 callback 处理时序。

### `Kobuki` 实例化

对 `Kobuki`，作者重点建模了：

1. `SafetyController-Update`
   - 负责定期 `spinOnce` 读取 wheel / bumper / cliff 三个传感器队列。
2. `SafetyController-Publisher`
   - 依据安全状态发出更高优先级控制命令。
3. `Multiplexer`
   - 对安全控制器与 `RandomWalker` 等来源进行命令仲裁。

### 关键时间参数

作者显式保留：

1. queue size；
2. spin rate；
3. callback 执行时间上下界；
4. `callAvailable()` timeout。

文中还指出 `ROS` 0.10 与 0.11 在默认 timeout 上有差异，这会直接影响系统行为。

## 验证目标与性质

### 待验证问题

论文的性质非常工程化，主要有三类：

1. **队列溢出**
   - 是否存在某条路径使 queue overflow。
2. **传感器消息不丢**
   - 例如左轮掉落事件是否最终反映到 `wheel_leftdropped` 状态变量。
3. **命令可达**
   - `RandomWalker` 的速度命令是否最终能送到底盘。

### 性质类型

1. 安全性质
   - 关键消息不能被静默吞掉。
2. 时序/资源性质
   - 队列在给定参数下不应溢出。
3. 活性性质
   - 某些消息最终必须到达执行端。

### 性质分组与实际含义

1. **Sensor-Property**
   - 轮传感器事件到来并处理后，应在安全控制器内部被反映。
2. **MUX-Property**
   - `RandomWalker` 消息在多源竞争下仍应有机会到达引擎。
3. **Queue-overflow queries**
   - 用以找出安全参数区域。

## 核心方法与验证流程

1. 先构建通用 `ROS` 通信 timed automata。
2. 证明该模型能表达 publisher-subscriber、queue、callback queue 和 `callAvailable()`。
3. 将其映射到 `Kobuki` 的 `SafetyController` 与 `Multiplexer`。
4. 通过改变 queue size、spin rate、timeout、callback time 等参数运行 `UPPAAL` 查询。
5. 当性质失败时，用反例轨迹解释具体哪类消息被覆盖或长期阻塞。

这种流程的优势在于：它给出的是“为什么错”的时序路径，而不只是一个测试里偶然观测到的问题。

## 案例与结果

### 安全控制器溢出

论文在 `SafetyController-Update` 上展示：

1. wheel / bumper / cliff 三类消息都会进入 subscriber queues；
2. 如果 queue 太小、spin 太慢或 callback 处理过慢；
3. 则某些关键安全消息会在队列满时被后续消息替换。

文中表 1 就列出了若干会触发 overflow 的参数组合。

### 传感器消息丢失

作者进一步证明，队列溢出不是“无害的实现细节”。当 `QWheel` 可能 overflow 时，左轮掉落这一安全事件就可能永远无法更新到 `wheel_leftdropped` 变量，导致安全控制器在逻辑上“没看见”危险事件。

### `Multiplexer` 饥饿

在 `Multiplexer` 中，论文展示了另一个问题：如果高优先级安全控制器发布足够频繁、timeout 足够长，则 `RandomWalker` 的 `cmdVel` 消息可能永远无法到达 `Kobuki` 底盘。这不是死锁，而是典型的优先级饥饿。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的关系在于：它展示了怎样把中间件语义、队列与 callback 组织成状态机，再让性质直接对着工程风险写。

### 可借鉴之处

1. 把通信中间件参数也纳入验证对象，而不是只验证业务状态机。
2. 用单条反例路径解释“为什么消息丢了”。
3. 让参数验证直接服务于工程配置选择。

### 存在的不足与改进空间

1. 重点仍在通信与调度层，机器人连续控制与环境动力学没有展开。
2. 原文未提供独立公开模型仓库，现实复跑需要自行重建。
3. 案例聚焦单机 `ROS` 节点组合，分布式 `ROS 2` 语义还未覆盖。

### 对本研究的启发

它提醒本研究：很多“状态机缺陷”并不是纯迁移逻辑错误，而是队列、timeout、调度优先级共同诱发的行为偏差。

## 重要的相关工作

### 1. `ROS` 形式化分析

- 论文明确面向 `ROS` 节点通信这一长期缺少统一形式化分析框架的层次。

### 2. `Kobuki`

- `Kobuki` 作为物理机器人案例，让验证结果具有真实工程含义，而不只是合成 benchmark。

### 3. `UPPAAL`

- `UPPAAL` 在这里承担的是参数空间穷举和反例解释工具，而不是单纯“跑一条时限公式”。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文可公开获取，但原文未提供独立 `UPPAAL` 模型仓库或完整实验配置包；当前只能稳定拿到论文 PDF。
- 获取方式/链接：[DOI](https://doi.org/10.1109/FORMALISE.2017.9)；[公开 PDF](https://repositorium.sdum.uminho.pt/bitstreams/c15d9b06-0fba-4f8b-bf80-8f16f7454ebf/download)
- 对后续复用的现实影响：这是很有价值的 `ROS` 实时语义案例，但更适合拿来借鉴建模方法和性质模板，而不是直接下载现成模型复跑。
