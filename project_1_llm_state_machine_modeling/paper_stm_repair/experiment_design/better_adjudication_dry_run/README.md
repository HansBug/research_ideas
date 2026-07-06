# better_adjudication_dry_run/ — R5.7.5 constructed STM_k 覆盖性 dry-run

> 冻结时间：2026-07-05 02:10:39。本目录是 R5.7.5 的人类可读 dry-run 文库；机器 bundle 在 [../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/)。

## 1. 定位

R5.7.5 不运行真实 repair loop，不调用真实 LLM，不证明方法有效。它构造 20 个 `STM_k` 候选，像单元测试一样覆盖 Better STM 裁决协议的 outcome、gate 与 anti-gaming 风险。

## 2. 阅读顺序

先读 [../evaluation_logic.md](../evaluation_logic.md)、[../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md)、[../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md)、[../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md)，再读 [../protocols/better_adjudication_prompt_v0.md](../protocols/better_adjudication_prompt_v0.md) 与 [../protocols/better_adjudication_output_schema_v0.json](../protocols/better_adjudication_output_schema_v0.json)。

## 3. 目录清单

| 文件 | 用途 |
|---|---|
| [2026-07-05-02-10-39-suite-index.md](./2026-07-05-02-10-39-suite-index.md) | 20 case 总览、coverage 表和禁止主张。 |
| `2026-07-05-02-10-39-cXX-*.md` | 单 case 的输入事实源、构造变化、expected gate path、expected verdict、禁止外推。 |
