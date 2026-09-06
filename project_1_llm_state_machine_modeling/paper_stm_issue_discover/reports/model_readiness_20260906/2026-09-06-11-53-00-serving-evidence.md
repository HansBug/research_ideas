# 远程部署与负载证据

核验日期：2026-09-06。本轮仅在远程 H200 节点执行权重下载、环境安装和推理服务；本机运行 HTTP/profile 客户端并通过 SSH tunnel 访问 loopback。使用 GPU 0-3，保留 GPU 4-7 及既有工作区。结束盘点的远程共享存储约 5.2 TiB 可用、远程根盘约 667 GiB、本机约 81 GiB；本机没有下载模型权重。[clm-serving-environment]

## 已验证配置

负载使用同一合成状态机任务，包含两次 warmup，每个并发档执行两倍请求。短输入约 2K，Qwen/Gemma 的短 sweep output cap 为 256；Muse 最终使用 function/tool 参数路径、high reasoning、32,768 output cap。`eligible` 要求 HTTP 成功、收到 `[DONE]`、schema 合法、对应 `finish_reason=stop/tool_calls` 和 usage 存在；它不自动判定语义正确。Muse 后续显式检查 literal placeholder，原 JSON response-format 结果只能算传输/结构测量。[src-load-client]

四款最终配置均为 BF16、SGLang、`mem_fraction_static=0.92`、`max_running_requests=64`。下表的 16-worker 测试同时使用长输入和 thinking；不是只测短 prompt。[clm-serving-capacity]

| 模型 | TP / 配置窗口 | 0.9 边界实际输入 / 完成 | 边界 p95 | 16-worker thinking 实际输入 / 完成 | 16-worker p95 / output cap |
|---|---|---|---:|---|---|
| Qwen3.8-27B | TP4 / 1,000,000，官方 YaRN，thinking-low | 900,036 / 2/2 | 97.30s | 16,056 / 32/32 | 17.37s / 65,536 |
| Qwen3.6-35B-A3B | TP4 / 1,010,000，官方 YaRN | 909,035 / 2/2 | 40.77s | 16,053 / 32/32 | 17.80s / 32,768 |
| Gemma4-31B-it | TP2 / 262,144 | 236,005 / 2/2 | 189.15s | 16,054 / 32/32 | 58.25s / 32,768 |
| Muse Glimmer 30B | TP4 / 131,072，function/tool，high reasoning | 118,375 / 2/2 | 9.12s | 16,410 / 32/32 | 18.83s / 32,768 |

各行上述测量均为零 transport/schema/truncation failure；长输入 sweep 另有并发 1、4 的成功记录。两款 Qwen 的原生窗口结果单独保留：Qwen3.8 输入 235,987、Qwen3.6 输入 236,005，各 2/2。Qwen3.8 早期输入 235,624 虽响应正常，但低于 0.9 原生目标，不能替代后续合格记录。[clm-serving-capacity]

四款最终短 sweep 均为 32 并发 64/64；代表性吞吐依次约 9.10、15.42、5.32、3.78 req/s。Muse 这行使用 high reasoning/tool，与其他短 sweep 的输出模式不同。短 sweep 中两款 Qwen 使用原生配置，最终扩展配置的承载依据是上表长 thinking sweep。思考模式、输出规模、prefix cache 和共享 GPU 环境会影响延迟，不能跨模型按 req/s 直接排名。[clm-serving-capacity]

Muse 的旧 `muse-context90` 两条响应都有占位符，旧 `muse-long16k-thinking-final` 的 42 条非 warmup 响应中 29 条有占位符；原 `eligible=true` 不表示任务正确。显式 high reasoning 和字段提示的 JSON 模式仍有失败，改为当前 method 同类的 function/tool 路径后，16K 共 42 条、边界 2 条、短 32 并发 64 条全部无占位符。本轮 agent 逐条检查了 16-worker 的 32 条和边界 2 条 tool 参数，均给出缺失联锁守卫及 open-interlock/start/Running 反例。该检查只针对这个合成任务，不是人工裁定，不外推到研究语料准确率。[clm-muse-routing]

