# research-artifacts-secondary-studies · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：是。读取路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`；`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` 未在本机文件树中找到对应 reference 文件，按 SKILL.md 中“Reviewer mode”职责要求自我执行（claim-evidence gate + 证据资产 gate + 弱主张降级）。
- 是否读取 `$research-planning`：未读。该 skill 在 `/home/zhangshaoang/.codex/skills/` 下未发现独立目录；按当前任务范围（A1-DT 单篇维度树审计，无新增 plan/research-question 设计）默认采用 ai-research-writing-skill 的 task-state / claim-evidence 模式作为等价口径。
- 是否读取 `$oh-my-codex:autoresearch`：未读。`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` 路径在本环境未列出可访问文件；本审计目标是 A1-DT 单篇审计，不进入二级 autoresearch 探索。
- 是否读取库级规则与 story：是。已读 `survey_of_surveys/GUIDE.md`、`patterns/pattern-field-schema.md`、单篇 `review.md`、`bibtex.bib`、`metadata.json` 关键字段；`README.md / SUMMARY.md / story/paper_story.md` 中仅查证与本篇 A1-DT 直接相关的字段（A1-M0--M6、`eligible_for_statistical_synthesis=false` 的 schema_seed 口径）。
- 是否完整阅读 `paper_content.txt`：是。共 358 行 / 6 页（含 1 页 references），逐页核对了 Abstract、Introduction（4 个 Reason）、Methods §2.1 Search、§2.2 Selection（IC1/IC2/IC3、Krippendorff α=0.776）、§2.3 Data extraction（两轮 + Python keyword + 100 字上下文）、§3 Results（RQ1--RQ4、Table 1a/b/c）、§4 Limitations、§5 Conclusion and Future work、CRediT、Data availability、References。
- 是否核对 `paper.pdf`：未做视觉级核对。`review.md` §2.5 已声明“用 PDF layout 文本核对 Table 1 关键数值”，并把视觉核验列入 §7 待复核第 2 项；本审计接受该口径，但 Table 1 子表精确页/列布局仍标 needs_manual_check。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

四个 RQ，按 `paper_content.txt` Page 2--4：

1. RQ1：537 篇 secondary studies 中包含 research artifact 的比例。
2. RQ2：research artifacts 的存放位置，重点是是否使用 permanent repository (Zenodo / Figshare / Mendeley Data) + DOI。
3. RQ3：data / artifact availability 在论文中如何陈述，特别是是否有 dedicated section。
4. RQ4：出版年份与出版论坛如何影响 research artifact availability（logistic regression）。

声明型贡献（Abstract + §5）：(i) 量化 SE secondary studies 的 artifact 报告与可获得性现状；(ii) “provide a comprehensive list of these artifacts”（摘要措辞，但正文未展开，依赖 Zenodo 工件）；(iii) 用 logistic regression 给出 year 与 journal 的可解释影响；(iv) 行动建议：强制发布工件 / 使用永久仓库 / 设置 Data availability section。

### 2.2 方法流程

- **指南遵循**：Petersen et al. 2015 systematic mapping guidelines + SIGSOFT Empirical Standards checklist（Page 2 §2 + footnote 1）。
- **检索**：单一来源 Scopus；查询为 ISSN OR (13 SE 期刊 + 2 CS 综述期刊) AND TITLE("Mapping Study" OR "Systematic review" OR "Systematic Literature Review" OR "Systematic Mapping" OR "Meta Analysis" OR "Meta Synthesis" OR "Scoping Review" OR "Case Survey" OR "Critical review") AND PUBYEAR>2012 AND PUBYEAR<2024（Page 2 完整查询）。
- **纳排**：IC1 2013--2023 / IC2 secondary study / IC3 SE-related；ACM Computing Surveys 与 Computer Science Review 因不限于 SE 经人工裁决；Krippendorff α=0.776（95% CI）作为 inter-rater agreement。
- **抽取**：两轮 — (1) 人工 full-text screening 识别 dedicated section；(2) Python 关键词脚本打印命中前后 100 字符，由人工裁决；判断是否引用外部资源 + 是否位于永久仓库（Figshare/Zenodo/Mendeley）。
- **统计**：(a) 按 publication channel 的 6 列频率表（Total / Yes / Permanent repo / No / By Request / Dead Link）；(b) 按年的 6 行 × 11 年频率表（Yes / No / By req. / Dead / Permanent repo / Dedicated section）；(c) 二元 logistic regression，自变量 = year（scaled ordered factor）+ journal（TSE 为 reference category，<10 篇期刊被排除）。
- **Finding 形成方式**：通过比例 + 年度趋势 + 回归显著性（year odds ratio = 2.31 / 3-year）+ journal 系数显著性，导出 (a) 改善趋势、(b) 永久仓库不足、(c) Data availability section 出现“no data was used” / “upon request”虚假透明度、(d) 2023 年 19 个非永久仓库链接已有 2 个失效 — 进而升级为 mandatory publication / permanent repository / dedicated section 三条建议。

