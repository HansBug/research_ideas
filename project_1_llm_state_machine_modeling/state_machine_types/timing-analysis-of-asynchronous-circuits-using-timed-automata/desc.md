# 用定时自动机分析异步电路时序 / Timing Analysis of Asynchronous Circuits using Timed Automata

## 基本信息

- 标题：Timing Analysis of Asynchronous Circuits using Timed Automata
- 中文标题：用定时自动机分析异步电路时序
- 作者：Oded Maler，Amir Pnueli
- 发表：*Correct Hardware Design and Verification Methods*，`LNCS 987`，pp. 189-205，1995
- DOI：`10.1007/3-540-60385-9_12`
- 链接：https://doi.org/10.1007/3-540-60385-9_12
- 形式主义：`Timed Automata / asynchronous circuits / KRONOS route`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：asynchronous-circuit timing analysis via timed-automata translation
- 工具/实现获取方式：原文明确把分析落到 `Kronos` 工具，并报告初步实验；正文未给现代公开仓库，但 `KRONOS` 是该路线的核心后端。
- 标准/格式获取方式：主承载对象是 delay equations、piecewise-continuous Boolean signals、共享变量式 timed automata 与可达性/综合问题；它不是行业交换标准。

## 简报

这篇论文补的是 timed-automata 线里非常经典、也很适合 `state_machine_types` 文库的一条工程桥梁：把异步数字电路从 delay equations 系统地翻译成定时自动机网络，使时序分析不再只能靠 ad-hoc simulation，而能直接做可达性、输入时序约束推导和参数合成。

- 形式主义定位：`asynchronous circuit -> timed automata` 的分析方法路线，不是新的 timed-automaton 家族。
- 构造方式简述：先把每根线的延迟关系写成区间 delay inclusion，再为每个信号构造局部 timed automaton，最后组合成全局 automaton 并交给 `KRONOS`。
- 基础设施与场景简述：依托 delay equations、shared-variable timed automata 和 `KRONOS`，服务异步电路的 reachability analysis、输入约束推导与 delay synthesis。

