# Modelling Interlocking Systems for Railway Stations - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：否
- 提取条目数：0
- 简要判断：论文主体聚焦联锁建模方法、模型生成与验证流程，虽然介绍了 train route based interlocking，但当前可直接摘出的控制对象行为描述仍偏方法论。

## 检查说明
- 结论：不计入本轮正例。原文多在讨论如何从 RSL 模型生成 transition system、如何表达安全性质与 route table，而不是直接给出一段可以原样整理成状态机自然语言需求的控制逻辑。
- 检查位置 1：`paper_content.txt` 第 3-4 页，行 19-34
- 相关摘录 1：`The goal of this project is to develop a formal method for verifying ... a dynamic behaviour of an interlocking system ... patterns for specifying safety properties are developed using LTL.`
- 检查位置 2：`paper_content.txt` 第 26-28 页，行 513-528
- 相关摘录 2：`Banedanmark uses train route based interlocking ... concrete safety rules are specified ... a physical implementation of the concrete safety rules is made.`
- 判断原因：这些段落足以说明论文对象与背景，但不足以像现有联锁正例那样稳定提炼出“请求-检查-锁闭-开放-释放”的完整原文型控制叙述。
