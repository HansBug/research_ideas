问题一句话：本文验证的是工业驱动模块的功能安全架构，核心问题是当危险故障随机出现时，诊断模块能否既满足 `STO` 安全时序要求，又把 `SFF` 提升到 `90%` 安全阈值以上。
方法一句话：作者先把 Danfoss `BDM` 的双通道 `STO` 架构建成 timed automata，用 `UPPAAL` 验证功能与安全性质，再借助 `UPPAAL Stratego` 的 `Q-learning` 优化诊断模块的故障检测行为。
验证收获一句话：论文显示 `12` 条核心功能/安全查询中，功能与时序要求均成立；未经优化时系统仅检测 `185` 个故障并漏掉 `196` 个，`SFF=48.5%`，而学习后可检测 `290` 个、漏掉 `29` 个，把 `SFF` 提升到 `90.9%`。

## 基本信息

- 标题：Formal Verification and Fault Detection Optimization of Industrial Drive Systems
- 中文标题：工业驱动系统的形式化验证与故障检测优化
- 作者：Imran Riaz Hasrat、Eun-Young Kang、Christian Uldal Graulund
- 单位：University of Southern Denmark；Danfoss Drives A/S
- 发表：2025 9th International Conference on System Reliability and Safety (ICSRS)，2025
- DOI：`10.1109/ICSRS68021.2025.11422059`
- 链接：[DOI](https://doi.org/10.1109/ICSRS68021.2025.11422059)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🏭 工业与基础设施
- 被验证系统：Danfoss 工业 `Basic Drive Module (BDM)` 的功能安全与故障诊断架构
- UPPAAL线：`UPPAAL Stratego`
- 代码/模型/仓库获取方式：论文参考文献直接给出公开仓库 `BDM_safety_optimization`。
- 案例/数据获取方式：案例来自真实 `BDM` 架构，论文与仓库共同提供模型与优化材料。

## 简报

这篇论文的特点是把“先证正确，再做优化”落到了工业功能安全场景上。作者没有直接让学习器在一个可能错误的模型上乱搜，而是先用 `UPPAAL` 确认 `BDM` 安全逻辑和时序成立，再让 `Stratego` 去提升诊断覆盖率。

- 系统：带 `iSM3` 安全模块的工业 `BDM`，实现 `SIL3` 级 `STO`。
- 特点：双冗余 `STO` 通道、诊断块持续监测、要求 `SFF >= 90%`。
- 规模：两条 `STO` 通道，各含 pulse generator、signal levelling and processing、switch、power processing；另有 diagnostic block 和 motor。
- 模型：各功能块对应 timed automata，并显式包含故障检测与停机时序。
- 性质：功能联动、危险状态不可达、`28 ms/30 ms` 时序要求、`SFF` 优化。
- 方法：先 `UPPAAL` 验证，再 `Stratego` 合成诊断优化策略。
- 结果：形式化性质通过；`SFF` 从 `48.5%` 提升到 `90.9%`。

`BDM 架构建模 -> 功能/安全查询验证 -> 构造 SFF fitness -> Stratego 学习诊断策略 -> 对比优化前后检测覆盖率`

## 论文定位

本文属于 `🎛️ + 🏭`。它验证的是工业驱动模块内部的安全执行逻辑和诊断机制，明显是控制器/设备控制主轴上的工业功能安全案例。与此同时，它又典型体现了 `UPPAAL -> UPPAAL Stratego` 的“验证后优化”工作流。

## 验证对象与问题背景

### 系统与场景

被验证对象是 Danfoss 的工业 `Basic Drive Module (BDM)`。该模块位于电机与电源之间，需要保证危险故障发生时电机能安全停止。

### 系统组成与运行机制

系统包括：

1. 两条独立 `STO` 通道 `A/B`；
2. 每条通道上的 pulse generator、signal levelling and processing、switch、power processing；
3. 独立 diagnostic block，负责监测和触发停机；
4. motor 和 user interface。

`STO` 激活后会切断相关供电，使 motor 进入安全关闭状态。

### 验证边界

论文验证的是**`BDM` 功能安全架构及其故障检测逻辑**，不是完整工厂产线。

### 核心问题

1. 危险故障出现具有随机性。
2. 仅有功能正确还不够，诊断效率过低同样会破坏安全指标。
3. `SFF` 是工业功能安全里的关键指标，目标阈值为 `90%`。

### 研究动机

作者希望展示：在工业驱动安全场景中，形式化验证与强化学习不是对立的，而是可以组成“正确模型 + 优化策略”的联合框架。

## 模型与形式化建模

### 结构映射

论文采用“一个功能块对应一个 timed automaton”的方式，把 `BDM` 架构逐块映射进 `UPPAAL Stratego`。

### 行为建模

模型显式保留：

1. `STO` 通道供电与断电；
2. switch 开闭与 power processing 联动；
3. motor 开/关状态；
4. diagnostic block 对故障的检测或漏检；
5. 启停时序约束。

### `SFF` 指标建模

作者把 `SFF` 写成：

$$
SFF = \frac{\lambda_{DD}}{\lambda_{DD} + \lambda_{DU}}
$$

其中关注检测到的危险故障 `\lambda_{DD}` 与未检测危险故障 `\lambda_{DU}` 的相对比例。

## 验证目标与性质

### 待验证问题

1. 开关与功率处理块之间的功能联动是否正确；
2. `STO` 激活时是否不存在不该出现的危险状态；
3. 电机关闭和 `STO` 激活是否满足给定毫秒级时序；
4. 诊断块能否通过学习把 `SFF` 提升到目标阈值。

### 性质类型

1. 活性；
2. 安全不可达；
3. 有界响应/截止时间；
4. 定量优化。

### 性质分组与实际含义

原文表 1 的 `12` 条查询可归纳为：

- `Q1-Q5`：开关、功率块与电机之间的核心功能联动；
- `Q6-Q10`：`STO` 激活后危险状态不应出现；
- `Q11-Q12`：时序预算要求，即 motor 关断与 `STO` 激活必须落在 `28 ms/30 ms` 预算内。

### 查询表达

论文直接使用 `A[]`、`E<>` 等 `CTL` 风格查询。例如：

1. `A[]((DiagnosticBlock.Stopping and m_status == 1 and z > 10 and z <= 28) imply Motor.Off)`
2. `A[]((Motor.Off and m_status == 0 and z > 10 and z <= 30) imply Initializer.STO)`

### 判定边界与前提

形式化验证阶段通过加全局时钟 guard 限制状态空间；而 `SFF` 优化阶段再移除该 deadlock cut-off，以便进行长时间学习。

## 核心方法与验证流程

1. 将 `BDM` 架构逐块映射成 timed automata。
2. 用 `UPPAAL` 验证功能、安全和时序性质，确认模型作为优化基线是正确的。
3. 定义 `SFF` fitness 函数，最小化当前 `SFF` 与目标 `90%` 之间的差距。
4. 用 `UPPAAL Stratego` 在 `10000` 分钟窗口内学习诊断策略。
5. 对比优化前后的 detected/undetected fault 数量。

这个流程清晰体现了“形式化验证先行，强化学习后置”的工业安全实践逻辑。

## 案例与结果

### 形式化验证结果

表 1 显示：

1. 功能联动查询均为 `Valid`；
2. `STO` 激活时，不应同时出现的危险状态查询均未发现违例；
3. `28 ms` 和 `30 ms` 的时序要求满足。

### `SFF` 优化结果

优化前：

1. detected faults：`185`
2. undetected faults：`196`
3. `SFF = 48.5%`

优化后：

1. detected faults：`290`
2. undetected faults：`29`
3. `SFF = 90.9%`

### 结果解释

论文最有说服力的地方是，它没有把学习效果写成抽象“性能提升”，而是直接落到工业安全指标 `SFF` 上，并且达到了设计要求的 `>= 90%` 阈值。

## 与本研究的关系

### 相关性分析

这篇论文非常贴近博士研究中的“生成-验证-修复/优化”闭环，因为它明确区分了正确性保证和后续改进阶段。

### 可借鉴之处

1. 先验证模型正确，再允许学习器介入。
2. 把工业安全指标直接编码成优化目标。
3. 用一组清晰的功能/安全/时序性质作为优化前基线。

### 存在的不足与改进空间

1. 真实工业细节仍做了抽象。
2. 大状态空间仍需要人为切割后再验证。
3. 当前只优化 `SFF`，未同时优化能耗与成本。

### 对本研究的启发

它提示本研究在迭代式模型修复方向上，可以把“先修到正确，再朝更优指标推进”作为稳定流程，而不是把正确性和优化同时交给一个黑盒过程。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文参考文献明确给出 `GitHub` 仓库，当前仓库可访问。
- 获取方式/链接：[DOI](https://doi.org/10.1109/ICSRS68021.2025.11422059)；[GitHub 仓库](https://github.com/ImranRiazAAU/BDM_safety_optimization)
- 对后续复用的现实影响：这是当前文库里公开度较高的工业功能安全 `Stratego` 案例，适合直接参考“先验证、后优化”的建模与实验组织方式。
