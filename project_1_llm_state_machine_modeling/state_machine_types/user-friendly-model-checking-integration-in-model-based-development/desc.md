# AutoFocus 3 的易用化模型检查集成 / User-friendly Model Checking Integration in Model-based Development

## 基本信息

- 标题：User-friendly Model Checking Integration in Model-based Development
- 中文标题：AutoFocus 3 的易用化模型检查集成
- 作者：Alarico Campetelli，Florian Hölzl，Philipp Neubeck
- 发表：*Proceedings of the 24th International Conference on Computer Applications in Industry and Engineering*，pp. 199-204，2011
- DOI：原文未给出
- 链接：https://download.fortiss.org/public/projects/af3/research/2011/af3_mc.pdf
- 形式主义：`AutoFocus 3 / SMV / TVARC`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：component-scoped property specification and model-checking integration route for `AutoFocus 3`
- 工具/实现获取方式：原文说明该方案直接集成在 `AutoFocus 3` 中，并使用 `Cadence SMV` 与 `TVARC` 作为后端 model checker。
- 标准/格式获取方式：承载方式是 `AutoFocus 3` 模型、property templates / patterns / `SALT`、转译后的 `SMV` 或 `TVARC` 模型，以及 `MSC`/simulation counterexample views；原文未给独立标准格式。

## 简报

这篇论文的重点，不是再定义一种状态机，而是把模型检查真正嵌进 `AutoFocus 3` 的建模流程里。论文把 usability 明确拆成四件事：属性与模型元素的紧耦合、不同层次的属性说明语言、可读的 counterexample 展示，以及多个 model checker 的性能比较。对本论文集而言，它是一条典型的 `🛠️` 方法路线条目：它说明一个组件自动机 DSL 怎样被做成“持续局部验证”的开发环境。

- 形式主义定位：`AutoFocus 3` 上层的 property-oriented verification integration route。
- 构造方式简述：先把性质附着到组件，再选择验证上下文，之后转译到 `SMV` 或 `TVARC`，最后把反例映回 simulation/`MSC`。
- 基础设施与场景简述：依托 `AutoFocus 3` 模型、property templates、patterns、`SALT`、`Cadence SMV`、`TVARC`、counterexample replay 与 `MSC` view，服务 embedded component models 的持续验证。

