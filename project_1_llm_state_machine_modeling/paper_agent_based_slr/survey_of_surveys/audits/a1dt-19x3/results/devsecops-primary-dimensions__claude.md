# devsecops-primary-dimensions · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（PR #135 / paper2-a1-dimension-tree-inventory）。
- 是否读取 `$ai-research-writing-skill`：是。
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- 是否读取 `$research-planning`：是。
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`
- 是否读取 `$oh-my-codex:autoresearch`：是。
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- 是否完整阅读 `paper_content.txt`：是（3158 行，全文 grep + 顺序阅读 §1 引言、§2 相关综述比较、§3.3 RQ、§3.4 Search Strings、§3.5 纳排与 QA、§3.6 复制与 snowballing、§3.7 Confirmatory search、§3.8 抽取/TA/trustworthiness、§4.1 五大方面与分类与 CPTM、§4.2 GSE、§5 威胁、§6 结论与开放材料）。
- 是否核对 `paper.pdf`：仅文本级；图 4、Fig.5–9 CPTM 连线、Table 5–21 表格版式未逐图核验，原因：审计任务在文本级即可定位结构性问题；版面级精核已显式归入 A2a。
- 已读取文库规则：`survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md`，及 `paper_agent_based_slr/story/paper_story.md`。

## 2. 原文真实结构复原

### 2.1 RQ 与贡献声明

- **RQ1**：DevSecOps 在 white + grey literature 中的 current state，包括 aspects、themes、links（§3.3）。
  - 子问 RQ1.1 aspects、RQ1.2 themes、RQ1.3 links。
- **RQ2**：DevSecOps 如何在 Global Software Engineering（GSE）context 中被采用。
- 显式贡献声明（§1、§3）：(a) MLR 覆盖 DevSecOps 第一个十年；(b) 新 taxonomy；(c) CPTM 模型；(d) GSE 空白报告；(e) 开放材料与 JSS Open Science Board 验证。

### 2.2 方法流程

- 检索分两轨：WL（ACM/IEEE/Scopus）+ GL（Google）。ScienceDirect、Springer 仅用于 snowballing 与 confirmatory。
- **Search String 1**（DevOps × security/secure/safe + secdevops/devsecops）服务 RQ1；
- **Search String 2**（在 SS1 基础上加 GSE/GSD/global/distributed/multi-site/multi-nation/transnational/remote work）服务 RQ2。
- 时间窗：2012–2021；2022 confirmatory 仅作 staleness 补丁，13 WL + 7 GL 不进入 TA 与 CPTM。
- 纳入 5 条、排除 5 条（含排除 secondary studies）。
- QA 表（§3.5 + Fig.2）：14 个 yes/no 题 + 1 个 literature type 0–4 分，总分 18，阈值 11。
- Snowballing：以 backward 为主，对包含的二级研究做雪球验证。

### 2.3 显式 extraction form / classification schema / coding scheme / 模型

- §3.8.1 数据抽取表来自 Kitchenham 2007 的改编（"adapted data extraction form … to summarize the result of data extraction"），细表在 Zenodo。
- §3.8.2 reflexive Thematic Analysis 四层抽象：Text → Code → Theme → Model（Braun & Clarke 2020/2021）。
- 显式 classification schema：
  - **5 aspects**：Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement（§4.1.1，Table 3）。
  - **4 high-order categories**：OPC / PC / Technology / Business（§4.1.2），Metrics 缺 Business（3 categories），Tools 单一 Technology。
  - **CPTM 元素**：Cxx / Pxx / Txx / Mxx 编号项 + 跨字段链接（§4.2）。
  - **Gartner DevSecOps 10-stage lifecycle**：Plan/Create/Verify/Preproduction/Release/Prevent/Detect/Respond/Predict/Adapt（§4.2，Fig.5–9）。
- 显式 quality rubric：QA 表 14+1 项、阈值 11/18。
- 显式 trustworthiness 框架（§3.8.3）：credibility / confirmability / dependability / transferability。
- 显式 threats to validity（§5）：study selection / QA / data extraction bias、coding & theming subjectivity、prior framework 渗透、search-string completeness、temporal staleness。
- Table 2 抽取量表给出 "extracted data / coded data / themes / categories" 4 列（§4.1.2 复盘表）。

### 2.4 字段到 finding 的形成路径

- 频次（per aspect / per category 行计数） → 来源结构对比（WL vs GL，Table 4）→ 与前序综述 overlap → CPTM 连线缺口（practice 无 tool/metric）→ candidate finding（metrics weak、business GL-biased、GSE absence、framework-design trend）。
- absence finding（GSE）来自 String 1 0-hit + String 2 仅 2 WL + GL 前 10 页无命中 + 四种竞争解释。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-...-root]` 指向 "Identifying the primary dimensions of DevSecOps" 与 RQ/贡献，与原文 §1/§3.3 一致 | 通过 |
| 主干分支是否覆盖原文 schema | 部分缺失 | b1 aspect / b2 theme-category / b3 CPTM item / b4 lifecycle stage / b5 GSE gap 覆盖五大显式 schema 主轴，但缺：QA rubric、search-string、source-track WL/GL、confirmatory-vs-main、extraction-form、trustworthiness 四轴、threats-to-validity 这些原文显式 schema 元素未被列入主干或候选种子层 | I |
| 叶子维度是否足够具体 | 不足但有兜底 | "叶子表"6 个通用 leaf 是跨论文接口；calibration 段已显式声明它们 **不是** 原文叶子全集，并通过"原文模式候选叶子映射（A1 种子）"列出 5 个 source schema 候选叶子；但这 5 个候选叶子仍把原文 5 aspects、4 categories、4 CPTM 元素类、10 Gartner stages、GSE gap 各自压成单个 leaf，无枚举取值空间 | I |
| 取值空间是否可执行 | 不足 | 通用 6 leaves 的取值空间写法是泛化模板；5 个 source-schema 候选叶子无枚举（aspect 应 ∈ {Definitions, Challenges, Practices, Tools/Technologies, Metrics}；category ∈ {OPC, PC, Technology, Business}；CPTM ∈ {Challenge, Practice, Tool, Metric}；stage ∈ Gartner 10 阶段）；这些都是原文显式封闭枚举，本应在 A1-DT 即可写出 | I |
| 关系边是否缺失 | 部分缺失 | 已建 method↔evidence 与 taxonomy↔finding 两条；但原文 CPTM 的核心关系 `Challenge→Practice→Tool→Metric` + `theme→category→lifecycle_stage` 未显式建边；这是 CPTM 模型的本体 | I |
| 统计用途 / 分母是否正确 | 通过 | 所有节点显式写 "否（A1-DT 阶段仅作 schema seed）"，未误入主统计池；候选发现统一降级 weak | 通过 |
| 候选 finding 路径是否完整 | 部分缺失 | EV-003 释义已覆盖统计→discussion→候选发现路径；但 absence finding (GSE) 的反向解释链 + confirmatory search 隔离策略 未单独建节点；当前 b5 把 GSE gap 与一般 evidence/finding 两个 leaf 混挂 | I |
| A.1–A.4 证据链是否足够 | 部分不足 | A.1/A.4 完整；A.2 全部 5 条 EV 标 `not_verified` 即便 `paper_content.txt` 本地 text-level 可直接核验（如 §3.3 RQ、§4.1.1 aspects、§3.8.1 extraction form、§3.8.3 trustworthiness）；当前未区分 "text-verified, 待 pdf 表图核验" 与 "未核验" | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | 所有结论标 weak + schema_seed / candidate_finding；calibration 段明确把通用 leaf 与原文叶子区分；不存在把 GSE absence 升级为完成型 finding 的语句；roadmap 类语句未被冒充统计结论 | 通过 |

