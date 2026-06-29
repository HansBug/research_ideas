# mde-ml-components-slr · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是
  - 路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - 关联参考：`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是
  - 路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - 关联参考：`references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是
  - 路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是 — 已全文阅读 2123 行，覆盖摘要、Introduction（§1）、Background（§2）、SLR Protocol（§3.1）、Search & Selection（§3.2）、Data Extraction & Synthesis（§3.3）、Quality Assessment（§3.4）、Results RQ1（§4）含 Tables 3–11 与 Fig. 5、Results RQ2（§5）含 Tables 12–21 与 Fig. 6、Results RQ3（§6）含 Tables 22–27 与 Fig. 7、Results RQ4（§7）含 Tables 28–29 与 Figs. 8–9、Gap Analysis（§7 后半）、Recommendations（§8）、Threats to Validity（§9）、Conclusion（§10）。
- **是否核对 `paper.pdf`**：否 — 受限于当前环境无法打开 PDF 进行版面级视觉核对；本次审计基于 `paper_content.txt` 全文文本与 `review.md` 中记载的 Fig. 5/Fig. 6 已核对记录。复杂表格（29 张表）的精确数值、页码和图表布局未做 PDF 逐页复验。此项限制应在 §5 修复清单中记录。

### 额外读取的文库级规则与故事

| 文件 | 路径 | 作用 |
|---|---|---|
| survey_of_surveys/README.md | `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md` | 定位与边界 |
| survey_of_surveys/GUIDE.md | `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md` | 证据等级、三池规则、维度树复原规则 |
| survey_of_surveys/SUMMARY.md | `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/SUMMARY.md` | 总账与 A1-M0–M6 元维度 |
| pattern-field-schema.md | `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/patterns/pattern-field-schema.md` | 字段合同与证据链合同 |
| paper_story.md | `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md` | S0-v2 方法论主线与禁止主张 |

---

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文 Naveed et al. (2024) 是一篇执行完成的 Kitchenham-style SLR，发表在 *Information and Software Technology*（IST, CCF-B）。其核心目标声明在 Abstract 和 §1 末尾明确：通过 SLR 系统性分析 MDE4ML 领域的研究动机、MDE 方案、评价技术和关键局限/gap。

原文设置 4 个 RQ：

| RQ | 原文问题 | 操作化对象 |
|---|---|---|
| RQ1 | What are the motivations behind using MDE for systems with ML components? | motivation/goal, ML technique, application domain, end users, contribution type, ML aspects |
| RQ2 | What MDE approaches and tools exist for MDE4ML? | model representation, modeling language type, model level/type, ML aspects, ML framework/library, transformation, generated artifact, automation level, tool availability, meta-tool/framework/transformation language |
| RQ3 | How are existing MDE4ML studies evaluated? | evaluation context, evaluation methods, ML metrics, MDE metrics, datasets |
| RQ4 | What are limitations and future work in MDE4ML? | limitation categories (approach/evaluation/solution quality), future work categories (approach enhancement/further evaluation/quality enhancement) |

### 2.2 原文方法流程

原文方法流程完整且可审计：

1. **Search**：7 个数据库自动检索，search string 由所有作者协作制定；初始 3934 条，去重后 3570 条。
2. **Selection**：三轮筛选（title → abstract → full-text），使用预定义 inclusion/exclusion criteria；初始 32 条纳入。
3. **Snowballing**：前向 + 后向 snowballing（遵循 Wohlin 2014 指南），增补 14 条，最终 46 篇 primary studies。
4. **Data extraction**：预定义 extraction form（§3.3 详述），先 pilot 5 篇论文验证 extraction form 的完整性与一致性；多数数据由第一作者抽取，其他作者讨论确认。
5. **Quality assessment**：对全部 46 篇 primary studies 执行质量评估，使用 12 条标准（源于 Kitchenham 指南），每条评分 Yes/Partly/No。
6. **Synthesis**：按 RQ 分组进行描述性统计与分类统计，产出 29 张数据表与 9 张图，每个 RQ 末尾给出 "RQ Answer Summary"。
7. **Gap analysis & Recommendations**：§7 系统归纳当前 gap（6 个 gap 类别），§8 给出面向研究人员和实践者的 recommendations（8 条建议）。
8. **Threats to validity**：§9 按 construct/internal/external/conclusion validity 四类报告效度威胁。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme

