# E1 总报告：四模型配置、验收与实验交接

2026-09-07 交付边界更新：本文所引原始记录、ZIP/JSON 和历史专用校验器仅本地留存，不随 Git 提供；数字与来源链接保留，逐条历史重放须另行取得原件。通用操作见[复现附录](./2026-09-07-11-55-00-reproduction.md)。

本报告汇总 E1 最终四款的配置和验收，Luna 新连接的逐调用记录见[11:10 新连接报告](./2026-09-07-11-10-00-luna-connection-recovery.md)，可执行核心见[复现附录](./2026-09-07-11-55-00-reproduction.md)。此前[06:55 复核](./2026-09-07-06-55-00-luna-route-recheck.md)与旧失败保留，不用旧路由状态覆盖后续验证。

核验日期：2026-09-07。正文的 `[src-*]`、`[clm-*]` 引用文末审计附录。本报告补充 [03:36 stream 快照](./2026-09-07-03-36-18-stream-model-max-acceptance.md)，保存最终 Muse serving 修复、四款 profile 的 baseline/ours 覆盖与 Luna 渠道失败；旧 run 和旧归档均保留。这里只判断接入，不计算效果排名；所有 smoke 的 `formal_result_eligible=false`。[clm-scope]

## 1. 组合与验收结论

用户优先组合为 **GPT-5.6 Luna + Claude Sonnet 5 + Qwen3.8-27B + Muse Glimmer-30B**。Sonnet 提供不同于 Luna 的商用模型族，Qwen/Muse 提供两种总参数小于 100B 的开放模型族。依据为公开任务相关能力、组合覆盖与接入可行性，不根据正式 ours/baseline 差值选模型，不主张这四款是本任务 SOTA。Haiku 保留备选，Gemini 与其余开放候选的调查和失败不删除，也不扩展部署队列。[src-bench] [clm-scope]

| 模型 | 最小 stream baseline | stream ours | 证据边界 |
|---|---|---|---|
| Luna | 新连接 0001/r1 成功，5118 input / 183 output、16.71s | 新连接 0001/r1，8 阶段完成、5 次 tool/usage；0 errors/audit errors/schema 修正，327.28s | 源码分别为 `672069f85` / `5cbf1442d`；旧 503 和首次 method 的 failed SSE 保留，有限成功不是持续 SLA |
| Sonnet 5 | 最终 profile 0001 成功 | 0019/0029/0049 均 eligible；0029 保留正常证据降级 | 无 provider 失败或 schema 配额耗尽；0029 仍有 1 error |
| Qwen3.8-27B | 最终 profile 0001 成功 | 三格完成，errors/audit errors 全 0 | low、TP4、1M YaRN、remaining_context；不能代表公开 xhigh |
| Muse Glimmer-30B | 最终 serving adapter 下 0001 成功 | 修复后三格完成，errors/audit errors 全 0 | high、TP4、131072、remaining_context；只验收原生 function/tool 路径 |

上述状态按本地 baseline record、每格 8 个 stage receipts、LLM stage、errors 和 audit errors 分别核对。Sonnet 0029 的两个阶段为 `completed_with_diagnostics`，其余八个大格的全部阶段为 `completed`；非零的 D 诊断条数不自动等于错误或基础设施失败。Luna 新连接的普通探针仅 1/1 usage，2.85s，只证明存活；shared runtime 的 required PumpIssue tool 一次通过，4500/106 tokens、24.27s、正常关闭。[clm-method] [clm-baseline] [clm-luna]

## 2. 精确 profile、预算与推理设置

最终本地配置经 `utils.llm` 加载，23 profiles，权限 600。下表不含 endpoint 或凭据；历史公开字段和配置 fingerprint 在本地 `ready/final-profiles.json`，Luna 更换连接后的配置差异见[新连接报告](./2026-09-07-11-10-00-luna-connection-recovery.md)；§7 的三项复验 fingerprint 均与当前 profile 一致，不能把旧连接 fingerprint 当作新连接。托管模型只能记录请求 ID 和渠道回报身份，未取得独立认证的上游不可变 revision，不将网关名称当作这种认证。[src-config] [src-luna-recovery] [clm-config]

