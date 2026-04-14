# 双向确定性下推自动机语言 / Two Way Deterministic Pushdown Automaton Languages and Some Open Problems in the Theory of Computation

## 基本信息

- 标题：Two Way Deterministic Pushdown Automaton Languages and Some Open Problems in the Theory of Computation
- 中文标题：双向确定性下推自动机语言与计算理论中的若干开放问题
- 作者：Zvi Galil
- 发表：Cornell University Department of Computer Science Technical Report `TR 74-204`, 1974-04；相关会议版见 `SWAT 1974`
- DOI：相关会议版 DOI 为 `10.1109/SWAT.1974.29`；当前技术报告版本本身未单独给出 DOI
- 链接：https://ecommons.cornell.edu/server/api/core/bitstreams/cfd53159-dfe3-4902-bf7f-2f4cbc5ce82b/content
- 形式主义：Two-Way Deterministic Pushdown Automata (2DPDA)
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文未提供实现；机器可处理入口是只读输入 tape、pushdown stack、双向读头与确定性 move relation。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `2dpda / k-dpda` 的配置更新规则与语言类定义。

## 简报

这篇论文研究的主角是 `2DPDA`，即“输入头能在只读 tape 上左右移动”的确定性下推自动机。相比普通一向 `PDA`，它并没有增加第二个栈或额外工作带，而只是把输入头从单向读改成双向读。论文用它统一表述了一批经典开放问题，但更重要的是，它把 `Pushdown Automata` 主干明确分裂出一个稳定的“two-way deterministic”子分支。

- 形式主义定位：`Pushdown Automata` 主干上的双向读头增强分支。
- 构造方式简述：有限控制 + 只读输入带 + pushdown stack + 左/右移动输入头。
- 基础设施与场景简述：原文没有工程标准，但语言类定义、配置语义和复杂度讨论都很清晰，并与 `RAM` 线性时间模拟、counter machine 与 multi-head `PDA` 紧密相连。

```text
输入串 + 双向读头 + 栈 -> 确定性 push/pop + 左/右扫描 -> 2DPDA language
```

## 形式主义定义与核心对象

### 定义对象

论文在第 2 节先定义更一般的 two-way nondeterministic `k`-head `PDA`，再把 `k=1` 且确定性的情形记为 `2dpda`。输入 tape 形如 `¢x$`，只有一个只读头和一个 pushdown stack；每一步根据当前状态、当前扫描符号和栈顶符号确定唯一动作。

### 核心抽象

按论文文字可把 `2DPDA` 保守整理成如下元组：

$$
M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)
$$

其中一步 move 可写成：