原文 §3.3 详细描述了 extraction form 的组织方式：

- **Pilot phase**：用 5 篇论文测试 extraction form 的完整性与一致性。
- **Extraction fields per RQ**（原文明确列出）：
  - RQ1：motivation category, ML technique addressed, application domain, end users, contribution type, ML aspects addressed
  - RQ2：model representation / DSLs used, modeling language type, model level/type, ML aspects, ML framework/library, model transformation, generated artifacts, automation level, tool/language, tool availability
  - RQ3：evaluation context (academic/industrial), evaluation methods, evaluation metrics (ML metrics, MDE metrics), datasets
  - RQ4：limitations, future work
- **Classification schemas** 显式出现在结果表中：
  - Table 3：motivation categories（Automation, Quality Improvement, Complexity Reduction 等）— 每个类别有计数
  - Table 12：MDE solution types（DSLs, transformations, tools, methods, processes）
  - Table 26：evaluation methods（Case Study, Experiment, Industrial Case, Tool Demo）
  - Table 28：limitation categories（approach, evaluation, solution quality）
  - Table 29：future work categories（approach enhancement, further evaluation, quality enhancement）
- **Quality assessment**：12 条标准，评分 Yes/Partly/No，结果见 Table 2
- **Feature tree**：Fig. 5 以图形化方式展示 Google Form 的 40 个问题按 5 个 section 对应的 extraction tree
- **Roadmap**：§7（Gap Analysis）与 §8（Recommendations）构成完整的 gap→recommendation 路线图

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的结论形成路径非常清晰：

1. **每张结果表都是 "field → count/percentage" 映射**（例如 Table 3：motivation categories × count，Table 22：evaluation context × count）。
2. **每个 RQ 末尾有 "RQ Answer Summary"**，将统计观察归纳为结构化的 answer paragraph。
3. **§7 Gap Analysis**：从跨 RQ 的统计观察中抽象出 6 个 gap 类别（例如 "Lack of MDE4ML tools for non-experts"）。
4. **§8 Recommendations**：从 gap 推导出 8 条 recommendations。
5. **§9 Threats to Validity**：自我报告效度威胁（construct: search string completeness；internal: single-extractor bias；external: limited to MDE4ML；conclusion: moderate quality scores）。

---

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树结构摘要

`review.md` 中的维度树结构为：

```
[dim-mde-ml-components-slr-root]
├── [dim-mde-ml-components-slr-b1] 综述范围与研究问题
│   └── [leaf-mde-ml-components-slr-scope]
├── [dim-mde-ml-components-slr-b2] 语料收集与纳排
│   └── [leaf-mde-ml-components-slr-corpus]
├── [dim-mde-ml-components-slr-b3] 主题 / 对象分类
│   └── [leaf-mde-ml-components-slr-taxonomy]
├── [dim-mde-ml-components-slr-b4] 方法 / 技术 / 干预
│   └── [leaf-mde-ml-components-slr-method]
└── [dim-mde-ml-components-slr-b5] 评价、统计与候选发现
    ├── [leaf-mde-ml-components-slr-evidence]
    └── [leaf-mde-ml-components-slr-finding]
```

另有 5 个「原文模式候选叶子」（`[leaf-*-orig-*]`）被放在独立表中，标记为 `not_verified`，用途为 `schema_seed`。

