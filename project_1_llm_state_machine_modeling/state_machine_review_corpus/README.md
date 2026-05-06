# `state_machine_review_corpus/` 论文集 README

## 1. 论文集定位

`project_1_llm_state_machine_modeling/state_machine_review_corpus/` 是 `project_1` 下专门维护"**输入文本 → 状态机模型** 范式下、**含可获取的 human expert review 数据**的论文与 review 数据集"的论文集工作区。

它服务于本研究中 reviewer 子系统（详见 `reproduction/expert_review/`）的训练与评估扩库需求。这里的核心目标，是把"reviewer 系统能用上的真实 human expert review 数据"作为一等资产，逐篇沉淀其论文、获取入口、原始评分表（或可推断的等价数据）和 review schema 对齐说明。

本论文集与 [baselines/](../baselines) 的关键区别：

1. **`baselines/`** 收录的是"LLM 状态机建模 baseline 论文"，关心的是**方法本身**（输入/输出/提示工程/反馈链路/验证方式）。
2. **本论文集**收录的是"**可作为 reviewer 训练/评估数据来源**"的论文与配套 review 数据。同一篇论文如果既是 baseline 又有可获取 review，会同时出现在两个文库中（保留 paper.pdf / paper_content.txt / bibtex.bib，但 review 抽取相关派生文件只在本文库中维护）。

## 2. 设立宗旨与期望收获

单独建立本论文集，主要为了沉淀以下几类内容：

1. 严格符合 `NL → state machine + 论文中含 human expert review on 状态机artifact + review 结果可获取` 三条硬条件的论文清单。
2. 每篇论文配套的 `review_extraction.md`：明确该篇 review 数据的规模、字段、获取途径、对齐到统一 schema 的方式。
3. 跨论文的 review 数据 schema 一致性记录：评分尺度（Likert / continuous / pass-fail / F1）、维度（correctness / completeness / readability / equivalence …）、reviewer 资质（domain expert / SE researcher / student）等。
4. 当前 dataset 实际能为 reviewer 系统提供多少可学/可评测样本的**真实盘点**，避免论文宣称与可用数据脱节。

本论文集希望最终回答三类问题：

1. 哪些论文真正提供了"对状态机 artifact 的 human expert review"原始数据，且可获取？
2. 这些 review 的尺度、维度、reviewer 资质是否可对齐到统一 schema？
3. 当前 corpus 整体能为 reviewer 系统提供的 review 样本量、样本来源 paper 数、artifact 类型覆盖度是多少？

## 3. 收录范围

### 3.1 三条硬条件（同时满足才正式收录为 🟢 `直接可用`）

1. **范式**：论文中存在 `输入文本（自然语言需求/规格/描述）→ 状态机模型` 的工件流。
2. **状态机泛化**：泛 state machine 即可——`FSM / EFSM / HSM / Statechart / SysML state machine / UML state machine / Protocol state machine / Timed Automata / ECC / Petri net 等可整理成状态机族的形式` 都接受。具体边界以本仓库 [`sources/STM_GUIDE.md`](../sources/STM_GUIDE.md) 的 STM 类型为准。
3. **review 数据**：
   - 论文中**有 human expert（领域专家 / SE 研究者 / 经验丰富的工程师）对状态机 artifact 的 review**——artifact 来源不限（LLM 生成 / 工具生成 / 人写都可）。
   - **review 数据可获取**——任意一种渠道：仓库公开（GitHub / Zenodo / OSF / Figshare）/ 论文附录 / 原始评分表 / 论文表格中可抽取的等价数据。

### 3.2 优先收录

1. 同时满足上述三条硬条件，且 review 数据已经公开（≥ 100 条）的论文。
2. 同时满足三条硬条件，但 review 数据需要从论文 tables / supplementary 抽取的论文，附 `review_extraction.md` 写清抽取后规模与字段。
3. 边缘情况：满足前两条但 review 渠道是"作者邮件可索取"——只有在已经联系作者并得到积极回应后才升级到正式收录。

### 3.3 不收录

1. 经典非 LLM 状态机合成论文（Damas / Harel / Whittle 等），即使有数据集，也因为没有 expert review 不在范围。
2. 用 ICP / EUCP / F1 / BLEU / pass-fail 等纯自动 metric 评估的论文（如 Umple Llama3、HDLBits LLM-FSM、SysMBench、SpecGPT），即使数据公开。
3. 状态机来源是图像 / scenario MSC / LSC / 协议逆向工程的论文（输入不是 NL）。
4. 输出不是状态机的论文（class diagram / sequence diagram / goal model / domain model），即使含 expert review。
5. 单 case study 作者主观评估（非独立 reviewer）的论文。

### 3.4 与 `baselines/` 的关系

