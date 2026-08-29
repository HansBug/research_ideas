# Numeric Targeted Rereview

## 结论

**FAIL**。本记录是独立的 `subagent:numeric-artifact-targeted-rereview` proposal，不是人工最终裁定，也没有读取或复制旧 numeric review 的结论。审查只读取冻结 raw、canonical `manual_adjudication_v2` JSON、现行 recompute 函数和 provider-free validator；没有调用 provider，没有修改 frozen raw 或 canonical decisions。

本次复算显示 canonical 数值与现行 deterministic recompute 全部一致；但 canonical 包仍有一个 manifest hash 失配，predicate audit 的 `planned_count` 还没有表达冻结的 15-item planned scope，故不能给整个 targeted review PASS。

## 复核命令

以下命令均在
`project_1_llm_state_machine_modeling/paper_stm_issue_discover/` 下执行。

```bash
PYTHONPATH=evaluation/src:scripts/evaluation python - <<'PY'
# In-memory call of metric_bundle/build_predicate_audit and
# build_inventory_from_archive; no dump/write call was made.
PY

PYTHONPATH=evaluation/src python scripts/evaluation/validate_manual_adjudication.py \
  --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

独立内存复算结果：`PASS`；两侧 `metric_bundle` 与
`derived/manual_adjudication_v2/summary.json` 全字段相同，predicate audit 与
现行 `build_predicate_audit` 输出相同，raw inventory 重新枚举相同。

validator 当前结果：`FAIL`。

```text
ValueError: MANIFEST hash mismatch: README.md
```

错误来自
`scripts/evaluation/validate_manual_adjudication.py:536`；canonical MANIFEST
的 hash 比较逻辑在 `validate_manifest` 中执行。

## Raw 与全集闭合

证据路径：

- `final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/inventory.json`
- `final_results/v60_current_vs_x1v2_baseline/raw/v60_current/archive_manifest.json`
- `final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/archive_manifest.json`
- `final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/SUMMARY.md:23-30`
- `final_results/v60_current_vs_x1v2_baseline/reference/ledger.json`

| 项目 | v60/current | X1v2 baseline |
|---|---:|---:|
| method cells | 162 | 162 |
| reports/findings | 1271 | 512 |
| round 1 / 2 / 3 reports | 415 / 446 / 410 | 173 / 163 / 176 |

ledger 重新读取为 145 expected issues、435 round-level units；L2 为 39 issues、117 round-level units。两侧 canonical decisions 的关系数为
`(1271 + 512) * 145 = 258535`，每条 report 覆盖 145 个 expected。

## 独立复算结果

### D/A、validity、K/N/I

| 指标 | v60/current | X1v2 baseline |
|---|---:|---:|
| D2 | 724/1271 = 56.96% | 410/512 = 80.08% |
| D1 | 257/1271 = 20.22% | 0/512 = 0.00% |
| D0 | 121/1271 = 9.52% | 0/512 = 0.00% |
| A0 | 169/1271 = 13.30% | 102/512 = 19.92% |
| VALID_KNOWN / VALID_NOVEL / INVALID | 750/231/290 | 276/134/102 |
| K / N / I | 750/231/290 | 276/134/102 |

canonical summary 与独立 `metric_bundle` 的 D/A、validity、KNI、relation、hit、W、cost 字段均为 exact match。

### Relation 与 hit

| 指标 | v60/current | X1v2 baseline |
|---|---:|---:|
| FULL / PARTIAL / NONE relation rows | 688 / 279 / 183328 | 265 / 107 / 73868 |
| relation denominator | 184295 | 74240 |
| hit@1 / FULL | 310/435 = 71.26% | 211/435 = 48.51% |
| L2 hit@1 / FULL | 105/117 = 89.74% | 46/117 = 39.32% |
| hit@3 | 119/145 = 82.07% | 104/145 = 71.72% |
| hit@all | 86/145 = 59.31% | 37/145 = 25.52% |
| L2 hit@3 | 37/39 = 94.87% | 26/39 = 66.67% |
| L2 hit@all | 33/39 = 84.62% | 5/39 = 12.82% |
| supported coverage, round units | 338/435 = 77.70% | 244/435 = 56.09% |
| supported coverage, unique expected | 128/145 = 88.28% | 116/145 = 80.00% |

### Precision、FP 与 ledger groups

| 指标 | v60/current | X1v2 baseline |
|---|---:|---:|
| report precision | 981/1271 = 77.18% | 410/512 = 80.08% |
| report FP rate | 290/1271 = 22.82% | 102/512 = 19.92% |
| partial-only known reports | 109/1271 = 8.58% | 42/512 = 8.20% |
| partial-only known expected | 22/145 = 15.17% | 24/145 = 16.55% |
| K_hit | 119/145 = 82.07% | 104/145 = 71.72% |
| N_group | 121 | 134 |
| I_group | 187 | 102 |
| ledger composition denominator | 427 | 340 |
| ledger precision | 119/427 = 27.87% | 104/340 = 30.59% |
| ledger FP rate | 187/427 = 43.79% | 102/340 = 30.00% |

L2 ledger precision/FP 为 `not_applicable`，因为 N/I groups 没有自然的 L2 expected 归属。N/I group 计数来自 `group_decisions.json`，独立调用 `validate_group_decisions` 通过；没有跨 side 或跨 pair 的 group closure 错误。

### W

| 指标 | v60/current | X1v2 baseline |
|---|---:|---:|
| finding-level W0/W1/W2 | 0/749/522（分母 1271） | 1/511/0（分母 512） |
| FULL-hit max-W0/W1/W2 | 0/113/197（分母 310） | 0/211/0（分母 211） |
| W2/all-expected | 197/435 = 45.29% | 0/435 = 0.00% |

hit-level W 只取 `VALID_KNOWN + FULL` supporting report；W2/all-expected 使用 435 分母。独立重算没有将 PARTIAL、INVALID 或 later Judge 证据计入 hit-level W。

### Predicate usage

现行 `build_predicate_audit` 在内存中重算得到 19 个 registry predicate，且与 canonical
`predicate_witness_audit.json` exact match：

| 项目 | v60/current |
|---|---:|
| usage binding / route / precise binding / receipt present | 825 / 825 / 825 / 825 |
| terminal true / false | 0 / 522 |
| all-usage W0/W1/W2 | 0 / 303 / 522（分母 825） |
| FULL-hit supporting usage | 353 |
| FULL-hit usage W0/W1/W2 | 0 / 53 / 300（分母 353） |
| predicate registry rows | 19 |

X1v2 predicate usage 为 `not_applicable`，不是零填充；其独立 W 审计仍为 `1/511/0`。

## Cost

来源：`final_results/v60_current_vs_x1v2_baseline/derived/recomputed_summary.json`，由现行
recompute 函数读取并原样带入 metric bundle。

| 成本项 | v60/current | X1v2 baseline |
|---|---:|---:|
| method cost | `$7.18277320`, eligible=True | `$6.77501040`, eligible=True |
| Judge/review recorded cost | `$39.78176580`, eligible=False | `$11.45008520`, eligible=True |
| Judge logical calls | 1374 | not recorded |
| unpriced billable Judge calls | 10 | not recorded |

## Findings

### NUM13-I001: canonical MANIFEST hash mismatch

- **Severity:** `I`
- **Status:** `FAIL`
- **Path/line:** `derived/manual_adjudication_v2/MANIFEST:1`; validator `scripts/evaluation/validate_manual_adjudication.py:536`
- **Reason:** `README.md` 当前存在，但 MANIFEST 记录的 hash 为 `sha256:74325c1c4be3ab67fd5069eb1538b20a69bf783227e0a5d2bbf0f41bb702eb56`，实际文件 hash 为 `sha256:339166157d9c8208edecbc2f7383693887f49a1ae25f9714eb80936e866e9366`。canonical MANIFEST 还记录了 `protocol_freeze_v2.md` 的旧 hash。validator 因此不能确认 canonical package 的完整性。
- **Basis:** provider-free validator 输出 `ValueError: MANIFEST hash mismatch: README.md`；逐文件 SHA-256 对拍发现 README 和 protocol_freeze_v2 两项失配。
- **Evidence:** `final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/MANIFEST:1`；对应两个文件；`scripts/evaluation/validate_manual_adjudication.py:536-537`。
- **Disposition:** `FAIL; PENDING_FIX`。待所有 canonical 文件稳定后重生成 MANIFEST，再执行 validator 和 targeted rereview。

### NUM13-I002: planned predicate denominator is not the frozen planned scope

- **Severity:** `I`
- **Status:** `FAIL`
- **Path/line:** `scripts/evaluation/recompute_manual_adjudication.py:178-185,210-220`; `raw/v60_current/judge/composite/evaluator/evaluation_summary.json`; `raw/v60_current/method/SUMMARY.md:27-30`
- **Reason:** 当前函数把 `planned_count` 从每条最终 report 的 `predicate_id` 累加；这不是冻结 evaluator 的 planned scope。raw evaluator 明确给出 `planned_predicate_count=15` 和 15 个 planned IDs，包括 `S1,S2,S3,S4,S5,S6,G1,G2,G3,G4,R1,R2,R4,V1,V4`。canonical predicate 表却对 `S1,S6,G3,G4,R1,R4,V1` 等 planned 但没有 report-bound usage 的 predicate 写成 planned count 0，并将该字段与 route/precise/receipt 同列。现行 audit 可以自洽复现 825 个 report-bound precise bindings，但不能独立表达 planned=15 与 observed usage 的区别。
- **Basis:** 独立内存调用 `build_predicate_audit` 与 canonical predicate JSON exact match；同时直接读取 raw planned list，并审阅函数 `planning_by_predicate[predicate_id]["planned"] += 1` 的实现。raw method 另记录 2461 execution receipts、12 executed predicates，不能被 825 report-bound usage 静默替代。
- **Evidence:** `final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/evaluator/evaluation_summary.json`；`final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/SUMMARY.md:27-30`；`scripts/evaluation/recompute_manual_adjudication.py:178-185,215-220`；`derived/manual_adjudication_v2/predicate_witness_audit.json:1`。
- **Disposition:** `FAIL; PENDING_FIX`。拆分 frozen planned-scope 字段（15-item membership/denominator）与 report-bound usage 字段，明确 2461 raw receipts、selected evaluator receipts 和 canonical finding bindings 的关系，并补充 provider-free regression assertion。

## 修复后状态与 targeted rereview

| 项目 | 状态 |
|---|---|
| canonical metric recompute | `PASS`，两侧 summary exact match |
| raw inventory and report closure | `PASS`，162/162 cells，1271/512 reports |
| dense relation count | `PASS`，258535 |
| D/A、validity、KNI、hit/L2、precision/FP、groups、W、cost | `PASS`，均由内存重算复核 |
| baseline predicate not_applicable | `PASS` |
| canonical manual validator | `FAIL`，MANIFEST hash mismatch |
| predicate planned-scope audit | `FAIL`，NUM13-I002 |
| targeted rereview of NUM13-I001/I002 | `PENDING_FIX` |

在上述两个 finding 修复并重新生成受影响的 canonical manifest/audit 后，需要再次执行本记录中的 validator 和内存 recompute。此次 reviewer 没有执行 recompute 脚本的 `main`，因为该入口会回写 canonical JSON/MANIFEST；没有执行 method/Judge/provider 调用。

## Follow-up Targeted Rereview

本节为同一 reviewer 在 raw-first submission 已持久化后，对修复后稳定快照进行的 targeted rereview；它 supersedes 上述两个 finding 的待修复状态。reviewer 仍为 `subagent:numeric-artifact-targeted-rereview`，proposal-only、只读、provider calls `0`。

复核命令：

```bash
PYTHONPATH=evaluation/src:scripts/evaluation python - <<'PY'
# In-memory only: build_inventory_from_archive, validate_decision_set,
# validate_group_decisions, metric_bundle and build_predicate_audit.
# No dump/write call was made.
PY