$$
\delta(q, a, X) = (q', \beta, m)
$$

这里的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是输入字母表，实际 tape 为 `\{\¢\}\Sigma^*\{\$\}`。
3. `\Gamma` 是栈字母表。
4. `q_0` 是初始状态。
5. `Z_0` 是初始栈底符号。
6. `F` 是接受状态集。
7. `q` 是当前状态。
8. `a` 是当前头下符号，可为普通输入符号或端标记。
9. `X` 是当前栈顶符号。
10. `q'` 是下一状态。
11. `\beta` 是对栈执行“先弹顶，再压入若干符号”后的替代串。
12. `m` 是读头移动方向，论文限定为向左或向右一步，且不能越过端标记。

这一定义是根据原文第 11 页对 `k-npda / k-dpda` 的文字叙述做的保守符号化整理；论文自己也说明，完全形式化的定义可参见其引用文献。

### 一个最小例子与通俗解释

一个最经典的直觉例子是回文语言。`2DPDA` 可以先向右扫描并把前半段信息压栈，再回退并逐步对照；即使只用一个栈和一个输入头，它也能通过“左右来回看输入”完成一些一向 `PDA` 不容易表达的匹配任务。

通俗地说，普通 `PDA` 像一个“一边往前走一边用栈记事”的读者，而 `2DPDA` 则像一个“可以翻回前页再核对”的读者。它没有增加新存储器，但通过双向读头显著改变了能实现的算法风格。

### 运行 / 接受 / 转移语义

若把配置写成：

$$
c = (q, i, \gamma)
$$

那么一步运行可压缩成：

$$
(q, i, X\alpha) \vdash (q', i+m, \beta\alpha)
$$

其中 `\delta(q, w_i, X) = (q', \beta, m)`。

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `i` 是输入头位置。
3. `\gamma = X\alpha` 是当前栈内容，`X` 为栈顶。
4. `w_i` 是当前位置读到的输入符号。
5. `m \in \{-1,+1\}` 表示左移或右移一步。
6. `\beta\alpha` 是更新后的栈内容。
7. `\vdash` 是一步配置转移关系。

论文对语言类的写法是：

$$
2DPDA = \{L \mid L = L(A)\ \text{for some } 1\text{-dpda } A\}
$$

也就是说，`2DPDA` 语言就是由单头双向确定性下推自动机接受的语言类。

### 语义边界

与普通 `PDA` 相比，它增强的是读头能力，不是存储结构；与 multi-head `PDA` 相比，它仍只有一个头；与 counter machine 相比，它保留了真正的栈而不是若干计数器。

### 关键性质与判定边界

论文的主题虽然是开放问题归约，但对模型本体而言，几个关键点非常稳定：

$$
\text{Membership}(M, x):\ x \in L(M)\ ?
$$

$$
\text{2DPDA} \subseteq \text{languages simulable in linear time on RAM}
$$

$$
\text{OpenProblem} \Longleftrightarrow \text{Question about a 2DPDA language}
$$

这些表达中的符号逐项解释如下：

1. `M` 是某个 `2DPDA`。
2. `x` 是输入串。
3. `L(M)` 是 `M` 所接受的语言。
4. `OpenProblem` 指论文中关于 determinism vs. nondeterminism、space/time bounded computation 的经典问题。

原文明确引用 Cook 的结果：`2DPDA` 的 membership problem 可以在 `RAM` 上以线性时间解决。这说明该模型虽然比普通 `PDA` 灵活，但仍保持相当强的算法可处理性。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 有限控制仍然是核心骨架。 |
| 事件 / 触发 | 支持 | 由当前输入符号和栈顶共同触发。 |
| 守卫 / 数据 | 部分支持 | 没有一般变量守卫，但栈和读头位置共同形成条件上下文。 |
| 层次 | 不支持 | 原始模型是平坦控制。 |
| 并发 / 同步 | 不支持 | 单输入头、单栈、单机运行。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散确定模型。 |
| 可执行 / 可验证性 | 强支持 | 配置语义清楚，membership 和复杂度性质可分析。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$M=(Q,\Sigma,\Gamma,\delta,q_0,Z_0,F)$` | 在普通 `PDA` 上加入双向输入头。 |
| 一步配置转移 | `$(q,i,X\alpha)\vdash(q',i+m,\beta\alpha)$` | 同时更新状态、栈和头位置。 |
| 语言类 | `$2DPDA=\{L\mid L=L(A)\text{ for some }1\text{-dpda }A\}$` | 这是该分支最稳定的类定义。 |
| 成员判定 | `$x\in L(M)?$` | Cook 结果说明可在线性时间 `RAM` 上求解。 |
| 归约母体 | `$\text{OpenProblem}\Longleftrightarrow\text{Question about a 2DPDA language}$` | 论文把多个开放问题统一归约到这一模型。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 确定输入字母表与端标记。
2. 定义状态集与栈字母表。
3. 给出由“状态 + 当前符号 + 栈顶”决定的唯一 move。

### 机器可处理承载方式

最直接的承载方式是 transition table / move relation，而不是图形化状态图或标准化文档格式。

### 交换与互操作

它与 one-way `PDA`、counter machine、multi-head `PDA` 和复杂度类之间有强互操作，但没有统一工程交换标准。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是配置语义和语言类定义。
- 仿真/执行支持：可按配置 `(state, head, stack)` 模拟。
- 验证/分析支持：membership、复杂度归约、与其他机器模型的关系是原文重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于经典 pushdown / complexity 交叉理论线。

## 适用场景与需求前提

### 适用场景

适用于输入仍是线性词，但需要“回看输入”和“栈式记忆”共同作用的语言识别问题。

### 需求前提

1. 输入对象仍是线性符号串。
2. 需要无界嵌套记忆。
3. 仅靠一向扫描不够，必须允许双向回看输入。

### 不适用或高成本场景

若需求核心是并发同步、时间约束或连续动力学，这条 `2DPDA` 支线并不合适。

## 与相邻形式主义的关系

相对 `Pushdown Automata`，它把输入头从单向推进改成双向移动；相对 `Multi-Head Finite Automata`，它把多头增强换成“单头 + 栈”；相对 `Visibly Pushdown Languages`，它更底层、更一般，也更偏机器能力讨论。

## 与本研究的关系

### 对 Project 1 的价值

它补出了 `Pushdown Automata` 主干下此前缺失的经典子节点，使演化树不再只沿 `VPL/NWA` 这条结构化词路线展开。

### 作为目标形式主义还是中间表示

通常更适合作为理论分支节点或中间分析模型，而不是控制系统自动建模的默认目标形式。

### 对需求到模型生成的启发

它提示我们：当需求不只是“需要栈”，还需要“反复回看输入历史”时，单纯一向 `PDA` 可能仍然过弱。

### 现实限制

它几乎没有工程标准和通用工具链，在控制系统落地中通常只是理论参考而不是直接产出格式。

## 重要的相关工作

### 奠基或前身工作

- [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)

### 同类型或同家族工作

- multi-head `PDA`
- two-way counter machine
- auxiliary pushdown machine

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具实现。

### 与本研究关系最紧的工作

- 它为 `Pushdown Automata` 主干补出了“输入头增强”这条经典支线。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Two-Way Deterministic Pushdown Automata (2DPDA)
- 论文角色：分支整理
- 核心功能：在 pushdown 自动机上加入双向输入头，形成更强的栈式串语言识别模型。
- 关键特性：双向读头、栈记忆、确定性 move relation、复杂度与归约性质清晰。
- 构造方式：有限控制 + 只读输入 tape + pushdown stack + 左/右移动。
- 基础设施：纯理论模型，无统一工程标准或工具链。
- 适用场景：需要“栈 + 回看输入”共同作用的线性词识别问题。
- 需求前提：对象仍是线性词，且增强点来自双向扫描而非时间/并发。
- 状态：🟢
