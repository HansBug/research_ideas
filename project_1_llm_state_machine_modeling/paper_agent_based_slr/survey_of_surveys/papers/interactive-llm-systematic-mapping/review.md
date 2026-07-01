# On the road to interactive LLM-based systematic mapping studies

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | On the road to interactive LLM-based systematic mapping studies |
| 年份 | 正式期刊卷期 2025；online available 为 2024-10-31，`metadata.json` 记录 `publication_date=2024-11-01` |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 类型 | 解决方案提案（solution proposal）；LLM-supported systematic 系统映射研究 方法设想；非实证 SLR/SMS |
| SE 子领域 | LLM-supported 系统映射研究 / evidence-based software engineering 方法学 |
| 阅读状态 | 已读全文文本-paper_content核验；已回原文核对 Fig. 1 映射流程图 |
| 证据等级 | 全文文本级；Fig. 1 为 原文图表级核对；无实证数值表可核对；补充材料未打开 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| A1 角色 | 为 survey-of-surveys 脚手架提供“LLM 介入 SMS 流程”的阶段划分、输入/输出、人机交互、agent 角色、traceability 和模型漂移风险先验。 |
| 是否目标证据池 | 是：作为 A1 方法脚手架与人机协同风险证据；否：不作为 Paper2 目标领域 finding 或“LLM 自动完成综述”的实证证据。 |
| 一句话结论 | 该文价值在于把 LLM 辅助 系统映射研究 拆成可讨论的流程阶段和 agent 角色；局限在于它是概念性 proposal，没有原型评测、语料分母、纳排执行或性能指标。 |

## 2. 论文内容详读

### 2.1 背景 / 问题

1. 论文从 SE 中 系统映射研究 的常用性出发：系统映射研究 主要用于分类研究和观察趋势，而 SLR 更偏证据综合。由于 系统映射研究 往往覆盖更大主题范围，人工分析大量论文和持续更新都很费力。
2. 作者提出使用 LLM 的动机包括：论文数量持续增加、mapping 范围可扩大、研究设计可通过与 LLM 互动获得补充想法、降低更新 系统映射研究 的工作量。
3. 论文明确采用 human-in-the-loop 视角：研究者仍需要懂 系统映射研究 方法并具备主题专家能力，才能判断 LLM 输出是否可靠。这一点对 Paper2 很关键：该文不是让系统取代专家的论证，而是“专家在环的 LLM 支持流程”设想。

证据锚点：`paper_content.txt` Page 1 Introduction；Page 1 摘要的 Context / Objective / Method / Results / Conclusion。

### 2.2 目标

论文目标不是完成一个新的 系统映射研究，而是讨论在 系统映射研究 各步骤中使用 LLM 的可能性与下一步研究方向。作者希望它作为 SE 社区讨论起点，推动一个经过评估的 holistic solution，但没有宣称已经完成该解决方案。

证据锚点：`paper_content.txt` Page 1 摘要 Objective / Conclusion；Page 1 Introduction 最后一段。

### 2.3 方法：输入 / 输出 / 流程 / 人机或 LLM 角色

论文自述方法是 解决方案提案（solution proposal）：两位作者基于自身 LLM 与 literature review 经验，迭代设计并讨论出方案。核心流程按 Petersen 等 mapping guideline 的阶段展开，Fig. 1 展示了“研究者输入与交互修订”和“LLM 输出”的对应关系；本轮已回 `paper.pdf` Page 2 核对 Fig. 1。

#### 2.3.1 Establishing a need for the map

- **用户输入**：研究目标、上下文信息，例如已有论文摘要。
- **LLM 输出**：研究问题候选、目标补充项。
- **人类角色**：编辑、筛选和确认问题，将其作为下一阶段输入。
- **可迁移点**：Paper2 scaffold 可以把“研究目标 → RQ 候选 → 人工确认”作为 stage 0，而不是让 LLM 直接固定最终 RQ。

证据锚点：`paper_content.txt` Page 2 §2.1；`paper.pdf` Page 2 Fig. 1。

#### 2.3.2 Study identification：search

作者强调搜索策略需要透明和可复现。虽然语义搜索越来越常见，但为了复现性，布尔检索仍有必要。作者提出一个以 human-in-the-loop 为中心的三 agent 架构：

1. **Keyword Identification Agent**：识别相关术语、近义词、历史术语和研究焦点层级。例如同一主题可按概念、子类型或上位类型检索。
2. **Semantic Search Agent**：用 RAG 依据语义相似度提出相关文献；可结合图数据库保存引用关系。它不直接选文献，而是辅助调整检索策略。
3. **Search Strategy Agent**：生成最终可执行的检索式或搜索策略。

作者把前两个 agent 与 citation pearl growing 关联起来：先由种子文献和语义相似文献扩展术语，再回到可复现检索式。

证据锚点：`paper_content.txt` Page 2 §2.2.1；`paper.pdf` Page 2 Fig. 1。

#### 2.3.3 Study identification：inclusion / exclusion

作者认为纳排标准捕捉研究者意图很关键，而研究者搜索意图常常不是一开始就完全显性化，因此持续学习系统可能比硬编码 prompt 更好。技术上，纳排是分类问题，但只输出 include/exclude 不够；LLM 需要给出理由、文本证据和引用，便于研究者核验。

需要注意：原文提到 chain-of-thought prompting 可帮助理解 LLM 决策。迁移到 Paper2 时，不应把它理解为必须暴露模型隐藏推理链；更稳妥的落点是要求可审计的 rationale、证据片段、引用位置和人工 override 记录。

证据锚点：`paper_content.txt` Page 2--3 §2.2.2。

#### 2.3.4 Data extraction and classification

作者区分 inductive coding 与 deductive coding：