### 2.3 原文显式 schema / 字段 / 表格

按字段抽取“**原文真实抽取与统计 schema**”（Page 2--4）：

| 原文字段 | 取值空间（原文给定） | 出现位置 |
|---|---|---|
| publication channel | 15 个具名 venue（Table 1a 列出） + Total | Table 1a |
| publication year | 2013--2023 离散；回归中作 scaled ordered factor | Table 1b / Table 1c |
| artifact availability | {Yes, No, By Request, Dead Link}（4 个原子状态，互斥总和=537） | Table 1a / 1b |
| permanent repository flag | {permanent repo, non-permanent}；与“Yes”是子集关系 | Table 1a / 1b |
| repository provider | {Zenodo, Figshare, Mendeley Data}（永久仓库白名单，§2.3） | §2.3 / §4 |
| dedicated section flag | {present, absent} | Table 1b（仅年度行）+ §5 |
| dedicated section content sub-type | {repository link / DOI, "no data was used", "available upon request"}（§5 提及，未独立列表） | §5 Conclusion |
| dead-link time-sensitivity | 2023 年 19 个非永久链接已 2 dead | §5 |
| reasons for needing artifact | {Replicability, Trust, Updates, Pathway to Automation}（§1 四条） | §1 Introduction |
| inclusion criteria | {IC1 2013--2023, IC2 secondary study, IC3 SE-related} | §2.2 |
| inter-rater agreement | Krippendorff α=0.776 (95% CI) | §2.2 |
| extraction method | {manual full-text screening, Python keyword script + 100-char context, manual check} | §2.3 |
| logistic regression covariates | year (ordered factor) + journal (TSE ref, journals<10 excluded) | Table 1c / §3 |
| recommendations / future work | {mandatory artifact publishing, permanent repo + DOI, dedicated section, quality assessment future study} | §5 |

### 2.4 字段 → finding 的形成路径

