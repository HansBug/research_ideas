# 合式性公理表（预注册草案，**尚未冻结**）

> ## ⛔ 2026-08-07：UML 原文逐字核对推翻了本表大部分规范依据
>
> 独立核对者取到 **OMG 官方 PDF**（`formal/2017-12-05`，18 MB / 796 页）逐字核对，**四条全部比表里写的弱**。这不是几个条款号的问题，是**整张表的主张需要降级**。
>
> | 公理 | 核对结论 |
> | :-- | :-- |
> | **A2** | **完全没有规范依据。** §14.2.3.9 的标题是 "Event Processing for StateMachines" 而非 "Transition semantics"（全文 grep "transition semantics" **0 命中**）；穷举 Clause 14 全部 **5 处** ill-formed 语句 + **5 组** OCL 约束集，**零支撑** |
> | **A3** | **"ill formed" 强度借错了地方。** §14.2.3.7 的两句引文逐字准确，但它们讲的是 **choice 伪态**出边。而 UML 恰好在 §14.2.3.9.3 用**与 A3 一字不差的例子**（同源、同事件、不同守卫、两个都为真）说明**如何处理**（至多一条 fire），**从未称其 ill formed** —— **规范对 A3 的主语有明确表态，且与 A3 相反** |
> | **A1** | 「唯一」的**存在性**那半，是规范**显式拒绝表态**处：§14.2.3.2 与 §14.2.3.4.5 主动列出**两种都合法**的解读，其一（复合态按简单叶态处理）**明确允许没有默认入口**。写成 $\exists!$ 等于在规范保留二义处单方面选边。另三处 OCL 引用问题见 §七 |
> | **A4** | **类别错位。** 它是从操作语义（§14.2.3.8：effect 于 traverse 时执行）推出的**制品-语义一致性检查**，不是 UML 合式性约束；规范无对应 ill-formed 规则。且 §14.2.3.4.5–6 支撑的是「顺序」，A4 主张的是「生效」 |
>
> ### 我已完成核对者交给我的那一项
>
> A3 的适用性取决于语料里「同源同触发、目标不同」的分支点是 choice 伪态还是普通 State。**实测 11 个 grid pair：2 组，全部是普通 State，零组是 choice 伪态。**
>
>     0029/enter_hwy[dist_to_front_25_extra_lane_true]     0047/Clamping[Collision_Avoided]
>
> **所以 A3 的引用不成立，"ill formed" 措辞必须放弃。**
>
> ### 核对者的一条结构性建议（已采纳，见 §七）
>
> 本表把三类东西混在同一列「规范出处」下，而它们**约束力依次递减**：
>
>     (a) 硬性 OCL 不变式        outgoing_from_initial、initial_vertex     (b) 规范性散文             §14.2.3.7 的 at-most-one     (c) 操作语义描述           §14.2.3.8 / §14.2.3.9.x
>
> **A2 与 A4 全部落在 (c)。** 一位审稿人只要抽查 A2，就会发现它的出处标题都是错的、内容也不在那里 —— **而那会连带削弱另外三条的可信度。**

由一位**对失败分析完全盲**的执行者从规范推导，隔离清单见 [docs/protocol/rule_provenance.md](../../protocol/rule_provenance.md)。交付 **4 条**（上限 6 条），另有 7 条候选被主动剔除并附理由。

⚠️ **本文件尚未冻结。** 冻结条件见 §五。

## 一、四条公理（**已按 UML 核对降级**）

| # | 公理（降级后表述） | 约束等级 | 出处（已更正） |
| :-- | :-- | :-- | :-- |
| **A1** | 复合态若声明了默认入口，则该入口**至多一个**且**不带 guard 与 trigger** | **(a) 硬性 OCL** | §14.5.6.7 `outgoing_from_initial`（p.350）—— **唯一同时覆盖 guard+trigger 且不限层级的 OCL** |
| **A3** | 同源同触发的备选迁移若守卫重叠，则**选择不确定** | **(c) 操作语义** | §14.2.3.9.3 Conflicting Transitions（p.317）+ §14.2.3.9.1 + §14.2.3.9.4 Firing priorities |
| **A4** | 已声明的迁移效果在迁移被 traverse 时执行 | **(c) 操作语义** | §14.2.3.8 Transitions（p.314）+ §14.2.3.9.6 执行序 step 2（p.318） |
| ~~A2~~ | ~~已声明的迁移必须可实现~~ | **⛔ 无出处** | **建议移出本表**，见下 |

