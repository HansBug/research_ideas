# R3 转换合同与转换器 v0

本目录是第一篇论文 `paper_stm_repair` 的 R3 转换层：把 [selected_seed_examples/](../../selected_seed_examples/) 中四个静态 `<NL, STM_0>` 冒烟样例转换、部分转换或阻塞裁决到 R3 规范化 STM JSON，并生成 conversion report 与 loss ledger。

## 1. 定位

- R3 是 **开发 / 审计级最小转换链路 v0**，只服务四例冒烟集合、R4/R4.5/R5 dry-run 与 schema/ledger 接口验证。
- [selected_seed_examples/](../../selected_seed_examples/) 是 smoke 迷你文库，不是最终实验集合、样本上限或论文主结果集合。
- R3 不是通用 UML / SysML / PlantUML / Umple / TTool 转换器；TTool XML 已从当前四例 selected smoke 中移除，只保留为未来 / 补充 adapter 方向。
- R3 committed report 只是 reviewer 固化样例 / contract evidence，不是 R7/R8 experiment-grade conversion，也不是主实验结果。
- 转换收益、人工规范化和后续修正循环收益必须分离；loss ledger 中所有 `repair_contribution_allowed` 均为 `false`。

## 2. 路径结构

```text
conversion/
├── README.md
├── TOOLCHAINS.md
├── schemas/
│   ├── canonical_stm.schema.json
│   ├── conversion_report.schema.json
│   ├── loss_ledger.schema.json
│   ├── normalization_ledger.schema.json
│   └── recovery_report.schema.json
├── artifacts/
│   └── plantuml_recovery/r3_1_committed/
│       ├── README.md
│       ├── manifest.json
│       ├── workdir.zip
│       └── workdir.zip.sha256
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

## 3. 工作方式

R3 的转换链路是“Python 编排器 + 外部成熟工具链 + 结构化 XML/SCXML adapter”，不是手写 PlantUML/Umple 文本 parser：

1. `cli.py` 先校验四例 `nl.txt`、`stm0.*` 与 `source_meta.json` 的 SHA-256。
2. `toolchain.py` 对不同格式执行真实 preflight：
   - PlantUML：运行 `plantuml` 或 `java -jar plantuml.jar`，先 `-checkonly`，再 `-tscxml`。
   - Umple：运行 `java -jar umple.jar`，先 `-g Nothing`，再 `-g Scxml`。
   - TTool XML：当前不在四例 selected smoke 中；未来 / 补充 adapter 若重新启用，仍必须检查一手 XML artifact，且不得宣称已有稳定 headless SMD -> SCXML/JSON/AST 导出。
3. adapter 只消费官方结构化产物：PlantUML / Umple 解析 `reports/toolchain_exports/` 里的 SCXML；TTool 若作为未来补充 adapter 进入，只能从一手 XML 或官方结构化导出取证。
4. 若工具缺失、工具不可执行、官方 syntax fail 或 SCXML export fail：
   - 缺工具 / Java runtime / jar 路径错误：命令 **显式失败**，错误信息会给出下载与配置建议。
   - 官方 syntax/export 失败：该样例只可标 `partial/blocked`，不得生成规范化 JSON。
   - R3 不复用 committed SCXML，不做 source-text parser 回退，不用正则/字符串从 `.puml` / `.ump` 重建 states/transitions。
   - conversion report 会保留官方命令、return code、stderr/stdout tail、structured export status 与 no-fallback 裁决，方便 reviewer 复核失败不是被静默吞掉。
5. 成功或部分成功后生成规范化 STM JSON、conversion report、loss ledger 和 markdown summary。

## 4. 运行环境与依赖配置

### 4.1 Python 依赖

在仓库根目录使用已有环境安装依赖：

```bash
pip install -r requirements.txt
```

运行 R3 CLI：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_conversion.cli convert-selected
```

### 4.2 Java / PlantUML / Umple

R3 需要真实外部工具链。缺少这些工具时会直接失败并给出操作建议，不会静默退回 committed 固化样例或文本解析。

