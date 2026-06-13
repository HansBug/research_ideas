# strict seed 文库总账

## 当前状态

本 PR 当前处于 PR-R1.5 初始执行阶段：已建立 seed 文库结构、strict seed 编码字段、初始本地候选矩阵和负例 sentinel。所有 `SS-A? / SS-B? / ES-C?` 仍需后续全文 agent 与 reviewer 复核，不能当作已冻结样本。

## 当前统计（bounded snapshot v0）

| 指标 | 数量 | 说明 |
|---|---:|---|
| 去重候选进入 title/abstract ledger | 27 | 来自 R1 baseline / reproduction、external planner、sources scout 与 OpenAlex 初始检索。 |
| 进入 fulltext/artifact 核验 | 10 | 本地已有 `paper_content.txt` 或 artifact 线索；其中 9 条已完成单篇 reader 全文编码。 |
| 已完成全文编码的 strict / candidate / extended 候选 | 9 | `SS-A+SA-2` 2 条；`SS-B+SA-2` 2 条；`SS-A/SS-B+SA-3` 4 条；`NN-D+SA-3` 1 条。 |
| 明确负例 sentinel | 5 | protocol、process、formal-spec、repair-only、sequence/scenario 边界均已入账，部分待全文核。 |
| 人工下载队列 | 0 | 本轮高优先本地候选均已有 PDF；外部候选下载尚未执行。 |

## 初步候选分组

当前已达到 `SS-A/SS-B + SA-1/SA-2` 的可交接 PR-R2 主 seed 候选为 4 条：`sefm-llm-state-machine`、`llms-emp-stm-subset`、`ttool-ai-smd-subset`、`designing-fsm-gpt4`。其中后两条仍带外部效度 / 修复边界 caveat，PR-R2 冻结前仍需人工裁决。


| 分组 | 候选 | 当前用途 |
|---|---|---|
| 高优先 seed / near comparison | `sefm-llm-state-machine`、`llms-emp-stm-subset` | R2 seed candidate / judge calibration。 |
| 工具格式 / converter pressure | `ttool-ai-smd-subset`、`umple-nl-state-machine`、`designing-fsm-gpt4` | R3 converter 压力与有限对照。 |
| classic scenario/use-case/statechart | `from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`scenarios-statecharts-interrelated`、`executable-state-machines-structured-text` | 扩展 strict seed 文献与 snowballing parent。 |
| hard exclusion sentinel | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel` | 校准 `X_PROTOCOL` 排除门。 |

## 关键风险

- **SA-3 不计入主 seed 可交接下限**：`SA-3` 只能作为文献证据 / related work；PR-R2 主候选下限只按 `SS-A/SS-B + SA-1/SA-2` 计算。

1. 当前 v0 主要来自本地 baseline 与 R1 台账，外部 IEEE / ACM / DBLP / publisher 检索尚未执行。
2. `sources/` 宽池只证明有大量控制系统 NL/STM 描述资源，不自动等同于 paired strict seed。
3. 多数候选仍需逐篇确认 `P3_GENERATION_RELATION`，尤其 classic scenario / use-case synthesis 可能使用形式化 scenario 而非自然语言。
4. artifact license、URL 稳定性、hash 和可再分发权利尚未冻结。

## 下一步

1. 对剩余高优先候选继续建立单篇目录并全文编码。
2. 执行 IEEE / ACM / DBLP / publisher 与 snowballing 检索，补外部候选下载队列。
3. 对 4 条可交接主 seed 候选做 reviewer 复核，确认是否足以交给 PR-R2。
4. 继续补 IEEE / ACM / DBLP / publisher 下载与 snowballing，扩展外部候选。

## 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