### 逐条降级的具体内容

**A1**：原表述「默认入口必须**唯一且无条件**」写成 $\exists!$，即同时主张**存在性**与**唯一性**。

- **唯一性 + 无条件** → 保留，改引 `outgoing_from_initial`（原引的 `initial_vertex` 管的是**出边条数** 不是 initial 顶点个数；原引的 `initial_transition` 前件含 `container.stateMachine->notEmpty()`，**对复合态恒真无效**，且它是 **OMG 未关闭 issue 的缺陷条款**）
- **存在性** → **删除**。§14.2.3.2 与 §14.2.3.4.5 主动列出两种都合法的解读，其一明确允许没有默认入口

$$\forall p \in S:\ \mathrm{comp}(p) \land \iota(p, c) \Rightarrow \mathrm{uncond}(p, c) \land \neg\exists c' \neq c.\ \iota(p, c')$$

⚠️ **这个降级有实质代价**：原 A1 能抓「复合态缺默认入口」，降级后**抓不到** —— 而那正是 `wellformedness` 层 6 条漏检的形态。**所以公理源这条通路的预期收益大幅下降。**

**A3**：放弃 "ill formed" 措辞。规范对同源自 State 的备选迁移**明确视为合法**并规定「至多一条 fire」。降级后 A3 只能主张「选择不确定」，而**「不确定」是否算缺陷取决于 NL 是否要求确定性** ——这使 A3 从合式性公理变成**一条依赖 NL 的条件性检查**，不再属于「模型内在义务源」。

**A4**：改为陈述操作语义事实。「已声明 effect 必须产生其声称的改变」**没有规范背书**，它是 `effect_declared` 与 `variable_delta_after` 的**对偶设计**所隐含的一致性检查 —— 可辩护，但不是 UML 约束。

**A2**：建议移出。理由三条叠加：

1. **零规范依据**（穷举验证）
2. 已因动机审计**退回普通形态**，§一自承「与 pyfcstm 重叠度上升、增量下降」
3. 一条既无规范依据、增量又低的公理，**收益不足以抵消「公理来源正当性」这一整体主张的风险**

## 一之二、⛔ 降级后这条通路还剩什么

**这是本次核对最重要的后果，必须写在前面。**

裁定给 v25 的第一条通路是「加 ≤6 条冻结公理，给方法一个模型内在义务源」，预期覆盖 **6 条** `wellformedness` 漏检（全是「复合态缺默认入口」）。

而降级后：

| 公理 | 还能抓什么 | 能抓那 6 条吗 |
| :-- | :-- | :-- |
| A1（降级） | 入口的**唯一性与无条件性** | ⛔ **不能** —— 存在性那半已删 |
| A3（降级） | 守卫重叠导致的选择不确定 | ⛔ 不能 |
| A4（降级） | effect 声明与执行的一致性 | ⛔ 不能 |

**所以第一条通路的预期收益从「6 条」降到「0 条」。**

### 这不意味着那 6 条不该被发现

它意味着**「用 UML 合式性公理去抓它们」这条路走不通** —— 因为 UML **显式允许**复合态没有默认入口（§14.2.3.2 的第二种解读）。那 6 条之所以是缺陷，依据不是 UML，而是**参考模型有而生成模型没有**，或 **NL 隐含了进入该复合态后应到哪**。

**那是另一类义务源，不是合式性公理。** 需要重新设计，而非在本表内加条目。

## 二、我对推导者三个提问的裁决

### ① A2 的叶量化维度 —— **裁决：退回不带叶量化的形态**

推导者的原始 A2 按 $\mathrm{Leaf}(s)$ 量化（复合态上的边必须在其**每个叶配置**上可实现，除被下层声明覆盖）。它主动披露：公理**内容**来自 UML §14.2.3.9.3（复合态上的迁移被全部子状态继承，这是规范事实），但**"去检查这一维"这个念头的触发源**是 `_simulate` / `_settle_cycles` 的 docstring —— 而那些 docstring 含语料统计（"704 bindings across 58 of the 60 pairs"）。

**裁决：退回 $\mathrm{Leaf}(s) = \\{s\\}$ 的普通形态。**

理由不是"内容有问题"，而是**动机审计会命中它，而且判得对**：

> 最可靠的判据是查引入动机，不是列举形态（§3.5）

推导者自己说它「最容易被质疑是不是为某种情形定制」。当**推导者本人不确定**时，保守选项是唯一站得住的。

