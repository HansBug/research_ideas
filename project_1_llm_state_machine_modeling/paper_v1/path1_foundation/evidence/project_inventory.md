# Path-1 Project Inventory

## 1. Repository map

| 路径 | 作用 | 当前状态 | 与论文的关系 |
|---|---|---|---|
| [../../../method/](../../../method/) | agent-loop / LangGraph runtime / stage API / run record / skill 工具箱 | 已完成 LG-M1 集成与最终四例 retained evidence | 方法实现与可复现实验入口 |
| [../../../eval/](../../../eval/) | component extraction、evaluation protocol、review package | 已有 Path-1 5-component manual eval 协议 | 评测与 human adjudication 基础 |
| [../../../baselines/](../../../baselines/) | LLM-for-modeling / STM generation / requirements-to-model baseline 文库 | 72 篇已完成全文分析 | related work 与 baseline matrix 来源 |
| [../../../sources/](../../../sources/) | 控制系统 source / STM 文库 | 真实控制系统样本池 | Path-1 / Path-2 样本来源之一 |
| [../../../talks/](../../../talks/) | project_1 内部导师讨论文库 | 已记录 2026-06-04 第一篇路线定调 | 学术决策来源 |
| [../](../) | `paper_v1` 历史工作区 | 旧 README 有 sprint 口径，本 PR 增加 current overlay | 第一篇论文工作区 |
| [../](../) | 当前 foundation | 本 PR 新增 | 后续第一篇 paper 主工作入口 |
| [../../../../runs/](../../../../runs/) | 真实运行记录 | 已按仓库 run record 规范维护 | 主实验与代表性 run evidence 保存位置 |

## 2. Method evidence

当前方法底座的推荐事实入口：

- [../../../method/README.md](../../../method/README.md)：当前功能入口地图、LLM env、runtime 语义、测试入口。
- [../../../method/ARCHITECTURE.md](../../../method/ARCHITECTURE.md)：LangGraph runtime、stage API、模块边界。
- [../../../method/STATUS.md](../../../method/STATUS.md)：LG-M1 子 PR 总账、final four-case evidence 与历史 provenance。
- [../../../method/agent_loop_skill/AGENT_LOOP_SKILL.md](../../../method/agent_loop_skill/AGENT_LOOP_SKILL.md)：成熟 agent skill route 的当前入口。

方法证据必须谨慎表述：

1. `method.loop.run_agent_loop(...)` 是 canonical full staged runtime。
2. 当前 full staged runtime 已切到 LangGraph 体系，但论文不应把 LangGraph 当核心贡献。
3. E1 自建 loop 与 E2 skill route 是 agent orchestration conditions，不是 Hybrid 方法。
4. run record 是 evidence chain；真实 provider run 必须记录 model/provider/prompt/raw output/usage/retry/redaction。

## 3. Experiment evidence currently available

| 证据 | 来源 | 可支持什么 | 不能支持什么 |
|---|---|---|---|
| LG-M1 final four-case evidence | [../../../method/STATUS.md](../../../method/STATUS.md) / PR #39 / PR #22 | agent-loop 已能真实运行并留 retained evidence | 不能替代 Path-1 main experiment |
| PR #9 sample selection | [sample_assets.md](../dataset_selection/sample_assets.md) | selection rationale、stress-test pool、Top/Backup 样本候选 | 不能当主结果 |
| PR #9 two early historical early reference drafts | [sample_assets.md](../dataset_selection/sample_assets.md) | reference discipline、V-rich/V-poor case insight | 不能当最终 human-signed oracle |
| Baseline corpus | [../../../baselines/SUMMARY.md](../../../baselines/SUMMARY.md) | close prior work matrix、direct / near / evidence-only 分类 | 不能直接给实验数字 |
| eval protocol | [../../../eval/PROTOCOL.md](../../../eval/PROTOCOL.md) | 5-component TP/FP/FN、人类签字、LLM 初审辅助协议 | 不能免除正式 annotator / blind / agreement |

## 4. Writing assets

| 资产 | 路径 | 用途 |
|---|---|---|
| Paper story | [paper_story.md](../story/paper_story.md) | Introduction / Method / Contribution 的 story source |
| Claim-evidence map | [claim_evidence_map.md](../story/claim_evidence_map.md) | 摘要和引言 claim 控制 |
| Baseline matrix | [baseline_and_related_work_matrix.md](./baseline_and_related_work_matrix.md) | Related Work 与 Experiments baseline section |
| Risk register | [reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) | Threats / Limitations / review gating |
| Execution plan | [execution_plan.md](../experiment_design/execution_plan.md) | 后续 PR / 实验 / 写作排期 |

## 5. Citation and related-work assets

当前 citation 工作尚未进入 manuscript 阶段；不要从记忆写 BibTeX。后续进入 Related Work 时必须：

1. 从 [../../../baselines/](../../../baselines/) 读取 `bibtex.bib` 和 `DESC.md`。
2. 对最接近论文重新核验标题、作者、年份、venue、DOI/URL。
3. 建立 manuscript-level `references.bib` 和 `citation_verification.md`。
4. 对无法公平复现的工作写明 `evidence-only` 或 `approximate reimplementation`。

## 6. Missing inputs

| 缺口 | 影响 | 进入下一阶段前动作 |
|---|---|---|
| Frozen sample registry | 影响 sample bias / cherry-pick 风险 | 冻结全量 9/101 或预注册降级样本，保留排除原因 |
| Human adjudication team | 影响 oracle credibility | 至少 2 名独立 annotator + blind coding + disagreement 仲裁 |
| External executable baselines | 影响 novelty/fairness | 至少 3 个 closest prior work 入矩阵，至少 1 个 same-sample approximate baseline |
| Main experiment runs | 影响所有 result claim | direct / structured / no-feedback / partial-feedback / full-method 全部留 run record |
| Manuscript template | 影响写作与投稿 | 根据 SoSyM / ASEJ / REJ 决定模板、页数、匿名性 |
| Submission artifact package | 影响 reproducibility | 从 raw requirement 到 generated STM / checks / repair / metrics 的最小复现命令 |
