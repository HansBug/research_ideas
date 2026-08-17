# R5.7.3 客观代理指标框架报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

R5.7.3 的任务是把 R5.7.1 的评价逻辑链和 R5.7.2 的 Better STM / repair target 合同进一步落实为**客观代理指标框架 v0**：哪些指标可以进入 G0--G6 gate、每个指标需要哪些字段、使用哪个分母、如何避免刷指标、何时必须回到语义裁决，以及哪些指标只能作为报告背景或禁止用于质量结论 [src-framework][clm-r573-scope]。

本阶段仍属于真实 repair loop 前的协议冻结：它不运行 LLM、不生成 `STM_k`、不报告 Better STM 成功率，也不把 `.fcstm` / `pyfcstm` / converter 写成论文贡献 [clm-r573-no-effect]。

## 2. 核心结论

| 主题 | R5.7.3 冻结结论 | 证据键 |
|---|---|---|
| 指标定位 | 客观指标是 Better STM gate 的证据层，不是独立 verdict 系统；任何单项指标或总分都不能单独判 `better`。 | [clm-r573-permission] |
| 权限模型 | 冻结五级 `metric_permission`：`hard_gate / supporting_evidence / trigger_only / report_only / forbidden`。 | [clm-r573-permission] |
| schema | 每个 metric entry 必须声明指标族、gate、分母、聚合层、reference、偏序、scope、headline 权限、证据源、风险、语义裁决、禁止外推、冻结状态和下游 owner。 | [clm-r573-schema] |
| 指标族 | v0 指标族覆盖制品有效性、证据链、诊断、结构元素、追踪、场景行为、修复目标闭合、成本稳定性和 baseline / 文本弱指标背景。 | [clm-r573-families] |
| gate matrix | 所有指标必须落到 R5.7.2 G0--G6 gate × metric matrix，不另起总分系统。 | [clm-r573-gate-matrix] |
| reference / P-R-F1 | 不设统一 gold STM；P/R/F1 只在存在 adjudicated reference set、scenario oracle 或 confirmed target ledger 时使用。 | [clm-r573-no-gold] |
| anti-gaming | 指标框架显式记录 semantic deletion、guard/action/event folding、over/under repair、trace loss、conversion laundering、hierarchy loss、scenario overfitting 和 textual similarity misuse。 | [clm-r573-risk] |
| scope / 汇总 | 每项统计必须声明 T0/T0.5/T1 适用范围、headline 权限、pair / cluster / LLM-family 聚合层和 denominator layer。 | [clm-r573-scope-agg] |
| target closure | `must_fix`、`should_fix`、`monitor`、`not_repair_target`、`out_of_scope` 必须分层，不允许单一 closure 总分。 | [clm-r573-closure] |
| baseline 迁移 | `llms_emp` 与 Structure/Event 可作为核心指标思想来源；其余 baseline 仅作支持性设计启发或背景。 | [clm-r573-baseline] |

## 3. 指标框架结构

### 3.1 五级权限

R5.7.3 的最重要设计是先给指标“限权”，再谈计算。`hard_gate` 只决定是否可评价或协议是否有效；`supporting_evidence` 只能支持 G3/G4/G5 的局部判断；`trigger_only` 只触发复查；`report_only` 只进成本、稳定性或背景分析；`forbidden` 显式禁止某类外推 [clm-r573-permission]。

这避免了一个常见错误：把 parse ok、diagnostics fewer、F1 higher、scenario pass 或文本相似度当成 Better STM 的充分条件。R5.7.3 明确这些指标至多进入 evidence bundle，最终仍要回到 R5.7.2 的 G5 semantic gate [src-better][clm-r573-gate-matrix]。

### 3.2 指标族与 gate matrix

R5.7.3 指标族不是并列评分维度，而是挂在 G0--G6 gate 下的证据来源 [clm-r573-families][clm-r573-gate-matrix]：

