# formal-re-llm-roadmap · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。读取了 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`（全文）、`references/paper-story.md`（全文）、`references/reviewer-guidelines.md`（全文）、`references/reviewer-self-review.md`（全文）。
- **是否读取 `$research-planning`**：是。读取了 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`（全文）、`references/planning-prompts.md`（全文）。
- **是否读取 `$oh-my-codex:autoresearch`**：是。读取了 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`（全文）。
- **是否完整阅读 `paper_content.txt`**：是。全文 2516 行，覆盖摘要、引言（Section 1）、背景（Section 2）、FM-based development 示例（Section 3，PROMELA/Spin/LTL/Python）、Roadmap A（Section 4，LLM→FM）、LLM-driven RE 示例（Section 5）、Roadmap B（Section 6，FM→LLM）、实践考虑与局限（Section 7）、结论与数据声明（Section 8）、参考文献。
- **是否核对 `paper.pdf`**：否。当前环境不支持可视化 PDF 页码级核对；但 `paper_content.txt` 提取了完整文本（含代码清单和图表说明），且 `metadata.json` 和 `review.md` 均已记录 Fig. 2 / Fig. 4 已人工核对。本审计仅依赖 `paper_content.txt` 的文本级证据，不依赖视觉图表比对，对需要图表外观核验的项均标注为待人工复核。
- **技能口径体现**：按 `$ai-research-writing-skill` 的 reviewer mode 要求，加载 `reviewer-guidelines.md`（通用审稿维度）、`reviewer-self-review.md`（自审框架）、`paper-story.md`（claim-evidence 纪律）；按 `$research-planning` 的 planning-prompts 理解论文结构分析方法论；按 `$oh-my-codex:autoresearch` 确认审计边界（本审计产出为 bounded deliverable，不触发 agent loop）。

- **文库级规则读取**：完整读取了 `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md` 和 `story/paper_story.md`。

---

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

本文**没有显式的编号化研究问题（RQ）**。其目标在摘要中清楚声明：

> **Objective**: This paper aims to address the concerns associated with the use of LLMs in RE activities. Specifically, it seeks to develop a roadmap that leverages formal methods (FMs) to provide guarantees of correctness, fairness, and trustworthiness when LLMs are utilised in RE. Symmetrically, it aims to explore how LLMs can be employed to make FMs more accessible.

这是一个**双向目标**：
1. 用 FMs 为 LLM-based RE 提供正确性、公平性、可信性保证（FM→LLM）。
2. 用 LLMs 提高 FMs 的可及性（LLM→FM）。

论文类型为 **vision / roadmap paper**。作者在引言中明确写明这是 vision paper，roadmap "should not be considered an exhaustive list"。

### 2.2 原文方法流程

本文的方法不是系统综述的标准流程（检索→纳排→抽取→编码→统计），而是 **illustrative example + roadmap proposal**：

1. **两组示例驱动**：用 Section 3 的 PROMELA/Spin 示例展示 FM-based development 的流程和局限；用 Section 5 的 LLM-driven RE 示例展示 LLM 在 RE 任务中的应用和局限。
2. **两个 roadmap 提案**：
   - Roadmap A（Section 4）：基于 Section 3 的示例，提出 LLM agents 如何支持 FM-based development 的 5 条研究大道（Fig. 2），每条附具体 action points。
   - Roadmap B（Section 6）：基于 Section 5 的示例，提出 FMs 如何增强 LLM-based development 的 8 条研究大道（Fig. 4），每条附具体 action points。
3. **实践考虑**（Section 7）：讨论专家协作、overreliance、FM 数据不足、制品维护、部署风险。
4. **数据声明**（Section 8）："No data was used for the research described in the article."

**重要**：本文没有进行系统检索、纳排、质量评价或数据综合。

### 2.3 原文显式结构元素

本文以下元素是论文自身提供的**原生结构**，不是外部观察者强加的：

