# research-artifacts-secondary-studies：A1 S1--S8 round3 单篇维度抽取审计

## 0. 审计边界与阅读状态

- **处理对象**：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/research-artifacts-secondary-studies`。
- **本轮角色**：A1 survey-of-surveys 单篇维度抽取；未开启 sub-subagent。
- **输出边界**：本文件只做 A1 文本级独立审计；只写入当前 round3 audit 文件，不直接修改 `review.md`、`evidence_chain.md` 或 `SUMMARY.md`。
- **总体判定**：该文是完整的 software engineering secondary studies research artifacts systematic mapping，样本单位为每篇 secondary study，最终纳入 $n = 537$。可作为 A1 的 `schema_seed` / 后续主统计池候选，但 A1 文本级结论不得写成 Paper2 final quantitative finding。

| 材料 | 阅读状态 | 依据与边界 |
|---|---|---|
| `bibtex.bib` | 已读全文 | 确认 `Huotala_2025`、IST、2025、DOI `10.1016/j.infsof.2025.107830`。 |
| `metadata.json` | 已读全文 | 确认本地元数据标注为 `systematic mapping`、`eligible_for_statistical_synthesis=true`、`systematic_mapping_pattern`；但 A1/A2a 前仍只能作为候选统计池。 |
| `paper_content.txt` | 已读全文 | 358 行；覆盖摘要、§1 动机、§2 方法、§3 RQ1--RQ4 结果、§4 limitations、§5 conclusion/data availability 与 references。关键锚点：摘要 8--16 行；检索式 58--86 行；纳排与 537 分母 87--104 行；抽取流程 105--117 行；Table 1 136--180 行；RQ2/RQ3/RQ4 184--219 行；limitations 220--237 行；conclusion 238--277 行；Zenodo data availability 295--297 行。 |
| `review.md` | 已读全文 | 1--435 行；重点复核“维度树复原”147--397 行与 “survey_of_surveys 自身 schema 抽取”401--431 行。 |
| `evidence_chain.md` | 已读全文 | 1--47 行；A.1--A.4 均已读，重点核对 `A1DT-research-artifacts-secondary-studies-C01--C04`。 |
| `paper.pdf` | 已做必要文本级核对 | `pdfinfo` 显示 6 页；用 `pdftotext -layout` 核对 Table 1(a)/(b)/(c)。本轮未打开 Zenodo，也未做 publisher final 与截图级视觉核验。 |

## 1. 原文如何描述“样本集合 / 编码对象 / 分母”

1. **样本集合**：2013--2023 年发表于 15 个期刊的 SE secondary studies；检索初始结果为 643 篇，IC1--IC3 筛选后最终纳入 537 篇。这里的 537 是本文的 primary sample denominator。
2. **ISSN token 与 journal 数**：检索式中出现 **16 个 `ISSN(...)` token**，正文随后说明这些 token 覆盖 **13 个 SE-related journals + 2 个 broader CS review journals = 15 个期刊**。因此应写作“16 个 ISSN token / 15 个期刊”，不要写成“15 个 ISSN”。
3. **编码对象**：每篇 secondary study 被编码的不是其研究主题，而是 research artifact 的可获得性、存储持久性、报告方式与上下文元数据。
4. **artifact availability 主字段**：Table 1 的主可获得性状态按总体分母互斥计数为 `Yes / No / By request / Dead link`，总计 $169 + 330 + 16 + 22 = 537$。`Dead link` 不应只被当作一个独立可选布尔叶子而丢失其“总体状态类别”语义。
5. **permanent repository 字段**：`Permanent repo` 是 `Yes` 子集中的持久仓库 + DOI 统计，核心分母是 $65/169 = 38.5\%$；同时作者也报告其占全体样本的 $65/537 = 12.1\%$，并在 2023 年报告 $24/79 = 30.4\%$。两种分母必须同时保留且不可混用。
6. **reporting 字段**：`Dedicated section` 是论文是否有专门 data/artifact availability section 的报告方式字段；Table 1(b) 报告全样本 $72/537 = 13.4\%$，正文 RQ3 又报告在有 artifact 的 169 篇中有 $50/169 = 29.6\%$。它不是 artifact 真正开放的同义词。
7. **Zenodo 边界**：正文脚注和 Data availability 指向 Zenodo DOI `10.5281/zenodo.15488074`，但本轮未打开 Zenodo，不能声称已核验逐篇编码表、sample ID、artifact URL、脚本、关键词列表、link-check 日期、license 或 artifact type taxonomy。

## 2. S1--S8 五分栏抽取

> 判定等级只说明该论文对本目录二级 schema 的可用程度。表内数字均为原文内部统计 / A1 文本级证据，不是 Paper2 final quantitative finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要说明目标是评估 SRs 如何报告 research artifacts，并分析 537 篇 2013--2023 secondary studies 的 availability/reporting；§3 明确 RQ1 artifact 比例、RQ2 存放位置、RQ3 data availability 声明、RQ4 年份/venue 影响。 | 任务树是“SE secondary studies 的 artifact reporting / availability audit”：对象为 secondary studies；核心问题围绕 artifact 是否可直接获得、是否持久存储、如何声明、是否随年份/venue 变化。 | **强；后续候选。** 可作为 A1 的综述任务设定与 RQ-to-field contract 样本；只贡献方法模式，不贡献目标领域事实。 | 核对 IST publisher final 与 arXiv v3 对摘要、RQ 表述和页码是否一致。 |
| S2 语料收集与筛选 | §2.1--§2.2：2024-10-02 用 Scopus；检索式含 16 个 ISSN token，覆盖 15 个期刊；标题限定 review/mapping/meta-analysis/scoping/critical 等词；2013--2023 年；643 初始结果，经 IC1 年份、IC2 secondary study、IC3 SE-related 筛选后 $n=537$；对 CSUR/Computer Science Review 做人工 SE 相关判定并报告 Krippendorff's Alpha=0.776。 | 可复原完整分母链：Scopus + ISSN token + title terms + year window → title/abstract screening → 两个 broad CS journal 的 SE-related 人工判定 → final included secondary studies。 | **强；后续候选。** 可用于“系统语料构造与分母链是否可复核”的统计池候选；643 是检索候选数，537 才是样本分母。 | 精核检索式中 16 个 ISSN token 对 15 个期刊的映射；核对 alpha 计算对象、人工筛选范围和是否有 Zenodo protocol。 |
| S3 原生维度树 / 样本编码对象 | §2.3 说明人工全文筛查 dedicated section、脚本关键词搜索并人工检查上下文；检查是否引用 external resource、是否位于 Figshare/Zenodo/Mendeley 等 permanent repository。Table 1(a)(b) 给出 year、venue、Yes/No/By request/Dead link、Permanent repo、Dedicated section。 | 原生树应是**扁平单表单树**：上下文元数据（year、venue）× artifact 可获得性/报告字段（availability status、permanent repo 条件字段、dedicated section）。**logistic regression、odds ratio、p value 是由这些字段派生出的 S6 统计分析层，不是 S3 原生逐样本叶子。** | **强；带边界候选。** 可统计为“有明确样本单位和可复原编码字段”；但若 `review.md` 把 logistic regression 放进原生树，应在回填时修正。 | 打开 Zenodo 逐篇清单，确认是否存在 sample ID、title/DOI、artifact URL、repository type、artifact type、keyword hit、link-check 日期等正文未展开字段。 |
| S4 字段级证据 | 正文 Table 1 给出聚合计数与比例；§2.3 给出抽取流程；Data availability 指向 Zenodo。当前本地文件没有逐篇原始编码表。 | 字段级证据分两层：正文聚合表可支撑字段存在与总体统计；sample-level evidence 依赖 Zenodo，当前未核验。 | **中；有条件候选。** 可统计为“有字段和聚合表”，不得统计为 sample-level artifact list 已闭合。 | 打开 Zenodo DOI，核验逐篇编码表、字段名、脚本、关键词、link-check 日期、license、版本；核对 Table 1 百分比分母与 IST By Request 百分比疑点。 |
| S5 维度模式演化 | 原文说明按 Petersen guideline 和 SIGSOFT Empirical Standards checklist 执行，并描述人工/脚本两轮抽取；没有说明 codebook 如何形成、pilot/open coding、冲突讨论或版本修订。 | 可复原为静态先验字段 + 抽取流程；year trend 是字段取值随时间变化，不是 schema evolution。 | **弱；边界样本。** 可作为“未报告维度形成过程”的反例，不应计为有完整 schema evolution。 | 核验 Zenodo 是否包含 protocol、codebook revision、pilot notes、coder discussion 或 disagreement log；若没有，保持 S5=弱。 |
| S6 统计分析 | Table 1(a) venue 交叉表；Table 1(b) 年度统计；Table 1(c) binary logistic regression。正文报告 $169/537$、$65/169$、$65/537$、2023 年 $49/79$ 与 $24/79$，并说明 year 的 odds ratio 为 2.31。 | 统计分析层从 S3 字段派生：frequency/proportion、year trend、venue comparison、binary logistic regression。该层可以和原生树相连，但不应作为原生叶子。 | **强；后续候选。** 可作为“字段级数据 → 聚合统计/模型”的方法样本；具体比例、odds ratio、venue 差异只属于 SE secondary studies。 | PDF 视觉核验 Table 1(a)(b)(c)；核对 less-than-10 publications 的回归排除规则；比较 publisher final 与 arXiv 表格。 |
| S7 候选 finding | §3/§5 从统计观察推出 artifact availability 上升、permanent repo/DOI 不足、non-permanent link 易失效、Data Availability section 可能只写 no data 或 upon request，并建议强制发布 artifact。 | finding 链是“字段统计 → availability/persistence/reporting gap → 政策建议 / future work”。其中 `no data was used` 是定性观察，未给频次。 | **强但限界。** 可作为候选 finding 生成模式；不得迁移 $31.5\%$、$62.0\%$、$30.4\%$、具体期刊差异或 SE improvement trend 为 Paper2 目标领域 finding。 | 核验每个 discussion claim 与 Table 1/Zenodo 的对应；特别确认 `no data was used` 是否有逐篇频次。 |
| S8 研究者 / 作者质疑与裁决 | §2.2 报告人工 SE-related 判断和 Krippendorff's Alpha；§2.3 报告人工全文筛查与人工检查关键词上下文；§4 明确排除会议、单一 Scopus、2013--2023 时间窗等限制。 | 可复原质量控制树：人工筛选、inter-rater reliability、人工上下文核验、limitations；但缺少公开完整 disagreement adjudication log 和字段级双人编码一致性记录。 | **中；有限候选。** 可统计为存在人工复核/质量控制，不可统计为完整双人独立筛选 + 抽取 + 裁决日志。 | 核验 Zenodo 是否提供 reviewer 分工、冲突裁决、关键词列表、manual override、link-check 时间戳。 |

## 3. 原生维度树 / 维度森林复原

> 结论：本文不是维度森林，而是一棵以“每篇 secondary study”为行单位的扁平单表原生编码树；另有一层派生统计分析层。派生统计层可记录为 S6 / relation / analysis output，但不得写成原生叶子。

```text
[根节点] SE secondary study research artifact audit
样本单位 = 每篇 included secondary study
最终分母 = 537
检索候选数 = 643
检索源 = Scopus；16 个 ISSN token 覆盖 15 个期刊；2013--2023；title review/mapping/meta-analysis/scoping/critical terms
统计池资格 = A2a 后候选；A1 文本级不得进入 final quantitative finding