- **归纳编码**：以标题和摘要为输入，使用 topic modeling；典型流程为生成 embedding、降维、聚类和生成 topic representation。作者举 BERTopic 作为模块化工具例子。
- **演绎编码**：已有 data extraction scheme，例如 SWE-BOK 类别；可用 one-shot / few-shot prompting，并在处理完整 PDF 时结合 RAG 先定位相关片段再调用 LLM。
- **阅读深度变化**：由于自动化能力提高，作者认为 mapping 不必只停留在 manual screening 的 adaptive reading depth，可把完整论文作为 deductive coding 输入。

证据锚点：`paper_content.txt` Page 3 §2.3。

#### 2.3.5 Visualization

作者指出 ChatGPT 已能生成可视化代码与图表，同时也出现 LIDA 等专门工具；BERTopic 可用于探索文献 landscape。Fig. 1 中用户负责提供数据表并核验图形表示的正确性和质量，LLM 输出图表、bar chart、气泡图等可视化建议或结果。

证据锚点：`paper_content.txt` Page 3 §2.4；`paper.pdf` Page 2 Fig. 1。

#### 2.3.6 Reporting

作者建议把数据表和可视化结果提供给 GPT，请其突出有趣模式、观察和研究空白；研究者再调整和补充报告。这里 LLM 角色更像 pattern spotting / drafting assistant，而不是最终结论裁决者。

证据锚点：`paper_content.txt` Page 3 §2.5；`paper.pdf` Page 2 Fig. 1。

### 2.4 研究问题或等价问题

原文没有列出正式 RQ 表。等价问题是：如何在 系统映射研究 流程各步骤中引入 LLM，以及每个步骤需要什么 agent、prompting、RAG、topic modeling、人类反馈和追踪机制。结尾提出两条研究方向：改进并评估单个步骤；构建覆盖整体 mapping process 的 prototype 来收集进一步想法。

证据锚点：`paper_content.txt` Page 1 Objective；Page 3 Reflections 末尾两条 research directions。

### 2.5 语料 / 纳排 / 抽取

1. **本文自身没有执行系统检索**：没有搜索库、搜索式、筛选分母、纳排清单或 原始研究 corpus。
2. **没有数据抽取表**：作者只引用若干相关研究来支撑每个阶段的可行性或风险，例如检索式生成、screening、topic modeling、case study 判断等。
3. **Data availability**：原文明确说明该研究没有使用数据。
4. **补充材料**：原文 DOI 下有 supplementary material，主要用于被下划线术语的定义；本轮未打开补充材料，不能把其中定义写成已核验事实。

证据锚点：`paper_content.txt` Page 3 Data availability；Page 4 References；Page 1--3 各 Relevant literature 段。

### 2.6 统计 / 分析

本文没有自己的统计分析。它通过 narrative discussion 汇总已有相关研究结论，例如：

- LLM 生成布尔检索式有潜力，但可能牺牲 recall；要求 refinement 可能提高 precision 但进一步降低 recall。
- screening 中 GPT-4 和优化 prompt 可能比 GPT-3.5 或 zero-shot 更好，但高 recall 仍是问题。
- topic modeling 和 BERTopic 可提供层次 topic、关键词和时间分析。
- GPT-4 被用于判断研究是否为 case study 的任务，并被作者作为 data extraction / classification 可能性的旁证。

这些都是“引用文献中的结果”，不是本文的独立实验结果。

证据锚点：`paper_content.txt` Page 2 §2.2.1 Relevant literature；Page 3 §2.2.2、§2.3 Relevant literature。

### 2.7 主要结果

1. 提出 LLM-supported mapping process 的阶段化设想，覆盖 need / RQ、search、inclusion/exclusion、data extraction/classification、visualization、reporting。
2. 提出 search 阶段的三 agent 角色：Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent。
3. 明确 human-in-the-loop 是核心控制点，研究者需要检查、修订、确认 LLM 输出。
4. 强调 traceability：纳排和分类需要理由、引用、证据片段，而不是只给最终标签。
5. 提出未来研究方向：分别评估单步骤策略，以及构建端到端 prototype。

证据锚点：`paper_content.txt` Page 1 Results / Conclusion；Page 2--3 §2；Page 3 Reflections。

### 2.8 效度威胁 / 限制

原文在 Reflections 中集中讨论 validity：

1. 现有研究可能存在 publication bias，且关于 LLM 在 literature review 中可靠性的研究还有限。
2. LLM 快速演化，例如不同模型和未来模型会让当前评估结果过时；这对应 Paper2 中需要处理的 服务提供商漂移（provider drift） / model drift 风险。
3. 很多现有研究来自 SE 之外，因此需要 SE-specific solution 和 SE-specific evaluation。
4. 原文是概念框架，不包含原型、benchmark、真实 mapping run、成本统计、错误分布或人工一致性分析。

证据锚点：`paper_content.txt` Page 3 §3 Reflections。

### 2.9 开放工件

- 论文 PDF 为开放获取，文本提取完整，共 4 页正文与参考文献。
- DOI 页面提供 supplementary material；本轮未打开，不能使用其内容作为已核验证据。
- 原文没有代码仓库、prompt set、benchmark corpus、run record 或评测数据；Data availability 声明没有使用数据。

