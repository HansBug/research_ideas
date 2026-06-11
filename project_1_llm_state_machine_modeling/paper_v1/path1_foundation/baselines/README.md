# Path-1 S1a 九大 Baseline 专项盘点

本目录是 Path-1 第一篇论文 foundation 工作区下的 baseline 专项盘点入口，服务于 PR-S1a：九大 direct baseline 的事实吸收、可比性分析、claim 风险控制和 S1b/S3 handoff。

## 1. 目录定位

本目录不是新的 baseline 文库，也不替代 [`../../../baselines/`](../../../baselines/) 的原始 baseline corpus。它只围绕 Path-1 第一篇论文，抽取九个五绿 direct baseline 中对论文 story、Related Work、competitor matrix、same-sample approximate baseline 和 claim-evidence gate 直接有用的信息。

信息流如下：

```text
../../../baselines/<baseline-slug>/
  ├── bibtex.bib
  ├── paper_content.txt
  ├── DESC.md
  └── ASSETS.md
        ↓ 逐篇事实吸收
./papers/<baseline-slug>.md
        ↓ 跨论文总账化
./SUMMARY.md
        ↓ 后续 handoff
../story/claim_evidence_map.md
../experiment_design/execution_plan.md
S1b / S3 执行 PR
```

## 2. 文件职责

| 文件 / 目录 | 职责 | 注意事项 |
|---|---|---|
| [`SUMMARY.md`](./SUMMARY.md) | 九大 baseline 总账；按方法框架、资产状态、生成流程内反馈、事后评测、同样本可比性、claim 风险与 handoff 六类表格整理全部信息 | 不写成短摘要；必须能直接服务 S1b/S3 |
| [`GUIDE.md`](./GUIDE.md) | 本目录维护、字段合同、review gate 与本地检查命令 | 后续 agent / reviewer 必读；若与 README 冲突，以 GUIDE 的执行细则为准 |
| [`papers/`](./papers/) | 每篇 baseline 一个详细 Markdown 文件 | 文件名使用原 baseline 目录 slug，保证稳定链接 |
| `papers/*.md` | 展开单篇论文的六类表格、阅读审计、source pointer、风险和 handoff | 每个关键判断都要有原文或既有派生文件依据 |

## 3. 阅读顺序

1. 先读本文件，理解本目录只服务 Path-1 第一篇论文。
2. 再读 [`GUIDE.md`](./GUIDE.md)，确认字段合同、红线和 review gate。
3. 再读 [`SUMMARY.md`](./SUMMARY.md)，把握九大 baseline 的总体分类、反证压力和可比性结论。
4. 若要核对某篇论文事实，再进入 [`papers/`](./papers/) 下对应逐篇文件。
5. 若对逐篇文件中的事实仍有疑问，回到原始 baseline 目录读取 `bibtex.bib -> paper_content.txt -> DESC.md -> ASSETS.md`。

## 4. 与其他文件的关系

- [`../evidence/baseline_and_related_work_matrix.md`](../evidence/baseline_and_related_work_matrix.md)：提供 foundation 阶段的 baseline 初始矩阵和 mandatory closest works 线索。本目录的 [`SUMMARY.md`](./SUMMARY.md) 是 S1a 执行后的正式专项总账，允许吸收该矩阵的分类线索，但必须以逐篇全文核验和六类表格为准。
- [`../../../baselines/SUMMARY.md`](../../../baselines/SUMMARY.md)：是 Project 1 baseline corpus 总账。本目录只抽取其中 9 个五绿 direct baseline 与 PR #92 census 边界审计，不替代原总账。
- [`../story/claim_evidence_map.md`](../story/claim_evidence_map.md)：后续 S1b/S5 可从本目录的 claim 风险表吸收 claims-to-avoid 和可保留 claim。
- [`../experiment_design/execution_plan.md`](../experiment_design/execution_plan.md)：后续 S3 可从本目录的 same-sample approximate 和 handoff 表吸收 baseline runner / prompt / output normalization 决策。

## 5. 关键口径

1. **生成流程内反馈**只统计会影响 LLM 生成、抽取、修复或再生成的反馈。GT F1、专家评分、SME rubric 等只用于事后评测，不得写成 in-loop feedback。
2. **人在回路**并入方法框架表：必须区分可无人工、生成流程内人工、人工后编辑和仅事后人工评估。
3. **形式化验证**只在论文明确使用 model checker、theorem prover、SAT/SMT solver 或等价形式化引擎时填写。schema、grammar、JSON、PlantUML parse、consistency rules 默认是静态/半形式化检查，不得写成完整 formal verification。
4. **输出 STM 类型**不能只写名称，必须解释语义能力、可执行性、guard/action/hierarchy/time/concurrency 支持、应用场景和与本项目 STM schema 的差距。
5. **不可复现**不是 prior work 弱点；只能记录为 artifact / assumption / output mismatch 或 same-sample approximate blocker。


## 6. 高重要性与长任务原则

S1a 直接决定 Path-1 第一篇论文的 novelty、baseline fairness、Related Work 定位和实验路线冻结，属于高风险学术审计任务。维护本目录时必须遵守以下原则：

1. 信息完整性优先：不得只读摘要或既有 `DESC.md` 后下结论；关键判断必须回到论文全文、`paper_content.txt`、`ASSETS.md` 或 artifact。
2. 事实准确性优先：任何会影响 novelty、same-sample approximate baseline、claim-to-avoid 或 S3 实验设计的事实错误都应按 C/I 处理。
3. 大量 subagent 分工：执行或复审时应按论文集合、字段体系或 claim 风险拆分给多个 subagent 并行核验；subagent 输出必须列明读取范围、文件路径和 source pointer。
4. 强对抗审稿：reviewer 应主动寻找 prior work 打穿本文 claim、in-loop feedback 与 post-hoc evaluation 混淆、人在回路误述、输出 STM 能力夸大、formal verification 误写和可复现性误判。
5. 本目录结论只作为后续 S1b/S3 的事实底座；不得把未核验推断直接写成论文强 claim。

## 7. 当前状态

本目录由 PR-S1a 初始化，用于承载九大 baseline 专项盘点。当前目标是形成可被后续 S1b/S3 直接使用的事实底座，而不是撰写最终 Related Work 成稿。
