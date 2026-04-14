# AVATAR：面向安全与安全性的 SysML 形式验证环境 / AVATAR: A SysML Environment for the Formal Verification of Safety and Security Properties

## 基本信息

- 标题：AVATAR: A SysML Environment for the Formal Verification of Safety and Security Properties
- 中文标题：AVATAR：面向安全与安全性的 SysML 形式验证环境
- 作者：Gabriel Pedroza，Ludovic Apvrille，Daniel Knorreck
- 发表：*2011 11th Annual International Conference on New Technologies of Distributed Systems*，pp. 1-10，2011
- DOI：`10.1109/NOTERE.2011.5957992`
- 链接：https://doi.org/10.1109/NOTERE.2011.5957992
- 形式主义：`AVATAR / TTool / SysML blocks + state machines + pragmas`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：将 safety/security 共置于同一 SysML 建模环境中的验证工作台
- 工具/实现获取方式：原文明确说明 `TTool` 提供 `AVATAR` 编辑与一键式验证入口，并调用 `UPPAAL` 和 `ProVerif` 完成 safety / security 证明。
- 标准/格式获取方式：核心承载包括 `AVATAR` Block Diagram、State Machine Diagram、`TEPE` Parametric Diagram，以及写在 block diagram note 中的 security pragmas。

## 简报

这篇论文补出的核心不是单个算法，而是一种把 `SysML` 设计、实时 safety 分析和 security 分析压到同一模型里的工作台。`AVATAR` 允许设计者在一个 `SysML` 风格模型中同时表达 block、状态机、时间行为和 security pragmas，然后分别自动落到 `UPPAAL` 与 `ProVerif`。

- 形式主义定位：`SysML`-based modeling and verification environment，不是新的底层自动机母型。
- 构造方式简述：系统由 communicating blocks 与 `AVATAR` state machines 描述，safety 属性写在 `TEPE` parametric diagrams，security 属性写成 `InitialCommonKnowledge / Confidentiality / Authenticity` pragmas。
- 基础设施与场景简述：依托 `TTool`、`UPPAAL`、`ProVerif` 和 press-button translation，面向分布式嵌入式系统的统一 safety/security 设计。

