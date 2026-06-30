I now have full context. Let me deliver the complete audit report.

`★ Insight ─────────────────────────────────────`
关键观察：本文 §4.3 文中明说 “seven clusters … five limitation clusters”，但 Table 3 实际给出 L1–L6（含 L6 usability，仅 1 个 proposal）；这是原文内部的口径不一致，必须保留为待复核证据，而不是擅自修正。
原文 §3.5 显式说明 RQ1 抽取“authors 用于 strategy 的 keywords”，RQ2 抽 goals/limitations，RQ3 抽 metrics/users + 若用 generic “user” 则留空——这就是真正的 extraction schema，应直接进入维度树叶子层。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇全文审计报告：`mdse-modelling-assistants-mapping`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `mdse-modelling-assistants-mapping` |
| agent | `claude`（Opus 4.7 [1m]，本会话由本进程直接执行） |
| 是否已读 `paper_content.txt` | 是；分段阅读 §1–§8（Page 1–18）及 References 起始部分；Table 1–5 文本核验 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；DOI 10.1016/j.infsof.2024.107492、IST 2024、CCF B、`evidence_role=systematic_mapping_dimension_pattern` 已记录 |
| 是否打开或核对 `paper.pdf` | 否（本审计只基于本地 `paper_content.txt` 文本与 `bibtex.bib` / `metadata.json`，未单独打开 PDF 视觉核验；图 4–15 的 bubble chart、PRISMA flow、Research Agenda 图等仍需 A2a 视觉核验） |
| 原文类型 | SMS（systematic mapping study）+ 实践侧 grey-literature documentation review（混合：SMS + practice review） |
| 被编码样本单位 | (a) primary studies / proposals（n=58，引用 [20]–[77]）；(b) MDSE tools from Gartner Magic Quadrant 2023（n=17，其中 7 个有 documentation，产出 15 个 practice proposals） |
| 样本数量 / 分母 | 文献侧：3,176 screened records → 77 possible → 58 included；K=0.634（inclusion）/ 0.651（clustering）。实践侧：17 GMQ tools → 10 NF + 7 D → 15 practice proposals |
| 原生树类型 | **维度森林**：literature-side SMS 编码 schema 一棵树（strategy / goal / limitation / metric / target user）+ practice-side documentation 编码同一 schema 投影一棵子树，外接 GMQ 分类（LE/C/V/NP）与 documentation 状态（D/NF） |
| 主统计池资格 | 局部可统计：proposals × cluster 频次表（Table 2/3/4）、literature vs practice 分布（Fig. 13）有原文分母与显式数字，可作主统计池候选；但**单标签 cluster** 与作者术语 cluster 边界主观这两条限制必须随统计一起迁移 |
| 总体判定 | **needs repair**（现 `review.md` 把六个通用接口叶子当作 A1-DT v2 主结构，与本文真实编码 schema 不一致；§3.5 与 Table 2/3/4 显式给出的 5 字段树未升级为主干叶子） |

## 1. 原文证据阅读说明

本轮实际读取的本地文件与章节：

- `bibtex.bib`（全文 12 行）：确认标题、作者、DOI、IST 2024 元信息。
- `metadata.json`（全文 35 行）：确认 `evidence_role=systematic_mapping_dimension_pattern`、`eligible_for_statistical_synthesis=true`、`systematic_evidence_status=systematic_mapping`、CCF B / IST / hybrid OA。
- `paper_content.txt`：分段阅读 §1 Introduction（Page 1–2）、§2 Related work（Page 2–3）、§3 Systematic mapping study design 含 §3.1–§3.5（Page 3–5）、§4 Results 含 §4.1–§4.4（Page 5–10）、§5 State of the practice 含 §5.1–§5.2（Page 10–13）、§6 Comparative analysis（Page 13–14）、§7 Threats（Page 15）、§8 Conclusions（Page 15–17）、References 开头（Page 17–18）。Table 1（QA questionnaire）、Table 2（RQ1 clusters）、Table 3（RQ2 goals/limitations）、Table 4（RQ3 metrics/users）、Table 5（RQ4 practice quotes）的文本部分均已通读。
- `review.md`（既有 v1+19×3 返修版）：通读全文 564 行；当前 A1-DT v2 主干仍是六叶通用接口（`scope/corpus/taxonomy/method/evidence/finding`），原文真正编码 schema 被压在“原文模式候选叶子映射（A1 种子）”与“19×3 审计后返修”两个二级表中。

仅基于 text 文件做的判断，**仍需 PDF 视觉核验**的内容：

1. Fig. 4 RQ1 distribution、Fig. 5 G–L bubble、Fig. 6 M–U bubble、Fig. 11 S–G–L bubble、Fig. 12 G–M–U bubble、Fig. 13 lit-vs-practice 的具体数值与气泡半径口径；
2. Fig. 1（Research overview）、Fig. 2（SMS design overview）、Fig. 3（PRISMA flow）、Fig. 7（GMQ review overview）、Fig. 9/10（practice distributions）、Fig. 14（repository visualisation）、Fig. 15（research agenda）的精确节点与文字；
3. §4.3 文中“five limitation clusters”与 Table 3 中 L1–L6 的口径差异：是否在版式中存在 L6 的脚注 / inline 解释；
4. Zenodo replication package `10262145` 的 raw extraction 与 cluster CSV。

关键原文证据锚点（5–12 条，短引或释义）：

