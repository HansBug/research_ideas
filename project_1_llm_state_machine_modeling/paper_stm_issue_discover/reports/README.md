# Paper1 实验与历史报告

[A3 四模型中间引导消融](./2026-09-10-20-39-37-a3-four-model-results.md) 是 A3 完整四模型的正式解释入口，包含普通/strict precision、有效报告与去重覆盖、24 行逐轮、内容分层和三个来源案例；配套[学术 talk](../../talks/2026-09-10-实验-A3中间引导消融与论文叙事.md)说明发现贡献与模型差异。[两模型旧报告](./2026-09-10-a3-direct-report-results-cn.md)保留为 Sonnet/Luna 历史快照。

[A4 谓词执行反馈消融](./2026-09-10-17-01-11-a4-frozen-full-tail-results.md) 记录全员 unknown 干预、四款模型全部 648 格/3675 份报告核销后的两种 precision、逐轮分母、候选筛选与源案例。随附小型核算 JSON 可独立复算已归档计数，Qwen 旧失败与后续成功裁定均保留；逐调用原始记录仅本地保存。配套[学术 talk](../../talks/2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md)解释四模型差异、误报抑制与 C-2。

[A1-ext 三模型无检视事实消融](./2026-09-12-10-17-38-a1-ext-three-model-no-inspect-results.md) 把 A1 的 `no-inspect` 干预扩展到 Claude Sonnet 5、Qwen3.8-27B、Muse Glimmer-30B，与 gpt-5.6-luna 的 A1 归档并列为四模型对照；含 24 行逐轮、L 分层、命中集合迁移、台账轴内容分层、候选与证据资格组成、三个来源可核查案例、九簇区间与 A.1–A.4 证据链，配套[学术 talk](../../talks/2026-09-12-实验-A1ext三模型无检视事实消融与论文叙事.md)与[冻结归档](../final_results/a1_ext_20260911/README.md)。

本目录保存按日期冻结的实验解释、过程报告、早期 Judge 结果、转换说明和运行健康记录。报告说明对应版本的结论与限制；逐格判定、分母和离线复算以各报告指向的 `final_results/` 归档为准。

现有论文 headline 仍见 [v61 与 X1v2 baseline 冻结归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)。[v60 人工裁定归档](../final_results/v60_current_vs_x1v2_baseline/README.md)及其 [v4 中文报告](../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)作为校准与历史参照保留；后续独立实验保留自己的版本、配置、裁定和可比性说明，不静默替换或混合历史结果。

`2026-08-19-luna-full-x3-v26*`、`2026-08-20-luna-full-x3-v27-stream/` 与 `2026-08-25-evidence-discovery-v51-final-54x3.md` 都是历史报告或重构前结果快照。它们的 Judge、发布边界、W、成本或指标定义不与 v60/current 静默聚合。需要理解版本演进时，从 [实验历史索引](../archive/experiment_history/README.md) 进入，并在同一行查看可比性条件。

R5/R5.7、Better STM、repair、旧 lifecycle 与 provider-health 材料同样属于 provenance 或历史复现；不应被用作当前方法的运行入口。保留这些文件不会改变最终归档，也不会使早期数字重新成为当前事实。

[2026-09-06 模型调研与推理接入快照](./model_readiness_20260906/README.md) 保存商用/开放模型官方事实、近半年 14 篇文献样本、远程 H200 负载及最小 workflow 证据。该组是基础设施与研究选型资料，不是新的效果实验；全部 smoke 排除于正式结果。

[全候选 benchmark 与任务选型](./model_readiness_20260906/2026-09-07-04-30-00-candidate-benchmarks.md) 保留未入选模型、公开推理档位、同版本 AA 矩阵、作者自报与严格结构化缺测；逐值历史复算须另行取得本地来源快照。

[E1 四模型总报告](./model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md) 汇总配置、Muse serving 修复、Sonnet 正常 D 证据降级、九格 stream 与四款 baseline/ours、Luna 新连接及历史故障、容量和并发数字；旧失败和历史实验不覆盖。[复现附录](./model_readiness_20260906/2026-09-07-11-55-00-reproduction.md) 收录独立 conda/权重/启动/tunnel、请求与校验核心。

[E2 综合结果报告：Luna 历史主线与三款 backbone 双臂实验](./2026-09-08-e2-three-backbone-results.md) 是本 PR 唯一的人类可读结果入口，汇总 Sonnet、Qwen3.8-27B、Muse Glimmer-30B 各 324 格的冻结裁定、历史 Luna main/baseline、配对统计、8-worker judge 调整、恢复与证据边界；逐格内容和无 API 复算见 [E2 紧凑归档](../final_results/e2_20260907/README.md)。

[E2 微观决策画像](./2026-09-09-e2-micro-decision-profiles.md) 在同一冻结归档上审计 Luna、Sonnet、Qwen 和 Muse 的逐候选 `reason/basis`、属性/方向、证据类型、阶段调用、同输入 Jaccard 和 round 转移；机器明细由报告脚本在本地生成并按报告中的 hash 核验，仅作可观测输出的描述性分析，不读取或推断 hidden chain-of-thought。

2026-09-07 用户明确 E1 的原始审计和辅助脚本仅本地保留，Git 提供 Markdown 事实、生产代码和必要回归；fresh clone 不含逐条历史审计原件。此交付边界仅适用于 E1，不改变 A1/v61 正式结果或其他材料。

[Luna 路由复核](./model_readiness_20260906/2026-09-07-06-55-00-luna-route-recheck.md) 单列最终 baseline 一次成功与随后普通生成/structured runtime 的四个 503，避免将单次成功写成全部路径恢复。

[Luna 新连接与四模型接入交接](./model_readiness_20260906/2026-09-07-11-10-00-luna-connection-recovery.md) 更新最终连接：普通/structured/baseline 与完整 stream method 通过，补充 Responses 失败事件分类修复，保留旧渠道失败；四款已测配置及 E2 推理档位边界可复核。