| profile | 请求 model ID | adapter / stream 结构路径 | context | 输出来源与实际请求 |
|---|---|---|---:|---|
| `gpt-5.6-luna` | `gpt-5.6-luna` | `openai-responses` / function tool | 1,050,000 | profile 128,000；HTTP `max_output_tokens=128000` |
| `claude-sonnet-5` | `claude-sonnet-5` | `anthropic` / native tool_use | 1,000,000 | Models API 核验 128,000；HTTP `max_tokens=128000` |
| `e1-qwen38-27b` | `qwen3.8-27b` | `openai` / SGLang qwen3_coder function/tool | 1,000,000 | `remaining_context`；无输出小额字段 |
| `e1-muse30b` | `muse-glimmer-30b` | `openai` / SGLang Muse ATEM function/tool + serving 约束 | 131,072 | `remaining_context`；无输出小额字段 |

开放模型的 profile `max_output_tokens` 等于部署窗口，表示经核验的模式声明，**不是额外允许生成一个完整窗口**。SGLang 0.5.19 在未提供 `max_new_tokens` 时按完整输入和实际 context/KV 页约束输出；源码推导的 context 上界为 `context_length - prompt_tokens - 2`。已核验 `allow_auto_truncate=false`，未配置环境输出小上限。真实输入不裁剪，容量与输出不能重复占用窗口。商业上限与来源保留在旧包 `model_max/` 和[规格调查](./2026-09-06-11-53-00-commercial-models.md)。[clm-budget]

| 模型 | 验收时实际推理与采样 | 与公开 benchmark 的区别 |
|---|---|---|
| Luna | 新连接 ordinary/baseline 省略 reasoning；method 显式 `effort=none`；均未显式传 temperature/top_p，method raw reasoning=0 | 两入口不同，E2 须明确；不能把 AA max 行当作当前验收档位 |
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
| Luna | 新连接 `baseline-aizzz-user-route` | 5118 / 183 | 0 | response.completed / 16.71s；旧六次 503 保留 |

Qwen 共享盘缓存路径复核后另有 `baseline-shared-cache-final`：stream/tool/usage 成功，839 input / 1070 output，71.71s，源码仍为 `c3f01f17a`。profile、依赖和全部配置参数对拍相同；SGLang 重启自动种子从 522151049 变为 781184292，启动时间和内部运行状态另记。没有把它写成完全相同的随机推理，也不因一次冷启动耗时重跑已有三格/容量结果。[src-env] [clm-baseline]

Luna 历史 method `915ecc689ff945c185779b1e7b6fd7c5` 来自 `17ad54b05e2bd8fda0e389ef925e18a03eede82d`。配置逐字段比较显示 adapter、endpoint、凭据、model、output、模式及 pricing 相同，只有 context 声明从 272K 增到 1.05M。旧 nominal 10K 在当时 langchain-openai 1.2.2 Responses 路径被构造器的 128K 覆盖；这由隔离 wire 复现和旧 profile 支撑，**不是改写历史审计**。历史该格没有 compact。该材料说明旧成功与共用 adapter 回归的复用依据，不证明新日期的渠道可用。[src-luna] [clm-luna]

09-07 04:43 至 06:02 的六次 baseline 均在约 2 秒返回上游 503；同业务原生 Responses 还出现 502 / Retry-After 60，模型列表则为 200，不能以列表成功推断生成可用。后续用户新连接仅更换 endpoint/key，23 profiles 中其他 22 项和 Luna 其余字段逐项相同；普通/shared runtime/baseline 成功后，在 `5cbf1442d` 下补齐新 method `3c38e4f070634aa097da075c13d285c0`。所有成功响应为 response.completed、incomplete_details=null，HTTP 输出额度 128000，未裁剪输入；最大单次 input/output 为 40229/1950。[clm-luna]

新连接首次 method `bc3c4b581bdf469ebf32c393142262e2` 的 8 次响应实为 7 completed、1 failed，旧 SDK 将 HTTP 200 中的 `server_error` 漏报为空成功，旧顶层 eligible/零 error 不代表 8/8 健康。`aa64c413f` 在共用 adapter 捕获 response.failed，后续完整 method 5/5 tool/usage、零 schema 修正；该修复不能消除上游过载。历史 nominal 10K 的映射偏差和所有失败保持原件，不用新结果重写旧审计。[clm-luna]

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

