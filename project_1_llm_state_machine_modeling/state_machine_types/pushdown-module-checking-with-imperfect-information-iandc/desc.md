# 带不完美信息的下推模块检验（I&C 全文版） / Pushdown module checking with imperfect information

## 基本信息

- 标题：Pushdown module checking with imperfect information
- 中文标题：带不完美信息的下推模块检验（I&C 全文版）
- 作者：Benjamin Aminof, Axel Legay, Aniello Murano, Olivier Serre, Moshe Y. Vardi
- 发表：*Information and Computation*, 223:1-17, 2013
- DOI：`10.1016/j.ic.2012.11.005`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/final-I%26C-C3983.pdf
- 形式主义：`Open Pushdown Systems (OPD)` 上的 imperfect-information / partial-observation 扩展
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / imperfect-information open pushdown
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 visibility-aware `OPD` tuple、`vis` observation、induced module `M_S`、semi-alternating pushdown tree automata（`PD-SBT / PD-SPT`）与 `CTL / CTL^* / $\mu$-calculus` reductions。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 visible/invisible control + stack variables、可见配置等价、环境剪枝语义以及带 Büchi / parity 接受条件的 pushdown tree automata。

## 简报

这篇 `I&C` 全文版把 `CONCUR 2007` 与 `IFIP TCS 2008` 两轮结果统一收束成了一个更完整的 family 口径：`OPD` 一旦进入 imperfect-information setting，general case 已经不可判定；但若 stack 完全可见、只隐藏 control states，则 `CTL` 与 propositional `$\mu$-calculus` 仍是 `2EXPTIME` 完全，而 `CTL^*` 是 `3EXPTIME` 完全。对当前演化树来说，它的意义不只是“证明更多逻辑更难”，而是把 **partial-observation open pushdown** 这一子枝的可见性边界、自动机化承载和逻辑覆盖范围一次性固定下来。

- 形式主义定位：`Imperfect-Information OPD` 的 journal full version，也是 open recursive hierarchy 中最稳定的 partial-observation family 依据。
- 构造方式简述：在 `OPD` 的 control states 与 stack symbols 上切 visible / invisible variables，用 `vis((q,\alpha))` 定义 observation，并用 observation-consistent pruning 解释环境行为。
- 基础设施与场景简述：全文版显式加入 `CTL^*` 与 propositional `$\mu$-calculus`，并通过 `PD-SBT / PD-SPT` 与 parity/Büchi 接受条件把 decidable 子类的自动机化承载完整补齐。

```text
OPD + partial observation -> vis-based open computation trees -> PD-SBT / PD-SPT -> CTL / CTL* / mu-calculus module checking
```

## 形式主义定义与核心对象

### 定义对象

论文研究的是 environment 只能看到 configuration 一部分的开放式 pushdown systems。它把“看不见什么”直接写进 formalism，而不是把 partial observation 留给外部博弈语义去隐式处理。

### 核心抽象

全文版保留了与 conference 版一致的主元组：

$$
S = \langle AP, Q, q_0, \Gamma, \gamma_b, \delta, \mu, Env \rangle
$$

上式中的符号逐项解释如下：

1. `AP` 是原子命题集合。
2. `Q \subseteq 2^{I \cup H}` 是控制状态集合，其中 `I` 与 `H` 分别是 visible / invisible control variables。
3. `q_0 \in Q` 是初始控制状态。
4. `\Gamma \subseteq 2^{I_\Gamma \cup H_\Gamma}` 是栈字母表，`I_\Gamma` 与 `H_\Gamma` 分别是 visible / invisible stack variables。
5. `\gamma_b` 是栈底符号。
6. `\delta` 是 pushdown transition relation。
7. `\mu` 是 labeling function。
8. `Env` 指出 environment configurations。

其 observation 核心仍然是：

$$
vis((q,\alpha)) = (vis(q), vis(\alpha))
$$

并且若一个 pushed symbol 只含 invisible stack variables，则环境甚至看不到这次 push 本身，只能看到可见栈串没有新增可见片段。

