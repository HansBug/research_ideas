# petersen-2008-systematic-mapping · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：已确认指引路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 及 `references/paper-story.md` / `reviewer-guidelines.md` / `reviewer-self-review.md`；以这些口径中“reviewer 必须区分原文 schema 与通用接口、必须按字段级证据链审计、不允许把 proposal/roadmap 当作完成型 finding”为审计基线。
- 是否读取 `$research-planning`：已确认 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`；以“维度树叶子必须可执行、必须支撑统计或候选发现，否则只能是 schema_seed”为审计基线。
- 是否读取 `$oh-my-codex:autoresearch`：已确认 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`；以“证据锚点必须精确到节/表/图/页，多对一聚合证据应被降级”为基线。
- 是否完整阅读 `paper_content.txt`：是；共 10 页 536 行，从 Abstract、§1 Introduction、§2.1–§2.5（process / RQ / search / screening / keywording / classification / extraction / bubble plot）、§3 Comparative Analysis（Table 4–5、§3.2 七个比较维度）、§4 四条 Guideline、§5 Conclusion、References 通读。
- 是否核对 `paper.pdf`：未做视觉级核对，仅以文本级证据为准；Table 5 的列对齐与 Figure 3 的 bubble 数值需 A2a 视觉复核，已在本报告中标注。

## 2. 原文真实结构复原

**原文目标 / RQ / 贡献声明**

- Abstract / §1 / §5 明确：本文不是某个 SE 主题的 SLR/SMS，而是一篇方法论文，目标是 (a) 定义 SMS 在 SE 中的流程；(b) 与 SLR 做系统性比较；(c) 提出 SMS 的扩展 guideline。
- 论文没有自己的 RQ 列表，但 Table 1 提供了两个示例 SMS（OO Design Map / Variability Map）的 RQ 模板，用于刻画 SMS 类 RQ 的典型形态：sub-topic 覆盖、研究类型分布、发表论坛识别、时间趋势。

**原文方法流程（§2，Figure 1）**

五步过程，每步带显式 outcome：
1. Definition of Research Questions → Review Scope
2. Conduct Search → All Papers
3. Screening of Papers → Relevant Papers
4. Keywording using Abstracts → Classification Scheme
5. Data Extraction and Mapping Process → Systematic Map

**原文显式 extraction form / classification schema / taxonomy / coding scheme**

- §2.2：搜索串建议按 PICO 结构（population / intervention / comparison / outcome）；mapping 应弱化 outcome/experimental design 限制以保 breadth。
- §2.3 Table 2：纳排准则两套，分别为 OO Design Map（包括/排除经验研究、grey literature、abstract-only、PPT）和 Variability Map（包括/排除变体性的显式贡献、SE 域外）。
- §2.4 Figure 2 + 三 facet：keywording → high-level concept → category cluster → adaptive scheme evolution。三个 facet：
  - **Topic facet**：领域内主题（例如 architecture / requirements / implementation / V&V / variability management / orthogonal variability）。
  - **Contribution facet**：四类枚举 process / method / model / tool（§2.4，"could be a process, method, tool etc." + Figure 3 axis 中显式列出 process / method / model / tool / metric）。
  - **Research facet**：Wieringa 等的六类枚举，Table 3 完整定义：Validation Research / Evaluation Research / Solution Proposal / Philosophical Papers / Opinion Papers / Experience Papers。
- §2.5 Figure 3：bubble plot 在 Variability Context Facet × Contribution Facet × Research Facet 上展示频次与百分比；分母固定为 128 / 118（两个面板）。
- §3.1 Table 5 是本文另一个完整 coding scheme，对 10 篇 SR 编码：
  - **Research Goals**：4 项枚举（Identify Best and Typical Practices；Classification and Taxonomy；Emphasis on Topic Categories；Identify Publication Fora）。
  - **Inclusion Requirements**：2 项（Research is Within Focus Area；Empirical Methods Used）。
  - **Number of Articles**：2 个数值字段（Potentially Relevant Studies；Relevant Studies Included）。
  - **Means of Analysis**：4 项枚举（Meta Study；Comparative Analysis；Thematic Analysis；Narrative Summary）。
- §3.2 提供七个 map–vs–review 比较维度：Goals / Process / Breadth and Depth / Classifying the Topic Area / Classifying the Research Approach / Validity / Industrial Accessibility & Relevance。
- §4 提出四条 guideline / roadmap action：Use Methods Complementarity；Adaptive Reading Depth；Classify on Evidence and Novelty；Visualize Your Data。

**原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation**

