# seed_library/SUMMARY.md

## 1. 当前状态一句话

本 SUMMARY 是 PR-R1.8-B 迁移后的种子文库当前横向事实真源；它承接 R1.7 有界快照 v4，而不是全域普查。旧 `seed_corpus/` 的横向台账与原始检索材料已归档到 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)，当前事实以本文件和 36 个单条目目录为准。

核心口径：种子文库记录上游 `NL -> STM_0` 方法 / 来源集合，不是本论文 `STM_0 -> STM_k` 修正基线；R2 四例样本还需要后续 逐案例冻结。

## 2. 关键统计表

| 指标 | 数量 | 可复算位置 | 注意事项 |
|---|---|---|---|
| 去重候选 | 47 | §5 候选全集；[归档 candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/candidate_matrix.md) | R1.7 有界快照 v4。 |
| 筛查入账 | 47 | [归档 screening_ledger.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/screening_ledger.md)；§14 迁移表 | 与候选 ID 一一对应。 |
| 单条目证据目录 | 36 | §8 本地证据容器表；`find corpora/seed_library -mindepth 1 -maxdepth 1 -type d` | `fsm-bench-20` 是 仅制品 / 流水线备选。 |
| R1.7 检索轮次哨兵 | 8 | §11 检索覆盖摘要；[归档 search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/) | archive 另含 R1.6 与早期检索记录。 |
| 旧九生成基线映射 | 9/9 | §8.1 旧九映射；[归档 baseline_seed_method_crosswalk.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/baseline_seed_method_crosswalk.md) | 这是 seed 方法集合，不是 修正基线。 |
| R2 主 / 条件主可计候选 | 4 | §4 / §6；R2资格为 🟢 或 🟡 | 2 强主 + 2 条件主，仍需 R2 裁决。 |
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
| R2 可计候选 | 后续可作为 `<NL, STM_0> -> Better STM` 实验输入来源；必须再做 逐案例冻结、许可 / 哈希 和泄漏检查。 |

### 3.2 emoji 列口径

正式总账表中，emoji 列只放 emoji；中文释义集中放在本节和 [GUIDE.md](./GUIDE.md)。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达，❓表示待核，⚪表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 文献资格 | 强种子：清楚满足 `NL -> T0 STM-family` | 条件种子：关系清楚但有 synthetic / 制品 / T0 等 边界说明 | 扩展 / 边界证据：对方法或转换压力有价值 | 不满足或明确排除 | 待核 | 不适用 |
| T0 适配 | T0 明确 | 大体 T0，但需切片或少量格式转换 | 存在 timed / hybrid / protocol / 中间产物 风险 | 非 STM family 或不可隔离 | 待核 | 不适用 |
| 生成关系 | 明确 `NL -> STM_0` | 方向基本成立但需切片 / 初始输出隔离 | 只有间接、中间模型或 paper-level 重建线索 | 不是 `NL -> STM_0` | 待核 | 不适用 |
| R2 实验输入可用性（派生汇总） | 关键输入可直接冻结：NL 数据、STM_0 数据、作者原生 pair、可重建 pair、配对索引、许可、版本 / 哈希均可支撑实验 | 关键输入基本可用但需抽取、切片或冻结版本 | 只可论文级重建或需要大量人工整理 | 关键输入不可得，不能直接做 R2 样本 | 待核 / 访问受阻 | 对该条目不适用 |
| R2 资格 | 主候选 | 条件主候选 | 备选 / 相关工作 / 转换器压力 | 不计入当前四例 | 待核 | 不适用 |
| 泄漏风险 | 未见明显泄漏 | 需隔离 reference / repair / oracle 字段 | 泄漏风险高，必须强约束使用 | 无法隔离 | 待核 | 不适用 |

### 3.3 资源可获取性分级

本节专门解释第 7 节资产盘点里用到的资源状态。盘点对象包括论文本体、来源文档、生成/复现实验代码、NL 原始数据、STM_0 原始数据、作者原生 `<NL, STM_0>` pair、可重建 pair、配对索引、原始生成输出、评测结果 / 日志，以及许可、版本 / 哈希信息；**不是**本地 `seed_desc.md`、`artifacts.md` 是否存在。资源列只统计论文正文 / 脚注 / Data Availability / 参考文献、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手入口；本仓库已经缓存的 parquet、ZIP、代码、PDF、hash、截图或复现副本只能作为本地审计证据，不能把资源等级从 ❓/🔴 升成 🟡/🟢。整体 R2 实验输入可用性是派生汇总项，不能用单个“资源可用”emoji 代替，至少要同时检查 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`许可`、`版本 / 哈希`。

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
| 许可 | 许可明确且允许后续研究使用 | 许可存在但需确认适用范围 | 许可不明但可追踪作者或仓库 | 无法确认或明确不可用 | 待核 | 不适用 |
| 版本 / 哈希 | 发布版本、commit / 哈希或数据快照明确可追踪 | 可补冻结但当前未完全记录 | 只能以下载日期或页面状态弱冻结 | 无法冻结 | 待核 | 不适用 |

### 3.4 方法与资源枚举

| 字段 | 允许值 / 写法 | 说明 |
|---|---|---|
| 生成者 | 人工 / 规则算法 / NLP工具 / LLM / 多阶段流水线 / 混合 | 只描述 `STM_0` 产生方式；不把后续 修正循环 混入 seed。 |
| LLM参与 | 是 / 否 / 可能 / 不适用 | “可能”必须有证据不足说明。 |
| NL类型 | 需求文本 / 用例 / 场景文本 / 系统描述 / 标准文档 / 合成需求 / 来源文档 / 非NL | 用中文写，不再使用 `非结构化` 等英文短语。 |
| STM类型 | FSM / HSM / EFSM / UML statechart / SysML STM / PlantUML / Mermaid / Umple / 协议FSM / 非STM | 协议FSM、非STM默认不计控制系统四例。 |
| 资源列 | 论文 / 来源文档 / 生成代码 / NL 数据 / STM_0 数据 / 作者原生 pair / 可重建 pair / 配对索引 / 原始生成输出 / 评测结果 / 许可 / 版本 / 哈希 | 资源可获取性面向后续实验可用资源，不等同于本地 `seed_desc.md` 是否存在；必须给论文正文 / 脚注 / Data Availability / 参考文献、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手可点击入口；本地缓存只作审计证据。 |

