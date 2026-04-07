# 面向寄存器自动机的灰盒学习 / Grey-Box Learning of Register Automata

## 基本信息

- 标题：Grey-Box Learning of Register Automata
- 中文标题：面向寄存器自动机的灰盒学习
- 作者：Bharat Garhewal，Frits Vaandrager，Falk Howar，Timo Schrijvers，Toon Lenaerts，Rob Smits
- 发表：*Integrated Formal Methods*，`LNCS 12546`，pp. 22-40，2020
- DOI：`10.1007/978-3-030-63461-2_2`
- 链接：https://doi.org/10.1007/978-3-030-63461-2_2
- 形式主义：`register automata learning / taint-guided RALib / grey-box active learning`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：grey-box register-automata learning method / taint-guided active-learning route
- 工具/实现获取方式：原文明确说明方法实现于 `RALib` 的 tree oracle 与 equivalence oracle 扩展之上，并给出 Python tainting 代码入口 `https://bitbucket.org/toonlenaerts/taintralib/src/basic/`；`RALib` 本身为公开学习框架。
- 标准/格式获取方式：主承载对象是 data words、`RA` 元组、tainted words、symbolic decision trees 与 `membership/equivalence queries`；它不是交换标准。

## 简报

这篇论文补的是 `register automata` 学习线里非常关键的一步：把原先纯黑盒的 `MQ/EQ` 学习流程推进成“查询 + tainting 约束观测”的灰盒路线。它没有重新定义新的 `RA` 母型，而是说明只要能在一次程序运行中读出输入输出参数间真正发生过的比较约束，`RALib` 原本最耗查询的 tree oracle 和 equivalence oracle 就能显著提速，并且开始学到组合锁这类纯黑盒几乎够不到的模型。

- 形式主义定位：围绕 `register automata` 的学习方法路线，而不是新的 `RA` 本体。
- 构造方式简述：在 `SL* + RALib` 框架里，把 membership / equivalence 查询返回值从单纯 `yes/no` 扩成“`yes/no + constraints`”，再据此构造 characteristic predicate 和 `SDT`。
- 基础设施与场景简述：依托 `RALib`、Python `tainting`、tree oracle、symbolic decision trees 与 data-word learning，服务带参数接口、数据独立协议和 `RA/EFSM` 风格模型恢复。

```text
SUL + tainting -> tainted MQ/EQ -> characteristic predicate -> symbolic decision tree -> register automaton hypothesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. deterministic register automata；
2. tainted states 与 tainted runs；
3. tainted membership / equivalence queries；
4. characteristic predicates；
5. symbolic decision trees (`SDT`)。

### 核心抽象

论文沿用 `RA` 母型：

$$
M = (L,l_0,X,\Gamma,\lambda)
$$

上式中的符号逐项解释如下：

1. `$L$` 是有限 location 集合。
2. `$l_0$` 是初始 location。
3. `$X$` 为各 location 配置的 register 集合。
4. `$\Gamma$` 是形如 `$\langle l,\alpha(p),g,\pi,l' \rangle$` 的转移集合，其中 `$g$` 是 guard，`$\pi$` 是赋值。
5. `$\lambda$` 给出接受/拒绝标记。

灰盒部分新增的关键对象是 tainted state。原文定义可整理为：

$$
\langle l,\nu,\zeta \rangle
$$

上式中的符号逐项解释如下：

1. `$l \in L$` 是当前 location。
2. `$\nu : X(l) \to D$` 给出当前 register valuation。
3. `$\zeta : X(l) \to V$` 给出每个 register 当前携带的 taint marker。
4. `$D$` 是数据域。
5. `$V$` 是 marker 域；同一 data word 里每个输入位置都会得到唯一 marker。

对应的 tainted run 可写成：

$$
\tau = \langle l_0,\nu_0,\zeta_0 \rangle \xrightarrow{\alpha_1(d_1),g_1,\pi_1} \cdots \xrightarrow{\alpha_n(d_n),g_n,\pi_n} \langle l_n,\nu_n,\zeta_n \rangle
$$

上式中的符号逐项解释如下：

1. `$\alpha_i(d_i)$` 是第 `$i$` 个带数据参数的动作。
2. `$g_i$` 是该步执行时被满足的 guard。
3. `$\pi_i$` 是该步 register 更新。
4. `$\zeta_i = \kappa_i \circ \pi_i$` 表示 taint marker 随赋值同步传播。
5. 因而 tainting 不只知道“这步是否接受”，还知道“这步 guard 到底比较了哪些先前输入”。

论文把一次 tainted run 上收集到的约束压成：

$$
M(\tau) = [G_1,\ldots,G_n]
$$

上式中的符号逐项解释如下：