| # | 章节定位（page / 行近似） | 角色 | 简要释义或短引 |
|---|---|---|---|
| E1 | §1, Page 1, abstract & “Modelling assistance is the strategy—i.e., any method, technique, framework, or guideline—that aims to assist humans during software modelling tasks in MDSE tools.” | scope definition | 给出 modelling assistance 定义，并明确 unit = MDSE-tool-user-facing proposals |
| E2 | §1, Page 2, MRQ：“What proposals exist in the literature and practice to assist humans during modelling tasks in MDSE tools?” | RQ root | MRQ + 拆解为 RQ1/RQ2/RQ3 + 实践侧 RQ4 |
| E3 | §3.1, Page 3–4, RQ1/RQ2/RQ3 的精确措辞与“we expect to gather a set of tools, methods, techniques, and frameworks…” | 树根 → 主干字段 | 显式说明 extraction 字段：strategy / goals / limitations / metrics / target users |
| E4 | §3.5, Page 4–5：“RQ1: Extract the keywords the proposals’ authors use…; RQ2: …leave the field blank…; RQ3: …Leave the field blank if the authors do not state something…or if the authors use ‘user’ to refer to their target users.” | 抽取规则 + 缺失语义 | 原文显式定义“留空”=作者未报告；后续转为 L-NS / NE / U-NS 编码 |
| E5 | §3.5, Page 5 脚注 5：“we recognise that…definitions of method, framework, technique, and tool are still not unified…we rely on the keywords adopted by the proposals’ authors and our definition to each cluster.” | terminology bias | 作者承认 cluster 边界依赖作者术语 |
| E6 | §4.1, Page 5–6 与 Fig. 3：1,996 + 5 = 2,001 → 51 possible → top 12 seeds → 4 rounds snowballing → 1,175 records → total 3,176 screened → 77 possible → 58 included；K=0.634 / 0.651 | corpus pipeline | 系统检索分母与 inter-rater 数据 |
| E7 | §4.2, Table 2 + Fig. 4：Tools 39.7 %、Frameworks 19.0 %、Techniques 15.5 %、Methods 13.8 %、Guidelines 6.9 %、Languages 5.2 %；“93.1 % … totally or partially software implementations” | strategy taxonomy | 6-cluster 完整枚举 + 比例 |
| E8 | §4.3, Page 7：“we propose seven clusters about proposals’ goals and five clusters about proposals’ limitations.”，但 Table 3 列出 L1–L6（含 L6 usability 仅 [65]） + L-NS | **原文内部口径不一致** | 必须按 not_verified 保留，A2a 须做 PDF/Zenodo 复核 |
| E9 | §4.3, Page 8：分布 “G6 31.0 %（18）……G1/G2/G3/G4/G7 合 43.1 %（25）……G5 25.9 %（15）……50.0 % proposals 明确报告 limitations” | goal × create/refine 三分法 + limitation reporting rate | 直接量化 missingness |
| E10 | §4.4, Table 4 + Page 9：M1 effectiveness 23.6 %、M2 efficiency 23.6 %、M3 user perception 4.2 %、NE 48.6 %；U1 27.6 %、U2 13.8 %、U3 29.3 %、U-NS 29.3 % | metric / user 频次 | 量化 evaluation gap 与 user gap |
| E11 | §5.2, Table 5 + Fig. 9/10：17 GMQ tools → 10 NF + 7 D → 15 proposals；practice strategy=80 % Tool、goal=100 % 报告、limitation 报告 20 %、metric NF 73.3 %、user NF 73.3 % | practice projection | 与 literature 同一 schema 投影 + “you” 隐藏 target user |
| E12 | §6, Fig. 11/12/13；§7.1 terminology / subjective interpretation / inter-rater；§7.2 grey literature & search bias；§7.3 language bias | cross-axis + threats | 关系边与 validity 边界的证据来源 |

## 2. 样本单位与字段来源判定

1. **原文纳入与逐项描述的对象是什么？**
   - 主样本单位 = **primary study proposals**（n=58，每个 proposal 一行编码，引用 [20]–[77]）。
   - 辅样本单位 = **MDSE tools**（n=17 GMQ tools，作为 grey-literature carriers）与 **practice proposals**（n=15 documented assistance proposals inside 7 tools）。
   - 不是“按 RQ 列 finding”，也不是“按章节列工具”，而是“每条 proposal 一条记录、字段化编码、再聚类”。

2. **作者有没有系统检索 / 纳排 / 抽取 / 编码方案？**
   - 有完整系统流程：PICO 检索式（5 数据库）+ snowballing（4 轮，top-12 seeds 来自 QA）+ I/E criteria（I1–I2、E1–E5）+ 3-point Likert QA（Table 1）+ data extraction schema（RQ1 keywords / RQ2 goals & limitations / RQ3 metrics & users）+ 三 reviewer + K-statistic 报告。
   - 实践侧不是新数据库检索，而是 GMQ 2023 报告 → 17 tool 列表 → 公开文档 quote 抽取 → 同 schema 投影。

3. **原文字段来自哪里？**
   - 主 schema 来自 **§3.5 data extraction strategy + §4.2/§4.3/§4.4 cluster definitions + Table 2/3/4**。这是“extraction form + post-hoc cluster ontology”混合：先抽 author keywords，再由 R1 cluster、R4 复核、K-statistic 量化 agreement。
   - 缺失语义来自 §3.5 与 §4.3/§4.4 显式编码：`L-NS`（limitation not specified）、`NE`（not evaluated）、`U-NS`（generic “user” 或 “he/she” 隐藏的 target user）；practice 侧加 `NF`（documentation not found）。
   - replication package = Zenodo `10262145`，含 raw + clustered data（本审计未访问）。

4. **RQ 与样本单位的关系：**
   - RQ1–RQ3 = **样本字段定义**（按 RQ 提取并 cluster），不是结果分章。
   - RQ4 = **实践侧 schema 投影 + GMQ 分类辅助维度**。
   - MRQ 是树根问题；RQ 是“样本单位 → 字段树各主干”的桥。

5. **是否需要降级？**
   - **不降级**：本文确有系统样本库（58 + 15）、显式纳排、QA、K-statistic、replication package。可作为 schema-seed + 局部统计候选。
   - 但 **单标签 cluster**（§4.2 末尾：“we cluster each proposal in one cluster even if some overlap”）与 **作者术语 cluster**（§3.5 / §7.1 terminology bias）这两条边界必须与统计一起迁移；混合型 LLM/agent assistant 不能机械套用单标签。

## 3. 原生样本编码维度树（维度森林）

下面是按本文 §3.5 + §4.2/§4.3/§4.4 + Table 2/3/4 + §5 实际还原的**原生编码 schema**（替代 review.md 当前那六叶通用接口主树）：

