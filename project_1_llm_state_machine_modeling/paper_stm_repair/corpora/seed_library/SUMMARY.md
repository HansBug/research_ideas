# seed_library/SUMMARY.md

## 1. 当前状态一句话

本 SUMMARY 是 PR-R1.8-B 迁移后的种子文库当前横向事实真源；它承接 R1.7 有界快照 v4，而不是全域普查。旧 `seed_corpus/` 的横向台账与原始检索材料已归档到 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)，当前事实以本文件和 24 个单条目目录为准。

核心口径：种子文库记录上游 `NL -> STM_0` 方法 / 来源集合，不是本论文 `STM_0 -> STM_k` 修正基线；R2 四例样本还需要后续 逐案例冻结。

## 2. 关键统计表

| 指标 | 数量 | 可复算位置 | 注意事项 |
|---|---:|---|---|
| 去重候选 | 47 | §5 候选全集；[归档 candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/candidate_matrix.md) | R1.7 有界快照 v4。 |
| 筛查入账 | 47 | [归档 screening_ledger.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/screening_ledger.md)；§14 迁移表 | 与候选 ID 一一对应。 |
| 单条目证据目录 | 24 | §8 本地证据容器表；`find corpora/seed_library -mindepth 1 -maxdepth 1 -type d` | `fsm-bench-20` 是 仅制品 / 流水线备选。 |
| R1.7 检索轮次哨兵 | 8 | §11 检索覆盖摘要；[归档 search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/) | archive 另含 R1.6 与早期检索记录。 |
| 旧九生成基线映射 | 9/9 | §8.1 旧九映射；[归档 baseline_seed_method_crosswalk.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/baseline_seed_method_crosswalk.md) | 这是 seed 方法集合，不是 修正基线。 |
| R2 主 / 条件主可计候选 | 4 | §4 / §6；R2资格为 🟢 或 🟡 | 2 强主 + 2 条件主，仍需 R2 裁决。 |
| 人工下载队列状态 | 2 / 2 / 10 / 2 | §9 人工队列 | 已下载后排除 / 元数据排除 / 仍受阻 / 新增待人工。 |

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

