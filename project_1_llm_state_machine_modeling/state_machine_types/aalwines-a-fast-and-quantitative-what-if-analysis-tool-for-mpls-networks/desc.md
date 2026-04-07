# AalWiNes：面向 MPLS 网络的快速定量假设分析工具 / AalWiNes: A Fast and Quantitative What-If Analysis Tool for MPLS Networks

## 基本信息

- 标题：AalWiNes: A Fast and Quantitative What-If Analysis Tool for MPLS Networks
- 中文标题：AalWiNes：面向 MPLS 网络的快速定量假设分析工具
- 作者：Peter Gjøl Jensen，Dan Kristiansen，Stefan Schmid，Morten Konggaard Schou，Bernhard Clemens Schrenk，Jiří Srba
- 发表：*Proceedings of the 16th International Conference on emerging Networking EXperiments and Technologies*，pp. 474-481，2020
- DOI：`10.1145/3386367.3431308`
- 链接：https://doi.org/10.1145/3386367.3431308
- 形式主义：`MPLS network / weighted pushdown automata / AalWiNes`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：quantitative network-verification infrastructure based on weighted pushdown automata
- 工具/实现获取方式：原文明确说明 `AalWiNes` 公开开源，并给出项目入口 `https://github.com/DEIS-Tools/AalWiNes`。
- 标准/格式获取方式：主承载是网络 topology XML、router forwarding tables、`MPLS` header-stack semantics、query language 与最小 witness 规范；它不是行业中立交换标准。

## 简报

这篇论文补的是一个很有代表性的“自动机理论后端真正进入网络验证”的基础设施条目。`AalWiNes` 并不是泛泛谈 `MPLS` 策略检查，而是把真实 dataplane forwarding tables、link failures、header rewrites 和 quantitative witness 搜索统一压到 weighted pushdown automata 上。它的关键点在于：既能回答“是否存在某条满足策略的 trace”，也能回答“在失败数、时延、跳数、隧道深度等多重指标下，哪条 witness trace 最优”。

- 形式主义定位：`MPLS` dataplane what-if analysis 的 weighted-pushdown 基础设施，而不是新的网络状态机母型。
- 构造方式简述：topology + forwarding tables + query language + minimization criteria -> weighted pushdown system -> quantitative reachability。
- 基础设施与场景简述：依托 `AalWiNes` GUI、query language、network-to-pushdown translation 与 weighted witness solver，服务 `MPLS` 网络在多链路故障下的 policy compliance 与 latency/hops/tunnel-depth 分析。

