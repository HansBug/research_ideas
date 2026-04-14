# 秒表的惊人威力 / The Impressive Power of Stopwatches

## 基本信息

- 标题：The Impressive Power of Stopwatches
- 中文标题：秒表的惊人威力
- 作者：Franck Cassez, Kim G. Larsen
- 发表：收录于 *CONCUR 2000 --- Concurrency Theory*, LNCS 1877, pp. 138-152, 2000
- DOI：`10.1007/3-540-44618-4_12`
- 链接：https://doi.org/10.1007/3-540-44618-4_12
- 形式主义：`Stopwatch Automata (SWA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文报告了 `UPPAAL` 的 stopwatch-extension；机器可处理入口是 `SWA / LSWA / LHA` 之间的 translation。
- 标准/格式获取方式：原文没有交换标准，核心承载方式是 `LHA` 七元组语义、`0/1` 导数限制、带 `τ`-delay 的 timed language 接受语义和 translation schema。

## 简报

这篇论文把 `Timed Automata` 上的“时钟要么一直走、要么 reset”为“变量在某些 location 可停表”这件事正式做成了 `Stopwatch Automata`。论文最强的结论不是单纯说“秒表很方便”，而是证明：带不可观察 delay 的 `SWA` 在 timed-language 表达力上与 `Linear Hybrid Automata (LHA)` 一样强。换句话说，从 `Timed Automata` 往前只迈出“导数可取 `0/1`”这一步，表达力就一下子顶到 `LHA`。对演化树来说，这正是 `Timed Automata -> Stopwatch Automata` 这条经典子枝最需要的模型本体代表条目。

- 形式主义定位：`Timed Automata` 主干上的 pause/resume 子类，允许变量在 location 中以 `0` 或 `1` 的速率演化。
- 构造方式简述：把 `Timed Automata` 视作 `\dot x = 1` 的特例，再把某些 location 的导数放宽为 `0`，并允许 `τ`-delay 参与语言接受。
- 基础设施与场景简述：论文给出 `LHA -> LSWA -> SWA` 翻译，并实现了 `UPPAAL` 的 stopwatch 扩展版用于 reachability 近似分析。

```text
Timed Automata -> add stoppable clocks (0/1 rates) -> Stopwatch Automata -> translate Linear Hybrid Automata -> UPPAAL stopwatch analysis
```

## 形式主义定义与核心对象

### 定义对象

论文先用 `Linear Hybrid Automata (LHA)` 给出统一语义，再把 `SWA` 定义成其一个重要子类。核心对象仍然是有限位置 + 实值变量，只是变量导数被限制成 `0` 或 `1`。

### 核心抽象

论文使用的上位模型是：

$$
H = (N,l_0,V,A,E,\mathrm{Act},\mathrm{Inv})
$$

上式中的符号逐项解释如下：

1. `N` 是有限位置集。
2. `l_0` 是初始位置。
3. `V` 是实值变量集。
4. `A` 是可观察动作集。
5. `E` 是带 guard、action 和 assignment 的边集。
6. `\mathrm{Act}(l)` 给出位置 `l` 中各变量的一阶导数区间。
7. `\mathrm{Inv}(l)` 是位置不变式。

在此基础上，论文明确区分三类：

$$
\mathrm{TA},\quad \mathrm{SWA},\quad \mathrm{LSWA}
$$

其中：

1. `TA` 要求所有 clocks 的导数都等于 `1`。
2. `SWA` 允许变量在某位置上的导数为 `0` 或 `1`。
3. `LSWA` 则是在 `SWA` 的 `0/1` 导数骨架上进一步允许线性 guards / assignments。

### 一个最小例子与通俗解释

最小例子可以是一个任务的“运行/暂停”计时器 `x`。在 `Run` 位置取 `\dot x = 1`，在 `Pause` 位置取 `\dot x = 0`；当系统暂停时，`x` 保留旧值但不再增长，恢复运行时再继续累计。普通 `Timed Automata` 的 clock 无法直接表达这种“冻结再继续”的语义，因为普通 clock 只能一直流逝并被 reset。

通俗地说，`Stopwatch Automata` 就是“能按模式停住的时钟自动机”。它比普通 `Timed Automata` 多的不是一般数据，而是一个很工程化也很关键的能力：计时可以被抢占、冻结、再恢复。

### 运行 / 接受 / 转移语义

论文把语义写成 timed transition system。离散跳转可保守写成：

$$
\langle l,v \rangle \xrightarrow{a} \langle l',v' \rangle
$$

要求存在边 `\langle l,\gamma,a,\alpha,l' \rangle \in E`，并满足 `\gamma(v)=\mathrm{tt}`、`v'=\alpha(v)` 且 `\mathrm{Inv}(l')(v')=\mathrm{tt}`。

连续流逝步可保守写成：

$$
\langle l,v \rangle \xrightarrow{d} \langle l,v+d\cdot t \rangle
$$

其中 `d \in \mathrm{Act}(l)`，而在 `SWA` 中每个分量的导数只允许取 `0` 或 `1`。这正是“stopwatch”语义的数学核心。

### 语义边界

论文给出的层级关系是：

$$
\mathrm{TA} \subset \mathrm{SWA} \subseteq \mathrm{LSWA} \subseteq \mathrm{LHA}
$$

其中 `SWA` 和 `LSWA` 的真正边界不在“有没有 clocks”，而在“导数是否允许停住，以及是否允许线性 guards / assignments”。

### 关键性质与判定边界

论文主定理是：

$$
TL_{\mathrm{SWA}} = TL_{\mathrm{LHA}}
$$

也就是 `SWA` 与 `LHA` 在 timed-language 表达力上等强。作者通过两步证明达成这一点：

$$
TL_{\mathrm{SWA}} = TL_{\mathrm{LSWA}},\qquad TL_{\mathrm{LSWA}} = TL_{\mathrm{LHA}}
$$

工程含义同样直接：`LHA` 的 reachability 分析可以转约到 `SWA` 上，再交给 stopwatch-aware 的 `UPPAAL` 做近似分析。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限位置 `N` 是离散骨架。 |
| 事件 / 触发 | 支持 | 边上动作与 `τ`-delay 共同组成行为。 |
| 守卫 / 数据 | 强支持时钟/线性约束 | `LSWA` 还允许线性 guards / assignments。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 部分支持 | 论文重点不是组合语义，而是表达力翻译。 |
| 时间约束 | 强支持 | 变量既可流逝也可冻结。 |
| 连续动态 / 随机性 | 支持受限连续、无随机 | 导数只取 `0/1`，比 `LHA` 更受限。 |
| 可执行 / 可验证性 | 强支持 | 可把 `LHA` reachability 归约到 `SWA` 分析。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 上位模型 | `$H=(N,l_0,V,A,E,\mathrm{Act},\mathrm{Inv})$` | 用 `LHA` 七元组统一给语义。 |
| stopwatch 限制 | `$\dot x \in \{0,1\}$` | 变量要么走表、要么停表。 |
| 子类层级 | `$\mathrm{TA} \subset \mathrm{SWA} \subseteq \mathrm{LSWA} \subseteq \mathrm{LHA}$` | 明确 `SWA` 在 timed / hybrid 谱系中的位置。 |
| 主定理 | `$TL_{\mathrm{SWA}} = TL_{\mathrm{LHA}}$` | `SWA` 在 timed-language 表达力上达到 `LHA`。 |
| 工程后果 | `$\text{Reachability}(LHA) \to \text{Reachability}(SWA)$` | 给 `UPPAAL` stopwatch extension 提供理论基础。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求中的时间量是否存在暂停/抢占/恢复。
2. 若只是一直增长的 clocks，用普通 `TA` 即可。
3. 若某些计时量必须在某些模式冻结，则转成 `SWA`。
4. 若同时还需要线性 guards / assignments，可进一步看 `LSWA`。

### 机器可处理承载方式

机器可处理承载方式是 `LHA/SWA` 的位置图、导数约束、线性 guard / assignment 与 translation schema，而不是某种标准交换格式。

### 交换与互操作

它和 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 `Timed Automata` 母线直接相连，也和 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)、[whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md) 的 `Hybrid Automata` 主干相交：`SWA` 处在两者之间，既是 `TA` 子类，又能顶到 `LHA` 的表达力边界。

## 配套基础设施

- 建模/编辑工具：论文报告了 `UPPAAL` 的 stopwatch-extension。
- 解析/交换/元模型支持：核心是 `LHA -> LSWA -> SWA` 翻译，而非统一交换格式。
- 仿真/执行支持：可按 timed transition system 执行。
- 验证/分析支持：reachability 近似分析、translation-based analysis、DBM-like data structures 的扩展。
- 代码生成/转换支持：论文提供了从 `LHA` 到 `SWA` 的系统翻译。
- 标准化或社区生态：是 `Timed Automata` 与 `Hybrid Automata` 之间极关键的桥接条目。

## 适用场景与需求前提

### 适用场景

适合 preemption、pause/resume、任务挂起恢复、带冻结时钟的调度模型，以及希望把某些 `LHA` 近似降到更可工具化 timed 模型的场景。

### 需求前提

1. 时间量必须能明确拆成“走表/停表”两种模式。
2. 若想保住 `SWA` 结构，连续变化最好能限制在 `0/1` 速率。
3. 若需求本身已明显超出线性 guards / assignments，则要继续回到更一般的 `HA`。

### 不适用或高成本场景

对完全没有暂停计时需求的模型，`SWA` 会比普通 `TA` 更重；对一般非线性混成系统，它又不够强。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它只多了一点点结构：导数可取 `0`；但这点变化就把表达力推到了 `LHA`。相对 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)，它又是更受限、更接近 timed 工具链的一条混成子枝。相对 [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)，后者增强的是 urgency 语义，这里增强的是 clock dynamics。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata` 主干下的 `Stopwatch Automata` 节点从原来主要靠应用条目支撑，升级成明确的模型本体节点。

