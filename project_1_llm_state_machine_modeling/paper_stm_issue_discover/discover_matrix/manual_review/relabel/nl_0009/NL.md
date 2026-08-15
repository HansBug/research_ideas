<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0009 -->
# NL 规约材料 · `nl_0009`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0009`](./0009.md)、[`0019`](./0019.md)、[`0029`](./0029.md)、[`0039`](./0039.md)、[`0049`](./0049.md)、[`0059`](./0059.md)。它们由**同一份 NL 规约**（sha8 `b7425c44`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **13** 段（`NL-L001` … `NL-L013`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0009.json](../translations/nl_0009.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. The system begins in the AutonomousMode state, which transitions into the InitialState substate, marking the starting point of the autonomous driving mode. | 1. 系统起始于自动驾驶模式（AutonomousMode）状态，其转入初始状态（InitialState）子状态，标志自动驾驶模式的起点。 |
| `NL-L002` | 2. From the InitialState, the system can transition to either HighwayMode or UrbanMode based on conditions: `high_way=true` for HighwayMode or `urban_way=true` for UrbanMode. | 2. 从初始状态出发，系统可迁移到高速模式（HighwayMode）或城市模式（UrbanMode）之一，基于条件：`high_way=true` 对应高速模式，或 `urban_way=true` 对应城市模式。 |
| `NL-L003` | 3. In the HighwayMode state, the system begins in the enter_hwy substate, and can transition to cruise or lane_change based on the distance to the front vehicle (`dist_to_front<25`) and the availability of an extra lane (`extra_lane=true`). | 3. 在高速模式状态中，系统起始于进入高速（enter_hwy）子状态，且可迁移到巡航（cruise）或变道（lane_change），基于与前车的距离（`dist_to_front<25`（前车距离小于 25））以及额外车道的可用性（`extra_lane=true`）。 |
| `NL-L004` | 4. If the system is in lane_change, it can return to cruise once the lane change is completed or exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`). | 4. 如果系统处于变道中，它可返回巡航，一旦变道完成，或驶出高速公路，如果到出口的距离小于 2 千米（`dist_to_exit<2`）。 |
| `NL-L005` | 5. In the cruise substate, if the distance to the front vehicle becomes less than 25 meters (`dist_to_front<25`) and there is an extra lane available, the system transitions to lane_change. The system can also exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`). | 5. 在巡航子状态中，如果与前车的距离变得小于 25 米（`dist_to_front<25`）且存在可用额外车道，系统迁移到变道。系统也可驶出高速公路，如果到出口的距离小于 2 千米（`dist_to_exit<2`）。 |
| `NL-L006` | 6. The HighwayMode ends when the system transitions to FinishState, triggered by the `auto_finished=true` condition. | 6. 高速模式结束，当系统迁移到完成状态（FinishState）时，由 `auto_finished=true`（自动驾驶完成）条件触发。 |
| `NL-L007` | 7. In UrbanMode, the system begins in the enter_urban substate. From here, it can transition to lane_change_urban if the distance to the front vehicle is less than 15 meters (`dist_to_front<15`) and an extra lane is available, or straight if the road ahead is clear, or intersection if it detects an intersection (`intersection=true`). | 7. 在城市模式中，系统起始于进入城区（enter_urban）子状态。从这里出发，它可迁移到城区变道（lane_change_urban），如果与前车的距离小于 15 米（`dist_to_front<15`）且存在可用额外车道，或直行（straight），如果前方道路畅通，或交叉口（intersection），如果它检测到交叉口（`intersection=true`）。〔译者存疑：原文「or straight ...」与「or intersection ...」为省略式，未重复「transition to」；译文「或直行」「或交叉口」同样承前省略了动词「迁移到」，未补出，省略结构与原文一致。〕 |
| `NL-L008` | 8. In the lane_change_urban substate, the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`). | 8. 在城区变道子状态中，系统迁移到直行，如果变道完成，或到驶离城区（exit_urban），如果到城区出口的距离小于 0.7 千米（`dist_to_exit<0.7`）。 |
| `NL-L009` | 9. In the straight substate, if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters (`dist_to_front<15`) and an extra lane is available, it transitions to lane_change_urban. | 9. 在直行子状态中，如果系统检测到交叉口，它迁移到交叉口子状态。如果与前车的距离变得小于 15 米（`dist_to_front<15`）且存在可用额外车道，它迁移到城区变道。 |
| `NL-L010` | 10. The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied. | 10. 系统驶出城市模式状态，通过迁移到完成状态，一旦 `auto_finished=true` 得到满足。 |
| `NL-L011` | 11. The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive. | 11. 系统支持高速模式与城市模式之间的动态迁移，基于条件 `urban_way=true` 和 `high_way=true`，分别地，促成行驶期间的无缝模式切换。 |
| `NL-L012` | 12. The collision avoidance system is initially in the collision_avoidance_deactive state. It transitions to collision_avoidance_active when certain conditions are met, such as detecting pedestrians (`pedestrian_detected`), the rear distance being less than 5 meters with a velocity over 30 km/h (`dist_to_rear<5 & vel>30`), or the front distance being less than 15 meters in highway mode or 10 meters in urban mode. | 12. 防碰撞系统（collision avoidance system）初始处于防碰撞未激活（collision_avoidance_deactive）状态〔原文如此：deactive 非标准英语词，疑为 deactivated 或 inactive 之误〕。它迁移到防碰撞激活（collision_avoidance_active），当某些条件满足时，如检测到行人（`pedestrian_detected`）、后方距离小于 5 米且速度超过 30 km/h（`dist_to_rear<5 & vel>30`）、或前方距离小于 15 米（在高速模式下）或 10 米（在城市模式下）。〔原文如此：`dist_to_rear<5 & vel>30` 使用单个 `&` 而非 `&&`，且该表达式是全文唯一使用符号连接词的地方，其余并列条件用 and / or / with 或逗号连接〕〔译者存疑：原文「in highway mode」/「in urban mode」未说明指的是系统处于状态 HighwayMode / UrbanMode，还是指条件变量 `high_way=true` / `urban_way=true`；译文照字面译作「在高速模式下」/「在城市模式下」，未作取舍。〕 |
| `NL-L013` | 13. Once in the collision_avoidance_active state, the collision avoidance system returns to the collision_avoidance_deactive state when there is no active danger, as indicated by the conditions `front_inactive`, `rear_inactive`, and `pedestrian_inactive`. | 13. 一旦处于防碰撞激活状态，防碰撞系统返回到防碰撞未激活状态〔原文如此：deactive 拼写异常，见第 12 句标注〕，当不存在活跃危险时，如条件 `front_inactive`（前方未激活）、`rear_inactive`（后方未激活）和 `pedestrian_inactive`（行人未激活）所示。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句给出初始状态与初始点：系统起始于 AutonomousMode 状态，转入 InitialState 子状态，后者被标为自动驾驶模式的起点；InitialState 被表述为 AutonomousMode 的子状态（层次）。歧义：which 的先行词既可能是 the AutonomousMode state（语法上最近的先行词），也可能是 the system，「转入」的主体不明确。
- `NL-L002`：该句要求两条迁移：从 InitialState 到 HighwayMode、从 InitialState 到 UrbanMode，条件分别为 `high_way=true` 与 `urban_way=true`。原文未说明这两条迁移的触发事件，也未说明两个条件是否互斥、同时为真时如何取舍。
- `NL-L003`：该句要求 HighwayMode 的初始子状态为 enter_hwy，并要求从 enter_hwy 出发的两条迁移：到 cruise 与到 lane_change，条件是与前车的距离小于 25（`dist_to_front<25`）且存在可用额外车道（`extra_lane=true`）。原文未说明这两个条件是否共同约束两条迁移还是分别对应其中一条，也未说明触发事件。
- `NL-L004`：该句要求从 lane_change 出发的两条迁移：其一返回 cruise，触发为「变道完成」（无形式化条件）；其二驶出高速公路，条件为到出口的距离小于 2 千米（`dist_to_exit<2`）。原文未给出「驶出高速公路」迁移的目标状态，也未说明触发事件。
- `NL-L005`：该句要求从 cruise 出发的两条迁移：其一，当前车距离小于 25 米（`dist_to_front<25`）且存在可用额外车道时，迁移到 lane_change；其二，当到出口的距离小于 2 千米（`dist_to_exit<2`）时，驶出高速公路。与第 4 句相同，原文未给出后者的目标状态，也未说明触发事件。
- `NL-L006`：该句要求 HighwayMode 结束的迁移：目标为 FinishState，条件为 `auto_finished=true`。原文未点名该迁移的源状态（未说明是 HighwayMode 自身还是其内部某个子状态），也未说明触发事件。
- `NL-L007`：该句要求 UrbanMode 的初始子状态为 enter_urban，并要求从该处出发的三条迁移：到 lane_change_urban（条件：前车距离小于 15 米（`dist_to_front<15`）且存在可用额外车道）；到 straight（条件：前方道路畅通，无形式化表达式）；到 intersection（条件：检测到交叉口（`intersection=true`））。「前方道路畅通」与「检测到交叉口」的判定标准原文未说明，三条迁移的触发事件也均未给出。
- `NL-L008`：该句要求从 lane_change_urban 出发的两条迁移：到 straight（触发为「变道完成」）与到 exit_urban（条件：到城区出口的距离小于 0.7 千米（`dist_to_exit<0.7`））。两条迁移的触发事件原文均未给出。
- `NL-L009`：该句要求从 straight 出发的两条迁移：检测到交叉口时迁移到 intersection 子状态；前车距离小于 15 米（`dist_to_front<15`）且存在可用额外车道时迁移到 lane_change_urban。两条迁移的触发事件原文均未给出。
- `NL-L010`：该句要求 UrbanMode 结束的迁移：系统迁移到 FinishState，条件为 `auto_finished=true` 满足。与第 6 句相同，原文未点名该迁移在 UrbanMode 内的源子状态，也未说明触发事件。
- `NL-L011`：该句要求 HighwayMode 与 UrbanMode 之间的动态迁移，基于条件 `urban_way=true` 和 `high_way=true`。按 respectively 的字面顺序，`urban_way=true` 对应 HighwayMode、`high_way=true` 对应 UrbanMode，与第 2 句的显式对应（`high_way=true` 对应 HighwayMode、`urban_way=true` 对应 UrbanMode）相反。原文未说明这些迁移的方向（由哪个模式到哪个模式）与触发事件，也未定义「动态」的含义。
- `NL-L012`：该句要求：防碰撞系统初始处于 collision_avoidance_deactive 状态，当某些条件满足时迁移到 collision_avoidance_active 状态。原文列出三类条件：检测到行人（`pedestrian_detected`）；后方距离小于 5 米且速度超过 30 km/h（`dist_to_rear<5 & vel>30`）；前方距离在高速模式下小于 15 米、在城市模式下小于 10 米（该条无形式化表达式）。歧义与问题：①「速度超过 30 km/h」的速度归属未说明；②「某些条件满足」与三类条件的关系未说明（三类前有 such as，未说明是否穷举、满足其一还是全部）；③前方距离阈值（高速模式 15 米）与第 3、5 句的 `dist_to_front<25`（25 米）不一致。
- `NL-L013`：该句要求从 collision_avoidance_active 返回 collision_avoidance_deactive 的迁移，条件为不存在活跃危险，由 `front_inactive`、`rear_inactive`、`pedestrian_inactive` 三个条件标示。原文未说明这三个条件须全部满足还是满足其一即可，也未说明触发事件。collision_avoidance_deactive 中 deactive 的拼写异常已在第 12 句标注。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英→中，正文照此译名）：AutonomousMode→自动驾驶模式；InitialState→初始状态；HighwayMode→高速模式；UrbanMode→城市模式；enter_hwy→进入高速；cruise→巡航；lane_change→变道；FinishState→完成状态；enter_urban→进入城区；lane_change_urban→城区变道；straight→直行；intersection→交叉口；exit_urban→驶离城区；collision avoidance system→防碰撞系统；collision_avoidance_deactive→防碰撞未激活；collision_avoidance_active→防碰撞激活。

通用术语：state→状态；substate→子状态；transition→迁移；condition→条件；mode→模式。守卫类表达式（`dist_to_front<25` 等）按原文逐字保留，不做改写。

原文共 13 句；点名的状态/子状态对象 15 个；出现在条件中的变量/标志标识符 13 个（其中 intersection 同时是子状态名）。

反复出现的欠指定：①全篇未出现显式命名的事件，各迁移的触发均以条件（守卫）或自然语言情形表述，事件槽位空缺；②多条迁移未点名源或目标状态（第 4、5 句「驶出高速公路」的目标状态、第 6、10 句结束迁移的源子状态、第 11 句模式间迁移的方向）；③第 11 句的 respectively 按字面顺序把 `urban_way=true` 对应 HighwayMode、`high_way=true` 对应 UrbanMode，与第 2 句的显式对应（`high_way=true` 对应 HighwayMode、`urban_way=true` 对应 UrbanMode）相反。

原文质量问题：第 12、13 句的 collision_avoidance_deactive 中 deactive 非标准英语词（疑为 deactivated 或 inactive）；第 12 句「高速模式下前方距离小于 15 米」与第 3、5 句的 `dist_to_front<25`（25 米）不一致；第 1 句 which 的先行词不明确。

边界外要素：原文不含时间与并发类约束（无秒级时间要求、无并发激活表述），全部要求落在状态、迁移、条件（守卫）与变量范围内。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. The system begins in the AutonomousMode state, which transitions into the InitialState substate, marking the starting point of the autonomous driving mode. 
  2 | 2. From the InitialState, the system can transition to either HighwayMode or UrbanMode based on conditions: `high_way=true` for HighwayMode or `urban_way=true` for UrbanMode. 
  3 | 3. In the HighwayMode state, the system begins in the enter_hwy substate, and can transition to cruise or lane_change based on the distance to the front vehicle (`dist_to_front<25`) and the availability of an extra lane (`extra_lane=true`). 
  4 | 4. If the system is in lane_change, it can return to cruise once the lane change is completed or exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`). 
  5 | 5. In the cruise substate, if the distance to the front vehicle becomes less than 25 meters (`dist_to_front<25`) and there is an extra lane available, the system transitions to lane_change. The system can also exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`). 
  6 | 6. The HighwayMode ends when the system transitions to FinishState, triggered by the `auto_finished=true` condition. 
  7 | 7. In UrbanMode, the system begins in the enter_urban substate. From here, it can transition to lane_change_urban if the distance to the front vehicle is less than 15 meters (`dist_to_front<15`) and an extra lane is available, or straight if the road ahead is clear, or intersection if it detects an intersection (`intersection=true`). 
  8 | 8. In the lane_change_urban substate, the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`). 
  9 | 9. In the straight substate, if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters (`dist_to_front<15`) and an extra lane is available, it transitions to lane_change_urban. 
 10 | 10. The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied. 
 11 | 11. The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive. 
 12 | 12. The collision avoidance system is initially in the collision_avoidance_deactive state. It transitions to collision_avoidance_active when certain conditions are met, such as detecting pedestrians (`pedestrian_detected`), the rear distance being less than 5 meters with a velocity over 30 km/h (`dist_to_rear<5 & vel>30`), or the front distance being less than 15 meters in highway mode or 10 meters in urban mode. 
 13 | 13. Once in the collision_avoidance_active state, the collision avoidance system returns to the collision_avoidance_deactive state when there is no active danger, as indicated by the conditions `front_inactive`, `rear_inactive`, and `pedestrian_inactive`.
```