| 指标族 | 主要服务的 gate | 典型用途 |
|---|---|---|
| `readiness_artifact_validity` | G1 / G6 | schema、parse、inspect、artifact validity。 |
| `provenance_reporting_completeness` | G1 / G2 / G6 | source、hash、change ledger、run record、denominator 证据链。 |
| `diagnostics` | G4 / G5 | 诊断减少作为 improvement 候选证据，同时触发删除语义风险检查。 |
| `structural_element` | G3 / G4 / G5 | state、transition、event、guard、action、hierarchy / pseudostate、trace link 分槽位观察。 |
| `traceability_grounding` | G2 / G3 / G5 / G6 | 元素到 `NL`、raw `STM_0`、source label 的追踪证据。 |
| `scenario_behavior` | G3 / G4 / G5 | no-regression 和预注册行为义务证据。 |
| `semantic_target_closure` | G4 / G5 | must-fix / should-fix / monitor 等 target-instance 分层闭合。 |
| `cost_stability` | G6 / report-only | token、runtime、retry、rollback、oscillation。 |
| `baseline_migration_or_textual_similarity` | report-only / forbidden for verdict | baseline 指标思想来源、文本弱信号和禁止外推记录。 |

### 3.3 结构槽位和折叠风险

结构指标必须拆为 `state / transition / event / guard / action / hierarchy_or_pseudostate / trace_link` 七个槽位 [clm-r573-families]。这样做是为了防止“整体结构 F1 看起来变好，但 guard/action 被塞进 event label”这类刷指标问题。例如 `buttonPressed [battery_ok] / motor_on` 若候选只保留一个 event label，则 event present 不能覆盖 guard/action 缺失；必须记录 `event_guard_action_folding_risk` 并进入 G5 语义裁决 [clm-r573-risk]。

### 3.4 reference、分母与偏序

R5.7.3 不设统一 gold STM。不同指标需要不同 reference：readiness 使用 parser/schema/inspector，no-regression 使用 canonical `STM_0` 与关键场景，slot-level P/R/F1 需要 adjudicated target set，target closure 使用 confirmed target ledger，scenario pass 使用 scenario oracle [clm-r573-no-gold]。

分母同样不能混用：scope counts 用 `scope_pool`，Better outcome 用 `adjudicated_pool`，target closure 用 `target_instance_ledger`，scenario pass 用 `scenario_ledger`，cost/stability 用 `run_ledger`。尤其不能把 `T0 = 48 pairs` 直接写成最终 eligible 或 success denominator [src-eval-logic][clm-r573-scope-agg]。

### 3.5 target closure 分层

`semantic_target_closure` 不允许只报一个闭合率。R5.7.3 要求至少拆成：`must_fix_closure_rate`、`should_fix_improvement_rate`、`monitor_stability_rate`、`not_repair_target_respect_rate`、`out_of_scope_exclusion_count` [clm-r573-closure]。这与 R5.7.2 的 `repair_action_allowed` 单值纪律一致：不同 target 层级的“未闭合”含义不同，不能合成一个总分。

## 4. baseline 调研迁移结论

R5.7.3 的 baseline 迁移采用奥卡姆剃刀原则：只迁移对本论文 `<NL, STM_0> -> STM_k` 修正评价有直接操作价值的指标思想；其余保留为支持性说明或背景，不能硬塞成指标 [clm-r573-baseline]。

| baseline / 线索 | R5.7.3 role | 可迁移内容 | 禁止迁移 |
|---|---|---|---|
| `llms_emp` | `core_metric_source` | `T_G` / parsing validity、`Acc_P` / `Acc_S` 的 grammar validity 思想、F1 的 reference-set 前提、Phase-II feedback resolution -> target closure。 | 不沿用 `Acc_P` / `Acc_S` 作为本文指标名；不迁移原文数值为本论文结果。 |
| Structure/Event | `core_metric_source` | state / transition / guard / action / hierarchy 分槽位 P/R/F1 思想。 | 不用 overall F1 掩盖 guard/action 局部退化。 |
| Designing FSM / TTool-AI / Nimbus / Umple | `supporting_design_note` | scenario / oracle、expert feedback、strict count 风险、compile / pass@k 的适用边界。 | 不把 expert score、compile 或 pass@k 写成语义质量。 |
| Agentic Flow FSM / Pushing Envelope / req / SpecGPT | `background_only` 或 `not_ingested` | 只作 related-work 背景或待核验线索。 | 不作为当前指标合同强证据。 |

