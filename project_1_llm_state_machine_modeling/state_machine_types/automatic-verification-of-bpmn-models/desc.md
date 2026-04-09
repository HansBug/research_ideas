# BPMN 模型的自动验证 / Automatic Verification of BPMN Models

## 基本信息

- 标题：Automatic Verification of BPMN Models
- 中文标题：BPMN 模型的自动验证
- 作者：Mihal Brumbulli，Emmanuel Gaudin，Ciprian Teodorov
- 发表：*10th European Congress on Embedded Real Time Software and Systems (ERTS 2020)*，2020
- DOI：原文未给 DOI，当前公开入口以 HAL 版本为主
- 链接：https://hal.science/hal-02441878
- 形式主义：`BPMN / OBP / PSC / GPSL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：BPMN executor and OBP verification bridge / semantics-driven workflow verification infrastructure
- 工具/实现获取方式：原文明确给出 `VeriMoB` 项目中的 BPMN executor 与 `OBP` 集成路线，并在参考文献中给出 `OBP2` 入口 `http://www.obpcdl.org/`；正文未给完整公开仓库。
- 标准/格式获取方式：主承载对象是 `BPMN`、`PSC`、`GPSL`、LTL/Büchi automata 和 `OBP` API；其中 `BPMN` 是标准化建模语言，其余部分属于验证工作流基础设施。

## 简报

这篇论文补的是 `BPMN` 线里非常有代表性的验证基础设施：不是把 `BPMN` 转一次、再证明转换语义正确，而是直接用同一个 BPMN executor 负责交互执行和模型检查接口，让 `OBP` 做与语义无关的探索与性质验证。这样 counterexample 也能直接回到 BPMN 概念层重放，而不是先掉进另一个中间模型。

- 形式主义定位：`BPMN` 的执行与验证桥接基础设施，不是新的 workflow 语言本体。
- 构造方式简述：`BPMN` executor 暴露统一 API 给 `OBP`，属性侧则用 `PSC / GPSL / LTL / Büchi` 描述，再由 `OBP` 驱动状态空间探索。
- 基础设施与场景简述：依托 `BPMN`、`OBP`、`PSC`、`GPSL` 和统一执行语义，服务业务过程、任务协同和复杂组织流程的自动验证。

```text
BPMN model -> BPMN executor -> OBP API -> GPSL / LTL / Büchi property -> exploration / counterexample replay
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. BPMN execution states；
2. BPMN executor；
3. `OBP` semantics-agnostic model checking；
4. `PSC` property language；
5. `GPSL` propositional / Büchi / LTL layers。

### 核心抽象

论文首先给出单个 BPMN element 的执行状态集合，可直接整理为：

$$
\Sigma_{exec} = \{\mathrm{None}, \mathrm{Active}, \mathrm{Ready}, \mathrm{Enabled}, \mathrm{Disabled}\}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{None}$` 表示元素从未启用且当前不接受动作。
2. `$\mathrm{Active}$` 表示元素正在等待 enable/disable 动作。
3. `$\mathrm{Ready}$` 表示用户已请求启用，但依赖条件尚未满足。
4. `$\mathrm{Enabled}$` 表示启用条件全部满足。
5. `$\mathrm{Disabled}$` 表示该元素被显式禁用。

论文说明“当前 execution state of a BPMN model 由所有元素的 execution states 组成”。可保守整理为：

$$
G = \prod_{e \in E} State_e
$$

上式中的符号逐项解释如下：

1. `$E$` 是 BPMN 模型中的元素集合。
2. `$State_e$` 是元素 `$e$` 当前持有的执行状态信息。
3. 这是根据原文执行器描述做的保守抽象，不是论文直接给出的单行元组。
4. `OBP` 通过 get/set state、枚举下一步、执行一步来操纵这个全局状态。

在属性层，论文给出 `GPSL` 的 automaton 语法。可压成标准 Büchi 风格对象：

$$
\mathcal B = (S,S_{init},S_{acc},\Delta)
$$

上式中的符号逐项解释如下：

1. `$S$` 是 automaton states。
2. `$S_{init}$` 是初始状态集。
3. `$S_{acc}$` 是接受状态集。
4. `$\Delta \subseteq S \times Expr \times S$` 是带布尔 guard 的迁移。
5. 这正对应原文 `states / initial / accept / transition` 四段式定义。

论文对单条 transition 给出的语法是：

$$
\text{transition} := s[\phi]s'
$$

上式中的符号逐项解释如下：

