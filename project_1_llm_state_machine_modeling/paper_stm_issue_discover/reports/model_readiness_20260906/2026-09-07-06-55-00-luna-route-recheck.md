# Luna：baseline 单次成功与生成路由复核

核验日期：2026-09-07 06:39 至 06:51 CST，07:07 追加同配置复查。此报告补充[四模型交接快照](./2026-09-07-06-12-00-four-model-handoff.md)中 Luna 的渠道状态。旧六次 baseline 503、旧 ZIP、v61/A1 和历史 method/judge 不覆盖。此次只有接入探针，没有新 method cell 或 judge cell，不进入效果统计。正文引用键对应文末审计附录。[clm-scope]

## 1. 新证据

同一最终 `gpt-5.6-luna` profile 在 06:39 的真实 stream baseline 成功：pair 0001、round 1、one worker、零 transport retries；record 为 `ok`，请求与观测 model 均为 `gpt-5.6-luna`，4956 input / 214 output，其中 reasoning 0，9.57s。真实 HTTP 参数为 `max_output_tokens=128000`，终态为 `response.completed`，`incomplete_details=null`。provider `created_at` 对应本次请求发出约 3 秒后，不是用历史 baseline 产物代替新调用。[clm-baseline]

随后普通生成和当前 method 使用的共用 structured runtime 仍返回 503，因此**不能将一次 baseline 成功解释为整个生成渠道已经恢复**。目前缺少这些失败之后对应路径恢复可用的证据；这是 provider 路由的接入缺口，不是模型能力评价。[clm-route]

| 时间 CST | 路径 | HTTP / 终态 | 耗时 |
|---|---|---|---:|
| 06:39:54 | 最终 profile / baseline / stream function tool | 200；完整 baseline `ok`、usage 齐全 | 9.57s |
| 06:43:16 | `utils.llm.create_chat_model` / async stream 普通生成 | 503；InternalServerError | 2.15s |
| 06:46:49 | 同一普通生成请求复查 | 503；InternalServerError | 2.12s |
| 06:49:20 | 原生 HTTP/SSE，复用第一次普通生成的完整 payload | 503；无生成 usage | 1.44s |
| 06:51:29 | `PublicStructuredRuntime` / stream function tool | 503；单次 provider failure，runtime 正常关闭 | 1.47s |

五个 HTTP 请求均使用原 profile、stream 和 128000 输出上限，无人为小额 override。普通生成的 adapter 与原生 HTTP payload hash 完全相同，比较中只改变客户端与 HTTP 封装；不能将这个 503 仅归因于 LangChain。structured runtime 探针使用已在 E1 用过的 pump/interlock 接入 fixture，保留完整 messages/schema/tool_choice；它不是 method cell，也没有修改方法。该探针只有一次调用，没有 schema 修正失败或整格重试。[clm-route]

离线 baseline 审计器此前假设所有 SSE `delta` 都是对象；Responses 的增量可以是字符串，导致统计脚本抛出 `AttributeError`。仅对审计器增加字典类型判断后，成功调用由原始字节复算，无需重跑 provider；生产 runtime、prompt、schema 与 validator 均未改变。[clm-audit]

07:07:39 CST 另做一次零重试的普通 stream 生成复查，源码为 `fe8713bd2f8911a0d0fa5c19d2a2d5cc89b3ccf8`。profile fingerprint 和完整 request body 均与前述普通生成一致，仍在 1.99s 返回 HTTP 503，正文为 `Service temporarily unavailable`；没有生成 usage 或 SSE 内容。该条记录独立保存，未覆盖五请求 ZIP。它确认此时同一渠道缺口仍存在，不支持宣布恢复。[src-final-gate] [clm-route]

## 2. 交接含义

Luna 最终 profile 的 baseline 覆盖得到补齐，历史完整 stream method 的复用依据仍见前一报告；但当前共用 runtime 探针和普通生成的 503 仍须保留为接入缺口。需要对应路由恢复后核对 stream/tool、模型身份、usage 和 finish，再判断当前配置是否可交接。不得以这次单条成功替换失败记录，也不得将失败归类成模型不支持 stream。[clm-route]

