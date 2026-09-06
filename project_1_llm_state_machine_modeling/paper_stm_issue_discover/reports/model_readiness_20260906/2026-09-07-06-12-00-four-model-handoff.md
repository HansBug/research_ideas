# E1 四模型配置、结构修复与实验交接证据

核验日期：2026-09-07。正文的 `[src-*]`、`[clm-*]` 引用文末审计附录。本报告补充 [03:36 stream 快照](./2026-09-07-03-36-18-stream-model-max-acceptance.md)，保存最终 Muse serving 修复、四款 profile 的 baseline/ours 覆盖与 Luna 渠道失败；旧 run 和旧归档均保留。这里只判断接入，不计算效果排名；所有 smoke 的 `formal_result_eligible=false`。[clm-scope]

## 1. 组合与验收结论

用户优先组合为 **GPT-5.6 Luna + Claude Sonnet 5 + Qwen3.8-27B + Muse Glimmer-30B**。Sonnet 提供不同于 Luna 的商用模型族，Qwen/Muse 提供两种总参数小于 100B 的开放模型族。依据为公开任务相关能力、组合覆盖与接入可行性，不根据正式 ours/baseline 差值选模型，不主张这四款是本任务 SOTA。Haiku 保留备选，Gemini 与其余开放候选的调查和失败不删除，也不扩展部署队列。[src-bench] [clm-scope]

| 模型 | 最小 stream baseline | stream ours | 证据边界 |
|---|---|---|---|
| Luna | 历史 baseline-02 成功；最终 profile 六次补查均 HTTP 503 | 历史 0001 成功，8 阶段完成、5 个 LLM stage success，0 errors/audit errors | 同 endpoint/key/model/output，context 声明增加；历史成功不能覆盖 09-07 渠道失败 |
| Sonnet 5 | 最终 profile 0001 成功 | 0019/0029/0049 均 eligible；0029 保留正常证据降级 | 无 provider 失败或 schema 配额耗尽；0029 仍有 1 error |
| Qwen3.8-27B | 最终 profile 0001 成功 | 三格完成，errors/audit errors 全 0 | low、TP4、1M YaRN、remaining_context；不能代表公开 xhigh |
| Muse Glimmer-30B | 最终 serving adapter 下 0001 成功 | 修复后三格完成，errors/audit errors 全 0 | high、TP4、131072、remaining_context；只验收原生 function/tool 路径 |

上述状态按 baseline `record.json`、每格 8 个 stage receipts、LLM stage、errors 和 audit errors 分别核对。Sonnet 0029 的两个阶段为 `completed_with_diagnostics`，其余八格的全部阶段为 `completed`；非零的 D 诊断条数不自动等于错误或基础设施失败。[clm-method] [clm-baseline] [clm-luna]

## 2. 精确 profile、预算与推理设置

最终本地配置经 `utils.llm` 加载，23 profiles，权限 600。下表不含 endpoint 或凭据；完整公开字段和配置 fingerprint 在归档的 `ready/final-profiles.json`。托管模型只能记录请求 ID 和渠道回报身份，未取得独立认证的上游不可变 revision，不将网关名称当作这种认证。[src-config] [clm-config]

| profile | 请求 model ID | adapter / stream 结构路径 | context | 输出来源与实际请求 |
|---|---|---|---:|---|
| `gpt-5.6-luna` | `gpt-5.6-luna` | `openai-responses` / function tool | 1,050,000 | profile 128,000；HTTP `max_output_tokens=128000` |
| `claude-sonnet-5` | `claude-sonnet-5` | `anthropic` / native tool_use | 1,000,000 | Models API 核验 128,000；HTTP `max_tokens=128000` |
| `e1-qwen38-27b` | `qwen3.8-27b` | `openai` / SGLang qwen3_coder function/tool | 1,000,000 | `remaining_context`；无输出小额字段 |
| `e1-muse30b` | `muse-glimmer-30b` | `openai` / SGLang Muse ATEM function/tool + serving 约束 | 131,072 | `remaining_context`；无输出小额字段 |

