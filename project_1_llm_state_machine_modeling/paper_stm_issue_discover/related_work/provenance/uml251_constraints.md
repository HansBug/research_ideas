# OMG UML 2.5.1 状态机良构性规则的开采结果

> **历史来源扫描说明：** 本文件是形式资料的原始摘录和审计，不是当前谓词表，也不
> 自动证明任何核心谓词已经通过严格来源门。当前注册表和来源三分类以
> [`pipeline/evidence_discovery/`](../../pipeline/evidence_discovery/) 为准。

> ⭐ **本文件记的是一次定向开采**：⭐ OMG UML 2.5.1（formal/2017-12-05）官方 PDF 全文 796 页，⭐ Chapter 14 StateMachines 逐条读完。⛔ 它**不是** 19 行分级表（那在 [predicate_provenance.md](./predicate_provenance.md)），⭐ 也不是证据总账。
>
> ⛔⛔ **本文件含一条对我方论证的更正**（§2），⛔ 不得只读正面部分。
>
> **档位标记**：§1 §3 §4 的条款与计数为【实测】，⭐ 关键两条已由我亲自回原文逐字复核；⭐ 判断与建议为【AI 建议·待确认】。

## 0. ⛔ 为什么专门开采这一份

⭐ 上一轮开采 Torre 的 UML 一致性规则系统映射研究时发现：⭐ 它**主动剔除了 66 条「已在 UML 标准里的良构性规则」**，且逐字写明，仅「只涉及状态机图」的 52 条被删规则里就有 **24 条**因此被删（`paperA_thesis.txt:2460-2462`）。⛔ **但它没有枚举这 66 条。** ⭐ 开采者的结论是「⭐ 这批证据的正确去处是 OMG UML 2.5.1 的 StateMachines 章」。

⭐ 同时这次开采带一个**判决性测试**（§2）。

### ⭐ 取文与复核

| 项 | 【实测】 |
| :-- | :-- |
| 来源 | `https://www.omg.org/spec/UML/2.5.1/PDF` —— ⭐ HTTP 200，⭐ 18,069,510 字节，⭐ 796 页，⛔ 无 WAF、⛔ 无重定向问题 |
| 抽取 | [tools/pdf_extractor.py](../../../../tools/pdf_extractor.py) `text` 模式，⭐ 26,663 行；⭐ OCL 表达式完整，⛔ 未触发切 OCR 的条件 |
| 页码校准 | ⭐ spec 页码 = PDF 页码 − 42（⭐ 逐页核对页脚；⚠️ front matter 区不适用该 offset） |
| ⭐ **独立交叉验证** | ⭐ Eclipse UML2 的 6 个 `*Operations.java`：`validate*` 方法名与数量与规范 **1:1 吻合**（⭐ Vertex **0** / Region 4 / State 5 / Pseudostate 9 / StateMachine 4 / Transition 9） |
| ⭐ **我亲自复核的两条** | ⭐ ① Ch.14 恰有 **9** 个 Constraints 小节且 `14.5.13`（Vertex）**不在其中**；⭐ ② 语义变异点原文逐字无误 |

## 1. ⭐⭐ 最重要的一条：`containment` 的结构性解释被**正面证据**印证

⭐ [SUMMARY.md](./SUMMARY.md) §4.5.2 记的裁定者推断是：「⭐ `containment` 的『正确』需要**外部规约作参照**，⛔ 而语言层良构性规则**天生给不出**」。⭐ 这次拿到了**可机械核验的正面事实**：

| 【实测】 | 值 |
| :-- | :-- |
| ⭐ Chapter 14 内本地成文的 constraint 总数 | **47** |
| ⛔ 其中判定「状态 Y 该挂在 X 之下而不是 Z 之下」的 | **0** |
| ⛔ `Vertex` 元类的 constraint 数 | **0**（⭐ 该元类**没有 Constraints 小节**：14.5.13 只有 Description / Diagrams / Generalizations / Specializations / Association Ends / Operations 六节） |
| ⚠️ 连「Vertex 必须属于某个 Region」这条**合法性** | ⛔ 也不是 constraint，⭐ 而是关联端多重度，⛔ 且是 `[0..1]` 而非 `[1..1]` |

> ⭐ `container : Region [0..1]{subsets NamedElement::namespace} (opposite Region::subvertex)` —— The Region that contains this Vertex. —— 14.5.13.5 Association Ends，spec p. 363

⭐ 全章唯一涉及「包含关系」的成文 constraint 只有两条，⛔ 且都只管**归属通道**与**作用域闭合**：

