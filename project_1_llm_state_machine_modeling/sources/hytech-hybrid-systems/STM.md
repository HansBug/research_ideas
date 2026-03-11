# HyTech: A model checker for hybrid systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：恒温器自动机是标准的控制对象状态机示例。

## 条目 1: Thermostat hybrid automaton
- 控制对象：温控器控制系统
- 整理后的英文描述：The thermostat hybrid automaton has an `on` node and an `off` node. While in `on`, the heater is on and temperature rises; when temperature reaches 3 degrees, the controller takes the `turn_off` transition to the `off` node. Invariants force the controller to leave `on` before temperature exceeds 3, and the variables/clocks can be reset on transitions.
- 要素 1：节点/状态为加热 `on` 与关闭 `off`。
- 要素 2：guard `x = 3` 触发 `turn_off` 转移。
- 要素 3：`on` 状态不变式为 `1 < x < 3`。
- 要素 4：转移可以 reset clock。
- 定位 1：`paper_content.txt` 第 2 页，Figure 1 与其说明，行 64-79。
- 证据 1：`models a simple thermostat`
- 证据 2：`When the temperature reaches 3 degrees, the heater is turned off`
- 证据 3：`the invariant of the node on is 1 < x < 3`
- 证据 4：`the guard on the transition labeled turn_off is x = 3`