| 工具 | 何时需要 | 配置方式 | 复验命令 |
|---|---|---|---|
| Java runtime | PlantUML jar / Umple jar | 安装 JRE/JDK，确保 `java -version` 可用 | `java -version` |
| PlantUML | 转换 `.puml` 冒烟样例 | 推荐 `export PLANTUML_JAR=/abs/path/to/plantuml.jar`；或安装 PATH 中的 `plantuml`；或放到 `tools/plantuml.jar` | `java -jar $PLANTUML_JAR -version`；`java -jar $PLANTUML_JAR -checkonly project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml`；`java -jar $PLANTUML_JAR -tscxml .../stm0.puml` |
| Umple | 转换 `.ump` 冒烟样例 | 推荐 `export UMPLE_JAR=/abs/path/to/umple.jar`；或放到 `tools/umple.jar` | `java -jar $UMPLE_JAR --version`；`java -jar $UMPLE_JAR -g Nothing project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/sefm-ssc7-umple/stm0.ump`；`java -jar $UMPLE_JAR -g Scxml .../stm0.ump` |

官方下载入口：

- PlantUML：<https://plantuml.com/download> / <https://github.com/plantuml/plantuml/releases>
- Umple：<https://cruise.umple.org/umpleonline/scripts/umple.jar> / <https://cruise.umple.org/umple/UmpleTools.html>

本仓库不提交第三方大型 jar；report 只保留工具名称、版本、命令、官方来源、结构化导出 hash/path 与失败原因。

### 4.3 缺工具时的预期错误

如果未配置 PlantUML，CLI 会类似这样失败：

```text
R3 conversion toolchain setup failed for llms-emp-gpt4o-hldcs:
R3 PlantUML 转换需要真实运行 PlantUML 官方工具链，但当前既没有 `plantuml` 命令，也没有可用 plantuml.jar。
R3 不允许在官方工具链缺失、不可执行、syntax check 失败或结构化导出失败时，静默退回 regex/string/source-text parser，也不允许复用已提交 SCXML 固化样例冒充本次转换证据。
请按下面步骤配置后重试。
... PLANTUML_JAR ...
```

如果设置了 `PLANTUML_JAR` / `UMPLE_JAR` 但路径不存在，也会直接报出对应环境变量与路径，要求修复后重试。

## 5. 当前四例裁决

| 样例 | 格式 | R3 status | 说明 |
|---|---|---|---|
| `llms-emp-deepseek-microwave` | PlantUML | `converted` | DeepSeek microwave PlantUML raw `STM_0` 依赖 R3.1 pre-SCXML normalization replay 后再走 PlantUML 官方 SCXML；raw `stm0.puml` 不覆盖，normalization / 转换收益 不得计入修正收益。 |
| `llms-emp-gpt4o-hldcs` | PlantUML | `converted` | PlantUML `-tscxml` 成功；canonical states/transitions 来自官方 SCXML。 |
| `llms-emp-kimi-autonomous-collision` | PlantUML | `converted` | Kimi 自动驾驶 / 碰撞规避 PlantUML 样例加入当前 selected smoke；PlantUML `-tscxml` 成功，canonical 来自官方 SCXML。 |
| `sefm-ssc7-umple` | Umple | `partial` | Umple `-g Scxml` 成功；canonical states/transitions 来自官方 SCXML，原始 `.ump` 仅用于 `after(60)` targeted timing loss audit，因此保留 timing loss。 |

## 6. 输出解释

- [reports/selected_seed_examples_conversion_report.json](./reports/selected_seed_examples_conversion_report.json)：四例 conversion report；其中每条 `tool_preflight` 记录官方/成熟工具链命令、版本、syntax status、structured export status、setup hint 与 failure reason；每条 item 还显式记录 `conversion_source`、`canonical_extraction_method`、`structured_export_path`、`fallback_used`、`fallback_scope`。每条 item 还必须显式保留 `source_nl_path`、`source_stm0_path`、`source_meta_path` 与 `canonical_output_path`，让 R3 report 自身可追溯到上游 NL 与原始 `STM_0`。
- [reports/selected_seed_examples_loss_ledger.jsonl](./reports/selected_seed_examples_loss_ledger.jsonl)：所有 loss / 降级 / partial 原因。
- [reports/selected_seed_examples_summary.md](./reports/selected_seed_examples_summary.md)：便于人工浏览的概览。
- [reports/unified_uml_plantuml_candidate_probe.json](./reports/unified_uml_plantuml_candidate_probe.json)：历史上针对 `unified-uml-synthetic-0000` 官方导出失败边界做过同源候选初筛；该 synthetic 样例现在只作为历史 / registry 线索，不属于当前四例冒烟。当前 microwave 样例通过 R3.1 pre-SCXML normalization replay 取得 official SCXML canonical。
- [reports/canonical/](./reports/canonical/)：`converted` / `partial` 样例的 规范化 STM JSON；当前四例均有 canonical 输出，其中 `sefm-ssc7-umple` 仍因 timing loss 标为 `partial`。
- [reports/toolchain_exports/](./reports/toolchain_exports/)：官方工具链能导出的结构化证据，例如 PlantUML / Umple SCXML；PlantUML / Umple 成功样例的 canonical 主结构必须来自这些 SCXML，而不是源文本解析。
- `blocked` / `unsupported` 样例允许 `canonical_output_path` 和 `canonical_output_sha256` 为 `null`；不得生成空 canonical STM 冒充转换成功。

