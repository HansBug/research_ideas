# Project 1 Sources

本清单基于 `BASELINE.md` 中推荐的学术检索关键词簇扩展检索，聚焦后续“状态机自然语言需求/描述数据集”可直接利用的控制系统需求、系统设计、行为建模、形式化规格与验证资料。

## 检索关键词簇

以下关键词簇用于指导后续增量检索，目标不是泛泛地搜“形式化方法”或“建模”，而是优先命中**具有具体控制系统客体**、并且更可能包含可提取状态机自然语言描述的论文。

### 当前推荐关键词簇

- `具体控制对象` + `control system/controller` + `design/requirements/specification`
  - 重点对象：`infusion pump`, `pacemaker`, `elevator control`, `traffic light controller`, `railway interlocking`, `landing gear system`, `vehicle platoon`, `ABS`, `parking system`, `PLC`
- `具体控制对象` + `state machine/FSM/statechart/mode switching/operation mode`
  - 适合寻找论文中显式给出运行模式、状态切换或控制阶段推进的文献
- `具体控制对象` + `formal model/formal specification/verification/modeling`
  - 适合寻找虽然标题不直接写 `state machine`，但正文可能给出可整理控制逻辑的论文
- `railway/rail/interlocking` + `control table/route control/signalling principle/formal verification`
  - 当前对 🚆 领域命中率较高，尤其容易找到进路建立、锁闭、释放等可提取逻辑
- `railway interlocking` + `route establishment/route request/route compatibility/mode selection`
  - 本轮新增结果表明，带有 `route establishment`、`route command`、`TP/DA/MO` 等词的题名或摘要更容易命中可直接整理的联锁控制逻辑
- `medical device` / `infusion pump` / `pacemaker` + `mode/control software/verification/specification`
  - 当前对 🩺 领域命中较高，容易找到模式切换、节律控制、报警/回退逻辑
- `vehicle` / `automotive` + `ABS/BBW/CACC/platoon/AEB/power steering` + `controller/control system/model/verification`
  - 当前对 🚗 领域命中较高，容易找到控制模式、状态约束、join/leave、制动切换等行为描述
- `PLC` / `IEC 61499` / `IEC 61131` + `control logic/function block/ECC/operation mode`
  - 当前对 🏭 领域有效，尤其适合寻找功能块级控制逻辑与设备运行模式
- `traffic light` / `parking system` / `elevator` + `controller/control system/design`
  - 当前对 🚦、🅿️、🏢 领域有实际收获，适合补充离散事件控制对象
- `elevator control system` + `PLC` + `workflow/traversal/door opening/floor call`
  - 本轮新增结果表明，带 `workflow`、`traversal`、`call button`、`door opening` 的电梯论文更容易直接抽到顺序控制逻辑
- `elevator` / `lift` + `PLC` + `hall call/car call/door obstruction/overload/manual mode`
  - 本轮新增结果表明，带 `hall call`、`car call`、`door obstruction`、`overload sensor`、`manual mode`、`direction state machine` 的电梯论文更容易命中高质量门控与调度逻辑
- `automatic parking` / `parallel parking` + `trajectory/steering/reverse/fuzzy logic`
  - 本轮新增结果表明，带 `parking trajectory`、`steering angle`、`reverse parking` 的自动泊车论文更容易抽到阶段化控制描述
- `automatic parking` / `parallel parking` + `stage 1/stage 2/trigger/HMI`
  - 新增结果表明，带 `Stage 1`、`Stage 2`、`trigger`、`driver aid`、`HMI` 的题名或正文更容易命中可直接复用的泊车阶段切换逻辑
- `automatic parking` / `parallel parking` + `position/direction angle/steering angle/fuzzy controller`
  - 本轮新增结果表明，带 `position`、`direction angle`、`steering angle`、`parking space detection`、`fuzzy inference` 的论文更容易抽到“检测-控制-再检测”的泊车闭环描述
- `water level control` / `tank` + `PLC/float/low level/high level/solenoid valve`
  - 新增结果表明，带 `LL/HL`、`float sensor`、`high level`、`low level`、`pump starts`、`valve opens` 的液位控制论文更容易抽到阈值驱动的顺序控制描述
- `adaptive traffic light` + `phase sequence/queue length/green time`
  - 本轮新增结果表明，带 `phase sequence`、`queue length`、`green time` 的交通灯论文更容易抽到可复用的相位控制逻辑
- `traffic light` + `image processing` + `traffic density/ambulance detection/red green yellow`
  - 本轮新增结果表明，带 `traffic density`、`ambulance detection`、`red green yellow timing`、`camera` 的交通灯论文更容易抽到动态配时控制逻辑
- `traffic light` + `emergency vehicle` + `priority request/GPS/RFID/ETA/green corridor`
  - 新增结果表明，带 `priority request`、`real-time location`、`estimated arrival time`、`override standard pattern`、`green corridor` 的交通灯论文更容易命中应急优先放行逻辑
- `traffic light` + `emergency vehicle` + `RF/RFID/transmitter/receiver/sequence override`
  - 新增结果表明，带 `RF transmission`、`transmitter`、`receiver`、`emergency mode sequence`、`change back to normal sequence` 的论文更容易命中可直接整理的抢占式灯序控制
- `railway interlocking` + `route request/track free/lock/green signal`
  - 本轮新增结果表明，带 `route request`、`track free`、`route locked`、`signals set to green` 的联锁论文更容易直接抽到“请求-检查-锁闭-开放”顺序
- `head tank` / `water level` + `PLC/ultrasonic sensor/motorized valve/solenoid valve/elevation`
  - 新增结果表明，带 `head tank`、`ultrasonic sensor`、`motorized valve`、`solenoid valve`、`41.xx mdpl` 这类阈值表述的论文更容易命中阈值驱动阀控逻辑
- `parallel parking` + `three steps/ready to reverse/scanning/reverse/adjusting forward`
  - 新增结果表明，带 `three steps`、`ready to reverse`、`scanning`、`reversing into the parking space`、`adjusting forward` 的论文更容易命中可直接复用的分阶段泊车控制流程
- `automatic parking assistance` + `exploration phase/parking phase/path shifting points/trajectory`
  - 新增结果表明，带 `exploration phase`、`parking phase`、`parking slot fitment decision`、`path shifting points`、`trajectory` 的 APAS 论文更容易命中阶段化泊车控制描述

### 已观察到的高命中标题/关键词特征

- 标题直接点名具体控制系统客体，而不是泛泛说 framework、architecture、approach。
  - 例如：`Infusion Pump Control System`、`Dual Chamber Pacemaker`、`Elevator Control System`、`Railway Interlocking`、`Traffic Light Controller`、`Landing Gear System`
- 标题同时出现“控制对象 + 控制/控制器 + 设计/规格/验证”三类词。
  - 例如：`... control system`, `... controller`, `design`, `specification`, `verification`, `modeling`
- 标题或关键词中含有明显状态机信号词。
  - 例如：`state machine`, `FSM`, `statechart`, `mode`, `operation mode`, `switching`, `interlocking table`, `control logic`
- 虽然未直接写 `state machine`，但带有“可落到具体控制逻辑”的表达。
  - 例如：`formal specification of ... control system`, `verification of ... controller`, `modeling of ... dynamic responses`
- 标题或摘要中出现顺序控制与流程词，但客体仍是具体控制系统本身。
  - 例如：`workflow`, `traversal`, `route establishment`, `phase sequence`, `door opening`, `parking trajectory`
- 标题或正文里同时出现阈值词和执行器动作词，尤其适合 PLC/液位类系统。
  - 例如：`low level`, `high level`, `float`, `pump starts`, `pump stops`, `solenoid valve`, `timer`
- 标题或正文里出现泊车阶段词和指令词，往往能直接抽到阶段切换逻辑。
  - 例如：`Stage 1`, `Stage 2`, `trigger`, `moving direction`, `steering guide`, `parking possible`
- 标题或正文里出现电梯调度与门控词时，通常容易抽到完整离散控制链。
  - 例如：`hall call`, `car call`, `door operation`, `door obstruction`, `overload sensor`, `collective call scheduling`, `manual mode`
- 标题或正文里出现交通灯密度调度与救护车优先词时，往往能抽到动态配时逻辑。
  - 例如：`traffic density`, `red green yellow`, `ambulance detection`, `camera`, `lane time`, `signal timing`
- 标题或正文里出现应急优先请求和 ETA/GPS/RFID 词时，通常能直接抽到“检测-请求-改灯-恢复”的优先放行链路。
  - 例如：`priority request`, `GPS`, `RFID`, `estimated arrival time`, `override standard pattern`, `green corridor`
- 标题或正文里出现 RF 发射器/接收器和 normal/emergency sequence 切换词时，通常能直接抽到抢占式应急灯序逻辑。
  - 例如：`RF transmission`, `transmitter`, `receiver`, `override sequence`, `emergency mode`, `change back to normal sequence`
- 标题或正文里出现联锁顺序词时，通常能直接抽到进路生命周期控制描述。
  - 例如：`route request`, `track elements free`, `route locked`, `switch positioning`, `signal set to green`
- 标题或正文里出现 head tank 液位阈值和阀门执行词时，通常能直接抽到 PLC 阀控顺序。
  - 例如：`head tank`, `elevation`, `ultrasonic sensor`, `motorized valve`, `solenoid valve`, `41.60 mdpl`, `42.00 mdpl`
- 标题或正文里出现泊车三阶段词时，通常能直接抽到扫描-倒车-前调的阶段控制流程。
  - 例如：`three steps`, `ready to reverse`, `parking space scanning`, `reversing`, `adjusting forward`
- 标题或正文里出现 exploration/parking 两阶段和 path shifting points 词时，通常能直接抽到 APAS 阶段控制逻辑。
  - 例如：`exploration phase`, `parking phase`, `parking slot fitment decision`, `path shifting points`, `trajectory`

### 已观察到的低命中标题/关键词特征

- 过于偏向综述、方法、框架、流程或标准。
  - 例如：`review`, `survey`, `state of the art`, `architecture`, `framework`, `middleware`, `standards landscape`
- 标题中的“状态/模式”并非控制系统运行状态，而是开发流程、工具流程或工程流程。
  - 例如：`development process`, `design process`, `workflow`, `analysis process`
- 只强调安全分析、攻击路径、漏洞知识，而不描述控制对象行为。
  - 例如：`security analysis`, `vulnerability`, `attack`, `knowledge-based system`
- 只讨论通用建模能力或工具链，没有具体控制系统客体。
  - 例如：泛化的 `toolset`, `virtual integration`, `meta-model`, `methodology`
- 虽然出现 `parking`、`trajectory`、`control`，但全文主要停留在连续优化、轨迹平滑或路径规划性能，不给出阶段化停车决策链路。
- 虽然出现 `water level`、`pressure`、`PLC`，但全文若只讨论连续调节性能或硬件组成，而不写阈值触发和执行顺序，也容易低产。

### 检索倾向调整

- 后续搜索应优先沿着“**具体控制对象 + control/controller/system + design/specification/verification/modeling**”这条主线展开，而不是先从宽泛的 `formal methods` 或 `system architecture` 出发。
- 对已经证明高产的对象词应继续深挖同义词、上下位词和子任务词。
  - 例如围绕 `railway interlocking` 继续扩展到 `route locking`, `route release`, `signalling principle`, `level crossing`
  - 例如围绕 `pacemaker` 扩展到 `DDD mode`, `rate control`, `mode switching`
  - 例如围绕 `elevator` 扩展到 `door control`, `group control`, `dispatching`, `operation mode`
  - 例如围绕 `elevator` 进一步扩展到 `hall call`, `car call`, `door obstruction`, `overload sensor`, `manual mode`, `direction state machine`
  - 例如围绕 `parking` 扩展到 `driver aid`, `parking possible`, `Stage 1`, `Stage 2`, `trigger`, `steering guide`
  - 例如围绕 `parking` 进一步扩展到 `position`, `direction angle`, `steering angle`, `parking space detection`, `fuzzy controller`
  - 例如围绕 `water level control` 扩展到 `float sensor`, `low level`, `high level`, `tank cycle`, `fill and drain`, `solenoid valve`
  - 例如围绕 `traffic light` 扩展到 `image processing`, `traffic density`, `red green yellow`, `ambulance detection`, `camera based controller`
  - 例如围绕 `traffic light` 进一步扩展到 `priority request`, `ETA`, `GPS`, `RFID`, `green corridor`, `override standard sequence`
  - 例如围绕 `traffic light` 再扩展到 `RF transmission`, `transmitter`, `receiver`, `emergency mode`, `normal sequence`
  - 例如围绕 `head tank` / `water level` 进一步扩展到 `ultrasonic sensor`, `motorized valve`, `solenoid valve`, `elevation`, `mdpl threshold`
  - 例如围绕 `parallel parking` 进一步扩展到 `three steps`, `ready to reverse`, `parking space scanning`, `adjusting forward`
  - 例如围绕 `automatic parking assistance` 进一步扩展到 `exploration phase`, `parking phase`, `parking slot fitment decision`, `path shifting points`
- 搜索时应尽量遵循本节已有高命中经验，但不能被现有词簇束缚住。
  - 允许并鼓励基于已有 `🟢 直接可用` 论文标题、控制对象名、控制任务名去脑补新的关键词组合
  - 这些新词必须逻辑上能指向“具体控制系统的状态机描述”，而不是泛化方法论文
