# research-artifacts-secondary-studies · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是。读取路径：
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是。358 行全文通读，覆盖 Abstract、Introduction、Methods（search / selection / extraction / analysis）、Results（按 RQ1--RQ4 组织）、Discussion / Conclusion、References。确认了论文中 Table 1 的期刊列表存在、四阶段数据抽取方法（人工全文筛查 + Python 脚本检查 + 非永久仓库链接活链 + 人工抽查 25 篇）、Krippendorff's Alpha 一致性评估、logistic regression 趋势分析。
- **是否核对 `paper.pdf`**：是。`paper.pdf` 存在（159816 bytes），通过 `paper_content.txt` 全文与 `review.md` 交叉比对完成文本级核对；未做逐页视觉截图级人工核验。`review.md` 在 A.4 中已记录 `needs_manual_check`，本报告接受此状态并在第 5 节给出具体需核对的表号/页码/字段建议。
- **文库级规则读取**：已读取 `README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md`、`story/paper_story.md`。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

原文是一个**系统映射研究（systematic mapping study）**，目标是评估软件工程 secondary studies 如何报告 research artifacts，并提供这些 artifacts 的总体可获得性图景。摘要声称要提供"comprehensive list"，但正文主要以统计表呈现，具体逐篇清单依赖 Zenodo 工件（DOI: `10.5281/zenodo.15488074`）。

四个 RQ 组织全文结果：
- **RQ1**："How many secondary studies include a research artifact？"
- **RQ2**："Where are research artifacts stored, particularly whether permanent repositories with DOIs are used？"
- **RQ3**："How is data/artifact availability stated in papers, particularly whether a dedicated section exists？"
- **RQ4**："How do publication year and publication forum affect research artifact availability？"

贡献声明聚焦于三点：(a) 首次系统映射 SE secondary studies 的 research artifact 可获得性，(b) 用 logistic regression 证明时间趋势显著改善，(c) 强烈建议强制性发布 research artifacts。

### 2.2 方法流程

1. **检索**：2024-10-02 在 Scopus 单库检索。限定 15 个期刊（13 个 SE 相关 + 2 个广义 CS 综述期刊）的 ISSN，标题限定"Mapping Study" / "Systematic review" / "Systematic Literature Review" / "Systematic Mapping" / "Meta Analysis" / "Meta Synthesis" / "Scoping Review" / "Case Survey" / "Critical review"。年份范围 2013--2023。初始命中 643 篇。
2. **筛选**：三条件纳入（IC1: 2013--2023；IC2: secondary study；IC3: SE 相关）。对 CSUR 和 Computer Science Review 条目人工判断是否 SE 相关。最终纳入 537 篇。
3. **质量评估**：使用 Krippendorff's Alpha 评估人工判断一致性，结果 0.776（95% CI），正文称 "strong agreement"。
4. **数据抽取（四阶段）**：
   - 阶段一：人工全文筛查，识别专门说明 research artifacts 可用性的章节（dedicated section）。
   - 阶段二：Python 脚本基于正则检测论文文本中是否存在"Data Availability" / "Data Availability Statement" 等关键词。
   - 阶段三：Python 脚本检查非永久仓库（如 GitHub、个人主页）链接是否仍可访问（活链 / 死链）。
   - 阶段四：25 篇论文人工抽查，验证脚本检查结果。
5. **统计分析**：
   - 描述性统计：artifact availability 百分比、repository 类型分布、dedicated section 比例。
   - 逻辑回归（logistic regression）：以年份和期刊为自变量，artifact availability 为因变量。
   - 死链统计：2023 年 19 个非永久仓库链接中 2 个已死。

### 2.3 显式 extraction form / classification schema / taxonomy / coding scheme

原文的 extraction form 并非以单独表格列出"字段名 + 取值空间"，而是通过 **RQ 结构 + 四阶段方法** 隐式定义。从全文可复原以下抽取/分类维度：

