# E2 综合结果报告：Luna 历史主线与三款 backbone 双臂实验

> 本文件是 PR #208 的唯一人类可读结果入口。它合并本轮三款新增 backbone 的全量结果，以及历史 `gpt-5.6-luna` 主线的 main/ours 与 baseline；逐格机器记录仍按模型保存在 [`final_results/e2_20260907/`](../final_results/e2_20260907/)。正文中的 `[src-*]`、`[clm-*]`、`[cmd-*]` 是文末审计附录中的稳定引用键。

核验日期：2026-09-09。E2 新增 Claude Sonnet 5、Qwen3.8-27B、Muse Glimmer-30B 三个 backbone；每个 backbone 的 `ours` 和 `baseline` 各为 54 个 pair × 3 round = 162 个格，合计 972 个新格。`gpt-5.6-luna` 不在本轮重新生成或重新裁定，使用 v61 已冻结的 324 个历史裁定作为只读主线参照。[src-protocol] [src-luna-history] [clm-scope]

## 1. 研究问题与范围

E2 的主要效应是同一个 backbone 内 `ours - baseline` 的配对差值：加入既定 FCSTM、仿真/形式化执行和谓词后，错误发现与证据质量是否改善。模型之间不是严格的单因素比较，因为模型族、渠道、推理档位、上下文设置和历史日期不同；报告不按报告条数给模型排序，也不把本轮结果写成四款模型的 SOTA 排名。[src-protocol] [clm-analysis]

每个格保留完整阶段状态、报告与 expected 集合、schema 修正、D 阶段诊断、usage、来源 hash、两读及必要仲裁结果。`K/N/I`、precision 和 hit 指标均由 145 条冻结台账离线复算；零发现、证据降级或一次传输恢复都不会被删失，也不自动等同模型失败。[src-e2-stats] [clm-eligibility]

## 2. 实验身份与固定配置

### 2.1 模型、profile 与部署

