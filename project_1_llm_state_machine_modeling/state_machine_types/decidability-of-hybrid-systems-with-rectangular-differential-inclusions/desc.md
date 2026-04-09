# 带矩形微分包含的混成系统的可判定性 / Decidability of Hybrid Systems with Rectangular Differential Inclusions

## 基本信息

- 标题：Decidability of Hybrid Systems with Rectangular Differential Inclusions
- 中文标题：带矩形微分包含的混成系统的可判定性
- 作者：Anuj Puri, Pravin Varaiya
- 发表：收录于 *Computer Aided Verification*, LNCS 818, pp. 95-104, 1994
- DOI：`10.1007/3-540-58179-0_46`
- 链接：https://doi.org/10.1007/3-540-58179-0_46
- 形式主义：`Hybrid Automata with Rectangular Differential Inclusions`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未给公开工具；机器可处理入口是 rectangular differential inclusion、initialization relation 和 continuous/discrete-time consistency。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 location、differential inclusion、enabling condition 与 initialization relation 的数学定义。

## 简报

这篇论文把 `Hybrid Automata` 主干里的一个早期可判定子类钉得很清楚：每个 location 只允许常值矩形微分包含 `\dot x_i \in [L_i,U_i]`，并要求变量的微分包含只在变量被初始化，或变量正好处在整数值时才允许改变。作者证明这类系统的验证问题可判定，且生成语言是 regular。对演化树而言，它很适合作为 `Hybrid Automata` 下 `Rectangular Differential-Inclusion` 子枝的早期稳定节点，并为后面的 `Initialized Rectangular Automata` 留出明确父边。

- 形式主义定位：`Hybrid Automata` 主干上的矩形微分包含子类，比一般 `HA` 更受限，也更接近可判定边界。
- 构造方式简述：location 上挂常值矩形导数区间，边上挂 enabling condition 和 initialization relation，并限制“何时允许切换导数区间”。
- 基础设施与场景简述：论文核心是 decidability proof，而不是工程工具；但它已经把矩形 drift、region abstraction 和离散化桥接写得很清楚。

```text
Hybrid Automata -> rectangular differential inclusions -> initialization discipline -> regular language / decidable verification
```

## 形式主义定义与核心对象

### 定义对象

论文研究的是一类带 location 和连续状态 `x \in \mathbb R^n` 的 hybrid systems。每个 location 上不是一般微分方程，而是一个按坐标分解的常值矩形微分包含。

### 核心抽象

一个坐标 `x_i` 在某个 location 上满足：

$$
\dot x_i \in [L_i,U_i]
$$

这里 `L_i,U_i` 是整数，表示该分量导数可以在一个固定区间里变化，但不能超出这个区间。

论文给出的混成自动机骨架可保守写成：

$$
H = (L,\Sigma,D,Z,r)
$$

上式中的符号逐项解释如下：

1. `L` 是有限 locations 集。
2. `\Sigma` 是事件集。
3. `D:L\to B` 给每个 location 指派一个 differential inclusion。
4. `Z \subseteq L` 是初始 locations 集。
5. `r \subseteq L \times L \times \Sigma \times \Delta \times \mathcal A` 是边标签集合，其中每条边都含事件、enabling condition 和 initialization relation。

论文还把 initialization relation 写成：

$$
A = (A_1,\ldots,A_n)
$$

其中每个 `A_i` 要么是 `id`，表示 `x_i` 过边时保持不变；要么是区间 `[l_i,u_i]`，表示 `x_i` 在过边时被非确定性重置到该区间内某个值。

### 一个最小例子与通俗解释

可以把它想成一个“带漂移时钟的模式切换系统”：在 location `\ell_1` 中，时钟 `x` 不是固定以 `1` 递增，而是在 `[1,3]` 的斜率区间内漂移；当满足某个 guard 时切到 `\ell_2`，此时 `x` 可以被重置到一个新区间，然后在新的矩形微分包含下继续演化。

通俗地说，这类模型就是“每个模式里每个连续变量都只能在一个坐标轴对齐的速度盒子里跑”的混成自动机。它比一般 `HA` 弱，但正因为弱，才有机会把验证问题拉回可判定。

### 运行 / 接受 / 转移语义

论文先给出初始化关系对状态的作用：

