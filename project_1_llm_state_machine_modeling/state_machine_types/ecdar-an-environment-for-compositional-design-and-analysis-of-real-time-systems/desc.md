# ECDAR：实时系统组合式设计与分析环境 / ECDAR: An Environment for Compositional Design and Analysis of Real Time Systems

## 基本信息

- 标题：ECDAR: An Environment for Compositional Design and Analysis of Real Time Systems
- 中文标题：ECDAR：实时系统组合式设计与分析环境
- 作者：Alexandre David，Kim G. Larsen，Axel Legay，Ulrik Nyman，Andrzej Wasowski
- 发表：*Automated Technology for Verification and Analysis*，pp. 365-370，2010
- DOI：`10.1007/978-3-642-15643-4_29`
- 链接：https://homes.cs.aau.dk/~adavid/publications/45-atva10.pdf
- 形式主义：`Timed I/O Automata / ECDAR`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：timed interface theory environment / compositional verifier
- 工具/实现获取方式：原文明确给出 `ecdar.cs.aau.dk` 作为工具入口，并说明实现复用了 `Uppaal-tiga` 的游戏求解核心。
- 标准/格式获取方式：承载方式是带输入/输出动作划分的 `Timed I/O Automata` 图形模板与 ECDAR query language；原文未给独立于工具的中立交换标准。

## 简报

这篇论文的意义，在于把 dense-time 接口理论第一次做成比较完整的工程环境。`ECDAR` 不只是一个 timed automata 编辑器，它把 `composition`、`conjunction`、`quotient`、`consistency`、`refinement` 和 `TCTL` 检查放进同一个游戏语义框架里，并且给出可交互的策略和错误解释。对 `state_machine_types` 文库来说，它补上了 `Timed I/O` / timed interface tooling 这一条长期缺口。

- 形式主义定位：面向 `Timed I/O Automata` 与 timed interface theory 的组合式分析环境，而不是新的状态机家族。
- 构造方式简述：用带输入/输出动作的 timed automata 模板描述组件接口，再通过 query interface 做 refinement、consistency、composition、conjunction 和 quotient。
- 基础设施与场景简述：依托图形化模板、查询面板、自研 engine 与 `Uppaal-tiga` game solver 复用链路，服务实时组件接口设计、组合验证和分步抽象证明。

```text
timed interface requirement -> TIOA templates -> composition / conjunction / quotient / refinement -> strategy-guided compositional proof
```

## 形式主义定义与核心对象

### 定义对象

论文把 `ECDAR` 的建模对象固定为带时间语义的接口自动机：

1. locations 与初始位置。
2. clocks。
3. input actions 与 output actions。
4. invariants、guards 与 resets。
5. timed game semantics 下的 consistency / refinement / quotient 等操作。

### 核心抽象

结合论文对 `Timed I/O Automata` 的使用方式，可保守整理为：

$$
I = (L, l_0, C, \Sigma_I, \Sigma_O, E, Inv)
$$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `l_0` 是初始 location。
3. `C` 是 clocks 集合。
4. `\Sigma_I` 是输入动作集合。
5. `\Sigma_O` 是输出动作集合。
6. `E` 是带 guards、actions 与 resets 的边集合。
7. `Inv` 为各 location 指派时钟不变式。

论文强调语义核心不是普通 LTS，而是 timed game。可保守压成：

$$
G_I = \langle S, S_{in}, S_{out}, \rightarrow \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是接口状态集合。
2. `S_{in}` 对应 environment / input player 的决策状态。
3. `S_{out}` 对应 component / output player 的决策状态。
4. `\rightarrow` 是时间推进与离散动作联合诱导的游戏边。

在 `ECDAR` 的 query language 中，最核心的关系之一是 refinement：

$$
\texttt{refinement: } A \le B
$$

其含义是：

1. `A` 的实现行为不比 `B` 更激进。
2. `A` 至少接受 `B` 所要求的环境行为。
3. `A` 的输出承诺与时间约束不比 `B` 更松。

