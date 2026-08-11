# discover 矩阵：审计工具与文档导航

本目录是 paper1「STM 缺陷发现」矩阵实验的**审计工具 + 口径文档**所在地。本文件是**唯一入口**：所有 `.md` 都能从这里一跳或两跳到达。

从 `runs/paper1/audit-20260727-claudecode/` 迁来。

## 为什么放在这里

`runs/` 只存运行产物，整个目录被 gitignore。这些脚本是**审计工具**，不是产物：它们决定预期缺陷的命中判据，也就是矩阵实验的头号指标怎么算。放在 `runs/` 里的直接后果已经发生过一次——2026-07-29 重装系统后，`build_gist.py` 因为在加 ignore 之前就被跟踪而幸存，它依赖的 `audit_v4.py` 从未被提交，直接丢失，只能对着已发布的 matrix-v11 审计包反推重建。

---

## 0. 按任务找文件（三条最常用的路）

| 我要做的事 | 先读 |
| :-- | :-- |
| 判一条产出算不算命中 | [docs/protocol/hit_criterion.md](./docs/protocol/hit_criterion.md) |
| 判一条未匹配台账的产出属哪一类多报 | [docs/protocol/unexpected_taxonomy.md](./docs/protocol/unexpected_taxonomy.md) → [docs/findings/representation_debt.md](./docs/findings/representation_debt.md) |
| 看 v46 全量矩阵的结论 | [v46/README.md](./v46/README.md)（**v46 的唯一入口**） |
| 引用召回率 / 分母 | [docs/protocol/ground_truth_limitations.md](./docs/protocol/ground_truth_limitations.md) + [docs/protocol/nl_scope_rule.md](./docs/protocol/nl_scope_rule.md) |
| 组织一次人工判定 | [docs/judges/](./docs/judges/)（**只有这个目录里的文件可以交给判定者**） |
| 查某条 prompt 规则的由来 | [docs/protocol/rule_provenance.md](./docs/protocol/rule_provenance.md) + [docs/generations/v23/motive_audit.md](./docs/generations/v23/motive_audit.md) |

## 1. 目录结构：四类文档，改动代价不同

```
discover_matrix/
├── README.md            ← 本文件，唯一入口
├── docs/
│   ├── protocol/        永久口径 —— 改它 = 改研究规则，必须同步改报告与复算
│   │   ├── rules/       仍在生效的单条 prompt 规则（带引入动机与通用性证据）
│   │   └── rulings/     仍在生效的单条分母裁定
│   ├── judges/          判定者运行材料 —— 物理隔离是它存在的理由，见 §3
│   ├── findings/        跨代次长期有效的发现
│   │   └── predicates/  谓词侧：缺陷登记 + provenance 观察
│   └── generations/     按代次归档（v21…v25、v40…v45）—— 历史，不被正文引用但删不得
├── v46/                 ⛔ 本轮实验的唯一入口，不重组、含大量派生物
├── manual_review/  onepass_sample/  blind_sample/  verdicts/  telemetry/   冻结证据，只读
└── *.py *.sh            审计工具与测试
```

**四类的判据**：`protocol` 是「现在生效、改它要改结论」；`judges` 是「会被逐字交给外部判定者」；`findings` 是「跨代次成立的事实」；`generations` 是「某一代次的历史记录，含事前登记」。一份文档同时像两类时，按**它现在是否被援引来做判定**归 `protocol`（是）或 `generations`（否）。

## 2. `docs/protocol/` —— 永久口径

