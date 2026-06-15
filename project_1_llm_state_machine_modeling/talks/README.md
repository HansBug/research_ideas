# project_1 正式导师讨论文库

## 1. 定位

本目录用于维护 `project_1_llm_state_machine_modeling` 中与导师形成的**正式研究讨论记录**。它不同于仓库根目录的 [talks/](../../talks/) 工作区，也不同于本项目内的 [discussions/](../discussions/)：

1. 根目录 [talks/](../../talks/) 更偏通用会前/会后纪要工作流，可包含 PPT、原始碎片、待办等完整会议工作区。
2. [discussions/](../discussions/) 主要记录 AI 与用户内部推演、方案辩论、技术调研和临时判断。
3. 本目录只收录**已经包含导师意见、会后路线决策或正式学术口径调整**的讨论记录，是后续写作、实验设计和 agent 工作的高优先级上下文。

## 2. 使用原则

当本目录中的正式导师讨论记录与 [discussions/](../discussions/) 中的内部讨论存在冲突时，默认以本目录为准；若本目录与更晚的导师讨论记录冲突，则以时间更新、明确性更高的记录为准。

后续 AI 在处理 project_1 第一篇论文路线、实验设计、baseline 选择、样本选择或方法定位时，应优先读取：

1. 本文件 [README.md](./README.md)。
2. [GUIDE.md](./GUIDE.md)。
3. [SUMMARY.md](./SUMMARY.md)。
4. 与任务日期或主题最相关的单篇正式导师讨论记录。

## 3. 当前记录

当前已收录：

1. [2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md](./2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md)
   - 记录 2026-06-15 关于 PR #112 第二篇论文从“SE review meta-model 驱动 evidence workflow”进一步转向 researcher-guided、finding-oriented、auditable agentic SLR support workflow 的导师讨论；明确 meta-model 应由使用该方法的 researcher 基于 scaffold 实例化，SLR 应产出 research findings，并引入 researcher challenge / refinement loop。
2. [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md)
   - 记录 2026-06-12 关于第一篇从 `NL -> STM` 生成转向 `<NL, STM_0> -> STM_k / Better STM` 无人化反馈驱动修正、弱化 `fcstm` / DSL 名头、baseline 角色重排、多格式转换器需求，以及第二篇从 `sources` 文库综述转向 agent-based SLR 方法学论文的导师讨论与会后定调。
3. [2026-06-04-导师-第一篇论文路线与E1E2定位.md](./2026-06-04-导师-第一篇论文路线与E1E2定位.md)
   - 记录 2026-06-04 关于 project_1 第一篇论文主线、Path-1/Path-2 分工、E1/E2 定位、核心贡献、baseline、数据选择、变量角色、LangChain/LangGraph、BMC/LTL 与 survey 可能性的导师意见；其中第一篇主任务边界已被 2026-06-12 记录更新。

## 4. 维护边界

本目录不存放论文 PDF、单篇论文提取物或实验 raw artifacts。若需要引用这些材料，应使用相对路径或 GitHub URL 指向对应 PR / issue / 文件，并在正式讨论记录中说明它们的用途与可信度边界。