证据锚点：`paper_content.txt` Page 1 开放获取声明；Page 3 Appendix A / Data availability。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 不是正式 RQ 表，而是“按 系统映射研究 阶段提出 LLM 支持策略”的等价问题；末尾把后续研究拆为单步骤评估与端到端 prototype 两类。 | `paper_content.txt` Page 1 Objective；Page 2 §2.1；Page 3 Reflections 末尾。 | 可迁移为 Paper2 的问题分层：先问流程各阶段如何被支持，再问每阶段如何被评估。 | 不能迁移为“已验证的 RQ 生成方法”；原文没有实证 RQ 质量评价。 |
| dimension pattern | 核心维度是流程树：need/RQ、search、inclusion/exclusion、data extraction/classification、visualization、reporting；search 进一步拆出 keyword、semantic search、search strategy 三 agent；extraction 拆为 inductive / deductive coding。 | `paper_content.txt` Page 2--3 §2；`paper.pdf` Page 2 Fig. 1 已核对。 | 高度可迁移为 survey-of-surveys scaffold 的阶段维度和字段树，尤其适合把“人类输入、交互修订、LLM 输出”作为每阶段通用字段。 | 这是作者提出的 conceptual dimension，不是通过 corpus saturation 得出的分类体系；不能写成通用标准。 |
| finding pattern | finding 形态是 解决方案提案（solution proposal） 的 design claim：LLM 可在 mapping 流程各阶段提供支持，但需要专家在环、可复现检索、可追溯证据和后续评估。 | `paper_content.txt` Page 1 Results / Conclusion；Page 3 Reflections。 | 可迁移为 Paper2 的“方法启发式 finding”：将 LLM 贡献写成辅助、建议、候选生成和审计支持。 | 不能迁移为效果结论；没有证明 LLM 提升 recall、降低成本或提高综述质量。 |
| evidence presentation pattern | 证据呈现以 Fig. 1 流程图 + 各阶段 relevant literature 叙述为主；没有 PRISMA 流程图、筛选表、质量评价表或数据抽取表。 | `paper.pdf` Page 2 Fig. 1；`paper_content.txt` Page 2--3 Relevant literature；Page 3 Data availability。 | 可迁移“流程图 + stage input/output + related evidence”的报告方式，用于展示 Paper2 scaffold。 | 不可作为 empirical evidence presentation 模板；没有分母、样本、统计图或效应比较。 |
| validity / threat pattern | 原文直接指出 publication bias、研究数量有限、模型快速演化、非 SE 证据外推不足，并呼吁 SE-specific evaluation。 | `paper_content.txt` Page 3 §3 Reflections。 | 高度可迁移到 Paper2 风险章节：model drift、证据域偏移、社区评估需求、LLM reliability。 | 原文没有系统 threat checklist；没有定量分析 prompt sensitivity、人工一致性或 API 版本漂移。 |
| report structure pattern | 短期刊 proposal 结构：Introduction → LLM-supported mapping process（按阶段分小节）→ Reflections → references；没有 Method/Results/Discussion 的实证研究结构。 | `paper_content.txt` Page 1--4。 | 可迁移为方法/vision 类 paper 的结构样式：先界定痛点，再给阶段化流程，最后讨论风险与研究议程。 | 不适合作为完整 SLR/SMS 报告结构；不能替代 protocol、search、selection、quality assessment、data synthesis 等章节。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 层级 | 对 survey-of-surveys scaffold 的启发 | 证据锚点 | 采纳边界 |
|---|---|---|---|
| A1-M0：元信息与来源层 | 同一条目可能存在 online year 与正式卷期 year 差异；review 卡片应同时记录正式卷期和 online 日期，避免总账年份混乱。 | `bibtex.bib` year=2025；`metadata.json` publication_date=2024-11-01；`paper_content.txt` Page 1 available online 2024-10-31。 | 只影响元数据记录，不影响方法结论。 |
| A1-M1：综述类型层 | 该文是 解决方案提案（solution proposal），不是 SLR/SMS/tertiary study；schema 需要允许“方法设想型文献”进入脚手架，但与实证综述样本分开。 | `paper_content.txt` Page 1 Method。 | 不能把它计为 completed 系统映射研究。 |
| A1-M2：流程阶段层 | Fig. 1 和 §2 提供了 mapping process 的阶段维度：need、study identification、extraction、visualization、reporting。 | `paper.pdf` Page 2 Fig. 1；`paper_content.txt` Page 2--3 §2。 | 可作为候选 stage taxonomy，不是最终标准。 |
| A1-M3：人机角色层 | 每个阶段都应记录 user input、interactive refinement、LLM output；这比只记录“使用了 LLM”更可审计。 | `paper.pdf` Page 2 Fig. 1。 | Paper2 应进一步加入人工 override、时间成本、错误类型和证据锚点。 |
| A1-M4：agent / 技术机制层 | Search 阶段三 agent、RAG、graph database、BERTopic、one/few-shot、完整 PDF deductive coding 等机制可成为字段候选。 | `paper_content.txt` Page 2--3 §2.2--§2.3。 | 这些是方案组件，不能默认都有效；每个组件需要独立评估。 |
| A1-M5：证据与效度层 | 该文把 traceability、citations、publication bias、model evolution、SE-specific evaluation 放在核心位置。 | `paper_content.txt` Page 2--3 §2.2.2 与 §3。 | Paper2 需要把这些落实为 run record、source anchor、eligibility filter，而不仅是口号。 |
| A1-M6：story / method 贡献层 | 对 Paper2 的启发是“交互式、可审计、阶段化 scaffold”，不是让系统自动接管系统综述专家工作。 | 全文综合；尤其 Page 1 Introduction 与 Page 3 Reflections。 | 任何首创性口号、端到端全自动口号、取代专家口号或已验证端到端的强主张都不受该文支持。 |

## 6. 对 Paper2 story / method 的启发与风险

### 6.1 可正向迁移的启发

1. **定位为 interactive scaffold 更稳**：Paper2 可以强调“帮助研究者构建、审计和迭代综述脚手架”，而不是宣称自动完成系统综述。
2. **阶段化 agent 更容易评估**：按 need、search、selection、extraction、visualization、reporting 拆分，可以分别设计 deterministic checks、LLM judge、人工审计和 run record。
3. **可复现搜索仍要保留 Boolean/log**：原文虽认可 semantic search，但把可复现性与 Boolean search 放在关键位置；Paper2 不应只依赖语义检索或 LLM 生成候选。
4. **纳排和抽取必须 source-grounded**：LLM 输出应带理由、证据片段和引用位置；这可作为候选转化为 Paper2 的 evidence anchor / review trace 字段。
5. **完整 PDF 输入是机会也是风险**：原文认为 deductive coding 可从完整 PDF 获益；Paper2 可探索 full-text extraction，但必须处理 PDF 提取质量、图表缺失和上下文截断。
6. **从单步骤到端到端 prototype 的路线合理**：原文建议先优化 individual steps，再构建整体 prototype；Paper2 方法章可采用类似 staged evaluation 叙事。

