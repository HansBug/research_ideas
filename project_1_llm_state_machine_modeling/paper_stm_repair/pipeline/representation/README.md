# R4.5 规范化 STM 到 fcstm 表示桥

> **LLMS-EMP 60 例 active 路线**：Issue #161 后，PlantUML 不再走 `SCXML -> legacy canonical -> lowering.py`。active 路径是 [Java source frontend](../conversion/java/plantuml-state-frontend/README.md) -> `plantuml_source_lowering.py` -> [60 例证据目录](./reports/llms_emp_r45_java_60/SUMMARY.md)。下文四例 R3 smoke 仍保留为历史合同，不得与新 60 例统计混用。

## 1. 定位

`representation/` 是第一篇论文 R4.5 的内部表示桥工作区，负责把 R3 的 `canonical_stm.json` 降到 pyfcstm 可解析的 `.fcstm` DSL，并同步产出 `name_mapping.json`、`lowering_inventory.json`、`fcstm_export_loss_ledger.jsonl` 与 `parse_inspect_report.json`。

它的角色是：

```text
R3 规范化 STM JSON -> R4.5 .fcstm / pyfcstm inspect report -> R5 确定性 smoke
```

R4.5 不是论文主贡献，不调用 LLM，不读取 `.env`，不生成 `STM_k`，也不执行修正循环。所有 lowering / loss / approximation 都归入 representation / conversion attribution，不能计入 source-level repair gain、issue closure 或方法效果。当前 [../../selected_seed_examples/](../../selected_seed_examples/) 是 smoke 迷你文库，不是最终实验集合。

## 2. 路径结构

```text
representation/
├── README.md
├── schemas/
│   ├── fcstm_export_report.schema.json
│   ├── fcstm_export_loss_ledger.schema.json
│   ├── lowering_inventory.schema.json
│   └── name_mapping.schema.json
├── src/paper_stm_repair_representation/
│   ├── __init__.py
│   ├── cli.py
│   ├── lowering.py              # 历史四例 canonical lowering / .fcstm render / report 入口
│   ├── plantuml_source_lowering.py # active 60 例的结构保真 lowering 与三轴裁决
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

新路线的 Python 层不解析 PlantUML，只校验 jar、调用 Java、读取 JSON、执行 FCSTM lowering 与 pyfcstm parse/inspect/runtime 验证。当前边界是结构与 raw text 可追溯，不把 opaque label 自动拆成 guard/effect/timing。只有 source fact 无法完整落入 `.fcstm + mandatory trace` 时才产生 structural blocker；可以完整保存、但无法证明运行解释的 composite entry、fan-out、concurrency、state body 或 lifecycle owner 记为 operational debt，并使 `fcstm_execution_eligible=false`、`discover_eligible=false`。因此 `structure_preserved` 不能被解释为行为等价。

其中 `lowering.py` 继续承担历史四例 R3 canonical 的 model view、lowering、`.fcstm` 渲染、loss ledger 与 export report；Issue #161 后的 active 60 例由 `plantuml_source_lowering.py` 和 `plantuml_source_audit.py` 承担结构投影与独立 AST 审计。两条统计不得混用，本 PR 未单独拆出 `canonical_to_fcstm.py`。

## 3. 运行方式

依赖仓库根目录已有 Python 环境和 `pyfcstm` submodule。active 60 例证据固定 pyfcstm commit `4ea23c9b153f47e5c4a2125d95b466eee6eed13e`；下文历史四例最初冻结于 `v0.4.0`，仅保留为 legacy contract。任何 gitlink 升级都必须复跑本目录测试并检查 committed reports 是否发生命名/inspect 漂移。新环境应先在仓库根目录执行：

```bash
git submodule update --init --recursive
pip install -r requirements.txt
pip install -e ./pyfcstm
```

重放 active 60 例时，不得覆盖已经绑定人工审阅的冻结目录。应显式使用新的 replay 目录：

```bash
make -C project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/java/plantuml-state-frontend fetch compile

PYTHONPATH=pyfcstm:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tools/run_llms_emp_r45.py \
  --output-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60_replay
```

若默认输出目录已存在 `MANUAL_REVIEW.md`，runner 必须拒绝覆盖。新 replay 只有在重新完成 60 对人工阅读并绑定新哈希后，才能替换冻结证据；机器 parse/inspect/AST audit 不能自动继承旧人工 PASS。

冻结证据完成后，可重新生成面向 GitHub 人工浏览的 60 个 NL/PlantUML/FCSTM 三元组目录：

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tools/build_llms_emp_pair_pages.py
```