📌 **注意这个裁决的方向：退回会降低方法的发现面，也就是降低我的数字。** 这一点使它更可信 —— 若我选保留，无论论证多规范都无法与"为达标而放宽"区分开。

叶量化维度可在**未来某代次**作为独立公理重新预注册，条件是由一位读到**干净的** `predicate_api.py` 的执行者推导（见 §三）。

### ② A1 的谓词硬限制 —— **裁决已修正：不改谓词，拒答在本语料上是正确的**

⚠️ **2026-08-07 复核后我推翻了自己原来的裁决（原文保留在下方）。**

#### 先纠正我复核时的两个错误

1. 我用 `sed -n '/def _initial_child_of/,/^    def /p'` 读那个函数，**正则在嵌套的 `def field(item, name)` 处提前终止**，于是只看到前 1/3，没看到后面的两处 `raise`。
2. 据此我用 `0048` 的实测（三个复合体全返回 `False`）去"否证"裁定。但 `0048` 那三个各**恰好 1 条无条件入口**，走的是正常路径 —— **实测根本不覆盖裁定说的情形**。

📌 **裁定引了确切行号（982–993），那本身就该让我先去看那几行。** 用一个会提前终止的正则读代码、再用一个不覆盖目标情形的实测去反驳，是两个独立的方法错误。

#### 裁定的代码断言成立

`_initial_child_of` 确实在两种情形 `raise UnsupportedEvidence`：`len(unconditional) > 1`，以及零条无条件。

#### 但发生面与性质都需要更正

实测 11 个 grid pair 的**全部 34 个复合态**：

    可答            33
    零条无条件       1     ← 0000 的**根状态** ≥2 条无条件      0

那 1 条的内容是决定性的：

    [*] --Power_On--> HumanDrivingMode
    [*] --Power_Off--> FinalState

**两条初始边都带事件。** 所以「进入这个模型时落在哪个子态」**真的取决于哪个事件先来** —— 这不是缺陷，是一个**事件驱动的入口选择**。谓词的拒答理由逐字是「which one entry takes depends on state this query cannot see」，**而那是对的**。

#### 结论：拒绝裁定的第 ② 项建议

若按建议改成返回 `False`，则 `initial_target(root, HumanDrivingMode)` = False 会被发布成「根的初始目标不是 HumanDrivingMode」这个**缺陷** —— 而模型在这里没有缺陷。**那会制造一条虚构。**

⚠️ 注意这与「影响面小所以降优先级」是**不同的结论**。我复核中途曾以为是前者（增量只有 1），实际是 **那 1 条改了会产生虚构**。前者是优先级判断，后者是正确性判断。

#### 保留的合理内核

裁定的关切本身有效：**A1 最有价值的那半边（入口确定性）若违反，不应落成 `unsupported`。** 但本语料上那一半的唯一实例是一个**合法的事件驱动入口**，不是违反。

若将来出现真正的「≥2 条**无条件**入口」（本语料 0 例），那才是 A1 该抓的歧义，且届时应返回 `False` 而非拒答。**登记为条件触发的 follow-up，而非 v25 首项。**

---

原裁决（已推翻，保留以便追溯）：

推导者查明：`initial_target` 在「≥2 条无条件入口」与「零条无条件入口」两种情形下 **`raise UnsupportedEvidence`**，不返回 `False`。即 **A1 最有价值的那半边其违反会落成 `unsupported` 而非 finding**。

它建议改 `initial_target`，理由是「放弃复合态入口确定性检查在学术上不可辩护」。**我同意这个判断**，但改动时机受两条约束：

1. **v24 正在运行，pipeline src 冻结** —— 不得中途改
2. 改一个谓词的返回语义会影响**所有**用它的断言，须走完整双 review

故登记为 v25 的第一项，与公理表冻结同批。

### ③ 「默认入口不得指向 pseudo 结点」的剔除 —— **裁决：剔除正确，且这条剔除本身是本次最有价值的产出**

推导者剔除它的理由是：`_reject_transient_subject` 的 docstring 记载 `pseudo` 关键字在语料中被**不一致使用**（同样语义的路由结点在某些制品里标了 `pseudo`、在另一些里写成普通叶态）。

> 这意味着该公理的命中分布是**语料生产方式的属性**，不是方法能力的属性 —— 收录它会把语料工件计成发现能力。

