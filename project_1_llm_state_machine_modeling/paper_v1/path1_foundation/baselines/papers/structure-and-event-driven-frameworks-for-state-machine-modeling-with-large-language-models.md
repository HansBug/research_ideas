# Structure- and Event-Driven SMF for UML State Machine Generation

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `abdulkarim2026structure` |
| 论文 | Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian, Boqi Chen, Gunter Mussbacher. *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*. arXiv:2604.00275, 2026. |
| 本地源目录 | `project_1_llm_state_machine_modeling/baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/` |
| 本地输出 | `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/papers/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models.md` |
| baseline verdict | 🟢 direct STM baseline：非结构化 NL 系统描述 → UML state machine；目前最接近 Project 1 的自由文本状态机生成 baseline 之一。 |

source pointer：`bibtex.bib:1-12`；`DESC.md:21-37,64-126,127-220,222-252`；`ASSETS.md:11-18,29-33,58-72,74-79`；`paper_content.txt:7-39,42-126,181-218,219-300,301-329,330-437,461-511,512-586,587-721,829-878,922-952`。

## 1. 阅读审计

| 审计项 | 已读范围 | 结论 |
|---|---|---|
| `bibtex.bib` | 全文 | 确认 arXiv 2026、DOI、作者、引用键和 URL。 |
| `paper_content.txt` | 覆盖摘要、引言、背景、方法四策略、LLM 设置、评测设计、实验结果、威胁与结论 | 重点核对输入/输出、Single-Prompt、Structure-Driven、Event-Driven、Hybrid、模型与温度、8 个场景、F1 结果。 |
| `DESC.md` | 全文 | 用于复核中文定位、实验数值、Project 1 差异与 baseline verdict。 |
| `ASSETS.md` | 全文 | 用于复核 4open anonymous artifact、代码、reference solutions、F1 workbook、license/长期可用性风险。 |
| 不确定项处理 | 论文对 Single-Prompt few-shot 在不同位置存在 2-shot / 3-shot 口径差异 | 以实验设置段为主：multi-step 2-shot，single-prompt 3-shot；同时保留 source pointer。 |

source pointer：`paper_content.txt:219-227,497-511`；`DESC.md:113-126`；`ASSETS.md:15-18,47-56,64-68`。

## 2. 表 A：方法框架与任务定位

| 字段 | 内容 |
|---|---|
| 输入 NL | 8 个非结构化英文 reactive-system / modeling problem descriptions，来自本科建模课程项目/作业，并配专家参考 UML 状态机。 |
| 任务目标 | 全自动从非结构化 NL 需求生成 UML state machine，覆盖 states、events/transitions、guards、transition actions、hierarchical states、parallel regions、history states。 |
| agent/prompt 模式（多选 tag+解释） | `single-prompt baseline`：一次生成完整 Umple；`few-shot prompting`：multi-step 使用 2-shot，实验设置称 single-prompt 使用 3-shot；`structure-driven multi-step`：按状态机元素顺序生成；`event-driven multi-step`：按事件逐步抽取转移；`hybrid draft-refinement`：先生成 Umple 草稿，再把草稿附到 Structure-Driven prompts 后作为 baseline；`rule-based post-processing`：多步输出 HTML tables 后合并/修正；`no human-in-loop generation`：生成阶段不依赖人工反馈。 |
| LLM 模型四元组 | OpenAI `GPT-4o`（non-reasoning）与 Anthropic `Claude 3.5 Sonnet`（reasoning）；temperature：多数步骤 0.01，state/event discovery 步骤 0.5；max output：每 prompt 1500 tokens；精确 dated model ID / context window 原文未说明。 |
| 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 类型：UML state machine；Single-Prompt 输出 Umple，multi-step 输出 HTML tables 后处理；语义能力：支持 transition guards、transition actions、hierarchy、parallel regions、history states；可执行性：Umple 具备代码化潜力，但论文未报告编译/执行 gate；time：无实时/clock 约束；应用场景：一般 reactive-system 建模；差距：非控制系统专用，缺少安全/时间/互锁语义和模型检查/修复闭环。 |
| 人在回路角色 | 生成过程中无人工反馈；参考解由 modeling experts 制作；评估由作者人工按规则对齐 GT。 |
| 输出后人工改动 | 原文未报告人工修正生成状态机后再评测；multi-step 有严格 rule-based post-processor，若某步组件处理失败则使用上一个成功处理步骤的输出。 |

