# A1 Round3 单篇审计：llm-assistants-developer-productivity

> 范围声明：本文件只做 A1 文本级独立抽取与审计，服务 `survey_of_surveys` 的 S1--S8 与单篇原生维度树 / 维度森林返修输入。**不得把本文件中的文本级统计观察写成 final quantitative finding**；所有页码、表图、Zenodo / supplementary 与逐 PS 字段矩阵精核均留给 A2a。

## 1. 已阅读材料与审计依据

### 1.1 必读规则

- 已读 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：按 claim-evidence discipline，不造证据，不把未核验数字升级为强结论。
- 已读 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：先理解研究问题、方法、任务依赖与风险，再输出结构化审计。
- 已读 `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md` §6.3/§6.4：A1-DT v2 三层分离、原生样本编码树 / 森林、S1--S8 五分栏、A1 与 A2a 分离、不得把 `not_verified` / 文本级结果写成最终定量发现。

### 1.2 本地材料阅读

| 材料 | 阅读状态 | 用途 | 限制 |
|---|---|---|---|
| `bibtex.bib` | 已读 10 行 | 确认标题、作者、TOSEM 2026、DOI `10.1145/3809494` | 正式 ACM 元数据仍应由 A2a / 出版页核对 |
| `metadata.json` | 已读 | 核对本地元数据、arXiv PDF 来源、正式 publication date、当前 eligibility 字段 | 元数据内 `eligible_for_statistical_synthesis=true` 不能覆盖 A1 文本级限制 |
| `paper_content.txt` | 已按全文顺序通读 Page 1--43 | 抽取 RQ、检索筛选、QA、数据抽取、RQ0--RQ3、Discussion、Threats、Primary Studies PS1--PS39 | PDF 图表版式、精确页码、Zenodo 文件未逐项核验 |
| `review.md` | 已读快速卡、全文详读、维度树复原、S1--S8 段落 | 审计当前本地归纳是否过强 / 是否与原文一致 | 本轮不修改 |
| `evidence_chain.md` | 已读 A.1--A.4 | 审计证据强度、A2a 待办、`not_verified` 边界 | 证据账本目前为树级最小账本，未展开 S1--S8 逐项证据 |
| `paper.pdf` | 已做 `pdfinfo`，并用 `pdftotext -layout` 抽查 PDF 第 9 页 Fig. 2 | 核对 PDF 是 arXiv 43 页；确认 Fig. 2 中存在 `2025-Jan` 轴标 | 未做全 PDF 视觉核验，不能替代 A2a |

## 2. 关键事实复核结论

1. **原文类型**：这是 SLR + SMS 混合研究。原文明确采用 Kitchenham & Charters 指南，含 pre-review mapping、控制论文、数据库检索、纳排、PRISMA-style flow、QA、数据抽取与主题综合。
2. **样本单位**：最终被编码的样本单位是 **peer-reviewed primary studies**，用 `PS1`--`PS39` 编号。不是 LLM 工具、不是开发者、不是任务实例，也不是二级综述。
3. **分母链**：文本级可复核链条为 `9,756` 初检记录 → 去重 `803` → `8,953` title/abstract screening → 排除 `8,725` → `228` full-text screening → 全文阶段排除 `189` → 先得 `39` → snowballing 加 `5` 得 `44` → QA 排除 `5` → 最终 `39`。当前 review 的压缩写法基本成立，但 A2a 应避免把 `228 -> 44` 写成无中间过程的直接转移。
4. **年份范围存在原文内部张力**：摘要 / 贡献 / 方法多处写 `January 2014` 到 `December 2024`，但 PDF Fig. 2 横轴含 `2025-Jan`，Primary Studies 列表中也有 2025 条目（如 PS15、PS30）。A1 只能记录“作者声称 2014--2024，同时图表 / PS 列表提示 2025-Jan 需 A2a 精核”，不能把年份范围简化成无争议事实。
5. **NASA-TLX / cognitive load 必须拆分**：Table 7 的 NASA-TLX 是 6 篇 `[PS2, PS8, PS12, PS13, PS25, PS38]`；§5.3.3 又把 custom questionnaire 的 PS23 纳入 cognitive load 叙述；Table 10 的 Cognitive load 子维度列出 7 篇 `[PS2, PS8, PS12, PS13, PS23, PS25, PS38]`。因此 A1 应分清“NASA-TLX 仪器分支”和“cognitive load 概念子维度分支”，不能直接写成统一的 6/39 最终分布。
6. **混合证据有两层**：一是研究方法层的 mixed-methods（27/39，69%）；二是结果层的 mixed findings（code quality 同时作为 benefit/risk，cognitive load 方向不一致）。两者不能混用。
7. **A1/A2a 边界**：本轮可确认原生维度森林、字段来源与 S1--S8 文本级等级；但 Fig. 1、Fig. 6、Fig. 7/8、Table 9--11、Zenodo 复现包和逐 PS 字段矩阵未核，不能进入最终定量统计。