1. `$G_i$` 是第 `$i$` 步由 tainting 观测得到的 guard 约束实例。
2. 这些约束是把原 guard 中的参数位置替换成 marker 后得到的谓词。
3. 由于论文关注 deterministic `RA`，对 data word `$w$` 有唯一 tainted run，因此也可写 `$M(w)$`。
4. 这正是 tainted membership query 相比普通 membership query 的新增信息。

对 tree query `$(u,w)$`，论文进一步把 characteristic predicate 写成：

$$
\nu \models H \iff \alpha_1(\nu(x_1)) \cdots \alpha_{k+n}(\nu(x_{k+n})) \in L(M)
$$

上式中的符号逐项解释如下：

1. `$u=\alpha_1(d_1)\cdots\alpha_k(d_k)$` 是具体前缀。
2. `$w=\alpha_{k+1}\cdots\alpha_{k+n}$` 是 symbolic suffix。
3. `$\nu$` 是对 `$x_1,\ldots,x_{k+n}$` 的 valuation，并且扩展了前缀 `$u$` 的具体数据。
4. `$H$` 是对“哪些 suffix 参数使 `$u \cdot w$` 可接受”的谓词化表示。
5. 论文用 tainted queries 直接构造 `$H$`，再从 `$H$` 构出 `SDT`。

### 一个最小例子与通俗解释

论文给出的 `FIFO buffer` 例子很适合解释这种模型：

1. 先执行 `Push(7)`，buffer 记住值 `7`。
2. 再执行 `Push(7)`，第二个槽位也装入 `7`。
3. 当后面出现 `Pop(7)` 时，真正生效的 guard 是“当前参数是否等于先前寄存器里记住的值”。
4. tainting 会把这一步记录成类似 `$v_3 = v_1$` 的约束，而不是只返回“yes”。

通俗地说，普通黑盒学习只知道“这串输入通过了还是没通过”，灰盒学习则进一步知道“为什么通过，是因为这一步拿到的参数刚好和第一次 `Push` 的值相等”。对带数据守卫的状态机，这个差别非常大。

### 运行 / 接受 / 转移语义

论文的核心运行语义是：普通 `RA` run 依然按 guard 和 assignment 前进，但每一步还额外输出一组 marker-level 约束给学习器。于是：

1. tainted membership query 返回 `yes/no + constraints`；
2. characteristic predicate 由这些 constraints 累积构造；
3. `SDTConstructor` 再把 characteristic predicate 变成非最简 `SDT`；
4. minimization 算法把它压成最终 `SDT`。

论文附录中的关键正确性主张可保守写成：

$$
SDT_{\mathrm{tainted}}(u,w) \cong SDT_{\mathrm{plain}}(u,w)
$$

上式中的符号逐项解释如下：

1. `$SDT_{\mathrm{tainted}}(u,w)$` 是 tainted tree oracle 生成的决策树。
2. `$SDT_{\mathrm{plain}}(u,w)$` 是原始黑盒 tree oracle 生成的决策树。
3. `$\cong$` 表示论文中证明的 isomorphism。
4. 这意味着 tainting 改进的是效率和可学习范围，而不是偷偷换了目标语义。

### 语义边界

