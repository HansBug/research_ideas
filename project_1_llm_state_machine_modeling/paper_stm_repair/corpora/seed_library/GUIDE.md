# seed_library/GUIDE.md

## 1. 目标与边界

本 GUIDE 约束种子文库的后续维护。种子文库只回答一个问题：哪些上游工作或来源能提供、描述或帮助构造 `<NL, STM_0>`，且其中 `STM_0` 与 `NL` 存在可追踪的生成 / 派生 / 人工建模关系。

不得把种子文库写成本论文修正基线文库；若同一工作也包含 repair / feedback / completion 环节，应在 [../repair_baselines/](../repair_baselines/) 另行登记其修正能力，并在两边交叉链接。若对象只有控制系统 NL 输入、尚未闭合 `NL -> STM_0`，应留在 [../nl_datasets/](../nl_datasets/)。

## 2. REGISTRY + SUMMARY 分工规则

从一手 registry 口径起，本目录有两个互补事实层：

1. [REGISTRY.md](./REGISTRY.md) 是逐条一手资源明细主表，负责条目、一手入口、`assets/README.md` 直链、NL 数量、pair 统计、eligible count、caveat / blocker、R2 选择建议和单条目 `seed_resource_registry.json` 跳转。
2. [SUMMARY.md](./SUMMARY.md) 是研究结论与统计摘要入口，负责候选全集、文献资格、资源分布、风险、迁移关系和面向 R2 的摘要；它不复制 [REGISTRY.md](./REGISTRY.md) 的全量逐条资源明细。
3. [README.md](./README.md) 只做定位、阅读顺序和最小速览，不维护独立事实表或第二套统计。

[REGISTRY.md](./REGISTRY.md) 的维护纪律：

1. 主表第一列必须叫“条目”，若该条目存在 `assets/README.md`，条目名本身必须直接链接到该文件，例如 [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md)；没有 `assets/` 的条目才保留普通文本。
2. 不再单独设置 `assets` 列；资源入口必须通过左侧条目链接进入，机器可读记录继续放在“结构化记录”列。
3. 表头、说明列、R2 建议、阻塞项、状态描述能用中文就用中文；`recommended_role`、`source_status`、hash、文件路径、schema 字段等机器枚举可以保留反引号英文，但解释文本必须中文化。
4. `generated eligible`、`trace verified` 等英文统计含义在表头中写作“可计生成对”“已回溯验证”；不要让读者必须理解英文才能读懂主表。
5. 主表必须维护 `NL 数` 与 `NL-only`：`NL 数` 写作 `raw / unique`；`raw` 是一手资源中可定位的 NL 行/条目数，`unique` 是按 NL 文本去重后的数量；`NL-only` 是有 NL 但无可计 generated `STM_0` 的数量。paper-only / 未机读条目统一写 `0 / 未知`，不得把论文图示数冒充一手资源数。§4 未建 registry 条目的处置表也必须保留 `NL 数`、`NL-only`、`可计生成对` 三列，默认按当前一手机读资源写 `0 / 未知`、`未知 / 未知`、`0`。
6. 每次新增或修改 `assets/README.md`、`seed_resource_registry.json`、`assets/manifest.json`、`validation_summary.json` 后，都必须同步核对 [REGISTRY.md](./REGISTRY.md) 主表的条目链接、计数、状态、NL 数、阻塞项 / caveat 和 [SUMMARY.md](./SUMMARY.md) 的摘要。
7. 若依据旧 `reproduction/`、旧 parquet、旧 predictions、旧 discussion assets 或 `project_ex1` review corpus 发现候选，只能把它们登记为 `legacy_audit_refs` / “发现入口”；不得把这些二手文件写入 `assets/`，不得用它们提升资源可获取性、pair 数、`trace_verified` 或 `recommended_role`。升级任何条目必须回到论文、作者 artifact、官方数据集、作者仓库、出版页 Data Availability、可版本化 release 等一手入口重新下载 / 核验，并用 raw hash + locator + validator 回写 [REGISTRY.md](./REGISTRY.md)。

新增条目时，不得只创建目录或只改单篇文件；必须同步更新单条目 `seed_desc.md` / `artifacts.md`、必要的 `seed_resource_registry.json` / `assets/` 审计链，以及 [SUMMARY.md](./SUMMARY.md) 中对应的统计摘要或风险结论。若新增的是一手资源或 pair 明细，必须优先回写 [REGISTRY.md](./REGISTRY.md)，再更新 [SUMMARY.md](./SUMMARY.md) 摘要。

