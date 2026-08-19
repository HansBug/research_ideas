# gpt-5.6-luna / gpt-5.6-terra 上游健康探针

本文记录 2026-08-19 15:44 至 16:23（Asia/Shanghai）对 `gpt-5.6-luna` 与 `gpt-5.6-terra` 的四个低成本结构化请求窗口。第一窗口每个 profile 并发发送 5 个独立请求，每个请求允许最多 3 次显式 transport retry；第二窗口分两波、每个 profile 每波 2 个请求，每请求只允许 1 次 retry；第三、第四窗口只复测 Luna，均分两波、每波 3 个请求、每请求只允许 1 次 retry。所有窗口都使用与 paper1 相同的 `DirectStructuredResponder`，关闭 SDK 隐式 retry。探针只说明对应时间窗口和当前 relay/upstream 的健康状态，不用于比较模型能力。

| Profile | 首次成功 | 最终成功 | 总 attempts | 主要失败形态 | 单请求墙钟 |
|---|---:|---:|---:|---|---|
| gpt-5.6-luna | 0/5 | 0/5 | 20 | relay HTTP 400 `Upstream request failed`、无状态码 `APIError: Upstream service temporarily unavailable`、Cloudflare 502 | 139.0–166.2 秒 |
| gpt-5.6-terra | 0/5 | 1/5 | 19 | incomplete structured stream、无状态码 upstream unavailable、Cloudflare 504 | 66.6–236.9 秒 |

第一窗口中 Luna 的 20 个 attempt 全部失败，Terra 最终成功 1/5。第二窗口表现为明显的 profile 差异：第一波 Luna 0/2（均为 Cloudflare 502），Terra 2/2；等待 20 秒后第二波 Luna 0/2（均为 relay 400 `Missing required parameter: 'tool_choice.name'`），Terra 2/2。第三窗口中 Luna 第一波 2/3 首次成功，另一个相同请求返回 `tool_choice.name` 400；等待 15 秒后的第二波又降为 0/3，第一次均为 Cloudflare 502，原地 retry 后仍为 relay `Upstream request failed`，因此第三窗口合计仅 2/6。第四窗口再次复测 Luna，两波均为 0/3：第一波从 relay `Upstream request failed` 转为 Cloudflare 502，第二波从 Cloudflare 502 转为 relay `Upstream request failed`，12 个 attempt 没有一次成功。

四个窗口共同说明：Terra 在第二窗口恢复为 4/4，但第一窗口仍有 504 与 incomplete stream；Luna 只在第三窗口短暂成功 2/6，第四窗口立即回到 0/6，当前仍是严重振荡而非稳定恢复，不适合启动全量网格。第三窗口的同一 profile、同一代码、同一请求形状在一波中同时出现 2 次成功和 1 次 `tool_choice.name` 400，排除了稳定可复现的本地 malformed request，更符合 relay 分片合同漂移；实现只对这一条结构化且精确的 receipt 做 provider compatibility retry，普通 400、schema、内容或本地错误仍不重试。paper1 的 method、feedback CLI 与 semantic judge 默认 transport retry 上限统一为 8，使用 `5/20/60/120/240` 秒退避并在更长序列中重复 240 秒；CLI 仍可按运行窗口显式调整。只有明确 provider/transport failure 且确实发生下一次原地重发时，前序 attempt 才标记 `provider_error_retry_exempt`；末次失败和其他失败照常计数。正式网格启动前应再做小批健康门：目标 profile 至少连续两波结构化请求接近全成功，且不能出现未分类的 request-contract 400。

完整逐 attempt 运行记录位于本机 `runs/paper1/provider-health-20260819/probe.json`、`probe-second-window.json`、`probe-luna-third-window.json` 与 `probe-luna-fourth-window.json`，包含配置模型、观测模型、错误类型、failure phase、retryable、billing disposition、usage、等待和墙钟；不包含 API key 或 Authorization。
