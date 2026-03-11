# Safety analysis integration in a SysML-based complex system design process - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：飞机轮刹系统四模态自动机非常适合状态机需求样本。

## 条目 1: Wheel brake system fault-tolerant mode automaton
- 控制对象：飞机 wheel brake system 的容错控制模式
- 整理后的英文描述：The wheel brake system is modeled with four system modes: `Normal`, `Alternate`, `Emergency`, and `Fail`. The controller starts in `Normal`; when the normal line fails (`failNormal`) it switches to `Alternate`; if the alternate path also fails (`failAlternate`) it switches to `Emergency` using the accumulator; if emergency power also fails (`failEmergency`), the system enters `Fail`.
- 要素 1：显式模式：`Normal`, `Alternate`, `Emergency`, `Fail`。
- 要素 2：`failNormal` 触发 `Normal -> Alternate`。
- 要素 3：`failAlternate` 触发 `Alternate -> Emergency`。
- 要素 4：`failEmergency` 触发 `Emergency -> Fail`。
- 要素 5：文中同时给出了与这些模式相对应的安全要求 SR1-WBS / SR2-WBS。
- 定位 1：`paper_content.txt` 第 6 页，Case study / wheel brake system，行 479-507。
- 证据 1：`we consider four modes or states of the system`
- 证据 2：`Normal`
- 证据 3：`Alternate: activated when the Normal line fails`
- 证据 4：`Emergency: activated when Alternate mode also fails`
- 证据 5：`Fail: when all systems are in failure`
