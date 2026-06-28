# PR-S0-v2 任务包：论文主线重新勘定

## 1. 目标

本 PR 是第二篇论文伞 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的阻塞性 PR-S0-v2。目标是把论文主线从旧的“自动化综述 / 证据制品工作流 / 候选发现工作流”重新勘定为：**面向软件工程系统综述 / 系统映射研究的审计优先证据工程方法：研究者引导的维度模式演化与发现裁决**。

本 PR 只冻结论文主线、术语、主张边界、新颖性差异、评价义务和后续 PR 门槛；不实现运行时、不跑真实大语言模型、不跑四个真实例子、不冻结最终指标公式。

本 PR-S0-v2 后续文档必须遵守术语写作规则：同一文档中，关键术语首次出现采用“中文术语（英文术语 / 缩写）”格式；首次定义后，除论文名、工具名、路径、命令、阶段编号和必要缩写外，一律优先使用中文术语，避免大段英文堆叠。核心术语表由 [../../story/terminology_policy.md](../../story/terminology_policy.md) 维护。

## 2. 背景事实

| 事实 | 对 PR-S0-v2 的影响 |
|---|---|
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) 已完成 35 篇全文文本级基线，并发现 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻 | 不能写首次、完全自动、完整生命周期或 PRISMA 透明报告框架（Preferred Reporting Items for Systematic Reviews and Meta-Analyses, PRISMA）合规系统综述。 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) 导师讨论确认 综述元模型由使用者研究者定义，智能体只提出候选发现，最终发现需证据链和研究者审计 | 不能写 大语言模型自动定义综述元模型或最终发现。 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) 导师讨论把真实系统综述压实为“收集论文 → 维度模式驱动的论文分析 → 统计分析与研究发现形成” | 必须把 维度模式生命周期、字段级内容证据、统计分析 / 研究发现分层、人工门控写进主线。 |
| 导师建议 综述之综述可放宽范围，用于提取维度模式，是低复杂度工作 | 综述之综述只作为脚手架 / 模式先验，不是目标证据池或三级综述。 |
| 导师建议先设定主题试运行，再让硕士生使用方法并收集人机交互过程数据 | 试运行只验证闭环可行性；学生数据只支撑方法发现，需伦理、匿名化、脱敏和教学关系隔离边界。 |
| PR #97 仍 未合入 | 只能作为 快照 / 分支局部证据，不能写成 `main` fact。 |

| 2026-06-28 story 再审查发现当前主线仍偏“强协议 / 弱证据”，需要更硬的论文级技术对象 | 本 PR 必须把正面贡献压缩为可导出审计制品链，并把最小闭环样例、risk-to-metric 评价矩阵列为后续阻塞性义务。 |

## 3. 允许修改范围

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/project_inventory.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/fact_drift_policy.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/SUMMARY.md`（仅允许为消除旧 S0 story 正向残留做窄口径同步，不新增论文、不重打 baseline 分数、不改单篇 `review.md`）
- PR #101 / PR #114 正文与评论

## 4. 不在本 PR 中修改

| 路径或资产 | 原因 |
|---|---|
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/**` | PR-B0 已建立 基线文库；本 PR 默认只消费结论。例外：若正式审查 发现 `baselines/SUMMARY.md` 中仍有旧 S0 正向主线口径，可仅同步 SUMMARY 的总账定调和更新日志，不新增论文、不改单篇 review。 |
| `project_1_llm_state_machine_modeling/paper_agent_based_slr/dataset_selection/**` | 本轮 S0-v2 不新增或冻结场景；历史 PR-S0 已做入口口径同步，后续 A3 才能深化场景。 |
| `project_1_llm_state_machine_modeling/method/**` | 本 PR 不实现工作流代码。 |
| `runs/**` | 本 PR 不跑真实大语言模型，不新增运行记录。 |
| `.env` | 本 PR 不触发 提供商调用，也不修改密钥配置。 |
| PR #97 分支资产 | 仍按 OPEN / 快照 / 分支局部证据处理，不复制未合入资产。 |

## 5. 必须回答的问题

