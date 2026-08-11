# 裁定：SoSyM 2026（Sultan / Apvrille / Coudert）—— ⭐ 三路独立判定互相冲突，本方回原文裁定

⭐ 本文件记录一次**必须由人回原文才能收口**的判定。⚠️ L1 的三路 agent 对**同一篇的同一个门**给出了**三个不同答案**，且它们各自都有证据。⛔ 按根 [CLAUDE.md](../../../../CLAUDE.md) §3.8，本方逐字回原文核对后裁定。

**一手材料**：出版方 OA PDF（40 页，`rd.springer.com`），本地提取为纯文本。⚠️ `link.springer.com` 与 `doi.org` 两条入口被 bot 防护挡下（返回约 3 KB 的 HTML 壳）。DOI [`10.1007/s10270-026-01388-4`](https://doi.org/10.1007/s10270-026-01388-4) 解析成功；HAL 记录 hal-05682394，CC-BY。

---

## 1. 三路的判定各是什么

| 路 | 对**门 ②（同对象：状态机类制品）**的判定 | 它的理由 |
| :-- | :-- | :-- |
| **A · 三篇独立复核** | ⛔ **不成立（界外）** | AVATAR 的迁移自带时间约束 + block 间并发同步 + 状态集平坦无层次 |
| **B · Q5 专攻** | ⭐ **成立（界内）** | 「SMD 定义为 $(S,T)$ 有向图 + guard/action/attribute/signal，**无时钟无不变式**；timed automata 仅在 §1 作为 view 举例出现」 |
| **C · Q3 专攻** | ⚠️ **部分成立** | 输入**包含** SMD，⛔ 但缺陷类是「与用例图之间的逻辑依赖错配」，**不是状态机内部缺陷** |

⚠️ 三路还对**落选的是哪一道门**给了不同答案：A 判 ②、C 判 ④（口径可复现）、B 认为 ②③ 之外主要缺 ④。

---

## 2. ⭐ 本方裁定：⛔ **门 ② 不成立**，且有**两条互相独立**的理由

### 理由一 · 形式主义本身越界 —— ⭐ B 路的「无时钟」是**错的**

原文 **Definition 3（Transition Descriptions）**逐字（提取文本第 578–583 行，PDF 第 8 页）：

> `TransDescr is the set of transition descriptions d = ⟨after, guard, actions⟩ where:`
> `– after ∈ N constrains the delay before firing t.`
> `– guard is a propositional formula that must evaluate to true to enable t.`
> `– actions is a sequence of actions executed when t is fired.`

⭐⭐ **`after` 是迁移描述三元组的第一个分量，⛔ 不是可选注解。** 每一条迁移描述都携带一个「触发前的延迟约束」。⛔ 而本文的建模对象是 $M = (S, E, V, Tr, A)$，**无时钟 $C$、无不变式 $Inv$** —— ⭐ 一个逐迁移强制的 `after ∈ N` 就是时间语义在对象内部。

⚠️ **B 路错在哪**：它读了 **Definition 4**（`A state machine diagram is a directed graph (S ∈ ℘(States)\{∅}, T ⊆ Trans_S)`）就下了「无时钟」的结论 —— ⛔ 但 `Trans = States × States × TransDescr`，**时间约束藏在 `TransDescr` 里**，Definition 4 的那个「有向图」写法把它包在下一层。⭐ **只读顶层定义会漏掉下一层的分量。**

⭐ **并发也确实在内**：`actions` 含 `send s(...)` / `receive s(...)` 两类**信号同步**（第 568–573 行），而第 121 行逐字说明依赖关系的遍历是「following its transitions **and transition synchronizations**」—— ⛔ 同步是依赖边构造的一部分，不是外围设施。

### 理由二 · 即便对象过门，⛔ **缺陷谓词也不落在状态机内部** —— ⭐ C 路这一点成立

⭐ 该篇检的是 **UCD ↔ AVATAR 模型**之间的**跨视图逻辑依赖**一致性。⚠️ 按 §4.0.2「同一篇论文可以部分可用，判据是**我们引的那一段**讲的是不是界内对象」，⭐ 判法应当是**看缺陷的谓词落在谁身上**：落在跨视图对应关系上，⛔ 就不是状态机内部缺陷。

⛔ **两条理由各自独立**：理由一杀的是「对象」，理由二杀的是「缺陷类」。⭐ 即便有人不接受理由一（例如主张 `after ∈ N` 是离散延迟而非连续时钟），理由二仍然成立。

---

## 3. ⛔ 门 ④（口径可复现）同样不成立 —— ⭐ C 路发现的这条最硬

### graph 通道（Table 8）

**原文数据**（PDF 第 34 页）：`[M-complete] 0/0/0` · `[M-incomplete] 9/0/0` · `[M-faulty] 14/0/0`（列为 `Detected / Errors / Missing`）。

⛔ **`Missing = 0` 没有配套的期望缺陷总数。** 原文只说「as demonstrated earlier with the first incomplete design, **all expected logical dependency inconsistencies were successfully detected**, and no false pos[itives]…」—— ⚠️ 「all expected」是一句**定性断言**，⛔ 论文从未事前列出该期望集有几条。

⭐⭐ **而同一篇文档在评 LLM 通道时自陈了相反的立场**（第 2233 行逐字）：

> `is subjective and time-consuming to exhaustively identify undetected inconsistencies, we have empirical evidence of their existence, as the graph-based approach identified incon[sistencies]…`

⛔⛔ **同一份文档里，「穷举未检出项」被认定为主观且不可行，却在另一张表上把 Missing 填成了 0。** ⭐ 这不是精度问题，是**分母不存在**：⚠️ 没有独立的期望缺陷清单，`0/23` 与 `0/未知` 无法区分。⛔ 任何换算都只是把作者的自评复制一遍。

⭐ 并且那句自陈还多说了一件事：**他们有 FN 存在的经验证据**（图方法查出了 LLM 通道漏掉的）。

**另三条各自独立的削弱**：三个模型是**作者自造**（第 1952 行逐字 `These three models, we have designed, represent:`）· $n = 3$、单系统、单缺陷类 · 检测器是确定性图比较，⭐ **`@k` 这一维不存在**。

### LLM 通道（Table 7）

⛔ **门 ③ 直接失守。** 原文 §6.3 Construct validity 逐字（第 2349–2350 行）：

> `measurements currently account for true positives and false positives, but not false negatives. However, we observed the presence of false negatives`

⭐ 那个 92% 的分母是「**本方法检出的条数**」，⛔ 不是「存在的条数」—— **它是 precision，不是 recall**。⛔ 缺 FN 项则无法由 precision 反推 recall。

⭐⭐ **A 路发现的另一条，Q3/Q5 都漏了**：§5.1.3 逐字（第 1873–1874 行）列出送进 LLM 的东西 ——

> `the request sent to the AI engine contains above-mentioned constraints, the question/query, the system specification, and the UCD and BD in textual format`

⛔⛔ **状态机图从未进入 LLM 通道的检测 prompt**；Table 7 的行也**只有 BD 与 UCD，无 SMD 行**。⭐ 故 LLM 通道**同时缺 ②③④**。

⚠️ **一处同一指标两个数**：§6.1.1 写「automatic resolution of **85.5%**」（= Table 7 的 59/69 聚合），§6.3 写「ranges from 50% to 100% per diagram, with an average of **87%**」（逐图均值）。⛔ 引用时必须指明是哪一种平均。

---

## 4. ⭐ 裁定结论

| 通道 | ① 同任务 | ② 同对象 | ③ 有 recall | ④ 口径可复现 | 结论 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **graph（Table 8）** | ✅ | ⛔ **否**（两条独立理由） | ✅ 字面有 `Missing` 列 | ⛔ **否**（分母不存在） | ⛔ 不作参照系 |
| **LLM（Table 7）** | ⚠️ 部分（受检图由同一流水线生成，属自检） | ⛔ **否**（状态机图未进 prompt） | ⛔ **否**（自陈不计 FN） | ⛔ n/a | ⛔ 不作参照系 |

⭐ **它仍是本轮最接近的一篇**，⛔ 但接近的方式与 S1 预判的不同：⚠️ S1 说 graph 通道「四门字面全中」而由四条外部理由否决；⭐ **实际是门 ② 与门 ④ 各自就已经否决了它**，⛔ 走不到那四条理由。⭐ 那四条理由 L1 逐条核过**全部属实且引文准确**，作为补充仍有效。

---

## 5. ⭐⭐ 这次冲突的方法论收获

1. ⛔ **只读顶层定义会漏掉下一层的分量。** ⚠️ B 路读 Definition 4 的「有向图」判「无时钟」，而时间约束在 `TransDescr`（Definition 3）里 —— ⭐ 形式化定义是**分层**的，判边界门必须**展开到叶子**。
2. ⭐ **「落选的是哪一道门」比「结论是什么」更容易出错，也更重要。** ⚠️ 三路对最终处置几乎一致（都不作参照系），⛔ 但落选门各不相同 —— ⭐ **而理由正是审稿人会追问的那一层。**
3. ⭐ **同一篇文档的两处自陈可以互相矛盾，⛔ 而矛盾本身就是最强的证据。** ⚠️ 本例中「穷举未检出项主观且不可行」与「Missing = 0」出自同一篇 —— ⭐ 引用这个矛盾，比引用我们自己对它的批评更有力。
4. ⭐ **多路独立判定的价值不在「多数票」，在于它们各自看到的不同东西。** ⚠️ 本例三路各贡献了一块：A 路的「状态机图未进 prompt」（Q3/Q5 都漏了）· C 路的「分母不存在」（A 路只说了作者自造）· B 路的错误反而定位出「分层定义」这个陷阱。⛔ 若只跑一路，无论哪一路都会交出一份有缺口的判定。
