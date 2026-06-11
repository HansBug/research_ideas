# #85 综述 baseline 文库维护指南

## 1. 目标

本 GUIDE 约束 #85 P0/P1 相关工作的全文级 baseline 调研。目标不是简单保存 PDF，而是让每篇 baseline 论文都形成一条可追溯证据链：

`paper.pdf -> paper_content.txt -> bibtex.bib -> fulltext_review.md -> fulltext_review_matrix.csv -> SUMMARY.md -> #85 claim/evidence map`

最终产物必须能回答：这篇论文到底与 #85 的“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”有多接近、能支撑哪类 Related Work 叙事、是否挑战新颖性、哪些证据还不够。

## 2. 单论文目录标准

每篇论文一个目录，目录名使用稳定英文 slug。每个单论文目录至少包含：

| 文件 | 是否必需 | 生成 / 维护规则 |
|---|---|---|
| `paper.pdf` | 必需 | 保存论文 PDF 原文；文件名固定为 `paper.pdf` |
| `paper_content.txt` | 必需 | 必须由 `tools/pdf_extractor.py` 从 `paper.pdf` 生成；text 异常时切 OCR |
| `bibtex.bib` | 必需 | DOI、title、author、year、venue、url 尽量完整 |
| `fulltext_review.md` | 必需 | 全文级证据链、D1--D7 评分、页码定位、短引文、可写 / 不可写声明 |

推荐命令：

```bash
source venv/bin/activate
python -m tools.pdf_extractor -i path/to/paper.pdf -o path/to/paper_content.txt -m text
```

若 `paper_content.txt` 出现乱码、大量缺页、页码错乱或可抽取字符极少，应改用 OCR 并在 `fulltext_review.md` 与 receipt 中记录。

### 2.1 四件套硬规则

