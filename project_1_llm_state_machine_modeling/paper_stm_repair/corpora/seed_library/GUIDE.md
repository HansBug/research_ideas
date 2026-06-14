# seed_library/GUIDE.md

## 1. 目标与边界

本 GUIDE 约束 seed library 的后续维护。seed library 只回答一个问题：哪些上游工作或来源能提供、描述或帮助构造 `<NL, STM_0>`，且其中 `STM_0` 与 `NL` 存在可追踪的生成 / 派生 / 人工建模关系。

不得把 seed library 写成本论文 repair baseline 文库；若同一工作也包含 repair / feedback / completion 环节，应在后续 `repair_baselines/` 另行登记其修正能力，并在两边交叉链接。

## 2. 分级口径

| 轴 | 等级 | 用途 |
|---|---|---|
| strict seed literature eligibility | `SS-A` / `SS-B` / `ES-C` / `NN-D` / `EX-E` / `pending` | 文献是否满足 `NL -> T0 STM-family` seed 定义。 |
| seed artifact usability | `SA-1` / `SA-2` / `SA-3` / `SA-4` / `SA-5` | artifact 是否可进入可复验实验样本。 |
| R2 计数资格 | `yes-main` / `yes-conditional` / `no-*` | 是否可进入当前 R2 四例主 / 条件主候选计数。 |

`SA-3/SA-4/SA-5` 不计四例，并不等于不属于 seed 方法集合。`fsm-bench-20` 这类 pipeline 可复跑但 generated outputs 未冻结的对象不得直接计为已有 `STM_0` 四例。

## 3. SUMMARY-first 规则

[SUMMARY.md](./SUMMARY.md) 是唯一横向事实真源。它必须直接可复算：

- candidate / screening：`47/47`；
- 单条目目录：`24 dirs`；
- 旧九 generation baseline crosswalk：`9/9`；
- R2 主 / 条件主可计候选：`4`；
- manual queue：`2 downloaded/excluded；2 excluded-by-metadata；10 still-blocked；2 new-manual-pending`。

新增条目时，不得只创建目录或只改单篇文件；必须同步更新 `SUMMARY.md` 的候选全集表、资产表、manual / negative / search / 更新日志等相关章节。

## 4. 单条目维护

生成或重写单条目派生文件时遵循：

1. 先读 `bibtex.bib` 核定元信息。
2. 再尽量完整读 `paper_content.txt`；若缺失或异常，按仓库 PDF 提取规范处理。
3. 必要时核对 `paper.pdf`。
4. 更新 `seed_desc.md`：生成关系、T0 / STM-family 边界、SS/SA、R2 角色、风险和证据指针。
5. 更新 `artifacts.md`：代码、数据、raw output、license、hash / release、manual blocker、复跑风险。
6. 回填 [SUMMARY.md](./SUMMARY.md)。

artifact-only 条目可以缺 `paper.pdf` / `paper_content.txt`，但必须有 `seed_desc.md` 与 `artifacts.md`，并在 `SUMMARY.md` 资产表中解释。

## 5. archive 使用规则

[../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/) 只保留 R1.5--R1.7 旧 ledger、search rounds 和 raw search results。archive 内旧链接按历史快照保留，可能指向迁移前的 `papers/` 或 ledger 路径；需要当前事实时必须回到 [SUMMARY.md](./SUMMARY.md) 和本目录单条目。

## 6. 禁止事项

- 禁止新增根层横向 ledger 作为第二事实源。
- 禁止把旧 generation baseline 改写成本论文 repair baseline。
- 禁止把 protocol / standard FSM、BPMN/process、Petri/CSP/Event-B/TLA+/LTL/STL、repair-only、co-exist-only、sequence/formal scenario 等误计为主 seed。
- 禁止在仓库文件中维护 PR 流程状态、review 状态、ready gate、commit / push / merge 进度。
- R1.8-B 不跑四例真实运行，不调用真实 LLM，不读取 `.env`。

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-14 17:55:00 | PR-R1.8-B 建立 seed_library 维护规则，冻结 SUMMARY-first 与 archive 边界。 |
