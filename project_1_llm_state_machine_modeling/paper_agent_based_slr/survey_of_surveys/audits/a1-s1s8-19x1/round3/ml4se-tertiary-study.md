# A1 round3 独立审计：ml4se-tertiary-study

> 审计边界：本文件只服务 `survey_of_surveys/` 的 A1 S1--S8 与原生维度树 / 森林抽取复核，**不得**把本文件中的文本级统计、等级或建议直接写成 Paper2 的 final quantitative finding。后续如要进入正式定量结论，必须由 A2a 对 PDF 版面、表图、supplementary / Zenodo 制品和字段级证据链再次精核。

## 1. 执行与阅读依据

- 角色与约束：A1 survey-of-surveys 单篇维度抽取 subagent；未开启 sub-subagent；只处理 `papers/ml4se-tertiary-study`。
- 已读规范：`ai-research-writing-skill/SKILL.md`、`research-planning/SKILL.md`、`survey_of_surveys/GUIDE.md` §6.3 / §6.4。
- 已读本地文件：
  - `papers/ml4se-tertiary-study/bibtex.bib`：确认正式引用为 Kotti / Galanopoulou / Spinellis，ACM Computing Surveys 55(12)，2023，DOI `10.1145/3572905`。
  - `papers/ml4se-tertiary-study/paper_content.txt`：正文按章节通读；参考文献段用于确认文本提取完整性与 included-study 编号来源，未逐条重建 83 篇二次研究 bibliographic record。
  - `papers/ml4se-tertiary-study/review.md`：重点审计快速卡片、维度树复原、S1--S8 表与五分栏拆分。
  - `papers/ml4se-tertiary-study/evidence_chain.md`：审计 A.1--A.4 是否足以支撑当前 `review.md` 和 SUMMARY 的 S1--S8 / 维度树口径。
- PDF 核对：用 `pdfinfo` 确认本地 PDF 为 37 页 arXiv / submitted manuscript；用 `pdftotext -layout` spot-check 关键页：p.5--12（Fig.1、§3 方法、RQ、检索、Kappa、DARE、数据抽取）、p.15（Table 5 SWEBOK）、p.23--24（Table 6 / Fig.6 / Table 7 ML 轴与任务）、p.27--29（Implications、Threats、Conclusion）。未核对 Zenodo / CSV supplementary。
- 主要原文依据：
  - 摘要：系统收集、质量评价、汇总、分类 83 篇 ML4SE reviews，覆盖 6,117 个非唯一 primary-study 覆盖计数。
  - §3.1：三条 RQ：SE task、欠覆盖 KA、ML techniques。
  - §3.2--§3.5：自动检索、手工检索、backward / forward snowballing、IC/EC、Kappa 校准、DARE-4 QA。
  - §3.6：每篇 quality-accepted secondary study 的抽取字段、SWEBOK KA/subarea/task、open coding、ML 四轴。
  - §4.1--§4.4：83 篇二次研究的书目 / QA / review type / SWEBOK / ML 轴统计和表图。
  - §5--§7：Implications 1--7、Threats to Validity、结论与研究者 / 实践者建议。

## 2. 关键分母与样本单位裁决

1. **主样本单位**：`secondary_study`，即最终 83 篇通过 DARE-4 QA 阈值的 ML4SE secondary reviews / studies。它们才是本文逐篇编码、质量评价和统计汇总的主对象。
2. **primary-study 数字边界**：6,117 是 83 篇二次研究报告或推断出的 **non-unique primary works / coverage count**，不是去重后的 primary-study 样本库，也不是本文逐篇编码的 primary-study 分母。
3. **分母链（文本级，待 supplementary 精核）**：
   - 自动检索：1,897 条 collected studies → DOI 去重后 1,566 条。
   - 手工检索：+1 条，形成 1,567 条；其中 15 条用于 IC/EC Kappa 校准，剩余 1,552 条 split 给两位作者筛选。
   - 选择与质量评价：所有搜索来源最终形成 140 distinct secondary studies 进入 DARE-4 QA；57 篇 QA < 2.0 被排除，83 篇进入分析。
   - backward snowballing：质量接受 reviews 的 3,195 条参考文献被评估，纳入 16 篇，其中 7 篇通过 QA；第二轮 backward 未新增。
   - forward snowballing：Scopus 检索 2,461 条 citing studies，纳入 84 篇，其中 43 篇通过 QA；其中 2 篇为已接受研究的扩展版本，保留扩展版本。
   - 审稿建议补入：3 篇未由检索策略识别但符合选择标准的研究被加入。
