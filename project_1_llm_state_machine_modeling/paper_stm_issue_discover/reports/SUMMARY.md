# 历史报告索引

本页不维护 active report 清单或当前实验结论。当前结果、复算和技术限制见 [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)；代次比较和旧报告的可比性见 [实验历史索引](../archive/experiment_history/README.md)。

| 报告类型 | 使用方式 |
| --- | --- |
| v26、v27-stream、v51 及早期 Judge 对照 | historical experiment report；不可与 v60/current 指标直接相减或合并 |
| PlantUML frontend、source trace、ledger contract | implementation/protocol provenance；不构成 current experiment result |
| R5/R5.5 readiness、seed、negative evidence、scope handoff | historical corpus/conversion evidence；不构成当前方法或评测协议 |
| provider-health、e2e smoke | 运维或结构验证证据；不构成论文结果 |
| [2026-09-06 模型调研与推理接入](./model_readiness_20260906/README.md) | 新建调查，workflow 源码 `2971a8ada`；四份 canonical report 与脱敏 ZIP/逐请求复算入口；四款开放模型约 0.9 context、16K thinking 16 worker 通过，Gemma method 降级、Gemini 路由及 Claude timeout 缺口保留；选型尚未冻结；不进入正式效果统计 |
| [2026-09-07 最大输出与 stream 大格验收](./model_readiness_20260906/2026-09-07-03-36-18-stream-model-max-acceptance.md) | 源码 `3901b0561` / `75b590306` / `aee59710c`，method 语义未变；15 格 eligible，其中 5 格降级；两开放模型迁移后容量与 16-worker 复验通过；建议 Luna + Sonnet、Qwen3.8 + Muse，保留 Gemini 504 和 Muse/Haiku 结构输出限制；独立于历史预算，不进入正式效果统计 |
| [2026-09-07 全候选 benchmark 与任务选型](./model_readiness_20260906/2026-09-07-04-30-00-candidate-benchmarks.md) | 17 个模型身份、20 个公开档位；09-06 AA Index v4.2 / LCR v1.1 快照，逐值重解析/Markdown 对拍；作者自报另表、严格结构化缺测保留，当前 Qwen low 不等同公开 xhigh；公开能力背景，不是本任务效果排行 |
| [2026-09-07 四模型配置与交接证据](./model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md) | Muse serving `7f1131afa`，运行 `c3f01f17a`：三格阶段全部完成，0 errors/audit errors；Sonnet 0029 为正常证据降级；三款最终 baseline 成功，Luna 六次新 baseline 均上游 503；约 0.9 窗口/16-worker、配置/环境锁与复现入口齐全；补充旧 stream 快照，原始失败不覆盖 |
| [2026-09-07 Luna 路由复核](./model_readiness_20260906/2026-09-07-06-55-00-luna-route-recheck.md) | 源码 `93d4d1db4`；最终 stream baseline 06:39 单次成功，4956 input/214 output、128K wire cap；随后两次普通生成、一次原生同 payload、一次共用 structured runtime 均 503；35 个成员独立归档，另附 `fe8713bd2` 下 07:07 同配置仍 503 的单请求记录，不覆盖旧失败，也不宣称渠道全面恢复 |
| [2026-09-05 P1 十二谓词十格 smoke](./2026-09-05-22-18-46-p1-twelve-predicates-smoke-cn.md) | 来源 `1f852a8b3`；十格完成，93 条匹配终止回执同判，但保留三类证据降级/漏报风险；原始审计仅本地，远端不能独立复核，不主张质量等价；建议暂不追加重跑 |
| [2026-09-02 台账外 D2 跨臂去重分析](./2026-09-02-novel-d2-cross-arm-dedup/analysis.md) | 基于 v4 人工裁定与人工分组的派生分析；跨臂匹配与类型/L 归类为 agent 单轮判读，非人工裁定；只服务 outline §5.4/§6.2 的量级陈述，不进任何主指标 |
| R5.7 Better STM 报告链 | 已归档的历史路线；从 [archive/](../archive/README.md) 进入 |

任何新读者应先读工作区 [README.md](../README.md) 和 v61 归档，而不是从本目录选择一份旧报告作为默认入口。
