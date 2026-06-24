# R3 conversion/GUIDE.md

## 1. 工作边界

1. 只处理 [../selected_seed_examples/](../selected_seed_examples/) 四例静态 smoke 输入。
2. 不读取 `.env`，不调用真实 LLM，不产生主实验结果。
3. 不把 converter、canonical schema、pyfcstm 或任何 DSL 写成论文主贡献。
4. 不允许为提高转换率而人工补语义、删元素或猜测 guard/action。
5. `partial` / `blocked` 是合法裁决，但必须有 source ref、status code、blocking reason 和 loss ledger。

## 2. 状态与 code 口径

| status | code | 含义 | canonical output |
|---|---|---|---|
| `converted` | `R3.STATUS.converted` | v0 adapter 可抽取足够 states / transitions，且无影响 R3 消费的已知 loss。 | 必须存在 |
| `partial` | `R3.STATUS.partial` | 可抽取部分结构，但存在 timing、hierarchy、endpoint、semantic 或 tooling loss。 | 通常存在；必须配 loss ledger |
| `blocked` | `R3.STATUS.blocked` | 输入存在或工具链存在阻塞，无法产出可信 canonical STM。 | 必须为 `null` |
| `unsupported` | `R3.STATUS.unsupported` | 格式不在 R3 目标范围。 | 必须为 `null` |

`R3.LOSS.<loss_type>.<severity>` 是后续 R4/R5 的稳定引用入口。R4 可以扩展诊断，但不得回写或重定义 R3 的 status/loss 语义。

## 3. schema 字段纪律

- canonical schema 中 `timing_level` 只能取：`none / qualitative / clock / timed_constraints / unknown`。
- canonical schema 中 `hierarchy_level` 只能取：`flat / hierarchical / concurrent / unknown`。
- conversion report 必须记录 run-level 字段：`run_id`、`created_at`、`conversion_command`、`repo_commit`、`schema_version`、`adapter_version`、`tool_*`、`source_locator`、`raw_locator`、`source_meta_path`、`loss_ledger_path`、`manual_edit_allowed=false`、`eligibility`。
- `states_count` / `transitions_count` 是 adapter inventory 规模；TTool XML 等 partial inventory 不得被 R4/R5 直接当作已解析 STM 规模使用。下游若需要只统计可语义消费的元素，应读 `resolved_states_count` / `resolved_transitions_count`。
- `blocked` / `unsupported` 不得伪造空 canonical 输出；`canonical_output_path` 和 `canonical_output_sha256` 应为 `null`。

## 4. adapter v0 纪律

### 4.1 PlantUML

v0 只覆盖四例所需子集：

- `@startuml` / `@enduml`
- `state X { ... }`
- `A --> B : label`
- quoted state name
- `[*]` 初始 / 终止伪状态

PlantUML v0 不能假定所有图都是 flat；`llms-emp-gpt4o-hldcs` 有局部 scope 和重复状态名。

### 4.2 Umple

v0 只覆盖 `class { sm { state { transition; } } }` 子集，至少解析：

- state block
- `event [guard] -> /{action} Target;`
- `entry /{...}`
- `after(n)` timer-like transition

`after(60)` 必须进入 timing loss，不得静默丢弃或当成普通无时间迁移。

### 4.3 TTool XML

v0 只做 XML inventory：

- XML well-formed check
- `AVATARStateMachineDiagramPanel`
- state / start components
- transition connectors
- guard / afterMin / afterMax 等字段原样保留

R3 不承诺把 TTool XML 无损切片为 T0 FSM/HSM/EFSM/statechart；未解析 graphical connecting points 到 exact source/target 时必须标 `partial` 并写 loss。

## 5. 输入审计

每次转换前必须核验四例 hash：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_conversion.cli convert-selected
```

生成的 [reports/selected_seed_examples_input_audit.json](./reports/selected_seed_examples_input_audit.json) 必须显示四例 `nl_hash_match=true`、`stm0_hash_match=true`、`source_pairs_exists=true`。

## 6. 测试与验收

R3 最低验收：

1. schema JSON 可由 `jsonschema` 校验。
2. 四例均有 conversion report。
3. PlantUML 两例达到 `converted` 或给出证据充分的 `partial/blocked`。
4. Umple 至少 partial，并对 timer-like loss 入账。
5. TTool XML 至少 partial / blocked 且不得静默跳过。
6. 本地 pytest 通过；如果没有 Codecov comment，不虚构覆盖率。
