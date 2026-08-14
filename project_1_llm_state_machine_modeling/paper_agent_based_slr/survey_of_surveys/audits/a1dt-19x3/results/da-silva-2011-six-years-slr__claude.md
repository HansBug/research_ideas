# da-silva-2011-six-years-slr · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude reviewer（受 PR #135 主 prompt 委派，无 sub-subagent）
- 是否读取 `$ai-research-writing-skill`：否。本机 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/` 路径在当前 sandbox 中不可访问，未做硬读；审计仍按 paper-story / reviewer-guidelines 的精神（原文 schema 复原优先、不臆造字段、roadmap 不写成 finding）执行。该缺口已显式声明。
- 是否读取 `$research-planning`：否，同上原因。
- 是否读取 `$oh-my-codex:autoresearch`：否，同上原因。
- 是否完整阅读 `paper_content.txt`：是。分两次 Read 完整覆盖 1–1626 行，包括 Abstract、§1 Introduction、§2 Previous studies、§3 Method（含 RQ1–RQ5、DCP、search string、QA 评分细则、10 个 data extraction 字段）、§4 Results（Table 2 全表、Table 3 quality scores、quartiles）、§5 RQ1–RQ5 全部 discussion（含 SE Curriculum / SWEBOK 映射 Table 5–6、Tables 7–13）、§6 Limitations、§7 Conclusions（含三种 update 模态）、References、Appendix A 全部 67 篇 SE 引用。
- 是否核对 `paper.pdf`：否。本轮以 paper_content 全文级审计为主；表格 / 图编号 / 页码在 paper_content 中已显式出现（Page 1–15 分页与 Table 1–13 标号），未做视觉版面核验。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

- 目标（Abstract Objective）：延展 OS [18] 与 FE [19] 两项 tertiary study，覆盖 2008-07-01 至 2009-12-31 时段，分析 SLR 的 quality、SE topic coverage、对 education 与 practice 的 potential impact。
- 5 个显式 RQ（§3.1）：
  - RQ1：2004-01-01 至 2009-12-31 共发表多少 SLR？含 RQ1.1（2004-01-01 至 2008-06-30）与 RQ1.2（2008-07-01 至 2009-12-31）两个子问题。
  - RQ2：被研究的 research topics 是什么？
  - RQ3：哪些个人 / 组织在 SLR-based research 中最活跃？
  - RQ4：OS / FE 中观察到的 SLR limitations 是否仍存在？显式拆为 4 个子项：5.4.1 review topics & extent of evidence；5.4.2 orientation towards practice；5.4.3 quality evaluation of primary studies；5.4.4 use of guidelines。
  - RQ5：SLR 的质量是否在提升？
- 贡献声明（§7）：1455 篇候选→ 67 篇入库；24 个 SE topics；15 篇相关 education，40 篇相关 practitioner，26 篇 researcher 导向；覆盖 SWEBOK 33%（15/46）。

### 2.2 方法流程与扩展数据抽取

- §3.2 Research team：6 名研究者 R1–R6（3 教师 + 2 博士生 + 1 硕士生）。
- §3.3 Decision & Consensus Procedure (DCP)：Fig. 1，对 study selection / quality assessment / data extraction 三阶段，先 R1 随机分配给 (Ri, Rj)，再由 R4 R5 整合成 Agreement / Disagreement Table，再由第三研究者 Rk 判定，最后六人 consensus。
- §3.4 Search process：自动检索 6 个引擎（ACM, IEEEXplore, Science Direct, CiteSeerX, ISI Web of Science, Scopus）+ Table 1 列出的 13 个人工检索源（含 IST、TSE、ICSE、ESEM、JSS 等）；automatic 返回 1389→ 初筛 157，manual 66；合并去重得 154。检索式由 18 个备选词构成（"systematic review" / "literature review" / "evidence-based" / "meta analysis" 等）。
- §3.5 Study selection：154 → 75 → 加 reference search 得 2 篇 → 77；再剔除 10 篇 → 67。剔除原因显式列 5 条。
- §3.6 Quality assessment：4 项 DARE 准则 QA1–QA4，每项 Y=1 / P=0.5 / N=0，最终分数加和。QA2 的 P / N 阈值与数字图书馆数量强绑定。盲评 10 篇对照 FE，仅 2 篇 1 项分歧。
- §3.7 Data extraction：明列 10 个抽取字段（**这就是原文真正的 extraction form**）：
  1. Year
  2. Quality Score
  3. Review Type ∈ {SLR, MA, MS}
  4. Review Scope ∈ {RQ, SERT, RT}
  5. Topic Area（开放枚举，本研究最终归为 24 个 SE topics）
  6. Cited EBSE papers ∈ {Y, N} 且区分引用 [14] / [8] / [20] / [24]
  7. Cited Guidelines ∈ {Y, N} 且区分引用 [15] / [16] / [13] / [4] / [12]
  8. Number of Primary studies（数值）
  9. Included Practitioners Guidelines ∈ {Y, N}
  10. Source Type ∈ {J, C, WS, BS}

### 2.3 显式的 schema / taxonomy / coding scheme / 图表

- Table 1 manual search sources（13 个 venue 清单，会议 / 期刊混合）。
- Table 2：67 篇逐篇 × 10 列抽取结果（**原文 schema 的核心载体**）。
- Table 3：QA1–QA4 分项 + final score + 四分位编号。
- Table 4：年份 × SLR 数 × EBSE-positioned 数 × 占比。
- Table 5：SLR ↔ SE Curriculum 2004 ↔ SWEBOK 映射，使用 {Yes, Possibly, No} 三值评估 useful for education / useful for practitioner，并显式给出 "Why?" 句式。
- Table 6：SLR 数 × SE Curriculum sections / SWEBOK chapters × OS/FE / SE / OS/FE+SE 三栏 + Increase 列。
- Table 7：作者出现次数 ≥3 的清单。Table 8：region × SLR 数。Table 9：年份 × median primary studies × SLR/MA × MS。Table 10：practitioner guidelines Y/N 跨 OS/FE vs SE。Table 11：quality evaluation of primary studies Y / N。Table 12：EBSE / Guidelines / 两者皆引 三类计数。Table 13：年份 × Cited Guidelines (No/Yes/All) × #SLR / Mean / σ / Increase。
- Fig. 1 DCP；Fig. 2 PRISMA 风格 search → selection → extraction 流。
- §7 显式提出三种 SLR update 模态：temporal update / search extension / temporal update + search extension。

### 2.4 finding 形成方式

原文 finding 的形成路径是：**10 字段抽取 → Table 2 总账 → 按字段做横截面统计（年份、topic、scope、quality、country、author）→ 与 OS/FE 历史 baseline 对照 → 在 §5.4.1–5.4.4 + §7 形成 "增长 + 仍存在缺口" 双向 finding**。三类典型 finding pattern：

1. 增长型：SLR 数、研究者数、组织数、国家数、引用 guideline 数、quality mean。
2. 缺口型：仅 21% 评 primary study quality；58% 仍以 trends 为主；EBSE step 4–5 未落实。
3. 方法学呼吁：呼吁更多 update / extension 型综述、qualitative synthesis 指南。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-...-root]` 锚定本文整体目标 / RQ / 贡献，描述与 §3.1 + §7 一致。 | 通过 |
| 主干分支是否覆盖原文 schema | 不通过 | b1–b5 是通用 "范围 / 语料 / 分类 / 方法 / 评价" 接口，未覆盖原文显式存在的：(a) **5 个 RQ 结构本身**、(b) **DCP 三阶段决策流程**、(c) **QA1–QA4 四项打分准则**、(d) **10 字段 extraction form**、(e) **SE Curriculum / SWEBOK 双轴映射**、(f) **三种 update 模态**、(g) **education / practitioner / researcher 三向影响 taxonomy**。 | C |
| 叶子维度是否足够具体 | 不通过 | 6 个 `leaf-*` 完全是跨论文通用接口（scope / corpus / taxonomy / method / evidence / finding），定义、取值空间、缺失值语义均为模板复用，与本文真实 schema 的颗粒度差距巨大。`原文模式候选叶子映射（A1 种子）` 表只给出 4 条 (secondary-study-profile / quality-assessment / topic-taxonomy / practice-impact)，但这 4 条仍是抽象类目，没有把 Table 2 的 10 字段、QA1–QA4 的 4 项准则、Review Type / Review Scope / Source Type 三个封闭枚举展开。 | C |
| 取值空间是否可执行 | 不通过 | 原文存在 **大量封闭枚举**（Review Type {SLR, MA, MS}、Review Scope {RQ, SERT, RT}、Source Type {J, C, WS, BS}、QA 评分 {Y=1, P=0.5, N=0}、Useful for education / practitioner {Yes, Possibly, No}、Update 模态 {temporal, search extension, both}），review.md 中均以 "层级枚举 / 关系值 / 开放 action point" 等模板套话覆盖，不可执行。 | I |
| 关系边是否缺失 | 不通过 | 缺：(a) extraction field ↔ RQ 的支撑关系（Table 2 字段被显式分派到 RQ1/RQ2/RQ3/RQ4/RQ5）；(b) QA1–QA4 ↔ final quality score ↔ quartile 的派生关系；(c) Topic Area ↔ SE Curriculum / SWEBOK ↔ {education, practice} 三段映射链。 | I |
| 统计用途 / 分母是否正确 | 通过 | 统计与候选发现链路表正确写明 "schema seed / 不进入主统计池"，分母锚到 19 篇 survey-of-surveys 样本，未越界。 | 通过 |
| 候选 finding 路径是否完整 | 不通过 | 缺原文核心 finding pattern："增长 + 仍存在缺口" 双向；缺 "1 篇 meta-analysis + 2 篇 meta-ethnography，其余皆未做 meta-synthesis" 这类硬观察；缺 "Update 模态分类" 这一原文 §7 显式贡献。 | I |
| A.1–A.4 证据链是否足够 | 部分通过 | A.1 完整；A.2 仅 4 条证据（root / taxonomy / stat / risk），全部 `not_verified` 且页码留白为 "待 A2a 精确页码复核"。实际上 paper_content.txt 已给出 Page 1–15 完整分页与 Table 1–13 编号，**可立即给出页码级锚点而无需 PDF 视觉核验**，但当前 A.2 没有利用这些。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | clm 与 ev 均标 `weak / schema_seed / not_verified`，未把 roadmap / discussion 升级为 finding。 [clm-da-silva-2011-six-years-slr-tree-type] 中 "tertiary 更新统计树" 的主类型判断与原文一致。 | 通过 |