## Profile 与真实 workflow

通过 `LLM_CONFIG_FILE` 指向权限 600 的隔离 `.llmconfig.yml`，调用未修改的 `utils.llm.create_chat_model`。四款开放模型均完成普通生成、JSON schema、tool call、streaming usage 四类探针。现有 Luna/Sonnet/Haiku 同样完成四类；Gemini 3.5 的旧兼容/原生路径均未成功，Gateway B 的 3.7/3.8 native profile 已完成正式接入和 method smoke。所有 workflow 仅用事前选定 pair `0001`、一轮、一 worker、零额外 transport retry，不读取 ledger、不评分。[clm-workflow-status]

## 配置字段迁移审计

本地主 registry 只接受 `LLMConfig` 的显式字段。旧的七个开放模型 profile 曾在本地配置中携带临时 `inference` 扩展字段；这些字段已从 `.llmconfig.yml` 清理，因此 registry 可正常加载。原设置保留在本报告和远程服务证据中，未被当作当前 profile schema 或新的运行参数：

本轮最终核验时主 registry 可加载共 23 个 profile；`gateway-b-gemini-3.7-native` 与 `gateway-b-gemini-3.8-native` 的 profile identity、endpoint 和凭据存在性与隔离实测配置一致。公开记录只保留布尔核验结果，不包含凭据或私有端点。

| profile | 原记录的 thinking / effort | 原记录的 sampling | 原记录的结构化输出预算 |
|---|---|---|---:|
| `e1-qwen38-27b` | thinking=true；effort=low | temperature=1.0；top_p=0.95；top_k=20 | 65,536 |
| `e1-qwen36-35b` | thinking=true | temperature=1.0；top_p=0.95；top_k=20 | 32,768 |
| `e1-gemma4-31b` | thinking=true | temperature=1.0；top_p=0.95；top_k=64 | 32,768 |
| `e1-muse30b` | thinking=true；reasoning_strength=high | temperature=1.0；top_p=0.95；top_k=64 | 32,768 |
| `e1-nemotron35-30b` | thinking=true | temperature=1.0；top_p=0.95；top_k 未记录 | 32,768 |
| `e1-glm47-flash` | thinking=true | temperature=1.0；top_p=0.95；top_k 未记录 | 32,768 |
| `e1-gptoss20b` | thinking=true；effort=medium | temperature=1.0；top_p/top_k 未记录 | 32,768 |

这张表是历史服务/实验设置审计，不是当前 `utils.llm` profile 合同；正式 E2 若需要这些 provider-specific controls，应通过已验证的 adapter 接口和独立 run record 明确登记。

| profile | baseline | 当前 method | 解释 |
|---|---|---|---|
| `gpt-5.6-luna` | 完成 | `completed`，eligible cell 1 | 最小工作流通过 |
| `claude-sonnet-5` | 完成 | `failed_with_receipt`，eligible cell 0 | `ChatAnthropic` timeout 类型不兼容 |
| `claude-haiku-4-5` | 未运行 | 未运行 | 仅四类 API 探针，不推断 method |
| `e1-gemini-3.5-flash` | provider 失败 | `failed_with_receipt`，eligible cell 0 | 现有网关路由/模型访问缺口；不代表模型一般不可用 |
| `gateway-b-gemini-3.7-native` | 未纳入旧四类表 | `completed`，eligible cell 1，约 90.40s | 5/5 stage success，9 calls，4 次节点内 schema 修正，3 条 W2，method/audit error 0；严格 native JSON Schema/canary 仍有限制 |
| `gateway-b-gemini-3.8-native` | 未纳入旧四类表 | `completed`，eligible cell 1，约 83.25s | 5/5 stage success，8 calls，3 次节点内 schema 修正，2 条 W2，method/audit error 0；严格 native JSON Schema/canary 仍有限制 |
| `e1-qwen38-27b` | 完成 | `completed`，eligible cell 1，约 236s | 首次因 detached worktree provenance 被拒；同 commit 的命名干净分支重跑后完成 |
| `e1-qwen36-35b` | 完成 | `completed`，eligible cell 1，约 95s | 最小工作流通过 |
| `e1-gemma4-31b` | 完成 | `completed_with_diagnostics`，eligible cell 1，约 934s | contract-completion 六轮后 `turns limit exceeded`，保留 coverage gap 后落盘 |
| `e1-muse30b` | 完成 | `completed`，eligible cell 1，约 103s | 工作流终态通过；本格没有执行谓词，不能据此声称所有 binder 都被覆盖 |

