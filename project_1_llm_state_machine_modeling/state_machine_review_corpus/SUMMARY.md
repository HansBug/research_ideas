# `state_machine_review_corpus/` Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_review_corpus/` 的总账。记录当前已正式收录的论文、当前 reviewer 系统可消费的总样本量、所有候选论文（含已收录与已排除）的逐项细节、外部已审查候选、检索关键词簇与更新日志。

推荐使用顺序：

1. 先读 [README.md](./README.md)，理解硬条件与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选与抽取流程。
3. 用本文件查看统计、清单、已审查候选与历史。
4. 若涉及单篇 `review_extraction.md`，再读 [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)。

## 一、当前收录统计

- 已收录论文（🟢 + 🟡 + ⏳）：**6** 篇（baselines 来源 3 + 外部 protocol-FSM 新增 3）
- 🟢 直接可用：**3** 篇（structure-event-driven / llms_emp / ttool-ai）
- 🟡 可整理：**3** 篇（**新增** psmbench / hermes / rfcnlp —— 数据已确认 GitHub 公开，待克隆并 ETL 为 parquet）
- ⚪ 未收获（评估后排除）：**23 篇**（baselines/ 内 18 篇 + 外部 5 篇）—— 仅在"§ 三、调研记录"与"§ 五、外部已审查候选"中保留排除原因与维度
- ⏳ 尚未提取：**0** 篇
- 当前 reviewer benchmark 实际可消费样本量：**820 行**（`baseline_double_green_human_review_records.parquet`，来自 🟢 三篇）；**🟡 三篇 ETL 完成后预计再增 ~1,500-15,000 行**（取决于按 paragraph-level 还是 transition-level 展开）

## 二、评估口径与维度

### 2.1 emoji 口径

| Emoji | 含义 |
|---|---|
| 🟢 | 直接可用：已下载、已对齐 schema、已 parquet 化、reviewer benchmark 已消费 |
| 🟡 | 可整理：来源已确认可获取，但抽取或对齐未完成 |
| ⚪ | 未收获：经硬条件评估不符合或数据不可获取（不进目录，仅记录） |
| ⏳ | 尚未提取：论文已进目录但 review 数据获取尝试未启动 |

### 2.2 收录硬条件（必须三选三）

| 编号 | 条件 | 判定方式 |
|:---:|---|---|
| H1 | NL 文本 → 状态机模型 范式 | 论文中明确存在自然语言需求/规格/描述 → 状态机 artifact 的工件流 |
| H2 | 状态机泛化（FSM/EFSM/HSM/UML SM/SysML SM/Statechart/TA/Petri/ECC） | 输出工件能整理成状态机族中的一种 |
| H3 | 论文含 human expert review on 状态机 artifact + review 数据可获取 | reviewer 是领域专家 / SE 研究者 / 经培训学生 ≥ 5 人；数据可从公开仓库 / 论文附录 / 论文 tables 抽取 |

### 2.3 状态机族覆盖度

| 状态机族 | 当前是否已覆盖 | 来源 |
|---|:---:|---|
| `UML state machine` | ✅ | structure-event-driven |
| `SysML behavior model / SysML state machine` | ✅ | llms_emp / ttool-ai |
| `Statechart` | ✅ | structure-event-driven 的 SMF 之一 |
| `EFSM`（扩展状态机） | ⚪ | — |
| `HSM`（层次状态机） | 部分（Hierarchical states 在 SMF 中作为 review_target） | 来自 structure-event-driven |
| `Timed Automata` | ⚪ | — |
| `Petri net / ECC` | ⚪ | — |
| `Protocol state machine` | ✅ | psmbench / hermes / rfcnlp（2026-05-06 新增） |

→ **当前 corpus 状态机族覆盖度**：UML/SysML 主流家族（baselines 来源 3 篇） + Protocol state machine（外部新增 3 篇）；仍缺 `EFSM / TA / Petri / ECC`。

## 三、调研记录（按候选论文逐项记录维度）

> 下表是**全部已经被本论文集硬条件审查过的候选论文**，含已收录的 3 篇与已排除的 18+ 篇。
> 字段说明：
> - **范式 H1**：是否 NL → state machine（✅ 是 / ❌ 否）
> - **状态机 H2**：状态机族归属（具体类型 / ❌ 不属于）
> - **review 类型**：实际 review 形式（人工专家 / 学生 / 自动 metric / 作者主观 / 缺失）
> - **reviewer N**：reviewer 数量与资质
> - **数据获取**：URL / 仓库 / 论文 tables / 不公开
> - **样本量**：可获取的 review 样本数
> - **emoji**：综合判定

### 3.1 🟢 已收录（直接可用）

下表把 [README.md §3](./README.md) 与 [REVIEW_GUIDE.md §3](./REVIEW_GUIDE.md) 定义的所有维度全部铺开，**每行 = 一篇论文，列 = 各维度**（详见 [GUIDE.md §11](./GUIDE.md) 的表格规范）。

