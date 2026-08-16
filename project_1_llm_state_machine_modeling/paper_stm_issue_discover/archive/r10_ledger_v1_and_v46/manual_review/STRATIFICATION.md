# 候选分层：154 条计入问题里哪些能成为 expected issue

> 🔴 **本文件已被取代，且它的数字连自己的生成源都对不上了。不要引用本文件的任何数字。**
>
> | | 本文件（下文正文） | [FINAL_STRATIFICATION.md](./FINAL_STRATIFICATION.md) | 机器事实源 |
> | :-- | :-- | :-- | :-- |
> | 结论形态 | **区间** 47 – 136 | **点值** 129 | — |
> | 分层基线 | 154 条计入问题 | 同 | [stratification.json](./stratification.json) `totals.in_scope = 154` |
> | 词法区间 | 47 – 136 | 引作 66 – 144 | [stratification.json](./stratification.json) `admissible_floor = 66` / `admissible_upper = 144` |
> | 层构成 | 良构 45 / NL 矛盾 2 / NL 点名 89 / 仅参考 6 / 未归层 12，**无 `over_specification` 层** | 七层，含 `over_specification` | [stratification.json](./stratification.json) `by_stratum`：良构 33 / NL 点名 78 / **over_specification 31** / NL 矛盾 2 / 仅参考 4 / 未归层 6 |
> | 可入 | 上界 136 | 129 | [final_stratification.json](./final_stratification.json) `summary.admissible = **126**` |
>
> **三点必须一起看：**
>
> 1. **本文件被 [FINAL_STRATIFICATION.md](./FINAL_STRATIFICATION.md) 取代**——后者把本文件末尾「仍需人工的两步」   （复核 `nl_named`、归层 `unclassified`）实际做完了，因此从区间收敛到点值。取代关系是**完成**，不是**推翻**。
> 2. **本文件的正文数字连 [stratification.json](./stratification.json) 都对不上**：该 JSON 由    [../stratify_candidates.py](../scripts/stratify_candidates.py) 重新生成过，`over_specification` 层（31 条）   在本文件正文里**根本不存在**，下界也因此从 47 变成 66。所以本文件不只是「旧版本」，是**与自己的生成源脱钩的旧版本**——    重跑一次脚本就会得到另一份内容。
> 3. **`FINAL_STRATIFICATION.md` 的 129 也已经不是当前值**：`final_stratification.json` 现记 `admissible = 126`，   与台账 [expected_issue_set.json](./expected_issue_set.json) 的 126 条一致。要引数字请**直接读 JSON**，   两份 `.md` 都只是某一时刻的散文快照。
>
> 本文件**保留不删**：它记录了「区间 → 点值」这一步是怎么走的，以及为什么 `nl_named` 只能当上界。但凡涉及具体数字，一律以上表右两列为准。

Issue [#171](https://github.com/HansBug/research_ideas/issues/171) 裁决点 1 问的是「154 条候选如何入账」。本文件把它从一个立场表态变成一个**可复算的数字**：分层由 [../stratify_candidates.py](../scripts/stratify_candidates.py) 产出，判据、触发词与逐条归属全部落盘在 [stratification.json](./stratification.json)，任何一行都可以被推翻。

## 为什么不能整体入账

原论文的需求模板要求 "Requirements must avoid explicitly stating the number of elements or inter-element [relations]"，所以 NL 是**构造性欠定**的：与 NL 一致的模型是一个**集合**，而参考模型只是其中一个任选成员。按该成员逐点扣分，测的是「猜中作者私有模型」而不是「建模需求」。这一点在 6 个 NL 组得到实证——参考模型自身与 NL 冲突（Issue #171 §4）。

## 四层

| 层 | 条数 | 可入 E1 | 判据 |
| --- | ---: | :-: | --- |
| `wellformedness` | 45 | ✓ | **无需 oracle**，仅凭模型自身即可判定：无触发的 completion 边挤压已声明分支、带触发的初始边、复合态无默认子态、死端 / 吸收态 / 不可达 |
| `nl_contradiction` | 2 | ✓ | 与 NL 的**显式义务**矛盾（方向写反、违反某句的明确要求） |
| `reference_only` | 6 | ✗ | 只存在于参考、NL 未点名。作为差异是真的，但**不可归因于生成模型** |
| `nl_named` | 89 | ✓ | NL **点名**的元素缺失或错位 |
| `unclassified` | 12 | ? | 词法判据未命中，需人工归层 |

## 结论是区间，不是点值

**可入 E1 的区间：47 – 136。**

- **下界 47** = `wellformedness` 45 + `nl_contradiction` 2。前者无需 oracle、后者引了 NL 的显式冲突，是最难被反驳的两层。（巧合：这个数恰好等于台帐现有的 47 条 E1。）
- **上界 136** = 再加 `nl_named` 89 条。**该层是上界**——词法判据只要理由里提到 NL 就命中，而「提到 NL」不等于「NL 点名了缺失的那个元素」：审阅者常先引 NL 某句、再说参考在它之外多加了东西。要收敛到点值必须人工复核这 89 条。
- 明确不可入 6 条，待人工归层 12 条。

**分层是提案不是判定。** 每一行都带触发它的词，见 [stratification.json](./stratification.json) 的 `rows[].trigger`。

## 对裁决点 2（是否补录台帐）的直接输入

可入 E1 的 136 条中，**36 条落在台帐无 E1 的 case 上**（分布在 22 个 case）——这是「补录」的**实际增量上界**。其中 129 条带 `assertable` 且标了 `predicate_exists`（该标注本身有 19 条已知问题，见 `_summary.json` 的 `assertable_warnings`，引用时应折减）。

## 按 NL 组

| NL 组 | 可入 E1 | 良构性 | NL 矛盾 | NL 点名 | 仅参考 | 未归层 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NL01 | **17** | 2 | 0 | 15 | 0 | 2 |
| NL02 | **4** | 4 | 0 | 0 | 0 | 1 |
| NL03 | **18** | 6 | 0 | 12 | 1 | 3 |
| NL04 | **25** | 9 | 0 | 16 | 0 | 3 |
| NL05 | **20** | 2 | 0 | 18 | 0 | 0 |
| NL06 | **15** | 5 | 0 | 10 | 0 | 0 |
| NL07 | **9** | 7 | 1 | 1 | 0 | 0 |
| NL08 | **13** | 5 | 0 | 8 | 0 | 4 |
| NL09 | **5** | 3 | 0 | 2 | 0 | 0 |
| NL10 | **14** | 2 | 1 | 11 | 0 | 0 |

⚠️ 按 Issue #171 §0.2，**按 NL 组的绝对数值受审阅单元与拆分粒度影响**，此表仅作描述性参照，不作难度或领域归因。

## 仍需人工的两步

1. **复核 `nl_named` 的 89 条**，把区间从 47–136 收敛到点值。判据是「NL 是否点名了缺失的那个元素」，而不是「理由里是否提到 NL」。
2. **归层 `unclassified` 的 12 条**。

这两步做完，才能过 Issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的六道门槛。本文件只负责把候选池切成有判据的层，不替代那六道门槛。