- (availability=Yes 比例) + (year ordered factor) → RQ4 finding：odds ratio 2.31 / 3-year，趋势显著。
- (permanent repo / Yes 子集 = 38.5%) + (permanent repo / 537 全集 = 12.1%) + (permanent repo 2023 = 30.4%) → RQ2 finding：DOI 持久仓库总体偏低，但趋势改善。
- (dedicated section 2023 = 58.2%) + (dedicated section 内容 = "no data" / "upon request") → RQ3 finding：声明结构改善但内容质量隐忧。
- (Dead Link = 22/537 = 4.1%) + (2023 年 19 非永久链接 → 2 dead) → §5 时间敏感性 finding。
- journal 系数显著性（CSR / SPE / JSEP / IST 显著为负） → RQ4 venue-effect finding。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分通过 | 根节点写“Research artifacts in secondary studies 的研究目标 / RQ / 贡献声明”，对象 = primary/secondary study，方向正确；但根节点未显式区分单位对象为“secondary study”（论文级）和“research artifact”（资产级），而原文 RQ2/RQ3 实际是在 artifact 子集上分母不同。 | M |
| 主干分支是否覆盖原文 schema | 否 | 当前 5 主干 b1 secondary study corpus / b2 artifact type / b3 availability status / b4 repository / DOI evidence / b5 reproducibility gap。其中 **b2 “artifact type”** 在原文不存在——本文明确不做 artifact 类型本体，只统计有无与位置；**b5 “reproducibility gap”** 是 finding 而非 schema branch；**dedicated section（RQ3）**未独立成为主干分支；**publication year / venue / logistic regression** 三个本文最核心的统计支撑维度被压在 b5 内，并未抬升到主干。 | C |
| 叶子维度是否足够具体 | 否 | 主 `维度树结构` (line 222--235) 每个主干只挂一个通用接口 leaf（scope / corpus / taxonomy / method / evidence / finding），完全是跨论文通用层，**与本文原文 schema 无具体对应**。原文真实字段（availability 四态、permanent repo flag、repository provider 白名单、dedicated section flag + 内容子类型、year ordered factor、journal reference、Krippendorff α、Python keyword 抽取流程）只在 §“原文模式候选叶子映射（A1 种子）”中以 6 行 `not_verified` schema_seed 出现，并未挂到正式 `维度树结构`。这正是 prompt 警示的“把通用 6 个 leaf 接口误当成原文 schema”。 | C |
| 取值空间是否可执行 | 否 | 主 leaf 表的取值空间写为“自由文本加 RQ / 贡献声明引用”“完整枚举 / 层级枚举 / 自由文本加理由”等抽象口径；而原文真实取值空间是封闭原子集（availability ∈ {Yes, No, By Request, Dead Link}；repository provider ∈ {Zenodo, Figshare, Mendeley Data, other-non-permanent}；dedicated section ∈ {present, absent}）。即便 A1-DT 阶段保留 schema_seed 语义，取值空间也应写成“原子集 + 缺失值 / 未检查 / 未报告”的封闭枚举。 | C |
| 关系边是否缺失 | 是 | 当前只声明两条关系边：method→evidence、taxonomy→finding。**原文最核心的关系**未被刻画：(a) availability ⊂ Yes 的子集关系（permanent repo 是 Yes 的子集；dedicated section 与 availability 的交叉）；(b) year × journal × availability 的三维交叉（logistic regression）；(c) availability vs dedicated section 的“声明 ≠ 真有”反例边（§5 “no data was used” / “upon request”）。 | I |
| 统计用途 / 分母是否正确 | 否 | 6 个主叶子全部统一写“可进入描述统计 / 交叉统计，前提是分母和样本单位明确”，未把原文**三类分母**写死：537（全体）、169（含 artifact 子集）、79（2023 子集）、<10 篇期刊被回归排除。`review.md` §2.7 自己已写出“Dedicated section 与真实开放 artifact 不是同一个概念，分母不能混用”，但这条 critical 信息未落入维度树的“统计用途 / 分母”字段。 | I |
| 候选 finding 路径是否完整 | 否 | `[leaf-...-finding]` 写为“说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现”，但**未列出原文 5 条 finding 的字段→finding 链路**（趋势 finding、permanent repo gap、dedicated section 虚假透明度、dead-link 时间敏感、journal-effect）。`A.3` 结论列表也只有 “tree_type / leaf_definition / migration_boundary / candidate_finding / relation_edge / source_schema_candidate” 元层级，没有把原文 5 条 candidate finding 显式登账。 | I |
| A.1--A.4 证据链是否足够 | 否 | A.1 只记录 paper.pdf / paper_content.txt / bibtex.bib 三条 source，**未记录 metadata.json**（虽然 §1 提到）；A.2 五条 EV-* 全部 `证据强度=not_verified`，所有“原文页码”写“摘要 / 引言页 / 方法 / 结果 / 讨论页 / threats / limitations 页；待 A2a 精确页码复核”。但 `paper_content.txt` 已经把 Page 1--6 分页号写明，**至少 Page 1 Abstract、Page 2 §2.1/§2.2/§2.3、Page 3 Table 1、Page 4 §3 RQ2--RQ4/§4 Limitations、Page 5 §5 Conclusion 可以直接锚定**，证据强度应从 `not_verified` 升级为 `paper_text_full`（GUIDE.md “证据等级”枚举中的“全文文本级；图表待人工核对”），而不是统一停留在 `not_verified`。这是自我降级过度。 | I |
| 是否存在可能误导 A2a 的强主张 | 否 | 全文未出现“本文证明…”“显著优于…”这类越界主张；所有 claim strength 均为 weak / schema_seed / candidate_finding，符合“A1-DT 仅作 schema seed”的纪律。但 §“一句话结论”（line 208）写“本 A1-DT 维度树仍是 schema seed”这句结论本身没问题；问题是当前 schema seed **过浅**，对 A2a 的提示力 = 仅 6 个通用接口 leaf 名称，无具体字段、无取值空间、无分母——A2a 接到这份维度树后仍需要从原文重做 RQ 复原，A1-DT 的增量贡献被压低。 | I（不构成误导，但 schema 信息密度过低） |

