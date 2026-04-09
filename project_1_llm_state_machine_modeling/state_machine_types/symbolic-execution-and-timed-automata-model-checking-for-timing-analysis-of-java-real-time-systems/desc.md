# SymRT：基于符号执行与定时自动机的 Java 实时系统时序分析 / Symbolic execution and timed automata model checking for timing analysis of Java real-time systems

## 基本信息

- 标题：Symbolic execution and timed automata model checking for timing analysis of Java real-time systems
- 中文标题：SymRT：基于符号执行与定时自动机的 Java 实时系统时序分析
- 作者：Kasper S. Luckow，Corina S. Păsăreanu，Bent Thomsen
- 发表：*EURASIP Journal on Embedded Systems*，2015(1)，2015
- DOI：`10.1186/s13639-015-0020-8`
- 链接：https://doi.org/10.1186/s13639-015-0020-8
- 形式主义：`SymRT / Program NTA / JVM NTA / Hardware NTA / TETASARTS`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：用符号执行树替换 `CFG` 过近似的 Java 实时系统 timed-analysis 路线
- 工具/实现获取方式：原文给出项目主页 `http://people.cs.aau.dk/~luckow/symrt/`，并说明开源代码可从 `https://bitbucket.org/luckow/symrt/` 与 `https://bitbucket.org/luckow/jpf-symbc-rt` 获取。
- 标准/格式获取方式：核心承载是 `UPPAAL` 风格 timed automata、`NTA` 组合、`TCTL`/`sup`/`inf` queries；不是行业交换标准，而是分析工作流格式。

## 简报

这篇论文补的是“Java 实时程序如何稳定落成 timed automata 后端”的方法路线。它的关键改进不是再写一个 schedulability checker，而是把 `CFG` 级过近似换成了 symbolic execution tree，于是 Program NTA 只覆盖可行路径，进而让 `WCET/BCET`、`WCRT/WCBT` 和 schedulability 分析都更紧。

- 形式主义定位：`Java bytecode -> timed automata` 的分析方法与工具链，不是新的 timed automaton 家族。
- 构造方式简述：先用 `JPF-SYMBC-RT` 对程序做符号执行，再把 symbolic execution tree 后翻译成 Program NTA，并与 `JVM NTA`、`Hardware NTA`、task controllers 组合。
- 基础设施与场景简述：依托 `UPPAAL`、`TETASARTS`、`JPF-SYMBC-RT` 和开源工具链，服务安全关键 Java/SCJ 实时系统的时间分析。