Gemma 的 provider 持续返回，不能把长延迟归为网络故障。其 contract-completion 工具结构未在预算内收敛，当前 E1 只记录事实，不修改生产 prompt/adapter。Sonnet 的失败可离线复现：`PublicStructuredRuntime` 构造 `httpx.Timeout`，当前 `ChatAnthropic` 的字段校验只接受 float。openai-compatible method 的部分 usage 也未从 adapter 暴露，虽然显式 `stream_usage=True` 的 profile 探针有 usage；因此 workflow cost/usage 完整性不得因负载探针成功而自动勾选。[clm-workflow-status]

当前 structured runtime 还会用 `MAX_STRUCTURED_OUTPUT_TOKENS=10_000` 覆盖部分调用预算；profile 中 32,768/65,536 并不表示 method 每次实际使用同样的上限。负载输入/输出参数与真实 workflow 分开记录，不能用高预算负载通过掩盖 method 的预算差异。源码依据见 [structured_runtime.py](../../../../utils/structured_runtime.py) 的 `call` / `call_async` 与常量；E1 不改这项生产行为。

## 失败与修复记录

1. Qwen3.8 初次服务环境缺 `ninja`，补齐远程环境 PATH 后服务正常；这是依赖问题，不是模型失败。
2. Qwen3.8 默认 thinking/低 output budget 的历史记录有 17/32 或 1/32 截断。改用官方支持的 `reasoning_effort=low` 并将 output 上限设为 65,536 后，新的 16-worker 记录为 32/32。旧失败记录不能删除，也不能写成所有 reasoning 档都通过。
3. Muse 初次 max output=256 时 2K 普通请求全部 `finish_reason=length`，原因是 reasoning channel 消耗了预算；将普通 output 调至 4096、thinking 调至 32768 后分别得到 64/64 和 32/32。该失败说明 output budget 必须随 thinking 模式记录。
4. 初始 Muse tunnel/服务连接失败记录保留；修正 CUDA link/parser 配置后通过。
5. 初始 vLLM 0.28.0 尝试留下 architecture/import/kernel 初始化失败，后续采用 SGLang 0.5.19。本轮没有完成 vLLM 的同等级性能验证，不主张两种框架等价通过。
6. method 初次启动缺失 `genai_prices` / pyfcstm 依赖；在隔离客户端环境补齐后保留新旧记录。Qwen3.8 的 detached worktree 失败在 provider 调用前发生，改用同 commit 的命名干净分支后复跑。
7. Gemini 旧路由探针有 404、500、read timeout 和“HTTP 200 但内容为网站 HTML”；它们都不算推理成功。Gateway B 的 3.7/3.8 native profile 后续 method 已完成，但严格 native JSON Schema、最小 enum schema 与复杂 forced-tool canary 仍有失败或不稳定记录。Sonnet method 退出码为 0 但 pair 状态失败，必须按终态解释。
8. SGLang 日志含 torchcodec 多媒体组件 warning、CUDA header/compiler mismatch 引起的 allreduce fusion fallback；文本请求可运行不等于启动过程没有 warning。
9. Muse 的 JSON response-format 存在占位符内容缺陷；非流式和增加 schema description 的小探针也未消除。function/tool 路径完成后续负载验证；不把原 schema sweep 改写为成功，也不宣称已确定其底层模型/grammar 根因。[clm-muse-routing]

以上旧失败及成功记录都保留在归档，没有以提高成功率为理由删掉失败分母。[clm-serving-failures]

