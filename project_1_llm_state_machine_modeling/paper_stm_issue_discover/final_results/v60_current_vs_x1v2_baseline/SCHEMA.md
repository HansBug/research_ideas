# Final Results Schema

current/v60 的当前 headline 来自 `derived/manual_adjudication_v4_current_reaudit/`；X1v2
baseline 非 K 的当前发布结果来自 `derived/manual_adjudication_v3_baseline_ni/`。两层共同支撑当前并列报告；旧
旧人工裁定记录、旧 witness audit、旧 reviews 只由 archive/provenance 入口保留，不是当前人工真值。
冻结 raw、reference ledger、method 输入和 predicate registry 不由本次重评修改。

论文真值中，current/v60 来自本目录 v4 对既有 pane5 source-first 确认的逐条
raw/source/hash/relation 再验证和确定性派生；v2 仅是该审计链的 provenance。baseline v3 只写入非 K 重审层，原 K
不被再次语义修改。

## v4 current re-audit layer

`derived/manual_adjudication_v4_current_reaudit/` 保存 current 全部 1271 条报告的
Pydantic-validated canonical decision、145 条 expected 的 dense relation、N substantive
groups、I diagnostic composition、review/arbitration log、summary 和 manifest。v4 不改变
v2 的语义裁定；它重新从 raw/source/hash 闭合既有 pane5 source-first 证据，并将 v4 结果作为
公平比较 headline。current v2 目录仍完整保留，只作为历史输入与 provenance。

v4 的每条 decision 还必须满足：D2/D1 的 source fact 与 normative duty 均为
`ESTABLISHED`；D0 的 source fact 为 `ESTABLISHED`、义务为 `NOT_ESTABLISHED`；A0 的
source fact 为 `REFUTED`、义务为 `NOT_ESTABLISHED`。D0/A0 均为 I，且 145 条正式 relation
全部为 `NO_MATCH`。这组字段闭合由
[`build_current_reaudit_v4.py`](../../scripts/evaluation/build_current_reaudit_v4.py) 的
Pydantic model validator 和 fair-comparison validator 同时检查。

## v3 baseline non-K layer

`baseline_report_decisions_v3.json` 保存 233 条原非 K report 的 Pydantic-validated final
decision，`baseline_report_decisions_v3.tsv` 是固定列镜像，`baseline_relation_decisions_v3.json`
是每条 report 对全部 145 expected 的 dense relation。每条保存 raw pointer/hash、完整原文、
作者 NL/PlantUML source refs、事实/D/A、validity、K/N/I、W、迁移和 report-specific
reason/basis。`ReviewChain` 保存两份 blind `subagent:` proposal、disagreement、pane5
arbitration、`reviews/arbitration_log_v3.json` 的逐条 pointer、human confirmation 和 session
reference；proposal 不能冒充人工真值。

`frozen_k_snapshot_v3.json` 是原有 279 K 的精确 v2 projection，`baseline_combined_512_v3.json`
只把该 projection 与 233 条 v3 decision 组合。v3 不修改 current/v60、method、人工裁定、predicate、
prompt、raw 或既有 v2 目录。

## 输入闭包

`inventory.json` 从 raw 重新枚举 `162` 个 v60/current cells、`162` 个 X1v2 cells、
`1271` 条 current report 和 `512` 条 baseline finding，并保存每条的 side、pair、round、
report index、raw repository-relative path、JSON Pointer 和 SHA-256。`pane5_evidence_reads.json`
再逐条闭合 raw target、作者 NL、PlantUML、145 条 ledger digest 和 source hash。
current v4 的输入闭包另见 `derived/manual_adjudication_v4_current_reaudit/inventory_v4.json`；
公平比较总索引见 `derived/fair_comparison_v4/combined_report_index_v4.json`。

## ReportDecision

`derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json` 与
`derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json` 是两侧
Pydantic canonical JSON；各自 TSV 是固定列、逐字段相同的镜像。每条决策至少保存：

- `side`, `pair_id`, `round`, `report_id`, `report_index`；
- raw method record path、report JSON Pointer、claim/where pointer 和 SHA-256；
- `fact_status`, `strict_da`, `a0_type`, `validity`, `corrected_kni`；
- 145 个 expected 的 `FULL_MATCH`, `PARTIAL_MATCH` 或 `NO_MATCH` relation，每行有专属
  reason、basis、source refs 和 report-owned field refs；
- `witness.level`、具体定位，及 W2 所需的 executable object、typed input、terminal receipt、
  artifact hash 和 terminal result；
