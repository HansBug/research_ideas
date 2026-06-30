# research-artifacts-secondary-studies · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex
- 是否读取 `$ai-research-writing-skill`：是；已读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。本审计按 claim-evidence、reviewer gate、unsupported claim 降级口径执行。
- 是否读取 `$research-planning`：是；已读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。本审计按“严格跟随原文 RQ / 方法 / 分析设定，缺失处显式标注”执行。
- 是否读取 `$oh-my-codex:autoresearch`：是；已读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本审计按 validator-gated artifact 口径输出 pass/fail、证据与修复项。
- 是否完整阅读 `paper_content.txt`：是；已从 Page 1 摘要 / 引言读到 Page 6 references，覆盖 objective、四个 RQ、Methods、Table 1、Limitations、Conclusion / Future work、Data availability。
- 是否核对 `paper.pdf`：是；使用 `pdfinfo` 确认 6 页 PDF，并用 `pdftoppm` 导出第 3 页后视觉核对 Table 1 的三段结构、列名、分母和回归表。未打开 Zenodo DOI 内部文件清单。

## 2. 原文真实结构复原

- 原文 RQ / 目标 / 贡献声明：
  - 目标：评估软件工程 secondary studies 如何报告 research artifacts，并提供 artifact 可获得性图景。摘要明确对象为 537 篇 2013--2023 年 secondary studies，关注 artifact availability 与 reporting。
  - RQ1：多少 secondary studies 包含 research artifact。
  - RQ2：research artifacts 存放在哪里，尤其是否使用带 DOI 的 permanent repository。
  - RQ3：artifact / data availability 如何在论文中陈述，尤其是否有 dedicated section。
  - RQ4：publication year 与 publication forum 如何影响 artifact availability。
  - 贡献边界：原文统计“有无、位置、报告方式、趋势和 venue 差异”，没有在正文中评估 artifact 内容质量，也没有给出细粒度 artifact type taxonomy。

- 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式：
  - 方法类型：systematic mapping，声明遵循 Petersen et al. guidelines 与 SIGSOFT Empirical Standards checklist。
  - 检索：2024-10-02 使用 Scopus；搜索式由 15 个 ISSN 约束 publication channels，并用 title 关键词覆盖 mapping study、systematic review、meta-analysis、scoping review、critical review 等；年份为 2013--2023；初始 643 篇。
  - 纳排：IC1 2013--2023、IC2 secondary study、IC3 SE-related。ACM Computing Surveys 与 Computer Science Review 需人工判断 SE 相关性；Krippendorff’s Alpha 为 0.776；最终 537 篇。
  - 数据抽取 / 编码：两轮。第一轮人工 full-text screening，识别 dedicated sections indicating artifact availability；第二轮 Python keyword search 打印每个命中前后 100 字，再人工检查。编码判断包括是否引用外部资源、外部资源是否在 Zenodo / Figshare / Mendeley Data 等 permanent repository。
  - 统计：Table 1a 按 venue 统计 Total / Yes / Permanent repo / No / By Request / Dead Link；Table 1b 按 year 统计 Yes / No / By request / Dead / Permanent repo / Dedicated section / Total；Table 1c 用 binary logistic regression 建模 artifact availability，predictors 为 publication year 与 journal，TSE 为 reference category，少于 10 篇样本的 journals 排除。
  - finding 形成：字段计数与比例先形成 statistical observations，再在 conclusion 中形成 gap / recommendation：artifact availability 增长但仍不足，permanent repository / DOI 使用不足，Data Availability section 不等于真实 artifact，upon request / no data used 对 secondary studies 不充分，journals 应 enforce artifact reporting。

- 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric：
  - 显式 evidence table / model：Table 1 是主 schema 证据，包含 venue 统计、year 统计和 logistic regression。
  - 显式 extraction / coding scheme：正文给出人工 full-text screening、keyword search、100-character context、manual check、external resource 与 permanent repository 判断；更完整细节在 Zenodo artifact，当前未核验。
  - 显式 classification schema：artifact availability 状态至少包括 Yes、No、By request、Dead link；permanent repo 是 Yes 子集 / 持久性属性；dedicated section 是 reporting anchor，不等价于 artifact availability。
  - 显式 quality / validity：没有对 included secondary studies 或 artifacts 做内容质量评分；只报告 selection reliability、scope limitations，并把 artifact quality 作为 future work。
  - 显式 roadmap figure：无。