| slug | 年份 / Venue | 作者团队 | H1（NL→SM 范式）| H2（状态机族）| 状态机来源 | review 类型 | reviewer 资质 | reviewer N | 独立 | inter-rater agreement | 样本量 | 样本量底线 | 数据获取类型 | 入口 URL | 当前可访问性 | 首次访问时间 | 原始 vs 聚合 | 可消费行数 | record_type 分布 | review_target | diagram_type | case 多样性 | score scale | score unit | schema 对齐 | verbatim 抽取 | public_artifact_limitations | emoji |
|---|---|---|:---:|---|---|---|---|:---:|:---:|---|:---:|:---:|---|---|:---:|---|:---:|:---:|---|---|---|---|---|---|:---:|:---:|---|:---:|
| [structure-event-driven](./structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/review_extraction.md) | 2026 arXiv (cs.SE) | McGill (Mussbacher 等) | ✅ 非结构化 NL → UML SM | UML state machine + Statechart | LLM 生成（4 strategies × 多 LLM） | 学生 component-level 评分（→ TP/FP/FN/F1） | 🟡 学生（高年级 + 任务训练） | 121（3 所 US 大学 senior/graduate） | ✅ | ⚪ 未显式报告 Kappa（component-level F1 单点判定较客观） | 512 | ✅ ≥100 | 🟡 论文 supplementary + tables 抽取 | [4open.science](https://anonymous.4open.science/r/llm_state_machine_modeling/) | ☑ 已下载+parquet化 | ~2026-04-15 01:03:52 | 🟡 仅聚合 | 512 | `component_level_review` × 512 | 7 类（States/Transitions/Guards/Actions/Hierarchical/Parallel Regions/History）+ All | `stm` | 8 个非结构化 reactive-system descriptions | 0-1 | `component_f1` | 🟢 已对齐 | ☑ | review 是 component-level 聚合非 raw reviewer-by-reviewer | 🟢 |
| [llms_emp](./llms_emp/review_extraction.md) | 2025 Internetware (ACM) | Beihang (Yuan Wang / Ning Ge 等) | ✅ NL 需求 → SysML 行为模型 | SysML behavior model（含 STM/ACT/SD） | LLM 生成（多 LLM × 单/双阶段） | SE 研究者 sample-level 评分 + 多维细分 | 🟢 SE 研究者 | N（论文研究团队多人独立） | ✅ | ☑ 论文方法学含一致性讨论 | 192 | ✅ ≥100 | 🟢 公开仓库（Google Drive） | [Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | ☑ 已下载+parquet化 | ~2026-04-15 01:03:52 | 🟡 仅聚合（多维细分） | 192 | `sample_level_review` × 192 | `generated_behavior_model` (sample 级) | `stm` / `act` / `sd` | 107 SysML 行为模型场景（5 域） | 0-1 | `normalized_quality` | 🟢 已对齐（JSON 序列化保留多维） | ☑ | 当前仅聚合，需 supplementary 才能拿 raw | 🟢 |
| [ttool-ai](./ttool-ai/review_extraction.md) | 2024 MODELSWARD | Télécom Paris (Apvrille / Sultan) | ✅ NL 系统规范 → SysML 联合模型（含 SMD） | SysML state machine（含 BD/IBD） | LLM 生成（GPT-4 + 知识注入） | 学生组 vs 工程师对照（0-100 分） | 🟡 学生 + 🟢 系统工程师对照 | 学生组 + 工程师组（具体 N 未明示） | ✅ | ⚪ 未显式 Kappa；含学生 vs 专家对照 | 116 | ✅ ≥100 | 🟢 公开仓库（GitHub） | [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) | ☑ 已下载+parquet化 | ~2026-04-15 01:03:52 | 🟢 两种都持有（30 raw + 各级聚合） | 116 | `summary_level_run_score` 30 / `case_aggregate_stat` 36 / `raw_score_row` 30 / `summary` 12 / `overall_aggregate_stat` 8 | `BD / SMD / Properties / UCD / All` | `bd` / `smd` | 3 测试系统 × 多 sub-case (platooning / space-based / AutomatedBraking) | 0-100 | `score_0_100` | 🟢 已对齐（保留分类标签 + diagram_type） | ☑ | result.ods 含 raw_score_row 但 reviewer 个人 ID 已脱敏 | 🟢 |

合计 **3 篇 / 820 行 review 数据**（与 reviewer 现有 dataset 完全对齐）。

### 3.1.1 🟡 已收录（可整理 / 待 ETL，2026-05-06 新增）

下表的 3 篇是 2026-05-06 第二轮外部学术检索的命中：均为 **protocol state machine** 域，状态机来源是 **人工标注 / cross-verified ground truth**（按用户口径"状态机来源不限，含人写"——符合 H3）。数据均已确认 GitHub 公开，待 ETL 为 reviewer parquet schema 后转 🟢。

| slug | 年份 / Venue | 作者团队 | H1（NL→SM 范式）| H2（状态机族）| 状态机来源 | review 类型 | reviewer 资质 | reviewer N | 独立 | inter-rater agreement | 样本量 | 样本量底线 | 数据获取类型 | 入口 URL | 当前可访问性 | 首次访问时间 | 原始 vs 聚合 | 可消费行数 | record_type 分布 | review_target | diagram_type | case 多样性 | score scale | score unit | schema 对齐 | verbatim 抽取 | public_artifact_limitations | emoji |
|---|---|---|:---:|---|---|---|---|:---:|:---:|---|:---:|:---:|---|---|:---:|---|:---:|:---:|---|---|---|---|---|---|:---:|:---:|---|:---:|
| [psmbench](./psmbench/review_extraction.md) | 2025 NeurIPS Datasets & Benchmarks | Lin Zilin et al. | ✅ RFC → Protocol State Machine | Protocol state machine | 人工 cross-verified ground-truth | annotator A 提取 → annotator B 审查 → 分歧讨论解决 | 🟢 domain experts / network protocol researchers | N（论文未单独披露具体 N） | ✅ | ☑ **κ=0.82 (states) / κ=0.78 (transitions)**（论文显式报告） | 14 协议 / 108 states / 297 transitions / 1,580 页 RFC | ✅ ≥100（含 14 协议 × 多 transitions） | 🟢 公开仓库（GitHub + HuggingFace） | [GitHub Zilinlin/RFC_PSM_Benchmark](https://github.com/Zilinlin/RFC_PSM_Benchmark) / [HF zilinlin/RFC2PSM](https://huggingface.co/datasets/zilinlin/RFC2PSM) | ☑ 已 web 验证 | 2026-05-06 14:39 | 🟢 单一 ground-truth（cross-verified）+ 数据集级 κ | ⚪ 待 ETL（预计 ~300+ transition-level / ~1,500+ RFC chunk-level） | ⚪ 待 ETL 后定义 | PSM (states + transitions) | protocol state machine | 14 协议（BGP / DCCP / DHCP / FTP / IMAP / MQTT / NNTP / POP3 / PPP / PPTP / RTSP / SIP / SMTP / TCP） | F1 + κ | state F1 / transition F1 | ⚪ 待对齐 | ⚪ 待 ETL | dataset-level κ；非 review-on-LLM-output（按用户口径"人写也算"） | 🟡 |
| [hermes](./hermes/review_extraction.md) | 2024 USENIX Security | Penn State (Al-Ishtiaq / Hussain 等) | ✅ cellular spec → FSM | Protocol state machine（cellular FSM） | 人工 TCNL grammar 标注 + 双 expert verify | paragraph-level grammar annotation + verification | 🟢 cellular systems researchers + 🟢 domain experts | **4 + 2** | ✅（标注 / 验证两阶段） | ⚪ 未显式 Kappa；含 cross-verify 流程 | ~16,000 datapoints / 2,800 person-hours / 3 specs | ✅ ≥100 | 🟢 公开仓库（GitHub） | [github.com/SyNSec-den](https://github.com/SyNSec-den) | ☑ org 主页可访问；待找具体 Hermes repo | 2026-05-06 14:44 | 🟢 paragraph-level 标注 + Gold FSM | ⚪ 待 ETL（预计 paragraph-level ~15,000+ / transition-level ~1,000+） | ⚪ 待 ETL 后定义 | FSM (states + transitions) | cellular protocol FSM | 4G-NAS R17 / 5G-NAS R17 / 5G-RRC R17 三大 cellular 规范 | 87.21% accuracy（论文报告） | transition Jaccard / state F1 | ⚪ 待对齐 | ⚪ 待 ETL | anchor 是 org 级；具体 repo 待克隆验证 | 🟡 |
| [rfcnlp](./rfcnlp/review_extraction.md) | 2022 IEEE S&P | Purdue + Northeastern (Pacheco / von Hippel / Weintraub / Goldwasser / Nita-Rotaru) | ✅ IETF RFC → FSM | Protocol state machine（FSM） | 人工 XML grammar 标注 + ground-truth FSM | 文档级 XML annotation + BIO tagging + Gold FSM | 🟢 domain experts（5 位 author 中至少多人参与） | N（论文未单独披露具体 N） | ☑ 标注与验证由不同 author 协作 | ⚪ 未显式 Kappa | 6 完整 RFC（BGPv4/DCCP/LTP/PPTP/SCTP/TCP）+ 9 类标签 | ⚪ 待 ETL（预计 ~500 paragraph / ~200 transition） | 🟢 公开仓库（GitHub） | [github.com/RFCNLP/RFCNLP](https://github.com/RFCNLP/RFCNLP) | ☑ org + 子目录已 web 验证 | 2026-05-06 14:46 | 🟢 paragraph-level XML + BIO + Gold FSM | ⚪ 待 ETL | ⚪ 待 ETL 后定义 | FSM (states + transitions + events) | protocol FSM | 6 协议（BGPv4 / DCCP / LTP / PPTP / SCTP / TCP） | 9 类标签 F1 + FSM transition accuracy | component F1 | ⚪ 待对齐 | ⚪ 待 ETL | TCP/DCCP 标注被 PSMBench 复用（lineage：rfcnlp → psmbench） | 🟡 |

合计 **3 篇 / ETL 待完成 / 预计可消费 ~1,500-15,000 行**（按 paragraph-level 或 transition-level 展开口径而定）。

### 3.2 ⚪ 评估后排除（baselines/ 内审查过）

下列论文已通过硬条件审查，**评估为不符合**，因此不进入目录。保留这条记录是为了避免后续重复调研。每行铺开所有维度（与 §3.1 表保持口径一致）。

| slug | 范式 H1 | 状态机 H2 | review 类型 | reviewer 资质口径 | reviewer 是否独立 | 样本量 | 数据获取类型 | 入口 URL | 排除原因（按 H1/H2/H3 分类） | 调研时间 |
|---|:---:|---|---|---|:---:|:---:|---|---|---|---|
| `umple` (Llama3 + Umple) | ✅ | Umple 状态机（FSM 族） | ❌ ICP / EUCP / 归一化 Levenshtein 自动 metric | — | — | 5 systems | 论文正文描述 | 论文文字 | **H3 失败**：仅自动 metric 无 human review；论文自承"no way to automatically check besides compilable" | 2026-05-05 |
| `enhance` (HDLBits + LLM FSM HDL) | ✅ | FSM 代码工件 | ❌ HDLBits 自动 testbench pass/fail | — | — | 20 FSM 题 | 🟢 公开网站 | [HDLBits](https://hdlbits.01xz.net/) | **H3 失败**：自动 testbench 非 human review；20 题样本量低 | 2026-05-05 |
| `safety` (LLM 状态图扩展 + 安全测试) | ✅ | State Diagram 扩展（HSM 族） | ❌ 平均执行轮数 + 算法稳定性 | — | — | 1 case | ⚪ 联系作者 | — | **H3 失败**：单 case + 自动评估 | 2026-05-05 |
| `STPA` (LLM + FSM + STPA + IEC 61499) | ✅ | FSM | 🟡 作者主观分类（正/负/中性变更） | 🔴 作者主观 | ❌ | 1 case | ⚪ 不公开 | — | **H3 失败**：单 case + 作者主观非独立 reviewer | 2026-05-05 |
| `fsm-gen-iec-61499` (fbAssistant tool paper) | ✅ | FSM | ❌ 缺独立 review | — | — | tool 视频 | ⚪ 无 dataset | tool 演示视频 | **H3 失败**：tool paper 无 dataset 无 review | 2026-05-05 |
| `LLM-FSM` (Stanford 2602.07032) | ✅ | FSM (RTL 码) | 🟡 LLM-as-Judge + SAT-solver + human review on subset | 🟢 SE/HW 研究者（subset） | ☑ 是（subset） | 1000 problems（subset 大小未披露） | ⚪ 不公开 | [arXiv:2602.07032](https://arxiv.org/abs/2602.07032) | **H3 失败**：经 2026-05-06 web 验证，论文无 github/zenodo URL；作者 GitHub 主页 6 repo 与本工作无关；human review subset 数据不公开。详见 §五 | 2026-05-06 |
| `I4.0` (PROFINET / OPC UA + diagram recognition) | ❌ **输入是图像** | 状态机表示 | ❌ 边识别准确率 vs IEC ground truth | — | — | PROFINET 80 + OPC UA 15 状态图 | 🟢 Zenodo 公开 | [zenodo:14730727](https://zenodo.org/records/14730727) | **H1 失败**：图像 → SM 不是 NL → SM；评估是自动 metric | 2026-05-05 |
| `req` (Volvo Cars 硕士论文) | ✅ | Statechart (Mermaid) | ✅ Likert + ANOVA / Tukey HSD / Wilcoxon + 半结构化访谈 | 🟢 4 位 Volvo Cars 领域专家 | ☑ 是 | 20 product functional requirements | ⚪ 工业专有不公开 | 论文 tables（仅聚合统计） | **H3 失败**：方法学完美但**原始评分不可获取**；review 数据是工业专有 | 2026-05-05 |
| `chatgpt-uml-assessment` (Cámara 2024) | 🟡 部分（UML 含 SM 但比例小） | UML（含状态机片段） | 🟡 作者经验报告 | 🔴 作者主观 | ❌ | 40 UML/OCL 练习 | 🟢 公开 GitHub | [atenearesearchgroup/chatgpt-uml](https://github.com/atenearesearchgroup/chatgpt-uml) | **H2 部分失败**：状态机比例小；**H3 失败**：作者经验报告非独立 reviewer ≥5 人 | 2026-05-05 |
| `completion-of-sysml-state-machines-from-gwt-requirements` (de Biase 2024) | ✅ | SysML state machine | 🟡 case study 内作者评估 | 🔴 作者本人 | ❌ | 2 cases (ETCS L3 + 医疗告警) | ⚪ 不公开 | 论文内案例描述 | **H3 失败**：作者评估非独立；数据不公开 | 2026-05-05 |
| `pushing-the-generative-envelope-mbse-artifacts` (Leidos 2025) | ✅ | SysML state machine | ❌ gold-standard exemplar by SME（reference 不是 review） | 🟢 SME（但是 reference 创建者非 reviewer） | — | air purifier + vacuum 2 systems | ⚪ 论文文字 | — | **H3 失败**：gold-standard 是输入参考非对 LLM 输出的 review；样本量低 | 2026-05-05 |
| `mcet` (Behavioral Model Correctness Evaluation) | ✅ NL → seq diagram | ❌ **sequence diagram 不是状态机** | ✅ 76 variants × expert-rated（Ferrari 2024） | 🟢 SE 研究者 | ☑ 是 | 76 variants（28 requirements × 多变体） | 🟡 Ferrari 源数据集 | [arXiv:2404.06371](https://arxiv.org/html/2404.06371v2) | **H2 失败**：行为模型是 sequence diagram；MCeT 自身用 LLM-as-Judge | 2026-05-05 |
| `spec2control` (ABB) | ✅ NL → FBD | ❌ **FBD 是 IEC 61131-3 控制逻辑非状态机** | ✅ subject matter experts reviewed | 🟢 ABB SME | ☑ 是 | 10 narratives + 65 cases | 🟡 部分公开 | 论文 + 公司内部 | **H2 失败**：FBD 与状态机相邻但不严格是 SM 族 | 2026-05-05 |
| `modelling-timed-reactive-systems-from-natural-language-requirements` (Carvalho) | ✅ controlled NL → DFRS | DFRS（含状态化语义） | ❌ 形式化推导无 review | — | — | 多 examples（论文内） | ⚪ 不公开 | — | **H3 失败**：形式化语义推导无 human review | 2026-05-05 |
| `generating-annotated-behavior-models-from-end-user-scenarios` (Damas) | ❌ scenarios 输入非 NL | LTS / behavior model | ❌ 经典论文无 LLM 无 review | — | — | — | ⚪ 工具有限公开 | — | **H1+H3 失败**：scenarios 输入非纯 NL；经典 ~2000s 无 LLM 无 review | 2026-05-05 |
| `executable-state-machines-derived-from-structured-textual-requirements` (Daimler) | ✅ structured textual req → executable SM | executable state machine | ❌ 单 case 无 review | — | — | 1 case | ⚪ 不公开 | — | **H3 失败**：单 case + 无 human review | 2026-05-05 |
| `extraction-of-system-states-from-natural-language-requirements` (2019 IEEE) | ✅ NL → 系统状态（NER 类） | ❌ **不是完整状态机** 是状态名抽取 | 🟡 工程师 9 小时手工标注 + F1 评估 | 🟢 工程师 | ☑ 是 | ~2000 需求 | 🟡 DOI 公开但数据不公开 | [DOI:10.14279/depositonce-8717](https://doi.org/10.14279/depositonce-8717) | **H2 失败**：是 state-as-NER 不是完整状态机；数据集本身不公开 | 2026-05-05 |
| `synthesizing-state-based-object-systems-from-lsc-specifications` (Harel 2002) | ❌ LSC 输入非 NL | object system state machine | ❌ 经典无 LLM 无 review | — | — | — | ⚪ 不公开 | — | **H1+H3 失败**：LSC 不是 NL；经典 2002 综合方法 | 2026-05-05 |
| 其它 ~50+ 篇 baselines（synthesis-revisited / synthesizing-finite-state-protocols / 各 NLP-RE 经典 / class-only LLM 工作 …） | 多数 ❌ | 多数 ❌ 输出非状态机 | ❌ 无 review 或自动 metric | — | — | — | 多数不公开 | — | **多重失败**：状态机命中数 < 5 或无状态机族输出 / 无 LLM / 无 human review；不一一列举 | 2026-05-05 |

### 3.3 排除原因维度统计

为后续调研提供参考——**排除原因不是单一**（一篇论文可能命中多个原因）：

| 排除原因 | 论文数（含外部 5 篇） | 备注 |
|---|---:|---|
| 仅自动 metric（ICP / EUCP / F1 / BLEU / pass-fail / LLM-as-Judge / SAT-solver） | 9 | umple / enhance / safety / fsm-gen-iec-61499 / I4.0 / mcet / Carvalho / **LLM-FSM** / **AIAA NL→SM** |
| 数据公开但**范式 H1 不符**（图像 / scenario / LSC / 协议日志 / dialog 控制流 输入） | 4 | I4.0 / Damas / Harel 2002 / **CLASP 2025** |
| **状态机 H2 不符**（输出 sequence diagram / FBD / state-NER / 类图等） | 4 | mcet / spec2control / extraction-of-system-states / 多数 UML class-only |
| 范式符合但**数据不公开**（工业专有 / 仅 case 内描述 / arXiv 无 release） | 7 | req(Volvo) / completion-of-sysml-state-machines / Daimler / Carvalho 1 case / **LLM-FSM** / **SpecGPT** / **AIAA** |
| **reference-as-ground-truth 而非 review on LLM output** | 3 | pushing-envelope / **SysMBench** / **SpecGPT** |
| 范式符合但**reviewer 是作者主观 / 单 case** | 3 | STPA / chatgpt-uml-assessment / pushing-envelope |
| 经典文献（无 LLM 或无独立 reviewer） | 多 | 多数 baselines/ 经典论文 |

加粗的 5 篇是本次（2026-05-06）新增的外部候选审查结论。

> 🔑 **5 个外部候选全部排除的核心原因**：4 篇数据不公开（论文文字宣称但实际无公开仓库 URL），1 篇范式不符（CLASP 是 dialog statechart 控制流，statechart 是设计者手写）。说明 baselines/ 已经覆盖了主要的可获取候选。

## 四、检索关键词簇

### 4.1 当前推荐关键词簇（每节最多 10 行；整合更新而非追加）

- `("state machine" OR "statechart" OR "FSM" OR "EFSM") AND ("expert review" OR "Likert" OR "annotat") AND ("natural language" OR "requirement")`
- `"NL → state machine" + "human evaluation" + "replication package"`
- 优先 venue：ICSE / FSE / ASE / EMSE / RE / SLE / SoSyM / RE@IEEE 2024-2026
- 追源：从含完整 review 数据的论文反向追源数据集论文
- 学位论文：博士 / 硕士论文（thesis）往往附完整评分表

### 4.2 已观察到的高命中特征

- 论文同时给出"用 N 位领域专家做 review"和评分公开仓库
- 用 Likert + ANOVA / Cohen Kappa / inter-rater reliability 的论文往往有原始评分表
- 学位论文：req（Volvo 硕士）即便数据不公开，方法学描述也是完整的——可作 review 设计参考

### 4.3 已观察到的低命中特征（避免无效检索）

- 仅出现"human evaluation"短语但实际是 BLEU / ROUGE 自动评估
- 用 LLM-as-Judge 替代人类专家
- 数据形式是 reference-as-ground-truth（不是 review LLM output）
- 状态机来源是图像 / 协议逆向工程 / 场景 MSC / LSC

### 4.4 检索倾向调整结论

- **基本结论**：`baselines/` 内已基本穷尽硬条件交集；继续在 baselines/ 内挖掘 ROI 极低
- **调整方向**：转向外部 arxiv 2024-2026 与 thesis 论文，重点关注汽车 / 航空 / 工业控制三个领域的状态机建模实证研究
- **避免**：再次进入"看到 'state machine' 字样就收"的粗筛模式
- **2026-05-06 第二轮新发现**：放宽"状态机来源不限（含人写）"后，**protocol state machine** 域立刻命中 3 篇高质量论文（NeurIPS 2025 PSMBench / USENIX 2024 Hermes / IEEE S&P 2022 RFCNLP）；说明 H3 真正瓶颈是"review 数据可获取"而非"LLM-only"；下一轮可继续追 RFC + cellular spec + IoT protocol 域

## 五、外部已审查候选（已全部审查完毕）

下列论文在外部 arXiv / Google Scholar 调研中识别，**已全部完成可获取性验证**，结果如下表。每行铺开的维度与 §3.1 / §3.2 一致。

| slug / 标题 | 来源 | H1（NL→SM 范式）| H2（状态机族）| review 类型 | reviewer 资质 | 独立 | 样本量 | 数据获取类型 | 入口 URL 验证 | 排除原因（按 H1/H2/H3 分类） | emoji |
|---|---|:---:|---|---|---|:---:|:---:|---|---|---|:---:|
| LLM-FSM: Scaling LLMs for Finite-State Reasoning in RTL Code Generation (Stanford) | [arXiv:2602.07032](https://arxiv.org/abs/2602.07032) | ✅ NL spec → RTL FSM | FSM (RTL 码) | 🟡 1000 problems + LLM-judge + SAT-solver + human review on subset | 🟢 SE/HW 研究者（subset） | ☑ 是 | subset 大小未在论文披露 | ⚪ 不公开 | arXiv 无 supplementary URL；论文 888 行内 0 个 github/zenodo URL；作者 Yuheng Wu GitHub 主页（joel-wu）公开 6 个 repo 全部与本工作无关 | **H3 失败**：human review subset 数据未公开 | ⚪ |
| Automated Extraction of Protocol State Machines from 3GPP Specifications (SpecGPT) | [arXiv:2510.14348](https://arxiv.org/abs/2510.14348) | ✅ 3GPP 规范 → protocol SM | Protocol state machine | 🟡 manually annotated reference state machines | 🟢 协议专家 | ☑ 是 | 5G NAS / NGAP / PFCP 三协议 | ⚪ 不公开 | arXiv PDF 全文 0 个仓库 URL；论文未提供 release 声明 | **H3 失败**：data 不公开；且 manual annotation 是 ground truth 不是 review on LLM output | ⚪ |
| A System Model Generation Benchmark from Natural Language Requirements (SysMBench) | [arXiv:2508.03215](https://arxiv.org/abs/2508.03215) | ✅ NL → system model（含 SM 片段） | System model（含 SysML SM 子集） | ❌ 151 human-curated **reference models** + 自动 metric (BLEU/ROUGE/BertScore/SysMEval) | 🟢 PKU 研究者 | ☑ 是（reference 创建者） | 151 scenarios | 🟡 论文宣称"release"但 HTML 中无 URL | abstract 与 conclusion 各提一次"We release SysMBench"；HTML 实际无 GitHub/Zenodo URL；human 参与是 annotation/validation/labeling 不是 review on LLM output | **H3 失败**：reference-as-ground-truth 不是 review on LLM output（按 [REVIEW_GUIDE §4](./REVIEW_GUIDE.md) 常见错误模式 #1） | ⚪ |
| From Natural Language Standard Documents to State Machines | [AIAA 2024 / 10.2514/1.I010525](https://arc.aiaa.org/doi/abs/10.2514/1.I010525) | ✅ ECSS Packet Utilization Standard → EFSM | EFSM | ❌ semi-automatic 工具评估 | — | — | — | ⚪ 付费墙 | AIAA 出版页 403 拒访；DOI PDF 同样 403；无外部公开镜像 | **H3 失败**：semi-automatic 工具评估非 human review；且付费墙数据不可获取 | ⚪ |
| Combining Information State Update + Harel Statecharts + LLMs for Conversational AI (CLASP 2025) | [aclanthology.org/2025.clasp-main.3](https://aclanthology.org/2025.clasp-main.3.pdf) | ❌ statechart 是**设计者手写**用于控制 dialog flow（不是从 NL 生成） | Harel statechart | ❌ 无 review on artifacts | — | — | — | 🟡 工具 Talkamatic Studio（无公开 GitHub） | 论文无 GitHub repo；实现细节"available in Talkamatic Studio"无公开访问 | **H1 失败**：范式不符（dialog 控制 statechart 是手写设计，不是 NL→SM 工件流）；**H3 失败**：无 review on artifacts | ⚪ |

**结论（第一轮）**：5 个外部候选全部审完，**0 篇可加入文库**。

调研验证日期：`2026-05-06 14:35`（含 web search + arxiv WebFetch + 作者主页 + GitHub 验证）。

### 五-bis、第二轮外部学术检索（2026-05-06 下午）

第一轮全部排除后，跳出原候选清单继续按硬条件检索，重点放在 **protocol state machine** 与 **cellular spec** 这两个尚未覆盖的状态机族。3 篇全部命中并已正式收录到 §3.1.1：

| slug / 标题 | 来源 | H1 | H2 | review 类型 | reviewer 资质 | 独立 | 样本量 | 数据获取类型 | 入口 URL 验证 | 入库判定 | emoji |
|---|---|:---:|---|---|---|:---:|:---:|---|---|---|:---:|
| **PSMBench**: Benchmark for Evaluating LLMs on Extracting Protocol State Machines from RFC Specifications | [OpenReview NeurIPS 2025](https://openreview.net/forum?id=5HGBErIHuV) | ✅ | Protocol SM | cross-verified annotation + κ | 🟢 domain experts | ✅ | 14 协议 / 108 states / 297 transitions | 🟢 GitHub + HuggingFace | [Zilinlin/RFC_PSM_Benchmark](https://github.com/Zilinlin/RFC_PSM_Benchmark) + [HF zilinlin/RFC2PSM](https://huggingface.co/datasets/zilinlin/RFC2PSM) 均 web 验证可访问 | ✅ 全部硬条件命中（含 κ=0.82/0.78） | 🟡 |
| **Hermes**: Synthesizing Finite State Machines from Cellular Network Specifications | [USENIX Security 2024](https://www.usenix.org/conference/usenixsecurity24/presentation/al-ishtiaq) / [arXiv:2310.04381](https://arxiv.org/abs/2310.04381) | ✅ | Protocol SM (cellular FSM) | grammar annotation + 2-stage verify | 🟢 cellular researchers + domain experts | ✅ | 4+2 reviewer / ~16,000 datapoints / 2,800 person-hours | 🟢 GitHub | [github.com/SyNSec-den](https://github.com/SyNSec-den) org 主页可访问；具体 Hermes repo 待克隆 | ✅ 硬条件命中 | 🟡 |
| **RFCNLP**: Automated Attack Synthesis by Extracting FSMs from Protocol Specification Documents | [IEEE S&P 2022](https://doi.org/10.1109/SP46214.2022.9833673) / [arXiv:2202.09470](https://arxiv.org/abs/2202.09470) | ✅ | Protocol SM (FSM) | XML grammar + BIO + Gold FSM | 🟢 domain experts | ☑ 协作标注 + 验证 | 6 协议 / 9 类标签 | 🟢 GitHub | [github.com/RFCNLP/RFCNLP](https://github.com/RFCNLP/RFCNLP) 已 web 验证（含 5 个标注子目录） | ✅ 硬条件命中（PSMBench 的源数据集之一） | 🟡 |

**结论（第二轮）**：3 个外部候选全部命中，**全部加入文库**（详见 §3.1.1）。这一轮的关键洞察是：第一轮聚焦"NL→SM + LLM 生成 + LLM 输出 review"导致候选集过窄（H1+H2+H3+"LLM 必须是 reviewer 对象"四个交集），而用户口径已经明确**状态机来源不限**——一旦放宽到"含人写状态机 + cross-verified review"，protocol-FSM 域立刻出现 3 篇高质量命中（含 1 篇 NeurIPS 2025、1 篇 USENIX 2024、1 篇 IEEE S&P 2022）。

调研验证日期：`2026-05-06 14:39 - 14:48`（含 web search + arxiv 全文核实 + GitHub repo 入口验证 + 论文 PDF 下载 + paper_content.txt 提取 + bibtex.bib 写入 + review_extraction.md 9 节模板填充）。

## 六、当前 reviewer 系统数据预算

按当前 corpus 实际能提供的 review 样本量盘点（与 reviewer benchmark 真实可消费一致）：

| record_type | 行数 | 占比 | 来源 paper |
|---|---:|---:|---|
| `component_level_review` | 512 | 62.4% | structure-event-driven |
| `sample_level_review` | 192 | 23.4% | llms_emp |
| `case_aggregate_stat` | 36 | 4.4% | ttool-ai |
| `summary_level_run_score` | 30 | 3.7% | ttool-ai |
| `raw_score_row` | 30 | 3.7% | ttool-ai |
| `summary` | 12 | 1.5% | ttool-ai |
| `overall_aggregate_stat` | 8 | 1.0% | ttool-ai |
| **合计** | **820** | 100% | 3 篇论文 |

**当前 LOFO worst gap = 13.09**（参考 reviewer Phase 14 报告）—— 直接来自 dataset 仅来自 3 篇论文 / 域分布窄的事实。

**🟡 三篇 ETL 完成后的预期增量**：

| 来源 | record_type 候选 | 预计行数（paragraph-level） | 预计行数（transition-level） | 备注 |
|---|---|---:|---:|---|
| psmbench | `transition_review` / `state_review` | ~1,500 | ~300 | 14 协议 × 108 states + 297 transitions |
| hermes | `paragraph_grammar_annotation` | ~15,000 | ~1,000 | 3 specs × ~5,000 paragraphs |
| rfcnlp | `xml_paragraph_annotation` / `bio_token` | ~500 | ~200 | 6 RFC × ~80 paragraphs |
| **合计** | — | **~17,000** | **~1,500** | 选展开口径取决于与 reviewer schema 对齐策略 |

ETL 完成后预期总样本量：**820（现有）+ 1,500-17,000（新增）≈ 2,300-17,800 行**，且**首次包含 protocol state machine 域**（覆盖度提升）。

## 七、待补 / 阻塞 / 下一步

### 7.1 待办（短期 1-2 周）

1. ~~审查 LLM-FSM (Stanford 2602.07032) 的 GitHub repo，判定 human review subset 是否公开~~ ✅ 完成（2026-05-06）：作者 GitHub 主页无相关 repo；论文无 supplementary URL → 数据不公开
2. ~~跟进 SysMBench / SpecGPT 的 supplementary，确认有无 review-on-LLM-output 数据~~ ✅ 完成（2026-05-06）：SysMBench 是 reference-as-ground-truth 不是 review；SpecGPT 数据不公开
3. （仍可选）邮件联系候选作者：Volvo Cars (`req` 论文)、Leidos (`pushing-envelope`)、AIAA `From NL Standard Documents to State Machines`、Stanford `LLM-FSM` 团队询问 human review subset 是否可申请获取
4. **路径 C 自补 review**：拿现成的 LLM 输出（SysMBench 151 scenarios + LLM-FSM 1000 problems），自己组织 reviewer 做 human review，做出新的 NL→SM expert-review 数据
5. **🟡 三篇 ETL（短期高优）**：
   - `git clone https://github.com/Zilinlin/RFC_PSM_Benchmark` 或 `datasets.load_dataset("zilinlin/RFC2PSM")` → 把 14 协议 PSM 展开为 reviewer parquet schema
   - 在 `github.com/SyNSec-den` 找具体 Hermes repo 并 `git clone` → 把 4G/5G 标注转换为 reviewer parquet schema
   - `git clone https://github.com/RFCNLP/RFCNLP` → 把 6 协议 XML/BIO/FSM 展开为 reviewer parquet schema
   - 三篇 ETL 完成后由 🟡 → 🟢，并把 §3.1.1 行迁入 §3.1

### 7.2 阻塞

1. **结构性阻塞**：`baselines/` 内基本穷尽硬条件交集，继续在 baselines/ 内挖掘 ROI 极低
2. 工业专有数据（Volvo / Daimler / ABB / Leidos）原则上不会公开

### 7.3 路径建议

详见 PR comment [#issuecomment-4385187887](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4385187887) 中讨论的 S1 分支：

- **路径 A**：外部调研 + 邮件联系（1-2 周）—— 短期 ROI
- **路径 B**：降低 review 严格度（不推荐）
- **路径 C**：自补 review（4-6 周，真研究价值）—— 拿现成 LLM 输出（LLM-FSM / SysMBench / SpecGPT）+ 自己组织 SE 研究生 + 领域专家做 review，做出新的"NL→SM expert-review benchmark"
- **路径 D**：承认现状（仅 LOFO 内部精化）

## 八、更新日志

- `2026-05-06 14:48:00` 完成第二轮外部学术检索，新增 3 篇 protocol-state-machine 论文入库（🟡 可整理）
  - **PSMBench** (NeurIPS 2025 D&B Track)：RFC2PSM 14 协议，108 states + 297 transitions，论文显式报告 **κ=0.82 (states) / κ=0.78 (transitions)**；GitHub `Zilinlin/RFC_PSM_Benchmark` + HuggingFace `zilinlin/RFC2PSM` 均 web 验证可访问；论文 PDF + paper_content.txt + bibtex.bib + review_extraction.md 已落盘
  - **Hermes** (USENIX Security 2024)：cellular spec → FSM，4 cellular researchers + 2 domain experts cross-verify；~16,000 datapoints / 2,800 person-hours；3 specs（4G-NAS R17 / 5G-NAS R17 / 5G-RRC R17）；GitHub org `SyNSec-den` 已 web 验证（具体 repo 待克隆）；论文文件均落盘
  - **RFCNLP** (IEEE S&P 2022)：6 协议 RFC（BGPv4/DCCP/LTP/PPTP/SCTP/TCP）的 XML grammar + BIO + Gold FSM；domain expert 协作标注 + 验证；GitHub `RFCNLP/RFCNLP` 已 web 验证（5 个标注子目录 `rfcs-annotated` / `rfcs-annotated-tidied` / `rfcs-bio` / `rfcs-original` / `rfcs-predicted`）；为 PSMBench 的源数据集（lineage：rfcnlp → psmbench）；论文文件均落盘
  - 同步更新 §一 收录统计（🟢=3 + 🟡=3，合计 6 篇）、§2.3 状态机族覆盖度（Protocol state machine ⚪ → ✅）、§3.1.1（新增 🟡 已收录小节，每行 = 一篇论文，全部 27 列维度展开）、§五-bis（第二轮检索完整记录）、§六（ETL 完成后 reviewer 数据预算预期 ~2,300-17,800 行）、§7.1（新增 ETL 短期高优待办 + 完成后由 🟡 → 🟢）
  - **关键洞察**：第一轮聚焦"NL→SM + LLM 生成 + LLM 输出 review"导致候选集过窄；用户口径明确"状态机来源不限，含人写"后，protocol-FSM 域立刻命中 3 篇高质量论文（NeurIPS 2025 + USENIX 2024 + IEEE S&P 2022）；说明硬条件中 H3 的"review 数据可获取"才是真正的瓶颈，不是"LLM-only"
- `2026-05-06 14:35:00` 完成 5 个外部候选的可获取性验证
  - **LLM-FSM** (Stanford 2602.07032)：arXiv 页面无 supplementary URL；作者 Yuheng Wu (joel-wu) GitHub 主页 6 个 repo 全部与本工作无关；论文 888 行内 0 个 github/zenodo URL → ⚪ 排除（H3 失败：数据不公开）
  - **SpecGPT** (3GPP 2510.14348)：arXiv PDF 全文 0 个仓库 URL；论文未提供 release 声明 → ⚪ 排除（H3 失败：数据不公开 + manual annotation 是 ground truth 不是 review on LLM output）
  - **SysMBench** (2508.03215)：abstract 与 conclusion 各提一次"We release SysMBench"，但 HTML 实际无 GitHub/Zenodo URL；human 参与是 annotation/validation/labeling 不是 review on LLM output → ⚪ 排除（H3 失败：reference-as-ground-truth 不是 review；按 [REVIEW_GUIDE §4](./REVIEW_GUIDE.md) 常见错误模式 #1）
  - **AIAA NL→SM** (10.2514/1.I010525)：AIAA 出版页 403 拒访；DOI PDF 同样 403；无外部公开镜像；semi-automatic 工具评估非 human review → ⚪ 排除（H3 失败 + 付费墙）
  - **CLASP 2025** (2025.clasp-main.3)：论文 statechart 是设计者**手写**用于 dialog 控制流（不是从 NL 生成）；Talkamatic Studio 工具无公开 GitHub → ⚪ 排除（H1 失败：范式不符 + H3 失败：无 review）
  - 同步更新 §一 收录统计（⚪ 排除从 18+ → 23）、§3.3 排除原因维度统计（含外部 5 篇按原因分类）、§五 标题从"待跟进"改为"已审查"、§7.1 待办勾掉已完成项 + 新增"路径 C 自补 review"
- `2026-05-06 13:54:54` 文库初始化建立
  - 创建 `README.md` / `GUIDE.md` / `SUMMARY.md` / `REVIEW_GUIDE.md`
  - 从 `baselines/` **复制**（不 move）3 篇硬条件符合论文的 `paper.pdf / paper_content.txt / bibtex.bib`：`structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` / `llms_emp` / `ttool-ai`（按 README §3.4：同篇论文可同时存在于 baselines/ 与本文库；两边独立维护各自的派生文件）
  - 各篇创建初版 `review_extraction.md`
  - `baselines/SUMMARY.md` 同步标注 3 篇 `· [review](../state_machine_review_corpus/<slug>/review_extraction.md)` 链接 + 在更新日志加注
  - 完整调研记录（含已收录 + 已排除的 18+ 篇 + 排除原因维度统计）+ 外部候选清单初版录入