### 一个最小例子与通俗解释

论文用改写后的 Milner scheduler 做演示：

1. 每个节点 `M_i` 接收 `rec[i]?` 后开始工作 `w[i]!`。
2. 它必须在 `[d,D]` 时间窗口内把 token 通过 `rec[i+1]!` 传给下一个节点。
3. 系统总规格 `S_0` 约束某些 `w[0]!` 事件最晚必须多久出现一次。
4. 证明时既可以 monolithic 地验证整个环，也可以用 `SS_i` 这类子规格逐步证明。

通俗地说，`ECDAR` 像“给实时接口做积木式证明的工作台”。你不用每次都把整套系统摊平去验，而是可以先为部分子系统写一个抽象接口，再一步一步把组合证明拼起来。

### 运行 / 接受 / 转移语义

论文最直观的 query 写法是：

$$
\texttt{refinement: } (M_0 \parallel M_1 \parallel \cdots \parallel M_4) \le S_0
$$

上式中的符号逐项解释如下：

1. `M_i` 是若干组件接口。
2. `\parallel` 表示接口组合。
3. `S_0` 是整体需求规格。
4. 查询要求组合后的系统满足总体规格。

对子规格递增验证，论文给出：

$$
M_1 \le SS_1,\quad (SS_1 \parallel M_2) \le SS_2,\ \ldots,\ (SS_4 \parallel M_0) \le S_0
$$

上式中的符号逐项解释如下：

1. `SS_i` 是对部分子系统的抽象子规格。
2. 每一步都在 refinement checker 中求解一个 timed game。
3. 这就是 compositional verification 在工具中的直接落地方式。

一致性检查则可保守写成：

$$
\mathrm{Cons}(I) \iff \exists \sigma_{out}\ \text{avoiding bad states}
$$

上式中的符号逐项解释如下：

1. `\sigma_{out}` 是 output player 的策略。
2. “bad states” 对应违反 independent progress 等条件的不可实现状态。
3. 若存在赢策略，则接口是可实现的。

### 语义边界

这篇论文的边界同样很清楚：

