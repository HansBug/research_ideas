# E1：模型最大输出、stream 大输入与独立环境验收

冻结时间：2026-09-07 03:36:18 CST。正文的 `[src-*]`、`[clm-*]`、`[cmd-*]` 引用文末审计附录。本报告是接入诊断快照，不是缺陷发现效果实验；不计算 hit、precision，也不进入 E2 主结果。15 格均为预先指定的 `0029 / 0019 / 0049`、round 1、stream、3 workers、0 transport retries，无候选 judge。[src-protocol] [clm-cells]

## 结论与选型建议

建议商业组合为 **GPT-5.6 Luna + Claude Sonnet 5**，开放组合按用户决定采用 **Qwen3.8-27B + Muse Glimmer 30B**。Sonnet 和 Haiku 新三格均没有 provider 失败，Sonnet 的节点内结构修正更少；Haiku 保留为较低价备选。Gemini 3.8 在本轮渠道仍出现 11 次 504，因而不作为当前优先商业交接对象。这是有限接入证据下的工程建议，不是模型能力排名，E2 尚需独立冻结实验协议。[clm-choice]

15 格都按现有 method 规则 eligible，其中 5 格为 `completed_with_diagnostics`。Qwen 三格均 `completed`、0 errors；Muse 的 0049、Sonnet/Haiku 的 0029、Gemini 的 0029/0049 保留真实降级。**eligible 不代表所有阶段成功，也不等于候选全面健康。** 结构错误和网关缺口没有通过修改 method、prompt、validator 或 eligibility 消除。[clm-cells] [clm-limits]

## 输出预算与配置身份

用户最新授权取消统一 10K 上限。`3901b0561` 使真实 shared runtime 采用 profile 预算，修复 Responses 别名覆盖并记录真实请求限制、finish/incomplete；`75b590306` 增加明确的 `remaining_context` 模式。旧 10K fixture 常量不再是实际 method 调用的默认上限。原始旧预算 run、v61/A1 及历史 judge/method 均不改写，新配置独立编号。[clm-budget]

| profile / 精确请求模型 ID | profile context | 允许输出来源与真实 HTTP 参数 | 本轮推理/采样 |
|---|---:|---|---|
| `gpt-5.6-luna` / 同名 | 1,050,000 | 128,000；Responses 映射经离线 wire 回归 | 保留历史 stream；本轮未重跑 Luna method |
| `gateway-b-gemini-3.8-native` / `gemini-3.8-flash` | 1,048,576 | `generationConfig.maxOutputTokens=65536` | 未传 thinking/采样控制，provider default；不能记 think-off |
| `claude-sonnet-5` / 同名 | 1,000,000 | `max_tokens=128000`，Models API 核实 | 未传 thinking/采样控制，provider default |
| `claude-haiku-4-5` / `claude-haiku-4-5-20251001` | 200,000 | `max_tokens=64000`，Models API 核实 | 未传 thinking/采样控制，provider default |
| `e1-qwen38-27b` / `qwen3.8-27b` | 1,000,000 | 声明上界 1,000,000；省略输出字段，SGLang 按剩余 context | 服务端模板默认 `reasoning_effort=low`；method 请求未覆盖 |
| `e1-muse30b` / `muse-glimmer-30b` | 131,072 | 声明上界 131,072；省略输出字段，SGLang 按剩余 context | 官方模板默认 high；function/tool；method 使用模型默认采样 |

