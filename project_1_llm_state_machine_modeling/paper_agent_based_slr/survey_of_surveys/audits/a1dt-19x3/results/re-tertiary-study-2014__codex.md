# re-tertiary-study-2014 · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。本次按 claim-evidence gate、reviewer risk 和 claims-to-avoid 口径审计。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。本次按“严格贴合原文方法、字段和实验/统计设计，不补造缺失细节”口径审计。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本次只使用其 artifact-gated、validator evidence 思路，不启动 autoresearch 循环。
- 是否完整阅读 `paper_content.txt`：是；逐段阅读 `paper_content.txt` 全文 1--966 行，覆盖摘要、引言、RQ、planning、search string、纳排、数据抽取、execution、结果、Table/Figure 文本、gap 分析、limitations、conclusion、Appendix A。
- 是否核对 `paper.pdf`：是；使用 `pdfinfo` 确认 9 页 PDF，使用 `pdftotext -layout` 核对关键页 2--8，并用 `pdftoppm` + 图像查看核对 PDF 第 3--7 页版面中的 RQ、Table I、Table II、Figure 1、Table III、Table IV、Table V、Figure 2--4、Table VI、limitations。未逐条视觉核对 Appendix A 的 53 个 included studies 引用项。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文明确定位为 Requirements Engineering 领域已发表 SLR/SMS/meta-analysis 的 tertiary study。摘要和引言声明目标是识别 RE 相关 SLR，给出覆盖主题、质量和 gap 的综合概览，并作为后续更新 RE roadmap 的第一步。核心 RQ 在 `paper_content.txt:117-123`：

- RQ1：RE 中哪些主要研究领域已被 published SLR 覆盖。
- RQ2：已发表 RE SLR 的质量如何。
- RQ3：已发表 SLR 对 RE research topics 的覆盖存在哪些 gap。

原文贡献不是“教育/实践影响字段表”，也不是完成型 roadmap；它给出 2006--2014 年 53 个 unique SLR、64 个 publications 的 tertiary mapping，并提出质量下降、主题覆盖 gap、部分 SLR 需要 replication 等 findings。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法按 EBSE planning、execution、reporting 组织。Planning 阶段声明 protocol 覆盖 search/selection、quality assessment、data extraction、data synthesis、data analysis，见 `paper_content.txt:108-117`。

检索流程包括：

- 两个主检索概念：Requirements Engineering 与 Systematic Literature Review，经过 pilot testing、同义词扩展和参考既有 tertiary/RE SLR 补关键词，形成长 search string，见 `paper_content.txt:184-207`。
- 自动检索源：IEEE Xplore、ACM DL、ScienceDirect、Google Scholar、EI Compendex，按数据库界面定制但保持逻辑一致，见 `paper_content.txt:208-213`。
- 没有 publication year 限制，见 `paper_content.txt:212-213`。
- snowball/manual 补检：四篇既有 tertiary studies 的 references，以及 2004 年起的 RE/EASE/ESEM/REFSQ/REJ/ESE/IST，见 `paper_content.txt:213-220`。
- 纳排标准：英文；Systematic Review/Systematic Mapping/meta-analysis；聚焦 Requirements Engineering，见 `paper_content.txt:221-230`。
- 多 publication 同一 study 的处理：保留多个 publication，但按 study ID 分组并用 A/B/C suffix 标识，见 `paper_content.txt:231-235`、`paper_content.txt:249-253`。

数据抽取与编码包括：

- publication details：title、authors、year、publication type、conference/journal name、complete reference、number of citations，见 `paper_content.txt:236-243`。
- RQ 字段：number of primary studies、focus of SLR，见 `paper_content.txt:242-244`。
- topic grouping：对 selected publications 的 titles/abstracts 做 thematic analysis，形成 Table V 第一列 topic group，见 `paper_content.txt:244-247`。
- 质量评价：DARE-derived QA1--QA4，Yes/Partial/No 分别为 1/0.5/0，评估 whole study 而非单 publication，见 `paper_content.txt:132-179`。
- publication impact：Google Scholar citation count，核验日期为 2014-05-19，见 `paper_content.txt:179-183`。

统计与 finding 形成方式包括：