### 6.2 必须避免的强主张

1. 不应写首创性或首个全自动 系统映射研究 系统这类口号：本文已经在 2024/2025 提出 interactive LLM-based SMS 的整体方向，且还有相关 screening/search 文献。
2. 不应写系统可以取代专家：原文明确要求研究者懂 mapping methodology 且是主题专家。
3. 不应写端到端全自动或 holistic solution 已实现：原文只是呼吁社区共同构建和评估 holistic solution。
4. 不能写“LLM 搜索已可靠覆盖文献”：原文引用的检索式生成研究反而提示 recall 下降风险。
5. 不应写符合 PRISMA：本文不是 PRISMA 报告，也没有执行系统筛选流程。

### 6.3 对 Paper2 方法的风险提示

| 风险 | 原文触发点 | Paper2 应对 |
|---|---|---|
| Search recall 风险 | GPT-generated query 可能漏掉相关论文；refinement 可能降低 recall。 | 保留人工种子、数据库搜索日志、query version、citation chasing 和 recall-oriented sanity check。 |
| 纳排透明性风险 | include/exclude 分类如果没有理由和引用，缺乏 traceability。 | 要求 evidence span、rationale、source location、人工 override；不要只存最终标签。 |
| 模型漂移风险 | 原文指出 LLM 快速演化会让当前评估过时。 | 记录 provider、model_id、调用日期、prompt、raw output、usage；不要把一次模型结果写成稳定事实。 |
| 域外证据迁移风险 | 很多 LLM literature review 研究来自 SE 之外。 | Paper2 的 claims 限定在 SE 语境，必要时设置 SE-specific pilot。 |
| 概念方案未评估风险 | 本文没有 prototype 或实验。 | Paper2 若要超越该文，需要提供可审计原型、case run、错误分析或至少真实 dry-run 证据。 |
| 工具名过拟合风险 | 文中举 BERTopic、LIDA、LangSmith、WebVoyager 等工具。 | 方法贡献应抽象为功能角色与审计接口，不绑定单一工具名。 |

## 7. 待复核

