# Implementation of an Electro-Pneumatic Prototype Elevator Controlled by PLC

## 论文在讲什么

这篇论文实现了一个三层电-气动电梯原型。系统由 PLC、气缸、solenoid、relay、proximity switch、内外呼梯按钮、门驱动、压力开关和应急制动部件组成，目标是让电梯原型能模拟真实楼宇电梯的呼梯、上下行、开关门和故障保护。

## 控制系统在文中的位置

控制系统贯穿硬件构造和软件过程。第 2-6 页写清了三层结构、按钮布置、内呼优先、proximity switch 楼层检测和 relay 输出；第 10 页说明软件过程会先检查楼层、上下运动、门开闭与传感器状态，再由 ladder program 控制所有运动。

## 对我们为什么有用

它补进 `🏢` 方向的电-气动原型控制链，和普通电机电梯不同。该样本的价值在于执行器命名很具体：`rlyup` 控制上行 solenoid，`rlydown` 控制下行 solenoid，`d-o/d-c` 控制门开闭；输入侧又有内外按钮、楼层 proximity switch 和压力开关制动保护，因此可以形成一个设备-状态-动作对应清楚的 EFSM/T0 样本。

## 如果需要人工细读，建议怎么读

先读第 3 页 `current work` 段落确认三层、PLC 型号和尺寸边界；再读第 5-7 页按钮、solenoid 与 relay 段落；最后读第 10 页 `Software Process`，把楼层状态检查、上下行、门开闭和梯形图控制串成主链。
