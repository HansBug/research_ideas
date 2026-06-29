# llm4se-systematic-review · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是。读取路径：
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是。已覆盖全部 4152 行，包括：
  - Abstract、Introduction（Section 1）
  - Methodology（Section 2）：检索策略（QGS）、纳排标准（Table 3）、质量评估（Table 4, QAC1-10）、数据抽取与分析（Section 2.5, Table 5）
  - RQ1（Section 3）：LLM 分类（encoder-only / encoder-decoder / decoder-only）、Table 6、Fig. 4-5
  - RQ2（Section 4）：数据来源 / 类型 / 预处理 / 输入形式、Table 7-8、Fig. 6-8
  - RQ3（Section 5）：调优技术 / prompt engineering / evaluation metrics、Table 9、Fig. 9-10
  - RQ4（Section 6）：SDLC 六阶段、85 SE 任务、Table 10-12
  - Discussion（Section 7）：key findings summary
  - Threats to Validity（Section 7）：搜索遗漏 / 选择偏倚 / 经验知识偏倚
  - Challenges & Opportunities（Section 8）：roadmap figure
  - Conclusion（Section 9）
  - References、Appendices A-E（Table 13-17）
- **是否核对 `paper.pdf`**：否。未进行逐页视觉核对。原因：本文已通过完整阅读 `paper_content.txt`（4152 行）获取了所有表格编号、图形编号、附录编号、章节结构和关键数值。`review.md` 自身已将 6 项关键证据（EV-llm4se-systematic-review-002/003/005 等）标记为 `needs_manual_check`。本文审计聚焦于维度树结构复原与证据链审计，不依赖 PDF 图表视觉确认。以下涉及表图精确数值的结论均在"全文文本级；图表待人工核对"证据等级下给出，并明确标注。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

**论文**：Hou et al. (2024). "Large Language Models for Software Engineering: A Systematic Literature Review." ACM TOSEM (CCF-A).

**核心目标**：对 LLM4SE 领域进行系统性文献综述（SLR），全面理解 LLM 在 SE 中的应用、效果和局限。

**四个 RQ**：

| RQ | 原文问题 | 核心抽取对象 |
|---|---|---|
| RQ1 | What LLMs have been employed to date to solve SE tasks? | LLM 架构类型（encoder-only / encoder-decoder / decoder-only）、模型家族、参数规模、SE 任务适配性 |
| RQ2 | How are SE-related datasets collected, preprocessed, and used in LLMs? | 数据来源（开源/收集/构造/工业）、数据类型（code/text/graph/repo/combined）、预处理流程、输入形式（token/tree-graph/pixel/hybrid） |
| RQ3 | What techniques are used to optimize and evaluate the performance of LLMs in SE? | 调优技术（全量微调/ICL/PEFT 四子类/RL/SFT）、prompt engineering（八类）、评价指标（按 generation/classification/recommendation/regression 分类） |
| RQ4 | What SE tasks have been effectively addressed to date using LLM4SE? | SDLC 六阶段（requirements/design/development/QA/maintenance/management）、85 个具体 SE 任务、问题类型（generation/classification/recommendation/regression） |

**贡献声明**（原文 Conclusion 提炼）：
1. 首个覆盖 LLM4SE 全领域的系统性综述（395 篇论文，2017-2024）
2. 提供按 LLM 架构 / 数据 / 优化与评价 / SE 任务四维度的分类体系
3. 总结关键挑战与提供研究路线图
4. 公开 replication package

### 2.2 原文方法流程

**检索**：Quasi-Gold Standard（QGS）策略。
- **Manual search**：在 6 个顶级 SE venue（ICSE、ESEC/FSE、ASE、ISSTA、TOSEM、TSE）中手动搜索，确认 51 篇 QGS 论文
- **Search string derivation**：从 QGS 和领域知识构造两组关键词（SE task keywords + LLM keywords）
- **Automated search**：在 7 个数据库（IEEE Xplore、ACM DL、ScienceDirect、WoS、Springer、arXiv、DBLP）检索，初始 218,765 条

**纳排**：
- **Inclusion criteria**（Table 3）：3 条——使用 LLM、涉及 SE 任务、全文可获取
- **Exclusion criteria**（Table 3）：9 条——<8 页、重复、非同行评审出版形式、工具 demo/editorial、workshop/doctoral symposium、灰色文献、非英语、只提 LLM 不描述技术、SE 方法增强 LLM 而非 LLM 用于 SE
- **六阶段筛选**（Fig. 1）：页数过滤 → 题名/摘要/关键词筛选 → venue 识别 → 去重 → 全文审阅 → 质量评估

**质量评估**：
- **QAC**（Table 4）：10 条质量评估标准（QAC1-QAC10），每条 0-3 分。已发表论文总分 21，阈值 16.8（80%）；arXiv 论文 QAC4=0，总分 18，阈值 14.4
- 382 篇通过质量评估

**Snowballing**：对 382 篇做 forward + backward snowballing，补充 13 篇，最终 395 篇。

**数据抽取**：Table 5 定义了明确的 extraction form，包含 8 个数据项，映射到 4 个 RQ。

**数据抽取项（Table 5）**：
| 数据项 | 对应 RQ |
|---|---|
| The category of SE task | 1,2,3,4 |
| The category of LLM | 1,2,3,4 |
| Characteristics and applicability of LLMs | 1,4 |
| The adopted data handling techniques | 2 |
| The adopted weight training algorithms and optimizer | 3 |
| The selected evaluation metrics | 3 |
| The SE activity to which the SE task belongs | 4 |
| The developed strategies and solutions | 4 |