PYTHONPATH=evaluation/src python scripts/evaluation/validate_manual_adjudication.py \
  --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

结果：

- independent `metric_bundle` 与 canonical `summary.json`：v60、X1v2 均 `summary_exact=True`；
- independent `build_predicate_audit` 与 canonical predicate audit：`predicate_exact=True`；
- raw inventory：`162/162` cells、`1271/512` reports，round counts `415/446/410` 与 `173/163/176`；
- dense relation：`258535`；
- canonical validator：`PASS`，输出 `{"decision_counts":{"v60_current":1271,"x1v2_baseline":512},"status":"PASS"}`；
- canonical MANIFEST：逐文件 hash mismatch `0`。

修复状态：

- `NUM13-I001`：`FIXED; targeted rereview PASS`。README/protocol hash 已与 MANIFEST 对齐。
- `NUM13-I002`：`FIXED; targeted rereview PASS`。predicate audit 现在显式保存 `planned_scope.count=15`、`planned_in_frozen_scope` 和 `report_bound_plan_count`，并将 planned scope 与 observed usage 分离。

最终 targeted rereview 结论：**PASS**。上述主结果、D/A、K/N/I、hit/L2、两种 precision/FP、N/I groups、W、predicate usage 与 cost 均已在修复后稳定快照中重新独立复算；没有修改 raw 或 canonical decision labels。
## Latest independent targeted rereview (2026-08-29)

