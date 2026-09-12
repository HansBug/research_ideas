# 高层驾驶模块 PlantUML 样例

## 1. 来源

- 原始条目：[llms-emp-stm-subset](../../../../../corpora/seed_library/llms-emp-stm-subset)
- 论文 PDF：[paper.pdf](../../../../../corpora/seed_library/llms-emp-stm-subset/paper.pdf)
- 论文全文提取：[paper_content.txt](../../../../../corpora/seed_library/llms-emp-stm-subset/paper_content.txt)
- BibTeX：[bibtex.bib](../../../../../corpora/seed_library/llms-emp-stm-subset/bibtex.bib)
- 单篇说明：[seed_desc.md](../../../../../corpora/seed_library/llms-emp-stm-subset/seed_desc.md)
- 一手资产说明：[assets/README.md](../../../../../corpora/seed_library/llms-emp-stm-subset/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../../../../corpora/seed_library/llms-emp-stm-subset/seed_resource_registry.json)
- 原始 pair：`llms_emp_stm_results_0000`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | workbook `STM Results` sheet 中的 `Requirement Description`，描述高层驾驶模块的自然语言需求。 |
| [stm0.puml](./stm0.puml) | 同一行 `Generation PlantUML` 字段中的 GPT-4o 初始生成 PlantUML。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、locator、哈希、生成方式与 trace 字段。 |
| [model.fcstm](./model.fcstm) | R4.5 表示桥导出的 pyfcstm smoke 快照；同步自 [pipeline/representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/model.fcstm](../../../../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/model.fcstm)，不是一手资源或 repair 后模型。 |
| [fcstm_meta.json](./fcstm_meta.json) | `model.fcstm` 的同步来源、hash、parse/inspect 状态、上游 NL / 原始 STM_0 / canonical / loss 归因记录。 |

## 3. 系统说明

该样例描述一个高层驾驶模式控制模块。系统在上电后进入人工驾驶模式；当 `front_distance > 10` 时进入自动驾驶模式；收到人工转向命令、刹车按下或自动驾驶结束后回到人工驾驶；断电后进入最终状态。生成出的 `STM_0` 是 PlantUML 状态机，包含 `HumanDriving` 和 `Autonomous` 两个主要状态块。

## 4. NL 中文完整翻译

1. 人工驾驶模式由一个简单状态表示。
2. 自动驾驶模式具有子状态，并由一个子机器状态表示。
3. 当上电时，系统进入人工驾驶模式。
4. 当 `front_distance > 10` 时，自动切换到自动驾驶状态。
5. 当收到人工转向命令、刹车被按下，或者处于自动驾驶最终状态时，切换回人工驾驶模式。
6. 当断电时，系统切换到最终状态。

## 5. STM 文件说明

- 格式：PlantUML，文件为 [stm0.puml](./stm0.puml)。
- 谱系：SysML / UML state machine 风格的层次化状态机。
- 时间特性：未见 timed automata clock 或 hybrid dynamics；当前按 T0 离散状态机处理。
- 重要 caveat：该论文制品同时提供 reference PlantUML 和 checking 后结果，本样例只允许使用 `Generation PlantUML` 作为 `STM_0`，不得混入 reference 或 checking 列。

## 6. R4.5 FCSTM 派生快照

- 派生文件：[model.fcstm](./model.fcstm)。
- 元数据：[fcstm_meta.json](./fcstm_meta.json)。
- 上游 R4.5 输出：[pipeline representation model.fcstm](../../../../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/model.fcstm)、[name_mapping.json](../../../../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/name_mapping.json)、[lowering_inventory.json](../../../../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/lowering_inventory.json)、[parse_inspect_report.json](../../../../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/parse_inspect_report.json)。
- 当前状态：`fcstm_meta.json` 中 `parse_status=ok`、`inspect_status=ok`、`repair_contribution_allowed=false`。
- 口径说明：R4.5 从官方 SCXML canonical 保留层次结构并导出可被 pyfcstm parse/inspect 的 smoke `.fcstm`；`Front Distance > 10` 这类条件式标签仍按 named event 保留。
- 维护纪律：若 R3 canonical、R4.5 exporter 或 [../../pipeline/representation/reports/fcstm_export_report.json](../../../../representation/reports/fcstm_export_report.json) 变化，必须先重新生成 R4.5 reports，再运行 `python -m paper_stm_representation.cli sync-selected-fcstm` 同步本目录；不得手工只改本目录 [model.fcstm](./model.fcstm)。
