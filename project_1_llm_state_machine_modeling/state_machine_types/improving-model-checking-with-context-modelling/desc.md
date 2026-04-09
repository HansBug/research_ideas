# 改进模型检查的上下文建模 / Improving Model Checking with Context Modelling

## 基本信息

- 标题：Improving Model Checking with Context Modelling
- 中文标题：改进模型检查的上下文建模
- 作者：Philippe Dhaussy，Frédéric Boniol，Jean-Charles Roger，Luka Leroux
- 发表：*Advances in Software Engineering*，Vol. 2012，Article 547157，pp. 1-13，2012
- DOI：`10.1155/2012/547157`
- 链接：https://doi.org/10.1155/2012/547157
- 形式主义：`CDL / context-aware verification / OBP / Fiacre / observer-based model checking`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：context language + automatic splitting route for observer-based model checking
- 工具/实现获取方式：论文明确给出 `OBP (Observer-based Prover)` 工具链与 `OBP Explorer`，并说明 `CDL` 模型会被自动翻译为 `Fiacre`；正文给出入口 `http://www.obpcdl.org/`。
- 标准/格式获取方式：核心承载对象是 `CDL` 上下文语言、生成的 context graphs、`Fiacre` 自动机、observer automata 与 textual property patterns；它是验证导向中间 DSL，不是行业交换标准。

## 简报

这篇论文真正补的，不是又一种底层状态压缩算法，而是把“环境上下文”从系统模型里显式剥出来，变成可单独建模、自动切分、再逐块验证的第一类对象。作者的核心判断是：很多嵌入式系统的 combinatorial explosion，并不是因为系统本体无法验证，而是因为把所有环境行为一次性并进来后，验证目标被无差别地拉得过宽。

- 形式主义定位：这是围绕 `CDL + context splitting + observer-based verification` 的验证路线，不是新的状态机母型。
- 构造方式简述：先用 `CDL` 单独写环境上下文与属性作用域，再把每个 context graph 与系统组合；若爆炸，就按深度参数递归切成多个 subcontexts。
- 基础设施与场景简述：依托 `CDL`、`OBP`、`Fiacre`、`TINA-SELT`、`OBP Explorer` 与 observer automata，服务大状态空间嵌入式/反应式系统的 focused verification。

