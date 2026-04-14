# 稠密时间下推自动机 / Dense-Timed Pushdown Automata

## 基本信息

- 标题：Dense-Timed Pushdown Automata
- 中文标题：稠密时间下推自动机
- 作者：Parosh Aziz Abdulla、Mohamed Faouzi Atig、Jari Stenman
- 发表：*2012 27th Annual IEEE Symposium on Logic in Computer Science*, pp. 35-44, 2012
- DOI：`10.1109/LICS.2012.15`
- 链接：https://user.it.uu.se/~parosha/publications/papers/lics12.pdf
- 形式主义：`Dense-Timed Pushdown Automata (TPDA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `TPDA` tuple、配置语义和基于 region + shadow items 的符号编码。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是全局 clocks、带 age 的栈符号、timed/discrete transitions 以及 symbolic pushdown encoding。

## 简报

这篇论文把 timed-pushdown family 明确推进到“**每个栈符号自己也带一个实值年龄**”的版本。也就是说，不再只是全局 clocks 受时间流逝影响，栈里每个 frame 的 age 也会跟着同步增长。正因为这会带来“无界个数的实值时钟”，论文的关键贡献是构造一种扩展 region 编码，用有限方式记录 top region 与深层栈帧之间的时间关系，并由此证明 reachability `EXPTIME`-complete。

- 形式主义定位：`Pushdown Timed Automata` 母节点下的 dense-time、stack-age 显式化子类。
- 构造方式简述：自动机保留一组全局 clocks，同时每个入栈符号都附带一个实值 age；时间流逝时两者同步增长。
- 基础设施与场景简述：核心基础设施是带 shadow items 的 region encoding，以及从 `TPDA` 到 untimed `PDA` 的精确 reachability reduction。

```text
global clocks + aged stack symbols -> dense-timed pushdown behavior -> region with shadow items -> untimed PDA reduction -> EXPTIME reachability
```

## 形式主义定义与核心对象

### 定义对象

论文明确把对象定位为“real-time recursive systems”。它想表达的不是一般 timed language，而是带递归栈、且每个未返回调用都带自己年龄信息的系统配置。

### 核心抽象

原文先固定一组时钟 `X`，再定义 `TPDA`。按原文写法，其核心 tuple 是：

$$
T = \langle S, s_{init}, \Gamma, \Delta \rangle
$$

其中背景里额外固定了 clocks 集合 `X`。上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `s_{init}\in S` 是初始状态。
3. `\Gamma` 是栈字母表。
4. `\Delta` 是有限转移集。
5. `X` 是全局 clocks 集合。

配置写成：

$$
\langle s, X, w \rangle
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `X` 是当前全局时钟赋值。
3. `w\in(\Gamma\times\mathbb R_{\ge 0})^*` 是栈内容，其中每个符号都带一个年龄值。

### 一个最小例子与通俗解释

最小直觉例子是“调用某个子过程后，必须在栈顶 frame 年龄落在 `[2,5]` 时返回”：

1. 执行 `push(a,[0,0])`，把符号 `a` 以年龄 `0` 压栈。
2. 时间流逝时，`a` 的年龄和全局 clocks 一起增加。
3. 返回时执行 `pop(a,[2,5])`，只有当栈顶是 `a` 且其年龄在 `[2,5]` 内时才允许弹栈。

通俗地说，`Dense TPDA` 像“每个栈帧都自带一个小计时器”的 timed pushdown automaton。这样它就能表达“某个调用已经挂了多久”这类普通全局时钟难以局部保存的信息。

### 运行 / 接受 / 转移语义

论文先定义 timed transition。对任意 `v\in\mathbb R_{\ge 0}`：

$$
\langle s,X,w\rangle \xrightarrow{v}_{Time} \langle s,X+v,w+v\rangle
$$

这里 `X+v` 表示每个全局 clock 都加 `v`，`w+v` 表示每个栈符号的 age 也都加 `v`。

离散转移则由五类操作构成：

$$
op \in \{nop,\ x\in I?,\ x\leftarrow I,\ pop(a,I),\ push(a,I)\}
$$

例如：

$$
op = pop(a,I)
$$

意味着只有当栈顶符号是 `a` 且其 age 落在区间 `I` 内时，才能把它弹出。

### 语义边界

相对 [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md)，这里更进一步：栈中每个符号自身都携带时钟式 age，而不仅仅是全局时钟加栈操作；相对 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，它更像栈机器而不是 component / box 调用。

### 关键性质与判定边界

论文最关键的结论是：

$$
\text{Reachability(TPDA) is EXPTIME-complete}
$$

证明思路不是普通 timed-automata region，而是构造一种带 shadow items 的 region encoding，使得无界深栈中的时间依赖还能被有限地传递到顶层符号推理里。直观上可压成：

$$
\text{TPDA reachability } \leq \text{ untimed PDA reachability}
$$

但这个 reduction 依赖的是专门为“栈符号也带时钟”设计的扩展 region，而不是直接复用普通 `TA` 区域图。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态 `S` 作为控制骨架。 |
| 事件 / 触发 | 强支持 | 有 timed transition 和多类 discrete stack operation。 |
| 守卫 / 数据 | 强支持 | 可检查全局 clock 区间，也可检查栈顶 age 区间。 |
| 层次 | 强支持 | 无界栈显式记录递归上下文。 |
| 并发 / 同步 | 不支持 | 原始模型面向单栈递归系统。 |
| 时间约束 | 强支持 | 全局 clocks 和 stack ages 同时存在。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | reachability 可判且 `EXPTIME`-complete。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$T=\langle S,s_{init},\Gamma,\Delta\rangle$` with fixed `$X$` | 原文的 `TPDA` 基本骨架。 |
| 配置 | `$\langle s,X,w\rangle$` | 同时保存控制状态、全局时钟和带年龄的栈。 |
| timed transition | `$\langle s,X,w\rangle \xrightarrow{v}_{Time} \langle s,X+v,w+v\rangle$` | 时间流逝会同步推进全局时钟和所有栈帧年龄。 |
| 离散操作 | `$nop,\ x\in I?,\ x\leftarrow I,\ pop(a,I),\ push(a,I)$` | 全局 clocks 与 stack ages 都可进入 guard / update。 |
| 复杂度结论 | `$\text{Reachability(TPDA)}$ is `EXPTIME`-complete` | 给 timed-pushdown with stack-age family 一个稳定边界。 |