```text
[ROOT] MDSE modelling assistance landscape (Mosquera et al. 2024)
│
├── [B-meta] Study & corpus metadata (per-proposal record key)
│   ├── proposal_id            // [20]..[77]; 1 row per proposal
│   ├── source_track           // database_search | snowballing | external_reviewer_suggestion
│   ├── inclusion_criteria_pass // I1, I2 (boolean each)
│   ├── exclusion_criteria_trigger // E1..E5 (one or more)
│   ├── quality_score           // 3-point Likert × 10 items (Table 1)
│   ├── selected_as_snowball_seed // true if in top-12
│   └── kappa_basis             // for inclusion (0.634) and clustering (0.651)
│
├── [B-RQ1] Modelling assistance strategy (RQ1)
│   ├── strategy_cluster        // ENUM = {Tools, Guidelines, Techniques, Methods, Frameworks, Languages}  (single-label, §4.2)
│   ├── strategy_subtype        // free-text but author-keyword grounded
│   │   ├── Tools.subtype       // recommender_system | AI_software_assistant | bot | plugin | view_manager | modelling_env | VR_env | reactive_system | testing_tool | transformation_tool | collab_tool
│   │   ├── Guidelines.subtype  // ISO_standardisation | flexible_workflow | refactoring_process | multi_modelling_arch
│   │   ├── Techniques.subtype  // model_development | model_validation | model_repair
│   │   ├── Methods.subtype     // consistency_validation | model_repair | task_driven_reuse | MDE_alignment
│   │   ├── Frameworks.subtype  // change_propagation | testing | collaborative_modelling | co_evolution | formal | modelling_framework
│   │   └── Languages.subtype   // mega_modelling | UML_extension | modelling_template
│   ├── software_based_ratio    // {totally, partially, no}  (§4.2 末 93.1 % vs 6.9 %)
│   └── author_keyword_evidence // raw text fragment (per §3.5)
│
├── [B-RQ2-G] Goals (RQ2-G)
│   ├── goal_cluster            // ENUM = {G1 change propagation, G2 consistency checking, G3 model compatibility, G4 model quality, G5 user interaction, G6 model evolution, G7 vulnerability detection}
│   ├── create_refine_role      // ENUM = {create_only(G6), refine_only(G1/G2/G3/G4/G7), both(G5)}   (§4.3 三分)
│   └── goal_evidence_quote     // raw fragment
│
├── [B-RQ2-L] Limitations (RQ2-L)
│   ├── limitation_reporting_status // {specified, not_specified=L-NS}  (§4.3：50.0 % 报告)
│   ├── limitation_cluster      // ENUM = {L1 accuracy, L2 effort, L3 generality, L4 learnability, L5 scope, L6 usability}  ← **Table 3 列 6 类，§4.3 prose 写 “five clusters”，待复核**
│   └── limitation_evidence_quote
│
├── [B-RQ3-M] Evaluation metrics (RQ3-M)
│   ├── evaluation_status       // {empirically_evaluated, not_evaluated=NE}
│   ├── metric_cluster          // ENUM = {M1 effectiveness, M2 efficiency, M3 user perception}  (TAM-based, §4.4)
│   ├── metric_subtype          // M1: faults | F-measure | accuracy | recall | precision | success_score | accepted_suggestions | compression_factor | feasibility | stakeholder_participation | trace_collection | inconsistency_coverage | effectiveness
│   │                           // M2: modelling_time | completion_time | testing_gen_time | repair_gen_time | performance | computational_effort | recommendation_time | preprocessing_time | resource_import | execution_count_reduction | execution_time
│   │                           // M3: industrial_adoption_perception | perceived_usefulness
│   └── metric_evidence_quote
│
├── [B-RQ3-U] Target users (RQ3-U)
│   ├── user_reporting_status   // {specified, generic_user_hidden=U-NS}  (§4.4 explicit)
│   ├── user_cluster            // ENUM = {U1 designers/modellers, U2 domain experts, U3 software developers}
│   ├── user_subtype            // U1: software_designer | model_developer | engineer_with_design_exp | UML_developer | MDE_developer | student/novice_modeller
│   │                           // U2: business_analyst | end_user | domain_user | domain_expert | domain_engineer | business_user
│   │                           // U3: developer | software_developer | SE_student | software_maintainer
│   └── user_evidence_quote
│
├── [B-RQ4-practice] Practice-side projection (RQ4)
│   ├── tool_id                 // 17 GMQ tools
│   ├── gmq_class               // ENUM = {LE Leaders, C Challengers, V Visionaries, NP Niche Players}
│   ├── documentation_status    // ENUM = {D documented, NF not_found}   (10 NF / 7 D)
│   ├── practice_proposal_id    // 15 sub-proposals inside 7 D tools
│   ├── practice_strategy       // projected to RQ1 schema (predominantly Tools)
│   ├── practice_goal           // projected to RQ2-G (G6 most common)
│   ├── practice_limitation     // projected to RQ2-L (mostly NF, only L1/L3/L5 surfaced)
│   ├── practice_metric         // projected to RQ3-M (mostly NF, M3 absent)
│   ├── practice_user           // projected to RQ3-U (mostly U3, U1/U2 absent)
│   ├── second_person_hidden    // boolean: doc uses “you” to hide target user
│   └── doc_quote_anchor        // URL / user-guide section / whitepaper id (Table 5)
│
├── [B-cross] Cross-axis derivations (§6, Fig. 5/6/11/12/13)
│   ├── strategy × goal × limitation   // Fig. 11
│   ├── goal × metric × user           // Fig. 6 / Fig. 12
│   └── literature × practice          // Fig. 13
│
└── [B-validity] Validity threats (§7)
    ├── internal: selection_bias | extraction_bias | subjective_clustering | inter_rater (K=0.634/0.651) | reviewer_fatigue
    ├── construct: grey_literature_bias | search_bias
    └── external: language_bias (English only)
```

**取值空间类型速查：**

| 主干 | 树结构 | 取值空间类型 |
|---|---|---|
| B-meta | 每 proposal 一行 | 标识符 / 数值 / 布尔 |
| B-RQ1 strategy_cluster | 单标签 ENUM | 完整封闭枚举（6 类） |
| B-RQ1 strategy_subtype | 层级子枚举 | 层级枚举 + 自由文本 anchor |
| B-RQ2-G goal_cluster | 单标签 ENUM | 完整封闭枚举（7 类） |
| B-RQ2-G create_refine_role | 派生 ENUM | 3 类 |
| B-RQ2-L limitation_cluster | 单/多标签 ENUM | 封闭枚举（6 类，**与 prose 中“five”冲突，待核**）+ NS |
| B-RQ3-M metric_cluster | 单/多标签 ENUM | 封闭枚举（3 类） + NE |
| B-RQ3-M metric_subtype | 自由文本 grounded | 自由文本加 TAM 类型 |
| B-RQ3-U user_cluster | 单标签 ENUM | 封闭枚举（3 类）+ U-NS |
| B-RQ4 gmq_class | 单标签 ENUM | 封闭枚举（4 类） |
| B-RQ4 documentation_status | 布尔 ENUM | {D, NF} |
| B-cross | 关系值 | 二维 / 三维 bubble |
| B-validity | 自由文本加理由 | 分类 + 缓解 + 残余 |

