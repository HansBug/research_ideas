# legacy asset inheritance：旧资产继承边界

## 1. 总原则

本工作区不拥有、不修改、不继承 `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/`。旧资产只能作为历史线索、结构经验或待盘点候选，不能把旧 story、旧 claim、旧样本或旧实验门直接搬入新主线。

## 2. 旧资产分类

| 资产 | 当前状态 | 可复用内容 | 不可继承内容 |
|---|---|---|---|
| [../../paper_v1/README.md](../../paper_v1/README.md) | `main` 已有历史入口 | 2026-05 Direction-Decision Sprint 背景。 | “第一篇仍在 Path-1/Path-2 决策阶段”的当前性口径。 |
| [../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md](../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md) | `main` 已有历史 guide | baseline hard comparison 的风险、旧实验边界线索。 | 把第一篇继续写成 direct `NL -> STM` hard comparison。 |
| [../../paper_v1/PATH2_DIFFERENTIATION_GUIDE.md](../../paper_v1/PATH2_DIFFERENTIATION_GUIDE.md) | `main` 已有历史 guide | 控制系统差异化、数据来源线索。 | 把 Path-2 直接压回第一篇主线。 |
| PR #93 `path1_foundation/` | #93 分支局部 | “入口 + story + evidence + experiment_design + plan”的分层经验。 | 目录所有权、旧 `NL -> STM` story、旧文件事实状态。 |
| PR #94 direct baseline 盘点 | #93 分支局部 | baseline 反证、候选 prior artifact 线索。 | 未经 R1 复核即写成可运行 / 可转换 / 可比较。 |
| PR #96 旧 story 重构 | #93 分支局部 | claim gate、弱化 DSL、outline 的可复用论证。 | 旧 S0a 主线和未进 `main` 的文件状态。 |
| [../../baselines/](../../baselines/) | `main` 已有 | R1 资产盘点入口。 | R0 阶段直接断言可转换 / 可运行。 |
| [../../sources/](../../sources/) | `main` 已有 | R1/R2 seed 池线索。 | R0 阶段直接冻结样本或 Top-N。 |

## 3. 新旧 story 的覆盖关系

| 旧口径 | 新 R0 口径 |
|---|---|
| 第一篇是 `NL -> STM` generation / hard comparison。 | 第一篇是 `<NL, STM_0> -> STM_k / Better STM` repair / refinement。 |
| baseline 是 direct competitor。 | baseline 兼作 seed source、converter pressure、error taxonomy、有限对照和 related work。 |
| `fcstm` 容易被推成新 DSL。 | 语义增强、可机检、可执行表示只是 feedback loop 的实验载体。 |
| run record / pipeline 可能被写进方法贡献。 | 它们只作内部审计和复现证据链，不作为论文贡献。 |

## 4. 后续 R1 任务入口

R1 应重新盘点旧 baseline / prior artifact：论文元数据、PDF、代码、demo、artifact、NL 输入、输出格式、许可证、可转换性、转换风险、是否适合四例样本、是否适合主实验、是否只作 related work。

R0 不提前替 R1 做任何条目级判断。