本节专门解释第 7 节资产盘点里用到的资源状态。盘点对象包括论文本体、来源文档、生成/复现实验代码、NL 原始数据、STM_0 原始数据、作者原生 `<NL, STM_0>` pair、可重建 pair、配对索引、原始生成输出、评测结果 / 日志，以及许可、版本 / 哈希信息；**不是**本地 `seed_desc.md`、`artifacts.md` 是否存在。整体 R2 实验输入可用性是派生汇总项，不能用单个“资源可用”emoji 代替，至少要同时检查 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`许可`、`版本 / 哈希`。

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
| 资源列 | 论文 / 来源文档 / 生成代码 / NL 数据 / STM_0 数据 / 作者原生 pair / 可重建 pair / 配对索引 / 原始生成输出 / 评测结果 / 许可 / 版本 / 哈希 | 资源可获取性面向后续实验可用资源，不等同于本地 `seed_desc.md` 是否存在。 |

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
|---|---:|---|---|---|---|---|---|---|---|---|---|
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
| `maritaca-use-case-behavior-models` | 2017 | R1.6 经典检索 | 半结构化用例 | UML statechart? | ❓ | 🟡 | ❓ | 🔴 | 人工队列 | 需 IEEE 全文和 制品核验 | https://doi.org/10.1109/DSN-W.2017.33 |
| `dependable-product-families-usecases-state-machines` | 2016 | R1.6 经典检索 | 受限用例 + variability | UML statechart? | ❓ | 🟡 | ❓ | 🔴 | 人工队列 | product-family variability 待核 | https://doi.org/10.1109/LADC.2016.28 |
| `automated-transition-use-cases-uml-sm` | 2011 | 外部检索 | 用例 | UML state machine | 🟢 | 🟡 | ❓ | 🔴 | 人工队列 | 需全文确认输出与用例格式 | https://doi.org/10.1007/978-3-642-21470-7_9 |
| `execution-nl-req-bt-sm` | 2012 | 外部检索 | 需求文本 | 行为树 -> FSM | 🟠 | 🟠 | 🟠 | 🔴 | BT 中间产物 边界 | JSS PDF 受限 | https://doi.org/10.1016/j.jss.2012.06.013 |
| `completion-sysml-gwt` | 2024 | 外部 / 旧基线 | GWT需求 + partial model | SysML transitions | 🟠 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 依赖已有 partial model | [seed_desc](./completion-sysml-gwt/seed_desc.md) |
| `towards-automatic-model-completion` | 2022 | R1.7人工复查 | GWT需求 + partial SMD | SysML STM 片段 | 🔴 | 🔴 | 🔴 | 🔴 | `X_REPAIR_ONLY` | 不是 initial `NL -> STM_0` | [seed_desc](./towards-automatic-model-completion/seed_desc.md) |
| `scenarios-statecharts-interrelated` | 待核 | 旧基线 | 结构化 scenario / event trace | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | 输入不是自然语言需求文本 | [seed_desc](./scenarios-statecharts-interrelated/seed_desc.md) |
| `generating-statechart-designs-from-scenarios` | 2000 | 外部检索 | sequence / scenario | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_SEQUENCE_CLASS` | sequence/scenario 输入 | https://doi.org/10.1145/337180.337217 |
| `synthesis-revisited-scenario-based` | 2005 | 外部 / 旧基线 | LSC / MSC 形式化场景 | statechart | 🟢 | 🔴 | 🔴 | 🔴 | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` | — | https://doi.org/10.1007/978-3-540-31847-7_18 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 待核 | 外部检索 | scenario / co-evolution | statechart | ❓ | 🔴 | 🔴 | 🔴 | 方向疑似 statechart -> scenario，不是 `NL -> STM` | — | 外部检索线索; Wayback PDF line |
| `nl-standard-docs-state-machines` | 2018 | 外部检索 | 标准文档 | state machine | 🟠 | ❓ | ❓ | 🔴 | 标准 / 协议哨兵 | 需全文确认 | https://doi.org/10.2514/1.I010525 |
| `semi-auto-efsm-standard-docs` | 2015 | R1.6 protocol search | 标准文档 | EFSM | 🟠 | ❓ | ❓ | 🔴 | 标准 / 协议哨兵 | 控制标准例外待核 | https://doi.org/10.1109/DSN-W.2015.17 |
| `statechart-use-case-validation-event-driven` | 2012 | R1.6 Crossref | use-case model | UML statechart? | ❓ | ❓ | ❓ | 🔴 | 验证 vs 生成 边界 | — | https://doi.org/10.1145/2245276.2231947 |
| `rscharter-statechart-elements` | 待核 | R1.6 Crossref | 需求规格 | UML statechart 元素 | ❓ | ❓ | ❓ | 🔴 | SSRN CLI 403 | 需人工浏览器下载 | https://doi.org/10.2139/ssrn.4964857 |
| `most-states-modes` | 2024 | 外部检索 | 需求文本 | 状态/模式形式化模型 | 🟠 | ❓ | 🟠 | 🔴 | 相关工作 | 需查是否输出 STM family | 外部检索规划 |
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
| `executable-use-cases-domain-machine-specifications` | 2004 | R1.7 manual 候选 | executable use cases | machine specifications | ❓ | ❓ | ❓ | 🔴 | 新 manual 候选 | 需确认是否 STM family | https://doi.org/10.1049/ic:20040231 |
| `web-tool-goal-statechart-derivation` | 2015 | R1.7 manual 候选 | 目标模型 / 需求模型 | statechart | ❓ | 🟠 | ❓ | 🔴 | 目标模型 边界 | 不一定是 NL 输入 | https://doi.org/10.1109/RE.2015.7320444 |
| `ucgen-usecase-descriptions` | 2026 | R1.7 排除 | 需求规格 | 用例文本 | ⚪ | 🔴 | 🔴 | 🔴 | 输出非 STM | 不进入 seed | Crossref textual usecase round |

## 6. R2 交接 / 可计候选明细

| ID | NL公开 | NL唯一输入 | 前置制品 | STM格式 | 输出方言 | T0 | 生成者 | LLM | 作者原生 pair | 可重建 pair | 配对索引 | 泄漏 | 转换 | R2 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 🟡 | 🟢 | ⚪ | UML statechart | Umple / UML | 🟢 | LLM | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | 🟢 | 🟢 | 🟡 | SysML / PlantUML STM | PlantUML | 🟢 | LLM | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | 🟡 | 🟢 | ⚪ | CSV DFSM / Mealy | CSV | 🟢 | LLM | 是 | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | 🟡 | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | 🟢 | 🟡 | 🟡 | PlantUML state diagram | PlantUML | 🟢 | 多模型流水线 | 是 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |

说明：`sefm-llm-state-machine` 的 4open 制品 可用但仍需正式冻结版本 / 许可 / 哈希；`designing-fsm-gpt4` 必须只取初始生成输出；`unified-uml-multimodal-validation` 必须记录合成 NL 和 HF 许可边界说明。

## 7. 外部资源可获取性矩阵（47 行）

本表盘点“后续环节能否直接使用”的外部资源，而不是本地 `README.md`、`seed_desc.md`、`artifacts.md` 是否存在。资源状态口径见 §3.2 和 §3.3。R2 实验输入至少要同时看 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`许可`、`版本 / 哈希`；论文本体、生成代码和评测结果主要支撑复核、复现和相关工作分析。**资源可获取性升级为 🟢/🟡 前，必须基于全文阅读与外部资源页核验**，包括 DOI / 出版页、作者仓库、数据集 / artifact 页面、附录、补充材料和许可页；不能只因为本地有 `seed_desc.md`、`artifacts.md` 或 PDF 缓存就判断作者公开了可复用资产。若全文或资源页受阻，应保持 ❓/🔴 并在说明列写明阻塞来源。