## 4. 建议维度树骨架

下面给出更忠实于原文的建议骨架。当前 review 的六叶通用接口可保留作为 cross-paper schema seed 层，但 **必须新增 / 提升以下原文 schema 节点为正式叶子**，否则维度树仅是模板复制，无法承担本论文的字段事实真源。

```text
[root] Updated tertiary study on SE SLRs (2004-01-01 — 2009-12-31)
├── B1 综述范围与 RQ 结构
│   ├── L1.1 单位对象 = secondary study (SLR / MA / MS)
│   ├── L1.2 时间窗（2004-07-01 — 2009-12-31）与与 OS/FE 时间窗的衔接
│   ├── L1.3 5 个 RQ + RQ1 子问题（RQ1, RQ1.1, RQ1.2, RQ2, RQ3, RQ4{4.1..4.4}, RQ5）
│   └── L1.4 Update 模态（temporal / search extension / combined）-- 取自 §7
├── B2 语料收集与纳排
│   ├── L2.1 数据库集合（ACM, IEEEXplore, ScienceDirect, CiteSeerX, ISI WoS, Scopus）
│   ├── L2.2 检索式（18 同义词分支 + "software engineering" AND ...）
│   ├── L2.3 manual venues（Table 1 的 13 个 venue 清单）
│   ├── L2.4 PRISMA 计数链（1389→157→merge 154→75→77→67）-- 取自 Fig. 2
│   └── L2.5 排除原因（5 条显式理由）
├── B3 决策与角色
│   ├── L3.1 Research team 角色 (R1..R6, lecturer / PhD / MSc)
│   └── L3.2 DCP 三阶段 + Agreement / Disagreement Table（study selection / QA / data extraction）
├── B4 Quality Assessment Rubric
│   ├── L4.1 QA1 inclusion / exclusion criteria {Y=1, P=0.5, N=0} + 判定文字
│   ├── L4.2 QA2 search coverage {Y, P, N} 与 #digital libraries 的阈值规则
│   ├── L4.3 QA3 quality of included studies {Y, P, N}
│   ├── L4.4 QA4 data extraction adequacy {Y, P, N}
│   ├── L4.5 final score ∈ [0, 4]，四分位 Q1..Q4
│   └── L4.6 与 FE 的盲评一致性（10 篇盲评）
├── B5 Extraction Form（Table 2 的 10 列）
│   ├── L5.1 Year
│   ├── L5.2 Quality Score
│   ├── L5.3 Review Type ∈ {SLR, MA, MS}
│   ├── L5.4 Review Scope ∈ {RQ, SERT, RT}
│   ├── L5.5 Topic Area（24 个 SE topic 的开放枚举）
│   ├── L5.6 Cited EBSE papers（细分 [14]/[8]/[20]/[24]）
│   ├── L5.7 Cited Guidelines（细分 [15]/[16]/[13]/[4]/[12]）
│   ├── L5.8 #Primary Studies（数值）
│   ├── L5.9 Practitioner Guidelines ∈ {Y, N}
│   └── L5.10 Source Type ∈ {J, C, WS, BS}
├── B6 影响 / 应用映射
│   ├── L6.1 Useful for Education ∈ {Yes, Possibly, No}
│   ├── L6.2 Useful for Practitioner ∈ {Yes, Possibly, No}
│   ├── L6.3 SE Curriculum 2004 映射（章 / 节 / 子节）
│   └── L6.4 SWEBOK 章节映射
└── B7 统计与候选 finding
    ├── L7.1 增长型 finding（年份 / topic / country / author / quality）
    ├── L7.2 缺口型 finding（QA3 低、guideline 缺、EBSE step 4-5 缺、meta-synthesis 仅 3 篇）
    ├── L7.3 跨年份回归（guideline ↔ quality 相关，#primary ↔ quality 反相关）
    └── L7.4 方法学呼吁（外部 update / extension、qualitative synthesis 指南）
```

