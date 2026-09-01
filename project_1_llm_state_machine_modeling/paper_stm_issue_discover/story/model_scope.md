# 模型与案例研究范围

Paper1 的方法对象是状态机语言族，而不是 PlantUML-only method。适配器把声明子集内的 source STM 投影为 `M=(S,E,V,Tr,A)` 形式的 FCSTM，并维护 source carrier 到 projection/native facts 的映射。另一个语言只有在 adapter 明确给出 supported fragment、source attribution、rule capability、failure disposition 和独立实证时，才能进入方法声称范围。

当前实现和冻结结果仅包含 PlantUML adapter。54 个输入制品是来自 Wang 等上游 LLM generation/feedback pipeline 的选定 stage/fallback outputs；`source artifact` 只表示本文分析的归因对象，绝不表示人类作者。方法在分析期不生成、不修改该制品。

当前支持片段不覆盖时钟、不变式、正交 region/并发、hybrid semantics 或未声明 FCSTM fragment。source text、canonical source IR、FCSTM、inspect facts、typed binding、compiled program 和 receipt 共同组成可追溯证据链。projection/compiler/runtime/evidence boundary 的失败须与 source-artifact issue 分开记录。
