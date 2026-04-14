# AdamMC：面向带 Transit 的 Petri 网与 Flow-LTL 的模型检查器 / AdamMC: A Model Checker for Petri Nets with Transits against Flow-LTL

## 基本信息

- 标题：AdamMC: A Model Checker for Petri Nets with Transits against Flow-LTL
- 中文标题：AdamMC：面向带 Transit 的 Petri 网与 Flow-LTL 的模型检查器
- 作者：Bernd Finkbeiner，Manuel Gieseking，Jesko Hecking-Harbusch，Ernst-Rüdiger Olderog
- 发表：*Computer Aided Verification*，pp. 64-76，2020
- DOI：`10.1007/978-3-030-53291-8_5`
- 链接：https://doi.org/10.1007/978-3-030-53291-8_5
- 形式主义：`Petri Nets with Transits / Flow-LTL / AdamMC`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：首个面向 `Petri Nets with Transits` 与 `Flow-LTL` 的模型检查工具
- 工具/实现获取方式：论文明确给出在线入口 `https://uol.de/en/csd/adammc`，并在参考文献中给出 artifact 说明。
- 标准/格式获取方式：输入包括 `Petri nets with transits + Flow-LTL`、`SDN topology/update + Flow-LTL` 或 `safe Petri net + LTL`；内部还使用 `APT`、`MCHyper` 与 `ABC` 组成分析链。

## 简报

`AdamMC` 补的是 Petri 网线里非常特殊但很有代表性的一条“局部流视角”路线。普通 `Petri Net + LTL` 更关注全局 marking 的行为，而 `Petri Nets with Transits + Flow-LTL` 能显式跟踪 token 的局部流链，因此特别适合网络包流、数据流和并发更新这种“全局状态太大，但每个 token 的局部流要求很关键”的系统。

- 形式主义定位：`Petri nets with transits` 的模型检查方法与工具链，不是新的通用 `Petri` 母型。
- 构造方式简述：把带 transit 的网与 `Flow-LTL` 公式归约成 safe `Petri net + LTL`，再落到 circuit model checking。
- 基础设施与场景简述：依托 `APT` parser、两种 reduction、`MCHyper` 和 `ABC`，服务 `SDN` 更新验证、flow safety 与 packet-level correctness。

