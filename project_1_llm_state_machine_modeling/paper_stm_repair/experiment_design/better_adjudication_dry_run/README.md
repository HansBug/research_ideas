# better_adjudication_dry_run/ — R5.7.5 constructed STM_k 覆盖性 dry-run

> 冻结时间：2026-07-05 02:10:39。本目录是 R5.7.5 的人类可读 dry-run 文库；机器 bundle 在 [../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/)。

## 1. 定位

本目录只维护 R5.7.5 的 constructed answer-key suite：20 个 `STM_k` 候选都是人工 / 确定性构造的 protocol dry-run case，像单元测试一样覆盖 Better STM 裁决协议的 outcome、gate 与 anti-gaming 风险。本目录本身不运行真实 repair loop，不调用真实 LLM，不证明方法有效。

R5.7.5 后续已基于这些 constructed case 派生 full blind adjudication bundle，并运行 Claude / DeepSeek / Codex 三方 isolated judges；该阶段的 canonical 总入口是 [../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md)，机器 bundle 在 [../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/README.md](../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/README.md)。这些 blind judge 结果也只支持 evaluation protocol readiness / calibration / limitation，不能写成真实 repair effectiveness。

## 2. 阅读顺序

先读 [../evaluation_logic.md](../evaluation_logic.md)、[../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md)、[../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md)、[../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md)，再读 [../protocols/better_adjudication_prompt_v0.md](../protocols/better_adjudication_prompt_v0.md) 与 [../protocols/better_adjudication_output_schema_v0.json](../protocols/better_adjudication_output_schema_v0.json)。若要理解 R5.7.5 最终状态，应继续读 full blind prompt/schema：[../protocols/better_adjudication_blind_prompt_v0.md](../protocols/better_adjudication_blind_prompt_v0.md)、[../protocols/better_adjudication_blind_output_schema_v0.json](../protocols/better_adjudication_blind_output_schema_v0.json)，以及 canonical 总报告：[../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md)。

## 3. 目录清单

| 文件 | 用途 |
|---|---|
| [2026-07-05-02-10-39-suite-index.md](./2026-07-05-02-10-39-suite-index.md) | 20 case 总览、coverage 表和禁止主张。 |
| `2026-07-05-02-10-39-cXX-*.md` | 单 case 的输入事实源、构造变化、expected gate path、expected verdict、禁止外推。 |
