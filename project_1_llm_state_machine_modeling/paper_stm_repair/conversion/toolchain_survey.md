# R3 转换工具链调研与 preflight 记录

本文件服务 PR-R3 converter v0。调研结论只用于四例 smoke 输入的转换 / 裁决，不把任何工具链写成本论文主贡献，也不把 R3 结果写成 R7/R8 正式实验级转换能力。

## 1. 调研与实现原则

1. 优先官方文档、官方仓库、官方 CLI / release 与本地可执行验证。
2. Python 只作为 orchestrator；Java / Node / Rust / GUI-first 工具均可作为候选。
3. converter 运行顺序必须是：**官方/成熟工具链 preflight -> 结构化导出证据保留 -> 必要时最小 parser / XML inventory fallback -> loss ledger**。
4. 如果 fallback 到最小 parser，必须说明官方 / 成熟工具为何不足以直接提供稳定 canonical STM，并记录命令、状态、导出证据或失败原因。
5. R3 fallback parser 只覆盖 [selected_seed_examples/](../selected_seed_examples/) 四例，不承诺通用 PlantUML / Umple / TTool 转换器。

## 2. 工具链表

| format | candidate_tool | source_url | source_type | language | install_or_access | cli_available | ast_or_export_available | selected_for_r3 | reason | risk | verification_command | last_verified_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PlantUML state diagram | PlantUML CLI / jar | <https://plantuml.com/command-line>; <https://plantuml.com/download>; <https://github.com/plantuml/plantuml/releases> | 官方文档 / release | Java/JVM | `plantuml` 或 `java -jar plantuml.jar ...`；本机使用外部本地 jar，不入库 | 是 | state diagram 可导出 SCXML；XMI 主要用于 class diagram；未找到官方文档化 AST | 是（真实 preflight + SCXML evidence + fallback parser） | PlantUML 是两个 smoke 样例的一手 `STM_0` 格式；官方 CLI 先做 syntax / SCXML preflight，R3 minimal parser 仅作为 canonical 抽取 fallback / crosscheck。 | PlantUML 语义宽、宏和皮肤语法多；`unified-uml-synthetic-0000` 被官方 `-checkonly` 判为 syntax failed，因此 R3 降为 `partial`。 | `java -jar plantuml.jar -checkonly selected_seed_examples/<id>/stm0.puml`; `java -jar plantuml.jar -tscxml selected_seed_examples/<id>/stm0.puml` | 2026-06-24 19:30:00 |
| Umple textual state machine | Umple compiler / CLI | <https://cruise.umple.org/umple/UmpleTools.html>; <https://cruise.umple.org/umpleonline/scripts/umple.jar>; <https://github.com/umple/umple> | 官方手册 / 官方 jar / repo | Java/JVM | `java -jar umple.jar ...`；本机用临时 `UMPLE_JAR`，jar 不入库 | 是 | 官方 generator 包含 `Json / FeatureModelJson / Scxml / Ecore / Xmi / StateTables`；未找到单独 AST export | 是（真实 preflight + SCXML evidence + fallback parser） | `sefm-ssc7-umple` 是 Umple 一手格式；官方 compiler 先做 `-g Nothing` syntax/compile preflight，再导出 SCXML 作为 evidence。 | 官方 SCXML 文件开头标注 experimental；且会把 `after(60)` 改写为 `timeoutTimeoutToReady`，不适合直接作为 loss attribution 的唯一真源。 | `java -jar umple.jar -g Nothing selected_seed_examples/<id>/stm0.ump`; `java -jar umple.jar -g Scxml selected_seed_examples/<id>/stm0.ump` | 2026-06-24 19:30:00 |
| TTool / AVATAR XML | TTool / AVATAR modeling tool | <https://ttool.telecom-paris.fr/avatar.html>; <https://ttool.telecom-paris.fr/installation_configuration.html>; <https://ttool.telecom-paris.fr/ttoolai.html>; <https://gitlab.telecom-paris.fr/mbe-tools/TTool> | 官方主页 / 配置文档 / TTool-AI / 官方 GitLab | Java / GUI-first | 官方源码可构建；文档出现 `ttool-cli.jar -mcp/-mcpcodex` 等入口 | 部分是 | 官方 XML model artifact 可用；未找到官方文档化 AVATAR SMD -> SCXML/JSON/AST 批处理导出 | 是（XML well-formed + inventory adapter） | `ttool-automatedbraking-xml` 是完整 TTool/SysML/AVATAR XML 工件；R3 至少定位 AVATAR SMD panel、state/start component、transition connector 并诚实标 `partial`。 | GUI-centric；XML 包含 block diagram、signals、timing 和多个 SMD panel，v0 不解析 graphical connecting point 到精确 source/target，也不切出纯 T0 STM。 | Python `xml.etree.ElementTree` well-formed check；官方 headless structured export 暂无 R3 证据 | 2026-06-24 19:30:00 |
| FCSTM DSL | pyfcstm | <https://github.com/HansBug/pyfcstm> / <https://pypi.org/project/pyfcstm/0.4.0/> | 本地 submodule + 官方仓库/PyPI | Python | `git submodule update --init --recursive`; `pip install -e ./pyfcstm` | 是 | `python -m pyfcstm` 提供 parse / plantuml / simulate 等 project-level 能力 | 是（下游消费者候选，不作为 R3 唯一输出） | pyfcstm 是本仓库最可控的结构化诊断 / 执行生态，可作为 R4/R5 后续消费者线索。 | FCSTM 是本仓库生态，不是外部通用 UML 标准；R3 canonical schema 不等同于 pyfcstm DSL。 | `git submodule status --recursive | grep pyfcstm`; `python -m pyfcstm --version`; `python -m pyfcstm --help` | 2026-06-24 17:26:35 |

## 3. R3 四例 preflight 裁决

| example_id | 格式 | 官方/成熟工具 preflight | 结构化导出证据 | R3 canonical 策略 | status |
|---|---|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | PlantUML `-checkonly` 成功 | [reports/toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml](./reports/toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml) | 保留 SCXML 作 crosscheck；canonical 仍用 minimal parser 以保留 raw label / body line 审计信息。 | `converted` |
| `unified-uml-synthetic-0000` | PlantUML | PlantUML `-checkonly` 失败 | 无可信 SCXML | minimal parser 只保留 smoke/debug 抽取；写 `R3.TOOLCHAIN.OFFICIAL_SYNTAX_FAILED` 与 tooling loss，不得作为 experiment-grade conversion。 | `partial` |
| `sefm-ssc7-umple` | Umple | Umple `-g Nothing` 成功 | [reports/toolchain_exports/sefm-ssc7-umple/stm0.scxml](./reports/toolchain_exports/sefm-ssc7-umple/stm0.scxml) | 保留官方 SCXML 作 crosscheck；因 SCXML experimental 且改写 `after(60)`，canonical 仍用 minimal parser 保留 timing loss attribution。 | `partial` |
| `ttool-automatedbraking-xml` | TTool XML | 官方 XML artifact 可 well-formed 解析；未找到稳定 headless structured export | 原始 [../selected_seed_examples/ttool-automatedbraking-xml/stm0.xml](../selected_seed_examples/ttool-automatedbraking-xml/stm0.xml) | 只做 AVATAR SMD XML inventory；resolved state/transition counts 保持 0。 | `partial` |

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

PlantUML 复验依赖本机外部 `plantuml.jar` 或 `plantuml` 命令；Umple 复验依赖临时设置 `UMPLE_JAR=/path/to/umple.jar`。第三方 jar 不提交入库，report 只保留版本、命令、官方来源、结构化导出证据和 fallback reason。
