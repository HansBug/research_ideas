# 高层驾驶模块 PlantUML 样例

## 1. 来源

- 原始条目：[llms-emp-stm-subset](../../llms-emp-stm-subset/)
- 单篇说明：[seed_desc.md](../../llms-emp-stm-subset/seed_desc.md)
- 一手资产说明：[assets/README.md](../../llms-emp-stm-subset/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../llms-emp-stm-subset/seed_resource_registry.json)
- 原始 pair：`llms_emp_stm_results_0000`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | workbook `STM Results` sheet 中的 `Requirement Description`，描述高层驾驶模块的自然语言需求。 |
| [stm0.puml](./stm0.puml) | 同一行 `Generation PlantUML` 字段中的 GPT-4o 初始生成 PlantUML。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、locator、哈希、生成方式与 trace 字段。 |

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
