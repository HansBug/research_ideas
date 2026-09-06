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

本轮实现版本为 `semantic-judge.two-stage.v3.3`。issue #195 的 relation 与计分定义保持
不变；validity 按 issue #189 的义务口径作显式澄清：Judge 检查报告自己的核心技术主张与
不可缺少的因果机制是否成立，不要求报告或义务逐字复述 NL。隐式测试预言（尤其非预期
reachable deadlock / no-progress）和明确陈述的领域必备义务可以在 NL 未逐字写出时成立；
“NL 没写”本身不是反驳。具体且可审计的自由文本 W1 也不因缺少 W2 谓词证书而失去 VALID
或 FULL 的资格。反之，错误并发语义、虚构路径、错误 guard/event/effect/region 解释若是
核心主张成立所必需的机制，仍必须判 INVALID。

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

validity 必须先闭合 issue #189 的 D/A 语义。第一问是承重事实是否成立于作者源
work product，而不是当前 backend 能否执行：事实不成立，或只在 PlantUML→FCSTM
派生表示中成立而归错制品，属于 A0；事实成立后才问是否存在存活的被违反义务，存在则为
D2/D1，不存在则为 D0。A0 分为 `FALSE_POSITIVE` 与 `NOT_A_DEFECT_CLAIM` 两类；后者
专指本方法 PlantUML→FCSTM 分析/表示链的错误归因（包括 unresolved/deferred analysis
status 或只在派生 IR 上成立的现象），X1v2 baseline 不经该链，故没有这一
subtype。不设 `OUT_OF_SCOPE`。当前谓词或 backend 不支持只影响 W，不得把 D2/D1 改判 I。

| D/A 结果 | relation closure | K/N/I |
| :-- | :-- | :-- |
| `D2` / `D1` | 至少一个 `FULL_MATCH` / `PARTIAL_MATCH` | `VALID_KNOWN` (K) |
| `D2` / `D1` | 全部 `NO_MATCH` | `VALID_NOVEL` (N) |
| `D0` / `FALSE_POSITIVE` / `NOT_A_DEFECT_CLAIM` | 只允许全部 `NO_MATCH` | `INVALID` (I) |