- 后续每轮更新时，都应根据新增 `🟢 直接可用` 与 `⚪ 未收获` 文献，继续修正本节内容，使检索策略逐步偏向更容易产出有效 STM 的标题词和关键词。

## 当前收录统计

- 已收录论文：**117** 篇
- 本轮新增论文：**3** 篇
- 本轮下载失败记录：**49** 条
- 已完成 STM 梳理：**117** 篇
- ⏳ 尚未提取 STM：**0** 篇
- 本轮新增目录均已包含：PDF 原文、`bibtex.bib`、自动生成的 `paper_content.txt`，并已按 `STM_GUIDE.md` 补齐 `STM.md`。

## 领域 Emoji 口径

- 统一规则：后文 `分类`、`领域`、失败记录分类以及分布统计中的 emoji 全部遵循同一口径；同一个 emoji 在全文只表示一种领域，不再混用“领域”和“方法/质量属性”含义。

| Emoji | 统一含义 |
|---|---|
| 🚗 | 汽车与道路车辆控制 |
| 🚆 | 轨道交通与铁路控制 |
| ✈️ | 航空航天与飞行/空管控制 |
| 🩺 | 医疗设备与生命支持控制 |
| 🏭 | 工业自动化与离散制造 |
| 🏢 | 楼宇机电与电梯控制 |
| 🌡️ | 过程与环境控制 |
| 🚦 | 道路交通信号控制 |
| 🅿️ | 智慧停车与车位管理 |
| 🧩 | 建模方法与系统工程 |
| 🔐 | 安全/安保分析 |
| ⚙️ | 通用控制与形式化工具 |

## 论文清单

### 领域分布（按论文篇数统计）

- 统计口径：按 `## 论文清单` 中已收录的 **117** 篇论文统计；所用 emoji 与上方“领域 Emoji 口径”完全一致。

| 领域 | 篇数 | 占比 | 说明 |
|---|---:|---:|---|
| 🚗 汽车与道路车辆控制 | 23 | 19.7% | ACC/CACC、ABS/BBW、AEB、转向、车队与自动驾驶相关控制 |
| 🚆 轨道交通与铁路控制 | 17 | 14.5% | 联锁表、进路控制、平交口、车门等轨道交通控制与验证 |
| ✈️ 航空航天与飞行/空管控制 | 10 | 8.5% | 无人机、起落架、飞机制动、空管协调协议等 |
| 🩺 医疗设备与生命支持控制 | 5 | 4.3% | 起搏器、输液泵、医疗 CPS 与闭环治疗控制相关文献 |
| 🏭 工业自动化与离散制造 | 11 | 9.4% | IEC 61499/61131、PLC、制造、分拣、机器人等工业自动化控制 |
| 🏢 楼宇机电与电梯控制 | 13 | 11.1% | 单梯/群梯控制、门控与楼宇机电交互逻辑 |
| 🌡️ 过程与环境控制 | 5 | 4.3% | 液位、水处理、锅炉与批处理等过程/环境控制 |
| 🚦 道路交通信号控制 | 11 | 9.4% | 交通灯相位控制、绿灯分配、紧急车辆优先放行 |
| 🅿️ 智慧停车与车位管理 | 11 | 9.4% | 自动停车、车位分配、车位监测与停车控制 |
| 🧩 建模方法与系统工程 | 4 | 3.4% | SysML/MDE/MBT/架构虚拟集成等方法与过程类文献 |
| 🔐 安全/安保分析 | 4 | 3.4% | CPS/ICS 安全分析、安全切片、secure-by-design 等 |
| ⚙️ 通用控制与形式化工具 | 3 | 2.6% | 混成系统、实时系统、通用控制工具与基础形式化文献 |
| **合计** | **117** | **100.0%** | - |

### 更新日志

| 时间 | 更新内容 | 检索策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-11 23:21:28 | 新增 **3** 篇，当前累计 **117** 篇 | 继续沿高命中主线深挖 `traffic light + emergency vehicle + RF/RFID + override sequence` 与 `automatic parking assistance + exploration phase + parking phase + path shifting points` 等组合，并优先保留可直链下载 PDF 的开放文献。 | RFID/RF 抢占式交通灯控制、低成本 APAS 两阶段泊车辅助。 |
| 2026-03-11 23:09:54 | 新增 **5** 篇，当前累计 **114** 篇 | 在既有高命中主线上继续深挖 `traffic light + emergency vehicle + priority request + ETA/GPS/RFID`、`head tank + ultrasonic sensor + motorized valve + solenoid valve`、`parallel parking + three steps + ready to reverse`、`ERTMS + train spacing + RBS` 等组合。 | 应急车辆优先放行、头水箱液位阈值阀控、三阶段并联泊车、ERTMS 列车间隔控制。 |
| 2026-03-11 22:43:00 | 新增 **12** 篇，当前累计 **109** 篇 | 在既有 `具体控制对象 + control/controller/system + design/specification/verification/modeling` 主线上，重点追加 `elevator + hall call/car call/door obstruction/overload`、`traffic light + image processing + traffic density + ambulance detection`、`railway interlocking + route request + lock + green`、`parking + position/direction angle + steering angle`、`water level + float switch + threshold` 等高命中词簇。 | 电梯 PLC 调度与门控、图像驱动交通灯配时、联锁进路顺序、模糊泊车闭环、水位阈值控制。 |
| 2026-03-11 22:07:39 | 新增 **3** 篇，当前累计 **97** 篇 | 沿用 `具体控制对象 + control/controller/system + design/specification/verification/modeling` 主线，并进一步加强 `water level + PLC + float + low/high level`、`parallel parking + stage/trigger/HMI`、`auto parking + parking possible + steering law` 等高命中词簇。 | 水箱液位控制、分阶段并联泊车辅助、自动泊车轨迹生成。 |
| 2026-03-11 21:45:03 | 新增 **6** 篇，当前累计 **94** 篇 | 继续沿用 `具体控制对象 + control/controller/system + design/specification/verification/modeling` 主线，并进一步强化 `railway interlocking + route establishment`、`elevator + PLC + workflow/traversal`、`parallel parking + trajectory/steering`、`adaptive traffic light + phase sequence/green time` 等扩展词簇。 | 法国铁路联锁、PLC 电梯控制、自适应交通灯控制、并联泊车控制。 |
| 2026-03-11 19:52:53 | 新增 **58** 篇，当前累计 **88** 篇 | 基于 `BASELINE.md` 中 `ALL-IN-ONE 综合检索关键词`，按“控制对象/系统类型 + design/requirements/specification/modeling/verification + state machine/FSM/statechart/formal method”等组合继续扩展检索，并优先保留可直接获取 PDF 与较完整 BibTeX 的开放文献。 | 铁路联锁与轨交控制、医疗设备闭环控制、车载控制（ACC/ABS/BBW/车队协同）、PLC/电梯/交通灯/停车控制，以及无人机/飞控/起落架等航空航天控制。 |

