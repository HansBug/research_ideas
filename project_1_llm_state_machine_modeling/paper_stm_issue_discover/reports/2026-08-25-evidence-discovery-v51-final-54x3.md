# Evidence Discovery v51 最终 54x3 实验报告

本报告是 v51 method-only 路线的最终实验入口。实验由 54 个 pair、3 轮、共 162 个 method cell 组成；method 只负责发现、issue 发布、D/W 裁定和证据审计，正式 validity、relation、hit、FP 与 precision 全部来自独立冻结的 `semantic-judge.two-stage.v3.2`。L 只读取 145 条正式台账，不由 method 或 Judge 生成。

最终结论是：162/162 method cell 与 162/162 Judge 结果均闭合；current 相对 X1v2 的 overall hit@1 为 `253/435` 对 `211/435`，L2 为 `80/117` 对 `46/117`，D2xL2 为 `67/102` 对 `40/102`，semantic precision 为 `92.91%` 对 `80.08%`。固定六 pair 的 current/v27/X1v2 FULL 为 `64/75`、`51/75`、`31/75`。因此 method 达到冻结门，不再基于最终测试集继续调 prompt、谓词或 Judge。

## 1. 冻结身份与评测边界

| 项 | 冻结值 |
|---|---|
| method run commit | `90d1c41ed3c1724de2c5283a5520b863fc307d5c` |
| embedded Judge removal | `4890c1f3172789857c9ef91eb2fc68445583fead` |
| method protocol | `evidence-discovery-typed-flow.v53-method-only` |
| prompt/schema | `evidence-discovery-prompts.v44-method-only` / `sha256:77ca0405...d5a2a` |
| predicate registry | `four-family-19-core.v1` / 19 predicates / `sha256:b456cd91...1959` |
| model/profile | `gpt-5.6-luna` |
| method concurrency | 6 process-isolated pair workers，transport retries = 8，streaming |
| Judge semantic commit | `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5` |
| Judge protocol | `semantic-judge.two-stage.v3.2` / issue #189 + issue #195 |
| Judge prompt hash | `sha256:534330d8...5ba4c` |
| ledger | 145 entries / `sha256:b5a38d3d...d0e36` |

`90d1c41e` 后的 `8f36fbfa` 只修复 method provider retry 行的费用保留，`1d474185` 只修复 composite 对同 commit repair run 的费用聚合；二者不改变已经落盘的 discovery 语义、release reports 或冻结 Judge 裁决。X1v2 少数 repair run 使用 `265d977c` 的 public Agent runtime structured-output 定向修复，但 semantic Judge 代码、protocol、prompt、schema 和 metrics 仍固定为 `05cf0da6`；composite 将其明确记录为 execution erratum，而不是 Judge 语义版本。

## 2. 主要覆盖结果

FULL 才计 hit；PARTIAL 只计 supported coverage；只有 INVALID 才计 semantic FP。`VALID_NOVEL` 是台账外有效报告，不是 hit，也不是 FP。

| 子集 | current hit@1 | X1v2 hit@1 | current hit@3 | X1v2 hit@3 | current hit@all | X1v2 hit@all |
|---|---:|---:|---:|---:|---:|---:|
| overall | 253/435 (58.16%) | 211/435 (48.51%) | 106/145 (73.10%) | 104/145 (71.72%) | 60/145 (41.38%) | 37/145 (25.52%) |
| L2 | 80/117 (68.38%) | 46/117 (39.32%) | 31/39 (79.49%) | 26/39 (66.67%) | 22/39 (56.41%) | 5/39 (12.82%) |
| D2xL2 | 67/102 (65.69%) | 40/102 (39.22%) | 26/34 (76.47%) | 23/34 (67.65%) | 19/34 (55.88%) | 4/34 (11.76%) |

