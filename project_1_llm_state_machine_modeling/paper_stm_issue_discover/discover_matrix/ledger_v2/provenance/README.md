> ⛔⛔ **本目录不是台账。** 当前唯一有效的台账是上一级的 [../ledger.json](../ledger.json)（**145** 条）。⭐ 本目录是**那份台账的证据链** —— 回答「某一条缺陷当初是怎么被判出来的」，⛔ 不回答「台账里有哪些条目」。⚠️ 下面提到的 `expected_issue_set.json`（126 条）是**第一版台账**，⛔ **已被取代，不得再作为任何分母或权威源使用**。

# provenance — 第二版台账的证据链

⚠️ **本目录 2026-08-17 之前叫 `manual_review/`，位置在 `archive/r10_ledger_v1_and_v46/` 下。** 它随台账一起搬回活跃区，是因为 [../ledger.json](../ledger.json) 每一条的 `worksheet` 字段都指向这里的工作单 —— 证据链留在冷归档里会让「凭什么这么判」断线。⭐ 搬迁保持了目录深度（两处都是 `paper_stm_issue_discover` 下第 3 层），所以内部全部相对链接原样有效。

## 〇、这里的东西各自是什么

| 对象 | 在证据链里的角色 | 现在还作数吗 |
| :-- | :-- | :-- |
| `<pair>-review.json`（60 份） | ⭐ **主档**：作者生成 STM_0 相对论文参考 STM_0 的逐条差异判定，60/60 全覆盖 | ⭐ 作数，是 `EIS-` 族的最上游 |
| [expected_issue_set.json](./expected_issue_set.json) | **第一版台账**，126 条。其中 27 条落在 `00x8` 六个先验越界 pair 上，余 **99** 条进入重标工作单，最终 **90** 条成为第二版台账的 `EIS-` 族 | ⛔ **作为台账已失效**；⭐ 作为证据链的中间产物仍需保留 |
| [relabel/](./relabel/) | ⭐ **重标工作区**：54 份工作单（含全部人工裁决与逐条 meta review）、三方 D 档判读包、去重台账、生成 / 回收 / 校验工具与测试 | ⭐ 作数，台账的 `D` 档与裁决理由全部出自这里 |
| `reliability/` | 12 例双盲复审，给组间信度 | ⭐ 作数（限于方法学结论） |
| `stratification.json` · 两份 `*STRATIFICATION.md` | 第一版台账成型前的候选分层三代产物 | ⛔ 仅历史，见 [§三](#三候选分层三份同名文件只有一份是当前的) |

判定原则见 [manual_review_spec.md](../../../discover_matrix/docs/protocol/manual_review_spec.md)，命中判据见 [hit_criterion.md](../../../discover_matrix/docs/protocol/hit_criterion.md)，分母的已知缺口见 [ground_truth_limitations.md](../../../discover_matrix/docs/protocol/ground_truth_limitations.md)。

完整报告与讨论：Issue [#171](https://github.com/HansBug/research_ideas/issues/171)。

## 一、为什么是人工判定

机械元素 diff 不可用：参考独有而生成缺失的状态有 229 个，规范化大小写、分隔符与常见修饰词后降到 191，**仍余大量假缺失**——绝大多数是同一状态的不同命名（`human_mode` / `HumanDrivingMode`、`avoid_frontend_collision` / `F`）。原论文本身也把它的 stage (3)(4) 标为 manual，正是因为元素对应关系无法机械判定。

## 二、主档与派生物

这里只存**主档**。其余一切都是主档的纯函数，可随时重算并与已发布版本 diff：

| 文件 | 性质 | 说明 |
| --- | --- | --- |
| `<case>-review.json` | **主档** | 单 case 完整判定。丢失不可恢复 |
| `_summary.json` | 派生 | 由 [../aggregate_manual_review.py](../../../archive/r10_ledger_v1_and_v46/scripts/aggregate_manual_review.py) 汇总 |
| `index.tsv` · `figure_data.tsv` | 派生 | 机读索引与图数据 |
| `corpus_structure.json` | 主档 | 60 个 FCSTM STM_0 的结构统计，由 [../corpus_census.py](../../../archive/r10_ledger_v1_and_v46/scripts/corpus_census.py) 经 pyfcstm 读出 |
| `<case>-readable.md` | 派生 | **不入库**，由 `aggregate_manual_review.py` 的 `readable()` 从主档生成 |
| issue 的全部表格与图 | 派生 | 由 [../render_refcmp_issue.py](../../../archive/r10_ledger_v1_and_v46/scripts/render_refcmp_issue.py) 生成，每个数字读自本目录 |

重算 —— ⚠️ **这两个脚本已随 v46 时代的分析脚本转入冷归档，且它们的目录深度变了，直接跑会静默解析到错误目录**（CLAUDE.md §9.5-3）。复活步骤见 [归档复活导引 §4.2](../../../archive/r10_ledger_v1_and_v46/README.md#42-v46-时代的分析脚本)：

```bash
P=project_1_llm_state_machine_modeling/paper_stm_issue_discover/archive/r10_ledger_v1_and_v46/scripts
venv/bin/python $P/aggregate_manual_review.py  <单 case 判定输入目录> /tmp/refcmp/agg
venv/bin/python $P/render_refcmp_issue.py      /tmp/refcmp/agg/audit <审计 gist id> <可读 gist id>
```

## 三、候选分层：三份同名文件，只有一份是当前的

⚠️ **本节全部内容属于第一版台账的成型过程**，⛔ 其中任何数字都不是当前口径 —— 当前台账是 [../ledger.json](../ledger.json) 的 145 条。保留本节是因为它解释了 `EIS-` 族的候选是怎么被筛出来的。

「154 条计入问题里哪些能成为 expected issue」这个问题，本目录下有三代产物。**按下表取用，不要按文件名猜。**

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| [expected_issue_set.json](./expected_issue_set.json) | 🟡 **第一版台账，已被取代** | **126 条**。⛔ 不再是任何命中率的分母；⭐ 仅作为 `EIS-` 族的上游证据 |
| [final_stratification.json](./final_stratification.json) | 🟡 与上一行一致 | 逐行分层点值，`summary.admissible = 126` |
| [FINAL_STRATIFICATION.md](./FINAL_STRATIFICATION.md) | 🟡 方法说明可用、数字已漂 | 讲清楚四批 NL 复核怎么做的；但正文写的 **129** 早于 JSON 的 126 |
| [stratification.json](./stratification.json) | 🟡 仅历史 | 词法分层基线，区间 66 – 144 |
| [STRATIFICATION.md](./STRATIFICATION.md) | 🔴 **已被取代** | 区间 47 – 136，且与 `stratification.json` 也已脱钩（缺 `over_specification` 层）。**不要引用其中任何数字**，见该文件顶部说明 |

一句话：**数字读 JSON，读法读 `.md`。** 两份 `.md` 都是某一时刻的散文快照，重跑 [../stratify_candidates.py](../../../archive/r10_ledger_v1_and_v46/scripts/stratify_candidates.py) 或 [../merge_manual_stratification.py](../../../archive/r10_ledger_v1_and_v46/scripts/merge_manual_stratification.py) 不会更新它们。

## 四、⭐ 人工全量重标：[relabel/](./relabel/) —— ⭐ 第二版台账就是从这里出来的

⛔ **上表的 126 条全部由 LLM agent 生成，人类校验 0 条**，双盲复审只覆盖 12/60 且是二元 case 级。[relabel/](./relabel/) 是为**逐 pair 人工重标**准备的工作区：54 份自包含工作单（判读原料 + 逐条裁决区）加生成 / 回收 / 校验工具，入口见 [relabel/README.md](./relabel/README.md)，进度见 [relabel/PROGRESS.md](./relabel/PROGRESS.md)。⚠️ 原先还有「候选新增登记」与「逐 pair 深度检查清单」两节，⛔ 已**整节拆除**（用户裁定：只保留对现有台账 + 候选的裁决）。

⛔⛔ **条目数口径：工作单共 321 个裁决区**（台账 99 + 候选 222）。⚠️ 三方 D 档判读做过 **380** 条，⛔ **那个数没有去重** —— 其中 59 条最终判定为「与另一条是同一个问题」，只作补充证据印在宿主条目里、⛔ 不设裁决区。⚠️ 历史上还出现过 `269` / `220` / `319` / `323` / `324` / `429` 几个数，⛔ **一个都不是当前口径**。⭐ 完整账目、每个数的来历见 [relabel/DEDUP_ACCOUNTING.md](./relabel/DEDUP_ACCOUNTING.md) —— ⛔ 动任何与条目数有关的代码或统计前先读那一页。

⭐ **重标已完成，产物就是 [../ledger.json](../ledger.json)。** 321 个裁决区经三臂独立 D 档判读 + 人工逐条 meta review + 人工逐条裁决后，判为 `D2` / `D1` 的 **145** 条构成第二版台账；`D0` 与三个 `A0` 出口不入账。⛔ [expected_issue_set.json](./expected_issue_set.json) 自此**不再被任何评测读取**，它保持冻结只为留住 `EIS-` 族的上游形态。

## 五、组间信度（双盲复审）

`reliability/` 下是 **12 例分层样本的双盲复审**，用于给出全量审阅结构上无法计算的组间信度（全量 60 case 零重叠，且 [../aggregate_manual_review.py](../../../archive/r10_ledger_v1_and_v46/scripts/aggregate_manual_review.py) 把重复审阅当作错误报出）。样本覆盖全部 10 个 NL 组、6 个 LLM、原审 `problem` 数 0–6 全区间；两个审阅者互不可见，也不可见原审结果与 `_summary.json`。

| 指标 | 结果 |
| --- | --- |
| `problem` 合计 | 原审 **28** · 盲审A **30** · 盲审B **32**，极差 4 条（**14%**） |
| case 级「是否存在问题」Cohen $\kappa$ | 原审–盲A **0.750** · 原审–盲B **0.750** · 盲A–盲B **1.000** |
| 逐 case `problem` 数秩相关 | **+0.883** / **+0.665** / **+0.741** |
| 三方一致判 0 problem | `0021` `0052` |
| 唯一分歧 | `0017`（原审 0，盲A 2，盲B 3——三处带触发的初始边） |

$\kappa = 0.750$ 落在 substantial agreement 区间。**但三方都是 LLM agent，高 $\kappa$ 可能部分反映同类模型的同类偏差，不等价于人类评审间一致性；它只证明判定可复现，不证明判定正确。**

这批盲审还检验了「审阅单元与 NL 组混淆」的影响：两个盲审各自横跨全部 10 个 NL 组、**不含混淆**，而被指「最严厉」的 R2（NL03/04）与「最宽松」的 R5（NL09/10）之比在三方都复现（原审 6.00 / 盲A 5.25 / 盲B 2.10）。所以**组间相对高低可复现，绝对数值受拆分粒度强烈影响**。

## 六、判定档位

| 档位 | 含义 | 条数 | 计入问题 |
| --- | --- | ---: | :-: |
| `correct` | 语义等价，写法不同 | 77 | ✗ |
| `similar` | 有差异但说得通、不违反 NL | 127 | ✗ |
| `problem` | 违反 NL，或丢失参考所承载的语义 | 132 | ✓ |
| `extra` | 生成方多出、参考与 NL 都没有 | 31 | ✓ |
| `uncertain` | 证据不足；卡点已写明 | 51 | ✗ |

`out_of_scope` 标记 `concurrency` / `timing`。这两类在本研究问题定义外（`T0 + FSM/HSM/EFSM`，核心是层次 + 形式化 + 语义性），**既不计入问题也不静默丢弃**：29 条（并发 24 / 时间 5）逐条保留在主档里。

计入问题 = 132 + 31 − 9 = **154**（被扣除的 9 条是 verdict 为 `problem`/`extra` 且带 `out_of_scope` 的那些；另 20 条 `out_of_scope` 落在 `similar`/`uncertain` 上，本就未计入）。

## 七、校验

`aggregate_manual_review.py` 在统计前 gate 四类会让结论失真的问题，并以非零退出码阻止发布：

1. 未审阅的 case——其缺席会被读成"该 case 无问题"
2. 未知档位
3. reviewer 自报计数与逐条统计不一致
4. 判定缺理由

本目录数据通过全部校验（退出码 0）。

## 八、oracle 局限

参考模型是论文作者**人工重建**的产物：论文 §7 自认 "we manually created them, which is subjective"，§4.2(4) 明写 "we **assume** the reference model is semantically correct"——正确性未经独立验证。本审阅在多个 NL 组发现参考模型自身与 NL 冲突（Issue #171 §5）。

**因此这里的判定是「相对该参考模型」的，不等于绝对缺陷集**；作为 expected issue 候选池时必须再过 Issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的门槛。