## context 解释

用户要求的“大差不差”具体化为 `floor(0.9 * declared_limit)`。原生窗口与官方有 recipe 的扩展都需达到目标；本轮 Qwen 两款扩展已实际启用且达到 0.9。边界请求为低并发、输出预算 4096 的容量探针（Muse 最终为 high reasoning/tool，其余边界非 thinking），task 位于合成 padding 末端；16 workers 则在约 16K 输入测试。两者不能合起来宣称 16 个 900K 请求同时满足延迟目标，也不证明长距离检索/推理准确率。[clm-serving-capacity]

## E2 交接

- 商用讨论候选：Luna + Gateway B 的 Gemini 3.7/3.8 native 路径；Gemini 3.5 的旧渠道仍 blocked，Sonnet/Haiku 为低优先级替代。E2 名单尚未冻结，严格 native schema/canary 限制和成本资格仍需在最终讨论中单独考虑。
- 开放模型优先保留 Qwen3.8；另一款在 Gemma4 的独立模型族覆盖与 Muse 的工作流稳定性之间讨论。Qwen3.6 也是已实测的替代。名单未冻结，不能根据这一个 pair 的问题数量选优。
- 四款开放模型都具备远程容量/负载证据；Gemma 的 method 降级和 usage 缺口仍需纳入正式运行前判断。[clm-handoff]
- 本文件不提供 defect-ledger 命中、precision、人工确认量或方法优越性结论；E2 必须新建正式 run record，并将 provider 错误、schema/truncation、partial run 和 eligibility 分开统计。

## 可复现部署

版本：SGLang 0.5.19、torch 2.13.0、transformers 5.12.1、flashinfer-python 0.6.18、nvidia-cuda-nvcc 13.3.73、ninja 1.13.2。客户端为隔离环境：pyfcstm 0.6.0、genai-prices 0.1.3、langchain-core 1.6.2、langchain-openai 1.2.2、langchain-anthropic 1.4.4、langchain-google-genai 4.4.0。生产依赖未修改。[src-infrastructure]

| 模型 | HF revision | SGLang reasoning / tool parser |
|---|---|---|
| Qwen3.8 | `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` | `qwen3` / `qwen3_coder` |
| Qwen3.6 | `995ad96eacd98c81ed38be0c5b274b04031597b0` | `qwen3` / `qwen3_coder` |
| Gemma4 | `842da3794eaa0b77d5f08bae87a17459d91ff475` | `gemma4` / `gemma4` |
| Muse | `a4e59da52a7bc87ae7251dd5545c0dd437c44b68` | `muse` / `muse` |