source pointer：`paper_content.txt:42-60`（problem statement）、`paper_content.txt:181-218`（architecture/output/postprocessor）、`paper_content.txt:219-300`（四策略）、`paper_content.txt:301-329,474-511`（模型/温度/token/few-shot）、`paper_content.txt:330-384`（GT 与人工评估）；`DESC.md:23-37,68-126`。

## 3. 表 B：资产状态与可复现性

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `abdulkarim2026structure`。 |
| 论文与版本 | arXiv:2604.00275，DOI `10.48550/arXiv.2604.00275`；本地有 `paper.pdf` 与 `paper_content.txt`。 |
| Reference/GT | 8 个系统：Printer、Spa Manager、Dishwasher、Chess Clock、Bread Maker、Thermomix TM6、W-UMPLE、SSC7；每个有非结构化描述与专家参考 state machine。 |
| 数据与 artifact | Anonymous Github / 4open artifact 可访问：源码、prompt/examples、reference solutions、生成图、`Final Detailed F1-Scores.xlsx`。不是实名 GitHub/Zenodo release。 |
| 已有本地复现资产 | 本地 `ASSETS.md` 已记录 hashbang 浏览器入口、ZIP 入口、关键文件大小与 SHA-256；F1 workbook 含 `SinglePrompt`、`StructureDriven`、`EventDriven`、`Hybrid`、`Averages` sheets。 |
| 可复现路径 | 先用 ZIP/API 冻结 artifact 与逐文件 hash → 安装依赖（Graphviz、Java、Umple jar、LLM provider libs）→ 配置 API keys → 复跑四策略两模型 → 用 workbook schema 或人工评审复核 F1。 |
| 资源许可与访问风险 | Anonymous artifact 无稳定 commit、release、正式 DOI 或 license 承诺；运行环境与 exact model version 可能 drift；正式使用前必须本地冻结。 |

source pointer：`ASSETS.md:11-18,29-33,47-68,70-79`；`paper_content.txt:461-511,1002-1003`；`DESC.md:13-20,129-158`。

## 4. 表 C：生成流程内反馈

| 字段 | 内容 |
|---|---|
| 静态/schema | 有。multi-step 要求 HTML tables，并由 strict rule-based post-processor 合并/精化；处理失败时回退到最近成功步骤。Single-Prompt 输出 Umple，但未报告语法/编译 gate。 |
| 编译/可执行性 | 未见 in-loop 编译或执行；Umple 只是 Single-Prompt 的目标语法，论文评测仍靠人工与 GT 对照。 |
| oracle/trace/等价性 | 无 in-loop oracle/trace/等价反馈。GT 和 F1 只用于事后评测，不得写成生成流程内反馈。 |
| 仿真执行 | 无系统仿真或运行 trace 执行。 |
| 形式化验证 | 无模型检查、性质证明或 formal verification engine；普通 HTML/Umple schema/post-processing 不算 formal verification。 |
| 人类过程反馈 | 无生成时 human-in-loop；人工只参与参考解制作与事后评估。 |
| 反馈粒度 | 主要是 stage-level structured output / post-processing fallback，不是错误纠正反馈。 |
| 反馈自动化程度 | 静态后处理自动；质量反馈不进入生成闭环。 |
| 人类反馈交叉一致性 | 原文称由 subset of authors 评估并 agreed on guidelines；未报告 Cohen κ、多评审交叉一致性或盲评。 |

source pointer：`paper_content.txt:212-218`（postprocessor/evaluation）、`paper_content.txt:330-357`（manual evaluation because no evaluator）、`paper_content.txt:358-384`（single author per approach + guidelines）、`paper_content.txt:829-859`（manual bias/output syntax/postprocessor threats）；`DESC.md:214-220`。

## 5. 表 D：事后评测、指标与证据强度

