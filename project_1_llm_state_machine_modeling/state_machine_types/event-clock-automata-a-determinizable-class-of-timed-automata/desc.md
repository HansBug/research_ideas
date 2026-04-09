# 事件时钟自动机：一类可确定化的时间自动机 / Event-Clock Automata: A Determinizable Class of Timed Automata

## 基本信息

- 标题：Event-Clock Automata: A Determinizable Class of Timed Automata
- 中文标题：事件时钟自动机：一类可确定化的时间自动机
- 作者：Rajeev Alur, Limor Fix, Thomas A. Henzinger
- 发表：University of California, Berkeley 技术报告 *UCB/ERL M97/28*, 1997；对应早期会议版本发表于 *Computer Aided Verification*, LNCS 818, pp. 1-13, 1994；后续期刊版发表于 *Theoretical Computer Science*, 211(1-2):253-273, 1999
- DOI：技术报告版本无单列 DOI；会议版本 DOI 为 `10.1007/3-540-58179-0_39`，期刊版本 DOI 为 `10.1016/S0304-3975(97)00173-4`
- 链接：https://digicoll.lib.berkeley.edu/nanna/record/139373/files/ERL-97-28.pdf?withWatermark=0&withMetadata=0&registerDownload=1&version=1
- 形式主义：`Event-Clock Automata / Event-Recording & Event-Predicting Automata`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `event-recording / event-predicting` 时钟、clock valuation 和 determinization / complementation 构造。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是有限位置集、符号绑定时钟集和边上的 event-clock constraints。

## 简报

这篇论文把 `Timed Automata` 主干中的“时钟由自动机自己任意 reset”改成“每个输入事件自带固定语义的时钟”。`event-recording clock` 记录某事件上次发生距今多久，`event-predicting clock` 记录该事件下次发生还要多久，而 `event-clock automata` 同时允许这两类时钟。正是由于时钟值不再由控制状态随意改写，而只由输入 timed word 决定，作者证明了这条分支可确定化、对布尔运算封闭，且语言包含可判定；这使它成为 `Timed Automata` 下非常适合挂树的经典“可分析规格子类”节点。

- 形式主义定位：`Timed Automata` 的 determinizable specification 子类，其内部再分出 `Event-Recording Automata`、`Event-Predicting Automata` 与总母类 `Event-Clock Automata`。
- 构造方式简述：把时钟预绑定到字母表中的事件符号，而不是让自动机在边上自由 reset；边只检查这些事件时钟的约束。
- 基础设施与场景简述：原文是纯理论工作，但 determinization、boolean closure、language inclusion 与 timed-transition-system translation 都给得很完整。

```text
timed word / event stream -> event-recording & event-predicting clocks -> event-clock automaton -> determinization / inclusion / complementation
```

## 形式主义定义与核心对象

### 定义对象

输入对象是 timed words，也就是“每个离散事件再带一个时间戳”的事件流。模型想描述的不是连续动力学，而是带显式时序的符号行为。

### 核心抽象

对字母表 `\Sigma`，论文给每个事件 `a \in \Sigma` 定义两类时钟：

$$
C_{\Sigma} = \{x_a \mid a \in \Sigma\} \cup \{y_a \mid a \in \Sigma\}
$$

上式中的符号逐项解释如下：

1. `x_a` 是 `a` 的 `event-recording clock`，表示“自上一次 `a` 发生以来经过了多久”。
2. `y_a` 是 `a` 的 `event-predicting clock`，表示“距离下一次 `a` 发生还要多久”。
3. 某事件从未出现过，或未来不再出现时，对应时钟值视为 `\bot`，其比较规则由论文专门约定。

在此基础上，一个 `Event-Clock Automaton` 可保守写成：

$$
A = (\Sigma, L, L_0, L_F, E)
$$

其中：

