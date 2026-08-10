# v46 意外发现归并后的问题清单

⚠️ **本文件的簇级数字由 [unexpected_verdicts/](./unexpected_verdicts/) 的 `G*.jsonl` 汇出，jsonl 是真源。**

簇不是缺陷。同一个缺陷会以不同谓词、不同命名、不同 roll-up 粒度反复产出，
本文件把 280 簇按**根因**归并（原 293 条中 13 条内容已被台账承载、按定义不属意外发现，见 §二）。逐簇判据见 [V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)，
结论与交叉表见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)。

## 一、✅ 真实台账漏记（4 条根因 / 23 簇）

归并比 5.8:1。**这 4 条是 v46 相对台账的净增量。**
⚠️ 原列 6 条，其中 `0022-EXTRA` 与 `0057-ENTRY` 已被对抗性复核推翻，详见
[V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md)。
⚠️ 补入台账会使 `hit@all` 下降（这 23 簇全部 ≤3/6），不是「分母不变故无影响」。

逐条根因、并入的簇与作者源判据见
[V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md) 与
[unexpected_verdicts/final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv)。

## 二、🔗 内容已被台账承载者：**不属意外发现，已移出分母**

原 293 条中的 13 条经复核确认与现有台账记录**同根**，按定义不是意外发现，
已物理移出到 [unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)。
**本文件其余各节的分母是 280。**

⚠️ 它们此前被做成第六个裁定类别 `MERGE_INTO_LEDGER`，那是分类错误——
该问题回答的是「这条产出该不该在桶里」，与其余五类回答的「这条产出是什么」不是同一个问题。
该标签已作废，`rebuild_unexpected.py` 见到即报错。

13 条按**对命中的影响**分四类（`disposition` 字段）：

| disposition | 条数 | 含义 |
| :-- | --: | :-- |
| 真漏配 | 1 | `0037-1`，对应 4 个格位原判未命中，已逐格复核翻转并入命中侧 |
| 冗余复述 | 6 | 目标记录在全部格已由同格另一条 issue 认领，无格可翻 |
| 同根但该格未建立记录 | 3 | 逐格复核维持未命中 |
| 报的是已退役判据 | 3 | `0050-2/3/4`——台账 `basis_superseded_by_ruling` 明写原判据已放弃 |

**移出 ≠ 记命中**：13 条里只有 1 条产生了新增命中（+4 位，`hit@1` 360→364）。

## 三、⚙️ 表示债务（4 个子类 / 129 簇）

**不是模型缺陷，是我们自己 R4.5 编译的信息损失。** 详见 [V46_UNEXPECTED_ADJUDICATION.md §一之二](./V46_UNEXPECTED_ADJUDICATION.md)。

| 子类 | 簇数 | 涉及 pair | 作者源实际写法 |
| :-- | --: | :-- | :-- |
| `D2` 析取守卫被压成单一事件名 | 73 | 0009 0019 0027 0029 0039 0049 0056 0059 | `a \| b & c \| d` 一条合法析取守卫 |
| `D1` 守卫文本未成为变量声明 | 45 | 0000 0009 0010 0016 0019 0020 0029 0030 0036 0046 0049 0050 0059 | `front_distance > 10` 写在守卫里；PlantUML 无变量声明语法 |
| `D3` `trigger / effect` 未切分 | 9 | 0016 0036 0046 | `Attack Complete / UAV Count Decreased` |
| `D4` 注入伪态 / 区语义偏移 | 2 | 0027 0043 | 作者写了合法的区内 `[*]`，R4.5 另注入 `UnspecifiedInitial` |



## 四、其余非发现（128 簇）

`无 NL 依据` 100 + `假阳性` 24 + `越界` 4 = 128。**不设「待定」。**子类分布见主文档表 C，逐簇判据见证据附件。

**其中 `N0`（4 簇）需单独跟进**：`0054-1` `0054-5` `0046-8` `0026-3` 的义务来自谓词被操作化的方式而非 NL，
`0054-5` 是构造性不可满足（NL 2/10 恰恰许可该迁移，谓词却禁止），属 CLAUDE.md §13 类缺陷。

**`0056-1` 已裁定 `OUT_OF_SCOPE`**（R-REGION 规则，见 [V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md)）：
作者源 `stm0.puml:10` 是正交区分隔符，region 0 恰为三个 Area，NL 义务已满足；5≠3 系拍平后跨区求和。
