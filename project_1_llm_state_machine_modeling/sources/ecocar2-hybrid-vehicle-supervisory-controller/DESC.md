# EcoCAR 2 混合动力汽车高层监督控制 / Hybrid Vehicle Supervisory Controller Development Process to Minimize Emissions and Fuel Consumption in EcoCAR 2

## 论文在讲什么

这篇论文表面上是一篇关于 supervisory controller development process 的硕士论文，但它并不只停留在流程方法。作者围绕一辆 EcoCAR 2 比赛用的 plug-in hybrid electric vehicle，系统说明了车辆硬件、Simulink 架构、诊断层和高层 mode-selection logic，并把不同驱动模式如何切换写成了明确的控制策略。

从我们关心的角度看，最重要的不是版本管理或 plant-model 搭建，而是第 `3.2-3.3` 节里的 hybrid supervisory control modes。论文把 `Charge Depleting`、`Charge Sustaining`、`Performance mode`、`ICE Only mode` 以及 fault fallback 的切换条件写得非常清楚，包括 `SOC` 阈值、speed threshold、component online/offline 诊断以及 `2 seconds` 的驾驶员触发条件。

## 控制系统在文中的位置

这套控制系统描述在文中属于核心车辆控制对象，不是陪衬案例。虽然论文有不少篇幅在讲 model-based development、plant model 和 HIL/SIL 测试，但这些内容都是为了服务 HSC，也就是 Hybrid Supervisory Controller 的设计、验证和落地。

更具体地说，我们真正需要抽取的控制链是“在当前系统诊断状态和车辆工况下，该让前后桥哪套动力系统出力、以什么模式出力、何时升降级、何时进入性能模式或 limp-home 模式”。这部分控制逻辑并没有被埋在图里，而是直接在模式说明章节中展开了。

## 对我们为什么有用

这篇论文对文库的价值在于，它提供了一个汽车方向里较少见的“高层能量/动力模式 supervisor”样本。它不是轨迹跟踪、避障或行为规划，而是 vehicle architecture 上层的 mode manager；同时又不像很多混动论文那样只给优化目标和仿真曲线，而是把离散模式、阶段推进和故障回退链明确写成文本。

从建模角度看，它很适合做 `EFSM + T1` 的车辆样本。状态切换依赖的不只是事件，还有 `SOC`、speed threshold、diagnostic status 和 pedal hold duration；此外，`Charge Sustaining` 自身还包含 electric launch、engine blend-in、ICE propulsion with load shifting 这样的阶段性子链，适合后续训练模型学习“一个 mode 里还可以有更细的 phase progression”。

## 如果需要人工细读，建议怎么读

如果要人工重读，建议先跳到 `paper_content.txt` 对应第 `49-55` 页。第一轮只读 `Mode Selection Logic Structure`、`Charge Depleting`、`Charge Sustaining` 和 `Additional Modes`，把模式集合、进入条件、每个模式下哪套动力系统接管，以及 `2-second` performance trigger 圈出来。

第二轮再回看前面的 system-level diagnostics 部分，确认 `Online / Offline / Limited` 是如何决定 `ICE Only` 与 fallback-to-CD 这些降级分支的。更后面的 plant-model 建立、参数验证和 competition testing 章节可以放到最后；它们对理解工程背景有帮助，但不是重建监督状态机主链的首要证据。
