# 零测试有界单向多计数器机 / Zerotesting bounded one-way multicounter machines

## 基本信息

- 标题：Zerotesting bounded one-way multicounter machines
- 中文标题：零测试有界单向多计数器机
- 作者：Pavol Ďuriš、Juraj Hromkovič
- 发表：*Kybernetika*, 23(1):13-18, 1987
- DOI：原文未提供
- 链接：https://dml.cz/bitstream/handle/10338.dmlcz/124775/Kybernetika_23-1987-1_2.pdf
- 形式主义：`Zerotesting-Bounded One-Way Multicounter Machines`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论分析
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是单向输入头、多计数器、quasirealtime 约束、以及接受运行中的 zerotest 次数上界。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 one-way multicounter machine、`Z(f)` / `R(f)` 类记号与相应 hierarchy 结论。

## 简报

这篇论文的重点不是再补一个“会数数的自动机”，而是把 zero-test 本身单独提升为 complexity resource。也就是说，它不只问机器有没有计数器、能不能 reversal，而是问“接受运行里到底允许做多少次零测试”。对当前文库来说，它正好沿着 [hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md](../hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md) 那条 one-way multicounter 支线继续长出一个近邻节点。

- 形式主义定位：`Counter Machines` 母线下，和 one-way reversal-bounded family 紧邻的 zerotest-complexity 分支。
- 构造方式简述：机器骨架仍是 one-way multicounter machine，但语言语义改成“存在一条接受运行，其 zerotest 次数不超过 `f(|w|)`”。
- 基础设施与场景简述：原文是纯理论工作，不过它把 `Z(f)` 与 `R(f)` 两种资源量化放到同一张图上比较，因此对演化树特别有价值。

```text
线性词输入 -> one-way multicounter machine -> 接受运行中的 zerotest 次数受限 -> hierarchy / 与 reversal complexity 对照
```

## 形式主义定义与核心对象

### 定义对象

论文延续 one-way multicounter machine 的既有定义：有限控制、单向输入头和若干计数器，转移依赖当前输入符号、控制状态以及每个计数器是否为零。当前论文新增的 formal focus 是 zerotest complexity measure。

### 核心抽象

沿用前一条 one-way multicounter 母线，可把机器骨架保守写成：

$$
A = (Q, \Sigma, k, \delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限控制状态集。
2. `\Sigma` 是输入字母表。
3. `k` 是计数器个数。
4. `\delta` 决定下一状态、输入头移动和各计数器的 `-1/0/+1` 更新。
5. `q_0` 是初始状态。
6. `F` 是接受状态集。

论文把 reversal-bounded 记号 `L_R^f(A)` 保留下来，同时引入 zerotest-bounded 版本：

$$
L_Z^f(A) = \{\, w \in L(A) \mid \exists \rho \text{ accepting run on } w,\ \mathrm{zt}(\rho) \le f(|w|) \,\}
$$

上式中的符号逐项解释如下：

1. `\rho` 是输入 `w` 上的一条接受运行。
2. `\mathrm{zt}(\rho)` 是运行 `\rho` 中 zero-test 事件的次数；按原文口径，它对应“机器把计数器置空/检查为空”的次数资源。
3. `f(|w|)` 是输入长度驱动的 zerotest 上界。
4. `L_Z^f(A)` 只保留那些有低 zerotest 接受运行的词。

对应类层面记号则是：

$$
\mathcal L_Z^f(M) = \bigcup_{B \in M} L_Z^f(B)
$$

### 一个最小例子与通俗解释

一个最直观的例子仍然是：

$$
L = \{ a^n b^n \mid n \ge 0 \}
$$

机器的工作方式可以理解成：

1. 在 `a` 段持续加一。
2. 在 `b` 段持续减一。
3. 只在最终检查“计数器是否回到零且进入终态”时做一次关键 zerotest。

这意味着该运行可以自然落在 `Z(1)`。通俗地说，zerotesting-bounded multicounter machine 像是在问：“你可以一直记数，但真正依赖‘数到零没’这件事的次数有多稀缺？”这和只限制 reversal 次数是不同维度的收束。

### 运行 / 接受 / 转移语义

机器的底层接受纪律仍然是“所有计数器回空且到达终态”。区别在于，当前论文把运行资源改写成：

$$
\text{accept under } Z(f) \iff \exists \rho \text{ accepting run with } \mathrm{zt}(\rho)\le f(|w|)
$$

因此，`Z(f)` family 允许很多次计数器增减，只要真正需要 zero-test 的次数足够少。

### 语义边界

这条 family 的边界是：

1. 输入仍是 one-way 线性词。
2. 数据载体仍只是多个计数器。
3. 额外资源是 zerotest 次数，而不是 reversal 次数、时钟数或栈深。
4. 论文重点是 hierarchy 和与 reversal complexity 的比较，不是新工程语法。

### 关键性质与判定边界

论文第一个核心结论是：对增长明显更慢的 zerotest 上界 `f` 和更快的 `g`，one-way deterministic quasirealtime multicounter family 出现严格层级：

$$
\mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(f)) \subsetneq \mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(g))
$$

原文给出的典型前提是：

$$
f(n) = o(g(n)), \quad g(n) = o(\log_2 n)
$$