## 3. S1--S8 五分栏审计

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文将对象定义为 LLM-assistants 对 software developer productivity 的影响；RQ0--RQ3 分别覆盖研究图景、方法 / 工具、收益风险、SPACE 维度映射；作者自称 systematic review and mapping。 | 可复原为 SLR+SMS 任务根：对象 = LLM-assistants；目标构念 = developer productivity；证据对象 = peer-reviewed primary studies；解释框架 = SPACE，Discussion 另用 McLuhan Tetrad。 | **文本级强，A1 可入 schema_seed**。任务设定清晰，可作为 S1 样本；但不是目标领域 empirical finding。 | 核对 ACM final 与 arXiv v2 是否一致；核对正式年份 / DOI 元数据。 |
| S2 语料收集与筛选 | 六个数据库、检索式、2014 onward 限制、17 control papers、5 次 query iteration、IC/EC、Rayyan、title/abstract 与 full-text screening、snowballing、QA 阈值均有正文证据。 | `树-meta` 应包含 source database、query、control papers、dedup、screening status、exclusion code、snowballing source、QA status。 | **文本级强；分母链可作为 A2a 候选统计字段**。当前不得作为 final 数字，因 Fig. 1 与 supplemental 未精核。 | PDF 精核 Fig. 1；下载 / 检查 Zenodo selection decisions、exclusion rationales、control papers 与 query refinement 细表。 |
| S3 原生维度树 / 样本编码对象 | 结果表和 Primary Studies 列表均以 `PS1`--`PS39` 为主键；Table 3--11、RQ0--RQ3 均围绕 primary study 的字段与映射展开。 | 原生结构是**以 PS-id 为共享主键的多根维度森林**：RQ0 景观树、RQ1 方法 / 工具树、RQ2 benefit-risk 主题树、RQ3 SPACE 映射树；protocol / QA 是 meta-gate，Discussion / Threats 是解释与限制层。 | **文本级强**。可统计“有明确样本单位和可复原维度森林”；不能统计具体逐 PS 字段值。 | A2a 需核对 PS1--PS39 完整清单、各表 PS 映射、是否有 supplemental 字段表与正文不一致。 |
| S4 字段级证据 | §3.4 明说抽取 study goals、tools、empirical strategy/design、tasks、settings、key results；Table 5--7 给 strategy/procedure/instrument，Table 8--11 给主题 / SPACE / metrics。 | 可复原叶子包括 publication year、venue focus、tool、strategy、procedure、objective、analysis type、instrument origin/name、metric、benefit theme、risk theme、SPACE dimension/sub-dimension、quality metric。 | **建议判为中或“文本级强 / 最终统计待核”**。有字段级结构，但当前 `evidence_chain.md` 仍多为 `not_verified`，A1 不应声称逐字段矩阵已可统计。 | PDF 精核 Table 5--11；Zenodo 查原始 extraction sheet；补逐字段证据锚点与 PS-id 矩阵。 |
| S5 维度模式演化 | 原文使用外部分类法：Stol & Fitzgerald（strategy）、Glass/Vessey/Ramesh（procedure）、Hartson（formative/summative）、Lenarduzzi QA、SPACE；又用 thematic analysis 生成 benefit/risk 与 SPACE 子维度。 | 模式演化是“外部 taxonomy + emergent thematic coding + targeted iterations”。RQ1/RQ3 偏框架驱动，RQ2 偏主题归纳，最后由作者 cross-check citations。 | **文本级强，适合作为 schema evolution 样本**。但只能统计“是否有模式演化过程”，不统计演化质量。 | A2a 查 supplemental 是否有 coding version、theme merge 记录、冲突处理记录；若无，则不得升级为“有完整代码本演化日志”。 |
| S6 统计分析 | 原文大量报告频次 / 比例：strategy、procedure、mixed-methods、objective、analysis type、instrument、time-to-completion、SPACE 覆盖等；RQ2 用雷达图呈 benefit/risk 频次。 | 统计层包括单变量分布、交叉关系（strategy×procedure、strategy×instrument）、SPACE 组合、benefit/risk 主题频次、contested theme。 | **建议判为中或“文本级强 / final quantitative 暂停”**。可统计其存在统计分析，但不应导出 Fig. 6/7/8 或逐主题最终数值。 | PDF 精核 Fig. 3--8 与 Table 5--11；确认所有百分比的分母是 39、10、44 还是局部分母；核对 2025-Jan 对年份统计的影响。 |
| S7 候选 finding | RQ2 与 Discussion 形成 benefit/risk、code quality contested、cognitive load mixed、acceptance-rate caution、well-being / human-human collaboration 缺口、实践者 / 研究者 recommendations。 | 候选 finding 层应与字段统计分开：记录支持证据、反向证据、边界条件、是否 contested、是否只作方法模式启发。 | **文本级强作为 candidate_finding 机制样本**。领域结论不可迁移；不能写成“LLM 一定提高 / 降低生产力”的最终发现。 | A2a 需逐 finding 回链 Table / PS 集合 / 原文段落；code quality 与 cognitive load 必须保留反证和上下文。 |
| S8 研究者 / 作者质疑与裁决 | 原文有 all authors consensus meeting、第二与最后作者验证 excluded papers、unclear full-text 与 senior co-authors consultation、9 个月 weekly meetings、first + last author citation cross-check；但 initial screening 与 data extraction 主要由第一作者执行。 | 只可复原为“有团队复查与协商机制，但无完整 inter-rater agreement / formal adjudication log”。应放在 threat mitigation / author-gate 节点，不应写成强裁决日志。 | **中**。可统计为存在复核 / 讨论 / 保守筛选；不得统计为有独立双人编码、Kappa、一致性系数或完整冲突裁决矩阵。 | A2a 查 Zenodo / supplemental 是否提供 selection decisions、coding decisions、QA 分数与冲突记录；若没有，S8 保持中。 |

