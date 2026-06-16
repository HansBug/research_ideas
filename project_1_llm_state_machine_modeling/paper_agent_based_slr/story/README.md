# story/：论文主线、协议、术语与主张控制

本目录维护第二篇论文的叙事真源。PR-S0 后，本论文不再主打“自动化生成综述”或“多智能体流水线本身”，而是研究：**研究者如何借助可配置脚手架显式化综述元模型，智能体如何在该框架下提出候选研究发现并组织证据链，研究者如何通过质疑闭环修订、降级、保留未解决或确认最终研究发现**。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | PR-S0 后的核心论点、任务边界、方法总览图、阶段契约、候选贡献、证据计划和审稿风险。 |
| [protocol.md](./protocol.md) | 发现导向的最小工作流协议；用于约束后续 A2/A3/A4/A5 的阶段输入、输出、审计门和证据链。 |
| [terminology_policy.md](./terminology_policy.md) | SLR/SMS、元模型、候选 / 最终研究发现、质疑闭环、类 PRISMA、可追踪性等术语口径。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每类潜在主张的证据状态、禁止写法、安全写法和后续所需证据。 |
| [differential_novelty_matrix.md](./differential_novelty_matrix.md) | 与 SLR/SMS 方法学、PRISMA、ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch 等近邻的差异化边界。 |
| [paper_outline.md](./paper_outline.md) | 后续论文稿的章节级架构和 RQ 到评价义务的映射。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认主线、图示、候选贡献和禁用主张。
2. 再读 [terminology_policy.md](./terminology_policy.md)，避免元模型、候选研究发现、最终研究发现、审计门、类 PRISMA 等术语漂移。
3. 写任何方法或阶段契约前读 [protocol.md](./protocol.md)。
4. 写摘要、引言、贡献或结论前查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 写相关工作前读 [differential_novelty_matrix.md](./differential_novelty_matrix.md)。
6. 组织论文结构或后续实验 PR 时读 [paper_outline.md](./paper_outline.md)。

## PR-S0 硬约束

- 不把第二篇写成 `sources/` 语料、映射或数据集论文。
- 禁止写智能体完全替代 SLR 专家。
- 禁止写端到端无人自动产出合格 SLR。
- 禁止在检查清单未闭合前写 PRISMA 合规。
- 禁止写完整覆盖、首次自动化 SLR 或首次智能体式 SLR。
- 不把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 不把 PR-S0 的评价维度种子写成 A5 已验证指标协议。
- 不把候选研究发现直接写成最终研究发现。
- 不把研究者定义的元模型写成 LLM 自动生成或作者预设通用软件工程本体。
