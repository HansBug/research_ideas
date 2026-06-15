# repair_baselines — STM 修正任务 baseline / 近邻工作文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 **repair baselines / near-miss related work** 文库，服务于 `<NL, STM_0> -> STM_k / Better STM` 主线。它只回答一个问题：已有工作在“已有模型之后的修正、补全、refinement、consistency fixing、verification / simulation / diagnostic feedback、LLM / agentic repair loop”上做到了什么。

**核心边界**：这里不是 `NL -> STM_0` generation baseline 的改名。只提供上游 `<NL, STM_0>` 的工作应登记在 [../seed_library/](../seed_library/)；纯控制系统自然语言来源应留给后续 `nl_datasets/`。同一篇论文如果既能提供 seed，又包含 repair / feedback 环节，应在 seed 文库记录 seed 关系，在本目录记录 repair 能力，并相互交叉链接。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界和结论速览。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、资源、全文阅读和更新规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是唯一横向事实真源，包含检索覆盖、候选分级、资源可获取性、排除证据、manual queue 和最终结论。
4. 进入单篇目录时，默认按 `bibtex.bib -> paper_content.txt -> baseline_desc.md -> artifacts.md -> paper.pdf（必要时）` 阅读。

## 2. 结论速览

当前文库的阶段性判断是：**完全同构的 `<NL, STM_0> -> STM_k` 自动 repair baseline 很少**；更可靠的写法是把候选分成“直接/条件 baseline、生成链内反馈、异构形式化 repair 强近邻、模型一致性/补全近邻、negative evidence”。

| 结论层级 | 当前代表 | 一句话判断 | 详情 |
|---|---|---|---|
| 直接 / 强条件 baseline | `completion-sysml-gwt`、`designing-fsm-gpt4-repair`、`execution-partial-state-machine-models`、`flowrepair-stateflow-cps`；`towards-automatic-model-completion` 为 precursor | 最接近“已有 STM 后补全 / 修复 / 产生更好 STM”的文献证据；其中 4 项独立、1 项为同簇早期版本不重复计数 | 见 [SUMMARY.md](./SUMMARY.md) §6 与 §10 |
| 生成链内 feedback-regeneration | `ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` | 不是独立 repair-only 方法，但能说明 LLM 生成模型后用 checker / rule / user / simulation feedback 迭代改进 | 见 [SUMMARY.md](./SUMMARY.md) §6 |
| 异构形式化 repair 强近邻 | `pat-agent`、`event-b-agent`、timed automata repair 簇 | 目标工件不是本论文 STM family，但 checker / counterexample / proof feedback loop 对 story 很关键 | 见 [SUMMARY.md](./SUMMARY.md) §6 与 [manual_download_queue.bib](./manual_download_queue.bib) |
| 模型一致性 / 补全近邻 | `automatic-debugging-support-uml-designs`、`ai-driven-consistency-sysml`、`few-shot-model-completion`、`automated-bpmn-diagnostic-repair` | 支撑 model repair / completion / diagnostics-to-repair 维度，但不能写成同构 STM baseline | 见 [SUMMARY.md](./SUMMARY.md) §6 与 §9 |

## 3. 核心 baseline / 资源结论表

本表只给入口速览；正式资源状态、风险和证据以 [SUMMARY.md](./SUMMARY.md) 为准。资源链接只记录论文或作者提供的一手入口；本仓库本地缓存不算公开资源。

