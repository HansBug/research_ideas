# 模型与案例研究范围

Paper1 的方法对象是状态机语言族，而非只适用于 PlantUML 的方法。适配器把声明子集内的源状态机制品投影为 `M=(S,E,V,Tr,A)` 形式的有限控制状态机（FCSTM），并维护源载体到投影和原生事实的映射。另一种语言只有在其适配器明确给出支持片段、来源归属、规则能力、失败处置和独立实证时，才能进入方法声称范围。

当前实现和冻结结果仅包含 PlantUML 适配器。上游数据来自 [Wang 等的 Internetware 2025 论文及其一手工作簿](../corpora/seed_library/llms-emp-stm-subset/assets/README.md)：60 行 `feedback-final` 池的阶段/回退选择由[验证摘要](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/feedback_final_validation_summary.json)固定，当前实验网格再依[范围规则](../selected_seed_examples/README.md)排除 6 个并发/秒级时间约束制品，形成 9 个自然语言簇、每簇 6 个制品的 54 个输入对。源制品只表示本文分析的归因对象，绝不表示人类作者。方法在分析期不生成、不修改该制品。

当前支持片段不覆盖时钟、不变式、正交区域/并发、混合语义或未声明的有限控制状态机片段。源文本、规范源中间表示、有限控制状态机、确定性检查事实、类型化绑定、编译程序和回放回执共同组成可追溯证据链。投影、编译器、运行时或证据边界的失败须与源制品问题分开记录。
