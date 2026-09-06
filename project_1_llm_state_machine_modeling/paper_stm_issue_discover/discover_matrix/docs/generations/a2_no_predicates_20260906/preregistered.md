# A2 整个谓词机制消融：事前登记

登记日期：2026-09-06，A2 真实调用之前。依据：[消融公约](../../protocol/ablation_design_and_parallel_contract.md)、[A2 #206](https://github.com/HansBug/research_ideas/pull/206)、[伞 PR #179](https://github.com/HansBug/research_ideas/pull/179)。用户已授权实现、验证、推送后运行 Luna 54×3、独立 Luna judge、复算与原因审计、归档和中文报告。本登记不以效果方向为完成门槛；施工进度和 review 写在 PR，事后结果另存，不回改事前假设。

> 当前适用补充：§7 的低并发、§8 的合法降级读取仍有效；**主比较对象由 §9 的用户明确指令覆盖为冻结 v61 ours，只运行 A2 及 A2 judge**。§1/§7 的 recovery full 对照安排已被覆盖，保留原文仅用于追溯登记历史。

## 1. 问题与条件

在完整 NL、作者源、FCSTM、转换追踪和前置检查事实保留时，整个谓词机制对 hit、precision、报告量和跨轮稳定性有什么净作用？机制同时包含定义引导和执行约束；本实验不估计这两部分各自的贡献，不是纯 LLM baseline，也不是谓词 subset 消融。

| 条件 | 模式 | 规模 | 正式 run ID |
| --- | --- | --- | --- |
| A2 | `no-predicates` | 54 pair × 3 round = 162 格 | `2d9c2b12efb4498489af2f268e9ede94` |
| 共享匹配 full | `none` | 相同 54×3 | `2893db20b2d846018f189233703bf098` |

共享 full 来自 [A1 的事前登记](../a1_no_inspect_20260906/preregistered.md)，在 A2 结果出现前固定，不另跑或事后挑选对照。其正式来源提交为 `9c7c99504db0f53fecd650af4076844af1f6e629`，运行语义来自 A1 已推实现；A2 合流代码以 `87e969b291156b98e2762967f0aa1439fbd4ddaa` 为 full 对拍锚点。两臂来源提交不同，不能写成同一代码 commit：须以实际请求/schema/决策对拍和下表身份核验，证明保留的方法语义相同。A1/full 后续若改变方法或输入，先复核对照资格，不静默换对照。

v61 的原 19 条身份、raw/derived 和统计全部冻结。它只作为版本差异明确的历史比较，不是当前 12 条的单因素对照。baseline 不修改、不重跑。

## 2. 固定边界

A2 移除实际 system/user prompt、响应 schema 及 description、补全/纠错中的谓词要求；provider 从一开始就不生成 `predicate_id` / `predicate_inputs`。关闭 `route_primary_candidates`、谓词参数补齐、compiler/validate/backend、执行专属探针、执行回执和 true 回执过滤。`frontier._materialize_group_post_states` 为 native R2 构造输入且调用 cold-prefix 执行定位，随机制关闭；保留由其他语义路径形成的状态响应义务。

保留原有契约提取/补全、两路 grounding、exact ID/cardinality 约束、普通模型绑定、源码分歧、source-transition closure、作者/转换归属保护、内部 D 及定向纠错、发布门、exact dedup、根因折叠和 guard modality 归并。混合 frontier 中已有源/契约/inspect 支持的发现保留，只不附着谓词参数。UML 初始迁移领域不变量保留原生观察值和 authority，使用独立 semantic invariant schema；缺边与根 wrapper 预检仍用普通语义引用。禁止以“语义检查”之名重建被移除的执行或过滤。

语义证据使用 `evidence-discovery.semantic_evidence_record.v1`，只形成真实 W0/W1；plan、receipt 和 execution_receipt 为 null，执行回执列表为空。只有精确绑定且内部 D1/D2 才进入发布。被关子步骤为 `disabled_by_ablation`，混合 execute_batch 仍完成语义处理；关闭机制本身不使整格 ineligible。W2=0 是设计结果，不是效果证据。

## 3. 输入与身份

论文相对根为 `project_1_llm_state_machine_modeling/paper_stm_issue_discover/`，数据为 `pipeline/representation/reports/llms_emp_r45_java_60`，台账为 `discover_matrix/ledger_v2/ledger.json`。固定 `FROZEN_PAIR_IDS` 的 54 pair、9 个 NL 簇、每簇 6 个制品；145 条台账，L0/L1/L2=71/35/39，三轮 expected-round 分母 435。无台账条目的 pair 仍运行并进入报告精度统计。

```text
0000 0001 0002 0003 0004 0005 0006 0007 0009
0010 0011 0012 0013 0014 0015 0016 0017 0019
0020 0021 0022 0023 0024 0025 0026 0027 0029
0030 0031 0032 0033 0034 0035 0036 0037 0039
0040 0041 0042 0043 0044 0045 0046 0047 0049
0050 0051 0052 0053 0054 0055 0056 0057 0059
```

| 身份 | 冻结值 |
| --- | --- |
| 输入集合 hash（包含完整 manifest） | `sha256:0e34a96951d2a7ee3da77e572ca42963e1270a1acba9ed50a38e2f03e3599039` |
| ledger SHA-256 | `sha256:b5a38d3d24a51e980e5b9f5afc7c8c66aded59f3b51f16afe67e0deb592d0e36` |
| 软件 registry | `four-family-12-core.v1`，A2 不调用这些谓词 |
| registry hash | `sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d` |
| full prompt/schema hash | `sha256:744e7f489591904a08e9919ded9f99ec73c2d55d81225fbd8a9ec18dca8fefe2` |
| A2 prompt/schema hash | `sha256:298a34a323f2a7da758b2d3ef24fe8bdf5f61751a8c4d9d9ee21d7aeedc73d0b` |
| A2 条件投影版本 | `no-predicates-semantic.v1` |
| 无凭据模型配置 hash | `sha256:a5bb978af02936e60784ad37bb85cb047c89f95eee971a9975c6f3ffc0b292c8` |
| 公共接线基点 | `f2e415276ecc2b00f2afb72090a56539da13dbbb` |

当前 loader 的 manifest hash 包含绝对路径。为保持与已登记 full 的实际请求身份相同，A2 用本 checkout 的代码和 venv，输入路径指向 `/home/zhangshaoang/oo-projects/research_ideas-2/` 下上述冻结数据目录，不改作者输入、转换产物或 sibling 源码。loader 会按既有算法原子刷新 `generated-evidence-discovery/` 缓存，其内容须与相同 artifact hash 一致；这不是新的方法运行输出。A2 的 cell、prompt/raw output、审计、judge 和统计全部写到本 checkout 独立 ignored runs。输入逐文件 hash、依赖/pyfcstm 版本与干净已推 source commit 保存在运行证据；方法不读取台账或本登记的分析内容。

## 4. 模型、smoke 与正式运行

- Method 每个 LLM 节点及独立 judge 均为 `gpt-5.6-luna`，adapter=`openai-responses`，endpoint 引用 `https://sub2api-new-api.deepghs.org`。region、provider revision 未提供，不虚构稳定服务快照；记录每次实际响应的模型 ID、调用时间、usage、错误与重试。
- 使用 `.llmconfig.yml` profile；context=272000、profile output=128000，实际结构化输出另受现有阶段上限约束。沿用 full 的推理/采样设置，不额外设置 temperature/seed/effort；按实际请求审计，不把 provider 默认值写成已知配置。不按 token 等长补充无关输入。
- Streaming 开启，transport retries=8，首字节/read 边界 30 秒、单调用 deadline 300 秒。schema 错误在节点内反馈；不冷启动重采样、不增加整格重试次数来改善结果。内部预算/绑定未闭合保留诊断与残缺产物；provider/schema 终止失败单列核销，不冒充正常零报告，不缩小计划分母。
- Smoke 固定 `0000/0004/0009/0024/0034` 各 1 轮，5 格；run ID=`e2076434178a49979fe4acba46ba64d0`，workers=2，输出 `runs/paper1/a2_no_predicates_20260906/smoke/`。依次覆盖源码分歧/补全、原生候选、guard、D 及 cardinality 既有风险。按工程机制选择，不能据此估总体质量，不把 smoke 转成正式重复。
- 正式 A2 workers=8。A1/full/A2 的活跃 method 配额合计不超过 16；当前两臂占满时等待空位，不改动或中止 sibling。Judge 全部活跃 pair workers 合计不超过 14，A2 最多 14，按既有任务的实际占用安排。
- 代码与本登记先 commit/push，运行前完成正确性、规则出处/引入动机和公平性审查，再启动 smoke。smoke 逐格审计输入/请求、禁用步骤、绑定、D、发布和降级，无新增阻塞问题才正式运行。效果方向不是门槛。

从本 checkout 根运行，显式 PYTHONPATH 包含本分支 method/src、evaluation/src、judge/src、论文兼容入口和根 `utils`。正式命令主体：

```bash
python -m paper_stm_method.cli \
  --report-root /home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60 \
  --output-dir runs/paper1/a2_no_predicates_20260906/method \
  --profile gpt-5.6-luna --ablation no-predicates \
  --run-id 2d9c2b12efb4498489af2f268e9ede94 \
  --rounds 3 --workers 8 --transport-retries 8 --allow-live --allow-full-live
```

Smoke 改用独立目录/ID、rounds=1、workers=2，并逐个传入上述五个 `--pair-id`，不传 full-live。每 30–60 秒检查确切进程与输出增长；静默触发调查，不按任意总墙钟阈值杀整批。确需修实现时保留原失败与原因，在新正式调用前追加登记，不能覆盖已产生的结果。

## 5. 独立裁定、指标与分析

Judge 固定 `semantic-judge.two-stage.v3.11`，协议 hash=`d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`。配置与共享 full 相同：validity_readings=2、validity_aggregation=arbitration、validity_arbitration_trigger=any、k_closure=relation_first、closure_profile=full。逐轮使用 `paper_stm_judge.cli --source-format evidence_discovery_release`，全量读取最终 `report_issue_clusters`，新报告重新裁定，不使用 report-filter 或复制历史裁定。方法内部 W/D/谓词元数据不作为 judge 的质量标签。Judge 的独立完整上下文不回流 method。

必须完整核销 162 格及全部最终报告，分别列出完成、降级、失败、未裁定和审计覆盖。自动裁定、agent 复核、用户人工确认分开记录；本登记时新报告人工确认数为 0。

1. FULL hit@1：expected-round 命中 /435；hit@3：至少一轮命中 /145；hit@all：三轮均命中 /145。列每轮、L0/L1/L2、pair 和 9 个 NL 簇结果。
2. 全部报告数、K/N/I、precision=`(K+N)/(K+N+I)`、无效报告量及 pair 有效率。N 是台账外有效报告数，不直接当新发现的独立缺陷数；重复有效报告不自动计 I。未闭合裁定不声称全量 precision。
3. 同一协议的严格 D2/D1-only 敏感性；绑定未闭合、W0/W1、D 决策、发布前后/去重归并、覆盖缺口和错误分布。A2 空执行列表按 disabled 解释。
4. 对 full/A2 全部 lost/gained expected 单元建立对应表，沿契约提取、grounding、语义候选、绑定、D、发布/归并和独立裁定追踪。先区分阶段事实与原因推断，无法唯一归因时保留不确定性；特别检查 0009/0024/0034 已有风险，不为这些样本增预算或写特判。
5. 配对比较以案例内描述性效应为主，不把 162 格或 435 单元当独立样本。采用 9 个 NL 簇同步成组重采样的 10000 次 bootstrap，seed=20260906，保留簇内 6 个制品与 3 轮；报告百分位区间和逐簇留出敏感性。round 标签不是共同随机种子，小簇数不支持普遍显著性承诺。

事前假设：没有定义引导和执行约束，precision 或重复命中稳定性可能下降；hit 和报告数方向不确定，不给无证据的数值跌幅。生成探针也随机制关闭，因此 true 回执数量不能等同于避免的误报数量。历史 v61 为 903 reports、K/N/I=561/198/144、precision=759/903、hit=323/435、130/145、82/145；W1/W2 划分及 predicate gold 的 exact13/sound-proxy34/unsupported98 不构成 A2 性能上界或预计损失。

解释随实际结果收敛：若覆盖接近而 precision 下降，讨论约束价值；若覆盖下降而 precision 接近，讨论系统性候选发现或定位；若二者反向，报告取舍；若 A2 接近或更好，收窄机制增益主张并审计冗余、干扰和无效报告来源。不分摊定义/执行的因果贡献，不宣称所有 backbone、全部控制系统、人工工时或价格收益。

## 6. 复现与归档

保留原始 prompt/output、调用配置/usage/重试、错误、各阶段产物、模型/依赖/input/registry/prompt/source 身份、eligibility 和逐报告裁定。Smoke 细粒度原件与测试/对拍证据只在 ignored runs；正式事实和可复算结果按 `final_results/<batch>/` 现有规范归档，中文报告进论文 `reports/`。共享 full 只读引用原 ID/hash，不伪造新的来源身份。敏感凭据和私有 judge 执行材料不进入公开制品；提交前核验脱敏、ignore、跟踪集合、逐文件 hash 和数值复算。运行前自审与事后结果审查分开，不冒称独立 reviewer 或人工裁定。

## 7. A2 调用前追加：对照 recovery 与并发调整

2026-09-06，A2 仍为零真实调用时，核对 [A1 事故记录](https://github.com/HansBug/research_ideas/pull/205#issuecomment-5556333437)及四份真实 manifest：原始 A1/full 全部 terminal，但 eligible 仅 23/28 格；大量 `No generations found in stream` 使它们不能充当完整效果实验。原件不删除、不拼入新批次。A1 已以同一 `9c7c99504` 源码、streaming、input/registry/model/prompt hash，分别降低到 workers=2，完整重跑 54×3 并记录 predecessor。

本补充在 A2 的新数据与任何 hit/precision 结果出现前固定：**共享主对照改为 full recovery `8f89338546a14096b8e3f11413555859`**，run contract hash=`sha256:a070d5b285e5aa061d30c1debaa6587ecba679b86e9a85c9cafd6b4075cf0d80`，来源为 `runs/paper1/a1_no_inspect_20260906/recovery_method/`，其 predecessor 为原 `2893db20b2d846018f189233703bf098`。输入、registry、模型和 full prompt/schema hash 与 §3 相同。恢复批次未完成或裁定未闭合前，不宣称主比较完成；主表使用其整个批次，绝不逐格挑选原始/recovery 中较好的结果。原始对照只保留事故及降级敏感性，不隐去其失败率。

并发对 §4 作如下事前覆盖：A2 smoke workers=1，正式 workers=2，A2 judge workers=2；总活跃 method workers 不超过 6，judge 总数仍不超过 14。模型、prompt、输入、重试次数、输出预算和轮次不变。较低并发是根据已经发生的传输事故作出的保守安排，不声称已证明并发是唯一根因；若再次发生空流，保留同调用链尝试与诊断，不以增加重试或整格重采样替代调查。

A1 的 recovery 书面登记晚于它自身启动，A1 已明确披露；A2 引用这份对照时同步披露该流程偏离。A2 本次补充在任何本臂真实调用之前提交推送，不能将两者的登记时序混写。

## 8. A2 调用前追加：合法降级格的 judge 读取

以共享 recovery 的真实 A1 `0033:r3` 复核发现，judge release adapter 原先只接收 `status=completed`，会错误拒绝 `eligible=true` 的 `completed_with_diagnostics`。该格保留 11 条最终报告，应按 §5 进入全量裁定。统一读取门修正为接收这两种完成状态且仍要求 eligible；failed、running 或 eligible=false 仍拒绝。两臂适用同一读取门，不改变报告字段、judge prompt、validity/closure 协议、内部发布门或方法运行产物。

这项修正发生在 A2 零真实调用时。此前 provider-free adapter 检查只覆盖普通 completed，不能证明合法降级格可读取；补充回归验证两种完成状态的 CandidateReport 完全一致，且真实 `0033:r3` 的 11 条报告均能读取。原始诊断和状态照常保留，统计须分别核销 clean、diagnostic、failed，不把 diagnostic 改写为 clean。

## 9. 正式 A2 前追加：用户指定 v61 ours 为 full

2026-09-06，在五格工程 smoke 已产生、A2 正式 162 格尚未启动且没有 A2 独立 judge 结果时，用户明确指示：“不要跑 full 的部分，只跑 A2，full 那边以 v61 ours 为准”。本条按仓库规则优先级覆盖本登记 §1/§7 及消融公约 §5.2 中本批次的匹配对照安排。A2 只新增本臂方法和 judge 调用，full 采用 [v61 冻结归档](../../../../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)及其既有裁定；不新增 full 方法运行、不重裁定 full，也不将 sibling recovery 升为本批次主比较。

主对照原 method run ID=`a7b47d84c3cb4377a8009e5018d5b745`，源码 `ea6141607037d6daabe7df6826fc7c90dab7a12b`，原 19 谓词 registry。沿用 v61 已冻结的 `0045:r1` 补格 run `0e450e5c6c9d4841820c7d1fd2a888ea` 和 `current-r*` 裁定合流政策，不增删历史格、不重挑结果。核验锚点：

- `raw/v61_current/method/run_manifest.json` SHA-256=`5ada697db9a66d3dfdb42d1e3722f2bb97e27cf9586b81ed88a1b9b80ef35df9`。
- `raw/v61_current_fill0045/run_manifest.json` SHA-256=`4f462365ba311b1e28f2559fd95c740d0dbc16265108a46a90d5e832ed8a7e4a`。
- `derived/v61_all_reports.tsv` SHA-256=`b4586298687f6501afe45d50c5d3014808642f24f77b44708196b411e768d38b`。

固定主比较为 A2 新结果与 v61 的 903 reports、K/N/I=561/198/144、FULL hit@1=323/435、hit@3=130/145、hit@all=82/145。计算继续从逐报告裁定和固定 145 台账复算，不只抄总数。v61 原 19 谓词、当前 A2 源码基线、运行日期、prompt/schema、manifest 绝对路径 hash 以及历史补格政策的差异须明确披露；不声称同版本、同时间的单因素因果识别。九簇配对 bootstrap/留簇分析仍可描述这两批记录的差值，但不能消除版本、服务状态或 judge 时序混杂。

该补充是在 smoke 后、正式实验前按用户指令作出，不能回写成初始预登记选择。先前使用 sibling full manifest 作输入身份工程核验的事实保留，该只读核验不等于新增 full 调用或效果对照。模型、A2 schema/prompt、54×3、低并发、重试配置、分母、独立裁定与证据留存规则均不改变。

## 10. 首次 A2 judge 前追加：按完成格滚动裁定

A2 正式方法已开始、尚无 A2 judge 调用时，明确执行顺序：judge 可对已原子落盘且 eligible 的完整格滚动启动，同一轮内按固定 pair 顺序选择当前已完成且从未提交 judge 的格。每条 CLI 运行都冻结完整 pair 列表、来源 hash 和独立 run ID；只跑 A2，workers=2，各 judge 批次串行，合计最多 2 个活跃 judge pair workers。选择不读取报告质量或命中，不使用 report-filter，零报告的 eligible 格仍裁定其空报告集合；失败格产物单列隔离。等待 method 全量结束后统一核销 162 格、全部 eligible 报告与 judge 失败，不能把先完成的子集称为全量结果。滚动处理不把裁定反馈给 method，不更改 §5 的 judge 配置与统计口径。

## 11. 正式 A2 期间追加：采用 A1 的传输修复与稀疏续接

2026-09-06，用户要求关注 pane8 的 Luna 稳定性措施并移植到 A2。此时已经产生 A2 部分 method 和 judge 结果；本补充是运行期间的工程变更，不追溯声称为初始预登记。合入 A1 的原提交 `d2e6843e6023f6eb7e3d9bf08f3148d49bab8260` 和 `7fb300640bba3eb5b10b3acd83c7d07e46d20ebe`，不另写一套共享修复。它们在 SDK 向 LangChain 交付 SSE 前保留失败事件、request/response ID、usage 和终止状态，把空流及明确定义的瞬时上游错误纳入已有有界请求重试；未知非瞬时错误和 `response.incomplete` 保留为不可重试诊断。方法的成功请求参数、prompt/schema、判定规则和 judge 协议不变。

旧 method `2d9c2b12efb4498489af2f268e9ede94` 在精确核对 PID、父子关系和启动时钟后停止派发，让已开始的格到达终态，最长等待 300 秒。逐次信号先写持久回执。切换实际保留 20 个 completed/eligible 格、155 条报告；`0006:r3` 刚开始的新请求只有 context，没有已返回的 decision。旧文件及未完成 audit 原件保留，不修改 source identity。续接 ID 预留为 `55f3799341d046888d8b2e61261913c6`，在新调用前冻结全部 162 格的选择表、旧文件 hash、输入/model/prompt hash、新干净源码和续接脚本 hash。

选择规则只看运行证据：完整且没有待恢复 provider 失败的格原样复用；未运行/中断格继续；明确 provider 失败按原请求恢复。不按 hit、precision、报告数或 judge 结果挑选重跑。复用格保留旧 run/source 身份，新增格记录新身份。成功阶段直接复用精确 outcome；只有 audit 的阶段回放成功 provider turn 及其 schema 修订历史，逐项比对 system/input/schema 和实际请求投影后到达首个未完成请求。仅归一化 `handle_errors` 函数内存地址，任何实质差异停止续接并保留诊断。关闭整阶段的 provider 外层冷启动重试，transport retries 仍为 8；这不增加方法修订预算。

A2 method 和 judge 各保持 2 个 worker。A1 已独立提高并发，因此 §7 的全机合计 6 个 method worker 不再是当前可满足的控制条件；A2 不调整 sibling 进程，实际共享服务并发与调用时段另记为运行条件。保留 §4 的总 method 上限 16，并按实际活跃进程核验。并发、版本和服务时序不能当成已消除的混杂。

前两批完整 judge `441ffdfffd4f5aaab90870395cb35618` / `62388b064f2255daa02439dcd045dbb0` 原样保留。退出旧调度器后，第三批 `82023a87854e5198b71a3ca48832a548` 的进程消失且没有 terminal receipt；该批标为切换中断，不解释成正常零报告或 provider 质量失败。其已有响应、未完成请求及来源 hash 保留，使用相同请求前缀核验恢复缺失裁定，不重裁定已完整格。新滚动调度只读取冻结选择表指定的 method 来源，跨目录核销重复提交、失败和未裁定项。所有实际调用仍只属于 A2，主比较继续使用 §9 的 v61 原件。

合流验收包括共享 runtime、A1/A2 schema/flow/resume 回归；完整 full 的 default/显式 `none` 与 `87e969b29` 的既有 provider-free 实际请求和决策对拍；真实 A2 已成功格、失败 smoke 及中断请求的离线回放边界检查。具体命令和原件随实验归档，动态执行状态留在 PR。

## 12. 续接期间追加：HTTP 5xx 重试遗漏与诊断格核销

2026-09-06，续接 `55f3799341d046888d8b2e61261913c6` 的 `0009:r2` 在 D 阶段收到 Cloudflare HTTP 520，原始结构化错误带 `retryable=true` / `retry_after=60`，但本地状态码白名单只包含 500/502/503/504，没有形成任何 transport retry。该格保留为 eligible `completed_with_diagnostics`、零发布报告；此前契约与两路 grounding 成功。这是请求恢复遗漏，不能解释为 A2 正常零发现。

共享修复按已安装 OpenAI SDK 的 server-error 类别覆盖 HTTP 5xx；已有请求重试次数、Retry-After、单调用 deadline 和显式 Responses `retryable=false` 优先级不变。补充原始/包装状态码分类以及真实 SDK HTTP 520 异常的离线请求重试检查。成功路径语义不改。已启动的长驻进程仍记录并使用 §11 的源码，后续新启动的进程记录修复后的源码，不假称在途运行已热更新。

本补充在 `0009:r2` 的任何独立 judge 调用前固定：后续遇到明确 provider 失败的格先保留诊断原件，暂缓提交其报告集合；当前 method 批次结束后，仅对有 provider 失败证据的格按 §11 的精确成功前缀做稀疏恢复。非 provider 的内部诊断格仍按原 eligibility 门裁定，效果差、零报告或命中低本身不触发恢复。所有原始失败、恢复来源、缺失和最终选择逐项核销；若恢复仍失败，保留其诊断并在固定分母及缺失敏感性中披露，不无限冷启动。已有正常 method/judge 结果不重采样。

滚动 judge 调度器在已完成批次边界暂停并更新来源选择，保留在途子进程直到其终态，以免再次依赖孤儿进程存活。pane8 新评估的另一 endpoint 尚未用于 A2；本批次保持已登记 model/config hash，任何服务迁移必须另记配置身份与时间边界。

## 13. 用户指定新 Luna 站点与正常运行路径

2026-09-06，用户明确要求切换 pane8 已评估的 Luna-only 服务并清理非必要修改。本补充覆盖 §11/§12 的旧站点、低并发、精确前缀恢复及逐小批等待安排。新 endpoint 为 `https://api.aizzz.xyz/v1`，独立私有配置 profile 为 `aizzz-luna-eval`，请求模型仍为 `gpt-5.6-luna`、adapter 为 `openai-responses`。共享 `.llmconfig.yml` 不修改；真实配置 hash、源码、时间、请求和实际响应身份分别落盘。pane8 的可用性评估只作为迁移依据，其探针和八个 A1 评估格不进入正式 A2 数据。

新 method run `af618190b34652b58ed0ae9ec231bdfe` 以普通 `PublicStructuredRuntime` 调用现有 `_method_cell`，仅调度尚未落盘或有明确 provider 失败证据的 A2 格，总并发 16。已完整格按字节 hash 保留旧来源，选择不依据报告数、效果或裁定。旧 method 停止时的在途请求和原始审计保留并记为主动服务切换中断；新站点缺格以新身份完整执行，不冒称旧配置 resume，也不使用在线 PrefixRetry、RecordedModel 或 ContinuingRuntime。该最小稀疏调度仅弥补现有 CLI 不能选择非连续 round 的限制。普通非 provider 诊断不触发重跑。

旧 judge 在当前批次终态停止；已完整裁定复用。后续使用原生 judge CLI，逐轮总并发 16，读取逐格冻结来源视图，不修改原格状态或身份；不叠加三轮各 16。正常有界 transport retry、空流/失败事件/异常 EOF 识别、错误与 usage 回执及节点内 schema 修订保留；不增加探针或重复压测作为启动前置条件。method、judge 的并发上限各 16，A1 的独立运行条件另列，不更改 sibling 进程。

模型配置从此按来源分段核验，禁止把不同 endpoint 的结果标成同一 config hash。最终报告须列出切换前后完成数、失败与中断、配置差异及分段敏感性。本条是已见部分结果后的运行条件变更，不能称为初始预登记；不改变 54×3、145 台账、435 expected-round、A2 prompt/schema、judge v3.11 和 §9 的冻结 v61 对照，也不新增 full 或 full judge 调用。