| # | 分类 | 标题 | 年份 | 主题 | 关键词 | 目录 |
|---|---|---|---:|---|---|---|
| 1 | ⚙️ | HyTech: A model checker for hybrid systems | 1997 | 混成系统验证 | `hybrid systems, model checker, formal verification` | [hytech-hybrid-systems](sources/hytech-hybrid-systems/) |
| 2 | 🏭 | A formal validation approach for holonic control system specifications | 2004 | Holonic控制规格验证 | `holonic control systems, formal validation, specifications` | [holonic-control-validation](sources/holonic-control-validation/) |
| 3 | 🩺 | Formal specifications and analysis of the computer-assisted resuscitation algorithm (CARA) Infusion Pump Control System | 2004 | 医疗控制系统规格 | `infusion pump, formal specification, control system` | [cara-infusion-pump-formal-spec](sources/cara-infusion-pump-formal-spec/) |
| 4 | ⚙️ | The TASM Toolset: Specification, Simulation, and Formal Verification of Real-Time Systems | 2007 | 实时系统工具链 | `real-time systems, specification, simulation, formal verification` | [tasm-toolset](sources/tasm-toolset/) |
| 5 | 🧩 | System Architecture Virtual Integration: An Industrial Case Study | 2009 | 工业案例虚拟集成 | `system architecture, virtual integration, industrial case study` | [system-architecture-virtual-integration](sources/system-architecture-virtual-integration/) |
| 6 | 🔐 | SafeSlice | 2011 | 安全分析切片 | `safety analysis, slicing, model-based` | [safeslice](sources/safeslice/) |
| 7 | 🏭 | Towards a Model-Driven IEC 61131-Based Development Process in Industrial Automation | 2011 | IEC 61131开发流程 | `IEC 61131, model-driven, industrial automation` | [model-driven-iec61131-development](sources/model-driven-iec61131-development/) |
| 8 | 🩺 | Modeling and Verification of a Dual Chamber Implantable Pacemaker | 2012 | 医疗设备状态建模 | `pacemaker, modeling, verification, medical CPS` | [dual-chamber-pacemaker](sources/dual-chamber-pacemaker/) |
| 9 | 🚗 | ViTAL: A Verification Tool for EAST-ADL Models Using UPPAAL PORT | 2012 | EAST-ADL验证工具 | `EAST-ADL, UPPAAL, verification tool` | [vital-east-adl-uppaal](sources/vital-east-adl-uppaal/) |
| 10 | 🚗 | A methodology for formal analysis and verification of EAST-ADL models | 2013 | 汽车体系结构验证 | `EAST-ADL, formal verification, automotive` | [east-adl-formal-analysis](sources/east-adl-formal-analysis/) |
| 11 | 🏭 | IEC 61499 vs. 61131: A Comparison Based on Misperceptions | 2013 | 控制标准对比 | `IEC 61499, IEC 61131, comparison` | [iec61499-vs-61131](sources/iec61499-vs-61131/) |
| 12 | 🧩 | Industrial-Strength Model-Based Testing - State of the Art and Current Challenges | 2013 | 工业级模型测试 | `model-based testing, industrial systems, state of the art` | [industrial-strength-mbt](sources/industrial-strength-mbt/) |
| 13 | 🧩 | On the Use of SysML Models in the Construction of the Design Process for Safety-Critical Systems | 2013 | SysML设计过程 | `SysML, safety-critical systems, design process` | [sysml-safety-critical-design-process](sources/sysml-safety-critical-design-process/) |
| 14 | 🧩 | Safety analysis integration in a SysML-based complex system design process | 2013 | SysML安全分析 | `SysML, safety analysis, complex systems` | [sysml-safety-analysis-integration](sources/sysml-safety-analysis-integration/) |
| 15 | 🩺 | Design Pillars for Medical Cyber-Physical System Middleware | 2014 | 医疗CPS中间件 | `medical CPS, middleware, design` | [design-pillars-medical-cps](sources/design-pillars-medical-cps/) |
| 16 | 🚗 | Model-checking and Model-based Testing of Automotive Embedded Systems : Starting from the System Architecture | 2014 | 汽车系统模型测试 | `automotive embedded systems, model checking, model-based testing` | [automotive-mbt-thesis](sources/automotive-mbt-thesis/) |
| 17 | 🏭 | Time-Complemented Event-Driven Architecture for Distributed Automation Systems | 2014 | 分布式自动化架构 | `distributed automation systems, event-driven architecture, time-aware` | [time-complemented-automation-architecture](sources/time-complemented-automation-architecture/) |
| 18 | 🔐 | Towards the Model-Driven Engineering of Secure yet Safe Embedded Systems | 2014 | 安全与安保建模 | `embedded systems, security, safety, model-driven engineering` | [secure-safe-embedded-mde](sources/secure-safe-embedded-mde/) |
| 19 | 🏭 | A real-time semantics for the IEC 61499 standard | 2015 | IEC 61499实时语义 | `IEC 61499, real-time semantics, automation` | [iec61499-realtime-semantics](sources/iec61499-realtime-semantics/) |
| 20 | 🔐 | Extracting Vulnerabilities in Industrial Control Systems using a Knowledge-Based System | 2015 | 工业控制系统知识建模 | `industrial control systems, knowledge-based system, vulnerabilities` | [ics-vulnerability-knowledge-base](sources/ics-vulnerability-knowledge-base/) |
| 21 | 🏭 | Service-Oriented Architecture in Industrial Automation Systems - The case of IEC 61499: A Review | 2015 | IEC 61499综述 | `IEC 61499, SOA, industrial automation` | [iec61499-soa-review](sources/iec61499-soa-review/) |
| 22 | 🏭 | Current Standards Landscape for Smart Manufacturing Systems | 2016 | 智能制造标准 | `smart manufacturing, standards, NIST` | [smart-manufacturing-standards-nist](sources/smart-manufacturing-standards-nist/) |
| 23 | 🏭 | Fault Handling in PLC-Based Industry 4.0 Automated Production Systems as a Basis for Restart and Self-Configuration and Its Evaluation | 2016 | PLC故障处理 | `PLC, Industry 4.0, fault handling, self-configuration` | [fault-handling-plc-industry4](sources/fault-handling-plc-industry4/) |
| 24 | 🚗 | Model-driven Analysis and Verification of Automotive Embedded Systems | 2016 | 汽车嵌入式系统分析 | `automotive embedded systems, model-driven analysis, verification` | [automotive-analysis-thesis](sources/automotive-analysis-thesis/) |
| 25 | ✈️ | AVENS - A Novel Flying Ad Hoc Network Simulator with Automatic Code Generation for Unmanned Aircraft System | 2017 | 无人机系统建模 | `unmanned aircraft system, simulator, code generation` | [avens-uas](sources/avens-uas/) |
| 26 | 🏭 | Modularity and architecture of PLC-based software for automated production Systems: An analysis in industrial companies | 2017 | PLC软件架构 | `PLC, modularity, architecture, production systems` | [plc-software-modularity](sources/plc-software-modularity/) |
| 27 | 🔐 | A model-based approach to security analysis for cyber-physical systems | 2018 | CPS安全分析 | `cyber-physical systems, security analysis, model-based` | [cps-security-analysis-sysml](sources/cps-security-analysis-sysml/) |
| 28 | 🚗 | Benchmarks for Temporal Logic Requirements for Automotive Systems | 2018 | 汽车需求基准 | `automotive, temporal logic, requirements` | [automotive-temporal-logic-benchmarks](sources/automotive-temporal-logic-benchmarks/) |
| 29 | 🏭 | Teaching Finite State Machines (FSMs) as Part of a Programmable Logic Control (PLC) Course | 2018 | PLC课程FSM | `FSM, PLC, teaching` | [plc-course-fsm](sources/plc-course-fsm/) |
| 30 | ✈️ | Exploring SysML v2 for Model-Based Engineering of Safety-Critical Avionics Systems | 2024 | SysML v2航空电子 | `SysML v2, avionics, safety-critical systems` | [sysmlv2-avionics](sources/sysmlv2-avionics/) |
| 31 | 🏭 | Adaptive control of robot manipulators with flexible joints | 1992 | 机器人与执行机构控制 | `robot manipulator, flexible joints, adaptive control` | [adaptive-control-of-robot-manipulators-with-flexible-joints](sources/adaptive-control-of-robot-manipulators-with-flexible-joints/) |
| 32 | 🚗 | Autonomous intelligent cruise control | 1993 | 车载控制与驾驶辅助 | `autonomous intelligent cruise control, vehicle control` | [autonomous-intelligent-cruise-control](sources/autonomous-intelligent-cruise-control/) |
| 33 | 🏢 | Elevator Group Control Using Multiple Reinforcement Learning Agents | 1998 | 工业自动化与离散事件控制 | `elevator group control, reinforcement learning, scheduling` | [elevator-group-control-using-multiple-reinforcement-learning-agents](sources/elevator-group-control-using-multiple-reinforcement-learning-agents/) |
| 34 | 🚆 | Formal modelling and simulation of train control systems using petri nets | 1999 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [formal-modelling-and-simulation-of-train-control-systems-using-petri-net](sources/formal-modelling-and-simulation-of-train-control-systems-using-petri-net/) |
| 35 | ✈️ | Modeling and Validation of a Navy A6-Intruder Actively Controlled Landing Gear System | 1999 | 航空航天与空管控制 | `landing gear system, active control, validation` | [modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin](sources/modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin/) |
| 36 | 🚆 | USING Z SPECIFICATION FOR RAILWAY INTERLOCKING SAFETY | 2001 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [using-z-specification-for-railway-interlocking-safety](sources/using-z-specification-for-railway-interlocking-safety/) |
| 37 | 🏢 | Multi Car Elevator Control by using Learning Automaton | 2005 | 工业自动化与离散事件控制 | `elevator control, learning automaton, multi-car` | [multi-car-elevator-control-by-using-learning-automaton](sources/multi-car-elevator-control-by-using-learning-automaton/) |
| 38 | 🚆 | A formal approach for the construction and verification of railway control systems | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [a-formal-approach-for-the-construction-and-verification-of-railway-contr](sources/a-formal-approach-for-the-construction-and-verification-of-railway-contr/) |
| 39 | 🚆 | Automated Verification of Signalling Principles in Railway Interlocking Systems | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [automated-verification-of-signalling-principles-in-railway-interlocking](sources/automated-verification-of-signalling-principles-in-railway-interlocking/) |
| 40 | 🚆 | Automatic generation and verification of railway interlocking control tables using FSM and NuSMV | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [automatic-generation-and-verification-of-railway-interlocking-control-ta](sources/automatic-generation-and-verification-of-railway-interlocking-control-ta/) |
| 41 | ✈️ | 3D pose estimation based on planar object tracking for UAVs control | 2010 | 无人机与飞行控制 | `UAV control, pose estimation, planar tracking` | [3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control](sources/3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control/) |
| 42 | 🚆 | Modelling Railway Interlocking Tables Using Coloured Petri Nets | 2010 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [modelling-railway-interlocking-tables-using-coloured-petri-nets](sources/modelling-railway-interlocking-tables-using-coloured-petri-nets/) |
| 43 | ⚙️ | Nonlinear controller design of a ship autopilot | 2010 | 船舶与通用控制系统 | `ship autopilot, nonlinear control` | [nonlinear-controller-design-of-a-ship-autopilot](sources/nonlinear-controller-design-of-a-ship-autopilot/) |
| 44 | ✈️ | On-board and Ground Visual Pose Estimation Techniques for UAV Control | 2010 | 无人机与飞行控制 | `UAV control, visual pose estimation` | [on-board-and-ground-visual-pose-estimation-techniques-for-uav-control](sources/on-board-and-ground-visual-pose-estimation-techniques-for-uav-control/) |
| 45 | ✈️ | Formal Specification and Verification of a Coordination Protocol for an Automated Air Traffic Control System | 2012 | 航空航天与空管控制 | `air traffic control, coordination protocol, formal verification` | [formal-specification-and-verification-of-a-coordination-protocol-for-an](sources/formal-specification-and-verification-of-a-coordination-protocol-for-an/) |
| 46 | 🏢 | Marginalizing Out Future Passengers in Group Elevator Control | 2012 | 工业自动化与离散事件控制 | `elevator group control, passenger modeling, scheduling` | [marginalizing-out-future-passengers-in-group-elevator-control](sources/marginalizing-out-future-passengers-in-group-elevator-control/) |
| 47 | 🚗 | Cooperative Adaptive Cruise Control in Real Traffic Situations | 2013 | 车载控制与驾驶辅助 | `cooperative adaptive cruise control, real traffic, vehicle platoon` | [cooperative-adaptive-cruise-control-in-real-traffic-situations](sources/cooperative-adaptive-cruise-control-in-real-traffic-situations/) |
| 48 | 🚗 | Experimental verification of vehicle platoon control algorithms | 2013 | 车载控制与驾驶辅助 | `vehicle platoon, control algorithms, experimental verification` | [experimental-verification-of-vehicle-platoon-control-algorithms](sources/experimental-verification-of-vehicle-platoon-control-algorithms/) |
| 49 | 🚆 | Online predictive diagnosis of electrical train door systems | 2013 | 铁路与轨道交通设备控制 | `train door system, predictive diagnosis, electrical systems` | [online-predictive-diagnosis-of-electrical-train-door-systems](sources/online-predictive-diagnosis-of-electrical-train-door-systems/) |
| 50 | 🚗 | Reactive approach for autonomous vehicle platoon systems (modelling and verification) | 2013 | 车载控制与驾驶辅助 | `vehicle platoon, reactive systems, modelling and verification` | [reactive-approach-for-autonomous-vehicle-platoon-systems-modelling-and-v](sources/reactive-approach-for-autonomous-vehicle-platoon-systems-modelling-and-v/) |
| 51 | 🚗 | Adaptive Cascade Control of a Brake-By-Wire Actuator for Sport Motorcycles | 2014 | 车载控制与驾驶辅助 | `brake-by-wire, actuator control, motorcycle` | [adaptive-cascade-control-of-a-brake-by-wire-actuator-for-sport-motorcycl](sources/adaptive-cascade-control-of-a-brake-by-wire-actuator-for-sport-motorcycl/) |
| 52 | 🚆 | Architecture description language for Cyber Physical Systems analysis: a railway control system case study | 2014 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [architecture-description-language-for-cyber-physical-systems-analysis-a](sources/architecture-description-language-for-cyber-physical-systems-analysis-a/) |
| 53 | 🩺 | Automated Verification of Quantitative Properties of Cardiac Pacemaker Software | 2014 | 医疗设备与闭环治疗控制 | `medical device, closed-loop control, verification` | [automated-verification-of-quantitative-properties-of-cardiac-pacemaker-s](sources/automated-verification-of-quantitative-properties-of-cardiac-pacemaker-s/) |
| 54 | 🩺 | Developing and Verifying User Interface Requirements for Infusion Pumps: A Refinement Approach | 2014 | 医疗设备与闭环治疗控制 | `medical device, closed-loop control, verification` | [developing-and-verifying-user-interface-requirements-for-infusion-pumps](sources/developing-and-verifying-user-interface-requirements-for-infusion-pumps/) |
| 55 | 🚗 | Modeling cooperative and autonomous adaptive cruise control dynamic responses using experimental data | 2014 | 车载控制与驾驶辅助 | `adaptive cruise control, dynamic response, experimental data` | [modeling-cooperative-and-autonomous-adaptive-cruise-control-dynamic-resp](sources/modeling-cooperative-and-autonomous-adaptive-cruise-control-dynamic-resp/) |
| 56 | 🚗 | Performance Evaluation of an Anti-Lock Braking System for Electric Vehicles with a Fuzzy Sliding Mode Controller | 2014 | 车载控制与驾驶辅助 | `anti-lock braking system, electric vehicle, fuzzy sliding mode` | [performance-evaluation-of-an-anti-lock-braking-system-for-electric-vehic](sources/performance-evaluation-of-an-anti-lock-braking-system-for-electric-vehic/) |
| 57 | 🚦 | High accuracy traffic light controller for increasing the given green time utilization | 2015 | 工业自动化与离散事件控制 | `traffic light controller, green time, traffic control` | [high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti](sources/high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti/) |
| 58 | ✈️ | The landing gear system in multi-machine Hybrid Event-B | 2015 | 航空航天与空管控制 | `landing gear system, Hybrid Event-B, formal model` | [the-landing-gear-system-in-multi-machine-hybrid-event-b](sources/the-landing-gear-system-in-multi-machine-hybrid-event-b/) |
| 59 | ✈️ | UAV Control on the Basis of 3D Landmark Bearing-Only Observations | 2015 | 无人机与飞行控制 | `UAV control, landmark observations, bearing-only` | [uav-control-on-the-basis-of-3d-landmark-bearing-only-observations](sources/uav-control-on-the-basis-of-3d-landmark-bearing-only-observations/) |
| 60 | 🚆 | Verification of railway interlocking systems | 2015 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [verification-of-railway-interlocking-systems](sources/verification-of-railway-interlocking-systems/) |
| 61 | 🚆 | Bond Graph modeling for fault detection and isolation of a train door mechatronic system | 2016 | 铁路与轨道交通设备控制 | `train door system, fault detection, bond graph` | [bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me](sources/bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me/) |
| 62 | 🚆 | Validation process for railway interlocking systems | 2016 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [validation-process-for-railway-interlocking-systems](sources/validation-process-for-railway-interlocking-systems/) |
| 63 | 🏢 | Design &amp; Control of an Elevator Control System using PLC | 2017 | 工业自动化与离散事件控制 | `elevator control, PLC, automation` | [design-amp-control-of-an-elevator-control-system-using-plc](sources/design-amp-control-of-an-elevator-control-system-using-plc/) |
| 64 | 🚗 | Formal verification of autonomous vehicle platooning | 2017 | 车载控制与驾驶辅助 | `autonomous vehicle platooning, formal verification` | [formal-verification-of-autonomous-vehicle-platooning](sources/formal-verification-of-autonomous-vehicle-platooning/) |
| 65 | 🚗 | Integrated Longitudinal and Lateral Networked Control System Design for Vehicle Platooning | 2018 | 车载控制与驾驶辅助 | `vehicle platooning, longitudinal control, lateral control` | [integrated-longitudinal-and-lateral-networked-control-system-design-for](sources/integrated-longitudinal-and-lateral-networked-control-system-design-for/) |
| 66 | 🏢 | Intelligent elevator control and safety monitoring system | 2018 | 工业自动化与离散事件控制 | `elevator control, safety monitoring, intelligent system` | [intelligent-elevator-control-and-safety-monitoring-system](sources/intelligent-elevator-control-and-safety-monitoring-system/) |
| 67 | 🚗 | Networked Cooperative Platoon of Vehicles for Testing Methods and Verification Tools | 2018 | 车载控制与驾驶辅助 | `vehicle platoon, testing methods, verification tools` | [networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi](sources/networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi/) |
| 68 | 🚦 | Automatic traffic light controller for emergency vehicle using peripheral interface controller | 2019 | 工业自动化与离散事件控制 | `traffic light controller, emergency vehicle, PIC` | [automatic-traffic-light-controller-for-emergency-vehicle-using-periphera](sources/automatic-traffic-light-controller-for-emergency-vehicle-using-periphera/) |
| 69 | 🌡️ | Features of Automatic Control of Technological Parameters of Water Level in the Drum Steam Boilers | 2019 | 工业自动化与离散事件控制 | `steam boiler, water level control, automatic control` | [features-of-automatic-control-of-technological-parameters-of-water-level](sources/features-of-automatic-control-of-technological-parameters-of-water-level/) |
| 70 | 🚗 | Fuzzy Sliding Mode Wheel Slip Ratio Control for Smart Vehicle Anti-Lock Braking System | 2019 | 车载控制与驾驶辅助 | `anti-lock braking system, wheel slip, fuzzy sliding mode` | [fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock](sources/fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock/) |
| 71 | 🚗 | Modular Verification of Vehicle Platooning with Respect to Decisions, Space and Time | 2019 | 车载控制与驾驶辅助 | `vehicle platooning, modular verification, space and time` | [modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa](sources/modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa/) |
| 72 | 🚗 | Research on Longitudinal Active Collision Avoidance of Autonomous Emergency Braking Pedestrian System (AEB-P) | 2019 | 车载控制与驾驶辅助 | `autonomous emergency braking, collision avoidance, pedestrian` | [research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge](sources/research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge/) |
| 73 | 🌡️ | Water Tank Level Controller by using PLC | 2019 | 工业自动化与离散事件控制 | `water tank level control, PLC, controller` | [water-tank-level-controller-by-using-plc](sources/water-tank-level-controller-by-using-plc/) |
| 74 | 🅿️ | Data Efficient Reinforcement Learning for Integrated Lateral Planning and Control in Automated Parking System | 2020 | 智能停车与感知控制 | `automated parking system, planning, lateral control` | [data-efficient-reinforcement-learning-for-integrated-lateral-planning-an](sources/data-efficient-reinforcement-learning-for-integrated-lateral-planning-an/) |
| 75 | 🚆 | Information Value-Based Fault Diagnosis of Train Door System under Multiple Operating Conditions | 2020 | 铁路与轨道交通设备控制 | `train door system, fault diagnosis, operating conditions` | [information-value-based-fault-diagnosis-of-train-door-system-under-multi](sources/information-value-based-fault-diagnosis-of-train-door-system-under-multi/) |
| 76 | 🚗 | Review on the Development, Control Method and Application Prospect of Brake-by-Wire Actuator | 2020 | 车载控制与驾驶辅助 | `brake-by-wire actuator, review, control method` | [review-on-the-development-control-method-and-application-prospect-of-bra](sources/review-on-the-development-control-method-and-application-prospect-of-bra/) |
| 77 | 🚗 | Sliding Mode Control Algorithms for Anti-Lock Braking Systems with Performance Comparisons | 2020 | 车载控制与驾驶辅助 | `anti-lock braking system, sliding mode control, comparison` | [sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo](sources/sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo/) |
| 78 | 🅿️ | Video-Based Parking Occupancy Detection for Smart Control System | 2020 | 智能停车与感知控制 | `parking control system, occupancy detection, video-based` | [video-based-parking-occupancy-detection-for-smart-control-system](sources/video-based-parking-occupancy-detection-for-smart-control-system/) |
| 79 | ✈️ | An Industrial Quadrotor UAV Control Method Based on Fuzzy Adaptive Linear Active Disturbance Rejection Control | 2021 | 无人机与飞行控制 | `quadrotor UAV, fuzzy adaptive control, ADRC` | [an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea](sources/an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea/) |
| 80 | 🚦 | Intelligent Traffic Light Controller using Fuzzy Logic and Image Processing | 2021 | 工业自动化与离散事件控制 | `traffic light controller, fuzzy logic, image processing` | [intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process](sources/intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process/) |
| 81 | 🚗 | Performance Assessment of an Electric Power Steering System for Driverless Formula Student Vehicles | 2021 | 车载控制与驾驶辅助 | `electric power steering, driverless vehicle, performance assessment` | [performance-assessment-of-an-electric-power-steering-system-for-driverle](sources/performance-assessment-of-an-electric-power-steering-system-for-driverle/) |
| 82 | 🚦 | Traffic Light Controller using Image Processing | 2021 | 工业自动化与离散事件控制 | `traffic light controller, image processing, embedded control` | [traffic-light-controller-using-image-processing](sources/traffic-light-controller-using-image-processing/) |
| 83 | 🚆 | Formal Modeling and Verification of the Functionality of Electronic Urban Railway Control Systems Through a Case Study | 2022 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [formal-modeling-and-verification-of-the-functionality-of-electronic-urba](sources/formal-modeling-and-verification-of-the-functionality-of-electronic-urba/) |
| 84 | 🅿️ | Research on Path Planning and Tracking Control of Automatic Parking System | 2022 | 工业自动化与离散事件控制 | `automatic parking system, path planning, tracking control` | [research-on-path-planning-and-tracking-control-of-automatic-parking-syst](sources/research-on-path-planning-and-tracking-control-of-automatic-parking-syst/) |
| 85 | 🚗 | Review of Brake-by-Wire System and Control Technology | 2022 | 车载控制与驾驶辅助 | `brake-by-wire system, control technology, review` | [review-of-brake-by-wire-system-and-control-technology](sources/review-of-brake-by-wire-system-and-control-technology/) |
| 86 | 🅿️ | A Smart Real-Time Parking Control and Monitoring System | 2023 | 工业自动化与离散事件控制 | `parking control system, monitoring, real-time` | [a-smart-real-time-parking-control-and-monitoring-system](sources/a-smart-real-time-parking-control-and-monitoring-system/) |
| 87 | 🚗 | Design and Assessment of an Anti-lock Braking System Controller | 2023 | 车载控制与驾驶辅助 | `anti-lock braking system, controller design, assessment` | [design-and-assessment-of-an-anti-lock-braking-system-controller](sources/design-and-assessment-of-an-anti-lock-braking-system-controller/) |
| 88 | ✈️ | Model-Based Design of Aircraft Landing Gear System | 2023 | 航空航天与空管控制 | `aircraft landing gear, model-based design, control` | [model-based-design-of-aircraft-landing-gear-system](sources/model-based-design-of-aircraft-landing-gear-system/) |
| 89 | 🚆 | A formal modeling methodology of the French railway interlocking system via HCPN | 2014 | 铁路联锁与进路建立控制 | `railway interlocking, HCPN, route establishment, signaling control` | [french-railway-interlocking-hcpn](sources/french-railway-interlocking-hcpn/) |
| 90 | 🏢 | PLC based Multi-Floor Elevator Control System | 2015 | 多层电梯 PLC 遍历控制 | `elevator control, PLC, multi-floor, traversal` | [plc-based-multi-floor-elevator-control-system](sources/plc-based-multi-floor-elevator-control-system/) |
| 91 | 🚦 | Development and Simulation of Adaptive Traffic Light Controller Using Artificial Bee Colony Algorithm | 2018 | 自适应交通灯相位调度 | `traffic light controller, adaptive scheduling, phase sequence, green time` | [adaptive-traffic-light-controller-using-artificial-bee-colony](sources/adaptive-traffic-light-controller-using-artificial-bee-colony/) |
| 92 | 🏢 | Design of PLC based Elevator Control System | 2019 | 四层电梯呼梯与门控流程 | `elevator control, PLC, call button, door control` | [design-of-plc-based-elevator-control-system](sources/design-of-plc-based-elevator-control-system/) |
| 93 | 🅿️ | Parallel Parking System Design with Fuzzy Logic Control | 2021 | 自动泊车轨迹与转向控制 | `parallel parking, fuzzy logic, steering control, parking trajectory` | [parallel-parking-system-design-with-fuzzy-logic-control](sources/parallel-parking-system-design-with-fuzzy-logic-control/) |
| 94 | 🏢 | Design of Elevator Control System Based on PLC | 2023 | 电梯工作流与自动/手动模式 | `elevator control system, PLC, workflow, manual operation` | [design-of-elevator-control-system-based-on-plc](sources/design-of-elevator-control-system-based-on-plc/) |
| 95 | 🌡️ | Automatic Water Level and Pressure Control System Prototype Design Using Programmable Logic Controller and Human Machine Interface | 2023 | 液位阈值与排水循环控制 | `water level control, PLC, float sensor, low level, high level, solenoid valve` | [automatic-water-level-and-pressure-control-system-prototype](sources/automatic-water-level-and-pressure-control-system-prototype/) |
| 96 | 🅿️ | Development of a Hierarchical Driver Aid for Parallel Parking Using Fuzzy Biomimetic Approach | 2010 | 分阶段并联泊车辅助 | `parallel parking, driver aid, fuzzy logic, stage 1, stage 2, HMI` | [hierarchical-driver-aid-for-parallel-parking](sources/hierarchical-driver-aid-for-parallel-parking/) |
| 97 | 🅿️ | An Intelligent Auto Parking System for Vehicles | 2012 | 自动泊车轨迹生成与可停判定 | `auto parking system, fuzzy logic, parking possible, steering law, trajectory generation` | [intelligent-auto-parking-system-for-vehicles](sources/intelligent-auto-parking-system-for-vehicles/) |
| 98 | 🏢 | Application of PLC for Elevator Control System | 2011 | 单梯呼梯与到层停靠控制 | `elevator control, PLC, forward reverse, limit switch` | [application-of-plc-for-elevator-control-system](sources/application-of-plc-for-elevator-control-system/) |
| 99 | 🏢 | PLC Controlling Program of an Elevator | 2020 | 五层电梯同向优先与门控安全 | `elevator control, PLC, call buttons, obstacle sensor, overload` | [plc-controlling-program-of-an-elevator](sources/plc-controlling-program-of-an-elevator/) |
| 100 | 🏢 | PLC Controlled Elevator System using XC1 PLC through Ladder Programming | 2019 | 同向优先电梯调度 | `elevator control, XC1 PLC, ladder programming, up calls, down calls` | [plc-controlled-elevator-system-using-xc1-plc-through-ladder-programming](sources/plc-controlled-elevator-system-using-xc1-plc-through-ladder-programming/) |
| 101 | 🏢 | PLC-Based Intelligent Control System for Four-Floor Elevator | 2025 | 四层电梯方向状态机与门控联锁 | `elevator control, direction state machine, car call, hall call, door obstruction` | [plc-based-intelligent-control-system-for-four-floor-elevator](sources/plc-based-intelligent-control-system-for-four-floor-elevator/) |
| 102 | 🏢 | Design of a PLC Based Elevator Control System | 2015 | 电梯空闲开门与上下行指示逻辑 | `elevator control, PLC, hall call, car call, auto door` | [design-of-a-plc-based-elevator-control-system](sources/design-of-a-plc-based-elevator-control-system/) |
| 103 | 🚦 | Automatic Traffic Using Image Processing | 2017 | 基于车流计数的交通灯配时 | `traffic light, image processing, vehicle counting, signal timing` | [automatic-traffic-using-image-processing](sources/automatic-traffic-using-image-processing/) |
| 104 | 🚦 | Intelligent Traffic Light Control System Based on Image Processing | 2023 | 四车道密度与救护车检测配时 | `traffic light, image processing, traffic density, ambulance detection` | [intelligent-traffic-light-control-system-based-on-image-processing](sources/intelligent-traffic-light-control-system-based-on-image-processing/) |
| 105 | 🚆 | Some Experiences on Formal Specification of Railway Interlocking Systems using Statecharts | 2005 | 联锁进路请求与锁闭顺序 | `railway interlocking, statecharts, route request, lock, green signal` | [some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts](sources/some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts/) |
| 106 | 🚆 | Modelling Interlocking Systems for Railway Stations | 2008 | 联锁建模与验证方法 | `railway interlocking, route table, verification, thesis` | [modelling-interlocking-systems-for-railway-stations](sources/modelling-interlocking-systems-for-railway-stations/) |
| 107 | 🌡️ | PLC Based Water Level Control System | 2020 | 多浮球液位阈值启停控制 | `water level control, PLC, float switch, threshold, pump motor` | [plc-based-water-level-control-system](sources/plc-based-water-level-control-system/) |
| 108 | 🅿️ | Fuzzy Controller-Based Design and Simulation of an Automatic Parking System | 2023 | 位置/方向角驱动的模糊泊车闭环 | `automatic parking, fuzzy controller, position, direction angle, steering angle` | [fuzzy-controller-based-design-and-simulation-of-an-automatic-parking-system](sources/fuzzy-controller-based-design-and-simulation-of-an-automatic-parking-system/) |
| 109 | 🅿️ | Design and Simulation of Small Space Parallel Parking Fuzzy Controller | 2015 | 小空间并联泊车检测与倒车控制 | `parallel parking, fuzzy control, parking space detection, Ackerman angle` | [design-and-simulation-of-small-space-parallel-parking-fuzzy-controller](sources/design-and-simulation-of-small-space-parallel-parking-fuzzy-controller/) |
| 110 | 🚆 | Formal Verification and Validation of ERTMS Industrial Railway Train Spacing System | 2009 | ERTMS 列车间隔与 RBS 调度控制 | `ERTMS, train spacing, LDS, RBS, scheduler, route control` | [formal-verification-and-validation-of-ertms-industrial-railway-train-spacing-system](sources/formal-verification-and-validation-of-ertms-industrial-railway-train-spacing-system/) |
| 111 | 🌡️ | Perencanaan Control Valve Pada Head Tank PLTA Tulungagung Menggunakan PLC | 2014 | 头水箱液位阈值阀门控制 | `head tank, PLC, ultrasonic sensor, motorized valve, solenoid valve, elevation` | [perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc](sources/perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc/) |
| 112 | 🚦 | Traffic Light Priority Control For Emergency Vehicle | 2024 | 基于优先请求的应急车辆绿波放行 | `traffic light, emergency vehicle, priority request, GPS, RFID, ETA` | [traffic-light-priority-control-for-emergency-vehicle](sources/traffic-light-priority-control-for-emergency-vehicle/) |
| 113 | 🚦 | Traffic Light Priority for Emergency Vehicle | 2023 | 基于检测覆盖常规灯序的应急优先控制 | `traffic light, emergency vehicle, override pattern, ambulance detection, deep learning` | [traffic-light-priority-for-emergency-vehicle](sources/traffic-light-priority-for-emergency-vehicle/) |
| 114 | 🅿️ | Fuzzy Logic Control of Autonomous Vehicles for Parallel Parking Maneuver | 2005 | 三阶段自主并联泊车控制 | `parallel parking, three steps, ready to reverse, fuzzy controller, scanning` | [fuzzy-logic-control-of-autonomous-vehicles-for-parallel-parking-maneuver](sources/fuzzy-logic-control-of-autonomous-vehicles-for-parallel-parking-maneuver/) |
| 115 | 🚦 | Intelligent 3-Way Priority-Driven Traffic Light Control System for Emergency Vehicles | 2023 | RFID 三路口应急车辆优先放行 | `traffic light, emergency vehicle, RFID, priority-driven, green signal` | [intelligent-3-way-priority-driven-traffic-light-control-system-for-emergency-vehicles](sources/intelligent-3-way-priority-driven-traffic-light-control-system-for-emergency-vehicles/) |
| 116 | 🚦 | Traffic Light Control System for Emergency Vehicles Using Radio Frequency | 2013 | RF 抢占式应急交通灯时序控制 | `traffic light, emergency vehicle, radio frequency, override sequence, emergency mode` | [traffic-light-control-system-for-emergency-vehicles-using-radio-frequency](sources/traffic-light-control-system-for-emergency-vehicles-using-radio-frequency/) |
| 117 | 🅿️ | Design and Development of Low Cost Automatic Parking Assistance System | 2014 | 低成本 APAS 探索-泊车两阶段控制 | `automatic parking assistance, exploration phase, parking phase, path shifting points, trajectory` | [design-and-development-of-low-cost-automatic-parking-assistance-system](sources/design-and-development-of-low-cost-automatic-parking-assistance-system/) |
## 本轮下载失败记录

