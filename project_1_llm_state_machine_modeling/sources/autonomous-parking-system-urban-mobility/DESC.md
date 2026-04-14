# 城市自动泊车系统 / Transport Automation in Urban Mobility: A Case Study of an Autonomous Parking System

## 论文在讲什么

这篇论文研究的是一个面向城市道路和公共停车设施的 autonomous parking system，目标不是只做局部泊车轨迹，而是把驾驶员、车辆、停车基础设施和移动端应用放进同一条自动化链路里。作者以一辆经过自动化改装的电动车为平台，讨论了 MQTT 通信、车载与移动端 HMI、并行/垂直泊车场景，以及真实停车场中的验证流程，整体上是一篇非常工程化的系统论文。

但它最重要的价值不在通信平台本身，而在于作者明确把整个 APS 的运行过程组织成从 `drop-off zone` 到 `pick-up zone` 的完整功能场景。论文不是停留在“可以自动泊车”这种泛化说法，而是把控制交接、驶向目标点、驶入车位、驶出车位、回到取车点这些环节逐一写开，并补出车辆何时接管、何时停车、何时中止、何时把控制权交还给司机。

## 控制系统在文中的位置

这篇论文里的控制系统描述是主体，而不是验证方法附带的一个小案例。虽然文中前半部分用了不少篇幅讲 HMI 和 MQTT 通信，但这些内容最终都是为 APS 的主控制链服务的。停车确认、车位保留、自动行驶、自动入位、自动离位和最终 handover 并不是各自分离的功能点，而是被作者当作一个连续的 automated cycle 来设计和测试。

从 `sources/` 的口径看，它尤其有价值的一点是：这里保留下来的不是单纯的“泊车轨迹规划器”，也不是只负责识别空车位的感知模块，而是一个系统级 supervisor。论文把上层生命周期和下层动作包都写出来了，例如 `straight/curved lane`、`turning left/right`、`accelerate/decelerate`、`reverse driving`，再加上 `driver abort`、`connectivity loss`、`unsafe condition` 这些中止条件，构成了完整而可追溯的离散控制链。

## 对我们为什么有用

这篇论文对 `sources/` 的意义，在于它补的是停车方向里相对稀缺的“系统级流程样本”，而不是近几轮频繁出现的 occupancy detection、meter/pricing、或弱化成课程原型的停车短文。它把 `drop-off -> park -> recall -> pick-up` 这条完整用户流程保住了，因此特别适合作为后续 `NL -> state machine` 数据集中“用户接管点明确、异常中止点明确、阶段推进明确”的样本。

它同时也有助于纠正停车方向的检索偏差。很多题名虽然也写 `parking system`，但正文往往偏轨迹、感知或局部模块；而这篇论文真正值得留下，是因为它把系统状态推进写到了能直接抽成 supervisor 的程度。对于后续继续扩停车领域样本，这种“系统级生命周期 + 明确交接与中止条件”的写法，比只给控制曲线或框图的文章要有用得多。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `1-2` 页，把系统目标和 “from drop-off to pick-up zones” 这条主线先立住。然后直接跳到第 `11-13` 页的 `4.1 System Requirements` 到 `4.5 Methodology`，这里是最关键的抽样区域：先抽不安全条件和 abort 条件，再抽五个 major functional scenarios，各阶段的完成条件也应一起拿走。接着再看第 `14-16` 页的 `5.2 Test Description`，用真实测试中的 parking reservation、autonomous parking、vehicle recall 和失联制动行为去校对这条状态链是否闭合。

如果只是为了重建 `STM.md`，`optimal speed package` 的连续优化细节、Bayesian decision graph 的局部求解，以及各种 HMI 界面布局都可以放到第二轮再看。它们能帮助理解系统实现方式，但不是第一优先级。第一轮阅读只要把上层生命周期、每个阶段的动作包、以及 abort/standby/handover 条件读稳，就已经足够把这个 APS supervisor 重新抽出来。
