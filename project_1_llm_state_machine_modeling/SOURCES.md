# Project 1 Sources

本清单基于 `BASELINE.md` 中推荐的学术检索关键词簇扩展检索，聚焦后续“状态机自然语言需求/描述数据集”可直接利用的控制系统需求、系统设计、行为建模、形式化规格与验证资料。

## 检索关键词簇

- `automotive requirements` + `state machine/statechart/behavior model`
- `SysML` + `safety-critical system` + `behavior/safety analysis`
- `IEC 61499` / `IEC 61131` + `industrial automation` + `control system`
- `PLC` + `state machine` + `industrial automation`
- `OPC UA` / `IIoT` + `control architecture`
- `formal specification` / `behavioral modeling` + `control system` / `cyber-physical system`

## 当前收录统计

- 已收录论文：**30** 篇
- 🚗 汽车/车载：6 篇
- 🧩 SysML/MBSE：5 篇
- 🏭 工业自动化/标准：6 篇
- 🤖 PLC/状态机：3 篇
- ⚙️ 控制规格/案例：6 篇
- 🔐 安全/韧性：4 篇

所有目录均已包含：PDF 原文、`bibtex.bib`、自动生成的 `paper_content.txt`。本轮未生成 `desc.md`。

## 论文清单

| # | 分类 | 标题 | 年份 | 主题 | 关键词 | 目录 |
|---|---|---|---:|---|---|---|
| 1 | ⚙️ | HyTech: A model checker for hybrid systems | 1997 | 混成系统验证 | `hybrid systems, model checker, formal verification` | [hytech-hybrid-systems](sources/hytech-hybrid-systems/) |
| 2 | ⚙️ | A formal validation approach for holonic control system specifications | 2004 | Holonic控制规格验证 | `holonic control systems, formal validation, specifications` | [holonic-control-validation](sources/holonic-control-validation/) |
| 3 | ⚙️ | Formal specifications and analysis of the computer-assisted resuscitation algorithm (CARA) Infusion Pump Control System | 2004 | 医疗控制系统规格 | `infusion pump, formal specification, control system` | [cara-infusion-pump-formal-spec](sources/cara-infusion-pump-formal-spec/) |
| 4 | ⚙️ | The TASM Toolset: Specification, Simulation, and Formal Verification of Real-Time Systems | 2007 | 实时系统工具链 | `real-time systems, specification, simulation, formal verification` | [tasm-toolset](sources/tasm-toolset/) |
| 5 | 🧩 | System Architecture Virtual Integration: An Industrial Case Study | 2009 | 工业案例虚拟集成 | `system architecture, virtual integration, industrial case study` | [system-architecture-virtual-integration](sources/system-architecture-virtual-integration/) |
| 6 | 🔐 | SafeSlice | 2011 | 安全分析切片 | `safety analysis, slicing, model-based` | [safeslice](sources/safeslice/) |
| 7 | 🏭 | Towards a Model-Driven IEC 61131-Based Development Process in Industrial Automation | 2011 | IEC 61131开发流程 | `IEC 61131, model-driven, industrial automation` | [model-driven-iec61131-development](sources/model-driven-iec61131-development/) |
| 8 | ⚙️ | Modeling and Verification of a Dual Chamber Implantable Pacemaker | 2012 | 医疗设备状态建模 | `pacemaker, modeling, verification, medical CPS` | [dual-chamber-pacemaker](sources/dual-chamber-pacemaker/) |
| 9 | 🚗 | ViTAL: A Verification Tool for EAST-ADL Models Using UPPAAL PORT | 2012 | EAST-ADL验证工具 | `EAST-ADL, UPPAAL, verification tool` | [vital-east-adl-uppaal](sources/vital-east-adl-uppaal/) |
| 10 | 🚗 | A methodology for formal analysis and verification of EAST-ADL models | 2013 | 汽车体系结构验证 | `EAST-ADL, formal verification, automotive` | [east-adl-formal-analysis](sources/east-adl-formal-analysis/) |
| 11 | 🏭 | IEC 61499 vs. 61131: A Comparison Based on Misperceptions | 2013 | 控制标准对比 | `IEC 61499, IEC 61131, comparison` | [iec61499-vs-61131](sources/iec61499-vs-61131/) |
| 12 | 🧩 | Industrial-Strength Model-Based Testing - State of the Art and Current Challenges | 2013 | 工业级模型测试 | `model-based testing, industrial systems, state of the art` | [industrial-strength-mbt](sources/industrial-strength-mbt/) |
| 13 | 🧩 | On the Use of SysML Models in the Construction of the Design Process for Safety-Critical Systems | 2013 | SysML设计过程 | `SysML, safety-critical systems, design process` | [sysml-safety-critical-design-process](sources/sysml-safety-critical-design-process/) |
| 14 | 🧩 | Safety analysis integration in a SysML-based complex system design process | 2013 | SysML安全分析 | `SysML, safety analysis, complex systems` | [sysml-safety-analysis-integration](sources/sysml-safety-analysis-integration/) |
| 15 | ⚙️ | Design Pillars for Medical Cyber-Physical System Middleware | 2014 | 医疗CPS中间件 | `medical CPS, middleware, design` | [design-pillars-medical-cps](sources/design-pillars-medical-cps/) |
| 16 | 🚗 | Model-checking and Model-based Testing of Automotive Embedded Systems : Starting from the System Architecture | 2014 | 汽车系统模型测试 | `automotive embedded systems, model checking, model-based testing` | [automotive-mbt-thesis](sources/automotive-mbt-thesis/) |
| 17 | 🏭 | Time-Complemented Event-Driven Architecture for Distributed Automation Systems | 2014 | 分布式自动化架构 | `distributed automation systems, event-driven architecture, time-aware` | [time-complemented-automation-architecture](sources/time-complemented-automation-architecture/) |
| 18 | 🔐 | Towards the Model-Driven Engineering of Secure yet Safe Embedded Systems | 2014 | 安全与安保建模 | `embedded systems, security, safety, model-driven engineering` | [secure-safe-embedded-mde](sources/secure-safe-embedded-mde/) |
| 19 | 🏭 | A real-time semantics for the IEC 61499 standard | 2015 | IEC 61499实时语义 | `IEC 61499, real-time semantics, automation` | [iec61499-realtime-semantics](sources/iec61499-realtime-semantics/) |
| 20 | 🔐 | Extracting Vulnerabilities in Industrial Control Systems using a Knowledge-Based System | 2015 | 工业控制系统知识建模 | `industrial control systems, knowledge-based system, vulnerabilities` | [ics-vulnerability-knowledge-base](sources/ics-vulnerability-knowledge-base/) |
| 21 | 🏭 | Service-Oriented Architecture in Industrial Automation Systems - The case of IEC 61499: A Review | 2015 | IEC 61499综述 | `IEC 61499, SOA, industrial automation` | [iec61499-soa-review](sources/iec61499-soa-review/) |
| 22 | 🏭 | Current Standards Landscape for Smart Manufacturing Systems | 2016 | 智能制造标准 | `smart manufacturing, standards, NIST` | [smart-manufacturing-standards-nist](sources/smart-manufacturing-standards-nist/) |
| 23 | 🤖 | Fault Handling in PLC-Based Industry 4.0 Automated Production Systems as a Basis for Restart and Self-Configuration and Its Evaluation | 2016 | PLC故障处理 | `PLC, Industry 4.0, fault handling, self-configuration` | [fault-handling-plc-industry4](sources/fault-handling-plc-industry4/) |
| 24 | 🚗 | Model-driven Analysis and Verification of Automotive Embedded Systems | 2016 | 汽车嵌入式系统分析 | `automotive embedded systems, model-driven analysis, verification` | [automotive-analysis-thesis](sources/automotive-analysis-thesis/) |
| 25 | 🚗 | AVENS - A Novel Flying Ad Hoc Network Simulator with Automatic Code Generation for Unmanned Aircraft System | 2017 | 无人机系统建模 | `unmanned aircraft system, simulator, code generation` | [avens-uas](sources/avens-uas/) |
| 26 | 🤖 | Modularity and architecture of PLC-based software for automated production Systems: An analysis in industrial companies | 2017 | PLC软件架构 | `PLC, modularity, architecture, production systems` | [plc-software-modularity](sources/plc-software-modularity/) |
| 27 | 🔐 | A model-based approach to security analysis for cyber-physical systems | 2018 | CPS安全分析 | `cyber-physical systems, security analysis, model-based` | [cps-security-analysis-sysml](sources/cps-security-analysis-sysml/) |
| 28 | 🚗 | Benchmarks for Temporal Logic Requirements for Automotive Systems | 2018 | 汽车需求基准 | `automotive, temporal logic, requirements` | [automotive-temporal-logic-benchmarks](sources/automotive-temporal-logic-benchmarks/) |
| 29 | 🤖 | Teaching Finite State Machines (FSMs) as Part of a Programmable Logic Control (PLC) Course | 2018 | PLC课程FSM | `FSM, PLC, teaching` | [plc-course-fsm](sources/plc-course-fsm/) |
| 30 | 🧩 | Exploring SysML v2 for Model-Based Engineering of Safety-Critical Avionics Systems | 2024 | SysML v2航空电子 | `SysML v2, avionics, safety-critical systems` | [sysmlv2-avionics](sources/sysmlv2-avionics/) |

