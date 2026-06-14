# seed_library — 上游 `NL -> STM_0` seed 方法 / 来源文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 seed library，服务于 `<NL, STM_0> -> STM_k / Better STM` 任务。它记录能说明 `STM_0` 从自然语言需求、用例、场景、系统描述或文本规格生成 / 派生 / 人工构造而来的上游方法与来源。

**核心边界**：seed library 不是本论文的 repair baseline，也不是 R2 四例样本集合本身。旧 `NL -> STM` generation baseline 在这里作为上游 seed 方法集合、转换压力、related work 和 R2 候选来源入账；本论文主贡献仍是后续的无人化反馈驱动修正循环。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、更新和验收规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是当前唯一横向事实真源，包含 `47/47`、`24 dirs`、旧九 `9/9` crosswalk、R2=4 handoff、manual queue、negative evidence、搜索覆盖和迁移表。
4. 进入单条目目录时，默认读取 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> seed_desc.md -> artifacts.md`；artifact-only 条目按 `seed_desc.md -> artifacts.md -> 原始 metadata / package` 顺序。
5. 需要旧 R1.5--R1.7 ledger / raw search 时，进入 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 只作审计，不是当前事实真源。

## 2. 收录范围

| 类别 | 收录口径 |
|---|---|
| 主 seed 方法 | `NL -> T0 FSM/HSM/EFSM/statechart` generation / derivation / extraction-from-NL / human modeling。 |
| 条件 seed 方法 | T0 边界、artifact、synthetic NL、license 或 leakage 需要 R2 再裁决，但生成关系清楚。 |
| 方法层证据 | paper-only、private-only、protocol-domain、pipeline-output-missing 等不能计四例但能解释上游 `STM_0` 来源的方法。 |
| negative sentinel | completion-only、protocol FSM、sequence/formal scenario、process/non-STM、co-exist-only 等防误收证据。 |

## 3. 单条目目录

每个条目目录至少应尽量包含：

```text
<slug>/
├── paper.pdf（artifact-only 可无）
├── paper_content.txt（artifact-only 可无）
├── bibtex.bib
├── seed_desc.md
└── artifacts.md
```

当前 24 个目录全部具备 `seed_desc.md` 与 `artifacts.md`；`fsm-bench-20` 是 artifact-only / pipeline fallback，缺 `paper.pdf` 与 `paper_content.txt` 属预期 caveat。

## 4. 更新纪律

- 横向事实只更新 [SUMMARY.md](./SUMMARY.md)，不得新增根层 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md`、`crosswalk.md` 等第二事实源。
- 新增 / 修改条目必须同步更新 `SUMMARY.md` 的候选表、资产表、manual queue / negative evidence / 更新日志中相关部分。
- 涉及 PR 执行计划、review 状态、ready gate、commit / push / merge 进度的信息只写 GitHub PR / issue body/comment，不写入本目录。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-14 17:55:00 | PR-R1.8-B 将旧 `seed_corpus/` 重构为 `corpora/seed_library/`，建立 README/GUIDE/SUMMARY 三件套，旧横向 ledger 与 raw search 归档。 |