| 结构元素 | 原文证据位置 | 内容 |
|---|---|---|
| **双路线图方向** | Section 4 标题、Section 6 标题 | Roadmap A：Using LLMs to support FM-based development；Roadmap B：Using FMs to support LLM-based development |
| **Roadmap A 的 5 条研究大道** | Section 4 正文 + Fig. 2 | ① NL2Formal (code gen from formal specs)；② Explainability/Tutorials (FM concept explanation)；③ NL-based Formal Model Evaluation (检查生成输出)；④ Formal Requirements Enhancement (reasoning about requirements)；⑤ Interactive Formalisation (human-in-the-loop formalisation) |
| **Roadmap B 的 8 条研究大道** | Section 6 正文 + Fig. 4 | ① Ensuring Correctness through Formal Requirements and Argumentation；② Improving Mathematical Reasoning with Formal LLMs；③ Formal Prompt Engineering；④ Formal Domain Knowledge and Explainability；⑤ Formal Requirements as Oracles；⑥ Formal Verification of Generated Code and Models；⑦ Trustworthiness Assessment；⑧ Human-in-the-Loop Verification |
| **每条大道的 action point** | Section 4 和 Section 6，以 ✦ 符号标记 | 每条大道 1--3 个具体 action point，格式为 "Action Point：..." |
| **两层架构隐喻** | Fig. 2 / Fig. 4 | Application Layer（RE/SE 任务）↔ LLM Layer（LLM agents）↔ FM Layer（formal tools）；Fig. 2 三层从下到上为 FM→LLM→Application，Fig. 4 方向相反 |
| **5 对 concern-mechanism 对** | Section 4 和 Section 6 的每条大道 | 每条大道陈述一个 concern（如 LLM 代码生成缺乏 verification）和 mechanism（如用 formal spec 作为 oracle） |
| **两组示例** | Section 3 + Section 5 | PROMELA/Spin/LTL/Python 验证示例 + LLM-driven RE 从需求到代码示例 |
| **实践风险清单** | Section 7 | 5 项实际考虑：专家协作需求、经验评估缺失、overreliance、FM 数据不足、部署/演化挑战 |
| **数据声明** | Section 8 | "No data was used for the research described in the article" |

**关键否定发现**：本文**不存在**以下 SLR/SMS 典型元素：
- 没有编号化 RQ 列表。
- 没有检索字符串、数据库列表、时间窗。
- 没有 PRISMA 流程图或纳排数。
- 没有 extraction form、coding scheme 或 classification taxonomy。
- 没有质量评价 rubric。
- 没有 evidence table（带计数的数据抽取表）。
- 没有频次/分布/交叉表统计分析。
- 没有从统计数据推导的 empirical findings。
- 作者声称的 contribution 是"two detailed roadmaps" + "action points"，不是 empirical/statistical findings。

### 2.4 原文如何形成 conclusion / finding

本文的 conclusion 直接来自 roadmaps 和 action points 的综合，而不是来自数据抽取和统计分析。形成路径为：

```
两组示例（揭示局限）→ 两个 roadmap（提出研究大道 + action points）→ 实践考虑（讨论风险和前提）→ 结论（"promising approach" + "激发进一步研究"）
```

作者明确声明 roadmaps 提供的是"激发研究"（stimulate research）的方向，不是已完成 evidence 的总结。

---

## 3. 当前 `review.md` 维度树审计

### 当前维度树概览

当前 `review.md` 维度树结构为：

```text
[dim-formal-re-llm-roadmap-root]
├── [b1] roadmap direction → [leaf-scope] 研究范围与单位对象
├── [b2] layer → [leaf-corpus] 语料与纳排链条
├── [b3] task family → [leaf-taxonomy] 主题与维度分类
├── [b4] assurance concern → [leaf-method] 方法/技术/干预分类
└── [b5] human gate / limitation
    ├── [leaf-evidence] 评价、证据与复现资产
    └── [leaf-finding] 统计观察与候选发现
```

外加 4 个"原文模式候选叶子"：
- orig-roadmap-direction（路线图方向）
- orig-task-family（任务族）
- orig-assurance-concern（可信性/保证关注点）
- orig-human-gate（人类裁决点）

