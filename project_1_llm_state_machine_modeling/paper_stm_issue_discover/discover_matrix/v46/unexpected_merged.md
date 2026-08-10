# v46 意外发现归并后的问题清单

⚠️ **本文件的簇级数字由 [unexpected_verdicts/](./unexpected_verdicts/) 的 `G*.jsonl` 汇出，jsonl 是真源。**
⛔ **全部交叉表只有一个产地**：[unexpected_tables.md](./unexpected_tables.md)，由
[../rebuild_unexpected.py](../rebuild_unexpected.py) 机器生成。**本文件不保存任何一张交叉表的副本。**

簇不是缺陷。同一个缺陷会以不同谓词、不同命名、不同 roll-up 粒度反复产出，
因此一切计数都给两套分母：**条目数**（原始簇数）与**去重数**（不同 `merge_key` 的个数，
去重单元 = `(pair, 根因)`；同 pair 同一处失误合并计 1，不同 pair 不合并）。

桶内 **288 条目 / 124 去重 / 43 个 pair**。逐簇判据见 [unexpected_evidence.md](./unexpected_evidence.md)，
结论与判据链见 [unexpected_adjudication.md](./unexpected_adjudication.md)，
成分与子类含义见 [composition.md](./composition.md)。

## 一、✅ 真实台账漏记：1 条

**`0014-4`（`V1` 惰性散文占位）是 v46 相对台账的唯一净增量。**
[unexpected_verdicts/final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv) 只有一行。

作者源 `stm0.puml:26` 把 NL 3 要求发出的 Obstacle Detected 信号写成 PlantUML **描述行**
（`EmergencyStopping: Obstacle Detected`）而非动作语法，`EmergencyStopping` 内因此无任何
`enter` / `during` 动作；台账 `EIS-0014-03`（`nl_evidence` 只引「Emergency Stop」）与
`EIS-0014-04`（scope 是 `InMotion.Approaching`）均不覆盖。逐条判据见
[unexpected_adjudication.md §三](./unexpected_adjudication.md)。

⚠️ 它只出现在 6 格中的 2 格；补入台账会使 `hit@all` 下降，不是「分母不变故无影响」。

## 二、🔗 内容已被台账承载者：不属意外发现，不在分母内

13 条经复核确认与现有台账记录**同根**，按定义不是意外发现，物理存放在
[unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)。
判「同根」的硬判据（数作者源上的引用次数）见
[unexpected_taxonomy.md](../docs/protocol/unexpected_taxonomy.md) 「先做零步」。

按**对命中的影响**分四类（jsonl 的 `disposition` 字段）：

| disposition | 条数 | 簇 | 含义 |
| :-- | --: | :-- | :-- |
| 真漏配 | 1 | `0037-1` | 内容对应 `EIS-0037-01`，属匹配器漏配，移出本桶 |
| 冗余复述 | 6 | `0006-3` `0016-2` `0016-11` `0026-4` `0035-1` `0035-2` | 目标记录在全部 6 格已由同格另一条 issue 认领，无格可翻 |
| 同根但该格未建立记录 | 3 | `0006-2` `0036-8` `0047-9` | 逐格复核维持未命中 |
| 报的是已退役判据 | 3 | `0050-2` `0050-3` `0050-4` | 台账 `EIS-0050-01` 的 `basis_superseded_by_ruling` 明写原判据已放弃 |

**移出 ≠ 记命中**：13 条全部只是「不属于意外发现」，无一产生新增命中。`0037-1` 的命中判定按 [hit_criterion.md](../docs/protocol/hit_criterion.md) §4.2 的引用次数判据裁定为未命中——模型点名的多余子是四个，含台账认定正确的 `Inactive`，是严格超集而非同一处失误。

## 三、⚪ 断言在冻结制品上为真：真阴性，两侧都不存在

2 条（`0044-2`、`0054-1`）的断言在冻结制品上求值为 **True**——被测模型**满足**该义务，
因而正确地不产出任何 issue。它既不在覆盖侧（无对应台账记录），也不在多报侧（无产出可判）。
明细见 [unexpected_verdicts/not_produced.jsonl](./unexpected_verdicts/not_produced.jsonl)。

由此闭合：`288 + 14 + 2 = 304`（[unexpected_tables.md](./unexpected_tables.md) 表 0）。

## 四、⚙️ 表示债务：按条目最大的一块

**不是模型缺陷，是我们自己 R4.5 编译（PlantUML → FCSTM）的信息损失**——作者在源制品上
已逐字表达，是中间表示装不下。机制见
[unexpected_adjudication.md §一之二](./unexpected_adjudication.md)，
完整论述见 [representation_debt.md](../docs/findings/representation_debt.md)，
条目 / 去重 / 稳定性见 [unexpected_tables.md](./unexpected_tables.md) 表 2。

子类按「**丢失的是哪一条区分**」切，⛔ 谓词族不参与判类：

