# Paper1：状态机模型问题发现

本工作区研究一条通用的状态机问题发现架构：给定自然语言需求和作者源状态机，方法发现需求、模型结构或可执行状态机语义之间的不一致，并为每条发现保留可追溯的定位和证据。架构以有限控制状态机（finite control state machine，FCSTM）为分析工作表示，通过语言适配器接收作者源状态机。原则上，能在声明的源语言子集内形成可追溯 FCSTM 投影的状态机建模语言，都可实现为该架构的方法实例；每个适配器还须提供作者源属追踪、规则相关能力约定、失败关闭边界和独立评测。当前实现和论文案例研究只含 PlantUML 适配器，因而只报告该适配器的结果。它面向需要复核大语言模型（large language model，LLM）建模结果的研究者与维护者，不是状态机生成或自动修复工具。

当前论文结果只来自 [v60/current 与 X1v2 baseline 最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md)。当前比较覆盖同一 54 个 pair、3 个 round、145 条人工标注的参考缺陷条目和 435 个 round-level evaluation units；历史 v46、v27 等代次只在 [实验历史索引](./archive/experiment_history/README.md) 中保留考据，不能作为当前结果或方法说明。

## 研究对象与输入

方法的输入闭包包含自然语言（NL）、作者源状态机制品、规范化源中间表示、FCSTM、原生检查事实、工作约定与来源追踪。语言适配器将作者源的定位信息带入规范化表示和已声明的 FCSTM 片段；FCSTM 支撑图、仿真和有界分析，原生检查事实提供确定性事实，二者都不产生新的需求义务。工作约定和来源追踪分别记录可用映射与归因。当前案例研究中的作者源制品是 PlantUML。输入、谓词注册表、提示词或模式以及运行约定均由清单和哈希固定。

本研究的状态机片段不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序。当前结果也不外推到其他执行模型、其他 ledger 或未声明的 FCSTM/soundness fragment。

## 当前方法与评测

现行实现依次准备输入闭包、提取 NL 约定、在固定条件下进行一次有界补全、用两个互补视角提出并定位候选，再进行确定性筛选、谓词路由、类型化输入绑定和后端执行。方法为候选保留来源追踪、绑定、回执和 W 级证据；人工另行裁定事实、义务和 D/A。独立评测中，人工按 issue #195 分别裁定关系和有效性，离线程序只校验、镜像和汇总已完成的裁定，并确定性派生 K/N/I。Paper1 的 D/A、有效性、关系和成分分析以人工裁定为准。

冻结设计注册表将 19 个谓词分为结构（6 个）、拓扑（4 个）、轨迹仿真（4 个）和有界验证（5 个）四族。它的来源标识映射已经冻结，但外部书目、全文引文和逐条语义边界仍以[谓词来源审计](./related_work/provenance/predicate_provenance.md)为准。当前结果中，12 个不同谓词标识有终止回执，8 个不同谓词标识至少绑定一条报告。这是两个不同的标识使用统计，不是发现数、W2 数或命中数。谓词不是问题发现的准入门；没有适用谓词但已有精确来源定位的发现仍可为 W1，不能具体定位的主张才是 W0。D2/D1 报告会发布，D0 不发布；L 是台账分类字段，方法不输出 L。方法不读取台账、评测裁定或历史报告。

这里的“发布”只指方法的 finding publication surface；独立评测和归档仍保留全部 report、validity、relation 与 D/A decision，供复核和复算使用。

[内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 保存 evaluation-only 的后端能力、输入和 receipt 审计。它用于复核证据闭合，不属于 paper1 主叙事，不进入 method registry、prompt、routing 或 package data，也不改写 hit、W、K/N/I。旧 registry 的 planned mapping 与旧 126 条 provenance 都不是当前主结果。

当前 headline 表格只保留在[正式 v4 公平对照报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。该报告的 JSON、TSV、分母和限制由[最终归档 README](./final_results/v60_current_vs_x1v2_baseline/README.md)链接；本页不再复制第二套结果表。X1v2 没有同构的 19 谓词或 receipt schema，所以 predicate usage 不适用；W 轴仍适用，后续人工核验不会倒灌为 baseline method 的 W2。

## 阅读与复现

1. [最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md) 是结果、分母、限制和复算的唯一入口；纸面 headline 只见[中文 v4 正式报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。
2. [method/](./method/)、[judge/](./judge/) 与 [evaluation/](./evaluation/) 分别说明运行时方法、人工裁定和离线评测的边界。
3. [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/README.md) 是当前 145 条台账与其 provenance；它不是 current headline 的第二份结果表。
4. [内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 是后端能力、receipt、review 和离线成分分析入口，不是 paper1 的主结果入口。
5. [story/](./story/README.md) 给出论文叙事、claim 与术语；[archive/experiment_history/](./archive/experiment_history/README.md) 给出重要历史代次的可比性边界。
6. [scripts/](./scripts/README.md) 列出所有薄命令行入口；[pipeline/](./pipeline/README.md) 仅保留输入准备和基础设施导航。

从仓库根可用下列 provider-free 命令验证最终归档：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

## 目录边界

`method/` 只产生发现和方法证据；`judge/` 只执行冻结 issue #195 判定。headline evaluation 只读取完成的制品并计算 hit、precision、W-on-hits、K/N/I、predicate usage 与成本；隔离的内部后端审计工具可以在 evaluation 层执行或重放预冻结 query，但不参与 discovery-time method predicate execution，也不进入 method 或人工裁定流程。顶层 `utils/` 只提供中立运行时和制品读取能力。[archive/legacy/feedback_loop/](./archive/legacy/feedback_loop/README.md) 是保留的旧实现，不是现行方法。

当前技术发布结构、内部 release candidate 与固定 15-pair 技术回归记录在 [release_validation/](./release_validation/README.md)。它们证明重构后的包结构和复现边界，不改变本页的冻结主实验。method source 的正式对外再分发仍需权利人明确指定 LICENSE；这不改变内部技术制品的复现状态。
