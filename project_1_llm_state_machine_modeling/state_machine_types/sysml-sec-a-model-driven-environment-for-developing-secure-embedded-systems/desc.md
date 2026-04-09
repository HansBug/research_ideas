# SysML-Sec：面向安全嵌入式系统开发的模型驱动环境 / SysML-Sec: A Model-Driven Environment for Developing Secure Embedded Systems

## 基本信息

- 标题：SysML-Sec: A Model-Driven Environment for Developing Secure Embedded Systems
- 中文标题：SysML-Sec：面向安全嵌入式系统开发的模型驱动环境
- 作者：Ludovic Apvrille，Yves Roudier
- 发表：*SAR-SSI 2013: 8eme Conference sur la Securite des Architectures Reseaux et des Systemes d'Information*，2013
- DOI：原文未提供
- 链接：https://www.eurecom.edu/en/publication/4187/download/rs-publi-4187.pdf
- 形式主义：`SysML-Sec / TTool / pi-calculus + ProVerif validation chain`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：secure-embedded `SysML` environment / model-transformation and verification infrastructure
- 工具/实现获取方式：原文明确说明 `SysML-Sec` 实现在 `TTool` 中，验证链路接到 `ProVerif`，并支持从设计模型到形式规格的自动转换。
- 标准/格式获取方式：承载方式是扩展的 `SysML` block/state-machine/requirement/parametric diagrams、security pragmas 以及生成的 `pi-calculus`/`ProVerif` 输入；原文未给中立交换标准。

## 简报

这篇论文的关键价值，不是简单在 `SysML` 里加几个“安全”标签，而是把安全需求、攻击树、软硬件划分、协议级状态机和形式验证真正连成一条链。`SysML-Sec` 让设计者在 partitioning 阶段就把 asset、threat、allocation 和 security objective 建起来，再在 design 阶段把 block/state machine 模型自动翻译到 `pi-calculus/ProVerif`，去检查 confidentiality 和 authenticity 是否真的成立。

- 形式主义定位：面向 secure embedded systems 的 `SysML` profile / environment，而不是通用状态机理论模型。
- 构造方式简述：先做 block + allocation + requirement + attack-tree 建模，再用 block/state-machine diagrams 描述协议与机制，最后通过 `TTool` 自动生成 `ProVerif` 可验证模型。
- 基础设施与场景简述：依托 `SysML-Sec`、`TTool`、`pi-calculus`、`ProVerif`、`Dolev-Yao` attacker model 和 property pragmas，服务嵌入式通信协议、车载电子和 security-aware system design。