├── [树 A：上下文元数据]
│   ├── [leaf-year] 发表年份
│   │   取值空间 = {2013, 2014, ..., 2023}
│   │   用途 = 年度趋势与回归 predictor
│   └── [leaf-venue] 发表期刊 / publication channel
│       取值空间 = 15 个期刊（Table 1(a) 行）
│       用途 = venue 交叉表与回归 predictor
│
├── [树 B：artifact 可获得性 / 报告字段]
│   ├── [leaf-availability-status] research artifact availability 主状态
│   │   取值空间 = {Yes, No, By request, Dead link}
│   │   分母 = 全部 537；四类互斥并合计 537
│   │   注 = Dead link 是总体状态类别之一，不只是 Yes 子集上的随意布尔标签
│   ├── [leaf-permanent-repo] permanent repository with DOI
│   │   取值空间 = {true, false / not permanent, not applicable}
│   │   主分母 = Yes 子集 169，统计为 65/169 = 38.5%
│   │   另一个报告分母 = 全体 537，统计为 65/537 = 12.1%；2023 年为 24/79 = 30.4%
│   ├── [leaf-dedicated-section] dedicated data/artifact availability section
│   │   取值空间 = {true, false}
│   │   全样本统计 = 72/537；有 artifact 子集统计 = 50/169；2023 年 = 46/79
│   │   注 = 有 dedicated section 不等于有真实开放 artifact
│   └── [leaf-artifact-quality] artifact content quality
│       取值空间 = not evaluated in this paper
│       注 = 作者把 quality evaluation 列为 future work；不能本地补造质量叶子
│
└── [派生统计层：不是原生树叶子]
    ├── [analysis-frequency] venue/year 频次与比例表
    ├── [analysis-denominator-switch] 537 全体、169 Yes 子集、79 个 2023 子集等分母切换
    ├── [analysis-logistic-regression] binary logistic regression: year + journal → artifact availability
    └── [analysis-finding] availability improving / permanent repo insufficient / reporting risk / policy recommendation
