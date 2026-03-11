# Design Pillars for Medical Cyber-Physical System Middleware - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 `SOURCES.md` 盘点：否
- 提取条目数：0
- 简要判断：是中间件设计原则，不是具体控制系统状态机。

## 检查说明
- 结论：文中提到 system state 和 device connection state，但这些是中间件可观测性原则，没有给出某个控制对象的状态集、输入条件和转移规则。
- 检查位置 1：`paper_content.txt` 第 4 页，讨论 “Visibility of runtime configuration” 与 connection state。
- 相关摘录 1：`the connection state of devices should be readily available`
- 相关摘录 2：`When the system is in an undesirable state`
