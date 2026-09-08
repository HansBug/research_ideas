# E2 三模型双臂全量结果（2026-09-08）

本报告对应事前登记的 [E2 协议](../discover_matrix/docs/generations/e2_20260907/preregistered.md) 和 [E2 紧凑归档](../final_results/e2_20260907/README.md)。实验新增 Claude Sonnet 5、Qwen3.8-27B、Muse Glimmer-30B 三个 backbone；每个 backbone 的 baseline/ours 均为 54 个 pair、3 个 round，即 324 个唯一格，合计 972 格。Luna 不新生成，历史 v61 的 324 个裁定只读复用。

## 结果

下表的 `K/N/I`、precision 和 hit 均由归档中的 145 条台账离线复算。`hit@1` 是三轮 expected-round 命中比例，`hit@3` 是至少一轮命中，`hit@all` 是三轮全部命中；N 是台账外有效报告数，不是独立缺陷数。百分比保留两位小数，不能跨不同 judge 协议或历史代次直接合并。

| backbone | arm | reports | K/N/I | precision | hit@1 | hit@3 | hit@all |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Claude Sonnet 5 | ours | 823 | 536/183/104 | 87.36% | 66.90% | 84.14% | 47.59% |
| Claude Sonnet 5 | baseline | 715 | 340/151/224 | 68.67% | 55.40% | 75.86% | 33.10% |
| Qwen3.8-27B | ours | 958 | 599/256/103 | 89.25% | 71.49% | 86.21% | 55.86% |
| Qwen3.8-27B | baseline | 455 | 247/122/86 | 81.10% | 51.72% | 65.52% | 36.55% |
| Muse Glimmer-30B | ours | 910 | 544/229/137 | 84.95% | 74.02% | 85.52% | 60.69% |
| Muse Glimmer-30B | baseline | 681 | 347/184/150 | 77.97% | 56.78% | 65.52% | 47.59% |

配对差值（ours - baseline，百分点）为：Sonnet precision +18.69、hit@1 +11.49、hit@3 +8.28、hit@all +14.48；Qwen 分别 +8.15、+19.77、+20.69、+19.31；Muse 分别 +6.97、+17.24、+20.00、+13.10。完整 L0/L1/L2、严格 D1/D2、九簇 bootstrap、逐簇留出和 gained/lost 明细见各模型 `statistics.json`，不按报告条数给模型排序。

## 执行与裁定

- 三个模型的生成均保持冻结 method/prompt/schema/validator/eligibility 语义；method 使用 stream、最多 16 workers。开放模型使用独立远程 conda 环境和 GPU 4–7，原始输入未裁剪。
- 所有新增裁定固定 `gpt-5.6-luna`、sub2api、stream、既有两读/仲裁和 24,000 请求预算；prompt、schema、参数和定向修复未改变。Sonnet/Qwen 先完成的裁定批次保留原并发；Muse 首六格使用原批次并发，剩余 318 格改为单一 8-worker judge 池。不存在多个池叠加。
- 归档核对每格全部阶段、报告/expected 集合、来源 hash、两读/仲裁、usage 审计和最终状态；正常证据降级不被抹除，零发现也不作为基础设施失败。离线入口：

  ```bash
  python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --check-counterexamples
  ```

  该命令不调用 API；2026-09-08 已验证三模型 324 格、归档 hash、算术和 14 个损坏反例。

## 已知限制与恢复

- Sonnet 的 `ours/0057:r1` 保留一个 `tool_not_allowed` 的 behavior-consequence 诊断，格本身完成并完成裁定；baseline `0000:r3` 的成功重试缺少启动元数据，未用邻近批次填补。
- Qwen 的原始 `ours/0009:r3` 流失败回执保留，独立恢复格按同一唯一键选入；另有 3 个 D 阶段未闭合义务，按 `completed_with_diagnostics` 计入而非删失。异步 ours 的 120 秒静默流边界只在隔离恢复使用 300 秒，baseline 同步调用没有该异步计时器；judge 设置未变。
- Muse 的 `0005:r3` 曾发生一次 600 秒整请求取消，后续既有传输恢复完成同一 payload；一次 observer 清理缺陷造成 40 个后续流的直接 wire-call 映射不完整，但原生调用回执和格裁定不变。Muse 的 910 份 ours 报告中保留正常证据统计，原始失败不覆盖。
- 三个模型的 normalized usage 仍遵循 provider 口径：reasoning tokens 已包含在 completion/output 中，不重复相加；完整原始 usage、失败调用和 provider 状态位于本地 runs 及远端备份，紧凑归档只保存可复核决策与 hash。

## 证据边界与后续交接

`final_results/e2_20260907/{sonnet,qwen,muse}/` 分别提供 `cells.json`、`verification.json`、`statistics.json` 和 `evidence.json`；根目录提供输入快照、历史 Luna hash、来源/备份摘要和归档 manifest。原始 prompt、SSE、请求响应和大型备份没有进入 Git，仍在本地 ignored runs 及 `/nfs/paper1-e1-20260906/e2-backups/`，需要另行取得才能逐条重放；fresh clone 不能声称带有全部原始审计。

逐格可查阅的生成与裁定 JSON 已随归档保存在 [`final_results/e2_20260907/raw/`](../final_results/e2_20260907/raw/)：三模型各 324 格的 `source` 与 `judge_source` 原件共 1944 个文件、1,666,325,086 bytes，manifest 提供逐文件 hash。该目录不含 wire/SSE、`call_metadata/llm` 或私有配置；因此 fresh clone 可审阅逐格结构化记录，但不能在没有本地受限原件和凭据的情况下重放每一次网络调用。

本轮只完成 E2 三模型全量裁定与复算，不启动 O2，也不新增候选 judge。后续若冻结 E2 协议，应明确公开 benchmark 档位与当前生成/裁定档位的差异，并把历史 Luna、三款新增 backbone 的渠道 provenance 分开报告。
