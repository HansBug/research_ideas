# v46 全量 324 格：运行结果审计

审计对象：`runs/paper1/matrix-v46-full`（本地，`runs/` 被 gitignore；证据以本目录下的
判定表、遥测表与本文件为准）。审计执行于结果发布之后，**发现并更正了一处分母错误**（§3）。

## 0. 冻结与溯源

| 项 | 值 | 核验方式 |
| :-- | :-- | :-- |
| 运行代码 | `ca41369e46c09eafe6bfbfe64c3754b02c6d8fee` | `CODE_VERSION.txt`，`written_before_launch: yes` |
| 该 commit 是否在远端 | 是 | `git branch -r --contains ca41369e` |
| 启动时 `src` 脏改动 | **0 files** | `CODE_VERSION.txt` |
| 运行至今 `src` 是否被改 | **否** | `git log ca41369e..HEAD -- .../feedback_loop/src/` 为空 |
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

## 3. ⚠️ 审计发现的分母错误（已更正）

`EIS-0043-02` 的台账字段：

```
boundary_ruling:   out_of_scope
boundary_effect:   从能力分母剔除。注意它是 6/6 命中，剔除使 hit@1 由 51.5% 降至 50.0%。
boundary_ruled_by: independent adjudication, 2026-08-07
boundary_rationale: 唯一容器为真正 PlantUML 正交区者；按正交语义读作者的源是合式的。
                   该记录的前提只在 R4.5 把两区摊平成顺序子态后才成立 —— 为表示层产物，非作者缺陷。
```

**存在明确裁定要求剔出能力分母，而 `metrics_at_k` 读的是 `in_scope`（对 126 条全为 `True`，
它记的不是这件事），裁定未被执行。** 首份报告的分母因此为 99 而非 98。

📌 **同时必须记下：`full_tables.py` 本来就正确输出了双分母** —— 表 2 说明里明写
「其中 1 条经独立边界裁定为 `out_of_scope`……剔除后：360/588 = 61.2%」。
**工具没错，是首份报告只抄了前一个数字。** 这是本轮第三次同形态失误（另两次：误读
`metrics_at_k` 的拒算原因、把 `adjudication_recheck` 的被拒列表当成裁定）——
共同点是把工具输出当**结论**引用，而不是当**需要读完的材料**。这三个工具恰恰都是设计来
强迫读者停下来看的。

- **修复**：`metrics_at_k._out_of_scope_record_ids()` 改为同时读 `boundary_ruling`；
  由 [test_scope_vs_holdout_are_different.py](./test_scope_vs_holdout_are_different.py)
  的 `test_a_boundary_ruling_in_the_ledger_is_actually_honoured` 钉住。
- **影响**：该记录在 v37 与 v46 **都是 6/6**，故只同等抬高两侧绝对值，**差值几乎不变**。
- 全库扫描确认这是**唯一**一条「在分母内但 `boundary_effect` 要求剔除」的记录。

## 4. 更正后的最终结果（分母 98 条 × 2 臂 × 3 轮 = 588 位）

| 口径 | v37 | **v46** | 差 |
| :-- | --: | --: | --: |
| `hit@1` | 274/588 = 46.6% | **364/588 = 61.9%** | **+15.3pp** |
| `hit@3` | 106/196 = 54.1% | **141/196 = 71.9%** | **+17.8pp** |
| `hit@all` | 77/196 = 39.3% | **98/196 = 50.0%** | **+10.7pp** |
| claude `hit@1` | 132/294 = 44.9% | 188/294 = 63.9% | +19.0pp |
| gpt `hit@1` | 142/294 = 48.3% | 176/294 = 59.9% | +11.6pp |

⚠️ v46 一列已含 2026-08-10 逐格复核上修（+4 位，全在 `EIS-0037-01`）。
变更前的首发数字为 `hit@1` 360/588 = 61.2%、`hit@3` 140/196 = 71.4%、`hit@all` 97/196 = 49.5%，
上修依据与双份数字见 [V46_RESULT.md](./V46_RESULT.md) §1.5。

判定来源：A 层自动 + 人工，见 [verdicts/v46_human.json](./verdicts/v46_human.json)（579 条
人工判定，每条带 `argument`）。

## 5. 成本（本次新增审计维度）

数据源为各格 `telemetry_summary`，导出工具 [run_telemetry.py](./run_telemetry.py)，
逐格明细 [telemetry/v46_cells.json](./telemetry/v46_cells.json)、
对照 [telemetry/v37_summary.json](./telemetry/v37_summary.json)。

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

