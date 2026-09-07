# Luna 新连接、Responses 错误修复与四模型接入交接

核验日期：2026-09-07；最终 method 于 11:04:32 至 11:09:59 CST 运行。正文引用键对应文末审计附录。本报告补充[四模型交接证据](./2026-09-07-06-12-00-four-model-handoff.md)，更新 Luna 当前连接的接入事实；[旧渠道 503](./2026-09-07-06-55-00-luna-route-recheck.md)、历史 method/baseline、v61/A1 和所有原始失败均保留。本次全部记录都是 E1 兼容性 smoke，`formal_result_eligible=false`，没有 judge 调用。[clm-scope]

## 1. 新连接与验收结论

用户提供的新连接已用于既有 `gpt-5.6-luna` profile；只改变 `base_url/api_key`，Luna 其余字段及另外 22 个 profile 逐项不变。根配置权限 600，registry 共 23 个 profile，`utils.llm validate` 通过。公开材料只保留配置 fingerprint、非敏感字段和差异布尔值，不收端点、凭据、完整配置或备份。四个路径的实测 fingerprint 均与最终本地 profile 相同。[clm-config]

| 路径 | source commit | 实际终态 | input / output tokens | 耗时 |
|---|---|---|---:|---:|
| 普通 API，stream | `672069f85` | `response.completed` | 1 / 1 | 2.85s |
| PublicStructuredRuntime，required function tool | `672069f85` | typed success，runtime 正常关闭 | 4500 / 106 | 24.27s |
| 原 baseline，0001/r1，stream | `672069f85` | `ok`，`response.completed` | 5118 / 183 | 16.71s |
| 当前 method，0001/r1，stream | `5cbf1442d` | 8 阶段 completed，5 个 LLM stage success | 逐调用见下表 | 327.28s |

前三项是用户转达并提供原始制品的已完成验证，经配置、wire 和终态独立复核后直接复用。普通探针的 1/1 usage 仅作存活信号，不用于性能或费用估计。baseline/structured 成功在 adapter 错误修复之前取得，最终 method 在修复之后取得；不把它们写成同一 source commit 下重跑。方法完整运行 ID 为 `3c38e4f070634aa097da075c13d285c0`，1/1 method eligible，errors/audit errors 均 0，5 次调用都有有效工具参数与 usage；无节点内 schema 修正、provider 失败或 transport 重试。[clm-probes] [clm-method]

请求和渠道回报 model ID 均为 `gpt-5.6-luna`，adapter 为 `openai-responses`。上下文声明 1,050,000、profile 最大输出 128,000；全部实际 HTTP 请求为 `stream=true, max_output_tokens=128000`，没有 10K 等小额 run override。所有成功响应均 `response.completed`、`incomplete_details=null`。这是渠道回报身份，不是独立认证的上游不可变 revision；本次没有证明最大输出可实际生成满 128K，也没有重做 Luna 容量压测。[clm-wire]

## 2. method 的逐调用与阶段核验

下表直接由归档 request/response SSE、观察器时间和 stage audit 按 `model_call_id` 对齐；离线核验器逐行对拍 Markdown。reasoning 是 output 的明细，**不能再加到 output 或 total**。五条原始 usage 的 reasoning 均为 0；最大 input 为 40,229、最大 output 为 1,950，每次 input 加请求输出额度均在声明窗口内。全部完整阶段输入无 runtime 截断，`compact_count=0`。[clm-wire] [clm-method]

| model_call_id | stage | input | output | reasoning（已含于 output） | 首 SSE，秒 | 完整响应，秒 |
|---|---|---:|---:|---:|---:|---:|
| `01a079d3-1e1c-7383-8cc2-5d333ad21953` | contract-extraction | 23785 | 1950 | 0 | 10.33 | 63.24 |
| `01a079d4-16bb-7e61-8149-8ba791edc706` | contract-completion | 29754 | 120 | 0 | 9.96 | 14.68 |
| `01a079d4-5115-7c13-889f-94570b153fea` | discovery-grounding/contract_structure_contrast | 40197 | 1389 | 0 | 19.83 | 62.00 |
| `01a079d5-44b6-7840-9070-50638e30e0de` | discovery-grounding/behavior_consequence | 40229 | 1122 | 0 | 14.36 | 44.83 |
| `01a079d6-02d4-7672-b4d2-27557233eb71` | d-adjudication | 25673 | 1003 | 0 | 98.34 | 135.03 |