**与 A1-DT v2 通用六叶接口的对应（仅作投影层，不是原文结构）：**

- `scope` → B-meta + §1 modelling assistance 定义；
- `corpus` → §3.2/§3.3/§3.4 + Fig. 3 + B-RQ4 GMQ 池；
- `taxonomy` → B-RQ1 / B-RQ2-G / B-RQ2-L / B-RQ3-M / B-RQ3-U（这是本文真正的 taxonomy 主体）；
- `method` → B-RQ1（strategy 是 method/tool/framework/language 的并集）；
- `evidence` → B-meta 的 QA、K-statistic、Zenodo replication、Table 5 quotes；
- `finding` → B-cross + §8 discussion 的“documentation gap” + “AI/LLM disruption” 候选。

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-strategy-cluster | 建模辅助策略 cluster | B-RQ1 | §3.5 RQ1 抽取规则 + §4.2 + Table 2 + Fig. 4 | 把每个 proposal 单标签归入 6 类作者术语 cluster 之一 | {Tools, Guidelines, Techniques, Methods, Frameworks, Languages} | 完整封闭枚举 | 不允许空；overlap 强制单标签（§4.2 末） | 频次 39.7/19.0/15.5/13.8/6.9/5.2 % | software-based 93.1 % 是候选 finding；混合系统外推风险 | E3, E7 | 单标签外推到 hybrid LLM/agent 系统须降级 |
| leaf-strategy-subtype | 策略子型 | leaf-strategy-cluster | §4.2 段落子列表 + Table 2 keywords | 在 cluster 内的作者术语子型 | 层级枚举（Tools 11+ 子型；其余每 cluster 3–6 子型） | 层级枚举 + 自由文本 | 子型未明时仅留 cluster | 子型分布尚未给出数字 | recommender / AI assistant 子型可对接 LLM4STM | E7 | 子型词表非饱和，A2a 待 Zenodo 核 |
| leaf-software-based | 软件实现程度 | B-RQ1 | §4.2 末 “93.1 %…software implementations” | 该 proposal 是否使用软件实现 | {totally_software, partially_software, no_software} | 派生 ENUM | 不允许空 | 93.1 % vs 6.9 % | 提示 guideline-only 占少数 | E7 | 直接迁移 |
| leaf-goal-cluster | 目标 cluster | B-RQ2-G | §3.5 + §4.3 + Table 3 + Fig. 5 | 单标签归入 7 类目标 | {G1, G2, G3, G4, G5, G6, G7} | 完整封闭枚举 | 不允许空 | G6=31.0 %、G1+G2+G3+G4+G7=43.1 %、G5=25.9 % | G6 对接 STM generation；G2/G5 对接 verification & repair | E3, E9 | G3/G7 单 proposal，统计稀疏 |
| leaf-create-refine-role | 创建/精化角色 | leaf-goal-cluster | §4.3 三分 | 派生：G6=create / G1-G4-G7=refine / G5=both | {create, refine, both} | 派生 ENUM（3 类） | 不允许空 | 31.0 / 43.1 / 25.9 % | 显示 refinement 主导，gap=纯创建少 | E9 | 直接迁移 |
| leaf-limitation-reporting | 限制是否报告 | B-RQ2-L | §3.5 “leave blank” + §4.3 L-NS | 50.0 % 明确报告 limitations | {specified, L-NS} | 布尔 | L-NS 即 not-reported（不是 not_applicable） | 50.0 % vs 50.0 % | missingness 本身=候选 finding | E9 | 直接迁移 |
| leaf-limitation-cluster | 限制 cluster | B-RQ2-L | Table 3 + §4.3 L1–L6 | 6 类限制（**§4.3 prose 写 “five”，待核**） | {L1 accuracy, L2 effort, L3 generality, L4 learnability, L5 scope, L6 usability} ∪ {L-NS} | 封闭枚举（带口径冲突待核） | L-NS=作者未声明 | 仅给出 L 子集的列表；具体每类频次未在 §4.3 完整给出 | L1/L3/L5 是 LLM4STM 主风险 | **E8 待复核** | 不允许把 “five” 直接当作权威；A2a 须复核 |
| leaf-evaluation-status | 是否经验评价 | B-RQ3-M | §4.4 NE 定义 | proposal 是否被经验评价 | {empirically_evaluated, NE} | 布尔 | NE=未评价 | NE=48.6 % | 评价缺口本身=候选 finding | E10 | 直接迁移 |
| leaf-metric-cluster | 指标 cluster | B-RQ3-M | Table 4 + §4.4 + TAM | 把指标按 TAM 分类 | {M1 effectiveness, M2 efficiency, M3 user perception} ∪ {NE} | 封闭枚举 | NE=未评价 | M1=23.6 %、M2=23.6 %、M3=4.2 %、NE=48.6 % | M3=4.2 % 是强 gap | E10 | 一 proposal 可有多 metric，注意多标签 |
| leaf-metric-subtype | 指标子型 | leaf-metric-cluster | Table 4 keywords | 在 cluster 内的具体指标项 | M1/M2/M3 子型枚举（见 §3） | 层级枚举 + 自由文本 | 缺则填 NE | 子型分布未数字化 | 直接对接 STM generation 评价 | E10 | 子型词表非饱和 |
| leaf-user-cluster | 目标用户 cluster | B-RQ3-U | §4.4 + Table 4 | 3 类 + 隐藏未报告 | {U1 designers/modellers, U2 domain experts, U3 software developers} ∪ {U-NS} | 封闭枚举 | U-NS=作者用 “user” / “he/she” 泛化或 second-person 隐藏 | U1=27.6 %、U2=13.8 %、U3=29.3 %、U-NS=29.3 % | U2 占比低是 LLM4STM domain expert 命题的起点 | E10, E11 | 直接迁移；practice 侧 U-NS 高度由 “you” 触发 |
| leaf-doc-status | 实践文档状态 | B-RQ4 | §5.2 + Fig. 9 | GMQ tool 是否有可访问的 modelling assistance documentation | {D documented, NF not_found} | 布尔 | NF≠工具缺失能力 | 10 NF / 7 D（58.8 % NF） | not-documented ≠ not-exists 是关键边界 | E11 | 直接迁移 |
| leaf-gmq-class | GMQ 分类 | B-RQ4 | §5.1 + Fig. 8 | Gartner Magic Quadrant 2023 分类 | {LE, C, V, NP} | 完整封闭枚举（4 类） | 不允许空 | LE=5, C=1, V=3, NP=8 | LE 更常公开 assistant 文档 | E11 | 仅代表 enterprise low-code 视角 |
| leaf-second-person-hidden | 第二人称隐藏用户 | leaf-doc-status | §5.2 末 “write using ‘you’… hides the actor” | 文档是否用 you 掩盖 target user | {true, false} | 布尔 | 不允许空 | 未数字化但 §5.2 显式声明常见 | LLM4STM 文档警示 | E11 | 直接迁移 |
| leaf-replication-link | 复现资料链接 | B-meta | §3.5 脚注 4 + §4.1 脚注 + §8 | Zenodo 10262145 | URL + 内容描述 | 链接 + 自由文本 | 不允许空 | n/a | 提升透明度证据 | E6 | 本审计未实际核验 |
| leaf-kappa-inclusion | 纳入 K-statistic | B-meta | §4.1 | 三 reviewer inter-rater | 数值 0–1 | 数值 | 不允许空 | K=0.634 | 处于 Landis-Koch substantial | E6 | 直接迁移 |
| leaf-kappa-clustering | 聚类 K-statistic | B-meta | §4.1 + §7.1 | 聚类 inter-rater | 数值 0–1 | 数值 | 不允许空 | K=0.651 | 同上 | E6 | 数据抽取阶段未算 K（§7.1） |

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-strategy-goal | leaf-strategy-cluster | 编码关联（per-proposal）| leaf-goal-cluster | 单标签 × 单标签 | 不允许空 | Fig. 5 + Fig. 11 + §6 | Tools↔G5/G6；Methods↔G2；Frameworks↔G1；用于 cross-axis 统计 |
| edge-strategy-limitation | leaf-strategy-cluster | 编码关联 | leaf-limitation-cluster | 单 × 单/多 + L-NS | L-NS 显式 | Fig. 5 + Fig. 11 | Tools↔L1/L5/L3；Frameworks↔L5；候选 finding 来源 |
| edge-goal-metric | leaf-goal-cluster | 编码关联 | leaf-metric-cluster | 单 × 单/多 + NE | NE 显式 | Fig. 6 + Fig. 12 | G6↔M1+M2；G5↔M2；G2↔M1 |
| edge-goal-user | leaf-goal-cluster | 编码关联 | leaf-user-cluster | 单 × 单 + U-NS | U-NS 显式 | Fig. 6 + Fig. 12 | G6↔U1+U3；G5↔U1；G1↔U3+U2；显示 domain expert 命题缺口 |
| edge-literature-practice | B-RQ1/2/3 (lit-side) | 投影关系（同 schema） | B-RQ4 (practice-side) | 同左 cluster × 同左 cluster | NF（practice 一侧专属） | Fig. 13 + §6 | 显示 practice 中 L2/L4/L5 缺失、U1/U2 缺失、M3 缺失 |
| edge-tool-proposal | leaf-gmq-class + tool_id | 包含 | practice_proposal_id | 1 tool → 0..n proposals | NF=0 | §5.2 + Table 5 | 7 tools 包含 15 proposals |
| edge-doc-strategy | leaf-doc-status | 仅在 D 下展开 | leaf-strategy-cluster (practice 投影) | 同 RQ1 ENUM | NF 直接终止链 | §5.2 “80 % strategies are tools” | not-documented 阻断后续编码 |
| edge-quality-snowball | leaf-quality-score | 选种关系 | leaf-replication-link / snowball seeds | top-12 阈值 | n/a | §3.4 + §4.1 | 显示 corpus 入口偏置 |

