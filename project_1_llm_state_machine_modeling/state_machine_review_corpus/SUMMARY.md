# `state_machine_review_corpus/` Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_review_corpus/` 的总账。记录当前已正式收录的论文、当前 reviewer 系统可消费的总样本量、所有候选论文（含已收录与已排除）的逐项细节、外部待跟进候选、检索关键词簇与更新日志。

推荐使用顺序：

1. 先读 [README.md](./README.md)，理解硬条件与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选与抽取流程。
3. 用本文件查看统计、清单、待跟进与历史。
4. 若涉及单篇 `review_extraction.md`，再读 [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)。

## 一、当前收录统计

- 已收录论文（🟢 + 🟡 + ⏳）：**3** 篇
- 🟢 直接可用：**3** 篇
- 🟡 可整理：**0** 篇
- ⚪ 未收获（评估后排除）：**18+** 篇（不进目录，仅在"§ 三、调研记录"中保留排除原因与维度）
- ⏳ 尚未提取：**0** 篇
- 当前 reviewer benchmark 实际可消费样本量：**820 行**（`baseline_double_green_human_review_records.parquet`）

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
| `Protocol state machine` | ⚪ | — |

→ **当前 corpus 状态机族覆盖度低**：仅 UML/SysML 主流家族；扩库时优先补 `EFSM / TA / Protocol SM`。

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

### 3.2 ⚪ 评估后排除（baselines/ 内审查过）

下列论文已通过硬条件审查，**评估为不符合**，因此不进入目录。保留这条记录是为了避免后续重复调研。每行铺开所有维度（与 §3.1 表保持口径一致）。

