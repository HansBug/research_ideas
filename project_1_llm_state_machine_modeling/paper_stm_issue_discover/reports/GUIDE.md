# reports/GUIDE.md — 研究报告维护规范

本文件约束 `paper_stm_issue_discover/reports/` 的 Markdown report 维护。目标是让报告能直接支撑 paper story、实验设计和 reviewer 审查，同时不把 Markdown 变成第二机器事实源。

## 1. 事实源优先级

1. 机器事实源：pipeline 中的 JSON、JSONL、ZIP、record、hash、schema 与 committed artifact。
2. 一手 corpus 事实源：seed library 的 raw / extracted assets、`seed_resource_registry.json`、`REGISTRY.md`、单篇论文路径与资源 README。
3. reports：面向人类阅读、论文 story、审查 handoff 的稳定快照。
4. redirect notice：pipeline 中旧 human-facing Markdown 只负责指向 canonical report，不保留完整结论表。

row-level canonical facts 永远以机器事实源和一手 corpus assets 为准；report 只能保存解释、摘要、风险与人类可读表格。**来源考据表只说明 report 从哪里迁移而来，不等于 claim 已经有证据链。每个 report 还必须在文末维护“审计附录：证据链与事实源”，并在正文中用稳定 ASCII citation key（如 `[src-case-matrix]`、`[clm-profile-status]`、`[cmd-profile-summary]`）引用对应事实源、claim 与复验命令。**

## 2. 文件命名硬规则

除 [README.md](./README.md)、[SUMMARY.md](./SUMMARY.md)、[GUIDE.md](./GUIDE.md) 外，每个长期 report 必须使用：

```text
yyyy-mm-dd-hh-mm-ss-short-slug.md
```

验收正则：

```text
^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*\.md$
```

时间前缀表示报告核心学术结论冻结时间，不是路径迁移时间。迁移、链接修复、Markdown lint、空白和排版不改变时间前缀。

## 3. 迁移 report 的 commit archaeology 流程

迁移旧 report 前必须逐个源文件考据：

```bash
git log --follow --date=iso -- <source-file>
git log --follow -p -- <source-file>
git blame --date=iso -- <source-file>
```

报告文末 `## 审计附录：证据链与事实源` 的 `### A.1 来源考据表` 必须给出至少如下列：

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|

`substantive fact commit` 的判定标准：diff 中新增、删除或修改正文结论句、统计数字、表格行 / 列、分类口径、抽样口径、eligibility / risk 判断，或会改变读者学术解释的说明。纯路径、链接、标题层级、空白或格式修正只能写入 `non-prefix revision/migration commit`。

## 4. 严格证据链硬规则

每个 canonical report 必须在正文之后、文件末尾维护 `## 审计附录：证据链与事实源`。审计附录至少包含 `### A.1 来源考据表`、`### A.2 上游事实源清单`、`### A.3 Claim-evidence map`、`### A.4 复验命令`。这些小节编号固定为 `A.1`–`A.4`；表内行用稳定 citation key 作为行编号。没有这些小节时，report 状态最多只能标为 🟡，不得作为论文写作的可信入口。

### 4.0 正文引用与稳定 key

1. 正文中凡出现核心数字、强结论、分类、风险判断或后续行动建议，必须在句末或表格标题处引用文末审计附录中的稳定 key。
2. citation key 必须是短 ASCII 文本，格式建议为 `[src-*]`、`[clm-*]`、`[cmd-*]`；禁止使用 `[1]` 这类数字型 citation，因为增删证据会造成大范围重编号。
3. key 一经发布默认稳定；后续新增证据只新增 key，不批量重命名旧 key。若必须废弃 key，应在审计附录保留 `deprecated / superseded_by` 说明。
4. 上游事实源清单和 Claim-evidence map 的第一列必须给出可被正文引用的 bracket key，例如 `[src-profile-case]`、`[clm-profile-status]`。
5. 复验命令必须有 `[cmd-*]` key，并在 Claim-evidence map 的 `复验命令` 列引用同一个 key。