```text
partitioning + requirements + attack trees -> SysML-Sec block/state-machine design -> pi-calculus / ProVerif translation -> confidentiality / authenticity / latency evidence
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. hardware/software partitioning 下的 `SysML` blocks 与 allocate relations。
2. 安全需求与攻击树。
3. 带 security extension 的 block diagrams 与 state machine diagrams。
4. cryptographic methods、public/private links、pre-shared knowledge pragmas。
5. `TTool -> pi-calculus -> ProVerif` 的形式验证链。

### 核心抽象

结合论文的 partitioning、design 和 property 三层结构，可以把一个 `SysML-Sec` 条目保守整理为：

$$
S = (B, A, R, K, SM, \Phi)
$$

上式中的符号逐项解释如下：

1. `B` 是 block 集合，既可表示任务也可表示硬件节点。
2. `A` 是 allocation / communication link 集合。
3. `R` 是 requirement 与 attack-tree 约束集合。
4. `K` 是 cryptographic knowledge 与 security mechanism 集合。
5. `SM` 是 block 关联的 state machine 集合。
6. `\Phi` 是 confidentiality / authenticity 等 security pragmas。
7. 这是根据论文的建模流程做的保守归纳，不是原文直接给出的单一元组。

论文对 design-level 语义给出的最关键收束是：

$$
\llbracket S \rrbracket_{\pi} \to \text{ProVerif queries}
$$

上式中的符号逐项解释如下：

1. `\llbracket S \rrbracket_{\pi}` 表示把 `SysML-Sec` 设计翻译到 `pi-calculus` 语义后的形式规格。
2. `\text{ProVerif queries}` 表示对 confidentiality / authenticity 的自动验证查询。
3. 论文明确指出 `TTool` 会把设计模型转成 `ProVerif` 所需的 Horn clauses / `pi-calculus` 规格。

论文还给出了直接的安全 pragma 口径，其中 authenticity 可压成：

$$
\mathsf{Authenticity}(block_1.s_1.m_1,\ block_2.s_2.m_2)
$$

上式中的符号逐项解释如下：

1. `block_1` 是发送消息的一方。
2. `s_1` 是发送前的状态。
3. `m_1` 是发送消息。
4. `block_2` 是接收消息的一方。
5. `s_2` 是接收后验证通过的状态。
6. `m_2` 是被视为 authentic 的接收消息。
7. 论文用 pragma 形式表达这一约束，其直觉是“接收端在状态 `s_2` 接受的消息，必须可追溯到发送端在状态 `s_1` 的先前发送”。

攻击者模型边界则可保守写成：

$$
L = L_{public} \cup L_{private}
$$

上式中的符号逐项解释如下：

1. `L_{public}` 是可被 `Dolev-Yao` attacker 窃听的 public links。
2. `L_{private}` 是不允许外部窃听的 private links。
3. 论文明确说明攻击者只能监听 block 之间的消息，而不能直接读取 block 内部属性。

### 一个最小例子与通俗解释

论文用 `EVITA` 架构里的 key distribution protocol 给了一个很典型的例子：

1. `ECU` 和 `KeyMaster` 都作为 block 建模。
2. block 内部用 state machine 表达协议步骤。
3. 设计者在 block 图上声明 `InitialCommonKnowledge` 等预共享知识。
4. 再用 confidentiality / authenticity pragma 指定“哪把 key 不能泄露”“哪个应答消息必须真的来自指定发送者”。

通俗地说，`SysML-Sec` 不是让你先写一份协议，再额外手写一份安全模型；而是让你在同一份 `SysML` 设计里，把“系统怎样分区”“消息怎样流动”“哪些数据要保密”“哪些消息要可认证”一起写出来，再自动送去验证。

### 运行 / 接受 / 转移语义

论文的主语义链分两层：

1. partitioning / requirement level：说明资产、威胁、分区与链路暴露面。
2. design / verification level：把 block/state-machine + crypto pragmas 变成 `pi-calculus` 规格，再交由 `ProVerif` 检查。

其中最关键的运行语义约束包括：

1. block 间通信链路可标记为 public 或 private。
2. block 可声明 cryptographic methods 与 pre-shared values。
3. security properties 主要以 confidentiality / authenticity pragmas 表达。
4. `ProVerif` 在 `Dolev-Yao` 模型下检验查询，并在失败时回给 trace。

### 语义边界

边界也很明确：

1. 主线是安全协议与架构安全建模，不是一般 timed state-machine 验证。
2. 攻击者模型是 `Dolev-Yao`，不覆盖物理攻击与复杂 exploit chain。
3. 当前 formal validation 主要支持 confidentiality 与 authenticity。
4. 安全性与实时性可以一起评估，但实时验证不是其主对象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 设计骨架 | `$S = (B, A, R, K, SM, \Phi)$` | blocks、allocation、状态机、安全 pragma 共同构成 `SysML-Sec` 设计。 |
| 形式翻译 | `$\llbracket S \rrbracket_{\pi} \to \text{ProVerif queries}$` | 设计模型自动落到 `pi-calculus/ProVerif` 验证链。 |
| authenticity 约束 | `$\mathsf{Authenticity}(block_1.s_1.m_1,\ block_2.s_2.m_2)$` | 指定发送与接收状态之间的真实性对应。 |
| 攻击者可见性边界 | `$L = L_{public} \cup L_{private}$` | 公开链路可被窃听，私有链路不可。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | block 可关联 state machine 描述协议行为。 |
| 事件 / 触发 | 强支持 | 消息发送、接收和协议步骤是核心对象。 |
| 守卫 / 数据 | 很强 | cryptographic data、knowledge pragmas、message authenticity 都显式建模。 |
| 层次 | 中等支持 | requirement hierarchy 与 attack-tree hierarchy 很强，但主线不是层次状态机语义。 |
| 并发 / 同步 | 中等到强 | 多 block 协议交互是核心，但重点在安全协议而非一般并发理论。 |
| 时间约束 | 中等支持 | 可评估 security mechanism 对 latency 的影响，但不是 timed formalism。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续物理过程或概率模型。 |
| 可执行 / 可验证性 | 很强 | `TTool` 自动翻译到 `ProVerif` 并回传验证结果。 |

### 形式化问题与性质

1. 论文真正补的是“如何把 security-aware system design 固定在同一份 `SysML` 工件里”，而不是单一协议证明技巧。
2. 把 attack tree、partitioning 和 design model 放在同一流程里，是它区别于单纯 `ProVerif` front-end 的关键。
3. confidentiality / authenticity pragma 的做法，说明很多安全性质可以直接挂在结构化建模元素上，而不用强迫用户手写完整逻辑公式。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 先做 hardware/software partitioning，与 SysML blocks 和 allocate relations 对齐。
2. 用 requirement diagrams 和 attack trees 表达 security objectives 与 threats。
3. 在 block/state-machine diagrams 中补 security mechanisms、link visibility、knowledge pragmas。
4. 通过 `TTool` 自动生成 `pi-calculus/ProVerif` 模型并验证。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 扩展的 `SysML` block / state-machine / requirement / parametric diagrams。
2. security pragmas，例如 shared knowledge、confidentiality、authenticity。
3. 生成的 `pi-calculus` / Horn-clause 风格 formal specs。
4. `ProVerif` queries 与回传 trace。

### 交换与互操作

这条路线的互操作重点不是通用交换标准，而是：

1. `SysML-Sec` 模型到 `ProVerif` 的自动转换。
2. partitioning 模型与 design 模型之间的连续 refinement。
3. `TTool` 对建模、回溯和验证结果的统一承载。

## 配套基础设施

- 建模/编辑工具：`TTool` 中的 `SysML-Sec` 环境。
- 解析/交换/元模型支持：扩展的 `SysML` diagrams、security pragmas、自动 model transformation。
- 仿真/执行支持：论文提到可从设计模型生成 executable code 进行测试，但主线仍是形式验证。
- 验证/分析支持：`ProVerif`、`pi-calculus` 翻译、partitioning 阶段的 latency / architecture 影响评估。
- 代码生成/转换支持：支持从设计模型到 formal specs，并提到从 design model 到 executable code 的测试链。
- 标准化或社区生态：依托 `SysML / TTool / ProVerif` 研究生态，而非独立工业中立标准。

## 适用场景与需求前提

### 适用场景

适合车载电子、嵌入式通信协议、安全敏感的分布式控制单元，以及需要同时考虑安全与系统分区设计的场景。

### 需求前提

1. 系统可拆成 block、allocation、message flow 和 protocol state machine。
2. 安全目标可以落成 confidentiality / authenticity 等结构化属性。
3. 攻击面主要体现在消息窃听、伪造和协议级交互，而不是复杂物理攻击。
4. 团队接受 `TTool -> ProVerif` 这一 tool-specific formal chain。

### 不适用或高成本场景

如果核心问题在连续控制律、强实时调度证明、复杂 side-channel / physical attack，`SysML-Sec` 就不是最直接的形式主义入口。

## 与相邻形式主义的关系

相对 [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)，它更聚焦 secure embedded design 和 `ProVerif` 式协议验证；相对 [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)，它强调 security properties 与 partitioning，而不是 refinement calculus；相对 [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)，它关注 confidentiality/authenticity 和 secure communication，而不是实时协议 profile 本体。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续想让 LLM 输出“可验证的安全敏感状态机”，则需求侧必须同时抽出 asset、trust boundary、public/private link 和 security property，而不能只生成一般行为状态图。

### 作为目标形式主义还是中间表示

更适合作为 security-aware 中间表示和 formal-validation bridge，而不是最终的通用行为执行标准。

### 对需求到模型生成的启发

1. requirement、attack、architecture 和 protocol state machine 应该共用一套可追溯元素。
2. confidentiality / authenticity 这类属性非常适合做成结构化 pragma，而不是完全自由文本。
3. 软硬件分区会直接影响安全性质能否成立，这一点对需求建模很关键。

### 现实限制

它能很好支撑安全协议和 secure embedded design，但不覆盖完整的实时/混成/连续控制语义。

## 重要的相关工作

1. [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)：同属 `TTool` 生态的 `SysML` formal environment。
2. [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)：更偏实时 `UML` profile 的 formal toolkit。
3. [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)：另一条图形前端到 formal back-end 的 `UML` 路线。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：论文主体是 `SysML-Sec` 环境、其 `TTool -> pi-calculus/ProVerif` 翻译链与建模口径，因此更像 security-aware `SysML` 基础设施，而不是单独一条验证算法论文。
