# A real-time semantics for the IEC 61499 standard - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：BFB/ECC 本身就是有限状态控制器，但示例状态名主要在图里。

## 条目 1: BFB execution control chart (ECC)
- 控制对象：IEC 61499 分布式控制系统中的 Basic Function Block 控制器
- 整理后的英文描述：A Basic Function Block is defined in a finite-state-machine-like manner by its ECC. Each ECC state may execute algorithms and emit output events; transitions are triggered by input events, guards over variables, or their combination. In the example system model, FB `b1` is driven by input events `i1` and `i3`, and the executed sub-task subset depends on the current ECC state.
- 要素 1：ECC 明确是 finite-state-machine-like 控制结构。
- 要素 2：transition condition 可以是 input event、Boolean guard 或二者组合。
- 要素 3：每个 ECC state 会执行有序算法并发送输出事件。
- 要素 4：示例系统中 `b1` 的 ECC 由 `i1` / `i3` 等事件驱动。
- 要素 5：状态名在正文中没有完全展开，所以只记为“可整理”。
- 定位 1：`paper_content.txt` 第 2 页，Background / IEC 61499，行 122-140。
- 定位 2：`paper_content.txt` 第 5 页，System model example，行 427-489。
- 证据 1：`The operation of a BFB is defined (in a finite state machine like manner) by its Execution Control Chart (ECC)`
- 证据 2：`A transition condition ... is either a single input event, a Boolean expression ... or a combination thereof`
- 证据 3：`Figure 6 depicts the ECC of b1`