### 4.1 上游事实源清单

`### A.2 上游事实源清单` 必须列出报告依赖的所有事实源类型，至少覆盖：

| 字段 | 要求 |
|---|---|
| `编号 / 引用键` | 稳定 bracket key，例如 `[src-case-matrix]`；正文只能引用该 key，不引用数字序号。 |
| `source_id` | 短且稳定，例如 `case_matrix`、`sweep_report`、`pairs_jsonl`。 |
| `事实源` | 指向 repo 内文件的相对路径链接；ZIP 必须写到 ZIP 文件本身。 |
| `类型` | `json` / `jsonl` / `zip` / `xlsx-derived-jsonl` / `md` / `schema` / `source-code` / `git-commit`。 |
| `用途` | 说明它支撑哪些 claim，而不是只列路径。 |
| `关键锚点` | JSON Pointer、JSONL row filter、ZIP member pattern、sheet/row/column locator、hash 字段或命令输出。 |

### 4.2 Claim-evidence map

`### A.3 Claim-evidence map` 是 report 的审计核心。每条强结论、数字、分类、风险判断、后续行动建议都必须至少有一条 map；只是引导性背景可不列，但不能把背景写成结论。

| 字段 | 要求 |
|---|---|
| `编号 / 引用键` | 稳定 bracket key，例如 `[clm-profile-status]`；正文引用该 key。 |
| `claim_id` | 稳定 ID，例如 `R5.5-PROFILE-C1`。同一 report 内不得重复。 |
| `结论 / claim` | 报告中实际要读者相信的结论。 |
| `类型` | `count` / `classification` / `decision` / `risk` / `prohibition` / `trace` / `narrative`。 |
| `上游事实源与锚点` | 至少给出路径 + JSON Pointer / row filter / ZIP member / hash / commit / command anchor。 |
| `复验命令` | 能在 repo 根目录运行的命令；如果只能人工复验，必须写 `人工复验` 与原因。 |
| `置信度` | `high` / `medium` / `low` / `unknown`；`medium` 以下必须写 caveat。 |
| `限制 / caveat` | 说明该 claim 不能外推到什么范围。 |

### 4.3 无法证明 / 无法证伪纪律

若某个说法当前无法从 committed artifact 证明或证伪，必须在 Claim-evidence map 中标为 `unknown` 或 `medium`，并在正文中显式写出：

1. 当前已证明的最强事实是什么。
2. 当前缺失的证据是什么。
3. 后续需要哪个 pipeline / probe / 人工审查补齐。
4. 该缺口是否影响主 claim；若影响，必须降级或删除主 claim。

禁止把“未在 committed evidence 中复现成功”写成“事实不存在”；也禁止把“未发现问题”写成“证明无问题”。

## 5. 报告模板

新增 report 默认使用以下骨架：

```markdown
# 报告标题

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

## 2. 核心结论

## 3. 证据表 / 分析

## 4. 学术风险与禁止主张

## 5. 后续入口

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|

> 本节只说明 report 的迁移与冻结来源，不替代下面的 claim-evidence map。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|

### A.4 复验命令
```

## 6. 与 pipeline 的同步纪律

