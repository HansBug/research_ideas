问题一句话：本文验证的是安全关键 `CPS` 的建模与分析框架，核心问题是 `SysML` 模型能否被系统化翻译成 `UPPAAL SMC` 可验证的 priced timed automata。
方法一句话：作者先限定一组 `SysML` 构件，再引入 `Enhanced Activity Calculus (EAC)` 作为中间代数，最后把模型转换为 `UPPAAL SMC` 输入，并在 artificial pancreas 案例上验证安全性质。
验证收获一句话：在 single-hormone artificial pancreas 案例中，论文不仅证明转换机制是 sound 的，还用 `10` 个虚拟患者、`24h` 仿真和 `Pr[t<=1440]...>=0.99` 查询比较了多种消息错误缓解策略对安全性的影响。

## 基本信息

- 标题：A framework for modeling and analyzing cyber-physical systems using statistical model checking
- 中文标题：使用统计模型检查对 cyber-physical systems 进行建模与分析的框架
- 作者：Abdel-Latif Alshalalfah、Otmane Ait Mohamed、Samir Ouchani
- 单位：Concordia University；CESI Lineact
- 发表：Internet of Things，2023
- DOI：`10.1016/j.iot.2023.100732`
- 链接：[DOI](https://doi.org/10.1016/j.iot.2023.100732)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🏥 医疗与健康
- 被验证系统：artificial pancreas 医疗 `CPS` 及其 `SysML -> PTA -> UPPAAL SMC` 分析链
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文公开 `HAL` 版本，但未给出完整模型仓库；正文详细给出了 `SysML`、`EAC` 和 PTA 结构。
- 案例/数据获取方式：案例是 single-hormone artificial pancreas，使用 `10` 个虚拟患者与随机餐食场景；患者数据来源在正文中给出。

## 简报

这篇论文虽然方法色彩很强，但不是空框架。它明确把 artificial pancreas 拉进了完整工作流里，从 `SysML` 图形模型一路落到 `UPPAAL SMC` 查询。

- 系统：sensor、controller、wireless channel、actuator 和 glucose-insulin dynamics 组成的 artificial pancreas。
- 特点：连续/离散混合、无线消息错误、医疗安全关键、`SysML` 到 `UPPAAL SMC` 的系统化翻译。
- 规模：`10` 个虚拟患者、`24h` 分析窗口，比较多种 message error 缓解配置。
- 模型：`SysML` -> `EAC` -> priced timed automata -> `UPPAAL SMC`。
- 性质：血糖安全区间、长时高血糖暴露和消息错误下的控制稳定性。
- 方法：先证明翻译 soundness，再在人工胰腺上运行统计安全查询。
- 结果：对不同控制配置，论文量化了 message errors 对两类安全性质 `SA/SB` 的影响。

`SysML / ODE-SCD -> EAC -> priced timed automata -> UPPAAL SMC 查询 -> artificial pancreas 安全比较`

## 论文定位

这是一篇偏方法驱动、但案例边界足够清楚的 `🎛️ + 🏥` 条目。它不能算纯技术论文，因为 artificial pancreas 是完整的真实医疗 `CPS` 用例，而且安全性质和实验结果都写得很具体。

## 验证对象与问题背景

### 系统与场景

案例是用于糖尿病治疗的 artificial pancreas。系统通过传感器测量血糖，经无线链路传给控制器，再由 actuator 驱动胰岛素注入。

### 系统组成与运行机制

论文明确给出了：

1. sensor PTA
   - 周期性采样血糖值。
2. lossy wireless channel PTA
   - 注入消息丢失/错误。
3. controller PTA
   - 使用标准 `PID` 计算 insulin infusion rate。
4. actuator PTA
   - 应用控制指令。
5. glucose-insulin dynamics PTA
   - 表示患者体内动力学。

### 验证边界

本文验证的是**系统级医疗控制闭环与翻译链**，不是完整商业人工胰腺硬件/软件产品认证。

### 核心问题

直接对真实 `CPS` 做穷举验证很难扩展，而仅靠仿真又缺乏状态空间覆盖保证，因此作者把重点放在“建模语言到 `UPPAAL SMC` 的可保持语义转换”。

## 模型与形式化建模

论文的形式化链条是：

1. 用一组受限 `SysML` construct 捕捉离散与连续行为；
2. 引入 `EAC` 作为中间代数；
3. 通过系统化规则把 `EAC` 转成 priced timed automata；
4. 在 `UPPAAL SMC` 中运行查询。

这使得 `sensor/controller/actuator/plant` 都能进入同一验证语义空间。

## 验证目标与性质

### 待验证问题

1. artificial pancreas 是否能把血糖维持在安全区间；
2. 长时高血糖暴露是否受控；
3. message errors 出现时哪种缓解策略更安全。

### 性质类型

- 统计安全性质
- 鲁棒性分析
- 模型转换正确性支撑下的系统验证

### 查询表达

文中给出了两条代表性查询：

1. `Pr[t<=1440] ( [] G >=50 && G <=300 ) >= 0.99`
2. `Pr[t<=1440] ( [] tg180<=150 ) >= 0.99`

第一条要求血糖始终保持在 `50-300` 范围；第二条限制高血糖持续时间变量 `tg180`。

## 核心方法与验证流程

1. 用 `SysML` 描述 sensor、controller、actuator 和动力学模型。
2. 把模型系统化改写到 `EAC`。
3. 生成 priced timed automata。
4. 在 `UPPAAL SMC` 中运行安全查询。
5. 对 `sustain / suspend / revert` 等配置在 message errors 下做对比。

## 案例与结果

论文在 `10` 个虚拟患者、`24h` 场景下比较了不同配置：

1. 无 message errors 时，各配置都退化为标准 `PID` 控制。
2. 有 message errors 时，`SA` 和 `SB` 两类性质对配置非常敏感。
3. 论文指出 `suspend` 对 `SA` 的保持更强，但 `SB` 上可能更差；`sustain` 和 `revert` 在部分高血糖恢复场景中更稳。

这使它不只是“能不能验证”，而是“验证之后能指导控制配置选择”。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究很重要，因为它展示了如何让上游建模语言、系统化翻译和验证结果形成闭环，而不是只靠人工从 PDF 翻模型。

### 可借鉴之处

1. 先定义受限建模子集，再谈自动翻译。
2. 用中间代数控制语义保持。
3. 把 message error 这类运行时异常直接纳入验证配置对比。

### 存在的不足与改进空间

论文仍偏方法型，且未开放完整工程，因此复现门槛不低。

### 对本研究的启发

它说明若博士研究未来要把 `UML/SysML` 或需求模型自动转成验证模型，中间语义层几乎是不可绕开的。

## 重要的相关工作

### 1. `SysML` 到形式模型转换

- 本文的核心就是为这条路线补足可执行中间层。

### 2. `UPPAAL SMC` 医疗 `CPS` 验证

- artificial pancreas 为统计安全分析提供了很强的示范案例。

### 3. message error 缓解策略比较

- 论文把验证结果直接用于比较控制策略，而不是只做布尔性质判断。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文和 `HAL` 版本公开，但未见完整 `SysML`、`EAC` 和 `UPPAAL SMC` 模型仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1016/j.iot.2023.100732)；[HAL 页面](https://hal.science/hal-04108550)
- 对后续复用的现实影响：适合作为“上游建模语言到 `UPPAAL SMC`”的代表样本，且人工胰腺安全查询很有参考价值；但若要直接复跑，需要自行重建完整模型链。
