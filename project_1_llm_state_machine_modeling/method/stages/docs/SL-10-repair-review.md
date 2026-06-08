---
stage_id: SL-10
stage_name: 修复后审阅 / NL-grounded Repair Review
stage_kind: LLM
---

## 目标

`SL-10` 在 PR-E1 中负责审阅 `SL-9` 产出的修复候选，判断它是否可以交给 `SC-11` 接受并回到 `SD-2` 做完整重验。它替代默认主链中的旧 `SD-10` deterministic final judge 与 `SL-10B` delta review；本地 parse / semantic / design / sim 复核仍运行，但作为 `local_check_evidence` 输入。

## 输入

### LLM 输入


- NL 原文，必须提供。
- old DSL 与 candidate DSL。
- `FixRequestBatch` 与 `SL-9` per-request accept/reject 决策。
- 完整跨 iter `FixLog`。
- diff summary。
- local deterministic checks evidence。
- GroundingMap 与 ScenarioSet 摘要。

## 输出

### LLM 输出


严格 JSON：

```json
{
  "decision": "pass|fail|rework",
  "target_resolved": true,
  "regression_detected": false,
  "drift_risk": "none|minor|major",
  "evidence": [{"summary": "reason"}],
  "rework_instructions": ["edit request"]
}
```

## 函数名或 prompt generator 名

- `build_sl10_repair_review_prompt(...)`
- `parse_sl10_repair_review_response(...)`
- `run_sl10_repair_review_llm(...)`

## 最小示例

```python
from method.stages.sl10_repair_review_prompt import build_sl10_repair_review_prompt

messages = build_sl10_repair_review_prompt(
    nl="Start moves Idle to Active.",
    grounding_map=None,
    old_dsl="state Root { state Idle; }",
    candidate_dsl="state Root { [*] -> Idle; state Idle { :: Start -> Active; } state Active; }",
    request_batch={"requests": []},
    sl9_decisions=[],
    fix_log=[],
    local_check_evidence={"parse": {"ok": True}},
)
```

## 依赖关系

- 上游：`SD-8` 生成 `FixRequestBatch`，`SL-9` 生成 candidate DSL 与 request decisions。
- 下游：`SL-10 pass` 才能进入 `SC-11`；`fail/rework` 回到 `SL-9` 继续修复并追加 `FixLog`。

## 常见失败模式

- 没有输入 NL，导致审阅无法判断语义忠实度。
- 只看 local checks，忽略 FixLog 中已经 waiver 的非硬 request。
- 把 `pass` 误解为 final success；实际仍必须回 `SD-2` 完整重验。
- 对具体样本写 lexical special-case，而不是基于 NL 与 FixLog 作普适判断。


## 失败语义

- provider/schema/empty-output retry 耗尽：进入 `SC-12`，verdict 为 `provider_error` 或 `invalid`。
- `decision=fail|rework`：写入 FixLog，回到 `SL-9` 继续修；不得直接 final success。
- `decision=pass`：进入 `SC-11`，然后回 `SD-2` 完整重验。
