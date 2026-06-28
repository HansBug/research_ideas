# R3 转换工具链调研与 preflight 记录

本文件服务 PR-R3 converter v0。调研结论只用于四例 smoke 输入的转换 / 裁决，不把任何工具链写成本论文主贡献，也不把 R3 结果写成 R7/R8 正式实验级转换能力。

## 1. 调研与实现原则

1. 优先官方文档、官方仓库、官方 CLI / release 与本地可执行验证。
2. Python 只作为 orchestrator；Java / Node / Rust / GUI-first 工具均可作为候选。
3. converter 运行顺序必须是：**官方/成熟工具链 preflight -> 官方结构化导出 -> 以结构化导出作为 canonical 主转换路径 -> targeted audit -> loss ledger**。
4. 缺 PlantUML / Umple / Java runtime 或显式 jar 路径无效时必须 loudly fail，并给出下载、环境变量和复验命令；不得复用 committed SCXML，不得静默 fallback 到 regex/string parser。
5. R3 不承诺通用 PlantUML / Umple / TTool 转换器；当前四例 selected smoke 不包含 TTool，四例内的 canonical element 来源必须可回指官方 SCXML。

## 2. 工具链表

| format | candidate_tool | source_url | source_type | language | install_or_access | cli_available | ast_or_export_available | selected_for_r3 | reason | risk | verification_command | last_verified_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PlantUML state diagram | PlantUML CLI / jar | <https://plantuml.com/command-line>; <https://plantuml.com/download>; <https://github.com/plantuml/plantuml/releases> | 官方文档 / release | Java/JVM | `plantuml` 或 `java -jar plantuml.jar ...`；本机使用外部本地 jar，不入库；缺工具时直接失败 | 是 | state diagram 可导出 SCXML；XMI 主要用于 class diagram；未找到官方文档化 AST | 是（真实 preflight + SCXML canonical 主路径） | PlantUML 是当前三个 smoke 样例的一手 `STM_0` 格式；官方 CLI 先做 syntax / SCXML preflight，R3 解析 SCXML 作为 canonical 主来源。 | PlantUML 语义宽、宏和皮肤语法多；`llms-emp-deepseek-microwave` 的 raw `.puml` 被官方 preflight 判为需要 pre-SCXML normalization，因此当前只通过 R3.1 deterministic normalization replay 后重新运行官方 `-tscxml` 取得 canonical，且该 conversion gain 不得计入 repair gain。 | `java -jar plantuml.jar -checkonly selected_seed_examples/<id>/stm0.puml`; `java -jar plantuml.jar -tscxml selected_seed_examples/<id>/stm0.puml` | 2026-06-24 19:30:00 |
| Umple textual state machine | Umple compiler / CLI | <https://cruise.umple.org/umple/UmpleTools.html>; <https://cruise.umple.org/umpleonline/scripts/umple.jar>; <https://github.com/umple/umple> | 官方手册 / 官方 jar / repo | Java/JVM | `java -jar umple.jar ...`；本机用临时 `UMPLE_JAR`，jar 不入库；缺工具时直接失败 | 是 | 官方 generator 包含 `Json / FeatureModelJson / Scxml / Ecore / Xmi / StateTables`；未找到单独 AST export | 是（真实 preflight + SCXML canonical 主路径 + targeted timing audit） | `sefm-ssc7-umple` 是 Umple 一手格式；官方 compiler 先做 `-g Nothing` syntax/compile preflight，再导出 SCXML 作为 canonical 主来源。 | 官方 SCXML 文件开头标注 experimental；且会把 `after(60)` 改写为 `timeoutTimeoutToReady`，不适合直接作为 loss attribution 的唯一真源。 | `java -jar umple.jar -g Nothing selected_seed_examples/<id>/stm0.ump`; `java -jar umple.jar -g Scxml selected_seed_examples/<id>/stm0.ump` | 2026-06-24 19:30:00 |
| TTool / AVATAR XML | TTool / AVATAR modeling tool | <https://ttool.telecom-paris.fr/avatar.html>; <https://ttool.telecom-paris.fr/installation_configuration.html>; <https://ttool.telecom-paris.fr/ttoolai.html>; <https://gitlab.telecom-paris.fr/mbe-tools/TTool> | 官方主页 / 配置文档 / TTool-AI / 官方 GitLab | Java / GUI-first | 官方源码可构建；文档出现 `ttool-cli.jar -mcp/-mcpcodex` 等入口 | 部分是 | 官方 XML model artifact 可用；未找到官方文档化 AVATAR SMD -> SCXML/JSON/AST 批处理导出 | 否（当前四例 smoke 已移除；未来补充 adapter） | `ttool-automatedbraking-xml` 曾作为 XML/SMD 切片压力源；当前已从四例 selected smoke 移除，只保留在 seed registry / evidence 中作为未来 TTool XML 专项线索。 | GUI-centric；XML 包含 block diagram、signals、timing 和多个 SMD panel，v0 不解析 graphical connecting point 到精确 source/target，也不切出纯 T0 STM。 | 若未来恢复，只能先做 Python `xml.etree.ElementTree` well-formed check 与官方 headless structured export 调研；当前不进入四例 report。 | 2026-06-24 19:30:00 |
| FCSTM DSL | pyfcstm | <https://github.com/HansBug/pyfcstm> / <https://pypi.org/project/pyfcstm/0.4.0/> | 本地 submodule + 官方仓库/PyPI | Python | `git submodule update --init --recursive`; `pip install -e ./pyfcstm` | 是 | `python -m pyfcstm` 提供 parse / plantuml / simulate 等 project-level 能力 | 是（下游消费者候选，不作为 R3 唯一输出） | pyfcstm 是本仓库最可控的结构化诊断 / 执行生态，可作为 R4/R5 后续消费者线索。 | FCSTM 是本仓库生态，不是外部通用 UML 标准；R3 canonical schema 不等同于 pyfcstm DSL。 | `git submodule status --recursive | grep pyfcstm`; `python -m pyfcstm --version`; `python -m pyfcstm --help` | 2026-06-24 17:26:35 |