因此 D0 与 A0 都不能因 ledger-unmatched 进入 N；二者的区别保留在逐条 reason/basis
审计中。该闭合引用 [issue #189](https://github.com/HansBug/research_ideas/issues/189)
的 D/A 定义，并与 [issue #195](https://github.com/HansBug/research_ideas/issues/195)
§1、§3、§4 的 K/N/I 定义共同构成现行协议。

## 人工监督发布层（current v2 + baseline v3）

论文主结果不把 Judge 输出改名为人工真值。current/v60 的发布层位于
[`manual_adjudication_v2`](../../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/README.md)。
X1v2 baseline 非 K 的版本化重审层位于
[`manual_adjudication_v3_baseline_ni`](../../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/README.md)。
每条当前发布 report/finding 都由用户授权的 pane5 主 session 逐条读取冻结 raw、作者
NL/PlantUML 和必要的 ledger/artifact evidence 后确认，subagent/LLM 仅提交 raw-first
proposal。两个层的 canonical JSON 都逐条保存 reason、basis、source refs、审阅链和
human-supervised attestation；TSV 只是镜像。

current v2 与 baseline v3 都沿用本文件的 issue #195 relation 语义，但使用 issue #189 的事实优先 D/A 闭合：
`D2/D1 + FULL/PARTIAL -> VALID_KNOWN -> K`，`D2/D1 + all NO_MATCH -> VALID_NOVEL -> N`，
`D0/A0 -> INVALID -> I` 且强制全 `NO_MATCH`。`PARTIAL` 不计主 hit 或 FP，W 不参与
validity/relation/hit/FP，最终不接受 `UNKNOWN`、`PENDING_REVIEW` 或 `OUT_OF_SCOPE`。
v60/current 与 X1v2 的主数字、N/I pair-local groups、W、predicate audit 和成本只能从
各自版本化目录的 JSON 及其 provider-free recompute 得到；本文件前述 v3.3 运行协议和旧
headline 仍作为历史 Judge 工具协议，不作为新的人工真值来源。

### 双侧 reviewer 输入映射

raw-first reviewer 只接收 `reviewer_input_projection.jsonl` 的共同 allowlist；`arm-a` 与
`arm-b` 在解盲前不映射到语义侧名。字段映射固定如下：

| 统一投影字段 | v60/current 冻结 raw | X1v2 baseline 冻结 raw | 用途 |
| :-- | :-- | :-- | :-- |
| `round`, `pair_token`, `slot` | `/round` 与 inventory 的 pair/record 顺序 | `/round` 与 inventory 的 pair/record 顺序 | 解盲前稳定位置；每个 pair/round 两臂使用同一 slot 宇宙 |
| `report_evidence.claim_text` | 归一化的 report claim prose | 归一化的 finding claim prose | 原始主张；不携带 producer schema、ID 或 pointer |
| `report_evidence.reason_text` | 归一化的 report reason prose | 归一化的 finding reason prose | finding 理由；不作自动标签 |
| `report_evidence.location_text` | 固定空字符串 | 固定空字符串 | 保持统一形状；producer-specific locus 仅在解盲后供主 session 回读 |
| `author_source.nl` | `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_<pair>/nl.txt` | `reference/x1v2_input_closure/pairs/<pair>/nl.txt` | 作者需求 |
| `author_source.plantuml` | `reference/x1v2_input_closure/pairs/llms_emp_feedback_final_<pair>/plantuml.puml` | `reference/x1v2_input_closure/pairs/<pair>/plantuml.puml` | 作者模型 |
| `author_source` hashes | 作者源 bytes | 作者源 bytes | raw-first 可见的作者源闭合；两臂同 slot 必须完全相同 |

`expected ledger`、旧 Judge 标签、predicate/receipt、W、D/A、validity、relation 和 K/N/I
均不在该 raw-first 投影中；`report_index`、raw JSON Pointer、raw target hash、`element_refs`
和 baseline `where` 也只留在 inventory/canonical 审计或 sealed
`reviewer_unblind_mapping.json` 中，不进入盲审输入。它们只能在独立 proposal 提交后、主
session 完成证据核对时进入解盲/仲裁与确定性派生。padding 不是 finding，也不进入任何分母或
semantic label；它只防止缺少某个 pair/round 行成为臂别线索。该映射与 [manual adjudication v2 schema](../../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/schema.md)
共同约束最终审计数据。

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
此外必须分别报告 raw-report Semantic Precision、N substantive root-cause grouping 的诊断
统计和 redundancy rate；I 不建立 substantive grouped precision。重复的 valid finding 进入
redundancy，不进入 FP。

论文主 precision 固定使用 raw-report 单位：

```text
report-based precision = (VALID_KNOWN reports + VALID_NOVEL reports) / all final reports
report-based FP rate = INVALID reports / all final reports
```

I 不适用 substantive grouped precision。`INVALID` 表示没有可接受的缺陷实体：D0 是事实
成立但不存在被违反的存活义务，A0 是事实不成立或归因到错误制品；两类记录没有可稳定
共享的 normative obligation、source locus、root cause 或 repair intent。I cluster 可以
作为附录诊断或敏感性分析，但不得被写成独立缺陷，也不得与 K ledger ID 和 N root-cause
group 混成论文主 precision 分母。N 的 group 归并是本项目在文献启发下的
operationalization，不应伪称为任一单篇论文的原定义。

台账应在论文中称为 `expert-annotated expected issue ledger` 或
`manually curated source-backed issue inventory`。它用于 known-issue coverage 的参照，
不宣称穷尽未知缺陷空间；K 以 ledger expected ID 去重，N 才按同一 side、同一 pair、同一
实质义务/source locus/root cause/property/最小修复意图归并，允许跨 round，不跨 pair。

## 条款追踪矩阵

| #195 合同 | Schema / prompt | 确定性代码 | Provider-free 测试 | 文档落点 |
| :-- | :-- | :-- | :-- | :-- |
| issue snapshot 是唯一权威，变更即升版并使旧分数失效 | `protocol.py` 的 `PROTOCOL_*` 与 `verify_snapshot` | CLI 在运行前校验 snapshot | snapshot hash、prompt hash 测试 | 本文件“冻结版本” |
| D2+D1 是唯一发布集合；D0 不进入 Judge | arm-neutral `CandidateReport` 不含 D/W/L | `artifacts.py` 只适配最终发布报告 | adapter 字段结构与排除字段测试 | `final_output_metrics_policy.md` |
| 先判核心真值，再判 relation，后端派生 K/N/I | `ValidityJudgeInput` 物理不含 expected；`RelationJudgeInput` 只接受冻结 VALID certificate | `materialize_validity_certificate`、`materialize_two_stage_reading` | expected isolation、clause closure、two-stage replay 测试 | 本文件“现行核心合同” |
| validity 只硬门核心主张、必要机制与最低举证责任 | 每条完整命题标记 `CORE_CLAIM / INDISPENSABLE_MECHANISM / AUXILIARY_CONTEXT`；minimum-evidence gate 同时要求作者源事实成立与存活的被违反义务 | 后端从 clause 派生 core/mechanism gate，再由三门机械派生真值；D0/A0 的 minimum-evidence 为 REFUTED，refuted auxiliary 只进入 warning | auxiliary-error、false-mechanism、D0/A0、unsupported-backend 非 validity gate 测试 | issue #189 与本文件“公平性与规模合同” |
| INVALID、VALID_NOVEL 全 NO；VALID_KNOWN 至少一条 FULL/PARTIAL | INVALID 不进入 relation schema；relation 动态 exact closure | `judge_pair` 的 invalid all-NO closure、`ReportAssessment` validator | 非法组合、invalid-no-relation 测试 | snapshot §1.1 |
| FULL 采用适度宽语义，不以字段复刻为 gate | `RELATION_SYSTEM_PROMPT` 的 root cause、obligation、symptom、repair overlap 规则 | relation enum 原样物化 | free-text FULL、多 expected FULL 测试 | `hit_criterion.md` |
| PARTIAL 只算 supported，不算 hit/FP | `PositiveMatchStrength.PARTIAL_MATCH` | `metrics.py::compute_semantic_metrics` | partial 指标测试 | 本文件“确定性指标” |
| Novel 需要独立真实性证据，不能由 unmatched 自动推出 | expected-isolated `FrozenValidityCertificate` | VALID + relation 全 NO 才派生 `VALID_NOVEL` | concise valid-novel 与 invalid 对照测试 | `ground_truth_limitations.md` |
| 只有 INVALID 是 Semantic FP | `ReportValidity.INVALID` 仅后端派生 | deterministic metrics / aggregate | invalid-only FP、duplicate-valid 测试 | `final_output_metrics_policy.md` §5 |
| 无最终 UNKNOWN；两阶段各双独立 reading，冲突定向仲裁 | validity/relation primary 与 arbitration Pydantic schema | `runner.py::judge_pair` 分阶段 merge 后完整重验 | validity/relation arbitration、failure 测试 | `verdict_methodology.md` |
| 每条 relation、validity、顶层结果有 reason/basis/source refs | 固定 field/clause truth audit 与 expected-specific relation evidence | `FrozenFieldValidityAudit` 与 `FrozenValidityCertificate` 由后端物化 exact text/hash | claim/clause omission、fixed slot、exact materialization 测试 | 本文件与 run record |
| 同一 expected 多报告只命中一次；一报告可 FULL 多 expected | 每个 report 的 positional relation decisions | expected-side unique 聚合 | 三 expected FULL、duplicate-valid 测试 | `hit_criterion.md` |
| W/D/L、谓词族、arm、历史结果不作 gate | `UnifiedJudgeInput` 不含这些字段 | 两臂共用 artifacts/runner/metrics | adapter diff、prompt leakage 测试 | 本文件“公平性合同” |
| 公共 artifact closure 对两臂相同 | `JudgeArtifactClosure` | `build_artifact_closure` 单入口 | closure identity 与完整角色测试 | 本文件“公平性合同” |
| 矛盾 deterministic facts 不得进入 provider | `ArtifactConsistencyPreflight` | provider 前交叉检查 FCSTM graph、owned inspection、verify 与 reference unreachable diagnostics | 0053 reachability 与 contradiction-block 测试 | 本文件“公平性合同” |
| 稀疏证据输出必须显式闭合全部 NO | 固定位置 `relation_decisions`，NO 仅保留 ID/enum | provider-native positional schema、dense audit materializer | 0029 shape 与真实规模审计 | 本文件“规模合同” |
| Judge 失败不产生分数且费用不消失 | failure Pydantic records、call receipts | CLI failure summary、normalized usage | failed-call cost/cache 测试 | `final_output_metrics_policy.md` §4/§8 |

## 公平性与规模合同

X1v2 与 evidence-discovery 仅在 source adapter 内读取各自报告结构；adapter 结束后，两臂
进入完全相同的 `UnifiedJudgeInput`、两阶段动态 Pydantic schema、英文 prompt、公共 artifact
closure、`gpt-5.6-luna` profile、双读、retry、仲裁和指标入口。provider 看不到 arm 名、
原始 ID、D/W/L、谓词、历史得分或旧判决。相同 pair 的公共闭包由一个 builder 构建，
顺序、内容、provenance 与 hash 不因 arm 改变。

每条报告先单独进入 `ValidityJudgeInput`。该 Pydantic 类型只含当前匿名 report、固定
`ReportCoreEnvelope` 与公共 artifact closure，物理上没有 expected/ledger 字段。两个独立
validity reading 与必要的 validity-only 仲裁完成后，后端冻结
`FrozenValidityCertificate`。后端对每个非空字段保留完整、gap-free 的 source-clause audit，
但不再把所有字段作全称合取。每条完整语义命题由 Judge 标记为 `CORE_CLAIM`、
`INDISPENSABLE_MECHANISM` 或 `AUXILIARY_CONTEXT`；核心主张、必要机制、最低举证责任三个
hard gate 全部满足时才是 VALID。被反驳的核心主张或必要机制使报告 INVALID；被反驳的
附带措辞保留为 `auxiliary_warnings`，不能单独杀死成立的核心主张。`basis` 只作支撑审计，
`where` 只作 locus，均不能替换或救活错误核心机制。
INVALID 不调用 relation LLM，后端直接为全部 expected 物化 `NO_MATCH`。只有冻结为 VALID
的报告才进入 `RelationJudgeInput`；它看到 immutable certificate/hash、expected 和同一公共
闭包，只能输出 FULL/PARTIAL/NO，不能重开 validity。

production prompt 的 typed-carrier 规则来自 PlantUML 状态图语法与层次状态机作用域，而非
固定 pair 答案：并发/正交 region 必须由同一 composite 内的显式 region separator 建立；
sibling composite declaration、名称中的 `region` 和 child-local initial transition 均不能
替代该 carrier。child-local entry 只证明 child 内部入口，不证明 parent-level entry，也不
证明 siblings 同时激活。relation 对 composite expected 逐项读取其明确写出的独立可行动
facet：报告准确陈述其中一个核心 facet 且修复会实质缓解时即可 FULL，不要求覆盖其它并列
facet；反向边界同样严格，公共 artifacts 中另一个真实 defect 不能扩写报告自己的
claim/scope/carrier/repair obligation。上述规则不含 benchmark ID、状态名或预设映射，且
必须由 provider-free replay 与 held-out calibration 共同验证。

规模协议只压缩重复表示，不裁剪 Judge 证据：relation 动态 Pydantic schema 为每个 expected
建立固定位置的 discriminated `relation_decision`；FULL/PARTIAL/NO 每一行均保存
expected-specific reason/basis/source refs，FULL/PARTIAL 另存 report-owned field refs。
NO 不再依赖另一个条件式 closure 字段，避免 relation partition 与 evidence 字段形成模型难以
一次闭合的跨字段条件。`prefixItems + minItems + maxItems` 在 provider schema 层保证每个
expected 恰好出现一次，再由后端物化完整 dense audit。validity schema 不让 provider
自由选择 `report_field`，而是按实际输入动态生成 `claim_audit`、`reason_audit` 等固定顶层槽；
每个字段中的完整语义命题按原文顺序进入不可遗漏的 clause row；每行给出 role、
`SUPPORTED/REFUTED`、reason、basis 和 source refs。完整字段原文与 SHA-256 由后端从不可变
输入确定性物化，既不允许摘取方便子句、用邻近真事实替换错误机制，也不要求模型复制长文本。
分句只使用句号、分号、换行等完整命题边界，不再按 64 字符硬切；offset/hash closure 仍必须
gap-free。模型不自报 aggregate core truth，后端从三个 hard gate 确定性派生。两个 validity
primary 都完全看不到 expected；两个 relation primary 只对 VALID
报告运行。真正冲突的 report 在对应隔离阶段逐条 atomic 仲裁；未冲突结果原样复用，全部
replacement 合并后重验 pair closure。真实 `0029` provider-free scale audit 必须从本轮选定
raw report artifact 实测 report / expected / clause 数，并按“所有报告均 VALID”的最坏四次
primary call / report 证明每个 validity/relation target 的 prompt、schema、带逐 expected
证据的 all-NO/all-FULL envelope 在 profile context/output
上限内闭合。该 audit 必须在任何 method 六 pair 或 baseline 全量重判之前通过；live smoke
失败不得当作 miss 或从分母排除。

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