16K/16-worker 的 batch 性能直接由非 warmup 请求复算；output tokens/s 使用 provider completion tokens（包含 reasoning，不重复相加），requests/s 为 32 除以实测 batch 墙钟，p95 使用 nearest-rank。[clm-load]

| 模型 | batch 墙钟 | requests/s | output tokens/s | p50 请求延迟 | p95 首有效 chunk |
|---|---:|---:|---:|---:|---:|
| Qwen | 24.75s | 1.293 | 550.69 | 11.47s | 8.28s |
| Muse 最终 serving | 27.81s | 1.151 | 711.30 | 13.22s | 9.02s |

普通生成、function/tool、stream usage 与实际推理控制在 09-06 的独立环境迁移中均通过。该日 Qwen 短生成只有 47–48 输入 tokens、Muse 简易工具约 395 tokens，旧输出额度分别为 65536/32768；这只能证明当时入口，不替代上表最终预算的大输入验收。Qwen 旧 0001 因 30s 首字节限制改为 nonstream 的记录也不充当最终 stream 证据，最终以本报告三大格及负载为准。[clm-deploy] [clm-history]

### 复现入口

[复现附录 §2/§3](./2026-09-07-11-55-00-reproduction.md) 固化关键依赖、精确权重、TP、parser、YaRN、low、64 个可运行请求和静态显存比例 0.92。Muse 需要仓库的 [serving_muse.py](../../../../utils/llm/serving_muse.py)。这是结合作者资料与本节点验通后的配置，不伪称官方未经调整的默认命令。原启动脚本和完整 pip lock 本地保留；附录给出独立环境创建和可执行启动核心。禁止安装到 base/系统，也不在本机下载权重；已验通环境直接复用。[clm-deploy]

远程复现时，`E1_SHARED_ROOT` 指向既有授权共享根，使用附录中的启动代码和仓库 Muse adapter；权重只使用表中 snapshot。环境将 `CONDA_PREFIX`、Python、CUDA_HOME/PATH/include/runtime 限定在所选 prefix，显式设 `SGLANG_CACHE_DIR` 和 `CUDA_CACHE_PATH` 到共享盘，并在 GPU 4-7 被占用时拒绝启动。[src-launcher]

服务在远程 loopback:8100。本机经既有 SSH tunnel 访问本地 loopback:8100/v1；两个 profile 共用这一端口。切换时先确认本服务无在途/排队，停止自己拥有的服务，再在指定 tmux 工作区启动另一款，核对 `/v1/models` 后才运行相应 profile。不得同时向两个 profile 发请求并误以为有两套常驻服务。新建 tunnel 的可复现形状为 `ssh -N -L 127.0.0.1:8100:127.0.0.1:8100 "$E1_SSH_ALIAS"`；已有 tunnel 时直接复用，凭据仅留本地 600 配置。[clm-deploy]

历史大格/baseline 启动脚本、观察器和原始 payload hash 仅本地留存。附录 §4/§5 给出不依赖固定 run ID 或 ZIP 的入口与核验核心；如要逐条重放历史结果，须另行取得原件。新运行使用新输出目录、干净具名分支、stream、同 pair/round 与已登记重试设置；不要覆盖旧 run，也不把复现命令当作 E2 全量授权。[clm-handoff]

## 6. E2 需要冻结的内容

E2 对每个 backbone 配对比较 baseline/ours，选型原则继承[导师 talk](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)。A1/A2 与 judge 均固定 Luna；价格只用于工程可行性，不作为论文贡献。其他已调查候选、benchmark 来源和缺测见[完整矩阵](./2026-09-07-04-30-00-candidate-benchmarks.md)；不把 Terminal-Bench 当严格结构化能力，不把 Omni 净分当本任务幻觉率。[clm-scope]

