# Paper1：状态机模型问题发现

本工作区研究如何审计一份由 LLM 生成的状态机模型：给定自然语言需求和作者的 PlantUML 状态机，方法发现需求、模型结构或可执行状态机语义之间不一致的地方，并为每条发现保留可追溯的定位和证据。它面向需要复核 LLM 建模结果的研究者与维护者，而不是状态机生成或自动修复工具。

当前论文结果只来自 [v60/current 与 X1v2 baseline 最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md)。当前比较覆盖同一 54 个 pair、3 个 round、145 条 expected issue 和 435 条 round-level expected row；历史 v46、v27 等代次只在 [实验历史索引](./archive/experiment_history/README.md) 中保留考据，不能作为当前结果或方法说明。

## 研究对象与输入

每个 pair 的输入闭包包含 NL、作者 PlantUML、canonical source IR、FCSTM、inspection-equivalent/native facts、working contract 与 source trace。作者 PlantUML 和 canonical source IR 用于定位作者制品；FCSTM 支撑可执行语义；inspection/native facts 是确定性事实库存，不能被写成新的规范义务；working contract 与 source trace 分别记录可用映射和归因。输入、registry、prompt/schema 与运行合同均由 manifest 和 hash 固定。

本研究的状态机片段不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序。当前结果也不外推到其他执行模型、其他 ledger 或未声明的 FCSTM/soundness fragment。

## 当前方法与评测

现行 runner 的顺序是：输入闭包准备，NL contract extraction，必要时一次有界的 contract completion，两个互补的 discovery-grounding lens，确定性 frontier、predicate routing、typed input binding 与 backend execution，方法内 D adjudication 和受限定向 correction，确定性 W，D1/D2 publication 与 exact typed deduplication。随后独立 Semantic Judge 按 issue #195 执行 relation 与 validity 两个正交维度的裁定，最后由 provider-free evaluation 汇总指标。

冻结的四族 19 谓词用于把一部分发现变为可执行证据，并在满足完整 receipt 时形成 W2。谓词不是问题发现的准入门；没有适合谓词的具体问题仍可按 W1 或 W0 进入方法内 D 裁定。D2/D1 才会发布，D0 不发布；L 是 ledger 的分类字段，方法不输出 L。方法不读取 ledger、expected answer、Judge 输出或历史 report。

[predicate gold v1](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 为 145 条台账义务保存 method-independent expected predicate、typed inputs、exact/proxy/unsupported 裁决和 provider-free receipt。它是 evaluation-only 参考层，不进入 method registry、prompt、routing 或 package data，也不改写 hit、W、K/N/I。旧 registry 的 planned mapping 与旧 126 条 provenance 都不是当前逐条 gold。

当前 headline 表格只保留在[正式 v4 公平对照报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。该报告的 JSON、TSV、分母和限制由[最终归档 README](./final_results/v60_current_vs_x1v2_baseline/README.md)链接；本页不再复制第二套结果表。X1v2 没有同构的 19 谓词或 receipt schema，所以 predicate usage 不适用；W 轴仍适用，Judge 后续核验不会倒灌为 baseline method 的 W2。

## 阅读与复现

1. [最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md) 是结果、分母、限制和复算的唯一入口；纸面 headline 只见[中文 v4 正式报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)。
2. [method/](./method/)、[judge/](./judge/) 与 [evaluation/](./evaluation/) 分别说明运行时方法、独立 Semantic Judge 和离线评测的边界。
3. [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/README.md) 是当前 145 条台账与其 provenance；它不是 current headline 的第二份结果表。
4. [predicate gold v1](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) 是 expected property/input、receipt、review 和离线 expected-vs-actual 分析入口。
5. [story/](./story/README.md) 给出论文叙事、claim 与术语；[archive/experiment_history/](./archive/experiment_history/README.md) 给出重要历史代次的可比性边界。
6. [scripts/](./scripts/README.md) 列出所有薄命令行入口；[pipeline/](./pipeline/README.md) 仅保留输入准备和基础设施导航。

从仓库根可用下列 provider-free 命令验证最终归档：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

## 目录边界

`method/` 只产生发现和方法证据；`judge/` 只执行冻结 issue #195 判定。headline evaluation 只读取完成的制品并计算 hit、precision、W-on-hits、K/N/I、predicate usage 与成本；隔离的 predicate-gold 工具可以在 evaluation 层执行或重放预冻结 query，但不参与 discovery-time method predicate execution，也不进入 method 或 Judge。顶层 `utils/` 只提供中立运行时和制品读取能力。[archive/legacy/feedback_loop/](./archive/legacy/feedback_loop/README.md) 是保留的旧实现，不是现行方法。

当前技术发布结构、内部 release candidate 与固定 15-pair 技术回归记录在 [release_validation/](./release_validation/README.md)。它们证明重构后的包结构和复现边界，不改变本页的冻结主实验。method source 的正式对外再分发仍需权利人明确指定 LICENSE；这不改变内部技术制品的复现状态。