| ID | 论文本体 | 来源文档 | 生成/复现实验代码 | NL 数据 | STM_0 数据 | 作者原生 pair | 可重建 pair | 配对索引 | 原始生成输出 | 评测结果 / 日志 | 许可 | 版本 / 哈希 | 获取性说明 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 🟢 | ⚪ | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 4open 制品含 descriptions / reference / 生成输出；需冻结许可、版本和哈希。 |
| `llms-emp-stm-subset` | 🟢 | ⚪ | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 本地 parquet / result 强；生成流水线代码未公开，Drive / 许可待核。 |
| `designing-fsm-gpt4` | 🟢 | ⚪ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ❓ | ❓ | GitHub 有样例、部分输出与评分；无正式发布版本 / 许可，需隔离初始输出。 |
| `unified-uml-multimodal-validation` | 🟢 | ⚪ | ❓ | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | ❓ | ❓ | HF parquet 可用；需确认许可、逐行可解析性与合成数据边界。 |
| `fsm-bench-20` | ⚪ | ⚪ | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | ⚪ | 🟢 | 🟢 | Zenodo/GitHub/MIT 可用；作者冻结的生成 `STM_0` 输出未公开。 |
| `ttool-ai-smd-subset` | 🟢 | ⚪ | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | ❓ | 🟡 | 仓库有 specification / XML / results.ods；SMD 需从联合 SysML 模型中切片。 |
| `fsm-gen-iec-61499` | 🟢 | ⚪ | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 核心实验数据 / 输出私有；只能作相关工作 / 私有边界。 |
| `ijisrt-uml-state-diagrams-llm` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内示例可读，无原始输出、代码或数据包。 |
| `umple-nl-state-machine` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | thesis 给需求和示例，完整 benchmark、输出包、评测脚本未公开。 |
| `req-mermaid-statechart` | 🟢 | ⚪ | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | Volvo / Car Weaver 核心 NL、人工 statecharts、评分与输出私有。 |
| `pushing-generative-envelope-mbse` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内题项 / 表格可读，无逐次输出包、代码、数据包或补充材料。 |
| `from-use-cases-to-statecharts` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 仅论文示例 / 手工推导线索。 |
| `beyond-scenarios-state-models` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文示例可读；本地 text 提取质量差，需 PDF 核验。 |
| `executable-state-machines-structured-text` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 仅论文示例；无可直接复验数据包。 |
| `maritaca-use-case-behavior-models` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | IEEE 访问受限，制品未发现。 |
| `dependable-product-families-usecases-state-machines` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | IEEE 访问受限，制品未发现。 |
| `automated-transition-use-cases-uml-sm` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | Springer 受限；需人工全文确认。 |
| `execution-nl-req-bt-sm` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ScienceDirect 受限；行为树中间产物边界。 |
| `completion-sysml-gwt` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文可读但为 partial-model completion，不是 seed pair。 |
| `towards-automatic-model-completion` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 论文可读但为 repair-only / completion-only。 |
| `scenarios-statecharts-interrelated` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 结构化 scenario / event trace，不是 NL seed pair。 |
| `generating-statechart-designs-from-scenarios` | 🟠 | ⚪ | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | sequence/scenario 输入；不作为 seed pair。 |
| `synthesis-revisited-scenario-based` | 🟠 | ⚪ | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 形式化 scenario 输入；不作为 seed pair。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | ❓ | ⚪ | 🔴 | ❓ | ❓ | 🔴 | 🔴 | 🔴 | ❓ | ❓ | ❓ | ❓ | 正式 PDF 未定位，方向疑似反。 |
| `nl-standard-docs-state-machines` | ❓ | 🟡 | 🔴 | 🟡 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 标准文档可能公开，但 AIAA 全文 / 输出受阻。 |
| `semi-auto-efsm-standard-docs` | ❓ | 🟡 | 🔴 | 🟡 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 标准文档可能公开；IEEE 全文 / 制品受阻。 |
| `statechart-use-case-validation-event-driven` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ACM 受限；生成 vs 验证边界待核。 |
| `rscharter-statechart-elements` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | SSRN CLI 403，需人工浏览器下载。 |
| `most-states-modes` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ACM/HAL CLI 受阻；是否 STM-family 待核。 |
| `sysmlv2-formalized-requirements` | 🟠 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 目前更像形式化 / LTL 相关证据。 |
| `protocol-flowfsm-sentinel` | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | RFC 输入公开；作者 规则书 / 标注答案 / 抽取迁移 未公开。 |
| `3gpp-protocol-sentinel` | 🟢 | 🟡 | 🔴 | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 3GPP 文档需锁版本；SpecGPT 代码 / 标注答案 / 输出未公开。 |
| `source-autonomous-driving-hsm` | ⚪ | 🟡 | ⚪ | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源文档 / HSM 可作本项目构造 seed，但无作者原生生成 pair。 |
| `source-rotorcraft-uas-hsm` | ⚪ | 🟡 | ⚪ | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源文档 / HSM 可作本项目构造 seed；需后续构造并冻结。 |
| `source-smarthand-hsm` | ⚪ | 🟡 | ⚪ | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源文档 / HSM 可作本项目构造 seed；目录名与证据待核。 |
| `source-hfsm-human-robot` | ⚪ | 🟡 | ⚪ | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源文档 / HSM 可作本项目构造 seed；需构造 STM0。 |
| `source-avp-hsm` | ⚪ | 🟡 | ⚪ | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | ⚪ | ⚪ | ❓ | ❓ | 来源文档 / HSM 可作本项目构造 seed；需防停车场景趋同。 |
| `nlp-req-formalization-testcase-generation` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内例子可重建，IRDL/sequence 中间产物与无机读输出限制使用。 |
| `statistical-usage-testing-uml` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内 textual/tabular use case 与 statechart 示例可重建。 |
| `unified-use-case-statecharts` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内 SRS use case / UCUM 示例可重建。 |
| `statechart-codesign-usecases` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内示例可重建；sequence 路径边界。 |
| `object-models-uml-embedded` | 🟢 | ⚪ | 🔴 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 论文内 textual use case / statechart 示例可重建。 |
| `integrating-graphical-nl-specifications` | 🟢 | ⚪ | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | NL 与 graphical notation 共现，不是 `NL -> STM` 输出资源。 |
| `specification-based-verification-usecase-sm` | 🟢 | ⚪ | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | state machine 是 testbench 执行机制，不是目标 STM 数据。 |
| `executable-use-cases-domain-machine-specifications` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 出版商封闭；需人工全文确认。 |
| `web-tool-goal-statechart-derivation` | ❓ | ⚪ | 🔴 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | IEEE 封闭；需确认 input 是否自然语言。 |
| `ucgen-usecase-descriptions` | 🟠 | ⚪ | 🔴 | 🟠 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | 🟠 | 🔴 | 🔴 | 输出是 use case descriptions，不是 STM。 |

