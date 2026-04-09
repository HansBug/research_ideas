# 通过有限自动机学习进行时间自动机验证与综合 / Timed Automata Verification and Synthesis via Finite Automata Learning

## 基本信息

- 标题：Timed Automata Verification and Synthesis via Finite Automata Learning
- 中文标题：通过有限自动机学习进行时间自动机验证与综合
- 作者：Ocan Sankur
- 发表：*Journal of Automated Reasoning*，69(2)，2025
- DOI：`10.1007/s10817-025-09730-z`
- 链接：https://doi.org/10.1007/s10817-025-09730-z
- 形式主义：`Timed Automata / finite automata learning / compRTMC`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：learning-based compositional model checking and controller synthesis method for timed automata
- 工具/实现获取方式：原文明确给出原型入口 `https://github.com/osankur/compRTMC/releases/tag/tacas23`，并说明实现使用 `LearnLib`、`TChecker`、`NuSMV` 等组件。
- 标准/格式获取方式：主承载是 `TChecker` timed automata、`SMV/Verilog` 有限状态模型、学习得到的 `DFA` 假设机和 timed-game inputs；它不是交换标准。

## 简报

这篇论文补的是时间自动机验证里的“学习式离散化”方法路线。作者把输入系统看成“大离散有限状态部分 `A` + 相对较小的 timed-automaton 部分 `T`”，再用主动自动机学习构造 `T` 的 `DFA` 近似 `H`，从而把原本难以扩展的大离散实时问题拆给两类后端：timed model checker 只回答关于 `T` 的 queries，finite-state model checker / game solver 则负责处理大的离散空间。

- 形式主义定位：`Timed Automata` 的 compositional verification / synthesis method，而不是新的 timed-automata 子类。
- 构造方式简述：把 `A \parallel T` 看成分解结构，用 `L* / TTT` 学习 `H`，再通过 assume-guarantee 规则把 `A \parallel T` 的验证或综合转成 `A \parallel H` 的离散问题。
- 基础设施与场景简述：依托 `LearnLib`、`TChecker`、`NuSMV`、`Uppaal-TIGA` 比较实验和 `Verilog + TChecker` 输入组合，服务大离散空间下的 timed verification / controller synthesis。

```text
large finite-state component A + smaller timed component T -> DFA learning of H -> finite-state checking / game solving on A || H -> query-guided refinement via TChecker
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata；
2. finite automata learning，尤其 `L*` 与 `TTT`；
3. assume-guarantee verification rule；
4. controller-silent timed games；
5. one-sided abstraction and counterstrategy refinement。

### 核心抽象

论文直接给出 timed automaton 定义：

$$
T = (L, \ell_0, \Sigma, Inv, C, E, F)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$\ell_0$` 是初始 location。
3. `$\Sigma$` 是动作字母表。
4. `$Inv$` 为各 location 上的 invariants。
5. `$C$` 是 clocks 集合。
6. `$E$` 是边集合，边形如 `$\ell \xrightarrow{g,\sigma,R} \ell'$`。
7. `$F$` 是 accepting locations。

论文把 timed 部分与 finite-state 部分组合起来，并利用：

$$
L(A \parallel T) = L(A) \cap L(T)
$$

上式中的符号逐项解释如下：

1. `$A$` 是 finite automaton 或 large finite-state component 的离散抽象。
2. `$T$` 是 timed automaton。
3. 并行组合的 untimed language 等于两者语言交集。
4. 这正是后续 learning-based assume-guarantee 推理成立的基础。

若学习到 `$H$` 满足 `$L(T) \subseteq L(H)$`，则论文使用规则：

$$
\frac{L(T) \subseteq L(H) \qquad L(A \parallel H) \subseteq Spec}{L(A \parallel T) \subseteq Spec}
$$

上式中的符号逐项解释如下：

1. `$H$` 是通过学习得到的 `DFA` 假设机。
2. `$Spec$` 是目标性质对应的 regular language。
3. 这就是本文 model checking 算法的 assume-guarantee 核心。

学习环中的两类 queries 也很关键：

