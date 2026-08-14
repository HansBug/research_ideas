# llm4se-systematic-review · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是。读取路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。本次采用其 claim-evidence、reviewer-risk、强主张降级和 roadmap 不得写成完成型贡献的口径。
- 是否读取 `$research-planning`：是。读取路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。本次采用其“严格贴合原文方法、数据、指标；不清楚时显式标注”的口径。
- 是否读取 `$oh-my-codex:autoresearch`：是。读取路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本次采用其 artifact-gated、validator evidence 不因模型自称完成而完成的口径。
- 是否完整阅读 `paper_content.txt`：是。按 1--4152 行完整过读，覆盖摘要、引言、Approach、RQ1--RQ4、Threats、Challenges and Opportunities、Roadmap、Conclusion、References 和 Appendix A--E；参考文献列表未逐条核验 570+ 引用元数据，但已阅读其在正文和附录 evidence table 中的引用结构。
- 是否核对 `paper.pdf`：是，选择性视觉核对。用 `pdfinfo` 确认本地 PDF 为 79 页；渲染并检查第 5 页 Fig. 1 study identification and selection process、第 9 页 Table 5 extraction form、第 72 页 Appendix A/Table 13 data types、第 76 页 Appendix D/Table 16 evaluation metrics、第 78 页 Appendix E/Table 17 SE tasks。未逐页核对全部图表，因此所有未抽检表图仍应在 A2a 精核。

本次还读取了文库级规则和 story：`survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md`、`story/paper_story.md`。核心约束是：维度树必须从原文 RQ / extraction form / taxonomy / coding scheme / quality / validity / evidence / finding path 推导；A1-DT 的 `not_verified` 或泛定位证据只能作为 `schema_seed` / `candidate_finding`，不得升级为 `statistical_synthesis` 或 final finding。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是对 LLM4SE 做系统文献综述，分析 2017 年 1 月至 2024 年 1 月的 395 篇研究论文，回答四个 RQ：

- RQ1：哪些 LLM 已被用于解决 SE tasks。原文按 encoder-only、encoder-decoder、decoder-only 组织模型 taxonomy，并分析模型家族、参数规模、任务适配与年度趋势。
- RQ2：SE-related datasets 如何被收集、预处理和使用。原文拆成 data source、data type、preprocessing procedure、input form 等字段。
- RQ3：哪些技术用于优化和评价 LLM4SE。原文覆盖 full fine-tuning、ICL、PEFT、prompt engineering 和 evaluation metrics，并把 metrics 绑定到 regression / classification / recommendation / generation 四类 problem type。
- RQ4：哪些 SE tasks 已被 LLM4SE 处理。原文按 SDLC 六阶段组织 85 个具体任务，并统计 problem type 分布。

贡献声明不是单一发现，而是“范围和分母 + 模型分类 + 数据处理 + 优化/评价 + SE task taxonomy + challenges / research directions”的组合。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文遵循 Kitchenham SLR 方法，包含 planning、conducting、analyzing 三步。检索使用 QGS：

- manual search：ICSE、ESEC/FSE、ASE、ISSTA、TOSEM、TSE 六个顶级 SE venue；爬取 4,618 篇，人工确认 51 篇相关论文形成 QGS。
- search string：由 SE task keywords 和 LLM keywords 两组构成；SE keywords 覆盖 code generation/search/completion/summarization、bug localization、program repair、requirement extraction/traceability/validation、mining GitHub/SO/app 等；LLM keywords 覆盖 LLM、PLM、pre-trained、Transformer、BERT、Codex、GPT、T5、ChatGPT 等。
- automated search：IEEE Xplore、ACM Digital Library、ScienceDirect、Web of Science、Springer、arXiv、DBLP 七个数据库；初始 218,765 条。
- study selection：少于 8 页过滤、title/abstract/keywords、venue 识别、去重、full-text scan、quality assessment；质量评估后得到 382 篇。
- snowballing：对 382 篇做 backward / forward snowballing，分别得到 3,964 和 9,610 条线索，去重后 5,152 条，再补入 13 篇；最终 395 篇。
- quality assessment：Table 4 给出 10 个 QAC。QAC1--QAC3 是 relevance gate；QAC4--QAC10 按 0/1/2/3 打分，正式发表论文阈值 16.8/21，arXiv 阈值 14.4/18。
- data extraction：Table 5 把 8 个 extracted data items 直接绑定到 RQ，是原文 schema 的主入口。

