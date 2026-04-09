# 使用 Acceleo 将 UML 状态机翻译为有色 Petri 网 / Translating UML State Machines to Coloured Petri Nets Using Acceleo: A Report

## 基本信息

- 标题：Translating UML State Machines to Coloured Petri Nets Using Acceleo: A Report
- 中文标题：使用 Acceleo 将 UML 状态机翻译为有色 Petri 网
- 作者：Étienne André，Mohamed Mahdi Benmoussa，Christine Choppy
- 发表：*Electronic Proceedings in Theoretical Computer Science*，150:1-7，2014
- DOI：`10.4204/EPTCS.150.1`
- 链接：https://doi.org/10.4204/EPTCS.150.1
- 形式主义：`UML State Machine / CPN Tools XML / Acceleo model-to-text bridge`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`UML` 状态机到 `CPN` 的自动化桥接实现报告 / model-to-text infrastructure
- 工具/实现获取方式：论文给出 `UML2CPN` 原始网页入口 `http://lipn.univ-paris13.fr/~benmoussa/UML2CPN/`，并说明基于 `Acceleo`、`EMF` 与 `CPN Tools`。
- 标准/格式获取方式：输入承载是基于 `EMF` 的 `UML State Machine` metamodel，输出承载是 `CPN Tools` 的 XML-like concrete syntax；不是中立交换标准。

## 简报

这篇论文的价值不在再发明一种新的 `UML` 形式化语义，而在把已有的 `UML State Machine -> Coloured Petri Net` 规则真正自动化。作者选择 `Acceleo` 不是因为它最强，而是因为 `CPN` 缺少广泛认可的 metamodel，导致传统 model-to-model 路线不方便，最终只能走 `EMF model -> text`，直接吐 `CPN Tools` 可读的 XML-like 语法。

- 形式主义定位：它是 `UML State Machine` 到 `CPN` 的自动桥接基础设施条目，不是新的状态机母型。
- 构造方式简述：`EMF UML metamodel -> Acceleo templates -> CPN Tools concrete syntax -> simulation / verification`。
- 基础设施与场景简述：依托 `EMF`、`Acceleo`、`CPN Tools` 与早先的 `SMD -> CPN` 翻译规则，服务 `UML` 模型的自动 formal-verification bridge。

