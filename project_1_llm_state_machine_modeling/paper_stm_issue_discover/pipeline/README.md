# pipeline：输入准备与基础设施导航

当前可发布的运行时实现不再位于 `pipeline/`：方法、Semantic Judge 和评测分别在 [../method/](../method/README.md)、[../judge/](../judge/README.md) 与 [../evaluation/](../evaluation/README.md)。本目录保留输入准备、转换制品、兼容 namespace 和需要追溯的基础设施材料；它不是当前论文的结果入口。

| 路径 | 当前职责 | 边界 |
| --- | --- | --- |
| [conversion/](./conversion/README.md) | PlantUML 到 canonical source representation 的准备链 | 改变制品须通过其专门验证；当前结果读取冻结输入 |
| [representation/](./representation/README.md) | 生成或保留输入闭包所需表示与报告目录 | 不承担 method discovery 或评测业务逻辑 |
| [readiness_audit/](./readiness_audit/README.md) | 已保存的语料准入与输入审计材料 | 只读历史和 provenance，非当前结果来源 |
| [evidence_discovery/](./evidence_discovery/README.md) | 迁移后的 method/evaluation compatibility namespace | 仅兼容旧 import；新代码应使用 `paper_stm_method` 或 `paper_stm_evaluation` |
| [archive/](./archive/) | 本目录下的旧原型材料 | 只作历史追溯 |

已停用的 `feedback_loop` 迁入 [../archive/legacy/feedback_loop/](../archive/legacy/feedback_loop/README.md)，不在默认安装、当前 method release 或当前实验叙事中。需要复算最终实验时请使用 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md) 的 evaluator 命令，而不是从本目录寻找旧运行入口。
