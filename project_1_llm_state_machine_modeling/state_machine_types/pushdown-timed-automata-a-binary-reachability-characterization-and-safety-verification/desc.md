# 下推时间自动机：二元可达性刻画与安全验证 / Pushdown timed automata: a binary reachability characterization and safety verification

## 基本信息

- 标题：Pushdown timed automata: a binary reachability characterization and safety verification
- 中文标题：下推时间自动机：二元可达性刻画与安全验证
- 作者：Zhe Dang
- 发表：*Theoretical Computer Science*, 302(1-3):93-121, 2003
- DOI：`10.1016/S0304-3975(02)00743-0`
- 链接：https://arxiv.org/pdf/cs/0110010.pdf
- 形式主义：`Pushdown Timed Automata (PTA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论分析
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `PTA` 元组、configuration 语义、pattern abstraction 与 pattern graph。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `PTA` 的状态-时钟-栈三元配置和 progress / reset transition 规则。

## 简报

这篇论文把 `Timed Automata` 和 `Pushdown Automata` 正式接到一起，得到一种既有 dense clocks、又有无界栈的实时递归模型。它最重要的不只是“模型存在”，而是给出了该 family 的可判定 binary reachability characterization，从而把许多普通 region 技术无法直接表达的 mixed linear safety property 拉回到了可验证范围内。

- 形式主义定位：`Timed Automata` 主干上的 timed-pushdown 母节点，面向带递归调用和无界栈的实时控制流。
- 构造方式简述：在有限状态和 dense clocks 上再加一个 pushdown stack；离散边同时携带 clock reset 与 stack rewrite。
- 基础设施与场景简述：核心基础设施不是工程工具，而是 `pattern` 抽象、pattern graph 与 `(D+NPCA)`-definable binary reachability。

```text
timed automaton + pushdown stack -> timed recursive control flow -> pattern abstraction -> binary reachability -> mixed linear safety verification
```

## 形式主义定义与核心对象

### 定义对象

`PTA` 的目标对象不是普通 timed word，而是“有限控制 + dense clocks + 无界栈”的递归实时系统。它适合描述带 procedure call / return、栈式上下文和时限约束的控制流程。

### 核心抽象

原文给出的 `PTA` 元组是：

$$
A = (S, \{x_1,\ldots,x_k\}, Inv, R, \Gamma, PD)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `x_1,\ldots,x_k` 是 dense clocks。
3. `Inv:S\to C` 给每个状态分配 clock invariant。
4. `R:S\times S\to C\times 2^{\{x_1,\ldots,x_k\}}` 给每条边分配 reset condition 和 reset 集合。
5. `\Gamma` 是栈字母表。
6. `PD:S\times S\to \Gamma\times\Gamma^*` 给每条边分配 stack operation；若 `PD(s_1,s_2)=(a,\gamma)`，则该边把栈顶符号 `a` 替换为字符串 `\gamma`。

语义配置写成：

$$
(s,v,w)
$$

上式中的符号逐项解释如下：

1. `s` 是当前控制状态。
2. `v` 是时钟赋值。
3. `w\in\Gamma^*` 是当前栈内容。

### 一个最小例子与通俗解释

一个最小直觉例子是“调用某个子过程后必须在 `5` 个时间单位内返回”：

1. 在状态 `Call` 进入边时，把返回标记 `r` 压入栈顶，并把 clock `x` reset 为 `0`。
2. 系统进入子过程内部状态，期间可以继续让时间流逝。
3. 当执行返回边时，要求当前栈顶是 `r`，并检查 `x \le 5`，然后把 `r` 弹出。

通俗地说，`PTA` 就像“给 timed automaton 加了一只真正会长大的栈”。普通 `TA` 只有有限控制和时钟，无法记住无界层级的调用上下文；`PTA` 则把“调用深度”和“时间约束”同时保留了下来。

### 运行 / 接受 / 转移语义

原文把一步转移分成两类。progress transition 可写成：

$$
(s_1,v_1,w_1)\to_A(s_2,v_2,w_2)
$$

其中若是时间流逝步，则要求：

$$
s_1=s_2,\quad w_1=w_2,\quad \exists \delta>0:\ v_2=v_1+\delta
$$

并且对任意 `0\le\delta'\le\delta` 都满足：

$$
v_1+\delta' \in Inv(s_1)
$$

reset transition 则要求：

$$
v_1\in Inv(s_1)\land c,\quad v_1\downarrow_r=v_2\in Inv(s_2),\quad w_1=aw,\quad w_2=\gamma w
$$

上式中的符号逐项解释如下：

1. `c` 是边上的 clock condition。
2. `r` 是被 reset 的时钟集合。
3. `a` 是当前栈顶符号。
4. `\gamma` 是替换到栈顶的新字符串。

### 语义边界

