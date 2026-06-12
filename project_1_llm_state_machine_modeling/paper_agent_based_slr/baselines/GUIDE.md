# baselines/GUIDE.md：LLM-based SLR 近邻 baseline 维护规则

## 1. 目标与边界

本目录用于支撑第二篇 agent-based SLR 论文的 Related Work、novelty matrix、claim-evidence map 和评测设计。新增条目时，必须判断它是否会威胁本文如下候选贡献：

1. 将 SLR / SMS 的检索、筛选、抽取、编码、综合、报告组织为 agent 工作流。
2. 为每个阶段保存可审计证据链和 run record。
3. 把报告级 claim 绑定到论文来源、筛选决策、抽取记录和编码决策。
4. 通过 human audit gate 控制幻觉、unsupported claim 和错误证据定位。
5. 在软件工程 / LLM4SE / MDE 语境中评价该工作流。

本目录不承诺完成正式系统综述；当前 PR-B0 是 baseline discovery / triage。任何只基于 title / abstract 的判断，都必须显式标注为粗筛。

## 2. 纳入范围

优先纳入：

1. LLM-based systematic literature review / systematic mapping。
2. LLM-assisted screening、corpus filtration、data extraction、coding、evidence synthesis、review composition。
3. agentic / multi-agent literature review、survey generation、scientific knowledge synthesis。
4. human-in-the-loop evidence synthesis、provenance-aware extraction、claim-to-source traceability。
5. 软件工程、LLM4SE、MDE、empirical SE 中与 SLR/SMS 自动化直接相关的论文。

暂不纳入或降为 P2：

1. 只做普通摘要、问答、RAG 写作，没有 SLR / SMS 任务语境的工作。
2. 只研究 LLM4SE 任务本身、没有文献综述自动化流程的工作。
3. 只有宣传网页、无论文 / DOI / arXiv / 官方仓库的工具。
4. 与本文 novelty 无关的通用 survey generation 工作；除非其 agent / evaluation / citation 机制强到足以影响本文报告生成 claim。

## 3. 分层口径

| 分层 | 含义 | 处理规则 |
|---|---|---|
| P0 | 强 baseline / 直接 novelty 威胁 | 必须建立单篇目录；后续 Related Work 与 novelty matrix 必须逐段核验。 |
| P1 | 高度关注 / 局部强 baseline | 原则上建立单篇目录；至少在 SUMMARY 说明威胁的具体环节。 |
| P2 | 背景相关 / 方法参照 | 可只保留在 search 表；若后续 story 触及对应 claim，再升级建目录。 |
| PX | 排除 | 只在检索日志保留必要排除理由，不进入总表。 |

## 4. 七维评分标准

emoji 列在正式表格中只写 emoji；中文解释集中写在本节。每篇候选必须独立给出 D1-D7，不能只给一个总等级。

| 维度 | 🟢 强 | 🟡 中 | 🟠 弱 | ⚪ 无 / 背景 |
|---|---|---|---|---|
| D1 主题贴合度 | 直接研究 LLM / agent 执行 SLR、SMS、literature review 或 evidence synthesis | 研究 LLM 辅助筛选、抽取、编码、综述写作中的关键环节 | 只讨论 LLM4SE / research automation，和 SLR 关系间接 | 与 SLR / 文献综述自动化基本无关 |
| D2 SLR/SMS 流程覆盖度 | 覆盖检索、筛选、抽取、编码、综合、报告中的四个及以上环节 | 覆盖两个到三个核心环节 | 只覆盖一个环节或泛泛讨论 | 不覆盖可识别 SLR/SMS 环节 |
| D3 LLM/agent 自动化深度 | 使用 LLM / agent 执行多阶段工作流并有明确输入输出链 | 使用 LLM 辅助单阶段或少数阶段，流程较清楚 | 只做 prompt / chatbot 演示或概念性讨论 | 没有 LLM / agent 自动化实质内容 |
| D4 人工审计与可追踪性 | 明确提供 human-in-the-loop audit、claim-to-source trace、决策日志或可复核证据包 | 有人工复核或 provenance，但链条不完整 | 只提到人工检查或引用来源，缺少可执行审计设计 | 无人工审计或可追踪性机制 |
| D5 评价严谨性 | 有真实数据集、多案例、金标或人工标注、误差分类或可复现实验 | 有实验或案例，但样本、指标或复现性有限 | 只有小例子、用户研究片段或定性讨论 | 无实证评价 |
| D6 SE / CCF 相关性 | 发表在 CCF A/B/C SE/AI4SE/MDE 强相关 venue 或直接面向软件工程 SLR | 非 CCF 但与 SE / LLM4SE / MDE 强相关 | 泛 AI / 医学 / 社科综述自动化，可提供方法背景 | 与本仓库主题或目标 venue 关联弱 |
| D7 对本文 novelty 的威胁强度 | 已经覆盖 agent-based + SLR 多阶段 + audit/traceability/evaluation 的核心组合 | 覆盖其中多个关键点，需要本文明确差异化 | 只覆盖局部点，可作为 related work 背景 | 不构成 novelty 威胁 |

## 5. 检索策略

### 5.1 CCF A/B/C venue 粗筛

1. 范围以 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 和 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 当前 42 个 venue 为基线。
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

每个 P0/P1 目录至少包含：

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
4. `review.md`：必须包含元数据、D1-D7 表、中文证据转述、逐维判定理由、对本文 story 的影响、后续全文细读清单。逐维判定理由不能只写模板句；每个维度至少要有一个 title / abstract / `paper_content.txt` 页级证据锚点。
5. 单篇 `review.md` 可以使用少量原文短语，但不要复制长段英文；默认用中文转述并给出 PDF / `paper_content.txt` 链接。

## 7. SUMMARY 回填规则

更新 [SUMMARY.md](./SUMMARY.md) 时必须同步：

1. 当前候选总数、本地建库数、P0/P1/P2 数量。
2. P0/P1 七维评分总表，每行都有 D1-D7 独立评分和本地链接。
3. P2 保留表，说明为什么暂不建目录。
4. CCF coverage / gap 与人工下载入口。
5. 对后续 story / novelty / evaluation 的约束：哪些 claim 必须降级，哪些差异化必须证明。

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

如果 reviewer 要求 dry-run，至少选 1 个 P0、1 个 P1、1 个 P2 场景，检查是否能从 README → GUIDE → SUMMARY → search → paper dir 找到证据链。

## 9. 写作禁令

- 不得写“本文是 first automated SLR / first agentic SLR”。
- 不得把 PRISMA-style 写成 PRISMA-compliant。
- 不得把 title-level CCF 未命中写成完整负证据。
- 不得把 arXiv 论文写成 peer-reviewed / CCF 事实。
- 不得把粗筛 `review.md` 当成最终 Related Work；正式写作必须回到 PDF / `paper_content.txt` 核验。