4. **QA / Kappa 边界**：Cohen’s Kappa ≥ 0.8 只用于 15 篇随机样本上的 IC/EC 校准；QA 阶段报告的是 extractor/checker 流程与 82% inter-rater agreement，不应把二者混写成“全流程 Kappa”。
5. **SWEBOK 边界**：搜索关键词阶段排除了 Computing / Mathematical / Engineering Foundations；但结果 Table 5 仍出现 Engineering Foundations / Statistical Analysis 1 篇。后续树表应区分“未作为检索关键词 seed”与“最终 KA 映射结果”。
6. **证据强度边界**：本轮可作为 A1 文本级 schema_seed / 主统计池候选审计，不可作为最终跨论文定量统计或目标领域 finding。

## 3. S1--S8 五分栏审计

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（强） | 摘要和 §3.1 明确本文是 ML4SE tertiary review，目标是质量评价目录、汇总所有 ML-in-SE secondary reviews、描述领域状态并寻找研究机会；RQ1--RQ3 分别对应 SE tasks、欠覆盖 SWEBOK KAs、ML techniques。 | 根对象应写为“83 篇 ML4SE secondary studies”；RQ 是字段用途锚：RQ1→KA/subarea/task，RQ2→coverage gap + further research / implications，RQ3→ML 四轴 + application task。 | 可作为 tertiary-review task / RQ-field contract 的强 schema seed；只贡献综述方法模式，不迁移 ML4SE 领域结论。 | 核对 ACM final 与本地 arXiv/submitted manuscript 在年份、页码、RQ 文本上的差异。 |
| S2 语料收集与筛选（强，文本级） | §3.2--§3.5 给出自动检索、手工检索、backward / forward snowballing、IC/EC、Kappa pilot、140→83 的 QA 漏斗；Fig.1 可视化流程。 | 应复原为多阶段漏斗森林：search-string construction → automated/manual search → DOI 去重 → IC/EC Kappa 校准与 split screening → snowballing → DARE-4 QA。 | 可作为主统计池候选的语料构造模式；但 A1 当前只能记录分母链 schema，不得把中间分母或 primary coverage 写成 final finding。 | 必须核对 `dl_search_results.csv`、`cohen_kappa_agreement.csv`、`study_selection_reviewer_{1,2}.csv`、backward/forward CSV；特别补全 1,897 / 1,566 / 1,567 / 1,552 / 3,195 / 2,461 / 140 / 83 的可复验链。 |
| S3 原生维度树 / 样本编码对象（强） | §3.6 明列每篇 quality-accepted secondary study 的字段；Tables 3--4 枚举 83 篇，Table 5 映射 SWEBOK KA/subarea，Table 6 映射 ML 四轴，Table 7 汇总 ML application task。 | 原生结构不是单棵树，而是以 `secondary_study` 为根的共根维度森林：书目元数据、研究设计、QA、primary coverage、SWEBOK KA×SE task、ML 四轴、further-research / implications、threats / artifacts。 | 可作为原生编码对象与维度森林模式的强 schema seed；primary coverage 只能是叶子字段。 | 核对 Tables 3--4 的列顺序：`Study / Venue / Year / Publisher / QA Score / Primary / Covered Years`；不可把 `QA Score` 当作 primary count。 |
| S4 字段级证据（中） | §3.6 给字段清单；Tables 3--7、Fig.3--6 与 footnote 文件提供字段结果与制品线索；但当前本地 `evidence_chain.md` 仍是树级最小 claim map，未列逐字段证据短引和 sample-level row anchors。 | 字段类型包括封闭枚举、数值、区间、关系值、自由文本与外部分类法引用；需要显式记录每个叶子的分母、缺失值语义和是否来自推断。 | 文本级可用作字段合同 seed；进入正式统计前必须降级为“中”，直到 supplementary / row-level evidence 完整核验。 | 逐项核验 Tables 3--7、Fig.3--6、Zenodo CSV / MD 文件；补全 A.2 证据账本中的原文短引、行号 / 页码、表号和支撑叶子标识。 |
| S5 维度模式演化（中） | §3.2 说明 search keywords 来自 SWEBOK、Kitchenham tertiary keywords、CSUR titles；§3.6 说明 SE task open coding、讨论后泛化/特化、qualitative content analysis；ML 四轴来自既有文献，Table 7 是事后 application-task 分组。 | 应复原为“先验分类法 + 人工开放编码 + 讨论归并 + 事后归纳”的混合维度形成过程；不是完整公开 codebook evolution。 | 可作为“维度如何形成”的中等级 schema seed；不宜升级为强 codebook-version / conflict-resolution evidence。 | 查 `knowledge_areas.csv`、`further_research.csv`、`ml_techniques.csv` 是否保留原始 code、合并记录、disagreement log；若无，保持 S5=中。 |
| S6 统计分析（中；文本级强但最终统计前降级） | §4.1--§4.4 报告年份、publisher、QA、研究类型、SWEBOK KA、primary coverage、ML 四轴与 KA×ML heatmap；Table 6 给 54/65%、65/78%、82/99%、72/87% 等四轴计数。 | 统计层由字段树派生：83 reviews 是主分母；6,117 是 non-unique coverage sum；Table 5 的 `Sec.` 与 `Prim.` 是不同层级；Fig.6 是 KA×ML 轴比例。 | 可作为“有统计分析”与“多层分母”模式候选；A2a 前不得进入 SUMMARY 定量统计或 final finding。建议单篇等级表写“中”或“强（文本级；A2a 前禁用定量）”并统一口径。 | 逐表重算百分比、四舍五入、Sec./Prim. 列、Fig.6 heatmap、primary 数推断规则；核验 non-unique primary coverage 与部分 bibliography-derived count。 |
| S7 候选 finding（强，限方法模式） | §4.3.1 给 7 类 general recommendations 及 n 计数；§5 形成 Implications 1--7；§7 提炼 quality/testing/process 主导、人本 KA 欠覆盖、offline/model-based/supervised 主导、数据与 SE 文献缺陷等结论。 | finding 形成路径是“field/statistical observation → KA coverage gap / obstacle → implication / recommendation”；这比单纯频次表更接近可迁移的 candidate finding 机制。 | 可作为候选 finding 形成机制的强 seed；具体 ML4SE finding、KA 频次、建议内容不得迁移为 Paper2 领域结论。 | 为每条 implication 建立 support / counter-evidence / scope map；区分统计观察、作者推断、领域建议与本仓库方法启发。 |
| S8 研究者 / 作者质疑与裁决（强，非 full audit trail） | §3.4：15 篇随机样本 IC/EC Kappa ≥ 0.8、分歧 consensus；§3.5：DARE-4、82% agreement、QA4 分歧较多；§3.6：extractor/checker、冲突由最后作者解决；§6：Study Selection / Data / Research threats。 | 应复原为裁决与质量控制树：protocol review by all authors、extractor/checker、Kappa pilot、split screening、DARE-4 QA、last-author conflict resolution、threat taxonomy。 | 可统计为“报告了人类裁决 / agreement / QA / threats”的强过程模式；但不是公开逐项裁决日志。 | 核验 `cohen_kappa_agreement.csv`、`dare_assessment.csv`、selection reviewer CSV；若 supplementary 不含逐项 disagreement log，避免写成 full audit trail。 |