```text
SysML-like blocks + state machines + TEPE / security pragmas -> TTool translation -> UPPAAL / ProVerif -> proof results
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `AVATAR` block diagrams。
2. `AVATAR` state machine diagrams。
3. `TEPE` parametric diagrams，用于 safety properties。
4. security pragmas：`InitialCommonKnowledge`、`Confidentiality`、`Authenticity`。
5. `TTool -> UPPAAL / ProVerif` 的双后端翻译与验证。

### 核心抽象

结合论文的分层方法论，可把一个 `AVATAR` 模型保守整理为：

$$
A = (BD, SMD, PD, P)
$$

上式中的符号逐项解释如下：

1. `BD` 是 block diagram，描述 blocks、ports、channels 和 signals。
2. `SMD` 是与 blocks 绑定的 state machine diagrams。
3. `PD` 是 `TEPE` parametric diagrams，用于形式化 safety properties。
4. `P` 是 security pragmas 集合。
5. 这组元组是根据论文的方法阶段和图模型对象做的保守归纳。

论文直接给出了 `AVATAR -> ProVerif` 的翻译定义：

$$
Pr = T(BD, P)
$$

上式中的符号逐项解释如下：

1. `T` 是论文定义的翻译过程。
2. `BD` 是 block diagram。
3. `P` 是 pragma 集合。
4. `Pr` 是输出的 `ProVerif` 规格。
5. 这正是论文 `Definition 1` 的核心公式。

论文还给出了三类 pragma 的枚举：

$$
\mathrm{Types}(P) = \{\mathrm{InitialCommonKnowledge},\ \mathrm{Confidentiality},\ \mathrm{Authenticity}\}
$$

上式中的符号逐项解释如下：

1. `InitialCommonKnowledge` 用于声明系统启动前的共享知识。
2. `Confidentiality` 用于声明某属性不应被 attacker 获得。
3. `Authenticity` 用于声明某接收事件必须由某发送事件先发生支撑。

对 `Authenticity`，论文直接给出 `ProVerif` 级查询模板：

$$
\mathrm{query}\ \mathrm{evinj}:b_2\_state_2(attr_2) \Longrightarrow \mathrm{evinj}:b_1\_state_1(attr_1)
$$

上式中的符号逐项解释如下：

1. `b_1, b_2` 是发送方和接收方 block。
2. `state_1, state_2` 是与消息相关的状态。
3. `attr_1, attr_2` 是参与真实性约束的数据。
4. `evinj` 表示注入式事件对应，用来表达“接收一定由先前发送支撑”的认证关系。

### 一个最小例子与通俗解释

论文中的 Alice-Bob toy example 很适合做最小直觉例子：

1. `Alice` 和 `Bob` 是两个 communicating blocks。
2. 他们在系统启动前共享对称密钥 `sk`，这由 `InitialCommonKnowledge` pragma 明确声明。
3. `Alice` 通过 channel 发送密文，`Bob` 解密并验证消息。
4. 建模完成后，`TTool` 自动把机密性问题翻成 `ProVerif` 查询，把 safety/timing 问题翻到 `UPPAAL`。

通俗地说，`AVATAR` 像是在 `SysML` 上再加一层“双验证插口”：同一份图既能问“这个时序会不会出错”，也能问“攻击者能不能拿到这个值”。

### 运行 / 接受 / 转移语义

运行语义核心包括：

1. `AVATAR` blocks 通过同步或异步 channels 交换 signals。
2. `AVATAR` state machines 基于 `SysML` state machines，并支持 hierarchical states。
3. `after(tmin,tmax)` 建模被动等待，`computeFor(tmin,tmax)` 建模主动执行时间。
4. security pragmas 不直接改变 block 行为，而是改变翻译后形成的 `ProVerif` 查询与辅助过程。

### 语义边界

边界也很清楚：

1. safety 与 security 共享同一个前端模型，但后端分析语义分别依赖 `UPPAAL` 与 `ProVerif`。
2. security 侧主要受 `ProVerif` 支持的 symbolic attacker model 与查询形式限制。
3. 数值运算和复杂 guard 并不能总是被完整保留到 `ProVerif` 层。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$A = (BD, SMD, PD, P)$` | `AVATAR` 同时维护结构、行为、safety 属性和 security pragmas。 |
| `ProVerif` 翻译 | `$Pr = T(BD, P)$` | security 分析依赖 block diagram 与 pragmas 的自动翻译。 |
| pragma 类型 | `$\mathrm{Types}(P)=\{\mathrm{InitialCommonKnowledge},\mathrm{Confidentiality},\mathrm{Authenticity}\}$` | 安全性扩展的核心建模接口是三类 pragma。 |
| authenticity 查询 | `$\mathrm{query}\ \mathrm{evinj}:b_2\_state_2(attr_2)\Rightarrow \mathrm{evinj}:b_1\_state_1(attr_1)$` | “接收必须由先前发送支撑”的认证关系被压成 `ProVerif` 查询。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 每个行为 block 都有显式 state machine。 |
| 事件 / 触发 | 很强 | signals、ports 和 channels 是一等对象。 |
| 守卫 / 数据 | 强支持 | blocks、attributes、pragmas 和函数调用共同参与数据语义。 |
| 层次 | 很强 | 直接继承 `SysML` 层次状态机能力。 |
| 并发 / 同步 | 很强 | communicating blocks 与同步/异步 channels 是系统骨架。 |
| 时间约束 | 很强 | `after` 与 `computeFor` 直接面向实时分析。 |
| 连续动态 / 随机性 | 不支持 | 重点是离散嵌入式行为与安全/安全性分析。 |
| 可执行 / 可验证性 | 很强 | `TTool` 自动连接 `UPPAAL` 与 `ProVerif`。 |

### 形式化问题与性质

