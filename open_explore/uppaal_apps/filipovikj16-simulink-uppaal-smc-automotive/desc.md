问题一句话：本文验证的是汽车工业中的 `Simulink` 模型，核心问题是如何把工业级 Brake-by-Wire 与 Adjustable Speed Limiter 子系统转换成可由 `UPPAAL SMC` 直接分析的形式模型。
方法一句话：作者设计了一个保持执行顺序的 `Simulink -> stochastic timed/hybrid automata` 模式化转换，并用 `Dafny` 检查部分块语义编码，再在 `UPPAAL SMC` 中验证两类工业车辆系统。
验证收获一句话：结果表明完整的 `BBW` 与 `ASL-EM` `Simulink` 模型可以在 `UPPAAL SMC` 中完成功能与时序需求分析，但论文也指出仅凭 `Simulink` 语义仍难完整覆盖更强的 extra-functional timing 需求。

## 基本信息

- 标题：Simulink to UPPAAL Statistical Model Checker: Analyzing Automotive Industrial Systems
- 中文标题：从 `Simulink` 到 `UPPAAL` 统计模型检查器的汽车工业系统分析
- 作者：Predrag Filipovikj、Nesredin Mahmud、Raluca Marinescu、Cristina Seceleanu、Oscar Ljungkrantz、Henrik Lonn
- 单位：Mälardalen University；Volvo Group Trucks Technology
- 发表：`FM 2016`，*21st International Symposium on Formal Methods*
- DOI：`10.1007/978-3-319-48989-6_46`
- 链接：[DOI](https://doi.org/10.1007/978-3-319-48989-6_46)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：Volvo 车辆电子系统中的 `Brake-by-Wire (BBW)` 原型和 `ASL Engine Manager`
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文未公开 Volvo 的 `Simulink` 工程或转换后的完整 `UPPAAL SMC` 模型。
- 案例/数据获取方式：案例来自 Volvo Group Trucks Technology 的工业模型；正文给出代表性需求、块数量和转换规模。

## 简报

这篇论文的中心是“如何让 `Simulink` 工业模型进入 `UPPAAL SMC`”，但它不是停在玩具示例上，而是直接拿 Volvo 的 `BBW` 原型和 `ASL` 功能模块做验证。它因此更像一篇方法驱动的应用论文。

- 系统：两个车载系统案例，分别是 `BBW` 制动系统和 `ASL-EM` 车速限制子系统。
- 特点：工业 `Simulink` 大模型、需要保留块执行顺序、既有离散块又有连续块、需求包含功能和时序两类。
- 规模：`BBW` 原模型 `320` 个 blocks，转换后 `174` 个 automata；`ASL` 总模型约 `4845` blocks，本论文分析其中 `ASL-EM` 的 `94` 个 non-virtual blocks。
- 模型：通过模式化转换把 `Simulink` block 编码成 stochastic timed/hybrid automata 网络。
- 性质：制动请求端到端延迟、`ABS` slip-rate 触发逻辑、速度上限选择、最小速度限制等。
- 方法：先 flatten `Simulink` 结构，再按块模式生成 `UPPAAL SMC` 自动机，并用 monitor automaton 跟踪数据传播。
- 结果：`BBW` 的代表性需求得到高概率满足；`ASL-EM` 的功能和时序需求也可分析，但更丰富的时间属性仍受 `Simulink` 原模型信息不足限制。

`工业 Simulink 模型 -> block pattern 转换 -> execution-order preserving automata network -> UPPAAL SMC 监视器查询 -> 功能/时序需求分析`

## 论文定位

这篇论文介于“应用案例”和“工具链方法”之间。若只看主要贡献，它更偏模型转换框架；但它之所以适合放在 `uppaal_apps/`，是因为文中确实把 `UPPAAL SMC` 用到了两个真实汽车系统上，并明确讨论了需求验证结果与工业可用性。

## 验证对象与问题背景

### 系统与场景

论文处理的不是抽象汽车协议，而是 Volvo 的工业 `Simulink` 模型。两个核心对象分别是：

1. `Brake-by-Wire`
   - 制动踏板与轮端执行器之间没有机械连接，依赖电子控制和 `ABS` 逻辑。
2. `ASL Engine Manager`
   - 控制卡车最大速度限制，并处理多个 speed-limit 来源的冲突。

### 系统组成与运行机制

`BBW` 中，踏板位置经传感器读取后转成请求制动力，各轮再根据 slip rate 决定是否真正施加制动力；若 slip rate 超过 `0.2`，应释放制动。

`ASL-EM` 则是更大的 `ASL` 系统中的逻辑组件，负责与动力系统接口，处理不同来源的速度限制请求、启停条件和时序约束。

### 验证边界

论文并没有深入车辆物理动力学，而是把重点放在 `Simulink` 控制逻辑层。特别是 `ASL` 方向，只验证了 `ASL-EM` 子系统，而不是整个 `ASL` 大模型。

### 核心问题

1. 如何保留 `Simulink` block 的 sorted order 执行语义。
2. 如何把连续和离散块统一翻译到 `UPPAAL SMC`。
3. 如何在工业规模模型上验证功能与时间需求，而不是只验证简化 toy example。

## 模型与形式化建模

### 抽象对象

作者把每个 atomic `Simulink` block 形式化为一个带输入、输出、局部变量、sample time 和 block routine 的对象，再按固定模式生成自动机。

### 建模形式

转换目标是带随机语义的 timed/hybrid automata。离散块按 sample time 触发，连续块则用位置上的 delay function 表达。多个自动机通过 broadcast channel 和共享变量通信。

### 关键抽象与取舍

1. 子系统会先被 flatten，只保留计算相关结构。
2. `S-Function` 更多按黑盒对待，不直接验证其内部代码。
3. 为了和 `Simulink` 保持一致，作者优先保留块级执行顺序，而不是追求更激进的抽象压缩。

## 验证目标与性质

### 待验证问题

对 `BBW`，论文至少展示了两类典型需求：

1. `R1BBW`
   - 制动请求从踏板传到轮端执行器的时间不得超过 `200 ms`。
2. `R2BBW`
   - 如果 slip rate 超过 `0.2`，施加制动力必须为 `0`。

对 `ASL-EM`，代表性需求包括：

1. 最低可处理 speed limit 为 `5 km/h`；
2. 多个 speed-limit 来源同时激活时应取最小值；
3. 最大延迟不超过 `20 ms`。

### 性质类型

这些性质覆盖：

1. 功能安全；
2. 有界响应；
3. 端到端时延；
4. 参数选择正确性。

### 查询表达

论文对 `BBW` 给出了明确的概率查询，例如：

1. `Pr[Monitor:x <= 200](<> Monitor:End)`
2. `Pr[Monitor:x <= 200]([] ... Monitor:torque == 0)`

这说明它不是传统符号穷举，而是通过 `UPPAAL SMC` 做统计验证。

## 核心方法与验证流程

1. 读取 `Simulink` 模型并执行 flatten。
2. 对各类 discrete / continuous blocks 采用预定义转换 pattern。
3. 用 `Dafny` 验证部分 block routines 的 `C` 编码与期望行为一致。
4. 生成 `UPPAAL SMC` 自动机网络。
5. 构造 monitor automaton 跟踪从传感器到执行器的数据传播和时钟。
6. 对工业案例运行统计模型检查，评估功能与时序需求是否满足。

## 案例与结果

### `BBW`

`BBW` 原始 `Simulink` 模型共有 `320` 个 blocks，其中 `174` 个是计算块；转换后形成 `174` 个 automata，其中只有 `10` 个是连续时间行为。论文报告了全部功能和时序需求都已分析，示例中：

1. `R1BBW` 的满足概率区间为 `[0.902606, 1]`；
2. `R2BBW` 的满足概率区间为 `[0.900924, 1]`。

### `ASL-EM`

整个 `ASL` 系统约有 `300` 条需求和 `4845` 个 blocks。论文把焦点收缩到 `ASL-EM` 的 `94` 个 non-virtual blocks，并验证了该组件的功能与时序需求。这里的意义在于：工业子系统级大模型已经可以进入 `UPPAAL SMC` 分析流程，而不是停在教科书例子。

### 结果边界

作者也明确承认，更多 extra-functional timing 属性仍然难直接从 `Simulink` 模型中恢复出来，因此该方法对纯功能与部分时序需求最有效。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究的建模与验证链条有很强参考价值，因为它展示了如何把工程建模语言中的控制逻辑系统性迁移到 `UPPAAL` 谱系工具中。

### 可借鉴之处

1. 用 block pattern 而不是逐模型手工翻译，提升自动化程度。
2. 用 monitor automaton 把端到端需求结构化成可验证查询。
3. 明确区分“模型可转”与“需求可证”的边界。

### 存在的不足与改进空间

1. 更偏转换框架，单个应用对象本体展开有限。
2. 对工业黑盒块和 extra-functional timing 的覆盖仍受限。
3. Volvo 工业模型未公开，复现实验难度高。

### 对本研究的启发

如果后续要把需求文本、架构模型或控制图自动送进 `UPPAAL` 验证，这篇论文提供了一个很现实的思路：先围绕“最常见、最稳定”的构件建立模式化映射，而不是一开始就追求所有建模元素全自动覆盖。

## 案例、模型与数据公开情况

- 可获取性判断：🔒 难以取得
- 判断依据：论文中的核心案例来自 Volvo 工业 `Simulink` 模型，正文未公开完整模型、转换结果或查询文件。
- 获取方式/链接：[DOI](https://doi.org/10.1007/978-3-319-48989-6_46)
- 对后续复用的现实影响：很适合复用其 `Simulink -> UPPAAL SMC` 转换思路和 monitor 组织方式，但若要复跑原始工业案例，基本需要重新构造等价模型。
