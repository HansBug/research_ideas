# R3 转换合同与 converter v0

本目录是第一篇论文 `paper_stm_repair` 的 R3 转换层：把 [selected_seed_examples/](../selected_seed_examples/) 中四个静态 `<NL, STM_0>` smoke 样例转换、部分转换或阻塞裁决到 R3 canonical STM JSON，并生成 conversion report 与 loss ledger。

## 1. 定位

- R3 是 **开发 / 审计级最小转换链路 v0**，只服务四例 smoke panel、R4/R5 dry-run 与 schema/ledger 接口验证。
- R3 不是通用 UML / SysML / PlantUML / Umple / TTool 转换器。
- R3 committed report 只是 reviewer fixture / contract evidence，不是 R7/R8 experiment-grade conversion，也不是主实验结果。
- 转换收益、人工规范化和后续 repair loop 收益必须分离；loss ledger 中所有 `repair_contribution_allowed` 均为 `false`。

## 2. 路径结构

```text
conversion/
├── README.md
├── GUIDE.md
├── toolchain_survey.md
├── schemas/
│   ├── canonical_stm.schema.json
│   ├── conversion_report.schema.json
│   └── loss_ledger.schema.json
├── src/paper_stm_repair_conversion/
│   ├── cli.py
│   ├── models.py
│   ├── report.py
│   ├── schema.py
│   └── adapters/
├── tests/
└── reports/
```

## 3. 运行方式

请在仓库根目录运行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_conversion.cli convert-selected
```

该命令会：

1. 校验四例 `nl.txt`、`stm0.*` 与 `source_meta.json` 的 SHA-256 是否一致。
2. 调用 PlantUML / Umple / TTool XML adapter。
3. 生成 canonical STM JSON、conversion report、loss ledger 和 markdown summary。

## 4. 当前四例裁决

| 样例 | 格式 | R3 status | 说明 |
|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | `converted` | 层次化 PlantUML；v0 解析状态、局部 scope、迁移 label。 |
| `unified-uml-synthetic-0000` | PlantUML | `converted` | flat synthetic PlantUML；仅用于格式跑通，不支撑控制系统有效性 claim。 |
| `sefm-ssc7-umple` | Umple | `partial` | 状态 / 迁移可抽取；`after(60)` 作为 qualitative timing loss 入账。 |
| `ttool-automatedbraking-xml` | TTool XML | `partial` | 只做 AVATAR SMD inventory；不解析 graphical connector 到精确 endpoint，不切出纯 T0 STM。 |

## 5. 输出解释

- [reports/selected_seed_examples_conversion_report.json](./reports/selected_seed_examples_conversion_report.json)：四例 conversion report。
- [reports/selected_seed_examples_loss_ledger.jsonl](./reports/selected_seed_examples_loss_ledger.jsonl)：所有 loss / 降级 / partial 原因。
- [reports/selected_seed_examples_summary.md](./reports/selected_seed_examples_summary.md)：便于人工浏览的概览。
- [reports/canonical/](./reports/canonical/)：`converted` / `partial` 样例的 canonical STM JSON。
- `blocked` / `unsupported` 样例允许 `canonical_output_path` 和 `canonical_output_sha256` 为 `null`；不得生成空 canonical STM 冒充转换成功。

## 6. 与后续阶段关系

- R4 可消费 R3 的 `R3.STATUS.*` 与 `R3.LOSS.*` code，但不得改写 R3 裁决语义。
- R5 应用 deterministic dry-run 检查 R3 输出是否足以支撑诊断 / 场景。
- R7/R8 才冻结正式实验格式范围与 experiment-grade conversion；R3 不提前承担该职责。