> ⭐ `owned` —— If a Region is owned by a StateMachine, then it cannot also be owned by a State and vice versa. —— 14.5.8.6，spec p. 354（`uml251.txt:13299-13301`）

> ⭐ `transition_vertices` —— The source and target Vertices of a Transition must be contained in the same StateMachine as the Transition. —— 14.5.11.8，spec p. 362（`uml251.txt:13577-13579`）

⭐ **可落稿的句子**（⛔ 只承诺存在性，⛔ 不承诺符合性）：

> ⭐ UML 2.5.1 为状态机语言成文了 47 条良构性规则（Chapter 14 内本地条款），⛔ 其中判定状态层次归属正确性的条目为 0；⭐ `Vertex` 元类无 Constraints 小节。

⚠️ ⛔ **计数口径必须限定**（⚠️ 开采者主动提出）：**47 是「Chapter 14 内本地成文的条数」，⛔ 不是「对状态机生效的全部条数」** —— ⭐ `Region` 继承 `Namespace`，因而 `members_distinguishable`（7.8.10.7）等通用条款同样生效，⛔ 而这批未被系统枚举。

## 2. ⛔⛔ 一条对我方论证的**更正**：缺席有两种成因，⛔ 只有一种支持我们

⭐ 我方的结构性假设原本是**双向**的。⭐ 这次的判决性测试表明**两个方向命运不同**：

| 方向 | 内容 | ⭐ 实测 |
| :-- | :-- | :-- |
| ⭐ **正方向** | 需要外部参照物 ⇒ 语言层**给不出** | ⭐ **未被触动，且被 §1 强力支持** |
| ⛔ **逆方向** | 只需模型自身即可判定 ⇒ 语言层**会成文** | ⛔ **被推翻** |

⛔ 推翻它的是 `initial_target` 的**存在性**那一半。⭐ 「这个 Region 里有没有 initial Pseudostate」是**纯粹的模型内部谓词**（`region.subvertex->exists(kind = initial)` 一行 OCL 写完，⛔ 不需要任何外部参照物），⛔ 而 UML **明确拒绝**把它列为良构性违规：

> ⭐ Default activation means that execution starts with the Transition originating from the initial Pseudostate of the Region, **if one is defined. However, no specific approach is defined if there is no initial Pseudostate that exists within the Region. One possible approach is to deem the model ill defined.** An alternative is that the Region remains inactive, although the State that contains it is active. —— 14.2.3.2 Regions，spec p. 307（`uml251.txt:11862-11867`，⭐ 我逐字复核过）

> ⭐ **If no initial Pseudostate is defined, there is no single approach defined. One alternative is to treat such a model as ill formed.** A second alternative is to treat the composite State as a simple State… —— 14.2.3.4.5 Entering a State，spec p. 310（`uml251.txt:11987-11992`）

⭐⭐ **正确的表述因此是**：

> ⭐ **语言层良构性规则集合是「模型内部可判定谓词」的一个真子集，⛔ 而不是等于。**

⛔ **缺席的两种成因必须分开，⛔ 不得混用**：

| 成因 | 含义 | ⭐ 能否支持我方论证 |
| :-- | :-- | :-- |
| **(a) 结构性不可能** | ⭐ 该检查需要外部参照物，⛔ 语言层**天生**给不出（⭐ `containment` 的父态正确性） | ⭐ **能** |
| ⛔ **(b) 能给而选择不给** | ⭐ 标准化组织把它留作实现自由度（⭐ `initial` 的存在性 —— **语义变异点**） | ⛔ **不能** |

⛔⛔ **若论文只论证 (a) 却把 (b) 也算进去，会被一句话打掉** —— ⭐ UML 自己写着 "One possible approach is to deem the model ill defined"，⛔ 那正是承认它**可以**是良构性规则。

⭐ **(b) 这一类另有正面价值**（⛔ 但要换个说法用）：⭐ 它说明「⭐ 语言标准留白 ⇒ 具体建模实践必须自己补规则」，⭐ 为「方法层需要一套比标准更严的检查集」提供了**来自标准原文的**依据 —— ⭐ 且这仍是存在性事实，⛔ 不是符合性主张。

## 3. ⭐ 逐谓词结果

### 3.1 ⭐ `initial_target` —— 成文 4 条（⛔ 但只覆盖唯一性与形状，⛔ 不覆盖存在性）