### 一个最小例子与通俗解释

全文版延续 ATM 例子：

1. 客户能看到 ATM 的屏幕反馈和部分 control states。
2. 机器内部是否缺纸、广告压栈了哪些 invisible symbols，对客户不可见。
3. 环境于是只能基于可见配置做 pruning，无法区分某些看起来一样但内部 stack content 不同的 runs。

通俗地说，这个 family 像“环境只透过磨砂玻璃看 `OPD`”。journal full version 的贡献，是把这块磨砂玻璃后面的可判定 / 不可判定边界画清楚了。

### 运行 / 接受 / 转移语义

诱导 module 仍写成：

$$
M_S = \langle AP, W_s, W_e, w_0, R, L, \approx \rangle
$$

其中：

$$
w \approx w' \iff vis(w) = vis(w')
$$

而 partial-observation module checking 判断的是：环境是否能在所有 observation-consistent 剪枝下保持公式成立。

对 decidable 子类，全文版把问题规约到 semi-alternating pushdown tree automata。其核心想法是：若两个 automaton copies 在同一 input 和相同 top-of-stack 上运行，则它们必须向 stack 推入同样的值，从而避免一般 alternating pushdown automata 那种立刻失控的不可判定性。

### 语义边界

这个 family 的边界如下：

1. general imperfect-information `OPD` 已经不可判定。
2. 不可判定性真正依赖于 stack information 的隐藏，而不是只依赖 control-state hiding。
3. 当 stack 完全可见时，partial observation 仍可保留 decidability。
4. 全文版把 `CTL`、`CTL^*` 与 propositional `$\mu$-calculus` 三种逻辑口径统一到了同一个 family 边界里。

### 关键性质与判定边界

全文版的核心结论可以压成三条：

$$
\mathrm{PMC}_{\mathrm{II}}(OPD, CTL) \text{ is undecidable}
$$

$$
\mathrm{PMC}_{\mathrm{ctrl\text{-}hidden,\ stack\text{-}visible}}(OPD, CTL)
\text{ is } 2\mathrm{EXPTIME}\text{-complete}
$$

$$
\mathrm{PMC}_{\mathrm{ctrl\text{-}hidden,\ stack\text{-}visible}}(OPD, \mu)
\text{ is } 2\mathrm{EXPTIME}\text{-complete},\quad
\mathrm{PMC}_{\mathrm{ctrl\text{-}hidden,\ stack\text{-}visible}}(OPD, CTL^*)
\text{ is } 3\mathrm{EXPTIME}\text{-complete}
$$

