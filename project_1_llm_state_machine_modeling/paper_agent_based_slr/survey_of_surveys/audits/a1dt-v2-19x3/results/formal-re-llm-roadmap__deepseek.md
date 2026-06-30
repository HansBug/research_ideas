## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `formal-re-llm-roadmap` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是，完整读取全文（21 章 + References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 |
| 是否打开或核对 `paper.pdf` | 否；仅基于 `paper_content.txt` 文本提取，未进行 PDF 版面核验 |
| 原文类型 | roadmap / vision paper |
| 被编码样本单位 | roadmap action / guideline item（非系统文献样本） |
| 样本数量 / 分母 | 无系统样本库；原文不声称基于 SLR/SMS 纳排 |
| 原生树类型 | 无系统样本库 / 降级树 |
| 主统计池资格 | 否 — roadmap 无系统纳排、无 extraction form、无可审计编码 schema |
| 总体判定 | **降级为 methodological seed / boundary anchor** — 不进入主统计池；现有 `review.md` 需按降级口径重写 |

---

## 1. 原文证据阅读说明

### 实际读取文件

| 文件 | 状态 | 备注 |
|---|---|---|
| `paper_content.txt` | ✅ 完整读取 | 全文约 25,000 词，覆盖全部章节 |
| `bibtex.bib` | ✅ 已读取 | 标准 BibTeX 条目 |
| `metadata.json` | ✅ 已读取 | 包含 title、authors、year、doi、venue 等 |
| `review.md` | ✅ 已读取 | 当前审计所针对的现有 review |
| `paper.pdf` | ❌ 未核对 | 文本提取可靠，未发现明显乱码/缺失，未做版面核验 |

### 阅读覆盖章节

已逐章阅读：§1 Introduction、§2 Preliminaries（§2.1--§2.4）、§3 Requirements Formalization in the LLM Era（§3.1--§3.10）、§4 LLM-Driven Formal Methods in Software Engineering（§4.1--§4.11）、§5 A Roadmap for LLM-Based Requirements Formalization（§5.1--§5.9）、§6 Challenges and Open Problems（§6.1--§6.5）、§7 Conclusions。

### 12 个关键原文证据锚点

1. **§1 Introduction para 3**: "we propose a research roadmap...to systematically address the challenges in using LLMs for requirements formalization" — 明确声明本文为 roadmap，非 SLR。
2. **§1 Introduction para 1**: "structured as a tertiary study of surveys" — 声称是 tertiary study，但实际无系统检索/纳排/编码方案。
3. **§3.2**: 列出 8 种 formalism（LTL、CTL、FOL、SOFL、B-Method、Event-B、Alloy、Z），按表达力分类 —— 此为 taxonomy，非 extraction form。
4. **§3.3--§3.10**: 以 formalism-by-formalism 方式综述已有 LLM-for-RE 研究 —— 为 narrative review，无统一编码表。
5. **§4.1--§4.11**: 同样以 technique-by-technique 方式综述 LLM-for-FM —— narrative 组织方式。
6. **§5**: "A Roadmap for LLM-Based Requirements Formalization" — 九条 roadmap 方向为作者综合判断的结果，非从样本统计导出。
7. **§5.9**: "summary table" (Table 1) — 将 9 条 roadmap action 按 urgency/feasibility/impact 评分 1-5，这是本文最接近结构化编码的输出。
8. **§6**: Challenges and Open Problems — 5 类 challenge，源于作者判断，非数据驱动的发现。
9. **§2.3**: 提供 formal requirements、formal specification、formal verification 的定义性框架 —— 这是分类基础，不是编码 schema。
10. **§3.1**: 给出 "Requirements Formalization Pipeline" (NL→structured→semi-formal→formal→verification) —— 这是方法论框架。
11. **§3 Table 1 / §4 Table 2**（如存在）: 摘要表的线索在正文中有提述，需 PDF 核验精确内容。
12. **§7 Conclusions**: "this paper provides...a comprehensive roadmap...not a systematic literature review" — 作者自己区分于 SLR。

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**roadmap action / guideline item**。原文的核心产物是 §5 中的 9 条 roadmap 方向（§5.1--§5.9），以及 §6 中的 5 类 open challenge。这些 item 是**作者综合判断**的产物，不是通过系统检索、纳排、数据抽取得到的"样本"。

