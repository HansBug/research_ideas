# v46 全量 324 格：运行结果审计

审计对象：`runs/paper1/matrix-v46-full`（本地，`runs/` 被 gitignore；证据以本目录下的
判定表、遥测表与本文件为准）。

## 0. 冻结与溯源

| 项 | 值 | 核验方式 |
| :-- | :-- | :-- |
| 运行代码 | `ca41369e46c09eafe6bfbfe64c3754b02c6d8fee` | `CODE_VERSION.txt`，`written_before_launch: yes`，`dirty_src: 0` |
| 复现 | `git checkout ca41369e` | `CODE_VERSION.txt` |
| 该 commit 是否在远端 | 是 | `git branch -r --contains ca41369e` |
| 启动时 `src` 脏改动 | **0 files** | `CODE_VERSION.txt` |
| `ca41369e` 之后 `src` 的变更 | `predicate_api.py` 的 `persists_until` / `stays_in` 有语义修订。**覆盖侧 588 位不受影响**（命中判定读的是产出文本与台账，不重新求值断言）；**多报侧分母受影响**，见下一行。**复现该 324 格运行须 `git checkout ca41369e`** | `git log ca41369e..HEAD -- .../feedback_loop/src/` |
| 多报侧分母的求值口径 | 桶内计入 288；`0044-2` 与 `0054-1` 本就不在桶内：`0044-2` 与 `0054-1` 的断言按**当前**谓词语义在冻结制品上求值为 **True**（模型满足该义务），属真阴性、两侧都不存在，记于 [not_produced.jsonl](./unexpected_verdicts/not_produced.jsonl)。**复现该判定须当前 HEAD，不是 `ca41369e`。** 这是一次运行后的口径变更，方向是缩小多报侧分母（对我们不利的方向） | `not_produced.jsonl` 的 `assertion` / `value_on_frozen_artifact` 字段逐条可复算 |
| 网格 | 54 pair × 2 模型 × 3 轮 = 324 | `GRID.txt`，含 `00x8`: 无 |
| 启动时刻 | `2026-08-09T20:09:52Z` | `WALLCLOCK.txt` |
| 完成时刻 / 墙钟 | `2026-08-10T03:15:41Z` / **7h05m49s** | 同上 |
## 1. 数据完整性（全部通过）

| 检查 | 结果 |
| :-- | :-- |
| 完成收据 | 324，正式格 324，`.try` 目录中 **0** |
| 期望格集 vs 实得 | 324 vs 324，缺 0、多 0 |
| `run_id` 唯一性 | 324 个，**重复 0**（重复即重复写入者） |
| `run_id` 时间戳早于 launcher 者（孤儿） | **0** |
| 耗尽格 | **0** |

## 2. 抽查判定（12 条，命中/未命中各 6，确定性抽样）

逐条回读台账 `statement` 与该格全部 issue 原文，核对判定理由：**12/12 站得住**。
抽样含 `EIS-0026-01` —— 台账自陈「`cardinality(scope=SearchingState,count=3)` 恰好为真
但理由完全错误」，判未命中避开了该假阳性陷阱。

## 3. 边界裁定：`EIS-0043-02` 剔出能力分母

`EIS-0043-02` 的台账字段：

```
boundary_ruling:   out_of_scope
boundary_effect:   从能力分母剔除。注意它是 6/6 命中，剔除使 hit@1 由 51.5% 降至 50.0%。
boundary_ruled_by: independent adjudication, 2026-08-07
boundary_rationale: 唯一容器为真正 PlantUML 正交区者；按正交语义读作者的源是合式的。
                   该记录的前提只在 R4.5 把两区摊平成顺序子态后才成立 —— 为表示层产物，非作者缺陷。
```

**该裁定的执行位置**：`metrics_at_k._out_of_scope_record_ids()` 同时读 `in_scope` 与
`boundary_ruling` —— `in_scope` 对 126 条全为 `True`，它记的不是这件事，所以边界裁定必须
另走 `boundary_ruling` 字段。由
[test_scope_vs_holdout_are_different.py](../test_scope_vs_holdout_are_different.py) 的
`test_a_boundary_ruling_in_the_ledger_is_actually_honoured` 钉住。

- **口径**：`full_tables.py` 表 2 说明里同时给出双分母 —— 99 记录（594 位）与剔除后的
  98 记录（588 位）。**本文件与 [result.md](./result.md) 一律采用 98 记录 / 588 位。**
- **影响**：该记录在 v37 与 v46 **都是 6/6**，故只同等抬高两侧绝对值，**差值几乎不变**。
- 全库扫描确认这是**唯一**一条「在分母内但 `boundary_effect` 要求剔除」的记录。

## 4. 最终结果（分母 98 条 × 2 臂 × 3 轮 = 588 位）

