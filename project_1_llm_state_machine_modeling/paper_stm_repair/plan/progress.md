# paper_stm_repair progress

## 1. 当前阶段

| 字段 | 状态 |
|---|---|
| PR | [#110](https://github.com/HansBug/research_ideas/pull/110) |
| 上游结构计划 PR | [#109](https://github.com/HansBug/research_ideas/pull/109) |
| 上游论文伞 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | PR-R1.8-A implementation：结构纪律冻结文件已落地，待三路 implementation review。 |
| 本轮目标 | 冻结三类文库分工、root 三件套、SUMMARY-first、fact-union 哨兵、project-level 边界和 R1.8-B/C/D/E 移交门。 |
| 四例真实运行 | 不需要；R1.8-A 是 docs-only 结构纪律 PR。 |
| 真实 LLM / `.env` | 不调用真实 LLM，不读取 `.env`。 |
| 事实迁移 | 不执行；不移动 `seed_corpus/`、`evidence/`、`search_rounds/`、`search_results/` 或单篇目录。 |
| 当前产物 | [../GUIDE.md](../GUIDE.md)、[../corpora/README.md](../corpora/README.md)、[./task-packets/r1.8-a-structure-discipline-freeze.md](./task-packets/r1.8-a-structure-discipline-freeze.md)。 |

## 2. 已消费输入

| 输入 | 用途 |
|---|---|
| PR #100 body | R0 范围、子 PR 依赖、四例运行要求、评价门顺序。 |
| PR #99 会后定调 comment | 第一篇转向与第二篇背景。 |
| [../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md](../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | 正式导师定调事实源。 |
| [../../talks/SUMMARY.md](../../talks/SUMMARY.md) | 当前高优先级约束。 |
| 旧 [../../paper_v1/](../../paper_v1/) | 历史目录与旧 story 共存风险。 |

## 3. 已产出文件

| 文件 | 状态 |
|---|---|
| [../README.md](../README.md) | 已创建 |
| [../story/README.md](../story/README.md) | 已创建 |
| [../story/paper_story.md](../story/paper_story.md) | 已创建 |
| [../story/task_boundary.md](../story/task_boundary.md) | 已创建 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | 已创建 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 已创建 |
| [../story/paper_outline.md](../story/paper_outline.md) | 已创建 |
| [../evidence/README.md](../evidence/README.md) | 已创建 |
| [../evidence/upstream_fact_ledger.md](../evidence/upstream_fact_ledger.md) | 已创建 |
| [../evidence/legacy_asset_inheritance.md](../evidence/legacy_asset_inheritance.md) | 已创建 |
| [../experiment_design/README.md](../experiment_design/README.md) | 已创建 |
| [../experiment_design/research_questions.md](../experiment_design/research_questions.md) | 已创建 |
| [../experiment_design/better_stm_definition.md](../experiment_design/better_stm_definition.md) | 已创建 |
| [../experiment_design/evaluation_gate.md](../experiment_design/evaluation_gate.md) | 已创建 |
| [./README.md](./README.md) | 已创建 |
| [./agent_provenance.md](./agent_provenance.md) | 已创建 |
| [../GUIDE.md](../GUIDE.md) | R1.8-A 已创建 |
| [../corpora/README.md](../corpora/README.md) | R1.8-A 已创建 |
| [./task-packets/r1.8-a-structure-discipline-freeze.md](./task-packets/r1.8-a-structure-discipline-freeze.md) | R1.8-A 已创建 |

## 4. PR-R1.8-A plan review 状态

| reviewer | comment | 结论 | 处理状态 |
|---|---|---|---|
| claude reviewer | [PR body 审查](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700794121) | C=0 / I=2 / M=3，No-Go-Until-I | I 已在 PR body、GUIDE、task packet 中闭合：目录骨架边界与迁移裁决表已固化。 |
| deepseek reviewer | [PR body 审查](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700795067) | C=0 / I=1 / M=2 | I 已在 task packet §5 执行前 fact-union 审计中闭合。 |
| codex reviewer | [PR body 审查](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700795122) | C=0 / I=1 / M=3 | I 已在 GUIDE §6、task packet §3、PR body §1.2/§4/§7 中闭合。 |
| 主 session | [implementation 第一轮汇报](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700906411) | 已进入 implementation review | 已 push 提交 `b0e5ce0c`，等待三路复审。 |

## 4.1 PR-R1.8-A implementation review 状态

| reviewer | comment | 结论 | 处理状态 |
|---|---|---|---|
| claude reviewer | [implementation review](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700931671) | C=0 / I=0 / M=3，ready | 无阻塞；M 级建议作为可选优化。 |
| deepseek reviewer | [implementation review](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700934990) | C=0 / I=0 / M=3，ready | 无阻塞；M 级建议作为可选优化。 |
| codex reviewer | [implementation review](https://github.com/HansBug/research_ideas/pull/110#issuecomment-4700935110) | C=0 / I=1 / M=1，not ready | I-1 指出本文件仍引用 #102 / R0 review/check 作为当前证据链；本次修复将 #110 review/check 写入当前 gate，并将 #102 记录降级为历史。 |

## 5. PR-R1.8-A 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| diff 范围 | `git diff --name-status origin/paper1/r1.8-corpus-architecture-reorg...HEAD` | 仅 6 个允许文件：`GUIDE.md`、`README.md`、`corpora/README.md`、`plan/agent_provenance.md`、`plan/progress.md`、`plan/task-packets/r1.8-a-structure-discipline-freeze.md`。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| Markdown 相对链接 | 自定义 Python 链接检查，范围 `paper_stm_repair` | 通过；missing links = 0。 |
| 旧事实目录 diff | `git diff --name-only ... | grep -E 'paper_stm_repair/(seed_corpus|evidence)/'` | 通过；无 `seed_corpus/` / `evidence/` 文件进入 diff。 |
| `corpora/` 物理边界 | `find paper_stm_repair/corpora -maxdepth 2 -print` | 仅 `corpora/README.md`；未创建 `seed_library/`、`repair_baselines/`、`nl_datasets/` 内容子库。 |
| R1.7 单篇目录哨兵 | `ls -d seed_corpus/papers/*/ | wc -l` | 24，与 task packet §5.4 对齐。 |
| R1.7 search rounds 哨兵 | `ls seed_corpus/search_rounds/ | wc -l` | 12，与 task packet §5.2 对齐。 |
| R1.7 raw search results 哨兵 | `find seed_corpus/search_results/ -name '*.jsonl' | wc -l` | 20，与 task packet §5.3 对齐。 |
| R1.7 candidate / screening 哨兵 | reviewer dry-run 解析 `candidate_matrix.md` / `screening_ledger.md` | 47 / 47 且 ID 顺序一致。 |
| 旧九 crosswalk 哨兵 | reviewer dry-run 检查 `baseline_seed_method_crosswalk.md` | 旧九 generation baseline seed-method 入账关系保留为后续迁移哨兵。 |
| 四例真实运行 | 按 PR #110 / #109 R1.8-A 合同 | 不执行；本 PR 是 docs-only 结构纪律冻结，不调用真实 LLM，不读取 `.env`。 |
| CI / feedback-smoke | `gh pr checks 110` | `feedback-smoke` pass。 |
| Codecov / coverage | PR comments / checks | 未发现 Codecov 覆盖率评论；本 PR 为 docs-only，无单测覆盖率变化，未虚构 coverage。 |

## 6. 剩余风险

| 风险 | 状态 | 后续处理 |
|---|---|---|
| R0 当前 story 仍是可迭代基线，部分论证链需等待真实实验回填。 | 已显式说明 | R1--R6 根据事实证据校准 claim、RQ 与大纲 |
| baseline / prior artifact 可用性尚未盘点。 | 已知未闭合 | PR-R1 |
| 四例样本尚未冻结。 | 已知未闭合 | PR-R2 |
| 转换器范围尚未冻结。 | 已知未闭合 | PR-R3 |
| 评价量表和主结果 eligibility 尚未冻结。 | 已知未闭合 | PR-R4 / PR-R6 |
| 修正循环效果尚未实证。 | 已知未闭合 | PR-R5 / PR-R6 |
| R1 当前资产审计仍是候选级证据，部分链路需等待 R2--R6 真实实验回填。 | 已显式说明 | R2 样本冻结、R3 转换器、R4--R6 实验结果出来后校准候选角色和论文 story。 |

## 7. Capability-use audit

| 项 | 记录 |
|---|---|
| 使用技能 | sub-agents；ai-research-writing-skill 的 claim-evidence discipline。 |
| 真实 LLM / API | 未调用。 |
| 外部网络 | 通过 `gh` 读取 / 更新 PR。 |
| 产物类型 | Markdown planning docs。 |
| 覆盖率 | docs-only，预计无 Codecov 覆盖率变化。 |

## 8. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-14 13:34:18 | PR-R1.8-A：冻结三类文库入口、fact-union 哨兵、project-level 边界与 task packet；已创建 `paper_stm_repair/GUIDE.md`、`corpora/README.md`、`plan/task-packets/r1.8-a-structure-discipline-freeze.md`。 |
| 2026-06-14 00:16:15 | PR-R1 补充 strict seed 大规模文献调研协议、初始统计和 review gate；等待补充后多智能体复审。 |
| 2026-06-13 00:45:00 | PR-R1 创建 baseline 资产审计文档：source coverage、branch-local trace、候选矩阵、artifact 可获取性与格式转换压力；本轮不改写 R0 completion 结论。 |
| 2026-06-13 00:19:18 | 按人工审阅意见补充 R0 是可执行论文工作基线而非最终论证链；后续 R1--R6 可按真实实验结果回填并局部校准 story / RQ / claim。 |
| 2026-06-13 00:08:00 | 三路 implementation re-review 均 C=0/I=0；feedback-smoke 通过；记录 docs-only 无 Codecov 覆盖率变化。 |
| 2026-06-12 23:43:33 | 完成本地链接、diff、forbidden wording 与 `path1_foundation` 修改检查；补充旧 `paper_v1/README.md` 入口提示。 |
| 2026-06-12 23:42:20 | 初始化 R0 文档路径与 progress 记录。 |

## 9. PR-R1 进度

| 字段 | 状态 |
|---|---|
| PR | [#104](https://github.com/HansBug/research_ideas/pull/104) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | R1 implementation / strict seed 调研协议补充后 review iteration |
| 四例真实运行 | 不需要；R1 是资产审计。 |
| 真实 LLM 调用 | 不需要。 |
| method runtime 修改 | 不涉及。 |
| `path1_foundation/` 修改 | 不允许；仅在 [../evidence/branch_asset_trace.md](../evidence/branch_asset_trace.md) 记录分支局部状态。 |

### 9.1 R1 已消费输入

| 输入 | 用途 |
|---|---|
| PR #100 body | R1 合同、字段、四例运行边界、后续依赖。 |
| PR-R0 / #102 文档 | 本地事实锚点，尤其是旧资产继承边界与 Better STM 定义。 |
| [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) | 91 篇 baseline 总账、九个五绿 direct baseline 与数据集清单。 |
| 九个 direct baseline `ASSETS.md` | 代码 / 数据 / artifact / 结果可获取性深审输入。 |
| [../../sources/SUMMARY.md](../../sources/SUMMARY.md) | 787 篇真实控制系统 seed 池规模与状态分布。 |
| PR #93/#94/#96 gh / git 状态 | 分支局部资产状态与消费决策。 |

### 9.2 R1 已产出文件

| 文件 | 状态 |
|---|---|
| [../evidence/baseline_asset_audit.md](../evidence/baseline_asset_audit.md) | 已创建 |
| [../evidence/baseline_candidate_matrix.md](../evidence/baseline_candidate_matrix.md) | 已创建 |
| [../evidence/artifact_availability_ledger.md](../evidence/artifact_availability_ledger.md) | 已创建 |
| [../evidence/format_conversion_matrix.md](../evidence/format_conversion_matrix.md) | 已创建 |
| [../evidence/branch_asset_trace.md](../evidence/branch_asset_trace.md) | 已创建 |
| [../evidence/source_coverage_ledger.md](../evidence/source_coverage_ledger.md) | 已创建 |
| [../evidence/strict_seed_literature_survey.md](../evidence/strict_seed_literature_survey.md) | 已创建 |

### 9.2.1 R1 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| Markdown 相对链接 | 自定义 Python 链接检查脚本，范围 `project_1_llm_state_machine_modeling/paper_stm_repair` | 通过；missing links = 0。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| forbidden wording grep | `grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|NL -> STM.*主贡献" project_1_llm_state_machine_modeling/paper_stm_repair` | 修复 R1 evidence 中的 `最强` 后，命中仅位于 forbidden / 降级 / 自检语境。 |
| `path1_foundation` 修改 | `git diff --name-only origin/paper1/better-stm-repair-loop-umbrella...HEAD | grep path1_foundation` | 通过；无命中。 |
| 四例真实运行 | 按 PR #100 / #104 R1 合同 | 不执行。 |
| 真实 LLM 调用 | 按 R1 范围 | 不执行。 |

### 9.3 R1 已知边界

| 边界 | 说明 |
|---|---|
| 未逐篇深审全部 91 篇 baseline | R1 对 91 篇做 summary-level closure，对 9 个 direct baseline 和部分强近邻做深审；未完成全部 91 篇 strict seed eligibility 闭合。 |
| 未冻结四例 seed | R2 才能基于本审计选择样本；`sources/` 的 337 条 strict-source 子池仍需构造 / 冻结 `STM_0`。 |
| 未验证转换器 | R3 才能把“可转换性评估”变成 schema / fixture / adapter。 |
| 未复跑外部 artifact | 活链接、仓库 HEAD、Drive / 4open / 3GPP dynareport 等正式实验前仍需冻结。 |

## PR-R1.5：strict seed 文献调研与 seed 文库（进行中）

- 时间：2026-06-14 02:22:00
- PR：[#106](https://github.com/HansBug/research_ideas/pull/106)
- 当前状态：implementation review 发现的统计闭合、TTool timing、`designing-fsm-gpt4` initial-only、`req-mermaid-statechart` 无目录等 C/I 已按 bounded snapshot + blocker handoff 口径修复。
- 已产出：`seed_corpus/README.md`、`GUIDE.md`、`SUMMARY.md`、`candidate_matrix.md`、`search_log.md`、`screening_ledger.md`、`exclusion_ledger.md`、`manual_download_queue.md`、`agent_provenance.md` 与 10 个单篇候选目录。
- bounded snapshot v1：candidate matrix 27 条，screening ledger 27 条，单篇全文 / artifact 编码目录 10 个；保守可交接 PR-R2 主 seed 候选为 3 条（`sefm-llm-state-machine`、`llms-emp-stm-subset`、`designing-fsm-gpt4` initial-only），未达到四例下限。
- R2 blocker：PR-R2 必须继续外部检索 / 人工下载、从 `sources/` 构造可追踪 `STM_0`，或用低配 prompt / 学生人工构造补足样本，并记录 provenance 与 leakage control；PR-R1.5 不声称已具备四例冻结输入。
- 检索风险：OpenAlex 两条宽 query 噪声很高，已记录为未筛查 / 早停经验；后续需 exact phrase、排除词、IEEE/ACM/DBLP/publisher 与 snowballing 补强。
- 四例运行：本 PR 不跑四例、不调用真实 LLM、不读取 `.env`。

### Capability-use audit

- Required references/scripts: `ai-research-writing-skill` claim-evidence discipline、`sub-agents` reviewer/reader、Crossref 元数据核验、GitHub PR review comment。
- Inputs consumed: PR #100 body、PR #104 strict seed 协议、baseline/reproduction/sources scout 结果、外部 search planner 结果、implementation reviewers 的 C/I/M 评论。
- Inputs not used and why: IEEE/ACM/DBLP 正式检索与部分 publisher PDF 尚未执行，需要后续联网或人工下载补齐。
- Artifacts produced: `paper_stm_repair/seed_corpus/` bounded snapshot v1、10 个单篇目录、人工下载队列、统计闭合台账。
- Verification run: body 三路 review、implementation 三路 review、统计脚本、Markdown 链接检查、`git diff --check`、GitHub `feedback-smoke`。
- Remaining risk: 当前主 seed 仅 3 条，四例下限交给 PR-R2 作为 blocker；外部下载 / IEEE / ACM / DBLP / snowballing 仍待补。

## 10. PR-R1.6 进度

| 字段 | 状态 |
|---|---|
| PR | [#107](https://github.com/HansBug/research_ideas/pull/107) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | implementation 完成；待三路 review |
| 四例真实运行 | 不需要；本 PR 只做文献与 artifact 审计。 |
| 真实 LLM 调用 | 不需要。 |
| `sources/` 构造 | 本 PR 不执行，只作 fallback handoff。 |
| 当前 bounded snapshot | PR-R1.6 已有 36 candidates / 36 screening / 15 fulltext/artifact dirs / 4 主或条件主 handoff / 11 manual queue。 |
| 目标 | 已补足 PR-R2 可人工裁决的 `>=4` 主 / 条件主候选；R1.6 不冻结最终四例。 |

### 10.1 PR-R1.6 已消费输入

| 输入 | 用途 |
|---|---|
| PR #107 body | R1.6 目标、硬边界、query refinement、negative evidence 门。 |
| PR #100 body | 上游伞 PR 合同与 R1.6 依赖。 |
| PR #106 / PR-R1.5 body | bounded snapshot v1 与 blocker handoff。 |
| [../seed_corpus/SUMMARY.md](../seed_corpus/SUMMARY.md) | 当前 27/27/10/3/6 统计与风险口径。 |
| [../seed_corpus/search_log.md](../seed_corpus/search_log.md) | 早停噪声 query 与 refinement 依据。 |
| [./task-packets/r1.6-strict-seed-expansion.md](./task-packets/r1.6-strict-seed-expansion.md) | 本轮任务包与验收门。 |

### 10.2 PR-R1.6 已产出文件

| 文件 / 目录 | 状态 |
|---|---|
| [../seed_corpus/search_rounds/](../seed_corpus/search_rounds/) | 已初始化并补 3 轮 R1.6 检索记录 |
| [../seed_corpus/seed_selection_candidates.md](../seed_corpus/seed_selection_candidates.md) | 已创建；交接 4 条主 / 条件主候选与 fallback |
| [../seed_corpus/candidate_matrix.md](../seed_corpus/candidate_matrix.md) | 已扩展到 36 条候选 |
| [../seed_corpus/screening_ledger.md](../seed_corpus/screening_ledger.md) | 已扩展到 36 条，与 candidate matrix 对齐 |
| [../seed_corpus/manual_download_queue.md](../seed_corpus/manual_download_queue.md) | 已扩展到 11 条 pending / manual queue |
| [../seed_corpus/SUMMARY.md](../seed_corpus/SUMMARY.md) | 已更新为 bounded snapshot v2 |
| 新增单篇 `papers/<paper-slug>/` 目录 | 新增 5 个：`fsm-gen-iec-61499`、`completion-sysml-gwt`、`fsm-bench-20`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation` |

### 10.3 PR-R1.6 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| 四例真实运行 | 按 PR #107 合同 | 不执行；本 PR 是文献与 artifact 审计。 |
| 真实 LLM / `.env` | 按 PR #107 合同 | 未调用真实 LLM，未读取 `.env`。 |
| candidate/screening ID 对齐 | 自定义 Python 表格检查 | 通过；36 / 36 且 ID 顺序一致。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| Markdown 相对链接 | 自定义 Python 链接检查 | 通过；missing links = 0。 |

### 10.4 R1.6 剩余风险

| 风险 | 处理 |
|---|---|
| `unified-uml-multimodal-validation` 是 synthetic requirements 且 HF license 不清 | 只作为 PR-R2 条件候选；PR-R2 必须 row-level / license 裁决。 |
| `designing-fsm-gpt4` 有 oracle / repair 泄漏风险 | 只允许 initial-generation-only。 |
| `fsm-bench-20` 没有公开 generated outputs | 作为 pipeline fallback；需 PR-R2 复跑冻结后升级。 |
| manual queue 仍有 closed PDF | 记录为 pending，不影响 R1.6 bounded snapshot ready。 |

## 11. PR-R1.7 进度

| 字段 | 状态 |
|---|---|
| PR | [#108](https://github.com/HansBug/research_ideas/pull/108) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | implementation completed；待三路 implementation review |
| 四例真实运行 | 不需要；本 PR 只做文献与 artifact 审计。 |
| 真实 LLM 调用 | 不需要，未读取 `.env`。 |
| 当前 bounded snapshot | R1.7 v4 已有 47 candidates / 47 screening / 24 fulltext dirs / 8 R1.7 rounds / manual queue 状态分布；旧九个 direct baseline 方法层覆盖 9/9。 |
| 关键结论 | seed 方法集合层已补齐旧九个 direct baseline 与 Pushing Envelope；R2 四例样本计数层仍未新增 `计数资格=yes-main/yes-conditional` 主 / 条件主候选；PR-R2 仍需裁决 R1.6 四条并准备 fallback。 |

### 11.1 PR-R1.7 已产出文件

| 文件 / 目录 | 状态 |
|---|---|
| [../seed_corpus/search_rounds/](../seed_corpus/search_rounds/) | 已新增 8 个 R1.7 round |
| [../seed_corpus/search_results/](../seed_corpus/search_results/) | 已新增 R1.7 OpenAlex/Crossref/arXiv/Semantic Scholar/DBLP raw dump |
| [../seed_corpus/candidate_matrix.md](../seed_corpus/candidate_matrix.md) | 已扩展到 47 条候选，增加 priority 列，并补 `pushing-generative-envelope-mbse` |
| [../seed_corpus/screening_ledger.md](../seed_corpus/screening_ledger.md) | 已扩展到 47 条，与 candidate matrix 对齐，增加 priority 列 |
| [../seed_corpus/exclusion_ledger.md](../seed_corpus/exclusion_ledger.md) | 已补 R1.7 boundary / exclusion rows |
| [../seed_corpus/manual_download_queue.md](../seed_corpus/manual_download_queue.md) | 已补 R1.7 状态分布和处理队列 |
| [../seed_corpus/SUMMARY.md](../seed_corpus/SUMMARY.md) | 已更新为 bounded snapshot v4 |
| [../seed_corpus/seed_selection_candidates.md](../seed_corpus/seed_selection_candidates.md) | 已更新 R2 handoff、negative evidence，并明确其不是 seed 方法全集 |
| 新增单篇 `papers/<paper-slug>/` 目录 | 新增 9 个：`nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`integrating-graphical-nl-specifications`、`specification-based-verification-usecase-sm`、`towards-automatic-model-completion`、`pushing-generative-envelope-mbse` |

### 11.2 PR-R1.7 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| 四例真实运行 | 按 PR #108 合同 | 不执行；本 PR 是文献与 artifact 审计。 |
| 真实 LLM / `.env` | 按 PR #108 合同 | 未调用真实 LLM，未读取 `.env`。 |
| candidate/screening ID 对齐 | 自定义 Python 表格检查 | 通过；47 / 47 且 ID 顺序一致。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| Markdown 相对链接 | 自定义 Python 链接检查 | 通过；missing links = 0。 |

### 11.3 PR-R1.7 剩余风险

| 风险 | 处理 |
|---|---|
| 可计主 / 条件主候选仍只有 4 条 | 已在 [../seed_corpus/seed_selection_candidates.md](../seed_corpus/seed_selection_candidates.md) 写出 negative evidence 与 fallback；`fsm-bench-20` 标为 `no-pipeline-output-missing`，不误计。 |
| 新增 classic 论文多为 paper-only | 明确 `SA-3` 不计主 seed，只作 related work / manual reconstruction。 |
| Semantic Scholar API 429 | 已有 blocker round，并用 OpenAlex/Crossref/arXiv/DBLP 替代。 |
| closed/manual 项仍多 | 已给状态分布，不作为 PR-R2 启动 blocker。 |
### 11.4 PR-R1.7 Capability-use audit

- Required references/scripts: `$ai-research-writing-skill` 的 claim-evidence / artifact discipline、`$sub-agents` 的 sidecar review、`gh` PR contract。
- Inputs consumed: PR #108 body、PR #100 伞 PR、PR-R1.6 bounded snapshot v2、R1.7 scout / structure reviewer 输出、OpenAlex/Crossref/arXiv/Semantic Scholar/DBLP raw dumps、9 篇新增全文目录。
- Inputs not used and why: 受 paywall / browser-only / API 429 阻塞的 manual queue 项未强行下载；已在 [../seed_corpus/manual_download_queue.md](../seed_corpus/manual_download_queue.md) 记录 blocker 与 PR-R2 影响。
- Artifacts produced: 47-row candidate / screening ledger、24 个全文 / artifact 编码目录、旧九个 direct baseline crosswalk、8 个 R1.7 search rounds、manual queue 状态分布、R2 handoff negative evidence。
- Verification run: `git diff --check`、candidate/screening ID 对齐、Markdown 相对链接检查、9 个新增单篇目录五件套检查。
- Remaining risk: seed 方法集合已补齐，但按 `计数资格` 可计主 / 条件主候选仍只有 4 条且其中 2 条为条件候选；R2 需要 case-level freeze，并准备 `fsm-bench-20` 复跑或 `sources/` / 低配 prompt / 学生人工 fallback。
