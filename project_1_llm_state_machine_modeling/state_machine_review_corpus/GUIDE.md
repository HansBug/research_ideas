# `state_machine_review_corpus/` AI 工作 GUIDE

本文件规定本论文集的 AI 自动工作流程：检索、筛选、整理、review 数据抽取、SUMMARY 回填、与 `baselines/` 的协同。

## 1. 论文集目标与边界

### 1.1 服务对象

本论文集服务于 reviewer 系统（`reproduction/expert_review/`）的训练 / 评估 / 泛化数据需求。它**不**服务于：

1. baseline 方法对照（这是 `baselines/` 的任务）。
2. 控制系统真实样本采集（这是 `sources/` 的任务）。
3. 一般综述与背景文献（这是 `discussions/` 的任务）。

### 1.2 不做的事

1. **不重复造方法分析**：单篇论文的"输入/输出/方法/实验/局限性"分析在 `baselines/<slug>/DESC.md` 中已经存在的，本文库的 `review_extraction.md` 不重复，仅用一句话引用。
2. **不收录无 review 数据的论文**——即便它在状态机方法学上很有价值。
3. **不把 reference / ground truth 当 review**——重点见 [README §3.3](./README.md#33-不收录)。

## 2. 检索策略

### 2.1 推荐入口

1. **优先扫 `baselines/`**：本论文集大量候选已经在 `baselines/` 下有 paper.pdf。先用本仓库内部 grep 扫"含 LLM + 含状态机字 + 含 human/expert review 字"的命中。
2. **外部 arxiv / Google Scholar**：用关键词组合搜索：
   - `("state machine" OR "statechart" OR "FSM" OR "EFSM") AND ("human evaluat" OR "expert review" OR "rated by" OR "Likert" OR "annotat") AND ("natural language" OR "requirement")`
   - 加 `2024..2026` 时间过滤，重点查 ICSE / FSE / ASE / EMSE / RE / SLE / SoSyM。
3. **追源**：若一篇候选论文的 review 数据来自更早的源数据集（例如 Ferrari 2024 的 NL2SD bench），追到源头并独立评估。

### 2.2 高命中模式

1. 论文同时给出"用 N 位领域专家做 review"和"评分公开在某仓库 / 附录"。
2. 论文用 Likert 量表 + ANOVA / Kappa / Inter-rater 等统计 → 有原始评分表的可能性高。
3. 论文是博士 / 硕士论文（thesis）：往往附完整评分表。

### 2.3 低命中模式（避免无效检索）

1. 仅出现"human evaluation"短语但实际是用 BLEU / ROUGE 自动评估的论文。
2. 用 LLM-as-Judge 替代人类专家的论文（这不是 human expert review）。
3. 有 reference 但用 reference 做 ground truth 不是 review LLM output 的论文。

## 3. 筛选标准

### 3.1 收录硬条件

参见 [README §3.1](./README.md#31-三条硬条件同时满足才正式收录为--直接可用)：

1. NL → state machine 范式
2. 状态机泛化（FSM/EFSM/HSM/UML SM/SysML SM/Statechart/TA/Petri/ECC）
3. review 数据可获取

### 3.2 降优先级

1. review 是作者主观（非独立 reviewer）。
2. review 数据需要邮件索取（先收邮件回复后再升级）。
3. 样本量 < 50。

### 3.3 排除（即使候选含状态机 + LLM）

1. 用纯自动 metric 评估（ICP / EUCP / F1 / BLEU / pass-fail）。
2. review 数据明确不公开且作者拒绝。
3. 状态机来源是图像 / 协议逆向工程 / 场景 MSC / LSC。

### 3.4 去重规则

1. 优先按 DOI 去重。
2. DOI 缺失时按标准化标题去重。
3. 工业专有版本与学术发布版本视为同一篇（合并为一个目录，在 `review_extraction.md` 中说明）。

## 4. 目录与文件标准

### 4.1 单论文目录必备文件

```
<slug>/
├── paper.pdf
├── paper_content.txt
├── bibtex.bib
└── review_extraction.md   ← 本论文集核心派生文件
```

可选：

```
<slug>/
├── data/                  ← 本地 review 原始数据（csv/parquet/json）
└── desc.md                ← 复制或软链 baselines/<slug>/DESC.md
```

### 4.2 review_extraction.md 必备字段

详见 [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)。最低要求是该文件能让读者 5 分钟内回答：

1. review 是谁做的（reviewer 数量 + 资质）？
2. review 了多少 artifact，每条评分维度有哪些？
3. 数据从哪取（URL / 仓库 / 论文 tables）？
4. 是否已映射到 reviewer 系统的统一 schema？

### 4.3 paper_content.txt

必须用 `tools/pdf_extractor.py` 生成；若 text 模式提取异常立即切到 ocr 模式。

## 5. 内容整理策略

### 5.1 单篇 `review_extraction.md` 中应记录

1. **review 数据来源**：URL / 仓库 / 论文表格位置。
2. **数据规模**：artifact 数 × reviewer 数 × 维度数。
3. **schema 字段**：每条 review 的字段名、取值范围、是否聚合后才公开。
4. **对齐到 reviewer 统一 schema 的方法**：每个本篇字段映射到 `expert_review` 的哪个 score 字段。
5. **Replication 验证**：是否自行下载并打开过原始数据；若否，原因。
6. **质量 emoji**：🟢 直接可用 / 🟡 可整理 / ⚪ 未收获 / ⏳ 尚未提取。

### 5.2 不进 `review_extraction.md` 的内容

1. 论文方法的输入/输出/算法描述（属于 `baselines/<slug>/DESC.md`）。
2. 论文的实验结论与作者讨论。
3. 与 review 数据无关的附属图表。

## 6. SUMMARY.md 撰写规范

### 6.1 必备章节

详见 [SUMMARY.md](./SUMMARY.md) 现有结构。每轮维护必须更新：

1. **当前收录统计**：🟢/🟡/⚪/⏳ 四档计数。
2. **总 review 样本量**：所有 🟢 论文的样本量加和（用于 reviewer 系统数据预算）。
3. **状态机类型覆盖**：当前 corpus 覆盖了哪几类（FSM / EFSM / HSM / UML SM / SysML SM / Statechart / TA / Petri / ECC）。
4. **关键词簇**：当前最有效的检索关键词簇 + 应避免的低命中模式。
5. **正式论文清单**：含年份 / 主题 / review 数据获取方式 / 样本量 / 状态。
6. **外部已审查候选**：未在 baselines/ 内但已在外部调研中识别的候选；含已审查完成（标 ⚪ 排除）与待审查（标 🟡 待跟进）两类。
7. **更新日志**：使用 `yyyy-mm-dd hh:mm:ss` 时间戳。

### 6.2 长度约束

按 CLAUDE.md `2.5 GUIDE.md 规范` 默认值：

1. 关键词簇相关小节每节最多 10 行，**采用压缩式整合更新**——不允许逐轮机械追加。
2. 正式论文清单按年份升序排列。
3. 失败记录保留历史不删。

## 7. 工作流程

一轮完整工作的推荐顺序：

1. **状态盘点**：先读 [SUMMARY.md](./SUMMARY.md)，了解当前 🟢/🟡 论文及待补任务。
2. **补历史欠账**：先把 ⏳ 转为 🟢 / 🟡 / ⚪ 之一，再做新检索。
3. **新检索**：按 [§2.1](#21-推荐入口) 顺序——baselines/ 内部扫 → 外部 arxiv → 追源。
4. **候选评估**：每个候选用 [§3.1](#31-收录硬条件) 三条硬条件硬过；不通过的标 ⚪ 留记录。
5. **正式收录**：通过的论文 git mv 进 corpus；写 `review_extraction.md`。
6. **回写 SUMMARY**：更新统计、清单、关键词簇、外部已审查候选、更新日志。
7. **一致性检查**：四档计数 = 总样本量加和 = 论文清单条数；时间戳 yyyy-mm-dd hh:mm:ss。

## 8. 质量与可追溯性

1. 每条 review 数据的来源必须能回溯到论文 + URL/页码。
2. 自行抽取的数据要在 `review_extraction.md` 中说明抽取方法 + 是否经过双人核对。
3. 若论文文字宣称数据公开但实际仓库 404 / 文件缺失，记为 ⚪ 并写明原因。

## 9. 与 `baselines/` 的协同

### 9.1 一篇论文同时进两库

1. 在 `baselines/<slug>/DESC.md` 中加一行 `> 本篇同时进入 [state_machine_review_corpus/<slug>](../../state_machine_review_corpus/<slug>/review_extraction.md)`
2. 在 `state_machine_review_corpus/<slug>/review_extraction.md` 顶部加 `> 本篇方法分析见 [baselines/<slug>/DESC.md](../../baselines/<slug>/DESC.md)`
3. 不强制软链 paper.pdf，避免历史 git mv 引起的链接断裂。

### 9.2 同步更新

1. `baselines/SUMMARY.md` 中含本论文集已收论文的，应在该论文条目末尾标注 `(also in state_machine_review_corpus)`。
2. 删除一边时不强制删另一边——但需在 SUMMARY.md 中说明原因。

## 10. SUMMARY.md 表格规范（硬约束）

### 10.1 行 / 列约定

`SUMMARY.md` 中所有正式总账表格、调研记录表、外部已审查/待跟进表，**必须遵守"每行 = 一篇论文，列 = 各维度"的横向布局**。

不允许做的事：

1. ❌ 不允许把"维度"放到行、"论文"放到列（即转置过来），即使列数会比较多
2. ❌ 不允许在表格中用一行同时塞多篇论文（即一行多论文聚合）
3. ❌ 不允许只列 emoji 综合判定而不展开维度——必须把 [README §3](./README.md) 与 [REVIEW_GUIDE §3](./REVIEW_GUIDE.md) 定义的所有维度作为列，缺失字段记 ⚪ 不留空

### 10.2 列必备维度（按当前判定口径）

每篇论文一行至少包含以下维度作为列（顺序参考 §3.1 已落实的样例）：

1. `slug`（含相对链接）
2. `年份 / Venue`
3. `作者团队`
4. `H1（NL→SM 范式）`
5. `H2（状态机族）`
6. `状态机来源`（LLM / tool / 人写）
7. `review 类型`
8. `reviewer 资质`（按 [REVIEW_GUIDE §3.1](./REVIEW_GUIDE.md) 口径）
9. `reviewer N`（人数 + 来源）
10. `独立`（是否非作者本人）
11. `inter-rater agreement`
12. `样本量`
13. `样本量底线`（≥100 / 50-100 / <50）
14. `数据获取类型`（按 [REVIEW_GUIDE §3.2](./REVIEW_GUIDE.md) 口径）
15. `入口 URL`
16. `当前可访问性`
17. `首次访问时间`
18. `原始 vs 聚合`
19. `可消费行数`（已 parquet 化的 record 数）
20. `record_type 分布`
21. `review_target`
22. `diagram_type`
23. `case 多样性`
24. `score scale` / `score unit`
25. `schema 对齐`（到 reviewer 系统）
26. `verbatim 抽取`（是否已存 paper_method_verbatim_excerpt）
27. `public_artifact_limitations`
28. `emoji`（综合判定）

`§3.2 已排除` 表与 `§五 外部已审查候选` 表的列可以是 §3.1 的子集（必要时省略不可填的列），但**仍须保持"行=文献"的方向**。

### 10.3 例外

只有"分类汇总统计"类表格（如 §3.3 排除原因维度统计、§六 record_type 分布统计、§2.3 状态机族覆盖度）可以不按"行=文献"——这些是按其它分类轴汇总的。**判断标准**：表的主键是不是论文 slug；如果是，必须是行；如果不是，可以自由排版。

## 11. 默认值（若本 GUIDE 无明确 override，按 CLAUDE.md 总规范）

1. 关键词簇每小节最多 10 行（整合更新而非追加）。
2. 失败重试默认窗口 5 天。
3. 批量规模默认下限：每轮筛查 ≥ 20 篇，最终入库 ≥ 10 篇——本论文集硬条件极严，**允许 override**：每轮入库 ≥ 1 篇也算成功。
4. 去重：DOI > 标准化标题 > 作者+年份+venue。
5. 时间格式：`yyyy-mm-dd hh:mm:ss`。
