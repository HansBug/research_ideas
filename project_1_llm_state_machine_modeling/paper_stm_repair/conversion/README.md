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
│   ├── toolchain.py
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
2. 先做成熟工具链 / 官方工件 preflight：PlantUML CLI、Umple compiler、TTool/AVATAR XML evidence。
3. **以官方结构化导出作为 canonical 主转换路径**：PlantUML / Umple 解析 `reports/toolchain_exports/` 中的 SCXML，TTool 解析一手 XML artifact。
4. 若官方 SCXML / XML 不可用或不可置信，文本 fallback 只能作为 debug / targeted loss audit，不得生成 regex 主导的 canonical STM。
5. 生成 canonical STM JSON、conversion report、loss ledger 和 markdown summary。

## 4. 当前四例裁决

| 样例 | 格式 | R3 status | 说明 |
|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | `converted` | PlantUML `-tscxml` 成功；canonical states/transitions 来自官方 SCXML。 |
| `unified-uml-synthetic-0000` | PlantUML | `partial` | PlantUML 官方 `-checkonly` 失败且无可信 SCXML；不再用 regex fallback 生成 canonical，`canonical_output_path=null`。 |
| `sefm-ssc7-umple` | Umple | `partial` | Umple `-g Scxml` 成功；canonical states/transitions 来自官方 SCXML，原始 `.ump` 仅用于 `after(60)` targeted timing loss audit。 |
| `ttool-automatedbraking-xml` | TTool XML | `partial` | 解析一手 TTool/AVATAR XML artifact 做 SMD inventory；connector endpoint 未解析完整，不切出纯 T0 STM。 |

## 5. 输出解释

- [reports/selected_seed_examples_conversion_report.json](./reports/selected_seed_examples_conversion_report.json)：四例 conversion report；其中每条 `tool_preflight` 记录官方/成熟工具链命令、版本、syntax status、structured export status 与 fallback reason；每条 item 还显式记录 `conversion_source`、`canonical_extraction_method`、`structured_export_path`、`fallback_used`、`fallback_scope`。
- [reports/selected_seed_examples_loss_ledger.jsonl](./reports/selected_seed_examples_loss_ledger.jsonl)：所有 loss / 降级 / partial 原因。
- [reports/selected_seed_examples_summary.md](./reports/selected_seed_examples_summary.md)：便于人工浏览的概览。
- [reports/canonical/](./reports/canonical/)：`converted` / `partial` 样例的 canonical STM JSON。
- [reports/toolchain_exports/](./reports/toolchain_exports/)：官方工具链能导出的结构化证据，例如 PlantUML / Umple SCXML；PlantUML / Umple 成功样例的 canonical 主结构必须来自这些 SCXML，而不是源文本 regex。
- `blocked` / `unsupported` 样例允许 `canonical_output_path` 和 `canonical_output_sha256` 为 `null`；不得生成空 canonical STM 冒充转换成功。

## 6. 与后续阶段关系

- R4 可消费 R3 的 `R3.STATUS.*` 与 `R3.LOSS.*` code，但不得改写 R3 裁决语义。
- R5 应用 deterministic dry-run 检查 R3 输出是否足以支撑诊断 / 场景。
- R7/R8 才冻结正式实验格式范围与 experiment-grade conversion；R3 不提前承担该职责。

## 7. 官方工具链优先纪律

R3 当前不是“直接手写 parser 即可”的实现。每次转换必须先尝试或记录成熟工具链 preflight，并且 canonical conversion 主路径必须优先消费官方结构化导出：

- PlantUML：优先使用 `plantuml` 或 `plantuml.jar` 做 syntax check，并在可行时导出 SCXML；syntax/export 成功时 canonical 来自 SCXML；若官方 syntax fail，不得凭 regex fallback 标为 `converted`。
- Umple：优先使用 `umple.jar` 做 `-g Nothing` syntax/compile preflight，并在可行时导出 SCXML；canonical 来自 SCXML；原始 `.ump` 仅允许用于 `after(...)` 等 targeted loss audit。
- TTool/AVATAR：当前只确认 XML artifact 与 ttool-cli/MCP 入口，未找到稳定 headless AVATAR SMD -> SCXML/JSON/AST 导出；因此基于官方 XML artifact 做 inventory 并标 `partial`。

本地若需要复现官方 Umple preflight，可临时设置：

```bash
export UMPLE_JAR=/path/to/umple.jar
```

本仓库不把大型第三方 jar 作为源码提交；report 中只保留命令、版本、hash/路径 evidence 与官方来源链接。canonical output 只允许 `conversion_source=official_scxml/official_xml`；`no_canonical_conversion` 只能出现在 report item 中，不能写出 canonical JSON。
