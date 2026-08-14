# llms_emp

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `wang_generating_2025` |
| 论文 | *Generating SysML Behavior Models via Large Language Models: an Empirical Study* |
| 作者 / 年份 | Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, Chunming Hu / 2025 |
| Venue | Internetware 2025, ACM |
| DOI / URL | `10.1145/3755881.3755926` / <https://dl.acm.org/doi/10.1145/3755881.3755926> |
| 原始目录 | `project_1_llm_state_machine_modeling/baselines/llms_emp/` |
| 本篇定位 | 九大 direct baseline 中的 mandatory closest；最适合作为 Path-1 的 SysML STM 子集 same-sample approximate 候选，但其反馈主要是 PlantUML/SysML rule-based checking，不等于已接入完整 formal verification 或 simulation traces。 |

主要 source pointer：

> 以下未带目录前缀的 source pointer 均相对于上表“原始目录”；跨库文件使用完整相对路径。

- 元信息：`project_1_llm_state_machine_modeling/baselines/llms_emp/bibtex.bib:2-18`；`DESC.md:5-18`；`ASSETS.md:21-24`。
- 任务与贡献：`paper_content.txt:83-119`（摘要）、`paper_content.txt:126-203`（SysML behavior diagrams、数据集、两阶段研究）。
- 数据集构建：`paper_content.txt:328-381`（G_Search/G_Model、重建与需求补写）、`paper_content.txt:458-483`（Table 2 领域与 ACT/STM/SD 数量）、`ASSETS.md:13-17`（Drive 与本地 parquet）。
- 实验流程：`paper_content.txt:394-429`（RQ1/RQ2 与 Phase-I/Phase-II）、`paper_content.txt:430-453`（四类检查与 F1）、`paper_content.txt:551-601`（模型、prompt、temperature=0）。
- 结果与反馈边界：`paper_content.txt:627-678`（Phase-I 结果）、`paper_content.txt:683-770`（幻觉分类）、`paper_content.txt:779-853`（Phase-II rule feedback、成本与 counterexample/future）、`paper_content.txt:894-924`（Table 11 逐类修复）。
- 资产与复现：`ASSETS.md:13-17`、`ASSETS.md:26-36`、`ASSETS.md:38-46`；`project_1_llm_state_machine_modeling/baselines/SUMMARY.md:126`（五绿 direct baseline 总账行）。

## 1. 阅读审计

| 文件 | 已读范围 | 用途 | 关键注意 |
|---|---|---|---|
| `bibtex.bib` | 全文 `1-19` | 元信息、稳定引用键、DOI、venue | ACM Internetware 2025，论文页与 DOI 已明确。 |
| `paper_content.txt` | 覆盖摘要、引言、相关工作、数据集、实验设计、结果、威胁与结论；重点行见 §0 | 抽取任务、输入输出、LLM、prompt、反馈、指标、局限 | 原文把 Phase-II 称为 model-checking rules，但多数证据是 PlantUML format、SysML grammar/semantics 与 reference F1 的规则/人工检查；simulation traces 和 counterexamples 是未来建议。 |
| `DESC.md` | 重点读 `5-121`、实验与局限段、文献分类段 | 复核中文摘要、数据集规模、方法总结、局限 | `DESC.md` 中“模型检查规则”需在本文件中弱化为 rule-based checking，不上调为完整 formal verification。 |
| `ASSETS.md` | 全文 `1-46` | 代码/数据/结果资产、parquet 与风险 | 公开的是 Drive 数据与结果表；未发现生成/修复 pipeline 源码。 |
| `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` | 对应行 `126` 与规则提示 `110` | 复核五绿 direct baseline 与形式化验证口径 | 总账已要求对 `llms_emp` 的检查/修复环按弱形式化或半形式化约束处理。 |

## 2. 表 A：方法框架与任务定位