$$
A[z] = \{z' \in \mathbb R^n \mid z'_i = z_i \text{ if } A_i=id,\ \ z'_i \in [l_i,u_i] \text{ if } A_i=[l_i,u_i]\}
$$

连续语义上，系统在 location `l` 内按 `D(l)` 演化；当状态满足边的 enabling condition `\delta` 时，可沿边跳转，并把状态更新到 `A[z]` 中某个值，再在新 location 的 differential inclusion 下继续流动。

论文还区分了 `continuous-time consistent` 与 `discrete-time consistent` 的路径语义，并以此搭桥到 regular-language 证明。

### 语义边界

作者明确指出，这个模型不包含 integration graphs 那类更一般的 hybrid systems；同时它要求 differential inclusion 的变化受到 initialization / integer-value 条件约束，因此比一般 `HA` 更严格。

### 关键性质与判定边界

论文主结论之一是：

$$
\mathcal L(H) \text{ is regular}
$$

更准确地说，作者先把 continuous-time system 与离散时间近似系统联系起来，再证明相应语言 regular，从而得到 verification decidability。就演化树而言，这条结论说明该分支不是“只是一个几何限制”，而是一个确实围绕可判定性组织起来的稳定家族。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 location 集 `L` 是离散骨架。 |
| 事件 / 触发 | 支持 | 边带事件标签和 enabling condition。 |
| 守卫 / 数据 | 强支持 | 边上显式有 enabling condition 与 initialization relation。 |
| 层次 | 不支持 | 原始模型不是层次混成自动机。 |
| 并发 / 同步 | 不支持 | 论文核心是单体子类及其可判定性。 |
| 时间约束 | 强支持 | 连续时间流动由矩形导数区间控制。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 支持非确定性的矩形微分包含。 |
| 可执行 / 可验证性 | 强理论支持 | 论文重点就是 decidability 与 regular-language 结果。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 微分包含 | `$\dot x_i \in [L_i,U_i]$` | 每维都限制在常值矩形导数区间。 |
| 模型骨架 | `$H=(L,\Sigma,D,Z,r)$` | 早期 rectangular hybrid 分支的基本自动机定义。 |
| 初始化关系 | `$A=(A_1,\ldots,A_n)$` | 过边时保持/重置各维坐标。 |
| 初始化作用 | `$A[z]=\{z' \mid \cdots\}$` | 给出跳转后的可能连续状态集。 |
| 主结论 | `$\mathcal L(H)$ is regular` | 由此得到 verification decidability。 |

## 构造方式与承载格式

### 建模入口

1. 先把系统拆成有限 locations。
2. 为每个 location 指定矩形微分包含。
3. 为每条边写 enabling condition 与 initialization relation。
4. 检查导数区间切换是否只发生在允许的初始化 / 整值条件下。

### 机器可处理承载方式

机器可处理承载方式是 location graph、rectangular differential inclusion、enabling condition 和 initialization relation，而不是 DSL 文件。

### 交换与互操作

它和 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md) 的一般 `Hybrid Automata` 主干直接相连，也为 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md) 里的 `Initialized Rectangular Automata` 提供更早的矩形子类背景。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 differential inclusion 与 initialization relation 的数学承载。
- 仿真/执行支持：可按 continuous/discrete consistency 语义展开。
- 验证/分析支持：regular-language 证明、离散化桥接和 decidability 结果。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 `Hybrid Automata` 矩形可判定子类的早期经典条目。

## 适用场景与需求前提

### 适用场景

适合有 bounded drift、矩形速度区间、可分段保守抽象的连续系统，以及想在 `HA` 主干里优先保住可判定性的建模场景。

### 需求前提

1. 连续变量的导数必须能按坐标独立地落进区间。
2. 系统切换时的连续状态更新能写成区间初始化或恒等保持。
3. 若希望落在论文子类中，导数区间变化必须满足其允许的初始化/整值条件。

### 不适用或高成本场景

对强耦合非矩形动力学、复杂非线性流或连续变量之间高度相关的系统，这一矩形近似会过于保守。

## 与相邻形式主义的关系

相对 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)，它是更受限、更偏 decidable subclass 的 `HA` 分支；相对 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，它更早、更偏“矩形微分包含本身”，而后者进一步系统化了 initialized rectangular 的边界。

## 与本研究的关系

### 对 Project 1 的价值

它可以把 `Hybrid Automata` 主干下的矩形分支往前补出一个更早的“矩形微分包含”节点，而不只是停在 1998 的 `Initialized Rectangular Automata`。

### 作为目标形式主义还是中间表示

更适合作为从一般连续需求到可判定混成模型之间的中间层或降阶目标。

### 对需求到模型生成的启发

如果自然语言需求里反复出现“速度在某个区间内漂移”“切换时把变量重置到一个范围里”，那就很适合先抽成这种 rectangular differential-inclusion 模型。

### 现实限制

它对流的限制很强，真实系统常常需要再做额外近似；此外论文并未提供工程标准格式。

## 重要的相关工作

### 奠基或前身工作

- [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)

### 同类型或同家族工作

- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)
- [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Hybrid Automata -> Hybrid Systems with Rectangular Differential Inclusions` 的早期可判定子枝。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Hybrid Automata with Rectangular Differential Inclusions`
- 论文角色：模型提出
- 核心功能：用矩形微分包含和初始化关系定义一类可判定的混成自动机。
- 关键特性：`$\dot x_i \in [L_i,U_i]$`、initialization relation、regular language、verification decidability。
- 构造方式：`H=(L,\Sigma,D,Z,r)` + enabling conditions + initialization relations。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：bounded drift、矩形速度区间和可判定混成建模。
- 需求前提：连续流必须能矩形化，切换时更新能写成区间初始化。
- 状态：🟢