## 4. 原生维度树 / 维度森林（独立复原）

```text
根：ML4SE tertiary review 的 quality-accepted secondary studies
样本单位：secondary_study，n=83；primary works=6,117 只是 non-unique coverage count
统计边界：83 reviews 是主分母；140 是 QA 前候选；1,567 / 1,566 / 1,897 是检索分母；6,117 是覆盖度叶子

F0 语料构造与筛选森林
├── search_seed：SWEBOK-derived SE keywords；CSUR-derived secondary-study keywords；CSUR-derived ML keywords
├── automated_search：IEEE Xplore / ACM DL / Scopus；2015-01 至 2020-06；1,897 collected → DOI 去重 1,566
├── manual_search：每个库随机 3-tuple search；+1 relevant paper → 1,567
├── screening_calibration：15 random studies；IC/EC；Cohen’s Kappa ≥ 0.8；consensus
├── split_screening：剩余 1,552；两位作者各 776；必要时 full text；疑难由讨论决定
├── backward_snowballing：3,195 references → 16 included → 7 QA-accepted；第二轮 0 新增
├── forward_snowballing：2,461 citing studies → 84 included → 43 QA-accepted；2 extensions 替代旧研究
└── QA_funnel：140 distinct secondary studies → DARE-4 QA ≥ 2.0 → 83 final studies

F1 书目与研究设计森林（Tables 3--4 / §3.6 / §4.1）
├── bibliographic：study reference；title/source；venue；year；publisher；authors；institutions；countries
├── review_type：SLR / systematic mapping / survey / taxonomy / meta-analysis；可有 second research type
├── research_method：Kitchenham / Petersen / Hall / Wohlin / Easterbrook / Sabir / Zhou / Dybå / CASP 等引用或推断
└── primary_coverage：Primary count；Covered Years；部分 count/year 由 bibliography inference 得到

F2 DARE-4 质量评估森林（Table 2 / §3.5）
├── QA1_IC_EC：Y=1 / P=0.5 / N=0
├── QA2_search_space：4+ libraries plus extra strategy 等 rubric
├── QA3_primary_quality_assessment：是否描述并应用 primary-study QA
├── QA4_primary_information：是否提供 primary-study 信息；分歧最多
└── QA_total：0..4；纳入阈值 ≥2；57/140 被排除

F3 SWEBOK KA × subarea × SE task 主题森林（RQ1/RQ2；Table 5 / §4.2 / §4.3）
├── swebok_ka：Software Quality、Testing、SE Process、SE Management、Requirements、Maintenance、Design、Configuration Management、Models & Methods、Professional Practice、Engineering Foundations 等结果侧映射
├── subarea：Practical Considerations、Test Techniques、SW Life Cycles、SW Project Planning 等 Table 5 子域
├── sec_count_and_percent：每个 KA/subarea cell 的 secondary-study 数和比例
├── prim_coverage：每个 cell 的 primary coverage count；非唯一、非主样本单位
├── se_task_open_codes：每篇 1--3 个任务码；可多对多映射到 KA
└── further_research_by_KA：按 KA/task 组织的研究空白、障碍与建议

F4 ML 技术分类森林（RQ3；§3.6 / §4.4 / Table 6 / Table 7）
├── role_of_AI_in_SE：SBSE / fuzzy-probabilistic / classification-learning-prediction
├── supervision：supervised / unsupervised / semi-supervised / reinforcement
├── incrementality：batch-offline / online-incremental
├── generalizability：model-based / instance-based
├── per_axis_most_prominent_category：每篇每轴取 most prominent category
└── ml_application_task：classification-clustering-regression / pattern discovery / dimensionality reduction / information retrieval / stochastic search / generation / hybrid / miscellaneous

F5 finding 与 implication 森林（§4.3.1 / §5 / §7）
├── general_recommendations：comparative-vs-statistical、empirical、open-large datasets、hybrid-ensemble-incremental、industrial/practitioner、hyperparameter、class imbalance
├── implication_1_to_7：empirical-industrial validation；SE literature deficiencies；human-centered KA data；data pipeline documentation/automation；proprietary data/data-paper paradigm；online/incremental ML；hybrid/cross-domain methods
└── conclusion_claims：领域 claim 仅可记录为 ML4SE 原文 finding，不得迁移为 Paper2 final finding

F6 研究者裁决、威胁与复现制品森林（§3 / §6 / footnotes）
├── protocol_and_roles：review protocol；all-author review；extractor/checker
├── agreement_and_resolution：Kappa pilot；consensus；82% QA agreement；last-author conflict resolution
├── threats：Study Selection / Data / Research validity
└── artifacts：review-protocol.md、dl_search_results.csv、cohen_kappa_agreement.csv、study_selection_reviewer_{1,2}.csv、dare_assessment.csv、knowledge_areas.csv、further_research.csv、ml_techniques.csv 等
```