## 6. 统计观察、候选 finding 与 final finding 边界

**A. 由字段 / 表支持的统计观察（可统计、可作 schema-seed 主统计池候选）：**

1. 纳入分母：3,176 screened → 77 possible → 58 included；K(inclusion)=0.634；K(clustering)=0.651。（E6）
2. RQ1 strategy 分布：Tools 39.7 %、Frameworks 19.0 %、Techniques 15.5 %、Methods 13.8 %、Guidelines 6.9 %、Languages 5.2 %；software-based 93.1 %。（E7）
3. RQ2-G create/refine 三分：G6 create=31.0 %（18）、refine(G1+G2+G3+G4+G7)=43.1 %（25）、G5 both=25.9 %（15）。（E9）
4. RQ2-L reporting rate：50.0 % proposals 明确报告 limitations；L-NS=50.0 %。（E9）
5. RQ3-M：M1=23.6 %、M2=23.6 %、M3=4.2 %、NE=48.6 %。（E10）
6. RQ3-U：U1=27.6 %、U2=13.8 %、U3=29.3 %、U-NS=29.3 %。（E10）
7. RQ4 documentation status：NF=10/17=58.8 %、D=7/17=41.2 %；7 D 包含 15 practice proposals；practice strategy 80 % tool、goal 100 % 报告、limitation 报告 20 %、metric NF 73.3 %、user NF 73.3 %。（E11）
8. Cross-axis（Fig. 5/6/11/12/13）支持的成对关联：Tools↔G5/G6/L1/L3/L5；Methods↔G2；Frameworks↔G1/L5；G6↔U1+U3；G5↔U1；practice 中 L2/L4/L5、M3、U1/U2 缺失。（E7, E9, E10, E11, E12）

**B. 原文 discussion / conclusion / future work 中的候选 finding（不是字段统计的直接结论，必须作 candidate 处理）：**