官方依据为 [Qwen3.8 卡](https://huggingface.co/Qwen/Qwen3.8-27B)、[Qwen3.6 卡](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)、[Gemma4 卡](https://huggingface.co/google/gemma-4-31B-it)、[Gemma vLLM recipe](https://recipes.vllm.ai/Google/gemma-4-31B-it)、[Muse 卡](https://huggingface.co/meta-models/Muse-Glimmer-30B)、[Muse vLLM recipe](https://recipes.vllm.ai/meta-models/Muse-Glimmer-30B)。后两者的官方/框架示例以 vLLM 为主；本轮用 SGLang 已有相应 parser 实测服务接口，TP2/TP4 是 H200 分配下的实测配置，不能称为作者原封不动的默认命令。Muse 最终负载使用官方推荐 system prompt `Reasoning strength: high`、temperature 1.0 / top_p 0.95 / top_k 64；早期负载和 method smoke 未注入该行，二者不混作同一推理档。[src-serving-recipes]

以下仅在远程已分配 GPU 的新 tmux 工作区执行。`SHARED_STORAGE` 由操作者指向该节点的共享盘；不在本机执行下载或服务命令。不要对现有工作负载执行宽泛 kill。

```bash
export E1_ROOT="${SHARED_STORAGE:?}/paper1-e1"
export HF_HOME="$E1_ROOT/hf" XDG_CACHE_HOME="$E1_ROOT/cache" TMPDIR="$E1_ROOT/tmp"
export UV_CACHE_DIR="$E1_ROOT/cache/uv" PIP_CACHE_DIR="$E1_ROOT/cache/pip"
mkdir -p "$HF_HOME" "$XDG_CACHE_HOME" "$TMPDIR"
df -h "$E1_ROOT"
uv venv --python 3.12 "$E1_ROOT/sglang-env"
uv pip install --python "$E1_ROOT/sglang-env/bin/python" \
  'sglang==0.5.19' 'torch==2.13.0' 'transformers==5.12.1' \
  'flashinfer-python==0.6.18' 'nvidia-cuda-nvcc==13.3.73' 'ninja==1.13.2'
export PATH="$E1_ROOT/sglang-env/bin:$PATH"
export CUDA_HOME="$E1_ROOT/sglang-env/lib/python3.12/site-packages/nvidia/cu13"
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:$CUDA_HOME/lib:${LD_LIBRARY_PATH:-}"
hf download Qwen/Qwen3.8-27B --revision 1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0
export CUDA_VISIBLE_DEVICES=0,1,2,3 HF_HUB_OFFLINE=1
export SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1
python -m sglang.launch_server --model-path Qwen/Qwen3.8-27B \
  --revision 1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0 \
  --served-model-name qwen3.8-27b --host 127.0.0.1 --port 8100 \
  --tp-size 4 --context-length 1000000 --mem-fraction-static 0.92 \
  --max-running-requests 64 --reasoning-parser qwen3 --tool-call-parser qwen3_coder \
  --default-chat-template-kwargs '{"reasoning_effort":"low"}' \
  --json-model-override-args '{"text_config":{"rope_parameters":{"mrope_interleaved":true,"mrope_section":[11,11,10],"rope_type":"yarn","rope_theta":10000000,"partial_rotary_factor":0.25,"factor":4.0,"original_max_position_embeddings":262144}}}'
```

运行时实际使用下载后的 snapshot 路径，精确启动 args 见 `servers/*-final-server.json`。在另一远程工作区切换模型时，用上表 revision/parser、容量表 TP/context；仅两款 Qwen 使用 YaRN override，且只有 Qwen3.8 设置 reasoning-low。Muse/Gemma 不需要 Qwen 的 RoPE 配置。环境的 CUDA 工具链路径需要实际存在；原运行修复过库目录链接，日志中的 fusion fallback 保留，以上 pin 不是所有平台通用的 CUDA 安装器。

本机只建立 tunnel：`ssh -N -L 127.0.0.1:8100:127.0.0.1:8100 REMOTE_NODE`。profile 示例由以下字段组成，凭据文件保持 600 且不入库；四个 profile 共用一个端口意味着一次只服务一款，不能同时启动四款实验。

```yaml
default: e1-qwen38-27b
profiles:
  e1-qwen38-27b:
    adapter: openai
    base_url: http://127.0.0.1:8100/v1
    api_key: local-not-used
    model: qwen3.8-27b
    context_window_tokens: 1000000
    max_output_tokens: 65536
```

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件，新建接入快照 | `git log --diff-filter=A --follow -- <本文件路径>` | 本轮冻结时间 | 新增实测汇总与限制 | 无历史迁移 | 逐请求 JSONL、workflow receipts、远程日志；协议起点 `14ffb4029`，workflow 源码 `2971a8ada` |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-load-client] | load_client | [load_client.py](./load_client.py)、[protocol.md](./protocol.md) | source-code/md | 输入、输出与资格规则 | `SCHEMA`、`request_one`、`eligible`、Measurements |
| [src-load] | load | [probes.zip](./evidence/probes.zip)、[load_summary.json](./evidence/load_summary.json) | zip/json | 容量、延迟、成功与失败 | `results/*/requests.jsonl`，filter `warmup=false`，按 concurrency 分组；Qwen `yarn900k/yarn909k/yarn-long16k-thinking`，Gemma `context90/long16k-thinking-final`，Muse `high-tool-*`；旧失败 member 全部保留 |
| [src-workflows] | workflows | [probes.zip](./evidence/probes.zip) | zip | 当前接口和工作流状态 | `probes/*/*.json`、`workflows/*/{baseline*,method*}/probe.json`、`artifacts/*/summary.json`、stage `result.json` / `audit.jsonl` |
| [src-infrastructure] | infrastructure | [probes.zip](./evidence/probes.zip) | zip | 版本、revision、启动和失败 | `infrastructure.json`、`servers/*-final-server.json`、`remote_logs/*`；下载 JSON 的 revision；startup 日志 |
| [src-serving-recipes] | recipes | [sources.zip](./evidence/sources.zip) | zip | 官方配方与实际偏差 | `qwen38_27b_card.raw`、`qwen36_card.raw`、`gemma4_31_card.raw`、`gemma4_recipe_actual.raw`、`muse30_card.raw`、`muse30_recipe_actual.raw` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-serving-environment] | E1-ENV | 远程服务、权重与固定 GPU 分配 | trace | [src-infrastructure] disk/versions/server args；[src-load-client] loopback 限制 | [cmd-serving-offline]；日志人工复验 | high | GPU 状态是快照，不是整个运行期间的资源隔离证明 |
| [clm-serving-capacity] | E1-CAP | 四款 0.9 边界和 16K thinking 16-worker 全部完成 | count | [src-load] usage、eligible、latency；具体 sweep 见 A.2 | [cmd-serving-offline] | high | 合成负载；不证明效果、全天稳定性或最大窗口高并发 |
| [clm-workflow-status] | E1-WORKFLOW | API 可用与 method 终态/降级分别记录 | classification | [src-workflows] pair status、diagnostics、stage result；[src-infrastructure] 同次服务日志 | [cmd-serving-workflow] | high | 单 pair；未覆盖所有谓词和输入形态；不构成 E2 正式结果 |
| [clm-serving-failures] | E1-FAILURES | 失败、截断、依赖缺口原样保留并归类 | risk | [src-load] 失败 sweep；[src-workflows] 旧 attempts；[src-infrastructure] startup warnings/errors | [cmd-serving-offline]，日志人工核对 | high | 根因只写有直接异常/配置证据的部分 |
| [clm-muse-routing] | E1-MUSE-ROUTING | Muse JSON 模式内容失败，function/tool high 路径有具体参数 | classification | [src-load] `muse-high-tool-{long16k,context90,short32}` 的 tool_arguments；[src-workflows] `probes/muse-routing-diagnostic.json` | [cmd-serving-offline]；人工复验 32+2 条 tool 参数 | high | 字面占位检查不等于语义 grader；prompt/协议已变，不作受控效果对比；底层原因未证实 |
| [clm-handoff] | E1-HANDOFF | 模型选择仍开放，接入缺口限制正式运行 | decision | [clm-workflow-status]、[clm-serving-capacity] | 人工复验 | medium | 推荐不构成名单冻结，不能依据本格效果选优 |

### A.4 复验命令

[cmd-serving-offline] 校验脱敏后所有 archive member 哈希，并从逐请求记录重算全部 sweep（含失败）。嵌入的原始 run hash 对应脱敏前字节，不能用它要求脱敏文件 byte-identical；这些导出仅为诊断证据，`formal_result_eligible=false`。

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_evidence.py
```

[cmd-serving-workflow] `probes.zip` 的 `clients/run_workflow_probe.py` 记录命令构造；workflow 终态按 `per_pair/0001/status` 和 `metrics/method/eligible_method_cells` 核验。需重新调用时从干净、具名分支启动，以下是原 probe 的 method 命令形状；不得用于全量实验。

```bash
LLM_CONFIG_FILE="$PRIVATE_CONFIG" PYTHONPATH=".:project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src" \
python -m paper_stm_method.cli \
  --report-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60 \
  --output-dir "$NEW_SMOKE_OUTPUT" --profile e1-qwen38-27b \
  --rounds 1 --pair-id 0001 --workers 1 --transport-retries 0 --allow-live
```
