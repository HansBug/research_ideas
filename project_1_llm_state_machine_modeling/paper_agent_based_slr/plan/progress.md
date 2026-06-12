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
- 按用户要求复刻旧 Path-1 的 `story/ evidence/ experiment_design/ plan/` 主结构，但不创建 `foundation/` 子路径。
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
| PR #97 仍 OPEN / 未合入 | 已建立 fact drift policy | A1 merge 或冻结 snapshot。 |
| 没有真实场景和运行 | A0 已补 [dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，但不冻结场景 | A3/A4/A5。 |
| A5 指标未冻结 | A0 非目标 | A5。 |

## 6. Capability-use audit

- Required references/scripts：`ai-research-writing-skill` 的 story gate；`sub-agents` / 三路 reviewer 合同审查；旧 Path-1 PR #96 路径结构。
- Inputs consumed：PR #101 body、PR #99 会后定调 comment、已合入导师讨论记录、PR #97 状态、PR #96 文件结构、三路 reviewer comment。
- Inputs not used and why：未读取或复制 PR #97 PDF / fulltext；A0 只做合同与证据层级，不复制未合入资产。
- Artifacts produced：`paper_agent_based_slr/` 下 README、story、evidence、experiment_design、plan 全部 A0 文件。
- Verification run：`source venv/bin/activate` 后运行 A0 Python sanity、Markdown 相对链接检查、成片英文检查、emoji 列检查、`git diff --check`，并用 DOI metadata 获取 A0 `references.bib` 种子。
- Remaining risk：真实 related-work coverage、benchmark scenarios、LLM run records 和 A5 metrics 尚未构造。
