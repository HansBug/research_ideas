# Paper1：状态机模型问题发现

本工作区研究一条通用的状态机问题发现架构：给定自然语言描述和一个在分析前已存在、带来源归属且分析期间保持固定的源状态机制品，方法发现描述、模型结构或可执行状态机语义之间的不一致，并为每条发现保留可追溯的定位和证据。架构以有限控制状态机（finite control state machine，FCSTM）为分析工作表示，通过语言适配器接收源状态机制品。原则上，能在声明的源语言子集内形成可追溯 FCSTM 投影的状态机建模语言，都可实现为该架构的方法实例；每个适配器还须提供 source attribution、规则相关 capability contract、失败关闭边界和独立评测。当前实现和论文案例研究只含 PlantUML 适配器，因而只报告该适配器的结果。当前 54 个 PlantUML 制品来自 Wang 等上游 LLM generation/feedback pipeline 按冻结 stage/fallback 规则选择的输出；“已存在”不表示必须由人类创作。它面向需要复核状态机制品的研究者与维护者，不是状态机生成或自动修复工具。

当前论文采用历史 Luna 与 E2 三模型的同模型整体比较，并以 A1、A3、A4 分别分析检查事实、中间引导和执行反馈。五项 RQ、结果使用范围和精确机器来源统一从 [story/README.md](./story/README.md) 与 [outline_sources.md](./story/outline_sources.md) 进入。各条件共享 54 个输入对、三轮重复和 145 条参考问题；435 是问题与轮次单位数。v60 与更早结果保留为历史考据，不混入当前结果。

## 研究对象与输入

方法的输入闭包包含自然语言（NL）、源状态机制品、规范化源中间表示、FCSTM、原生检查事实、工作约定与来源追踪。语言适配器将源制品的定位信息带入规范化表示和已声明的 FCSTM 片段；FCSTM 支撑图、仿真和有界分析，原生检查事实提供确定性事实，二者都不产生新的描述义务。工作约定和来源追踪分别记录可用映射与归因。当前案例研究中的源制品语言是 PlantUML。输入、谓词注册表、提示词或模式以及运行约定均由清单和哈希固定。

本研究的状态机片段不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序。当前结果也不外推到其他执行模型、其他 ledger 或未声明的 FCSTM/soundness fragment。

## 当前方法与评测

现行实现依次准备输入闭包、提取 NL 约定、在固定条件下进行一次有界补全、用两个互补视角提出并定位候选，再进行确定性筛选、谓词路由、类型化输入绑定和后端执行。方法为候选保留来源追踪、绑定、回执和 W 级证据；事实、义务与 D/A 由评测仪器另行裁定（人工裁定协议定义，校准语义 judge 执行）。独立评测的定义来自冻结 issue #195 协议，执行者是固定 Luna 评价器；离线程序核对字段并派生 K/N/I。用户于 2026-09-05 确认历史 v61 方法侧 903 条报告已人工复核；这不覆盖全部基线或新增实验。A4 另按原 true 指定 I、内容等价复用和残余新判核算。本段描述的是内部评价装置与人工确认范围，属仓库内部事实；论文对外口径按 [story/README.md](./story/README.md) 的铁律写为博士生人工评阅（两位独立判读、第三位仲裁），⛔ 不得把本段或各实验报告中的评价装置描述抄入论文，机械门为 [check_paper_wording.py](./story/check_paper_wording.py)。

当前方法按工作流证据需求选择四类共 12 种可执行谓词：结构 S1–S5、拓扑 G1–G3、轨迹 R1–R3、有界验证 V1，族规模为 `5/3/3/1`。逐条用途、来源与执行边界见[谓词来源审计](./related_work/provenance/predicate_provenance.md)。谓词用于结构化绑定与执行适用检查；没有适用谓词但已有精确来源定位的发现仍可为 W1，不能具体定位的主张为 W0。D2/D1 报告会发布，D0 不发布；L 是台账分类字段，方法不输出 L。方法不读取台账、评测裁定或历史报告。