### 3.5 R2 交接表列口径

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
| R2 | 是否可计入当前四例候选。 |

## 4. R2 交接分组

| 分组 | 候选 | 当前用途 |
|---|---|---|
| 强主种子候选 | `sefm-llm-state-machine`、`llms-emp-stm-subset` | 最优先进入 R2 四例候选池；仍需冻结制品、许可 / 哈希、输入输出切片。 |
| 条件主种子候选 | `designing-fsm-gpt4`、`unified-uml-multimodal-validation` | 可补足四例候选数；前者必须 仅初始生成，后者必须标 synthetic / 许可 边界说明。 |
| 流水线 备选 | `fsm-bench-20` | 任务关系强、MIT / Zenodo / GitHub 可用；但 生成的 `STM_0` 输出 未公开冻结，需要 R2 复跑。 |
| 仅论文的严格 / 条件证据 | `nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`pushing-generative-envelope-mbse` 等 | 相关工作、人工重建线索和严格门槛论证；不计 R2 主 seed。 |
| 扩展 / 转换压力 | `ttool-ai-smd-subset`、`fsm-gen-iec-61499` | 对 转换器、控制系统相关性和 反馈叙事 有价值，但因 timing / 私有 制品 / 中间产物 边界 不计主 seed。 |
| 协议域方法 / 排除哨兵 | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel` 及其他 protocol / sequence / completion / formal-spec 哨兵 | 保留为方法证据和防误收证据，不计控制系统四例。 |

## 5. 候选全集：基础事实与资格矩阵（47 行）

本节把旧宽表拆成多张窄表。§5 只记录元数据、输入输出、生成关系和资格；§7 另列资源可获取性；§8 只列本地证据容器完整性。更细历史原表见 [归档 candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/candidate_matrix.md)。 `证据` 列只提供来源指针或本地分析入口，不代表对应外部资源已经可获取，资源状态必须回到 §7 判读。