| 问题 | 文件落点 | 验收方式 |
|---|---|---|
| 新的一句话论文主线是什么？ | [../../story/paper_story.md](../../story/paper_story.md) | 必须体现审计优先证据工程主线，并把研究者引导、模式演化、内容证据、统计分析、候选发现、最终裁决和过程证据串成同一条证据链。 |
| 三阶段系统综述 如何转成 L0--L7 方法合同？ | [../../story/paper_story.md](../../story/paper_story.md)、[../../story/protocol.md](../../story/protocol.md) | 必须包含论文收集、维度模式、字段证据、统计分析、候选发现、质疑 / 裁决。 |
| 维度模式生命周期 如何表达？ | [../../story/protocol.md](../../story/protocol.md)、[../../story/terminology_policy.md](../../story/terminology_policy.md) | 必须有 模式版本、变更触发、影响分析、回填状态。 |
| 统计分析与研究发现 如何拆分？ | [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md)、[../../story/paper_outline.md](../../story/paper_outline.md) | 禁止频次 / 分布 / 交叉表直接升级 最终发现。 |
| 内容证据与过程证据 如何分工？ | [../../story/terminology_policy.md](../../story/terminology_policy.md)、[../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | 领域发现只能由内容证据支撑；方法发现才使用过程证据。 |
| 综述之综述如何定位？ | [../../story/protocol.md](../../story/protocol.md)、[../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) | 它是 脚手架 / 模式先验，不是目标证据池，不是 PRISMA 三级综述。 |
| 试运行与硕士生过程数据如何写？ | [../../story/paper_outline.md](../../story/paper_outline.md)、[../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) | 试运行只验证可行性；学生数据只评价方法，需同意、匿名化和脱敏。 |
| 文档是否足够干净、自包含？ | [../progress.md](../progress.md)、本任务包、各入口 README | 删除纯历史流水账；必要历史只保留为证据链接和当前事实来源。 |
| 方法图是否足够完整？ | [../../story/paper_story.md](../../story/paper_story.md) | 除时序 / 泳道图外，必须有普通流程图说明阶段、参与者、制品、反馈关系和过程证据横切边界；图的长宽比需适中，不能为了压缩而牺牲可读性；普通流程图必须能从渲染图本身读出阶段、参与者、制品、反馈和 G6 横切边界。 |

| 审计优先证据工程对象是什么？ | [../../story/paper_story.md](../../story/paper_story.md)、[../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) | 必须列出维度模式与修订 / 回填日志、字段级内容证据表、统计分析表（字段版本、纳入样本、统计方法、限制）、候选发现台账、质疑 / 裁决日志、过程证据包，并绑定评价入口。 |
| 最小闭环样例如何要求？ | [../../story/paper_story.md](../../story/paper_story.md)、[../../story/paper_outline.md](../../story/paper_outline.md) | 必须要求 LLM4STM / LLM4Modeling 3--5 篇种子论文 dry-run，展示模式修订、回填、统计观察、候选发现、裁决与证据分离。 |
| risk-to-metric 评价矩阵如何落地？ | [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md)、[../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) | 必须把近邻威胁和审稿风险转成可评价指标，而不是只写效率或生成质量。 |

| 最小闭环样例如何防止 cherry-pick？ | [../../story/paper_story.md](../../story/paper_story.md)、[../../story/paper_outline.md](../../story/paper_outline.md) | 种子论文应覆盖至少 2 类方法或输出形态；至少包含一个预设风险触发点；必须定义 pass/fail gate：若无字段证据表、模式修订 / 回填日志、统计分析表、候选发现台账、质疑 / 裁决日志和过程证据记录则 fail；若无反向证据或无降级 / 拒绝 / 未解决案例，不得声称质疑闭环有效。 |
| 核心指标的最小定义是什么？ | [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | S0 只冻结方向，但必须给 A5 指定至少三个优先公式候选：来源锚点准确性、无支撑 / 过强候选发现率、回填完成率。 |

## 6. 拒收检查

- 不能把第二篇写回 `sources` 语料 / 基准来源论文。
- 不能写智能体完全替代系统综述专家。
- 不能写首次、完整自动化、PRISMA 透明报告框架合规、完整覆盖等被 基线调研击穿的强主张。
- 不能把统计分析直接写成 最终研究发现。
- 不能把 大语言模型 / 智能体候选发现 写成 最终发现。
- 不能把 过程证据或学生日志用于领域发现。
- 不能把 综述之综述写成目标证据池、完整三级综述或 PRISMA 透明报告框架合规三级综述。
- 不能把 试运行 / 学生过程数据 写成泛化证明或已完成结果。
- 不能让 人在回路退化为末端签字。
- 不能把 维度模式写成一次性平铺字段表而无修订 / 回填。
- 不能把 PR #97 未合入资产写成 `main` 事实。
- 不能运行真实大语言模型；后续真实运行必须 `source .env` 并保存运行记录。
- 不能让核心 Markdown 出现成片英文叙事；术语首次定义后应回到中文主称。
- 不能只有时序 / 泳道图而缺少普通流程图；普通流程图必须让读者一眼看出阶段、参与者、制品和反馈路径。

- 不能让本 PR 停留在“流程门控清单”：必须把审计对象、最小闭环样例和 risk-to-metric 后续义务写入当前合同。

## 7. 验证命令

```bash
git status --short --branch
git diff --check
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr')
required = [
    root / 'README.md',
    root / 'story' / 'README.md',
    root / 'story' / 'paper_story.md',
    root / 'story' / 'protocol.md',
    root / 'story' / 'terminology_policy.md',
    root / 'story' / 'claim_evidence_map.md',
    root / 'story' / 'differential_novelty_matrix.md',
    root / 'story' / 'paper_outline.md',
    root / 'experiment_design' / 'evaluation_dimensions_seed.md',
    root / 'experiment_design' / 'reviewer_risk_register.md',
    root / 'plan' / 'README.md',
    root / 'plan' / 'progress.md',
    root / 'plan' / 'task-packets' / 's0-story-recalibration.md',
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, missing
print('paper_agent_based_slr PR-S0-v2 packet ok')
PY
# 强主张 / 旧叙事 grep 只作为人工审查线索，不是直接 pass/fail 门控；
# 命中若位于禁止写法、风险、限制或 grep 规则本身语境，可判为通过。
rg -n -i "first automated|first agentic|complete coverage|PRISMA-compliant|LLM final|agent-generated final|process evidence supports target|student data shows|pilot proves|tertiary review|evidence package|证据包|finding-centered|研究发现为中心|report-generation|报告生成" \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/README.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/story \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/experiment_design \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/project_inventory.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/progress.md \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/task-packets/s0-story-recalibration.md
```

Mermaid 渲染验收需使用 no-sandbox 配置：

```bash
python - <<'PY'
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md')
text = p.read_text(encoding='utf-8')
start = text.index('```mermaid') + len('```mermaid')
end = text.index('```', start)
Path('/tmp/pr114_s0v2_method.mmd').write_text(text[start:end].strip() + '\n', encoding='utf-8')
PY
cat >/tmp/puppeteer-no-sandbox-pr114.json <<'JSON'
{"args":["--no-sandbox","--disable-setuid-sandbox"]}
JSON
mmdc -p /tmp/puppeteer-no-sandbox-pr114.json -i /tmp/pr114_s0v2_method.mmd -o /tmp/pr114_s0v2_method.svg
```

SVG 普通流程图验收：

```bash
test -f project_1_llm_state_machine_modeling/paper_agent_based_slr/story/figures/s0_method_flow.svg
git ls-files --error-unmatch project_1_llm_state_machine_modeling/paper_agent_based_slr/story/figures/s0_method_flow.svg
rsvg-convert -f png \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/story/figures/s0_method_flow.svg \
  -o /tmp/pr114_s0_method_flow.png
file /tmp/pr114_s0_method_flow.png
```


当前普通流程图采用可控 SVG 维护，不再按 Mermaid 渲染；验收时必须检查 SVG 文件存在、可被 `rsvg-convert` 渲染、宽高比正常、关键文字包含 L0--L7 / G0--G6 / G6 过程证据边界，并确认该 SVG 已被 git 跟踪。Mermaid 渲染只针对时序 / 泳道图。

## 8. 完成标准

- [../../story/paper_story.md](../../story/paper_story.md) 能独立解释新论文主线、三阶段系统综述、L0--L7、G0--G6、方法图、候选贡献和禁用主张。
- [../../story/protocol.md](../../story/protocol.md) 明确 维度模式生命周期、统计分析到研究发现的转移、内容证据 / 过程证据边界和人工门控契约。
- [../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) 能约束摘要、引言、贡献和结论的主张强度。
- [../../story/differential_novelty_matrix.md](../../story/differential_novelty_matrix.md) 能说明与强近邻的安全差异化。
- [../../story/paper_outline.md](../../story/paper_outline.md) 能指导后续 A2/A3/A5/A6 的方法、试运行、过程评价和写作。
- [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) 明确 模式稳定性、回填、字段证据、统计正确性、候选到最终的转移和过程指标。
- [../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) 登记统计 / 发现混淆、证据类型混用、综述之综述误定位、试运行过度外推、学生数据伦理等 C/I 风险。
- 当前 Markdown 以中文为主，必要英文仅作为术语锚点、论文 / 工具名、命令或文件路径出现。
- 术语首次出现规则在 [../../story/paper_story.md](../../story/paper_story.md) 与 [../../story/terminology_policy.md](../../story/terminology_policy.md) 中明确；正文后续使用中文主称。
- [../../story/paper_story.md](../../story/paper_story.md) 同时包含普通流程图和时序 / 泳道图，二者在阶段、参与者、制品、门控和证据边界上互相一致；普通流程图的渲染结果应长宽比正常、无大面积空白、文字可读。
- 当前 Markdown 应尽量干净、自包含：保留必要证据链接和当前合同，清除纯历史痕迹、过期状态和已修复 review 流水。

- [../../story/paper_story.md](../../story/paper_story.md) 必须把正面贡献从流程门控收敛为“审计优先证据工程”的可导出对象链，而不是只列 L0--L7。
- [../../story/paper_story.md](../../story/paper_story.md) 与 [../../story/paper_outline.md](../../story/paper_outline.md) 必须明确最小闭环样例要求，避免后续 A2/A3/A5 继续停留在抽象协议。
- [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) 必须包含 risk-to-metric 口径，说明近邻威胁和审稿风险如何转成可评价指标。
