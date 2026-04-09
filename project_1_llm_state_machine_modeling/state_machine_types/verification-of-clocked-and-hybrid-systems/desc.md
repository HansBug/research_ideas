# 时钟化系统与混成系统的验证 / Verification of Clocked and Hybrid Systems

## 基本信息

- 标题：Verification of Clocked and Hybrid Systems
- 中文标题：时钟化系统与混成系统的验证
- 作者：Yonit Kesten, Zohar Manna, Amir Pnueli
- 发表：*Acta Informatica*, 36:836-912, 2000
- DOI：`10.1007/PL00013496`
- 链接：https://cs.nyu.edu/home/people/in_memoriam/pnueli/kmp00.pdf
- 形式主义：`Clocked Transition Systems / Phase Transition Systems`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供统一下载包；机器可处理入口是 `CTS` 的 `$\mathcal C=(V,\Theta,T,\Pi)$`、`tick` 扩展迁移，以及 hybrid 扩展 `PTS` 的 `$\mathcal P=(V,\Theta,T,A,\Pi)$`。
- 标准/格式获取方式：原文没有 XML / DSL 标准，核心承载方式是 clocked / phase transition tuples、verification diagrams 和 non-zeno proof rules。

## 简报

这篇论文的核心贡献是把早期 `Timed Transition Systems` 线继续整理成一个更适合证明的实时模型：`Clocked Transition Systems (CTS)`。它用一组显式 clocks 加上 master clock `T` 取代了旧式“时间只是外部参数”的处理方式，并引入专门的 `tick` 迁移表示时间流逝。更重要的是，论文最后把这条线自然扩展到 `Phase Transition Systems (PTS)`，于是 `CTS` 成为 `Timed Transition Systems` 与 `PTS` 之间非常关键的中间节点。对当前演化树来说，它正好补齐了 `Timed Transition Systems -> Clocked Transition Systems` 这条经典 transition-system 支线。

- 形式主义定位：`Timed Transition Systems` 的 proof-oriented 发展型子枝，并在同文中回接 `Phase Transition Systems`。
- 构造方式简述：用 clocks + master clock `T` + `tick` transition 建模时间流逝，用 activities 把 `CTS` 扩成 `PTS`。
- 基础设施与场景简述：verification diagrams、safety / liveness rules、non-zeno proof，以及对 hybrid systems 的 invariance rule 是本文的主要基础设施。

```text
timed transition system -> explicit clocks + tick -> clocked transition system -> activities/integrators -> phase transition system
```

## 形式主义定义与核心对象

### 定义对象

`CTS` 面向 real-time systems，`PTS` 面向 hybrid systems。前者强调 clocks 和 proof rules，后者在同一骨架上加入 integrators 与 activities。

### 核心抽象

论文定义的 `CTS` 是：

$$
\mathcal C = (V,\Theta,T,\Pi)
$$

上式中的符号逐项解释如下：

1. `V = D \cup C`，其中 `D` 是离散变量集合，`C` 是 clocks 集合。
2. `\Theta` 是初始条件，并要求所有 clocks 初始为 `0`。
3. `T` 是有限 transition 集，每个 transition 都有自己的 transition relation。
4. `\Pi` 是 time-progress condition。

在此基础上，论文把 hybrid 扩展写成：

$$
\mathcal P = (V,\Theta,T,A,\Pi)
$$

这里 `A` 是 activities 集；在 `PTS` 中，`V` 被拆成离散变量和 integrators，master clock `T` 也被看作特殊 integrator。

### 一个最小例子与通俗解释

可以把 `CTS` 想成一个“带显式时钟的 timeout 状态机”。例如系统在位置 `Wait` 中等待外部响应：

1. 时钟 `x` 与 master clock `T` 一直随着 `tick` 增长。
2. 若在 `x<5` 时收到事件，则走成功 transition。
3. 若 `x=5` 仍未收到响应，就触发 timeout transition。

通俗地说，`CTS` 的直觉就是：普通 transition 负责离散跳转，`tick` 负责让所有 clocks 一起往前走。这样 proof system 可以直接围绕显式 clocks 来写。

### 运行 / 接受 / 转移语义

论文把 `tick` 视为特殊扩展 transition，其关系可压成：

$$
p_{\mathrm{tick}}:\ \Delta>0 \land D'=D \land C'=C+\Delta \land \forall t\in[0,\Delta).\ \Pi(D,C+t)
$$

上式中的符号逐项解释如下：

1. `\Delta` 是一次时间流逝的长度。
2. `D'=D` 表示时间流逝不改变离散变量。
3. `C'=C+\Delta` 表示所有 clocks 统一增长。
4. `\Pi(D,C+t)` 要求整个流逝区间内 time-progress condition 都成立。

`PTS` 则把时间流逝进一步拆成由某个 activity `a` 驱动的 phase。原文写成：

$$
p_a \to I = F^a(V^0,t)
$$

这里 `p_a` 是 activity 的 activation condition，`F^a` 给出 integrators 在这段 phase 中的演化函数。

### 语义边界

`CTS` 比普通 `Timed Automata` 更偏 proof-oriented transition-system 模型；它没有 region graph 那套 automata-theoretic machinery，但显式 clocks、`tick` 和 verification diagrams 非常适合写证明规则。`PTS` 则沿着同一条线把 hybrid phase 加了进来。

### 关键性质与判定边界

论文关注的核心性质是 non-zeno 和 proof rules。它对 computation 要求：

$$
s_0[T],s_1[T],\ldots \text{ grows beyond any bound}
$$

并定义：

$$
\mathcal C\ \text{is non-zeno iff every finite run can be extended into a computation}
$$

