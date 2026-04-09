# iState：状态图验证方法 / Statechart Verification with iState

## 基本信息

- 标题：Statechart Verification with iState
- 中文标题：iState：状态图验证方法
- 作者：Dai Tri Man Le
- 发表：*arXiv preprint arXiv:0909.1361*，2009（`FM 2006` 同名扩展长文）
- DOI：原文未提供
- 链接：https://arxiv.org/abs/0909.1361
- 形式主义：`Statecharts / iState / state invariants / verification tuples`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：状态不变式验证路线 / `iState` 定理证明桥接
- 工具/实现获取方式：论文明确说明 `iState` 可把 statecharts 翻译到 `AMN`、`Pascal` 与 `Java`，并在其中加入验证能力；但原文没有给出稳定公开下载包，只保留工具描述与论文长文。
- 标准/格式获取方式：原文给出了 statechart 到 guarded-command AST、`EventCode` 与 `VTuple` 的形式化映射，但没有定义独立公共交换格式。

## 简报

这篇论文的重点，不是再造一个新的状态图语义，而是给 `statecharts` 增加一条“把状态不变式挂在状态上，再自动生成局部证明义务”的验证路线。`iState` 不走全局时序逻辑模型检查的主路，而是把层次状态、并发状态和广播事件翻译成 guarded-command 风格的 AST，再把它们压成适合 theorem prover 处理的 verification tuples。

- 形式主义定位：围绕 `statecharts` 的局部安全验证方法与工具桥接，而不是新的状态机本体。
- 构造方式简述：`statechart + state invariants -> EventCode AST -> verification tuples -> Hoare-style obligations -> Simplify`。
- 基础设施与场景简述：依托 `iState`、guarded commands、`AMN` 与 `Simplify`，服务层次/并发 statechart 的安全性质交叉校验。

