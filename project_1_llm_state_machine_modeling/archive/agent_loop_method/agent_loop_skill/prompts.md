# SL prompt generators

PR-1B 约定：`SL-*` 只暴露 prompt generator / stage spec / schema，不绑定内部 LLM wrapper。仓库内部 `agents/*` wrapper 也复用同一 prompt generator，避免 prompt drift。程序化调用优先从 `archive.agent_loop_method.stages.sl_prompt_api` 或总 façade `archive.agent_loop_method.stages.api` 导入；`archive.agent_loop_method.stages.sl_prompt_common` 是多个 SL prompt module 共享的底层 schema/format helper，不是面向 skill 的 API。


## PR-E2 外部 agent 使用方式

在 PR-E2 中，Codex / Claude Code 可以使用本页 `SL-*` prompt generator 或 stage 文档作为提示蓝本，自行调用自身 CLI / subagent / 其他 provider 产出候选、场景、repair 或 review。不要误解为 skill 会自动绑定唯一 provider。

所有真实 LLM 输出都应在 PR comment 中至少摘要记录：输入上下文、输出候选、schema/格式检查、重试或修复原因。若输出过长，保留最终候选模型全文与关键失败/修复证据。

PR-E2 producer 使用 SL prompt 时，应额外提醒模型：当前 pyfcstm parser 不支持 `def bool` / `true` / `false`，布尔语义用 `int` flag 表达；外部输入不能只靠 `// @external` 注释让 SD-4 自动通过。

PR-E2 的最终模型评审必须使用 [nfrr_evaluation_guide.md](./nfrr_evaluation_guide.md)：不要只让 LLM 给“高/中/低质量”评价，而要输出 NFRR claim、NL coverage ledger、obligation alignment、scenario/mutation evidence、八维 vector、tier、cap reasons 与 allowed_use。若目标是 Ground-Truth 级 ref-model candidate，prompt 中应显式要求 `final_tier >= T3` 的证据包；若达不到，则必须如实降级为 `T2 within_NL_candidate` 或 diagnostic evidence。

## 使用边界

- prompt generator 只返回 message pack 或 markdown prompt。
- prompt generator 不调用 LLM、不读取 `.env`、不绑定 provider。
- 真实 provider 调用、ReviewRunMeta/interaction record wiring 属于 PR-B2 的 `archive.agent_loop_method.llm_stages`；top-down driver 与 run record 完整写入属于 PR-B1/PR-C。
- `GroundingMap`、`FixRequestBatch`、`FixLog`、`ScenarioSet` 等输入默认由上游提供 schema-valid 对象；PR-1B/PR-E1 只消费并格式化它们，不负责生产。

## Generator 列表

| Stage | Generator | 主要输入 | 主要输出约束 |
|---|---|---|---|
| SL-1 | `build_sl1_initial_modeling_prompt(...)` | NL、SpecJson、upstream lists、pyfcstm grammar digest | JSON：`candidate_dsl` + `grounding_seeds` |
| SL-5 | `build_sl5_scenario_generation_prompt(...)` | NL、current DSL、inspect JSON、design summary、GroundingMap、coverage directive | JSON：`scenarios`，兼容 `TestScenario` / `ScenarioStep` |
| SL-7 | `build_sl7_model_review_prompt(...)` | NL、current DSL、GroundingMap、inspect JSON、design diagnostics、sim summary、5-component summary、warning budget exhausted、ReviewPolicy | JSON：decision/risk/findings，findings 映射 issue #14 I.2 九类 category |
| SL-9 | `build_sl9_repair_prompt(...)` | NL、current DSL、FixRequestBatch、完整 FixLog、GroundingMap、selected diagnostics、grammar digest、preserve list、scenario summary | JSON：per-request accept/reject + candidate DSL；legacy DSL-only 仅兼容 |
| SL-10 | `build_sl10_repair_review_prompt(...)` | NL、GroundingMap、old DSL、candidate DSL、FixRequestBatch、SL-9 decisions、完整 FixLog、diff、local check evidence | JSON：pass/fail/rework + evidence + rework_instructions |
| SL-10B | `build_sl10b_delta_review_prompt(...)` | NL、GroundingMap、old DSL、candidate DSL、FixPlan/RevisedFixPlan、diff summary | legacy/ablation：accept/reject/revise + drift evidence |

最小 repair prompt 顺序：

```text
SD-8 legacy FixPlan/RevisedFixPlan
-> 整理为 FixRequestBatch
-> build_sl9_repair_prompt(..., fix_request_batch=..., fix_log=...)
-> build_sl10_repair_review_prompt(..., fix_request_batch=..., sl9_decisions=..., fix_log=..., local_check_evidence=...)
```

## Fake response / parser 测试

- snapshot test 覆盖 prompt 文本中的关键 contract 字段。
- fake LLM / fixture response test 覆盖 parser 与 schema validation，不依赖真实 provider。
- invalid category / invalid decision 必须 fail loudly，不能静默放过。

## LLM stage trace 要求

每次真实调用必须保存 `ReviewRunMeta` 或等价 LLM interaction 记录：provider、model、resolved model、prompt template version、prompt hash、input hash、temperature、seed、retry、raw output hash/path、schema validation、cache key、decision threshold、failure policy、replay key。

## PR-B2 adapter trace 补充

`archive.agent_loop_method.llm_stages` 对每个 SL stage 都会记录：`prompt_messages`、`raw_output`、`parsed_output`、`schema_validation_ok/error`、`usage`、`provider/model`、`attempts`、`retry_error`、prompt/input/raw hash 与 redaction report。

注意：`SL-5` 的 coverage directive retry 由 `SD-5A` / runtime 决定何时触发；PR-B2 只保证带 directive 的 `SL-5` LLM call 可重放、可审计。`SL-9` 中的 `suggested_fix` 永远是 context hint，不是强制编辑命令；PR-E1 后 `SL-9` 还必须读取 FixLog，避免重复修复已被 waiver/reject 的 request。
