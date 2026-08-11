# seed_library/SUMMARY.md

## 1. 当前状态一句话

本 SUMMARY 是种子文库的研究结论与统计摘要入口；它承接 R1.7 有界快照 v4，而不是全域普查。旧 `seed_corpus/` 的横向台账与原始检索材料已归档到 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)。逐条一手资源明细以 [REGISTRY.md](./REGISTRY.md) 和单条目 `seed_resource_registry.json` 为准。

核心口径：种子文库记录上游 `NL -> STM_0` 方法 / 来源集合，**不是修正基线文库**（那是 [../repair_baselines/](../repair_baselines/) 的职责，且 paper1 收窄为 issue discover 后已不做 repair）。

⚠️ **下面这句已作废**：~~[selected_seed_examples/](../../selected_seed_examples/) 是当前四个 smoke 用代表性种子样例，四例不是最终实验集合或主结果样本上限。~~
现状是：[selected_seed_examples/](../../selected_seed_examples/) 已是 **60 个 pair 的人读镜像**，
且**就是**论文语料——全部来自本库条目 [llms-emp-stm-subset/](./llms-emp-stm-subset/)，
实验网格 **54 个**（末位为 `8` 的 6 个按建模对象边界永久排除）。它不再是「smoke 用四例」。

### 1.1 三类文库关系

| 文库 | 当前角色 | 本 SUMMARY 的使用边界 |
|---|---|---|
| [./](./) | 上游 `NL -> STM_0` seed 方法 / 来源 | 种子池当前事实入口；仍需逐案例冻结版本、哈希、泄漏边界和数据质量 caveat。 |
| [../repair_baselines/](../repair_baselines/) | 模型修正 / 补全 / refinement 近邻 | 只用于 related work / 边界论证与后续 repair 论文储备；**不是 paper1 的 baseline**，也不提供种子。 |
| [../nl_datasets/](../nl_datasets/) | 只有 NL、尚未闭合 `STM_0` 生成关系的数据源 | 不提前计为 seed；生成并记录 `STM_0` 后才可 crosslink 到本库。 |


## 1.6 一手 seed resource registry 摘要

从一手 registry 口径起，逐条一手资源明细以 [REGISTRY.md](./REGISTRY.md) 为准；本 SUMMARY 只保留研究结论、统计摘要与风险，不复制全量资源表。当前 registry 的稳定结论如下。源码、论文 LLM 与复跑证据的逐条可见列在 [REGISTRY.md](./REGISTRY.md) §2；机器字段为 `resource_profile`，其中 `code_reproducibility` 只表示本项目对作者一手代码的连通性检查，不会把 pipeline-only 条目升级为作者一手 generated seed。

| recommended_role | 数量 | 当前含义 | 后续影响 |
|---|---:|---|---|
| 🟢 `final_pool_ready` | 3 | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` 已具备 committed raw、typed locator 与 trace verified generated pair；许可/再分发不再作为升绿 blocker，后续论文引用原作即可 | 可作为种子候选，但需按各自 caveat 选样 |
| 🟡 `conditional_final_pool` | 1 | `ttool-ai-smd-subset` 已有一手 `NL + generated TTool XML` 与 validator trace，但仍需 SMD/T0 切片、时间/信号/guard/action 规范化与 incoherency 泄漏隔离 | 条件候选 / 转换器压力源，不计现成 final pool |
| 🟠 `pipeline_only` | 2 | `fsm-bench-20` 有固定 NL/prompt/schema/code；`designing-fsm-gpt4` 有固定作者源码与初始调用连通性检查 但 NL 是运行时合成；二者都没有作者公开 generated `STM_0` | 只能后续本项目复跑另建 seed，复跑输出必须另建 run record |
| ⚪ `paper_reconstructable` | 10 | 多数传统 use-case/statechart 工作只有论文示例 / 附录 | 不计现成 seed；可做 related / 手工构造线索 |
| 🔴 `related_only` | 0 | 当前主表无 related-only 登记条目；排除/哨兵留在未登记处置或相关文献区 | 不进 final pool |

硬性结论：上级 [selected_seed_examples/README.md](../../selected_seed_examples/README.md) 已保存四个 smoke 用代表性种子样例；四例只是后续工具链最小连通性自检输入，不是最终实验集合或主结果样本上限。旧 parquet / 缓存 / PR comment 只能作审计线索，不能替代一手 `assets/raw/`。🟢 表示可回溯复验，不表示无 synthetic、非控制系统、样本少或泄漏隔离等学术 caveat。

### 1.6.1 NL 数量与数据质量摘要

| 条目 | NL raw / unique | NL-only raw / unique | generated pair | 数据构造与质量结论 |
|---|---:|---:|---:|---|
| `unified-uml-multimodal-validation` | 999 / 999 | 10 / 10 | 989 | LLaMA-3.2-1B 合成 feature description，DeepSeek 生成 PlantUML；无重复 NL / 无 1×N；10 行生成失败只作审计；适合 synthetic stress，不是控制系统真实需求。 |
| `llms-emp-stm-subset` | 60 / 10 | 0 / 0 | 60 | `Experiment Results.xlsx` / `STM Results`；10 个需求描述 × 6 个 LLM 输出；只取 `Generation PlantUML`，reference/checking 列必须隔离；reference canonical case=10，exact unique reference PlantUML=11。 |
| `sefm-llm-state-machine` | 9 / 9 | 8 / 8 | 1 | 4open ZIP 有 9 个 NL、8 个 reference、1 个 SSC7 generated text output；只有 SSC7 可计 generated pair，其余 8 个无 generated 输出的 NL 中 7 个是 reference-only、1 个 ATAS 是纯 NL-only，不得冒充 generated `STM_0`。 |
| `fsm-bench-20` | 252 / 252 | 252 / 252 | 0 | Zenodo/GitHub release 有 requirements/prompt/schema/code，但未公开 generated `STM_0`；全部 NL 当前只能作为 pipeline-only / 复跑来源。 |
| `designing-fsm-gpt4` | 0 / 未知 | 未知 / 未知 | 0 | 作者源码可运行时合成 DFSM / Mealy 英文描述并调用 LLM 生成 CSV；无冻结 NL corpus、无作者一手 generated pair。当前只登记源码与初始调用连通性检查，若后续使用需本项目 run record 记录随机种子与生成出的 NL。 |

## 1.7 代表性种子样例摘要

smoke 用代表性样例目录见上级 [selected_seed_examples/README.md](../../selected_seed_examples/README.md)。本 SUMMARY 只保留结论摘要：

| 分组 | 条目 | 裁决 | 关键 caveat |
|---|---|---|---|
| final seed pool | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` | 进入当前一手 seed 池 | 分别保留 reference/checking 隔离、SEFM 单例、synthetic/non-control-domain caveat。 |
| conditional seed pool | `ttool-ai-smd-subset` | 条件进入代表性样例集合 | 需 SMD/T0 切片、时间/信号/guard/action 规范化与 incoherency 泄漏隔离。 |
| pipeline-only supplement | `fsm-bench-20`、`designing-fsm-gpt4` | 不进入 author first-source final pool | 只有 NL/code/prompt/schema 或未配对 run artifacts；复跑必须另建 run record。 |

⚠️ **本段原写的「固定 smoke 用代表性样例集合」四例已不存在，四个链接全部指向已删除的目录，故删去。**
它们是 `llms-emp-deepseek-microwave` / `llms-emp-gpt4o-hldcs` / `llms-emp-kimi-autonomous-collision` / `sefm-ssc7-umple`；
`ttool-automatedbraking-xml` 与 `unified-uml-synthetic-0000` 当时已被移出该四例。

**现状**：[../../selected_seed_examples/](../../selected_seed_examples/) 下是 **60 个 `llms_emp_feedback_final_NNNN/`**，
全部来自 [llms-emp-stm-subset/](./llms-emp-stm-subset/)，即论文语料本身（实验网格 54 个）。
四例 smoke 时代已经过去，替换样例的旧流程随之作废；语料变更现在要回到
[REGISTRY.md](./REGISTRY.md)、条目 `assets/` 与 [../../pipeline/representation/](../../pipeline/representation/) 的证据目录同步。

## 2. 关键统计表

| 指标 | 数量 | 可复算位置 | 注意事项 |
|---|---|---|---|
| 去重候选 | 47 | §5 候选全集；[归档 candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-candidate-matrix.md) | R1.7 有界快照 v4。 |
| 筛查入账 | 47 | [归档 screening_ledger.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-screening-ledger.md)；§14 迁移表 | 与候选 ID 一一对应。 |
| 单条目证据目录 | 36 | §8 本地证据容器表；`find corpora/seed_library -mindepth 1 -maxdepth 1 -type d` | `fsm-bench-20` 是 仅制品 / 流水线备选。 |
| R1.7 检索轮次哨兵 | 8 | §11 检索覆盖摘要；[归档 search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/) | archive 另含 R1.6 与早期检索记录。 |
| 旧九生成基线映射 | 9/9 | §8.1 旧九映射；[归档 baseline_seed_method_crosswalk.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-baseline-seed-method-crosswalk.md) | 这是 seed 方法集合，不是 修正基线。 |
| 一手 registry 状态 | 3 / 1 / 2 / 10 / 0 | [REGISTRY.md](./REGISTRY.md) §2 | 🟢 final_pool_ready=3；🟡 conditional_final_pool=1；🟠 pipeline_only=2；⚪ paper_reconstructable=10；🔴 related_only=0。 |
| smoke 用代表性样例集合 | 4 | [selected_seed_examples/README.md](../../selected_seed_examples/README.md) | 当前 4 例均来自一手 `NL + generated STM_0` pair：LLMS-EMP 3 例、SEFM 1 例；Unified UML 与 TTool XML 已退出当前四例 selected smoke，只保留为后续 synthetic / XML 专项线索。仅作后续工具链最小连通性自检，不是最终实验集合。 |
| 人工下载队列状态 | 11 / 2 / 2 / 1 | §9 人工队列 | 已下载并复核 / 已下载后排除 / 元数据排除 / 仍受阻。 |

## 3. 定义、枚举与 emoji 口径

### 3.1 基本定义

| 概念 | 口径 |
|---|---|
| 严格种子 | 有证据表明 $STM_0$ 由自然语言需求 / 用例 / 场景 / 系统描述 / 文本规格生成、派生、抽取或人工建模得到。 |
| 目标 STM family | T0 范围内 FSM / HSM / EFSM / statechart；关键 timed / hybrid / protocol / process 行为不可隔离时不计主 seed。 |
| 作者原生 `<NL, STM_0>` pair | 作者或原始制品直接提供的输入 NL 与生成出的 $STM_0$ 配对；不是我们后续复跑、人工补造或从论文截图猜出的 pair。 |
| 可重建 `<NL, STM_0>` pair | 可以根据论文、附录、示例、图表或代码重建出来的配对，但作者未直接提供原始 pair。 |
| 配对索引 / case 对齐 | case id、文件名、表格编号或显式映射能稳定把 NL 与 STM_0 对齐。 |
| 可计种子候选 | 后续可作为 `NL + raw/source STM_0 -> issue discover` 实验输入来源；必须再做逐案例冻结、哈希、泄漏检查和数据质量 caveat 标注。 |

**一手 registry 角色定义**：从一手 registry 起，是否可作为现成 generated seed 只看 [REGISTRY.md](./REGISTRY.md) 的 `recommended_role` 与 validator 输出；旧“严格种子 / 条件种子”只保留为文献层 `NL -> STM_0` 方法证据标签，不能直接决定 实验输入。

| recommended_role | 含义 | 默认使用态度 |
|---|---|---|
| 🟢 `final_pool_ready` | committed 一手 `NL + generated STM_0` 可通过 raw hash / locator / 文本回溯复验；许可 / 再分发不再作为升绿 blocker，论文中引用原作即可 | 可进入现成 seed pool；当前数量为 3 |
| 🟡 `conditional_final_pool` | 一手入口与 trace 强相关，但仍缺 SMD/T0 切片、泄漏隔离或质量抽检等 blocker | 当前数量为 1：`ttool-ai-smd-subset`；不计现成 final pool |
| 🟠 `pipeline_only` | 有 NL、prompt、schema 或代码，但作者未公开可回溯的 `<NL, generated STM_0>` pair；若源码包含未配对 run artifacts，也只能作审计线索 | 不计现成 seed；可后续由本项目复跑另建 seed |
| 🔵 `reference_only` | 有 `NL + reference STM`，不是 generated `STM_0` | 可做参考解 / 评价线索，不计 generated seed |
| ⚪ `paper_reconstructable` | 只有论文图示、附录或示例可重建 | 可做方法证据 / 人工构造线索，不计现成 seed |
| 🔴 `related_only` / `excluded` | 不满足当前一手 seed 条件 | 只作 related work / sentinel |