## 7. 与后续阶段关系

- R4 可消费 R3 的 `R3.STATUS.*` 与 `R3.LOSS.*` code，但不得改写 R3 裁决语义。
- R5 应用 deterministic dry-run 检查 R3 输出是否足以支撑诊断 / 场景。
- R7/R8 才冻结正式实验格式范围与 experiment-grade conversion；R3 不提前承担该职责。

## 8. 状态、schema 与官方工具链纪律

### 8.1 状态口径

| status | code | 含义 | canonical output |
|---|---|---|---|
| `converted` | `R3.STATUS.converted` | adapter 可抽取足够 states / transitions，且无影响 R3 消费的已知 loss | 必须存在 |
| `partial` | `R3.STATUS.partial` | 可抽取部分结构，但存在 timing、hierarchy、endpoint、semantic 或 tooling loss | 通常存在，必须配 loss ledger |
| `blocked` | `R3.STATUS.blocked` | 输入或工具链阻塞，无法产出可信 canonical STM | 必须为 `null` |
| `unsupported` | `R3.STATUS.unsupported` | 格式不在 R3 目标范围 | 必须为 `null` |

`R3.LOSS.<loss_type>.<severity>` 是后续评价门和 smoke 的稳定引用入口；下游可以扩展诊断，但不得回写或重定义 R3 状态 / loss 语义。

### 8.2 schema 纪律

conversion report 必须记录 `run_id`、`created_at`、`conversion_command`、`repo_commit`、`schema_version`、`adapter_version`、工具 preflight、source locator、raw locator、`source_nl_path`、`source_stm0_path`、`source_meta_path`、`canonical_output_path`、loss ledger、`manual_edit_allowed=false` 与 eligibility。blocked / unsupported 不得伪造空 canonical 输出。规范化 STM JSON 的 `metadata.conversion_source` 只允许 `official_scxml / official_xml`；`no_canonical_conversion` 只能出现在 conversion report item 中。

### 8.3 官方工具链优先纪律

R3 当前不是“直接手写 parser 即可”的实现。每次转换必须先尝试或记录成熟工具链 preflight，并且 canonical conversion 主路径必须优先消费官方结构化导出：

- PlantUML：必须使用 `plantuml` 或 `plantuml.jar` 做 syntax check，并在可行时导出 SCXML；syntax/export 成功时 canonical 来自 SCXML；若工具缺失则显式失败；若官方 syntax fail，不得凭文本解析标为 `converted`。
- Umple：必须使用 `umple.jar` 做 `-g Nothing` syntax/compile preflight，并在可行时导出 SCXML；canonical 来自 SCXML；原始 `.ump` 仅允许用于 `after(...)` 等 targeted loss audit。
- TTool/AVATAR：当前已从四例 selected smoke 中移除；未来若作为补充 adapter 重新进入，仍只确认 XML artifact 与 ttool-cli/MCP 入口，未找到稳定 headless AVATAR SMD -> SCXML/JSON/AST 导出时不得标为完整转换。

本地若需要复现官方 preflight，可临时设置：

```bash
export PLANTUML_JAR=/path/to/plantuml.jar
export UMPLE_JAR=/path/to/umple.jar
```

本仓库不把大型第三方 jar 作为源码提交；report 中只保留命令、版本、hash/路径 evidence 与官方来源链接。canonical output 只允许 `conversion_source=official_scxml/official_xml`；`no_canonical_conversion` 只能出现在 report item 中，不能写出规范化 JSON。

## 9. 当前四例冒烟与历史 TTool 边界

当前 selected smoke 四例固定为：`llms-emp-deepseek-microwave`、`llms-emp-gpt4o-hldcs`、`llms-emp-kimi-autonomous-collision`、`sefm-ssc7-umple`。它们只是 smoke 迷你文库，用于验证转换、表示桥和评价门接口，不是最终实验集合。

