# A1 no-inspect 与冻结 v61：完整结果归档

冻结日期：2026-09-06。A1 的 **54 pair × 3 round = 162 格、814 份发布报告全部裁定**；逐格报告 ID 与冻结 method 原件完全对应。对照只读引用 v61 的 162 格、903 份报告，不重跑、不改写。完整中文解释、局限和证据索引见[结果报告](../../reports/2026-09-06-19-49-18-a1-no-inspect-v61-results-cn.md)。

| 指标 | frozen v61 | A1 no-inspect |
| --- | --- | --- |
| FULL hit@1 | 323/435 | 233/435 |
| FULL hit@3 | 130/145 | 91/145 |
| FULL hit@all | 82/145 | 65/145 |
| L2 hit@1 / @3 / @all | 97/117；36/39；28/39 | 50/117；23/39；10/39 |
| K / N / I | 561 / 198 / 144 | 392 / 262 / 160 |
| report precision | 759/903 | 654/814 |

`hit@1` 是三轮 expected-round 命中率，不是第一轮或排序第一条报告的命中率；`hit@3` 是至少一轮命中，`hit@all` 是三轮均命中。N 是台账外有效报告数，不是独立新缺陷数。来源与分母遵守[事前登记及追加澄清](../../discover_matrix/docs/generations/a1_no_inspect_20260906/preregistered.md)。

## 内容与复算

| 文件 | 用途 |
| --- | --- |
| [results.json](./results.json) | 两臂逐报告冻结判定、435 个 expected-round、逐格覆盖、指标、簇级敏感性、164 条命中变化定位和输入审计摘要 |
| [source_manifest.json](./source_manifest.json) | 冻结 method selection、逐段源码与 provider/config 身份、原件 hashes、未采用的失败来源及本地细节审计 hashes |
| [archive_manifest.json](./archive_manifest.json) | 上述两个 JSON 的 SHA-256 |
| [analyze_a1.py](../../discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py) | stdlib-only、provider-free 校验与全指标复算，不重新裁定 |

从仓库根运行：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py
```

校验包括归档和 ledger hash、162 个唯一格、每格报告数与报告 ID、435 个 expected-round、FULL/PARTIAL 支持集合、全部保存指标，以及 seed=20260906 的九个 NL 簇配对 bootstrap 和逐簇留出复算。发现缺格、漏报告或数字不一致即失败。

## 来源边界

A1 method 固定为当前 12 谓词 `no-inspect`；v61 保留原 19 谓词历史身份。因此本归档是用户指定的历史对比，不冒称同版本、同 endpoint/时间的严格单因素估计。默认 full 的软件行为对拍与历史实验的可比性是不同问题。没有使用额外 full 或 provider-evaluation 的八格诊断样本。

A1 method 来源为 `f195753f` 的 111 格、`0ee98d4d` 的 8 格、`2ec6e204` 的 43 格。历史恢复及偏离如实保留；后续 judge 不改变这份冻结选择。最终 judge 为旧站点 18 格、新 `aizzz-luna-eval` 144 格；新站点正式 `0047/r1` 的旧 run 名含 probe，但输入属于已冻结正式 method，不是 provider-evaluation 样本。主批使用原生 CLI，总 worker 上限 16，轮次串行；两份补裁只处理尚无完成判定的 `0059/r1`、`0032/r2`。

两格合法 method 诊断仍保留并完整裁定，不冒充无诊断运行。自动 Luna 判定、自行审计和人工确认分开记录，**本次新结果人工确认数为 0**。相同核心文本的裁定差异、关系理由越界和 provider 恢复历史均披露，不按质量重裁。

原始 prompt、响应流、失败细节和恢复脚本留在本地 ignored `runs/paper1/a1_no_inspect_20260906/`，不进入 PR。本归档允许远端独立复算已冻结判定的算术；它不提供所有私有请求的远端重放，不声称独立语义重裁或真实 API 随机复现已完成。统计解释状态为 `ANALYZED`，离线算术另有可执行校验。
