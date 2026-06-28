# A1 证据资产登记表

核验时间：2026-06-28 19:47:37 +0800

## 1. 作用与边界

本文件是 PR-A1 的资产总账，服务于后续 A2 / A3 / A5a / A6。它只登记“哪些证据资产当前能被怎样使用”，不复制论文 PDF，不复制 PR #97 未合入文库，不跑真实大语言模型，也不生成最终实验数据。

使用本文件时必须同时阅读：

1. [fact_drift_policy.md](./fact_drift_policy.md)：确认 T0--T3 证据层级和 PR #97 写法。
2. [../dataset_selection/a1_seed_papers.md](../dataset_selection/a1_seed_papers.md)：查看 A1 5 篇正选种子与备选 / 排除候选。
3. [../plan/task-packets/a1-evidence-assets-seed-selection.md](../plan/task-packets/a1-evidence-assets-seed-selection.md)：查看 A1 范围、非目标和验收门。

## 2. 资产状态口径

状态列只放 emoji：🟢 = 当前可直接引用；🟡 = 可用但需复核或有公开性限制；🟣 = PR #97 快照 / 分支局部证据；⚪ = 计划证据或不可支撑当前结论。

证据层级沿用 [fact_drift_policy.md](./fact_drift_policy.md)：T0 是当前仓库事实，T1 是 PR #97 快照事实，T2 是历史评论线索，T3 是计划证据。

## 3. A1 核心资产表

| asset_id | 资产 | 状态 | 层级 | 来源 | 快照 / 当前性 | 允许用途 | 禁止用途 | 下游消费者 |
|---|---|---:|---|---|---|---|---|---|
| A1-ASSET-STORY | Paper2 story / protocol / claim map | 🟢 | T0 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 当前伞 PR #101 HEAD `1b1c662d67e740ade6d829ec073a84067223c9aa` 上可复查 | 约束 A1 不越界、不写强主张，给 A2/A3/A5a 提供方法边界。 | 不得把 story 中待构造义务写成已完成结果。 | A2 / A3 / A5a / A6 |
| A1-ASSET-FACT-POLICY | 事实漂移政策 | 🟢 | T0 | [fact_drift_policy.md](./fact_drift_policy.md) | 已在本 PR 同步 PR #97 完整 SHA 写法 | 约束 PR #97、`sources/` 数字、计划证据写法。 | 不得只写 `PR #97` 而不写状态和快照。 | 所有后续 PR |
| A1-ASSET-P1-BASELINES | Project 1 baseline 文库 | 🟢 | T0 | [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) | 当前收录 91 篇；五绿 direct baseline `ASSETS.md` 为 9/9 | A1 LLM4STM / LLM4Modeling 种子池主入口。 | 不得把全部 91 篇写成 Paper2 实验集或最终 benchmark。 | A1 / A2 / A3 / A6 |
| A1-ASSET-P1-SOURCES | Project 1 sources 文库 | 🟢 | T0 | [../../sources/SUMMARY.md](../../sources/SUMMARY.md) | 当前已收录 787 篇，正例案例 746 条 | 作为控制系统 STM 场景线索、后续 A3 压力测试或字段模式示例。 | 不得把 `sources/` 语料规模写成 Paper2 主要贡献。 | A3 / A5a / A6 |
| A1-ASSET-PR97 | PR #97 baseline-related screening | 🟣 | T1 | [PR #97](https://github.com/HansBug/research_ideas/pull/97) | OPEN / 未合入 / head `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727` | 只能作为 related-work / baseline 筛选线索和待复核快照。 | 不得写成 `main` 已合入事实，不得直接支撑结果主张。 | A1 / A6 |
| A1-ASSET-B0 | Paper2 B0 近邻基线文库 | 🟢 | T0 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md) | 已合入伞 PR；记录 agentic SLR / LLM-assisted SLR 强近邻 | 提供新颖性威胁和禁用主张边界。 | 不得用来替代 A1 LLM4STM 种子选择。 | A1 / A5a / A6 |
| A1-ASSET-A1-SEEDS | A1 正选种子表 | 🟢 | T0 | [../dataset_selection/a1_seed_papers.md](../dataset_selection/a1_seed_papers.md) | 本 PR 新增；5 篇正选、3 篇备选、1 篇排除 | 直接交给 A2 / A3 / A5a 设计 schema、mini-case 与指标。 | 不得写成最终 benchmark 或真实运行结果。 | A2 / A3 / A5a |
| A1-ASSET-A1-PACKET | A1 任务包 | 🟢 | T0 | [../plan/task-packets/a1-evidence-assets-seed-selection.md](../plan/task-packets/a1-evidence-assets-seed-selection.md) | 本 PR 新增 | 说明范围、非目标、交付物和验收命令。 | 不得把任务计划当作论文结果。 | reviewer / 后续 PR |
| A1-ASSET-A2-SCHEMA | 后续 schema / contract | ⚪ | T3 | 待 PR-A2 构造 | 尚不存在 | 只能作为 A1 交接对象。 | 不得在 A1 声称已冻结 schema。 | A2 |
| A1-ASSET-A3-MINICASE | 后续 mini-case / 金银事实 | ⚪ | T3 | 待 PR-A3 构造 | 尚不存在 | 只能作为 A1 交接对象。 | 不得在 A1 构造或声称已有 gold / silver facts。 | A3 |
| A1-ASSET-A5A-METRICS | 后续运行前指标公式 | ⚪ | T3 | 待 PR-A5a 构造 | 尚不存在 | 只能接收 A1 风险触发点。 | 不得在 A1 冻结公式、阈值或统计协议。 | A5a |