## 8. 旧九生成基线映射与本地证据容器

### 8.1 旧九生成基线映射（9/9）

本节是旧九生成方法与 seed 文库条目的摘要映射；`资源摘要（非原子）` 只是阅读提示，正式资源状态以 §7 的原子列为准。


| 原基线 | 种子方法 ID | 矩阵 ID | 单条目 | 输入 NL | 输出 STM | 生成方法 | 作者原生 pair | 资源摘要（非原子） | R2 用途 |
|---|---|---|---|---|---|---|---|---|---|
| Structure- and Event-Driven Frameworks | `sefm-llm-state-machine` | `sefm-llm-state-machine` | [sefm-llm-state-machine](./sefm-llm-state-machine/) | 8 个 reactive-system / system descriptions | UML state machine / statechart | LLM；单轮提示、结构驱动、事件驱动、混合策略 | 🟢 | 4open 制品 含代码 / 数据 / F1 workbook；许可 / 哈希 待冻结 | 强主 seed 候选 |
| LLMS EMP / SysML Behavior Models | `llms-emp-stm-subset` | `llms-emp-stm-subset` | [llms-emp-stm-subset](./llms-emp-stm-subset/) | 107 个 SysML 行为模型需求描述；只取 `diagram_type=stm` 子集 | PlantUML / SysML STM | LLM；requirements + prompt；含检查 / 反馈再生成设计 | 🟢 | 数据 / human review / results 强；流水线 代码未公开；Drive/许可 待核 | 强主 seed / judge 校准 |
| Designing FSM with GPT-4 | `designing-fsm-gpt4` | `designing-fsm-gpt4` | [designing-fsm-gpt4](./designing-fsm-gpt4/) | 合成英文 DFSM / Mealy 需求描述 | CSV DFSM / Mealy | GPT-4/GPT-4o；初始生成 + oracle / 检查 / 修正实验 | 🟡 | GitHub 有样例、generated text、部分 Graphviz / score；无 发布版本/许可 | 条件主；仅初始生成 |
| TTool-AI | `ttool-ai-smd-subset` | `ttool-ai-smd-subset` | [ttool-ai-smd-subset](./ttool-ai-smd-subset/) | platooning、spacebasedsystem、AutomatedBraking 等自然语言系统规范 | SysML/TTool state-machine diagram subset | ChatGPT 3.5；语法/语义检查、JSON→TTool XML | 🟡 | GitHub 制品 强；需从联合 SysML 模型中分离 SMD；provider drift/许可 待核 | 转换器压力 / 条件 seed |
| Umple thesis | `umple-nl-state-machine` | `umple-nl-state-machine` | [umple-nl-state-machine](./umple-nl-state-machine/) | 5 个自然语言 requirements 系统 | Umple textual state machine code | Llama 3；zero-shot、one-shot、RAG | 🟠 | PDF / thesis 稳定；完整 benchmark、输出包、评测脚本未公开 | 仅论文 种子证据 |
| REQ automotive thesis | `req-mermaid-statechart` | `req-mermaid-statechart` | [req-mermaid-statechart](./req-mermaid-statechart/) | Volvo Cars / Car Weaver 产品功能自然语言需求 | Mermaid.js statechart | GPT-3.5/GPT-4/GPT-4o；数据增强 / 微调 / prompt | 🔴 | 核心 NL、人工 statecharts、专家评分和输出样本未公开 | 私有数据 相关工作 |
| Pushing the Generative Envelope | `pushing-generative-envelope-mbse` | `pushing-generative-envelope-mbse` | [pushing-generative-envelope-mbse](./pushing-generative-envelope-mbse/) | air purifier、vacuum 两个简短 MBSE 题项 | SysML STM diagrams | local LLM；Mixtral、Llama-3-Smaug；shot / CoT / temperature 消融 | 🟠 | 论文公开；无代码、数据包、原始输出 或 许可 | 仅论文 prompt / temperature 参考 |
| FlowFSM / Agentic Flow | `protocol-flowfsm-seed-method` | `protocol-flowfsm-sentinel` | 仅旧基线 | RFC 协议文档 | 协议 FSM / rulebook | LLM agent / CrewAI；prompt chaining、CoT | 🔴 | RFC 输入公开；作者 规则书 / 标注答案 / 抽取迁移 未公开 | 协议域方法证据；不计控制系统四例 |
| SpecGPT / 3GPP extraction | `specgpt-3gpp-seed-method` | `3gpp-protocol-sentinel` | 仅旧基线 | 3GPP Release 17 标准文档 | 协议 FSM | GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro | 🔴 | 3GPP 输入可定位但需锁版本；代码 / 标注答案 / 输出 未公开 | 协议域 ensemble / span grounding 参考 |

