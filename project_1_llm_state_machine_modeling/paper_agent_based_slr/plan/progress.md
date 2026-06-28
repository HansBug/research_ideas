# 进度记录：PR-S0-v2 论文主线重新勘定

## 1. 当前状态

| 字段 | 状态 |
|---|---|
| PR | [#114](https://github.com/HansBug/research_ideas/pull/114) |
| 上游 | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/s0-story-recalibration` |
| 当前阶段 | S0-v2 文档大修、首轮正式复审 I/M 修复、2026-06-27 术语中文化与双图补强已完成本地验证、内部最终复核并已推送；正式三路复审围绕 PR 当前 HEAD 进行，GitHub checks 以 PR 页面最新状态为准 |
| 真实大语言模型 | 未运行；本 PR 不触发提供商调用 |
| 四个真实例子 | 不运行；本 PR 只冻结论文主线、术语和下游评价义务 |
| Codecov | 纯文档 PR，无可执行代码，Codecov 不适用 |

## 2. 本 PR 的输入来源

| 来源 | 用途 | 当前口径 |
|---|---|---|
| PR-A0 / PR [#103](https://github.com/HansBug/research_ideas/pull/103) | 提供初始目录结构、初始主线与协议雏形 | 历史输入；当前主线以 S0-v2 为准 |
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) | 提供 35 篇全文文本级近邻基线和“宽泛自动化主线被击穿”的证据 | 当前 PR-S0-v2 必须吸收其结论 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) | 提供 2026-06-15 导师定调：综述元模型由使用者定义，系统综述需要研究发现，智能体只能提出候选发现 | S0-v2 的正式上游约束 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) | 提供 2026-06-24/26 导师定调：三阶段系统综述、维度模式、统计分析 / 研究发现分层、人在回路、试运行与过程数据 | S0-v2 的最高优先级新增约束 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | 提供 sources 相关工作筛选线索 | 仍为 未合入，只能写成快照 / 分支局部证据 |

## 3. 当前交付物

| 文件 | 当前作用 |
|---|---|
| [../README.md](../README.md) | 工作区入口、S0-v2 当前结论、目录导航和禁止主张 |
| [../story/paper_story.md](../story/paper_story.md) | S0-v2 论文核心论点、任务边界、方法总览图、L0--L7、候选贡献和禁用主张 |
| [../story/protocol.md](../story/protocol.md) | 模式演化、字段证据、统计观察、发现质疑与 G0--G6 人工门控的最小协议 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | 术语、证据类型、发现状态和高风险写法 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 可写 / 谨慎 / 禁止主张与证据状态，特别约束统计分析 / 发现、内容证据 / 过程证据、试运行 / 学生数据边界 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | 与强近邻工作的 S0-v2 差异化边界 |
| [../story/paper_outline.md](../story/paper_outline.md) | 后续论文结构、试运行、多用户过程评价与研究问题到评价义务的映射 |
| [../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md) | S0-v2 评价维度种子，不冻结公式或阈值 |
| [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) | 当前最高优先级审稿风险和缓解入口 |
| [./task-packets/s0-story-recalibration.md](./task-packets/s0-story-recalibration.md) | 本 PR 的任务范围、拒收检查和验证命令 |

## 4. 已完成修改

1. 将第二篇论文主线从旧“研究者引导、发现导向、可审计证据流”升级为“研究者引导、模式演化、证据支撑、发现导向的智能体式系统综述 / 系统映射研究支持方法”。
2. 将真实系统综述明确拆成三层：论文收集与初步处理、维度模式驱动的论文分析、统计分析与研究发现形成。
3. 在 [../story/paper_story.md](../story/paper_story.md) 中更新 SVG 普通流程图与 Mermaid 时序 / 泳道图，显式包含 L0--L7、G0--G6、内容证据、统计分析、候选发现、最终裁决与过程证据边界。
4. 在 [../story/protocol.md](../story/protocol.md) 中明确维度模式生命周期、模式修订 / 影响分析 / 回填、统计分析到研究发现的转移规则、脚手架边界、试运行与学生过程数据边界。
5. 在 [../story/terminology_policy.md](../story/terminology_policy.md) 中新增并中文化维度模式、模式演化、内容证据 / 过程证据、统计分析、候选发现、领域发现、方法发现、G0--G6 等术语。
6. 重写 [../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/paper_outline.md](../story/paper_outline.md)、[../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)、[../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)，修复内部审查者指出的旧 S0 落点不同步问题。
7. 更新入口 README、story README、任务包和 项目证据清单，使下一位智能体能直接按 S0-v2 接手。
8. 按 2026-06-27 新增要求，补强术语首次出现规则：关键术语首次出现采用“中文术语（英文术语 / 缩写）”，后续正文优先使用中文主称；同时在 [../story/paper_story.md](../story/paper_story.md) 引入可控 SVG 普通流程图，与原 Mermaid 时序 / 泳道图互补说明阶段、参与者、制品、反馈和过程证据边界。

## 5. 基于大语言模型的状态机建模主题（LLM4STM / LLM4Modeling）试读检查口径

本 PR 不运行真实大语言模型；这里只做文档可执行性试读检查，检查 S0-v2 文档是否能指导一个贴近博士主线的主题。

| 步骤 | LLM4STM 试读检查示例 | 文档是否能指导 |
|---|---|---|
| L0 综述元模型 | 研究者定义主题为“基于大语言模型的状态机生成”，研究问题包含输入材料、输出状态机谱系、方法 / 智能体使用、评价与复现资产 | [paper_story.md](../story/paper_story.md) 与 [protocol.md](../story/protocol.md) 能说明研究者拥有综述元模型 |
| L1 脚手架 / 种子探测 | 从既有 LLM4SE / MDE 综述与少量状态机生成种子论文提取候选字段 | [protocol.md](../story/protocol.md) 明确综述之综述只是脚手架 |
| L2 维度模式 | 字段树可含输入材料类型、输出状态机类型、状态 / 迁移 / 守卫 / 动作 / 时钟、大语言模型 / 智能体类型、评价指标、制品可用性 | [terminology_policy.md](../story/terminology_policy.md) 定义维度模式与模式演化 |
| L4 字段证据 | 每篇论文字段必须带页码、章节、短引文、表格、制品链接或缺失 / 不确定说明 | [protocol.md](../story/protocol.md) §2/§4 能指导内容证据 |
| L5 统计分析 | 统计不同状态机输出谱系、智能体使用程度、公开制品比例、评价方式分布 | [protocol.md](../story/protocol.md) §5 禁止统计结果直接升级为发现 |
| L6 候选发现 | 例如“多数 LLM4STM 论文缺少 机器可检查评价（machine-checkable evaluation）”只能作为候选发现 | [claim_evidence_map.md](../story/claim_evidence_map.md) 明确候选 / 最终边界 |
| L7 裁决 | 研究者检查反例、范围、强度；可能降级为“在当前样本中观察到制品 / 评价透明度不足” | [paper_outline.md](../story/paper_outline.md) 与风险登记能指导质疑 / 裁决 |
| 过程证据 | 记录模式修订、回填、质疑和人工时间，用于方法评价 | [evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md) 已把过程指标分离 |

试读检查结论：当前文档已经能把 LLM4STM 主题从“普通综述自动化”导向维度模式、字段证据、统计观察、候选发现与研究者裁决的闭环；后续试运行 / 评价仍需真实试运行和运行记录才能写结果。

## 6. 验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-26 | 合入 `origin/paper2/agent-based-slr-umbrella` | 通过；merge commit `47ce6cc3`，无冲突 |
| 2026-06-26 | 三路 PR 正文 计划阶段审查 | 0C/0I，可进入实现；M 级建议已吸收进 S0-v2 文档方向 |
| 2026-06-26 | 内部子代理只读检查 | 发现 C/I：多份下游文档仍旧 S0、L8/G6 不一致、方法图缺 G6；本轮已修复 |
| 2026-06-26 | 基于大语言模型的状态机建模主题试读检查口径检查 | 通过；文档能指导维度模式 → 字段证据 → 统计分析 → 候选发现 → 裁决 |
| 2026-06-26 | `git diff --check` | 通过 |
| 2026-06-26 | PR-S0-v2 必需文件存在性检查 | 通过；`paper_agent_based_slr PR-S0-v2 packet ok` |
| 2026-06-26 | 禁止强主张 grep | 通过；命中均位于禁止 / 风险 / 安全边界 / grep 规则语境中，不是正向主张 |
| 2026-06-26 | Markdown 相对链接检查 | 通过；`markdown relative links ok` |
| 2026-06-26 | Mermaid 渲染检查：`mmdc -p /tmp/puppeteer-no-sandbox-pr114.json -i /tmp/pr114_s0v2_method.mmd -o /tmp/pr114_s0v2_method.svg` | 通过；SVG 已生成，本地大小 44619 bytes |
| 2026-06-26 | 首轮正式复审修复验证：`git diff --check`、必需文件检查、Markdown 相对链接检查、Mermaid 渲染、旧 story grep | 通过；`baselines/SUMMARY.md` 旧 S0 正向 story 口径已同步为 S0-v2，grep 无旧正向叙事命中 |
| 2026-06-26 | 状态同步提交复核 | 通过；`ed55b912` / `397b6d05` 均仅修改 `plan/progress.md` 当前阶段或复审目标说明，不改变 S0-v2 方法合同；当前复审对象以 PR 当前提交为准 |
| 2026-06-27 | 术语中文化与双图补强 | 通过；修复 `paper_outline.md` / `differential_novelty_matrix.md` 中英混杂与坏链接，补强术语首次出现规则，普通流程图与时序图均已渲染；普通流程图 SVG 已渲染为 1260×780、比例 1.615，时序图白底渲染为 784×1037、比例 0.756；普通流程图已在图内补充 L0--L7 映射、颜色图例和 G6“仅审计记录 / 不作为领域发现证据”边界 |
| 2026-06-27 | 内部子代理术语审查 | 首轮发现 0C/3I/2M，主要为大纲中英混杂、坏链接和新颖性矩阵误替换；已修复后重新检查 |
| 2026-06-27 | 普通流程图视觉盲读 | 视觉检查发现 Mermaid 普通流程图会被自动布局成倒序、过扁或过高；已改为可控 SVG 普通流程图。多轮盲读指出 G6 与 G4 反馈歧义；当前 SVG 已调整为三阶段主流程居中、G2/G4 左侧反馈、回 L2 / 回 L4 标签、颜色图例和“G6 仅审计记录 / 不作为领域发现证据”说明；最终内部只读复核已闭合 |
| 2026-06-27 | Markdown 相对链接检查 | 通过；`markdown relative links ok`，此前因中文化误替换产生的若干错误文件链接均已恢复 |
| 2026-06-27 | 最终内部复核：术语 / SVG / 链接 / 渲染 | 通过；视觉盲读确认普通流程图 0C/0I，仅余不阻塞的 M 级视觉微调；只读 verifier 确认 SVG 已可被 git 跟踪、`baselines/GUIDE.md` 不再越界、任务包已改为 SVG + Mermaid 分离验收、`git diff --check` / Markdown 相对链接 / Mermaid 渲染 / SVG 渲染均通过；随后复核“术语首次中文锚点、后续中文主称、普通流程图 + 时序图双图并存”要求，未发现新的 C/I 缺口 |

## 7. 审查状态

| 阶段 | 审查者 | 结果 | 处理 |
|---|---|---|---|
| PR 正文 计划阶段 | deepseek 审查者 | 0C / 0I / 3M | 可进入实现；M 已吸收为术语和风险补强 |
| PR 正文 计划阶段 | codex 审查者 | 0C / 0I | 可进入实现 |
| PR 正文 计划阶段 | claude 审查者 | 0C / 0I / 少量 M | 可进入实现 |
| 内部实现中只读检查 | verifier 子代理 | C/I：多数落点旧 S0、L8/G6 不一致、方法图缺 G6；PR 正文 / 进度状态与验证记录曾不同步 | 已重写 主张-证据映射 / 大纲 / 评价 / 风险 / README / 任务包 / 进度，并修正 L8/G6；验证记录与 PR 正文已同步，当前复审对象以 PR 当前提交为准 |
| 内部实现中学术审查 | critic 子代理 | C/I：大纲、主张-证据映射、评价、风险、新颖性矩阵、项目证据清单未同步 S0-v2；旧证据包叙事残留 | 已逐项修复，并把旧叙事 grep 标为人工审查线索而非硬 gate |
| 正式三路复审 | codex / claude / deepseek 审查者 | 最新轮已进入当前 HEAD 复审：deepseek 0C/0I；codex 指出 progress 推送前口径 I；claude 等待当前轮评论 | 本提交修复 codex 指出的 progress stale 口径；修复后需针对 PR 当前 HEAD 复验 |

## 8. 剩余风险

1. 当前 PR-S0-v2 仍是主线和合同冻结，不提供真实运行证据；后续不得把候选贡献写成结果。
2. SVG 普通流程图与 Mermaid 时序 / 泳道图是方法总览草案；若后续设计、试运行、真实运行或评价改变阶段契约、维度模式或证据字段，必须同步更新。
3. 脚手架仍是计划证据；后续若执行，必须避免写成目标证据池或完整三级综述。
4. 学生过程数据仍是计划；评价前必须冻结同意、匿名化、脱敏、教学关系隔离和访问权限。
5. 相关工作仍需 A6 深化，尤其是 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻；`baselines/SUMMARY.md` 已完成 S0-v2 方向性同步，但正式论文写作前仍需逐篇 PDF / 制品审计。


## 9. 本轮补充：SVG 源稿说明与 story 再审查

- 已新增 [../story/figures/README.md](../story/figures/README.md)，明确普通方法流程图 [../story/figures/s0_method_flow.svg](../story/figures/s0_method_flow.svg) 是手写 / 直接维护的可控 SVG，文件本身就是当前源稿，不是 Mermaid 生成。
- 已在 [../story/README.md](../story/README.md) 增加图源维护说明入口。
- 已按 `ai-research-writing-skill` / `research-planning` / `literature-search` / `autoresearch` 口径完成本轮 story 薄弱点复核；当前不运行真实大语言模型 API，不触发 `.env`。
- OMX spawn 三路只读审查结论一致：当前 S0-v2 方向正确，但 story 仍偏“强协议 / 弱证据”，正面贡献需要从流程门控收敛为“审计优先证据工程”或等价的可验证技术对象，并用完整闭环 pilot、可执行评价协议、可导出审计制品链和 risk-to-metric 结果闭合；本轮已将该要求落入 story、protocol、outline、claim map、评价维度、风险登记和任务包。
- 轻量文献检索已覆盖 arXiv / OpenAlex 四组查询共 160 条结果，用于确认近邻压力；新检索主要强化既有结论：自动综述、agentic SLR、HITL provenance、SE LLM-SLR screening / replication 风险均已有近邻，后续不能回到宽泛自动化或 firstness 叙事。

- 已完成当前 PR 内文档迭代：将工作标题 / 一句话论点收敛为“审计优先证据工程方法”，新增审计制品链、最小闭环样例、risk-to-metric 评价矩阵、强协议 / 弱证据风险，以及图源维护说明；这些内容现在属于当前 PR-S0-v2 合同，而不是留给外部口头建议。

### Capability-use audit

- Required references/scripts: `ai-research-writing-skill/references/paper-story.md`，`research-planning/references/planning-prompts.md`，`research-planning/references/output-schemas.md`，`literature-search` / `systematic-review` 检索脚本，`autoresearch` artifact-gated 审查口径。
- Inputs consumed: [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)、[../story/paper_outline.md](../story/paper_outline.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)、[../baselines/SUMMARY.md](../baselines/SUMMARY.md)。
- Artifacts produced: [../story/figures/README.md](../story/figures/README.md)、更新后的 [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)、[../story/paper_outline.md](../story/paper_outline.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/terminology_policy.md](../story/terminology_policy.md)、[../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)、[../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)、[./task-packets/s0-story-recalibration.md](./task-packets/s0-story-recalibration.md) 与本进度记录；外部检索临时结果保存在 `/tmp/s0_story_litsearch/`，不作为仓库事实源。
- Verification run: `git diff --check`、修改文件 Markdown 链接检查、`rsvg-convert` SVG 渲染检查。
- Remaining risk: 本轮已修改 paper story 主线并补强当前合同；但仍未执行真实 pilot，也未冻结 A5 指标公式、阈值、统计协议或最终数据结构。