| 文件 | 管什么 |
| :-- | :-- |
| [hit_criterion.md](./docs/protocol/hit_criterion.md) | 什么算命中（§3 的四种语义同一形态是闭集；§4.5 双读法并列义务；§7 禁止用重建版台账算命中） |
| [verdict_methodology.md](./docs/protocol/verdict_methodology.md) | 判定分层（A/B/C 层）与各层的可采信范围 |
| [nl_scope_rule.md](./docs/protocol/nl_scope_rule.md) | `00x8` 六个 pair 永久越界的判据（只读 `nl.txt` 与先验，与运行结果无关） |
| [method_provenance_policy.md](./docs/protocol/method_provenance_policy.md) | 不设 hold-out 的口径，以及方法由来该怎么陈述 |
| [ground_truth_limitations.md](./docs/protocol/ground_truth_limitations.md) | 分母**系统性不覆盖**什么，每处缺口是边界还是欠账 |
| [manual_review_spec.md](./docs/protocol/manual_review_spec.md) | 人工逐条差异判定的规范（含范围外的硬规则、比较级断言两条硬约束） |
| [unexpected_taxonomy.md](./docs/protocol/unexpected_taxonomy.md) | 多报侧五类裁定的定义与判定流程（**没有第六类，也不设「待定」**） |
| [fused_event_policy.md](./docs/protocol/fused_event_policy.md) | 合并事件的既定裁定（断言阶段必须接受，L379 给出许可条件） |
| [rule_provenance.md](./docs/protocol/rule_provenance.md) | 每条进入 prompt / gate 的规则的引入动机与领域出处 |
| [rules/conditional_activation.md](./docs/protocol/rules/conditional_activation.md) | 一条仍在生效的 prompt 规则，附通用性证据 |
| [rulings/wellformedness_attribution.md](./docs/protocol/rulings/wellformedness_attribution.md) | 仍在生效的分母归属裁定 |

⚠️ `rulings/wellformedness_attribution.md`（**生效中的裁定**）与 [docs/generations/v25/wellformedness_axioms.md](./docs/generations/v25/wellformedness_axioms.md)（**未冻结的规则草案，其规范依据已被 UML 核对推翻**）是两份不同性质的文件，**不要混用、不要合并** ——合并会让死提案和活口径共享同一个标题。

## 3. `docs/judges/` —— 判定者运行材料

⛔ **这个目录存在的全部理由是物理隔离防泄漏。** 实测：靠「读到此为止」这类**约定**做隔离，合规率 **0/2**；把内容**拆成不同文件**后 **2/2**。见 [docs/generations/v25/instrument_ablation.md](./docs/generations/v25/instrument_ablation.md) §二.1。

| 文件 | 交不交给判定者 |
| :-- | :-- |
| [judges/hit_criterion_for_judges.md](./docs/judges/hit_criterion_for_judges.md) | ✅ 交（实例**全部合成**，无语料内容） |
| [judges/onepass_instructions.md](./docs/judges/onepass_instructions.md) | ✅ 指令段（第一个 `## ⛔` 之前）交 |
| [judges/blind_judge_prompt.md](./docs/judges/blind_judge_prompt.md) | ✅ 指令段交 |
| [judges/onepass_maintenance.md](./docs/judges/onepass_maintenance.md) | ⛔ **永不交** —— 含往轮具体判定 |
| [docs/protocol/hit_criterion.md](./docs/protocol/hit_criterion.md) | ⛔ **永不交** —— 维护版本，含真实语料实例与命中裁定 |

`hit_criterion.md` 与 `hit_criterion_for_judges.md` **必须保持两份**：后者存在的唯一目的就是让前者的真实语料实例不进入判定者视野。合并 = 把泄漏装回去，且会让 [test_judge_materials_carry_no_verdicts.py](./test_judge_materials_carry_no_verdicts.py) 直接红。

该测试机械扫描 `judges/` 下三份材料里的往轮判定指纹。⚠️ 它对缺文件用 `pytest.skip` 处理，所以**改动路径后必须用 `pytest -rs` 确认 skip 数为 0** —— 否则检查会静默跳过、看起来全绿。

## 4. `docs/findings/` —— 跨代次长期有效的发现