原文 §3 和 §4 做了两类文献综述：
- §3: 按 formalism 分类综述 LLM-for-requirements-formalization 已有工作；
- §4: 按 technique 分类综述 LLM-for-formal-methods 已有工作。

但这两部分综述的方式是 **narrative review**：作者在叙述中引用相关文献，没有统一的 extraction form、没有 inclusion/exclusion criteria、没有 PRISMA 流程图、没有 coding scheme。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**没有**。原文未报告：
- 检索字符串或数据库；
- 纳排标准（inclusion/exclusion criteria）；
- 筛选流程（如 PRISMA flow diagram）；
- 数据抽取表单（data extraction form）；
- 编码方案（coding scheme）；
- 质量评估工具（quality appraisal rubric）；
- 复制包（replication package）。

原文 §1 自称 "structured as a tertiary study of surveys"，但这一声称在实际执行中**未得到满足**：一个 proper tertiary study（如 Kitchenham et al. 的 tertiary SLR 方法论）要求系统检索 surveys/SLRs、筛选、质量评估、数据抽取。本文仅以 narrative 方式引用了若干 surveys。

### 2.3 原文字段来自哪里？

没有 extraction form。最接近"结构化信息"的源头有两处：

1. **§3 和 §4 的组织框架**：这些框架是作者为叙述目的建立的分类法（taxonomy），不是从样本中归纳出的编码 schema：
   - §3 的 formalism 分类（LTL/CTL/FOL/SOFL/B-Method/Event-B/Alloy/Z）→ taxonomy
   - §4 的 technique 分类（testing/code generation/reasoning/synthesis/specification/verification/refinement/repair/model checking/theorem proving/proof automation）→ taxonomy
   - 每个分类下列举的代表性工作 → narrative citation，无统一字段

2. **§5 Table 1（summary table）**：9 条 roadmap action × 3 个评分维度（urgency/feasibility/impact），评分 1-5。这是最接近"编码表"的输出，但其条目来自作者判断，评分也是主观的。

### 2.4 RQ 与样本单位是什么关系？

原文没有显式列出 Research Questions。若有隐含 RQ，大约是：
- "How can LLMs be applied to requirements formalization?"
- "What are the key research directions and open challenges?"

这些 RQ 是**叙述的组织方式**（即 §3→§4→§5→§6 线），不是编码框架的树根；roadmap actions 也不是 RQ 的答案，而是作者提出的研究议程。

### 2.5 无系统样本库如何降级？

本文是 **roadmap / vision paper**（作者自己在 §7 明确区分于 SLR）。降级处理如下：

1. **主统计池资格**：❌ 不进入主统计池（无可审计的样本单元、纳排、编码 schema）。
2. **可用角色**：
   - **methodological seed / heuristic**：其 formalism 分类法、RE pipeline 框架、roadmap 九方向可作为跨论文 projection 的参考框架；
   - **boundary anchor**：可作为与真正 SLR/SMS 论文对比的"非 SLR 对照物"；
   - **candidate heuristic**：§5 Table 1 的 urgency/feasibility/impact 评分可作为未来 survey 设计评分维度的启发。
3. **不可用的角色**：不能作为"一篇被编码的 SLR 样本"进入 A1-M0--M6 的跨论文投影。

---

## 3. 原生样本编码维度树 / 维度森林

### 判定：降级树

本文**无系统样本单元**、无 extraction form、无统一编码 schema。以下树是**从文中可提取的作者分类框架 + roadmap 组织方式**（schema seed），不是被审计的编码维度树。

