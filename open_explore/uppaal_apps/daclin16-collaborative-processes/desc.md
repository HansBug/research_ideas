问题一句话：本文验证的是协同流程中的互操作性需求，核心问题是这类需求能否被写成结构化 DSL，并进一步落成 `UPPAAL` 可验证的 `TCTL` 查询。
方法一句话：作者先构建互操作性需求 repository 和领域 DSL，再把 DSL 需求映射为 `TCTL`，用 `UPPAAL` 验证 collaborative drug circulation process 中的消息流、任务、资源和时间约束。
验证收获一句话：论文在药物流转协同流程上给出了从 DSL 到 `TCTL` 的完整重写链条，并展示了消息流、资源激活和任务执行约束如何被转成 `E<>`、`A[]` 等可执行查询。

## 基本信息

- 标题：Writing and verifying interoperability requirements: Application to collaborative processes
- 中文标题：互操作性需求的编写与验证：面向协同流程的应用
- 作者：Nicolas Daclin、Sihem Mallek Daclin、Vincent Chapurlat、Bruno Vallespir
- 单位：LGI2P / Ecole des Mines d'Ales；Univ. Bordeaux；CNRS IMS
- 发表：Computers in Industry，2016
- DOI：`10.1016/j.compind.2016.04.001`
- 链接：[DOI](https://doi.org/10.1016/j.compind.2016.04.001)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🏥 医疗与健康
- 被验证系统：collaborative drug circulation process 的互操作性需求与流程模型
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文依赖 DSL、repository 和 `UPPAAL` 查询重写流程，但未提供独立仓库；公开 `HAL` 版本可获取正文。
- 案例/数据获取方式：正文给出 collaborative drug circulation process 的 `BPMN 2.0` 流程和需求示例，可据此重建。

## 简报

这篇论文的对象不是单一协议，而是“协同流程需要满足哪些互操作性要求，以及这些要求怎么被正式写下来再验证”。它的重要性在于把需求写作和模型检查接到了一起。

- 系统：药物流转协同流程中的任务、资源、消息流和参与方协作关系。
- 特点：先有互操作性需求 repository，再有 DSL，再有 `TCTL` / `UPPAAL` 验证。
- 规模：围绕 collaborative drug circulation process 展开，正文展示了 `BPMN` 流程、资源声明和多类需求样例。
- 模型：需求以 DSL 表达，再映射到 `TCTL`，最终由 `UPPAAL` 检查。
- 性质：消息流终止、资源激活、任务执行、时间上界和流程可达性。
- 方法：`repository -> DSL -> syntax tree -> TCTL -> UPPAAL query`。
- 结果：论文给出具体 DSL/TCTL 对照和实际查询，证明互操作性需求可以稳定落到形式验证层。

`互操作性需求 repository -> DSL 编写 -> TCTL 重写 -> UPPAAL 查询 -> 协同流程验证`

## 论文定位

这是一篇偏方法驱动但案例边界清晰的 `🧩 + 🏥` 条目。它不只是提需求理论，而是明确在一个具体药物流程上执行了重写与验证。

## 验证对象与问题背景

### 系统与场景

案例是 collaborative drug circulation process。药物流转涉及处方、发药、交付、资源和消息流，如果互操作性需求表达不清，就容易出现接口错配和执行阻塞。

### 系统组成与运行机制

论文把系统分成：

1. tasks / activities
2. resources / human resources
3. message flows
4. process model (`BPMN 2.0`)
5. interoperability requirements

### 验证边界

本文验证的是**协同流程模型和互操作性需求的一致性**，不涉及医院真实信息系统的全部实现。

### 核心问题

互操作性需求若只停留在自然语言，很难复用、更难验证；而直接写 `CTL/TCTL` 又过于底层，不利于领域人员维护。

## 模型与形式化建模

作者的路径是：

1. 用 repository 对互操作性需求按抽象层、视图和生命周期分类。
2. 用领域 DSL 让需求能以更贴近领域语言的方式表达。
3. 再把 DSL proposition 映射成 `TCTL` proposition。
4. 最终交给 `UPPAAL` 验证。

这篇论文的关键价值正是“形式逻辑和领域表达之间的中间层”。

## 验证目标与性质

### 待验证问题

1. 某些消息流是否最终到达接收端；
2. 任务和资源是否在正确状态组合下发生；
3. 时间和同步要求是否满足；
4. 互操作性需求在流程模型上是否可证。

### 性质类型

- 可达性
- 流程一致性
- 时间约束
- 消息/资源协同

### 查询表达

论文给出多种 DSL 到 `TCTL` 的映射示例，例如：

1. `E<> task.Working and resource.Active ...`
2. `E<> forall(i:NbMessageFlow) emission_message_end[i] - recep...`
3. DSL modality 与 `A[] / E[] / E<>` 的系统映射。

## 核心方法与验证流程

1. 建立互操作性需求 repository。
2. 用 DSL 编写单条需求。
3. 解析需求语法树。
4. 把 DSL proposition 映射为 `TCTL` proposition。
5. 在 `UPPAAL` 上对 collaborative process model 运行查询。
6. 用验证结果回看需求和流程模型中的互操作性缺口。

## 案例与结果

药物流转案例中，论文展示了：

1. 如何对消息流终止与接收写出正式要求；
2. 如何在查询中同时约束 task 和 resource 状态；
3. 如何让一个原本是自然语言的互操作性需求，被稳定重写成 `UPPAAL` 查询。

它的核心收获不是某一条数值结果，而是把需求写作、需求结构化和模型检查打通。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究非常接近，因为它展示了“需求语言 -> 形式性质 -> 模型验证”的完整桥接过程。

### 可借鉴之处

1. 先定义领域 DSL，再谈性质生成。
2. 把需求 repository 作为可复用中间层。
3. 用语法映射而不是纯人工翻译来连接需求和逻辑。

### 存在的不足与改进空间

论文更强调需求写作链条，对实际 `UPPAAL` 模型细节展开不多，且未公开工件。

### 对本研究的启发

如果博士研究要做“自动生成验证场景与性质”，这篇论文说明先把需求语言结构化是非常关键的一步。

## 重要的相关工作

### 1. interoperability requirements repository

- 本文把需求组织和验证放在同一工作流中。

### 2. DSL 到 `TCTL` 映射

- 这是它相对传统需求工程工作的最大增量。

### 3. `UPPAAL` 在业务流程场景中的应用

- 文中把流程互操作性明确落成了 timed automata 可检验问题。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：`HAL` 论文可得，但未见独立 DSL 工具实现、`UPPAAL` 工程和案例包。
- 获取方式/链接：[DOI](https://doi.org/10.1016/j.compind.2016.04.001)；[HAL 页面](https://hal.science/hal-01930301)
- 对后续复用的现实影响：适合作为“需求 DSL 如何重写为 `TCTL`”的强样本，但要复跑完整链路仍需自行重建 DSL 和流程模型。
