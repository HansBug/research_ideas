问题一句话：本文验证的是电子显微镜中的相机保护软件，核心问题是怎样把 ASD 已验证的组件接口设计进一步放进 `UPPAAL`，补足端到端安全性质与全局错误轨迹检查。
方法一句话：作者把 ASD 状态机翻译为 `UPPAAL` 自动机，再通过时序逻辑性质与 observer 自动机检查 `Dose Protector`、`BlankerShutter` 和 `SafetyList` 之间的全局安全关系。
验证收获一句话：论文在 FEI 相机保护案例上发现了 ASD 单独无法发现的两个主要问题，并指出 observer 方式更适合工业用户理解和落地。

## 基本信息

- 标题：Complementary verification of embedded software using ASD and Uppaal
- 中文标题：结合 ASD 与 Uppaal 的嵌入式软件互补验证
- 作者：Richard Doornbos、Jozef Hooman、Bernard van Vlimmeren
- 单位：Embedded Systems Institute；Radboud University Nijmegen；FEI Company
- 发表：IIT 2012
- DOI：`10.1109/INNOVATIONS.2012.6207775`
- 链接：[DOI](https://doi.org/10.1109/INNOVATIONS.2012.6207775)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🏭 工业与基础设施
- 被验证系统：FEI 电子显微镜中的 camera protection system
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文未提供公开仓库；模型来源于工业 ASD 设计与作者手工翻译。
- 案例/数据获取方式：案例来自 FEI 公司相机保护系统，原始工业资产未公开。

## 简报

本文的价值在于证明“接口级形式验证并不够”。FEI 已经用 ASD 验过组件接口一致性，但作者进一步把关键组件送进 `UPPAAL` 后，还是发现了两个 ASD 标准检查发现不了的问题。

- 系统：电子显微镜中的相机保护系统关键子集。
- 特点：`ASD` 组件模型 + `UPPAAL` 全局闭系统验证、端到端安全性质、observer 风格检查。
- 规模：核心围绕 `DoseProtector`、`BlankerShutter`、`SafetyList` 及其子状态机 `HandleChanges`。
- 模型：由 ASD 接口/设计模型翻译而来，非法调用通过 deadlock 暴露。
- 性质：安全曝光状态、blanker 错误状态、错误轨迹观察。
- 方法：先写时序逻辑性质，再引入 observer 自动机对坏轨迹进行模式检测。
- 结果：发现 `2` 个重大问题；其中一个性质通过 `20` 步诊断轨迹暴露，observer 方法被认为更适合工业使用。

`ASD 接口/设计状态机 -> 翻译到 UPPAAL -> 全局安全性质/observer -> 诊断轨迹 -> 回写设计修正`

## 论文定位

这是一篇很典型的 `🎛️ + 🏭` 工业控制应用论文。虽然包含一点工具整合方法，但核心贡献是通过真实工业系统说明 `UPPAAL` 如何补足已有工业形式方法的盲区。

## 验证对象与问题背景

### 系统与场景

对象是 FEI 电子显微镜中的相机保护系统。其目标是在任何时刻都防止昂贵且敏感的相机受到过高电子束剂量。

### 系统组成与运行机制

论文聚焦的关键软件组件包括：

1. `DoseProtector`
2. `BlankerShutter`
3. `SafetyList`

其中 `SafetyList` 负责判断当前束流是否安全；若不安全，`BlankerShutter` 必须及时 blank 电子束；`DoseProtector` 对外提供控制接口。

### 验证边界

论文验证的是软件控制逻辑及其组件交互，并不建模完整显微镜硬件物理过程。

### 核心问题

ASD 擅长组件接口一致性和代码生成，但只检查固定性质。作者要验证的是更高层的“全局安全状态是否真的意味着束流安全且 blanker 不出错”。

## 模型与形式化建模

### 抽象对象

ASD 中的接口模型和设计模型都被翻译为 `UPPAAL` 自动机。`Illegal` 调用不会被显式翻译，而是让模型在对应位置 deadlock，以便交给 `UPPAAL` 检出。

### 建模形式

模型是闭系统的 automata network。为了观测特定坏轨迹，作者还引入了并行 observer 自动机。

### 关键抽象与取舍

1. ASD 负责单组件接口符合性。
2. `UPPAAL` 负责多组件闭系统性质。
3. observer 所需通道被声明为 broadcast，以便额外自动机旁路观察。

## 验证目标与性质

### 待验证问题

1. `DoseProtector.SafeExposure` 是否必然意味着 beam intensity 安全。
2. 安全状态下 `BlankerShutter` 是否也必然不处于错误状态。
3. 某些不允许的交互序列是否可能发生。

### 查询表达

文中给出了代表性查询：

1. `A[] DoseProtector.SafeExposure imply (safe==1)`
2. `A[] DoseProtector.SafeExposure imply (safe==1 and !BlankerShutter.Error)`
3. `A[] not Observer.Error`

### 性质分组与实际含义

1. 局部安全：安全曝光状态应对应安全束流。
2. 端到端安全：安全曝光状态还应排除 blanker 错误。
3. 坏轨迹监视：指定错误交互一旦出现，observer 进入 `Error`。

## 核心方法与验证流程

1. 从 ASD 选出相机保护系统的关键组件子集。
2. 把 ASD 状态机翻译成 `UPPAAL` 自动机。
3. 先用时序逻辑直接检查关键安全性质。
4. 再用 observer 自动机检测工业上更容易理解的坏轨迹模式。
5. 利用诊断轨迹与仿真定位问题原因。

## 案例与结果

### 案例规模

论文没有给出统一状态空间规模数字，但围绕 `DoseProtector`、`BlankerShutter`、`SafetyList` 和 `HandleChanges` 等关键组件建立了一个可检查闭系统。

### 关键结果

1. 作者在验证过程中发现了 `2` 个重大问题。
2. 查询 `A[] DoseProtector.SafeExposure imply (safe==1)` 成立。
3. 但更强的查询 `A[] DoseProtector.SafeExposure imply (safe==1 and !BlankerShutter.Error)` 不成立。
4. 一个违例通过 `20` 步诊断轨迹暴露出来。
5. 论文最终认为 observer 自动机比直接书写时序逻辑更易被工业用户理解。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究中的“生成-验证-修复”闭环高度契合，因为它展示了已有建模成果进入更强验证器后，如何找到先前没发现的问题。

### 可借鉴之处

1. 现有模型/接口工具与 `UPPAAL` 可以是互补关系，而不是替代关系。
2. observer 很适合把工程坏模式编码成可验证对象。
3. 诊断轨迹可以直接服务设计修正。

### 存在的不足与改进空间

案例强依赖工业资产，公开工件缺失；同时论文只给出了少量性质示例，没有形成大规模性质库。

### 对本研究的启发

如果 LLM 前端生成的是偏接口或局部状态机，后端完全可以再接一个更全局的验证层，这样更容易发现跨组件语义错误。

## 案例、模型与数据公开情况

- 可获取性判断：🔒 难以取得
- 判断依据：论文公开，但 FEI 相机保护系统模型、ASD 工程和翻译后的完整 `UPPAAL` 模型都属于工业内部资产。
- 获取方式/链接：[DOI](https://doi.org/10.1109/INNOVATIONS.2012.6207775)；[PDF](https://sws.cs.ru.nl/publications/papers/hooman/ITT2012.pdf)
- 对后续复用的现实影响：适合作为“互补验证”思路样例，但难以直接复跑工业模型。
