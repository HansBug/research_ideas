# Designing FSMs from Requirements with GPT-4

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `nguenaTimo2026DesigningFSMRequirementsGPT40` |
| 论文 | Omer Nguena Timo, Paul-Alexis Rodriguez, Florent Avellaneda. *Designing FSMs Specifications from Requirements with GPT 4.0*. arXiv:2603.29140, 2026. |
| 本地源目录 | `project_1_llm_state_machine_modeling/baselines/designing-fsm-specifications-from-requirements-gpt4/` |
| 本地输出 | `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/papers/designing-fsm-specifications-from-requirements-gpt4.md` |
| baseline verdict | 🟢 direct STM baseline：输入是英文自然语言 DFSM 描述，输出是可解析 CSV DFSM / Mealy machine；但数据合成、语义较平坦。 |

source pointer：`bibtex.bib:1-9`；`DESC.md:21-63,173-206`；`ASSETS.md:11-18,29-49`；`paper_content.txt:11-32,83-104,111-132,185-190,191-235,255-300,349-398,404-489,492-620,621-691,697-755`。

## 1. 阅读审计

| 审计项 | 已读范围 | 结论 |
|---|---|---|
| `bibtex.bib` | 全文 | 确认 arXiv 2026、作者、标题、引用键和 URL。 |
| `paper_content.txt` | 覆盖摘要、引言、方法、实验、四类 repair、结论与附录 pattern | 重点核对 DFSM 定义、GPT-4o prompt、随机 oracle、语法/语义比较、repair 实验和局限。 |
| `DESC.md` | 全文 | 用于复核中文摘要、baseline 评估、方法/实验总结与 Project 1 差距。 |
| `ASSETS.md` | 全文 | 用于复核 arXiv、GitHub `Paul3246/nl2fsm`、数据/结果资产、license/release 风险。 |
| 不确定项处理 | 原文未给 DOI；正文未给 GitHub 链接；模型只见 `gpt-4o` 与 GPT-4.0 表述 | 按“原文未说明/本轮额外核到”写，不把仓库当作论文内正式 artifact。 |

source pointer：`bibtex.bib:1-9`；`DESC.md:13-19,54-63`；`ASSETS.md:13-18,31-39,45-49`；`paper_content.txt:191-235,350-398,697-755`。

## 2. 表 A：方法框架与任务定位

| 字段 | 内容 |
|---|---|
| 输入 NL | 合成英文 DFSM 描述：随机生成 oracle DFSM，再用句式模板把每条转移转写成自然语言；不是工业/控制系统真实需求。 |
| 任务目标 | 将英文文本描述转为 deterministic finite state machine / Mealy machine 规格，并研究生成错误的检测与修复。 |
| agent/prompt 模式（多选 tag+解释） | `single-prompt generation`：一次 prompt 生成 CSV DFSM；`format-constrained prompting`：要求 `State,Input,Output,Next_State` CSV；`oracle/trace feedback repair`：把语法 fault、distinguishing sequence 或 checking sequence 写回 prompt；`formal-method constrained repair`：fault-model/mutation-machine repair 不再让 LLM 自由修复；`no multi-agent`：未见 agent 协作。 |
| LLM 模型四元组 | provider：OpenAI；model：代码片段为 `gpt-4o`，论文叙述称 GPT-4.0/GPT-4；temperature：0.0；max output/context/date：原文未说明。 |
| 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 类型：平坦 complete deterministic Mealy DFSM；语义：输入/输出 trace 等价；可执行性：CSV 可解析为 DFSM，适合自动比较；guard：无布尔 guard，仅输入符号；action：只有输出符号，无变量更新/动作块；hierarchy/time/concurrency：无；应用：高层 reactive-system 规格与 FSM testing；差距：缺少控制系统变量、复杂 guard/action、时间约束、层次/并发和安全性质。 |
| 人在回路角色 | prompt engineering 由工程师设计；repair 中“专家/oracle”提供期望转移或输入序列输出，实验中由 DFSM oracle 模拟专家。 |
| 输出后人工改动 | 未报告人工直接改 CSV；repair 通过 LLM 重新生成或 fault-model mining 选择候选。语法 fault repair 依赖 oracle 精确差异，现实性被作者承认较弱。 |

