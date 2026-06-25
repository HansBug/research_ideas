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
- conversion report 必须记录 run-level 字段：`run_id`、`created_at`、`conversion_command`、`repo_commit`、`schema_version`、`adapter_version`、`tool_*`、`tool_preflight`、`source_locator`、`raw_locator`、`source_meta_path`、`loss_ledger_path`、`manual_edit_allowed=false`、`eligibility`。
- `tool_preflight` 必须写清楚成熟/官方工具是否真正运行、syntax status、structured export status、导出证据路径/hash、fallback reason；不能只写“已调研”。
- `states_count` / `transitions_count` 是 adapter inventory 规模；TTool XML 等 partial inventory 不得被 R4/R5 直接当作已解析 STM 规模使用。下游若需要只统计可语义消费的元素，应读 `resolved_states_count` / `resolved_transitions_count`。
- `blocked` / `unsupported` 不得伪造空 canonical 输出；`canonical_output_path` 和 `canonical_output_sha256` 应为 `null`。
- canonical STM JSON 的 `metadata.conversion_source` 只允许 `official_scxml / official_xml`。`no_canonical_conversion` 只能出现在 conversion report item 中，用于说明某个样例没有可信 canonical 输出；它不得写入 canonical JSON。

## 4. 官方工具链与 adapter v0 纪律

R3 的默认顺序是 **官方/成熟工具链 preflight -> 官方结构化导出 -> 以结构化导出作为 canonical 主转换路径 -> targeted audit -> loss ledger**。不得把 regex/string parser 写成 canonical 主路径，也不得在官方工具失败时仍标 `converted`。

缺少 PlantUML / Umple / Java runtime 或显式 jar 路径无效时，CLI 必须 loudly fail，并在错误信息中给出下载、环境变量与复验命令建议；不得复用 committed SCXML，不得静默 fallback 到 regex/string/source-text parser，不得把旧 report fixture 当作当前转换 evidence。错误信息与 report evidence 中应明确出现 no-fallback 裁决，避免 reviewer 误以为转换器会“摆烂”或悄悄降级。

每个 conversion report item 必须写清：`conversion_source`、`canonical_extraction_method`、`structured_export_path`、`fallback_used`、`fallback_scope`。`tool_preflight.evidence` 应保留官方命令、return code、stderr/stdout tail、setup hint、no-fallback policy；官方 syntax/export 失败的样例还应保留 `failure_observation`。R3 目前不允许 source-text fallback；Umple 的 `after(...)` 扫描属于 `targeted_audit_used`，不能写成 fallback，也不能参与 states/transitions canonical 抽取。canonical output 只允许 `conversion_source=official_scxml/official_xml`；`no_canonical_conversion` 只能出现在 report item 中，不能写出 canonical JSON。

### 4.1 PlantUML

v0 不再用 regex/string parser 作为 PlantUML canonical 主路径。PlantUML canonical 主路径只能是 `-tscxml` 官方 SCXML：

- states / transitions / hierarchy 从 SCXML XML 节点抽取；
- canonical element `raw_ref` 指向 `stm0.scxml:...` 节点路径；
- 源 `.puml` 文本最多用于 debug / 人工定位，不得重建整机结构。

PlantUML v0 不能假定所有图都是 flat；`llms-emp-gpt4o-hldcs` 有局部 scope 和重复状态名，必须依赖 SCXML 层级证据。

必须先通过 PlantUML CLI / jar 做 syntax preflight，并在可行时导出 SCXML：

```bash
java -jar plantuml.jar -checkonly selected_seed_examples/<id>/stm0.puml
java -jar plantuml.jar -tscxml selected_seed_examples/<id>/stm0.puml
```

若缺少 PlantUML / Java runtime / jar 路径错误，CLI 必须直接失败并给出配置建议。若官方 syntax check 或 SCXML export 失败，该样例最多只能标 `partial/blocked`，并必须写入 `R3.TOOLCHAIN.OFFICIAL_SYNTAX_FAILED` 或等价 diagnostic 与 tooling loss；不得用 source-text parser 产出 canonical states/transitions。

若某个 PlantUML smoke 样例被官方工具判为 syntax/export 失败，R3 可以另外维护只读候选探测报告，用于后续人工决定是否替换同源样例；候选探测不得自动改写 [../selected_seed_examples/](../selected_seed_examples/)。

### 4.2 Umple

v0 不再用 regex/string parser 作为 Umple canonical 主路径。Umple canonical 主路径只能是 `-g Scxml` 官方 SCXML：

- state / transition / guard / script 从 SCXML XML 节点抽取；
- canonical element `raw_ref` 指向 `stm0.scxml:...` 节点路径；
- 原始 `.ump` 文本只允许用于 targeted audit，例如发现 `after(n)` 被 SCXML 改写后记录 timing loss。

`after(60)` 必须进入 timing loss，不得静默丢弃或当成普通无时间迁移。