1. “documentation about MDSE assistants’ limitations, evaluation metrics, and target users is scarce or non-existent”（abstract & §8）—— 由 #4–#7 支撑但仍是 author claim，迁移时需保留分母。
2. “software-based strategies dominate”（§4.2）—— 93.1 % 数值支撑，相对稳健。
3. “practice tools 中 not-documented ≠ not-exists”（§5.2 + §7.1）—— 是方法论级别 caveat，不是领域 finding。
4. “AI/LLM/GPT 将带来 disruptive 变化，需要 unified framework”（§8）—— **不是字段统计结论**，是 future expectation；在 review.md 与 SUMMARY 中只能写成 candidate，不能写成已验证。
5. “designers/modellers (U1) 与 domain experts (U2) 在 practice 中几乎缺席”（§6 / Fig. 13）—— 由 practice 73.3 % U-NS + “you” 隐藏支撑。
6. “user-perception metrics (M3) 4.2 %”是 evaluation 维度的强 gap（§4.4 + Fig. 13）。
7. proposed unified framework 应连接 IMA [103] 与 elicitation framework [81]（§8 future work）—— 仅 design implication，不进入领域 final finding。

**C. 对 Paper2 可迁移的方法学启发（不依赖 MDSE 领域真值）：**

1. 字段树 = RQ-extraction-schema-as-tree：把 RQ 直接当作主干、把抽取规则当作叶子；
2. 显式缺失语义（L-NS / NE / U-NS / NF）是一等字段，不是空值；
3. 单标签 cluster 风险 + 作者术语依赖（terminology bias）必须随 schema 一起迁移；
4. literature × practice 同一 schema 双投影 + “not-documented ≠ not-exists”；
5. inter-rater 在 inclusion + clustering 两个环节分别报告 K（数据抽取阶段未算 K，是已声明限制）；
6. cross-axis bubble chart 是“多字段联合”候选 finding 的图形化载体；
7. replication package（Zenodo）作为字段证据的最终源。

**D. 绝不能迁移的领域结论：**

1. 任何 RQ1–RQ4 中 MDSE 领域具体百分比、cluster 名、proposal id 不能直接外推到 LLM4STM / 控制系统状态机领域；
2. “Tools 39.7 %”等比例只在 MDSE-assistant 普通研究池成立；
3. “M3 4.2 %”不能直接用作 LLM4STM 的 evaluation gap 论据，只能作为方法学警示；
4. AI/LLM disruption 论述是 future work，不是已验证结果。

## 7. 对现有 `review.md` 的返修建议（C/I/M）

**C（critical，影响 A1-DT v2 事实源与统计池可信度）：**

- **C1**：当前 `review.md` 主结构（第 4 节“维度树复原 → 叶子维度表”那 6 行 `leaf-*-scope/corpus/taxonomy/method/evidence/finding`）把跨论文通用接口当成原文叶子全集，与本文真实 schema（strategy/goal/limitation/metric/user × 5 字段 × 6+7+6+3+3+NS/NE/NF cluster）严重不符。**返修**：把 §3 给出的 [B-RQ1] / [B-RQ2-G] / [B-RQ2-L] / [B-RQ3-M] / [B-RQ3-U] / [B-RQ4-practice] / [B-cross] / [B-validity] 抬升为正式主干叶子，把现有六叶降级为 §维度树复原 末尾的 “通用接口投影”小节（这部分目前虽然存在，但被压在 19×3 v1 旧框下，不是 v2 主结构）。
- **C2**：当前“原文模式候选叶子映射（A1 种子）”表只列了 5 个高粒度种子（strategy / goal / artifact / metric-user / limitation），且全部 `not_verified`；但原文 Table 2/3/4 已经显式给出**完整封闭枚举 + 频次**，应直接升级为已核验枚举（仅 `leaf-limitation-cluster` 因 §4.3 prose “five” vs Table 3 “L1–L6” 冲突保留 `not_verified`），不能继续整体停留在 `schema_seed`。
- **C3**：当前 SUMMARY 或 A.3 中“样本单位 / 样本数量 / 原生树类型 / 统计池资格”应改为：原生树类型=**维度森林**、样本单位=**proposal + tool**（双层）、样本数=58 + 17/15、主统计池资格=**局部可统计 schema-seed**（不是当前的 `否（A1-DT 阶段仅作 schema seed）`，因为 Table 2–4 已给出原文 closed-enum + 比例 + K）。

**I（important，影响证据链可读性与下游 schema 迁移）：**

- **I1**：§4.3 文中 “five limitation clusters” 与 Table 3 “L1–L6” 的口径冲突应在 A.2 中作为单独 evidence 行登记（建议 `EV-mdse-modelling-assistants-mapping-006`），强度=`not_verified`，并列入 A2a 必须 PDF + Zenodo 复核任务。
- **I2**：当前 A.2 把 5 条 evidence 全部标 `not_verified`，但 §3.5 / §4.1 / §4.2 / §4.4 / §5.2 文本级证据强度应至少升级为 `text_verified`（仅图表数字、bubble 半径与 §4.3 limitation count 保持 `not_verified`）。否则 A.3 推不出任何 `schema_seed` 以上的结论。
- **I3**：缺失语义编码 `L-NS / NE / U-NS / NF` 是本文一等字段，应在叶子维度表中单独列出，而非合并在叶子定义里；当前 review.md 把它们隐入 `not_specified` 自由文本，下游 schema 迁移容易丢。
- **I4**：当前 A.2 / A.3 没有为 [B-cross]（Fig. 5/6/11/12/13）建独立证据行；§6 cross-axis 是本文 finding 的主要来源，必须有专属 evidence + 关系边 claim。
- **I5**：当前 SUMMARY 表“样本数量 / 分母 = 58 proposals / 3,176 records / 17 tools”应改为“proposals=58 / practice_tools=17（D=7 / NF=10）/ practice_proposals=15 / records_screened=3,176 / K_inclusion=0.634 / K_clustering=0.651”，把 K 一并显化。
- **I6**：当前“可迁移与不可迁移边界”表把“具体领域结论”整体禁止迁移是对的，但应额外明确禁止把 `M3=4.2 %` 类指标直接当 LLM4STM gap 论据，只允许作方法学警示。

**M（minor，可后续顺手清理）：**

