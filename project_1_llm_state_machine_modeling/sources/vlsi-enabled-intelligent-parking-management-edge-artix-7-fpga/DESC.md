# Artix-7 智慧停车管理控制 / VLSI-Enabled Intelligent Parking Management System using Edge Artix-7 FPGA for Real-Time Automation

## 论文在讲什么

这篇论文研究的是停车场入口与车位监测的硬件化实时控制，而不是车辆自动泊车轨迹。作者使用 Edge Artix-7 FPGA、HC-SR04 超声传感器、IR 车位传感器、SG90 伺服电机和 LED 指示器构成一个四车位停车场原型。

系统运行方式比较直接：入口超声传感器检测到车辆接近后触发 FPGA，FPGA 通过 PWM 打开伺服道闸；车位上的 IR 传感器实时更新占用状态，LED 用于显示车位占用和满位告警。论文进一步把超声测距模块写成 FSM，并给出 50 MHz 时钟、触发脉冲、echo 测量、超时和 PWM 脉宽等实现细节。

## 控制系统在文中的位置

控制系统是论文主线。`System Architecture`、`FPGA Control Logic`、`Design Flow` 和 `Testing and Results` 都在说明同一个停车控制链：入口测距、道闸动作、车位占用、LED 显示和满位处理。

需要注意的是，原文显式 FSM 主要在超声传感器控制模块，而不是一个完整的停车场系统级状态图。但这个测距 FSM 直接触发道闸和车位监测控制，因此按本论文集口径可以作为真实控制子系统样本。它不是纯传感算法，因为后续动作包括 `servo_out`、LED 状态和 parking full alert。

## 对我们为什么有用

这篇论文补的是 `🅿️` 方向中“入口测距 + 伺服道闸 + 车位占用反馈”的样本。相比一些只写停车 App、数据库或显示界面的论文，它把传感器输入和执行器输出绑定得更紧，能够直接写成状态机自然语言描述。

它也提供了较好的时间语义：0.5 秒道闸响应、10 us 处理、50 MHz 时钟、50/75 us PWM 脉宽、600 周期触发脉冲和 150000 周期 echo timeout。后续做 `T1` 类样本时，这些数字可以帮助模型学习工程局部定时而不是只学静态阈值。

## 如果需要人工细读，建议怎么读

建议先读第 1 页摘要和第 4 页 `Sensor Integration / FPGA Control Logic / Output Mechanisms`，先把入口传感器、车位传感器、伺服电机和 LED 的关系建立起来。随后读第 4 页 `Design Flow`，重点抽取 ultrasonic sensor controller、servo motor driver、IR sensor processor 和 main integrator 四个模块，以及 FSM、PWM、trigger 和 echo 计数。

第二轮再读测试章节，核对 vehicle entry、slot occupancy、full parking、sensor failures 和 rapid inputs 这些测试情形是否覆盖 `STM.md` 中的行为。前面的 IoT/ML/RFID 文献比较可以放到最后，对恢复控制状态机不是最关键。