| 文件 | 内容 |
| :-- | :-- |
| [findings/representation_debt.md](./docs/findings/representation_debt.md) | 表示债务：R4.5 编译（PlantUML → FCSTM）的信息损失，**引用多报数字前必读** |
| [findings/predicates/defects_registered.md](./docs/findings/predicates/defects_registered.md) | 谓词求值实现与断言构造的缺陷登记（P-0…P-4，按「已实施 / 未实施」两栏） |
| [findings/predicates/observations.md](./docs/findings/predicates/observations.md) | 谓词行为的 provenance 观察（`predicate_api.py` 的注释引它作依据） |

这三份加上 [docs/generations/v24/predicate_bottleneck.md](./docs/generations/v24/predicate_bottleneck.md) 是**三种不同对象**，都不要合并：`predicate_bottleneck` 是 v23/v24 的诊断叙事；`observations` 是 provenance 卫生件；`defects_registered` 是 v46 起的活登记。

## 5. `docs/generations/` —— 按代次归档

事前登记与历代分析结果不被正文引用，但**删不得**——事前登记的全部价值来自它写在运行之前。

| 代次 | 文件 |
| :-- | :-- |
| v21 | [preregistered_calibre.md](./docs/generations/v21/preregistered_calibre.md)（判定口径的事前登记；`build_comment.py` / `capability.py` 都引它） |
| v22 | [progress.md](./docs/generations/v22/progress.md) ｜ [backlog.md](./docs/generations/v22/backlog.md) ｜ [blind_readjudication.md](./docs/generations/v22/blind_readjudication.md) ｜ [denominator_exhaustion.md](./docs/generations/v22/denominator_exhaustion.md)（⛔ hold-out 时代，结论已作废，仅供追溯） |
| v23 | [README.md](./docs/generations/v23/README.md)（报告骨架）｜ [motive_audit.md](./docs/generations/v23/motive_audit.md)（引入动机溯源，泄漏审查材料）｜ [overreport_adjudication.md](./docs/generations/v23/overreport_adjudication.md)（v22 数据的多报核验） |
| v24 | [report_determined.md](./docs/generations/v24/report_determined.md)（与判定无关的已定部分）｜ [predicate_bottleneck.md](./docs/generations/v24/predicate_bottleneck.md) |
| v25 | [instrument_ablation.md](./docs/generations/v25/instrument_ablation.md)（**预登记 + 结果合并件**）｜ [paths_feasibility.md](./docs/generations/v25/paths_feasibility.md) ｜ [synthesized_placeholder_proposal.md](./docs/generations/v25/synthesized_placeholder_proposal.md) ｜ [coverage_levers.md](./docs/generations/v25/coverage_levers.md) ｜ [obligation_source_gap.md](./docs/generations/v25/obligation_source_gap.md)（`wellformedness` 漏检的构造性根因）｜ [wellformedness_axioms.md](./docs/generations/v25/wellformedness_axioms.md)（⛔ 未冻结草案）｜ [retired_onepass_prompt.md](./docs/generations/v25/retired_onepass_prompt.md)（⛔ 已退役） |
| v40–v45 | [v40](./docs/generations/v40/preregistered.md) ｜ [v41](./docs/generations/v41/preregistered.md) ｜ [v43](./docs/generations/v43/preregistered.md) ｜ [v44](./docs/generations/v44/preregistered.md) ｜ [v45](./docs/generations/v45/preregistered.md) —— 各代次事前登记（判据、达标档位、回归红旗） |
| v46 | [v46/preregistered.md](./v46/preregistered.md)，其余材料见 [v46/README.md](./v46/README.md) |

⛔ 没有 v42：该代次未产出事前登记文件。

⛔ 纯施工台账（进度、试跑计划、变更清单、已撤销提案）不入库——它们属 GitHub PR / issue，见 [CLAUDE.md](../../../CLAUDE.md) §9。

---

## 6. 先读裁决原则与已知缺口