8 个阶段依次为 prepare、contract_extraction、contract_completion、discovery_grounding、execute_batch、d_adjudication、validate_d、publish，均 completed。5 个谓词执行回执已落盘。D 阶段的一条 diagnostic 是 `status=completed, exceeds_budget=false` 的完整 dossier 批次记录，不是证据降级或结构耗尽；其他阶段 diagnostics 为空。method 的四个正向 eligibility reason 均保留，不能把非空 reason 列表误读成无资格。[clm-method]

本轮 method 的首字节/read idle 为 300s、单调用总 deadline 为 600s、stage deadline 为 3630s；D 的首 SSE 98.34s 在此界内，说明旧 30s 配置不能用于解释本次 stream 支持程度。baseline 的原 timeout 记录仍按它自己的 wire 保存，不套用 method 常量。未新增负载测试，也不由这个单格推断持续 SLA。[clm-wire]

## 3. 首次运行揭示的错误与修复

新连接第一次 method run `bc3c4b581bdf469ebf32c393142262e2` 在 `672069f85` 上耗时 458.02s，最终 completed/eligible、errors/audit errors 记录为 0；但原始 SSE 实际只有 **7 次 response.completed 和 1 次 response.failed**。失败 call `01a079c2-56a8-7f63-aa1d-2270344221ed` 属于 contract completion，HTTP 200 内嵌 `server_error` 和上游过载信息。旧 SDK/LangChain 路径将它忽略并归一化为空的成功输出，缺 usage；后续节点调用成功不能抹掉它。旧 audit 原样冻结，由本报告及独立 verifier 更正其解释，不伪称 8/8 健康。[clm-failure]

该旧格另有一次真正的 schema 修正：`candidates.0.predicate_inputs` 从不合法 list 修正为契约所需 dict；另有一次 D 语义修订。它们与 provider 失败分开统计。中间一次修复后启动因两份未提交报告触发既有 clean-worktree 门，1.22s 退出且未发请求；提交文档后以新目录运行上述最终格，未放松运行门。[clm-failure]

修复提交 `aa64c413fe2d95d21ba4df39551b6c57ff54a7f4` 只调整共用 adapter：在每个 Responses SDK client 的事件解码处识别 `response.failed`，抛出原生 `openai.APIError`，保留实际 HTTP 200、provider code/message，避免当作 schema 修正消耗。factory 与 AgentApp 复用同一处理，sync/async 同时覆盖；成功事件与请求参数原样交回 SDK，没有全局 monkeypatch，没有改方法、prompt、schema 或 validator。[clm-fix]

真实失败 payload 和 SSE 的离线回放复现了 provider error：同业务 payload、1 次 SDK 调用、0 次网络调用、响应正常关闭。三项定向回归通过，最终共用 utils 为 259 passed、1 remote-only skipped；该 skip 对应已在 Muse 独立远程 env 验过的 tokenizer/engine 测试，不在本机安装服务消除 skip。成功 Responses 和 incomplete 元数据由已有预算回归覆盖，修复后的真实 stream method 又验证了正常路径。[clm-fix]

这个修复修正错误分类，不能消除上游偶发过载。以后如果出现相同 provider 错误，应保留失败、按正式协议处理；不能当成模型不支持 stream，也不能把有限成功外推为网关全面健康。adapter 使用所安装 SDK 的 per-client 解码入口，SDK 升级时需重跑现有 wire 回归。[clm-failure] [clm-fix]

## 4. 四模型交接边界

| 模型 | 最终 profile 的 baseline/ours 证据 | 保留的限制 |
|---|---|---|
| Luna | 本报告的新连接 baseline 0001/r1 与最终 method 0001/r1 | 只补连接变化所需最小格；旧 503、首次 SSE 过载均保留 |
| Sonnet 5 | 既有最终 stream baseline 和 0019/0029/0049 | 0029 正常证据义务降级，1 error、0 audit errors；不是未闭合结构耗尽 |
| Qwen3.8-27B | 既有最终 stream baseline 和三大格，errors/audit errors 全 0 | 当前 low，与公开 xhigh 分开；remaining_context、TP4/1M YaRN |
| Muse Glimmer-30B | 既有最终 serving 修复后的 baseline 和三大格，errors/audit errors 全 0 | high/function-tool 路径限定；旧 schema/字段顺序反例保留 |