1. **不允许 metadata-only 条目混入本全文文库**：进入本文库的论文必须同时具备 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md` 四件套；缺任一文件时只能停留在上游 [../baselines/](../baselines/) 的初筛 / 下载交接层。
2. **`paper_content.txt` 必须可复现生成**：默认使用仓库根目录的 `tools.pdf_extractor.py`；`fulltext_review.md` 与 [data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv) 必须记录抽取方式、页数 / 可抽取页数、短哈希与异常。
3. **PDF 与抽取文本是本地研究证据链，不是对外引用文本**：PR comment、论文正文和 issue comment 只允许使用短引文、页码定位和中文转述，不得粘贴长段原文。
4. **SUMMARY 必须可跳转**：每篇论文在 [SUMMARY.md](./SUMMARY.md) 中必须同时提供到 `fulltext_review.md`、`paper.pdf`、`paper_content.txt`、`bibtex.bib` 的相对路径链接，方便后续人工复核。
5. **单篇目录是事实承载单元**：后续若移动、重命名或替换任何单篇目录，必须同步更新两个 CSV、[SUMMARY.md](./SUMMARY.md) 与所有相对路径链接。

## 3. 证据写法与短引文规则

1. `fulltext_review.md` 的主证据应是**页码定位 + 中文短转述**，不能只写“相关 / 不相关”。
2. 每篇允许保留少量短引文用于定位原文语境；短引文必须很短，并配页码或位置，不得复制长段摘要、正文、表格或结论。
3. D1--D7 每个维度都要同时写：
   - 评分；
   - 正证据定位 / 短转述；
   - 负证据 / 边界；
   - 对 #85 写作动作。
4. 如果某个维度只能由关键词命中支持，必须标明这是“全文初检 / 关键词页码定位”，不能写成深度人工精读结论。
5. 若后续人工精读发现自动关键词误判，优先以人工页码证据覆盖，并同步 CSV 与 SUMMARY。

## 4. D1--D7 可执行评分标准

Emoji 口径：`🟢` 核心强相关，`🟡` 高度近邻，`🟠` 值得关注，`🔴` 低相关 / 排除。正式总账表格中 emoji 列只写 emoji；解释写在 rationale / review 文本中。

### 4.0 七维独立打分硬规则

1. **每一行必须有七个独立评分**：`D1`--`D7` 不能被一个总等级、总相关性或人工印象替代；缺任一维度评分时，该行不能进入全文级 baseline 总账。
2. **读者可见维度名必须中文化**：正式 Markdown 表格、`fulltext_review.md` 小节标题和人工审阅意见中应写“D1 控制系统领域贴近度”这类中文名；CSV 可保留机器字段名如 `D1_fulltext_score`。
3. **评分必须写出正证据、负证据和写作动作**：每个维度至少包含 `score / locator / paraphrase / negative_evidence / writing_action` 五类信息；只写 emoji 或只写“相关”视为 I 级问题。
4. **优先按全文证据打分**：题名 / 摘要只能作为初筛证据；进入本文库后，分数必须来自 `paper_content.txt` 与必要的 PDF 核对。若只是关键词定位而非深度人工精读，必须在 `fulltext_review.md` 明确标为“全文初检”。
5. **强相关不得由泛词单独触发**：例如 `model`、`system`、`testing`、`AI`、`human-in-the-loop` 这类泛词不能单独把 D1--D4 升到 `🟢`；必须有与该维度定义匹配的上下文证据。
6. **D7 是 claim gate，不是平均分**：D7 只评价该文对 #85 gap、novelty、Related Work、方法门槛或排除审计的支撑度；不得简单由 D1--D6 多数投票得出。
7. **分数变动必须可审计**：若从 metadata 初筛分数升级 / 降级，必须记录 `changed_from_metadata`、原因和新证据位置，并同步 [data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv)。

### D1 控制系统领域贴近度

| 等级 | 可执行标准 |
|---|---|
| 🟢 | 论文核心问题域就是控制、CPS、嵌入式、安全关键、自动驾驶、机器人、IoT、数字孪生、ECU 等；这些词出现在摘要 / 引言 / RQ / 方法 / 结果等核心位置 |
| 🟡 | 论文有明确控制/CPS/嵌入式等案例或子类，但不是全文唯一主线 |
| 🟠 | 仅在背景、相关工作、参考文献或泛化例子中出现控制/CPS 词，不能直接支撑 #85 domain claim |
| 🔴 | 基本不涉及控制系统或安全关键系统语境 |

### D2 行为模型与状态机贴近度

| 等级 | 可执行标准 |
|---|---|
| 🟢 | state machine/statechart/automata、行为模型、SysML/UML 状态行为、模型转换或系统行为验证是核心对象 |
| 🟡 | 明确涉及 MBSE/MDE/行为模型/系统行为，但状态机不是中心对象 |
| 🟠 | 只出现建模、架构、测试或泛 formalism，缺少状态机/行为模型实质证据 |
| 🔴 | 与行为模型或状态机无明显关系 |

### D3 语料、基准与景观研究贴近度

| 等级 | 可执行标准 |
|---|---|
| 🟢 | 论文提供或系统整理 benchmark、corpus、dataset、primary studies、taxonomy、landscape、mapping，能直接启发 #85 的 benchmark-source landscape 写法 |
| 🟡 | 有系统综述 / 系统映射或主研究表，但与 benchmark/source landscape 关系间接 |
| 🟠 | 只有少量数据/案例/评价对象，不能形成景观或基准叙事 |
| 🔴 | 无语料、基准、数据集、主研究或景观结构 |

### D4 大模型辅助建模贴近度

| 等级 | 可执行标准 |
|---|---|
| 🟢 | LLM、生成式 AI、ChatGPT 或 AI/ML 辅助建模 / 需求 / 测试 / 代码智能是核心主题 |
| 🟡 | AI/ML 是重要维度，但 LLM4Modeling 只是子主题或相邻应用 |
| 🟠 | 只在背景或未来工作中提到 LLM/AI，或 AI 不是主要对象 |
| 🔴 | 不涉及 LLM/AI/ML |

### D5 系统综述与系统映射方法严谨性

检查 9 项：RQ、检索策略、纳排标准、筛选流程 / PRISMA、数据抽取、质量评估、一致性 / 仲裁、threats、补充材料 / 主研究清单。

| 等级 | 可执行标准 |
|---|---|
| 🟢 | 命中 7--9 项，且方法节足以作为 CCF-A/B survey / mapping 写作门槛参照 |
| 🟡 | 命中 5--6 项，有较完整系统综述过程但存在少量缺口 |
| 🟠 | 命中 3--4 项，更像 roadmap / survey / position paper 或方法信息不完整 |
| 🔴 | 命中 0--2 项，不能作为系统综述方法学锚点 |

### D6 制品、可复现性与获取价值

| 等级 | 可执行标准 |
|---|---|
| 🟢 | 单篇目录有 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md`，且原文还提供公开 artifact / replication package / primary-study list / supplementary material |
| 🟡 | 单篇目录四件套齐全，文本可抽取，可支持本地复查；但公开 artifact 或补充材料未确认 |
| 🟠 | PDF 或抽取文本存在质量问题，仍可部分复查 |
| 🔴 | 无法获得 PDF 或无法可靠抽取文本 |