`llms-emp-deepseek-microwave` 的当前 `converted` 依赖 R3.1 pre-SCXML normalization replay：normalization 发生在 PlantUML `-tscxml` 之前，随后仍以官方 SCXML 作为 canonical 来源。必须保留以下边界：

1. [../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml](../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml) 是一手 raw 输入，不得覆盖。
2. normalized candidate / official SCXML 是 run/report artifact，不得回写替换 raw `stm0.puml`。
3. 该例的 conversion / 规范化收益只能归入 conversion attribution，不能计入修正收益、Better STM gain 或模型修复收益。

历史 `ttool-automatedbraking-xml` 与 `unified-uml-synthetic-0000` 已从当前 selected smoke 移除。TTool XML 仍可作为未来 / 补充 adapter 方向，用来研究 SysML / AVATAR XML inventory、connector endpoint、timing fields 等问题；`unified-uml-synthetic-0000` 只保留为 registry / 历史 probe 线索。二者都不应出现在当前 R4/R4.5 四例统计中。

## 10. R3.1 PlantUML pre-SCXML normalization / recovery

R3.1 在本目录下新增 [normalization/](./normalization/) 微型工作区，用于回答 failed PlantUML 样本能否在 **不修改一手 raw assets** 的前提下，通过转换前规范化恢复为 official-toolchain-compatible STM。

关键纪律：

1. normalization 只生成 run/report 路径中的候选 `.puml`，不覆盖 seed library assets、`pairs.jsonl` 或 [selected_seed_examples/](../../selected_seed_examples/)。
2. recovered 判定仍必须来自官方 PlantUML `-checkonly` / `-tscxml` 产物；normalizer 不直接生成 canonical STM。
3. 恢复率必须同时报告 `technical_scxml_pass_all_rules`、`low_risk_scxml_pass`、`main_eligibility_included`；论文主张 只能使用低风险 / 主 eligibility 口径。
4. 高风险 action/guard/hierarchy/concurrency/pseudo-state loss 默认不得进入主 repair eligibility；`fork_join_decl_to_state` 必须标 `concurrency_degraded=true`，endpoint 内嵌 `[*]` 伪状态标记必须作为 supplementary / manual-review。
5. 主 eligibility 还必须通过 source-level semantic preservation audit；该 audit 证明的是 raw-vs-normalized source signature 保持，不是定理级严格语义等价证明。
6. raw / normalized candidate 与官方 SCXML 这类高基数制品必须归档为 `artifacts/plantuml_recovery/r3_1_committed/workdir.zip`，不得提交根目录 `runs/` 下的散文件。

主要输出：

- [normalization/README.md](./normalization/README.md)：工作方式与复验命令。
- [normalization/GUIDE.md](./normalization/GUIDE.md)：规则、ledger 与 eligibility gate 纪律。
- [reports/plantuml_recovery_report.json](./reports/plantuml_recovery_report.json)：R3.1 committed 恢复报告。
- [reports/plantuml_recovery_summary.md](./reports/plantuml_recovery_summary.md)：人工阅读摘要。
- [reports/plantuml_normalization_ledger.jsonl](./reports/plantuml_normalization_ledger.jsonl)：逐变换 ledger。
- [artifacts/README.md](./artifacts/README.md)：conversion workspace 下的长期运行制品入口。
- [artifacts/plantuml_recovery/r3_1_committed/README.md](./artifacts/plantuml_recovery/r3_1_committed/README.md)：全量 raw / normalized `.puml` 与官方 `.scxml` archive 的路径映射、校验和复验说明。
- [artifacts/plantuml_recovery/r3_1_committed/workdir.zip](./artifacts/plantuml_recovery/r3_1_committed/workdir.zip)：高基数运行制品压缩包；PR 中不得提交解压后的几千个散文件。

R3 report 仍是四例转换器 v0 smoke 固化样例；R3.1 report 是 failed PlantUML recovery / eligibility audit。两者事实合流应通过 PR body/comment 或后续合流 commit 处理，避免恢复率形成第二事实真源。

## 11. 测试与验收

R3 最低验收：schema JSON 可由 `jsonschema` 校验；四例均有 conversion report；PlantUML 三例必须有官方 syntax preflight / SCXML evidence；Umple 至少 partial 并记录 timer-like loss；当前四例不得包含 TTool；本地 pytest 通过；缺工具时必须 loud fail 且不能依赖已提交的 SCXML 固化样例。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_conversion.cli convert-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
pytest -q project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tests
```
