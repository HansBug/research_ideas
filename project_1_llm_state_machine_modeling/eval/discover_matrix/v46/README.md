# v46 全量矩阵：核心结论与统计

**这是 v46 的唯一入口。** 所有 v46 材料集中在本目录，本文件给核心结论与统计，细节引向各 sub md。

- 网格：**54 pair × 2 模型（claude / gpt）× 3 轮 = 324 格**（`00x8` 永久排除，见
  [NL_SCOPE_RULE.md](../NL_SCOPE_RULE.md)）
- 判定分母：**98 条台账记录 × 2 臂 × 3 轮 = 588 位**

---

## 一、覆盖侧（expected issue）

| 口径 | v37 | **v46** | 差 |
| :-- | --: | --: | --: |
| `hit@1` | 274/588 = 46.6% | **364/588 = 61.9%** | **+15.3pp** |
| `hit@3` | 106/196 = 54.1% | **141/196 = 71.9%** | **+17.8pp** |
| `hit@all` | 77/196 = 39.3% | **98/196 = 50.0%** | **+10.7pp** |
| claude `hit@1` | 132/294 = 44.9% | 188/294 = 63.9% | +19.0pp |
| gpt `hit@1` | 142/294 = 48.3% | 176/294 = 59.9% | +11.6pp |

**第二套口径**（扣除 [CONDITIONAL_ACTIVATION_RULE.md](../CONDITIONAL_ACTIVATION_RULE.md) §二
按 provenance 排除的 `EIS-0047-03`）：`hit@1` 361/582 = 62.0%｜`hit@3` 140/194 = 72.2%｜
`hit@all` 97/194 = 50.0%。

**成本**：output token 9.91M → 17.18M（1.73×），节点耗时 50.8 → 88.0 机时。
每百万 output token 命中位数 27.6 → 21.2（−23%）——提升有相当部分是多花算力换来的。

详见 [result.md](./result.md)（逐项结果）与 [audit.md](./audit.md)（审计与损失阶段）。

⚠️ **`hit@k` 的界**：本代次做过一次单向上修（找回匹配器漏配的 4 位）；反方向的
「台账记录本身是否编码了编译产物」尚未按同一判据回读作者源。
**两侧都做完之前，`hit@k` 既不是上界也不是下界。** 见
[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md) §4.7。

---

## 二、多报侧（unexpected issue）

未被任何台账记录认领的产出，归并为同质簇后**逐条人工裁定**。
原 293 条中 13 条经复核确认**内容已被现有台账记录承载**，按定义不属意外发现，
已移出至 [unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)。
**本侧分母 280 条目。**

### ⛔ 两套分母必须同时读

| 大类 | 条目 | 占比 | **去重** | **占比** | 比值 | 子类 |
| :-- | --: | --: | --: | --: | --: | --: |
| ⚙️ 表示债务 | 129 | **46.1%** | 27 | **22.7%** | 4.78 | 5 |
| 📄 无 NL 依据 | 115 | **41.1%** | 64 | **53.8%** | 1.80 | 10 |
| ❌ 假阳性 | 22 | 7.9% | 19 | 16.0% | 1.16 | 4 |
| 🚫 越界 | 10 | 3.6% | 5 | 4.2% | 2.00 | 3 |
| 🔧 谓词产物 | 3 | 1.1% | 3 | 2.5% | 1.00 | 2 |
| ✅ **真漏记** | **1** | **0.4%** | **1** | **0.8%** | 1.00 | 1 |
| **合计** | **280** | 100% | **119** | 100% | **2.35** | 25 |

⚠️ **两套分母给出相反的主要矛盾**：按条目读是「编译债务最大」，按去重读是「断言侧过度规定最大」。
原因是表示债务的条目/去重比 4.78 远高于无 NL 依据的 1.80——同一处损失被反复重述的程度高得多。
**只报一套会得出错误的整改优先级。**

去重单元 = `(pair, 根因)`；同 pair 同一处失误合并计 1，不同 pair 不合并。
每组的成员与**自然语言合并理由**见
[unexpected_verdicts/merge_groups.tsv](./unexpected_verdicts/merge_groups.tsv)（119 组，
`merge_key` 可与 [cluster_index.tsv](./unexpected_verdicts/cluster_index.tsv) 直接 join）。

### 三条可直接引用的结论

1. **多报的最大成分不是模型的问题。** 129 条目（27 处不同内容）是 PlantUML → FCSTM 编译的
   信息损失——作者在源制品上已逐字表达，是 IR 装不下。见 [REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md)。
2. **净增量是 1 条。** 全部 280 条目中只有 `0014-4` 通过了「事实为真 + 作者源确实没写 +
   NL 有逐字依据 + 台账未记」四条判据。**论文里能说的是 1，不是 280。**
3. **多报以单次采样噪声为主**：179/280（64%）只出现在 6 格中的 1 格。

成分与子类见 [composition.md](./composition.md)；裁定与交叉表见
[unexpected_adjudication.md](./unexpected_adjudication.md)；逐簇判据见
[unexpected_evidence.md](./unexpected_evidence.md)。

---

## 三、本目录文件

| 文件 | 内容 |
| :-- | :-- |
| [result.md](./result.md) | 逐项结果、成本、`hit@k` 变更记录 |
| [audit.md](./audit.md) | 审计：损失阶段、降级、遥测、多报侧判定 |
| [preregistered.md](./preregistered.md) | 本代次的事前登记（判据与达标档位） |
| [composition.md](./composition.md) | **成分分析**：六大类的子类体系与双分母 |
| [unexpected_adjudication.md](./unexpected_adjudication.md) | 多报侧裁定结论与三张交叉表 |
| [unexpected_merged.md](./unexpected_merged.md) | 按根因归并的问题清单 |
| [unexpected_evidence.md](./unexpected_evidence.md) | 280 簇逐条判据 |
| [verdicts/](./verdicts/) | `v46_tiers.json`（命中位真源）、`v46_human.json`、`v46_flips.json` |
| [unexpected_verdicts/](./unexpected_verdicts/) | 多报侧真源 `G1`–`G8.jsonl` 与全部派生 tsv |
| [telemetry/](./telemetry/) | 逐格 token 与耗时 |
| [verdicts/predicate_recheck.json](./verdicts/predicate_recheck.json) | 谓词语义复核：在冻结制品上重算受影响断言的对照 |

**裁定口径**（跨代次通用，故留在上级目录）：
[UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)（六类定义与判定流程）、
[HIT_CRITERION.md](../HIT_CRITERION.md)（什么算命中）、
[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md)（表示债务）。

**重建**：改多报侧裁定只能改 `unexpected_verdicts/G*.jsonl`，然后跑
`python3 ../rebuild_unexpected.py`——它会一并重建全部派生物，并在字段缺失、
标签作废、`merge_key` 跨界时拒绝执行。