**这条剔除比任何一条收录更有价值**，因为它识别了一类我此前没有名字的错误：**用一条规则去检测语料自身的不一致，然后把命中记为方法能力。** 那不是特化（规则本身通用），但它同样使能力主张失效。

## 三、⚠️ 结构性问题：`predicate_api.py` 的 docstring 含实验结果

推导者的披露：

> 第 2、3 两个文件（任务指定必读）的 docstring 与注释中**大量包含实验结果性内容** —— 具体 pair 编号、"matrix-v16 / v17 / v20 / v22+v23 published X as a confirmed defect"、`EXP-0000-IT-001` 这类条目 ID、以及"51 of 219 False results (23.3%)"这类统计。

**这是我写进去的**，理由是"保留发现过程"。后果有两层，我逐层查了：

### 第一层（已排除）：不是实验泄漏

| 检查 | 结果 |
| :-- | :-- |
| `__doc__` / `inspect.getsource` / `getdoc` 用法 | **0 处** |
| 8 个语料统计探针在 v23 全 66 格 record 中 | **全部 0**（`matrix-v` 的 66 处命中全在 `.log` 的 output-dir 路径里，不在 record 内容中） |
| 送模型的谓词目录 `predicates.py` 含 pair 编号 / 条目 ID / 统计 | **0 处** |

**docstring 不进 prompt，未污染被测对象。**

### 第二层（成立）：污染了规则编写侧

任何未来的盲态推导都必读这些文件。本次推导者是**自己识别并披露**了这一点，还给出了补救建议 ——但下一位可能不会。

### 处置

**不删这些 docstring**（它们记录了真实的发现过程与教训，删掉会丢失可追溯性），改为**隔离**：

1. 把语料统计与代次编号从 `predicate_api.py` 的 docstring 移入 `eval/discover_matrix/` 下的专门文件，docstring 只留**机制说明**并链接过去
2. `docs/protocol/rule_provenance.md` 的隔离清单增列 `predicate_api.py` / `predicates.py` 的**当前版本**为"结果邻接"，要求推导者只把它们当可执行性证据、不用于决定收录哪条
3. 在移出完成之前，任何盲态推导的产出都必须附一份"哪些判断受结果邻接文本影响"的自查 —— 本次推导者已自发做到，应固化为要求

## 四、被剔除的 7 条候选（保留理由，防止后续重复推导）

| 候选 | 剔除理由 |
| :-- | :-- |
| 每个状态必须从默认入口可达 | 不是 UML 合式性约束；`W_UNREACHABLE_STATE` 已可靠报出；`reaches` 的 False 只是"界内没找到" |
| 每个叶态必须有出边 | 终态合法；`W_DEADLOCK_LEAF` 已报；属建模习惯非语言语义 |
| 入口链必须终止于叶 | **A1 的定理**，非独立公理（FCSTM 要求入口目标为直接子状态，有限树必然终止） |
| 默认入口不得指向 pseudo | **语料 `pseudo` 标注不一致** —— 命中分布是语料生产方式的属性（见 §二③） |
| 迁移端点可见性 / 复合态至少一子态 | 前者 `E_DANGLING_TRANSITION` 构建即失败；后者 `is_composite` 由 `substates` 派生，断言恒真 |
| 声明的事件必须被消耗 / 事件作用域一致 | `W_UNUSED_EVENT` 已报且非语言要求；后者 error 级、构建失败 |
| 运行到完成必须收敛到稳定配置 | **真实覆盖缺口**（`W_TOPOLOGICAL_NOEXIT` 只查 guard-agnostic 无出口），但**19 谓词无法表达** —— `terminates` 问"能否结束"非"能否稳定" |

## 五、冻结条件（尚未满足）

1. [x] **UML 2.5.1 原文逐字核对已完成**（2026-08-07，取到官方 PDF 18 MB / 796 页）—— **结论是推翻性的**：四条全部比表里写的弱，A2 **无规范依据**，A3 的 "ill formed" **借错地方且规范表态与之相反**。详见顶部横幅与 §七。**冻结前必须先按 §七 重写主张，否则冻结一张出处错误的表。**
2. [x] **`initial_target` 的返回语义 —— 复核后判定不需要修改**（2026-08-07）。实测 34 个复合态里拒答仅 1 例，且那例是**合法的事件驱动入口**（两条初始边都带事件），改成返回 `False` 会制造虚构。真正的「≥2 条无条件入口」本语料 **0 例**，登记为条件触发 follow-up
3. [x] **`predicate_api.py` 的结果邻接文本已移出**（2026-08-07）→ [observations.md](../../findings/predicates/observations.md)。9 处（4 计数 + 7 判定，有重叠）已改写为链接；**16 行定位类保留** —— 判别标准执行中修正过一次，见该文件
4. [x] **A2 已按 §二① 退回普通形态并重新表述**（2026-08-07）—— 终版形式见 §一，代价（与 pyfcstm 重叠度上升、增量下降）已写明
5. [ ] 冻结后写入 `holdout.json` 或等价冻结文件，记录 `frozen_at` commit