### D7 对 #85 证据门支撑度

| 等级 | 可执行标准 |
|---|---|
| 🟢 | 直接影响 #85 gap / novelty / RQ / Related Work 主体，必须在论文中正面定位 |
| 🟡 | 是高度近邻或重要方法学锚点，需在 Related Work 或方法学部分处理 |
| 🟠 | 只作背景、术语、写法或方法参考，不影响核心 gap |
| 🔴 | 对 #85 主线基本无支撑，或只需在排除审计中保留 |

### 4.8 评分降级与升级判定

| 场景 | 默认动作 |
|---|---|
| 只有标题 / 摘要出现相关词，正文无法定位 | 对应维度最高 `🟠`，并标注 `metadata_or_abstract_only` |
| 关键词命中多但语境是参考文献、工具名、泛背景 | 维度不得自动升为 `🟢`；必须写清为什么只能 `🟡/🟠` |
| 原文有系统综述方法，但缺少纳排、质量评估或主研究清单 | D5 按 9 项 checklist 命中数降级，不用“survey”标题自动给高分 |
| 原文有公开 artifact / supplementary / primary-study list | D6 可从 `🟡` 升为 `🟢`，但必须写出入口或页码 / 附录位置 |
| 论文非常接近 #85 但仍未覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling”三段式 | final relation 写 `verified_gap_neighbor_fulltext`，不得写成已排除 direct competitor risk |
| 后续 G3 检索发现同题完整竞品 | 立刻升级为 C 级 novelty 风险，回写 [../story/claim_evidence_map.md](../story/claim_evidence_map.md) 与 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md) |

### 4.9 CSV 与 SUMMARY 字段合同

`data/fulltext_review_matrix.csv` 是机器真源；每一行至少应维护以下字段族：

| 字段族 | 必填字段示例 | 规则 |
|---|---|---|
| 身份与关系 | `fulltext_review_id`、`request_id`、`priority`、`title`、`doi_value`、`final_relation_level`、`related_work_bucket` | `final_relation_level` 必须与 [SUMMARY.md](./SUMMARY.md) 的关系分布一致 |
| 文件证据 | `paper_pdf_path`、`paper_content_path`、`bibtex_path`、`fulltext_review_path`、`pdf_sha256_16`、`paper_content_sha256_16` | 路径必须能从本文库根目录解析；短哈希用于重抽取审计 |
| 七维评分 | `D1_fulltext_score` ... `D7_fulltext_score` | 七个字段都不能为空，且只允许 `🟢/🟡/🟠/🔴` |
| 七维证据 | `D*_fulltext_evidence_locator`、`D*_fulltext_paraphrase`、`D*_negative_evidence`、`D*_writing_action`、`D*_confidence` | 每个维度必须能回到 `fulltext_review.md` 对应证据段；`writing_action` 必须保留该维度如何进入 / 避让 #85 写作 |
| 方法学 checklist | `has_rq`、`has_search_strategy`、`has_inclusion_exclusion`、`has_flow_or_prisma`、`has_data_extraction`、`has_quality_assessment`、`has_irr_or_arbitration`、`has_threats`、`has_artifact_or_primary_list` | D5 必须由这 9 项推导；不能只凭标题判断 |
| claim gate | `claim_element`、`challenge_or_support`、`difference_from_85_fulltext`、`novelty_action_fulltext`、`eligible_for_claims`、`remaining_uncertainty` | 用于回写 #85 story，防止 unsupported novelty claim |

[SUMMARY.md](./SUMMARY.md) 是人类总账，不复制全部 CSV 字段；但必须保留四件套链接、D1--D7 emoji、final relation、关系分布与当前安全写法。

## 5. `fulltext_review.md` 必备结构

每篇 `fulltext_review.md` 至少包含：

1. 本条 review 定位。
2. 文件与元数据：必须链接 `paper.pdf`、`paper_content.txt`、`bibtex.bib`。
3. 最终全文级判断：metadata 关系、全文关系、Related Work 桶、claim gate、剩余不确定性。
4. 可追溯短引文与页码定位。
5. D1--D7 全文级证据链：评分、正证据、负证据、写作动作。
6. 关键词页码索引。
7. 系统综述 / 系统映射方法学 checklist。
8. 可写与不可写声明。
9. 后续复查入口。

