# R4.5 表示桥 GUIDE

## 1. 目标与边界

本目录只维护 R3 canonical STM JSON 到 pyfcstm `.fcstm` 的 deterministic lowering。它不负责重新转换 PlantUML / Umple / TTool，也不负责 repair、LLM 调用或正式实验统计。

实现与 review 必须遵守：

1. 不读取 `.env`，不调用真实 LLM。
2. 不把 R4.5 lowering / normalization / representation gain 计入 Better STM 或 repair gain。
3. 不在论文贡献层面强调 `fcstm` / pyfcstm / DSL。
4. 对无法可信降低的对象必须 `blocked` / `partial` + loss ledger，不允许静默伪造。

## 2. lowering inventory 完整性纪律

`lowering_inventory.json` 是 R4.5 的审计主账，不只是 guard/action 清单。每个 example 至少包含：

| 分组 | 对齐基线 | 说明 |
|---|---|---|
| `events` | canonical transition 中不同 `(scope,event)` | 事件声明位置、合法化 identifier 与 raw event mapping。 |
| `guards` | canonical 中 `guard != null` 的 transitions | raw guard、mapped expression、declared variables、supported/reason code。 |
| `actions` | canonical 中 `action != null` 的 transitions | raw action、abstract/flag lowering、emitted flag。 |
| `references` | canonical transitions | source/target/scope 的 lowered endpoint、状态、reason code。 |
| `initial_final` | root + 每个 composite | initial child 推导方法；不能默认无证据选第一个 child 而不记 loss。 |
| `timing` | timed/timeout event 或 timing_level 非 none 的 transitions | `after(...)` / timeout event 的降低与 loss。 |
| `hierarchy` | canonical states | parent/child 保留情况。 |
| `blocked_supplementary` | model-level blocked examples | TTool/unified blocked 原因与补充 skeleton 范围。 |

## 3. 命名纪律

- 单段 raw text 使用 `pyfcstm.utils.to_identifier(raw_text, strict_mode=True, keyword_safe_for=["python", "java"])`。
- 多段合成名使用 `pyfcstm.utils.sequence_safe([...])` 后再过 `to_identifier(...)`。`sequence_safe` 会用双下划线连接 segment，R4.5 再经 `to_identifier` 折叠为 pyfcstm 可读单 token；此行为必须在 `name_mapping.json.tool_parameters` 中可见。
- R4.5 依赖 pyfcstm submodule `v0.4.0`（当前 commit `5f811a0f`）的 DSL grammar、`to_identifier`、`sequence_safe` 与 inspect API；后续升级 pyfcstm 时必须重跑本目录 pytest 并检查 name mapping 是否漂移。
- FCSTM lexer 中 `event`、`continue`、`E`、`if` 等保留词 / 特殊 token 不能直接作为 emitted identifier；R4.5 在 pyfcstm 工具后追加 FCSTM keyword-safe suffix，并在 `is_dsl_keyword_adjusted=true` 中记录。
- 所有 emitted identifiers 都必须进入 `name_mapping.json`：root / wrapper state、state、event、pseudo relay、guard variable、action flag、abstract action、blocked skeleton node。
- state / pseudo state 在 DSL 中用 `named` 保留 raw label；event 在当前 committed 四例中也用 `named` 保留 raw label。
- 若未来 event identifier 与 pyfcstm lexer 特殊 token 冲突导致 `event ... named ...` 无法解析，必须 blocked 或在 loss ledger 中显式记录，并以 `name_mapping.json` 保留 raw event；不得静默丢原名。

## 4. event + guard 降低

pyfcstm transition 不能直接同时带 event 与 guard。R4.5 必须使用 pseudo relay：

```fcstm
Ready -> ready_scan_barcode_is_valid_barcode_security_check_relay : scanBarcode;
ready_scan_barcode_is_valid_barcode_security_check_relay -> SecurityCheck : if [isValidBarcode > 0];
```

禁止：

1. 把 event 默认降为 event flag；
2. 丢 guard；
3. 用普通 stoppable state 作为 relay；
4. guard unsupported 时伪造表达式。

## 5. action / timing / hierarchy

- transition action 降为 `def int act_x = 0` + `effect { act_x = 1; }`。
- entry action 只在有明确 evidence 的情况下映射为 `enter abstract Foo;`。
- bool-like guard variable 默认值 `0` 是 R4.5 表示近似，必须写入 loss ledger。
- timeout/timing 仅按 event 降低，不恢复 clock semantics。
- HSM hierarchy 默认保留；跨层级 transition 只能在可解释的 boundary lifting / forced transition 下处理，并记录 loss。

## 6. 运行与验收

每次修改 exporter 后运行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/representation/src \
python -m paper_stm_repair_representation.cli export-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/representation/src \
pytest -q project_1_llm_state_machine_modeling/paper_stm_repair/representation/tests
```

验收重点：

1. `llms-emp-gpt4o-hldcs` 与 `sefm-ssc7-umple` parse/inspect 均为 `ok`。
2. `ttool-automatedbraking-xml` 与 `unified-uml-synthetic-0000` 保持 blocked，不产生伪造 `model.fcstm`。
3. `repair_contribution_allowed` 始终为 `false`。
4. `name_mapping.json` 与 `lowering_inventory.json` 可追溯到 R3 canonical ref。
5. 所有本目录 schema 与 committed reports 通过 pytest contract。
