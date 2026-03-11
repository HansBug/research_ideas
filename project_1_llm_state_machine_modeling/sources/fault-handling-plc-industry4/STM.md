# Fault Handling in PLC-Based Industry 4.0 Automated Production Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：既有通用 operation modes，又有 abort/reset/start 的实际切换链路。

## 条目 1: Standardized machine-part operation modes
- 控制对象：PLC 控制下机器部件的通用 operation-mode 状态机
- 整理后的英文描述：A machine part is described with a standardized set of operation modes including `automatic`, `setup`, `manual`, `semi-automatic`, `initialize`, `shut down`, and `safe stop`. The paper explicitly says that these modes may be implemented as additional automata or as branches inside other automata, and cites the OMAC state machine as the source of valid state transitions.
- 要素 1：显式模式：`automatic`, `setup`, `manual`, `semi-automatic`, `initialize`, `shut down`, `safe stop`。
- 要素 2：这些模式被说明为可实现成附加 automata 或 automata 分支。
- 要素 3：OMAC State Machine 负责根据当前状态和条件判定有效状态转移。
- 定位 1：`paper_content.txt` 第 5 页，Section 2.2，行 232-250。
- 证据 1：`Automatic mode`
- 证据 2：`Setup mode`
- 证据 3：`Manual mode`
- 证据 4：`The OMAC State Machine is responsible for identifying valid state transitions`

## 条目 2: Abort-reset-start return path
- 控制对象：包装机械模块在故障后的重启控制流程
- 整理后的英文描述：In automatic mode, a module runs in `execute`. Errors can drive it to `aborting` and then to the failure state `aborted`. Recovery is performed by switching to manual mode to resolve the issue, then performing recalibration in `starting`, and finally returning to automatic mode.
- 要素 1：显式状态/模式包括 `execute`, `aborting`, `aborted`, `resetting`, `starting`。
- 要素 2：自动模式下出错会导致模块转入 `aborted`。
- 要素 3：恢复路径是 manual mode -> recalibration/`starting` -> automatic mode。
- 定位 1：`paper_content.txt` 第 9 页，Case study B 之前的公司标准化模式描述，行 398-404。
- 证据 1：`execute`, `aborting`, `aborted`, `resetting` and `starting`
- 证据 2：`aborted in case of errors resulting in a failure state`
- 证据 3：`resetting is done by switching to manual mode`
- 证据 4：`followed by an automatic recalibration of the machine (starting)`