## 5. 对现有 review / evidence / SUMMARY 的 C/I/M 修改清单

### C / critical

- **C-01（潜在 C；若已进入写作则必须立即修）**：任何下游文本若把 6,117 写成“本文逐篇编码的 primary-study 样本数”或“去重 primary-study 总数”，应立即改为“83 篇 secondary studies 为主样本单位；6,117 为 non-unique primary-work coverage count”。当前 `review.md` 主体基本已意识到此点，但 SUMMARY / 后续写作复制时仍需强制保留该边界。
- **C-02（潜在 C；若进入 final quantitative finding 则必须立即修）**：A1 round3、本地 `paper_content` 与 partial PDF spot-check 只支撑 schema_seed / 主统计池候选；不得直接把 Table 5 / Table 6 的 ML4SE 数字写入 Paper2 final empirical finding。

### I / important

- **I-01：`evidence_chain.md` 的分母链过度压缩。** A.2 `ev-ml4se-tertiary-study-denom` 目前只写 `1 567 → 140 → 83`，应补入 1,897 automated collected、1,566 DOI-dedup、15-study Kappa pilot、1,552 split screening、3,195 backward references、16/7 backward、2,461 forward、84/43 forward、3 reviewer-suggested studies、57 QA-rejected 等关键分母；否则后续容易误读语料链。
- **I-02：`review.md` 叶子表的 Tables 3--4 列号需修。** 当前 `L4.1 primary 数` 写为 Table 3/4 第 5 列，但 PDF / `paper_content` 表头显示列序为 `Study / Venue / Year / Publisher / QA Score / Primary / Covered Years`，Primary 是第 6 列，Covered Years 是第 7 列。
- **I-03：SWEBOK keyword exclusion 与 result mapping 的表述需修。** `review.md` 将 Engineering Foundations 同 Computing / Mathematical Foundations 一起写成 scope 排除，但 Table 5 结果中仍出现 Engineering Foundations / Statistical Analysis 1 篇。建议改为：“这些 Foundations 未作为检索关键词 seed；最终结果侧仍映射到 Engineering Foundations 1 篇。”
- **I-04：S6 / S8 等级在 `review.md` 与 SUMMARY 之间不完全一致。** 本审计建议 S6 采用“中（文本级强，最终统计前降级）”，S8 可采用“强（报告了 Kappa / agreement / QA / threats，但非 full audit trail）”。SUMMARY 当前 S6=中、S8=中；`review.md` 当前 S6=强、S8=强。主线程需统一等级口径，并在五分栏里写明文本级 / A2a 边界。
- **I-05：`review.md` 早期六类 pattern 中的 validity / threat 描述已过期。** §2 仍写“threats 章节待进一步定位 / 本轮未完整定位”，但后文维度树已读并引用 §6 Study Selection / Data / Research threats。建议更新早期 pattern，避免读者只看前半部分得出错误结论。
- **I-06：`review.md` 快速卡片的“是否目标证据池=否”需消歧。** 该论文不是 Paper2 目标领域证据池，但在 `survey_of_surveys` 自身主统计池中是候选样本。建议改成“不是目标领域证据；是 survey_of_surveys 主统计池候选（A2a 前 schema_seed）”。
- **I-07：`evidence_chain.md` A.2 证据短引与行号不足。** 当前多处写“短引见 review.md 的证据锚点”且证据强度统一 `not_verified`；A2a 前至少应为 S1--S8 核心证据补 `paper_content` 行号 / PDF 页码 / 表号 / 图号，尤其是 RQ、分母链、DARE-4、Table 5、Table 6、Implications、Threats。
- **I-08：QA/Kappa 口径需防止混写。** 后续 review/SUMMARY 若采用本审计，应明确：Kappa ≥ 0.8 是 15 篇 random studies 上的 IC/EC 校准；QA 阶段是 extractor/checker + 82% agreement；RQ1 task coding 冲突由最后作者解决。

