# 不完美信息下 pushdown module checking 的新结果 / New results on pushdown module checking with imperfect information

## 基本信息

- 标题：New results on pushdown module checking with imperfect information
- 中文标题：不完美信息下 pushdown module checking 的新结果
- 作者：Laura Bozzelli
- 发表：*Electronic Proceedings in Theoretical Computer Science*, 54:162-177, 2011
- DOI：`10.4204/EPTCS.54.12`
- 链接：https://doi.org/10.4204/EPTCS.54.12
- 形式主义：`Stable Open Pushdown Systems / stable OPD`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：subclass introduction / imperfect-information `OPD` refinement
- 工具/实现获取方式：原文没有工程工具；机器可处理入口是 `OPD` 八元组、visible / invisible control-stack partition、strategy tree semantics 与 stable 条件。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 `OPD` tuple、可见性函数 `vis`、induced open Kripke structure 与 stable subclass definition。

## 简报

这篇论文虽然外表还是 module checking 复杂度论文，但它真正为演化树补出来的是一个新命名子类：`stable OPD`。此前文库里已经有 `Imperfect-Information OPD / Pushdown Module Checking with Imperfect Information (2007 / 2013)`，但这一支内部还缺少“在可见栈深前提下，哪些 `OPD` 本体才算观测一致”的稳定子类说明；这篇论文正好把这个空缺补成 `stable OPD / visible-stack-depth stable OPD`。

- 形式主义定位：`Imperfect-Information OPD` 下面的观测一致性子类。
- 构造方式简述：先给出普通 `OPD` 八元组和 visible / invisible control-stack 分区，再用 `stable` 条件限制 visually equivalent configurations 的后继结构。
- 基础设施与场景简述：原文无工程工具，但把 partial-observation open recursive system 的 family boundary 进一步切细。

```text
open pushdown system + partial observation -> imperfect-information OPD -> visible depth restriction -> stable OPD subtype
```

## 形式主义定义与核心对象

### 定义对象

论文把 open recursive system 建成 `OPD`，并进一步区分环境到底能看到多少控制状态和栈信息。`stable OPD` 的关键不是再加一套新栈操作，而是要求：只要两个配置在环境可见部分上等价，它们就必须暴露出可见上等价的后继选择结构。

### 核心抽象

原文直接给出 `OPD` 八元组：

$$
S = \langle AP, Q, q_0, \Gamma, \bot, \Delta, \mu, Env \rangle
$$

上式中的符号逐项解释如下：

1. `AP` 是命题集合。
2. `Q` 是控制状态集合，`q_0` 是初始控制状态。
3. `\Gamma` 是栈字母表，`\bot` 是栈底符号。
4. `\Delta` 是内部、push、pop 三类迁移关系。
5. `\mu` 是标签函数。
6. `Env` 指出哪些控制状态与栈顶组合属于 environment configurations。

一个配置写成 `(q,\alpha)`，其中 `q \in Q`，`\alpha \in \Gamma^* \cdot \bot`。环境可见性由 `vis` 给出，论文进一步把 `stable OPD` 定义为：若两个非终止局部对 `(q_1,\gamma_1)` 与 `(q_2,\gamma_2)` 在可见部分上等价，那么任何一方的后继都必须能在另一方找到可见上匹配的后继。可保守压成：

$$
vis(q_1)=vis(q_2)\ \land\ vis(\gamma_1)=vis(\gamma_2)
\Longrightarrow
\mathrm{Succ}_{vis}(q_1,\gamma_1)=\mathrm{Succ}_{vis}(q_2,\gamma_2)
$$

这里的符号逐项解释如下：

1. `vis` 只保留环境可见的控制与栈信息。
2. `\mathrm{Succ}_{vis}` 表示后继在可见信息意义下的等价类。
3. 这就是 stable 条件的直观本质。

### 一个最小例子与通俗解释

一个最小例子可以是“带递归调用的开放控制器”：

1. 系统控制状态分成 environment state 和 system state。
2. 环境能看到“当前在处理哪类调用”以及“当前栈深”，但看不到栈帧内部细节。
3. 如果两个配置在环境眼里完全一样，那么环境不该因为系统内部隐藏细节不同而获得不同的可见下一步分支。

通俗地说，`stable OPD` 像“对环境视角一致的开放 pushdown 系统”。它不是再造一个新栈机，而是给 `imperfect-information OPD` 加了一条观测一致性纪律。

### 运行 / 接受 / 转移语义

原文把 `OPD` 诱导成 open Kripke structure：

$$
M_S = \langle AP, W_s, W_e, w_0, R, L, \approx \rangle
$$

上式中的符号逐项解释如下：

1. `W_s` 与 `W_e` 分别是 system states 与 environment states。
2. `w_0` 是初始配置。
3. `R` 是配置迁移关系。
4. `L` 给出命题标签。
5. `\approx` 是环境的观测等价关系。

在 visible stack content depth 的场景下，原文指出：

$$
\text{stable } OPD \text{ with visible stack depth} \Longrightarrow \text{a well-behaved observation discipline}
$$

这使得后续 `ECTL` 决定性结果有了明确 family 载体，而不只是对任意 partial-observation `OPD` 的偶然算法特例。

### 语义边界

这条子类的边界如下：

1. 仍属于 `OPD`，不是脱离 pushdown module checking 另起一套模型。
2. 新增的是 imperfect-information compatibility 条件，而不是新栈操作。
3. visible stack content 与 visible stack depth 需要严格区分。
4. stable 只保证“可见层面上的后继一致性”，不自动保证所有逻辑片段都可判定。

### 关键性质与判定边界

论文最关键的 family boundary 正是：