身份：`subagent:numeric-artifact-targeted-rereview`；本节是当前 raw-first 独立复核记录。未读取或复制旧 numeric review 的结论；未调用 provider，未修改 frozen raw、canonical decision JSON/TSV 或其他 canonical labels。

### Verdict

`FAIL` pending one artifact-closure repair. The numerical and dense canonical projections independently recompute, but the formal validator fails closed because the inventory and manual MANIFEST retain stale hashes for two top-level source manifests that were subsequently changed.

Finding `NUM13-I003` (`I`, artifact closure):

- Evidence: `derived/manual_adjudication_v2/inventory.json` and `derived/manual_adjudication_v2/MANIFEST` record `archive_manifest.json` as `sha256:93e31be21628b5ae6343d47ec4b7ecf228ef5bf19a6cb58bd1dde40838a6cfce` and `publication_manifest.json` as `sha256:b0d494bae61635fba3763ed796393d305e85f7559f0e5f72c2a9ef2e0189e56d`; current files hash to `sha256:1c88343f854ef0019c6f1e29c81c898272568422f2b4e18fbef395cfe1033289` and `sha256:ab93ecbe0aee265f6ff5ecb74cf761520fbbccaeed06b1be5791146d47c6df78`.
- Basis: the fresh inventory builder found the same 1271/512 report universe and 162/162 cells, but `validate_manual_adjudication.py` stopped at `validate_raw_inventory()` with `ValueError: inventory does not equal a fresh enumeration of the frozen archive`. The two side-specific raw archive manifest hashes still match.
- Impact: the release validator is not PASS and the current audit directory cannot yet be treated as a closed release. Required disposition is to regenerate the inventory and all dependent source-hash fields against the current manifests, then rerun the full validator and this targeted rereview. No repair commit exists in this reviewer session; targeted rereview therefore remains `FAIL`.