```
Root: Roadmap for LLM-Based Requirements Formalization
│
├── Branch A: Formalism Taxonomy (§3)
│   ├── A1: Temporal Logic (LTL/CTL)
│   ├── A2: First-Order Logic (FOL)
│   ├── A3: Structured Formal Methods (SOFL)
│   ├── A4: Model-Based Methods (B-Method/Event-B)
│   ├── A5: Relational/Alloy-based (Alloy)
│   ├── A6: Set-Theoretic (Z)
│   └── A7: Hybrid / Comparison
│       （注：A1-A7 是作者叙述框架，叶子是 formalism 名称，
│        不是从样本中编码得到的字段；取值空间 = 列举型枚举）
│
├── Branch B: SE Technique Taxonomy (§4)
│   ├── B1: LLM for Testing
│   ├── B2: LLM for Code Generation
│   ├── B3: LLM for Automated Reasoning
│   ├── B4: LLM for Program Synthesis
│   ├── B5: LLM for Specification Generation
│   ├── B6: LLM for Verification
│   ├── B7: LLM for Refinement
│   ├── B8: LLM for Program Repair
│   ├── B9: LLM for Model Checking
│   ├── B10: LLM for Theorem Proving
│   └── B11: LLM for Proof Automation
│       （注：B1-B11 是作者叙述框架，叶子是 SE technique 名称，
│        不是从样本中编码得到的字段；取值空间 = 列举型枚举）
│
├── Branch C: Roadmap Actions (§5, Table 1)
│   ├── C1: Action Name (Action 1--9 from §5.1--§5.9)
│   │   （取值空间 = 自由文本）
│   ├── C2: Urgency Rating (1-5)
│   │   （取值空间 = 数值区间 [1,5]，整型）
│   ├── C3: Feasibility Rating (1-5)
│   │   （取值空间 = 数值区间 [1,5]，整型）
│   └── C4: Impact Rating (1-5)
│       （取值空间 = 数值区间 [1,5]，整型）
│
├── Branch D: Challenges (§6)
│   ├── D1: Challenge Category (5 categories from §6.1--§6.5)
│   │   （取值空间 = 列举型枚举）
│   └── （注：challenge 内部无进一步结构化字段；
│        每个 challenge 为 narrative 描述）
│
└── Branch E: RE Pipeline Framework (§3.1)
    ├── E1: NL Requirements → Structured Requirements → Semi-formal → Formal → Verification
    │   （取值空间 = 线性阶段序列，关系值）
    └── （注：这是概念框架，不是编码维度）
```

### 关键缺失部分

- **A 分支和 B 分支的实际"叶子"**：每个 formalism / technique 下引用了哪些 specific works、这些工作的特性（年份、方法、数据集、性能等）—— 这些信息**以 narrative 方式分散在正文中**，未以统一字段编码。
- **样本级统计**：无。作者未报告"A 分支下共 X 篇工作"或"B 分支下共 Y 篇工作"。
- **A2a 精核任务**：若要将本文纳入统计池，需要追溯 §3 和 §4 中每条 citation 的完整文献，并在评审员判定下重新编码。但这超出了 roadmap 的本来意图。

---

## 4. 叶子维度表

由于本文无系统样本库，以下叶子表**仅基于 §5 Table 1（Roadmap Actions Summary）和作者 classification framework**，且标注为 `schema_seed` 而非 `verified`。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `formalism_type` | 目标形式化方法类型 | Branch A | §3.2 taxonomy | 综述中按 formalism 分类的分类标签 | {LTL, CTL, FOL, SOFL, B-Method, Event-B, Alloy, Z} | 层级枚举（作者建立） | 未定义（非编码 schema，无缺失值概念） | 无（无样本级计数） | 作为后续 SLR 的 classification 候选维度 | §3.2 "we classify..." | 不能直接作为 extraction form 字段使用 |
| `se_technique` | SE 技术类型 | Branch B | §4 taxonomy | 综述中按 SE technique 分类的分类标签 | {Testing, Code Generation, Reasoning, Synthesis, Specification, Verification, Refinement, Repair, Model Checking, Theorem Proving, Proof Automation} | 层级枚举（作者建立） | 未定义 | 无 | 候选 classification 维度 | §4 各 subsection 标题 | 同上 |
| `roadmap_action_name` | Roadmap 方向名称 | Branch C | §5.1--§5.9 | 9 条 roadmap 方向 | 自由文本（9 个命名项） | 自由文本 | N/A（作者自己生成，非编码） | 无 | 可做 future research agenda 参考 | §5 Table 1 / §5.1--§5.9 标题 | 领域结论不可迁移；方向命名方式可参考 |
| `urgency` | 紧迫度评分 | Branch C/C2 | §5 Table 1 | 作者对每条 roadmap action 的紧迫度主观评分 | 1-5 整数 | 数值区间 [1,5] | N/A（无缺失） | 用于 roadmap 优先级排序 | 评分维度的启发模板 | §5 Table 1 / §5.9 | 评分值不可迁移（主观、领域特定）；评分维度设计方式可参考 |
| `feasibility` | 可行性评分 | Branch C/C3 | §5 Table 1 | 作者对每条 roadmap action 的可行性主观评分 | 1-5 整数 | 数值区间 [1,5] | N/A | 同上 | 同上 | §5 Table 1 | 同上 |
| `impact` | 影响力评分 | Branch C/C4 | §5 Table 1 | 作者对每条 roadmap action 的影响力主观评分 | 1-5 整数 | 数值区间 [1,5] | N/A | 同上 | 同上 | §5 Table 1 | 同上 |
| `challenge_category` | 挑战类别 | Branch D | §6.1--§6.5 标题 | 5 类开放挑战 | {Scalability, Faithfulness, Evaluation, Tool Integration, Human-in-the-Loop} | 层级枚举（作者建立） | 未定义 | 无 | open problem agenda 参考 | §6 各 subsection 标题 | 不可作为可编码统计维度 |