E2 需冻结模型/profile/revision、实际推理与采样、两臂预算与超时、并发与重试、完整输入/台账版本、方法与基线版本、裁定和 eligibility。尤其应明确 Qwen 是否沿用已验收 low、Sonnet 是否沿用本次 provider default；任何新档位需补受影响的接入验收，不能用公开 max/xhigh 成绩代替。最大输出或 remaining_context 不意味着四款实际生成长度相同，也不与旧 nominal 10K 实验自动等价。[clm-handoff]

合流前 E1 `0c49863f3` 的方法目录与 `2971a8ada` 无差异；本次合入上游 A1 后，应与上游 `05cd98b0f` 对拍方法、baseline、judge、台账和正式结果，不能用旧起点误判上游授权变更。E1 额外生产修复仍限共用 adapter/runtime/serving，历史 v61/A1 与旧失败不改写，不运行候选 judge，不自动合并或启动 E2/O2。动态施工状态只在 GitHub #204/#179 维护。[src-code] [clm-history]

## 7. 合流版本的接入复核

2026-09-07 的生产源码 `8b377e977b8c03b57e64f4540415356d9e53a074` 合入上游 `05cd98b0f9e8329de99431690f7b571fd3ec4f71`。报告索引保留 E1 六条和 A1 两条入口；method、baseline_arm、judge、discover_matrix、final_results 和 pyfcstm 与该上游逐路径无差异，继承的 A1 变更没有被 E1 覆盖。[src-merge] [clm-merge]

两套 Responses 防护统一到 [utils/llm/responses_stream.py](../../../../utils/llm/responses_stream.py)。factory 与 AgentApp 共用幂等的 per-client guard；旧 agent 导入只保留异常类型兼容，无 `utils.llm -> agent.runtime` 反向依赖。保留 failed/error 原事件、code/message、身份、HTTP 状态和失败 usage，识别空流、提前 EOF 和 incomplete；显式 `retryable=false` 优先于一般状态码推断，HTTP 500–599（含 52x）仍分类为可重试。Google 状态提取、structured runtime 的失败归类与有限重试一并复核，provider 失败不混入 schema 修正。[src-merge] [clm-merge]

| 离线验证 | 结果 | 范围与限制 |
|---|---:|---|
| 完整 `tests/utils` | 321 passed / 1 skipped | 包括 sync/async、两构造入口、正常 tool/usage、失败事件、空流/EOF/incomplete、HTTP 5xx、显式不可重试、有限重试与失败 usage |
| 两套 Responses 回归 | 57 passed | 已包含在 321 中，不重复相加 |
| 上游 A1 contract/default-full 投影 | 65 passed | `test_ablation_contract.py`、`test_no_inspect.py`；7 个既有 Pydantic warnings |
| 已捕获失败事件离线回放 | 8/8 | E1/A1 × factory/AgentApp × sync/async，零网络调用；保留错误与原缺失 usage |

唯一 skip 是需要远程 Muse 引擎/tokenizer 的既有测试；生产 `serving_muse.py` 和该测试均保留，未因删除审计数据触发新 skip。E1 回放使用原始 request/response 字节，SHA-256 分别为 `1da9b166ea2284c24a977c61677be696eb7e0358bfa5ccd4519239e5aeb9732b` / `68bb863b3856e2fdcf10bea2e411c202e501a6fa535c01a37eb8c0ae6a515e4b`；A1 使用 audit 中的原 `failure_event` 重建 SSE，**不是原始 wire 字节**，原 usage 为 null 的项仍记缺失。[src-merge] [clm-merge]

以下新探针发生于 12:15–12:17 CST，生产代码固定为 `8b377e977`，工作树当时仅有 Markdown、ignore 和审计产物取消跟踪待提交。各入口使用最终 Luna profile，零 transport retries；全部 HTTP 200、stream、`response.completed`、`incomplete_details=null`，实际请求额度均为 128000。[src-merged-live] [clm-merged-live]

| 入口 / 样本 | input / output | reasoning tokens | 墙钟 | 终态与结构 |
|---|---:|---:|---:|---|
| factory 普通短生成 | 1 / 1 | 未回报 | 2.94s | completed；极短存活信号，不用于计量或性能估计 |
| 共用 PublicStructuredRuntime / PumpIssue | 4500 / 98 | 0 | 8.63s | success，required tool 一次 schema-valid，零 schema 修正/压缩/重试，runtime 已关闭 |
| 原 baseline runner / 0001 r1 | 5118 / 182 | 0 | 19.97s | record=ok，一次 NaiveReview tool，参数与落盘 parsed_output 一致，无 failure |

