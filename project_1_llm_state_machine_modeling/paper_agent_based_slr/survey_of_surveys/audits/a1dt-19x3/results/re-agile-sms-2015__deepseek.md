# re-agile-sms-2015 · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。
  - 读取路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - 关联参考：`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是。
  - 读取路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - 关联参考：`references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是。
  - 读取路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是。
  - 覆盖范围：全部 954 行，9 页（Page 1--9），从标题 / 摘要 / RQ / Background / Methodology / Results / Benefits (B1-B6) / Problems (P1-P6) / Solutions / Discussion / Limitations / Conclusion / References 全覆盖。
- **是否核对 `paper.pdf`**：是。
  - 通过 `pdfinfo` 确认 9 页 PDF，通过 `pdftotext -layout` 按页抽取逐页核对了 Table I（venue 分布）、Table II（agile method 分布）、Table III（article type 分布）、Table IV（benefits）、Table V（problems）以及 Discussion 节标题结构（Article metadata/context/type → Definition → Benefits/Problems/Solutions）。
  - 未做视觉级版面比对；本次核对定为"全文文本 + layout PDF 核对"，确认表格存在、字段命名、分类项和编号与 `paper_content.txt` 一致。
- **是否读取文库级规则**：是。
  - `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`
  - `patterns/pattern-field-schema.md`
  - `story/paper_story.md`

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文声明三个 RQ（Page 1）：

1. **RQ1**：What has been researched regarding requirements engineering in an agile context?
2. **RQ2**：What are the reported key benefits of agile requirements engineering?
3. **RQ3**：What are the reported problems and corresponding solutions related to agile requirements engineering?

贡献声明：对 28 篇文献进行系统映射研究（systematic mapping study），梳理敏捷需求工程的研究现状、收益、问题和解决方案，识别研究空白。

### 2.2 原文方法流程

- **检索**：Elsevier Scopus abstracts 数据库，2014 年 9 月执行，检索式为 `TITLE-ABS-KEY(("requirements analysis" OR "requirements engineering") AND ("agile" OR "scrum"))`。
- **纳排**：241 → 去除非期刊/会议 46 条 → 非英语 8 条 → 标题摘要筛选 187 → 含全文阅读筛选，最终 28 篇。
- **数据抽取**：**原文显式声明了四类抽取主题区域**（Page 3 Methods 节，PDF 原文）：
  1. Definition of RE in the agile context
  2. Benefits identified in agile RE
  3. Problems identified in agile RE
  4. Solutions proposed for the aforementioned problems
  - 同时抽取 article metadata、context、methods。
- **编码/分类 schema**：
  - RQ1 回答：通过 Table I（venue 分布）、Table II（agile method 类型：Unspecified Agile / Scrum / FDD）、Table III（article type：Multiple case study / Single case study / Experience report / Tool evaluation / Method evaluation / Method proposal / Position paper），以及对 agile RE 的定义性概述。
  - RQ2 回答：通过 Table IV 明确给出 6 个 benefit 类别（B1--B6），每类有定义文本和文章引用列表。
  - RQ3 回答：通过 Table V 明确给出 6 个 problem theme 类别（P1--P6），每类有定义文本、文章引用列表和对应的 solution 讨论；其中 P3（prioritization difficulties）、P4（growing technical debt）、P6（imprecise effort estimates）原文明确写"**No solutions to P3/P4/P6 were proposed in the articles**"——这是一个显式的 absence evidence。
  - Table VI：文章按 benefit / problem 的交叉分布（paper_content 可辨识其存在，但具体格式需人工核对原 PDF 版面）。

### 2.3 原文显式 extraction form / classification schema / taxonomy / coding scheme

原文不含独立的"extraction form 附录"，但其 Methods 节明确了抽取的四类主题区域（见 2.2），且 Results 节产出了以下完整的分类/编码产物：

