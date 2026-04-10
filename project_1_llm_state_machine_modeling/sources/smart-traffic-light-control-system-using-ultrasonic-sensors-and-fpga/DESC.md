# 超声传感 FPGA 智能交通灯 / Smart Traffic Light Control System using Ultrasonic Sensors and FPGA

## 论文在讲什么

这篇论文设计了一个基于超声传感器和 Edge Artix-7 FPGA 的自适应交通灯控制系统。它不采用固定红绿灯周期，而是用 HC-SR04 测量车道内车辆距离或密度，再由 FPGA 比较两条车道的密度，给密度更高的车道分配绿灯。

正文提供了比较完整的控制链：超声传感器模块有 `IDLE`、`SEND_TRIGGER`、`WAIT_ECHO_START`、`MEASURE_ECHO` 和 `DONE` 状态；传感器控制器每 60 ms 触发测距，并按 10 cm、15 cm、20 cm、30 cm 阈值驱动四个 LED；双超声控制器比较两个车道的结果，决定 green/red LED 输出。

## 控制系统在文中的位置

交通灯控制是论文主体。`System Architecture`、`Finite State Machine`、`Verilog Modules`、`Simulation` 和 `Testing and Results` 都围绕超声测距 FSM 与交通信号输出展开，不是只给了一个硬件框图。

这篇与现有交通灯样本有邻近相似性，但它的差异在于显式状态机落在超声测距与密度比较链上，而不是传统的固定相位红黄绿循环。对库内样本来说，它能补充“传感器测距子 FSM + 信号相位选择”的表达形态。

## 对我们为什么有用

这篇论文适合做 `🚦 + EFSM + T1` 样本。它的自然语言描述可以保留状态、事件、guard、输出和时间参数：例如 10 us trigger、3 ms echo timeout、60 ms 周期、四级距离阈值、双车道密度比较、非均衡时给高密度车道绿灯、均衡时回到 15 s 平衡周期。

它还有较好的可验证性。测试部分给出了两车道对象数量差异、固定周期对照、60 ms 双传感器更新和 20 us 单传感器延迟，足以支撑 `STM.md` 中的行为不是从图里硬猜出来的。

## 如果需要人工细读，建议怎么读

建议先读第 5 页 `Finite State Machine`，直接确认超声传感器 FSM 的状态名和触发/echo 行为。随后读第 7 页 `Verilog Modules`，补齐 `WAIT_ECHO_START`、3 ms timeout、60 ms start pulse、10/15/20/30 cm LED 阈值和双传感器比较逻辑。

第二轮再看第 8 页测试结果，用两车道模拟实验核对“Lane 1 五个对象、Lane 2 一个对象时 Lane 1 绿灯”的行为描述，以及 equal density 默认 15 s 周期。引言和相关工作主要用于理解动机，对恢复状态机骨架不是最重要。
