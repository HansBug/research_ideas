# 下推模块检验 / Pushdown module checking

## 基本信息

- 标题：Pushdown module checking
- 中文标题：下推模块检验
- 作者：Laura Bozzelli, Aniello Murano, Adriano Peron
- 发表：*Formal Methods in System Design*, 36(1):65-95, 2010
- DOI：`10.1007/s10703-010-0093-x`
- 链接：http://dx.doi.org/10.1007/s10703-010-0093-x
- 形式主义：`Open Pushdown Systems (OPD)`，即开放式下推系统 / pushdown modules
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / open recursive hierarchy
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `OPD` tuple、induced module `M_S`、environment pruning semantics 与 pushdown tree automata reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 control states、stack alphabet、environment partition 与 module-checking tree semantics。

## 简报

这篇论文把 module checking 从有限层次开放系统继续推进到了 pushdown / recursive setting。它真正补到树上的不是某个复杂度定理，而是 `Open Pushdown Systems (OPD)` 这个模型本体：配置不仅有控制状态和栈，还要按 system/environment 分区，从而把开放环境剪枝语义正式接到无界调用栈上。对层次状态机支线来说，这正是 `Open Hierarchical Modules` 再往“递归开放系统”方向长出的经典后继。

- 形式主义定位：`module checking` 在 pushdown / recursive 系统上的扩展，也是 finite open hierarchy 向 open recursive hierarchy 的标准过桥点。
- 构造方式简述：模型仍有 system/environment 两类配置，但每个配置再携带 pushdown stack；环境通过 pruning computation tree 的方式选择外部后继。
- 基础设施与场景简述：纯理论条目，但清楚给出了 `OPD -> module M_S -> pushdown tree automata` 的自动机化路线。

```text
pushdown control + environment partition -> open computation tree -> pruning semantics -> CTL / CTL* module checking
```

## 形式主义定义与核心对象

### 定义对象

论文先回顾 finite-state module checking，然后指出 open systems 一旦带上无界栈，就需要一个既保 pushdown 递归、又保 environment choice 的 formalism，于是定义了 `OPD`。

### 核心抽象

原文把一个 `OPD` 写成：

$$
S=\langle AP,\Gamma,P,p_0,\Delta,L,Env\rangle
$$

上式中的符号逐项解释如下：

1. `AP` 是原子命题集合。
2. `\Gamma` 是栈字母表。
3. `P` 是控制状态集合，`p_0` 是初始控制状态。
4. `\Delta` 是 pushdown transition rules 集合。
5. `L` 是根据控制状态与栈顶符号给标签的函数。
6. `Env\subseteq P\times(\Gamma\cup\{\gamma_0\})` 用来标出 environment configurations。

论文进一步把 `OPD` 诱导成一个 module：

$$
M_S=\langle AP,W_s,W_e,\to,w_0,\mu\rangle
$$

其中 `W_s` 与 `W_e` 是 system / environment configurations 的分区。

### 一个最小例子与通俗解释

论文给的直觉例子是饮料机：

1. 闭系统版本里，机器自己在茶和咖啡之间做内部选择。
2. 开放系统版本里，环境决定这一步想要茶还是咖啡。
3. 再往上加 pushdown stack 后，就能表达“环境驱动的递归服务/子过程调用”。

通俗地说，`OPD` 是“环境可在某些配置上插手决策的 pushdown 状态机”。它不是普通 pushdown games，因为这里的 open semantics 来自 module checking 的环境剪枝，而不是显式双人赢法。

### 运行 / 接受 / 转移语义

一个 `OPD` configuration 形如：

$$
(p,\alpha)
$$

上式中的符号逐项解释如下：

1. `p\in P` 是当前控制状态。
2. `\alpha\in \Gamma^*\cdot\gamma_0` 是当前栈内容。

根据 `OPD` 规则，诱导模块里的迁移满足：

$$
(p,A\cdot\alpha)\to(q,\beta)
$$

表示若存在相应 pushdown rule，则在读到当前栈顶 `A` 时，把控制切到 `q` 并把栈改写成 `\beta`。

module checking 的关键不在单条 run，而在所有环境剪枝后的执行树集合：

$$
exec(M_S)
$$

即环境可在 environment configurations 上删去部分后继分支后，所有可能保留下来的 computation trees。

### 语义边界

这个 family 的边界如下：

