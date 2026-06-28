# 候选场景与证据资产总账

状态口径：🟢 = `main` 中已有可复核入口；🟡 = 计划或需 A1/A3 复核；🟣 = PR #97 OPEN / 未合入 / 快照 / 分支局部证据。emoji 列只放 emoji。

| 资产 / 场景 | 状态 | 当前角色 | A3 前置要求 | 禁止写法 |
|---|---:|---|---|---|
| PR-A1 LLM4STM / LLM4Modeling 种子 | 🟢 | 5 篇正选种子 + 备选 / 排除候选，直接服务 A2 schema、A3 mini-case、A5a 指标冻结。 | A3 必须从 [a1_seed_papers.md](./a1_seed_papers.md) 中选择具体 mini-case，并记录未选理由。 | 不能写成最终 benchmark 或已运行结果。 |
| `sources/` 控制系统 STM 文库 | 🟢 | 可作为领域压力测试或证据包案例来源。 | 复核当前 `main` 总账数量、抽样策略和版权边界。 | 不能写第二篇主贡献是 `sources` 语料。 |
| PR #97 baseline 文库 | 🟣 | 可作为相关工作筛选 / 全文抽取的快照线索。 | 按 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 核验 OPEN / snapshot SHA；merge 后做事实合流。 | 不能写 PR #97 资产已合入 `main`。 |
| issue #85 / #101 历史评论 | 🟡 | 可作为 story 理由与候选场景设计线索。 | 必须回落到仓库文件、PR body 或可复验数据，不得只引用 comment。 | 不能把 comment 当实验数据。 |
| 小型已知领域 SLR / SMS 场景 | 🟡 | 便于构造金事实 / 银事实与陷阱论文。 | A3 定义 RQ、known-item seed、人工审计样本和排除理由台账。 | PR-S0 不能声称已构造。 |
| LLM4SE / LLM4Modeling 场景 | 🟡 | 贴近博士大主题，可验证近邻文献筛选和证据综合。 | A1 已在 [a1_seed_papers.md](./a1_seed_papers.md) 选择 5 篇 LLM4STM / LLM4Modeling 最小闭环种子；A3 需再构造 gold / silver facts。 | 不能提前写覆盖率、召回率或真实运行效果。 |
| 控制系统 STM / `sources/` 场景 | 🟡 | 高贴合 project_1，可作为压力测试。 | A3 冻结样本、全文可获取性、抽取 schema 和审计门。 | 不能把 `sources/` 全库默认视为可公开 benchmark。 |