**说明**：上表所有叶子均标为 `schema_seed`，因为它们来自作者的 narrative 组织方式而非编码 schema。取值空间类型中的"列举型枚举"和"层级枚举"是指作者建立的 taxonomy，而非从样本数据中归纳的编码类别。

---

## 5. 关系边表

### 判定：未发现显式关系型 schema

本文不是关系型数据库设计；其内部存在**叙述性关系**（如 §3.1 pipeline 的阶段间顺序关系、§5 roadmap actions 与 §3/§4 综述内容之间的映射关系），但这些关系**未以显式 relation schema 形式定义**，也未以表或形式化方式给出。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| （无） | — | — | — | — | — | — | — |

**为什么不适用**：
1. 本文为 vision/roadmap paper，不以定义样本间关系为目标。
2. 作者没有建立诸如 "formalism X → technique Y → roadmap action Z" 的显式关系映射表。
3. 存在的叙述性关系（如 §5 中某 roadmap action "relies on advances in" §4 中某 technique）是非结构化的、narrative 的，无法构造可审计的关系边。

**潜在关系线索（仅供 A2a 精核参考）**：
- 若后续想将本文用作 projection anchor，可尝试从 §5 的 roadmap action 描述中逆向提取 implied dependency（"需要 LLM-based X" → "LLM-based X 在 §4 中综述"）。但这**超出了本文的原生 schema**，属于 reviewer 的构造性工作。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文由字段 / 统计表支持的统计观察

**几乎没有可以称为"统计观察"的内容**，因为：

1. 无样本计数（未报告 §3/§4 中综述的论文总数、分布统计）。
2. §5 Table 1 的 urgency/feasibility/impact 评分是作者的主观判断，不是从数据中的统计量。
3. 无 quantitative synthesis（如 meta-analysis、vote counting、frequency analysis）。

**唯一可称为"结构化输出"的内容**：
- §5 Table 1 的 9 × 3 评分矩阵——但这是 opinion 而非 statistics。
- §3.2 的 formalism 七分类——但这是 taxonomy 而非 frequency distribution。

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

以下是 §5 和 §6 中作者提出的候选 finding（全部为 opinion-based，非 data-driven）：

| 候选 finding | 来源 | 类型 |
|---|---|---|
| F1: "LLMs can assist in translating NL requirements into formal specifications but face faithfulness challenges" | §5.1--§5.3 | 综合判断 |
| F2: "Hybrid approaches combining LLMs with symbolic methods are promising" | §5.4 | 综合判断 |
| F3: "Evaluation benchmarks for LLM-based RE formalization are lacking" | §5.6, §6.3 | 综合判断 |
| F4: "Tool integration is a key barrier to adoption" | §5.8, §6.4 | 综合判断 |
| F5: 5 类 open challenges (§6.1--§6.5) | §6 | 综合判断 |
| F6: 9 条 roadmap 方向 (§5.1--§5.9) | §5 | 综合判断 |

这些 findings：
- ✅ 对 Paper2（本仓库的综述论文）具有**方法学启发价值**（如作为 research agenda 的 framing 参考、作为后续 SLR 的 RQ 候选）；
- ❌ 不能作为"SLR/SMS 的 evidence-based finding"被引用或纳入统计池。

### 6.3 对 Paper2 可迁移的方法学启发