- 专属 `reason`, `basis`, `source_refs`；
- primary/independent/final reviewer IDs、blind event、分歧/仲裁、授权 attestation、
  `human_confirmation`、`human_supervised_session` 和 `review_blockers`。

所有正式 model class 位于
`evaluation/src/paper_stm_evaluation/manual_adjudication.py`，每个 class 有 docstring，
字段使用带 description 的 Pydantic `Field`。`review_status` 只有 `PROPOSAL`,
`INDEPENDENT_REVIEW`, `ARBITRATED`, `FINAL`；FINAL 不能保留 blocker。最终数据不接受
`UNKNOWN`, `PENDING_REVIEW` 或 `OUT_OF_SCOPE`。

## 确定性闭合

先判断作者源事实，再判断义务：事实成立且义务明确为 D2，事实成立但有两种具体存活读法
为 D1，事实成立但没有违反义务或设计正当为 D0，事实不成立/归错制品/方法表示债务为 A0。
A0 只允许 `FALSE_POSITIVE` 与 current-only `NOT_A_DEFECT_CLAIM`。

| D/A | relation | validity | K/N/I |
| --- | --- | --- | --- |
| D2/D1，且人工确认有效 | 至少一个 FULL 或 PARTIAL | VALID_KNOWN | K |
| D2/D1，且人工确认有效 | 全部 NO_MATCH | VALID_NOVEL | N |
| D0/A0 | 强制全部 NO_MATCH | INVALID | I |

`PARTIAL_MATCH` 是真实但不充分的 expected 关系，提供 supported coverage，不贡献主 hit，
也不计 FP。W、L、predicate usage、method 自报 D 和 method 自报 valid 不参与上述闭合。

## Method-cost audit v1

`derived/final_talk_cost_section7_v1/` 是 provider-free 的 method-cost audit，不是新的实验层。它以两侧各 162 个 method cells 的保存 usage receipt 为成本对象，使用 `gpt-5.6-luna` 的 uncached input/cache read/cache creation/output 价格卡，并排除 evaluator、人工审核、CPU、存储和开发成本。ours 的完整 receipt cost 为 `$7.18277320`；baseline 的 `$0.22523328` 仅为 known recorded subtotal，因一条 billable schema-error attempt 缺 usage 而不具完整 cost eligibility。历史 `$6.77501040` 只保留为错绑到 baseline archive 的旧 current/evidence-discovery provenance。audit 的 JSON、TSV、source hashes、重建命令和自校验均在该目录内。

## Relation、hit 和 precision

两侧 relation projection 合计必须覆盖 `(1271 + 512) * 145 = 258535` 行，每个 report/expected
恰好一次。`hit@1` 是 435 个 expected-round 单元中有 `VALID_KNOWN + FULL_MATCH` 的单元数；
`hit@3` 是 145 个 expected 中至少一轮 FULL 的数量；`hit@all` 是三轮均 FULL 的数量。
L2 对应分母是 `117` 和 `39`。

论文主指标固定为：

```text
report-based precision = (VALID_KNOWN + VALID_NOVEL) / all final reports
report-based FP rate = INVALID / all final reports
```

### Conversion attribution overlay

`derived/conversion_attribution_v1/` 是对冻结 current v4 invalid decisions 的 provider-free、evaluation-only 派生层。`report_attribution_v1.json` 对 291 条 I report 各保留一条记录，并以七类互斥 `primary_attribution` 区分 D0、普通 source-level FP、compiler/projection/runtime 机制和 indeterminate。`CONVERSION_LOWERING_CONFIRMED` 必须同时有 source absence/semantic mismatch 与具体 lowering/loss/ownership 证据；本版本为 0。118 条 NADC 中 110 条为已确认 method-owned mechanisms，8 条为 indeterminate。overlay 不修改 K/N/I 或 report-based precision；全部 I 仍在 `(K+N)/all reports` 分母。baseline v3 未提供同构 NADC subtype，故 precision-gap summary 对 NADC 只保留 current-side rate，机械零值残差仅作 bookkeeping。

它们使用逐条 report 作为分母，不使用 N/I group。发布级 operational composition 另行记录：

```text
K_hit = unique expected issue with at least one FULL across three rounds
N_group = same-side, same-pair, cross-round merged VALID_NOVEL substantive groups
I_diagnostic_cluster = same-side, same-pair, cross-round merged INVALID diagnostic cluster (diagnostic only; not a substantive defect entity)
ledger/group diagnostic ratio = (K_hit + N_group) / (K_hit + N_group + I_diagnostic_cluster)
ledger/group diagnostic invalid share = I_diagnostic_cluster / (K_hit + N_group + I_diagnostic_cluster)
```

