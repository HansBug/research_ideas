# ledger_v2：当前 expected issue ledger

`ledger.json` 是 Paper1 当前唯一的 expected issue ledger。它包含 145 条条目：`D2` 98 条、`D1` 47 条；L0/L1/L2 为 71/35/39。每条记录保留 pair、NL/PlantUML 定位、问题描述、D/L basis、来源族和到 `provenance/` 工作单的链接。

| 文件或目录 | 角色 |
| --- | --- |
| [ledger.json](./ledger.json) | 当前 expected issue 的机器可读真源 |
| [predicate_gold_v1/](./predicate_gold_v1/README.md) | 当前 145 条内部谓词后端能力、typed inputs、执行裁决与 receipt 的 evaluation-only overlay；不改写 `ledger.json` |
| [l_tier.json](./l_tier.json) | L0/L1/L2 的逐条派生记录与依据 |
| [JUDGING_PROTOCOL.md](./JUDGING_PROTOCOL.md) | ledger 形成和命中判定的冻结协议材料 |
| [provenance/](./provenance/README.md) | 逐 pair review、人工裁决、去重和来源追溯 |
| [X1V2_RESULTS.md](./X1V2_RESULTS.md) | 已替代的历史 X1v2 人工裁定结果，仅保留 provenance |

`D` 表示问题主张在 ledger 形成时的裁定，`L` 表示 expected issue 的问题性质与陈述所需的信息范围：L0 是点状/表面对齐性质，L1 是结构或局部状态性质，L2 是跨迁移、路径、可达性、终止、响应或全局交互的行为性质。L 不规定算法、predicate、backend 或 witness；L2 不蕴含 W2。D/L 不等同于 method 的 W 或 D，也不等同于人工完成的 relation/validity。方法不读取此 ledger；issue #195 的人工 relation 裁定只接收评测层显式投影的 expected material，evaluation 再以人工输出机械计算 hit 和 precision。

`l_tier.json` 是当前 L 定义和逐条依据的唯一入口。`ledger.json` 中内嵌的历史 provenance 文本保持冻结，以便复现既有制品；其中任何旧的“须构造或排除”措辞不构成当前 L 口径，也不改变 L 值、ID、计数或 hit 分母。

`predicate_gold_v1/` 保存内部的 source-backed executable-property 与输入审计。它不进入 method registry、prompt、routing 或 package data，也不改变既有 hit、W、K/N/I。旧 registry 的 `118/145` 只是一份 `planned_mapping_not_new_method_measurement` 设计期快照；当前审计记录以该目录的 canonical JSON 为准。

当前实验结果、W-on-hits、K/N/I、predicate usage 与成本资格只以 [v60/current 与 X1v2 baseline 最终归档](../../final_results/v60_current_vs_x1v2_baseline/README.md) 的 v4 公平对照层为准。特别是，X1v2 baseline v3 的 overall FULL 为 227/435 = 52.18%，不是本目录保留的历史数字。

历史 v46、v27-stream、v26 及旧 X1v2 人工裁定网格的可比性说明见 [实验历史索引](../../archive/experiment_history/README.md)。