- Table II 给出 search execution denominator：267 primary-search hits、91 included after selection criteria、58 after duplicate removal、6 secondary-search additions、64 publications、53 studies，见 `paper_content.txt:273-288`。
- Results 先统计出版年份、publication type、review type，见 `paper_content.txt:299-314`、Figure 1、Table III。
- RQ1 使用 Table IV scope classification 和 Table V RE topic taxonomy + # primary studies + year 回答。
- RQ2 使用 Table I rubric、Figure 2/3/4、Table VI citation/QA 表形成 quality finding。
- RQ3 明确分三条 finding path：不同 SLR 对同一 topic 的 primary-study 数量 anomaly；部分 topic 的 primary studies 数量很少；与既有 RE roadmaps 对照后发现未被 SLR 覆盖的 RE areas，见 `paper_content.txt:494-576`。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 至少包括：

- RQ schema：RQ1/RQ2/RQ3。
- Search/selection schema：search string、source、included count、duplicate handling、secondary-search source、selection criteria、fulltext retrieval status。
- Extraction form：title、authors、year、publication type、conference/journal name、complete reference、citation count、number of primary studies、focus of SLR。
- Publication/study relation：64 publications vs 53 unique SLR；同一 study 多 publication 用 study ID + suffix A/B/C。
- Table I quality rubric：QA1 inclusion/exclusion criteria、QA2 search-space adequacy、QA3 quality assessment of primary studies、QA4 information regarding primary studies；答案 Yes/Partial/No；分值 1/0.5/0。
- Table III publication type taxonomy：conference papers、journal papers、workshop papers、technical reports、theses、unknown。
- Review type taxonomy：12 systematic mapping studies、1 meta-analysis、其余为 SLR。
- Table IV scope taxonomy：state of the art、methods、techniques、tools、frameworks、technology。
- Table V topic taxonomy：Non Functional Requirements、Complete RE Process、Model Driven Development、Knowledge Management and RE、RE in GSD、RE in Software Product Lines、Requirements Management、Multi Agent Systems、Requirements Reuse、Value based RE、Virtual Reality Systems、Web Engineering、Creativity in RE、Requirements Elicitation、Stakeholders and users、Requirements Prioritization、Meta Modelling、Software Requirements Specifications、Requirements Verification / Validation / Evaluation、Requirements Traceability、Requirements Change Management、RE Education、Mobile Learning、Checklist for RE。
- Table VI citation/impact schema：S-ID、GS citations、publication channel、QA score。
- Figures 1--4：year distribution、quality score distribution、per-QA check distribution、average quality score by publication year。
- Appendix A：included studies ledger，字段为 ID、complete reference、citation。
- Roadmap：原文没有独立 roadmap figure 或完整 roadmap taxonomy；只有把 Table V topics 与 Nuseibeh/Easterbrook 2000、Cheng/Atlee 2007 roadmaps 对照，并声明本 study 是后续 updated RE roadmap 的 first step。因此 roadmap 字段应写成 `roadmap_comparison / future_plan`，不能写成完成型 roadmap figure。
- Artifact：原文未报告 replication package；仅有 Appendix A included-studies ledger、文中 search/QA/table evidence，以及未来计划更新 Alan Davis bibliography。`protocol available` 只在 replication discussion 中作为条件性建议，不是本文发布的 artifact。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding 链条是字段到统计再到解释：

