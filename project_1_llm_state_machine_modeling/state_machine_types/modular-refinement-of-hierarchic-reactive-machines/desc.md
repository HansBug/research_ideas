# 分层反应机的模块化精化 / Modular Refinement of Hierarchic Reactive Machines

## 基本信息

- 标题：Modular Refinement of Hierarchic Reactive Machines
- 中文标题：分层反应机的模块化精化
- 作者：Rajeev Alur, Radu Grosu
- 发表：*Proceedings of the 27th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages*, pp. 390-402, 2000
- DOI：`10.1145/325694.325746`
- 链接：https://doi.org/10.1145/325694.325746
- 形式主义：`Hierarchic Reactive Machines / Modes (HRM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：语义精化 / refinement calculus
- 工具/实现获取方式：论文未给出独立可下载实现；机器可处理入口是 mode tuple、closure construction、macro-transition semantics、trace language、mode refinement 与 assume-guarantee rule。文中明确把它放在 reactive modules / `Mocha` 语境下。
- 标准/格式获取方式：原文没有独立交换标准，核心承载方式是 hierarchic modes、entry/exit points、global/local variables、default entry/exit、group transitions 与 trace-based denotational semantics。

## 简报

这篇论文的重要性在于，它把 `HRM` 从“有层次的 mode 图”推进成了真正有语义层次的模型族。作者的核心判断很明确：从 `Statecharts` 到 `UML`，behavior hierarchy 长期只是语法层次；而 `HRM` 必须拥有观察语义、trace semantics 与 refinement calculus，才能支撑模块化推理。对当前演化树来说，这篇条目不是再开一条新支，而是把 `HRM` 这条支线从“reachability 可分析”进一步补强成“语义上可精化、可组合”的稳定经典节点。

- 形式主义定位：`HSM` 之后 richer semantic hierarchy 的代表家族之一，强调 mode 接口、变量作用域、history 与 refinement。
- 构造方式简述：模型以 mode 为基本对象；mode 由 entry/exit、全局/局部变量、submodes 与 guarded transitions 构成，并通过 default entry/exit 表达 history 与 group transition。
- 基础设施与场景简述：虽然标题强调 refinement，但真正收进文库的是 `HRM` 模型本体，因为论文给出了其观测语义、组合性和 mode hierarchy 的正式口径。

```text
hierarchical mode graph -> closure / macro-step semantics -> trace language -> refinement / assume-guarantee over modes
```

## 形式主义定义与核心对象

### 定义对象

原文的中心对象是 mode。mode 不是单纯的嵌套状态，而是一个带接口、带变量作用域、可以重用、可以记忆 history 的行为单元。外界只能通过 entry / exit 与它交互，因此它天然适合做 black-box reasoning。

### 核心抽象

原文给出的 mode 可以整理为：

$$
M = (E,X,V_r,V_w,V_l,SM,T)
$$

上式中的符号逐项解释如下：

1. `E` 是 regular entry points 集合。
2. `X` 是 regular exit points 集合。
3. `V_r` 是 global read variables。
4. `V_w` 是 global write variables。
5. `V_l` 是 local variables。
6. `SM` 是 submodes 集合。
7. `T` 是 transitions 集合，每条 transition 连接某个 entry/exit/control point，并带有 action / guarded command。

mode 关闭后的 closure `c(M)` 会显式补入 default entry `de` 与 default exit `dx` 相关迁移，从而把 history 与 group transition 语义显化。

原文对 refinement 的核心判定可压成：

$$
M \preceq N \iff L_M \subseteq L_N
$$

这里的符号逐项解释如下：

1. `L_M` 是 mode `M` 的 trace language。
2. `L_N` 是 mode `N` 的 trace language。
3. `\preceq` 表示 `M` 细化 `N`，即 `M` 的行为不超出 `N` 允许的观察行为。

### 一个最小例子与通俗解释

原文用 village telephone system 解释 mode 非常直观。一个连接控制 mode 可能有：

1. `disconnected` 子模式；
2. `connected` 子模式；
3. `drooping` 子模式；
4. 若内部无边可走，就从 default exit 把控制交回上一层；
5. 若稍后通过 default entry 重新进入，又会恢复之前的局部历史位置。

通俗地说，`HRM` 像“一个带输入口、输出口、局部变量和历史寄存器的小状态机盒子”。它比普通 `HSM` 多的，不只是更复杂的图，而是“这个盒子对外暴露什么、隐藏什么、能否被另一个盒子安全替换”的正式语义。

### 运行 / 接受 / 转移语义

原文把 mode 的运行解释成 macro-transition。可保守压成：

$$
(e,s) \xRightarrow{M} (x,t)
$$

上式中的符号逐项解释如下：

1. `e \in E \cup \{de\}` 是环境把控制交给 mode 的入口点。
2. `x \in X \cup \{dx\}` 是 mode 把控制还给环境的出口点。
3. `s` 是进入时对变量的赋值状态。
4. `t` 是完成一个 macro-step 后的赋值状态。

trace 语义则通过对 global variables 投影得到：

$$
L_M = \pi_{V_g}(\sigma_0,\sigma_1,\ldots)
$$

其中 `V_g = V_r \cup V_w`。这意味着：mode 的真正观察语义，不是内部每一步怎么跳，而是外界能从全局变量与接口点上看到什么。

### 语义边界

原文明确区分了几件事：

1. `HRM` 不是单纯的 `Statecharts` 语法糖，而是带观察语义的 hierarchy。
2. 这里的 hierarchy 是 semantic hierarchy，不只是 syntactic nesting。
3. 模型仍然是离散 reactive model，不引入 clocks 或连续流。
4. 重点是 behavior hierarchy，而不是 architectural hierarchy 本身。

### 关键性质与判定边界

这篇论文最关键的“性质”不是某个复杂度数字，而是两个语义规则：

$$
M \preceq N \iff L_M \subseteq L_N
$$

以及组合性：

$$
P \preceq Q \Rightarrow P \parallel R \preceq Q \parallel R
$$

这里的第二条是对 reactive modules 式组合性的继承，表示 refinement 与组合构造相容。

原文还给出 circular assume-guarantee rule，其直觉可以压成：

$$
P_1 \parallel Q_2 \preceq Q_1 \land Q_1 \parallel P_2 \preceq Q_2
\Rightarrow
P_1 \parallel P_2 \preceq Q_1 \parallel Q_2
$$

这说明 `HRM` 不仅是能画出来的层次状态机，而且是能支撑模块化证明规则的层次状态机。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | mode 是一等对象。 |
| 事件 / 触发 | 强支持 | transitions 带 guarded commands。 |
| 守卫 / 数据 | 强支持 | 全局/局部变量与作用域是核心。 |
| 层次 | 强支持 | submodes、reuse、history 都属于 hierarchy 本体。 |
| 并发 / 同步 | 部分支持 | 通过 conjunctive modes 与 modules 组合进入并发。 |
| 时间约束 | 不支持 | 无显式 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | trace semantics、refinement calculus、assume-guarantee。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| mode tuple | `$M=(E,X,V_r,V_w,V_l,SM,T)$` | `HRM` 的 canonical mode definition。 |
| macro-transition | `$(e,s)\xRightarrow{M}(x,t)$` | mode 级黑盒执行语义。 |
| trace refinement | `$M \preceq N \iff L_M \subseteq L_N$` | 观察语义上的精化准则。 |
| compositionality | `$P \preceq Q \Rightarrow P \parallel R \preceq Q \parallel R$` | mode constructors 与 refinement 相容。 |
| assume-guarantee | `$P_1\parallel Q_2 \preceq Q_1 \land Q_1\parallel P_2 \preceq Q_2 \Rightarrow P_1\parallel P_2 \preceq Q_1\parallel Q_2$` | 支撑模块化推理的核心证明规则。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 mode 的 entry / exit 与变量接口。
2. 再定义 submodes。
3. 用 transitions 连接顶层 control points 与 submodes。
4. 最后通过 closure 显式补入 default entry/exit 语义。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. mode tuple；
2. default entry / exit closure；
3. macro-transition relation；
4. trace language 与 refinement 关系。

### 交换与互操作

这篇文献在谱系上主要承担：

1. 为 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md) 已经提出的 `HRM` 补上 refinement-calculus 语义；
2. 将 `HRM` 与 reactive modules / `Mocha` 风格模块化推理接通；
3. 把 `Statecharts` 式 behavior hierarchy 从“语法层次”推进到“语义层次”。

## 配套基础设施

- 建模/编辑工具：论文置于 reactive modules / `Mocha` 语境，但未给独立下载入口。
- 解析/交换/元模型支持：核心是 mode、control points、closure 与 trace semantics。
- 仿真/执行支持：通过 macro-step / micro-step 语义执行。
- 验证/分析支持：refinement、compositional reasoning、assume-guarantee。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，未形成通用工业标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要 black-box mode hierarchy 的反应式控制模型。
2. 需要变量作用域、history 与 group transition。
3. 需要模块化 refinement / assume-guarantee 推理。

### 需求前提

1. 行为可组织成有限 mode hierarchy。
2. 环境交互可通过 entry / exit points 与全局变量表达。
3. 关注的不只是“能否分析”，还包括“能否替换与细化”。

### 不适用或高成本场景

如果系统只是简单的 hierarchy 复用而没有作用域 / history / refinement 需求，普通 `HSM` 已足够；如果核心是递归 call-return，则 `RSM/uHSM` 更贴切。

## 与相邻形式主义的关系

相对 `HSM`，`HRM` 增加了 scoped variables、history 和 black-box mode interface；相对 reactive modules，它把行为 hierarchy 明确纳入语义；相对 `Statecharts`，它收紧了跨层交互方式，使得 refinement 与组合性可以正式表达。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机不只是“树状控制结构”，还可以是“具有可替换性和模块化证明规则的语义对象”。这对 Project 1 后续考虑 LLM 生成模型之后如何做验证与修复闭环非常重要。

### 作为目标形式主义还是中间表示

更适合作为高质量中间表示或理论对照族，而不是直接工业最终语言。

### 对需求到模型生成的启发

如果需求里出现“子模式必须被黑盒替换”“局部变量只在某个模式内生效”“打断后需要从历史位置恢复”这类表达，LLM 应该识别到这是 `HRM` 一类 richer hierarchy，而不是 plain `HSM`。

### 现实限制

其生态偏研究型，公开工具与标准化承载都较弱；但语义价值很高。

## 重要的相关工作

### 奠基或前身工作

- [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)
- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)

### 同类型或同家族工作

- reactive modules / `Mocha` 线路是其模块化背景。
- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 提供更简洁的 `HSM` 母线。

## 文献分类总结

- 这篇论文虽然以 refinement 为题，但其主要价值仍落在 `HRM` 模型本体语义完善上，而不是某个独立算法技巧。
- 它适合作为 `HRM` 支线上的经典补强条目，与 reachability 条目一起把这条分支补完整。
- 在演化树里，它更像 `HRM` 节点的“语义与精化说明依据”，而不是另一棵平行新树。