```text
system model + CDL context + scoped properties -> context graph(s) -> compose with system -> verify each subcontext -> aggregate verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. system model `S`；
2. context description language `CDL`；
3. context graph / subcontexts；
4. observer automata 与 invariants；
5. `OBP` 主导的递归 splitting and verification procedure。

### 核心抽象

论文把环境上下文建成一类可组合的有限行为对象。结合正文可保守整理为：

$$
C ::= \mathrm{msc} \mid C ; C \mid C \parallel C \mid C [] C
$$

上式中的符号逐项解释如下：

1. `\mathrm{msc}` 表示一个由 sequence diagrams 给出的基本场景片段。
2. `C ; C` 表示顺序组合。
3. `C \parallel C` 表示并行交织。
4. `C [] C` 表示 alternative 选择。
5. 这是对论文中 `seq / par / alt` 三类连接语义的保守符号化整理。

论文的实际验证对象不是裸系统，而是系统与某个上下文组合后的模型：

$$
S \parallel C_i
$$

上式中的符号逐项解释如下：

1. `S` 是待验证系统模型。
2. `C_i` 是某个 context 或 subcontext。
3. `\parallel` 表示论文中的 composition operator。
4. 每个 `C_i` 都对应“环境行为的一个受限片段”。

上下文切分后，整体验证会被改写成多个子问题。论文给出等价性主张，可保守写成：

$$
\mathrm{Verify}(S \parallel C_i,\ pty) \equiv \bigcup_{k=1}^{K_i}\mathrm{Verify}(S \parallel C_{ik},\ pty)
$$

上式中的符号逐项解释如下：

1. `pty` 是绑定到该上下文上的性质集合。
2. `C_i` 是原始上下文。
3. `C_{ik}` 是切分后得到的第 `k` 个 subcontext。
4. `K_i` 是 `C_i` 被切成的 subcontexts 数量。
5. 这里的“等价”表达的是论文所说“先整体组合再验证”和“先切分再逐块验证”对 safety/invariant 场景的等价结果。

### 一个最小例子与通俗解释

可以把这篇论文想成“先把环境剧本写出来，再按剧本局部验证”：

1. 系统是一个嵌入式控制器 `S`。
2. 环境不是无限自由地和它互动，而是先被写成一个 `CDL` 场景 `C`，例如初始化、若干设备登录、再执行某类操作。
3. 某条 requirement 只绑定在这个场景下检查，而不是对所有可能环境都检查。
4. 如果 `S \parallel C` 仍太大，就把 `C` 再切成 `C_1,C_2,\ldots`，逐个验证。

通俗地说，这相当于不再问“系统在所有可能世界里是否正确”，而是先把世界写成有限个工程上真会出现的上下文，再分别检查。

### 运行 / 接受 / 转移语义

论文里的运行语义可以压成以下链路：

1. `CDL` 场景会先被编译成 context graphs。
2. 每个 context graph 再被翻译成 `Fiacre` 自动机。
3. `OBP` 将 system model、context graph 和 properties 组合起来。
4. 若使用 `OBP Explorer`，性质会进一步被生成为 observer automata，并把验证问题转成 reject state reachability。

递归切分过程可保守整理为：

$$
mc(model, context_i, pty, d)
$$

其中：

1. `model` 是被验证系统。
2. `context_i` 是当前上下文。
3. `pty` 是绑定到该上下文上的性质集。
4. `d` 是 splitting depth 参数。
5. 若探索失败，则对 `context_i` 执行 `split(context_i,d)` 并递归处理所得子上下文。

### 语义边界

这篇论文的边界很明确：

1. 它主要针对 finite contexts 与 safety / invariant / bounded-liveness 友好的 observer-style checking。
2. 它不是通用 `CTL/LTL` 全覆盖后端，而是更强调工程上可写、可解释的 scoped properties。
3. `CDL` 更像验证中间语言，不是系统实现语言。
4. 若上下文本身就极度异步且难以形式化，splitting 也可能继续爆炸。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `CDL` 结构骨架 | `$C ::= \mathrm{msc} \mid C ; C \mid C \parallel C \mid C [] C$` | 上下文通过顺序、并行和选择组合场景。 |
| 验证对象 | `$S \parallel C_i$` | 不是裸系统，而是系统与环境上下文的组合。 |
| 递归验证入口 | `$mc(model, context_i, pty, d)$` | 爆炸时按深度参数自动切分上下文。 |
| 切分等价主张 | `$\mathrm{Verify}(S \parallel C_i,pty) \equiv \bigcup_k \mathrm{Verify}(S \parallel C_{ik},pty)$` | 把一个大验证问题改写为多个小验证问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 系统本体可以是自动机/LTS，context 也会落成有限图。 |
| 事件 / 触发 | 很强 | 场景、属性绑定和 observer 全部围绕事件序列。 |
| 守卫 / 数据 | 中等支持 | 通过 predicates / patterns 可表达状态与事件条件，但不是富数据语言。 |
| 层次 | 中等支持 | `CDL` 有三层结构化建模入口。 |
| 并发 / 同步 | 强支持 | context actors 可并行交织，且与系统组合验证。 |
| 时间约束 | 条件支持 | 属性 patterns 支持 timed aspects，但论文主轴是 context reduction。 |
| 连续动态 / 随机性 | 不支持 | 完全围绕离散组合爆炸与 observer-based checking。 |
| 可执行 / 可验证性 | 很强 | `CDL -> Fiacre -> OBP/TINA/OBP Explorer` 工具链完整。 |

### 形式化问题与性质

1. 论文的核心问题是“如何把环境约束显式化并切分”，而不是“如何发明新的 model checker”。
2. 它把 properties 与 contexts 显式绑定，这一点对大系统验证特别重要。
3. 其 reduction 轴有三条：约束 context behavior、聚焦 properties、把 state space 拆成多块。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. system model；
2. `CDL` context diagrams / textual syntax；
3. property patterns、invariants 与 observer properties；
4. 由 `OBP` 生成的 context graphs；
5. 下游 `Fiacre` 与 observer automata。

### 承载格式

机器可处理承载方式包括：

1. `CDL` 图形/文本场景；
2. `Fiacre` 自动机；
3. `SELT` 公式或 observer automata；
4. `LTS` exploration results；
5. context splitting 生成的一组 subcontext graphs。

### 交换与互操作

这条路线的互操作重点在：

1. `CDL` 作为用户视角与 formal backend 之间的中间层；
2. `OBP` 可把 `CDL` 转到 `Fiacre`；
3. 性质可接 `TINA-SELT` 或 `OBP Explorer`；
4. 论文明确提到 `UML/SysML/AADL/SDL` 等标准模型可通过翻译器接到同一链路。

## 配套基础设施

- 建模/编辑工具：`CDL` 图形/文本建模、上下文层次结构与 property patterns。
- 解析/交换/元模型支持：`CDL -> context graphs -> Fiacre` 自动翻译链。
- 仿真/执行支持：`OBP Explorer` 可在组合模型上执行可达性分析。
- 验证/分析支持：context splitting、observer generation、`TINA-SELT` / `OBP Explorer`。
- 代码生成/转换支持：重点是 formal artifacts generation，不是部署代码生成。
- 标准化或社区生态：依附 `OBP/Fiacre` 学术路线；原文没有行业标准化定位。

## 适用场景与需求前提

### 适用场景

适合以下场景：

1. 嵌入式反应式系统，环境交互已知且有限。
2. 系统大到直接全局 model checking 易爆炸，但工程上可以给出 use-case / context。
3. 需要让工程师以接近 `UML` 的方式写环境约束和性质作用域。

### 需求前提

1. 环境行为需要能被整理成有限上下文。
2. 目标性质最好是 safety / bounded-liveness / observer-friendly 的。
3. 团队愿意显式维护 context，而不是把所有环境默认揉进主模型。
4. 翻译到 `Fiacre` / `OBP` 的语义损失必须可接受。

### 不适用或高成本场景

如果环境高度开放、上下文难以界定，或者性质本质上依赖全局开放行为，这条路线就很难获得稳定收益。

## 与相邻形式主义的关系

相对 [partially-bounded-context-aware-verification/desc.md](../partially-bounded-context-aware-verification/desc.md)，那篇把环境 guide 写成更显式的 `xGDL` 文本语言，并把有界性只施加到 guide 侧；这篇则更早地建立了 `CDL + context splitting + observer-based verification` 的总框架。相对 [automatic-verification-of-bpmn-models/desc.md](../automatic-verification-of-bpmn-models/desc.md)，后者把 `BPMN` 业务流程接到 `OBP` 风格验证后端，这篇则更强调 environment contexts 的独立建模。相对 [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)，两者都使用 observers，但本文的中心是 context modelling，而不是 executable-`UML` 运行期闭环。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对博士主线很关键，因为它说明“模型出来以后，验证场景本身也应该是可建模、可拆分、可复用的对象”，而不只是附在需求文档里的自然语言注释。

### 作为目标形式主义还是中间表示

更适合作为 verification-profile / scenario-layer 中间表示，而不是最终交付给工程师的主状态机语言。

### 对需求到模型生成的启发

1. 需求中的“适用上下文”应单独抽取，不要全部塞进主状态机。
2. LLM 后续可以直接生成 `context + property binding`，而不只生成系统模型。
3. 验证爆炸时，修复对象不一定是系统模型，也可能是 context 的切分与重组方式。

### 现实限制

论文自己也承认最难的是方法论层面：上下文到底怎么抽、怎么切，并不是完全自动的。

## 重要的相关工作

1. [partially-bounded-context-aware-verification/desc.md](../partially-bounded-context-aware-verification/desc.md)：`xGDL` 版本的后续 context-aware verification 路线。
2. [model-checking-of-scade-designed-systems/desc.md](../model-checking-of-scade-designed-systems/desc.md)：把同步 DSL 系统接入 `FIACRE + CDL + OBP` 的桥接条目。
3. [automatic-verification-of-bpmn-models/desc.md](../automatic-verification-of-bpmn-models/desc.md)：同一 `OBP`/observer 思路在流程模型上的另一类应用。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`CDL / context-aware verification / OBP / Fiacre / observer-based model checking`
- 论文角色：context language + automatic splitting route for observer-based model checking
- 归类理由：论文的真正贡献是围绕 `CDL`、context graphs、`OBP` 和 observer-based checking 组织一条验证方法路线，主体不在新模型本体，而在可执行的验证中间层与分解流程。
