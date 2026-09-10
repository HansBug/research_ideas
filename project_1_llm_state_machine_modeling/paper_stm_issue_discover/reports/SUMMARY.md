# 历史报告索引

本页不维护 active report 清单或当前实验结论。当前结果、复算和技术限制见 [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)；代次比较和旧报告的可比性见 [实验历史索引](../archive/experiment_history/README.md)。

| 报告类型 | 使用方式 |
| --- | --- |
| [2026-09-10 A2 三模型汇总与 Qwen 全量结果](./2026-09-10-a2-three-model-results.md) | Luna/Sonnet/Qwen 各 162 格 A2 裁定；普通 precision 均未下降，九簇区间均含零。Qwen full/A2 为 89.25%/91.36%，FULL hit@1 为 311/435 和 283/435，L0/L1 下降而 L2 上升；逐轮、逐 pair 和机器摘要附后。Muse 仅 method 162 eligible，未执行 A2 judge，不计作零分 |
| [2026-09-10 Sonnet 5 A2 全量报告](./2026-09-10-a2-sonnet5-full-results.md) | 162 格全部裁定；A2/full precision 为 88.44%/87.36%，strict precision 为 77.64%/78.98%，FULL hit@1 为 294/435 和 291/435；普通 precision 差值九簇区间跨零，不能沿用 15-pair pilot 作为全量效果证据 |
| v26、v27-stream、v51 及早期 Judge 对照 | historical experiment report；不可与 v60/current 指标直接相减或合并 |
| PlantUML frontend、source trace、ledger contract | implementation/protocol provenance；不构成 current experiment result |
| R5/R5.5 readiness、seed、negative evidence、scope handoff | historical corpus/conversion evidence；不构成当前方法或评测协议 |
| provider-health、e2e smoke | 运维或结构验证证据；不构成论文结果 |
| [2026-09-06 模型调研与推理接入](./model_readiness_20260906/README.md) | 初始调查 workflow 源码 `2971a8ada`；商用/开放模型、近期文献与部署 Markdown 完整保留；09-06 四款开放模型容量/16-worker 及 Gemma method/Gemini 路由/Claude timeout 缺口按历史配置解释，最终四款见总报告；原审计与校验器仅本地留存，不进入正式效果统计 |
| [2026-09-07 最大输出与 stream 大格验收](./model_readiness_20260906/2026-09-07-03-36-18-stream-model-max-acceptance.md) | 源码 `3901b0561` / `75b590306` / `aee59710c`，method 语义未变；15 格 eligible，其中 5 格降级；两开放模型迁移后容量与 16-worker 复验通过；建议 Luna + Sonnet、Qwen3.8 + Muse，保留 Gemini 504 和 Muse/Haiku 结构输出限制；独立于历史预算，不进入正式效果统计 |
| [2026-09-07 全候选 benchmark 与任务选型](./model_readiness_20260906/2026-09-07-04-30-00-candidate-benchmarks.md) | 17 个模型身份、20 个公开档位；09-06 AA Index v4.2 / LCR v1.1 快照，逐值重解析/Markdown 对拍；作者自报另表、严格结构化缺测保留，当前 Qwen low 不等同公开 xhigh；公开能力背景，不是本任务效果排行 |
| [2026-09-07 E1 四模型总报告](./model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md) | Muse serving `7f1131afa`、运行 `c3f01f17a` 三格全部完成；Sonnet 0029 正常证据降级；Qwen 三格零 errors/audit errors；0019/0029/0049 仅三款共 9 格，新 Luna 仅 0001，不宣称四款同样压测；两开放模型 0.9 窗口/16-worker 与故障数字保留。Muse 官方/社区依据及新版 any_order 限制已核对，替代部署未实测；合流回归独立于历史效果 |
| [2026-09-07 E1 复现与原件边界](./model_readiness_20260906/2026-09-07-11-55-00-reproduction.md) | 两独立 conda、精确权重/依赖、YaRN/Muse 参数、GPU/缓存/tunnel 与请求/校验核心；29 个 E1 审计和辅助文件取消跟踪而本地原件不变；历史逐条重放须另行取得原件，不宣称 fresh clone 已附审计或已删除旧 Git 历史 |
| [2026-09-07 Luna 路由复核](./model_readiness_20260906/2026-09-07-06-55-00-luna-route-recheck.md) | 源码 `93d4d1db4`；06:39 baseline 单次成功，4956 input/214 output、128K wire cap；随后两次普通生成、一次原生同 payload、一次 shared runtime 均 503；35 成员和 `fe8713bd2` 下 07:07 单请求原件仅本地保留，不覆盖旧失败或宣称全面恢复 |
| [2026-09-07 Luna 新连接与接入交接](./model_readiness_20260906/2026-09-07-11-10-00-luna-connection-recovery.md) | 只改连接两字段，普通/structured/baseline 通过；adapter `aa64c413f` 修复漏报 response.failed，`5cbf1442d` 下 method 0001/r1：8 阶段完成、5 次 tool/usage、0 errors/audit/schema 修正；160 成员原件仅本地，逐调用数字留表；其他三款证据复用，不等于 E2 协议冻结或持续 SLA |
| [2026-09-08 E2 综合结果：Luna 历史主线与三款 backbone](./2026-09-08-e2-three-backbone-results.md) | 本 PR 唯一人类可读入口；Sonnet、Qwen3.8-27B、Muse 各 324 格完成裁定与离线复算，并纳入历史 Luna main/baseline、两种 precision 定义、配对指标、诊断、judge 8-worker 调整和原始证据边界；机器明细见 `final_results/e2_20260907/`，不启动 O2 |
| [2026-09-09 E2 微观决策画像](./2026-09-09-e2-micro-decision-profiles.md) | 四模型共 1,296 个 cell 的可观测候选 `reason/basis`、属性/方向、证据类型、D 阶段与重复 round 审计；Luna 历史 19 predicates 与三款 12 predicates 明确分开；机器明细由报告脚本本地生成并按报告 hash 核验 |
| [2026-09-06 A1 全量结果与 v61 对照](./2026-09-06-19-49-18-a1-no-inspect-v61-results-cn.md) | [冻结归档及复算](../final_results/a1_no_inspect_vs_v61_20260906/README.md)；162 格、814 报告全部裁定；hit 尤其 L2 明显下降，precision 方向不稳；源码与 provider 分段身份保留，历史对比而非严格单因素估计；人工确认 0，私有原件仅本地 |
| [2026-09-06 A1 `no-inspect` Luna smoke](./2026-09-06-04-10-13-a1-smoke.md) | 源码 `65687f8c6`；A1/full 各 5 格完成；开关隔离、谓词保留与 Luna 链路通过，但存在 provider 恢复和未闭合 evidence；无独立 judge，不构成 hit/precision/KNI 结果；raw audit 仅本地 ignored runs |
| [2026-09-05 P1 十二谓词十格 smoke](./2026-09-05-22-18-46-p1-twelve-predicates-smoke-cn.md) | 来源 `1f852a8b3`；十格完成，93 条匹配终止回执同判，但保留三类证据降级/漏报风险；原始审计仅本地，远端不能独立复核，不主张质量等价；建议暂不追加重跑 |
| [2026-09-02 台账外 D2 跨臂去重分析](./2026-09-02-novel-d2-cross-arm-dedup/analysis.md) | 基于 v4 人工裁定与人工分组的派生分析；跨臂匹配与类型/L 归类为 agent 单轮判读，非人工裁定；只服务 outline §5.4/§6.2 的量级陈述，不进任何主指标 |
| R5.7 Better STM 报告链 | 已归档的历史路线；从 [archive/](../archive/README.md) 进入 |
| [2026-09-06 A2 `no-predicates` Luna smoke](./2026-09-06-11-40-04-a2-smoke.md) | 源码 `507f1bac2`；五格为 3 正常、1 降级、1 失败，31 eligible 报告、2 隔离报告；51 处实际上下文事实对拍通过，谓词零执行；空流未走现有 transport retry，保留运行风险；无独立 judge，不构成效果结论，raw 仅本地 |
| [2026-09-06 A2 完整结果与原因审计](./2026-09-06-20-24-24-a2-no-predicates-v61-results-cn.md) | [独立归档](../final_results/a2_no_predicates_vs_v61_20260906/README.md)；162 格/942 报告全部裁定，FULL hit@1=328/435、precision=800/942；44 gained/39 lost 已逐项定位。未见预期精度下降，四项九簇区间跨零；主/严格口径、269 组相同核心文本分歧及双臂裁定反例均保留。历史版本/provider 对比，非单因素因果估计；人工确认 0。运行源码与创建提交见报告 A.1 |
| [2026-09-09 Sonnet5 C2 15-pair A2 对照](./2026-09-09-03-14-14-c2-sonnet15-a2-comparison.md) | [独立归档](../final_results/c2_sonnet15_20260909/README.md)；15 pair round-1：full 114/94.74%/43，A2 `no-predicates` 126/86.51%/45，full-removal/broad 62/87.10%/33，baseline 89/79.78%/38；另记录 12-pair raw-inspect stress（full 78.79% vs raw 47.37%）。一次 Sonnet draw、定向集合、无新增人工确认；不能作总体或 predicate-only 因果结论。 |
| [2026-09-09 Sonnet5 A2 全量事前登记](../discover_matrix/docs/generations/a2_sonnet5_full_20260909/preregistered.md) | 54 pair × 3 round；Sonnet method `no-predicates`，Luna v3.11 judge；用于确认 15-pair pilot 的 precision/coverage 信号，主张边界限定为整套 predicate-guided mechanism 的条件性净差异。 |

任何新读者应先读工作区 [README.md](../README.md) 和 v61 归档，而不是从本目录选择一份旧报告作为默认入口。
