# 基于定时自动机的汽车反应式系统测试 / Testing Automotive Reactive Systems Using Timed Automata

## 基本信息

- 标题：Testing Automotive Reactive Systems Using Timed Automata
- 中文标题：基于定时自动机的汽车反应式系统测试
- 作者：Jan Sobotka, Jiri Novak
- 发表：*2017 9th IEEE International Conference on Intelligent Data Acquisition and Advanced Computing Systems: Technology and Applications (IDAACS)*, pp. 510-513, 2017
- DOI：`10.1109/IDAACS.2017.8095133`
- 链接：https://doi.org/10.1109/IDAACS.2017.8095133
- 形式主义：`Timed Automata / Taster HIL Testing Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：汽车电子测试 / 定时自动机应用建模
- 工具/实现获取方式：原文使用 `UPPAAL` 建立 `SUT + environment` timed automata model，并在自研 `Taster` 工具中结合 `NI VeriStand` 做 Hardware-in-the-Loop 在线测试；论文未给公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` 4 模型、`Taster` 的对象化模型解析和 `NI VeriStand` 适配层；无独立行业交换标准。

## 简报

这篇论文处理的是汽车电子集成测试里一个很现实的问题：如果 ECU 行为已经能被抽成一个带时间语义的反应式模型，那么测试就不该只靠手写脚本，而应该由模型直接驱动硬件在环环境。作者因此提出 `Taster` 工具：先在 `UPPAAL` 里把 `SUT` 和 environment 写成 timed automata network，再让 `Taster` 负责模型探索、刺激生成和对 `NI VeriStand` 硬件在环平台的连接。

- 形式主义定位：这是 `Timed Automata` 在 automotive integration testing 上的应用条目，重点是“模型驱动测试执行”，不是新的语言本体。
- 构造方式简述：把按钮、钥匙位置和 ECU 观测状态写成 timed automata，再由 `Taster` 的随机 / systematic / relevance-guided 三种策略探索模型并驱动 `SUT`。
- 基础设施与场景简述：依托 `UPPAAL`、`Taster`、`NI VeriStand` 和 HIL 工作流，服务汽车电子功能级集成测试。

```text
textual automotive function spec -> UPPAAL timed automata model -> Taster exploration -> NI VeriStand / HIL -> ECU integration testing
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `SUT` 及其 environment 的 timed automata network。
2. `Taster` 工具中的模型分析器和运行时执行器。
3. `NI VeriStand` 硬件在环适配器。
4. 随机、systematic 和 relevance-guided 三种探索策略。
5. Keyless access (`KESSY`) 示例中的 start button、door button、key position 和 engine observer。

### 核心抽象

论文直接采用 timed automaton 的标准四元组：

$$
A = (N, l_0, E, I)
$$

上式中的符号逐项解释如下：

1. `$N$` 是位置集合。
2. `$l_0 \in N$` 是初始位置。
3. `$E$` 是边集合。
4. `$I$` 是位置不变式。

文中说明 testing workflow 的形式对象其实是一个 network of timed automata，可保守整理为：

$$
\mathcal{T}_{auto} = A_{env,start} \parallel A_{env,door} \parallel A_{env,key} \parallel A_{sut}
$$

上式中的符号逐项解释如下：

1. `$A_{env,start}$` 是 start button 环境 automaton。
2. `$A_{env,door}$` 是 door lock button 环境 automaton。
3. `$A_{env,key}$` 是 key position 环境 automaton。
4. `$A_{sut}$` 是被测 ECU / observer automaton。
5. `$\parallel$` 表示整个测试环境由多个 automata 并行构成。

论文另一个很有辨识度的扩展是 `relevance` 标注。它并不是 timed automata 理论的新元组，但在工具实现里它相当于对位置附加了优先级映射：

$$
rel : N \to \mathbb{N}
$$

上式中的符号逐项解释如下：

1. `$N$` 是 automaton 的位置集合。
2. `$rel(n)$` 是位置 `$n$` 的 relevance 数值。
3. 工具用它偏置模型探索，使高相关状态更容易被优先覆盖。

### 一个最小例子与通俗解释

论文中的 `KESSY` keyless access 示例很直观：

1. environment 侧分别建模 start button、door lock button 和 key position。
2. `SUT` 侧建模 engine state observer，区分 engine stop / running 以及更细的 power supply 状态。
3. 当“钥匙在车内 + start button 短按”成立时，模型允许探索发动机启动路径。
4. `Taster` 根据模型探索结果向真实 HIL 系统发刺激，再读回输出判断是否符合 automaton oracle。

通俗地说，这像“先把司机和车钥匙也写成状态机，然后让这些状态机去按按钮测 ECU”。这样测试刺激不是人工拍脑袋写出来的，而是由 timed automata 探索自然产生。

### 运行 / 接受 / 转移语义

论文主体不是模型检查查询，而是模型驱动测试执行。其核心执行语义可以保守写成：

$$
(\mathcal{T}_{auto}, s_0) \xrightarrow{\text{explore}} \sigma \xrightarrow{\text{adapter}} IUT
$$

上式中的符号逐项解释如下：

1. `$\mathcal{T}_{auto}$` 是测试用 timed automata network。
2. `$s_0$` 是其初始状态。
3. `explore` 表示 `Taster` 按某种策略探索模型。
4. `$\sigma$` 是由探索生成的一段刺激序列。
5. `adapter` 把模型刺激映射为 `NI VeriStand` 可执行的真实输入。

工具运行时支持三种主要策略：

1. `random`：适合黑盒起步。
2. `systematic`：近似 conformance testing。
3. `experimental/relevance-guided`：优先探索高 relevance 状态。

论文还给出测试终止条件：invariant violation、用户终止或 coverage criterion 满足。也就是说，这里的“接受语义”更接近测试判定而不是语言接受。

### 语义边界

这篇论文的边界主要有：

1. 主体贡献在 testing workflow，而不是复杂 timed automata 理论。
2. 论文当时只支持 `bool / int / clock / chan` 等相对受限的数据类型。
3. 测试效果高度依赖被测系统与 adapter 的可连接性。
4. KESSY 例子主要是功能级 integration testing，不是整车级交通场景验证。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单 automaton 骨架 | `$A = (N, l_0, E, I)$` | 论文采用的 timed automaton 基础对象。 |
| 测试网络 | `$\mathcal{T}_{auto} = A_{env,start} \parallel A_{env,door} \parallel A_{env,key} \parallel A_{sut}$` | 把环境与被测 ECU 联合建模。 |
| relevance 映射 | `$rel : N \to \mathbb{N}$` | 用来偏置探索优先级。 |
| 模型驱动测试链 | `$(\mathcal{T}_{auto}, s_0) \xrightarrow{\text{explore}} \sigma \xrightarrow{\text{adapter}} IUT$` | 把模型探索直接映射成 HIL 测试刺激。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 按钮、钥匙、engine observer 都是显式状态机。 |
| 事件 / 触发 | 强支持 | button press、key presence、engine transition 是测试主体。 |
| 守卫 / 数据 | 部分支持 | 支持 `bool/int/clock/chan`，但数据能力刻意做了裁剪。 |
| 层次 | 弱支持 | 可做高低层 observer 组合，但主体仍是平铺 automata network。 |
| 并发 / 同步 | 支持 | environment 与 `SUT` 并行执行。 |
| 时间约束 | 中等支持 | 以 timed automata 保障反应式时序与 HIL 节奏。 |
| 连续动态 / 随机性 | 不支持 | 论文不做连续动力学或概率行为建模。 |
| 可执行 / 可验证性 | 很强 | 模型直接进入 `Taster + VeriStand` 执行。 |

### 形式化问题与性质

1. 论文最重要的不是“汽车领域用了 timed automata”，而是把 timed automata 直接推进了 HIL testing workflow。
2. `relevance` 扩展说明，测试并不只是穷举，还可以把领域知识压进探索优先级。
3. 对 `project_1` 而言，这提示后续 LLM 生成模型时，应尽量保留可测试的环境动作而不是只保留系统内部逻辑。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 先把 textual function specification 写成 environment / `SUT` automata。
2. 在 `UPPAAL` 中完成模型编辑。
3. 用 `Taster` 解析 `UPPAAL 4` 格式并构造成对象模型。
4. 通过 `NI VeriStand` 适配器把探索结果注入硬件在环平台。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL 4` 模型文件。
2. `Taster` 内部对象模型。
3. XML 格式的系统模型和测试 trace。
4. `NI VeriStand` API。