| 原文维度 | 对应 RQ | 取值空间 / 分类项 | 统计方式 |
|---|---|---|---|
| Artifact availability | RQ1 | 有工件 / 无工件（二级分类：工件类型枚举——search strings、data extraction forms、statistics scripts、bibtex files、downloadable CSV、quality assessment forms 等） | 百分比、年份趋势 |
| Repository type | RQ2 | Permanent with DOI / Permanent without DOI / Non-permanent / By request / Data availability statement only / No statement | 百分比、堆叠条形图 |
| Specific repository name | RQ2 | Zenodo、Figshare、Mendeley Data、GitHub、GitLab、机构仓库、publisher supplementary 等 | 频次 |
| DOI presence | RQ2 | Yes / No | 百分比 |
| Reporting anchor | RQ3 | Dedicated "Data Availability" section / Mentioned in methods / Mentioned elsewhere / Not mentioned | 百分比 |
| Section content quality | RQ3 | Actually has data / "No data was used" / "Available upon request" | 定性发现 |
| Link health | RQ2 子分析 | Accessible / Dead / Redirecting | 计数（2023 年：2/19 死链） |
| Publication year | RQ4 | 2013--2023（连续或分组） | logistic regression 自变量 |
| Venue (journal) | RQ4 | 15 个期刊（TSE、TOSEM、EMSE、IST、JSS、ESE、SQJ、RE、JSEP、SoSyM、SEN、JOT、SPE、CSUR、Computer Science Review） | logistic regression 自变量 + 分组统计 |
| Quality assessment | 方法 | Krippendorff's Alpha = 0.776 | 方法学指标 |

### 2.4 从字段/统计到 conclusion / finding / gap / recommendation 的路径

本文的 finding 形成路径是**线性单一的**：每个 RQ 产生一组描述性统计 → 直接写为结果段落中的 finding 句 → Discussion 中不做额外统计，而是将结果提炼为三条 policy recommendation：(a) journals should enforce reporting practices，(b) secondary studies should have a data availability section，(c) artifacts should be stored in permanent repositories with DOIs。

**关键特征**：本文没有将统计观察转换为多路径 candidate finding、gap 或 risk hierarchy；它本质上是"状态扫描 + 趋势回归 + 规范性建议"的单层映射。Discussion 没有跨 RQ 的综合发现、矛盾信号分析或子群比较。

**对 A1-DT 审计的含义**：这篇论文的 finding 形成方式过于简单，不足以作为 Paper2 "候选发现 → 研究者质疑 → 裁决"的完整榜样。它更适合作为"artifact availability / reporting / storage"这一维度分支的 **schema seed**，而不是 finding-formation pattern 的范例。

## 3. 当前 `review.md` 维度树审计

### 3.1 树结构总览

当前 review.md 的维度树由三层组成：

- **Layer 1（根 + 主干）**：`[dim-root]` → 5 个分支 `[dim-b1]` 至 `[dim-b5]`（secondary study corpus / artifact type / availability status / repository-DOI evidence / reproducibility gap）。
- **Layer 2（通用叶子）**：6 个叶子 `[leaf-scope]`、`[leaf-corpus]`、`[leaf-taxonomy]`、`[leaf-method]`、`[leaf-evidence]`、`[leaf-finding]`，每片叶子挂在一个分支下（b5 挂两个叶子）。
- **Layer 3（候选叶子）**：6 个 `[leaf-orig-*]`，在"原文模式候选叶子映射（A1 种子）"表中独立列出，标记为 `not_verified` / `schema_seed`，明确声称"用来避免把上表六个通用接口误读为原文叶子全集"。

