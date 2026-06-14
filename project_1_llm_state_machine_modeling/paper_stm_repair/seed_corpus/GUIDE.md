# strict seed 文库工作指南

## 1. 工作边界

本指南约束 PR-R1.5 / PR-R1.6 / PR-R1.7 的 seed 文献调研和文库建设。所有结论必须服务于第一篇论文的 `<NL, STM_0> -> STM_k / Better STM` 任务，不得把 `NL -> STM` 初始生成重新包装成论文主贡献，也不得把 `fcstm` / `pyfcstm` / DSL 当成贡献点。

本目录使用双层口径：

1. **seed 方法 / 来源集合层**：记录上游 `NL / text -> STM_0` 的论文、artifact、pipeline、人工方法、protocol-domain 方法、paper-only 方法和 fallback 来源。只要能解释 `STM_0` 从何而来，就应入账并标清证据与局限。
2. **PR-R2 四例样本计数层**：只从方法集合中筛出可冻结、可复验、泄漏可控、领域边界可接受的 `yes-main / yes-conditional` 条目。`计数资格` 只表示 R2 样本计数资格，不能用来判断一个条目是否属于 seed 方法集合。

## 2. 检索策略

### 2.1 数据源

必须覆盖：

- 本地：`baselines/`、`sources/`、`reproduction/results/`、project_ex1 reviewer corpus、PR #73/#82/#92/#94 线索。
- 外部：Semantic Scholar、arXiv、OpenAlex、IEEE Xplore、ACM Digital Library、DBLP、publisher 页面；必要时记录 Google Scholar / 手工网页检索线索。
- snowballing：对 `SS-A? / SS-B? / ES-C?` 候选执行至少一轮 references / cited-by 追踪；无法访问时记录 blocker。

### 2.2 关键词簇

推荐从以下 query cluster 起步，记录实际检索式、日期、source、top-k / page cap、命中、去重、失败与早停理由：

1. `natural language requirements state machine generation`
2. `use case statechart generation`
3. `scenario to state machine synthesis`
4. `textual requirements UML state machine`
5. `requirements to finite state machine`
6. `natural language to statechart`
7. `LLM state machine modeling requirements`
8. `end-user scenarios state machine synthesis`
9. `structured textual requirements executable state machine`
10. `control system requirements finite state machine`

## 3. 筛查流程

1. title / abstract 初筛：只决定是否进入全文，不得标 `SS-A`。
2. fulltext 核验：读取 PDF / `paper_content.txt`，确认输入、输出、生成关系和排除码。
3. artifact 核验：查代码、dataset、demo、结果输出、license、URL 稳定性。
4. 单篇编码：写 `seed_desc.md` 与 `artifacts.md`，并回填矩阵。
5. reviewer 复查：对 `SS-A/SS-B/ES-C` 与边界负例做事实复核。

## 4. SS/SA 双轴

| 轴 | 等级 | 用途 |
|---|---|---|
| strict seed literature eligibility | `SS-A` / `SS-B` / `ES-C` / `NN-D` / `EX-E` / `pending` | 文献是否满足 strict seed 定义。 |
| seed artifact usability | `SA-1` / `SA-2` / `SA-3` / `SA-4` / `SA-5` | artifact 是否可进入可复验实验样本。 |

`SS-A + SA-1/SA-2` 是 PR-R2 主 seed 的必要条件；`SS-B + SA-1/SA-2` 只有在生成关系清楚、T0 边界清楚且 artifact 可隔离时，才可作为条件主候选。正式统计还必须检查 `candidate_matrix.md` 的 `计数资格`：只有 `yes-main` / `yes-conditional` 计入当前主 / 条件主候选；`SA-3/SA-4/SA-5` 只能作为文献证据或 related work。注意：`SA-3/SA-4/SA-5` 不计四例，并不等于不属于 seed 方法集合。含 `after` / timeout / timed automata / hybrid dynamics 的候选不得默认计入主 seed，除非后续完成 case-level T0 isolation 或在 PR-R3 中冻结可审计的时间语义规范化策略。

## 5. 单论文目录规范

每个进入全文核验的候选建议建立：

```text
papers/<paper-slug>/
├── paper.pdf
├── paper_content.txt
├── bibtex.bib
├── seed_desc.md
└── artifacts.md
```

生成 / 重写单篇文件时必须遵循：`bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> seed_desc.md / artifacts.md`。