| 元类 | 条款名 | 章节 / 页 | 逐字 |
| :-- | :-- | :-- | :-- |
| `Region` | `initial_vertex` | 14.5.8.6 / p. 354 | ⭐ A Region can have **at most one** initial Vertex. |
| `Pseudostate` | `initial_vertex` | 14.5.6.7 / p. 351 | ⭐ An initial Vertex can have **at most one** outgoing Transition. |
| `Pseudostate` | `outgoing_from_initial` | 14.5.6.7 / p. 350 | ⭐ The outgoing Transition from an initial vertex may have a behavior, **but not a trigger or a guard**. |
| `Transition` | `initial_transition` | 14.5.11.8 / p. 361 | ⭐ An initial Transition at the topmost level Region of a StateMachine that has **no Trigger**. |

⭐⭐ 后两条对本研究特别有价值：⭐ 它们意味着「⭐ 默认初始迁移若带守卫，则默认进入可能无路可走」这件事**在语言层就被判为违规** —— ⭐ 那是 `initial_target` 要抓的一类**实质缺陷**，⛔ 不只是画图习惯。

### 3.2 ⛔⛔ `guard_distinguishable` —— UML 是**许可**，⛔ 不是义务

⛔ **Chapter 14 中没有任何 constraint 要求同一状态同一事件的多条迁移守卫互斥。** ⭐ 规范正相反：

> ⭐ It is possible for more than one Transition to be enabled within a StateMachine. If that happens, then such Transitions may be **in conflict** with each other… **at most one of those Transitions can fire in a given run-to-completion step.** —— 14.2.3.9.3 Conflicting Transitions，spec p. 317

> ⭐ These priorities **resolve some but not all** Transition conflicts, as they only define a **partial ordering**. —— 14.2.3.9.4 Firing priorities，spec p. 317

⚠️ ⭐ 「模型者应避免不确定性」这句话**只出现在 Activities 章的 DecisionNode**，⛔ 且是 "should"（建议）⛔ 而非 constraint，⛔ **不在 StateMachines 章**（15.3.3，spec p. 390）。

⛔⛔ **因此 `guard_distinguishable` 不得从 UML 2.5.1 取普遍性依据。** ⭐ 依据须另找（⭐ 本轮补强已从 Torre 规则集 #13 取到，⭐ 那条另有 106 位专家的逐条评议数据与 62 处真实模型违例）。

### 3.3 ⛔ `variable_declared` —— Chapter 14 **没有变量概念**

⭐ State 侧只有 `stateInvariant : Constraint [0..1]`，⭐ Transition 侧只有 `guard : Constraint [0..1]`；⭐ `Variable` 属 Activities（Clause 15/16）。⛔ **不得从 UML StateMachines 取此谓词的依据**；⚠️ 即便去 Activities 找到，⛔ 那属活动图而非状态机，⛔ 取来当状态机语言的普遍性依据是错的。

### 3.4 ⭐⭐ `*_declared` 家族：⛔ 缺席另有**第三种**成因 —— 表示介质不同

⭐⭐ ⛔ **这一条必须写进论文，⛔ 否则「UML 没有 `state_declared` 规则」会被误读成「UML 认为不必检查」。**

⭐ UML 抽象语法用的是**元模型链接**，⛔ 不是名字引用：`Transition::source : Vertex [1..1]`、`Transition::target : Vertex [1..1]` 都是**关联端**。⛔ 于是「一个悬空的状态名」在 UML 里**根本不可表达** —— ⭐ 因此既不存在、⛔ 也不需要「被引用的状态必须已声明」这条 constraint。

⭐⭐ **而在文本 DSL（如 `pyfcstm`）里，名字可以悬空，于是它是一条真实的检查。** ⭐ 这为 **② 元模型定义性**这一类给出了一个比原先更准的说法：⛔ 它们的外部证据薄**不是**因为领域不在乎，⭐ 而是因为**图元模型让这类错误不可表达**。

⭐ 在这个前提下，Ch.14 里真正的「被引用者必须在被引用命名空间中已声明」条款有 3 条：

| 谓词侧 | 元类 | 条款名 | 章节 / 页 |
| :-- | :-- | :-- | :-- |
| ⭐ 跨命名空间声明检查（⭐ 最强命中） | `State` | `destinations_or_sources_of_transitions` | 14.5.9.8 / p. 356 |
| 种类符合 | `State` | `entry_or_exit` | 14.5.9.8 / p. 356 |
| ⭐ 名字唯一性（通用层，⭐ 经 `Region` 继承 `Namespace` 生效） | `Namespace` | `members_distinguishable` | 7.8.10.7 / p. 51 |

### 3.5 ⭐ `cardinality` —— 成文密度最高，⛔ 但阈值一律由元模型固定

⭐ 命名 constraint 形式 **13 条**（`FinalState` 6 · `Pseudostate` 3 · `Region` 2 · `State` 2），⭐ 另有大量以**关联端多重度**形式给出的基数要求（⚠️ 后者无条款名，⛔ 引用时须引 Association Ends 小节）。

