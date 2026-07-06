# A1 survey-of-surveys 单篇审计：re-tertiary-study-2014

> 角色：A1 survey-of-surveys 单篇维度抽取 subagent（round3）。
> 范围：仅处理 `papers/re-tertiary-study-2014/`；未开启 sub-subagent；本文件只作为独立审计输入，不是 final quantitative finding。
> 输出文件：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1-s1s8-19x1/round3/re-tertiary-study-2014.md`。

## 0. 执行约束与阅读状态

- 已读并遵循：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`survey_of_surveys/GUIDE.md` §6.3/§6.4。
- 已读本篇：`bibtex.bib`、`metadata.json`（辅助核对）、`paper_content.txt` 全文、`review.md`、`evidence_chain.md`。
- 未打开 `paper.pdf` 逐项视觉核对：本轮在 20 分钟约束下完成文本级 A1 审计；Figure 1--4、Table III--VI、Appendix A 的版面对齐与页码仍列入 A2a。
- 证据纪律：本文所有数字只按“原文文本级统计观察 / A2a 候选”使用；不得直接写成 Paper2 final quantitative finding。

## 1. 全文阅读依据

### 1.1 元数据与出版信息

- `bibtex.bib`：`@inproceedings{Bano2014RETertiary}`；Bano、Zowghi、Ikram；EmpiRE 2014；pp. 9--16；DOI `10.1109/EmpiRE.2014.6890110`。
- `metadata.json`：出版形态为工作坊；综述类型为 `tertiary study`；当前入账为 schema seed 与后续主统计池候选。

### 1.2 `paper_content.txt` 覆盖范围

| 原文范围 | 本轮阅读用途 |
|---|---|
| L23--40 摘要 | 确认 RE tertiary 任务、53 distinct systematic reviews、64 publications、质量与 coverage/gap 主结论。 |
| L57--79 | 确认 conventional SLR / systematic mapping / tertiary study 的原文定义边界。 |
| L108--123 | 确认 §II 标题、protocol 与 RQ1--RQ3。 |
| L125--146 | 确认 topic grouping、quality of SLR 与 quality of publications 的区别；QA 以 study 为单位，不以每篇 publication 为单位。 |
| L147--178 | 确认 QA1--QA4 三档量规：Yes=1、Partial=0.5、No=0。 |
| L179--183 | 确认 citation/impact 使用 Google Scholar citation count，截止日为 2014-05-19。 |
| L184--230 | 确认 search string、5 个数据库、snowball/manual search、三项纳入标准。 |
| L231--247 | 确认多 publication 合并到同一 study ID，以及抽取字段：publication details、citation、#PS、focus、topic thematic analysis。 |
| L249--288 | 确认 Table II funnel：267→91→58→64 publications→53 studies；正文“5 SLR”与表格/最终算术“+6 publications”存在口径差异。 |
| L290--314 | 确认 S3/S8 全文不可得、S40 publication channel unknown、12 SMS + 1 meta-analysis + 其余 SLR。 |
| L317--331 | 确认 publication type 分布：31 conference、16 journal、4 workshop、4 technical reports、8 theses、1 unknown。 |
| L332--375 | 确认 scope 分类：state-of-the-art 33、methods 7、techniques 7、tools 4、frameworks 1、technology 1。 |
| L376--429 | 确认 Table V topic group / focus / #PS / year；`NM`、`NF` 与 S26/S39 overlap 注脚需 A2a 复核。 |
| L433--493 | 确认 QA 分母 51、42/51 ≥ 2、QA3/QA4 问题、Top-10 citation/QA table；Figure 2--4 需视觉核验。 |
| L494--576 | 确认 RQ3 gap taxonomy：anomalies、lack of primary studies、ignored RE areas，以及 RE roadmap 对照。 |
| L577--615 | 确认 limitations：检索漏检风险、S40 缺 publication details、topic grouping 主观、QA guideline 依赖、gap analysis preliminary。 |
| L616--645 | 确认 conclusion/future work：53/64、replication need、QA attention、RE roadmap / bibliography future work。 |
| L697--966 | 确认 Appendix A S1--S53 名录与 publication citation 入口；OCR 中部分 S-ID 断行，A2a 需核对 PDF。 |

### 1.3 现有 `review.md` / `evidence_chain.md` 阅读结论

- `review.md` 已包含较完整的“维度树复原”和 S1--S8 小节；主干判断基本可信，但早期“快速结论卡片 / 六类 pattern”仍残留若干旧口径和过粗表述。
- `evidence_chain.md` 已有 A.1--A.4 最小证据链，但 A.2 多数证据仍是泛定位 / `not_verified`；这与 A1-DT v2 的 A2a 接力边界一致，但若要支撑 S1--S8 汇总，应补更细的文本行号、表图与 S 维度 claim。

## 2. 总体审计结论

1. 本文是一个 **Requirements Engineering 领域 tertiary study**，而不是 primary-study SLR；样本单位必须优先写成 **53 distinct SLR / SMS / meta-analysis studies**，同时单独保留 **64 publications** 作为 publication-level 分母。
2. QA 评价不是 64 publications，也不是 53 全部 studies，而是 **51 studies**：S3、S8 因全文不可得未进入 QA。
3. 原生结构不是单棵通用树，而是围绕 RQ1--RQ3 的 **维度森林**：publication metadata、study-level extraction、topic group、scope、QA rubric、citation/impact、gap taxonomy、publication type、search funnel 与 limitations / researcher challenge。
4. `topic group`、RE roadmap gap、scope 的具体取值都是 **RE-specific**；只能作为“领域专门化 tertiary 如何编码 topic/gap”的方法样本，不能直接迁移为 Paper2 通用枚举。
5. 现有文字可支持 S1、S2、S3、S6、S7 的强文本级候选；S4 因表图 / 附录 / 样本级精核未完成应保持中等；S5、S8 因没有完整 codebook evolution / adjudication log，应保持中等。

## 3. S1--S8 五分栏证据拆分

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定（强） | 摘要和引言说明本文按 EBSE guidelines 对 RE 相关 SLR 做 tertiary study；§II.A 明确 RQ1=covered RE areas、RQ2=quality、RQ3=gaps。文本位置：L23--40、L80--99、L108--123。 | 根任务是“RE SLR 的三级映射 / tertiary overview”；RQ1 驱动 topic/scope，RQ2 驱动 QA/citation，RQ3 驱动 gap taxonomy。 | 可作为 tertiary-review task / RQ-tree 的强文本级候选；不得外推为 Paper2 领域发现。 | PDF 标题、摘要、§II 标题与 RQ 原文页码；确认 “Systematic Mapping Tertiary Study” 与 tertiary study 的版面表述。 |
| S2 语料收集与筛选（强，含口径差异） | 原文给出 5 个数据库、snowball、manual venue scan、三项纳入标准；Table II 给 `267→91→58→64 publications→53 studies`。正文称 secondary searches found 5 SLR，但 Table II/final arithmetic 表示 +6 publications。文本位置：L184--230、L249--288。 | 检索漏斗必须分两层：publication-level funnel 与 distinct-study corpus；纳入标准为 English + SLR/SMS/meta-analysis + RE focus。 | 可作为语料构造强候选，但必须保留“5 SLR vs +6 publications”的内部口径差异；不能把 64 publications 与 53 studies 混算。 | 视觉核 Table II 六行 secondary search、正文 “5 SLR” 与表格 “6” 的差异；核对 S3/S8/S40 缺失说明。 |
| S3 原生维度树 / 样本编码对象（强） | 原文说明多 publication 用同一 study ID 加 A/B/C 后缀；抽取 publication details、citation、#PS、focus；Table III--VI 和 Appendix A 提供 publication type、scope、topic/#PS、citation/QA、S1--S53。文本位置：L231--247、L249--253、L290--331、L364--429、L482--493、L697--966。 | 主对象是 distinct SLR study；另有 publication-level 子对象。维度森林含 F1 publication metadata、F2 study extraction、F3 topic group、F4 scope、F5 QA、F6 search funnel、F7 gap taxonomy、F8 limitations / challenge。 | 可作为原生维度森林强候选；叶子取值进入统计前需 A2a。 | Appendix A 的 S-ID / A/B/C 分组、Table III--VI 是否跨页漏列、OCR 断行与 `NM/NF`。 |
| S4 字段级证据（中） | Table I 明确 QA1--QA4；Table III--VI 给 publication type / scope / topic/#PS/year / citation+QA；Appendix A 给完整 reference 与 citation。文本位置：L147--178、L317--331、L364--429、L482--493、L697--966。 | 可复原字段包括 title、authors、year、publication type、venue/channel、citation、S-ID、review subtype、#PS、focus、topic group、scope、QA1--QA4/total、gap type、limitation。 | 字段结构可进入候选 schema；但当前只为文本级，数值表、figure 与样本级映射不得升级为 final quantitative evidence。 | 核对 Table I--VI、Appendix A 列名和数值；尤其 Figure 2--4、Table V `NM/NF`、S26/S39 overlap 星号、Top-10 citation/QA。 |
| S5 维度模式演化（中） | 作者说明搜索词经过 pilot testing，并参考既有 tertiary studies / RE SLR 扩词；topic 从 title/abstract 抽取，第一作者分组命名，另外两位作者复核同意最终名称。文本位置：L184--190、L239--247、L594--600。 | 维度形成过程是“关键词扩展 + thematic analysis + topic-name review”，不是完整开放编码、codebook versioning、饱和度分析或冲突日志。 | 可作为维度形成机制的中等候选；不宜并入“完整 codebook evolution”强统计池。 | 核对 §IV topic grouping 段；确认没有被 OCR 漏掉的 protocol appendix / coding agreement。 |
| S6 统计分析（强，文本级） | 原文给 publication type、study subtype、scope、#PS 极值 / 区间、QA 分布、year trend、Top-10 citation。文本位置：L300--314、L317--331、L332--363、L364--429、L433--493。 | 统计由字段森林派生：64 publication 分布、53 study subtype、51 QA 分母、scope 分布、topic/#PS、citation/impact、year trend、gap observations。 | 强文本级候选；A2a 前只能写“原文报告 / 文本级可复核”，不得作为 Paper2 final quantitative finding。 | Figure 1--4 柱高 / 曲线、Table IV--VI 数值、`42/51 ≥ 2`、#PS 极值与 Top-10 citation/QA。 |
| S7 候选 finding（强，限 RE 语境） | RQ3 明确三类 gap；discussion/conclusion 提出 QA 下降、QA3/QA4 被忽略、#PS anomaly、low #PS 可能原因、ignored RE areas 与 replication need。文本位置：L433--479、L494--576、L616--635。 | finding 应拆成：统计观察、作者解释、RE roadmap 对照、replication / QA attention 建议。具体 RE topic 名单是领域事实，不是 Paper2 通用枚举。 | 可作为“字段→candidate finding / gap taxonomy”的强方法样本；不迁移具体 RE 结论。 | 核对 RQ3 三类 gap、Cheng/Atlee 与 Nuseibeh/Easterbrook roadmap 对照、Conclusion 中 replication/QA 建议。 |
| S8 研究者 / 作者质疑与裁决（中） | §IV limitations 记录检索漏检、S40 元信息缺失、topic grouping 主观、QA guideline 依赖、gap analysis 不完整；topic 命名由第一作者分组，另两位作者复核同意。文本位置：L577--615、L594--600。 | 可复原为“作者自我质疑 + topic naming review”；没有完整多研究者独立筛选 / 抽取 / QA 裁决、disagreement resolution、inter-rater agreement 或 kappa。 | 中等候选；不能按完整 adjudication / coding reliability 统计。 | 核对是否有未进入 OCR 的 threats-to-validity / protocol 细节；确认无双人独立筛选、抽取或 QA 裁决日志。 |

## 4. 原生维度树 / 维度森林

```text
根：RE systematic reviews tertiary study（样本库：53 distinct SLR/SMS/meta-analysis studies；publication 分母：64）
│
├── F0 任务与 RQ 层
│   ├── RQ1：RE 中哪些主要研究领域已有 SLR 覆盖？
│   ├── RQ2：RE SLR 的质量如何？
│   └── RQ3：RE SLR 覆盖中有哪些 gap？
│
├── F1 Publication-level metadata（分母 = 64 publications）
│   ├── title / authors / year / complete reference
│   ├── publication type ∈ {conference, journal, workshop, technical report, thesis, unknown}
│   │   └── 原文计数：31 / 16 / 4 / 4 / 8 / 1；S40 = unknown
│   ├── publication channel / venue
│   ├── Google Scholar citation count（cut-off = 2014-05-19）
│   └── S-ID suffix：同一 study 的多份 publication 用 [A] / [B] / [C] 区分
│
├── F2 Distinct study extraction（分母 = 53 studies）
│   ├── study ID ∈ {S1 ... S53}
│   ├── review subtype ∈ {conventional SLR, systematic mapping study, meta-analysis}
│   │   └── 原文报告：12 SMS + 1 meta-analysis + 其余 conventional SLR
│   ├── # of primary studies ∈ integer ∪ {NM, NF}
│   ├── focus of SLR（自由文本）
│   └── study/publication availability status：S3/S8 full source unavailable；S40 channel unknown
│
├── F3 Search / selection funnel（聚合层；不是每个 study 的字段）
│   ├── sources ∈ {Google Scholar, IEEE Xplore, ACM DL, Science Direct, EI Compendex,
│   │              references of previous tertiary studies, REJ, ESE, RE/EASE/ESEM/REFSQ/IST manual scan}
│   ├── selection criteria ∈ {English, SLR/SMS/meta-analysis, RE focus}
│   └── funnel：267 found → 91 passed → 58 after duplicates → 64 publications → 53 studies
│       └── caveat：正文 “5 SLR” vs table/arithmetic “+6 publications”
│
├── F4 Topic group layer（RE-specific；非封闭通用枚举）
│   ├── topic group 来自 title/abstract thematic analysis
│   ├── 观察到约 24 个 RE topic group，例如 Non Functional Requirements、Complete RE Process、
│   │   Model Driven Development、Knowledge Management and RE、RE in GSD、Requirements Prioritization 等
│   └── overlap：S26/S39 同时与 Knowledge Management and RE / RE in GSD 相关
│
├── F5 Scope layer（RE-specific scope；分母 = 53 studies）
│   └── scope ∈ {state of the art within RE, methods, techniques, tools, frameworks, technology}
│       └── 原文计数：33 / 7 / 7 / 4 / 1 / 1
│
├── F6 QA rubric layer（分母 = 51 studies；S3/S8 excluded）
│   ├── QA1 inclusion/exclusion criteria ∈ {Yes=1, Partial=0.5, No=0}
│   ├── QA2 search space adequacy ∈ {Yes=1, Partial=0.5, No=0}
│   ├── QA3 quality assessment of primary studies ∈ {Yes=1, Partial=0.5, No=0}
│   ├── QA4 information regarding primary studies ∈ {Yes=1, Partial=0.5, No=0}
│   └── total QA score ∈ {0, 0.5, ..., 4}
│
├── F7 Citation / impact layer
│   ├── Google Scholar citation count per publication（2014-05-19）
│   ├── Top-10 highly cited SLR table: S-ID × citations × publication channel × QA score
│   └── relation：publication-level citation impact ≠ study-level QA score
│
├── F8 Gap taxonomy layer（candidate finding；RE 语境）
│   ├── gap type ∈ {anomaly in #PS, lack of primary studies, ignored RE areas}
│   ├── anomaly 例：同一主题不同 SLR 的 #PS 差异；state-of-the-art 与子主题 #PS 不一致
│   ├── lack-of-PS 例：低 #PS 可能来自检索不足或该 RE 子领域确实缺少 empirical studies
│   └── ignored areas：与 RE roadmaps [Nuseibeh & Easterbrook 2000; Cheng & Atlee 2007] 对照
│
└── F9 Researcher challenge / limitation layer
    ├── search completeness risk
    ├── S40 publication details missing
    ├── topic grouping subjective naming risk
    ├── QA rubric depends on EBSE/DARE criteria quality
    └── gap analysis preliminary and non-exhaustive
```

### 4.1 可迁移与不可迁移边界

| 项 | 可迁移到 Paper2 schema 的层面 | 不可直接迁移的层面 |
|---|---|---|
| 53 studies / 64 publications 分层 | 可迁移为“study-level vs publication-level”去重/分母纪律。 | 不可把 RE 的 53/64 数字作为 Paper2 经验事实。 |
| QA rubric | 可迁移为 tertiary/SLR 质量评估的候选量规结构。 | 不可未经裁定就当成所有 Paper2 样本的唯一质量评分标准。 |
| topic group | 可迁移“由 title/abstract thematic analysis 形成领域 topic group”的方法。 | RE-specific topic 名单不能成为 LLM/state-machine 通用枚举。 |
| scope | 可迁移“scope as study-intent classification”的思路。 | state-of-art/methods/techniques/tools/frameworks/technology 这 6 档是 RE 语境，不应机械套用。 |
| citation/impact | 可迁移 citation snapshot、cut-off date、impact-vs-quality 分离。 | 2014-05-19 Top-10 citation 名单已过时，不能作为当前 impact 事实。 |
| gap taxonomy | 可迁移 anomaly / lack-of-evidence / ignored-area 的 gap 形成机制。 | RE roadmap topic 和 RE gap 名单不能外推。 |
| publication type | 可迁移 publication-type 分层和 unknown 明示。 | 不能把 EmpiRE/workshop 分布当作目标领域出版结构。 |

## 5. 需修改 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 清单

> 说明：本表是 A1 文本级审计提出的返修建议；本轮按用户要求不修改这些文件。

| 等级 | 目标文件 | 问题 | 影响 | 建议修改 |
|---|---|---|---|---|
| C | -- | 未发现必须立即阻断的 final quantitative finding 写法；现有 `SUMMARY.md` 中统计池表述总体仍写作候选。 | -- | 保持“候选 / A2a 待核验 / 不进入 final quantitative finding”防线。 |
| I | `papers/re-tertiary-study-2014/review.md` | 快速结论卡片中“是否目标证据池：否”与后文“后续主统计池候选”容易冲突。 | 后续 agent 可能误判该篇完全不属于统计池，或把“非目标领域证据”与“主统计池候选”混淆。 | 改成“非目标领域 final finding；是 survey-of-surveys 后续主统计池候选（A2a 前仅 schema_seed）”。 |
| I | `papers/re-tertiary-study-2014/review.md` | 旧“六类 pattern 抽取”仍写“当前只读摘要级结果”“threat section 未完整定位”等旧状态，但后文已全文阅读并定位 limitations。 | 同一 `review.md` 内存在第二事实源，削弱证据链一致性。 | 将旧 pattern 表标注为历史摘要或压缩改写；以“维度树复原”和 S1--S8 为唯一当前事实入口。 |
| I | `papers/re-tertiary-study-2014/review.md` | `leaf-orig-search-source` 写“secondary 找到 6 篇（占 9.4%）→ 单一检索口径不充分”，但正文同时有“5 SLR”口径。 | 若不显式区分 +6 publications vs +5 SLR，会污染分母链。 | 在叶子表中改为“+6 publications / 正文称 5 SLR，需 A2a 核验”；占比只保留为候选，不作统计结论。 |
| I | `papers/re-tertiary-study-2014/evidence_chain.md` | A.2 只保留树级泛证据，缺少 S1--S8 对应的细粒度证据标识和行号；许多行写“短引见 review.md”。 | S1--S8 被 SUMMARY 引用时，证据链回链不够直接，后续 A2a 难以逐项升级。 | 增补 `ev-...-s1` 到 `ev-...-s8` 或等价证据组，至少给出 paper_content 行号、表图、是否需 PDF 核验。 |
| I | `SUMMARY.md` | S1--S8 覆盖矩阵中 S2/S6/S7 若只写“强”而不压缩呈现分母差异和 A2a 图表核验边界，容易被误读为最终可统计。 | 可能违反 GUIDE §6.4 “S1--S8 不直接写成 Paper2 最终 empirical finding”。 | 在对应行短语中补“文本级强；64 publications / 53 studies / QA 51；Figure/Table 待 A2a”。 |
| M | `papers/re-tertiary-study-2014/review.md` | “education_practice_relevance / 教育/实践影响字段”表述略偏离本文原生主轴。原文主要说 future RE researchers、doctoral students、roadmap 与 bibliography。 | 轻微概念漂移，可能让后续 schema 加入无充分依据的 field。 | 改为“future researcher relevance / roadmap impact / citation impact”，若保留 education/practice，应标为作者展望而非字段。 |
| M | `papers/re-tertiary-study-2014/review.md` | scope 6 档中的 `Techniques` 与 `Technology` 中文都接近“技术”，容易混淆。 | 可读性风险。 | 保留原文英文枚举，并中文注释为“技术方法（techniques）”与“单数技术/technology”。 |
| M | `papers/re-tertiary-study-2014/evidence_chain.md` | A.1/A.4 表头与 GUIDE 模板有轻微差异（如“文件 / 链接”“命令 / 人工核验动作”）。 | 不影响当前审计，但可能影响脚本化门禁。 | 后续统一成 GUIDE §6.3.7 的正式中文宽表表头。 |
| M | `SUMMARY.md` | 总表“RE 子领域 tertiary，验证 target SE subfield、topic taxonomy、教育/实践影响字段”可更精确。 | 轻微摘要偏差。 | 改为“验证 study/publication 分母、RE-specific topic grouping、QA rubric、citation/impact、gap taxonomy 与 publication type 的分层边界”。 |

## 6. 本轮不足与接力

1. 未视觉核对 `paper.pdf`；所有 Table / Figure 数字仍为 `paper_content.txt` 文本级证据。
2. Appendix A 的 S-ID 断行较多，无法在本轮保证 64 publications → 53 studies 的全部映射逐项无误。
3. 当前审计不改 `review.md`、`evidence_chain.md`、`SUMMARY.md`；上表 C/I/M 只作为主线程回填和 A2a 精核输入。
4. 本文可以作为 Paper2 方法 schema 的强样本，但只能贡献“如何分层和编码 tertiary study”的方法模式；不能贡献 LLM 状态机建模领域的最终定量结论。
