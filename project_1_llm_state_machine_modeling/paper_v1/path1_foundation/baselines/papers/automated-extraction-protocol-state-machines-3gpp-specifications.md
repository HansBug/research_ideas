# SpecGPT / 3GPP 协议状态机抽取

## 0. 元信息与 source pointer

| 项目 | 内容 | Source pointer |
|---|---|---|
| 稳定引用键 | `zhang2025SpecGPT3GPPStateMachines` | `project_1_llm_state_machine_modeling/baselines/automated-extraction-protocol-state-machines-3gpp-specifications/bibtex.bib:1-10` |
| 论文 | Miao Zhang et al., *Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles*, arXiv:2510.14348, 2025 | `.../bibtex.bib:1-10`; `.../paper_content.txt:1-32` |
| 本地原始目录 | `project_1_llm_state_machine_modeling/baselines/automated-extraction-protocol-state-machines-3gpp-specifications/` | 本任务指定路径；`.../ASSETS.md:13-19` |
| 主要 source pointer 简写 | `P=`同目录 `paper_content.txt`；`D=`同目录 `DESC.md`；`A=`同目录 `ASSETS.md`；`S=` `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` | 本文下方表格使用这些简写，但均指向上述原始目录 |
| 关键证据线索 | 任务与动机：`P:10-30`, `P:57-85`, `P:121-139`；框架：`P:226-276`, `P:333-356`, `P:357-474`, `P:475-529`, `P:530-588`；评测：`P:641-697`, `P:735-789`, `P:791-860`；限制/用途：`P:862-915`, `P:956-971`；资产：`A:13-19`, `A:28-40` | 逐项结论见各表 Source pointer 列 |

## 1. 阅读审计

| 材料 | 已读范围 | 结论 | Source pointer |
|---|---|---|---|
| `bibtex.bib` | 全文 10 行 | 确认 arXiv 2025、作者、标题、URL 与引用键。 | `.../bibtex.bib:1-10` |
| `paper_content.txt` | 覆盖摘要、引言、背景、设计、评测、讨论、结论与相关工作；重点读 §III Design、§IV Evaluation、§V Discussion | 原文支持“3GPP 长规格 -> protocol FSM”的 direct/near baseline 判断，但不支持“已有公开 GT / 可复现实验包”。 | `P:10-30`, `P:57-85`, `P:226-276`, `P:333-588`, `P:641-860`, `P:862-971` |
| `DESC.md` | 全文阅读 | 既有派生文件已将其评为 Project 1 direct STM baseline，并明确代码/GT 未公开、无模型检查闭环。 | `D:13-18`, `D:20-62`, `D:122-129`, `D:151-173`, `D:175-208` |
| `ASSETS.md` | 全文阅读 | 公开的是论文与 3GPP 输入规格入口；SpecGPT 代码、NAS/NGAP/PFCP GT、逐转移结果和复现包未公开。 | `A:13-19`, `A:28-40`, `A:46-50` |
| `SUMMARY.md` 对应行 | 核对 direct baseline 总账行 | 总账同样记录：输入规格公开、作者 GT 未公开、无运行/仿真、形式化角色停在抽取层。 | `S:123`, `S:250` |

