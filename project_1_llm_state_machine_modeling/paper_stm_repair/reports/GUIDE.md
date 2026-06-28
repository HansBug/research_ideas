# reports/GUIDE.md — 研究报告维护规范

本文件约束 `paper_stm_repair/reports/` 的 Markdown report 维护。目标是让报告能直接支撑 paper story、实验设计和 reviewer 审查，同时不把 Markdown 变成第二机器事实源。

## 1. 事实源优先级

1. 机器事实源：pipeline 中的 JSON、JSONL、ZIP、record、hash、schema 与 committed artifact。
2. reports：面向人类阅读、论文 story、审查 handoff 的稳定快照。
3. redirect notice：pipeline 中旧 human-facing Markdown 只负责指向 canonical report，不保留完整结论表。

row-level canonical facts 永远以机器事实源为准；report 只能保存解释、摘要、风险与人类可读表格。

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

报告头部必须包含 `## 事实源与复验 / 来源考据` 小节，并给出至少如下列：

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|

`substantive fact commit` 的判定标准：diff 中新增、删除或修改正文结论句、统计数字、表格行 / 列、分类口径、抽样口径、eligibility / risk 判断，或会改变读者学术解释的说明。纯路径、链接、标题层级、空白或格式修正只能写入 `non-prefix revision/migration commit`。

## 4. 报告模板

新增 report 默认使用以下骨架：

```markdown
# 报告标题

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|

## 1. 定位与问题

## 2. 核心结论

## 3. 证据表 / 分析

## 4. 学术风险与禁止主张

## 5. 后续入口
```

## 5. 与 pipeline 的同步纪律

1. report 中的完整派生表必须由 canonical JSON/JSONL 生成或能被脚本复算。
2. 修改 report 表格后必须确认 machine source 未变，或同步更新 machine source。
3. `run-llms-emp-profile` 当前只生成 [../pipeline/readiness_audit/llms_emp_profile/](../pipeline/readiness_audit/llms_emp_profile/) 下的 machine artifacts 与 redirect notice；canonical 完整阅读表保存在 [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。
4. 复验时至少确认 60 / 10 / 16 / 41 / 3，以及 10 cluster 表、10×6 LLM 矩阵、行为特征矩阵与 JSONL 一致。

## 6. 迁移旧 pipeline Markdown 的规则

旧 pipeline human-facing report 迁移后只能保留 redirect / migration notice：

- 指向本目录 canonical report。
- 指向 canonical machine source。
- 不保留完整结论表、cluster 表、LLM 矩阵或 blocked/partial 明细。

## 7. SUMMARY 同步规则

以下情况必须同步更新 [SUMMARY.md](./SUMMARY.md)：

1. 新增 report。
2. 拆分 report。
3. report 被后续 report 替代。
4. machine source 路径变化。
5. report 状态从 🟡 / 🔴 变为 🟢，或反向降级。

[SUMMARY.md](./SUMMARY.md) 只维护入口、核心结论、来源 commit 和风险，不复制完整事实表。

## 8. 禁止事项

1. 不记录 PR ready、CI 状态、merge 进度、review 已处理等动态流程信息。
2. 不把 R5/R5.5 report 写成真实 repair loop 或 `STM_k` 结果。
3. 不把 conversion / normalization / representation lowering 的收益写成 repair gain。
4. 不手工改完整表后跳过 machine-source 一致性检查。
5. 不静默删除被替代报告；应在 SUMMARY 中标注 `superseded_by`。

## 9. dry-run 审查要求

大改本 GUIDE、报告模板或迁移规则时，reviewer 必须选 1–3 个真实 report dry-run，检查：

1. 能否从 [README.md](./README.md) 和 [SUMMARY.md](./SUMMARY.md) 找到 report 与 machine source。
2. 能否判断 source commit、prefix commit、migration commit 的含义。
3. 能否复算关键统计或明确复算 blocker。
4. 能否发现 report 与 machine source 不一致时的失败判据。