## 3. R3 四例 preflight 裁决

| example_id | 格式 | 官方/成熟工具 preflight | 结构化导出证据 | R3 canonical 策略 | status |
|---|---|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | PlantUML `-checkonly` 成功 | [reports/toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml](./reports/toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml) | 解析官方 SCXML 作为 canonical 主来源；不使用源文本解析。 | `converted` |
| `llms-emp-kimi-autonomous-collision` | PlantUML | PlantUML `-checkonly` 成功 | [reports/toolchain_exports/llms-emp-kimi-autonomous-collision/stm0.scxml](./reports/toolchain_exports/llms-emp-kimi-autonomous-collision/stm0.scxml) | 新加入较高难度 Kimi 自动驾驶 / 碰撞规避 PlantUML；解析官方 SCXML 作为 canonical 主来源。 | `converted` |
| `sefm-ssc7-umple` | Umple | Umple `-g Nothing` 成功 | [reports/toolchain_exports/sefm-ssc7-umple/stm0.scxml](./reports/toolchain_exports/sefm-ssc7-umple/stm0.scxml) | 解析官方 SCXML 作为 canonical 主来源；原始 `.ump` 仅用于 `after(60)` targeted timing loss audit，记录为 `targeted_audit_used`，不是 fallback。 | `partial` |
| `llms-emp-deepseek-microwave` | PlantUML | raw PlantUML 依赖 R3.1 normalized candidate replay；replay 后 `-checkonly` / `-tscxml` 成功 | [reports/toolchain_exports/llms-emp-deepseek-microwave/stm0.r3_1_normalized.scxml](./reports/toolchain_exports/llms-emp-deepseek-microwave/stm0.r3_1_normalized.scxml) | raw `stm0.puml` 不覆盖；只消费 R3.1 语义保持审计通过后的 normalized candidate 所导出的官方 SCXML；不使用 source-text parser。 | `converted` |

## 4. 本机复验摘要

```bash
java -version
# java version "1.8.0_202"

git submodule status --recursive | grep pyfcstm
# 5f811a0f71a4b35bac544d7896ba0acb401ade7f pyfcstm (v0.4.0)

python -m pyfcstm --version
# Pyfcstm, version 0.4.0.

python -m pyfcstm --help
# Commands include generate / plantuml / simulate / visualize.
```

PlantUML 复验依赖本机外部 `plantuml.jar` 或 `plantuml` 命令；Umple 复验依赖临时设置 `UMPLE_JAR=/path/to/umple.jar`。第三方 jar 不提交入库，report 只保留版本、命令、官方来源、结构化导出证据和 failure reason。

## 5. microwave raw `STM_0` 与 R3.1 replay

当前四例中的 `llms-emp-deepseek-microwave` 是 R3.1 pre-SCXML normalization replay 覆盖样例。该样例的一手 raw 输入必须保留在 [../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml](../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml)，不得用 normalized candidate 覆盖。R3 从 [reports/plantuml_recovery_report.json](./reports/plantuml_recovery_report.json) 与 [artifacts/plantuml_recovery/r3_1_committed/workdir.zip](./artifacts/plantuml_recovery/r3_1_committed/workdir.zip) 读取已通过审计的 normalized candidate，再重新调用本地配置的 PlantUML `-tscxml` 生成 [reports/toolchain_exports/llms-emp-deepseek-microwave/stm0.r3_1_normalized.scxml](./reports/toolchain_exports/llms-emp-deepseek-microwave/stm0.r3_1_normalized.scxml)。R3 canonical 只来自该 official SCXML；不使用 source-text parser，也不把 normalization / conversion gain 计入 repair gain。

历史同源候选探测报告 [reports/unified_uml_plantuml_candidate_probe.json](./reports/unified_uml_plantuml_candidate_probe.json) 仍保留为只读背景：它探测 `assets/extracted/pairs.jsonl` 前 80 条 PlantUML，其中 40 条通过 `-checkonly` 且产生 SCXML。`unified-uml-synthetic-0000` 现在只作为历史 / registry 线索，不属于当前四例 smoke，不应出现在 R4/R4.5 当前四例统计中。