- **M1**：当前“历史草稿（已迁移，不作事实真源）”两节占 80+ 行，建议折叠到附录或文末 history 区，避免新 reviewer 误读为当前事实。
- **M2**：emoji 列（如 `🟢` 等口径）不出现在本 review.md，但 `[clm-*]` 引用键格式偶有空格不一致，建议统一。
- **M3**：将 Zenodo `10262145` 与 GMQ 2023 URL 在 A.1 中作为独立 src 行登记，便于 A2a 自动化抓取。
- **M4**：CCF 等级、IST OA 状态、`paper.pdf` 视觉核验是否完成，建议在 0 卡片末单独列“尚未做的最小动作清单”，避免 reviewer 误以为已完成。

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案（中文表头）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-mma-001 | paper_content.txt, bibtex.bib | §1 Introduction（Page 1）+ Abstract | abstract; “Modelling assistance is the strategy…that aims to assist humans during software modelling tasks in MDSE tools.” | 给出 modelling assistance 定义和 MDSE/低代码边界 | scope_definition | text_verified | B-meta, ROOT, leaf-strategy-cluster | 否 | 仅本文 scope；不外推 LLM4STM 领域 |
| EV-mma-002 | paper_content.txt | §3.1 RQ1/RQ2/RQ3（Page 3–4） + §3.5 extraction rules（Page 4–5） | RQ 表述与“Extract the keywords…leave the field blank…” | RQ 即字段树主干；缺失语义=显式留空 | rq_and_extraction_schema | text_verified | B-RQ1, B-RQ2-G, B-RQ2-L, B-RQ3-M, B-RQ3-U, leaf-limitation-reporting, leaf-evaluation-status, leaf-user-reporting | 否（仅 Zenodo raw form 待核） | 直接迁移结构，不迁移领域结论 |
| EV-mma-003 | paper_content.txt | §3.2/§3.3/§3.4/§4.1 + Fig. 3 PRISMA（Page 3–6） | 1,996+5 → 51 → top12 seeds → 1,175 snowball → 3,176 → 77 → 58；K=0.634/0.651 | corpus pipeline + inter-rater | corpus_pipeline | text_verified（图 3 视觉待核） | leaf-quality-score, leaf-kappa-inclusion, leaf-kappa-clustering, leaf-replication-link, B-meta | true（Fig. 3 视觉） | 仅本文样本池 |
| EV-mma-004 | paper_content.txt | §4.2 + Table 2 + Fig. 4（Page 6–7） | 6 cluster + 比例 + 93.1 % software-based | taxonomy_with_distribution | text_verified（图 4 数字待核） | leaf-strategy-cluster, leaf-strategy-subtype, leaf-software-based | true（Fig. 4 视觉） | 单标签 cluster 风险 |
| EV-mma-005 | paper_content.txt | §4.3 + Table 3 + Fig. 5（Page 7–9） | 7 G clusters + “five limitation clusters”（prose）/ Table 3 列 L1–L6 + L-NS | taxonomy + 口径冲突 | text_verified_with_internal_conflict | leaf-goal-cluster, leaf-create-refine-role, leaf-limitation-reporting, leaf-limitation-cluster | true（§4.3 prose vs Table 3） | **A2a 必须复核 PDF / Zenodo**，否则 L 总数不可信 |
| EV-mma-006 | paper_content.txt | §4.4 + Table 4 + Fig. 6（Page 9–10） | 3 M + 3 U + NE/U-NS + 频次 | taxonomy + missingness | text_verified（图 6 数字待核） | leaf-evaluation-status, leaf-metric-cluster, leaf-metric-subtype, leaf-user-cluster | true（Fig. 6 视觉） | 一 proposal 可多 metric，注意多标签 |
| EV-mma-007 | paper_content.txt | §5.1/§5.2 + Table 5 + Fig. 8/9/10（Page 10–13） | 17 GMQ tools → 10 NF + 7 D → 15 proposals；“you” 隐藏 user | practice_projection + missingness | text_verified（Fig. 9/10 视觉与 vendor URL 待核） | B-RQ4-practice, leaf-doc-status, leaf-gmq-class, leaf-second-person-hidden | true | grey-literature 局限于 GMQ；vendor URL 当前状态未复核 |
| EV-mma-008 | paper_content.txt | §6 + Fig. 11/12/13（Page 13–14） | strategy×goal×limitation；goal×metric×user；lit vs practice | cross_axis_relations | text_verified（bubble 视觉待核） | edge-strategy-goal, edge-strategy-limitation, edge-goal-metric, edge-goal-user, edge-literature-practice | true | bubble 半径 = 计数，单 proposal 单 cluster |
| EV-mma-009 | paper_content.txt | §7.1–§7.3（Page 15） | selection / extraction / subjective interpretation / inter-rater / grey literature / search / language bias | validity_threats | text_verified | B-validity, terminology_basis | 否 | 缓解 ≠ 消除；data extraction K 未算 |
| EV-mma-010 | paper_content.txt | §8（Page 15–17） + Fig. 14/15 | future framework + AI/LLM disruption + Zenodo 10262145 | future_work_candidate_finding | text_verified（视觉待核） | candidate findings (B/C/D) | true | AI/LLM disruption=expectation，不是结果 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-mma-01 | 本文真正的 A1-DT 维度森林由 5 字段树（strategy / goal / limitation / metric / user）+ practice 投影 + cross-axis 关系 + validity 组成；不是六叶通用接口。 | tree_type | ROOT, B-RQ1..4, B-cross, B-validity | EV-mma-002, 004, 005, 006, 007, 008 | strong（schema 级） | review.md 主结构、SUMMARY 行 | 单标签 cluster + 作者术语 cluster 必须随用 |
| C-mma-02 | 样本单位是 proposal（n=58）+ tool（n=17，含 15 practice proposals）的双层 schema；分母与 K 都已显化。 | sampling_unit | B-meta, B-RQ4 | EV-mma-003, 007 | strong | SUMMARY、统计池资格 | grey-literature 仅限 GMQ |
| C-mma-03 | RQ1 strategy 是完整封闭 6-cluster 单标签编码；93.1 % software-based。 | closed_enum + distribution | leaf-strategy-cluster, leaf-software-based | EV-mma-004 | strong | 可作 schema-seed 统计 | 单标签压扁混合系统 |
| C-mma-04 | RQ2-G 是完整封闭 7-cluster 单标签编码；可派生 create/refine 三分（31.0/43.1/25.9 %）。 | closed_enum + derived | leaf-goal-cluster, leaf-create-refine-role | EV-mma-005 | strong | 可作 schema-seed 统计 | G3/G7 单 proposal 稀疏 |
| C-mma-05 | RQ2-L cluster 总数在原文内部存在 “five (§4.3 prose)” vs “L1–L6 (Table 3)” 冲突，必须保留 `not_verified` 直到 A2a 复核。 | internal_inconsistency | leaf-limitation-cluster | EV-mma-005 | weak | 候选 finding 不可作 final | 必须 A2a PDF + Zenodo 复核 |
| C-mma-06 | RQ3-M cluster 是 3-cluster TAM-based 单/多标签；M3=4.2 %、NE=48.6 % 是显式 evaluation gap。 | closed_enum + missingness | leaf-evaluation-status, leaf-metric-cluster | EV-mma-006 | strong | 可作 schema-seed 统计；可作方法学警示 | 不可直接外推 LLM4STM gap 数字 |
| C-mma-07 | RQ3-U cluster 是 3-cluster 单标签 + U-NS；U-NS=29.3 %、practice 73.3 %；practice U-NS 由 “you” 触发是 §5.2 显式机制。 | closed_enum + missingness + mechanism | leaf-user-cluster, leaf-user-reporting, leaf-second-person-hidden | EV-mma-006, 007 | strong | 可作 schema-seed 统计 | 不外推领域比例 |
| C-mma-08 | not-documented ≠ not-exists（GMQ 中 10/17 NF 不能等同“工具没有 assistant”）。 | methodological_caveat | leaf-doc-status, B-validity | EV-mma-007, 009 | strong | 直接迁移到 Paper2 / Project1 | grey-literature 局限 |
| C-mma-09 | AI/LLM disruption 与 unified framework 论述是 future expectation，不是字段统计的 final finding。 | candidate_finding | §8 论述 | EV-mma-010 | weak | review.md / SUMMARY 只能写 candidate | 与原文 RQ 抽取数据不直接挂钩 |
| C-mma-10 | cross-axis（strategy×goal×limitation；goal×metric×user；lit vs practice）是本文 finding 的主要候选来源，但需 PDF 复核 bubble 半径数字。 | relation_finding | edge-* | EV-mma-008 | medium | 可作 candidate finding | bubble 数字 PDF 待核 |
| C-mma-11 | terminology bias + subjective clustering + data extraction K 未算 + grey literature limited to GMQ + English-only：5 条 validity 边界必须随 schema 一起迁移。 | migration_boundary | B-validity | EV-mma-009 | strong | review.md 迁移边界 + Paper2 启发 | 缓解不等于消除 |