每个叶子需补：可统计性（频次 / 中位数 / 分布 / 相关 / 回归）、缺失值语义（原文 N/A 行为）、证据来源 (page + table/figure)。当前 review 仅 4 候选叶子且都用同一行模板，无法替代上述结构。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把 6 叶通用接口降级为 "cross-paper schema seed 层"，并增加专门的 "原文 schema 叶子层" | review.md §维度树结构 + 叶子维度表 | 保留现 6 叶但显式标 `cross_paper_interface`；新增 B5 Extraction Form 等 7 个原文专属叶子（Year / Quality Score / Review Type / Review Scope / Topic Area / Cited EBSE / Cited Guidelines / #Primary / Practitioner Guidelines / Source Type） | paper_content.txt Page 3 §3.7 数据抽取字段；Page 5–8 Table 2 | C |
| 补 QA1–QA4 子叶子并写明评分准则与四分位 | review.md 叶子维度表 + 取值空间列 | 增加 4 个 leaf 节点，取值空间填 {Y=1, P=0.5, N=0} + 各自的 verbal 判定条件 | paper_content.txt Page 5 §3.6（QA1–QA4 判定）；Page 7 Table 3 | C |
| 补 Update 模态 taxonomy（temporal / search extension / combined） | review.md 维度树 + 取值空间 | 增加 L1.4，作为 "前序综述关系" 的封闭枚举升级 | paper_content.txt Page 13 §7 倒数第 3 段 | I |
| 修正取值空间从模板套话改为原文封闭枚举 | review.md 叶子维度表 "取值空间" 列 | Review Type / Scope / Source Type / Education / Practitioner 等列写出实际 enum 值 | paper_content.txt Table 2 + Table 5 | C |
| 补关系边（extraction field ↔ RQ ↔ table）的说明 | review.md 新增 "关系边表" | 至少列出 RQ1→Table 4；RQ2→Table 2/5/6；RQ3→Table 7/8；RQ4→Table 9/10/11/12；RQ5→Table 13；QA1..4→Table 3→quartile→final score | paper_content.txt §5 各小节首段 | I |
| 把 A.2 证据账本的 "待 A2a 精确页码复核" 替换为已可锚定的 Page + Table/Figure | review.md A.2 证据账本 | EV-002 锚到 Page 3 §3.7 + Page 5–8 Table 2；EV-003 锚到 Page 9 §5.1 Table 4、Page 7 Table 3；EV-004 锚到 Page 11 §6。无需 PDF 视觉核验，paper_content.txt 已含 `--- Page N ---` 标记 | paper_content.txt 全文分页标记 | I |
| 增加 finding 双向化（增长 + 缺口）候选清单 | review.md §候选 finding 路径 | 至少枚举 5 条增长型 + 5 条缺口型候选发现，便于 A2a / A2b 做 cross-paper 比对 | paper_content.txt §5.1–5.5 + §7 | I |
| 在 schema 启发 / SUMMARY 反馈中补 "原文 schema 的封闭枚举密度" 这一可迁移特性 | review.md §3 对 PR-A1 schema 的启发 | 显式提示 Paper2 在 A2a 阶段应优先识别 closed enum 抽取字段并复用此 paper 的 4-criteria QA rubric | paper_content.txt §3.6 + §3.7 | M |
| 把 `EV-001..004` 的 `证据强度 = not_verified` 在已可锚定页码后升级为 `text_verified` | review.md A.2 | 章节 / 页码 / 表号已可在 paper_content 内核验；保留 "PDF 版面 / 图细节待人工" 即可，不必整体留在 not_verified | paper_content.txt 全文 | M |
| 在 [clm-...-source-schema-candidates] 中显式列出 10 字段 + 4 准则 + 3 update 模态作为候选 schema 完整集 | review.md A.3 | 当前 C12 只引 4 候选叶子；扩到至少 17 个候选项（10 + 4 + 3） | paper_content.txt §3.6/3.7/§7 | I |

