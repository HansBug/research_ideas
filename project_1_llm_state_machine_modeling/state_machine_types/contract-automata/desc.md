# 契约自动机 / Automata for Analysing Service Contracts

## 基本信息

- 标题：Automata for Analysing Service Contracts
- 中文标题：用于分析服务契约的自动机
- 作者：Davide Basile, Pierpaolo Degano, Gian-Luigi Ferrari
- 发表：Trustworthy Global Computing (TGC 2014) Pre-Proceedings
- DOI：原文未提供
- 链接：https://www.cs.le.ac.uk/events/tgc2014/pre-proceedings/basile_et_al.pdf
- 形式主义：Contract Automata
- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具下载。
- 标准/格式获取方式：原文给出自动机与组合规则，不提供标准交换格式。

## 简报

Contract Automata 把多方服务协作中的 request/offer 匹配过程状态机化，重点不是一般接口兼容，而是“组合后所有请求是否最终得到满足”。为此，论文围绕 agreement、weak agreement、orchestrator 和 liability 构建了一整套组合与责任分析框架。

- 形式主义定位：面向多方服务契约匹配的组合状态机。
- 构造方式简述：动作由 request/offer/match 向量组成，自动机通过 product 与 a-product 组合。
- 基础设施与场景简述：原文没有标准文件载体，但给出 agreement/weak agreement 检查、controller/orchestrator 合成与 liability 分析方法。

```text
多方服务契约 -> request/offer 向量自动机 -> 组合与编排 -> agreement/liability 分析
```

## 形式主义定义与核心对象

### 定义对象

它主要描述服务或参与方之间的契约履约关系，而不是单个控制器内部状态。

### 核心抽象

一个 contract automaton 是带向量字母表的有限自动机。每个向量分量记录某个参与方此步是 request、offer、match 还是 idle。

可把一个 rank 为 `n` 的 contract automaton 保守写成：

$$
CA = (Q, q_0, F, T)
$$

其中迁移关系为：

$$
T \subseteq Q \times S^n \times Q
$$

这里 `S^n` 是 `n` 维向量动作字母表；每个分量描述对应参与方在该步的 request、offer、match 或 idle 行为。

### 运行 / 接受 / 转移语义

一条运行写成：

$$
q_0 \xrightarrow{\vec{a}_1} q_1 \xrightarrow{\vec{a}_2} \cdots \xrightarrow{\vec{a}_m} q_m
$$

其对应的词为：

$$
w = \vec{a}_1 \vec{a}_2 \cdots \vec{a}_m \in L(CA)
$$

原文的关键不是普通接受，而是对词 `w` 是否满足 agreement / weak agreement 的判断。记 `Obs(w)` 为向量动作的可观察投影，则论文给出的 agreement 集合是：

$$
\mathcal{A} = \{ w \in (S^n)^* \mid Obs(w) \in (O \cup \{\tau\})^* \}
$$

也就是说，强 agreement 要求接受词中不留下未配对的 request。

弱 agreement 的定义更宽松。原文给出：

$$
\mathcal{W} = \{ w = \vec{a}_1 \cdots \vec{a}_m \mid \exists f:[1..m]\to[1..m],\ f \text{ 对 requests 全定义且单射，且 } f(i)=j \Rightarrow \vec{a}_i \bowtie \vec{a}_j \}
$$

它允许 request 和 offer 异步配对，因此：

$$
\mathcal{A} \subsetneq \mathcal{W}
$$

### 语义边界

它适合表达多方契约满足关系和编排责任，不适合表达层次控制、实时约束或连续动态。

### 关键性质与判定边界

围绕上述两个集合，论文把契约分析压成如下问题：

$$
\text{Safe}(CA) \iff L(CA) \subseteq \mathcal{A}
$$

$$
\text{AdmitsAgreement}(CA) \iff L(CA) \cap \mathcal{A} \neq \emptyset
$$

$$
\text{WeakSafe}(CA) \iff L(CA) \subseteq \mathcal{W}
$$

$$
\text{AdmitsWeakAgreement}(CA) \iff L(CA) \cap \mathcal{W} \neq \emptyset
$$