⛔ **全部阈值均为元模型固定的常数**（`<= 1` / `>= 1` / `= 0`），⛔ 与前两轮被拒的 15 条同型 —— ⛔ **不支撑「恰好为 N、N 取自需求文本」这一形式**。

⭐ 但它**恰好支撑** [SUMMARY.md](./SUMMARY.md) §4.1 已备好的那句落稿表述的前半层：「⭐ 对作用域内元素计数并与预期值比对，是这类元模型的常规良构性手段」。⭐ 本次开采为该句提供了**可精确到条款名**的引证。

## 4. ⛔ 证据轴合规：⭐ 可写与⛔ 不可写的句式

⭐ **可以写**（⭐ 只承诺「该检查是成文条目」）：

- ⭐ 「复合结构默认初始入口的**唯一性**与默认迁移**形状**，是 UML 2.5.1 状态机语言成文良构性规则中的条目（`Region::initial_vertex`、`Pseudostate::outgoing_from_initial`）。」
- ⭐ 「UML 2.5.1 **Chapter 14 内本地成文**的 47 条状态机良构性规则中，判定状态层次归属正确性的条目为 0；`Vertex` 元类无 Constraints 小节。」（⚠️ ⛔ **括号里那句限定不可删** —— ⭐ §1 与 §5 都写明 47 **不是**「对状态机生效的全部条数」，⭐ `Region` 继承 `Namespace` 故 `members_distinguishable` 等通用条款同样生效。⛔ 上一版的可写清单里漏了这个限定，⭐ 2026-08-12 补回。）
- ⭐ 「UML 2.5.1 明确将『Region 缺少 initial Pseudostate』留作**语义变异点**，⛔ 而非良构性违规。」

⛔ **不可以写**（⛔ 承诺「我们与谁一致」）：

- ⛔ 「UML 要求每个 Region 至多一个 initial，**因此**我们的 `initial_target` 谓词有标准依据。」
- ⛔ 「我们的谓词集合**覆盖了** UML 良构性规则的 X%。」
- ⛔ 「我们的实现**符合** OMG UML 2.5.1 §14.5.8.6。」

## 5. ⛔ 未核验项（⛔ 不得据此推论）

1. ⚠️ **Eclipse UML2 未实现 `transition_vertices` 的原因** —— ⭐ 确证了它不在 `TransitionOperations.java` 里（⭐ 三种 grep 全无命中），⛔ 但「因为它是 2.5.1 新增」**只是推断**；⛔ 未取 UML 2.5（formal/2015-03-01）原文对比。
2. ⚠️ **PDF 中「•」前导符的含义** —— ⭐ 三处带、其余不带，⛔ 未找到图例，⛔ 不排除是抽取伪影。
3. ⚠️ **history Pseudostate 是否在 `pyfcstm` 的 $M$ 表达范围内** —— ⭐ 影响 3 条的 scope 归属，⛔ 待 project_1 侧裁定。
4. ⛔ **`event_declared` 在 Clause 13 (CommonBehavior) 的成文情况未查** —— ⭐ 只核了 Chapter 14。
5. ⛔ **Chapter 14 之外经继承生效的通用 constraint 未系统枚举** —— ⭐ 只顺手核了 `Namespace::members_distinguishable`。⭐ 这直接决定 §1 那个 **47** 的口径。

## 6. ⛔ 界外条款（⭐ 列出以便边界门审计，⛔ 不得取）

⭐ 8 条与正交区 / 并发（fork / join / AND-state）绑定：`Pseudostate::fork_vertex` · `join_vertex` · `transitions_outgoing` · `transitions_incoming` · `Transition::fork_segment_guards` · `fork_segment_state` · `join_segment_guards` · `join_segment_state`。

⭐ 另有散文规范一条同样界外：「⭐ NOTE. A Transition from one Region to another in the same immediate enclosing composite State is not allowed.」（14.2.3.9.6，spec p. 318）。

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | 建立。⭐ 开采 OMG UML 2.5.1 Chapter 14 全部 47 条 constraint；⭐ 印证 `containment` 的结构性解释（0/47、`Vertex` 无 Constraints 小节，⭐ 经 Eclipse UML2 交叉验证）；⛔ **更正**我方假设的逆方向（⭐ 语义变异点反例）；⛔ 记录 `guard_distinguishable` 不得引 UML、⛔ `variable_declared` 不得引 UML；⭐ 提出 `*_declared` 缺席的第三种成因（表示介质）。 |