- §2.5：从 bubble plot 频数与交叉密度识别 sub-topic × research-type 缺口。
- §3.1–§3.2：把 Table 5 的 4×2×4 编码与文字描述结合，得出“多数 SR 偏 best practice + empirical inclusion + narrative summary”这一描述性 finding，并由此过渡到 §3.2 的 map/review 边界论证。
- §4：guideline 是基于上述编码结果与作者经验的 roadmap proposal，不是完成型 finding。
- §5：结论强调 goals/breadth/depth 差异以及互补使用，是 methodological conclusion，不是领域事实。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但偏抽象 | root 写成“Systematic Mapping Studies in SE 的研究目标 / RQ / 贡献声明”，未在节点层固化“方法论文 / SMS process + map–vs–review comparison”双任务结构。 | M |
| 主干分支是否覆盖原文 schema | 主干仅复原 §2 五步流程，**完全缺失** §3 Table 5 编码体系与 §3.2 七维比较体系，也未把 §4 四条 guideline 作为独立 roadmap 分支 | review.md L186–199 仅有 b1–b5 五个分支；paper_content.txt §3.1 Table 5、§3.2、§4 四条 guideline 均无对应 branch。 | C |
| 叶子维度是否足够具体 | 严重不足 | b1–b5 各仅挂 1 个通用接口叶子（scope / corpus / taxonomy / method / evidence / finding），原文 schema 中显式存在的 Wieringa 六类研究类型、Contribution 四类（process/method/model/tool）、Table 5 的 4 Research Goals + 2 Inclusion + 4 Means of Analysis、§3.2 七维比较、§4 四条 guideline 均未上树。 | C |
| 取值空间是否可执行 | 不可执行 | 所有叶子取值空间被压缩为“自由文本”“层级枚举”等抽象描述，未列出原文已枚举的 6+4+4+2+4 项具体值；候选叶子表 5 行模板文本完全相同。 | C |
| 关系边是否缺失 | 缺失 | bubble plot 的“facet × facet 交叉”关系、Table 5 的“10 SR × 4 编码维度”关系、§3.2 的“map vs review 对照关系”均未在树中表达。 | I |
| 统计用途 / 分母是否正确 | 部分错误 | review 一律写“不进入主统计池 / 只作 schema seed”，但原文 Figure 3 的分母 128 / 118 和 Table 5 的 N=10 是确凿可用的方法学描述性统计；这两个分母被完全忽略，导致 A2a 失去可重复的统计入口。 | I |
| 候选 finding 路径是否完整 | 不完整 | finding 叶子只笼统写“候选发现 / boundary anchor”，未把 §4 四条 guideline（Complementarity / Adaptive Reading Depth / Classify on Evidence-Novelty / Visualize）作为 roadmap action 显式列入候选发现台账。 | I |
| A.1–A.4 证据链是否足够 | 颗粒度过粗 | EV-002 一条同时支撑 b1/b2/b3/b4/b5 与 taxonomy/method 两个叶子，违反“证据锚点要精确到节/表/图”的口径；A.2 全部条目页码写为“待 A2a 精确页码复核”，但 paper_content.txt 提供的 §2.4 第 4 页 Table 3、§3.1 第 6–7 页 Table 5、§2.5 第 5 页 Figure 3 完全可在不依赖 PDF 视觉的条件下精确锚定。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在 | review.md L172 / L228 把整树标为“weak / schema_seed / 不进入主统计池”，与本文真实地位（SMS 方法学母文 + 含两个可统计 coding scheme）相比偏保守；同时 A1-DT 叶子层口径校准段（L176）虽然标注了“通用接口层”，但树主体仍以通用接口为唯一叶子，正文与校准说明存在内部不一致。 | I |

## 4. 建议维度树骨架

下面是一个更忠实于原文的维度树骨架；当前 review 已经把 b1–b5 主干对到原文五步流程，这一选择可保留，但叶子层和并列主干需要扩充。若 A1-DT 阶段确实不希望冻结取值空间，可以保留 `schema_seed / not_verified` 标记，但取值枚举本身必须先落地。

