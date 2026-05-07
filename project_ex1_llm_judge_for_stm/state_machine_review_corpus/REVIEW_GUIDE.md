# `review_extraction.md` 撰写规范

本文件用于固定 `state_machine_review_corpus/<slug>/review_extraction.md` 的当前写法、内容要求和判定逻辑。

> 进入具体论文目录前，应先阅读本论文集的 [README.md](./README.md)、[GUIDE.md](./GUIDE.md) 与 [SUMMARY.md](./SUMMARY.md)。

## 0. 与论文集级文档的关系

`review_extraction.md` 不是孤立文件，默认位于 `state_machine_review_corpus/` 论文集中。后续 AI 在生成、补写或重写 `review_extraction.md` 时，应按以下关系理解：

1. [README.md](./README.md) — 论文集为什么存在、收什么、不收什么。
2. [GUIDE.md](./GUIDE.md) — 工作流、检索、筛选、回填规则。
3. [SUMMARY.md](./SUMMARY.md) — 本论文集每篇论文的实时状态、统计与待补。
4. [REVIEW_GUIDE.md](./REVIEW_GUIDE.md)（本文件）— 单篇 `review_extraction.md` 的判定标准、结构模板、证据写法。

## 1. 目标与适用范围

`review_extraction.md` 的目标**不是**复述整篇论文（这是 `baselines/<slug>/DESC.md` 的任务），也**不是**重新做方法对照（同上）。它的唯一目标是：

> **从这篇论文中找出"对状态机 artifact 的 human expert review 数据"，并把这些数据落实成 reviewer 系统可以消费的样本。**

每一条 review_extraction.md 都必须能回答以下 5 个问题：

1. review 数据从哪取？
2. review 是谁做的？
3. review 了多少 artifact、每条评分有哪些维度、采用什么尺度？
4. review 数据如何对齐到 reviewer 系统的统一 schema？
5. 当前是否已经成功获取数据？是否已落地为 parquet / csv 等可消费格式？

## 2. 必备章节模板

```markdown
# `<slug>` review extraction

> 本篇方法分析见 [baselines/<slug>/DESC.md](../../baselines/<slug>/DESC.md)（如该篇同时是 baseline）。

## 1. 论文元信息

- **标题**：...（中英）
- **作者**：...
- **年份 / Venue**：...
- **DOI / arXiv / URL**：...
- **本篇 review 数据用途**：...（用一两句话说明这篇 review 数据为何对 reviewer 系统有价值）

## 2. review 数据获取方式

- **来源类型**：☐ 公开仓库 / ☐ 论文附录 / ☐ 论文 tables 抽取 / ☐ 作者邮件可索取 / ☐ 其它
- **入口 URL**：...
- **本地落盘路径**：...（如已下载，写 `<slug>/data/...`）
- **当前可访问性**：☐ 已下载 / ☐ 已浏览未下载 / ☐ 链接 404 / ☐ 仅论文文字声称未验证
- **首次访问时间戳**：`yyyy-mm-dd hh:mm:ss`

## 3. reviewer 资质与人数

- **reviewer 总人数**：N
- **资质**：...（领域专家 / SE 研究者 / 工程师 / 高年级学生 / 其它）
- **是否独立**：☐ 是 / ☐ 否（作者本人参与了 review）
- **是否报告 inter-rater agreement**：☐ 是（具体值：...）/ ☐ 否

## 4. review 数据 schema

### 4.1 单条 review 的字段

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `<artifact_id>` | string | ... | 状态机 artifact 标识 |
| `<reviewer_id>` | string | ... | 评审人标识 |
| `<dimension_1>` | int / float / categorical | ... | 例如 correctness 0-5 |
| `<dimension_N>` | ... | ... | ... |
| `<comment>` | string | optional | 评审意见 |

### 4.2 数据规模

- artifact 总数：N
- reviewer 总数：M
- 每个 artifact 平均被几位 reviewer 评：K
- review 总条数：N × K（或论文实际数）

### 4.3 评分聚合方式

- 论文是否提供原始评分表（每条独立）：☐ 是 / ☐ 否
- 论文公开的是聚合后的（mean / median / vote）：☐ 是 / ☐ 否
- 当前 corpus 持有的是哪一种：...

## 5. 对齐到 reviewer 统一 schema

参照 reviewer 系统 (`reproduction/expert_review/`) 当前的统一字段：

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| ... | `human_score`（0-1） | ...（如 Likert 1-5 → /5） |
| ... | `dim_correctness` | ... |
| ... | `dim_completeness` | ... |
| ... | `unsupported_claim_flag` | ... |
| ... | ... | ... |

## 6. 落盘与 parquet 化（如已完成）

- 本地数据路径：...
- parquet schema 是否对齐到 `baseline_double_green_human_review_records` schema：☐ 是 / ☐ 否
- parquet 行数：N
- 当前 reviewer benchmark 是否已能消费：☐ 是 / ☐ 否

## 7. 状态与 emoji

| Emoji | 含义 |
|---|---|
| 🟢 | 直接可用：已下载、已对齐 schema、已 parquet 化、reviewer benchmark 可消费 |
| 🟡 | 可整理：来源已确认可获取，但抽取或对齐工作未完成 |
| ⚪ | 未收获：经评估不符合三条硬条件，或数据不可获取 |
| ⏳ | 尚未提取：论文已收录但 review 数据获取尝试未启动 |

当前状态：🟢 / 🟡 / ⚪ / ⏳

## 8. 后续动作

- 已完成：...
- 待办：...
- 阻塞：...

## 9. 更新日志

- `yyyy-mm-dd hh:mm:ss` ：...
```

