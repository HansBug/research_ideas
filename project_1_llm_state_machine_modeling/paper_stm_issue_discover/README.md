# Paper1：状态机模型问题发现

本工作区研究一条通用的状态机问题发现架构：给定自然语言描述和一个在分析前已存在、带来源归属且分析期间保持固定的源状态机制品，方法发现描述、模型结构或可执行状态机语义之间的不一致，并为每条发现保留可追溯的定位和证据。架构以有限控制状态机（finite control state machine，FCSTM）为分析工作表示，通过语言适配器接收源状态机制品。原则上，能在声明的源语言子集内形成可追溯 FCSTM 投影的状态机建模语言，都可实现为该架构的方法实例；每个适配器还须提供 source attribution、规则相关 capability contract、失败关闭边界和独立评测。当前实现和论文案例研究只含 PlantUML 适配器，因而只报告该适配器的结果。当前 54 个 PlantUML 制品来自 Wang 等上游 LLM generation/feedback pipeline 按冻结 stage/fallback 规则选择的输出；“已存在”不表示必须由人类创作。它面向需要复核状态机制品的研究者与维护者，不是状态机生成或自动修复工具。

当前论文结果只来自 [v61 与 X1v2 baseline 全量归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md)：两臂全部报告由同一台经人工裁定校准的语义 judge 判定（大纲 §5.3），复算脚本为 [evaluate_full.py](./discover_matrix/docs/generations/v61/evaluate_full.py) 与 [evaluate_rq3.py](./discover_matrix/docs/generations/v61/evaluate_rq3.py)。当前比较覆盖同一 54 个 pair、3 个 round、145 条人工标注的参考缺陷条目和 435 个 round-level evaluation units；[v60 人工裁定归档](./final_results/v60_current_vs_x1v2_baseline/README.md)保留为仪器校准参照与历史考据，历史 v46、v27 等代次只在 [实验历史索引](./archive/experiment_history/README.md) 中保留考据，不能作为当前结果或方法说明。

## 研究对象与输入

方法的输入闭包包含自然语言（NL）、源状态机制品、规范化源中间表示、FCSTM、原生检查事实、工作约定与来源追踪。语言适配器将源制品的定位信息带入规范化表示和已声明的 FCSTM 片段；FCSTM 支撑图、仿真和有界分析，原生检查事实提供确定性事实，二者都不产生新的描述义务。工作约定和来源追踪分别记录可用映射与归因。当前案例研究中的源制品语言是 PlantUML。输入、谓词注册表、提示词或模式以及运行约定均由清单和哈希固定。

本研究的状态机片段不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序。当前结果也不外推到其他执行模型、其他 ledger 或未声明的 FCSTM/soundness fragment。

## 当前方法与评测

现行实现依次准备输入闭包、提取 NL 约定、在固定条件下进行一次有界补全、用两个互补视角提出并定位候选，再进行确定性筛选、谓词路由、类型化输入绑定和后端执行。方法为候选保留来源追踪、绑定、回执和 W 级证据；事实、义务与 D/A 由评测仪器另行裁定（人工裁定协议定义，校准语义 judge 执行）。独立评测中，D/A、有效性与对应关系的定义来自 issue #195 的人工裁定协议，执行者是同模型的校准语义 judge（两臂同一仪器，配置与偏移见 [story/paper_outline.md](./story/paper_outline.md) §5.3）；离线程序只在 judge 已完成的字段上校验、汇总并确定性派生 K/N/I。用户已于 2026-09-05 确认 v61 方法侧 903 条报告已人工复核；论文按大纲 §5.3 的人工裁定口径记录两臂结果。

当前方法按工作流证据需求选择四类共 12 种可执行谓词：结构 S1–S5、拓扑 G1–G3、轨迹 R1–R3、有界验证 V1，族规模为 `5/3/3/1`。逐条用途、来源与执行边界见[谓词来源审计](./related_work/provenance/predicate_provenance.md)。谓词用于结构化绑定与执行适用检查；没有适用谓词但已有精确来源定位的发现仍可为 W1，不能具体定位的主张为 W0。D2/D1 报告会发布，D0 不发布；L 是台账分类字段，方法不输出 L。方法不读取台账、评测裁定或历史报告。

这里的“发布”只指方法的 finding publication surface；独立评测和归档仍保留全部 report、validity、relation 与 D/A decision，供复核和复算使用。

[内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 保存 evaluation-only 的后端能力、输入和 receipt 审计。它用于复核证据闭合，不属于 paper1 主叙事，不进入 method registry、prompt、routing 或 package data，也不改写 hit、W、K/N/I。旧 registry 的 planned mapping 与旧 126 条 provenance 都不是当前主结果。

当前 headline 表格只保留在 [v61 归档 README](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 与其 `derived/evaluate_rq3_output.txt`；论文口径的解释与冻结运行的版本说明见 [story/paper_outline.md](./story/paper_outline.md) §5.1。X1v2 没有同构的谓词或 receipt schema，所以 predicate usage 不适用；W 轴仍适用，评测不会倒灌为 baseline method 的 W2。

## 阅读与复现

1. [v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 是结果、分母、限制和复算的唯一入口；[v60 归档](./final_results/v60_current_vs_x1v2_baseline/README.md)只作仪器校准参照。
2. [method/](./method/)、[judge/](./judge/) 与 [evaluation/](./evaluation/) 分别说明运行时方法、语义 judge（含人工裁定协议与校准）和离线评测的边界。
3. [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/README.md) 是当前 145 条台账与其 provenance；它不是 current headline 的第二份结果表。
4. [内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 是后端能力、receipt、review 和离线成分分析入口，不是 paper1 的主结果入口。
5. [story/](./story/README.md) 给出论文叙事、claim 与术语；[archive/experiment_history/](./archive/experiment_history/README.md) 给出重要历史代次的可比性边界。
6. [scripts/](./scripts/README.md) 列出所有薄命令行入口；[pipeline/](./pipeline/README.md) 仅保留输入准备和基础设施导航。

从仓库根可用下列 provider-free 命令从 v61 归档复算论文口径的全部数字：

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
