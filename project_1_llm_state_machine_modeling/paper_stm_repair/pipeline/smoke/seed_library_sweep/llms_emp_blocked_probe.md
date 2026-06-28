# R5.5 `llms-emp` blocked probe

本文件记录 3 个 `R5.LOSS.official_scxml_unavailable` 样例的可复核失败证据。事实源是 [plantuml_recovery_report.json](../../conversion/reports/plantuml_recovery_report.json) 与 [llms_emp_case_matrix.jsonl](./llms_emp_case_matrix.jsonl)。

## 1. 总结

3 个 blocked 样例均有作者一手 `NL + generated PlantUML`，但 R3.1 的 raw 与 normalized official PlantUML probe 均未获得可信 SCXML。当前 committed evidence 未证明它们可渲染；只能说明 `-checkonly` / `-tscxml` 路径失败，且当前 normalization rules 未修复。

注意：当前 committed evidence 只保存 JSON 中的 stdout / stderr tail，没有完整 stdout/stderr log 文件；本仓库快照也未提交 PlantUML jar 与 normalized candidate 单文件。因此 R5.5 对“是否可渲染”的结论是 `not_reproducible_from_committed_evidence`，而不是“已证明不可渲染”。如后续需要精确错误行和渲染性，应另开 converter follow-up probe。

## llms_emp_stm_results_0018 / gpt-4

- cluster: `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`
- model:  Digital camera state machine diagrams
- issue_category: `F_unquoted_state_names_with_spaces`
- tool: PlantUML CLI / PlantUML version 1.2024.7 (Sat Sep 07 19:18:17 CST 2024)
- raw syntax status: `failed`; normalized syntax status: `failed`
- raw scxml returncode: `1`; normalized scxml returncode: `1`
- raw candidate: `normalized_candidates/0018__llms-emp-stm-subset__llms_emp_stm_results_0018__raw.puml`
- normalized candidate: `normalized_candidates/0018__llms-emp-stm-subset__llms_emp_stm_results_0018__normalized.puml`
- render status: `unknown_from_committed_r5_evidence`
- renderability recheck: `not_reproducible_from_committed_evidence`
- renderability blocker: PlantUML jar、normalized candidate 文件与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
- render probe recommended: `True`
- pre-SCXML recovery possible: `False`
- evidence: `project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0018]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```

## llms_emp_stm_results_0028 / llama

- cluster: `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`
- model:  Digital camera state machine diagrams
- issue_category: `A_non_plantuml_stm_directive`
- tool: PlantUML CLI / PlantUML version 1.2024.7 (Sat Sep 07 19:18:17 CST 2024)
- raw syntax status: `failed`; normalized syntax status: `failed`
- raw scxml returncode: `1`; normalized scxml returncode: `1`
- raw candidate: `normalized_candidates/0028__llms-emp-stm-subset__llms_emp_stm_results_0028__raw.puml`
- normalized candidate: `normalized_candidates/0028__llms-emp-stm-subset__llms_emp_stm_results_0028__normalized.puml`
- render status: `unknown_from_committed_r5_evidence`
- renderability recheck: `not_reproducible_from_committed_evidence`
- renderability blocker: PlantUML jar、normalized candidate 文件与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
- render probe recommended: `True`
- pre-SCXML recovery possible: `False`
- evidence: `project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0028]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```

## llms_emp_stm_results_0037 / kimi

- cluster: `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st`
- model: Collision avoidance sub-machine state diagram
- issue_category: `A_non_plantuml_stm_directive`
- tool: PlantUML CLI / PlantUML version 1.2024.7 (Sat Sep 07 19:18:17 CST 2024)
- raw syntax status: `failed`; normalized syntax status: `failed`
- raw scxml returncode: `1`; normalized scxml returncode: `1`
- raw candidate: `normalized_candidates/0037__llms-emp-stm-subset__llms_emp_stm_results_0037__raw.puml`
- normalized candidate: `normalized_candidates/0037__llms-emp-stm-subset__llms_emp_stm_results_0037__normalized.puml`
- render status: `unknown_from_committed_r5_evidence`
- renderability recheck: `not_reproducible_from_committed_evidence`
- renderability blocker: PlantUML jar、normalized candidate 文件与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
- render probe recommended: `True`
- pre-SCXML recovery possible: `False`
- evidence: `project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0037]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```
