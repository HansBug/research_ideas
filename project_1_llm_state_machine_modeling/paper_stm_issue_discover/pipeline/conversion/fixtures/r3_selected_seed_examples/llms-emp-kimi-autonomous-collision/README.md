# 自主驾驶与碰撞规避 PlantUML 样例

## 1. 来源

- 原始条目：[llms-emp-stm-subset](../../corpora/seed_library/llms-emp-stm-subset/)
- 论文 PDF：[paper.pdf](../../corpora/seed_library/llms-emp-stm-subset/paper.pdf)
- 论文全文提取：[paper_content.txt](../../corpora/seed_library/llms-emp-stm-subset/paper_content.txt)
- BibTeX：[bibtex.bib](../../corpora/seed_library/llms-emp-stm-subset/bibtex.bib)
- 单篇说明：[seed_desc.md](../../corpora/seed_library/llms-emp-stm-subset/seed_desc.md)
- 一手资产说明：[assets/README.md](../../corpora/seed_library/llms-emp-stm-subset/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../corpora/seed_library/llms-emp-stm-subset/seed_resource_registry.json)
- 原始 pair：`llms_emp_stm_results_0039`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | workbook `STM Results` sheet 中的 `Requirement Description`，描述自动驾驶模式、高速 / 城市道路切换与碰撞规避逻辑。 |
| [stm0.puml](./stm0.puml) | 同一行 `Generation PlantUML` 字段中的 Kimi 初始生成 PlantUML。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、locator、哈希、生成方式与 trace 字段。 |
| [model.fcstm](./model.fcstm) | R4.5 表示桥导出的 pyfcstm smoke 快照；同步自 [pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/model.fcstm](../../pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/model.fcstm)，不是一手资源或 repair 后模型。 |
| [fcstm_meta.json](./fcstm_meta.json) | `model.fcstm` 的同步来源、hash、parse/inspect 状态、上游 NL / 原始 STM_0 / canonical / loss 归因记录。 |

## 3. 系统说明

该样例是 LLMS-EMP 中更高难度的 PlantUML smoke 输入：自然语言描述一个自动驾驶模式控制器，包含 `AutonomousMode`、`HighwayMode`、`UrbanMode` 以及独立的 collision avoidance 片段。`STM_0` 是 Kimi 生成的 PlantUML 状态机，包含层次状态、多个条件标签、跨模式转移和碰撞规避激活 / 解除逻辑。它适合替代 TTool XML 作为 R4.5 正向 smoke 样例，因为它仍来自一手 `NL + generated STM_0` pair，且官方 PlantUML 可直接导出 SCXML。

## 4. NL 中文完整翻译

1. 系统从 `AutonomousMode` 状态开始，并转入 `InitialState` 子状态，表示自动驾驶模式的起点。
2. 从 `InitialState` 出发，系统可根据条件 `high_way=true` 转入 `HighwayMode`，或根据 `urban_way=true` 转入 `UrbanMode`。
3. 在 `HighwayMode` 中，系统从 `enter_hwy` 子状态开始，并可根据前车距离 `dist_to_front<25` 与是否存在额外车道 `extra_lane=true` 转入 `cruise` 或 `lane_change`。
4. 若系统处于 `lane_change`，车道变更完成后可回到 `cruise`；若距离出口小于 2 公里 `dist_to_exit<2`，则可退出高速。
5. 在 `cruise` 子状态中，如果前车距离小于 25 米 `dist_to_front<25` 且存在额外车道，系统转入 `lane_change`。如果距离出口小于 2 公里 `dist_to_exit<2`，系统也可退出高速。
6. 当 `auto_finished=true` 条件触发时，`HighwayMode` 结束并转入 `FinishState`。
7. 在 `UrbanMode` 中，系统从 `enter_urban` 子状态开始。若前车距离小于 15 米 `dist_to_front<15` 且存在额外车道，则转入 `lane_change_urban`；若前方道路通畅，则转入 `straight`；若检测到路口 `intersection=true`，则转入 `intersection`。
8. 在 `lane_change_urban` 子状态中，车道变更完成后转入 `straight`；若距离城市出口小于 0.7 公里 `dist_to_exit<0.7`，则转入 `exit_urban`。
9. 在 `straight` 子状态中，若检测到路口，系统转入 `intersection`；若前车距离小于 15 米 `dist_to_front<15` 且存在额外车道，则转入 `lane_change_urban`。
10. 一旦满足 `auto_finished=true`，系统退出 `UrbanMode` 并转入 `FinishState`。
11. 系统支持根据 `urban_way=true` 与 `high_way=true` 在 `HighwayMode` 和 `UrbanMode` 之间动态切换，从而在驾驶过程中实现无缝模式转换。
12. 碰撞规避系统初始处于 `collision_avoidance_deactive`。当检测到行人 `pedestrian_detected`、后方距离小于 5 米且速度超过 30 km/h `dist_to_rear<5 & vel>30`，或在高速 / 城市场景下前方距离低于阈值时，系统转入 `collision_avoidance_active`。
13. 当 `front_inactive`、`rear_inactive` 与 `pedestrian_inactive` 表明没有活动危险后，碰撞规避系统从 `collision_avoidance_active` 回到 `collision_avoidance_deactive`。

## 5. STM 文件说明

- 格式：PlantUML，文件为 [stm0.puml](./stm0.puml)。
- 谱系：UML state diagram / PlantUML statechart，包含层次状态与并列顶层片段。
- 时间特性：未见 timed automata clock；当前按 T0 离散状态机处理。
- 难度来源：包含层次模式切换、条件标签、碰撞规避片段和多条带复合条件的转移，规模高于 [高层驾驶模块 PlantUML](../llms-emp-gpt4o-hldcs/README.md)。
- 重要 caveat：PlantUML / SCXML 工具链会把 `dist_to_front<25 && extra_lane=true` 等标签主要保留为事件或标签文本；R4.5 只验证 canonical 到 `.fcstm` 表示桥的连通性，不把这些标签自动解释为严格 guard 语义，也不把转换收益计入 repair gain。

## 6. R4.5 FCSTM 派生快照

- 派生文件：[model.fcstm](./model.fcstm)。
- 元数据：[fcstm_meta.json](./fcstm_meta.json)。
- 上游 R4.5 输出：[pipeline representation model.fcstm](../../pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/model.fcstm)、[name_mapping.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/name_mapping.json)、[lowering_inventory.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/lowering_inventory.json)、[parse_inspect_report.json](../../pipeline/representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/parse_inspect_report.json)。
- 当前状态：`fcstm_meta.json` 中 `parse_status=ok`、`inspect_status=ok`、`repair_contribution_allowed=false`。
- 口径说明：R4.5 从官方 SCXML canonical 导出可被 pyfcstm parse/inspect 的 smoke `.fcstm`；多个疑似 guard 的条件标签只作 named event 和 loss ledger caveat，不自动恢复为严格 guard。
- 维护纪律：若 R3 canonical、R4.5 exporter 或 [../../pipeline/representation/reports/fcstm_export_report.json](../../pipeline/representation/reports/fcstm_export_report.json) 变化，必须先重新生成 R4.5 reports，再运行 `python -m paper_stm_representation.cli sync-selected-fcstm` 同步本目录；不得手工只改本目录 [model.fcstm](./model.fcstm)。
