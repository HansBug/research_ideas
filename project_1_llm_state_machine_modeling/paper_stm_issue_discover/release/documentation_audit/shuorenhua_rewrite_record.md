# shuorenhua 文档改写记录

场景为 docs + README，无源判断采用 audit-only。受保护片段清单见 [facts ledger](./facts_ledger.md)。

## Pass 1：保真回读

- 核对所有 current headline 的版本、commit、run ID、hash、分母、指标和路径均可回指 facts ledger。
- 保留 FULL/PARTIAL/NONE、VALID_KNOWN/VALID_NOVEL/INVALID、W、D、L、issue #189、issue #195、CLI、资源名和 protocol 名称。
- 删除了以 v27/v46/旧 Judge 作为当前结果来源的导航；历史数字只留在明确的 historical/provenance 材料中。
- 未改变任何 prompt、schema、registry、raw/derived JSON 或冻结实验报告的数据语义。

## Pass 2：文风回读

- 删除入口页的施工提示、过多图标、模板式总结和已失效的迁移叙事。
- README 第一屏先说明项目、读者和问题；技术说明保留条件、命令、边界和责任主体。
- 术语稳定使用“方法”“Judge”“evaluation”“最终归档”“历史归档”，不为避免重复更换术语。
- 未为自然表达补造数字、能力、来源、因果或新颖性结论。

## 最终回读与复核

- Pass 1 再次逐项核对 protected spans：版本、commit、run ID、hash、路径、命令、issue 编号、指标及分母均保持 facts ledger 中的事实关系；未更改 frozen raw/derived/reference 数据。
- Pass 2 只收束 README 与导航中的施工口吻、旧入口和重复说明，保留 method、Judge、evaluation、W/D/L、FULL/PARTIAL/NONE 与 validity 术语的正式含义。
- 全项目 Markdown 相对链接检查为 `0` 条失效；历史关键词逐文件审计以最终工作树机械枚举，`176/176` 条目均带职责分类。
- authoritative final archive validator、release structure validator 与 raw/derived/reference 基线对拍均在本轮文档改写后通过；provider 和 billable 调用均为 `0`。
- 四类独立 reviewer 的首轮 finding 与 targeted rereview disposition 见 [review_disposition.md](./review_disposition.md) 和 [reviews/](./reviews/)。