R5.7.3 因而把 `llms_emp.Acc_P / Acc_S` 降级为源论文内部命名；本文指标应使用描述性 id，例如 `artifact_validity_rate`、`schema_validity_rate`、`Acc(scope)` 或 slot-level metric，而不是沿用 PlantUML / SysML 语法准确率命名 [clm-r573-baseline]。

## 5. 学术风险与禁止主张

### 5.1 当前阶段禁止主张

1. 禁止写“R5.7.3 已证明 repair loop 有效”：本阶段没有真实 `STM_k`、change ledger 或 semantic adjudication [clm-r573-no-effect]。
2. 禁止写“指标总分更高就是 Better STM”：R5.7.3 明确禁止 overall score / weighted score [clm-r573-permission]。
3. 禁止写“conversion success / `.fcstm` inspect ok 是 repair gain”：这些只属于 readiness / representation bridge [src-eval-logic]。
4. 禁止写“T0.5 tick 表示支持 timed automata”：T0.5 只能是离散 tick-counter caveat；T1 只作 stress / limitation [src-model-scope]。
5. 禁止把 LLM-family 差异写成 LLM 排名：它只能作为 source STM bias / repair difficulty 辅助分析 [clm-r573-scope-agg]。

### 5.2 对 R5.7.4 / R5.7.5 / R7 的风险提示

R5.7.4 必须用真实或准真实样例 dry-run 本框架，记录 ambiguous metric cases、schema missing fields、risk trigger false positive/false negative 和 v0-to-v1 proposal；没有 dry-run finding 的规则修订只能标为 provisional [src-better][clm-r573-risk]。

R5.7.5 需要把 R5.7.1 / R5.7.2 / R5.7.3 与 R5.7.4 findings 合成 R6/R7 handoff。R7 才能冻结 numeric thresholds、statistical test、effect size、final eligibility、primary / secondary endpoints 和最终成功分母 [clm-r573-schema]。

## 6. 后续入口

