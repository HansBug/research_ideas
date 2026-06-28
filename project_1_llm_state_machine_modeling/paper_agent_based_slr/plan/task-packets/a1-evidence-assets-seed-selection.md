# PR-A1 任务包：证据资产盘点与最小闭环种子选择

## 1. 定位

本任务包对应伞 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的 PR-A1，当前 PR 为 [#129](https://github.com/HansBug/research_ideas/pull/129)。A1 的目标是把第二篇论文后续 A2 / A3 / A5a 能直接消费的证据资产和 3--5 篇最小闭环种子先冻结下来。

A1 不是运行阶段，也不是实现阶段。它只回答三个问题：

1. 当前仓库里哪些资产可以作为后续审计优先证据工程的输入。
2. 哪些 LLM4STM / LLM4Modeling 论文适合作为最小闭环种子。
3. 这些资产和种子会给 A2 的模式 / 契约、A3 的 mini-case、A5a 的运行前指标带来哪些风险压力。

当前上游顺序固定为：

> A1 资产与种子 → A2 schema / contract → A3 mini-case → A5a 运行前指标 → A4 真实运行 → A5b 运行后评价 → A6 写作。

## 2. 允许修改范围

| 路径 | 本 PR 允许动作 | 说明 |
|---|---|---|
| [../../evidence/a1_asset_inventory.md](../../evidence/a1_asset_inventory.md) | 新增 | A1 专用资产登记表。 |
| [../../dataset_selection/a1_seed_papers.md](../../dataset_selection/a1_seed_papers.md) | 新增 | A1 正选 / 备选 / 排除种子表。 |
| [../../evidence/project_inventory.md](../../evidence/project_inventory.md) | 更新 | 补 A1 专用入口和资产层级。 |
| [../../evidence/fact_drift_policy.md](../../evidence/fact_drift_policy.md) | 小修 | 将 PR #97 快照示例统一为完整 SHA。 |
| [../../dataset_selection/README.md](../../dataset_selection/README.md) 与 [../../dataset_selection/sample_assets.md](../../dataset_selection/sample_assets.md) | 更新 | 挂接 A1 种子入口。 |
| [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | 小幅更新 | 只补 A1 暴露出的风险触发点，不冻结公式。 |
| [../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) | 更新 | 追加 A1 相关审稿风险。 |
| [../README.md](../README.md) 与 [../progress.md](../progress.md) | 更新 | 记录 A1 任务包和当前进展。 |
| [../../README.md](../../README.md) | 小幅更新 | 在阅读顺序和目录导航中加入 A1 入口。 |

## 3. 本 PR 不做

1. 不实现智能体工作流、脚本、数据结构或运行时代码。
2. 不运行真实大语言模型，不读取 `.env`，不产出真实运行记录。
3. 不跑四个真实例子；真实场景与 mini-case 留给 A3，真实运行留给 A4。
4. 不构造金事实 / 银事实，不冻结最终维度模式、指标公式、阈值或统计协议。
5. 不把 PR [#97](https://github.com/HansBug/research_ideas/pull/97) 的未合入资产写成 `main` 事实。
6. 不把 A1 种子写成最终 benchmark，也不写结果型论文主张。

## 4. 输入证据

| 输入 | 当前状态 | A1 使用方式 |
|---|---|---|
| [../../README.md](../../README.md) | PR-S0-v2 工作区入口 | 确认论文主线、非目标和禁止主张。 |
| [../../story/paper_story.md](../../story/paper_story.md) | 当前 story 真源 | 确认 A1 种子必须服务“审计优先证据工程”，而非宽泛自动化综述。 |
| [../../evidence/fact_drift_policy.md](../../evidence/fact_drift_policy.md) | 事实漂移政策 | 约束 PR #97、`sources/` 数字和快照事实写法。 |
| [../../evidence/project_inventory.md](../../evidence/project_inventory.md) | 项目证据总账 | 登记 A1 新入口，不复制未合入资产。 |
| [../../../baselines/SUMMARY.md](../../../baselines/SUMMARY.md) | Project 1 baseline 总账 | A1 LLM4STM / LLM4Modeling 种子池主入口。 |
| [../../../sources/SUMMARY.md](../../../sources/SUMMARY.md) | Project 1 sources 总账 | 只作为后续场景线索和 `main` 数字复核入口。 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | OPEN / 未合入 / 快照事实 | 只作为 T1 线索，不作为当前已合入事实。 |
| PR [#105](https://github.com/HansBug/research_ideas/pull/105) | B0 基线已合入伞 PR | 提醒 A1 不回到“首次 / 完整自动化 SLR”旧叙事。 |
| PR [#112](https://github.com/HansBug/research_ideas/pull/112) 与 PR [#123](https://github.com/HansBug/research_ideas/pull/123) | 导师讨论已合入伞 PR | 约束研究者定义综述元模型、维度模式演化、统计分析 / 研究发现分层、人在回路。 |

## 5. 证据层级

A1 统一使用以下层级：

| 层级 | 含义 | A1 写法 |
|---|---|---|
| T0 | 当前伞 PR / 本分支已有可复查仓库事实 | 写相对路径、核验时间、可用边界。 |
| T1 | 未合入 PR 快照事实，例如 PR #97 | 写 PR 编号、状态、完整 SHA、漂移触发条件。 |
| T2 | 历史 issue / PR comment 线索 | 只能作为发现线索，不能支撑当前结论。 |
| T3 | 后续计划证据 | 只能写待构造或待冻结。 |

## 6. 种子选择规则

A1 正选种子以 3--5 篇为限。本轮选择 5 篇，目标是覆盖不同证据压力，而不是凑齐最终 benchmark。

### 6.1 必选条件

| 维度 | 要求 |
|---|---|
| 主题贴合 | 必须贴近自然语言 / 文档到状态机、SysML 行为模型、UML 状态机、FSM 或状态机族建模。 |
| 可审计证据 | 本地至少应有 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`；五绿 direct baseline 应优先有 `ASSETS.md`。 |
| 维度压力 | 集合层面覆盖输入、输出、方法、工具 / 模型、数据 / 制品、评价方式和缺失值语义。 |
| 困难样本 | 至少一篇能触发模式修订、证据定位困难、缺失制品、私有数据或主张降级。 |
| 反 cherry-picking | 必须记录备选 / 排除候选及理由。 |

### 6.2 困难样本判定

下列任一项可使论文成为困难样本；正式写入 [../../dataset_selection/a1_seed_papers.md](../../dataset_selection/a1_seed_papers.md) 时必须给触发证据：

1. 输出边界复杂：同一论文涉及多种模型视图、代码、表格或行为模型。
2. 方法命名不标准：原文同时使用提示链、反馈修复、工具辅助或智能体术语，容易错误归类。
3. 证据定位困难：关键事实分散在正文、图表、附录、仓库或外部制品中。
4. 制品 / 数据缺失：论文声称或使用数据、工具、结果，但公开性、许可、可运行性或长期稳定性不足。
5. 主张强但支撑有限：论文对自动化、泛化、效率或质量有强表述，但样本、基线或 oracle 有明显限制。
6. 领域术语冲突：同一对象可能被写作 state machine、statechart、protocol FSM、behavior model 或 Umple code。

## 7. 本轮 A1 交付物

| 交付物 | 当前作用 | 下游消费者 |
|---|---|---|
| [../../evidence/a1_asset_inventory.md](../../evidence/a1_asset_inventory.md) | 资产层级、可用边界、公开性、禁用用途和漂移触发条件。 | A2 / A3 / A5a / A6 |
| [../../dataset_selection/a1_seed_papers.md](../../dataset_selection/a1_seed_papers.md) | 5 篇正选种子、备选 / 排除候选、覆盖矩阵、风险触发点和交接项。 | A2 / A3 / A5a |
| [../../evidence/project_inventory.md](../../evidence/project_inventory.md) | 把 A1 入口挂回项目总账。 | 后续所有 PR |
| [../../dataset_selection/sample_assets.md](../../dataset_selection/sample_assets.md) | 把 A1 种子作为候选场景资产入口，而非最终数据集。 | A3 |
| [../../experiment_design/evaluation_dimensions_seed.md](../../experiment_design/evaluation_dimensions_seed.md) | 把 A1 暴露出的风险转成 A5a 指标义务。 | A5a |
| [../../experiment_design/reviewer_risk_register.md](../../experiment_design/reviewer_risk_register.md) | 记录 A1 阶段的学术和证据链风险。 | reviewer / A6 |

## 8. A2 / A3 / A5a 交接清单

| 后续 PR | A1 交接内容 | 明确不替它做的事 |
|---|---|---|
| A2 | 候选字段、字段证据类型、缺失 / 不适用 / 不确定语义、模式修订触发点、制品对象需求。 | 不冻结最终 schema，不写 contract tests。 |
| A3 | 5 篇正选种子、备选 / 排除候选、困难样本、幻觉陷阱方向、mini-case 候选。 | 不构造金事实 / 银事实，不跑 L0--L7。 |
| A5a | 风险触发点、可评价字段、证据定位难点、主张降级场景。 | 不定义公式、阈值、统计协议。 |
| A6 | 强近邻、资产边界、禁用主张和相关工作差异化线索。 | 不写最终 related work 结论。 |

## 9. 验收检查

A1 完成时必须满足：

1. [../../evidence/a1_asset_inventory.md](../../evidence/a1_asset_inventory.md) 中每个资产都有 `asset_id`、层级、来源、允许 / 禁止用途、公开性、漂移触发和下游消费者。
2. [../../dataset_selection/a1_seed_papers.md](../../dataset_selection/a1_seed_papers.md) 至少 5 篇正选种子，每篇有全文状态、选择理由、困难样本标记、风险触发点、A2/A3/A5a 交接。
3. 有备选 / 排除候选表，排除理由可执行。
4. PR #97 仍按 OPEN / 未合入 / snapshot `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727` 写；若状态变化，先更新事实漂移政策。
5. 文档明确 A1 不跑真实大语言模型、不读取 `.env`、不跑四个真实例子。
6. Markdown 链接可点击，中文为主，英文只作论文题名、术语锚点、路径或固定缩写。
7. 本地验证通过，PR comment 说明无 Codecov / 单元测试覆盖变化。

## 10. 验证命令

```bash
git status --short --branch
gh pr view 101 --repo HansBug/research_ideas --json number,state,headRefOid,mergeStateStatus,url
gh pr view 97 --repo HansBug/research_ideas --json number,state,headRefName,headRefOid,baseRefName,url
python - <<'PY_CHECK'
from pathlib import Path
required = [
    Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/task-packets/a1-evidence-assets-seed-selection.md'),
    Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/evidence/a1_asset_inventory.md'),
    Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/dataset_selection/a1_seed_papers.md'),
]
for p in required:
    assert p.exists(), f'missing {p}'
    text = p.read_text(encoding='utf-8')
    for needle in ['种子', '备选', '排除', '风险触发', '困难样本', 'A2', 'A3', 'A5a']:
        assert needle in text, (p, needle)
print('A1 documentation smoke passed')
PY_CHECK
git diff --check
```

## 11. 当前实现结论

本轮 A1 选出 5 篇正选种子：

1. `Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models`
2. `System Architects Are not Alone Anymore: Automatic System Modeling with AI`
3. `Generating SysML Behavior Models via Large Language Models: an Empirical Study`
4. `Designing FSMs Specifications from Requirements with GPT 4.0`
5. `Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering`

其中第 5 篇作为“私有工业数据 / 真实控制系统需求 / 可复现性受限”的困难样本，第 1--4 篇覆盖公开制品、工具闭环、公开数据集、合成 oracle / repair 等不同压力。`FlowFSM`、`SpecGPT 3GPP`、`Umple` 和 `Pushing the Generative Envelope` 暂列备选 / 排除，不进入 A1 正选集合。
