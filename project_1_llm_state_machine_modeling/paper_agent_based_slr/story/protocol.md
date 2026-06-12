# Agent-based SLR 最小流程协议

## 1. 协议目标

本协议定义 A0 阶段的 agent-based SLR / systematic mapping workflow 边界。它不是最终实现，也不是 A5 评价指标协议；它只规定后续 A2/A3/A4/A5 必须保留哪些输入、输出、人工审计门和证据链。

## 2. 流程总览

```text
RQ / scope seed
  -> protocol draft
  -> human protocol approval
  -> query planning and search
  -> deduplication and screening
  -> fulltext availability logging
  -> extraction and evidence location
  -> coding and taxonomy
  -> synthesis and claim-evidence map
  -> PRISMA-style transparency material
  -> final claim review
```

## 3. Stage Contract

| Stage ID | 阶段 | 输入 | 输出 | 必需审计信息 |
|---|---|---|---|---|
| S0 | Protocol setup | topic、RQ seed、scope constraints | protocol draft、纳排标准、数据库范围 | human approval、版本、偏离日志。 |
| S1 | Query planning | approved protocol、数据库范围 | query strings、search plan | 查询式理由、日期、数据库、限制条件。 |
| S2 | Search logging | query strings | raw result、metadata cache | source、时间、命中数、失败记录。 |
| S3 | Deduplication | raw result | candidate pool | 去重键、冲突处理、保留理由。 |
| S4 | Screening | candidate pool、纳排标准 | include / exclude ledger | 理由、置信度、人工抽检、分歧。 |
| S5 | Fulltext status | included pool | fulltext availability log | legal source、用户提供、下载失败、版权边界。 |
| S6 | Extraction | fulltext / metadata | extraction table | 字段来源、页 / 段定位、uncertain、负证据。 |
| S7 | Coding | extraction table、coding schema | coding decisions | 标签定义、证据、分歧、裁决。 |
| S8 | Synthesis | coded corpus | matrices、draft claims | claim-evidence map、unsupported claim check。 |
| S9 | Reporting | synthesis、audit log | report draft、PRISMA-style materials | final claim review、threats、artifact checklist。 |

## 4. Human Audit Gates

| Gate | 位置 | 目的 | 最小记录 |
|---|---|---|---|
| G0 Protocol approval | S0 后 | 防止 scope 和 RQ 一开始漂移。 | 审批人、时间、批准版本、修改意见。 |
| G1 Screening audit | S4 中 / 后 | 检查 inclusion / exclusion 理由是否可接受。 | 抽样策略、分歧率、裁决日志。 |
| G2 Gold / silver fact audit | S6 / S7 | 为抽取和编码提供事实锚点。 | fact ID、来源、证据定位、置信等级。 |
| G3 Disagreement adjudication | S7 / S8 | 处理 agent / reviewer 分歧。 | 分歧类型、裁决结果、理由。 |
| G4 Final claim review | S9 前 | 拦截无证据 claim 和过强 conclusion。 | claim ID、支持证据、降级或删除记录。 |

## 5. Claim-to-source 不可断链要求

每个报告级 claim 必须至少能追溯到：

```text
claim -> synthesis row -> coding decision -> extraction record -> evidence locator -> paper metadata -> screening decision -> query/search batch -> audit status
```

若任一环节缺失，应标记为 `断链`，不得进入摘要或主要结论。

## 6. A0 不冻结的内容

A0 不冻结以下内容：

1. 每个 stage 的 JSON schema 细节；这由 A2 冻结。
2. 具体 benchmark scenarios；这由 A3 冻结。
3. 真实 agent 实现和 provider；这由 A4 冻结。
4. 指标公式、阈值、统计协议；这由 A5 冻结。
5. 真实 LLM 调用；后续若调用必须 `source .env` 并保存 run record。
