# 145 条台账 expected-predicate gold 审计报告

## 结论和发布边界

本轮对当前 `ledger_v2` 的 145 条 issue 逐条恢复规范义务 `O`，比较可执行性质 `P`，
并在执行前冻结 proposal 和 typed inputs。最终只有 13/145（8.97%）
满足 `O <=> P` 且通过坏制品 `false`、positive control `true` 和 replay match。另有
34 条只有 `O => P` 的可靠证伪 proxy；
98 条在现有 19 谓词、可审计组合性质和
pyfcstm-native evaluation-only oracle 下仍无法精准表达。`BLOCKED_EXECUTION=0`。

这组结果没有重跑或修改冻结 v60 method、Judge、15x1、54x3、raw、current/baseline canonical
decisions 或 19-predicate runtime。gold 只用于台账说明、离线 evaluation 和人工审计。

## 状态分布

| disposition | count | share of 145 |
| --- | ---: | ---: |
| `EXACT_FALSE` | 8 | 8/145 = 5.52% |
| `COMPOSITE_EXACT_FALSE` | 5 | 5/145 = 3.45% |
| `SOUND_FALSE_PROXY` | 34 | 34/145 = 23.45% |
| `UNSUPPORTED_EXACT` | 98 | 98/145 = 67.59% |
| `BLOCKED_EXECUTION` | 0 | 0/145 = 0.00% |

`EXACT_FALSE` 与 `COMPOSITE_EXACT_FALSE` 合计 13 条，是 exact executable coverage 的分子。
`SOUND_FALSE_PROXY` 和 `UNSUPPORTED_EXACT` 均不进入该分子。

### Family

| family | EXACT_FALSE | COMPOSITE_EXACT_FALSE | SOUND_FALSE_PROXY | UNSUPPORTED_EXACT | total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `EIS` | 5 | 1 | 24 | 60 | 90 |
| `INS` | 2 | 2 | 3 | 28 | 35 |
| `VU` | 0 | 0 | 4 | 8 | 12 |
| `DIFF` | 1 | 2 | 3 | 2 | 8 |

### D tier

| d_tier | EXACT_FALSE | COMPOSITE_EXACT_FALSE | SOUND_FALSE_PROXY | UNSUPPORTED_EXACT | total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `D2` | 6 | 5 | 27 | 60 | 98 |
| `D1` | 2 | 0 | 7 | 38 | 47 |

### L tier

| l_tier | EXACT_FALSE | COMPOSITE_EXACT_FALSE | SOUND_FALSE_PROXY | UNSUPPORTED_EXACT | total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `L2` | 0 | 0 | 10 | 29 | 39 |
| `L1` | 2 | 0 | 6 | 27 | 35 |
| `L0` | 6 | 5 | 18 | 42 | 71 |

## 执行和复核闭合

| check | result |
| --- | ---: |
| completed Boolean `false` | 47/47 |
| completed positive-control `true` | 47/47 |
| replay match | 47/47 |
| Track A obligation review | 145/145 |
| Track B property/input review | 145/145 |
| Track C execution/semantic review | 145/145 |
| independent fourth review | 145/145 |
| rows retaining disclosed conflicts | 131/145 |
| retained conflict records | 368 |
| `BLOCKED_EXECUTION` | 0 |

Track A/B/C 和 fourth review 是内部、hash-bound 的质量复核，不是正式人类 inter-rater study。
Pane5 依据作者 source、正式语义、query、receipt 和并列意见仲裁；多数票和 confidence 都不是
裁决规则。当前选择见 [`review/active_review_manifest.json`](review/active_review_manifest.json)。

早期 31 条 portable Track C packet 绑定历史协议 hash `3762ebf1...`，而同一路径当前保存的冻结
协议 hash 为 `6d91c5d8...`。历史字节已精确恢复并嵌入
[`review/evidence_corrections/protocol_hash_drift_resolution.json`](review/evidence_corrections/protocol_hash_drift_resolution.json)；
current-protocol fourth review 与 pane5 仲裁重新关闭了语义权限。历史 packet 的同路径 hash 不一致仍
作为 provenance limitation 保留，没有重写旧 packet，也没有把两版协议说成相同字节。

## 现有谓词和 evaluation-only 使用

下表是多标签 usage：一个 composite 可以同时使用多个 predicate，因此 exact 列不能横向求和后
当作 issue 数。`EVALUATION_ONLY` 是隔离在 evaluation package 内的 pyfcstm-native oracle，未加入
method registry。

| predicate/bucket | selected exact | selected proxy | unsupported bucket |
| --- | ---: | ---: | ---: |
| `EVALUATION_ONLY` | 8 | 21 | 0 |
| `G1` | 0 | 6 | 0 |
| `G2` | 0 | 0 | 0 |
| `G3` | 0 | 0 | 0 |
| `G4` | 0 | 0 | 0 |
| `R1` | 0 | 0 | 0 |
| `R2` | 0 | 0 | 0 |
| `R3` | 0 | 0 | 0 |
| `R4` | 0 | 0 | 0 |
| `S1` | 0 | 3 | 0 |
| `S2` | 0 | 1 | 0 |
| `S3` | 3 | 1 | 0 |
| `S4` | 2 | 2 | 0 |
| `S5` | 3 | 0 | 0 |
| `S6` | 0 | 0 | 0 |
| `UNSUPPORTED` | 0 | 0 | 98 |
| `V1` | 0 | 0 | 0 |
| `V2` | 0 | 0 | 0 |
| `V3` | 0 | 0 | 0 |
| `V4` | 0 | 0 | 0 |
| `V5` | 0 | 0 | 0 |

