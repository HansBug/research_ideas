# 带输入决定守卫的连续时间自动机 / On Continuous Timed Automata with Input-Determined Guards

## 基本信息

- 标题：On Continuous Timed Automata with Input-Determined Guards
- 中文标题：带输入决定守卫的连续时间自动机
- 作者：Fabrice Chevalier、Deepak D'Souza、Pavithra Prabhakar
- 发表：*FSTTCS 2006: Foundations of Software Technology and Theoretical Computer Science*, pp. 369-380, 2006
- DOI：`10.1007/11944836_34`
- 链接：https://lsv.ens-paris-saclay.fr/Publis/PAPERS/PDF/CDP-fsttcs06.pdf
- 形式主义：`Continuous Input-Determined Automata (CIDA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CIDA` 元组、symbolic alphabet、state invariant、`TMSO_c` / `TLTL_c` 翻译链。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 input-determined operators、continuous symbolic words 和 `CIDA` 语义。

## 简报

这篇论文不是再给 `Timed Automata` 加一类自由 reset 的时钟，而是把“时间谓词完全由输入 timed word 决定”的 `input-determined` 思路推进到**连续语义**。与 pointwise 版本只在事件点检查守卫不同，`CIDA` 允许在事件之间的任意连续时间点上写约束，因此形成了 `Input-Determined Timed Automata` 下面一条更强的 continuous branch。

- 形式主义定位：`Input-Determined Timed Automata` 的连续语义扩展。
- 构造方式简述：围绕一组 input-determined operators 建 symbolic alphabet，再用状态 invariant 和转移关系定义接受。
- 基础设施与场景简述：核心基础设施是 determinization、boolean closure、`TMSO_c` 逻辑刻画和 `TLTL_c` 到 `TFO_c` 的表达等价。

```text
input-determined operators -> continuous symbolic words -> CIDA -> TMSO_c / TLTL_c -> continuous timed specifications
```

## 形式主义定义与核心对象

### 定义对象

原文关心的是那些“时间约束值由输入 timed word 本身决定”的实时规格。典型例子包括：

1. 上一次事件 `a` 发生距今多久。
2. 下一次某事件还要多久才出现。
3. 某个将来区间里是否会发生某事件。

和普通 `TA` 不同，这些值不由 automaton 自己 reset，而是由输入 timed word 决定。

### 核心抽象

`CIDA` 在一组 input-determined operators `Op` 上定义为：

$$
A = (Q,s,\delta,F,inv)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `s\in Q` 是起始状态。
3. `\delta \subseteq Q\times 1\times Q` 是转移关系，这里的 `1` 是由 `Op` 诱导出的 symbolic alphabet。
4. `F\subseteq Q` 是接受状态集。
5. `inv:Q\to 2` 给每个状态分配连续时间上的 invariant 标注，这里的 `2` 表示另一部分 symbolic alphabet 成分。

原文随后定义 symbolic language、function language 和 timed language：

$$
F(A)=timing(L_{sym}(A)),\qquad L(A)=tw(F(A))
$$

上式中的符号逐项解释如下：

1. `L_{sym}(A)` 是 automaton 接受的 symbolic language。
2. `timing(\cdot)` 把 symbolic word 解释成连续时间上的 finitely varying function。
3. `tw(\cdot)` 再把这些 function 映回 timed words。

### 一个最小例子与通俗解释

可以用“未来 `3` 个时间单位内必须会发生一次 `a`”来理解 `CIDA`。在 continuous semantics 下，系统不只在离散事件点上检查这个约束，而是允许在事件之间的任意时刻都检查“距下一次 `a` 还有多久”。于是：

1. 若某段静默区间中，未来 `a` 的距离一直不超过 `3`，就可留在当前状态。
2. 一旦某个连续时刻开始，这个距离超过了允许范围，就会违反 invariant。

通俗地说，`CIDA` 像是“把时间逻辑观察点从离散事件点扩展到整条时间轴”的 `IDA`。它不是只看“事件发生时”，而是看“事件之间连续时间里，这些 input-determined 谓词是否一直成立”。

### 运行 / 接受 / 转移语义

对符号串 `\sigma=\sigma_0\sigma_1\cdots\sigma_{2n}`，原文把一次 run 写成映射：

$$
\rho:N\to Q
$$

并要求：

$$
\rho(0)=s,\qquad (\rho(i),\sigma_{2i},\rho(i+1))\in\delta
$$

同时对每个中间位置还要求：

$$
inv(\rho(i))=\sigma_{2i-1}
$$

接受条件是：

$$
\rho(n+1)\in F
$$

这套定义的核心点是：invariant 不再只是 location 上的附属说明，而是 continuous semantics 的第一等约束接口。

### 语义边界

相对已有的 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)，这里新增的是：