- 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation：
  - RQ1 从 169 / 537 = 31.5% 得出 artifact availability 基线。
  - RQ2 从 65 / 169 = 38.5% 与 65 / 537 = 12.1% 得出 permanent repo / DOI 不足。
  - RQ3 从 dedicated section 统计与 discussion 中 no data used / upon request 例子得出“报告位置不等于真实可复现资产”。
  - RQ4 从 year ordered factor odds ratio 2.31 和 journal coefficients 得出 adoption 随时间显著提升、部分 venue 相对 TSE 更低的统计观察。
  - Conclusion 把这些观察降级为实践建议：mandatory artifact publication、permanent DOI repository、data availability section；并明确 future work 是 artifact quality。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但单位对象有错误 | `review.md` 第 218 行把单位对象写成 `primary study / secondary study`；原文对象是 SE secondary studies，不是 primary studies。根类型“证据资产审计树 / artifact availability 统计树”是合理的。 | M |
| 主干分支是否覆盖原文 schema | 未充分覆盖 | 当前正式主干为 corpus / artifact type / availability / repository DOI / reproducibility gap，但没有把 RQ1--RQ4 对应的 availability、storage / permanent DOI、reporting anchor、year / venue effects、limitations 组织成主干；且 `artifact type` 在正文并无显式分类表支撑。 | I |
| 叶子维度是否足够具体 | 不足 | 第 241--246 行正式叶子仍是 scope、corpus、taxonomy、method、evidence、finding 六个通用接口。第 212 行虽声明这不是原文 leaf 全集，但事实真源的叶子表没有展开 Table 1 列、search / selection / extraction coding 字段和 regression 字段。 | I |
| 取值空间是否可执行 | 部分可执行，但关键取值空间缺失或位置错配 | 第 254--259 行候选叶子列出 availability、repository、reporting、link health、artifact content、trend context，但仍是 A1 种子，未给出每个字段的分母、闭合枚举、缺失语义和统计资格。`artifact_content` 中 search_strategy / extraction_table 等更像 Paper2 期望字段或 Zenodo 待核验内容，不应写成已复原的原文 schema。 | I |
| 关系边是否缺失 | 缺失关键原文关系 | 第 265--266 行关系边是通用 method-evidence 与 taxonomy-finding。原文关键关系应包括 availability status → permanent repo 子集、dedicated section ↛ true artifact 的非蕴含关系、year / venue → availability regression、scope limitations → conclusion 外推边界。 | I |
| 统计用途 / 分母是否正确 | 正文说明较好，正式树不足 | 第 75--80 行正确记录 537、169、79 等分母；第 103 行也提醒 Table 1 分母切换。但第 270--274 行正式统计链路只写“当前 19 篇样本 / 本文纳入样本或分类表”，没有把原文 537 总分母、169 artifact 子分母、65 permanent repo、72 dedicated section、79 篇 2023 子分母与 logistic regression 样本规则结构化。 | I |
| 候选 finding 路径是否完整 | 有方向但不完整 | 第 71、79--80、188--193 行已经指出趋势、持久性缺口和 Data Availability 误导风险；但维度树的正式 finding path 没有绑定 RQ1--RQ4、Table 1a--c、limitations 和 recommendation，导致 A2a 难以复验“统计观察 → gap → recommendation”。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，证据粒度不足 | A.1 有 pdf/text/bib，但缺 `metadata.json`、Zenodo DOI、PDF page 3 visual Table 1 核验记录；A.2 全部用泛定位和“见释义”，证据强度均为 `not_verified`，符合降级纪律但不足以支撑完整维度树复原；A.4 仍显示 visual check `needs_manual_check`，与快速卡片“已用 PDF layout 文本核对”存在轻微不一致。 | I |
| 是否存在可能误导 A2a 的强主张 | 有中等风险，但已被部分降级语缓解 | 第 212 与第 250 行明确说通用 leaf 不是原文 schema、候选叶子 `not_verified`，这避免了 C 级误导。但第 208 行仍称“本文的维度树”已复原，第 241--246 行正式叶子过泛，可能让 A2a 以为修复只需补页码，而不是重建原文 schema。 | I |

