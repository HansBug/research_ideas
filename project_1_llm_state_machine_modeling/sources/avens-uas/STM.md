# AVENS - A Novel Flying Ad Hoc Network Simulator with Automatic Code Generation for UAS - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 `SOURCES.md` 盘点：否
- 提取条目数：0
- 简要判断：聚焦飞行/网络联合仿真，不提供可复用的控制系统状态机描述。

## 检查说明
- 结论：文中主体是 UAV 网络仿真平台、XML 交互与仿真回调流程。虽然出现了“simple state machine”或等待/更新循环，但对象是仿真器/数据交换机制，不是控制系统本体的状态机需求。
- 检查位置 1：`paper_content.txt` 第 5-6 页，Section 3 AVENS，讨论 X-Plane/OMNeT++ 集成、WAIT_XPLANE 与 UPDATE_POSITIONS 循环。
- 检查位置 2：`paper_content.txt` 第 4 页，说明 case study 关注 network communication，而非 autopilot 其他控制部件。
- 相关摘录 1：`the network communication is the focus of this case study, thus other components of the autopilot are not being taken into account`
- 相关摘录 2：`WAIT_XPLANE` / `UPDATE_POSITIONS`
