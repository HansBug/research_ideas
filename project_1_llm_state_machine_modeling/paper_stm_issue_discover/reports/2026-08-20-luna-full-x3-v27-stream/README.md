# v27-stream Luna 全量结果

本目录保存 paper1 witness-search v27-stream 的 54 个非 NL04 pair、三轮方法运行与同一 Luna 模型下 X1v2 baseline 的独立语义评审结果。方法原始运行目录位于本机 `runs/paper1/luna-full-x3-20260820-v27-stream/`，baseline 原始运行目录位于 `runs/paper1/luna-full-x3-20260819-v1/`；原始 prompt、response 和每格 stage record 体积较大，保留在本机运行目录，不把密钥或原始敏感配置复制进仓库。

最终报告见 `REPORT-luna.md`，机器可读汇总见 `metrics.json`，方法与 X1v2 逐条台账表分别见 `ledger_method.md` 和 `ledger_baseline.md`。`judge-luna/` 保存 54 份真实 Luna pair judgement，`judge-luna/audit-manifests/` 保存 6 个并行 worker 的调用审计 manifest；judge 仅读取方法末端 `report_issue_clusters` 中的 D1/D2，D0 只留在 raw record 审计面。

本轮最终主要结果为：整体 hit@1 方法 `276/435`、X1v2 `177/435`；整体 hit@3 方法 `107/145`、X1v2 `79/145`；L2 hit@3 方法 `35/39`、X1v2 `13/39`；D2×L2 hit@3 方法 `30/34`、X1v2 `11/34`。方法 release-emission precision 为 `45.74%`，X1v2 为 `41.60%`；方法绝对 FP 较多但 FP rate 更低，详见报告中的双口径说明。

统计纪律固定为：D1/D2 `report_issue_clusters` 才是最终发布面；D0、D_UNRESOLVED、raw finding、coverage gap 和内部诊断不进入 hit 或 FP。hit/FP 由 Luna LLM 语义 judge 对照冻结台账裁定，禁止关键词、substring、正则、编辑距离、embedding 或其他词法捷径。judge token 和成本独立审计，不并入方法 issue-generation 倍率。

本轮方法矩阵 162/162 格完成且观测均使用 stream；provider error retry 只对实际同请求重发的前序 attempt 免计费，其他 attempt 均计费。方法成本 `$6.633537`、X1v2 `$0.225233`、倍率 `29.45x`；本轮按优先级先保护 hit、L2 和 FP，成本超 25x 作为后续优化项记录。
