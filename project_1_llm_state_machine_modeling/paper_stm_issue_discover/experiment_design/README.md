# experiment_design/ — 下一轮实验的设计工作区

> ⛔ **本目录不是判定口径与指标的真源，一个字都不是。**
>
> | 你要找 | 真源在哪 |
> | :-- | :-- |
> | 命中判据、多报侧分类学、分母口径、语料筛选规则、方法出处口径 | [../discover_matrix/docs/protocol/](../discover_matrix/docs/protocol/)（11 份） |
> | `hit@1` / `hit@3` / `hit@all` / `over@k` 的**计算实现** | [../discover_matrix/metrics_at_k.py](../discover_matrix/metrics_at_k.py) |
> | 当前（v46）的实验结果、逐层分析与全部局限 | [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) |
> | 历代事前登记与代次记录 | [../discover_matrix/v46/preregistered.md](../discover_matrix/v46/preregistered.md)、[../discover_matrix/docs/generations/](../discover_matrix/docs/generations/) |
>
> **本目录只服务一件事：设计下一轮尚未开跑的实验。** 一旦某条设计真的跑了、并产生了口径，
> 那条口径的归宿是 `../discover_matrix/docs/protocol/`，不是这里。

## 1. 为什么要把这条边界写死

这个位置历史上出过一次问题：2026-07 建立的 issue lifecycle 脚手架（25 份文件）
一度同时承担「设计工作区」与「口径定义处」两个身份，于是同一件事在两处各有说法。
当 paper1 于 2026-08 收窄为 **issue discover 单独成篇**后，那套脚手架里
Repair / Confirm / closure / regression 的部分整体作废，而它定义的口径又已被
`discover_matrix/docs/protocol/` 用真实运行重写了一遍。

**结论：设计工作区只能产出「待做的实验方案」，不能产出「判定规则」。**
判定规则必须由真实运行倒逼出来，且只允许住在 protocol 目录里。

## 2. 本目录有什么

| 文件 | 职责 |
| :-- | :-- |
| [README.md](./README.md) | 本页：定位、边界、导航 |
| [GUIDE.md](./GUIDE.md) | 下一轮实验的设计纪律（引用仓库根 `CLAUDE.md`，不复制条文） |
| [next_round.md](./next_round.md) | **主体**：下一轮实验的候选项清单，每项含问题 / 阻塞 / 成本 / 依赖 |

三份，不再多。原来那套 25 份的多层目录结构不重建。

## 3. 上一代脚手架归档到哪、哪些还有用

原 25 份已整体归档到
[../archive/r7_issue_lifecycle_scaffold/experiment_design/](../archive/r7_issue_lifecycle_scaffold/experiment_design/)。
它由四块组成：顶层三份（`README` / `GUIDE` / `SUMMARY`）、`metrics/`、
`issue_lifecycle/`（11 份）、`source_trace/`（10 份）。

### 3.1 仍有价值的部分（已逐份核实）

以下判断来自实际回读归档原文，不是转述：

| 归档材料 | 为什么仍有价值 | 与 v46 结果的对应 |
| :-- | :-- | :-- |
| [issue_lifecycle/source_level_issue_definition.md](../archive/r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/source_level_issue_definition.md) §5 **conversion artifact 归因边界** | 它在 2026-07 就把「问题来自 conversion / lowering / normalization 而非源模型」单列成一个不可计入方法产出的类别 | 这正是 v46 §7.5 的 **⚙️ 表示债务**，按条目占多报侧 **46.5%**、是最大一块。**当时的处置与现在不同**：归档文件写的是 `rejected_conversion_artifact`（拒掉），v46 选的是「单独成类报告」并把归属留给导师裁定 |
| 同上 §4 **folded event / expression debt 默认只能 `candidate_only`** | 「作者把多个东西压成一个名字，不等于源模型错了」这条判断当时就立住了 | 对应 v46 §7.5 的子类 `D1` 析取备选融合（61 条目）与 `D3` 槽位焊死（18 条目） |
| 同上 §3 **两条 confirmation 路径**及其证据要求 | `nl_grounded_behavioral_issue` 要求 NL 证据 + 源模型证据 + typed behavior 证据三者齐备；`raw_internal_inconsistency` 则**允许无 NL 证据**，但必须给出「为什么此处不需要 NL」的 rationale | 第二条路径直指 v46 §6.3 的 `wellformedness` 层（27 条记录，`hit@1` 48.1%，且零命中里占 10 条）——**当时已经预见到「有一类缺陷不从任何 NL 句子推出」，只是没有落成运行入口**。v46 §9 的第一项「补一条模型驱动的巡检入口」本质上就是把这条路径实装 |
| 同上 §2 **六个状态定义**（`candidate_only` / `confirmed` / `rejected_conversion_artifact` / `rejected_other` / `out_of_scope` / `insufficient_evidence`） | 五个是纯 discover 侧分类 | 与 v46 §7.2 的五类裁定同构但不同名，且 `insufficient_evidence` 对应现在的**谓词拒答**机制（v46 §4.2 ⚠️） |
| [issue_lifecycle/fixtures/](../archive/r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/fixtures/) 的 **6 个 fixture** | 每个覆盖一个分支：folded event / NL-grounded guard mismatch / raw-internal inconsistency / conversion artifact / timed out-of-scope / insufficient evidence。**六个分支全部是 discover 侧的** | 可直接作为下一轮分类器或巡检入口的回归样例 |