- 一篇论文同时进入 `baselines/` 和 `state_machine_review_corpus/` 是被允许的——前者从"baseline 方法对比"角度，后者从"review 数据资产"角度。
- 同一篇论文的 `paper.pdf / paper_content.txt / bibtex.bib` 在两个文库中**可同时存在**（不强制软链接，避免历史可追溯性问题；但更新时两边需同步）。
- 单篇分析文件区分：`baselines/<slug>/DESC.md` 关心方法对照；`state_machine_review_corpus/<slug>/review_extraction.md` 关心 review 数据。

## 4. 纳入与排除判定标准

后续判断一篇论文是否进入本论文集时，至少从以下维度执行：

1. **输入输出范式**
   - 纳入：明确的 `NL 文本 → 状态机模型` 工件流。
   - 排除：图像 / 协议日志 / 场景 MSC / 已有形式化模型 作为输入。
2. **状态机族**
   - 纳入：FSM / EFSM / HSM / UML state machine / SysML state machine / Statechart / Timed Automata / Petri net 等。
   - 排除：序列图 / 类图 / 目标图 / 用例图 / 数据流图，即使含状态语义片段。
3. **review 主体**
   - 纳入：领域专家 / 经验丰富的 SE 研究者 / 经过结构化训练的工程师 / 高年级 SE 学生（≥ 5 人）。
   - 降优先级：仅作者本人主观评估。
   - 排除：纯自动 metric / 单 case study 个人评估。
4. **review 数据可获取性**
   - 纳入：公开仓库 / 论文附录 / 论文 tables 可抽取 / 作者已确认可索取。
   - 排除：仅论文中聚合统计（无原始评分）+ 数据持有者拒绝公开。
5. **样本量底线**
   - 优先收录：≥ 100 条 review 样本。
   - 可收录：50-100 条，附明确补充计划。
   - 谨慎收录：< 50 条，需要在 [SUMMARY.md](./SUMMARY.md) 中说明用途。

## 5. 本论文集下文件说明

本论文集默认包含以下核心文件：

1. [README.md](./README.md)
   - 入口说明文件。
2. [GUIDE.md](./GUIDE.md)
   - AI 工作操作规范。
3. [SUMMARY.md](./SUMMARY.md)
   - 总账：当前收录、待补、外部候选、关键词簇、更新日志。
4. [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)
   - 单篇 `review_extraction.md` 的专项规范。

AI 推荐阅读顺序如下：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)（当任务涉及单篇 `review_extraction.md`）
5. 目标论文目录下的 `bibtex.bib`
6. 目标论文目录下的 `paper_content.txt`
7. 必要时回到 `paper.pdf`

## 6. 单论文路径约束

本论文集下每个单论文目录默认至少应包含：

1. `paper.pdf`
2. `paper_content.txt`（必须由 `tools/pdf_extractor.py` 生成）
3. `bibtex.bib`
4. `review_extraction.md`（**本论文集核心派生文件**，必须遵循 [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)）

可选：

5. `desc.md`：若该论文同时是 baseline，可以从 `baselines/<slug>/DESC.md` 复制或软链接。
6. `data/`：本地落盘的 review 原始数据（如 csv / parquet / json），优先放未经修改的源文件。

## 7. AI 工作入口提示

进入本论文集时，默认按以下方式工作：

1. 先读 [README.md](./README.md)，确认硬条件三选三。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、抽取、回填流程。
3. 再读 [SUMMARY.md](./SUMMARY.md)，掌握当前收录、待补候选、外部候选状态。
4. 若需要创建或重写单篇 `review_extraction.md`，必须再读 [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)。
5. 进入单论文目录后，严格按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时）-> review_extraction.md` 的顺序处理。
6. 完成后必须回写 [SUMMARY.md](./SUMMARY.md)，不允许只在论文目录里留下未入账条目。

## 8. 后续 AI 应优先做什么、避免做什么

优先做：

1. 优先确认每篇候选的 review 数据是否真的可获取（不只看论文文字声称，要真的尝试访问仓库 / 抽取数据）。
2. 推动外部候选（SysMBench / SpecGPT / LLM-FSM / Volvo 等）的 review 数据实际入库。
3. 维护 [SUMMARY.md](./SUMMARY.md) 中"当前 reviewer 系统可消费的总样本量"实时统计。

避免做：

1. 只看论文标题或摘要就把"看起来含 human review"的论文收进来。
2. 把 ICP / EUCP / F1 / BLEU / 自动 metric 当成 human review 收录。
3. 把 reference-as-ground-truth（如 SysMBench 的 151 个 human-curated reference models）等同于 expert review。
4. 漏写"review 数据获取尝试结果"——即使作者邮件未回信，也要在 [SUMMARY.md](./SUMMARY.md) 中记录。
