# 扩展有限状态机规格分析方法 / Method of analysing extended finite-state machine specifications

## 基本信息

- 标题：Method of analysing extended finite-state machine specifications
- 中文标题：扩展有限状态机规格分析方法
- 作者：Behcet Sarikaya, Vassilios Koukoulidis, Gregor V. Bochmann
- 发表：Computer Communications, 13(2):83-92, 1990
- DOI：`10.1016/0140-3664(90)90175-G`
- 链接：http://dx.doi.org/10.1016/0140-3664(90)90175-G
- 形式主义：Extended Finite State Machine (EFSM)
- 主类：🧩
- 描述客体：🎛️
- 所属领域：🌐
- 论文角色：方法佐证
- 工具/实现获取方式：原文提到基于 Prolog 的分析程序，可处理 Estelle 规格并输出组合后的 Estelle 规格，但未提供公开下载入口。
- 标准/格式获取方式：论文明确依赖 `Estelle` 与 `SDL` 两类基于 EFSM 的形式描述语言，它们是该模型最直接的标准/格式入口。

## 简报

这篇论文的直接主题是“如何分析 EFSM 规格”，但它对 `EFSM` 本体仍然给出了很实用的模型侧信息：相较普通 `FSM`，`EFSM` 不再只靠离散状态和简单输入/输出迁移，而是允许状态变量、参数、动作、队列通信以及单迁移上的多输出行为。论文还把 `Estelle` 与 `SDL` 作为典型承载，说明了 EFSM 在通信协议规格中的标准化落点。

- 形式主义定位：在 `FSM` 上加入变量、参数、动作和更复杂 I/O 行为的数据增强型离散状态机。
- 构造方式简述：通过状态、状态变量、输入/输出事件、带条件与动作的迁移，以及 `when / from / to / output` 这类文本子句来构造。
- 基础设施与场景简述：原文直接把 `Estelle`、`SDL`、`SDL-GR` 视为 EFSM 生态入口，说明它已具备较明确的 FDT 语言和协议分析背景。

```text
协议/控制需求 + 数据变量 -> EFSM 迁移与动作 -> Estelle / SDL 规格 -> 组合分析 / reachability / 验证
```

## 形式主义定义与核心对象

### 定义对象

论文把 EFSM 放在通信协议与服务规格的语境中讨论。与传统 `FSM` 相比，核心变化是：迁移不再局限于“单输入无输出”或“自发无输入单输出”的简单形式，而是可以携带参数、状态变量更新和多个输出动作。

### 核心抽象

原文没有把 `EFSM` 统一写成一个数学元组；它主要通过 `Estelle/SDL` 的迁移子句、变量和通信语义来展开。为了方便后续分析，这里按论文明确出现的结构做一个**保守整理**：

$$
M = (S, s_0, V, \Sigma_{ext}^{in}, \Sigma_{ext}^{out}, H, T)
$$

上式中的符号逐项解释如下：

1. `S` 是 major state 集合，`s_0` 是初始状态。
2. `V` 是上下文变量、参数和局部数据。
3. `\Sigma_{ext}^{in}`、`\Sigma_{ext}^{out}` 是外部输入/输出交互集合。
4. `H` 是内部交互通道集合，论文明确说明这些通道带排队语义。
5. `T` 是迁移集合。

结合论文对 `Estelle/SDL` 风格迁移的描述，一条迁移可进一步压成：