### 3.1 字段化资产元数据

下表按 A1 reviewer gate 明确列出最低审计字段，避免后续 A2/A3/A5a 只看到“资产名称”而误判可用性。

| `asset_id` / 资产ID | `asset_type` / 资产类型 | `evidence_tier` / 证据层级 | `source_path_or_url` / 来源 | `snapshot_state` / 快照状态 | `last_verified_at` / `verified_by` | `allowed_use` / 允许用途 | `prohibited_use` / 禁止用途 | `public_access_status` / 公开状态 | `license_or_copyright_status` / 许可 / 版权状态 | `artifact_audit_status` / 制品审计状态 | `downstream_consumers` / 下游消费者 | `eligibility_for_stats` / 统计资格 | `drift_triggers` / 漂移触发 | `selection_rationale` / `known_limitations` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-ASSET-STORY | 当前论文合同 | T0 | [../story/paper_story.md](../story/paper_story.md) 等 | #101 HEAD `1b1c662d67e740ade6d829ec073a84067223c9aa` | 2026-06-28 / 主会话 | 约束 A1/A2/A3/A5a 的主线和禁用主张 | 当作已完成实验结果 | 仓库内可读 | 仓库文档；不含第三方全文复制 | 已完成 S0-v2 多轮审查 | A2/A3/A5a/A6 | 不进入统计，只进入合同审计 | story 文件或伞 PR body 更新 | 作为方法边界真源；限制是尚未包含真实运行证据。 |
| A1-ASSET-FACT-POLICY | 事实漂移政策 | T0 | [fact_drift_policy.md](./fact_drift_policy.md) | 本 PR 已同步完整 SHA 写法 | 2026-06-28 / 主会话 | 约束快照、数字和未合入事实引用 | 替代实际资产核验 | 仓库内可读 | 仓库文档 | 已审计 PR #97 状态与 SHA | 所有后续 PR | 不进入统计，只进入事实边界审计 | PR #97 状态 / SHA / `sources` 数字变化 | 保护证据层级；限制是依赖后续 PR 主动复核。 |
| A1-ASSET-P1-BASELINES | Project 1 状态机 baseline 文库 | T0 | [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) | 当前 91 篇、五绿 `ASSETS.md` 9/9 | 2026-06-28 / 主会话 | A1 种子池、A6 related work 线索 | 直接当作 Paper2 完整实验集 | 仓库内可读；部分外部制品需单独复核 | PDF/文本来自既有文库；A1 不复制 | 已有 DESC / ASSETS 总账，但 A1 未逐篇复跑 | A1/A2/A3/A6 | 种子表可统计，不能统计为 Paper2 结果 | baseline 总账重分类或新增论文 | 主题贴合；限制是它服务 Project 1，不是 Paper2 自有 corpus。 |
| A1-ASSET-P1-SOURCES | Project 1 控制系统 sources 文库 | T0 | [../../sources/SUMMARY.md](../../sources/SUMMARY.md) | 当前 787 篇、746 条正例案例 | 2026-06-28 / 主会话 | 后续 A3 场景线索和领域压力测试 | 写成 Paper2 主贡献或完整 benchmark | 仓库内可读；单篇版权按原文处理 | 既有论文集资产；A1 不复制 | 总账可审计，A1 未新增/改动 | A3/A5a/A6 | 当前仅作背景数字，不能作为 A1 种子统计 | `sources/SUMMARY.md` 数字变化 | 贴合控制系统；限制是并非系统综述自动化 baseline。 |
| A1-ASSET-PR97 | 未合入 PR 快照 | T1 | [PR #97](https://github.com/HansBug/research_ideas/pull/97) | OPEN / `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727` | 2026-06-28 / 主会话 + `gh pr view` | related-work 筛选线索、待复核快照 | 写成 `main` fact 或已合入全文文库 | GitHub PR 可访问，资产未合流 | 未进入当前分支；不复制 | 只核验状态与 SHA | A1/A6 | 不进入当前统计 | PR merge / close / head 改变 | 保留历史筛选价值；限制是不可作为当前已合入证据。 |
| A1-ASSET-B0 | Paper2 近邻 baseline 文库 | T0 | [../baselines/SUMMARY.md](../baselines/SUMMARY.md) | 已合入伞 PR | 2026-06-28 / 主会话 | 新颖性威胁、禁用主张边界 | 替代 LLM4STM 种子选择 | 仓库内可读 | 仓库文档与已整理全文 | 已完成 B0 近邻调研 | A1/A5a/A6 | 可用于近邻数量描述，不能当作 A1 结果 | B0 文库更新 | 防止 firstness 叙事；限制是主题不完全等同 LLM4STM。 |
| A1-ASSET-A1-SEEDS | A1 种子表 | T0 | [../dataset_selection/a1_seed_papers.md](../dataset_selection/a1_seed_papers.md) | 本 PR 新增 | 2026-06-28 / 主会话 | A2/A3/A5a 的最小闭环输入 | 写成最终 benchmark 或已运行结果 | 仓库内可读 | 只链接既有 PDF/ASSETS，不复制 | 已完成 A1 级资产复核；未复跑作者代码 | A2/A3/A5a | 可统计 A1 种子覆盖，不可统计方法性能 | 种子集合或证据入口变化 | 覆盖 5 类压力；限制是选择性最小闭环，不代表全领域。 |
| A1-ASSET-A1-PACKET | A1 任务包 | T0 | [../plan/task-packets/a1-evidence-assets-seed-selection.md](../plan/task-packets/a1-evidence-assets-seed-selection.md) | 本 PR 新增 | 2026-06-28 / 主会话 | 说明 A1 范围、非目标、输入、验收和交接 | 当作已完成实验或最终 schema | 仓库内可读 | 仓库文档；不含第三方全文复制 | 已与 PR body、资产表和种子表交叉检查 | reviewer/A2/A3/A5a | 不进入实验统计，只进入合同审计 | A1 范围、上游 #101 顺序或交付物路径变化 | 保证 A1 可验收；限制是任务合同本身不提供论文内容证据。 |
| A1-ASSET-A2-SCHEMA | 后续 schema / contract | T3 | 待 PR-A2 | 尚未构造 | 2026-06-28 / 主会话 | 只作为交接目标 | 声称 A1 已冻结 schema | 不适用 | 不适用 | 未构造 | A2 | 不可统计 | A2 启动 | 当前只是计划证据。 |
| A1-ASSET-A3-MINICASE | 后续 mini-case / 金银事实 | T3 | 待 PR-A3 | 尚未构造 | 2026-06-28 / 主会话 | 只作为交接目标 | 声称 A1 已有 gold / silver facts | 不适用 | 不适用 | 未构造 | A3 | 不可统计 | A3 启动 | 当前只是计划证据。 |
| A1-ASSET-A5A-METRICS | 后续运行前指标 | T3 | 待 PR-A5a | 尚未构造 | 2026-06-28 / 主会话 | 接收风险触发点 | 声称 A1 已冻结公式 / 阈值 | 不适用 | 不适用 | 未构造 | A5a | 不可统计 | A5a 启动 | 当前只是计划证据。 |

## 4. 正选种子资产快照

正选种子全部来自 [../../baselines/](../../baselines/) 当前 T0 文库，均已具备 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md` 和 `ASSETS.md`。A1 只登记其可用性，不复制原文。

| seed_id | 论文 | 状态 | 本地路径 | 全文状态 | 制品 / 数据状态 | 允许用途 | 禁止用途 |
|---|---|---:|---|---|---|---|---|
| A1-SEED-01 | Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models | 🟢 | [../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | PDF / TXT / BibTeX / DESC / ASSETS 均存在 | 4open 匿名制品公开但长期归档和许可仍需冻结 | 公开制品强样本；用于压测状态机槽位、层次结构、参考解和结果 workbook。 | 不得声称其匿名制品长期稳定或已在本 PR 复跑。 |
| A1-SEED-02 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | 🟢 | [../../baselines/ttool-ai/](../../baselines/ttool-ai/) | PDF / TXT / BibTeX / DESC / ASSETS 均存在 | GitHub 工件公开，TTool / provider 环境需复跑前固定 | 多视图 SysML + 反馈循环强样本；用于压测工具闭环和多图一致性。 | 不得把语法 / 规则反馈写成正式模型检查结果。 |
| A1-SEED-03 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | 🟢 | [../../baselines/llms_emp/](../../baselines/llms_emp/) | PDF / TXT / BibTeX / DESC / ASSETS 均存在 | 数据集公开 + 本地 parquet 冻结；生成代码未公开 | 公开数据集与行为模型混合样本；用于压测 state machine / activity / sequence 切分。 | 不得把公开数据集等同于公开生成 pipeline。 |
| A1-SEED-04 | Designing FSMs Specifications from Requirements with GPT 4.0 | 🟡 | [../../baselines/designing-fsm-specifications-from-requirements-gpt4/](../../baselines/designing-fsm-specifications-from-requirements-gpt4/) | PDF / TXT / BibTeX / DESC / ASSETS 均存在 | GitHub 可访问但无 release / license / 依赖锁 | 合成 oracle + repair 强样本；用于压测形式化诊断、fault model、合成数据边界。 | 不得把合成数据当成真实工业需求证据。 |
| A1-SEED-05 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | 🟡 | [../../baselines/req/](../../baselines/req/) | PDF / TXT / BibTeX / DESC / ASSETS 均存在 | 论文公开；Volvo / Car Weaver 数据与代码私有 | 困难样本；用于压测私有工业数据、主张边界、缺失值语义和真实控制系统贴合度。 | 不得声称可复现训练 / 评测或可公开原始数据。 |

## 5. 公开性、版权与审计边界

| 资产类别 | 当前判断 | A1 处理 |
|---|---|---|
| 本地 PDF / TXT / BibTeX | 已在既有 baseline 文库中存在 | A1 仅链接，不复制，不新增版权风险。 |
| 公开仓库 / 4open / Google Drive / HAL / arXiv / DOI | 可作为来源入口 | 记录当前访问状态和复跑前冻结要求。 |
| 私有工业数据 | 只在论文描述中可见 | 作为“缺失 / 受限证据”困难样本，不作为可复现实验数据。 |
| PR #97 未合入文库 | T1 快照事实 | 只记录状态和完整 SHA，不合流、不复制。 |
| 后续真实运行记录 | 尚未构造 | A1 不生成；A4/A5 才能生成。 |

## 6. 漂移触发条件

若出现以下任一情况，必须更新本文件：

1. PR #97 merge、关闭或 head SHA 变化。
2. [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) 中 direct baseline 表或五绿 `ASSETS.md` 数量变化。
3. [../../sources/SUMMARY.md](../../sources/SUMMARY.md) 的 787 / 746 数字或统计口径变化。
4. 任一种子论文公开制品入口失效、许可状态变化、仓库 release / commit 变化或人工下载到新版本。
5. A2 / A3 / A5a 修改了种子消费方式、schema 字段、mini-case 策略或指标定义。

### 6.1 外部制品冻结前置步骤

A1 不冻结外部仓库、4open、Google Drive 或匿名 artifact 的本地副本；但 A3 / A4 若要把这些制品用于 mini-case、真实运行或结果统计，必须先执行以下前置步骤并在对应 run record 或任务包中留下记录：

1. 记录外部入口、访问时间、下载方式、commit / release / 文件版本和访问失败信息。
2. 将可合法保存的制品放入后续 PR 明确指定的本地证据目录；若版权或许可不允许入库，只保留脱敏元数据、hash、截图或人工核验记录。
3. 对下载文件计算 hash，并记录下载日期、操作者、来源 URL、许可状态和复现用途。
4. 若外部制品不可访问或许可不清，必须把该论文对应字段降级为“可审计但不可复跑”或“仅论文内证据”，不得把它写成可复现实验资产。

## 7. A1 交接摘要

1. A2 应从本文件读取资产层级、允许 / 禁止用途、公开性、缺失语义和漂移触发条件。
2. A3 应从 [../dataset_selection/a1_seed_papers.md](../dataset_selection/a1_seed_papers.md) 读取 5 篇正选种子、困难样本和备选 / 排除理由。
3. A5a 应把本文件中的制品缺失、锚点可得性、私有数据、匿名仓库漂移等风险映射为指标，而不是只评价摘要质量或运行时间。
4. A6 写作时只能把这些资产写成 evidence boundary / limitation / design input，不能写成已经完成的实验结果。