### 交换与互操作

互操作重点在：

1. `UPPAAL` 模型到 `Taster` 对象模型的解析。
2. `Taster` 到 `NI VeriStand` 的适配。
3. HIL 输出再回流到 `Taster` 做 oracle 判断。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：`Taster` 自带 `UPPAAL` 模型分析器；无统一外部元模型。
- 仿真/执行支持：`Taster` + `NI VeriStand` + HIL 环境。
- 验证/分析支持：支持不同探索策略、trace 记录和 coverage-based 停止条件。
- 代码生成/转换支持：不是代码生成，而是模型到测试刺激的执行转换。
- 标准化或社区生态：依托 `UPPAAL` 和汽车电子 HIL 测试生态。

## 适用场景与需求前提

### 适用场景

适合汽车电子功能级集成测试、尤其是已经有明确反应式状态和时间行为边界的 ECU 场景。

### 需求前提

1. 环境输入和系统输出都能抽成有限状态。
2. 被测系统可接入 HIL 平台。
3. 需求关注点在反应式行为和按钮/传感器触发逻辑。

### 不适用或高成本场景

如果系统关键性状主要来自复杂连续车辆动力学或大规模交通交互，仅用这里的功能级 timed automata 抽象会太薄。

## 与相邻形式主义的关系

相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，本文更偏测试执行而不是静态验证；相对 [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，它不做计划修正，而是直接驱动 HIL 测试；相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，本文对象是 ECU integration testing，而不是总线协议。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：状态机如果最终要服务工程闭环，就不应只支持验证，还应尽可能支持“用模型直接驱动测试”。

### 作为目标形式主义还是中间表示

对 automotive integration testing，它更适合作为测试阶段的中间表示；但如果团队以 timed automata 作为规范核心，它也可以成为直接目标工件。

### 对需求到模型生成的启发

1. 环境模型和系统模型应该一起生成，而不是只生成 `SUT`。
2. 若后续要支持自动测试，状态上最好保留 relevance / criticality 一类可探索信息。
3. 形式模型和测试平台之间的 adapter 设计应当尽早纳入闭环方法论。

## 重要的相关工作

- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：同样展示 timed automata 如何接入复杂运行系统，但重心是验证。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：同样是汽车/嵌入式相关 timed automata 条目，但对象是总线协议。
- [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)：同样把 timed automata 放到工程链路里，但用于计划约束求解。

## 文献分类总结

- 形式主义：`Timed Automata / Taster HIL Testing Model`
- 成熟度：`UPPAAL + Taster + VeriStand` 执行链清晰，属于偏测试落地的应用条目。
- 条目价值：这是一篇 `⏱️` 类应用条目，核心贡献是把 timed automata 直接推进到 automotive HIL integration testing。