开放模型的 profile `max_output_tokens` 等于部署窗口，表示经核验的模式声明，**不是额外允许生成一个完整窗口**。SGLang 0.5.19 在未提供 `max_new_tokens` 时按完整输入和实际 context/KV 页约束输出；源码推导的 context 上界为 `context_length - prompt_tokens - 2`。已核验 `allow_auto_truncate=false`，未配置环境输出小上限。真实输入不裁剪，容量与输出不能重复占用窗口。商业上限与来源保留在旧包 `model_max/` 和[规格调查](./2026-09-06-11-53-00-commercial-models.md)。[clm-budget]

| 模型 | 验收时实际推理与采样 | 与公开 benchmark 的区别 |
|---|---|---|
| Luna | 本次 baseline 请求未显式传 reasoning/temperature；渠道失败，无新生成 usage；历史 method 控制保留原件 | 不能把 AA max 行写成本次已独立认证的实际档位 |
| Sonnet | 未显式传 thinking/effort/采样，provider default；24 个大格 raw usage 均明确 `output_tokens_details.thinking_tokens=0` | 这更正了旧报告“该字段不可得”的描述；网关回报 0 不独立认证上游推理状态，也不等同 AA adaptive/max |
| Qwen | 服务默认 chat-template `reasoning_effort=low`；generation config 为 temperature 1.0、top_p 0.95、top_k 20 | AA xhigh 的 LCR/GPQA/HLE 为 82.0/90.5/33.9；AA low 为 77.3/84.5/14.0，不能混用 |
| Muse | 原生模板默认 high；generation config 为 temperature 1.0、top_p 0.95、top_k 64 | 公开 AA high 只提供能力背景；实际 revision、harness、任务不同 |

推理 token 是 output/completion 的组成部分，不重复相加。Qwen/Muse 的 raw `reasoning_tokens` 有值时，即使归一化 details 缺失也不记为 0；Sonnet 以 raw 回报的 0 记录，并明确来源。没有静默改动任何模型的验收档位。[clm-thinking]

method 使用首字节/读取空闲 300s、单次调用总时限 600s；零 transport retries 的 stage 为 3630s、外层为 3660s。六次节点内调用边界保持原样。baseline 单调用的 wire timeout 四字段均为 null，**不是**上述 structured runtime 的 300/600s；本报告记录实际值，E2 需分别冻结两条入口的等待配置。Qwen/Muse 三层同请求对照的完整 hash、SSE 时间、usage 和失败见旧 stream 报告；其中旧 30s 超时不是不支持 stream 的证据。[src-wire] [clm-timeout]

## 3. 大输入 stream method

三款各运行预先指定的 0019/0029/0049、round 1、3 workers；无 candidate judge。下表括号是 cell errors，全部 audit errors 为 0。[clm-method]

| 模型 | 0019 | 0029 | 0049 | HTTP 正常响应/调用 | schema 修正 | 三格墙钟 |
|---|---|---|---|---:|---:|---:|
| Sonnet 5 | 完成 (0) | 证据降级 (1) | 完成 (0) | 24/24 | 7 | 617.72s |
| Qwen3.8-27B | 完成 (0) | 完成 (0) | 完成 (0) | 26/26 | 7 | 1140.05s |
| Muse 最终 serving | 完成 (0) | 完成 (0) | 完成 (0) | 16/16 | 1 | 441.56s |

| 模型 | run ID | 运行源码 | 最大单次 input / output | 最晚首 SSE |
|---|---|---|---:|---:|
| Sonnet | `b88d3d28d5c342d9bab366b2bbff1942` | `3901b0561ae0b0a2dcdab655b1455c0a7a047e83` | 111527 / 21302 | 3.93s |
| Qwen | `bd02ea1ee61a43e7ac4341db210a05fd` | `aee59710cdbd4205b24a35bae05b227f13fe76d6` | 78465 / 34919 | 65.95s |
| Muse | `c992d05ed017449cb18da961fbbc4f46` | `c3f01f17a7f836bab3a0946400e06a2d48c704a8` | 67087 / 15999 | 5.07s |