### 3.2 维度树审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-mde-ml-components-slr-root]` 的命名和定义正确指向 Naveed et al. (2024) 的 SLR 研究目标与贡献声明。 | 通过 |
| 主干分支是否覆盖原文 schema | **I** | 当前 5 个主干分支（b1–b5）映射了 A1-M0–M6 元维度的前五层，但**缺少原文最核心的 RQ→extraction-field 映射结构**。原文有 4 个 RQ，每个 RQ 对应 5–10 个具体抽取字段（合计约 25 个字段），当前树完全没有按 RQ 组织分支，也没有把这些字段作为叶子维度收入主树。Section 2.2 的 RQ 映射表是准确的，但没有在维度树中兑现。详见 §3.3。 | **I** |
| 叶子维度是否足够具体 | **C** | 当前 6 个叶子维度是**通用 meta-interface**（scope / corpus / taxonomy / method / evidence / finding），而非原文的 specific extraction fields。例如原文有 "motivation category"（Automation/Quality/Complexity 等具体取值）、"evaluation context"（academic/industrial）、"model representation"（DSL type）等可执行字段，但在维度树中被压缩为一个抽象的 `[leaf-mde-ml-components-slr-taxonomy]`。5 个候选叶子被隔离在独立表并标记 `not_verified`，形成事实上的「树是空壳，实词在候选表」结构。详见 §3.3。 | **C** |
| 取值空间是否可执行 | **I** | 6 个主叶子的取值空间描述为「自由文本加理由」「完整枚举/层级枚举」「布尔/数值/链接状态」等**方法论指导语而非原文具体取值**。例如 `[leaf-mde-ml-components-slr-method]` 的取值空间写的是「层级枚举、关系值或开放 action point」，而原文 Table 12 明确有 "DSLs / transformations / tools / methods / processes" 的具体分类，这个信息在候选叶子表中也只是粗写「方法、框架、工具、语言、流程或平台」。A2a 无法从当前树直接知道原文到底分了哪些类。 | **I** |
| 关系边是否缺失 | **I** | 原文有明确的跨 RQ 关系边：例如 RQ3 的 "evaluation methods" 度量 RQ2 的 "MDE solutions"；RQ4 的 "limitations" 反向指向 RQ1–RQ3 的缺口。当前树只有父子包含关系，没有任何横向关系边（如 "evaluation_method → measures → MDE_solution"）。这与 `pattern-field-schema.md` §8.3 要求的关系边合同不符。 | **I** |
| 统计用途 / 分母是否正确 | **I** | 「统计与候选发现链路」表正确标注了当前所有节点为 `schema_seed`（不进入主统计池），但原文本身有 46 篇 primary studies 的分母和 29 张表的统计结果，这些分母信息未出现在维度树的叶子规格中。当前表述「分母：当前 19 篇 survey-of-surveys 样本」混淆了**被审论文的统计分母**和**脚手架文库的分母**。原文 46 的分母应当作为叶子维度的统计前置条件写入。 | **I** |
| 候选 finding 路径是否完整 | **I** | 原文的 gap→recommendation 链条（§7 Gap Analysis 的 6 个 gap 类别 → §8 Recommendations 的 8 条建议）是典型的 "统计观察 → gap → recommendation" finding 路径示例，但当前树没有为这条路径设置对应的叶子或关系边。`[leaf-mde-ml-components-slr-finding]` 的候选发现用途只写了通用描述，未引用原文具体的 gap categories 或 recommendation items 作为样例。 | **I** |
| A.1–A.4 证据链是否足够 | **M** | A.1（来源）正确列出 3 个来源文件。A.2（证据账本）有 5 条证据记录，但大多数证据强度标记为 `not_verified` 或 `medium`，而原文 paper_content.txt 中对应内容实际上可读。例如 EV-mde-ml-components-slr-001（根节点证据）标记为 `not_verified`，但原文摘要和 §1 的目标声明在 paper_content.txt 中是完整存在的。A.3（结论映射）结构完整，回链正确。A.4（复验清单）只有结构检查（passed）和视觉核对（needs_manual_check），缺少对原文 extraction form、quality assessment、gap analysis 等关键结构的专项复验项。 | **M** |
| 是否存在可能误导 A2a 的强主张 | **I** | Section 2.2 的 RQ→维度树映射表说「RQ2 对应 solutions-tools 维度树」「RQ3 对应 evaluation 维度树」，但实际 A.2 维度树中没有 RQ2 分支也没有 RQ3 分支。A2a 如果只看维度树本体（不看 Section 2.2 的历史描述），会得到一棵只有 6 个通用 leaf 的树，这与 Section 2.2 声称的「非常清楚的维度树」形成期待落差。这不是强主张过度承诺，而是**树本体与描述之间的结构不一致**，可能导致 A2a 绕路重做。 | **I** |

### 3.3 核心问题详析：「树是通用接口，不是原文 schema」

当前维度树的 6 个叶子维度（scope / corpus / taxonomy / method / evidence / finding）实际上**与 A1-M0–M6 的 7 层元维度高度重合**：

