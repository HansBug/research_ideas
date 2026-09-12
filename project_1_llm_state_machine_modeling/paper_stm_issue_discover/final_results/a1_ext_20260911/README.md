# A1-ext：Sonnet / Qwen / Muse 无检视事实消融，与同模型 E2 Full 的冻结对照

冻结日期：2026-09-12（UTC 02:17:38 归档）。三个固定模型配置各 **54 pair × 3 round = 162 格，共 486 格 method、486 格 judge 全部完成裁定，pending=0**；对照只读引用 [E2](../e2_20260907/README.md) 同模型 Full ours 的 162 格，不重跑、不改写。gpt-5.6-luna 的同款对照只读引用 [A1 归档](../a1_no_inspect_vs_v61_20260906/README.md)。完整中文解释见[正式报告](../../reports/2026-09-12-10-17-38-a1-ext-three-model-no-inspect-results.md)，学术解释见[talk](../../../talks/2026-09-12-实验-A1ext三模型无检视事实消融与论文叙事.md)。

| 模型 | 条件 | 报告 R | K/N/I | 普通 precision | strict precision | hit@1 | hit@3 | hit@all | L2 hit@1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Full | 823 | 536/183/104 | 719/823（87.36%） | 650/823（78.98%） | 291/435（66.90%） | 122/145 | 69/145 | 93/117 |
| Claude Sonnet 5 | no-inspect | 536 | 280/160/96 | 440/536（82.09%） | 410/536（76.49%） | 201/435（46.21%） | 98/145 | 33/145 | 39/117 |
| Muse Glimmer-30B | Full | 910 | 544/229/137 | 773/910（84.95%） | 712/910（78.24%） | 322/435（74.02%） | 124/145 | 88/145 | 78/117 |
| Muse Glimmer-30B | no-inspect | 690 | 345/187/158 | 532/690（77.10%） | 500/690（72.46%） | 215/435（49.43%） | 92/145 | 51/145 | 28/117 |
| Qwen3.8-27B | Full | 958 | 599/256/103 | 855/958（89.25%） | 781/958（81.52%） | 311/435（71.49%） | 125/145 | 81/145 | 78/117 |
| Qwen3.8-27B | no-inspect | 738 | 386/248/104 | 634/738（85.91%） | 606/738（82.11%） | 240/435（55.17%） | 103/145 | 53/145 | 47/117 |
| gpt-5.6-luna（A1 归档） | Full v61 | 903 | 561/198/144 | 759/903（84.05%） | 678/903（75.08%） | 323/435（74.25%） | 130/145 | 82/145 | 97/117 |
| gpt-5.6-luna（A1 归档） | no-inspect | 814 | 392/262/160 | 654/814（80.34%） | 630/814（77.40%） | 233/435（53.56%） | 91/145 | 65/145 | 50/117 |

`hit@1` 是三轮 expected-round 命中数除以 435，不是首轮或首条报告；`hit@3` 为至少一轮命中除以 145，`hit@all` 为三轮均命中除以 145。普通 precision 为 `(K+N)/R`，全部发布报告进入分母；strict precision 只把有效且外部 D1/D2 的报告计入分子。N 是台账外有效报告数，不是独立新缺陷数。四模型三轮去重命中、hit@3、hit@all 与 L2 hit@1 全部下降；precision 在 Sonnet、Muse 上区间不跨零地下降，在 Qwen、Luna 上区间跨零。九簇配对区间、逐轮、分层、内容轴、候选组成与运行审计见正式报告。

## 内容与复算

| 文件 | 用途 |
| --- | --- |
| [results.json](./results.json) | 三模型两臂逐报告冻结判定、162 格来源 hash、435 个 expected-round、metrics、逐轮、内容轴、候选/证据资格组成、call audit、judge run 清单、配对比较（seed 20260906、10000 次九簇 bootstrap）、strict 区间扩展，以及 Luna A1 归档的只读指针 |
| [source_manifest.json](./source_manifest.json) | method run manifest hash、被排除的失败尝试、隔离恢复 run、judge_source MANIFEST、被中止的重复 judge 目录、975 个原件的路径/大小/SHA-256 |
| [archive_manifest.json](./archive_manifest.json) | 本目录四个文件的 SHA-256 与 ledger hash |
| [INCIDENTS.md](./INCIDENTS.md)、[RUN_RECORD.md](./RUN_RECORD.md) | 运行事故 I-1 至 I-7 与自动汇编的 run record，原样复制自本地运行目录 |
| [analyze_a1_ext.py](../../discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py) | stdlib-only、provider-free 校验与全部表格导出；不重新裁定 |
| [build_archive.py](../../discover_matrix/docs/generations/a1_ext_20260911/build_archive.py) | 从本地运行目录冻结本归档；需要 gitignored 原件，fresh clone 不可重放 |

从仓库根执行：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py --tables
python -m pytest -q project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/test_analyze_a1_ext.py
```

校验包括归档与 ledger hash、每模型每臂 162 个唯一格与 435 个 expected-round、逐格报告数与报告 ID 闭合、全部保存指标、逐轮与内容轴、配对比较与 strict 区间的逐值复算，以及 Luna 归档指针的 hash。测试含一个篡改反例：改动一条报告的有效性并刷新文件 hash，校验仍会因指标重算不一致而拒绝。

## 来源边界

三模型 no-inspect 的 method 与 judge 均运行于源提交 `7ef78e604`（含事前登记），协议、prompt、12 谓词与 ledger 与 A1 #205 相同；judge 为 `gpt-5.6-luna`、协议 `v3.11`、两读加必要仲裁、`relation_first`、`full` closure，走 aizzz 通道，与 A1 的 Luna judge 同一提供方。Full 对照来自 E2 冻结归档（Sonnet 源 `839cfb793`/`f52507d1a`，Qwen `839cfb793`，Muse `3b9068928`），运行日期、服务与随机性未与本次同步，因此这是同模型配对比较，不是严格单因素因果估计。Qwen 有 5 格在 provider 故障后按事前登记以同一 profile 单格隔离重跑一次并替换进 judge 来源，原失败回执保留；Muse r3 pair 0059 的 judge 因结构性 schema 死路以同一代码重采样一次；Sonnet 首次启动的 162 格 HTTP 403 尝试整体排除。这些偏离逐条记录在 INCIDENTS.md，不进入任何统计。自动 Luna 判定与人工确认分开记录，**本次新结果人工确认数为 0**。
