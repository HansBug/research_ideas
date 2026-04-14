# 反转有界单向多计数器机层级 / Hierarchy of reversal bounded one-way multicounter machines

## 基本信息

- 标题：Hierarchy of reversal bounded one-way multicounter machines
- 中文标题：反转有界单向多计数器机层级
- 作者：Juraj Hromkovič
- 发表：*Kybernetika*, 22(2):200-206, 1986
- DOI：原文未提供
- 链接：https://dml.cz/bitstream/handle/10338.dmlcz/125016/Kybernetika_22-1986-2_8.pdf
- 形式主义：`One-Way Reversal-Bounded Multicounter Machines / One-Way Reversal-Bounded Partially Blind Multicounter Machines`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论分析
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是单向输入头、有限控制、多个计数器、计数器符号测试以及“接受运行的反转次数上界”。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 one-way multicounter machine、partially blind multicounter machine、接受运行与 reversal bound 类记号 `R(f)`。

## 简报

这篇论文的价值不是重新定义一般 `Counter Machine`，而是把“单向输入 + 多计数器 + 反转次数受输入长度函数控制”这条分支稳定拉出来，并且同时处理普通 one-way multicounter 与 one-way partially blind multicounter 两个近邻 family。对当前文库来说，它正好把 [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md) 往下细分到“单向 + 局部盲化 + reversal hierarchy”这一更贴近演化树的节点。

- 形式主义定位：`Counter Machines -> Reversal-Bounded Multicounter Machines` 下的单向输入子枝，并顺带补出 partially blind 近邻。
- 构造方式简述：在 one-way 多计数器机上，对接受运行中每个计数器从“递增到递减”或反向切换的次数施加函数型上界 `f(n)`。
- 基础设施与场景简述：原文是纯理论工作，但给出了 `COUNTER-R(f)`、`PBLIND-R(f)`、`QR-DPBLIND-R(g)` 等标准类记号与 hierarchy 结论，足以作为树上的稳定家族节点。

```text
线性词输入 -> 有限控制 + 多计数器 -> one-way 读取 -> reversal 次数按 f(n) 受限 -> hierarchy / separation
```

## 形式主义定义与核心对象

### 定义对象

论文第 2 节先用自然语言回顾 two 个母模型：

1. one-way multicounter machine：动作依赖当前状态、当前输入符号以及每个计数器是零还是正。
2. one-way partially blind multicounter machine：看不到计数器零/正信息；若某步使计数器跌到负值，则该计算中止且不接受。

原文把 formal definition 外引到更早文献，但当前条目真正新增的是“接受运行的 reversal complexity 作为单独资源”。

### 核心抽象

按论文第 2 节的机器组成与后续 `L_R^f(A)` 记号，可把 one-way multicounter machine 保守整理成：

