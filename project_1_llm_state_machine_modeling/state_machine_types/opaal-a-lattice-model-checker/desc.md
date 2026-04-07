# opaal：格自动机模型检查器 / opaal: A Lattice Model Checker

## 基本信息

- 标题：opaal: A Lattice Model Checker
- 中文标题：opaal：格自动机模型检查器
- 作者：Andreas Engelbredt Dalsgaard，René Rydhof Hansen，Kenneth Yrke Jørgensen，Kim Gulstrand Larsen，Mads Chr. Olesen，Petur Olsen，Jiří Srba
- 发表：*NASA Formal Methods*，`LNCS 6617`，pp. 487-493，2011
- DOI：`10.1007/978-3-642-20398-5_37`
- 链接：https://doi.org/10.1007/978-3-642-20398-5_37
- 形式主义：`Lattice Automata / Lattice Transition Systems / UPPAAL subset / opaal`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：open-source lattice-automata model checker extending a subset of the `UPPAAL` language
- 工具/实现获取方式：原文明确说明 `opaal` 是开源模型检查器，支持用户通过 Python 类定义 lattice type、ordering 和 join；当前可在项目站点 `opaal-modelchecker.com` 查到架构与代码入口。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata 语言子集加 lattice 特性、Python lattice 定义、图形模型与 reachability configuration；不是独立行业交换标准。

## 简报

这篇论文的价值，在于把“抽象域”直接塞进状态机模型里，而不是把抽象完全藏在验证器后端。`opaal` 允许用户在 `UPPAAL` 风格模型中声明 lattice variables，再通过 ordering、join 和 joining strategy 控制探索时的覆盖与抽象精度。它补的不是新的 timed automata 母型，而是一条兼具建模语言、抽象策略和 model-checking backend 的基础设施路线。

- 形式主义定位：围绕 lattice automata 的模型检查工具链，而不是新的主干状态机家族。
- 构造方式简述：`UPPAAL` 子集模型 + Python lattice library -> lattice transition system -> explicit / cover / join-based reachability。
- 基础设施与场景简述：依托 lattice variables、monotonicity、join strategies 和 CEGAR-style refinement，服务抽象状态空间大、但单调结构明显的协议、数据库与缓存分析。

```text
UPPAAL-style model + lattice variables -> LaTS -> cover or join-based exploration -> reachable / unreachable verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. join semi-lattice / lattice；
2. lattice automata；
3. lattice transition systems (`LaTS`)；
4. cover update、join update 与 joining strategy；
5. `opaal` model checker 与 Python lattice library。

### 核心抽象

论文先把 join semi-lattice 写成偏序集合：

$$
L = (L,\sqsubseteq)
$$

上式中的符号逐项解释如下：

1. 第一个 `$L$` 是 lattice 元素集合。
2. `$\sqsubseteq$` 是偏序关系。
3. 若任意两个元素都有最小上界，则可定义 join。
4. 论文用它来承载“更大元素代表更多行为”的抽象语义。

论文直接把 lattice transition system 定义为：

$$
T = (S, L, \rightarrow)
$$

上式中的符号逐项解释如下：

1. `$S$` 是有限状态集合。
2. 第二个 `$L$` 是 lattice。
3. `$\rightarrow \subseteq S \times L \times S \times L$` 是转移关系。
4. configuration 是 `$(s,\ell)$` 形式的状态-格值对。

其核心单调性条件可写成：

$$
(s_1,\ell_1) \rightarrow (s_2,\ell_2)\ \land\ \ell_1 \sqsubseteq \ell_1'
\Rightarrow
\exists \ell_2'.\ (s_1,\ell_1') \rightarrow (s_2,\ell_2')\ \land\ \ell_2 \sqsubseteq \ell_2'
$$

上式中的符号逐项解释如下：

1. `$\ell_1 \sqsubseteq \ell_1'$` 表示把当前抽象值放宽。
2. 单调性要求放宽后的源配置，仍能沿同一结构边走到某个不更精细的目标配置。
3. 这正是 `cover update` 和 `join update` 可用的基础。

