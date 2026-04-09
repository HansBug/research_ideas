# 可见下推模块博弈 / Visibly Pushdown Modular Games

## 基本信息

- 标题：Visibly Pushdown Modular Games
- 中文标题：可见下推模块博弈
- 作者：Ilaria De Crescenzo、Salvatore La Torre、Yaron Velner
- 发表：*Proceedings of the Fifth International Symposium on Games, Automata, Logics and Formal Verification (GandALF 2014)*, EPTCS 161, pp. 260-274, 2014
- DOI：`10.4204/EPTCS.161.22`
- 链接：https://arxiv.org/pdf/1408.5969.pdf
- 形式主义：`Visibly Pushdown Modular Games (VPMG / MVPG)`，即带 visibly pushdown automaton 规格的 `RGG`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`RGG` 规格自动机扩展 / visibly-pushdown winning-condition branch
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RGG` tuple、modular strategy、`VPA` tuple 与 `MVPG` reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 `RGG` + visibly pushdown automaton specification + modular strategy。

## 简报

这篇论文把 `RGG` 的 winning-condition family 从 ordinary `\omega`-regular 规格继续推进到了 visibly pushdown automata。与 `CaRet` modular games 相比，它不是改用更强的逻辑，而是直接用一类 stack-sensitive automaton 作为胜利条件，从而把 `RGG` 和 visibly pushdown language family 明确连到一起。

- 形式主义定位：`RGG` 的 visibly-pushdown specification branch。
- 构造方式简述：底层仍是 recursive game graph 与 modular strategy；新增的是胜利条件由 `VPA` 而非普通 finite automaton 给出。
- 基础设施与场景简述：论文没有工程工具，但它把 `RGG`、modular strategy、`VPA` 与 temporal-logics-over-pushdown-specs 的复杂度边界一次性理顺，是 `RGG` 分支很适合挂树的一篇。

```text
RGG -> modular strategy -> visibly pushdown automaton specification -> MVPG -> recursive controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文的对象是一个 pair：

1. 底层递归博弈图 `G`；
2. 一个 visibly pushdown automaton `P`；
3. 二者组成 visibly pushdown modular game。

### 核心抽象

论文显式给出 `RGG` 的正式定义：

$$
G = (M,m_{in},\{S_m\}_{m\in M})
$$

其中每个 game module 是：

$$
S_m = (N_m,B_m,Y_m,En_m,Ex_m,d_m,h_m,P_m^0,P_m^1)
$$

上式中的符号逐项解释如下：

1. `M` 是模块名集合，`m_{in}` 是主模块。
2. `N_m` 是普通 nodes。
3. `B_m` 是 boxes，即模块调用点。
4. `Y_m : B_m \to (M \setminus \{m_{in}\})` 指定 box 调哪个模块。
5. `En_m` 与 `Ex_m` 是 entry / exit nodes。
6. `d_m` 给出模块内从 nodes / returns 到 nodes / calls 的转移。
7. `h_m` 给顶点打 atomic proposition 标签。
8. `P_m^0,P_m^1` 划分两位玩家控制的顶点。

而 winning-condition automaton `P` 的 tuple 则写成：