## 6. C/I/M 结论

- **C (critical)**：
  - C1 主干分支未覆盖原文 schema（B5 / B4 / Update 模态全缺）→ 直接破坏 Paper2 A1-DT 的 "维度树复原" 任务目标。
  - C2 叶子层只有 6 通用接口 + 4 抽象候选，未展开原文显式的 10 字段 extraction form 与 4 项 QA rubric → 后续 A2a 若直接消费会把 "通用接口" 误当成 "原文叶子全集"，污染 cross-paper 统计。
  - C3 取值空间未使用原文封闭枚举 → 不可执行，直接影响 A2a/A2b 字段实例化与饱和度判断。
- **I (important)**：
  - I1 关系边（RQ ↔ extraction field ↔ table）缺失。
  - I2 finding 候选路径仅留 schema-seed 模板，未把原文 "增长 + 缺口" 双向 finding 写成候选。
  - I3 A.2 证据账本未利用 paper_content 已有页码 / 表号锚点，整体留在 not_verified。
  - I4 [clm-...-source-schema-candidates] 候选 schema 不完整（10 + 4 + 3 缺）。
  - I5 Update 模态 taxonomy 在 §7 是原文核心方法学贡献，未进入维度树。
- **M (minor)**：
  - M1 schema 启发段落可补 "原文 schema 的封闭枚举密度" 一条可迁移特性。
  - M2 已可锚定的证据可升级为 `text_verified`，不必整体保留 not_verified。
  - M3 19 篇分母在 "统计与候选发现链路" 一节可显式说明这是 PR 当前样本量，不是原文 N=120 的样本量，避免读者混淆。

**最终建议：NEEDS FIX**。当前 review 的维度树骨架属于通用接口模板，未完成对 da-silva-2011 原文 schema 的实质复原；尽管已经正确做了 not_verified / schema_seed 降级，避免了 finding 误升级，但 A1-DT 任务的核心交付物（原文维度树）目前过小，缺失 Table 2 的 10 字段、QA1–QA4 的 4 项准则、§7 的 3 种 update 模态、Education / Practitioner / SWEBOK 双轴映射等原文显式 schema。必须按 §4 / §5 修复后才能作为 A2a 入口使用。
