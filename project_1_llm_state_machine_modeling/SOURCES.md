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

- 已收录论文：**88** 篇
- 本轮新增论文：**58** 篇
- 本轮下载失败记录：**39** 条
- 已完成 STM 梳理：**30** 篇
- ⏳ 尚未提取 STM：**58** 篇
- 本轮新增目录均已包含：PDF 原文、`bibtex.bib`、自动生成的 `paper_content.txt`。本轮未生成 `STM.md`。

## 论文清单

- 更新于：`2026-03-11 19:52:53`
- 本次更新：新增 **58** 篇，当前累计 **88** 篇
- 检索策略：基于 `BASELINE.md` 中 `ALL-IN-ONE 综合检索关键词`，按“控制对象/系统类型 + design/requirements/specification/modeling/verification + state machine/FSM/statechart/formal method”等组合继续扩展检索，并优先保留可直接获取 PDF 与较完整 BibTeX 的开放文献
- 本轮侧重：铁路联锁与轨交控制、医疗设备闭环控制、车载控制（ACC/ABS/BBW/车队协同）、PLC/电梯/交通灯/停车控制，以及无人机/飞控/起落架等航空航天控制

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
| 31 | 🏭 | Adaptive control of robot manipulators with flexible joints | 1992 | 机器人与执行机构控制 | `robot manipulator, flexible joints, adaptive control` | [adaptive-control-of-robot-manipulators-with-flexible-joints](sources/adaptive-control-of-robot-manipulators-with-flexible-joints/) |
| 32 | 🚗 | Autonomous intelligent cruise control | 1993 | 车载控制与驾驶辅助 | `autonomous intelligent cruise control, vehicle control` | [autonomous-intelligent-cruise-control](sources/autonomous-intelligent-cruise-control/) |
| 33 | 🏭 | Elevator Group Control Using Multiple Reinforcement Learning Agents | 1998 | 工业自动化与离散事件控制 | `elevator group control, reinforcement learning, scheduling` | [elevator-group-control-using-multiple-reinforcement-learning-agents](sources/elevator-group-control-using-multiple-reinforcement-learning-agents/) |
| 34 | 🚆 | Formal modelling and simulation of train control systems using petri nets | 1999 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [formal-modelling-and-simulation-of-train-control-systems-using-petri-net](sources/formal-modelling-and-simulation-of-train-control-systems-using-petri-net/) |
| 35 | ✈️ | Modeling and Validation of a Navy A6-Intruder Actively Controlled Landing Gear System | 1999 | 航空航天与空管控制 | `landing gear system, active control, validation` | [modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin](sources/modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin/) |
| 36 | 🚆 | USING Z SPECIFICATION FOR RAILWAY INTERLOCKING SAFETY | 2001 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [using-z-specification-for-railway-interlocking-safety](sources/using-z-specification-for-railway-interlocking-safety/) |
| 37 | 🏭 | Multi Car Elevator Control by using Learning Automaton | 2005 | 工业自动化与离散事件控制 | `elevator control, learning automaton, multi-car` | [multi-car-elevator-control-by-using-learning-automaton](sources/multi-car-elevator-control-by-using-learning-automaton/) |
| 38 | 🚆 | A formal approach for the construction and verification of railway control systems | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [a-formal-approach-for-the-construction-and-verification-of-railway-contr](sources/a-formal-approach-for-the-construction-and-verification-of-railway-contr/) |
| 39 | 🚆 | Automated Verification of Signalling Principles in Railway Interlocking Systems | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [automated-verification-of-signalling-principles-in-railway-interlocking](sources/automated-verification-of-signalling-principles-in-railway-interlocking/) |
| 40 | 🚆 | Automatic generation and verification of railway interlocking control tables using FSM and NuSMV | 2009 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [automatic-generation-and-verification-of-railway-interlocking-control-ta](sources/automatic-generation-and-verification-of-railway-interlocking-control-ta/) |
| 41 | ✈️ | 3D pose estimation based on planar object tracking for UAVs control | 2010 | 无人机与飞行控制 | `UAV control, pose estimation, planar tracking` | [3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control](sources/3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control/) |
| 42 | 🚆 | Modelling Railway Interlocking Tables Using Coloured Petri Nets | 2010 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [modelling-railway-interlocking-tables-using-coloured-petri-nets](sources/modelling-railway-interlocking-tables-using-coloured-petri-nets/) |
| 43 | ⚙️ | Nonlinear controller design of a ship autopilot | 2010 | 船舶与通用控制系统 | `ship autopilot, nonlinear control` | [nonlinear-controller-design-of-a-ship-autopilot](sources/nonlinear-controller-design-of-a-ship-autopilot/) |
| 44 | ✈️ | On-board and Ground Visual Pose Estimation Techniques for UAV Control | 2010 | 无人机与飞行控制 | `UAV control, visual pose estimation` | [on-board-and-ground-visual-pose-estimation-techniques-for-uav-control](sources/on-board-and-ground-visual-pose-estimation-techniques-for-uav-control/) |
| 45 | ✈️ | Formal Specification and Verification of a Coordination Protocol for an Automated Air Traffic Control System | 2012 | 航空航天与空管控制 | `air traffic control, coordination protocol, formal verification` | [formal-specification-and-verification-of-a-coordination-protocol-for-an](sources/formal-specification-and-verification-of-a-coordination-protocol-for-an/) |
| 46 | 🏭 | Marginalizing Out Future Passengers in Group Elevator Control | 2012 | 工业自动化与离散事件控制 | `elevator group control, passenger modeling, scheduling` | [marginalizing-out-future-passengers-in-group-elevator-control](sources/marginalizing-out-future-passengers-in-group-elevator-control/) |
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
| 57 | 🏭 | High accuracy traffic light controller for increasing the given green time utilization | 2015 | 工业自动化与离散事件控制 | `traffic light controller, green time, traffic control` | [high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti](sources/high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti/) |
| 58 | ✈️ | The landing gear system in multi-machine Hybrid Event-B | 2015 | 航空航天与空管控制 | `landing gear system, Hybrid Event-B, formal model` | [the-landing-gear-system-in-multi-machine-hybrid-event-b](sources/the-landing-gear-system-in-multi-machine-hybrid-event-b/) |
| 59 | ✈️ | UAV Control on the Basis of 3D Landmark Bearing-Only Observations | 2015 | 无人机与飞行控制 | `UAV control, landmark observations, bearing-only` | [uav-control-on-the-basis-of-3d-landmark-bearing-only-observations](sources/uav-control-on-the-basis-of-3d-landmark-bearing-only-observations/) |
| 60 | 🚆 | Verification of railway interlocking systems | 2015 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [verification-of-railway-interlocking-systems](sources/verification-of-railway-interlocking-systems/) |
| 61 | 🚆 | Bond Graph modeling for fault detection and isolation of a train door mechatronic system | 2016 | 铁路与轨道交通设备控制 | `train door system, fault detection, bond graph` | [bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me](sources/bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me/) |
| 62 | 🚆 | Validation process for railway interlocking systems | 2016 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [validation-process-for-railway-interlocking-systems](sources/validation-process-for-railway-interlocking-systems/) |
| 63 | 🏭 | Design &amp; Control of an Elevator Control System using PLC | 2017 | 工业自动化与离散事件控制 | `elevator control, PLC, automation` | [design-amp-control-of-an-elevator-control-system-using-plc](sources/design-amp-control-of-an-elevator-control-system-using-plc/) |
| 64 | 🚗 | Formal verification of autonomous vehicle platooning | 2017 | 车载控制与驾驶辅助 | `autonomous vehicle platooning, formal verification` | [formal-verification-of-autonomous-vehicle-platooning](sources/formal-verification-of-autonomous-vehicle-platooning/) |
| 65 | 🚗 | Integrated Longitudinal and Lateral Networked Control System Design for Vehicle Platooning | 2018 | 车载控制与驾驶辅助 | `vehicle platooning, longitudinal control, lateral control` | [integrated-longitudinal-and-lateral-networked-control-system-design-for](sources/integrated-longitudinal-and-lateral-networked-control-system-design-for/) |
| 66 | 🏭 | Intelligent elevator control and safety monitoring system | 2018 | 工业自动化与离散事件控制 | `elevator control, safety monitoring, intelligent system` | [intelligent-elevator-control-and-safety-monitoring-system](sources/intelligent-elevator-control-and-safety-monitoring-system/) |
| 67 | 🚗 | Networked Cooperative Platoon of Vehicles for Testing Methods and Verification Tools | 2018 | 车载控制与驾驶辅助 | `vehicle platoon, testing methods, verification tools` | [networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi](sources/networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi/) |
| 68 | 🏭 | Automatic traffic light controller for emergency vehicle using peripheral interface controller | 2019 | 工业自动化与离散事件控制 | `traffic light controller, emergency vehicle, PIC` | [automatic-traffic-light-controller-for-emergency-vehicle-using-periphera](sources/automatic-traffic-light-controller-for-emergency-vehicle-using-periphera/) |
| 69 | 🏭 | Features of Automatic Control of Technological Parameters of Water Level in the Drum Steam Boilers | 2019 | 工业自动化与离散事件控制 | `steam boiler, water level control, automatic control` | [features-of-automatic-control-of-technological-parameters-of-water-level](sources/features-of-automatic-control-of-technological-parameters-of-water-level/) |
| 70 | 🚗 | Fuzzy Sliding Mode Wheel Slip Ratio Control for Smart Vehicle Anti-Lock Braking System | 2019 | 车载控制与驾驶辅助 | `anti-lock braking system, wheel slip, fuzzy sliding mode` | [fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock](sources/fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock/) |
| 71 | 🚗 | Modular Verification of Vehicle Platooning with Respect to Decisions, Space and Time | 2019 | 车载控制与驾驶辅助 | `vehicle platooning, modular verification, space and time` | [modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa](sources/modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa/) |
| 72 | 🚗 | Research on Longitudinal Active Collision Avoidance of Autonomous Emergency Braking Pedestrian System (AEB-P) | 2019 | 车载控制与驾驶辅助 | `autonomous emergency braking, collision avoidance, pedestrian` | [research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge](sources/research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge/) |
| 73 | 🏭 | Water Tank Level Controller by using PLC | 2019 | 工业自动化与离散事件控制 | `water tank level control, PLC, controller` | [water-tank-level-controller-by-using-plc](sources/water-tank-level-controller-by-using-plc/) |
| 74 | 🏭 | Data Efficient Reinforcement Learning for Integrated Lateral Planning and Control in Automated Parking System | 2020 | 智能停车与感知控制 | `automated parking system, planning, lateral control` | [data-efficient-reinforcement-learning-for-integrated-lateral-planning-an](sources/data-efficient-reinforcement-learning-for-integrated-lateral-planning-an/) |
| 75 | 🚆 | Information Value-Based Fault Diagnosis of Train Door System under Multiple Operating Conditions | 2020 | 铁路与轨道交通设备控制 | `train door system, fault diagnosis, operating conditions` | [information-value-based-fault-diagnosis-of-train-door-system-under-multi](sources/information-value-based-fault-diagnosis-of-train-door-system-under-multi/) |
| 76 | 🚗 | Review on the Development, Control Method and Application Prospect of Brake-by-Wire Actuator | 2020 | 车载控制与驾驶辅助 | `brake-by-wire actuator, review, control method` | [review-on-the-development-control-method-and-application-prospect-of-bra](sources/review-on-the-development-control-method-and-application-prospect-of-bra/) |
| 77 | 🚗 | Sliding Mode Control Algorithms for Anti-Lock Braking Systems with Performance Comparisons | 2020 | 车载控制与驾驶辅助 | `anti-lock braking system, sliding mode control, comparison` | [sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo](sources/sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo/) |
| 78 | 🏭 | Video-Based Parking Occupancy Detection for Smart Control System | 2020 | 智能停车与感知控制 | `parking control system, occupancy detection, video-based` | [video-based-parking-occupancy-detection-for-smart-control-system](sources/video-based-parking-occupancy-detection-for-smart-control-system/) |
| 79 | ✈️ | An Industrial Quadrotor UAV Control Method Based on Fuzzy Adaptive Linear Active Disturbance Rejection Control | 2021 | 无人机与飞行控制 | `quadrotor UAV, fuzzy adaptive control, ADRC` | [an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea](sources/an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea/) |
| 80 | 🏭 | Intelligent Traffic Light Controller using Fuzzy Logic and Image Processing | 2021 | 工业自动化与离散事件控制 | `traffic light controller, fuzzy logic, image processing` | [intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process](sources/intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process/) |
| 81 | 🚗 | Performance Assessment of an Electric Power Steering System for Driverless Formula Student Vehicles | 2021 | 车载控制与驾驶辅助 | `electric power steering, driverless vehicle, performance assessment` | [performance-assessment-of-an-electric-power-steering-system-for-driverle](sources/performance-assessment-of-an-electric-power-steering-system-for-driverle/) |
| 82 | 🏭 | Traffic Light Controller using Image Processing | 2021 | 工业自动化与离散事件控制 | `traffic light controller, image processing, embedded control` | [traffic-light-controller-using-image-processing](sources/traffic-light-controller-using-image-processing/) |
| 83 | 🚆 | Formal Modeling and Verification of the Functionality of Electronic Urban Railway Control Systems Through a Case Study | 2022 | 铁路联锁与轨交控制验证 | `railway control, train system, verification` | [formal-modeling-and-verification-of-the-functionality-of-electronic-urba](sources/formal-modeling-and-verification-of-the-functionality-of-electronic-urba/) |
| 84 | 🏭 | Research on Path Planning and Tracking Control of Automatic Parking System | 2022 | 工业自动化与离散事件控制 | `automatic parking system, path planning, tracking control` | [research-on-path-planning-and-tracking-control-of-automatic-parking-syst](sources/research-on-path-planning-and-tracking-control-of-automatic-parking-syst/) |
| 85 | 🚗 | Review of Brake-by-Wire System and Control Technology | 2022 | 车载控制与驾驶辅助 | `brake-by-wire system, control technology, review` | [review-of-brake-by-wire-system-and-control-technology](sources/review-of-brake-by-wire-system-and-control-technology/) |
| 86 | 🏭 | A Smart Real-Time Parking Control and Monitoring System | 2023 | 工业自动化与离散事件控制 | `parking control system, monitoring, real-time` | [a-smart-real-time-parking-control-and-monitoring-system](sources/a-smart-real-time-parking-control-and-monitoring-system/) |
| 87 | 🚗 | Design and Assessment of an Anti-lock Braking System Controller | 2023 | 车载控制与驾驶辅助 | `anti-lock braking system, controller design, assessment` | [design-and-assessment-of-an-anti-lock-braking-system-controller](sources/design-and-assessment-of-an-anti-lock-braking-system-controller/) |
| 88 | ✈️ | Model-Based Design of Aircraft Landing Gear System | 2023 | 航空航天与空管控制 | `aircraft landing gear, model-based design, control` | [model-based-design-of-aircraft-landing-gear-system](sources/model-based-design-of-aircraft-landing-gear-system/) |