[docs/protocol/hit_criterion.md](./docs/protocol/hit_criterion.md) 定义什么算命中；[docs/protocol/ground_truth_limitations.md](./docs/protocol/ground_truth_limitations.md) 记录分母**系统性不覆盖**什么，以及每处缺口是问题定义边界还是待补欠账——引用召回率前必须读后者，否则会把「问题定义不做的类」误报成「方法没检出」。

引用任何命中数字前，先确认用的是 frozen ledger 而非 `expected_issues_reconstructed.json` ——后者仅覆盖 4 个 pair，且已知把 `EXP-0029-SH-001` 写严，据它算出的命中率是错的。

⛔ **引用任何多报 / over-report 数字前，必读 [docs/findings/representation_debt.md](./docs/findings/representation_debt.md)。** v46 实测：未匹配台账的 **288 个同质簇（去重到 124 处不同内容）**里，**134 簇 / 30 处（条目 46.5% / 去重 24.2%）不是模型缺陷，而是我们自己 R4.5 编译（PlantUML → FCSTM）的信息损失**——作者在 `stm0.puml` 里已逐字写全，`model.fcstm` 装不下才被压平，且压平已由 `fcstm_meta.json` 的债务码如实登记。**把它们计入多报会同时高估模型的乱报程度、又掩盖编译链的问题。** 该文件给出定义、三条操作化判据、实例与论文表述口径。

⚠️ **条目份额与去重份额不可互换**，引用时必须写清用的是哪一套分母；两套数字的机器产地是 [v46/unexpected_tables.md](./v46/unexpected_tables.md) 表 1。同一批产出的净增量（真实台账漏记）**只有 2 条**（`0014-4` 与 `0010-2`）。

⚠️ 判定表示债务必须回读**作者源 `stm0.puml`**，只读 `model.fcstm` 必然看不出来—— v46 的**九个**判定组全部做了回读，并各自产出表示债务裁定（20/14/19/17/16/19/11/8/10 条）——差异在留痕详略，不在是否回读。

## 7. 脚本

- `build_gist.py <matrix_dir> <out_dir>` —— 读一个矩阵运行目录，产出 `readable/` 与 `audit/` 两套 bundle 以及逐格表格。命中判据在 `expected_verdicts()`。
- `audit_v4.py` —— `build_gist.py` 的两个依赖：`_walk`（按键名递归取值，因为不同节点把同名字段写在不同深度）与 `_segment_macro_sources`（从 frozen trace 的排除表反推被转换器拆成多段的源迁移）。
- `launch_cells_serial.sh` —— 串行启动单元格的历史脚本，保留作参考。
- `rebuild_unexpected.py` —— 从 `v46/unexpected_verdicts/G*.jsonl` 一键重建 v46 的派生 md（`v46/unexpected_evidence.md`、`v46/unexpected_tables.md`）。`--check` 可用于 CI。⚠️ 那两份是**派生物**，改它们必须改本脚本。

## 8. 预期缺陷台账：原件，已校验

命中判据读 `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`。当前装着的是**原件**：370994 字节，SHA-256 `03d8756650c079229dacb7fc2d7700ca98fda44f3c4648fd308e4f8e24ac955e`，与 issue #166 正文「机器总账 SHA-256」逐字符一致；来源记录见同目录 `PROVENANCE.md`，找回过程见 [docs/protocol/hit_criterion.md](./docs/protocol/hit_criterion.md) §7。

复核命令：

```bash
L=../../../.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json
wc -c "$L" && sha256sum "$L"
```

- 该文件**不被 git 跟踪**（体积与来源所限），所以每台机器都要自己装一份并核 SHA。它丢失过一次（2026-07-29 重装），因此这条校验不是形式主义。
- `_expected_ledger_path()` 优先取原件；实际所用来源写入每个审计制品的 `expected_ledger_provenance` 字段——命中率是头号数字，读者必须能自己看出它建立在什么之上，而不是听谁说。
- `expected_issues_reconstructed.json` 与 `calibration_matrix_v11.json` 是原件缺席时的退路（覆盖 8 格矩阵用到的 4 对），`test_ledger_reconstruction.py` 要求它在 matrix-v11 上复现该台账给出的 12 条判定、其中 10 条命中。**v46 未使用退路**。