$$
P = (Q,Q_0,\widehat{\Sigma},\Gamma \cup \{\gamma_?\},\delta,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是 automaton 状态集合。
2. `Q_0` 是初始状态集合。
3. `\widehat{\Sigma}` 是按 `call / ret / int` 扩展后的输入字母表。
4. `\Gamma \cup \{\gamma_?\}` 是栈字母表与底符号。
5. `\delta` 由 internal / push / pop 三类转移组成。
6. `F` 是 Büchi 或 co-Büchi 接受条件。

最后，游戏对象可整理成：

$$
\mathcal G_{vp} = \langle G,P \rangle
$$

### 一个最小例子与通俗解释

论文图 1 给了一个很好的最小例子：

1. 主模块 `M_{in}` 通过 box `b` 调用模块 `M_1`。
2. 玩家 `pl_1` 在 `M_1` 里选择走向 `p_a` 还是 `p_b`。
3. 返回后玩家 `pl_0` 选择 `p_c` 或 `p_d`。
4. 规格 automaton `P` 不只是看字母序列，还能利用 call / ret / int 三类输入显式感知模块嵌套。

通俗地说，`VPMG` 就像“在递归模块博弈上，再接一台看得见调用栈形状的裁判自动机”。这比普通 finite-state winning conditions 更贴近递归程序规格，因为 automaton 自己就知道什么时候是 call、什么时候是 return。

### 运行 / 接受 / 转移语义

论文先定义 modular strategy：

$$
f = \{f_m\}_{m\in M}
$$

其中每个 `f_m` 只依赖模块 `m` 当前 activation 的 local memory。

随后，对任意 play `p=s_0s_1\cdots`，可抽取出带调用类型的词 `w_p` 送给 `VPA`。因此 winning 语义可压成：

$$
\forall p \in \mathrm{Plays}(G,f),\ w_p \in L(P)
$$

上式中的符号逐项解释如下：

1. `f` 是 protagonist 的 modular strategy。
2. `\mathrm{Plays}(G,f)` 是所有与该策略一致的 plays。
3. `w_p` 是从 play 抽出的带 `call / ret / int` 标记的词。
4. `L(P)` 是 visibly pushdown automaton `P` 接受的语言。

### 语义边界

这篇论文把 `VPMG` 的边界也说得很清楚：

1. 底层仍是 `RGG`，不是新的递归控制流语法。
2. 新增的是 stack-sensitive automaton specification，而不是 plain finite-state specification。
3. 一般 pushdown automaton 规格会导致 undecidable；切到 visibly pushdown 才重新变得可判定。
4. 策略仍必须是 modular，而不是全局历史可见策略。

### 关键性质与判定边界

论文最核心的结论可压成：

$$
\mathrm{MVPG}(G,P)\ \text{with deterministic / universal Büchi or co-Büchi VPA specs is EXPTIME-complete}
$$

以及：

$$
\mathrm{MVPG}(G,P)\ \text{with temporal-logic specs such as CARET / NWTL is } 2\mathrm{EXPTIME}\text{-complete}
$$

上式中的符号逐项解释如下：

1. `\mathrm{MVPG}` 表示 visibly pushdown modular game 判定问题。
2. `G` 是 recursive game graph。
3. `P` 是 visibly pushdown automaton specification。
4. 不同规格形态会把复杂度维持在 `EXPTIME` 或推到 `2EXPTIME`。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 底层仍是 `RGG` 的 modules / nodes / boxes。 |
| 事件 / 触发 | 强支持 | play 被编码成 `call / ret / int` 标记词。 |
| 守卫 / 数据 | 不支持 | 核心不在有限变量。 |
| 层次 | 强支持 | 递归模块层次与 visibly pushdown 栈同步出现。 |
| 并发 / 同步 | 不支持 | 目标是 sequential recursive games。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `VPA`-based winning-condition decision pipeline 完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RGG` 总体 | `$G = (M,m_{in},\{S_m\}_{m\in M})$` | 底层递归博弈图骨架。 |
| module tuple | `$S_m = (N_m,B_m,Y_m,En_m,Ex_m,d_m,h_m,P_m^0,P_m^1)$` | 单模块的 formal interface。 |
| `VPA` tuple | `$P = (Q,Q_0,\widehat{\Sigma},\Gamma\cup\{\gamma_?\},\delta,F)$` | stack-sensitive winning-condition automaton。 |
| game pair | `$\mathcal G_{vp}=\langle G,P\rangle$` | `VPMG` 的基本对象。 |
| winning condition | `$\forall p\in\mathrm{Plays}(G,f),\ w_p\in L(P)$` | modular strategy 的接受语义。 |

## 构造方式与承载格式

### 建模入口

1. 先构造 `RGG`。
2. 再给每个 play 抽取 `call / ret / int` 标记词。
3. 用 `VPA` 写 winning condition。
4. 最后求是否存在 winning modular strategy。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RGG` tuple；
2. modular strategy family；
3. `VPA` tuple；
4. `MVPG` reduction to finite-state modular games。

### 交换与互操作

它与当前文库的关系如下：

1. 向上承接 [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md) 的 `RGG`。
2. 向旁边衔接 [winning-caret-games-with-modular-strategies/desc.md](../winning-caret-games-with-modular-strategies/desc.md) 的 `CaRet`-logic sibling。
3. 向更一般的 structured-word family 可联系 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `RGG` 和 `VPA` 这两类 tuple 表达。
- 仿真/执行支持：可按 `RGG` play semantics 与 `VPA` run semantics 同步解释。
- 验证/分析支持：对 deterministic / universal VPA 给出到 finite-state modular games 的 reduction，并给出复杂度分类。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：理论型 family，主要服务于 stack-sensitive recursive-game synthesis。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归开放系统上的 stack-sensitive controller synthesis。
2. 需要以 automaton 而不是逻辑表达胜利条件的 recursive games。
3. 希望把 `RGG` 支线继续接到 visibly pushdown specification family 的场景。

### 需求前提

1. 系统 / 环境交互可压成 `RGG`。
2. 控制器必须满足 modularity，即只用模块局部历史。
3. 胜利条件依赖 call / ret 结构，适合用 visibly pushdown automaton 编码。

### 不适用或高成本场景

如果 winning condition 只需 ordinary finite-state automaton，则退回更简单的 modular game 足够；如果更适合逻辑而不是 automaton 规格，可转向 [winning-caret-games-with-modular-strategies/desc.md](../winning-caret-games-with-modular-strategies/desc.md)。

## 与相邻形式主义的关系

相对 plain `RGG`，`VPMG` 新增的是 visibly pushdown specification；相对 `CaRet` modular games，它把 stack-sensitive requirement 从逻辑侧改写成 automaton 侧；相对 सामान्य pushdown automaton winning conditions，它靠“visible”限制重新保住可判定性。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RSM -> RGG` 支线不仅能长出 `CaRet` 逻辑规格分支，还能长出 `VPA` 自动机规格分支，从而把递归控制流模型和 visibly pushdown family 明确接到一起。

### 作为目标形式主义还是中间表示

更适合作为验证 / 合成阶段的中间表示，而不是需求建模前端。

### 对需求到模型生成的启发

当需求最终要落成“对所有模块化控制策略，所有带调用标记的执行词都必须被某类栈敏感 automaton 接受”时，`VPMG` 比普通 `RGG` 或 `LTL` modular games 更自然。

## 重要的相关工作

1. [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)：`RGG` 主干。
2. [winning-caret-games-with-modular-strategies/desc.md](../winning-caret-games-with-modular-strategies/desc.md)：逻辑规格版本的 sibling。
3. [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)：winning-condition 侧可见下推语言的上游模型。

## 文献分类总结

- 这篇论文最适合在演化树里承担：`RGG` 的 visibly-pushdown winning-condition 子枝。
- 它虽然不重新定义 `RGG` 语法，但确实稳定命名了一个新的 modular-game family，因此不应仅按“方法”处理。
- 后续如果继续补这条线，优先应找 `VPMG` 的 full version 或更明确的 `VPA/NWTL/CARET` modular-game family 论文，而不是泛泛的 pushdown-game complexity 论文。
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