1. `$s,s' \in S$` 是源状态与目标状态。
2. `$\phi$` 是由 atomic propositions 与 propositional operators 组成的布尔表达式。
3. atomic proposition 的真假由 BPMN executor 负责解释，而不是由 `OBP` 内部固定。

在案例部分，作者给出一个很典型的 BPMN 性质：

$$
\Diamond P \rightarrow ((\neg P)\ U\ S) \land ((\neg P)\ U\ T)
$$

上式中的符号逐项解释如下：

1. `$S$` 表示 “Describe situation” 已经 enable。
2. `$T$` 表示 “Describe target” 已经 enable。
3. `$P$` 表示 “Authorize fire” 变为 active。
4. 该性质表达“若最终能够授权开火，则此前必须先完成态势和目标描述”。

### 一个最小例子与通俗解释

论文给的 client-server 例子很适合做最小解释：

1. client 向 server 发出 request。
2. 一个简单的 `PSC` 要求：只要发过 request，后面就必须有 answer。
3. 该 `PSC` 被翻译成一个只有 `S1/S3/S4` 三个状态的 Büchi automaton。
4. `OBP` 在探索 BPMN 执行时同步跑这台 property automaton，于是可以直接判断是否违反要求。

通俗地说，这个框架不是先把 BPMN 改写成另一种验证模型，而是让 BPMN 自己负责“下一步能做什么”，让 `OBP` 只负责“沿着这些合法步探索并监控性质是否被破坏”。

### 运行 / 接受 / 转移语义

论文的关键运行语义是 semantics-driven，而不是 transformation-driven：

1. `OBP` 不直接加载 BPMN 模型。
2. `OBP` 通过 API 让执行器返回全局状态、设置状态、枚举可执行步、执行一步。
3. `PSC/GPSL/LTL/Büchi` 里的 atomic propositions 也交由执行器解释。
4. 因而交互执行、trace replay 和 model checking 共用同一 BPMN semantics。

这种架构的直接收益是：

1. 无需再证明 “BPMN -> 中间模型” 的语义等价。
2. 反例天然仍是 BPMN 概念层的动作序列。
3. 诊断时可由 executor 直接重放 counterexample。

### 语义边界

1. 论文重点是语义统一的执行/验证架构，不是 BPMN 全语法的形式定义论文。
2. 为避免无限状态空间，原文对 loops 采用“一次迭代足以覆盖结构场景”的限制性处理。
3. 对 empty pool collaboration 场景，未接收消息数需要设定上界。
4. 许多路径条件仍来自自然语言业务条件，这部分不会被框架自动消解。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| element execution states | `$\Sigma_{exec}=\{\mathrm{None},\mathrm{Active},\mathrm{Ready},\mathrm{Enabled},\mathrm{Disabled}\}$` | BPMN executor 对单元素状态的核心抽象。 |
| model global state | `$G=\prod_{e \in E} State_e$` | 整个 BPMN 执行配置由各元素状态组成。 |
| property automaton | `$\mathcal B=(S,S_{init},S_{acc},\Delta)$` | `GPSL` 的 Büchi 层骨架。 |
| transition syntax | `$\text{transition}:=s[\phi]s'$` | `GPSL` guard transition 的统一写法。 |
| 样例性质 | `$\Diamond P \rightarrow ((\neg P)\ U\ S) \land ((\neg P)\ U\ T)$` | CAS 模型中的依赖先决条件验证。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 每个 BPMN 元素都有显式执行状态。 |
| 事件 / 触发 | 很强 | enable/disable actions 和消息事件是执行主轴。 |
| 守卫 / 数据 | 中等 | 路径条件常来自自然语言，数据不是本文主轴。 |
| 层次 | 中等 | BPMN 可有 call activities，但本文重点不是层次语义本体。 |
| 并发 / 同步 | 很强 | gateways、message flows 和多 participant 协同是核心。 |
| 时间约束 | 弱支持 | 不是 timed-BPMN 论文，重点在语义驱动验证。 |
| 连续动态 / 随机性 | 不支持 | 纯离散流程执行语义。 |
| 可执行 / 可验证性 | 很强 | executor、trace replay、`OBP`、`PSC/GPSL` 已打通。 |

### 形式化问题与性质

1. 论文真正补的是 “同一语义如何同时服务交互执行与模型检查”。
2. 它把 `BPMN` 从“可视流程图”推进到“可探索、可验证、可回放”的执行对象。
3. `PSC -> GPSL/Büchi` 让非时序逻辑专家也能较自然地表达性质。
4. 对文库来说，这是 workflow/BPMN 线很关键的验证基础设施证据。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `BPMN` process model；
2. BPMN executor；
3. `PSC` 或 `GPSL/LTL` 性质；
4. `OBP` exploration API。

