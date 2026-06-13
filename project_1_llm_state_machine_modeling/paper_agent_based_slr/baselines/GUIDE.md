# baselines/GUIDE.md：LLM-based SLR 近邻 baseline 维护规则

## 1. 目标与边界

本目录用于支撑第二篇 agent-based SLR 论文的 Related Work、novelty matrix、claim-evidence map 和评测设计。它不是普通“文献堆放处”，而是一个面向 CCF A 类论文写作的 **claim-evidence baseline 审计库**：每条强判断都必须能回到 PDF、`paper_content.txt`、BibTeX 或官方元数据。

新增或重写条目时，必须判断它是否会威胁本文如下候选贡献：

1. 将 SLR / SMS 的检索、筛选、抽取、编码、综合、报告组织为 agent 工作流。
2. 为每个阶段保存可审计证据链和 run record。
3. 把报告级 claim 绑定到论文来源、筛选决策、抽取记录和编码决策。
4. 通过 human audit gate 控制幻觉、unsupported claim 和错误证据定位。
5. 在软件工程 / LLM4SE / MDE 语境中评价该工作流。

本目录可以先保存 title / abstract 粗筛，但只要 PDF 已获取，`review.md` 必须逐步升级为全文核验稿。正式写 paper 的 Related Work / novelty 对比时，不能引用粗筛结论替代全文证据。

## 2. 纳入范围

优先纳入：

1. LLM-based systematic literature review / systematic mapping。
2. LLM-assisted screening、corpus filtration、data extraction、coding、evidence synthesis、review composition。
3. agentic / multi-agent literature review、survey generation、scientific knowledge synthesis。
4. human-in-the-loop evidence synthesis、provenance-aware extraction、claim-to-source traceability。
5. 软件工程、LLM4SE、MDE、empirical SE 中与 SLR/SMS 自动化直接相关的论文。
6. 虽不直接自动化 SLR，但会影响本文 evaluation design、survey quality evaluation、citation grounding、LLM variability、false negative 风险或 SE community positioning 的论文。

暂不纳入或降为 P2：

1. 只做普通摘要、问答、RAG 写作，没有 SLR / SMS 任务语境的工作。
2. 只研究 LLM4SE 任务本身、没有文献综述自动化流程的工作。
3. 只有宣传网页、无论文 / DOI / arXiv / 官方仓库的工具。
4. 与本文 novelty 无关的通用 survey generation 工作；除非其 agent / evaluation / citation 机制强到足以影响本文报告生成 claim。

## 3. 分层口径

| 分层 | 含义 | 处理规则 |
|---|---|---|
| P0 | 强 baseline / 直接 novelty 威胁 | 必须建立单篇目录；`review.md` 必须全文核验；Related Work 与 novelty matrix 必须逐段对比。 |
| P1 | 高度关注 / 局部强 baseline | 原则上建立单篇目录并全文核验；至少说明威胁筛选、抽取、综合、审计、评价或报告生成中的哪一环。 |
| P2 | 背景相关 / 方法参照 | 若 PDF 可自动获取且会影响 story/evaluation，应建立单篇目录；否则可只留检索表。 |
| PX | 排除 | 只在检索日志保留必要排除理由，不进入总表。 |

## 4. 七维评分标准

emoji 列在正式表格中只写 emoji；中文解释集中写在本节。每篇候选必须独立给出 D1-D7，不能只给一个总等级。

| 维度 | 🟢 强 | 🟡 中 | 🟠 弱 | ⚪ 无 / 背景 |
|---|---|---|---|---|
| D1 主题贴合度 | 直接研究 LLM / agent 执行 SLR、SMS、literature review 或 evidence synthesis | 研究 LLM 辅助筛选、抽取、编码、综述写作中的关键环节 | 只讨论 LLM4SE / research automation，和 SLR 关系间接 | 与 SLR / 文献综述自动化基本无关 |
| D2 SLR/SMS 流程覆盖度 | 覆盖检索、筛选、抽取、编码、综合、报告中的四个及以上环节 | 覆盖两个到三个核心环节 | 只覆盖一个环节或泛泛讨论 | 不覆盖可识别 SLR/SMS 环节 |
| D3 LLM/agent 自动化深度 | 使用 LLM / agent 执行多阶段工作流并有明确输入输出链 | 使用 LLM 辅助单阶段或少数阶段，流程较清楚 | 只做 prompt / chatbot 演示或概念性讨论 | 没有 LLM / agent 自动化实质内容 |
| D4 人工审计与可追踪性 | 明确提供 human-in-the-loop audit、claim-to-source trace、决策日志、per-cell provenance 或可复核证据包 | 有人工复核或 provenance，但链条不完整 | 只提到人工检查或引用来源，缺少可执行审计设计 | 无人工审计或可追踪性机制 |
| D5 评价严谨性 | 有真实数据集、多案例、金标或人工标注、误差分类、对照基线或可复现实验 | 有实验或案例，但样本、指标或复现性有限 | 只有小例子、用户研究片段或定性讨论 | 无实证评价 |
| D6 SE / CCF 相关性 | 发表在 CCF A/B/C SE/AI4SE/MDE 强相关 venue 或直接面向软件工程 SLR | 非 CCF 但与 SE / LLM4SE / MDE 强相关 | 泛 AI / 医学 / 社科综述自动化，可提供方法背景 | 与本仓库主题或目标 venue 关联弱 |
| D7 对本文 novelty 的威胁强度 | 已经覆盖 agent-based + SLR 多阶段 + audit/traceability/evaluation 的核心组合 | 覆盖其中多个关键点，需要本文明确差异化 | 只覆盖局部点，可作为 related work 背景 | 不构成 novelty 威胁 |

