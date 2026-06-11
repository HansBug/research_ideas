# A Systematic Review of IoT Systems Testing: Objectives, Approaches, Tools, and Challenges

## 0. 本条 review 的定位

本文件是 #85 综述 baseline 文库的单篇全文级审计记录。它的目的不是复述论文全文，而是把 [paper.pdf](./paper.pdf) 与 [paper_content.txt](./paper_content.txt) 中可追溯的证据压缩成可用于 #85 Related Work、novelty gate 和方法学门槛的判断。

## 1. 文件与元数据

| 字段 | 值 |
|---|---|
| review id | `FR-023` |
| request id | `MD-P1-016` |
| 优先级 | `P1` |
| DOI | [10.1109/tse.2024.3363611](https://doi.org/10.1109/tse.2024.3363611) |
| 期刊 / 会议 | IEEE Transactions on Software Engineering |
| 年份 | 2024 |
| CCF | CCF-A |
| 单篇目录 | [./](./) |
| PDF | [paper.pdf](./paper.pdf) |
| 提取文本 | [paper_content.txt](./paper_content.txt) |
| BibTeX | [bibtex.bib](./bibtex.bib) |
| PDF 页数 / 可抽取页 | 31 / 31 |
| PDF SHA256 短哈希 | `7ed5126bbdacf164` |
| `paper_content.txt` SHA256 短哈希 | `25829bcfb2502854` |
| 抽取方式 | `python -m tools.pdf_extractor -m text` |

## 2. 最终全文级判断

| 字段 | 结论 |
|---|---|
| metadata 阶段关系 | `candidate_near_metadata_only` |
| 全文级关系 | `verified_near_neighbor_fulltext` |
| Related Work 桶 | `near_neighbor` |
| claim gate | `G3 novelty / G6 related-work positioning / G7 method bar` |
| 是否可用于正文 claim | `yes_with_locator_and_caveat` |
| 剩余不确定性 | 本轮为 P0/P1 本地全文初检；仍需后续 G3 多数据库直接竞品检索闭环。 |

**对 #85 的短结论**：全文确认其可作为控制/CPS/自动驾驶/IoT 等应用域近邻，主要支撑领域 taxonomy、测试/验证背景或 benchmark asset 叙事；与 #85 的 LLM4Modeling/STM 来源景观仍需区分。

**差异化写作动作**：保留 #85 的状态机来源景观定位；写作时必须说明该文覆盖的相邻主题与 #85 的对象/语料/任务边界差异。

## 3. 可追溯短引文与页码定位

> 短引文只用于帮助人工回到原文定位；每篇保留一个很短片段，正式写作以页码定位 + 中文转述为主。

| 页码 / 位置 | 触发词 | 短引文 |
|---|---|---|
| 1 | `abstract` | “Internet of Things IoT systems are becoming prevalent in various domains from healthcare to smart homes Testing IoT systems is critical in” |

## 4. 多维证据锚点

| 支撑维度 | 页码 / 章节定位 | 短摘录 / 定位词 | 中文转述与用途 |
|---|---|---|---|
| D1 | 页 1; 全部页码 1;2;3;4;5;6;7;8;9;10 | `cyber-physical` / `control` / `embedded` 等定位词 | 控制/CPS 相关词命中 591 次，说明其领域相邻性为 🟢。 |
| D2 | 页 30; 全部页码 30;17;18 | `state machine` / `behavioral model` / `SysML` 等定位词 | 状态机/行为模型相关证据合计 3 次，说明其模型对象贴近度为 🟡。 |
| D3 | 页 1; 全部页码 1;2;3;4;5;6;7;10;11;21 | `benchmark` / `corpus` / `dataset` / `primary studies` 等定位词 | 基准/语料/主研究相关证据命中 17 次，说明其景观/基线写法价值为 🟡。 |
| D4 | 页 26; 全部页码 26;28 | `LLM` / `generative AI` / `machine learning` 等定位词 | LLM/AI/ML 相关证据命中 2 次，说明其 LLM4Modeling 或 AI-for-SE 近邻价值为 🟠。 |
| D5/D7 | 见 §7 方法学 checklist 与 §5 D7 | `research question` / `search strategy` / `threats` 等方法定位词 | 方法学检查项命中 9/9，最终关系为 `verified_near_neighbor_fulltext`；可支撑 #85 的 Related Work/claim gate，但不关闭 G3。 |

## 5. D1--D7 全文级证据链

| 维度 | 评分 | 正证据定位 / 短转述 | 负证据 / 边界 | 写作动作 |
|---|---|---|---|---|
| D1 控制系统领域贴近度 | 🟢 | 全文关键词定位显示 `控制/CPS/嵌入式/自动驾驶` 命中 591 次，页码 1;2;3;4;5;6;7;8;9;10；用于判断论文是否真正处在控制/CPS/嵌入式或安全关键系统问题域。 | 未发现同一论文完整覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 #85 主线。 | 用于 Related Work 分层；若写入论文正文，必须保留页码/章节 locator，并用短转述说明与 #85 的对象差异。 |
| D2 行为模型与状态机贴近度 | 🟡 | `状态机/自动机` 命中 1 次（页 30），`行为模型/MBSE/SysML/UML` 命中 2 次（页 17;18）；用于判断是否靠近状态机/行为模型。 | 未发现同一论文完整覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 #85 主线。 | 用于 Related Work 分层；若写入论文正文，必须保留页码/章节 locator，并用短转述说明与 #85 的对象差异。 |
| D3 语料、基准与景观研究贴近度 | 🟡 | `基准/语料/数据/主研究` 命中 17 次，页码 1;2;3;4;5;6;7;10;11;21；用于判断其是否能支撑语料、基准、景观或系统映射写法。 | 未发现同一论文完整覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 #85 主线。 | 用于 Related Work 分层；若写入论文正文，必须保留页码/章节 locator，并用短转述说明与 #85 的对象差异。 |
| D4 大模型辅助建模贴近度 | 🟠 | `LLM/AI/ML` 命中 2 次，页码 26;28；用于判断其是否属于 LLM/AI-for-SE/LLM4Modeling 近邻。 | 未发现同一论文完整覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 #85 主线。 | 用于 Related Work 分层；若写入论文正文，必须保留页码/章节 locator，并用短转述说明与 #85 的对象差异。 |
| D5 系统综述与系统映射方法严谨性 | 🟢 | 系统综述方法 checklist 命中 9/9 项；命中项和页码在 §7 展开，用于判断是否达到 CCF-A/B survey / mapping 的方法学参照价值。 | 方法学 checklist 来自文本检索与人工可读初检，不能替代最终投稿前对 protocol、appendix、supplementary material 的逐项人工复核。 | 用于反推 #85 的 survey / mapping 写作标准、Threats、数据抽取表和审稿门槛。 |
| D6 制品、可复现性与获取价值 | 🟡 | 本条已提交 `paper.pdf`、由 `tools.pdf_extractor.py` 生成的 `paper_content.txt`、`bibtex.bib` 与本 review；PDF 页数 31，可抽取页 31，短哈希 `7ed5126bbdacf164`。 | PDF 与抽取文本只作为本论文工作区的研究资料；对外写作/PR comment 不应粘贴长段原文，正式引用仍需页码/章节定位和短转述。 | 用于后续复查与引用资产管理；若 PDF/文本重抽取，必须更新短哈希和 receipt。 |
| D7 对 #85 证据门支撑度 | 🟡 | 最终关系为 `verified_near_neighbor_fulltext`，支持 `G3 novelty / G6 related-work positioning / G7 method bar`；对 #85 的影响是 `support_and_bound_gap`，但仍保留 G3 全面检索不确定性。 | 未发现同一论文完整覆盖“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 #85 主线。 | 用于 claim-evidence map；只允许写 gap-neighbor / near-neighbor，不允许宣称 complete direct-competitor search 已关闭。 |

## 6. 负证据检索

为避免把近邻误写成直接竞品，本条至少检查了以下同题信号：`state machine source landscape`、`state-machine corpus`、`control requirements benchmark`、`LLM4Modeling state machine`、`benchmark-source landscape`。当前未形成同一论文完整覆盖 #85 三段式主线的证据；该结论仍需后续 G3 多数据库检索闭环复核。

## 7. 关键词页码索引

| 证据组 | 命中次数 | 页码定位 |
|---|---:|---|
| 状态机/自动机 | 1 | 30 |
| 行为模型/MBSE/SysML/UML | 2 | 17;18 |
| MDE/MDSE/模型转换 | 0 | — |
| 需求/规约 | 13 | 2;3;14;15;16;17;21 |
| LLM/AI/ML | 2 | 26;28 |
| 基准/语料/数据/主研究 | 17 | 1;2;3;4;5;6;7;10;11;21 |
| 控制/CPS/嵌入式/自动驾驶 | 591 | 1;2;3;4;5;6;7;8;9;10 |
| 验证/测试/安全 | 697 | 1;2;3;4;5;6;7;8;9;10 |

## 8. 系统综述 / 系统映射方法学 checklist

| 检查项 | 命中 | 页码定位 |
|---|---|---|
| 研究问题 RQ | yes | 1;2;3;6;7;13;15;25 |
| 检索策略 | yes | 3;4;5 |
| 纳入/排除标准 | yes | 1;2;4;5;6;25 |
| 筛选流程 / PRISMA | yes | 1;2;3;4;6;25;27;28 |
| 数据抽取 | yes | 6;7;25 |
| 质量评估 | yes | 6;8;28 |
| 一致性 / 仲裁 | yes | 5;6;11;13;25;28 |
| 威胁与限制 | yes | 1;4;8;13;20;21;23;24 |
| 补充材料 / 主研究清单 | yes | 1;2;4;5;6;7;10;11 |

## 9. 可写与不可写声明

### 9.1 当前可写

- 可写成 #85 的 `near_neighbor` 相关工作，并用上表页码定位支撑其领域、模型、语料 / 基准、LLM/AI、方法学价值。
- 可作为 #85 叙事中的边界参照：说明已有工作覆盖了哪些相邻主题，以及为何仍未等同于“控制系统状态机来源景观”。

### 9.2 当前不可写

- 不可声称该文已经完整覆盖 #85 的三段主线。
- 不可用本条替代 G3 多数据库 direct-competitor safety search。
- 不可在论文或 PR comment 中复制长段原文；如需引用，只使用短引文 + 页码 + 自己的转述。

## 10. 后续复查入口

- 若 D1--D7 任一评分被后续人工精读改动，必须同步更新 [../../data/fulltext_review_matrix.csv](../../data/fulltext_review_matrix.csv) 与 [../../SUMMARY.md](../../SUMMARY.md)。
- 若 PDF 或 `paper_content.txt` 重生成，必须更新本文件的短哈希、页数、抽取状态和 [../../data/local_fulltext_receipt.csv](../../data/local_fulltext_receipt.csv)。
