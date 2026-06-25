# R3 selected_seed_examples 转换 v0 摘要

本文件由 `python -m paper_stm_repair_conversion.cli convert-selected` 生成，是 R3 reviewer fixture；它不是最终实验结果。

| example_id | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | syntax | structured export | losses | 说明 |
|---|---|---|---:|---:|---|---|---|---|---:|---|
| `llms-emp-gpt4o-hldcs` | `plantuml` | `converted` | 7 | 7 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 |  |
| `sefm-ssc7-umple` | `umple` | `partial` | 7 | 22 | `qualitative` | `flat` | `ok` | `scxml_export_ok` | 1 | Umple official SCXML rewrites after(...) timer-like transitions; R3 preserves this as targeted timing loss while canonical structure remains SCXML-derived. |
| `ttool-automatedbraking-xml` | `ttool_xml` | `partial` | 245 | 233 | `timed_constraints` | `concurrent` | `xml_wellformed_checked_by_python_etree` | `official_xml_available_no_scxml_json_ast_export_documented` | 2 | TTool XML adapter performs XML/SMD inventory only: it extracts AVATAR SMD panels, state/start components and transition connector records, but does not yet resolve graphical connecting points to exact source/target states or slice a pure T0 state machine from the full SysML/AVATAR artifact. |
| `unified-uml-synthetic-0000` | `plantuml` | `partial` | 0 | 0 | `none` | `flat` | `failed` | `scxml_not_trusted_after_syntax_failure` | 2 | Official PlantUML syntax check failed; R3 does not use any source-text parser as canonical conversion source. The example cannot be marked converted. R3 不允许在官方工具链缺失、不可执行、syntax check 失败或结构化导出失败时，静默退回 regex/string/source-text parser，也不允许复用已提交 SCXML fixture 冒充本次转换证据。 |

Loss ledger 行数：5

所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。

## 官方工具链失败细节

以下内容记录的是官方/成熟工具链返回值与截断后的输出；R3 不会因此退回正则或 source-text parser，也不会复用 committed SCXML。

### `unified-uml-synthetic-0000`

- tool: `PlantUML CLI`
- command: `['java', '-jar', 'external-local-tool/plantuml.jar', '-checkonly', 'selected_seed_examples/unified-uml-synthetic-0000/stm0.puml']`
- returncode: `200`
- structured_export_status: `scxml_not_trusted_after_syntax_failure`
- fallback_used: `False`；canonical_output_path: `None`

stderr tail:

```text
Some diagram description contains errors

Exception in thread "main" java.lang.UnsupportedOperationException: SCXML
	at net.atmp.ImageBuilder.createUGraphic(ImageBuilder.java:349)
	at net.atmp.ImageBuilder.writeImageInternal(ImageBuilder.java:249)
	at net.atmp.ImageBuilder.write(ImageBuilder.java:231)
	at net.sourceforge.plantuml.PlainDiagram.exportDiagramNow(PlainDiagram.java:65)
	at net.sourceforge.plantuml.error.PSystemError.exportDiagramNow(PSystemError.java:244)
	at net.sourceforge.plantuml.AbstractPSystem.exportDiagram(AbstractPSystem.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```
