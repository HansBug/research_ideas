# 重新审视定时自动机网络的局部时间语义 / Revisiting Local Time Semantics for Networks of Timed Automata

## 基本信息

- 标题：Revisiting Local Time Semantics for Networks of Timed Automata
- 中文标题：重新审视定时自动机网络的局部时间语义
- 作者：R. Govind，Frédéric Herbreteau，B. Srivathsan，Igor Walukiewicz
- 发表：*CONCUR 2019 / LIPIcs 140*，Article 16，2019
- DOI：`10.4230/LIPIcs.CONCUR.2019.16`
- 链接：https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CONCUR.2019.16
- 形式主义：`Timed Automata Networks / local-time semantics / local-zone graph`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：local-zone reachability / local-sync graph / timed-automata verification route
- 工具/实现获取方式：论文说明作者实现了 prototype，并与 `TChecker` 上的标准 global-zone 方法比较；未给出长期维护的独立产品页。
- 标准/格式获取方式：对象是标准 networked timed automata，本论文新增的是 local-time semantics、local zones 和 local sync graph 算法，而不是新的交换格式。

## 简报

这篇论文做的不是重新定义 `Timed Automata`，而是针对“网络化 timed automata 的 zone graph 在并发交错下容易爆炸”这个老问题，重新启用并修正了 local-time semantics 这条线。它的关键贡献是说明：只要改成每个进程独立推进局部时间，再在同步动作时对齐参考时钟，就能把许多仅因交错顺序不同而重复出现的 global zones 聚合掉；同时作者又指出旧的 local-zone finiteness 办法有 flaw，并给出基于 synchronized zones 的新 subsumption。

- 形式主义定位：面向 networked timed automata reachability 的 local-time / local-zone 算法路线。
- 构造方式简述：先把 global time `t` 换成每进程局部参考时钟 `t_p`，再定义 local valuation、local zones、local zone graph，最后用 synchronized valuations 做 subsumption 构造 finite local sync graph。
- 基础设施与场景简述：依托标准 timed automata 网络、zone abstraction 和 `TChecker` 原型实现，适合多进程并发交错导致 zone 爆炸的实时系统。

```text
networked timed automata -> local-time semantics -> local zone graph -> synchronized-zone subsumption -> finite local sync graph -> reachability result
```

## 形式主义定义与核心对象

### 定义对象

论文直接从 networked timed automata 出发，并额外引入：

1. global valuation 与 local valuation 两种时钟解释。
2. global zone graph 与 local zone graph。
3. synchronized local valuations。
4. local sync graph。

### 核心抽象

论文对网络化 timed automata 给出正式定义：

$$
\mathcal{N} = (A_1,\ldots,A_k)
$$

其中每个进程自动机满足：

$$
A_p = \langle Q_p, \Sigma_p, X_p, q^{init}_p, T_p \rangle
$$

上式中的符号逐项解释如下：

1. `Q_p` 是进程 `p` 的离散状态集合。
2. `\Sigma_p` 是动作字母表。
3. `X_p` 是 clocks 集合。
4. `q^{init}_p` 是初始状态。
5. `T_p \subseteq \Sigma_p \times Q_p \times \varphi(X_p) \times 2^{X_p} \times Q_p` 是迁移集合。

论文先用 offset 变量重写 standard global-time semantics。全局 valuation 写成：

$$
v : \widetilde{X} \cup \{t\} \to \mathbb{R}_{\ge 0}
$$

上式中的符号逐项解释如下：

1. `t` 是全局参考时间。
2. `\widetilde{x}` 是时钟 `x` 的 offset 变量，记录上次 reset 时间。
3. `\widetilde{X}` 是所有 offset 变量集合。
4. 时钟值通过 `v(t)-v(\widetilde{x})` 读取。

local-time semantics 的核心，则是把单一 `t` 换成每个进程自己的 `t_p`。local valuation 写成：

$$
\mathbf{v} : \widetilde{X}' \to \mathbb{R}_{\ge 0}
$$

上式中的符号逐项解释如下：

1. `\widetilde{X}' = \bigcup_p (\widetilde{X}_p \cup \{t_p\})`。
2. `t_p` 是进程 `p` 的局部参考时钟。
3. 对于 `x \in X_p`，时钟值由 `\mathbf{v}(t_p)-\mathbf{v}(\widetilde{x})` 给出。

local action step 则要求参与同步的进程局部时间对齐。对动作 `b`，论文要求：

$$
\mathbf{v}(t_{p_1}) = \mathbf{v}(t_{p_2}) \qquad \forall p_1,p_2 \in \mathrm{dom}(b)
$$

上式中的符号逐项解释如下：

1. `\mathrm{dom}(b)` 是必须在动作 `b` 上同步的进程集合。
2. 只有当这些进程当前局部时间一致时，动作 `b` 才可共同发生。

### 一个最小例子与通俗解释

论文第一页的双进程例子最适合说明它的意义：