## 9. v46 全量矩阵（2026-08）

⛔ **v46 的全部材料集中在 [v46/](./v46/)，唯一入口是 [v46/README.md](./v46/README.md)** ——核心结论、覆盖侧与多报侧统计都在那里，细节引向各 sub md。

跨代次通用的裁定口径在 `docs/`：[docs/protocol/unexpected_taxonomy.md](./docs/protocol/unexpected_taxonomy.md)（多报侧五类定义与判定流程，**判任何一条未匹配产出前必读**）、[docs/findings/representation_debt.md](./docs/findings/representation_debt.md)（表示债务，**引用多报数字前必读**）、[docs/findings/predicates/defects_registered.md](./docs/findings/predicates/defects_registered.md)（测量链侧缺陷，已实施 / 未实施两栏；**「谓词词表冻结」不等于「谓词实现冻结」**，该文件写清了分界）。

## 10. ⚠️ 冻结证据件仍指向旧文件名

`verdicts/*.json`、`onepass_sample/**/*.json`、`manual_review/**`（含 `rescope.json` 三十余处）、`v46/verdicts/*.json`、`v46/unexpected_verdicts/*.jsonl` 是**判定证据**，本次重组**没有改动**它们。因此它们里面出现的 `HIT_CRITERION.md`、`MANUAL_REVIEW_SPEC.md`、`GROUND_TRUTH_LIMITATIONS.md` 等**是当时的文件名**，请按本文件 §2–§5 的表格换算到新路径。改动它们等于篡改证据链，所以宁可留一份需要换算的旧名。

旧名 → 新路径的完整对照：

