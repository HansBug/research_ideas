# 下推模块检验（LPAR 会议版） / Pushdown Module Checking

## 基本信息

- 标题：Pushdown Module Checking
- 中文标题：下推模块检验（LPAR 会议版）
- 作者：Laura Bozzelli, Aniello Murano, Adriano Peron
- 发表：*Logic for Programming, Artificial Intelligence, and Reasoning*, `LNCS 3835`, pp. 504-518, 2005
- DOI：`10.1007/11591191_35`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/Pushdown.pdf
- 形式主义：`Open Pushdown Systems (OPD) / Pushdown Module Checking`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：conference origin / open recursive hierarchy
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `OPD` tuple、induced module `M_S`、environment pruning 语义与 pushdown tree automata reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 control states、stack alphabet、environment partition、induced module 与 branching-time module-checking 语义。

## 简报

这篇 `LPAR 2005` 会议论文的价值，在于它第一次把 finite-state module checking 明确推进到 pushdown / recursive setting，并把这个新 family 直接命名成 `Open Pushdown Systems (OPD)`。它不只是说“开放系统也许可以带栈”，而是把 `system/environment` 分区、pushdown 配置和 `exec(M_S)` 剪枝语义整理成了一个稳定 tuple，因此它正是当前演化树里 `Open Hierarchical Modules` 继续长到 recursive hierarchy 的 conference 起点。

- 形式主义定位：finite open hierarchy 进入无界调用栈之后的第一篇标准化条目，也是 `Open Pushdown Systems / Pushdown Module Checking` 节点的会议版奠基文献。
- 构造方式简述：模型由 control state、stack content 和 environment partition 组成；环境只在 environment configurations 上剪枝，而不显式扮演策略玩家。
- 基础设施与场景简述：原文纯理论，但已经完整给出 `OPD -> module M_S -> pushdown tree automata` 的自动机化分析路线，并固定了 `CTL / CTL*` 的经典复杂度边界。

```text
open hierarchical module intuition -> pushdown control + stack -> induced open module M_S -> pruning semantics exec(M_S) -> CTL / CTL* module checking
```

## 形式主义定义与核心对象

### 定义对象

论文从 finite-state module checking 出发，指出一旦系统包含递归子过程，单纯 finite open hierarchy 已不足以表达其行为，因此需要一个同时保留 pushdown recursion 与 open-system pruning semantics 的 formalism。

### 核心抽象

原文把一个 `OPD` 写成：

$$
S = \langle AP, \Gamma, P, p_0, \alpha_0, \Delta, L, Env \rangle
$$

上式中的符号逐项解释如下：

1. `AP` 是原子命题集合。
2. `\Gamma` 是栈字母表，另有底符号 `\gamma_0 \notin \Gamma`。
3. `P` 是控制状态集合，`p_0 \in P` 是初始控制状态。
4. `\alpha_0 \in \Gamma^* \cdot \gamma_0` 是初始栈内容。
5. `\Delta \subseteq (P \times (\Gamma \cup \{\gamma_0\})) \times (P \times \Gamma^*)` 是 pushdown 迁移关系。
6. `L : P \times (\Gamma \cup \{\gamma_0\}) \to 2^{AP}` 给控制状态与栈顶符号打标签。
7. `Env \subseteq P \times (\Gamma \cup \{\gamma_0\})` 指出哪些 `(state, top-of-stack)` 属于 environment configurations。

论文随后把 `OPD` 诱导成一个 open module：

$$
M_S = \langle AP, W_s, W_e, R, w_0, \mu \rangle
$$

其中 `W_s` 与 `W_e` 是 system / environment configurations 的分区，`w_0 = (p_0,\alpha_0)`。

### 一个最小例子与通俗解释

原文延续 module checking 里的饮料机直觉。可以把它理解成：

1. 系统某个 configuration 上会调用一个递归子服务。
2. 在 system configuration 上，所有后继都由系统自身保留。
3. 在 environment configuration 上，环境可以删去部分后继，但不能把全部后继都删光。

通俗地说，`OPD` 就是“带无界栈、而且环境能在某些配置上删分支的状态机”。它比 closed pushdown system 多的是 open pruning semantics，比 finite open hierarchy 多的是 pushdown recursion。

### 运行 / 接受 / 转移语义

一个 configuration 形如：

$$
(p,\alpha)
$$

上式中的符号逐项解释如下：

1. `p \in P` 是当前控制状态。
2. `\alpha \in \Gamma^* \cdot \gamma_0` 是当前栈内容。

若 `((p,A),(q,\beta')) \in \Delta`，则 induced module 里的迁移满足：