## 构造方式与承载格式

### 建模入口

建模时通常要决定：

1. 哪些时间信息应该记在全局 clocks 中。
2. 哪些信息必须绑定到具体栈帧的年龄上。
3. push / pop 上应检查哪些年龄区间。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `TPDA` tuple。
2. timed / discrete configuration semantics。
3. region + shadow items 的符号编码。

### 交换与互操作

它和 [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md) 的 timed-pushdown 母节点、[recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md) 的 recursive timed branch，以及本轮新增的 [event-clock-visibly-pushdown-automata/desc.md](../event-clock-visibly-pushdown-automata/desc.md) 都构成 `Timed Automata` 下的 stack-oriented family。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是扩展 region、shadow items 和从 `TPDA` 到 `PDA` 的 reduction。
- 仿真/执行支持：语义直接可执行，但需要维护所有 stack ages。
- 验证/分析支持：reachability、region-style symbolic encoding、复杂度分类。
- 代码生成/转换支持：支持转成 untimed `PDA` 分析，但不讨论工程代码生成。
- 标准化或社区生态：属于 timed pushdown / recursive real-time verification 的经典理论模型。

## 适用场景与需求前提

### 适用场景

适合那些不仅要记录递归调用层次，还要记录“每个未返回调用已经持续多久”的实时递归系统。

### 需求前提

1. 系统同时需要无界栈和 dense-time。
2. 仅靠全局时钟不足以表达每层调用自己的时间年龄。
3. 关心的是 reachability / safety 一类理论分析，而不是工程执行格式。

### 不适用或高成本场景

若只需要全局 clocks 而不需要栈帧年龄，`PTA` 更轻；若只需要组件级调用，不需显式 age-per-stack-symbol，可考虑 `RTA`。

## 与相邻形式主义的关系

相对 [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md)，`Dense TPDA` 更强调 stack symbols 的 age 语义与 `EXPTIME` reachability；相对 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，它是“显式栈 + 显式 age”路线，而不是“组件调用 + clock passing”路线；相对 [event-clock-visibly-pushdown-automata/desc.md](../event-clock-visibly-pushdown-automata/desc.md)，它表达力更强，但不再保 visible / determinizable 特征。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Pushdown Timed Automata` 母节点继续细化成“每个栈帧自带年龄”的 dense-time 子枝，使 timed-pushdown family 在演化树里更完整。

### 作为目标形式主义还是中间表示

更适合作为理论目标形式主义或强表达力中间抽象，不适合作为普通工程建模的首选交付语言。

### 对需求到模型生成的启发

当需求文本显式谈到“某个调用被压栈后在多长时间内必须完成”，而这个时间不能仅用全局时钟近似时，LLM 生成 `Dense TPDA` 比普通 `PTA` 更贴近语义。

### 现实限制

虽然 reachability 可判，但模型和符号编码都明显比普通 `TA` / `PTA` 更重，工程落地门槛高。

## 重要的相关工作

### 奠基或前身工作

- [pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md](../pushdown-timed-automata-a-binary-reachability-characterization-and-safety-verification/desc.md)
- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)
- [event-clock-visibly-pushdown-automata/desc.md](../event-clock-visibly-pushdown-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的基础设施是 region with shadow items。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Timed Automata -> Pushdown Timed Automata -> Dense-Timed Pushdown Automata`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