```

### 3.1 关系边与缺失语义

| 边或缺失项 | 类型 | 源 → 目标 | 缺失值 / 不适用语义 | 审计结论 |
|---|---|---|---|---|
| `availability → permanent_repo` | 条件字段 | `availability-status=Yes` → `permanent-repo` | 非 `Yes` 样本上 `permanent_repo` 不应与 false 混写；统计时必须说明是 65/169 还是 65/537。 | 关键 denominator 风险。 |
| `dedicated_section ↔ availability` | 报告字段与真实可获得性关系 | `dedicated-section` → `availability-status` | 有 section 可写 no data / upon request；不是开放 artifact 的充分条件。 | 关键 reporting 风险。 |
| `year/venue → availability` | 派生统计关系 | context fields → availability status | 模型输出为 S6 派生统计，不是逐篇编码叶子。 | 需从原生树移出。 |
| `Zenodo artifact → sample-level evidence` | 待核验证据链 | 正文 DOI → supplementary data | 未打开则所有逐篇清单、sample ID、artifact URL、脚本、link-check 时间均为 `not_verified`。 | 不能升级 sample-level closure。 |

## 4. 对 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

| 等级 | 文件 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| C | -- | 未发现需要立即阻断 A1 的 critical 问题。 | 当前大方向已正确识别为 systematic mapping、537 secondary studies 与 artifact-audit 方法样本。 | -- |
| I | `review.md`、`evidence_chain.md` | 当前 `review.md` 维度树卡片和代码块仍把“统计建模输出 / logistic 回归系数”作为第三主干或 `[leaf-回归]`；`evidence_chain.md` 的 C03 也写成“三主干（上下文元数据 × 制品可获得性 × 统计建模）”。 | 会把 S6 派生统计层误写成 S3 原生样本编码叶子，破坏原生树 / 跨论文投影层分离。 | 将原生树改为“上下文元数据 × artifact availability/reporting 字段”的扁平单表树；把 logistic regression、odds ratio、p value 移到 S6 派生统计层 / 关系边 / analysis output。 |
| I | `review.md`、`SUMMARY.md` | 多处写法容易把“15 个期刊”与“ISSN token 数”混同；`review.md` 证据锚点曾写“15 个 ISSN”，而原文检索式实际有 16 个 `ISSN(...)` token，正文说覆盖 15 个期刊。 | 检索协议复现会出现 token 数与 journal 数不一致；A2a 可能误判检索式。 | 统一写作“16 个 ISSN token，覆盖 13 个 SE-related + 2 个 broader CS review journals，共 15 个期刊”。 |
| I | `review.md` | `leaf-availability` 现写为 `Yes / No / By Request`，又把 `Dead link` 单独列为链接布尔；但 Table 1 的主 availability 分布是 `Yes / No / By req. / Dead` 四类互斥并合计 537。 | 可能导致 availability 主字段语义错误、Dead Link 被重复或漏计，进而污染 S3/S6 字段合同。 | 将主字段写为 `availability_status={Yes, No, By request, Dead link}`；另可保留 `link_health` 作为解释性派生/质量字段，但需声明其来自 Dead Link 状态而非独立全样本布尔。 |
| I | `review.md`、`SUMMARY.md` | permanent repository 的两种分母需要更醒目地区分：65/169 是 Yes 子集比例，65/537 是全样本比例，24/79 是 2023 年全样本比例。 | 若 SUMMARY 或后续统计表只保留一个百分比，容易把“有 artifact 的持久化率”与“全体论文持久仓库覆盖率”混算。 | 在字段名或图注中写明 `permanent_repo_among_artifact_yes` 与 `permanent_repo_overall`；所有引用同时带 numerator/denominator。 |
| I | `review.md` | §6.1 中部分统计观察标为 `strong（直接计数）`，而 `evidence_chain.md` A.2/A.3 仍多为 `not_verified` / A2a 待精核。 | 后续摘录时可能把 A1 文本级或 PDF-layout 级核对误读为 final quantitative finding。 | 改写为“原文内部直接计数强；A1 使用层级仍为文本级 / A2a 待精核，不进入 final quantitative finding”。 |
| I | `review.md`、`evidence_chain.md` | Zenodo 边界总体有说明，但 evidence chain 未把“Zenodo 未打开”作为独立证据缺口 / A2a checklist 项绑定到 S4/S8。 | 逐篇 sample-level evidence、脚本、关键词、link-check 时间戳可能被误认为已核验。 | 在 A.4 增加 Zenodo DOI 打开与文件清单核验项；S4/S8 相关结论保持 `not_verified`，直到 replication package 精核完成。 |
| M | `review.md` | `leaf-permanent` 同时写“全样本字段：适用于全部 537 篇”和“条件可见”，语义略冲突。 | 不一定影响结论，但人类读者难以判断非 Yes 样本应填 false 还是 N/A。 | 明确 raw field 是 Yes 子集条件字段；overall rate 是派生统计。 |
| M | `evidence_chain.md` | A.2 多处用“短引见 review.md”或泛化章节代替原文短引、页码、表号。 | A1 最小链路可接受，但 A2a 之前不能升级为精确证据。 | A2a 将核心证据补为精确页码 / 表号 / 行号 / 原文短引。 |
| M | `SUMMARY.md` | 主表“证据资产审计树 + artifact availability 统计树”可读，但仍可能让人把统计模型当作树的一部分。 | 轻度命名风险。 | 改为“artifact availability/reporting 原生字段树 + S6 派生统计分析”。 |

## 5. 审计结论

本篇 A1 价值很高，但边界必须写窄：它能提供 **secondary-study artifact audit 的字段合同**、**537 篇系统映射的分母链**、**availability/reporting/persistence 字段** 和 **从字段到统计 finding 的方法模板**；它不能提供 Paper2 目标领域的最终比例或趋势。当前最需要返修的是把 logistic regression 从原生树中移出、把 availability 主字段改为四类互斥状态、把 ISSN token 与 journal 数分清，并把 Zenodo 未打开造成的 sample-level 证据缺口显式挂到 A2a。