**编码 / 分类 schema**（原文显式定义，非推导）：
1. **LLM 架构分类**（Section 3.1, Fig. 4）：encoder-only / encoder-decoder / decoder-only；在每个大类下列出具体模型家族
2. **数据来源分类**（Section 4.1）：open-source / collected / constructed / industrial
3. **数据类型分类**（Section 4.2, Table 7）：code-based / text-based / graph-based / software repository-based / combined
4. **数据预处理分类**（Section 4.3, Fig. 7-8）：data extraction → unqualified data deletion → duplicated instance deletion → data segmentation（及各自的子步骤）
5. **输入形式分类**（Section 4.4, Table 8）：token-based / tree/graph-based / pixel-based / hybrid
6. **调优技术分类**（Section 5.1）：full fine-tuning / ICL / LoRA / prompt tuning / prefix tuning / adapter tuning / RL / SFT / 其他
7. **Prompt engineering 分类**（Section 5.2, Fig. 9）：Few-shot / Zero-shot / CoT / Automatic CoT / Chain of Code / Modular-of-Thought / Structured CoT / Automatic Prompt Engineer / Others
8. **评价指标分类**（Section 5.3, Table 9）：按 generation / classification / recommendation / regression 四类任务分别列出
9. **SE 任务分类**（Section 6, Fig. 10, Table 10）：SDLC 六阶段 × 85 任务 × 4 问题类型（generation / classification / recommendation / regression）

**Finding 形成方式**：
- 每个 RQ 的分析结尾都有 "RQ-N - Summary" 框，列出 2-4 条关键发现
- Section 7 为 Discussion，整合跨 RQ 观察
- Section 8 为 Challenges & Opportunities，提出路线图
- 文中大量使用 Fig./Table 展示统计分布和计数，从分布中形成趋势/差距/机会判断

### 2.3 原文显式 artifact / evidence 结构

| 证据类型 | 位置 | 内容 |
|---|---|---|
| **Extraction form** | Table 5 | 8 个数据项，RQ 映射 |
| **QAC rubric** | Table 4 | 10 条评分标准，3 级评分 |
| **纳排标准** | Table 3 | 3 inclusion + 9 exclusion |
| **LLM 分类 taxonomy** | Fig. 4, Table 6 | 三类架构 + 模型分布 |
| **数据分类 schema** | Table 7, Table 8, Fig. 6-8 | 四类来源 / 五类类型 / 预处理流程 / 四类输入形式 |
| **优化/评价分类** | Table 9, Fig. 9-10 | 调优 + prompt engineering + metrics |
| **SE 任务分类** | Table 10, Fig. 10 | 六阶段 × 85 任务 × 问题类型 |
| **统计图** | Fig. 2, 4-10 | 分布柱状图 |
| **SOTA 应用表** | Table 11 (code generation), Table 12 (program repair) | 模型 vs baseline vs benchmark vs metric |
| **全文附录** | Appendices A-E (Table 13-17) | 完整论文引用映射表 |
| **Replication package** | GitHub repo | 模型参数、论文列表、LLM-SE 任务映射 |
| **Threats to validity** | Section 7 | 搜索遗漏 / 选择偏倚 / 经验知识偏倚 |
| **Challenges & Opportunities** | Section 8 | 7 类挑战 + 5 类机遇 + roadmap |
| **Key findings summary** | 每个 RQ 结尾 + Section 7 | 带编号的 finding 陈述 |

### 2.4 原文如何从字段/统计观察形成 conclusion / finding / gap / recommendation

1. **RQ 级 finding**：每个 RQ 分析完成后，以 "RQ-N - Summary" 框列出关键统计发现（例如：开源数据集占 62.83%、decoder-only 模型占 195/395 篇等），然后提炼为趋势判断
2. **跨 RQ 整合**：Section 7 Discussion 将四个 RQ 的 finding 串联为领域现状与趋势
3. **挑战提取**：Section 8.1 从领域统计数据中识别 7 类结构化挑战（LLM 适用性 / 泛化性 / 评估 / 可解释性与信任 / 等）
4. **机遇/路线图**：Section 8.2 基于挑战和趋势提出 5 类未来方向，形成 roadmap
5. **结论**：Section 9 总结四个 RQ 的主要回答 + 挑战 + 路线图

## 3. 当前 `review.md` 维度树审计

当前 `review.md` 的 A.2 维度树结构如下：

```
[dim-llm4se-systematic-review-root]
├── [dim-llm4se-systematic-review-taxonomy]  (主题 / 分类 — A1-M2)
├── [dim-llm4se-systematic-review-method]    (方法 / 技术 — A1-M3)
├── [dim-llm4se-systematic-review-evidence]  (评价 / 证据 — A1-M4)
└── [dim-llm4se-systematic-review-finding]   (统计观察与候选发现 — A1-M6)
```

以及底层叶子：
```
[leaf-llm4se-systematic-review-orig-se-task]
[leaf-llm4se-systematic-review-orig-llm-method]
[leaf-llm4se-systematic-review-orig-dataset-benchmark]
[leaf-llm4se-systematic-review-orig-metric]
[leaf-llm4se-systematic-review-orig-limitation-risk]
```

