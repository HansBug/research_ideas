# v46 意外发现归并后的问题清单

⚠️ **本文件的簇级数字由 [unexpected_verdicts/](./unexpected_verdicts/) 的 `G*.jsonl` 汇出，jsonl 是真源。**

簇不是缺陷。同一个缺陷会以不同谓词、不同命名、不同 roll-up 粒度反复产出，
本文件把 293 簇按**根因**归并。逐簇判据见 [V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)，
结论与交叉表见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)。

## 一、✅ 真实台账漏记（4 条根因 / 23 簇）

归并比 5.8:1。**这 4 条是 v46 相对台账的净增量。**
⚠️ 原列 6 条，其中 `0022-EXTRA` 与 `0057-ENTRY` 已被对抗性复核推翻，详见
[V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md)。
⚠️ 补入台账会使 `hit@all` 下降（这 23 簇全部 ≤3/6），不是「分母不变故无影响」。

逐条根因、并入的簇与作者源判据见
[V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md) 与
[unexpected_verdicts/final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv)。

## 二、🔗 应并入已有台账（10 条根因 / 14 簇）

**这些不是漏记，是匹配环节的问题**：台账已有该缺陷，但产出换了个谓词或换了个命名，
按签名归并的匹配器就对不上了。典型是 `terminates` → `persists_until`。

**逐条清单见 [unexpected_verdicts/final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv)**（由 `rebuild_unexpected.py` 从 jsonl 真源生成，不手工维护——本目录曾因手写此表四次出错）。

并入目标与理由写在各簇 jsonl 的 `note` 字段，渲染在 [V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)。


## 三、⚙️ 表示债务（4 个子类 / 129 簇）

**不是模型缺陷，是我们自己 R4.5 编译的信息损失。** 详见 [V46_UNEXPECTED_ADJUDICATION.md §一之二](./V46_UNEXPECTED_ADJUDICATION.md)。

| 子类 | 簇数 | 涉及 pair | 作者源实际写法 |
| :-- | --: | :-- | :-- |
| `D2` 析取守卫被压成单一事件名 | 70 | 0009 0019 0027 0029 0039 0049 0056 0059 | `a \| b & c \| d` 一条合法析取守卫 |
| `D1` 守卫文本未成为变量声明 | 42 | 0000 0009 0010 0016 0019 0020 0029 0030 0036 0046 0049 0050 0059 | `front_distance > 10` 写在守卫里；PlantUML 无变量声明语法 |
| `D3` `trigger / effect` 未切分 | 9 | 0016 0036 0046 | `Attack Complete / UAV Count Decreased` |
| `D4` 注入伪态 / 区语义偏移 | 2 | 0027 0043 | 作者写了合法的区内 `[*]`，R4.5 另注入 `UnspecifiedInitial` |



## 四、其余非发现（127 簇）

`无 NL 依据` 99 + `假阳性` 24 + `越界` 4 = 127。**不设「待定」。**子类分布见主文档表 C，逐簇判据见证据附件。

**其中 `N0`（4 簇）需单独跟进**：`0054-1` `0054-5` `0046-8` `0026-3` 的义务来自谓词被操作化的方式而非 NL，
`0054-5` 是构造性不可满足（NL 2/10 恰恰许可该迁移，谓词却禁止），属 CLAUDE.md §13 类缺陷。

**`0056-1` 已裁定 `OUT_OF_SCOPE`**（R-REGION 规则，见 [V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md)）：
作者源 `stm0.puml:10` 是正交区分隔符，region 0 恰为三个 Area，NL 义务已满足；5≠3 系拍平后跨区求和。