| 产物 | 内容 | 原文位置 | 是否可统计 |
|---|---|---|---|
| Table I | Venue 分布（conference proceedings / journal articles / magazine articles 及具体 venue 名） | Page 3--4 | 是（N 和百分比明确） |
| Table II | Agile method 类型（Unspecified=20, Scrum=7, FDD=1） | Page 4 | 是 |
| Table III | Article type（7 类：Multiple case study=6, Single case study=5, Experience report=3, Tool evaluation=1, Method evaluation=2, Method proposal=8, Position paper=3） | Page 4 | 是 |
| Table IV | Benefit 类别（6 类 B1--B6），每类附文章列表 | Page 5 | 是（每类的文章引用数可计数） |
| Table V | Problem theme（6 类 P1--P6），每类附文章列表 | Page 5--6 | 是（每类的文章引用数可计数） |
| 4-subject-area schema | Definition / Benefits / Problems / Solutions | Page 3 Methods 节 | 是（原文的抽取框架） |
| Discussion §A 节 | 对 article metadata/context/type 的进一步分析（venue 碎片化、agile method 未指定普遍性、article type 分布） | Page 6--7 | 部分可统计 |

### 2.4 原文如何从字段/统计观察形成 conclusion / finding / gap / recommendation

原文形成 finding 的路径清晰：

1. **RQ1 → Descriptive finding**："There is no primary venue for articles on RE in ASD"（Table I 分布）+ "Most articles have unspecified ASD as the context"（Table II）+ 定义性判断："the definition of agile RE is vague"。
2. **RQ2 → Table IV 6 类 benefit**：每类有定义 + 文章引用，Discussion 中进一步讨论 benefit 的实据 vs 声称。
3. **RQ3 → Table V 6 类 problem theme**：每类有定义 + 文章引用 + solution 讨论，其中 P3/P4/P6 **明确标注无解决方案**，构成 research gap。
4. **Discussion → Gap identification**：识别出 agile RE 定义模糊、缺少主导 publication venue、某些 problem theme 无解决方案、需要更多经验研究。

## 3. 当前 `review.md` 维度树审计

### 3.1 先确认 `review.md` 的设计意图

`review.md` 的"维度树复原"节有两层设计：

- **上层 6 叶"通用接口层"**（scope / corpus / taxonomy / method / evidence / finding）：review 明确声明这是"跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原"。
- **下层 5 个"原文模式候选叶子映射（A1 种子）"**（orig-agile-re-topic / orig-problem / orig-benefit / orig-solution / orig-evidence-gap）：用来"避免把上表六个通用接口误读为原文叶子全集"。

这种双层设计本身是合理的架构选择——用统一接口做跨论文可比性，用候选叶子做原文锚定。但该设计在本文的具体执行上存在以下问题。

