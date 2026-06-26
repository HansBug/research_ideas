# 进度记录：PR-S0-v2 论文主线重新勘定

## 1. 当前状态

| 字段 | 状态 |
|---|---|
| PR | [#114](https://github.com/HansBug/research_ideas/pull/114) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/s0-story-recalibration` |
| 当前阶段 | S0-v2 文档大修与首轮正式复审 I/M 修复已推送为 `1cc50aca`，状态同步提交为 `ed55b912`；当前复审目标为 `ed55b912`，`feedback-smoke` 已通过 |
| 真实 LLM | 未运行；本 PR 不触发 provider 调用 |
| 四个真实例子 | 不运行；本 PR 只冻结论文主线、术语和下游评价义务 |
| Codecov | 纯文档 PR，无可执行代码，Codecov 不适用 |

## 2. 本 PR 的输入来源

| 来源 | 用途 | 当前口径 |
|---|---|---|
| PR-A0 / PR [#103](https://github.com/HansBug/research_ideas/pull/103) | 提供初始目录结构、初始 story 与协议雏形 | 历史输入；当前 story 以 S0-v2 为准 |
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) | 提供 35 篇全文文本级近邻 baseline 和“宽泛自动化 story 被击穿”的证据 | 当前 PR-S0-v2 必须吸收其结论 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) | 提供 2026-06-15 导师定调：meta-model 由使用者定义、SLR 需要 research finding、agent 只能提出 candidate findings | S0-v2 的正式上游约束 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) | 提供 2026-06-24/26 导师定调：三阶段 SLR、dimension pattern、statistical analysis / research finding 分层、human-in-the-loop、pilot 与 process data | S0-v2 的最高优先级新增约束 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | 提供 sources 相关工作筛选线索 | 仍为 OPEN / 未合入，只能写成 snapshot / 分支局部证据 |

## 3. 当前交付物

| 文件 | 当前作用 |
|---|---|
| [../README.md](../README.md) | 工作区入口、S0-v2 当前结论、目录导航和禁止主张 |
| [../story/paper_story.md](../story/paper_story.md) | S0-v2 论文核心论点、任务边界、方法总览图、L0--L7、候选贡献和禁用主张 |
| [../story/protocol.md](../story/protocol.md) | 模式演化、字段证据、统计观察、finding challenge 与 G0--G6 gate 的最小协议 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | 术语、证据类型、finding 状态和高风险写法 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 可写 / 谨慎 / 禁止主张与证据状态，特别约束 statistical/finding、content/process、pilot/student data 边界 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | 与强近邻工作的 S0-v2 差异化边界 |
| [../story/paper_outline.md](../story/paper_outline.md) | 后续论文结构、pilot、multi-user process evaluation 与 RQ 到评价义务映射 |
| [../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md) | S0-v2 评价维度种子，不冻结公式或阈值 |
| [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) | 当前最高优先级审稿风险和缓解入口 |
| [./task-packets/s0-story-recalibration.md](./task-packets/s0-story-recalibration.md) | 本 PR 的任务范围、拒收检查和验证命令 |

## 4. 已完成修改

1. 将第二篇论文主线从旧“研究者引导、发现导向、可审计证据流”升级为“研究者引导、模式演化、证据支撑、发现导向的智能体式 SLR/SMS 支持方法”。
2. 将真实 SLR 明确拆成三层：论文收集与初步处理、维度 pattern 驱动的论文分析、统计分析与 research finding 形成。
3. 在 [../story/paper_story.md](../story/paper_story.md) 中更新 Mermaid 方法总览图，显式包含 L0--L7、G0--G6、content evidence、statistical analysis、candidate finding、final adjudication 与 process evidence boundary。
4. 在 [../story/protocol.md](../story/protocol.md) 中明确 dimension pattern lifecycle、schema revision / impact analysis / backfill、statistical-analysis-to-finding 转移规则、survey-of-surveys scaffold 边界、pilot 与学生过程数据边界。
5. 在 [../story/terminology_policy.md](../story/terminology_policy.md) 中新增 dimension pattern、pattern-evolving、content/process evidence、statistical analysis、candidate finding signal、target-domain finding、method-evaluation finding、G0--G6 等术语。
6. 重写 [../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/paper_outline.md](../story/paper_outline.md)、[../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)、[../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)，修复内部 reviewer 指出的旧 S0 落点不同步问题。
7. 更新入口 README、story README、task packet 和 project inventory，使下一位 agent 能直接按 S0-v2 接手。

## 5. LLM4STM / LLM4Modeling dry-run 口径检查

本 PR 不运行真实 LLM；这里只做文档可执行性 dry-run，检查 S0-v2 文档是否能指导一个贴近博士主线的主题。