1. 它是 open pushdown systems，而不是一般 pushdown games。
2. 它保留无界栈，但不引入 dense time 或连续变量。
3. 它强调 system/environment partition 与 pruning semantics。
4. 若去掉 environment partition，就退回 closed pushdown model checking。

### 关键性质与判定边界

论文给出最核心的结论：

$$
\mathrm{PMC}(OPD,CTL)\text{ is }2\mathrm{EXPTIME}\text{-complete}
$$

以及：

$$
\mathrm{PMC}(OPD,CTL^*)\text{ is }3\mathrm{EXPTIME}\text{-complete}
$$

对固定公式，复杂度为：

$$
\mathrm{EXPTIME}\text{-complete}
$$

这说明 open recursive hierarchy 比 closed pushdown model checking 显著更难，但仍处在清晰的自动机理论边界之内。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | control states + pushdown stack + environment partition。 |
| 事件 / 触发 | 强支持 | push/pop/rewrite rules 决定配置迁移。 |
| 守卫 / 数据 | 弱支持 | 标签只看控制状态与栈顶；核心不在数据。 |
| 层次 | 强支持 | stack-based recursion 是核心。 |
| 并发 / 同步 | 不支持 | 仍是 sequential pushdown。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `CTL/CTL*` pushdown module checking。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `OPD` 元组 | `$S=\langle AP,\Gamma,P,p_0,\Delta,L,Env\rangle$` | 开放式 pushdown 模型骨架。 |
| 诱导 module | `$M_S=\langle AP,W_s,W_e,\to,w_0,\mu\rangle$` | 转成 module-checking 语义的对象。 |
| configuration | `$(p,\alpha)$` | 控制状态 + 栈内容。 |
| 执行树集合 | `$exec(M_S)$` | 所有环境剪枝后的 computation trees。 |
| 复杂度 | `CTL: 2EXPTIME`, `CTL*: 3EXPTIME`, fixed formula: `EXPTIME` | pushdown module checking 主边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 pushdown control states 与 stack alphabet。
2. 再标出哪些 `(state, top-of-stack)` 组合属于环境控制。
3. 用 pushdown rules 描述配置重写。
4. 最后通过 induced module 与 environment pruning 解释开放语义。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `OPD` tuple；
2. pushdown configurations；
3. induced module `M_S`；
4. execution-tree set `exec(M_S)`；
5. pushdown tree automata。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md) 的 open hierarchical modules。
2. 旁接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 所代表的 `RSM` / pushdown 递归母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `OPD` 元组、environment partition 与 `exec(M_S)`。
- 仿真/执行支持：可按 pushdown configuration semantics 直接运行。
- 验证/分析支持：`CTL/CTL*` pushdown module checking、pushdown tree automata emptiness。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要连接 module checking、pushdown verification 与 open systems。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归调用栈上的 open-system verification。
2. 需要 system/environment 明确分责的程序控制流。
3. 想把 finite open hierarchy 推到 recursive open hierarchy。

### 需求前提

1. 系统核心复杂度来自栈式递归。
2. 环境控制边界必须能在配置层显式分区。
3. 关注的是 branching-time open semantics，而不是线性 trace。

### 不适用或高成本场景

如果系统是 closed 的，就没必要上 module checking；如果环境与系统是显式双人对抗关系，则 `RGG` 更合适；如果只需要有限层次 open model，`Open Hierarchical Modules` 更轻。

## 与相邻形式主义的关系

相对 open hierarchical modules，它把有限 hierarchy 推向了 pushdown / recursive stack setting；相对 `RSM`，它加入了 environment partition 和 pruning semantics；相对 pushdown games，它不是策略竞争，而是 module checking。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机支线中的“open-system”方向不会停在有限 `HSM`。一旦需求里有递归子过程和环境不可控选择，理论上就会自然长到 `OPD / pushdown module checking` 这一层。

### 对状态机自动建模的启发

如果未来要把需求映射到可验证的 open recursive model，这篇论文给出了一个比 plain `RSM` 更贴近环境交互语义的目标 formalism。

## 重要的相关工作

1. [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)：finite open hierarchy 的代表条目。
2. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：open pushdown 递归所依附的 recursive-state-machine 母线。
3. `module checking` for finite-state systems：本文明确以它为理论前身。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🧩 经典离散状态机`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🤝 接口 / 交互契约`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> Open Hierarchical Modules -> Open Pushdown Systems / Pushdown Module Checking` 位置，用来表明 open hierarchy 分支在 classic automata-theory 里确实继续长到了 recursive pushdown setting。