在此基础上，论文还讨论 orchestrator / controller 合成，以及导致违反 agreement 的 liable participants。也就是说，Contract Automata 的判定边界不在普通接口相容，而在“多方契约是否能被同步或异步满足，以及谁对失败负责”。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 契约履约过程由状态刻画。 |
| 事件 / 触发 | 强支持 | request/offer/match 是核心动作。 |
| 守卫 / 数据 | 部分支持 | 原文重点不在复杂数据状态。 |
| 层次 | 不支持 | 非层次结构。 |
| 并发 / 同步 | 强支持 | 多方组合、同步/异步匹配是核心。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散契约行为。 |
| 可执行 / 可验证性 | 强支持 | agreement、weak agreement、controller/liability 明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 向量动作词 | `$w = \vec{a}_1 \cdots \vec{a}_m \in L(CA)$` | 行为由多方同步动作向量组成。 |
| agreement | `$\mathcal{A} = \{w \mid Obs(w)\in (O \cup \{\tau\})^*\}$` | 所有请求都被同步满足。 |
| weak agreement | `$\mathcal{W} = \{w \mid \exists f,\ f(i)=j \Rightarrow \vec{a}_i \bowtie \vec{a}_j\}$` | 允许异步 request/offer 配对。 |
| 安全性 | `$L(CA)\subseteq \mathcal{A}$` 或 `$L(CA)\subseteq \mathcal{W}$` | 组合是否始终守约。 |
| 可达 agreement | `$L(CA)\cap \mathcal{A}\neq\emptyset$` | 是否存在至少一条可接受协作路径。 |

## 构造方式与承载格式

### 建模入口

先为每个参与方定义 request/offer 行为，再通过 product 或 a-product 组合成多方契约系统。

### 机器可处理承载方式

原文没有给出标准 DSL 或 XML。机器可处理性来自向量动作和自动机组合规则。

### 交换与互操作

互操作体现在多方契约组合和 orchestrator 合成上，而不是通用交换格式上。

## 配套基础设施

- 建模/编辑工具：原文未说明。
- 解析/交换/元模型支持：原文未说明。
- 仿真/执行支持：通过 automata composition 和 controller 语义体现。
- 验证/分析支持：agreement、weak agreement、liability、network-flow 风格分析。
- 代码生成/转换支持：原文未说明。
- 标准化或社区生态：偏研究型生态，标准化程度较低。

## 适用场景与需求前提

### 适用场景

适用于服务组合、契约匹配、编排责任分析、多方 request/offer 配平问题。

### 需求前提

1. 需求能抽象为多方请求与提供。
2. 需要判断契约能否达成 agreement。
3. 需要分析失败责任属于哪个参与方。

### 不适用或高成本场景

若目标是工业控制状态机本体或标准化执行载体，契约自动机不是首选。

## 与相邻形式主义的关系

相对 `Interface Automata`，它更强调多方 request/offer 匹配和 agreement；相对 `I/O Automata`，它更偏契约编排而不是一般组件交互；相对 `SCXML/UML`，它不是通用执行标准。

## 与本研究的关系

### 对 Project 1 的价值

可作为“多个状态机生成结果如何签约式拼装”的参考模型。

### 作为目标形式主义还是中间表示

更适合作为特定交互/编排问题的中间分析表示。

### 对需求到模型生成的启发

当需求本质上是多方协作责任分配时，直接生成契约自动机比普通控制状态机更贴切。

### 现实限制

其生态和标准基础设施明显弱于 `UML/SCXML` 一类主流工程载体。

## 重要的相关工作

### 奠基或前身工作

- 服务契约与编排研究。

### 同类型或同家族工作

- Interface Automata。
- 过程代数和服务组合语义工作。

### 标准 / 格式 / 工具链工作

- 原文未提供统一标准格式。

### 与本研究关系最紧的工作

- 多主体行为拼装、契约满足与责任追踪。

## 文献分类总结

- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 形式主义：Contract Automata
- 论文角色：模型提出
- 核心功能：把多方 request/offer 契约匹配建模为可组合自动机。
- 关键特性：agreement、weak agreement、controller/orchestrator、liability。
- 构造方式：向量动作自动机 + product/a-product 组合。
- 基础设施：原文提供分析方法，无统一文件标准。
- 适用场景：服务编排、契约组合、责任分析。
- 需求前提：需求可抽象为多方请求/提供关系。
- 状态：🟢