```text
asynchronous circuit / delay equations -> local timed automata -> composed timed automaton -> KRONOS reachability / synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. piecewise-continuous Boolean signals；
2. ideal / latency / nondeterministic delay；
3. digital circuits as delay inclusions；
4. timed automata with shared variables；
5. circuit-to-automaton translation。

### 核心抽象

原文对异步数字电路给出的核心对象是：

$$
N = (X,F,D)
$$

上式中的符号逐项解释如下：

1. `$X=\{x_1,\ldots,x_k\}$` 是电路线集合。
2. `$F=\{f_1,\ldots,f_k\}$` 是各线的组合布尔函数。
3. `$D=\{(l_1,u_1),\ldots,(l_k,u_k)\}$` 是每根线的最小/最大传播延迟区间。
4. 整个电路行为不是单次离散跳转，而是所有信号在实时间上的解集。

电路行为被写成一组 simultaneous inclusions：

$$
x_i \in \Delta_{[l_i,u_i]}(b_i, f_i(x_1,\ldots,x_k))
$$

上式中的符号逐项解释如下：

1. `$x_i$` 是第 `$i$` 根线对应的布尔信号。
2. `$\Delta_{[l_i,u_i]}$` 是区间延迟算子。
3. `$b_i$` 是初始默认值。
4. `$f_i(x_1,\ldots,x_k)$` 是由其他线决定的瞬时逻辑值。
5. 该 inclusion 表示“输入变化若持续足够久，则在 `[l_i,u_i]` 范围内传播到输出”。

原文给出的 timed automaton 不是经典 `A=(L,l_0,C,E,...)` 课本写法，而是带共享变量的版本：

$$
A = (V_A,C_A,R,O)
$$

上式中的符号逐项解释如下：

1. `$V_A$` 是 automaton 自有的布尔变量集合。
2. `$C_A$` 是该 automaton 自有的 clocks。
3. `$R : Q_A \times Q_A \to F(V \setminus V_A, C)$` 给每对离散状态分配守卫公式。
4. `$O : Q_A \times Q_A \to 2^{C_A}$` 指定每次离散迁移要 reset 的本地 clocks。
5. `$Q_A$` 是 `$V_A$` 的全部布尔赋值空间。

论文的核心等价性可以保守整理为：

$$
L(A)[V] = Sol(N)
$$

上式中的符号逐项解释如下：

1. `$L(A)$` 是 timed automaton 生成的全体信号。
2. `$[V]$` 表示只观察原电路的可观测变量维度。
3. `$Sol(N)$` 是电路 delay equations 的解集。
4. 这说明翻译后的 automaton 精确保留了电路的时序行为。

原文还给出整体规模结论：

$$
\text{every } k\text{-wire circuit can be transformed into an equivalent timed automaton with } 2k \text{ variables and } k \text{ clocks}
$$

上式中的符号逐项解释如下：

1. `$k$` 是原电路线数。
2. `2k` 来自每根线同时需要可观测/隐藏层面的变量信息。
3. `$k$` 个 clocks 对应每根线的延迟计时。
4. 这为工程上“电路能否落到 timed-automata backend”提供了直接复杂度刻画。

### 一个最小例子与通俗解释

最直观的例子是一根带延迟的线：

1. 输入信号先从 `0` 变为 `1`。
2. 如果这个变化只是一瞬抖动，不足最小持续时间 `$l$`，输出可以不变。
3. 如果变化持续足够久，则输出必须在 `[l,u]` 时间窗口内切换。
4. 每个局部 timed automaton 就是在追踪“这根线已经稳定多久、是否该触发输出变化”。

通俗地说，这种建模把“门延迟”和“输入到达时间不确定性”都变成了 clocks 上的约束，从而不必一条一条枚举仿真轨迹，而是一次性分析整片连续时间区域。

### 运行 / 接受 / 转移语义

原文采用 dense-time 语义，并允许 automata 通过 continuously present shared variables 通信。其要点是：

1. 在离散状态不变时，clock 按连续时间统一增长。
2. 只有当某个 `R(q,q')` 被满足时，才允许从 `$q$` 跳到 `$q'$`。
3. 迁移发生时，`O(q,q')` 中的 clocks 被 reset。
4. 全局系统通过组合多个局部 automata，精确反映延迟依赖和结构依赖。

与经典 timed automata 教科书语义相比，本文更强调：

1. 可观测变量与隐藏变量的区分；
2. 通过 shared variables 而非 message passing 通信；
3. 直接用信号语义而不是 sampled-step 语义。

### 语义边界

1. 论文面向的是异步数字电路的时序层，不是晶体管级连续物理建模。
2. delay 模型允许不确定区间，但仍是离散逻辑值上的连续时间约束。
3. 主线问题是 reachability、输入约束推导和 delay synthesis，而不是一般概率/混成分析。
4. 若系统关键行为无法压成有限条线与区间延迟，这条翻译路线会失效。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 电路元组 | `$N=(X,F,D)$` | 异步电路的高层结构表示。 |
| delay inclusion | `$x_i \in \Delta_{[l_i,u_i]}(b_i,f_i(x_1,\ldots,x_k))$` | 每根线的时序传播语义。 |
| automaton 元组 | `$A=(V_A,C_A,R,O)$` | 共享变量式 timed automaton 骨架。 |
| 行为等价 | `$L(A)[V]=Sol(N)$` | 翻译后 automaton 精确保留电路行为。 |
| 尺度结论 | `$k \mapsto (2k\text{ vars}, k\text{ clocks})$` | 翻译规模可控的总体结论。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 电路离散逻辑模式被显式编码到自动机状态。 |
| 事件 / 触发 | 很强 | 输入变化与延迟到期共同触发迁移。 |
| 守卫 / 数据 | 中等 | 守卫主要是 clocks 与共享布尔变量。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 很强 | 多根线的局部 automata 通过共享变量组合。 |
| 时间约束 | 很强 | 核心就是区间延迟与连续时间分析。 |
| 连续动态 / 随机性 | 不支持 | 不是一般 hybrid / stochastic 模型。 |
| 可执行 / 可验证性 | 很强 | 直接对接 `KRONOS` 做分析与综合。 |

### 形式化问题与性质

1. 论文把异步电路 timing analysis 统一拉入 timed-automata 语境。
2. 它特别适合处理 gate delay、input arrival time 和初始条件不确定性。
3. 与单次仿真相比，symbolic reachability 可以一次覆盖无穷多条时间轨迹。
4. 这也是 `KRONOS` 早期应用到异步电路的重要锚点。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 以布尔线和延迟区间表示的电路；
2. signal-level delay equations；
3. 每根线对应的局部 timed automaton。

### 机器可处理承载方式

机器可处理承载方式包括：

1. piecewise-continuous Boolean signals；
2. interval-delay operators；
3. shared-variable timed automata；
4. 组合后的全局自动机。

### 交换与互操作

互操作重点在：

1. 电路语义先写成 delay equations；
2. 再系统翻成 timed automata；
3. 最终落到 `KRONOS` 这类 timed backend。

## 配套基础设施

- 建模/编辑工具：原文不主打图形编辑器，核心是电路 delay-equation 建模与 `KRONOS` 分析。
- 解析/交换/元模型支持：signals、delay operators、timed automata with shared variables。
- 仿真/执行支持：重点不是普通仿真，而是 symbolic reachability。
- 验证/分析支持：reachability、proper-functioning 条件推导、delay-parameter synthesis。
- 代码生成/转换支持：核心是从 circuit model 到 timed automaton 的翻译，不是部署代码生成。
- 标准化或社区生态：依托 `Timed Automata` / `KRONOS` 早期实时验证生态。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 异步数字电路 timing analysis；
2. 输入到达时间和门延迟存在不确定性的硬件分析；
3. 需要自动推出安全输入时序约束或部件 delay 约束的场景。

### 需求前提

1. 电路应能抽成有限根布尔线和组合函数。
2. delay 应能保守表示为区间 `[l,u]`。
3. 目标问题主要关心 reachability / deadline-style 时序性质。
4. 系统规模要允许进入 timed-automata backend。

### 不适用或高成本场景

若关键问题在模拟电路连续波形、复杂模拟噪声或数据路径算术，而不是离散逻辑加连续时间延迟，那么本文路线并不直接适用。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文不是 timed automata 本体定义，而是早期硬件应用桥梁；相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，本文更像 `KRONOS` 在异步电路上的典型应用母线；相对 [petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md](../petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md)，后者更偏 `STG` 异步控制器综合，而本文走的是 `Timed Automata` timing-analysis 路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明了硬件/控制逻辑的时序不确定性可以稳定落到 `Timed Automata` 后端。
2. 对后续控制系统状态机建模来说，这类“从结构模型到 timed backend”的桥梁很有参考价值。
3. 论文中的输入时序约束推导也接近 `project_2 / project_3` 想要的性质生成与验证 profile 思路。

### 作为目标形式主义还是中间表示

更适合作为从硬件结构/时序需求转向形式验证的中间表示，而不是前端需求语言。

### 对需求到模型生成的启发

1. 时序需求不一定直接写在状态机里，也可以先由结构和 delay 范围推导。
2. 连续时间不确定性进入后端时，应尽量保持 clocks + guard 这种规则骨架。
3. 异步控制逻辑的验证需要把“是否稳定持续足够久”显式建模出来。

## 重要的相关工作

1. [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文所有时钟语义的理论母线。
2. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：本文分析实际落到的 timed-automata 验证后端。
3. [petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md](../petrify-a-tool-for-manipulating-concurrent-specifications-and-synthesis-of-asynchronous-controllers/desc.md)：异步电路线另一条重要 `STG` / `Petri` 路线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / asynchronous circuits / KRONOS route`
- 论文角色：asynchronous-circuit timing analysis via timed-automata translation
- 归类理由：论文主体贡献是把异步电路系统化翻译到 `Timed Automata` 并做 `KRONOS` 分析，核心是方法路线，不是新的标准或运行时平台。