## 4. 建议维度树骨架

A1-DT 阶段不要求完成 A2a 精核，但维度树骨架应**忠实于原文**，把通用 6-leaf 接口与原文真实字段**双层并置**（接口层做迁移锚点，原文层做证据复原），而不是用接口层覆盖原文层。建议骨架：

```text
[dim-research-artifacts-secondary-studies-root] Research artifacts in secondary studies (SE)
  - 单位对象：secondary study (paper-level) AND research artifact (asset-level，作为 paper 的子集字段)
  - 分母候选：537 全体 / 169 含 artifact 子集 / 79 篇 2023 子集 / <10 篇被回归排除的 venue 子集

├── [b1] corpus & screening protocol（语料与纳排链条）
│   ├── search-source = {Scopus single-source}
│   ├── venue-filter = {13 SE journals + 2 CS review journals, ISSN-based}（封闭 15 列）
│   ├── title-keyword = {Mapping Study, Systematic review, Systematic Literature Review, Systematic Mapping, Meta Analysis, Meta Synthesis, Scoping Review, Case Survey, Critical review}（封闭 9 项）
│   ├── time-window = 2013--2023（因 Zenodo/Figshare 2011--2013 上线）
│   ├── inclusion-criteria = {IC1 2013--2023, IC2 secondary study, IC3 SE-related}
│   ├── disambiguation = {ACM Computing Surveys, Computer Science Review 经人工裁决}
│   └── inter-rater = Krippendorff α=0.776 (95% CI)
│
├── [b2] research-artifact availability schema（核心抽取 schema，A1-DT 此处必须复原）
│   ├── availability-status ∈ {Yes, No, By Request, Dead Link}（4 原子，互斥求和=537；缺失语义=未检查 / 未报告 单列）
│   ├── permanent-repository-flag ∈ {permanent, non-permanent, n/a}（仅在 availability=Yes 时有效，是 Yes 的子集）
│   ├── repository-provider ∈ {Zenodo, Figshare, Mendeley Data, other-non-permanent, none}（永久仓库白名单 = 前三）
│   ├── persistent-identifier ∈ {DOI, none}（与 permanent-repository-flag 强相关但不等同）
│   ├── extraction-method ∈ {manual full-text screening, Python keyword + 100-char context + manual check}
│   └── access-mode ∈ {open-link, upon-request, dead}（与 availability 字段交叉而非重复）
│
├── [b3] reporting anchor schema（声明位置与声明质量）
│   ├── dedicated-section-flag ∈ {present, absent}（独立于 availability 字段，分母=537）
│   ├── dedicated-section-content-sub-type ∈ {repository-link/DOI, "no data was used", "available upon request"}（§5 提及，A2a 待精核完整枚举）
│   └── section-name = 自由文本（"Data availability" / "Artifact availability" / "Replication package" / ...）
│
├── [b4] trend & venue covariates（时间 / 论坛交叉）
│   ├── publication-year（2013--2023 离散；回归中 scaled ordered factor）
│   ├── publication-venue（15 个具名期刊，<10 篇被回归排除）
│   ├── logistic-regression-design = {dependent: availability=Yes; covariates: year + journal; reference: IEEE TSE}
│   └── effect-size = {year odds ratio = 2.31 per 3-year; journal coefficients (CSR, SPE, JSEP, IST 显著为负)}
│
├── [b5] motivation & action schema（论证与建议）
│   ├── reasons-for-artifact ∈ {Replicability, Trust, Updates, Pathway to Automation}（§1 四条）
│   ├── recommendation ∈ {mandatory artifact publishing, permanent repo + DOI, dedicated section, quality assessment as future study}
│   └── time-sensitivity = {2023 年 19 个非永久链接已 2 dead → dead-link 是时间敏感事实}
│
└── [b6] threats & external validity boundary（外推边界）
    ├── excluded-population = {conference proceedings}（理由：高质量 secondary studies 多在期刊 + ISSN 不稳）
    ├── single-database = {Scopus only}（理由：Scopus 已包含相关库元数据；仅元数据搜索可接受）
    ├── time-window-restriction = {2013--2023}（理由：Zenodo / Figshare 平台上线）
    └── un-discussed-risks = {keyword recall, link checkpoint timestamp, artifact content quality}

# 通用迁移接口层（保留当前 6 leaf 作为跨论文 schema 对齐入口，但**不再充当本文原文 schema**）
[interface-scope] [interface-corpus] [interface-taxonomy] [interface-method] [interface-evidence] [interface-finding]
  - 这 6 个 interface leaf 仅用于跨论文聚合时的字段对齐，不参与本文原文 schema 复原。
  - 当前 review.md `维度树结构` 把它们当作主叶子，是本审计 C 级核心问题。
```