| ID | 年份 | 来源批次 | NL类型 | STM类型 | T0 | 关系 | 文献资格 | R2资格 | 当前角色 | 主要风险 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 2026 | 旧基线 / 复现 | 系统描述 | UML statechart | 🟢 | 🟢 | 🟢 | 🟢 | R2 强主候选 | 需冻结制品、许可 / 哈希、逐 case T0 边界 | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | 2024 | 旧基线 / 复现 | 需求文本 | SysML / PlantUML STM | 🟢 | 🟢 | 🟢 | 🟢 | R2 强主候选 | 只允许 STM 子集，ACT/SD 排除 | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | 2026 | 旧基线 | 合成需求 | DFSM / Mealy CSV | 🟢 | 🟢 | 🟡 | 🟡 | 条件主候选 | 只取初始生成，排除 oracle / repair 环节 | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | 2026 | R1.6 + HF 制品 | 合成需求 | PlantUML | 🟢 | 🟢 | 🟡 | 🟡 | 条件主候选 | 需逐行解析/渲染抽检与许可边界说明 | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |
| `fsm-bench-20` | 2026 | R1.6 + Zenodo/GitHub | 需求文本 | FSM JSON | 🟢 | 🟢 | 🟢 | 🟠 | 流水线备选 | 公开包缺作者冻结 生成的 `STM_0` 输出 | [seed_desc](./fsm-bench-20/seed_desc.md) |
| `ttool-ai-smd-subset` | 2024 | 旧基线 / 复现 | 系统规范 | SysML STM | 🟡 | 🟡 | 🟠 | 🟠 | 转换器压力 | 需切出 SMD 并处理时间 / 信号边界说明 | [seed_desc](./ttool-ai-smd-subset/seed_desc.md) |
| `fsm-gen-iec-61499` | 2025 | 旧基线 / R1.6全文 | 工业自动化需求 | FSM / IEC 61499 ECC | 🟡 | 🟡 | 🟡 | 🔴 | 私有制品边界 | 初始 STM 与 refinement 难隔离 | [seed_desc](./fsm-gen-iec-61499/seed_desc.md) |
| `ijisrt-uml-state-diagrams-llm` | 2026 | R1.6全文 | 系统描述 / prompt | UML statechart / PlantUML | 🟢 | 🟢 | 🟢 | 🔴 | 仅论文 近期证据 | 案例偏 玩具级 且无 原始输出 | [seed_desc](./ijisrt-uml-state-diagrams-llm/seed_desc.md) |
| `umple-nl-state-machine` | 2024 | 旧基线 | 需求文本 | Umple state machine | 🟢 | 🟢 | 🟢 | 🔴 | 仅论文 种子证据 | 可作手工重建线索 | [seed_desc](./umple-nl-state-machine/seed_desc.md) |
| `req-mermaid-statechart` | 2025 | 旧基线 | 汽车产品功能需求 | Mermaid statechart | 🟡 | 🟡 | 🟡 | 🔴 | 私有数据边界 | 任务贴合但不可复验 | [seed_desc](./req-mermaid-statechart/seed_desc.md) |
| `pushing-generative-envelope-mbse` | 2025 | 旧基线 / 仅论文 | MBSE题项 | SysML STM | 🟢 | 🟢 | 🟡 | 🔴 | 仅论文 prompt / temperature 参考 | — | [seed_desc](./pushing-generative-envelope-mbse/seed_desc.md) |
| `from-use-cases-to-statecharts` | 2001 | 旧基线 | 用例 | UML statechart | 🟡 | 🟡 | 🟡 | 🔴 | 经典文献 | statechart 是中间产物 | [seed_desc](./from-use-cases-to-statecharts/seed_desc.md) |
| `beyond-scenarios-state-models` | 2004 | 旧基线 | 受限英语用例 | HFSTM | 🟢 | 🟡 | 🟡 | 🔴 | 经典文献 | `paper_content` 质量差，需 PDF 核验 | [seed_desc](./beyond-scenarios-state-models/seed_desc.md) |
| `executable-state-machines-structured-text` | 2019 | 旧基线 | 结构化需求 / SPS | executable FSM | 🟢 | 🟠 | 🟡 | 🔴 | NL->SPS 有人工步骤 | 弱 seed 相关工作 | [seed_desc](./executable-state-machines-structured-text/seed_desc.md) |
| `maritaca-use-case-behavior-models` | 2017 | R1.6 经典检索 | 半结构化用例 | UML state machine | 🟢 | 🟢 | 🟢 | 🔴 | 严格种子 / 传统 NLP 基线 | 作者 artifact 403；pair/代码未冻结 | [seed_desc](./maritaca-use-case-behavior-models/seed_desc.md) |
| `dependable-product-families-usecases-state-machines` | 2016 | R1.6 经典检索 | 受限用例 + variability | UML state machine / EFSM | 🟡 | 🟢 | 🟡 | 🔴 | 条件严格种子 / 产品族哨兵 | variability 需切片；pair/code未公开 | [seed_desc](./dependable-product-families-usecases-state-machines/seed_desc.md) |
| `automated-transition-use-cases-uml-sm` | 2011 | 外部检索 | 用例 | UML state machine | 🟡 | 🟢 | 🟡 | 🔴 | 条件种子 / RUCM 方法证据 | 论文 [DOI](https://doi.org/10.1007/978-3-642-21470-7_9)；附录可重建局部 pair，原生 pair / 代码 / 许可未冻结 | [seed_desc](./automated-transition-use-cases-uml-sm/seed_desc.md) |
| `execution-nl-req-bt-sm` | 2012 | 外部检索 | 需求文本 | 行为树 -> FSM | 🟢 | 🟠 | 🟠 | 🔴 | BT 中间产物 / 转换链证据 | BT2SMExamples 链接不稳定；不计主 seed | [seed_desc](./execution-nl-req-bt-sm/seed_desc.md) |
| `completion-sysml-gwt` | 2024 | 外部 / 旧基线 | GWT需求 + partial model | SysML transitions | 🟠 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 依赖已有 partial model | [seed_desc](./completion-sysml-gwt/seed_desc.md) |
| `towards-automatic-model-completion` | 2022 | R1.7人工复查 | GWT需求 + partial SMD | SysML STM 片段 | 🔴 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 不是 initial `NL -> STM_0` | [seed_desc](./towards-automatic-model-completion/seed_desc.md) |
| `scenarios-statecharts-interrelated` | 待核 | 旧基线 | 结构化 scenario / event trace | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | 输入不是自然语言需求文本 | [seed_desc](./scenarios-statecharts-interrelated/seed_desc.md) |
| `generating-statechart-designs-from-scenarios` | 2000 | 外部检索 | sequence / scenario | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | sequence/scenario 输入 | https://doi.org/10.1145/337180.337217 |
| `synthesis-revisited-scenario-based` | 2005 | 外部 / 旧基线 | LSC / MSC 形式化场景 | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` | — | https://doi.org/10.1007/978-3-540-31847-7_18 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 2002 | 外部检索 | scenario / co-evolution | statechart | ❓ | 🔴 | 🔴 | 🔴 | 反向边界哨兵 | 仅二手 Academia PDF；方向是 statechart/scenario 协同与原型验证，不是 NL->STM | [seed_desc](./requirements-analysis-prototyping-scenarios-statecharts/seed_desc.md) |
| `nl-standard-docs-state-machines` | 2018 | 外部检索 | 标准文档 | state machine | 🟡 | 🟢 | 🟠 | 🔴 | 标准文档哨兵 | 论文 [DOI](https://doi.org/10.2514/1.I010525)；ECSS/PUS 标准为引用来源文档，原始输出包未公开 | [seed_desc](./nl-standard-docs-state-machines/seed_desc.md) |
| `semi-auto-efsm-standard-docs` | 2015 | R1.6 protocol search | 标准文档 | EFSM | 🟢 | 🟢 | 🟠 | 🔴 | 标准文档哨兵 | 论文 [DOI](https://doi.org/10.1109/DSN-W.2015.17)；ECSS/PUS 为引用标准，code/data 未公开 | [seed_desc](./semi-auto-efsm-standard-docs/seed_desc.md) |
| `statechart-use-case-validation-event-driven` | 2012 | R1.6 Crossref | use-case model | UML statechart | 🟢 | 🟢 | 🟡 | 🔴 | 条件种子 / 验证导向 | 论文 [DOI](https://doi.org/10.1145/2245276.2231947)；[RealState](http://openseminar.org/se/) 为案例入口，图示可重建 pair；原生数据包/代码未公开 | [seed_desc](./statechart-use-case-validation-event-driven/seed_desc.md) |
| `rscharter-statechart-elements` | 待核 | R1.6 Crossref | 需求规格 | UML statechart 元素 | 🟢 | 🟡 | 🟡 | 🔴 | 条件种子 / FOPL 桥接 | 论文 [SSRN](https://papers.ssrn.com/abstract=4964857)；PuRE 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.1414117)；增强 pair 未公开 | [seed_desc](./rscharter-statechart-elements/seed_desc.md) |
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

## 6. R2 交接 / 可计候选明细

| ID | NL公开 | NL唯一输入 | 前置制品 | STM格式 | 输出方言 | T0 | 生成者 | LLM | 作者原生 pair | 可重建 pair | 配对索引 | 泄漏 | 转换 | R2 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 🟡 | 🟢 | ⚪ | UML statechart | Umple / UML | 🟢 | LLM | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | 🟢 | 🟢 | 🟡 | SysML / PlantUML STM | PlantUML | 🟢 | LLM | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | 🟠 | 🟢 | ⚪ | CSV DFSM / Mealy | CSV | 🟢 | LLM | 是 | 🔴 | 🟠 | 🟠 | 🟠 | 🟡 | 🟡 | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | 🟢 | 🟡 | 🟡 | PlantUML state diagram | PlantUML | 🟢 | 多模型流水线 | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |

说明：`sefm-llm-state-machine` 的 [4open 制品](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) 可用但仍需正式冻结版本 / 许可 / 哈希；`designing-fsm-gpt4` 只按论文 [arXiv](https://arxiv.org/abs/2603.29140) 中 Listing 可重建的初始生成口径处理；`unified-uml-multimodal-validation` 必须记录论文 [Data Availability](https://www.techscience.com/CMES/v146n1/65740/html) 指向的 [HF 数据集](https://huggingface.co/nguyenvanviet/datasets) 许可边界和合成 NL 风险。

## 7. 外部资源可获取性矩阵（47 行）

本表盘点“后续环节能否直接使用”的外部资源，而不是本地 `README.md`、`seed_desc.md`、`artifacts.md` 是否存在。资源状态口径见 §3.2 和 §3.3。R2 实验输入至少要同时看 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`许可`、`版本 / 哈希`；论文本体、生成代码和评测结果主要支撑复核、复现和相关工作分析。**资源可获取性升级为 🟢/🟡 前，必须基于全文阅读与外部资源页核验**，包括 DOI / 出版页、论文明确指向的作者仓库、数据集 / artifact 页面、附录、补充材料和许可页；不能只因为本地有 `seed_desc.md`、`artifacts.md`、PDF 缓存、parquet 缓存、ZIP 缓存、代码副本或本地 hash 就判断作者公开了可复用资产。若全文或资源页受阻，应保持 ❓/🔴 并在说明列写明阻塞来源。凡说明列提到可获取的一手资源，必须给出可点击链接。

| ID | 论文本体 | 来源文档 | 生成/复现实验代码 | NL 数据 | STM_0 数据 | 作者原生 pair | 可重建 pair | 配对索引 | 原始生成输出 | 评测结果 / 日志 | 许可 | 版本 / 哈希 | 获取性说明 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 🟢 | ⚪ | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) 含 descriptions / reference / 生成输出；需冻结许可、版本和哈希。 |
| `llms-emp-stm-subset` | 🟢 | ⚪ | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文正文/脚注给出数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；生成流水线代码未公开，数据许可待核。 |
| `designing-fsm-gpt4` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | ❓ | ❓ | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；论文内 Listing 1.1/1.2 可重建初始 NL/CSV；论文未给一手代码/数据链接，论文外 GitHub 不计入资源可获取性。 |
| `unified-uml-multimodal-validation` | 🟢 | ⚪ | ❓ | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | ❓ | ❓ | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html) 的 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram)，许可、逐行可解析性与合成边界待核。 |
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
| `dependable-product-families-usecases-state-machines` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [IEEE DOI](https://doi.org/10.1109/LADC.2016.28)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但按受阻处理；只能从论文中的 use case / variability / traceability matrix 重建 pair，原生代码、数据、许可、hash 未公开。 |
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
| `statechart-use-case-validation-event-driven` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文 [ACM DOI](https://doi.org/10.1145/2245276.2231947)；论文引用案例来源 [RealState](http://openseminar.org/se/)；图示可重建 pair，完整代码/数据/许可/hash 未公开。 |
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


| 原基线 | 种子方法 ID | 矩阵 ID | 单条目 | 输入 NL | 输出 STM | 生成方法 | 作者原生 pair | 资源摘要（非原子；一手入口） | R2 用途 |
|---|---|---|---|---|---|---|---|---|---|
| Structure- and Event-Driven Frameworks | `sefm-llm-state-machine` | `sefm-llm-state-machine` | [sefm-llm-state-machine](./sefm-llm-state-machine/) | 8 个 reactive-system / system descriptions | UML state machine / statechart | LLM；单轮提示、结构驱动、事件驱动、混合策略 | 🟢 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) 含代码 / 数据 / F1 workbook；许可 / 哈希待冻结 | 强主 seed 候选 |
| LLMS EMP / SysML Behavior Models | `llms-emp-stm-subset` | `llms-emp-stm-subset` | [llms-emp-stm-subset](./llms-emp-stm-subset/) | 107 个 SysML 行为模型需求描述；只取 `diagram_type=stm` 子集 | PlantUML / SysML STM | LLM；requirements + prompt；含检查 / 反馈再生成设计 | 🟢 | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)，流水线代码未公开，许可待核 | 强主 seed / judge 校准 |
| Designing FSM with GPT-4 | `designing-fsm-gpt4` | `designing-fsm-gpt4` | [designing-fsm-gpt4](./designing-fsm-gpt4/) | 合成英文 DFSM / Mealy 需求描述 | CSV DFSM / Mealy | GPT-4/GPT-4o；初始生成 + oracle / 检查 / 修正实验 | 🔴 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；论文内 Listing 可重建初始 NL/CSV；论文未给一手代码/数据链接，论文外 GitHub 只作线索 | 条件主；仅初始生成 |
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

| 状态 | 数量 | ID | R2影响 |
|---|---|---|---|
| 已下载并复核 | 11 | `automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`semi-auto-efsm-standard-docs`、`rscharter-statechart-elements`、`nl-standard-docs-state-machines`、`requirements-analysis-prototyping-scenarios-statecharts`、`most-states-modes`、`web-tool-goal-statechart-derivation` | 已下载全文并回填到候选 / 资源表，不再阻塞 R2。 |
| 已下载后排除 | 2 | `completion-sysml-gwt`、`towards-automatic-model-completion` | 已有全文并确认为 repair-only，不阻塞 R2。 |
| 元数据已足够排除 | 2 | `generating-statechart-designs-from-scenarios`、`ucgen-usecase-descriptions` | 元数据已足够排除，不阻塞 R2。 |
| 仍受阻 | 1 | `executable-use-cases-domain-machine-specifications` | 仍需人工下载全文；不作为 R2 阻塞项。 |

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
| `bpmn-process-sentinel` | `X_PROCESS` | BPMN / workflow / resource-flow 与 STM-family 不同 | 防误收 | [exclusion_ledger](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/exclusion_ledger.md) |
| `formal-spec-sentinel` | `X_FORMAL_SPEC` | Petri / CSP / Event-B / TLA+ / LTL/STL 或 形式化 scenario | 防误收 | [exclusion_ledger](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/exclusion_ledger.md) |
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
| `r17-01-openalex-broad-nl-requirements` | OpenAlex | 宽口径 NL requirements / statechart / use-case 检索簇 | 95 | 0 | 宽检索噪声高 / 宽检索保留为排除证据 | 详见 [round-r17-01-openalex-broad-nl-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-01-openalex-broad-nl-requirements.md) |
| `r17-02-crossref-refined-usecase-statechart` | Crossref | use-case / statechart / requirements 精细检索 | 50 | 1 | 无全文/制品 / 精确 DOI/标题发现 | 详见 [round-r17-02-crossref-refined-usecase-statechart.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-02-crossref-refined-usecase-statechart.md) |
| `r17-03-crossref-textual-usecase-behavior` | Crossref | textual 用例文本 / behavior models / state machine | 30 | 0 | 输出非 STM 噪声为主；MARITACA 已由人工下载全文入库，旧轮次仅作历史发现入口 | 详见 [round-r17-03-crossref-textual-usecase-behavior.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-03-crossref-textual-usecase-behavior.md) |
| `r17-04-arxiv-llm-requirements` | arXiv | LLM + state machine / state diagram / requirements | 40 | 0 | 需求质量 / 切片 / 非 STM LLM 噪声 / 无新增 SA-1/2 种子 | 详见 [round-r17-04-arxiv-llm-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-04-arxiv-llm-requirements.md) |
| `r17-05-semanticscholar-阻塞项` | Semantic Scholar API | 6 检索簇 | 6 个错误 | 0 | HTTP 429 频率限制 / 降级到 OpenAlex/Crossref/arXiv/DBLP | 详见 [round-r17-05-semanticscholar-blocker.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-05-semanticscholar-blocker.md) |
| `r17-06-dblp-exact-title` | DBLP API | 12 精确标题人工 / 经典候选 | 429 / 连接限制前确认 3 条 | 0 | DBLP 频率/连接限制 / 仅元数据互证 | 详见 [round-r17-06-dblp-exact-title.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-06-dblp-exact-title.md) |
| `r17-07-classic-fulltext-wave` | 开放/出版商 PDF | 经典用例 / 嵌入式 / 测试生成全文波次 | 7 | 7 dirs | 均仅论文 / 两个硬边界 / 强化排除证据; 无新增 SA-1/2 | 详见 [round-r17-07-classic-fulltext-wave.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-07-classic-fulltext-wave.md) |
| `r17-08-manual-queue-artifact-recheck` | 出版商精确检索 + 制品检索 | R1.6 人工队列 + R1.7 新增人工候选 | 13 | 1 个新增下载目录 | 付费墙 / 需浏览器访问的开放入口 / 无制品 / 人工队列状态分布已更新 | 详见 [round-r17-08-manual-queue-artifact-recheck.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-08-manual-queue-artifact-recheck.md) |

归档入口：

- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/)