```text
MPLS forwarding tables + failure assumptions + query -> weighted pushdown system -> witness search / minimization -> concrete network trace
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `MPLS` network topology 与 forwarding rules。
2. label-stack / header rewrite semantics。
3. network traces 与 reachability query language。
4. quantitative trace-weight expressions。
5. `AalWiNes` GUI 与 weighted pushdown solver。

### 核心抽象

论文首先定义 network topology：

$$
G = (V, E, s, t)
$$

上式中的符号逐项解释如下：

1. `V` 是 routers 集合。
2. `E` 是有向多重边集合。
3. `s,t : E \to V` 分别给出边的源端点与目标端点。
4. 这是论文 `Definition 1` 的核心骨架。

在此基础上，`MPLS` network 被定义为：

$$
N = (V, E, s, t, L, \tau)
$$

上式中的符号逐项解释如下：

1. `(V,E,s,t)` 是网络拓扑。
2. `L` 是 labels 集合，含普通标签与特殊底标记。
3. `\tau` 记录 forwarding-table induced operations。
4. 这是论文 `Definition 2` 的核心对象。

header rewrite 语义可保守写成：

$$
H : L^\ast \rightharpoonup L^\ast
$$

上式中的符号逐项解释如下：

1. `L^\ast` 是 label stacks 集合。
2. `H` 是偏函数，对应 push、pop、swap 或透传等 `MPLS` 操作。
3. 论文 `Definition 3` 用 partial header rewrite semantics 来解释 dataplane 行为。

network trace 可写成：

$$
\sigma = (e_1, h_1)(e_2, h_2)\cdots(e_n, h_n)
$$

上式中的符号逐项解释如下：

1. `e_i` 是第 `i` 步经过的链路。
2. `h_i` 是该步关联的 packet header / label stack。
3. 这正是论文 `Definition 4` 中 trace 的骨架。

查询语言的核心对象写成：

$$
\varphi = \langle a \rangle b \langle c \rangle k
$$

上式中的符号逐项解释如下：

1. `a` 约束初始 header stack。
2. `b` 约束链路序列或中间路径模式。
3. `c` 约束最终 header stack。
4. `k` 限制允许的链路失败数量。
5. 这是论文 `Definition 5` 的 reachability query 骨架。

若加入定量优化，则最小 witness 问题可压成：

$$
\sigma^\ast = \arg\min_{\sigma \models \varphi} (expr_1(\sigma), expr_2(\sigma), \ldots, expr_n(\sigma))
$$

上式中的符号逐项解释如下：

1. `\sigma \models \varphi` 表示 trace 满足查询。
2. `expr_i` 可是 `Hops`、`Failures`、`Latency`、`Tunnels` 等代价。
3. 论文通过 weighted pushdown automata 解决这种字典序最优 witness 搜索。

### 一个最小例子与通俗解释

论文里的 running example 很适合直观看：

1. 一张 `MPLS` 网络图给出 router 与 link。
2. 每个 router 的 forwarding table 决定收到某类 label-stack 后该怎么改写 header 并走哪条边。
3. 查询可以问“有没有一条从某个 service label 出发、最终回到某个 `IP` 头的 trace，而且最多容忍 `1` 条链路失效？”
4. 如果有不止一条 trace，工具还能进一步返回 latency/hops/failures 更优的 witness。

通俗地说，`AalWiNes` 像是把“出故障后网络包会怎么绕、会不会违反策略、会不会变慢很多”这类运维问题，翻成了“带权栈自动机上有没有一条最优路径”的问题。

### 运行 / 接受 / 转移语义

论文的执行语义重点包括：

1. dataplane forwarding tables 决定 packet 在网络中的一步步重写和转发。
2. link failures 改写可用边集合。
3. query language 在 trace 层面约束起始 header、链路序列与最终 header。
4. weighted pushdown backend 返回 witness trace，并在需要时做 feasibility replay。

代表性的 trace 代价函数可写成：

$$
\mathrm{Links}(\sigma),\ \mathrm{Hops}(\sigma),\ \mathrm{Failures}(\sigma),\ \mathrm{Latency}(\sigma),\ \mathrm{Tunnels}(\sigma)
$$

上式中的符号逐项解释如下：

1. `Links` 是 trace 长度。
2. `Hops` 表示跳数。
3. `Failures` 表示所依赖的故障数。
4. `Latency` 表示路径时延。
5. `Tunnels` 表示 trace 中正向增加的 label-stack 深度。

### 语义边界

1. 论文主线是 `MPLS` dataplane verification，不是一般网络协议状态机统一前端。
2. 它更关注 trace-property 与 quantitative witness，而不是分支时序逻辑全景。
3. weighted pushdown 之所以适合这里，关键在于 `MPLS` header stack 是无界但结构化的。
4. 网络可达性结果最终仍需映射回具体 trace feasibility，这也是工具链里专门保留 replay/validation 的原因。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| topology | `$G = (V,E,s,t)$` | `MPLS` 网络的基础图结构。 |
| network model | `$N = (V,E,s,t,L,\tau)$` | forwarding tables 与 labels 一起定义系统对象。 |
| header rewrite | `$H : L^\ast \rightharpoonup L^\ast$` | dataplane 行为的核心。 |
| trace | `$\sigma = (e_1,h_1)\cdots(e_n,h_n)$` | witness 不只是路径，还绑定 header 演化。 |
| query | `$\varphi = \langle a \rangle b \langle c \rangle k$` | 初始/路径/最终约束与故障预算统一进单一查询对象。 |
| 最优 witness | `$\sigma^\ast = \arg\min_{\sigma \models \varphi} \cdots$` | 工具能做定量而不仅是布尔验证。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 隐含在 router/label-stack configuration 中。 |
| 事件 / 触发 | 中等支持 | 主要体现为 packet forwarding 与 link-failure 假设。 |
| 守卫 / 数据 | 很强 | header stacks、forwarding rules 和 failure assumptions 都直接参与语义。 |
| 层次 | 不适用 | 不是层次状态机前端。 |
| 并发 / 同步 | 弱到中等 | 重点是单 packet trace 分析，不是并发同步语义建模。 |
| 时间约束 | 间接支持 | 可做 latency 最优 witness，但不是 clocks/invariants 语义。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | GUI、query language、weighted solver 与 witness replay 全都已工具化。 |

### 形式化问题与性质

1. `AalWiNes` 的重点不是重新定义 `MPLS`，而是把 network what-if analysis 稳定地翻进 weighted-pushdown 求解框架。
2. 它让 network verification 从“能否满足逻辑性质”推进到“哪条 witness 在多个指标上最好”。
3. 这条路线也证明了 weighted pushdown 基础设施不只是程序分析后端，同样能服务网络 dataplane 验证。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 网络 topology。
2. routers 的 forwarding tables。
3. query language 中的 header/path/failure constraints。
4. trace minimization expressions。

### 机器可处理承载方式

机器可处理承载方式包括：

1. topology XML 与 forwarding tables。
2. `MPLS` label stacks。
3. query language 字符串。
4. weighted pushdown system 与 witness traces。

### 交换与互操作

互操作重点在于：

1. 工具直接消费 dataplane configuration，而不是抽象控制平面。
2. 网络模型会被翻译成 weighted pushdown backend。
3. GUI 会把求出的 witness trace 回显成具体网络路径与 header 操作。

## 配套基础设施

- 建模/编辑工具：`AalWiNes` 图形界面与输入配置文件。
- 解析/交换/元模型支持：topology XML、forwarding tables、query language parser。
- 仿真/执行支持：主线不是运行时仿真，而是 trace replay 与 witness feasibility validation。
- 验证/分析支持：logical property checking、quantitative reachability、minimum witness search、故障场景分析。
- 代码生成/转换支持：重点是 `network -> weighted pushdown` 翻译，不主打部署代码生成。
- 标准化或社区生态：依托 `AalWiNes` 自身与 weighted pushdown analysis ecosystem，而非网络行业交换标准。

## 适用场景与需求前提

### 适用场景

适合 `MPLS` 网络的 what-if analysis、policy compliance 检查、多链路故障鲁棒性评估，以及需要同时考虑 correctness 和 latency/hops/tunneling 等指标的运维调试场景。

### 需求前提

1. 网络应能稳定恢复出 dataplane forwarding tables。
2. 关键行为主要体现在 packet trace 与 header-stack 演化上。
3. 关心的问题可以压成 reachability query 与 witness 最优化。
4. 故障模型主要是 link failures，而不是一般连续时间或概率演化。

### 不适用或高成本场景

如果系统主体不是 `MPLS` dataplane，或者需求是一般控制器合成、复杂时钟逻辑或多包并发队列语义，`AalWiNes` 这条 `WPDS` 路线就不够直接。

## 与相邻形式主义的关系

相对 [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)，`PDAAAL` 是通用 `WPDS` 算法库，而 `AalWiNes` 是把 `WPDS` 落到 `MPLS` dataplane 分析的上层基础设施；相对 [opennwa-a-nested-word-automaton-library/desc.md](../opennwa-a-nested-word-automaton-library/desc.md)，这里处理的是 header-stack 与 forwarding trace，不是 visible call/return 词；相对 [model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md](../model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md)，两者都属于“真实工程对象 -> pushdown backend”的路线，但 `CodeSurfer/x86 + WPDS++` 面向程序控制流，而 `AalWiNes` 面向网络 dataplane。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机/自动机工具谱系里的很多基础设施节点其实是“跨领域承载体”，不应只盯控制系统或 UML 家族。
2. 对后续若考虑把需求 trace、故障场景和最小反例路径一起生成出来，这种“query + best witness”工作流很有参考价值。
3. 它也补强了文库里 `weighted-pushdown backend` 这条基础设施线的横向广度。

### 作为目标形式主义还是中间表示

更像某类工程对象到自动机后端之间的专用分析载体，而不是本课题的一线目标状态机语言。

### 对需求到模型生成的启发

1. 若系统天然以 trace 和栈式上下文为中心，就不该强压成平面有限状态图。
2. “最短/最低代价/最少失败”的 witness 搜索，比单纯 yes/no 验证更适合进入修复闭环。
3. 对 bridge 型条目，要特别留意它有没有稳定的 query language 和机读输入，而不是只讲一个求解思路。

### 现实限制

这条路线很强于 `MPLS` what-if analysis，但它并不等价于一般协议状态机前端，也不直接覆盖 richer control-plane semantics。

## 重要的相关工作

1. [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)：通用 weighted-pushdown reachability 库。
2. [model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md](../model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md)：另一条工程对象到 `WPDS` backend 的代表工具链。
3. [opennwa-a-nested-word-automaton-library/desc.md](../opennwa-a-nested-word-automaton-library/desc.md)：结构化序列对象自动机基础设施的相邻工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`MPLS network / weighted pushdown automata / AalWiNes`
- 归类理由：论文主体是 network-to-`WPDS` 的 query 与 witness 基础设施，而不是新的网络模型本体；其核心对象仍然是 trace、header-stack 与分析载体，因此按 `📦/🏗️/📝` 处理更稳。