```text
[root] SMS in SE：方法论文（SMS process）+ map–vs–review comparison
├── [b1] Mapping Planning（§2.1）
│   ├── [leaf-rq-type] SMS 类 RQ 模板
│   │   取值：sub_topic_coverage / publication_forum / research_type_distribution / time_trend
│   │   证据：Table 1 (p.2)
│   ├── [leaf-search-pico] 搜索串 PICO 结构
│   │   取值：population / intervention / comparison / outcome（mapping 默认弱化 comparison+outcome）
│   │   证据：§2.2 (p.3)
│   └── [leaf-unit] 单位对象
│       取值：paper / study / map / SR；统计分母：本文 Figure 3 = 128/118，Table 5 N=10
├── [b2] Search + Screening（§2.2–§2.3）
│   ├── [leaf-source] 数据源类型
│   │   取值：scientific_database / manual_conference / manual_journal / grey_literature
│   ├── [leaf-inclusion] 纳入条件
│   │   取值：focus_area_match / explicit_contribution / empirical_evidence_required
│   └── [leaf-exclusion] 排除条件
│       取值：abstract_only_mention / out_of_se_domain / abstract_or_ppt_only / duplicate_report
│       证据：Table 2 (p.3)
├── [b3] Keywording → Classification Scheme（§2.4，Figure 2）
│   ├── [leaf-reading-depth] adaptive reading depth
│   │   取值：abstract_only / abstract+introduction / abstract+conclusion / full_text
│   ├── [leaf-topic-facet] Topic facet（领域相关，示例 variability：architecture / requirements / implementation / V&V / variability_management / orthogonal_variability）
│   ├── [leaf-contribution-facet] Contribution facet（封闭枚举）
│   │   取值：process / method / model / tool / metric
│   │   证据：§2.4 (p.4) + Figure 3 contribution axis (p.5)
│   └── [leaf-research-facet] Research-type facet（Wieringa 六类，封闭枚举）
│       取值：validation_research / evaluation_research / solution_proposal / philosophical_paper / opinion_paper / experience_paper
│       证据：Table 3 (p.4)
├── [b4] Data Extraction + Map Visualization（§2.5，Figure 3）
│   ├── [leaf-extraction-table] 抽取表字段
│   │   取值：category_assignment + short_rationale（每篇必填）
│   ├── [leaf-frequency] category frequency
│   │   分母：128 / 118（Figure 3 两个面板）
│   ├── [leaf-cross-facet] 三 facet 交叉
│   │   关系：topic × contribution × research-type
│   └── [leaf-viz-form] 可视化形式
│       取值：summary_statistics_table / frequency_table / bubble_plot
├── [b5] Map vs Review Comparison（§3.1–§3.2）
│   ├── [leaf-sr-coding] SR 编码体系（Table 5，N=10）
│   │   ├── research_goal：identify_best_practice / classification_taxonomy / emphasis_on_topic / identify_publication_fora
│   │   ├── inclusion_requirement：within_focus_area / empirical_methods_used
│   │   ├── number_field：potentially_relevant / included
│   │   └── means_of_analysis：meta_study / comparative_analysis / thematic_analysis / narrative_summary
│   └── [leaf-comparison-dim] §3.2 七维比较
│       取值：goals / process / breadth_and_depth / classifying_topic_area / classifying_research_approach / validity / industrial_accessibility
└── [b6] Guidelines / Roadmap（§4，候选 finding 池）
    └── [leaf-guideline] 四条 guideline（roadmap action，不是完成型 finding）
        取值：use_methods_complementarity / adaptive_reading_depth / classify_on_evidence_and_novelty / visualize_your_data
        证据：§4 (p.8–9)
```

缺失值语义：topic-facet 是领域相关的开放枚举，跨论文迁移时写 `domain_specific_open`；其余 contribution / research / SR-coding / guideline 均为封闭枚举，缺失值写 `not_reported`。