必须优先用 Umple compiler 做 syntax/compile preflight，并在可行时导出 SCXML：

```bash
java -jar umple.jar -g Nothing selected_seed_examples/<id>/stm0.ump
java -jar umple.jar -g Scxml selected_seed_examples/<id>/stm0.ump
```

若缺少 Umple / Java runtime / jar 路径错误，CLI 必须直接失败并给出配置建议。Umple 官方 SCXML 若重写 `after(60)` 等原始 timing 语法，R3 只能用原始 `.ump` 做 targeted timing/loss audit；canonical states/transitions 仍必须来自官方 SCXML。

### 4.3 TTool XML

v0 只做 XML inventory：

- XML well-formed check
- `AVATARStateMachineDiagramPanel`
- state / start components
- transition connectors
- guard / afterMin / afterMax 等字段原样保留

R3 不承诺把 TTool XML 无损切片为 T0 FSM/HSM/EFSM/statechart；未解析 graphical connecting points 到 exact source/target 时必须标 `partial` 并写 loss。

TTool/AVATAR 当前只确认官方 XML artifact 与 ttool-cli/MCP 入口，未确认稳定 headless SMD -> SCXML/JSON/AST 导出；因此 R3 必须显式记录 `official_xml_available_no_scxml_json_ast_export_documented`，并把 `resolved_states_count` / `resolved_transitions_count` 保持为语义可消费计数。

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
3. PlantUML 两例必须有官方 syntax preflight；syntax fail 的样例不得标 `converted`。
4. Umple 至少 partial，并对 timer-like loss 入账；若 `umple.jar` 可用，canonical states/transitions 必须来自官方 SCXML。
5. TTool XML 至少 partial / blocked 且不得静默跳过；必须说明官方 headless structured export 是否有证据。
6. 本地 pytest 通过；如果没有 Codecov comment，不虚构覆盖率。
7. `test_cli_regenerates_four_example_report` 与 `test_cli_invokes_configured_external_toolchains` 使用 fake Java / fake PlantUML / fake Umple 验证 CLI 会真实调用外部工具链；`test_cli_fails_loudly_when_required_toolchains_missing` 验证缺工具时必须 loud fail。
8. 本地真实重生成 report 时必须配置 `PLANTUML_JAR` 与 `UMPLE_JAR`，不能依赖已提交的 SCXML fixture。CI 若不安装第三方 jar，应至少保留 schema/report/canonical fixture 校验和 fake-toolchain 回归。
9. `unified-uml-synthetic-0000` 当前作为官方工具失败边界样例保留；若未来替换为同源可导出 SCXML 的候选，必须同步更新 `nl.txt`、`stm0.puml`、`source_meta.json`、样例 README、hash audit、conversion report 和 [reports/unified_uml_plantuml_candidate_probe.json](./reports/unified_uml_plantuml_candidate_probe.json)。

## 7. R3.1 PlantUML normalization / recovery 纪律

当任务涉及 [normalization/](./normalization/) 时，除本 GUIDE 的 R3 no-fallback 纪律外，还必须遵守：

1. normalization 必须发生在 PlantUML `-tscxml` 之前；不得在 adapter 内部从源文本直接构造 canonical states/transitions。
2. 每条变换必须写入 [reports/plantuml_normalization_ledger.jsonl](./reports/plantuml_normalization_ledger.jsonl)，包含 rule id、line/span、before/after、raw hash、normalized hash、risk tier 与 eligibility 口径。
3. 任何高风险规则（comment-out、entry/do/exit loss、dependency 注释、fork/join 降级等）默认只能作为 supplementary / manual-review；不得进入主 repair / verification statistics。
4. R3.1 report 必须保留三种恢复率：`technical_scxml_pass_all_rules` / `low_risk_scxml_pass` / `main_eligibility_included`。
5. `main_eligibility_included=true` 必须同时满足低风险规则、normalized official SCXML 可解析、`semantic_preservation_pass=true`；任何未审计或审计失败项不得进入主 eligibility。
6. semantic preservation audit 是 source-level raw-vs-normalized signature audit，不是定理级严格语义等价证明；文档和论文写作应使用“source-signature-preserving / 结构签名保持”这类措辞。
7. LLMS-EMP cross-LLM claim gate 必须计算：每个 LLM `eligible_after >= 5` 且 max/min ratio <= 2 才允许谨慎 aggregate claim；否则只能写 coverage audit 或 negative finding。
8. recovered vs naturally-converted profile comparison 必须至少覆盖状态数、迁移数、层级、transition label 长度、alias 数和 semantic risk 分布。
9. 高基数候选 `.puml` 与官方 `.scxml` 必须归档到 [artifacts/plantuml_recovery/r3_1_committed/](./artifacts/plantuml_recovery/r3_1_committed/) 的 `workdir.zip`；解压态 `workdir/` 和根目录 `runs/` 散文件不得提交。
