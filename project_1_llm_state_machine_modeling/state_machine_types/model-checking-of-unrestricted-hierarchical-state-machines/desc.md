# 无约束层次状态机的模型检验 / Model Checking of Unrestricted Hierarchical State Machines

## 基本信息

- 标题：Model Checking of Unrestricted Hierarchical State Machines
- 中文标题：无约束层次状态机的模型检验
- 作者：Michael Benedikt, Patrice Godefroid, Thomas W. Reps
- 发表：*Automata, Languages and Programming*, pp. 652-666, 2001
- DOI：`10.1007/3-540-48224-5_54`
- 链接：https://doi.org/10.1007/3-540-48224-5_54
- 形式主义：`Unrestricted Hierarchical State Machines (uHSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 component-structure 集合、nodes / boxes / entries / exits、call / return nodes、Kripke-style expansion `K(M)` 与 `LTL/CTL/CTL*` model-checking 任务。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 unrestricted component tuple、recursive box calls、possibly infinite Kripke expansion 与 pushdown / context-free correspondence。

## 简报

这篇论文做的关键增强只有一句话：把 `HSM` 上“box 只能引用更低层组件”的限制去掉。结果是 hierarchy 不再只是有界层次复用，而变成了真正能递归调用自己的状态机族。作者因此得到 `uHSM`，并明确证明 single-exit 版本与 context-free processes 等价、multiple-exit 版本与 pushdown processes 等价。对当前演化树来说，这篇文献的意义在于把 `HSM` 和 `RSM / pushdown` 之间那条“递归化”过渡线写得更清楚。

- 形式主义定位：`HSM` 的递归化、Kripke-structure 化扩展，也就是 hierarchy 从有界 DAG 走向真正 recursive call graph 的节点。
- 构造方式简述：模型由若干 component structures 组成；每个 component 里有 nodes、boxes、entry / exit、call / return nodes 与 edge relation；box 可以指向任意 component，包括递归地指回自己。
- 基础设施与场景简述：纯理论条目，但直接把 `uHSM` 对应到 context-free / pushdown process，并给出 `LTL` 与 `CTL*` 的改进复杂度。

```text
hierarchical control graph -> recursive box calls -> infinite Kripke expansion -> context-free / pushdown correspondence -> temporal model checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 unrestricted `HSM` 定义成一组 component structures。与普通 `HSM` 最大不同在于：box 的索引函数不再要求“只能指向更低层编号”，因此调用图可以递归。

### 核心抽象

原文给出的 `uHSM` 写作：

$$
M = \{M_1,\ldots,M_n\}
$$

其中每个 component structure

