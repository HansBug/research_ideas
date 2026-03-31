问题一句话：本文验证的是 Océ 打印/复印系统中的图像处理数据通路调度，核心问题是在作业到达时间不确定时，控制器如何同时兼顾 `DirectCopy` 吞吐量和 `PrintWithProcessing` 服务时间。
方法一句话：作者把打印系统资源、作业 use case 和不确定到达建成 timed game automata，用 `UPPAAL Tiga` 自动综合满足 trade-off 约束的调度策略。
验证收获一句话：论文得到 `6` 个 Pareto-optimal 策略，证明 `UPPAAL Tiga` 能为不确定作业到达的工业调度问题生成自适应策略，同时也指出自动生成规则过大、难以直接部署到真实控制器。

## 基本信息

- 标题：Adaptive Scheduling of Data Paths using Uppaal Tiga
- 中文标题：使用 `Uppaal Tiga` 对数据通路做自适应调度
- 作者：Israa AlAttili、Fred Houben、Georgeta Igna、Steffen Michels、Feng Zhu、Frits Vaandrager
- 单位：Radboud University Nijmegen
- 发表：QFM 2009 / Electronic Proceedings in Theoretical Computer Science 13
- DOI：`10.4204/EPTCS.13.1`
- 链接：[DOI](https://doi.org/10.4204/EPTCS.13.1)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🏭 工业与基础设施
- 被验证系统：Océ 打印/复印设备的图像处理 pipeline 与资源调度
- UPPAAL线：`UPPAAL Tiga`
- 代码/模型/仓库获取方式：论文给出在线模型页，可访问 [TigaOce 页面](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/) 与 `model.xml`、`ExtendedModel.zip`。
- 案例/数据获取方式：案例来自 Océ 工业打印系统设计；模型与扩展版公开，但无真实生产数据集。

## 简报

本文研究的不是一般 job-shop，而是一个具体打印设备中的 image-processing pipeline。它的关键难点是：远程/本地作业共享 `Scanner`、`USB`、`IP` 组件和 memory，而某些作业的到达时间不可预测。

- 系统：Océ 打印/复印系统，包含 `Scanner`、`Controller`、`ScanIP`、`IP1`、`IP2`、`PrintIP`、memory、`USB`。
- 特点：同时处理本地与远程作业，数据通路可并行，且 `PrintWithProcessing` 到达时间不确定。
- 规模：基础案例围绕 `DirectCopy` 与 `PrintWithProcessing` trade-off；扩展模型还加入 `ScanToEmail`，并分析 `10` 个 `ScanToEmail` job。
- 模型：每个 use case 与资源各有 automaton，memory 用共享变量建模；不确定作业在 `UPPAAL Tiga` 中用 uncontrollable edge 表达。
- 性质：`DirectCopy` 吞吐上界、`PrintWithProcessing` 最大服务时间、作业最终完成。
- 方法：综合 Pareto-optimal 策略，再与简单固定策略比较。
- 结果：得到 `6` 个最优 trade-off；优先级策略可逼近最优，但自动生成策略过大，不适合直接烧到控制器。

`打印 pipeline 架构 -> use case/resource automata -> 不确定作业到达 -> Tiga 赢策略综合 -> Pareto trade-off -> 固定策略对照`

## 论文定位

这篇论文是很标准的 `⏱️ + 🏭` 条目。作者验证的不是控制器功能正确性，而是工业资源调度和服务时间权衡，因此放在“调度、资源与性能分析”主轴最合适。

## 验证对象与问题背景

### 系统与场景

Océ 系统不仅做扫描、复印和打印，还支持远程 image processing 作业。作业通过 `Scanner` 或 `Controller` 两个端口进入，经过不同的数据通路后从 `Printer` 或 `Controller` 离开。

### 系统组成与运行机制

论文明确给出若干 datapath：

1. `DirectCopy = Scanner -> ScanIP -> IP1 -> IP2 -> USBClient, PrintIP`
2. `ScanToStore`
3. `ScanToEmail`
4. `ProcessFromStore`
5. `PrintWithProcessing = USBClient -> IP2 -> PrintIP`

它们共享 image processing 组件、memory 和 `USB` 带宽，因此天然形成调度竞争。

### 验证边界

论文关注的是作业调度和资源占用，不涉及打印内容正确性或物理打印质量。

### 核心问题

一个典型问题是：当 `PrintWithProcessing` 作业到达时间不可预测时，控制器能否在不预知未来到达时刻的前提下，仍保证合理服务时间，同时维持 `DirectCopy` 的高吞吐。

## 模型与形式化建模

### 基础架构

1. 每个 use case 用单独 automaton 建模。
2. 每个资源也有 automaton。
3. memory 以共享变量表示。

资源 automaton 具有 `idle -> running -> recovery` 三种典型阶段，并用 `execution time` 与 `recover time` 参数化。

### 抽象边界

论文保留了：

1. 组件 claim/release；
2. memory 分配/释放；
3. `USB` 上下行并发；
4. use case 间资源争用；
5. 不确定 job arrival。

### `UPPAAL Tiga` 的作用

普通 `UPPAAL` 可以用 nondeterminism 表示不确定作业，但优化时会“偷看未来”。`UPPAAL Tiga` 通过 controllable / uncontrollable 划分，把作业到达变成环境动作，从而避免控制器利用未来知识。

## 验证目标与性质

### 待验证问题

1. `DirectCopy` 的最大完成间隔能否保持低值。
2. `PrintWithProcessing` 的最大服务时间能否满足上界。
3. 在 trade-off 条件下，是否存在 winning strategy。

### 性质类型

1. 有界响应；
2. 调度/资源性能；
3. 赢策略可存在性。

### 查询表达

论文将 `DCTIME` 与 `DPTIME` 作为 trade-off 参数，在 observer 支持下表达：

1. 第一份 `DirectCopy` 完成时间约束；
2. 后续 `DirectCopy` 吞吐约束；
3. `PrintWithProcessing` 服务时间约束；
4. job 最终完成性。

## 核心方法与验证流程

1. 先建立 Océ 系统基础 `UPPAAL` 模型。
2. 识别不可预测作业 arrival 带来的“未来知识”问题。
3. 将 arrival 改成环境不可控动作，转入 `UPPAAL Tiga`。
4. 计算不同 `DCTIME` / `DPTIME` 组合下的 winning strategy。
5. 输出 Pareto frontier，并与简单固定策略对比。

## 案例与结果

### Pareto 最优前沿

论文找到 `6` 个最优策略点，形成 `DirectCopy` 吞吐与 `PrintWithProcessing` 服务时间之间的 Pareto frontier。

### 最优值与边界

1. 在没有其他 job 干扰时，`PrintWithProcessing` 的最小服务时间是 `7`。
2. 但若要求其“最终完成”且同时兼顾其他 job，就不存在达到该极值的通用策略。
3. 为最小化 `PrintWithProcessing` 服务时间而设计的策略，会让 `DirectCopy` 吞吐变得比最优值差两倍以上。

### 简单策略对照

论文进一步比较了几类简单策略：

1. 全资源 non-lazy；
2. `DirectCopy` 优先；
3. `PrintWithProcessing` 优先。

结论是：简单策略虽然比自动综合策略弱，但可以逼近最优，并更有现实部署意义。

### 扩展模型

扩展模型加入更多真实调度规则和 memory bus。对一个包含 `ScanToEmail` 与 `PrintWithProcessing` 的场景，`UPPAAL Tiga` 仍可算出优先某类 job 的最快策略，但在更强 nondeterminism 下已难以处理。

## 与本研究的关系

### 相关性分析

它和博士研究相关，因为它清楚展示了“现实资源约束 -> 状态机模型 -> 性质/目标 -> 自动策略生成”的闭环。

### 可借鉴之处

1. 将性能目标写成 observer + 查询。
2. 用 game semantics 消除“未来知识”。
3. 通过 Pareto frontier 解释验证结论，而不是只输出一个 yes/no。

### 存在的不足与改进空间

1. 自动综合出的规则过大，难直接部署。
2. 扩展模型在高 nondeterminism 下仍受状态爆炸限制。
3. 更像调度优化案例，而非传统安全性质案例。

### 对本研究的启发

对于控制系统中的“时延/吞吐/等待时间”需求，验证剖面完全可以写成类似 `DCTIME/DPTIME` 的参数化 trade-off，而不是只验证单个 deadline。

## 重要的相关工作

### 1. 工业打印数据通路建模

- 本文直接建立了 printer/copier pipeline 的 `UPPAAL` 应用样本。

### 2. `UPPAAL Tiga` 工业应用

- 它是 `Tiga` 在工业调度/控制上的早期代表案例之一，而且模型目前仍可获取。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文页面当前可访问，并公开 `model.xml`、优先级变体和扩展模型压缩包。
- 获取方式/链接：[论文模型页](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/)；[基础模型](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/new_model.xml)；[扩展模型](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/ExtendedModel.zip)
- 对后续复用的现实影响：这是一个高公开度的工业调度案例，适合后续直接复跑、修改查询并比较不同策略。
