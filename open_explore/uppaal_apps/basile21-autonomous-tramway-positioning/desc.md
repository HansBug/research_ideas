问题一句话：本文验证的是用自主定位系统替代传统轨道电路的有轨电车定位与联锁方案，核心问题是位置不确定性、通信延迟和虚拟轨道设备会不会引入新的运营危险。
方法一句话：作者把 `OCC/OBC/IXL/TCV` 等模块建成 `UPPAAL SMC` 模型，并采用 model-driven hazard analysis，把预期行为的反面系统化写成概率查询来探索新 hazard。
验证收获一句话：论文不只验证了 `27` 个危险性质，还发现即便对列车位置做保守包络，某些 corner case 依然可能威胁安全；同时模型和实验日志均已公开。

## 基本信息

- 标题：Analysing an autonomous tramway positioning system with the Uppaal Statistical Model Checker
- 中文标题：使用 `Uppaal` 统计模型检查器分析自主有轨电车定位系统
- 作者：Davide Basile、Alessandro Fantechi、Luigi Rucher、Gianluca Mando
- 单位：ISTI-CNR；University of Florence；Thales Italia
- 发表：Formal Aspects of Computing，2021
- DOI：`10.1007/S00165-021-00556-1`
- 链接：[DOI](https://doi.org/10.1007/S00165-021-00556-1)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：基于自主定位系统 (`APS`) 的 tramway 位置检测与联锁协同控制系统
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文明确公开了模型与实验日志仓库。
- 案例/数据获取方式：案例来自 Tuscany `SISTER` 工业项目的 tramway 场景与参数配置；模型和日志公开，但真实工业设备细节仍有抽象。

## 简报

这篇论文验证的不是单条铁路协议，而是一个把传统 track circuit 虚拟化后的整个车-地协同定位场景。重点不是证明“系统永远安全”，而是在需求早期利用 `UPPAAL SMC` 主动挖掘新 hazard，看看自主定位和虚拟设备到底会带来哪些以前没有的问题。

- 系统：`OCC`、`OBC`、`IXL` 与多个 `TCV` 组成的 tramway 自主定位与联锁系统。
- 特点：位置不确定性、保护级 (`PL`) 包络、通信丢失、虚拟标签、degraded mode。
- 规模：实验场景含 `1` 个 `OCC`、`1` 个 `IXL`、`2` 辆 tram、`3` 个 `TCV`，共检查 `27` 个 hazard 性质。
- 模型：工业需求驱动的 `UPPAAL SMC` 模型，模块化分为连接、收位、监督、缓解等子自动机。
- 性质：连接超时、位置未达、错误连接、路权释放错误、保护级超界、降级模式等 hazard 概率。
- 方法：把 hazard 直接写成概率查询，并通过夸大不利条件快速筛查风险。
- 结果：发现多个此前被忽视的新危险；模型与实验日志已公开。

`tramway 需求与场景 -> OCC/OBC/IXL/TCV 模块化模型 -> 27 个 hazard 概率查询 -> 新危险发现与参数敏感性分析`

## 论文定位

本文是很强的 `🎛️ + 🚦` 工业铁路/有轨电车案例。它的重点不是 `UPPAAL` 技术展示，而是把形式化方法前移到需求探索和 hazard 发现阶段，这一点在现有文库里很有代表性。

## 验证对象与问题背景

### 系统与场景

`SISTER` 项目希望用 onboard 自主定位系统替代 tramway 线路上的物理 track circuits，以降低地面设备维护成本并提升灵活性。

### 系统组成与运行机制

核心组成包括：

1. `OCC`：运营控制中心
2. `OBC`：车载计算机
3. `IXL`：联锁设备
4. `TCV`：虚拟轨道电路
5. `APS`：结合卫星定位、惯导和里程计的自主定位系统

tram 周期性向 `IXL` 与 `OCC` 上报带不确定度的位置；联锁再根据位置、路线与虚拟轨道占用情况决定连接、释放和降级动作。

### 验证边界

论文聚焦的是需求探索与 hazard 分析，不是最终 SIL 级定量安全证明；定位融合算法本身也被视作黑盒。

### 核心问题

作者要回答的不是“模型是否完全正确”，而是：

1. 位置不确定性和保护级会不会导致原本没出现过的新 hazard
2. 虚拟化设备是否会破坏既有安全假设
3. 通信丢失和监督超时在何处触发 degraded mode

## 模型与形式化建模

### 抽象对象

论文为多个子功能建立模板，例如：

1. `OCC Connect / ReceivePos / Supervision / Mitigation`
2. `OBC CommOCC / SendPosIXL / Drive / ConnectionSupervision / Mitigation`
3. `IXL Connect / ReceivePos / Disconnect / Supervision / Mitigation`
4. `TCV`

### 建模形式

模型显式保留位置 `Lv`、保护级 `PL`、列车长度 `l`、连接计数器、最大安全时间等量，并通过概率查询测量 hazard 在给定边界内出现的可能性。

### 关键抽象与取舍

1. 对定位误差采取保守包络近似，而不是精确连续轨迹。
2. 用夸大的不利条件做探索性分析，而不是直接给出最终 `THR` 结论。
3. 通过模块化 hazard 查询替代手工零散 hazard 讨论。

## 验证目标与性质

### 待验证问题

论文围绕 `27` 个 hazard 展开，覆盖：

1. `OCC` 连接和收位超时
2. `OBC` 与 `IXL/OCC` 的错误连接、连接丢失和降级
3. `IXL` 侧接入、断连、路权释放、位置接收与监督
4. `TCV` 占用/空闲状态与真实列车位置不一致

### 查询表达

代表性查询包括：

1. `f3 = Pr(<>[0,bound]([][0,TmaxSafeOCC] ... OCCR.WaitingLoc ...))`
2. `f10 = Pr[<=bound](<> OBCS_0.ConnectionLost && OBCM_0.NormalOperation)`
3. `f23 = Pr[<=bound](<> (IXLS_0.c1 > IXLS_0.TmaxSafe && ... && !IXLS_0.FailSafe))`
4. `f27 = Pr[<=bound](<> IXLM_0.DegradadedMode)`

这些查询把具体 hazard 直接编码成“在给定时间边界内达到某个坏配置的概率”。

## 核心方法与验证流程

1. 先与工业伙伴共同细化运行场景和需求。
2. 再把每个场景拆成更小步骤，并为每步列举可能故障与缓解。
3. 将系统模块化建模到 `UPPAAL SMC`。
4. 把预期行为的反面写成 hazard 查询，测量其出现概率并分析 corner case。

## 案例与结果

论文最重要的结果不是“全部通过”，而是：

1. 在替换 track circuits 的新场景中识别出一批此前未被注意到的 hazard。
2. 即便使用保守位置包络，也依然发现可能威胁安全的 corner case。
3. 通过 `27` 个性质，系统地覆盖了 `OCC/OBC/IXL/TCV` 多个层面的风险。
4. 论文同时公开了模型、参数配置和实验日志，便于复现。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究中的“控制系统状态机建模 + 验证场景生成 + 风险发现”高度一致，尤其适合作为需求早期验证与 hazard 生成范式。

### 可借鉴之处

1. 把 hazard 发现过程系统化为公式生成问题。
2. 用模块化场景模型覆盖不同子系统风险，而不是只做整体黑盒分析。
3. 用 `SMC` 在需求早期快速探索，而不是等到模型完全定型才验证。

### 存在的不足与改进空间

论文只覆盖一个代表性场景，未声称 hazard 集合或场景集合已经完备；真实定位算法也仍被抽象成黑盒。

### 对本研究的启发

它直接证明了“验证不只是在末端检查真假，也可以前移为需求发现工具”，这对博士研究的生成-验证-修复闭环非常重要。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文明确给出模型与实验日志公开仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1007/S00165-021-00556-1)；[预印本 PDF](https://openportal.isti.cnr.it/data/2021/456085/2021_456085.preprint.pdf)；[模型仓库](https://github.com/davidebasile/faoc2020)
- 对后续复用的现实影响：这是当前文库里公开度很高的 tramway/railway hazard 分析案例，适合直接复跑并抽取 hazard 模板。