1. 补充材料（supplementary material）未打开；其中被下划线术语定义未进入本 review 的已核验证据。
2. Fig. 1 已回原文核对；除 Fig. 1 外，本文没有需要数值级核验的表格。
3. CCF 字段本轮沿用本仓库 ccf_venues 缓存记录 IST 为 B 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
4. 原文没有开放代码、prompt、数据或原型；如果后续要引用“artifact availability”，只能写“无数据使用 / 无代码仓库”，不要推断作者未提供所有内部材料。
5. 年份引用需统一：正式引用按 IST volume 178 (2025)；讨论 online-first 背景时可注明 2024-10-31 available online。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__codex.md](../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__codex.md)、[../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__claude.md](../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__claude.md)、[../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__deepseek.md](../../audits/a1dt-v2-19x3/results/interactive-llm-systematic-mapping__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/interactive-llm-systematic-mapping.md](../../audits/a1dt-v2-19x3/adjudications/interactive-llm-systematic-mapping.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `interactive-llm-systematic-mapping` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；4 页全文 281 行均通读 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；二者交叉核对，年份字段已对齐：BibTeX `year=2025` ↔ `metadata.json publication_date=2024-11-01`，Page 1 脚注 "Available online 31 October 2024" 与之一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮未用 Read 打开 PDF；Fig. 1 的文字描述只能依赖 `paper_content.txt` 第 79 行的 caption "The mapping 流程 with LLM support."；列为待人工版面核验 |
| 原文类型 | 解决方案提案（作者自述："The research can be classified as a 解决方案提案"，Page 1 §Method）；既不是 SLR、也不是 SMS、tertiary、MLR；可被视为 愿景 / 路线图 |
| 被编码样本单位 | **无系统样本库**。原文样本单位是"假想 LLM-supported mapping 工作流中的流程阶段 / 智能体 角色 / 人机交互节点"，不是 原始研究 |
| 样本数量 / 分母 | `不适用（不适用）`。论文 References 仅 10 条，全部以叙事 "Relevant literature" 形式被引，不构成 coded sample；`数据可得性声明：未使用数据（No data was used）`（Page 3） |
| 原生树类型 | **维度森林（降级）**：①方法流程树（6 阶段） + ②智能体/role 树（含 search 阶段 3 智能体 + 各阶段 LLM/人 双轨） + ③效度/risk 树（Reflections）。无样本编码模式 |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

**实际读取的本地文件**（按本次会话顺序）：

1. `bibtex.bib`（13 行，已读全文）
2. `metadata.json`（35 行，已读全文）
3. `review.md`（437 行，已读全文，作为返修基线）
4. `paper_content.txt`（281 行，已读全文，覆盖 Page 1 摘要+引言、Page 2 §2、Page 3 §2.4-§3 Reflections+数据可获得性（Data 可获得性）、Page 4 References）

**未读但应核验**：`paper.pdf` 本轮未通过 Read 工具打开。Fig. 1 的视觉结构只通过文本提取中的 caption "The mapping 流程 with LLM support." 推定；图中每个阶段下方的"研究者 input + interactive refinement / LLM output"二/三栏布局，仅通过 §2 各小节自述行文重构，**未做版面核验**。这是本审计第一位的 blocked 风险，A2a 必须打开 PDF 核对。

**5–12 个最关键原文证据锚点**（行号引用 `paper_content.txt`）：

1. **Page 1 摘要 / Method 自述**：`"The research can be classified as a 解决方案提案（solution proposal）. The solution was iteratively designed and discussed among the authors..."`（行 18–19）→ 决定了"非实证、无样本"。
2. **Page 1 Introduction §动机四点**：`"(1) An increased number of published papers... (2) 执行（Conducting） mapping studies on a larger scope; (3) Getting additional research design ideas by interacting with the LLM; (4) Reduced effort allows updating mapping studies more regularly."`（行 35–39）。
3. **Page 1 人在环 前提**：`"reviewers (a) are well educated in using the 系统映射研究 method, and (b) be experts in the topic they are reviewing."`（行 53–55）→ HITL 是硬约束。
4. **Page 2 Fig. 1 caption**：`"Fig. 1. The mapping process with LLM support."`（行 79）→ 图是流程图，不是分类表。
5. **Page 2 §2.2.1 三 智能体 列举**：`"Keyword Identification Agent... Semantic Search Agent... Search Strategy Agent..."`（行 101–120）→ search 阶段的 3-智能体 子树。
6. **Page 2 §2.2.1 Relevant literature - Wang et al. [5]**：`"GPT-generated queries result in less recall... (1) The use of PICO harms recall; (2) ... (3) requesting refinements reduces recall and improves precision."`（行 131–135）→ 这是被引文献的 发现，不是本文 发现。
7. **Page 3 §2.2.2 纳排 模式 雏形**：`"language models have to explain the reasons for inclusion and exclusion. Chain-of-thoughts prompting... citations are indispensable. They allow the verification of arguments and increase traceability."`（行 153–157）→ 纳排输出字段：decision + rationale + citation。
8. **Page 3 §2.3 编码二分**：`"1. Inductive coding... topic modeling... embeddings, reduce dimensions, cluster embeddings, and create topic representations... Bertopic ... 2. Deductive coding: Given is a data 抽取 scheme (e.g., SWE-BOK 类别)... One-shot or Few-shot... RAG architecture..."`（行 177–191）→ 抽取 子树二分。
9. **Page 3 §3 Reflections - 效度 四点**：`"Publication bias and limited studies... The rapid evolution of LLMs... Many existing studies are from outside SE..."`（行 213–223）→ 效度/risk 树叶子。
10. **Page 3 §3 two research directions**：`"Improving individual steps... Build a prototype representing the overall mapping process..."`（行 231–234）→ 路线图 两条。
11. **Page 3 数据可获得性（Data 可获得性）**：`"No data was used for the research described in the article."（即未使用数据）`（行 246）→ 支撑无样本分母的关键原文依据（A2a 前仍按候选证据管理）。
12. **Page 4 References**：10 条参考文献（行 252–280）；其中 [4] = Petersen et al. 2015 SMS 指南，是本文流程阶段的真正母本，等价于"借用现成 阶段 分类法"，不是本文新构建。

### 2. 样本单位与字段来源判定

**Q1: 原文纳入和逐项描述的对象是什么？**

原文不"纳入"任何 原始研究。它"逐项描述"的对象是 **Petersen 等 2015 SMS 指南 提出的 5–6 个流程阶段**（need → search → inclusion/exclusion → 数据抽取 & 分类 → visualization → 报告方式），在每个阶段下逐项描述：（a）人类研究者输入；（b）LLM 输出；（c）拟用的技术机制（RAG、BERTopic、CoT prompting 等）；（d）相关已有文献的旁证。这些"阶段"是单位对象，但它们不是 sample，而是 design slot。

**Q2: 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**

没有。`数据可得性声明：未使用数据（No data was used）`（行 246）。Method 自述为 "iteratively designed and discussed among the authors based on their experience"（行 18–19）。10 条参考文献以叙事方式被引，不是检索结果。

**Q3: 原文字段来自哪里？**

字段来源是 **作者基于 SMS 指南 [4] 构造的 流程模型（process model） + 三 智能体 架构 + HITL 模式 + LLM 技术 menu**，不是 抽取 form / 分类方案（classification scheme；首次术语） / 分类法 / 质量量规 / 复现包。可视为 **概念蓝图（概念蓝图）**，对应 v2 口径下的 "方法学种子 / 边界锚点"。

**Q4: RQ 与样本单位是什么关系？**

原文无显式 RQ 表。Objective 是 "discuss possibilities and next steps for using LLMs (e.g., GPT-4) in the 系统映射研究 流程"（行 17）。它把"流程阶段"既当作 RQ 划分锚点（每个阶段一个 §），又当作贡献组织方式（每段都是一组 design claims + relevant literature）。即：**阶段 = RQ 容器 = 字段容器 = 贡献容器**，三位一体。

**Q5: 若无系统样本库，如何降级？**

按 v2 口径降级为：

- **不进入主统计池**（与 `metadata.json eligible_for_statistical_synthesis=false` 一致）
- **作 边界锚点**：界定"interactive LLM-based SMS"的概念已在 2024/2025 被显式提出，Paper2 不能宣称首创
- **作 方法学种子**：为 Paper2 的 scaffold 提供候选 阶段 分类法 与 HITL/智能体 字段模板
- **作 风险清单种子（风险清单种子）**：Reflections 中的 发表偏倚（publication bias） / 模型漂移（模型 drift） / SE-specificity / 非 SE 证据外推 可作为 Paper2 风险章候选风险清单种子（需研究者确认适用性后采纳）

### 3. 原生样本编码维度树 / 维度森林

**重要说明**：本树**不是样本编码模式**，而是该论文用来组织"LLM-supported SMS 流程设计"的概念骨架。这是降级形态。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 交互式 LLM 支持的系统映射流程模型（interactive LLM-based SMS 流程模型（process model）；Fig. 1 + §2）
│   树类型：概念蓝图（conceptual blueprint）/ 流程模型（process model）
│   样本单位：流程阶段（process_stage），不是原始研究
│   样本数量：不适用
│
├── [B1] 流程阶段分类法（过程 阶段；借自 SMS 指南[4]）
│   ├── [S1] 确立映射研究必要性 (§2.1)
│   ├── [S2] 研究识别
│   │   ├── [S2a] 检索 (§2.2.1)
│   │   └── [S2b] 纳入 / 排除 (§2.2.2)
│   ├── [S3] 数据抽取与分类 (§2.3)
│   │   ├── [S3a] 归纳式编码
│   │   └── [S3b] 演绎式编码
│   ├── [S4] 可视化 (§2.4)
│   └── [S5] 报告撰写 (§2.5)
│
├── [B2] 逐阶段三元组（Fig. 1 通用结构）
│   ├── [L-input] 研究者输入（每阶段都有）
│   ├── [L-refine] 交互式精化 / 人工覆盖
│   └── [L-output] LLM 输出（每阶段都有；稳定 ID 保留）
│
├── [B3] 角色（roles） (S2a search 阶段专有 3-智能体 架构)
│   ├── [A1] 关键词识别智能体（Keyword Identification Agent）
│   ├── [A2] 语义检索智能体（Semantic Search Agent；检索增强生成 + 图数据库）
│   └── [A3] 检索策略智能体（Search Strategy Agent）
│
├── [B4] 技术机制菜单（各阶段可调用的技术组件）
│   ├── 主题建模（topic modeling）：BERTopic (S3a)
│   ├── 提示策略：单样本（one-shot）/ 少样本（few-shot）/ 思维链提示（CoT prompting） (S2b / S3b)
│   ├── 检索增强生成（RAG）+ 文档切分（document splitting） (S3b)
│   ├── 持续学习 / 提示优化组件：持续学习（continual learning）/ DSPy (S2b)
│   ├── 追踪工具（tracing 工具） / LangSmith (§3)
│   ├── WebVoyager（灰色文献（grey literature），§3）
│   └── 可视化工具（visualization tools） / LIDA, ChatGPT 代码（S4)
│
├── [B5] 审计 / 可追踪要求集合 (§2.2.2 + §2.3)
│   ├── 决策标签 (纳入 / 排除 / 不确定（include/exclude/uncertain）)
│   ├── 理由 / 解释
│   ├── 被引用片段 / 引用
│   └── 来源位置
│
├── [B6] 有效性 / 威胁（§3 Reflections）
│   ├── 发表偏倚（发表偏倚（publication bias））
│   ├── LLM 可靠性研究有限（limited studies on LLM reliability）
│   ├── 模型快速演化（rapid 模型演化）/ 服务提供商漂移（provider drift） (Claude.ai, GPT-o1)
│   ├── 非软件工程证据迁移风险（non-SE 证据 transfer risk）
│   └── 需要软件工程特定评价（SE-specific 评价 needed）
│
└── [B7] 研究路线图（Research 路线图；§3 末尾)
    ├── [R1] 改进并评价单个步骤（Improve & evaluate individual steps）
    └── [R2] 构建端到端原型（Build end-to-end prototype）