**历史文献结论类型定义**：以下四类是 早期文献层分类，用于解释上游 `NL -> STM_0` 生态，不等于 一手 registry 一手资源 eligibility。

| 类型 | 定义 | 典型用途 | 进入当前种子池的默认态度 |
|---|---|---|---|
| 严格种子 | 有较清楚证据表明存在 `NL -> STM_0`，且输出属于 T0 范围内 FSM / HSM / EFSM / statechart；若资源可用性、泄漏风险和数据质量 caveat 也可冻结，则最接近真实实验 seed。 | 作为 `NL + raw/source STM_0 -> issue discover` 的优先候选来源、论文 story 中的上游 seed 证据。 | 优先考虑，但仍需逐案例冻结 NL、STM_0、pair 对齐、许可、版本 / 哈希和泄漏边界。 |
| 条件种子 / 方法证据 | `NL -> STM_0` 关系基本成立，但存在合成 NL、只可论文级重建、需要切片、验证导向、中间层、可变性、完整原生 pair 未公开等限制。 | 作为候选 seed、方法证据、转换器压力或 related work 论证；用于说明上游 seed 生态比严格可用样本更宽。 | 不能自动进入当前种子池；必须先解决具体限制，或明确只作为方法证据 / 备选。 |
| 边界 / 相关工作 / 哨兵 | 与 `NL -> STM` 或状态机建模相关，但不满足当前 seed 定义；常见原因包括输入不是 NL-only、输出不是目标 STM family、方向相反、只是 protocol / standard-doc / behavior-tree / goal-model / sequence / formal-spec 中间链路。 | 用于 related work、边界论证和防误收，帮助说明哪些工作不能冒充本论文 seed。 | 默认不进入当前种子池；除非后续有独立证据证明可切出合格 `<NL, STM_0>` pair。 |
| 仅元数据 | 目前只有 BibTeX、DOI、标题或少量元信息，全文或关键制品未拿到，无法判断是否满足 `NL -> T0 STM-family`。 | 保留人工下载 / 后续核验队列，避免遗漏潜在证据。 | 不进入当前种子池，也不作为正向结论；只能标记为待核。 |

### 3.2 emoji 列口径

正式总账表中，emoji 列只放 emoji；中文释义集中放在本节和 [GUIDE.md](./GUIDE.md)。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达，❓表示待核，⚪表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 文献资格（非资源 eligibility） | 强方法证据：清楚满足 `NL -> T0 STM-family` | 条件方法证据：关系清楚但有 synthetic / 制品 / T0 等边界说明 | 扩展 / 边界证据：对方法或转换压力有价值 | 不满足或明确排除 | 待核 | 不适用 |
| T0 适配 | T0 明确 | 大体 T0，但需切片或少量格式转换 | 存在 timed / hybrid / protocol / 中间产物 风险 | 非 STM family 或不可隔离 | 待核 | 不适用 |
| 生成关系 | 明确 `NL -> STM_0` | 方向基本成立但需切片 / 初始输出隔离 | 只有间接、中间模型或 paper-level 重建线索 | 不是 `NL -> STM_0` | 待核 | 不适用 |
| 实验输入可用性（派生汇总） | 关键输入可直接冻结：NL 数据、STM_0 数据、作者原生 pair、可重建 pair、配对索引、版本 / 哈希均可支撑实验 | 关键输入基本可用但需抽取、切片或冻结版本 | 只可论文级重建或需要大量人工整理 | 关键输入不可得，不能直接做当前实验样本 | 待核 / 访问受阻 | 对该条目不适用 |
| 一手 registry 角色 | `final_pool_ready` | `conditional_final_pool` | `pipeline_only` / `paper_reconstructable` | `related_only` / `excluded` | 待核 | 不适用 |
| 泄漏风险 | 未见明显泄漏 | 需隔离 reference / repair / oracle 字段 | 泄漏风险高，必须强约束使用 | 无法隔离 | 待核 | 不适用 |

### 3.3 资源可获取性分级

