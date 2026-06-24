# R3 转换工具链调研

本文件服务 PR-R3 converter v0。调研结论只用于四例 smoke 输入的转换 / 裁决，不把任何工具链写成本论文主贡献，也不把 R3 结果写成 R7/R8 正式实验级转换能力。

## 1. 调研原则

1. 优先官方文档、官方仓库、官方 CLI / release 与本地可执行验证。
2. Python 只作为 orchestrator；Java / Node / Rust / GUI-first 工具均可作为候选。
3. 如果 fallback 到最小 parser，必须说明官方 / 成熟工具为何不足以直接提供稳定 AST 或 headless 切片。
4. R3 fallback parser 只覆盖 [selected_seed_examples/](../selected_seed_examples/) 四例，不承诺通用 PlantUML / Umple / TTool 转换器。

## 2. 工具链表

| format | candidate_tool | source_url | source_type | language | install_or_access | cli_available | ast_or_export_available | selected_for_r3 | reason | risk | verification_command | last_verified_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PlantUML state diagram | PlantUML CLI / jar | <https://plantuml.com/command-line> | 官方文档 | Java/JVM | `java -jar plantuml.jar ...`；也可用发行版或 Docker | 是 | 支持渲染和多格式导出；但 R3 未依赖稳定公开 AST | 是（工具链调研 + fallback parser） | PlantUML 是两个 smoke 样例的一手 `STM_0` 格式；官方 CLI 可做语法 / 渲染核验，但 R3 需要结构化 states/transitions，因此使用最小 state-diagram parser 并记录限制。 | PlantUML 语义宽、宏和皮肤语法多；v0 parser 只覆盖四例中的 `state {}`、`A --> B : label`、quoted state、`[*]`。 | `java -version`; `curl -L https://plantuml.com/command-line | rg -n "java -jar plantuml.jar|--svg|--scxml|--xmi"` | 2026-06-24 17:26:35 |
| Umple textual state machine | Umple compiler / CLI | <https://cruise.umple.org/umple/UmpleTools.html> / <https://cruise.umple.org/umple/GettingStarted.html> | 官方手册 | Java/JVM | `java -jar umple.jar ...`；部分平台可包管理安装 | 是 | 支持多种代码 / 模型导出；R3 未把派生导出当作一手 `STM_0` | 是（工具链调研 + fallback parser） | Umple 是 `sefm-ssc7-umple` 的一手格式；官方 compiler 适合后续 syntax check，R3 v0 先解析四例中的 `class { sm { state { transition; } } }` 子集。 | Umple 完整语法远超 v0；`after(60)` 等 timer-like transition 不能静默降为普通 T0，需要 loss ledger。 | `curl -L https://cruise.umple.org/umple/UmpleTools.html | rg -n "java -jar umple.jar|--generate|Scxml|Json|Ecore"` | 2026-06-24 17:26:35 |
| TTool / AVATAR XML | TTool / AVATAR modeling tool | <https://ttool.telecom-paris.fr/avatar.html> | 官方主页 / 文档入口 | Java / GUI-first | 通过 TTool 网站下载 / 安装并打开 `.xml` 模型 | 本轮未确认稳定 headless CLI | 官方模型文件为 XML；AVATAR 支持建模、验证、代码生成，但 XML schema / headless AST 需继续核验 | 是（条件型 XML inventory adapter） | `ttool-automatedbraking-xml` 是完整 TTool/SysML/AVATAR 工件，R3 至少要定位 AVATAR SMD panel、state component、transition connector 并诚实标 partial。 | GUI-centric；XML 包含 block diagram、signals、timing 和多个 SMD panel，v0 不解析 graphical connecting point 到精确 source/target，也不切出纯 T0 STM。 | `curl -L https://ttool.telecom-paris.fr/avatar.html | rg -n "xml|AVATAR State Machines|formal verification|code generation"` | 2026-06-24 17:26:35 |
| FCSTM DSL | pyfcstm | <https://github.com/HansBug/pyfcstm> / <https://pypi.org/project/pyfcstm/0.4.0/> | 本地 submodule + 官方仓库/PyPI | Python | `git submodule update --init --recursive`; `pip install -e ./pyfcstm` | 是 | `python -m pyfcstm` 提供 parse / plantuml / simulate 等 project-level 能力 | 是（下游消费者候选，不作为 R3 唯一输出） | pyfcstm 是本仓库最可控的结构化诊断 / 执行生态，可作为 R4/R5 后续消费者线索。 | FCSTM 是本仓库生态，不是外部通用 UML 标准；R3 canonical schema 不等同于 pyfcstm DSL。 | `git submodule status --recursive | grep pyfcstm`; `python -m pyfcstm --version`; `python -m pyfcstm --help` | 2026-06-24 17:26:35 |

## 3. R3 选择结论

- PlantUML / Umple：采用“官方工具链调研 + 最小结构化 parser fallback”。原因是官方 CLI 适合语法 / 渲染 / 导出核验，但 R3 当前需要可审计地抽取 states/transitions 并生成统一 JSON，而不是把派生图像或派生 XMI/SCXML 当作一手事实。
- TTool XML：采用 XML inventory adapter，裁决为 `partial`。R3 只抽取 AVATAR SMD panel、state/start component、transition connector 与 timing 字段，不声称完成 TTool XML 到纯 T0 STM 的无损切片。
- pyfcstm：记录为后续 diagnostic / execution target 的可控消费者，不把 R3 canonical schema 绑定成 pyfcstm DSL，也不把 pyfcstm 写成论文主贡献。

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