### 3.1 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但过于泛化 | 根节点 `[dim-llm4se-systematic-review-root]` 未体现本文是"SLR on LLM4SE with extraction form + taxonomy + classification schema + roadmap"，更像占位符。根节点摘要中说"把 LLM4SE 拆成四个 RQ"，这个定位正确。 | M |
| 主干分支是否覆盖原文 schema | **否，严重不足** | 当前主干只有 4 个分支（taxonomy / method / evidence / finding），实质上是把 A1-M0--M6 的通用 6 层元维度中的 4 层直接映射到本文。原文实际具有的维度结构远远超过这 4 个通用接口：缺少 RQ 结构（4 RQ 各有独立维度子空间）、缺少检索纳排维度（search strategy / QGS / inclusion-exclusion / QAC / snowballing / venue distribution）、缺少 LLM 分类维度（architecture → model family → parameter size → task fit）、缺少数据维度（source → type → preprocessing → input form 四层嵌套）、缺少优化评价维度（tuning 子类 / prompt engineering 八类 / metrics 按任务类型）、缺少 SE 任务维度（SDLC activity → task → problem type 三层嵌套）、缺少效度威胁维度（3 类 threat）、缺少挑战与路线图维度（Challenges & Opportunities section）、缺少制品维度（5 Appendices + GitHub replication package）。当前树将上述全部压缩到 4 个通用桶中，只有 5 个候选叶子做了映射但没有展开为完整子树。 | C |
| 叶子维度是否足够具体 | **否，过于粗粒度** | 5 个候选叶子 `[leaf-llm4se-systematic-review-orig-*]` 虽标记为"A1 种子"，但：(1) 这 5 个叶子覆盖了原文可能的叶子总数不到 20%（原文至少有 25+ 个可操作化叶子）；(2) 叶子没有展开原文的层级嵌套结构（如 LLM → architecture → model family → parameter size 三个层次被压平为一个"LLM method"叶子）；(3) SE 任务维度（SDLC 六阶段 × 85 任务 × 4 问题类型）被简化为一个"SE task"叶子。 | C |
| 取值空间是否可执行 | **否，当前不可执行** | A.2 证据账本中 EV-llm4se-systematic-review-002/003 对叶子取值的描述是"解码器专用架构、Codex 类模型、代码生成任务等""文本型数据集、代码型数据集、开源代码数据集等""Accuracy / F1 / BLEU / EM 等"，但这些：(1) 并非原文分类体系的完整枚举；(2) 未区分取值空间的层级嵌套结构（如 encoder-only / encoder-decoder / decoder-only 是顶层，其下还有具体模型家族）；(3) 未给出操作化可填值的边界（如"等"字无法判断是否闭合）。 | C |
| 关系边是否缺失 | **是，大量缺失** | 当前仅有 2 条关系边：`[edge-llm4se-systematic-review-method-evidence]`（方法→证据）和 `[edge-llm4se-systematic-review-taxonomy-finding]`（分类→发现）。原文至少遗漏以下关键关系：RQ ↔ 数据抽取项（Table 5 显式映射）、数据抽取项 ↔ 分类 schema（每个字段对应一个分类体系）、分类 schema ↔ 统计分布（Fig./Table 中的频次统计）、统计分布 ↔ finding（RQ Summary 框中的关键发现）、finding ↔ 挑战（Section 8 从 finding 到 challenge 的推演）、LLM 架构 ↔ SE 任务适配（Table 6）、数据来源 ↔ 数据类型（多层交叉）。此外，缺失关系边意味着 A2a 无法判断哪些叶子可以交叉制表。 | C |
| 统计用途 / 分母是否正确 | **是，当前 review.md 中统计字段基本空缺** | A.2 证据账本中虽然标注了"分母：395 篇"，但没有按原文 RQ/分类建立可统计的叶子维度。例如：根据 Table 5 的 extraction form，原文对每个纳入论文抽取 8 个字段；这些字段在 review.md 中没有被建模为可统计叶子。当前 review.md 没有给出任何统计结论（因为 A1-DT 阶段不允许 `statistical_synthesis`），这在阶段纪律上是正确的。问题不在于统计本身，而在于维度树没有为 A2a 统计准备好可执行的叶子。 | M |
| 候选 finding 路径是否完整 | **否，当前仅做了框架性标注** | A.3 结论-证据映射中 12 条结论（C01-C12）基本上都是方法论迁移层面的结论（如"本文的 RQ/方法/分类/评价/讨论结构可作为 Paper2 维度树候选节点"），而不是从原文 finding 到 candidate finding 的忠实复原。原文明确有：(1) 每个 RQ 的 "RQ-N - Summary" 框中 2-4 条统计发现；(2) Section 7 Discussion 中的跨 RQ 整合发现；(3) Section 8 中的 11 条挑战陈述 + 5 类机遇。这些 finding 需要被标记为候选发现并关联到具体叶子维度，当前完全缺失。 | C |
| A.1--A.4 证据链是否足够 | **框架存在但证据不够** | A.1 有 6 条来源标识；A.2 有 6 条证据但 3 条（EV-002/003/005）标记为 `needs_manual_check` 且都是 `weak` 强度；A.3 有 12 条结论但全部标记为 `weak` 强度且全部只允许 `schema_seed` 或 `candidate_finding`；A.4 有 1 条结构检查通过和 1 条待人工核对。框架合规，但证据锚定太弱——所有 EV 都是"Section 2--6"级别的泛定位，没有具体到表号/图号/页码/段落。对于一篇有 17 个正式表格、10 个图、5 个附录的 79 页论文来说，证据锚定精度不够。 | I |
| 是否存在可能误导 A2a 的强主张 | **是** | (1) A.3 中 C05-C07 说"叶子维度来自本文的 RQ/方法/分类/评价/讨论结构，可作为 Paper2 维度树候选节点"——但当前叶子仅有 5 个泛化候选（orig-se-task / orig-llm-method / orig-dataset-benchmark / orig-metric / orig-limitation-risk），远不足以代表原文结构。若 A2a 直接以当前 5 个叶子为起点，会丢失原文 80% 以上的维度信息。(2) C12 说"本文已把原文抽取字段、分类项、模型节点或报告叶子列为'原文模式候选叶子映射（A1 种子）'"——这个说法暗示叶子映射已完成，但实际上只是用一个通用范式套了 5 个名称，没有忠实复原原文分类体系。这可能导致 A2a 误认为维度树工作已完成大部分。 | I |

