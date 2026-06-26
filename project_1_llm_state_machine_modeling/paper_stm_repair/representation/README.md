# R4.5 canonical STM 到 fcstm 表示桥

## 1. 定位

`representation/` 是第一篇论文 R4.5 的内部表示桥工作区，负责把 R3 的 `canonical_stm.json` 降到 pyfcstm 可解析的 `.fcstm` DSL，并同步产出 `name_mapping.json`、`lowering_inventory.json`、`fcstm_export_loss_ledger.jsonl` 与 `parse_inspect_report.json`。

它的角色是：

```text
R3 canonical STM JSON -> R4.5 .fcstm / pyfcstm inspect report -> R5 deterministic smoke
```

R4.5 不是论文主贡献，不调用 LLM，不读取 `.env`，不生成 `STM_k`，也不执行 repair loop。所有 lowering / loss / approximation 都归入 representation / conversion attribution，不能计入 Better STM 或 repair gain。

## 2. 路径结构

```text
representation/
├── README.md
├── GUIDE.md
├── schemas/
│   ├── fcstm_export_report.schema.json
│   ├── fcstm_export_loss_ledger.schema.json
│   ├── lowering_inventory.schema.json
│   └── name_mapping.schema.json
├── src/paper_stm_repair_representation/
│   ├── __init__.py
│   ├── cli.py
│   ├── lowering.py              # canonical view / lowering / .fcstm render / report 主入口
│   └── pyfcstm_names.py
├── reports/
│   ├── fcstm_export_report.json
│   ├── fcstm_export_loss_ledger.jsonl
│   ├── lowering_inventory.json
│   └── fcstm_exports/<example_id>/
│       ├── model.fcstm
│       ├── name_mapping.json
│       ├── lowering_inventory.json
│       └── parse_inspect_report.json
└── tests/
    ├── test_r45_export_contract.py
    ├── test_r45_name_mapping.py
    └── test_r45_schema_contract.py
```

其中 `lowering.py` 是 R4.5 的主实现入口，同时承担 canonical model view、lowering 策略、`.fcstm` 渲染、loss ledger 与 export report 生成；本 PR 未单独拆出 `canonical_to_fcstm.py`。

## 3. 运行方式

依赖仓库根目录已有 Python 环境和 `pyfcstm` submodule。当前 R4.5 contract 以 pyfcstm `v0.4.0`（submodule commit `5f811a0f`）为准；升级 pyfcstm 后必须复跑本目录测试并检查 committed reports 是否发生命名/inspect 漂移。新环境应先在仓库根目录执行：

```bash
git submodule update --init --recursive
pip install -r requirements.txt
pip install -e ./pyfcstm
```

导出四个 selected seed examples：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/representation/src \
python -m paper_stm_repair_representation.cli export-selected
```

预期摘要：

```json
{"blocked": 2, "converted": 2, "examples": 4, "partial": 0}
```

运行 R4.5 tests：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/representation/src \
pytest -q project_1_llm_state_machine_modeling/paper_stm_repair/representation/tests
```

## 4. 当前四例输出

| example_id | R4.5 状态 | 输出 |
|---|---|---|
| `llms-emp-gpt4o-hldcs` | `converted` | 保留 HSM 层次，输出 [model.fcstm](./reports/fcstm_exports/llms-emp-gpt4o-hldcs/model.fcstm) 与 inspect report。 |
| `sefm-ssc7-umple` | `converted` | event+guard 通过 pseudo relay，bool guard 降为 int guard，action 降为 flag，输出 [model.fcstm](./reports/fcstm_exports/sefm-ssc7-umple/model.fcstm)。 |
| `ttool-automatedbraking-xml` | `blocked` | R3 仍是 TTool XML inventory-only 且 endpoint unresolved；R4.5 不伪造 `.fcstm`。 |
| `unified-uml-synthetic-0000` | `blocked` | R3 没有可信 canonical JSON；R4.5 不替换样例、不伪造模型。 |

## 5. 关键语义策略

1. **命名**：主路径使用 `pyfcstm.utils.to_identifier(..., strict_mode=True, keyword_safe_for=["python", "java"])` 与 `pyfcstm.utils.sequence_safe([...])`，不手写 regex sanitizer。
2. **原名保真**：state / pseudo state 使用 `named` 保留 raw label；event 在当前 committed 四例中也使用 `named`。若未来某个 event 合法化后仍与 pyfcstm lexer 特殊 token 冲突，`name_mapping.json` 必须继续作为 raw event 的事实源，不允许丢失原名。
3. **event+guard**：pyfcstm 不允许同一 transition 同时出现 event 与 guard；R4.5 必须通过 pseudo relay 降低为 `source -> relay : Event; relay -> target : if [guard];`。
4. **层次**：默认保留 hierarchy，不 flatten。跨层级 transition 只在可审计的 boundary lifting / forced transition 模式下降低，并写入 loss ledger。
5. **timing**：`after(60)` 等时间语义不恢复 clock，只使用 R3 SCXML 中已有 timeout event，并记录 timing lowering / loss。
6. **blocked honesty**：TTool/unified 不具备可信 canonical / endpoint 时保持 blocked，不为通过 smoke 伪造 `.fcstm`。

## 6. 与上下游关系

- 上游 R3：[../conversion/README.md](../conversion/README.md) 提供 canonical JSON、conversion report 与 loss ledger。
- 上游 R4：[../evaluation/README.md](../evaluation/README.md) 提供诊断 / 场景 / Better STM gate 草案。
- 下游 R5 只消费 R4.5 committed `.fcstm` / report，不应在 R5 再补写 exporter。

## 7. 学术注意点

- `.fcstm` 是内部可机检载体，论文中只能弱化为 implementation representation，不进标题、摘要或贡献列表。
- `fcstm_export_loss_ledger.jsonl` 中所有 `repair_contribution_allowed=false`；任何表示转换带来的可解析性改善都不能算作 repair loop 改进。
- R5/R6/R7 引用 R4.5 输出时，应同时读取 `lowering_inventory.json` 和 loss ledger，避免把 representation approximation 当作 STM 语义真实变化。
