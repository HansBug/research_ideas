# 扩展宏文法与栈控制机器 / Extended Macro Grammars and Stack Controlled Machines

## 基本信息

- 标题：Extended Macro Grammars and Stack Controlled Machines
- 中文标题：扩展宏文法与栈控制机器
- 作者：Joost Engelfriet, Giora Slutzki
- 发表：*Journal of Computer and System Sciences*, 29(3):366-408, 1984
- DOI：`10.1016/0022-0000(84)90006-0`
- 链接：https://ris.utwente.nl/ws/files/6563191/Engelfriet84extended.pdf
- 形式主义：`Stack Controlled Machines / Checking-Stack Controlled Machines`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 machine type、存储配置集合、指令集和对应的 `SP(D) / CS(D)` 构造。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是抽象 machine type、宏文法和存储指令语义。

## 简报

这篇论文最值得收进文库的部分，不是宏文法本身，而是它把“栈去控制一个 pushdown of `D`-tapes”的 machine family 明确定义出来，并证明它正好对应 `K`-extended basic macro grammars。对演化树来说，这意味着 `Finite Automata -> 存储增强` 下面不必只停留在 `Pushdown` 和 `Multicounter`；还可以继续长出“用一层 stack 管多层数据存储”的 `Stack-Controlled Machines` 分支。

- 形式主义定位：有限自动机主干上的高阶存储控制模型，介于普通 pushdown 与更深层 nested-stack 家族之间。
- 构造方式简述：从任意 machine type `D` 出发，增加 `push / pop / movedown / moveup` 等控制指令，让一个外层 stack 去控制底层 `D`-tape 的展开与返回。
- 基础设施与场景简述：原文是纯理论工作，但给出了 `SP(D)`、`CSP(D)`、`S(D)`、`CS(D)` 的标准定义，以及与 `B(K)`、`LB(K)` 的精确对应，足以把它当成稳定的模型本体节点。

```text
基础 machine type D -> stack controls pushdown of D-tapes -> SP(D) / CS(D) -> extended macro grammar language classes
```

## 形式主义定义与核心对象

### 定义对象

论文的出发点是“machine type”这一抽象存储骨架，然后在其上定义 stack-controlled family。换言之，`SP(D)` 不是某个固定字母表上的具体自动机，而是“从任意底层存储 `D` 派生出的新机器类型”。

### 核心抽象

原文先把一般 machine type 写成：

$$
D = (S, s_0, S_\infty, Z, m)
$$

上式中的符号逐项解释如下：

1. `S` 是存储配置集合。
2. `s_0` 是初始存储配置。
3. `S_\infty` 是接受时允许的终止存储配置集合。
4. `Z` 是指令集。
5. `m` 把每条指令映成 `S` 上的部分函数。

在此基础上，stack-controlled machine type 可写成：