| 当前叶子 | 对应 A1-M 层 | 匹配度 |
|---|---|---|
| scope | A1-M0 研究意图与综述元模型 | 高度重合 |
| corpus | A1-M1 语料收集与纳排 | 高度重合 |
| taxonomy | A1-M2 研究对象与主题语义 | 高度重合 |
| method | A1-M3 方法 / 技术 / 干预 | 高度重合 |
| evidence | A1-M4 评价、证据与复现资产 | 高度重合 |
| finding | A1-M6 research finding 形成与裁决 | 高度重合 |

这不是巧合——当前树的 5 个主干分支 + 6 个叶子几乎逐层对应 A1-M0–M6 元维度（缺 A1-M5 统计分析就绪层）。换句话说，当前树是一棵**通用元维度投影树**，而非 Naveed et al. (2024) 这篇论文的**原文 schema 复原树**。

GUIDE.md §6 和 pattern-field-schema.md §8.2 明确要求维度树复原为「原文中出现的抽取字段、分类项、模型节点或报告叶子」。当前树没有做到这一点——它用元维度框架包裹了原文，但原文的具体字段没有被组织进树体内。

5 个「候选叶子」表的存在恰好证明了这一点：作者自己也意识到 6 个通用叶子不够，因此额外列出了 orig-ml-lifecycle、orig-mde-artifact、orig-solution-type、orig-motivation-benefit、orig-evaluation-context。但候选叶子被标记为 `not_verified` 且列在独立表中，A2a 无法从树的本体直接看到原文究竟有哪些字段。

### 3.4 对比：原文实际字段 vs 当前树中的反映

| 原文实际抽取字段 (from §3.3 / Tables 3–29) | 当前树中的位置 | 缺失程度 |
|---|---|---|
| Motivation category: Automation / Quality / Complexity / … (Table 3) | 候选表 `orig-motivation-benefit`，`not_verified` | 完全未进入主树 |
| ML technique: supervised / unsupervised / deep / … (Table 4) | 无任何对应节点 | 完全缺失 |
| Application domain: healthcare / finance / transport / … (Table 5) | 无任何对应节点 | 完全缺失 |
| End users: data scientist / developer / domain expert / … (Table 6) | 无任何对应节点 | 完全缺失 |
| Contribution type: modeling language / transformation / tool / … (Table 7) | 候选表 `orig-solution-type`，`not_verified` | 完全未进入主树 |
| ML aspects: data preparation / model training / deployment / … (Table 8) | 候选表 `orig-ml-lifecycle`，`not_verified` | 完全未进入主树 |
| Model representation / DSL (Table 12) | 候选表 `orig-mde-artifact`，`not_verified` | 完全未进入主树 |
| Modeling language type: UML-based / DSL / ontology / … (Table 13) | 无任何对应节点 | 完全缺失 |
| Model level/type: M1/M2 (Table 14) | 无任何对应节点 | 完全缺失 |
| Model transformation (Table 17) | 无任何对应节点 | 完全缺失 |
| Generated artifacts (Table 18) | 无任何对应节点 | 完全缺失 |
| Automation level: manual / semi-auto / auto (Table 19) | 无任何对应节点 | 完全缺失 |
| Tool availability: public / private / not available (Table 20) | 无任何对应节点 | 完全缺失 |
| Evaluation context: academic / industrial (Table 22) | 候选表 `orig-evaluation-context`，`not_verified` | 完全未进入主树 |
| Evaluation methods: case study / experiment / … (Table 26) | 无任何对应节点 | 完全缺失 |
| ML evaluation metrics: accuracy / precision / … (Table 24) | 无任何对应节点 | 完全缺失 |
| MDE evaluation metrics (Table 25) | 无任何对应节点 | 完全缺失 |
| Limitations categories (Table 28) | 无任何对应节点 | 完全缺失 |
| Future work categories (Table 29) | 无任何对应节点 | 完全缺失 |
| Quality assessment criteria × 12 (Table 2) | 无任何对应节点 | 完全缺失 |
| Gap categories × 6 (§7) | 无任何对应节点 | 完全缺失 |
| Recommendations × 8 (§8) | 无任何对应节点 | 完全缺失 |
| Threats to validity × 4 categories (§9) | 无任何对应节点 | 完全缺失 |
| Data availability: figshare link | 无任何对应节点 | 完全缺失 |

