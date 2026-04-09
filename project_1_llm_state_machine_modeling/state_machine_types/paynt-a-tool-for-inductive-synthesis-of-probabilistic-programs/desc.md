# PAYNT：概率程序归纳综合工具 / PAYNT: A Tool for Inductive Synthesis of Probabilistic Programs

## 基本信息

- 标题：PAYNT: A Tool for Inductive Synthesis of Probabilistic Programs
- 中文标题：PAYNT：概率程序归纳综合工具
- 作者：Roman Andriushchenko，Milan Ceska，Sebastian Junges，Joost-Pieter Katoen，Simon Stupinsky
- 发表：*Computer Aided Verification*，pp. 856-869，2021
- DOI：`10.1007/978-3-030-81685-8_40`
- 链接：https://doi.org/10.1007/978-3-030-81685-8_40
- 形式主义：`probabilistic program sketches / realizations / PAYNT`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：probabilistic-program sketch synthesis and design-space exploration backend
- 工具/实现获取方式：原文明确给出 GitHub 入口 `https://github.com/gargantophob/synthesis`。
- 标准/格式获取方式：输入是带 holes 的 `PRISM` 或 `JANI` sketch，核心机读对象是 hole assignments、subfamilies、reachability / reward specs 和 `Storm` backend；它不是中立交换标准。

## 简报

`PAYNT` 补的是概率程序设计空间探索里一条很关键的路线：系统结构先写成 sketch，某些 guard、update 或参数位置保留 holes，再由工具自动在有限家族里找出满足时序性质、甚至最优的 realization。它把 probabilistic model checking 和 inductive synthesis 结合起来，不是暴力枚举全部候选，而是借助 `CEGIS`、abstraction-refinement 和 `Storm` 后端，对整片 design space 做剪枝。

- 形式主义定位：面向 probabilistic-program sketches 的综合与设计空间探索方法，而不是新的概率自动机母型。
- 构造方式简述：先用 holes 定义一族 `PRISM/JANI` 程序，再由 learner 选 realization，oracle 用 model checking 给出满足性或反例信息，并把这些信息推广为对整片子家族的剪枝。
- 基础设施与场景简述：依托 `PRISM/JANI` sketch、`Storm` backend、Python API 和 inductive synthesis architecture，服务概率协议、能耗管理器和有限状态控制器的自动选型。

