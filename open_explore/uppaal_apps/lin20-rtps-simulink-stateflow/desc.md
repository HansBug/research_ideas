问题一句话：本文验证的是 `DDS/RTPS` 发布订阅协议，核心问题是 writer 与多个 reader 之间的数据样本顺序、确认修复机制和传输成功概率，是否在不可靠信道下仍满足协议要求。
方法一句话：作者同时构建 `Simulink/Stateflow` 与 `UPPAAL` 两套形式模型，并证明翻译后的 timed automata 是前者的 refinement，再用 `TCTL` 和 `SMC` 检查正确性与性能。
验证收获一句话：论文证明关键一致性与确认机制性质全部成立，并通过 `SMC` 量化表明，当信道通过率超过 `0.8` 时限内成功传输几乎可以保证，而过大的响应延迟会显著降低传输效率。

## 基本信息

- 标题：Modelling and Verification of Real-Time Publish and Subscribe Protocol Using Uppaal and Simulink/Stateflow
- 中文标题：使用 `Uppaal` 与 `Simulink/Stateflow` 对实时发布订阅协议建模与验证
- 作者：Qian-Qian Lin、Shu-Ling Wang、Bo-Hua Zhan、Bin Gu
- 单位：中国科学院软件研究所 State Key Laboratory of Computer Science；北京控制工程研究所
- 发表：Journal of Computer Science and Technology，2020
- DOI：`10.1007/S11390-020-0537-8`
- 链接：[DOI](https://doi.org/10.1007/S11390-020-0537-8)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`DDS` 互操作协议 `RTPS` 的 writer/reader/history cache 交互机制
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：原文未提供稳定公开的 `UPPAAL`/`Stateflow` 模型仓库或生成代码仓库。
- 案例/数据获取方式：案例来自 `RTPS` 协议规范和作者配置的通信参数，无独立公开数据集。

## 简报

本文不是单纯把 `RTPS` 画成几个状态机，而是搭了一个“双模型”框架：`Stateflow` 负责仿真与代码生成，`UPPAAL` 负责性质证明与性能估计。被验证对象集中在 writer/reader 的 history cache、一致性、心跳和重传逻辑上。

- 系统：`RTPS` 中 writer、reader、`WHC/RHC`、heartbeat 与 `ACKNACK` 协议机制。
- 特点：不可靠信道、数据重传、双建模语言、还带性质保持证明。
- 规模：一个 writer 配多个 readers；代表性数据样本数组为 `[100,200,300,400,500]`。
- 模型：`Stateflow` 模型经翻译得到 `UPPAAL` timed automata。
- 性质：死锁自由、样本顺序一致、heartbeat 周期性、缺失样本后最终修复、限时内完成传输概率。
- 方法：`TCTL` + `SMC` + `Stateflow -> TA` refinement 证明。
- 结果：所有核心符号性质成立；通过率高和延迟小都能明显提升限时内完成传输的概率。

`RTPS 规范 -> Stateflow/UPPAAL 双模型 -> 一致性/确认机制/性能查询 -> 协议正确性证明 + 参数敏感性分析`

## 论文定位

本文属于 `🛰️ + 🌐` 的中间件协议案例。虽然翻译和性质保持证明占了较大篇幅，但验证对象始终是具体的 `RTPS` 协议，因此仍是应用协议论文而不是纯工具论文。

## 验证对象与问题背景

### 系统与场景

`DDS` 是面向实时分布式系统的中间件技术，`RTPS` 是其中负责互操作消息交换的关键协议。它广泛面向航天、国防和资源受限但要求可预测性的分布式系统。

### 系统组成与运行机制

论文围绕以下核心实体展开：

1. `Writer` 与其 `Writer History Cache (WHC)`
2. 多个 `Reader` 与各自 `Reader History Cache (RHC)`
3. `HEARTBEAT` 消息
4. `ACKNACK` 与 repair 机制

writer 周期性通告可用样本；reader 接收心跳后在缺样时发送 `ACKNACK`；writer 再进入 repair 状态补发缺失数据。

### 验证边界

本文主要分析协议控制逻辑、缓存一致性和性能参数，不展开底层网络实现或完整 `DDS` `QoS` 空间。

### 核心问题

作者关注：

1. 数据样本是否按顺序送达
2. 所有 reader 的缓存内容是否最终与 writer 一致
3. 心跳与确认机制是否保证重传闭环
4. 在不可靠信道和不同定时参数下，限时传输成功概率怎样变化

## 模型与形式化建模

### 抽象对象

模型保留了：

1. writer/reader 的状态与同步行为
2. `WHC/RHC` 数组内容
3. 心跳、确认和修复相关标志位
4. 信道通过率和时延参数

### 建模形式

一方面，`Stateflow` 用于仿真和导出可执行代码；另一方面，翻译规则把 `Stateflow` 子集转换为 `UPPAAL` timed automata，并证明 `Stateflow` 模型是译后模型的 refinement。

### 关键抽象与取舍

1. 聚焦协议核心行为，不覆盖 `Stateflow` 全部高级特性。
2. 只对一部分 `TCTL` 片段给出严格性质保持证明。
3. 概率性能分析只在 `UPPAAL SMC` 模型上完成。

## 验证目标与性质

### 待验证问题

论文把性质分成三组：

1. 一致性与顺序性
2. heartbeat/acknowledgement 机制正确性
3. 传输完成概率与参数敏感性

### 查询表达

代表性查询包括：

1. `A[] not deadlock`
2. `A<> forall (sq: sq_t) WHC[sq] == cachechanges[sq]`
3. `A[] forall (id: rid_t) ... imply RHC[id][sq] == cachechanges[sq]`
4. `A<> Writer_repair(WriterId).must_repair`
5. `Pr[<=300;1000](<> acked_all())`

这些查询分别对应死锁自由、缓存一致性、确认驱动的修复必达和限时完成传输概率。

## 核心方法与验证流程

1. 先在 `Stateflow` 中建立 `RTPS` 协议模型并做仿真。
2. 将模型翻译为 `UPPAAL` timed automata。
3. 用 `TCTL` 检查死锁自由、顺序性和心跳/确认机制。
4. 再用 `SMC` 改变 passing rate、`heartbeatResponseDelay`、`nackResponseDelay` 等参数，估算完成传输的概率。

## 案例与结果

论文的关键结果包括：

1. 仿真显示两个 readers 会在不同时间收到数据，说明丢包补发逻辑生效。
2. 所有列出的 `TCTL` 正确性性质都被 `UPPAAL` 证明成立。
3. 对 `Pr[<=300;1000](<> acked_all())` 的统计分析表明，信道通过率越高，限时内成功传输的概率越高；当通过率超过 `0.8` 时几乎可以保证完成。
4. 当 `PassingRate = 0.7` 且 `heartbeatPeriod = 10` 固定时，更小的 `heartbeatResponseDelay` 和 `nackResponseDelay` 会提高传输效率，但现实部署中也可能带来拥塞。

## 与本研究的关系

### 相关性分析

它与博士研究中的“状态机结构化建模 + 性质保持 + 性能化验证”非常接近，尤其适合作为“协议状态机 + 翻译 + 验证”的完整链路样本。

### 可借鉴之处

1. 同一对象同时保留可执行仿真模型和可验证抽象模型。
2. 把一致性、顺序性和确认机制拆成性质簇逐项验证。
3. 用 `SMC` 补足“协议参数如何影响性能”的问题。

### 存在的不足与改进空间

模型和生成代码未公开，且性质保持证明只覆盖受限片段；若要大规模复用仍需重新实现翻译链。

### 对本研究的启发

这篇论文说明，LLM 生成状态机后不必只停在“能验证”，还可以继续衔接仿真和性能估计，形成更完整的建模闭环。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文和扩展版 PDF 可公开获取，但未见稳定模型仓库、`Stateflow` 工程或生成代码下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.1007/S11390-020-0537-8)；[扩展 PDF](https://lcs.ios.ac.cn/~bzhan/jcst20extended.pdf)
- 对后续复用的现实影响：适合作为 `RTPS` 性质模板和双模型流程参考，但若要复跑仍需自行重建模型。