1. 进程 `A_1` 做本地动作 `a`，重置时钟 `x`。
2. 进程 `A_2` 做本地动作 `b`，重置时钟 `y`。
3. 在传统 global-zone graph 里，序列 `ab` 和 `ba` 会落到不同 zone，因为全局时间会记住先后顺序。
4. 在 local-time semantics 下，两个进程可以各自推进局部时间，于是 `ab` 和 `ba` 落到同一个 local zone。

通俗地说，这篇论文相当于把“每个并发进程都带自己的表”，只有在真正需要同步时才对表。这样，那些只因为 interleaving 不同而产生的重复 zone 就被合并掉了。

### 运行 / 接受 / 转移语义

论文先定义 global-time reachability。对全局配置 `(q,v)`，动作序列 `u` 的可达性写为：

$$
(q_0,v_0)\xRightarrow{u}(q_n,v'_n)
$$

接着改写为 local semantics：

$$
(q_0,\mathbf{v}_0)\xrightarrow{u}(q_n,\mathbf{v}'_n)
$$

二者最重要的联系由论文的 Lemma 10 给出：若 local run 的起终 valuation 都 synchronized，则存在某个等价交错 `w \sim u`，使它对应一条 global run。

论文在 zone 层面给出 local step：

$$
(q,Z)\xrightarrow{b}(q',Z')
$$

其中

$$
Z'=\mathrm{local\mbox{-}elapse}([R](Z \cap Z_g \cap Z_{sync}))
$$

上式中的符号逐项解释如下：

1. `Z` 是当前 local zone。
2. `Z_g` 是 guard 约束对应的 zone。
3. `Z_{sync}` 表示参与动作 `b` 的进程在当前步前需要局部时间对齐。
4. `[R]` 是 reset 操作。
5. `\mathrm{local\mbox{-}elapse}` 允许各进程分别推进局部时间。

论文最关键的聚合结果是：

$$
MZ(q,Z,u) = \mathrm{global}(\mathrm{sync}(Z'))
$$

上式中的符号逐项解释如下：

1. `MZ(q,Z,u)` 是 standard zone graph 中，动作序列 `u` 的所有等价交错所能到达 zone 的并。
2. `Z'` 是 local zone graph 中执行 `u` 后得到的 local zone。
3. `\mathrm{sync}(Z')` 取其中 synchronized valuations。
4. `\mathrm{global}` 再把它们投回 global valuations。
5. 这就是 Theorem 18 的核心含义。

### 语义边界

1. 论文关注的是 reachability 和 zone-based verification，不是全面的 timed synthesis 或 testing。
2. 它处理的是 networks of timed automata，而不是 pushdown timed、probabilistic timed 或 hybrid timed family。
3. local-zone graph 本身可能无限，因此必须再加 synchronized-zone subsumption。
4. 作者明确指出 Minea 的 maximized-local-zone 方案不 sound，这也是本文修正的边界点。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 网络骨架 | `$\mathcal{N}=(A_1,\ldots,A_k),\ A_p=\langle Q_p,\Sigma_p,X_p,q^{init}_p,T_p\rangle$` | 标准 timed automata 网络输入对象。 |
| global valuation | `$v:\widetilde{X}\cup\{t\}\to\mathbb{R}_{\ge0}$` | 用 offset 变量重写全局时钟语义。 |
| local valuation | `$\mathbf{v}:\widetilde{X}'\to\mathbb{R}_{\ge0}$` | 每个进程有自己的参考时钟 `t_p`。 |
| 同步条件 | `$\mathbf{v}(t_{p_1})=\mathbf{v}(t_{p_2})$` | 同步动作前相关进程局部时间必须一致。 |
| local zone successor | `$Z'=\mathrm{local\mbox{-}elapse}([R](Z\cap Z_g\cap Z_{sync}))$` | 定义 local zone graph 的转移。 |
| 聚合定理 | `$MZ(q,Z,u)=\mathrm{global}(\mathrm{sync}(Z'))$` | local zone 直接给出所有等价交错聚合后的 global zone。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 基础对象仍是标准 networked timed automata。 |
| 事件 / 触发 | 很强 | 通过动作字母和同步域 `dom(b)` 驱动。 |
| 守卫 / 数据 | 中等支持 | 重点在时钟 guards，不强调复杂数据变量。 |
| 层次 | 不适用 | 不是层次状态机。 |
| 并发 / 同步 | 很强 | 论文核心就是并发交错与同步局部时间。 |
| 时间约束 | 很强 | 全部贡献都围绕时钟与 zone abstraction。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 直接落成 local zone graph 和 prototype implementation。 |

### 形式化问题与性质

1. local-time semantics 的主要收益是让独立动作的交换真正变成 zone 级可合并。
2. Theorem 18 说明 aggregated zones 可以直接从 local zone 计算出来。
3. Theorem 20 进一步给出 local sync graph 的 soundness / completeness，补上了可终止算法一环。

## 构造方式与承载格式

### 建模入口

建模入口并没有脱离普通 timed automata：

1. 先给出标准 network of timed automata。
2. 再在算法层选择 global-time 还是 local-time semantics。
3. 最后构造 local zone graph 和 local sync graph。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed automata 网络。
2. global / local valuations。
3. global zones / local zones。
4. synchronized local valuations。
5. local sync graph。

### 交换与互操作

1. 论文不是新格式工作，而是 timed-automata backend algorithm 工作。
2. 与现有工具的接口体现为 prototype 和 `TChecker` 比较。
3. 它对 timed-automata 工具链的贡献主要是“算法后端升级”，不是前端语言替换。

## 配套基础设施

- 建模/编辑工具：沿用标准 timed automata 网络建模入口。
- 解析/交换/元模型支持：核心是 zone、offset valuation 和 synchronization-aware abstraction，而非新文件格式。
- 仿真/执行支持：原文没有强调仿真，重点是 reachability computation。
- 验证/分析支持：local zone graph、aggregated zone computation、subsumption-based finite local sync graph。
- 代码生成/转换支持：不涉及代码生成。
- 标准化或社区生态：论文给出 prototype implementation，并与 `TChecker` 的标准方法做实验比较。

## 适用场景与需求前提

### 适用场景

适合多进程并发、局部动作很多、global-zone interleavings 容易爆炸的实时系统验证，尤其是 timed automata 网络 reachability。

### 需求前提

1. 系统已能建成 standard timed automata network。
2. 复杂度主要来自并发交错，而不是复杂数据或连续动力学。
3. 核心问题是 reachability / zone exploration，而不是 controller synthesis。

### 不适用或高成本场景

1. 若系统根本没有并发交错爆炸，local-time 路线收益会有限。
2. 若模型已经超出 timed automata 网络家族，如 hybrid / pushdown timed，则这篇不够。
3. 若团队更关心工具生态而非后端算法，这篇需要与 `TChecker/UPPAAL` 等工具条目结合看。

## 与相邻形式主义的关系

1. 相比 standard global-time zone graph，它的差异不在模型本体，而在语义与抽象后端。
2. 相比 `UPPAAL` 风格经典 zone route，它更强调并发独立动作的 commutativity。
3. 相比 `pushdown timed automata` 那条线，它没有显式栈，仅处理并发 timed automata 网络。
4. 与 `TChecker` 的关系最紧，因为它可以被视为 timed-automata backend algorithm 的一条增强路线。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的意义是：当目标模型落成 timed automata 网络后，验证后端不必只依赖 standard zone graph。对于由 LLM 生成、天然存在大量并发交错的模型，这条 local-zone route 能显著影响可验证性。

### 作为目标形式主义还是中间表示

它不是新的最终输出形式主义，而是 timed automata 网络的验证方法路线。

### 对需求到模型生成的启发

1. 若未来要让 LLM 生成 timed automata，最好保留各动作涉及的进程域 `dom(b)`。
2. 模型中局部动作与同步动作的区分会直接影响后端是否能用这条 local-time 优化路线。
3. 生成模型时最好少引入不必要的跨进程同步，否则会削弱 local-time 语义优势。

### 现实限制

1. 贡献主要在 reachability 后端，前端建模收益间接。
2. 论文原型和工具生态成熟度不如主流完整平台条目。
3. 更适合拿来补 timed backend 视角，而不是单篇承担 timed automata 全貌。

## 重要的相关工作

### 奠基或前身工作

1. Bengtsson 等人的 local-time semantics / local zones 是直接前身。
2. Salah 等人的 aggregated-zone 观察是本文的重要起点。

### 同类型或同家族工作

1. standard zone graph / abstraction 方法是直接对照组。
2. Minea 的 maximized-local-zone 方法是本文明确指出 flaw 的近邻工作。

### 标准 / 格式 / 工具链工作

1. `TChecker` 是本文实验对照里最直接的工具锚点。
2. timed automata 标准建模本体仍沿用既有家族，不另起语言。

### 与本研究关系最紧的工作

1. 文库里所有 timed backend 条目都与它有关，尤其 `UPPAAL in a Nutshell`、`Verified Model Checking of Timed Automata`、`Fast zone-based algorithms for reachability in pushdown timed automata`。
2. 它是 “global zone -> local zone -> synchronized-zone subsumption” 这条 timed verification 方法线的重要锚点。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata Networks / local-time semantics / local-zone graph`
- 论文角色：local-zone reachability / local-sync graph / timed-automata verification route
- 核心功能：通过 local-time semantics 和 synchronized-zone subsumption 缓解 networked timed automata 的 zone 爆炸。
- 关键特性：offset valuation、per-process reference clocks、local zones、aggregated zones、finite local sync graph。
- 构造方式：standard timed automata network -> local valuation / local zone -> subsumption-based local sync graph。
- 基础设施：prototype implementation、zone abstraction、与 `TChecker` 标准方法的比较基线。
- 适用场景：多进程并发实时系统 reachability，尤其是独立动作交错很多的 timed automata 网络。
- 需求前提：系统已能建成 timed automata 网络，且复杂度主要来自并发交错。
- 状态：🟢 直接可用
