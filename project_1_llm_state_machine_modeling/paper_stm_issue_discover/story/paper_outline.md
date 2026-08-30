# Paper1 论文提纲

| 章节 | 讨论内容 | 主要证据 |
| --- | --- | --- |
| 1. 问题与范围 | NL 与作者状态机之间的问题发现任务、研究对象和不覆盖的语义 | [研究范围](./paper_story.md) 与 scope protocol |
| 2. 背景与相关工作 | 需求-模型一致性、状态机分析、LLM 辅助建模与可执行证据 | [related_work/](../related_work/) 的可核查资料 |
| 3. 方法 | 输入闭包、contract extraction/completion、双 lens、frontier、谓词执行、D/W 与 publication | [method/](../method/README.md) 和冻结方法制品 |
| 4. 独立判定与评测 | issue #195 Judge 的 validity/relation 两轴，以及 evaluator 的分母与指标所有权 | [judge/](../judge/README.md) 与 [evaluation/](../evaluation/README.md) |
| 5. 实验设计 | 54 pair、145 条 ledger、3 round、X1v2 baseline、输入与 hash 固定方式 | [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md) |
| 6. 结果 | hit、L2、precision、W-on-hits、谓词使用与成本资格 | [中文正式报告](../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md) |
| 7. 威胁与限制 | ledger/Judge 测量边界、片段范围、执行模型与成本资格 | 正式报告的限制与 [claim map](./claim_evidence_map.md) |
| 8. 结论 | 在冻结范围内总结可审计发现链路及其结果 | 前述冻结证据 |

历史 v46、v27-stream、旧 Judge 和旧 feedback-loop 不安排在上述主结果章节中。若需要解释演进，只在相关工作或历史背景中引用 [实验历史索引](../archive/experiment_history/README.md)，并同时说明不可比条件。
