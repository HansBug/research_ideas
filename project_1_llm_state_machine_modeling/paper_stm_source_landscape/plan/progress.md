# 状态机来源景观基础工作进度

## 当前阶段

PR #97 实现阶段：已从计划 PR 进入实现；在原 #85 论文工作区与相关工作 / 基线初筛证据链基础上，追加用户已提供 PDF 后的 P0/P1 全文级 baseline 文库。

## 已完成

- [x] PR body 去除带顺序含义的版本化命名 / 顺序版本命名，固定 `paper_stm_source_landscape/`。
- [x] 对齐 PR #96 论文工作区的六层分工思路，不再引用当前 `main` 上不存在的旧子路径。
- [x] 新建 `story/`、`evidence/`、`baselines/`、`dataset_selection/`、`experiment_design/`、`plan/`。
- [x] 落地 `baselines/data/screening_audit.csv` 覆盖 #95 438 行候选，并修复 `source_row_index` 为 #95 原始 CSV 的 1-based 行号。
- [x] 落地 `baselines/SUMMARY.md` 覆盖 69 行 D1--D7 初筛矩阵，并为入选行补齐 evidence / locator / rationale / pending 字段。
- [x] 落地 `baselines/data/manual_download_needed.bib` 覆盖 25 条 P0/P1 人工下载候选。
- [x] 补齐字段级 provenance / 下载拆分字段，并把 [baselines/MANUAL_DOWNLOAD_REQUESTS.md](../baselines/MANUAL_DOWNLOAD_REQUESTS.md) 扩展为 request-level 人工协作 receipt。
- [x] 落地 `baselines/data/auto_fulltext_light_review_gate.csv` 覆盖 21 条复查门禁。
- [x] 落地 `baselines/data/targeted_search_audit.csv` 记录直接近邻安全检索起点，含命中、零命中与访问受限；后续 G3 仍需全面补跑。
- [x] 按用户要求将新增 Markdown 尽量中文化，保留论文题名、路径、字段名和必要术语。
- [x] 建立 paper 内部 `survey_baseline_library/` 综述 baseline 文库，完成 25 篇 P0/P1 本地 PDF receipt、全文初检矩阵和单篇 `fulltext_review.md`。
- [x] 将用户最新维护要求固化进 `survey_baseline_library/GUIDE.md` 与 `README.md`：四件套硬规则、D1--D7 七维独立评分、CSV/SUMMARY 同步合同、`fulltext_review.md` 证据链最低密度和文库 roadmap。

## 校验 / 审阅日志

| 时间 | 动作 | 结果 |
|---|---|---|
| 2026-06-12 00:45:00 | 处理 codex reviewer sidecar I-1：CSV 机器真源缺逐维 `writing_action` | 已从 25 篇单篇 review 抽取 D1--D7 写作动作写回 `fulltext_review_matrix.csv`，同步 GUIDE 字段合同与校验脚本；顺手将单篇 `Negative evidence searched` heading 中文化为“负证据检索” |
| 2026-06-12 00:30:00 | 按用户要求强化 `survey_baseline_library/` 维护规则 | README 增加任务路线图与七维入口；GUIDE 增加四件套硬规则、D1--D7 独立评分硬规则、升级/降级判定、CSV/SUMMARY 字段合同和 fulltext review 最低证据密度；新增 `scripts/validate_library.py` 作为可执行校验入口 |
| 2026-06-11 23:25:00 | 根据用户补充的本地 Zotero/PDF 已下载事实，建立 `survey_baseline_library/` 并完成 25 篇 P0/P1 全文初检 | 按单篇四件套提交 PDF/TXT/BibTeX/review，并同步 receipt、短哈希、页码定位、短转述和 D1--D7 全文评分 |
| 2026-06-11 21:45:00 | 修复 deepseek reviewer I 级意见：将自动全文复查门禁规则显式收紧为 D7 未降至 🔴 且 D1/D2/D4 至少两个非红，并把命中列表从 7 条扩展到 21 条 | 本地门禁规则与 CSV/Markdown 统计一致性校验通过 |
| 2026-06-11 21:13:00 | 修复 codex reviewer 第二轮 I 级残留：同步 row 32 聚合 `preliminary_rationale` 的 D1=🟠，并更新派生 CSV SHA256 | 本地 69 行聚合 rationale 与 D1--D7 独立分数一致性校验通过 |
| 2026-06-11 20:56:00 | 处理 codex reviewer 复审 I 级意见：补字段级 provenance / 下载 handoff schema，并将 `human-in-the-loop` 泛词误判降级 | 本地校验通过，待推送后复审 |
| 2026-06-11 19:06:00 | 本地生成工作区与审计文件 | 待本地检查 / 三路审阅 |
| 2026-06-11 20:50:00 | 处理 codex reviewer I 级意见：行号修复、D1--D7 字段补齐、targeted search 起点审计扩充、PR body 待同步 | 本地校验通过，待推送后复审 |
| 2026-06-11 19:40:00 | 中文化新增 Markdown | 已完成；保留论文题名、路径、字段名和必要术语 |

## 能力使用审计

- 所需技能：`ai-research-writing-skill`、`sub-agents`。
- 已使用输入：PR #96 结构、issue #85、issue #95、PR #97 Gist、定向检索。
- 未使用输入：未使用真实 LLM / `.env`，因为本 PR 不需要四例真实运行。
- 已产出制品：`story/`、`evidence/`、`baselines/`、`survey_baseline_library/`、`dataset_selection/`、`experiment_design/`、`plan/`。
- 剩余风险：P0/P1 已完成本地全文初检，但仍不是最终 direct-competitor safety search；21 条自动全文门禁尚待轻量方法节复查；Stage 1b 仍是起点审计，Semantic Scholar / Google Scholar / ACM DL / IEEE Xplore / SpringerLink / ScienceDirect 等需后续 G3 补跑。