### Independent raw and canonical checks

Commands run from `project_1_llm_state_machine_modeling/paper_stm_issue_discover`:

```text
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/validate_manual_adjudication.py --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

Result: `FAIL` only at stale inventory/source-manifest comparison, before later validator stages.

The following read-only in-memory check used the fresh `build_manual_inventory.py` output, Pydantic decision models, current raw files and current canonical files. It passed:

```text
fresh raw inventory: v60 1271, X1v2 512; cells 162/162
round counts: v60 415/446/410; X1v2 173/163/176
raw path/hash/JSON-pointer closure: PASS
v60 decision/TSV/W2 closure: PASS (1271)
X1v2 decision/TSV/W2 closure: PASS (512)
group/source-ref closure: PASS (544 groups)
dense relation rows/unique keys: 258535/258535
dense relation equality with nested canonical rows: PASS
INVALID positive relations: 0
```

The deterministic recomputation comparison also passed with zero field differences for both side summaries, including hit/L2, precision/FP, supported coverage, partial-only-known, W, costs and ledger composition:

| side | D2/D1/D0/A0 | K/N/I | hit@1 | hit@3 | hit@all | L2 hit@1 | report precision | report FP | K_hit/N_group/I_group | finding W0/W1/W2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v60/current | 724/257/121/169 | 750/231/290 | 310/435 | 119/145 | 86/145 | 105/117 | 981/1271 | 290/1271 | 119/121/187 | 0/749/522 |
| X1v2 baseline | 410/0/0/102 | 276/134/102 | 211/435 | 104/145 | 37/145 | 46/117 | 410/512 | 102/512 | 104/134/102 | 1/511/0 |

Additional recomputed values:

- v60 L2 hit@3/all `37/39`, `33/39`; X1v2 L2 hit@3/all `26/39`, `5/39`.
- v60 ledger composition denominator `427`, precision `119/427`, FP `187/427`; X1v2 denominator `340`, precision `104/340`, FP `102/340`.
- v60 partial-only known `109/1271` reports and `22/145` expected IDs; X1v2 `42/512` and `24/145`.
- v60 supported coverage `338/435` round units and `128/145` unique expected IDs; X1v2 `244/435` and `116/145`.
- max-W on FULL hits: v60 `W0/W1/W2 = 0/113/197` over `310`; X1v2 `0/211/0` over `211`. W2/all-expected is v60 `197/435`, X1v2 `0/435`.
- current predicate audit projection equals deterministic rebuild: 19 registry rows, planned frozen scope `15/19`, all usage `825`, FULL-hit supporting usage `353`; baseline status is `not_applicable`. The canonical audit and rebuild agree row by row.
- Method/Judge cost fields are preserved from `derived/recomputed_summary.json`: v60 method `$7.18277320`, Judge `$39.78176580`, 1374 logical calls and 10 unpriced billable calls; X1v2 method `$6.77501040`, Judge `$11.45008520`.
- `hit_max_witness.json`, `predicate_witness_audit.json` and `reference_ledger_aggregate.json` each equal their deterministic in-memory rebuild; canonical MANIFEST internal file hash mismatch count is `0`.

### Targeted rereview disposition

All numerical, dense-relation, raw-pointer, W2, grouping, predicate projection and cost checks are `PASS`. `NUM13-I003` is the sole open finding. It is an artifact-manifest synchronization issue, not a finding against frozen raw data or the canonical decision labels. After the inventory/source-hash repair, rerun the exact validator command above and record the repair commit plus a new targeted `PASS`; until then this review is `FAIL`.
## Final post-fix numeric review (2026-08-29)

身份仍为 `subagent:numeric-artifact-targeted-rereview`，proposal/review 身份明确；本节只读取当前 raw、canonical JSON/TSV、summary、group、hit witness、predicate audit、reference aggregate 和现行脚本，没有调用 provider，也没有修改 frozen raw 或 canonical data。

### Final verdict: FAIL

`NUM13-I003` 仍未修复完整，属于 release-blocking artifact closure finding：

- `derived/manual_adjudication_v2/inventory.json:source_manifests` 仍记录 `archive_manifest.json` 为 `sha256:93e31be21628b5ae6343d47ec4b7ecf228ef5bf19a6cb58bd1dde40838a6cfce`，实际为 `sha256:1c88343f854ef0019c6f1e29c81c898272568422f2b4e18fbef395cfe1033289`。
- 同字段仍记录 `publication_manifest.json` 为 `sha256:b0d494bae61635fba3763ed796393d305e85f7559f0e5f72c2a9ef2e0189e56d`，实际为 `sha256:ab93ecbe0aee265f6ff5ecb74cf761520fbbccaeed06b1be5791146d47c6df78`。
- `derived/manual_adjudication_v2/MANIFEST` 的四个 `raw_input_hashes` 已与当前文件一致，但这不能替代 inventory 的 fresh-enumeration equality；两个 side-specific raw archive manifest hash 也一致。
- 正式 validator 在 `scripts/evaluation/validate_manual_adjudication.py:135` / `:646` 处失败：`ValueError: inventory does not equal a fresh enumeration of the frozen archive`。

Disposition: `FAIL; PENDING_FIX`。Required repair is to regenerate `inventory.json` against the current top-level manifests, regenerate any dependent v2 manifest fields, then rerun the full validator. Repair commit: `none available in this review snapshot` (the affected files remain uncommitted in the working tree). Targeted rereview result: `FAIL`, because the same finding remains reproducible. This is not a numerical disagreement and does not alter the frozen raw or canonical decision labels.

### Commands and independent results

Formal validator, run from `project_1_llm_state_machine_modeling/paper_stm_issue_discover`:

```text
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/validate_manual_adjudication.py --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