**冻结后不允许运行期追加。** 追加一条须重走盲态推导（[docs/protocol/rule_provenance.md](../../protocol/rule_provenance.md)）。


## 六、条件 3 的待移清单（29 行，精确定位）

`predicate_api.py` 里含结果邻接文本的行（代次名 / 条目 ID / pair 编号 / 语料统计）：

    L10    On pair 0006 that produced ``init state("X"); check exists_always <= 1:
    L331   seal path.  The third was measured to constrain nothing: 60 of 60 pairs L465   the model is answerable for. Across the v20 hold-out set the same shape produced 17 L466   published findings on pairs `0018` and `0038`. L472   *inconsistently*: pair `0018` marks nine routing nodes `pseudo state`, while `0048` L474   marks nothing. So the rule reaches `0018` and `0038` and not `0048` -- a property of L511   runs 2 to 7 edges deep.  matrix-v16 published one of those as a confirmed L512   defect: pair 0050's `AutonomousMode` settles `SubState1 -> SubState2 -> L588   than a leaf came back False.  Measured on pair 0000 -- pinned at L596   consumed: pinned at pair 0000's root, that cycle reports "no stoppable L716   # on pair 0006 the only effect on the Attack_Complete L897   a converted one: pair 0029's `HighwayMode` carries five, four of them L909   `no_progress`.  Two of pair 0029's requirements were lost that way in one L945   # the predicate refused -- on 22 of the corpus's 169 composites -- with a L959   # while excluding pair 0029's identical shape as representation debt. L960   # 0029 has five entries and so went through the branch that notes; 0019, L961   # 0043 and 0053 have one and went through this one.  Same evidence, two L973   # and attribution has nothing to match: on pair 0029 the entry is the L976   # policy -- but the binding came back `safe` and matrix-v16 published L1016  # pair-0006 regression `filtered_route_control:` was introduced to stop. L1062  # verbatim the pair-0029 defect. L1242  # "the failure this gate exists to stop" -- but no gate did, and matrix-v17 L1243  # published one on the first cell that finished: pair 0006's L1251  # findings: EXP-0000-IT-001 and EXP-0029-IT-001 are False at every horizon L1286  # `cycles`**: measured on pair 0018, L1299  # Two things this cost before it was found.  Across v22+v23, 51 of 219 L1313  # measured on pair 0006, `Attack --Attack_Complete--> AttackingTarget` L1396  # Only the root means nothing was committed: on pair 0000 no state is L1665  # `terminates` calls in matrix-v16 were unaffected by the order defect:

### 处置方式

**不删**（它们记录真实的发现过程与教训）。移入 `eval/discover_matrix/` 下的专门文件，docstring 只留 **机制说明**并链接过去。判别标准：

| 留在 docstring | 移出 |
| :-- | :-- |
| 「`_simulate` 构造 `[settle...] + [[trigger]] + [[]...]`，故 cycle 0 在触发之前」 | 「实测 pair 0006：cycle 0 含 Attack…」 |
| 「扫全部帧会在机器本已在目标里而触发把它带走时返回 True」 | 「10/11 个 pair 有此类翻转」「51/219 个 False 是 horizon 假象」 |
| 「`pseudo` 关键字在语料中被不一致使用，故该规则的命中分布是语料属性」 | 「pair 0018 标了九个、0048 标了两个、0038 一个没标」 |

即：**保留「为什么这样实现」，移出「在哪些样本上观测到多少」。**

### ⚠️ 为什么现在不做

7 步流程要求先走完 v24 的第 4–7 步，**避免在解读结果时同时改代码**。且这个改动应与冻结条件 2（`initial_target` 的返回语义修改）**同批**过一次双 review，而不是分两次。

登记为 **v25 第 1 步**的组成部分。本清单使它成为机械操作 —— 不需要重新查找。
