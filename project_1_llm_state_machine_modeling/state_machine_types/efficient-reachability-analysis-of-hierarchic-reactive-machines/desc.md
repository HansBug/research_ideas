# 分层反应模块的高效可达性分析 / Efficient Reachability Analysis of Hierarchic Reactive Machines

## 基本信息

- 标题：Efficient Reachability Analysis of Hierarchical Reactive Machines
- 中文标题：分层反应模块的高效可达性分析
- 作者：Rajeev Alur, Radu Grosu, Mark McDougall
- 发表：*Computer Aided Verification*, pp. 280-295, 2000
- DOI：`10.1007/10722167_23`
- 链接：https://doi.org/10.1007/10722167_23
- 形式主义：`Hierarchic Reactive Modules / Machines (HRM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 语义收束
- 工具/实现获取方式：论文给出 Java visual checker 原型，但未提供现成下载入口；机器可处理入口是 mode、entry/exit points、global/local variables、guarded commands、default entry/exit、macro-step semantics。
- 标准/格式获取方式：原文没有独立标准格式；核心承载方式是 visual mode graph、mode definition / mode reference、guarded transitions 与 trace-based denotational semantics。

## 简报

这篇论文虽然题目写的是 reachability analysis，但真正值得文库收的是 `HRM` 本身：它把层次状态机从“盒子里再套盒子”的语法层次，推进到具有显式 entry/exit、变量作用域、history、group transition 和 black-box 模块边界的语义层次。相比 `Statecharts`，它更克制；相比 `HSM`，它更像面向实际反应式软件的 mode-based family；而且原文非常明确地把 hierarchy 解释成 semantic hierarchy，而不是单纯 syntactic nesting。

- 形式主义定位：`Statecharts / HSM` 之后的 semantic hierarchy 分支，用 mode 作为黑盒模块单元。
- 构造方式简述：每个 mode 有 global/local variables、entry/exit points、submodes 与带 guarded commands 的 transitions，并通过 default entry/exit 实现 history 与 group transitions。
- 基础设施与场景简述：论文实现了 visual checker，并强调 direct-on-hierarchy reachability，而不是先 flatten 到 `SMV/Spin` 一类后端。

```text
reactive mode structure -> mode + scoped variables + entry/exit + history -> macro-step traces -> hierarchy-preserving reachability
```

## 形式主义定义与核心对象

### 定义对象

原文的基本对象不是 state 或 box，而是 mode。mode 既像一个子状态机，也像一个带接口的黑盒模块：外界只能通过 entry / exit 与它交互，不能任意跨层戳进内部。

### 核心抽象

论文没有给出单一 canonical tuple；下面这个元组是根据原文“mode 的属性”做的保守整理：

$$
\mathcal M = (E_{in}, E_{out}, V_g, V_l, S, T, \rho)
$$

上式中的符号逐项解释如下：

1. `E_{in}` 是 entry points 集合。
2. `E_{out}` 是 exit points 集合。
3. `V_g` 是与环境共享的 global variables。
4. `V_l` 是 mode 内部的 local variables。
5. `S` 是 submode instances 集合。
6. `T` 是带 guarded commands 的 transitions。
7. `\rho` 记录 submode reference / reuse 关系。

这个整理不是论文原样 tuple，但和文中对 mode 的属性描述一一对应。

### 一个最小例子与通俗解释

原文 Figure 1 的典型直觉是：顶层 mode `M` 里嵌着子 mode `n` 和 `p`。当控制流进入 `n` 后，内部可以正常跑；如果内部无边可走，控制会沿 default exit 被“弱抢占”回到外层；而如果下一次再从 default entry 进入，history 又会把先前停下的内部位置恢复回来。

通俗地说，`HRM` 像“有输入口和输出口、还能记住上次停在哪里的状态机模块”。普通 `Statecharts` 更像一张大图；`HRM` 更像若干可复用的小盒子，每个盒子有明确接口和局部变量作用域。

### 运行 / 接受 / 转移语义

原文把 mode execution 解释成 macro-step game。可保守写成：

$$
(e_{in}, \sigma) \xRightarrow{\mathcal M} (e_{out}, \sigma')
$$

上式中的符号逐项解释如下：

1. `e_{in} \in E_{in}` 是环境把控制交给该 mode 的入口点。
2. `e_{out} \in E_{out}` 是该 mode 返回控制给环境的出口点。
3. `\sigma` 是进入 mode 时的状态估值。
4. `\sigma'` 是 mode 运行一个 macro-step 后返回给环境的状态估值。

原文进一步强调：一个 mode 的 execution 由若干 micro-steps 组成，但外部只观察 macro-step；trace 则由执行过程中 global variables 的投影得到。因此可写成：

$$
\mathrm{Trace}(\mathcal M) = \pi_{V_g}(\sigma_0,\sigma_1,\ldots)
$$

default exit / default entry 又给出两条关键语义：

1. default exit 支持 group transition 与 weak preemption；
2. default entry 支持 history 恢复。

### 语义边界

`HRM` 的边界与相邻 family 非常清楚：

1. 它仍是离散 reactive model，不含 clocks 或连续流。
2. 它比 `HSM` 多了变量作用域、history、group transitions 与 mode reuse。
3. 它比 `Statecharts` 更克制，因为跨层交互被收束到 entry / exit。
4. 它允许通过 top-level-form mode 来表达并行组合，但原文只实现 interleaving semantics。