$$
M_i = (N_i,B_i,I_i,O_i,X_i,Y_i,C_i,R_i,E_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes 集合。
3. `I_i \subseteq N_i` 是 entry nodes。
4. `O_i \subseteq N_i` 是 exit nodes。
5. `X_i : N_i \to 2^P` 给节点打 atomic propositions 标签。
6. `Y_i : B_i \to \{1,\ldots,n\}` 指出 box 调用哪个 component。
7. `C_i` 是 call-nodes，形如 `(b,e)`，表示通过 box `b` 进入被调 component 的某个 entry `e`。
8. `R_i` 是 return-nodes，形如 `(b,z)`，表示 box `b` 的某个 exit `z` 返回点。
9. `E_i` 是边关系，源点可以是普通节点或 return-node，终点可以是普通节点或 call-node。

它的 expansion 是一个可能无限的 Kripke 结构：

$$
K(M) = (S,R,L)
$$

其中状态集满足：

$$
S \subseteq N \times B^*
$$

这里的符号逐项解释如下：

1. `N` 是所有普通节点的并集。
2. `B^*` 是由若干 boxes 组成的有限上下文序列，也就是调用栈。
3. 因为允许递归，`K(M)` 一般是无限状态的。

### 一个最小例子与通俗解释

原文 Figure 1 的典型例子是“重发式消息发送器”：

1. 顶层结构 `M_1` 里有一个 box 调用 `M_2`。
2. `M_2` 负责一次发送尝试。
3. 如果超时仍没有收到确认，`M_2` 会再通过某个 box 递归调用 `M_2` 自己。

通俗地说，`uHSM` 就像“允许子状态机反复调用自己”的层次状态机。普通 `HSM` 只是有限层次抽屉；`uHSM` 则多了一个真正的调用栈，所以会长出无限的全局展开图。

### 运行 / 接受 / 转移语义

原文的 expansion `K(M)` 用“当前节点 + box 上下文”表示状态。可压成：

$$
(v,w) \in N \times B^*
$$

上式中的符号逐项解释如下：

1. `v` 是当前最内层普通节点。
2. `w` 是有限 box 序列，记录当前所处的调用上下文。

若当前边进入一个 call-node `(b,e)`，则语义上相当于压栈进入：

$$
(v,w) \to (e,wb)
$$

若当前在某个被调 component 的 exit `z` 处返回，则语义上相当于沿相应 return-node 退栈：

$$
(z,wb) \to (v',w)
$$

因此，`uHSM` 的运行语义已经具有典型 call-return stack flavor。

### 语义边界

这篇论文明确划出了几条分界：

1. single-entry 与 multiple-entry 的表达力相同，但 concise 程度不同。
2. single-exit 与 multiple-exit 的表达力不同。
3. single-exit `uHSM` 与 context-free processes 同层。
4. general multiple-exit `uHSM` 与 pushdown processes 同层。

### 关键性质与判定边界

原文最重要的对应关系可以压成：

$$
\text{single-exit } uHSM \simeq \text{context-free processes}
$$

以及

$$
\text{multiple-exit } uHSM \simeq \text{pushdown processes}
$$

这里的 `\simeq` 表示文中通过 bisimulation / 线性时间可构造给出的表达力对应。

在验证复杂度上，原文给出的新结果包括：

$$
\mathrm{MC}_{LTL}(uHSM) \text{ for single-entry multiple-exit machines can be linear in } |M|
$$

以及

$$
\mathrm{MC}_{CTL^*}(uHSM) \text{ for single-exit machines can be linear in } |M|
$$

这说明：一旦接口形状受控，即便系统因为递归而具有无限展开图，也仍能保留相当强的可分析性。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | component structure + boxes 是骨架。 |
| 事件 / 触发 | 支持 | 通过边与 call / return nodes 表达。 |
| 守卫 / 数据 | 不支持 | 原文主体不涉及变量。 |
| 层次 | 强支持 | `HSM` 基础能力被完整保留。 |
| 并发 / 同步 | 不支持 | 主线仍是 sequential。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、cycle detection、`LTL/CTL/CTL*` 都进入分析。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `uHSM` 总体 | `$M=\{M_1,\ldots,M_n\}$` | 若干 component structures 的集合。 |
| component tuple | `$M_i=(N_i,B_i,I_i,O_i,X_i,Y_i,C_i,R_i,E_i)$` | recursive hierarchy 的 canonical 骨架。 |
| expansion | `$K(M)=(S,R,L)$` | 可能无限的 Kripke expansion。 |
| global state | `$(v,w)\in N\times B^*$` | 当前节点 + 调用上下文。 |
| 表达力对应 | `$\text{single-exit }uHSM \simeq \text{CFP}$`，`$\text{multiple-exit }uHSM \simeq \text{PDS}$` | 把 hierarchy-recursion 主线接到 context-free / pushdown。 |

## 构造方式与承载格式

### 建模入口

1. 先定义若干 component structures。
2. 为每个 structure 固定 entry / exit 接口。
3. 再通过 boxes 定义 call graph。
4. 如果需要递归，允许某些 boxes 指向自己或形成循环调用。

### 机器可处理承载方式

原文的机器可处理承载方式主要是：

1. component tuple；
2. call / return nodes；
3. Kripke-style recursive expansion；
4. temporal model-checking reductions。

### 交换与互操作

它在谱系上承担桥梁作用：

1. 往前承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 non-recursive `HSM`。
2. 往旁边对应 pushdown / context-free process。
3. 往后可与 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 对照理解为“更 Kripke 化、更一般接口形状的递归层次家族”。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component tuple 与 recursive expansion。
- 仿真/执行支持：可通过 `K(M)` 的 Kripke expansion 解释。
- 验证/分析支持：reachability、cycle detection、`LTL`、`CTL`、`CTL*`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要与 pushdown / program-analysis 社区相连。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归控制流或过程调用主导的 reactive system。
2. 需要明确 call / return 上下文而不是仅有有限层次复用。
3. 需要把 hierarchy 与 context-free / pushdown 理论精确接起来。

### 需求前提

1. 系统仍以 sequential 控制为主。
2. 递归调用才是主要结构复杂度来源。
3. 接口可以通过有限 entry / exit 与 call / return nodes 表达。

### 不适用或高成本场景

如果系统没有 recursion，只是有限层次结构，则普通 `HSM` 更直接；如果需要变量作用域、history 与 black-box mode semantics，则 `HRM` 支线更合适。

## 与相邻形式主义的关系

相对普通 `HSM`，`uHSM` 去掉了 acyclic-call 限制；相对 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 的 `RSM`，它更偏 Kripke / call-return graph 视角，且多入口/多出口层次更一般；相对 pushdown systems，它保留了更直观的 state-machine / box 结构。

## 与本研究的关系

### 对 Project 1 的价值

它有助于把当前层次状态机演化树从“有限 hierarchy”再向前推进一步，说明 hierarchy 一旦递归化，为什么会自然接上 pushdown / recursive-control 家族。

### 作为目标形式主义还是中间表示

更适合作为高表达力中间表示或理论比较节点，而不是工程最终语言。

### 对需求到模型生成的启发

如果需求文本里已经出现“过程再次进入同类子过程”“返回到调用点后继续执行”这类 call-return 结构，LLM 不应只停留在普通 `HSM`，而应考虑递归层次模型。

### 现实限制

它的工程工具生态很弱，而且由于无限展开图的存在，更适合理论分析而不是直接作为工业图形语言。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)

### 同类型或同家族工作

- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)
- context-free / pushdown processes 相关文献是它的理论对照物。

## 文献分类总结

- 这篇论文严格属于 `HSM` 主枝的递归化模型扩展，而不是单纯验证算法论文。
- 它对当前文库最大的价值，是提供了一个能直接挂在“层次状态机支线”上的 classic recursive node。
- 在演化树中，它最适合作为 `HSM` 向 `RSM / pushdown-style recursive hierarchy` 过渡时的中间说明节点。
