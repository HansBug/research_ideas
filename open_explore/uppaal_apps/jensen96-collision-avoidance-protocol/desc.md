问题一句话：本文验证的是一个运行在类 Ethernet 广播介质上的冲突避免协议，核心问题是在存在介质延迟和丢包抽象时如何避免冲突并给出有界通信时延。
方法一句话：作者把 master、medium 和多个 slave 抽象为 timed automata 网络，用 `UPPAAL` 检查碰撞不可达与时间界，同时借助测试自动机编码有界活性性质。
验证收获一句话：`UPPAAL` 证明在有错误介质抽象下只要 timeout 下界达到 `3` 个时间单位即可避免冲突，并给出了首轮往返时间至少 `18` 个时间单位的结论。

## 基本信息

- 标题：Modelling and Analysis of a Collision Avoidance Protocol using SPIN and `UPPAAL`
- 中文标题：使用 `SPIN` 与 `UPPAAL` 对冲突避免协议进行建模与分析
- 作者：Henrik Ejersbo Jensen、Kim G. Larsen、Arne Skou
- 单位：BRICS，Aalborg University
- 发表：`BRICS Report Series` 3(24), 1996
- DOI：`10.7146/brics.v3i24.20005`
- 链接：[DOI](https://doi.org/10.7146/brics.v3i24.20005)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：运行在类 Ethernet 广播介质上的冲突避免轮询协议
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文仅公开了 [BRICS 报告 PDF](https://tidsskrift.dk/brics/article/download/20005/17638)，未提供独立 `UPPAAL` 模型包。
- 案例/数据获取方式：无额外案例数据，主要依据论文中的协议描述与自动机图重建。

## 简报

本文验证的不是通用 timed automata 技术，而是一个具有明确通信对象的广播轮询协议。系统由一个 master、一个可广播并检测冲突的 medium，以及多个 slave 组成，目标是在轮询和回复过程中既避免冲突，又把用户间通信延迟限制在明确上界内。

- 系统：`1` 个 master + `1` 个 medium + 若干 slave 的 Ethernet-like 广播协议。
- 特点：master 轮询、slave 异步向用户取数、介质延迟 `1` 个时间单位、可建模丢包与冲突。
- 规模：协议按 `N` 个站点参数化；文中的有界活性测试以 `3` 个用户/从站为代表。
- 模型：master、medium、slave 的 timed automata 网络，外加针对 bounded liveness 的测试自动机。
- 性质：无冲突、消息最终到达、用户到用户时延有界、轮询 round-trip 时间有界。
- 方法：用 `UPPAAL` 做 timed 安全/可达性验证，并把有界活性转写为测试自动机可达性问题。
- 结果：当 timeout `>= 3` 时可避免碰撞；首轮 round-trip 时间下界为 `18`；还展示了如何在 `UPPAAL` 中编码 bounded liveness。

`轮询协议需求 -> master/medium/slave timed automata -> 无冲突与时延测试自动机 -> 诊断 trace 与时间界结论`

## 论文定位

这篇论文是非常早期、也很典型的 `UPPAAL` 应用案例。它真正验证的对象是广播介质上的协议行为，因此在本论文集里属于 `🛰️ 协议与通信机制`，同时其现实场景是共享网络介质上的分布式通信，所以放在 `🌐 网络与分布式服务` 次轴下最合适。

它的特殊价值在于：正文并不只说“协议可建模”，而是明确把 timed 问题抽成 `UPPAAL` 能检查的 collision safety 和 bounded liveness。尽管文章同时对比了 `SPIN`，但 `UPPAAL` 负责的部分是论文里真正的时间验证主线。

## 验证对象与问题背景

### 系统与场景

被验证对象是一个运行在类 `Ethernet` 广播介质上的 collision avoidance protocol。多个站点共享介质，master 负责轮询各 slave，slave 再与本地用户交互并返回数据。

### 系统组成与运行机制

论文中的核心部件有三类：

1. `Master`
   负责依次向 slave 发送 enquiry。
2. `Slave`
   在接到 enquiry 后与本地用户交互，必要时回送数据。
3. `Medium`
   提供广播通信，并在两个发送请求过近到达时进入 collision 状态。

协议的基本意图是避免两个发送方几乎同时占用共享介质，同时让 master 维持稳定轮询节奏。

### 验证边界

论文验证的是**协议层的轮询与广播时序**，不是完整以太网规范，也不包含物理编码层细节。介质被抽象为具有固定延迟、可丢包、可检测碰撞的广播组件。

### 核心问题

作者关心两个层面：

1. 在 timed 语义下是否还能保证“无冲突”。
2. 用户到用户的通信延迟以及询问 round-trip 是否可给出明确时间界。

### 研究动机

论文的直接动机是比较 `SPIN` 与 `UPPAAL` 的适用边界，但对本论文集而言更重要的是它展示了：一旦协议问题涉及介质延迟、timeout 和 bounded liveness，`UPPAAL` 更自然地承担 timed 验证主线。

## 模型与形式化建模

`UPPAAL` 模型由 master、medium 和 slave 自动机组成：

1. `Master`
   维护下一个待轮询站点 `next`，向 medium 发送 enquiry，并在超时后重新发起轮询。
2. `Medium`
   接收来自 master/slave 的消息，在一个时间单位后广播给相关参与者；若出现连续发送则进入 collision 状态。
3. `Slave`
   接收 enquiry、向本地用户取数，并把返回数据送回 medium。

关键抽象包括：

1. 介质广播通过 committed locations 保证“接收后立即顺序广播”的原子性。
2. 介质延迟固定为 `1` 个时间单位。
3. 作者同时考虑 perfect medium 和 lossy/erroneous medium 两类情形。
4. bounded liveness 不直接由原生属性语言表达，而通过额外测试自动机观察 `send_i/recv_i` 等 probe 动作。

## 验证目标与性质

### 待验证问题

1. 共享介质上是否会发生 collision。
2. 在 lossy medium 下 timeout 取值会不会诱发 collision。
3. 用户消息是否能在给定时间内送达。
4. 轮询 round-trip 是否存在可验证时间界。

### 性质类型

1. 安全性质：`collision` 不可达。
2. 有界活性：消息必须在时间界内收到。
3. 有界响应：相邻轮询与 round-trip 需要满足上界/下界。

### 性质分组与实际含义

1. `82(not medium:col)`
   对应“系统永不进入碰撞态”。
2. `82 not(check_1:bad1 or check_1:bad2)`
   对应“发送到接收、接收到下一次发送都不能超时失界”。
3. `93(check2:ch2 and s <= 18)`
   对应“round-trip 时间界是否足够紧”。

### 判定边界与前提

关于时延界的结论依赖于具体 timeout 和介质假设。论文明确指出：在有错误介质时，timeout 过小会把正常等待误判成丢包，从而反过来诱发碰撞。

## 核心方法与验证流程

作者的 timed 验证流程非常清楚：

1. 先把协议拆成 master、medium、slave 三类自动机。
2. 用 `UPPAAL` 先检查基本 collision safety。
3. 再调 timeout 参数，观察 collision 是否重新变为可达。
4. 对于原生语言不易表达的 bounded liveness，引入测试自动机监听 `send/recv` 事件。
5. 通过 reachability 查询验证 bad 状态是否可达，并使用 diagnostic trace 理解失败原因。

这一点对后续博士研究很有价值，因为它说明：即便查询语言不直接支持某类性质，也可以通过 observer / test automata 回收成标准可达性问题。

## 案例与结果

1. 在 perfect medium 下，`UPPAAL` 可以证明 collision 状态不可达。
2. 在 erroneous medium 下，timeout 选择决定是否会诱发 collision。
3. 论文通过反复验证发现：timeout `>= 3` 时不会发生 collision，而 timeout `= 2` 时存在通往 collision 的诊断轨迹。
4. 对用户到用户通信和轮询行为，作者构造测试自动机验证有界活性。
5. 对首轮 round-trip，论文证明不存在 `< 18` 的完成时间，也就是初始 round-trip 的下界是 `18` 个时间单位。

这些结果都能直接映射回工程解释：master 轮询过快会导致 slave 仍在内部处理时就被重新询问，从而与 slave 返回消息在介质上冲突。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究中的“控制逻辑/协议如何落成 timed automata，并进一步构造验证性质”高度相关，尤其适合支撑性质模式与 observer 模式的积累。

### 可借鉴之处

1. 用 committed locations 表达广播原子性。
2. 用测试自动机绕过查询语言表达力限制。
3. 通过 timeout 参数扫面定位协议正确性的阈值边界。

### 存在的不足与改进空间

论文同时承担工具比较任务，因此系统对象本身并不大；此外它主要分析协议层，不涉及更丰富的工业环境扰动。

### 对本研究的启发

它非常适合作为“协议 -> 状态机网络 -> observer 性质”的经典模板，后续在控制系统通信层、环境监测链路或控制器协调机制中都可复用这一套路。

## 重要的相关工作

### 1. SPIN 与 timed 扩展

本文把 `SPIN` 的 untimed 强项和 `UPPAAL` 的 timed 强项明确区分开，对理解早期工具边界很有帮助。

### 2. bounded liveness 的测试自动机

论文已经显式提出通过测试自动机来编码 bounded liveness，这与后续大量 observer-based verification 工作是同一路线。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：公开可得的是 [BRICS 报告 PDF](https://tidsskrift.dk/brics/article/download/20005/17638)；未发现稳定的独立 `UPPAAL` 模型下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.7146/brics.v3i24.20005)
- 对后续复用的现实影响：可据正文稳定重建模型与性质，但更可能属于“论文复刻型案例”，而不是“直接下载即跑”的公开 benchmark。
