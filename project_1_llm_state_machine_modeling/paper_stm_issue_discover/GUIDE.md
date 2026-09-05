# Paper1 工作指引

本文件说明当前工作区的稳定入口和边界。研究问题、当前结果和适用范围先读 [README.md](./README.md)；精确指标、hash、复算和限制只读 [v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md)。

| 工作目标 | 权威入口 |
| --- | --- |
| 理解或修改当前方法实现 | [method/](./method/README.md)；prompt、schema、registry、backend 或输入闭包的变化需要独立实验授权 |
| 设计、实现或审查 A1/A2 消融 | [消融设计与并行施工公约](./discover_matrix/docs/protocol/ablation_design_and_parallel_contract.md)；两路必须共同遵守关闭边界、共享接口、full 不变和合流验收要求 |
| 理解人工裁定 | [judge/](./judge/README.md) 与冻结 issue #195 snapshot |
| 复算结果或检查指标 | [evaluation/](./evaluation/README.md) 与 v61 归档的 `evaluate_rq3.py` / `evaluate_full.py`；默认只运行 provider-free 命令 |
| 查询 current ledger/provenance | [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/README.md) |
| 准备输入或查询兼容代码 | [pipeline/](./pipeline/README.md) |
| 查询历史代次 | [archive/experiment_history/](./archive/experiment_history/README.md) |

`pipeline/feedback_loop`、旧 v46/v27/v26 报告、R5/R5.7 设计和早期人工裁定记录仅用于历史追溯，不是当前方法或结果来源。方法不得读取 ledger、expected answer、人工裁定输出或历史 report；人工裁定和 evaluation 的职责分别见各自 README。

真实 provider 调用只能在单独明确授权的实验任务中进行。默认验证使用 fixture、安装、`--help`、边界测试和 archive validator；不得用未声明的 live run 替代冻结制品或离线复算。