$$
((p, A \cdot \alpha), (q, \beta' \cdot \alpha)) \in R
$$

而 open-system 语义不是只看某一条 run，而是看所有环境可能保留的执行树集合：

$$
exec(M_S)
$$

对任意 environment node，环境可以从 `succ(w)` 中选取一个非空子 tuple 作为保留后继；因此 module checking 判断的是：

$$
M_S \models_r \varphi
$$

即 `exec(M_S)` 中所有执行树都满足公式 `\varphi`。

### 语义边界

这个 family 的边界如下：

1. 它是 open pushdown systems，而不是一般双人 pushdown games。
2. 它保留无界调用栈，但不引入时间、连续变量或概率。
3. 它的开放性来自 environment pruning，而不是显式 adversarial winning condition。
4. 若去掉 `Env` 分区，就退回 closed pushdown model checking；若去掉栈，就退回 finite-state module checking。

### 关键性质与判定边界

会议版已经给出当前节点最核心的复杂度结论：

$$
\mathrm{PMC}(OPD, CTL) \text{ is } 2\mathrm{EXPTIME}\text{-complete}
$$

以及：

$$
\mathrm{PMC}(OPD, CTL^*) \text{ is } 3\mathrm{EXPTIME}\text{-complete}
$$

对固定 `CTL^*` 公式，原文还给出：

$$
\mathrm{PMC}(OPD, \varphi_{\mathrm{fixed}}) \text{ is } \mathrm{EXPTIME}\text{-complete}
$$

因此，这篇会议论文已经足够把 `OPD` 节点从“层次模块的自然延伸”稳定成独立 family，而不只是 journal full version 的前置摘要。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | control state、stack content、environment partition 共同构成状态。 |
| 事件 / 触发 | 强支持 | push/pop/rewrite 规则直接决定 configuration 迁移。 |
| 守卫 / 数据 | 弱支持 | 原文标签只依赖控制状态与栈顶，不以复杂变量语义为中心。 |
| 层次 | 强支持 | recursion / pushdown stack 是模型本体的一部分。 |
| 并发 / 同步 | 不支持 | 仍是 sequential recursive family。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可观测性 / 信息模式 | 强支持 | system / environment 分区与 pruning semantics 是关键。 |
| 可执行 / 可验证性 | 强理论支持 | induced module、pushdown tree automata、`CTL / CTL*` complexity 全部明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `OPD` 元组 | `$S = \langle AP, \Gamma, P, p_0, \alpha_0, \Delta, L, Env \rangle$` | open recursive pushdown model 的基本骨架。 |
| induced module | `$M_S = \langle AP, W_s, W_e, R, w_0, \mu \rangle$` | 把 `OPD` 放进 module-checking 语义后的对象。 |
| configuration | `$(p,\alpha)$` | 控制状态 + 栈内容。 |
| 执行树集合 | `$exec(M_S)$` | 所有环境剪枝后的 open computations。 |
| 复杂度 | `CTL: 2EXPTIME`, `CTL*: 3EXPTIME` | conference 版已固定的主边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义 pushdown control states、stack alphabet 与初始 stack。
2. 再标出哪些 `(state, top-of-stack)` 属于 environment configurations。
3. 用 `\Delta` 描述 push/pop/rewrite 规则。
4. 最后通过 induced module `M_S` 和 `exec(M_S)` 解释开放 branching-time 语义。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `OPD` tuple；
2. pushdown configurations；
3. induced module `M_S`；
4. environment pruning semantics；
5. pushdown tree automata reduction。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md) 的 `Open Hierarchical Modules`。
2. 向旁承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 所代表的 recursive pushdown 母线。
3. 向后续推进到 [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md) 与 [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供公开实现。
- 解析/交换/元模型支持：核心是 `OPD` 元组、induced module 与 `exec(M_S)`。
- 仿真/执行支持：可按 pushdown configuration 语义展开运行。
- 验证/分析支持：`CTL / CTL*` pushdown module checking、pushdown tree automata emptiness。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要连接 module checking、pushdown verification 与 open recursive systems。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流上的 open-system verification。
2. 需要明确划分 system / environment 配置的开放递归模型。
3. 想把 finite open hierarchy 继续推进到 pushdown / recursive setting 的场景。

### 需求前提

1. 系统核心复杂度来自栈式递归，而不是并发或时间。
2. 环境可控边界能在 configuration 层显式分区。
3. 关心的是 branching-time open semantics，而不是单条 trace。

### 不适用或高成本场景

如果系统是 closed 的，plain pushdown model checking 更自然；如果环境被建模成显式双人策略对抗，`RGG` 更贴切；如果只有有限层次复用，则 `Open Hierarchical Modules` 更轻。

## 与相邻形式主义的关系

相对 `Open Hierarchical Modules`，它把有限 hierarchy 推到无界调用栈；相对 `RSM`，它加入了 environment pruning semantics；相对显式 pushdown games，它仍保留 module-checking 的开放环境视角，而不是直接换成赢法语义。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机演化树里的 open-system 分支不会停在 finite hierarchy。一旦需求里同时出现递归子过程和外部不可控选择，就会自然长到 `OPD` 这一层。

### 作为目标形式主义还是中间表示

更适合作为验证导向中间表示，而不是最终工程建模语言。

### 对需求到模型生成的启发

如果需求文本含有“递归服务 + 环境分支裁剪”这类信号，LLM 不应只生成 closed `RSM`，而应考虑 `OPD` 这类 open recursive family。

### 现实限制

它没有工程 DSL 与工业工具生态，主要是 formal verification family。

## 重要的相关工作

### 奠基或前身工作

- [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)
- finite-state `module checking`

### 同类型或同家族工作

- [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)
- [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)：2010 `FMSD` full version。
- [pushdown-module-checking-with-imperfect-information/desc.md](../pushdown-module-checking-with-imperfect-information/desc.md)：把 `OPD` 继续推进到 imperfect-information open pushdown。

## 文献分类总结

- 这篇论文补出了 `Open Hierarchical Modules` 之后的 `OPD` conference origin。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、运行库或纯算法壳文。
- 在当前演化树里，它最适合挂到 `Statecharts -> HSM -> Open Hierarchical Modules -> Open Pushdown Systems / Pushdown Module Checking`，并作为该节点的 2005 会议锚点。
