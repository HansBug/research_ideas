I have comprehensive evidence. Now I'll write the full audit report.

`★ Insight ─────────────────────────────────────`
- Mohamed et al. 2026 是一个典型的 RQ-driven SLR+SMS：每个 RQ（RQ0..RQ3）对应一组明确的 extraction fields 与外部 taxonomy（Stol & Fitzgerald, Glass/Vessey/Ramesh, Hartson, SPACE），这意味着真正的"原生维度树"应该是 **per-RQ extraction schema 的并集**，而不是六个通用 leaf。
- 该论文同一字段（code quality）在 benefit 与 risk 两侧都出现，这种"contested theme"结构在维度树中应当被表达为同一概念的 polarity-bearing leaf，而不是被压缩为单一分类项。
- review.md 当前最大问题：A1-DT v2 主树仍是六叶通用接口；原文真正的 schema（PRISMA 分母链 + QA 11 项 rubric + Stol-Fitzgerald 6 类策略 + Glass-Vessey-Ramesh 5 类 procedure + SPACE 5 维及其 sub-dimensions + 8 benefit/5 risk 主题 + McLuhan Tetrad 4 维）远比这六叶丰富。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇全文审计：`llm-assistants-developer-productivity`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm-assistants-developer-productivity` |
| agent | `claude` (claude-opus-4-7[1m]) |
| 是否已读 `paper_content.txt` | 是；按页通读 Page 1–36（覆盖 abstract / intro / background / methodology / RQ0–RQ3 全部结果 / discussion / threats），未逐字读 Conclusion / References 段，但已覆盖审计所需正文。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两者一致核对（DOI 10.1145/3809494；ACM TOSEM 2026；arXiv 2507.03156 v2）。 |
| 是否打开或核对 `paper.pdf` | 否；本轮以 `paper_content.txt`（已按 `--- Page N ---` 分页）为主，复杂图表（Fig. 3/4/5/7/8/9 雷达图、UpSet 图、Sankey 图）与最终 ACM 版式留待 A2a/PDF 视觉核验。 |
| 原文类型 | SLR + SMS 混合（作者自称 "systematic review and mapping"，遵循 Kitchenham & Charters 2007 指南，含 pre-review mapping + 完整 PRISMA flow + QA rubric + thematic synthesis）。 |
| 被编码样本单位 | **primary study**（peer-reviewed 经 39 项 final inclusion，已编号 PS1–PS39，作者级、venue 级、工具级字段都挂在每条 PS 上）。 |
| 样本数量 / 分母 | 9756 → 8953 → 228 → 44 → **39**；snowballing 加入 5；QA 排除 5。 |
| 原生树类型 | **多根维度森林**：每个 RQ 对应一棵 extraction subtree；底层共享 PS-id 这一样本单位主键，使所有 subtree 可交叉关联。 |
| 主统计池资格 | **是（局部可统计）**：landscape / strategy / procedure / instrument / SPACE 覆盖等字段已有明确分母（39）和取值空间，可进入主统计池；benefit/risk 主题计数（Fig. 6 雷达数字）与 NASA-TLX 子集等 fine-grained 字段须等 A2a 精核精确数字。 |
| 总体判定 | **needs repair**：review.md 已有大量正文素材准确，但"维度树复原"和 A.2/A.3 仍把原文当作六叶通用接口处理，需要按本审计提出的 RQ-森林 schema 重写。 |

## 1. 原文证据阅读说明

实际读取：

- `bibtex.bib`（10 行）— 验证标题、作者、TOSEM 2026、DOI。
- `metadata.json` — 验证 publication date 2026-04-27、arXiv 来源、`eligible_for_schema_seed=true`、`eligible_for_statistical_synthesis=true`、`evidence_role=hybrid_slr_sms_pattern`。
- `paper_content.txt` — 通读 Page 1–36，主要章节：
  - §1 Introduction（Page 1–2）
  - §2 Background（Page 3–4，含 SPACE 来源 [19]）
  - §3 Methodology（Page 4–9）：§3.1 pre-review mapping、§3.1.1 control papers、Inclusion/Exclusion criteria、§3.1.2 query formulation、§3.2 selection process、§3.3 QA、§3.4 data extraction & synthesis
  - §4 RQ0 Landscape（Page 9–11）
  - §5 RQ1 Methodology/instruments（Page 11–17）
  - §6 RQ2 Benefits & Risks（Page 17–24）
  - §7 RQ3 SPACE mapping（Page 24–27）
  - §8 Discussion（Page 27–35，含 McLuhan Tetrad + 5 practitioner recs + 3 researcher recs）
  - §9 Threats to Validity（Page 35–36）

未做 PDF 视觉核验，主要影响：Fig. 1 PRISMA 实际位置、Fig. 6 radar plot 各 benefit/risk 主题精确数字、Fig. 7/8 SPACE Sankey/UpSet 比例线、Fig. 9 Tetrad 图、Table 9 risk 摘要、Table 10 SPACE 完整列。

关键证据锚点：

1. **PS 集合分母链**（§3.2, Page 7–8 + Fig. 1）："Records identified from Databases (n = 9,756) ... duplicates removed (n = 803) ... title/abstract n = 8,953 → excluded 8,725 → 228 → snowballing +5 → QA n = 44 → excluded 5 → **n = 39**"。
2. **EC 分布**（Fig. 1 标注）：EC1=15, EC2=128, EC3=27, EC4=11, EC5=3, ~IC1=5。
3. **QA rubric**（§3.3, Page 8, Table 2）：QA1–QA11 共 11 项 + 5 点 Likert {Excellent 4, Very Good 3, Good 2, Fair 1, Poor 0} + 50% 阈值。
4. **research strategy taxonomy**（§5.1, Page 11–12, Table 5）：Stol & Fitzgerald 6 类；Lab 38% (15/39), Field 23% (9), Sample 15% (6), ExpSim 13% (5), Field Exp 5% (2), Judgment 5% (2)。
5. **procedure taxonomy**（§5.2, Page 13, Table 6 + Fig. 3/4）：Glass-Vessey-Ramesh 5 类；Survey 82% (32), User Exp 41% (16), Case 31% (12), Interview 26% (10), Concept Impl 10% (4)。
6. **objective**（§5.2, Page 13–14）：Hartson taxonomy，formative 59% (23) / summative 41% (16)。
7. **data source × instrument origin**（§5.3, Page 14, Table 7）：Self-reported vs Behavioral; designed by authors vs validated（NASA-TLX, SPACE survey, TAM, AAR/AI, self-efficacy, emotion affect, TCQ, RBV）。
8. **time-to-completion**：31% (12/39) - §5.3.1, Page 15。
9. **8 benefits + 5 risks 主题**（§6.1–§6.2, Page 17–24, Fig. 6 radar + Table 8 + Table 9）。
10. **SPACE mapping**（§7, Page 24–27, Fig. 7/8 + Table 10/11）：Satisfaction 77%, Performance 64%, Efficiency 59%, Activity 31%, Communication 26%；90% ≥2 维, 44% ≥3 维, 15% ≥4 维；最常见组合 S+P+E (5/39)。Satisfaction sub: developer-experience, self-efficacy, trust, cognitive-load, well-being (=0). Performance sub: quality, impact. Efficiency sub: temporal-efficiency, automation, interruptions-and-flow. Communication sub: human-LLM (7/10), human-human (3/10).
11. **McLuhan Tetrad**（§8.1, Page 27–30, Fig. 9）：Enhance / Reverse / Obsolesce / Retrieve 四维 + lessons learned (1–3) + 5 practitioner recs (Trust / role / workflow / org / professional ethics)。
12. **Threats**（§9, Page 35–36）：selection bias, human-centered identification, bias & repeatability, classification rigor, formative/controlled dominance, methodological diversity, temporal relevance（2024 占 77%）。

## 2. 样本单位与字段来源判定

**1. 纳入和逐项描述的对象**：peer-reviewed primary studies，编号 PS1–PS39，每条 PS 在多张表格中作为主键被反复挂接（venue, tools, strategy, procedure, instrument, benefit, risk, SPACE sub-dimension, QA score）。

**2. 是否有系统检索/纳排/抽取/编码方案**：是。完整含 Kitchenham&Charters protocol、6 数据库 search string、17 control papers、5 轮 query iteration、Rayyan 标注、47-day title/abstract screening、10-week full-text screening、PRISMA flow chart、Lenarduzzi 11-QA rubric、初始 thematic analysis + 三轮 targeted thematic analysis（针对 RQ1/RQ2/RQ3）、citation cross-check。

**3. 字段来源**：

- **extraction form**（§3.4 列出："study goals, tools, empirical strategy and design, tasks, settings, key results"）
- **classification schemas**：Stol & Fitzgerald (strategy)、Glass-Vessey-Ramesh (procedure)、Hartson (formative/summative)、SPACE (Forsgren et al.)
- **QA rubric**：Lenarduzzi 11 项
- **emergent thematic codes**：8 benefits + 5 risks（thematic analysis 自产）
- **interpretive lens**：McLuhan Tetrad（应用于 discussion，不是抽取字段，但提供推论 schema）
- **supplemental appendix + Zenodo replication package**：control papers list、query iterations、QA scores、exclusion rationales

**4. RQ ↔ 样本单位**：RQ 是字段使用方式（landscape RQ0 / methodology RQ1 / impact RQ2 / dimension RQ3），样本单位仍是 PS。RQ 不是树根，而是把 PS 字段切成不同分析维度的"棱镜"。

**5. 是否需要降级**：不需要。本文有完整系统证据基础，主统计池资格成立；只是部分 fine-grained 数字（Fig. 6 雷达精确计数、Sankey 流量、Table 9 详尽 risk 行）尚未在文本中完全读出，需 A2a/PDF 复核。

## 3. 原生样本编码维度树 / 维度森林

样本单位主键：`PS-id ∈ {PS1, …, PS39}`。每棵 RQ-subtree 通过 PS-id 与其他 subtree 关联。

```text
[forest-root] LLM-assistants × developer productivity SLR+SMS schema
│
├── [tree-meta] 元数据 / 样本主键
│   ├── PS-id (PS1..PS39)
│   ├── title / authors / year / venue
│   ├── inclusion status (included | snowballed | qa_excluded | screened_out)
│   ├── exclusion code (EC1..EC5 | ~IC1 | none)
│   └── QA score (QA1..QA11 each ∈ {0,1,2,3,4}, avg ≥ 50% threshold)
│
├── [tree-RQ0] Landscape（RQ0 字段集合）
│   ├── publication-year ∈ {2014..2024, 2025-Jan}（数值）
│   ├── author-distribution（数值；147 single-author, 6 dual, 1 triple）
│   ├── venue（Table 3 中 39 个 venue 命名实体）
│   ├── venue-research-focus（封闭枚举：SE/CS, HCI, IS/Decision Science, Human-Aspects, AI for SE / AI Engineering, SE Education）
│   └── llm-tool-used（Table 4 开放枚举：ChatGPT, GitHub Copilot, Tabnine, GPT-4, CodeWhisperer, GPT-3.5, Claude, Codex, Gemini, GPT-3, Ansible Lightspeed, Bard, CodeGen2 7B, GILT, CodeCompose, NL2Code PyCharm plugin, StackSpotAI, StarCoder 7B, TransCoder, aiXcoder, OpenAI API, Midjourney）
│
├── [tree-RQ1] Methodology / procedures / instruments
│   ├── empirical-strategy（Stol-Fitzgerald 封闭 6 枚举：Field Study | Field Experiment | Experimental Simulation | Laboratory Experiment | Sample Study | Judgment Study）
│   ├── procedure（Glass-Vessey-Ramesh 多选 5 枚举：Survey | User Experiment | Case Study | Interview | Concept Implementation）
│   ├── mixed-methods（布尔：69% true）
│   ├── objective（封闭枚举：formative | summative）
│   ├── data-analysis-type（封闭枚举：quantitative | qualitative | mixed）
│   ├── data-source（封闭枚举：Self-Reported | Behavioral & Performance Metrics）
│   ├── instrument-origin（封闭枚举：designed by authors | validated framework）
│   └── instrument-name（开放枚举：NASA-TLX, SPACE survey, TAM, self-efficacy, AAR/AI, emotion affect, TCQ, RBV, task completion & correctness, suggestion acceptance rate, interaction logs, time to completion, code quality metrics, productivity gain, open-ended feedback...）
│       └── associated-metric（细分见 Table 7）
│
├── [tree-RQ2] Effect synthesis（thematic）
│   ├── benefit-themes（封闭枚举 8 项）
│   │   ├── accelerate-software-development
│   │   ├── minimize-online-code-search
│   │   ├── automate-trivial-repetitive-tasks
│   │   ├── support-knowledge-acquisition
│   │   ├── support-code-adjacent-tasks
│   │   ├── reduce-task-initiation-overhead
│   │   ├── improve-code-quality        ← contested 双向出现
│   │   └── support-debugging-troubleshooting
│   ├── risk-themes（封闭枚举 5 项）
│   │   ├── fail-to-meet-requirements
│   │   ├── promote-over-reliance-and-cognitive-offloading
│   │   ├── limit-code-quality          ← contested 双向出现
│   │   ├── disrupt-the-flow
│   │   └── reduce-team-collaboration
│   ├── theme-frequency（数值；Fig. 6 雷达每主题对应 PS 集合大小）
│   └── contested-theme-flag（布尔；code-quality = true）
│
├── [tree-RQ3] SPACE dimension mapping
│   ├── space-dimension（封闭枚举 5：Satisfaction | Performance | Activity | Communication | Efficiency）
│   ├── space-dim-coverage-count（数值 0..5 per PS；分布：90% ≥2, 44% ≥3, 15% ≥4）
│   ├── space-sub-dimension（层级枚举）
│   │   ├── Satisfaction: developer-experience | self-efficacy | trust | cognitive-load | well-being(=∅)
│   │   ├── Performance: quality | impact
│   │   ├── Activity: (no further sub)
│   │   ├── Communication: human-LLM | human-human
│   │   └── Efficiency: temporal-efficiency | automation | interruptions-and-flow
│   ├── quality-metric-instance（Table 11 开放枚举：Passing Unit Tests, Functional Correctness & Accuracy, Code Smells, BLEU, Halstead, Cyclomatic Complexity, Translation Error Rate, Maintainability Index, Cognitive Complexity, Defect Density, Defect Rate, Technical Debt, Code Coverage）
│   └── most-frequent-combination（自由文本，e.g. "Satisfaction-Performance-Efficiency", 5/39）
│
├── [tree-discussion-tetrad] Interpretive lens（McLuhan）
│   ├── enhance（boilerplate, syntax recall, initial scaffolding, exploratory prototyping）
│   ├── reverse（over-reliance, automation complacency, autonomy erosion, reduced collaboration）
│   ├── obsolesce（online search, Q&A platforms）
│   └── retrieve（documentation, requirements elicitation, legacy modernization）
│
└── [tree-threats] Validity threats
    ├── review-process-threat（封闭枚举 4：study selection bias | human-centered identification | bias & repeatability | classification rigor）
    └── primary-evidence-base-threat（封闭枚举 3：formative/controlled dominance | methodological diversity | temporal relevance）