## 4. 建议维度树骨架

当前 review 在 calibration + "原文模式候选叶子映射" 一节已经守住底线（明确通用 6 leaf 不是原文叶子全集，5 个 source-schema 候选叶子全部 `not_verified` + `schema_seed`），方向正确。但要让 A2a 能精核而不重写，建议骨架补强如下：

```
[dim-root] Identifying the primary dimensions of DevSecOps  (MLR)
├── [b1] DevSecOps aspect                                   value ∈ {Definitions, Challenges, Practices, Tools/Technologies, Metrics/Measurement}
├── [b2] high-order category                                value ∈ {OPC, PC, Technology, Business}（Metrics 缺 Business；Tools 仅 Technology）
├── [b3] CPTM item                                          subtype ∈ {Challenge(Cxx), Practice(Pxx), Tool(Txx), Metric(Mxx)}
├── [b4] Gartner DevSecOps lifecycle stage                  value ∈ {Plan, Create, Verify, Preproduction, Release, Prevent, Detect, Respond, Predict, Adapt}
├── [b5] GSE context probe                                  value ∈ {SS1-hit, SS2-hit, snowball-hit, GL-hit, absence}
├── [b6] (新增) review-protocol schema                       叶子：source_track {WL, GL}, search_string_id {SS1, SS2}, database, time_window, snowballing_role {backward, replication}, confirmatory_only {true,false}
├── [b7] (新增) quality-assessment schema                    叶子：qa_item_id (14 个 yes/no), literature_type_score (0–4), qa_total (0–18), qa_threshold = 11, included {true,false}
├── [b8] (新增) trustworthiness-axes schema                  value ∈ {credibility, confirmability, dependability, transferability}
└── [b9] (新增) threats-to-validity schema                   value ∈ {study_selection, QA, extraction, synthesis_subjectivity, search_string, staleness, prior_framework_priming}

关系边（最少需要）：
- edge_cptm_chain      : Challenge → Practice → Tool → Metric
- edge_theme_category  : theme → category
- edge_item_stage      : (challenge|practice|tool) → lifecycle_stage
- edge_aspect_source   : aspect × source_track (WL/GL count)
- edge_qa_inclusion    : study × qa_total ≥ 11 → included
- edge_gse_probe       : SS1/SS2/GL/snowball → absence_strength
```