### 3.2 审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-re-agile-sms-2015-root]` 正确指向"A Mapping Study on Requirements Engineering in Agile Software Development"，与原文题名、目标和 RQ 一致。 | 通过 |
| 主干分支是否覆盖原文 schema | **未通过** | 主干分支（B1--B5：范围 / 语料 / 分类 / 方法 / 评价）的五分支结构是按跨论文通用接口组织的，**而不是按原文的三 RQ 结构或四类抽取主题区组织的**。原文的"四类抽取主题区"（Definition / Benefits / Problems / Solutions）以及三 RQ 的回答结构没有在主干分支中得到体现。B5 "评价、统计与候选发现"将 evidence 和 finding 合并，而原文明确分开呈现了 Tables I--VI 的证据与 Discussion 中的 finding。 | **I** |
| 叶子维度是否足够具体 | **未通过** | 6 个通用叶子（scope / corpus / taxonomy / method / evidence / finding）的定义足够通用，但对本文而言**过粗**。例如 `[leaf-re-agile-sms-2015-taxonomy]` 的定义"复原原文中的 taxonomy、classification schema、coding scheme"是接口定义，而不是本文实际 taxonomy 的复原——本文有 6 个具体分类表（Tables I--VI），每个有自己的分类轴和取值空间，但在叶子维度中无法区分。 | **I** |
| 取值空间是否可执行 | **未通过** | 6 个通用叶子的取值空间写为"自由文本加 xxx"或"完整枚举/层级枚举/自由文本加理由"，是框架性描述，并未给出本文的实际取值空间。5 个候选叶子的取值空间同样过于泛化（如 orig-problem 写"需求变更、沟通、文档、质量、客户参与、规模化等 problem"），这些词汇并非从 Tables IV/V 精确提取，而是近似描述。**本文 Table IV 中 B1--B6 和 Table V 中 P1--P6 是受控编码，取值空间已封闭**，但 review 未体现。 | **I** |
| 关系边是否缺失 | **部分未通过** | review 缺少以下关键关系：（1）RQ→维度映射（原文的 RQ1/RQ2/RQ3 分别对应哪些 Table 和分类轴）；（2）problem→solution 链接（原文明确 P3/P4/P6 "无 solutions"，这是 absence evidence，应作为关系边记录）；（3）classification table→finding 的统计链路（每张 Table 的分布如何形成 Discussion 中的 gap/conclusion）。 | **I** |
| 统计用途 / 分母是否正确 | **通过**（带保留） | review 正确标注分母 28，所有叶子当前用途为 `schema_seed`，不进入 SUMMARY 定量统计。统计池资格判定为"后续主统计池候选"，当前不予升级——这与 A1-DT 阶段合同一致。但需注意：**原文 Tables I--VI 中每个分类的 N 和百分比是可统计的实际值**，review 未记录这些值，这会导致 A2a 精核时缺少快速比对依据。 | M |
| 候选 finding 路径是否完整 | **未通过** | review 把候选 finding 路径抽象为 `statistical_result` → `candidate_finding` → `researcher_adjudication`，但对本文而言缺失了具体路径：Tables I--VI 统计分布 → Discussion §A--C 的分析 → 识别出的 gap（venue 碎片化、agile method 未指定普遍性、agile RE 定义模糊、P3/P4/P6 无方案）。原文 Discussion 第 6 页还指出了 "the list of publication venues suggests that factors other than an RE focus have been more important" 和 "RE in ASD as a subject has not yet found a comfortable home"——这些都是具体的 finding 锚点。 | **I** |
| A.1--A.4 证据链是否足够 | **部分未通过** | A.1 来源表正确。A.2 证据账本仅有 4 条证据（EV-001 至 EV-004），且全部标记为 `not_verified`。对于一篇有 6 张分类表、明确 extraction form、完整 Results/Discussion 的 SMS 论文而言，4 条证据过少：**每张 Table 应当至少有一条独立证据**，每类 benefit/problem/solution 的编码来源应当可追溯。A.3 结论-证据映射的回链存在但结论数（10 条）与证据数（4 条）的比率偏高。A.4 中 `needs_manual_check` 状态正确。 | **I** |
| 是否存在可能误导 A2a 的强主张 | **未通过** | **`[leaf-re-agile-sms-2015-orig-problem]` 被挂载到 `[dim-re-agile-sms-2015-b2]`（语料收集与纳排）下**——原文的 problem 分类（P1--P6）属于 RQ3 的领域分类/编码，与语料收集没有关系。这会在 A2a 跨论文聚合时把 problem taxonomy 误归入 corpus/search 类统计，产生 schema 污染。同时，`[leaf-re-agile-sms-2015-orig-benefit]` 和 `[leaf-re-agile-sms-2015-orig-solution]` 都挂载在 B3 下，但原文 benefit 属于 RQ2、problem+solution 属于 RQ3，这些领域语义差异被"合并到 B3 主题/对象分类"掩盖了。 | **C** |

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树建议。它保留 6 个通用接口叶子作为跨论文可比性层，但增加**原文模式叶子层**以完整复原本文的 extraction form、classification schema 和 evidence tables。