## 6. 人工下载队列

无法自动下载 PDF / artifact 的条目写入 [manual_download_queue.md](./manual_download_queue.md)，使用 Markdown 表格 + BibTeX 代码块。不要把它当正式 `references.bib`。

## 7. agent 纪律

- 批次筛查 agent 只能给候选与初筛，不写最终 `SS-A`。
- 单篇全文 agent 原则上一篇一 agent，必须记录输入、输出、失败和证据指针。
- 审稿 agent 复查事实性错误、排除码误收、SS/SA 混淆和过强 claim。
- 所有 agent 禁止 sub-subagent。
- [agent_provenance.md](./agent_provenance.md) 仅记录本目录内与文献筛查、全文阅读、证据等级判断直接相关的审计细账；跨 PR / issue 的执行进度、review 状态、ready gate 和 merge 进度以 GitHub PR / issue body 与 comment 为准，不在仓库内另建动态流程总账。

## 8. R1.6 / R1.7 补充纪律

1. `candidate_matrix.md` 与 `screening_ledger.md` 必须 ID 一一对应；新增候选不得只进入一边。
2. `search_log.md` 只写摘要；每轮检索细节写入 [search_rounds/](./search_rounds/) 并保持 append-only。
3. 新增或升级为主 / 条件主候选时，必须同步更新 [seed_selection_candidates.md](./seed_selection_candidates.md)。
4. `SS-B + SA-2` 只能作为条件候选，必须写明生成关系、T0 边界、artifact 可隔离性与 caveat。
5. pipeline 可复跑但 outputs 未冻结的候选（如 `fsm-bench-20`）不得直接计入已生成 `STM_0` 四例下限。
6. 旧九个 direct baseline 必须通过 [baseline_seed_method_crosswalk.md](./baseline_seed_method_crosswalk.md) 入账；crosswalk 中每个 seed 方法必须能在 [candidate_matrix.md](./candidate_matrix.md) 与 [screening_ledger.md](./screening_ledger.md) 中找到对应 ID 或显式 alias。
7. 不得因为 paper-only、private-data、protocol-domain、pipeline-output-missing 或 `sources/` fallback 就静默删除方法层条目；只能在 `计数资格`、SS/SA、后续角色和 caveat 中降级。

## 9. 研究快照最低门

当前 bounded snapshot 的长期复核门：原则上不少于 `20` 条去重候选进入 title / abstract ledger，不少于 `8` 条进入 fulltext / artifact 核验，并显式统计 `SS-A/SS-B + SA-1/SA-2 + 计数资格=yes-main/yes-conditional` 可计主 / 条件主候选数量。`>=4` 只表示可交接后续四例样本冻结的候选池达到最低裁决起点，不等于四例已经冻结；`>=6` 是广域检索希望达到的更稳健缓冲目标。若未达到 `>=6`，只能以“bounded snapshot + negative evidence + fallback handoff”作为后续样本冻结前置资料：明确当前可计候选数量、缺口原因、后续补足路径，不得声称已具备四例冻结输入或全域穷尽。`SA-3/SA-4/SA-5` 只能作为文献证据 / related work。最终只能声称“当前 bounded snapshot”，不得写成全域 census。

额外 crosswalk 完成门：旧九个 direct baseline 必须达到 `9/9` 方法层覆盖；若某条不在 `candidate_matrix.md` / `screening_ledger.md`，必须在 [baseline_seed_method_crosswalk.md](./baseline_seed_method_crosswalk.md) 写明 alias、排除理由和不进入矩阵的原因。默认不允许“因为不计四例所以不入账”。

## 10. R1.7 补充纪律

1. R1.7 新增/重判候选必须同时进入 [candidate_matrix.md](./candidate_matrix.md) 与 [screening_ledger.md](./screening_ledger.md)，并显式记录 `P0..P3` priority。
2. `search_results/r17_*.jsonl` 只是 raw evidence，必须由 [search_rounds/](./search_rounds/) 的 `round-r17-*.md` 解释后才能作为验收证据。
3. R1.7 新增 `SA-3` paper-only strict/conditional 论文不得计入 PR-R2 主 / 条件主 seed 数量。
4. 若 R1.7 未把可计数主 / 条件主候选提升到 `>=6`，必须在 [seed_selection_candidates.md](./seed_selection_candidates.md) 写出 negative evidence 与 fallback。
