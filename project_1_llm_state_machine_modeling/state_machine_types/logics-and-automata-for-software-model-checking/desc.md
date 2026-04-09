# 软件模型检验中的逻辑与自动机 / Logics and Automata for Software Model-Checking

## 基本信息

- 标题：Logics and Automata for Software Model-Checking
- 中文标题：软件模型检验中的逻辑与自动机
- 作者：Rajeev Alur、Swarat Chaudhuri
- 发表：Marktoberdorf Summer School 2006 讲义，2006
- DOI：原文未提供
- 链接：https://www.cis.upenn.edu/~alur/Marktoberdorf06.pdf
- 形式主义：`Nested State Machines (NSM)`，并同时引出 `nested words / nested trees`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：讲义型总述 / `NSM` 语义入口
- 工具/实现获取方式：原文未给出工程实现；机器可处理入口是 `NSM` 元组、nested-word / nested-tree 语义、`NWA` 与 `NT-μ` 这两类规范化分析对象。
- 标准/格式获取方式：原文没有 DSL、交换标准或文件格式；核心承载方式是 `NSM` tuple、nested structures 与 automata-theoretic semantics。

## 简报

这份讲义的价值，不在于再讲一次一般性的 software model checking，而在于它把 `RSM` 之后一条此前在当前文库中尚未显式命名的支线稳定了下来：程序不再只被看成“配置图 + 栈”的生成器，也可以被看成生成 `nested words / nested trees` 的 `Nested State Machine`。对当前演化树来说，它提供了把 `RSM` 继续分叉到 `NSM` 的最清楚入口。

- 形式主义定位：`RSM` 的 nested-structure semantics 侧枝，用 `NSM` 统一承载 call / return 的线性与分支语义。
- 构造方式简述：用 `NSM` 的 local / call / return 三类迁移描述程序控制流，再把执行语义落成 nested words 或 nested trees。
- 基础设施与场景简述：原文没有工程工具，但明确把 `NWA`、`CaRet`、`NT-μ` 都挂到 `NSM` 之上，说明它适合作为递归控制流的语义母线，而不只是某个单独算法的前置模型。

```text
recursive program -> NSM -> nested words / nested trees -> NWA / CaRet / NT-μ -> software model checking
```

## 形式主义定义与核心对象

### 定义对象

原文先把程序抽象成一类新的递归控制流模型 `NSM`，再分别赋予它：

1. 线性时间上的 nested-word trace semantics；
2. 分支时间上的 nested-tree unfolding semantics。

因此这里真正新增的不是某个新逻辑，而是一种把 call / return 结构直接刻进状态机语义对象的模型蓝本。

### 核心抽象

原文给出的 `NSM` 核心元组可整理为：

$$
M = (V, v_{in}, \kappa, \Delta_{loc}, \Delta_{call}, \Delta_{ret})
$$

上式中的符号逐项解释如下：

1. `V` 是有限状态集合。
2. `v_{in} \in V` 是初始状态。
3. `\kappa : V \to \Sigma` 是状态观测标注函数，文中取 `\Sigma = 2^{AP}`。
4. `\Delta_{loc} \subseteq V \times V` 是不改动调用上下文的局部迁移。
5. `\Delta_{call} \subseteq V \times V` 是调用迁移，对应进入新过程上下文。
6. `\Delta_{ret} \subseteq V \times V \times V` 是返回迁移，其中中间状态参数记录最近一次未匹配调用的来源状态。

与普通 `FSM` 相比，新增的关键不是变量或时间，而是：

1. `call` 与 `ret` 被单独提升为一等迁移类别；
2. 返回迁移显式依赖“最后一次未匹配调用”的来源状态；
3. 模型的自然语义对象不再只是平面路径，而是 nested structures。

### 一个最小例子与通俗解释

原文用一个递归过程 `foo()` 说明 `NSM` 的直觉：

1. 某个状态 `v_2` 表示“在这里发起一次过程调用”。
2. 调用迁移 `v_2 \to v_1` 进入新过程体。
3. 过程完成后，从结束状态 `v_5` 通过返回迁移回到 `v_2'`。
4. 这次返回并不是普通边，而是“带着最近一次调用来源状态 `v_2`”回来的。