```text
[dim-re-agile-sms-2015-root] A Mapping Study on RE in Agile Software Development
├── [dim-re-agile-sms-2015-b1] 综述范围与研究问题
│   ├── [leaf-re-agile-sms-2015-scope] 研究范围与单位对象  ← 通用接口
│   └── [leaf-re-agile-sms-2015-orig-rq1-landscape] RQ1：研究景观
│       ├── 取值：agile RE definition landscape
│       └── 证据：[Table I] venue 分布、[Table II] agile method 分布、[Table III] article type 分布
├── [dim-re-agile-sms-2015-b2] 语料收集与纳排
│   └── [leaf-re-agile-sms-2015-corpus] 语料与纳排链条  ← 通用接口
│       ├── 取值：Scopus / 241→187→28 / 含全文筛选 / 2014年9月
│       └── 证据：Methods 节 Page 3
├── [dim-re-agile-sms-2015-b3] 主题 / 对象分类（原文 extraction schema）
│   ├── [leaf-re-agile-sms-2015-taxonomy] 主题与维度分类  ← 通用接口
│   ├── [leaf-re-agile-sms-2015-orig-agile-re-topic] Agile RE 主题  ← 原文 RQ1 候选
│   │   └── 取值空间：agile RE 定义、研究类型、实践分类
│   ├── [leaf-re-agile-sms-2015-orig-benefit] Benefit 类别（B1--B6） ← 原文 RQ2 候选
│   │   └── 取值空间（受控枚举）：B1 降低流程开销 / B2 提升需求理解 / B3 减少过度分配 / B4 变更响应性 / B5 快速交付与验证 / B6 改善客户关系
│   │   └── 证据：[Table IV], Page 5
│   ├── [leaf-re-agile-sms-2015-orig-problem] Problem theme（P1--P6） ← 原文 RQ3 候选
│   │   └── 取值空间（受控枚举）：P1 客户代表问题 / P2 用户故事格式不足 / P3 优先级困难 / P4 技术债务增长 / P5 隐性知识依赖 / P6 工作量估计不精确
│   │   └── 证据：[Table V], Page 5--6
│   └── [leaf-re-agile-sms-2015-orig-solution] Solution proposals ← 原文 RQ3 候选
│       └── 取值空间：P1 解决方案（requirements engineer / domain owner / ethnography / Scrum+goal-oriented RE / mind-mapping / storytest-driven / ATDD）、P2 解决方案（delivery stories / hierarchical requirements model / aspect-oriented / feature-driven / 传统 RE 分析+规范化）、P5 解决方案（additional documentation）
│       └── 关系边：[edge-problem-solution-link] 将 solution 链接到对应 problem；P3/P4/P6 缺少解决方案 → absence evidence
├── [dim-re-agile-sms-2015-b4] 方法 / 技术 / 干预
│   ├── [leaf-re-agile-sms-2015-method] 方法 / 技术 / 干预分类  ← 通用接口
│   └── [leaf-re-agile-sms-2015-orig-study-type] 研究类型分类  ← 原文候选（当前缺失）
│       └── 取值空间（受控枚举）：Multiple case study / Single case study / Experience report / Tool evaluation / Method evaluation / Method proposal / Position paper
│       └── 证据：[Table III], Page 4
└── [dim-re-agile-sms-2015-b5] 评价、统计与候选发现
    ├── [leaf-re-agile-sms-2015-evidence] 评价、证据与复现资产  ← 通用接口
    ├── [leaf-re-agile-sms-2015-finding] 统计观察与候选发现  ← 通用接口
    └── [leaf-re-agile-sms-2015-orig-evidence-gap] 证据缺口与未来工作
        ├── 取值空间：agile RE 定义模糊 / 无主导 venue / P3/P4/P6 无方案 / 缺少经验研究
        └── 证据：Discussion §§A--C, Conclusion
```

**关键差异说明**：