### 4.1 全文核验评分规则

1. `粗筛评分` 可以来自 title / abstract；`全文评分` 必须来自 `paper_content.txt` 或 PDF 的方法、实验、系统描述、结论等正文证据。
2. 若全文没有支持某个维度的证据，应降级评分，而不是沿用粗筛推测。
3. 若 PDF 文本提取缺页、乱码或图表缺失，应在该维度写“证据不足 / 待 PDF 核对”，不能脑补。
4. D7 必须和本文 paper2 的具体 claim 绑定：威胁的是 agent workflow、human audit、claim-to-source、SE setting、evaluation protocol，还是报告生成。
5. 对 arXiv 论文，D6 不能写成 CCF/peer-reviewed；若后续发现正式版本，必须补充 venue 和核验日期。

## 5. 检索策略

### 5.1 CCF A/B/C venue 粗筛

1. 范围以 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 和 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 当前 venue 为基线。
2. 优先级：年度 README 已维护 paper list → 官方 accepted/program/proceedings → publisher TOC → DBLP 年度页 → 搜索线索。
3. 多数 CCF venue 不提供可批量获取 abstract；若只有标题，必须写成 title-level discovery，不能写成 abstract screening。
4. 遇到 429、403、WAF、尚未出版、DBLP 未归档，应写入 [search/ccf-venue-coverage-gaps.md](./search/ccf-venue-coverage-gaps.md)，不得解释为“无相关论文”。
5. 每个 venue-year 的最低审计字段为：入口 URL、检查日期、coverage emoji、是否拿到 title list、命中 title 数、排除理由或 gap 原因；能自动扫描的原始命中应保留到 [search/ccf-dblp-title-scan-raw.md](./search/ccf-dblp-title-scan-raw.md)。
6. 若发现 CCF-adjacent workshop / companion 命中，必须标注 track / source，不得冒充 main track。

### 5.2 arXiv 粗筛

1. 保留 query、检索时间、原始记录、去重数量、纳入数量。
2. 初始 query 至少覆盖：`LLM + systematic literature review`、`LLM + screening/extraction/synthesis`、`agentic literature review`、`automated literature review`、`evidence synthesis`、`survey generation`。
3. 原始 arXiv query 快照写入 [search/arxiv-query-raw-snapshot.jsonl](./search/arxiv-query-raw-snapshot.jsonl)，2024--2026 去重候选池写入 [search/arxiv-dedup-candidate-pool.jsonl](./search/arxiv-dedup-candidate-pool.jsonl)。
4. 正式纳入候选元数据写入 [search/arxiv-query-results.jsonl](./search/arxiv-query-results.jsonl)，粗筛总表写入 [search/arxiv-2024-2026-title-abstract-screening.md](./search/arxiv-2024-2026-title-abstract-screening.md)。
5. 每条未纳入候选至少保留 `screening_decision=excluded` 与中文排除理由；否则不能把 291→34 这类筛选链条写成可审计。

## 6. 单篇目录规则

每个入库目录至少包含：

```text
papers/<slug>/
├── paper.pdf
├── paper_content.txt
├── bibtex.bib
└── review.md
```

要求：

1. `paper.pdf`：优先使用 arXiv / official open PDF；若 publisher 受限，不强行绕过。
2. `paper_content.txt`：必须用仓库工具生成：
   ```bash
   source venv/bin/activate
   python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
   ```
   若文字模式严重异常，再记录 OCR 或人工复查。