1. 论文主线仍落在 deterministic `RA` 学习，不是一般带算术约束的 `EFSM` 全谱。
2. tainting 只能记录实际执行中发生过的比较；像外层 `not` 这类不直接落在 `tstr` 比较上的结构，原文明确说不会自动被记录。
3. 原型实现重点围绕 Python 和 equality/inequality 数据关系展开，更丰富理论仍需额外工程化。
4. 它需要 query access，不适合只有静态需求文本而没有可执行对象的场景。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RA` 母型 | `$M=(L,l_0,X,\Gamma,\lambda)$` | 目标学习对象仍是标准寄存器自动机。 |
| tainted state | `$\langle l,\nu,\zeta \rangle$` | 在 valuation 之外再显式跟踪 taint marker。 |
| tainted constraints | `$M(\tau)=[G_1,\ldots,G_n]$` | 一次运行中实际发生的参数关系被显式返回。 |
| characteristic predicate | `$\nu \models H \iff u\cdot w \in L(M)$` | 学习器据此重建 `SDT`。 |
| 正确性主张 | `$SDT_{\mathrm{tainted}}(u,w) \cong SDT_{\mathrm{plain}}(u,w)$` | tainted oracle 与原 oracle 在语义上同构。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 目标就是恢复带有限 locations 的 `RA`。 |
| 事件 / 触发 | 很强 | 输入动作带数据参数，是学习主轴。 |
| 守卫 / 数据 | 很强 | 灰盒价值几乎全部来自 guard / register 约束恢复。 |
| 层次 | 不支持 | 不处理层次状态机。 |
| 并发 / 同步 | 弱支持 | 论文目标是单组件或单接口 `SUL`。 |
| 时间约束 | 不支持 | 不是 timed-learning 路线。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散数据语言学习。 |
| 可执行 / 可验证性 | 很强 | `RALib + Python tainting` 已有原型和 benchmark。 |

### 形式化问题与性质

1. 论文真正解决的是“如何更便宜地恢复数据守卫”，而不是“如何定义新 automaton”。
2. 与纯黑盒 `MQ/EQ` 相比，grey-box 返回的 constraints 让 suffix 探测更快定位寄存器依赖。
3. 文中报告在多个 benchmark 上发送给 `SUT` 的输入符号数可下降近两个数量级。
4. 它还能学到组合锁这类纯黑盒 equivalence oracle 很难随机撞出的模型。

## 构造方式与承载格式

### 建模入口

建模入口主要有三类：

1. 可执行 query 的 `SUL`；
2. data words；
3. 运行期 tainting 观测到的 parameter constraints。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `RA` 元组；
2. tainted words；
3. characteristic predicates；
4. symbolic decision trees；
5. `RALib` 内部的 tree/equivalence oracle 数据结构。

### 交换与互操作

这篇论文的互操作重点不在文件格式，而在学习接口：

1. learner 通过 `MQ/EQ` 与 `SUL` 交互；
2. tainting 把程序运行约束回传给 oracle；
3. `RALib` 则把这些约束转成 `SDT` 与 `RA` hypothesis。

## 配套基础设施

- 建模/编辑工具：不主打图形建模，核心是 `RALib`、Python `taintedstr` 和 learning benchmark。
- 解析/交换/元模型支持：data words、tainted words、`RA` 元组、symbolic suffix 与 `SDT`。
- 仿真/执行支持：通过 membership / equivalence queries 与可执行 `SUL` 交互。
- 验证/分析支持：tainted tree oracle、tainted equivalence oracle、counterexample-guided refinement。
- 代码生成/转换支持：不面向部署代码生成，重点是从行为恢复结构化状态机。
- 标准化或社区生态：依托 `RALib`、主动自动机学习社区与公开 tainting 原型。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 带数据参数的 API、协议、库接口行为恢复；
2. 想从实现侧恢复 `RA/EFSM` 再做对照验证或回归分析；
3. 需要比纯黑盒学习更高效地定位 equality-style guards 的场景。

### 需求前提

1. 目标系统必须可被 query 驱动访问。
2. 关键交互要能压成 data words。
3. 程序运行时应能注入或观测 taint 信息。
4. 数据理论最好主要围绕 equality / inequality，而不是复杂算术。

### 不适用或高成本场景

若目标只有自然语言需求而无可执行对象、或者 guard 依赖复杂数值关系与外部环境连续变量，这条路线的收益会显著下降。

## 与相邻形式主义的关系

相对 [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)，本文更具体地把 white-box 信息落成 tainting 约束，而不只是一般性的黑白盒融合；相对 [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)，本文不是 classification-tree 路线，而是直接加速 `RALib` 既有 oracle；相对 [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)，本文强调的是数据守卫恢复效率，而不是 `LearnLib Studio` 式展示性 workflow。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明需求生成之外，还可以从实现运行痕迹回收 guard-level 证据，用来校验或修复 LLM 生成模型。
2. 对控制逻辑里“状态少、数据守卫难”的对象，这类灰盒学习尤其有价值。
3. tainted constraints 也很像后续“生成-验证-修复”闭环中修复阶段需要的反例解释材料。

### 作为目标形式主义还是中间表示

更适合作为从实现恢复模型、校正模型和补证模型的中间表示，而不是领域工程师直接手写的前端语言。

### 对需求到模型生成的启发

1. 数据守卫不能只靠离散结构猜测，最好能结合执行证据。
2. 若后续要自动修复状态机，保存“哪条 guard 真实比较了哪些历史值”很重要。
3. `RA` 与 `EFSM` 型控制对象很适合把 query 证据层引入 LLM 闭环。

## 重要的相关工作

1. [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)：更一般地讨论黑盒与白盒融合的 `RA` 学习。
2. [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)：`RA` 学习从 observation-table 向 classification-tree 继续演化的代表路线。
3. [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)：`RA` 学习基础设施和 workflow 演示入口。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`register automata learning / taint-guided RALib / grey-box active learning`
- 论文角色：grey-box register-automata learning method / taint-guided active-learning route
- 归类理由：论文主体贡献在于 `RA` 学习算法的 oracle 增强与 taint-guided guard 恢复，不是新的标准、运行时或语言本体。