| 后续阶段 | 应读取 | 必须继承 | 不得做什么 |
|---|---|---|---|
| R5.7.4 | [objective_metric_framework.md](../experiment_design/metrics/objective_metric_framework.md)、R5.7.1/5.7.2 合同 | schema、指标族、gate matrix、risk tag、baseline migration 表。 | 不报告 repair effectiveness；不无证据改指标。 |
| R5.7.5 | 本报告、R5.7.4 findings、[evaluation_logic.md](../experiment_design/evaluation_logic.md)、[better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | claim boundary、gate、taxonomy、metrics、dry-run findings。 | 不重开已决策问题；只合成 handoff。 |
| R7 | R5.7.x 全部合同和 findings | final eligibility、metric columns、thresholds、statistical tests、primary / secondary endpoints。 | 不把指标替代 Better verdict；不隐藏 failure / partial / unknown。 |
| R8 | R7 正式运行与失败台账 | 结果表、失败分析和 limitation。 | 不把失败样例从 denominator 中消失。 |

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| [../experiment_design/metrics/objective_metric_framework.md](../experiment_design/metrics/objective_metric_framework.md) | 当前 PR 提交 | `2026-07-03 21:18:25` report freeze | 首次系统冻结 R5.7.3 metric permission、schema、指标族、gate matrix、anti-gaming、baseline migration 和 handoff。 | 当前 PR 后续链接 / 总账同步若有，不改变本报告 freeze time。 | 规则真源是 Markdown 合同；无真实 repair machine result。 |
| [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md) | `feb0deef` | R5.7.1 freeze | 冻结 claim boundary、分母、A 层、归因边界和指标 supporting-only 上限。 | R5.7.3 只追加指标框架链接，不重写 R5.7.1 结论。 | [../pipeline/readiness_audit/llms_emp_profile/](../../../pipeline/readiness_audit/llms_emp_profile) JSONL 支撑 denominator 事实。 |
| [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | `df4af008` + `1724051d` + `964ef6e0` | R5.7.2 freeze | 冻结 G0--G6 gate、三层输出、G5 rubric 和 evidence-driven revision。 | R5.7.3 只挂接 objective metrics 位置。 | 规则真源是 Markdown 合同；R5.7.4/R7 负责 dry-run / run evidence。 |

> 本节说明本 report 的冻结来源，不替代下面的事实源清单和 claim-evidence map。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-framework] | `r573_objective_metric_framework` | [../experiment_design/metrics/objective_metric_framework.md](../experiment_design/metrics/objective_metric_framework.md) | md | R5.7.3 客观代理指标框架真源。 | §1--§13；A.1--A.4。 |
| [src-eval-logic] | `r571_evaluation_logic` | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md) | md | R5.7.1 claim boundary、分母、A 层、归因边界、指标位置。 | §2--§10。 |
| [src-better] | `r572_better_stm_definition` | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) | md | R5.7.2 G0--G6、三层输出、semantic gate、T0.5 caveat。 | §1--§13。 |
| [src-taxonomy] | `r572_repair_target_taxonomy` | [../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) | md | repair target taxonomy、`repair_action_allowed`、target ledger。 | §1--§7。 |
| [src-model-scope] | `r56_model_scope` | [../story/model_scope.md](../story/model_scope.md) | md | T0/T0.5/T1、模型族、状态机抽象、禁止外推。 | §2--§6。 |
| [src-case] | `llms_emp_case_matrix` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | 10×6 denominator、pair time level、conversion/readiness 当前事实。 | JSONL fields: `nl_cluster_id`、`llm_family`、`time_level`、`conversion_status`、`parse_status`、`inspect_status`。 |
| [src-cluster] | `llms_emp_cluster_profiles` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../../../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | jsonl | cluster-level time / structure / story role。 | JSONL fields: `nl_cluster_id`、`time_level`、`structure_family`。 |
| [src-llms-emp-paper] | `llms_emp_paper_content` | [../../baselines/llms_emp/paper_content.txt](../../baselines/llms_emp/paper_content.txt) | txt | `T_G`、`Acc_P`、`Acc_S`、F1 与 feedback resolution 的来源线索。 | search `Evaluation Metrics`、`Acc_P`、`Acc_S`、`F1`。 |
| [src-structure-event] | `structure_event_desc` | [../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) | md | states / transitions / guards / actions / hierarchy 分槽位评价思想。 | DESC 中 evaluation / metric summary。 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r573-scope] | `R573-RPT-C1` | R5.7.3 的对象是 objective metric framework v0，不是 repair loop 或实验结果。 | scope | [src-framework] §1--§2；[src-eval-logic] §9；[src-better] §13。 | [cmd-r573-doc-links] | high | 只支持协议 / evaluation claim。 |
| [clm-r573-no-effect] | `R573-RPT-C2` | R5.7.3 不运行 LLM、不生成 `STM_k`、不报告 Better STM 成功率或 repair effectiveness。 | prohibition | [src-framework] §2.2；[src-eval-logic] §1/§9。 | [cmd-r573-required-terms] | high | R7/R8 才能报告效果。 |
| [clm-r573-permission] | `R573-RPT-C3` | 五级 `metric_permission` 限定指标权限，指标不能单独产生 Better verdict。 | contract | [src-framework] §2.1；PR #141 Q1 comment。 | [cmd-r573-required-terms] | high | critical regression 可作 hard negative trigger，但不是 Better positive verdict。 |
| [clm-r573-schema] | `R573-RPT-C4` | metric entry schema v0 必须包含分母、偏序、scope、风险、语义裁决、冻结状态等审计字段，并以机器检查阻止 T0.5/T1 混入 T0 headline。 | contract | [src-framework] §3 与 §11.2；PR #141 Q12 comment；PR #141 focused re-review。 | [cmd-r573-entry-schema] | high | R7 可扩展，不可删除最低审计字段。 |
| [clm-r573-families] | `R573-RPT-C5` | v0 指标族覆盖 readiness、provenance、diagnostics、structural、traceability、scenario、target closure、cost、baseline/textual background。 | contract | [src-framework] §4；PR #141 Q2/Q13 comments。 | [cmd-r573-required-terms] | high | textual similarity / conversion success 是降级项。 |
| [clm-r573-gate-matrix] | `R573-RPT-C6` | 指标必须落到 G0--G6 gate matrix，不另起 overall score。 | contract | [src-framework] §5；[src-better] §3/§9。 | [cmd-r573-required-terms] | high | 单项 override 不能突破 family 权限。 |
| [clm-r573-no-gold] | `R573-RPT-C7` | 本任务无统一 gold STM；P/R/F1 只在明确 reference set 下使用。 | decision | [src-framework] §7；PR #141 Q4 comment。 | 人工复验 | high | canonical `STM_0` 不是“越像越好”的 gold。 |
| [clm-r573-risk] | `R573-RPT-C8` | anti-gaming 风险模型必须显式覆盖删除语义、语义折叠、过修 / 欠修、trace loss、conversion laundering 等。 | protocol | [src-framework] §8；PR #141 Q8 comment。 | [cmd-r573-required-terms] | high | risk flag 需 evidence bundle 才能 confirmed。 |
| [clm-r573-scope-agg] | `R573-RPT-C9` | 统计必须声明 scope、headline 权限、pair / cluster / LLM-family 聚合层和 denominator，且 registry 必须机器级阻止 T0.5/T1 混入 T0 headline。 | protocol | [src-framework] §9 与 §11.2；[src-case]、[src-cluster]。 | [cmd-r573-entry-schema] + [cmd-r573-counts] | high | T0 scope 上限不是 success denominator。 |
| [clm-r573-closure] | `R573-RPT-C10` | target closure 必须按 target-instance 与 `repair_action_allowed` 分层，不得单一总分。 | protocol | [src-framework] §9.3；[src-taxonomy]。 | [cmd-r573-required-terms] | high | 当前没有真实 closure 结果。 |
| [clm-r573-baseline] | `R573-RPT-C11` | baseline migration 只把 `llms_emp` 和 Structure/Event 作为核心指标思想来源，其余降级为支持性说明或背景。 | decision | [src-framework] §10；[src-llms-emp-paper]；[src-structure-event]。 | [cmd-r573-required-terms] | medium | R7 前仍需对 Structure/Event 与部分 baseline 原文复核；不迁移 baseline 数值。 |

