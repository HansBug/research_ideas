# 统一语义 Judge 协议入口

本目录中的 [semantic_judge_issue_195.snapshot.md](./semantic_judge_issue_195.snapshot.md) 是 GitHub issue [#195](https://github.com/HansBug/research_ideas/issues/195) 正文的逐字快照。GitHub issue 是唯一现行权威；本文件只提供版本、完整性校验和仓库内导航，不建立另一套 Judge 定义。

## 冻结版本

- 抓取时间（UTC）：`2026-08-23T06:08:08+00:00`
- issue 创建时间：`2026-08-23T03:57:22Z`
- issue 最后更新时间：`2026-08-23T04:05:33Z`
- issue 状态：`OPEN`
- 正文大小：`21,806 bytes`
- 正文 SHA-256：`45874c298781e23b712d9566e75719b1fede0197c1f668030911c77f8f86574c`
- 快照校验范围：仅 Markdown 正文原始 UTF-8 bytes，不包含本导航文件。

若 issue #195 的 `updatedAt` 或正文 hash 变化，必须新建 protocol version、重新执行条款追踪审计，并使旧 Judge 结果失去与新结果直接比较的资格。不得静默覆盖快照后继续使用旧分数。

## 现行核心合同

- 维度 A：`FULL_MATCH / PARTIAL_MATCH / NO_MATCH`。
- 维度 B：`VALID_KNOWN / VALID_NOVEL / INVALID`。
- 只有 `VALID_KNOWN + FULL_MATCH` 贡献主 hit。
- `PARTIAL_MATCH` 只贡献 Supported Rate，不算主 hit，也不算 FP。
- 只有 `INVALID` 是 Semantic FP；ledger-unmatched 只是兼容诊断。
- 最终统计不得保留 `UNKNOWN` 或 `PENDING_REVIEW`。

条款到 schema、prompt、代码、测试和文档的落地证据维护在后续同目录追踪矩阵中。历史 exact-field 或 unmatched=FP 结果只能标记为 legacy protocol。