| 角色 | 精确请求 model ID / revision | adapter 与结构化路径 | context / 输出预算 | 推理与采样档位 |
| --- | --- | --- | ---: | --- |
| 历史 main `ours` / `gpt-5.6-luna` | `gpt-5.6-luna`；托管渠道回报 ID，未取得独立上游 revision | `openai-responses`；Responses function tool | 历史 profile 1,050,000 / 128,000；历史生成结果只读 | v61 原配置；19 predicates |
| 历史 `X1v2 baseline` / `gpt-5.6-luna` | 同上 | 同上 | 同上 | v61 原配置；19 predicates |
| Sonnet 5 | `claude-sonnet-5`；托管渠道回报 ID，未取得独立上游 revision | `anthropic`；native `tool_use` | 1,000,000 / profile 128,000 | provider default；未显式传 thinking/effort/temperature/top_p |
| Qwen3.8-27B | `qwen3.8-27b`；权重 revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` | `openai`；SGLang `qwen3_coder` function/tool | 1,000,000 YaRN / `remaining_context` | serving chat-template `low`；temperature 1.0、top_p 0.95、top_k 20 |
| Muse Glimmer-30B | `muse-glimmer-30b`；权重 revision `a4e59da52a7bc87ae7251dd5545c0dd437c44b68` | `openai`；SGLang Muse ATEM function/tool 与 serving adapter | 131,072 / `remaining_context` | 模板默认 `high`；temperature 1.0、top_p 0.95、top_k 64 |
| E2 judge（唯一） | `gpt-5.6-luna`；渠道回报 ID | `openai-responses`；既有 shared structured runtime | judge 请求预算 24,000 | `semantic-judge.two-stage.v3.11`；两读、分歧仲裁、`relation_first`、`closure-profile=full` |

新增生成均为 stream；method 生成池最多 16 workers，后续 judge 使用单池最多 8 workers，已完成的首批 16-worker 裁定不重写。开放模型只使用远程 GPU 4–7 的独立 conda 环境，Qwen 与 Muse 不共用 serving 依赖；base、系统 Python/CUDA、GPU 0–3 和其他任务不参与本轮。[src-protocol] [src-e1-handoff] [clm-runtime]

生成端没有统一的 10K 人为上限：Sonnet 使用 profile 的 128K，Qwen/Muse 使用服务端 `remaining_context`，完整输入不裁剪；judge 的 24K 是独立的既有裁定协议。reasoning tokens 若由 provider 返回，已包含在 completion/output 中，不能再次相加。[src-protocol] [clm-budget]

### 2.2 代码、台账和裁定身份

| 内容 | 版本或身份 |
| --- | --- |
| E2 事前协议与后续追加登记 | [`preregistered.md`](../discover_matrix/docs/generations/e2_20260907/preregistered.md) |
| 新增 backbone 生成/裁定提交 | Sonnet `f52507d1a360f7b728e143f51ad738fed07eff9a`；Qwen `839cfb7935dc87830aae9d21446d4692e2a12935`；Muse `3b9068928a23e0e3f3eba2d81a7a94846cb1cefe` |
| Muse 后续 judge continuation | `ae6e2cc81ca4e089ff6648f9eb9df12cf8ab41b8`；只改变 judge 池大小，不改变语义 |
| 共同台账 | `discover_matrix/ledger_v2/ledger.json`，145 条；L0/L1/L2 = 71/35/39 |
| 共同 expected 分母 | 每臂 145 × 3 = 435；每个新增 backbone 324 格 |
| 历史 Luna | v61 method commit `ea6141607`，method run `a7b47d84c3cb4377a8009e5018d5b745`；X1v2 baseline 只读裁定同一 judge 配置 |

首批 Sonnet judge 格保留旧 `aizzz` 渠道 provenance，后续使用已验证的 `sub2api`；这只是渠道边界，不改变 prompt、schema、裁定规则或历史结果。[src-luna-route] [clm-provenance]

## 3. 双臂全量结果

### 3.1 两种 precision 与主指标

这里明确列出两种 precision，沿用 `analyze_a1.py` 的既有定义，不互相替换：

- **普通 report precision**：`(K + N) / (K + N + I)`，即所有发布报告中 `VALID_KNOWN` 或 `VALID_NOVEL` 的比例，是主 precision。
- **strict precision**：先只保留 `validity != INVALID` 且 `d_tier ∈ {D1, D2}` 的报告，再以全部发布报告数为分母；它是 D1/D2-only 敏感性口径，不是新的主分母。strict hit 同样只使用 D1/D2 的 FULL 单元，expected 分母仍为 435/145。[src-a1-definition] [src-e2-stats]

`hit@1` 的分母是 435 个 expected-round，`hit@3` 和 `hit@all` 的分母是 145 个台账条目；`N` 是台账外有效报告数，不是独立新缺陷数。[src-e2-stats] [clm-metrics]

| backbone / 历史主线 | arm | reports | K/N/I | 普通 precision（分子/分母） | strict precision（分子/分母） | hit@1 | hit@3 | hit@all |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Claude Sonnet 5 | ours | 823 | 536/183/104 | 719/823 = 87.36% | 650/823 = 78.98% | 66.90% | 84.14% | 47.59% |
| Claude Sonnet 5 | baseline | 715 | 340/151/224 | 491/715 = 68.67% | 382/715 = 53.43% | 55.40% | 75.86% | 33.10% |
| Qwen3.8-27B | ours | 958 | 599/256/103 | 855/958 = 89.25% | 781/958 = 81.52% | 71.49% | 86.21% | 55.86% |
| Qwen3.8-27B | baseline | 455 | 247/122/86 | 369/455 = 81.10% | 339/455 = 74.51% | 51.72% | 65.52% | 36.55% |
| Muse Glimmer-30B | ours | 910 | 544/229/137 | 773/910 = 84.95% | 712/910 = 78.24% | 74.02% | 85.52% | 60.69% |
| Muse Glimmer-30B | baseline | 681 | 347/184/150 | 531/681 = 77.97% | 477/681 = 70.04% | 56.78% | 65.52% | 47.59% |
| 历史 Luna v61 main | ours | 903 | 561/198/144 | 759/903 = 84.05% | 678/903 = 75.08% | 74.25% | 89.66% | 56.55% |
| 历史 Luna X1v2 | baseline | 512 | 293/134/85 | 427/512 = 83.40% | 403/512 = 78.71% | 51.72% | 72.41% | 32.41% |

上述八行不构成同批次排行榜：Luna 是历史只读结果，使用 19 predicates；本轮三个新增 backbone 使用 12 predicates，并拥有各自的模型、渠道和运行版本。[src-luna-history] [src-e2-stats] [clm-comparability]

### 3.2 同 backbone 配对差值

| backbone | 普通 precision | strict precision | hit@1 | hit@3 | hit@all |
| --- | ---: | ---: | ---: | ---: | ---: |
| Claude Sonnet 5 | +18.69 pp | +25.55 pp | +11.49 pp | +8.28 pp | +14.48 pp |
| Qwen3.8-27B | +8.15 pp | +7.02 pp | +19.77 pp | +20.69 pp | +19.31 pp |
| Muse Glimmer-30B | +6.97 pp | +8.20 pp | +17.24 pp | +20.00 pp | +13.10 pp |
| 历史 Luna v61（只读参照） | +0.65 pp | -3.63 pp | +22.53 pp | +17.24 pp | +24.14 pp |

差值是描述性、同 backbone 内的配对结果。新增模型的 9 个 NL cluster 以 seed `20260907` 同步重采样 10,000 次；例如 Sonnet 的 95% 区间为普通 precision `[11.00, 24.79]`、hit@1 `[-1.67, 25.37]`，区间和 cluster 留出结果见对应 `statistics.json`。这不是模型间因果估计，也不是谓词机制已被单独证明。[src-e2-stats] [clm-uncertainty]

### 3.3 L0/L1/L2 分层 hit@1

下表按 `L0/L1/L2` 顺序列出 hit@1，分母固定为 `213/105/117`；其余分层 hit@3、hit@all 和严格 D1/D2-only 指标保存在三份 `statistics.json` 及 Luna 历史统计中。[src-e2-stats] [src-luna-history] [clm-tier]

| backbone / arm | L0 | L1 | L2 |
| --- | ---: | ---: | ---: |
| Sonnet ours / baseline | 62.44% / 52.11% | 61.90% / 70.48% | 79.49% / 47.86% |
| Qwen ours / baseline | 77.46% / 51.64% | 64.76% / 62.86% | 66.67% / 41.88% |
| Muse ours / baseline | 77.46% / 61.50% | 75.24% / 73.33% | 66.67% / 33.33% |
| Luna v61 ours / X1v2 baseline | 71.83% / 50.70% | 69.52% / 68.57% | 82.91% / 38.46% |

## 4. 生成与阶段审计

### 4.1 选定格的 usage 与阶段状态

以下 usage 统计只针对最终选入的 162 个格；`ours` 的 usage 按 `model_call_id` 去重并包含选定格中的失败尝试，baseline 是每格聚合，因此两臂的调用数不能用来比较成本或速度。[src-generation-stats] [clm-usage]

| 模型 / arm | 格状态 | 发布 reports | usage 记录（完成/失败） | input P50/P95/max | output P50/P95/max | schema 修正事件 | 缺失 input/output usage |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sonnet ours | 111 completed；51 completed_with_diagnostics | 823 | 1229（1226/3） | 41857/94518/118261 | 4564/10757/26363 | 284 | 3/3 |
| Sonnet baseline | 162 ok | 715 | 162（162/0） | 1416/2778/2821 | 1169/2158/2649 | 未记录 | 0/0 |
| Qwen ours | 159 completed；3 completed_with_diagnostics | 958 | 1136（1058/78） | 27555/51596/83791 | 8543/21071/35381 | 141 | 78/78 |
| Qwen baseline | 162 ok | 455 | 162（162/0） | 875/1720/1778 | 2233/5583/7730 | 未记录 | 0/0 |
| Muse ours | 162 completed | 910 | 867（867/0） | 25476/48412/67766 | 5799/10784/17184 | 62 | 0/0 |
| Muse baseline | 162 ok | 681 | 162（162/0） | 922/1749/1801 | 2870/5652/9264 | 未记录 | 0/0 |

所有选定格均保留完整 stage receipts 和最终 judge 状态；ours 的 `audit_errors` 均为 0。`completed_with_diagnostics` 是带诊断落盘的有效格状态，不等同 provider 失败，也不应被改写成“所有义务均满足”。[src-e2-cells] [clm-stage]

### 4.2 Judge 审计

| 模型 / arm | judge logical calls | provider retries | judge 完成状态 |
| --- | ---: | ---: | --- |
| Sonnet ours / baseline | 1151 / 795 | 113 / 83 | 324/324 completed |
| Qwen ours / baseline | 1326 / 769 | 179 / 82 | 324/324 completed |
| Muse ours / baseline | 1151 / 808 | 64 / 24 | 324/324 completed |

裁定使用同一 prompt/schema/hash、两读、必要仲裁和 `relation_first` 闭合。中途失败、schema 修正和 usage 缺失均保留在逐格审计；顶层 completed 不替代对阶段回执的核对。[src-e2-cells] [clm-judge]

### 4.3 主要诊断与恢复

- **Sonnet**：51 个 ours 格以 `completed_with_diagnostics` 落盘，诊断来自 D 阶段 obligation 证据不完整；其中 `0057/r1` 的 `tool_not_allowed` 行为后果诊断保留并完成裁定。它们不是 provider 失败，不能包装成“所有 D 判断已完成”。[src-sonnet-limit] [clm-sonnet-d]
- **Qwen**：原始 `0009/r3` 的静默流失败回执保留，隔离恢复格按同一唯一键纳入；另有 3 个 D 阶段未闭合义务。初始异步生成存在 120 秒 chunk 边界，恢复请求使用 300 秒；baseline 的同步 `invoke` 不经过该异步计时器。96 次不完整流是尝试数，不是 96 个最终失败格。[src-qwen-limit] [clm-qwen-recovery]
- **Muse**：`0005/r3` 曾发生 600 秒整请求取消，之后同 payload 的传输恢复完成；一次 observer 清理缺陷导致 40 个后续流缺少直接 wire-call 映射，但原生回执与最终格裁定仍保留。62 次 schema 修正事件不表示 62 个独立缺陷。[src-muse-limit] [clm-muse-recovery]
- **三款整体**：Sonnet 的 generation wire summary 为 2007 次尝试、1480 个完整 tool stream；Qwen 为 1322/1226；Muse 为 1030/1029。该层统计包含原始失败与修订尝试，只用于传输和审计解释，不进入效果分母。[src-wire-summaries] [clm-wire-scope]

## 5. 历史 Luna main 与 baseline

Luna 的两臂结果来自 v61 canonical 归档：main `ours` 903 份报告、`K/N/I=561/198/144`，baseline 为 X1v2 的 512 份报告、`293/134/85`。两者均由 `semantic-judge.two-stage.v3.11`、relation-first 闭合、两读加分歧仲裁产生；本轮没有新增 Luna 生成或裁定调用。[src-luna-history] [clm-luna-readonly]

历史主线保留 v61 的 19 predicates、运行日期、渠道、method commit 与原始 profile；本轮三个新增 backbone 使用 12 predicates。Luna 的这两行用于提供已有 main/baseline 能力锚点，也说明 E2 组合中的唯一 judge 与历史模型结果之间的协议边界；不把 Luna 旧数字改写成新 profile 下的结果。[src-luna-history] [clm-comparability]

## 6. 结果解释与限制

1. 同 backbone 的配对差值支持对“在该 backbone 上加入现有方法组件”的描述性分析；它不能单独证明仿真、形式化验证或谓词各自的因果贡献。需要逐组件消融时，应使用 A1/A2 的冻结协议，不能从本表反推。
2. 报告数、`K/N/I` 和 W1/W2 回执数不是独立缺陷数；模型输出长度、修订次数和证据折叠会改变报告计数。N 不能直接写成新缺陷数量，hit 指标的分母必须保持 145/435。
3. Luna 历史与本轮三模型跨代次、跨 predicate 数、跨 profile/渠道；E2 结果不可拼成统一排行榜。公开 benchmark 档位与本轮实际 serving 档位也应分开，尤其 Qwen 的公开 xhigh 不等于本轮 low。
4. 三款生成的 usage 分布混合了成功、修订和恢复尝试；reasoning 已包含在 completion/output 中。baseline 的同步调用与 ours 的异步 structured runtime 有不同的等待边界，不能以调用数或墙钟作成本结论。
5. raw prompt、完整 SSE/wire、`call_metadata/llm` 和私有配置不进入 Git；逐格结构化 `source`/`judge_source` JSON 已在 `final_results/e2_20260907/raw/` 提供，但 fresh clone 仍不能重放真实 provider 调用。没有把原始 ZIP 或凭据提交到仓库。[src-artifact-boundary] [clm-artifact]

## 7. 可复验与交接

不需要 API、GPU 或凭据即可复算本报告的 E2 机器结果：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --check-counterexamples
```

