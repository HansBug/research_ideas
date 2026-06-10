# Path-1 Sample and Historical Asset Ledger

## 1. 资产来源与使用原则

本文件把历史 Path-1 sprint PR [#9](https://github.com/HansBug/research_ideas/pull/9) 中对第一篇论文仍有价值的样本、扩充 NL、参考模型和数据文件压缩迁移到当前 foundation 工作区。

硬原则：

1. 这些资产是 **historical sprint evidence / candidate inputs / reference assets**，不是当前 paper 的主实验结果。
2. 所有样本、reference、baseline、oracle 在进入正式 paper 之前都必须重新进入冻结协议、人工复核和 run-record 体系。
3. PR #9 的自动评分和扩充 NL 可以作为 selection rationale，但不能直接证明方法效果。
4. 任何使用这些资产的论文 claim 都必须在 [claim_evidence_map.md](../story/claim_evidence_map.md) 中明确证据状态。

## 2. PR #9 可搬运资产总览

| 资产 | 历史路径 | 数量 / 状态 | 当前用途 | 不能怎么用 |
|---|---|---:|---|---|
| 323 sample selection pool | `project_1_llm_state_machine_modeling/paper_v1/selection/candidates.jsonl` in PR #9 branch | 323 条 T0+🟢 控制系统 sample | 作为 Path-1 stress-test 样本池来源和抽样纪律证据 | 不能说成正式 benchmark 已冻结 |
| selection report | `paper_v1/selection/SELECTION_REPORT.md` in PR #9 branch | Top-15 + Backup-15 + 全量评分统计 | 迁移 Top-15 / Backup-15 和评分维度定义 | 不能说成最终实验结果 |
| expansion report | `paper_v1/selection/expansion/EXPANSION_REPORT.md` in PR #9 branch | 30/30 扩充完成，0 fail，0 marker mismatch | 作为严格溯源 NL 扩充资产 | 不能把扩充文本当作人工 oracle |
| expansion JSON | `paper_v1/selection/expansion/expansions/*.json` in PR #9 branch | 30 个 JSON | 后续构造 frozen NL input / provenance packet 的候选原料 | 不能不复核就进入 main result |
| Path-1 parquet | `project_1_llm_state_machine_modeling/eval/data/sources_path1.parquet` in PR #9 branch | 1 个主数据文件 | 历史 sprint 主数据集候选 | 不能默认与当前 main 的正式样本一致 |
| Path-1 backup parquet | `project_1_llm_state_machine_modeling/eval/data/sources_path1_backup.parquet` in PR #9 branch | 1 个备份数据文件 | 备份样本池候选 | 语义需重新核验 |
| historical early reference draft STM | `paper_v1/selection/ref_stms/audited/...` in PR #9 branch | 2 个：CARA 低-V、CubeSat 高-V | 参考模型纪律、V-rich/V-poor 对照、ref pipeline few-shot | 不能直接作为最终 signed reference model |
| ref-STM handover | `paper_v1/selection/ref_stms/HANDOVER.md` in PR #9 branch | 1 份 | 迁移 D1-D8 纪律和 pipeline 风险 | 不能当作 pipeline 完工证明 |
| Path-1 report | `paper_v1/PATH1_REPORT.md` in PR #9 branch | Phase 4a 完成，4b 进行中，结果 TODO | 历史状态说明 | 不能作为 current paper result |

## 3. Selection 统计摘要

历史 selection report 给出的关键统计：

- 已评审 sample 总数：323。
- 通过硬排除 + base≥4 的合格样本：305。
- Top-15：15。
- Backup-15：15。
- 排除 / 不合格：18。

STM 类型分布：

| STM 类型 | 评审样本数 | Top-15 中数量 | 历史目标 |
|---|---:|---:|---:|
| HSM | 71 | 7 | 5-6 |
| EFSM | 172 | 5 | 4-5 |
| FSM | 68 | 3 | 2-3 |
| Other | 12 | 0 | ≤1 |

评分维度：

| 维度 | 含义 | 与 Path-1 的关系 |
|---|---|---|
| H | Hierarchical / composite states | 对齐 prior baseline 的 hierarchy 弱项 |
| G | Guarded arithmetic | 对齐 guard correctness 弱项 |
| A | Non-trivial actions | 对齐 action correctness 弱项 |
| F | Fault recovery / global escape | 检查跨状态恢复和 safety/fail-safe 逻辑 |
| bd | baseline-trap density | 估计 prior baseline 容易丢失的内容结构 |
| ft | formal-state-machine tool fit | 估计形式化表示 / 检查 / 仿真是否有发挥空间 |

> 注意：selection 是 stress-test design，不是代表性随机抽样。正式论文中若报告平均性能，必须另行冻结代表性或分层样本；若报告 stress-test 性能，则必须明确说明选择逻辑。

## 4. Top-15 样本表

| # | 领域 | sample_id | type | 系统简述 | H | G | A | F | final | 历史用途 |
|---:|:-:|---|---|---|:-:|:-:|:-:|:-:|---:|---|
| 1 | ⚙️ | `amazing-race-robot-edition__01` | HSM | 室内寻人问路与寻门任务监督器 | 3 | 3 | 3 | 3 | 12.9 | 高层机器人 HSM stress test |
| 2 | ✈️ | `autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle__01` | HSM | 室内灭火无人机室外-室内任务监督控制器 | 3 | 3 | 3 | 3 | 12.9 | UAV mission hierarchy + recovery |
| 3 | ⚙️ | `autonomous-navigation-framework-holonomic-mobile-robots-agriculture__01` | HSM | 温室全向移动机器人导航与巡检监督控制器 | 3 | 3 | 3 | 3 | 12.9 | navigation / alignment / rail traversal |
| 4 | 🌡️ | `control-system-design-of-water-filter-test-bench__01` | HSM | 水滤测试台主状态、阀门与泵监督控制器 | 3 | 3 | 3 | 3 | 12.9 | industrial process HSM |
| 5 | 🏭 | `fault-handling-plc-industry4__02` | HSM | 包装机械模块故障后恢复控制过程 | 3 | 3 | 3 | 3 | 12.9 | PLC fault recovery |
| 6 | ⚙️ | `finite-state-automaton-control-system-walking-machines__01` | HSM | walking machine / hexapod 高层导航与步态监督控制器 | 3 | 3 | 3 | 3 | 12.9 | walking machine HSM |
| 7 | 🩺 | `cara-infusion-pump-formal-spec__01` | EFSM | CARA 输液泵控制系统中的泵控制方式 | 2 | 3 | 3 | 3 | 11.9 | 低-V historical early reference draft 经验 |
| 8 | 🅿️ | `lift-control-automatic-car-parking-using-plc__01` | EFSM | PLC 多层停车升降机定位与存取控制器 | 2 | 3 | 3 | 3 | 11.9 | parking lift EFSM |
| 9 | 🏭 | `plc-scada-liquid-filling-automation-ejosat__01` | EFSM | PLC/SCADA 液体灌装产线控制器 | 2 | 3 | 3 | 3 | 11.9 | process automation EFSM |
| 10 | 🚆 | `railway-generic-electronic-interlocking-software-engineering-methods__01` | EFSM | 电子铁路联锁软件 Route 3 控制链 | 2 | 3 | 3 | 3 | 11.9 | railway interlocking EFSM |
| 11 | ✈️ | `reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01` | EFSM | Masat-1 CubeSat 飞控任务/故障管理逻辑 | 2 | 2 | 3 | 3 | 11.0 | 高-V historical early reference draft 经验 |
| 12 | ⚙️ | `finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking__01` | FSM | MABEL 双足机器人台阶/绊倒应对监督控制器 | 2 | 3 | 3 | 3 | 11.9 | bipedal recovery FSM |
| 13 | 🌡️ | `optimization-control-energy-management-system-microgrids__01` | FSM | 并网微电网 EMS 模式切换控制器 | 2 | 3 | 3 | 3 | 11.3 | energy management FSM |
| 14 | ✈️ | `automated-contingency-management-in-unmanned-aircraft-systems__01` | FSM | 无人机自动应急管理安全监视器 | 1 | 3 | 3 | 3 | 10.9 | contingency management |
| 15 | 🚗 | `full-automated-drive-urban-environments-gomentum-station__01` | HSM | 城市场景自动驾驶高层行为监督器 | 3 | 3 | 3 | 3 | 12.9 | autonomous driving HSM |

## 5. Backup-15 样本表

| # | 领域 | sample_id | type | 系统简述 | final | 可能用途 |
|---:|:-:|---|---|---|---:|---|
| 1 | ✈️ | `long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition__01` | HSM | 长时自主旋翼无人机数据采集与回充任务控制器 | 12.9 | UAV endurance / recharge |
| 2 | ✈️ | `methodology-to-develop-a-discrete-event-supervisory-controller-for-an-autonomous-helicopter-flight__01` | HSM | Bell 412 直升机自主飞行监督控制器 | 12.9 | helicopter supervisor |
| 3 | 🚗 | `odin-team-victortango-darpa-urban-challenge__01` | HSM | 城市自动驾驶分层 driving behaviors 控制器 | 12.9 | autonomous driving backup |
| 4 | ✈️ | `onboard-mission-management-vtol-uav-sequence-supervisory-control__01` | HSM | VTOL 无人机机载任务执行与监督控制器 | 12.9 | mission management |
| 5 | ✈️ | `robust-accurate-drone-landing-moving-targets__01` | HSM | 移动目标无人机视觉滑降监督控制器 | 12.9 | drone landing |
| 6 | 🏭 | `safety4-dynamic-fsm-multilayer-operation-modes__01` | HSM | 人机协作机床上下料单元安全 operation-mode 控制器 | 12.9 | safety operation modes |
| 7 | 🅿️ | `scale-model-parking-garage-integrating-automation-in-parking-facilities__01` | HSM | 环形车库自动/手动分层控制器 | 12.9 | parking garage HSM |
| 8 | ✈️ | `sequence-supervisory-control-onboard-uav-mission-management__01` | HSM | Mission / Command Mode 无人直升机任务控制器 | 12.9 | UAV mission backup |
| 9 | ⚙️ | `autonomous-robotic-manipulation-exploratory-interactions__01` | HSM | 自主机器人材料探索与舀取任务监督控制器 | 12.1 | manipulation task |
| 10 | 🏢 | `mechatronic-control-system-finite-state-machine__01` | HSM | 自动滑门运动与阻塞恢复控制器 | 12.1 | building mechatronics |
| 11 | 🏭 | `prefabricated-board-transfer-palletizer-s7-1500-plc__01` | HSM | 预制板转运码垛机模式与顺序控制器 | 12.1 | PLC palletizer |
| 12 | ⚙️ | `state-machine-based-hybrid-position-force-control-waste-mobile-robot__01` | HSM | 垃圾分拣移动机器人 5DOF 机械臂任务监督控制器 | 12.1 | force/position mobile robot |
| 13 | 🌡️ | `virtual-commissioning-wick-soilless-cultivations__01` | HSM | 营养液制备模块分层监督控制器 | 12.1 | virtual commissioning |
| 14 | ✈️ | `autonomous-uav-multimodal-mapping-underground-mines__01` | HSM | 地下矿井测绘无人机任务监督控制器 | 12.0 | underground UAV |
| 15 | ✈️ | `hybrid-autonomy-future-mars-science-helicopter__01` | HSM | 火星科学直升机任务自治监督器 | 12.0 | Mars helicopter |

## 6. 30 条扩充 NL 资产

历史 expansion report 给出的摘要：

- 30 个 sample（15 candidate + 15 backup）全部完成。
- 0 fail，0 marker mismatch。
- mean = 266.3 words，min = 234，max = 289。
- 平均 inline markers = 17.4，provenance entries = 17.4，保持 1:1。

覆盖率：

| 轴 | 支持数 | 不支持数 | 支持率 | 说明 |
|---|---:|---:|---:|---|
| H 层次 | 25 | 5 | 83% | mode / sub-phase / nested hooks |
| G 守卫算术 | 24 | 6 | 80% | 多变量算术 guard hook |
| A 动作 | 30 | 0 | 100% | 非平凡 action hook |
| F 故障恢复 | 22 | 8 | 73% | 全局应急 / safe-state / fail-safe hook |
| bd baseline-trap | 29 | 1 | 96% | prior baseline failure-mode signal |
| ft tool-fit | 17 | 13 | 56% | 深复合 init / SMT guard / forced+aspect / abstract action |

正式使用前必须做三件事：

1. 对每条 expanded NL 与原始 `paper_content.txt` / `STM.md` 做抽样或全量人工复核。
2. 冻结 NL input hash、来源路径、版本和排除规则。
3. 把 expansion 作为输入材料，而不是 reference oracle；reference model 仍需人工确认。

## 7. Historical early reference draft 经验

| case | 历史路径 | 状态 | 关键经验 | 当前处理 |
|---|---|---|---|---|
| CARA | `paper_v1/selection/ref_stms/audited/cara-infusion-pump-formal-spec__01/` in PR #9 branch | historical draft v3，含 `bundle.md`、`ref_model.fcstm`、`ref_components.json` | 低-V / mode-switching case；输出信号变量容易变成“为变量而变量” | 可作为 low-V historical reference-discipline case；正式 ref 仍需复核 |
| CubeSat | `paper_v1/selection/ref_stms/audited/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01/` in PR #9 branch | historical draft v1，含 `ref_model.fcstm`、`ref_components.json`；缺 `bundle.md` | 高-V case；`@external`、counter self-read、V-driven guard、forced transition effect 限制、event/guard 分离 | 可作为 high-V historical reference-discipline case；需要补 bundle / review |

历史 handover 固定的 D1-D8 discipline：

| ID | discipline | 当前论文意义 |
|---|---|---|
| D1 | drop mode-mirror | 避免把目标状态重复写成无意义 action |
| D2 | drop event-paraphrase | 避免把 event 复述成 dummy variable |
| D3 | drop external-actor actions | 区分 controller action 与外部 actor 行为 |
| D4 | output signal vars + pulse-signal handshake | 处理输出信号变量的可审计使用 |
| D5 | case-by-case judge V necessity | 变量不是装饰品；只在 NL 支持时引入 |
| D6 | `@external` annotation | 区分外部输入变量与内部控制变量 |
| D7 | forced transition 无 effect 的 enter-clear 模式 | 保持 DSL 语义与 recovery 建模一致 |
| D8 | event-driven vs guard-driven 分离 | 避免不受支持的 event + guard 混合表达 |

## 8. 当前需要补做的核验

| 优先级 | 待核验项 | 原因 | 目标文件 |
|---|---|---|---|
| C | 冻结正式 sample registry 前重核 selection 代表性 / stress-test 口径 | selection 是按 weak-component stress test 设计，不能默认代表平均场景 | future `tables/03_sample_registry.csv` |
| C | reference model 必须由 human adjudication 确认 | PR #9 的 historical early reference drafts 是 early assets，不是最终 oracle | future `oracle_protocol.md` |
| I | CubeSat `bundle.md` 缺失 | 高-V historical reference draft 的审计链不完整 | future ref packet |
| I | `sources_path1_backup.parquet` 语义待核验 | 当前报告未清晰定义 backup parquet | future data ledger |
| M | Top-15 HSM 偏多 | stress-test 合理，但如写代表性 claim 需分层修正 | sample registry |