Result: `FAIL` at inventory equality. A fresh `build_manual_inventory.py` comparison independently found v60/current `162` cells and `1271` reports, X1v2 baseline `162` cells and `512` reports, round counts `415/446/410` and `173/163/176`, and `1783` raw report items. Only the two top-level source-manifest entries differ.

Recompute was run without touching the repository by symlinking current raw/canonical inputs into `/tmp/paper1_numeric_final_recompute.3nblOW` and executing:

```text
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/recompute_manual_adjudication.py --directory /tmp/paper1_numeric_final_recompute.3nblOW/derived/manual_adjudication_v2
```

It returned `status=PASS`, `dense_relations=258535`, `reports={v60_current:1271,x1v2_baseline:512}`, `provider_calls=0`. Temporary `relation_decisions.json`, `hit_max_witness.json`, `predicate_witness_audit.json`, `reference_ledger_aggregate.json` and `summary.json` each byte-matched the current canonical file. Current canonical MANIFEST hash checks were all `0` mismatches; decision/TSV files were included in that check.

### Independently checked metrics

All entries below are `numerator/denominator (percentage)` from current `derived/manual_adjudication_v2/summary.json`, not hand-entered values.

| Metric | v60/current | X1v2 baseline | v60 minus X1v2 |
|---|---:|---:|---:|
| D2/D1/D0/A0 report counts | 724/257/121/169 | 410/0/0/102 | +314/+257/+121/+67 reports |
| K/N/I report counts | 750/231/290 | 276/134/102 | +474/+97/+188 reports |
| FULL/PARTIAL/NONE dense relations | 688/279/183328 of 184295 | 265/107/73868 of 74240 | +423/+172/+109460 rows; different report denominators |
| overall hit@1/FULL | 310/435 (71.26%) | 211/435 (48.51%) | +99/435; +22.76 pp |
| hit@3 | 119/145 (82.07%) | 104/145 (71.72%) | +15/145; +10.34 pp |
| hit@all | 86/145 (59.31%) | 37/145 (25.52%) | +49/145; +33.79 pp |
| L2 hit@1/FULL | 105/117 (89.74%) | 46/117 (39.32%) | +59/117; +50.43 pp |
| L2 hit@3 | 37/39 (94.87%) | 26/39 (66.67%) | +11/39; +28.21 pp |
| L2 hit@all | 33/39 (84.62%) | 5/39 (12.82%) | +28/39; +71.79 pp |
| supported coverage, round units | 338/435 (77.70%) | 244/435 (56.09%) | +94/435; +21.61 pp |
| supported coverage, unique expected | 128/145 (88.28%) | 116/145 (80.00%) | +12/145; +8.28 pp |
| partial-only known reports | 109/1271 (8.58%) | 42/512 (8.20%) | +0.38 pp; report denominators differ |
| partial-only known expected | 22/145 (15.17%) | 24/145 (16.55%) | -2/145; -1.38 pp |
| report-based precision | 981/1271 (77.18%) | 410/512 (80.08%) | -2.89 pp |
| report-based FP rate | 290/1271 (22.82%) | 102/512 (19.92%) | +2.89 pp |
| ledger K_hit | 119/145 (82.07%) | 104/145 (71.72%) | +15/145; +10.34 pp |
| ledger N_group | 121/427 (28.34%) | 134/340 (39.41%) | -11.07 pp |
| ledger I_group / FP | 187/427 (43.79%) | 102/340 (30.00%) | +13.79 pp |
| ledger precision | 119/427 (27.87%) | 104/340 (30.59%) | -2.72 pp |
| ledger FP rate | 187/427 (43.79%) | 102/340 (30.00%) | +13.79 pp |
| finding-level W0/W1/W2 | 0/749/522 of 1271 | 1/511/0 of 512 | counts as shown; different denominators |
| FULL-hit max-W0/W1/W2 | 0/113/197 of 310 | 0/211/0 of 211 | W1 -63.55 pp; W2 +63.55 pp |
| W2/all-expected | 197/435 (45.29%) | 0/435 (0.00%) | +197/435; +45.29 pp |

