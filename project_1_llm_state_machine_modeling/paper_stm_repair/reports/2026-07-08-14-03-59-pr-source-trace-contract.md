# PR-source-trace contract report

## 1. 报告定位

本报告总结 `PR-source-trace` 的合同设计、machine artifacts、测试证据和后续 handoff。它服务于 paper1 当前主线：给定 `NL + raw/source STM_0`，发现、确认、修复 source-level behavioral issues，并回到 raw/source 层做 closure / regression audit。

本报告不是实验结果，不支持 method effectiveness claim；它只证明 source trace v0 合同、fixtures 与 tests 已经具备可复验入口。

## 2. 为什么要做 source trace

`PR-issue-ledger` / #150 已经定义了 source issue ledger v0：哪些 candidate issue 可以成为 confirmed + repair-eligible issue。但后续 repair / closure 还必须知道：

1. issue 对应 raw/source STM 里的哪个元素；
2. 该元素转换到中间可执行语义表示后对应哪个元素；
3. 中间表示中的修复是否能投影回 raw/source 层；
4. 哪些 trace 关系不能作为 source-level closure 主证据。

source trace 因此是 source-level attribution 和 closure evidence 的桥，而不是 paper contribution。

## 3. 本 PR 产物

### 3.1 文档入口

| 路径 | 作用 |
|---|---|
| [../experiment_design/source_trace/README.md](../experiment_design/source_trace/README.md) | source trace 入口。 |
| [../experiment_design/source_trace/GUIDE.md](../experiment_design/source_trace/GUIDE.md) | 后续 agent 维护规范。 |
| [../experiment_design/source_trace/source_trace_contract.md](../experiment_design/source_trace/source_trace_contract.md) | Source Trace Contract v0 主合同。 |
| [../experiment_design/source_trace/fixtures/README.md](../experiment_design/source_trace/fixtures/README.md) | 六个 synthetic fixtures 的人类可读入口。 |

### 3.2 Machine artifacts

| 路径 | 作用 |
|---|---|
| [../pipeline/evaluation/schemas/source_trace.schema.json](../pipeline/evaluation/schemas/source_trace.schema.json) | JSON Schema，固定 source trace v0 字段、relation、projection 和 attribution gate。 |
| [../pipeline/evaluation/fixtures/source_trace/](../pipeline/evaluation/fixtures/source_trace/) | 六个 source trace contract fixtures。 |
| [../pipeline/evaluation/tests/test_source_trace_schema.py](../pipeline/evaluation/tests/test_source_trace_schema.py) | schema / fixture / cross-ledger tests。 |

## 4. v0 关键设计决策

| 决策 | 内容 | 原因 |
|---|---|---|
| v0 不支持 `merged` / `inferred` | schema enum 只含 `exact` / `normalized` / `split` / `ambiguous` / `untraceable` / `conversion_artifact` | plan review 认为 `merged` / `inferred` 在无真实样例和负例测试前容易造成 attribution 漂移。 |
| 不修改 #150 issue ledger schema | 使用 `required_for_issue_ids[]` 形成 trace → issue 链接，并用 `issue_binding_policy` 锁定 relation 允许绑定的 issue status 范围 | 避免在 source trace PR 中重定义 issue lifecycle；consumer 构造 deterministic reverse index，并复制 cross-ledger status check。 |
| negative trace gate | `ambiguous` / `untraceable` / `conversion_artifact` 必须 `source_level_claim_allowed=false` 且 `closure_claim_allowed=false` | 防止无法追踪或转换产物进入 source-level closure 主结论。 |
| `normalized` 必须有 normalization evidence | `normalized` fixture / schema 要求 `normalization_report` | 防止把语义改变或无证据 normalization 当 repair gain。 |
| `split` 只能 partial | `projection_status=partially_projectable` 且 `closure_claim_allowed=false`，并要求 `projection_detail` | 拆分可用于定位，但不能单独证明 full closure。 |
| `conversion_artifact` 分层 | trace relation 与 #150 `rejected_conversion_artifact` issue status 分层定义 | 防止把 conversion/lowering 问题写成 source STM 本身问题。 |

## 5. Fixture coverage

| fixture | relation | issue linkage | 关键 gate |
|---|---|---|---|
| `exact_transition_trace.json` | `exact` | `ISSUE.GUARD.001` | projectable + positive claim boundary。 |
| `normalized_guard_trace.json` | `normalized` | `ISSUE.GUARD.001` | projectable + `normalization_report`。 |
| `split_transition_trace.json` | `split` | `ISSUE.INTERNAL.001` | partially_projectable + `projection_detail` + closure claim false。 |
| `ambiguous_trace.json` | `ambiguous` | `ISSUE.EXPR.001` candidate-only | unprojectable + negative claim boundary。 |
| `untraceable_element.json` | `untraceable` | none | empty source + `negative_trace_check`。 |
| `conversion_artifact_trace.json` | `conversion_artifact` | `ISSUE.CONV.001` rejected conversion artifact | not_applicable + conversion report + negative claim boundary。 |