### 3.2 对「约 80% 是纯 discover 材料」这一说法的修正

按**主题**算，`issue_lifecycle/` 大致如此；但按**行数**算要打折，且有两处必须说清：

1. **`issue_ledger_contract.md` 的一半是 repair 侧的。** 它的 §4 `repair eligibility gate`
   （`confirmation_status == confirmed and downstream_repair_allowed == true and ...`）
   与 §5 的五条规则里有四条（Repair 不得对无 `confirmed issue_id` 的目标 `fix`、
   Confirm 只审本轮 disposition、canonical export、C closure audit）**已随论文收窄整体作废**。
   `issue_lifecycle/README.md` §4 的「与后续阶段的接口」表同理，5 行里 4 行作废。
2. ⚠️ **fixture 与 schema 的机器事实源根本不在归档里，它们还活着。**
   归档的只是 6 份人读 README（每份 7 行）；机器版在
   [../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../pipeline/evaluation/schemas/source_issue_ledger.schema.json)、
   [../pipeline/evaluation/fixtures/source_issue_ledger/](../pipeline/evaluation/fixtures/source_issue_ledger/)、
   [../pipeline/evaluation/tests/test_source_issue_ledger_schema.py](../pipeline/evaluation/tests/test_source_issue_ledger_schema.py)，
   **仍在仓库运行路径上、仍在被测试约束**。而该 schema 里带着已作废的 repair 侧字段
   `downstream_repair_allowed`。要不要清理它是一个独立决定，见 [next_round.md](./next_round.md) 的 TODO。

### 3.3 明确不再有价值的部分

- `source_trace/`（10 份，含 169 行的 `source_trace_contract.md`）：它服务的是
  「accepted repair 如何回写成 fresh canonical source `STM_k`」，属 repair 论文范围。
  ⚠️ 但注意它的 `negative attribution gate` 概念与 §3.1 的 conversion artifact 是同一件事的
  另一半，若下一轮要量化表示债务，值得回看一眼。
- `metrics/README.md`：全部内容是「未冻结」的占位与 repair 侧指标方向
  （closure / regression / export success）。已被 `metrics_at_k.py` 与 v46 报告完全取代。
- 顶层 `SUMMARY.md` 与 `GUIDE.md`：主体是 R5.7 Better STM 归档说明与 Repair-Confirm 流程纪律，
  两者都已作废。

## 4. 推荐阅读顺序

1. **想知道现在的口径是什么** → 不要读本目录，直接去
   [../discover_matrix/docs/protocol/](../discover_matrix/docs/protocol/)。
2. **想知道现在的结果是什么** → 读
   [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md)，它自包含。
3. **想设计下一轮实验** → 先读 [GUIDE.md](./GUIDE.md) 立纪律，再读 [next_round.md](./next_round.md) 挑项。
4. **想考古上一代脚手架** → 从
   [../archive/r7_issue_lifecycle_scaffold/](../archive/r7_issue_lifecycle_scaffold/) 进，
   并先读本页 §3 判断哪些还作数。

## 5. 更新日志

| 时间 | 更新内容 |
| :-- | :-- |
| 2026-08-11 | 原 25 份 issue lifecycle 脚手架归档，本目录重建为「下一轮实验的设计工作区」三件套；写死「本目录不是判定口径真源」的定位；逐份核实归档材料的残余价值。 |