| 输入 NL | 任务目标 | agent/prompt 模式（多选 tag+解释） | LLM 模型四元组 | 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 人在回路角色 | 输出后人工改动 |
|---|---|---|---|---|---|---|
| SysML behavior model 对应的自然语言需求描述；部分来自原始需求，部分由 G_Model 分析模型结构和行为后补写。Source: `paper_content.txt:371-381`, `paper_content.txt:861-864`。 | 从 NL 生成 SysML behavior models，并评估 LLM 在 STM/ACT/SD 三类行为图上的语法、语义一致性和幻觉；Phase-II 用检查规则反馈再生成。Source: `paper_content.txt:394-429`。 | `structured-prompt`：Role + Instruction + Requirements + Sample + Error 五段；`RAG/spec-injection`：检索 PlantUML 与 SysML v1.6 规范；`few-shot/sample`：Sample 中给 PlantUML 格式；`feedback-regeneration`：把检查结果作为 Error 注入；非 multi-agent。Source: `paper_content.txt:561-601`, `paper_content.txt:410-429`。 | 论文表 5 口径：GPT-4 / GPT-4-Turbo / OpenAI official API / temperature=0；GPT-4o / `GPT-4o-2024-11-20` / OpenAI / temperature=0；Kimi / Moonshot-v1 / Moonshot AI / temperature=0；Claude / Claude 3 Haiku / Anthropic / temperature=0；Llama / Llama3.1 / Meta AI via NVIDIA API / temperature=0；DeepSeek / DeepSeek-v3 / DeepSeek via NVIDIA API / temperature=0。Source: `paper_content.txt:551-571`, `paper_content.txt:597-601`。 | 输出是 PlantUML 格式的 SysML v1.6 behavior models，包含 STM/ACT/SD；STM 语义对象按 state、vertex、pseudostate、region、transition 统计，可表达 composite state、region、pseudo state、transition 等，但不是本项目 `pyfcstm` schema。PlantUML 可渲染且格式可自动检查，但 PlantUML 缺少 SysML grammar/semantic checker，许多验证需人工规则检查；guard/action/time/concurrency 只按 SysML/PlantUML 表达和错误类别间接出现，未形成本项目式可执行 scenario-level repair feedback。Source: `paper_content.txt:491-503`, `paper_content.txt:525-538`, `paper_content.txt:701-710`, `paper_content.txt:894-924`。 | 数据集构建由 G_Search/G_Model 人工收集、重建、补写需求并 cross-validate；Phase-II 中 PlantUML format 可自动报告，SysML grammar/semantics 由人工对标准和 55 条语义规则检查并记录；human review parquet 是事后评审资产。Source: `paper_content.txt:338-381`, `paper_content.txt:430-453`, `ASSETS.md:15-17`。 | 论文不报告把生成模型人工改成最终答案；Phase-II 是 LLM regeneration。人工主要用于数据集重建、需求补写、错误检查/评分和公开 human-review 结果，不应写成“人手工修复生成结果后再计分”。Source: `paper_content.txt:422-427`, `paper_content.txt:434-440`, `ASSETS.md:15-17`。 |

## 3. 表 B：资产状态与可复现性

| 稳定引用键 | 论文与版本 | Reference/GT | 数据与 artifact | 已有本地复现资产 | 可复现路径 | 资源许可与访问风险 |
|---|---|---|---|---|---|---|
| `wang_generating_2025`。Source: `bibtex.bib:2`。 | ACM Internetware 2025，DOI `10.1145/3755881.3755926`，本地 `paper.pdf` 与 `paper_content.txt` 已存在。Source: `bibtex.bib:3-18`, `ASSETS.md:13`。 | Reference model 被假定为语义正确，用于计算 generated vs reference 的 F1；公开数据集含 107 个 SysML 行为模型，摘要称 36 ACT、36 STM、35 SD。Source: `paper_content.txt:190-197`, `paper_content.txt:449-453`, `ASSETS.md:16`。 | Google Drive 公开入口；本地已冻结 raw samples、complete samples、human review 三个 parquet；无公开生成/修复 pipeline 源码。Source: `ASSETS.md:13-17`, `ASSETS.md:26-36`。 | 本仓库已有 `llms_emp_raw_samples.parquet`、`llms_emp_complete_samples.parquet`、`llms_emp_human_review.parquet` 及 SHA-256；原始目录含 PDF、BibTeX、提取文本、`DESC.md`、`ASSETS.md`。Source: `ASSETS.md:15-17`。 | S3 可先冻结本地 parquet，抽 STM 子集，重建 `NL -> PlantUML/SysML STM -> normalized STM`；prompt/RAG/checker 需自行实现，Phase-II rule feedback 可近似但不能宣称完全复现作者 pipeline。Source: `ASSETS.md:28-40`, `paper_content.txt:561-601`, `paper_content.txt:790-808`。 | Drive 权限和结构可能漂移；数据公开但许可细节需正式实验前复核；代码缺失；paper text 在 `paper_content.txt:389-390` 出现“34 state machine diagrams”的抽取/正文不一致，而摘要与 Table 2 total/ASSETS 是 36 STM，需以公开 parquet 与 Table 2 复核。Source: `ASSETS.md:42-46`, `paper_content.txt:389-390`, `paper_content.txt:458-483`。 |

## 4. 表 C：生成流程内反馈

> 本表只统计影响 LLM 生成/再生成的 in-loop feedback；GT F1、人类评分、human-review parquet 是 post-hoc eval 或审计资产，除非被明确注入再生成，否则不写成流程内反馈。

