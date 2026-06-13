# Progress：PR-A0 主线与协议冻结

## 1. 当前阶段

| 字段 | 状态 |
|---|---|
| PR | [#103](https://github.com/HansBug/research_ideas/pull/103) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前阶段 | A0 文档实现与 review |
| 真实 LLM | 未运行 |
| 四个真实例子 | A0 不运行 |
| Codecov | 纯文档 PR，无可执行代码，Codecov 不适用 |

## 2. 已完成

- 创建 `project_1_llm_state_machine_modeling/paper_agent_based_slr/` 工作区。
- 按用户要求复刻旧 Path-1 的 `story/ evidence/ baselines/ dataset_selection/ experiment_design/ plan/` 主结构，但不创建 `foundation/` 子路径。
- 落地 story、protocol、terminology policy、claim-evidence map、novelty matrix、outline。
- 落地 project inventory、fact drift policy、citation seed inventory 与 A0 `references.bib` 种子。
- 落地 evaluation dimensions seed 与 reviewer risk register。
- 落地 A0 task packet 和本进度文件。

## 3. 合同 review 记录

| reviewer | comment | C/I/M | 处理 |
|---|---|---:|---|
| claude reviewer | [comment](https://github.com/HansBug/research_ideas/pull/103#issuecomment-4692631648) | 0 / 2 / 3 | 已补 fact drift / risk register，evaluation contract 降级。 |
| deepseek reviewer | [comment](https://github.com/HansBug/research_ideas/pull/103#issuecomment-4692634998) | 0 / 3 / 5 | 已补 terminology policy、fact drift、risk register 和 M 级口径。 |
| codex reviewer | [comment](https://github.com/HansBug/research_ideas/pull/103#issuecomment-4692635270) | 0 / 2 / 1 | 已扩展验证命令覆盖所有承诺文件。 |

## 4. Verification log

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-06-12 | `source venv/bin/activate` 后运行 A0 Python sanity：检查 25 个必需文件、无 `foundation/` 子层、PR #97 引用含 OPEN / 未合入 / snapshot / 分支局部口径、禁止 claim 只在禁止 / 风险语境中出现、novelty matrix 覆盖 SLR / SMS / PRISMA / ASReview / RobotReviewer / systematic review automation / LLM-assisted | 通过，输出 `paper_agent_based_slr A0 sanity ok`。 |
| 2026-06-12 | `git diff --check` | 通过。 |

## 5. Remaining risks

| 风险 | 当前状态 | 后续处理 |
|---|---|---|
| Related work corpus 仍不完整 | A0 已登记 seed 并补 `references.bib` 核心锚点；LLM-assisted SLR 仍待系统检索 | A1 / related-work PR。 |
| PR #97 仍 OPEN / 未合入 | 已建立 fact drift policy，并在 A0 task packet 增加 A1 snapshot 等值断言 gate | A1 merge 或冻结 snapshot。 |
| 没有真实场景和运行 | A0 已补 [dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，但不冻结场景 | A3/A4/A5。 |
| A5 指标未冻结 | A0 非目标 | A5。 |

## 6. Capability-use audit

- Required references/scripts：`ai-research-writing-skill` 的 story gate；`sub-agents` / 三路 reviewer 合同审查；旧 Path-1 PR #96 路径结构。
- Inputs consumed：PR #101 body、PR #99 会后定调 comment、已合入导师讨论记录、PR #97 状态、PR #96 文件结构、三路 reviewer comment。
- Inputs not used and why：未读取或复制 PR #97 PDF / fulltext；A0 只做合同与证据层级，不复制未合入资产。
- Artifacts produced：`paper_agent_based_slr/` 下 README、story、evidence、baselines、dataset_selection、experiment_design、plan 全部 A0 文件。
- Verification run：`source venv/bin/activate` 后运行 A0 Python sanity、Markdown 相对链接检查、成片英文检查、emoji 列检查、`git diff --check`，并用 DOI metadata 获取 A0 `references.bib` 种子。
- Remaining risk：真实 related-work coverage、benchmark scenarios、LLM run records 和 A5 metrics 尚未构造。

## 7. PR-B0 强化进度（2026-06-14）

| 字段 | 状态 |
|---|---|
| PR | [#105](https://github.com/HansBug/research_ideas/pull/105) |
| 当前阶段 | B0 baseline 文库从粗筛升级为全文 review |
| 真实 LLM | 未运行 |
| 四个真实例子 | B0 不运行 |
| Codecov | 纯文档/文献 PR，不适用 |

### 已追加合同

- PR body 已新增“2026-06-14 强化迭代”章节。
- PR comment 已说明本轮从 title/abstract 粗筛升级为全文证据级 baseline review。
- [task-packets/b0-fulltext-baseline-review.md](./task-packets/b0-fulltext-baseline-review.md) 已记录本轮范围、拒收检查和验证命令。

### 已完成（B0 强化）

- [../baselines/README.md](../baselines/README.md) 已更新为 34 篇本地建库、P0/P1/P2 全部 `paper_content.txt` 全文文本核验口径。
- [../baselines/GUIDE.md](../baselines/GUIDE.md) 已新增 `阅读状态` + `证据等级`、SUMMARY 最小 / 增强 schema、I 级必需字段与字段命名风险。
- [../baselines/SUMMARY.md](../baselines/SUMMARY.md) 已拆成“主表 A：方法事实与证据等级”“主表 B：D1-D7 与 paper2 主张影响”“主表 C：主张绑定与 baseline 可用性”“主表 D：阶段边界、人工审计与 provenance”“主表 E：LLM 设置、可复现资产与数值使用许可”，覆盖 34 篇本地条目。
- 9 篇 P2 已补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`review.md`。
- 34 篇本地 `review.md` 均包含快速结论卡片、阅读状态、证据等级、D1-D7、方法/实验/结果/局限/paper2 影响和待复核清单；并已按 `$ai-research-writing-skill` 字段审阅补齐作者/venue/出版状态、研究脉络、引用角色、LLM/agent 角色、证据溯源粒度、威胁/支持 paper2 主张、paper2 应避免的主张、baseline 可用性与可复现资产阻塞项。
- 2026-06-14 继续吸收字段体系审稿意见：34 篇快速结论卡片新增受影响主张 ID、威胁类型、阶段边界、人类角色、审计时机、主张追踪状态、决策日志状态、审计导出性、模型/API 设置、提示词状态、温度/重复/随机种子、代码/数据/许可状态、运行可行性、关键结果锚点与数值使用许可。

### Verification log（B0 强化）

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-06-14 | `source venv/bin/activate` 后运行 B0 sanity：检查 34 个论文目录四件套、`review.md` 必需章节、SUMMARY 描述性字段与禁用强 claim | 通过，输出 `paper_dirs= 34`、`missing= []`、`bad= []`。 |
| 2026-06-14 | `git diff --check` | 通过；本轮已清理新增 `paper_content.txt` 的 PDF 提取残留 NUL 与行尾空白，避免验收记录与真实 gate 冲突。 |
| 2026-06-14 | 字段 hardening sanity：检查 34 篇 quick card 均含受影响主张 ID、威胁类型、阶段边界、人类角色、审计时机、主张追踪、决策日志、审计导出性、模型/API、提示词、随机种子、代码/数据/许可、运行可行性、关键结果锚点、数值使用许可；检查 SUMMARY 含主表 C/D/E | 通过，输出 `B0 field-hardened sanity ok`。 |
| 2026-06-14 | 修复复审指出的 artifact 状态误标风险：清理 34 篇 `review.md` 与 SUMMARY §7 中“声称有/正文出现 GitHub 或 code 线索”“dataset 或 data availability 线索”等模板句；按原文文本线索改成未提及、给出 URL 待打开、需申请、占位承诺、匿名仓库、Colab/补充材料等更保守口径；同时在 GUIDE / task packet 固化 artifact-status、方法假设、负面证据、伦理/license 和 claim-anchor 分层规则。 | 待复验。 |

### Capability-use audit（B0 强化）

- Required references/scripts：`ai-research-writing-skill` 的主张-证据、story gate、reviewer gate；仓库 `tools.pdf_extractor`；本地 schema 审核子agent。
- Inputs consumed：PR #105 body、用户关于全文 review / SUMMARY 描述性维度的追加要求、字段 schema 审核意见、字段 hardening 子agent 审阅输出、字段体系复审意见、当前 baseline PDF / `paper_content.txt` / `bibtex.bib`、arXiv query results。
- Inputs not used and why：WSESE@ICSE 2025 PDF 仍未获取，不能全文核验；关键 P0 的 PDF 图表尚未逐页人工核对，因此当前证据等级为“全文文本级；图表待人工核对”。
- Artifacts produced：更新 [../baselines/README.md](../baselines/README.md)、[../baselines/GUIDE.md](../baselines/GUIDE.md)、[../baselines/SUMMARY.md](../baselines/SUMMARY.md)、补 P2 本地目录、重写单篇 `review.md`、补齐主张-证据 / baseline 可用性 / artifact readiness 字段、清理 `paper_content.txt` 提取残留、更新 [task-packets/b0-fulltext-baseline-review.md](./task-packets/b0-fulltext-baseline-review.md)。
- Verification run：已运行 B0 sanity、字段 hardening sanity 与 `git diff --check`。
- Remaining risk：自动文本提取可能遗漏图表细节；正式写 Related Work 前，关键 P0 仍建议人工打开 PDF 复核图表/表格/数值，WSESE@ICSE 2025 仍需人工全文；当前代码/数据/许可只完成文本级线索识别，未打开 URL、未 clone、未核验 license、未 smoke，不能写成可运行 baseline。
