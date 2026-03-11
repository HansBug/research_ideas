# Benchmarks for Temporal Logic Requirements for Automotive Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：自动变速器基准模型明确给出了 gear FSM 和 shift guard。

## 条目 1: Automatic transmission switching logic
- 控制对象：自动变速器控制器
- 整理后的英文描述：The automatic transmission model contains concurrently executing finite state machines. One gear machine has states `first`, `second`, `third`, and `fourth`; the switching logic uses guards such as `[speed > up_th]`, `[speed < down_th]`, and timed conditions `after(TWAIT,tick)` to control upshifting and downshifting.
- 要素 1：gear 状态显式给出为 `first`, `second`, `third`, `fourth`。
- 要素 2：另一个并发状态机含有 `selection_state`, `steady_state`, `upshifting`, `downshifting`。
- 要素 3：典型转移 guard 包括 `[speed > up_th]`, `[speed < down_th]`, `after(TWAIT,tick)`。
- 要素 4：自然语言需求 AT3-AT5 直接约束 gear 之间的转移时间窗口。
- 定位 1：`paper_content.txt` 第 2 页，Figure 1，行 57-85。
- 定位 2：`paper_content.txt` 第 4 页，Table 1 中 AT3-AT5，行 217-231。
- 证据 1：`first`, `second`, `third`, `fourth`
- 证据 2：`[speed > up_th]` / `[speed < down_th]`
- 证据 3：`after (TWAIT,tick)`
- 证据 4：`There should be no transition from gear two to gear one and back to gear two in less than 2.5 sec.`