### 机器可处理承载方式

机器可处理承载方式包括：

1. BPMN 元素执行状态；
2. BPMN executor 全局状态；
3. `GPSL` 命题、Büchi automaton 与 `LTL`；
4. `PSC` 到 Büchi 的翻译结果。

### 交换与互操作

互操作重点在：

1. `OBP` 不依赖具体语言语义；
2. BPMN executor 通过统一 API 暴露语义；
3. `PSC/GPSL` 作为性质层对接 BPMN 事件与状态。

## 配套基础设施

- 建模/编辑工具：BPMN editor / executor 与 `VeriMoB` 工作流。
- 解析/交换/元模型支持：`BPMN`、`PSC`、`GPSL`、LTL、Büchi automata。
- 仿真/执行支持：交互式执行、trace simulation、counterexample replay。
- 验证/分析支持：`OBP` 模型检查、状态空间探索、性质验证。
- 代码生成/转换支持：重点不是部署代码生成，而是 executor-driven verification bridge。
- 标准化或社区生态：依托 `BPMN` 标准、`OBP` 平台与 `PSC/GPSL` property stack。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 业务过程与任务协同流程验证；
2. 需要把模型执行、trace replay 和 model checking 统一到一套语义中的场景；
3. stakeholders 更熟悉流程图而不熟悉时序逻辑的项目。

### 需求前提

1. 流程需能稳定表示为 BPMN。
2. 关键流程语义要由可执行 BPMN executor 给出。
3. 性质最好能写成 `PSC` 或 `GPSL/LTL`。
4. 对 loops、空池消息等潜在无限状态源需要有额外约束。

### 不适用或高成本场景

若业务核心依赖复杂数据域、无界消息累积或高精度时间/概率语义，仅靠本文架构还不够，需要进一步限制或扩展执行器语义。

## 与相邻形式主义的关系

相对 [business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md](../business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md)，本文不是 `BPMN -> Timed Automata` 映射，而是直接保留 BPMN 执行语义接入 `OBP`；相对 [kriql-a-query-language-for-the-diagnosis-of-transition-systems/desc.md](../kriql-a-query-language-for-the-diagnosis-of-transition-systems/desc.md)，二者都依托 `OBP`，但本文更前置于模型执行与性质验证，后者更偏 counterexample 诊断；相对 [model-checking-of-scade-designed-systems/desc.md](../model-checking-of-scade-designed-systems/desc.md)，两者都在做“前端 DSL / 执行器 -> `OBP`”桥接，只是前端一个是 `BPMN`，一个是 `SCADE/Lustre`。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明流程/任务语言也可以通过统一 executor 语义接入形式验证，而不一定必须完全重写成另一门状态机语言。
2. 这对“需求到模型”链条很有启发：中间表示不一定非要一次到位，也可以先有稳定执行语义。
3. `PSC/GPSL` 这类面向属性表达的外层语言，也能为后续 verification scenario generation 提供参考。

### 作为目标形式主义还是中间表示

它更像工作流/BPMN 线的执行与验证基础设施，而不是单独的状态机母型。

### 对需求到模型生成的启发

1. 如果前端需求语言已有稳定执行器，优先复用执行语义往往比再造转换器更稳。
2. 性质语言应尽量与领域用户的表达习惯接近，再逐步降到 `LTL/Büchi`。
3. 反例回放能力对后续模型修复非常重要。

## 重要的相关工作

1. [business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md](../business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md)：同样面向 `BPMN` 验证，但采用 `BPMN -> TA-network` 路线。
2. [kriql-a-query-language-for-the-diagnosis-of-transition-systems/desc.md](../kriql-a-query-language-for-the-diagnosis-of-transition-systems/desc.md)：`OBP` 生态中的后续诊断查询层。
3. [model-checking-of-scade-designed-systems/desc.md](../model-checking-of-scade-designed-systems/desc.md)：另一条 DSL/executor 到 `OBP` 的验证桥接路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`BPMN / OBP / PSC / GPSL`
- 论文角色：BPMN executor and OBP verification bridge / semantics-driven workflow verification infrastructure
- 归类理由：论文主体价值在于 BPMN 执行器、性质语言和 `OBP` 间的统一验证基础设施，而不是 BPMN 语言本体的新定义。
