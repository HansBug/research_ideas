# Paper1 论文叙事

本目录是 Paper1 当前的故事合同，服务于冻结的主臂与基线比较。Paper1 提出以有限控制状态机（finite control state machine，FCSTM）为分析工作表示的通用状态机问题发现架构，通过语言适配器接收分析前已存在、带来源归属且在分析期间保持固定的源状态机制品。能在声明子集内形成可追溯 FCSTM 投影的语言可实现为方法实例；每个适配器都须完成 source attribution、规则相关 capability contract、投影与 fail-closed boundary 及独立评测。当前实现与冻结结果只覆盖 PlantUML 适配器和相应案例研究；输入可以来自人工或上游 LLM。这里不替代[最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md)的数据、[方法](../method/README.md)的运行约定或人工评测协议。

| 文档 | 作用 |
| --- | --- |
| [paper_story.md](./paper_story.md) | 问题、总方法、C1/C2、实际意义、RQ 和可写边界 |
| [paper_outline.md](./paper_outline.md) | 唯一 canonical paper outline：准论文级章节、证据、图表、引用与实验门 |
| [claim_evidence_map.md](./claim_evidence_map.md) | strongest defensible claims、证据、相关工作风险与限制 |
| [terminology_policy.md](./terminology_policy.md) | C1/C2、L/W/D、关系、K/N/I 与人工责任边界 |
| [model_scope.md](./model_scope.md) | `M=(S,E,V,Tr,A)`、FCSTM 投影、来源归因和证据范围 |

当前相关工作和谓词出处分别从[最接近工作矩阵](../related_work/closest_work_matrix.md)与[谓词来源审计](../related_work/provenance/predicate_provenance.md)进入。旧反馈循环、旧评审机制和旧版本结果只在[实验历史索引](../archive/experiment_history/README.md)保留，不应回流为当前主张或结果。