1. **`orig-problem` 从 B2（语料收集）移至 B3（主题分类）**：原文 problem 分类是 RQ3 的领域编码，不是语料纳排的一部分。
2. **新增 `orig-study-type` 叶子**：原文 Table III 是独立的 7 类研究类型分类轴，当前 review 完全缺失。
3. **`orig-benefit` 和 `orig-solution` 的取值空间收窄为受控枚举**：原文 Table IV 和 Table V 已封闭取值——B1--B6 是固定 6 类，P1--P6 是固定 6 类。
4. **新增 `edge-problem-solution-link` 关系边**：P3/P4/P6 的"无解决方案"是 absence evidence，应在证据账本中显式记录。
5. **6 个通用接口叶子保留**：它们服务于跨论文可比性（符合 pattern-field-schema 合同 §8.2），但原文模式叶子才是本文的真实 schema 复原。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| `orig-problem` 挂载到错误分支 | 维度树结构表 和 原文模式候选叶子映射表 | 将 `[leaf-re-agile-sms-2015-orig-problem]` 的父节点从 `[dim-re-agile-sms-2015-b2]` 改为 `[dim-re-agile-sms-2015-b3]`；若需要独立区分 RQ3 域，可新建 `[dim-re-agile-sms-2015-b3-rq3]` 分支。 | paper_content.txt Page 5--6；Table V；原文 RQ3 语义 | **C** |
| 缺失原文 Table III 研究类型分类轴 | 原文模式候选叶子映射表 | 新增 `[leaf-re-agile-sms-2015-orig-study-type]`，取值空间为原文 Table III 的 7 类受控枚举（Multiple case study / Single case study / Experience report / Tool evaluation / Method evaluation / Method proposal / Position paper）。N 值见 PDF Page 4。 | paper_content.txt Page 4 Table III | **I** |
| 缺失原文 extraction 四类主题区 | 维度树结构 或 RQ→主干映射表 | 在 RQ→主干映射表中补充原文 Methods 节声明的四类抽取主题区（Definition / Benefits / Problems / Solutions），并映射到对应 leaf。 | PDF Page 3 Methods 节："extracted results were categorized under the following four subject areas: Definition of RE in the agile context, benefits identified in agile RE, problems identified in agile RE and solutions proposed for the aforementioned problems" | **I** |
| 缺失 problem→solution 关系边 | 关系边表（当前缺失）或 A.2 证据账本 | 新增 `[edge-re-agile-sms-2015-problem-solution-link]`，明确 P1/P2/P5 有解决方案、P3/P4/P6 无解决方案（absence evidence）。 | paper_content.txt Page 5--6；Table V；原文明确写："No solutions to P3 were proposed" / "No solutions to P4 were proposed" / "No solutions to P6 were proposed" | **I** |
| 缺失原文 Tables I/II 的 venue/method 分布维度 | 原文模式候选叶子映射表 | 补充 venue 分布（Table I：15 conference proceedings / 8 journal articles / 5 magazine articles）和 agile method 分布（Table II：Unspecified=20, Scrum=7, FDD=1）作为原文候选叶子或其子类。 | paper_content.txt Page 3--4；PDF Page 3 Table I、Page 4 Table II | **I** |
| 原文候选叶子取值空间过于泛化 | 原文模式候选叶子映射表 取值空间列 | 将 orig-benefit 取值空间从自由文本改为受控枚举 B1--B6（附 N 值和原文 Table IV 页码）；将 orig-problem 改为受控枚举 P1--P6（附 N 值和原文 Table V 页码）。orig-solution 应按 P1/P2/P5 分别列出具体方案类型。 | paper_content.txt Page 4--6 Tables IV/V | **I** |
| 证据账本条目过少 | A.2 维度树证据账本 | 从当前 4 条扩展至至少 8 条：每条 Table（I--VI）至少一条独立证据，四类抽取主题区至少一条独立证据。当前 EV-002 承担了 taxonomy+method+所有叶子维度的支撑，信息密度过高。 | pattern-field-schema §8.2 证据链合同要求"每张 Table 应至少有独立证据引用" | **I** |
| 候选 finding 路径缺少具体锚点 | A.3 结论-证据映射 或 统计与候选发现链路表 | 至少补充 3 条原文实际 finding 的候选链路：① Tables I/II 分布 → "RE in ASD 无主导 venue"；② Table V 分布 → "P3/P4/P6 缺少解决方案 → 研究空白"；③ Discussion §A → "article type 以 method proposal 最多 → 经验研究不足"。 | paper_content.txt Page 6--8 Discussion | **M** |
| "六类 pattern 抽取"中 finding pattern 证据锚点仅写"Page 1 摘要" | §2 六类 pattern 抽取表 finding pattern 行 | 补充原文 Discussion §V 的具体 finding 锚点："the definition of agile RE is vague"（Page 7）、"no primary venue"（Page 6）、"most articles have unspecified ASD"（Page 6）、"no solutions to P3/P4/P6"（Pages 5--6）。 | paper_content.txt Page 5--7 | M |

## 6. C/I/M 结论

### C（Critical）——直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