**结论**：原文有约 25 个明确的提取字段 + 12 个质量评估标准 + 6 个 gap 类别 + 8 条 recommendation + 4 类效度威胁 + 数据制品链接，而当前维度树只有 6 个通用叶子 + 5 个候选叶子（且候选叶子仅覆盖了其中约 5 个字段）。覆盖率约为 (5+6)/(25+12+6+8+4+1) ≈ 11/56 ≈ 20%，**严重不足**。

---

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树。由于本审计为 full-text 级（未经 PDF 页码复验），叶子取值空间中的精确数值以 `[T3]` 等形式标注表号。

```
[dim-root] Naveed et al. (2024): MDE4ML SLR — IST, CCF-B, 46 primary studies
│
├── [dim-rq1] RQ1: Motivations for MDE4ML
│   ├── [leaf-rq1-motivation] Motivation category
│   │   └── 取值: Automation, Quality Improvement, Complexity Reduction, Productivity, Reusability, Maintainability, Traceability, Interoperability [T3]
│   ├── [leaf-rq1-ml-technique] ML technique addressed
│   │   └── 取值: Supervised/Unsupervised/Reinforcement/Deep Learning/Semi-supervised [T4]
│   ├── [leaf-rq1-domain] Application domain
│   │   └── 取值: Healthcare, Finance, Transport, IoT, CPS, Robotics, … [T5]
│   ├── [leaf-rq1-end-users] Target end users
│   │   └── 取值: Data Scientist, ML Engineer, Software Developer, Domain Expert, … [T6]
│   ├── [leaf-rq1-contribution] Contribution type
│   │   └── 取值: Modeling Language, Model Transformation, Tool, Method/Framework, Process [T7]
│   └── [leaf-rq1-ml-aspect] ML aspects addressed
│       └── 取值: Data Preparation, Feature Engineering, Model Training, Model Selection, Hyperparameter Tuning, Deployment, Monitoring, … [T8]
│
├── [dim-rq2] RQ2: MDE Approaches & Tools for MDE4ML
│   ├── [leaf-rq2-dsl] Model representation / DSL used
│   │   └── 取值: UML profile, custom DSL, ontology, Ecore-based, … [T12]
│   ├── [leaf-rq2-lang-type] Modeling language type
│   │   └── 取值: General-purpose (UML), Domain-specific, Ontology-based [T13]
│   ├── [leaf-rq2-model-level] Model level / type
│   │   └── 取值: M1 (model), M2 (metamodel) [T14]
│   ├── [leaf-rq2-ml-aspect] ML aspects targeted
│   │   └── 取值: (同 leaf-rq1-ml-aspect 取值空间) [T15]
│   ├── [leaf-rq2-ml-framework] ML framework / library
│   │   └── 取值: TensorFlow, PyTorch, scikit-learn, Keras, Weka, … [T16]
│   ├── [leaf-rq2-transformation] Model transformation
│   │   └── 取值: Model-to-text (M2T), Model-to-model (M2M) [T17]
│   ├── [leaf-rq2-generated-artifact] Generated artifact type
│   │   └── 取值: Source code, Configuration file, Pipeline script, Documentation, … [T18]
│   ├── [leaf-rq2-automation] Automation level
│   │   └── 取值: Manual, Semi-automated, Fully automated [T19]
│   └── [leaf-rq2-tool-availability] Tool / language availability
│       └── 取值: Public, Private (proprietary), Not available [T20]
│
├── [dim-rq3] RQ3: Evaluation of MDE4ML Studies
│   ├── [leaf-rq3-eval-context] Evaluation context
│   │   └── 取值: Academic, Industrial [T22]
│   ├── [leaf-rq3-eval-method] Evaluation method
│   │   └── 取值: Case Study, Experiment, Industrial Case, Tool Demo, Running Example [T26]
│   ├── [leaf-rq3-ml-metrics] ML evaluation metrics
│   │   └── 取值: Accuracy, Precision, Recall, F1, RMSE, … [T24]
│   ├── [leaf-rq3-mde-metrics] MDE evaluation metrics
│   │   └── 取值: Code generation correctness, Model quality, Time/Effort reduction, … [T25]
│   └── [leaf-rq3-datasets] Datasets used
│       └── 取值: UCI, MNIST, CIFAR, custom industrial data, … [T27]
│
├── [dim-rq4] RQ4: Limitations & Future Work
│   ├── [leaf-rq4-limitation-type] Limitation category
│   │   └── 取值: Approach limitations, Evaluation limitations, Solution quality limitations [T28]
│   └── [leaf-rq4-future-work-type] Future work category
│       └── 取值: Approach enhancement, Further evaluation, Quality enhancement [T29]
│
├── [dim-quality] Quality Assessment (Kitchenham 12 criteria)
│   ├── [leaf-qa-criteria] Individual QA criteria
│   │   └── 取值: 12 criteria, score = Yes / Partly / No per primary study [T2]
│   └── [leaf-qa-aggregate] Aggregate quality distribution
│       └── 取值: count of Yes/Partly/No per criterion across 46 studies [T2]
│
├── [dim-gap-roadmap] Gap Analysis & Recommendations
│   ├── [leaf-gap-category] Gap category (§7)
│   │   └── 取值: Lack of MDE4ML tools for non-experts, Limited evaluation in industrial settings, …, 共 6 类
│   └── [leaf-recommendation] Recommendation (§8)
│       └── 取值: 8 条面向 researchers/practitioners 的建议
│
├── [dim-validity] Threats to Validity (§9)
│   └── [leaf-validity-type] Validity threat category
│       └── 取值: Construct validity, Internal validity, External validity, Conclusion validity
│
├── [dim-artifact] Data & Artifact Availability
│   └── [leaf-data-link] Replication data link
│       └── 取值: figshare URL [present] / not available
│
└── [dim-search] Search & Selection Protocol
    ├── [leaf-search-databases] Databases searched
    │   └── 取值: ACM DL, IEEE Xplore, Scopus, Web of Science, SpringerLink, ScienceDirect, Google Scholar
    ├── [leaf-search-results] Search yield
    │   └── 取值: 3934 initial → 3570 after dedup → 32 after screening → 46 after snowballing
    └── [leaf-snowballing] Snowballing method
        └── 取值: Forward snowballing + Backward snowballing (Wohlin 2014), +14 papers

[横向关系边]
[edge-eval-measures-solution]: RQ3.evaluation_method → measures → RQ2.MDE_solution
[edge-limitation-points-to-gap]: RQ4.limitation → points_to → dim-gap-roadmap.gap_category
[edge-gap-derives-recommendation]: dim-gap-roadmap.gap_category → derives → dim-gap-roadmap.recommendation
[edge-qa-qualifies-finding]: dim-quality.qa_criteria → qualifies → RQ1..RQ4 statistics
```