3. `bibtex.bib`：至少含 title、author、year、url/eprint；正式引用前再补 DOI / venue。
4. `review.md`：必须按 §6.1 的全文 review 模板维护。逐维判定理由不能只写模板句；每个维度至少要有一个 `paper_content.txt` 页码/章节/表格/实验证据锚点。
5. 单篇 `review.md` 可以使用少量原文短语，但不要复制长段英文；默认用中文转述并给出 PDF / `paper_content.txt` 链接。

### 6.1 `review.md` 全文核验模板

每篇 review 必须显式区分“是否读过原文”。这是证据管理字段，不是措辞装饰。允许的 `阅读状态` 至少包括：

| 阅读状态 | 含义 | 可写结论边界 |
|---|---|---|
| `未读原文-仅题摘粗筛` | 只读 title / abstract / 元数据 | 只能写候选相关性和待核验假设，不得写方法细节或实验结论为事实 |
| `已读全文文本-paper_content核验` | 已阅读 `paper_content.txt` 的摘要、引言、方法、实验、结论等关键部分 | 可写全文级方法/实验/结果总结，但图表和公式若提取不完整需标注 |
| `已回PDF核对图表` | 在文本阅读之外，已打开 PDF 核对关键图表、表格、公式或版式 | 可写图表/表格级证据，并标注页码或表号 |
| `全文不可得-待人工下载` | 合法 PDF 未获取 | 只能保留元数据、下载尝试和为什么值得补全文 |

`阅读状态` 只说明“读到哪里”；`证据等级` 说明“能支撑多强的 paper claim”。快速结论卡片必须同时包含这两个字段，避免把题摘粗筛、全文文本核验和 PDF 图表核对混成同一证据层级。受控 `证据等级` 如下：

| 证据等级 | 适用条件 | 写作边界 |
|---|---|---|
| `题摘级` | 只读题名、摘要、元数据 | 只能写候选相关性，不能支撑方法/实验强对比 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文，但未逐页看 PDF 图表 | 可写方法、实验、结果的文本级总结；涉及表格/图形具体数值时须标注待核对 |
| `PDF图表级` | 已人工打开 PDF 核对关键图表、表格、公式或版式 | 可支撑图表/表格级细节，但仍需记录核对日期和位置 |
| `全文不可得` | PDF 未获取或无法合法访问 | 只能保留下载需求和题摘级判断 |

如果一篇论文只是粗略 review，必须在快速结论卡片和 SUMMARY 中如实标注；如果已经全文阅读，也必须写清楚阅读入口和范围，避免后续把不同证据等级混在一起。

每篇全文 review 至少包含以下章节，顺序保持稳定，便于后续汇总脚本和人工阅读：

1. **快速结论卡片**：用一个紧凑表格给出标题、年份、分层、阅读状态、证据等级、核验入口、输入、输出、方法形态、覆盖阶段、评价强度、审计强度、对 paper2 的作用。
2. **D1-D7 全文核验评分**：emoji 单值列 + 每维中文理由 + 证据锚点；明确哪些评分相对粗筛发生变化。
3. **论文解决的问题与背景**：说明原文为什么认为该问题重要，以及与 SLR/SMS/evidence synthesis 的关系。
4. **方法 / 系统拆解**：必须写清输入、输出、阶段、LLM/agent 角色、prompt/RAG/检索/抽取/编码/生成模块、人机交互与异常处理。
5. **实验 / 评价设计**：整理 RQ、数据集或案例、baseline、指标、设置、人工标注/专家评审、统计方式；若没有实验，要明确写出。
6. **主要结果与结论**：只写原文能支持的结果；数字必须来自正文、表格或图，不确定时写“原文未给出明确数值”。
7. **局限与可复现性**：记录代码/数据/提示词是否可得、样本规模、领域限制、模型漂移、人工标注风险、arXiv 未审稿风险。
8. **对 paper2 的具体影响**：指出它威胁或支撑 paper2 的哪类 claim，以及 paper2 必须如何差异化。
9. **可用于写作的引用角度**：给出 2--4 条中文 Related Work 句子草稿或定位语，但不能写 unsupported novelty。
10. **待复核清单**：列出仍需人工看 PDF 图表、补 DOI/venue、下载代码、复核实验数字等事项。

### 6.2 证据锚点写法

推荐格式：

- `paper_content.txt §Abstract / Page 1`：中文转述证据。
- `paper_content.txt §Method / Page 3--5`：中文转述系统阶段。
- `paper_content.txt Table 1 / Page 6`：中文转述指标或结果。

如果 `paper_content.txt` 没有保留章节名或页码，就写关键词定位，例如：`paper_content.txt 中 “Evaluation” 附近段落`。不要把无法定位的记忆写成事实。