**说明**：当前 `review.md` 已经具备做这件事的全部素材（§2.5--§2.8、§3 dimension pattern、§5 历史草稿字段树、§“原文模式候选叶子映射”），只需要把这些素材**从历史草稿 / 候选种子位置抬升到 `维度树结构` 主干 + 叶子**，并把六个通用 interface leaf 降为对齐入口；不需要新增任何原文之外的字段，不存在“为凑完整而臆造原文没有的字段”的风险。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主 `维度树结构` 用通用 6-leaf 接口替代原文 schema | review.md line 222--235 | 用 §4 建议骨架替换：每个主干分支挂**原文真实字段**（availability 四态 / permanent-repo flag / repository-provider 白名单 / dedicated-section flag + 内容子类型 / year / venue / logistic regression covariates / Krippendorff α / IC1-3 / Python keyword 抽取流程 / Replicability-Trust-Updates-Automation 四条 reason），保留 6 个通用 leaf 作为接口层 alignment anchor 而非主叶子。 | `paper_content.txt` Page 1--5；`review.md` §2.5--§2.8、§3、§5 已有素材 | C |
| 主干分支 b2 "artifact type" 在原文不存在 | review.md line 218（"主干分支"列）+ line 226 | 改为 b2 = "research-artifact availability schema"。原文明确不做 artifact 类型本体，只做 availability + location + reporting 三轴。 | `paper_content.txt` §2.3 + §3 RQ1--RQ3 | C |
| 主干分支 b5 "reproducibility gap" 是 finding 而非 schema branch | review.md line 218 + line 232 | 把 b5 拆为 b5 motivation & action（Replicability / Trust / Updates / Automation + recommendation）和 b6 threats & external validity（excluded conferences / Scopus only / 2013--2023 window）。trend & venue 因素单列为 b4。 | `paper_content.txt` §1 + §4 + §5 | C |
| 主干-叶子映射机械错位 | review.md line 223--234 | 现状 b1→scope / b2→corpus / b3→taxonomy / b4→method 的机械 1:1 映射应废弃，改为按 §4 骨架把多个原文字段挂在同一主干下，并保留接口层 leaf 单独成节作 alignment。 | review.md 内部一致性 + `paper_content.txt` schema | I |
| 叶子取值空间过抽象 | review.md line 240--246 "取值空间"列 | 把六个 interface leaf 的“取值空间”改写为接口语义；新增主表（§4 骨架对应行）使用原文封闭原子集（如 availability ∈ {Yes, No, By Request, Dead Link}）。 | Page 3 Table 1a / 1b + §2.3 | C |
| 三类分母未写死 | review.md line 271--275 "统计与候选发现链路" | 在统计用途列明确写出三类分母：537 全体 / 169 含 artifact 子集 / 79 篇 2023 子集 / <10 篇被回归排除的 venue 子集，并写明 `permanent_repo / 169` 与 `permanent_repo / 537` 是两个不同指标，不可混用。 | `review.md` §2.7 自身已警示 + Page 3 Table 1 footer | I |
| 关系边缺失原文核心关系 | review.md line 264--267 关系边表 | 至少补三条：(a) `[edge-availability-permanent-repo]` 子集关系：permanent repo ⊂ availability=Yes（38.5% vs 12.1% 双分母对照）；(b) `[edge-availability-dedicated-section]` 不重合关系：dedicated section ≠ 真有可复现 artifact（§5 反例）；(c) `[edge-year-availability]` / `[edge-venue-availability]` 解释边：logistic regression year odds ratio 2.31 / 3-year，journal 系数显著性。 | Page 3 Table 1 + §5 + §3 RQ4 | I |
| 候选 finding 路径未登账 5 条原文 finding | review.md A.3 结论-证据映射 | 新增至少 5 条 `candidate_finding` 行：(1) artifact-availability-improving-trend；(2) permanent-repo-gap；(3) dedicated-section-false-transparency；(4) dead-link-time-sensitivity；(5) journal-effect-significance。每条挂 `weak / candidate_finding`，引用 `EV-...-stat`（升级证据后），不得升级为 final research finding。 | Page 3--5 §3 + §5 | I |
| A.2 五条 EV-* 全部 `not_verified` 过度降级 | review.md A.2 line 295--301 "证据强度"列 | `paper_content.txt` 已按 Page 1--6 分页；GUIDE.md `证据等级`枚举中“全文文本级；图表待人工核对”可直接采纳。建议把 EV-001 / EV-002 / EV-003 / EV-004 升级为 `paper_text_full`（保留 EV-005 表格交叉关系待 PDF 视觉核验作为 `paper_text_full` 但 needs_manual_check）。同时把“原文页码”列从“摘要 / 引言页；待 A2a 精确页码复核”改为具体页号 + 章节号（Page 1 §Abstract / Page 2 §2.1--§2.3 / Page 3 Table 1 / Page 4 §3 RQ2--RQ4 + §4 / Page 5 §5）。 | `paper_content.txt` 已有分页 + GUIDE.md §3 证据等级 | I |
| A.1 缺 metadata.json | review.md A.1 line 286--291 | 新增一行 `[src-research-artifacts-secondary-studies-meta]` 指向 [metadata.json](../metadata.json)，类型 `publisher_metadata`，用途“出版日期 / venue / 年份口径与 bibtex.bib 交叉核对”。 | review.md 自述 §1 已提及 metadata.json | M |
| 原文模式候选叶子映射停留在 schema_seed 但缺映射到 A2a 工作单元 | review.md line 252--259 "A2a 精核任务"列 | 当前所有行写同一句“核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义”。应**逐行差异化**：availability-status 行写“核对 Table 1a 全 venue 行四态求和=Total，Table 1b 全年度四态求和=各列 Total”；repository-provider 行写“核对 §2.3 永久仓库白名单是否仅 {Zenodo, Figshare, Mendeley Data} + Zenodo 工件内部清单”；trend-context 行写“核对 Table 1c 11 行系数 + reference category + <10 篇排除规则”。 | Page 2--4 Table 1 + §2.3 | I |
| `eligible_for_statistical_synthesis` 与 metadata.json 一致性 | review.md 与 metadata.json 双侧 | 本文是系统映射 + 回归分析，按 pattern-field-schema.md 第 4 节定义 `eligible_for_statistical_synthesis` 候选值为 `true`；但本审计未读 metadata.json，无法核对当前字段是否一致。请在修正主干分支后同步核对 metadata.json `eligible_for_statistical_synthesis` / `evidence_role` / `review_type=systematic mapping` 是否与正文一致。 | pattern-field-schema.md §4 + metadata.json | M |
| “一句话结论”过于自我循环 | review.md line 208 | 当前句“候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed”是合理的降级；但建议追加一句具体化结论：“本文真实抽取 schema 为 6 列 venue × {Yes, No, By Request, Dead Link, Permanent repo, Dedicated section}，A1-DT 应直接复原该 schema 而非仅 6 个通用接口”，让一句话结论与 §4 § 5 修复方向对齐。 | Page 3 Table 1 + 本审计 §4 | M |
| `clm-research-artifacts-secondary-studies-tree-type` 描述待精炼 | review.md line 307 | 当前 tree_type 写“证据资产审计树 + artifact availability 统计树”，方向正确；建议补充“+ logistic regression 趋势解释树”作为第三个 sub-type，因为 RQ4 在原文是与前三个 RQ 并列的独立证据维度。 | Page 3 Table 1c + §3 RQ4 | M |
| `审计附录 A.4` 视觉核验状态停留 needs_manual_check | review.md line 325 | 不强求本 PR 完成 PDF 视觉级核验，但建议把 needs_manual_check 拆为：(a) Table 1a/1b/1c 三个子表数值校验、(b) §2.3 keyword 列表（原文未给出完整 keyword 集合）核验、(c) Zenodo 工件内部清单核验三条具体待办，方便 A2a 入口。 | review.md §7 已有 6 条待复核 | M |