### 关键性质与判定边界

原文的核心方法仍是 invariance / reachability，但这些结论之所以重要，是因为它们依赖于 `HRM` 的语义结构本身。可保守压成：

$$
\mathrm{Reachability}_{HRM} \text{ is solved directly on hierarchy, without full flattening}
$$

更细一点，论文强调：

1. 状态按 stack-of-vectors 表示，而不是一次性打平成单向量。
2. transition relation 按 mode / control point 建索引。
3. variable scoping 与 typing 直接被 checker 用来削减搜索空间。

因此 `HRM` 不只是“Statecharts + tool”，而是“专门为了 hierarchy-preserving analysis 收束出来的一类 mode semantics”。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | mode 是一等对象。 |
| 事件 / 触发 | 强支持 | guarded transitions + control points。 |
| 守卫 / 数据 | 强支持 | global/local variables 与 guarded commands 是核心。 |
| 层次 | 强支持 | submodes + mode reuse。 |
| 并发 / 同步 | 部分支持 | 可用 top-level-form mode 表达 interleaving parallel composition。 |
| 时间约束 | 不支持 | 无显式 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | 原文就围绕 checker 与 reachability 展开。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| mode 整理元组 | `$\mathcal M=(E_{in},E_{out},V_g,V_l,S,T,\rho)$` | 按原文属性做的保守 canonicalization。 |
| macro-step | `$(e_{in},\sigma)\xRightarrow{\mathcal M}(e_{out},\sigma')$` | mode 对环境暴露的黑盒语义。 |
| trace 语义 | `$\mathrm{Trace}(\mathcal M)=\pi_{V_g}(\sigma_0,\sigma_1,\ldots)$` | 观察只投影到 global variables。 |
| weak preemption | `inner > group` priority | 内层边优先于外层 group transition。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 mode 的 global / local variables。
2. 再定义 entry / exit points。
3. 然后补 submodes 与 guarded transitions。
4. 最后用 default entry / exit 指定 history 与 group-transition 语义。

### 机器可处理承载方式

原文的机器可处理承载方式主要是 visual mode graph + internal representation：

1. mode definition / mode reference；
2. control points；
3. guarded commands；
4. closure 后的 default entry / exit transitions；
5. trace-based denotational semantics。

### 交换与互操作

原文没有独立交换标准，但它在谱系上承担两种桥接：

1. 往上承接 `Statecharts / HSM` 的 hierarchy 直觉。
2. 往下衔接 hierarchy-preserving verification 与 modular refinement 路线。

## 配套基础设施

- 建模/编辑工具：论文明确实现了 visual hierarchical language。
- 解析/交换/元模型支持：核心是 mode、control points、scope-aware transitions。
- 仿真/执行支持：按 macro-step / micro-step semantics 执行。
- 验证/分析支持：enumerative 与 symbolic reachability checker。
- 代码生成/转换支持：原文未把重点放在代码生成。
- 标准化或社区生态：研究型生态，未形成通用标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 有显式 mode hierarchy 的 reactive software。
2. 需要 black-box module interface 与 variable scoping。
3. 希望保留 hierarchy 做 analysis，而不是先 flatten。

### 需求前提

1. 行为可拆成有限 mode。
2. 环境交互可通过 entry / exit 接口表达。
3. 数据需求仍可控制在有限离散变量上。

### 不适用或高成本场景

如果需求需要真正并发同步字母 product，更贴近 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)；如果需求核心是 recursion / call-return，更适合 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 与相邻形式主义的关系

相对 `Statecharts`，`HRM` 用 entry / exit 和 black-box boundary 收束跨层语义；相对 `HSM`，它加入了 shared variables、history 与 group transitions；相对 `CHSM`，它不是同步 product family，而是 mode / scope / trace family；相对 `RSM`，它没有无界 call stack。

## 与本研究的关系

### 对 Project 1 的价值

它让层次状态机支线不只停留在“可视化状态图”，而是出现了一个可直接连接模块语义、作用域和保层次分析的中间节点。

### 作为目标形式主义还是中间表示

更适合作为中间表示或谱系节点；若真要工程落地，还要再映射到更明确的实现语言或工具链。

### 对需求到模型生成的启发

当需求文本里出现“局部变量只在某个 mode 内有效”“中断后恢复原子流程”“只允许通过模块接口进入 / 退出”的描述时，LLM 生成目标不该再是 plain `Statecharts`，而应该意识到 `HRM` 这类更语义化的 hierarchy model。

### 现实限制

它没有成为通用工业标准；同时，原文中的实现更多是研究型 checker 而不是长期维护的公共生态。

## 重要的相关工作

### 奠基或前身工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)
- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)

### 同类型或同家族工作

- `Modular refinement of hierarchic reactive machines`：`HRM` 的 refinement 主文。
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：hierarchy 走向 recursion 的子线。

## 文献分类总结

- 这篇论文虽然以 analysis 为题，但真正稳定入树的对象是 `HRM` 模型本体。
- 它属于层次状态机支线中的“semantic hierarchy / scoped mode”路线，而不是 DSL 或工具条目。
- 在当前演化树里，最适合作为 `HSM` 之后的一条 richer semantic sibling / child 节点。
