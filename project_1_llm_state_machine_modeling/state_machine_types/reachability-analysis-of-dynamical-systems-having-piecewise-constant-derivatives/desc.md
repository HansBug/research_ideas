# 具有分段常值导数的动力系统的可达性分析 / Reachability Analysis of Dynamical Systems having Piecewise-Constant Derivatives

## 基本信息

- 标题：Reachability Analysis of Dynamical Systems having Piecewise-Constant Derivatives
- 中文标题：具有分段常值导数的动力系统的可达性分析
- 作者：Eugene Asarin, Oded Maler, Amir Pnueli
- 发表：*Theoretical Computer Science*, 138(1):35-65, 1995
- DOI：`10.1016/0304-3975(94)00228-B`
- 链接：https://doi.org/10.1016/0304-3975(94)00228-B
- 形式主义：`Hybrid Systems with Piecewise-Constant Derivatives (PCD)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具；机器可处理入口是 `$H=(X,f)$`、polyhedral partition、slope vectors 和 `Reach(H,P,P')`。
- 标准/格式获取方式：原文没有 DSL / 交换标准，核心承载方式是“区域列表 + 斜率向量”的几何定义。

## 简报

这篇论文把一类非常有辨识度的混成模型固定成单独分支：`PCD systems`。它不再显式保留离散 location 和 reset，而是把连续状态空间切成有限个 polyhedral regions，每个 region 都绑定一个常值向量场；系统轨迹因此变成折线，离散“切换”只在跨 region 边界时隐式发生。其价值不只是模型定义，还在于给出了极清晰的判定边界：二维 deterministic `PCD` 的 reachability 可判定，而三维及以上已经可以模拟足够强的自动机，导致不可判定。对演化树来说，这正好补出 `Hybrid Automata` 主干上一条非常经典的连续/几何支线。

- 形式主义定位：`Hybrid Automata` 主干上的连续几何型子类，不以 reset 为核心，而以 region partition + constant vector field 为核心。
- 构造方式简述：把状态空间按 polyhedra 分区，每个区域配一个常斜率向量，轨迹跨边界时自动切换斜率。
- 基础设施与场景简述：核心基础设施不是 model checker，而是 polyhedral partition、successor-chain、几何拓扑分析和 reachability decision procedure。

```text
continuous state space -> polyhedral partition -> constant slope per region -> broken-line trajectory -> planar decidability / 3D undecidability
```

## 形式主义定义与核心对象

### 定义对象

论文研究的是一种没有显式 reset、没有独立离散赋值、但仍然具备混成系统 flavor 的动力系统。离散成分被“编码”进空间分区本身。

### 核心抽象

论文给出的定义是：

$$
H = (X,f)
$$

上式中的符号逐项解释如下：

1. `X` 是连续状态空间，通常取 `\mathbb{R}^d`。
2. `f:X\to X` 是一个可能部分定义的函数。
3. `f` 的值域是有限个向量组成的集合 `C \subseteq X`。
4. 对每个 `c\in C`，逆像 `f^{-1}(c)` 必须是有限个 convex polyhedral sets 的并。

换句话说，`X` 被切成有限个 polyhedral regions；在每个 region 内，系统都按一个固定斜率向量 `c` 演化。

### 一个最小例子与通俗解释

论文引言里用 `Pacman` 和 ghost 的追逐问题举了一个很好的二维例子。把两者的位置记作 `(x,y)`，则整个系统状态就是平面上的一个点；依据两者相对位置不同，系统落入不同 region，每个 region 都有自己的速度向量 `(v_x,v_y)`。于是：

1. 在同一个 region 内，点沿直线运动。
2. 一旦跨到边界另一侧，斜率向量切换，运动方向随之改变。

通俗地说，`PCD` 像“在地图不同区域上装了不同方向的传送风”。物体一进入某个区域，就会沿该区域规定的方向匀速漂移；漂到边界时，再按新区域的风向继续漂。

### 运行 / 接受 / 转移语义

连续轨迹 `\gamma` 的定义仍然是经典微分语义：

$$
\dot{\gamma}(t) = f(\gamma(t))
$$

只是这里的 `f` 在每个 region 内都恒定，所以 `\gamma` 是 broken-line trajectory。论文关心的核心判定问题是：

$$
\mathrm{Reach}(H,x,x')
$$

即给定 `x,x' \in X`，是否存在某条轨迹从 `x` 出发在某个时刻到达 `x'`。更一般的区域版问题是：

$$
\mathrm{R\text{-}Reach}(H,P,P')
$$

这里 `P,P'` 是 polyhedral subsets，问题变成“是否存在 `x\in P` 与 `x'\in P'` 使得点到点 reachability 成立”。

### 语义边界

它比 timed automata 更宽，因为不同变量可在不同区域里以不同斜率变化，且 guards 可是一般线性不等式组合；但它又比一般 hybrid automata 更窄，因为没有 discrete reset，也没有任意 jump assignment。

### 关键性质与判定边界

这篇论文最关键的就是二维与三维的 sharp split。正结果可以概括为：

$$
\text{For deterministic planar PCD systems, }\mathrm{Reach}(H,x,x')\text{ is decidable}
$$

并进一步推广到 region-to-region：

$$
\text{For deterministic planar PCD systems, }\mathrm{R\text{-}Reach}(H,P,P')\text{ is decidable}
$$

而负结果则是：

$$
\text{Reachability for 3-dimensional PCD systems is undecidable}
$$

论文通过模拟 PDA / 2PDA 建立了这一不可判定边界，因此 `PCD` 不是“玩具模型”，而是一条真正有表达力和边界结果的经典分支。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 以几何分区隐式支持 | 没有显式 location，mode 被编码成 regions。 |
| 事件 / 触发 | 边界触发 | 轨迹跨越 region 边界时发生“离散切换”。 |
| 守卫 / 数据 | 强支持几何 guard | polyhedral inequalities 决定 region 和边界。 |
| 层次 | 不支持 | 核心模型不是层次自动机。 |
| 并发 / 同步 | 不支持 | 论文关注单体动力系统的 reachability。 |
| 时间约束 | 强支持 | 时间完全体现在连续轨迹长度上。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每个 region 里是 constant vector field。 |
| 可执行 / 可验证性 | 强理论支持 | planar decidability 与 3D undecidability 都很清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$H=(X,f)$` | `PCD` 的最简几何定义。 |
| 连续语义 | `$\dot{\gamma}(t)=f(\gamma(t))$` | 轨迹在各 region 内沿常向量场演化。 |
| 点到点可达 | `$\mathrm{Reach}(H,x,x')$` | 判断两点之间是否存在轨迹。 |
| 区域可达 | `$\mathrm{R\text{-}Reach}(H,P,P')$` | 判断两块 polyhedral 区域间的可达性。 |
| 判定边界 | `$\mathrm{Reach}_{2D}$ decidable, `$\mathrm{Reach}_{3D}$` undecidable | 二维与三维的 sharp split。 |

## 构造方式与承载格式

### 建模入口

1. 先给定连续状态空间 `X`。
2. 用有限个 polyhedral regions 切分 `X`。
3. 为每个 region 绑定一个 constant slope vector。
4. 把要验证的问题写成点到点或区域到区域的 reachability。

### 机器可处理承载方式

机器可处理承载方式就是“区域列表 + 斜率向量 + reachability 查询”，而不是独立的图形或文本 DSL。

### 交换与互操作

它和 [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md) 的 `Phase Transition Systems` 线相容，也和 [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md) 的 `Linear Hybrid Systems`、[decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md) 的矩形分支共同构成 `Hybrid Automata` 附近的可判定边界族谱。

## 配套基础设施

- 建模/编辑工具：原文未提供独立工具。
- 解析/交换/元模型支持：核心是 polyhedral partition 和 slope-vector description。
- 仿真/执行支持：根据 region 与当前点可直接计算短时 successor。
- 验证/分析支持：point-to-point / region-to-region reachability、successor-chain 分析、PDA simulation。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 `PCD` 这条混成几何支线的经典命名文献。

## 适用场景与需求前提

### 适用场景

适合那些连续状态在不同区域中按不同固定速度漂移、但不发生显式重置的系统，也适合用来研究混成可达性的几何边界。

### 需求前提

1. 状态空间必须能切成有限个 polyhedral regions。
2. 每个 region 内的连续动态应能近似成 constant vector field。
3. 若要享受论文正结果，最好落在 deterministic planar 情形。

### 不适用或高成本场景

如果系统高度依赖 reset、离散赋值或强耦合非线性动力学，`PCD` 会过于受限。

## 与相邻形式主义的关系

相对 [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md)，它更几何、更连续，也更少显式 discrete bookkeeping；相对 [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md)，它不要求矩形导数区间，而是直接按区域给定常向量场；相对 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，它是另一条经典 decidable / undecidable boundary 路线。

## 与本研究的关系

### 对 Project 1 的价值

它能把演化树里的混成主干从“phase/linear/rectangular”之外，再补出一条 `PCD` 几何子线。

### 作为目标形式主义还是中间表示

更适合作为中间语义层、理论分析对象，或一般混成模型的保守连续近似。

### 对需求到模型生成的启发

当自然语言需求强调“系统在不同区域内按不同固定速度漂移”，而不是强调事件重置时，LLM 很适合优先抽成 `PCD`。

### 现实限制

它对离散控制和赋值的表达不如一般 `Hybrid Automata` 灵活；高维以后判定性也迅速崩塌。

## 重要的相关工作

### 奠基或前身工作

- [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md)

### 同类型或同家族工作

- [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md)
- [decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md](../decidability-of-hybrid-systems-with-rectangular-differential-inclusions/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准；其关键基础设施是 polyhedral geometry 与 reachability procedure。

### 与本研究关系最紧的工作

- 它最适合挂成 `Hybrid Automata -> Hybrid Systems with Piecewise-Constant Derivatives` 的经典子节点。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Hybrid Systems with Piecewise-Constant Derivatives (PCD)`
- 论文角色：模型提出
- 核心功能：把 polyhedral partition + constant vector field 固定成 `PCD` 家族，并给出二维/三维 reachability 边界。
- 关键特性：piecewise-constant derivatives、polyhedral regions、broken-line trajectories、planar decidability、3D undecidability。
- 构造方式：`H=(X,f)` + region list + slope vectors + reachability queries。
- 基础设施：纯理论几何框架，无工程标准/工具。
- 适用场景：区域切换型连续控制对象、混成可达性边界分析、保守连续近似。
- 需求前提：状态空间需可 polyhedral partition，且每块区域内可近似为常斜率演化。
- 状态：🟢