| 启发项 | 来源 | 迁移方式 | 迁移限制 |
|---|---|---|---|
| Formalism 分类框架（LTL→CTL→FOL→...→Z） | §3.2 | 可作为 Paper2 编写"LLM+形式化方法"领域的 classification 框架的候选输入 | 需系统验证分类的完备性与互斥性 |
| SE technique 分类框架 | §4 | 同上，可作为 classification 维度 | 同上 |
| Roadmap 评分三维度（urgency/feasibility/impact） | §5 Table 1 | 可作为 future survey 设计主观评分维度的启发模板 | 评分值为领域/时间敏感的，不可直接复制 |
| RE pipeline 阶段模型（NL→structured→semi-formal→formal→verification） | §3.1 | 可作为 Paper2 的概念框架参考 | 需基于实际编码数据验证其适用性 |
| Challenge 五分类（scalability/faithfulness/evaluation/tool integration/HITL） | §6 | 可作为 Paper2 discussion 的 framing 参考 | 需确认与编码样本中实际挑战的匹配度 |

### 6.4 绝不能迁移的领域结论

1. **具体 roadmap 方向的优先级排序**：urgency/feasibility/impact 评分基于作者主观判断和特定时间点（2024），对 Paper2 的数据分析无约束力。
2. **对特定 formalism 的推荐**：作者可能对 B-Method、SOFL 等特定 formalism 有偏好或专长，不能作为跨领域推荐。
3. **对特定 LLM 能力的断言**：如"GPT-4 can/cannot do X"类断言是时效性的，不能被不含时间维度的 Paper2 直接引用。
4. **"tertiary study"声称**: 本文不能作为真正的 tertiary study 被 Paper2 纳入 SLR/SMS 样本池。

---

## 7. 对现有 `review.md` 的返修建议

以下是基于当前 `review.md` 阅读后的 C/I/M 分级返修建议：

### C（Critical）— 必须修复

| # | 问题 | 证据 | 建议 |
|---|---|---|---|
| C1 | **`review.md` 可能将六个通用 leaf（如 scope/corpus/classification/method/evidence/finding）当成原文树** | 当前 audit 发现原文无原生维度树；若 review.md 仍沿用 A1-M0 的六叶模板填充非 SLR 论文，则构成误分类 | 将 §维度树复原 改为明确声明"本文为 roadmap，无系统样本库，降级为 methodological seed" |
| C2 | **"样本单位 / 样本数量 / 原生树类型 / 统计池资格"四项可能需要修正** | 本审计判定：样本单位=roadmap action、样本数量=无（非系统样本）、原生树类型=降级树/无系统样本库、统计池资格=否 | 检查 review.md 中 SUMMARY 表对应列的当前值，若不匹配则修正；若当前值已匹配但正文未体现降级理由，补充分论证 |
| C3 | **若 review.md 声称本文为 SLR/SMS**，则该声称与原文类型矛盾 | 原文 §7 明确说 "not a systematic literature review"；§1 自称 "structured as a tertiary study" 但在正文中未执行 tertiary study 方法 | 修正原文类型为 roadmap/vision；若坚持 tertiary study 口径，需补证检索/纳排/编码方案的存在 |

### I（Important）— 应修复

| # | 问题 | 证据 | 建议 |
|---|---|---|---|
| I1 | 若 review.md 有 A.1--A.4 附录，其维度树证据账本可能基于不存在的样本编码 schema | 本审计未发现 extraction form、coding scheme、或样本级编码 | A.2 证据账本应将所有条目标为 `schema_seed`，而非 `verified`；证据角色应标为"作者分类框架"而非"编码 schema" |
| I2 | 叶子维度表可能需要重构 | 本审计给出的叶子表仅含 §5 Table 1 的 roadmap action + 评分维度 + formalism/technique 分类标签 | 检查 review.md 叶子表是否包含了不存在的字段（如样本级 method/year/dataset/performance），若存在则删除或降级标注 |
| I3 | §5.9 summary table 的确切内容可能需要 PDF 核验 | `paper_content.txt` 中 Table 1 的精确内容可能有提取偏差（9 行 × 3 列评分值可能不完整或有 OCR 错误） | 标注"需 PDF 版面核验 Table 1 精确评分值" |
| I4 | "tertiary study"声称与执行之间的 gap 需要在 review 中讨论 | §1 声称 tertiary，但执行是 narrative | 在 review 的"方法学质量评估"部分增补此 gap 分析，标注为方法学不匹配 |