以下条目是在本轮检索中实际尝试下载但未成功的候选文献。记录失败时间与原因，便于后续避开近期重复尝试。

| # | 分类 | 标题 | 失败时间 | 失败原因 |
|---|---|---|---|---|
| 1 | 🚆 | Formal Verification of a Railway Interlocking System using Model Checking | 2026-03-11 19:32 | https://dl.acm.org/doi/pdf/10.1007/s001650050022 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s001650050022 -> HTML中未发现可下载PDF \| http://hdl.handle.net/11572/20411 -> HTML中未发现可下载PDF  |
| 2 | 🚆 | An automatic SPIN validation of a safety critical railway control system | 2026-03-11 19:32 | https://research.utwente.nl/files/6146146/gnesi00automatic.pdf -> 非PDF \| https://research.utwente.nl/en/publications/06fb35d2-62eb-424e-b325-22802fb893a8 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/857524/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/icdsn.2000.857524 -> HTML中未发现可下载PDF  |
| 3 | 🚆 | Tracking and collision avoidance of virtual coupling train control system | 2026-03-11 19:33 | https://doi.org/10.1016/j.aej.2020.12.010 -> HTML中未发现可下载PDF \| https://doaj.org/article/352ecde0e746421486256bb016596f38 -> HTML中未发现可下载PDF  |
| 4 | 🚆 | Next Generation Train Control (NGTC): More Effective Railways through the Convergence of Main-line and Urban Train Control Systems | 2026-03-11 19:33 | https://doi.org/10.1016/j.trpro.2016.05.152 -> HTML中未发现可下载PDF  |
| 5 | 🚆 | How to Deal with Revolutions in Train Control Systems | 2026-03-11 19:33 | https://doi.org/10.1016/j.eng.2016.03.015 -> HTML中未发现可下载PDF \| https://doaj.org/article/22a4c7da7e014d5bb3f2b2c42b4852b0 -> HTML中未发现可下载PDF  |
| 6 | 🩺 | A Formal Verification Methodology for DDD Mode Pacemaker Control Programs | 2026-03-11 19:33 | http://downloads.hindawi.com/journals/jece/2015/939028.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2015/939028 -> HTML中未发现可下载PDF \| https://doaj.org/article/2bd2be4fe24545199bc5d22ae671b3bc -> HTML中未发现可下载PDF  |
| 7 | 🩺 | Closed-Loop Quantitative Verification of Rate-Adaptive Pacemakers | 2026-03-11 19:33 | https://dl.acm.org/doi/pdf/10.1145/3152767 -> HTML中未发现可下载PDF \| https://doi.org/10.1145/3152767 -> HTML中未发现可下载PDF  |
| 8 | 🩺 | New Insights Into Soft-Faults Induced Cardiac Pacemakers Malfunctions Analyzed at System-Level via Model Checking | 2026-03-11 19:33 | https://ieeexplore.ieee.org/document/8493464/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/access.2018.2876318 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/8493464/ -> 非PDF \| https://doaj.org/article/f74ecb7b159a49839c4715126161cffd -> HTML中未发现可下载PDF  |
| 9 | 🩺 | Combining human error verification and timing analysis: a case study on an infusion pump | 2026-03-11 19:33 | https://dl.acm.org/doi/pdf/10.1007/s00165-013-0288-1 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s00165-013-0288-1 -> HTML中未发现可下载PDF  |
| 10 | 🩺 | An Integrated Multivariable Artificial Pancreas Control System | 2026-03-11 19:33 | https://journals.sagepub.com/doi/pdf/10.1177/1932296814524862 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1932296814524862 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/24876613 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC4455451/pdf/10.1177_1932296814524862.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/10.1177_1932296814524862.pdf -> 非PDF  |
| 11 | 🩺 | Meal Detection in Patients With Type 1 Diabetes: A New Module for the Multivariable Adaptive Artificial Pancreas Control System | 2026-03-11 19:34 | https://ieeexplore.ieee.org/document/7124410/ -> 非PDF \| http://doi.org/document/ -> 非PDF \| http://doi.org/10.1109/JBHI.2015.2446413 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7124410/ -> 非PDF \| https://doi.org/document/ -> 非PDF  |
| 12 | 🩺 | Event-Triggered Model Predictive Control for Embedded Artificial Pancreas Systems | 2026-03-11 19:34 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5839516/pdf/nihms944924.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/nihms944924.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/5839516 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7932935/ -> 非PDF \| https://doi.org/document/ -> 非PDF  |
| 13 | 🩺 | Adaptive Control of Artificial Pancreas Systems ‐ A Review | 2026-03-11 19:34 | https://downloads.hindawi.com/journals/jhe/2014/131923.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1260/2040-2295.5.1.1 -> HTML中未发现可下载PDF \| https://onepetro.org/NACECORR/proceedings/CORR03/All-CORR03/NACE-03654/114399 -> HTML中未发现可下载PDF \| https://doaj.org/article/83a4b72eda794e6f9abb6d27ff4c6a31 -> HTML中未发现可下载PDF  |
| 14 | 🩺 | The Next Generation of Artificial Pancreas Control Algorithms | 2026-03-11 19:34 | https://journals.sagepub.com/doi/pdf/10.1177/193229680800200115 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/193229680800200115 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/19885184 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC2769707/pdf/dst-02-0105.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/dst-02-0105.pdf -> 非PDF  |
| 15 | 🩺 | Multi-level supervision and modification of artificial pancreas control system | 2026-03-11 19:34 | https://www.sciencedirect.com/science/article/am/pii/S0098135418300619?via%3Dihub -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.compchemeng.2018.02.002 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/30287976 -> HTML中未发现可下载PDF \| http://europepmc.org/pmc/articles/PMC6166877 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC6166877/pdf/nihms942006.pdf -> 非PDF  |
| 16 | 🩺 | Artificial Pancreas Device Systems for the Closed-Loop Control of Type 1 Diabetes | 2026-03-11 19:34 | https://journals.sagepub.com/doi/pdf/10.1177/1932296815617968 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1932296815617968 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/26589628 -> HTML中未发现可下载PDF \| http://dst.sagepub.com/content/early/2015/11/20/1932296815617968.full.pdf+html -> curl: (60) SSL certificate problem: certificate has expired More details here: https://curl.se/docs/sslcerts.html   |
| 17 | 🩺 | Simulation Environment to Evaluate Closed-Loop Insulin Delivery Systems in Type 1 Diabetes | 2026-03-11 19:35 | https://journals.sagepub.com/doi/pdf/10.1177/193229681000400117 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/193229681000400117 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/20167177 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC2825634/pdf/dst-04-0132.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/dst-04-0132.pdf -> 非PDF  |
| 18 | 🚗 | The Impact of Cooperative Adaptive Cruise Control on Traffic-Flow Characteristics | 2026-03-11 19:35 | http://infoscience.epfl.ch/record/188484 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/4019451/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/tits.2006.884615 -> HTML中未发现可下载PDF \| https://research.utwente.nl/files/6843867/Arem06impact.pdf -> 非PDF  |
| 19 | 🚗 | Design and experimental evaluation of cooperative adaptive cruise control | 2026-03-11 19:35 | https://research.tue.nl/files/73899058/Ploeg_2011_Design_and_Experimental_Evaluation_of_Cooperative_Adaptive_Cruise_Control.pdf -> 非PDF \| https://research.tue.nl/en/publications/4f434e73-cc96-434f-9c89-addcca8352a6 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/6082981/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/itsc.2011.6082981 -> HTML中未发现可下载PDF  |
| 20 | 🚗 | Cooperative Adaptive Cruise Control: A Reinforcement Learning Approach | 2026-03-11 19:36 | https://ieeexplore.ieee.org/document/5876320/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/tits.2011.2157145 -> HTML中未发现可下载PDF  |
| 21 | 🚗 | Developing a platoon-wide Eco-Cooperative Adaptive Cruise Control (CACC) system | 2026-03-11 19:36 | https://escholarship.org/content/qt1gf0c6r9/qt1gf0c6r9.pdf -> HTML中未发现可下载PDF \| https://escholarship.org/uc/item/1gf0c6r9 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7995884/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/ivs.2017.7995884 -> HTML中未发现可下载PDF  |
| 22 | 🚗 | Transient fault tolerant control for vehicle brake-by-wire systems | 2026-03-11 19:37 | https://dspace.lboro.ac.uk/2134/20830 -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.ress.2016.01.001 -> HTML中未发现可下载PDF  |
| 23 | 🚗 | A Survey of Brake-by-Wire System for Intelligent Connected Electric Vehicles | 2026-03-11 19:37 | https://ieeexplore.ieee.org/ielx7/6287639/6514899/09268150.pdf -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/9268150/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/access.2020.3040184 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/9268150/ -> 非PDF  |
| 24 | 🚗 | Data-driven model-free slip control of anti-lock braking systems using reinforcement Q-learning | 2026-03-11 19:37 | https://ro.ecu.edu.au/ecuworkspost2013/4015 -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.neucom.2017.08.036 -> HTML中未发现可下载PDF  |
| 25 | 🚗 | A Study of Coordinated Vehicle Traction Control System Based on Optimal Slip Ratio Algorithm | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/mpe/2016/3413624.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2016/3413624 -> HTML中未发现可下载PDF \| https://doaj.org/article/a2fda65a0c484a7086b7b289fe523de2 -> HTML中未发现可下载PDF  |
| 26 | 🚗 | Development of a new traction control system using ant colony optimization | 2026-03-11 19:38 | https://journals.sagepub.com/doi/pdf/10.1177/1687814018792152 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1687814018792152 -> HTML中未发现可下载PDF \| https://doaj.org/article/5de7d0442548412b8a857a990f435ddd -> HTML中未发现可下载PDF  |
| 27 | 🚗 | Autonomous rear-end collision avoidance using an electric power steering system | 2026-03-11 19:38 | https://dspace.lboro.ac.uk/2134/17359 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/0954407014567517 -> HTML中未发现可下载PDF  |
| 28 | 🚗 | Torque Control of Electric Power Steering Systems Based on Improved Active Disturbance Rejection Control | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/mpe/2020/6509607.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2020/6509607 -> HTML中未发现可下载PDF \| https://doaj.org/article/705dd5f3ac4f420c893249e7eaf78db4 -> HTML中未发现可下载PDF  |
| 29 | 🚗 | Design of the Auto Electric Power Steering System Controller | 2026-03-11 19:38 | https://doi.org/10.1016/j.proeng.2012.01.466 -> HTML中未发现可下载PDF  |
| 30 | 🚗 | A Systematic Review of Autonomous Emergency Braking System: Impact Factor, Technology, and Performance Evaluation | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/jat/2022/1188089.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2022/1188089 -> HTML中未发现可下载PDF \| https://doaj.org/article/ba6ca96049d846d3ab2b2f79b07c87f2 -> HTML中未发现可下载PDF  |
| 31 | 🚦 | Wireless Traffic Light Controller | 2026-03-11 19:38 | https://doi.org/10.1016/j.proeng.2011.03.035 -> HTML中未发现可下载PDF  |
| 32 | 🚦 | Design of Smart Traffic Light Controller Using Embedded System | 2026-03-11 19:39 | https://doi.org/10.9790/0661-01013033 -> HTML中未发现可下载PDF  |
| 33 | 🏢 | Implementation of an Electro-Pneumatic Prototype Elevator Controlled by PLC | 2026-03-11 19:39 | https://etj.uotechnology.edu.iq/article_108840_232d4fe1493af04f96c54c2d0a56b6b1.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.30684/etj.2015.108840 -> HTML中未发现可下载PDF \| https://etj.uotechnology.edu.iq/article_108840_232d4fe1493af04f96c54c2d0a56b6b1.pdf -> 非PDF \| https://doaj.org/article/94e938798aaa4ec4b9d59b2f8cb82e45 -> HTML中未发现可下载PDF  |
| 34 | 🏭 | Process sequencing for a pick-and-place robot in a real-life flexible robotic cell | 2026-03-11 19:39 | https://research.manchester.ac.uk/en/publications/7451ccd3-3ad3-47c5-9400-61c940becb13 -> HTML中未发现可下载PDF \| https://link.springer.com/content/pdf/10.1007/s00170-019-03739-6.pdf -> 非PDF \| https://doi.org/10.1007/s00170-019-03739-6#icon-eds-i-download-medium -> 非PDF \| https://doi.org/10.1007/s00170-019-03739-6 -> HTML中未发现可下载PDF \| https://www.research.manchester.ac.uk/portal/en/publications/process-se  |
| 35 | 🌡️ | PLC Batch Process Control Design and Implementation Fundamentals | 2026-03-11 19:40 | https://doi.org/10.36548/jei.2020.3.001 -> HTML中未发现可下载PDF \| http://doi.org/10.36548/jei.2020.3.001 -> HTML中未发现可下载PDF  |
| 36 | 🌡️ | Modelling and verification of an automatic controller for a water treatment mixing tank | 2026-03-11 19:40 | https://doi.org/10.5004/dwt.2019.24143 -> HTML中未发现可下载PDF  |
| 37 | ✈️ | Eliminating synchronization faults in air traffic control software via design for verification with concurrency controllers | 2026-03-11 19:40 | https://hdl.handle.net/11511/30420 -> curl: (28) Operation timed out after 44028 milliseconds with 0 bytes received \| https://link.springer.com/content/pdf/10.1007/s10515-007-0008-2.pdf -> 非PDF \| https://doi.org/10.1007/s10515-007-0008-2#icon-eds-i-download-medium -> 非PDF \| https://doi.org/10.1007/s10515-007-0008-2 -> HTML中未发现可下载PDF \| http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.138.431  |
| 38 | ✈️ | Bifurcation Analysis of a Nose Landing Gear System | 2026-03-11 19:42 | https://research-information.bris.ac.uk/files/66353645/Cooper_AIAA2016_FULL_PAPER_12072015FINALv1_1_.pdf -> 非PDF \| https://research-information.bris.ac.uk/en/publications/53c3434d-4520-43b3-b8ca-eaf13192c7df -> HTML中未发现可下载PDF \| https://research-information.bris.ac.uk/files/66353645/Cooper_AIAA2016_FULL_PAPER_12072015FINALv1_1_.pdf -> 非PDF \| https://hdl.handle.net/files/66353645/Cooper_AIAA2016_FUL  |
| 39 | ✈️ | Indoor UAV Control Using Multi-Camera Visual Feedback | 2026-03-11 19:45 | https://dspace.lboro.ac.uk/2134/17856 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s10846-010-9506-8 -> HTML中未发现可下载PDF \| https://scholarworks.unist.ac.kr/handle/201301/20220 -> HTML中未发现可下载PDF  |
| 40 | 🚦 | Traffic Light Controller Module Based on Particle Swarm Optimization (PSO) | 2026-03-11 21:48 | http://article.sciencepublishinggroup.com/pdf/10.11648.j.ajai.20180201.12.pdf -> 下载内容损坏，`pdf_extractor` 报错 `EOF marker not found`  |
| 41 | ✈️ | A Formal Verification Framework for Model Checking Safety Requirements of a Simulink Landing Gear Case Study | 2026-03-11 21:48 | https://www.rpsonline.com.sg/proceedings/esrel2023/pdf/P599.pdf -> curl: (22) The requested URL returned error: 406  |
| 42 | 🚦 | Novel Intelligent Traffic Light Controller Design | 2026-03-11 21:48 | https://www.mdpi.com/2075-1702/12/7/469/pdf?version=1720709156 -> curl: (22) The requested URL returned error: 403  |
| 43 | 🚆 | Fault tolerant train door control | 2026-03-11 21:48 | http://etheses.bham.ac.uk/1756/1/Zubrzycki11MRes.pdf -> 长时间无响应未完成下载 \| https://etheses.bham.ac.uk/id/eprint/1756/1/Zubrzycki11MRes.pdf -> HTTP 404  |
| 44 | 🅿️ | Automatic Parking Path Planning and Tracking Control Research for Intelligent Vehicles | 2026-03-11 22:07 | https://www.mdpi.com/2076-3417/10/24/9100/pdf?version=1608369025 -> curl: (22) The requested URL returned error: 403  |
| 45 | 🚦 | Traffic Management for Emergency Vehicle Priority Based on Visual Sensing | 2026-03-11 22:07 | https://www.mdpi.com/1424-8220/16/11/1892/pdf -> curl: (22) The requested URL returned error: 403  |
| 46 | 🅿️ | Parking Space Detection And Trajectory Tracking Control For Vehicle Auto-Parking | 2026-03-11 22:07 | https://zenodo.org/record/1132611/files/114.pdf?download=1 -> curl: (22) The requested URL returned error: 403  |
| 47 | 🚆 | Identifying Alterability States of a Single Track Railway Line Control System | 2026-03-11 22:07 | https://univagora.ro/jour/index.php/ijccc/article/download/4444/1829 -> 长时间无响应未完成下载  |
| 48 | 🏢 | Design and Implementation of a Prototype of Elevator Control System: Experimental Work | 2026-03-11 22:07 | https://svusrc.journals.ekb.eg/article_250615_e27357a82ac073b46eca5ea9ce1ece02.pdf -> 长时间无响应未完成下载  |
| 49 | 🏢 | Developing a Software Architecture for Graceful Degradation in an Elevator Control System | 2026-03-11 22:07 | https://figshare.com/ndownloader/files/11891195 -> 下载结果为空文件，`pdf_extractor` 报错 `Cannot read an empty file`  |
## 状态机描述收获盘点

