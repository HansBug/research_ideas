# ledger_v2：当前 expected issue ledger

`ledger.json` 是 Paper1 当前唯一的 expected issue ledger。它包含 145 条条目：`D2` 98 条、`D1` 47 条；L0/L1/L2 为 71/35/39。每条记录保留 pair、NL/PlantUML 定位、问题描述、D/L basis、来源族和到 `provenance/` 工作单的链接。

| 文件或目录 | 角色 |
| --- | --- |
| [ledger.json](./ledger.json) | 当前 expected issue 的机器可读真源 |
| [l_tier.json](./l_tier.json) | L0/L1/L2 的逐条派生记录与依据 |
| [JUDGING_PROTOCOL.md](./JUDGING_PROTOCOL.md) | ledger 形成和命中判定的冻结协议材料 |
| [provenance/](./provenance/README.md) | 逐 pair review、人工裁决、去重和来源追溯 |
| [X1V2_RESULTS.md](./X1V2_RESULTS.md) | 已替代的历史 X1v2 Judge 结果，仅保留 provenance |

`D` 表示问题主张在 ledger 形成时的裁定，`L` 表示陈述该问题所需的分析层级。它们不等同于 method 的 W 或 D，也不等同于 Judge 的 relation/validity。方法不读取此 ledger；Semantic Judge 的 relation 阶段只接收评测层显式投影的 expected material，evaluation 再以其输出计算 hit 和 precision。

当前实验结果、W-on-hits、K/N/I、predicate usage 与成本资格只以 [v60/current 与 X1v2 baseline 最终归档](../../final_results/v60_current_vs_x1v2_baseline/README.md) 为准。特别是，X1v2 在当前 issue #195 rejudge 中的 overall FULL 为 211/435 = 48.51%，不是本目录历史表中的百分比。

历史 v46、v27-stream、v26 及旧 X1v2 Judge 网格的可比性说明见 [实验历史索引](../../archive/experiment_history/README.md)。