current 的 overall hit@1 高出 `42/435`（+9.66 个百分点），L2 高出 `34/117`（+29.06 个百分点），D2xL2 高出 `27/102`（+26.47 个百分点）。overall hit@3 只高出 2 条，说明 baseline 对“至少偶然发现一次”的已知缺陷已有较广覆盖；current 的主要收益在单轮期望覆盖、L2、三轮稳定命中和更低 INVALID，而不是把最终台账可达边界夸大成大幅 hit@3 提升。

overall supported 为 current `293/435`、X1v2 `244/435`；L2 supported 为 `87/117`、`69/117`；D2xL2 supported 为 `72/102`、`60/102`。

## 3. 三轮分布

| arm/round | FULL | supported | L2 FULL/support | D2xL2 FULL/support | K/N/I | semantic precision | selected Judge cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| current r1 | 88/145 | 104/145 | 28/30 of 39 | 23/25 of 34 | 229/147/28 | 93.07% | $11.201770 |
| current r2 | 81/145 | 89/145 | 26/28 of 39 | 22/23 of 34 | 182/152/20 | 94.35% | $10.194599 |
| current r3 | 84/145 | 100/145 | 26/29 of 39 | 22/24 of 34 | 215/149/34 | 91.46% | $10.483411 |
| X1v2 r1 | 64/145 | 78/145 | 12/23 of 39 | 10/20 of 34 | 85/45/43 | 75.14% | $3.601292 |
| X1v2 r2 | 73/145 | 82/145 | 17/23 of 39 | 15/20 of 34 | 91/45/27 | 83.44% | $3.453036 |
| X1v2 r3 | 74/145 | 84/145 | 17/23 of 39 | 15/20 of 34 | 100/44/32 | 81.82% | $3.738426 |

`selected Judge cost` 只对应最终选入 composite 的结果。current 还有原失败调用 `$0.9391240` 和独立 repair 结果 `$0.8793016`；完整 Judge 支出在 §6 单独报告。

## 4. 报告质量、novel 与聚类

| 指标 | current | X1v2 |
|---|---:|---:|
| raw reports | 1156 | 512 |
| VALID_KNOWN (K) | 626 | 276 |
| VALID_NOVEL (N) | 448 | 134 |
| INVALID / semantic FP (I) | 82 | 102 |
| semantic precision | 92.91% | 80.08% |
| raw root-cause clusters | 1128 | 511 |
| root-cause cluster precision | 93.00% | 80.04% |
| raw-report redundancy | 2.42% | 0.20% |
| cross-round novel clusters | 404 | 132 |
| cross-round cluster precision | 92.72% | 80.00% |

current 发布量是 X1v2 的 2.26 倍，但 INVALID 绝对数仍少 20 条。`448` 是 raw VALID_NOVEL report 数，按 pair-namespaced root-cause key 跨轮去重后为 `404` 个 cluster；它们不能写成 448 个独立新缺陷，也尚未经过人工台账扩充裁定。

## 5. Method 产出与 W2 审计

method run 为 `162/162 completed/eligible`，无 crash、无 diagnostic cell、无半成品，生成 1156 条 release report 与 1422 条 evidence record。evidence record 的确定性分布如下：

| 维度 | 分布 |
|---|---|
| D | D2=1152，D1=142，D0=46，D_UNRESOLVED=82 |
| W | W2=347，W1=1009，W0=66 |

D2/D1 evidence 可进入聚合后的 release reports；D0 和 D_UNRESOLVED 保留审计但不进入正式 hit/FP。347/347 W2 bundle 都包含完整谓词逻辑、精确输入绑定、compiled program/code、hash、真实执行结果、环境、receipt、reason/basis，并通过 Pydantic 与 hash closure。W1 仍可正常发布 issue；谓词不能表达只影响证据等级，不构成发布或 Judge FULL 的硬门。

method-only run 没有产生 `llm/judge`、`judge/*.json`、Judge provider call、Judge cost、hit、FP 或 precision。W2 audit 在 method 阶段只记录 `pending_independent_judge`，正式质量指标由本报告引用的外置 composite 关联。

## 6. 成本、调用与 retry

### 6.1 Method generation