$$
A = (Q, \Sigma, k, \delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限控制状态集。
2. `\Sigma` 是输入字母表。
3. `k` 是计数器个数。
4. `\delta` 依赖当前状态、当前输入符号以及计数器零/正符号，输出下一状态、输入头是否右移以及每个计数器的 `-1/0/+1` 更新。
5. `q_0` 是初始状态。
6. `F` 是接受状态集。

若把计数器向量记为 `\vec c \in \mathbb N^k`，把一次接受运行记为 `\rho`，则当前论文关心的不是裸语言 `L(A)`，而是 reversal-bounded 版本：

$$
L_R^f(A) = \{\, w \in L(A) \mid \exists \rho \text{ accepting run on } w,\ \mathrm{rev}(\rho) \le f(|w|) \,\}
$$

上式中的符号逐项解释如下：

1. `f` 是定义在输入长度上的实值函数。
2. `|w|` 是输入词 `w` 的长度。
3. `\mathrm{rev}(\rho)` 是运行 `\rho` 中计数器由“增”切到“减”或由“减”切到“增”的总次数。
4. `L_R^f(A)` 只保留那些存在低 reversal 接受运行的输入。

进而，论文把机器类 `M` 的 `R(f)` 版本写成类层面闭包：

$$
\mathcal L_R^f(M) = \bigcup_{B \in M} L_R^f(B)
$$

### 一个最小例子与通俗解释

最小例子仍可以取：

$$
L = \{ a^n b^n \mid n \ge 0 \}
$$

一台单向单计数器机的直觉性运行是：

1. 读取 `a` 段时每见一个 `a` 就把计数器加一。
2. 切到 `b` 段后每见一个 `b` 就把计数器减一。
3. 若串尾进入终态且计数器回空，则接受。

这条运行只发生一次“由增转减”的相位切换，因此它落在 `R(1)` 之内。通俗地说，反转有界单向多计数器机就是“只允许少量加减相位切换的 one-way counter machine”；它比普通 `FA` 强，因为它能记数；但它又比任意多次来回折腾计数器的一般 multicounter machine 更瘦，因此更容易出现严格层级与可分离性。

### 运行 / 接受 / 转移语义

对普通 one-way multicounter machine，接受纪律仍是“终态 + 所有计数器清空”。论文再把接受运行上的 reversal 次数作为过滤条件，因此真正被该 family 采纳的语言语义是上面的 `L_R^f(A)` 而不是裸 `L(A)`。

对 partially blind 变体，还需额外满足：

$$
\text{if some counter would become negative, the computation blocks and rejects}
$$

这意味着 `pblind` family 不能在转移时显式分支于“该计数器是否为零”，只能被动依靠“负值非法”来收束运行。

### 语义边界

这条 family 的边界很明确：

1. 输入对象是 one-way 线性词，不是树或网格。
2. 无界信息只来自 `k` 个计数器，不是一般栈字或带内容。
3. 额外资源不是时间上界本身，而是接受运行里的 reversal 次数函数上界。
4. `partially blind` 与普通版本共享同一条树枝，但前者进一步去掉了计数器零测试能力。

### 关键性质与判定边界

论文的主结论不是某个孤立算法，而是“更小的 reversal 上界无法被时间、非确定性和计数器数量补偿”。核心可压成：

$$
\mathcal L(\mathrm{QR\mbox{-}DPBLIND\mbox{-}R}(g)) \setminus \mathcal L(\mathrm{COUNTER\mbox{-}R}(f)) \neq \varnothing
$$

这里的含义是：在文中给定的增长条件下，只要 `f(n) = o(g(n))`，则即便右边允许更一般的 multicounter machine、非确定性与无界时间，也无法覆盖左边那个“deterministic + quasirealtime + partially blind + 更大 reversal bound”的类。

论文随即推出层级结论，例如：

$$
\mathcal L(\mathrm{QR\mbox{-}PBLIND\mbox{-}R}(f)) \subsetneq \mathcal L(\mathrm{QR\mbox{-}PBLIND\mbox{-}R}(g))
$$

这说明对同一条 `one-way / pblind` 母线，允许的 reversal 上界确实形成严格 hierarchy，而不是可被别的资源吞掉。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍保留有限控制状态。 |
| 事件 / 触发 | 强支持 | 由当前输入符号和计数器零/正信息驱动；`pblind` 版本则不看零/正。 |
| 守卫 / 数据 | 部分支持 | 数据来自多个整数计数器，但守卫很弱，核心额外资源是 reversal 次数。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 不支持 | 单机串行识别模型。 |
| 时间约束 | 不支持 | 讨论的是 complexity resource，不是显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散计数模型。 |
| 可执行 / 可验证性 | 强理论支持 | hierarchy、separation 与 cycle 分析都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| family 骨架 | `$A=(Q,\Sigma,k,\delta,q_0,F)$` | 把 one-way multicounter 分支压成稳定的机器骨架。 |
| reversal 过滤语义 | `$L_R^f(A)$` | 当前论文真正关心的是“接受运行中 reversal 次数受限”的语言。 |
| 类层面版本 | `$\mathcal L_R^f(M)=\bigcup_{B\in M}L_R^f(B)$` | 便于直接陈述 hierarchy。 |
| 主分离结论 | `$\mathcal L(\mathrm{QR\mbox{-}DPBLIND\mbox{-}R}(g)) \setminus \mathcal L(\mathrm{COUNTER\mbox{-}R}(f)) \neq \varnothing$` | 更大的 reversal 上界不能被其他资源补偿。 |
| 严格层级 | `$\mathcal L(\mathrm{QR\mbox{-}PBLIND\mbox{-}R}(f)) \subsetneq \mathcal L(\mathrm{QR\mbox{-}PBLIND\mbox{-}R}(g))$` | 同一母线内部形成稳定 hierarchy。 |

## 构造方式与承载格式

### 建模入口

建模时需要先决定：

1. 输入是否必须 strictly one-way。
2. 需要几个计数器。
3. 接受运行里的增减相位切换是否天然很少。
4. 是否还能保留零测试，还是应该进入 partially blind 版本。

### 机器可处理承载方式

原文的承载方式是机器骨架、运行、cycle characteristic 和 `R(f)` 类记号，不涉及图形 DSL 或工程化交换格式。

### 交换与互操作

它与以下理论对象互操作最紧：

1. [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md) 的 counter-machine 母线。
2. [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md) 的一般 reversal-bounded multicounter family。
3. 本目录下后续的 zerotest-bounded one-way multicounter 分支。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `COUNTER / PBLIND / QR-* / R(f)` 这些 machine-class 口径。
- 仿真/执行支持：可按配置和计数器更新关系直接执行。
- 验证/分析支持：cycle characteristic、hierarchy 与 separation proof 是核心。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 classic automata theory 中 counter-family 的细分理论节点。

## 适用场景与需求前提

### 适用场景

适用于需要在 one-way 词语言模型里表达“有限控制 + 少量无界计数 + 很少相位切换”的情形。

### 需求前提

1. 输入必须是线性词。
2. 无界记忆主要是计数，而不是任意嵌套栈结构。
3. 系统行为天然呈现少量“只增一阵、再减一阵”的相位结构。

### 不适用或高成本场景

如果需求需要频繁来回修改计数器，reversal-bounded family 会很别扭；如果需要真正的调用/返回嵌套，`PDA` 或 nested-stack family 更自然。

## 与相邻形式主义的关系

相对 [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)，它把一般 counter family 收紧到了 one-way 且 reversal-bounded 的分支；相对 [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)，它进一步强调 one-way 输入与 partially blind 近邻；相对 [zerotesting-bounded-one-way-multicounter-machines/desc.md](../zerotesting-bounded-one-way-multicounter-machines/desc.md)，后者把资源焦点转到 zerotest 次数，而不是 reversal 次数。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Counter Machines -> Reversal-Bounded Multicounter Machines` 下面一直偏粗的单一节点，细化成“单向 + partially blind + reversal hierarchy”这一更可继续生长的树枝。

### 作为目标形式主义还是中间表示

它更适合作为谱系树节点和理论参照，而不是控制系统需求自动建模的直接终点；但它对“有限控制 + 有限相位切换的计数约束”很有启发。

## 重要的相关工作

1. [counter-machines-and-counter-languages/desc.md](../counter-machines-and-counter-languages/desc.md)：更一般的 `Counter Machines` 母节点。
2. [reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md](../reversal-bounded-multicounter-machines-and-their-decision-problems/desc.md)：把 reversal bound 放到更一般 multicounter family 上。
3. [zerotesting-bounded-one-way-multicounter-machines/desc.md](../zerotesting-bounded-one-way-multicounter-machines/desc.md)：同一条 one-way multicounter 母线上的另一类受限资源。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它稳定命名并分离了 one-way reversal-bounded multicounter / partially blind multicounter 家族，而不是只讨论某个证明技巧。
- 它应挂在 `Counter Machines -> Reversal-Bounded Multicounter Machines` 之下，作为继续向 `partially blind` 和 `zerotest-bounded` 扩树的中间节点。
- 它不是 DSL、工具或应用论文，也不是只研究某个固定语言的 case paper。