也就是说，journal full version 真正稳住的不是单一证明，而是“partial-observation open pushdown family 在多种 branching-time logics 下的统一边界”。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | open pushdown skeleton 完整保留。 |
| 事件 / 触发 | 强支持 | push/pop/rewrite 规则仍决定 configuration 演化。 |
| 守卫 / 数据 | 弱支持 | 重点不在丰富数据，而在 visibility partition。 |
| 层次 | 强支持 | recursion / stack 仍是母骨架。 |
| 并发 / 同步 | 不支持 | sequential open recursion。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可观测性 / 信息模式 | 强支持 | visibility boundary 决定 decidability。 |
| 可执行 / 可验证性 | 强理论支持 | `PD-SBT / PD-SPT`、`CTL / CTL^* / $\mu$-calculus` complexity 全部收束。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| visibility-aware `OPD` | `$S = \langle AP, Q, q_0, \Gamma, \gamma_b, \delta, \mu, Env \rangle$` | partial-observation open pushdown model。 |
| visible part | `$vis((q,\alpha)) = (vis(q), vis(\alpha))$` | 环境可见配置定义。 |
| observation equivalence | `$w \approx w' \iff vis(w) = vis(w')$` | pruning 必须对观察一致。 |
| general case | `$\mathrm{PMC}_{\mathrm{II}}(OPD, CTL)$ undecidable` | stack-hidden 情形的主边界。 |
| visible-store case | `$CTL,\mu: 2\mathrm{EXPTIME};\ CTL^*: 3\mathrm{EXPTIME}$` | journal full version 新补齐的统一复杂度口径。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 `OPD` 的 control states、stack alphabet 与 environment partition。
2. 再把 control / stack variables 分成 visible 与 invisible 两部分。
3. 用 `vis` 和 observation equivalence 定义环境能区分哪些 configurations。
4. 最后针对 visible-store 子类，用 `PD-SBT / PD-SPT` 承载 `CTL / CTL^* / $\mu$-calculus` 规约。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. visibility-aware `OPD` tuple；
2. induced module `M_S`；
3. `vis` observation function；
4. `PD-SBT`（Büchi）与 `PD-SPT`（parity）；
5. observation-consistent pruning trees。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md) 的 perfect-information `OPD`。
2. 会议版起点是 [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md)。
3. 若再放宽到更一般 alternating pushdown tree automata，则很快越出 decidable 边界，因此这篇全文版对 current tree 的价值恰恰在于它把“该停在哪里”写清楚了。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 visibility-aware `OPD`、`vis` 与 observation equivalence。
- 仿真/执行支持：可按 partial-observation induced module 语义解释。
- 验证/分析支持：`PD-SBT / PD-SPT`、`CTL / CTL^* / $\mu$-calculus` module checking、visible-store decidability。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要连接 module checking、partial observation 与 pushdown tree automata。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归开放系统里环境只能观察 configuration 一部分的场景。
2. 需要同时考虑 `CTL`、`CTL^*` 与 `$\mu$-calculus` 边界的 partial-observation family 盘点。
3. 想把 `OPD` 子线从“有无不完美信息”进一步稳定成完整 journal-level family。

### 需求前提

1. 系统复杂度主要来自 recursion 与 partial observation。
2. stack 可见性是否完全开放，是需求里必须明确的前提。
3. 关心的是 branching-time open semantics，而不是线性 trace 或工程执行语言。

### 不适用或高成本场景

如果环境具备完全信息，plain `OPD` 更合适；如果只需要 `CTL` conference 边界，2007 会议版已够；如果系统没有 recursion，则不需要这么重的 open pushdown machinery。

## 与相邻形式主义的关系

相对 conference 版，这篇全文版把 `CTL^*` 与 propositional `$\mu$-calculus` 统一纳入同一 family；相对 perfect-information `OPD`，它增加了 partial observation 和 visible-store boundary；相对一般 alternating pushdown automata，它保守停在 semi-alternating 子类，以换取 decidability。

## 与本研究的关系

### 对 Project 1 的价值

它使层次状态机理论线里的 open recursive branch 多了一层真正可用的“观测能力约束”。这对后续从非形式化需求决定目标模型时很重要，因为很多需求差别并不在控制骨架，而在环境能看见多少内部状态。

### 作为目标形式主义还是中间表示

更适合作为验证分析用的高表达力中间表示，而不是需求建模前端语言。

### 对需求到模型生成的启发

如果需求显式出现“环境只能看到部分模式 / 看不到内部栈上下文”，那么自动建模时需要优先判断 stack 是否必须完全可见；这一步直接决定模型是否还留在 decidable family 内。

### 现实限制

它是高度理论化 family，没有现成工业 DSL 或成熟工具链。

## 重要的相关工作

### 奠基或前身工作

- [pushdown-module-checking-lpar/desc.md](../pushdown-module-checking-lpar/desc.md)
- [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md)

### 同类型或同家族工作

- [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)
- `finite-state module checking with imperfect information`
- `semi-alternating pushdown tree automata`：本文为当前 family 给出的关键自动机承载。

## 文献分类总结

- 这篇全文版把 `Imperfect-Information OPD` 的 family boundary 从 `CTL` 正式扩到 `CTL^* / $\mu$-calculus`。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、工具论文或单纯复杂度优化。
- 在当前演化树里，它最适合继续挂在 `Statecharts -> HSM -> Open Hierarchical Modules -> Open Pushdown Systems / Pushdown Module Checking -> Imperfect-Information OPD`，并作为该子节点的 journal full version 依据。
