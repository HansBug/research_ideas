# PR-E1 Round23 Lingya valid evidence

本目录保存 PR-E1 Round23 在仓库 `.env` 的 Lingya provider 下得到的四个有效主证据 run。

## Provider / timeout 口径

- 本轮有效证据显式使用 `.env`：`LLM_ENDPOINT=https://api.lingyaai.cn/`，`LLM_MODEL=gpt-5.5`。
- 不使用 shell 中残留的旧 `deepghs` provider；此前错 provider / Cloudflare 502 结果已删除，不进入本目录。
- `path2_lng_ems` 首次 Lingya run 被本地 `LLM_REQUEST_TIMEOUT_SECONDS` 默认超时截断，已移入 `../pr_e1_real_agent_loop_round23_lingya_timeout_diagnostic/`，只作为 infrastructure diagnostic。
- 本目录中的 `path2_lng_ems` 有效结果来自同一 `.env` provider、同一代码提交、同一 `LoopConfig()`，但额外导出 `LLM_REQUEST_TIMEOUT_SECONDS=none` 以符合“Lingya 慢响应不要本地 kill”的实验口径。

## 有效主证据

| case | verdict | record | eligible | 备注 |
|---|---|---|---:|---|
| `path1_abs` | `success` | `success` | ✅ | 默认满血 `LoopConfig()`，1 iteration |
| `path1_elevator` | `success` | `success` | ✅ | 默认满血 `LoopConfig()`，1 iteration |
| `path1_cara` | `not_converged` | `rejected` | ❌ | 非 provider 故障；用于质量/repair-loop 诊断 |
| `path2_lng_ems` | `success` | `success` | ✅ | 首次 timeout 无效后，用 `LLM_REQUEST_TIMEOUT_SECONDS=none` 重跑得到有效结果 |

本目录下的 `SUMMARY.md` / `summary.json` / `pr_comment.md` 只汇总上述四个有效主证据。