人工下载的 BibTeX 起点应集中维护在 [manual_download_queue.bib](./manual_download_queue.bib)；当 PDF 尚未拿到时，只在该文件追加可复制条目，`SUMMARY.md` 只保留状态与路径，不再保留长 BibTeX 代码块。

## 3. emoji / enum 标准

正式总账表中，emoji 列只写 emoji，中文释义集中写在本节和 [SUMMARY.md](./SUMMARY.md)。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达，❓表示待核，⚪表示不适用。

### 3.1 偏序型 emoji 口径

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 文献资格（非 R2 eligibility） | 强方法证据：清楚满足 `NL -> T0 STM-family` | 条件方法证据：关系清楚但有 synthetic / 制品 / T0 等边界说明 | 扩展 / 边界证据：对方法或转换压力有价值 | 不满足或明确排除 | 待核 | 不适用 |
| T0 适配 | T0 明确 | 大体 T0，但需切片或少量格式转换 | 存在 timed / hybrid / protocol / 中间产物 风险 | 非 STM family 或不可隔离 | 待核 | 不适用 |
| 生成关系 | 明确 `NL -> STM_0` | 方向基本成立但需切片 / 初始输出隔离 | 只有间接、中间模型或 paper-level 重建线索 | 不是 `NL -> STM_0` | 待核 | 不适用 |
| R2 实验输入可用性（派生汇总） | 关键输入可直接冻结：NL 数据、STM_0 数据、作者原生 pair、可重建 pair、配对索引、版本 / 哈希均可支撑实验 | 关键输入基本可用但需抽取、切片或冻结版本 | 只可论文级重建或需要大量人工整理 | 关键输入不可得，不能直接做 R2 样本 | 待核 / 访问受阻 | 对该条目不适用 |
| R2.0 registry 角色 | `final_pool_ready` | `conditional_final_pool` | `pipeline_only` / `paper_reconstructable` | `related_only` / `excluded` | 待核 | 不适用 |
| 泄漏风险 | 未见明显泄漏 | 需隔离 reference / repair / oracle 字段 | 泄漏风险高，必须强约束使用 | 无法隔离 | 待核 | 不适用 |
| 本地证据容器 | 本地文件存在且可读 | 本地文件存在但需修复 / 质量较弱 | 只有替代证据或待整理 | 缺失且应补 | 待核 | 该条目按设计不需要 |

### 3.2 外部资源可获取性口径

资源盘点面向后续实验和论文证据链能否直接使用，不等于本地文档是否齐全。每个条目至少要分别判断：论文本体、来源文档、生成/复现实验代码、NL 数据、STM_0 数据、作者原生 `<NL, STM_0>` pair、可重建 `<NL, STM_0>` pair、配对索引、原始生成输出、评测结果 / 日志、版本 / 哈希。许可 / 再分发不作为升绿 blocker，但仍可作为来源说明。整体 R2 实验输入可用性是派生汇总项，不能由单个“资源可用”emoji 代替，至少要同时检查 `NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引` 和 `版本 / 哈希`；许可 / 再分发只作来源说明和论文引用提醒，不作为升绿 blocker。

**硬约束**：资源可获取性必须由全文阅读和外部资源页共同支撑。可用证据包括 DOI / 出版页、官方 PDF、论文正文 / 脚注 / Data Availability 明确指向的作者或项目仓库、Zenodo / OSF / Hugging Face / Figshare 等数据页、补充材料、artifact 页面、许可 / 引用说明、release / commit / hash。只看本地 `paper.pdf`、`paper_content.txt`、`seed_desc.md`、`artifacts.md` 或历史 PR 评论，不足以把外部资源列升级为 🟢/🟡；全文或资源页受阻时必须保留 ❓/🔴 并写明阻塞。

**状态边界**：入口已定位但因 403 / WAF / CAPTCHA / 登录 / SPA 壳 / 网络超时等暂时无法核验时，优先记为 `❓`，说明列写 `入口 URL + 访问日期 + 受阻类型 + 待人工核验`；只有官方页面明确声明未公开、404 且无替代入口、或全文核验后确认不可得时，才记为 `🔴`。

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

### 3.3 分类型枚举口径

