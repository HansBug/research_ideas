# repair_baselines — STM 修正任务 baseline / 近邻工作文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 **repair baselines / near-miss related work** 文库，服务于 `<NL, STM_0> -> STM_k / Better STM` 主线。它只回答一个问题：已有工作在“已有模型之后的修正、补全、refinement、consistency fixing、verification / simulation / diagnostic feedback、LLM / agentic repair loop”上做到了什么。

**核心边界**：这里不是 `NL -> STM_0` generation baseline 的改名。能写成本文 baseline 的工作必须满足 `<NL, STM_0> -> STM_k / Better STM`，且 `STM_0` 明确由同一 `NL` 生成 / 派生。只提供上游 `<NL, STM_0>` 的工作应登记在 [../seed_library/](../seed_library/)；只有 `STM + error / tests / oracle / diagnostics` 的 repair 工作只能作为 near-neighbor / related work；纯控制系统自然语言来源应留给后续 `nl_datasets/`。同一篇论文如果既能提供 seed，又包含 repair / feedback 环节，应在 seed 文库记录 seed 关系，在本目录记录 repair 能力，并相互交叉链接。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界和结论速览。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、资源、全文阅读和更新规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是唯一横向事实真源，包含检索覆盖、候选分级、资源可获取性、排除证据、manual queue 和最终结论。
4. 进入单篇目录时，默认按 `bibtex.bib -> paper_content.txt -> baseline_desc.md -> artifacts.md -> paper.pdf（必要时）` 阅读。

## 2. 结论速览

当前文库的阶段性判断是：**严格同构 baseline 尚未确认；`completion-sysml-gwt` 是唯一 P0 条件 baseline 候选，其余已入库条目都不能直接写成本文 baseline**。更可靠的写法是把候选分成“P0 条件 baseline 候选、生成链内 feedback、repair-engine / partial-STM 近邻、异构形式化 repair 近邻、模型一致性/补全近邻、negative evidence”。

| 结论层级 | 当前代表 | 一句话判断 | 详情 |
|---|---|---|---|
| 严格全绿 baseline | 暂无 | 尚无条目同时闭合 `NL`、`STM_0`、`NL -> STM_0`、`STM_0 -> STM_k` 与资源可复验 | 见 [SUMMARY.md](./SUMMARY.md) §6 与 §10 |
| P0 条件 baseline 候选 | `completion-sysml-gwt` | 最接近“GWT/NL + partial SysML SMD -> completed SMD transitions”；但 `STM_0` 是否严格由同一 NL 生成仍需核验 | 见 [SUMMARY.md](./SUMMARY.md) §6 与 §10 |
| 生成链内 feedback / refinement | `designing-fsm-gpt4-repair`、`ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` | 支撑“NL->STM 后仍需反馈修正”的 story，但不能替代 `<NL, STM_0> -> STM_k` baseline | 见 [SUMMARY.md](./SUMMARY.md) §6 |
| repair-engine / partial-STM 近邻 | `flowrepair-stateflow-cps`、`execution-partial-state-machine-models` | repair/refinement 机制较强，但缺少 NL 或 `NL -> STM_0` 关系 | 见 [SUMMARY.md](./SUMMARY.md) §6 |
| 异构形式化 / 模型一致性近邻 | `pat-agent`、`event-b-agent`、UML/SysML consistency、BPMN diagnostics 等 | 对 feedback loop、diagnostics、repair taxonomy 有参考价值，但不能写成同构 STM baseline | 见 [SUMMARY.md](./SUMMARY.md) §6 与 §9 |

## 3. 核心文献 + 资源结论表

本表只给入口速览；正式资源状态、风险和证据以 [SUMMARY.md](./SUMMARY.md) 为准。资源链接只记录论文或作者提供的一手入口；本仓库本地缓存不算公开资源。

