# 用观察者自动机验证和监控 UML 模型：一种无转换方法 / Verifying and Monitoring UML Models with Observer Automata: A Transformation-Free Approach

## 基本信息

- 标题：Verifying and Monitoring UML Models with Observer Automata: A Transformation-Free Approach
- 中文标题：用观察者自动机验证和监控 UML 模型：一种无转换方法
- 作者：Valentin Besnard，Ciprian Teodorov，Frédéric Jouault，Matthias Brun，Philippe Dhaussy
- 发表：*2019 ACM/IEEE 22nd International Conference on Model Driven Engineering Languages and Systems (MODELS)*，pp. 161-171，2019
- DOI：`10.1109/MODELS.2019.000-5`
- 链接：https://hal.science/hal-02433749v1/file/besnard2019.pdf
- 形式主义：`UML observer automata / OBP2 / executable UML monitoring`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：UML verification-and-monitoring bridge / synchronous observer-automata workflow
- 工具/实现获取方式：原文明确给出 `OBP2` 模型检查器入口 `https://plug-obp.github.io/`，并说明方法建立在已有 `EMI`/UML model interpreter 之上，可部署到 `STM32` discovery board 做 runtime monitoring。
- 标准/格式获取方式：主要承载方式是 `UML` 模型、`UML` 状态机形式的 observer automata、解释器 action language 宏、同步组合组件与 `LTL` invariants；原文不强调独立交换标准。

## 简报

这篇论文的核心贡献，是把 `UML` 里的 observer automata 做成“验证期和运行期共用”的同一套资产。作者不再走“先把 LTL 变成 monitor，再为目标平台单独生成另一份 runtime monitor”的路线，而是直接把 system requirements 写成 `UML` observer automata，同步组合到模型执行里，既可用 `OBP2` 做 reachability-based verification，也可在嵌入式目标板上原样跑 runtime monitoring。

- 形式主义定位：`UML` 解释执行与 observer-based verification/monitoring 方法路线，而不是新的状态机本体。
- 构造方式简述：把系统模型和 observer automata 都写成 `UML` 状态机，通过同步组合在每一步执行时同时推进 system 与 observers。
- 基础设施与场景简述：依托 `EMI`、`OBP2`、UML action language 宏和 `STM32` 部署链，服务嵌入式 `UML` 模型的统一验证与监控。

```text
UML system model + UML observer automata -> synchronous composition -> OBP2 reachability check / STM32 runtime monitoring
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织方法：

1. `UML System Model`；
2. `UML Observer Automata`；
3. synchronous composition；
4. `OBP2` model checker；
5. runtime `Sequencer`；
6. `fail` states 与 monitor assertions。

### 核心抽象

结合论文表述，可把单个 observer automaton 保守整理为：

$$
O = (Q, q_0, \Sigma, \delta, F_{fail})
$$

上式中的符号逐项解释如下：

1. `$Q$` 是 observer 的离散状态集合。
2. `$q_0$` 是初始状态。
3. `$\Sigma$` 是 observer 可观察到的系统事件与状态谓词。
4. `$\delta$` 是由 UML state machine guards/effects 诱导的转移关系。
5. `$F_{fail}$` 是用户显式标记的失败状态集合。
6. 这是对论文中 UML observer automata 结构的保守符号化整理。

论文的关键思想是把 observer 与系统同步推进。可保守写成：

$$
(m, o) \xrightarrow{\tau} (m', o') \iff m \xrightarrow{\tau} m' \land o \xrightarrow{\tau} o'
$$

上式中的符号逐项解释如下：

1. `$m$` 和 `$m'$` 是系统模型在执行前后的配置。
2. `$o$` 和 `$o'$` 是 observer 在执行前后的配置。
3. `$\tau$` 表示当前被执行的系统步。
4. 同步组合要求系统步发生时，observer 也沿兼容转移前进。
5. 论文特别强调 observer 必须 deterministic 且 complete，避免阻塞系统执行。

