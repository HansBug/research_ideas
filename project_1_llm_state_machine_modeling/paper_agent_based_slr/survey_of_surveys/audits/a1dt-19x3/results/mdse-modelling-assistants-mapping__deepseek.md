# mdse-modelling-assistants-mapping · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是；读取路径：
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是；读取路径：
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是；读取路径：
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是；覆盖全文 1798 行，从 Page 1（Abstract/Keywords/Abbreviations）到 Page 16（Conclusions/Future Work/References），逐段阅读 §1 Introduction、§2 Related Work、§3 Systematic Mapping Study Design（含 §3.1 RQ/§3.2 Search Strategy/§3.3 I/E Criteria/§3.4 Quality Assessment/§3.5 Data Extraction）、§4 Results（§4.1-4.4 三个 RQ + RQ4 实践侧）、§5 Discussion、§6 Comparative Analysis、§7 Threats to Validity、§8 Conclusions；核对所有 Table（1-4）、Figure（1-15）的文中描述。
- **是否核对 `paper.pdf`**：否；原因是 reviewer 无视觉访问能力，无法打开 PDF 核验图表细节与页码。下文所有涉及 Table/Figure 的具体版面定位均以 `paper_content.txt` 中的文本描述为准，并标注为「图表待 PDF 视觉核对」。