## 4. 建议维度树骨架

以下是更忠实于原文结构的维度树。所有节点均能追溯到原文的具体 section/table/figure。候选取值空间和缺失值语义按 `pattern-field-schema.md` 合同给出。

### 4.1 维度树根节点

```
[dim-llm4se-slr-root]  — Hou et al. (2024) LLM4SE SLR 维度树
│  原文定位：全文，TOSEM 2024, 79 pages, 395 primary studies
│  统计分母：395 篇（quality-assessed: 382 + snowballing: 13）
│  证据等级：全文文本级；图表待人工核对
```

### 4.2 主干分支

**Branch 1: 研究设计维度（Methodology Schema）**

```
[dim-slr-methodology]
├── [leaf-search-strategy]
│   │  取值空间：{QGS, manual_search_in_6_venues, automated_search_in_7_databases}
│   │  原文定位：Section 2.2, Table 2
│   │  可统计：否（描述性）
│   │  缺失语义：not_applicable（单篇 SLR 描述自身方法）
│   │  证据来源：Section 2.2, para 1-3
│   │
├── [leaf-inclusion-criteria]
│   │  取值空间：{use_LLM, involve_SE_task, full_text_accessible}
│   │  原文定位：Table 3 (Inclusion criteria)
│   │  可统计：否
│   │
├── [leaf-exclusion-criteria]
│   │  取值空间：{less_than_8_pages, duplicate, non_peer_reviewed_venue, tool_demo_editorial,
│   │             workshop_doctoral_symposium, grey_literature, non_English, LLM_mention_without_technique,
│   │             SE_method_to_enhance_LLM}
│   │  原文定位：Table 3 (Exclusion criteria)
│   │  可统计：否
│   │
├── [leaf-quality-assessment-criteria]
│   │  取值空间：QAC1--QAC10（每条 0-3 分）
│   │  原文定位：Table 4
│   │  可统计：否（描述 QAC 框架）
│   │
├── [leaf-quality-assessment-threshold]
│   │  取值空间：{published_≥16.8_of_21, arXiv_≥14.4_of_18}
│   │  原文定位：Section 2.3.2
│   │  可统计：否
│   │
├── [leaf-screening-stages]
│   │  取值空间：{filter_less_than_8_pages, title_abstract_keyword_screening, venue_identification,
│   │             deduplication, full_text_review, quality_assessment}
│   │  原文定位：Fig. 1, Section 2.3
│   │  可统计：否（可记录各阶段论文数：218,765→80,611→5,078→4,341→1,172→810→594→382+13）
│   │
├── [leaf-extraction-form]
│   │  取值空间：{category_of_SE_task, category_of_LLM, characteristics_applicability_LLMs,
│   │             data_handling_techniques, weight_training_algorithms_optimizer,
│   │             evaluation_metrics, SE_activity, developed_strategies_solutions}
│   │  原文定位：Table 5
│   │  可统计：是（这些字段的取值频次就是原文 RQ1-4 的主要内容）
│   │
├── [leaf-rq-mapping]
│   │  取值空间：{RQ1: LLMs employed, RQ2: data collection/preprocessing/usage,
│   │             RQ3: optimization/evaluation, RQ4: SE tasks addressed}
│   │  原文定位：Section 2.1
│   │  可统计：否（结构描述）
```

**Branch 2: RQ1 — LLM 分类维度（LLM Taxonomy）**

```
[dim-rq1-llm-taxonomy]
├── [leaf-llm-architecture]
│   │  取值空间：{encoder-only, encoder-decoder, decoder-only}
│   │  原文定位：Section 3.1, Fig. 4
│   │  可统计：是（分母：395；encoder-only ~50 篇 BERT 系，decoder-only 195 篇
│   │          含 "over 45 LLMs"）
│   │  缺失语义：not_reported（部分论文未声明模型架构）
│   │
├── [leaf-llm-model-family]
│   │  取值空间：{BERT_variants, CodeBERT, GraphCodeBERT, RoBERTa, ALBERT, PLBART, T5, CodeT5,
│   │             GPT_series, Codex, CodeGen, LLaMA, StarCoder, InCoder, ChatGPT, ... (45+ models)}
│   │  原文定位：Section 3.1, Fig. 4, Table 6
│   │  可统计：是（分母：395）
│   │
├── [leaf-llm-parameter-size]
│   │  取值空间：{<1B, 1B-10B, 10B-100B, >100B, not_reported}
│   │  原文定位：Section 3.1（GitHub repo 中有完整记录）
│   │  可统计：是
│   │  缺失语义：not_reported（论文未声明参数规模）
│   │
├── [leaf-llm-task-fit]
│   │  取值空间：{understanding_tasks, generation_tasks, understanding_and_generation_tasks}
│   │  原文定位：Table 6
│   │  可统计：是（交叉表：架构 × SE 任务适配）
│   │
├── [leaf-llm-temporal-trend]
│   │  取值空间：{year → architecture_count} 时间序列
│   │  原文定位：Fig. 5
│   │  可统计：是
│   │  缺失语义：not_applicable_for_single_year_papers
```