论文还明确把安全验证收束成 reachability 问题。可写成：

$$
\exists (m, o): o \in F_{fail}
$$

上式中的符号逐项解释如下：

1. `$(m,o)$` 是同步组合系统的某个可达配置。
2. `$o \in F_{fail}$` 表示至少一个 observer 到达失败状态。
3. 因而验证任务从一般性质检查收束成“是否可达 fail”。

### 一个最小例子与通俗解释

论文中的 cruise control interface 给了一个很直观的例子。第三条需求可写成：

$$
[]\ (|ccsEngaged| \rightarrow \neg |unknownCS|)
$$

上式中的符号逐项解释如下：

1. `|ccsEngaged|` 表示巡航控制当前处于 engaged 状态。
2. `|unknownCS|` 表示 cruise speed manager 处于未定义速度状态。
3. 性质要求：只要系统还处于 engaged，就不应该看到未知速度。

通俗地说，observer automaton 就像一个“跟着系统一起跑的看门员”。系统每迈一步，它也迈一步；如果它观察到某种绝不该发生的状态组合，就立刻进入 `fail`。

### 运行 / 接受 / 转移语义

论文强调 observer automata 必须 deterministic 且 complete。可压成：

$$
\forall q \in Q,\ \forall \tau,\ \exists !\ q' \in Q:\ q \xrightarrow{\tau} q'
$$

上式中的符号逐项解释如下：

1. `$q$` 是 observer 当前状态。
2. `$\tau$` 是当前系统步对应的可观察执行条件。
3. `$\exists !$` 表示恰有一个可走后继。
4. 这保证 observer 不引入额外非确定性，也不会卡住系统执行。

论文还给出运行期开销估计：

$$
\mathrm{overhead} \approx 6.5 + \frac{100}{nb\_ao}\sum_{i=1}^{N} \frac{nb\_outgoings_i}{nb\_states_i}
$$

上式中的符号逐项解释如下：

1. `nb_ao` 是系统中的 active objects 数量。
2. `$N$` 是 observer 数量。
3. `nb_outgoings_i` 是第 `i` 个 observer 的总 outgoing transitions 数。
4. `nb_states_i` 是第 `i` 个 observer 的状态数。
5. 该式用于估计 runtime monitoring 引入的执行时间开销。

### 语义边界

这篇论文的边界主要有：

1. observer automata 主要表达 safety properties。
2. 方法依赖可执行 `UML` 子集与统一解释器语义。
3. observer 只能观察系统，不应主动向系统发送/接收业务事件。
4. 同步组合不是标准 UML 语义的一部分，而是解释器层的扩展机制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| observer 骨架 | `$O = (Q, q_0, \Sigma, \delta, F_{fail})$` | 说明 UML observer automata 的最小结构。 |
| 同步组合 | `$(m, o) \xrightarrow{\tau} (m', o')$` | 系统与 observer 如何共同推进。 |
| fail reachability | `$\exists (m, o): o \in F_{fail}$` | 安全验证被化约为可达性检查。 |
| 运行期开销 | `$\mathrm{overhead} \approx 6.5 + \frac{100}{nb\_ao}\sum \frac{nb\_outgoings_i}{nb\_states_i}$` | 论文对 monitoring overhead 的经验模型。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 系统和 observer 都落成 UML state machine。 |
| 事件 / 触发 | 很强 | observer 通过事件与状态谓词跟踪系统执行。 |
| 守卫 / 数据 | 强支持 | action language 宏可访问对象属性、事件池与状态。 |
| 层次 | 条件支持 | 依赖 UML state machine 子集，不追求 UML 全语义。 |
| 并发 / 同步 | 强支持 | 同步组合是论文主轴。 |
| 时间约束 | 弱支持 | 主线不在 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 论文完全围绕离散执行与监控。 |
| 可执行 / 可验证性 | 很强 | 同一 observer 既能用于 `OBP2` 验证，也能部署到 `STM32` 监控。 |