- 覆盖 finding：Table IV/Table V 的 scope/topic/#PS/year 支撑“哪些 RE 主题被覆盖”和“哪些 topic primary studies 较多或较少”。
- 质量 finding：Table I rubric 先定义质量字段，Figure 2--4 汇总 51 个可获取 studies 的 QA scores，再推导 “42/51 scored 2 or above” 和 “2009 后 average quality 下降”，并把原因指向 QA3/QA4 缺失。
- gap finding：RQ3 明确由 anomalies、low #PS、ignored RE areas 三条路径形成；其中 anomaly 例子比较 S1/S4 与 S24/S4/S21/S25 的 #PS 与检索流程差异，最终提出 replication need。
- limitation 降级：作者承认可能漏检、S40 publication detail unknown、topic grouping 命名有主观性、quality assessment 受 EBSE/DARE criteria 限制、gap analysis 仅 preliminary observations。因此 current review 不能把这些 observations 升级为无条件定量结论。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确但单位对象错误 | 根节点抓住了 RE tertiary study，但 `review.md:73` 把单位对象写成 `primary study / secondary study`。原文统计分母实际有两层：53 unique secondary studies / 64 publications；primary studies 只是被纳入 SLR 的 `# of PS` 字段。此错误会污染后续统计分母。 | C |
| 主干分支是否覆盖原文 schema | 不覆盖 | `review.md:77-90` 的 b1--b5 是跨论文通用接口，未按 RQ1/RQ2/RQ3、method protocol、extraction form、quality rubric、gap path、limitations 复原原文 schema。虽有 `review.md:67` 的免责声明，但真实原文 schema 仍没有被展开。 | C |
| 叶子维度是否足够具体 | 不足 | `review.md:96-101` 六个 leaf 是通用接口；`review.md:109-112` 只有四个原文候选叶子，遗漏 search string/source/selection/fulltext status、publication-study relation、Table III/IV/V/VI、QA1--QA4、citation checked date、RQ3 三类 gap、limitations、Appendix A、artifact missing 等原文叶子。 | C |
| 取值空间是否可执行 | 多数不可执行 | 当前候选取值如“需求获取、建模、验证、管理、追踪、质量等子主题”和“检索、纳排、QA、数据抽取、综合和报告质量”过粗，没有列出 Table IV/V 的真实枚举，也没有说明 `NM`、`NF`、unknown、not retrieved、not peer-reviewed、low QA score 等缺失语义。 | I |
| 关系边是否缺失 | 缺失关键关系 | 原文至少需要 study-publication grouping、RQ→table/figure→finding、topic↔#PS、QA rubric→quality score→trend、roadmap topic comparison→ignored area、anomaly pair comparison 等关系。当前没有关系边表，也没有把缺失关系如 S3/S8 fulltext missing、S40 publication detail unknown 入账。 | I |
| 统计用途 / 分母是否正确 | 不正确且过泛 | `review.md:118-120` 用“当前 19 篇 survey-of-surveys 样本”作为 root 统计分母，不能替代本文内部 267/91/58/64/53/51 等分母。当前没有分清 64 publications、53 studies、51 QA-scored studies、Table V topic rows、Appendix A citations。 | C |
| 候选 finding 路径是否完整 | 不完整 | 原文 finding path 包括 RQ2 quality decline/QA3/QA4 问题，以及 RQ3 anomalies、low #PS、ignored RE areas、replication need。当前 `review.md:119-120` 只泛写“主题覆盖、缺口或 roadmap action”和“candidate finding”，不能复验 finding 形成。 | I |
| A.1--A.4 证据链是否足够 | 不足 | A.1 文件来源存在；但 A.2 多处写“见释义”“邻近段落”“待 A2a 精确页码复核”，没有行号范围、短引、表号/图号级映射。按 GUIDE 6.3.7 降级为 `not_verified` 是正确的，但这也意味着当前维度树不能被视为完整可追溯复原。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在 | `review.md:63` 的 C01 树型判断和 `review.md:163` 的“已把原文抽取字段、分类项、模型节点或报告叶子列为候选”容易让 A2a 误以为原文 schema 已覆盖；但实际只列四个粗叶子。`review.md:111` 的“工业采用”不是原文 extraction field。`review.md:144-145` 泛写 roadmap/action point，也可能误导为存在 roadmap figure。 | C |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为忠实原文 schema。建议将“六个通用接口”保留为跨论文 wrapper，但必须新增以下原文维度树作为本篇事实源。

