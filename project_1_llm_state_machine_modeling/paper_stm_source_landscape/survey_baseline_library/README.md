# #85 综述 baseline 文库

本目录是 `paper_stm_source_landscape/` 内部的综述 / related-work baseline 文库，专门维护 #85 P0/P1 初步入选论文的全文级证据。它借鉴 [project_1_llm_state_machine_modeling/baselines/](../../baselines/) 的“单论文目录 + 总账 + GUIDE”组织方式，但**不放在 project 根目录**，只服务 #85 这篇状态机来源景观论文。

## 1. 文库定位

本文库的目标不是“收藏 PDF”，而是把已经获取到的综述 / 系统映射 / benchmark landscape 近邻论文转化为可维护、可审计、可直接支持论文写作的 baseline 证据链：

1. 支撑 #85 的 Related Work 分层：direct gap neighbor、near neighbor、methodology anchor、background。
2. 支撑 #85 的 novelty gate：确认哪些相邻工作已经覆盖，哪些没有覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”。
3. 支撑 CCF-A/B 级综述写作门槛：抽取系统综述 / 系统映射论文的方法学做法、数据抽取方式、threats 写法和 artifact policy。
4. 支撑后续人工精读：每篇都能从总账跳到 `fulltext_review.md`、`paper.pdf`、`paper_content.txt` 与 `bibtex.bib`。

## 2. 当前范围与边界

- 当前范围：PR #97 中 P0/P1 共 `25` 篇，用户已在本地 Zotero / 导出目录提供 PDF。
- 当前状态：`25/25` 已建单篇目录，均包含 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md`。
- 当前结论：P0 更适合表述为 `verified_gap_neighbor_fulltext`，不是最终 verified direct competitor；P1 主要支撑 Related Work 分层和方法学门槛。
- 边界：本轮仍不能替代 G3 多数据库 direct-competitor safety search，也不能替代 21 条 auto-fulltext Skip gate 复查。

## 3. 维护路线图与工作入口

本文库按“先闭合证据链，再服务论文写作”的路线维护。后续 agent 或人工进入本文库时，应先判断自己处在哪一类任务中：

| 任务类型 | 先读 | 主要改动 | 退出条件 |
|---|---|---|---|
| 快速了解 #85 baseline 现状 | 本 README → [SUMMARY.md](./SUMMARY.md) | 通常不改文件 | 能说清 P0/P1 数量、关系分布、当前安全 claim 与 G3 未闭合风险 |
| 修正单篇全文判断 | [GUIDE.md](./GUIDE.md) → 单篇 `fulltext_review.md` → `paper_content.txt` / `paper.pdf` | 单篇 review、[data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv)、[SUMMARY.md](./SUMMARY.md) | D1--D7 七维独立评分、正/负证据、写作动作与总账一致 |
| 新增 baseline 论文 | [GUIDE.md](./GUIDE.md) §2--§6 | 新单篇目录、两个 CSV、[SUMMARY.md](./SUMMARY.md) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md` 四件套齐全 |
| 回写 #85 论文 story | [SUMMARY.md](./SUMMARY.md) §4 → [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | claim map、Related Work matrix、risk register | 只写 supported claim；P0 只称 gap-neighbor，不称 complete direct competitor search |
| Reviewer dry-run | [GUIDE.md](./GUIDE.md) §7--§8 | PR comment / review comment；必要时修正文库 | 至少抽查 1 篇 P0 与 1 篇 P1，从 README 跳转到 review/PDF/TXT/BibTeX 并核验 D1--D7 |

### 3.1 七维独立评分总原则

本文库中每一行 baseline 都必须有 D1--D7 七个独立评分，不能只给一个总等级。七维分别是：

1. D1 控制系统领域贴近度。
2. D2 行为模型与状态机贴近度。
3. D3 语料、基准与景观研究贴近度。
4. D4 大模型辅助建模贴近度。
5. D5 系统综述与系统映射方法严谨性。
6. D6 制品、可复现性与获取价值。
7. D7 对 #85 证据门支撑度。

完整可执行标准以 [GUIDE.md](./GUIDE.md) §4 为准；README 只保留路线图与入口，不作为第二事实真源。

## 4. 路径结构

```text
survey_baseline_library/
├── README.md
├── GUIDE.md
├── SUMMARY.md
├── data/
│   ├── README.md
│   ├── fulltext_review_matrix.csv
│   └── local_fulltext_receipt.csv
├── scripts/
│   └── validate_library.py
└── papers/
    └── <paper-slug>/
        ├── paper.pdf
        ├── paper_content.txt
        ├── bibtex.bib
        └── fulltext_review.md
```