## 状态机描述收获盘点

- ✅ 直接可用论文：**10** 篇
- 🟡 可整理论文：**3** 篇
- ⚪ 暂未收获论文：**17** 篇
- 🧾 提取到的状态机/控制逻辑条目：**17** 条
- 🔁 去重后可归纳的控制对象/子控制逻辑类型：**约 14 类**（BBW/ABS 在多篇论文中重复出现）

| 目录 | 结果 | 条目数 | 备注 | STM |
|---|---|---:|---|---|
| `automotive-analysis-thesis` | 🟢 直接可用 | 1 | BBW ABS 功能块给出了显式 TA 状态与转移。 | [STM](sources/automotive-analysis-thesis/STM.md) |
| `automotive-mbt-thesis` | 🟢 直接可用 | 1 | BBW ABS 行为图直接给出了 Entry/CalcSlipRate/Exit 三态。 | [STM](sources/automotive-mbt-thesis/STM.md) |
| `automotive-temporal-logic-benchmarks` | 🟢 直接可用 | 1 | 自动变速器基准模型明确给出了 gear FSM 和 shift guard。 | [STM](sources/automotive-temporal-logic-benchmarks/STM.md) |
| `avens-uas` | ⚪ 未收获 | 0 | 聚焦飞行/网络联合仿真，不提供可复用的控制系统状态机描述。 | [STM](sources/avens-uas/STM.md) |
| `cara-infusion-pump-formal-spec` | 🟢 直接可用 | 2 | OCR 后可稳定提取泵模式与 cuff handler 的状态/回退逻辑。 | [STM](sources/cara-infusion-pump-formal-spec/STM.md) |
| `cps-security-analysis-sysml` | ⚪ 未收获 | 0 | 重点是 CPS 安全威胁/攻击路径，不是控制对象行为状态机。 | [STM](sources/cps-security-analysis-sysml/STM.md) |
| `design-pillars-medical-cps` | ⚪ 未收获 | 0 | 是中间件设计原则，不是具体控制系统状态机。 | [STM](sources/design-pillars-medical-cps/STM.md) |
| `dual-chamber-pacemaker` | 🟢 直接可用 | 2 | 既有基础 DDD 节律控制，也有 DDD/VDI 模式切换。 | [STM](sources/dual-chamber-pacemaker/STM.md) |
| `east-adl-formal-analysis` | 🟡 可整理 | 1 | BBW ABS 逻辑清晰，但正文把状态机更多留给 TA 模型/工具层。 | [STM](sources/east-adl-formal-analysis/STM.md) |
| `fault-handling-plc-industry4` | 🟢 直接可用 | 2 | 既有通用 operation modes，又有 abort/reset/start 的实际切换链路。 | [STM](sources/fault-handling-plc-industry4/STM.md) |
| `holonic-control-validation` | ⚪ 未收获 | 0 | Petri 网验证很强，但抽取文本里缺少可直接落数据集的具体控制对象状态描述。 | [STM](sources/holonic-control-validation/STM.md) |
| `hytech-hybrid-systems` | 🟢 直接可用 | 1 | 恒温器自动机是标准的控制对象状态机示例。 | [STM](sources/hytech-hybrid-systems/STM.md) |
| `ics-vulnerability-knowledge-base` | ⚪ 未收获 | 0 | ICS 组件与攻击路径描述为主，不是控制行为状态机。 | [STM](sources/ics-vulnerability-knowledge-base/STM.md) |
| `iec61499-realtime-semantics` | 🟡 可整理 | 1 | BFB/ECC 本身就是有限状态控制器，但示例状态名主要在图里。 | [STM](sources/iec61499-realtime-semantics/STM.md) |
| `iec61499-soa-review` | ⚪ 未收获 | 0 | 综述型论文，没有可追溯的控制状态设计。 | [STM](sources/iec61499-soa-review/STM.md) |
| `iec61499-vs-61131` | ⚪ 未收获 | 0 | 有 ECC 示例，但对象是泛化 counter FB，不作为控制系统需求样本。 | [STM](sources/iec61499-vs-61131/STM.md) |
| `industrial-strength-mbt` | ⚪ 未收获 | 0 | 模型测试方法综述，不是控制系统设计原文。 | [STM](sources/industrial-strength-mbt/STM.md) |
| `model-driven-iec61131-development` | ⚪ 未收获 | 0 | 有 Feeder FB/SFC 背景，但正文没有把状态和转移文本化到可追溯程度。 | [STM](sources/model-driven-iec61131-development/STM.md) |
| `plc-course-fsm` | 🟢 直接可用 | 2 | 给出了非常干净的 box-fill 三态 FSM 和 auto/standby 二态 FSM。 | [STM](sources/plc-course-fsm/STM.md) |
| `plc-software-modularity` | ⚪ 未收获 | 0 | 列出了 operation modes，但没有具体控制对象的转移逻辑。 | [STM](sources/plc-software-modularity/STM.md) |
| `safeslice` | ⚪ 未收获 | 0 | 出现的模式是工具模式，不是控制系统模式。 | [STM](sources/safeslice/STM.md) |
| `secure-safe-embedded-mde` | ⚪ 未收获 | 0 | 文中状态机主要对应密钥分发协议，不是控制系统对象。 | [STM](sources/secure-safe-embedded-mde/STM.md) |
| `smart-manufacturing-standards-nist` | ⚪ 未收获 | 0 | 标准/参考架构综述，不提供状态机行为细节。 | [STM](sources/smart-manufacturing-standards-nist/STM.md) |
| `sysml-safety-analysis-integration` | 🟢 直接可用 | 1 | 飞机轮刹系统四模态自动机非常适合状态机需求样本。 | [STM](sources/sysml-safety-analysis-integration/STM.md) |
| `sysml-safety-critical-design-process` | ⚪ 未收获 | 0 | 更偏设计流程方法，缺少具体控制对象状态机正文。 | [STM](sources/sysml-safety-critical-design-process/STM.md) |
| `sysmlv2-avionics` | ⚪ 未收获 | 0 | 探索 SysML v2 建模能力，没有可追溯控制状态样本。 | [STM](sources/sysmlv2-avionics/STM.md) |
| `system-architecture-virtual-integration` | ⚪ 未收获 | 0 | 以体系结构/虚拟集成为主，状态逻辑多停留在工具链层。 | [STM](sources/system-architecture-virtual-integration/STM.md) |
| `tasm-toolset` | ⚪ 未收获 | 0 | 只说明工具曾用于 Electronic Throttle Controller，没有给出状态细节。 | [STM](sources/tasm-toolset/STM.md) |
| `time-complemented-automation-architecture` | 🟢 直接可用 | 1 | Sorter1 的控制流非常适合作为分布式自动化状态/转移样本。 | [STM](sources/time-complemented-automation-architecture/STM.md) |
| `vital-east-adl-uppaal` | 🟡 可整理 | 1 | 有 BBW 功能约束和 fp 执行周期，但显式状态较少。 | [STM](sources/vital-east-adl-uppaal/STM.md) |

### 说明

- `🟢 直接可用`：正文已明确给出控制对象、状态/模式与转移/guard，可直接进入后续自然语言状态机数据整理。
- `🟡 可整理`：正文明确给出控制逻辑或 automata 执行语义，但部分状态信息更多保存在图或工具语义里，整理时需要轻度补形。
- `⚪ 暂未收获`：要么论文主题不是控制对象行为本身，要么 `paper_content.txt` 中没有足够具体、可追溯的状态/转移描述。
- `CARA` 的 `paper_content.txt` 已改为 OCR 版，以便 `STM.md` 的页码/段落定位可靠。