Sonnet/Qwen/Muse 的最终 profile 与前次归档逐字段相同，本轮直接复用，没有重跑。两个开放模型各自独立 conda、GPU 4-7、共享盘缓存与 tunnel 切换步骤沿用[完整交接报告](./2026-09-07-06-12-00-four-model-handoff.md)：约 16K/16 workers 各 32/32；Qwen 236005/900037-token 两长度目标各 2/2，Muse 118375-token 2/2。Qwen 原生长度目标是在最终 YaRN 服务上测量，不宣称另启无扩展服务对照；也不宣称 16 个最大窗口同时驻留。[clm-reuse]

公开能力与实际档位须分开：[全候选 benchmark 矩阵](./2026-09-07-04-30-00-candidate-benchmarks.md)保留 17 个已调查身份、20 个档位，未入选者和缺测也保留。本轮 Luna ordinary/baseline **省略 reasoning**，method **显式 effort=none**；两者都未指定 temperature/top_p。E2 必须决定两臂推理设置，不得把本轮接入检查当作已统一的效果协议，或以 AA max 声称当前档位达到该能力。Sonnet 默认档、Qwen low 与公开 max/xhigh 的区别也继续保留。[clm-config] [clm-reuse]

E2 仍需冻结精确模型/profile/revision、实际推理与采样、配对预算/超时/重试、输入与方法版本、裁定和 eligibility。judge/A1/A2 固定 Luna；本轮不合并、不启动 E2/O2，不补候选 judge，也不按正式 ours/baseline 的有利差值挑模型。相对 `2971a8ada`，method、baseline_arm 与 pyfcstm 对拍无变化；历史 v61/A1 及旧预算结果不改写。动态 ready/review/合流状态只在 GitHub #204/#179 维护。[clm-scope] [clm-fix]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告（新建） | 本次归档提交，`git log --diff-filter=A` 可查 | 本次归档提交 | `672069f85` 的新路由探针及首次 method；`aa64c413f` 的 adapter 修复；`5cbf1442d` 的最终真实 method | 无迁移 | 以下 recovery ZIP；新旧 run 与导出 hash 分离 |

### A.2 上游事实源清单

新包为 [luna-recovery-diagnostics.zip](./evidence/luna_recovery_20260907/luna-recovery-diagnostics.zip)，共 160 个成员；[manifest](./evidence/luna_recovery_20260907/manifest.json)同时保留原始和脱敏 SHA-256，内嵌原始 run hash 不重签。[verification.json](./evidence/luna_recovery_20260907/verification.json)由[离线核验器](./verify_luna_recovery_evidence.py)重新解析生成；[独立隐私扫描](./evidence/luna_recovery_20260907/privacy-scan.json)检查当前/旧配置、账号标识、私有 SSH 信息与文档，敏感匹配为 0。仅允许具体探针子目录、公开配置比较与复现脚本，明确排除私有连接根目录、完整配置及备份。[clm-privacy]