Sonnet/Qwen/Muse 的既有验收没有配置变化，本次不重跑它们、不扩展候选。优先四款及 judge/A1/A2 固定 Luna 的边界不变；不合并、不启动 E2/O2。动态退出门状态由 GitHub #204/#179 维护。[clm-scope]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告 | `fe8713bd2` | `fe8713bd2` | 运行源码 `93d4d1db4c6f68ac5a1b8c5295f630d667f55d7b`；新增 baseline 成功与四个路由失败 | 本次追加 07:07 复查，运行源码 `fe8713bd2`；无迁移 | 本节 ZIP 与独立 final-gate JSON，不改旧证据包 |

### A.2 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 关键锚点与用途 |
|---|---|---|---|---|
| [src-route] | luna_routes | [luna-route-diagnostics.zip](./evidence/luna_route_20260907/luna-route-diagnostics.zip) | json/body/log | `baseline/{probe.json,artifacts/record.json,call_metadata/wire/}`、`checks/{plain-api,plain-api-recheck,native-same-plain,runtime-tool}/` |
| [src-hash] | luna_manifest | [manifest.json](./evidence/luna_route_20260907/manifest.json) | json | 35 个成员，原始/脱敏 SHA-256、privacy policy；内嵌原 run hash 不重签 |
| [src-privacy] | luna_privacy | [privacy-scan.json](./evidence/luna_route_20260907/privacy-scan.json) | json | 独立扫描 35 个成员，敏感值匹配 0；JSON/JSONL 可解析 |
| [src-final-gate] | luna_final_recheck | [final-gate-recheck.json](./evidence/luna_route_20260907/final-gate-recheck.json) | json | 07:07 单请求的原始 request/response 文本、wire 时间、源码/profile、源文件 hash；当前及历史配置敏感值扫描 0 |
| [src-scripts] | probes_and_audit | [ZIP](./evidence/luna_route_20260907/luna-route-diagnostics.zip) | source | `scripts/` 中的 baseline、普通生成、原生 HTTP、runtime 探针与修正后的离线审计器 |
| [src-prior] | prior_handoff | [交接报告](./2026-09-07-06-12-00-four-model-handoff.md) | md/zip | 四款完整配置、此前失败、历史 Luna method 复用与其他三款验收 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 / 限制 |
|---|---|---|---|---|---|---|
| [clm-baseline] | E1-LUNA-BASELINE-RESTORED | 最终 baseline 单次成功、usage/finish/model/wire cap 齐全 | trace/count | [src-route] baseline record、SSE response.completed | [cmd-route] | high；不代表所有路径或持续 SLA |
| [clm-route] | E1-LUNA-ROUTE-PARTIAL | 同 profile 后续四次 503，原生同 payload 也失败；07:07 复查仍 503 | risk/count | [src-route] checks、payload hash、runtime outcome.attempts；[src-final-gate] 同请求复查 | [cmd-route] | high；不能仅归因 SDK，也不能判模型能力差 |
| [clm-audit] | E1-LUNA-AUDIT-DELTA | 仅离线审计器适配 Responses 字符串 delta | trace | [src-scripts] `e1-ready-baseline-audit.py`；原始成功响应未重跑 | [cmd-route]；对照脚本 | high；未修改生产方法或重写原件 |
| [clm-scope] | E1-LUNA-SCOPE | 新旧记录分离；无 method/judge 重跑或模型名单扩展 | prohibition | [src-scripts] 启动参数、runtime record；[src-prior] | [cmd-route]；人工对照指令 | high；不是 E2 结果 |

### A.4 复验命令

[cmd-route] 仓库根离线执行，不调用 provider：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_luna_route_evidence.py
```

该命令核对成员 hash、实际 wire cap/stream、baseline record 与原始 SSE usage/finish、四个 503、同 payload hash，以及 runtime 的 provider 错误归属和正常关闭；另核验 07:07 JSON 的请求一致性、profile、预算、原始错误与隐私扫描。原始五请求在脱敏 ZIP，追加请求在独立 JSON，敏感配置不入库。
