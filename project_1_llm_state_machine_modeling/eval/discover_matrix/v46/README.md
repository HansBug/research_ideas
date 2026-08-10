# v46 全量矩阵：核心结论与统计

**这是 v46 的唯一入口。** 所有 v46 材料集中在本目录，本文件给核心结论与统计，细节引向各 sub md。

- 网格：**54 pair × 2 模型（claude / gpt）× 3 轮 = 324 格**（`00x8` 永久排除，见
  [NL_SCOPE_RULE.md](../NL_SCOPE_RULE.md)）
- 判定分母：**98 条台账记录 × 2 臂 × 3 轮 = 588 位**

---

## 一、覆盖侧（expected issue）

| 口径 | v37 | **v46** | 差 |
| :-- | --: | --: | --: |
| `hit@1` | 274/588 = 46.6% | **360/588 = 61.2%** | **+14.6pp** |
| `hit@3` | 106/196 = 54.1% | **140/196 = 71.4%** | **+17.3pp** |
| `hit@all` | 77/196 = 39.3% | **97/196 = 49.5%** | **+10.2pp** |
| claude `hit@1` | 132/294 = 44.9% | 185/294 = 62.9% | +18.0pp |
| gpt `hit@1` | 142/294 = 48.3% | 175/294 = 59.5% | +11.2pp |

⚠️ **`hit@k` 只能作为上界读。** 命中侧尚未做与多报侧对称的表示债务审计
（[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md) §4.7）。已量化的规模：**人工表覆盖的
351 个命中位中，51 位（14.5%）在判据里引用「变量未声明」，其中 10 位（2.8%）不依赖其它事实**。
PlantUML 无变量声明语法、作者变量全语料 0/60，故「变量缺失」本身不能区分缺陷模型与忠实模型。
逐位清单见 [verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)。

**下界**：扣掉那 10 位，`hit@1` 为 350/588 = **59.5%**。真值落在 **[59.5%, 61.2%]** 之间。

📌 **351 与 360 的换算**：人工表覆盖 594 位中的 575 位，含 351 个命中判定；其中 6 位属被剔出
分母的 `EIS-0043-02`，故分母内 345；另有 15 个命中位无人工条目，`345 + 15 = 360`。上界性的
量化以 351 为分母，因为只有人工表带逐位 `argument`。

**成本**：output token 9.91M → 17.18M（1.73×），节点耗时 50.8 → 88.0 机时。
每百万 output token 命中位数 27.6 → **21.0（−24%）**——提升有相当部分是多花算力换来的。

详见 [result.md](./result.md)（逐项结果）与 [audit.md](./audit.md)（审计与损失阶段）。

---

## 二、多报侧（unexpected issue）

未被任何台账记录认领的产出，归并为同质簇后**逐条人工裁定**。
最初 293 簇中，13 条经复核确认**内容已被现有台账记录承载**，按定义不属意外发现，移出至
[unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)；
另有 2 条的断言在冻结制品上求值为 **True**（模型满足该义务），属**真阴性**——正确地不产出任何
issue，两侧都不存在，记于
[unexpected_verdicts/not_produced.jsonl](./unexpected_verdicts/not_produced.jsonl)。
**本侧分母 278 条目 / 117 去重 / 42 pair。**

### ⛔ 两套分母必须同时读

| 大类 | 条目 | 占比 | **去重** | **占比** | 比值 | 子类 |
| :-- | --: | --: | --: | --: | --: | --: |
| ⚙️ 表示债务 | 129 | 46.4% | 27 | 23.1% | 4.78 | 5 |
| 📄 无 NL 依据 | 115 | 41.4% | 64 | 54.7% | 1.80 | 10 |
| ❌ 假阳性 | 23 | 8.3% | 20 | 17.1% | 1.15 | 4 |
| 🚫 越界 | 10 | 3.6% | 5 | 4.3% | 2.00 | 3 |
| ✅ **真漏记** | 1 | 0.4% | 1 | 0.9% | 1.00 | 1 |
| **合计** | **278** | 100% | **117** | 100% | **2.38** | 23 |

⚠️ **两套分母给出相反的主要矛盾**：按条目读是「编译债务最大」，按去重读是「断言侧过度规定最大」。
原因是表示债务的条目/去重比 4.78 远高于无 NL 依据的 1.80——同一处损失被反复重述的程度高得多。
**只报一套会得出错误的整改优先级。**

⛔ **上表是本目录**唯一**允许的多报侧摘要。** 其余全部交叉表（分母闭合、子类双分母、
谓词族 × 裁定、稳定性分布、合并规模）都在唯一产地
[unexpected_tables.md](./unexpected_tables.md)，由 `unexpected_verdicts/G*.jsonl` 机器生成。
**不要在别处另存副本。**