三款共 66 个响应都有 usage 和正常 tool 结束；本组没有 length、上下文截断或 compact。Muse baseline 与最终三格启动有短暂重叠；模型间输入、输出和缓存状态也不同，墙钟不是严格性能对比，更不能以发现条数排名。[src-wire] [clm-method]

### Sonnet：证据降级保留

0029 的初始 D 产出有 8 个 obligation 缺 exact `defeater_evidence_ref`，一次 D 修订后 i18/i22/i3 仍缺充分 `strongest_defeater`，按现有规则保留 unresolved。该格全部 6 个 LLM stage 都为 success，结构修正已收敛；`d_adjudication` 和 `validate_d` 的回执为 `completed_with_diagnostics`。这是原方法证据义务未满足的降级，不是 provider 故障或六轮 schema 修正耗尽。缺口会影响可给出的判断，不能将 eligible 写成“所有判断完成”或抹去 1 error。[clm-sonnet-d]

### Muse：结构问题在 serving 侧修复

原 SGLang Muse parser 能解析原生 required tool，但未施加解码结构约束，旧 0049 D 连续缺顶层 `reason`/`basis`，六次修正耗尽。`b4e5ba18c` 用 XGrammar 既有 XML 参数编译器与 Muse ATEM namespace 约束参数外壳。完整三格又暴露嵌套 JSON 字段顺序过窄：合法的修订把 `binding_hints` 追加到对象末尾也被拒绝。旧语法对同一对象“schema 顺序接受、末尾追加拒绝”，不能解释成模型能力差。[src-muse-fix]

`7f1131afa` 保留顶层必填和标量约束，让嵌套 array/object 使用通用 JSON、字段顺序自由。**完整原始 schema 仍发给模型，原方法 validator 仍检查全部嵌套约束**；没有改 prompt、领域规则、修订配额或 eligibility。修复仅作用于 required/指定 function 的 serving 解码；auto 保留上游行为。固定 SGLang 0.5.19 / XGrammar 0.2.1，版本变化必须重新验通。[src-code] [clm-muse-fix]

原失败修订请求 SHA-256 `77976fceb097818c4b7b3ae8eafcf048045d8405aadd4d168c74d73cfbec9d5b` 实测通过：30 contracts 保留，21 个 endpoint contracts 的 source/target hints 齐全，经原 `NLContractResponse.model_validate` 通过，148.47s。远程原生 tokenizer/grammar/stream parser 定向测试通过。最终三格共 15 个 LLM stage 全 success，唯一 schema 修正是 0019 首次 extraction 的 5 个嵌套字段错误，一次修订后收敛；D 不再耗尽。[clm-muse-fix]

旧 `cd647...` 的 D 耗尽、`c81cf6c526b24785816ac29313774b56` 的 0049 extraction 失败、v1/v2 反例和 dirty-tree 启动前拦截均保留。最终成功不覆盖这些失败，也不宣称任意 schema、auto tool 或 JSON response-format 全面健康。[clm-history]

## 4. baseline、Luna 复用与渠道限制

baseline 补测统一 pair 0001、round 1、one worker、stream、zero transport retries，使用原 `baseline_arm/src/runner.py`。Sonnet/Qwen 原最终 profile baseline 的源码为 `72620417897ec7620880960e7b53f4527a97c74d`；Muse 在 `c3f01f17a` 下补测最终 serving 版本。[clm-baseline]

| 模型 | 选定 baseline variant | input / output | raw reasoning 分项 | 结束 / 墙钟 |
|---|---|---:|---:|---|
| Sonnet | `baseline` | 1337 / 1376 | 网关明确 0 | tool_use / 15.29s |
| Qwen | `baseline` | 839 / 1620 | 1252 | tool_calls / 11.57s |
| Muse | `baseline-schema-order-final` | 894 / 2741 | 2202 | tool_calls / 21.99s |
| Luna | 六个独立 provider 补查记录 | 无生成 usage | 不可得 | 全部 HTTP 503，未伪称完成 |