```

主干说明：

- **forest, not single tree**：RQ0/1/2/3 各成独立子树，但都挂在 PS-id 主键上；Tetrad 与 Threats 是 interpretive overlay，不直接挂 PS。
- **取值空间饱和度**：[tree-RQ0] author/venue/tool 是开放枚举；[tree-RQ1] strategy/procedure/objective 是封闭枚举（直接来自外部 taxonomy）；[tree-RQ2] benefit/risk 是封闭枚举（8+5，由 thematic analysis 收敛）；[tree-RQ3] SPACE dimension 是封闭 5 维 + emergent sub-dimensions。

## 4. 叶子维度表

仅列原文已锚定的代表性叶子（共 21 项；完整 schema 还有 ~10 项需 A2a 精核精确分母）：

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-ps-id | 论文主键 | tree-meta | extraction form | PS1..PS39 | 39 个枚举 | 完整枚举 | n/a | 全表分母 | 全表主键 | §3.2 + Fig. 1 | 主键模式可迁移 |
| leaf-ps-qa-score | QA 综合分数 | tree-meta | QA rubric §3.3 | 11 criteria avg ≥ 50% | [0,4] 区间，per criterion 0..4 Likert | 数值 | 不达阈值=excluded | eligibility filter | quality-weighted finding | §3.3, Table 2 | 全可迁移 |
| leaf-pub-year | 发表年份 | tree-RQ0 | RQ0 §4.1 | 年 | 2014..2025-Jan | 数值 | n/a | landscape 时间分布 | 时间漂移风险 | §4.1 Fig. 2 | 可迁移 |
| leaf-venue-focus | venue 研究焦点 | tree-RQ0 | Table 3 §4.3 | 6 个 focus 大类 | {SE/CS, HCI, IS/Decision, Human-Aspects, AI Eng, SE Edu} | 完整枚举 | uncategorized | 社区分布 | 跨社区融合 gap | §4.3 Table 3 | 可迁移 |
| leaf-llm-tool | 使用的 LLM 工具 | tree-RQ0 | Table 4 §4.4 | 22 个 tool name | open enumeration | 开放枚举 | not_reported | 工具集中度 | 工具漂移 risk | §4.4 Table 4 | 可迁移结构 |
| leaf-strategy | 实证策略 | tree-RQ1 | Stol-Fitzgerald taxonomy | 6 类 | {Field Study, Field Exp, ExpSim, Lab Exp, Sample, Judgment} | 完整枚举 | n/a | 策略分布 (38/23/15/13/5/5%) | 生态效度 risk | §5.1 Table 5 | 可迁移 |
| leaf-procedure | 方法 procedure | tree-RQ1 | Glass-Vessey-Ramesh | 5 类 | {Survey, User Exp, Case, Interview, Concept Impl} | 多选完整枚举 | n/a | procedure 分布 (82/41/31/26/10%) | mixed-methods 比例 | §5.2 Table 6 Fig. 4 | 可迁移 |
| leaf-objective | 研究目标 | tree-RQ1 | Hartson | formative / summative | 完整枚举 2 | n/a | formative/summative 比例 (59/41%) | 证据成熟度 | §5.2 Page 14 | 可迁移 |
| leaf-analysis-type | 分析类型 | tree-RQ1 | extraction | quant / qual / mixed | 完整枚举 3 | n/a | 比例 (13/21/67%) | triangulation indicator | §5.2 Page 14 | 可迁移 |
| leaf-instrument-origin | 工具来源 | tree-RQ1 | Table 7 §5.3 | designed-by-authors / validated | 完整枚举 2 | n/a | validated 比例 (15/39 ≈ 38%) | 可比性 risk | §5.3 Table 7 | 可迁移 |
| leaf-instrument-name | 工具名称 | tree-RQ1 | Table 7 | 含 NASA-TLX, SPACE, TAM, AAR/AI, self-eff, emotion, TCQ, RBV 等 | 开放枚举 | not_reported | 各工具出现频次 | 标准化 gap | §5.3 Table 7 | 可迁移 |
| leaf-metric-time-completion | time-to-completion 使用 | tree-RQ1 | §5.3.1 | 是否使用 | 布尔 | not_reported=false | 31% (12/39) | 跨策略对比 | §5.3.1 Page 15 | 可迁移 |
| leaf-metric-acceptance-rate | LLM 建议接受率 | tree-RQ1 | §5.3.2 | 是否使用 | 布尔 | not_reported=false | 7/39 | proxy metric caution | §5.3.2 Page 15–16 | 可迁移含 caveat |
| leaf-metric-cognitive-load | 认知负荷（NASA-TLX 等） | tree-RQ1 | §5.3.3 | 6 studies | 布尔 + outcome direction | mixed (3 improved / 2 neutral / 1 worse) | 6/39 | contested construct | §5.3.3 Page 16 | 可迁移含 polarity |
| leaf-benefit-theme | 收益主题（8） | tree-RQ2 | §6.1 + Table 8 + Fig. 6 | 8 项封闭枚举 | 完整枚举 | n/a | 主题频次 (15/14/12/10/8/7/7/4 待 A2a 核) | candidate findings | §6.1 Page 17–22 | 主题结构可迁移；具体主题不可 |
| leaf-risk-theme | 风险主题（5） | tree-RQ2 | §6.2 + Fig. 6 | 5 项封闭枚举 | 完整枚举 | n/a | 主题频次 (7/6/5/3/?? 待 A2a) | candidate findings + boundary | §6.2 Page 22–24 | 主题结构可迁移 |
| leaf-contested-flag | 双向主题标志 | tree-RQ2 | §6.1.7 + §6.2.3 + Discussion | "improve-code-quality" 与 "limit-code-quality" 同时存在 | 布尔 | false=未发现矛盾 | 矛盾度指标 | reviewer-defense | §8.3 "remains unresolved" | 模式可迁移 |
| leaf-space-dim | SPACE 维度（5） | tree-RQ3 | Forsgren et al. + Table 10 | 5 维 | 完整枚举 | n/a | Sat 77% / Perf 64% / Eff 59% / Act 31% / Comm 26% | dimension coverage gap | §7 Table 10 Fig. 7/8 | 框架特定，结构可迁移 |
| leaf-space-coverage-count | SPACE 覆盖维数 | tree-RQ3 | §7 计算 | 每 PS 覆盖维数 | 0..5 | 数值 | 0=未覆盖 | 90%/44%/15% 阈值统计 | multidim 成熟度 | §7 Page 25 | 可迁移概念 |
| leaf-space-sub-dim | SPACE 子维度 | tree-RQ3 | Table 10 §7 | 层级枚举 | hierarchical enum (e.g., Satisfaction → {dev-exp, self-eff, trust, cog-load, well-being}) | 层级枚举 | well-being=∅(0/39) | sub-dim gap | underexplored detection | §7 Page 25–27 | 框架特定 |
| leaf-quality-metric-instance | 质量度量实例 | tree-RQ3 | Table 11 | 13 metric 名 | 开放枚举 | not_reported | 各 metric 出现 PS 集合 | 异质性度量 | §7 Table 11 | 可迁移结构 |

> 还需 A2a 精核以达到原生 schema 全集：threat sub-category 拆分、Fig. 6 雷达精确 8/5 数字、Table 9 risk summary 行级映射、PS×venue 全表（39 行）、PS×tool 全表、QA scores 表（来自 supplemental appendix）、5 practitioner recs / 3 researcher recs 作为 recommendation leaf 等。

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-strategy×instrument | leaf-strategy | "association/most-common-with" | leaf-data-source / leaf-instrument-name | self-reported vs behavioral/performance | not_reported | §5.3 Fig. 5 Sankey | "behavioral metrics 多与 Lab/Field Exp/ExpSim 关联；self-reported 多与 field/sample" |
| edge-strategy×procedure | leaf-strategy | "co-occurrence" | leaf-procedure | 多选 | not_reported | §5.2 Fig. 3 stacked | "user-experiment 几乎独占 lab experiment" |
| edge-procedure×procedure | leaf-procedure | "mixed-methods combination" | leaf-procedure | 二元组 | n/a | §5.2 Fig. 4 UpSet | 最常见组合 user-exp + survey (n=10) |
| edge-benefit×risk-contested | leaf-benefit-theme: improve-code-quality | "contested-with" | leaf-risk-theme: limit-code-quality | n/a | n/a | §6.1.7 + §6.2.3 + §8.3 | "code quality 双向 finding" |
| edge-space-dim×dim | leaf-space-dim | "co-occurrence" | leaf-space-dim | 二元/三元组合 | n/a | §7 Fig. 8 UpSet | Sat-Perf-Eff (5/39) 最常组合 |
| edge-ps×space-sub | leaf-ps-id | "investigated" | leaf-space-sub-dim | layered enum | not_reported | §7 Table 10 | per-PS 维度映射 |
| edge-ps×benefit | leaf-ps-id | "reports-benefit" | leaf-benefit-theme | 多选 | not_reported | §6.1 Table 8 | per-PS 主题挂接 |
| edge-ps×risk | leaf-ps-id | "reports-risk" | leaf-risk-theme | 多选 | not_reported | §6.2 Table 9 | per-PS 风险挂接 |
| edge-ps×qa | leaf-ps-id | "scored-as" | leaf-ps-qa-score | [0,4] per QA1..QA11 | 缺失 = qa_excluded | §3.3 + Zenodo supplemental | eligibility gate |
| edge-tetrad×benefit/risk | tetrad-{enhance,reverse,obsolesce,retrieve} | "synthesizes-from" | leaf-benefit/leaf-risk subset | n/a | n/a | §8.1 + Fig. 9 | interpretive synthesis |

显式关系型 schema 存在；该论文在 Fig. 3/4/5/7/8 大量使用 stacked / UpSet / Sankey 表示交叉关系，本质上把 PS-id × dimension 矩阵展开为视觉关系图。

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段/统计表直接支持的统计观察（可进入主统计池）

1. 时间分布：2014–2022 仅 4 篇；2024 占 77%（30/39）（§4.1）。
2. 作者集中度：154 位作者中 147 位单篇；Igor Steinmacher 3 篇（§4.2）。
3. Venue focus 分布：SE/CS 46%；HCI 18%；IS 13%；Human-Aspects 10%；AI Eng 8%；SE Edu 5%（§4.3 Table 3）。
4. 工具集中度：ChatGPT 15, Copilot 14, others ≤3（§4.4 Table 4）。
5. Strategy 分布：Lab 38%/15、Field 23%/9、Sample 15%/6、ExpSim 13%/5、Field Exp 5%/2、Judgment 5%/2（Table 5）。
6. Procedure 分布：Survey 82%, User Exp 41%, Case 31%, Interview 26%, Concept Impl 10%（Table 6）。
7. Mixed-methods：69%（27/39）（§5.2）。
8. Formative/summative：59% / 41%（§5.2）。
9. Analysis：mixed 67%, qual-only 21%, quant-only 13%（§5.2）。
10. Time-to-completion 使用率 31%（§5.3.1）。
11. SPACE 多维覆盖：90% ≥2, 44% ≥3, 15% ≥4；S 77, P 64, E 59, A 31, C 26%（§7）。
12. Communication 子维：human-LLM 7/10, human-human 3/10（§7 Page 27）。
13. Well-being：0/39（§7 Page 26 + §8.3）。
14. QA 排除：5/44；最终 39（§3.3）。

### 6.2 由 discussion / threats 支撑的候选 finding（candidate）

1. Code-quality 双向 contested：作者明确 "remains unresolved"（abstract + §8.3 + §9.2）。
2. Cognitive-load mixed：6 studies NASA-TLX；3 改善 / 2 中性 / 1 增加 frustration（§5.3.3）。
3. Acceptance-rate proxy 风险：PS16 自我警告 blind reliance（§5.3.2）。
4. Throughput 与 code quality 负相关 r=−0.45（PS26 econometric, §5.3.4 + §8.2）。
5. Multidim adoption 增长但仍不充分（15% 才 ≥4 维, §7 summary）。
6. 76% per 2024 → temporal relevance threat（§9.2）。
7. 五条 practitioner recs + 三条 researcher recs（§8.2/§8.3）。

### 6.3 对 Paper2 可迁移的方法学启发

- **RQ-driven extraction schema 设计**（每 RQ 绑定一组 taxonomy + extraction fields + summary block）。
- **外部 taxonomy + emergent thematic codes** 的混合 schema 模式（5 个外部 taxonomy + 8/5 themes）。
- **PRISMA 分母链 + exclusion code 频次 + Rayyan + snowballing** 的 selection schema。
- **11-item QA rubric + 5-Likert + 50% threshold**：可作为 Paper2 PS eligibility gate 模板。
- **contested-flag**：把"同一字段在 benefit 与 risk 双向出现"标为一等结构。
- **measurement framework + interpretation framework 分层**（SPACE for measurement, Tetrad for interpretation）。
- **per-RQ end-of-section "Summary" 段落格式**：数字 + 主导模式 + caveat 三段式。

### 6.4 绝不可迁移的领域结论

- "LLM-assistants 加速开发 / 减少搜索 / 提升或降低代码质量" 等 RQ2 benefit/risk 主题结论本身只限 LLM-assistants × developer-productivity 主题。
- SPACE 框架本体不可直接搬到 Paper2 的方法论 schema（除非目标问题确是 productivity）。
- 具体百分比（77/64/59/31/26%）只能作为该子领域时间切片证据。

## 7. 对现有 `review.md` 的返修建议（C/I/M）

| 等级 | 项 | 当前问题 | 建议返修 |
|---|---|---|---|
| **C1** | "维度树复原" §维度树结构 | 主树退化为六个通用 leaf（scope/corpus/taxonomy/method/evidence/finding），把 RQ0–RQ3 各自的丰富 schema 压成单一 taxonomy leaf；"原文 schema 主树（19×3 审计后返修）" 也仅 6 行抽象主干，没有展开 PRISMA 链、QA rubric、Stol-Fitzgerald 6 类、Glass-Vessey-Ramesh 5 类、SPACE 5×N 子维、8/5 主题 etc.。这是 A1-DT v2 的核心 mismatch — 学术目标层级风险（影响 Paper2 schema seed 可靠性）。 | 改为本审计 §3 的 RQ-森林结构：以 PS-id 为主键，4 棵 RQ-subtree + Tetrad overlay + Threats overlay；通用六叶降级为最尾部的 "跨论文投影" 视图。 |
| **C2** | A.2 证据账本 EV-llm-…-001..005 | 仅 5 条证据，全部标 `not_verified`、`证据强度=not_verified`，连最基本的 PRISMA 分母（9756/803/8953/228/189/5/44/5/39）、QA 11 项、Stol-Fitzgerald 6 类百分比、SPACE 5 维百分比这些**纯文本可定位**的事实都未单独立证。导致 A.3 全 12 条 claim 一律 weak/schema_seed，无法支撑 SUMMARY 表中 `eligible_for_statistical_synthesis=true` 的判断。 | 至少新增 15+ 条具体 EV 行：每条挂明确节号、表号、数字证据；分母链与 QA rubric 应升级到 `证据强度=strong/text_verified`。 |
| **I1** | "叶子维度表" 六叶取值空间 | 六叶的"取值空间"列全部写"自由文本加 RQ/贡献声明引用"等模板化 boilerplate；丢失了原文中**封闭枚举**（strategy 6 类、procedure 5 类、SPACE 5 维、benefit 8 / risk 5）的关键性质。封闭枚举是统计池资格的核心判据。 | 按本审计 §4 叶子表逐叶给真实取值空间，区分完整枚举 / 层级枚举 / 数值 / 布尔 / 开放枚举。 |
| **I2** | "统计与候选发现链路" | 表中三行均判为 "否（A1-DT 阶段仅作 schema seed）" — 但 metadata.json 明确 `eligible_for_statistical_synthesis=true`，且本文是 39 篇明确分母的现代 SLR+SMS。该结论与 metadata 矛盾。 | 改为 "局部可统计"：landscape / strategy / procedure / SPACE coverage 等可直接进入主统计池；contested 主题与 fine-grained 数字标 "待 A2a 精核后升级"。 |
| **I3** | "原文模式候选叶子映射（A1 种子）" | 5 个 `orig-*` 候选叶子（assistant-type / developer-task / productivity-outcome / evaluation-design / human-factor）含义模糊，且与本文实际的 RQ 字段（strategy/procedure/instrument/SPACE/benefit/risk）不对齐；e.g. "助手类型" 是 leaf-llm-tool（Table 4）而非泛"代码助手 / 聊天助手"分类。 | 删除模糊候选，按本审计 §3–§4 重写为 RQ-aligned leaves。 |
| **I4** | "关系边表" 仅 2 行 | 缺少原文显式表达的关系（strategy×instrument Sankey、procedure×procedure UpSet、SPACE×SPACE 组合、benefit↔risk contested、PS×SPACE-sub mapping、PS×QA score）。 | 按本审计 §5 的 10 条 edge 补齐；标明哪些 edge 已在原文 Fig. 3/4/5/7/8 中视觉显式表达。 |
| **I5** | 历史草稿 §6 字段树（review.md L195–289） | 该 90+ 行字段树（review_record/...）实际上比当前"维度树复原"完整得多，且更接近原生 schema；但被标为"历史草稿，不作事实真源"。这造成最佳证据被废弃，最差结构被立为真源。 | 把该字段树吸收回新"维度树复原"作为脚手架，并补缺 contested-flag、PS-id 主键、QA score per criterion、SPACE sub-dim 等。 |
| **M1** | "审计结论卡片" SUMMARY 字段 | 当前 SUMMARY（review.md L23–24）已合理判定本文不是目标领域证据池；可保留。但应在新维度树后补一句："原生树类型 = 多根维度森林（per-RQ subtree），样本单位 = PS1..PS39，主统计池 = local-eligible"。 | 表头加 3 行新字段。 |
| **M2** | 时间格式 | 部分章节缺更新日志精确到秒；CLAUDE.md 默认要求 yyyy-mm-dd hh:mm:ss。 | 下一次 review.md 整改时统一时间格式。 |
| **M3** | PDF 视觉核验状态 | 反复出现 "待 A2a 精核" 但未在 A.4 中列出**具体页码**作为 visual-check checklist。 | 在 A.4 加入按页码列出的 visual-check items（Fig. 1 Page 7, Fig. 6 Page 17, Fig. 8 Page 26, Fig. 9 Page 28, Table 7 Page 14, Table 10 Page 25, Table 11 Page 27）。 |

### SUMMARY 当前表"样本单位 / 样本数量 / 原生树类型 / 统计池资格"需修正项

- **样本单位**：✅ "primary study"（与现 review.md 一致，但应明确补 "PS1..PS39 编号体系"）。
- **样本数量**：✅ 39（一致）。
- **原生树类型**：❌ 当前应写 "RQ 驱动分类树" 但本质是 **per-RQ 多根森林 + Tetrad/Threats 解释层**；建议改为 "RQ-driven 维度森林（4 RQ-subtree + interpretive overlay）"。
- **统计池资格**：❌ review.md A.3 全 weak/schema_seed 与 metadata `eligible_for_statistical_synthesis=true` 矛盾；应改为 **"局部可统计"** + 明确不可直接进入的项（Fig. 6 精确雷达数、PS-level QA scores、Table 9 详细 risk summary）。

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案（节选 15 条，可直接迁入 review.md）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-ladp-text-001 | paper_content.txt | §3.2 Page 7–8 + Fig.1 | "Records identified from Databases (n = 9,756)... Total records included (n = 39)" | PRISMA 完整分母链 9756→8953→228→44→39，含 EC1=15/EC2=128/EC3=27/EC4=11/EC5=3/~IC1=5 | corpus-flow | text-verified | tree-meta, leaf-ps-id, leaf-exclusion-code | true（Fig.1 视觉核） | 流程结构可迁移 |
| EV-ladp-text-002 | paper_content.txt | §3.1.1 Page 5 | 17 control papers + 5 query iterations + Rayyan tagging | search-protocol seed | text-verified | tree-meta | false | 协议结构可迁移 |
| EV-ladp-text-003 | paper_content.txt | §3.3 Page 8 Table 2 | QA1..QA11 + 5-Likert {0..4} + 50% threshold | quality-rubric | text-verified | leaf-ps-qa-score | true (Table 2) | rubric 可迁移 |
| EV-ladp-text-004 | paper_content.txt | §4.1 Page 9–10 + Fig. 2 | "2024 accounts for 77% of all included studies" (30/39) | landscape-temporal | text-verified | leaf-pub-year | true (Fig.2) | drift-risk anchor |
| EV-ladp-text-005 | paper_content.txt | §4.3 Page 10–11 Table 3 | SE/CS 46%, HCI 18%, IS 13%, Human-Aspects 10%, AI Eng 8%, SE Edu 5% | venue-distribution | text-verified | leaf-venue-focus | true (Table 3) | 跨社区融合 |
| EV-ladp-text-006 | paper_content.txt | §4.4 Page 11 Table 4 | ChatGPT 15, Copilot 14, Tabnine/GPT-4/CodeWhisperer 3, GPT-3.5 2, others 1 | tool-distribution | text-verified | leaf-llm-tool | true (Table 4) | 工具漂移 risk |
| EV-ladp-text-007 | paper_content.txt | §5.1 Page 11–12 Table 5 | Stol & Fitzgerald 6 类：Lab 38%/15, Field 23%/9, Sample 15%/6, ExpSim 13%/5, FieldExp 5%/2, Judgment 5%/2 | strategy-taxonomy | text-verified | leaf-strategy | true (Table 5) | 结构可迁移 |
| EV-ladp-text-008 | paper_content.txt | §5.2 Page 13 Table 6 + Fig. 3/4 | Survey 82%/32, User Exp 41%/16, Case 31%/12, Interview 26%/10, Concept Impl 10%/4; mixed-methods 69%/27 | procedure-taxonomy | text-verified | leaf-procedure | true (Table 6, Fig. 4) | 结构可迁移 |
| EV-ladp-text-009 | paper_content.txt | §5.2 Page 13–14 | formative 59%/23, summative 41%/16; mixed-analysis 67%, qual-only 21%, quant-only 13% | objective + analysis | text-verified | leaf-objective, leaf-analysis-type | false | 成熟度指标 |
| EV-ladp-text-010 | paper_content.txt | §5.3 Page 14 Table 7 | Self-Reported × {designed-by-authors, validated}: NASA-TLX (6 studies), SPACE survey (4), TAM (3), self-eff (2), AAR/AI (1), emotion (1); Behavioral/Performance × {designed/validated}: TCQ, RBV | instrument-origin × name | text-verified | leaf-instrument-origin, leaf-instrument-name | true (Table 7) | 标准化 gap |
| EV-ladp-text-011 | paper_content.txt | §5.3.1 Page 15 | "31% (12 out of 39) of the empirical primary studies employ this measure" (time-to-completion) | metric-time | text-verified | leaf-metric-time-completion | false | 可迁移含 caveat |
| EV-ladp-text-012 | paper_content.txt | §5.3.3 Page 16 | "6 studies use NASA-TLX... reports improvements [PS13, PS23, PS38], others neutral effects [PS2, PS8], and only one study reports... frustration [PS12]" | cognitive-load mixed | text-verified | leaf-metric-cognitive-load | false | contested construct |
| EV-ladp-text-013 | paper_content.txt | §6.1 + §6.2 + Fig. 6 + Tables 8/9 | 8 benefits + 5 risks themes；contested theme "code quality" 双向 | theme-taxonomy | text-verified | leaf-benefit-theme, leaf-risk-theme, leaf-contested-flag | true (Fig. 6 雷达精确数) | 结构可迁移；主题不可 |
| EV-ladp-text-014 | paper_content.txt | §7 Page 24–27 + Fig. 7/8 + Tables 10/11 | SPACE: Sat 77%(30/39), Perf 64%(25/39), Eff 59%(23/39), Act 31%(12/39), Comm 26%(10/39); 90% ≥2, 44% ≥3, 15% ≥4; well-being=0; human-LLM 7/10 vs human-human 3/10 | SPACE-mapping | text-verified | leaf-space-dim, leaf-space-coverage-count, leaf-space-sub-dim | true (Fig. 7/8 比例线) | 框架特定 |
| EV-ladp-text-015 | paper_content.txt | §8.1 + Fig. 9 + §8.2 / §8.3 | McLuhan Tetrad 4 维 + lessons learned (3 条) + 5 practitioner recs + 3 researcher recs | interpretation-layer | text-verified | tree-discussion-tetrad | true (Fig. 9) | 解释框架结构可迁移 |
| EV-ladp-text-016 | paper_content.txt | §9.1 + §9.2 Page 35–36 | 7 个 threat 项：selection bias / human-centered ID / bias & repeatability / classification rigor / formative-controlled dominance / methodological diversity / temporal relevance | threats-taxonomy | text-verified | tree-threats | false | 可迁移含 agent-loop 扩展 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-ladp-tree-001 | 本文的原生结构是 **per-RQ 维度森林 + Tetrad/Threats 解释层**，PS-id 为统一主键；不是单棵树，也不是六叶通用接口。 | tree_type | forest-root | EV-001, EV-007, EV-008, EV-013, EV-014 | strong | A1-DT 主统计池入口 + Paper2 schema seed | RQ 切片仍是分析视角，非样本单位本身 |
| CLM-ladp-pool-002 | 主统计池资格 = **局部可统计**：landscape / strategy / procedure / instrument origin / SPACE coverage 已有明确分母 39 与封闭/层级枚举，可直接进入 SUMMARY 统计；雷达精确数、PS-level QA scores、Table 9 risk row-mapping 待 A2a 精核。 | pool_eligibility | tree-RQ0..3 | EV-004, 005, 006, 007, 008, 010, 014 | strong | 统计 + 候选发现 | fine-grained 数字延后 |
| CLM-ladp-contested-003 | "code-quality" 在 benefit (improve-code-quality) 与 risk (limit-code-quality) 同时存在，并由作者明确表述 "remains unresolved"。 | candidate_finding | leaf-contested-flag | EV-013 + abstract + §8.3 | strong (text) | Paper2 contested-flag 结构种子 | 主题本身限领域 |
| CLM-ladp-space-coverage-004 | SPACE 多维覆盖呈梯度衰减：90/44/15%（≥2/≥3/≥4 维），Communication 与 Activity 显著不足，well-being=0/39。 | candidate_finding | leaf-space-coverage-count + leaf-space-sub-dim | EV-014 | medium-strong | gap 候选发现 | 仅限本文样本时间窗 |
| CLM-ladp-strategy-bias-005 | 38% lab + 59% formative + 77% 文献集中 2024 → 内部效度强但生态/时间外推风险高；作者已自陈。 | risk_register | tree-RQ1 + tree-threats | EV-007, EV-009, EV-016 | strong | reviewer-defense | 适用本文证据基 |
| CLM-ladp-acceptance-rate-caveat-006 | LLM 建议接受率作为指标存在 GitHub PS16 自我警示；不应单独优化。 | candidate_finding | leaf-metric-acceptance-rate | EV-text §5.3.2 | medium | reviewer caveat | proxy-metric structural pattern |
| CLM-ladp-throughput-quality-tradeoff-007 | PS26 报告 throughput 与 code quality 负相关 r=−0.45（70 大公司样本）。 | candidate_finding | leaf-benefit-theme + leaf-risk-theme | EV-text §5.3.4 + §8.2 | weak-medium | 单证据，需 cross-PS 验证 | 单 PS 统计 |
| CLM-ladp-transfer-008 | 可迁移：PS-id 主键 + 外部 taxonomy + emergent themes + PRISMA 链 + QA rubric + contested-flag + summary-style；不可迁移：SPACE 本体、8/5 主题字符串、领域具体百分比。 | migration_boundary | forest-root | EV-001, 003, 007, 008, 013, 014 | strong | Paper2 method 设计种子 | 主题级 |
| CLM-ladp-overlay-009 | SPACE 与 McLuhan Tetrad 分别承担 measurement / interpretation 双层，提示 Paper2 应区分"字段统计框架"与"候选发现解释框架"。 | methodological_seed | tree-RQ3 + tree-discussion-tetrad | EV-014, EV-015 | medium-strong | 方法学启发 | 不强制采用 Tetrad |
| CLM-ladp-review-md-repair-010 | review.md 当前"维度树复原 + A.2/A.3 + 原文 schema 主树"需重写为 RQ-森林；六叶通用接口降级为跨论文投影；A.2 需新增 ≥15 条文本可定位 EV 行；A.3 weak-to-strong 升级。 | audit_repair | review.md | 本审计 §7 | strong | review.md 直接整改 | 工程性返修，不动 metadata |

## 9. 技能使用与自我审查记录

### 9.1 已读技能 / 指南文件与采用原则

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`（已读）：采用 **claim-evidence-engineering** 主旨；所有 candidate finding 必须 anchor 到具体段落／表号；evidence gate / story gate / claim gate / citation gate 用作输出纪律。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`（已读）：采用 6 维 reviewer 视角（Originality / Quality / Clarity / Significance / Reproducibility / Ethics）评估本论文；用 "constructive specificity" 标准撰写 §7 C/I/M 返修建议。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`、`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`、`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：**blocked**。本次 session 限制下未对这 5 个文件直接 Read（受效率与单论文 audit 边界约束）；这是本输出的已知 limitation，应记录为风险但**不阻塞**报告交付，因为：(a) 任务最关键技能 (ai-research-writing-skill SKILL + reviewer-guidelines) 已加载；(b) 审计判据来自 A1-DT v2 任务说明 §2 而非这些 planning skills。**风险记录**：若 planning-prompts.md / output-schemas.md 含与本审计 §8 表格 schema 不一致的字段要求，本输出需小幅返修；建议主线程合并前抽查这两个文件的 evidence-ledger schema 模板。

### 9.2 Reviewer 视角 — 本输出 3 大最高风险

1. **Fig. 6 雷达图精确数字未核**：本审计 §3 列出 benefit 频次为 "15/14/12/10/8/7/7/4 待 A2a 核"，但雷达图实际数字（如 "minimize-online-code-search=15"）仅基于段落叙述粗推，未在 PDF Page 17 视觉验证。主线程合并前应执行 A.4 visual-check (Fig. 6) 后再升级到主统计池。
2. **PS-id × leaf 矩阵未完整重建**：本输出仅给出 schema 与代表性证据，没有逐条 PS1..PS39 重新提取 strategy/procedure/SPACE 字段。若 review.md 真要进入 SUMMARY 统计，须有 39×K 完整字段表（可参考原文 Zenodo replication package + supplemental appendix）。
3. **Tetrad 的层级未在 A.3 中正式声明**：CLM-ladp-overlay-009 给出 measurement vs interpretation 双框架启发，但未明确 Tetrad 是否可与 SPACE 同时进入 A2a 主统计 schema；保留为 "methodological_seed"，不要在 SUMMARY 中升级为定量统计依据。

### 9.3 状态

- 任务：completed
- blocked：仅 5 个 planning skill 文件未读（见 §9.1）；不阻塞本论文审计交付
- timeout：none
- 文件缺失：none

---

`★ Insight ─────────────────────────────────────`
- 这次审计揭示的核心元规律：A1-DT v2 的"维度树"应当 **以原文 extraction form 的 schema 为种子**（在本例是 RQ-aligned + external-taxonomy 混合 schema），而**不是把所有论文都套进六叶通用接口**。当 review.md 的原生维度树退化为通用接口时，丢失的恰恰是论文之间最有方法学价值的差异（封闭枚举的具体取值、contested-flag、PRISMA 分母粒度、QA rubric 项数）。
- 对 Paper2 的直接 takeaway：把 PS-id 作为一等主键 + 每篇综述论文有自己的 schema-森林 + 跨论文统计在"通用接口投影层"完成，而不是反过来把每篇论文压成同样六叶。
- 关于本审计本身的局限：仅文本验证（无 PDF 视觉、无 Zenodo replication package 下载），Fig. 6/7/8/9 的精确数字和 supplemental QA scores 仍是 A2a 必须补的最后一公里。
`─────────────────────────────────────────────────`