这为 safety、response 以及 hybrid invariance 的证明提供了统一前提。换言之，本文的重要性不在复杂度边界，而在把 `CTS/PTS` 这套模型固定成“可证明的 transition-system 语义”。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 transitions 和显式状态变量组成骨架。 |
| 事件 / 触发 | 强支持 | ordinary transitions + `tick` / activity phases。 |
| 守卫 / 数据 | 强支持 | transition relation 与 time-progress condition 都显式可写。 |
| 层次 | 不支持 | 原始模型不是层次状态机。 |
| 并发 / 同步 | 非重点 | 核心是 proof-oriented real-time / hybrid semantics。 |
| 时间约束 | 强支持 | 显式 clocks、master clock 和 `tick` 是模型核心。 |
| 连续动态 / 随机性 | `CTS` 无连续、`PTS` 强支持连续 | 通过 activities / integrators 引入 hybrid 扩展。 |
| 可执行 / 可验证性 | 强理论支持 | safety / liveness / non-zeno / hybrid invariance 规则完备。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `CTS` 骨架 | `$\mathcal C=(V,\Theta,T,\Pi)$` | 明确 clocks + transitions + time-progress。 |
| `tick` 语义 | `$p_{\mathrm{tick}}:\ \Delta>0 \land D'=D \land C'=C+\Delta \land \forall t\in[0,\Delta).\Pi(D,C+t)$` | 时间流逝被建成特殊 transition。 |
| `PTS` 骨架 | `$\mathcal P=(V,\Theta,T,A,\Pi)$` | 在 `CTS` 上加入 activities。 |
| activity 语义 | `$p_a \to I = F^a(V^0,t)$` | phase 内连续演化规则。 |
| non-zeno 条件 | `$\mathcal C$ non-zeno iff every finite run extends to a computation` | proof rules 的关键前提。 |

## 构造方式与承载格式

### 建模入口

1. 先列出离散变量和 clocks，并指定 master clock `T`。
2. 为离散行为写普通 transitions。
3. 用 `\Pi` 约束哪些时间流逝是允许的。
4. 若系统含连续动力学，再加入 integrators 与 activities，升级到 `PTS`。

### 机器可处理承载方式

机器可处理承载方式是 clocked / phase transition tuples、`tick` / `t_a` 扩展迁移和 verification diagrams，而不是统一工程文件格式。

### 交换与互操作

它直接继承 [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md) 的 `TTS/PTS` 语义线，也与 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 `Timed Automata` 路线形成鲜明对照：一个偏证明，一个偏 automata-theoretic decision procedure。

## 配套基础设施

- 建模/编辑工具：原文提到 ongoing implementation support，但未给统一公开包。
- 解析/交换/元模型支持：核心是 tuples、verification diagrams 与 proof rules。
- 仿真/执行支持：`tick` / activity semantics 清晰，可直接解释运行。
- 验证/分析支持：invariance、response、non-zeno、hybrid invariance。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 explicit-clock transition-system 线的经典节点。

## 适用场景与需求前提

### 适用场景

适合那些更关心“如何证明系统正确”而不是“如何做 region-based 自动判定”的实时/混成系统，尤其适合写 invariance、response 和 non-zeno 证明。

### 需求前提

1. 需求必须能显式写成离散 transitions 与 clocks。
2. 若要升级到 `PTS`，连续变量应能写成 integrators / activities。
3. 更适合 proof-oriented analysis，而不是直接工业模型交换。

### 不适用或高成本场景

如果目标是直接进入主流 `UPPAAL` 风格工具链，`CTS` 本身并不是最自然的工程输入格式。

## 与相邻形式主义的关系

相对 [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md)，它把 `TTS` 线进一步显式 clock 化；相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它没有走 region-graph / language-theoretic 路线，而是把 proof rules 保持得更接近 untimed transition systems；相对 [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)，`TIOA` 更强调接口与组合，而 `CTS` 更强调显式时间推进和证明规则。

## 与本研究的关系

### 对 Project 1 的价值

它能在演化树里补出 `Clocked Transition Systems` 节点，并把 `Timed Transition Systems` 和 `Phase Transition Systems` 之间的历史连接补完整。

### 作为目标形式主义还是中间表示

更适合作为中间语义层和证明导向模型，而不是最终工程交换格式。

### 对需求到模型生成的启发

若需求很强调 response / invariance / non-zeno 一类 proof obligation，先抽成 `CTS/PTS` 往往比直接落成普通 `TA/HA` 更自然。

### 现实限制

它的主要优势在 proof style，不在工程生态；自动化支持通常需要后续再映射到更主流的 model-checking 输入形式。

## 重要的相关工作

### 奠基或前身工作

- [from-timed-to-hybrid-systems/desc.md](../from-timed-to-hybrid-systems/desc.md)

### 同类型或同家族工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)
- [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有统一标准格式；其关键配套是 verification diagrams 与 proof rules。

### 与本研究关系最紧的工作

- 它最适合挂成 `Timed Transition Systems -> Clocked Transition Systems` 的经典节点，并继续把 `PTS` 线与混成主干接上。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Clocked Transition Systems / Phase Transition Systems`
- 论文角色：模型提出
- 核心功能：把 `TTS` 发展成显式 clocks 的 `CTS`，并在同文中回接 hybrid 扩展 `PTS`。
- 关键特性：master clock、`tick`、time-progress condition、non-zeno、activities、verification diagrams。
- 构造方式：`$\mathcal C=(V,\Theta,T,\Pi)$` / `$\mathcal P=(V,\Theta,T,A,\Pi)$` + proof rules。
- 基础设施：proof-oriented semantic framework，无工程标准格式。
- 适用场景：实时/混成系统的 invariance、response、non-zeno 证明建模。
- 需求前提：需求需能显式写成 transitions、clocks 与必要时的 activities。
- 状态：🟢
