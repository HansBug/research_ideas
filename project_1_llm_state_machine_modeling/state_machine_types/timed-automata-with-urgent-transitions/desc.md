# 带紧迫迁移的时间自动机 / Timed Automata with Urgent Transitions

## 基本信息

- 标题：Timed Automata with Urgent Transitions
- 中文标题：带紧迫迁移的时间自动机
- 作者：Roberto Barbuti, Luca Tesei
- 发表：*Acta Informatica*, 40(5):317-347, 2004
- DOI：`10.1007/s00236-003-0135-6`
- 链接：https://doi.org/10.1007/s00236-003-0135-6
- 形式主义：`Timed Automata with Urgent Transitions`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文给出 formal semantics 与 transformation to ordinary timed automata；当前目录保存作者公开 postprint。
- 标准/格式获取方式：原文没有交换标准，核心承载方式是普通边集 `E`、urgent 边集 `U`、entry-time counter `\delta_q` 和 region-based transformation。

## 简报

这篇论文把 `Timed Automata` 上的 urgency 从“状态中不许时间继续流”改成“某条 urgent transition 一旦被使能，就必须在固定窗口内执行，并且压过同状态下的 non-urgent transitions”。作者给出精确的 operational semantics，并证明从 timed-language 角度看，`Timed Automata with Urgent Transitions` 与普通 `Timed Automata` 表达力等价，但在规格层面能更短、更直接地表达 urgency 与 priority。对演化树来说，它很适合挂成 `Timed Automata` 主干下的 `Urgent Transitions` 子枝。

- 形式主义定位：`Timed Automata` 的 urgency / priority 语义扩展，重点不在增强语言表达力，而在增强规格表达便利性。
- 构造方式简述：把边分成 non-urgent `E` 与 urgent `U` 两类，并引入“自进入当前状态以来经过的时间”来判定 urgent window。
- 基础设施与场景简述：原文给出从 `TA_u^\ell` 到普通 `TA` 的 region-based transformation，因此这条分支既是新语义，也是可回收进经典 `TA` 工具链的模型本体。

```text
Timed Automata -> split edges into urgent / non-urgent -> fixed urgency window + priority -> transform back to ordinary TA
```

## 形式主义定义与核心对象

### 定义对象

论文研究的仍是 clocks + finite states 的 timed automata，只是其中一部分迁移被标成 urgent，并赋予额外语义。

### 核心抽象

给定常数 `\ell \in \mathbb Q_{>0}`，一个带紧迫迁移的时间自动机可写成：

$$
T_u^{\ell} = (Q,\Sigma,E,U,I,R,X)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是动作字母表。
3. `E` 是普通边集。
4. `U` 是 urgent 边集。
5. `I \subseteq Q` 是初始状态集。
6. `R \subseteq Q` 是 repeated states，用于接受语义。
7. `X` 是 clocks 集。

每条边都还是普通 timed-automata 风格的五元组：

$$
e \in Q \times \Phi(X) \times 2^X \times \Sigma \times Q
$$

区别只在于这条边属于 `E` 还是 `U`。

### 一个最小例子与通俗解释

最小例子可以取一个状态 `q`，其中普通边 `b` 在 `0 < x \le 1` 时可走，而 urgent 边 `a` 在 `x > 1` 后必须在 `1` 个时间单位的窗口内执行。于是当 `x` 刚超过 `1` 时，系统进入“必须尽快走 `a`”的阶段；如果再继续拖延，就违反 urgent semantics。

通俗地说，这个模型就是“给某些边加上一个从 enabling moment 开始计时的强制执行窗口”。它不像 deadline-based 模型那样把 urgency 完全揉进 guard/deadline 代数里，而是直接把 urgent 当成一类带优先级的边语义。

### 运行 / 接受 / 转移语义

论文把语义状态扩成三元组：

$$
(q,\nu,\delta_q)
$$

其中：

1. `q` 是当前 automaton state。
2. `\nu` 是当前 clock valuation。
3. `\delta_q` 是进入状态 `q` 以来已经流逝的时间。

普通时间步是：

$$
(q,\nu,\delta_q) \xrightarrow{\delta} (q,\nu+\delta,\delta_q+\delta)
$$

当没有 urgent 条件阻塞时，普通边可按普通 `TA` 规则执行；urgent 边则还要满足“未错过任何 urgent window，且没有更早失效的 urgent transition 被跳过”这类额外条件。论文正是用这些规则把“优先级 + 固定 urgency 窗口”形式化。

### 语义边界

作者特别强调：这条语义与早期 deadline-based urgency 不完全相同。deadline 线把 urgency 主要当作 transition-level predicate；这里的 urgent transition 则是“从 enabling time 起算固定长度 `\ell` 的强制执行窗口”，而且在窗口内对 non-urgent transitions 具有优先级。

### 关键性质与判定边界

论文最重要的结论是：

$$
TL(T_u^{\ell}) = TL(TA)
$$