| ID | 当前角色 | 输入是什么 | 输出是什么 | 修正 / feedback 核心 | 一手资源入口 | 结论 |
|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | 直接/强条件 baseline | GWT/Gherkin 需求 + partial SysML model / SMD states | 补全 transitions 的 SysML SMD | 规则解析、MetaReq/MetaFragment、traceability、检查与 analyst review | [DOI](https://doi.org/10.1007/s10270-024-01228-3) | 可作为 completion baseline；非无人 repair loop |
| `towards-automatic-model-completion` | precursor | BDD/GWT 需求 + partial SysML architecture / SMD | SysML SMD transition fragments | Clause extraction + model completion 概念流程 | [arXiv](https://arxiv.org/abs/2210.03388) | 与上条交叉登记，避免重复计数 |
| `designing-fsm-gpt4-repair` | repair slice | 合成 DFSM 描述生成的初始 CSV DFSM + oracle/trace/fault-model | 修正后的 DFSM | oracle comparison、distinguishing/checking sequence、fault-model repair | [arXiv](https://arxiv.org/abs/2603.29140) | seed 与 repair 分段共存，只登记 repair slice |
| `ttool-ai-feedback` | 生成链内 feedback baseline | NL 系统规范 + SysML/TTool 约束 + 已生成上下文 | TTool/SysML SMD 等模型 | JSON / syntax / TTool constraint feedback regeneration | [HAL](https://telecom-paris.hal.science/hal-04483279)、[GitHub](https://github.com/zebradile/ttool-ai) | P1；反馈偏语法/约束 |
| `llms-emp-feedback` | STM 子集 feedback baseline | SysML 行为模型需求 + PlantUML/SysML 规则 + Error feedback | PlantUML/SysML STM 子集 | format / grammar / semantic / requirement inconsistency feedback regeneration | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)、[Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | P1；必须只取 STM 子集 |
| `fsm-gen-iec-61499` | 仿真/用户 refinement 近邻 | 控制系统 NL + I/O + 用户 refinement 请求 | FSM / IEC 61499 ECC / FB | 用户自然语言 feedback + 闭环仿真观察 | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/) | 工业近邻；非无人自动 repair |
| `execution-partial-state-machine-models` | partial STM refinement 条件 baseline | 无 NL；partial UML-RT/HSM + completeness setting | refined executable HSM / decision points / execution rules | execution-semantics static analysis + automatic refinement + input-driven execution | [DOI](https://doi.org/10.1109/TSE.2020.3008850)、[arXiv](https://arxiv.org/abs/2103.17194)、[Bitbucket](https://bitbucket.org/moji1/partialmodels) | 可作为 `STM_0 -> executable/refined STM` 条件 baseline；非 NL/LLM repair |
| `flowrepair-stateflow-cps` | Stateflow repair 强条件 baseline | 无 NL；buggy Simulink/Stateflow model + tests/oracle + SBFL suspiciousness | plausible / partial patches for Stateflow CPS controllers | SBFL/Tarantula + global/local search + simulation repair objectives + Stateflow mutation operators | [DOI](https://doi.org/10.1016/j.infsof.2025.108010)、[arXiv](https://arxiv.org/abs/2404.04688)、[GitHub](https://github.com/aitorarrietamarcos/StateflowRepairTool)、[Zenodo](https://zenodo.org/records/10936238) | 强 Stateflow/CPS repair 近邻；依赖 Simulink/Stateflow 与仿真 oracle，非 NL/LLM repair |
| `pat-agent` | 异构形式化 repair 强近邻 | NL 系统描述 + assertion / expected result | PAT/CSP# model | PAT model-checking counterexample repair loop | [arXiv](http://arxiv.org/abs/2509.23675)、[GitHub](https://github.com/ZuoXinyue/PAT-Agent) | 强方法参照；非 STM family |
| `event-b-agent` | 异构形式化 repair 强近邻 | NL requirements | Event-B machines / refinements / proofs | ProB/Rodin/SMT/proof feedback + atomic repair | [arXiv](http://arxiv.org/abs/2605.17475)、[GitHub](https://github.com/HongshuW/EventB_Agent)、[Zenodo](https://doi.org/10.5281/zenodo.19642103) | 强方法参照；非 STM family |

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
| 2026-06-15 17:40:00 | 补入 `flowrepair-stateflow-cps`，将其从人工队列升级为 Stateflow repair 强条件 baseline，并同步修正检索账与资源表。 |
| 2026-06-15 16:50:00 | 补入 `execution-partial-state-machine-models` 与候选池筛查账，修正 direct baseline 计数口径。 |
| 2026-06-15 16:20:00 | PR-R1.8-C 初始化 repair_baselines 文库三件套、首批全文阅读条目、检索覆盖表与人工下载队列。 |