### 维度树审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| **根节点是否准确** | 部分准确 | 根节点 `[dim-formal-re-llm-roadmap-root]` 正确识别了论文主题（formal RE + LLM），也正确标注了树型为"roadmap / concern / action-point 树"和 boundary_anchor 身份。但根节点没有体现本文最核心的结构特征：**双向对称路线图**。本文的 contribution 是"two-way roadmap"，这个"two-way"是全文组织逻辑的骨架，应该出现在根或根的直接子节点上。 | I |
| **主干分支是否覆盖原文 schema** | 否——分支是通用模板，不是原文 schema | 5 个分支（roadmap direction / layer / task family / assurance concern / human gate）的设计目标在 `review.md` 中被自述为"跨论文通用接口层"——即这 5 个分支是为所有 19 篇论文统一设计的检查类别，不是为本文专门复原的。本文的**真实原生结构**是：两条路线图 × 每条路线图的多个研究大道 × 每条研究大道的 action points、concern、mechanism、artifact 和 limitation。当前的 5 个分支中，b3（task family）和 b4（assurance concern）与原文有一定对应关系，但 b2（layer）和 b1（roadmap direction）的语义与原文结构错位。 | C |
| **叶子维度是否足够具体** | 否——6 个通用叶子 vs 原文 13 条研究大道 | `review.md` 的 A1-DT 口径校准段明确声明："下方叶子维度表的六个 leaf-* 是跨论文通用接口层...它不是对原文全部抽取字段、分类项或报告叶子的完成复原"。这意味着**当前叶子维度不是对本文原生 schema 的复原**，而是所有论文共享的检查清单。原文有 5 + 8 = 13 条具名研究大道（每条有独立标题和 action point），而当前树只有 6 个通用叶子 + 4 个粗粒度候选叶子。4 个候选叶子将 13 条研究大道压缩为 4 个笼统类别，丢失了大道名称、action point 文本、concern-mechanism 对等关键信息。 | C |
| **取值空间是否可执行** | 否——候选叶子只有笼统说明 | 4 个候选叶子的取值空间只写了自由文本描述（如"需求抽取、形式化、分析、验证、追踪、修复等 formal RE 任务族"），没有给出完整的枚举值列表、没有说明哪些来自原文哪些是推测、没有标注 `not_reported` vs `not_applicable` 语义。A2a 无法基于当前取值空间开始抽取。 | I |
| **关系边是否缺失** | 是——缺失原文内部的横向关系 | 本文有明确的关系结构：每条研究大道的 concern → mechanism → artifact → limitation 形成了因果链；两个 roadmap（A 和 B）是对称的互补关系；两组示例各自驱动一个 roadmap。当前树没有记录任何关系边。`pattern-field-schema.md` §8.3 要求记录关系边类型、源节点、目标节点和缺失语义，但当前树中完全缺失。 | I |
| **统计用途 / 分母是否正确** | 是——review 正确标注了不可统计 | 当前 review 正确地将所有叶子标注为"不进入主统计池；只作 schema seed / boundary anchor"，且 taxonomy、corpus 等叶子的统计用途标注为 `not_applicable`。这与本文的 roadmap 身份一致。 | 通过 |
| **候选 finding 路径是否完整** | 否——原文的 concrete action points 未被列为 finding seed | 原文的 15+ action points 是最高价值的候选 finding 种子：每个 action point 是一个"当前能力缺口 + 提议方向"的对偶，可以直接转为候选发现。但当前树只将其归入 4 个笼统类别而未逐条列出，A2a 将无法精确定位。 | I |
| **A.1--A.4 证据链是否足够** | 部分不足 | A.1（来源文件）正确列出了所有本地文件。A.2（证据表）的 4 条证据中，EV-001 是根问题证据（`not_verified`），EV-002--EV-004 全部标注为 `not_verified` 且"待 A2a 精确页码复核"。A.2 没有为原文的具体结构元素（每条研究大道、每个 action point、每对 concern-mechanism）建立独立证据条目，导致 A.3 的结论无法精确回链到原文位置。A.4 只列出了两项检查，且"visual check"标记为 `needs_manual_check`。 | I |
| **是否存在可能误导 A2a 的强主张** | 是——维度树标题"维度树复原"暗示已完成复原 | 标题"维度树复原"（dimension tree restoration）传达了"已经忠实复原了本文维度结构"的语义，但实际提供的是跨论文通用接口 + 4 个粗粒度候选叶子。标题与实际内容之间的 gap 会误导 A2a 认为当前树已经足够并直接开始抽取。 | C |

