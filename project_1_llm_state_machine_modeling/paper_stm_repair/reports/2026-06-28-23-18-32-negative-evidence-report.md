# R5.5 `llms-emp` negative evidence report

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排；新增证据时只新增 key，不批量改旧 key。

## R5.5 `llms-emp` blocked probe

本文件记录 3 个 `R5.LOSS.official_scxml_unavailable` 样例的可复核失败证据。事实源是 [plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) 与 [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) [src-neg-recovery][src-neg-case]。

### 1. 总结

3 个 blocked 样例均有作者一手 `NL + generated PlantUML`，但 R3.1 的 raw 与 normalized official PlantUML probe 均未获得可信 SCXML。当前 committed evidence 未证明它们可渲染；只能说明 `-checkonly` / `-tscxml` 路径失败，且当前 normalization rules 未修复 [clm-neg-probe-failure]。

注意：当前 committed evidence 只保存 JSON 中的 stdout / stderr tail，没有完整 stdout/stderr log 文件；本仓库快照也未提交 PlantUML jar。candidate loose files 未单独提交，但 raw / normalized candidate 可从 committed [workdir.zip](../pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip) members 复验。因此 R5.5 对“是否可渲染”的结论是 `not_reproducible_from_committed_evidence`，而不是“已证明不可渲染”。如后续需要精确错误行和渲染性，应另开 converter follow-up probe [clm-neg-workdir-members][clm-neg-returncode-risk]。

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
- renderability blocker: PlantUML jar 与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；candidate loose files 未单独提交，但 raw / normalized candidate 可从 committed `workdir.zip` members 复验。R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
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
- renderability blocker: PlantUML jar 与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；candidate loose files 未单独提交，但 raw / normalized candidate 可从 committed `workdir.zip` members 复验。R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
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
- renderability blocker: PlantUML jar 与完整 stdout/stderr log 未作为 R5.5 committed evidence 保存；candidate loose files 未单独提交，但 raw / normalized candidate 可从 committed `workdir.zip` members 复验。R5.5 只能复用 R3.1 -checkonly/-tscxml 摘要证据，完整 render probe 应另开 converter follow-up。
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

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.md` | `ee35e44407c85835dc4f3ec669477e298d89cb8a` (2026-06-28 22:54:39 +0800) | `81995de735586b602284e02cea0f0754f36b37b1` (2026-06-28 23:18:32 +0800, negative evidence fact freeze) | `81995de735586b602284e02cea0f0754f36b37b1` (2026-06-28 23:18:32 +0800)：修正 blocked probe 的审查问题，明确 committed evidence 只能支持 `not_reproducible_from_committed_evidence`，不能外推为已证明不可渲染。 | `1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl)；[llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)；[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json)；[r5_to_r8_negative_evidence.json](../pipeline/readiness_audit/handoff/r5_to_r8_negative_evidence.json) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-neg-blocked] | `blocked_probe` | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) | `jsonl` | 支撑 3 个 llms-emp blocked case 的 issue、syntax/scxml status、`r5_loss_codes` 与 renderability caveat | rows: `raw_pair_id in {0018,0028,0037}`；field: `r5_loss_codes=["R5.LOSS.official_scxml_unavailable"]` |
| [src-neg-recovery] | `plantuml_recovery` | [plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) | `json` | 支撑 raw / normalized official PlantUML preflight 与 artifact archive policy | `#/items[] where pair_id=...`、`#/artifact_archive` |
| [src-neg-workdir-zip] | `workdir_zip` | [workdir.zip](../pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip) | `zip` | 保存 raw / normalized candidate members；避免提交数千 loose files | `normalized_candidates/0018...{raw,normalized}.puml` 等；`sha256=500955e1c6d7d5b33b92a5915f8f93ee6099335a32a9f7d73dae2a12acbc7750`；hash file: [workdir.zip.sha256](../pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip.sha256) |
| [src-neg-case] | `case_matrix` | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | `jsonl` | 支撑 blocked pair 的 cluster / LLM / negative evidence role | rows: `raw_pair_id in {0018,0028,0037}` |
| [src-neg-r8-handoff] | `r8_handoff` | [r5_to_r8_negative_evidence.json](../pipeline/readiness_audit/handoff/r5_to_r8_negative_evidence.json) | `json` | 支撑 blocked 进入 R8 negative evidence / follow-up 的 handoff | `#/items[] where pair_id=...` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-neg-probe-failure] | `R5-NEG-C1` | 3 个 llms-emp blocked 样例均为一手 `NL + generated PlantUML`，但 raw / normalized official SCXML probe 均未获得可信 SCXML。 | `trace` | `blocked_probe` fields `r5_loss_codes`、`raw_syntax_status`、`normalized_syntax_status`、`raw_scxml_returncode`、`normalized_scxml_returncode`; `plantuml_recovery.items[].{raw_preflight,normalized_preflight}` | [cmd-neg-probe] | `high` | 只说明 committed R3.1/R5.5 evidence 下失败，不证明永远不可渲染。 |
| [clm-neg-workdir-members] | `R5-NEG-C2` | candidate loose files 未单独提交，但 raw / normalized candidate 可从 committed `workdir.zip` members 复验。 | `trace` | `plantuml_recovery#/artifact_archive`、`workdir_zip` member pattern、`workdir.zip.sha256` | [cmd-neg-workdir] | `high` | 仍缺 PlantUML jar、完整 stdout/stderr log 与独立 render probe。 |
| [clm-neg-returncode-risk] | `R5-NEG-C3` | `returncode=200` 与 `scxml_returncode=1` 需区分；最终信任 `syntax_status=failed` 与 `structured_export_status=scxml_not_trusted_after_syntax_failure`。 | `risk` | `plantuml_recovery.items[].raw_preflight` / `normalized_preflight` | [cmd-neg-probe] | `high` | 不应只引用单一 returncode 作结论。 |
| [clm-neg-handoff] | `R5-NEG-C4` | 这些 case 进入 negative evidence / converter follow-up，而不是 repair loop 已修复或可直接主实验。 | `decision` | `case_matrix.r5_6_story_role=negative_evidence`、`r8_handoff` | [cmd-neg-probe] | `high` | 后续若补完整 probe，可更新分类；当前不进入主 claim。 |

