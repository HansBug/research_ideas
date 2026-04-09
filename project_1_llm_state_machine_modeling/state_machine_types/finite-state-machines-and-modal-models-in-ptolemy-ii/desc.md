# Ptolemy II 中的有限状态机与模态模型 / Finite State Machines and Modal Models in Ptolemy II

## 基本信息

- 标题：Finite State Machines and Modal Models in Ptolemy II
- 中文标题：Ptolemy II 中的有限状态机与模态模型
- 作者：Edward A. Lee
- 发表：Technical Report No. UCB/EECS-2009-151, University of California at Berkeley, 2009
- DOI：原文未提供
- 链接：https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-151.html
- 形式主义：Ptolemy II FSMActor / ModalModel
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：工具教程
- 工具/实现获取方式：论文提供 Ptolemy II 在线可运行示例入口，并以 `Ptolemy II` 作为直接实现载体。
- 标准/格式获取方式：原文明确给出图形表示、`MoML` 结构和 Java API，说明其机器可处理承载来自 Ptolemy II 框架本身。

## 简报

这份技术报告把 `FSM` 和 `modal model` 真正变成了异构系统建模框架中的一等 actor。`FSMActor` 负责 guards / output actions / set actions，`ModalModel` 则在状态上挂 refinement，并要求 refinement 自身带 compatible director。它的重点不是又定义一个新状态机，而是说明“在异构 timed/untimed 计算域里，状态机和 mode refinement 应该怎样执行”。

- 形式主义定位：Ptolemy II 中面向异构嵌入式/CPS 的状态机与模态执行框架。
- 构造方式简述：用状态、transition、guard、output action、set action 构造 `FSMActor`，再给 mode 绑定 refinement 构成 `ModalModel`。
- 基础设施与场景简述：直接依赖 Ptolemy II、MoML、Java API 和 director 机制，适合多计算模型协同的嵌入式与 CPS。

```text
模式切换需求 -> FSMActor / ModalModel -> refinement + compatible director -> timed / untimed 异构执行
```

## 形式主义定义与核心对象

### 定义对象

报告同时讲两件事：

1. 如何把一个 actor 的行为写成状态机。
2. 如何让状态机的不同状态承载不同 refinement，从而形成 mode-based heterogeneous model。

### 核心抽象

报告先回顾了扩展状态机模型，把 Ptolemy II 的状态机写成：

$$
E = (S, I, O, T, s, V)
$$

并指出对确定性扩展状态机有：

$$
T : S \times I \times V \to S \times O \times V
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集合。
2. `I` 是输入端口取值空间。
3. `O` 是输出端口取值空间。
4. `T` 是转移函数，由 guards、output actions、set actions 编码。
5. `s` 是初始状态。
6. `V` 是局部变量赋值空间。

对于 modal model，原文没有单独给统一元组，这里按其结构做一个**保守整理**：

$$
MM = (E, R, D)
$$

其中：

1. `E` 是控制该 modal model 的扩展状态机。
2. `R : S \to \mathcal{M}` 把每个 state 映射到一个 refinement。
3. `D` 表示 refinement 中 director 的兼容性约束。

### 一个最小例子与通俗解释

报告最直观的例子是 thermostat：

1. 两个状态：`heating` 和 `cooling`。
2. 输入 `temperature`，输出 `heat`。
3. 在 `heating` 中，温度低于 `heatOffThreshold` 时继续加热。
4. 在 `cooling` 中，温度低于 `heatOnThreshold` 时重新切回加热。

如果换成 modal model，则每个 mode 不只是“一个状态名”，而是一个完整 refinement，例如 `clean` 和 `noisy` 两个通信通道模式，各自有不同的内部 actor 图。

通俗解释是：`Ptolemy II` 里的 modal model 像“用状态机来切不同的小系统”。状态机只负责决定当前在哪个 mode，真正做事的是该 mode 下挂的 refinement。

### 运行 / 接受 / 转移语义

