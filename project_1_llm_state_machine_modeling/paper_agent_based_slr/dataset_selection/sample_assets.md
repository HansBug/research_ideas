# sample_assets.md：A0 候选场景与证据资产总账

状态口径：🟢 = `main` 中已有可复核入口；🟡 = 计划或需 A1/A3 复核；🟣 = PR #97 OPEN / 未合入 / snapshot / 分支局部证据。emoji 列只放 emoji。

| 资产 / 场景 | 状态 | 当前角色 | A3 前置要求 | 禁止写法 |
|---|---:|---|---|---|
| `sources/` 控制系统 STM 文库 | 🟢 | 可作为 domain stress test 或 evidence package case 来源。 | 复核当前 `main` 总账数量、抽样策略和版权边界。 | 不能写第二篇主贡献是 `sources` corpus。 |
| PR #97 baseline 文库 | 🟣 | 可作为 related-work screening / fulltext extraction 的 snapshot 线索。 | 按 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 核验 OPEN / snapshot SHA；merge 后做 fact-union。 | 不能写 PR #97 资产已合入 `main`。 |
| issue #85 / #101 historical comments | 🟡 | 可作为 story rationale 与候选 scenario 设计线索。 | 必须回落到仓库文件、PR body 或可复验数据，不得只引用 comment。 | 不能把 comment 当实验数据。 |
| 小型已知领域 SLR / SMS 场景 | 🟡 | 便于构造 gold / silver facts 与 trap papers。 | A3 定义 RQ、known-item seed、人工审计样本和排除理由台账。 | A0 不能声称已构造。 |
| LLM4SE / LLM4Modeling 场景 | 🟡 | 贴近博士大主题，可验证近邻文献筛选和证据综合。 | A1 先完成 LLM-assisted SLR / LLM4MDE 近邻检索。 | 不能提前写 coverage 或 recall。 |
| 控制系统 STM / `sources/` 场景 | 🟡 | 高贴合 project_1，可作为 stress test。 | A3 冻结样本、fulltext availability、抽取 schema 和 audit gate。 | 不能把 `sources/` 全库默认视为可公开 benchmark。 |