$$
SP(D) = (S', s_0', S_\infty', I', m')
$$

其中原文给出的配置集合可保守整理为：

$$
S' = \Gamma^* \cup \Gamma^*(\Gamma \times \Gamma \times S)^+\Gamma,\qquad s_0'=\lambda,\qquad S_\infty'=\{\lambda\}
$$

上式中的符号逐项解释如下：

1. `\Gamma` 是外层 stack / pushdown 使用的有限符号集。
2. `\Gamma^*` 表示只有外层 stack、尚未进入下层 `D`-tape 的配置。
3. `(\Gamma \times \Gamma \times S)^+\Gamma` 表示“若干层受 stack 控制的 `D`-tape”被串接在一起的配置形态。
4. `\lambda` 是空栈配置。

对应指令集包含：

$$
I' \supseteq Z \cup \{\mathrm{push}(y), \mathrm{pop}, \mathrm{movedown}(y), \mathrm{moveup}\}
$$

并附带测试：

$$
\mathrm{stackempty},\ \mathrm{pdempty},\ \mathrm{stacksymbol}=y,\ \mathrm{pdsymbol}=y
$$

直观上：

1. `push(y)` / `pop` 操作外层 stack。
2. `movedown(y)` 在当前控制点下方打开一条新的 `D`-tape。
3. `moveup` 从当前下层 `D`-tape 返回上层。
4. 原 `Z` 中的指令始终作用在“当前最低层”的 `D`-tape 上。

### 一个最小例子与通俗解释

一个直观例子是把 `D` 取成“识别局部 regular 片段”的底层机。设想输入里有两个嵌套块：

1. 外层机器先读到一个“进入子任务”的标记，于是执行 `push(y)` 记住返回点。
2. 接着执行 `movedown(y)`，在更低一层打开新的 `D`-tape，专门处理这个子块。
3. 子块处理完后，执行 `moveup` 回到上一层继续处理外层任务。

通俗地说，这个模型像“栈控制栈”，或者“外层有限控制拿一个栈来调度若干底层存储任务”。它不是普通 `PDA` 的单层 push/pop，也不是完全任意的高阶机器，而是有明确层级纪律的受控嵌套存储。

### 运行 / 接受 / 转移语义

若 `M=(Q,\Sigma,I_M,q_0,Q_\infty,\delta)` 是一台类型为 `D` 的机器，则其总配置属于：

$$
Q \times \Sigma^* \times S
$$

接受语义仍然是从初始总配置经若干步转移到达终态配置。对 `SP(D)` 而言，只是把 `S` 替换为更复杂的 `S'`，并把转移动作扩展到控制 stack / pushdown of `D`-tapes 的新指令。

更关键的是语言类对应关系。原文 Theorem 4.5 可压成：

$$
K(SP(D)) = B(K(D))
$$

$$
K(CSP(D)) = LB(K(D)) = H(K(D))
$$

上式中的符号逐项解释如下：

1. `K(D)` 是由 machine type `D` 定义的语言类。
2. `B(K)` 是 `K`-extended basic macro grammars 生成的语言类。
3. `LB(K)` 是线性版本。
4. `H(K)` 是原文讨论的 hyper-AFL 闭包对应语言类。

### 语义边界

这个 family 的重点不是“换一种等价文法写法”，而是把一类稳定的存储结构明确命名出来：

1. 外层有 stack discipline。
2. stack 控制的是下层 `D`-tape，而不是直接的普通字符栈。
3. checking-stack 版本进一步限制了 push、读、pop 的阶段顺序。

### 关键性质与判定边界

论文最重要的形式化价值在于 machine / grammar 双刻画，而不是单条复杂度定理。其核心性质可压成：

$$
LB(K)=H(K)
$$

以及上面的 `K(SP(D))`、`K(CSP(D))` 对应式。这说明：

1. `CS(D)` 正好刻画 full hyper-AFL。
2. `SP(D)` 为更强的 `basic-AFL` 家族提供了具体机器模型。

对演化树而言，这一点比“某个具体判定算法”更重要，因为它给的是稳定家族边界。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然保留有限控制。 |
| 事件 / 触发 | 强支持 | 按输入符号和存储测试驱动。 |
| 守卫 / 数据 | 部分支持 | 通过测试指令访问当前 stack / pushdown / `D`-tape 局部信息。 |
| 层次 | 强支持 | 存储本体就是显式分层的。 |
| 并发 / 同步 | 不支持 | 不是并发网模型。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散语言机。 |
| 可执行 / 可验证性 | 强理论支持 | 与 macro grammar、AFL / hyper-AFL 闭包精确对应。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 底层 machine type | `$D=(S,s_0,S_\infty,Z,m)$` | 把任意存储骨架抽象化。 |
| 栈控制派生 | `$SP(D)=(S',s_0',S_\infty',I',m')$` | 在 `D` 上增加外层 stack 控制。 |
| checking-stack 版本 | `$CSP(D)$` | 把 push/read/pop 分成阶段。 |
| 语言类刻画 | `$K(SP(D))=B(K(D))$` | 机器与扩展 basic macro grammars 对齐。 |
| hyper-AFL 刻画 | `$K(CSP(D))=LB(K(D))=H(K(D))$` | 说明这不是偶然构造，而是稳定家族。 |

## 构造方式与承载格式

### 建模入口

建模时的关键不是先画状态图，而是先回答：

1. 底层存储骨架 `D` 是什么。
2. 是否需要外层 stack 去递归地打开 / 返回这些 `D`-tapes。
3. 是否还要限制成 checking-stack 的单向阶段纪律。

### 机器可处理承载方式

机器可处理承载方式是抽象 machine type、指令集与存储配置，而不是工程图形语言。

### 交换与互操作

它与以下对象互操作最紧：

1. macro grammars / indexed languages。
2. AFL、hyper-AFL、basic-AFL。
3. nested stack automata、bounded nested-stack families。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 machine type 定义、指令语义和 grammar 对应。
- 仿真/执行支持：理论上可直接执行 push / movedown / moveup 语义。
- 验证/分析支持：主要是语言类对应、闭包与家族分层。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 macro grammar / indexed language / nested storage 经典理论线。

## 适用场景与需求前提

### 适用场景

适用于需要“显式分层存储纪律”的语言家族分析，例如超出普通 `PDA`、但又不想直接跳到完全一般高阶机器的场景。

### 需求前提

1. 对象仍然是线性词语言。
2. 需求中的核心难点来自嵌套控制上下文，而不是时间或数据约束。
3. 希望把文法类和机器类一一对齐。

### 不适用或高成本场景

如果目标只是普通上下文无关结构，`PDA` 往往已足够；如果目标是工程控制器建模，这种抽象 machine type 又过于理论化。

## 与相邻形式主义的关系

相对 [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)，它不再是单层 pushdown，而是 stack 去控制更深层的存储对象；相对 [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)，这里的重点是字符串语言与存储机，而不是树变换；相对 `nested stack automata` / indexed languages 传统，这篇给出了更抽象、可组合的 machine-type 版本。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Pushdown` 之上的“受控嵌套存储”节点，使文库的存储增强支线不再只有 `PDA / counter / multi-head` 这几类相对平面的增强。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和语言类桥接层，而不是控制系统需求的默认落地模型。

### 对需求到模型生成的启发

当需求天然表现出“递归上下文里还要管理另一层局部状态”的结构时，模型生成阶段可以把这类受控嵌套存储当作能力上界参考，而不必只在 `FSM/PDA` 两点之间摇摆。

### 现实限制

缺少工程化 DSL 和工具生态；更偏向理论结构整理，不适合直接拿去做工业控制实现。

## 重要的相关工作

### 奠基或前身工作

- [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)
- macro grammars / indexed languages / nested stack automata

### 同类型或同家族工作

- checking-stack machines
- stack-pushdown machines
- bounded nested-stack controlled machines

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为“有限自动机如何走向更深层存储控制”这一分支的经典挂树节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Stack Controlled Machines / Checking-Stack Controlled Machines`
- 论文角色：模型提出
- 核心功能：用外层 stack 去控制 pushdown of `D`-tapes，并与扩展宏文法语言类精确对应。
- 关键特性：抽象 machine type、分层存储、`push/movedown/moveup` 语义、grammar-machine 双刻画。
- 构造方式：从一般 `D` 出发派生 `SP(D)` / `CSP(D)`。
- 基础设施：纯理论承载，无工程标准，但与 macro grammar、indexed language 和 AFL 分层强互操作。

