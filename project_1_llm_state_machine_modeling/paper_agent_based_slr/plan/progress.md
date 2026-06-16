# 进度记录：PR-S0 论文主线重新勘定

## 1. 当前状态

| 字段 | 状态 |
|---|---|
| PR | [#114](https://github.com/HansBug/research_ideas/pull/114) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/s0-story-recalibration` |
| 当前阶段 | Mermaid 方法图正式复审 C/I 修复中 |
| 真实 LLM | 未运行；本 PR 不触发 provider 调用 |
| 四个真实例子 | 不运行；本 PR 只冻结论文主线和下游评价义务 |
| Codecov | 纯文档 PR，无可执行代码，Codecov 不适用 |

## 2. 本 PR 的输入来源

| 来源 | 用途 | 当前口径 |
|---|---|---|
| PR-A0 / PR [#103](https://github.com/HansBug/research_ideas/pull/103) | 提供初始目录结构、初始故事、术语和证据政策 | 已合入上游，作为历史输入，不再在当前文档中重复展开 |
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) | 提供 35 篇全文文本级基线调研和“宽泛自动化叙事被击穿”的证据 | 当前 PR-S0 必须吸收其结论 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) | 提供 2026-06-15 导师定调：元模型由使用者定义，SLR 应服务研究发现，研究者可质疑证据 | 当前 PR-S0 的核心约束 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | 提供 sources 相关工作筛选线索 | 仍为 OPEN / 未合入，只能写成快照 / 分支局部证据 |

## 3. 当前交付物

| 文件 | 当前作用 |
|---|---|
| [../README.md](../README.md) | 工作区入口、当前结论、目录导航和禁止主张 |
| [../story/paper_story.md](../story/paper_story.md) | 论文核心论点、任务边界、方法总览图、阶段契约、候选贡献和禁用主张 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | 中英术语锚点、误用防范和高风险写法 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 可写 / 谨慎 / 禁止主张与证据状态 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | 与强近邻工作的差异化边界 |
| [../story/paper_outline.md](../story/paper_outline.md) | 后续论文结构和 PR #101 RQ1--RQ7 到评价义务的映射 |
| [../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md) | PR-S0 只冻结评价维度种子，不冻结公式或阈值 |
| [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) | 当前最高优先级审稿风险和缓解入口 |
| [./task-packets/s0-story-recalibration.md](./task-packets/s0-story-recalibration.md) | 本 PR 的任务范围、拒收检查和验证命令 |

## 4. 已完成修改