| 字段 | 允许值 / 写法 | 说明 |
|---|---|---|
| 生成者 | 人工 / 规则算法 / NLP工具 / LLM / 多阶段流水线 / 混合 | 只描述 `STM_0` 的产生方式；不要把本论文后续修正循环混入种子阶段。 |
| LLM参与 | 是 / 否 / 可能 / 不适用 | “可能”必须在说明列给出证据不足原因。 |
| NL类型 | 需求文本 / 用例 / 场景文本 / 系统描述 / 标准文档 / 合成需求 / 来源文档 / 非NL | 用中文写，不再使用 `non-structured` 等英文短语。 |
| STM类型 | FSM / HSM / EFSM / UML statechart / SysML STM / PlantUML / Mermaid / Umple / 协议FSM / 非STM | 协议FSM、非STM默认不计控制系统四例。 |
| 资源列 | 论文 / 来源文档 / 生成代码 / NL 数据 / STM_0 数据 / 作者原生 pair / 可重建 pair / 配对索引 / 原始生成输出 / 评测结果 / 许可 / 版本 / 哈希 | 资源可获取性面向后续实验可用资源，不等同于本地 `seed_desc.md` 是否存在；只统计论文正文 / 脚注 / Data Availability / 参考文献、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手入口，本仓库缓存的 parquet、ZIP、代码、PDF 或 hash 只作本地证据。 |
| 排除码 | `X_PROTOCOL_FSM` / `X_PROCESS_MODEL` / `X_NON_STM_FORMALISM` / `X_T1PLUS_TIMED_HYBRID` / `X_SEQUENCE_ONLY` / `X_REPAIR_ONLY` / `X_COEXIST_ONLY` | 排除码用于防误收；不能因为“看起来有 state machine”就绕过生成关系与 T0 范围。 |


### 3.4 结论总表的 NL / STM / 时间列口径

[README.md](./README.md) 核心表与 [SUMMARY.md](./SUMMARY.md) §16 不得只写“真实 NL=是 / STM family=是”。必须拆出：

1. `NL输入是什么`：说明输入是需求、系统描述、use case、SRS、标准文档、goal model、scenario，还是合成文本；若不是 NL-only 必须明说。
2. `STM输出是什么`：说明输出是 UML state machine、SysML / PlantUML STM、DFSM/Mealy CSV、EFSM、statechart elements、MoSt/NuSMV 等具体制品。
3. `STM关键特性`：说明状态机是否含层次、区域、伪状态、guard、action、变量、exception、variability、组合/合并、输入输出等对后续转换和修正有影响的特征。
4. `STM谱系`：说明属于 FSM、HSM/statechart、EFSM、SysML/UML state machine，还是中间/边界/非目标形式化模型。
5. `时间特性等级`：只按全文和制品证据判断。默认用“未见显式时钟”表达没有发现 timed automata clock、连续时间或 hybrid dynamics；用“数据/守卫级”表达变量、guard、exception 或 EFSM 数据状态；证据不足时写“待核”。不要为了表格完整臆测时钟或时间约束。
6. `资源获取方式` / `关键资源获取方式`：必须给出可点击的一手入口链接；若只有本仓库本地缓存、历史 agent 另行找到的非论文链接、未确认与论文对应的仓库、或当前 repo 中已有的 parquet / 代码 / PDF / hash，只能写作“本地证据 / 线索”，不得计为作者公开资源。

### 3.5 一手资源 registry 与 assets 纪律

从一手 registry 口径起，seed library 采用 **REGISTRY 明细 + SUMMARY 摘要 + 单条目 assets 审计链**：