通俗地说，`NSM` 像“把递归调用栈折进了边类型里的状态机”。普通层次状态机告诉你“进入某个子流程”；`RSM` 用 components / boxes 讲 call-return；`NSM` 则进一步说：把执行过程看成带 jump-edge 的嵌套结构，这样 call 和 matching return 的配对就直接出现在语义对象本身里。

### 运行 / 接受 / 转移语义

原文先定义状态级 nested execution，再把它投影为观测 trace。其线性语义可压成：

$$
L(M)=\{(w',\rightsquigarrow)\mid \exists (w,\rightsquigarrow)\in L_V(M),\ \forall i\ge 0,\ w'(i)=\kappa(w(i))\}
$$

上式中的符号逐项解释如下：

1. `L_V(M)` 是按状态字母表 `V` 给出的 nested execution 语言。
2. `\rightsquigarrow` 是 matching call / return 的 jump-edge 关系。
3. `w` 是状态序列。
4. `w'` 是把状态序列经 `\kappa` 投影后的观测序列。
5. `L(M)` 因而是 `NSM` 的 nested-trace 语言。

对 branching-time，原文把语义落成 execution tree：

$$
T_V(M) = (T,\rightsquigarrow,\lambda)
$$

其中：

1. `T` 是由 `NSM` 展开的树形执行骨架。
2. `\rightsquigarrow` 连接 call 与 matching return。
3. `\lambda` 给每个节点赋一个 `NSM` 状态。

再经观测投影得到最终 unfolding `T(M)`。

### 语义边界

这篇讲义给 `NSM` 的边界画得很清楚：

1. 它仍然服务于 sequential recursive programs，不处理并发交错。
2. 它强调 call / return 的嵌套结构，而不是一般 pushdown store 的任意操作。
3. 它不是 DSL，也不是执行框架；核心是 semantic object 的改写。
4. 它与 `RSM` 非竞争关系，而是从“组件 + 栈”视角切到“nested structure”视角。

### 关键性质与判定边界

原文强调 `NSM` 之所以重要，是因为在其上定义的 `NT-μ` 与 automata-theoretic model checking 仍保持可判定。可压缩写成：

$$
\mathrm{MC}_{NT\text{-}\mu}(M,\varphi) \in \mathrm{EXPTIME}
$$

以及：

$$
\mathrm{MC}_{NT\text{-}\mu}(M,\varphi)\ \text{is EXPTIME-complete}
$$

上式中的符号逐项解释如下：

1. `M` 是一个 `NSM`。
2. `\varphi` 是 nested-tree 上的 `NT-μ` 公式。
3. `\mathrm{MC}` 表示模型检验问题。
4. 结论说明把 call / return 显式写进 nested structures 之后，仍能保住经典的 `EXPTIME` 边界。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `V` 是有限状态集合。 |
| 事件 / 触发 | 中等支持 | 原文更强调三类迁移而不是独立事件字母表。 |
| 守卫 / 数据 | 不支持 | 不处理有限变量与赋值。 |
| 层次 | 强支持 | 通过 call / return 的嵌套结构体现。 |
| 并发 / 同步 | 不支持 | 目标是 sequential recursive programs。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散递归控制流。 |
| 可执行 / 可验证性 | 强理论支持 | `NWA`、`CaRet`、`NT-μ` 都以它为语义蓝本。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `NSM` 元组 | `$M = (V, v_{in}, \kappa, \Delta_{loc}, \Delta_{call}, \Delta_{ret})$` | `NSM` 的最小模型骨架。 |
| nested trace 语言 | `$L(M)=\{(w',\rightsquigarrow)\mid \exists (w,\rightsquigarrow)\in L_V(M),\forall i,\ w'(i)=\kappa(w(i))\}$` | 线性语义直接保留 matching 结构。 |
| execution tree | `$T_V(M)=(T,\rightsquigarrow,\lambda)$` | branching-time 语义是 nested tree 而非 plain tree。 |
| `NT-μ` 模型检验 | `$\mathrm{MC}_{NT\text{-}\mu}(M,\varphi)$` | `NSM` 上的核心判定问题。 |
| 复杂度 | `$\mathrm{EXPTIME}$-complete` | 说明 nested semantics 没有把问题推到不可控边界。 |

## 构造方式与承载格式

### 建模入口

1. 先识别程序里的 local steps、procedure calls 和 returns。
2. 用三类迁移分别编码这三种控制流。
3. 再根据任务是 linear-time 还是 branching-time，选择 nested word 或 nested tree 语义。

### 机器可处理承载方式

原文的机器可处理入口主要是：

1. `NSM` tuple；
2. nested words；
3. nested trees；
4. `NWA` 与 `NT-μ`。

### 交换与互操作

原文没有工程交换格式，但理论互操作非常强：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向旁边衔接 [languages-of-nested-trees/desc.md](../languages-of-nested-trees/desc.md) 的 nested-tree automata family。
3. 向下连接 `CaRet`、`NWA` 与 `NT-μ` 这几类 stack-sensitive specification formalisms。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `NSM` tuple 与 nested-structure semantics。
- 仿真/执行支持：可经 nested executions / execution tree 给出精确语义。
- 验证/分析支持：`NWA`、`CaRet`、`NT-μ` 与相应的 automata-theoretic model checking。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 recursive-program verification 的理论支线，不是标准语言或运行时。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流的语义建模。
2. 需要把 matching call / return 直接暴露给规范语言的场景。
3. 希望把 `RSM` 家族继续分出 nested-structure semantics 侧枝的理论梳理。

### 需求前提

1. 系统核心是顺序递归控制流。
2. 关注点在 call / return 的上下文结构，而不是并发、数据或时间。
3. 需求希望直接引用“matching return”“当前过程上下文”这类 stack-sensitive 关系。

### 不适用或高成本场景

如果问题核心只是 ordinary reachability / `LTL/CTL*` over `RSM`，则 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 已足够；若需要显式变量与赋值，应改看 [model-checking-procedural-programs/desc.md](../model-checking-procedural-programs/desc.md) 的 `ERSM` 线。

## 与相邻形式主义的关系

相对 `HSM`，`NSM` 已经进入真实的 call / return 递归语义；相对 `RSM`，`NSM` 不再以 components / boxes 的全局配置图为唯一语义入口，而是把 matching structure 直接落成 nested words / nested trees；相对 `NWA` 或 `NT-μ`，`NSM` 是被这些 specification formalisms 解释的程序模型，而不是规范语言本身。

## 与本研究的关系

### 对 Project 1 的价值

它把当前 `Statecharts -> HSM -> uHSM -> RSM` 主线继续向“semantic encoding”方向长出一个可命名的 sibling：`NSM`。这能帮助后续在“层次控制流模型”和“stack-sensitive specification language”之间建立更干净的桥接层。

### 作为目标形式主义还是中间表示

更适合作为验证 / 分析阶段的中间表示，而不是需求建模前端的最终交付形式。

### 对需求到模型生成的启发

当需求里频繁出现“在同一调用上下文内”“返回到当前过程后”“调用-返回必须匹配”这类叙述时，直接生成为 plain `HSM` 或 `RSM` 还不够，后续验证环节更适合投影成 `NSM` 及其 nested structures。

## 重要的相关工作

1. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：`RSM` 的主干定义，是 `NSM` 的最近上游模型。
2. [languages-of-nested-trees/desc.md](../languages-of-nested-trees/desc.md)：把 `NSM` 的 branching semantics 推到 nested-tree language family。
3. [software-model-checking-using-languages-of-nested-trees/desc.md](../software-model-checking-using-languages-of-nested-trees/desc.md)：`NSM` 的 journal full version，给出更稳定的 `V_{loc}/V_{call}/V_{ret}` 划分。

## 文献分类总结

- 这篇文献在当前文库中应视为：`NSM` 支线的讲义型主入口，而不是单纯的 logic survey。
- 它最适合承担的角色是：为 `RSM -> NSM` 的树节点提供“为什么这是单独 family”的挂接说明。
- 若后续只保留一个 `NSM` 的主锚点，应优先保留 journal 版 [software-model-checking-using-languages-of-nested-trees/desc.md](../software-model-checking-using-languages-of-nested-trees/desc.md)；本文则作为它的 early overview / semantic-intuition 补强条目。
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