```text
AutoFocus 3 component model + attached property -> SMV / TVARC translation -> model checking -> simulation / MSC counterexample feedback
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `AutoFocus 3` component hierarchy。
2. 挂接到 component 上的 verification properties。
3. property templates、patterns 与 `SALT`。
4. `SMV` 与 `TVARC` 两条后端。
5. simulation 与 `MSC` counterexample feedback。

### 核心抽象

论文对“属性作用域”说得很清楚。可把某个属性 `\varphi` 挂到组件 `C` 的规则整理为：

$$
\mathrm{Scope}(C,\varphi) \subseteq Ports(C) \cup \bigcup_{D \in Sub(C)} Ports(D) \cup Vars(C)
$$

上式中的符号逐项解释如下：

1. `Ports(C)` 是组件 `C` 自身的输入/输出端口。
2. `Sub(C)` 是 `C` 的直接子组件集合。
3. `Vars(C)` 是若 `C` 用 automaton 定义时可见的 state variables。
4. 这正对应论文对 property scope 的原文描述。

论文还定义了一个“验证上下文”。若用户选择验证组件 `C`，则系统只考虑 `C` 及其子层级，而忽略外部环境，因此可保守写成：

$$
\mathrm{Verify}(C,\varphi) = \mathrm{MC}\left(\llbracket C^\downarrow \rrbracket, \mathrm{Enc}(\varphi)\right)
$$

上式中的符号逐项解释如下：

1. `C^\downarrow` 表示组件 `C` 及其全部后代组件构成的子层级。
2. `\llbracket C^\downarrow \rrbracket` 表示该子层级的 formal model。
3. `\mathrm{Enc}(\varphi)` 表示把属性编码成 `SMV` 或 `TVARC` 可消费的形式。
4. `MC` 表示执行 model checking。
5. 论文明确说：chosen component fixes the verification context。

对模板属性，论文给出示例：

$$
G\big((A = X) \rightarrow F(B = Y)\big)
$$

上式中的符号逐项解释如下：

1. `A` 是某个输入端口。
2. `B` 是某个输出端口。
3. `X`、`Y` 是用户在模板中绑定的值。
4. 这正对应论文里的模板 “After input port A has value X, output port B has eventually value Y”。

### 一个最小例子与通俗解释

论文里最适合入门的例子，就是图 1 那种“小组件网络 + 模板属性”：

1. 用户先选一个组件或某个端口。
2. 从模板列表里选一个常见性质，例如 “Port value is eventually equal to X”。
3. 把模板变量填成端口名、状态变量或常量。
4. 工具把它翻成 `SMV` 或 `TVARC` 约束。
5. 若失败，就把 counterexample 展示为 simulation 或 `MSC`。

通俗地说，这条路线的意义在于：开发者不用先离开建模环境、再手写一堆底层时序逻辑，才能做验证。属性是跟着组件走的，反例也能回到组件图上。

### 运行 / 接受 / 转移语义

论文这里不重新定义 `AutoFocus 3` 的 automaton 语义，而是强调验证如何贴在既有组件语义上：

1. 属性绑定到组件。
2. 组件与其子组件确定验证上下文。
3. 模型被翻译到 `SMV` 或 `TVARC`。
4. 反例再映射回 `AutoFocus 3` 级 simulation/`MSC`。

因此它的关键语义，不是新状态机，而是“组件级局部验证”的工作流语义。

### 语义边界

1. 本文不是 `AutoFocus 3` 语言本体，而是其 model-checking integration。
2. 主线是 usability 和 tool support，不是新 verifier algorithm。
3. 两个后端里，`SMV` 路线更成熟，`TVARC` 路线在文中还处于持续集成阶段。
4. 该方法默认验证的是组件子层级，外部环境被抽空，这既是优势也是边界。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 属性作用域 | `$\mathrm{Scope}(C,\varphi) \subseteq Ports(C) \cup \bigcup_{D \in Sub(C)} Ports(D) \cup Vars(C)$` | 性质只允许引用当前组件、直接子组件和局部 automaton 变量。 |
| 验证上下文 | `$\mathrm{Verify}(C,\varphi) = \mathrm{MC}(\llbracket C^\downarrow \rrbracket, \mathrm{Enc}(\varphi))$` | 选中的组件固定了验证子系统。 |
| 模板属性 | `$G((A = X) \rightarrow F(B = Y))$` | 论文给出的典型高层模板可以压成标准时序逻辑。 |
| 反例回映 | `$\mathrm{cex}_{backend} \rightarrow \mathrm{simulation} / \mathrm{MSC}$` | 工具链的工程核心是把 backend 反例还原到模型层。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强 | 依托 `AutoFocus 3` 的 component + automata 模型。 |
| 事件 / 触发 | 强 | 可直接引用 ports 与 state variables。 |
| 守卫 / 数据 | 中等支持 | 模板和值检查能绑定到具体类型。 |
| 层次 | 强 | 验证上下文直接利用 component hierarchy。 |
| 并发 / 同步 | 中等支持 | 通过所选组件子层级一并进入后端模型。 |
| 时间约束 | 间接支持 | 主要取决于后端和 `AutoFocus 3` 模型本体。 |
| 连续动态 / 随机性 | 不支持 | 不是主体。 |
| 可执行 / 可验证性 | 很强 | property specification、model checking、debugging 三位一体。 |

### 形式化问题与性质

1. 这篇论文把“模型检查是否易用”当成一个一等工程问题来做。
2. 真正的技术核心在于 component-scoped properties、template/pattern abstraction 和 counterexample feedback。
3. 它不是要替代 `SMV` 或 `TVARC`，而是把这些后端嵌进 component DSL 的日常开发流程。

## 构造方式与承载格式

### 建模入口

主要入口有：

1. `AutoFocus 3` component model。
2. property templates。
3. specification patterns。
4. `SALT`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 转译后的 `SMV` model。
2. 转译后的 `TVARC` model。
3. backend counterexample。
4. `MSC` 和 simulation views。

### 交换与互操作

互操作重点在 verification bridge：

1. `AutoFocus 3 -> SMV`。
2. `AutoFocus 3 -> TVARC`。
3. backend counterexample -> model-level simulation / `MSC`。

## 配套基础设施

- 建模/编辑工具：`AutoFocus 3` 图形建模环境。
- 解析/交换/元模型支持：properties 随模型一起保存，支持模板和值的类型检查。
- 仿真/执行支持：counterexample simulation 与 on-target/co-simulation 环境。
- 验证/分析支持：`Cadence SMV`、`TVARC`、模板/模式/`SALT` 三层属性输入。
- 代码生成/转换支持：重点是到 backend verifier 的模型转换，而不是部署代码。
- 标准化或社区生态：`AutoFocus 3`、`SMV`、`TVARC` 和 `MSC` visualization 共同构成生态。

## 适用场景与需求前提

### 适用场景

适合 embedded component models 的持续局部验证，尤其适合开发者希望在建模环境内部直接做属性检查和反例调试的场景。

### 需求前提

1. 模型需已落成 `AutoFocus 3` component hierarchy。
2. 关键性质需能绑定到端口、状态变量和组件上下文。
3. 团队希望把 formal verification 放进日常建模流程，而不是后置离线执行。

### 不适用或高成本场景

如果团队并不使用 `AutoFocus 3`，或者模型与属性无法稳定翻译到 `SMV/TVARC`，这套路线的收益会迅速下降。

## 与相邻形式主义的关系

相对 [autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md](../autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md)，本文是 `AutoFocus 3` 的验证集成路线而非平台本体；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，两者都在做 DSL -> backend bridge，但本文更强调 property usability 和 feedback loop；相对 [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)，后者是 backend 本体，本文是 front-end integration。

## 与本研究的关系

### 对 Project 1 的价值

1. 它直接说明：如果未来让 LLM 生成状态机模型，还需要同时生成“可挂在模型元素上的性质模板”。
2. 对 `project_1` 的验证场景生成与闭环修复任务，这种 component-scoped property + counterexample feedback 的设计非常贴近目标。
3. 它也提醒我们：验证结果必须回到模型语境中，最好能被自动解释成结构化证据，而不是只输出 backend 原生反例。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像面向工程落地的 verification workflow，而不是最终的状态机类型本体。

## 重要的相关工作

- [autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md](../autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md)：平台本体。
- [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：另一条 DSL 到 model checker 的桥接路线。
- [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)：symbolic backend 本体的对照条目。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 verification-integration 条目，适合作为 `AutoFocus 3` component DSL 上“属性挂接、后端转译、反例回映”这条方法路线的直接证据入账。