1. `AVATAR` 的最大价值是把“一个前端模型 + 两个形式后端”做成稳定工作流。
2. 它把 security 从零散注释提升成 block-diagram 级 pragma 对象。
3. 它也把 `SysML` state machine 的 timing 语义通过 `after/computeFor` 做得更贴近 formal analysis。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 在 block diagram 中定义 blocks、attributes、signals、ports 和 channels。
2. 为行为 blocks 编写 `AVATAR` state machines。
3. 用 `TEPE` parametric diagrams 描述 safety properties。
4. 在 block diagram note 中声明 security pragmas。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `TTool` 中的 `AVATAR` block/state-machine/TEPE 模型；
2. `InitialCommonKnowledge / Confidentiality / Authenticity` pragmas；
3. 自动生成的 `UPPAAL` 模型；
4. 自动生成的 `ProVerif` 规格。

### 交换与互操作

这条线的互操作重点在于：

1. 前端维持统一的 `SysML` 风格；
2. safety 与 security 各自落到最合适的专用后端；
3. 建模者不用手工维护两套异构形式模型。

## 配套基础设施

- 建模/编辑工具：`TTool` 提供 `AVATAR` block/state machine/TEPE 编辑。
- 解析/交换/元模型支持：`TTool` 负责 `AVATAR` 到 `UPPAAL` / `ProVerif` 的翻译。
- 仿真/执行支持：重点不在运行时执行，而在验证前的结构化 SysML 建模与分析准备。
- 验证/分析支持：`UPPAAL` 负责 safety / timing 证明，`ProVerif` 负责 confidentiality / authenticity 证明。
- 代码生成/转换支持：核心是 model-to-model / model-to-specification translation，不是部署代码生成。
- 标准化或社区生态：依托 `TTool`、`UPPAAL`、`ProVerif` 与 SysML-based MBSE 研究生态。

## 适用场景与需求前提

### 适用场景

适合车载网络、分布式 ECU、通信链路暴露于攻击面的嵌入式系统，以及需要同时审计 safety 与 security 的早期设计场景。

### 需求前提

1. 系统可以抽成 communicating blocks 与 state machines。
2. 时间行为能用 `after/computeFor` 这类离散时间算子表达。
3. safety 属性可以落成 `TEPE` parametric diagrams。
4. security 属性主要是机密性、真实性和启动前共享知识这类 symbolic 问题。

### 不适用或高成本场景

如果系统严重依赖连续动力学、复杂概率模型或 `ProVerif` 难以表达的攻击语义，`AVATAR` 的统一前端优势就会被削弱。

## 与相邻形式主义的关系

相对 [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)，`AVATAR` 从 `UML/RT-LOTOS` 进一步走向 `SysML + UPPAAL/ProVerif`，更强调 safety/security 一体化；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，它不是把行为图送进单一验证后端，而是把不同属性拆给不同工具；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 在这里是后端引擎而不是前端建模语言。

## 与本研究的关系

### 对 Project 1 的价值

它直接说明：当未来要做“需求 -> 模型 -> 验证 -> 修复”闭环时，属性类型并不一定要塞进同一个验证器；统一前端模型、按属性分流到不同后端，可能更现实。

### 作为目标形式主义还是中间表示

更像高层中间表示与验证工作台，而不是最终交付给下游控制器的最低层形式模型。

### 对需求到模型生成的启发

1. safety 与 security 需求应该在前端模型里就被区分成不同承载物，而不是都混成普通注释。
2. block / state machine / property diagram / pragma 这种多视图协同，比单图承载所有语义更稳。
3. 一键式后端分发是非常可借鉴的工程策略。

### 现实限制

它的统一性建立在专用翻译链条之上，一旦属性或数据语义超出后端能力，前端模型再统一也无济于事。

## 重要的相关工作

1. [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)：更早的 `TTool` 生态条目，偏 `RT-LOTOS` 后端。
2. [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：另一条 `UML` 行为图自动验证桥接路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：`UML` 状态机自动验证路线的系统综述。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：主贡献是把 `SysML` 设计对象、属性承载和 `UPPAAL/ProVerif` 双后端验证工作流固定成可复用环境，因此更适合作为 `📦/🏗️` 条目入账。
