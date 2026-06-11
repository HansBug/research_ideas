# FlowFSM: Agentic Prompt Chaining for FSM Extraction

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `wael2025AgenticFlowFSMPromptChaining` |
| 论文 | Fares Wael, Youssef Maklad, Ali Hamdi, Wael Elsersy. *An Agentic Flow for Finite State Machine Extraction using Prompt Chaining*. arXiv:2507.11222, 2025. |
| 本地源目录 | `project_1_llm_state_machine_modeling/baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/` |
| 本地输出 | `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/papers/agentic-flow-finite-state-machine-extraction-prompt-chaining.md` |
| baseline verdict | 🟢 direct STM extraction baseline：原始 RFC 自然语言协议规范 → FSM-family rulebook / protocol FSM；但领域是网络协议，artifact 不完整。 |

source pointer：`bibtex.bib:1-10`；`DESC.md:21-63,87-135,136-183,184-216`；`ASSETS.md:11-18,29-49`；`paper_content.txt:21-41,42-106,202-210,212-343,346-393,394-470`。

## 1. 阅读审计

| 审计项 | 已读范围 | 结论 |
|---|---|---|
| `bibtex.bib` | 全文 | 确认 arXiv 2025、作者、标题、引用键和 URL。 |
| `paper_content.txt` | 覆盖摘要、引言、相关工作、背景、RFC 处理、prompt chaining、rulebook、实现、实验、结论 | 重点核对 FlowFSM 输入输出、三阶段提示链、CrewAI、模型、FTP/RTSP 指标和未来工作。 |
| `DESC.md` | 全文 | 用于复核中文摘要、baseline verdict、Project 1 启发与风险。 |
| `ASSETS.md` | 全文 | 用于核对 GitHub shell、公开 RFC、未公开源码/GT/结果细则风险。 |
| 不确定项处理 | RTSP RFC 版本、完整 ground truth、逐转移输出、prompt 细节、provider/temperature 未公开 | 统一写“原文未说明/未见公开证据”，不猜测。 |

source pointer：`paper_content.txt:354-362`（模型/协议）、`paper_content.txt:363-393`（指标与人工验证）、`paper_content.txt:394-444`（结果）、`ASSETS.md:15-18,31-39,45-49`。

## 2. 表 A：方法框架与任务定位

| 字段 | 内容 |
|---|---|
| 输入 NL | 原始 RFC 协议文档；实验覆盖 FTP 和 RTSP。FTP 明确关联 RFC-959；RTSP 具体 RFC 版本原文未锁定。 |
| 任务目标 | 从长篇自然语言协议规范中抽取 protocol FSM：状态、命令/消息、合法前序/后续约束和状态转移，用于协议分析、安全验证、fuzzing/reverse engineering。 |
| agent/prompt 模式（多选 tag+解释） | `agentic flow`：基于 CrewAI 组织 agent/flow；`long-document preprocessing`：清洗 RFC 并解析章节树、leaf chunks、appendix path；`prompt chaining`：Command Extraction → State Transition Analysis → Rulebook Synthesis；`CoT`：摘要/方法明确使用 chain-of-thought reasoning；`rulebook intermediate representation`：先生成可审查 rulebook 而非直接只画图；`RAG-capable but unverified`：CrewAI 支持 vector-store retrieval for RAG，但实验配置未说明；`no repair loop`：未见错误驱动修复。 |
| LLM 模型四元组 | model IDs：`llama3.3-70b-versatile`、`deepseek-r1-distill-llama-70b`、`llama3-70b-8192`；provider/API：原文未明确，CrewAI 支持多 provider；temperature/max output/context/date：原文未说明，只说按性能与大上下文选择。 |
| 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 类型：协议 FSM / command rulebook；语义：命令目的、precondition states、postcondition states、valid preceding/subsequent commands；可执行性：原文未给可直接运行的 DSL/模型检查文件；guard：文本化前置状态/合法性约束；action：命令效果/状态转移说明；hierarchy/time/concurrency：无层次/并发/实时 clock，只有协议顺序约束；应用：cybersecurity、protocol verification、fuzzing；差距：非控制系统，缺少变量更新、时间约束、安全性质和可机读验证闭环。 |
| 人在回路角色 | 生成阶段未报告人工反馈；评估阶段人工 cross-reference RFC 和 standard references 判断 TP/FP/FN。 |
| 输出后人工改动 | 原文未报告人工修改抽取 FSM；只报告人工验证正确性。 |

