# 进度记录：PR-A1 综述之综述脚手架文库

## 1. 当前状态

| 字段 | 状态 |
|---|---|
| PR | [#132](https://github.com/HansBug/research_ideas/pull/132) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/a1-survey-of-surveys-scaffold` |
| 当前阶段 | A1 已建立 `survey_of_surveys/` 文库骨架、字段 schema、候选池、人工下载清单和 dry-run；等待正式三路实现审查 |
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
| [../survey_of_surveys/SUMMARY.md](../survey_of_surveys/SUMMARY.md) | A1 总账、论文列表、覆盖矩阵、模式总表、schema 回修日志、失败路径和后续入口。 |
| [../survey_of_surveys/search/](../survey_of_surveys/search/) | 检索日志、候选池和 BibTeX 格式人工下载清单。 |
| [../survey_of_surveys/patterns/pattern-field-schema.md](../survey_of_surveys/patterns/pattern-field-schema.md) | 六类 pattern、证据等级、字段总表、缺失值语义和回修规则。 |
| [../survey_of_surveys/papers/](../survey_of_surveys/papers/) | 9 个单篇目录；6 个含 PDF + `paper_content.txt`，3 个 metadata-only。 |
| [./task-packets/a1-survey-of-surveys-scaffold.md](./task-packets/a1-survey-of-surveys-scaffold.md) | 当前 PR 任务合同、验收门和验证命令。 |

## 4. 已完成修改

1. 新建 `survey_of_surveys/` 三件套与 `search/`、`patterns/`、`papers/` 子路径。
2. 下载并用 `tools.pdf_extractor.py` 生成 6 篇全文文本：Kitchenham & Charters 2007、Kitchenham 2009、da Silva 2011、Bano 2014、Heikkilä 2015、Kotti 2023。
3. 建立 9 个 `review.md`：6 篇全文文本级、3 篇 metadata-only / 需人工下载。
4. 用现代样本覆盖 ML4SE、Requirements Engineering、Agile RE，并保留早期 EBSE guideline / tertiary study 作为方法学先验。
5. 记录 3 个失败路径：app reviews SLR 2022、Petersen 2008、Petersen 2015，均进入 [../survey_of_surveys/search/manual-download-needed.bib](../survey_of_surveys/search/manual-download-needed.bib)。
6. 在 [../survey_of_surveys/patterns/pattern-field-schema.md](../survey_of_surveys/patterns/pattern-field-schema.md) 中回修 `review_type`、`target_se_subfield`、`predecessor_relation`、`challenge_action_pattern` 等字段。
7. 更新 [../README.md](../README.md) 和 [./README.md](./README.md)，增加 A1 入口和任务包。
8. 更新 [../evidence/references.bib](../evidence/references.bib)，加入 A1 中正式核验的核心 BibTeX 种子。

## 5. dry-run 验收摘要

| 验收项 | 结果 |
|---|---|
| 至少 3 篇全文文本级 | 6 篇，满足 |
| 至少 2 类综述类型 | guideline / tertiary / updated tertiary / SMS / metadata-only SLR，满足 |
| 至少 1 篇高等级来源 | ACM Computing Surveys、IST、ESE metadata-only，满足 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、技术报告，满足 |
| 至少 1 篇非 LLM4SE 子领域 | ML4SE、RE、Agile RE、EBSE 方法学，满足 |
| 至少 1 个降级 / 失败路径 | 3 个 metadata-only，满足 |
| schema 回修 | 已记录 4 类回修，满足 |

## 6. 验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-29 02:18:07 | `python -m tools.pdf_extractor ... -m text` | 6 篇 PDF 成功提取；Springer HTML 伪 PDF 被识别并删除。 |
| 2026-06-29 02:18:07 | 文件存在性 / dry-run 数量检查 | 通过；`reviews=9, texts=6, pdfs=6`。 |
| 2026-06-29 02:18:07 | 禁止强主张 grep | 通过；命中均位于“禁止写法 / 不声称 / grep 规则”语境，不是正向主张。 |
| 2026-06-29 02:18:07 | Markdown 相对链接检查 | 通过；`markdown relative links ok`。 |
| 2026-06-29 02:18:07 | `git diff --check` | 通过。 |
| 2026-06-29 02:18:07 | PDF 类型检查 | 通过；6 个 `paper.pdf` 均为 PDF，非 PDF / HTML 伪文件已删除。 |
| 2026-06-29 02:35:56 | sidecar 只读审查后复验 | 通过；修复 dry-run 数量入口口径、单篇 review 不可迁移列、schema 字段 ID 一致性和 `plan/README.md` PR-A1 状态说明；新增 `review limit columns ok` 检查。 |
| 2026-06-29 02:54:44 | 实现阶段 codex reviewer I 级修复复验 | 通过；修复入口 README 旧 #129/LLM4STM 阻塞路线残留，清理新增 `paper_content.txt` trailing whitespace 使 `git diff --check` 可复现，并澄清 `predecessor_relation` 字段来源中 Petersen 2015 metadata 仅作待核验线索。 |

## 7. 审查状态

| 阶段 | 审查者 | 结果 | 处理 |
|---|---|---|---|
| PR body 初审 | deepseek reviewer | 0C / 1I / 2M | 已修 schema↔dry-run 回修、多样性和 BibTeX 格式。 |
| PR body 初审 | claude reviewer | 0C / 2I / 若干 M | 已修 dry-run 压测和 task packet/progress 同步。 |
| PR body 初审 | codex reviewer | 0C / 0I / 2M | M 级建议已吸收进实现。 |
| PR body 复审 | codex / claude / deepseek reviewer | 0C / 0I | 已进入实现阶段。 |
| 内部 sidecar 实现预审 | codex sidecar | 0C / 3I / 2M | 已修 dry-run 数量口径、review 不可迁移字段、schema 字段名漂移和 `plan/README.md` 状态说明；M2 记录为人工解释型 grep 风险，不阻塞。 |
| 实现阶段正式审查 | 待运行 | 待三路审查 | 当前等待 push 后正式 review。 |

## 8. 剩余风险

1. A1 不是完整 `survey_of_surveys/` 文库；A2a/A2b 仍需大规模扩展。
2. 当前全文样本虽已读 `paper_content.txt`，但多数表格 / 图形尚未逐页 PDF 核对。
3. 现代高等级 SLR `app-reviews-slr-se` 本轮未获取 PDF，只能作为 metadata-only。
4. `pattern-field-schema.md` 是 A1 dry-run 后的最小合同，不能直接当 A3 最终 schema。
5. references.bib 只是种子引用入口，正式 LaTeX 写作前仍需逐条 citation verification。

### Capability-use audit

- Required references/scripts: `sub-agents`、`ai-research-writing-skill` story/reviewer references、`research-planning` planning references、`tools.pdf_extractor.py`。
- Inputs consumed: PR #101 / #132 body、A0/S0/B0/S0B 文档、现有 baselines/GUIDE/SUMMARY、subagent dry-run 样本建议。
- Artifacts produced: `survey_of_surveys/` 文库、9 个单篇 `review.md`、6 个 `paper_content.txt`、A1 task packet、更新后的 progress / README / references。
- Verification run: PDF 提取、`git diff --check`、文件存在性、Markdown 相对链接、PDF 类型和禁用强主张检查均已运行并通过。
- Remaining risk: 文库规模和现代覆盖仍不足以写完整 paper 结论；必须留给 A2a/A2b。