$$
\mathrm{PMC}(stable\ OPD,\ ECTL,\ visible\ stack\ depth) \in 2EXPTIME
$$

同时又证明：

$$
\mathrm{PMC}(stable\ OPD,\ CTL(EF,EX,AG,AX),\ visible\ stack\ depth)
\text{ is undecidable}
$$

以及

$$
\text{program complexity of } \mathrm{PMC}(OPD,\ CTL,\ visible\ stack\ content)
\text{ is } 2EXPTIME\text{-complete}
$$

这些结果说明：`stable OPD` 的价值不是“把一切都变可判定”，而是把 imperfect-information `OPD` 内部哪些子类仍可稳定维护为状态机 family 讲清楚。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | pushdown configuration + environment/system partition。 |
| 事件 / 触发 | 强支持 | internal / push / pop 三类迁移。 |
| 守卫 / 数据 | 弱支持 | 重点不在变量，而在可见性分区。 |
| 层次 | 强支持 | 通过 stack 自然表达 recursive hierarchy。 |
| 并发 / 同步 | 不支持 | 主要是顺序开放系统。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | module checking、strategy trees、partial observation、`2EXPTIME` / undecidability boundary。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `OPD` 元组 | `$S=\langle AP,Q,q_0,\Gamma,\bot,\Delta,\mu,Env\rangle$` | 母模型。 |
| open Kripke structure | `$M_S=\langle AP,W_s,W_e,w_0,R,L,\approx\rangle$` | module checking 语义对象。 |
| stable 条件 | `$vis(q_1,\gamma_1)=vis(q_2,\gamma_2)\Rightarrow \mathrm{Succ}_{vis}(q_1,\gamma_1)=\mathrm{Succ}_{vis}(q_2,\gamma_2)$` | 观测一致性子类。 |
| decidable fragment | `$\mathrm{PMC}(stable\ OPD,\ ECTL,\ visible\ stack\ depth)\in 2EXPTIME$` | 新子类的正面边界。 |
| undecidable fragment | `$\mathrm{PMC}(stable\ OPD,\ CTL(EF,EX,AG,AX),\ visible\ stack\ depth)$` undecidable | 新子类的负面边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义控制状态和栈字母表。
2. 再把配置划分为 environment 与 system 两侧。
3. 为控制状态与栈内容规定 visible / invisible 变量分区。
4. 最后检查 visually equivalent configurations 是否满足 stable 后继匹配条件。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `OPD` 八元组。
2. 可见性函数 `vis`。
3. induced open Kripke structure。
4. strategy tree semantics。

### 交换与互操作

它与文库既有条目的关系非常明确：

1. 向上承接 [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md) 与 [pushdown-module-checking-with-imperfect-information-iandc/desc.md](../pushdown-module-checking-with-imperfect-information-iandc/desc.md) 的 `Imperfect-Information OPD`。
2. 向旁说明 visible stack content 与 visible stack depth 两种可见性假设不能混为一谈。
3. 向下补出 `stable OPD` 这条可独立命名的 subtype。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `OPD` tuple、visibility partition 与 strategy-tree semantics。
- 仿真/执行支持：由 induced open Kripke structure 和 strategy trees 给出。
- 验证/分析支持：`CTL / ECTL` pushdown module checking、`AVPA` reduction。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：纯理论 family，无公开工程标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 开放递归系统的 partial-observation 分析。
2. 需要明确环境能看见多少 stack 信息的开放控制模型。
3. 希望把 imperfect-information `OPD` 再细分出可稳定命名的子类时。

### 需求前提

1. 系统核心复杂度来自 recursion / pushdown，而不是并发。
2. 环境观测边界需要显式建模。
3. 关心的不是单纯可达性，而是 open-system branch-time property。

### 不适用或高成本场景

如果需求没有开放环境和不完美观测，就应退回 [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)；如果只需要 perfect-information `OPD`，也没必要强行引入 `stable` 子类。

## 与相邻形式主义的关系

相对 `Pushdown Module Checking with Imperfect Information (2007 / 2013)`，这篇论文最核心的新内容是 `stable OPD`；相对一般 `OPD`，它多了可见性一致性约束；相对 `RSM`，它关注的是 open-system module checking 语义，而不是单纯递归控制流本体。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Open Pushdown Systems` 这条层次状态机理论支线进一步切细，给树上补出了一个以前没有被稳定命名的 subtype。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和理论选型依据，而不是工程终端目标。

### 对需求到模型生成的启发

当需求中出现“环境只能看到控制器的一部分内部状态”“环境知道当前递归深度但不知道具体栈帧内容”这类信息时，生成目标不应只写成普通 `OPD`，而应进一步判断是否落在 `stable OPD` 这样的子类里。

### 现实限制

它是 workshop-level paper，工程生态几乎没有；同时它补出的更多是 family boundary，而不是工具落地。

## 重要的相关工作

### 前后衔接

- [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)
- [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md)
- [pushdown-module-checking-with-imperfect-information-iandc/desc.md](../pushdown-module-checking-with-imperfect-information-iandc/desc.md)

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为其母对象仍是 pushdown-style 离散状态机，不涉及时间、混成或随机动态。
- 这是一篇 `🧱 模型本体` 文献，因为它补出的是 `stable OPD` 这一命名子类与其观测一致性定义，而不只是算法微调。
- 这篇论文的描述客体是 `🤝 接口 / 交互契约`，因为它研究的是开放系统与环境之间在部分可观测条件下的交互边界。
- 这篇论文属于 `🧮 形式语言与自动机理论`，因为它服务的是 recursive open-state-machine family 的 subtype 命名和可判定性边界。