1. 将第二篇论文主线从“自动生成综述 / 多阶段证据包工作流”收紧为“研究者引导、发现导向、可审计的智能体式 SLR 支持工作流”。
2. 明确元模型由使用本文方法的研究者基于脚手架裁剪并实例化，而不是作者预设通用本体，也不是 LLM 自动决定。
3. 明确智能体只能提出候选研究发现；最终研究发现必须经过证据链和研究者审计。
4. 在 [../story/paper_story.md](../story/paper_story.md) §6.1 新增 Mermaid 方法总览图，展示研究者责任边界、智能体辅助边界、候选研究发现、证据链、质疑闭环、最终研究发现和报告投影之间的关系。
5. 清理当前 PR 文档中的纯历史流水账，保留必要证据链接，让各 Markdown 尽量自包含、干净、可直接指导后续 PR。
6. 更新 [../evidence/project_inventory.md](../evidence/project_inventory.md)、[../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md) 与 [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，避免证据盘点继续停留在旧 A0 / PR #103 口径。
7. 收敛三路复审的低成本 M 级建议：让证据链状态模板通过研究者批准的 schema 门，并补充“类 PRISMA（PRISMA-style）”术语映射。

## 5. 验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-15 | `git diff --check` | 通过 |
| 2026-06-15 | 文件存在性检查：确认 `README.md`、`story/*`、`experiment_design/*`、`plan/*` 等 PR-S0 必需文件存在 | 通过 |
| 2026-06-15 | Markdown 相对链接检查 | 通过 |
| 2026-06-15 | 禁用强主张 grep：首次自动化 SLR、PRISMA 合规、完整覆盖、智能体替代专家等 | 命中均位于禁止 / 风险语境 |
| 2026-06-16 | 中文化与自包含性检查 | 已清理英文骨架、旧 A0 证据盘点和纯历史流水；三路复审无 C/I |
| 2026-06-16 | Mermaid 方法图检查：`mmdc -p /tmp/puppeteer-no-sandbox.json -i /tmp/pr114_method.mmd -o /tmp/pr114_method.svg` | 通过；已修复节点 / 子图 ID 冲突，并让证据链状态模板进入研究者批准的 schema 门 |
| 2026-06-16 | `git diff --check origin/paper2/agent-based-slr-umbrella...HEAD` | 通过 |
| 2026-06-16 | Markdown 相对链接检查 | 通过 |
| 2026-06-16 | PR-S0 文件存在性检查 | 通过 |
| 2026-06-16 | 低成本 M 级建议收敛检查：A3 进入 R4、补“类 PRISMA”术语映射、更新 review 状态 | 通过 |
| 2026-06-17 | Mermaid 方法图视觉迭代：改为两列紧凑 block 图，真实渲染 PNG 为 584×322，长宽比约 1.81，并人工检查图文一致性 | 通过 |
| 2026-06-17 | Mermaid 方法图二次视觉迭代：两轮 2×3 block 图盲读均发现跨行箭头 / 回边存在 I 级误读风险，改为时序 / 泳道式 sequence 图；最终 v7 真实渲染 PNG 为 784×499，长宽比约 1.57，盲读复述确认 schema 批准权、候选发现边界、schema 回批准门和非自动写作边界均可理解，仅剩字号 / 密度类 M 级建议 | 通过 |

## 6. Review 状态

| 阶段 | reviewer | 结果 | 处理 |
|---|---|---|---|
| 第一轮正式复审 | deepseek reviewer | 0C / 4I / 3M | 已修复 I1--I4；M 级不阻塞 |
| 第一轮正式复审 | claude reviewer | 0C / 0I / 3M | 无阻塞问题 |
| 第一轮正式复审 | codex reviewer | 0C / 0I / 1M | `protocol.md` 旧线性口径留给后续 A2 |
| 中文化与方法图复审 | codex reviewer | 0C / 0I / 0M | 通过 |
| 中文化与方法图复审 | claude reviewer | 0C / 0I / 3M | 已收敛低成本 M：方法图 A3 过研究者 schema 门；其余 M 不阻塞 |
| 中文化与方法图复审 | deepseek reviewer | 0C / 0I / 2M | 已收敛低成本 M：补“类 PRISMA”术语映射；Mermaid 前缀共享不阻塞 |
| 序列图最终复审 | codex reviewer | 0C / 1I / 0M | I1 指出 §7 提前写“三路最终复审无 C/I”，本提交改为不预判并等待复审闭合 |
| 序列图最终复审 | claude reviewer | 0C / 0I / 2M | 无阻塞问题；M 级为字号 / A4 命名一致性 |
| 序列图最终复审 | deepseek reviewer | 0C / 0I / 2M | 无阻塞问题；M 级为 §6 复审表补记与候选→最终提示 |

## 7. 剩余风险

1. PR-S0 仍是论文主线和合同冻结，不提供真实运行证据；后续不能把当前候选贡献写成结果。`e86faf38` 后的正式复审结论以 PR comments 与本节后续更新为准；若无 C/I，再将剩余项降为不阻塞 M 级建议。
2. Mermaid 图是方法总览草案，不表示运行时已经实现；当前图已通过真实渲染和视觉检查，但后续 A2/A3/A4/A5 若改变阶段契约仍需同步更新。
3. 相关工作仍需 A6 深化，尤其是 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻。
4. 评价公式、阈值、统计协议、真实场景和运行记录必须由后续 A2/A3/A4/A5 接走。
