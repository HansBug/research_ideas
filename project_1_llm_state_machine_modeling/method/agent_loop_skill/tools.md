# SD deterministic tools

PR-0/PR-1A 约定：`SD-*` 是确定性工具层，不调用 LLM、不读取 `.env`。这些入口用于 agent-loop runner、Path1/Path2 handoff smoke、Codex/Claude skill、人工 ref model 制作前的本地检查。


## PR-E2 skill-driven e2e 调用提醒

PR-E2 的 agent 可以直接调用本页 `SD-*` deterministic tools 来检查候选模型，但不得把这些工具包在 `method.loop.run_agent_loop(...)` 或一键 runner 里间接执行。推荐最小顺序是：

```text
run_sd2_parse -> run_sd3_semantic -> run_sd4_design -> SD-5A/SC-5F/SD-6 -> SD-8 FixRequestBatch -> SL-9 decision/repair -> SL-10 review -> 回到 SD-2
```

若某个工具因 import、语法或 pyfcstm 版本问题不可用，必须在 PR comment 中记录命令、错误摘要和影响分类；不能静默跳过并声称模型已通过验证。

特别注意：`SC-5F freeze_scenario_set` 的实际参数是 `source_dsl_hash` / `source_inspect_hash` / `source_grounding_hash`，不是原始 DSL 或 inspect dict；`SD-6` 对正式样本是 required 行为检查，不是可省略 polish。

## Python 入口

推荐从总 façade `method.stages.sd_tools` 导入；若需要按 stage 拆分，也可使用 `method.stages.sd_parse` / `sd_semantic` / `sd_design` / `sd_scenario_coverage` / `sd_sim` / `sd_fix_plan` / `sd_repair_review` 这些薄 re-export 模块。

```python
from method.schema import StageContext
from method.stages.sd_tools import (
    freeze_scenario_set,
    mark_warning_repair_attempt,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,  # PR-E1 中作为 SL-10 local_check_evidence 使用
)

context = StageContext(nl=nl)
parse_feedback, parse_meta = run_sd2_parse(current_dsl, context)
semantic_feedback, semantic_meta, build = run_sd3_semantic(current_dsl, context)
design_feedback, design_meta = run_sd4_design(context, policy_profile="generated_candidate")
fix_plan, fix_meta = run_sd8_fix_plan(
    design_feedback,
    source="design",
    grounding_map=context.grounding_map,
    before_dsl=current_dsl,
)
```

## 工具清单

| Stage | 函数 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| `SD-2` | `run_sd2_parse(current_dsl, context=None)` | pyfcstm DSL | `ParseFeedback`, `StageResultMeta` | 复用 `method.feedback.parse.check_parse`。 |
| `SD-3` | `run_sd3_semantic(parse_ok_dsl, context=None)` | parse-ok DSL | `SemanticFeedback`, `StageResultMeta`, `BuildResult` | canonical build helper 写入 `StageContext.ast/model`，避免重复隐式构建。 |
| `SD-4` | `run_sd4_design(context, policy_profile="generated_candidate")` | `StageContext.model`, warning budget | `DesignFeedback`, `StageResultMeta` | 消费 `inspect_model().to_json()`；E hard-block，high-risk W budgeted repair，I/info 入 trace。 |
| `SD-5A` | `run_sd5a_scenario_coverage(current_dsl, scenarios)` | DSL + scenario candidates | coverage report, `StageResultMeta` | coverage probe；有缺口时给 retry directive。 |
| `SC-5F` | `freeze_scenario_set(...)` | scenario candidates + hashes | `ScenarioSet`, `StageResultMeta` | 冻结 oracle，后续 repair 不随意重生成。 |
| `SD-6` | `run_sd6_sim(current_dsl, scenario_set, context=None)` | DSL + frozen `ScenarioSet` | `SimFeedback`, `StageResultMeta` | scenario 缺失时显式 error，不静默跳过。 |
| `SD-8` | `run_sd8_fix_plan(selected_feedback, source=..., ...)` | 最早失败 feedback + grounding | legacy `FixPlan` 或 `RevisedFixPlan`, `StageResultMeta` | PR-E1 runtime 会把它提升为 `FixRequestBatch`；`suggested_fix_hints` 仅供参考。 |
| local checks for `SL-10` | `run_sd10_repair_review(nl=..., grounding_map=..., old_dsl=..., candidate_dsl=..., fix_plan=..., scenario_set=...)` | NL + grounding + before/after DSL + plan + oracle | `RepairReviewFeedback`, `StageResultMeta` | 作为 `SL-10` 的 `local_check_evidence`；不再是默认主链最终裁判。 |

## Warning budget

```python
blocking_keys = [item.instance_key for item in design_feedback.blocking_items]
mark_warning_repair_attempt(context.warning_budget_state, blocking_keys)
```

默认每个 high-risk warning instance 有 `DEFAULT_WARNING_REPAIR_BUDGET = 2` 次修复预算。预算耗尽后降级为 advisory，仍必须进入 trace / run record。

## 契约要点

- enabled deterministic stage 必须产出 `StageResultMeta`。
- `skipped` 必须带 `skipped_reason`；`error` 必须带 `stage_error` 或 `output_validation_error`。
- `advisory` 不阻塞，但必须进入 trace / run record。
- `inspect_model` 的 suggested fix 只能作为 `FixPlan.suggested_fix_hints`，不是强制执行脚本。
- SD 工具不调用 LLM、不读取 `.env`；需要 LLM 时只通过后续 `SL-*` prompt generator 或外部 agent 调用。