去重单元 = `(pair, 根因)`；同 pair 同一处失误合并计 1，不同 pair 不合并。
**117 组 = 42 个多成员组 + 75 个单成员组**，每组的成员与**自然语言合并理由**见
[unexpected_verdicts/merge_groups.tsv](./unexpected_verdicts/merge_groups.tsv)（`merge_key`
可与 [unexpected_verdicts/cluster_index.tsv](./unexpected_verdicts/cluster_index.tsv) 直接 join）。

### 三条可直接引用的结论

1. **多报的最大成分不是模型的问题。** 129 条目（27 处不同内容）是 PlantUML → FCSTM 编译的
   信息损失——作者在源制品上已逐字表达，是 IR 装不下。见 [REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md)。
2. **净增量是 1 条。** 全部 278 条目中只有 `0014-4` 通过了「事实为真 + 作者源确实没写 +
   NL 有逐字依据 + 台账未记」四条判据。**论文里能说的是 1，不是 278。**
3. **多报以单次采样噪声为主**：171/278（62%）只出现在 6 格中的 1 格。

成分与子类体系见 [composition.md](./composition.md)；裁定判据见
[unexpected_adjudication.md](./unexpected_adjudication.md) 与
[unexpected_evidence.md](./unexpected_evidence.md)。

---

## 三、本目录文件

| 文件 | 内容 |
| :-- | :-- |
| [result.md](./result.md) | 逐项结果、成本、判定口径 |
| [audit.md](./audit.md) | 审计：损失阶段、降级、遥测、多报侧判定 |
| [preregistered.md](./preregistered.md) | 本代次的事前登记（判据与达标档位） |
| [composition.md](./composition.md) | **成分分析**：五大类的子类体系与划分维度 |
| [unexpected_tables.md](./unexpected_tables.md) | **多报侧全部交叉表的唯一产地**（机器生成，勿手改） |
| [unexpected_adjudication.md](./unexpected_adjudication.md) | 多报侧裁定结论与判据 |
| [unexpected_merged.md](./unexpected_merged.md) | 按根因归并的问题清单 |
| [unexpected_evidence.md](./unexpected_evidence.md) | 278 簇逐条判据 |
| [telemetry/](./telemetry/) | 逐格 token 与耗时 |

**判定真源** [verdicts/](./verdicts/)：

| 文件 | 内容 |
| :-- | :-- |
| [verdicts/v46_tiers.json](./verdicts/v46_tiers.json) | 台账记录 × 2 臂 × 3 轮的 1/0/null 判定表（命中位真源） |
| [verdicts/v46_human.json](./verdicts/v46_human.json) | 逐位人工判定，每条带 `argument`，命中位另带 `equivalence_form` |
| [verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json) | 命中位中依赖「变量未声明」的逐位清单（`hit@k` 上界性的量化依据） |

**多报侧真源** [unexpected_verdicts/](./unexpected_verdicts/)：

| 文件 | 内容 |
| :-- | :-- |
| `G1.jsonl` – `G8.jsonl` | **手工裁定真源**，278 簇按判定组分文件，每簇带 `verdict` / `subclass` / `merge_key` / `merge_reason` / `fact` / `nl`，另有可选的 `root` / `note` |
| [ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl) | 13 条内容已被台账承载、不进桶的簇 |
| [not_produced.jsonl](./unexpected_verdicts/not_produced.jsonl) | 2 条断言求值为 True 的真阴性 |
| [cluster_index.tsv](./unexpected_verdicts/cluster_index.tsv) | 派生：逐簇索引（`pair` / `verdict` / `subclass` / `merge_key` / `cells_of_6` / `predicate_families`） |
| [merge_groups.tsv](./unexpected_verdicts/merge_groups.tsv) | 派生：117 个去重组及其自然语言合并理由 |
| [subclass_table.tsv](./unexpected_verdicts/subclass_table.tsv) | 派生：子类双分母统计 |
| [by_pair.tsv](./unexpected_verdicts/by_pair.tsv) | 派生：pair × 大类分布 |
| [final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv) | 派生：真漏记的根因归并 |

**裁定口径**（跨代次通用，故留在上级目录）：
[UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)（五类定义与判定流程）、
[HIT_CRITERION.md](../HIT_CRITERION.md)（什么算命中）、
[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md)（表示债务）、
[METHOD_PROVENANCE_POLICY.md](../METHOD_PROVENANCE_POLICY.md)（方法出处与分母口径：台账记录
同等参与度量，不因参与过规则编写而剔出分母）。

**重建**：改多报侧裁定只能改 `unexpected_verdicts/G*.jsonl`，然后跑
`python3 ../rebuild_unexpected.py`——它会一并重建
[unexpected_tables.md](./unexpected_tables.md) 与全部派生 tsv，并在字段缺失、
裁定不在五类内、`merge_key` 跨界时拒绝执行。
