# 历史报告索引

本页不维护 active report 清单或当前实验结论。当前结果、复算和技术限制见 [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)；代次比较和旧报告的可比性见 [实验历史索引](../archive/experiment_history/README.md)。

| 报告类型 | 使用方式 |
| --- | --- |
| v26、v27-stream、v51 及早期 Judge 对照 | historical experiment report；不可与 v60/current 指标直接相减或合并 |
| PlantUML frontend、source trace、ledger contract | implementation/protocol provenance；不构成 current experiment result |
| R5/R5.5 readiness、seed、negative evidence、scope handoff | historical corpus/conversion evidence；不构成当前方法或评测协议 |
| provider-health、e2e smoke | 运维或结构验证证据；不构成论文结果 |
| [2026-09-06 A1 全量结果与 v61 对照](./2026-09-06-19-49-18-a1-no-inspect-v61-results-cn.md) | [冻结归档及复算](../final_results/a1_no_inspect_vs_v61_20260906/README.md)；162 格、814 报告全部裁定；hit 尤其 L2 明显下降，precision 方向不稳；源码与 provider 分段身份保留，历史对比而非严格单因素估计；人工确认 0，私有原件仅本地 |
| [2026-09-06 A1 `no-inspect` Luna smoke](./2026-09-06-04-10-13-a1-smoke.md) | 源码 `65687f8c6`；A1/full 各 5 格完成；开关隔离、谓词保留与 Luna 链路通过，但存在 provider 恢复和未闭合 evidence；无独立 judge，不构成 hit/precision/KNI 结果；raw audit 仅本地 ignored runs |
| [2026-09-05 P1 十二谓词十格 smoke](./2026-09-05-22-18-46-p1-twelve-predicates-smoke-cn.md) | 来源 `1f852a8b3`；十格完成，93 条匹配终止回执同判，但保留三类证据降级/漏报风险；原始审计仅本地，远端不能独立复核，不主张质量等价；建议暂不追加重跑 |
| [2026-09-02 台账外 D2 跨臂去重分析](./2026-09-02-novel-d2-cross-arm-dedup/analysis.md) | 基于 v4 人工裁定与人工分组的派生分析；跨臂匹配与类型/L 归类为 agent 单轮判读，非人工裁定；只服务 outline §5.4/§6.2 的量级陈述，不进任何主指标 |
| R5.7 Better STM 报告链 | 已归档的历史路线；从 [archive/](../archive/README.md) 进入 |

任何新读者应先读工作区 [README.md](../README.md) 和 v61 归档，而不是从本目录选择一份旧报告作为默认入口。