| 旧文件名（重组前，平铺在本目录） | 现在的位置 |
| :-- | :-- |
| `HIT_CRITERION.md` | [docs/protocol/hit_criterion.md](./docs/protocol/hit_criterion.md) |
| `VERDICT_METHODOLOGY.md` | [docs/protocol/verdict_methodology.md](./docs/protocol/verdict_methodology.md) |
| `NL_SCOPE_RULE.md` | [docs/protocol/nl_scope_rule.md](./docs/protocol/nl_scope_rule.md) |
| `METHOD_PROVENANCE_POLICY.md` | [docs/protocol/method_provenance_policy.md](./docs/protocol/method_provenance_policy.md) |
| `GROUND_TRUTH_LIMITATIONS.md` | [docs/protocol/ground_truth_limitations.md](./docs/protocol/ground_truth_limitations.md) |
| `MANUAL_REVIEW_SPEC.md` | [docs/protocol/manual_review_spec.md](./docs/protocol/manual_review_spec.md) |
| `UNEXPECTED_TAXONOMY.md` | [docs/protocol/unexpected_taxonomy.md](./docs/protocol/unexpected_taxonomy.md) |
| `FUSED_EVENT_POLICY.md` | [docs/protocol/fused_event_policy.md](./docs/protocol/fused_event_policy.md) |
| `RULE_PROVENANCE.md` | [docs/protocol/rule_provenance.md](./docs/protocol/rule_provenance.md) |
| `CONDITIONAL_ACTIVATION_RULE.md` | [docs/protocol/rules/conditional_activation.md](./docs/protocol/rules/conditional_activation.md) |
| `WELLFORMEDNESS_ATTRIBUTION_RULING.md` | [docs/protocol/rulings/wellformedness_attribution.md](./docs/protocol/rulings/wellformedness_attribution.md) |
| `HIT_CRITERION_FOR_JUDGES.md` | [docs/judges/hit_criterion_for_judges.md](./docs/judges/hit_criterion_for_judges.md) |
| `ONEPASS_JUDGE_INSTRUCTIONS.md` | [docs/judges/onepass_instructions.md](./docs/judges/onepass_instructions.md) |
| `ONEPASS_JUDGE_MAINTENANCE.md` | [docs/judges/onepass_maintenance.md](./docs/judges/onepass_maintenance.md) |
| `BLIND_JUDGE_PROMPT.md` | [docs/judges/blind_judge_prompt.md](./docs/judges/blind_judge_prompt.md) |
| `REPRESENTATION_DEBT.md` | [docs/findings/representation_debt.md](./docs/findings/representation_debt.md) |
| `PREDICATE_DEFECTS_REGISTERED.md` | [docs/findings/predicates/defects_registered.md](./docs/findings/predicates/defects_registered.md) |
| `OCCUPANCY_HORIZON_BUG.md` | **已合并** → [docs/findings/predicates/defects_registered.md](./docs/findings/predicates/defects_registered.md) §P-0 |
| `PREDICATE_OBSERVATIONS.md` | [docs/findings/predicates/observations.md](./docs/findings/predicates/observations.md) |
| `V21_PREREGISTERED_CALIBRE.md` | [docs/generations/v21/preregistered_calibre.md](./docs/generations/v21/preregistered_calibre.md) |
| `V22_PROGRESS.md` | [docs/generations/v22/progress.md](./docs/generations/v22/progress.md) |
| `POST_V22_BACKLOG.md` | [docs/generations/v22/backlog.md](./docs/generations/v22/backlog.md) |
| `BLIND_READJUDICATION.md` | [docs/generations/v22/blind_readjudication.md](./docs/generations/v22/blind_readjudication.md) |
| `DENOMINATOR_EXHAUSTION.md` | [docs/generations/v22/denominator_exhaustion.md](./docs/generations/v22/denominator_exhaustion.md) |
| `V23_REPORT_SKELETON.md` | [docs/generations/v23/README.md](./docs/generations/v23/README.md) |
| `V23_MOTIVE_AUDIT.md` | [docs/generations/v23/motive_audit.md](./docs/generations/v23/motive_audit.md) |
| `OVERREPORT_ADJUDICATION_V23.md` | [docs/generations/v23/overreport_adjudication.md](./docs/generations/v23/overreport_adjudication.md) |
| `V24_REPORT_DETERMINED.md` | [docs/generations/v24/report_determined.md](./docs/generations/v24/report_determined.md) |
| `PREDICATE_BOTTLENECK.md` | [docs/generations/v24/predicate_bottleneck.md](./docs/generations/v24/predicate_bottleneck.md) |
| `V25_INSTRUMENT_ABLATION_PREREG.md` + `V25_ABLATION_RESULT.md` | **已合并** → [docs/generations/v25/instrument_ablation.md](./docs/generations/v25/instrument_ablation.md) |
| `V25_PATHS_FEASIBILITY.md` | [docs/generations/v25/paths_feasibility.md](./docs/generations/v25/paths_feasibility.md) |
| `V25_SYNTHESIZED_PLACEHOLDER_PROPOSAL.md` | [docs/generations/v25/synthesized_placeholder_proposal.md](./docs/generations/v25/synthesized_placeholder_proposal.md) |
| `COVERAGE_LEVERS.md` | [docs/generations/v25/coverage_levers.md](./docs/generations/v25/coverage_levers.md) |
| `OBLIGATION_SOURCE_GAP.md` | [docs/generations/v25/obligation_source_gap.md](./docs/generations/v25/obligation_source_gap.md) |
| `WELLFORMEDNESS_AXIOMS.md` | [docs/generations/v25/wellformedness_axioms.md](./docs/generations/v25/wellformedness_axioms.md) |
| `ONEPASS_JUDGE_PROMPT.md` | **已退役** → [docs/generations/v25/retired_onepass_prompt.md](./docs/generations/v25/retired_onepass_prompt.md) |
| `V40_PREREGISTERED.md` … `V45_PREREGISTERED.md` | `docs/generations/v40/preregistered.md` … `v45/preregistered.md` |
