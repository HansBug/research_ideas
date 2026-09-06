# `utils`：LLM 与 Agent 基础设施

本文档是根级 `utils` 的中文公共 API 指南。基础实现以 [Issue #155](https://github.com/HansBug/research_ideas/issues/155) 为设计稿，强实时输出与阶段耗时以 [Issue #159](https://github.com/HansBug/research_ideas/issues/159) 为合同；Issue、本文档和测试必须保持同步。

设计只解决五件事：保存 LLM 配置、装配一个真实 Agent、自动管理可审计上下文、实时观察运行、把完整结果交给下游实验。没有自有 LLM client、Fake、离线 demo、checkpoint、memory、multi-agent 或 paper1 业务逻辑。配置、事件和结果不设置版本号，直接维护当前公开结构。

## 1. 首次配置

`.env` 只用于一次性初始化。初始化把 endpoint、API key 和 model 直接写入根目录的 ignored `.llmconfig.yml`；文件权限必须是 `0600`，之后运行代码直接读取 YAML，不需要再次 `source .env`。

```bash
source .env
python -m utils.llm init --from-env --profile gpt-5.5 --context-window-tokens 1050000 --max-output-tokens 128000
```

`init --from-env` 只读取 `LLM_ENDPOINT`、`LLM_API_KEY`、`LLM_MODEL`。配置文件不写 `*_env`、stream、retry、timeout、snapshot 或 model source。真实 key 不得提交或写入日志、Issue、运行记录或测试 fixture。

文件结构保持直接明了：

```yaml
default: gpt-5.5
profiles:
  gpt-5.5:
    adapter: openai
    base_url: https://api.example.invalid
    api_key: replace-me
    model: gpt-5.5
    context_window_tokens: 1050000
    max_output_tokens: 128000
```

示例中的地址和 key 只是无效占位值；本地文件才写入真实直接值。

```bash
python -m utils.llm validate --require-credentials
python -m utils.llm list --format json
python -m utils.llm show gpt-5.5 --format json
git check-ignore -v .llmconfig.yml
```

当前 `gpt-5.5` profile 显式保存官方 1,050,000 context window 和 128,000 max output；通用字段允许缺省。官方依据：[GPT-5.5 模型页](https://developers.openai.com/api/docs/models/gpt-5.5)。

## 2. 公共 API

下游只从包根导入，不依赖 `utils.agent` 或 `utils.llm` 的内部文件。

### 2.1 `utils.llm`

```python
from utils.llm import (
    LLMConfig,
    LLMModelFactoryError,
    LLMPricing,
    LLMRegistry,
    LLMTokenPrices,
    PromptCacheTTL,
    adapter_name,
    cached_system_prompt_content,
    collect_usage_sources,
    create_chat_model,
    default_stream_usage,
    estimate_usage_cost_usd,
    load_llm_registry,
    model_kwargs,
    normalize_model_output_usage,
    normalize_usage,
    prompt_cache_policy,
)
```

```python
class LLMConfig(BaseModel):
    adapter: Literal["openai", "openai-responses", "anthropic", "deepseek", "google-genai"] = "openai"
    base_url: str | None = None
    api_key: SecretStr | None = None
    model: str
    context_window_tokens: int | None = None
    max_output_tokens: int | None = None
    stream_usage: bool | None = None
```

只有 `model` 必填；`adapter` 可省略且严格默认为 `openai`。`adapter` 显式选择 LangChain client 与传输协议，不表示实际 provider 或 endpoint：`openai` 与 `openai-responses` 都使用 `ChatOpenAI`，但分别固定走 Chat Completions 与 Responses；`anthropic`、`deepseek` 分别对应 `ChatAnthropic`、`ChatDeepSeek`。运行时不根据 model 名或 host 猜测传输协议。其他字段为 `None` 时，Agent 构造模型时不传对应参数。`LLMRegistry` 是只读 `Mapping[str, LLMConfig]`：

```python
registry = load_llm_registry()
config = registry["gpt-5.5"]
config = registry.default
registry.default_name
registry.names()
```

`stream_usage` 可在 profile 中显式设置，适合已经验证支持 usage 的自托管兼容端点。缺省时保留 provider 安全默认；调用方显式参数优先于 profile。该字段仅在显式配置时加入公开配置与 fingerprint，因此不改变旧 profile 的身份。`PublicStructuredRuntime` 给 Anthropic 传浮点 timeout，OpenAI/DeepSeek 保留 `httpx.Timeout` 以隔离 async client 生命周期。

`PublicStructuredRuntime` 的 stream 首字节及读取空闲等待为 300 秒，单次模型调用总时限为 600 秒；长输入 prefill、推理和工具参数缓冲均可能超过旧 30 秒边界。阶段与外层时限按现有调用配额和 grace 自动推导：零 transport retries 时为 3630 / 3660 秒，不增加原有六次调用配额。非流式调用仍可用于诊断，但不能替代要求 stream 的接入验收。运行 manifest 和 structured outcome 记录实际时限；该调整不改变输出预算映射、prompt、schema 或 eligibility。Google SDK 的 HTTP 状态从 typed `APIError.code` 读取，504 等归入 provider 错误，不能误记为 schema 失败。

路径优先级为显式参数、`LLM_CONFIG_FILE`、根 `.llmconfig.yml`。加载器不访问网络、不创建 client、不维护全局可变单例。公开摘要必须脱敏；`api_key` 不能打印。
`adapter: google-genai` 使用官方 `langchain-google-genai` 的 `ChatGoogleGenerativeAI`，固定连接 Gemini Developer API。`base_url` 填 API 根地址，由 SDK 追加 `/v1beta/models/...`，不要填 OpenAI 兼容路径 `/v1`。凭据仍来自 profile；不从环境变量选择 Vertex AI。原生流自带 usage，不发送 OpenAI 的 `stream_usage` 参数。

当前 pin 的 LangChain 版本没有把 `vertexai=False` 继续传给 Google SDK。因此若环境设置 `GOOGLE_GENAI_USE_VERTEXAI=true`，构造时会明确报错，防止 SDK 静默改走 Vertex AI；清除该环境设置后按 profile 连接。

直接调用 `create_chat_model(config).with_structured_output(Schema, method="json_schema", include_raw=True)` 会通过官方 adapter 发送 `responseMimeType` 与 `responseJsonSchema`。`AgentApp` 继续使用原有 `ToolStrategy`，不会因为模型族而切换方法或解析规则。网关是否兑现 schema 和 forced-tool 约束需要真实验证，添加 adapter 本身不代表某个网关已健康。

Google 的单次调用输出上限会从公共 `max_tokens` 映射到 `max_output_tokens`。显式 `reasoning_effort` 支持 `minimal`、`low`、`medium`、`high`，具体型号仍需支持该档位；不把 `none` 映射成关闭思考。未指定思考控制时记录 provider default（`effective_think_mode=None`），避免把 Gemini 3 的默认思考误报成关闭。原生 timeout 使用秒数，持久 runtime 负责关闭 Google SDK 的同步与异步连接。

`PublicStructuredRuntime` 的真实调用默认沿用 profile 中经核验的 `max_output_tokens`，不再添加统一 10K 覆盖值；缺少该配置时明确报错。显式调用覆盖值在共用适配层先映射为 OpenAI 的 `max_completion_tokens`、Google 的 `max_output_tokens` 或其他适配器的 `max_tokens`，避免 Responses SDK 合并别名时让构造值覆盖调用值。审计逐调用保存 profile、显式覆盖值、请求输出上限及 provider 的 finish/stop/incomplete 信息；请求上限不等于实际生成量，也不等于服务端结合输入和剩余 context 后的最终容量。Anthropic 持久 runtime 使用由自身创建和关闭的异步 HTTP 客户端，避免跨事件循环复用已关闭的连接。

仅当兼容 API 已验证省略输出字段会使用全部剩余 context 时，可配置 `output_budget_mode: remaining_context`，并令 `max_output_tokens` 等于部署窗口以记录容量声明。该模式省略 HTTP 输出限额，审计来源为 `provider_remaining_context`；不能用于省略字段会落回小默认值的渠道。SGLang 0.5.19 的 Chat Completions 默认将 `max_new_tokens=None` 传给调度器，再以完整输入、总窗口和 KV 页容量约束输出；须保持输入自动截断关闭，并另存引擎版本、源码及实际配置证据。

接入依据：[LangChain Google 集成](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)、[Gemini 结构化输出](https://ai.google.dev/gemini-api/docs/structured-output)、[generateContent 参数](https://ai.google.dev/api/generate-content)。

### 2.2 `utils.agent`

稳定导出只有：

```python
from utils.agent import AgentApp, AgentError, AgentEvent, AgentRunResult, AgentSpec
```

```python
AgentSpec(
    name: str,
    system_prompt: str,
    tools: tuple[BaseTool | Callable, ...] = (),
    output_schema: type[BaseModel] | None = None,
    limits: Mapping[str, int | float | None] | None = None,
    require_tool_call: bool = False,
    retry_missing_structured_output: bool = False,
)
```

`limits` 默认是空或 `None`，表示不设置 Agent 框架上限。需要限制时直接写少量键：

```python
spec = AgentSpec(
    name="bounded-agent",
    system_prompt="先使用工具，再回答。",
    tools=(lookup_note,),
    limits={"model_calls": 20, "tool_calls": 50, "turns": 30,
            "seconds": 900},
    require_tool_call=True,
)
```

限制键只有 `model_calls`、`tool_calls`、`turns`、`seconds`。未设置限制时不因为调用次数、轮数或时间主动失败；同一轮的多个已注册业务工具调用也正常交给 LangGraph `ToolNode` 执行。`tools` 同时是 allowlist：未知工具、业务工具与结构化终止在同一轮混合时，在 ToolNode 执行前直接失败；工具异常和结构化输出校验失败仍按运行错误处理。这些是行为边界，不是复杂预算策略。

`require_tool_call=True` 要求整次运行至少成功调用过一个业务工具。对于 provider 偶发以空白或普通文本结束、但方法协议明确要求结构化终止的 Agent，可显式设置 `retry_missing_structured_output=True`：runtime 会保留完整、符合 provider tool-message 协议的可见历史，追加一条带 hash 的恢复上下文，并在这条恢复路径中要求模型选择业务工具或结构化终止工具。如果 provider 把末尾损坏的结构化调用保存在 `invalid_tool_calls` 或原始 `tool_calls` 中，runtime 会把该次失败提交记为 `rejected` 并从回放历史中排除。若末尾是参数无法解析、从未执行且名称属于当前 allowlist 的业务工具调用，也允许以相同方式保留拒绝审计并重试；动态 mandatory resolver 仍优先强制当前尚未完成的具体工具。正常业务工具调用缺少结果、未知工具、混合调用、历史中段损坏或无法归因的悬空调用一律 fail-closed，不会伪造工具结果。该机制只在 graph 已结束且 `structured_response` 缺失时启动一次，不限制整次运行的模型调用、工具调用、时间或 token，也不解析普通文本伪造结构化结果。

限制计数是整个 `run` 的累计值；compact summary transport 也计入显式 `model_calls`，但不计业务 turn/tool。`context_window_tokens` 与 `max_output_tokens` 都是可选配置；缺省时把容量交给 provider，不在本地擅自猜测数值。

`seconds` 是从 `run_started` 到 `completed/failed/cancelled` 的 wall-clock 上限，包含 provider 等待、工具执行和写出结果的时间；普通同步工具在线程中执行，不阻塞 heartbeat。

```python
AgentApp.from_registry(
    spec: AgentSpec,
    registry: LLMRegistry,
    profile: str | None = None,
    *,
    model_options: Mapping[str, Any] | None = None,
) -> AgentApp

AgentApp.from_config(
    spec: AgentSpec,
    config: LLMConfig,
    *,
    profile: str = "direct",
    model_options: Mapping[str, Any] | None = None,
) -> AgentApp
```

`from_registry` 是下游实验首选入口；省略 `profile` 使用默认 profile。`model_options` 只允许 `streaming`、`stream_usage`、`timeout`、`max_retries` 四个构造选项，不写入 YAML，也不能覆盖 `model`、`base_url`、`api_key`、`headers` 或身份相关参数；未知键直接失败。配置缺少 `api_key` 时运行前失败，不从环境变量静默回退。

结果中的 `model` 是 profile 中实际传入的模型 ID，`observed_model` 来自 provider 响应（若 provider 返回）；真实 demo 默认使用 `gpt-5.5`，也允许通过 `--profile` 选择其他已配置模型，结束后若 provider 返回了不同 model 也失败，不把错误模型标成真实 demo 成功。

```python
app.run(
    input_text: str,
    *,
    context: Sequence[str | Mapping[str, Any]] | None = None,
    renderer: str = "auto",
    log_level: str = "INFO",
    on_event: Callable[[AgentEvent], None] | None = None,
    audit_out: Path | None = None,
    result_out: Path | None = None,
    think_mode: bool = False,
    reasoning_effort: str | None = None,
    compact_trigger_ratio: float | None = 0.85,
    model_call_options: Mapping[str, Any] | None = None,
) -> AgentRunResult

await app.arun(input_text, context=context, renderer="auto", think_mode=False,
               tool_choice_resolver=None, tool_choice_policy_name=None, ...) -> AgentRunResult
```

`renderer` 使用 `auto`、`rich`、`jsonl` 或 `quiet`；`log_level` 使用标准 logging 的 `DEBUG`、`INFO`、`WARNING`、`ERROR`。`INFO` 显示 Agent 阶段、模型可见输出、工具参数/结果和最终结果；heartbeat 只在 `DEBUG` 显示。`auto` 会按终端环境选择适合的人类可读输出；`arun` 是已有 event loop 时的入口；`run` 只用于普通同步脚本。`model_call_options` 只作用于当前推理，不能携带 secret、覆盖 profile 身份或重复设置 think/reasoning；允许的键为 `temperature`、`top_p`、`stop`、`seed`、`verbosity` 与 `max_tokens`，其中只有 `max_tokens` 可以覆盖单次 output reserve。

`think_mode` 默认关闭，所有模型都必须显式传入 `True` 才会开启 provider 的 thinking/reasoning 模式；`reasoning_effort` 只有在 `think_mode=True` 时才可传入。`openai-responses` adapter 在 think-off 时统一发送 `reasoning_effort=none`，不按模型名或 endpoint 猜测；因此只应给接受该 Responses reasoning 合同的 profile 使用。当前 Anthropic adapter 不开放 extended thinking，因为 Anthropic 不允许 thinking 与框架的强制工具选择同时使用；显式开启时配置阶段直接失败，不静默弱化必用工具合同。模型请求默认 `streaming=True`；`stream_usage` 的安全默认值由 runtime adapter 统一决定：Anthropic 与官方 OpenAI endpoint 默认开启，DeepSeek 与其他 OpenAI-compatible endpoint 默认关闭，调用方仍可在 `model_options` 中显式覆盖。Anthropic adapter 还会在底座层自动安装官方 `AnthropicPromptCachingMiddleware`，以 5 分钟 ephemeral cache 标记静态 system prompt、工具定义和可缓存消息前缀；业务 Agent、prompt 和工具不感知 provider 细节。每次调用的 `input_tokens`、`output_tokens`、`total_tokens`、`cache_read`、`cache_creation` 以及可用时的 `ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens` 都写入 audit/result；原始 Anthropic usage 仅提供未缓存输入量时，runtime 会把缓存读取和写入量补回真实 input/total 口径。YAML 不保存这些单次运行参数；缺少 terminal usage 时审计记录 `unavailable`。`seed`、`verbosity` 等 OpenAI 专属调用参数不会透传给 Anthropic。

当某个方法阶段存在由 Controller 定义、但参数必须由 Agent 生成的必用工具顺序时，
可以同时传入 `tool_choice_resolver` 与稳定的 `tool_choice_policy_name`。resolver 在每次
主模型调用前返回一个必用业务工具名或 `None`；返回工具名时 runtime 临时隐藏结构化
终止 surface，并把该轮可见工具面收窄为这一个工具，既避免 LangChain `ToolStrategy`
把指定工具覆盖成 `tool_choice=any`，也避免 provider 忽略精确工具选择后改调其他工具。
resolver 返回 `None` 后恢复完整工具面与正常结构化输出。该接口不能用于代替 Agent 生成业务参数或
裁决结果；policy 名会进入行为指纹和 audit，二者必须同时提供。

官方依据：OpenAI [reasoning effort](https://developers.openai.com/api/docs/guides/reasoning) 与 [gpt-5.5 model page](https://developers.openai.com/api/docs/models/gpt-5.5)；Z.AI [GLM-5.2](https://docs.z.ai/guides/llm/glm-5.2) 与 [Thinking Mode](https://docs.z.ai/guides/capabilities/thinking-mode)；DeepSeek [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode) 与 [API quick start](https://api-docs.deepseek.com/guides/reasoning_model)。

`adapter: openai` 使用 `langchain-openai` 的 `ChatOpenAI` 与 Chat Completions；`adapter: openai-responses` 使用同一官方集成的 Responses transport，适用于 Codex/Responses-compatible endpoint。`adapter: anthropic` 使用 `langchain-anthropic` 的 `ChatAnthropic` 与原生 Messages API；`adapter: deepseek` 使用 `langchain-deepseek` 的 `ChatDeepSeek`。DeepSeek 虽兼容 OpenAI Chat Completions，但专用 adapter 会保留 `reasoning_content`、DeepSeek model profile 和 tool/structured-output 兼容语义，因此不降级为普通 `ChatOpenAI`。Anthropic `base_url` 必须是 API 根地址，例如 `https://api.anthropic.com` 或中转站根地址，由 SDK 追加 `/v1/messages`。各路径保持 `streaming=True`、LangGraph `ToolStrategy`、同一 Rich 事件顺序和同一 audit 契约，不在 runtime 手写 provider 消息转换或 JSON 后处理。

Rich 输出按 LLM I/O 顺序组织：`MODEL INPUT` 是本轮交给模型的 system/user/tool messages，并在 provider transport 开始前立即显示；`MODEL OUTPUT` 是流式 assistant 文本、完整 tool call 或结构化 call，完整 tool call 在 ToolNode 进入工具函数前已经显示；工具返回后立即显示 `TOOL RESULT -> NEXT MODEL INPUT`，下一轮 input 再把它作为 `[tool]` message 交给模型。`CONTEXT` 只保留两行消耗摘要，结构化最终结果只在 `AGENT COMPLETE` 中完整展示一次。同步和异步 callable 都由 LangChain `StructuredTool` / LangGraph ToolNode 执行，运行时不自行调度或 await 业务工具。

结构化结果通过 `create_agent(response_format=ToolStrategy(YourSchema))` 交给 LangGraph 官方 tool-calling structured output。这里显式指定官方 `ToolStrategy`，用于保持 `model_copy()` 改造前由 `RunnableBinding` 触发的跨 provider 行为，避免 OpenAI-compatible provider 被 AutoStrategy 误选为其不支持的 provider-native `response_format`。运行时不把普通 assistant 文本自行 `json.loads` 成结果，也不为某个 provider 另写一套结构化后处理；provider 不支持或返回无效结构时保留原始失败诊断。

官方 tool-calling fallback 的 schema 校验重试由 LangGraph 自己管理；默认不额外增加恢复路径。只有 AgentSpec 显式开启 `retry_missing_structured_output` 时，才在 graph 无结构化终止后追加一次可审计恢复上下文。需要为不兼容 provider 设置止损时，显式传 `limits`（例如 `model_calls` 或 `seconds`），失败结果会保留 `structured_output_invalid`/provider 诊断和 audit `finish`。

终端按消息顺序显示：第一次模型请求显示一次 system/user 消息，后续请求只显示新增的 tool 消息；已经显示的历史不会每轮重复打印。assistant 输出、tool 参数和 tool 返回紧随对应消息出现。超长可见内容保留头尾，中间只做明确的长度标记；`audit_out` 仍保存完整的可审计内容。每个 tool Panel 都明确标出 `name`、`tool_call_id`、`status`、`arguments`，结果 Panel 还标出 `result`；工具异常会标出安全的 `error`，DEBUG 时补充异常类型和 provider request id 等诊断字段。现有块内附带紧凑耗时：input 为 `t=+X.XXXs`，assistant/tool request 为 `model=X.XXXs` 和可用时的 `first_chunk=X.XXXs`，tool result/error 为 `queue=X.XXXs` 与 `execution=X.XXXs`，最终块为整次 run duration；不另建 timing Panel。

运行时不会改写、追加或重排调用方提供的 `system_prompt` 和任务输入。若实验需要可见的计算步骤、依据、工具结果或总结，直接把要求写进调用方自己的 prompt 或输出 schema；框架只展示模型实际返回的内容，不生成或猜测隐藏思维链。`model_started.data.prompt` 和 Rich 的 MODEL INPUT 面板会展示经过脱敏的可见输入，这是实时观察契约的一部分；学术审计同样只保存脱敏后的上下文事实。

`context` 是本次运行的有序上下文页面，不需要额外的上下文类：

```python
context = [
    {"id": "record-001", "hash": "sha256:...", "text": "不可变事实一"},
    {"id": "record-002", "hash": "sha256:...", "text": "不可变事实二"},
]
result = app.run("分析这些事实", context=context, renderer="rich")
```

也可以直接传字符串，运行时会按顺序编号。mapping 至少包含 `text`，推荐同时提供 `id`、`hash`、`snapshot`、`cursor`、`source`；hash 必须等于规范化 text 的 SHA-256，重复 id、hash 不匹配或同一运行内 snapshot 漂移直接失败。compact 阈值使用 LangChain 官方 `max_input_tokens`/`context_window_tokens`，按 `floor(context_window_tokens * compact_trigger_ratio)` 触发，不从官方输入窗口擅自扣减单独的 `max_output_tokens`；`safe_input_tokens` 只是该官方输入容量的公开别名。默认保留最近 20 条消息，摘要仍由同一模型和推理设置完成。`compact_trigger_ratio=None` 禁用自动 compact，窗口未知时不猜测容量并记录 `compact unavailable`。compact 会把官方 summary replacement 写回 LangGraph state，后续任务继续使用新上下文，不重放工具、不启动额外上下文流程。实现对应 [LangChain 短期记忆与 SummarizationMiddleware](https://docs.langchain.com/oss/python/langchain/short-term-memory)；容量和 usage 字段以 [GPT-5.5 官方模型页](https://developers.openai.com/api/docs/models/gpt-5.5) 与 [Reasoning usage 文档](https://developers.openai.com/api/docs/guides/reasoning) 为准。

每个 primary turn 结束后只输出一个最多两行的 `CONTEXT` Panel，保持高信号而不重复历史：

```text
turn 2 · 487 in + 96 out = 583 · cache_read=320 · cache_creation=0 · reasoning=0
context ~1,240/1,050,000 tokens (0.1%) · compact@892,500 (85%) not required
```

第一行只说明本轮核心消耗 `input + output = total`，provider 返回时追加 `cache`/`reasoning`；第二行只说明整体上下文的 `used/window`、占比和百分比，再给 compact 阈值及状态。`~` 表示使用了 LangChain 公共估算补足 provider 未返回的输入锚点；不会把 output/reasoning 重复加进 input，也不会从 input 扣除 cache。provider 没有 terminal usage 时第一行明确标记 unavailable，第二行仍可使用公共估算。达到阈值且还要继续时标记 `REQUIRED`，最终轮标记 `run ending`。compact 生命周期使用 `compaction_started`、`compaction_summary`、`compaction_completed`/`compaction_failed`；官方 summary transport 也发出带 `model_call_id` 的 `model_started`/`model_completed` 事件，但 Rich 不再重复渲染一套 MODEL INPUT/OUTPUT 面板。

`AGENT RUN` 启动面板是本次实验的行为配置快照，固定展示会改变模型决策或运行边界的有效配置：profile/model、实际 adapter、脱敏 config/endpoint fingerprint、stream/stream_usage、think/reasoning、sampling、SDK retry / transport retry / timeout、system/tools/input/context 的行为指纹、system/task 字符数、context 页数、工具 allowlist/数量/是否必须调用、结构化输出策略、显式 limits、context/max-output/safe-input 容量来源，以及 compact ratio/threshold/summary 保留策略。它不会显示 raw endpoint、API key、原始 prompt 或文件路径；长度和 hash 只用于复现实验输入，不代替 `MODEL INPUT` 的实际可见消息。

底层 provider SDK 默认保持 `max_retries=0`，避免不可审计的静默重试。`AgentApp` 在完整 ModelResponse 形成之前遇到 `RemoteProtocolError`、`incomplete chunked read`、连接/读取超时、HTTP 408/409/429/500/502/503/504 等瞬时传输故障时，会对同一有效 ModelRequest 最多透明重发两次，默认等待 `5s`、`20s`，provider 给出数值型 `Retry-After` 时优先采用。重发严格保留 profile、model、messages、tools、tool choice、response schema 与推理参数；不完整响应从 Agent history 丢弃，业务工具只在完整响应返回后执行。每个 provider attempt 仍有独立 usage，`transport_retry` audit record 和实时事件记录请求指纹、失败/成功 model call ID、attempt、等待时间、错误与恢复/耗尽结果；两次重发均失败时 run 以 `provider_error` 结束，不切换模型、endpoint 或代理。

```python
AgentEvent(
    run_id: str,
    seq: int,
    timestamp: datetime,
    kind: str,
    data: dict[str, JSONValue],
)

AgentRunResult(
    run_id: str,
    status: str,
    output: Any,
    final_text: str,
    tool_calls: list[dict],
    usage: list[dict],
    error: dict | None,
    real_llm: bool,
    model: str,
    observed_model: str | None,
    academic_eligible: bool,
    context_manifest_hash: str | None,
    profile: str,
    context_window_tokens: int | None,
    max_output_tokens: int | None,
    safe_input_tokens: int | None,
    capacity_source: dict[str, str],
    eligibility_scope: str,
    eligibility_reasons: list[str],
    trace_commit_id: str | None,
    model_calls_used: int,
    model_calls_reserved: int,
    compact_count: int,
    started_at_utc: str | None,
    ended_at_utc: str | None,
    duration_seconds: float | None,
)
```

`status` 只有 `success`、`failed`、`cancelled`；上下文无法无损继续时使用 `status="failed"` 和 `error.code="context_budget_exceeded"`。`real_llm` 在公共真实运行中为 `True`，仅测试目录的内部桩可以为 `False`，测试结果不得作为真实实验制品。

事件 `kind` 使用简单字符串：`run_started`、`heartbeat`、`context_loaded`、`context_usage`、`context_failed`、`model_started`、`model_text`、`model_completed`、`model_failed`、`tool_started`、`tool_completed`、`tool_failed`、`compaction_started`、`compaction_summary`、`compaction_completed`、`compaction_failed`、`structured_output`、`completed`、`failed`。每个模型 transport（包括 official compact summary）都带 canonical `model_call_id` 与 `call_kind`；结构化输出事件也带产生它的 `model_call_id`。compact 的开始/成功/失败事件都带唯一 `compaction_id` 和 `source_refs`，summary transport 与 replacement 通过该 ID 对账。`seq` 从 1 递增，普通观察事件的 data 不得包含 key、headers、raw response 或 hidden reasoning。context 预检失败也走 `run_started -> context_failed -> failed`，同时写入 audit `context` 与 `finish`，不会在错误发生前启动模型。

每个 primary/compact model call 的 event、`result.usage`、`decision`/compact `context` 和 `finish.usage` 使用同一 timing snapshot：

```text
started_at_utc
first_chunk_at_utc
ended_at_utc
duration_seconds
time_to_first_chunk_seconds
timing_source  # provider_callback | graph_fallback | runtime_cancel_fallback
```

绝对时间统一为 UTC，duration 使用 monotonic clock。首 chunk 只认非空公开文本、明确公开的 `reasoning_summary`/`rationale` 或非空 tool-call delta；空 sentinel、usage-only chunk 和 raw `reasoning_content` 不计入。provider 未产生公开语义 chunk 时两个 first-chunk 字段保持 `None`，Rich 显示 `unavailable`，不会伪造为零。正常路径使用 `provider_callback`；adapter 完全没有 model callback 时只由 graph terminal 生成一次 `graph_fallback`；callback 已开始但取消时没有 terminal callback，则以 `runtime_cancel_fallback` 闭合。后两者不会伪装成 provider 观测。

`tool_calls` 是普通 JSON 列表，每条记录至少有 `kind`、`name`、`tool_call_id`、`attempt_id`、`turn`、`arguments`、`status` 和 `requested_at`，以及成功时的 `result` 或失败/拒绝时的安全错误。真正进入 ToolNode 的 business action 还会有 `started_at`、`finished_at`、`queue_duration_seconds`、`duration_seconds`；结构化提交、allowlist 拒绝、预算拒绝或未能唯一对账的 orphan execution 不伪造执行时间，相关字段保持 `None`，并通过 `status`/`mapping` 说明事实。`requested_at` 是模型完整 tool request 到达时刻，queue 是 requested 到 ToolNode start，duration 是 ToolNode start 到 end/error/cancel；duration 同样使用 monotonic clock。同名并行工具优先以参数和官方 `ToolMessage.tool_call_id` 对账，不按名称或完成顺序猜测；上游没有暴露可确定关联时显式保留 `tool_call_id=null` 与 `mapping="orphan"`，不把同一 ID 写成两个终态。业务工具使用 `kind="business"`，结构化提交使用 `kind="structured"`。同一轮模型响应内出现多个已注册业务工具调用是合法的；同一轮出现未知工具，或业务工具与结构化终止同时出现，必须在任何工具执行前失败。`usage` 按 primary/compact transport 顺序保存，缺失值保持 `None`，不能把未知伪造成 0。

```python
result.require_output() -> T
result.to_dict() -> dict[str, JSONValue]
result.to_json() -> str
```

`require_output` 在失败、取消或没有 output 时抛出 `AgentError`。完整内容从 result 读取，不从终端抓取。没有 `audit_out` 或审计未能写出完整 `finish` 时，`academic_eligible=False`，结果不得进入正式学术统计；这不改变普通运行的 `status`，但调用者必须检查该字段。

真实 smoke 产物可在模型运行结束后离线校验，不需要重新调用 provider：

```bash
venv/bin/python tests/utils/validate_agent_smoke.py --root runs/utils-agent
```

校验器检查三 profile 的 result/audit/receipt 是否存在、SHA-256 与 commit id 是否一致、唯一 finish、两个业务工具、结构化字段、关键审计记录、无 credential 泄漏且没有残留 `.part` 文件。

### 脱敏选型

配置侧的 `api_key` 使用 Pydantic `SecretStr`，不会在公开摘要中展开。运行侧需要处理的是审计、console、export 的嵌套 JSON 边界：普通 URL 必须保留，`api_url`/`base_url`、Bearer/API key 和 secret-like 字段才精确替换。已核对的第三方方案中，`detect-secrets` 是仓库扫描器，`scrubadub`/Presidio 面向 PII 文本，`loggingredactor` 只作用于 logging record，LangChain `PIIMiddleware` 会改写 agent state/工具输入且 URL 规则过宽；它们都不能直接满足这个导出契约。因此这里保留无状态的递归策略，并用结构化/嵌套/普通 URL/endpoint/异常路径测试钉住边界，不引入不匹配的重依赖。

provider token 的静态识别只使用高置信格式：Anthropic `sk-ant-`、OpenAI project `sk-proj-`、Groq `gsk_`、Perplexity `pplx-`、Replicate `r8_` 使用当前 scanner/官方资料支持的形态；xAI、Together、Fireworks、Mistral 等没有稳定且官方公开的固定长度合同，默认只依赖当前运行的精确 `api_key` inventory，显式 `auth`/`token`/`api_key` 语境仍会进入上下文脱敏。不会用通用长字符串正则，否则会把 `gsk_baseline_v1_epoch_100`、`key-research-153` 等学术标识抹掉。流式 holdback 会保留紧邻的 credential context，确保 `api_key=`、`auth:` 等无空格分块也能在同一次解析中脱敏；长度不足的研究标识如 `sk-ant-baseline-1`、`sk-project-plan-2026` 保持原样。

`AgentError` 是运行期间唯一需要下游捕获的公开异常，至少提供安全的 `code` 和 `message`；`AgentRunResult.error` 使用相同的两个字段。稳定错误码包括 `config_error`、`provider_error`、`tool_error`、`tool_not_allowed`、`mixed_terminal_tool`、`context_budget_exceeded`、`compact_error`、`context_invalid`、`input_invalid`、`tool_required`、`structured_output_invalid`、`limit_exceeded`、`cancelled`、`audit_write_failed`、`json_export_failed`、`runtime_error` 和 `incomplete_tool`。错误消息不得包含 key、headers、完整 endpoint、prompt 或 traceback。脱敏会覆盖复合 secret 字段（如 `api_key_value`、`my_token`），同时保留 `token_usage`、`prompt_tokens` 和 `api_key_configured` 等统计/状态字段。
## 3. 最小真实 Agent 示例

```python
from pydantic import BaseModel
from langchain_core.tools import tool
from utils.agent import AgentApp, AgentSpec
from utils.llm import load_llm_registry

@tool
def lookup_note(note_id: str) -> dict[str, str]:
    """读取一个只读实验笔记。"""
    return {"note_id": note_id, "content": "示例内容"}

class Answer(BaseModel):
    summary: str
    evidence_id: str

spec = AgentSpec(
    name="note-reader",
    system_prompt="先调用 lookup_note，再根据工具结果回答。",
    tools=(lookup_note,),
    output_schema=Answer,
    require_tool_call=True,
)
app = AgentApp.from_registry(
    spec, load_llm_registry(), profile="gpt-5.5",
    model_options={"streaming": True},
)
result = app.run("请读取 note-001", renderer="rich")
answer = result.require_output()
print(answer.summary)
```

## 4. 实时输出和真实 demo

Agent 运行使用 `create_agent(...).astream_events(...)` 或当前依赖版本的等价异步事件流，不能先 `invoke/ainvoke` 再伪造进度。

启动 provider 请求前立即输出 `run_started`。每次 `arun()` 都用 run-scoped model copy 安装 callback，保留调用方已有 callback，不修改共享 model；该 callback 会穿过官方 `bind_tools()`。request capture 后、transport 前发出 `model_started`；首个公开 chunk 到达即刷新同一个 Rich Live；`on_llm_end` 到达即发出完整 message/tool request；工具 end/error 到达即显示结果。静默期间每秒发送 `heartbeat`（logging DEBUG），实际观察间隔不超过约 1.5 秒。LangGraph event stream 只负责 ToolNode、middleware、state 对账和明确 fallback，不重复输出 callback 已发布的 assistant/tool request。流式脱敏只在检测到已知凭据形态或运行配置中的精确 secret 时短暂保留候选 token，普通文本不会被固定延迟。`audit_out` 是另一条只面向学术分析的行为轨迹通道，`result_out` 保存最终结果。Rich 控制台会连续显示模型文本、工具调用参数、工具返回值、两行 CONTEXT、compact 生命周期和结束状态，不是运行结束后的摘要。

`audit_out` 是可选的 JSONL 文件，不新增审计包装类，也不复制工程事件。它只按 Agent 行为顺序写入四类普通 JSON 记录：`context`、`decision`、`action`、`finish`；compact 作为 `context.operation="compact"`。每条记录都带 `run_id`、`seq/order`、`recorded_at`，工具记录另外带 `tool_call_id`，模型决策带 `model_call_id`。`input_message_refs`/`replacement_refs` 中每条 message ref 都带 `source_seq` 与 `source_record`（初始输入回链 `context`，工具结果回链对应 `action`），从而能重建每轮输入、输出、工具结果、context decision、compact replacement 和最终结束。

1. `context`：任务输入、system prompt、Agent 名称、可用工具名称/描述/schema、输出 schema、模型标识，以及每个 attempt 实际交给模型的页面顺序、`id`、`hash` 和文本，说明 Agent 当时能做什么、看到了什么。
2. `decision`：每一轮模型可见的输出、请求调用的工具及参数、结构化提交、canonical `model_call_id`、usage/timing，以及 provider 明确返回的 `reasoning_summary`/`rationale`（没有就写 `null`）。
3. `action`：每次工具尝试的目标、参数、requested/start/terminal 时点、queue/execution duration、是否被 allowlist 接受、实际返回值或错误；未知工具、拒绝执行和重复调用也必须记录。
4. `finish`：最终文本/结构化结果、逐 model call 的 usage/timing、run duration、结束原因（成功时为 `final_answer` 或 `structured_output`；失败/取消时为对应的 `error.code`，例如 `provider_error`、`limit_exceeded` 或 `cancelled`）和最终状态。

审计记录只保留回答“Agent 试图做什么、实际做了什么、看到了什么、得到了什么、context 如何 compact、最后如何结束”所需的数据。heartbeat、Rich 刷新、HTTP endpoint、headers、内部 graph state、observer 错误、traceback 和 hidden chain-of-thought 不进入 `audit_out`；usage 只因为它决定 compact 才记录。每条记录写入后 flush，成功和失败都必须有 `finish`。启用 `audit_out` 时最终发布 `<audit_out>.receipt.json`，receipt 保存 audit/result hash、`trace_commit_id` 和 finish 序号；只有 receipt 与两个文件 hash 一致时 `academic_eligible=True`。

### 4.1 Compact 与学术审计的完整闭环

compact 只由 LangGraph 官方 `SummarizationMiddleware` 执行，运行时不手写第二套上下文压缩、工具重放或 JSON 摘要解析。装配关系固定为：

1. `threshold = floor(context_window_tokens * compact_trigger_ratio)`，其中 `context_window_tokens` 来自配置或官方模型 profile；`max_output_tokens` 单独记录，不从输入窗口中扣减。两者都未知时不猜容量，compact 状态为 `unavailable`。
2. `SummarizationMiddleware(trigger=("tokens", threshold), keep=("messages", 20))` 观察 LangGraph state；达到阈值时在官方 token counter 内预留唯一 `compaction_id`，再由同一模型、同一推理设置生成 summary，并由 middleware 用官方 `RemoveMessage` replacement 写回 state。summary callback、外层 middleware replacement、usage/timing 和 audit 都显式关联该 ID，不使用可变的“最近一次 compact”作为事实真源。
3. compact 不重新执行已经完成的业务工具，不复制旧 tool result，不改变调用方原始 prompt；summary transport 是一次普通模型调用，计入显式 `model_calls`，但不计业务 tool/turn。
4. 实时顺序必须是 `CONTEXT` -> `COMPACTION | START` -> 可见 summary 流 -> `COMPACTION | COMPLETE` -> 下一轮 `MODEL INPUT`；失败则输出 `COMPACTION | FAILED`，并在最终 `AGENT FAILED` 与 audit `finish` 中说明归属和诊断。

显式 `limits.model_calls` 使用同一 run-scoped ledger；普通 turn 不需要 compact 时预留 1 次，需要 compact 时在 summary transport 前原子预留 `summary + next primary` 两次，预算不足不会启动任何一条 transport。ledger 的 reserved/started/completed/cancelled 和 compact 次数会进入 result/finish，默认无限策略不增加隐藏上限。

学术审计只记录 Agent 行为事实：`context` 说明输入、可用能力和实际 context；`decision` 说明模型可见输出、工具/结构化请求和 provider 提供的 rationale/summary；`action` 说明尝试访问的工具、参数、结果或拒绝/异常；`finish` 说明如何结束。compact 的开始、summary hash、replacement 和结束状态仍作为 `context.operation="compact"` 写入，便于重建“为什么压缩、压缩了什么、压缩后继续看到了什么”。不写 heartbeat、Rich 刷新、请求 headers、内部 graph state 或隐藏 chain-of-thought。

审计文件采用 `.part` + 独占 lock + flush/fsync + 原子 rename；完成后生成 receipt，保存 audit/result SHA-256、`trace_commit_id` 和 finish 序号。只有 `audit_out` 存在、最终状态成功、finish 完整且 receipt hash 校验通过时，`academic_eligible=True`；否则结果仍可供调试读取，但不能进入正式学术统计。

```bash
python -m utils.agent
python -m utils.agent.demo --profile gpt-5.5 --renderer rich --log-level INFO \
  --audit-out /tmp/agent-audit.jsonl \
  --result-out /tmp/agent-result.json </dev/null
python -m utils.agent.demo --profile gpt-5.5 --renderer rich --log-level DEBUG </dev/null
python -m utils.agent.demo --profile gpt-5.5 --max-model-calls 20 --max-tool-calls 50 \
  --max-turns 30 --max-seconds 900 --compact-trigger-ratio 0.85 </dev/null
```

不传 `--audit-out/--result-out` 时 demo 默认写入 `runs/utils-agent/demo-audit.jsonl` 和 `runs/utils-agent/demo-result.json`；这些文件只包含脱敏内容。`python -m utils.agent` 与 `python -m utils.agent.demo` 使用同一真实 demo 入口。

demo 的 `--max-model-calls`、`--max-tool-calls`、`--max-turns`、`--max-seconds` 都是可选限制；不传任何一个时不设置业务资源预算。LangGraph 内部的递归保护会自动提高到足够大的值，不会把默认的 25 次图步骤误当成 Agent 的最大迭代次数；只有显式的 limits 才会返回 `limit_exceeded`。

demo 使用两个无副作用工具：无参数 `current_system_time` 和安全的 `calculate_expression`，计算当前系统时间起 51.25 小时后的美国东部时间节点，完成结构化输出并校验两个 evidence ID；system prompt 只放通用工具/输出协议，具体任务只放在唯一的 user prompt：`请计算当前系统时间 (2 * 24) + 3 + (15 / 60) 小时后的美国东部时间。`；默认使用真实 `gpt-5.5`，也可通过 `--profile` 运行其他已配置的真实模型，没有 fake、offline、deterministic、replay 或人工输入。

## 5. CLI、测试和边界

```bash
python -m utils.llm init --from-env --profile NAME --context-window-tokens N --max-output-tokens N [--config PATH]
python -m utils.llm validate [--config PATH] [--require-credentials]
python -m utils.llm list [--config PATH] [--format table|json]
python -m utils.llm show NAME [--config PATH] [--format table|json]
```

CLI 不访问 provider 网络，错误写 stderr，成功数据写 stdout，`show` 永远脱敏。

默认测试不能访问真实 API。使用临时 YAML、测试专用 `BaseChatModel`、事件 fixture 和 fake clock；测试桩只放 `tests/`，不从 `utils` 导出。真实测试必须显式启用，失败不能降级成固定答案。

实现 PR 必须提供 `tests/utils/test_public_api_docs.py`，检查 README 的公共导入、最小示例、命令、事件名和结果字段与实现一致。需要 standalone chat/stream、公共 Fake、checkpoint、multi-agent 或 paper1 adapter 时另开 Issue。

## 6. 简单维护规则

允许增加必要的可选参数和事件，但不要引入新的包装实体、枚举层或版本系统，不要重定义现有语义，不要把业务工具和结构化输出混计，不要把 secret 放入公开对象。修改 API 时同步修改 Issue #155、本文档和测试。

评审时必须先查阅当前 LangGraph/LangChain/provider 官方文档：已有官方能力时直接调用官方 API，禁止手写等价 agent loop、schema parser、tool dispatcher 或 provider 专用后处理。新增兼容分支必须有官方依据、最小回归测试和真实 smoke 证据；没有依据的“看起来能用”实现不进入基础设施。