## 本轮下载失败记录

以下条目是在本轮检索中实际尝试下载但未成功的候选文献。记录失败时间与原因，便于后续避开近期重复尝试。

| # | 分类 | 标题 | 失败时间 | 失败原因 |
|---|---|---|---|---|
| 1 | 🚆 | Formal Verification of a Railway Interlocking System using Model Checking | 2026-03-11 19:32 | https://dl.acm.org/doi/pdf/10.1007/s001650050022 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s001650050022 -> HTML中未发现可下载PDF \| http://hdl.handle.net/11572/20411 -> HTML中未发现可下载PDF |
| 2 | 🚆 | An automatic SPIN validation of a safety critical railway control system | 2026-03-11 19:32 | https://research.utwente.nl/files/6146146/gnesi00automatic.pdf -> 非PDF \| https://research.utwente.nl/en/publications/06fb35d2-62eb-424e-b325-22802fb893a8 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/857524/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/icdsn.2000.857524 -> HTML中未发现可下载PDF |
| 3 | 🚆 | Tracking and collision avoidance of virtual coupling train control system | 2026-03-11 19:33 | https://doi.org/10.1016/j.aej.2020.12.010 -> HTML中未发现可下载PDF \| https://doaj.org/article/352ecde0e746421486256bb016596f38 -> HTML中未发现可下载PDF |
| 4 | 🚆 | Next Generation Train Control (NGTC): More Effective Railways through the Convergence of Main-line and Urban Train Control Systems | 2026-03-11 19:33 | https://doi.org/10.1016/j.trpro.2016.05.152 -> HTML中未发现可下载PDF |
| 5 | 🚆 | How to Deal with Revolutions in Train Control Systems | 2026-03-11 19:33 | https://doi.org/10.1016/j.eng.2016.03.015 -> HTML中未发现可下载PDF \| https://doaj.org/article/22a4c7da7e014d5bb3f2b2c42b4852b0 -> HTML中未发现可下载PDF |
| 6 | 🩺 | A Formal Verification Methodology for DDD Mode Pacemaker Control Programs | 2026-03-11 19:33 | http://downloads.hindawi.com/journals/jece/2015/939028.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2015/939028 -> HTML中未发现可下载PDF \| https://doaj.org/article/2bd2be4fe24545199bc5d22ae671b3bc -> HTML中未发现可下载PDF |
| 7 | 🩺 | Closed-Loop Quantitative Verification of Rate-Adaptive Pacemakers | 2026-03-11 19:33 | https://dl.acm.org/doi/pdf/10.1145/3152767 -> HTML中未发现可下载PDF \| https://doi.org/10.1145/3152767 -> HTML中未发现可下载PDF |
| 8 | 🩺 | New Insights Into Soft-Faults Induced Cardiac Pacemakers Malfunctions Analyzed at System-Level via Model Checking | 2026-03-11 19:33 | https://ieeexplore.ieee.org/document/8493464/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/access.2018.2876318 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/8493464/ -> 非PDF \| https://doaj.org/article/f74ecb7b159a49839c4715126161cffd -> HTML中未发现可下载PDF |
| 9 | 🩺 | Combining human error verification and timing analysis: a case study on an infusion pump | 2026-03-11 19:33 | https://dl.acm.org/doi/pdf/10.1007/s00165-013-0288-1 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s00165-013-0288-1 -> HTML中未发现可下载PDF |
| 10 | 🩺 | An Integrated Multivariable Artificial Pancreas Control System | 2026-03-11 19:33 | https://journals.sagepub.com/doi/pdf/10.1177/1932296814524862 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1932296814524862 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/24876613 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC4455451/pdf/10.1177_1932296814524862.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/10.1177_1932296814524862.pdf -> 非PDF |
| 11 | 🩺 | Meal Detection in Patients With Type 1 Diabetes: A New Module for the Multivariable Adaptive Artificial Pancreas Control System | 2026-03-11 19:34 | https://ieeexplore.ieee.org/document/7124410/ -> 非PDF \| http://doi.org/document/ -> 非PDF \| http://doi.org/10.1109/JBHI.2015.2446413 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7124410/ -> 非PDF \| https://doi.org/document/ -> 非PDF |
| 12 | 🩺 | Event-Triggered Model Predictive Control for Embedded Artificial Pancreas Systems | 2026-03-11 19:34 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5839516/pdf/nihms944924.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/nihms944924.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/5839516 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7932935/ -> 非PDF \| https://doi.org/document/ -> 非PDF |
| 13 | 🩺 | Adaptive Control of Artificial Pancreas Systems ‐ A Review | 2026-03-11 19:34 | https://downloads.hindawi.com/journals/jhe/2014/131923.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1260/2040-2295.5.1.1 -> HTML中未发现可下载PDF \| https://onepetro.org/NACECORR/proceedings/CORR03/All-CORR03/NACE-03654/114399 -> HTML中未发现可下载PDF \| https://doaj.org/article/83a4b72eda794e6f9abb6d27ff4c6a31 -> HTML中未发现可下载PDF |
| 14 | 🩺 | The Next Generation of Artificial Pancreas Control Algorithms | 2026-03-11 19:34 | https://journals.sagepub.com/doi/pdf/10.1177/193229680800200115 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/193229680800200115 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/19885184 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC2769707/pdf/dst-02-0105.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/dst-02-0105.pdf -> 非PDF |
| 15 | 🩺 | Multi-level supervision and modification of artificial pancreas control system | 2026-03-11 19:34 | https://www.sciencedirect.com/science/article/am/pii/S0098135418300619?via%3Dihub -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.compchemeng.2018.02.002 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/30287976 -> HTML中未发现可下载PDF \| http://europepmc.org/pmc/articles/PMC6166877 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC6166877/pdf/nihms942006.pdf -> 非PDF |
| 16 | 🩺 | Artificial Pancreas Device Systems for the Closed-Loop Control of Type 1 Diabetes | 2026-03-11 19:34 | https://journals.sagepub.com/doi/pdf/10.1177/1932296815617968 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1932296815617968 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/26589628 -> HTML中未发现可下载PDF \| http://dst.sagepub.com/content/early/2015/11/20/1932296815617968.full.pdf+html -> curl: (60) SSL certificate problem: certificate has expired More details here: https://curl.se/docs/sslcerts.html  |
| 17 | 🩺 | Simulation Environment to Evaluate Closed-Loop Insulin Delivery Systems in Type 1 Diabetes | 2026-03-11 19:35 | https://journals.sagepub.com/doi/pdf/10.1177/193229681000400117 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/193229681000400117 -> HTML中未发现可下载PDF \| https://pubmed.ncbi.nlm.nih.gov/20167177 -> HTML中未发现可下载PDF \| https://pmc.ncbi.nlm.nih.gov/articles/PMC2825634/pdf/dst-04-0132.pdf -> 非PDF \| https://www.ncbi.nlm.nih.gov/pmc/articles/pdf/dst-04-0132.pdf -> 非PDF |
| 18 | 🚗 | The Impact of Cooperative Adaptive Cruise Control on Traffic-Flow Characteristics | 2026-03-11 19:35 | http://infoscience.epfl.ch/record/188484 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/4019451/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/tits.2006.884615 -> HTML中未发现可下载PDF \| https://research.utwente.nl/files/6843867/Arem06impact.pdf -> 非PDF |
| 19 | 🚗 | Design and experimental evaluation of cooperative adaptive cruise control | 2026-03-11 19:35 | https://research.tue.nl/files/73899058/Ploeg_2011_Design_and_Experimental_Evaluation_of_Cooperative_Adaptive_Cruise_Control.pdf -> 非PDF \| https://research.tue.nl/en/publications/4f434e73-cc96-434f-9c89-addcca8352a6 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/6082981/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/itsc.2011.6082981 -> HTML中未发现可下载PDF |
| 20 | 🚗 | Cooperative Adaptive Cruise Control: A Reinforcement Learning Approach | 2026-03-11 19:36 | https://ieeexplore.ieee.org/document/5876320/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/tits.2011.2157145 -> HTML中未发现可下载PDF |
| 21 | 🚗 | Developing a platoon-wide Eco-Cooperative Adaptive Cruise Control (CACC) system | 2026-03-11 19:36 | https://escholarship.org/content/qt1gf0c6r9/qt1gf0c6r9.pdf -> HTML中未发现可下载PDF \| https://escholarship.org/uc/item/1gf0c6r9 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/7995884/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/ivs.2017.7995884 -> HTML中未发现可下载PDF |
| 22 | 🚗 | Transient fault tolerant control for vehicle brake-by-wire systems | 2026-03-11 19:37 | https://dspace.lboro.ac.uk/2134/20830 -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.ress.2016.01.001 -> HTML中未发现可下载PDF |
| 23 | 🚗 | A Survey of Brake-by-Wire System for Intelligent Connected Electric Vehicles | 2026-03-11 19:37 | https://ieeexplore.ieee.org/ielx7/6287639/6514899/09268150.pdf -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/9268150/ -> 非PDF \| https://doi.org/document/ -> 非PDF \| https://doi.org/10.1109/access.2020.3040184 -> HTML中未发现可下载PDF \| https://ieeexplore.ieee.org/document/9268150/ -> 非PDF |
| 24 | 🚗 | Data-driven model-free slip control of anti-lock braking systems using reinforcement Q-learning | 2026-03-11 19:37 | https://ro.ecu.edu.au/ecuworkspost2013/4015 -> HTML中未发现可下载PDF \| https://doi.org/10.1016/j.neucom.2017.08.036 -> HTML中未发现可下载PDF |
| 25 | 🚗 | A Study of Coordinated Vehicle Traction Control System Based on Optimal Slip Ratio Algorithm | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/mpe/2016/3413624.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2016/3413624 -> HTML中未发现可下载PDF \| https://doaj.org/article/a2fda65a0c484a7086b7b289fe523de2 -> HTML中未发现可下载PDF |
| 26 | 🚗 | Development of a new traction control system using ant colony optimization | 2026-03-11 19:38 | https://journals.sagepub.com/doi/pdf/10.1177/1687814018792152 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/1687814018792152 -> HTML中未发现可下载PDF \| https://doaj.org/article/5de7d0442548412b8a857a990f435ddd -> HTML中未发现可下载PDF |
| 27 | 🚗 | Autonomous rear-end collision avoidance using an electric power steering system | 2026-03-11 19:38 | https://dspace.lboro.ac.uk/2134/17359 -> HTML中未发现可下载PDF \| https://doi.org/10.1177/0954407014567517 -> HTML中未发现可下载PDF |
| 28 | 🚗 | Torque Control of Electric Power Steering Systems Based on Improved Active Disturbance Rejection Control | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/mpe/2020/6509607.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2020/6509607 -> HTML中未发现可下载PDF \| https://doaj.org/article/705dd5f3ac4f420c893249e7eaf78db4 -> HTML中未发现可下载PDF |
| 29 | 🚗 | Design of the Auto Electric Power Steering System Controller | 2026-03-11 19:38 | https://doi.org/10.1016/j.proeng.2012.01.466 -> HTML中未发现可下载PDF |
| 30 | 🚗 | A Systematic Review of Autonomous Emergency Braking System: Impact Factor, Technology, and Performance Evaluation | 2026-03-11 19:38 | https://downloads.hindawi.com/journals/jat/2022/1188089.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.1155/2022/1188089 -> HTML中未发现可下载PDF \| https://doaj.org/article/ba6ca96049d846d3ab2b2f79b07c87f2 -> HTML中未发现可下载PDF |
| 31 | 🏭 | Wireless Traffic Light Controller | 2026-03-11 19:38 | https://doi.org/10.1016/j.proeng.2011.03.035 -> HTML中未发现可下载PDF |
| 32 | 🏭 | Design of Smart Traffic Light Controller Using Embedded System | 2026-03-11 19:39 | https://doi.org/10.9790/0661-01013033 -> HTML中未发现可下载PDF |
| 33 | 🏭 | Implementation of an Electro-Pneumatic Prototype Elevator Controlled by PLC | 2026-03-11 19:39 | https://etj.uotechnology.edu.iq/article_108840_232d4fe1493af04f96c54c2d0a56b6b1.pdf -> HTML中未发现可下载PDF \| https://doi.org/10.30684/etj.2015.108840 -> HTML中未发现可下载PDF \| https://etj.uotechnology.edu.iq/article_108840_232d4fe1493af04f96c54c2d0a56b6b1.pdf -> 非PDF \| https://doaj.org/article/94e938798aaa4ec4b9d59b2f8cb82e45 -> HTML中未发现可下载PDF |
| 34 | 🏭 | Process sequencing for a pick-and-place robot in a real-life flexible robotic cell | 2026-03-11 19:39 | https://research.manchester.ac.uk/en/publications/7451ccd3-3ad3-47c5-9400-61c940becb13 -> HTML中未发现可下载PDF \| https://link.springer.com/content/pdf/10.1007/s00170-019-03739-6.pdf -> 非PDF \| https://doi.org/10.1007/s00170-019-03739-6#icon-eds-i-download-medium -> 非PDF \| https://doi.org/10.1007/s00170-019-03739-6 -> HTML中未发现可下载PDF \| https://www.research.manchester.ac.uk/portal/en/publications/process-se |
| 35 | 🏭 | PLC Batch Process Control Design and Implementation Fundamentals | 2026-03-11 19:40 | https://doi.org/10.36548/jei.2020.3.001 -> HTML中未发现可下载PDF \| http://doi.org/10.36548/jei.2020.3.001 -> HTML中未发现可下载PDF |
| 36 | 🏭 | Modelling and verification of an automatic controller for a water treatment mixing tank | 2026-03-11 19:40 | https://doi.org/10.5004/dwt.2019.24143 -> HTML中未发现可下载PDF |
| 37 | ✈️ | Eliminating synchronization faults in air traffic control software via design for verification with concurrency controllers | 2026-03-11 19:40 | https://hdl.handle.net/11511/30420 -> curl: (28) Operation timed out after 44028 milliseconds with 0 bytes received \| https://link.springer.com/content/pdf/10.1007/s10515-007-0008-2.pdf -> 非PDF \| https://doi.org/10.1007/s10515-007-0008-2#icon-eds-i-download-medium -> 非PDF \| https://doi.org/10.1007/s10515-007-0008-2 -> HTML中未发现可下载PDF \| http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.138.431 |
| 38 | ✈️ | Bifurcation Analysis of a Nose Landing Gear System | 2026-03-11 19:42 | https://research-information.bris.ac.uk/files/66353645/Cooper_AIAA2016_FULL_PAPER_12072015FINALv1_1_.pdf -> 非PDF \| https://research-information.bris.ac.uk/en/publications/53c3434d-4520-43b3-b8ca-eaf13192c7df -> HTML中未发现可下载PDF \| https://research-information.bris.ac.uk/files/66353645/Cooper_AIAA2016_FULL_PAPER_12072015FINALv1_1_.pdf -> 非PDF \| https://hdl.handle.net/files/66353645/Cooper_AIAA2016_FUL |
| 39 | ✈️ | Indoor UAV Control Using Multi-Camera Visual Feedback | 2026-03-11 19:45 | https://dspace.lboro.ac.uk/2134/17856 -> HTML中未发现可下载PDF \| https://doi.org/10.1007/s10846-010-9506-8 -> HTML中未发现可下载PDF \| https://scholarworks.unist.ac.kr/handle/201301/20220 -> HTML中未发现可下载PDF |

