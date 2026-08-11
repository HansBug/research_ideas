# 60 pair 人工审阅数据

作者生成 STM_0 相对论文参考 STM_0 的逐条差异判定，**60/60 全覆盖**。判定原则见 [manual_review_spec.md](../docs/protocol/manual_review_spec.md)，命中判据见 [hit_criterion.md](../docs/protocol/hit_criterion.md)，分母的已知缺口见 [ground_truth_limitations.md](../docs/protocol/ground_truth_limitations.md)。

完整报告与讨论：Issue [#171](https://github.com/HansBug/research_ideas/issues/171)。

## 为什么是人工判定

机械元素 diff 不可用：参考独有而生成缺失的状态有 229 个，规范化大小写、分隔符与常见修饰词后降到 191，**仍余大量假缺失**——绝大多数是同一状态的不同命名（`human_mode` / `HumanDrivingMode`、`avoid_frontend_collision` / `F`）。原论文本身也把它的 stage (3)(4) 标为 manual，正是因为元素对应关系无法机械判定。

## 主档与派生物

这里只存**主档**。其余一切都是主档的纯函数，可随时重算并与已发布版本 diff：

| 文件 | 性质 | 说明 |
| --- | --- | --- |
| `<case>-review.json` | **主档** | 单 case 完整判定。丢失不可恢复 |
| `_summary.json` | 派生 | 由 [../aggregate_manual_review.py](../aggregate_manual_review.py) 汇总 |
| `index.tsv` · `figure_data.tsv` | 派生 | 机读索引与图数据 |
| `corpus_structure.json` | 主档 | 60 个 FCSTM STM_0 的结构统计，由 [../corpus_census.py](../corpus_census.py) 经 pyfcstm 读出 |
| `<case>-readable.md` | 派生 | **不入库**，由 `aggregate_manual_review.py` 的 `readable()` 从主档生成 |
| issue 的全部表格与图 | 派生 | 由 [../render_refcmp_issue.py](../render_refcmp_issue.py) 生成，每个数字读自本目录 |

重算：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/aggregate_manual_review.py \
    <单 case 判定输入目录> /tmp/refcmp/agg
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/render_refcmp_issue.py \
    /tmp/refcmp/agg/audit <审计 gist id> <可读 gist id>
```

## 候选分层：三份同名文件，只有一份是当前的

「154 条计入问题里哪些能成为 expected issue」这个问题，本目录下有三代产物。**按下表取用，不要按文件名猜。**

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| [expected_issue_set.json](./expected_issue_set.json) | 🟢 **台账权威源** | **126 条**。命中率的分母只能从这里来 |
| [final_stratification.json](./final_stratification.json) | 🟢 当前 | 逐行分层点值，`summary.admissible = 126`，与上一行一致 |
| [FINAL_STRATIFICATION.md](./FINAL_STRATIFICATION.md) | 🟡 方法说明可用、数字已漂 | 讲清楚四批 NL 复核怎么做的；但正文写的 **129** 早于 JSON 的 126 |
| [stratification.json](./stratification.json) | 🟡 仅历史 | 词法分层基线，区间 66 – 144 |
| [STRATIFICATION.md](./STRATIFICATION.md) | 🔴 **已被取代** | 区间 47 – 136，且与 `stratification.json` 也已脱钩（缺 `over_specification` 层）。**不要引用其中任何数字**，见该文件顶部说明 |

一句话：**数字读 JSON，读法读 `.md`。** 两份 `.md` 都是某一时刻的散文快照，重跑
[../stratify_candidates.py](../stratify_candidates.py) 或
[../merge_manual_stratification.py](../merge_manual_stratification.py) 不会更新它们。

## 组间信度（双盲复审）

`reliability/` 下是 **12 例分层样本的双盲复审**，用于给出全量审阅结构上无法计算的组间信度（全量 60 case 零重叠，且 [../aggregate_manual_review.py](../aggregate_manual_review.py) 把重复审阅当作错误报出）。样本覆盖全部 10 个 NL 组、6 个 LLM、原审 `problem` 数 0–6 全区间；两个审阅者互不可见，也不可见原审结果与 `_summary.json`。

| 指标 | 结果 |
| --- | --- |
| `problem` 合计 | 原审 **28** · 盲审A **30** · 盲审B **32**，极差 4 条（**14%**） |
| case 级「是否存在问题」Cohen $\kappa$ | 原审–盲A **0.750** · 原审–盲B **0.750** · 盲A–盲B **1.000** |
| 逐 case `problem` 数秩相关 | **+0.883** / **+0.665** / **+0.741** |
| 三方一致判 0 problem | `0021` `0052` |
| 唯一分歧 | `0017`（原审 0，盲A 2，盲B 3——三处带触发的初始边） |

$\kappa = 0.750$ 落在 substantial agreement 区间。**但三方都是 LLM agent，高 $\kappa$ 可能部分反映同类模型的同类偏差，不等价于人类评审间一致性；它只证明判定可复现，不证明判定正确。**

这批盲审还检验了「审阅单元与 NL 组混淆」的影响：两个盲审各自横跨全部 10 个 NL 组、**不含混淆**，而被指「最严厉」的 R2（NL03/04）与「最宽松」的 R5（NL09/10）之比在三方都复现（原审 6.00 / 盲A 5.25 / 盲B 2.10）。所以**组间相对高低可复现，绝对数值受拆分粒度强烈影响**。

## 判定档位

| 档位 | 含义 | 条数 | 计入问题 |
| --- | --- | ---: | :-: |
| `correct` | 语义等价，写法不同 | 77 | ✗ |
| `similar` | 有差异但说得通、不违反 NL | 127 | ✗ |
| `problem` | 违反 NL，或丢失参考所承载的语义 | 132 | ✓ |
| `extra` | 生成方多出、参考与 NL 都没有 | 31 | ✓ |
| `uncertain` | 证据不足；卡点已写明 | 51 | ✗ |

`out_of_scope` 标记 `concurrency` / `timing`。这两类在本研究问题定义外（`T0 + FSM/HSM/EFSM`，核心是层次 + 形式化 + 语义性），**既不计入问题也不静默丢弃**：29 条（并发 24 / 时间 5）逐条保留在主档里。

计入问题 = 132 + 31 − 9 = **154**（被扣除的 9 条是 verdict 为 `problem`/`extra` 且带 `out_of_scope` 的那些；另 20 条 `out_of_scope` 落在 `similar`/`uncertain` 上，本就未计入）。

## 校验

`aggregate_manual_review.py` 在统计前 gate 四类会让结论失真的问题，并以非零退出码阻止发布：

1. 未审阅的 case——其缺席会被读成"该 case 无问题"
2. 未知档位
3. reviewer 自报计数与逐条统计不一致
4. 判定缺理由

本目录数据通过全部校验（退出码 0）。

## oracle 局限

参考模型是论文作者**人工重建**的产物：论文 §7 自认 "we manually created them, which is subjective"，§4.2(4) 明写 "we **assume** the reference model is semantically correct"——正确性未经独立验证。本审阅在多个 NL 组发现参考模型自身与 NL 冲突（Issue #171 §5）。

**因此这里的判定是「相对该参考模型」的，不等于绝对缺陷集**；作为 expected issue 候选池时必须再过 Issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的门槛。