## 12. 文献筛查与全文阅读 provenance 摘要

旧 `agent_provenance.md` 已归档为 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md)。其记录范围仅限文献筛查、全文阅读、证据等级调整和研究性 阻塞项；不记录 PR review / ready / merge 进度。R1.7 最终整合输出为：47 候选 / 47 筛查 / 36 单条目目录；主 / 条件主可计候选仍为 4；Semantic Scholar API 429 已记录并由 OpenAlex/Crossref/arXiv/DBLP exact-title 替代。

## 13. 关键风险与 R2 建议

1. **四例候选仍紧绷**：当前 R2 🟢 / 🟡 只有 4 条，且其中 2 条为条件候选。
2. **`fsm-bench-20` 不能直接算 生成种子**：公开包有 dataset / prompt / schema / code / MIT，但缺作者冻结 生成的 `STM_0` 输出；若使用必须 R2 复跑并保存 清单 / 哈希。
3. **仅论文 / 私有 / protocol 方法不能替代可运行样本**：它们必须进入 seed 方法集合，但不能冒充可复验实验输入。
4. **封闭 / 人工 项可能改变 相关工作 叙述，不应改变当前 硬门槛**。
5. **本快照 非全域 普查**：只能作为 有界快照 + 排除证据 + 备选 交接。

