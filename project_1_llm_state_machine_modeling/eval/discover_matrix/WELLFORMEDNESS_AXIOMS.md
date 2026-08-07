# 合式性公理表（预注册草案，**尚未冻结**）

由一位**对失败分析完全盲**的执行者从规范推导，隔离清单见 [RULE_PROVENANCE.md](./RULE_PROVENANCE.md)。交付 **4 条**
（上限 6 条），另有 7 条候选被主动剔除并附理由。

⚠️ **本文件尚未冻结。** 冻结条件见 §五。

## 一、四条公理

| # | 公理 | 规范出处 | 可执行形式 |
| :-- | :-- | :-- | :-- |
| **A1** | 复合态的默认入口必须**唯一且无条件** | UML 2.5.1 §14.2.3.2、§14.2.3.7、OCL 约束 `initial_vertex` / `initial_transition` | `initial_target(composite=p, child=c)` 恰有一个为 True |
| **A2** | 已声明的迁移必须可实现（**已按 §二① 退回普通形态，无叶量化**） | UML 2.5.1 §14.2.3.9 | `occupancy_after(source=s, trigger=e, target=t, within_cycles=k)` |
| **A3** | 同源同触发的备选迁移，守卫必须**两两不相交** | UML 2.5.1 §14.2.3.7（Choice：多守卫为真时选择算法**未定义**；无守卫为真时模型 **ill formed**） | `guard_distinguishable(source=s, trigger=e)` |
| **A4** | 已声明的迁移效果必须**真实生效** | UML 2.5.1 §14.2.3.9、§14.2.3.4.5–6 | `effect_declared` → `variable_delta_after` 对偶 |

形式化陈述（只含量化变量，无任何具体元素名）：

$$\forall p \in S:\ \mathrm{comp}(p) \Rightarrow \exists ! \, c \in S:\ \mathrm{child}(p,c) \land \iota(p,c) \land \mathrm{uncond}(p,c)$$

$$\forall s \in S,\ \forall e \in E,\ \forall t_1,t_2 \in Tr(s,e):\ \mathrm{tgt}(t_1) \neq \mathrm{tgt}(t_2) \Rightarrow \neg\,\mathrm{Sat}(g_{t_1} \land g_{t_2})$$

$$\forall (s,e,t) \in Tr:\ \forall v \in V:\ \forall \sigma \in \\{+,-\\}:\ \mathrm{Eff}(s,e,v,\sigma) \Rightarrow \mathrm{Delta}(s,e,v,\sigma)$$

**A2 的终版形式**（退回后，$\mathrm{Leaf}(s) = \{s\}$）：

$$\forall (s,e,t) \in Tr:\ \exists k \le K:\ \mathrm{Occ}(s,e,t,k)$$

即「已声明的迁移必须在其源上可实现」，**不再按 $\mathrm{Leaf}(s)$ 量化**。

代价与收益都要写明：**与 pyfcstm 的重叠度上升、增量下降**（`W_TRANSITION_SHADOWED` /
`W_GUARD_CONST_FALSE` / `W_DEAD_GUARD` 覆盖了部分成因），但**污染嫌疑归零**。叶量化维度可在未来某代次
作为独立公理重新预注册，条件是由一位读到**干净的** `predicate_api.py` 的执行者推导（§三 处置第 1 项完成
之后）。

## 二、我对推导者三个提问的裁决

### ① A2 的叶量化维度 —— **裁决：退回不带叶量化的形态**

推导者的原始 A2 按 $\mathrm{Leaf}(s)$ 量化（复合态上的边必须在其**每个叶配置**上可实现，除被下层声明覆盖）。
它主动披露：公理**内容**来自 UML §14.2.3.9.3（复合态上的迁移被全部子状态继承，这是规范事实），但**"去检查
这一维"这个念头的触发源**是 `_simulate` / `_settle_cycles` 的 docstring —— 而那些 docstring 含语料统计
（"704 bindings across 58 of the 60 pairs"）。

**裁决：退回 $\mathrm{Leaf}(s) = \\{s\\}$ 的普通形态。**

理由不是"内容有问题"，而是**动机审计会命中它，而且判得对**：

> 最可靠的判据是查引入动机，不是列举形态（§3.5）

推导者自己说它「最容易被质疑是不是为某种情形定制」。当**推导者本人不确定**时，保守选项是唯一站得住的。

