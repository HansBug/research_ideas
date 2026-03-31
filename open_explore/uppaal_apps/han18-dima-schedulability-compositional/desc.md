问题一句话：本文验证的是 `DIMA` 航电系统的组合式可调度性，核心问题是面对状态空间爆炸时，能否通过消息接口和 assume-guarantee 推理，把原本不可直接验证的全系统调度问题拆成可独立检查的分区问题。
方法一句话：作者基于 `UPPAAL` 秒表自动机提出 message interface、timed selection simulation 和 assume-guarantee 组合分析流程，逐个验证分区在其通信环境假设下的 schedulability。
验证收获一句话：论文在与前一篇相同的 `DIMA` 案例上证明了组合式分析可以显著降低状态空间，并同样定位出 `P3` 因 `Msg2` 刷新周期违例而不可调度；修改分区表后，全部分区分别可证可调度。

## 基本信息

- 标题：A Compositional Approach for Schedulability Analysis of Distributed Avionics Systems
- 中文标题：分布式航电系统可调度性分析的组合式方法
- 作者：Pujie Han、Zhengjun Zhai、Brian Nielsen、Ulrik Nyman
- 单位：Northwestern Polytechnical University；Aalborg University
- 发表：EPTCS 272 (MeTRiD 2018)，2018
- DOI：`10.4204/EPTCS.272.4`
- 链接：[DOI](https://doi.org/10.4204/EPTCS.272.4)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🚀 航天
- 被验证系统：通过 `AFDX` 网络通信的 `DIMA` 航电分区系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未给出稳定公开模型仓库。
- 案例/数据获取方式：案例参数来自已有 workload 与 `AFDX` 配置组合，论文给出关键参数但无完整工程包。

## 简报

这篇论文可以看作上一篇 `DIMA` 工作的“降维版”：对象还是同一类航电系统，但重点从“怎么建模型”转向“如何把难以直接验证的大系统拆小再验证”。作者通过 message interface 和 assume-guarantee，把每个 partition 的外部通信环境抽象成更小模型。

- 系统：`5` 分区 `DIMA` 系统，分布在 `3` 个模块和 `AFDX` 网络上。
- 特点：同一对象上强调状态空间削减和组合推理，而非再引入统计测试。
- 规模：全局模型约 `51` 个 processes；组合后单个分区验证通常只涉及很少任务模型。
- 模型：各分区仍用 `UPPAAL` `SWA` 建模，但外部环境被 message interface 抽象替代。
- 性质：各分区的 `A[] not perror[i]`，最终推导全局可调度。
- 方法：decomposition -> interface construction -> local model checking -> deduction。
- 结果：`Case 1` 下 `P3` 不可调度；交换 `P1/P2` 时间窗后 `Case 2` 全部分区可调度。

`全局 DIMA 模型 -> 分区拆分 -> message interface 构造 -> 局部 A[] not perror[i] 验证 -> assume-guarantee 推导全局结论`

## 论文定位

本文同样是 `⏱️ + 🚀` 航电案例，但方法色彩比前一篇更强。它依然有真实 `DIMA` 系统对象，不过真正的新意是组合式验证流程，因此更适合作为“复杂状态机系统如何拆分验证”的参考。

## 验证对象与问题背景

### 系统与场景

对象仍是通过 `AFDX` 互联的 `DIMA` 航电系统。由于分区之间通信依赖复杂，全局符号模型检查很容易状态爆炸。

### 系统组成与运行机制

每个分区 `Pi` 都由分区调度器、任务模型及其接收通信模型组成；分区间通过消息类型 `Msg1-Msg4` 和对应虚链路交换数据。系统级目标仍是同时满足本地 deadline 和通信约束。

### 验证边界

本文重点研究如何在局部假设下验证 schedulability，而不是重新定义完整通信或任务语义。

### 核心问题

作者要解决的是：

1. 如何为每个分区构造足够保守但不至于过大的通信环境抽象
2. 如何证明这些抽象在 assume-guarantee 推理下仍能推出全局可调度结论

## 模型与形式化建模

### 抽象对象

除了原始分区模型 `Pi` 外，本文新增的关键对象是：

1. 单消息类型接口 `A_i^k`
2. 组合消息接口 `A_i,j`
3. timed selection simulation 关系

### 建模形式

消息接口被建成只描述发送行为的 `TA`，用于抽象其他分区对当前分区的通信环境。系统再通过 `Pi || environment` 的方式逐个分区验证。

### 关键抽象与取舍

1. 假设任务在跨分区通信时不会阻塞，以避免循环推理。
2. 接口参数如 `period/initOffset/offset/jitter` 通过二分搜索启发式调优。
3. 该方法给出的是 schedulability 的充分条件，而不是必要条件。

## 验证目标与性质

### 待验证问题

每个分区的局部性质被统一写成：

`A[] not perror[i]`

即一旦任意本地 error location 被触达，该分区就不可调度。

### 查询表达

核心查询和推理对象包括：

1. `A[] not perror[i]`
2. `Pj ⪯ A_i,j` 形式的接口抽象关系
3. 基于 assume-guarantee 规则把所有局部结果合成为全局可调度结论

## 核心方法与验证流程

1. 把系统分解为 `5` 个 partition 模型。
2. 为每个 partition 构造其接收消息环境的接口自动机。
3. 在 `Pi || interfaces` 上验证 `A[] not perror[i]`。
4. 根据 assume-guarantee 规则汇总全部局部结果。

## 案例与结果

论文在与前一篇相同的 `DIMA` 系统上得到以下结果：

1. `Case 1` 中除 `P3` 外其余分区都可调度，`P3` 违反 `Msg2` 刷新周期约束。
2. 通过仿真得到反例后，作者把 `P1/P2` 时间窗对调。
3. `Case 2` 中五个分区全部分别验证通过，因此系统在全局层面可调度。
4. 与全局直接验证相比，组合式分析把单次验证规模控制在远小于 `51` 个 process 的范围内，显著降低了状态空间。

## 与本研究的关系

### 相关性分析

它对博士研究有直接价值，因为“按元素拆分状态机环境，再逐块验证”非常适合后续做 verification profile 或针对局部缺陷的修复。

### 可借鉴之处

1. 将通信环境单独抽象成 message interface。
2. 把复杂全局验证问题拆成多个局部安全性质。
3. 用显式抽象关系支撑 assume-guarantee 推理，而不是凭经验口头说明。

### 存在的不足与改进空间

接口构造仍需要工程师手工参与，且只给出充分条件；若接口过于保守，可能得到“局部不通过但全局未必真的不可调度”的情况。

### 对本研究的启发

这篇论文说明，对大型控制系统状态机，验证 profile 不一定只是一组查询，也可以包含“如何局部化环境”的建模规则。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未给出稳定公开的消息接口模板或完整模型工程。
- 获取方式/链接：[DOI](https://doi.org/10.4204/EPTCS.272.4)；[PDF](https://cgi.cse.unsw.edu.au/~eptcs/paper.cgi?MeTRiD2018.4.pdf)
- 对后续复用的现实影响：适合作为组合式 schedulability 验证套路参考，但若要复跑需自行重建接口模板。