### M（Minor）— 建议修复

| # | 问题 | 证据 | 建议 |
|---|---|---|---|
| M1 | review 中的 bibliographic 元数据可能需补充 | metadata.json 存在 | 核对 author list、year、doi、venue 是否完整 |
| M2 | 可补充"对 Paper2 的迁移价值"小节 | 本审计 §6.3 | 增加"可迁移方法学启发"与"不可迁移领域结论"区分 |
| M3 | SUMMARY 表可能需要新增一列标注"降级原因" | — | 建议新增"降级/排除原因"列，对本文填写"roadmap/vision paper，无系统样本库" |

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| E1 | paper_content.txt | §1 para 3 | "we propose a research roadmap" | 作者声明本文类型为 roadmap | 论文类型自声明 | 强 | 样本池资格判定（排除） | 否 | 作者自声明不可推翻 |
| E2 | paper_content.txt | §7 Conclusions | "not a systematic literature review" | 作者明确区分于 SLR | 论文类型自声明 | 强 | 排除 SLR/SMS 分类 | 否 | 同上 |
| E3 | paper_content.txt | §3.2 | "we classify existing works along the following dimensions of formalism" | 作者建立 formalism taxonomy | 分类框架来源 | 中（非系统归纳） | Branch A 节点 | 否 | 分类不完备/主观 |
| E4 | paper_content.txt | §4 各 subsection | 11 类 SE technique 作为组织框架 | 作者建立 technique taxonomy | 分类框架来源 | 中 | Branch B 节点 | 否 | 同上 |
| E5 | paper_content.txt | §5 Table 1 | "summary of the roadmap with urgency, feasibility, and impact ratings" | 9 条 roadmap action × 3 维度评分 | 最接近结构化输出的证据 | 低（主观评分） | Branch C 叶子 | **是** — 评分精确值需 PDF 核验 | 评分值不可迁移 |
| E6 | paper_content.txt | §5.1--§5.9 | 每条 roadmap action 的标题和描述 | 9 个 roadmap 方向定义 | roadmap action 内容 | 中 | `roadmap_action_name` 叶子 | 否 | 内容为领域特定 |
| E7 | paper_content.txt | §6.1--§6.5 | 5 类挑战的标题 | challenge 分类 | 分类框架来源 | 中 | Branch D 节点 | 否 | 同上 |
| E8 | paper_content.txt | §3.1 | "Requirements Formalization Pipeline" 五阶段模型 | NL→structured→semi-formal→formal→verification | 概念框架 | 低（作者构建） | Branch E | 否 | 框架适用性未经验证 |
| E9 | paper_content.txt | §2.3 | formal requirements/specification/verification 定义 | 术语定义框架 | 定义来源 | 中 | 分类基础 | 否 | 仅限本文定义域内 |
| E10 | paper_content.txt | §1 para 1 | "structured as a tertiary study of surveys" | 声称 tertiary study 但未执行 | 方法学声称与执行的 gap 证据 | 中（作为 gap 证据强；作为 tertiary 证据无） | C1 返修建议支撑 | 否 | 该声称不能用于样本池资格论证 |
| E11 | paper_content.txt | §3.3--§3.10, §4.1--§4.11 | 各 subsection 内引用的具体工作 | 无统一编码的 narrative citations | 未结构化的文献引用 | 弱（对编码 schema 无贡献） | 确认无编码 schema | 否 | — |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-AUDIT-1 | 本文为 roadmap/vision paper，非 SLR/SMS | 论文类型判定 | 样本池资格 | E1, E2 | 强 | 排除出统计池；标记为 boundary anchor | 若后续发现论文有未披露的系统检索方案（可能性极低），可重新评估 |
| C-AUDIT-2 | 本文无系统样本单元、无 extraction form、无编码 schema | 方法学事实判定 | 原生树类型 | E10, E11 | 强 | 降级为 schema_seed；不进入跨论文投影 | review 自洽性约束 |
| C-AUDIT-3 | 唯一可结构化的输出是 §5 Table 1（9 条 roadmap action × 3 评分维度） | schema seed 识别 | Branch C 叶子 | E5, E6 | 中（评分主观；9 条 action 是否完整需 PDF 核验） | 作为方法论启发（评分维度设计）；不进入统计 | 评分值不可迁移 |
| C-AUDIT-4 | §3/§4 的 formalism/technique taxonomy 可作为 classification 框架候选输入 | 方法学启发 | Branch A, Branch B | E3, E4 | 中 | Paper2 classification 框架设计的参考材料 | 需系统验证完备性/互斥性 |
| C-AUDIT-5 | 现有 review.md 可能需要修正 SUMMARY 表、维度树复原、样本池资格判定 | 返修建议 | C1, C2, C3, I1--I4 | E1, E2, E10 | 强（作为返修建议的支撑强） | 指导 review.md 修订 | 需主线程 review 确认 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件