## 2. 表 A：方法框架与任务定位

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 输入 NL | 3GPP Release 17 技术规格，覆盖 NAS、NGAP、PFCP；是面向领域专家的半结构化自然语言标准文档，页数多、跨 release 更新频繁。 | `P:57-85`, `P:130-136`, `P:194-225`, `D:26-28` |
| 任务目标 | 从 3GPP 规格自动抽取 protocol state machines，减少人工建模，服务协议验证、测试和规格结构化。 | `P:21-30`, `P:121-139`, `P:888-915`, `P:956-971` |
| agent/prompt 模式（多选 tag+解释） | `structured prompt`：状态、条件、动作、JSON 字段显式约束；`CoT/decomposition`：state extraction、transition extraction、post-processing 三阶段；`few-shot`：condition/action 分离示例；`lightweight RAG/context`：章节号 cross-reference 与历史上下文；`ensemble`：五个 LLM 同 prompt 输出后对齐与多数投票。 | `P:255-276`, `P:357-474`, `P:475-529`, `P:530-588`, `D:122-128` |
| LLM 模型四元组 | 模型：Claude Sonnet 4、DeepSeek V3、Gemini 2.5 Pro、GPT-4o、Qwen Turbo；provider：Anthropic / DeepSeek / Google / OpenAI / Qwen 系；调用方式：API/hosted LLM，temperature 0.2；版本锁：论文只给模型名和当时价格/耗时，不给精确 API snapshot 或 deployment id。 | `P:530-541`, `P:589-610`, `P:821-840`, `D:144-149` |
| 输出 STM 类型 | Protocol finite state machine，论文形式化为 $\langle Q, \Sigma, q_0, \delta, F \rangle$，实际转移包含 `from/to state + condition span + action span`；语义能力：适合协议状态/消息/条件抽取；可执行性：论文未给可直接运行的 DSL/代码；guard/action：以原文 condition/action span 表示；hierarchy：可把 PFCP/NGAP 按层拆分评估，但不是通用层次状态机；time/concurrency：无显式 timed/concurrent semantics；应用场景：协议验证/测试前处理；与本项目差距：不覆盖控制变量、pyfcstm schema、时间约束、层次并发、scenario trace 或 repair loop。 | `P:235-254`, `P:413-436`, `P:641-653`, `P:698-734`, `P:888-915`, `D:97-121`, `D:200-208` |
| 人在回路角色 | 作者人工构建并交叉验证 ground truth，是事后评测与 reference 构建；生成流程中原文提到多模型输出差异“necessitating manual alignment”，但未说明人工对齐流程、角色和可复现细节，不能视作完整可复核的人类反馈闭环。 | `P:134-138`, `P:530-544`, `D:132-137`, `A:18`, `A:36` |
| 输出后人工改动 | 论文没有公开最终 FSM 输出或逐转移编辑记录；可确认的是 post-processing 会做 JSON 结构校验、伪状态/空状态移除，多模型输出会对齐后投票；人工 GT 与可能的 manual alignment 不等于公开可复现的输出后人工修订记录。 | `P:461-474`, `P:530-588`, `A:16-19`, `A:38-40` |