Qwen 共享盘缓存路径复核后另有 `baseline-shared-cache-final`：stream/tool/usage 成功，839 input / 1070 output，71.71s，源码仍为 `c3f01f17a`。profile、依赖和全部配置参数对拍相同；SGLang 重启自动种子从 522151049 变为 781184292，启动时间和内部运行状态另记。没有把它写成完全相同的随机推理，也不因一次冷启动耗时重跑已有三格/容量结果。[src-env] [clm-baseline]

Luna 历史 method `915ecc689ff945c185779b1e7b6fd7c5` 来自 `17ad54b05e2bd8fda0e389ef925e18a03eede82d`。配置逐字段比较显示 adapter、endpoint、凭据、model、output、模式及 pricing 相同，只有 context 声明从 272K 增到 1.05M。旧 nominal 10K 在当时 langchain-openai 1.2.2 Responses 路径被构造器的 128K 覆盖；这由隔离 wire 复现和旧 profile 支撑，**不是改写历史审计**。历史该格没有 compact。该材料说明旧成功与共用 adapter 回归的复用依据，不证明新日期的渠道可用。[src-luna] [clm-luna]

09-07 04:43 至 06:02 的六次最终 profile baseline 均在约 2 秒返回上游 503；同业务原生 Responses 请求还出现 502 / Retry-After 60，普通 Responses 与同业务 Chat Completions 也返回 503，而模型列表 200。故问题定位为渠道生成路由不可用，不能以列表成功、历史成功或错误码推断模型能力。可执行的恢复条件是该 Luna 路由恢复后，对相同最终 profile 补一次成功的 stream baseline/API 并核对身份、usage、结束原因；若换渠道则另记录配置身份与受影响复验。[clm-luna]

## 5. 独立部署与容量

仅远程 GPU 4-7、TP4，两个模型各自独立 conda prefix。Python 3.12.14、SGLang 0.5.19、PyTorch 2.13.0、Transformers 5.12.1、FlashInfer 0.6.18、NVCC 13.3.73、CUDA runtime 13.3.29；Muse XGrammar 0.2.1。conda base、系统 Python/CUDA、GPU 0-3 他人任务均不修改。完整 conda 包元数据和 pip 版本清单在新归档；共享盘约剩 5.47TB、本机约剩 35GiB 的核验快照只表示当时存储，部署前仍要实时检查。[src-env] [clm-deploy]

| 模型 | 权重 revision | context / parser |
|---|---|---|
| Qwen | `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` | 1M YaRN；qwen3 reasoning + qwen3_coder tool |
| Muse | `a4e59da52a7bc87ae7251dd5545c0dd437c44b68` | 131072；muse reasoning + muse tool/serving adapter |

容量和 16-worker 是两个测试维度，以下只列非 warmup 请求。Qwen 复用配置一致的 `model-max` 证据；Muse 使用修复后的 `schema-order-final` 证据。[clm-load]

| 模型 / 场景 | 实际输入 tokens | 并发 | 有效请求 | p95 |
|---|---:|---:|---:|---:|
| Qwen / 约 16K function/tool | 16369 | 16 | 32/32 | 16.11s |
| Qwen / 原生 262144 的约 0.9 | 236005 | 1 | 2/2 | 13.40s |
| Qwen / 官方 1M YaRN 的约 0.9 | 900037 | 1 | 2/2 | 84.69s |
| Muse / 约 16K high/function-tool | 16410 | 16 | 32/32 | 19.77s |
| Muse / 原生 131072 的约 0.9 | 118375 | 1 | 2/2 | 10.08s |

Qwen 两个长度档均在最终 1M YaRN 服务运行，原生行表示按原生窗口确定的输入目标；历史独立原生配置的记录仍在旧包。这不是无 YaRN 与 YaRN 性能比较。padding 长请求证明容量，不证明跨全文语义能力；16K 短输出工具 sweep 不表示 16 个完整 method 或 16 个最大窗口同时驻留，也不是持续 SLA。[clm-load]

### 复现入口

