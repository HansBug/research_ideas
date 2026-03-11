# Modeling and Verification of a Dual Chamber Implantable Pacemaker - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：既有基础 DDD 节律控制，也有 DDD/VDI 模式切换。

## 条目 1: Basic DDD pacemaker timing control
- 控制对象：双腔起搏器 DDD 模式基本控制逻辑
- 整理后的英文描述：The pacemaker is modeled as interacting timing components `LRI`, `AVI`, `URI`, `PVARP`, and `VRP`. `LRI` maintains the lower rate by issuing `AP` if no atrial event is sensed after a ventricular event. `AVI` waits for a ventricular event after an atrial event and delivers `VP` if needed, while `URI` can delay `VP` to keep the upper-rate limit. `PVARP` and `VRP` filter atrial/ventricular events during refractory periods.
- 要素 1：控制分解为 `LRI`, `AVI`, `URI`, `PVARP`, `VRP` 五个定时组件。
- 要素 2：`LRI` 在收到 `VS/VP` 后复位；若未感知到 `AS`，则在 `TLRI-TAVI` 后发出 `AP`。
- 要素 3：`AVI` 在 atrial event 后等待 `VS`，若超时则发出 `VP`。
- 要素 4：`URI` 会在上限速率约束下延迟 `VP`。
- 要素 5：`PVARP/VRP` 负责 blanking/refractory 过滤。
- 定位 1：`paper_content.txt` 第 4-6 页，Section 3.3 “Basic DDD Pacemaker Modeling”，行 147-157、192-208、212-215。
- 证据 1：`The DDD pacemaker has 5 basic timing cycles triggered by events`
- 证据 2：`If no atrial event has been sensed (AS), the component will deliver atrial pacing (AP)`
- 证据 3：`If no ventricular event has been sensed (VS) within TAVI ... the component will deliver ventricular pacing (VP)`
- 证据 4：`AVI will hold VP and deliver it after the global clock reaches TURI`

## 条目 2: Mode-switch algorithm between DDD and VDI
- 控制对象：双腔起搏器的 DDD/VDI 模式切换控制
- 整理后的英文描述：The mode-switch algorithm detects sustained fast atrial activity, confirms it with a counter and duration window, and then switches the pacemaker from dual-chamber `DDD` mode to single-chamber `VDI` mode. When the fast rhythm ends or the counter drops to zero, it switches back to `DDD`.
- 要素 1：显式模式：`DDD` 与 `VDI`。
- 要素 2：间隔被判定为 `fast` 或 `slow`；counter 对 fast/slow 事件增减计数。
- 要素 3：counter 达到 `Entry Count` 后开启 `Duration` 窗口以确认 SVT。
- 要素 4：`Duration` 结束后若 counter 仍为正，则切入 `VDI`；若 counter 归零，则回到 `DDD`。
- 要素 5：修改后的 `AVI` 和 `LRI` 组件通过 `DDD` / `VDI` switching events 切换。
- 定位 1：`paper_content.txt` 第 9-10 页，Section 5.2 “Verification of the Mode-Switch Algorithm”，行 360-414。
- 证据 1：`switches the pacemaker from a dual-chamber mode to a single-chamber mode`
- 证据 2：`switch to the VDI mode (Fallback mode)`
- 证据 3：`the pacemaker is switched back to DDD mode`
- 证据 4：`switch between each other when switching events (DDD, VDI) are received`