| 编号 | 问题 | 影响分析 |
|---|---|---|
| C-1 | `[leaf-re-agile-sms-2015-orig-problem]` 错误挂载在 B2（语料收集与纳排）分支下，原文 problem taxonomy（P1--P6）实际属于 RQ3 领域分类 | 若 A2a 按当前分支归属聚合多篇论文的模式叶子，problem taxonomy 会被误归类为 corpus/search 维度，导致 schema 聚合偏差和跨论文统计口径混乱。属于 schema 结构性错误，必须修复后方可进入 A2a 统计聚合。 |
| C-2 | review 在"叶子维度表"正确声明了 6 个通用 leaf 不是原文叶子全集，但在视觉呈现上，维度树结构图只展示通用的 5 分支 7 叶子（6 通用 + finding），5 个原文候选叶子被放在次级表中 | 一个不仔细阅读次级表文字声明的 A2a/A2b 执行者可能在视觉上误认 6 个通用 leaf 已完整覆盖原文 schema，导致遗漏原文真实维度的补全工作。虽然 review 写有说明文字，但文档信息架构放置了一个高风险陷阱。 |

### I（Important）——实质影响维度树可用性、原文 schema 复原、证据可审计性

| 编号 | 问题 | 影响分析 |
|---|---|---|
| I-1 | 原文 extraction form 显式声明了四类抽取主题区（Definition / Benefits / Problems / Solutions），review 未复原该结构 | 这四类主题区是原文的方法骨架，缺失会导致 Paper2 无法从本文学到"SMS 如何将 RQ 投影为 extraction schema"这一关键模式。 |
| I-2 | 缺失原文 Table III 研究类型分类轴（7 类受控枚举）和 Tables I/II 的 venue/agile method 分布维度 | 这些是可迁移的 taxonomy 设计先验——本文展示了 SMS 如何用多个正交分类轴（venue × method × study type × benefit × problem）组织证据。当前 review 只捕捉了 benefit/problem/solution 轴。 |
| I-3 | 缺失 problem→solution 关系边，尤其是 P3/P4/P6 的 absence evidence | Absence evidence 是 Paper2 方法中"缺失值语义"和"否定证据"的重要来源，缺失它会削弱 A2a 对 absence evidence pattern 的识别能力。 |
| I-4 | 证据账本仅有 4 条（全部 `not_verified`），对于 6 张分类表 + 4 类抽取主题区的 SMS 论文过少 | A2a 精核时缺少独立证据锚点会导致核验效率低下，每条 Table 的核对需要回头重新读原文。 |
| I-5 | orig-benefit/orig-problem/orig-solution 的取值空间过于泛化，未使用原文的受控编码 | 原文 B1--B6 和 P1--P6 已经是封闭取值空间，写为"自然语言描述"会丢失 A2a 可直接统计的编码信息。 |

### M（Minor）——不阻塞的清晰度或维护性建议

| 编号 | 问题 | 建议 |
|---|---|---|
| M-1 | "六类 pattern 抽取"中 finding pattern 仅以"Page 1 摘要"为证据 | 应补充 Discussion §§A--C 的多个具体 finding 锚点 |
| M-2 | Tables I--VI 的 N 值和百分比未在 review 任何位置记录 | 可在叶子取值空间或统计链表中补充，方便 A2a 精核时比对 |
| M-3 | "六类 pattern 抽取"中 evidence presentation pattern 仅提"28 articles"，实际原文有 Tables I--VI 的完整 evidence table 结构 | 补充"多张分类表 + 文章交叉引用"这一呈现模式 |
| M-4 | §3 "对 PR-A1 schema 的启发" 可以补充 "absence evidence 是 SMS 的重要发现形式" | P3/P4/P6 的无方案标注是最好的 absence evidence 样例 |

### 最终建议：**NEEDS FIX**

C-1（orig-problem 分支归属错误）是结构性 schema 错误，必须在 A2a 开始跨论文聚合前修复。I-1 至 I-5 累计会实质影响本文对 Paper2 的 schema seed 价值和 A2a 精核效率。建议优先修复 C-1 / C-2 / I-1 / I-2 / I-3，再修复 I-4 / I-5，最后处理 M 级。