```

**取值空间类型说明**：

- B1 阶段 分类法：**层级枚举**（5 大阶段 + 2 子阶段），但是借自 [4]，非本文饱和分类。
- B2 triplet：**关系值（字段角色）**，input/refine/output 是固定三槽。
- B3 智能体：**有限枚举**（恰好 3），仅限 search 阶段。
- B4 mechanisms：**开放枚举**，作者只是示例性列举工具名，不是封闭集。
- B5 audit fields：**关系值集合**（decision + 4 个挂件字段），是 Paper2 最有迁移价值的部分。
- B6 威胁：**开放枚举**，作者列了 4–5 项，是 风险清单种子（风险清单种子）。
- B7 路线图：**二值 / 有限枚举**（个体优化 vs 整体原型）。

**未完成 / 需 A2a 精核**：

- Fig. 1 实际包含多少 阶段 box、每个 box 的 input/output 文字是否与 §2 完全一致——必须开 PDF 核对。
- §2.4 / §2.5 较短，是否在 Fig. 1 中也有完整 triplet 槽，文本无法独自确认。
- Supplementary material（DOI 链接下）给出被下划线术语的定义——本轮未打开，叶子语义可能因此残缺。

### 4. 叶子维度表

下表只列**原文确实出现且可作为字段候选**的叶子，不混入跨论文通用接口。证据列直接给 `paper_content.txt` 行号。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 阶段.need | 阶段：建立 map 需求 | B1 | §2.1 | 把研究目标 + 上下文输入给 LLM 得到候选 RQ，由人确认 | 1 个 阶段 | 单值标识 | 阶段缺失 = 路线图 不完整 | 仅 模式种子（schema_seed） | 阶段缺失为 缺口（gap） | 行 81–84 | 可作 阶段 模板，不能写成已验证流程 |
| 阶段.search | 阶段：检索 | B1 | §2.2.1 | 在保持可复现性前提下生成 Boolean 检索式 | 1 个 阶段（内含 3 智能体） | 单值 + 子树 | 同上 | 同上 | 同上 | 行 86–122 | 同上 |
| 阶段.inc_exc | 阶段：纳排 | B1 | §2.2.2 | LLM 给 include/exclude + rationale + citation | 1 个 阶段 | 单值 | 同上 | 同上 | 同上 | 行 136–170 | 同上 |
| 阶段.extract | 阶段：数据抽取与分类 | B1 | §2.3 | 二分为归纳/演绎编码 | 1 个 阶段（内含 2 子模式） | 单值 + 子枚举 | 同上 | 同上 | 同上 | 行 171–199 | 同上 |
| 阶段.vis | 阶段：可视化 | B1 | §2.4 | LLM 生成绘图代码 / 拓扑可视化 | 1 个 阶段 | 单值 | 同上 | 同上 | 同上 | 行 200–206 | 同上 |
| 阶段.报告 | 阶段：报告 | B1 | §2.5 | LLM 在数据表/可视化基础上提示模式与 缺口（gap） | 1 个 阶段 | 单值 | 同上 | 同上 | 同上 | 行 207–211 | 同上 |
| triplet.input | 字段角色：研究者 input | B2 | Fig. 1 + §2 各小节首句 | 用户提供给 LLM 的对象（目标/abstracts/scheme/数据表/RQ） | 自由文本，每阶段类型不同 | 关系值（角色槽） | 缺失 = 自动化越界 | 用于 HITL gate 描述 | 可生成 "哪些阶段 input 最易自动化越界" 的候选发现 | 行 79–211 各 § 首句 | **该结构是本文最强迁移点** |
| triplet.refine | 字段角色：interactive refinement | B2 | Fig. 1 + §2 各小节"We edit ... as input for the next 阶段"等表述 | 用户对 LLM 输出的编辑、覆盖、追问、确认 | 自由文本 | 关系值 | 缺失 = 退化为全自动 | 同上 | 同上 | 行 83–84 等 | 同上 |
| triplet.output | 字段角色：LLM output | B2 | Fig. 1 + §2 各小节"the LLM proposes/suggests/generates ..." | LLM 在该阶段的产物（RQ 候选、智能体 建议、include/exclude、topic 表、图、报告 highlights） | 自由文本，每阶段类型不同 | 关系值 | 缺失 = LLM 未介入该阶段 | 同上 | 同上 | 行 82–211 | 同上 |
| 智能体.keyword | Search-Agent：关键词识别 | B3 | §2.2.1 item 1 | 识别相关术语、同义词、历史术语、概念层级 | 1 个有限 智能体 slot | 单值 | -- | 同上 | -- | 行 101–110 | 仅限 search 阶段 |
| 智能体.semantic | Search-Agent：语义检索 | B3 | §2.2.1 item 2 | RAG + 可选 graph DB；调整检索策略，不直接选文献 | 1 slot | 单值 | -- | 同上 | -- | 行 111–118 | 同上 |
| 智能体.strategy | Search-Agent：检索策略 | B3 | §2.2.1 item 3 | 输出最终可执行 Boolean / DB-specific 查询 | 1 slot | 单值 | -- | 同上 | -- | 行 119–120 | 同上 |
| mech.bertopic | 技术机制：topic modeling | B4 | §2.3 item 1, §2.4 | embeddings → 降维 → 聚类 → topic 表示 | 工具列：BERTopic | 开放枚举 | -- | -- | -- | 行 178–184, 205–206 | 工具名易过时 |
| mech.prompt_style | 技术机制：prompt 形式 | B4 | §2.2.2 + §2.3 item 2 | zero/one/few-shot / CoT / DSPy 优化 | 开放枚举 | 开放枚举 | -- | -- | -- | 行 154, 158–166, 187–188 | 不要绑定具体 prompt 写法 |
| mech.rag | 技术机制：RAG + 文档切分 | B4 | §2.2.1 + §2.3 item 2 | 先 RAG 定位再 prompt LLM | 布尔值 / 配置 | 布尔 + 配置自由文本 | -- | -- | -- | 行 111–117, 188–191 | 同上 |
| mech.continual | 技术机制：持续学习 / DSPy | B4 | §2.2.2 | 从 inc/exc 偏好迭代学习 | 布尔值 + 工具名 | 布尔 + 工具引用 | -- | -- | -- | 行 144–149 | 工具名易过时 |
| mech.trace_tool | 技术机制：tracing 工具 | B4 | §3 Complementary Tools | LangSmith 类工具 | 工具列 | 开放枚举 | -- | -- | -- | 行 224–226 | 同上 |
| mech.web | 技术机制：web 智能体 | B4 | §3 | WebVoyager 用于灰文献 | 工具列 | 开放枚举 | -- | -- | -- | 行 226–229 | 工具名易过时 |
| audit.decision | 审计字段：决策标签 | B5 | §2.2.2 | include / exclude / borderline | 三值枚举 | 有限枚举 | 缺失即不可审 | 用于 trace 覆盖率 seed | 可作 缺口（gap）：哪个阶段 trace 最缺 | 行 150–157 | **强迁移点** |
| audit.rationale | 审计字段：理由 | B5 | §2.2.2 | LLM 给出的解释 / CoT | 自由文本 | 自由文本 | 同上 | 同上 | 同上 | 行 153–155 | CoT 不等于必须暴露推理链，应解读为可审计 rationale |
| audit.citation | 审计字段：引用 | B5 | §2.2.2 | 文本证据片段 + 原文位置 | 关系值（fragment + locator） | 关系值 | 同上 | 同上 | 同上 | 行 155–157 | 强迁移点 |
| audit.source_loc | 审计字段：来源位置 | B5 | §2.2.2 隐含 | 引用所指原文 page / paragraph / line | 关系值 | 关系值 | 同上 | 同上 | 同上 | 行 156–157 | 同上 |
| 威胁.pub_bias | 风险：发表偏倚（publication bias） | B6 | §3 | 现有 LLM-for-review 研究有限且可能有发表偏差 | 风险条目 | 布尔 + 描述 | -- | 用于 risk inventory | risk 候选 | 行 213–217 | 候选使用（需裁决） |
| 威胁.model_drift | 风险：模型快速演化 | B6 | §3 | Claude.ai、GPT-o1 等会让评估过时 | 风险条目 | 同上 | -- | 同上 | 同上 | 行 215–217 | 等价 Paper2 服务提供商漂移（provider drift） |
| 威胁.non_se | 风险：证据外 SE 化 | B6 | §3 | 很多证据来自 SE 之外 | 风险条目 | 同上 | -- | 同上 | 同上 | 行 218–221 | 候选使用（需裁决） |
| 威胁.se_specific | 风险：缺 SE-specific 评价 | B6 | §3 | 需要 SE-specific solution & 评价 | 风险条目 | 同上 | -- | 同上 | 同上 | 行 219–222 | 候选使用（需裁决） |
| 路线图.steps | 路线图条 R1：单步评估 | B7 | §3 末尾 | 分别评估每个 阶段 的策略 | 1 path | 二值 | -- | 候选 next-step | candidate 路线图 | 行 231–232 | 候选使用（需裁决） |
| 路线图.proto | 路线图条 R2：端到端 prototype | B7 | §3 末尾 | 构建覆盖全流程 prototype 收集反馈 | 1 path | 二值 | -- | 同上 | 同上 | 行 232–234 | 候选使用（需裁决） |

### 5. 关系边表

原文虽然不是 ER 模式，但 Fig. 1 + §2 + §2.2.1 / §2.3 存在若干 **显式关系边**，列举如下：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel.stage_to_triplet | 阶段.* | 每阶段包含（each has a） | 三元组.{输入, 精化, 输出} | 角色槽固定 3 个 | 槽缺失 = 该阶段未被建模 | Fig. 1 全图；行 79；行 81–211 各阶段首句 | Paper2 scaffold 字段模板 |
| rel.stage_seq | 阶段.need | 流入下一阶段（feeds into） | 阶段.search → 阶段.inc_exc → 阶段.extract → 阶段.vis → 阶段.报告 | 有序链 | 顺序断裂 = 流程不完整 | 行 64–71 §2 开篇；§2.1 末尾 "as input for the next 阶段" 行 83 | 脚手架阶段顺序 |
| rel.search_to_agent | 阶段.search | 由……组成（composed of） | 智能体.{关键词, 语义检索, 检索策略} | 3 智能体 | 智能体 缺失 = 搜索代理化不完整 | 行 99–122 | 唯一显式 3-智能体 子树 |
| rel.agent_pipe_kw_to_sem | 关键词识别智能体 | 向……提供术语（provides terms to） | 语义检索智能体 | 关系值 | -- | 行 117–118 "Relevant search terms are then extracted again from the selected documents" | citation pearl growing 流程管线 |
| rel.agent_pair_pearl | 智能体.{关键词识别, 语义检索} | 共同支撑（jointly support） | 引文珍珠增长策略（citation pearl growing） | 关系值 | -- | 行 121–122 | 把 pearl growing 作为复合产出 |
| rel.extract_branch | 数据抽取阶段 | 分成两个分支（branches into） | {归纳式编码, 演绎式编码} | 二分 | -- | 行 177–191 | 抽取子模式 |
| rel.inc_exc_to_audit | 纳排阶段输出 | 必须携带（must carry） | 审计字段.{决策, 理由, 引用, 来源位置} | 关系值集合 | 缺失 = 不可审 | 行 150–157 | **追踪强约束**，是 Paper2 最可执行的模式 |
| rel.fulltext_unlock | 自动化水平 | 解锁 | 全文作为抽取输入 | 布尔 | -- | 行 173–176 "go beyond adaptive reading depth ... consider the complete papers as input" | 解读为"自动化越高，输入可越深" |
| rel.threat_to_evaluation | 威胁.{模型漂移, 非软件工程证据, 软件工程特定评价} | 驱动 | 路线图步骤与端到端原型 | 关系值 | -- | 行 213–234 | 风险驱动路线图 |

**总结**：原文存在 **流程顺序、智能体 内部 流程管线、纳排→审计字段挂件、风险→路线图** 四类显式关系边。它不是 ER 模式，但已经足够支撑 Paper2 scaffold 的字段映射，**比"无显式关系边"要强**。

### 6. 统计观察、候选发现 与 最终发现边界

| 类别 | 内容 | 证据 |
|---|---|---|
| **原文自身统计观察** | 无。论文没有任何数字、表格、图表数据点。Fig. 1 是流程图。 | 行 246 数据可获得性（Data 可获得性） |
| **被引文献统计观察（不是本文发现）** | (a) Wang et al. [5]：GPT 生成的 Boolean query 召回更低；PICO 损害召回；refinement 降召回升精度（行 130–135）；(b) Huotala et al. [6]：one-shot / few-shot / few-shot CoT 与人类性能接近；zero-shot 较差；GPT-4 优于 GPT-3.5（行 159–166）；(c) Guo et al. [7]：GPT 善于排除无关，但召回不高（行 167–170）；(d) Petersen [9]：GPT-4 判断 case study 时优于作者（行 197–199） | 行 123–135、158–170、192–199 |
| **原文 discussion / 路线图 候选发现** | (i) HITL 是 LLM-supported SMS 必要前提；(ii) 可复现性需要保留 Boolean search；(iii) inc/exc 必须挂 rationale + citation；(iv) 自动化提升后可用完整 PDF 做 deductive coding；(v) 模型快速演化导致评估易过时；(vi) 需要 SE-specific 评价；(vii) 路线图 双轨：先单步评估再端到端 prototype | 全文综合，主要行 52–55、92–96、150–157、173–176、213–234 |
| **对 Paper2 可迁移的方法学启发** | （a）阶段 × triplet × audit 三层 模式 模板；（b）三 智能体 search 是可重用模式；（c）服务提供商漂移（provider drift） / non-SE transfer / SE-specific 评价 作为 risk inventory；（d）路线图 双轨叙事可借用 | 行 79, 99–122, 213–234 |
| **绝不能迁移的领域结论** | 1. 不可写"已被验证的 LLM-supported SMS 解决方案"；2. 不可写"GPT 在文献综述中可靠"；3. 不可写"首创 interactive LLM-based SMS"（本文 2024/2025 已显式提出该方向）；4. 不可把被引文献 [5–9] 的数字当作本文 发现；5. 不可写本文符合 PRISMA / 提供 复现包 | 行 18–19、行 213–234、行 246 |

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