**Branch 3: RQ2 — 数据维度（Data Schema）**

```
[dim-rq2-data]
├── [leaf-data-source]
│   │  取值空间：{open-source, collected, constructed, industrial}
│   │  原文定位：Section 4.1, Fig. 6
│   │  可统计：是（分母：374 篇明确声明数据集的论文；open-source: ~235 篇, ~62.83%）
│   │  缺失语义：not_reported（论文未声明数据来源）
│   │
├── [leaf-data-type]
│   │  取值空间：{code-based, text-based, graph-based, software-repository-based, combined}
│   │  原文定位：Section 4.2, Table 7
│   │  可统计：是
│   │  缺失语义：not_reported
│   │
├── [leaf-data-preprocessing]
│   │  取值空间：{data_extraction, unqualified_data_deletion, duplicated_instance_deletion,
│   │             data_segmentation, text_specific_steps(*), code_specific_steps(*)}
│   │  (*) text-specific: noise removal, stop word removal, normalization, tokenization（Fig. 7）
│   │  (*) code-specific: data extraction, filtering, AST parsing, data segmentation,
│   │                      sub-tokenization, AST-based transformation, data formatting（Fig. 8）
│   │  原文定位：Section 4.3, Fig. 7-8
│   │  可统计：是（频次）
│   │
├── [leaf-input-form]
│   │  取值空间：{token-based, tree-graph-based, pixel-based, hybrid}
│   │  原文定位：Section 4.4, Table 8
│   │  可统计：是（分母：355 篇明确声明输入形式的论文）
│   │  缺失语义：not_reported
```

**Branch 4: RQ3 — 优化与评价维度（Optimization & Evaluation Schema）**

```
[dim-rq3-optimization-evaluation]
├── [leaf-tuning-technique]
│   │  取值空间：{full_fine_tuning, ICL, LoRA, prompt_tuning, prefix_tuning, adapter_tuning,
│   │             RL, SFT, syntax_fine_tuning, knowledge_preservation_fine_tuning,
│   │             task_oriented_fine_tuning, not_applicable}
│   │  原文定位：Section 5.1
│   │  可统计：是（分母：83 篇使用微调；8 LoRA + 3 prompt tuning + 2 prefix tuning
│   │          + 2 adapter tuning + RL/SFT/其他）
│   │  缺失语义：not_applicable（论文仅使用 zero-shot/few-shot 无训练）
│   │
├── [leaf-prompt-engineering]
│   │  取值空间：{few_shot, zero_shot, CoT, Automatic_CoT, Chain_of_Code,
│   │             Modular_of_Thought, Structured_CoT, Automatic_Prompt_Engineer, Others}
│   │  原文定位：Section 5.2, Fig. 9
│   │  可统计：是（分母：395；few-shot 88 篇, zero-shot 79 篇, CoT 22 篇, ...）
│   │
├── [leaf-evaluation-metric]
│   │  取值空间：{generation_metrics: {BLEU, EM, CodeBLEU, ROUGE, METEOR, ...},
│   │             classification_metrics: {Accuracy, Precision, Recall, F1, AUC, ...},
│   │             recommendation_metrics: {MRR, MAP, Top-K_Accuracy, ...},
│   │             regression_metrics: {MAE, MRE, MMRE, ...}}
│   │  原文定位：Section 5.3, Table 9
│   │  可统计：是（交叉表：指标类 × SE 任务）
│   │
├── [leaf-problem-type]
│   │  取值空间：{generation, classification, recommendation, regression}
│   │  原文定位：Section 5.3, Fig. 10(b)
│   │  可统计：是（分母：395；generation ~46% 即 ~182 篇, ...）
```

**Branch 5: RQ4 — SE 任务维度（SE Task Taxonomy）**

```
[dim-rq4-se-task]
├── [leaf-sdlc-activity]
│   │  取值空间：{requirements, software_design, software_development,
│   │             software_quality_assurance, software_maintenance, software_management}
│   │  原文定位：Section 6, Fig. 10(a), Table 10
│   │  可统计：是（分母：395）
│   │
├── [leaf-se-task]
│   │  取值空间：85 个 SE 任务名（如 code_generation: 118, program_repair: 35,
│   │            code_completion: 22, code_summarization: 21, vulnerability_detection: 18,
│   │            test_generation: 17, code_translation: 12, code_search: 12, ...）
│   │  原文定位：Section 6, Table 10, Table 17 (Appendix E)
│   │  可统计：是（分母：395）
│   │  缺失语义：not_applicable（论文归类到单一 SE 任务）
│   │
├── [leaf-se-task-problem-type]
│   │  取值空间：{generation, classification, recommendation, regression}
│   │  原文定位：Section 6, Fig. 10(b)
│   │  可统计：是（交叉表：SE 任务 × 问题类型）
```