1. `L` 是有限位置集。
2. `L_0 \subseteq L` 是起始位置集。
3. `L_F \subseteq L` 是接受位置集。
4. `E \subseteq L \times L \times \Sigma \times \Phi(C_{\Sigma})` 是边集；每条边都带输入符号和 event-clock 约束。

### 一个最小例子与通俗解释

最小例子可以取“每个 `a` 之后 3 秒内必须出现 `b`”。在读到 `a` 之后，后续所有位置都检查 `y_b \le 3`，因为 `y_b` 直接告诉我们“离下一次 `b` 还有多久”。如果要表达“任意两个 `a` 至少间隔 5 秒”，则在读到第二个 `a` 时检查 `x_a \ge 5` 即可。

通俗地说，`Event-Clock Automata` 像是“把和事件相关的过去/未来计时器直接焊死在字母表上”的时间自动机。普通 `Timed Automata` 要自己设计何时 reset 哪个 clock；这里 clock 的更新完全跟着输入事件走，因此规格更像在“读 timed word 时观察事件时距”，而不是在“操纵一堆可编程时钟”。

### 运行 / 接受 / 转移语义

对 timed word `$w = (a_0,t_0)(a_1,t_1)\cdots(a_n,t_n)$`，自动机从左到右扫描；若当前位置 clock valuation `\gamma_i` 满足对应边约束 `\varphi_i`，则可沿边前进。可接受计算可保守写成：

$$
\ell_0 \xrightarrow{a_0,\varphi_0} \ell_1 \xrightarrow{a_1,\varphi_1} \cdots \xrightarrow{a_n,\varphi_n} \ell_{n+1}
$$

并要求：

$$
\ell_0 \in L_0,\quad \ell_{n+1} \in L_F,\quad \gamma_i \models \varphi_i \text{ for all } i
$$

这里的关键点不是状态更新，而是 `\gamma_i` 完全由 timed word 决定，而不由自动机边上的 reset 动作决定。

### 语义边界

若只允许 `x_a`，得到 `Event-Recording Automata (ERA)`；若只允许 `y_a`，得到 `Event-Predicting Automata (EPA)`；允许两者并存，则得到总类 `ECA`。论文还用例子说明 `ERA` 与 `EPA` 互不包含，因此真正稳定的树节点应是它们共同上层的 `Event-Clock Automata`。

### 关键性质与判定边界

论文最关键的正结论是：

$$
\text{Every ECA can be determinized}
$$

并且：

$$
\text{ECA is closed under all boolean operations}
$$

因此：

$$
\text{Language inclusion for ECA is decidable and PSPACE-complete}
$$

论文还证明 `ERA` 足以建模 finite timed transition systems，因此它不是“太弱的教学玩具”，而是一个可分析而又有实际表达力的 timed-specification 家族。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍有有限位置集 `L` 作为离散控制骨架。 |
| 事件 / 触发 | 强支持 | 每条边都由输入事件触发，且时钟语义与事件直接绑定。 |
| 守卫 / 数据 | 支持时钟守卫、不支持一般数据 | 约束对象是 `x_a / y_a` 这类事件时钟。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 不支持 | 论文核心是 timed-word 识别与规格，而非并发组合。 |
| 时间约束 | 强支持 | 过去/未来时间差都是一等对象。 |
| 连续动态 / 随机性 | 不支持 | 时间只通过时钟值进入，不含连续流或概率。 |
| 可执行 / 可验证性 | 强理论支持 | determinization、complementation、inclusion 都清晰可做。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 时钟集 | `$C_{\Sigma}=\{x_a\}\cup\{y_a\}$` | 过去/未来事件时距的固定观测接口。 |
| 模型骨架 | `$A=(\Sigma,L,L_0,L_F,E)$` | `Event-Clock Automata` 的基本结构。 |
| 语义关键点 | `$\gamma_i$ solely determined by the input word` | 时钟值不受 automaton 自主 reset 控制。 |
| 可确定化 | `$\mathrm{ECA}_{nd}=\mathrm{ECA}_{det}$` | 这条分支可用子集构造 determinize。 |
| 判定边界 | `$\text{Inclusion}_{ECA}$ is PSPACE-complete` | 相比一般 `Timed Automata`，规格分析边界大幅改善。 |