---

## 4. 建议维度树骨架

以下是与本文原生结构更契合的维度树。所有节点均基于 `paper_content.txt` 文本证据，取值空间从原文摘取，缺失值标注为 `not_applicable` 而非省略。

```text
[dim-formal-re-llm-roadmap-root] Formal RE + LLM two-way roadmap
│  tree_type = vision/roadmap, eligible_for_statistical_synthesis = false
│  evidence_basis = illustrative_examples (Section 3 + Section 5)
│  data_declaration = "No data was used for the research described in the article" (Section 8)
│
├── [dim-formal-re-llm-roadmap-direction] 路线图方向（双向对称）
│   │  取值空间 = {LLM_supporting_FM, FM_supporting_LLM}
│   │  原文锚点：Section 4 标题 / Section 6 标题
│   │
│   ├── [dim-formal-re-llm-roadmap-A] Roadmap A：Using LLMs to support FM-based development
│   │   │  原文锚点：Section 4 + Fig. 2；三层架构：Application Layer ↖ LLM Layer ↖ FM Layer
│   │   │
│   │   ├── [leaf-formal-re-llm-roadmap-A-avenue-01] NL2Formal：code generation from formal specifications
│   │   │   │  concern = NL需求到形式化代码间的gap；mechanism = LLM agents + FM tool chain + iterative refinements
│   │   │   │  action_point = "facilitate code generation from formal specifications...by leveraging the capability of LLMs to generate source code from specifications"（Section 4 ¶1--4）
│   │   │   │  artifact = source code (e.g. Python/Dafny)
│   │   │   │  limitation = 代码实现细节（host/port/socket）不在形式化模型中，需额外验证
│   │   │
│   │   ├── [leaf-formal-re-llm-roadmap-A-avenue-02] Explainability / Tutorials
│   │   │   │  concern = FM artifacts难以被非专家理解；mechanism = LLM summarisation + natural-language explanation of formal models, counterexamples, and verification results
│   │   │   │  action_point = "Explanations of FM artifacts can be achieved by...LLMs to generate...explanations"（Section 4 ¶5--8）
│   │   │   │  artifact = NL explanation of formal model / counterexample / verification report
│   │   │
│   │   ├── [leaf-formal-re-llm-roadmap-A-avenue-03] NL-based Formal Model Evaluation
│   │   │   │  concern = LLM 生成的 formal models 需要验证正确性；mechanism = LLM 自我评估 + formal verification
│   │   │   │  action_point = "To translate formal languages into one another, we can leverage LLMs"（Section 4 ¶9--10）
│   │   │   │  artifact = translated formal models
│   │   │
│   │   ├── [leaf-formal-re-llm-roadmap-A-avenue-04] Formal Requirements Enhancement
│   │   │   │  concern = 形式化需求需要持续迭代和演化；mechanism = LLM 辅助推理 + knowledge extraction
│   │   │   │  action_point = "To support iterations and evolution, we can leverage LLMs to perform reasoning...knowledge can be extracted"（Section 4 ¶11--13）
│   │   │   │  artifact = enhanced / refined formal requirements
│   │   │
│   │   └── [leaf-formal-re-llm-roadmap-A-avenue-05] Interactive Formalisation
│   │       │  concern = 形式化需要人类专业知识但门槛高；mechanism = human-in-the-loop + LLM agents for explanation and step guidance
│   │       │  action_point（隐含在 Section 4 对两层架构的描述中）
│   │       │  artifact = formal specification co-produced by human + LLM
│   │
│   └── [dim-formal-re-llm-roadmap-B] Roadmap B：Using FMs to support LLM-based development
│       │  原文锚点：Section 6 + Fig. 4；三层架构：LLM Layer ↖ FM Layer
│       │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-01] Ensuring Correctness through Formal Requirements and Argumentation
│       │   │  concern = LLM 输出 plausible but incorrect；mechanism = formal specification + verification + formal argumentation theory
│       │   │  action_point = "a formal development process can be adopted, supported by LLM-generated explanations...use of a formal argumentative structure to constrain LLM responses can enhance logical coherence"（Section 6 ¶1--4, ①）
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-02] Improving Mathematical Reasoning with Formal LLMs
│       │   │  concern = LLM 数学推理弱；mechanism = FM-trained LLMs + RAG + multi-agent
│       │   │  action_point = "leveraging specialised training, dynamic knowledge retrieval with RAG, and collaboration between multiple LLM agents"（Section 6 ¶5--7, ②）
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-03] Formal Prompt Engineering
│       │   │  concern = NL prompt ambiguity → 生成 artifacts 不可靠；mechanism = formal notations in prompts (ACSL) + prompt architecture design
│       │   │  action_point = "Using formal notation or controlled natural languages can help enhance the precision of NL prompts...develop interconnected prompt architectures using semi-formal languages"（Section 6 ¶8--10, ③）
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-04] Formal Domain Knowledge and Explainability
│       │   │  concern = 领域知识难以整合进 LLM；mechanism = formal ontology / knowledge graphs + LLM explainability
│       │   │  action_point（Section 6 ¶11--12, ④）：formal domain knowledge for explainability
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-05] Formal Requirements as Oracles
│       │   │  concern = 缺乏对 LLM 生成输出的自动验证；mechanism = formal requirements as test oracles / validation criteria
│       │   │  action_point（Section 6 ¶13--14, ⑤）
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-06] Formal Verification of Generated Code and Models
│       │   │  concern = LLM 生成的代码/模型可能包含 bug；mechanism = model checking / deductive verification of LLM-generated artifacts
│       │   │  action_point（Section 6 ¶15--17, ⑥）
│       │   │
│       ├── [leaf-formal-re-llm-roadmap-B-avenue-07] Trustworthiness Assessment
│       │   │  concern = LLM 输出的 correctness / fairness / trustworthiness 无法保证；mechanism = formal trustworthiness metrics + verification frameworks
│       │   │  action_point（Section 6 ¶18--20, ⑦）
│       │   │
│       └── [leaf-formal-re-llm-roadmap-B-avenue-08] Human-in-the-Loop Verification
│           │  concern = 全自动验证可能不可靠；mechanism = LLM-in-the-loop + human verification gate
│           │  action_point（Section 6 ¶21--22, ⑧）
│
├── [dim-formal-re-llm-roadmap-method] 方法 / 证据基础
│   │  取值空间 = {illustrative_example, literature_grounding, author_expertise}
│   │
│   ├── [leaf-formal-re-llm-roadmap-example-1] 示例 1：PROMELA/Spin sender-receiver
│   │   │  位置：Section 3 + Listings 1--4 + Fig. 1
│   │   │  演示内容：NL requirements → PROMELA model → LTL assertions → Spin verification → counterexample → Python implementation
│   │   │  揭示局限：FM 工具链复杂，需要专业知识；需要额外验证
│   │   │  驱动：Roadmap A
│   │
│   └── [leaf-formal-re-llm-roadmap-example-2] 示例 2：LLM-driven RE（red-crossing function）
│       │  位置：Section 5 + Fig. 3
│       │  演示内容：NL requirements → LLM 抽取/分析/分类/补全需求 → PlantUML sequence diagram → code gen
│       │  揭示局限：LLM 输出需要正确性验证、可解释性支持、领域知识边界检查
│       │  驱动：Roadmap B
│
├── [dim-formal-re-llm-roadmap-limitation] 实践考虑与局限
│   │  原文锚点：Section 7
│   │
│   ├── [leaf-formal-re-llm-roadmap-risk-01] 专家协作需求（expert-human required）
│   ├── [leaf-formal-re-llm-roadmap-risk-02] 经验评估缺失（no empirical evaluation yet）
│   ├── [leaf-formal-re-llm-roadmap-risk-03] Overreliance on LLMs
│   ├── [leaf-formal-re-llm-roadmap-risk-04] FM 数据不足（lack of FM training data）
│   ├── [leaf-formal-re-llm-roadmap-risk-05] 制品维护与部署/扩展风险
│   └── [leaf-formal-re-llm-roadmap-risk-06] 人类创造力不可替代
│
└── [dim-formal-re-llm-roadmap-assurance] 可信性关注点
    │  取值空间 = {correctness, fairness, trustworthiness, explainability, auditability, safety}
    │  此为两个 roadmap 的横切 concern，每条研究大道可标注其 address 的 concern(s)
    │
    └── （见各大道叶子的 concern 字段，此处为跨大道汇总索引）
```

