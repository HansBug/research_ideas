# Model-checking and Model-based Testing of Automotive Embedded Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 行为图直接给出了 Entry/CalcSlipRate/Exit 三态。

## 条目 1: BBW ABS behavior TA
- 控制对象：车载 Brake-by-Wire 系统的 ABS 计算逻辑
- 整理后的英文描述：The ABS behavior TA starts in `Entry`, checks whether the vehicle is moving, and either exits with zero torque or transitions to `CalcSlipRate`. In `CalcSlipRate`, if the slip rate exceeds 0.2 it outputs zero torque; otherwise it outputs the requested wheel torque, then terminates in `Exit`.
- 要素 1：状态显式出现在 Figure 5.1：`Entry`, `CalcSlipRate`, `Exit`。
- 要素 2：`Entry -> Exit` 对应 `v == 0`，输出零制动力。
- 要素 3：`Entry -> CalcSlipRate` 对应 `v > 0`。
- 要素 4：`CalcSlipRate -> Exit` 中根据 `slip rate > 0.2` 与否选择输出 0 或 `wheelABS`。
- 定位 1：`paper_content.txt` 第 50 页，Section 5.1 / Figure 5.1，行 2141-2152。
- 定位 2：`paper_content.txt` 第 54 页附近，关于接口 TA 与行为 TA 的同步描述，行 2373-2381。
- 证据 1：`Entry` / `CalcSlipRate` / `Exit`
- 证据 2：`if the car has no speed then no brake force is applied`
- 证据 3：`if the slip rate exceeds 0.2, no braking force should be applied`
- 证据 4：`otherwise the desired braking torque wheelABS is sent`