对 `FSMActor`，报告把一次执行拆成 `fire()` 与 `postfire()`：

1. 读输入。
2. 评估当前状态所有 outgoing transitions 的 guards。
3. 选出一个为真的 transition。
4. 执行该 transition 的 output actions。
5. 在 `postfire()` 中执行 set actions。
6. 最后把当前状态更新为目标状态。

可压缩成：

$$
(s, i, v) \xRightarrow{\mathrm{fire/postfire}} (s', o, v')
$$

在 fixed-point domain 中，这种拆分是必须的，因为 actor 可能在一次迭代中被多次 `fire()`，但只能在固定点收敛后真正 commit 状态改变。

时间语义方面，报告明确给出 Ptolemy 的事件标签：

$$
\mathrm{tag}(e) = (t, n) \in \mathbb{R} \times \mathbb{N}
$$

其中：

1. `t` 是 time stamp。
2. `n` 是 microstep。

报告反复强调 modal model 的关键时间规则：当某个 mode inactive 时，local time stands still。保守整理可写成：

$$
\tau_{\mathrm{local}}' = \tau_{\mathrm{local}} \quad \text{when mode is inactive}
$$

因此 mode 被重新激活时，其内部 timed actor 会从停住的 local time 继续，而不是按 global time 跳过。

### 语义边界

`Ptolemy II` 的强项在于 heterogeneous execution，因此它的语义也比普通状态机重很多：

1. 状态机是否 reactive / spontaneous，取决于所处 timed domain。
2. refinement 是否能工作，取决于内部 director 与外部 director 的兼容性。
3. 同一个 formalism 在不同 domain 下可能出现 fixed-point、microstep、local time 等差异。

所以它不是“一个轻量自动机定义”，而是“一个嵌入框架中的状态机语义家族”。

### 关键性质与判定边界

报告给出几个特别关键的工程性质：

1. nondeterministic transitions 必须显式标注，否则多条 guard 同时为真会报错。
2. default transitions 只有在其它非 default transitions 都不使能时才会被考虑。
3. timed modal model 中，reactive outputs 与输入同 time stamp；spontaneous outputs 可在无输入时出现，但仍通过 `(t,n)` 标签排序。

可以把 reactive 输出压成：

$$
\mathrm{stamp}(o) = \mathrm{stamp}(i)
$$

而 spontaneous mode 的关键现象则是：

$$
\mathrm{tag}(e_1) = (t, n), \qquad \mathrm{tag}(e_2) = (t, n+1)
$$

也就是同一 time stamp 下通过 microstep 明确顺序。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `FSMActor` 和 `ModalModel` 都以显式 state/mode 为核心。 |
| 事件 / 触发 | 强支持 | guards 直接依赖输入事件与变量。 |
| 守卫 / 数据 | 强支持 | guard、output action、set action 都可引用输入和参数。 |
| 层次 | 强支持 | mode 可以挂 refinement，形成层次模型。 |
| 并发 / 同步 | 部分支持 | 并发主要来自 refinement 内部 director，而不是状态机本体。 |
| 时间约束 | 强支持 | `tag=(t,n)`、local time、preemptive transition 都是核心内容。 |
| 连续动态 / 随机性 | 部分支持 | 依赖 refinement 中的 actor 与 director，可承载连续/随机组件。 |
| 可执行 / 可验证性 | 强支持 | 直接服务于 Ptolemy II 可执行模型构建。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 扩展状态机 | `$E = (S,I,O,T,s,V)$` | 状态机不只看状态，还显式包含输入/输出和局部变量。 |
| 转移函数 | `$T : S \times I \times V \to S \times O \times V$` | guard、输出动作和 set action 联合决定下一步。 |
| fire/postfire 语义 | `$(s,i,v)\xRightarrow{\mathrm{fire/postfire}}(s',o,v')$` | 固定点域中输出生成与状态提交必须分离。 |
| 事件标签 | `$\mathrm{tag}(e)=(t,n)$` | 同一时间戳下用 microstep 表示先后顺序。 |
| reactive 输出 | `$\mathrm{stamp}(o)=\mathrm{stamp}(i)$` | 反应式状态机在 timed domain 中看起来“零时间反应”。 |
| 冻结 local time | `$\tau_{\mathrm{local}}'=\tau_{\mathrm{local}}$ when inactive` | mode 非激活时其内部时间不会前进。 |