入口为 [reports/llms_emp_r45_java_60/PAIR_INDEX.md](./reports/llms_emp_r45_java_60/PAIR_INDEX.md)。每个目录包含 `nl.txt`、`plantuml.puml`、`fcstm.fcstm` 和三合一 `README.md`；生成器会先校验 NL、PlantUML、FCSTM 与 comparison hash，不允许把漂移后的文本写成既有人工结论。

导出四个 selected seed examples：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
python -m paper_stm_repair_representation.cli export-selected
```

预期摘要：

```json
{"examples": 4, "converted": 4, "partial": 0, "blocked": 0}
```

R4.5 report item 和每个样例的 `lowering_inventory.json.source_traceability` 都已包含 `source_nl_path`、`source_stm0_path`、`source_meta_path`、`canonical_output_path`，用于把 `.fcstm` 输出追溯回 selected 冒烟输入与 R3 canonical。也就是说，R4.5 阶段 report 自身就能直接定位上游 NL、原始 `STM_0` 文件、`source_meta.json` 与 R3 规范化 JSON。当前四例固定为 `llms-emp-deepseek-microwave`、`llms-emp-gpt4o-hldcs`、`llms-emp-kimi-autonomous-collision`、`sefm-ssc7-umple`。

运行 R4.5 tests：

```bash
PYTHONPATH=pyfcstm:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
python -m pytest -q project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests
```

## 4. R5.7.4 裁决样例补充 bundle 已归档

R5.7.4 / R5.7.5 为 Better STM static adjudication 与 constructed `STM_k` dry-run 物化过两类补充表示资产：`r5_7_4_adjudication_fcstm_exports/` 和 `r5_7_4_adjudication_baseline_bundles/`。这些资产只服务旧 Better STM 裁决链，不属于当前 active representation contract，已迁入 cold archive：

- [../../archive/r5_7_better_stm_snapshot/pipeline/representation/reports/r5_7_4_adjudication_fcstm_exports/](../../archive/r5_7_better_stm_snapshot/pipeline/representation/reports/r5_7_4_adjudication_fcstm_exports/)
- [../../archive/r5_7_better_stm_snapshot/pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/](../../archive/r5_7_better_stm_snapshot/pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/)

后续若需要 `0001` / `0018` 的 standalone baseline `.fcstm` 作为 source-level pilot 输入，必须在新的 issue lifecycle PR 中重新登记其 source trace、scope 与 attribution；不得直接恢复旧 Better STM / adjudication / constructed `STM_k` 语义。

## 5. 当前四例输出

R4.5 的人类可读报告也必须能直接回到上游输入：下表中的 `上游 NL` 与 `原始 STM_0` 链接对应 `fcstm_export_report.json` item 里的 `source_nl_path` / `source_stm0_path`，不是二手 parquet 或转换后中间产物。

| example_id | 上游 NL | 原始 STM_0 | R4.5 状态 | 输出 |
|---|---|---|---|---|
| `llms-emp-deepseek-microwave` | [nl.txt](../../selected_seed_examples/llms-emp-deepseek-microwave/nl.txt) | [stm0.puml](../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml) | `converted` | R4.5 消费 R3.1 pre-SCXML normalization replay 后得到的 canonical，输出 [model.fcstm](./reports/fcstm_exports/llms-emp-deepseek-microwave/model.fcstm)；raw `stm0.puml` 不覆盖，normalization / 表示转换收益不计入修正收益。 |
| `llms-emp-gpt4o-hldcs` | [nl.txt](../../selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt) | [stm0.puml](../../selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml) | `converted` | 保留 HSM 层次，输出 [model.fcstm](./reports/fcstm_exports/llms-emp-gpt4o-hldcs/model.fcstm) 与 inspect report。 |
| `llms-emp-kimi-autonomous-collision` | [nl.txt](../../selected_seed_examples/llms-emp-kimi-autonomous-collision/nl.txt) | [stm0.puml](../../selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml) | `converted` | Kimi 自动驾驶 / 碰撞规避 EMPirical 样例替代 TTool 进入当前 selected smoke，输出 [model.fcstm](./reports/fcstm_exports/llms-emp-kimi-autonomous-collision/model.fcstm) 与 inspect report。 |
| `sefm-ssc7-umple` | [nl.txt](../../selected_seed_examples/sefm-ssc7-umple/nl.txt) | [stm0.ump](../../selected_seed_examples/sefm-ssc7-umple/stm0.ump) | `converted` | event+guard 通过 pseudo relay，bool guard 降为 int guard，action 降为 flag；R3 timing loss 继续只作 caveat，输出 [model.fcstm](./reports/fcstm_exports/sefm-ssc7-umple/model.fcstm)。 |

## 6. 维护纪律

### 6.1 审计主账

`lowering_inventory.json` 是 R4.5 的审计主账，不只是 guard/action 清单。每个样例至少要覆盖事件、guard、action、引用端点、初始/终止推导、timing、层次结构和 `source_traceability`。其中 `source_traceability` 必须包含 `source_nl_path`、`source_stm0_path`、`source_meta_path`、`canonical_output_path`、上游 R3 状态与 R3.1 replay 标记，便于从 `.fcstm` 回到 选定输入、原始 `STM_0` 与 R3 canonical。

### 6.2 命名纪律

- 单段 raw text 使用 `pyfcstm.utils.to_identifier(raw_text, strict_mode=True, keyword_safe_for=["python", "java"])`。
- 多段合成名使用 `pyfcstm.utils.sequence_safe([...])` 后再过 `to_identifier(...)`，不要手写正则 sanitizer。
- FCSTM lexer 中 `event`、`continue`、`E`、`if` 等保留词 / 特殊 token 不能直接作为 emitted identifier；如需调整，必须在 `name_mapping.json` 中记录。
- 所有 emitted identifiers 都必须进入 `name_mapping.json`：root / wrapper state、state、event、pseudo relay、guard variable、action flag、abstract action。
- state / pseudo state 在 DSL 中用 `named` 保留 raw label；event 在当前四例中也用 `named` 保留 raw label。

### 6.3 关键语义策略

1. **命名**：主路径使用 `pyfcstm.utils.to_identifier(..., strict_mode=True, keyword_safe_for=["python", "java"])` 与 `pyfcstm.utils.sequence_safe([...])`，不手写 regex sanitizer。
2. **原名保真**：state / pseudo state 使用 `named` 保留 raw label；event 在当前四例中也使用 `named`。若未来某个 event 合法化后仍与 pyfcstm lexer 特殊 token 冲突，`name_mapping.json` 必须继续作为 raw event 的事实源，不允许丢失原名。
3. **event+guard**：pyfcstm 不允许同一 transition 同时出现 event 与 guard；R4.5 必须通过 pseudo relay 降低为 `source -> relay : Event; relay -> target : if [guard];`。
4. **层次**：默认保留 hierarchy，不 flatten。跨层级 transition 只在可审计的 boundary lifting / forced transition 模式下降低，并写入 loss ledger。
5. **timing**：`after(60)` 等时间语义不恢复 clock，只使用 R3 SCXML 中已有 timeout event，并记录 timing lowering / loss。
6. **raw 与 attribution honesty**：`llms-emp-deepseek-microwave` 的可导出性来自 R3.1 pre-SCXML normalization replay；R4.5 只消费其 canonical，不覆盖 raw `stm0.puml`，也不把 normalization / representation 可解析性计入修正收益。TTool XML 与 `unified-uml-synthetic-0000` 不在当前四例冒烟中，只能作为历史 / 未来补充 adapter / registry 线索。

## 7. 运行与验收

每次修改 exporter 后运行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
python -m paper_stm_repair_representation.cli export-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
pytest -q project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests
```

