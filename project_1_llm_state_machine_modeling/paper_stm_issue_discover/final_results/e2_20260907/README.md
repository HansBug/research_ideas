# E2：冻结判定与离线复算

本目录按 backbone 保存完整的双臂结果。每款模型必须包含 baseline/ours 各 54 pair × 3 round，即 **324 个唯一格**；只有完成两读、必要仲裁和全部报告核销的完整模型组才能归档。实验规则、模型角色、渠道变更及传输恢复见[事前登记与追加授权](../../discover_matrix/docs/generations/e2_20260907/preregistered.md)。

结果解释、三模型配对指标、历史 `gpt-5.6-luna` main/baseline、两种 precision 定义、并发调整和已知限制统一见[E2 综合结果报告：Luna 历史主线与三款 backbone 双臂实验](../../reports/2026-09-08-e2-three-backbone-results.md)。本目录只承载按模型拆分的机器归档，不再维护第二份人类结果表。

历史 Luna 只读引用 [canonical v61](../v61_source_divergence_vs_x1v2_baseline/README.md)，不属于本目录的新生成量。新三款采用 12 谓词，历史 Luna 保留原 19 谓词以及原运行日期、渠道和版本；同 backbone 的双臂差值与跨 backbone 的描述性比较必须区分。

## 文件约定

| 文件 | 内容与边界 |
| --- | --- |
| `模型/cells.json` | 逐格阶段状态、D 未闭合义务、来源 hash、发布报告及最终判定、expected-round、谓词回执与裁定审计摘要；不是原始 prompt/SSE |
| `模型/verification.json` | 从原生生成与 judge 原件核验出的逐格报告数、expected 数、两读/仲裁统计及结果来源 hash |
| `模型/statistics.json` | K/N/I、precision、FULL hit、L0/L1/L2、严格 D1/D2、配对差值、9 簇 bootstrap、逐簇留出及获得/丢失命中定位 |
| `模型/evidence.json` | 候选、执行回执与发布报告分别计数；不把修订或 pass 回执当作新缺陷 |
| [luna_history.json](./luna_history.json) | 324 个历史裁定来源 hash、只读核验记录及同口径配对复算；没有新增 Luna 调用 |
| [input_snapshot.json](./input_snapshot.json) | 首次运行前的输入、依赖、配置与 prompt/schema 身份；不是后续渠道变更后的最终 profile 快照 |
| [sources.json](./sources.json) | 后续 judge 渠道变更、未采用的失败来源、原始备份摘要与已知记录缺口 |
| [archive_manifest.json](./archive_manifest.json) | 本目录所列紧凑 JSON 的字节数及 SHA-256 |
| [raw/](./raw/) | 逐格生成与 Luna 裁定 JSON 原件；每模型 324 格、source/judge 各一份 |

`source` 和 `judge_source` 是本地 ignored `runs/paper1/e2_20260907/` 下的相对路径，便于取得原件后定位；它们不是本目录附带的文件链接。原始记录另有私有远端备份，清单 hash 和数量见来源摘要。fresh clone 可以复算冻结判定的算术，不能据此声称已附带全部请求、独立语义重裁或 API 随机重现证据。

`raw/` 提供上述 648 个 source/judge 引用在仓库内的 JSON 原件副本（共 1944 个文件、1,666,325,086 bytes），因此不需要本地 runs 即可查阅逐格阶段输出、报告、诊断、两读和仲裁。它不包含逐调用 wire/SSE 或私有凭据；这些仍按报告说明从本地 ignored runs 或受限备份取得。

## 复验

从仓库根执行，不需要凭据、网络或 GPU：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --check-counterexamples
```

默认要求 Sonnet、Qwen、Muse 三组全部存在且完整；缺文件或缺格直接失败，不跳过。单独审阅一个完整模型组可显式添加 `--model sonnet`、`--model qwen` 或 `--model muse`，单组通过不等于 E2 全量通过。

入口使用标准库并复用 [A1 算术](../../discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py)。它检查归档 hash、台账 hash、324 个唯一格、每臂 435 个 expected-round、报告与原生核销记录的数量一致、完整阶段状态、FULL/PARTIAL 集合、所有保存指标、证据分母、人工确认数、仲裁/恢复计数和 14 个损坏反例。另逐一核对324份canonical Luna裁定原件的hash并重算其配对指标。它不重新判断某条报告语义上是否有效；原件级的两读/仲裁检查已在导出前执行，紧凑核销记录保存其结果。

## 解释纪律

`hit@1` 是三轮 expected-round 命中比例，`hit@3` 是至少一轮命中，`hit@all` 是三轮全部命中。N 是台账外有效**报告数**，不能解释为独立新缺陷数。配对 bootstrap 同步重采样 9 个 NL 簇，每次保留簇内六个制品、三轮和两臂，10,000 次、seed=20260907；小簇数及区间跨零均需如实解释。

正常证据降级、失败后恢复和未采用失败原件分别记录。本轮新增人工确认数为 **0**；历史复核元数据中的该计数也仅限本轮，不覆盖历史人工作业记录。自动 Luna 裁定与人工确认不是同一件事。W1/W2、来源归因或执行回执本身不证明有效性，也不单独证明谓词降低幻觉的因果机制。
