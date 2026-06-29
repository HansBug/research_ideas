# 进度记录：PR-A1 综述之综述脚手架文库

## 1. 当前状态

| 字段 | 状态 |
|---|---|
| PR | [#132](https://github.com/HansBug/research_ideas/pull/132) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/a1-survey-of-surveys-scaffold` |
| 当前阶段 | A1 已建立 `survey_of_surveys/` 文库骨架、字段 schema、候选池、人工下载清单和 dry-run；本轮已纳入 #95 十篇现代维度锚点，补充 A1-M0--M6 元维度字段，并在用户补齐历史 PDF 后完成 19 篇 `review.md`、19 个 `metadata.json`、19 个 `paper.pdf`、19 个 `paper_content.txt`、0 个 active manual-download 条目的总账；最新返工已将 SUMMARY / GUIDE 重构为长期文库总账，统一年份降序主表、三类证据池和 19 × A1-M0--M6 覆盖矩阵已成为后续维护合同 |
| 真实大语言模型 | 未运行；本 PR 不触发 provider 调用 |
| `.env` | 未读取；本 PR 不需要 key |
| 四个真实例子 | 不运行；上游 #101 对 A1 只要求 3--5 篇文库 dry-run |
| Codecov | 纯文档 / PDF 文库 PR，Codecov 预计不适用；若 PR 页面出现检查仍需纳入 review |

## 2. 本 PR 的输入来源

| 来源 | 用途 | 当前口径 |
|---|---|---|
| PR-S0 / PR [#114](https://github.com/HansBug/research_ideas/pull/114) | 提供审计优先证据工程主线和 survey-of-surveys scaffold 需求 | 当前 A1 必须遵守 S0-v2 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) | 提供三阶段 SLR、维度模式、统计分析 / finding 分层、人机协同约束 | 当前 A1 只建立模式先验，不生成领域 finding |
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) | 提供近邻 baseline 压力和 forbidden claims | A1 禁止写首次、完整自动化、PRISMA 合规 |
| PR #132 body review | 提供 schema↔dry-run 回修、多样性覆盖、task packet/progress 同步等验收门 | 已落实到文档和任务包 |

## 3. 当前交付物

| 文件 / 目录 | 当前作用 |
|---|---|
| [../survey_of_surveys/README.md](../survey_of_surveys/README.md) | 文库入口、边界、文件说明和禁止误读。 |
| [../survey_of_surveys/GUIDE.md](../survey_of_surveys/GUIDE.md) | 检索、筛选、证据等级、单篇目录、schema 回修、SUMMARY 回填和 dry-run 规则。 |
| [../survey_of_surveys/SUMMARY.md](../survey_of_surveys/SUMMARY.md) | 长期文库总账：统一年份降序主表、CCF 复核状态列、三类证据池、A1-M0--M6 定义、19 篇逐篇覆盖矩阵、pattern 总结、schema 修订 / 回填日志、风险和 A2a/A2b 接力入口。 |
| [../survey_of_surveys/search/](../survey_of_surveys/search/) | 检索日志、候选池、issue #95 十篇来源审计和 BibTeX 格式人工下载清单。 |
| [../survey_of_surveys/patterns/pattern-field-schema.md](../survey_of_surveys/patterns/pattern-field-schema.md) | 六类 pattern、证据等级、字段总表、缺失值语义和回修规则。 |
| [../survey_of_surveys/papers/](../survey_of_surveys/papers/) | 19 个单篇目录；19 个含 `metadata.json`、`paper.pdf`、`paper_content.txt` 和 `review.md`；当前无 active metadata-only / 需人工下载条目。 |
| [./task-packets/a1-survey-of-surveys-scaffold.md](./task-packets/a1-survey-of-surveys-scaffold.md) | 当前 PR 任务合同、验收门和验证命令。 |

## 4. 已完成修改

1. 新建 `survey_of_surveys/` 三件套与 `search/`、`patterns/`、`papers/` 子路径。
2. 下载并用 `tools.pdf_extractor.py` 生成 6 篇全文文本：Kitchenham & Charters 2007、Kitchenham 2009、da Silva 2011、Bano 2014、Heikkilä 2015、Kotti 2023。
3. 建立 9 个初始 `review.md`；其中历史 3 篇 metadata-only / 需人工下载已由用户本地 Zotero PDF 补齐并升级为全文文本级。
4. 用现代样本覆盖 ML4SE、Requirements Engineering、Agile RE，并保留早期 EBSE guideline / tertiary study 作为方法学先验。
5. 记录并闭环 3 个失败路径：app reviews SLR 2022、Petersen 2008、Petersen 2015 曾进入 [../survey_of_surveys/search/manual-download-needed.bib](../survey_of_surveys/search/manual-download-needed.bib)，现已补齐 PDF/text/review/metadata，active 人工下载清单清零。
6. 在 [../survey_of_surveys/patterns/pattern-field-schema.md](../survey_of_surveys/patterns/pattern-field-schema.md) 中回修 `review_type`、`target_se_subfield`、`predecessor_relation`、`challenge_action_pattern` 等字段。
7. 更新 [../README.md](../README.md) 和 [./README.md](./README.md)，增加 A1 入口和任务包。
8. 更新 [../evidence/references.bib](../evidence/references.bib)，加入 A1 中正式核验的核心 BibTeX 种子。
9. 按用户新增要求，把来源字段拆为 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级`、`CCF 复核状态`，并同步到 SUMMARY、candidate-pool、19 篇单篇 review 和 schema。
10. 按用户新增要求，从 issue #95 纳入 10 篇现代维度锚点，已建立 `metadata.json` / `bibtex.bib` / `paper.pdf` / `paper_content.txt` / `review.md`，并按一篇一 subagent 原则完成全文 review 与 SUMMARY 回填。
11. 在 GUIDE、schema、patterns README、search log、候选池和 [../survey_of_surveys/search/issue95-selection-audit.md](../survey_of_surveys/search/issue95-selection-audit.md) 中补充 A1-M0--M6 元维度规则、#95 锚点状态、年份口径和统计池资格。
12. 根据用户对 SUMMARY 缝合感和批次拆表问题的反馈，重构 [../survey_of_surveys/SUMMARY.md](../survey_of_surveys/SUMMARY.md) 与 [../survey_of_surveys/GUIDE.md](../survey_of_surveys/GUIDE.md)：取消“初始 dry-run / #95 十篇”等批次化主表，改为统一年份降序论文总表；明确主统计池、方法学参考池、schema seed / boundary pool 三类证据池；新增 19 篇 × A1-M0--M6 覆盖矩阵；要求后续 SUMMARY 按长期文库对象维护而非按 PR 施工批次维护。
13. 修复本轮三路 reviewer 复审 C/I：主表新增 `CCF 复核状态` 列以避免 A/B/C 字面值脱离 disclaimer；三类证据池改为主归属计数（13 + 2 + 4 = 19），并说明 Petersen 2015 的次级方法学价值不重复计数；恢复 SUMMARY 的结构化“schema 修订 / 回填日志”，同步 GUIDE、pattern schema 与 task packet。

## 5. dry-run 验收摘要

| 验收项 | 结果 |
|---|---|
| 至少 3 篇全文文本级 | 19 篇，满足；其中初始 dry-run 9 篇、#95 现代锚点 10 篇 |
| 至少 2 类综述类型 | guideline / tertiary / updated tertiary / SLR / SMS / systematic mapping / MLR / roadmap / solution proposal，满足 |
| 至少 1 篇高等级来源 | TOSEM、IST、JSS、ESE、ACM Computing Surveys；其中 TOSEM 为 CCF A 本地缓存、IST/JSS/ESE 为 CCF B 本地缓存，官方目录待人工复核 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、技术报告，满足 |
| 至少 1 篇非 LLM4SE 子领域 | ML4SE、RE、Agile RE、EBSE 方法学、MDE4ML、MDSE、DevSecOps、secondary-study artifacts，满足 |
| 至少 1 个降级 / 失败路径 | 3 个历史 metadata-only / manual-download-needed 已闭环；另有 roadmap / proposal 统计池排除，满足 |
| schema 回修 | 已记录 review type、前序关系、SE 子领域、挑战/行动、来源字段、统计池资格、证据角色、年份口径等多类回修，满足 |
| SUMMARY 长期总账 | 已取消批次化主表，19 篇统一按年份降序排列；主表包含 `CCF 复核状态`；三类证据池按主归属计数；19 × A1-M0--M6 覆盖矩阵与 schema 修订 / 回填日志已写入 SUMMARY / GUIDE，满足 |

## 6. 验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-29 18:05:48 | 三路 reviewer C/I 修复复验 | 已修复 codex reviewer 1I 与 claude reviewer 2I：SUMMARY 主表新增 `CCF 复核状态` 列；三类证据池改为主归属计数并解释 Petersen 2015 次级方法学价值；恢复结构化 schema 修订 / 回填日志并同步 GUIDE / pattern schema / task packet；本地结构验证、`git diff --check` 与 PDF 类型检查已通过，待三路 reviewer 复审确认。 |
| 2026-06-29 17:48:49 | SUMMARY / GUIDE 长期文库总账化返工复验 | 通过结构自检：旧分批标题已移除；统一论文总表 19 行且年份降序；A1-M0--M6 覆盖矩阵 19 行；19 个 `review.md` 均含 A1-M0--M6；19 review / 19 metadata / 19 PDF / 19 text / active manual-download=0；本轮等待三路 reviewer 复审。 |
| 2026-06-29 16:59:12 | 用户本地 Zotero PDF 补齐复验 | 通过；app reviews SLR 2022、Petersen 2008、Petersen 2015 已复制 `paper.pdf`、生成 `paper_content.txt`、重写 `review.md` / `metadata.json`；文件系统统计更新为 19 review / 19 metadata / 19 PDF / 19 text；active manual-download=0。 |
| 2026-06-29 16:13:28 | 三路 reviewer C/I 修复复验 | 通过；当时 19 篇均有 `metadata.json` 必填字段，16 个 PDF/text、3 个 manual-download 条目一致；SUMMARY §9/§12 降序；`git diff --check` 两点工作区口径通过；非 CCF venue 的复核状态已从 `--` 改为明确说明。后续 16:59 已升级为 19/19/19/19 与 active manual-download=0。 |
| 2026-06-29 15:41:07 | #95 十篇现代维度锚点扩展 | 已获取 10 篇公开 PDF / 开放预印本并生成 `paper_content.txt`；已补 A1-M0--M6 元维度规则；10 篇均已完成 `review.md` 并回填 SUMMARY；早期 9 篇也已补齐 `metadata.json`，使 19 篇具备统一机器可读字段。 |
| 2026-06-29 15:37:22 | A1 现代锚点一致性复验 | 通过；`git diff --check` 通过；当时文件系统统计为 19 个 `review.md`、19 个 `metadata.json`、16 个 `paper.pdf`、16 个 `paper_content.txt`；#95 十篇均具备 `bibtex.bib` / `metadata.json` / PDF / 文本 / review；`interactive-llm-systematic-mapping` 年份统一为正式卷期 2025，并保留 online-first 2024-11-01；manual-download-needed 当时保持 3 条旧失败路径，后续已清零。 |
| 2026-06-29 13:20:00 | 用户新增来源字段要求落实 | 已同步 `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级`、`CCF 复核状态` 到总账、候选池、单篇 review 和 schema；CCF 字段目标不局限 `ccf_venues/`，但本轮官方页受 WAF，当前使用本地缓存并显式标注。 |
| 2026-06-29 02:54:44 | 实现阶段 codex reviewer I 级修复复验 | 通过；修复入口 README 旧 #129/LLM4STM 阻塞路线残留，清理新增 `paper_content.txt` trailing whitespace 使 `git diff --check` 可复现，并澄清 `predecessor_relation` 字段来源中 Petersen 2015 metadata 仅作待核验线索。 |
| 2026-06-29 02:35:56 | sidecar 只读审查后复验 | 通过；修复 dry-run 数量入口口径、单篇 review 不可迁移列、schema 字段 ID 一致性和 `plan/README.md` PR-A1 状态说明；新增 `review limit columns ok` 检查。 |
| 2026-06-29 02:18:07 | `python -m tools.pdf_extractor ... -m text` | 6 篇 PDF 成功提取；Springer HTML 伪 PDF 被识别并删除。 |
| 2026-06-29 02:18:07 | 文件存在性 / dry-run 数量检查 | 通过；`reviews=9, texts=6, pdfs=6`。 |
| 2026-06-29 02:18:07 | 禁止强主张 grep | 通过；命中均位于“禁止写法 / 不声称 / grep 规则”语境，不是正向主张。 |
| 2026-06-29 02:18:07 | Markdown 相对链接检查 | 通过；`markdown relative links ok`。 |
| 2026-06-29 02:18:07 | `git diff --check` | 通过。 |
| 2026-06-29 02:18:07 | PDF 类型检查 | 通过；6 个 `paper.pdf` 均为 PDF，非 PDF / HTML 伪文件已删除。 |

## 7. 审查状态

| 阶段 | 审查者 | 结果 | 处理 |
|---|---|---|---|
| PR body 初审 | deepseek reviewer | 0C / 1I / 2M | 已修 schema↔dry-run 回修、多样性和 BibTeX 格式。 |
| PR body 初审 | claude reviewer | 0C / 2I / 若干 M | 已修 dry-run 压测和 task packet/progress 同步。 |
| PR body 初审 | codex reviewer | 0C / 0I / 2M | M 级建议已吸收进实现。 |
| PR body 复审 | codex / claude / deepseek reviewer | 0C / 0I | 已进入实现阶段。 |
| 内部 sidecar 实现预审 | codex sidecar | 0C / 3I / 2M | 已修 dry-run 数量口径、review 不可迁移字段、schema 字段名漂移和 `plan/README.md` 状态说明；M2 记录为人工解释型 grep 风险，不阻塞。 |
| 内部 sidecar 预审 | codex sidecar（Boole the 2nd） | 0C / 3I / 1M | 已修 progress 19/16/3 口径、task packet 勾选、interactive 年份、`git diff --check` EOF 问题。 |
| 实现阶段正式审查 | codex / claude / deepseek reviewer | 已发现并修复 I 级问题 | 修复 `git diff --check`、19 篇 metadata、TOSEM 年份口径、SUMMARY 日志降序、CSUR/非 CCF 复核状态；等待本次 push 后复审。 |
| SUMMARY / GUIDE 总账化返工复审 | codex / claude / deepseek reviewer | 0C / 3I / 5M | deepseek 0C/0I/1M；codex 0C/1I；claude 0C/2I。I 级已修：CCF 复核状态列、三池主归属计数、schema 修订 / 回填日志。M 级仅作后续 hardening，不阻塞。 |

## 8. 剩余风险

1. A1 不是完整 `survey_of_surveys/` 文库；A2a/A2b 仍需大规模扩展。
2. 当前全文样本虽已读 `paper_content.txt`，但多数表格 / 图形尚未逐页 PDF 核对。
3. 历史高等级 SLR `app-reviews-slr-se` 的自动下载失败已由用户本地 Zotero PDF 解决；当前剩余风险是复杂表格、搜索式和图形仍需 A2a 视觉核对。
4. `pattern-field-schema.md` 是 A1 dry-run 后的最小合同，不能直接当 A3 最终 schema。
5. references.bib 只是种子引用入口，正式 LaTeX 写作前仍需逐条 citation verification。

### Capability-use audit

- Required references/scripts: `sub-agents`、`ai-research-writing-skill` story/reviewer references、`research-planning` planning references、`tools.pdf_extractor.py`。
- Inputs consumed: PR #101 / #132 body、A0/S0/B0/S0B 文档、现有 baselines/GUIDE/SUMMARY、subagent dry-run 样本建议。
- Artifacts produced: `survey_of_surveys/` 文库、19 个单篇 `review.md`、19 个 `paper_content.txt`、19 个 `paper.pdf`、0 条 active manual-download BibTeX、A1 task packet、更新后的 progress / README / references。
- Verification run: PDF 提取、`git diff --check`、文件存在性、Markdown 相对链接、PDF 类型、#95 年份/统计池资格、manual-download-needed 条目数、SUMMARY 统一主表 / 年份降序 / A1-M0--M6 矩阵结构和禁用强主张检查均已运行；最新复验见 §6。
- Remaining risk: 文库规模和现代覆盖仍不足以写完整 paper 结论；必须留给 A2a/A2b。