| 主干节点 | 叶子维度 | 候选取值空间 | 是否可统计 / 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|
| 根节点：RE SLR tertiary study | 研究对象与分母 | `unique_secondary_study=53`；`publication=64`；`qa_scored_study=51`；`primary_search_hits=267`；`post_selection=91`；`post_dedup=58`；`secondary_added=6` | 可统计；缺失值区分 `not_retrieved_fulltext`、`publication_detail_unknown`、`duplicate_publication_same_study` | 摘要 `paper_content.txt:23-40`；Table II `273-288`；S3/S8/S40 `290-295` |
| RQ 层 | RQ1 topic coverage | RQ1 原文问题；输出 Table IV/Table V | 作为 finding root，不直接统计；统计落到 topic/scope/#PS | `117-131`、`332-376` |
| RQ 层 | RQ2 quality | RQ2 原文问题；输出 Table I/Figures 2--4/Table VI | 作为 finding root；统计分母 51 studies | `132-183`、`433-493` |
| RQ 层 | RQ3 coverage gaps | anomaly、lack_of_primary_studies、ignored_RE_areas | 可统计为候选 gap 类型；必须保留 preliminary limitation | `494-576`、`612-615` |
| 检索与纳排 | search concept/string | RE synonym set；SLR/review/mapping synonym set；Boolean expression | 不统计或统计 source/method coverage；缺失写 `not_reported` | `184-207`；PDF 第 3 页已核对 |
| 检索与纳排 | search source | IEEE Xplore、ACM DL、ScienceDirect、Google Scholar、EI Compendex；manual venues RE/EASE/ESEM/REFSQ/REJ/ESE/IST；snowball refs [8-11] | 可统计；缺失写 `source_not_used` | `208-220`；Table II |
| 检索与纳排 | selection criteria | English；SR/SMS/meta-analysis；Requirements Engineering focus | 可统计为 inclusion criterion presence；缺失写 `criterion_not_reported` | `221-230`；PDF 第 3 页已核对 |
| 检索与纳排 | retrieval / exclusion anomalies | S3/S8 full paper not retrieved；S40 publication channel unknown | 可统计为 missing evidence flags；不可写成 excluded | `290-295`、`577-593` |
| 抽取表 | bibliographic fields | title、authors、year、publication type、venue/channel、complete reference、GS citations | 可统计；citation 需记录 checked_date=2014-05-19 | `236-243`、`179-183`、Appendix A |
| 抽取表 | SLR content fields | number of primary studies、focus of SLR、main topic group、study ID/suffix | 可统计；`NM=not mentioned`、`NF=not found` | `242-247`、Table V、Appendix A |
| study-publication 关系 | multiple publications per study | same study ID + suffix A/B/C；8 studies with two publications；1 study with three publications；S2 extended second version | 关系型字段；缺失写 `single_publication` | `231-235`、`296-298`、Appendix A |
| 分类 schema | publication type | conference、journal、workshop、technical report、thesis、unknown | 可统计；unknown=S40 | Table III `317-331`；PDF 第 4 页已核对 |
| 分类 schema | review type | systematic mapping study、meta-analysis、SLR | 可统计；需要按 study 分母 53 | `311-314` |
| 分类 schema | scope of RE SLR | state_of_the_art、methods、techniques、tools、frameworks、technology | 可统计；Table IV 封闭枚举 | Table IV `364-375`；PDF 第 5 页已核对 |
| 主题 taxonomy | main RE topic group | Non Functional Requirements、Complete RE Process、Model Driven Development、Knowledge Management and RE、RE in GSD、RE in Software Product Lines、Requirements Management、Multi Agent Systems、Requirements Reuse、Value based RE、Virtual Reality Systems、Web Engineering、Creativity in RE、Requirements Elicitation、Stakeholders and users、Requirements Prioritization、Meta Modelling、Software Requirements Specifications、Requirements Verification / Validation / Evaluation、Requirements Traceability、Requirements Change Management、RE Education、Mobile Learning、Checklist for RE | 可统计；overlap flag 如 S26/S39；`NM`/`NF` 单独入账 | Table V `376-429`；PDF 第 5 页已核对 |
| 质量 rubric | QA1 inclusion/exclusion | Yes=1、Partial=0.5、No=0 | 可统计；按 51 retrievable studies | Table I `147-178`；Figure 3 |
| 质量 rubric | QA2 search-space adequacy | Yes=1、Partial=0.5、No=0 | 可统计；按 51 retrievable studies | Table I；Figure 3 |
| 质量 rubric | QA3 primary-study quality assessment | Yes=1、Partial=0.5、No=0 | 可统计；原文 finding 指向 half ignored QA3 | Table I；`469-479` |
| 质量 rubric | QA4 information regarding primary studies | Yes=1、Partial=0.5、No=0 | 可统计；原文 finding 指向 QA4 overview/summary 缺失 | Table I；`469-479` |
| 质量与影响 | total QA score / yearly average | score 0--4；yearly average by publication year | 可统计；图表数值需 PDF/table extraction 精核 | Figure 2/4；`433-481` |
| 质量与影响 | citation impact | GS citations、publication channel、QA score；checked_date=2014-05-19 | 可统计；不等于 industry adoption | `179-183`、Table VI `482-493` |
| finding 路径 | anomaly finding | compared_studies、topic、#PS conflict、search string/source/criteria cause、replication_need | 候选 finding；需保留作者推断与范围 | `505-539` |
| finding 路径 | low #PS finding | studies with <10 primary studies；possible causes: weak search vs neglected empirical area | 候选 finding；不能直接断言 neglected | `540-551` |
| finding 路径 | ignored RE areas | covered roadmap topics；uncovered topics: Requirements Scaling、RE for self-management systems、effects of system environment on RE、effectiveness of RE research in practice、conflict resolution、requirements negotiation | 候选 finding；roadmap comparison，不是 roadmap figure | `552-576` |
| limitations | search completeness risk | electronic resources unavailable、keywords absent from title/abstract；secondary search mitigation | risk field；不进入 positive finding | `577-586` |
| limitations | classification subjectivity | first author grouped titles/abstracts；other two authors reviewed names；future short descriptions planned | risk field；topic taxonomy confidence limiter | `594-602` |
| limitations | QA/gap limits | QA quality bounded by EBSE criteria；gap analysis preliminary and not exhaustive | risk field；强制降级 RQ3 claims | `603-615` |
| artifacts / appendix | Appendix A included-studies ledger | ID、complete reference、citation | 可作为 evidence ledger；不是 replication package | `697-966` |
| artifacts / roadmap future | artifact availability | `replication_package=not_reported`；`published_protocol=not_reported`；`future_bibliography_update=planned` | 不进入完成型 artifact 统计；缺失语义必须明确 | `536-539`、`636-645` |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 修正根节点单位对象和分母 | `review.md` 维度树复原：根问题 / RQ 到主干分支映射、统计链路 | 将单位对象改为 secondary study 与 publication 双层；把 primary studies 改为 `# of PS` 字段；显式记录 267/91/58/64/53/51 分母 | `paper_content.txt:23-40`、`273-288`、`433-438` | C |
| 用原文 RQ 重建主干 | `review.md` 维度树结构 | 在通用接口之外新增 RQ1 topic coverage、RQ2 quality、RQ3 gaps 三条原文主干，并把 method/extraction/limitations 作为支撑分支 | `117-123`、`332-576` | C |
| 扩展原文候选叶子表 | `review.md` 原文模式候选叶子映射 | 从 4 个粗叶子扩展为 search/selection、extraction form、publication-study relation、publication type、review type、scope taxonomy、topic taxonomy、QA1--QA4、citation、gap path、limitations、Appendix/artifact missing 等叶子 | Table I--VI、Figures 1--4、Appendix A | C |
| 补全取值空间与缺失语义 | `review.md` 叶子维度表和原文模式候选叶子映射 | 写出 Table IV/V 的封闭枚举；写 `NM`、`NF`、unknown、not retrieved fulltext、publication_detail_unknown、not_reported replication package 等缺失语义 | `290-295`、`317-331`、`364-429` | I |
| 移除或降级非原文字段 | `review.md` 原文模式候选叶子映射与 A.2 释义 | 删除“工业采用”作为原文字段；将 roadmap/action point 改为 `roadmap_comparison / future_plan`，并声明无 roadmap figure；将 artifact/replication package 设为 not_reported | `111`、`536-539`、`636-645` 对照当前 `review.md:111`、`144-145` | I |
| 补 RQ3 finding path | `review.md` 统计与候选发现链路、A.3 | 分别建 anomaly、low #PS、ignored RE areas、replication need、quality QA3/QA4 gap 的候选 finding 节点；每个节点保留支持字段、反证/限制、claim strength | `494-576`、`612-615`、`625-635` | I |
| 补 validity / limitation 复原 | 六类 pattern、维度树叶子、A.2/A.3 | 当前写“threat section 未完整定位”不成立；应复原 Section IV 的 search completeness、S40 unknown、topic grouping subjectivity、QA criteria limitation、gap preliminary limitation | `577-615` | I |
| 加强 A.2/A.3 可追溯性 | 审计附录 A.2--A.4 | 将 EV-002/003 拆成多个证据项，写具体行号范围、页码、表/图编号、短引或释义；需要版面核验的全部设 `需要原文版面核验=true` 并回链 A.4 | 当前 `review.md:143-146` 与 PDF 页 3--7 | I |
| 修正早期六类 pattern 的 stale 结论 | `review.md` 六类 pattern 抽取 | `finding pattern` 不应说“当前只读摘要级结果”；若保留则会和全文阅读状态冲突。应按 Results/Discussion/Limitations 改写 | 当前 `review.md:31`；原文 `299-645` | M |

## 6. C/I/M 结论

- C：当前维度树主干和叶子仍主要是通用接口层，原文 RQ、抽取表、taxonomy、quality rubric、finding path 和真实分母没有完整复原；这会直接破坏 Paper2 对“维度模式从原文 schema 演化而来”的学术目标。根节点把 primary study 与 secondary study/publication 混为单位对象，也会直接污染 A2a/A2b 的统计分母和证据链。
- I：取值空间、缺失值语义、limitations、artifact/not_reported、roadmap 降级、A.2/A.3 证据定位都不足，会实质影响后续 A2a 精核、schema 回填和 candidate finding 的可审计性。
- M：六类 pattern 中仍有“只读摘要级结果”等 stale 表述；建议同步清理，避免与全文文本级状态冲突。
- 最终建议：NEEDS FIX。