上述官方规格入口为 [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna)、[Sonnet](https://platform.claude.com/docs/en/models/sonnet-5/overview)、[Haiku](https://platform.claude.com/docs/en/models/haiku-4-5/overview)、[Gemini](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)、[Qwen](https://huggingface.co/Qwen/Qwen3.8-27B)、[Muse](https://huggingface.co/meta-models/Muse-Glimmer-30B)。网关回报的 ID 不构成上游身份的独立认证。profile 指纹、官方来源快照和 API 模型回执在证据包中；私有配置不入库。[src-budget] [clm-budget]

开放模型没有额外独立的“整窗输出加完整输入”空间。已核实 SGLang 0.5.19 将省略字段传为 `max_new_tokens=None`，当前源码派生上界为 `context_length - prompt_tokens - 2`，另受 KV 页准入和正值环境限额约束；Qwen 当前进程没有环境输出小上限。两个保留位置分别来自 worker 和 scheduler。原准备笔记的单保留位置简写保留原件，由 `serving-output-derivation.json` 单独更正。输入 auto-truncate=false，实际 method compact_count=0。该推导是部署源码证据，不伪装为 provider 返回的 effective-cap 字段。[clm-budget]

`stage.context_budget.max_output_tokens` 仍表示 profile 声明值；开放模型逐请求的可用输出必须结合原始 `prompt_tokens` 和 serving 推导解释，不能把它当作额外允许生成 1M/131K tokens。阶段 `provider_input_tokens` 可能累加多次修订请求，也不能当作单次最大输入。逐调用 HTTP、原始 usage 和 finish 才是本次审计依据。[clm-budget]

## 15 格实际结果

表中“完成”是 `completed`，“降级”是 `completed_with_diagnostics`；括号为 errors 数。所有格 eligible=true、audit errors=0，每格 8 个阶段回执均保留。[clm-cells]

| 模型 | 0029 | 0019 | 0049 | 三格总耗时 | 模型调用 / 正常响应 | 节点内 schema 修正 |
|---|---|---|---|---:|---:|---:|
| Gemini 3.8 native | 降级 (2) | 完成 (0) | 降级 (2) | 630.40s | 41 / 30 | 11 |
| Sonnet 5 | 降级 (1) | 完成 (0) | 完成 (0) | 617.72s | 24 / 24 | 7 |
| Haiku 4.5 | 降级 (1) | 完成 (0) | 完成 (0) | 795.97s | 28 / 28 | 12 |
| Qwen3.8-27B | 完成 (0) | 完成 (0) | 完成 (0) | 1,140.05s | 26 / 26 | 7 |
| Muse Glimmer 30B | 完成 (0) | 完成 (0) | 降级 (1) | 683.44s | 21 / 21 | 7 |

| 模型 | run ID | 精确源码 commit |
|---|---|---|
| Gemini | `560bfe6078334293a16335bbe6200225` | `3901b0561ae0b0a2dcdab655b1455c0a7a047e83` |
| Sonnet | `b88d3d28d5c342d9bab366b2bbff1942` | `3901b0561ae0b0a2dcdab655b1455c0a7a047e83` |
| Haiku | `5f4d1d8675e1476999bfbb72d61a31c0` | `3901b0561ae0b0a2dcdab655b1455c0a7a047e83` |
| Qwen | `bd02ea1ee61a43e7ac4341db210a05fd` | `aee59710cdbd4205b24a35bae05b227f13fe76d6` |
| Muse | `cd647b2ff7ae4730af8eed98e6de97b6` | `75b590306c9a931e3a09e66926ae840373d39e46` |

Sonnet 0029 的 D 结构请求已返回并解析，后续证据校验仍有缺少 exact `defeater_evidence_ref`、`strongest_defeater` 的条目，修订后按既有规则降级。Haiku 0029 的 D 输出出现 `decisions` 不是列表、条目缺 `basis`/`reason`，六次调用配额内未收敛。Muse 0049 的 D 连续缺顶层 `reason`/`basis`，后续又出现多包一层 `arguments`、`decisions` 字符串化；六次结构修正耗尽。实际 wire 中对应字段的约束仍在，不能靠放松 validator 或额外增加配额抹去限制。[clm-limits]

Gemini 0029/0049 分别在 grounding 和 D 阶段保留 provider 504 errors；另有中途 504 后恢复的调用，所以 11 次 provider 失败与 4 条最终 cell errors 不是同一分母。三个模型的降级都留下产物和回执，未冷启动整格重试挑结果。[clm-limits]

## 逐调用输出与 stream 证据

| 模型 | 有正常响应及 usage | 最大单次 input | 最大单次 output | provider 正常结束 | 最晚首 SSE |
|---|---:|---:|---:|---|---:|
| Gemini | 30/30；11 个 504 无 usage | 103,136 | 25,458 | 30 STOP | 61.22s |
| Sonnet | 24/24 | 111,527 | 21,302 | 24 tool_use | 3.93s |
| Haiku | 28/28 | 89,993 | 34,798 | 28 tool_use | 4.63s |
| Qwen | 26/26 | 78,465 | 34,919 | 26 tool_calls | 65.95s |
| Muse | 21/21 | 68,412 | 15,212 | 21 tool_calls | 67.14s |

新预算正常响应没有 `length`/`MAX_TOKENS`；这是本轮观察结果，不新增“中途零截断”eligibility 门槛。每调用保留原始请求体、响应体/SSE、chunk 时间、请求 SHA-256、provider finish/incomplete、normalized 和 raw usage。Qwen/Muse 的原始 `usage.reasoning_tokens` 是 `completion_tokens` 的组成部分，LangChain 未放进 normalized details 时仍可从 raw 回执读取；不能把缺字段当作零，更不能重复相加。Gemini 保留 `candidatesTokenCount`、`thoughtsTokenCount` 与归一化值，网关 token 计量和身份限制没有因这次成功消失。Claude 未返回独立 reasoning token 数，记为不可得。[clm-calls]

Sonnet/Haiku 原始 SSE 为 gzip。初始旁路观察器错误地按 UTF-8 解码，但 SDK 正常完成；已从原始字节和时间戳离线重建 24/28 个响应，gzip EOF 均完整。原始压缩响应、初始观察错误、解码后的事件均保留，未为观测器问题重跑模型。观察器只记录传输，不修改请求或方法。[clm-calls]

## 独立环境、容量与并发

两模型使用各自 conda prefix，Python 3.12.14、SGLang 0.5.19、PyTorch 2.13.0、Transformers 5.12.1、FlashInfer 0.6.18、NVCC 13.3.73、CUDA runtime 13.3.29。仅 GPU 4-7、TP4，`mem-fraction-static=0.92`、`max-running-requests=64`；权重和缓存仍在指定共享存储。Qwen revision 为 `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`，Muse 为 `a4e59da52a7bc87ae7251dd5545c0dd437c44b68`。普通生成/推理控制的既有独立环境证据保留，本轮重新确认正式 profile、`/models`、tool/usage 和长请求。[src-serving] [clm-load]

下表为迁移后、新预算、stream 的**非 warmup** 请求。并发负载与单请求容量分开测试；0.9 原生窗口和官方扩展分别列行。[clm-load]

| 模型 / 场景 | 实际输入 tokens | 并发 | 有效请求 | p95 延迟 | requests/s |
|---|---:|---:|---:|---:|---:|
| Qwen / 约 16K 工具负载 | 16,369 | 16 | 32/32 | 16.11s | 1.293 |
| Qwen / 原生 262,144 的约 0.9 | 236,005 | 1 | 2/2 | 13.40s | 0.075 |
| Qwen / 1M YaRN 的约 0.9 | 900,037 | 1 | 2/2 | 84.69s | 0.012 |
| Muse / 约 16K high/tool 负载 | 16,410 | 16 | 32/32 | 18.27s | 1.134 |
| Muse / 原生 131,072 的约 0.9 | 118,375 | 1 | 2/2 | 9.10s | 0.111 |

全部列示负载均无 transport/schema/truncation/字面占位符失败。Qwen 两个容量长度档都使用最终 1M YaRN 部署；原生行表示按 262,144 原生窗口目标长度复验，不是另启无 YaRN 的性能对照。16K sweep 的短生成不代表 16 个完整多阶段 method 或 16 个最大窗口同时驻留；0.9 padding 探针验证输入容量，不证明跨全文的推理准确率。预热、prefix cache、排队状态和输出长度均影响延迟，不将小样本数字宣传为持续 SLA。共享盘快照约余 5.47 TB，本机归档前约余 35 GB；本机仅运行客户端和 tunnel。[clm-load]

## 同请求三层对照与超时定位

共享等待配置为首字节/读取空闲 300s、单次模型调用 600s、零 transport retries 时 stage 3,630s、外层 3,660s。三个商业候选的新 method 均使用这套 stream 配置。旧 30 秒 ReadTimeout 不能推断为模型不支持 stream；Gemini 约一分钟的网关 HTTP 504 不受本地等待上调控制。[clm-stream]

| 请求 / 层级 | 首 SSE | 首内容或工具参数 | 流结束 | 原始结果 |
|---|---:|---:|---:|---|
| Qwen 旧 0001 / adapter+tunnel | 65.37s | 123.58s | 128.00s | 10K length、JSON 不完整；后续节点内修正单列 |
| 同请求 / native+tunnel | 0.94s | 33.20s | 42.37s | tool_calls、schema 合法、usage |
| 同请求 / 远端 loopback | 0.21s | 42.23s | 51.33s | tool_calls、schema 合法、usage |
| Muse 新 0029 / adapter+tunnel | 67.14s | 176.61s | 176.73s | tool_calls、schema 合法、usage |
| 同请求 / native+tunnel | 0.96s | 71.45s | 71.53s | tool_calls、schema 合法、usage |
| 同请求 / 远端 loopback | 0.26s | 107.25s | 107.30s | tool_calls、usage；schema 不合法 |

Qwen 三层首请求业务 payload SHA-256 均为 `4577de628e6e97a12815d635639eb06de86a12dca055871fe2c9e3de4417f22f`；Muse 均为 `4a5f046f57d399348fe50408379c495afc4c1dfd0ee5d6179423521054399dd8`。地址和鉴权封装之外保留 messages、tools、tool_choice、预算与推理设置。Muse 远端返回 `contracts` 类型错误并缺两个必填字段，不能写成三层 schema 全通过。其 chunk 间隔最大约 78.09 秒说明“已连通”后也可能长时间没有增量；延长 read-idle 有实际依据。不同请求次序/缓存状态不允许据此把耗时差全部归因于 tunnel。[clm-stream]

## 保留限制与 E2 交接

Qwen 旧 10K 轮 49 个响应中 43 次 length，三个大格不 eligible；本轮新预算三格全部完成，两个配置不能混算。Muse 初次把 131,072 整窗作为额外输出显式请求，24 次预检 HTTP 400，run `986d646987614065902dada0f563816c` 保留；修正为经核验的剩余窗口模式后才运行本报告的 Muse run。Qwen 另有一次协议修改未提交导致的启动前拦截，无 API 调用；也不写成模型失败。旧 Gemini nonstream/stream 失败同样保留。[clm-history]

推荐组合具备进入 E2 协议讨论的工程证据，但 Muse D 结构修正耗尽和 Sonnet D 证据降级须原样交接；它们不是“无错误健康证明”。Gemini 的 schema/canary 和网关 504、Haiku 的 D 结构错误维持备选限制。未取得可核验价卡的自托管/Gemini成本不具资格，0 USD 不表示免费。价格仅用于工程选择，来源仍见 09-06 商用调查，不进入论文成本贡献。[clm-choice] [clm-limits]

交接须冻结各 backbone 的 profile、实际推理档、预算模式、依赖/权重 revision 和服务参数，并为每个 backbone 配对运行 baseline/ours。两开放 profile 共用一个 tunnel 端口，必须在确认本服务无在途/排队后顺序切换，以 `/v1/models` 核验新身份再启动对应客户端；不能同时向两个 profile 发请求并假定它们是两套服务。judge 与 A1/A2 始终 Luna。本次不启动 E2/O2，不因已有 smoke 自动冻结商业选型或重跑历史样本。[clm-handoff]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告（新建） | 本次归档提交，可由 `git log --diff-filter=A` 定位 | 本次归档提交 | 09-07 15 格与迁移负载完成后冻结；运行源码分别为 `3901b0561`、`75b590306`、`aee59710c` | 无迁移 | 下列 ZIP 的 cells/serving/comparisons |

### A.2 上游事实源清单

所有 ZIP member 路径相对 [stream-diagnostics.zip](./evidence/stream_20260907/stream-diagnostics.zip)，逐 member 原始/脱敏 hash 见 [manifest.json](./evidence/stream_20260907/manifest.json)。公开包共 2,558 个成员，对凭据、私有端点、地址、用户名、路径和 opaque provider state 脱敏；原件保留，内嵌原始 run hash 不重签。[独立隐私扫描](./evidence/stream_20260907/privacy-scan.json)检查当前及预算变更前后的私有配置值，剩余匹配为 0，JSON/JSONL 均可解析。

| 引用键 | source_id | 事实源 | 类型 | 用途 / 关键锚点 |
|---|---|---|---|---|
| [src-protocol] | e1_protocol | [protocol.md](./protocol.md) | md | 最后两项用户 amendment、15 格、GPU/stream/语义边界 |
| [src-cells] | large_cells | [ZIP](./evidence/stream_20260907/stream-diagnostics.zip) | zip/json/jsonl | `cells/*model-max*/probe.json`、`artifacts/<run>/method/<pair>/round-1.json`、`summary-audit.json`；选择本报告五个 run ID |
| [src-wire] | raw_transport | [ZIP](./evidence/stream_20260907/stream-diagnostics.zip) | zip/body/json | `cells/<profile>-<variant>/call_metadata/wire/<call_id>/<request>/` 的 request/response、metadata、原始与 decoded SSE |
| [src-budget] | output_budget | [ZIP](./evidence/stream_20260907/stream-diagnostics.zip) | zip/json/source-code | `model_max/profile-budget-audit.json`、`remaining-context-profiles.json`、`claude-model-metadata.json`、`serving-output-derivation.json`、`sources/` |
| [src-serving] | isolated_serving | [ZIP](./evidence/stream_20260907/stream-diagnostics.zip) | zip/json/jsonl | `serving/{qwen38,muse}/model-max/*/{requests.jsonl,summary.json}`、`*remaining*/active-server-snapshot.json`、`scripts/e1-large-cells-start-server.sh`；原普通生成/控制另见 [09-06 环境报告](./2026-09-06-isolated-env-final-verification.md) |
| [src-comparison] | same_request | [ZIP](./evidence/stream_20260907/stream-diagnostics.zip) | zip/json/body | `comparisons/{qwen38-failed-0001,muse-large-0029-model-max}/comparison.json` 与三层原始请求/响应 |
| [src-source] | frozen_semantics | `3901b0561`、`75b590306`、`aee59710c` | git-commit | utils 参数/transport 修复；method 目录相对 `2971a8ada` 无 diff |
| [src-prices] | commercial_survey | [09-06 商用报告](./2026-09-06-11-53-00-commercial-models.md) | md | 官方价格来源及版本口径，不采用其旧施工状态作为本轮结果 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 / 限制 |
|---|---|---|---|---|---|---|
| [clm-budget] | E1-STREAM-BUDGET | 无统一小上限；商业 wire 匹配 profile，开放使用完整输入后的剩余窗口 | trace | [src-budget]、[src-wire] 请求输出字段、[src-source] | [cmd-verify] | high；开放有效上界是源码推导，非新增 provider 字段 |
| [clm-cells] | E1-STREAM-CELLS | 15 格 eligible、5 格降级、各格 errors 与修正数 | count | [src-cells] 指定 run、`/eligible`、`/errors`、`/stage_receipts`、`/llm_calls` | [cmd-verify] | high；不是完整阶段成功率或方法效果 |
| [clm-calls] | E1-STREAM-CALLS | 逐调用 output/usage/finish 与 gzip 还原 | count | [src-wire]、`summary-audit.json#/calls` | [cmd-verify]；人工检查 raw usage | high；未暴露的 reasoning 分项不可推断为零 |
| [clm-load] | E1-STREAM-LOAD | 两模型迁移后 16-worker 和 0.9 窗口通过 | count | [src-serving] 非 warmup 请求、模型/窗口/并发过滤 | [cmd-verify] | high；仅对应记录负载，非持续 SLA |
| [clm-stream] | E1-STREAM-LAYERS | 三层同请求 stream 可达，超时/缓冲和 schema 分开判断 | classification | [src-comparison] 第一请求 hash、时间、finish、schema 字段 | [cmd-verify] | high；顺序执行不能分离 cache 和链路耗时 |
| [clm-limits] | E1-STREAM-LIMITS | provider、D 结构/证据降级和计量缺口保留 | risk | [src-cells] Gemini/Haiku/Muse/Sonnet 对应失败 stage、[src-wire] | [cmd-verify]；人工复核字段错误 | high；未以改变研究语义换取通过 |
| [clm-choice] | E1-STREAM-CHOICE | 推荐 Luna+Sonnet、Qwen+Muse，Haiku 备选 | decision | [clm-cells]、[clm-load]、[clm-limits]、[src-prices]、用户开放选型 | 人工复验工程限制与价格偏好 | medium；三格是接入样本，不构成能力排名或最终 E2 冻结 |
| [clm-history] | E1-STREAM-HISTORY | 旧预算、失败和启动前拦截不覆盖 | trace | [src-cells] 全部旧 variant；新 run ID 分离 | [cmd-verify]；对照 source hash | high；新旧配置不等价 |
| [clm-handoff] | E1-STREAM-HANDOFF | 共端口需身份切换；E2/O2、judge/A1/A2 边界 | prohibition | [src-protocol]、[src-serving] port/model、[src-cells] candidate_judge_calls | [cmd-verify] | high；服务驻留状态以远端实时检查为准 |

### A.4 复验命令

[cmd-verify] 从仓库根运行，仅离线读归档，不调用 provider：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_stream_evidence.py
git diff 2971a8ada aee59710c -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/method
```

首条核验 member hash、15 格回执、请求输出参数、stage 无截断、provider finish 与 usage、三层首请求 hash，并从逐请求记录复算五组新预算负载。第二条应无输出。预算及 adapter 修复的 utils 回归为 256 passed；本报告与公开包验证不重跑真实 API。
