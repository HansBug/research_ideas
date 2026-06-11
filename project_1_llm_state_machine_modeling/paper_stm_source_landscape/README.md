# STM source landscape paper workspace

## 1. 定位

本目录是 issue #85 的独立 paper workspace，服务于 **control-system STM corpus / benchmark-source landscape** 论文。它与 [`../paper_v1/`](../paper_v1/) 并列，不是 `paper_v1` 的后续版本，也不得使用带顺序含义的版本化命名。

本目录复刻 PR #96 `paper_v1/path1_foundation/` 的 paper-workspace 分层：用 `story/` 管论文主线，用 `evidence/` 管证据桥接，用 `baselines/` 管 related-work / baseline 初筛，用 `dataset_selection/` 管 `sources/` corpus 边界，用 `experiment_design/` 管 RQ / protocol / reviewer risk，用 `plan/` 管当前 PR 进度与 task packet。

## 2. 当前论文主线

> 从长期维护的控制系统论文库中，用 retrospective systematic mapping + audit protocol，把论文中的状态机 / 模式切换 / 门控逻辑案例转化为可追溯、可分层、版权安全的 LLM 状态机建模 benchmark-source landscape。

当前统计只是 planning baseline：`sources/` 中 787 篇论文、746 条正例案例、FSM/EFSM/HSM/Timed/Hybrid 等标签都必须在正式 manuscript snapshot 中用脚本复算后才能进入论文结果。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文 thesis、gap、contribution 边界、terminology policy、outline、venue gate 与 claim-evidence gate | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、#95/#85 初筛与论文 story / claim gate 的桥接 | [evidence/README.md](./evidence/README.md) |
| [baselines/](./baselines/) | D1--D7 related-work / baseline 初筛矩阵、下载审计、人工下载 handoff、排除候选审计 | [baselines/README.md](./baselines/README.md) |
| [dataset_selection/](./dataset_selection/) | `sources/` corpus snapshot、scope、后续 benchmark-card 输入边界 | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | RQ、protocol、execution gate、reviewer risk register | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前 PR 任务状态、review 记录和 task packet | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

1. [story/paper_story.md](./story/paper_story.md)
2. [story/claim_evidence_map.md](./story/claim_evidence_map.md)
3. [baselines/SUMMARY.md](./baselines/SUMMARY.md)
4. [baselines/MANUAL_DOWNLOAD_REQUESTS.md](./baselines/MANUAL_DOWNLOAD_REQUESTS.md)
5. [baselines/data/auto_fulltext_light_review_gate.csv](./baselines/data/auto_fulltext_light_review_gate.csv)
6. [evidence/baseline_and_related_work_matrix.md](./evidence/baseline_and_related_work_matrix.md)
7. [experiment_design/execution_plan.md](./experiment_design/execution_plan.md)
8. [plan/progress.md](./plan/progress.md)

## 5. 非目标

1. 本目录不提交 PDF、出版社全文、长摘录或未授权全文抽取物。
2. 本 PR 不写 manuscript 正文，不声称完成最终 Related Work。
3. 本 PR 不把 #95 的 438 篇候选包装成 #85 的 systematic review corpus。
4. 本 PR 不声称 #85 是 `paper_v1` 的后续版本。

## 6. 当前验收标准

- [x] 目录结构与 PR #96 `path1_foundation/` 同构，并明确与 `paper_v1/` 并列。
- [x] #95 的 438 行候选有全量筛选审计入口。
- [x] #85 初筛 69 行候选有 D1--D7 独立打分与 rationale。
- [x] P0/P1 的 25 条人工下载 BibTeX 已落地。
- [x] 7 条 `auto_fulltext_light_review_flag=yes` 候选已列入复查 gate，复查前不得最终排除。
- [ ] 后续多智能体学术 review 无 C/I 级事实、学术、可执行性问题；M 级进入 follow-up。