原文的 finding 不是从单个字段直接生成，而是沿着 “extraction field -> taxonomy / count / trend -> RQ summary -> Section 8 challenges / opportunities / roadmap” 形成。尤其 Section 8.3 是 prose roadmap，不是已完成的统计 finding，也未在我核对的文本中表现为独立 roadmap figure。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 至少包括：

- Extraction form：Table 5 八项 data items：SE task category、LLM category、LLM characteristics and applicability、data handling techniques、weight training algorithms and optimizer、evaluation metrics、SE activity、developed strategies and solutions。
- Corpus / quality rubric：Fig. 1 study identification and selection process；Table 3 inclusion / exclusion criteria；Table 4 QAC。
- RQ1 taxonomy：LLM architectures 三分法；Fig. 4 model taxonomy；Table 6 architecture-to-SE-task fit；Fig. 5 yearly trend。
- RQ2 schema：dataset source 四类 open-source / collected / constructed / industrial；data type 五类 text / code / graph / repository / combined；preprocessing flow for text/code；input form 四类 token / tree-graph / pixel / hybrid；Appendix A/Table 13 和 Appendix B/Table 14 逐项映射到 primary-study references。
- RQ3 schema：tuning techniques、PEFT 子类 LoRA / prompt tuning / prefix tuning / adapter tuning；prompt engineering 八类 few-shot / zero-shot / CoT / APE / CoC / Auto-CoT / MoT / SCoT 加 Others；evaluation metrics 按 problem type 组织；Appendix C/Table 15 和 Appendix D/Table 16 提供 evidence table。
- RQ4 taxonomy：SDLC 六阶段；85 个具体 SE tasks；problem type 四类；Table 10 和 Appendix E/Table 17 以 field value + study count + references 方式呈现。
- Validity schema：Section 7 明确 paper search omission、study selection bias、empirical knowledge bias，并给出缓解措施。
- Artifact 字段：正文和 footnote 指向 replication package；`paper_content.txt` 指向 `https://github.com/xinyi-hou/LLM4SE_SLR`，而 `metadata.json` abstract 记录 `https://github.com/security-pride/LLM4SE_SLR`，该差异需要联网核验。

原文未充分暴露的是 coder agreement、字段冲突解决日志、schema revision history。因此 Paper2 可以借鉴其字段和 evidence table，但不能把它写成 audit-first 的完整过程证据范例。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文每个 RQ 都先给 taxonomy 或字段表，再给统计结果和 RQ summary。例如：

- RQ1 从 architecture taxonomy 和趋势图得出 decoder-only 逐渐占优、不同 architecture 适配不同任务。
- RQ2 从 dataset source/type/input form 统计得出 open-source 数据占主导、industrial data 稀少、token-based input 占绝对多数。
- RQ3 从 tuning/prompt/metrics 表得出 PEFT、prompt engineering 和 problem-type-specific metrics 的使用格局。
- RQ4 从 SDLC + task table 得出 development / maintenance / QA 研究多，requirements / design / management 覆盖少，generation problem type 占主导。
- Section 8 再把上述统计观察组织为 challenges、opportunities 和 roadmap：model size/deployment、data dependency、ambiguity、generalizability、evaluation、interpretability/trustworthiness/ethics；以及 code-specialized LLMs、ChatGPT、task-specific training、collaborative LLMs、new input forms、widening SE phases、domain-specific datasets、evaluation framework、SE4LLM 等方向。

