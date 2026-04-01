问题一句话：本文验证的是异构区块链之间的 pub-sub 互操作协议，核心问题是 publisher、broker 与 subscriber 之间的 API 调用链在给定吞吐约束下是否能可靠完成消息互通。
方法一句话：作者先从 JavaScript chaincode 抽取调用图和上下文信息，再把 publisher、subscriber、broker connector、broker topic 建成 `UPPAAL-SMC` 的 stochastic timed automata 网络，验证功能与实时性质。
验证收获一句话：论文证明了一组核心功能性质成立，并进一步量化了不同吞吐组合下 topic 创建与消息送达的概率，表明 broker 吞吐配置会显著影响端到端互操作效果。

## 基本信息

- 标题：Formal verification of the pub-sub blockchain interoperability protocol using stochastic timed automata
- 中文标题：使用随机 timed automata 对 pub-sub 区块链互操作协议进行形式化验证
- 作者：Md Tauseef Alam、Raju Halder、Abyayananda Maiti
- 单位：Indian Institute of Technology Patna
- 发表：Frontiers in Blockchain，2023
- DOI：`10.3389/fbloc.2023.1248962`
- 链接：[DOI](https://doi.org/10.3389/fbloc.2023.1248962)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：区块链 pub-sub 互操作协议中的 publisher / subscriber / broker 消息交互机制
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文提供 `JavaScriptChaincodeAnalyzer` 仓库 [GitHub](https://github.com/mdtauseefalam/JavaScriptChaincodeAnalyzer/)；`UPPAAL` 模型仍需依据分析结果和文中步骤重建。
- 案例/数据获取方式：案例由 pub-sub 协议 chaincode 与 Hyperledger 官方仓库中的代表性 chaincode 构成。

## 简报

这篇论文验证的不是某一条链上的合约，而是多条异构链之间的消息互操作协议。它把协议专属 chaincode 的调用图抽出来，再把 publisher、subscriber 与 broker 的交互抽成随机 timed automata，使“跨链消息有没有丢、多久能到”变成可统计验证的问题。

- 系统：pub-sub 区块链互操作协议，参与方包括 publisher、subscriber、broker connector 和 broker topic。
- 特点：异构链、链码调用图、跨链 API 同步、吞吐敏感、消息中介式转发。
- 规模：建模 `4` 类 actor/template，并为避免状态爆炸固定验证 `5` 个 topics；性能实验覆盖 `10` 个 chaincodes。
- 模型：根据 analyzer 抽取的调用图、全局变量、guard 和 throughput 参数构造 `NSTA`。
- 性质：注册、topic 创建、topic 同步、消息通知、重复 topic 传播，以及时限内成功概率和消息丢失比较。
- 方法：先做 `TCTL` 功能验证，再做 `MITL` 风格概率估计与概率比较。
- 结果：核心功能性质成立；不同吞吐配置下消息互通概率差异明显；协议层面未观察到 broker 到 subscriber 的消息丢失。

`chaincode 源码 -> 调用图/上下文抽取 -> NSTA -> TCTL/MITL queries -> 跨链互通概率`

## 论文定位

本文是 `🛰️ + 🌐` 的现代协议应用条目，但偏方法驱动：它不仅验证协议，还构建了从 chaincode 到 `UPPAAL-SMC` 模型的分析链。因此更适合作为 `🟡 可整理` 条目。

## 验证对象与问题背景

### 系统与场景

被验证对象是 Linux Foundation 提出的区块链 pub-sub 互操作协议。它允许不同区块链网络上的实体通过 broker 进行 many-to-many 通信。

### 系统组成与运行机制

论文中的关键对象包括：

1. Publisher connector chaincode
2. Subscriber connector chaincode
3. Broker connector chaincode
4. Broker topic chaincode

publisher 先在 broker 注册，再创建 topic 并发布消息；subscriber 订阅 topic；broker 保存区块链和 topic 关系，并负责把消息从 publisher 转发给 subscriber。

### 验证边界

本文验证的是**协议专属 chaincodes 的互操作行为**，而不是具体业务应用，也不是底层区块生成和共识算法的完整实现。

### 核心问题

在跨链支付、供应链金融等实时场景中，一次消息丢失或延迟就可能导致严重后果，因此需要确认：topic 是否能正确创建、订阅是否能同步、消息是否能可靠到达。

### 研究动机

既有区块链形式化验证主要针对单链协议、共识或智能合约，而互操作协议几乎没有被模型检查覆盖。

## 模型与形式化建模

### 建模对象

1. Chaincode 的状态转换
2. 外部函数调用对应的同步通道
3. topic / blockchain / subscriber 关系数组
4. 由 throughput 导出的 transaction 时间上界

### 模型形式

作者把 chaincode 形式化为有限状态转移系统，并在 `UPPAAL-SMC` 中实现为 stochastic timed automata network。

### 关键抽象

1. 共识过程细节被抽象，只保留由 throughput 派生的平均交易时间。
2. 通过 `Chaincode Analyzer` 抽取调用图、上下文信息和全局变量。
3. 各 actor 以模板方式建模，topic 数量固定为 `5` 以缓解状态爆炸。

## 验证目标与性质

### 待验证问题

1. publisher / subscriber 是否最终能够加入协议。
2. publisher 创建的 topic 是否最终在 broker 上建立。
3. 已订阅 subscriber 是否最终收到 publisher 更新的消息。
4. 端到端消息是否会在 broker 中丢失。
5. 不同吞吐配置下，上述行为在给定时间窗内成功的概率有多大。

### 性质类型

1. Reachability
2. Liveness
3. 概率时限性质

### 性质分组与实际含义

1. 注册与 topic 建立
   协议是否能正常完成初始互联。
2. 互操作消息传递
   publisher 发布的消息是否能传播到订阅者。
3. 吞吐敏感性
   不同链配置对成功概率的影响。

### 查询表达

论文给出了多条典型查询，例如：

1. `E<> Pub.Registered imply DispatcherConnector.Registered`
2. `A<> Pub.TopicCreated imply DispatcherTopic.TopicCreated`
3. `A<> ((Pub.Published and SubFabric.Subscribed) imply SubFabric.Notified)`
4. `Pr[<=100](<> Pub.TopicCreated imply DispatcherTopic.TopicCreated)`
5. `Pr[<=100](<> DispatcherTopic.Published imply SubFabric.Notified)`

## 核心方法与验证流程

1. 对 JavaScript chaincodes 做静态分析，抽取调用图和上下文。
2. 识别同步通道、状态、guard、update 与全局数组。
3. 基于 publisher / subscriber / broker 两类 chaincode 在 `UPPAAL-SMC` 中搭建 `NSTA`。
4. 先用 `TCTL` 验证核心功能性质，再用时限概率性质量化 throughput 影响。
5. 对 benchmark chaincodes 评估 analyzer 的时间和内存开销。

## 案例与结果

### 案例规模

1. 模型包含 `4` 类 actor/template。
2. 性能评估覆盖 `10` 个 chaincodes。
3. throughput 取值包括 Fabric v2 `20000 TPS`、Fabric v1.4 `3000 TPS`、Besu `300 TPS`。

### 主要结果

1. 功能性质 `(1)-(5)` 均被 `UPPAAL-SMC` 判定满足。
2. “publisher 在 `45` 时间单位内创建 topic” 的概率估计约为 `[0.0990515, 0.199051]`。
3. “publisher 创建后 broker 在 `100` 时间单位内也创建该 topic” 的概率约为 `[0.901855, 1]`。
4. subscriber 在 `10-100` 时间单位内收到 publisher 消息的概率，在不同吞吐组合下可从约 `[0.153252, 0.253252]` 到 `[0.92561, 1]`。
5. 概率比较结果表明，broker 发布到 subscriber 的链路未出现额外消息丢失。

### 结果解释

这说明跨链互操作协议的正确性不只取决于逻辑步骤，还明显依赖三方链的吞吐匹配关系；broker 配置不当时，端到端通知成功概率会显著下滑。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究的价值在于：它展示了如何从源代码或接口层结构化抽取模型元素，再反向生成验证模型与性质。

### 可借鉴之处

1. 以调用图和上下文抽取驱动状态机建模。
2. 把吞吐等系统参数显式转成时钟/不变式。
3. 将 reachability、liveness 与概率性质并置，形成分层验证。

### 存在的不足与改进空间

1. `UPPAAL` 模型仍需人工 drag-and-drop 重建。
2. 验证时假设通信信道公平、硬件故障可忽略。
3. 状态爆炸限制了 topics 数量。

### 对本研究的启发

对博士研究尤其重要的一点是：如果后续要把 LLM 生成的状态机与代码/链路配置打通，这种“源代码/调用图 -> 状态机网络 -> 查询”的路径非常值得借鉴。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文开放获取，且 analyzer 仓库可访问，但未提供现成 `UPPAAL` 模型文件。
- 获取方式/链接：[DOI](https://doi.org/10.3389/fbloc.2023.1248962)；[PDF](https://public-pages-files-2025.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2023.1248962/pdf)；[Analyzer](https://github.com/mdtauseefalam/JavaScriptChaincodeAnalyzer/)
- 对后续复用的现实影响：适合作为“从 chaincode 自动抽取模型元素”的样本，但复用到验证层仍需手工搭建或补全 `UPPAAL` 模型。
