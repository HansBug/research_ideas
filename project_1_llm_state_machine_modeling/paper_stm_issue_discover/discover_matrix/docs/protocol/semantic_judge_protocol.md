# 统一语义 Judge 协议入口

本目录中的 [semantic_judge_issue_195.snapshot.md](./semantic_judge_issue_195.snapshot.md) 是 GitHub issue [#195](https://github.com/HansBug/research_ideas/issues/195) 正文的逐字快照。GitHub issue 是唯一现行权威；本文件只提供版本、完整性校验和仓库内导航，不建立另一套 Judge 定义。

## 冻结版本

- 抓取时间（UTC）：`2026-08-23T10:30:00+00:00`
- issue 创建时间：`2026-08-23T03:57:22Z`
- issue 最后更新时间：`2026-08-23T10:27:51Z`
- issue 状态：`OPEN`
- 正文大小：`24,548 bytes`
- 正文 SHA-256：`d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`
- 快照校验范围：仅 Markdown 正文原始 UTF-8 bytes，不包含本导航文件。

若 issue #195 的 `updatedAt` 或正文 hash 变化，必须新建 protocol version、重新执行条款追踪审计，并使旧 Judge 结果失去与新结果直接比较的资格。不得静默覆盖快照后继续使用旧分数。

## 现行核心合同

- 维度 A：`FULL_MATCH / PARTIAL_MATCH / NO_MATCH`。
- 维度 B：`VALID_KNOWN / VALID_NOVEL / INVALID`。
- `FULL_MATCH/PARTIAL_MATCH + INVALID` 与 `FULL_MATCH/PARTIAL_MATCH + VALID_NOVEL` 均为非法组合；`VALID_KNOWN` 必须至少有一个正向 relation。
- 只有 `VALID_KNOWN + FULL_MATCH` 贡献主 hit。
- `PARTIAL_MATCH` 只贡献 Supported Rate，不算主 hit，也不算 FP。
- 只有 `INVALID` 是 Semantic FP；ledger-unmatched 只是兼容诊断。
- 最终统计不得保留 `UNKNOWN` 或 `PENDING_REVIEW`。

报告级闭合顺序固定为：先判核心主张 `VALID / INVALID`；`INVALID` 的全部 relation
必须为 `NO_MATCH`；有效报告再逐 expected 裁定 relation；最后由后端从核心真值和
relation closure 派生 `VALID_KNOWN / VALID_NOVEL / INVALID`。provider 不输出最终
K/N/I，也不输出 hit、FP、precision 或 expected-side 汇总。

## 确定性指标

```text
hit(e) = 存在 VALID_KNOWN report r 且 match(r,e)=FULL_MATCH
Hit Rate = unique FULL-hit expected / expected 总数
FN = expected 总数 - unique FULL-hit expected
Supported Rate = 被 FULL 或 PARTIAL 覆盖的 unique expected / expected 总数
Semantic FP = INVALID 发布报告数
Semantic Precision = (VALID_KNOWN + VALID_NOVEL) / 全部已裁定发布报告
Ledger-Unmatched = 只有 PARTIAL 的 VALID_KNOWN + VALID_NOVEL + INVALID
```

`Ledger-Unmatched` 仅是兼容旧 closed-ledger 报告的诊断项，禁止再命名为 Semantic FP。
此外必须分别报告 raw-report Semantic Precision、root-cause-cluster precision 和
redundancy rate；重复的 valid finding 进入 redundancy，不进入 FP。

## 条款追踪矩阵

| #195 合同 | Schema / prompt | 确定性代码 | Provider-free 测试 | 文档落点 |
| :-- | :-- | :-- | :-- | :-- |
| issue snapshot 是唯一权威，变更即升版并使旧分数失效 | `protocol.py` 的 `PROTOCOL_*` 与 `verify_snapshot` | CLI 在运行前校验 snapshot | snapshot hash、prompt hash 测试 | 本文件“冻结版本” |
| D2+D1 是唯一发布集合；D0 不进入 Judge | arm-neutral `CandidateReport` 不含 D/W/L | `artifacts.py` 只适配最终发布报告 | adapter 字段结构与排除字段测试 | `final_output_metrics_policy.md` |
| 先判核心真值，再判 relation，后端派生 K/N/I | provider 输出 assertion truth、certificate selector 与 `PositiveMatchStrength`，不重复 aggregate core truth | `derive_causal_field_verdict`、`schema.py::materialize_reading` | 3x3 合法组合、全局 closure、core-truth derivation 测试 | 本文件“现行核心合同” |
| INVALID、VALID_NOVEL 全 NO；VALID_KNOWN 至少一条 FULL/PARTIAL | 动态 exact-closure schema 与 validator | `_validate_report_judgment`、`ReportAssessment` validator | 非法组合确定性拒绝测试 | snapshot §1.1 |
| FULL 采用适度宽语义，不以字段复刻为 gate | `SYSTEM_PROMPT` 的 root cause、obligation、symptom、repair overlap 规则 | relation enum 原样物化 | free-text FULL、多 expected FULL 测试 | `hit_criterion.md` |
| PARTIAL 只算 supported，不算 hit/FP | `PositiveMatchStrength.PARTIAL_MATCH` | `metrics.py::compute_semantic_metrics` | partial 指标测试 | 本文件“确定性指标” |
| Novel 需要独立真实性证据，不能由 unmatched 自动推出 | causal certificate 与 `core_truth=VALID` | VALID + all NO 才派生 `VALID_NOVEL` | valid-novel 与 invalid 对照测试 | `ground_truth_limitations.md` |
| 只有 INVALID 是 Semantic FP | `ReportValidity.INVALID` 仅后端派生 | deterministic metrics / aggregate | invalid-only FP、duplicate-valid 测试 | `final_output_metrics_policy.md` §5 |
| 无最终 UNKNOWN；双独立 reading，冲突定向仲裁 | primary/arbitration Pydantic schema | `runner.py::judge_pair`、targeted merge 后完整重验 | primary、arbitration、failure 测试 | `verdict_methodology.md` |
| 每条 relation、validity、顶层结果有 reason/basis/source refs | provider 输出字段引用与逐 material assertion 的 truth audit | `derive_causal_field_verdict` 派生 field verdict；`ReportCausalFieldAudit` 的 exact text/hash 由后端物化 | 空字段、错引用、assertion closure、whole-field derivation 与 exact materialization 测试 | 本文件与 run record |
| 同一 expected 多报告只命中一次；一报告可 FULL 多 expected | 每个 report 的 positional relation decisions | expected-side unique 聚合 | 三 expected FULL、duplicate-valid 测试 | `hit_criterion.md` |
| W/D/L、谓词族、arm、历史结果不作 gate | `UnifiedJudgeInput` 不含这些字段 | 两臂共用 artifacts/runner/metrics | adapter diff、prompt leakage 测试 | 本文件“公平性合同” |
| 公共 artifact closure 对两臂相同 | `JudgeArtifactClosure` | `build_artifact_closure` 单入口 | closure identity 与完整角色测试 | 本文件“公平性合同” |
| 稀疏证据输出必须显式闭合全部 NO | 固定位置 `relation_decisions`，NO 仅保留 ID/enum | provider-native positional schema、dense audit materializer | 0029 shape 与真实规模审计 | 本文件“规模合同” |
| Judge 失败不产生分数且费用不消失 | failure Pydantic records、call receipts | CLI failure summary、normalized usage | failed-call cost/cache 测试 | `final_output_metrics_policy.md` §4/§8 |

## 公平性与规模合同

X1v2 与 evidence-discovery 仅在 source adapter 内读取各自报告结构；adapter 结束后，两臂
进入完全相同的 `UnifiedJudgeInput`、动态 Pydantic schema、英文 prompt、公共 artifact
closure、`gpt-5.6-luna` profile、双读、retry、仲裁和指标入口。provider 看不到 arm 名、
原始 ID、D/W/L、谓词、历史得分或旧判决。相同 pair 的公共闭包由一个 builder 构建，
顺序、内容、provenance 与 hash 不因 arm 改变。

规模协议只压缩重复表示，不裁剪 Judge 证据：动态 Pydantic schema 为每个 expected
建立固定位置的 discriminated `relation_decision`；FULL/PARTIAL 行保存 expected-specific
reason/basis/source refs，NO 行显式保存 expected ID 与 `NO_MATCH`，共同的 NO 证据只在
report 级保存一次。`prefixItems + minItems + maxItems` 在 provider schema 层保证每个
expected 恰好出现一次，再由后端物化完整 dense audit。whole-field causal audit 同样只让
provider 选择 `report_field`，并把字段中每个 material factual assertion、modeling-semantic
assumption 和 causal link 按原文顺序拆成独立 assertion row；每行给出
`SUPPORTED/REFUTED`、reason、basis 和 source refs。模型不自报 whole-field verdict 或
aggregate core truth，后端按
“全 SUPPORTED = SUPPORTED、全 REFUTED = REFUTED、混合 = MIXED”机械派生。完整字段原文与
SHA-256 也由后端从不可变输入确定性物化，既不允许摘取方便子句、用邻近真事实替换错误机制，
也不要求模型复制长文本。仲裁仅重写冲突 report，
未冲突报告复用已验证 primary，合并后重新执行全 closure validator。真实 `0029`
provider-free scale audit 按真实 causal-field 长度每 64 字符至少预留一条 material assertion，
同时验证 all-NO 与 all-positive envelope；只有在 profile 声明的输出上限和完整 context
reserve 内均闭合才通过。该 audit 必须在任何 method 六 pair 或 baseline 全量重判之前通过；
live smoke 失败时转入原子裁定，而不是把失败当 miss。

## 学术边界

本项目 operationalization 综合 MCeT 的 same-root-cause equivalence、NIST SATE 的
direct/indirect finding 区分、Pearson 的 best-case fault localization、APR 的 semantic
与 repair equivalence、Porter 的 known-fault detection，以及 Klees 的 distinct-bug
deduplication。它不是任何单篇文献逐字提出的标准。尤其 SATE 的 exact closed-world
统计不能直接迁移到台账不完备的生产制品；APR 的补丁等价也不自动证明两份缺陷报告
同义。完整引用、适用范围和限制以 issue #195 snapshot 的文献部分为准。

历史 exact-field、W2 gate、partial=FP 或 unmatched=FP 结果只能标记为 legacy protocol。
固定 pair 的人工答案仅用于外部 calibration，不得写入 production prompt、schema
description 或代码分支。
