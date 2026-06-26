# story/：论文主线、协议、术语与主张控制

本目录维护第二篇论文的叙事真源。PR-S0-v2 后，本论文不再主打“自动化生成综述”“多智能体流水线本身”或旧的“多阶段证据制品工作流”，而是研究：**研究者如何定义 topic / RQ / scope / meta-model，如何把它投影为可演化 dimension schema，agent 如何在批准 schema 下抽取字段级 content evidence、生成统计观察和 candidate finding signals，研究者如何通过 challenge / counter-evidence / adjudication 形成 final target-domain findings，同时用 process evidence 评价方法自身**。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | PR-S0-v2 核心论点、任务边界、Mermaid 方法总览图、L0--L7 阶段、候选贡献、证据计划和审稿风险。 |
| [protocol.md](./protocol.md) | S0-v2 最小协议；约束后续 A2/A3/A4/A5 的阶段输入输出、G0--G6 human gates、dimension lifecycle、statistical-analysis-to-finding 转移与证据类型。 |
| [terminology_policy.md](./terminology_policy.md) | dimension pattern、pattern-evolving、content/process evidence、statistical analysis、candidate/final finding、survey-of-surveys scaffold、process evidence boundary 等术语口径。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每类潜在主张的证据状态、禁止写法、安全写法和后续所需证据；写摘要、引言、贡献和结论前必须检查。 |
| [differential_novelty_matrix.md](./differential_novelty_matrix.md) | 与 SLR/SMS 方法学、PRISMA、ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等近邻的差异化边界。 |
| [paper_outline.md](./paper_outline.md) | 后续论文稿的章节级架构、pilot / multi-user process evaluation 入口和 PR #101 RQ 到 S0-v2 评价义务的映射。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认主线、方法图、L0--L7、候选贡献和禁用主张。
2. 再读 [terminology_policy.md](./terminology_policy.md)，避免统计分析 / research finding、content evidence / process evidence、candidate / final finding 等术语漂移。
3. 写任何方法或阶段契约前读 [protocol.md](./protocol.md)。
4. 写摘要、引言、贡献、结论或 PR comment 前查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 写相关工作前读 [differential_novelty_matrix.md](./differential_novelty_matrix.md)。
6. 组织论文结构或后续实验 PR 时读 [paper_outline.md](./paper_outline.md)。

## PR-S0-v2 硬约束

- 不把第二篇写成 `sources/` 语料、映射或数据集论文。
- 禁止写智能体完全替代 SLR 专家。
- 禁止写端到端无人自动产出合格 SLR。
- 禁止在检查清单未闭合前写 PRISMA 合规。
- 禁止写完整覆盖、首次自动化 SLR 或首次智能体式 SLR。
- 禁止把统计分析直接写成 final research finding。
- 禁止把 process evidence / student logs 用于 target-domain findings。
- 禁止把 survey-of-surveys 写成目标 evidence pool 或 PRISMA tertiary review。
- 禁止把 pilot / 学生过程数据写成泛化证明。
- 不把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 不把 PR-S0-v2 的评价维度种子写成 A5 已验证指标协议。