L2 ledger precision and FP rate remain `not_applicable` for both sides, with the protocol reason that N/I groups have no natural L2 expected attribution. Current predicate witness audit independently covers all `19` registry rows, frozen planned scope `15/19`, all usage `825` bindings and FULL-hit supporting usage `353`; its per-predicate W0/W1/W2 and failure/degradation rows match the deterministic rebuild. X1v2 predicate usage remains `not_applicable`, not zero. Costs are v60 method `$7.18277320`, Judge `$39.78176580`, `1374` logical Judge calls and `10` unpriced billable calls; X1v2 method `$6.77501040`, Judge `$11.45008520`.

### Targeted rereview status

Numerical recomputation, report/TSV closure, dense relation closure, raw path/hash/pointer closure, W2 receipt checks, group checks, predicate audit, cost fields and canonical per-file hashes are `PASS`. The formal release validator is `FAIL` solely because `inventory.json` has not been regenerated for the current top-level manifest hashes. No repair commit or successful targeted rereview is present; final status is therefore `FAIL`, not `PASS`.
## Current working-tree independent numeric review (2026-08-29)

身份：`subagent:numeric-artifact-targeted-rereview`，仅为独立 provider-free proposal/review。本节不采用此前 review 中的数值，直接从当前 canonical JSON/TSV、ledger、raw inventory、group/hit/predicate files、报告和现行脚本重算；没有修改 raw 或 canonical artifacts。