**已读取的文库级规则与 story**：
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/SUMMARY.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/patterns/pattern-field-schema.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md`

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

- **MRQ**：What proposals exist in the literature and practice to assist humans during modelling tasks in MDSE tools?
- **RQ1**：How is software modelling assisted?（抽取 proposal 的 strategy 关键词 → 聚类为 6 类）
- **RQ2**：What goals and limitations do existing modelling assistance proposals report?（抽取 goal 和 limitation → G1-G7 + L1-L5/L-NS）
- **RQ3**：Which evaluation metrics and target users do existing modelling assistance proposals consider?（抽取 evaluation metric 和 target user → M1-M3/NE + U1-U3/U-NS）
- **RQ4 (practice side)**：What is the state of the practice of modelling assistance?（从 Gartner Magic Quadrant 2023 的 17 个 enterprise low-code platforms 中抽取 15 个 modelling assistance proposals）

**贡献声明**（§1 末 & §8）：
1. 首次对 MDSE 建模辅助（literature + practice 双轨）进行不限制特定 strategy 的系统映射。
2. 产出 5 组聚类：strategy（6 类）、goal（7 类）、limitation（5 类 + L-NS）、evaluation metric（3 类 + NE）、target user（3 类 + U-NS）。
3. 发现文献和实践中 limitation / metric / user 信息稀缺或缺失，呼吁建立 well-founded frameworks for designing modelling assistants。

### 2.2 原文方法流程

| 阶段 | 操作 | 输出 |
|---|---|---|
| 1. RQ 设计 | 初始四问 → 经 9 位 SE 专家咨询 → 精炼为 3 个 RQ + MRQ（Petersen et al. 2013 guideline） | §3.1 RQ1-RQ3 |
| 2. 检索策略 | PICO 构建 search string → 5 库检索（IEEE Xplore, ACM DL, Scopus, Springer Link, WoS）+ Wohlin 2014 snowballing（前向/后向 4 轮） | Fig. 2 整体设计图，Fig. 3 PRISMA 流图 |
| 3. 纳排标准 | I1/I2 + E1-E5；title/abstract/full-text 三轮筛选 | §3.3 |
| 4. 质量评价 | 10 题 3-Point-Likert-Scale（7 主观 + 3 客观：CORE/JCR/citations）→ 选前 12 篇作为 snowballing 种子 | Table 1（Quality Assessment Questionnaire） |
| 5. 数据抽取 | 针对每个 RQ 提取原文文本片段：RQ1→strategy keywords、RQ2→goal + limitation、RQ3→metric + user；空白字段记录为缺失 | §3.5 |
| 6. 聚类 | 基于作者术语（authors' terminology）聚类；R1（一作）聚类后 R4（二作）review，K-statistic=0.651（substantial agreement） | §4.1 |
| 7. 统计与可视化 | 对每棵分类树做频次/百分比分布；bubble chart 展示 cross-tab（G×L, M×U）；comparative analysis（literature vs practice） | Fig. 4-15, Tables 2-4 |
| 8. Finding 形成 | 从统计分布、交叉关系和缺失比例中归纳 3 个主要 finding → Discussion（§5-6） → Conclusions（§8） | 见 §2.4 |

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、图表、roadmap

#### 2.3.1 数据抽取表单（Data Extraction Form）

§3.5 明确定义了按 RQ 组织的抽取字段：

| RQ | 抽取字段 | 缺失处理 | 对应原文 Table/Fig |
|---|---|---|---|
| RQ1 | strategy keywords（原文作者用词） | 无显式缺失值标记（但 strategy 本质不适用"缺失"） | Table 2 |
| RQ2 | goals（原文作者声明的目标）; limitations（原文作者声明的限制） | 空字段→L-NS（limitation not specified）| Table 3, Fig. 5 |
| RQ3 | evaluation metrics（原文作者报告的评价指标）; target users（原文作者期望的用户）| 未评价→NE（not evaluated）；用户只写"user"→U-NS（user not specified）| Table 4, Fig. 6 |

注意：原文并非只有一份统一的 extraction form，而是 3 条独立的抽取指令 + 1 条实践侧指令（RQ4 从公开文档中抽取 15 个 practice proposals 的 strategy/goal/limitation/metric/user）。

#### 2.3.2 五棵分类树（Five Taxonomies）

原文产出了 **5 棵独立的分类/聚类 schema**，每棵都有明确的关键词映射表和取值空间：

| # | Taxonomy | 取值空间 | 证据来源 | 统计用途 |
|---|---|---|---|---|
| 1 | **Strategy taxonomy**（§4.2, Table 2） | `Tool`, `Guideline`, `Technique`, `Method`, `Framework`, `Language`（6 类） | 58 篇 proposals 的作者术语 + reviewer 聚类定义 | 频次分布（39.7% Tool, 19.0% Framework, etc.）；Fig. 4 饼图 |
| 2 | **Goal taxonomy**（§4.3, Table 3） | `G1 Change propagation`, `G2 Consistency checking`, `G3 Model compatibility`, `G4 Model quality`, `G5 User interaction`, `G6 Model evolution`, `G7 Vulnerability detection`（7 类） | 58 篇 proposals 的作者目标声明 | 频次分布；与 limitation 做 cross-tab bubble chart（Fig. 5） |
| 3 | **Limitation taxonomy**（§4.3, Table 3） | `L1 Maturity/Usability`, `L2 Evaluation`, `L3 Generality`, `L4 Learnability`, `L5 Scope` + `L-NS (Not Specified)`（5 类+缺失类） | 58 篇 proposals 的作者限制声明 + 空字段 | 频次分布（50% L-NS）；与 goal 做 cross-tab（Fig. 5） |
| 4 | **Evaluation metric taxonomy**（§4.4, Table 4） | `M1 Effectiveness`, `M2 Efficiency`, `M3 User perception` + `NE (Not Evaluated)`（3 类+缺失类）；按 TAM 框架定义 | 58 篇 proposals 的评价指标文本 | 频次分布；与 user 做 cross-tab bubble chart（Fig. 6） |
| 5 | **Target user taxonomy**（§4.4, Table 4） | `U1 Designers/Modellers`, `U2 Domain experts`, `U3 Software developers` + `U-NS (Not Specified)`（3 类+缺失类） | 58 篇 proposals 的用户描述 | 频次分布；与 metric 做 cross-tab（Fig. 6） |

#### 2.3.3 质量评价量表（Quality Rubric）

Table 1：10 题 3-Point-Likert-Scale 质量评价问卷（得分值 -1/0/+1），覆盖 subjective quality（Q1-Q8）和 objective quality（Q9=CORE/JCR ranking, Q10=citation count）。该量表不仅用于筛选，也是后续 snowballing 种子选择的依据（top 12 above 80th percentile）。

#### 2.3.4 PRISMA 流图（Evidence Flow）

Fig. 3 是标准 PRISMA 流图，记录了从 1,996 条数据库记录 + 5 条 external → 1,175 条 snowballing → 3,176 条 screened → 77 条 possible → 58 条 final 的完整筛选链路，并附带 quality assessment 得分分布。

#### 2.3.5 方法论架构图（Roadmap/Design Figure）

Fig. 2：「Systematic mapping study design overview」—从 Research Questions → Search Strategy → I/E Criteria → Quality Assessment → Data Extraction 的完整流程架构图，标注每个阶段的 input/output。

#### 2.3.6 统计交叉分析

- Fig. 5：Goal × Limitation bubble chart（G1-G7 vs L1-L5/L-NS 的二维交叉分布）
- Fig. 6：Metric × User bubble chart（M1-M3/NE vs U1-U3/U-NS 的二维交叉分布）
- §6：Literature vs Practice 对照分析（Table-like 对比：literature 58 proposals 的 G/L/M/U 模式 vs practice 15 proposals 的 G/L/M/U 模式）

#### 2.3.7 效度威胁分类体系（Validity Threat Taxonomy）

§7 使用经典的 internal/construct/external validity 三分法，每个大类下又细分：
- Internal: selection bias, data extraction bias, inter-rater reliability, subjective interpretation
- Construct: grey literature bias, search bias
- External: language bias

#### 2.3.8 原始数据/制品

原文在 §3.1 脚注 1 和 §4.1 脚注 4 中声明所有研究材料（research protocol、raw extracted data）发布在 Zenodo（https://zenodo.org/records/10262145）。

### 2.4 原文从字段/统计观察到 conclusion/finding/gap/recommendation 的形成路径

原文的 finding 形成路径遵循清晰的分层：

| 层次 | 原文操作 | 原文输出 |
|---|---|---|
| **Field-level** | 对每篇 proposal 按 RQ1/RQ2/RQ3 抽取策略/目标/限制/指标/用户文本 | Raw data（Zenodo） |
| **Category-level** | R1 基于作者术语聚类，R4 review，K=0.651 | 5 棵分类树（Tables 2-4） |
| **Statistical observation** | 计频/百分比；二维 cross-tab；literature vs practice 对比 | Fig. 4-15 和 §4-6 正文叙述 |
| **Finding-level** | 从统计中提炼模式+(absence evidence) | 主要 finding：（1）93.1% 使用基于软件的 strategy；（2）50% proposals 不报告 limitation；（3）metric 和 user 信息稀缺/缺失；（4）实践侧 leader 工具更多文档化 modelling assistance |
| **Gap/recommendation** | Finding → 推理 → 建议 | 呼吁建立 well-founded frameworks for designing modelling assistants；未来工作建议进行 external validation、扩展 grey literature、建立 common terminology |

关键观察：原文的 finding 不是来自单一统计表的列联，而是一个「五棵分类树 × 交叉分析 × 缺失统计 × 文献-实践对照」的多路径综合推理，且明确承认 finding 强度受样本规模（N=58）、author terminology bias 和文档可得性（practice 侧仅公开文档）限制。

---

## 3. 当前 `review.md` 维度树审计

### 3.1 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | ⚠️ 通过但片面 | 当前 `review.md` 使用 A1-M0--M6 七元维度作为整个维度树的骨架（`dim-mdse-modelling-assistants-mapping-root → [dim-mdse-modelling-assistants-mapping-m0] ... [dim-mdse-modelling-assistants-mapping-m6]`）。这是 survey-of-surveys 脚手架定义的**元级维度框架**，用于跨论文比较综述方法学特征，而非本文自己的 schema。从元级复用的角度看，这篇 mapping 确实可被投射到 A1-M0--M6 各槽位；但这棵树的骨架是脚手架的通用接口，不是论文的专属 schema。结论：根节点和主干分支对的靶子是「论文是否可填充 A1-M0--M6」，而非「论文自身的维度树是什么」。| I |
| 主干分支是否覆盖原文 schema | ❌ 严重不足 | 原文拥有 **5 棵独立分类树 + 1 套质量量表 + 纳排标准 + PRISMA 流图 + 效度分类 + 文献-实践对照维度**。当前 review.md 的主干分支只有 7 个 A1-M0--M6 槽位。在这 7 个槽中，A1-M3（方法/技术/干预）试图装入原文的 strategy taxonomy，A1-M4（评价/证据/复现资产）试图装入 metric taxonomy，A1-M2（研究对象与主题语义）试图装入 target user taxonomy——但这意味着原文的 **5 棵分类树被压缩进了 3 个 meta-slot**，而 goal taxonomy（G1-G7）、limitation taxonomy（L1-L5/L-NS）、质量评价量表（Q1-Q10）、纳排标准（I1/I2/E1-E5）、PRISMA 流图、效度分类和文献-实践对照维度的独立结构被彻底消解。| C |
| 叶子维度是否足够具体 | ❌ 严重不足 | A1-M0--M6 是 7 个**高度抽象的操作化问题**（例如「A1-M2 研究对象与主题语义：论文研究了什么对象，使用了哪些主题、领域或语义范畴来组织研究对象？」），不是原文的分类取值空间。原文的叶子是具体的：`Strategy ∈ {Tool, Guideline, Technique, Method, Framework, Language}`、`Goal ∈ {G1..G7}`、`Limitation ∈ {L1..L5, L-NS}` 等。当前 review.md 将原文叶子列为「原文模式候选叶子」并从 A.3 标注为需要 A2a 精核——但在维度树主结构中并没有体现为正式节点。实际读起来，树的 7 片叶子仍是 7 个通用 A1-M0--M6 操作化问题。| C |
| 取值空间是否可执行 | ❌ 不可执行 | A1-M0--M6 的取值空间是「自由文本 + 短语级摘要」，在 review.md 的 §A.2 evidence ledger 中表现为自然语言证据段。但对“原文 classification schema”的取值空间——即 5 棵分类树的完整枚举——当前 review.md 没有以结构化形式给出。这意味着后续 A2a 无法基于当前维度树直接执行「看另一篇论文是否有相同的 goal taxonomy」，因为 goal taxonomy 的 7 类取值没有作为树的叶子出现。| C |
| 关系边是否缺失 | ❌ 严重缺失 | 原文存在大量可审计、可结构化的关系边：Goal × Limitation cross-tab（Fig. 5）、Metric × User cross-tab（Fig. 6）、Strategy × Goal（正文隐式）、RQ → Data Extraction Field、I/E Criteria → Study Selection → PRISMA Flow → Final Set、Quality Assessment Score → Snowballing Seed Selection → Final Set。当前 review.md 仅在 A.3 中记录了 2 条关系边（`edge-mdse-modelling-assistants-mapping-method-evidence` 和 `edge-mdse-modelling-assistants-mapping-taxonomy-finding`），且定义极为泛化。PRISMA 流图的分母链路（3,176→77→58）和 quality rubric 筛选链路完全未作为关系边出现。| I |
| 统计用途 / 分母是否正确 | ⚠️ 部分正确但缺乏结构化映射 | review.md §0 快速结论卡片中记录了「文献分母 3,176 screened → 58 纳入」「实践分母 17 工具 → 15 proposals」。这些数字是正确的。但 review.md **没有把原文的统计逻辑（哪些字段基于 N=58 全量、哪些基于 N=29 有 limitation 的子集、哪些基于文献 vs. 实践双轨）映射到维度树的叶子或关系边上**。例如原文发现「50% proposals 不报告 limitation（29/58）」依赖于 limitation taxonomy 的 L-NS 类——但 L-NS 作为叶子取值没有出现在维度树中。后续 A2a 若只读维度树而不回原文，会丢失这一关键分母条件。| I |
| 候选 finding 路径是否完整 | ❌ 不完整 | review.md A.3 列出了 12 条 `A1DT-mdse-modelling-assistants-mapping-C01` 到 `-C12` 的结论。其中 C02--C07 是 6 条「叶子维度定义」结论（对应 A1-M1--M6），C08 是可迁移性声明，C09 是 finding boundary，C10/C11 是两条关系边，C12 是原文候选叶子状态。但 review.md **没有记录原文的实际发现路径**：从 58 篇数据抽取 → 5 棵分类树聚类 → 统计频次与交叉表 → 3 个核心 finding → gap/recommendation。当前 A.3 的 12 条结论是**关于维度树本身的元结论**（「这个叶子定义了…」），不是「原文通过什么路径形成了什么发现」。| I |
| A.1--A.4 证据链是否足够 | ⚠️ 形式合规但证据定位不足 | A.1 来源表、A.2 evidence ledger（5 条 EV）、A.3 conclusion ledger（12 条）、A.4 复验清单均存在，且回链关系（A.2→A.1, A.3→A.2）形式上闭合。但 A.2 的 5 条证据均为**泛定位级**（例如 EV-003 覆盖「全文 §3-§8」），未做到 §8.2 合同要求的「原文页码、表号、段落号」级精确锚定。EV-005（关系边证据）的定位写「正文分类和统计表关联」，过于泛化。这 5 条证据均标记为 `weak`，符合 A1-DT 降级规则，但用于后续 A2a 时必须有精确锚定升级计划。当前 review.md 缺少该升级路线图。| I |
| 是否存在可能误导 A2a 的强主张 | ❌ 存在 | 快速结论卡片中写道：「最值得迁移的不是具体比例，而是 strategy--goal--limitation--metric--user 的**树状元维度**，以及把 `not specified / not evaluated / not found` 当成一等字段而非空值的报告方式」。这句话在两层上可能误导 A2a：（1）将 5 棵独立分类树描述为「树状元维度」暗示它们之间有统一层级，但原文的 strategy/goal/limitation/metric/user 是 **5 棵并列的独立分类树**，不是一棵统一维度树的 5 个分支——它们之间是 cross-tab 关系（bubble chart），不是 is-a 或 has-a 关系；（2）`not specified / not evaluated / not found` 的缺失值语义确实是一个有价值的脚手架启发，但当前维度树并未系统化定义 5 棵分类树各自的 missing value semantics（L-NS, NE, U-NS 的处理方式在 review.md 中没有作为叶子出现）。| I |

### 3.2 审计核心发现

当前 `review.md` 的维度树存在结构性问题：**它用 A1-M0--M6 脚手架元维度替换了原文的真实 schema**。虽然元级投射能覆盖论文的部分信息（例如 A1-M1 对应检索/纳排，A1-M3 对应 strategy），但原文的 5 棵独立分类树 + 质量量表 + 纳排标准 + PRISMA 流图 + 效度分类 + 文献-实践对照轴的丰富结构被严重压扁。

更精确地说，这不是「树过小」，而是「把通用元接口当成原文 schema」。review.md 本应在元维度投射之外**同时还原**原文的专属维度树——例如「原文的 classification schema 包含 5 棵分类树：Strategy(6 类)、Goal(7 类)、Limitation(5 类+缺失)、Metric(3 类+缺失)、User(3 类+缺失)；每棵树都有独立的关键词映射表和统计用途」——并将这些信息作为 A2a 可执行的 schema seed。

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树骨架。这棵树的根是论文本身的系统映射结构，不是 A1-M0--M6 元框架。

```
[dim-mdse-modelling-assistants-mapping-root] Mosquera 2024 系统映射
│
├── [dim-rq] 研究问题体系
│   ├── [leaf-rq-mrq] MRQ: literature & practice 中有哪些 modelling assistance proposals?（取值：{MRQ text}）
│   ├── [leaf-rq-rq1] RQ1: 如何辅助？（取值映射 → strategy taxonomy）
│   ├── [leaf-rq-rq2] RQ2: 目标和限制？（取值映射 → goal taxonomy + limitation taxonomy）
│   ├── [leaf-rq-rq3] RQ3: 评价指标和用户？（取值映射 → metric taxonomy + user taxonomy）
│   └── [leaf-rq-rq4] RQ4: 实践状态？（取值：{来自 GMQ 17 tools 的 15 proposals}）
│
├── [dim-method] 方法流程
│   ├── [leaf-search-db] 数据库检索（取值：{IEEE Xplore, ACM DL, Scopus, Springer Link, WoS}, search string, 1985-2024）
│   ├── [leaf-search-snowball] Snowballing（取值：{Wohlin 2014, 4 rounds, 12 seed papers from top quality}, 1,175 additional records）
│   ├── [leaf-ie-criteria] 纳排标准（取值：{I1, I2; E1-E5} 一一枚举）
│   ├── [leaf-quality-assessment] 质量评价量表（取值：{Q1-Q10, 3-Point-Likert-Scale, -1/0/+1}, subjective vs objective 维度）
│   ├── [leaf-data-extraction-form] 数据抽取表单（取值：{RQ1→strategy keywords; RQ2→goal+limitation; RQ3→metric+user; 空→NS/NE}; RQ4→public docs}
│   ├── [leaf-prisma-flow] PRISMA 筛选流（取值：{1996+5→2001→77→58}, K=0.634）
│   └── [leaf-clustering-method] 聚类方法（取值：{author terminology-based clustering, R1 cluster→R4 review, K=0.651, triangulation}）
│
├── [dim-classification-taxonomies] 五棵分类树（核心 contribution）
│   ├── [tax-strategy] Strategy taxonomy（Table 2）
│   │   ├── [leaf-strat-tool] Tool（39.7%, 23 proposals）
│   │   ├── [leaf-strat-framework] Framework（19.0%, 11 proposals）
│   │   ├── [leaf-strat-technique] Technique（15.5%, 9 proposals）
│   │   ├── [leaf-strat-method] Method（13.8%, 8 proposals）
│   │   ├── [leaf-strat-guideline] Guideline（6.9%, 4 proposals）
│   │   └── [leaf-strat-language] Language（5.2%, 3 proposals）
│   │   取值完整性：N=58；无缺失；原文 Fig. 4 饼图
│   │
│   ├── [tax-goal] Goal taxonomy（Table 3, §4.3）
│   │   ├── [leaf-goal-g1] G1 Change propagation
│   │   ├── [leaf-goal-g2] G2 Consistency checking
│   │   ├── [leaf-goal-g3] G3 Model compatibility
│   │   ├── [leaf-goal-g4] G4 Model quality（multi-aspect）
│   │   ├── [leaf-goal-g5] G5 User interaction
│   │   ├── [leaf-goal-g6] G6 Model evolution（creating new models）
│   │   └── [leaf-goal-g7] G7 Vulnerability detection
│   │   取值完整性：N=58；cross-tab with limitation taxonomy via Fig. 5
│   │
│   ├── [tax-limitation] Limitation taxonomy（Table 3, §4.3）
│   │   ├── [leaf-lim-l1] L1 Maturity/Usability
│   │   ├── [leaf-lim-l2] L2 Evaluation
│   │   ├── [leaf-lim-l3] L3 Generality
│   │   ├── [leaf-lim-l4] L4 Learnability
│   │   ├── [leaf-lim-l5] L5 Scope
│   │   └── [leaf-lim-lns] L-NS（Not Specified; 50.0%=29 proposals）
│   │   缺失值语义：L-NS = proposal 原文未显式声明限制，非 reviewer 遗漏
│   │   ⚠️ review.md 指出的「五类/六类不一致」：Table 3 正文定义 L1-L5 共 5 类 + L-NS（缺失），review 已标注待复核
│   │
│   ├── [tax-metric] Metric taxonomy（Table 4, §4.4）
│   │   ├── [leaf-met-m1] M1 Effectiveness（基于 TAM）
│   │   ├── [leaf-met-m2] M2 Efficiency（基于 TAM）
│   │   ├── [leaf-met-m3] M3 User perception（基于 TAM）
│   │   └── [leaf-met-ne] NE（Not Evaluated; 原文脚注列表 [21-23,25-28,30-39,41-50,54,64,65,70,72,73,76,77]）
│   │   取值完整性：N=58；NE 列表明确
│   │
│   └── [tax-user] Target user taxonomy（Table 4, §4.4）
│       ├── [leaf-usr-u1] U1 Designers/Modellers
│       ├── [leaf-usr-u2] U2 Domain experts
│       ├── [leaf-usr-u3] U3 Software developers
│       └── [leaf-usr-uns] U-NS（Not Specified; 原文脚注列表）
│       取值完整性：N=58；U-NS 列表明确
│
├── [dim-cross-analysis] 交叉分析维度（关系边密集）
│   ├── [edge-cross-gl] Goal × Limitation cross-tab（Fig. 5 bubble chart）
│   │   ├── 源节点：[tax-goal]，目标节点：[tax-limitation]
│   │   ├── 关系类型：metric/measure（交叉频次）
│   │   └── 产出：G2×L3,L5 有显著关系（50%）；G5 和 G4 的 limitation documentation 缺失
│   │
│   ├── [edge-cross-mu] Metric × User cross-tab（Fig. 6 bubble chart）
│   │   ├── 源节点：[tax-metric]，目标节点：[tax-user]
│   │   ├── 关系类型：metric/measure（交叉频次）
│   │   └── 产出：多数 proposal 集中在 U3×M1/M2
│   │
│   └── [edge-cross-litprac] Literature vs Practice 对照（§6）
│       ├── 源节点：literature set（58 proposals），目标节点：practice set（15 proposals）
│       ├── 关系类型：compare（同字段对照）
│       └── 产出：leader tools 更多文档化 modelling assistance；practice 侧 goal/limitation/metric/user 模式趋同
│
├── [dim-evidence-artifacts] 证据与制品
│   ├── [leaf-evidence-tables] Evidence tables（取值：{Table 2, Table 3, Table 4}）
│   ├── [leaf-evidence-figures] Figures（取值：{Fig.2 study design, Fig.3 PRISMA, Fig.4 strategy dist, Fig.5 G×L bubble, Fig.6 M×U bubble, Fig.7-14 various, Fig.15 summary}）
│   ├── [leaf-evidence-zenodo] Raw data & protocol（取值：{Zenodo DOI: 10.5281/zenodo.10262145}）
│   ├── [leaf-evidence-quality-scores] Quality assessment scores（取值：{per-proposal Q1-Q10 scores}）
│   └── [leaf-evidence-kappa] Inter-rater reliability（取值：{selection K=0.634, clustering K=0.651, Landis & Koch substantial}）
│
├── [dim-validity-threats] 效度威胁分类
│   ├── [leaf-vt-internal] Internal validity（取值：{selection bias, data extraction bias, inter-rater reliability, subjective interpretation}）
│   ├── [leaf-vt-construct] Construct validity（取值：{grey literature bias, search bias}）
│   └── [leaf-vt-external] External validity（取值：{language bias}）
│
└── [dim-finding-path] Finding 形成路径与结论
    ├── [leaf-fp-stat-observation] 统计观察（取值：{频次: 39.7% Tool, 50% L-NS, ...; 交叉: G2×L3/L5, ...}）
    ├── [leaf-fp-absence-evidence] 缺失证据（取值：{50% proposals 无 limitation; metric/user 稀疏; practice 工具文档不足}）
    ├── [leaf-fp-core-finding-1] Finding 1: 93.1% proposals 使用 software-based strategy
    ├── [leaf-fp-core-finding-2] Finding 2: 限制/指标/用户信息稀缺或缺失
    ├── [leaf-fp-core-finding-3] Finding 3: 文献与实践均认可 modelling assistance 价值，但缺乏 well-founded frameworks
    ├── [leaf-fp-gap] Gap: need for frameworks for designing modelling assistants focusing on target users' needs
    ├── [leaf-fp-future-work] Future work（取值：{external validation with peer review, broaden grey literature, common terminology, AI/LLM-powered assistants 方向判断}）
    └── [leaf-fp-roadmap-claim] Roadmap/vision 声明（取值：{AI advent → more assistants expected, imperative need for frameworks}；⚠️ 不得计为 empirical finding）
