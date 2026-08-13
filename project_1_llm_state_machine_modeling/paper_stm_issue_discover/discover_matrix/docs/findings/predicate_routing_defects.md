# 闭合词表内部的路由缺陷

> ⭐ **本文件记的是一类特定缺陷**:闭合词表自己的描述文字把生产者从某个谓词身边**路由走**,导致该谓词被问的比例极低。
>
> ⭐⭐ **它不是「模型能力不够」,也不是「供给不足」** —— ⭐ 是**规则建立**层的缺陷(角色划分见 [`related_work/neighborhood/TOOL_ROLE_TAXONOMY.md`](../../../related_work/neighborhood/TOOL_ROLE_TAXONOMY.md))。⛔ 修法在词表文字里,不在模型、不在注入更多材料。
>
> ⛔⛔ **本文件的每一条都必须区分「引入动机」与「领域出处」**(`CLAUDE.md` §3.5.-1)。⭐ 只有能给出**不引用台账**的独立论证的那些,才可以作为方法的一部分对外表述。

---

## 1. 已确认并已修的一例:`edge_declared`

**现象**:324 格里被问 **0.0%**,台账 primary 7 条 / 42 位,Δ **+64.3pp**。

**根因**(30 格三臂、事前登记跑前 push 的干预实验查明):

- ⛔ **干预 v1**(只追加四条结构扫描,即让 LLM 自己去扫)→ **仍得 0**
- ⭐ **干预 v2**(解决词表内部的措辞冲突)→ **立刻 4/6**

⭐ 源码注释逐字:`the supply gap is not an oversight, it is what the catalogue instructs`。

**当前状态**:⭐ v2 的修法在 `prompts.py` 的 `X1_SWEEP_CATALOGUE_PRECEDENCE` 里,⛔ **只在 mode 2 生效**(⭐ 刻意的,为保住主臂 prompt hash 与旧代次可复现性)。

⚠️ **两条 `nl_cue` 现已互相一致**(都说「制品含有什么 → `edge_declared`;运行时行为 → `occupancy_after`」),⛔ **但那个一致是「互斥划分」** —— ⭐ 一个描述运行时行为的句子被送去 `occupancy_after` 而**不**同时送去 `edge_declared`。⭐ v2 的贡献正是说清**两个 Requirement 都欠着**,而不是二选一。

---

## 2. ⭐⭐⭐ 未修的一例:`occupancy_after` 的字段说明吸收了 `event_consumed`

**现象**:`event_consumed` 被问 **0.0%**,台账 primary 3 条 / 18 位,主臂 33.3% vs X1 **88.9%**,Δ **+55.6pp**。

### 2.1 机制

⭐ `occupancy_after` 的 `trigger` 字段说明逐字:

> `the declared event path; **the predicate also verifies this event was actually consumed**`

⭐⭐ **这句话让生产者没有理由去拿 `event_consumed`** —— 它宣称自己已经覆盖了那件事。

### 2.2 ⛔⛔ 而这个吸收主张是**过宽的**,可从签名直接看出

| 谓词 | 字段 | 它问什么 |
| :-- | :-- | :-- |
| `event_consumed(source, trigger)` | ⭐ **2 个** | 「这个刺激在这个配置下有没有被处理」—— ⭐ `nl_index` 逐字:`a stimulus must be acted on in some situation -- **its False says nothing there handles it**` |
| `occupancy_after(source, trigger, target, within_cycles)` | ⛔ **4 个,`target` 必填** | 「从这个源、这个触发,**是否落到这个目标**」 |

⭐⭐⭐ **`occupancy_after` 要求点名 `target`;`event_consumed` 不要求。**

⛔ 所以当 NL 说「系统必须响应事件 E」而**不说它去哪**时:

- ⭐ `event_consumed(source=<那个 scope>, trigger=E)` **表达得出**
- ⛔ `occupancy_after` **表达不出** —— 除非凭空编一个 `target`,⭐ 而编出来的 target 若碰巧对,断言就变成真空为真;若碰巧错,报的是错缺陷

⭐⭐ **即:那句吸收主张只在「完整指定的 source→trigger→target 迁移」这个更窄的情形下成立**,而它被写成了无条件的。

### 2.3 ⭐⭐ 引入动机 vs 领域出处(⛔ 这一节决定它能不能报成方法改进)

⛔⛔ **必须承认的动机侧**:⭐ 我方是**因为观察到 `event_consumed` 被问 0.0% 且台账要它**,才去查这条路由的。⭐ **那是 oracle-informed 的** —— ⛔ 与 `X1_STRUCTURAL_SWEEP_SPLITTER` 那个四扫描块同性质,⭐ 而那个块的源码注释自己写着 `That is oracle-informed, and it is why this block must never be reported as a method improvement`。

