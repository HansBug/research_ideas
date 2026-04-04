# 长时全自主旋翼无人机遥感数据采集运行 / Long-Duration Fully Autonomous Operation of Rotorcraft UAS for Remote-Sensing Data Acquisition

## 论文在讲什么

这篇论文解决的是长时户外自主旋翼无人机如何反复执行“起飞-采集-返航-着陆-充电”任务循环的问题。输入是电池状态、起飞前健康检查、航点任务、着陆点视觉可见性和紧急事件，方法是把 autonomy engine 组织成 `master + phase-specific autopilot` 的层次状态机，输出是可在真实充电站上连续自主运行数小时的任务控制系统。
从论文的展开方式看，输入侧主要落在 battery status、motor nominal performance、mission waypoint/hover plan、landing pad visibility、touchdown detection，核心做法是 master state machine 调度 `takeoff / mission / landing / emergency landing` 四个 autopilot，最终形成的则是 可长时运行的自主飞行任务控制逻辑、视觉回充落点对准流程和应急降落回退链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置

这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是一个真实的 rotorcraft UAS 与地面 landing station 联合系统，不是泛化的无人机框架。系统能在用户只给出一次任务后反复执行自主飞行、着陆、充电和再次起飞，并已在室内外实验中完成多次无人值守飞行循环。
原文明确说明高层自主决策采用 `hierarchy of master and slave state machines`。其中，例如 master state machine 负责选择当前任务阶段、slave / autopilot state machines 分别实现 `takeoff`、`mission`、`landing` 和 `emergency landing` 的具体逻辑。 这篇论文对 `project_1` 很有价值的一点，是它把每个阶段的控制动作写得相当具体，例如 起飞前要检查 battery voltage 和 motor nominal performance、`takeoff` 中要重新初始化状态估计器并记住返航位置、`landing` 中先检查 AprilTag 着陆标记是否可见；不可见时进入 spiral grid search。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补充了 `sources` 中高质量的真实 UAV 任务管理样本。 它不是连续控制律论文，而是把高层 mission control 的状态骨架直接写清楚。 它能提供“正常任务链 + 异常回退链 + 真实实验验证”三者同时具备的 source 证据。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `master state + phase autopilot` 的层次化写法、从健康检查、返航、视觉搜索到 touchdown 判定的自然语言组织方式、把 low battery、motor fault、pad invisible 这些异常条件写成高层模式切换触发器 这些最容易直接转成状态机自然语言描述的部分。 论文的低层控制与感知仍包含较多导航/视觉实现细节，不应整段混入状态机文本。 真正的 autopilot 内部图主要依赖文中流程图，抽取时需要结合相关图示理解。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

## 如果需要人工细读，建议怎么读

如果后续是为了人工复核 `STM.md`、重做案例抽取，或确认这篇论文能否稳定进入数据集，建议先看 第 1 页起的摘要与引言，只用来确认系统边界、控制对象和本文到底是在讲系统设计还是在讲方法。随后直接跳到 第 19-22 页附近关于 master state machine、mission autopilot、landing autopilot 和 emergency landing autopilot 的正文，优先人工标出状态/模式名、状态进入与退出条件、事件或 guard、局部时间量、状态内动作，以及 nominal / abnormal / hold / retreat 这类分支；最后再用 第 23-31 页的实验结果、运行模式对比和长时自主运行记录 去核对这些状态在完整系统或实验场景里是怎样串起来的，借此区分“主控制链”与“只为实现服务的细节”。
像 第 11-18 页更偏 visual landing navigation、轨迹生成与低层控制回路的内容 这类更偏低层模型、连续控制律、感知/估计、硬件实现或数学推导的内容，通常可以放到第二轮再看；除非你是在追某个阈值、guard 或时间条件到底从哪一节推出来。换句话说，这一节的目的不是复读 `STM.md`，而是在 `STM.md` 不再可靠甚至需要重做时，仍然给人工一条稳定的原文阅读顺序：先锁定系统边界，再锁定状态骨架和转移条件，最后才回头补低层推导与性能细节。
