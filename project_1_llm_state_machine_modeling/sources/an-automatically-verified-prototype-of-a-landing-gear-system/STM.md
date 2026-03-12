# An Automatically Verified Prototype of a Landing Gear System - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：否
- 提取条目数：0
- 简要判断：论文重点是把既有 Event-B 起落架模型编码到 `{log}` 并自动 discharge proof obligations，不是直接提供可复用的控制系统自然语言描述。

## 检查说明
- 结论：虽然对象仍然是 landing gear system，但本文主体是验证器编码、proof obligation discharge 与模型流水线说明。控制逻辑主要以内嵌事件模型和谓词形式出现，不足以稳定整理成面向数据集的自然语言控制描述。
- 检查位置 1：第 1 页，`paper_content.txt` 行 11-16
> as an automated veriﬁer for B speciﬁcations. In particular we encode in {log} an Event-B specification ... Next we use {log} to discharge all the proof obligations proposed in the Event-B specification by the Rodin platform.
- 检查位置 2：第 12 页，`paper_content.txt` 行 431-437
> The Event-B development of the LGS consists of eleven models organized in a refinement pipeline ... the first and simplest model specifies the gears ... the second one adds the doors ... the third one adds the hydraulic cylinders that either open (extend) or close (retract) the doors (gears).