| 子类 | 丢失的区分 | 作者源实际写法 |
| :-- | :-- | :-- |
| `D1` 析取备选融合 | 备选之间的可分性（`or` 被强化成 `and`） | `a \| b & c \| d` 一条合法析取守卫，整条被压成一个原子事件名 |
| `D2` 原子子表达式不可寻址 | 该量 / 该条件是一个可寻址的一等实体 | `front_distance > 10` 只活在守卫文本里；PlantUML 无变量声明语法 |
| `D3` 槽位焊死 | 槽位角色（哪段是触发、哪段是效果） | `Attack Complete / UAV Count Decreased` 未在 `/` 处切分 |
| `D5` 跨通道打包 | 一簇同时跨 ≥2 个损失通道 | 索要串里既含析取支又含合取分量 |
| `D4` 结构性下沉债务 | 谁是真正的初始态 / 层次深度 | 作者写了合法的区内 `[*]`，R4.5 另注入 `UnspecifiedInitial` |

**关键分界线**（各自都踩过坑）：`D1` vs `D2` 看被指串**是不是一个完整析取支**；
`D2` vs `D3` 看该量写在**守卫侧**还是 `/` **之后的效果槽**；`D5` 要通过正向计数测试
（枚举分量归类结果 ≥2 种），**不是兜底类**。判定流程见
[unexpected_taxonomy.md](../docs/protocol/unexpected_taxonomy.md)。

## 五、📄 无 NL 依据 / ❌ 假阳性 / 🚫 越界

**不设「待定」**——证据不足不构成一个裁定类别，取不到证据就实跑
`SimulationAPI` / `FBMCQAPI` 取反例。三类的子类分布见
[unexpected_tables.md](./unexpected_tables.md) 表 2，含义见 [composition.md](./composition.md)。

三条按整改价值排序的结论：

1. **拆分类过度规定是唯一系统性的一支**：`N-SPLIT`（要求把复合条件拆成独立元素）的
   ≥4 格簇数是全部子类里最高的，不是单次采样噪声；`N-SPLIT-PROSE`（NL 只给散文、无标识符，
   报告者必须自己造名）的条目/去重比是全部子类里最高的，因为**造名空间无上界**。
   两者合计 49 条目 / 15 去重，属 prompt 侧可收敛项。
2. **语境措辞与承载相位被过度指定**（`N-CTX` + `N-FORM`，33 条目 / 20 去重）：NL 的统称词、
   语境状语、`indicating that…` / `where the … is …` 式语义注解都不构成元素义务。
3. **假阳性以名字槽差与类别槽差为主**（`FP-N` + `FP-K`）：承载者其实在场，
   只是标识符字面不同、或以 `action` 而非 `event` 存在。⚠️ 后者的直接成因是证据包的路径清单
   **不列 action**，见 [unexpected_adjudication.md §五](./unexpected_adjudication.md)。

**越界（`OOS-*`）**三个子类：`OOS-FLATTEN`（`0023` 的正交区展平产物被当作作者缺失迁移——
参考模型同样零事件零迁移，不可归因于被测模型）、`OOS-REGION`（`0056-1` / `0007-3` 的区数量义务，
R-REGION 规则）、`OOS-INV`（`0017-7` / `0027-6` 的不变式 + 并发保持，双重越界）。判据与风险披露见
[unexpected_adjudication.md §三之二](./unexpected_adjudication.md)。

**测量链侧待修项**已登记于
[defects_registered.md](../docs/findings/predicates/defects_registered.md)（本桶内涉及
`0046-8` / `0044-4` / `0054-5` / `0026-3`），登记区分**词表**与**实现**：谓词词表冻结（不增删谓词，否则作废跨代次可比性），求值实现的缺陷该修就修——P-1 / P-2 已实施，P-3 / P-4 未实施。

## 六、相对上一版的改动


- 交叉表统一归口到 [unexpected_tables.md](./unexpected_tables.md)，本文件只留链接与结论。
  **理由**：手工副本无法随裁定变更同步，会让同一目录内出现两个互斥的答案。
- 分母切换为清洗后的口径（桶内 288 条目 / 124 去重），并新增 §三 把真阴性单列，使
  `288 + 14 + 2 = 304` 在本文件内即可闭合。**理由**：真阴性既不在覆盖侧也不在多报侧，
  混进任一侧都会让该侧分母失真。
- §二 的分类改为直接取 `ledger_accounted.jsonl` 的 `disposition` 字段并列出簇号。
  **理由**：该表此前不可追溯到具体记录，无法复核。
- 子类改用 `rebuild_unexpected.py` 校验的 `D*` / `N-*` / `FP-*` / `OOS-*` / `V1` 体系，
  §四 只保留划分维度与分界线，不再复述条目数。**理由**：条目数属交叉表内容，只应有一个产地。