## 构造方式与承载格式

### 建模入口

建模入口是 Ptolemy II 图形编辑器中的 states、transitions、mode refinements 和 directors。用户直接配置 guard、outputActions、setActions。

### 机器可处理承载方式

报告给出三层承载方式：

1. 图形化状态图。
2. `MoML` XML 结构。
3. Java API 创建 `FSMActor`、`State`、`Transition` 的程序化方式。

### 交换与互操作

互操作核心在于 director compatibility。一个 mode refinement 能否被挂到 modal model 上，不只看它是不是模型，还看它的 director 能不能和外层执行域一起工作。

## 配套基础设施

- 建模/编辑工具：Ptolemy II 图形建模环境。
- 解析/交换/元模型支持：`MoML` 和 Java API 都是明确入口。
- 仿真/执行支持：这是报告主体，包含 timed / untimed、reactive / spontaneous 等语义。
- 验证/分析支持：报告更强调执行语义与建模方法，不主打独立 model checking。
- 代码生成/转换支持：原文未把代码生成当核心。
- 标准化或社区生态：依托 Ptolemy II actor + director 生态，而非跨厂商交换标准。

## 适用场景与需求前提

### 适用场景

适合异构嵌入式系统、CPS、多计算模型协同系统，尤其是不同 mode 下需要不同内部模型和执行语义的场景。

### 需求前提

1. 需求中存在显式 mode switching。
2. 各 mode 内部行为适合用不同 refinement 表达。
3. 系统需要和 timed domain、microstep 或 director 语义协同。

### 不适用或高成本场景

若只需要一个轻量、可移植、标准化的状态机文件格式，`Ptolemy II` 太重；若研究问题关注可判定性而非框架执行，`Ptolemy` 也不是最干净的理论核心。

## 与相邻形式主义的关系

相对 `SCXML`，它更像执行框架而不是交换标准；相对 `Statecharts`，它把层次 state 变成 refinement actor；相对 `Hybrid Automata`，它提供的是工程执行环境，而不是单一连续-离散统一语义。

## 与本研究的关系

### 对 Project 1 的价值

它证明了一条重要路线：状态机完全可以不是最终工件本身，而是“切不同计算域 refinement 的控制器”。这对后续把 LLM 生成的状态机接到异构仿真/执行环境里很有参考价值。

### 作为目标形式主义还是中间表示

如果研究目标是进入 Ptolemy II / actor-oriented 工具链，它可以直接是目标形式主义；否则更适合作为实现载体或执行后端。

### 对需求到模型生成的启发

当需求存在“模式不同，内部算法/模型也完全不同”时，直接生成带 refinement 的 modal model 比只生成平面状态图更贴近工程语义。

### 现实限制

它的表达力很强，但语义强绑定 Ptolemy II 框架与 director 机制，因此抽象比较和跨工具迁移成本较高。

## 重要的相关工作

### 奠基或前身工作

- 经典 `FSM`
- 扩展状态机

### 同类型或同家族工作

- modal model / mode-based design 路线
- actor-oriented modeling

### 标准 / 格式 / 工具链工作

- `MoML`
- Ptolemy II directors / actors

### 与本研究关系最紧的工作

- 面向异构控制系统的模式切换执行载体。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：Ptolemy II FSMActor / ModalModel
- 论文角色：工具教程
- 核心功能：用状态机控制 refinement 切换，并在异构 director 语义下执行。
- 关键特性：guard/output/set action、mode refinement、microstep、冻结 local time。
- 构造方式：图形状态图 + refinement actor + MoML / Java API。