## 4. 原生维度树 / 维度森林复原

### 4.1 树型裁决

- **树型**：维度森林，不是单树。
- **共享样本单位**：`primary_study_id = PS1..PS39`。
- **主统计池资格**：原文自身具备系统综述 / 映射研究基础；但本仓库 A1 当前仅冻结 schema_seed 与候选统计字段，A2a 前不得进入 final quantitative finding。
- **解释层分离**：RQ0--RQ3 是样本编码 / 综合层；McLuhan Tetrad、Recommendations、Threats 是解释 / 风险层，不应反向当成 primary-study 字段树模板。

```text
[forest-root] LLM-assistants × developer productivity SLR+SMS
│
├── [meta-protocol] 检索、筛选与资格门禁
│   ├── database_source ∈ {ACM, IEEE Xplore, ScienceDirect, Web of Science, Scopus, Springer}
│   ├── query_segments = AI/LLM terms × developer/SE actor terms × productivity terms
│   ├── control_papers = 17
│   ├── query_iterations = 5
│   ├── screening_chain = 9756 -> 8953 -> 228 -> 39 -> 44 -> 39
│   ├── exclusion_code ∈ {EC1, EC2, EC3, EC4, EC5, ~IC1}
│   └── QA1..QA11 score ∈ {0,1,2,3,4}; threshold = 50% average
│
├── [tree-RQ0] 研究图景 / corpus characteristics
│   ├── publication_year（注意：作者声称 2014--2024，但 Fig.2/PS refs 含 2025-Jan 待核）
│   ├── author_distribution
│   ├── venue 与 venue_focus
│   └── llm_tool_used（ChatGPT、GitHub Copilot 等开放枚举）
│
├── [tree-RQ1] 方法策略 / 流程 / 工具与指标
│   ├── empirical_strategy ∈ {Field Study, Field Experiment, Experimental Simulation, Laboratory Experiment, Sample Study, Judgment Study}
│   ├── procedure ∈ {Survey, User Experiment, Case Study, Interview, Concept Implementation}
│   ├── objective ∈ {formative, summative}
│   ├── analysis_type ∈ {quantitative, qualitative, mixed}
│   ├── data_source ∈ {self-reported, behavioral/performance}
│   ├── instrument_origin ∈ {designed_by_authors, validated_framework}
│   └── instrument_or_metric
│       ├── NASA-TLX branch = [PS2, PS8, PS12, PS13, PS25, PS38]
│       ├── cognitive_load broader branch = [PS2, PS8, PS12, PS13, PS23, PS25, PS38]
│       ├── SPACE-based surveys = [PS16, PS22, PS24, PS27]
│       ├── TAM, self-efficacy, AAR/AI, emotion affect, TCQ, RBV
│       └── time-to-completion, acceptance-rate, logs, correctness, code-quality metrics
│
├── [tree-RQ2] 影响主题 / benefit-risk synthesis
│   ├── benefit_theme ∈ {accelerate development, minimize code search, automate repetitive tasks, support knowledge acquisition, support code-adjacent tasks, reduce task initiation overhead, improve code quality, support debugging/troubleshooting}
│   ├── risk_theme ∈ {fail to meet requirements, promote over-reliance/cognitive offloading, limit code quality, disrupt flow, reduce team collaboration}
│   └── contested_theme_flag：code quality 同时出现在 benefit 与 risk；cognitive load 方向也为 mixed evidence
│
├── [tree-RQ3] SPACE productivity mapping
│   ├── SPACE_dim ∈ {Satisfaction, Performance, Activity, Communication, Efficiency}
│   ├── Satisfaction_subdim ∈ {developer experience, self-efficacy, trust, cognitive load, well-being}
│   ├── Performance_subdim ∈ {quality, impact}
│   ├── Communication_subdim ∈ {human-LLM collaboration, human-human collaboration}
│   ├── Efficiency_subdim ∈ {temporal efficiency, automation, interruptions and flow}
│   └── quality_metric_examples ∈ {passing unit tests, functional correctness, code smells, BLEU, Halstead, cyclomatic complexity, translation error rate, maintainability index, cognitive complexity, defect density, defect rate, technical debt, code coverage}
│
└── [interpretive-and-validity-layer] 解释、建议与威胁（非 primary-study 字段主干）
    ├── McLuhan Tetrad ∈ {Enhance, Reverse, Obsolesce, Retrieve}
    ├── practitioner_recommendations = 5 类
    ├── researcher_recommendations = 3 类
    ├── review_method_threats ∈ {selection bias, human-centered identification, bias/repeatability, classification rigor}
    └── evidence_base_limitations ∈ {formative/controlled dominance, methodological diversity, temporal relevance}
```