```text
UML state machine model in EMF -> Acceleo model-to-text templates -> CPN Tools syntax -> CPN analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 非并发 `UML State Machine Diagram (SMD)`。
2. `EMF` 下的 `UML` 状态机 metamodel。
3. `Acceleo` 模板化 model-to-text transformation。
4. `CPN Tools` 的 XML-like concrete syntax。

### 核心抽象

虽然论文没有像理论母文那样给出完整元组，但其桥接关系可以保守整理为：

$$
\mathcal{T}_{A} : SMD_{EMF} \to CPN_{xml}
$$

上式中的符号逐项解释如下：

1. `$SMD_{EMF}$` 表示在 `EMF` metamodel 下编码的 `UML State Machine Diagram`。
2. `$CPN_{xml}$` 表示 `CPN Tools` 的 XML-like concrete syntax。
3. `$\mathcal{T}_{A}$` 表示本文通过 `Acceleo` 实现的自动翻译。
4. 该翻译不是抽象语义映射，而是直接生成目标工具可读文本。

论文对 source metamodel 的核心对象做了明确说明，可保守整理为：

$$
M_{UML} = (\text{StateMachine}, \text{State}, \text{Transition}, \text{Behaviour}, \text{HistoryState}, \text{InputArc}, \text{OutputArc})
$$

上式中的符号逐项解释如下：

1. `StateMachine` 是全局状态机对象。
2. `State` 与 `FinalState` 描述状态节点。
3. `Transition` 描述迁移。
4. `Behaviour` 描述 `do/entry/exit` 等行为。
5. `HistoryState` 描述 history pseudostate。
6. `InputArc` 与 `OutputArc` 描述状态和迁移之间的连接关系。

翻译骨架则可压成三类映射规则：

$$
\text{state} \mapsto \text{place},\qquad \text{behaviour} \mapsto \text{transition},\qquad \text{SMD transition} \mapsto \text{CPN subnet}
$$

上式中的符号逐项解释如下：

1. `UML` state 通常被映射为 `CPN` place。
2. `entry/exit/do` 等 behaviour 被映射为 `CPN` transition。
3. 一条 `SMD` transition 往往不是一条简单弧，而是一个小型 `CPN` 结构。
4. 这说明本文关注的是工具落地，而不是最小化抽象编码。

### 一个最小例子与通俗解释

论文用 CD player 状态机举例：

1. `BUSY`、`NONPLAYING` 等 composite states 作为 `SMD` 结构骨架。
2. `PLAYING` 带 `do` behavior，`BUSY` 带 history pseudostate。
3. 翻译后这些对象会变成 `CPN` 中的 places、transitions 和附加结构。
4. 最终生成的 `CPN` 可以直接交给 `CPN Tools` 仿真或验证。

通俗地说，这篇论文解决的是“别再人工照着论文规则把 UML 图抄成 CPN 了，能不能直接从建模工具里的 UML 模型自动吐出 CPN Tools 文件”。答案是可以，但 `Acceleo` 在工程上并不好用。

### 运行 / 接受 / 转移语义

论文强调的是自动生成而不是重新定义完整语义，但其工具链语义可以概括为：

$$
SMD \xrightarrow{\mathcal{T}_{A}} CPN \xrightarrow{\text{CPN Tools}} \text{simulation / verification}
$$

上式中的符号逐项解释如下：

1. `$SMD$` 是输入的 `UML` 状态机。
2. `$\mathcal{T}_{A}$` 是 `Acceleo` 自动翻译。
3. `$CPN$` 是输出的有色 Petri 网模型。
4. `CPN Tools` 负责后续仿真与验证。

对于 `Acceleo` 自身，论文给出的关键限制也可以保守压成：

$$
\text{templates only output text}
$$

上式中的符号逐项解释如下：

1. `Acceleo` 的 template 更像文本生成器，而不是普通函数。
2. 没有全局变量、用户自定义函数和复杂数据结构。
3. 因此很多中间结果无法缓存，只能重复扫描模型。
4. 这直接导致部分模板出现指数级循环和可维护性问题。

### 语义边界

1. 本文只处理 non-concurrent `UML` state machines。
2. 原始翻译规则中的 history-state 相关算法在实现里没有完整完成。
3. 输出高度依赖 `CPN Tools` concrete syntax，一旦目标语法变化，模板要大改。
4. 因而它更像一条“可用但脆弱”的工程桥接，而不是稳定中间标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 自动翻译关系 | `$\mathcal{T}_{A} : SMD_{EMF} \to CPN_{xml}$` | 从 `EMF`-based UML 直接生成 `CPN Tools` 文本。 |
| source metamodel | `$M_{UML} = (\text{StateMachine}, \text{State}, \ldots)$` | 说明 bridge 的输入骨架来自精简过的 `UML` metamodel。 |
| 核心映射 | `state \mapsto place`，`behaviour \mapsto transition` | 翻译不是一对一拷贝，而是结构化映射。 |
| 工程限制 | `templates only output text` | `Acceleo` 缺少函数/数据结构导致效率和维护性问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `UML` states 是翻译输入主骨架。 |
| 事件 / 触发 | 很强 | `SMD` transitions 与事件驱动关系都会下沉到 `CPN`。 |
| 守卫 / 数据 | 强支持 | guards、variables、`entry/exit/do` 都在支持范围内。 |
| 层次 | 强支持 | 处理 composite state 与 inter-level transitions。 |
| 并发 / 同步 | 不支持 | 本文显式限定 non-concurrent `SMD`。 |
| 时间约束 | 不支持 | 不是 timed bridge。 |
| 连续动态 / 随机性 | 不支持 | 不在 `UML -> CPN` 实现范围内。 |
| 可执行 / 可验证性 | 很强 | 生成后可直接进入 `CPN Tools` 分析。 |

### 形式化问题与性质

1. 这篇论文的主要贡献是把已有桥接规则做成自动化工具，而不是提出新的形式主义。
2. 它同时暴露了 model-to-text 路线在缺少目标 metamodel 时的现实取舍。
3. 从文库角度看，它是 `UML -> CPN` 桥的基础设施节点。
4. 其负面经验同样重要，因为它说明“没有目标 metamodel”会显著伤害工具可维护性。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 基于 `EMF` 的 `UML` 状态机模型。
2. `State / Transition / Behaviour / HistoryState` 等 source metamodel 元素。
3. `Acceleo` 模板。
4. `CPN Tools` concrete syntax。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `EMF` source metamodel。
2. `Acceleo` 模板代码。
3. `CPN Tools` XML-like 输出文件。
4. 后续 `CPN Tools` 仿真 / 验证接口。

### 交换与互操作

这篇论文最核心的互操作就是：

1. `EMF/UML` 作为上游模型承载。
2. `Acceleo` 作为中间桥。
3. `CPN Tools` 语法作为下游验证承载。

它没有定义中立交换层，反而因为直接输出 concrete syntax 而把维护成本提前暴露出来。

## 配套基础设施

- 建模/编辑工具：`EMF`-based `UML` 建模环境。
- 解析/交换/元模型支持：`EMF` metamodel 与 `Acceleo` 模板。
- 仿真/执行支持：`CPN Tools`。
- 验证/分析支持：生成的 `CPN` 可用 `CPN Tools` 做 simulation / state-space analysis。
- 代码生成/转换支持：`UML2CPN` 自动桥接是论文主体。
- 标准化或社区生态：依赖 `UML`、`EMF`、`Acceleo` 和 `CPN Tools` 四个现成生态的交界处。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 已经使用 `UML State Machine` 建模，但需要借助 `CPN` 工具做形式分析。
2. 想把 `UML` 前端与 `CPN Tools` 验证后端接起来。
3. 模型主要是 non-concurrent `SMD`，并包含 guard、variables、`entry/exit/do` 等要素。

### 需求前提

1. `UML` 模型需要落在论文支持的 non-concurrent 子集。
2. 团队接受通过 `CPN` 作为验证中间模型。
3. 模型可通过 `EMF` 获得结构化访问。
4. 能接受 bridge 对 `CPN Tools` 具体语法的强依赖。

### 不适用或高成本场景

若模型高度并发、需要 timed semantics，或者希望获得长期稳定、易维护的中间标准，这条 `Acceleo` 路线成本会偏高。

## 与相邻形式主义的关系

相对 [formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md](../formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md)，那篇更偏并发 `UML -> CPN` 形式化方法，本文更偏自动化实现与工具经验；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，两者都做 `UML` 到验证后端的桥，但本文选 `CPN Tools` 与 model-to-text，后者选其他验证链路；相对 [a-metamodel-based-execution-framework-for-uml-state-machines/desc.md](../a-metamodel-based-execution-framework-for-uml-state-machines/desc.md)，`BlueState` 更像执行框架，本文是验证桥接工具。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明 `UML State Machine` 的形式化落地不一定非得重新定义语言，可以通过自动桥接走向成熟验证后端。
2. 对 LLM 自动建模来说，这意味着目标语言即使不是最终验证语言，也未必是问题，只要桥接链路够稳。
3. 它还提醒我们，中间表示如果没有清晰 metamodel，后续工具化会明显吃亏。

### 作为目标形式主义还是中间表示

更适合作为 `UML` 的验证中间桥接基础设施，而不是独立目标形式主义。

### 对需求到模型生成的启发

1. 如果最终想接 formal backend，生成的 `UML` 模型必须结构化到足以支持自动遍历和转换。
2. `entry/exit/do`、history、变量等元素如果生成得含糊，会显著影响桥接质量。
3. 目标后端缺 metamodel 时，最好尽早考虑中间层而不是直接耦合 concrete syntax。

### 现实限制

论文自己也明确承认 `Acceleo` 版本的实现维护性一般，因此它更像一个重要的桥接证据，而不是最终推荐的长期技术路线。

## 重要的相关工作

### 奠基或前身工作

- 早先的 non-concurrent `UML State Machines -> CPN` 翻译规则论文。

### 同类型或同家族工作

- [formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md](../formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md)
- [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)

### 标准 / 格式 / 工具链工作

- `EMF`、`Acceleo`、`CPN Tools` 与 `UML2CPN`。

### 与本研究关系最紧的工作

- [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)
- [formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md](../formalising-concurrent-uml-state-machines-using-coloured-petri-nets/desc.md)

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / CPN Tools XML / Acceleo model-to-text bridge`
- 论文角色：`UML` 状态机到 `CPN` 的自动化桥接实现报告 / model-to-text infrastructure
- 核心功能：把 `EMF` 中的 `UML State Machine` 自动翻译成 `CPN Tools` 可分析的 `CPN` 文本。
- 关键特性：`EMF` metamodel、`Acceleo` 模板、`CPN Tools` concrete syntax、`UML2CPN`、non-concurrent 子集。
- 构造方式：`UML model -> Acceleo templates -> CPN Tools XML-like syntax -> CPN analysis`。
- 基础设施：`EMF`、`Acceleo`、`CPN Tools` 与原始 `UML2CPN` 实现。
- 适用场景：需要把 `UML` 前端快速接到 `CPN` 验证后端的软件行为建模任务。