1. [REGISTRY.md](./REGISTRY.md) 是逐条资源明细主表；[SUMMARY.md](./SUMMARY.md) 只保留研究结论、统计摘要与风险，不复制全量明细。REGISTRY 主表必须用“条目”列直接链接到对应 `assets/README.md`，不得另设 assets 列。
2. 单条目 `assets/` 是短名，但语义必须是**一手来源资产目录**。只有论文 / 作者 artifact / 官方数据集 / 作者仓库 / 出版页 Data Availability / 可版本化 release 中直接取得的文件，及其从 raw 直接抽取得到的审计产物，可以进入 `assets/`。
3. 本仓库历史 parquet、旧缓存、人工复写、论文图示重建、PR comment 摘要、`reproduction/` 输出和 `project_ex1` review extraction 只能写入 `legacy_audit_refs` 或 blocker，不能升级为 current first-source asset；这些二手线索最多用于定位应重新核验的一手入口。
4. “重点条目”指 [REGISTRY.md](./REGISTRY.md) §2 已纳入一手资源主表、或后续准备升级为 R2.0 种子 / 资源候选的条目；这些条目必须有 `seed_resource_registry.json`。尚未建 registry 的既有目录默认按 [REGISTRY.md](./REGISTRY.md) §4 的 `paper_reconstructable` / `related_only` 处置，可计生成数量视为 0，不得被 R2 直接选用。
5. 有一手 raw 或 conditional pair 的条目还必须有 `assets/manifest.json`、中文 `assets/README.md`、`assets/raw/`、`assets/extracted/`。
6. `assets/extracted/pairs.jsonl` 的每个 pair 必须至少记录 `pair_set_id`、`eligibility_state`、`exclusion_reason`、`source_asset_id`、`source_locator_type`、`source_locator`、`source_sha256`、`nl_text` / `nl_sha256`、`stm0_text` / `stm0_sha256`、`is_generated_stm0`、`is_reference`、`is_postprocessed`、`trace_verified`。
7. `seed_resource_registry.json` 必须维护 `source_inventory`、`data_construction`、`quality_audit` 三组机器可读字段：
   - `source_inventory` 至少写清 `raw_nl_count`、`unique_nl_count`、`nl_only_count`、`nl_only_unique_count`、`generated_pair_count`、`eligible_generated_pair_count`、`reference_pair_count`、`canonical_case_count`、`unique_generated_stm0_count`、`one_to_many_shape`、`count_status`、`count_basis`、`notes`；`REGISTRY.md` 的 `NL 数` 与 `NL-only` 必须可由这些字段解释，并且这些字段会被 validator 从 `pair_sets[].nl_count`、`pairs.jsonl`、raw locator 或 pipeline raw 结构复算，不能只靠人工填表。
   - 计数语义固定为：`raw_nl_count / unique_nl_count` 表示一手资源中可定位的 NL 原始条目数与去重数；`generated_pair_count` 表示作者一手资源中已登记的生成输出行数（可包含被明确排除的 failure 行）；`eligible_generated_pair_count` 表示可进入 seed 的有效生成对；`unique_generated_stm0_count` 表示真实 generated `STM_0` 输出文本去重数；明确排除的 failure sentinel（如 `No valid PlantUML code found.`）只进入 `nl_only_count`、`validation_summary.excluded_pair_ids` / `notes` 与 `extraction_notes.md` 审计，不得抬高 generated `STM_0` diversity。
   - `data_construction` 必须说明论文如何描述数据来源 / 构造流程、artifact 实际来源、`raw_nl` 是什么、`STM_0` 是什么，并给出证据路径；不得只写“见论文”。
   - `quality_audit` 必须记录抽检状态、样本数、样本标识、质量发现、领域适配 caveat 与证据路径；没有一手 pair 的 paper-only 条目也必须明确写 `not_applicable_no_first_source_pair`，避免后续误以为未审。
8. 只有 validator 能按 raw hash + locator + 文本 / 文本 hash 回溯成功，且 `trace_verified=true`、`is_generated_stm0=true`、`is_reference=false`、`is_postprocessed=false` 的 pair 才能计入 eligible generated seed count；不能只信任 `pairs.jsonl` 自报。eligible generated row 的 `eligibility_state` 必须与所属 `pair_sets[].eligibility_state` 一致，且 `exclusion_reason` 必须为空；非阻塞 caveat 写入 registry / README，而不是写成 row-level exclusion。若 raw 中存在生成失败行（例如 `No valid PlantUML code found.`），应保留为审计行但设置 `is_generated_stm0=false`、`eligibility_state=excluded`、`exclusion_reason` 明确原因，不得静默丢弃或计入 eligible。
9. 当前 validator 已支持 `parquet_row_columns`、`xlsx_sheet_row_columns`、`zip_python_symbol_and_text_file` 三类 locator。新增 locator 类型前必须先扩展 validator 与负向测试，再把对应 pair 计入 trace verified。
10. `storage_mode=committed` 可支撑仓库内直接复验；`local_only` 只能 conditional；`metadata_only` 不得标为 `final_pool_ready`。
11. 公开学术资源的 license / redistribution 不再作为 `final_pool_ready` blocker；维护时可在 `license_status` / `redistribution_status` 中写 `paper_public_resource` / `cite_original_work`，并在论文中规范引用原作。

