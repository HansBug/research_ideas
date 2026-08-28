# Paper1 实验历史索引

本目录记录 Paper1 的重要实验代次及其可复核材料。它不提供当前结果，也不替代最终归档。当前论文实验只以 [v60/current 与 X1v2 baseline 最终归档](../../final_results/v60_current_vs_x1v2_baseline/README.md) 为准。

## 如何阅读

同一数字只有在 ledger、Judge、输入闭包、执行模型、轮数和指标定义一致时才可以比较。本页把不一致之处写在对应行内，不能据此计算跨代差值或排名。

| 版本 / 里程碑 | 日期与代码锚点 | 当时方法与实验范围 | ledger 与 Judge | 可复核结果 | 与 v60 的关系、替代原因 | 现有材料与状态 |
| --- | --- | --- | --- | --- | --- | --- |
| v46 method 与旧判定 | 结果记录为 2026-08-10；方法提交 ca41369e46c09eafe6bfbfe64c3754b02c6d8fee；材料于 b6ec2917f16104d3a8ac8b07c8a519dca2bfacf6 在 2026-08-17 归档 | 旧 feedback-loop 路线，54 pair、两条执行模型臂、每臂 3 round，共 324 cells；result.md 记录 324/324 落盘 | 第一版台账 99 条，能力分母经边界裁定为 98；旧 A/B/C 人工判定与人工审计，不是 issue #195 Judge | v46：355/588 = 60.4%，139/196 = 70.9%，95/196 = 48.5%；报告明确这些 hit 只可作上界，因为命中侧尚未完成对称的表示债务审计 | 不可与 v60 或当前 X1v2 相减：台账、方法结构、判定协议、分母和证据等级均不同。后续台账换为 145 条且旧路线归档，v46 仅保留为历史证据 | [r10 归档](../r10_ledger_v1_and_v46/README.md)、[结果](../r10_ledger_v1_and_v46/v46/result.md)、[事前登记](../r10_ledger_v1_and_v46/v46/preregistered.md)、[审计](../r10_ledger_v1_and_v46/v46/audit.md)。historical / superseded |
| v27-stream method 与旧 Judge | 2026-08-20；结果归档提交 2accd7213bad43955314efc6daec8b74e614b03f。已跟踪报告没有完整 method run ID；原方法运行目录只在未跟踪 runs/ 中，本索引不把它当作提交证据 | 重构前的 evidence-discovery 流程，gpt-5.6-luna，54 pair、每臂 3 round；方法臂 162 cells，与 X1v2 的历史臂一起组成旧对照 | 第二版 145 条 ledger，但使用旧 Luna semantic review，不是冻结 issue #195 两阶段 Judge；旧 report 定义的 release emission/FP 与当前 K/N/I 不能混用 | 方法：276/435、107/145、76/145；旧 baseline：177/435、79/145、37/145；旧 report 的 emission precision 为 45.74%，不是当前 report semantic precision | 不可与 v60/X1v2 current 直接比较：Judge、report validity、W、成本审计和发布边界不同。它保留了后续重构的来源和旧路线的测量事实，不承担当前结论 | [v27 报告](../../reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md)、[运行审计](../../reports/2026-08-20-luna-full-x3-v27-stream/RUN_AUDIT.md)、[预注册快照](../../discover_matrix/docs/generations/v27/preregistered.md)。historical / superseded |
| v60/current method + issue #195 Judge | 2026-08-28；method 66b5d71aecd73f6eeddac082037f7c34e04da057，run 915d56e45a634c27aa03866f03818c6d；Judge 05cf0da6f7d9fcf1de26c349b586fc71c268f1c5 | typed evidence-discovery method；54 pair、3 round、162 method cells；输入闭包、registry、prompt/schema 与运行合同均冻结 | 145 expected issue、435 round-level expected，L2 为 39/117；issue #195 protocol github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2 | current：overall FULL 306/435 = 70.34%，L2 FULL 104/117 = 88.89%，hit@3 118/145 = 81.38%，precision 1165/1271 = 91.66% | 当前终点。仅与同一最终归档中的 X1v2 baseline 进行公平比较；不以 v27/v46 数字说明改动收益 | [最终归档](../../final_results/v60_current_vs_x1v2_baseline/README.md)、[正式报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md)、[archive manifest](../../final_results/v60_current_vs_x1v2_baseline/archive_manifest.json)。current |
| X1v2 baseline 的 issue #195 rejudge | 与 v60 共同归档；legacy method 的顶层 source commit 未保存 | 单提示、无工具的比较臂；54 pair、3 round、162 cells、512 findings | 同一 145 条 ledger 与同一 issue #195 Judge。512 条 finding 经两轮独立 W 回溯审计 | overall FULL 211/435 = 48.51%，L2 FULL 46/117 = 39.32%，precision 410/512 = 80.08%；finding-level W0/W1/W2=1/511/0 | 这是比较臂，不是 method 迭代代次。旧 59.8%/70.3%/47.9% 表使用旧 Judge、两条生成模型臂和不同网格，只留作历史记录 | [最终归档报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md)、[W 审计](../../final_results/v60_current_vs_x1v2_baseline/derived/x1v2_witness_level_audit.json)。current comparison arm |

## 演进说明

v46 建立在第一版台账和旧 feedback-loop 判定时期。它留下了有价值的原始审计和表示债务分析，但它的分母、Judge 与方法证据形态均不是 v60 的对象。v27-stream 是重构前最后一次完整方法报告，仍采用旧 Judge 和旧 report validity 口径。v60 把当前 typed evidence-discovery method 与 issue #195 Semantic Judge 和 X1v2 baseline 放入同一冻结归档，形成目前唯一的主比较。

历史文档可以说明某一阶段当时做了什么，不能作为当前方法描述、默认复算入口或论文主结果来源。

## 历史原始数据

[历史原始数据 inventory](./historical_raw_inventory.json) 对 v46 与 v27 分别给出是否建立 ZIP 的决定。v60/current 与 X1v2 baseline 已有结构化最终归档，不重复打包。当前没有新的 ZIP：v46 当前目录只保留 157 个 tracked 文件；完整的 478-file 历史源树需由 `b6ec2917f16104d3a8ac8b07c8a519dca2bfacf6` 恢复。v27 的已跟踪报告和 Judge 审计已保留，而完整 method raw 仅存在于用户未跟踪的 runs/，本任务不会读取、打包或提交它。

若未来确需建立 ZIP，必须从已跟踪、明确的源目录按排序文件清单构建，规范化时间戳和权限，并同时提交逐文件 SHA-256 manifest、排除规则、恢复方法和 unzip -t 记录。不得把 provider request/response stream、cache、凭据、worktree 元数据或临时日志纳入 ZIP。