exact issue 中有 8 条使用 evaluation-only oracle。能力边界和
registry/backend 不一致见 [`predicate_semantics_capability_audit.md`](predicate_semantics_capability_audit.md)：
S2 只检查 direct authored carrier，G1 是 guard-agnostic macro topology；R1 的 registry `step`
不能独立选择 runtime observation；S6 runtime 只接受一个 effect；V1 还需要 registry 未声明的完整
guard multiset。gold protocol 将这些差异限制在 evaluation 层，冻结 runtime 保持不变。

## Unsupported

`UNSUPPORTED_EXACT=98` 不表示 issue 无效，也不表示
method 无法命中。它只说明目前没有 source-backed、obligation-equivalent、可执行且可重放的参考性质。
逐条 ID、capability gap、nearest proxy 和 arbitration 见
[`unsupported_exact.md`](unsupported_exact.md)；机器可读版本是
[`unsupported_exact.json`](unsupported_exact.json)。

主要限制来自 source 未给出完整 domain/bound/schedule/initial scope、义务量词或 timing 超出冻结
wrapper、whole-model termination/并发/RTC 语义无法从转换制品获得等价 attribution，以及 direct
carrier/topology/static slot 只能表达更强或更弱的邻近条件。没有为了减少 unsupported 数量而补造
变量、状态、事件、domain 或 bound。

## 冻结 v60 expected-vs-actual 离线分析

该分析只解释 method 的成分，不改写 FULL/PARTIAL hit、W 或 K/N/I。冻结 v60 对 145 个 issue 的
FULL hit 为 119/145，FULL 或 PARTIAL supported 为
128/145。98 个 unsupported gold 中仍有
82 个 FULL hit。因此，
unsupported 不能自动解释成 method miss。

| diagnostic classification | issues |
| --- | ---: |
| `ALTERNATE_PREDICATE_REQUIRES_SEMANTIC_REVIEW` | 2 |
| `EVALUATION_ONLY_GOLD_ACTUAL_REQUIRES_SEMANTIC_REVIEW` | 21 |
| `EXPECTED_ID_AND_INPUT_MATCH` | 1 |
| `EXPECTED_ID_INPUT_MISMATCH` | 7 |
| `EXPECTED_ID_INPUT_NOT_OBSERVABLE` | 4 |
| `NOT_HIT` | 26 |
| `NO_PREDICATE_ON_FULL_HIT` | 2 |
| `UNSUPPORTED_GOLD_BUT_FULL_HIT` | 82 |

其中 `EXPECTED_ID_INPUT_NOT_OBSERVABLE=4`；
冻结 raw 无法可靠恢复输入时，矩阵明确保留不可观察状态，没有猜值，也没有重跑 54x3。完整多标签
矩阵见 [`expected_vs_actual_v60.json`](expected_vs_actual_v60.json)。

## 学术依据和项目 operationalization

[`predicate_gold_protocol.md`](predicate_gold_protocol.md) 与
[`academic_claim_to_source_matrix.json`](academic_claim_to_source_matrix.json) 记录了 12 条经核验的
primary/formal source claim，覆盖 requirements pattern、FRET 字段化、oracle implication、vacuity、
有限测试边界、UML initial/RTC/completion、refinement、trace semantics、bounded model checking 和
spurious counterexample。独立学术复核结论为 `PASS_WITH_LIMITATIONS`，见
[`review/horizontal/academic_review_v2.md`](review/horizontal/academic_review_v2.md)。

`obligation-equivalent executable reference property`、四种 implication label、三 Track + pane5、
五种 disposition 和 positive-control/replay 合同是本项目综合文献形成的 operationalization。
文献不保证这套流程恢复 ground truth，也没有提出统一的“most precise predicate” family 排序；本项目
未声称测量了该 operationalization 的独立有效性。

## 复算和文件

| role | path |
| --- | --- |
| canonical annotations | [`predicate_gold_v1.json`](predicate_gold_v1.json) |
| schema / flat mirror | [`predicate_gold_v1.schema.json`](predicate_gold_v1.schema.json), [`predicate_gold_v1.tsv`](predicate_gold_v1.tsv) |
| mechanical summary | [`summary.json`](summary.json) |
| input inventory | [`inventory.json`](inventory.json) |
| receipts / controls | [`receipts/`](receipts/), [`controls/`](controls/) |
| reviews / arbitration | [`review/`](review/) |
| release manifest | [`manifest.json`](manifest.json) |

Provider-free validation and replay use the evaluation package only. The release manifest binds all selected
inputs, code, receipts, controls, reviews and derived views by repository-relative path and SHA-256.