| 静态/schema | 编译/可执行性 | oracle/trace/等价性 | 仿真执行 | 形式化验证 | 人类过程反馈 | 反馈粒度 | 反馈自动化程度 | 人类反馈交叉一致性 |
|---|---|---|---|---|---|---|---|---|
| 有。PlantUML format checking 自动报告；SysML grammar/semantic checking 依据标准和 55 条语义规则记录错误；这些错误作为 Error prompt 进入 Phase-II regeneration。Source: `paper_content.txt:430-440`, `paper_content.txt:592-596`, `paper_content.txt:779-789`。 | 弱。PlantUML format 可以理解为 render/parse 层面的可接受性；原文明确 PlantUML 缺少 SysML syntax/semantic checking，未证明生成 STM 可执行。Source: `paper_content.txt:525-538`。 | 无 trace/oracle repair loop。要求一致性通过 generated model 与 reference model 的 GP/F1 衡量；Phase-II 使用“缺失状态/错误 transition”等规则修复，但不是 distinguishing trace、oracle equivalence 或 scenario execution。Source: `paper_content.txt:441-453`, `paper_content.txt:738-758`, `paper_content.txt:909-924`。 | 无。原文把 simulation-based validation 作为 model generation functional correctness 的一般需求，并在摘要/讨论中说 counterexamples 与 simulation traces 是未来更优反馈。Source: `paper_content.txt:105-110`, `paper_content.txt:449-450`, `paper_content.txt:843-853`。 | 低到中。原文称 model-checking rules / formal verification techniques，但当前证据主要是格式、语法、语义、需求一致性的 rule-based/manual checking；不得上调为完整 model checking、theorem proving 或 timed automata verification。Source: `paper_content.txt:790-808`, `paper_content.txt:833-853`, `paper_content.txt:933-938`。 | 有人工检查痕迹：SysML grammar/semantics 由人工比对标准并 log violations；数据集需求补写和 cross-check 也人工完成。但没有 SME 在生成过程中逐轮指导 LLM 的交互式反馈。Source: `paper_content.txt:434-440`, `paper_content.txt:371-381`, `paper_content.txt:861-864`。 | 幻觉类型 / 检查规则级，例如 Non-Existent Element、Transition must connect two State、Missing State or Transition；不是逐条可执行 trace/counterexample。Source: `paper_content.txt:894-924`。 | 中低。PlantUML format 自动化较高；SysML grammar/semantics 和 requirement consistency 依赖人工/规则表；反馈再生成自动调用但 checker 本身不完整自动化。Source: `paper_content.txt:430-453`, `paper_content.txt:811-818`。 | 未见 inter-rater agreement / Cohen κ 等交叉一致性统计；只报告 cross-validated dataset 和 human-review parquet。Source: `paper_content.txt:380-381`, `ASSETS.md:15-17`。 |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 指标 / 结果 | 证据强度 | 对 Path-1 的使用方式 | source pointer |
|---|---|---|---|---|
| 生成速度 | Phase-I 超过 70% 模型在 10 秒内生成；Phase-II 因顺序检查与多次 regeneration，STM/ACT/SD 的 `GT-II / GT-I` 比例分别约 `(2.72, 7.67)`、`(4.05, 4.81)`、`(4.00, 4.31)`。 | 中 | 可用于说明检查反馈有显著成本，不能把“反馈闭环”免费化。 | `paper_content.txt:627-633`, `paper_content.txt:809-818` |
| 语法/格式 | Phase-I AccP/AccS 多数超过 90%；RAG/规范上下文提高 syntactic accuracy；Phase-II AccP 对 STM/SD 达 100%，AccS 多数接近 100% 但 SD 仍有波动。 | 中强 | 可作为 prompt + rule feedback 对格式/语法有效的 prior evidence。 | `paper_content.txt:635-651`, `paper_content.txt:820-827` |
| 语义一致性 | Phase-I ACT 平均约 97.49%，STM 平均 69.29%，SD 平均 50.02%；Phase-II 有提升但 semantic hallucinations resolution 低，要求一致性 STM 42.14%、ACT 83.33%、SD 16.67%。 | 强，但需注意 F1 是 reference-GP 对齐，不是执行语义。 | 适合支撑“LLM 在行为语义/需求一致性上仍弱，尤其复杂结构和 SD”这一 claim。 | `paper_content.txt:659-678`, `paper_content.txt:833-842` |
| 幻觉分类 | PlantUML format 37 例，SysML grammar 25 例，semantic 72 例，requirement inconsistency STM 23 / ACT 27 / SD 100 例。 | 强 | 可直接作为 Related Work 的 error taxonomy 对比，但不要等同本项目 defect ontology。 | `paper_content.txt:683-758` |
| 修复结果 | Table 11 给出逐规则 resolved counts，例如 format 35/37、grammar 22/25；语义/需求一致性明显较弱。 | 中强 | 可作为“rule feedback 对浅层错误强、对深层语义弱”的 closest evidence。 | `paper_content.txt:790-808`, `paper_content.txt:894-924` |
| 资产证据 | Drive + 本地 parquet，含 raw/complete/human-review；无公开 pipeline 源码。 | 强于多数 baseline，但复现 pipeline 不完整。 | S3 可优先使用 frozen parquet，而不是在线 Drive 作为唯一事实源。 | `ASSETS.md:13-17`, `ASSETS.md:34-36` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | 理由与 source pointer |
|---|---|---|
| 输入可同样本性 | 高：STM 子集可作为 same-sample approximate 候选。 | 数据集中每个模型有需求描述，公开 Drive + 本地 parquet；但部分需求由作者从模型结构推断，需用输入差异标记说明。Source: `paper_content.txt:371-381`, `ASSETS.md:16`。 |
| 输出可归一性 | 中高：PlantUML SysML STM 可映射到本项目 flat/typed STM，但 hierarchy/region/pseudostate/PlantUML 特性需归一。 | STM grammar points 包含 State、Vertex、Pseudostate、Region、Transition；与 `pyfcstm` 的状态/事件/guard/action schema 不完全同构。Source: `paper_content.txt:491-503`。 |
| 模型预算 | 中：原文使用 6 个 LLM，温度 0；后续可选少数模型复刻，但不必覆盖全矩阵。 | 模型列表和 greedy sampling 明确。Source: `paper_content.txt:551-601`。 |
| 人在回路预算 | 中：若复刻 Phase-II，需要人工/规则检查 grammar、semantics、requirements inconsistency。 | PlantUML 自动化外的 SysML grammar/semantics 检查依赖人工记录。Source: `paper_content.txt:430-440`。 |
| 反馈预算 | 中：可近似实现 rule feedback，但不应与本项目 executable trace feedback 混为一类。 | Phase-II 将 rule/error 注入 prompt；counterexample 和 simulation trace 是未来。Source: `paper_content.txt:422-429`, `paper_content.txt:843-853`。 |
| GT 可得性 | 高：reference models 与 human review parquet 已本地冻结。 | `ASSETS.md:15-17`。 |
| 最终可比性决策 | **same-sample approximate candidate（优先 STM 子集）**。适合比较“prompt/RAG/rule checking baseline vs 本项目 executable feedback loop”，不适合宣称完整 pipeline 复现。 | 综合以上。 |