1. report 中的完整派生表必须由 canonical JSON/JSONL 生成或能被脚本复算。
2. 修改 report 表格后必须确认 machine source 未变，或同步更新 machine source。
3. `run-llms-emp-profile` 当前只生成 [../pipeline/readiness_audit/llms_emp_profile/](../pipeline/readiness_audit/llms_emp_profile/) 下的 machine artifacts 与 redirect notice；canonical 完整阅读表保存在 [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。
4. 复验时至少确认 denominator `60 / 10`，并按 report 当前性区分旧 R5.5 快照 `16 / 41 / 3` 与 R5.5.2 当前状态 `16 / 44 / 0`；同时确认 10 cluster 表、10×6 LLM 矩阵、行为特征矩阵与 JSONL 一致。
5. report 的 Claim-evidence map 若引用 JSONL，必须用 row filter 表达清楚 denominator，例如 `nl_cluster_id=...`、`raw_pair_id=...`、`conversion_status=partial`。
6. report 若引用 ZIP archive，必须写清 ZIP 文件、member pattern 和 hash 字段；不要只说“见 archive”。
7. 正文引用不得只出现在审计附录：报告正文中的核心表格标题、结论句和风险句必须带 `[clm-*]` / `[src-*]` key，确保远程阅读时能直接跳到文末证据链。

## 7. 迁移旧 pipeline Markdown 的规则

旧 pipeline human-facing report 迁移后只能保留 redirect / migration notice：

- 指向本目录 canonical report。
- 指向 canonical machine source。
- 不保留完整结论表、cluster 表、LLM 矩阵或 blocked/partial 明细。

例外：若某个 `pipeline/**/reports/*_summary.md` 是 CLI / pytest 合同明确生成的 machine-adjacent convenience summary（例如转换器 smoke summary），可以保留为工具输出摘要，但必须同时满足：

1. 文件开头明确写出它不是 canonical human-facing report，不是论文写作事实源。
2. 完整结论、学术解释和跨阶段判断必须回到本目录 canonical report 或对应 JSON/JSONL/ZIP。
3. 下游 dry-run / fixture 若引用它，只能把它当作工具运行上下文，不得把它当作 report 证据链终点。
4. 若它开始承载新的学术判断、选样决策或 paper claim，必须迁移到本目录秒级 report 并补齐来源考据、上游事实源清单和 Claim-evidence map。

## 8. SUMMARY 同步规则

以下情况必须同步更新 [SUMMARY.md](./SUMMARY.md)：

1. 新增 report。
2. 拆分 report。
3. report 被后续 report 替代。
4. machine source 路径变化。
5. report 状态从 🟡 / 🔴 变为 🟢，或反向降级。
6. report 新增、删除或重写 Claim-evidence map，且影响核心结论、置信度或 caveat。

[SUMMARY.md](./SUMMARY.md) 只维护入口、核心结论、来源 commit、证据链状态和风险，不复制完整事实表。

## 9. 禁止事项

1. 不记录 PR ready、CI 状态、merge 进度、review 已处理等动态流程信息。
2. 不把 R5/R5.5 report 写成真实 repair loop 或 `STM_k` 结果。
3. 不把 conversion / normalization / representation lowering 的收益写成 repair gain。
4. 不手工改完整表后跳过 machine-source 一致性检查。
5. 不静默删除被替代报告；应在 SUMMARY 中标注 `superseded_by`。
6. 不允许只有 Markdown 内部交叉引用而没有上游 machine/corpus evidence anchor。
7. 不允许把 `confidence=unknown` 的内容放进核心结论；只能放进风险、限制或后续工作。

## 10. dry-run 审查要求

大改本 GUIDE、报告模板或迁移规则时，reviewer 必须选 1–3 个真实 report dry-run，检查：

1. 能否从 [README.md](./README.md) 和 [SUMMARY.md](./SUMMARY.md) 找到 report 与 machine source。
2. 能否判断 source commit、prefix commit、migration commit 的含义。
3. 能否从正文 citation key 跳到文末审计附录，并从 Claim-evidence map 找到每个核心 claim 的上游路径、row filter / JSON Pointer / ZIP member / hash / command。
4. 能否复算关键统计或明确复算 blocker。
5. 能否发现 report 与 machine source 不一致时的失败判据。
6. 能否识别无法证明 / 无法证伪 claim，并确认正文已降低结论强度。

建议 dry-run 至少覆盖：一个统计型 report、一个 negative evidence report、一个 story / scope handoff report。