⭐⭐⭐ **但本条有一个独立的领域出处,而那个出处不引用台账**:

> ⭐ **两个谓词的签名不同**:`occupancy_after` 有必填的 `target`,`event_consumed` 没有。⭐ 因此「`occupancy_after` 也验证事件被消费」这句话,**只在 target 已被指定时成立**;⛔ 对「点名了刺激但没点名去向」的句子,它根本不可表达。⭐⭐ **这是一句关于两个函数签名的事实,只读 `predicates.py` 即可核验,⛔ 与任何 pair、任何台账条目、任何运行结果无关。**

⭐⭐ **所以修法的正当理由应当陈述为**:⭐ 更正一句**事实上过宽**的字段说明,⛔ 而不是「补上一个被问得少的谓词」。⭐ 前者不引用台账,⭐ 后者引用。

⚠️⛔ **两者的措辞差别不是修辞** —— ⭐ 按 `CLAUDE.md` §3.5.-1,**引入动机(某次运行暴露了什么)写 commit body,领域出处(它凭什么成立)写源码注释,⛔ 不得互相冒充**。

### 2.4 建议的修法(⭐ 仍待裁)

⭐ 把 `occupancy_after` 的 `trigger` 字段说明改成**带条件的**表述:说清它验证消费**是作为一次完整 source→trigger→target 主张的副条件**,⛔ 而当句子没有点名去向时应改用 `event_consumed`。

⛔ **不要**做的:⭐ 在 prompt 里加一句「记得也要用 `event_consumed`」—— ⭐ 那是**规则建立**的加法,⛔ 而三个独立团队已报告这类加法使召回**重新分配而非增加**(见 [`related_work/neighborhood/tool_roles.md`](../../../related_work/neighborhood/tool_roles.md))。⭐ 本条的修法是**删掉一句过宽的话**,不是加一条新规则。

---

## 3. ⭐ 待查的两例

⚠️ 同样低提问率、⛔ 但根因未查:

| 谓词 | 被问 | 台账 | Δ | 当前状态 |
| :-- | --: | --: | --: | :-- |
| `reaches` | **27.1%** | 8 条 / 48 位 | **+58.3pp** | ⛔ **根因未查** |
| `guard_distinguishable` | **56.7%** | 5 条 / 30 位 | **+40.0pp** | ⛔ **根因未查** |
| `stays_in` | **0.0%** | ⚠️ **1 条 / 6 位** | +16.7pp | ⚠️ **n 太小,不足以定性** |

⭐ **查法**:照 §2 的形态 —— ⛔ **先看有没有别的谓词的描述文字宣称覆盖了它**,⭐ 再看两者签名是否真的等价。⛔ **不要先假定是能力问题或供给问题。**

---

## 4. ⭐⭐ 这一类缺陷的通用判据

⭐ 从两例归纳(⚠️ **n = 2,⛔ 不外推**):

1. ⭐ **症状**:某谓词提问率极低,⛔ 而**同一格里另一个谓词提问率极高**且两者主题相邻。
2. ⭐⭐ **查证动作**:读那个高提问率谓词的 `nl_cue` 与**全部 `field_specs`** —— ⛔ **不只 `nl_cue`**。⭐ §2 那条就在 `field_specs` 里,⛔ 只读 `nl_cue` 查不出来。
3. ⭐⭐⭐ **判定**:若它含「本谓词也覆盖 X」这类主张,**逐字比对两者签名**。⛔ 签名不等价 → 主张过宽 → **这是一条可独立论证的缺陷**。
4. ⛔ **修法方向**:⭐ **删掉或收窄那句过宽的话**,⛔ **不是加一条新规则** —— ⭐ 后者属规则建立的加法,有三团队的负面报告。

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。⭐ 起因是把 [`TOOL_ROLE_TAXONOMY.md`](../../../related_work/neighborhood/TOOL_ROLE_TAXONOMY.md) 的角色划分拿去和逐谓词提问率对拍。⚠️ **原本想做的交叉表(「谓词主题 NL 能不能点名」× 提问率)做不成** —— ⛔ 那个分类本身分不干净,硬做出来的表没有意义;⭐ 改问「被问得少是因为没信息(信息探索缺位)还是因为词表把句子路由走了(规则建立冲突)」后才查出 §2。⭐ §2 是**新发现**:`occupancy_after` 的 `trigger` 字段说明吸收了 `event_consumed`,⛔ 而 v2 的修法只覆盖 `edge_declared`(该常量里 `event_consumed` 出现 **0** 次、`edge_declared` 出现 **3** 次)。⭐ §2.3 按 §3.5.-1 分开记了引入动机与领域出处。 |