### Verdict: FAIL

数值、闭合和报告表均通过，但 release metadata 尚未闭合，故不能给 PASS。

`NUM13-I005` (`I`, fresh-inventory closure): [inventory.json](../derived/manual_adjudication_v2/inventory.json) 的 `/source_manifests/archive_manifest.json` 与 `/source_manifests/publication_manifest.json` 仍分别记录旧 hash `93e31b...`、`b0d494...`；当前文件 hash 是 `1c8834...`、`ab93ec...`。其余两个 frozen raw archive manifest hash 一致。正式 validator 因 [validate_manual_adjudication.py](../../../scripts/evaluation/validate_manual_adjudication.py:135) 的 fresh-enumeration equality fail-closed。

`NUM13-I006` (`I`, canonical MANIFEST closure): [MANIFEST](../derived/manual_adjudication_v2/MANIFEST:1) 的 `/canonical_files/reviewer_input_projection.jsonl` 记录 `384437...`，当前是 `5b6e4a...`；`/canonical_files/reviewer_projection_audit.json` 记录 `b8f8fc...`，当前是 `2cbbe9...`。该错误在 inventory 修复后会由 [validate_manual_adjudication.py](../../../scripts/evaluation/validate_manual_adjudication.py:635) 的 manifest gate 捕获。

两项 finding 的 disposition 均为 `PENDING_FIX`。当前 `HEAD` 是 `af7cab04aa10061febc356d62fdf6efac759ad6b`，没有覆盖上述 metadata 的 repair commit；顶层 `archive_manifest.json` 和 `publication_manifest.json` 仍为未提交修改。Targeted rereview 建议：先用 current archive rebuild `inventory.json`，再运行 `build_reviewer_projection.py` 重建两份 projection，随后 provider-free recompute 重建 MANIFEST，最后重跑 full validator 和本 review。不要修改 raw 或 decisions。