### 更新日志

| 时间 | 范围 | 收获 | 备注 |
|---|---|---|---|
| 2026-03-11 23:21:28 | 新增 3 篇文献的 STM 提取 | 🟢 3 篇 / 🟡 0 篇 / ⚪ 0 篇 | 新增 3 个 `STM.md`，补入 3 条控制逻辑，当前已完成 117/117 篇文献的 STM 盘点 |
| 2026-03-11 23:09:54 | 新增 5 篇文献的 STM 提取 | 🟢 4 篇 / 🟡 1 篇 / ⚪ 0 篇 | 新增 5 个 `STM.md`，补入 5 条控制逻辑，当前已完成 114/114 篇文献的 STM 盘点 |
| 2026-03-11 22:43:00 | 新增 12 篇文献的 STM 提取 | 🟢 8 篇 / 🟡 3 篇 / ⚪ 1 篇 | 新增 12 个 `STM.md`，补入 11 条控制逻辑，当前已完成 109/109 篇文献的 STM 盘点 |
| 2026-03-11 22:07:39 | 新增 3 篇文献的 STM 提取 | 🟢 3 篇 / 🟡 0 篇 / ⚪ 0 篇 | 新增 3 个 `STM.md`，补入 6 条控制逻辑，当前已完成 97/97 篇文献的 STM 盘点 |
| 2026-03-11 21:45:03 | 新增 6 篇文献的 STM 提取 | 🟢 6 篇 / 🟡 0 篇 / ⚪ 0 篇 | 新增 6 个 `STM.md`，补入 9 条控制逻辑，当前已完成 94/94 篇文献的 STM 盘点 |
| 2026-03-11 20:18:12 | 完成此前 58 篇“尚未提取”文献的 STM 梳理与回填 | 🟢 13 篇 / 🟡 9 篇 / ⚪ 36 篇 | 新增 58 个 `STM.md`，当前已完成 88/88 篇文献的 STM 盘点 |

