问题一句话：本文验证的是 TCP 与 SCTP 的握手机制，核心问题是 `SCTP` 的四次握手和 cookie 认证是否真的比 `TCP` 更能抵抗 `SYN flooding/DoS`。
方法一句话：作者在 `UPPAAL` 中分别建模 TCP/SCTP 的合法客户端、非法客户端、服务器和 `TCB` 状态，并用性质检查半开连接和资源占用。
验证收获一句话：模型检查结果确认 TCP 会留下 half-open connection 并允许资源被非法客户端占住，而 SCTP 的 cookie 机制能避免这类资源劫持。

## 基本信息

- 标题：Evaluating the Stream Control Transmission Protocol Using Uppaal
- 中文标题：使用 Uppaal 评估流控制传输协议
- 作者：Shruti Saini、Ansgar Fehnker
- 单位：The University of the South Pacific；University of Twente
- 发表：`EPTCS 244 (MARS 2017)`
- DOI：`10.4204/EPTCS.244.1`
- 链接：[DOI](https://doi.org/10.4204/EPTCS.244.1)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：TCP 三次握手与 SCTP 四次握手关联建立机制
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：公开可得 [arXiv PDF](https://arxiv.org/pdf/1703.06568)，未见独立 `UPPAAL` 模型仓库。
- 案例/数据获取方式：无独立数据集，主要依据协议握手流程建模。

## 简报

本文的对象非常明确：不是验证整个传输层协议栈，而是验证 TCP 与 SCTP 在建立连接时的握手逻辑是否会暴露 DoS 攻击面。

- 系统：TCP 三次握手与 SCTP 四次握手。
- 特点：同时建模合法客户端、非法客户端、服务器和 `TCB`。
- 规模：两个协议各包含 client/server/illegitimate client 与连接状态块。
- 模型：对 SYN、ACK、cookie 等关键消息流做 timed automata 建模。
- 性质：half-open connection 是否存在；非法客户端能否占住资源。
- 方法：`UPPAAL` 查询协议状态与资源占用条件。
- 结果：TCP 会暴露 half-open connection 和 resource hogging，SCTP 不会。

`握手协议语义 -> client/server/attacker 自动机 -> half-open/resource queries -> TCP 与 SCTP 安全差异`

## 论文定位

这篇论文是很典型的协议应用验证案例：对象具体，攻击面明确，性质与工程意义也直接对应。因此适合放在 `🛰️ 协议与通信机制 / 🌐 网络与分布式服务`。

## 验证对象与问题背景

### 系统与场景

论文关注 IoT/分布式系统场景下的传输层连接建立问题。TCP 传统的三次握手一直存在 `SYN flooding` 风险，而 SCTP 宣称通过 cookie 机制缓解该问题。

### 系统组成与运行机制

1. 合法客户端
   负责按协议建立连接/association。
2. 非法客户端
   发起请求但不完成认证。
3. 服务器
   维护连接状态并分配资源。
4. `TCB`
   存放协议状态变量和关键信息。

### 验证边界

本文验证的是**握手阶段**。它不分析吞吐、拥塞控制或多流能力，而是聚焦“连接建立阶段是否会留下安全漏洞”。

## 模型与形式化建模

论文分别构造了：

1. TCP legitimate client / illegitimate client / server 模板；
2. SCTP legitimate client / illegitimate client / server 模板；
3. 表示 `TCB` 和消息字段的共享数据结构。

建模时只保留握手所需的包头/块字段，并把客户端行为非确定化，以观察非法客户端是否可以阻塞服务器资源。

## 验证目标与性质

### 待验证问题

1. 合法连接建立时，服务器是否总能进入 fully-established 状态。
2. 是否会留下 half-open connection。
3. 非法客户端是否能成功占住资源。

### 性质类型

1. 安全性质：服务器状态必须和活跃连接匹配。
2. 攻击相关性质：非法客户端不得造成资源 hogging。

### 性质分组与实际含义

1. half-open connection
   对应 TCP 典型 `SYN flooding` 漏洞。
2. resource hogging
   对应服务器是否在未确认对端合法前就消耗连接资源。

## 核心方法与验证流程

1. 先形式化 TCP 三次握手和 SCTP 四次握手。
2. 再加入非法客户端模板。
3. 用 `UPPAAL` 查询 TCP 是否出现 half-open connection。
4. 再检查非法客户端能否使服务器为其保留资源。

## 案例与结果

1. TCP 模型无法满足“活跃连接一定对应 fully-established server state”这类性质，说明 half-open connection 确实存在。
2. 论文进一步确认，这一行为恰好构成 `SYN flooding` 的基础。
3. SCTP 中 association 在 cookie 被验证前不会真正占用资源，因此相关资源劫持性质不成立。
4. 最终结论是：在握手阶段的 DoS 防护上，SCTP 确实优于 TCP。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究的重要意义在于：它展示了如何把“安全漏洞陈述”翻译成协议状态机性质，而不只是做攻击仿真。

### 可借鉴之处

1. 将攻击者显式建模成系统参与者。
2. 把“资源是否被占住”写成可检验的状态性质。
3. 用对照协议揭示设计差异。

### 存在的不足与改进空间

论文只覆盖握手阶段，不涉及更长运行过程和性能评价。

### 对本研究的启发

对后续待验证性质生成来说，这篇论文很适合作为“协议安全需求 -> 状态属性/可达性属性”的示例。

## 重要的相关工作

### 1. TCP SYN flooding

论文直接把 TCP 的半开连接问题作为对照基线。

### 2. SCTP cookie 认证

SCTP 的安全性优势在文中被非常明确地还原为握手状态机差异。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：公开可得 [arXiv PDF](https://arxiv.org/pdf/1703.06568)；未发现配套 `UPPAAL` 模型或查询文件仓库。
- 获取方式/链接：[DOI](https://doi.org/10.4204/EPTCS.244.1)
- 对后续复用的现实影响：适合据论文重建握手模型和攻击性质，但不是现成可复跑案例。
