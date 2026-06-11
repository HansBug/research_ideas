# 状态机来源景观项目清单

## 1. 仓库地图

| 路径 | 作用 | 当前状态 |
|---|---|---|
| [`../`](../) | #85 论文工作区 | 本 PR 新建 |
| [`../../sources/`](../../sources/) | 控制系统论文语料与 STM 派生文件 | 规划基线：787 篇、746 正例案例 |
| [`../baselines/`](../baselines/) | #85 相关工作 / 基线初筛与下载交接 | 本 PR 新建 |
| [`../story/`](../story/) | 论文主线 / 声明-证据 / 大纲 | 本 PR 新建 |
| [`../experiment_design/`](../experiment_design/) | RQ、执行门禁、审稿风险 | 本 PR 新建 |

## 2. 当前已有证据

- `sources/SUMMARY.md` 给出 787 篇论文、746 正例案例、状态机类型 / 时间级别 / 结构标签等规划基线。
- issue #85 给出 G0--G10 硬门禁、论文主线、RQ/DQ、论文章节架构。
- issue #95 给出 CCF-A/B 综述候选 438 行、87 篇自动解析全文结构统计、438 行全文下载审计。
- 本 PR 的 [../baselines/data/screening_audit.csv](../baselines/data/screening_audit.csv) 覆盖 #95 438 行候选，并标出 69 行 #85 初筛子集。

## 3. 形成论文声明前仍缺少的输入

1. 冻结后的论文快照提交与统计复算脚本。
2. G1 后验协议审计：`PROTOCOL.md`、`INCLUSION_TRACE.csv/jsonl`、流程。
3. G2 编码可靠性：盲编码 / 双人编码、一致性 / 裁决日志。
4. P0/P1 人工全文下载与核验。
5. 7 条 `auto_fulltext_light_review_flag=yes` 候选的轻量方法节复查。
6. G0 版权安全发布包与污染检查。