### 3.2 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-root]` 定位为"Research artifacts in secondary studies 的研究目标 / RQ / 贡献声明"，描述准确。 | 通过 |
| 主干分支是否覆盖原文 schema | **不充分** | 5 个分支 (b1--b5) 试图覆盖原文全部维度，但存在归类偏差：(a) `availability-status`（候选叶子）被挂到 b1 "secondary study corpus"，而原文的 availability 实际是 RQ1 的核心结果维度，不应归入"语料"；(b) `repository-provider` 被挂到 b2 "artifact type"，但原文的 repository type 是关于存储方式，不是 artifact 内容类型；(c) 原文的 quality assessment（Krippendorff's Alpha）、validity threats、artifact type sub-taxonomy 没有被显式映射到任何分支或候选叶子。 | I |
| 叶子维度是否足够具体 | **部分不足** | 通用 6 叶子设计用于跨论文统一接口，符合 `pattern-field-schema.md` 的合同，但对于本文具体 schema 来说覆盖粒度偏粗：(a) `leaf-taxonomy` 试图同时容纳"原文中的 taxonomy、classification schema、coding scheme"——本文恰有丰富的 artifact type sub-taxonomy，但在 leaf-taxonomy 层面未展开；(b) `leaf-evidence` 试图同时容纳"评价指标、数据、artifact、replication package、质量评价、threat"——本文有 Krippendorff's Alpha 质量评估和 validity threats，但皆未在通用叶子中显式填充。**候选 6 叶子改善了粒度**，但候选叶子之间的层次关系（如 repository → DOI → link health 的嵌套）未表达。 | I |
| 取值空间是否可执行 | **候选叶子部分不足** | 候选叶子 `availability-status` 取值空间写为"有开放工件、无工件、仅请求获取、断链、不清楚等状态"——但原文实际分类更细：在"有工件"下有 artifact type 子分类（search strings / data extraction forms / statistics / bibtex / CSV 等），在"无工件"下还区分"no data was used"和"available upon request"两种有害子类。候选叶子未体现这些子分类。 | M |
| 关系边是否缺失 | **是** | 现有关系边只有 2 条（method→evidence、taxonomy→finding），但本文至少有以下隐含关系未被捕获：(a) RQ → extraction field 的驱动关系（四个 RQ 决定抽取维度）；(b) availability → repository → DOI → link health 的嵌套层级关系；(c) year + venue → artifact availability 的 logistic regression 统计关系；(d) quality assessment (Krippendorff's Alpha) → extraction reliability 的方法学支撑关系；(e) validity threats → conclusion strength 的限制关系。 | I |
| 统计用途 / 分母是否正确 | **通过但有限制** | review.md 中"[统计与候选发现链路]"表明确将 `dim-root` 和 `leaf-taxonomy`、`leaf-finding` 的统计用途设为"否（A1-DT 阶段仅作 schema seed）"，并标注"原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定"。这是正确的保守处理。但需注意：原文本身有清晰分母（537 篇），且统计结果可直接用于 Paper2 的方法设计参考（如"31.5% 的 SE secondary studies 提供 artifact"这一数字可作为 Paper2 自身 artifact 要求的辩护证据），当前 review.md 未区分"不进入 SUMMARY 定量统计"和"不可作为 Paper2 方法设计引用"的差异。 | M |
| 候选 finding 路径是否完整 | **不足** | review.md 的 A.3 结论-证据映射表中，所有 12 条结论均为 `weak` / `schema_seed` / `candidate_finding`，没有一条升到 `strong`。这符合 A1-DT 降级规则。但遗漏了原文 Discussion 中的三条 policy recommendation 对应的 finding 路径：(a) "journals should enforce reporting practices" → 对应原文 RQ4 venue 差异证据；(b) "secondary studies should have data availability section" → 对应 RQ3 reporting anchor 证据；(c) "permanent repositories with DOIs" → 对应 RQ2 DOI 证据。这三条是本文的最终 conclusion，应至少作为 `candidate_finding` 或 `boundary_anchor` 出现在 A.3。 | I |
| A.1--A.4 证据链是否足够 | **基本通过但需补充** | A.1 来源表记录 3 条证据（bibtex / metadata / paper_content），覆盖完整；A.2 维度树证据账本记录 6 条证据（EV-001 至 EV-006），覆盖 RQ 声明、分类表、统计结果、discussion 和缺失项；A.3 结论映射表覆盖 12 条结论；A.4 复验清单记录 2 个检查点（结构检查 passed + 视觉核对 needs_manual_check）。**但 A.2 中多条证据定位为泛章节级（如 EV-003 "全文 RQ……"），缺少具体页码和表号**，这对 A2a 精核构成前置风险。 | M |
| 是否存在可能误导 A2a 的强主张 | **否** | review.md 在多处（行 212、行 318 的 [clm-C12]、原文候选叶子表头、A.3 全部结论的 `weak` 标记）显式声明当前为 `schema_seed` / `not_verified`，不得进入 SUMMARY 定量统计。没有将"6 个候选叶子"写成"原文 schema 完整复原"的措辞。 | 通过 |

### 3.3 关键发现：候选叶子的归类错误

当前 6 个候选叶子与 5 个分支的归属关系如下：

| 候选叶子 | 当前归属分支 | 原文实际归属 | 问题 |
|---|---|---|---|
| `availability-status` | b1 (secondary study corpus) | **RQ1 结果维度**——artifact 可得性是研究对象属性，不是 corpus 定义 | 误归类；corpus 定义应是 b1 下的 15 期刊 + ISSN + 纳入排除，不是统计结果 |
| `repository-provider` | b2 (artifact type) | **RQ2 存储方式维度**——repository 类型是关于存储，不是 artifact 内容类型 | 误归类；artifact type 应是 b2 下的 search strings / data extraction forms / scripts / bibtex 等枚举 |
| `reporting-anchor` | b3 (availability status) | **RQ3 报告位置维度**——dedicated section / methods / elsewhere 是关于报告方式 | 归类基本合理但命名偏差；b3 命名为"availability status"，实际内容却是 reporting anchor |
| `link-health` | b4 (repository/DOI evidence) | **RQ2 子维度**——链接健康是 repository 的下层属性 | 归类基本合理 |
| `artifact-content` | b5 (reproducibility gap) | **RQ1 子维度**——artifact 内容类型（search strings / data extraction forms 等）是 artifact type 的子分类 | 误归类；应归属于 b2 (artifact type)，不是 b5 (reproducibility gap) |
| `trend-context` | b5 (reproducibility gap) | **RQ4 独立维度**——年份 + venue 趋势是独立的时间/场所分析轴 | 误归类；trend 不是 reproducibility gap 的下位概念 |

这不是"把通用接口当成原文 schema"的问题，而是**候选叶子到分支的归类需要校正**。

## 4. 建议维度树骨架

以下是基于原文全文结构复原的更忠实维度树：

```
[dim-root] Research artifacts in secondary studies: a systematic mapping (2013--2023)
│
├── [dim-rq-framework] RQ 框架与贡献声明
│   ├── [leaf-rq1] RQ1: artifact availability
│   ├── [leaf-rq2] RQ2: storage location & permanence
│   ├── [leaf-rq3] RQ3: reporting mechanism
│   └── [leaf-rq4] RQ4: year & venue effects
│
├── [dim-corpus] 语料构造与纳排
│   ├── [leaf-search] 检索策略（Scopus、15 期刊 ISSN、标题关键词、2013--2023）
│   ├── [leaf-inclusion] 纳入标准（IC1/IC2/IC3）
│   ├── [leaf-denominator] 样本分母（643 → 537）
│   └── [leaf-quality-assessment] 一致性评估（Krippendorff's Alpha = 0.776）
│
├── [dim-extraction-form] 数据抽取 schema（四阶段方法）
│   ├── [leaf-artifact-availability] 工件可得性（是/否 + 工件类型子分类）
│   │   ├── [sub-leaf-artifact-type] 工件类型枚举
│   │   │   ├── search strings
│   │   │   ├── data extraction forms
│   │   │   ├── statistics scripts
│   │   │   ├── bibtex files
│   │   │   ├── downloadable CSV
│   │   │   ├── quality assessment forms
│   │   │   └── 其他 / 未分类
│   │   └── 候选取值空间：has_artifact / no_artifact / unclear
│   │
│   ├── [leaf-repository] 存储方式分类
│   │   ├── permanent_with_doi
│   │   ├── permanent_without_doi
│   │   ├── non_permanent
│   │   ├── by_request
│   │   ├── data_availability_statement_only
│   │   └── no_statement
│   │
│   ├── [leaf-repository-provider] 具体仓库 （Zenodo / Figshare / Mendeley Data / GitHub / GitLab / 机构仓库 / publisher supplementary / 其他）
│   ├── [leaf-doi] DOI 存在（是/否）
│   ├── [leaf-link-health] 链接健康（accessible / dead / redirecting / not_checked + 检查时间）
│   ├── [leaf-reporting-anchor] 报告位置（dedicated_section / in_methods / elsewhere / not_mentioned）
│   └── [leaf-section-quality] 章节内容质量（has_actual_data / no_data_claimed / upon_request / unclear）
│
├── [dim-context] 时间与场所上下文
│   ├── [leaf-year] 出版年份（2013--2023，连续或分组）
│   └── [leaf-venue] 期刊（15 个期刊枚举：TSE / TOSEM / EMSE / IST / JSS / ESE / SQJ / RE / JSEP / SoSyM / SEN / JOT / SPE / CSUR / CSR）
│
├── [dim-statistical-method] 统计方法
│   ├── [leaf-descriptive] 描述性统计（百分比、分段统计）
│   └── [leaf-regression] logistic regression（因变量：artifact availability；自变量：year + venue）
│
├── [dim-finding] 研究发现与建议
│   ├── [leaf-stat-finding] 统计发现（31.5% 有工件；2023 年 62.0% 有工件 / 30.4% 用永久仓库 + DOI；2023 年 2/19 非永久链接已死）
│   ├── [leaf-policy-recommendation] 政策建议（强制发布工件 / 应有 Data Availability 章节 / 使用永久仓库 + DOI）
│   └── [leaf-gap] 缺口声明（工件内容质量评估为未来工作）
│
├── [dim-validity] 效度威胁
│   ├── [leaf-construct-validity] 构造效度（work-in-progress papers 可能影响分类）
│   ├── [leaf-internal-validity] 内部效度（单库检索 Scopus 可能遗漏）
│   ├── [leaf-external-validity] 外部效度（只覆盖 15 个期刊）
│   └── [leaf-conclusion-validity] 结论效度（分类主观性 + 单轮编码）
│
└── [dim-self-artifact] 本文自有工件
    └── [leaf-zenodo] Zenodo DOI: 10.5281/zenodo.15488074（含完整方法细节、逐篇清单）
```

### 各叶子的统计属性

| 叶子 | 可统计 | 分母 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|
| `leaf-rq1`--`leaf-rq4` | 否（结构描述） | — | — | Abstract + §2 + §3（各 RQ 引导句） |
| `leaf-search` | 否（描述） | — | — | §2.1 |
| `leaf-inclusion` | 否（描述） | — | — | §2.2 |
| `leaf-denominator` | 是 | 643 初始 → 537 纳入 | — | §2.1--2.2 |
| `leaf-quality-assessment` | 是（单一值） | — | — | §2.2（"Krippendorff's Alpha 0.776"） |
| `leaf-artifact-availability` | 是（二分类 + 多分类子类） | 537 | `not_reported` | §3 RQ1 段落 + 对应 Table |
| `leaf-repository` | 是（6 类枚举） | 有工件的子集（约 31.5% × 537 ≈ 169） | `not_reported` | §3 RQ2 段落 + 对应 Table |
| `leaf-repository-provider` | 是（频次） | 同上 | `unspecified` | §3 RQ2 + 对应 Table |
| `leaf-doi` | 是（二分类） | 同上 | `not_reported` | §3 RQ2 |
| `leaf-link-health` | 是（accessible / dead / redirecting） | 非永久仓库链接子集 | `not_checked` | §3 RQ2 子段落 |
| `leaf-reporting-anchor` | 是（4 类枚举） | 537 | `not_found` | §3 RQ3 段落 + 对应 Table |
| `leaf-section-quality` | 是（定性分类） | 有 dedicated section 的子集 | `not_evaluated` | §3 RQ3 讨论段落 |
| `leaf-year` | 是（连续 + 分组） | 537 的年份分布 | — | §2.1 + §3 RQ4 |
| `leaf-venue` | 是（15 类枚举） | 537 的 venue 分布 | — | Table 1 + §3 RQ4 |
| `leaf-descriptive` | 否（方法描述） | — | — | §2.3 |
| `leaf-regression` | 是（模型系数、显著性） | 537 | — | §3 RQ4 |
| `leaf-stat-finding` | 否（文本性 finding） | — | — | §3 + §4 Discussion |
| `leaf-policy-recommendation` | 否（规范性建议） | — | — | §4 Discussion |
| `leaf-gap` | 否（缺口声明） | — | — | §4 Discussion + §5 Conclusion |
| `leaf-construct-validity`--`leaf-conclusion-validity` | 否（文本性 threat） | — | — | 原文 validity threats 段落（位于 Discussion 附近） |
| `leaf-zenodo` | 是（单一链接） | — | — | 正文脚注 + Data availability |

### 与当前 review.md 的关系

当前 review.md 的结构（5 分支 + 6 通用叶子 + 6 候选叶子）在**总体上表达了本文的字段方向**，且明确标注所有候选叶子为 `not_verified` / `schema_seed`。上述建议骨架不是推翻重做，而是在现有基础上做三类修正：**(a)** 校正候选叶子的分支归属，**(b)** 补充分支和叶子（quality、validity、RQ 框架、statistical method、self-artifact），**(c)** 显式表达嵌套层级（如 availability → artifact type 子分类不可扁平化为并列叶子）。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 校正 `availability-status` 候选叶子的分支归属 | 原文模式候选叶子映射表中 `availability-status` 行 | 将所属主干从 `[dim-b1]` 改为新建的 extraction-form 维度（或至少改为 `[dim-b3]`），并在释义中说明它对应原文 RQ1 的统计结果，不是 corpus 定义 | `paper_content.txt` §2.2 纳入排除（corpus 定义）vs §3 RQ1（artifact availability 统计） | I |
| 校正 `repository-provider` 候选叶子的分支归属 | 原文模式候选叶子映射表中 `repository-provider` 行 | 将所属主干从 `[dim-b2]` 改为新建的 extraction-form 维度（对应原文 RQ2），并说明 repository 类型是关于存储而非 artifact 内容 | `paper_content.txt` §3 RQ2 | I |
| 校正 `artifact-content` 候选叶子的分支归属 | 原文模式候选叶子映射表中 `artifact-content` 行 | 将所属主干从 `[dim-b5]` 改为 `[dim-b2]`（artifact type），artifact 内容类型是 artifact type 的自然子分类；或新建 extraction-form 维度 | `paper_content.txt` §3 RQ1 对 artifact 类型的描述 | I |
| 补充原文 RQ 框架维度 | 维度树主干层新增 `[dim-rq-framework]` | 将原文四个 RQ 作为叶子维度显式记录，因为本文的 extraction form 是按 RQ 组织的（而非按 flat 字段列表） | `paper_content.txt` §3 以 RQ1--RQ4 组织全章 | I |
| 补充原文 quality assessment 维度 | 新增候选叶子 `[leaf-orig-quality-assessment]` | 原文使用 Krippendorff's Alpha（0.776）评估编码一致性，这是 A1-M3（方法）层级的重要证据，不应被忽略 | `paper_content.txt` §2.2 "Krippendorff's Alpha of 0.776 which shows strong agreement" | I |
| 补充原文 validity threats 维度 | 新增 `[dim-validity]` 及其子叶 | 原文在 Discussion 中讨论了 construct/internal/external/conclusion validity threats，这是 survey-of-surveys 脚手架需要的 validity threat pattern 来源 | `paper_content.txt` Discussion 部分的 validity 讨论（需核对具体页码） | I |
| 补充原文三条 policy recommendation 到 A.3 | A.3 结论-证据映射表新增 3 条结论 | 新增：`[clm-journals-enforce]`、`[clm-data-availability-section]`、`[clm-permanent-repository-doi]`，每条映射到对应的 RQ 统计证据和 discussion 段落 | `paper_content.txt` §4 Discussion 末段三条 recommendation | I |
| 补充原文自有 Zenodo artifact 信息 | A.1 来源表或新增 artifact 节点 | 原文自身发布了一个 Zenodo artifact（DOI: `10.5281/zenodo.15488074`），这既是"本文的自我实践"，也是潜在复制/核查入口 | `paper_content.txt` 正文脚注 2 + §Data availability；`metadata.json` "本文自有开放工件"字段 | M |
| 补充 A.2 证据的具体页码/表号 | A.2 证据账本 EV-002 至 EV-006 | 将 `EV-002` "Table 1 及对应段落"分解为具体表号（如 Table 1a: journals, Table 1b: search terms），补充页码（paper.pdf 页码 vs 期刊页码） | 需人工打开 `paper.pdf` 核验 | M |
| 补充统计方法维度 | 新增 `[leaf-regression]` | 原文使用了 logistic regression 而非仅描述性统计，这是区别于大多数 survey-of-surveys 样本的方法特征 | `paper_content.txt` §3 RQ4 "logistic regression" | M |
| 记录 RQ4 的 venue 维度未展开 | 候选叶子 `trend-context` 的备注 | `trend-context` 当前将 year 和 venue 合并在一个叶子里，但原文 Table 1 显式列出了 15 个期刊的 artifact availability 统计，应作为独立分类维度 | `paper_content.txt` Table 1 + §3 RQ4 | M |

## 6. C/I/M 结论

### C（Critical）——直接破坏 Paper2 学术目标或证据链的问题

**无。** 当前 review.md 未出现将 roadmap/vision 写成完成型统计 finding、将弱证据升级为强结论、或声称 PRISMA 合规等禁止性错误。所有结论均标记为 `weak` / `schema_seed`，符合 A1-DT 降级规则。

### I（Important）——实质影响维度树可用性、原文 schema 复原或证据可审计性的问题

1. **候选叶子分支归属错误**（I）：`availability-status` → b1 而非 extraction-form/RQ1 维度、`repository-provider` → b2 而非 extraction-form/RQ2 维度、`artifact-content` → b5 而非 b2。这会导致后续 A2a 在合并多篇论文的维度树时出现系统性归类偏差——例如其他论文的"artifact type"和"repository type"被分到不同分支后无法交叉统计。**影响**：破坏 A2a 跨论文统计时的字段对齐和交叉表可用性。

2. **原文 RQ 框架未被显式建模**（I）：本文的 extraction form 是按四个 RQ 组织的，而当前维度树用 5 个扁平化分支替代了 RQ 结构。这丢失了"RQ 驱动抽取字段"这一重要的综述元模型信息——Paper2 的核心方法正是研究者定义 RQ → 投影为维度模式。**影响**：这篇论文本应是"RQ → extraction form"模式的正面范例，但当前维度树没有捕获这一结构，削弱了其在 Paper2 方法设计中的引用价值。

3. **原文 quality assessment（Krippendorff's Alpha）遗漏**（I）：质量评估是 survey-of-surveys 脚手架 A1-M3（方法/技术/干预）层级的关键证据类型，`pattern-field-schema.md` 中的 `evidence_presentation_pattern` 也明确包含"质量表"。遗漏这一维度意味着后续 A2a 无法从本文学习"如何在 secondary study 中报告编码一致性"。**影响**：限制 Paper2 方法设计中对编码质量控制的设计空间。

4. **原文 validity threats 维度完全遗漏**（I）：本文在 Discussion 中讨论了四种效度威胁，这是 survey-of-surveys `validity_threat_pattern` 的直接来源。当前维度树没有任何 validity 相关节点。**影响**：Paper2 在 A5 报告自身 validity threats 时缺少可参考的模式先验。

5. **原文三条 policy recommendation 未进入 A.3**（I）：本文的 Discussion 中三条 recommendation 是其最终 conclusion，但 review.md 的 A.3 结论映射表只有 12 条 schema-level 结论，没有一条直接引用原文的 finding/recommendation 内容。**影响**：A3 只映射了"这篇论文有哪些维度可迁移"，但没有映射"这篇论文自己发现了什么"——这是对原文学术贡献的不完整表征。

### M（Minor）——不阻塞但影响清晰度或可维护性的问题

1. 候选叶子取值空间未体现原文的嵌套子分类（如 artifact type 的 search strings / data extraction forms 等子类）。
2. A.2 证据账本中多数证据定位为章节级，缺少页码和表号。
3. 原文自有 Zenodo artifact 未被记录为独立节点。
4. 原文的 logistic regression 统计方法特征未被记录。
5. 原文 Table 1 的 15 个期刊列表未被显式映射。

### 最终建议

**NEEDS FIX。** 不是阻断性驳回——当前 review.md 已正确执行 A1-DT 的核心纪律（所有结论 `weak` / `schema_seed`、明确区分通用接口与候选叶子、不做越权统计）。但 I 级问题（分支归属错误、RQ 框架遗漏、quality/validity 遗漏、A.3 遗漏原文 finding）需要在 A2a 启动前修复，否则会：

- 使跨论文维度树合并时产生不可逆的归类偏移；
- 丢失可被 Paper2 方法设计直接引用的关键模式（RQ → extraction form、编码一致性评估、效度威胁报告）；
- 导致 A3 结论-证据映射无法完整反映本文的学术贡献。

修复量估计：中等（约需修改 5 个分支归属 + 新增 3--4 个维度/候选叶子 + 补充 3--5 条 A.3 结论），预计 1 个 PR 可完成。