### 8.2 24 个本地证据容器完整性表

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
| `unified-uml-multimodal-validation` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | HF dataset files |
| `unified-use-case-statecharts` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | - |

## 9. 人工下载队列 / 阻塞项

### 9.1 状态分布

| 状态 | 数量 | ID | R2影响 |
|---|---:|---|---|
| 已下载后排除 | 2 | `completion-sysml-gwt`、`towards-automatic-model-completion` | 已有全文并确认为 repair-only，不阻塞 R2。 |
| 元数据已足够排除 | 2 | `generating-statechart-designs-from-scenarios`、`ucgen-usecase-descriptions` | 元数据已足够排除，不阻塞 R2。 |
| 仍受阻 | 10 | `automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`semi-auto-efsm-standard-docs`、`rscharter-statechart-elements`、`nl-standard-docs-state-machines`、`requirements-analysis-prototyping-scenarios-statecharts`、`most-states-modes` | 可后续人工下载 / 相关工作，不应阻塞 R2。 |
| 新增待人工 | 2 | `executable-use-cases-domain-machine-specifications`、`web-tool-goal-statechart-derivation` | 新候选待人工全文确认，不作为 R2 阻塞项。 |

### 9.2 当前 待核 明细

本节只列人工下载 / 待核状态；可复制 BibTeX 片段见 §9.3。下载全文后，必须重新阅读全文并核验外部 artifact / code / dataset / license 页面，再更新 §5、§7 和必要单条目文件。

| ID | 标题 | 来源URL | 状态 |
|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | Automated Transition from Use Cases to UML State Machines to Support State-Based Testing | https://doi.org/10.1007/978-3-642-21470-7_9 | 仍受阻：Springer 付费墙 / 未发现公开 制品；PR-R2 可暂不依赖。 |
| `execution-nl-req-bt-sm` | Execution of Natural Language Requirements using State Machines Synthesised from Behavior Trees | https://doi.org/10.1016/j.jss.2012.06.013 | 仍受阻：ScienceDirect 访问受限；BT 中间产物 使其不作为主 seed。 |
| `maritaca-use-case-behavior-models` | MARITACA: From Textual Use Case Descriptions to Behavior Models | https://doi.org/10.1109/DSN-W.2017.33 | 仍受阻：IEEE 付费墙 / 未发现制品；高优先人工下载。 |
| `dependable-product-families-usecases-state-machines` | Modeling Dependable Product-Families: From Use Cases to State Machine Models | https://doi.org/10.1109/LADC.2016.28 | 仍受阻：IEEE 付费墙 / 未发现制品。 |
| `statechart-use-case-validation-event-driven` | Statechart-based use case requirement validation of event-driven systems | https://doi.org/10.1145/2245276.2231947 | 仍受阻：ACM 付费墙 / generation-vs-validation 边界。 |
| `semi-auto-efsm-standard-docs` | Semi-automatic Generation of Extended Finite State Machines from Natural Language Standard Documents | https://doi.org/10.1109/DSN-W.2015.17 | 仍受阻：IEEE 付费墙；默认 标准/协议 sentinel。 |
| `rscharter-statechart-elements` | Rscharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification | https://doi.org/10.2139/ssrn.4964857 | 仍受阻 / 开放但需浏览器：SSRN CLI 403；需人工浏览器下载。 |
| `nl-standard-docs-state-machines` | From Natural Language Standard Documents to State Machines: Advantages and Drawbacks | https://doi.org/10.2514/1.I010525 | 仍受阻：AIAA 访问受限；默认 标准/协议 sentinel。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | Requirements Analysis and Prototyping Using Scenarios and Statecharts | 待定位 | 仍受阻 / low priority：正式 PDF 未定位；方向疑似反。 |
| `most-states-modes` | Modeling and Verification of Natural Language Requirements based on States and Modes | https://doi.org/10.1145/3640822 | 仍受阻 / 开放但需浏览器：ACM/HAL CLI 受阻；默认 相关工作 不计 seed。 |
| `executable-use-cases-domain-machine-specifications` | Executable use cases as links between application domain requirements and machine specifications | https://doi.org/10.1049/ic:20040231 | 新增待人工：出版商封闭；非 R2 阻塞项。 |
| `web-tool-goal-statechart-derivation` | Web tool for Goal modelling and statechart derivation | https://doi.org/10.1109/RE.2015.7320444 | 新增待人工：IEEE 封闭；需确认 input 是否 NL。 |


### 9.3 人工下载 BibTeX 队列

本节给人工下载与补全文献时直接复制用；位置就是本文件 [§9.3](#93-人工下载-bibtex-队列) 的 `bibtex` 代码块，可整段复制到临时 `.bib` 文件或按单条复制到下载记录中。来源主要为 DOI/Crossref BibTeX，**不是最终正式引用库**。下载成功后应在对应单条目目录补 `paper.pdf`、用仓库 PDF 提取工具生成 `paper_content.txt`、以全文核验 `bibtex.bib`，并重新判断 §7 的资源列。`requirements-analysis-prototyping-scenarios-statecharts` 目前缺正式 DOI / 出版页，只保留占位，不能进入正式参考文献。

```bibtex
% 人工下载队列临时 BibTeX；正式引用以下载后的出版页/全文核验为准。