三次真实请求逐字段与新连接最初成功请求相同，包括完整输入、tool/schema、推理和采样；ordinary/baseline 仍省略 reasoning，runtime 仍为 none。普通探针与 runtime 的 HTTP timeout 为 300s，baseline 仍为 null。该合流只拦截失败/不完整终态，成功事件透传；结合原请求对拍和离线成功路径回归，没有另行重跑完整 method。Luna 完整 0001 method 继续使用 §4 的 `5cbf1442d` / `3c38e4f070634aa097da075c13d285c0` 证据，不冒称在合流 commit 下新跑过整格。[clm-merged-live]

本次成功之前，两轮相同的三入口调用均在约 1–3s 返回 503；原始错误为 `new_api_error/system_cpu_overloaded`，回报 CPU 96.2%、阈值 90%。同业务原生请求与不同请求头的顺序诊断有成功也有失败，随后原 SDK 配置自行恢复；这些对照不能证明请求头是原因，生产 profile/headers 未因此修改。旧 503、新连接首次 HTTP 200 内 failed SSE、此次六个 503 均本地保留。一次诊断脚本在接到响应后错误使用 context manager、未保存响应，已单独标为 harness failure 并排除结果统计。有限成功不外推持续 SLA。[src-merged-live] [clm-merged-live]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告（新建） | 本次归档提交，`git log --diff-filter=A` 可查 | 本次归档提交 | `c3f01f17a` 下最终 Muse 三格、负载、baseline 和最终四 profile 调查 | 无迁移 | 下列新旧两个 ZIP；不重写旧快照 |

### A.2 上游事实源清单

新包为 本地 `evidence/handoff_20260907/handoff-diagnostics.zip`（handoff-diagnostics.zip），逐 member hash 见 本地 `evidence/handoff_20260907/manifest.json`（manifest.json），派生复算见 本地 `evidence/handoff_20260907/verification.json`（verification.json）。本地 `evidence/handoff_20260907/privacy-scan.json`（独立隐私扫描）核验 477 个成员及本轮文档，敏感值匹配为 0；教程中的明确 loopback 示例不视为私有端点。旧包为 本地 `evidence/stream_20260907/stream-diagnostics.zip`（stream-diagnostics.zip），仍按其原 manifest 冻结。新包排除私有配置和 PR body；脱敏导出保留原始 hash 与导出 hash 的区别，内嵌 run hash 不伪造重签。