## 9. 技能使用与自我审查记录

**已读技能 / 指南文件与采纳原则：**

1. `ai-research-writing-skill/SKILL.md` —— 采纳 “claim-evidence-engineering” + “evidence gate / story gate / citation gate”：每个 leaf / claim 必须挂证据锚点（EV-mma-001..010），不写无证据的强 finding；§4.3 内部冲突 → 显式标 `not_verified`，不脑补。
2. `ai-research-writing-skill/references/reviewer-guidelines.md` —— 采纳“constructive specificity”：返修建议 C/I/M 每条指定文件位置（review.md 哪一节、哪一表）+ 期望行为 + 实际行为差异。
3. `ai-research-writing-skill/references/reviewer-self-review.md` —— 采纳“Five-Dimension Review + Reviewer-Review Simulation”，并把它转成本审计末尾的“最高风险 3 点”。
4. `research-planning/SKILL.md` —— 采纳“先理解上下文 → 再生成 plan”的步骤约束，先读 schema 三件套再读论文。
5. `research-planning/references/planning-prompts.md` —— Paper2Code 4-turn 模板让我先做“overall scope 判定 → architecture（维度树） → logic（叶子+关系边） → configuration（取值空间/缺失/统计）”而不是一次性堆。
6. `research-planning/references/output-schemas.md` —— JSON schema 提示我把维度树以可序列化方式列出（叶子表 + 关系边表）。
7. `autoresearch/SKILL.md` —— 提醒本任务是 artifact-gated 单步审计，不进入 stateful loop；本输出本身即为完成 artifact，无需 nudge。

**Reviewer 自审：本输出最高风险的 3 点 + 主线程合并复核办法：**

1. **§4.3 limitation 口径冲突可能让下游错把 6 当作权威**。主线程合并 review.md 时，必须把 `leaf-limitation-cluster` 与 EV-mma-005 同时标 `not_verified`，并在 SUMMARY 中给 “limitations cluster 数 5 或 6 待核” 留显式 risk 条目；A2a 必须打开 PDF Table 3 + Zenodo raw CSV 双源核对。
2. **图表数字（Fig. 4/5/6/11/12/13）未做 PDF 视觉核验**。所有 cross-axis edge claim（C-mma-10）目前都基于 §6 文本叙述，bubble 半径未复核；合并时应保留 `needs_visual_check`，不要把 §6 中 “Tools↔G5/G6”、“Frameworks↔L5”、“G6↔U1+U3” 等关系直接升级为 strong。
3. **现有 review.md 历史草稿与 19×3 旧表与本 v2 审计存在叙事冲突**。合并时必须显式把旧 v1 主树 + 旧 19×3 主树降级为“历史草稿（已迁移）”小节，把本审计 §3 的维度森林作为唯一事实源；否则下游 paper2 reviewer 会同时看到三套相互矛盾的“原文 schema”。

**blocked / timeout / 文件缺失：**

- 无 `blocked`：所有要求阅读的技能文件、bibtex.bib、metadata.json、paper_content.txt、review.md 均成功本地读取。
- 未访问：`paper.pdf` 未在本审计中打开（按硬约束 5 仅“必要时”才核对，且不允许 subagent；图表视觉核验留 A2a）；Zenodo `10262145` replication package 未访问（不在硬约束允许的本地材料范围内）。
- 无 timeout。

---

报告结束。本审计为自包含完整报告；A1-DT v2 维度森林、叶子表、关系边表、证据账本草案与结论映射草案均已落到本回答正文，主线程可直接据此重写 `review.md` 的“维度树复原 / 叶子维度表 / 关系边表 / A.1–A.4 审计附录”节，无需再回到上一条消息或工具调用结果。
