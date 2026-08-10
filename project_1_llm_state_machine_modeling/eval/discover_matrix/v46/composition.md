# v46 意外发现成分分析：五大类的子类体系与划分维度

**本文件只写「怎么分、每一类是什么意思、为什么这么分」。全部计数、占比与交叉表在唯一产地
[unexpected_tables.md](./unexpected_tables.md)** —— 它整份由 `unexpected_verdicts/G*.jsonl` 经
[../rebuild_unexpected.py](../rebuild_unexpected.py) 生成。本文件**不保存任何一份副本**：
手工副本一旦与真源分岔，读者无从判断哪一份有效。

全量 286 条目逐条阅读裁定，各大类由独立分析员分别负责，每类要求「不许有其他类」。
裁定口径见 [UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)；逐簇判据见
[unexpected_evidence.md](./unexpected_evidence.md)；机器可读真源在
[unexpected_verdicts/](./unexpected_verdicts/)，每簇带 `verdict` / `subclass` / `merge_key` / `merge_reason`。

## ⛔ 两套分母，必须同时读

- **条目数**：原始簇数。
- **去重数**：不同 `merge_key` 的个数，去重单元 = `(pair, 根因)`。
  同 pair 同一处失误合并计 1；**不同 pair 即使类型相同也不合并**（不同制品上的不同实例）。

两套分母给出**不同的主要矛盾**：按条目读是「编译债务最大」，按去重读是「断言侧过度规定最大」。
成因是表示债务的条目/去重比远高于无 NL 依据——同一处损失被反复重述的程度高得多。
**只报一套会得出错误的整改优先级。** 双分母全表见
[unexpected_tables.md 表 1](./unexpected_tables.md)。

## ⛔ 去重可审计：每一次合并都有理由

去重把分母改小，**改小分母必须能被复核**——否则「132 条其实只有 29 处」这句话无从验证。
因此每个 `merge_key` 组都带一句自然语言 `merge_reason`，单成员组也写明「单条，无合并」，
**不留空**（空值与「没写理由」在表里长得一样）。

**审计入口**：[unexpected_verdicts/merge_groups.tsv](./unexpected_verdicts/merge_groups.tsv)
—— **123 组 = 44 个多成员组 + 79 个单成员组**，字段
`merge_key | verdict | subclass | pair | 成员数 | 成员簇 | 累计格次 | merge_reason`。
`merge_key` 列可直接与
[unexpected_verdicts/cluster_index.tsv](./unexpected_verdicts/cluster_index.tsv)
的同名列 **join**，逐簇追到它属于哪一组、为什么被判为重复。
合并规模前 10 见 [unexpected_tables.md 表 5](./unexpected_tables.md)。

⛔ **工具层三道硬门**（[../rebuild_unexpected.py](../rebuild_unexpected.py)）：
`merge_key` / `merge_reason` / `subclass` 任一缺失即 `SystemExit`；
`merge_key` 跨 `verdict` / `subclass` / `pair` 即报「去重单元被破坏」；裁定不在五类内即拒绝执行。
配套测试见 [../test_rebuild_unexpected.py](../test_rebuild_unexpected.py)。

⚠️ **条目/去重比本身是数据**：比值高有两种解释——「该缺陷天然被多个谓词命中」（缺陷属性）
与「产出侧在重复报同一件事」（产出质量问题）。**各大类的分析员独立判断，结论一致指向后者**，
依据一致：膨胀集中在**同一个谓词**内部（`D1` 的 59 簇里 52 条挂 `event_declared`；
`N-SPLIT` 的 33 簇里 32 条挂 `event_declared`），而非跨谓词发散。

## ⛔ 头条结论：净增量是 2 条

**286 条目里，通过「事实为真 + 作者源确实没写 + NL 有逐字依据 + 台账未记」四条判据的只有
`0014-4`**（`EmergencyStopping` 的发送信号写成裸描述行）。它站得住靠的是**台账自身的不一致**：
同一份 NL 下 0024（写法更强，只是挂错元素）与 0034（完全没写）都记了 E1，
唯独 0014（严格弱于 0024、实质等同 0034）判 `similar` 未记；
而同卷宗对**同一状态相邻一行**的裸描述行判的是 `problem`。

⛔ **论文里能说的净增量是 2 条。**

### 边界上最接近真漏记的两组，为什么不算