```text
probabilistic sketch with holes -> realizations / subfamilies -> model-checking oracle -> pruning / refinement -> feasible or optimal realization
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. probabilistic program sketch；
2. holes 及其 options；
3. realizations 与其诱导的 `MC`；
4. reachability / expected-reward 规格；
5. feasibility 与 maximality synthesis problems。

### 核心抽象

原文把 sketch 的设计空间写成：

$$
R = \prod_k R_k
$$

上式中的符号逐项解释如下：

1. `H = \{H_k\}_k` 是 sketch 里的 holes 集合。
2. `R_k` 是 hole `H_k` 可选的具体选项集合。
3. `R` 是所有 hole assignments，也就是全部 realizations 的集合。
4. `|R|` 一般会随着 holes 数量指数增长，这正是 `PAYNT` 要避免暴力枚举的原因。

每个 realization 诱导一个完整程序与其语义模型：

$$
P[r] \leadsto D_r
$$

上式中的符号逐项解释如下：

1. `P` 是原始 probabilistic sketch。
2. `r \in R` 是一个具体 hole assignment。
3. `P[r]` 是把所有 holes 都替换后的完整程序。
4. `D_r` 是该程序诱导的有限状态 `MC`。

原文直接给出性质语法：

$$
\varphi \equiv P_{\triangleleft \lambda}[F T], \quad \varphi \equiv E_{\triangleleft \lambda}[F T]
$$

上式中的符号逐项解释如下：

1. `P_{\triangleleft \lambda}[F T]` 是 reachability property，约束最终到达目标集合 `T` 的概率。
2. `E_{\triangleleft \lambda}[F T]` 是 expected-reward property，约束到达 `T` 前累计 reward 的期望。
3. `\triangleleft` 取自 `<,\le,>,\ge` 或 `<,\le` 这类阈值比较。
4. `PAYNT` 允许把多个此类性质合成一个规格集合 `\Phi`。

论文定义的两类综合问题是：

$$
\exists r \in R.\ P[r] \models \Phi
$$

以及

$$
r^* \in \arg\max_{r \in R} \{ P[P[r] \models \varphi_{\max}] \mid P[r] \models \Phi \}
$$

上式中的符号逐项解释如下：

1. 第一式是 feasibility synthesis，问是否存在满足 `\Phi` 的 realization。
2. 第二式是 maximality synthesis，在满足约束 `\Phi` 的前提下再最优化某个目标性质 `\varphi_{\max}`。
3. `r^*` 是工具返回的最优 realization。
4. 原文还支持 `\varepsilon`-maximal synthesis，用近似最优换速度。

### 一个最小例子与通俗解释

论文给出的 server power-manager 例子很适合直觉理解：

1. 队列阈值 `T_1,T_2,T_3`、电源档位 `P_1,\ldots,P_4` 和容量 `Q_{max}` 都先留成 holes。
2. 每组 hole 取值组合代表一个 candidate power manager。
3. 规格要求“丢失请求的期望数量不超过 `1`，同时功耗尽量低”。
4. `PAYNT` 最终给出一组具体阈值与电源策略，而不是让用户手工把几百万种组合都试完。

通俗地说，`PAYNT` 像是“带模型检查内核的 sketch synthesizer”。用户先描述“哪些地方还没决定”，工具再自动在有限选项空间里搜索满足性质的完整程序。

### 运行 / 接受 / 转移语义

语义链路是：

1. sketch 本身不是单个模型，而是一个模型家族。
2. 每个 `r \in R` 生成一个完整概率程序 `P[r]`。
3. 该程序语义是有限状态 `MC`，可交给 `Storm` 做 model checking。
4. synthesis 层再利用单次 checking 的结果，对大量 realizations 做集合级剪枝。

论文强调的关键点不是重新发明 `MC` 语义，而是统一 family-level reasoning：

$$
R' \subseteq R
$$

上式中的符号逐项解释如下：

1. `R'` 是仍待探索的 subfamily。
2. `PAYNT` 不只分析单个 `r`，还会证明某些 `R'` 整体可行或整体不可行。
3. 这正是它相对纯枚举法的主要加速来源。
4. 原文把这类 family-level reasoning 分别交给 `CE` 和 `AR` oracle。

### 语义边界

1. 论文聚焦 finite-state probabilistic programs，不处理无限结构 general synthesis。
2. `PAYNT` 主要解决 topology / sketch synthesis，不是连续参数上的 symbolic region synthesis。
3. holes 的 domain 必须是有限离散集合。
4. 若家族过大且性质无法有效泛化，仍可能退化到较重的搜索成本。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 设计空间 | `$R = \prod_k R_k$` | 所有 realizations 的全集由各 hole 的离散选项乘积给出。 |
| 实例化 | `$P[r] \leadsto D_r$` | 每个 hole assignment 诱导一个具体概率程序与 `MC`。 |
| 规格语法 | `$\varphi \equiv P_{\triangleleft \lambda}[F T],\ \varphi \equiv E_{\triangleleft \lambda}[F T]$` | 支持 reachability 与 expected reward 约束。 |
| 可行性综合 | `$\exists r \in R.\ P[r] \models \Phi$` | 是否存在满足规格的 realization。 |
| 最优综合 | `$r^* \in \arg\max_{r \in R}\{\cdots\}$` | 在满足约束的 realization 中继续找最优候选。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 每个 realization 都是有限状态概率程序。 |
| 事件 / 触发 | 中等支持 | 依赖 `PRISM/JANI` 语法中的 guarded commands 与同步。 |
| 守卫 / 数据 | 强支持 | holes 可以出现在 guards 和 updates 中。 |
| 层次 | 不支持 | 不是层次状态机综合。 |
| 并发 / 同步 | 中等支持 | 通过 `PRISM` modules 和同步机制体现。 |
| 时间约束 | 间接支持 | 可经 `JANI/Storm` 接入更广概率模型，但论文主线是 finite-state programs。 |
| 连续动态 / 随机性 | 很强 | 随机性是模型本体，设计空间探索是主题。 |
| 可执行 / 可验证性 | 很强 | 工具直接调用 `Storm` 并输出可运行的 hole assignment。 |