| 口径 | v37 | **v46** | 差 |
| :-- | --: | --: | --: |
| `hit@1` | 274/588 = 46.6% | **355/588 = 60.4%** | **+13.8pp** |
| `hit@3` | 106/196 = 54.1% | **139/196 = 70.9%** | **+16.8pp** |
| `hit@all` | 77/196 = 39.3% | **95/196 = 48.5%** | **+9.2pp** |
| claude `hit@1` | 132/294 = 44.9% | 184/294 = 62.6% | +17.7pp |
| gpt `hit@1` | 142/294 = 48.3% | 171/294 = 58.2% | +9.9pp |

⚠️ **上表的 `hit@k` 只能作为上界读。** 多报侧已做表示债务审计（§6），**命中侧的对称审计
尚未做**（[representation_debt.md](../docs/findings/representation_debt.md) §4.7）。已量化的规模：
**分母内带逐位判据的 340 个命中位中，51 位（15.0%）在判据里引用「变量未声明」，
其中 10 位（2.9%）不依赖其它事实**（另有 15 个无判据文字的命中位未被筛查，故 51 是下界）。PlantUML 无变量声明语法、作者变量全语料 0/60，故「变量缺失」本身不能区分
缺陷模型与忠实模型。逐位清单见
[verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)。

📌 **另一条不经 prompt 的通道**：谓词拒答文案会进入生成者的下一轮上下文。实测
`predicate_api.py:1524` 的 `UnsupportedEvidence` 原文——「variable 'uav_count' is not
observable in the simulation state. **If the NL requires a quantity this model has no variable
for, assert that variable's existence as a `precondition`**」——出现在 `run1/0006-claude` 的
`findings` 里，而 `EIS-0006-02` 是 6/6。它交出的不是元素名（那是生产者自己先绑的），是
**极性**与**「把它发布出去」的指示**。计入上界的理由与变量缺失同源，故上界应按两条通道
一起读，而不是只按 `variable_declared` 一条。

📌 **346 与 355 的换算**：人工表覆盖 594 位中的 574 位，含 346 个命中判定；其中 6 位属被剔出
分母的 `EIS-0043-02`，故分母内 340；另有 15 个命中位无人工条目，`340 + 15 = 355`。

判定来源：A 层自动 + 人工，见 [verdicts/v46_human.json](./verdicts/v46_human.json)（574 条
人工判定，每条带 `argument`；其中 346 条判为命中，且全部带 `equivalence_form`）。
📌 **判定覆盖的缺口**：588 位中 **20 位**在该文件里没有对应条目（15 位判为命中、5 位判为
未命中），涉及 `EIS-0002-01` / `EIS-0002-03` / `EIS-0009-02` / `EIS-0029-02` / `EIS-0029-04` /
`EIS-0037-01` / `EIS-0039-01` / `EIS-0057-01`；**这 20 位无逐格 `argument` 可复核**。

## 5. 成本（本次新增审计维度）

数据源为各格 `telemetry_summary`，导出工具 [run_telemetry.py](../run_telemetry.py)，
逐格明细 [telemetry/v46_cells.json](./telemetry/v46_cells.json)、
对照 [telemetry/v37_summary.json](../telemetry/v37_summary.json)。

| 项 | v37 | v46 | 比值 |
| :-- | --: | --: | --: |
| output token | 9,914,815 | **17,178,685** | **1.73×** |
| input token | 105,439,224 | 163,365,699 | 1.55× |
| LLM 调用 | 3,160 | 3,621 | 1.15× |
| 节点耗时合计 | 50.8 机时 | **88.0 机时** | 1.73× |
| 每格 output token（中位 / 最大） | 21,444 / 155,495 | 38,387 / 329,283 | 1.79× |
| 每格墙钟（中位 / 最大） | 381s / 3327s | 636s / 8109s | 1.67× |

**逐角色 output token（v46）**：`assertion_converter` 54.7%、`requirement_splitter` 34.4%、
`requirement_reviewer` 5.0%、`assertion_reviewer` 2.9%、`result_adjudicator` 2.9%。

**逐节点耗时（v46）**：`convert_assertions` 49.2%、`split_requirements` **38.9%**、
`review_requirements` 5.7%、`review_assertions` 3.4%、`adjudicate_results` 2.6%。
**前两者合计 88.1%**，且都随需求条数线性增长 —— 与 §7 第 1 条残留缺陷同源。

📌 **效率反而下降**：每百万 output token 的命中位数，v37 为 **27.6**、v46 为 **20.7**（−25%）。
命中率的提升有相当一部分是**多花算力换来的**，不是纯效率提升。只报命中率而不报成本会掩盖这一点。

## 6. 多报侧（未被台账认领的产出）

- 已发布 issue **1105 条**（v37 为 566，1.95×），而命中位只涨到 1.30×（274 → 355）。
- 命中位 355 由部分已发布 issue 支撑（一个命中位可由同格多条 issue 共同支撑），
  其余产出未被任何台账记录认领。