- **0023（6 簇）是越界**：台账同族记录 `EIS-0002-01`/`0033-01`/`0053-01` 的 `reference_side`
  与 0023 作者源**逐字相同**；`manual_review/0023-review.json` 判 **`correct`**——
  「与参考模型逐字同构……NL 1/2/3/4/5 的全部内容都被满足」，另一条标 `out_of_scope: 并发`。
  「区间零迁移」是正交区**展平后**才出现的，参考模型同样如此。
- **0017 + 0047 的两个 merge 组（各 8 簇，合计 16）无 NL 依据**：`EIS-0047-03` 的 `nl_evidence` 自陈
  **「NL 未给出任何状态或事件标识符（只有散文描述），故不是 nl_named」**——这是台账
  **对同一句 NL 的既有裁定**；`manual_review/0017-review.json` 对同一主张判 `similar` 而非
  `problem`：「NL 第 2 句本身是三种碰撞之一被检测到的析取，用统一激活事件不违反该句」。
  那只证明拆分**被允许**，不证明 NL **要求**它。

---

以下五节只给**子类的划分维度与含义**。每个子类的条目数、去重数、条目/去重比、涉及 pair 数与
稳定性分布，见 [unexpected_tables.md 表 2](./unexpected_tables.md)。

## ⚙️ 表示债务 `D*`

**划分维度**：按「丢失的是哪一条区分」切。

| 子类 | 含义 |
| :-- | :-- |
| `D1` | 析取备选融合 —— 丢失「备选之间的可分性」（`or` 被强化成 `and`） |
| `D2` | 原子子表达式不可寻址 —— 丢失「该量是一等实体」 |
| `D3` | 槽位焊死 —— 丢失「槽位角色」（`trigger / effect` 未在分隔符处切分） |
| `D4` | 结构性下沉债务 —— 丢失「谁是真正的初始态 / 层次深度」 |
| `D5` | 跨通道打包 —— 一簇同时跨 ≥2 个损失通道 |

## 📄 无 NL 依据 `N-*`

**划分维度**：按「相对 NL 真实义务，多要求的那一部分是什么」切。

| 子类 | 含义 |
| :-- | :-- |
| `N-SPLIT` | 要求把复合条件拆成独立元素（撤掉「必须分立」即一致） |
| `N-SPLIT-PROSE` | 散文析取被读成具名事件枚举（NL 只有散文、无标识符，报告者虚构名） |
| `N-FUSE` | 统称/整体被要求成一个单一元素（**方向与 `N-SPLIT` 相反**） |
| `N-CTX` | 语境/状语措辞被抬成同名元素（`During flight` / `powered on`） |
| `N-FORM` | 承载构件/相位被过度指定（要求 `during` 动作，NL 只是解释含义） |
| `N-ANCHOR` | 义务被绑到 NL 未定或定为他者的锚点上（松开锚点即成立） |
| `N-KIND` | 范畴错置：把 NL 里**被比较的量**当成事件，或把输出动作当成输入事件（`dist_to_front` 是量不是信号，`Send` 是输出动作不是输入事件） |
| `N-META` | 建模元语言术语被抬成模型内元素（`region` / `substates`） |
| `N-CLOSED` | 把 NL 当穷尽规约（要求排他或定数） |
| `N-MODAL` | 定性表述被强化为时序不变式（`continuously` 当驻留义务） |

## ❌ 假阳性 `FP-*`

**划分维度**：按「索要形式与实际承载者差在哪一个槽位」切。

| 子类 | 含义 |
| :-- | :-- |
| `FP-N` | 名字槽差 —— 同类别承载者在场，仅标识符字面不同 |
| `FP-K` | 类别槽差 —— 承载者以 `action` 存在，断言按 `event` 索要 |
| `FP-A` | 谓词锚点错置 —— 触发只能锚在源态，断言却锚到了目标态。**事实为假**，这是与 `N-ANCHOR` 的分界 |
| `FP-0` | 零槽差 —— 四槽全对、属性实际成立，断言仍判假 |

## ✅ 真漏记 `V*`

**划分维度**：按「作者的失误方式」切。

| 子类 | 含义 |
| :-- | :-- |
| `V1` | 惰性散文占位 —— 作者写了名字但写在不承载语义的位置 |

## 🚫 越界 `OOS-*`

**划分维度**：按「越的是哪条边界」切。边界定义见
[../NL_SCOPE_RULE.md](../NL_SCOPE_RULE.md)。

| 子类 | 含义 |
| :-- | :-- |
| `OOS-FLATTEN` | 正交区展平产物被当作作者缺失迁移 |
| `OOS-INV` | 不变式 + 并发保持（双重越界） |
| `OOS-REGION` | 区数量义务 |