## 3. 字段填写规则

### 3.1 reviewer 资质判定

| 判定输入 | 资质标签 |
|---|---|
| 论文明确写"domain experts" / "industry practitioners with X+ years" | 🟢 领域专家 |
| 论文写"experienced software engineers" / "graduate SE researchers" | 🟢 SE 研究者 |
| 论文写"senior CS/SE students" / "trained students with N hours of training" | 🟡 学生（可接受） |
| 论文写"the authors evaluated" / "we manually checked" | 🔴 作者主观（降优先级） |
| 论文用 LLM-as-Judge | 🔴 不算 human review |

### 3.2 数据可获取性判定

| 状态 | 标签 |
|---|---|
| 公开仓库 + 文件可下载 + schema 清晰 | 🟢 直接可用 |
| 公开仓库但 schema 需手工对齐 | 🟡 可整理 |
| 论文附录有原始评分表（PDF / supplementary） | 🟡 可整理（需 OCR/抽取） |
| 论文 tables 中可抽取等价聚合数据 | 🟡 可整理（仅聚合数据，不是原始评分） |
| 链接 404 / 仓库不存在 / 仅论文文字声称 | ⚪ 未收获 |
| 工业专有 + 作者拒绝 + 邮件未回 | ⚪ 未收获 |

### 3.3 schema 对齐"不要做"

1. 不要把 Likert 5 分量表硬强制为连续 0-1（保留原始尺度，再映射成 normalized score 字段）。
2. 不要在 review 数据中硬塞 reviewer 系统不需要的字段（如 reviewer 个人信息、隐私字段）。
3. 不要把"作者声称的 review"无条件信任——论文中说"4 位专家 review"但实际只在 tables 中给出聚合 mean 是常见情况。

## 4. 常见错误模式

1. ❌ **把 reference / ground truth 当 review**：SysMBench 的 151 个 human-curated reference models 是输入 ground truth，不是对 LLM 输出的 review。
2. ❌ **把自动 metric 当 human review**：HDLBits 的 testbench pass-fail / Umple 的 ICP/EUCP 都不是 human review。
3. ❌ **把 LLM-as-Judge 当 human review**：MCeT 用 LLM 做 judge 不算 human review；它的源数据 Ferrari 2024 才是含 human review 的。
4. ❌ **盲信论文文字声称的"公开"**：很多论文写"available on GitHub"但实际仓库私有、404 或缺失关键文件。

## 5. 单篇填写时的最低底线

无论具体论文写法如何，凡是写 `review_extraction.md`，至少都要满足以下底线：

1. **数据真实尝试访问**：不能只看论文文字就判断可获取；至少访问一次 URL。
2. **schema 字段真实记录**：从 paper / supplementary 中真实抽出，不能凭印象写。
3. **状态 emoji 与"§ 6 落盘"段一致**：已 parquet 化就标 🟢，没 parquet 就最多到 🟡。
4. **更新日志格式严格**：`yyyy-mm-dd hh:mm:ss`，不要简写。