这里的“发布”只指方法的 finding publication surface；独立评测和归档仍保留全部 report、validity、relation 与 D/A decision，供复核和复算使用。

[内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 保存 evaluation-only 的后端能力、输入和 receipt 审计。它用于复核证据闭合，不属于 paper1 主叙事，不进入 method registry、prompt、routing 或 package data，也不改写 hit、W、K/N/I。旧 registry 的 planned mapping 与旧 126 条 provenance 都不是当前主结果。

各实验精确结果保留在各自归档；论文主表是 [来源索引](./story/outline_sources.md) 指向这些归档的展示视图。X1v2 没有同构的谓词或 receipt schema，predicate usage 不适用；W 轴仍适用，评测不能倒灌为 baseline method 的 W2。

## 阅读与复现

1. [论文来源索引](./story/outline_sources.md) 汇总整体比较与三项消融的结果、分母、限制和复算入口；[v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 保留历史 Luna 结果；[v60 归档](./final_results/v60_current_vs_x1v2_baseline/README.md)只作仪器校准参照。
2. [method/](./method/)、[judge/](./judge/) 与 [evaluation/](./evaluation/) 分别说明运行时方法、语义 judge（含人工裁定协议与校准）和离线评测的边界。
3. [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/README.md) 是当前 145 条台账与其 provenance；它不是 current headline 的第二份结果表。
4. [内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 是后端能力、receipt、review 和离线成分分析入口，不是 paper1 的主结果入口。
5. [story/](./story/README.md) 给出论文叙事、claim 与术语；[archive/experiment_history/](./archive/experiment_history/README.md) 给出重要历史代次的可比性边界。
6. [scripts/](./scripts/README.md) 列出所有薄命令行入口；[pipeline/](./pipeline/README.md) 仅保留输入准备和基础设施导航。
7. [E2 三模型双臂事前登记](./discover_matrix/docs/generations/e2_20260907/preregistered.md) 定义972个新增格、历史Luna只读引用、固定Luna裁定及配对分析；执行进度见其合同PR，事前计划不作为效果结果。
8. A3 的[正式四模型报告](./reports/2026-09-10-20-39-37-a3-four-model-results.md)与[学术 talk](../talks/2026-09-10-实验-A3中间引导消融与论文叙事.md)解释预期支持程度、有效发现与模型差异；[四模型完整裁定汇总](./final_results/a3_open_judge_20260910/README.md) 覆盖 648 格、2207 条发布报告，并提供同模型 Full 对比及离线复算；[Sonnet/Luna 原归档](./final_results/a3_20260910/README.md)和 [Qwen/Muse method-only 历史快照](./final_results/a3_open_method_20260910/README.md)保持不变，后者本身不含外部 judge 指标。

从仓库根可用下列 provider-free 命令复算历史 Luna 数字；其他实验命令见来源索引：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/v61/evaluate_rq3.py
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/v61/evaluate_full.py \
  --judge-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v61_source_divergence_vs_x1v2_baseline/raw/judge_v3.11_iter6cfg
```

验证 v60 校准参照归档的结构完整性：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

## 目录边界

`method/` 只产生发现和方法证据；`judge/` 只执行冻结 issue #195 判定。headline evaluation 只读取完成的制品并计算 hit、precision、W-on-hits、K/N/I、predicate usage 与成本；隔离的内部后端审计工具可以在 evaluation 层执行或重放预冻结 query，但不参与 discovery-time method predicate execution，也不进入 method 或人工裁定流程。顶层 `utils/` 只提供中立运行时和制品读取能力。[archive/legacy/feedback_loop/](./archive/legacy/feedback_loop/README.md) 是保留的旧实现，不是现行方法。

当前技术发布结构、内部 release candidate 与固定 15-pair 技术回归记录在 [release_validation/](./release_validation/README.md)。它们证明重构后的包结构和复现边界，不改变本页的冻结主实验。method source 的正式对外再分发仍需权利人明确指定 LICENSE；这不改变内部技术制品的复现状态。