**Branch 6: 证据呈现与制品维度（Evidence & Artifact Schema）**

```
[dim-evidence-artifact]
├── [leaf-table-inventory]
│   │  取值空间：按用途分类 {methodology_table, result_table, summary_table, appendix_table}
│   │  原文定位：全文 Table 1-17
│   │  可统计：否（描述性）
│   │
├── [leaf-figure-inventory]
│   │  取值空间：{Fig_1_screening_flow, Fig_2_paper_distribution, Fig_3_wordcloud,
│   │             Fig_4_LLM_distribution, Fig_5_temporal_trend, Fig_6_data_collection,
│   │             Fig_7_text_preprocessing, Fig_8_code_preprocessing, Fig_9_prompt_engineering,
│   │             Fig_10_SE_activities_problem_types}
│   │  原文定位：全文 Fig. 1-10
│   │  可统计：否（描述性）
│   │
├── [leaf-appendix-inventory]
│   │  取值空间：{Appendix_A_LLM_table, Appendix_B_input_forms_table,
│   │             Appendix_C_prompt_engineering_table, Appendix_D_evaluation_metrics_table,
│   │             Appendix_E_SE_tasks_table}
│   │  原文定位：Table 13-17
│   │  可统计：否（描述性）
│   │
├── [leaf-replication-package]
│   │  取值空间：{GitHub_repo, model_parameters, paper_list, LLM-SE_task_mapping}
│   │  原文定位：Section 2.5, GitHub URL
│   │  可统计：否
│   │  缺失语义：not_verified（需 A2a 核对 repo 内容完整性）
```

**Branch 7: 效度威胁维度（Validity Threats Schema）**

```
[dim-validity-threats]
├── [leaf-paper-search-omission]
│   │  取值空间：{mitigated_by: QGS_manual_automated_snowballing}
│   │  原文定位：Section 7, para 1
│   │  可统计：否
│   │
├── [leaf-study-selection-bias]
│   │  取值空间：{mitigated_by: two_reviewers_secondary_review, replication_package}
│   │  原文定位：Section 7, para 2
│   │  可统计：否
│   │
├── [leaf-empirical-knowledge-bias]
│   │  取值空间：{mitigated_by: RQ_reference_to_DL4SE_survey, predefined_categories_from_prior_work}
│   │  原文定位：Section 7, para 3
│   │  可统计：否
```

**Branch 8: Challenges & Opportunities（路线图维度）**

```
[dim-challenges-opportunities]
├── [leaf-challenge-category]
│   │  取值空间：{LLM_applicability/model_size_deployment, LLM_applicability/data_dependency,
│   │             LLM_applicability/ambiguity_in_code_generation,
│   │             LLM_generalizability,
│   │             LLM_evaluation/metric_limitations,
│   │             LLM_interpretability_trustworthiness_ethics,
│   │             emerging_challenges/multimodal_LLM4SE,
│   │             ...}
│   │  原文定位：Section 8.1
│   │  可统计：否（descriptive taxonomy）
│   │
├── [leaf-opportunity-category]
│   │  取值空间：{optimization_of_LLM4SE/code_specialized_LLMs,
│   │             optimization_of_LLM4SE/ChatGPT_influence,
│   │             optimization_of_LLM4SE/task_specific_training,
│   │             LLM4SE_frameworks_and_benchmarks,
│   │             predictive_analytics_and_decision_support,
│   │             LLMs_in_software_security,
│   │             SE4LLM}
│   │  原文定位：Section 8.2
│   │  可统计：否（roadmap taxonomy）
```

### 4.3 关系边

以下关系边忠实于原文的显式结构：

| 关系边 ID | 源 | 目标 | 关系类型 | 原文证据 |
|---|---|---|---|---|
| `[edge-rq-extraction]` | RQ1-RQ4 | Table 5 数据抽取项 | 映射 | Table 5 显式列 "RQ Data Item" |
| `[edge-extraction-category]` | Table 5 字段 | 各分类 schema | 实例化 | Section 2.5 描述数据抽取后如何归类 |
| `[edge-category-stat]` | 分类 schema 叶子 | Fig./Table 统计数字 | 计数 | 每个 Section 的 Fig./Table |
| `[edge-stat-finding]` | 统计分布 | RQ-Summary finding | 支撑 | 每个 RQ 结尾的 "RQ-N - Summary" |
| `[edge-finding-challenge]` | RQ finding | Section 8.1 Challenge | 推演 | Section 8 从统计观察推导挑战 |
| `[edge-challenge-opportunity]` | Section 8.1 Challenge | Section 8.2 Opportunity | 对应 | Section 8 结构 |
| `[edge-llm-architecture-task-fit]` | LLM 架构叶子 | SE 任务叶子 | 适配关系 | Table 6 |
| `[edge-data-source-type]` | 数据来源叶子 | 数据类型叶子 | 属于 | Section 4 文本描述 |
| `[edge-metric-problem-type]` | 评价指标叶子 | 问题类型叶子 | 度量 | Table 9 |
| `[edge-methodology-threat]` | 检索/纳排/QAC 叶子 | 效度威胁叶子 | 偏倚控制 | Section 7 |