N/I identity 至少包含 `side + pair_id + canonical_group_key`，并由人工确认的
property、author-source locus、repair obligation 和 substantive cause 支持；不跨 side/pair，
不按文本相似度、状态名或 expected ID 自动合并。`partial_only_known_report` 和
`partial_only_known_expected` 单独报告，不进入 K_hit 或 FP。N group 是实质性问题的
secondary analysis；I diagnostic cluster 不是缺陷实体，只是诊断聚类，不能用于论文主 precision 或 FP
结论。I 中的 D0、A0/`FALSE_POSITIVE`、A0/`NOT_A_DEFECT_CLAIM` 没有共同的
normative obligation、source locus 或 repair intent，不能仅凭 subtype、文本相似或同一
pair 合并。L2 ledger precision/FP 是 `not_applicable`，因为 N/I group 没有自然的 L2
expected 归属。

台账是研究人员/博士生基于作者 NL、PlantUML 和来源证据人工维护的
`expert-annotated expected issue ledger`，是 source-backed expected inventory，不是
穷尽所有缺陷的绝对 ground truth。K 按 expected ledger ID 去重；N 才按同一 side、同一
pair、同一实质义务/source locus/root cause/property/最小修复意图归并，允许跨 round，
不允许跨 pair；I 保留 report-level invalid 统计，cluster 仅用于敏感性分析。

## W 和 predicate

W0 只有散文主张；W1 有具体模型元素/路径定位但无精确 terminal receipt；W2 必须同时有
原始 executable object、typed input、精确 artifact hash、terminal true/false 和 receipt。
`hit_max_witness.json` 只在 FULL supporting reports 内按 `W2 > W1 > W0` 取最高档，分母
是 hit 单元；`W2/all-expected` 分母是 435。finding-level W 单独报告，不能混用。

`predicate_witness_audit.json` 的 `planned_scope` 从冻结 evaluator summary 读取完整 planned
scope（当前为 `full-scale-15` 的 15 个 ID），并以 `planned_in_frozen_scope` 明确每个 registry
predicate 的 membership；逐报告的 `report_bound_plan_count`、route、precise-binding、receipt/
terminal/failure 和 W0/W1/W2 是另一条 usage 轴。receipt 缺失/失败的合法 binding 仍
留在 all-usage 分母；FULL-hit supporting usage 单独给出。一个 finding 绑定多个 predicate
不增加 finding 数。X1v2 没有同构 receipt schema，predicate usage 明确为 `not_applicable`，
但 baseline W 仍按相同三档证据轴审计。

## Review、provenance 和 manifest

`derived/manual_adjudication_v3_baseline_ni/reviews/` 保存 v3 的独立复算、证据闭合、grouping、
academic、fairness/leakage 和文风 review；`reviews/arbitration_log_v3.json` 为每条 v3 report
提供可定位的 pane5 仲裁记录。`review_log.json` 每条 report 恰一条，记录 subagent raw-first blind proposal、pane5 主 session
逐条确认、解盲、冲突和最终 attestation。`human_supervised_authorization.json` 保存用户
授权消息、时间和 session。`reviewer_input_projection.jsonl` 与
`reviewer_projection_audit.json` 是去除 provider/model/profile/prompt/endpoint/credential、
report index、raw pointer、raw target hash 和 producer-specific location fields 的 raw-first
reviewer 输入投影。`location_text` 在两臂均固定为空；精确 raw identity/hash 只在独立
proposal 提交后可见的 `reviewer_unblind_mapping.json` 与 canonical evidence 中保存。
每个 pair/round 使用两臂相同的 slot universe；padding slot 是空输入闭合记录，不能成为
finding、classification 或统计单位。冻结 raw 中保留的历史元数据和精确 pointer 只在
inventory/canonical evidence 中保存。`MANIFEST` 绑定上述 canonical 文件、TSV、输入 manifests、projection 和 supporting
artifacts；顶层 `archive_manifest.json` 与 `publication_manifest.json` 绑定整个归档发布面。
`reviews/shuorenhua_process_v3.json` 另存 docs 场景的 protected spans、首轮问题清单、
二次回读和 fidelity diff；它是文风与文档保真审计，不是分类来源。

## 可复现与限制

当前 v4 和公平比较的 provider-free 验证入口：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_current_reaudit_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only
```

所有指标由 canonical JSON provider-free 重算。X1v2 缺少同构 method commit，v60 人工裁定有
未定价 usage；source catalog 中缺失的作者/出版物字段也保留为 evidence gap，不能从标题或
二手摘要补造。台账不完备、人工归并粒度、L2 语义边界、baseline schema 差异和观察性比较
不能推出因果。