### 形式化问题与性质

1. `PAYNT` 的关键不是“能检查一个模型”，而是“能在模型家族上做带证明的搜索”。
2. 它与 `PROPhESY` 的差异很明确：前者改结构选择，后者改概率参数。
3. 对 `project_1` 而言，它很适合充当“需求不完整时，从 sketch 到候选状态机”的方法侧证。

## 构造方式与承载格式

### 建模入口

原文给出的典型入口包括：

1. `PRISM` sketch；
2. `JANI` sketch；
3. 每个 hole 的离散 domain；
4. reachability / reward 规格；
5. 可选的优化目标。

### 机器可处理承载方式

机器可处理承载方式包括：

1. hole assignments；
2. unexplored subfamilies；
3. counterexamples；
4. abstraction-refinement state；
5. `Storm` 内部支持的 Markov models。

### 交换与互操作

这篇论文的互操作重点在：

1. 对 `PRISM` 采取保守扩展而不是重新发明语法；
2. 同时支持 `JANI` 作为更中立的承载层；
3. 把 Python orchestration 层和 `Storm` backend 分离，便于更换搜索策略。

## 配套基础设施

- 建模/编辑工具：核心是 `PRISM/JANI` sketch，不主打图形编辑器。
- 解析/交换/元模型支持：直接复用 `PRISM` 语言，兼容 `JANI`。
- 仿真/执行支持：主体不是 simulator，而是 synthesis + model checking。
- 验证/分析支持：feasibility、maximality、`\varepsilon`-maximal synthesis、`CEGIS`、abstraction-refinement。
- 代码生成/转换支持：重点在输出满足规格的 hole assignment，而不是下游部署代码生成。
- 标准化或社区生态：依托 `Storm`、`PRISM`、`JANI` 与概率程序综合社区。

## 适用场景与需求前提

### 适用场景

适合还处于 early design 阶段、控制器或协议结构尚未完全定型、但已经能把候选选项离散化并写成 probabilistic sketch 的任务。

### 需求前提

1. holes 的 domain 必须有限且可枚举。
2. 每个 realization 最终要能下沉成 finite-state `MC`。
3. 目标性质最好是 reachability 或 expected reward 一类 `Storm` 能高效处理的规格。
4. 如果要找最优解，优化目标也应可通过 model checking 评价。

### 不适用或高成本场景

若设计空间来自连续参数、复杂博弈结构或强非有限状态语义，`PAYNT` 并不是最直接入口。

## 与相邻形式主义的关系

相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md) 与 [the-probabilistic-model-checker-storm/desc.md](../the-probabilistic-model-checker-storm/desc.md)，`Storm` 是验证后端，`PAYNT` 是 family-level synthesizer；相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md) 与 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，这些条目更偏交换层或 Python workflow，而 `PAYNT` 直接做综合；相对 [prophesy-a-probabilistic-parameter-synthesis-tool/desc.md](../prophesy-a-probabilistic-parameter-synthesis-tool/desc.md)，`PROPhESY` 改概率参数，`PAYNT` 改结构 hole assignments。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机建模完全可以从“不完整模型草图”开始，而不是一开始就把每个状态与转移定死。
2. 这和 `project_1` 从自然语言需求生成结构化状态机的路线非常贴近。
3. 以后若要做“候选状态机自动筛选”，`PAYNT` 的 family-level pruning 思路很值得借用。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像 synthesis backend，而非目标状态机语言。

### 对需求到模型生成的启发

1. 需求中的模糊选择可以先保留成 holes。
2. 先生成一个模型家族，再用验证条件自动排除坏候选，比一次性硬生完整模型更稳。
3. 可行性和最优性可以统一放进后端筛选闭环。

## 重要的相关工作

- [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：`PAYNT` 当前实现依赖的重要概率模型检查后端。
- [the-probabilistic-model-checker-storm/desc.md](../the-probabilistic-model-checker-storm/desc.md)：更完整的 `Storm` 平台条目。
- [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：`JANI` 作为 sketch / model 交换层的重要配套。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇很典型的 sketch-based probabilistic synthesis 条目，适合作为“从不完整程序家族自动筛出满足时序性质的状态机/控制器”的方法证据入账。