## 5. 文件职责

| 文件 / 目录 | 职责 |
|---|---|
| [GUIDE.md](./GUIDE.md) | 全文核验协议、D1--D7 可执行评分标准、单篇目录规范、review dry-run 门禁 |
| [SUMMARY.md](./SUMMARY.md) | 25 篇 P0/P1 全文级 baseline 总账；表格直接链接到单篇 review/PDF/TXT/BibTeX |
| [data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv) | 机器真源：D1--D7 全文评分、页码定位、方法学 checklist、final relation、claim impact |
| [data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv) | 文件 receipt：记录每篇 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md`、短哈希与抽取状态 |
| [scripts/validate_library.py](./scripts/validate_library.py) | 文库结构与同步规则校验脚本：检查四件套、D1--D7、SUMMARY 链接、README/GUIDE 规则锚点 |
| [papers/](./papers/) | 单论文目录；每篇一目录，承载原文、抽取文本、BibTeX 和全文 review |

## 6. 推荐阅读路线图

### 6.1 快速了解 #85 相关工作 landscape

1. 读 [SUMMARY.md](./SUMMARY.md) 的 §0--§4，确认 P0/P1 数量、关系分布和对 #85 story 的当前影响。
2. 在 §3 表格中按 `关系` 或 D1--D7 找到重点论文。
3. 点击“题名 / Review”进入单篇 `fulltext_review.md`，看 §2 最终判断、§5 D1--D7 证据链、§9 可写 / 不可写声明。

### 6.2 人工精读或修正某篇论文

1. 从 [SUMMARY.md](./SUMMARY.md) 点击目标论文的 `fulltext_review.md`。
2. 如需核对原文，打开目标单篇目录中的 `paper.pdf` 或 `paper_content.txt`；不要只凭总账改分。
3. 修改 `fulltext_review.md` 后，必须同步 [data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv)、[SUMMARY.md](./SUMMARY.md) 与 [data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv) 的相关字段。
4. 若 D1--D7 或 final relation 改动影响 #85 主张，还要回写 [../story/claim_evidence_map.md](../story/claim_evidence_map.md) 与 [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)。

### 6.3 新增一篇 baseline 论文

1. 先读 [GUIDE.md](./GUIDE.md) 的 §3--§6，确认 D1--D7 与单篇目录标准。
2. 新建 `papers/<slug>/`，至少放入 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md`。
3. `paper_content.txt` 必须用仓库工具生成：`python -m tools.pdf_extractor -i paper.pdf -o paper_content.txt -m text`；若异常再切 OCR。
4. 更新 [data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv)、[data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv)、[SUMMARY.md](./SUMMARY.md)。

## 7. 当前结论摘要

- P0：7 篇均已全文初检为 `verified_gap_neighbor_fulltext`。它们强烈约束 #85 的 gap 表述，但未关闭 #85 的核心空白。
- P1：18 篇分为 `verified_near_neighbor_fulltext` 与 methodology / LLM benchmark anchor，用于 Related Work 和方法学门槛。
- 当前安全写法：**“P0/P1 gap-neighbor 已完成本地全文初检，未发现关闭 #85 三段式 gap 的同题完整竞品；仍需 G3 多数据库检索闭环。”**


## 8. 后续路线

| 阶段 | 目标 | 退出条件 |
|---|---|---|
| A. 四件套与 receipt 闭合 | 每篇都有 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md` | [SUMMARY.md](./SUMMARY.md) 与 [data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv) 均显示 25/25 闭合 |
| B. P0 gap-neighbor 深化 | 对 7 篇 P0 做人工精读，补充更细的章节级证据与差异化段落 | 每篇 P0 都有清晰“覆盖什么 / 没覆盖什么 / #85 如何避让” |
| C. P1 Related Work 分桶 | 把 18 篇 P1 稳定分入 CPS/testing、MDE/RE/MBSE、LLM/AI-for-SE、methodology anchor | 每篇 P1 有可写 Related Work 句式与不可写边界 |
| D. G3 direct-competitor safety search | 补 Semantic Scholar、Google Scholar、ACM DL、IEEE Xplore、SpringerLink、ScienceDirect 等入口 | `targeted_search_audit.csv` 从起点审计升级为完整检索记录 |
| E. 回写 paper story | 把最终 baseline 结论回写 #85 outline、claim-evidence map、Related Work 草稿 | Abstract/Introduction/Related Work 中无 unsupported novelty claim |