校验入口：

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/corpora/seed_library/tools/validate_seed_assets.py unified-uml-multimodal-validation
```

JSON schema 位于 [schemas/seed_resource_registry.schema.json](./schemas/seed_resource_registry.schema.json) 与 [schemas/assets_manifest.schema.json](./schemas/assets_manifest.schema.json)。

## 4. SUMMARY 表格字段纪律

[SUMMARY.md](./SUMMARY.md) 的横向表应拆分维度，避免一列塞入多个概念：

1. **候选全集表**：至少拆出 `ID`、`年份`、`来源批次`、`NL类型`、`STM类型`、`T0`、`关系`、`文献资格`、`R2.0 registry 角色 / 状态`、`当前角色`、`主要风险`、`证据`。
2. **R2 交接 / registry queue 表**：至少拆出 `recommended_role`、`generated_eligible_count`、`trace_verified_count`、`first_source_status`、`NL 数据`、`STM_0 数据`、`blocker`、`下一步`；旧 `R2` 单列不得替代一手 registry 判断。
3. **外部资源可获取性表**：必须面向后续可用资源，至少覆盖 `论文本体`、`来源文档`、`生成/复现实验代码`、`NL 数据`、`STM_0 数据`、`作者原生 pair`、`可重建 pair`、`配对索引`、`原始生成输出`、`评测结果 / 日志`、`许可 / 引用说明`、`版本 / 哈希`、`获取性说明`。
4. **本地证据容器表**：可以检查 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`seed_desc.md`、`artifacts.md`，但必须明确它不是外部资源可用性表。
5. emoji 列只写 emoji；若需要解释，放到相邻说明列或标准表中。

## 5. 单条目维护

生成或重写单条目派生文件时遵循：

1. 先读 `bibtex.bib` 核定元信息。
2. 再尽量完整读 `paper_content.txt`；若缺失或异常，按仓库 PDF 提取规范处理。
3. 必要时核对 `paper.pdf`。
4. 更新 `seed_desc.md`：生成关系、T0 / STM-family 边界、文献资格、R2.0 `recommended_role`、blocker、是否可计为生成 pair、风险和证据指针。
5. 更新 `artifacts.md`：外部资源可获取性，包括论文本体、来源文档、生成/复现实验代码、NL 数据、STM_0 数据、作者原生 `<NL, STM_0>` pair、可重建 `<NL, STM_0>` pair、配对索引、原始生成输出、评测结果 / 日志、引用说明、版本 / 哈希、人工阻塞项、复跑风险。写这些字段前必须阅读全文，并逐项打开外部 artifact / code / dataset / 引用说明 / release 页面核验；若只能看到本地缓存或二手摘要，一律标为待核或受阻。
6. 回填 [SUMMARY.md](./SUMMARY.md) 的候选全集表、外部资源可获取性表、本地证据容器表和更新日志。人工下载队列需要补 BibTeX 时，优先更新 [manual_download_queue.bib](./manual_download_queue.bib)，并在 [SUMMARY.md](./SUMMARY.md) §9 只保留状态与链接，不新增根层横向台账。

仅制品 条目可以缺 `paper.pdf` / `paper_content.txt`，但必须有 `seed_desc.md` 与 `artifacts.md`，并在 [SUMMARY.md](./SUMMARY.md) 的本地证据容器表中解释；这不等于其外部 `STM_0` 输出已经可用。

## 6. archive 使用规则

[../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/) 只保留 R1.5--R1.7 旧台账、检索轮次和原始检索结果。archive 内旧链接按历史快照保留，可能指向迁移前的 `papers/` 或台账路径；需要当前事实时必须回到 [SUMMARY.md](./SUMMARY.md) 和本目录单条目。

## 7. 禁止事项

- 禁止新增根层横向台账作为第二事实源。
- 禁止把旧 `NL -> STM` 生成基线改写成本论文修正基线。
- 禁止把 protocol / standard FSM、BPMN/process、Petri/CSP/Event-B/TLA+/LTL/STL、repair-only、co-exist-only、sequence/formal scenario 等误计为 `final_pool_ready` 或 `conditional_final_pool`。
- 禁止把“本地有 `seed_desc.md` / `artifacts.md`”误写成“作者公开了 `<NL, STM_0>` 原生配对”。
- 禁止在仓库文件中维护 PR 流程状态、review 状态、ready gate、commit / push / merge 进度。
- registry 文档维护和 validator 测试不调用真实 LLM，不读取 `.env`；若后续复跑构造 seed，必须按 run record 规则单独记录。

## 8. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-23 12:10:59 | PR-R2.0：补充旧 `reproduction/`、旧 parquet 与 `project_ex1` 只能作为发现入口的 REGISTRY 维护纪律，要求所有升级回到一手入口和 validator，不得把二手资源写入 `assets/` 或用于升绿。 |
| 2026-06-22 22:10:00 | PR-R2.0：补强 validator 对 `source_inventory` 派生计数与 JSON Schema enum 的校验要求，防止 REGISTRY 与 JSON 同步篡改后仍通过。 |
| 2026-06-22 21:30:00 | PR-R2.0：将 `source_inventory` / `data_construction` / `quality_audit` 纳入 registry 必填纪律，明确所有登记条目都要写 NL raw/unique/NL-only 与数据构造 / 抽检状态；公开学术资源许可不作为升绿 blocker。 |
| 2026-06-22 20:30:00 | PR-R2.0：补充 pair-level eligibility 与 registry pair-set 状态一致性纪律，明确 eligible row 不得携带 `exclusion_reason`，非阻塞 caveat 只能写 registry / README。 |
| 2026-06-22 19:40:00 | PR-R2.0：补充全量 parquet / xlsx locator 纪律，明确生成失败行需保留但不计 eligible，validator 已支持 `xlsx_sheet_row_columns`。 |
| 2026-06-22 19:10:00 | PR-R2.0：补充 REGISTRY 维护纪律，规定条目列直链 `assets/README.md`、不另设 assets 列、主表能中文尽量中文。 |
| 2026-06-22 18:30:00 | PR-R2.0：初始化一手 registry 口径，明确未建 registry 目录默认不可入池，并补强 validator 的 raw locator / 文本 hash 回溯校验；后续本轮已更新为 `final_pool_ready=3`。 |
| 2026-06-15 14:23:39 | PR-R1.8-B：规定 README 核心表与 SUMMARY §16 必须显式拆出 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系和时间特性等级，并要求资源列只写一手可点击入口，本地 parquet / 代码缓存不计资源。 |
| 2026-06-14 23:40:00 | PR-R1.8-B：Yue 2011 已补全文并转正到 seed 目录；人工下载 BibTeX 队列只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | PR-R1.8-B：接入人工下载后的 36 dirs 口径，规定人工下载 BibTeX 放入 `manual_download_queue.bib`，SUMMARY 只保留状态链接。 |
| 2026-06-14 20:50:00 | 进一步明确资源页受阻时的 ❓ / 🔴 边界，避免把可定位但暂时打不开与确实不可得混淆。 |
| 2026-06-14 20:45:00 | 补充全文阅读 + 外部资源页核验硬约束，并在当时的过渡口径下规定人工下载 BibTeX 片段集中维护在 SUMMARY §9。 |
| 2026-06-14 20:35:00 | 修复 pair 口径同步问题，补入可重建 pair、作者原生 pair、配对索引与 R2 交接列，并把 R2 实验输入可用性标为派生汇总项。 |
| 2026-06-14 20:10:00 | 按 review I 级意见继续拆分资源矩阵和字段纪律，新增来源文档、STM_0 数据、配对索引、原始生成输出、评测结果 / 日志、许可、版本 / 哈希，并明确 R2 实验输入可用性聚合规则。 |
| 2026-06-14 19:30:00 | 继续细化资源可获取性分级，明确资产盘点应覆盖论文本体、生成代码、NL 数据、STM_0 数据、作者原生 pair、实验结果 / 原始输出和版本 / 哈希；同步候选全集拆列纪律。 |
| 2026-06-14 18:45:00 | 补充 emoji / enum 标准、中文字段纪律和外部资源可获取性规则，明确资产盘点面向论文、生成代码、NL 数据、STM_0 数据、作者原生 pair、实验结果与许可版本。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 建立种子文库维护规则，冻结 SUMMARY-first 与 archive 边界。 |