| ID | 是否真 baseline | NL->STM | 修正 | 谱系 | baseline | 资源 | 一手资源入口 | 结论 |
|---|---|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | P0 条件候选 | 🟡 | 🟢 | 🟢 | 🟡 | 🟠 | [DOI](https://doi.org/10.1007/s10270-024-01228-3) | 唯一主 baseline 候选；仍需核验 partial SMD / states 是否严格由同一 GWT/NL 生成 |
| `towards-automatic-model-completion` | 否 | 🟡 | 🟡 | 🟢 | 🟠 | 🟠 | [arXiv](https://arxiv.org/abs/2210.03388) | 同簇 precursor / 条件线索，不独立计 baseline |
| `designing-fsm-gpt4-repair` | 否 | 🟢 | 🟢 | 🟢 | 🟠 | 🟠 | [arXiv](https://arxiv.org/abs/2603.29140) | seed 与 repair 分段共存；repair 阶段主要是 `STM + oracle/trace/fault-model`，只能作近邻 |
| `ttool-ai-feedback` | 否 | 🟢 | 🟠 | 🟡 | 🟠 | 🟡 | [HAL](https://telecom-paris.hal.science/hal-04483279)、[GitHub](https://github.com/zebradile/ttool-ai) | 生成链内 feedback-regeneration，适合作 related / 消融参考 |
| `llms-emp-feedback` | 否 | 🟢 | 🟠 | 🟡 | 🟠 | 🟡 | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)、[Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | STM 子集 feedback 近邻，不能混入 ACT/SD |
| `fsm-gen-iec-61499` | 否 | 🟡 | 🟠 | 🟢 | 🟠 | 🔴 | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/) | 工业仿真/用户 refinement 近邻，非无人自动 baseline |
| `execution-partial-state-machine-models` | 否 | 🔴 | 🟡 | 🟢 | 🔴 | 🟡 | [DOI](https://doi.org/10.1109/TSE.2020.3008850)、[arXiv](https://arxiv.org/abs/2103.17194)、[Bitbucket](https://bitbucket.org/moji1/partialmodels) | partial STM execution/refinement 近邻；无 NL |
| `flowrepair-stateflow-cps` | 否 | 🔴 | 🟢 | 🟡 | 🔴 | 🟡 | [DOI](https://doi.org/10.1016/j.infsof.2025.108010)、[arXiv](https://arxiv.org/abs/2404.04688)、[GitHub](https://github.com/aitorarrietamarcos/StateflowRepairTool)、[Zenodo](https://zenodo.org/records/10936238) | 强 Stateflow repair-engine 近邻；无 NL，依赖仿真 oracle |
| `pat-agent` | 否 | 🔴 | 🟡 | 🔴 | 🔴 | 🟡 | [arXiv](http://arxiv.org/abs/2509.23675)、[GitHub](https://github.com/ZuoXinyue/PAT-Agent) | 异构形式化 repair 近邻；非 STM family |
| `event-b-agent` | 否 | 🔴 | 🟡 | 🔴 | 🔴 | 🟢 | [arXiv](http://arxiv.org/abs/2605.17475)、[GitHub](https://github.com/HongshuW/EventB_Agent)、[Zenodo](https://doi.org/10.5281/zenodo.19642103) | 异构 formal-state repair 近邻；非 STM family |

## 4. 单篇目录结构

每个单篇目录默认包含：

```text
<paper-slug>/
├── paper.pdf
├── paper_content.txt
├── bibtex.bib
├── baseline_desc.md
└── artifacts.md
```

若论文仍需人工下载或机构访问，则先进入 [manual_download_queue.bib](./manual_download_queue.bib)，并在 [SUMMARY.md](./SUMMARY.md) 中保留候选状态，不提前创建伪完整目录。

## 5. 更新纪律

- 横向事实只更新 [SUMMARY.md](./SUMMARY.md)，不得新增根层 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md` 等第二事实源。
- 新增条目必须同步更新 [SUMMARY.md](./SUMMARY.md) 的候选表、资源表、manual queue / negative evidence / 更新日志。
- PR / issue 的执行计划、review 状态、ready gate、commit / push / merge 进度只写 GitHub body/comment，不写入本目录；本目录只保留长期事实、口径和论文材料。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 18:35:00 | 按 `<NL, STM_0> -> STM_k` 且 `STM_0` 必须由同一 NL 生成 / 派生的硬定义收紧 README 结论，明确当前只有 `completion-sysml-gwt` 是 P0 条件 baseline 候选。 |
| 2026-06-15 17:40:00 | 补入 `flowrepair-stateflow-cps`，将其从人工队列升级为 Stateflow repair-engine 近邻，并同步修正检索账与资源表。 |
| 2026-06-15 16:50:00 | 补入 `execution-partial-state-machine-models` 与候选池筛查账，修正旧 direct baseline 计数口径。 |
| 2026-06-15 16:20:00 | PR-R1.8-C 初始化 repair_baselines 文库三件套、首批全文阅读条目、检索覆盖表与人工下载队列。 |