📌 **注意这个裁决的方向：退回会降低方法的发现面，也就是降低我的数字。** 这一点使它更可信 —— 若我选
保留，无论论证多规范都无法与"为达标而放宽"区分开。

叶量化维度可在**未来某代次**作为独立公理重新预注册，条件是由一位读到**干净的** `predicate_api.py`
的执行者推导（见 §三）。

### ② A1 的谓词硬限制 —— **裁决：改谓词，但不在本代次**

推导者查明：`initial_target` 在「≥2 条无条件入口」与「零条无条件入口」两种情形下 **`raise
UnsupportedEvidence`**，不返回 `False`。即 **A1 最有价值的那半边其违反会落成 `unsupported` 而非 finding**。

它建议改 `initial_target`，理由是「放弃复合态入口确定性检查在学术上不可辩护」。**我同意这个判断**，
但改动时机受两条约束：

1. **v24 正在运行，pipeline src 冻结** —— 不得中途改
2. 改一个谓词的返回语义会影响**所有**用它的断言，须走完整双 review

故登记为 v25 的第一项，与公理表冻结同批。

### ③ 「默认入口不得指向 pseudo 结点」的剔除 —— **裁决：剔除正确，且这条剔除本身是本次最有价值的产出**

推导者剔除它的理由是：`_reject_transient_subject` 的 docstring 记载 `pseudo` 关键字在语料中被**不一致
使用**（同样语义的路由结点在某些制品里标了 `pseudo`、在另一些里写成普通叶态）。

> 这意味着该公理的命中分布是**语料生产方式的属性**，不是方法能力的属性 —— 收录它会把语料工件计成发现
> 能力。

**这条剔除比任何一条收录更有价值**，因为它识别了一类我此前没有名字的错误：**用一条规则去检测语料自身
的不一致，然后把命中记为方法能力。** 那不是特化（规则本身通用），但它同样使能力主张失效。

## 三、⚠️ 结构性问题：`predicate_api.py` 的 docstring 含实验结果

推导者的披露：

> 第 2、3 两个文件（任务指定必读）的 docstring 与注释中**大量包含实验结果性内容** —— 具体 pair 编号、
> "matrix-v16 / v17 / v20 / v22+v23 published X as a confirmed defect"、`EXP-0000-IT-001` 这类条目 ID、
> 以及"51 of 219 False results (23.3%)"这类统计。

**这是我写进去的**，理由是"保留发现过程"。后果有两层，我逐层查了：

### 第一层（已排除）：不是实验泄漏

| 检查 | 结果 |
| :-- | :-- |
| `__doc__` / `inspect.getsource` / `getdoc` 用法 | **0 处** |
| 8 个语料统计探针在 v23 全 66 格 record 中 | **全部 0**（`matrix-v` 的 66 处命中全在 `.log` 的 output-dir 路径里，不在 record 内容中） |
| 送模型的谓词目录 `predicates.py` 含 pair 编号 / 条目 ID / 统计 | **0 处** |

**docstring 不进 prompt，未污染被测对象。**

### 第二层（成立）：污染了规则编写侧

任何未来的盲态推导都必读这些文件。本次推导者是**自己识别并披露**了这一点，还给出了补救建议 ——
但下一位可能不会。

### 处置

**不删这些 docstring**（它们记录了真实的发现过程与教训，删掉会丢失可追溯性），改为**隔离**：

1. 把语料统计与代次编号从 `predicate_api.py` 的 docstring 移入 `eval/discover_matrix/` 下的专门文件，
   docstring 只留**机制说明**并链接过去
2. `RULE_PROVENANCE.md` 的隔离清单增列 `predicate_api.py` / `predicates.py` 的**当前版本**为"结果邻接"，
   要求推导者只把它们当可执行性证据、不用于决定收录哪条
3. 在移出完成之前，任何盲态推导的产出都必须附一份"哪些判断受结果邻接文本影响"的自查 —— 本次推导者
   已自发做到，应固化为要求

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

1. [ ] UML 2.5.1（OMG formal/17-12-05）**原文逐字核对** —— 推导者未能直接取到 PDF，条款号经二手来源交叉
   核对，须人工复核