R2 最小动作：先冻结 `sefm-llm-state-machine` 与 `llms-emp-stm-subset`，再裁决 `designing-fsm-gpt4` 与 `unified-uml-multimodal-validation`；若条件候选失败，启动 `fsm-bench-20` 复跑或 本项目构造 seed 备选。

## 14. 迁移表

| 旧路径 / 对象 | 新路径 / 新章节 | 当前事实真源 | 迁移理由 |
|---|---|---|---|
| `seed_corpus/README.md` | `seed_corpus/README.md redirect + corpora/seed_library/README.md` | corpora/seed_library/README.md | 旧入口降级为跳转，避免第二事实源。 |
| `seed_corpus/GUIDE.md` | `archive/.../legacy_ledgers/seed_corpus_GUIDE.md + corpora/seed_library/GUIDE.md` | corpora/seed_library/GUIDE.md | 旧规则归档，新规则按 SUMMARY-first 重写。 |
| `seed_corpus/SUMMARY.md` | `archive/.../legacy_ledgers/seed_corpus_SUMMARY.md + corpora/seed_library/SUMMARY.md` | corpora/seed_library/SUMMARY.md | 旧总账归档，新总账承载所有横向事实。 |
| `candidate_matrix.md` | `archive/.../legacy_ledgers/candidate_matrix.md；摘要进入 SUMMARY §5` | corpora/seed_library/SUMMARY.md | 47 条候选进入单一横向总账。 |
| `screening_ledger.md` | `archive/.../legacy_ledgers/screening_ledger.md；47/47 进入 SUMMARY §2/§5/§14` | corpora/seed_library/SUMMARY.md | 候选 / 筛查 对齐哨兵可复算。 |
| `exclusion_ledger.md` | `archive/.../legacy_ledgers/exclusion_ledger.md；摘要进入 SUMMARY §10` | corpora/seed_library/SUMMARY.md | 排除证据 直接可见。 |
| `manual_download_queue.md` | `archive/.../legacy_ledgers/manual_download_queue.md；摘要进入 SUMMARY §9` | corpora/seed_library/SUMMARY.md | manual 阻塞项 直接可见。 |
| `baseline_seed_method_crosswalk.md` | `archive/.../legacy_ledgers/baseline_seed_method_crosswalk.md；9/9 表进入 SUMMARY §8` | corpora/seed_library/SUMMARY.md | 旧九生成基线进入 seed 方法集合，不误作 修正基线。 |
| `seed_selection_candidates.md` | `archive/.../legacy_ledgers/seed_selection_candidates.md；R2 交接进入 SUMMARY §4/§6` | corpora/seed_library/SUMMARY.md | R2=4 交接可直接读取。 |
| `search_log.md / search_rounds/ / search_results/` | `archive/.../legacy_ledgers/search_log.md`、`archive/.../search_rounds/`、`archive/.../search_results/`；摘要进入 SUMMARY §11 | corpora/seed_library/SUMMARY.md | 原始检索归档，搜索覆盖摘要当前可读。 |
| `agent_provenance.md` | `archive/.../legacy_ledgers/agent_provenance.md；研究性审计摘要进入 SUMMARY §12` | corpora/seed_library/SUMMARY.md | 保留文献筛查 provenance，但不记录 PR 流程状态。 |
| `seed_corpus/papers/<slug>/` | `corpora/seed_library/<slug>/；本地证据容器表进入 SUMMARY §8` | corpora/seed_library/<slug>/ + SUMMARY §8 | 36 个单篇 / 制品证据容器迁入当前 seed library。 |