### 建议树的统计可执行性

- 所有叶子取值空间均基于原文 Tables 2–29 的显式分类，可直接执行 extraction。
- 原文分母为 46 篇 primary studies，可作为所有叶子维度的统计分母。
- 跨 RQ 交叉统计（如 "哪些 evaluation method 用于评估哪些 MDE solution type"）原文未做，不代表不可做——这是 A2a 可从本树获得的启发。
- 缺失值语义：原文 Tables 中未出现的类别即 `not_reported`；原文未报告的字段（如部分 primary study 不声明 tool availability）即 `not_reported`。

### 与当前 `review.md` 树的关系

当前树不是「错误」的——它正确地抽象了一个通用维度框架。但它是**通用接口，不是原文 schema**。建议树保留了当前树的根节点和 5 个主干分支的**组织意图**（即研究意图→语料→主题→方法→评价→发现），但在每个主干下**展开为原文实际使用的字段**，并用横向关系边连接跨 RQ 关联。这可以视为把 Section 2.2 的 RQ 映射表整体提升为维度树的本体。

---

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将维度树从 6 个通用 leaf 扩展为覆盖原文 ~25 个提取字段的完整树 | `review.md` §维度树复原 → 维度树结构 | 参考 §4 建议树骨架，在 5 个主干分支下展开 RQ1–RQ4 的具体字段作为叶子维度，将 §2.2 的 RQ 映射表提升进树体。至少将 5 个候选叶子从独立表移入主树，并将 `not_verified` 状态按实际可读性修正。 | `paper_content.txt` §3.3, Tables 2–29 | **C** |
| 补充 quality assessment 维度和叶子 | `review.md` §维度树复原 | 新增 `[dim-quality]` 分支 + `[leaf-qa-criteria]` / `[leaf-qa-aggregate]` 叶子，取值空间为 12 criteria × Yes/Partly/No。 | `paper_content.txt` §3.4, Table 2 | **I** |
| 补充 gap analysis 和 recommendations 作为显式维度 | `review.md` §维度树复原 | 新增 `[dim-gap-roadmap]` 分支，含 `[leaf-gap-category]`（6 类）和 `[leaf-recommendation]`（8 条）。这两者是原文 finding 路径的核心环节。 | `paper_content.txt` §7, §8 | **I** |
| 补充 validity threats 维度 | `review.md` §维度树复原 | 新增 `[dim-validity]` 分支，`[leaf-validity-type]` 取值 construct/internal/external/conclusion。当前只有 Section 3.2（历史草稿）提及，未进入维度树。 | `paper_content.txt` §9 | **I** |
| 补充搜索/纳排协议维度 | `review.md` §维度树复原 | 新增 `[dim-search]` 分支，含 `[leaf-search-databases]`、`[leaf-search-results]`、`[leaf-snowballing]`。原文搜索链条（7 databases → 3934 → 3570 → 32 → 46）是 SLR 方法学核心。 | `paper_content.txt` §3.2 | **I** |
| 补充横向关系边 | `review.md` §维度树复原 | 新增至少 3 条关系边：RQ3.evaluation → measures → RQ2.solutions（评估方法度量方案）、RQ4.limitations → points_to → gap categories（局限指向缺口）、gap → derives → recommendations（缺口推导建议）。遵循 `pattern-field-schema.md` §8.3 合同。 | `paper_content.txt` §4–8 的跨 RQ 关联 | **I** |
| 补充 data/artifact 制品维度 | `review.md` §维度树复原 | 新增 `[dim-artifact]` 分支，记录原文的 figshare replication data 链接与 availability 状态。原文字面提供了 data link。 | `paper_content.txt` §Data availability, p.1 的 Dataset link 行 | **M** |
| 修正统计分母混淆 | `review.md` §统计与候选发现链路 | 区分「被审论文（Naveed 2024）的统计分母 = 46 primary studies」和「脚手架文库的分母 = 19 篇」。当前表格中 `[dim-mde-ml-components-slr-root]` 的分母写 "当前 19 篇 survey-of-surveys 样本"，但该行讨论的是被审论文的 tree type distribution，分母应为 46 或标注为 "不适用（树型定性判断）"。 | `paper_content.txt` §3.2, `SUMMARY.md` 三池规则 | **M** |
| 修正 A.2 证据账本中不合理的 `not_verified` | `review.md` A.2 表 | EV-mde-ml-components-slr-001（根节点证据）和 EV-mde-ml-components-slr-005（snowballing 证据）在 `paper_content.txt` 中均完整可读，应从 `not_verified` 升级为 `medium`（全文文本级；图表待人工核对）或 `strong`（若内容已明确）。 | `paper_content.txt` 摘要、§1、§3.2 | **M** |
| 扩展 A.4 复验清单 | `review.md` A.4 | 当前只有结构检查和视觉核对两项。应增加对原文 extraction form 完整性、quality assessment 表号、gap categories 枚举、recommendations 条数、validity threats 分类的专项复验项。 | `pattern-field-schema.md` §8.4 的 A.4 合同 | **M** |
| 补充对原文「初始数量不一致」风险的单独标注 | `review.md` §1 快速结论卡片（已有） → 应在 A.3 中增一条对应结论映射 | 原文 p.21 结论处写 3496/3934，而 §3.2 实际为 3570/3934。当前快速卡片已标注此风险，但 A.3 结论映射表没有对应的 `[clm-*]` 条目，建议增加一条 `[clm-*-numerical-inconsistency]` 标记为 `risk_only`。 | `paper_content.txt` p.21 vs §3.2 | **M** |