| 引用键 | source_id | 事实源 | 类型 | 关键锚点与用途 |
|---|---|---|---|---|
| [src-probes] | recovered_probes | 新 ZIP | json/body | `plain/`、`runtime/`、`baseline/`：record/probe、request、原始 SSE、usage 与源码 |
| [src-method] | recovered_method | 新 ZIP | json/jsonl/body | `method/artifacts/3c38e4f070634aa097da075c13d285c0/` 的 summary、method/0001/round-1、LLM result/audit；`method/call_metadata/` 与 `summary-audit.json` |
| [src-prior] | prior_failure | 新 ZIP | json/body/log | `method-prior/` 首次 run，failed call 的 `response.body` 原始 SHA `68bb863b3856e2fdcf10bea2e411c202e501a6fa535c01a37eb8c0ae6a515e4b`；`method-launch-rejected/` 无 API 请求的启动拒绝 |
| [src-config] | configuration_delta | 新 ZIP | json | `configuration/config-comparison.json`：仅两字段变化、22 profile 等式、最终四配置 fingerprint |
| [src-checks] | adapter_checks | 新 ZIP、[factory](../../../../utils/llm/model_factory.py)、[runtime](../../../../utils/agent/runtime.py)、[定向测试](../../../../tests/utils/test_responses_stream_failure.py) | json/source/git | `configuration/replayed-provider-failure.json`、`post-guard-checks.json`、`utils-regression.log`；旧 `source-boundary.json` 是修复前快照，不能作当前版本声明 |
| [src-api] | responses_events | [OpenAI Streaming Responses 指南](https://developers.openai.com/api/docs/guides/streaming-responses) | official-doc | 2026-09-07 核验 typed response.failed 事件；模型身份仍仅是渠道回报 |
| [src-reuse] | accepted_other_models | [四模型交接](./2026-09-07-06-12-00-four-model-handoff.md)、[候选 benchmark](./2026-09-07-04-30-00-candidate-benchmarks.md)、[protocol](./protocol.md) | md/zip | 最终三款配置、九格、容量/负载、D 分类、公开档位与 E2 边界 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 / 限制 |
|---|---|---|---|---|---|---|
| [clm-config] | E1-LUNA-NEW-CONFIG | 仅连接两字段改变；最终 profile 匹配；两入口 reasoning 不同 | trace | [src-config] 等式/fingerprint、[src-probes]/[src-method] request | [cmd-recovery] | high；不认证上游 revision |
| [clm-probes] | E1-LUNA-NEW-PROBES | 普通/structured/baseline 成功，前三项直接复用 | count | [src-probes] 三份终态与 usage | [cmd-recovery] | high；1/1 usage 仅存活信号，不作性能/成本证据 |
| [clm-method] | E1-LUNA-NEW-METHOD | 最终 8 阶段/5 调用完成、零 errors/audit/schema failures，D 为正常批次记录 | count/classification | [src-method] stage_receipts、LLM result、predicate receipts、raw SSE | [cmd-recovery] | high；单格兼容性，非效果结论 |
| [clm-wire] | E1-LUNA-NEW-WIRE | stream、128K 请求额度、完整 usage、无压缩截断、实际时限 | trace/count | [src-probes]/[src-method] request、SSE 与 metadata 时间 | [cmd-recovery] | high；不外推容量/持续 SLA |
| [clm-failure] | E1-LUNA-FAILED-EVENT | 首次 7 completed/1 failed，旧 audit 漏报，启动拒绝无请求 | classification | [src-prior] 原始 failed SSE、原 audit、process.log | [cmd-recovery] | high；旧产物不改写，过载仍可能发生 |
| [clm-fix] | E1-LUNA-ADAPTER-GUARD | adapter 修复正确分类，离线/真实回归通过，方法冻结 | trace | [src-checks] 失败回放、259/1 回归、冻结目录 diff；[src-api] | [cmd-recovery]、[cmd-regression] | high；SDK 升级需复验 |
| [clm-reuse] | E1-LUNA-OTHER-REUSE | 其余三款配置相同，沿用九格及开放容量/负载 | trace | [src-config] profile 对拍、[src-reuse] 两归档 | [cmd-recovery]、[cmd-handoff] | high；Sonnet 正常降级、Muse 路径限定保留 |
| [clm-privacy] | E1-LUNA-EXPORT | 160 成员哈希可复算、私有值检查零匹配 | count | manifest、privacy-scan、[src-checks] | [cmd-recovery]；私有值扫描在有配置的工作区复核 | high；脱敏不等于原始 hash 重签 |
| [clm-scope] | E1-LUNA-HANDOFF-BOUNDARY | 2+2 接入交接与正式协议分开，历史/研究语义冻结 | prohibition/decision | [src-reuse] protocol、导师 talk、[src-checks] 源码对拍 | [cmd-regression]、人工核对 E2 登记 | high；不授权 merge/E2/O2 |

### A.4 复验命令

[cmd-recovery] 从仓库根离线运行；不会调用 provider：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_luna_recovery_evidence.py
venv/bin/python -m utils.llm validate
```

[cmd-regression] 共用 adapter 及冻结边界：

```bash
venv/bin/python -m pytest tests/utils -q
git diff 2971a8ada -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/method project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm pyfcstm
```

[cmd-handoff] 未变化的三款证据及全部候选矩阵：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_handoff_evidence.py
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_benchmark_evidence.py
```

本轮真实命令的构造、observer 及 wire 脚本保存在新 ZIP 的 `scripts/`；私人路径以占位符导出，复现时映射到自己的仓库和新输出目录。运行仍须干净已推送 commit、明确 profile 与 `--allow-live --pair-id 0001 --rounds 1 --workers 1 --transport-retries 0`，不添加 `--no-stream` 或小额 output override；不能把这段复现说明当作新的全量运行授权。