### Reproduction commands

```text
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/validate_manual_adjudication.py --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/build_manual_inventory.py --archive-root final_results/v60_current_vs_x1v2_baseline --output final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/inventory.json
PYTHONPATH=evaluation/src:scripts/evaluation python scripts/evaluation/build_reviewer_projection.py --archive-root final_results/v60_current_vs_x1v2_baseline --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

For this read-only review, recompute was instead run against a temporary symlinked input directory. It returned `PASS`, `provider_calls=0`, `1271/512` reports and `258535` dense relations; its generated relation, hit witness, predicate audit, reference aggregate and summary files byte-matched the canonical counterparts.

### Independent numeric result

Fresh raw inventory passed: v60/current `162` cells and `1271` reports (`415/446/410` by round); X1v2 baseline `162` cells and `512` reports (`173/163/176`). The provider-free Pydantic/raw-identity/TSV/W2 checks, human-process files, `543` group records, source refs and all `258535` dense relation rows passed.

| Metric | v60/current | X1v2 baseline | v60 minus baseline |
|---|---:|---:|---:|
| D2/D1/D0/A0 reports | 721/259/120/171 | 408/3/2/99 | +313/+256/+118/+72 |
| K/N/I reports | 749/231/291 | 279/132/101 | +470/+99/+190 |
| hit@1 | 310/435 (71.26%) | 212/435 (48.74%) | +98; +22.53 pp |
| hit@3 / hit@all | 119/145 (82.07%) / 86/145 (59.31%) | 104/145 (71.72%) / 38/145 (26.21%) | +15; +10.34 pp / +48; +33.10 pp |
| L2 hit@1 / hit@3 / hit@all | 105/117 (89.74%) / 37/39 (94.87%) / 33/39 (84.62%) | 46/117 (39.32%) / 26/39 (66.67%) / 5/39 (12.82%) | +59; +50.43 pp / +11; +28.21 pp / +28; +71.79 pp |
| report precision / FP rate | 980/1271 (77.10%) / 291/1271 (22.90%) | 411/512 (80.27%) / 101/512 (19.73%) | -3.17 pp / +3.17 pp |
| K_hit / N_group / I_group | 119/145 / 121/429 / 189/429 | 104/145 / 132/337 / 101/337 | +15 / -11 / +88 counts |
| ledger precision / FP | 119/429 (27.74%) / 189/429 (44.06%) | 104/337 (30.86%) / 101/337 (29.97%) | -3.12 pp / +14.09 pp |
| finding W0/W1/W2 | 0/749/522 of 1271 | 1/511/0 of 512 | side-specific report denominators |
| FULL-hit max W0/W1/W2 | 0/113/197 of 310 | 0/212/0 of 212 | W2 +63.55 pp |
| W2/all expected | 197/435 (45.29%) | 0/435 (0.00%) | +45.29 pp |

Relation counts are v60 `685/279/183331` and baseline `265/110/73865` for FULL/PARTIAL/NO across dense denominators `184295`/`74240`; PARTIAL is separate from hits and FP. Supported coverage is `337/435` and `128/145` for v60, `245/435` and `116/145` for baseline. Partial-only known is `110/1271`, `21/145` versus `45/512`, `24/145`. Current predicate audit covers all 19 registry rows, frozen planned scope `15/19`, `825` all usages and `353` FULL-hit usages; baseline is `not_applicable`. L2 ledger precision/FP is `not_applicable` on both sides. Costs remain v60 method `$7.18277320`, Judge `$39.78176580` (1374 logical calls, 10 unpriced billable calls); baseline method `$6.77501040`, Judge `$11.45008520`.

The report numeric table agrees with the current summary for all checked metrics at [v60_current_vs_x1v2_baseline_cn.md](../report/v60_current_vs_x1v2_baseline_cn.md:21) through [v60_current_vs_x1v2_baseline_cn.md](../report/v60_current_vs_x1v2_baseline_cn.md:70). Once `NUM13-I005` and `NUM13-I006` are repaired, rerun the validator and repeat this targeted rereview; until then the independent review remains `FAIL`.