### 4.1 建议维度树与原树的差异说明

| 差异点 | 原树 | 建议树 |
|---|---|---|
| **根节点体现双向** | 根节点只标注主题 | 根节点 + 第一级分支体现"two-way" |
| **主干为原文原生大道** | 主干为 5 个通用类别 | 主干为两个 roadmap 的 13 条研究大道 |
| **叶子粒度** | 6 个通用接口叶子 + 4 个笼统候选叶子 | 13 条具名大道（每条带 concern/mechanism/action_point/artifact/limitation 子字段） |
| **示例记录** | 未进入维度树 | 两条示例作为方法/证据基础独立分支 |
| **实践局限性** | 散布在 A.2 和 A.3 中 | 独立分支，逐条列出 Section 7 的 5+ 项考虑 |
| **关系边** | 缺失 | 示例→roadmap、concern→mechanism、avenue↔avenue（对称）等关系可明确记录 |
| **通用接口层** | 占据主干 | 可保留为横切索引（如 A1-M0--M6 贡献表），不占据维度树主干 |

### 4.2 当前 review 的可用部分

当前 review.md 的以下部分仍然有效且可以使用：
- 快速结论卡片（正确识别了 roadmap 身份和三池归类）。
- 阅读范围与证据锚点（覆盖了全文关键章节）。
- A1-M0--M6 脚手架元维度贡献表（对跨论文模式抽象有价值）。
- A.1 来源文件清单（完整正确）。
- 树型和统计池排除声明（正确标注为 boundary_anchor / `eligible_for_statistical_synthesis=false`）。