该命令核对 archive manifest、每模型 324 个唯一格、每臂 435 个 expected-round、阶段/报告集合、来源 hash、judge hash、指标、证据分母和 14 个损坏反例；它不重新判断报告语义，也不调用 provider。[cmd-e2-check] [clm-repro]

机器入口：

- [E2 紧凑归档 README](../final_results/e2_20260907/README.md)：文件约定、scope、复算边界和逐格 JSON 入口。
- [Sonnet statistics](../final_results/e2_20260907/sonnet/statistics.json)、[Qwen statistics](../final_results/e2_20260907/qwen/statistics.json)、[Muse statistics](../final_results/e2_20260907/muse/statistics.json)：完整分层、严格口径、bootstrap 和 gained/lost。
- [E2 事前协议](../discover_matrix/docs/generations/e2_20260907/preregistered.md)：模型身份、预算、谓词、worker、judge 规则和后续授权记录。
- [Luna canonical v61](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)：历史 main/baseline 唯一来源。

本报告只承载 E2 稳定事实和复验入口；后续 E2 协议冻结仍需明确实际生成档位、渠道 provenance 与跨模型可比性，不在本报告中启动 O2 或新增 judge 实验。[clm-handoff]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 本综合报告 | `03988214beefe4281ae3b5a6650506c680780f92` | 同左 | 首次写入三 backbone E2 结果、协议边界与配对统计；本次扩展 Luna 与 precision 定义 | 本次只扩展为唯一综合入口 | 本报告引用的 E2 compact JSON 与 Luna history |
| `final_results/e2_20260907/{sonnet,qwen,muse}` | `03988214beefe4281ae3b5a6650506c680780f92` | 同左 | 冻结三模型 324 格、统计与证据摘要 | `added10f737b1714198107b7c8632f429a4cebd7` 增加 raw JSON 副本 | 各模型 `cells.json` / `verification.json` / `statistics.json` / `evidence.json` |
| `final_results/e2_20260907/raw/` | `added10f737b1714198107b7c8632f429a4cebd7` | 同左 | 增加可查阅的逐格 source/judge JSON 与 manifest | 无 | `raw/MANIFEST.json` 与逐格 JSON |
| `final_results/e2_20260907/luna_history.json` | `03988214beefe4281ae3b5a6650506c680780f92` | 同左 | 记录历史 Luna 只读来源 hash 与配对复算 | 无 | v61 canonical judge records |
| `discover_matrix/docs/generations/e2_20260907/preregistered.md` | `f52507d1a360f7b728e143f51ad738fed07eff9a` | 同左 | 冻结 scope、模型、预算、predicate、judge 和并发口径 | 后续追加授权均在同一登记文件中保留 | protocol text and input snapshot |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
| --- | --- | --- | --- | --- | --- |
| [src-e2-stats] | e2_statistics | [`final_results/e2_20260907/*/statistics.json`](../final_results/e2_20260907/) | json | 三款双臂指标、差值、分层与 bootstrap | `metrics`, `delta_pp`, `cluster_bootstrap_95pct` |
| [src-e2-cells] | e2_cells | [`final_results/e2_20260907/*/cells.json`](../final_results/e2_20260907/) | json | 324 格阶段、errors、usage 审计与 judge 状态 | `cells[*]`; `schema=paper1.e2.frozen-decisions.v1` |
| [src-generation-stats] | generation_statistics | [`final_results/e2_20260907/sources.json`](../final_results/e2_20260907/sources.json) | json | 选定格 usage 分布与状态 | `models.*.generation_statistics` |
| [src-wire-summaries] | generation_wire | [`final_results/e2_20260907/sources.json`](../final_results/e2_20260907/sources.json) | json | 所有保留生成尝试的 stream/错误边界 | `models.*.generation_wire_summary` |
| [src-protocol] | e2_protocol | [`discover_matrix/docs/generations/e2_20260907/preregistered.md`](../discover_matrix/docs/generations/e2_20260907/preregistered.md) | md | 实验设计、profile、predicate、worker、judge 规则 | §§1–9；追加授权记录 |
| [src-a1-definition] | a1_arithmetic | [`discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py`](../discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py) | source-code | 普通与 strict precision 的确定性定义 | `calculate()` 的 `precision` 与 `strict` 字段 |
| [src-luna-history] | luna_v61 | [`final_results/e2_20260907/luna_history.json`](../final_results/e2_20260907/luna_history.json) 与 [`final_results/v61_source_divergence_vs_x1v2_baseline/README.md`](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md) | json/md | 历史 Luna main/baseline 数字和只读边界 | `verification.arms`; v61 总表 |
| [src-luna-route] | luna_route | [`final_results/e2_20260907/sources.json`](../final_results/e2_20260907/sources.json) | json | judge 渠道切换和 provenance | `judge_route_change`, `models.sonnet.limitations` |
| [src-sonnet-limit] | sonnet_limits | 同上 | json | Sonnet failed records 与限制 | `models.sonnet.limitations`, `unselected_failed_records` |
| [src-qwen-limit] | qwen_limits | 同上 | json | Qwen 流恢复、缺失 usage、D 诊断 | `models.qwen.limitations`, `generation_wire_summary` |
| [src-muse-limit] | muse_limits | 同上 | json | Muse 取消、observer 映射和 serving 限制 | `models.muse.limitations`, `deployment` |
| [src-artifact-boundary] | e2_archive_readme | [`final_results/e2_20260907/README.md`](../final_results/e2_20260907/README.md) | md | raw/compact 证据边界与 fresh clone 限制 | 文件约定、复验、raw 说明 |
| [src-e1-handoff] | model_handoff | [`reports/model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md`](./model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md) | md | 最终 profile、部署、上下文和 16-worker 背景 | §§2–5；配置与容量表 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [clm-scope] | E2-SCOPE-01 | 三款新增 backbone 各 324 格，共 972 格；Luna 只读复用 | count/scope | [src-protocol] §1；[src-luna-history] `scope` | [cmd-e2-check] | high | Luna 不属于本轮新增生成量 |
| [clm-analysis] | E2-ANALYSIS-01 | 主要效应是同 backbone 的 ours-baseline 配对差 | decision | [src-protocol] §5、§10 | 人工核对协议 | high | 不是跨模型因果比较 |
| [clm-metrics] | E2-METRICS-01 | K/N/I、普通 precision、strict precision、hit 的分母和定义如正文所述 | count | [src-e2-stats] `metrics`; [src-a1-definition] `calculate()` | [cmd-e2-check] | high | strict 是 D1/D2-only 敏感性，不替换主 precision |
| [clm-comparability] | E2-COMP-01 | Luna 历史 19 predicates 与新增模型 12 predicates，不能合并排行 | prohibition | [src-luna-history] `scope`; [src-protocol] §2 | 人工核对版本/hash | high | 只允许描述性并列展示 |
| [clm-runtime] | E2-RUNTIME-01 | 新增生成 stream，method 最多16 workers，后续 judge 单池最多8 | trace | [src-protocol] §§1,8,9; [src-e1-handoff] 部署表 | 人工核对登记与 cells | high | 已完成的旧 16-worker judge 不重写 |
| [clm-budget] | E2-BUDGET-01 | 生成无统一10K cap；开放模型使用 remaining_context，judge 独立24K | trace/prohibition | [src-protocol] §§2,8；input snapshot profiles | [cmd-e2-check] | high | profile 上界不是额外可用输出窗口 |
| [clm-provenance] | E2-PROV-01 | Sonnet 首批 judge 保留旧渠道，后续使用 sub2api | trace | [src-luna-route] `models.sonnet.limitations` | 人工核对来源 manifest | high | 渠道差异不改变裁定语义 |
| [clm-eligibility] | E2-ELIG-01 | 正常降级和恢复格保留，未用顶层状态抹平诊断 | classification | [src-e2-cells] `status`, `errors`, `audit_errors` | [cmd-e2-check] | high | 语义有效性以冻结 judge 结果为准 |
| [clm-usage] | E2-USAGE-01 | ours usage 去重口径与 baseline 聚合口径不同，不能作成本/速度比较 | prohibition | [src-generation-stats] `scope` | 人工核对 scope 字段 | high | provider reasoning 已包含在 output |
| [clm-stage] | E2-STAGE-01 | 每格需同时核对完整 stage、errors/audit errors 与 judge 状态 | trace | [src-e2-cells] `cells[*].stages`, `judge_status` | [cmd-e2-check] | high | exit code/HTTP 200 不构成整格通过 |
| [clm-tier] | E2-TIER-01 | L0/L1/L2 分层使用 213/105/117 的 expected 分母 | count | [src-e2-stats] `metrics.*.tiers`; [src-luna-history] `statistics.metrics.*.tiers` | [cmd-e2-check] | high | 仅报告 hit@1，其余分层指标在 JSON |
| [clm-wire-scope] | E2-WIRE-01 | wire summary 包含尝试级 stream/错误，不进入效果分母 | scope | [src-wire-summaries] `generation_wire_summary` | 人工核对 scope 字段 | high | 失败尝试不等于失败格 |
| [clm-sonnet-d] | E2-SONNET-D-01 | Sonnet diagnostics 是落盘的证据义务缺口，不是 provider 故障 | classification | [src-sonnet-limit]；[src-e2-cells] Sonnet ours cells | [cmd-e2-check] | high | 不能写成所有 D 判断完成 |
| [clm-qwen-recovery] | E2-QWEN-REC-01 | Qwen 96 次不完整流是尝试级记录，恢复格按唯一键纳入 | trace | [src-qwen-limit] `generation_wire_summary`, `limitations` | [cmd-e2-check] | high | 不等于96个失败样本 |
| [clm-muse-recovery] | E2-MUSE-REC-01 | Muse 取消与 observer 映射缺口被保留，最终格仍逐格核销 | trace | [src-muse-limit] `limitations`; [src-e2-cells] | [cmd-e2-check] | high | 不外推持续 SLA |
| [clm-judge] | E2-JUDGE-01 | 三款新增模型均由唯一 Luna judge 按固定协议完成 324/324 格 | trace | [src-e2-cells] `judge_protocol`, `judge_status`; [src-protocol] §6 | [cmd-e2-check] | high | 无人工复核，不是人工金标准 |
| [clm-uncertainty] | E2-UNC-01 | bootstrap/cluster 留出只作不确定性描述，不作普遍性证明 | risk | [src-e2-stats] `cluster_bootstrap_95pct`, `leave_one_cluster_out` | [cmd-e2-check] | high | 仅9个 NL cluster |
| [clm-luna-readonly] | E2-LUNA-READ-01 | Luna 数字来自 v61 canonical，E2 无新增 Luna 调用 | trace | [src-luna-history] `verification`, `statistics` | [cmd-e2-check] | high | 不是新连接下的重新验收 |
| [clm-artifact] | E2-ARTIFACT-01 | raw prompt/SSE/private config 不随 Git 提供，compact/raw JSON 可审阅 | boundary | [src-artifact-boundary] 文件约定与 raw 说明 | [cmd-e2-check] | high | fresh clone 不能重放 provider |
| [clm-repro] | E2-REPRO-01 | 复验脚本只做离线 hash、结构与算术核对，不调用 provider | trace | [src-protocol] §9；`analyze_e2.py` main | [cmd-e2-check] | high | 不替代语义重裁 |
| [clm-handoff] | E2-HANDOFF-01 | 后续冻结需保留 profile、档位、渠道和 predicate 差异 | handoff | [src-protocol]；[src-e1-handoff] | 人工核对文档 | high | 本报告不启动 O2 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 作用 |
| --- | --- | --- |
| [cmd-e2-check] | `python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --check-counterexamples` | 无 API 复算三模型完整归档、hash、指标和反例拒绝 |
| [cmd-e2-single] | `python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --model sonnet`（或 `qwen` / `muse`） | 单独复算一个完整 backbone；单组通过不等于三组全量通过 |
| [cmd-luna-history] | `venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/v61/evaluate_rq3.py` | 在取得 canonical v61 原件时复算历史 Luna 的 RQ3 派生统计；不调用 provider |
