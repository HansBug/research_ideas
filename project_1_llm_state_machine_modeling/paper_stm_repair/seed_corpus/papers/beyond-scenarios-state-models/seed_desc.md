# Beyond Scenarios: Generating State Models from Use Cases

## R1.5 strict seed 全文核验结论

| 字段 | 结论 |
|---|---|
| candidate_id | `beyond-scenarios-state-models` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/beyond-scenarios-generating-state-models-from-use-cases/`](../../../../baselines/beyond-scenarios-generating-state-models-from-use-cases/) |
| 核验顺序 | `bibtex.bib` -> `paper_content.txt` -> `paper.pdf` -> `DESC.md` |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-3` |
| R2 可用性 | `low`：论文内有可读用例、domain model、生成算法和 FSM 图；无公开代码、数据包、可下载 UCEd、机器可读输出或 license。 |
| 当前结论 | 可作为“结构化 use case / restricted NL -> hierarchical finite state transition machine”的历史前身 seed；不应冻结为 SS-A/R2 可复现样本。 |

## P1/P2/P3/P4 判定

| 谓词 | 判定 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | PDF p.1 abstract: Use Case 是 textual representation of requirements；p.1 introduction: use cases 使用 restricted form of natural language；p.2 Figure 1 给出 Patient Monitoring System 的 login use case，包含 Goal、Precondition、Steps、Exceptions、Postcondition。 |
| P2_T0_STM_FAMILY | pass | PDF p.3 Section 3: 生成 hierarchical type of finite state transition machines；PDF p.4 定义 finite state transition machine 元组 $[\Sigma, S, F, S0]$，Figure 5 标注为 finite state transition machine generated from use case User login。 |
| P3_GENERATION_RELATION | pass | PDF p.1 abstract: 提出 formalization、natural-language based syntax 和 algorithm，incrementally composes a set of use cases as a finite state transition machine；PDF p.4 给出从 use case `[Title, Pre, Steps, Post]` enrich state transition machine `M` 的逐步算法。 |
| P4_EVIDENCE_POINTER | pass | PDF p.2 Figure 1 / Figure 2；PDF p.3 Figure 3 / Figure 4；PDF p.4 FSM definition + algorithm + Figure 5；PDF p.5 Section 4 描述 UCEd 工具边界。 |

## SS/SA 解释

- `SS-B`：满足 strict seed 的核心研究关系，输入是需求级 use case/restricted natural language，输出是有限状态迁移机/层次 FSM，生成关系由论文算法和 Figure 5 直接支持。
- 不标 `SS-A`：输入不是自由自然语言需求，而是受限英文 + 字段化 use case + domain model；论文没有开放可复现实验包，`paper_content.txt` 也存在严重编码异常，需要依赖 PDF 页面核验。
- `SA-3`：artifact 主要是论文内示例和本地 PDF。论文描述 UCEd 正在实现，未给公开下载、源码仓库、版本化 artifact、benchmark 或 supplementary。

## 排除码检查

| 排除项 | 结论 | 说明 |
|---|---|---|
| 非 NL/需求输入 | 不触发 | 输入是 use case 文本与 restricted natural language，但需要结构化字段和 domain model。 |
| 非 STM 输出 | 不触发 | 输出为 finite state transition machine，且含 sub-state / hierarchical 关系。 |
| 仅 verification/repair | 不触发 | 论文主体是 generation；postcondition 可用于 verification，但不是主任务。 |
| Protocol-only / T1+ / timed / hybrid | 不触发 | 输出不是 timed automata/hybrid automata；引用 timed automata 只在 related/reference 背景中出现。 |
| Artifact-only 无论文证据 | 不触发 | 论文正文、算法、图 5 直接支持。 |

## 证据与风险

- 本地 `paper_content.txt` 含 NUL 字节并大面积乱码，不能作为主要全文证据；本次以 PDF 渲染页核验为准。
- OCR 路径尝试失败：本机 `tesseract` 不在 `PATH`，因此未生成新的 OCR 文本。
- PDF 页数为 5 页，`pdfinfo` 显示 Producer 为 GNU Ghostscript 6.51，PDF version 1.2。
- `DESC.md` 与 PDF 结论一致：原文未提供公开代码/仓库或统一 benchmark。

## 后续使用建议

1. 可用于 R1/R2 讨论中的“早期结构化需求到状态模型”对照样本。
2. 若进入转换实验，应手工转录 PDF p.2 Figure 1、PDF p.3 Figure 3、PDF p.4 Figure 5，并在 run record 中标注为 manual transcription。
3. 不建议纳入需要公开 artifact/license/机器可读输出的 R2 主统计。