$$
\mathrm{MQ}(w) \in \{yes,no\}, \qquad \mathrm{EQ}(H) \Rightarrow \text{yes or counterexample}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{MQ}(w)$` 询问单词 `$w$` 是否属于目标语言。
2. `$\mathrm{EQ}(H)$` 询问当前 hypothesis automaton `$H$` 是否已与目标语言等价。
3. timed model checker 负责回答与 `$T$` 相关的 membership / inclusion 类 queries。

### 一个最小例子与通俗解释

论文里给了一个典型 planning / timed-game 例子：

1. 有一个大的有限状态游戏 `G`，表示机器人、障碍物和门的离散位置。
2. 另有较小的 timed automaton `T`，负责限制“门多久能开关、障碍多久移动一次”等时序约束。
3. 直接在 `G \parallel T` 上做 timed-game synthesis 很容易被大离散空间拖垮。
4. 论文改为学习一个 `DFA` 近似 `T` 的 untimed language，再先在 `G \parallel H` 上做有限状态求解。

通俗地说，这个方法像“先把实时部分压成一个会说话的离散代理”。它不直接消掉 timing，而是让定时系统在 query 层回答“哪些 label 序列可行”，然后把大规模搜索工作交给更擅长离散空间的工具。

### 运行 / 接受 / 转移语义

论文把 finite automaton 与 timed automaton 的并行组合也定义成 timed automaton：

$$
A \parallel T = (L', \ell'_0, \Sigma, Inv', C, E', F')
$$

上式中的符号逐项解释如下：

1. `$A$` 是 finite automaton，可带 `\epsilon`-transitions。
2. `$T$` 是 timed automaton。
3. `$L' = Q \times L$`，把离散状态与 timed locations 配对。
4. `$E'$` 的 guard 和 reset 主要来自 timed 边，而 finite automaton 提供 label compatibility。

controller synthesis 侧，论文考虑 timed games：

$$
G \parallel T
$$

上式中的符号逐项解释如下：

1. `$G$` 是 finite safety game。
2. `$T$` 是 timed automaton。
3. 目标通常写成避免坏状态对 `Bad \times F` 的 reachability。

在 one-sided abstraction 下，论文给出代表性结论：

$$
L(T) \subseteq L(H) \land \mathrm{Win}_C(G \parallel H) \Rightarrow \mathrm{Win}_C(G \parallel T)
$$

上式中的符号逐项解释如下：

1. `$H$` 是 `T` 的 over-approximation `DFA`。
2. `$\mathrm{Win}_C$` 表示 Controller 赢得相应 safety objective。
3. 这让 finite-state game solver 的结果可以安全迁回原 timed game。

### 语义边界