[serve_selected_model.sh](./serve_selected_model.sh) 固化精确权重、TP、parser、YaRN、low、64 个可运行请求和静态显存比例 0.92。Muse 同时需要仓库的 [serving_muse.py](../../../../utils/llm/serving_muse.py)。这是结合作者模型卡与本节点验通后的配置，不伪称官方未经调整的默认命令。首次创建独立 env 时，使用已有 conda 管理器在指定共享根下 `conda create --prefix <该模型独立prefix> python=3.12.14 pip`，再以该 prefix 的 Python 安装归档 `ready/<profile>-pip-lock.txt` 中的版本；禁止安装到 base/系统，也不在本机下载权重。已有通过的 env 直接复用，不重复安装。[clm-deploy]

远程复现时，`E1_SHARED_ROOT` 指向既有授权共享根，复制脚本与 Muse adapter 到该根；权重只使用表中已缓存 snapshot。脚本将 `CONDA_PREFIX`、Python、CUDA_HOME/PATH/include/runtime 限定在所选 env，显式设 `SGLANG_CACHE_DIR` 和 `CUDA_CACHE_PATH` 到共享盘，避免仅设 XDG 而被引擎忽略。它在 GPU 4-7 被占用时拒绝启动。[src-launcher]

```bash
# Only on the authorized remote node, after checking ownership and free GPU 4-7.
E1_SHARED_ROOT="$E1_REMOTE_ROOT" bash "$E1_REMOTE_ROOT/serve_selected_model.sh" qwen38
# Run the same command with muse after draining/stopping only the owned Qwen service.
```

服务在远程 loopback:8100。本机经既有 SSH tunnel 访问本地 loopback:8100/v1；两个 profile 共用这一端口。切换时先确认本服务无在途/排队，停止自己拥有的服务，再在指定 tmux 工作区启动另一款，核对 `/v1/models` 后才运行相应 profile。不得同时向两个 profile 发请求并误以为有两套常驻服务。新建 tunnel 的可复现形状为 `ssh -N -L 127.0.0.1:8100:127.0.0.1:8100 "$E1_SSH_ALIAS"`；已有 tunnel 时直接复用，凭据仅留本地 600 配置。[clm-deploy]

完整大格和 baseline 启动脚本、逐调用观察器在新包 `scripts/`，保留源 commit、实际 argv 构造和 payload hash；它们是本次验收的复现材料。若要重验，使用新输出目录和干净具名分支，启用 stream、零 transport retries、相同 pair/round；不要覆盖旧 run。执行前仍须核对所用 profile 和服务身份，不能把本报告命令当作 E2 全量授权。[clm-handoff]

## 6. E2 需要冻结的内容

E2 对每个 backbone 配对比较 baseline/ours，选型原则继承[导师 talk](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)。A1/A2 与 judge 均固定 Luna；价格只用于工程可行性，不作为论文贡献。其他已调查候选、benchmark 来源和缺测见[完整矩阵](./2026-09-07-04-30-00-candidate-benchmarks.md)；不把 Terminal-Bench 当严格结构化能力，不把 Omni 净分当本任务幻觉率。[clm-scope]

E2 需冻结模型/profile/revision、实际推理与采样、两臂预算与超时、并发与重试、完整输入/台账版本、方法与基线版本、裁定和 eligibility。尤其应明确 Qwen 是否沿用已验收 low、Sonnet 是否沿用本次 provider default；任何新档位需补受影响的接入验收，不能用公开 max/xhigh 成绩代替。最大输出或 remaining_context 不意味着四款实际生成长度相同，也不与旧 nominal 10K 实验自动等价。[clm-handoff]

方法/prompt/schema/validator/eligibility 与 `2971a8ada` 的对应目录对拍无变化；本轮生产修复均在共用 adapter/runtime/serving。v61/A1 及本轮旧失败不改写，不运行候选 judge，不自动合并或启动 E2/O2。实际 PR 退出门及施工状态只在 GitHub #204/#179 维护。[src-code] [clm-history]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告（新建） | 本次归档提交，`git log --diff-filter=A` 可查 | 本次归档提交 | `c3f01f17a` 下最终 Muse 三格、负载、baseline 和最终四 profile 调查 | 无迁移 | 下列新旧两个 ZIP；不重写旧快照 |

### A.2 上游事实源清单