$$
\tau = (s, \iota, \gamma, \alpha, \omega, s')
$$

其中：

1. `\iota \in \Sigma_{ext}^{in} \cup \{h?m \mid h \in H\} \cup \{\epsilon\}` 表示外部输入、内部消息消费或 spontaneous trigger。
2. `\gamma` 是 `PROVIDED` 子句对应的守卫 / 路径谓词。
3. `\alpha` 是动作块，对变量赋值、调用局部过程并更新上下文。
4. `\omega \in (\Sigma_{ext}^{out} \cup \{h!m \mid h \in H\})^*` 是输出序列，论文特别强调单条迁移可含一个或多个输出。

论文后半段的关键操作是把原始 EFSM 通过 symbolic execution 变成只含单一路径的 normal form transition。其本体可进一步记成：

$$
\tau^{nf} = (s, \iota, \phi, \alpha, \omega, s')
$$

这里的 `\phi` 是沿该路径累计得到的 path predicate。原文对 `IF`、`CASE`、循环展开、过程内联和 `FROM` 多状态展开的讨论，本质上都是在把“多路径迁移”拆成若干 `NFT`。

上述 EFSM 结构公式中的符号逐项解释如下：

1. `\tau` 是一条普通迁移。
2. `s` 与 `s'` 分别是源 major state 和目标 major state。
3. `\iota` 是输入触发，可能是外部输入、内部消息消费或 `\epsilon` 自发触发。
4. `\gamma` 是原始守卫条件。
5. `\alpha` 是动作块，会更新变量或调用局部过程。
6. `\omega` 是输出动作序列。
7. `\tau^{nf}` 是 normal form transition。
8. `\phi` 是经 symbolic execution 展开后累积得到的路径谓词。

### 一个最小例子与通俗解释

一个最小例子是“带重试计数的握手协议”。设状态有 `Idle` 和 `WaitingAck`，并引入变量 `retry`：

1. 在 `Idle` 收到 `send(req)` 时，输出 `req!`，令 `retry := 0`，转到 `WaitingAck`。
2. 在 `WaitingAck` 收到 `timeout` 且满足 `retry < 3` 时，执行 `retry := retry + 1`，再次输出 `req!`。
3. 在 `WaitingAck` 收到 `ack` 时，转回 `Idle`。

通俗解释是：`EFSM` 就是在普通状态机外面再挂一层“变量和动作脚本”。状态负责描述大的控制模式，变量负责记住次数、参数和值，守卫和动作则决定什么时候能走、走的时候顺便改什么数据。

### 运行 / 接受 / 转移语义

若把运行时配置写成：

$$
c = (s, \nu, \kappa)
$$

其中 `\nu : V \to Val` 是变量赋值，`\kappa` 记录内部通道状态，则一条 normal form transition 的触发条件可保守写成：

$$
(s, \nu, \kappa) \xrightarrow{\tau^{nf}} (s', \nu', \kappa')
$$

当且仅当：

1. 当前 major state 为 `s`。
2. 输入 `\iota` 与外部事件或内部消息匹配，或 `\iota = \epsilon`。
3. `\nu \models \phi`。
4. `\nu' = \alpha(\nu)`，并按 `\omega` 更新输出与内部通道。

论文真正有价值的地方，是它给出了内部通信消去后的组合规则。若：

$$
\tau_1 = (s_1, \iota, \phi_1, \alpha_1, \omega_1 \cdot h!m, s_1')
$$

$$
\tau_2 = (s_2, h?x, \phi_2, \alpha_2, \omega_2, s_2')
$$

则根据原文“把 combiner NFT 的输出参数代入 combinee NFT，并把 combinee 的动作替换到 combiner 输出位置”的描述，可把组合迁移保守整理为：

$$
\tau_1 \bowtie_h \tau_2 = ((s_1, s_2), \iota, \phi_1 \land \phi_2[x := m], \alpha_1 ; \alpha_2[x := m], \omega_1 \cdot \omega_2, (s_1', s_2'))
$$

这条公式不是原文逐字给出的元组定义，而是对第 1 步组合规则的符号化压缩；它忠实反映了原文三件事：

1. 内部输出 `h!m` 被对应的内部消费 `h?x` 吸收。
2. 参数值通过替换进入 `PROVIDED` 与动作。
3. 组合后得到的迁移在 product EFSM 上运行，并只保留对外可见的行为。

因此，组合后的 product machine / product EFSM 可记为：

$$
P = M_1 \bowtie M_2,\qquad S_P = S_1 \times S_2
$$

上述运行与组合语义中的符号逐项解释如下：

1. `c = (s,\nu,\kappa)` 是运行时配置。
2. `\nu : V \to Val` 是变量赋值函数。
3. `\kappa` 记录内部通道或消息队列状态。
4. `\nu \models \phi` 表示当前变量赋值满足路径谓词 `\phi`。
5. `\nu' = \alpha(\nu)` 表示动作块 `\alpha` 对变量环境的更新结果。
6. `h!m` 表示在内部通道 `h` 上发送消息 `m`。
7. `h?x` 表示在内部通道 `h` 上接收消息并把值绑定到变量 `x`。
8. `[x := m]` 表示把消息值 `m` 代入变量 `x` 后再计算守卫或动作。
9. `\tau_1 \bowtie_h \tau_2` 表示沿内部通道 `h` 把两条迁移组合成一条 product 迁移。
10. `P = M_1 \bowtie M_2` 是两个 EFSM 的组合产物。
11. `S_P = S_1 \times S_2` 表示组合后状态空间是笛卡尔积。

### 语义边界

它仍然是离散状态机，不带显式时间语义，也没有层次状态或连续动力学。原文的动态分析还带有一个非常关键的适用边界：limited reachability 默认只考察“内部队列至多含一条消息”的近似。

$$
\forall h \in H,\quad |\kappa_h| \le 1
$$

也就是说，这个 product machine 不是任意 FIFO 语义下的完整全局系统，而是一个为了控制状态空间、服务测试与验证而构造的有限近似。论文自己也明确指出：

1. collision cases 不能被这一近似完整覆盖。
2. 任意长度内部队列仍需进一步理论扩展。
3. 因而它比纯 `FSM` 强，但又比真正的异步通信系统全语义更受限。

### 关键性质与判定边界

原文关心的不是语言接受问题，而是“给定一组通信 EFSM 规格，能否在有限近似下发现动态交互错误”。其核心问题可压缩为：

$$
\text{Reach}_{\le 1}(M_1, M_2): \text{ explore } P = M_1 \bowtie M_2 \text{ under } |\kappa_h| \le 1
$$

$$
\text{Deadlock}(c) \equiv Enabled(c) = \emptyset \land c \notin F
$$

$$
\text{UnspecRecv}(h,m) \equiv h!m \land \neg \exists \tau \in T:\ consume_h(\tau,m)
$$

$$
\text{Overflow}(h) \equiv \exists \pi \text{ cycle with unbounded } emit_h(\pi)
$$

这些分析问题中的符号逐项解释如下：

1. `\text{Reach}_{\le 1}(M_1, M_2)` 表示在每条内部通道最多保留一条消息的前提下做可达性探索。
2. `|\kappa_h| \le 1` 是对应的队列近似边界。
3. `\text{Deadlock}(c)` 表示配置 `c` 中没有任何可使能迁移，且它不是终止配置。
4. `Enabled(c)` 是配置 `c` 下当前可触发迁移的集合。
5. `F` 是终止或接受配置集合。
6. `\text{UnspecRecv}(h,m)` 表示消息 `m` 被发到通道 `h` 上，但不存在匹配消费迁移。
7. `consume_h(\tau,m)` 表示迁移 `\tau` 能在通道 `h` 上消费消息 `m`。
8. `\pi` 是某条循环路径。
9. `emit_h(\pi)` 表示在循环 `\pi` 中向通道 `h` 发消息的行为。
10. `unbounded` 表示该循环可导致信道内容无限增长。

其中 `Deadlock`、`UnspecRecv` 和 `Overflow` 都是原文显式讨论的错误类型；`blocking receptions` 与 `tempo-blockings` 则属于同一类“内部通信无法按预期继续推进”的动态异常。论文同时明确给出一个判定边界：

1. limited reachability 适合发现大量 self-consistency 问题，但不是完整异步 FIFO 验证。
2. 当内部队列可能累积多条消息时，分析结论不再由当前 product machine 完整覆盖。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 基础仍然是离散状态机。 |
| 事件 / 触发 | 强支持 | 输入事件和 spontaneous transition 都是原文主干。 |
| 守卫 / 数据 | 强支持 | `Estelle` 明确带状态变量、表达式与语句。 |
| 层次 | 不支持 | 原文不讨论层次状态。 |
| 并发 / 同步 | 部分支持 | 通过多个模块与内部通道组合，不是 Statechart 式并发区。 |
| 时间约束 | 不支持 | 论文未给出显式时钟或时间不变式。 |
| 连续动态 / 随机性 | 不支持 | 纯离散模型。 |
| 可执行 / 可验证性 | 支持 | 论文直接围绕 symbolic execution 与 limited reachability 展开。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| Normal form 转换 | `$M \mapsto M^{nf}$` | 通过 symbolic execution 把复合迁移拆成单路径 `NFT`。 |
| 组合迁移 | `$\tau_1 \bowtie_h \tau_2$` | 消去内部通信并构造 product EFSM。 |
| 有界 reachability | `$\text{Reach}_{\le 1}(M_1, M_2)$` | 在内部队列长度至多为 `1` 的前提下探索组合行为。 |
| 死锁检测 | `$\text{Deadlock}(c) \equiv Enabled(c) = \emptyset \land c \notin F$` | 检测非终态全局卡死。 |
| 未指定接收 | `$\text{UnspecRecv}(h,m) \equiv h!m \land \neg \exists \tau \in T:\ consume_h(\tau,m)$` | 一个模块输出了消息，但另一侧没有匹配消费迁移。 |
| 信道溢出 / 阻塞风险 | `$\exists \pi \text{ cycle},\ emit_h(\pi) \text{ unbounded}$` | 反复输出到内外通道会引发 overflow、blocking 或 tempo-blocking。 |

## 构造方式与承载格式

### 建模入口

原文给出的建模入口有两层：

1. 抽象层：状态、输入/输出、内部通道、状态变量、迁移动作。
2. 语言层：`Estelle` 与 `SDL` 这类基于 EFSM 的 FDT。

### 机器可处理承载方式

论文明确展示了用文本子句表达迁移的方式，例如 `when / from / to / output`。这说明 EFSM 在该语境下不是只有图形画法，而是有稳定文本化入口。`SDL-GR` 又补足了图形化承载。

### 交换与互操作

原文没有 XML/JSON 这类交换标准，但它把 `Estelle` 与 `SDL` 作为事实上的标准载体。这类 FDT 使 EFSM 可以进入协议规格、分析和实现链路，而不是停留在抽象图论对象。

## 配套基础设施

- 建模/编辑工具：原文默认依托 `Estelle` 与 `SDL/SDL-GR` 生态。
- 解析/交换/元模型支持：依赖 FDT 语言本身的语法与编译/处理链，而非单独交换标准。
- 仿真/执行支持：论文强调 formal specification 可作为自动化实现与验证基础。
- 验证/分析支持：核心就是 symbolic execution、limited reachability 和模块组合分析。
- 代码生成/转换支持：论文提到 formal specification 可支撑实现，但未提供通用代码生成框架。
- 标准化或社区生态：`Estelle` 与 `SDL` 是最直接的标准化背景，说明 EFSM 在协议规格领域已有成熟落点。

## 适用场景与需求前提

### 适用场景

适用于需要同时描述“状态切换 + 数据变量 + 输入输出参数 + 模块通信”的协议或反应式软件规格，尤其是通信协议与服务接口。

### 需求前提

1. 需求需要显式状态划分。
2. 需求不仅有事件，还需要状态变量、参数或动作。
3. 系统交互边界清晰，输入输出和内部通信可被抽象出来。

### 不适用或高成本场景

如果核心需求在层次控制、复杂并发状态嵌套、严格实时约束或连续物理过程，单纯 EFSM 不够直接，通常要转向 `Statechart`、`Timed Automata` 或 `Hybrid Automata`。

## 与相邻形式主义的关系

相对 `FSM`，EFSM 的关键增量是变量、参数和动作；相对 `Statechart`，它不靠层次/并发区来扩展表达力；相对 `I/O Automata`，它更偏工程规格语言与数据增强，而不是组合语义优先；相对 `SCXML`，它不是统一 XML 承载。

## 与本研究的关系

### 对 Project 1 的价值

它是“从简单状态图到可落地控制规格”之间非常重要的一层，因为很多真实需求不是时间难，而是数据和动作难。

### 作为目标形式主义还是中间表示

可作为中间表示，也可在特定协议/软件建模场景下作为目标形式主义。

### 对需求到模型生成的启发

如果需求文本里已经稳定出现参数、变量条件、消息载荷和动作序列，就不该强行压回纯 `FSM`；EFSM 是更合适的目标。

### 现实限制

它缺少统一的现代交换标准，且论文本身仍以分析方法为主，不足以单独回答今天全部 EFSM 基础设施问题，后续仍应继续回补更纯粹的定义和标准条目。

## 重要的相关工作

### 奠基或前身工作

- 经典 `FSM` reachability 分析。
- 协议验证中的 product machine 思路。

### 同类型或同家族工作

- `SDL` 与 `Estelle` 这两条 EFSM 规格语言主线。
- 面向协议测试与一致性分析的 EFSM 工作。

### 标准 / 格式 / 工具链工作

- `Estelle` 标准。
- `SDL` / `SDL-GR` 标准与图形语法。

### 与本研究关系最紧的工作

- 需求中带数据与动作效果的状态机建模。
- 协议/交互规格到验证模型的自动转换。

## 文献分类总结

- 主类：🧩
- 描述客体：🎛️
- 所属领域：🌐
- 形式主义：Extended Finite State Machine (EFSM)
- 论文角色：方法佐证
- 核心功能：在 `FSM` 上加入变量、参数和多输出动作，以支撑更真实的协议与交互规格。
- 关键特性：状态变量、参数化 I/O、spontaneous transition、队列通信、symbolic execution。
- 构造方式：状态 + 变量 + 输入输出 + 带条件/动作迁移，可通过 `Estelle/SDL` 文本或图形规格承载。
- 基础设施：`Estelle`、`SDL`、`SDL-GR` 提供标准化 FDT 入口，原文还给出分析程序语境。
- 适用场景：协议规格、数据驱动反应式软件、带参数交互系统。
- 需求前提：需求必须显式包含状态、数据变量和输入输出动作。
- 状态：🟢