### 作为目标形式主义还是中间表示

当需求里存在抢占和恢复，这一形式主义可直接成为目标模型；在更复杂场景中，它也可以作为从 `HA` 往下收缩、从 `TA` 往上扩展的中间层。

### 对需求到模型生成的启发

自然语言里只要出现“暂停后保留已累计时间”“恢复后继续计时”这类句式，就不该硬塞给普通 `TA`，而应优先考虑 `SWA`。

### 现实限制

论文依赖 `τ`-delay 和翻译论证来建立表达力等价；工程上若只关心直接可判定性，还要继续看具体分析算法是否终止。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)
- [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)

### 同类型或同家族工作

- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)
- [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)

### 标准 / 格式 / 工具链工作

- `UPPAAL` stopwatch extension

### 与本研究关系最紧的工作

- 它最适合挂成 `Timed Automata -> Stopwatch Automata` 的经典模型本体代表条目。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Stopwatch Automata (SWA)`
- 论文角色：模型提出
- 核心功能：用可停表的 `0/1` 导数时钟把 `Timed Automata` 扩展到 `LHA` 级表达力。
- 关键特性：stopwatches、`τ`-delay、`TA/SWA/LSWA/LHA` 层级、translation to `UPPAAL` stopwatch analysis。
- 构造方式：继承 `LHA` 七元组语义，并把变量导数限制到 `0/1`。
- 基础设施：有 `UPPAAL` stopwatch-extension 作为分析入口。
- 适用场景：抢占调度、暂停/恢复计时和 `LHA` 到 timed 分析的降阶桥接。
- 需求前提：需求必须显式包含计时冻结与恢复。
- 状态：🟢