### M / minor

- **M-01：阅读状态文字可更新。** 当前 `review.md` 审计卡片仍写未打开 PDF；本 round3 已做关键页 PDF text-layout spot-check，但未做 full visual / supplementary audit。若主线程采纳，可在 adjudication 中记录，不必马上改原文。
- **M-02：术语中文化可更稳。** “原始研究数量（原始研究数量）”“内容分析（内容分析）”“混合（混合）”等重复括号可在后续清理；不影响本次审计结论。
- **M-03：早期 `schema 历史观察` 与后文 A1-DT v2 口径可合并压缩。** 当前不影响事实，但增加读者认知负担。
- **M-04：SUMMARY 中 CSUR CCF 待核验状态与本地未建档说明可保留；若以后官方页面可访问，再统一回填，不应在本轮 A1 文本审计中冒充官方核验。**

## 6. 不足与交接

- 未下载或核验 Zenodo / supplementary CSV；所有涉及逐行 study list、field-level sample ID、agreement CSV、DARE CSV、knowledge_areas / ml_techniques 的结论均保持 A2a 待核验。
- 未对 ACM final 版本重新抓取文本；本地 PDF / `paper_content.txt` 显示为 arXiv submitted manuscript 形态，正式页码和版面需后续核对。
- 本文件是独立审计结果，不自动覆盖 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`；是否采纳由主线程 adjudication 决定。