- 这批未认领产出**已归并为同质簇并逐条人工裁定**（八个并行判定组 + 一组回读原件复核）：
  最初 304 簇中 14 簇内容已被台账记录承载、2 簇的断言在冻结制品上求值为真（真阴性），
  均按定义移出，**本侧分母 288 条目 / 124 去重 / 43 pair**。

**结论**：「产出变多」既不是纯粹的发现能力增强，也不是纯粹的噪声增加——
**最大的一块（表示债务）根本不是模型的问题，是我们自己编译链的信息损失被当成了缺陷**；
而通过全部四条判据的**净增量为 2 条**（`0014-4` 与 `0010-2`），出现格数分别是 2/6 与 3/6，
无稳定复现。

📌 **五类分布、双分母、谓词族 × 裁定、稳定性与合并规模的全部交叉表，由
[rebuild_unexpected.py](../rebuild_unexpected.py) 从 `unexpected_verdicts/G*.jsonl`
机器生成于唯一产地 [unexpected_tables.md](./unexpected_tables.md)。本文件不留副本**——
副本与真源分岔过一次，代价是同一目录内两份文件对净增量给出互斥答案。

判据与定义另见 [unexpected_evidence.md](./unexpected_evidence.md)（288 簇逐条判据）、
[unexpected_merged.md](./unexpected_merged.md)（归并后的问题）、
[unexpected_taxonomy.md](../docs/protocol/unexpected_taxonomy.md)（裁定口径）、
[representation_debt.md](../docs/findings/representation_debt.md)（表示债务的定义与论文口径）。

⚠️ CLAUDE.md §3.5.2 要求的 `over@1` / `over@any` 口径：本轮以**稳定性维度**（簇在 6 格中
出现几次）实现，见 [unexpected_tables.md](./unexpected_tables.md) 表 4。
**174/288（60%）只出现在 1 个格里**，即多报以单次采样噪声为主。

## 7. 残留缺陷（v47 入口，按严重度）

1. **需求集规模失控** —— 中位 15 条，最大 **99**；按末次修订计，需求集超 60 的有 13 格，
   其中 **4 格降级（30.8%，全局 2.8%）**：`run1/0039-gpt`、`run2/0009-gpt`、`run3/0039-gpt`、
   `run3/0049-gpt` —— **全部是 gpt 臂**。（计数基准写明：取每格最后一次 `split_requirements`
   状态更新里的去重需求 id 数；换成「跨修订取最大」会多出 2 格，降级集不变。）
   耗时侧亦印证：`convert_assertions` + `split_requirements` 占 88% 且随条数线性增长。
   **应加需求集规模约束或合并策略，而不是继续修单个门。**
2. **schema 校验失败缺节点内原地重试** —— `responder._retryable_error` 对 `ValueError`
   返回 `False`，而 pydantic 的 `ValidationError` 是其子类；本代 7 次整格冷启动重跑里 **6 次**由此而来。
   ⛔ **第 7 次是另一回事，必须分开记**：`run2/0019-gpt` 抛的是
   `ValueError: no-progress gate rejected repeated AssertionScript semantics` ——
   内部阶段的配额/门耗尽，按 [CLAUDE.md](../../../../CLAUDE.md) §10 属**必须降级、不得抛出**的一类，
   与 schema 那条逃生口不同源。并进同一条统计会让它彻底看不见。
   违反 CLAUDE.md §10，不污染结果。
3. **「多」与「缺」方向相反的系统性盲区** —— 模型看到异常却把「多余」读成「缺失」；
   9 处未命中同属此形态。
4. **命中侧的表示债务审计未做** —— 多报侧已查、命中侧尚未查，两侧失效模式方向相同（都偏
   乐观），故本代 `hit@k` 只能作为上界（§4）。待办是对参与度量的 98 条台账记录逐条回读
   `stm0.puml`，见 [representation_debt.md](../docs/findings/representation_debt.md) §4.7。

## 8. 复算

```bash
cd project_1_llm_state_machine_modeling/eval/discover_matrix
python verdict_tiers.py     --generation matrix-v46-full --verdicts v46/verdicts/v46_human.json --audit /tmp/a.json
python audit_to_verdicts.py --generation matrix-v46-full --audit /tmp/a.json --out /tmp/v.json
python metrics_at_k.py      /tmp/v.json --no-direction-check      # 分母自动扣 27 条 00x8 越界 + 1 条 boundary_ruling（来源不同，不可混谈）
python full_tables.py       --generation v46-full --verdicts /tmp/v.json
python loss_stages.py       --generation matrix-v46-full --audit /tmp/a.json
python degradation_audit.py --generation matrix-v46-full
python adjudication_recheck.py --generation matrix-v46-full --audit /tmp/a.json
python run_telemetry.py     --generation matrix-v46-full --compare matrix-v37
```