这些是候选 finding path，不是 Paper2 的目标领域 finding。对 Paper2 可迁移的是“统计观察必须经过 gap / opportunity / roadmap 解释并保留 claim strength”，而不是 LLM4SE 领域结论本身。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 大体准确，但单位对象和分支粒度需修正。 | 当前根节点把该文识别为“大规模 RQ 驱动分类树”是合理的；但单位对象写成 `primary study / secondary study` 偏松，原文主分母是 395 篇 LLM4SE research papers，经 QAC3 尝试排除 secondary study，虽又保留 systematic views/survey/review 进入质量阶段，需写成“LLM4SE research paper / retained study with QAC status”。 | M |
| 主干分支是否覆盖原文 schema | 未覆盖。 | 当前正式树只有范围、语料、主题、方法、评价/发现五个泛分支；没有把 Table 5 八项 extraction form、Table 3/4 纳排与 QAC、RQ1--RQ4 的分类体系、Appendix A--E evidence tables、Section 7 threats、Section 8 roadmap/finding path 作为一等主干/子树。旧“历史草稿”更接近原文，但被标注为不作事实真源。 | C |
| 叶子维度是否足够具体 | 不足。 | 当前六个 `leaf-*` 是通用接口层；`review.md` 已明确它们不是原文叶子全集，这避免了最严重误读。但“原文模式候选叶子映射”只有 5 个粗叶子：SE task、LLM method、dataset-benchmark、metric、limitation-risk，明显小于原文真实叶子空间。 | C |
| 取值空间是否可执行 | 部分不可执行。 | 候选取值空间把 “LLM 方法与模型” 写成模型家族、prompting、fine-tuning、RAG、agent、tool use、workflow；其中部分不是 Table 5 或正文核心 taxonomy 的封闭取值，容易混入后验泛化概念。data source/type/input form、problem type->metric、SDLC->task 这些原文封闭或层级枚举未展开。 | I |
| 关系边是否缺失 | 缺失关键关系。 | 当前只有 method->evidence、taxonomy->finding 两条泛关系；缺少 RQ->data item、search step->count、QAC->eligibility、architecture->task fit、dataset source/type->study count、problem type->metric、SDLC activity->specific task、threat->mitigation、appendix field value->primary-study references。 | I |
| 统计用途 / 分母是否正确 | 纪律方向正确，但分母不够具体。 | 当前明确 A1-DT 不进入 SUMMARY 定量统计，这是正确的；但对原文字段自身的分母缺失，例如 395 collected papers、382 after QA、374 explicitly stating dataset、355 explicitly stating input form、problem type / task-instance count 等，没有逐叶子记录。 | I |
| 候选 finding 路径是否完整 | 不完整。 | 当前只有 taxonomy->finding 泛边；没有把 RQ summary、Section 8.1 challenges、8.2 opportunities、8.3 roadmap 以及“under-explored phases / data dependency / metric limitation”等路径拆成 candidate finding ledger。 | I |
| A.1--A.4 证据链是否足够 | 结构合格，内容不足。 | A.1--A.4 表头和回链结构存在；但 A.2 仅 EV-001--005 泛定位，原文页码写“待复核”、短引写“见释义”，无法审计某个叶子是否来自 Table 5、Table 13、Table 16 或 Table 17。`not_verified` 降级是合规的，但不能声称全文级维度树复原已经充分。 | I |
| 是否存在可能误导 A2a 的强主张 | 有局部风险，但已被降级声明缓解。 | 当前 `review.md` 显式说明通用六叶不是原文全集，且 C12 说明候选叶子不是完成复原；这避免了“把通用 6 个 leaf 接口误当原文 schema”的 C 级误导。但“本文已把原文抽取字段、分类项、模型节点或报告叶子列为候选叶子映射”容易让读者忽略该表只有 5 个粗叶，需改成“仅列出极粗入口，非完整候选映射”。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为忠实原文维度树。建议最小修复不是扩写自然语言摘要，而是把正式 `维度树复原` 从“通用接口树 + 5 个粗候选叶子”升级为“原文 schema 子树 + 通用接口映射”。建议骨架如下。

