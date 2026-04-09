# KriQL：用于迁移系统诊断的查询语言 / KriQL: a query language for the diagnosis of transition systems

## 基本信息

- 标题：KriQL: a query language for the diagnosis of transition systems
- 中文标题：KriQL：用于迁移系统诊断的查询语言
- 作者：Khaoula Es-Salhi，Siham Rim Boudaoud，Ciprian Teodorov，Zoé Drey，Vincent Ribaud
- 发表：*15th International Workshop on Automated Verification of Critical Systems (AVOCS'15)*，pp. 151-165，2015
- DOI：原文未给 DOI，当前公开入口以 HAL 版本为主
- 链接：https://hal.science/hal-01203649
- 形式主义：`Labelled Transition Systems / KriQL / OBP / graph-based diagnosis`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：面向 `LTS` witness trace 诊断的 query language、meta-model 与存储后端探索
- 工具/实现获取方式：原文明确把 `KriQL` 集成到 `OBP` 验证环境，并实现了基于 relational database 与 graph database 的 feasibility prototypes；正文未给稳定公开仓库地址。
- 标准/格式获取方式：核心承载不是外部交换标准，而是 `LTS`、`ConfigurationSet / TransitionSet / PathSet / Trail` 元模型，以及 `KriQL` 查询语法与语义。

## 简报

这篇论文补的是“模型检查给了 counterexample 之后，如何继续做结构化诊断”这层基础设施。作者认为仅有 witness trace 还不够，因为 trace 太长、太低层、太依赖工具内部结构，因此提出 `KriQL` 作为专门面向 `LTS` 的查询语言，把配置、转移、路径和折叠后的 trail 都变成可查询对象。

- 形式主义定位：针对 `LTS` 诊断与 trace 理解的查询语言基础设施，而不是新的状态机母型。
- 构造方式简述：`model checking -> LTS + witness trace -> KriQL query -> filtered states / transitions / paths / trails`。
- 基础设施与场景简述：依托 `OBP`、`LTS` graph、meta-model 与关系型/图数据库后端，服务 counterexample diagnosis、trace slicing 和故障解释。

```text
系统验证 -> LTS / witness trace -> KriQL 查询 -> 关键配置 / 关键路径 / 子图 -> 诊断与解释
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Labelled Transition System (LTS)`，作为模型检查探索图。
2. `ConfigurationSet`、`TransitionSet`、`PathSet`、`Trail` 四类核心数据结构。
3. `KriQL` 查询语法与 denotational semantics。
4. `OBP` 环境中的 trace diagnosis 场景。
5. relational / graph database 两类存储后端。

### 核心抽象

从论文语境看，可把底层探索图保守整理为：

$$
L = (C, T, c_0)
$$

上式中的符号逐项解释如下：

1. `$C$` 是 configurations 集合。
2. `$T$ \subseteq C \times C$` 是带标签的迁移集合。
3. `$c_0$` 是初始 configuration。

论文在此之上给出面向 API 的元模型。其语义域骨架可压成：

$$
env_C : Id \to Configuration, \qquad env_T : Id \to Transition
$$

上式中的符号逐项解释如下：

1. `$Id$` 是对象标识符。
2. `$env_C$` 把标识符映到具体 configuration。
3. `$env_T$` 把标识符映到具体 transition。
4. 这说明 `KriQL` 的查询结果并不是裸文本，而是对探索图对象的结构化引用。

论文给出的抽象语法核心可保守整理为：

$$
Query ::= Get\ Key\ where\ Cond \mid Query\ union\ Query \mid Query\ inter\ Query
$$

上式中的符号逐项解释如下：

1. `Key` 指要抽取的对象类型，如 `Configuration`、`Process`、`Component`。
2. `Cond` 是谓词，可由等式、访问、变更和 visited 条件组成。
3. `union` 与 `inter` 允许组合查询结果。
4. 这说明 `KriQL` 不是单一过滤器，而是带集合运算的图查询语言。

对应的核心语义函数，论文直接写成：

$$
Q[[Get\ configuration\ where\ C]](env_C, env_T) = \{ c \in env_C \mid C(c)=\top \}
$$

上式中的符号逐项解释如下：

1. `$Q[[\cdot]]$` 是 query valuation function。
2. `$env_C$` 与 `$env_T$` 是配置与迁移环境。
3. `$C(c)=\top$` 表示 configuration `$c$` 满足谓词。
4. 结果是 configuration 子集，而不是直接输出字符串报表。

### 一个最小例子与通俗解释

论文给了一个很直观的 Alice/Bob 互斥示例。假设模型检查返回了违反互斥性的 trace：

1. `0 -> 1 -> 3 -> 6 -> 9 -> 12`。
2. 诊断者并不想逐字读完整 counterexample。
3. 她只想问：“在出错前后的两个配置里，`flagA` 和 `flagB` 分别是多少？”
4. `KriQL` 就允许把问题缩成针对特定 configuration 和变量视图的结构化查询。

通俗地说，`KriQL` 像是“给 LTS 和 counterexample 装了一层 SQL/graph query 式的诊断接口”，让人不必被整条低层 trace 淹没。

### 运行 / 接受 / 转移语义

这篇论文的重点不是重新定义 `LTS` 运行语义，而是给运行结果添加查询语义。对路径对象，论文把它们区分成：

$$
Path \subseteq T^\ast, \qquad Trail = \mathrm{fold}(Path, filter)
$$

上式中的符号逐项解释如下：

1. `Path` 是有序转移序列。
2. `Trail` 是按查询过滤条件折叠后的路径表示。
3. `fold` 表示只保留诊断真正关心的片段，而不是整条原始路径。
4. 这正是 `KriQL` 用于 trace understanding 的独特价值。

### 语义边界

1. `KriQL` 面向的是已经生成好的 `LTS` 与 traces，不负责替代 model checker 本身。
2. 它假设底层探索图及其设计结构是可访问的，因此不适合完全黑盒的 verifier。
3. 语言主打 diagnosis 与理解，不主打一般图挖掘或通用数据库查询完备性。
4. 原文原型已经显示：不同查询类型对 relational / graph backend 的偏好不同，没有单一后端能在所有查询上都最优。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTS` 骨架 | `$L=(C,T,c_0)$` | 所有查询都建立在探索图之上。 |
| 环境语义域 | `$env_C:Id\to Configuration$` | 查询结果指向结构化配置对象。 |
| 语法骨架 | `$Query ::= Get\ Key\ where\ Cond \mid \cdots$` | 支持对象抽取与集合组合。 |
| 基本查询语义 | `$Q[[Get\ configuration\ where\ C]]=\{c \mid C(c)\}$` | 语言本质上是对探索图对象的选择器。 |
| trail 折叠 | `$Trail=\mathrm{fold}(Path, filter)$` | trace 不必原样阅读，可按诊断意图裁剪。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | configuration 是一等查询对象。 |
| 事件 / 触发 | 中等支持 | transitions 与 visited/changed 条件可被查询。 |
| 守卫 / 数据 | 中等支持 | 可查询变量值变化，但不是 rich theorem proving。 |
| 层次 | 弱支持 | 主要是 process/component 层次，不是状态机层次语义。 |
| 并发 / 同步 | 很强 | 面向 concurrent system 的 `LTS` 诊断而设计。 |
| 时间约束 | 不支持 | 不特化 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散转移系统查询。 |
| 可执行 / 可验证性 | 很强 | 能直接对 model checker 产生的图与 traces 做后处理。 |

### 形式化问题与性质

1. 这篇论文真正解决的是“验证之后的信息利用率”问题，而不是“如何再做一次验证”。
2. `ConfigurationSet / TransitionSet / PathSet / Trail` 的分层设计，说明 trace 诊断不该只是一串文本搜索。
3. 后端实验结果也说明：诊断查询本身就是独立的基础设施问题。

## 构造方式与承载格式

### 建模入口

论文里的典型入口包括：

1. `OBP` 生成的 `LTS`。
2. witness / counterexample trace。
3. system 的 design structure。
4. 用户编写的 `KriQL` 查询。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `ConfigurationSet`。
2. `TransitionSet`。
3. `PathSet`。
4. `Trail`。
5. process / component / variable 级别的结构化字段。

### 交换与互操作

1. `KriQL` 不是通用数据库标准，而是针对 `LTS` 诊断的专用前端语言。
2. 它依赖设计结构与探索图之间的可追溯关系。
3. 其实现层已探索 relational 与 graph DB 两条路线，说明它适合作为诊断层而非验证核心层。

## 配套基础设施

- 建模/编辑工具：原文依托 `OBP` 验证环境，而不是新的状态机编辑器。
- 解析/交换/元模型支持：`ConfigurationSet / TransitionSet / PathSet / Trail` 元模型与相应语义域。
- 仿真/执行支持：主线不是执行器，而是对已生成 traces 的查询与切片。
- 验证/分析支持：可查询 configuration、路径存在性、路径计算、set construction 与 side-effect restrictions。
- 代码生成/转换支持：没有部署代码生成；转换重点在 `LTS -> database representation -> query results`。
- 标准化或社区生态：原文没有把 `KriQL` 发展成通用标准，而是把它定位为 `OBP` 周边的 diagnosis kernel language。

## 适用场景与需求前提

### 适用场景

适合 counterexample 过长、配置过多、变量视图复杂、需要交互式缩小诊断范围的模型检查后处理场景。

### 需求前提

1. 底层验证器需要能暴露 `LTS`，而不是只给一句 yes/no。
2. trace 必须可追溯到 process、component、variable 等设计结构。
3. 诊断目标应适合表达为配置过滤、变量变化、路径搜索或子图抽取。
4. 团队愿意把 diagnosis 看成独立的工程层，而不只靠人工读 counterexample。

### 不适用或高成本场景

1. 若 verifier 完全不暴露内部图结构，`KriQL` 无法发挥作用。
2. 对非常小的 traces，引入专门查询语言可能收益有限。
3. 若目标是通用图分析而不是 verification diagnosis，`KriQL` 的专用语义会显得过窄。

## 与相邻形式主义的关系

相对 [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)，`SPIN` 负责生产 counterexample，而 `KriQL` 关注 counterexample 之后怎么读懂它；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`LTSmin` 解决高性能探索，`KriQL` 解决探索结果的诊断利用；相对 [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)，observer 路线负责把性质压入模型，而 `KriQL` 负责在性质失败后对 witness trace 做结构化查询。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对博士主线尤其重要，因为你的研究不只需要“生成模型”和“验证结果”，还需要“把失败解释给修复环节”。`KriQL` 正好补了这层：

1. 它把 counterexample 解释问题明确转成查询问题。
2. 它说明单纯拿到 witness trace 还不够，必须有可交互的结构化诊断层。
3. 这正好对应后续 `project_4_iterative_model_repair` 所需要的 defect localization 入口。

### 可借鉴点

1. 可把 LLM 生成的修复问题描述转换成对 witness/LTS 的结构化查询模板。
2. 在验证剖面生成中，可预先设计需要回收哪些 configuration/path 片段，减少人工定位成本。
3. 对状态机建模研究来说，`Trail` 这类折叠表示很适合做“人可读但又保留因果”的解释层。

### 局限与注意事项

1. 它处理的是诊断层，不是模型本体定义层。
2. 原型后端性能仍不均衡，说明工程化还需专门的存储设计。
3. 若目标是自动修复，还需要在 `KriQL` 之上再加 root-cause inference 和 patch generation。

## 重要的相关工作

1. [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)：经典 model checker，与 `KriQL` 的“验证后诊断层”形成分工。
2. [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)：语言无关状态空间后端，说明 `KriQL` 这类诊断接口可附着在更通用探索器之后。
3. [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)：展示性质失败时对状态与观察器配置做结构化定位的另一类思路。

## 文献分类总结

- 这是一篇 `📦 标准、交换格式、元模型与执行载体` 条目，因为它提供的是 `LTS` 诊断层的可复用语言与元模型基础设施。
- 这是一篇 `🏗️ 标准/基础设施` 条目，而不是单纯 `🛠️ 方法路线`，因为重点是 `KriQL` 语言、对象模型与后端实现框架。
- 它描述的核心对象是 `🎛️ 控制 / 反应式逻辑`，因为被查询的仍是系统行为图及其 witness traces。
- 它应挂在 `LTS diagnostic-query infrastructure / OBP explanation workflow` 的静态挂接口径下，为后续 trace explanation 和模型修复提供中间层依据。