| 项 | 数值 |
|---|---:|
| original reported cost（历史保留） | $6.62169376 |
| corrected formal cost | $6.77501040 |
| X1v2 generation cost | $0.22523328 |
| corrected current/X1v2 ratio | 30.07997042x |
| uncached input | 16,388,498 tokens / $3.27769960 |
| cache read | 15,232,000 tokens / $0.30464000 |
| cache creation | 0 tokens / $0 |
| output | 2,660,559 tokens / $3.19267080 |
| logical calls / provider requests | 646 / 909 |
| billable / provider-error-exempt requests | 890 / 19 |
| schema validation failures（billable） | 244 |

正式费用来自不可变 receipt 的离线更正聚合；不改写原 summary。cache-read 按 `$0.02/M`、普通 input 按 `$0.20/M`、output 按 `$1.20/M` 分类，provider-owned 失败行不计费，schema/non-provider repair 仍计费。本次全量开始前 cache 分类已修正，离线 aggregate 主要补回后来遇到 provider error 时被旧行覆盖的已完成 billable schema-repair 行，因此正式总价比原 summary 净增 `$0.15331664`。最终倍率约 30.08x，未通过删减 discovery lens、reason/basis 或 W2 审计来压成本。

### 6.2 Independent Judge

| arm | logical/provider requests | provider-error attempts | schema failures | APIConnectionError / loop-closed | total incurred cost |
|---|---:|---:|---:|---:|---:|
| current | 1185/1451 | 31 | 253 | 0/0 | $32.81890360 |
| X1v2 | 725/868 | 5 | 144 | 0/0 | $11.45008520 |

Judge cost 与 method generation cost 物理分开，不进入 30.08x generation 倍率。current 原始 r1 `0015` 与 r2 `0029` terminal failure 均保留；独立 repair run 只补对应格，成功格未重跑。最终 composite 选择 162 个唯一 PairJudgeResult，无未恢复失败。`0029` 的 oversized relation arbitration 在 provider 前失败，随后由冻结 deterministic split 恢复，不伪装为 miss/FP。

## 7. 固定六 pair 的局部 v27 参照

v27 只有固定六 pair 在冻结 v3.2 下完成三轮重判，因此它是局部能力参照，不应外推为 v27 的 54x3 正式结果。

| arm | FULL | supported | L2 FULL | K/N/I | semantic precision |
|---|---:|---:|---:|---:|---:|
| current | 64/75 | 69/75 | 31/33 | 147/46/15 | 92.79% |
| v27 | 51/75 | 56/75 | 26/33 | 92/28/68 | 63.83% |
| X1v2 | 31/75 | 41/75 | 17/33 | 36/12/19 | 71.64% |

current 三轮 FULL 为 `22/25`、`20/25`、`22/25`；v27 为 `17/25`、`18/25`、`16/25`。该排序满足“current 与 v27 不出现能力断崖，且整体优于 X1v2”的冻结门，不用于反向调 Judge。

## 8. 逐 pair 结果

`FULL r1/r2/r3` 与 `support r1/r2/r3` 是每轮命中的 expected 数；K/N/I 为三轮 raw report 合计。expected=0 的 pair 仍保留 method/Judge 终态，其报告只能成为 VALID_NOVEL 或 INVALID，不能制造 hit。