1. 这是一条方法路线，不是新的 timed automata 语义分支。
2. model checking 主要处理 untimed properties，timed properties需先通过 tester/component reduction 进入。
3. controller synthesis 算法是 sound but incomplete。
4. 方法特别针对“大离散部分 + 相对小但非平凡 timed 部分”的分解结构，不是所有 `TA` 模型都受益。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$T=(L,\ell_0,\Sigma,Inv,C,E,F)$` | timed component 的标准对象。 |
| 组合语言 | `$L(A \parallel T)=L(A)\cap L(T)$` | compositional verification 的基础。 |
| assume-guarantee rule | `$\frac{L(T)\subseteq L(H)\ \ L(A\parallel H)\subseteq Spec}{L(A\parallel T)\subseteq Spec}$` | 学习到的 `DFA` 假设如何支撑验证。 |
| learning queries | `$\mathrm{MQ}(w), \mathrm{EQ}(H)$` | automata learning 的交互接口。 |
| one-sided abstraction | `$L(T)\subseteq L(H)\land \mathrm{Win}_C(G\parallel H)\Rightarrow \mathrm{Win}_C(G\parallel T)$` | controller synthesis 侧的关键安全结论。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | timed automata 与 finite-state component 的分解是全文核心。 |
| 事件 / 触发 | 很强 | labels 是 learning、composition 和 solver 对接的中心。 |
| 守卫 / 数据 | 中等支持 | timed side 处理 clocks，finite side 承担大离散状态。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等到强 | 通过 parallel composition 组合 timed 与 finite components。 |
| 时间约束 | 很强 | clocks、timed games、timed automata semantics 都是主轴。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic line。 |
| 可执行 / 可验证性 | 很强 | `TChecker`、`LearnLib`、`NuSMV`、`Uppaal-TIGA` 等组成完整实验链。 |

### 形式化问题与性质

1. 本文的关键不是“再做一个 timed checker”，而是“怎样把 timed piece 学习成 finite abstraction”。
2. automata learning 在这里只学习 timed component 的 untimed language，而不是学习整个系统。
3. synthesis 侧的一大亮点是 one-sided abstraction，它把真实 timed-game 难题拆成 finite-game 可解子问题。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `TChecker` timed automata；
2. `SMV` finite-state models；
3. `Verilog` + uncontrollable inputs for synthesis；
4. automata-learning queries and hypotheses。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed automata edges 和 clock constraints；
2. learned `DFA` hypotheses；
3. membership / inclusion oracles；
4. finite-state model checking or game solving backends。

### 交换与互操作

互操作是这篇论文的核心：

1. `TChecker` 负责 timed side queries。
2. `LearnLib` 负责 `TTT` 等 learning algorithm。
3. `NuSMV` 和 finite-state solvers 负责离散验证。
4. 对 synthesis，`Verilog` 与 `TChecker` 组合形成 controller-silent timed-game 输入。

## 配套基础设施

- 建模/编辑工具：原型直接消费 `TChecker` timed automata、`SMV` 和 `Verilog` 输入。
- 解析/交换/元模型支持：finite-state/timed-state 分离输入，label-based composition，learning hypotheses。
- 仿真/执行支持：重点是 verification / synthesis，不是 runtime execution platform。
- 验证/分析支持：model checking、assume-guarantee reasoning、controller synthesis、over/under-approximation refinement。
- 代码生成/转换支持：主要是 solver / learner 之间的模型与假设转换，不主打部署代码生成。
- 标准化或社区生态：`LearnLib`、`TChecker`、`NuSMV`、`Uppaal-TIGA` 比较基准共同构成其生态。

## 适用场景与需求前提

### 适用场景

适合大离散状态空间但 timed component 相对较小的实时系统验证与控制综合，例如调度器约束、协议时序外壳、环境约束型 planning / controller synthesis。

### 需求前提

1. 系统能分解成 large finite-state component 与 smaller timed component。
2. 目标性质最好能转为 untimed regular-language style checking，或通过 tester 降到这一层。
3. 团队接受 learning loop 带来的额外 queries 和假设机收敛过程。
4. synthesis 侧需满足论文假设，例如 controller-silent timed games 等限制。

### 不适用或高成本场景

如果系统是“时钟结构巨大而离散部分不大”，传统 zone-based 工具可能更直接；若目标必须处理完整 timed logic 或要求 synthesis 完备性，这条路线也有局限。

## 与相邻形式主义的关系

相对 [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)，本文不是改 `TA` 到 solver 的编码，而是改验证策略；相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，`UPPAAL-Tiga` 代表经典 timed-game 求解主线，而本文强调 large discrete space 下的学习式缩减；相对 [libalf-the-automata-learning-framework/desc.md](../libalf-the-automata-learning-framework/desc.md) 与 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，那些条目提供 learning infrastructure，本条则展示 learning 如何反哺 timed verification / synthesis。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为“复杂 timed model 太大时如何做 verification profile 缩减”提供了很有代表性的方法证据。
2. 学习得到的 `DFA` 假设机也提示了一个很适合 LLM 参与的中间表示层。
3. 对 `project_2` 和 `project_4` 来说，counterexample-guided hypothesis refinement 和 over/under-approximation 交替都很值得借鉴。

### 作为目标形式主义还是中间表示

更像 timed verification / synthesis 方法路线，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 若需求系统天然有“小 timed shell + 大 discrete core”结构，就不该把两者无差别揉成一个庞大 `TA`。
2. 可以考虑让 LLM 先抽取 label alphabet 和 finite assumption，再交给 learning / checking loop 细化。
3. timed-game 综合中把 environment timing discipline 单独建模，能明显改善可扩展性。

### 现实限制

本文的优势依赖于结构分解前提；没有这种分解时，learning-based route 可能并不优于传统 zone-based tools。

## 重要的相关工作

1. [improved-bounded-model-checking-of-timed-automata/desc.md](../improved-bounded-model-checking-of-timed-automata/desc.md)：另一条时间自动机验证方法路线。
2. [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：经典 timed-game controller synthesis 工具锚点。
3. [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：主动自动机学习基础设施主线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / finite automata learning / compRTMC`
- 归类理由：主贡献是把自动机学习与 assume-guarantee reasoning 接到 timed verification / synthesis 上，属于典型的 timed-automata 方法路线条目。
