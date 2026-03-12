# Formal Verification of Simulation Scenarios in Aviation Scenario Definition Language (ASDL) - STM 提取记录

## 盘点结论
- 评级：⚪ 未收获
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：否
- 提取条目数：0
- 简要判断：论文关注的是航空场景 DSL 与 landing scenario 验证流程，核心对象是 scenario/tool 而不是实际控制系统或控制器。

## 检查说明
- 结论：文中虽然有 aircraft landing statechart，但其角色是 ASDL 生成场景的验证对象，主要服务于 scenario builder 和 tool verification，不是控制系统设计/需求描述，因此不作为目标样本纳入。
- 检查位置 1：第 1-2 页，`paper_content.txt` 行 41-49
> In this paper, statecharts will be utilized for the verification of each scenario generated using ASDL. The underlying assumption is that once a set of rules has been established and verified for the type of scenario required, all other scenarios of that type only need to conform to these rules.
- 检查位置 2：第 10 页，`paper_content.txt` 行 397-400
> An aircraft begins in cruise mode and the pilot receives descent and approach clearance as requested. Landing clearance is granted next and the pilot is able to touchdown, taxi, and park at the gate in order to complete a normal landing.