需要替换的是：维度树主干/叶子结构和 A.2/A.3/A.4 的证据锚点细节。

---

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| **F1：用原文原生维度树替换 6 个通用叶子** | `review.md` §维度树复原 | 将当前维度树从 5 分支 + 6 通用叶子替换为 §4 建议的双向 13 大道树。保留 A1-M0--M6 贡献表作为跨论文横切索引，但不占据维度树主干。 | `paper_content.txt` Section 4 + Section 6 + Fig. 2 + Fig. 4 | C |
| **F2：将"维度树复原"标题降级为"维度树候选草案"** | `review.md` 标题 + §维度树复原 | 标题从"维度树复原"改为"维度树候选草案（A1 seed，待 A2a 精核）"，并在开头明确声明当前树基于全文文本级阅读，尚未完成页码/表图/附录精核。 | `pattern-field-schema.md` §8.6（A1-DT 阶段临时降级规则） | C |
| **F3：逐条列出 13 条研究大道的 action point 原文** | `review.md` §维度树复原 → 每条叶子 | 为每条研究大道摘录原文 action point 段落或 ✦ 标记段落；标注 source page/section（如 Section 4 ¶n）。 | `paper_content.txt` Section 4 各 ¶、Section 6 各 ¶ | I |
| **F4：补充关系边表** | `review.md` §维度树复原或审计附录 | 为以下关系建立边表：① 示例 1 驱动 Roadmap A；② 示例 2 驱动 Roadmap B；③ 每条大道的 concern→mechanism→artifact；④ Roadmap A 和 Roadmap B 的对称关系；⑤ 6 个 concern 横切两条 roadmap。按 §8.3 格式填写源节点、关系类型、目标节点、取值空间。 | `paper_content.txt` Section 3--6；`pattern-field-schema.md` §8.3 | I |
| **F5：取消 b5 下挂两个叶子的非标结构** | `review.md` §维度树结构 | b5 同时挂 `leaf-evidence` 和 `leaf-finding` 打破了每分支一叶子的树形约定。在建议树中，实践局限分支的叶子是独立的多条 risk item，finding 路径通过每条大道的 concern/mechanism/limitation 表达。 | `review.md` 自身树结构 | I |
| **F6：明确标注"本文无 RQ / 无 extraction form / 无 taxonomy / 无统计 / 无 evidence table"** | `review.md` §维度树复原 | 在根节点说明中增加否定字段：rq_format = `not_applicable（vision/roadmap，用目标声明替代）`、extraction_form = `not_applicable`、coding_scheme = `not_applicable`、evidence_table = `not_applicable`、statistical_analysis = `not_applicable`、data_declaration = `"No data was used"`。避免 A2a 误以为本文有这些元素只是"待核验"。 | `paper_content.txt` 全文；Section 8 数据声明 | I |
| **F7：为每条大道叶子给出可执行取值空间** | `review.md` §叶子维度表 | 每条大道叶子应给出：① concern 的可枚举类型（来自原文 labeling）；② mechanism 的类型（LLM agent / RAG / formal verification / argumentation / ...）；③ artifact 类型；④ 状态（proposed / partially_demonstrated / not_verified）及其证据锚点。 | `paper_content.txt` Section 4 + Section 6 | I |
| **F8：在 A.2 为每条研究大道建立独立证据条目** | `review.md` A.2 证据表 | 当前 A.2 只有 4 条证据，且均为泛定位。建议为 13 条大道各自建立证据条目，标注原文段落/行号范围。 | `paper_content.txt` 各对应段落 | I |
| **F9：更新 A.4 人工核验清单** | `review.md` A.4 | 增加核对项：对照 `paper.pdf` 逐条核对 Fig. 2 和 Fig. 4 的大道编号、名称、action point 文本与 `paper_content.txt` 是否一致。 | `paper.pdf` Fig. 2 + Fig. 4 | M |
| **F10：保留并明确标注 6 通用接口为"跨论文横切索引"** | `review.md` §维度树复原或 A1-M0--M6 节 | 将 6 通用叶子从"维度树复原"主干中移出，改为 A1-M0--M6 贡献表中的行或审计附录中的横切检查表，并显式标注"通用接口，非本文原生 schema"。 | `review.md` 自身声明 + `pattern-field-schema.md` §8.6 | M |