理由：

1. 不增 b6/b7/b8/b9 这四个 schema 主轴，A2a 在做"原文 schema 复原"时只能写自由文本而无法 ground 到精确字段；review 给的 `[leaf-...-corpus]` 等通用叶子无法承载 WL/GL/SS1/SS2/QA-cutoff 这些原文显式 enum。
2. b1–b5 的 5 个候选源 schema 叶子继续保留为 `[leaf-...-orig-*]`，但**必须给出枚举取值空间**——原文都给了封闭集合（见 §3.4、§4.1.1、§4.1.2、§4.2），A1-DT 应当能写出。
3. CPTM 关系是本论文核心贡献，必须显式建边而不是隐藏在 evidence ledger。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 5 个 source-schema 候选叶子补"候选取值空间"枚举 | "原文模式候选叶子映射（A1 种子）" 表的"候选取值空间"列 | 把 aspect / category / cptm / stage / gse-probe 的封闭枚举写出，标 `schema_seed; closed_enum` | `paper_content.txt` §3.4、§4.1.1、§4.1.2、§4.2 | I |
| 新增 4 个 schema 主轴 b6–b9 | "维度树结构" 与 "叶子维度表" | 加入 review-protocol、QA-rubric、trustworthiness、threats-to-validity 四轴；至少各挂 1 个 `[leaf-...-orig-*]` 候选叶子 + 枚举取值空间 | `paper_content.txt` §3.4–§3.5、Fig.2 QA form、§3.8.3、§5 | I |
| 关系边补 CPTM 链 + theme↔category + item↔stage + aspect↔source_track | "关系边表" | 新增 4–5 条 edge；其中 `edge_cptm_chain` 是本文核心贡献，缺它将削弱 b3 b4 之间的语义 | `paper_content.txt` §4.2 + Fig.5–9 文本叙述 | I |
| A.2 EV 强度细化：text_level_verified vs not_verified | "A.2 维度树证据账本" | 把当前 `not_verified` 拆为 `text_level_verified`（paper_content.txt 已可定位）与 `pdf_pending`（仅 Fig./Table 版面）；并补章节锚（§3.3、§3.8.1、§4.1.1、§4.2、§5） | `paper_content.txt` 显式段落 | I |
| GSE absence 单列证据链节点 | b5 或独立 evidence | 在 b5 增加 GSE-probe 的 SS1/SS2/snowball/GL 四路探查 + 四种竞争解释 + claim_strength=weak | `paper_content.txt` §4.2 RQ2 段、§5 | M |
| 1.快速结论卡片"样本规模"口径 | §1 卡片 | 补注 "RQ1 102 WL + 43 GL；摘要合并 104 WL（含 RQ2 的 2 WL）" 已在 §7 列待复核，可在卡片处加 (*) 标注以免误统计 | `paper_content.txt` §4.1、摘要 | M |
| 5 个 source-schema 候选叶子的"证据引用"列 | 同表 | 现在统一指 EV-002；建议拆 EV-002 为 EV-002a（aspect 5 项）、EV-002b（category 4 项）、EV-002c（CPTM 编号 + lifecycle）三个子证据，便于 A2a 精确锚定 | `paper_content.txt` §4.1.1、§4.1.2、§4.2 | M |

## 6. C/I/M 结论

- **C**：无。当前 review.md 没有把通用 6 leaf 误当原文 schema（已有显式 calibration），没有把 GSE absence 或 roadmap/CPTM 升级为完成型 finding，所有结论 `weak + schema_seed/candidate_finding`，未误入主统计池；不存在直接破坏 Paper2 学术目标或证据链的硬伤。
- **I**（5 项）：
  1. 主干缺 review-protocol / QA-rubric / trustworthiness / threats-to-validity 四个原文显式 schema 主轴 → 影响 A2a 能否对 WL/GL/SS1/SS2/QA-cutoff/threat 做精核。
  2. 5 个 source-schema 候选叶子未写封闭枚举取值空间（原文都给了）→ A2a 必须重写而非精核。
  3. CPTM `Challenge→Practice→Tool→Metric` 关系链未显式建边 → 削弱本文核心贡献在维度树中的表达。
  4. A.2 全部 EV `not_verified` 笼统降级 → 与 paper_content.txt 文本级可核验事实不符，损害证据链精度。
  5. GSE absence 的 4 路探查 + 4 种竞争解释 未独立为节点 → 影响 A2a 评估 absence finding 的可统计性边界。
- **M**（3 项）：候选叶子证据引用粒度过粗、样本规模口径需在卡片处加 (*)、GSE 节点位置可独立。

**最终建议：NEEDS FIX（I 级 5 项；不阻塞 PR 落库，但需在 A2a 入口前修复或显式记录为遗留任务）**。