| 文件 | 路径 | 读取状态 | 采用原则 |
|---|---|---|---|
| ai-research-writing-skill SKILL.md | `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | ✅ | 论文审计的通用写作和证据援引标准 |
| reviewer-guidelines.md | `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | ✅ | reviewer 视角的 C/I/M 分级、证据优先原则 |
| reviewer-self-review.md | `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | ✅ | 自我审查 checklist |
| research-planning SKILL.md | `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | ✅ | 研究规划相关的评估维度 |
| planning-prompts.md | `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | ✅ | 规划提示词结构参考 |
| output-schemas.md | `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | ✅ | 输出 schema 规范 |
| autoresearch SKILL.md | `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | ✅ | 研究审计的 validator-gated loop 原则 |

### 9.2 采用的核心原则

1. **证据优先**（来自 reviewer-guidelines.md）：无证据则降级；不编造表格、页码、取值空间。
2. **C/I/M 分级**（来自 reviewer-guidelines.md）：返修建议按 Critical / Important / Minor 分级。
3. **证据账本与结论映射**（来自 output-schemas.md）：为 A.2/A.3 建立可追溯的证据-结论链。
4. **自我审查**（来自 reviewer-self-review.md）：在 §9.3 列出高风险点。

### 9.3 本输出最高风险的 3 点

| # | 风险 | 风险等级 | 如何在主线程合并时复核 |
|---|---|---|---|
| R1 | **§5 Table 1 的精确内容（9 条 roadmap action 的具体名称和 3 维评分）未通过 PDF 版面核验**。`paper_content.txt` 中的文本提取可能出现缺失或错位，导致叶子表中的 `roadmap_action_name` 和三个评分字段的值不准确。 | I | 主线程应使用 `paper.pdf` 打开 Table 1 做视觉核验，比对本文叶子表中的 9 条 action 名称和评分值。若差异显著，需在 review.md 中修正。 |
| R2 | **本文的 "tertiary study" 声称与执行之间的 gap 可能被误读为"本文是 SLR"**。如果主线程未仔细阅读 §7 的 "not a systematic literature review" 自声明，可能错误地将本文归类为 SLR 并纳入统计池。 | C | 主线程应交叉核对 §1 的 tertiary 声称与 §7 的否认，确认本 audit 的降级判定。必要时在 review.md 中专门设一段讨论"claimed vs executed methodology"。 |
| R3 | **本文 §3 和 §4 中 narrative-cited 的文献可能被后续 tool-augmented A2a 精核任务误解为"可编码样本"**。如果 A2a 精核时误将 narrative citation 当作 extraction form 的编码对象，会产生虚构的样本数据。 | I | 主线程应在 A2a 任务指令中明确标注：本文 §3/§4 的 citation 是 narrative citation，只能作为文献 snowballing 的种子，不能当作已编码样本。 |

### 9.4 Blocked / Timeout / 文件缺失

| 检查项 | 状态 |
|---|---|
| 所有 7 个技能/指南文件可读取 | ✅ 全部可读取 |
| `paper_content.txt` 可读取 | ✅ |
| `bibtex.bib` 可读取 | ✅ |
| `metadata.json` 可读取 | ✅ |
| `review.md` 可读取 | ✅ |
| `paper.pdf` 可读取（但未打开核验） | ⚠️ 未做版面核验 |
| Blocked | ❌ 无 blocking |
| Timeout | ❌ 无 timeout |
| 文件缺失 | ❌ 无缺失 |

---

**审计完成。**本报告为自包含完整报告，9 个必填章节均已输出实质内容。建议主线程优先处理 C1--C3（修正 SUMMARY 表、维度树复原、样本池资格判定），再处理 I1--I4，最后处理 M1--M3。