| 维度 | 内容 |
|---|---|
| post-hoc 指标 | 对 7 类组件计算 precision、recall、F1：states、transitions、guards、actions、hierarchical states、parallel regions、history states；整体 F1 聚合 TP/FP/FN。 |
| 主要结果 | Single-Prompt：Claude overall F1 0.7029，GPT-4o 0.5431。GPT-4o 上 Hybrid 0.6559、Structure-Driven 0.6260、Event-Driven 0.3735。Claude 上 Single-Prompt 仍最好，Structure-Driven 0.5026、Event-Driven 0.3052、Hybrid 0.6336。actions、parallel regions、history states 仍弱。 |
| 证据强度 | 中：任务与 Project 1 高度对齐，artifact 和 F1 workbook 可访问；但样本只有 8 个，来自课程场景，评估人工且非盲，多策略输出语法不一致。 |
| 评测盲点 | 无编译/执行/模型检查；未覆盖控制系统时间/安全约束；exact model version 未锁；temperature 0.5 导致可重复性风险。 |

source pointer：`paper_content.txt:386-437`（评价公式和组件）、`paper_content.txt:523-586`（RQ1/Single-Prompt）、`paper_content.txt:603-665,709-721`（GPT-4o multi-step）、`paper_content.txt:678-703,810-822`（Claude multi-step）、`paper_content.txt:829-878`（validity threats）；`DESC.md:159-220`。

## 6. 表 E：同样本近似与可比性决策

| 字段 | 决策 |
|---|---|
| 是否可做同样本直接比较 | 可作为“外部 8-case same-sample”复跑候选：artifact 提供输入描述、reference solutions、生成图和 F1 workbook；但它不是 Project 1 现有 101 条控制系统需求主样本。 |
| 可做的近似比较 | 对同 8 个案例运行 Project 1 方法，按 states/transitions/guards/actions/hierarchy/parallel/history 的 P/R/F1 近似比较；或者只用其维度作为 Project 1 评测 schema 参考。 |
| 与 Path-1 S1a 的放置 | 推荐作为 direct baseline 中最高优先级条目；同时在论文中说明“自由文本 UML state machine baseline”，不是控制系统安全/时间状态机 baseline。 |
| 若复跑需要 | 先冻结 4open artifact；明确模型版本和调用日期；保持 train/test few-shot 排除规则；统一输出语法或明确 Umple vs HTML tables 差异对评分的影响。 |

source pointer：`ASSETS.md:58-72`；`paper_content.txt:461-511,846-859,861-876`；`DESC.md:233-252`。

## 7. 表 F：Claim 风险与 handoff

| 风险 / handoff | 内容 |
|---|---|
| Claim 风险 1 | “fully automate” 是研究目标/任务定义，不代表结果已达到完全自动化；原文明确 performance remains insufficient，尤其 actions/parallel/history。 |
| Claim 风险 2 | 不应把 post-processor、HTML tables 或 Umple 输出写成 formal verification；原文无模型检查/执行验证。 |
| Claim 风险 3 | 多步 prompting 并非普遍优于单提示：对 GPT-4o 有益，对 Claude 3.5 Sonnet overall 反而不如 Single-Prompt。 |
| 可 handoff 到 Project 1 | 采用细粒度槽位评测；设计 hybrid “先全局草稿、再结构化查漏补缺”；按模型类型选择 workflow；把 actions/guards/hierarchy 作为关键难点而非只看 state/transition。 |
| 下一步 | 冻结 artifact 后抽取 8 个输入和 GT；实现统一评分 mapping；若写 paper，把该工作设为最强 direct baseline 并突出 Project 1 在控制系统语义/验证闭环上的差异。 |

source pointer：`paper_content.txt:576-586,656-665,823-828,922-952`；`DESC.md:246-252`；`ASSETS.md:74-79`。

## 8. 待补与风险

1. 必须本地冻结 anonymous artifact；不能长期依赖 4open hashbang 页面。
2. 需要确认 artifact license、release/commit、exact provider model IDs 和运行日期。
3. 若进行同样本复跑，要重新审查人工评分协议和多评审一致性；原文未给 κ 等一致性指标。
4. 需要避免把 GT F1 事后评分误写成 in-loop feedback。