### 5.1 证据链最低密度

为避免 `fulltext_review.md` 变成只有结论的空壳，每篇 review 必须满足：

1. §2 写清 `metadata 阶段关系 -> 全文级关系 -> Related Work 桶 -> claim gate -> 剩余不确定性`。
2. §3 至少提供 1 条短引文定位；每条短引文应尽量短，默认不超过 25 个英文词或等价长度，并配页码 / 章节位置。
3. §4 至少覆盖 D1--D4 与 D5/D7 的证据锚点；若某维度为 `🔴`，也要写明“未命中 / 不支撑”的负证据。
4. §5 的 D1--D7 表格必须逐维写 `评分、正证据、负证据、写作动作`。
5. §6 必须列出与 #85 三段式主线相关的 negative evidence search，例如 `state machine source landscape`、`control requirements benchmark`、`LLM4Modeling state machine` 等。
6. §8 方法学 checklist 必须能解释 D5；若 checklist 由关键词自动检出，须保留人工复查风险。
7. §9 必须区分“当前可写”和“当前不可写”，尤其禁止把 P0 gap-neighbor 写成 complete direct competitor search。

### 5.2 可写 / 不可写声明模板

单篇 review 的 §9 应至少覆盖以下问题：

| 问题 | 当前可写 | 当前不可写 |
|---|---|---|
| Related Work | 可写其属于哪个近邻桶，以及与 #85 的对象 / 方法 / 数据边界差异 | 不可把近邻直接写成同题竞品，除非 G3 已确认 |
| Novelty gate | 可写“该文未关闭 #85 三段式 gap”，但必须保留 G3 caveat | 不可写“已经证明不存在直接竞品” |
| 方法学 | 可借鉴其 RQ、检索、纳排、抽取、质量评估、Threats 或 artifact policy | 不可把其方法完整性当作 #85 方法已经达标 |
| 原文引用 | 可用短引文 + 页码 + 中文转述 | 不可复制长摘要、长表格、长结论或整段原文 |

## 6. 数据同步规则

任何单篇 review 变化都必须检查以下同步：

| 变化类型 | 必须同步 |
|---|---|
| PDF 或 TXT 重生成 | `fulltext_review.md`、[data/local_fulltext_receipt.csv](./data/local_fulltext_receipt.csv)、[data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv) 的短哈希、页数、抽取状态 |
| D1--D7 改分 | 单篇 `fulltext_review.md`、[data/fulltext_review_matrix.csv](./data/fulltext_review_matrix.csv)、[SUMMARY.md](./SUMMARY.md) |
| final relation 改动 | [SUMMARY.md](./SUMMARY.md)、[../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md) |
| 新增 / 删除论文 | [SUMMARY.md](./SUMMARY.md) 总数、两个 CSV、单篇目录、更新日志 |

## 7. 更新流程

1. 先读本 [README.md](./README.md)、本 [GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 进入单篇目录，按 `bibtex.bib -> paper_content.txt -> paper.pdf -> fulltext_review.md` 的顺序核验。
3. 修改单篇 review 或源文件。
4. 同步 CSV 与 SUMMARY。
5. 回到 #85 上层 [../story/claim_evidence_map.md](../story/claim_evidence_map.md) 和 [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md) 检查 claim 影响。
6. reviewer 必须 dry-run 至少 2 篇：一篇 P0 gap neighbor，一篇 P1 near/methodology anchor；检查从 README → SUMMARY → 单篇 review → PDF/TXT 的跳转与证据链是否闭合。
7. 每轮修改后运行文库校验脚本：

```bash
source venv/bin/activate
python project_1_llm_state_machine_modeling/paper_stm_source_landscape/survey_baseline_library/checks/validate_library.py
git diff --check
```

校验脚本会检查四件套数量、D1--D7 独立评分、七维证据字段、SUMMARY 相对路径链接、README/GUIDE 规则锚点和旧口径残留；失败时不得把该文库标记为 ready。

## 8. C/I/M 审查口径

- C：缺少任一单篇四件套；把初检写成 complete direct competitor search；覆盖上游/用户已确认事实；长段复制原文导致制品污染。
- I：D1--D7 没有页码/章节定位；CSV 与 SUMMARY 统计不一致；README/GUIDE 无法指导新增或修正；P0/P1 结论未回写 claim gate。
- M：命名、表格局部可读性、措辞和非阻塞字段扩展建议。
