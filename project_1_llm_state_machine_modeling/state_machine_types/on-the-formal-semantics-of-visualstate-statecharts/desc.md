# VisualSTATE 状态图的形式语义 / On the Formal Semantics of VisualSTATE Statecharts

## 基本信息

- 标题：On the Formal Semantics of VisualSTATE Statecharts
- 中文标题：VisualSTATE 状态图的形式语义
- 作者：Andrzej Wasowski，Peter Sestoft
- 发表：*IT University Technical Report Series*，TR-2002-19，30 页，2002 年 9 月
- DOI：原文未给出 DOI
- 链接：https://pure.itu.dk/en/publications/on-the-formal-semantics-of-visualstate-statecharts
- 形式主义：`VisualSTATE Statecharts`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：implementation-oriented semantics / commercial statechart variant stabilization
- 工具/实现获取方式：论文围绕商业工具 `IAR VisualSTATE` 的状态图方言展开，并说明该语义已被用于实验性代码生成器 `SCOPE` 的规范；原文未提供开源仓库。
- 标准/格式获取方式：`VisualSTATE` 不是公开交换标准；可获取的稳定规范主要就是这篇技术报告与对应 tool concept guide。

## 简报

这篇论文的价值，不只是“再讲一遍 statecharts”。它做的是把 `IAR VisualSTATE` 这一实际商用方言的语义钉死成实现导向、可编译、可验证的正式说明，让状态图不只是设计草图，而是代码生成器和验证器都能依赖的稳定语言骨架。

- 形式主义定位：特定 statechart 方言的正式语义与实现规范，而不是新的通用理论母线。
- 构造方式简述：先定义层次状态、history marking、事件、变量与多目标迁移，再用全局配置、store、history 和 signal queue 定义 microstep / macrostep 语义。
- 基础设施与场景简述：依托 `IAR VisualSTATE` 商业建模环境和 `SCOPE` 代码生成实验，服务嵌入式控制算法的可执行建模、代码生成和验证。