## 6. Test coverage

[../pipeline/evaluation/tests/test_source_trace_schema.py](../pipeline/evaluation/tests/test_source_trace_schema.py) 覆盖：

1. source trace schema 本身合法。
2. 六个 committed fixtures 全部 validate。
3. fixtures 是 `contract_fixture`，不指向 seed、archive、runs 或本机绝对路径。
4. v0 拒绝 `merged` / `inferred`。
5. relation → projection_status gate。
6. normalized 必须包含 normalization evidence。
7. split 必须 partial、必须有 `projection_detail`、不能 closure claim。
8. negative trace relation 必须 source-level claim false / closure claim false。
9. untraceable 必须 source empty 且有 negative trace evidence。
10. conversion artifact 只关联 #150 rejected conversion issue。
11. `required_for_issue_ids[]` 必须存在于 #150 issue ledger fixtures。
12. negative trace relation 不得绑定 confirmed repair-eligible issue。
13. confirmed repair-eligible issue 必须有 projectable / partial trace coverage：
    - `ISSUE.GUARD.001` 覆盖 `T_move`；
    - `ISSUE.INTERNAL.001` 覆盖 `T_unlock_ok` / `T_unlock_alarm`。
14. reverse index 是 v0 issue-to-trace 的确定性连接方式。
15. `issue_binding_policy` 在 schema 层锁定 positive / negative relation 的 issue 绑定范围；pytest 层再核对实际 issue status。
16. exact / normalized 必须 `closure_claim_allowed=true`，且非 split relation 不允许携带 `projection_detail`。
17. schema 拒绝额外字段，避免 method-effectiveness 等临时字段混入。

## 7. 复验命令与结果

| 命令 | 结果 | 说明 |
|---|---|---|
| `python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests/test_source_trace_schema.py -q` | `18 passed in 0.15s` | source trace 单项 schema / fixture / cross-ledger gate。 |
| `python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests -q` | `45 passed in 0.25s` | evaluation 目录 source issue + source trace 测试。 |
| `PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests -q` | `110 passed in 20.04s` | conversion / representation / readiness / evaluation 组合 smoke。 |

## 8. 可以支持的结论

本 PR 可以支持：

1. source trace v0 合同已定义。
2. trace relation、projection status、attribution boundary 和 issue linkage 有 machine schema。
3. confirmed repair-eligible synthetic issue fixture 已有 positive trace coverage。
4. ambiguous / untraceable / conversion artifact 已被 machine gate 排除出 source-level closure 主证据。
5. source trace 与 #150 issue ledger 的 v0 reverse-index 连接已经可测试。

## 9. 不可支持的结论

本 PR 不支持：

1. 真实 repair loop 已经运行。
2. 真实 `STM_final` 或 raw/source patch bundle 已生成。
3. source trace 能证明 method effectiveness。
4. final evaluation rubric / baseline contract / judge prompt 已冻结。
5. archived R5.7 Better STM dry-run 可以回流为 active result。
6. `fcstm` / schema / ledger / trace 是 paper1 headline contribution。

## 10. 后续 handoff

| 后续 PR | 如何消费 source trace |
|---|---|
| `PR-loop-io` | 将 source trace ledger 纳入 run record / stage IO 合同，明确每个 stage 如何携带 `trace_ledger_id` 与 reverse index。 |
| `PR-discover-confirm` | 对 confirmed issue 输出时检查是否有 trace coverage 或标记 `required_future_trace` 未满足。 |
| `PR-repair-runner` | repair action 必须绑定 confirmed issue 与 trace entry，避免泛泛重写模型。 |
| `PR-raw-export` | 使用 `projection_status` 与 `projection_detail` 决定 raw/source patch bundle 的可投影性。 |
| `PR-closure-audit` | 只允许 positive trace relation 参与 closure 主证据；negative trace relation 必须进入 unresolved / unjudgeable / conversion artifact 分支。 |
| `PR-loop-pilot` | 用真实 case 检验 v0 relation 是否足够；若出现 `merged` / `inferred` 需求，另开 schema migration。 |

## 11. Capability-use audit

- Required references/scripts: `ai-research-writing-skill` story / reviewer gate、`research-planning` 可执行计划原则、`oh-my-codex:autoresearch` / `autoresearch-goal` 证据门禁、#150 issue ledger schema / tests。
- Inputs consumed: #100 umbrella body、#150 source issue ledger docs/schema/fixtures/tests、三路 plan review comments。
- Inputs not used and why: archived R5.7 dry-run outputs未用于 active evidence，因为当前 PR 是 source-level trace 合同，不是 Better STM adjudication。
- Artifacts produced: source trace docs、JSON Schema、six fixtures、pytest tests、本报告。
- Verification run: 17 source trace tests、44 evaluation tests、109 pipeline smoke tests。
- Remaining risk: v0 未支持真实 pilot 中可能出现的 `merged` / `inferred`；若真实 pilot 需要，必须单独扩展并补负例测试。
