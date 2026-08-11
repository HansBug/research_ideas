# 微波炉控制 PlantUML 样例

## 1. 来源

- 原始条目：[llms-emp-stm-subset](../../corpora/seed_library/llms-emp-stm-subset/)
- 论文 PDF：[paper.pdf](../../corpora/seed_library/llms-emp-stm-subset/paper.pdf)
- 论文全文提取：[paper_content.txt](../../corpora/seed_library/llms-emp-stm-subset/paper_content.txt)
- BibTeX：[bibtex.bib](../../corpora/seed_library/llms-emp-stm-subset/bibtex.bib)
- 单篇说明：[seed_desc.md](../../corpora/seed_library/llms-emp-stm-subset/seed_desc.md)
- 一手资产说明：[assets/README.md](../../corpora/seed_library/llms-emp-stm-subset/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../corpora/seed_library/llms-emp-stm-subset/seed_resource_registry.json)
- 原始 pair：`llms_emp_stm_results_0045`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | workbook `STM Results` sheet 中的 `Requirement Description`，描述微波炉门、物品、烹饪时间、开始、取消和计时器到期等控制逻辑。 |
| [stm0.puml](./stm0.puml) | 同一行 `Generation PlantUML` 字段中的 DeepSeek 初始生成 PlantUML。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、locator、哈希、生成方式与 trace 字段。 |
| [model.fcstm](./model.fcstm) | R4.5 表示桥导出的 pyfcstm smoke 快照；同步自 [pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/model.fcstm](../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/model.fcstm)，不是一手资源或 repair 后模型。 |
| [fcstm_meta.json](./fcstm_meta.json) | `model.fcstm` 的同步来源、hash、parse/inspect 状态、上游 NL / 原始 STM_0 / canonical / loss 归因记录。 |

## 3. 系统说明

该样例来自 LLMS-EMP 的 empirical workbook，是微波炉控制器的 `NL + generated STM_0` 一手 pair。自然语言需求覆盖 `DoorShut`、`DoorOpen`、`DoorOpenWithItem`、`DoorShutWithItem`、`ReadytoCook` 与 `Cooking` 等状态，并描述开门、关门、放入 / 移除物品、输入烹饪时间、启动、取消和计时器到期。`STM_0` 是 DeepSeek 生成的 PlantUML 状态机，包含层次状态、多个用户事件和条件标签，难度高于最小驾驶模式样例，同时比数码相机 fork / join 例更适合当前 R4.5 表示桥稳定跑通。

## 4. NL 中文完整翻译

1. 微波炉从 `DoorShut` 状态开始。在该状态下，若执行 `Cancel` 动作，系统可以保持在 `DoorShut`；当门被打开时，系统转入 `DoorOpen`。
2. 在 `DoorShut` 中发生 `Door Opened` 动作时，系统转入 `DoorOpen`。门关闭后可返回 `DoorShut`。
3. 在 `DoorOpen` 中，放入物品会使系统转入 `DoorOpenWithItem`。如果物品被移除，系统返回 `DoorOpen`。
4. 从 `DoorOpenWithItem` 出发，如果门在烹饪时间为零时关闭，则系统转入 `DoorShutWithItem`；如果输入了烹饪时间，则转入 `ReadytoCook`。
5. 在 `DoorShutWithItem` 中，打开门会使系统回到 `DoorOpenWithItem`；输入烹饪时间会使系统进入 `ReadytoCook`，并显示 / 更新烹饪时间。
6. 在 `ReadytoCook` 中，如果执行 `Cancel` 动作，系统返回 `DoorShutWithItem`，并取消或更新烹饪时间；如果门被打开，系统转入 `DoorOpenWithItem`。
7. 在 `ReadytoCook` 中执行 `Start` 动作时，系统进入 `Cooking`，计时器开始运行。
8. 在 `Cooking` 中，打开门会停止计时器并转入 `DoorOpenWithItem`；如果计时器到期，系统转入 `DoorShutWithItem`；执行 `Cancel` 会使系统返回 `ReadytoCook`。

## 5. STM 文件说明

- 格式：PlantUML，文件为 [stm0.puml](./stm0.puml)。
- 谱系：UML state diagram / PlantUML statechart，包含层次状态和多个事件触发转移。
- 时间特性：NL 描述中有计时器开始与到期，但 `STM_0` 只以 `Timer Expired` 事件表达；当前按 T0 离散状态机处理，不恢复 clock 语义。
- 难度来源：相比高层驾驶模块，它包含更多业务状态、门 / 物品 / 烹饪流程交互和 self-loop；相比数码相机 fork / join 候选，它能被当前 R3/R4.5 工具链稳定转换并进入 `.fcstm` smoke。
- 重要 caveat：PlantUML / SCXML 工具链会把 `[zero time set]` 等条件标签保留为事件或标签文本；R4.5 只验证 canonical 到 `.fcstm` 表示桥的连通性，不把这些标签自动解释为严格 guard 语义，也不把转换收益计入 repair gain。

## 6. R4.5 FCSTM 派生快照

- 派生文件：[model.fcstm](./model.fcstm)。
- 元数据：[fcstm_meta.json](./fcstm_meta.json)。
- 上游 R4.5 输出：[pipeline representation model.fcstm](../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/model.fcstm)、[name_mapping.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/name_mapping.json)、[lowering_inventory.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/lowering_inventory.json)、[parse_inspect_report.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave/parse_inspect_report.json)。
- 当前状态：`fcstm_meta.json` 中 `parse_status=ok`、`inspect_status=ok`、`repair_contribution_allowed=false`。
- 口径说明：R4.5 消费 R3.1 pre-SCXML normalization replay 后的 canonical，导出可被 pyfcstm parse/inspect 的 smoke `.fcstm`；该快照不覆盖 raw `stm0.puml`，也不计 repair gain。
- 维护纪律：若 R3 canonical、R4.5 exporter 或 [../../pipeline/representation/reports/fcstm_export_report.json](../../pipeline/representation/reports/fcstm_export_report.json) 变化，必须先重新生成 R4.5 reports，再运行 `python -m paper_stm_representation.cli sync-selected-fcstm` 同步本目录；不得手工只改本目录 [model.fcstm](./model.fcstm)。
