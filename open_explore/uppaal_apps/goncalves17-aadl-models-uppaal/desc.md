问题一句话：本文验证的是无人机感知与执行子系统的架构模型，核心问题是如何把 AADL 架构、错误属性和线程行为自动映射成 `UPPAAL` 模型并系统化检查 deadline、安全、活性与故障概率。
方法一句话：作者提出 `ECPS Verifier`，把 AADL 基础模型、Error Annex 和 Behavior Annex 细化后自动转换为 timed automata，并用 `UPPAAL/UPPAAL-SMC` 检查离散和概率性质。
验证收获一句话：论文在 UAV 案例上分析了 `42` 条性质，显示系统总体满足需求，并给出了执行器进入错误状态的概率估计区间。

## 基本信息

- 标题：Formal Verification of AADL Models Using UPPAAL
- 中文标题：使用 `UPPAAL` 的 AADL 模型形式验证
- 作者：Fernando Silvano Gonçalves、David Pereira、Eduardo Tovar、Leandro Buss Becker
- 单位：UFSC（Federal University of Santa Catarina）；CISTER/INESC-TEC，ISEP/IPP
- 发表：SBESC 2017
- DOI：`10.1109/SBESC.2017.22`
- 链接：[DOI](https://doi.org/10.1109/SBESC.2017.22)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：UAV 的 sensing and actuation 子系统及其 AADL 架构模型
- UPPAAL线：`UPPAAL` + `UPPAAL SMC`
- 代码/模型/仓库获取方式：论文描述了 `ECPS Verifier` 工具与转换流程，但未给出稳定公开仓库。
- 案例/数据获取方式：案例基于 ProVant UAV 的 AADL 设计模型和设备故障树，需要按论文中的 AADL 片段与规则重建。

## 简报

这篇论文的核心价值在于把“架构描述语言 -> timed automata -> 查询集合”真正串起来。作者不是手工从 UAV 案例重写一套 `UPPAAL` 模型，而是先补齐 AADL 中的错误属性与行为属性，再自动生成模型。

- 系统：UAV 的 sensing/actuation 子系统，含 GPS、Sonar、IMU、ESC、Servo 等设备。
- 特点：AADL + Error Annex + Behavior Annex、自动模型转换、离散/概率性质混合分析。
- 规模：涉及多个设备线程与执行器模型；总计验证 `42` 条性质。
- 模型：线程、调度器、设备故障与行为属性被映射为 `UPPAAL` templates。
- 性质：deadline、安全、活性、deadlock freeness、执行器错误概率。
- 方法：先在 AADL 中补 fault tree、错误状态和行为属性，再用 `ECPS Verifier` 转换成 `UPPAAL`。
- 结果：系统整体满足需求；其中 `Actuator(0)` 进入 `EmergencyMode` 的概率区间为 `[0.107051, 0.206887]`（置信度 `0.95`）。

`AADL 架构 + EA/BA 细化 -> ECPS Verifier -> timed automata + 查询 -> deadline/安全/概率结果`

## 论文定位

本文是非常贴近博士研究主线的应用论文，因为它把架构建模、形式验证和应用案例连在了一起。尽管它包含方法成分，但最终落点仍然是一个明确的 UAV 子系统案例。

## 验证对象与问题背景

### 系统与场景

对象是无人机的 sensing and actuation subsystems。它们负责感知位姿/环境信息，并把控制参考发送给执行器。

### 系统组成与运行机制

论文给出了：

1. 顶层 `UAV.impl`，集成 control system 与 sensing/actuation process。
2. `pi_est_act` 过程，其中包含 `ti_sensing`、`ti_positionEst`、`ti_signalTransformation` 等线程。
3. 设备层包括 `GPS`、`Sonar`、`IMU`、左右 `ESC` 与左右 `Servo`。

作者还为设备设计 fault-tree，并将逻辑错误状态通过 AADL Error Annex 引入模型。

### 验证边界

论文验证的是架构级线程行为、设备错误传播和时序约束，不覆盖完整连续控制律或飞行动力学。

### 核心问题

1. AADL 本身不足以直接做自动形式验证。
2. UAV 设计必须同时考虑线程 deadline、设备故障和执行器错误概率。
3. 设计团队通常很难手工写出完整 timed automata，因此需要自动转换。

## 模型与形式化建模

### 抽象对象

作者把 AADL 中的系统、过程、线程、设备、错误行为和线程行为属性映射为 `UPPAAL` 模板、变量、通道和时钟。

### 建模形式

1. 离散性质由标准 `UPPAAL` 检查。
2. 概率性质由 `UPPAAL-SMC` 检查。
3. 设备错误状态被建成显式 automata，例如 GPS 的 `partialOperation`、`emergencyMode`、`irreversibleFailure`。

### 关键抽象与取舍

1. 需要在 AADL 模型中遵循若干设计约定，才能保证转换成功。
2. 线程行为必须用 Behavior Annex 明确状态、守卫、时钟和过渡。
3. 论文目前只支持单文件 AADL 输入。

## 验证目标与性质

### 待验证问题

1. 所有任务是否至少能运行一次并回到 `Idle`。
2. 任务是否始终受调度器控制。
3. 任务运行时是否仍小于 deadline。
4. 系统 deadlock 是否只会在错误状态出现。
5. 执行器进入错误状态的概率是多少。

### 查询表达

文中代表性查询包括：

1. `E<>(T1.Idle and ... and Tk.Idle)`
2. `A[] not(...)`
3. `A[] deadlock imply (T1.Error or ... or Ti.Error)`
4. `Pr[<=12000](<> Actuator(i).EmergencyMode)`

### 性质分组与实际含义

1. 活性：线程最终能运行并回到空闲。
2. 安全：任务执行必须受调度器管控。
3. 时序：任务执行时间不能超过 deadline。
4. 故障概率：执行器在一个周期窗口内进入异常模式的概率。

## 核心方法与验证流程

1. 设计 UAV 的基础 AADL 架构模型。
2. 为设备补 fault tree，并通过 Error Annex 注入错误行为。
3. 通过 Behavior Annex 补齐线程状态、变量、守卫与时钟。
4. 使用 `ECPS Verifier` 生成 `UPPAAL` timed automata。
5. 编写 TCTL/SMC 查询，检查离散与概率性质。

## 案例与结果

### 案例规模

1. UAV 含多个传感器与执行器设备。
2. 重点验证 sensing/actuation process。
3. 总计评估 `42` 条性质。

### 关键结果

1. `42` 条性质覆盖 reachability、safety、liveness 和 deadlock freeness。
2. 其中一半是错误状态相关概率性质，置信度为 `95%`。
3. 其余一般性质中，`52.38%` 被完全满足，`47.62%` 为“可能满足”。
4. 对 `Actuator(0)`（`ESC right`）而言，进入 `EmergencyMode` 的概率在 `[0.107051,0.206887]`。
5. 作者总结认为 UAV 模型整体满足需求：线程满足 deadline，安全性质成立，除错误状态外不存在 deadlock。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究中的“从非形式化/半形式化架构到可验证模型”的问题几乎正面重合。

### 可借鉴之处

1. 先补行为和错误 annex，再做自动转换。
2. 在统一模型上同时运行布尔和概率查询。
3. 用架构级建模直接承接安全关键系统设计流程。

### 存在的不足与改进空间

`ECPS Verifier` 当前没有稳定公开入口；性质编写仍要求用户直接掌握 `UPPAAL` 语法，这在工程上门槛较高。

### 对本研究的启发

它说明把架构语言中的约束、错误模式和行为 annex 统一送进形式验证，是一条很适合 LLM + 形式方法融合的路线。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文可公开获取，但 `ECPS Verifier` 和完整 UAV `UPPAAL` 工程未见稳定公开仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1109/SBESC.2017.22)；[PDF](https://cister-labs.pt/docs/formal_verification_of_aadl_models_using_uppaal/1331/attach.pdf)
- 对后续复用的现实影响：非常适合作为架构到验证模型的参考样本，但复现仍需按论文手动补足转换与查询。