## 4. 建议维度树骨架

当前 review 未足够忠实于原文；建议把“六个通用接口”降为跨论文检查视图，把以下树作为该单篇 `维度树复原` 的主事实源。

| 节点 / 叶子 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| [dim-ras-root] SE secondary-study research artifact reporting | -- | 根对象：SE secondary study × research artifact reporting / availability | 是，原文分母 537；A1-DT 当前仅 schema_seed | not_applicable | 摘要；Methods；Results RQ1--RQ4 |
| [dim-ras-rq] RQ-driven audit schema | [dim-ras-root] | RQ1 availability；RQ2 storage / permanent DOI；RQ3 reporting statement；RQ4 year / venue effects | 是 | not_reported if RQ absent | Results RQ1--RQ4 |
| [leaf-ras-unit] study unit | [dim-ras-rq] | secondary study；not primary study | 是 | not_applicable | IC2 与 final 537 |
| [leaf-ras-availability-status] artifact availability status | [dim-ras-rq] | Yes / No / By request / Dead link | 是；venue × status、year × status | not_checked；ambiguous_link；not_reported | Table 1a / 1b；Data extraction |
| [leaf-ras-permanent-repo] permanent repository / DOI | [dim-ras-rq] | true / false / not_applicable；provider examples Zenodo / Figshare / Mendeley Data；DOI present / absent | 是；分母可为 169 artifacts 或 537 all studies | no_artifact；not_permanent；not_verified | RQ2；Data extraction；Table 1 |
| [leaf-ras-reporting-anchor] dedicated availability section | [dim-ras-rq] | dedicated section present / absent；section says repository link / no data used / upon request / unclear | 是；分母 537 和 169 需分开 | no_section；section_without_artifact；not_verified | RQ3；Table 1b；Conclusion |
| [leaf-ras-year] publication year | [dim-ras-rq] | 2013--2023 | 是；year × status | outside_window | Search process；Table 1b |
| [leaf-ras-venue] publication channel | [dim-ras-rq] | 15 journals in Table 1a；regression excludes journals with <10 publications | 是；venue × status；regression predictor | excluded_low_n；not_in_scope | Search ISSN query；Table 1a / 1c |
| [dim-ras-corpus] corpus construction and selection | [dim-ras-root] | Search → screening → final corpus | 是，protocol denominator chain | not_reported | Methods 2.1--2.2 |
| [leaf-ras-search-source] search source and query | [dim-ras-corpus] | Scopus；ISSN list；TITLE terms；PUBYEAR > 2012 and < 2024 | 是，supports reproducible search | query_not_available | Methods 2.1 |
| [leaf-ras-inclusion] inclusion / exclusion criteria | [dim-ras-corpus] | IC1 / IC2 / IC3；exclude conferences；manual SE relevance for CSUR / CSR | 是，supports scope validity | exclusion_reason_missing | Methods 2.2；Limitations |
| [leaf-ras-selection-reliability] screening reliability | [dim-ras-corpus] | Krippendorff’s Alpha = 0.776；95% CI mentioned | 是，quality / reliability metadata | not_measured | Methods 2.2 |
| [dim-ras-extraction] extraction and coding workflow | [dim-ras-root] | manual full-text screening + keyword script + manual check | 局部可统计；主要为方法 field | not_reported | Methods 2.3 |
| [leaf-ras-manual-screening] manual full-text screening | [dim-ras-extraction] | dedicated section found / not found | 是，feeds reporting anchor | not_checked | Methods 2.3 |
| [leaf-ras-keyword-context] keyword script context | [dim-ras-extraction] | keyword hit; 100 chars before / after; manually checked | 方法字段；若 Zenodo 核验可统计 | keyword_list_not_verified | Methods 2.3；Zenodo 待核验 |
| [leaf-ras-external-resource] external resource reference | [dim-ras-extraction] | link present / absent / by request / dead | 是，feeds availability status | no_external_resource | Methods 2.3；Table 1 |
| [dim-ras-stat-model] statistical analysis model | [dim-ras-root] | descriptive table + logistic regression | 是 | not_applicable | Table 1 |
| [leaf-ras-descriptive-counts] descriptive counts and percentages | [dim-ras-stat-model] | Total, count, percentage; denominators 537 / 169 / 79 / per-venue total | 是 | denominator_not_applicable | Table 1a--b |
| [leaf-ras-regression] logistic regression | [dim-ras-stat-model] | outcome artifact available; predictors year ordered factor, journal; reference TSE; coef / SE / z / p / odds ratio | 是 | excluded_low_n；model_not_run | Table 1c；RQ4 text |
| [dim-ras-validity] validity and scope boundaries | [dim-ras-root] | conference exclusion; Scopus-only; 2013--2023; no artifact quality assessment | 不作为 outcome 统计；作为外推边界 | not_reported | Limitations；Conclusion future work |
| [leaf-ras-artifact-quality-status] artifact quality assessment status | [dim-ras-validity] | not_assessed / future_work / assessed | 可统计为缺席事实，不得当作质量 finding | not_assessed | Conclusion lines about future quality study |
| [dim-ras-finding-path] finding / recommendation path | [dim-ras-root] | observation → gap → recommendation | 候选 finding；不直接迁移为 Paper2 final finding | insufficient_support | Results + Conclusion |
| [leaf-ras-gap-availability] availability gap | [dim-ras-finding-path] | 31.5% overall; 62.0% in 2023 | 是，原文 finding；Paper2 only schema_seed | out_of_scope_for_paper2_domain | RQ1; Conclusion |
| [leaf-ras-gap-persistence] persistence / DOI gap | [dim-ras-finding-path] | 38.5% among artifacts; 12.1% overall; 30.4% in 2023 | 是，原文 finding；Paper2 only schema_seed | no_artifact | RQ2; Conclusion |
| [leaf-ras-reporting-gap] reporting transparency gap | [dim-ras-finding-path] | dedicated section may say no data / upon request; section ≠ artifact | 候选 finding；needs qualitative evidence | section_without_artifact | RQ3; Conclusion |
| [leaf-ras-recommendation] practice recommendation | [dim-ras-finding-path] | mandatory artifact publication; permanent DOI repository; data availability section | 不进入统计池；recommendation field | author_recommendation_only | Conclusion / Future work |

