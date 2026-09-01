# Paper predicate narrative alignment v5

这次复核只检查 paper1 对谓词体系的公开口径、数据单位和证据链接，不改变
method、Judge、raw 制品或任何语义裁定。

## Independent fact review

`subagent:paper_fact_audit` 逐项核对了 registry、v60 method summary、current v4
canonical decisions 和 fair-comparison summary。核对结果为：registry 为 19 个谓词，
四族数量为 Structure/Topology/Trajectory simulation/Bounded verification =
6/4/4/5；12 个 distinct ID 产生过 terminal receipt；8 个 distinct ID 至少绑定
到一条 report-bound finding。后两组 ID 与原始来源一致。

复核还确认 `825/1271` 是 report-bound binding rows，`303/825` 是旧
`coverage_class=semantic_hit` marker。它们是行级诊断，不能替代 12/19 或 8/19，
也不能解释成 W2、terminal-false 或“8 个谓词各自贡献了错误”。

## Shuorenhua pass

按 `$shuorenhua:shuorenhua` 的 docs/public-writing 规则回读了 README、STATUS、story、
evaluation README、正式 v4 报告、fair-comparison README/SCHEMA 和 facts ledger：

- 保留数字、版本、路径、ID、指标分母和责任主体；
- 将 distinct-ID 指标与 report-level 行指标直接分开；
- 将 expected-property/input gold 明确放在 evaluation-only 边界；
- 删除正式 paper-facing 报告中不必要的 assertion/oracle 理论展开；
- 只保留一句证伪导向的 simulation/BMC 使用解释，没有补充无来源的普遍性结论。

本记录证明的是文档和事实一致性，不能替代新的实验或人工语义重审。

## Final working-tree reread

按同一 `docs` 场景、`minimal` 强度和保真优先规则，复读了本轮定稿涉及的
README、STATUS、SUMMARY、story、正式报告、fair-comparison README/SCHEMA
和 evaluation README。将主文导航中的 `predicate gold` 改成“内部谓词后端审计”，
把比较层的 `expected-predicate coverage` 改成中性的 issue-level coverage wording，
并删除正式报告中会引出预设问题复现的句子。19/12/8、825/1271、303/825、W/D/K/N/I、
baseline N/A、路径和执行边界均保持不变。

最终保真回读确认：主文只把谓词写成文献来源的证据后端；没有引入 P/Q、oracle、
断言完备性或台账谓词预设。simulation/BMC 的低使用量只用“静态 sound witness
已经闭合时不强行升级，动态语义需要时再使用”解释。evaluation-only、raw 和 archive
中的详细属性/输入审计仍保留，且未被提升为方法输入或主结果。状态：PASS。

## Final working-tree supplement

随后又回读了 `discover_matrix/README.md`、`discover_matrix/ledger_v2/README.md`
和 `release/documentation_audit/current_facing_markdown_inventory.md`。这三份导航/审计
文档现在把 predicate gold 明确标为内部 evaluation-only 能力审计；它们仍保留 ledger、
provenance 和复算入口，不把属性映射写成 method 输入。此次补充没有改变 registry、
19/12/8、825/1271、303/825、W/D/K/N/I 或任何冻结制品。保真和边界检查：PASS。