### 4.2 关系边审计

| 关系 | 当前 A1 判定 | A2a 需求 |
|---|---|---|
| `PS-id -> RQ0/RQ1/RQ2/RQ3 fields` | 原文所有主结果围绕 PS 编号展开，关系成立。 | 需要逐表核 PS 集合，尤其 Table 8--10 是否完整列出所有 PS。 |
| `strategy -> procedure` | Fig. 3 / Table 5--6 支撑 strategy 与 procedure 的共现关系。 | 需 PDF 视觉核验 Fig. 3 叠加条形图。 |
| `procedure -> procedure` | Fig. 4 支撑 mixed-methods overlap，最常见 user experiment + survey。 | 需核 UpSet 图数值；当前只可文本级记录。 |
| `strategy -> instrument` | Fig. 5 支撑高控制研究更多用 behavioral/performance metrics，field/sample 更依赖 self-report。 | 需核 Sankey 图；不可提前导出具体流量。 |
| `benefit -> risk contested` | code quality 同时在 benefit 与 risk，原文明确解释为 context / metric / task 差异。 | 需要逐 PS 支撑与反证矩阵。 |
| `NASA-TLX -> cognitive load` | NASA-TLX 是 instrument 子集；cognitive load 是更宽 SPACE sub-dimension。 | 必须拆分 PS23 custom questionnaire 与 PS25 NASA-TLX outcome；不要合并成一个 6/39 final 结论。 |
| `SPACE_dim -> SPACE_subdim` | Table 10 支撑层级关系；Activity 无进一步子维度。 | 核 Table 10 与 Fig. 7/8；确认 well-being 0/39。 |

## 5. 对当前 review / evidence_chain / SUMMARY 的 C/I/M 清单

### C / Critical

- **暂无必须立即阻断的 C 级问题**。在当前文本明确保留 A2a 待核、`schema_seed` 与非 final quantitative 边界的前提下，尚未看到会直接破坏本仓库学术结论的错误。若后续把本 A1 结果直接写入 final empirical finding，则应升级为 C。

### I / Important

1. **NASA-TLX 与 cognitive load 分支需要拆分返修**
   - 影响对象：`review.md` 维度树叶子表、S1--S8 S4/S6/S7，必要时 `SUMMARY.md` S1--S8 覆盖矩阵。
   - 问题：当前归纳容易写成“6 studies NASA-TLX，3 improved / 2 neutral / 1 worse”。但原文 Table 7 的 NASA-TLX 是 6 篇 `[PS2, PS8, PS12, PS13, PS25, PS38]`；§5.3.3 的 improved 列表含 PS23（custom questionnaire）且未交代 PS25 方向；Table 10 cognitive load 是 7 篇。
   - 建议：A1 中改为“NASA-TLX instrument branch = 6；broader cognitive-load SPACE sub-dimension = 7；outcome polarity 待 A2a 精核”。不要在 SUMMARY 中写最终方向比例。

