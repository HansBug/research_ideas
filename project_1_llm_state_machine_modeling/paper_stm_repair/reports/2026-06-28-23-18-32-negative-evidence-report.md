# R5.5 `llms-emp` negative evidence report

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.md` | `ee35e444` (2026-06-28 22:54:39 +0800) | N/A：source 在旧 smoke 前缀冻结后创建，未经历早期路径 prefix move。 | `81995de7` (2026-06-28 23:18:32 +0800)：修正 blocked probe 的审查问题，明确 committed evidence 只能支持 `not_reproducible_from_committed_evidence`，不能外推为已证明不可渲染。 | 本报告所在的 R5.5.1 migration commit（同一提交内无法自嵌最终 SHA；精确提交用 `git log --follow -- <report>` 复核）；仅迁移 human-facing report 与改写入口，不改 canonical machine facts。 | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl)；[llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)；[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json)；[r5_to_r8_negative_evidence.json](../pipeline/readiness_audit/handoff/r5_to_r8_negative_evidence.json) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## R5.5 `llms-emp` blocked probe

本文件记录 3 个 `R5.LOSS.official_scxml_unavailable` 样例的可复核失败证据。事实源是 [plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) 与 [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)。

### 1. 总结

3 个 blocked 样例均有作者一手 `NL + generated PlantUML`，但 R3.1 的 raw 与 normalized official PlantUML probe 均未获得可信 SCXML。当前 committed evidence 未证明它们可渲染；只能说明 `-checkonly` / `-tscxml` 路径失败，且当前 normalization rules 未修复。

注意：当前 committed evidence 只保存 JSON 中的 stdout / stderr tail，没有完整 stdout/stderr log 文件；本仓库快照也未提交 PlantUML jar 与 normalized candidate 单文件。因此 R5.5 对“是否可渲染”的结论是 `not_reproducible_from_committed_evidence`，而不是“已证明不可渲染”。如后续需要精确错误行和渲染性，应另开 converter follow-up probe。

### llms_emp_stm_results_0018 / gpt-4

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
- evidence: `../pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0018]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```

### llms_emp_stm_results_0028 / llama

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
- evidence: `../pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0028]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```

### llms_emp_stm_results_0037 / kimi

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
- evidence: `../pipeline/conversion/reports/plantuml_recovery_report.json#/items[pair_id=llms_emp_stm_results_0037]/normalized_preflight`

```text
ceforge.plantuml.PSystemUtils.exportDiagramsDefault(PSystemUtils.java:207)
	at net.sourceforge.plantuml.PSystemUtils.exportDiagrams(PSystemUtils.java:96)
	at net.sourceforge.plantuml.SourceFileReaderAbstract.getGeneratedImages(SourceFileReaderAbstract.java:190)
	at net.sourceforge.plantuml.Run.manageFileInternal(Run.java:510)
	at net.sourceforge.plantuml.Run.processArgs(Run.java:404)
	at net.sourceforge.plantuml.Run.manageAllFiles(Run.java:371)
	at net.sourceforge.plantuml.Run.main(Run.java:206)
```