---

## 6. C/I/M 结论

### C（Critical — 直接破坏 Paper2 学术目标、证据链或 A2a/A2b 可靠性）

**C1：维度树是通用元维度接口而非原文 schema 复原。** 当前维度树的 6 个叶子是 A1-M0–M6 元维度的投影，而非 Naveed et al. (2024) 原文的 extraction form / classification schema / taxonomy 的忠实复原。原文有约 25 个明确抽取字段 + 12 个 QA 标准 + 4 类效度威胁 + 6 个 gap + 8 条 recommendation + 数据制品链接 + 搜索协议链，当前树只覆盖了约 20%（以候选叶子 + 元维度叶子合计约 11 个节点 vs 56 个真实信息点）。

**对 Paper2 学术目标的影响**：survey-of-surveys 脚手架的核心价值在于让 A2a/A2b 能从已完成 SLR 中抽取可迁移的维度模式、统计设计和 finding 路径。如果维度树是通用接口而非原文 schema，A2a 将无法从本树了解 MDE4ML SLR 实际使用了哪些字段、如何分类、如何统计和如何形成 finding。这直接破坏了脚手架对 Paper2 维度模式演化的支撑作用。A2a 要么被迫回头重读原文，要么基于一棵高度抽象的树做无根模式推断。

### I（Important — 实质影响维度树可用性、原文 schema 复原、证据可审计性）