### 4.4 与当前 review.md 维度树的差距总结

| 差距维度 | 当前 review.md | 建议维度树 | 覆盖差距 |
|---|---|---|---|
| 主干分支数 | 4 | 8 | 缺少 methodology / RQ1-LLM / RQ2-data / RQ3-optim-eval / RQ4-SE-task / evidence-artifact / validity / challenges 中的 4 个独立分支 |
| 叶子节点数 | 5（5 个候选叶子） | 25+ | 原文可操作化字段至少 25 个以上 |
| 取值空间 | 非正式枚举（"等"） | 完整枚举（原文分类体系直译） | 丢失了所有分类 schema 的细粒度层级 |
| 关系边 | 2 | 10 | 缺失了 RQ↔extraction↔category↔stat↔finding↔challenge 链条的关键关系 |
| 统计分母 | 仅统一分母 395 | 按 RQ/子问题分层分母 | 原文不同子问题使用不同有效分母（如数据来源 / 输入形式分析只覆盖明确声明的论文子集） |
| 缺失值语义 | 未明确 | 按 not_reported / not_applicable / not_verified 分层 | 原文在多个计数场景下区分"未声明"与"不适用" |
| RQ 级 finding 复原 | 12 条结论全为方法论迁移 | 8+ 条原文 finding 可独立标记 | 原文 4 个 RQ-Summary 框的统计发现未进入 A.3 |
| 效度威胁复原 | 无 | 3 类 threat 结构 | 完全缺失 |
| 制品 / 附录复原 | 无 | Tables 1-17, Figs 1-10, Appendices A-E | 完全缺失 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将 4 个通用分支扩展为 8 个原文忠实分支 | `review.md` A.2 维度树节点表 | 增加 `[dim-slr-methodology]`、`[dim-rq1-llm-taxonomy]`、`[dim-rq2-data]`、`[dim-rq3-optimization-evaluation]`、`[dim-rq4-se-task]`、`[dim-evidence-artifact]`、`[dim-validity-threats]`、`[dim-challenges-opportunities]` 八个分支，保持与现有 A1-M0--M6 元维度标注的映射关系。 | Section 2-8, Tables 2-12, Figs 1-10 | C |
| 将 5 个候选叶子扩展为 25+ 个原文忠实叶子 | `review.md` A.2 维度树叶子和取值空间表 | 按本报告 §4.2 中建议的完整叶子列表，为每个叶子填写取值空间（完整枚举，不用"等"）、原文定位（精确到 section/table/figure/paragraph）、可统计性、缺失值语义。将现有 5 个叶子降级为"early-seed"并标注覆盖度。 | Section 2.5 Table 5, Section 3-6, Tables 6-10, Figs 4-10 | C |
| 补充原文 8 条 RQ 级 finding 到 A.3 | `review.md` A.3 结论-证据映射表 | 为原文"RQ-1 - Summary"至"RQ-4 - Summary"中的每条统计发现（至少 8 条，见 §2.1 各 RQ 的 Summary 框）创建 `[clm-llm4se-systematic-review-finding-rq*]` 条目，关联到 A.2 对应叶子证据。 | Section 3-6 各 RQ 结尾的 "RQ-N - Summary" 框 | C |
| 补充原文效度威胁与挑战/路线图到 A.3 | `review.md` A.3 结论-证据映射表 | 为 Section 7 的 3 类效度威胁、Section 8.1 的 7+ 类挑战、Section 8.2 的 5+ 类机遇创建 `[clm-*]` 条目，并分别链到 A.2 的证据。当前 A.3 完全缺失这些内容。 | Section 7, Section 8 | C |
| 补充 10+ 条关系边 | `review.md` A.2 关系边表 | 按本报告 §4.3 中建议的关系边列表，增加 RQ↔extraction↔category↔stat↔finding↔challenge 链条的边 | Table 5 显式映射, Section 3-8 分析过程 | C |
| 将 A.2 证据锚定从泛定位升级为精确表/图/段 | `review.md` A.2 证据账本 | EV-002/003/005 将原文定位从 "Section 2--6" 升级为具体的表号（Table 5 数据抽取项、Table 4 QAC、Table 6 LLM 分类、Table 7 数据类型、Table 8 输入形式、Table 9 评价指标、Table 10/17 SE 任务、Fig. 4/6/7/8/9/10 分布图）、页码（Page 8-38）和段落号 | Section 3-6, Tables 6-10, Figs 4-10 | I |
| 补充原文制品/附录维度 | `review.md` A.2 维度树节点表 | 增加 `[dim-evidence-artifact]` 分支，覆盖全文 17 个正式表格、10 个图、5 个附录、GitHub replication package | Table 1-17, Figs 1-10, Appendices A-E, Section 2.5 GitHub URL | M |
| 保留现有 C12（原文模式候选叶子映射）但补充说明 | `review.md` A.3 C12 | 在 C12 的备注中增加："当前 5 个候选叶子为 A1 初步种子，覆盖原文叶子全集不足 20%。A2a 需按本报告 §4.2 建议维度树补全至 25+ 叶子和完整取值空间后方可进入正式统计。" | A.3 C12 自身 + 本报告 §3, §4 | I |
| 更新 A.4 复验清单 | `review.md` A.4 | 增加一条检查："A2a 前置验证：确认维度树分支 ≥ 8，叶子 ≥ 25，关系边 ≥ 10，A.3 RQ 级 finding ≥ 8 条，效度威胁/挑战/路线图结论存在" | 本报告 §4.2-4.4 | I |

