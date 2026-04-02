问题一句话：本文验证的是分布式实时网络协议 `RTnet`，核心问题是在广播局域网、节点动态加入/退出和丢包故障下，协议是否仍能稳定、无冲突并在有界时间内恢复。
方法一句话：作者为 `RTnet` 的 node、network 和 control message 建立 `UPPAAL` 模型，分别分析 unicast token 与 broadcast token 两个变体，并用定性和定量查询检查稳定性、唯一发送者、轮询冲突和恢复时长。
验证收获一句话：论文证明无故障时两个变体都能稳定运行；单包丢失时二者通常都可恢复，但 broadcast token 变体更容易出现并发发送和鲁棒性下降，恢复时长也更敏感。

## 基本信息

- 标题：Verifying the Distributed Real-Time Network Protocol RTnet Using Uppaal
- 中文标题：使用 `Uppaal` 验证分布式实时网络协议 `RTnet`
- 作者：Ferdy Hanssen、Angelika Mader、Pierre G. Jansen
- 单位：Distributed and Embedded Systems Group, University of Twente
- 发表：`14th IEEE International Symposium on Modeling, Analysis, and Simulation`，2006
- DOI：`10.1109/MASCOTS.2006.52`
- 链接：[DOI](https://doi.org/10.1109/MASCOTS.2006.52)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`RTnet` 分布式实时网络协议的 token 传递、流调度与故障恢复机制
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文 PDF 可公开获取，但未提供独立模型仓库或查询文件。
- 案例/数据获取方式：论文给出了 unicast/broadcast token 两种协议变体、节点角色、参数与 stream set，可按正文重建。

## 简报

这篇论文关心的是一个真实协议对象，而不是泛泛的 timed automata 示例。`RTnet` 运行在具备广播能力的局域网中，需要同时支持实时流、非实时流和节点动态加入/移除，因此故障恢复能力是它的核心卖点。

- 系统：`RTnet` 协议中的 token holder / monitor / idle 节点和网络介质。
- 特点：广播局域网、动态节点加入退出、实时流调度、控制报文可能丢失。
- 规模：实验重点使用 `4` 节点 stream set，利用率大约 `82%` 与 `96%` 两组负载。
- 模型：每个节点一个协议 automaton，加一个 network automaton 区分控制包和数据包。
- 性质：稳定性、唯一 token/monitor/transmit、故障恢复、轮询冲突、恢复时长。
- 方法：分别建模 unicast token 与 broadcast token，按 `0-2` 个 packet loss 做验证实验。
- 结果：单包丢失下两种变体通常都能恢复；broadcast token 比 unicast 更容易出现并发发送和更弱鲁棒性。

`RTnet 协议角色/消息 -> node + network automata -> 稳定性/冲突/恢复查询 -> 比较 unicast 与 broadcast 变体`

## 论文定位

这是很标准的 `🛰️ + 🌐` 应用协议案例。虽然论文中有建模技巧，但核心贡献中心是具体协议在故障场景下的形式化分析，而不是 `UPPAAL` 技术本体。

## 验证对象与问题背景

### 系统与场景

`RTnet` 面向全连接、支持广播的局域网，目标是在同一协议内支持实时和非实时通信，并允许节点在线加入或移除。

### 系统组成与运行机制

每个节点在协议运行中会轮流承担三种角色：

1. `token holder`
2. `monitor`
3. `idle`

协议通过 token 在节点间传递来分配发送权限，并通过 monitor 监督当前 token holder 的行为。若控制包丢失，则需要通过 poll 等机制恢复协议稳定状态。

### 验证边界

论文主要覆盖协议控制逻辑和丢包恢复，不展开真实硬件驱动、比特级物理层和复杂应用负载生成器。

### 核心问题

1. 无故障时协议是否稳定。
2. 丢包后系统是否会长期失稳或出现多个发送者。
3. 恢复时长是否可估计、可接受。

## 模型与形式化建模

### 抽象对象

模型由两部分组成：

1. **node automata**
   - 对应协议状态机与角色切换。
2. **network automaton**
   - 抽象控制包与数据包传输，并非确定地决定是否丢包。

### 建模形式

作者分别为 unicast token 和 broadcast token 两种协议变体建模，并对控制消息、数据流和加入/移除操作建立同步关系。

### 关键抽象与取舍

1. 假设消息要么完整到达，要么丢失，不考虑内容被篡改。
2. 流集合和调度参数采用代表性负载而非无限参数化。
3. 恢复时长通过附加 clock 和标志位计算上下界。

## 验证目标与性质

### 待验证问题

论文将性质分成三类：

1. 稳定性和唯一性。
2. 故障后是否能恢复。
3. 恢复需要多长时间。

### 性质类型

这些性质覆盖安全、活性和有界恢复时间。

### 查询表达

代表性查询包括：

1. 是否最多只有一个 token holder / monitor / transmitter。
2. 是否能重新回到稳定状态。
3. 在单次 packet loss 后恢复时间的上下界。

## 核心方法与验证流程

1. 从 `RTnet` 状态转移图出发建立节点模型。
2. 用 network automaton 表达消息送达与丢失。
3. 分别配置 unicast 与 broadcast token。
4. 在不同 stream set、调度粒度和 packet loss 参数下运行查询。
5. 比较两种协议变体的稳定性和恢复特性。

## 案例与结果

论文给出了几类关键发现：

1. 无故障时，协议满足预期稳定性。
2. 在单包丢失下，多数实验仍能恢复，且不会把节点永久打入错误状态。
3. broadcast token 变体比 unicast token 更容易出现多节点并发发送和更弱恢复鲁棒性。
4. 恢复时间具有可估计边界，unicast 变体的最大恢复时长通常与估计式 `CLCU + δpoll` 一致。

这些结果直接支持论文的结论：`RTnet` 的 fault recovery 可以被形式化量化，但广播版设计在故障下代价更高。

## 与本研究的关系

### 相关性分析

论文展示了“协议状态机 + 故障场景 + 时间恢复界”的完整应用链，对博士研究中的验证场景生成很有参考价值。

### 可借鉴之处

1. 把稳定性、冲突和恢复时长拆成明确的性质簇。
2. 在同一模型中同时做定性和定量验证。
3. 用协议角色视角组织模型，便于回映反例。

### 存在的不足与改进空间

实验主要集中在代表性 `4` 节点场景；节点规模和工件开放度都比较有限。

### 对本研究的启发

它说明通信协议验证不能只看“不会死锁”，还要明确恢复条件、恢复代价和不同协议变体的鲁棒性差异。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文 PDF 公开，但未见独立 `UPPAAL` 模型、查询文件或协议实验包公开入口。
- 获取方式/链接：[DOI](https://doi.org/10.1109/MASCOTS.2006.52)；[公开 PDF](https://ris.utwente.nl/ws/files/5489944/hanssen.pdf)
- 对后续复用的现实影响：适合复用其协议角色划分和恢复查询组织方式，但复跑仍需自行重建模型。