建议关系边：

| 关系边 | 源节点 | 关系类型 | 目标节点 | 缺失值语义 | 证据定位 |
|---|---|---|---|---|---|
| [edge-ras-availability-permanent] | [leaf-ras-availability-status] | subset / attribute | [leaf-ras-permanent-repo] | no_artifact → not_applicable | RQ2；Table 1 |
| [edge-ras-reporting-not-equivalent] | [leaf-ras-reporting-anchor] | does_not_imply | [leaf-ras-availability-status] | section_without_artifact | RQ3；Conclusion no data / upon request |
| [edge-ras-year-availability] | [leaf-ras-year] | predictor_of | [leaf-ras-availability-status] | model_not_run | Table 1c |
| [edge-ras-venue-availability] | [leaf-ras-venue] | predictor_of / grouped_by | [leaf-ras-availability-status] | excluded_low_n | Table 1a / 1c |
| [edge-ras-limitation-scope] | [dim-ras-validity] | limits_generalization_of | [dim-ras-finding-path] | not_reported | Limitations |
| [edge-ras-quality-future] | [leaf-ras-artifact-quality-status] | future_work_for | [leaf-ras-recommendation] | not_assessed | Conclusion / Future work |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把正式维度树从通用接口改为 RQ-driven artifact audit schema | `review.md` `## 维度树复原` 第 214--246 行 | 以 RQ1--RQ4 建主干：availability、storage / permanent DOI、reporting anchor、year / venue effects；保留六个通用 leaf 为“跨论文检查视图”或删除出事实真源。 | `paper_content.txt` RQ1--RQ4；Table 1；PDF 第 3 页 | I |
| 修正单位对象 | 根问题 / RQ 映射表 | 把 `primary study / secondary study` 改为 `secondary study`；若要表达被综述对象中的 primary studies，应另写为 secondary studies 的研究对象，不作为本 mapping 的单位。 | Methods IC2；final 537 secondary studies | M |
| 展开 Table 1 字段为一等叶子 | 叶子维度表 / 原文模式候选叶子映射 | 增加 Venue、Year、Yes、No、By request、Dead link、Permanent repo、Dedicated section、Total、regression outcome / predictors / reference category / odds ratio 字段，并写明分母。 | Table 1a--c；PDF 第 3 页视觉核对 | I |
| 补 extraction / coding workflow 字段 | 叶子维度表 | 增加 manual full-text screening、keyword script、100-character context、manual check、external resource reference、permanent repository 判断。 | Methods 2.3 | I |
| 降级或重写 artifact content leaf | 原文模式候选叶子映射第 258 行 | 当前 `search_strategy_or_query / screening_decisions / extraction_table / scripts / README` 未在正文中作为被研究 artifacts 的编码 schema 出现；应标为 Zenodo 待核验 / Paper2 迁移候选，不写成原文模式来源。 | 正文只声明 Zenodo artifact 与 Data availability；未打开 Zenodo | I |
| 增加 validity / quality 状态叶子 | 叶子维度表 / 候选叶子映射 | 增加 `artifact_quality_assessment_status = not_assessed / future_work`，并记录 included-study quality rubric 未在正文报告；Krippendorff alpha 是 selection reliability，不是 artifact quality。 | Methods 2.2；Conclusion future work | I |
| 重建关系边表 | 关系边表 | 用 availability→permanent repo、reporting section↛availability、year/venue→availability regression、limitations→finding scope 替代通用 method-evidence / taxonomy-finding 边。 | Table 1；RQ3；Limitations | I |
| 补精确证据锚点 | A.2 | 将 EV-002 / EV-003 拆成 search、selection、extraction、Table 1a、Table 1b、Table 1c、limitations、conclusion 等多条证据；至少写 page、section、table number、`paper_content.txt` 行号范围；PDF 第 3 页 Table 1 可由本次视觉核对升级到“已核对表格结构”，但若仍无最终出版版核对则不要升级为 strong。 | `paper_content.txt` 全文；`paper.pdf` Page 3 | I |
| 补 A.1 来源 | A.1 | 增加 `metadata.json`、Zenodo DOI `10.5281/zenodo.15488074`（状态：未打开内部清单）、PDF Page 3 visual check 作为来源或复验对象。 | metadata.json；正文脚注 / Data availability；PDF Page 3 | M |
| 修正 PDF 核验状态不一致 | 快速卡片与 A.4 | 统一“已核对 Table 1 layout 文本 / 视觉核对”与 `needs_manual_check` 状态；如仍需 publisher final / Zenodo 核验，明确剩余对象。 | review.md 第 19--20、324--325 行 | M |
| 补 denominator semantics | 统计与候选发现链路 | 明确 537 all studies、169 artifact studies、65 permanent repo、72 dedicated section、79 2023 studies、regression excluded low-n journals；防止 50/169 与 72/537 混用。 | Table 1；RQ3 text；Conclusion | I |

## 6. C/I/M 结论

- C：0。当前 `review.md` 已有重要降级声明，没有把 `not_verified` 证据升级为 `statistical_synthesis`，也没有把该单篇统计直接写成 Paper2 final finding。
- I：8。核心问题是正式“维度树复原”仍以通用六叶接口为主，原文 RQ / Table 1 / extraction workflow / regression / validity / quality absence / finding path 没有成为事实真源中的一等叶子和关系边。这会实质影响 A2a/A2b 的 schema 回填和证据可审计性：后续 agent 可能只补页码，而不是重建该文真正的 artifact-audit schema。
- M：3。包括单位对象表述、A.1 来源完整性、PDF 核验状态一致性等维护性问题。
- 最终建议：NEEDS FIX。

最小修复方案：保留现有全文详读与六类 pattern 部分，但重写 `## 维度树复原` 的正式树、叶子表、关系边表和 A.2 / A.3，使 Table 1a--c、Methods 2.1--2.3、Limitations、Conclusion 成为可回链的 schema 证据；六个通用 leaf 只能作为跨论文检查接口，不应作为该单篇原文 schema 的正式叶子。