## 状态机描述收获盘点

- ✅ 直接可用论文：**10** 篇
- 🟡 可整理论文：**3** 篇
- ⚪ 暂未收获论文：**17** 篇
- ⏳ 尚未提取论文：**58** 篇
- 🧾 已提取到的状态机/控制逻辑条目：**17** 条
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

<!-- AUTO-PENDING-ROWS-BEGIN -->
| `adaptive-control-of-robot-manipulators-with-flexible-joints` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `autonomous-intelligent-cruise-control` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `elevator-group-control-using-multiple-reinforcement-learning-agents` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `formal-modelling-and-simulation-of-train-control-systems-using-petri-net` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `modeling-and-validation-of-a-navy-a6-intruder-actively-controlled-landin` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `using-z-specification-for-railway-interlocking-safety` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `multi-car-elevator-control-by-using-learning-automaton` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `a-formal-approach-for-the-construction-and-verification-of-railway-contr` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `automated-verification-of-signalling-principles-in-railway-interlocking` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `automatic-generation-and-verification-of-railway-interlocking-control-ta` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `3d-pose-estimation-based-on-planar-object-tracking-for-uavs-control` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `modelling-railway-interlocking-tables-using-coloured-petri-nets` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `nonlinear-controller-design-of-a-ship-autopilot` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `on-board-and-ground-visual-pose-estimation-techniques-for-uav-control` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `formal-specification-and-verification-of-a-coordination-protocol-for-an` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `marginalizing-out-future-passengers-in-group-elevator-control` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `cooperative-adaptive-cruise-control-in-real-traffic-situations` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `experimental-verification-of-vehicle-platoon-control-algorithms` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `online-predictive-diagnosis-of-electrical-train-door-systems` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `reactive-approach-for-autonomous-vehicle-platoon-systems-modelling-and-v` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `adaptive-cascade-control-of-a-brake-by-wire-actuator-for-sport-motorcycl` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `architecture-description-language-for-cyber-physical-systems-analysis-a` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `automated-verification-of-quantitative-properties-of-cardiac-pacemaker-s` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `developing-and-verifying-user-interface-requirements-for-infusion-pumps` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `modeling-cooperative-and-autonomous-adaptive-cruise-control-dynamic-resp` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `performance-evaluation-of-an-anti-lock-braking-system-for-electric-vehic` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `high-accuracy-traffic-light-controller-for-increasing-the-given-green-ti` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `the-landing-gear-system-in-multi-machine-hybrid-event-b` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `uav-control-on-the-basis-of-3d-landmark-bearing-only-observations` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `verification-of-railway-interlocking-systems` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `bond-graph-modeling-for-fault-detection-and-isolation-of-a-train-door-me` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `validation-process-for-railway-interlocking-systems` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `design-amp-control-of-an-elevator-control-system-using-plc` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `formal-verification-of-autonomous-vehicle-platooning` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `integrated-longitudinal-and-lateral-networked-control-system-design-for` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `intelligent-elevator-control-and-safety-monitoring-system` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `networked-cooperative-platoon-of-vehicles-for-testing-methods-and-verifi` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `automatic-traffic-light-controller-for-emergency-vehicle-using-periphera` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `features-of-automatic-control-of-technological-parameters-of-water-level` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `fuzzy-sliding-mode-wheel-slip-ratio-control-for-smart-vehicle-anti-lock` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `research-on-longitudinal-active-collision-avoidance-of-autonomous-emerge` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `water-tank-level-controller-by-using-plc` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `data-efficient-reinforcement-learning-for-integrated-lateral-planning-an` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `information-value-based-fault-diagnosis-of-train-door-system-under-multi` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `review-on-the-development-control-method-and-application-prospect-of-bra` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `sliding-mode-control-algorithms-for-anti-lock-braking-systems-with-perfo` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `video-based-parking-occupancy-detection-for-smart-control-system` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `an-industrial-quadrotor-uav-control-method-based-on-fuzzy-adaptive-linea` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `intelligent-traffic-light-controller-using-fuzzy-logic-and-image-process` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `performance-assessment-of-an-electric-power-steering-system-for-driverle` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `traffic-light-controller-using-image-processing` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `formal-modeling-and-verification-of-the-functionality-of-electronic-urba` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `research-on-path-planning-and-tracking-control-of-automatic-parking-syst` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `review-of-brake-by-wire-system-and-control-technology` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `a-smart-real-time-parking-control-and-monitoring-system` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `design-and-assessment-of-an-anti-lock-braking-system-controller` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
| `model-based-design-of-aircraft-landing-gear-system` | ⏳ 尚未提取 | - | 本轮新增文献，已完成 PDF/BibTeX/文本整理，待后续 STM 提取。 | 尚未提取 |
<!-- AUTO-PENDING-ROWS-END -->

### 说明

- `🟢 直接可用`：正文已明确给出控制对象、状态/模式与转移/guard，可直接进入后续自然语言状态机数据整理。
- `🟡 可整理`：正文明确给出控制逻辑或 automata 执行语义，但部分状态信息更多保存在图或工具语义里，整理时需要轻度补形。
- `⚪ 暂未收获`：要么论文主题不是控制对象行为本身，要么 `paper_content.txt` 中没有足够具体、可追溯的状态/转移描述。
- `⏳ 尚未提取`：新增文献已完成 PDF/BibTeX/文本整理，但尚未创建 `STM.md`，待后续继续抽取。
- `CARA` 的 `paper_content.txt` 已改为 OCR 版，以便 `STM.md` 的页码/段落定位可靠。
