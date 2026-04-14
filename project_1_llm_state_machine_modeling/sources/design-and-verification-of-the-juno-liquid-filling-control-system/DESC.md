# JUNO 液体填充控制系统论文 / Design and Verification of the JUNO Liquid Filling Control System

## 论文在讲什么

这篇论文围绕 JUNO 中央探测器的 `Filling / Overflow / Circulation`（FOC）系统，说明一个大型液体处理系统如何在高可靠 PLC 架构下长期稳定运行。它不仅讨论连续量调节，还明确涉及液位、压力、流量、温度、overflow/refill 和在线循环这些过程控制问题，因此不是单纯的实验装置介绍。

对我们最重要的是，作者把控制系统写成了“分层控制 + 顺序控制 + 安全联锁”的组合体。也就是说，论文不是只给 PID 曲线，而是说明哪些条件满足后才能启动下一步、何时需要切换填充/回补/循环模式、压力异常时怎样自动停泵，因而可以稳定抽成过程监督状态机样本。

## 控制系统在文中的位置

FOC 控制系统是正文的核心对象之一，而不是附带配套设施。JUNO 的液体填充既关系到探测器结构安全，也关系到液体纯度和 20 年寿命期内的稳定运行，所以控制逻辑在文中占据了非常实质的位置。作者专门给出需求、控制架构、典型逻辑类型和测试结果，这些章节都围绕同一套控制系统展开。

尤其值得注意的是，论文明确区分了 detection、control、monitoring & safety 三层，并在 control layer 里把 `PID / sequential control / safety interlock / split-range & selective control` 分开说明。对于我们做 `STM` 抽取，这意味着可以把离散监督逻辑和连续调节逻辑区分开来，而不用把整篇过程控制论文误判成纯连续控制。

## 对我们为什么有用

这篇论文补的是 `🌡️ + EFSM + T1` 的大体积液体处理过程样本。仓库里过程控制方向已有水箱、闸门、能源管理、批混等案例，但像 JUNO 这样同时包含 filling、overflow、circulation、threshold gating、独立 safety interlock 的监督控制器还不多，尤其适合补“顺序执行 + 安全前置条件 + 模式切换”这一类语义。

它也有助于防止误收这类科学实验装置论文。很多实验系统论文只会讲工艺流程或硬件配置，不足以抽成状态机；而这篇不同，它把顺序控制条件、阈值前提、overflow 回补和独立联锁都写成了工程控制规则，因此确实能达到双 A。

## 如果需要人工细读，建议怎么读

如果要人工重做或复核 `STM.md`，建议先读第 1-3 页的 system requirement 与 FOC 职责，只确认系统边界和主要物理对象。随后直接跳到第 8-11 页的 Section 3，看 `Architecture of the control logic` 与 `Typical control logic types and application scenarios`，重点标出顺序控制的前置条件、独立 interlock、standby activation 和 overflow/refill 的阈值触发。

第 11-14 页的测试章节则适合第二轮补证时再读，用来确认这些模式不是纸面规格，而是在 LS transfer、overflow、filling 等工况里真实执行过。至于大量硬件选型、传感器精度和物理实验背景，可以放到更后面再看；第一次人工细读应优先锁定 supervisory logic 本身。