## 15. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-15 14:23:39 | PR-R1.8-B：补强 §16 结论总表，显式列出 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系与时间特性等级；将资源列改为一手可点击链接，并统一 `作者原生 pair` 与 `可重建 pair` 口径，避免本地缓存或论文级重建线索冒充公开原生资源。 |
| 2026-06-14 23:40:00 | PR-R1.8-B：从 vpn-lab 全书 PDF 中抽取 Yue 2011 章节，`automated-transition-use-cases-uml-sm` 从 BibTeX-only 升级为 conditional seed；人工队列更新为 `11/2/2/1`，剩余队列只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | PR-R1.8-B：接入 vpn-lab 人工下载 PDF/BibTeX，新增 12 个 evidence 目录，移除 SUMMARY 长 BibTeX 块并改链到 `manual_download_queue.bib`，补充 seed / 资源可用性结论总表。 |
| 2026-06-14 20:45:00 | PR-R1.8-B：补充人工下载 BibTeX 队列，明确资源可获取性必须基于全文阅读与外部资源页核验，不能只看本地 repo 资源。 |
| 2026-06-14 20:35:00 | PR-R1.8-B：修复 review 指出的 pair 口径同步问题，补入可重建 pair、作者原生 pair、配对索引与 R2 交接列，并把 R2 实验输入可用性标为派生汇总项。 |
| 2026-06-14 20:10:00 | PR-R1.8-B：按 review I 级意见继续拆分资源矩阵，新增来源文档、STM_0 数据、配对索引、原始生成输出、评测结果 / 日志、许可、版本 / 哈希等列，并说明 R2 实验输入可用性不能由单个资源 emoji 代替。 |
| 2026-06-14 19:30:00 | PR-R1.8-B：继续中文化 SUMMARY，新增资源可获取性分级说明，细化候选矩阵中的当前角色与主要风险，并把资源盘点范围明确到论文本体、源码、NL 数据、STM 数据、作者原生 pair、实验结果和许可 / 版本 / 哈希。 |
| 2026-06-14 18:45:00 | PR-R1.8-B：按最新审阅意见中文化 SUMMARY，拆分耦合列，新增 emoji 枚举口径与外部资源可获取性矩阵；明确本地证据容器表不等同于资源可用性。 |
| 2026-06-14 17:55:00 | PR-R1.8-B：迁移旧 `seed_corpus/` 到 `corpora/seed_library/`；建立三件套；旧横向 ledger、检索轮次 / results 进入 archive；当前 SUMMARY 可复算 `47/47`、`36 dirs`、`9/9 映射`、R2=4 和 人工队列状态。 |
| 2026-06-14 13:20:00 | PR-R1.7 有界快照 v4：纠正 seed 方法集合 vs R2 四例计数口径，补齐旧九 旧基线直接映射，新增 `pushing-generative-envelope-mbse`，扩展到 47 候选 / 47 筛查 / 24 单条目目录；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 12:10:00 | PR-R1.7 有界快照 v3：扩展到 46 候选 / 46 筛查 / 23 单条目目录 / 8 R1.7 检索轮次；新增 经典全文波次、人工队列状态分布和 排除证据；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 03:55:00 | PR-R1.6 有界快照 v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF 制品核验、search_rounds 与 PR-R2 交接。 |
| 2026-06-14 02:22:00 | 补齐 `req-mermaid-statechart` 单篇目录与 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 阻塞项交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |


## 16. seed / 资源可用性结论总表

本表给后续快速判断用的最终结论速览；细表仍以 §5 / §7 / §9 为准，R2 四例仍仅以 §6 为准。

**列口径**：

- `NL输入是什么` 要说明自然语言材料的实际形态，例如非结构化需求、系统描述、use case、SRS、标准文档、goal model 或 scenario，而不是只写“是”。
- `STM输出是什么` 要说明输出制品的具体形态，例如 UML state machine、SysML / PlantUML STM、DFSM/Mealy CSV、EFSM、statechart elements、MoSt/NuSMV 等。
- `STM关键特性` 用于说明状态机是否含层次、区域、伪状态、guard、action、变量、exception、variability、组合/合并、输入输出等对后续转换和修正有影响的特征。
- `STM谱系` 用于说明该输出落在 FSM/HSM/EFSM/statechart 哪个谱系，或为什么只是中间 / 边界 / 非目标形式化模型。
- `时间特性等级` 只按当前全文 / 制品证据判断：`未见显式时钟` 表示未发现 timed automata clock、连续时间或 hybrid dynamics；`数据/守卫级` 表示存在变量、guard、exception 或 EFSM 数据状态，但未冻结时钟语义；`待核` 表示缺全文或输出制品不足。

### 16.1 可作为 seed 的文献

