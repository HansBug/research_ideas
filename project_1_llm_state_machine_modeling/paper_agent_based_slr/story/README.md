# 主线/：论文主线、协议、术语与主张控制

本目录维护第二篇论文的叙事真源。当前阶段后，本论文不再主打“自动化生成综述”“多智能体流水线本身”或旧的“多阶段证据制品工作流”，而是研究：**研究者如何定义主题、研究问题、范围和综述元模型，如何把它投影为可演化维度模式，智能体如何在批准模式下抽取字段级内容证据、生成统计观察和候选发现，研究者如何通过质疑、反向证据和裁决形成最终领域发现，同时用过程证据评价方法自身**。

术语写作规则：首次出现必须采用“中文术语（English term / abbreviation）”格式，例如“系统综述（Systematic Literature Review, SLR）”；首次定义后，除论文名、工具名、路径、命令、阶段编号和必要缩写外，一律优先使用中文术语。完整术语表见 [terminology_policy.md](./terminology_policy.md)。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | 当前阶段核心论点、任务边界、两类 Mermaid 方法图、L0--L7 阶段、候选贡献、证据计划和审稿风险。 |
| [protocol.md](./protocol.md) | S0-v2 最小协议；约束后续设计、试运行、真实运行与评价的阶段输入输出、G0--G6 人工门控、维度模式生命周期、统计分析到发现的转移与证据类型。 |
| [terminology_policy.md](./terminology_policy.md) | 维度模式、模式演化、内容证据 / 过程证据、统计分析、候选 / 最终发现、脚手架、过程证据边界等术语口径。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每类潜在主张的证据状态、禁止写法、安全写法和后续所需证据；写摘要、引言、贡献和结论前必须检查。 |
| [differential_novelty_matrix.md](./differential_novelty_matrix.md) | 与系统综述 / 系统映射研究方法学、PRISMA、ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等近邻的差异化边界。 |
| [paper_outline.md](./paper_outline.md) | 后续论文稿的章节级架构、试运行 / 多用户过程评价入口和 PR #101 研究问题到 S0-v2 评价义务的映射。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认主线、方法图、L0--L7、候选贡献和禁用主张。
2. 再读 [terminology_policy.md](./terminology_policy.md)，避免统计分析 / 研究发现、内容证据 / 过程证据、候选发现 / 最终发现等术语漂移。
3. 写任何方法或阶段契约前读 [protocol.md](./protocol.md)。
4. 写摘要、引言、贡献、结论或 PR 评论 前查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 写相关工作前读 [differential_novelty_matrix.md](./differential_novelty_matrix.md)。
6. 组织论文结构或后续实验 PR 时读 [paper_outline.md](./paper_outline.md)。

## 当前阶段硬约束

- 不把第二篇写成 `sources/` 语料、映射或数据集论文。
- 禁止写智能体完全替代系统综述专家。
- 禁止写端到端无人自动产出合格系统综述。
- 禁止在检查清单未闭合前写 PRISMA 合规。
- 禁止写完整覆盖、首次自动化系统综述或首次智能体式系统综述。
- 禁止把统计分析直接写成最终研究发现。
- 禁止把过程证据 / 学生日志用于领域发现。
- 禁止把脚手架写成目标证据池或 PRISMA 三级综述。
- 禁止把试运行 / 学生过程数据写成泛化证明。
- 不把 PR #97 未合入资产写成 `main` 已有事实。
- 不把当前阶段的评价维度种子写成后续评价已验证指标协议。