```text
Java bytecode -> symbolic execution tree -> Program NTA -> JVM/Hardware/Task NTA composition -> UPPAAL queries -> WCET / BCET / WCRT / schedulability
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. symbolic execution tree；
2. Program NTA；
3. JVM NTA 与 Hardware NTA；
4. complete timing model；
5. `UPPAAL` queries for `WCET/BCET/WCRT/WCBT/schedulability`。

### 核心抽象

论文首先回顾 timed automata 网络：

$$
NTA = A_1 \parallel A_2 \parallel \cdots \parallel A_n
$$

上式中的符号逐项解释如下：

1. `$A_i$` 是单个 timed automaton。
2. `$\parallel$` 表示并行组合。
3. 各自动机通过同步信道与共享变量交互。

结合论文 4.1 节的系统架构，可把完整 timing model 保守整理为：

$$
N_{sys} = A_{prog} \parallel A_{jvm} \parallel A_{hw} \parallel A_{task}
$$

上式中的符号逐项解释如下：

1. `$A_{prog}$` 是由 symbolic execution tree 生成的 Program NTA。
2. `$A_{jvm}$` 是 Java Virtual Machine timing model。
3. `$A_{hw}$` 是 hardware timing model，例如 cache / pipeline 行为。
4. `$A_{task}$` 是任务控制器与调度策略自动机。
5. 这是根据论文架构图做的保守归纳，不是原文单行元组定义。

论文强调 Program NTA 的生成是在 Java bytecode 粒度进行的，可保守写成：

$$
loc_{i} \xrightarrow{bc_i} loc_{j}
$$

上式中的符号逐项解释如下：

1. `$bc_i$` 表示某条 Java bytecode instruction。
2. `loc_i` 与 `loc_j` 是翻译后 timed automaton 中的两个位置。
3. 对普通指令一般只有一条后继边。
4. 对分支指令，若对应 path condition 可满足，则会生成多条后继边。

### 一个最小例子与通俗解释

论文的 running example 是一个带分支的 Java 实时任务：

1. 程序里有条件分支与循环。
2. `JPF-SYMBC-RT` 用符号输入展开出 symbolic execution tree。
3. 每条可行路径对应到 Program NTA 中的一条控制流路径。
4. 再把 JVM、硬件和调度器拼上去，用 `UPPAAL` 直接问 `WCET/BCET`。

通俗地说，以前很多工具会先恢复 `CFG`，但 `CFG` 会把一些根本不可能同时成立的路径也算进去，结果时间上界会很松。`SymRT` 则先用符号执行过滤掉 infeasible paths，再翻译成 timed automata，因此估计更紧。

### 运行 / 接受 / 转移语义

论文把 schedulability 写成 reachability 问题。若 `\varphi` 是所有 `DeadlineOverrun_i` 位置的析取，则：

$$
A[]\ \neg \varphi
$$

上式中的符号逐项解释如下：

1. `$\varphi$` 表示“某个任务发生 deadline miss”。
2. `$A[]\neg\varphi$` 表示所有可达状态里都不会进入 deadline-overrun。
3. 这就是论文给出的 schedulability query。

论文还直接给出 `WCET/BCET` 查询：

$$
\mathrm{WCET} = sup\{TC.ExecutingThread\}:TC.wcet
$$

$$
\mathrm{BCET} = inf\{TC.Done\}:TC.wcet
$$

上式中的符号逐项解释如下：

1. `$TC$` 是 task controller。
2. `TC.wcet` 是对应 stopwatch clock。
3. `sup` 求可达路径上的上确界，即 `WCET`。
4. `inf` 求可达路径上的下确界，即 `BCET`。

对 `WCRT/WCBT`，论文也给出：

$$
\mathrm{WCRT} = sup\{TC.ExecutingThread\}:TC.wcrt
$$

$$
\mathrm{WCBT} = sup\{TC.ExecutingThread\}:TC.blockingTime
$$

### 语义边界

1. 论文明确要求程序终止；循环需要有 bound，递归深度也要有限。
2. 若 symbolic execution 深度上限过低，工具只保证在该 bound 内正确。
3. 对共享变量，`SymRT` 会引入 fresh symbolic values 做安全过近似。
4. 它的优势主要针对 Java bytecode timing analysis，不是通用 timed-automata 建模前端。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `NTA` 组合 | `$NTA = A_1 \parallel \cdots \parallel A_n$` | timed automata network 的基本骨架。 |
| 完整 timing model | `$N_{sys} = A_{prog} \parallel A_{jvm} \parallel A_{hw} \parallel A_{task}$` | 论文架构的保守整理。 |
| schedulability | `$A[]\neg\varphi$` | 是否存在 deadline miss。 |
| `WCET` 查询 | `$sup\{TC.ExecutingThread\}:TC.wcet$` | 直接由 `UPPAAL` 给出最坏执行时间。 |
| `BCET` 查询 | `$inf\{TC.Done\}:TC.wcet$` | 直接由 `UPPAAL` 给出最好执行时间。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | Program / JVM / Hardware / Task 四层都以 timed-state 形式进入模型。 |
| 事件 / 触发 | 强支持 | bytecode、scheduling events、sync channels 都被显式编码。 |
| 守卫 / 数据 | 很强 | path conditions、clock guards、shared-variable over-approx 都是一等对象。 |
| 层次 | 不支持 | 不是层次状态图语言。 |
| 并发 / 同步 | 很强 | 多任务控制器、JVM 与硬件模型通过 channel 组合。 |
| 时间约束 | 很强 | 核心目标就是时间分析。 |
| 连续动态 / 随机性 | 不支持 | 不处理混成连续动力学或概率。 |
| 可执行 / 可验证性 | 很强 | 直接落入 `UPPAAL` 的 model checking / sup / inf query 工作流。 |

### 形式化问题与性质

1. 这篇论文补的不是新的 `TA` 子类，而是更紧的 Java-to-`TA` translation route。
2. 对时序分析文库来说，它的关键价值是“symbolic execution tree 取代 `CFG` over-approximation”。
3. 它也说明 `WCET/BCET` 和 schedulability 可以共用同一 complete timing model。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. Java class files；
2. 系统配置与分析目标；
3. symbolic execution tree；
4. execution-environment timing model。

### 机器可处理承载方式

机器可处理承载方式包括：

1. Program NTA；
2. JVM NTA；
3. Hardware NTA；
4. task-controller automata；
5. `UPPAAL` queries。

### 交换与互操作

互操作重点在以下链路：

1. `JPF-SYMBC-RT` 产出 symbolic execution tree；
2. `TETASARTS` / `SymRT` 组合生成 complete timing model；
3. `UPPAAL` 消费这些 automata 和 queries 给出分析结果。

## 配套基础设施

- 建模/编辑工具：`SymRT` 前端配置、`JPF-SYMBC-RT`、`TETASARTS`。
- 解析/交换/元模型支持：Java bytecode、symbolic execution tree、`UPPAAL` timed automata。
- 仿真/执行支持：`UPPAAL` simulator 可回放导致 `WCET` 的 trace。
- 验证/分析支持：`WCET`、`BCET`、`WCRT`、`WCBT`、schedulability、processor utilization / idle time。
- 代码生成/转换支持：核心是 model extraction，不是部署代码生成。
- 标准化或社区生态：依托 `UPPAAL` 和开源 `Bitbucket` 项目，属于研究型 timing-analysis ecosystem。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. Java / Safety Critical Java 实时任务的时间分析；
2. 需要同时做 `WCET/BCET` 与 schedulability 的嵌入式系统；
3. 需要把程序、JVM、硬件与调度器统一放进一个 formal timing model 的场景。

### 需求前提

1. 循环和递归必须可界定。
2. 需要有 timing scheme 或 JVM / hardware NTA。
3. 团队接受 `UPPAAL` query 风格的后端分析。

### 不适用或高成本场景

如果目标程序高度依赖不可控原生库、无界动态行为或难以为 JVM / hardware 建 timing model，这条路线的建模成本会迅速升高。

## 与相邻形式主义的关系

相对 [a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)，这里不是直接从架构模型下手，而是从 Java bytecode 与符号执行树下手。相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，`UPPAAL` 是后端平台，而 `SymRT` 是一条 Java-to-`UPPAAL` 的抽取路线。相对 [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)，后者优化的是 timed-automata network 的 zone 搜索语义，这里优化的是 program-to-model extraction 阶段。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明从程序级 artifact 自动得到 timed automata 是现实可行的，不一定总要手工建模。
2. 对后续“需求到模型”路线来说，symbolic execution 能帮助筛掉 infeasible behavior，这对提升模型可信度很有参考价值。
3. 它也给 `project_3` 一条很明确的验证落点：`UPPAAL` queries 对 timing profile 的承载非常成熟。

### 作为目标形式主义还是中间表示

更像从程序到 timed-verification backend 的中间表示与方法路线，不是最终面向领域专家的规格语言。

### 对需求到模型生成的启发

1. 路径可行性分析应尽量前置，而不是把所有分支都丢给后端。
2. 若未来要从源码或半结构化设计模型抽 timed automata，Program NTA 这种中间层很有借鉴价值。
3. 任务控制器与调度器最好显式分离成独立 automata，再和程序体组合。

### 现实限制

这条路线需要相当多 execution-environment knowledge；如果硬件、JVM 或共享变量干扰无法良好抽象，最终模型仍可能很重。

## 重要的相关工作

1. [uppaal-40/desc.md](../uppaal-40/desc.md)：经典 `UPPAAL` 平台。
2. [timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md](../timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md)：更传统的实时调度 `TA` 分析路线。
3. [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)：在 `TA` 网络搜索后端上的进一步优化。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`SymRT / Program NTA / JVM NTA / Hardware NTA / TETASARTS`
- 归类理由：论文主贡献是 Java 实时系统到 timed-automata 后端的构造与分析方法路线，而不是新的语言标准。