source pointer：`paper_content.txt:21-41`（摘要）、`paper_content.txt:77-99`（contributions）、`paper_content.txt:202-210`（两阶段方法）、`paper_content.txt:212-264`（RFC tree/chunking）、`paper_content.txt:265-327`（三阶段与 rulebook）、`paper_content.txt:328-343`（CrewAI/RAG/code claim）、`paper_content.txt:354-362`（模型/协议）；`DESC.md:23-63,87-135`。

## 3. 表 B：资产状态与可复现性

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `wael2025AgenticFlowFSMPromptChaining`。 |
| 论文与版本 | arXiv:2507.11222，2025；未见 DOI；本地有 `paper.pdf` 与 `paper_content.txt`。 |
| Reference/GT | 论文评估依赖人工将抽取 transition 与官方 RFC / standard references 对照；完整 GT、逐转移 TP/FP/FN 明细未公开。 |
| 数据与 artifact | 输入 RFC 公开可获取；GitHub `YoussefMaklad/FlowFSM` 是 paper-specific 入口，但当前只有 README/`.gitignore`，README 称 source code will be shared later；无数据、prompt、结果包。 |
| 已有本地复现资产 | 本地有论文文本、`DESC.md`、`ASSETS.md`；`ASSETS.md` 记录 GitHub HEAD `4ab9aa4e2e68da63f842b7e516aee8c27747d339`、FTP/RTSP 指标与缺失项。 |
| 可复现路径 | 现阶段不能直接复现；需等待源码/GT 开放或自行重建：锁定 FTP/RTSP RFC 版本 → 实现 RFC parser + prompt chain → 人工构建 GT/rulebook → 运行同类 LLM → 重新计算 TP/FP/FN。 |
| 资源许可与访问风险 | 代码未公开、无 license/release/requirements；RTSP 版本未锁；ground truth 和输出未公开；结果只见论文 Table I。 |

source pointer：`ASSETS.md:11-18,27-39,45-49`；`DESC.md:13-19,176-183`；`paper_content.txt:328-343,363-393,394-403`。

## 4. 表 C：生成流程内反馈

| 字段 | 内容 |
|---|---|
| 静态/schema | 有结构化 rulebook 模板和 prompt-chain 阶段输出；但未见自动 schema validator、parser gate 或一致性检查实现细节。普通 rulebook 格式不算 formal verification。 |
| 编译/可执行性 | 无编译、模型执行或可执行 FSM DSL 证据。 |
| oracle/trace/等价性 | 无 in-loop oracle/trace/等价反馈；RFC 人工核对只用于 post-hoc TP/FP/FN 评估。 |
| 仿真执行 | 无协议仿真或 fuzzing-in-loop；作者只把集成 fuzzing 作为 future work。 |
| 形式化验证 | 无模型检查/性质证明；论文动机提到 FSM 可用于 verification，但 FlowFSM 当前没有 formal verification engine。 |
| 人类过程反馈 | 生成流程未见 human-in-loop；人工只在事后 cross-reference 协议行为。 |
| 反馈粒度 | Prompt chain 的中间结果粒度为 command inventory、pre/post state、rulebook chapter；不是错误反馈粒度。 |
| 反馈自动化程度 | LLM 链式生成自动化；质量反馈未自动回流。 |
| 人类反馈交叉一致性 | 未报告多标注者、一致性指标或评审协议细节。 |

source pointer：`paper_content.txt:265-327`（三阶段/rulebook）、`paper_content.txt:328-343`（CrewAI/RAG 工具能力）、`paper_content.txt:363-393`（人工验证指标）、`paper_content.txt:445-470`（future fuzzing/cost）；`DESC.md:128-135`。