| pair | expected | current FULL r1/r2/r3 | current support r1/r2/r3 | current K/N/I | X1v2 FULL r1/r2/r3 | X1v2 support r1/r2/r3 | X1v2 K/N/I |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0000 | 3 | 1/3/2 | 2/3/3 | 10/2/0 | 0/1/2 | 0/2/2 | 4/1/2 |
| 0001 | 2 | 1/0/0 | 1/0/0 | 1/1/0 | 2/1/1 | 2/1/1 | 4/0/0 |
| 0002 | 7 | 2/1/2 | 4/3/4 | 29/3/1 | 2/1/0 | 3/1/0 | 3/0/4 |
| 0003 | 0 | 0/0/0 | 0/0/0 | 0/3/0 | 0/0/0 | 0/0/0 | 0/3/3 |
| 0004 | 3 | 3/1/2 | 3/1/2 | 10/11/0 | 2/0/2 | 2/0/2 | 4/4/4 |
| 0005 | 3 | 3/3/2 | 3/3/3 | 29/11/4 | 0/1/2 | 0/1/2 | 6/0/3 |
| 0006 | 1 | 1/1/1 | 1/1/1 | 5/17/0 | 1/1/1 | 1/1/1 | 3/4/0 |
| 0007 | 3 | 1/0/0 | 2/0/0 | 6/2/1 | 0/1/1 | 0/1/1 | 2/0/7 |
| 0009 | 5 | 5/4/2 | 5/4/4 | 28/35/3 | 2/0/4 | 2/0/4 | 7/5/1 |
| 0010 | 7 | 3/4/4 | 3/5/5 | 10/1/0 | 5/7/6 | 6/7/7 | 18/0/0 |
| 0011 | 2 | 0/0/0 | 0/0/0 | 0/0/1 | 0/1/1 | 2/1/2 | 5/1/0 |
| 0012 | 2 | 0/0/0 | 0/0/0 | 0/2/1 | 1/1/0 | 1/1/0 | 2/1/2 |
| 0013 | 1 | 0/0/0 | 0/0/0 | 0/6/0 | 1/1/1 | 1/1/1 | 9/0/0 |
| 0014 | 5 | 5/5/5 | 5/5/5 | 37/16/1 | 3/3/3 | 3/3/3 | 12/1/2 |
| 0015 | 1 | 0/1/1 | 0/1/1 | 7/10/1 | 0/0/1 | 0/0/1 | 2/2/0 |
| 0016 | 4 | 2/0/0 | 2/0/0 | 2/7/0 | 1/0/0 | 1/0/0 | 1/1/0 |
| 0017 | 2 | 1/2/2 | 1/2/2 | 10/3/1 | 1/0/0 | 1/0/0 | 1/1/1 |
| 0019 | 5 | 5/5/5 | 5/5/5 | 38/31/1 | 1/3/1 | 3/4/1 | 9/3/7 |
| 0020 | 1 | 0/1/0 | 1/1/0 | 2/2/2 | 0/1/1 | 0/1/1 | 4/3/4 |
| 0021 | 0 | 0/0/0 | 0/0/0 | 0/0/2 | 0/0/0 | 0/0/0 | 0/5/0 |
| 0022 | 0 | 0/0/0 | 0/0/0 | 0/2/0 | 0/0/0 | 0/0/0 | 0/7/0 |
| 0023 | 3 | 3/3/3 | 3/3/3 | 16/0/1 | 3/3/0 | 3/3/0 | 4/1/0 |
| 0024 | 6 | 2/1/3 | 3/1/5 | 11/11/2 | 5/5/5 | 5/5/5 | 17/1/0 |
| 0025 | 2 | 2/2/2 | 2/2/2 | 10/4/2 | 2/1/2 | 2/1/2 | 13/1/0 |
| 0026 | 3 | 1/1/1 | 1/1/2 | 4/2/0 | 2/2/3 | 2/2/3 | 7/0/0 |
| 0027 | 2 | 0/0/0 | 0/0/0 | 0/4/0 | 0/0/2 | 0/0/2 | 2/1/6 |
| 0029 | 8 | 7/7/7 | 7/7/7 | 48/23/9 | 1/4/3 | 2/5/7 | 12/1/5 |
| 0030 | 4 | 1/1/2 | 1/1/3 | 6/3/0 | 3/3/2 | 3/3/2 | 10/0/0 |
| 0031 | 0 | 0/0/0 | 0/0/0 | 0/3/0 | 0/0/0 | 0/0/0 | 0/7/1 |
| 0032 | 2 | 1/1/0 | 2/1/0 | 3/2/4 | 0/1/2 | 0/2/2 | 3/3/4 |
| 0033 | 3 | 2/2/3 | 2/2/3 | 13/14/3 | 2/2/2 | 2/2/2 | 7/1/3 |
| 0034 | 7 | 5/4/5 | 6/4/5 | 35/17/3 | 6/6/6 | 7/6/7 | 22/4/3 |
| 0035 | 4 | 4/4/4 | 4/4/4 | 25/8/4 | 2/2/1 | 3/2/1 | 7/3/1 |
| 0036 | 0 | 0/0/0 | 0/0/0 | 0/18/0 | 0/0/0 | 0/0/0 | 0/16/1 |
| 0037 | 1 | 1/1/1 | 1/1/1 | 23/2/0 | 0/1/1 | 1/1/1 | 4/5/1 |
| 0039 | 5 | 3/2/1 | 3/2/2 | 16/34/4 | 1/1/0 | 2/1/0 | 2/3/0 |
| 0040 | 3 | 0/1/0 | 1/1/0 | 3/9/2 | 1/1/0 | 1/1/0 | 2/3/1 |
| 0041 | 0 | 0/0/0 | 0/0/0 | 0/3/0 | 0/0/0 | 0/0/0 | 0/8/0 |
| 0042 | 1 | 1/1/1 | 1/1/1 | 5/0/2 | 1/1/0 | 1/1/0 | 3/1/0 |
| 0043 | 2 | 1/1/1 | 2/1/1 | 19/12/0 | 2/1/1 | 2/1/1 | 6/0/1 |
| 0044 | 2 | 1/1/1 | 1/1/1 | 10/18/2 | 0/1/1 | 0/1/1 | 2/1/1 |
| 0045 | 1 | 1/1/1 | 1/1/1 | 5/7/0 | 0/1/1 | 0/1/1 | 3/3/0 |
| 0046 | 4 | 2/2/3 | 4/4/4 | 18/1/0 | 1/1/1 | 2/1/1 | 5/3/5 |
| 0047 | 3 | 2/3/2 | 3/3/3 | 21/0/1 | 2/1/2 | 2/2/2 | 10/1/0 |
| 0049 | 4 | 3/3/4 | 4/4/4 | 27/32/12 | 2/3/2 | 2/4/3 | 9/2/8 |
| 0050 | 2 | 2/1/2 | 2/2/2 | 7/3/1 | 0/0/1 | 0/0/1 | 1/0/0 |
| 0051 | 0 | 0/0/0 | 0/0/0 | 0/1/5 | 0/0/0 | 0/0/0 | 0/6/0 |
| 0052 | 0 | 0/0/0 | 0/0/0 | 0/2/2 | 0/0/0 | 0/0/0 | 0/4/0 |
| 0053 | 3 | 3/3/3 | 3/3/3 | 30/3/1 | 1/3/1 | 2/3/2 | 4/0/4 |
| 0054 | 3 | 0/2/1 | 1/3/1 | 5/14/1 | 0/0/1 | 0/2/1 | 3/2/4 |
| 0055 | 1 | 1/0/1 | 1/0/1 | 4/6/1 | 0/1/1 | 0/1/1 | 4/3/1 |
| 0056 | 3 | 1/2/0 | 1/2/1 | 4/5/0 | 2/2/2 | 2/2/2 | 6/1/3 |
| 0057 | 2 | 2/0/1 | 2/0/1 | 13/5/1 | 1/1/2 | 1/1/2 | 4/2/0 |
| 0059 | 4 | 3/0/3 | 4/0/4 | 21/17/0 | 2/2/2 | 3/3/3 | 8/5/9 |