| 层级 | 节点 / 叶子 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| 根节点 | LLM4SE SLR schema，单位对象为纳入/保留的 LLM4SE research paper | 2017-01 至 2024-01；最终 395 篇；正式发表 / arXiv 状态；primary-study status / retained review ambiguity | 可作为后续主统计池候选；A1-DT 当前仅 `schema_seed` | `not_in_scope`、`excluded_by_qac`、`not_verified` | 摘要；Section 2.1；Fig. 1；Table 3/4 |
| B0 Protocol / corpus | 检索与纳排链条 | manual venues 6 个；QGS 51；databases 7 个；218,765 initial；80,611 / 5,078 / 1,172 / 810 / 594 / 382 / +13 / 395；inclusion/exclusion；snowballing | 可统计，分母按阶段记录 | `not_reported`、`not_applicable`、`metadata_incomplete`、`manual_review_retained` | Fig. 1；Table 2；Table 3；Section 2.2--2.4 |
| B0.1 Quality rubric | QAC 与 eligibility gate | QAC1--QAC10；QAC1--3 的 -1 排除；QAC4--10 的 0/1/2/3；published threshold 16.8/21；arXiv threshold 14.4/18 | 可统计，但需 artifact/QAC score 表支持 | `not_scored`、`score_not_available`、`qac_not_applicable` | Table 4；Section 2.3.2 |
| B1 RQ / extraction form | RQ 到 data item 映射 | Table 5 八项：SE task category、LLM category、LLM characteristics/applicability、data handling techniques、weight training algorithms/optimizer、evaluation metrics、SE activity、strategies/solutions | 可作为字段合同，不直接统计 | `not_extracted`、`not_applicable`、`not_verified` | Table 5；Section 2.5 |
| B2 LLM object | LLM architecture / family / parameter / task fit / trend | architecture: encoder-only / encoder-decoder / decoder-only；model family 70+；parameter size if declared；task fit: understanding / generation / both；year trend 2020--2024 | 可统计，需区分 study count 与 model-instance count | `not_declared`、`unknown_architecture`、`multiple_models` | Section 3；Fig. 4/5；Table 6；replication package |
| B3 Data object | data source / type / preprocessing / input form | source: open-source / collected / constructed / industrial；type: text / code / graph / repository / combined；preprocessing steps；input form: token / tree-graph / pixel / hybrid | 可统计；分母需分别记录 374 dataset-declared、355 input-form-declared 等 | `not_declared`、`not_applicable`、`unclear_type`、`multiple_types` | Section 4；Table 7/8；Fig. 7/8；Appendix A/B |
| B4 Optimization / prompting | tuning / PEFT / prompt engineering | full fine-tuning；ICL；PEFT: LoRA / prompt tuning / prefix tuning / adapter tuning；RL/SFT/syntax/task-oriented 等；prompt: few-shot / zero-shot / CoT / APE / CoC / Auto-CoT / MoT / SCoT / Others | 可统计，需以 study count 和 technique occurrence 区分 | `not_reported`、`custom_prompt`、`multiple_techniques` | Section 5.1--5.2；Fig. 9；Appendix C |
| B5 Evaluation | problem type 到 metric 的关系型字段 | problem type: regression / classification / recommendation / generation；metric family: MAE, Precision, Recall, F1, Accuracy, AUC, MRR, BLEU, Pass@k, CodeBLEU, ROUGE, etc. | 可统计；分母为 metric occurrence / problem-type task count，不能混用 | `no_metric_reported`、`task_specific_metric`、`not_applicable` | Section 5.3；Table 9；Appendix D/Table 16 |
| B6 SE task taxonomy | SDLC activity / specific task / problem type / artifact | activities: requirements, design, development, QA, maintenance, management；85 tasks；problem type: generation / classification / recommendation / regression；input/output artifact 可选 | 可统计；需区分 activity share、task count、study references | `other_task`、`unclear_activity`、`multiple_tasks` | Section 6；Fig. 10；Table 10；Appendix E/Table 17 |
| B7 Evidence / artifact layer | appendix evidence table / replication package / primary references | appendix A--E field value -> # studies -> references；artifact URL；selected primary studies list；model/parameter table | 可统计前需链接核验 | `dead_link`、`url_mismatch`、`artifact_not_checked`、`reference_not_verified` | Abstract footnote / Section 7 footnote；Appendix A--E；GitHub package |
| B8 Validity / threat | threat type / mitigation | paper search omission -> manual+automated+snowballing；study selection bias -> retention + secondary review + replication package；empirical knowledge bias -> prior survey categories and pre-reading | 不作为领域统计，作为 validity pattern | `threat_not_reported`、`mitigation_not_reported` | Section 7 |
| B9 Finding / roadmap path | RQ summary -> challenge/opportunity/roadmap | challenge: model size/deployment, data dependency, ambiguity, generalizability, evaluation, interpretability/trust/ethics；opportunity: code-specialized LLMs, ChatGPT, task-specific training, collaborative LLMs, new input forms, wider SE phases, domain datasets, evaluation framework；roadmap prose including formal verification and SE4LLM | 只作为 `candidate_finding` / `boundary_anchor`，不能写 final finding | `roadmap_only`、`author_opinion`、`not_supported_by_stat` | RQ summaries；Section 8.1--8.3 |