```text
statechart + 需求不变式 -> 累积不变式 ai(s) -> EventCode/VTuple -> 本地 Hoare 风格验证条件 -> theorem prover
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `statechart` 状态结构与事件；
2. 挂在状态上的 invariants；
3. 由层次关系累积得到的 accumulated invariant；
4. `EventCode` 抽象语法树；
5. `VTuple` 验证元组与对应的本地 Hoare 风格证明义务。

### 核心抽象

原文先定义状态不变式与累积不变式。对子状态组合部分，可压成：

$$
ci(s) = si(s) \land \dot{\bigvee} ci[\mathrm{children}[\{s\}]] \text{ if } s \in XOR,\quad ci(s) = si(s) \land \bigwedge ci[\mathrm{children}[\{s\}]] \text{ if } s \in AND,\quad ci(s) = si(s) \text{ if } s \in Basic
$$

上式中的符号逐项解释如下：

1. `si(s)` 是设计者直接挂在状态 `s` 上的局部不变式。
2. `ci(s)` 是把子状态信息组合后的 child invariant。
3. `XOR`、`AND`、`Basic` 分别表示异或复合态、并发复合态与基本状态。
4. `\dot{\bigvee}` 表示异或式组合，`\bigwedge` 表示并发态要求所有子状态同时满足。
5. `\mathrm{children}[\{s\}]` 是状态 `s` 的子状态集合。

对应的累积不变式写成：

$$
ai(s) = \bigwedge si[\mathrm{parent}^{+}[\{s\}]] \land ci(s)
$$

上式中的符号逐项解释如下：

1. `ai(s)` 是状态 `s` 的 accumulated invariant。
2. `\mathrm{parent}^{+}[\{s\}]` 是 `s` 的所有祖先状态集合。
3. 该式表示“处在某个状态时，也必须满足所有祖先态的状态约束”。

对每条迁移 `E[guard]/action: S -> T`，原文生成如下验证条件：

$$
\{ ai(S) \land guard \}\ action\ \{ ai(T) \}
$$

上式中的符号逐项解释如下：

1. `ai(S)` 是源状态的累积不变式。
2. `guard` 是迁移守卫。
3. `action` 是迁移动作，允许读写全局变量、做 state tests 以及广播事件。
4. `ai(T)` 是目标状态的累积不变式。
5. 这就是 `iState` 生成 local proof obligation 的核心。

为统一处理中间结果，论文定义验证元组：

$$
VTuple = \mathcal{P}(State) \times Expression \times Statement \times \mathcal{P}(State)
$$

上式中的符号逐项解释如下：

1. 第一个分量是源状态集合。
2. 第二个分量是守卫表达式。
3. 第三个分量是动作语句。
4. 第四个分量是目标状态集合。
5. 它对应 paper 中 `(s, g, a, t)` 这一类局部验证对象。

论文还给出了 statechart 数据结构：

$$
State = Basic(id) \mid And(id, seq(State)) \mid Xor(id, seq(State), init, Transition)
$$

上式中的符号逐项解释如下：

1. `Basic(id)` 表示基本状态。
2. `And(id, seq(State))` 表示并发复合态。
3. `Xor(id, seq(State), init, Transition)` 表示异或复合态，携带初始子状态和迁移关系。
4. 这说明 `iState` 的验证算法并不是只看平面图，而是显式编码了层次结构。

### 一个最小例子与通俗解释

论文开头给了一个小例子：

1. 根层有 `R` 与 `U`。
2. `R` 下有 `S`，`U` 下并发地包含 `A/M` 与 `B/N`。
3. 事件 `E` 在 `S` 中、守卫 `x != 5` 时触发。
4. 动作执行 `x := x + 10`，并把根状态切到 `U`、并发子状态切到 `M` 与 `N`。

对应的局部不变式例如：

$$
si(S) = (r = S \land x \le 100), \quad si(U) = (root = U \land x > 6)
$$

通俗地说，这条路线是在问：“如果我声称 `S` 状态时 `x` 一定不超过 `100`，而迁移 `E` 会把系统带到 `U/M/N`，那这条迁移是否真能把系统带到一个满足新状态不变式的配置里？” 它把这种问题拆成很多小证明义务，而不是直接对整张状态图做一个巨大的全局时序证明。

### 运行 / 接受 / 转移语义

原文的 `EventCode` 抽象语法树可保守整理为：

$$
EventCode = Identifier \mapsto Statement
$$

其中 `Statement` 递归包含 `StateAssign`、`Assignment`、`Bcast`、`Guard`、`Par`、`Seq` 与 `Skip`。其并行组合函数可压成：

$$
\mathrm{parProd}([s_1,\ldots,s_n]) = \{ \mathrm{concat}_1([t_1,\ldots,t_n]) \mid (t_1,\ldots,t_n) \in s_1 \times \cdots \times s_n \}
$$

上式中的符号逐项解释如下：

1. `s_i` 是若干验证元组集合。
2. `\times` 是笛卡尔积。
3. `\mathrm{concat}_1` 把多个局部验证元组合并成一个并行验证对象。
4. 这一步用来处理并发子状态在同一事件上的联合迁移。

### 语义边界

这条路线的边界也很明确：

1. 它主要验证 safety-style invariants，不是完整 `CTL/LTL` 模型检查。
2. 证明能力依赖 `Simplify` 的一阶逻辑和线性算术能力。
3. 论文明确把 timed transitions 列为后续工作，说明时间语义尚未纳入这条验证线。
4. 方法建立在 event-centric semantics 之上，和传统 state-centric statechart 语义不同。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 局部不变式组合 | `$ci(s)=\cdots$` | 说明 `XOR/AND/Basic` 状态如何组合局部不变式。 |
| 累积不变式 | `$ai(s)=\bigwedge si[\mathrm{parent}^{+}[\{s\}]] \land ci(s)$` | 体现层次状态必须继承祖先约束。 |
| 单迁移验证条件 | `$\{ ai(S) \land guard \}\ action\ \{ ai(T) \}$` | `iState` 生成的核心证明义务。 |
| 验证元组骨架 | `$VTuple = \mathcal{P}(State) \times Expression \times Statement \times \mathcal{P}(State)$` | 统一承载本地验证对象。 |
| statechart 数据结构 | `$State = Basic(id) \mid And(id, seq(State)) \mid Xor(id, seq(State), init, Transition)$` | 说明算法直接处理层次/并发状态结构。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 面向层次、并发 statecharts。 |
| 事件 / 触发 | 很强 | 采用 event-centric semantics，事件是验证主入口。 |
| 守卫 / 数据 | 很强 | 守卫、全局变量与状态测试直接进入验证条件。 |
| 层次 | 很强 | `ai(s)` 显式累积祖先态约束。 |
| 并发 / 同步 | 很强 | `AND` 态与 `parProd` 专门处理并发组合。 |
| 时间约束 | 弱支持 | 论文把 timed transitions 列为 future work。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围内。 |
| 可执行 / 可验证性 | 很强 | 已打通 statechart -> `EventCode` -> theorem prover 的路线。 |

### 形式化问题与性质

1. 它把“状态的意图”编码成 invariants，从而补足裸 statechart 只有 well-formedness、缺少语义交叉校验的问题。
2. 它通过 verification tuples 把大验证问题拆成小而局部的证明义务，更适合自动定理证明器处理。
3. 它的 event-centric 视角尤其适合控制/反应式逻辑，因为事件本来就是这类系统的核心驱动单位。

## 构造方式与承载格式

### 建模入口

原文中的主要建模入口是：

1. 设计带 hierarchy、concurrency 与 communication 的 statechart。
2. 给关键状态补 state invariants。
3. 用 `iState` 把图结构翻译到 guarded-command 风格中间形式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `EventCode` 映射；
2. `Statement` / `Condition` 抽象语法树；
3. `VTuple` 集合；
4. 输出到 `AMN`、`Pascal` 与 `Java` 的翻译链。

### 交换与互操作

这篇论文的互操作重点不在外部标准，而在内部验证桥接：

1. `statechart` -> guarded commands；
2. guarded commands -> verification tuples；
3. verification tuples -> `Simplify` 可处理的 Hoare 风格证明条件。

## 配套基础设施

- 建模/编辑工具：`iState` 负责 statechart 翻译与验证扩展。
- 解析/交换/元模型支持：`EventCode`、`Statement`、`Condition` 与 `VTuple` 作为内部中间表示。
- 仿真/执行支持：论文强调可翻译到 `AMN`、`Pascal` 与 `Java`，说明其保留了可执行生成路径。
- 验证/分析支持：`Simplify` 定理证明器负责一阶逻辑与线性算术下的证明义务求解。
- 代码生成/转换支持：支持 statechart 到 `AMN/Pascal/Java` 的转换。
- 标准化或社区生态：无统一行业标准，属于研究型工具桥接路线。

## 适用场景与需求前提

### 适用场景

适合需要给 statechart 补安全不变式、检查局部状态意图是否被迁移保持的 reactive software / control logic 验证场景。

### 需求前提

1. 系统已经被建成 statechart，而不是纯代码或纯时序逻辑。
2. 需求能压成状态级 predicates，而不是只能写成全局时序性质。
3. 团队接受 event-centric statechart semantics 与 theorem-proving 路线。
4. 目标性质主要是 safety / consistency，而不是完整 liveness。

### 不适用或高成本场景

若需求主要是时间约束、概率性质或复杂连续动态，单靠这条 invariant 路线就不够，需要转向 timed / probabilistic / hybrid 工具链。

## 与相邻形式主义的关系

相对 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)，这篇论文不再讨论 `Statecharts` 本体提出，而是给它补验证线路；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，`iState` 更偏局部 proof obligations 和 theorem prover，而不是把整机翻到另一个模型检查器；相对 [a-method-for-testing-and-validating-executable-statechart-models/desc.md](../a-method-for-testing-and-validating-executable-statechart-models/desc.md)，那篇偏测试与场景校验，这篇偏静态证明。

## 与本研究的关系

### 对 Project 1 的价值

1. 它给了“生成后的状态机如何补局部语义检查”的直接路线。
2. 把需求文字压成状态 invariants，再挂到生成 statechart 上，是 `project_1` 很自然的后处理方向。
3. `VTuple` 这种中间表示也提醒我们：验证剖面不一定非要直接写成时序逻辑，也可以先走局部证明义务。

### 局限

1. 对时间与概率性质支持弱。
2. 工具公开生态不强，复现门槛高于成熟模型检查器。

## 重要的相关工作

- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)：提供 `Statecharts` 母线本体。
- [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：对照 `UML/State Machine -> model checker` 的另一条自动验证路线。
- [a-method-for-testing-and-validating-executable-statechart-models/desc.md](../a-method-for-testing-and-validating-executable-statechart-models/desc.md)：对照测试/验证执行态状态图的场景化方法。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一个适合归入 `statecharts` 工具/方法锚点的条目，价值在于“state invariants + verification tuples”这条局部验证路线。