## 9. 完整性、自检与复现

机器事实源：

- method: `runs/paper1/evidence-discovery-method-only-54x3-final-90d1c41e/90d1c41e000000000000000000000162`
- corrected cost: `runs/paper1/evidence-discovery-corrected-cost-v1/90d1c41e-54x3-corrected-cost.json`
- current Judge composite: `runs/paper1/semantic-judge-v3.2-current-54x3-composite-05cf0da6/composite-summary.json`
- X1v2 Judge composite: `runs/paper1/semantic-judge-v3.2-x1v2-54x3-composite-265d977c/composite-summary.json`
- v27 six-pair composite: `runs/paper1/semantic-judge-v3.2-v27-six-x3-composite-05cf0da6/composite-summary.json`

对应 SHA-256 依次为 method manifest `47bf874c...dd640`、method summary `886fba61...bfed`、corrected cost `85ecf2d1...f2e44`、current composite `4f3abe92...6d03`、X1v2 composite `e74ef496...a2e9`、v27 composite `53297a1b...045d`。current composite 的确定性重建逐字节一致。

最终自检确认：NL、PlantUML STM、FCSTM STM 与既有 inspect-result artifact 进入各自正确阶段；正式 backend 不 import/use Python `inspect`；运行继续复用 public `respond`、LangGraph、`utils.agent` 和 `utils.llm`；D 由 method 裁定，W 由确定性证据链派生，L 只来自台账；provider error 原地重试且免计费，schema/non-provider repair 计费；commit、registry、prompt/schema、input、artifact closure 与 resume identity 均有 hash；162 个 method cell 和 162 个 Judge 结果无缺格。