source pointer：`paper_content.txt:111-132`（DFSM 定义）、`paper_content.txt:171-190`（合成描述与专家/oracle）、`paper_content.txt:191-235`（prompt 与 `gpt-4o`）、`paper_content.txt:255-300`（语法/语义比较）、`paper_content.txt:404-489,492-620,621-691`（四类 repair）；`DESC.md:25-41,95-123`。

## 3. 表 B：资产状态与可复现性

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `nguenaTimo2026DesigningFSMRequirementsGPT40`。 |
| 论文与版本 | arXiv:2603.29140，2026，未见 DOI；本地有 `paper.pdf` 与 `paper_content.txt`。 |
| Reference/GT | GT 是作者随机生成的 DFSM oracle；每个 oracle 自动生成英文描述；实验用 5/10/25 states、5 inputs、2 outputs，常规每规模 30 oracles，25 states 只报告 1 个。 |
| 数据与 artifact | 原文未给独立数据下载；本轮额外核到 `Paul3246/nl2fsm`，含 `v1`-`v5`、`err_lim`、`Fault_model_approach.zip`、示例数据/结果，但不是冻结 replication package。 |
| 已有本地复现资产 | 本地已有论文 PDF、提取文本、`DESC.md`、`ASSETS.md`；`ASSETS.md` 记录 GitHub HEAD `354f9aacf51b5121abb8a2e04718232185e71928` 与部分结果/数据入口。 |
| 可复现路径 | 冻结 GitHub HEAD → 检查依赖与潜在 `.env` 风险 → 配置 OpenAI API → 复跑 `v1`/`v4`/`v5`/fault-model 流程 → 对齐论文 Table 1-5。需要补模型 ID、日期、调用成本、seed 与生成 oracle 清单。 |
| 资源许可与访问风险 | GitHub 仓库无 release、license、依赖锁；论文正文未引用该仓库；实验调用真实 API，存在 provider drift 与成本风险；合成数据没有标准 split。 |

source pointer：`ASSETS.md:11-18,29-39,45-49`；`DESC.md:13-19,127-149`；`paper_content.txt:349-398,475-489,591-596,664-676`。

## 4. 表 C：生成流程内反馈

| 字段 | 内容 |
|---|---|
| 静态/schema | 有。prompt 强约束 CSV header 和字段顺序；生成结果被解析为 DFSM，并检查状态/转移差异、input-complete/确定性等。普通 schema/CSV 约束不记为 formal verification。 |
| 编译/可执行性 | 无传统编译；有 DFSM 解析与 machine-level 比较。checking-sequence 算法中若生成机器不 input-complete 会先转换为 input-complete。 |
| oracle/trace/等价性 | 有，仅在 repair loop 中使用：语法 fault diff、distinguishing input-output sequences、checking sequence、fault-model output queries 都依赖 oracle/专家反馈。初次生成后的 Table 1 评估本身是 post-hoc，不算 in-loop。 |
| 仿真执行 | 无控制系统仿真；有随机 oracle 实验和 trace/sequence 计算，但不是系统仿真。 |
| 形式化验证 | 无 UPPAAL/NuSMV/性质模型检查；FSM 等价、distinguishing automaton、checking sequence 属于 oracle/trace/testing feedback，不在本表记作 formal verification。 |
| 人类过程反馈 | 设计上专家可回答 checking sequence / output query；实验中主要由 oracle DFSM 自动模拟专家。 |
| 反馈粒度 | transition-level fault；input-output trace；single checking sequence；fault-model repair domain 中的 output query。 |
| 反馈自动化程度 | 合成实验中高（oracle 自动给出差异/输出）；现实场景中中-低（专家需回答行为 query）。 |
| 人类反馈交叉一致性 | 原文未报告多专家一致性或交叉标注。 |

source pointer：`paper_content.txt:255-300`（syntax/semantic evidence）、`paper_content.txt:404-489`（syntax repair loop）、`paper_content.txt:492-553`（distinguishing repair）、`paper_content.txt:561-620`（checking sequence + expert）、`paper_content.txt:621-691`（fault model + output queries）；`DESC.md:118-123`。

## 5. 表 D：事后评测、指标与证据强度