新包为 [handoff-diagnostics.zip](./evidence/handoff_20260907/handoff-diagnostics.zip)，逐 member hash 见 [manifest.json](./evidence/handoff_20260907/manifest.json)，派生复算见 [verification.json](./evidence/handoff_20260907/verification.json)。[独立隐私扫描](./evidence/handoff_20260907/privacy-scan.json)核验 477 个成员及本轮文档，敏感值匹配为 0；教程中的明确 loopback 示例不视为私有端点。旧包为 [stream-diagnostics.zip](./evidence/stream_20260907/stream-diagnostics.zip)，仍按其原 manifest 冻结。新包排除私有配置和 PR body；脱敏导出保留原始 hash 与导出 hash 的区别，内嵌 run hash 不伪造重签。

| 引用键 | source_id | 事实源 | 类型 | 关键锚点与用途 |
|---|---|---|---|---|
| [src-config] | final_profiles | 新 ZIP | json | `ready/final-profiles.json`；23 profiles、权限、四款字段和 fingerprint |
| [src-cells] | final_cells | 新/旧 ZIP | json/jsonl | 新 `cells/e1-muse30b-schema-order-final-stream/`；旧 Sonnet/Qwen 指定 run；每格 method round-1、stage receipts、summary-audit |
| [src-wire] | wire_usage | 新/旧 ZIP | body/json | 相应 `call_metadata/wire/`；request/response、时间、usage/finish；新 `ready/baseline-audit.json` 与原 baseline record |
| [src-luna] | luna_route | 新/旧 ZIP、[probes.zip](./evidence/probes.zip) | json/body | 新 `ready/gpt-5.6-luna/` 六次 baseline、`ready/luna-direct*`、`ready/luna-method-reuse.json`；旧 `prior_luna/`；历史 baseline 为 `probes.zip` 的 `workflows/gpt-5.6-luna/baseline-02/` |
| [src-muse-fix] | muse_counterexamples | 新 ZIP | json/body/log | `ready/muse-optional-order-check.json`、`ready/muse-contract-order-native/`、`ready/muse-adapter-order-test.json`、各旧 `schema-*` run |
| [src-env] | isolated_environment | 新/旧 ZIP | json/txt | 新 `ready/*-environment.json`、`ready/*-pip-lock.txt`、`ready/client-environment.json`、`ready/muse-serving-identity-schema-order-final-budget.json`、`ready/qwen-cache-relocation-comparison.json`、`ready/qwen-serving-identity-shared-cache-final.json`；新旧 active-server snapshots |
| [src-load] | final_loads | 新/旧 ZIP | json/jsonl | 新 `serving/muse/schema-order-final/{long16k,native90}`；旧 `serving/qwen38/model-max/{long16k,native90,extended90}` |
| [src-code] | adapter_semantics | [serving_muse.py](../../../../utils/llm/serving_muse.py)、[test_serving_muse.py](../../../../tests/utils/test_serving_muse.py) | source/git | `b4e5ba18c`、`7f1131afa`；冻结目录 diff、定向原生回归；utils 256 passed/1 remote-only skip |
| [src-launcher] | remote_launcher | [serve_selected_model.sh](./serve_selected_model.sh) | source | `c3f01f17a`；独立 prefix、共享缓存、GPU 门、精确模型与 serving 参数 |
| [src-bench] | task_benchmarks | [完整矩阵](./2026-09-07-04-30-00-candidate-benchmarks.md) | md/json/zip | 17 身份、20 档位，AA v4.2/LCR v1.1、作者自报分表、严格结构化缺测 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 / 限制 |
|---|---|---|---|---|---|---|
| [clm-scope] | E1-HANDOFF-SCOPE | 四模型优先组合与工程选型边界 | decision | [src-bench]、`protocol.md` 最后 amendment、导师 talk | 人工核对用户决策和来源 | high；不是效果排名或 E2 冻结 |
| [clm-config] | E1-HANDOFF-CONFIG | 精确 profile 与身份边界 | trace | [src-config] 四款公开字段、[src-wire] 请求/响应 model | [cmd-handoff] | high；托管上游 revision 无独立认证 |
| [clm-budget] | E1-HANDOFF-BUDGET | 无人为小额输出限制，遵守 context | trace | [src-wire] cap、旧 `model_max/serving-output-derivation.json` | [cmd-handoff] | high；剩余上界为源码推导，非新增 provider usage 字段 |
| [clm-thinking] | E1-HANDOFF-THINK | 实际档位与公开成绩分开，Sonnet raw 0 更正 | count/trace | [src-wire] raw usage、`ready/sonnet-reasoning-usage-correction.json`、[src-env] 模板/generation config | [cmd-handoff] | high；网关回报不证明上游内部状态 |
| [clm-timeout] | E1-HANDOFF-TIMEOUT | method 与 baseline 的真实 timeout 分开 | trace | [src-wire] request extensions、probe timeouts、旧三层 comparison | [cmd-handoff]；人工核对 runtime 常量 | high；baseline null 不改写为 300s |
| [clm-method] | E1-HANDOFF-CELLS | 九格状态、阶段与 66 个响应逐项复核 | count | [src-cells] 指定三 run、[src-wire] usage/finish | [cmd-handoff] | high；有限接入样本 |
| [clm-baseline] | E1-HANDOFF-BASELINE | 三款最终 baseline 成功、Luna 六次 503 | count | [src-wire] `baseline-audit.json` 与每次 record/request | [cmd-handoff] | high；不以退出码代替成功 |
| [clm-luna] | E1-HANDOFF-LUNA | 历史成功可追溯、09-07 渠道仍失败 | risk | [src-luna] 状态码、Retry-After、配置逐字段比较 | [cmd-handoff] | high；恢复后的可用性需真实复验 |
| [clm-sonnet-d] | E1-HANDOFF-SONNET-D | 正常证据义务降级，保留 1 error | classification | 旧 Sonnet `method/0029/round-1.json` 的 errors/stage receipts/LLM calls | [cmd-handoff]；人工逐条对照 defeater 缺口 | high；不代表全部判断完成 |
| [clm-muse-fix] | E1-HANDOFF-MUSE-FIX | 原生参数约束与嵌套顺序修复，不改方法 | trace | [src-muse-fix] 同请求 hash、原 validator、[src-code] 版本门与测试 | [cmd-handoff]、[cmd-regression] | high；不外推任意 schema 或 auto 路径 |
| [clm-load] | E1-HANDOFF-LOAD | 最终 Muse 和配置匹配 Qwen 的容量/并发 | count | [src-load] 非 warmup `requests.jsonl` 与 summary | [cmd-handoff] | high；不是 16 个最大窗口或持续 SLA |
| [clm-deploy] | E1-HANDOFF-DEPLOY | 独立环境、共享缓存、身份切换可复现 | trace | [src-env] 版本/进程、[src-launcher] | 人工检查 GPU/prefix/模型身份；[cmd-handoff] | high；实时空闲状态需部署前核对 |
| [clm-history] | E1-HANDOFF-HISTORY | 历史不覆盖，方法语义不改 | prohibition | [src-code] 冻结 diff、新旧 run ID 和 manifests | [cmd-regression] | high；源码不同的 smoke 不伪称同配置结果 |
| [clm-handoff] | E1-HANDOFF-E2 | 两臂配置与推理仍需协议冻结 | decision | [src-config]、[src-bench]、`protocol.md` | 人工核对 E2 事前登记 | high；本材料不授权全量实验 |

### A.4 复验命令

[cmd-handoff] 从仓库根离线运行，不调用 provider：

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_handoff_evidence.py
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_benchmark_evidence.py
venv/bin/python -m utils.llm validate
```

[cmd-regression] 共用 utils 和语义边界检查：

```bash
venv/bin/python -m pytest tests/utils -q
git diff 2971a8ada -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/method project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm pyfcstm
```

本机 utils 为 256 passed、1 skipped；skip 是需要远程 Muse tokenizer/engine 的测试，已在对应独立 env 通过。远端复验用该 env 的 Python，设置 `E1_MUSE_TOKENIZER` 为缓存 snapshot、`E1_MUSE_ADAPTER` 为部署文件，运行同一测试；不能在本机安装 serving 引擎或下载 tokenizer/权重来消除 skip。