最小关系边表应至少包含：

| 关系边 | 源 | 关系 | 目标 | 缺失值语义 | 证据 |
|---|---|---|---|---|---|
| RQ->extraction item | RQ1--RQ4 | defines / requires | Table 5 data item | `no_data_item` | Table 5 |
| search stage->count | selection step | filters_to | next stage count | `count_not_reported` | Fig. 1 |
| QAC->eligibility | QAC criterion | gates | retained/excluded study | `score_not_available` | Table 4 |
| architecture->task fit | encoder-only / encoder-decoder / decoder-only | suited_for | understanding / generation / both and example tasks | `not_declared` | Table 6 |
| problem type->metric | regression/classification/recommendation/generation | measured_by | metric family | `no_metric_reported` | Table 9 / Table 16 |
| SDLC->specific task | SE activity | contains | 85 task leaves | `other_task` | Table 10 / Table 17 |
| field value->primary study refs | appendix field value | supported_by | references list | `reference_not_verified` | Appendix A--E |
| threat->mitigation | threat type | mitigated_by | mitigation action | `mitigation_not_reported` | Section 7 |
| statistical observation->candidate finding | RQ summary statistic | motivates | challenge / opportunity / roadmap item | `roadmap_only` | RQ summaries / Section 8 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将正式维度树从通用接口树升级为原文 schema 树 | `review.md` 的 `## 维度树复原`，尤其“维度树结构”和“叶子维度表” | 保留六个通用接口作为 cross-paper projection，但新增 B0--B9 原文子树；把旧“历史草稿”中的有效字段迁回事实真源，并用 stable IDs 标识。 | Table 5；Sections 2--8；Appendix A--E | C |
| 补全 Table 5 八项 extracted data items | `原文模式候选叶子映射（A1 种子）` | 不能只列 5 个粗叶；至少逐项列出 Table 5 的八个抽取字段，并说明服务 RQ、取值空间、证据要求、缺失值语义和是否可统计。 | PDF 第 9 页 Table 5；paper_content lines 386--395 | C |
| 把 QGS、纳排、QAC 质量 rubric 设为一等字段 | `语料收集与纳排` 相关节点、A.2 证据账本 | 加入 search stage counts、database counts、Table 3 inclusion/exclusion、Table 4 QAC 和 thresholds；QAC 是原文质量 schema，不能只在正文摘要里出现。 | Fig. 1；Table 3；Table 4；paper_content lines 229--381 | I |
| 展开 RQ1--RQ4 的原文 taxonomy 和 closed / hierarchical value space | `叶子维度表` 与 `原文模式候选叶子映射` | 增加 architecture、model family、parameter-declared、dataset source/type/input form、tuning/PEFT/prompt、problem type、metric、SDLC activity、specific task 等叶子。 | Sections 3--6；Table 6--10；Appendix A--E | I |
| 建立关系边表而非只保留两条泛边 | `关系边表` | 补 RQ->data item、architecture->task fit、problem type->metric、SDLC->task、appendix field->primary references、threat->mitigation、stat observation->candidate finding 等边。 | Table 5、6、9、10、13--17；Section 7/8 | I |
| 细化统计分母和 missing semantics | `统计与候选发现链路`、每个叶子维度 | 逐字段写分母：395、382、374、355、task-instance、metric occurrence 等；缺失值区分 `not_reported`、`not_declared`、`not_applicable`、`not_verified`、`multiple_values`、`artifact_not_checked`。 | RQ summaries；Table 8/9/10/13--17 | I |
| 重写 A.2 证据账本为可追溯条目 | `A.2 维度树证据账本` | 当前 EV-001--005 太泛；应新增证据条目分别锚定 RQ、Fig. 1、Table 3、Table 4、Table 5、Table 6、Table 9、Table 10、Appendix A--E、Section 7、Section 8，并给出页码/行号/短引。未精核可保留 `not_verified`，但不能只有“见释义”。 | `paper_content.txt` + PDF 第 5/9/72/76/78 页抽检 | I |
| 还原 finding path 和 roadmap 降级 | `统计与候选发现链路`、A.3 | 把 RQ summaries 到 Section 8 challenges / opportunities / roadmap 的路径列成 candidate finding ledger；明确 roadmap prose 不是完成型统计 finding，未发现独立 roadmap figure。 | paper_content lines 955--967、1173--1187、1924--1932、1976--2248 | I |
| 核验 artifact URL 差异 | 快速卡片、A.1、artifact 叶子 | `paper_content.txt` 指向 `xinyi-hou/LLM4SE_SLR`，`metadata.json` abstract 记录 `security-pride/LLM4SE_SLR`；正式引用前必须联网核验真实仓库、可访问性、license 和版本关系。 | abstract line 28；footnote line 1996；metadata.json abstract | M |
| 调整可能后验化的取值空间 | `orig-llm-method` 等候选叶子 | RAG、agent、tool use、workflow 若不是原文核心 taxonomy 或 Table 5 字段，应移到 `not_reported_or_later_extension` 或 Paper2 扩展候选，不要伪装成原文封闭取值。 | Table 5；Sections 5/8 | M |