| Step | LLM4STM dry-run 示例 | 文档是否能指导 |
|---|---|---|
| L0 meta-model | 研究者定义 topic=`LLM-based STM generation`，RQ 包含输入材料、输出 STM 谱系、方法/agent 使用、评价与复现资产 | [paper_story.md](../story/paper_story.md) 与 [protocol.md](../story/protocol.md) 能说明研究者拥有 meta-model |
| L1 scaffold / seed probing | 从既有 LLM4SE / MDE survey 与少量 STM generation 种子论文提取候选字段 | [protocol.md](../story/protocol.md) 明确 survey-of-surveys 只是 scaffold |
| L2 dimension schema | 字段树可含输入材料类型、输出 STM 类型、状态/迁移/guard/action/clock、LLM/agent 类型、评价指标、artifact 可用性 | [terminology_policy.md](../story/terminology_policy.md) 定义 dimension pattern 与 pattern-evolving |
| L4 field evidence | 每篇论文字段必须带 page/section/quote/table/artifact URL 或 missing/uncertainty | [protocol.md](../story/protocol.md) §2/§4 能指导 content evidence |
| L5 statistical analysis | 统计不同 STM 输出谱系、agent 使用程度、公开 artifact 比例、评价方式分布 | [protocol.md](../story/protocol.md) §5 禁止统计结果直接升级 finding |
| L6 candidate signal | 例如“多数 LLM4STM 论文缺少 machine-checkable evaluation”只能作为 candidate signal | [claim_evidence_map.md](../story/claim_evidence_map.md) 明确 candidate/final 边界 |
| L7 adjudication | 研究者检查反例、范围、强度；可能降级为“在当前样本中观察到 artifact/evaluation 透明度不足” | [paper_outline.md](../story/paper_outline.md) 与 risk register 能指导 challenge/adjudication |
| Process evidence | 记录 schema 修订、backfill、challenge 和人工时间，用于 method-evaluation | [evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md) 已把 process metrics 分离 |

Dry-run 结论：当前文档已经能把 LLM4STM 主题从“普通综述自动化”导向 dimension schema、field evidence、统计观察、candidate signal 与 researcher adjudication 的闭环；后续 A3/A5 仍需真实 pilot 和 run record 才能写结果。

## 6. 验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-26 | 合入 `origin/paper2/agent-based-slr-umbrella` | 通过；merge commit `47ce6cc3`，无冲突 |
| 2026-06-26 | 三路 PR body 计划阶段 review | 0C/0I，可进入实现；M 级建议已吸收进 S0-v2 文档方向 |
| 2026-06-26 | 内部 subagent 只读检查 | 发现 C/I：多份 downstream 文档仍旧 S0、L8/G6 不一致、方法图缺 G6；本轮已修复 |
| 2026-06-26 | LLM4STM / LLM4Modeling dry-run 口径检查 | 通过；文档能指导 dimension pattern → field evidence → statistical analysis → candidate signal → adjudication |
| 2026-06-26 | `git diff --check` | 通过 |
| 2026-06-26 | PR-S0-v2 必需文件存在性检查 | 通过；`paper_agent_based_slr PR-S0-v2 packet ok` |
| 2026-06-26 | 禁止强主张 grep | 通过；命中均位于禁止 / 风险 / 安全边界 / grep 规则语境中，不是正向主张 |
| 2026-06-26 | Markdown 相对链接检查 | 通过；`markdown relative links ok` |
| 2026-06-26 | Mermaid 渲染检查：`mmdc -p /tmp/puppeteer-no-sandbox-pr114.json -i /tmp/pr114_s0v2_method.mmd -o /tmp/pr114_s0v2_method.svg` | 通过；SVG 已生成，本地大小 44619 bytes |
| 2026-06-26 | 首轮正式复审修复验证：`git diff --check`、必需文件检查、Markdown 相对链接检查、Mermaid 渲染、旧 story grep | 通过；`baselines/SUMMARY.md` 旧 S0 正向 story 口径已同步为 S0-v2，grep 无旧正向叙事命中 |
| 2026-06-26 | `ed55b912` 状态同步提交复核 | 通过；该提交仅修改 `plan/progress.md` 当前阶段 1 行，不改变 S0-v2 方法合同；当前复审目标为 `ed55b912` |

## 7. Review 状态

| 阶段 | reviewer | 结果 | 处理 |
|---|---|---|---|
| PR body 计划阶段 | deepseek reviewer | 0C / 0I / 3M | 可进入实现；M 已吸收为术语和风险补强 |
| PR body 计划阶段 | codex reviewer | 0C / 0I | 可进入实现 |
| PR body 计划阶段 | claude reviewer | 0C / 0I / 少量 M | 可进入实现 |
| 内部实现中只读检查 | verifier subagent | C/I：多数落点旧 S0、L8/G6 不一致、方法图缺 G6；PR body / progress 状态与验证记录曾不同步 | 已重写 claim / outline / eval / risk / README / task / progress，并修正 L8/G6；本轮验证记录与 PR body 已同步到 `ed55b912` |
| 内部实现中学术审查 | critic subagent | C/I：outline、claim map、evaluation、risk、novelty matrix、project inventory 未同步 S0-v2；旧 evidence-package 叙事残留 | 已逐项修复，并把旧叙事 grep 标为人工审查线索而非硬 gate |
| 正式三路复审 | codex / claude / deepseek | 首轮已执行：codex 0C/0I/2M，claude 0C/0I/4M；deepseek 路发现 baselines 旧 story 口径 I 且身份 comment 需重发 | 已修复 deepseek I 与低成本 M；当前以 `ed55b912` 作为小 diff 复审对象 |

## 8. 剩余风险

1. 当前 PR-S0-v2 仍是 story 和合同冻结，不提供真实运行证据；后续不得把候选贡献写成结果。
2. Mermaid 方法图是方法总览草案；若 A2/A3/A4/A5 改变阶段契约、schema 或证据字段，必须同步更新。
3. survey-of-surveys scaffold 仍是计划证据；后续若执行，必须避免写成目标 evidence pool 或 complete tertiary review。
4. 学生 process data 仍是计划；A5 前必须冻结 consent、匿名化、脱敏、教学关系隔离和访问权限。
5. 相关工作仍需 A6 深化，尤其是 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻；`baselines/SUMMARY.md` 已完成 S0-v2 方向性同步，但正式论文写作前仍需逐篇 PDF / artifact audit。