| 引用键 | source_id | 事实源 | 类型 | 关键锚点与用途 |
|---|---|---|---|---|
| [src-config] | final_profiles | 新 ZIP | json | `ready/final-profiles.json`；23 profiles、权限、四款字段和 fingerprint |
| [src-cells] | final_cells | 新/旧 ZIP | json/jsonl | 新 `cells/e1-muse30b-schema-order-final-stream/`；旧 Sonnet/Qwen 指定 run；每格 method round-1、stage receipts、summary-audit |
| [src-wire] | wire_usage | 新/旧 ZIP | body/json | 相应 `call_metadata/wire/`；request/response、时间、usage/finish；新 `ready/baseline-audit.json` 与原 baseline record |
| [src-luna] | luna_route | 新/旧 ZIP、本地 `evidence/probes.zip`（probes.zip） | json/body | 新 `ready/gpt-5.6-luna/` 六次 baseline、`ready/luna-direct*`、`ready/luna-method-reuse.json`；旧 `prior_luna/`；历史 baseline 为 `probes.zip` 的 `workflows/gpt-5.6-luna/baseline-02/` |
| [src-muse-fix] | muse_counterexamples | 新 ZIP | json/body/log | `ready/muse-optional-order-check.json`、`ready/muse-contract-order-native/`、`ready/muse-adapter-order-test.json`、各旧 `schema-*` run |
| [src-env] | isolated_environment | 新/旧 ZIP | json/txt | 新 `ready/*-environment.json`、`ready/*-pip-lock.txt`、`ready/client-environment.json`、`ready/muse-serving-identity-schema-order-final-budget.json`、`ready/qwen-cache-relocation-comparison.json`、`ready/qwen-serving-identity-shared-cache-final.json`；新旧 active-server snapshots |
| [src-load] | final_loads | 新/旧 ZIP | json/jsonl | 新 `serving/muse/schema-order-final/{long16k,native90}`；旧 `serving/qwen38/model-max/{long16k,native90,extended90}` |
| [src-code] | adapter_semantics | [serving_muse.py](../../../../utils/llm/serving_muse.py)、[test_serving_muse.py](../../../../tests/utils/test_serving_muse.py) | source/git | `b4e5ba18c`、`7f1131afa`；冻结目录 diff、定向原生回归；utils 256 passed/1 remote-only skip |
| [src-launcher] | remote_launcher | [复现附录（原 serve_selected_model.sh）](./2026-09-07-11-55-00-reproduction.md) | source | `c3f01f17a`；独立 prefix、共享缓存、GPU 门、精确模型与 serving 参数 |
| [src-bench] | task_benchmarks | [完整矩阵](./2026-09-07-04-30-00-candidate-benchmarks.md) | md/json/zip | 17 身份、20 档位，AA v4.2/LCR v1.1、作者自报分表、严格结构化缺测 |
| [src-luna-recovery] | recovered_luna | [新连接报告](./2026-09-07-11-10-00-luna-connection-recovery.md)、本地 `luna_recovery_20260907/` | md/local | 连接差异、plain/runtime/baseline、失败 SSE 与完整 method；不包含私有配置副本 |
| [src-merge] | merged_guard | [provider guard](../../../../utils/llm/responses_stream.py)、[两入口回归](../../../../tests/utils/test_responses_stream.py)、本地 `e1-conflict-20260907/` | source/local | `8b377e977`；测试记录、`failed-event-replays.json`、索引事实并集与上游目录对拍 |
| [src-merged-live] | merged_luna_smoke | 本地 `e1-conflict-20260907/merged-live-verification.json` 及其指向的具体探针目录 | local | plain `merged-stream-guard-later`、runtime `final/runtime-tool`、baseline `baseline-merged-stream-guard-later`；两轮旧 503、原生对照和独立 harness failure |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 / 限制 |
|---|---|---|---|---|---|---|
| [clm-scope] | E1-HANDOFF-SCOPE | 四模型优先组合与工程选型边界 | decision | [src-bench]、`protocol.md` 最后 amendment、导师 talk | 人工核对用户决策和来源 | high；不是效果排名或 E2 冻结 |
| [clm-config] | E1-HANDOFF-CONFIG | 精确 profile 与身份边界 | trace | [src-config] 四款公开字段、[src-wire] 请求/响应 model、[src-luna-recovery] 新连接、[src-merged-live] fingerprint | [cmd-handoff] | high；托管上游 revision 无独立认证 |
| [clm-budget] | E1-HANDOFF-BUDGET | 无人为小额输出限制，遵守 context | trace | [src-wire] cap、旧 `model_max/serving-output-derivation.json` | [cmd-handoff] | high；剩余上界为源码推导，非新增 provider usage 字段 |
| [clm-thinking] | E1-HANDOFF-THINK | 实际档位与公开成绩分开，Sonnet raw 0 更正 | count/trace | [src-wire] raw usage、`ready/sonnet-reasoning-usage-correction.json`、[src-env] 模板/generation config | [cmd-handoff] | high；网关回报不证明上游内部状态 |
| [clm-timeout] | E1-HANDOFF-TIMEOUT | method 与 baseline 的真实 timeout 分开 | trace | [src-wire] request extensions、probe timeouts、旧三层 comparison | [cmd-handoff]；人工核对 runtime 常量 | high；baseline null 不改写为 300s |
| [clm-method] | E1-HANDOFF-CELLS | 九格状态、阶段与 66 个响应逐项复核 | count | [src-cells] 指定三 run、[src-wire] usage/finish | [cmd-handoff] | high；有限接入样本 |
| [clm-baseline] | E1-HANDOFF-BASELINE | 四款 baseline 成功，Luna 旧六次 503 保留 | count | [src-wire] `baseline-audit.json`、[src-luna-recovery] 与各次 record/request | [cmd-handoff] | high；不以退出码代替成功 |
| [clm-luna] | E1-HANDOFF-LUNA | 旧失败可追溯，新连接完成真实 method | trace/risk | [src-luna] 状态码与历史配置、[src-luna-recovery] 新连接完整记录 | [cmd-handoff] | high；成功不证明持续 SLA |
| [clm-sonnet-d] | E1-HANDOFF-SONNET-D | 正常证据义务降级，保留 1 error | classification | 旧 Sonnet `method/0029/round-1.json` 的 errors/stage receipts/LLM calls | [cmd-handoff]；人工逐条对照 defeater 缺口 | high；不代表全部判断完成 |
| [clm-muse-fix] | E1-HANDOFF-MUSE-FIX | 原生参数约束与嵌套顺序修复，不改方法 | trace | [src-muse-fix] 同请求 hash、原 validator、[src-code] 版本门与测试 | [cmd-handoff]、[cmd-regression] | high；不外推任意 schema 或 auto 路径 |
| [clm-load] | E1-HANDOFF-LOAD | 最终 Muse 和配置匹配 Qwen 的容量/并发 | count | [src-load] 非 warmup `requests.jsonl` 与 summary | [cmd-handoff] | high；不是 16 个最大窗口或持续 SLA |
| [clm-deploy] | E1-HANDOFF-DEPLOY | 独立环境、共享缓存、身份切换可复现 | trace | [src-env] 版本/进程、[src-launcher] | 人工检查 GPU/prefix/模型身份；[cmd-handoff] | high；实时空闲状态需部署前核对 |
| [clm-history] | E1-HANDOFF-HISTORY | 历史不覆盖，方法语义不改 | prohibition | [src-code] 冻结 diff、新旧 run ID 和 manifests | [cmd-regression] | high；源码不同的 smoke 不伪称同配置结果 |
| [clm-handoff] | E1-HANDOFF-E2 | 两臂配置与推理仍需协议冻结 | decision | [src-config]、[src-bench]、`protocol.md` | 人工核对 E2 事前登记 | high；本材料不授权全量实验 |
| [clm-merge] | E1-MERGED-CONTRACT | 合流保留两入口防护和上游研究语义 | trace | [src-merge] 源码、321/65 回归与 8 回放 | [cmd-regression]；历史回放先取得原件 | high；远程 Muse skip 不以本地 fake 替代 |
| [clm-merged-live] | E1-MERGED-LUNA | 合流版本三入口 stream 成功，间歇 503 如实保留 | trace/risk | [src-merged-live] 三请求/响应与旧失败目录；§7 参数与 usage 表 | 复现附录 §4/§5；原件取得后对拍 | high；身份仅渠道回报，未重跑完整 method |

### A.4 复验命令

[cmd-handoff] 从仓库根离线运行，不调用 provider：

历史逐条复验须先取得对应的本地原件及校验器；通用校验与新运行操作见[复现附录](./2026-09-07-11-55-00-reproduction.md)。

[cmd-regression] 共用 utils 和语义边界检查：

```bash
venv/bin/python -m pytest tests/utils -q
git diff 2971a8ada 0c49863f3 -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/method project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm pyfcstm
```

上面的 `2971a8ada..0c49863f3` 只用于合流前历史边界，当时 utils 为 256 passed、1 skipped。本次合流后的 321 passed、1 skipped 及 65 项 A1 投影回归见 §7；与上游 `05cd98b0f` 的逐目录检查命令见[复现附录 §6](./2026-09-07-11-55-00-reproduction.md)。skip 是需要远程 Muse tokenizer/engine 的测试，已在对应独立 env 通过。远端复验用该 env 的 Python，设置 `E1_MUSE_TOKENIZER` 为缓存 snapshot、`E1_MUSE_ADAPTER` 为部署文件，运行同一测试；不能在本机安装 serving 引擎或下载 tokenizer/权重来消除 skip。