---

## 6. C/I/M 结论

### C（Critical）——直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题

| 编号 | 问题 | 影响 |
|---|---|---|
| **C1** | 当前维度树的 6 个叶子是"跨论文通用接口层"而非本文原生 schema 复原。`review.md` 自身对此有声明，但维度树标题"维度树复原"与实际内容之间存在严重的语义 gap。A2a 若直接使用当前树进行字段抽取，会发现叶子定义与原文实际包含的信息不匹配，导致抽取失败或强行填充。 | 直接破坏 Paper2 的"维度模式演化"主线——如果单篇维度树不能忠实反映原文结构，跨论文模式抽象就失去了可追溯基础。 |
| **C2** | 维度树包含了本文不存在的 SLR/SMS 概念（语料与纳排链条、统计观察、evidence table），虽然标注了 `not_applicable`，但这些字段的出现在结构上暗示本文应按 SLR/SMS 框架评估。这违反了 `metadata.json` 中 `eligible_for_statistical_synthesis=false` 和 `review_type=vision/roadmap` 的分类纪律，也为 A2a 的跨论文统计埋下了分类混淆的风险。 | 若后续 A2a 不仔细核验每篇论文的 `review_type` 而直接根据叶子名称判断是否有可统计数据，roadmap/vision 论文的"not_applicable"可能被误读为"原文未报告但应存在"，导致错误归类。 |
| **C3** | 本文最核心的结构特征——**双向对称路线图**——在维度树中完全不可见。两条路线图的 13 条研究大道在树中被压缩为 4 个笼统候选叶子。这对 Paper2 的综述元模型设计是一个实质性损失：本文提供了少见的"两条路线图互为对称、每个 roadmap 有明确 concern→mechanism→artifact 链条"的模式，这种模式应该被脚手架捕获作为 schema seed，而不是被通用接口淹没。 | Paper2 的综述元模型若不能容纳 vision/roadmap 论文的双向结构，就无法从这类高价值文献中有效抽取维度先验。 |

### I（Important）——会实质影响维度树可用性、原文 schema 复原、证据可审计性的问题

