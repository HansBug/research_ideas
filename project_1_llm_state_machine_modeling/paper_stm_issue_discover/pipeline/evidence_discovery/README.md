# `pipeline.evidence_discovery` 兼容命名空间

本目录保留重构前的 import 兼容层、历史测试和只读辅助代码。它不是当前 method 的实现或运行入口，也不定义 prompt、谓词、W/D、publication 或评测口径。

| 需要了解的内容 | 权威入口 |
| --- | --- |
| 当前 method、输入闭包、12 条谓词、W/D 与 CLI | [method/](../../method/README.md) 与 `paper_stm_method` |
| 人工裁定协议和输入输出 | [judge/](../../judge/README.md) 与 `paper_stm_judge` |
| hit、precision、W-on-hits、K/N/I、cost 与离线复算 | [evaluation/](../../evaluation/README.md) 与 `paper_stm_evaluation` |
| 当前冻结评测结果 | [项目当前入口](../../README.md) |

兼容层保留通向当前实现的导入路径，不能作为新实验入口，也不再提供历史 replay 的执行入口。历史 replay 依赖原 commit 的类型和后端，使用[历史版本记录](../../related_work/provenance/archive/pre_p1_20260905/README.md)中的复现入口。它不读取 ledger、expected answer、人工裁定输出或其他 pair 的数据，也不能把 replay 的 receipt 写回冻结 method finding，或把它计为新的 W2、hit 或 precision。

当前方法语义见 `method/` 的资源和包 README；冻结运行的语义以其 manifest 和原 commit 为准。复算结果与旧编号映射使用 `evaluation/` 的离线入口。旧 `feedback_loop` 实现只保留在 [archive/legacy/feedback_loop/](../../archive/legacy/feedback_loop/README.md)，用于历史复核，不属于当前路径。