相对普通 `Timed Automata`，它新增了无界栈，因此可以表达递归与无限调用上下文；相对普通 `Pushdown Automata`，它新增了 dense clocks 和 invariant / reset 约束，因此能表达“何时调用 / 何时返回”的实时限制。

### 关键性质与判定边界

论文最关键的结果是：`PTA` 的 binary reachability 仍然有可判定刻画。可保守写成：

$$
\to_A^* \text{ is } (D+\mathrm{NPCA})\text{-definable}
$$

其中 `D` 表示 dense clocks 的线性约束部分，`NPCA` 表示对离散 pushdown 部分的自动机化刻画。对没有栈的特例，也就是普通 `Timed Automata`，论文进一步得到：

$$
\to_A^* \text{ is definable in the additive theory of reals and integers}
$$

这意味着不仅 region reachability 可判，某些混合实数时钟和无界离散变量的 safety property 也能落到自动验证。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限控制状态 `S` 始终存在。 |
| 事件 / 触发 | 强支持 | 离散边可同时触发 reset 与 stack rewrite。 |
| 守卫 / 数据 | 强支持 | 有 invariant、reset condition 和栈顶匹配。 |
| 层次 | 强支持 | 无界栈显式提供调用层次。 |
| 并发 / 同步 | 不支持 | 原始模型不是并发网络。 |
| 时间约束 | 强支持 | dense clocks 与 invariant 是模型核心。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | 核心贡献就是 pattern-based binary reachability。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A = (S,\{x_1,\ldots,x_k\},Inv,R,\Gamma,PD)$` | 给 timed-pushdown family 一个稳定的标准骨架。 |
| 配置 | `$(s,v,w)$` | 同时保留控制状态、时钟值和栈内容。 |
| progress 语义 | `$v_2=v_1+\delta$` 且 `$v_1+\delta' \in Inv(s)$` | 时间流逝时必须持续满足 invariant。 |
| reset + 栈操作 | `$v_1\downarrow_r=v_2,\ w_1=aw,\ w_2=\gamma w$` | 离散边同时更新 clocks 和 stack。 |
| 核心结论 | `$\to_A^*$ is `(D+NPCA)`-definable` | binary reachability 可自动机化。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 哪些信息应该进有限控制状态。
2. 哪些约束需要作为 dense clocks 保存。
3. 哪些调用上下文必须进栈，而不能靠有限状态近似掉。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `PTA` 元组。
2. configuration 语义。
3. pattern abstraction 与 pattern graph。

### 交换与互操作

它和 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 `Timed Automata` 母线、[visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md) 的结构化栈母线以及后续的 dense-timed / recursive timed 分支都有直接互操作意义。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `pattern` 抽象、pattern graph 与 binary relation 编码。
- 仿真/执行支持：可按 progress / reset 两类语义直接执行。
- 验证/分析支持：binary reachability、mixed linear safety verification、timed-automata special-case characterization。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 timed verification 与 pushdown verification 交叉处的经典理论家族。

## 适用场景与需求前提

### 适用场景

适合带递归调用、过程栈和显式实时时限的程序模型、协议模型与控制逻辑理论建模。

### 需求前提

1. 系统既有无界调用上下文，又有 dense-time 约束。
2. 这些上下文最好能由栈式 discipline 表达。
3. 需求关心的不只是普通 reachability，而是带线性关系的更强安全性质。

### 不适用或高成本场景

如果系统没有无界栈需求，普通 `Timed Automata` 更简单；如果只有栈而没有时间，则普通 `Pushdown Automata` 更直接。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`PTA` 多出真正的 pushdown store；相对 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，它更偏“栈机器”而不是“组件调用 + clock passing”；相对 [dense-timed-pushdown-automata/desc.md](../dense-timed-pushdown-automata/desc.md)，这篇条目更强调 binary reachability characterization，而不是 later `EXPTIME` symbolic-region algorithm。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Timed Automata` 主干明确接到 `timed pushdown` 这条经典 family 上，使演化树不再只在 event-clock / stopwatch / parametric / recursive 调参方向扩展。

### 作为目标形式主义还是中间表示

更适合作为理论目标形式主义或后续更工程化 timed-recursive 模型的母节点，而不是直接作为工业交付格式。

### 对需求到模型生成的启发

当需求同时出现“调用层次不能丢”和“每层调用都有时间窗口”时，LLM 生成 `PTA` 比强行把系统压平到普通 `TA` 更自然。

### 现实限制

它的价值主要在理论可达性与安全验证边界，工程生态远弱于 `UPPAAL` 一类普通 `TA` 工具链。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)
- [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)

### 同类型或同家族工作

- [dense-timed-pushdown-automata/desc.md](../dense-timed-pushdown-automata/desc.md)
- [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的“基础设施”就是 pattern graph 和 binary relation characterization。

### 与本研究关系最紧的工作

- 这篇论文最适合被当作 `Timed Automata -> Pushdown Timed Automata` 母节点条目来挂树。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
