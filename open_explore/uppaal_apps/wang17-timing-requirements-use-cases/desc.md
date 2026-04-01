问题一句话：本文验证的是汽车嵌入式软件的 timing requirements 测试流程，核心问题是在只额外提供部分 timed automata、而不重建完整功能模型的情况下，能否自动生成足够有效的可执行时序测试用例。
方法一句话：作者提出 `TAUC`，把 `RUCM` use case 规格、`UMTG` 生成的功能场景和人工编写的 timing automata 结合起来，再借助 `UPPAAL` 生成 timeliness scenarios，并用多样性搜索扩展成更有效的测试集。
验证收获一句话：在工业汽车案例 `BodySense` 上，`TAUC` 用 `122` 个测试用例就达到了约 `91%` 的变异体故障检出率，明显高于随机测试的约 `40%` 和人工测试的约 `60%`，说明 `UPPAAL` 支撑的时序测试生成对真实嵌入式软件很有价值。

## 基本信息

- 标题：System Testing of Timing Requirements based on Use Cases and Timed Automata
- 中文标题：基于用例与 timed automata 的时序需求系统测试
- 作者：Chunhui Wang、Fabrizio Pastore、Lionel Briand
- 单位：SNT - University of Luxembourg
- 发表：2017 IEEE International Conference on Software Testing, Verification and Validation (ICST)
- DOI：`10.1109/ICST.2017.34`
- 链接：[DOI](https://doi.org/10.1109/ICST.2017.34)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：汽车嵌入式软件 `BodySense` 的 timing requirements 测试模型
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：`TAUC` 原型页面当前可访问，但原文未公开 `BodySense` 的用例、timed automata、mapping tables 和完整测试资产。
- 案例/数据获取方式：论文给出 `BodySense` 的 use case、约束、timed automata 数量和实验设置，可据此重建部分流程。

## 简报

这是一篇明显偏测试的边界条目，但它并不是泛泛谈“模型驱动测试”，而是把 `UPPAAL` 直接嵌入到工业汽车软件 timing requirements 的测试生成流程中。

- 系统：`BodySense` 汽车座椅乘员识别与自诊断软件。
- 特点：功能规格来自 use case，时序规格来自少量人工编写的 timed automata，不要求完整系统模型。
- 规模：`25` 个 timed automata，其中 `3` 个环境自动机、`22` 个 requirement automata；真实测试预算 `122` 个用例；实验含 `323` 个变异体。
- 模型：`RUCM` 用例 + `UMTG` 功能场景 + `UPPAAL` timeliness test model。
- 性质：温度错误检测/确认等时序需求、边覆盖、故障检出能力。
- 方法：先由 `UPPAAL` 生成覆盖边的 timeliness scenarios，再用多样性搜索挑选更强测试集。
- 结果：`TAUC` 的故障覆盖率约 `91%`，显著高于随机和人工测试。

`用例规格 + timing automata -> timeliness test model -> UPPAAL 生成场景 -> 多样性优化 -> 可执行测试用例`

## 论文定位

本文属于本 collection 中的边界型 `🧩 + 🚦` 条目。它主线更偏“基于 `UPPAAL` 的工业软件时序测试”，不是经典意义上的对象验证论文，因此需要在使用时明确它更偏 testing than proof。

## 验证对象与问题背景

### 系统与场景

对象是 `BodySense`，一个由工业合作方 IEE 开发的汽车嵌入式系统。系统要根据座椅传感器、温度传感器等输入识别乘员状态，并把结果发送给 AirbagControlUnit。

### 系统组成与运行机制

论文展示了两个关键 use cases：

1. `Identify the Occupancy Status of a Seat`
   - 负责识别座椅占用状态。
2. `Self Diagnosis`
   - 负责读取温度并在必要时设置 `TemperatureError`。

它们共同决定了时序需求，例如温度超范围后错误何时被检测、何时被确认等。

### 验证边界

论文验证的是**时序需求测试模型与测试生成流程**，不是直接证明 `BodySense` 实现本身在所有状态下都正确。

### 核心问题

1. 传统 timed automata 测试生成通常需要完整功能模型，现实中代价太高。
2. 若只建 timing automata，则往往只能得到抽象测试用例，难以直接执行。
3. 工业测试预算固定，测试集必须足够“强”。

### 研究动机

作者希望在不大幅增加建模负担的前提下，让 use case 规格与 `UPPAAL` 协同支持可执行的 timing requirements 测试。

## 模型与形式化建模

### 抽象对象

模型不是直接从实现代码抽出来的，而是由三部分组合：

1. `RUCM` use case 规格；
2. `UMTG` 生成的功能场景；
3. 人工编写的 timing requirements automata。

### 建模形式

`TAUC` 将上述信息合成为 timeliness test model，再送入 `UPPAAL` 生成 timeliness scenarios。

### 关键状态与元素

1. 用例步骤与 `OCL` 约束；
2. scenario automata；
3. environment automata；
4. augmented timing requirements automata；
5. mapping tables
   - 将抽象测试步骤翻译为可执行总线消息或接口调用。

### 关键抽象与取舍

1. 不要求完整功能逻辑 timed automata。
2. 只要求额外描述 timing requirements 和关键环境属性。
3. 通过用例而不是代码语义来恢复“达到某状态需要哪些输入”。

## 验证目标与性质

### 待验证问题

论文真正关心的是：

1. 是否能自动生成可执行 timing test cases。
2. 测试集对 timing faults 的检出率如何。
3. 多样性优化是否能提升 fault coverage。

### 性质类型

1. 时序需求测试覆盖性质。
2. 变异体故障检出性质。
3. 部分 observable-oracle 检查。

### 性质分组与实际含义

- edge coverage：每条关键时序边都要被测试到。
- timeliness scenarios：不同输入序列是否会触发不同 timing behavior。
- fault detection：实现如果延迟错误确认或卡在错误状态，测试能否抓到。

### 查询表达

`UPPAAL` 主要用于生成 shortest trace 以满足边覆盖，然后 `TAUC` 再对场景做多样性增强。论文里的查询目标不是传统安全公式，而是测试目的驱动的 reachability。

### 判定边界与前提

测试依赖可观察变量作为 oracle；若故障只表现为“内部状态错了但外部值还对”，则并非所有变异都能被直接检出。

## 核心方法与验证流程

1. 编写 `RUCM` use cases 和 `OCL` 约束。
2. 用 `UMTG` 提取功能场景。
3. 手工建 timing requirement automata。
4. `TAUC` 自动识别功能场景与 timing automata 的依赖。
5. 组合成 timeliness test model 并交给 `UPPAAL` 生成覆盖场景。
6. 用多样性搜索扩展测试集。
7. 通过 mapping tables 把抽象场景翻成可执行测试用例。

## 案例与结果

### 案例规模

1. `25` 个 timed automata：
   - `3` 个 environment automata；
   - `22` 个 requirement automata。
2. `122` 个测试用例代表现实测试预算。
3. 评估基准包含 `323` 个非等价变异体。

### 主要结果

Table III 显示：

1. `TAUC` 在 `122` 个用例预算下的平均 fault coverage 约 `91%`。
2. 随机测试约 `40%`。
3. 人工测试约 `60%`。

### 结果解释

论文指出，`TAUC` 的优势来自它能生成覆盖非平凡输入交互的时序测试，例如多条总线消息组合导致 interrupt handler 延迟，进而拖慢错误确认流程。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究的主要价值不在“对象验证”，而在“如何把非正式需求和少量 formal model 结合，自动生成高价值验证/测试场景”。

### 可借鉴之处

1. 用用例场景弥补 formal model 不完整的问题。
2. 将 `UPPAAL` 用作场景生成器，而不局限于证明器。
3. 通过 diversity 优化提升固定预算下的故障检出率。

### 存在的不足与改进空间

1. 更偏 testing than verification。
2. 依赖 partial oracle。
3. `BodySense` 实际工件未公开。

### 对本研究的启发

如果博士研究后续要从自然语言/半结构化需求生成验证场景，这篇论文说明：完全可以用“轻量 formal model + 场景约束”的方式，避免一开始要求完整状态机。

## 重要的相关工作

### 1. `UMTG`

- `UMTG` 负责从 use case 规格中抽取功能场景，是 `TAUC` 的上游。

### 2. `UPPAAL`

- `UPPAAL` 用于生成 timeliness scenarios 和支撑 test automation。

### 3. 工业案例 `BodySense`

- `BodySense` 让方法不只停留在教学示例，而是落在真实汽车嵌入式软件上。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：`TAUC` 原型页面当前可访问，但 `BodySense` 的用例、timed automata 和 mapping tables 未公开。
- 获取方式/链接：[DOI](https://doi.org/10.1109/ICST.2017.34)；[PDF](https://orbilu.uni.lu/bitstream/10993/29023/1/Chunhui-ICST-2017.pdf)；[`TAUC` 原型页](https://taucgen.github.io/)
- 对后续复用的现实影响：适合复用“用例 + timed automata + `UPPAAL`”的场景生成思路，但若要复现实验仍需自建工业案例资产。