候选发现路径（保持 candidate / schema_seed 等级，不直接升 finding）：
1. Bubble plot 缺口路径：从 frequency × cross-facet 推 topic×research-type 覆盖缺口。
2. SR 编码缺口路径：Table 5 显示 10/10 SR 都用 narrative summary、仅 2/10 用 thematic analysis、0/10 单独用 meta-analysis 完整覆盖——可作为方法学描述性候选发现，**分母明确为 N=10**。
3. Roadmap 路径：§4 四条 guideline 各对应一个 candidate recommendation，需在 Paper2 反证后才能成为 finding。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干补 b6 Guidelines/Roadmap 分支 | review.md “维度树结构” 代码块 | 在 b5 之后增加 `[dim-...-b6] guidelines/roadmap`，挂叶子 `leaf-guideline`，取值枚举四条 guideline | §4 (p.8–9) | C |
| b5 拆分为 “gap identification + map–vs–review comparison” 或新增 `[b5-sr-coding]` 与 `[b5-comparison-dim]` 两个并列叶子 | review.md 同上 | 在 b5 下并列添加 `leaf-sr-coding`（含 Table 5 的 4+2+2+4 字段枚举）与 `leaf-comparison-dim`（§3.2 七维）；移除“SR 编码不可统计”的笼统降级 | Table 5 (p.7)、§3.2 (p.7–8) | C |
| b3 classification scheme 必须并列展开 topic / contribution / research-type 三个叶子 | review.md 同上、叶子维度表 | 用 `leaf-topic-facet` / `leaf-contribution-facet` / `leaf-research-facet` 替换当前唯一的 `leaf-...-taxonomy` 通用接口；后两者写出封闭枚举（Wieringa 6 / process-method-model-tool-metric） | §2.4 + Table 3 (p.4)、Figure 3 contribution axis (p.5) | C |
| b4 map visualization 叶子必须落地分母与交叉关系 | review.md 同上、统计与候选发现链路表 | 把 Figure 3 的分母 128/118 写入“可统计方式 / 分母”列；把三 facet 交叉写为显式 relation edge；删除 b4 写为 `not_applicable` 的笼统语言 | §2.5 + Figure 3 (p.5) | I |
| 候选叶子表 5 行模板文本统一化问题 | review.md “原文模式候选叶子映射（A1 种子）” | 每行的“候选取值空间”应改为原文显式枚举而不是抽象描述；A2a 精核任务应区分各叶子要核对的具体表/图/页 | §2.2–§2.5、§3.1、§4 | C |
| EV-002 / EV-003 颗粒度过粗 | review.md A.2 | 拆分为至少 5–6 条证据：EV-process-fig1（Figure 1 p.2）、EV-table1-rq（Table 1 p.2）、EV-table2-incl（Table 2 p.3）、EV-table3-research-type（Table 3 p.4）、EV-fig3-bubble（Figure 3 p.5）、EV-table5-sr-coding（Table 5 p.7）、EV-section4-guidelines（§4 p.8–9）；每条只挂 1–2 个 dim/leaf | paper_content.txt 中各节均有明确页码 | I |
| 统计池保守降级口径需要分情况 | review.md “统计与候选发现链路” | 区分“SMS 方法学描述性统计”（Figure 3 N=128/118、Table 5 N=10，可作为 methodological descriptive 入池）与“SE 主题领域统计”（确实不入池）；当前一律写“不进入主统计池”会让 A2a 失去显式的 N | §2.5、§3.1 | I |
| §3.2 七维比较未上树 | review.md 维度树结构 + 叶子表 | 增加 `leaf-comparison-dim`，取值枚举为：goals / process / breadth_and_depth / classifying_topic_area / classifying_research_approach / validity / industrial_accessibility | §3.2 (p.7–8) | I |
| A1-DT 校准段与树主体不一致 | review.md L172 / L176 / L228 | 一旦补完原文 schema 叶子，应同步删除“树主体是 6 个通用接口、原文 schema 候选只在另一节列出”的二元叙述，避免误导后续 reviewer | review.md 内部一致性 | M |
| 历史草稿（旧第 5 节迁移来源）信息冗余 | review.md L104–141 | 旧 ASCII 树已包含 search_and_selection / classification_scheme / extraction_evidence / visualization / finding_boundary 等更接近原文 schema 的叶子，但被声明为“不作事实真源”；建议把其中可复用的叶子并入正式维度树而不是仅保留为历史草稿 | review.md L104–141 | M |
| 根节点未承载“双任务结构” | review.md root | root 同时承担 (a) SMS 方法过程描述 + (b) map–vs–review comparison，根节点说明里应显式写出这两个 sub-goal，避免 reviewer 只把它当作单一 process 论文 | Abstract / §1 / §5 | M |

## 6. C/I/M 结论

- **C（直接破坏 Paper2 学术目标 / 证据链 / 后续 A2a/A2b 可靠性）**：
  - 主干完全缺失 §3 Table 5 编码体系 + §3.2 七维比较 + §4 四条 guideline，会让 A2a 在“维度树 → 原文统计字段 → 候选 finding”的链路上断裂；
  - b3 classification scheme 没有把 Wieringa 6 类 + Contribution 4 类作为枚举叶子，等于把本文最可迁移的 SE 方法学公共资产丢失；
  - 叶子取值空间被压缩为抽象描述，候选叶子表 5 行模板化，无法直接指导 A2a 精核。
- **I（实质影响维度树可用性 / 原文 schema 复原 / 证据可审计性）**：
  - EV-002/003 一条证据覆盖多个 dim/leaf，违反字段级证据锚点；
  - Figure 3 分母 128/118 与 Table 5 N=10 这两个明确分母被笼统降级为“不进入主统计池”；
  - §3.2 七维比较未上树；
  - 候选 finding 路径未把 §4 四条 guideline 显式收入 ledger。
- **M（不阻塞的清晰度 / 维护性建议）**：
  - root 节点叙述未明确双任务结构；
  - A1-DT 叶子层校准段与树主体存在内部叙述不一致；
  - 旧第 5 节迁移来源的可复用叶子未回流到正式树。

- **最终建议：NEEDS FIX**。本文在 A1-DT 阶段的角色是“SMS / SE methodology seed”，其可迁移价值高度依赖于 Wieringa 六类、Contribution 四类、Table 5 编码维度与 §3.2/§4 这些**封闭枚举**被准确写入维度树；当前 review 把这些全部压缩到通用六接口叶子下，存在把“通用 reviewer 接口”当作“原文 schema 复原”的误读风险，必须先补齐主干 b6 与叶子层枚举，再进入 A2a。