```text
VisualSTATE syntax -> implementation-oriented semantic objects -> microstep / macrostep execution -> deterministic priority resolution -> code generation / verification basis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `VisualSTATE` 的层次状态集合与 hierarchy relation。
2. initial / history markings。
3. 事件、变量、动作与多目标迁移。
4. 全局执行状态：configuration、store、history、signal queue。
5. microstep / macrostep 执行语义与 priority-based 冲突消解。

### 核心抽象

论文对一致系统给出的总对象定义是：

$$
System = (State, @, S, initial, \eta_0, exit, entry, Var, Event, Trans)
$$

上式中的符号逐项解释如下：

1. `State` 是状态集合。
2. `@` 是层次关系，表示子状态到父状态的树结构。
3. `S` 是状态类型信息。
4. `initial` 与 `\eta_0` 分别是初始 marking 与初始 history marking。
5. `exit` 与 `entry` 是状态进入/退出规则。
6. `Var` 与 `Event` 是变量和事件集合。
7. `Trans` 是一致的迁移集合。

论文对迁移骨架的正式化很关键，可保守整理为：

$$
Trans \subseteq Ebind \times State_{or} \times \mathcal P(State_{and}) \times \mathcal P(State_{and}) \times Bexp \times Action \times \mathcal P(State_{and})
$$

上式中的符号逐项解释如下：

1. `Ebind` 是带参数绑定的触发事件。
2. `State_{or}` 表示显式 scope 所在的 `or-state`。
3. 两个 `\mathcal P(State_{and})` 分别对应 positive / negative state conditions。
4. `Bexp` 是布尔守卫条件。
5. `Action` 是迁移动作。
6. 最后的目标状态集合允许显式目标外再加 forced states，因此它是多目标迁移。

论文对全局执行状态给出的四元组非常重要：

$$
G = (\sigma, \rho, \eta, \omega)
$$

上式中的符号逐项解释如下：

1. `\sigma` 是 explicit state configuration。
2. `\rho` 是变量 store。
3. `\eta` 是 history marking。
4. `\omega` 是 signal queue。
5. 这四者共同决定任一时刻系统的可执行行为。

论文进一步把执行拆成外部事件驱动的宏步，可保守压成：

$$
(\sigma, \rho, \eta, \epsilon, e_{ext}) \xRightarrow{\mathrm{macro}} (\sigma', \rho', \eta', \epsilon)
$$

上式中的符号逐项解释如下：

1. `e_{ext}` 是单个外部输入事件。
2. 宏步期间可能产生若干内部 signal，并被放入队列依次处理。
3. `\epsilon` 表示队列为空。
4. 论文强调一次宏步处理一个外部事件，然后持续消费内部 signals 直到队列清空。

### 一个最小例子与通俗解释

论文附录和正文都围绕控制器类 statechart 讨论。用最小直觉例子可以这样理解：

1. 系统在某个 `Closed` / `Standby` 状态等待外部按钮事件。
2. 一个迁移由事件触发，并可带正负状态条件、守卫和动作。
3. 动作既可能修改变量，也可能发出内部 signal。
4. 内部 signal 进入 FIFO queue，并在同一外部事件处理期间继续触发后续微步。

通俗地说，`VisualSTATE` 不是“点一下箭头就瞬时完成”的朴素状态图，而是一套带层次、history 和记忆、内部 signal 队列和确定性优先级裁决的可执行状态机语言。

### 运行 / 接受 / 转移语义

论文明确采用 microstep / macrostep 执行结构：

$$
\mathrm{MacroStep}(e_{ext}) = \mathrm{MicroStep}(e_{ext}) ; \mathrm{MicroStep}(signal_1) ; \cdots ; \mathrm{MicroStep}(signal_k)
$$

上式中的符号逐项解释如下：

1. `e_{ext}` 是当前外部事件。
2. 每个 `signal_i` 是动作执行后进入 queue 的内部事件。
3. 一个宏步会持续执行，直到 signal queue 为空。
4. 这正是论文所说 run-to-completion 的具体实现方式。

同时，论文把冲突迁移的裁决建立在 priority function 上，可保守写成：

$$
t_i \prec t_j \Rightarrow t_i\ \text{has lower priority than}\ t_j
$$

其含义是：

1. priority function 是全序。
2. 冲突迁移不再保留非确定性，而是由优先级决定保留哪一条。
3. 这使语义更适合实现与代码生成。

### 语义边界

这篇论文的边界也很清楚：

1. 它是全局、非组合式语义。
2. 它紧贴 `VisualSTATE` 实际实现，而不是追求所有 statechart 变体的统一抽象。
3. 它重点是嵌入式控制算法、代码生成和可执行语义，不是 profile 标准化。
4. 外部环境的事件缓冲不在论文语义内部定义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 一致系统对象 | `$System = (State, @, S, initial, \eta_0, exit, entry, Var, Event, Trans)$` | 说明 `VisualSTATE` 语义不仅有状态图，还包含 history、entry/exit 规则与变量环境。 |
| 多目标迁移 | `$Trans \subseteq Ebind \times State_{or} \times \mathcal P(State_{and}) \times \mathcal P(State_{and}) \times Bexp \times Action \times \mathcal P(State_{and})$` | 把触发、scope、正负条件、守卫、动作和多目标都统一纳入迁移对象。 |
| 全局执行状态 | `$G = (\sigma, \rho, \eta, \omega)$` | 说明执行不是只看当前活动状态，还要看变量、history 和记号队列。 |
| 宏步语义 | `$\mathrm{MacroStep}(e_{ext}) = \mathrm{MicroStep}(e_{ext}) ; \mathrm{MicroStep}(signal_1) ; \cdots$` | 解释 `VisualSTATE` 的 run-to-completion 处理方式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象就是层次状态与配置。 |
| 事件 / 触发 | 很强 | 外部事件、内部 signal 与参数绑定都是一等对象。 |
| 守卫 / 数据 | 很强 | 守卫、变量 store、外部 C 函数接口都被纳入语义。 |
| 层次 | 很强 | hierarchy、scope、history/deep history 都是主线。 |
| 并发 / 同步 | 很强 | orthogonal state 与多目标迁移都明确出现。 |
| 时间约束 | 弱支持 | 本文主线不在 clocks 或 dense-time。 |
| 连续动态 / 随机性 | 不支持 | 不在论文讨论范围内。 |
| 可执行 / 可验证性 | 很强 | 语义明确服务代码生成与验证。 |

### 形式化问题与性质

1. 论文最重要的工程立场是“语义必须能真正约束编译器行为”。
2. history、deep history、signal queue 与 priority resolution 这些实现敏感细节被正式写进语义，而不是留在工具手册的模糊描述里。
3. 它把 `VisualSTATE` 从“工具方言”推进成了一个有稳定执行骨架的状态机 DSL。

## 构造方式与承载格式

### 建模入口

原文中的建模入口主要有：

1. `VisualSTATE` 图形状态图。
2. 层次状态与 orthogonal regions。
3. 带参数的事件和动作。
4. entry / exit rules、history markings 与多目标迁移。

### 机器可处理承载方式

机器可处理承载方式包括：

1. hierarchy relation 和状态类型化；
2. 显式 transition tuple；
3. store / history / signal queue 组成的全局执行状态；
4. microstep / macrostep operational semantics。

### 交换与互操作

这篇论文不是交换标准论文，但它完成了关键的“语义稳定化”：

1. 人工图形状态图可转成明确的抽象语法对象。
2. 抽象语法对象可被代码生成器和验证器共享。
3. 这使 `VisualSTATE` 真正成为一种可复用的语义载体，而不是只依赖 IDE 的隐式解释。

## 配套基础设施

- 建模/编辑工具：`IAR VisualSTATE` 商业状态图建模环境。
- 解析/交换/元模型支持：论文给出的是语言语义，不是公开 `XML/XMI` 标准。
- 仿真/执行支持：`VisualSTATE` 自身支持建模与软件生成，论文语义直接面向执行解释。
- 验证/分析支持：论文明确把语义整理为 verification-friendly、compiler-friendly 形式。
- 代码生成/转换支持：原文说明这套语义已被用作实验代码生成器 `SCOPE` 的规范。
- 标准化或社区生态：它是 `VisualSTATE` 商业方言的正式技术报告，而不是开放标准。

## 适用场景与需求前提

### 适用场景

适合嵌入式控制算法、事件驱动控制逻辑和需要“图形建模 + 确定执行 + 代码生成”统一语义的 statechart 场景。

### 需求前提

1. 团队接受 `VisualSTATE` 这类实现导向 statechart 方言。
2. 需求能写成层次状态、事件、守卫和动作结构。
3. 需要 history、orthogonal regions 和内部 signal queue 这类语义细节。
4. 目标更偏代码生成或精确定义执行语义，而不是仅做高层草图。

### 不适用或高成本场景

如果团队需要开放交换标准、组合式语义，或希望把状态机直接接到现代开源建模生态，这篇论文代表的 `VisualSTATE` 路线会有明显局限。

## 与相邻形式主义的关系

相对 [the-statemate-semantics-of-statecharts/desc.md](../the-statemate-semantics-of-statecharts/desc.md)，这篇论文同样是具体方言语义钉扎，但 `VisualSTATE` 更强调实现导向的 deterministic operational semantics；相对 [statechart-development-beyond-wysiwyg/desc.md](../statechart-development-beyond-wysiwyg/desc.md)，`KIT/KIEL` 更偏建模入口与编辑基础设施，而这里更偏执行与编译语义；相对 [formal-compositional-semantics-for-yakindu-statecharts/desc.md](../formal-compositional-semantics-for-yakindu-statecharts/desc.md)，后者补的是组件化组合层，而这里补的是单体 statechart 方言本身。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 很重要，因为它展示了“把一个商用 statechart 方言写到足够精确”需要哪些语义部件。LLM 若要从需求自动生成高可信状态机，最终也必须面对 history、内部事件、冲突裁决和队列语义这些经常被概括掉的实现细节。

### 作为目标形式主义还是中间表示

更像可执行目标方言或工业工具语义蓝本，而不是轻量中间表示。

### 对需求到模型生成的启发

1. 只生成状态和箭头远远不够，真正可执行的 statechart 需要完整执行上下文。
2. priority resolution 与 signal queue 这类机制必须在需求到模型映射时就被明确。
3. 若目标是代码生成，语义应优先服务确定性与实现可行性，而不是只追求理论美观。

### 现实限制

论文采用全局、非组合式语义，这对后续模块化扩展和组合验证不是最理想的基础。

## 重要的相关工作

1. [the-statemate-semantics-of-statecharts/desc.md](../the-statemate-semantics-of-statecharts/desc.md)：另一条经典 statechart 工具方言语义线。
2. [statechart-development-beyond-wysiwyg/desc.md](../statechart-development-beyond-wysiwyg/desc.md)：更偏 statechart DSL 与编辑基础设施。
3. [formal-compositional-semantics-for-yakindu-statecharts/desc.md](../formal-compositional-semantics-for-yakindu-statecharts/desc.md)：把 statechart 语义从单体模型推进到组件化组合。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`VisualSTATE Statecharts`
- 论文角色：implementation-oriented semantics / commercial statechart variant stabilization
- 归类理由：论文主体是 `VisualSTATE` 这一稳定 statechart 方言的正式语义与实现基础设施，不是抽象 statechart 综述，也不是单纯案例论文。