论文把 reachability 问题压成：

$$
\text{Given } (s_0,\ell_0) \text{ and } s_g,\ \text{decide whether } \exists \ell.\ (s_0,\ell_0) \rightarrow^\ast (s_g,\ell)
$$

这就是 `opaal` 解决的基本问题。

### 一个最小例子与通俗解释

论文给出的数据库例子很直观：

1. 系统里有多个用户，可以 `login`、`work`、`logout`。
2. 某些信息不再记录成“精确有多少个用户已登录”，而是记录成 bitvector lattice。
3. lattice variable 允许工具直接问“这个抽象状态是否已经覆盖了另一个状态的行为”。
4. 因而 reachability 不再只能做纯显式枚举，还能利用 monotonicity 和 join 减少探索。

通俗地说，`opaal` 像“把抽象解释器的抽象域直接嵌进状态机变量里”，让用户自己告诉模型检查器：哪些细节可以合并、哪些不能。

### 运行 / 接受 / 转移语义

论文对路径定义为：

$$
\sigma = (s_0,\ell_0)(s_1,\ell_1)\cdots(s_n,\ell_n)
$$

其中：

1. 每一步都满足 `$(s_i,\ell_i) \rightarrow (s_{i+1},\ell_{i+1})$`。
2. 这是 `LaTS` 上的具体路径。

抽象路径则写成：

$$
\hat{\sigma} = (s_0,\ell_0)(s_1,\ell_1)\cdots(s_n,\ell_n)
$$

但要求变成：

1. 每一步存在某个更精细目标 `$\ell'_{i+1}$`，使得 `$(s_i,\ell_i)\rightarrow(s_{i+1},\ell'_{i+1})$`。
2. 同时 `$\ell'_{i+1} \sqsubseteq \ell_{i+1}$`。
3. 这就是 over-approximate join update 的语义来源。

论文还把 joining strategy 视作：

$$
\mathrm{joining} : S \times L \times L \to \{\mathrm{True}, \mathrm{False}\}
$$

上式中的符号逐项解释如下：

1. 输入是某个 control state 与两个 lattice elements。
2. 输出决定这两个 lattice elements 是否允许在该 state 被 join。
3. 这让用户能用 domain knowledge 控制抽象精度。

### 语义边界

1. `opaal` 重点是 safety / reachability，不是通用时序逻辑全能后端。
2. 它依赖 monotonicity；若模型不满足单调结构，lattice 技巧就用不上。
3. 论文实现的是 `UPPAAL` 语言子集加 lattice 扩展，而不是完整 `UPPAAL`。
4. 精度与效率很依赖用户提供的 joining strategy。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| lattice 骨架 | `$L = (L,\sqsubseteq)$` | 用偏序和 join 表达抽象域。 |
| `LaTS` 骨架 | `$T = (S,L,\rightarrow)$` | `opaal` 的正式分析对象。 |
| 单调性 | `$(s_1,\ell_1)\rightarrow(s_2,\ell_2)\land \ell_1\sqsubseteq\ell_1' \Rightarrow \exists \ell_2' ...$` | 放宽抽象值后行为仍可被覆盖。 |
| reachability | `$\exists \ell.\ (s_0,\ell_0)\rightarrow^\ast(s_g,\ell)$` | 工具的核心判定问题。 |
| joining strategy | `$\mathrm{joining}: S \times L \times L \to \{\mathrm{True},\mathrm{False}\}$` | 用户控制哪些抽象值允许被合并。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍以同步扩展有限状态机骨架承载控制状态。 |
| 事件 / 触发 | 很强 | 继承 `UPPAAL` 风格边和同步结构。 |
| 守卫 / 数据 | 很强 | lattice variables、ordering 与 join 是核心。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等支持 | 支持同步扩展有限状态机组合，但论文重点不在并发语义创新。 |
| 时间约束 | 中等支持 | 输入语言来自 `UPPAAL` 子集，但全文重点是 lattice abstraction 而非 dense-time theory。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散 reachability。 |
| 可执行 / 可验证性 | 很强 | 有显式、cover、join 三类探索方式与开源实现。 |