- ✅ 直接可用论文：**47** 篇
- 🟡 可整理论文：**16** 篇
- ⚪ 暂未收获论文：**54** 篇
- ⏳ 尚未提取论文：**0** 篇
- 🧾 已提取到的状态机/控制逻辑条目：**75** 条
- 🔁 去重后可归纳的控制对象/子控制逻辑类型：**约 53 类**（新增 RFID 应急优先放行、RF 抢占式灯序切换、APAS 探索-泊车两阶段控制等对象）

### 领域分布（按已提取条目统计）

- 统计口径：按 `STM.md` 中已经入账的 **75** 个状态机/控制逻辑条目统计；所用 emoji 与上方“领域 Emoji 口径”完全一致。

| 领域 | 条目数 | 占比 | 代表控制对象 |
|---|---:|---:|---|
| 🚗 汽车与道路车辆控制 | 10 | 13.3% | ABS 轮端控制、自动变速器、车队 join/leave、AEB-P |
| 🚆 轨道交通与铁路控制 | 12 | 16.0% | 进路建立与释放、道岔锁闭、联锁模式选择、RBS 调度、检测点输入处理 |
| 🏭 工业自动化与离散制造 | 6 | 8.0% | PLC operation modes、故障恢复、IEC 61499 BFB/ECC、分拣/灌装顺序控制 |
| 🩺 医疗设备与生命支持控制 | 5 | 6.7% | 输液泵模式切换、袖带血压闭环子系统、双腔起搏器节律控制 |
| 🚦 道路交通信号控制 | 12 | 16.0% | 紧急车辆优先放行、动态相位选择、空车道跳过、图像驱动绿灯分配 |
| ✈️ 航空航天与飞行/空管控制 | 3 | 4.0% | 空管协调协议、飞机轮刹供压切换、起落架伸收与锁定控制 |
| 🏢 楼宇机电与电梯控制 | 10 | 13.3% | 电梯运行与门控逻辑、上/下行遍历、自动/手动工作流 |
| 🌡️ 过程与环境控制 | 6 | 8.0% | 恒温器开关控制、双水箱液位阈值控制、头水箱阀控、液位排水循环控制 |
| 🅿️ 智慧停车与车位管理 | 11 | 14.7% | 车位分配、倒车入位分段轨迹、模糊转向修正、分阶段泊车与可停判定 |
| **合计** | **75** | **100.0%** | - |