**逐节点耗时（v46）**：`convert_assertions` 49.2%、`split_requirements` 37.8%、
`review_requirements` 5.7%、`review_assertions` 3.4%、`adjudicate_results` 2.6%。
**前两者合计 88%**，且都随需求条数线性增长 —— 与 §7 第 1 条残留缺陷同源。

📌 **效率反而下降**：每百万 output token 的命中位数，v37 为 **27.6**、v46 为 **21.0**（−24%）。
命中率的提升有相当一部分是**多花算力换来的**，不是纯效率提升。只报命中率而不报成本会掩盖这一点。

## 6. ✅ 多报侧已判定（本节于 2026-08-10 重写，原「未判定」结论已作废）

- 已发布 issue **1105 条**（v37 为 566，1.95×），而命中位只涨到 1.32×。
- 命中位 370 ⇒ 被台账认领的 issue ≤ 366 条，其余未被任何台账记录认领。
- 这批未认领产出**已归并为 293 个同质簇并逐条人工裁定**（八个并行判定组 + 一组回读原件复核）：

| 裁定 | 簇数 | 占比 |
| :-- | --: | --: |
| 表示债务（R4.5 编译损失，非模型缺陷） | 129 | 44.0% |
| 无 NL 依据（过度规定） | 100 | 34.1% |
| 假阳性（元素其实存在） | 24 | 8.2% |
| **真实台账漏记** | **23** | **7.8%** |
| 内容已被台账承载 | 13 | 4.4% |
| 越界（M 边界外） | 4 | 1.4% |

**结论**：「产出变多」既不是纯粹的发现能力增强，也不是纯粹的噪声增加——
**最大的一块（44.0%）根本不是模型的问题，是我们自己编译链的信息损失被当成了缺陷**。
23 簇真漏记归并到根因后只有 4 条，且**全部 ≤3/6 格，无一稳定复现**。

详见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)（结论与交叉表）、
[V46_UNEXPECTED_MERGED.md](./V46_UNEXPECTED_MERGED.md)（归并后的问题）、
[V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)（293 簇逐条判据）、
[REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)（表示债务的定义与论文口径）。

⚠️ CLAUDE.md §3.5.2 要求的 `over@1` / `over@any` 口径：本轮以**稳定性维度**（簇在 6 格中
出现几次）实现，见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md) 表 A。
**179/293（61%）只出现在 1 个格里**，即多报以单次采样噪声为主。

## 7. 残留缺陷（v47 入口，按严重度）

1. **需求集规模失控** —— 中位 15 条，12 格超 60、最大 100；超 60 条的 12 格里 3 格降级
   （25%，全局 2.8%），全部是 gpt 臂、全部落在同一份 NL 的六个 pair（条件从句最密集）。
   耗时侧亦印证：`convert_assertions` + `split_requirements` 占 88% 且随条数线性增长。
   **应加需求集规模约束或合并策略，而不是继续修单个门。**
2. **schema 校验失败缺节点内原地重试** —— `responder._retryable_error` 对 `ValueError`
   返回 `False`，而 pydantic 的 `ValidationError` 是其子类；本代 7 次整格冷启动重跑全由此而来。
   违反 CLAUDE.md §10，不污染结果。
3. **「多」与「缺」方向相反的系统性盲区** —— 模型看到异常却把「多余」读成「缺失」；
   9 处未命中同属此形态。
4. ~~多报侧未判定~~ —— 已于 2026-08-10 完成判定，见 §6。

## 8. 复算

```bash
cd project_1_llm_state_machine_modeling/eval/discover_matrix
python verdict_tiers.py     --generation matrix-v46-full --verdicts verdicts/v46_human.json --audit /tmp/a.json
python audit_to_verdicts.py --generation matrix-v46-full --audit /tmp/a.json --out /tmp/v.json
python metrics_at_k.py      /tmp/v.json --no-direction-check      # 分母自动扣除 28 条越界记录
python full_tables.py       --generation v46-full --verdicts /tmp/v.json
python loss_stages.py       --generation matrix-v46-full --audit /tmp/a.json
python degradation_audit.py --generation matrix-v46-full
python adjudication_recheck.py --generation matrix-v46-full --audit /tmp/a.json
python run_telemetry.py     --generation matrix-v46-full --compare matrix-v37
```