## 构造方式与承载格式

### 建模入口

1. 先确定字母表里的“关键事件”是什么。
2. 再判断需求更依赖“上次发生距今多久”还是“下次发生还要多久”。
3. 由此选择 `ERA`、`EPA` 或完整 `ECA`。
4. 最后只在边上写 clock constraints，不额外设计 reset 规则。

### 机器可处理承载方式

机器可处理承载方式是位置图、事件字母表和 event-clock constraints，而不是 XML / DSL 文件。

### 交换与互操作

它和 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的一般 `Timed Automata` 母线直接相连，也和 [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)、[the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md) 这类“如何表达 urgency / deadlines”的 timed-specification 分支互补：后两者增强表达方式，`ECA` 则强调可确定化与布尔闭包。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 event-clock valuation、constraint satisfaction 和 determinization construction。
- 仿真/执行支持：可按 timed word 直接扫描执行。
- 验证/分析支持：determinization、boolean closure、emptiness、language inclusion、translation from timed transition systems。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 `Timed Automata` 家族中经典的“可分析规格子类”文献。

## 适用场景与需求前提

### 适用场景

适合实时协议规格、时距约束、响应窗口、请求间最小间隔、timed-word 语言包含和 deterministic timed specification。

### 需求前提

1. 需求对象应能自然写成 timed event stream。
2. 时间约束最好围绕“某事件距过去/未来另一事件的时间差”表达。
3. 若希望做布尔组合、包含或补集分析，`ECA` 比一般 `TA` 更合适。

### 不适用或高成本场景

若需求需要自由 reset 的局部计时策略、复杂并发网络或连续变量流，普通 `Timed Automata` / `Hybrid Automata` 更自然。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`ECA` 最大区别是“时钟语义固定绑定到事件，而非由边任意重置”；相对 [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md) 的 `deadline` / `timed action` 线，`ECA` 更像语言规格与判定性分支，而不是组合代数分支；相对 [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md) 的 `Stopwatch Automata`，`ECA` 牺牲了表达力，换来可确定化与布尔封闭。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata` 主干下再分出一个非常稳定的“可确定化规格分支”，这比继续补 timed 应用条目更直接服务于演化树扩展。

### 作为目标形式主义还是中间表示

更适合作为理论上的目标规格语言或中间表示，而不是最终控制器执行模型。

### 对需求到模型生成的启发

如果自然语言需求大量出现“某事件之后/之前多少时间内必须发生另一个事件”，LLM 其实更容易先生成 `event-recording / event-predicting` 约束，再决定是否要降到更工程化的 `TA`。

### 现实限制

它主要针对 timed-word 规格；对复杂控制结构、资源变量和并发组合支持不如一般 `TA` 或 `HA`。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [the-compositional-specification-of-timed-systems-a-tutorial/desc.md](../the-compositional-specification-of-timed-systems-a-tutorial/desc.md)
- [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)
- [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Timed Automata -> Event-Clock Automata`，并进一步拆出 `Event-Recording` 与 `Event-Predicting` 子枝。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Event-Clock Automata / Event-Recording & Event-Predicting Automata`
- 论文角色：模型提出
- 核心功能：把与事件绑定的过去/未来时距直接做成时钟，从而得到可确定化、布尔封闭的 timed-specification 自动机。
- 关键特性：event-recording clocks、event-predicting clocks、determinization、complementation、PSPACE inclusion。
- 构造方式：`A=(\Sigma,L,L_0,L_F,E)` + event-clock constraints。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：timed-word 规格、实时协议约束、响应窗口和包含关系分析。
- 需求前提：需求能自然落到“事件之间的时间差”而不是自由 reset 的局部计时策略。
- 状态：🟢
