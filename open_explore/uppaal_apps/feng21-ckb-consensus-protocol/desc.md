问题一句话：本文验证的是 Nervos `CKB` 区块链共识协议中的 two-step confirmation 机制，核心问题是交易从 proposal 到 commitment 的整个确认链条是否满足若干必要安全条件，并在交易缺失时能否正确拉黑故障矿工。
方法一句话：作者把 `TwoStep`、`MiningNode`、`FullNode` 和 `BlockPropagation` 四部分建成 `UPPAAL` 自动机，并用 `7` 条性质刻画 proposal / commitment / missing transaction / blacklist / deadlock 等关键行为。
验证收获一句话：论文在一个简洁模型中证明了交易只有经过 `txid` 检查、全节点接收与验证后才能进入 proposal/commitment，同时缺失交易在请求和查询均失败后会触发矿工断开与黑名单，是区块链协议状态机化验证的紧凑样本。

## 基本信息

- 标题：Modeling and Verification of CKB Consensus Protocol in UPPAAL
- 中文标题：`CKB` 共识协议在 `UPPAAL` 中的建模与验证
- 作者：Yi-Chun Feng、Yuteng Lu、Meng Sun
- 单位：Peking University
- 发表：SEKE 2021 / International Conference on Software Engineering and Knowledge Engineering
- DOI：`10.18293/SEKE2021-072`
- 链接：[DOI](https://doi.org/10.18293/SEKE2021-072)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：Nervos `CKB` 区块链中的共识与区块传播协议
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文与会议 PDF 可获取，但未给独立 `UPPAAL` 模型仓库。
- 案例/数据获取方式：案例来自 `CKB` 共识协议设计和区块传播规则，不依赖外部数据集。

## 简报

这篇论文关注的是 `CKB` 相对 Bitcoin 的一个关键设计点：两步确认。作者用一个很紧凑的 `UPPAAL` 模型把 proposal zone、commitment zone、矿工、全节点和缺失交易追问过程串起来，因此能够直接验证“什么条件下交易才算 proposed / committed”。

- 系统：`CKB` 共识协议中的 two-step confirmation 与 block propagation。
- 特点：显式保留 proposal / commitment 双阶段、miner / full node 分工和 missing transaction 处理。
- 规模：模型至少含 `TwoStep`、`MiningNode`、`FullNode`、`BlockPropagation` 四个核心自动机，并用 `7` 条性质检查关键行为。
- 模型：基于 timed automata 的协议状态机。
- 性质：proposal 合法性、全节点接收/验证、commitment 边界、缺失交易追问、黑名单、无死锁。
- 方法：围绕交易状态 `T1-T6` 和传播状态 `P1-P4` 写出 `A[]` / `A<>` 查询。
- 结果：所有给定性质在模型中成立，说明 two-step confirmation 的抽象逻辑一致。

`CKB 共识流程 -> proposal/commitment 与传播自动机 -> 7 条关键安全性质 -> 验证交易确认与缺失处理边界`

## 论文定位

这是一篇典型的“区块链协议流程验证”论文。它关注的不是性能评估或博弈攻击概率，而是协议状态机层面的合法状态迁移，因此属于 `🛰️` 主轴下的协议验证案例。

## 验证对象与问题背景

### 系统与场景

被验证对象是 Nervos `CKB` 共识协议。相较于 Bitcoin，它通过 two-step confirmation 设计改善吞吐和对 selfish mining 的抵抗能力。

### 系统组成与运行机制

论文把协议核心拆成：

1. **TwoStep**
   - 表示交易从生成到 proposal，再到 commitment 的阶段推进。
2. **MiningNode**
   - 表示矿工挖块和对缺失交易请求的响应。
3. **FullNode**
   - 表示全节点对交易的接收、验证和确认。
4. **BlockPropagation**
   - 处理缺失交易查询与矿工拉黑逻辑。

### 运行机制

关键流程是：

1. 新交易先进入 proposal zone；
2. proposal 阶段结束后，合格交易进入 commitment zone；
3. commitment 完成后交易才被认为真正 committed；
4. 若传播中发现交易缺失，则启动 request / querying 机制向矿工追问。

### 验证边界

本文验证的是**共识协议的离散状态转移与传播逻辑**，不是经济激励分析、密码学证明或网络大规模仿真。

### 核心问题

作者关注的不是“概率上大概安全”，而是几个必要逻辑条件：

1. 未经检查的交易不能被 proposed；
2. 全节点未收到或未验证的交易不能进入后续阶段；
3. commitment 必须满足高度边界；
4. 追问失败的矿工应被断开和拉黑；
5. 模型不能死锁。

## 模型与形式化建模

### 双阶段确认

`TwoStep` 自动机显式保留：

1. proposal step；
2. commitment step；
3. 交易状态 `T1-T6`。

其中 `T1` 表示进入 proposal zone，`T4` 表示交易被视为 proposed，`T5` 表示进入 commitment zone，`T6` 表示 committed。

### 矿工与传播

`MiningNode` 模型负责挖块和回应该交易是否可重新发送；`BlockPropagation` 负责在交易缺失时发起 request / querying，并在连续失败后把矿工视为 fault peer。

### 全节点

`FullNode` 负责接收交易、检查 `txid`、验证交易内容以及判断交易是否应进入 commitment。

## 验证目标与性质

### 待验证问题

论文给出 `7` 条性质，核心包括：

1. 新交易都会经过 proposal zone；
2. proposed 交易必须先通过 `txid` 检查；
3. proposed 交易必须已被 full nodes 接收并验证；
4. 进入 commitment zone 的交易也必须满足接收和验证前提；
5. committed 交易必须满足 `close <= hc-hp <= far`；
6. 缺失交易在 request/query 均失败后，矿工被断开并拉黑；
7. 模型无死锁。

### 性质类型

1. 安全前置条件；
2. 有界一致性；
3. 异常处理；
4. 死锁安全。

### 查询表达

文中查询大多为：

1. `A<> TwoStep:T1`
2. `A[] TwoStep:T4 imply ...`
3. `A[] TwoStep:T5 imply ...`
4. `A[] BlockPropagation:P3 and BlockPropagation:P4 imply MiningNode:M6`
5. `A[] not deadlock`

## 核心方法与验证流程

1. 先对 `CKB` 的 proposal / commitment 机制做协议级抽象。
2. 分别建立交易阶段、矿工、全节点和传播自动机。
3. 用变量如 `checkT`、`checkR`、`checkV`、`checkC`、`hp`、`hc` 表示检查与高度关系。
4. 将必要安全条件写成 `UPPAAL` 查询。
5. 对正常确认路径和缺失交易处理路径分别验证。

这是一种非常“规约驱动”的建模方式：每条查询都直接对应一条协议直觉。

## 案例与结果

### Proposal / Commitment 条件

论文证明：

1. 交易进入 proposal zone 后，还必须通过 `txid` 检查；
2. 被视为 proposed 前，全节点必须已接收并验证；
3. 进入 commitment zone 也需要相同前提；
4. committed 交易还要满足高度边界约束。

### 缺失交易

在 block propagation 路径中，如果交易缺失且矿工在 request / querying 后仍无法提供交易，则对应矿工会被断开并拉黑。

### 死锁

作者还显式验证了 `A[] not deadlock`，说明在该抽象层下协议过程是可重复执行的。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究的关系在于：它非常清楚地展示了如何把协议描述压成少量状态变量和阶段状态，再把必要条件逐条写成性质簇。

### 可借鉴之处

1. 用阶段状态 `T1-T6` 清晰组织协议语义。
2. 异常处理路径与正常路径在同一模型里统一验证。
3. 性质写法直接对着协议不变量和阶段前提。

### 存在的不足与改进空间

1. 论文篇幅较短，模型规模和实验展开都较有限。
2. 没有公开独立模型仓库。
3. 更像流程级验证，而非对复杂攻击面的全面分析。

### 对本研究的启发

它适合作为“如何把协议流程分层结构化后生成性质”的小而完整的范例。

## 重要的相关工作

### 1. Bitcoin / Blockchain 形式化验证

- 论文把自身放在区块链协议形式化验证的持续研究脉络中。

### 2. Two-step confirmation

- 这是 `CKB` 与其他协议区分度最高、也是本文验证重心最集中的机制。

### 3. `UPPAAL`

- `UPPAAL` 在这里承担协议逻辑 sanity check 和异常传播验证工具。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：会议论文可获取，但未确认到独立 `UPPAAL` 模型仓库或查询工件。
- 获取方式/链接：[DOI](https://doi.org/10.18293/SEKE2021-072)；[会议 PDF](https://ksiresearch.org/seke/seke21paper/paper072.pdf)
- 对后续复用的现实影响：适合借鉴其协议分阶段建模方式，但现实复跑仍需自行重建模型。