**I1：候选叶子与主树分离。** 5 个 orig-* 候选叶子包含原文的部分真实字段，但被放在独立表中且标记为 `not_verified`。这使得 A2a 在阅读维度树本体时会得到一棵不含任何原文具体字段的空壳树，必须额外跳转到候选表才能发现碎片信息。应将这些字段整合进主树。

**I2：缺少 gap/roadmap/recommendation 维度。** 原文 §7 Gap Analysis 和 §8 Recommendations 是完整的 "统计观察 → gap → recommendation" finding 路径范例，对 Paper2 的候选发现→研究者裁决链路有直接启发价值，但维度树中没有对应分支。

**I3：缺少 validity threats 维度。** 原文 §9 有 construct/internal/external/conclusion 四类效度威胁报告，是典型的 validity threat pattern，应在维度树中反映。

**I4：缺少横向关系边。** 原文有明确的 RQ3→RQ2 评价关系（evaluation methods → measures → MDE solutions）和 RQ4→gap→recommendation 推导链，但维度树中没有任何横向关系边。

**I5：取值空间过于抽象。** 6 个主叶子的取值空间写的是方法论指导语（"完整枚举/层级枚举/自由文本"），而非原文实际分类值（如 "Automation/Quality/Complexity"），导致维度的可执行性低。

**I6：统计分母混淆。** 「统计与候选发现链路」表中混淆了被审论文的统计分母（46）和脚手架文库的分母（19），可能导致 A2a 误判节点的统计资格。

### M（Minor — 不阻塞的清晰度或维护性建议）

**M1：A.2 证据账本中若干 `not_verified` 标记偏保守。** EV-mde-ml-components-slr-001（根节点）和 EV-mde-ml-components-slr-005（snowballing）在 paper_content.txt 中内容完整可读，可升级为 `medium`。

**M2：A.4 复验清单项目过少。** 应增加 extraction form、QA、gap/recommendation、validity threats 的专项复验项。

**M3：原文 §10 Conclusion 的 3496/3934 数值不一致风险未在 A.3 中映射。** 快速结论卡片已标注，建议增一条 `risk_only` 结论映射。

---

### 最终建议：**NEEDS FIX**

当前 `review.md` 的 Section 2.2（RQ 映射表）写得很好且忠于原文，但维度树本体（§维度树复原）未能兑现 Section 2.2 的丰富内容。修复方向明确且可执行：

1. **将 Section 2.2 的 RQ→extraction field 映射提升为维度树的本体**（参照 §4 建议骨架），至少把 5 个候选叶子移入主树，并按原文 Tables 2–29 补充对应叶子维度。
2. **补充 quality assessment、gap/roadmap、validity threats、search protocol、data artifact 五个分支**。
3. **增加横向关系边**。
4. **修正证据强度标记和分母描述**。

修复后，这篇 `review.md` 将成为 survey-of-surveys 文库中最强的维度树样本之一——因为原文本身就是一篇方法学执行标准、提取字段完整、报告结构清晰的 SLR。当前树浪费了原文的这一优势。

---

*审计完成时间：2026-06-29*
*审核人：deepseek*
*证据基础：paper_content.txt 全文（2123 行）、review.md（427 行）、bibliography/metadata、文库 GUIDE/SUMMARY/pattern-field-schema、paper_story.md、ai-research-writing-skill references*