## 3. 表 B：资产状态与可复现性

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 稳定引用键 | `zhang2025SpecGPT3GPPStateMachines` | `.../bibtex.bib:1-10` |
| 论文与版本 | arXiv preprint `arXiv:2510.14348`，2025，cs.NI；非 CCF venue。 | `.../bibtex.bib:1-10`, `A:21-27` |
| Reference / GT | 作者为 NAS、NGAP、PFCP Release 17 手工标注完整 state machine dataset，并用 precision/recall/F1 评测；GT 未公开。 | `P:130-138`, `P:641-656`, `D:132-137`, `A:18`, `A:36` |
| 数据与 artifact | 公开可取得的是 3GPP TS 24.501 / 38.413 / 29.244 规格入口；SpecGPT 源码、GT、逐转移输出、复现包均未发现公开入口。 | `A:13-19`, `A:30-40`, `P:1066-1071` |
| 已有本地复现资产 | 本地仅有 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md`；没有本地 SpecGPT runner、prompt 包、GT 或输出表。 | `A:13-19`, `A:30-40` |
| 可复现路径 | 只能做 method-level approximate：锁定 3GPP Release 17 文档，重建清洗/section tree/chunking、prompt、五模型调用、JSON 后处理和 ensemble；由于 GT 与代码缺失，不能声称复现论文结果。 | `P:292-356`, `P:357-588`, `A:17-19`, `A:48-50` |
| 资源许可与访问风险 | 3GPP dynareport 是活入口，必须锁定具体 release/version；作者 GT 是私有资产，论文未给申请表或公开数据服务；多 hosted LLM 会有 provider drift 与价格漂移。 | `A:17-19`, `A:28`, `A:46-50`, `P:791-840` |

## 4. 表 C：生成流程内反馈

> 只统计会进入生成/抽取/聚合流程的反馈；NAS/NGAP/PFCP GT F1、Hermes 对比和专家 GT 是事后评测，不写成 in-loop feedback。

| 字段 | in-loop feedback 判定 | Source pointer |
|---|---|---|
| 静态/schema | 有弱 in-loop：prompt 要求 JSON 格式；post-processing 解析 JSON、flag 格式错误、移除 pseudo-states / empty states。 | `P:413-436`, `P:461-474`, `D:122-128` |
| 编译/可执行性 | 无。输出不是可编译 DSL / simulator 工件，论文未报告把 FSM 输入编译器或执行环境来驱动再生成。 | `P:641-653`, `P:888-915`, `D:127-129` |
| oracle/trace/等价性 | 无 in-loop。transition correctness 与 span-overlap 阈值用于事后评测和 ensemble 对齐；GT F1 不反馈给 LLM 修复。 | `P:641-653`, `P:662-697`, `P:735-789` |
| 仿真执行 | 无。论文只说输出可支持 downstream testing/verification，没有把仿真 trace 作为生成反馈。 | `P:888-915`, `P:956-971`, `D:127-129` |
| 形式化验证 | 无完整 formal verification in-loop。协议 FSM 是形式化风格输出，但没有 model checker / theorem prover / SAT-SMT 验证闭环。 | `P:888-915`, `D:167-173`, `S:123` |
| 人类过程反馈 | 不明/弱：多模型输出对齐处出现“manual alignment”表述，但流程、频率、判据和一致性未披露；GT 专家构建是 post-hoc。 | `P:530-544`, `P:641-656`, `A:18`, `A:36` |
| 反馈粒度 | JSON/tuple 级、transition tuple 级、action/condition span overlap 级；没有 scenario trace / component diagnostic / FixLog 粒度。 | `P:413-436`, `P:551-588`, `P:641-653` |
| 反馈自动化程度 | JSON parsing、规则清理、span-overlap 对齐和 majority voting 可自动化；manual alignment 细节不可复现；GT F1 是离线评估。 | `P:461-474`, `P:530-588`, `P:641-697` |
| 人类反馈交叉一致性 | 作者称 GT 经交叉验证/peer review（既有 DESC 记录），但原文/资产未公开 annotator agreement、rubric 或逐项分歧表；不能作为可复现人类反馈一致性证据。 | `D:132-137`, `A:18`, `A:36` |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 结果 / 证据 | 证据强度 | Source pointer |
|---|---|---|---|
| NAS 状态抽取 | NAS GT 有 18 states、179 transitions；五模型均抽取 18 states，state F1=100%。 | 中：论文表述清晰，但 GT 未公开。 | `P:654-660`, `A:18` |
| NAS transition extraction | Ensemble precision/recall/F1 = 91.86 / 90.43 / 91.14；单模型 F1 68.77-85.29。 | 中：核心指标明确，缺逐转移输出和 GT。 | `P:662-697` |
| PFCP / NGAP | PFCP-all F1=87.80，PFCP-session F1=92.30；NGAP-all F1=69.31，UCM 层 F1=60.93，显示复杂层级下降。 | 中：论文内表格，有层级困难证据。 | `P:698-734` |
| Hermes / NEUTREX 对比 | SpecGPT 在 NAS action/condition 上 86.41/92.94，高于 Hermes 81.39/86.40；Hermes GT 上 LLM tagging F1=88.90，高于 NEUTREX。 | 中偏弱：依赖 Hermes 报告与作者复用 GT，实际 state machines 未公开。 | `P:735-789` |
| 直接 prompt baseline | 作者称直接 prompt 各 LLM 输出状态机 F1 只有 14.87%，支持“需要 pipeline”结论。 | 中：关键反证，但输出样例未公开。 | `P:685-689`, `D:192-199` |
| 成本/泛化 | 每次运行成本估算 NAS $2.7、NGAP $1.6、PFCP $1.5；R15 NAS 抽取 142 transitions，约比 R17 少 20%。 | 中：论文给 token/time 表，但 provider 价格会漂移。 | `P:791-860` |
| 证据总体 | 事后指标丰富、真实长规格任务强；但代码、GT、输出、复现包缺失，证据不适合直接 same-sample comparison。 | 中。 | `A:13-19`, `A:38-50` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | Source pointer |
|---|---|---|
| 输入可同样本性 | 不适合同样本：输入是 3GPP 长规格而非 Project 1 控制系统功能安全需求；可借鉴长文档切分和 grounding，但不能直接拿其样本跑本项目主表。 | `P:57-85`, `P:130-136`, `D:200-208` |
| 输出可归一性 | 部分可归一：protocol FSM 的 states/transitions/action/condition 可映射到 flat STM 字段；但缺控制变量、时间约束、层次/并发和可执行 DSL。 | `P:235-254`, `P:413-436`, `D:200-208` |
| 模型预算 | 多模型 ensemble 成本和 hosted-provider 组合与本项目预算差异大；若复刻，需单独列模型预算和 provider drift 风险。 | `P:530-541`, `P:791-840`, `A:48-50` |
| 人在回路预算 | GT 构建超过一般实验预算；manual alignment 不可量化。 | `D:132-137`, `A:18`, `A:36` |
| 反馈预算 | 可复用 JSON/schema + ensemble 作为 ablation idea；不能把 GT F1 当 in-loop feedback。 | `P:461-474`, `P:530-588`, `P:641-697` |
| GT 可得性 | 不可得；公开输入规格不等于公开 benchmark。 | `A:17-19`, `A:36`, `S:250` |
| 最终决策 | `evidence-only / near`：用于 Related Work 和反证“长规格到 FSM / LLM ensemble 已有人做”，不进入严格 same-sample approximate baseline。 | `A:42-50`, `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/SUMMARY.md:§6` |

## 7. 表 F：Claim 风险与 handoff

| 项目 | 结论 | Source pointer |
|---|---|---|
| 打穿的 claim | 不能声称“长篇自然语言规格到 FSM 抽取尚无人做”或“LLM ensemble + domain prompt 抽取协议状态机是本文首创”。 | `P:21-30`, `P:121-139`, `P:956-971` |
| 可保留的弱化表述 | 可说本文聚焦控制系统需求、可执行 STM schema、scenario-level feedback 与 repair decision。SpecGPT 聚焦通信协议规格抽取且无公开代码/GT。 | `P:888-915`, `D:200-208`, `A:13-19` |
| S1b handoff | Related Work 中作为“long technical specifications -> protocol FSM”的强相关 evidence-only prior；强调其 chunking、domain prompt、span grounding、ensemble 对本项目有方法启发。 | `P:333-588`, `D:192-208` |
| S3 handoff | 不建议重跑原实验；若需要做近似 ablation，可只抽取 `section-tree chunking + JSON schema + majority voting` 作为 pipeline 变体，并使用本项目公开控制需求样本。 | `P:292-356`, `P:413-474`, `P:530-588`, `A:46-50` |
| 风险等级 | M/I：claim 风险高于复现实验价值；证据足以约束 novelty，但不足以支撑直接可复现实验比较。 | `A:17-19`, `A:46-50`, `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/SUMMARY.md:§7` |

## 8. 待补与风险

1. **GT 与代码缺失**：若未来必须做 protocol FSM 复现，只能先联系作者或自行重建 GT；当前不得把 3GPP 输入规格误写为公开 benchmark。Source：`A:17-19`, `A:36`, `A:46-50`。
2. **manual alignment 不清**：原文提到 manual alignment，但未给流程和一致性，S1b 不应把它写成可复用 human-in-the-loop protocol。Source：`P:530-544`。
3. **formal role 容易夸大**：输出 FSM 可服务 verification/testing，但本文没有模型检查或仿真闭环。Source：`P:888-915`, `P:956-971`。
4. **模型/价格漂移**：五模型 hosted API、温度和价格表应只作为论文时点证据，不作当前成本事实。Source：`P:791-840`。