### 形式化问题与性质

1. 论文真正补的是“observer 不再只在验证期存在”，而是被做成验证与监控共用资产。
2. 它把传统 `LTL -> monitor -> codegen` 双重转换路线，压缩成统一解释执行语义。
3. 对本文库而言，它是 `UML interpreter` 母线上非常关键的 verification/monitoring bridge。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 使用 `UML` 设计系统模型。
2. 再用 `UML` 状态机写 observer automata。
3. 用 action language 宏访问系统对象、属性和状态。
4. 通过同步组合执行并交给 `OBP2` 或 runtime sequencer。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML` classes / active classes / state machines；
2. observer composite root `Obs`；
3. action language 宏，如 `IS_IN_STATE`、`GET_ACTIVE_PEER`、`OBSERVER_FAIL`；
4. synchronous composition component 与 execution environment。

### 交换与互操作

这篇论文的互操作重点不在中立文件标准，而在统一执行语义：

1. 同一 UML 模型可被解释器直接执行。
2. 同一 observer automata 可被 `OBP2` 验证也可被目标板监控。
3. 不再需要“验证期 monitor”和“运行期 monitor”两套不同资产。

## 配套基础设施

- 建模/编辑工具：`UML` 建模环境与 active-class/state-machine 子集。
- 解析/交换/元模型支持：解释器 action language、对象访问宏与同步组合组件。
- 仿真/执行支持：`EMI`/execution environment、sequencer、`STM32` 部署。
- 验证/分析支持：`OBP2` reachability checking、observer fail-state assertions、LTL 对照验证。
- 代码生成/转换支持：重点不是代码生成，而是 transformation-free deployment of monitors。
- 标准化或社区生态：依托 `UML`、`OBP2` 与作者持续维护的 UML interpreter/monitoring 路线。

## 适用场景与需求前提

### 适用场景

适合想在可执行 `UML` 模型上统一完成设计期验证和运行期监控的嵌入式系统、反应式软件和带明确状态逻辑的控制接口。

### 需求前提

1. 系统模型已经落在可执行 `UML` 子集内。
2. 需求主要是 safety-oriented，可写成 observer fail-state 逻辑。
3. 团队接受解释执行和同步组合，而不是纯翻译到外部后端。
4. 目标硬件能承受一定监控开销。

### 不适用或高成本场景

如果需求主要是 liveness、概率、连续时间或高维连续动态，这条 observer-automata 路线就需要额外后端补强。

## 与相邻形式主义的关系

相对 [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)，本文把同一解释器母线进一步推进到 observer-based verification/monitoring；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，后者更偏设计到运行时桥接，本文更强调 requirements-as-observers；相对 [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)，那篇更偏 deployment modularity，本文更聚焦 fail-state based verification/monitoring unification。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常贴近 `project_1` 的目标，因为它展示了状态机生成后如何直接承接 verification 和 runtime monitoring。
2. 若未来 LLM 生成的是 `UML` 或可执行 statechart 子集，这篇论文说明“性质”可以不必总写成外部逻辑公式，也可以落成同语言 observer。
3. 这对“生成-验证-修复”闭环尤其重要，因为 counterexample 与 runtime violation 都仍然保留在同一建模语言里。

### 作为目标形式主义还是中间表示

它更像 `UML` 状态机生态上的验证/监控方法路线和工具桥，而不是新的目标形式主义。

## 重要的相关工作

1. [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)：统一解释器语义上的 `LTL` 验证桥。
2. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：同一路线的 design/runtime bridge。
3. [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)：更偏 deployment architecture 的后续扩展。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML observer automata / OBP2 / executable UML monitoring`
- 论文角色：UML verification-and-monitoring bridge / synchronous observer-automata workflow
- 归类理由：论文主体在讲如何用同一套 `UML` observer automata 贯通验证与监控，核心贡献落在方法与执行桥，而非新的状态机本体。