## 6. C/I/M 结论

- C：2 项。最关键问题是正式 `维度树复原` 没有完整复原原文 schema，且 Table 5 八项 extraction form / RQ-driven taxonomy 被压缩成过小的通用接口与 5 个粗候选叶子。这会直接破坏 Paper2 的 A1->A2a 接力：A2a 如果按当前事实真源回填，会错过质量、纳排、数据、任务、指标、附录 evidence table 和 finding path 的关键字段。
- I：6 项。主要包括 QGS/QAC 未一等化、取值空间不可执行、关系边缺失、统计分母不具体、A.2/A.3 证据锚点过泛、candidate finding / roadmap 路径未复原。这些会实质影响维度树可用性、原文 schema 复原和证据可审计性。
- M：3 项。主要是根节点单位对象表述、artifact URL 差异、部分取值空间混入后验泛化术语。
- 最终建议：NEEDS FIX。

审计判断：当前 `review.md` 已经正确声明六个通用 `leaf-*` 不是原文 schema 全集，也把 `not_verified` 证据降级为 `schema_seed`，因此没有把 A1-DT 误写成完成型统计综合；但这只是防止过强主张，不能替代全文级维度树复原。对 `llm4se-systematic-review` 这种表格和附录非常丰富的 SLR，当前树显著过小，必须先补齐原文 schema 和证据锚点，才能作为 Paper2 后续 A2a/A2b 的可靠输入。