也就是从 timed-language 角度看，带紧迫迁移的时间自动机并不比普通 `Timed Automata` 更强；但它能更紧凑地表达 urgency 和 priority。论文进一步给出三步 transformation，把 `TA_u^\ell` 变成接受同一语言的普通 `TA`。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态 `Q` 仍是离散骨架。 |
| 事件 / 触发 | 强支持 | urgent / non-urgent 边都以动作字母表为基础。 |
| 守卫 / 数据 | 强支持时钟守卫 | 边约束仍是 clocks 上的 predicate。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 支持 | 论文讨论了 parallel composition，但重点仍是单体 urgent semantics。 |
| 时间约束 | 强支持 | urgency window 直接是时间语义核心。 |
| 连续动态 / 随机性 | 不支持 | 仍是纯 timed automata 语义。 |
| 可执行 / 可验证性 | 强支持 | 可回译到普通 `TA`，保住经典 region 分析入口。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$T_u^{\ell}=(Q,\Sigma,E,U,I,R,X)$` | 为普通 `TA` 加上 urgent 边集。 |
| 语义状态 | `$(q,\nu,\delta_q)$` | 需要显式记住“进入当前状态以来过了多久”。 |
| urgency 窗口 | `$\ell \in \mathbb Q_{>0}$` | urgent transition 的固定强制执行窗口长度。 |
| 主结论 | `$TL(T_u^{\ell}) = TL(TA)$` | 语言表达力不增加，但规格表达更直接。 |
| 分析入口 | `TA_u^\ell \to TA` | 给经典 `TA` 工具和 region 理论留下接口。 |

## 构造方式与承载格式

### 建模入口

1. 先用普通 `TA` 方式确定状态、clocks 和 guards。
2. 再挑出哪些边必须在 enabled 后“尽快且优先”执行。
3. 为这些边放入 urgent 集 `U`，并给出统一或局部 urgency window。
4. 若后续要验证，可再用论文 transformation 回到普通 `TA`。

### 机器可处理承载方式

机器可处理承载方式是 `(Q,\Sigma,E,U,I,R,X)` 结构、operational semantics 和 region-form transformation。

### 交换与互操作

它和 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的经典 `TA` 母线直接相连，也和 [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md) 的 deadline-based urgency 分支构成紧邻关系：两者都讲 urgency，但语义视角不同。

## 配套基础设施

- 建模/编辑工具：原文未单列工具，但给出可落回普通 `TA` 的 transformation。
- 解析/交换/元模型支持：核心是 urgent/non-urgent 边划分、语义转移规则和 region-based construction。
- 仿真/执行支持：通过扩展后的 transition system `S(T_u^\ell)` 执行。
- 验证/分析支持：可回译到普通 `TA`，从而重用经典 timed-automata 理论。
- 代码生成/转换支持：论文核心贡献之一就是 preserving-language transformation。
- 标准化或社区生态：是 `Timed Automata` urgency 语义中的稳定经典节点。

## 适用场景与需求前提

### 适用场景

适合需要明确表达“某个边一旦 enabled 就必须尽快执行，且优先于其他边”的实时协议与控制规格。

### 需求前提

1. urgency 必须是 transition-level，而不是仅仅状态级不变量。
2. 需求里要能明确标出 enabling moment 与强制执行窗口。
3. 若后续还想回到普通 `TA` 工具链，窗口和 guards 需要保持在 region-friendly 约束内。

### 不适用或高成本场景

若 urgency 主要是组合代数与 deadline 约束问题，可能 [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md) 那条 deadline/timed-action 线更自然。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它在 `TA` 上增加的是 urgent-edge semantics，而不是新的 clocks 或新动力学；相对 [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md)，两者都表达 urgency，但 deadline 线偏 compositional algebra，这里偏 operational semantics 与 priority；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，后者强调 determinization，这里强调规格简洁性。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata` 主干下再补出一条稳定的 `Urgent Transitions` 语义分支，使 timed 树不再只停留在 clocks、priced、game、parametric 和 stopwatch 这些结构增强点。

### 作为目标形式主义还是中间表示

当需求里存在明确的“必须尽快执行且压过其他候选动作”的句式时，它可以直接作为目标模型；否则也可作为更一般 timed 需求的中间层。

### 对需求到模型生成的启发

自然语言里常见的“立即”“尽快”“一旦使能就优先处理”并不一定意味着换到 hybrid；很多时候它更像是 `urgent transition` 语义，应优先抽成这类 timed 分支。

### 现实限制

表达力并没有超出普通 `TA`，所以它的主要收益在规格层面；若只关心语言能力，不一定必须显式保留这一分支。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md)
- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供独立工程标准；主要基础设施是回译到普通 `TA` 的 transformation。

### 与本研究关系最紧的工作

- 它最适合挂成 `Timed Automata -> Timed Automata with Urgent Transitions` 的经典规格语义节点。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Timed Automata with Urgent Transitions`
- 论文角色：模型提出
- 核心功能：给 `TA` 增加基于 enabling time 的固定 urgency window 与优先级语义。
- 关键特性：urgent/non-urgent edge split、`(q,\nu,\delta_q)` 语义状态、priority、language-preserving transformation to `TA`。
- 构造方式：`T_u^{\ell}=(Q,\Sigma,E,U,I,R,X)`。
- 基础设施：可回译到普通 `TA`，无独立标准文件格式。
- 适用场景：需要显式“尽快执行/高优先级边”语义的实时规格。
- 需求前提：urgency 必须能落到 transition-level 且带固定窗口。
- 状态：🟢