本节专门解释第 7 节资产盘点里用到的资源状态。盘点对象包括论文本体、来源文档、生成/复现实验代码、NL 原始数据、STM_0 原始数据、作者原生 `<NL, STM_0>` pair、可重建 pair、配对索引、原始生成输出、评测结果 / 日志，以及许可、版本 / 哈希信息；**不是**本地 `seed_desc.md`、`artifacts.md` 是否存在。资源列只统计论文正文 / 脚注 / Data Availability / 参考文献、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手入口；本仓库已经缓存的 parquet、ZIP、代码、PDF、hash、截图或复现副本只能作为本地审计证据，不能把资源等级从 ❓/🔴 升成 🟡/🟢。整体实验输入可用性是派生汇总项，不能用单个“资源可用”emoji 代替，至少要同时检查 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引` 和 `版本 / 哈希`；许可 / 再分发只作来源说明和论文引用提醒，不作为升绿 blocker。

| 资源对象 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 论文本体 | 官方 PDF / 预印本 / 出版页可直接读取 | 需少量跳转、页面不稳或要登录 | 只能借助二手摘要、镜像或零散转引 | 当前无法获取 | 待核 | 不适用 |
| 来源文档 | 原始需求文档 / 标准 / 说明书可直接定位 | 可定位但需版本冻结或登录 | 只有论文转述或二手入口 | 不可得 | 待核 | 不适用 |
| 生成/复现实验代码 | 官方仓库可直接拉取并复用 | 可获取但需版本冻结、子模块或许可确认 | 仅有脚本片段、补丁或非完整复现材料 | 未公开或不可得 | 待核 | 不适用 |
| NL 数据 | 原始自然语言需求、用例或场景文本可直接使用 | 需抽取、切片或冻结版本 | 只能从论文或附录重建 | 不可得 | 待核 | 不适用 |
| STM_0 数据 | 作者原始 `STM_0` / 结构化输出可直接使用 | 需解析、切片或冻结版本 | 只能从图表、示例或截图重建 | 不可得 | 待核 | 不适用 |
| 作者原生 `<NL, STM_0>` pair | 作者原始配对可直接拿到 | 仅部分配对直接公开或需切片 | 只能从局部制品、截图或附录间接恢复 | 不可得 | 待核 | 不适用 |
| 可重建 `<NL, STM_0>` pair | 可从论文、附录、示例或代码稳定重建 | 需要人工整理或脚本核验才能重建 | 只能从高层描述或图表半自动恢复 | 不可得 | 待核 | 不适用 |
| 配对索引 / case 对齐 | case id、文件名或表格能稳定对齐 NL 与 STM_0 | 对齐关系存在但需脚本或人工核验 | 只能从论文示例推断 | 无法对齐 | 待核 | 不适用 |
| 原始生成输出 | 作者生成的 STM_0 文本、PlantUML、JSON、CSV 等原始输出可直接拿到 | 部分公开或需抽取 | 只有截图 / 图表 / 示例 | 不可得 | 待核 | 不适用 |
| 评测结果 / 日志 | 原始结果表、日志、评分表或运行记录可直接复核 | 部分公开，需补整理或补切片 | 只有论文聚合指标 | 不可得 | 待核 | 不适用 |
| 许可 / 引用说明 | 官方许可明确或公开学术资源可引用原作 | 许可说明需补来源，但不影响一手 trace eligibility | 许可不明但来源可追踪，记录为 caveat | 来源不可追踪或非公开资源 | 待核 | 不适用 |
| 版本 / 哈希 | 发布版本、commit / 哈希或数据快照明确可追踪 | 可补冻结但当前未完全记录 | 只能以下载日期或页面状态弱冻结 | 无法冻结 | 待核 | 不适用 |

### 3.4 方法与资源枚举

| 字段 | 允许值 / 写法 | 说明 |
|---|---|---|
| 生成者 | 人工 / 规则算法 / NLP工具 / LLM / 多阶段流水线 / 混合 | 只描述 `STM_0` 产生方式；不把后续 修正循环 混入 seed。 |
| LLM参与 | 是 / 否 / 可能 / 不适用 | “可能”必须有证据不足说明。 |
| NL类型 | 需求文本 / 用例 / 场景文本 / 系统描述 / 标准文档 / 合成需求 / 来源文档 / 非NL | 用中文写，不再使用 `非结构化` 等英文短语。 |
| STM类型 | FSM / HSM / EFSM / UML statechart / SysML STM / PlantUML / Mermaid / Umple / 协议FSM / 非STM | 协议FSM、非STM默认不计控制系统四例。 |
| 资源列 | 论文 / 来源文档 / 生成代码 / NL 数据 / STM_0 数据 / 作者原生 pair / 可重建 pair / 配对索引 / 原始生成输出 / 评测结果 / 许可 / 版本 / 哈希 | 资源可获取性面向后续实验可用资源，不等同于本地 `seed_desc.md` 是否存在；必须给论文正文 / 脚注 / Data Availability / 参考文献、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手可点击入口；本地缓存只作审计证据。 |

### 3.5 资源交接表列口径

| 列 | 口径 |
|---|---|
| NL公开 | 原始 NL 是否可直接拿到；不是我们后续复写出的 NL。 |
| NL唯一输入 | 在生成 $STM_0$ 时，NL 是否是唯一必要输入。 |
| 前置制品 | partial model、prompt chain、图形表示或其他前置资产是否参与。 |
| STM格式 | 目标输出是否属于 T0 范围内的 FSM / HSM / EFSM / statechart。 |
| 输出方言 | 具体输出方言或序列化形式，如 PlantUML、CSV、JSON、Mermaid 等。 |
| T0 | 是否满足 T0 边界。 |
| 生成者 | 只能取 LLM / 人工 / 规则算法 / 多阶段流水线 / 混合。 |
| LLM | 是否使用 LLM。 |
| 作者原生 pair | 原始 pair 是否直接可得。 |
| 可重建 pair | 是否可由论文 / 附录 / 示例稳定重建。 |
| 配对索引 | 是否有稳定的 case 对齐。 |
| 泄漏 | 是否存在 reference / repair / oracle 泄漏。 |
| 转换 | 是否需要格式转换或强前处理。 |
| 一手 registry role | 以 [REGISTRY.md](./REGISTRY.md) 的 `recommended_role`、eligible count、trace count 与 blocker 判断；不是旧四例候选单列。 |

## 4. 一手 registry 交接分组

本节只给后续动作分组；逐条事实、eligible count、trace count、NL 数与 caveat 以 [REGISTRY.md](./REGISTRY.md) 为准。当前已有 3 个 🟢 `final_pool_ready` 条目与 1 个 🟡 `conditional_final_pool` 条目；这表示一手 `NL + generated STM_0/XML` 可回溯复验，不表示没有 synthetic、非控制系统、样本少、切片或泄漏隔离等学术 caveat。四个代表性样例 仍需后续逐案例冻结，四例也不是最终实验规模上限。

| 分组 | 候选 | 当前用途 | 进入当前种子池前必须满足 |
|---|---|---|---|
| 🟢 可直接复验但需按 caveat 选样 | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` | 已有 committed 一手 raw、typed locator、hash / 文本回溯和 validator 复算，可作为种子候选池 | `llms-emp` 必须隔离 reference/checking 列；`sefm` 只能计 SSC7 generated pair，其余 8 个无 generated 输出的 NL 中 7 个只作 reference-only、1 个只作纯 NL-only；`unified` 必须标注 synthetic / 非控制系统 / 无逐行 validation score |
| 🟡 条件一手 / 转换器压力候选 | `ttool-ai-smd-subset` | 有一手 `NL + generated TTool XML`，但 XML 是完整 TTool/SysML/AVATAR 工件，不是纯 T0 STM | 先冻结 SMD/T0 切片、时间/信号/guard/action 规范化与 incoherency 泄漏边界，切片产物另建 run record |
| 🟠 复跑构造候选 | `fsm-bench-20`、`designing-fsm-gpt4` | 有 NL / prompt / schema / code 或运行时 NL generator，但无作者公开 generated `STM_0`；可由本项目复跑另建 seed | 复跑必须保存 run record、模型、prompt、raw output、hash 与 eligibility，不得冒充作者原生 seed；`designing-fsm-gpt4` 还需记录 runtime synthetic NL 随机种子 |
| ⚪ 论文级重建 / 方法证据 | `automated-transition-use-cases-uml-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`rscharter-statechart-elements` 等 | 支撑 related work、转换器压力、人工构造线索 | 若要升级为 seed，必须新建 registry + assets + validator，而不是只引用论文图示 |
| 🔴 相关工作 / 排除哨兵 | repair-only、protocol / standard-doc / sequence / formal-spec 等 | 防误收与 related work 定位 | 默认不进入当前种子池 现成 seed；除非后续找到一手 generated pair 并重新登记 |

## 5. 候选全集：基础事实与资格矩阵（47 行）

本节把旧宽表拆成多张窄表。§5 只记录元数据、输入输出、生成关系和资格；§7 另列资源可获取性；§8 只列本地证据容器完整性。更细历史原表见 [归档 candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-candidate-matrix.md)。 `证据` 列只提供来源指针或本地分析入口，不代表对应外部资源已经可获取，资源状态必须回到 §7 判读。

| ID | 年份 | 来源批次 | NL类型 | STM类型 | T0 | 关系 | 文献资格 | 入池资格 | 当前角色 | 主要风险 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 2026 | 旧基线 / 复现 | 系统描述 | UML statechart / Umple | 🟢 | 🟢 | 🟢 | 🟢 | 一手 registry `final_pool_ready` | 4open ZIP 已 committed，SSC7 generated pair trace verified，eligible=1；另有 7 个 reference-only + 1 个 ATAS 纯 NL-only caveat；assets 见 [assets/README.md](./sefm-llm-state-machine/assets/README.md) | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | 2024 | 旧基线 / 复现 | 需求文本 | SysML / PlantUML STM | 🟡 | 🟢 | 🟢 | 🟢 | 一手 registry `final_pool_ready` | Google Drive workbook 已 committed，60 条 generated PlantUML trace verified；10 个唯一 NL × 6 个 LLM；R5.5 复核为 mixed：8 T0 / 1 T0.5 / 1 T1，Digital Camera 仅作 supplementary stress；详见 [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)；需隔离 reference / checking 列；reference canonical case=10、exact unique reference PlantUML=11 | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | 2026 | 旧基线 | 运行时合成需求 | DFSM / Mealy CSV | 🟢 | 🟢 | 🟡 | 🟠 | 一手 registry `pipeline_only` / NL+源码条件可复跑 | 作者源码已按 commit 固定并完成连通性检查；NL 是 runtime synthetic，不是冻结 corpus；无作者发布 pair，复跑输出需 run record | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | 2026 | R1.6 + HF 制品 | 合成需求 | PlantUML | 🟢 | 🟢 | 🟡 | 🟢 | 一手 registry `final_pool_ready` | HF parquet 999 行已全量 trace verified，989 条有效 PlantUML；synthetic / 非控制系统 / 无逐行 validation score caveat | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |
| `fsm-bench-20` | 2026 | R1.6 + Zenodo/GitHub | 需求文本 | FSM JSON | 🟢 | 🟢 | 🟢 | 🟠 | 一手 registry `pipeline_only` | 公开包缺作者 generated `STM_0`；需本项目复跑另建 seed | [seed_desc](./fsm-bench-20/seed_desc.md) |
| `ttool-ai-smd-subset` | 2024 | 旧基线 / 复现 | 系统规范 | SysML/TTool XML | 🟡 | 🟡 | 🟠 | 🟡 | 一手 registry `conditional_final_pool` / 转换器压力 | 6 组一手 `NL + generated TTool XML` 已 trace verified；需切出 SMD/T0 并处理时间 / 信号 / guard/action / incoherency 边界 | [seed_desc](./ttool-ai-smd-subset/seed_desc.md) |
| `fsm-gen-iec-61499` | 2025 | 旧基线 / R1.6全文 | 工业自动化需求 | FSM / IEC 61499 ECC | 🟡 | 🟡 | 🟡 | 🔴 | 私有制品边界 | 初始 STM 与 refinement 难隔离 | [seed_desc](./fsm-gen-iec-61499/seed_desc.md) |
| `ijisrt-uml-state-diagrams-llm` | 2026 | R1.6全文 | 系统描述 / prompt | UML statechart / PlantUML | 🟢 | 🟢 | 🟢 | 🔴 | 仅论文 近期证据 | 案例偏 玩具级 且无 原始输出 | [seed_desc](./ijisrt-uml-state-diagrams-llm/seed_desc.md) |
| `umple-nl-state-machine` | 2024 | 旧基线 | 需求文本 | Umple state machine | 🟢 | 🟢 | 🟢 | 🔴 | 仅论文 种子证据 | 可作手工重建线索 | [seed_desc](./umple-nl-state-machine/seed_desc.md) |
| `req-mermaid-statechart` | 2025 | 旧基线 | 汽车产品功能需求 | Mermaid statechart | 🟡 | 🟡 | 🟡 | 🔴 | 私有数据边界 | 任务贴合但不可复验 | [seed_desc](./req-mermaid-statechart/seed_desc.md) |
| `pushing-generative-envelope-mbse` | 2025 | 旧基线 / 仅论文 | MBSE题项 | SysML STM | 🟢 | 🟢 | 🟡 | 🔴 | 仅论文 prompt / temperature 参考 | — | [seed_desc](./pushing-generative-envelope-mbse/seed_desc.md) |
| `from-use-cases-to-statecharts` | 2001 | 旧基线 | 用例 | UML statechart | 🟡 | 🟡 | 🟡 | 🔴 | 经典文献 | statechart 是中间产物 | [seed_desc](./from-use-cases-to-statecharts/seed_desc.md) |
| `beyond-scenarios-state-models` | 2004 | 旧基线 | 受限英语用例 | HFSTM | 🟢 | 🟡 | 🟡 | 🔴 | 经典文献 | `paper_content` 质量差，需 PDF 核验 | [seed_desc](./beyond-scenarios-state-models/seed_desc.md) |
| `executable-state-machines-structured-text` | 2019 | 旧基线 | 结构化需求 / SPS | executable FSM | 🟢 | 🟠 | 🟡 | 🔴 | NL->SPS 有人工步骤 | 弱 seed 相关工作 | [seed_desc](./executable-state-machines-structured-text/seed_desc.md) |
| `maritaca-use-case-behavior-models` | 2017 | R1.6 经典检索 | 半结构化用例 | UML state machine | 🟢 | 🟢 | 🟢 | 🔴 | 一手 registry `paper_reconstructable` | 作者 artifact 403；machine-readable native pair / 代码未冻结 | [seed_desc](./maritaca-use-case-behavior-models/seed_desc.md) |
| `dependable-product-families-usecases-state-machines` | 2016 | R1.6 经典检索 | 受限用例 + variability | UML state machine / EFSM | 🟡 | 🟢 | 🟡 | 🔴 | 一手 registry `paper_reconstructable` | variability 需切片；pair/code 未公开 | [seed_desc](./dependable-product-families-usecases-state-machines/seed_desc.md) |
| `automated-transition-use-cases-uml-sm` | 2011 | 外部检索 | 用例 | UML state machine | 🟡 | 🟢 | 🟡 | 🔴 | 一手 registry `paper_reconstructable` | 论文 [DOI](https://doi.org/10.1007/978-3-642-21470-7_9)；附录可重建局部 pair，原生 pair / 代码 / 版本未冻结 | [seed_desc](./automated-transition-use-cases-uml-sm/seed_desc.md) |
| `execution-nl-req-bt-sm` | 2012 | 外部检索 | 需求文本 | 行为树 -> FSM | 🟢 | 🟠 | 🟠 | 🔴 | BT 中间产物 / 转换链证据 | BT2SMExamples 链接不稳定；不计主 seed | [seed_desc](./execution-nl-req-bt-sm/seed_desc.md) |
| `completion-sysml-gwt` | 2024 | 外部 / 旧基线 | GWT需求 + partial model | SysML transitions | 🟠 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 依赖已有 partial model | [seed_desc](./completion-sysml-gwt/seed_desc.md) |
| `towards-automatic-model-completion` | 2022 | R1.7人工复查 | GWT需求 + partial SMD | SysML STM 片段 | 🔴 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 不是 initial `NL -> STM_0` | [seed_desc](./towards-automatic-model-completion/seed_desc.md) |
| `scenarios-statecharts-interrelated` | 待核 | 旧基线 | 结构化 scenario / event trace | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | 输入不是自然语言需求文本 | [seed_desc](./scenarios-statecharts-interrelated/seed_desc.md) |
| `generating-statechart-designs-from-scenarios` | 2000 | 外部检索 | sequence / scenario | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | sequence/scenario 输入 | https://doi.org/10.1145/337180.337217 |
| `synthesis-revisited-scenario-based` | 2005 | 外部 / 旧基线 | LSC / MSC 形式化场景 | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` | — | https://doi.org/10.1007/978-3-540-31847-7_18 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 2002 | 外部检索 | scenario / co-evolution | statechart | ❓ | 🔴 | 🔴 | 🔴 | 反向边界哨兵 | 仅二手 Academia PDF；方向是 statechart/scenario 协同与原型验证，不是 NL->STM | [seed_desc](./requirements-analysis-prototyping-scenarios-statecharts/seed_desc.md) |
| `nl-standard-docs-state-machines` | 2018 | 外部检索 | 标准文档 | state machine | 🟡 | 🟢 | 🟠 | 🔴 | 标准文档哨兵 | 论文 [DOI](https://doi.org/10.2514/1.I010525)；ECSS/PUS 标准为引用来源文档，原始输出包未公开 | [seed_desc](./nl-standard-docs-state-machines/seed_desc.md) |
| `semi-auto-efsm-standard-docs` | 2015 | R1.6 protocol search | 标准文档 | EFSM | 🟢 | 🟢 | 🟠 | 🔴 | 标准文档哨兵 | 论文 [DOI](https://doi.org/10.1109/DSN-W.2015.17)；ECSS/PUS 为引用标准，code/data 未公开 | [seed_desc](./semi-auto-efsm-standard-docs/seed_desc.md) |
| `statechart-use-case-validation-event-driven` | 2012 | R1.6 Crossref | use-case model | UML statechart | 🟢 | 🟢 | 🟡 | 🔴 | 一手 registry `paper_reconstructable` | 论文 [DOI](https://doi.org/10.1145/2245276.2231947)；[RealState](http://openseminar.org/se/) 为案例入口，图示可重建 pair；原生数据包/代码未公开 | [seed_desc](./statechart-use-case-validation-event-driven/seed_desc.md) |
| `rscharter-statechart-elements` | 待核 | R1.6 Crossref | 需求规格 | UML statechart 元素 | 🟢 | 🟡 | 🟡 | 🔴 | 一手 registry `paper_reconstructable` | 论文 [SSRN](https://papers.ssrn.com/abstract=4964857)；PuRE 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.1414117)；增强 pair 未公开 | [seed_desc](./rscharter-statechart-elements/seed_desc.md) |
| `most-states-modes` | 2024 | 外部检索 | 需求文本 | 状态/模式形式化模型 | 🟠 | ❓ | 🟠 | 🔴 | 相关工作 / 形式化 | 论文 [DOI](https://doi.org/10.1145/3640822)；工具 [GitHub](https://github.com/liuyinling/MoSt-Modeling-Tool.git) 与例子支撑 MoSt/NuSMV，不是直连 NL->STM | [seed_desc](./most-states-modes/seed_desc.md) |
| `sysmlv2-formalized-requirements` | 2025 | 外部 / 旧基线 | 需求 + temporal logic | SysML v2 / 形式化模型? | 🟠 | 🟠 | 🟠 | 🔴 | LTL / 形式化 风险高 | — | `baselines/enhancing-model-based-development-formalized-requirements/` |
| `protocol-flowfsm-sentinel` | 2024 | 旧基线 / 协议域 | RFC / 协议文本 | 协议 FSM | 🟠 | 🟡 | 🔴 | 🔴 | `X_PROTOCOL` | 保留方法证据，不计控制系统四例 | `baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/` |
| `3gpp-protocol-sentinel` | 2024 | 旧基线 / 协议域 | 3GPP标准文本 | 协议 FSM | 🟠 | 🟡 | 🔴 | 🔴 | `X_PROTOCOL` | 保留 ensemble / span grounding 线索 | `baselines/automated-extraction-protocol-state-machines-3gpp-specifications/` |
| `source-autonomous-driving-hsm` | 待核 | sources | 来源文档 | HSM | 🟢 | ⚪ | ❓ | 🔴 | 本项目构造 来源候选 | 需构造 STM0 并防泄漏 | sources 线索 |
| `source-rotorcraft-uas-hsm` | 待核 | sources | 来源文档 | HSM | 🟢 | ⚪ | ❓ | 🔴 | 本项目构造 来源候选 | 需构造 STM0 | sources 线索 |
| `source-smarthand-hsm` | 待核 | sources | 来源文档 | HSM | 🟢 | ⚪ | ❓ | 🔴 | 本项目构造 来源候选 | 需查目录名与证据 | sources 线索 |
| `source-hfsm-human-robot` | 待核 | sources | 来源文档 | HSM | 🟢 | ⚪ | ❓ | 🔴 | 本项目构造 来源候选 | 需构造 STM0 | sources 线索 |
| `source-avp-hsm` | 待核 | sources | 来源文档 | HSM | 🟢 | ⚪ | ❓ | 🔴 | 本项目构造 来源候选 | 需防停车趋同 | sources 线索 |
| `nlp-req-formalization-testcase-generation` | 2021 | R1.7 CEUR全文 | 需求文本 | IRDL -> UML statechart | 🟠 | 🟠 | 🟡 | 🔴 | 仅论文 严格证据 | IRDL/sequence 中间产物 | [seed_desc](./nlp-req-formalization-testcase-generation/seed_desc.md) |
| `statistical-usage-testing-uml` | 2003 | R1.7 经典全文 | 用例 + domain class model | UML statechart / 使用图 | 🟢 | 🟠 | 🟡 | 🔴 | 仅论文 严格证据 | 需要 refinement / domain model | [seed_desc](./statistical-usage-testing-uml/seed_desc.md) |
| `unified-use-case-statecharts` | 2007 | R1.7 经典全文 | SRS use cases | 统一用例 statechart | 🟢 | 🟠 | 🟡 | 🔴 | 仅论文 / manual UCUM statechart | — | [seed_desc](./unified-use-case-statecharts/seed_desc.md) |
| `statechart-codesign-usecases` | 2003 | R1.7 经典全文 | 用例 / 用例图 | UML statechart / 子 statechart | 🟢 | 🟡 | 🟡 | 🔴 | 仅论文 | sequence diagram 路径与人工方法边界说明 | [seed_desc](./statechart-codesign-usecases/seed_desc.md) |
| `object-models-uml-embedded` | 2004 | R1.7 经典全文 | textual use case | UML statechart | 🟢 | 🟡 | 🟡 | 🔴 | 仅论文 | object-model 目标且无制品 | [seed_desc](./object-models-uml-embedded/seed_desc.md) |
| `integrating-graphical-nl-specifications` | 2016 | R1.7 边界全文 | NL + 已有图形表示 | 图形表示输入 | 🔴 | 🔴 | 🔴 | 🔴 | `X_COEXIST_ONLY` | 类 statechart 对象 不是目标输出 | [seed_desc](./integrating-graphical-nl-specifications/seed_desc.md) |
| `specification-based-verification-usecase-sm` | 2008 | R1.7 边界全文 | 半形式化用例 | 验证用 state machine | 🔴 | 🔴 | 🔴 | 🔴 | `X_COEXIST_ONLY` | state machine 是验证执行机制 | [seed_desc](./specification-based-verification-usecase-sm/seed_desc.md) |
| `executable-use-cases-domain-machine-specifications` | 2004 | R1.7 manual 候选 | executable use cases | machine specifications | ❓ | ❓ | ❓ | 🔴 | BibTeX-only / PDF 仍受阻 | 出版商封闭；人工下载队列 | [seed_desc](./executable-use-cases-domain-machine-specifications/seed_desc.md) |
| `web-tool-goal-statechart-derivation` | 2015 | R1.7 manual 候选 | 目标模型 / 需求模型 | statechart | ❓ | 🟠 | ❓ | 🔴 | 目标模型 / statechart 哨兵 | 论文 [DOI](https://doi.org/10.1109/RE.2015.7320444)；[supplement](http://www.cin.ufpe.br/~ler/supplement/re2015/) 可定位；非 NL-only | [seed_desc](./web-tool-goal-statechart-derivation/seed_desc.md) |
| `ucgen-usecase-descriptions` | 2026 | R1.7 排除 | 需求规格 | 用例文本 | ⚪ | 🔴 | 🔴 | 🔴 | 输出非 STM | 不进入 seed | Crossref textual usecase round |

## 6. 一手 registry handoff / caveat 明细

本节替代旧“可计种子候选 4 条”口径。当前 **final_pool_ready=3，conditional_final_pool=1，pipeline_only=2**；前三项是可回溯复验的现成 generated seed 候选，TTool-AI 是条件一手 XML 候选，pipeline-only 条目只能由本项目复跑后另建 seed。`复跑` 列只记录当前本项目对一手代码的最小连通性证据：`fsm-bench-20` 为单系统连通性检查，`designing-fsm-gpt4` 为初始生成连通性检查；二者仍不计现成 generated seed。

| ID | registry role | resource category | code | LLM | rerun | generated eligible | trace verified | 当前一手入口状态 | NL 数据 | STM_0 数据 | 主要 caveat | 下一步 |
|---|---:|---|---|---|---|---:|---:|---|---|---|---|---|
| `unified-uml-multimodal-validation` | 🟢 `final_pool_ready` | NL+STM一手 | 🔴未公开 | 🟢开权重可用 | ⚪不适用 | 989 | 999 | `downloaded` | HF parquet `input`；999 条 synthetic feature descriptions，989 条 eligible NL 均唯一，10 条 generation failure 为 NL-only / excluded | HF parquet `uml_code`；PlantUML StateDiagram；10 行 `No valid PlantUML code found.` 已列入 `excluded_pair_ids` 并排除 | synthetic_requirements_caveat；non_control_domain_quality_caveat；no_per_row_vlm_or_human_score；10_generation_failure_rows_excluded | 可作 synthetic UML state-diagram 连通性 / 压力 seed；不得包装为控制系统真实需求 |
| `llms-emp-stm-subset` | 🟢 `final_pool_ready` | NL+STM一手 | 🔴未公开 | 🟡混合 | ⚪不适用 | 60 | 60 | `downloaded` | Google Drive `Experiment Results.xlsx` / `STM Results` / `Requirement Description`；60 raw / 10 unique，10×6 LLM 输出 | `Generation PlantUML`；reference `PlantUML` 与 checking outputs 必须排除 | reference_and_postprocessed_columns_must_be_isolated | 可作强相关 LLM seed；转换器输入必须白名单只取 `Requirement Description + Generation PlantUML` |
| `sefm-llm-state-machine` | 🟢 `final_pool_ready` | NL+STM一手 | 🟢固定源码 | 🟡混合 | ⚪不适用 | 1 | 1 | `downloaded` | committed 4open ZIP 中 9 个 NL descriptions；只有 `SSC7_fall_2024` 有 generated 输出，其余 8 个无 generated 输出的 NL 中 7 个为 reference-only、1 个 ATAS 为纯 NL-only | committed 4open ZIP 中 `SSC7_single_prompt_*.txt` generated Umple / UML SM | only_ssc7_generated_pair_extracted_so_far；missing_generated_outputs_for_8_other_nl_descriptions；workbook_image_refs_without_actual_png_or_stm_text | 可作单例强相关 LLM seed；7 个 reference-only 与 1 个纯 NL-only 继续不可计 generated pair |
| `ttool-ai-smd-subset` | 🟡 `conditional_final_pool` | NL+STM一手 | 🟠片段/部分 | 🟡混合 | ⚪未尝试 | 6 | 6 | `downloaded` | 作者 GitHub 工件中的 `*.md` / `specification_*.md`；6 raw / 4 unique，主案例与 `incoherencies/` 变体分开 | 作者 GitHub 工件中的 TTool `.xml` generated artifacts；完整 TTool/SysML/AVATAR XML，非纯 T0 STM | requires_smd_t0_slice_contract；full_ttool_xml_not_pure_t0_stm；incoherency_outputs_may_mix_repair_scope；legacy_or_retired_model_drift | 条件可作 converter pressure；进入实验前必须另建 SMD/T0 切片 run record，不计现成 final pool |
| `fsm-bench-20` | 🟠 `pipeline_only` | NL+源码可复跑 | 🟢固定源码 | 🟡本地/代理可用 | 🟢单系统连通 | 0 | 0 | `downloaded` | Zenodo/GitHub benchmark systems / prompts | 作者未公开 generated `STM_0` | no_published_generated_stm0；rerun_required_before_seed | 若使用，必须由本项目复跑生成 `STM_0`，并写完整 run record；不能冒充作者原生 pair |
| `designing-fsm-gpt4` | 🟠 `pipeline_only` | NL+源码可复跑 | 🟢固定源码 | 🟠需代理/替代 | 🟢初始连通 | 0 | 0 | `downloaded` | 作者源码运行时合成 DFSM / Mealy 英文描述；没有冻结 NL corpus | 作者仓库含未配对 `generated_text.csv` / Graphviz run artifacts，但无冻结 `<NL, STM_0>` pair / locator；本地连通性检查只证明初始生成调用可走通 | unpaired_run_artifacts_excluded；runtime_synthetic_nl_not_frozen；no_frozen_pair_index；full_pipeline_timeout_risk；rerun_required_before_seed | 只作源码复跑线索；后续若使用必须记录随机种子、prompt、模型、raw output 与 run record |

## 7. 外部资源可获取性矩阵（47 行）

本节保留 早期外部入口盘点，用于说明论文 / 数据页 / artifact 页面是否可定位；它不等同于 一手 registry committed first-source eligibility。当前是否能计为一手 generated seed 必须回到 [REGISTRY.md](./REGISTRY.md) 的 role、eligible count、trace validator 与 blocker。

本表盘点“后续环节能否直接使用”的外部资源，而不是本地 `README.md`、`seed_desc.md`、`artifacts.md` 是否存在。资源状态口径见 §3.2 和 §3.3。实验输入至少要同时看 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`版本 / 哈希`；论文本体、生成代码和评测结果主要支撑复核、复现和相关工作分析。**资源可获取性升级为 🟢/🟡 前，必须基于全文阅读与外部资源页核验**，包括 DOI / 出版页、论文明确指向的作者仓库、数据集 / artifact 页面、附录、补充材料和许可页；不能只因为本地有 `seed_desc.md`、`artifacts.md`、PDF 缓存、parquet 缓存、ZIP 缓存、代码副本或本地 hash 就判断作者公开了可复用资产。若全文或资源页受阻，应保持 ❓/🔴 并在说明列写明阻塞来源。凡说明列提到可获取的一手资源，必须给出可点击链接。

| ID | 论文本体 | 来源文档 | 生成/复现实验代码 | NL 数据 | STM_0 数据 | 作者原生 pair | 可重建 pair | 配对索引 | 原始生成输出 | 评测结果 / 日志 | 许可 / 引用说明 | 版本 / 哈希 | 获取性说明 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 🟢 | ⚪ | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) 含 descriptions / reference / 生成输出；需冻结版本和哈希；公开学术资源按引用原作处理。 |
| `llms-emp-stm-subset` | 🟢 | ⚪ | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文正文/脚注给出数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；生成流水线代码未公开；公开学术资源按引用原作处理，主要风险是 reference/checking 列隔离。 |
| `designing-fsm-gpt4` | 🟢 | ⚪ | 🟢 | 🟠 | 🔴 | 🔴 | 🟠 | 🔴 | 🟠 | 🟠 | ❓ | 🟡 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；作者代码 [GitHub](https://github.com/Paul3246/nl2fsm) 已按 commit 固定并完成初始调用连通性检查；但 NL 是运行时合成，不是冻结发布 corpus，作者也未公开 generated `STM_0` pair。 |
| `unified-uml-multimodal-validation` | 🟢 | ⚪ | ❓ | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | ❓ | ❓ | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html) 的 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram)，合成边界、逐行可解析性与非控制系统适用性需标注；HF parquet 无逐行 VLM/human score。 |
| `fsm-bench-20` | ⚪ | ⚪ | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | ⚪ | 🟢 | 🟢 | 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.20517969) 与 [GitHub tag](https://github.com/cesar-andress/llm-fsm-local-benchmark/tree/v1.0.0) / [release](https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.0.0) 可用；作者冻结的生成 `STM_0` 输出未公开。 |
| `ttool-ai-smd-subset` | 🟢 | ⚪ | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | ❓ | 🟡 | 论文 [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645)；论文给出作者仓库 [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)，含 specification / XML / results.ods；SMD 需从联合 SysML 模型中切片。 |
| `fsm-gen-iec-61499` | 🟢 | ⚪ | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/)；核心实验数据 / 输出私有，只能作相关工作 / 私有边界。 |
| `ijisrt-uml-state-diagrams-llm` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.38124/ijisrt/26feb1435)；仅论文内示例可重建，无原始输出、代码或数据包。 |
| `umple-nl-state-machine` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 学位论文 [uOttawa record](https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6)；论文给需求和示例，完整 benchmark、输出包、评测脚本未公开。 |
| `req-mermaid-statechart` | 🟢 | ⚪ | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 学位论文 [Chalmers record/PDF](https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download)；Volvo / Car Weaver 核心 NL、人工 statecharts、评分与输出私有。 |
| `pushing-generative-envelope-mbse` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [ACL Anthology](https://aclanthology.org/2025.ranlp-1.137/) / [DOI](https://doi.org/10.26615/978-954-452-098-4-137)；论文内题项 / 表格可读，无逐次输出包、代码、数据包或补充材料。 |
| `from-use-cases-to-statecharts` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.2498/cit.2004.03.04) / 官方 [HRČAK PDF](https://hrcak.srce.hr/file/69340)；仅论文示例 / 手工推导线索，无作者原生机读 pair。 |
| `beyond-scenarios-state-models` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 PDF [uOttawa](https://www.site.uottawa.ca/~ssome/UCEdWeb/publis/ICSE02_Scenario_Workshop.pdf)；仅论文示例可读，无公开 UCEd 下载 / 机读 pair。 |
| `executable-state-machines-structured-text` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.5220/0007236601930200)；仅论文示例，无可直接复验数据包。 |
| `maritaca-use-case-behavior-models` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2017.33)；论文引用作者网页 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但按 403/受阻处理；只能从论文例子重建 pair，原生数据包、代码和许可未冻结。 |
| `dependable-product-families-usecases-state-machines` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [IEEE DOI](https://doi.org/10.1109/LADC.2016.28)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但按受阻处理；只能从论文中的 use case / variability / traceability matrix 重建 pair，原生代码、数据、版本 / hash 未公开。 |
| `automated-transition-use-cases-uml-sm` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | ❓ | ❓ | 论文 [Springer DOI](https://doi.org/10.1007/978-3-642-21470-7_9)；Appendix A/B 可重建局部 RUCM use case 与生成 state machine；未见论文一手原生 pair 包、完整代码、许可或 hash。 |
| `execution-nl-req-bt-sm` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0164121212001690) / [DOI](https://doi.org/10.1016/j.jss.2012.06.013)；论文示例可重建 NL/BT/SM，`BT2SMExamples.pdf` 入口不稳定。 |
| `completion-sysml-gwt` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1007/s10270-024-01228-3)；任务为 partial-model completion，不是 seed pair。 |
| `towards-automatic-model-completion` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2210.03388) / [DOI](https://doi.org/10.48550/arXiv.2210.03388)；任务为 repair-only / completion-only。 |
| `scenarios-statecharts-interrelated` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 PDF [Tsukuba](https://www.iplab.cs.tsukuba.ac.jp/paper/international/simona-isfst2001.pdf)；结构化 scenario / event trace，不是 NL seed pair。 |
| `generating-statechart-designs-from-scenarios` | 🟠 | ⚪ | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1145/337180.337217)；sequence/scenario 输入，不作为 seed pair。 |
| `synthesis-revisited-scenario-based` | 🟠 | ⚪ | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1007/978-3-540-31847-7_18)；形式化 scenario 输入，不作为 seed pair。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🟠 | ⚪ | 🔴 | ❓ | ❓ | 🔴 | 🔴 | 🔴 | ❓ | ❓ | ❓ | ❓ | 仅定位到二手 [Academia PDF](https://www.academia.edu/download/31191491/1.pdf)，正式 DOI / 作者页 / 出版页未定位；非 `NL -> STM_0`，未发现可直接复用的 pair。 |
| `nl-standard-docs-state-machines` | 🟢 | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [AIAA DOI](https://doi.org/10.2514/1.I010525)；ECSS/PUS 输入来源为 [ECSS-E-ST-70-41C 官方标准页](https://ecss.nl/standard/ecss-e-st-70-41c-space-engineering-telemetry-and-telecommand-packet-utilization-15-april-2016/) / [官方 PDF](https://ecss.nl/wp-content/uploads/2016/06/ECSS-E-ST-70-41C15April2016.pdf)；原始 TXT2SMM 输出包未公开。 |
| `semi-auto-efsm-standard-docs` | 🟢 | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2015.17)；ECSS/PUS 输入来源为 [ECSS-E-ST-70-41C 官方标准页](https://ecss.nl/standard/ecss-e-st-70-41c-space-engineering-telemetry-and-telecommand-packet-utilization-15-april-2016/) / [官方 PDF](https://ecss.nl/wp-content/uploads/2016/06/ECSS-E-ST-70-41C15April2016.pdf)；TXT2SMM / case data / generated EFSM package 未公开。 |
| `statechart-use-case-validation-event-driven` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [ACM DOI](https://doi.org/10.1145/2245276.2231947)；论文引用案例来源 [RealState](http://openseminar.org/se/)；图示可重建 pair，完整代码/数据/版本 / hash 未公开。 |
| `rscharter-statechart-elements` | 🟢 | 🟢 | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟡 | 🟡 | 论文 [SSRN](https://papers.ssrn.com/abstract=4964857)；输入来源 PuRE 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.1414117)；PuRE 许可 / 版本仅覆盖来源数据，不覆盖 RSCharter 增强 pair/code。 |
| `most-states-modes` | 🟢 | ⚪ | 🟢 | 🟢 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟢 | ❓ | 🟡 | 论文 [ACM DOI](https://doi.org/10.1145/3640822)；论文给出工具 [GitHub](https://github.com/liuyinling/MoSt-Modeling-Tool.git) 和相关 example；这些是 MoSt / NuSMV 形式化模型资源，非目标 T0 `STM_0`；仓库可定位但 release / tag / commit 尚未冻结。 |
| `sysmlv2-formalized-requirements` | 🟠 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1007/s10010-025-00806-1)；目前更像形式化 / LTL 相关证据。 |
| `protocol-flowfsm-sentinel` | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2507.11222)；输入 [RFC 959](https://www.rfc-editor.org/rfc/rfc959) 公开；论文给出的 [FlowFSM GitHub](https://github.com/YoussefMaklad/FlowFSM) 当前仅为仓库壳，作者 rulebook / GT / 输出未公开。 |
| `3gpp-protocol-sentinel` | 🟢 | 🟡 | 🔴 | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2510.14348)；3GPP 输入规格 [TS 24.501](https://www.3gpp.org/dynareport/24501.htm)、[TS 38.413](https://www.3gpp.org/dynareport/38413.htm)、[TS 29.244](https://www.3gpp.org/dynareport/29244.htm) 需锁版本；SpecGPT 代码 / GT / 输出未公开。 |
| `source-autonomous-driving-hsm` | ⚪ | 🟡 | ⚪ | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源论文 [DOI](https://doi.org/10.3390/app10103543)；仅可从论文正文 / 图表抽取系统描述与 HSM 线索，不是独立公开 NL/STM 数据集，也无作者原生生成 pair。 |
| `source-rotorcraft-uas-hsm` | ⚪ | 🟡 | ⚪ | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源论文 [DOI](https://doi.org/10.1002/rob.21898)；仅可从论文正文 / 图表抽取任务描述与 HSM 线索，不是独立公开 NL/STM 数据集；若使用需本项目后续构造并冻结。 |
| `source-smarthand-hsm` | ⚪ | 🟡 | ⚪ | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源论文 [DOI](https://doi.org/10.1186/1743-0003-8-29)；仅可从论文正文 / 图表抽取设备行为与 HSM 线索，不是独立公开 NL/STM 数据集；目录名与证据仍待核。 |
| `source-hfsm-human-robot` | ⚪ | 🟡 | ⚪ | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源论文 [DOI](https://doi.org/10.1109/IROS47612.2022.9981618)；仅可从论文正文 / 图表抽取协作装配任务与 HFSM 线索，不是独立公开 NL/STM 数据集；需本项目构造 `STM_0`。 |
| `source-avp-hsm` | ⚪ | 🟡 | ⚪ | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源论文 [汽车工程](https://www.qichegongcheng.com/CN/abstract/abstract1407.shtml) / [DOI](https://doi.org/10.19562/j.chinasae.qcgc.2023.02.009)；仅可从论文正文 / 图表抽取 AVP 决策规划与 FSM/HSM 线索，不是独立公开 NL/STM 数据集；需防停车场景趋同。 |
| `nlp-req-formalization-testcase-generation` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 PDF [CEUR](https://ceur-ws.org/Vol-2951/paper15.pdf)；论文内例子可重建，IRDL/sequence 中间产物与无机读输出限制使用。 |
| `statistical-usage-testing-uml` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 PDF [Uni Hamburg](https://www.inf.uni-hamburg.de/en/inst/ab/swk/research/publications/pdf/2003-sci2003-paper.pdf)；论文内 textual/tabular use case 与 statechart 示例可重建。 |
| `unified-use-case-statecharts` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1007/s00766-007-0053-1)；论文内 SRS use case / UCUM 示例可重建。 |
| `statechart-codesign-usecases` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1109/MEMCOD.2003.1210083)；论文内示例可重建，sequence 路径边界。 |
| `object-models-uml-embedded` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.2498/cit.2004.03.04) / [PDF](https://hrcak.srce.hr/file/69340)；论文内 textual use case / statechart 示例可重建。 |
| `integrating-graphical-nl-specifications` | 🟢 | ⚪ | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1109/REW.2017.50)；NL 与 graphical notation 共现，不是 `NL -> STM` 输出资源。 |
| `specification-based-verification-usecase-sm` | 🟢 | ⚪ | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1007/978-0-387-09661-2_4)；state machine 是 testbench 执行机制，不是目标 STM 数据。 |
| `executable-use-cases-domain-machine-specifications` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 仅 [DOI](https://doi.org/10.1049/ic:20040231) / BibTeX；出版商封闭，PDF / 全文仍待人工下载。 |
| `web-tool-goal-statechart-derivation` | 🟢 | 🟡 | 🔴 | ❓ | 🟠 | ❓ | ❓ | ❓ | 🟠 | 🟠 | ❓ | 🟠 | 论文 [IEEE DOI](https://doi.org/10.1109/RE.2015.7320444)；论文给出 [supplement](http://www.cin.ufpe.br/~ler/supplement/re2015/)；输入不是 NL-only。 |
| `ucgen-usecase-descriptions` | 🟠 | ⚪ | 🔴 | 🟠 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | 🟠 | 🔴 | 🔴 | 论文 [DOI](https://doi.org/10.1145/3796563.3796606)；输出是 use case descriptions，不是 STM。 |

## 8. 旧九生成基线映射与本地证据容器

### 8.1 旧九生成基线映射（9/9）

本节是旧九生成方法与 seed 文库条目的摘要映射；`资源摘要（非原子）` 只是阅读提示，正式资源状态以 §7 的原子列为准。`作者原生 pair` 只表示作者是否公开了原始 `<NL, STM_0>` 配对；论文 Listing / 图表 / 题项可重建但没有原始数据包时必须记为 🔴，可重建性另见 §7 的 `可重建 pair`。


| 原基线 | 种子方法 ID | 矩阵 ID | 单条目 | 输入 NL | 输出 STM | 生成方法 | 作者原生 pair | 资源摘要（非原子；一手入口） | 用途 |
|---|---|---|---|---|---|---|---|---|---|
| Structure- and Event-Driven Frameworks | `sefm-llm-state-machine` | `sefm-llm-state-machine` | [sefm-llm-state-machine](./sefm-llm-state-machine/) | 9 个 reactive-system / system descriptions；仅 SSC7 有 generated 输出（其余 7 个 reference-only + 1 个 ATAS 纯 NL-only） | UML state machine / statechart / Umple | LLM；单轮提示、结构驱动、事件驱动、混合策略 | 🟢 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) 含代码 / 数据 / F1 workbook；ZIP hash 已固化 | 一手 registry `final_pool_ready`；ZIP 已落盘且 SSC7 trace verified，eligible=1；其余 8 个无 generated 输出的 NL 不计 generated pair（7 个 reference-only + 1 个 ATAS 纯 NL-only） |
| LLMS EMP / SysML Behavior Models | `llms-emp-stm-subset` | `llms-emp-stm-subset` | [llms-emp-stm-subset](./llms-emp-stm-subset/) | `STM Results` 中 60 条 SysML 行为模型需求描述；10 个唯一 NL × 6 个 LLM 输出 | PlantUML / SysML STM | LLM；requirements + prompt；含 reference / checking 后结果，需隔离 | 🟢 | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)，已用 gdown 下载 workbook | 一手 registry `final_pool_ready`；60 条 generated PlantUML trace verified，使用时只取 `Generation PlantUML` |
| Designing FSM with GPT-4 | `designing-fsm-gpt4` | `designing-fsm-gpt4` | [designing-fsm-gpt4](./designing-fsm-gpt4/) | 运行时合成英文 DFSM / Mealy 需求描述 | CSV DFSM / Mealy | GPT-4/GPT-4o；初始生成 + oracle / 检查 / 修正实验 | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；作者代码 [GitHub](https://github.com/Paul3246/nl2fsm) 已按 commit 固定并完成连通性检查；无冻结 NL corpus / generated pair | 一手 registry `pipeline_only` / NL+源码条件可复跑；任何复跑输出另建 run record |
| TTool-AI | `ttool-ai-smd-subset` | `ttool-ai-smd-subset` | [ttool-ai-smd-subset](./ttool-ai-smd-subset/) | platooning、spacebasedsystem、AutomatedBraking 等自然语言系统规范 | SysML/TTool state-machine diagram subset | ChatGPT 3.5；语法/语义检查、JSON→TTool XML | 🟡 | 论文 [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645)；论文给出作者仓库 [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)，需分离 SMD；provider drift/许可待核 | 转换器压力 / 条件 seed |
| Umple thesis | `umple-nl-state-machine` | `umple-nl-state-machine` | [umple-nl-state-machine](./umple-nl-state-machine/) | 5 个自然语言 requirements 系统 | Umple textual state machine code | Llama 3；zero-shot、one-shot、RAG | 🔴 | 学位论文 [uOttawa record](https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6)；完整 benchmark、输出包、评测脚本未公开；仅论文示例可重建 | 仅论文 种子证据 |
| REQ automotive thesis | `req-mermaid-statechart` | `req-mermaid-statechart` | [req-mermaid-statechart](./req-mermaid-statechart/) | Volvo Cars / Car Weaver 产品功能自然语言需求 | Mermaid.js statechart | GPT-3.5/GPT-4/GPT-4o；数据增强 / 微调 / prompt | 🔴 | 学位论文 [Chalmers PDF](https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download)；核心 NL、人工 statecharts、专家评分和输出样本未公开 | 私有数据 相关工作 |
| Pushing the Generative Envelope | `pushing-generative-envelope-mbse` | `pushing-generative-envelope-mbse` | [pushing-generative-envelope-mbse](./pushing-generative-envelope-mbse/) | air purifier、vacuum 两个简短 MBSE 题项 | SysML STM diagrams | local LLM；Mixtral、Llama-3-Smaug；shot / CoT / temperature 消融 | 🔴 | 论文 [ACL Anthology](https://aclanthology.org/2025.ranlp-1.137/) / [DOI](https://doi.org/10.26615/978-954-452-098-4-137)；无代码、数据包、原始输出或许可；仅论文题项 / 表格可重建 | 仅论文 prompt / temperature 参考 |
| FlowFSM / Agentic Flow | `protocol-flowfsm-seed-method` | `protocol-flowfsm-sentinel` | 仅旧基线 | RFC 协议文档 | 协议 FSM / rulebook | LLM agent / CrewAI；prompt chaining、CoT | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2507.11222)；输入 [RFC 959](https://www.rfc-editor.org/rfc/rfc959) 公开；论文给出 [FlowFSM GitHub](https://github.com/YoussefMaklad/FlowFSM)，但作者 rulebook / GT / 输出未公开 | 协议域方法证据；不计控制系统四例 |
| SpecGPT / 3GPP extraction | `specgpt-3gpp-seed-method` | `3gpp-protocol-sentinel` | 仅旧基线 | 3GPP Release 17 标准文档 | 协议 FSM | GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2510.14348)；3GPP 输入规格 [TS 24.501](https://www.3gpp.org/dynareport/24501.htm)、[TS 38.413](https://www.3gpp.org/dynareport/38413.htm)、[TS 29.244](https://www.3gpp.org/dynareport/29244.htm) 需锁版本；代码 / GT / 输出未公开 | 协议域 ensemble / span grounding 参考 |

### 8.2 36 个本地证据容器完整性表

本表只检查本地证据容器是否完整，不代表外部资源可用性；外部资源以 §7 为准。

| slug | paper.pdf | paper_content.txt | bibtex.bib | seed_desc.md | artifacts.md | 说明 |
|---|---|---|---|---|---|---|
| `beyond-scenarios-state-models` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `completion-sysml-gwt` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `designing-fsm-gpt4` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `executable-state-machines-structured-text` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `from-use-cases-to-statecharts` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `fsm-bench-20` | ⚪ | ⚪ | 🟢 | 🟢 | 🟢 | 仅制品 / 流水线备选 |
| `fsm-gen-iec-61499` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `ijisrt-uml-state-diagrams-llm` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `integrating-graphical-nl-specifications` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `llms-emp-stm-subset` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `nlp-req-formalization-testcase-generation` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `object-models-uml-embedded` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `pushing-generative-envelope-mbse` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `req-mermaid-statechart` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `scenarios-statecharts-interrelated` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `sefm-llm-state-machine` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `specification-based-verification-usecase-sm` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `statechart-codesign-usecases` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `statistical-usage-testing-uml` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `towards-automatic-model-completion` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `ttool-ai-smd-subset` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `umple-nl-state-machine` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `unified-uml-multimodal-validation` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 本地缓存只作审计线索；外部 HF 资源以 §7 链接为准 |
| `unified-use-case-statecharts` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `automated-transition-use-cases-uml-sm` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 本地章抽取只作全文审计线索；外部资源以 §7 链接为准 |
| `dependable-product-families-usecases-state-machines` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `executable-use-cases-domain-machine-specifications` | ⚪ | ⚪ | 🟢 | 🟢 | 🟢 | BibTeX-only / PDF 仍受阻 |
| `execution-nl-req-bt-sm` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `maritaca-use-case-behavior-models` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `most-states-modes` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `nl-standard-docs-state-machines` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `rscharter-statechart-elements` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `semi-auto-efsm-standard-docs` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `statechart-use-case-validation-event-driven` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |
| `web-tool-goal-statechart-derivation` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |

## 9. 人工下载队列 / 阻塞项

### 9.1 状态分布

| 状态 | 数量 | ID | 影响 |
|---|---|---|---|
| 已下载并复核 | 11 | `automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`semi-auto-efsm-standard-docs`、`rscharter-statechart-elements`、`nl-standard-docs-state-machines`、`requirements-analysis-prototyping-scenarios-statecharts`、`most-states-modes`、`web-tool-goal-statechart-derivation` | 已下载全文并回填到候选 / 资源表，不再阻塞当前种子池。 |
| 已下载后排除 | 2 | `completion-sysml-gwt`、`towards-automatic-model-completion` | 已有全文并确认为 repair-only，不阻塞当前种子池。 |
| 元数据已足够排除 | 2 | `generating-statechart-designs-from-scenarios`、`ucgen-usecase-descriptions` | 元数据已足够排除，不阻塞当前种子池。 |
| 仍受阻 | 1 | `executable-use-cases-domain-machine-specifications` | 仍需人工下载全文；不作为当前种子池阻塞项。 |

### 9.2 当前 仍受阻 明细

本节只列仍需人工下载 / 仍受阻状态；下载全文后请继续回填 §5、§7 和单条目文件。

| ID | 标题 | 来源URL | 状态 |
|---|---|---|---|
| `executable-use-cases-domain-machine-specifications` | Executable use cases as links between application domain requirements and machine specifications | https://doi.org/10.1049/ic:20040231 | 仍受阻：出版商封闭；PDF 仍待人工下载。 |

### 9.3 人工下载 BibTeX 队列

人工下载用的 BibTeX 已集中到 [manual_download_queue.bib](./manual_download_queue.bib)。这是临时复制起点，不是正式引用库；下载成功后应在对应条目目录补 `paper.pdf` / `paper_content.txt`，并全文核验后再回填 `SUMMARY.md` §5 / §7 / §16。

| 文件 | 内容 |
|---|---|
| [manual_download_queue.bib](./manual_download_queue.bib) | `Jorgensen_2004_executable_use_cases_domain_machine_specifications` |

## 10. 排除证据 / 硬排除

### 10.1 排除码口径

| 排除码 | 常用别名 | 含义 |
|---|---|---|
| `X_PROTOCOL_FSM` | `X_PROTOCOL` | RFC / 3GPP / network 协议 FSM 或 标准/协议 风险。 |
| `X_PROCESS_MODEL` | `X_PROCESS` | BPMN / workflow / business process / resource-flow。 |
| `X_NON_STM_FORMALISM` | `X_FORMAL_SPEC` / `X_FORMAL_SPEC_ONLY` | Petri / CSP / Event-B / TLA+ / LTL/STL / 形式化 scenario 等非 STM 输出。 |
| `X_T1PLUS_TIMED_HYBRID` | `X_T1_PLUS` / `X_T1_PLUS_OR_HYBRID` | timed automata / hybrid / critical timeout 语义不可隔离。 |
| `X_SEQUENCE_ONLY` | `X_SEQUENCE_CLASS` | sequence diagram / MSC / LSC / structured scenario trace 输入或输出，不是 NL requirements -> STM。 |
| `X_REPAIR_ONLY` | `X_REPAIR_ONLY` | 已有 model / partial state machine completion、repair 或 refinement，不是 initial `NL -> STM_0`。 |
| `X_COEXIST_ONLY` | `X_NO_GEN_REL?` | 只有 NL 与 STM 共现，方向或生成关系不足。 |

### 10.2 排除 / sentinel 表

| ID | 排除码 | 触发对象 / 原因 | 角色 | 证据 |
|---|---|---|---|---|
| `protocol-flowfsm-sentinel` | `X_PROTOCOL` | RFC / network 协议 FSM；非控制系统 T0 seed | 协议域方法证据 / 防误收 | §5 / §7；旧基线 path |
| `3gpp-protocol-sentinel` | `X_PROTOCOL` | 3GPP 标准协议 FSM；非控制系统四例 | 协议域 ensemble / span grounding 线索 | §5 / §7；旧基线 path |
| `bpmn-process-sentinel` | `X_PROCESS` | BPMN / workflow / resource-flow 与 STM-family 不同 | 防误收 | [exclusion_ledger](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-06-18-24-exclusion-ledger.md) |
| `formal-spec-sentinel` | `X_FORMAL_SPEC` | Petri / CSP / Event-B / TLA+ / LTL/STL 或 形式化 scenario | 防误收 | [exclusion_ledger](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-06-18-24-exclusion-ledger.md) |
| `repair-only-sentinel` | `X_REPAIR_ONLY` | partial model completion / repair-only，不是 initial seed | 防误收 | `completion-sysml-gwt` / `towards-automatic-model-completion` |
| `most-states-modes` | `X_FORMAL_SPEC?` | states/modes 形式化，STM-family 未确认 | 相关工作 / 待核 | §5 / §7 |
| `sysmlv2-formalized-requirements` | `X_FORMAL_SPEC` / `X_T1_PLUS?` | requirements + temporal logic / 形式化 风险 | extended 边界 | §5 / §7 |
| `completion-sysml-gwt` | `X_REPAIR_ONLY` | 输入包含 partial SysML model / pre-existing states | completion 边界 | [seed_desc](./completion-sysml-gwt/seed_desc.md) |
| `scenarios-statecharts-interrelated` | `X_SEQUENCE_CLASS` | OMT event trace / structured scenario，不是 NL需求文本 | sequence 边界 | [seed_desc](./scenarios-statecharts-interrelated/seed_desc.md) |
| `generating-statechart-designs-from-scenarios` | `X_SEQUENCE_CLASS` | sequence / scenario -> statechart | sequence 边界 | DOI https://doi.org/10.1145/337180.337217 |
| `synthesis-revisited-scenario-based` | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` | LSC / MSC 形式化场景 | 形式化 scenario 边界 | DOI https://doi.org/10.1007/978-3-540-31847-7_18 |
| `requirements-analysis-prototyping-scenarios-statecharts` | `X_NO_GEN_REL?` | 方向疑似 statechart -> scenario/prototype | 共现 / 方向 边界 | 外部检索线索 |
| `semi-auto-efsm-standard-docs` | `X_PROTOCOL?` / `CONTROL_STANDARD_EXCEPTION_PENDING` | standard documents -> EFSM；控制标准例外未证明 | 标准/协议 sentinel | DOI https://doi.org/10.1109/DSN-W.2015.17 |
| `integrating-graphical-nl-specifications` | `X_COEXIST_ONLY` | NL 与 graphical notation 共现，类 statechart 对象 不是目标输出 | 边界 排除 | [seed_desc](./integrating-graphical-nl-specifications/seed_desc.md) |
| `specification-based-verification-usecase-sm` | `X_COEXIST_ONLY` / `X_NON_STM_FORMALISM?` | state machine 是 SystemC testbench 执行机制 | testbench 边界 | [seed_desc](./specification-based-verification-usecase-sm/seed_desc.md) |
| `towards-automatic-model-completion` | `X_REPAIR_ONLY` | partial SMD completion，不是 initial `NL -> STM_0` | repair-only 边界 | [seed_desc](./towards-automatic-model-completion/seed_desc.md) |
| `ucgen-usecase-descriptions` | `X_NON_STM_FORMALISM` | 输出是 use-case textual descriptions，不是 STM | 输出非 STM | Crossref textual usecase round |
| `web-tool-goal-statechart-derivation` | `X_SEQUENCE_ONLY?` / `X_COEXIST_ONLY?` | goal model -> statechart，不一定有 NL 输入 | 待核 边界 | DOI https://doi.org/10.1109/RE.2015.7320444 |

## 11. 检索覆盖摘要与归档入口

R1.7 检索轮次哨兵为 8；归档中还保留 R1.6 与早期检索记录。原始 JSONL / 轮次 Markdown 只作审计证据，当前结论以本 SUMMARY 为准。

| 轮次 | 来源 | 检索式 / 入口 | 原始命中 | 全文/制品 | 阻塞 / 早停 | 结论 |
|---|---|---|---|---|---|---|
| `r17-01-openalex-broad-nl-requirements` | OpenAlex | 宽口径 NL requirements / statechart / use-case 检索簇 | 95 | 0 | 宽检索噪声高 / 宽检索保留为排除证据 | 详见 [round-r17-01-openalex-broad-nl-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-01-openalex-broad-nl-requirements.md) |
| `r17-02-crossref-refined-usecase-statechart` | Crossref | use-case / statechart / requirements 精细检索 | 50 | 1 | 无全文/制品 / 精确 DOI/标题发现 | 详见 [round-r17-02-crossref-refined-usecase-statechart.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-02-crossref-refined-usecase-statechart.md) |
| `r17-03-crossref-textual-usecase-behavior` | Crossref | textual 用例文本 / behavior models / state machine | 30 | 0 | 输出非 STM 噪声为主；MARITACA 已由人工下载全文入库，旧轮次仅作历史发现入口 | 详见 [round-r17-03-crossref-textual-usecase-behavior.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-03-crossref-textual-usecase-behavior.md) |
| `r17-04-arxiv-llm-requirements` | arXiv | LLM + state machine / state diagram / requirements | 40 | 0 | 需求质量 / 切片 / 非 STM LLM 噪声 / 无新增 SA-1/2 种子 | 详见 [round-r17-04-arxiv-llm-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-04-arxiv-llm-requirements.md) |
| `r17-05-semanticscholar-阻塞项` | Semantic Scholar API | 6 检索簇 | 6 个错误 | 0 | HTTP 429 频率限制 / 降级到 OpenAlex/Crossref/arXiv/DBLP | 详见 [round-r17-05-semanticscholar-blocker.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-05-semanticscholar-blocker.md) |
| `r17-06-dblp-exact-title` | DBLP API | 12 精确标题人工 / 经典候选 | 429 / 连接限制前确认 3 条 | 0 | DBLP 频率/连接限制 / 仅元数据互证 | 详见 [round-r17-06-dblp-exact-title.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-06-dblp-exact-title.md) |
| `r17-07-classic-fulltext-wave` | 开放/出版商 PDF | 经典用例 / 嵌入式 / 测试生成全文波次 | 7 | 7 dirs | 均仅论文 / 两个硬边界 / 强化排除证据; 无新增 SA-1/2 | 详见 [round-r17-07-classic-fulltext-wave.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-07-classic-fulltext-wave.md) |
| `r17-08-manual-queue-artifact-recheck` | 出版商精确检索 + 制品检索 | R1.6 人工队列 + R1.7 新增人工候选 | 13 | 1 个新增下载目录 | 付费墙 / 需浏览器访问的开放入口 / 无制品 / 人工队列状态分布已更新 | 详见 [round-r17-08-manual-queue-artifact-recheck.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md) |

归档入口：

- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/)

## 12. 文献筛查与全文阅读 provenance 摘要

旧 `agent_provenance.md` 已归档为 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-15-49-35-agent-provenance.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-15-49-35-agent-provenance.md)。其记录范围仅限文献筛查、全文阅读、证据等级调整和研究性 阻塞项；不记录 PR review / ready / merge 进度。R1.7 最终整合输出为：47 候选 / 47 筛查 / 36 单条目目录；当时旧口径的主 / 条件主可计候选为 4；一手 registry 后当前一手 registry 口径改为 final_pool_ready=3、conditional_final_pool=1、pipeline_only=2。Semantic Scholar API 429 已记录并由 OpenAlex/Crossref/arXiv/DBLP exact-title 替代。

## 13. 关键风险与 使用建议

1. **当前有 3 个 🟢 `final_pool_ready`，但它们不是同质高质量控制系统池**：`llms-emp` 最贴近控制 / SysML 行为模型；`sefm` 只有 1 个 SSC7 generated pair；`unified` 规模大但 synthetic 且偏通用软件 feature。
2. **许可 / 再分发不再作为升绿 blocker**：这些对象来自公开论文、作者 artifact、HF、Google Drive 或 Zenodo 等公开学术资源，论文中规范引用原作即可；后续风险评估应集中在一手 trace、泄漏隔离、数据质量和领域适配。
3. **`llms-emp-stm-subset` 的主要风险是泄漏隔离**：60 条 workbook trace verified generated pair 可用，但必须只取 `Requirement Description + Generation PlantUML`；reference `PlantUML` 和 `Result with * Checking` 不得进入原始 `STM_0`。
4. **`sefm-llm-state-machine` 的主要风险是样本少和 reference/generated 边界**：ZIP 有 9 个 NL descriptions、8 个 reference solutions、1 个 generated text output；当前只有 SSC7 可计 generated pair，其余 8 个无 generated 输出的 NL 中 7 个是 reference-only、1 个 ATAS 是纯 NL-only。
5. **`unified-uml-multimodal-validation` 的主要风险是 synthetic / 非控制系统 / 无逐行 validation score**：HF parquet 999 行全量 trace verified，其中 989 行是有效 PlantUML generated pair，10 行生成失败已列入 `excluded_pair_ids` 并排除；可作 synthetic stress seed，不得包装为真实控制系统需求。
6. **`fsm-bench-20` 不能直接算作者 generated seed**：公开包有 dataset / prompt / schema / code，但缺作者冻结的 generated `STM_0` 输出；若使用必须由本项目复跑并保存 run record、prompt、模型、raw output、hash 与 eligibility。
7. **paper-reconstructable / related-only 不能替代现成样本**：论文图示、附录、旧缓存、人工重建、protocol / standard / sequence / repair-only 线索都不能绕过 registry + assets + validator。
8. **四例只是 后续开发阶段 代表性样例集合，不是最终实验规模上限**：最终实验池应继续扩大，但每个入池 pair 都必须满足一手来源和可审计 trace。
9. **旧 reproduction / project_ex1 只能作发现入口，不能作事实源**：本轮已在 [REGISTRY.md](./REGISTRY.md) §3.5 基于旧线索回到论文、作者制品、官方仓库、Google Drive、4open、HF 等一手入口，补充 LLMS-EMP、SEFM、TTool-AI、Nimbus、PSMBench、RFCNLP、Hermes 的追溯结论；旧 parquet / predictions / review extraction 不计入资源可用性、pair 数或升绿依据。LLMS-EMP 与 SEFM 已被当前 registry 通过一手来源正确吸收；TTool-AI 已登记为 conditional / 转换器压力源但不计现成 final pool；Nimbus 更适合 NL dataset / related work；protocol / RFC / cellular FSM corpus 不进入 paper1 seed 主池。

使用建议顺序：先从 `llms-emp` 选取若干控制 / SysML 行为模型样例，再用 `sefm` 的 SSC7 覆盖非结构化 reactive-system 描述与 Umple 转换压力，必要时引入 `unified` 做 synthetic PlantUML stress；若真实控制系统覆盖不足，再用 `fsm-bench-20` 复跑构造补充 seed，并保留完整 run record。

## 14. 迁移表

| 旧路径 / 对象 | 新路径 / 新章节 | 当前事实真源 | 迁移理由 |
|---|---|---|---|
| `seed_corpus/README.md` | 已删除纯跳转入口；历史材料保留在 archive | corpora/seed_library/README.md | 删除前向兼容壳，避免第二事实源。 |
| `seed_corpus/GUIDE.md` | `archive/.../legacy_ledgers/2026-06-14-15-49-35-seed-corpus-guide.md + corpora/seed_library/GUIDE.md` | corpora/seed_library/GUIDE.md | 旧规则归档，新规则按 SUMMARY-first 重写。 |
| `seed_corpus/SUMMARY.md` | `archive/.../legacy_ledgers/2026-06-14-15-49-35-seed-corpus-summary.md + corpora/seed_library/SUMMARY.md` | corpora/seed_library/SUMMARY.md | 旧总账归档，新总账承载所有横向事实。 |
| `candidate_matrix.md` | `archive/.../legacy_ledgers/2026-06-14-11-18-35-candidate-matrix.md；摘要进入 SUMMARY §5` | corpora/seed_library/SUMMARY.md | 47 条候选进入单一横向总账。 |
| `screening_ledger.md` | `archive/.../legacy_ledgers/2026-06-14-11-18-35-screening-ledger.md；47/47 进入 SUMMARY §2/§5/§14` | corpora/seed_library/SUMMARY.md | 候选 / 筛查 对齐哨兵可复算。 |
| `exclusion_ledger.md` | `archive/.../legacy_ledgers/2026-06-14-06-18-24-exclusion-ledger.md；摘要进入 SUMMARY §10` | corpora/seed_library/SUMMARY.md | 排除证据 直接可见。 |
| `manual_download_queue.md` | `archive/.../legacy_ledgers/2026-06-14-06-18-24-manual-download-queue.md；摘要进入 SUMMARY §9` | corpora/seed_library/SUMMARY.md | manual 阻塞项 直接可见。 |
| `baseline_seed_method_crosswalk.md` | `archive/.../legacy_ledgers/2026-06-14-11-18-35-baseline-seed-method-crosswalk.md；9/9 表进入 SUMMARY §8` | corpora/seed_library/SUMMARY.md | 旧九生成基线进入 seed 方法集合，不误作 修正基线。 |
| `seed_selection_candidates.md` | `archive/.../legacy_ledgers/2026-06-14-11-18-35-seed-selection-candidates.md；资源交接进入 SUMMARY §4/§6` | corpora/seed_library/SUMMARY.md | 代表性样例=4 交接可直接读取。 |
| `search_log.md / search_rounds/ / search_results/` | `archive/.../legacy_ledgers/2026-06-14-06-18-24-search-log.md`、`archive/.../search_rounds/`、`archive/.../search_results/`；摘要进入 SUMMARY §11 | corpora/seed_library/SUMMARY.md | 原始检索归档，搜索覆盖摘要当前可读。 |
| `agent_provenance.md` | `archive/.../legacy_ledgers/2026-06-14-15-49-35-agent-provenance.md；研究性审计摘要进入 SUMMARY §12` | corpora/seed_library/SUMMARY.md | 保留文献筛查 provenance，但不记录 PR 流程状态。 |
| `seed_corpus/papers/<slug>/` | `corpora/seed_library/<slug>/；本地证据容器表进入 SUMMARY §8` | corpora/seed_library/<slug>/ + SUMMARY §8 | 36 个单篇 / 制品证据容器迁入当前 seed library。 |

## 15. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-23 19:45:00 | 一手 registry：补齐资源类别 / 源码 / 论文 LLM 可用性口径，`fsm-bench-20` 与 `designing-fsm-gpt4` 统一为 `pipeline_only` 的 NL+源码可复跑线索；`ttool-ai-smd-subset` 已以一手 `NL+TTool XML` 登记为 `conditional_final_pool`，但不计现成 final pool。 |
| 2026-06-23 12:02:20 | 一手 registry：在 [REGISTRY.md](./REGISTRY.md) §3.5 基于旧 reproduction / project_ex1 线索回到一手入口，补充 LLMS-EMP、SEFM、TTool-AI、Nimbus、PSMBench、RFCNLP、Hermes 的追溯结论；明确旧 parquet / predictions / review extraction 只能作发现入口，不作资源事实源、pair 计数或升绿依据。 |
| 2026-06-22 19:40:00 | 一手 registry：修正 unified 计数口径为 raw=999、trace=999、eligible=989；用 gdown 下载 llms-emp Google Drive workbook 并抽取 60 条 generated PlantUML；公开学术资源按引用原作处理后，三条一手资源均为 final_pool_ready，并保留各自 caveat。 |
| 2026-06-15 15:05:00 | 补充 §3.1 最终结论类型定义，明确严格种子、条件种子 / 方法证据、边界 / 相关工作 / 哨兵、仅元数据四类与 当前 进入态度。 |
| 2026-06-15 14:23:39 | 补强 §16 结论总表，显式列出 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系与时间特性等级；将资源列改为一手可点击链接，并统一 `作者原生 pair` 与 `可重建 pair` 口径，避免本地缓存或论文级重建线索冒充公开原生资源。 |
| 2026-06-14 23:40:00 | 从 vpn-lab 全书 PDF 中抽取 Yue 2011 章节，`automated-transition-use-cases-uml-sm` 从 BibTeX-only 升级为 conditional seed；人工队列更新为 `11/2/2/1`，剩余队列只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | 接入 vpn-lab 人工下载 PDF/BibTeX，新增 12 个 evidence 目录，移除 SUMMARY 长 BibTeX 块并改链到 `manual_download_queue.bib`，补充 seed / 资源可用性结论总表。 |
| 2026-06-14 20:45:00 | 补充人工下载 BibTeX 队列，明确资源可获取性必须基于全文阅读与外部资源页核验，不能只看本地 repo 资源。 |
| 2026-06-14 20:35:00 | 修复 review 指出的 pair 口径同步问题，补入可重建 pair、作者原生 pair、配对索引与资源交接列，并把实验输入可用性标为派生汇总项。 |
| 2026-06-14 20:10:00 | 按 review I 级意见继续拆分资源矩阵，新增来源文档、STM_0 数据、配对索引、原始生成输出、评测结果 / 日志、许可、版本 / 哈希等列，并说明 实验输入可用性不能由单个资源 emoji 代替。 |
| 2026-06-14 19:30:00 | 继续中文化 SUMMARY，新增资源可获取性分级说明，细化候选矩阵中的当前角色与主要风险，并把资源盘点范围明确到论文本体、源码、NL 数据、STM 数据、作者原生 pair、实验结果和引用说明 / 版本 / 哈希。 |
| 2026-06-14 18:45:00 | 按最新审阅意见中文化 SUMMARY，拆分耦合列，新增 emoji 枚举口径与外部资源可获取性矩阵；明确本地证据容器表不等同于资源可用性。 |
| 2026-06-14 17:55:00 | 迁移旧 `seed_corpus/` 到 `corpora/seed_library/`；建立三件套；旧横向 ledger、检索轮次 / results 进入 archive；当前 SUMMARY 可复算 `47/47`、`36 dirs`、`9/9 映射`、代表性样例=4 和 人工队列状态。 |
| 2026-06-14 13:20:00 | 有界快照 v4：纠正 seed 方法集合 vs 代表性四例计数口径，补齐旧九 旧基线直接映射，新增 `pushing-generative-envelope-mbse`，扩展到 47 候选 / 47 筛查 / 24 单条目目录；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 12:10:00 | 有界快照 v3：扩展到 46 候选 / 46 筛查 / 23 单条目目录 / 8 R1.7 检索轮次；新增 经典全文波次、人工队列状态分布和 排除证据；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 03:55:00 | 有界快照 v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF 制品核验、search_rounds 与 代表性种子池冻结 交接。 |
| 2026-06-14 02:22:00 | 补齐 `req-mermaid-statechart` 单篇目录与 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 当前阻塞项交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |


## 16. `NL -> STM` 文献证据与 一手 registry 角色速览

本节给快速阅读用的结论表；**它不复制 [REGISTRY.md](./REGISTRY.md) 的逐条资源明细**。`文献层判断` 说明该工作是否展示了 `NL -> STM_0` 方法关系；`一手 registry role` 才决定当前能否作为一手 generated seed。

| ID | 文献层判断 | 一手 registry role | NL输入是什么 | STM输出是什么 | STM关键特性 | STM谱系 | 时间特性等级 | NL->STM 方式 | 当前资源结论 |
|---|---|---:|---|---|---|---|---|---|---|
| `unified-uml-multimodal-validation` | 条件方法证据 | 🟢 `final_pool_ready` | LLaMA 生成的 synthetic user-focused requirements / feature descriptions | PlantUML StateDiagram / `UMLCode_StateDiagram` | PlantUML 状态图文本；需标注 synthetic、非控制系统和无逐行 validation score caveat | UML state diagram / PlantUML statechart | T0-离散；未见显式时钟 | 多模型流水线：requirements -> PlantUML | HF parquet 999 行全量 trace verified，989 条有效 PlantUML；可作 synthetic stress，不作真实控制系统需求 |
| `llms-emp-stm-subset` | 强相关 LLM seed 方法证据 | 🟢 `final_pool_ready` | SysML 行为模型需求描述 / requirements descriptions；10 个唯一 NL × 6 个 LLM 输出 | SysML / PlantUML STM | State、Region、Pseudostate、Transition 等 SysML STM 子集；只允许初始 `Generation PlantUML` | SysML state machine / UML statechart | R5.5 复核为 mixed：8 个 T0、Microwave 为 T0.5 timer-like caveat、Digital Camera 为 T1 supplementary stress | LLM；requirements + prompt；6 个 LLM 各 10 条 | Google Drive workbook 已 committed，60 条 generated PlantUML trace verified；reference / checking 列需隔离；reference canonical case=10、exact unique reference PlantUML=11 |
| `sefm-llm-state-machine` | 强相关 LLM seed 方法证据 | 🟢 `final_pool_ready` | 非结构化 reactive-system 系统描述 / 行为需求；ZIP 共 9 个 NL descriptions | UML state machine / Umple 输出 | 显式 state / transition / guard / action；评估 hierarchy / parallel / history；SSC7 generated 输出含 `after(60)` 类 timer-like transition | UML statechart / HSM-capable | T0-结构化离散；不是 timed automata / hybrid model | LLM；当前可计 pair 为 Claude Sonnet 3.5 single prompt | 4open ZIP 已 committed，SSC7 generated pair trace verified；仅 1 组 generated pair，其余 8 个无 generated 输出的 NL 不计 generated pair（7 个 reference-only + 1 个 ATAS 纯 NL-only） |
| `fsm-bench-20` | pipeline 相关证据 | 🟠 `pipeline_only` | 控制系统需求、prompt、schema | FSM JSON schema / gold systems；作者 generated `STM_0` 缺失 | 平坦 FSM schema、可复跑 prompt/code | FSM JSON / T0 | T0-离散；未见显式时钟 | 作者 benchmark pipeline；需本项目 rerun | Zenodo/GitHub release 可用，但 no published generated `STM_0`；不计现成 seed |
| `ttool-ai-smd-subset` | 条件一手 / 转换器压力证据 | 🟡 `conditional_final_pool` | 作者 GitHub 工件中的系统规格；6 raw / 4 unique | TTool/SysML/AVATAR XML generated artifacts | 完整 TTool XML，需切出 SMD/T0 子集；可能含时间、信号、guard/action 和 incoherency correction 上下文 | SysML/TTool state-machine diagram subset / XML | T1-含时间/信号语义线索；需转换器明确处理 | TTool + ChatGPT 3.5 | 一手 GitHub artifact 已 committed 并 trace verified 6 组条件 pair；不计现成 final pool，进入实验前需切片 run record |
| `maritaca-use-case-behavior-models` | 传统 NLP / 半自动方法证据 | ⚪ `paper_reconstructable` | 半结构化 textual use case descriptions | UML state machine / behavior model | use-case step 到状态/迁移的模板化行为模型；需人工特征选择 | UML state machine / 用例行为模型 | T0-离散事件；未见显式时钟 | 半自动 NLP + template / 规则 + 人工特征选择 | 作者站点 403；无 machine-readable native pair，论文例子只可重建 |
| `automated-transition-use-cases-uml-sm` | 传统规则方法证据 | ⚪ `paper_reconstructable` | RUCM textual use case specifications | UML State Machine | RUCM flow / transition 到 state-based testing 用状态机 | UML state machine / state-based testing | T0-离散事件；未见显式时钟 | RUCM + aToucan / rule-based | 附录可重建局部 pair；无一手原生 pair 包 / 代码 / 引用说明 |
| `dependable-product-families-usecases-state-machines` | 传统规则 / product-line 方法证据 | ⚪ `paper_reconstructable` | 受限格式 use cases，含 variability、exception handling、traceability matrix | product-specific state machine / EFSM | product-line variability、exception、traceability | EFSM / product-line state machine | T0-数据/守卫级；未见显式时钟 | 半自动规则 / traceability matrix | 作者站点受阻；例子可重建，原生代码/数据/许可未公开 |
| `statechart-use-case-validation-event-driven` | validation-oriented 方法证据 | ⚪ `paper_reconstructable` | 结构化 use case 模板，含 pre/postconditions、events、main flow | 单 use-case UML Statechart 与 combined Statechart | 事件驱动，多 use-case statechart 合并 | UML Statechart / validation-oriented | T0-离散事件；未见显式时钟 | use case 文档 -> statechart -> combined statechart | 案例入口可定位，图示可重建；完整代码/数据/hash 未公开 |
| `rscharter-statechart-elements` | statechart elements / FOPL 桥接证据 | ⚪ `paper_reconstructable` | PuRE dataset 中 RUPP/EARS 风格 SRS / NL requirements | statechart diagram elements / state diagram；经 FOPL 中间层 | 元素抽取 + FOPL bridge，完整图需另行冻结 | statechart elements + FOPL bridge | T0-元素级待核 | NL SRS -> FOPL -> statechart elements | PuRE 输入公开，但 RSCharter 增强 pair/code 未公开 |
| `designing-fsm-gpt4` | LLM toy-line / NL+code 复跑线索 | 🟠 `pipeline_only` | 运行时合成的英文 DFSM / Mealy 自然语言描述；不是冻结发布 corpus | CSV DFSM / Mealy machine | 平坦、确定性、输入/输出驱动 | 平坦 FSM / Mealy | T0-平坦离散；未见显式时钟 | GPT-4 / GPT-4o 初始生成，论文含 oracle / repair；当前只承认初始生成切片 | 作者 GitHub 源码已固定并完成连通性检查；无作者发布 generated pair，复跑输出需另建 run record |

边界 / 哨兵类（如 `execution-nl-req-bt-sm`、`semi-auto-efsm-standard-docs`、`nl-standard-docs-state-machines`、`most-states-modes`、`web-tool-goal-statechart-derivation`、`requirements-analysis-prototyping-scenarios-statecharts` 等）默认按 [REGISTRY.md](./REGISTRY.md) §4 或 §10 排除码处理：它们可支撑 related work 和防误收，但不能绕过一手 registry 成为现成 generated seed。