| 目录 | 领域 | 结果 | 条目数 | 备注 | STM |
|---|---|---|---:|---|---|
| `automotive-analysis-thesis` | 🚗 | 🟢 直接可用 | 1 | BBW ABS 功能块给出了显式 TA 状态与转移。 | [STM](sources/automotive-analysis-thesis/STM.md) |
| `automotive-mbt-thesis` | 🚗 | 🟢 直接可用 | 1 | BBW ABS 行为图直接给出了 Entry/CalcSlipRate/Exit 三态。 | [STM](sources/automotive-mbt-thesis/STM.md) |
| `automotive-temporal-logic-benchmarks` | 🚗 | 🟢 直接可用 | 1 | 自动变速器基准模型明确给出了 gear FSM 和 shift guard。 | [STM](sources/automotive-temporal-logic-benchmarks/STM.md) |
| `avens-uas` | ✈️ | ⚪ 未收获 | 0 | 聚焦飞行/网络联合仿真，不提供可复用的控制系统状态机描述。 | [STM](sources/avens-uas/STM.md) |
| `cara-infusion-pump-formal-spec` | 🩺 | 🟢 直接可用 | 2 | OCR 后可稳定提取泵模式与 cuff handler 的状态/回退逻辑。 | [STM](sources/cara-infusion-pump-formal-spec/STM.md) |
| `cps-security-analysis-sysml` | 🔐 | ⚪ 未收获 | 0 | 重点是 CPS 安全威胁/攻击路径，不是控制对象行为状态机。 | [STM](sources/cps-security-analysis-sysml/STM.md) |
| `design-pillars-medical-cps` | 🩺 | ⚪ 未收获 | 0 | 是中间件设计原则，不是具体控制系统状态机。 | [STM](sources/design-pillars-medical-cps/STM.md) |
| `dual-chamber-pacemaker` | 🩺 | 🟢 直接可用 | 2 | 既有基础 DDD 节律控制，也有 DDD/VDI 模式切换。 | [STM](sources/dual-chamber-pacemaker/STM.md) |
| `east-adl-formal-analysis` | 🚗 | 🟡 可整理 | 1 | BBW ABS 逻辑清晰，但正文把状态机更多留给 TA 模型/工具层。 | [STM](sources/east-adl-formal-analysis/STM.md) |
| `fault-handling-plc-industry4` | 🏭 | 🟢 直接可用 | 2 | 既有通用 operation modes，又有 abort/reset/start 的实际切换链路。 | [STM](sources/fault-handling-plc-industry4/STM.md) |
| `holonic-control-validation` | 🏭 | ⚪ 未收获 | 0 | Petri 网验证很强，但抽取文本里缺少可直接落数据集的具体控制对象状态描述。 | [STM](sources/holonic-control-validation/STM.md) |
| `hytech-hybrid-systems` | ⚙️ | 🟢 直接可用 | 1 | 恒温器自动机是标准的控制对象状态机示例。 | [STM](sources/hytech-hybrid-systems/STM.md) |
| `ics-vulnerability-knowledge-base` | 🔐 | ⚪ 未收获 | 0 | ICS 组件与攻击路径描述为主，不是控制行为状态机。 | [STM](sources/ics-vulnerability-knowledge-base/STM.md) |
| `iec61499-realtime-semantics` | 🏭 | 🟡 可整理 | 1 | BFB/ECC 本身就是有限状态控制器，但示例状态名主要在图里。 | [STM](sources/iec61499-realtime-semantics/STM.md) |
| `iec61499-soa-review` | 🏭 | ⚪ 未收获 | 0 | 综述型论文，没有可追溯的控制状态设计。 | [STM](sources/iec61499-soa-review/STM.md) |
| `iec61499-vs-61131` | 🏭 | ⚪ 未收获 | 0 | 有 ECC 示例，但对象是泛化 counter FB，不作为控制系统需求样本。 | [STM](sources/iec61499-vs-61131/STM.md) |
| `industrial-strength-mbt` | 🧩 | ⚪ 未收获 | 0 | 模型测试方法综述，不是控制系统设计原文。 | [STM](sources/industrial-strength-mbt/STM.md) |
| `model-driven-iec61131-development` | 🏭 | ⚪ 未收获 | 0 | 有 Feeder FB/SFC 背景，但正文没有把状态和转移文本化到可追溯程度。 | [STM](sources/model-driven-iec61131-development/STM.md) |
| `plc-course-fsm` | 🏭 | 🟢 直接可用 | 2 | 给出了非常干净的 box-fill 三态 FSM 和 auto/standby 二态 FSM。 | [STM](sources/plc-course-fsm/STM.md) |
| `plc-software-modularity` | 🏭 | ⚪ 未收获 | 0 | 列出了 operation modes，但没有具体控制对象的转移逻辑。 | [STM](sources/plc-software-modularity/STM.md) |
| `safeslice` | 🔐 | ⚪ 未收获 | 0 | 出现的模式是工具模式，不是控制系统模式。 | [STM](sources/safeslice/STM.md) |
| `secure-safe-embedded-mde` | 🔐 | ⚪ 未收获 | 0 | 文中状态机主要对应密钥分发协议，不是控制系统对象。 | [STM](sources/secure-safe-embedded-mde/STM.md) |
| `smart-manufacturing-standards-nist` | 🏭 | ⚪ 未收获 | 0 | 标准/参考架构综述，不提供状态机行为细节。 | [STM](sources/smart-manufacturing-standards-nist/STM.md) |
| `sysml-safety-analysis-integration` | 🧩 | 🟢 直接可用 | 1 | 飞机轮刹系统四模态自动机非常适合状态机需求样本。 | [STM](sources/sysml-safety-analysis-integration/STM.md) |
| `sysml-safety-critical-design-process` | 🧩 | ⚪ 未收获 | 0 | 更偏设计流程方法，缺少具体控制对象状态机正文。 | [STM](sources/sysml-safety-critical-design-process/STM.md) |
| `sysmlv2-avionics` | ✈️ | ⚪ 未收获 | 0 | 探索 SysML v2 建模能力，没有可追溯控制状态样本。 | [STM](sources/sysmlv2-avionics/STM.md) |
| `system-architecture-virtual-integration` | 🧩 | ⚪ 未收获 | 0 | 以体系结构/虚拟集成为主，状态逻辑多停留在工具链层。 | [STM](sources/system-architecture-virtual-integration/STM.md) |
| `tasm-toolset` | ⚙️ | ⚪ 未收获 | 0 | 只说明工具曾用于 Electronic Throttle Controller，没有给出状态细节。 | [STM](sources/tasm-toolset/STM.md) |
| `time-complemented-automation-architecture` | 🏭 | 🟢 直接可用 | 1 | Sorter1 的控制流非常适合作为分布式自动化状态/转移样本。 | [STM](sources/time-complemented-automation-architecture/STM.md) |
| `vital-east-adl-uppaal` | 🚗 | 🟡 可整理 | 1 | 有 BBW 功能约束和 fp 执行周期，但显式状态较少。 | [STM](sources/vital-east-adl-uppaal/STM.md) |
| `adaptive-control-of-robot-manipulators-with-flexible-joints` | 🏭 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/adaptive-control-of-robot-manipulators-with-flexible-joints/STM.md) |
| `autonomous-intelligent-cruise-control` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/autonomous-intelligent-cruise-control/STM.md) |
| `elevator-group-control-using-multiple-reinforcement-learning-agents` | 🏢 | ⚪ 未收获 | 0 | 重点是调度、分配或路径规划策略，缺少明确的运行模式切换和执行控制逻辑。 | [STM](sources/elevator-group-control-using-multiple-reinforcement-learning-agents/STM.md) |
| `formal-modelling-and-simulation-of-train-control-systems-using-petri-net` | 🚆 | ⚪ 未收获 | 0 | 重点是建模语言、验证框架、开发过程或体系结构，不是控制对象本身的运行逻辑。 | [STM](sources/formal-modelling-and-simulation-of-train-control-systems-using-petri-net/STM.md) |
| `modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin/STM.md) |
| `using-z-specification-for-railway-interlocking-safety` | 🚆 | 🟡 可整理 | 1 | 联锁系统状态由组件状态组合构成，route/sub-route 的 set/lock 逻辑可整理。 | [STM](sources/using-z-specification-for-railway-interlocking-safety/STM.md) |
| `multi-car-elevator-control-by-using-learning-automaton` | 🏢 | ⚪ 未收获 | 0 | 文本分布过于分散或语言/提取质量限制较强，当前未定位到足够可靠的控制状态描述。 | [STM](sources/multi-car-elevator-control-by-using-learning-automaton/STM.md) |
| `a-formal-approach-for-the-construction-and-verification-of-railway-contr` | 🚆 | 🟢 直接可用 | 1 | 路由保留、道岔定位、进路开放与释放链路描述清楚，可直接整理为控制逻辑样本。 | [STM](sources/a-formal-approach-for-the-construction-and-verification-of-railway-contr/STM.md) |
| `automated-verification-of-signalling-principles-in-railway-interlocking` | 🚆 | 🟡 可整理 | 1 | 联锁控制循环和对象互斥条件明确，但更多体现为 ladder logic 的周期执行与状态约束。 | [STM](sources/automated-verification-of-signalling-principles-in-railway-interlocking/STM.md) |
| `automatic-generation-and-verification-of-railway-interlocking-control-ta` | 🚆 | 🟢 直接可用 | 1 | 轨道区段、道岔、信号和进路的离散状态与进路设定条件写得很明确。 | [STM](sources/automatic-generation-and-verification-of-railway-interlocking-control-ta/STM.md) |
| `3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control/STM.md) |
| `modelling-railway-interlocking-tables-using-coloured-petri-nets` | 🚆 | 🟢 直接可用 | 1 | route set/release、冲突进路和入口信号开放条件的文字依据很充分。 | [STM](sources/modelling-railway-interlocking-tables-using-coloured-petri-nets/STM.md) |
| `nonlinear-controller-design-of-a-ship-autopilot` | ⚙️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/nonlinear-controller-design-of-a-ship-autopilot/STM.md) |
| `on-board-and-ground-visual-pose-estimation-techniques-for-uav-control` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/on-board-and-ground-visual-pose-estimation-techniques-for-uav-control/STM.md) |
| `formal-specification-and-verification-of-a-coordination-protocol-for-an` | ✈️ | 🟢 直接可用 | 1 | AAC 中 AutoResolver/TSAFE/TCAS 的控制接管与返还条件非常明确。 | [STM](sources/formal-specification-and-verification-of-a-coordination-protocol-for-an/STM.md) |
| `marginalizing-out-future-passengers-in-group-elevator-control` | 🏢 | ⚪ 未收获 | 0 | 重点是调度、分配或路径规划策略，缺少明确的运行模式切换和执行控制逻辑。 | [STM](sources/marginalizing-out-future-passengers-in-group-elevator-control/STM.md) |
| `cooperative-adaptive-cruise-control-in-real-traffic-situations` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/cooperative-adaptive-cruise-control-in-real-traffic-situations/STM.md) |
| `experimental-verification-of-vehicle-platoon-control-algorithms` | 🚗 | ⚪ 未收获 | 0 | 重点是建模语言、验证框架、开发过程或体系结构，不是控制对象本身的运行逻辑。 | [STM](sources/experimental-verification-of-vehicle-platoon-control-algorithms/STM.md) |
| `online-predictive-diagnosis-of-electrical-train-door-systems` | 🚆 | ⚪ 未收获 | 0 | 重点是故障诊断或监测，原文中的阶段/工况主要服务于诊断而不是控制设计。 | [STM](sources/online-predictive-diagnosis-of-electrical-train-door-systems/STM.md) |
| `reactive-approach-for-autonomous-vehicle-platoon-systems-modelling-and-v` | 🚗 | ⚪ 未收获 | 0 | 文本分布过于分散或语言/提取质量限制较强，当前未定位到足够可靠的控制状态描述。 | [STM](sources/reactive-approach-for-autonomous-vehicle-platoon-systems-modelling-and-v/STM.md) |
| `adaptive-cascade-control-of-a-brake-by-wire-actuator-for-sport-motorcycl` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/adaptive-cascade-control-of-a-brake-by-wire-actuator-for-sport-motorcycl/STM.md) |
| `architecture-description-language-for-cyber-physical-systems-analysis-a` | 🚆 | ⚪ 未收获 | 0 | 重点是建模语言、验证框架、开发过程或体系结构，不是控制对象本身的运行逻辑。 | [STM](sources/architecture-description-language-for-cyber-physical-systems-analysis-a/STM.md) |
| `automated-verification-of-quantitative-properties-of-cardiac-pacemaker-s` | 🩺 | ⚪ 未收获 | 0 | 重点是建模语言、验证框架、开发过程或体系结构，不是控制对象本身的运行逻辑。 | [STM](sources/automated-verification-of-quantitative-properties-of-cardiac-pacemaker-s/STM.md) |
| `developing-and-verifying-user-interface-requirements-for-infusion-pumps` | 🩺 | 🟡 可整理 | 1 | 围绕输液泵数据录入的进入、修改、提交和 entry mode 条件有清楚的离散描述。 | [STM](sources/developing-and-verifying-user-interface-requirements-for-infusion-pumps/STM.md) |
| `modeling-cooperative-and-autonomous-adaptive-cruise-control-dynamic-resp` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/modeling-cooperative-and-autonomous-adaptive-cruise-control-dynamic-resp/STM.md) |
| `performance-evaluation-of-an-anti-lock-braking-system-for-electric-vehic` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/performance-evaluation-of-an-anti-lock-braking-system-for-electric-vehic/STM.md) |
| `high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti` | 🚦 | 🟡 可整理 | 1 | 下一相位选择和绿灯持续时间计算流程明确，但更偏算法化相位决策。 | [STM](sources/high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti/STM.md) |
| `the-landing-gear-system-in-multi-machine-hybrid-event-b` | ✈️ | 🟢 直接可用 | 1 | 起落架手柄、模拟开关和 door/gear movement machines 的切换关系很明确。 | [STM](sources/the-landing-gear-system-in-multi-machine-hybrid-event-b/STM.md) |
| `uav-control-on-the-basis-of-3d-landmark-bearing-only-observations` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/uav-control-on-the-basis-of-3d-landmark-bearing-only-observations/STM.md) |
| `verification-of-railway-interlocking-systems` | 🚆 | 🟢 直接可用 | 1 | request-check-lock-green-release 的 route lifecycle 写得非常完整。 | [STM](sources/verification-of-railway-interlocking-systems/STM.md) |
| `bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me` | 🚆 | ⚪ 未收获 | 0 | 重点是故障诊断或监测，原文中的阶段/工况主要服务于诊断而不是控制设计。 | [STM](sources/bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me/STM.md) |
| `validation-process-for-railway-interlocking-systems` | 🚆 | ⚪ 未收获 | 0 | 重点是建模语言、验证框架、开发过程或体系结构，不是控制对象本身的运行逻辑。 | [STM](sources/validation-process-for-railway-interlocking-systems/STM.md) |
| `design-amp-control-of-an-elevator-control-system-using-plc` | 🏢 | 🟢 直接可用 | 1 | 电梯门、超载、停层和失电应急动作都给出了明确的控制描述。 | [STM](sources/design-amp-control-of-an-elevator-control-system-using-plc/STM.md) |
| `formal-verification-of-autonomous-vehicle-platooning` | 🚗 | 🟢 直接可用 | 2 | 加入和离队流程都给出了逐步的控制约束与安全条件。 | [STM](sources/formal-verification-of-autonomous-vehicle-platooning/STM.md) |
| `integrated-longitudinal-and-lateral-networked-control-system-design-for` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/integrated-longitudinal-and-lateral-networked-control-system-design-for/STM.md) |
| `intelligent-elevator-control-and-safety-monitoring-system` | 🏢 | 🟡 可整理 | 1 | 门感应、语音选层和超时关闭前的语音控制逻辑较明确。 | [STM](sources/intelligent-elevator-control-and-safety-monitoring-system/STM.md) |
| `networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi/STM.md) |
| `automatic-traffic-light-controller-for-emergency-vehicle-using-periphera` | 🚦 | 🟢 直接可用 | 1 | 紧急车辆触发、绿灯延长和恢复正常模式的控制链路非常清楚。 | [STM](sources/automatic-traffic-light-controller-for-emergency-vehicle-using-periphera/STM.md) |
| `features-of-automatic-control-of-technological-parameters-of-water-level` | 🌡️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/features-of-automatic-control-of-technological-parameters-of-water-level/STM.md) |
| `fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock/STM.md) |
| `modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa` | 🚗 | 🟢 直接可用 | 1 | join procedure 的通信、变道、速度/转向接管顺序明确。 | [STM](sources/modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa/STM.md) |
| `research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge` | 🚗 | 🟡 可整理 | 1 | AEB-P 的预警、自动制动接管和分层控制模块较清楚。 | [STM](sources/research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge/STM.md) |
| `water-tank-level-controller-by-using-plc` | 🌡️ | 🟢 直接可用 | 1 | 上下阈值触发泵/阀动作的控制序列明确，适合直接当成简单控制需求样本。 | [STM](sources/water-tank-level-controller-by-using-plc/STM.md) |
| `data-efficient-reinforcement-learning-for-integrated-lateral-planning-an` | 🅿️ | ⚪ 未收获 | 0 | 重点是调度、分配或路径规划策略，缺少明确的运行模式切换和执行控制逻辑。 | [STM](sources/data-efficient-reinforcement-learning-for-integrated-lateral-planning-an/STM.md) |
| `information-value-based-fault-diagnosis-of-train-door-system-under-multi` | 🚆 | ⚪ 未收获 | 0 | 重点是故障诊断或监测，原文中的阶段/工况主要服务于诊断而不是控制设计。 | [STM](sources/information-value-based-fault-diagnosis-of-train-door-system-under-multi/STM.md) |
| `review-on-the-development-control-method-and-application-prospect-of-bra` | 🚗 | ⚪ 未收获 | 0 | 综述/综述型技术总结为主，缺少单一控制对象的可追溯运行逻辑。 | [STM](sources/review-on-the-development-control-method-and-application-prospect-of-bra/STM.md) |
| `sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo/STM.md) |
| `video-based-parking-occupancy-detection-for-smart-control-system` | 🅿️ | ⚪ 未收获 | 0 | 重点是调度、分配或路径规划策略，缺少明确的运行模式切换和执行控制逻辑。 | [STM](sources/video-based-parking-occupancy-detection-for-smart-control-system/STM.md) |
| `an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea/STM.md) |
| `intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process` | 🚦 | 🟡 可整理 | 1 | 用车流量与红黄绿时间共同决定六个信号输出，具备明确的相位控制含义。 | [STM](sources/intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process/STM.md) |
| `performance-assessment-of-an-electric-power-steering-system-for-driverle` | 🚗 | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/performance-assessment-of-an-electric-power-steering-system-for-driverle/STM.md) |
| `traffic-light-controller-using-image-processing` | 🚦 | 🟢 直接可用 | 1 | 图像匹配结果到红绿灯时长的映射规则明确可追溯。 | [STM](sources/traffic-light-controller-using-image-processing/STM.md) |
| `formal-modeling-and-verification-of-the-functionality-of-electronic-urba` | 🚆 | 🟢 直接可用 | 2 | 电车平交口保护序列和检测点状态机都给出了可追溯的离散行为。 | [STM](sources/formal-modeling-and-verification-of-the-functionality-of-electronic-urba/STM.md) |
| `research-on-path-planning-and-tracking-control-of-automatic-parking-syst` | 🅿️ | ⚪ 未收获 | 0 | 重点是调度、分配或路径规划策略，缺少明确的运行模式切换和执行控制逻辑。 | [STM](sources/research-on-path-planning-and-tracking-control-of-automatic-parking-syst/STM.md) |
| `review-of-brake-by-wire-system-and-control-technology` | 🚗 | ⚪ 未收获 | 0 | 综述/综述型技术总结为主，缺少单一控制对象的可追溯运行逻辑。 | [STM](sources/review-of-brake-by-wire-system-and-control-technology/STM.md) |
| `a-smart-real-time-parking-control-and-monitoring-system` | 🅿️ | 🟡 可整理 | 1 | 停车位分配、预约和到位核验逻辑较清楚，但更偏管理控制层而非底层执行控制。 | [STM](sources/a-smart-real-time-parking-control-and-monitoring-system/STM.md) |
| `design-and-assessment-of-an-anti-lock-braking-system-controller` | 🚗 | 🟡 可整理 | 1 | ABS 的检测-减压-再增压闭环很清楚，但表达更偏控制机理而非显式状态机。 | [STM](sources/design-and-assessment-of-an-anti-lock-braking-system-controller/STM.md) |
| `model-based-design-of-aircraft-landing-gear-system` | ✈️ | ⚪ 未收获 | 0 | 重点是连续控制、估计或性能优化，不提供可直接整理成状态机自然语言样本的离散控制模式描述。 | [STM](sources/model-based-design-of-aircraft-landing-gear-system/STM.md) |
| `french-railway-interlocking-hcpn` | 🚆 | 🟢 直接可用 | 2 | 同时给出进路建立检查链路和 TP/DA/MO 模式约束。 | [STM](sources/french-railway-interlocking-hcpn/STM.md) |
| `plc-based-multi-floor-elevator-control-system` | 🏢 | 🟢 直接可用 | 1 | 程序明确拆成上行/下行与一至三层遍历 cases。 | [STM](sources/plc-based-multi-floor-elevator-control-system/STM.md) |
| `adaptive-traffic-light-controller-using-artificial-bee-colony` | 🚦 | 🟢 直接可用 | 2 | 既有队列优先相位排序，也有空车道零绿灯跳过逻辑。 | [STM](sources/adaptive-traffic-light-controller-using-artificial-bee-colony/STM.md) |
| `design-of-plc-based-elevator-control-system` | 🏢 | 🟢 直接可用 | 1 | 呼梯、3 秒开门等待、关门、转向目标层的顺序清晰。 | [STM](sources/design-of-plc-based-elevator-control-system/STM.md) |
| `parallel-parking-system-design-with-fuzzy-logic-control` | 🅿️ | 🟢 直接可用 | 2 | 同时给出倒车入位分段轨迹和模糊转向修正闭环。 | [STM](sources/parallel-parking-system-design-with-fuzzy-logic-control/STM.md) |
| `design-of-elevator-control-system-based-on-plc` | 🏢 | 🟢 直接可用 | 1 | 工作流描述覆盖初始层、呼梯、门控、手动/自动和紧急呼叫。 | [STM](sources/design-of-elevator-control-system-based-on-plc/STM.md) |
| `automatic-water-level-and-pressure-control-system-prototype` | 🌡️ | 🟢 直接可用 | 2 | 同时给出 LL/HL 浮球触发的泵启停和高液位后延时排水循环。 | [STM](sources/automatic-water-level-and-pressure-control-system-prototype/STM.md) |
| `hierarchical-driver-aid-for-parallel-parking` | 🅿️ | 🟢 直接可用 | 2 | 既有双摄像头-HMI 驾驶指令链路，也有 Stage 1/Stage 2 触发切换。 | [STM](sources/hierarchical-driver-aid-for-parallel-parking/STM.md) |
| `intelligent-auto-parking-system-for-vehicles` | 🅿️ | 🟢 直接可用 | 2 | 既有 PAS 控制链路，也有 parking possible 判定和轨迹半径选择逻辑。 | [STM](sources/intelligent-auto-parking-system-for-vehicles/STM.md) |
| `application-of-plc-for-elevator-control-system` | 🏢 | 🟢 直接可用 | 1 | 呼梯后正反转运行并在限位开关处停层，结构很干净。 | [STM](sources/application-of-plc-for-elevator-control-system/STM.md) |
| `plc-controlling-program-of-an-elevator` | 🏢 | 🟢 直接可用 | 1 | 同向优先调度、到层开门、重开门与超载/障碍响应链路完整。 | [STM](sources/plc-controlling-program-of-an-elevator/STM.md) |
| `plc-controlled-elevator-system-using-xc1-plc-through-ladder-programming` | 🏢 | 🟢 直接可用 | 1 | XC1 PLC 的 up-call/down-call 调度和到层减速策略很明确。 | [STM](sources/plc-controlled-elevator-system-using-xc1-plc-through-ladder-programming/STM.md) |
| `plc-based-intelligent-control-system-for-four-floor-elevator` | 🏢 | 🟢 直接可用 | 1 | 直接点名 Ascending/Descending/Stopped 三态及门阻挡/超载约束。 | [STM](sources/plc-based-intelligent-control-system-for-four-floor-elevator/STM.md) |
| `design-of-a-plc-based-elevator-control-system` | 🏢 | 🟢 直接可用 | 1 | 无请求停层开门、自动关门和 hall/car call 优先逻辑清晰。 | [STM](sources/design-of-a-plc-based-elevator-control-system/STM.md) |
| `automatic-traffic-using-image-processing` | 🚦 | 🟡 可整理 | 1 | 图像计数到配时控制链路清楚，但相位细节更偏算法层。 | [STM](sources/automatic-traffic-using-image-processing/STM.md) |
| `intelligent-traffic-light-control-system-based-on-image-processing` | 🚦 | 🟢 直接可用 | 1 | 四车道密度、红黄绿时间和 ambulance detection 控制目标明确。 | [STM](sources/intelligent-traffic-light-control-system-based-on-image-processing/STM.md) |
| `some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts` | 🚆 | 🟢 直接可用 | 1 | route request 后的 check-lock-green 顺序写得非常完整。 | [STM](sources/some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts/STM.md) |
| `modelling-interlocking-systems-for-railway-stations` | 🚆 | ⚪ 未收获 | 0 | 更偏联锁建模与验证流程，当前未稳定抽出原文型控制叙述。 | [STM](sources/modelling-interlocking-systems-for-railway-stations/STM.md) |
| `plc-based-water-level-control-system` | 🌡️ | 🟢 直接可用 | 1 | 四浮球阈值触发泵启停逻辑非常适合简单顺序控制样本。 | [STM](sources/plc-based-water-level-control-system/STM.md) |
| `fuzzy-controller-based-design-and-simulation-of-an-automatic-parking-system` | 🅿️ | 🟡 可整理 | 1 | 位置/方向角到转向角的迭代闭环清楚，但更偏控制闭环叙述。 | [STM](sources/fuzzy-controller-based-design-and-simulation-of-an-automatic-parking-system/STM.md) |
| `design-and-simulation-of-small-space-parallel-parking-fuzzy-controller` | 🅿️ | 🟡 可整理 | 1 | 先检测可停车位，再基于 Ackerman 倒车模型执行泊车。 | [STM](sources/design-and-simulation-of-small-space-parallel-parking-fuzzy-controller/STM.md) |
| `formal-verification-and-validation-of-ertms-industrial-railway-train-spacing-system` | 🚆 | 🟡 可整理 | 1 | LDS/RBS 列车间隔控制与调度职责清楚，但正文更偏验证抽象。 | [STM](sources/formal-verification-and-validation-of-ertms-industrial-railway-train-spacing-system/STM.md) |
| `perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc` | 🌡️ | 🟢 直接可用 | 1 | 头水箱液位阈值到阀门开启动作的 PLC 逻辑非常明确。 | [STM](sources/perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc/STM.md) |
| `traffic-light-priority-control-for-emergency-vehicle` | 🚦 | 🟢 直接可用 | 1 | priority request 到绿灯放行再恢复常规灯序的链路完整。 | [STM](sources/traffic-light-priority-control-for-emergency-vehicle/STM.md) |
| `traffic-light-priority-for-emergency-vehicle` | 🚦 | 🟢 直接可用 | 1 | ambulance detection 触发 override 标准灯序并切为绿灯。 | [STM](sources/traffic-light-priority-for-emergency-vehicle/STM.md) |
| `fuzzy-logic-control-of-autonomous-vehicles-for-parallel-parking-maneuver` | 🅿️ | 🟢 直接可用 | 1 | 直接给出 scanning-reverse-adjusting forward 三阶段泊车流程。 | [STM](sources/fuzzy-logic-control-of-autonomous-vehicles-for-parallel-parking-maneuver/STM.md) |
| `intelligent-3-way-priority-driven-traffic-light-control-system-for-emergency-vehicles` | 🚦 | 🟢 直接可用 | 1 | RFID 检测、优先分配、绿灯放行和恢复常规灯序链路完整。 | [STM](sources/intelligent-3-way-priority-driven-traffic-light-control-system-for-emergency-vehicles/STM.md) |
| `traffic-light-control-system-for-emergency-vehicles-using-radio-frequency` | 🚦 | 🟢 直接可用 | 1 | normal sequence 与 emergency mode sequence 的切换和恢复都写得很明确。 | [STM](sources/traffic-light-control-system-for-emergency-vehicles-using-radio-frequency/STM.md) |
| `design-and-development-of-low-cost-automatic-parking-assistance-system` | 🅿️ | 🟢 直接可用 | 1 | exploration phase 与 parking phase 的职责划分很清楚。 | [STM](sources/design-and-development-of-low-cost-automatic-parking-assistance-system/STM.md) |

### 说明

- `🟢 直接可用`：正文已明确给出控制对象、状态/模式与转移/guard，可直接进入后续自然语言状态机数据整理。
- `🟡 可整理`：正文明确给出控制逻辑或 automata 执行语义，但部分状态信息更多保存在图或工具语义里，整理时需要轻度补形。
- `⚪ 暂未收获`：要么论文主题不是控制对象行为本身，要么 `paper_content.txt` 中没有足够具体、可追溯的状态/转移描述。
- `⏳ 尚未提取`：该图例为后续波次预留；当前所有已收录文献均已完成 `STM.md` 盘点。
- `CARA` 的 `paper_content.txt` 已改为 OCR 版，以便 `STM.md` 的页码/段落定位可靠。