## 7. SUMMARY 回填规则

更新 [SUMMARY.md](./SUMMARY.md) 时必须同步：

1. 当前候选总数、本地建库数、P0/P1/P2 数量、全文核验数量、PDF 图表级核对数量、人工下载数量。
2. **主表不能只有 D1-D7**。主表必须同时包含描述性维度，让读者不打开单篇 `review.md` 也能直观看到每篇论文状况。
3. 主表最低字段：年份、分层、标题、venue/状态、阅读状态、证据等级、输入、输出、覆盖阶段、方法/系统形态、人审/审计机制、实验/指标、主要发现、D1-D7、对 paper2 的作用、本地链接。
4. 推荐增强字段：是否同行评审、line of work、citation role、LLM/agent 角色、provenance 粒度、实验对象/数据集、gold/reference、baselines/metrics、代码/数据/提示词可得性、威胁的 paper2 claim、支持的 paper2 claim、claims to avoid、差异化要求。
5. 若 GitHub 单张表过宽，可拆成“主表 A：方法事实与证据等级”和“主表 B：D1-D7 与 claim 影响”，但两张表必须覆盖同一批本地条目，并都保留标题到单篇 `review.md` 的相对链接。
6. 以下字段缺失应按 I 级学术风险处理：阅读状态 / 证据等级、venue/状态、输入、输出、覆盖阶段、方法/系统形态、人审/审计机制、provenance 粒度或其缺失说明、实验对象/指标、主要发现、D1-D7、威胁的 paper2 claim 或对 paper2 的作用、本地证据入口。
7. 分组总结必须覆盖：多 agent / agentic SLR workflow、human audit / provenance、screening / corpus filtration、survey generation / review composition、SE 场景近邻、evaluation benchmark / prompt reproducibility。
8. P2 若已建本地目录，应进入主表或背景表，并说明为什么不是 P0/P1。
9. CCF coverage / gap 与人工下载入口必须保留，不能把 coverage gap 写成负证据。
10. `SUMMARY.md` 应给出总体定调结论：哪些 claim 必须禁用，哪些 claim 可以保守保留，后续实验必须补哪些证据。

### 7.1 字段命名风险

1. 避免在主表使用单列 `初步判断` 承载所有信息；它会混淆题摘粗筛与全文结论。应拆为 `主要发现`、`对 paper2 的作用`、`差异化要求`。
2. 避免只写 `核验阶段`；应写成 `阅读状态` + `证据等级`。
3. D6 的正式含义是 `SE / 目标 venue 相关性`，不能把 arXiv 或非同行评审工作写成 CCF / peer-reviewed 事实。
4. P0/P1/P2 表示 novelty 威胁强度，不等同“可复现实验 baseline”或“正式发表等级”。

## 8. 验证与验收

每轮提交前至少运行：

```bash
source venv/bin/activate
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/papers')
missing = []
for d in sorted(p for p in base.iterdir() if p.is_dir()):
    for name in ['paper.pdf', 'paper_content.txt', 'bibtex.bib', 'review.md']:
        if not (d / name).exists():
            missing.append(f'{d}/{name}')
print('missing=', missing)
raise SystemExit(1 if missing else 0)
PY

git diff --check
```

全文强化 PR 还必须检查：

1. `review.md` 是否包含快速结论卡片、D1-D7、方法、实验、结果、局限、paper2 影响。
2. `SUMMARY.md` 主表是否包含输入、输出、方法、阶段、审计、实验、发现等描述性列。
3. 是否仍有“粗筛”“待全文核验”字样残留在已全文阅读的核心 P0/P1 条目里；若有，必须解释原因。
4. 是否存在“首次性 / 完整覆盖 / PRISMA 合规”等未经证据支撑的强 claim。

如果 reviewer 要求 dry-run，至少选 1 个 P0、1 个 P1、1 个 P2 场景，检查是否能从 README → GUIDE → SUMMARY → search → paper dir 找到证据链。

## 9. 写作禁令

- 不得写“本文是首次自动化 SLR / 首次 agentic SLR”。
- 不得把 PRISMA 风格 / PRISMA 启发式提示写成 PRISMA 合规。
- 不得把 title-level CCF 未命中写成完整负证据。
- 不得把 arXiv 论文写成 peer-reviewed / CCF 事实。
- 不得把粗筛 `review.md` 当成最终 Related Work；正式写作必须回到 PDF / `paper_content.txt` 核验。
- 不得为了让 story 显得强而降低 baseline 的相关性；强近邻必须正面承认并差异化。
