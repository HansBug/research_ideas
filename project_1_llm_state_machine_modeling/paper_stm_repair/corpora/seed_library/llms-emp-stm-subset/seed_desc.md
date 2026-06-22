# On the Empirical Evaluation of LLMs for Model Generation / Generating SysML Behavior Models via LLMs

## R1.5 strict seed 编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `llms-emp-stm-subset` |
| source_batch | baseline / local fulltext + source ASSETS/DESC |
| local_source | [`baselines/llms_emp/`](../../../../baselines/llms_emp/) |
| strict_seed_grade | `SS-A` |
| artifact_usability | `SA-2` |
| 当前结论 | 入选 strict seed；仅取 STM 子集。该论文充分支持 `NL requirements -> SysML/PlantUML state machine` 生成与反馈式再生成；R2 只冻结初始 / 指定 `STM_0`，不要混入作者后续 human review / feedback 改进结果。公开资产偏数据/结果表，不是完整 pipeline 复现包。 |

## P1/P2/P3/P4 全文核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt:175-183` 明确评估 LLMs 从 natural-language requirements 生成 SysML behavioral diagrams；`paper_content.txt:190-197` 说明公开数据集中每个模型 paired with natural-language requirements；`paper_content.txt:371-381` 说明对缺失需求的案例根据模型结构推断并编写描述；`paper_content.txt:582-591` 说明 prompt 中提供 Requirements Descriptions，引导 LLM 生成对应 behavioral model。 |
| P2_T0_STM_FAMILY | pass | `paper_content.txt:131-137` 将 STM 与 ACT/SD 一起定义为本研究关注的 SysML behavioral diagrams；`paper_content.txt:458-483` 的 Table 2 按 N#STM 列出状态机样例并给出 Total 36；`paper_content.txt:491-500` 将 STM 节点/边定义为 State、Vertex、Pseudostate、Region 与 Transition，属于 T0 FSM/HSM/statechart 家族；`paper_content.txt:701-728`、`paper_content.txt:899-904` 进一步出现 Composite State、Region、PseudoState、Transition 等 STM 结构。 |
| P3_GENERATION_RELATION | pass | `paper_content.txt:176-183` 描述 Phase-I prompt template 和 Phase-II regeneration；`paper_content.txt:410-428` 说明需求与辅助上下文进入 prompt，输出经验证后将 feedback 注入 revised prompt 再生成；`paper_content.txt:575-596` 给出 Role / Instruction / Requirements / Sample / Error 五组件 prompt，其中 Requirements 是输入，Error 是模型检查反馈；`paper_content.txt:780-788` 说明基于 RQ1 hallucination rules 进行 feedback-driven model regeneration。 |
| P4_EVIDENCE_POINTER | pass | 论文 DOI 与 BibTeX 见 `bibtex.bib`；本地全文见 `paper.pdf` 与 `paper_content.txt`；公开数据集 URL 见 `paper_content.txt:190-197` 和脚注 `paper_content.txt:212-213`；源 baseline `ASSETS.md` 记录了 Drive 入口、本地 parquet 冻结路径与 SHA-256。 |

## SS / SA 结论

**SS-A**：满足 strict seed 的四个核心谓词。该候选的 STM 子集可以作为自然语言需求到状态机图生成任务的 seed：输入是需求描述，目标/参考模型是 PlantUML 格式 SysML STM，生成关系和反馈式再生成关系均有全文证据。

**SA-2**：数据与结果资产可用，但不是完整可复现代码包。源 `ASSETS.md` 说明论文公开 Google Drive 数据集，并在本仓库冻结了 raw/complete/human-review parquet；同时明确未发现公开生成脚本、模型调用脚本、RAG、PlantUML/SysML 检查或 feedback regeneration pipeline 源码。因此 R2 可直接使用数据级 STM seed，但若要复现实验方法，需要自行实现 pipeline。

## 排除码与边界

| 排除码 | 状态 | 说明 |
|---|---|---|
| `EX-ACT-SD` | active | 本候选只取 STM 子集；ACT 与 SD 样例不进入 STM repair seed。 |
| `EX-PIPELINE-CODE-ABSENT` | active | 论文与源 `ASSETS.md` 均未定位公开生成/修复 pipeline 源码，不能标为完整方法复现包。 |
| `EX-DATA-LICENSE-PENDING` | inactive for R2.0 eligibility | 公开学术 Drive 数据后续论文引用原作即可；R2.0 不再把 license / 再分发作为升绿 blocker。 |
| `EX-PROTOCOL-ONLY` | inactive | 证据显示为 SysML state machine diagrams，不是协议-only trace/spec。 |
| `EX-T1-TIMED-HYBRID` | inactive | 未见 timed automata / hybrid automata 作为目标模型；“Hybrid Sport Utility Vehicle”只是案例名称，不改变模型族。 |
| `EX-IMAGE-ONLY` | inactive | 论文说明原始来源多为图像，但作者已重建为 PlantUML，并配套需求描述。 |

## R2 可用性

可用方向：

1. 从公开数据或本地 parquet 冻结中抽取 STM 样例，构造 `NL requirement -> PlantUML/SysML STM` 的 R2 seed；只冻结初始/指定版本 `STM_0`，不要混入作者后续 human review / feedback 改进结果。
2. 用 human-review / generated-output 结果表做 LLM-as-Judge、hallucination taxonomy、repair benchmark 的对照材料。
3. 使用论文 Table 8-11 的 STM hallucination 与 checking-rule 分类作为 repair 任务的错误类型参考。

不可直接声称：

1. 不能声称已经获得作者原始 prompt runner、RAG 检索器、checker 或 regeneration 代码。
2. 不能将 Drive 当前内容视为不可漂移；正式 run record 应固定本地 parquet hash、行数、抽取日期和 eligibility filter。
3. 不能把 ACT/SD 结果混入 STM seed 统计。

## Pending / blocker

- `pending:file_level_drive_audit`：本轮未逐文件打开 Drive；使用源 `ASSETS.md` 的 2026-06-10 记录和本地 parquet hash 作为资产证据。
- `blocker:pipeline_reproduction`：若 R2 目标是复现作者完整两阶段 LLM + RAG + checker + feedback pipeline，则公开代码缺失构成 blocker；若 R2 目标是抽取 STM seed 数据，则不阻塞。