| 维度 | 内容 |
|---|---|
| post-hoc 指标 | fault type mean/max；faulty generated DFSM 数；repair succeeding rate；repair attempts；output query 数/长度；repair domain augmentation 次数。没有使用 GT F1/专家评分。 |
| 主要结果 | 5-state 初始生成平均 fault 0.03、最大 1；10-state 平均 fault 1.1、最大 11。syntax repair 5/10-state 成功率均 100%；distinguishing repair 5-state 100%、10-state 0%；checking sequence 5-state 40%；fault-model repair 5/10-state 均 100%，但部分 repair domain 被 oracle-specific transition 增强。 |
| 证据强度 | 内部效度：中-高，因为合成 oracle 可精确比较；外部效度：低-中，因为文本是模板合成、样本规模小、25-state 只有 1 个、无真实控制系统需求。 |
| 评测盲点 | 未报告真实专家评审、多模型比较、成本、prompt 稳健性、真实工业需求、层次/并发/时间语义。 |

source pointer：`paper_content.txt:349-398`（实验设置与 Table 1）、`paper_content.txt:466-489`（syntax repair Table 2）、`paper_content.txt:517-553`（distinguishing Table 3）、`paper_content.txt:591-620`（checking Table 4）、`paper_content.txt:647-691`（fault-model Table 5）；`DESC.md:150-157`。

## 6. 表 E：同样本近似与可比性决策

| 字段 | 决策 |
|---|---|
| 是否可做同样本直接比较 | 不建议作为控制系统主数据集的同样本直接 baseline；原样本是随机 DFSM + 模板英文描述，与 Project 1 的真实控制系统功能安全需求分布不同。 |
| 可做的近似比较 | 可作为 synthetic smoke / oracle-rich baseline：用其 DFSM CSV 任务测试 parser gate、trace equivalence、fault-type 统计、repair feedback 设计。 |
| 与 Path-1 S1a 的放置 | 作为 direct STM baseline 方法条目保留，但实验可比性标注为“任务同构、样本不同”。 |
| 若复跑需要 | 固定 `nl2fsm` HEAD、生成 oracle seed、模型 ID/date/usage、prompt hash、必要脱敏输出摘要、repair attempts；不要把 fake/replay 或 oracle-augmented repair 冒充真实无 oracle 场景结果。 |

source pointer：`paper_content.txt:171-184,349-398,697-755`；`ASSETS.md:31-49`；`DESC.md:197-206`。

## 7. 表 F：Claim 风险与 handoff

| 风险 / handoff | 内容 |
|---|---|
| Claim 风险 1 | 不应写成“LLM 能从真实工业需求稳定生成控制系统状态机”；原文只做合成英文 DFSM 描述，作者未来工作才考虑 industrial-like descriptions。 |
| Claim 风险 2 | 不应把 CSV/schema 检查或 FSM testing feedback 写成通用 formal verification / model checking。 |
| Claim 风险 3 | fault-model repair 的 100% 成功率带有 oracle/repair-domain augmentation 条件，不能外推到无 oracle 真实需求。 |
| 可 handoff 到 Project 1 | 引入 machine-readable output gate；用 missing transition / wrong output / transfer fault 映射缺陷类型；设计 trace/checking-sequence 专家最小查询；比较“LLM 自由修复”与“候选空间受限修复”。 |
| 下一步 | 若纳入实验，先复现最小 5-state synthetic chain，再决定是否把 CSV DFSM 转成 pyfcstm/内部 DSL；补模型 / 日期 / 用量 / 脱敏说明。 |

source pointer：`paper_content.txt:404-489,621-691,697-755`；`DESC.md:197-206`；`ASSETS.md:45-49`。

## 8. 待补与风险

1. 需要确认 `Paul3246/nl2fsm` 与论文版本的作者/版本对应关系；论文正文未给仓库链接。
2. 需要补 license、依赖、运行命令、seed、模型调用记录与结果对齐表。
3. 若用于论文 claim，只能说“合成 DFSM 描述上的 direct baseline”，不能说“控制系统需求 benchmark”。
4. 需要区分初始生成 post-hoc oracle comparison 与 repair loop 的 in-loop oracle feedback。