### A.4 复验命令

```bash
# [cmd-neg-probe] CMD-NEG-1 / CMD-NEG-3 / CMD-NEG-4
python - <<'PY'
import json, pathlib
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
probe=[json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl').read_text().splitlines() if l.strip()]
recovery=json.load(open(base/'pipeline/conversion/reports/plantuml_recovery_report.json'))
by_pair={i['pair_id']: i for i in recovery['items']}
for r in probe:
    assert r['r5_loss_codes'] == ['R5.LOSS.official_scxml_unavailable'], r
    item=by_pair[r['raw_pair_id']]
    print(r['raw_pair_id'], r['r5_loss_codes'], r['issue_category'], r['raw_syntax_status'], r['normalized_syntax_status'], r['renderability_recheck_status'])
    for stage in ['raw_preflight','normalized_preflight']:
        pf=item[stage]
        print(' ', stage, {'returncode': pf['returncode'], 'scxml_returncode': pf['scxml_returncode'], 'syntax_status': pf['syntax_status'], 'structured_export_status': pf['structured_export_status']})
PY
```

```bash
# [cmd-neg-workdir] CMD-NEG-2
python - <<'PY'
import zipfile, pathlib, hashlib
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
zp=base/'pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip'
expected=(base/'pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip.sha256').read_text().split()[0]
actual=hashlib.sha256(zp.read_bytes()).hexdigest()
print('workdir_zip_sha_ok', actual == expected, actual)
with zipfile.ZipFile(zp) as z:
    names=set(z.namelist())
    for pair in ['0018','0028','0037']:
        raw=[n for n in names if n.startswith(f'normalized_candidates/{pair}__') and n.endswith('__raw.puml')]
        norm=[n for n in names if n.startswith(f'normalized_candidates/{pair}__') and n.endswith('__normalized.puml')]
        print(pair, raw, norm)
PY
```