## 6. C/I/M 结论

### C（Critical）— 直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

1. **维度树主干覆盖严重不足**（对照 §3 检查项"主干分支是否覆盖原文 schema"）：当前 4 个通用分支（taxonomy / method / evidence / finding）只反映了 A1-M0--M6 元维度的 4 层，没有从原文真实结构（4 RQ × 各自的分类轴 + methodology + validity + challenges/roadmap + artifacts）中复原。若 A2a 直接以当前树为起点进行统计合成，将丢失原文 80% 以上的可操作化维度信息。**影响**：Paper2 的"从已有 SE SLR/SMS 中抽取维度模式"这一核心目标在本文上将基本落空。

2. **叶子维度过粗，取值空间不可执行**（对照 §3 检查项"叶子维度是否足够具体"和"取值空间是否可执行"）：原文有 25+ 个可操作化字段，但当前仅有 5 个候选叶子，且取值空间用"等"字未闭合。**影响**：A2a 无法基于当前维度树进行任何有意义的字段级频次统计、交叉表或维度饱和度判断。

3. **原文 RQ 级 finding 完全未进入 A.3 候选发现表**（对照 §3 检查项"候选 finding 路径是否完整"）：原文 4 个 RQ 各有 2-4 条明确统计发现（RQ Summary 框），Section 7 Discussion 有跨 RQ 整合发现，但 A.3 的 12 条结论全部是方法学迁移层面的框架性陈述。**影响**：后续 "从脚手架 finding 到 candidate finding 到 final finding" 的链条在本文上断裂，因为原文的真实 finding 根本没有被标记和链入证据。

4. **关系边极度稀疏**（对照 §3 检查项"关系边是否缺失"）：当前仅有 2 条模糊的关系边，而原文至少显式存在 RQ↔extraction form、extraction↔category schema、category↔statistical count、statistical count↔finding、finding↔challenge 等多条运行关系。**影响**：A2a 无法判断哪些叶子可交叉制表，哪些叶子只是分类轴。

### I（Important）— 会实质影响维度树可用性、原文 schema 复原、证据可审计性

1. **A.2 证据锚定精度不足**（对照 §3 检查项"A.1--A.4 证据链是否足够"）：所有 EV 的原文定位都是 "Section 2--6" 级别的泛定位。论文有 79 页、17 个正式表格、10 个图、5 个附录，但没有任何一条证据精确到表号/图号/页码。A2a 做精确页码/表图锚定时将需要从零开始。

2. **存在可能误导 A2a 的强主张**（对照 §3 检查项"是否存在可能误导 A2a 的强主张"）：A.3 中 C12 说"本文已把原文抽取字段、分类项、模型节点或报告叶子列为'原文模式候选叶子映射（A1 种子）'"——可能被 A2a 误读为"维度树复原已基本完成"，但实际覆盖率不足 20%。

3. **效度威胁与挑战/路线图维度完全缺失**：Section 7 的 3 类 threat 和 Section 8 的挑战/机遇分类体系是 SLR 方法学的重要组成部分，也直接对应 `pattern-field-schema.md` 中 `validity_threat_pattern` 和 `finding_pattern` 的字段合同。

### M（Moderate）— 不阻塞的清晰度或维护性建议

1. **根节点命名过于泛化**：`[dim-llm4se-systematic-review-root]` 未体现本文是"SLR on LLM4SE with extraction form + taxonomy + classification schema + roadmap"。建议改名为 `[dim-hou2024-llm4se-slr-root]` 并在描述中强调"4 RQ + Table 5 extraction form + 多层分类 schema + Appendix + replication package"。

2. **A.1 来源标识中 GitHub repo 链接建议补充克隆验证状态**：当前 A.1 中的 GitHub URL 标注为 `not_verified_link`，但原文在 Section 2.5 进行了显式声明。建议 A2a 验证 repo 仍可访问且包含所声称的 artifacts。

3. **A.4 中仅有的 2 条检查的覆盖度有限**：建议增加至少 4 条检查对应本报告 §4.2 中新增的 4 个主干分支。

### 最终建议

**NEEDS FIX**。

当前 `review.md` 的维度树本质上是一个 **通用元维度接口层**（A1-M0--M6 的 4 层映射），而不是从原文真实结构中复原出来的**原文专用维度树**。这违反了 `survey_of_surveys/GUIDE.md` §8.4 中"维度树必须忠实于原文 schema"和 `pattern-field-schema.md` §8.2 中"每个叶子必须有原文定位和完整取值空间"的合同要求。

在完成本报告 §5 中标注为 C 的 6 项修复（特别是补充 8 个主干分支、25+ 个叶子、8+ 条 RQ finding、10+ 条关系边）之前，该论文的维度树不能进入 A2a 统计合成。C 级问题会直接导致 Paper2 的"模式演化"与"字段级内容证据"工程在该论文上停摆。

建议修复优先级：先修复主干分支（C1 和 C2），再修复 RQ finding 和关系边（C3 和 C4），最后修复证据锚定精度（I1）和 misleading claims（I2）。

---

*审计人：deepseek | 审计日期：2026-06-29 | 审计范围：全文级 | 证据等级：全文文本级；图表待人工核对 | 仓库文件无修改*