### A.4 复验命令

```bash
# [cmd-r573-doc-links]
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
for rel in [
    'experiment_design/metrics/objective_metric_framework.md',
    'experiment_design/metrics/README.md',
    'experiment_design/evaluation_logic.md',
    'experiment_design/quality_model/better_stm_definition.md',
    'experiment_design/quality_model/repair_target_taxonomy.md',
    'reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md',
]:
    p = base / rel
    print(rel, p.exists(), p.stat().st_size if p.exists() else 'missing')
PY
```

```bash
# [cmd-r573-counts]
python - <<'PY'
import json, collections, pathlib
base = pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
print('pairs', len(case), 'clusters', len({r['nl_cluster_id'] for r in case}))
print('conversion_status', collections.Counter(r['conversion_status'] for r in case))
print('parse_status', collections.Counter(r['parse_status'] for r in case))
print('inspect_status', collections.Counter(r['inspect_status'] for r in case))
print('pair_time', collections.Counter(r['time_level'] for r in case))
print('cluster_time', collections.Counter(r['time_level'] for r in clusters))
PY
```

```bash
# [cmd-r573-entry-schema]
python - <<'PY'
from pathlib import Path
import json
p = Path('project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/metrics/objective_metric_framework.md')
text = p.read_text()
section = text.split('### 11.2 完整 JSON registry', 1)[1].split('## 12.', 1)[0]
block = section.split('```json', 1)[1].split('```', 1)[0].strip()
entries = json.loads(block)
required = [
    'metric_id', 'metric_family', 'metric_definition', 'metric_permission', 'gate_position',
    'denominator_layer', 'aggregation_level', 'reference_type', 'fallback_when_no_reference',
    'ordering_relation', 'scope_applicability', 'headline_inclusion', 'evidence_source',
    'evidence_confidence', 'gaming_risk_tag', 'risk_trigger_condition', 'risk_required_evidence',
    'risk_gate_impact', 'semantic_adjudication_required', 'forbidden_extrapolation',
    'freeze_status', 'downstream_owner',
]
allowed_headline = {'yes_if_eligible', 'no_caveat_only', 'no_stress_or_excluded', 'report_only'}
missing = {
    entry.get('metric_id', f'index:{idx}'): [field for field in required if field not in entry]
    for idx, entry in enumerate(entries)
}
missing = {k: v for k, v in missing.items() if v}
headline_errors = {}
for idx, entry in enumerate(entries):
    mid = entry.get('metric_id', f'index:{idx}')
    scopes = entry.get('scope_applicability', [])
    if isinstance(scopes, str):
        scopes = [scopes]
    headline = entry.get('headline_inclusion')
    errors = []
    if isinstance(headline, dict):
        missing_scope = [s for s in scopes if s not in headline]
        if missing_scope:
            errors.append(f'missing headline scope keys: {missing_scope}')
        bad_values = {k: v for k, v in headline.items() if v not in allowed_headline}
        if bad_values:
            errors.append(f'invalid headline values: {bad_values}')
        if headline.get('T0_5_caveat') == 'yes_if_eligible':
            errors.append('T0_5_caveat cannot be yes_if_eligible')
        if headline.get('T1_stress_or_excluded') in {'yes_if_eligible', 'no_caveat_only'}:
            errors.append('T1_stress_or_excluded cannot enter headline/caveat headline')
    else:
        if headline not in allowed_headline:
            errors.append(f'invalid headline value: {headline}')
        if 'T0_5_caveat' in scopes and headline == 'yes_if_eligible':
            errors.append('scalar yes_if_eligible cannot cover T0_5_caveat; use scope-keyed headline map')
        if 'T1_stress_or_excluded' in scopes and headline in {'yes_if_eligible', 'no_caveat_only'}:
            errors.append('scalar headline value would let T1 enter headline/caveat headline; use no_stress/report or scope map')
        if len(scopes) > 1 and headline in {'yes_if_eligible', 'no_caveat_only', 'no_stress_or_excluded'}:
            errors.append('multi-scope non-report entry should use scope-keyed headline map')
    if errors:
        headline_errors[mid] = errors
print('entry_count', len(entries))
print('missing', missing)
print('headline_errors', headline_errors)
raise SystemExit(1 if missing or headline_errors else 0)
PY
```

```bash
# [cmd-r573-required-terms]
python - <<'PY'
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/metrics/objective_metric_framework.md')
text = p.read_text()
required = [
    'metric_permission', 'hard_gate', 'supporting_evidence', 'trigger_only', 'report_only', 'forbidden',
    'denominator_layer', 'aggregation_level', 'ordering_relation', 'scope_applicability', 'headline_inclusion',
    'gaming_risk_tag', 'semantic_adjudication_required', 'freeze_status',
    'readiness_artifact_validity', 'structural_element', 'traceability_grounding', 'scenario_behavior', 'semantic_target_closure',
    'event_guard_action_folding_risk', 'must_fix_closure_rate', 'should_fix_improvement_rate',
    'G0 scope', 'G1 readiness', 'G2 attribution', 'G3 no-regression', 'G4 improvement', 'G5 semantic', 'G6 reporting',
]
missing = [x for x in required if x not in text]
print('missing', missing)
raise SystemExit(1 if missing else 0)
PY
```
