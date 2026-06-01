# SL prompt generators

PR-1B 约定：`SL-*` 只暴露 prompt generator / stage spec / schema，不绑定内部 LLM wrapper。仓库内部 `agents/*` wrapper 也复用同一 prompt generator，避免 prompt drift。

## 使用边界

- prompt generator 只返回 message pack 或 markdown prompt。
- prompt generator 不调用 LLM、不读取 `.env`、不绑定 provider。
- 真实 provider 调用、ReviewRunMeta replay/cache wiring、run record writer 属于 PR-2A/PR-2B。
- `GroundingMap`、`FixPlan`、`ScenarioSet` 等输入默认由上游提供 schema-valid 对象；PR-1B 只消费并格式化它们，不负责生产。

## Generator 列表

| Stage | Generator | 主要输入 | 主要输出约束 |
|---|---|---|---|
| SL-1 | `build_sl1_initial_modeling_prompt(...)` | NL、SpecJson、upstream lists、pyfcstm grammar digest | JSON：`candidate_dsl` + `grounding_seeds` |
| SL-5 | `build_sl5_scenario_generation_prompt(...)` | NL、current DSL、inspect JSON、design summary、GroundingMap、coverage directive | JSON：`scenarios`，兼容 `TestScenario` / `ScenarioStep` |
| SL-7 | `build_sl7_model_review_prompt(...)` | NL、current DSL、GroundingMap、inspect JSON、design diagnostics、sim summary、5-component summary、warning budget exhausted、ReviewPolicy | JSON：decision/risk/findings，findings 映射 issue #14 I.2 九类 category |
| SL-9 | `build_sl9_repair_prompt(...)` | NL、current DSL、FixPlan/RevisedFixPlan、GroundingMap、selected diagnostics、grammar digest、preserve list、scenario summary | corrected pyfcstm DSL only；`suggested_fix` 只是 hint, not a command |
| SL-10B | `build_sl10b_delta_review_prompt(...)` | NL、GroundingMap、old DSL、candidate DSL、FixPlan/RevisedFixPlan、diff summary | JSON：accept/reject/revise + drift evidence |

## Fake response / parser 测试

- snapshot test 覆盖 prompt 文本中的关键 contract 字段。
- fake LLM / fixture response test 覆盖 parser 与 schema validation，不依赖真实 provider。
- invalid category / invalid decision 必须 fail loudly，不能静默放过。

## LLM stage trace 要求

每次真实调用必须保存 `ReviewRunMeta` 或等价 LLM interaction 记录：provider、model、resolved model、prompt template version、prompt hash、input hash、temperature、seed、retry、raw output hash/path、schema validation、cache key、decision threshold、failure policy、replay key。