## 7. 表 F：Claim 风险与 handoff

| 类型 | 内容 | 风险等级 | handoff |
|---|---|---|---|
| 会被打穿的 claim | “我们首次做 NL -> SysML/STM behavior model generation”；“我们首次做 LLM 生成后检查反馈”；“现有工作没有公开 SysML behavior dataset”。 | C/I | S1b Related Work 必须正面承认本篇是 closest direct baseline。 |
| 需要弱化的 claim | 可写成“已有工作已探索 NL -> SysML behavior models 与 rule-based checking feedback；我们的差异是面向控制系统可执行 STM schema、scenario/trace feedback 与 repair decision（若实验确实支持）”。 | I | 写作时避免“first”，改用“differs from / complements”。 |
| 不能误写的点 | Phase-II 的 grammar/semantic/consistency check 不等于完整 formal verification；simulation traces/counterexamples 是作者提出的未来方向，不是本文已接入。 | C | S1b 与 S3 都必须沿用本文件 §4 的反馈口径。 |
| S1b handoff | mandatory closest；建议在 Related Work 中列为“SysML behavior model empirical baseline + rule-feedback regeneration”。 | C/I | 关联 `project_1_llm_state_machine_modeling/baselines/SUMMARY.md:126`。 |
| S3 handoff | 先冻结 parquet 与 Drive metadata，再抽 STM 子集；实现 `PlantUML/SysML STM -> normalized STM`；保留 “requirements inferred” 与 “checker not public” 的 输入差异标记。 | C/I | 关联 `ASSETS.md:15-17`, `paper_content.txt:371-381`。 |

## 8. 待补与风险

1. **复核公开 Drive 文件树与本地 parquet schema**：正式 S3 前应记录行数、SHA-256、字段含义、STM 子集过滤逻辑；当前 `ASSETS.md:15-17` 已给 SHA，但未在本文件重新打开 parquet。
2. **解决 STM 数量口径**：摘要/ASSETS/Table 2 total 为 36 STM，而 `paper_content.txt:389-390` 抽取处显示 34；应以公开 workbook/parquet 和 PDF 表格最终复核。
3. **不要复用“model checking”字面称呼做强 claim**：本文当前 evidence 是 rule-based checking + manual semantic checking；本项目若主张 formal/executable feedback，需显式说明差异。
4. **生成 pipeline 缺失**：没有 prompt/RAG/checker 源码；同样本近似需要重建 pipeline，并标注 approximate，而不是 replication。
