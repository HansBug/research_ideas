# Towards the Model-Driven Engineering of Secure yet Safe Embedded Systems - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 `SOURCES.md` 盘点：否
- 提取条目数：0
- 简要判断：文中状态机主要对应密钥分发协议，不是控制系统对象。

## 检查说明
- 结论：虽然论文提到 state machine diagrams 和 brake actuation scheduling，但可读正文里的具体状态机例子是 key distribution protocol，不符合“控制系统客体”限定。
- 检查位置 1：`paper_content.txt` 第 9-10 页，Figure 6 为 Key Distribution Protocol 状态机。
- 检查位置 2：`paper_content.txt` 第 11 页，仅把 brake actuation 作为安全/调度影响举例。
- 相关摘录 1：`state machine diagram of Key Distribution Protocol`
- 相关摘录 2：`prevent the scheduling of the process controlling the brake actuation`