@inbook{Yue_2011_automated_transition_use_cases_uml_sm,
  title = {Automated Transition from Use Cases to UML State Machines to Support State-Based Testing},
  ISBN = {9783642214707},
  ISSN = {1611-3349},
  url = {https://doi.org/10.1007/978-3-642-21470-7_9},
  DOI = {10.1007/978-3-642-21470-7_9},
  booktitle = {Modelling Foundations and Applications},
  publisher = {Springer Berlin Heidelberg},
  author = {Yue, Tao and Ali, Shaukat and Briand, Lionel},
  year = {2011},
  pages = {115--131}
}

@article{Kim_2012_execution_nl_requirements_behavior_trees_sm,
  title = {Execution of Natural Language Requirements Using State Machines Synthesised from Behavior Trees},
  volume = {85},
  ISSN = {0164-1212},
  url = {https://doi.org/10.1016/j.jss.2012.06.013},
  DOI = {10.1016/j.jss.2012.06.013},
  number = {11},
  journal = {Journal of Systems and Software},
  publisher = {Elsevier BV},
  author = {Kim, Soon-Kyeong and Myers, Toby and Wendland, Marc-Florian and Lindsay, Peter A.},
  year = {2012},
  month = nov,
  pages = {2652--2664}
}

@inproceedings{Erazo_2017_maritaca,
  title = {MARITACA: From Textual Use Case Descriptions to Behavior Models},
  url = {https://doi.org/10.1109/DSN-W.2017.33},
  DOI = {10.1109/DSN-W.2017.33},
  booktitle = {2017 47th Annual IEEE/IFIP International Conference on Dependable Systems and Networks Workshops (DSN-W)},
  publisher = {IEEE},
  author = {Erazo, Leydi and Martins, Eliane and Greghi, Juliana Galvani},
  year = {2017},
  month = jun,
  pages = {83--90}
}

@inproceedings{Erazo_2016_dependable_product_families,
  title = {Modeling Dependable Product-Families: From Use Cases to State Machine Models},
  url = {https://doi.org/10.1109/LADC.2016.28},
  DOI = {10.1109/LADC.2016.28},
  booktitle = {2016 Seventh Latin-American Symposium on Dependable Computing (LADC)},
  publisher = {IEEE},
  author = {Erazo, Leydi and Martins, Eliane and Greghi, Juliana Galvani},
  year = {2016},
  month = oct,
  pages = {131--134}
}

@inproceedings{Tiwari_2012_statechart_use_case_validation,
  series = {SAC 2012},
  title = {Statechart-Based Use Case Requirement Validation of Event-Driven Systems},
  url = {https://doi.org/10.1145/2245276.2231947},
  DOI = {10.1145/2245276.2231947},
  booktitle = {Proceedings of the 27th Annual ACM Symposium on Applied Computing},
  publisher = {ACM},
  author = {Tiwari, Saurabh and Gupta, Atul},
  year = {2012},
  month = mar,
  pages = {1091--1093},
  collection = {SAC 2012}
}

@inproceedings{Greghi_2015_semi_automatic_efsm_standard_docs,
  title = {Semi-Automatic Generation of Extended Finite State Machines from Natural Language Standard Documents},
  url = {https://doi.org/10.1109/DSN-W.2015.17},
  DOI = {10.1109/DSN-W.2015.17},
  booktitle = {2015 IEEE International Conference on Dependable Systems and Networks Workshops},
  publisher = {IEEE},
  author = {Greghi, Juliana Galvani and Martins, Eliane and Carvalho, Ariadne Maria Brito Rizzoni},
  year = {2015},
  month = jun,
  pages = {45--50}
}

@article{Bhatt_2024_rscharter,
  title = {Rscharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification},
  url = {https://doi.org/10.2139/ssrn.4964857},
  DOI = {10.2139/ssrn.4964857},
  publisher = {Elsevier BV},
  author = {Bhatt, Janvi and Dasgupta, Sourish and Tiwari, Saurabh and Sharma, Akhilesh},
  year = {2024}
}

@article{Greghi_2018_nl_standard_docs_state_machines,
  title = {From Natural Language Standard Documents to State Machines: Advantages and Drawbacks},
  volume = {15},
  ISSN = {2327-3097},
  url = {https://doi.org/10.2514/1.I010525},
  DOI = {10.2514/1.I010525},
  number = {5},
  journal = {Journal of Aerospace Information Systems},
  publisher = {American Institute of Aeronautics and Astronautics (AIAA)},
  author = {Greghi, Juliana Galvani and Martins, Eliane and Carvalho, Ariadne M. B. R. and Ambrosio, Ana Maria and Villani, Emília},
  year = {2018},
  month = may,
  pages = {271--281}
}

@article{Liu_2024_states_modes,
  title = {Modeling and Verification of Natural Language Requirements Based on States and Modes},
  volume = {36},
  ISSN = {1433-299X},
  url = {https://doi.org/10.1145/3640822},
  DOI = {10.1145/3640822},
  number = {2},
  journal = {Formal Aspects of Computing},
  publisher = {Association for Computing Machinery (ACM)},
  author = {Liu, Yinling and Bruel, Jean-Michel},
  year = {2024},
  month = jun,
  pages = {1--47}
}

@inproceedings{Jorgensen_2004_executable_use_cases_domain_machine_specs,
  title = {Executable Use Cases as Links Between Application Domain Requirements and Machine Specifications},
  volume = {2004},
  url = {https://doi.org/10.1049/ic:20040231},
  DOI = {10.1049/ic:20040231},
  booktitle = {Third International Workshop on Scenarios and State Machines: Models, Algorithms, and Tools (SCESM04), W5S Workshop - 26th International Conference on Software Engineering},
  publisher = {IEE},
  author = {Jorgensen, J. B.},
  year = {2004},
  pages = {8--13}
}

@inproceedings{Pimentel_2015_goal_statechart_derivation,
  title = {Web Tool for Goal Modelling and Statechart Derivation},
  url = {https://doi.org/10.1109/RE.2015.7320444},
  DOI = {10.1109/RE.2015.7320444},
  booktitle = {2015 IEEE 23rd International Requirements Engineering Conference (RE)},
  publisher = {IEEE},
  author = {Pimentel, Joao and Vilela, Jessyka and Castro, Jaelson},
  year = {2015},
  month = aug,
  pages = {292--293}
}

@misc{requirements_analysis_prototyping_scenarios_statecharts_todo,
  title = {Requirements Analysis and Prototyping Using Scenarios and Statecharts},
  note = {人工下载队列占位：正式 DOI、作者、年份、venue 与 PDF 入口待核；不得作为正式引用使用。}
}
```

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
|---|---|---|---:|---:|---|---|
| `r17-01-openalex-broad-nl-requirements` | OpenAlex | 宽口径 NL requirements / statechart / use-case 检索簇 | 95 | 0 | 宽检索噪声高 / 宽检索保留为排除证据 | 详见 [round-r17-01-openalex-broad-nl-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-01-openalex-broad-nl-requirements.md) |
| `r17-02-crossref-refined-usecase-statechart` | Crossref | use-case / statechart / requirements 精细检索 | 50 | 1 | 无全文/制品 / 精确 DOI/标题发现 | 详见 [round-r17-02-crossref-refined-usecase-statechart.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-02-crossref-refined-usecase-statechart.md) |
| `r17-03-crossref-textual-usecase-behavior` | Crossref | textual 用例文本 / behavior models / state machine | 30 | 0 | 输出非 STM 噪声 / MARITACA 仍留人工队列 | 详见 [round-r17-03-crossref-textual-usecase-behavior.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-03-crossref-textual-usecase-behavior.md) |
| `r17-04-arxiv-llm-requirements` | arXiv | LLM + state machine / state diagram / requirements | 40 | 0 | 需求质量 / 切片 / 非 STM LLM 噪声 / 无新增 SA-1/2 种子 | 详见 [round-r17-04-arxiv-llm-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-04-arxiv-llm-requirements.md) |
| `r17-05-semanticscholar-阻塞项` | Semantic Scholar API | 6 检索簇 | 6 个错误 | 0 | HTTP 429 频率限制 / 降级到 OpenAlex/Crossref/arXiv/DBLP | 详见 [round-r17-05-semanticscholar-阻塞项.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-05-semanticscholar-阻塞项.md) |
| `r17-06-dblp-exact-title` | DBLP API | 12 精确标题人工 / 经典候选 | 429 / 连接限制前确认 3 条 | 0 | DBLP 频率/连接限制 / 仅元数据互证 | 详见 [round-r17-06-dblp-exact-title.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-06-dblp-exact-title.md) |
| `r17-07-classic-fulltext-wave` | 开放/出版商 PDF | 经典用例 / 嵌入式 / 测试生成全文波次 | 7 | 7 dirs | 均仅论文 / 两个硬边界 / 强化排除证据; 无新增 SA-1/2 | 详见 [round-r17-07-classic-fulltext-wave.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-07-classic-fulltext-wave.md) |
| `r17-08-manual-queue-artifact-recheck` | 出版商精确检索 + 制品检索 | R1.6 人工队列 + R1.7 新增人工候选 | 13 | 1 个新增下载目录 | 付费墙 / 需浏览器访问的开放入口 / 无制品 / 人工队列状态分布已更新 | 详见 [round-r17-08-manual-queue-artifact-recheck.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-08-manual-queue-artifact-recheck.md) |

归档入口：

- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/)

## 12. 文献筛查与全文阅读 provenance 摘要

旧 `agent_provenance.md` 已归档为 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md)。其记录范围仅限文献筛查、全文阅读、证据等级调整和研究性 阻塞项；不记录 PR review / ready / merge 进度。R1.7 最终整合输出为：47 候选 / 47 筛查 / 24 单条目目录；主 / 条件主可计候选仍为 4；Semantic Scholar API 429 已记录并由 OpenAlex/Crossref/arXiv/DBLP exact-title 替代。

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
| `seed_corpus/papers/<slug>/` | `corpora/seed_library/<slug>/；本地证据容器表进入 SUMMARY §8` | corpora/seed_library/<slug>/ + SUMMARY §8 | 24 个单篇 / 制品证据容器迁入当前 seed library。 |

## 15. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 20:45:00 | PR-R1.8-B：补充人工下载 BibTeX 队列，明确资源可获取性必须基于全文阅读与外部资源页核验，不能只看本地 repo 资源。 |
| 2026-06-14 20:35:00 | PR-R1.8-B：修复 review 指出的 pair 口径同步问题，补入可重建 pair、作者原生 pair、配对索引与 R2 交接列，并把 R2 实验输入可用性标为派生汇总项。 |
| 2026-06-14 20:10:00 | PR-R1.8-B：按 review I 级意见继续拆分资源矩阵，新增来源文档、STM_0 数据、配对索引、原始生成输出、评测结果 / 日志、许可、版本 / 哈希等列，并说明 R2 实验输入可用性不能由单个资源 emoji 代替。 |
| 2026-06-14 19:30:00 | PR-R1.8-B：继续中文化 SUMMARY，新增资源可获取性分级说明，细化候选矩阵中的当前角色与主要风险，并把资源盘点范围明确到论文本体、源码、NL 数据、STM 数据、作者原生 pair、实验结果和许可 / 版本 / 哈希。 |
| 2026-06-14 18:45:00 | PR-R1.8-B：按最新审阅意见中文化 SUMMARY，拆分耦合列，新增 emoji 枚举口径与外部资源可获取性矩阵；明确本地证据容器表不等同于资源可用性。 |
| 2026-06-14 17:55:00 | PR-R1.8-B：迁移旧 `seed_corpus/` 到 `corpora/seed_library/`；建立三件套；旧横向 ledger、检索轮次 / results 进入 archive；当前 SUMMARY 可复算 `47/47`、`24 dirs`、`9/9 映射`、R2=4 和 人工队列状态。 |
| 2026-06-14 13:20:00 | PR-R1.7 有界快照 v4：纠正 seed 方法集合 vs R2 四例计数口径，补齐旧九 旧基线直接映射，新增 `pushing-generative-envelope-mbse`，扩展到 47 候选 / 47 筛查 / 24 单条目目录；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 12:10:00 | PR-R1.7 有界快照 v3：扩展到 46 候选 / 46 筛查 / 23 单条目目录 / 8 R1.7 检索轮次；新增 经典全文波次、人工队列状态分布和 排除证据；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 03:55:00 | PR-R1.6 有界快照 v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF 制品核验、search_rounds 与 PR-R2 交接。 |
| 2026-06-14 02:22:00 | 补齐 `req-mermaid-statechart` 单篇目录与 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 阻塞项交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
