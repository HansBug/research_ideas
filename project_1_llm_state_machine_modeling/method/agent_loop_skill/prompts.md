# SL prompt generators

PR-1B 约定：`SL-*` 只暴露 prompt generator / stage spec / schema，不绑定内部 LLM wrapper。仓库内部 `agents/*` wrapper 也复用同一 prompt generator，避免 prompt drift。


## PR-E2 外部 agent 使用方式

在 PR-E2 中，Codex / Claude Code 可以使用本页 `SL-*` prompt generator 或 stage 文档作为提示蓝本，自行调用自身 CLI / subagent / 其他 provider 产出候选、场景、repair 或 review。不要误解为 skill 会自动绑定唯一 provider。

所有真实 LLM 输出都应在 PR comment 中至少摘要记录：输入上下文、输出候选、schema/格式检查、重试或修复原因。若输出过长，保留最终候选模型全文与关键失败/修复证据。

PR-E2 producer 使用 SL prompt 时，应额外提醒模型：当前 pyfcstm parser 不支持 `def bool` / `true` / `false`，布尔语义用 `int` flag 表达；外部输入不能只靠 `// @external` 注释让 SD-4 自动通过。

## 使用边界

- prompt generator 只返回 message pack 或 markdown prompt。
- prompt generator 不调用 LLM、不读取 `.env`、不绑定 provider。
- 真实 provider 调用、ReviewRunMeta/interaction record wiring 属于 PR-B2 的 `method.llm_stages`；top-down driver 与 run record 完整写入属于 PR-B1/PR-C。
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

## PR-B2 adapter trace 补充

`method.llm_stages` 对每个 SL stage 都会记录：`prompt_messages`、`raw_output`、`parsed_output`、`schema_validation_ok/error`、`usage`、`provider/model`、`attempts`、`retry_error`、prompt/input/raw hash 与 redaction report。

注意：`SL-5` 的 coverage directive retry 由 `SD-5A` / runtime 决定何时触发；PR-B2 只保证带 directive 的 `SL-5` LLM call 可重放、可审计。`SL-9` 中的 `suggested_fix` 永远是 context hint，不是强制编辑命令。