| 编号 | 问题 | 影响 |
|---|---|---|
| **I1** | 原文的 15+ action points 未被逐条记录。每个 action point 是一个可操作的"gap + direction"对偶，是 Paper2 候选发现系统最直接的输入之一。当前只将其笼统归入 4 个候选叶子，A2a 将无法定位具体 action point 与后续候选发现的对应关系。 | 降低 Paper2 候选发现形成的粒度和追溯性。 |
| **I2** | 关系边完全缺失。原文有明确的关系结构（示例→roadmap、concern→mechanism、两条 roadmap 的对称性），这些都是 `pattern-field-schema.md` §8.3 要求记录的内容。 | 后续跨论文关系边分析缺少此篇的锚点。 |
| **I3** | A.2 证据表只有 4 条证据且均为泛定位（"摘要/引言页"、"方法/结果页"），没有为原文具体结构元素建立逐条证据。A.3 的结论声称从原文的"RQ / 方法 / 分类 / 评价 / 讨论结构"推导出叶子维度，但 A.2 中没有对应的精确锚点支撑这一声称。 | 证据链断裂：A.3→A.2 的回链无法精确验证。 |
| **I4** | 叶子"语料与纳排链条"的取值空间写为"完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明"，这假定了"语料与纳排"是所有综述类型论文的通用维度，但实际上 roadmap/vision 论文根本没有这个维度。把它作为维度树的一个正式叶子节点，是在分类学上犯了范畴错误。 | 如果 Paper2 的综述元模型包含"语料与纳排"作为通用维度，那么 roadmap/vision 论文将被错误地标记为"缺失此维度"而非"此维度不适用于此类论文"。 |
| **I5** | 当前 4 个候选叶子的取值空间都是自由文本而非可执行枚举，且没有与原文的具体段落/图号进行锚定。A2a 精核任务描述为"核对原文页码、表号/图号、附录或复现实验包"，但没有给出当前已知的部分取值。 | A2a 无法从当前状态开始工作，需要重新完整阅读原文。 |

### M（Minor）——不阻塞的清晰度或维护性建议

| 编号 | 问题 | 建议 |
|---|---|---|
| **M1** | 分支 b2 命名为"layer"，但原文的"layer"指的是 Fig. 2/Fig. 4 中的 Application/LLM/FM 三层架构，而叶子是"语料与纳排链条"，语义不匹配。 | 在建议树中，三层架构作为 Fig. 2/Fig. 4 的元数据记录，不作为分支标签。 |
| **M2** | b5 下挂两个叶子（evidence + finding）打破了树形结构每分支一叶子的约定。 | 在建议树中，实践局限和横切 concern 各自独立分支。 |
| **M3** | `review.md` 有大量标记为"历史草稿/迁移来源"的弃用节（§2.5、§3、§4、§5），增加了阅读噪音。 | 建议后续清理或折叠为 `<details>` 块。 |
| **M4** | 叶子"统计观察与候选发现"对 roadmap 论文的语义是"本文不包含统计观察但包含 action points 作为候选发现种子"，但叶子名称暗示统计观察存在只是未提取。 | 建议对于 roadmap 论文将叶子重命名为"候选发现种子与 action point"。 |

### 最终建议

**NEEDS FIX**。

当前 `review.md` 在快速结论卡片、三池归类、A1-M0--M6 贡献表和 A.1 来源清单方面是合格且有用的。但**维度树部分存在结构性问题**：6 个通用接口叶子不是本文原生 schema 的复原，构成了一个"能通过所有论文的通用清单"而非"忠实反映每篇论文独特结构的学术审计"。对本文而言，这意味着论文最重要的结构特征（双向对称路线图、13 条具名研究大道、action points、concern-mechanism 对、两组示例驱动）在当前维度树中不可见。

建议的修复路径：
1. **先修 C 级问题**：将维度树替换为基于本文原生结构的 13 大道树（§4），将标题降级为"候选草案"。
2. **再修 I 级问题**：逐条补充 action point 原文、关系边、否定字段声明和 A.2 精确证据锚点。
3. **最后处理 M 级**：清理弃用节、修正命名不一致。

修复后的树可以作为"原生结构 seed"供 A2a 消费，而现有的 A1-M0--M6 贡献表作为"跨论文横切索引"同时保留。两类结构互补而不互相替代。

---

*审计完成时间：2026-06-29*
*审计范围：单篇 `formal-re-llm-roadmap`*
*未修改仓库文件，未 push，未 gh comment*