第二个更有树上价值的结论，是 zerotest complexity 与 reversal complexity 之间并不能轻易互相替代：

$$
\mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(1)) \setminus \mathcal L(\mathrm{COUNTER\mbox{-}R}(f)) \neq \varnothing
$$

其中 `f(n)=o(n)`。也就是说，哪怕右边允许一般 nondeterministic multicounter machine 和无界时间，只要 reversal 上界是严格次线性的，它仍然接不住左边那个“只有一个 zerotest”的语言。

论文给出的 witness 语言可压成：

$$
L' = \{\, w \in \{a,b\}^* \mid \#_a(w)=\#_b(w),\ w=xy,\ x,y\in\{a,b\}^+ \Rightarrow \#_a(x)>\#_b(x) \,\}
$$

它说明一个 very small zerotest budget 也可能比 sublinear reversal budget 更关键。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限控制。 |
| 事件 / 触发 | 强支持 | 按输入符号和计数器零/正信息驱动。 |
| 守卫 / 数据 | 部分支持 | 数据由多计数器承载，但当前额外资源是 zerotest 次数。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 不支持 | 单机串行识别模型。 |
| 时间约束 | 不支持 | 讨论的是理论 complexity resource，不是显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散计数模型。 |
| 可执行 / 可验证性 | 强理论支持 | hierarchy、witness language 与与 reversal complexity 的 separation 都很清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| zerotest 过滤语义 | `$L_Z^f(A)$` | 把 zero-test 次数提升成第一类资源。 |
| 类层面版本 | `$\mathcal L_Z^f(M)=\bigcup_{B\in M}L_Z^f(B)$` | 便于直接陈述 hierarchy。 |
| 严格层级 | `$\mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(f)) \subsetneq \mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(g))$` | 较大的 zerotest budget 确实更强。 |
| 典型前提 | `$f(n)=o(g(n)),\ g(n)=o(\log_2 n)$` | 原文给出首批 non-constant zerotest hierarchy。 |
| 与 reversal 的分离 | `$\mathcal L(\mathrm{QR\mbox{-}DCOUNTER\mbox{-}Z}(1)) \setminus \mathcal L(\mathrm{COUNTER\mbox{-}R}(f)) \neq \varnothing$` | zerotest complexity 不能被 sublinear reversal complexity 取代。 |

## 构造方式与承载格式

### 建模入口

建模时要先判断：

1. 系统是否仍然是 one-way 词输入模型。
2. 关键难点是在“相位切换次数”还是“真正做零测试的次数”。
3. 是否需要 quasirealtime 约束来避免 stationary computation 任意膨胀。

### 机器可处理承载方式

原文的承载方式是 one-way multicounter machine、`Z(f)` / `R(f)` 记号、witness languages 和 cycle-analysis 证明，不涉及工程化格式。

### 交换与互操作

它与以下条目直接相邻：

1. [hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md](../hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md)：同一条 one-way multicounter 母线上的 reversal-bounded 近邻。
2. [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)：更一般的 reversal-bounded multicounter family。
3. [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)：更上层的 counter-machine 母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `COUNTER`、`QR-DCOUNTER`、`Z(f)` 与 `R(f)` 这些类记号。
- 仿真/执行支持：可按 one-way multicounter 配置直接执行。
- 验证/分析支持：hierarchy construction、witness languages 与 cycle reasoning 是主体。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 classic automata theory 里 counter-family 的 complexity-parameter 分支。

## 适用场景与需求前提

### 适用场景

适用于那些“计数可以很多，但真正依赖 zero-test 的次数很少”的线性词语言建模问题。

### 需求前提

1. 输入是线性词。
2. 无界存储可压成少量计数器。
3. 需求真正敏感的是 zero-test 预算，而不是一般数据比较。

### 不适用或高成本场景

如果需求主要依赖丰富数值守卫、任意栈结构或连续时间，这个 family 不自然；如果限制点其实是 reversal 次数，则前一篇 reversal-bounded 分支更直接。

## 与相邻形式主义的关系

相对 [hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md](../hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md)，它把“受限资源”从 reversal 改成 zerotest；相对 [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)，它更靠近 one-way deterministic quasirealtime family；相对 [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)，它依旧属于 counter-machine 母线，但切分维度更细。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Counter Machines` 支线继续补成“reversal-bounded / zerotest-bounded”两条相邻但不等价的资源约束分支，使演化树更接近经典 automata theory 的真实细分结构。

### 作为目标形式主义还是中间表示

它更适合作为谱系和能力边界条目，而不是控制系统自动建模的直接终点；但它对“哪些约束本质上是在稀疏做零检查”很有启发。

## 重要的相关工作

1. [hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md](../hierarchy-of-reversal-bounded-one-way-multicounter-machines/desc.md)：同一条 one-way multicounter 母线上的 reversal-bounded 版本。
2. [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)：更广义的 reversal-bounded multicounter family。
3. [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)：counter-machine 总母线。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它稳定引入了 `Z(f)` 这条新的 machine-family 口径，并证明其与 reversal complexity 的非平凡分离。
- 它应挂在 `Counter Machines` 主线上，并与 one-way reversal-bounded 分支保持紧邻关系。
- 它不是 DSL、工具或应用条目，也不是只讨论某个特定算法的旁支工作。