```text
Petri net with transits / SDN update -> Flow-LTL formula -> safe Petri net + LTL -> MCHyper circuit -> ABC checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. safe Petri nets with transits；
2. flow chains；
3. `Flow-LTL`；
4. sequential / parallel reductions；
5. circuit-based model checking backend。

### 核心抽象

论文直接给出带 transit 的安全 `Petri` 网：

$$
N = (P,T,F,In,\Upsilon)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transition 集合。
3. `$F \subseteq (P\times T)\cup(T\times P)$` 是普通 flow relation。
4. `$In \subseteq P$` 是初始 marking。
5. `$\Upsilon$` 是 transit relation，用于跟踪 token 局部流向。

论文对 transit relation 给出：

$$
\Upsilon(t) \subseteq (pre_N(t)\cup\{\triangleright\}) \times post_N(t)
$$

上式中的符号逐项解释如下：

1. `$pre_N(t)$` 是 transition `$t$` 的输入 place 集。
2. `$post_N(t)$` 是 `$t$` 的输出 place 集。
3. `$\triangleright$` 表示一条新 flow 的起点。
4. 若 `$p\Upsilon(t)q$`，表示 firing `$t$` 时 place `$p$` 中的 flow 被延续到 `$q$`。
5. 若 `$\triangleright\Upsilon(t)q$`，表示 firing `$t$` 时在 `$q$` 启动一条新 flow chain。

论文说明 `Flow-LTL` 在 `LTL` 之上加入新的 flow operator。可保守写成：

$$
\varphi = \varphi_{run} \rightarrow A\psi_{flow}
$$

上式中的符号逐项解释如下：

1. `$\varphi_{run}$` 是 run formula，用来约束全局 marking / fired transitions。
2. `$A\psi_{flow}$` 表示对所有 flow chains 都要满足局部流性质 `$\psi_{flow}$`。
3. `A` 是 `Flow-LTL` 相对普通 `LTL` 的核心新算子。

### 一个最小例子与通俗解释

论文给了一个机场安检例子：

1. 乘客 token 从 `airport` 出发，经 `queue`，最终要到 `terminal`。
2. 安检员自己的行为也用另一条 flow chain 表示。
3. transit relation 记录“某个 token 的局部轨迹”而不只看全局 marking。
4. 因此可以表达“每个乘客最终到达 terminal，且中途不进入禁区”这类 local-flow 性质。

通俗地说，普通 `Petri Net` 更像只看“系统此刻有多少 token 在哪儿”，而 `Petri nets with transits` 多记了一层“这个 token 之前是怎么来的、之后往哪儿去”。`AdamMC` 就是把这种 packet/data-flow 语义真正做成可验证工具。

### 运行 / 接受 / 转移语义

论文的核心算法是把 `N` 与 `Flow-LTL` 归约为 safe `Petri net` 与普通 `LTL`：

$$
(N,\varphi) \leadsto (N^{>},\varphi^{>})
$$

上式中的符号逐项解释如下：

1. `$N$` 是原始 Petri net with transits。
2. `$\varphi$` 是原始 `Flow-LTL` 公式。
3. `$N^{>}$` 是归约后的 safe `Petri net`。
4. `$\varphi^{>}$` 是对应的 `LTL` 公式。

对含有 `$n$` 个 flow subformulas `A\psi_i` 的情形，论文构造：

$$
N^{>} = N^{>}_O \cup N^{>}_1 \cup \cdots \cup N^{>}_n
$$

上式中的符号逐项解释如下：

1. `$N^{>}_O$` 负责跟踪 run part，也就是全局系统进展。
2. `$N^{>}_i$` 负责跟踪第 `$i$` 个 flow subformula 对应的一条 flow chain。
3. 这使得“全局行为”和“局部流链”可以在归约后分别被编码。

论文给出两种 reduction：

1. sequential approach：网和公式大小多项式增长；
2. parallel approach：在 flow subformula 很少时，虽然最坏指数增长，但实践中更快。

最后一步可概括为：

$$
(N^{>},\varphi^{>}) \leadsto \text{circuit} \leadsto \text{ABC}
$$

即先经 `MCHyper` 生成电路，再由 `ABC` 做底层 circuit model checking。

### 语义边界

1. 工具面向的是 safe Petri nets with transits，不是任意高层或无界高层网。
2. 它特别强调 local flow chains，因此更适合 packet/data-flow correctness，而不是一般全局资源调度。
3. parallel reduction 在理论上可能指数 blow-up，但对少量 flow formulas 的实际问题常更快。
4. 这条线的优势主要在 local flow verification，不是传统 `Petri` 分析的全覆盖替代品。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 网对象 | `$N=(P,T,F,In,\Upsilon)$` | `Petri nets with transits` 的基本元组。 |
| transit relation | `$\Upsilon(t)\subseteq (pre_N(t)\cup\{\triangleright\})\times post_N(t)$` | token-flow tracking 的关键扩展。 |
| `Flow-LTL` 结构 | `$\varphi = \varphi_{run} \rightarrow A\psi_{flow}$` | 全局运行约束与局部流性质组合。 |
| reduction | `$(N,\varphi)\leadsto (N^{>},\varphi^{>})$` | `AdamMC` 的核心模型检查步骤。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | global markings 与 local flow chains 同时可表达。 |
| 事件 / 触发 | 很强 | transitions 是全局与局部流语义的共同核心。 |
| 守卫 / 数据 | 弱支持 | 重点不是复杂数据守卫，而是 token-flow structure。 |
| 层次 | 不支持 | 不是层次网或 profile 语言。 |
| 并发 / 同步 | 很强 | `Petri` 并发性是本体基础。 |
| 时间约束 | 不支持 | 主文不讨论 timed `Petri` 语义。 |
| 连续动态 / 随机性 | 不支持 | 主线是离散并发与流链逻辑。 |
| 可执行 / 可验证性 | 很强 | reduction、circuit encoding 与 `ABC` backend 都已工具化。 |

### 形式化问题与性质

1. `AdamMC` 的价值在于“局部流链可验证”，而不是普通 `LTL on markings`。
2. 它把 `Petri Net` 的 token-flow 视角拉到和网络包流验证直接对齐。
3. 对文库而言，这是 `Petri` 工具线里非常有辨识度的 flow-sensitive branch。

## 构造方式与承载格式

### 建模入口

论文中有三类入口：

1. `Petri nets with transits + Flow-LTL`；
2. `SDN topology + initial configuration + concurrent update + Flow-LTL`；
3. `safe Petri net + LTL`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `APT` 可解析的 `Petri` 输入；
2. `Flow-LTL` 公式；
3. reduction 后的 safe `Petri net + LTL`；
4. `MCHyper` 生成的 circuits；
5. `ABC` backend。

### 交换与互操作

互操作重点在于：

1. `APT` 提供 Petri parser；
2. `AdamMC` 把 flow-aware 模型归约成普通 `LTL` 问题；
3. `MCHyper` 与 `ABC` 负责最终 circuit-level checking。

## 配套基础设施

- 建模/编辑工具：`AdamMC` 在线工具入口，支持 `SDN` 与 `Petri` 两类前端。
- 解析/交换/元模型支持：`APT` parser、`Flow-LTL` parser、并发更新与网络拓扑输入。
- 仿真/执行支持：重点是模型检查，不是运行时仿真。
- 验证/分析支持：sequential / parallel reduction、`Flow-LTL` checking、`SDN` 常见性质库、`LTL` checking。
- 代码生成/转换支持：核心是到 safe `Petri net`、`LTL` 与 circuits 的归约，不是部署代码生成。
- 标准化或社区生态：依托 `Adam`、`APT`、`MCHyper`、`ABC` 构成研究型工具生态。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 软件定义网络的并发更新正确性；
2. 需要按 token / packet 局部路径表达性质的并发系统；
3. 局部流链比全局 marking 更关键的 `Petri` 建模任务。

### 需求前提

1. 系统最好能建成 safe `Petri net with transits`。
2. 性质应自然表达为 `Flow-LTL` 的 run part + flow part。
3. 若走 `SDN` 入口，需要网络拓扑和更新操作可显式化。

### 不适用或高成本场景

如果需求主要是传统 `P/T net` 的可达性、时间网调度、随机网 performability，而不是 token-flow path correctness，那么这条路线可能不如传统 `Petri` 工具链直接。

## 与相邻形式主义的关系

相对 [building-petri-nets-tools-around-neco-compiler/desc.md](../building-petri-nets-tools-around-neco-compiler/desc.md)，`Neco` 更偏 `Petri net -> explicit exploration / LTL` 基础设施，而 `AdamMC` 更偏 flow-aware specification。相对 [marcie-model-checking-and-reachability-analysis-done-efficiently/desc.md](../marcie-model-checking-and-reachability-analysis-done-efficiently/desc.md)，`MARCIE` 主打 stochastic-Petri quantitative platform，而这里主打 token-flow logic。相对 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，`TINA` 侧重时间网与 state-class 分析，而 `AdamMC` 强在 `Flow-LTL` 与 SDN concurrent-update verification。

## 与本研究的关系

### 对 Project 1 的价值

1. 它补强了 `Petri` 支线里“局部资源流 / packet flow”这类非纯全局 marking 的谱系节点。
2. 对控制系统建模来说，这类“flow-aware”逻辑很适合表达数据包、工件、资源令牌的局部约束。
3. 如果未来 `project_2` 要生成验证场景，`run formula -> flow formula` 这种二层结构很值得借鉴。

### 作为目标形式主义还是中间表示

更像面向并发流系统的验证侧目标形式主义和 backend，而不是通用控制软件前端。

### 对需求到模型生成的启发

1. 对 token / packet / 工件这类对象，需求可以拆成“全局运行规则”和“每个 flow chain 必须满足的局部性质”。
2. `Petri nets with transits` 为“对象轨迹”提供了比普通 `Petri` 更自然的承载层。
3. 这类局部流性质对网络控制、任务流和资源流系统很有价值。

### 现实限制

它依赖专门的 flow-aware `Petri` 本体和 `Flow-LTL`，因此不适合作为一般状态机文档交换标准；但正因为语义聚焦，才在特定并发流问题上非常有辨识度。

## 重要的相关工作

1. [building-petri-nets-tools-around-neco-compiler/desc.md](../building-petri-nets-tools-around-neco-compiler/desc.md)：显式状态探索与 `LTL` 后端的 `Petri` 工具链。
2. [marcie-model-checking-and-reachability-analysis-done-efficiently/desc.md](../marcie-model-checking-and-reachability-analysis-done-efficiently/desc.md)：stochastic `Petri` quantitative platform。
3. [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：时间网分析主线工具。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Petri Nets with Transits / Flow-LTL / AdamMC`
- 归类理由：论文主贡献是 `Petri nets with transits` 的模型检查方法与工具链，而不是新的通用 `Petri` 母型。
