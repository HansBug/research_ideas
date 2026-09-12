# A1-ext run record（自动汇编，`make_run_record.py`）

生成时间：2026-09-11T21:06:27+00:00。事前登记 `discover_matrix/docs/generations/a1_ext_20260911/preregistered.md`（提交 `7ef78e604`，子 PR #213，伞 PR #179 §4.8）。冻结源码 worktree `/tmp/paper1-a1-ext`，分支 `paper1/a1-ext`。事故明细见 [INCIDENTS.md](./INCIDENTS.md)。

## method runs

| 模型 | profile | run_id | workers | 状态 | 格数 | completed / with_diagnostics / failed | 起止（UTC） | 源提交 |
| :-- | :-- | :-- | --: | :-- | --: | :-- | :-- | :-- |
| Claude Sonnet 5 | claude-sonnet-5 | `10ed3f533ec44466b38e852b46006252` | 24 | completed_with_diagnostics | 162 | 122 / 40 / 0 | 2026-09-11T12:48:20Z → 2026-09-11T13:32:05Z | `7ef78e604` |
| Muse Glimmer-30B | e1-muse30b | `6ea657d77bf04d6982e38786edfd8519` | 24 | completed | 162 | 162 / 0 / 0 | 2026-09-11T12:41:28Z → 2026-09-11T13:30:13Z | `7ef78e604` |
| Qwen3.8-27B | e1-qwen38-27b | `1dc566e64c4b43bf964678f238960d78` | 24 | completed_with_diagnostics | 162 | 154 / 3 / 5 | 2026-09-11T13:55:41Z → 2026-09-11T16:38:49Z | `7ef78e604` |

失败尝试（不进入任何统计）：`method/sonnet_failed_403_attempt1/`（run `0242288dd7ff47c2a193eb93cf13f9a2`，162/162 HTTP 403，见 INCIDENTS I-1）。

## 隔离恢复格（provider 失败后按同一 profile 单格重跑一次）

| 模型 | 格 | 恢复 run 目录 | 状态 |
| :-- | :-- | :-- | :-- |
| Qwen3.8-27B | 0009-r1 | `method/qwen_recovery/0009-r1` | completed |
| Qwen3.8-27B | 0009-r2 | `method/qwen_recovery/0009-r2` | completed |
| Qwen3.8-27B | 0019-r1 | `method/qwen_recovery/0019-r1` | completed |
| Qwen3.8-27B | 0029-r1 | `method/qwen_recovery/0029-r1` | completed |
| Qwen3.8-27B | 0039-r1 | `method/qwen_recovery/0039-r1` | completed |

## judge_source 冻结

- Claude Sonnet 5：162 格，冻结于 2026-09-11T13:50:55.160144+00:00，替换 0 格（无）。
- Muse Glimmer-30B：162 格，冻结于 2026-09-11T13:35:53.932104+00:00，替换 0 格（无）。
- Qwen3.8-27B：162 格，冻结于 2026-09-11T17:38:14.186216+00:00，替换 5 格（0009/r1, 0009/r2, 0019/r1, 0029/r1, 0039/r1）；人工替换 0009/r2。

## judge runs（gpt-5.6-luna，aizzz，协议 v3.11）

| 模型 | 轮 | run_id | workers | pairs | 起止（UTC） | rc | 备注 |
| :-- | --: | :-- | --: | --: | :-- | --: | :-- |
| Claude Sonnet 5 | 1 | `dec87ac937d04526847859548f912f50` | 24 | 54 | 2026-09-11T17:39:14Z → 2026-09-11T18:05:05Z | 0 |  |
| Claude Sonnet 5 | 2 | `c29e2173c3e74a6d982d1b051d5a1f57` | 24 | 54 | 2026-09-11T18:06:15Z → 2026-09-11T18:34:25Z | 0 |  |
| Claude Sonnet 5 | 3 | `fa959dd10f0644fa84bdf2efa557076b` | 24 | 54 | 2026-09-11T18:36:17Z → 2026-09-11T19:04:59Z | 0 |  |
| Muse Glimmer-30B | 1 | `ace3c21de6f2426db880ebaf03181511` | 24 | 54 | 2026-09-11T13:35:54Z → 2026-09-11T14:30:47Z | 0 |  |
| Muse Glimmer-30B | 2 | `c387e3c643ac4db8a6add7e0bcb094a5` | 24 | 54 | 2026-09-11T14:32:43Z → 2026-09-11T15:33:24Z | 0 |  |
| Muse Glimmer-30B | 3 | `076b959315ba4d809c4591f9052b02da` | 24 | 53 | 2026-09-11T15:35:14Z → 2026-09-11T16:43:02Z | 1 | failures 1 |
| Muse Glimmer-30B | 3 | `89b5f76708474770b654c7da0ddd6252` | 1 | 1 | 2026-09-11T17:15:11Z → 2026-09-11T17:44:57Z | 0 | 重采样（原 run 的 0059 schema 死路后一次） |
| Qwen3.8-27B | 1 | `b8e05369d79241a7a0c0b94b9ea02a69` | 24 | 54 | 2026-09-11T19:06:19Z → 2026-09-11T19:45:55Z | 0 |  |
| Qwen3.8-27B | 2 | `f19ef4a5333c4172b85063b59e840dfe` | 24 | 54 | 2026-09-11T19:47:21Z → 2026-09-11T20:22:43Z | 0 |  |
| Qwen3.8-27B | 3 | `df8f1b6a6e1a4ca39f87c4e2e9469be2` | 24 | 54 | 2026-09-11T20:24:23Z → 2026-09-11T21:05:10Z | 0 |  |

已中止且不进入统计的 judge 目录：`judge/_aborted/muse-r2-duplicate-71922e9b`（INCIDENTS I-3）。

## 凭据与脱敏

凭据只在 `mktemp -d` 的 0700 目录（0600 文件 `llmconfig-a1ext.yml`），经 `LLM_CONFIG_FILE` 注入；共享 `.llmconfig.yml` 未改。本目录全部内容 gitignored。