### 形式化问题与性质

1. 论文补出的不是“另一种 timed automata 变体”，而是“如何把 lattice-based abstraction 直接内置到模型检查流程里”。
2. monotonicity + joining strategy 的组合，使用户能半手工、半自动地控制 over-approximation。
3. 这条线位于 `UPPAAL` timed backend 与更一般 `WSTS/abstract interpretation` 之间。

## 构造方式与承载格式

### 建模入口

论文中的典型入口包括：

1. `UPPAAL` 语言子集模型；
2. 通过 `extern` 导入的 lattice types；
3. Python 中定义的 lattice class；
4. control graph 上使用 lattice variables 的 guards 和 updates。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` 风格模型文本；
2. lattice library 中的 Python classes；
3. configurations `$(s,\ell)$`；
4. cover / join exploration data structures。

### 交换与互操作

这篇论文的互操作重点在工具内部：

1. 模型前端沿用 `UPPAAL` 子集。
2. lattice 类型通过 Python 扩展注入。
3. reachability backend 在显式探索、cover check 和 join abstraction 之间切换。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 风格输入语言与 `opaal` 前端。
- 解析/交换/元模型支持：Python lattice classes、ordering、join 和 joining strategy。
- 仿真/执行支持：重点不在 simulation，而在 symbolic / abstract reachability。
- 验证/分析支持：explicit exploration、cover update、join update、CEGAR-style refinement。
- 代码生成/转换支持：原文不涉及代码生成。
- 标准化或社区生态：开源发布，依托 `UPPAAL` 社区与 lattice-abstraction 实验路线。

## 适用场景与需求前提

### 适用场景

适合数据库程序、异步 lossy 协议、cache analysis 等能自然写成单调抽象系统、且需要利用 domain abstraction 缩减状态空间的问题。

### 需求前提

1. 模型最好满足 monotonicity。
2. 用户能给出合适的 lattice、ordering 和 join。
3. 目标主要是 reachability / safety，而不是复杂时序逻辑全覆盖。
4. 系统可接受 `UPPAAL` 子集前端和工具特定扩展。

### 不适用或高成本场景

若系统缺乏单调结构、抽象域难以设计，或者主要需求是完整 `UPPAAL` 生态兼容，`opaal` 的收益会明显下降。

## 与相邻形式主义的关系

相对 [uppaal-in-a-nutshell/desc.md](../uppaal-in-a-nutshell/desc.md)，本文不是核心 `UPPAAL` 平台总览，而是带 lattice abstraction 的扩展工具；相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md) 与 [using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md](../using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md)，这些条目更偏 zone abstraction/backend 优化，`opaal` 则把抽象域作为模型一部分显式暴露给用户；相对 [tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md](../tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md)，`Tarzan` 强调 region backend，`opaal` 强调 lattice-guided abstraction backend。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“形式主义选型”不只看模型本体，还要看后端允许怎样的抽象与缩减。
2. 对后续 LLM 生成状态机而言，若目标系统天然存在可抽象单调结构，这类 backend 会直接影响可验证性。
3. 它也提示：有些状态机工具不是只吃标准模型，而是允许把领域抽象知识显式注入验证流程。

### 局限

1. 它不是通用交换标准。
2. 对用户侧抽象域设计能力有较高要求。

## 重要的相关工作

1. [uppaal-in-a-nutshell/desc.md](../uppaal-in-a-nutshell/desc.md)：`UPPAAL` 核心平台总览。
2. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：`LU` 抽象路线。
3. [tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md](../tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md)：region-based timed backend。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Lattice Automata / Lattice Transition Systems / UPPAAL subset / opaal`
- 论文角色：open-source lattice-automata model checker extending a subset of the `UPPAAL` language
- 归类理由：论文主体是 open-source model checker、输入扩展、joining strategy 和 reachability backend，核心贡献明显属于 toolchain / backend 基础设施。
