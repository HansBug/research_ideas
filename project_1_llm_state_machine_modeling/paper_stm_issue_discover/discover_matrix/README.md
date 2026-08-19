# discover_matrix — 实验与评测

> ⭐⭐ **本论文的缺陷台账只有一份**：[ledger_v2/ledger.json](./ledger_v2/ledger.json)，**145** 条（`D2` 98 + `D1` 47，每条逐条落定 `L0`/`L1`/`L2`）。⛔ 仓库里出现过的 99 / 126 / 319 / 321 / 323 / 380 / 429 **一个都不是台账条目数**。

⭐ **本页只做路由，不做第二事实源。** 全部数字、口径、限制与复验命令都在 [ledger_v2/README.md](./ledger_v2/README.md)。

## 一、两个子目录

| 路径 | 内容 | 什么时候进去 |
| :-- | :-- | :-- |
| ⭐ [ledger_v2/](./ledger_v2/) | **台账**（145 条）· **判定协议**（判定前写定）· **X1v2 基线在台账上的精确结果** · **证据链** [`provenance/`](./ledger_v2/provenance/)（第一版台账、60 份逐 pair 复审、54 份工作单含全部人工裁决与逐条 meta review、三方 D 档判读包、去重台账） | 看结果、复算数字、追溯某条缺陷怎么定的 |
| [docs/](./docs/) | 学术口径：`protocol/`（判定协议、缺陷分类学、边界裁定、出处政策）· `findings/`（已裁定的发现）· `generations/`（历代事前登记，每代次一个子目录、文件名 `preregistered.md`） | 查判定规则、查某条规则为什么这么定；⭐ 方法最终输出、hit 与 FP 的唯一边界见 [final_output_metrics_policy.md](./docs/protocol/final_output_metrics_policy.md) |

⛔ **v46 主臂与 v46 时代的评测数据、分析脚本已整体转入冷归档** [../archive/r10_ledger_v1_and_v46/](../archive/r10_ledger_v1_and_v46/)（归档不是删除，那里有复活导引）。⛔ 本目录**不含任何 v46 数字**：历史上出现过的 `hit@1 60.4%`、`76.2%` 一律不是当前口径。

## 二、三句话读懂当前状态

1. ⭐ **台账**：145 条，`D` 档（缺陷主张站不站得住）与 `L` 档（陈述这个错误需要哪一层）逐条落定，无第四类、无「界外」。
2. ⭐ **基线**：历史的 X1v2 精确网格是 145 × 6（两个生成模型 × 三轮），全台账 `hit@1` **59.8%** · `hit@3` **70.3%** · `hit@all` **47.9%**；⛔ 最弱处是 `D2 × L2`（34 条，`hit@all` 仅 **29.4%**）。
3. ⭐ **当前同模型对照已按最终发布边界完成**：gpt-5.6-luna 下 v26-dnorm 与 X1v2 各三轮、54 个 eligible pair 均由独立 Sol semantic judge 完成对账；方法侧只读 D1/D2 `report_issue_clusters`，X1v2 只读 `parsed_output.issues`。旧含 D0 raw-finding 数字 `226/435` 与 `566/953 FP` 仍废止；Sol/Luna 的同输入 54/54 对照见 [judge comparison report](../reports/2026-08-19-judge-model-comparison.md)。
4. ⚠️ **口径限制**：⭐ v46 已裁定不在新台账上重测（2026-08-17），因此不能把 v46 历史数字与任何当前结果相减；当前主结果使用 Sol semantic judge，Luna 仅作同输入低成本敏感性对照，不能把两套 judge 混成一个 headline。

⭐ 以上三条的完整表、逐档拆分与全部五条限制，读 [ledger_v2/README.md](./ledger_v2/README.md) 与 [ledger_v2/X1V2_RESULTS.md](./ledger_v2/X1V2_RESULTS.md)。

## 三、边界（不随台账换代而变）

建模对象是 $M = (S, E, V, Tr, A)$：**无时钟变量 $C$、无不变式 $Inv$、无正交区并发语义**。由此导出的两项永久裁定 —— `00x8` 六个 pair 永久排除（故全量网格恒为 54 pair）、hold-out 永久不用 —— 见 [docs/protocol/nl_scope_rule.md](./docs/protocol/nl_scope_rule.md) 与 [docs/protocol/method_provenance_policy.md](./docs/protocol/method_provenance_policy.md)。