```

**此树与当前 review.md 的关系**：A1-M0--M6 元维度可以作为这棵专属树的另一种正交投射（即每个专属节点可以额外挂接一个 A1-Mx 标签），用于跨论文 comparison。但专属树本身必须作为独立结构存在，不能被元维度消灭。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补充原文的 5 棵分类树为正式维度节点 | `review.md` §维度树结构 | 将当前以 A1-M0--M6 为主干的维度树扩展为「双树结构」：A. 元维度投影树（A1-M0--M6，保留用于跨论文比较）；B. 专属 schema 树（上述 §4 结构，直接对应论文的 5 棵 taxonomy + 质量量表 + 效度分类 + 文献-实践对照维度）。两树通过交叉引用互链。 | paper_content.txt §4.2-4.4, Tables 2-4 | C |
| 为 5 棵分类树补充完整取值枚举与统计分母 | `review.md` §维度树取值空间 | 对每棵 taxonomy 列出完整的取值空间（如 Strategy: Tool/Guideline/Technique/Method/Framework/Language），标注每类的 proposal 数和百分比（基于 N=58），记录缺失值计数和语义（L-NS, NE, U-NS） | paper_content.txt Tables 2-4, Fig. 4-6 | C |
| 补充 Goal × Limitation 和 Metric × User 的关系边 | `review.md` A.3 或新增 relation edge ledger | 添加至少 2 条可审计关系边：`[edge-cross-gl]` 和 `[edge-cross-mu]`，标注源/目标节点、关系类型（cross-tab/measure）、原文证据锚点（Table 3+Fig.5, Table 4+Fig.6）、交叉发现和缺失语义 | paper_content.txt §4.3-4.4, Fig. 5-6 | I |
| 补充 PRISMA 流图作为证据链节点与关系边 | `review.md` §维度树 | 添加 PRISMA 流图节点链：`[leaf-prisma-flow]: 3,176 screened → 77 possible → 58 final`，并标注从检索→筛选→纳排的分母逻辑作为关系边；当前 review 仅在 §0 快速卡片中提及分母数字，未在维度树中结构化 | paper_content.txt §4.1, Fig. 3 | I |
| 补充质量评价量表（Q1-Q10）为独立 schema 元素 | `review.md` §维度树 | 原文的质量评价量表（10 题 3-Point-Likert-Scale）是一个独立的方法学组件，不归属 strategy/goal/limitation 任何一棵树。应在维度树中创建 `[leaf-quality-assessment]` 节点 | paper_content.txt §3.4, Table 1 | I |
| 将「五棵分类树」与「五个元叶子」的误称修正 | `review.md` §0 快速结论卡片 或 A.3 解释 | 当前 review.md 使用「strategy--goal--limitation--metric--user 树状元维度」的表述，暗示 5 棵树之间有层级关系。应修正为「5 棵并列的独立分类树」，并说明它们之间是 cross-tab 关系而非 is-a/has-a 关系 | paper_content.txt Tables 2-4 各自独立定义 | I |
| 补充 Finding 形成路径的结构化映射 | `review.md` A.3 | 当前 A.3 的 12 条结论是关于维度树本身的元结论。应增设至少 3 条记录原文从统计观察→核心 finding→gap/recommendation 的实际推理路径，并标注每步对应的证据节点 | paper_content.txt §4-6, §8 | I |
| 升级 A.2 证据锚点精确度（prep for A2a） | `review.md` A.2 | 当前 5 条 EV 均为泛定位（如「全文 §3-§8」）。应在 A2a 启动前至少将核心证据（Tables 2/3/4, Fig 3/4/5/6, §3.5 extraction form, §3.3 I/E criteria）的锚点升级为「Table N + 页码 + 行号范围」级 | pattern-field-schema.md §8.2 证据链合同 | I |
| 补充文献→实践对照的比较维度 | `review.md` §维度树 | 原文特别设置了 RQ4 作为实践侧，并在 §6 做了系统的 literature vs practice comparative analysis。当前维度树未将其作为独立维度。应添加 `[edge-cross-litprac]` 节点 | paper_content.txt §5-6 | M |
| 将 roadmap/vision 声明标记为不可进入统计 | `review.md` §0 或 A.3 | 原文 §8 Conclusions 中关于「AI advent → more assistants」和「imperative need for frameworks」的声明是 roadmap/vision，不是 empirical finding。应在 A.3 中显式标记为 `boundary_anchor` 或 `do_not_use`（statistical sense）| paper_content.txt §8 | M |
| 复核「五类/六类 limitation」不一致 | `review.md` §0 | 当前 review.md 已标注「Table 3 中 limitation 数量口径存在"五类/六类"不一致，需复核」。建议在 A.4 中增加一条指向 Table 3 原文的核对指令 | paper_content.txt Table 3 | M |

## 6. C/I/M 结论

### 6.1 分类定义（复述 survey_of_surveys 口径）

- **C**：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题。
- **I**：会实质影响维度树可用性、原文 schema 复原、证据可审计性的问题。
- **M**：不阻塞的清晰度或维护性建议。

### 6.2 本论文审计 C/I/M

#### C 级（2 项）

1. **原文 5 棵分类树被 A1-M0--M6 元维度消灭**：这是最严重的问题。当前维度树把原文的 5 棵独立 taxonomy、质量量表、纳排标准、PRISMA 流图、效度分类和文献-实践对照维度全部压缩进 7 个通用 meta-slot。A2a 如果继承这棵树作为「论文已有的 schema seed」，将**无法识别原文实际使用了哪些 classification schema、每个 schema 的取值空间是什么、它们之间如何 cross-tab**。这会直接导致 Paper2 维度模式演化的起点偏差——后续所有基于"这篇论文有什么 schema"的判断都将基于一个过度归约的骨架。

   **对 Paper2 的影响**：维度模式演化（A2a "种子论文压力测试候选维度模式"）的第一步是从 A1 脚手架中提取可操作的维度候选。如果这篇 IST 2024 mapping 的 schema seed 只有 7 个 A1-M0--M6 槽位，A2a 将无法识别原文的 5 个独立 classification dimension（strategy / goal / limitation / metric / user），也无法获得它们的完整取值空间、缺失语义和交叉统计逻辑。这会系统性地削弱 A2a 的 schema 初始精度。

2. **取值空间不可执行**：A2a 需要的不只是「这篇论文讨论了 evaluation metrics」，而是「这篇论文用 M1/M2/M3/NE 四类分类 evaluation metrics，每类有明确的关键词映射（Table 4）和统计频次」。当前 review.md 将取值空间写成「自由文本+短语摘要」，后续 A2a 无法直接基于此树做交叉论文的维度一致性检验。

#### I 级（5 项）

3. **关系边缺失**：Goal × Limitation cross-tab（Fig. 5）和 Metric × User cross-tab（Fig. 6）是原文方法学最独特的贡献——它不仅分类，还做二维交叉分析。当前 review 只记录了 2 条泛化关系边，遗漏了这组核心 cross-tab 关系和 PRISMA 流图链路。对 A2a 的影响是：丢失了「分类维度之间如何交互」的关键模式先验。

4. **统计分母/条件的结构化映射缺失**：例如原文发现「50% proposals 无 limitation」依赖于 L-NS 类——但 L-NS 作为叶子取值没有出现在维度树中。A2a 继承这棵树后，无法从树本身理解「这篇论文的分母逻辑」——即哪些统计基于 N=58、哪些基于 N=29 个子集。

5. **Finding 形成路径被平面化**：当前 A.3 的 12 条结论全是关于维度树本身的元结论（「这个叶子定义了…」），而非「原文通过什么路径从 data extraction → clustering → statistical observation → core finding → gap」。A2a 需要后者作为 finding formation 的模式先验，前者只是元信息。

6. **A.2 证据锚点泛定位**：5 条证据的定位覆盖「全文 §3-§8」「正文分类和统计表关联」等，未达到 pattern-field-schema.md §8.2 合同要求的「原文页码、表号、段落号」级。A2a 的精确核验会因缺乏锚点而需要重读全文，降低效率。

7. **可能误导 A2a 的「树状元维度」表述**：将 5 棵独立分类树描述为统一层级树，可能使 A2a 错误地假设它们是 has-a 关系而非 cross-tab 关系。

#### M 级（3 项）

8. **文献-实践对照维度缺少独立节点**：原文的核心差异化特征之一是 literature vs practice 双轨，当前维度树未将其作为独立维度。不阻塞 A2a 但削弱了完整性。

9. **Roadmap/vision 声明未显式标记**：§8 的 AI/LLM forward-looking 声明是 boundary anchor，应在 A.3 中显式标记 `do_not_use`（statistical）。

10. **「五类/六类 limitation」不一致待复核**：review.md 已标注但未给出明确 A.4 检查指令。

### 6.3 最终建议

**NEEDS FIX**（需要修复后重新审计）。

理由：2 个 C 级问题——原文 schema 被元维度消灭和取值空间不可执行——会直接破坏 A2a 的维度模式演化起点。这不是措辞问题，而是维度树结构选择问题。修复方向不是打补丁，而是将当前的单树结构改为「元维度投影树（A1-M0--M6）+ 专属 schema 树」的双树结构，并补全 §5 清单中的 5 个 I 级和 3 个 M 级项。

具体修复优先级：
1. **P0**（阻塞 A2a）：建立专属 schema 树，将 5 棵分类树 + 质量量表 + 纳排标准 + PRISMA + 效度分类 + 文献-实践对照作为正式节点，并补全每棵树的完整取值枚举、统计分母和缺失值语义。
2. **P1**（影响 A2a 质量）：补全 Goal × Limitation 和 Metric × User 的关系边；升级 A.2 证据锚点精确度。
3. **P2**（提升可用性）：标记 roadmap/vision 声明；复核 limitation「五类/六类」；文献-实践对照独立节点。

---

*审计生成时间：2026-06-29。reviewer 身份：deepseek。不修改仓库文件，不 push，不 gh comment。此报告仅供 PR #135 审核流程使用。*