| ID | 最终结论 | NL输入是什么 | STM输出是什么 | STM关键特性 | STM谱系 | 时间特性等级 | NL->STM 方式 | 关键资源获取方式 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 严格种子 | 非结构化 reactive-system 系统描述 / 行为需求 | UML state machine | 显式 state / transition / guard / action；评估 hierarchy / parallel / history | UML statechart / HSM-capable | T0-结构化离散；未见显式时钟 / 连续动力学 | LLM；单轮提示、结构驱动、事件驱动、混合策略 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip)；许可 / 哈希待冻结 | 当前最强主 seed |
| `llms-emp-stm-subset` | 严格种子 | SysML 行为模型需求描述 / requirements descriptions；只取 STM 子集 | SysML / PlantUML STM | State、Region、Pseudostate、Transition 等 SysML STM 子集；仅冻结初始/指定输出 | SysML state machine / UML statechart | T0-结构化离散；未见 timed / hybrid 目标模型 | LLM；requirements + prompt；R2 只冻结初始/指定 `STM_0` | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出的数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；流水线代码未公开，许可待核 | 当前最强主 seed；隔离作者反馈阶段 |
| `designing-fsm-gpt4` | 条件种子 | 模板合成的英文 DFSM / Mealy 自然语言描述 | CSV DFSM / Mealy machine | 字段为 State、Input、Output、Next_State；确定性、平坦、输入/输出驱动 | 平坦 FSM / Mealy | T0-平坦离散；未见显式时钟 / 时间变量 | GPT-4 / GPT-4o 初始生成 + oracle / 检查 / 修正；R2 只取初始生成 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；论文内 Listing 1.1/1.2 可重建初始 NL/CSV；论文未给一手代码/数据链接，论文外 GitHub 只作线索不计入资源列 | 只取初始生成 |
| `unified-uml-multimodal-validation` | 条件种子 | LLaMA 生成的 synthetic user-focused requirements / feature descriptions | PlantUML StateDiagram / `UMLCode_StateDiagram` | PlantUML 状态图文本；需抽检非状态图污染和合成数据泄漏 | UML state diagram / PlantUML statechart | T0-离散；未见显式时钟，需抽检非状态图污染 | 多模型流水线：requirements -> PlantUML | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html)；论文 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram) | 条件主候选 |
| `maritaca-use-case-behavior-models` | 严格种子 | 半结构化 textual use case descriptions | UML state machine / behavior model | use-case step 到状态/迁移的模板化行为模型；需人工特征选择 | UML state machine / 用例行为模型 | T0-离散事件；未见显式时钟 | 半自动 NLP + template / 规则 + 人工特征选择 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2017.33)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但当前按 403/受阻处理；论文例子可重建 | 传统 NLP seed |
| `automated-transition-use-cases-uml-sm` | 条件种子 / 方法证据 | RUCM textual use case specifications，受限自然语言 use case | UML State Machine | 从 RUCM flow / transition 信息生成 state-based testing 用状态机；Appendix A/B 可重建局部 pair | UML state machine / state-based testing | T0-离散事件；未见显式时钟 | RUCM + aToucan / rule-based | 论文 [Springer DOI](https://doi.org/10.1007/978-3-642-21470-7_9)；Appendix A/B 可重建局部 pair；未见论文一手原生 pair 包、完整代码、许可或 hash | 不计当前四例；后续冻结或可审计重建后再裁决 |
| `dependable-product-families-usecases-state-machines` | 条件种子 | 受限格式 use cases，含 variability、exception handling、traceability matrix | product-specific state machine / EFSM | 处理 product-line variability、exception 和 traceability；需切片为具体产品 seed | EFSM / product-line state machine | T0-数据/守卫级；variability 需切片，未见显式时钟 | 半自动，含 variability / traceability matrix | 论文 [IEEE DOI](https://doi.org/10.1109/LADC.2016.28)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但按受阻处理；论文例子可重建，原生代码/数据/许可未公开 | product-family 边界 |
| `statechart-use-case-validation-event-driven` | 条件种子 | 结构化 use case 模板，含 pre/postconditions、events、main flow | 单 use-case UML Statechart 与 combined Statechart | 事件驱动；支持将多个 use-case statechart 合并用于 validation | UML Statechart / validation-oriented | T0-离散事件；未见显式时钟 | use case 文档 -> statechart -> combined statechart | 论文 [ACM DOI](https://doi.org/10.1145/2245276.2231947)；案例来源 [RealState](http://openseminar.org/se/)；论文图示可重建，完整代码/数据/许可/hash 未公开 | validation-oriented |
| `rscharter-statechart-elements` | 条件种子 / 方法证据 | PuRE dataset 中 RUPP/EARS 风格 SRS / NL requirements | statechart diagram elements / state diagram；经 FOPL 中间层 | 主要抽取状态图元素并经 FOPL 桥接；完整图与 pair 需另行冻结 | statechart elements + FOPL bridge | T0-元素级待核；未冻结完整状态图时间语义 | NL SRS -> FOPL -> statechart elements | 论文 [SSRN](https://papers.ssrn.com/abstract=4964857)；输入来源 PuRE 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.1414117)；RSCharter 增强 pair/code 未公开 | FOPL bridge；不计当前四例 |

### 16.2 边界 / 相关工作 / 仅元数据

| ID | 最终结论 | NL输入是什么 | STM输出是什么 | STM关键特性 | 边界原因 | STM谱系 | 时间特性等级 | 关系 | 关键资源获取方式 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| `execution-nl-req-bt-sm` | 边界 / 相关工作 | 自然语言系统需求；安全报警系统案例列出 7 条需求 | Behavior Tree 中间产物再转换为 UML state machine | BT 是必要中间层；UML SM 输出可切 | 非直接 NL-only，且 BT 中间层必须先冻结 | BT -> UML state machine | T0-离散事件；BT 中间层未冻结时钟语义 | NL -> BT -> UML SM | 论文 [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0164121212001690) / [DOI](https://doi.org/10.1016/j.jss.2012.06.013)；论文示例可重建，BT2SMExamples 入口不稳定 | 中间产物边界 |
| `semi-auto-efsm-standard-docs` | 边界哨兵 | 自然语言 standard documents；ECSS/PUS space standard | EFSM，可供 SMC / Graphviz / DiVinE 等工具 | 变量与 transition extraction，含人工数据库步骤 | 标准/协议服务边界，非控制系统 seed 优先级 | EFSM / 标准文档 | T0-数据/守卫级；标准/协议时间语义未冻结 | standard doc -> EFSM | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2015.17)；PUS 输入来源为 [ECSS-E-ST-70-41C 官方标准页](https://ecss.nl/standard/ecss-e-st-70-41c-space-engineering-telemetry-and-telecommand-packet-utilization-15-april-2016/) / [官方 PDF](https://ecss.nl/wp-content/uploads/2016/06/ECSS-E-ST-70-41C15April2016.pdf)；TXT2SMM/case data/generated EFSM package 未公开 | 标准/协议边界 |
| `nl-standard-docs-state-machines` | 边界哨兵 | ECSS Packet Utilization Standard 需求文本 | 半自动生成 EFSM，并与人工 FSM 比较 | 标准条款到 EFSM/FSM，含人工比较 | 标准服务 / 协议式行为，代码/原生输出未公开 | EFSM / FSM | T0-数据/守卫级；标准/协议时间语义未冻结 | standard doc -> state machine | 论文 [AIAA DOI](https://doi.org/10.2514/1.I010525)；ECSS/PUS 输入来源为 [ECSS-E-ST-70-41C 官方标准页](https://ecss.nl/standard/ecss-e-st-70-41c-space-engineering-telemetry-and-telecommand-packet-utilization-15-april-2016/) / [官方 PDF](https://ecss.nl/wp-content/uploads/2016/06/ECSS-E-ST-70-41C15April2016.pdf)；原始输出包未公开 | 标准/协议边界 |
| `most-states-modes` | 相关工作 / 形式化 | 自然语言需求经 MoSt DSL 重写 / 建模；案例含车状态、洗衣机手册等 | MoSt model / NuSMV model，不是目标 STM family | 强形式化 transition relation，可启发 check | 非 FSM/HSM/EFSM/statechart seed，不能直接当 `STM_0` | MoSt DSL / NuSMV formal model | 非目标形式化模型；NuSMV transition relation 不能直接等同目标 `STM_0` | NL requirements -> MoSt DSL -> NuSMV | 论文 [ACM DOI](https://doi.org/10.1145/3640822)；论文给出工具 [GitHub](https://github.com/liuyinling/MoSt-Modeling-Tool.git) 和 examples；这些不是目标 T0 `STM_0` | 不计主 seed |
| `web-tool-goal-statechart-derivation` | 边界哨兵 | goal model / requirements view / flow expressions，不是 NL-only | atomic-state statecharts | 生成 atomic-state statecharts | 输入是 goal model / flow expressions，不是自然语言唯一输入 | goal-model-derived statechart | T0-平坦离散；未见显式时钟 | goal model -> statechart | 论文 [IEEE DOI](https://doi.org/10.1109/RE.2015.7320444)；论文给出 [supplement](http://www.cin.ufpe.br/~ler/supplement/re2015/)；非 NL-only | 不作为 seed |
| `requirements-analysis-prototyping-scenarios-statecharts` | 反向边界 | scenarios / action descriptions；不是直接自然语言需求文档唯一输入 | statecharts / state machines，同时生成 scenarios / prototype | statechart 与 scenario/prototype 协同 | 方向和 seed 定义不一致 | statechart / scenario co-evolution；方向相反 | T0-离散；时间语义未冻结 | statechart -> scenarios / prototype | 仅定位到二手 [Academia PDF](https://www.academia.edu/download/31191491/1.pdf)，正式 DOI / 作者页 / 出版页未定位；非 `NL -> STM_0` | 防误收证据 |
| `executable-use-cases-domain-machine-specifications` | 仅元数据 | application domain requirements / executable use cases，待全文确认 | machine specifications，是否为 FSM/HSM/EFSM/statechart 待核 | 缺全文，不能判断是否含状态/迁移、层次、guard 或时间语义 | 出版商封闭，全文仍受阻 | 待核 | 待核 | 待核 | 仅 [DOI](https://doi.org/10.1049/ic:20040231) / BibTeX；出版商封闭，PDF / 全文仍待人工下载 | 人工队列 |