## 5. 表 D：事后评测、指标与证据强度

| 维度 | 内容 |
|---|---|
| post-hoc 指标 | TP、FP、FN、Precision、Recall、F1；正确性由人工 cross-reference 官方 RFC 与 standard references。 |
| 主要结果 | FTP：TP=90、FP=18、FN=12、Precision=83.33%、Recall=88.24%、F1=85.71%。RTSP：TP=18、FP=4、FN=3、Precision=81.82%、Recall=85.71%、F1=83.72%。作者强调 recall 高于 precision，适合安全场景中“少漏转移”。 |
| 证据强度 | 中-低：指标清楚且任务直接，但只有 2 个协议，无源码/GT/逐转移结果，无同数据集 baseline 复核。 |
| 评测盲点 | 未公开 prompt、chunk、rulebook、错误清单；未说明 RTSP 版本；未给成本/token/time；未接入 verifier/fuzzer；未报告多评审一致性。 |

source pointer：`paper_content.txt:346-393`（RQ 和指标）、`paper_content.txt:394-444`（Table I 与解释）、`paper_content.txt:445-470`（future work/成本）；`DESC.md:157-183`；`ASSETS.md:37-39`。

## 6. 表 E：同样本近似与可比性决策

| 字段 | 决策 |
|---|---|
| 是否可做同样本直接比较 | 现阶段不建议：论文未公开 GT、抽取输出、完整 prompt 和源码；RTSP RFC 版本也未锁。 |
| 可做的近似比较 | 可作为 long-document prompt-chaining 方法参考；若后续源码/GT 开放，可用 FTP/RTSP 复跑，但仍属于协议文档样本，不是控制系统需求样本。 |
| 与 Path-1 S1a 的放置 | 保留为 direct STM extraction baseline，但可复现性标注为弱；适合论证“agentic prompt chain + rulebook IR”而非直接横向量化。 |
| 若复跑需要 | 先定期复查 GitHub；若仍为空，需人工重建 RFC chunk、GT transition set 和评审协议；复跑时需保存模型、日期、prompt hash、必要脱敏输出摘要与调用成本。 |

source pointer：`ASSETS.md:15-18,45-49`；`paper_content.txt:354-362,383-393,394-403`；`DESC.md:201-216`。

## 7. 表 F：Claim 风险与 handoff

| 风险 / handoff | 内容 |
|---|---|
| Claim 风险 1 | 不应把“we open source”当成当前已可复现事实；本地核验时仓库仍是 shell，源码未开放。 |
| Claim 风险 2 | 不应把协议 verification / fuzzing 动机写成 FlowFSM 已完成的形式化验证；当前只有抽取与人工 TP/FP/FN。 |
| Claim 风险 3 | 两个协议不足以证明跨域泛化；FTP/RTSP F1 接近只能作为初步 evidence。 |
| 可 handoff 到 Project 1 | 采用“事件/命令 inventory → pre/post state → rulebook → 状态机”的中间表示；对每条转移保留来源 chunk 和合法前后条件；将 rulebook 作为 LLM-as-Judge / 人工审查入口。 |
| 下一步 | 等源码开放或自行实现最小 FlowFSM-like chain；不要把该论文作为主量化 baseline，除非补齐 GT 和可复现证据链。 |

source pointer：`paper_content.txt:328-343,394-470`；`ASSETS.md:15-18,45-49`；`DESC.md:208-216`。

## 8. 待补与风险

1. 定期复查 `YoussefMaklad/FlowFSM` 是否补源码、license、requirements、prompt 和数据。
2. 需要确认 RTSP 输入 RFC 版本与官方 GT 构造方式。
3. 若引用实验数值，必须说明“论文内 Table I，未见公开逐转移证据”。
4. 需要避免把 post-hoc 人工核验写成 in-loop feedback，也避免把 verification/fuzzing 应用愿景写成本文已实现验证闭环。