2. [ ] `initial_target` 的返回语义修改（§二②）落地并过双 review
3. [ ] `predicate_api.py` 的结果邻接文本移出（§三处置第 1 项）—— **待移清单已精确定位，见 §六**
4. [x] **A2 已按 §二① 退回普通形态并重新表述**（2026-08-07）—— 终版形式见 §一，代价（与 pyfcstm 重叠
   度上升、增量下降）已写明
5. [ ] 冻结后写入 `holdout.json` 或等价冻结文件，记录 `frozen_at` commit

**冻结后不允许运行期追加。** 追加一条须重走盲态推导（[RULE_PROVENANCE.md](./RULE_PROVENANCE.md)）。


## 六、条件 3 的待移清单（29 行，精确定位）

`predicate_api.py` 里含结果邻接文本的行（代次名 / 条目 ID / pair 编号 / 语料统计）：

    L10    On pair 0006 that produced ``init state("X"); check exists_always <= 1:
    L331   seal path.  The third was measured to constrain nothing: 60 of 60 pairs
    L465   the model is answerable for. Across the v20 hold-out set the same shape produced 17
    L466   published findings on pairs `0018` and `0038`.
    L472   *inconsistently*: pair `0018` marks nine routing nodes `pseudo state`, while `0048`
    L474   marks nothing. So the rule reaches `0018` and `0038` and not `0048` -- a property of
    L511   runs 2 to 7 edges deep.  matrix-v16 published one of those as a confirmed
    L512   defect: pair 0050's `AutonomousMode` settles `SubState1 -> SubState2 ->
    L588   than a leaf came back False.  Measured on pair 0000 -- pinned at
    L596   consumed: pinned at pair 0000's root, that cycle reports "no stoppable
    L716   # on pair 0006 the only effect on the Attack_Complete
    L897   a converted one: pair 0029's `HighwayMode` carries five, four of them
    L909   `no_progress`.  Two of pair 0029's requirements were lost that way in one
    L945   # the predicate refused -- on 22 of the corpus's 169 composites -- with a
    L959   # while excluding pair 0029's identical shape as representation debt.
    L960   # 0029 has five entries and so went through the branch that notes; 0019,
    L961   # 0043 and 0053 have one and went through this one.  Same evidence, two
    L973   # and attribution has nothing to match: on pair 0029 the entry is the
    L976   # policy -- but the binding came back `safe` and matrix-v16 published
    L1016  # pair-0006 regression `filtered_route_control:` was introduced to stop.
    L1062  # verbatim the pair-0029 defect.
    L1242  # "the failure this gate exists to stop" -- but no gate did, and matrix-v17
    L1243  # published one on the first cell that finished: pair 0006's
    L1251  # findings: EXP-0000-IT-001 and EXP-0029-IT-001 are False at every horizon
    L1286  # `cycles`**: measured on pair 0018,
    L1299  # Two things this cost before it was found.  Across v22+v23, 51 of 219
    L1313  # measured on pair 0006, `Attack --Attack_Complete--> AttackingTarget`
    L1396  # Only the root means nothing was committed: on pair 0000 no state is
    L1665  # `terminates` calls in matrix-v16 were unaffected by the order defect:

### 处置方式

**不删**（它们记录真实的发现过程与教训）。移入 `eval/discover_matrix/` 下的专门文件，docstring 只留
**机制说明**并链接过去。判别标准：

| 留在 docstring | 移出 |
| :-- | :-- |
| 「`_simulate` 构造 `[settle...] + [[trigger]] + [[]...]`，故 cycle 0 在触发之前」 | 「实测 pair 0006：cycle 0 含 Attack…」 |
| 「扫全部帧会在机器本已在目标里而触发把它带走时返回 True」 | 「10/11 个 pair 有此类翻转」「51/219 个 False 是 horizon 假象」 |
| 「`pseudo` 关键字在语料中被不一致使用，故该规则的命中分布是语料属性」 | 「pair 0018 标了九个、0048 标了两个、0038 一个没标」 |

即：**保留「为什么这样实现」，移出「在哪些样本上观测到多少」。**

### ⚠️ 为什么现在不做

7 步流程要求先走完 v24 的第 4–7 步，**避免在解读结果时同时改代码**。且这个改动应与冻结条件 2
（`initial_target` 的返回语义修改）**同批**过一次双 review，而不是分两次。

登记为 **v25 第 1 步**的组成部分。本清单使它成为机械操作 —— 不需要重新查找。
