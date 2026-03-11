# Model-driven Analysis and Verification of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 功能块给出了显式 TA 状态与转移。

## 条目 1: Brake-by-Wire ABS timed automaton (pABS FL)
- 控制对象：车载 Brake-by-Wire 系统的 ABS 控制功能块
- 整理后的英文描述：The ABS controller cycles through `idle`, `Entry`, `CalcSlipRate`, and `Exit`. After activation it checks vehicle speed; if `v == 0`, it directly outputs zero brake torque and exits. If `v > 0`, it enters `CalcSlipRate`; when slip rate is above 0.2 it commands zero torque, otherwise it forwards `wheelABS`, and then returns to `idle`.
- 要素 1：状态集合显式给出为 `idle`, `Entry`, `CalcSlipRate`, `Exit`。
- 要素 2：转移 `idle -> Entry` 表示功能块被触发后进入计算。
- 要素 3：转移 `Entry -> Exit` 的条件是 `v == 0`，动作是 `torqueABS = 0`。
- 要素 4：转移 `Entry -> CalcSlipRate` 的条件是 `v > 0`。
- 要素 5：在 `CalcSlipRate` 中，根据 slip rate 阈值 0.2 决定 `torqueABS = wheelABS` 或 `torqueABS = 0`，再转入 `Exit`。
- 定位 1：`paper_content.txt` 第 80-81 页，Chapter 5 / Figure 5.5 与 Figure 5.7，行 4339-4450。
- 证据 1：`state idle, Entry, CalcSlipRate, Exit;`
- 证据 2：`Entry->Exit {guard v==0; assign torqueABS=0;}`
- 证据 3：`Entry->CalcSlipRate {guard v>0;}`
- 证据 4：`CalcSlipRate->Exit {guard ... assign torqueABS=wheelABS;}`
- 证据 5：`CalcSlipRate->Exit {guard ... assign torqueABS=0;}`