## 6. C/I/M 结论

- **C（critical，直接破坏 Paper2 A1-DT 学术目标 / 证据链）**：
  1. 主 `维度树结构` 用 6 个通用 interface leaf 充当原文 schema → 把原文 schema 复原降级为 0，破坏 A1-DT 对 A2a 的脚手架贡献。
  2. b2 "artifact type" 是原文不存在的字段（原文明确不做 artifact 类型本体），写入主干会反向污染 A2a 跨论文聚合。
  3. b5 "reproducibility gap" 是 finding 而非 schema，写入主干会把 finding 与 schema 混层。
  4. 叶子取值空间全部抽象化，未把原文封闭原子集（availability 四态、repository 白名单、dedicated-section flag）落地，A1-DT 的字段合同失效。
- **I（important，会实质影响维度树可用性与证据可审计性）**：
  1. 主干-叶子机械 1:1 错位（b1→scope / b3→taxonomy 等语义不自洽）。
  2. 三类分母（537 / 169 / 79）未写入“统计用途 / 分母”字段，已知风险未登账。
  3. 关系边表只有 2 条，未刻画 permanent-repo ⊂ Yes、dedicated section ≠ 真有 artifact、year/venue → availability 三类原文核心关系。
  4. A.3 未把原文 5 条 candidate finding（趋势 / permanent-repo gap / 虚假透明度 / dead-link 时间敏感 / journal-effect）登账。
  5. A.2 五条 EV-* 全部 `not_verified`，但 `paper_content.txt` 已分页可锚定，至少应升级为 `paper_text_full`。
  6. “原文模式候选叶子映射”A2a 精核任务 6 行同一模板，未差异化到 Table 1 子表 / §2.3 keyword / Zenodo 工件。
- **M（minor，不阻塞 A1-DT 学术目标）**：
  1. A.1 缺 metadata.json source。
  2. 一句话结论与 tree_type 描述可进一步具体化。
  3. metadata.json 与正文 `eligible_for_statistical_synthesis` / `evidence_role` 待交叉核对。
  4. A.4 needs_manual_check 可拆细。

- **最终建议**：**NEEDS FIX**。
  - 阻塞理由：4 项 C 级问题（主 schema 复原失败、b2/b5 主干语义错、取值空间不可执行）直接导致 A1-DT 对该篇的 schema seed 贡献趋近于零；如果就此进入 A2a，A2a 必须重做 RQ 复原，A1-DT 阶段的工作几乎无法增量利用。
  - 推荐修复顺序：先按 §4 骨架重写 `维度树结构` + 叶子表（解 C1--C4），再升级 EV-* 证据强度与具体页号锚定（解 I5），再补 candidate finding 登账与关系边（解 I3--I4），最后处理 M 级补漏。
  - 修复后无需重做 PDF 视觉级核验即可重审，因为所有 C/I 修复证据已在 `paper_content.txt` 全文文本内。