| slug | 范式 H1 | 状态机 H2 | review 类型 | reviewer 资质口径 | reviewer 是否独立 | 样本量 | 数据获取类型 | 入口 URL | 排除原因（按 H1/H2/H3 分类） | 调研时间 |
|---|:---:|---|---|---|:---:|:---:|---|---|---|---|
| `umple` (Llama3 + Umple) | ✅ | Umple 状态机（FSM 族） | ❌ ICP / EUCP / 归一化 Levenshtein 自动 metric | — | — | 5 systems | 论文正文描述 | 论文文字 | **H3 失败**：仅自动 metric 无 human review；论文自承"no way to automatically check besides compilable" | 2026-05-05 |
| `enhance` (HDLBits + LLM FSM HDL) | ✅ | FSM 代码工件 | ❌ HDLBits 自动 testbench pass/fail | — | — | 20 FSM 题 | 🟢 公开网站 | [HDLBits](https://hdlbits.01xz.net/) | **H3 失败**：自动 testbench 非 human review；20 题样本量低 | 2026-05-05 |
| `safety` (LLM 状态图扩展 + 安全测试) | ✅ | State Diagram 扩展（HSM 族） | ❌ 平均执行轮数 + 算法稳定性 | — | — | 1 case | ⚪ 联系作者 | — | **H3 失败**：单 case + 自动评估 | 2026-05-05 |
| `STPA` (LLM + FSM + STPA + IEC 61499) | ✅ | FSM | 🟡 作者主观分类（正/负/中性变更） | 🔴 作者主观 | ❌ | 1 case | ⚪ 不公开 | — | **H3 失败**：单 case + 作者主观非独立 reviewer | 2026-05-05 |
| `fsm-gen-iec-61499` (fbAssistant tool paper) | ✅ | FSM | ❌ 缺独立 review | — | — | tool 视频 | ⚪ 无 dataset | tool 演示视频 | **H3 失败**：tool paper 无 dataset 无 review | 2026-05-05 |
| `LLM-FSM` (Stanford 2602.07032) | ✅ | FSM (RTL 码) | 🟡 LLM-as-Judge + SAT-solver + human review on subset | 🟢 SE/HW 研究者（subset） | ☑ 是（subset） | 1000 problems（subset 待查） | 🟡 待查 GitHub | [arXiv:2602.07032](https://arxiv.org/abs/2602.07032) | **H3 部分通过**：LLM-judge + SAT 不算；human review on subset 待确认公开度 → 升级到 §五 外部候选 | 2026-05-06 |
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

为后续调研提供参考——**排除原因不是单一**：

| 排除原因 | 论文数 | 备注 |
|---|---:|---|
| 仅自动 metric（ICP / EUCP / F1 / BLEU / pass-fail / LLM-as-Judge） | 7 | umple / enhance / safety / fsm-gen-iec-61499 / I4.0 / mcet / Carvalho |
| 数据公开但**范式 H1 不符**（图像 / scenario / LSC / 协议日志 输入） | 3 | I4.0 / Damas / Harel 2002 |
| **状态机 H2 不符**（输出 sequence diagram / FBD / state-NER / 类图等） | 4 | mcet / spec2control / extraction-of-system-states / 多数 UML class-only |
| 范式符合但**数据不公开**（工业专有 / 仅 case 内描述） | 4 | req(Volvo) / completion-of-sysml-state-machines / Daimler / Carvalho 1 case |
| 范式符合但**reviewer 是作者主观 / 单 case** | 3 | STPA / chatgpt-uml-assessment / pushing-envelope |
| 经典文献（无 LLM 或无独立 reviewer） | 多 | 多数 baselines/ 经典论文 |

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

## 五、外部待跟进候选

下列论文在外部 arXiv / Google Scholar 调研中识别，需要进一步验证 review 数据可获取性。每行铺开的维度与 §3.1 / §3.2 一致。

| 候选 | 来源 | 范式 H1 | 状态机 H2 | review 类型 | reviewer 资质 | reviewer 是否独立 | 样本量 | 数据获取类型 | 待跟进任务 | 当前 emoji |
|---|---|:---:|---|---|---|:---:|:---:|---|---|:---:|
| LLM-FSM: Scaling LLMs for Finite-State Reasoning in RTL Code Generation (Stanford) | [arXiv:2602.07032](https://arxiv.org/abs/2602.07032) | ✅ NL spec → RTL FSM | FSM (RTL 码) | 🟡 1000 problems + LLM-judge + SAT-solver + **human review on subset** | 🟢 SE/HW 研究者（subset） | ☑ 是 | subset 待查 | 🟡 待查 GitHub repo | 查 replication package；判定 subset 公开度与样本量 | 🟡 |
| Automated Extraction of Protocol State Machines from 3GPP Specifications (SpecGPT) | [arXiv:2510.14348](https://arxiv.org/abs/2510.14348) | ✅ 3GPP 规范 → protocol SM | Protocol state machine | 🟡 manually annotated reference state machines | 🟢 协议专家 | ☑ 是 | 5G NAS / NGAP / PFCP 三协议 | 🟡 待查 supplementary | 评估"manual annotation as reference"是否算 expert review；查 supplementary | 🟡 |
| A System Model Generation Benchmark from Natural Language Requirements (SysMBench) | [arXiv:2508.03215](https://arxiv.org/abs/2508.03215) | ✅ NL → system model（含 SM 片段） | System model（含 SysML SM 子集） | 🟡 151 human-curated reference models + SysMEval（语义 metric） | 🟢 PKU 研究者 | ☑ 是 | 151 scenarios | 🟡 待查 GitHub | 抽取 SM 子集；判定 reference vs review；评估是否含 human review on LLM output | 🟡 |
| From Natural Language Standard Documents to State Machines | [AIAA 2024](https://arc.aiaa.org/doi/abs/10.2514/1.I010525) | ✅ aviation NL spec → SM | State machine | 🟡 工业实验 | 待查 | 待查 | 待查 | ⚪ 不公开 | 邮件联系作者询问 review 数据 | 🔴 阻塞 |
| Combining Information State Update + Harel Statecharts (CLASP 2025) | [aclanthology.org/2025.clasp-main.3](https://aclanthology.org/2025.clasp-main.3.pdf) | ✅ NL dialog → Harel statechart | Harel statechart | 待细查 | 待查 | 待查 | 待查 | 待查 | 通读论文判定 review 形式 | 🟡 |

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

## 七、待补 / 阻塞 / 下一步

### 7.1 待办（短期 1-2 周）

1. 审查 LLM-FSM (Stanford 2602.07032) 的 GitHub repo，判定 human review subset 是否公开
2. 跟进 SysMBench / SpecGPT 的 supplementary，确认有无 review-on-LLM-output 数据
3. 邮件联系候选作者：Volvo Cars (`req` 论文)、Leidos (`pushing-envelope`)、AIAA `From NL Standard Documents to State Machines`

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

- `2026-05-06 13:54:54` 文库初始化建立
  - 创建 `README.md` / `GUIDE.md` / `SUMMARY.md` / `REVIEW_GUIDE.md`
  - 从 `baselines/` **复制**（不 move）3 篇硬条件符合论文的 `paper.pdf / paper_content.txt / bibtex.bib`：`structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` / `llms_emp` / `ttool-ai`（按 README §3.4：同篇论文可同时存在于 baselines/ 与本文库；两边独立维护各自的派生文件）
  - 各篇创建初版 `review_extraction.md`
  - `baselines/SUMMARY.md` 同步标注 3 篇 `· [review](../state_machine_review_corpus/<slug>/review_extraction.md)` 链接 + 在更新日志加注
  - 完整调研记录（含已收录 + 已排除的 18+ 篇 + 排除原因维度统计）+ 外部候选清单初版录入