2. **年份范围需要显式记录原文内部不一致 / 待核验**
   - 影响对象：`review.md` 快速卡、维度树 `leaf-pub-year`、`SUMMARY.md` 文献总表与 S1/S2 行。
   - 问题：摘要与方法写 2014--December 2024，但 PDF Fig. 2 含 `2025-Jan`，Primary Studies 列表有 2025 条目。当前如果只写“2014--2024”会掩盖原文张力。
   - 建议：写成“作者声称检索 / 抽取截至 2024 年底；图表 / PS refs 出现 2025-Jan，A2a 需确认是否 online-first、accepted paper 或出版年份归档差异”。

3. **S4/S6 的等级在 SUMMARY 中应避免被误读为 final 强证据**
   - 影响对象：`SUMMARY.md` S1--S8 覆盖矩阵；`review.md` S1--S8 第一张表。
   - 问题：`review.md` 五分栏已有“文本级强；最终统计暂缓”说明，但 SUMMARY 行只显示“强”，读者可能误认为逐字段矩阵和图表数值已可统计。
   - 建议：SUMMARY 中将 S4/S6 写成“强（文本级；A2a 表图 / supplementary 待核）”或降为“中：字段级结构强、最终统计待核”。

4. **分母链应展开 `228 -> 39 -> +5 -> 44 -> -5 -> 39` 的中间语义**
   - 影响对象：`review.md` 维度树、S2 五分栏、`evidence_chain.md` denominator 证据。
   - 问题：压缩链 `9756 → 8953 → 228 → 44 → 39` 虽不算错，但会隐藏全文筛选先得到 39、snowballing 加 5 后 QA 的过程。
   - 建议：在树 / evidence 中保留中间节点与每个节点动作，避免后续 agent 把 snowballing 与 full-text screening 混为一类筛选。

5. **`evidence_chain.md` 目前不足以承载 S1--S8 最终证据链**
   - 影响对象：`evidence_chain.md` A.2/A.3。
   - 问题：当前 A.2 多数是树级泛证据，强度 `not_verified`，且大量写“短引见 review.md”。这适合 A1 最小账本，但不够支撑 S1--S8 的 final quantitative 或逐字段统计。
   - 建议：A2a 时新增 S1--S8 或关键叶子级证据，至少覆盖 Fig. 1、Table 5--11、Fig. 6--8、Threats、Zenodo artifacts。

6. **混合证据需分清 mixed-methods 与 mixed findings**
   - 影响对象：`review.md` RQ1/RQ2、S6/S7、SUMMARY 归纳。
   - 问题：69% mixed-methods 是研究设计属性；code quality / cognitive load mixed findings 是结果方向属性。两者在后续 pattern 命名中若都叫“mixed evidence”会混淆。
   - 建议：分别命名为 `mixed_methods_design` 与 `mixed_outcome_or_contested_finding`。

### M / Minor

1. **术语中文化可再稳一点**：`Field Study`、`Sample Study`、`Judgment Study` 等建议在树中保留英文枚举同时补中文解释，避免后续 agent 误译。
2. **A1-M0--M6 与 S1--S8 的边界可再显式**：当前 review 已大体分离；建议在后续返修中再提示 A1-M 是跨论文投影，S1--S8 是本目录二级编码，不是目标领域结论。
3. **PDF 核验记录可更具体**：A2a 时在 A.4 写明每个待核图表 / 表格页码，而不是只写“Table 1--11、Fig. 1--9”。

## 6. 本轮审计结论

- 本文是高价值 SLR+SMS 样本，S1--S8 覆盖度高；S1/S2/S3/S5/S7 文本级证据较强，S4/S6 有强结构但 final 数值待 A2a，S8 应保持中。
- 原生维度结构应维持“PS-id 主键 + 多根 RQ 维度森林 + 解释 / 威胁层分离”。
- 最需要返修或至少加注的是：NASA-TLX 与 broader cognitive load 分支拆分、2014--2024 vs 2025-Jan 年份张力、S4/S6 在 SUMMARY 的强度口径、分母链中 snowballing/QA 的中间节点、evidence_chain 的 S1--S8 证据粒度。
