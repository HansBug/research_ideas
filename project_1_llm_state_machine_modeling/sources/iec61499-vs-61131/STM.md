# IEC 61499 vs. 61131: A Comparison Based on Misperceptions - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 `SOURCES.md` 盘点：否
- 提取条目数：0
- 简要判断：有 ECC 示例，但对象是泛化 counter FB，不作为控制系统需求样本。

## 检查说明
- 结论：文中确实展示了 up-counter function block 的 ECC，但这是标准对比用的泛化 FB 例子，不是具体控制系统对象；第 9 页则主要是在批评执行语义。为保证数据集对象严格是控制系统，本篇不计入收获。
- 检查位置 1：`paper_content.txt` 第 3 页，Figure 2 讨论 up-counter 61499 FB 与 ECC。
- 检查位置 2：`paper_content.txt` 第 9 页，讨论 event-driven/cyclic execution 争议。
- 相关摘录 1：`Up-counter 61499 function block`
- 相关摘录 2：`trigger the transitions of the Execution control chart (ECC)`