验收重点：四例 parse/inspect 均为 `ok`；summary 为 `{"examples": 4, "converted": 4, "partial": 0, "blocked": 0}`；`llms-emp-deepseek-microwave` 必须追溯到 R3.1 pre-SCXML normalization replay；`repair_contribution_allowed` 始终为 `false`；TTool XML 与 `unified-uml-synthetic-0000` 不混入当前四例。

## 8. 与上下游关系

- 上游 R3：[../conversion/README.md](../conversion/README.md) 提供规范化 JSON、conversion report 与 loss ledger。
- 历史 R4/R5.7 evaluation：[../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/](../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/) 已冷归档；active [../evaluation/README.md](../evaluation/README.md) 只是 future source-level closure / regression placeholder。
- 下游 R5 只消费 R4.5 已提交 `.fcstm` / report，不应在 R5 再补写 exporter。

## 9. 学术注意点

- `.fcstm` 是内部可机检载体，论文中只能弱化为 implementation representation，不进标题、摘要或贡献列表。
- R4.5 只降低 R3 canonical 已承载的语义；例如 SEFM raw Umple 中若存在 entry action 但 R3 canonical 未证明/未保留，R4.5 不从 raw source 私自补回，只能在上游 conversion caveat 中解释。
- `fcstm_export_loss_ledger.jsonl` 中所有 `repair_contribution_allowed=false`；任何表示转换带来的可解析性改善都不能算作修正循环改进。
- R5/R6/R7 引用 R4.5 输出时，应同时读取 `lowering_inventory.json` 和 loss ledger，避免把 representation approximation 当作 STM 语义真实变化。
- `.fcstm` export / lowering 是 intermediate executable semantic medium，不是 source-level closure gate，也不能计入 repair gain。