最终 provider-free gate 为 evidence-discovery `158 passed`、semantic-judge `79 passed`、公共 runtime/pricing `181 passed`；compileall、JSON 解析、artifact hash、diff check、embedded-Judge/production-inspect 扫描均通过。本次收口没有 Python diff。额外执行的 repository-wide Ruff 报告 125 条既有规则债务，均位于本轮未修改代码；因此按冻结计划采用 changed-file/scoped Ruff gate，不借文档收尾重排生产代码，也不把全仓 Ruff 误写成零告警。

从 paper 工作区复现新的同协议运行可使用：

```bash
python -m pipeline.evidence_discovery.cli \
  --report-root pipeline/representation/reports/llms_emp_r45_java_60 \
  --output-dir <new-method-output-dir> \
  --run-id <new-32-hex-run-id> \
  --profile gpt-5.6-luna --rounds 3 --workers 6 \
  --transport-retries 8 --allow-live --allow-full-live

python -m pipeline.semantic_judge.cli \
  --report-root pipeline/representation/reports/llms_emp_r45_java_60 \
  --ledger discover_matrix/ledger_v2/ledger.json \
  --source-format evidence_discovery_release \
  --source-root <method-run-root> \
  --output-dir <new-judge-output-dir> --run-id <new-judge-run-id> \
  --profile gpt-5.6-luna --round 1 --workers 4 \
  --transport-retries 8 --allow-live
```

Judge 命令需对 round 1/2/3 分别使用全新 run identity，再由 `pipeline.semantic_judge.composite` 对 immutable source runs 做闭包聚合。历史 artifact 不得覆盖或混入新的 run identity。

## 10. 非阻塞限制与冻结决定

1. v27 在冻结 v3.2 下只有六 pair x3，不能宣称 current 在 54x3 上全面优于 v27。
2. 448 条 raw VALID_NOVEL 仍需后续人工研究，不等于 448 个独立根因；现有 404 个跨轮 cluster 也只是确定性语义键下的问题形状。
3. current overall hit@3 只比 X1v2 高 2/145；论文应把显著收益放在 hit@1、L2、D2xL2、hit@all 和 precision，不夸大能力边界。
4. 两个原始 Judge terminal failure 与 82 条 D_UNRESOLVED 均完整保留；前者已独立补齐，后者是 method 审计状态而非缺格。
5. LLM Judge 仍有双读分歧与 schema repair 成本；本实验通过冻结 prompt/schema、完整 reason/basis、后端闭合和逐条 artifact 降低而非消除该威胁。

这些限制不构成 crash、数据缺失、协议混用或系统性能力断崖。v51 method 与 v3.2 Judge 因而在本轮正式冻结；后续工作应进入论文分析和人工 novel 审计，不再使用最终 54x3 测试集反向调优。