1. 主体是 dense-time timed interface theory，不是一般混成系统。
2. 组件交互通过输入/输出动作建模，不允许共享全局变量。
3. 工具聚焦 compositional reasoning，不是大而全的执行平台。
4. 其核心优势依赖 timed game semantics；若系统不适合游戏式接口解释，这条路线的收益会下降。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TIOA` 骨架 | `$I = (L, l_0, C, \Sigma_I, \Sigma_O, E, Inv)$` | 固定 timed interface 的基本对象。 |
| timed game semantics | `$G_I = \langle S, S_{in}, S_{out}, \rightarrow \rangle$` | 把接口分析转成输入/输出双方博弈。 |
| refinement query | `$\texttt{refinement: } A \le B$` | 检查一个实现/规格是否细化另一个规格。 |
| consistency | `$\mathrm{Cons}(I) \iff \exists \sigma_{out}\ \text{avoiding bad states}$` | 检查接口是否存在可实现策略。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 以 timed automata locations 为骨架。 |
| 事件 / 触发 | 很强 | 输入/输出动作是接口主语义。 |
| 守卫 / 数据 | 中等支持 | guards、invariants、resets 很强，但共享数据弱。 |
| 层次 | 不支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 很强 | composition、conjunction、quotient 是主线。 |
| 时间约束 | 很强 | dense-time communication constraints 是核心。 |
| 连续动态 / 随机性 | 不支持 | 纯 timed interface，不含连续流。 |
| 可执行 / 可验证性 | 很强 | refinement、consistency、策略裁剪与 `TCTL` 检查都已落地。 |

### 形式化问题与性质

1. `ECDAR` 的关键工程价值，是把 timed interface theory 的整套操作做成了统一前端。
2. 它特别适合把大系统证明拆成多个 refinement 小步，而不是一次性 monolithic 展开。
3. 在当前文库里，它补的是 `Tempo` 和 `MIO Workbench` 之间那条 dense-time compositional interface tooling 缺口。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 在 specification interface 中画 timed I/O automata 模板。
2. 指定输入/输出动作、guards、invariants 与 resets。
3. 在 query interface 中写 refinement / consistency / composition 查询。
4. 需要时用 pruning 和策略查看器收缩状态空间。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `ECDAR` 图形模板。
2. `Uppaal-tiga` 风格的 timed automata 输入语言。
3. 查询语句如 `refinement:`。
4. 工具内部的游戏求解状态空间与策略对象。

### 交换与互操作

这篇论文的互操作重点在工具链内部而非中立标准：

1. 输入语言与 `Uppaal-tiga` 近亲，便于复用现有求解核心。
2. 自研 engine 复用了 `Uppaal-tiga` 的游戏部件。
3. `quotient`、`conjunction`、`refinement` 和 `TCTL` 检查消费的是同一接口模型表示。

## 配套基础设施

- 建模/编辑工具：图形化 specification interface。
- 解析/交换/元模型支持：`Uppaal-tiga` 风格模型语言与 `ECDAR` 自身模板；无中立交换标准。
- 仿真/执行支持：主体是策略与验证环境，而不是运行时执行器。
- 验证/分析支持：refinement、consistency、composition、conjunction、quotient、`TCTL` constraints、pruning facility。
- 代码生成/转换支持：原文未强调代码生成；重点是 interface reasoning。
- 标准化或社区生态：`ECDAR` 站点、图形 UI 与 `Uppaal-tiga` 生态复用构成主要工程载体。

## 适用场景与需求前提

### 适用场景

适合实时组件接口设计、分布式通信协议、组合式验证，以及需要把总体规格拆成多个子接口逐步证明的场景。

### 需求前提

1. 系统能够抽成输入/输出动作驱动的 timed interfaces。
2. 时间约束主要体现在 guards、invariants 和 communication deadlines。
3. 设计者关心的是 compositional reasoning，而不是单纯仿真。
4. 能接受不使用共享全局变量的接口建模风格。

### 不适用或高成本场景

若系统高度依赖共享数据状态、连续动力学或复杂数值更新，`ECDAR` 这种 timed interface tooling 就不是最自然的入口。

## 与相邻形式主义的关系

相对 [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)，本文讲的是工程环境而不是 timed I/O automata 理论本体；相对 [tempo-a-toolkit-for-the-timed-input-output-automata-formalism/desc.md](../tempo-a-toolkit-for-the-timed-input-output-automata-formalism/desc.md)，`Tempo` 更像语言加 simulator/translator，而 `ECDAR` 更强在 game-based compositional reasoning；相对 [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)，它把 modal/interface tooling 推进到了 dense-time setting。

## 与本研究的关系

### 对 Project 1 的价值

它证明如果后续 `project_1` 需要把某类需求映射到“接口化的实时状态机”，那么不止能建模，还能直接得到组合式 refinement / quotient 工具链。

### 作为目标形式主义还是中间表示

更适合作为面向实时交互系统的目标形式主义或高质量中间表示，而不是纯需求描述层的临时草模。

### 对需求到模型生成的启发

1. 生成阶段要显式区分 input/output actions，而不是只给一张没有责任边界的状态图。
2. 若希望后续做 quotient 或 compositional verification，就必须在建模时保留接口化结构。
3. 对复杂系统，可优先生成子规格 `SS_i` 一类中间接口，再逐步组合证明。

### 现实限制

它主要服务 timed interface reasoning，不直接处理连续控制对象，也不替代通用 hybrid verification 工具。

## 重要的相关工作

- [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)：`Timed I/O Automata` 的理论母线。
- [tempo-a-toolkit-for-the-timed-input-output-automata-formalism/desc.md](../tempo-a-toolkit-for-the-timed-input-output-automata-formalism/desc.md)：偏语言与 toolkit 的 `TIOA` 工程载体。
- [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)：untimed modal interface theory 的工作台。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
