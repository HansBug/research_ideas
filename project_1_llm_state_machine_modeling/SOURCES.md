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