1. 守卫可在连续时间点上解释。
2. automata 允许 epsilon-transition 和 state invariant。
3. 逻辑刻画从 pointwise 推进到 continuous `TMSO_c / TLTL_c`。

### 关键性质与判定边界

论文的核心正结果是：

$$
\text{CIDA is closed under union, intersection and complementation}
$$

并且它有完整的逻辑刻画：

$$
L \subseteq T\Sigma^* \text{ is accepted by a CIDA } \iff L \text{ is definable in } TMSO_c(\Sigma,Op)
$$

进一步，连续时间版时序逻辑也与一阶片段对齐：

$$
TLTL_c(\Sigma,Op) \equiv TFO_c(\Sigma,Op)
$$

论文还指出，这一 general framework 直接推出 continuous semantics 下 `MTL` 的 expressive completeness 结果。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态骨架。 |
| 事件 / 触发 | 强支持 | 输入仍是 timed events，但约束可在事件之间连续解释。 |
| 守卫 / 数据 | 强支持守卫 | 守卫来自 input-determined operators，而不是自由 reset 的 clocks。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 不支持 | 论文重点是单体 timed-language family。 |
| 时间约束 | 强支持 | continuous semantics 是该条目的核心新增点。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | determinization、boolean closure、MSO / temporal-logic characterization 都完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,s,\delta,F,inv)$` | continuous input-determined automaton 的标准骨架。 |
| 语言接口 | `$F(A)=timing(L_{sym}(A)),\ L(A)=tw(F(A))$` | 把 symbolic semantics 连接到 timed words。 |
| 布尔闭包 | `$\cup,\ \cap,\ \complement$` all preserved | 说明 continuous branch 仍保有 determinizable 规格子类特征。 |
| MSO 刻画 | `$CIDA \iff TMSO_c$` | 把 automata 和 continuous timed logic 直接接通。 |
| 时序逻辑刻画 | `$TLTL_c \equiv TFO_c$` | 给 continuous timed temporal logic 一个一阶精确落点。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. 需要哪些 input-determined operators。
2. 这些 operator 是只在事件点看，还是必须在连续时间里看。
3. 哪些约束应该写成 state invariant，哪些写成离散转移条件。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. symbolic alphabet。
2. `CIDA` 元组。
3. `TMSO_c / TLTL_c` 公式。

### 交换与互操作

它和 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md) 的 pointwise `IDA` 母线、[event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md) 的 event-clock 早期特例，以及 [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md) 的 counter-free fragment 都直接相关。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 symbolic alphabets、proper alphabets 与逻辑翻译链。
- 仿真/执行支持：可按 symbolic word / finitely varying function 解释。
- 验证/分析支持：determinization、boolean closure、`TMSO_c` characterization、`TLTL_c` expressive completeness。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 input-determined timed specification family 的连续语义主线。

## 适用场景与需求前提

### 适用场景

适合那些必须在事件之间连续时间上陈述约束的 timed-word specification，例如“从某个时刻开始，未来若干时间单位内必须发生某事件”。

### 需求前提

1. 时间约束应主要来自输入自身可观测的时间距离。
2. 需求需要 continuous semantics，而不是只在 action-points 上检查。
3. 目标偏规格与逻辑刻画，而不是工程执行器。

### 不适用或高成本场景

若需求依赖自由 reset 的本地计时程序，普通 `TA` 更自然；若只需要 pointwise 语义，原始 `IDA` 已足够。

## 与相邻形式主义的关系

相对 [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)，它把 `input-determined` family 从离散事件点推进到连续时间语义；相对 [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)，它是更一般的母类；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，event-clock 只是其中一组具体 operator 的特例。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Input-Determined Timed Automata` 主线继续细化成 continuous branch，有助于把演化树从“可确定化 timed specification”进一步推进到“pointwise / continuous 两种语义分裂”。

### 作为目标形式主义还是中间表示

更适合作为 high-level timed specification 或 logic-to-automata 中间表示，而不是工程执行模型。

### 对需求到模型生成的启发

当自然语言需求说的是“在某段连续时间内一直成立”而不是“在事件点上成立”，LLM 更适合先生成 `CIDA` 一类 continuous specification，再考虑是否降到更工程化的自动机。

### 现实限制

它的优势主要在逻辑表达与可判定性；对工业建模者来说，symbolic alphabet 和 operator 参数化仍比较抽象。

## 重要的相关工作

### 奠基或前身工作

- [on-timed-automata-with-input-determined-guards/desc.md](../on-timed-automata-with-input-determined-guards/desc.md)

### 同类型或同家族工作

- [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)
- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具；最重要的基础设施是 `proper alphabet`、`TMSO_c` 与 `TLTL_c`。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Timed Automata -> Input-Determined Timed Automata -> Continuous Input-Determined Automata`。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
