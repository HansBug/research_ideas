# `utils`：LLM 与 Agent 基础设施

本文档是根级 `utils` 的中文公共 API 指南。实现以 [Issue #155](https://github.com/HansBug/research_ideas/issues/155) 为设计稿；Issue、本文档和测试必须保持同步。

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
from utils.llm import LLMConfig, LLMRegistry, load_llm_registry
```

```python
class LLMConfig(BaseModel):
    base_url: str | None = None
    api_key: SecretStr | None = None
    model: str
    context_window_tokens: int | None = None
    max_output_tokens: int | None = None
```

只有 `model` 必填。其他字段为 `None` 时，Agent 构造模型时不传对应参数。`LLMRegistry` 是只读 `Mapping[str, LLMConfig]`：

```python
registry = load_llm_registry()
config = registry["gpt-5.5"]
config = registry.default
registry.default_name
registry.names()
```

路径优先级为显式参数、`LLM_CONFIG_FILE`、根 `.llmconfig.yml`。加载器不访问网络、不创建 client、不维护全局可变单例。公开摘要必须脱敏；`api_key` 不能打印。
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

限制计数是整个 `run` 的累计值，跨 context rollover attempt 不重置；rollover 只重放已完成动作，不重新获得新的预算。`context_window_tokens` 与 `max_output_tokens` 都是可选配置；两者同时提供时运行时才做本地窗口预检，缺省时把窗口/输出预算交给 provider，不在本地擅自猜测数值。

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
    model_call_options: Mapping[str, Any] | None = None,
) -> AgentRunResult

await app.arun(input_text, context=context, renderer="auto", think_mode=False, ...) -> AgentRunResult
```

`renderer` 使用 `auto`、`rich`、`jsonl` 或 `quiet`；`log_level` 使用标准 logging 的 `DEBUG`、`INFO`、`WARNING`、`ERROR`。`INFO` 显示 Agent 阶段、模型可见输出、工具参数/结果和最终结果；heartbeat 只在 `DEBUG` 显示。`auto` 会按终端环境选择适合的人类可读输出；`arun` 是已有 event loop 时的入口；`run` 只用于普通同步脚本。`model_call_options` 只作用于当前推理，不能携带 secret 或覆盖 profile 身份。

`think_mode` 默认关闭，所有模型都必须显式传入 `True` 才会开启 provider 的 thinking/reasoning 模式；`reasoning_effort` 只有在 `think_mode=True` 时才可传入。CLI 对应 `--enable-think` 和 `--reasoning-effort`。模型请求默认 `streaming=True`，也可以在 `model_options` 中显式传入 `{"streaming": False}` 覆盖；YAML 不保存这些单次运行参数。

Rich 输出按 LLM I/O 顺序组织：`MODEL INPUT` 是本轮交给模型的 system/user/tool messages；`MODEL OUTPUT` 是模型返回的 assistant 文本、tool call 或结构化结果；工具执行结果标为 `TOOL RESULT -> NEXT MODEL INPUT`，并在下一轮 input 面板中作为 `[tool]` message 出现。已展示的 assistant history 不重复打印，完成面板保留一次完整最终结果。

结构化结果直接通过 `create_agent(response_format=YourSchema)` 交给 LangGraph；由 LangGraph AutoStrategy 按模型能力选择 provider-native structured output 或官方 tool-calling fallback。运行时不把普通 assistant 文本自行 `json.loads` 成结果，也不为某个 provider 另写一套结构化后处理；provider 不支持或返回无效结构时保留原始失败诊断。

官方 tool-calling fallback 的 schema 校验重试由 LangGraph 自己管理；默认不额外加隐藏重试上限，以保持“未配置预算就不限制”的契约。需要为不兼容 provider 设置止损时，显式传 `limits`（例如 `model_calls` 或 `seconds`），失败结果会保留 `structured_output_invalid`/provider 诊断和 audit `finish`。

终端按消息顺序显示：第一次模型请求显示一次 system/user 消息，后续请求只显示新增的 tool 消息；已经显示的历史不会每轮重复打印。assistant 输出、tool 参数和 tool 返回紧随对应消息出现。超长可见内容保留头尾，中间只做明确的长度标记；`audit_out` 仍保存完整的可审计内容。每个 tool Panel 都明确标出 `name`、`tool_call_id`、`status`、`arguments`，结果 Panel 还标出 `result`；工具异常会标出安全的 `error`，DEBUG 时补充异常类型和 provider request id 等诊断字段。

运行时不会改写、追加或重排调用方提供的 `system_prompt` 和任务输入。若实验需要可见的计算步骤、依据、工具结果或总结，直接把要求写进调用方自己的 prompt 或输出 schema；框架只展示模型实际返回的内容，不生成或猜测隐藏思维链。`model_started.data.prompt` 和 Rich 的 MODEL INPUT 面板会展示经过脱敏的可见输入，这是实时观察契约的一部分；学术审计同样只保存脱敏后的上下文事实。

`context` 是本次运行的有序上下文页面，不需要额外的上下文类：

```python
context = [
    {"id": "record-001", "hash": "sha256:...", "text": "不可变事实一"},
    {"id": "record-002", "hash": "sha256:...", "text": "不可变事实二"},
]
result = app.run("分析这些事实", context=context, renderer="rich")
```

也可以直接传字符串，运行时会按顺序编号。mapping 至少包含 `text`，推荐同时提供 `id`、`hash`、`snapshot`、`cursor`、`source`；hash 必须等于规范化 text 的 SHA-256，重复 id、hash 不匹配或同一运行内 snapshot 漂移直接失败。运行时根据 `LLMConfig.context_window_tokens` 与 `max_output_tokens` 装配当前请求；接近窗口时从同一组页面开启新的 attempt，并重放原始输入、已完成的结构化工具/动作记录和精确页面，不做静默截断、自动摘要或 provider compact。没有足够 token 配置、单页本身超限或无法无损继续时返回 `status="failed"`、`error.code="context_budget_exceeded"`。paper1 只需把自己的 immutable record pager 转成上述页面，不需要让根级 `utils` 认识 issue、DSL 或 trace。

上下文装配会产生 `context_loaded`、`context_rollover`、`context_failed` 观察事件；这些事件可以显示在 Rich 中，但学术 `audit_out` 只记录实际交给模型的页面及其顺序/hash，不记录上下文管理器的内部调试状态。rollover 只注入已经完成的结构化 action 记录，不重新执行工具；存在未决工具副作用时直接失败。若实验需要分析决策依据，可在 system prompt 或输出 schema 中要求简短、可见的 rationale；审计只保存模型实际给出的这类摘要，不声称拥有隐藏思维链。

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
    usage: dict | None,
    error: dict | None,
    real_llm: bool,
    model: str,
    observed_model: str | None,
    academic_eligible: bool,
    context_manifest_hash: str | None,
)
```

`status` 只有 `success`、`failed`、`cancelled`；上下文无法无损继续时使用 `status="failed"` 和 `error.code="context_budget_exceeded"`。`real_llm` 在公共真实运行中为 `True`，仅测试目录的内部桩可以为 `False`，测试结果不得作为真实实验制品。

事件 `kind` 使用简单字符串：`run_started`、`heartbeat`、`context_loaded`、`context_rollover`、`context_failed`、`model_started`、`model_text`、`model_completed`、`tool_started`、`tool_completed`、`tool_failed`、`structured_output`、`completed`、`failed`。`seq` 从 1 递增，普通观察事件的 data 不得包含 key、headers、raw response 或 hidden reasoning。

`tool_calls` 是普通 JSON 列表，每条记录至少有 `kind`、`name`、`tool_call_id`、`attempt_id`、`turn`、`arguments`、`status`、开始/结束时间，以及成功时的 `result` 或失败时的安全错误；业务工具使用 `kind="business"`，结构化提交使用 `kind="structured"`。工具的完整 description/schema 仍保存在 `context` 审计记录中，但不在实时 tool Panel 重复输出。rollover 重放的记录标记 `replayed=true`；物理执行统计应过滤该标记，重放事实保存在 rollover 的 `context.replayed_actions` 中，不重复写入新的 `action`。同一轮模型响应内出现多个已注册业务工具调用是合法的；同一轮出现未知工具，或业务工具与结构化终止同时出现，必须在任何工具执行前失败。流式参数由 LangGraph/LangChain 先完整重组并校验。`usage` 未知时为 `None` 或字段值为 `None`，不能把未知伪造成 0。`error` 至少包含 `code` 和 `message`，`status` 只允许 `success`、`failed`、`cancelled`。

```python
result.require_output() -> T
result.to_dict() -> dict[str, JSONValue]
result.to_json() -> str
```

`require_output` 在失败、取消或没有 output 时抛出 `AgentError`。完整内容从 result 读取，不从终端抓取。没有 `audit_out` 或审计未能写出完整 `finish` 时，`academic_eligible=False`，结果不得进入正式学术统计；这不改变普通运行的 `status`，但调用者必须检查该字段。

### 脱敏选型

配置侧的 `api_key` 使用 Pydantic `SecretStr`，不会在公开摘要中展开。运行侧需要处理的是审计、console、export 的嵌套 JSON 边界：普通 URL 必须保留，`api_url`/`base_url`、Bearer/API key 和 secret-like 字段才精确替换。已核对的第三方方案中，`detect-secrets` 是仓库扫描器，`scrubadub`/Presidio 面向 PII 文本，`loggingredactor` 只作用于 logging record，LangChain `PIIMiddleware` 会改写 agent state/工具输入且 URL 规则过宽；它们都不能直接满足这个导出契约。因此这里保留无状态的递归策略，并用结构化/嵌套/普通 URL/endpoint/异常路径测试钉住边界，不引入不匹配的重依赖。

`AgentError` 是运行期间唯一需要下游捕获的公开异常，至少提供安全的 `code` 和 `message`；`AgentRunResult.error` 使用相同的两个字段。稳定错误码包括 `config_error`、`tool_error`、`tool_not_allowed`、`mixed_terminal_tool`、`context_budget_exceeded`、`limit_exceeded`、`audit_write_failed` 和 `json_export_failed`。错误消息不得包含 key、headers、完整 endpoint、prompt 或 traceback。
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
    model_options={"streaming": True, "stream_usage": True},
)
result = app.run("请读取 note-001", renderer="rich")
answer = result.require_output()
print(answer.summary)
```

## 4. 实时输出和真实 demo

Agent 运行使用 `create_agent(...).astream_events(...)` 或当前依赖版本的等价异步事件流，不能先 `invoke/ainvoke` 再伪造进度。

启动 provider 请求前立即输出 `run_started`；静默期间每秒发送 `heartbeat`（logging DEBUG），实际观察间隔不超过约 1.5 秒。Rich 和 callback 消费实时 `AgentEvent`，用于操作员观察；`audit_out` 是另一条只面向学术分析的行为轨迹通道，`result_out` 保存最终结果。Rich 控制台会连续显示模型文本、工具调用参数、工具返回值、上下文 rollover、结构化结果和结束状态，不是运行结束后的摘要。

`audit_out` 是可选的 JSONL 文件，不新增审计包装类，也不复制工程事件。它只按行为顺序写入四类普通 JSON 记录；每条记录都带 `run_id`、`attempt_id`、`turn`、`order`、`context_manifest_hash`，工具记录另外带 `tool_call_id`，从而能把决策、页面和动作在 rollover 后重新绑定：

1. `context`：任务输入、system prompt、Agent 名称、可用工具名称/描述/schema、输出 schema、模型标识，以及每个 attempt 实际交给模型的页面顺序、`id`、`hash` 和文本，说明 Agent 当时能做什么、看到了什么。
2. `decision`：每一轮模型可见的输出、请求调用的工具及参数、结构化提交，以及 provider 明确返回的 `reasoning_summary`/`rationale`（没有就写 `null`）。
3. `action`：每次工具尝试的目标、参数、是否被 allowlist 接受、实际返回值或错误；未知工具、拒绝执行和重复调用也必须记录。
4. `finish`：最终文本/结构化结果、结束原因（如 `final_answer`、`structured_output`、`error`、`cancelled`、`limit`）和成功/失败状态。

审计记录只保留回答“Agent 试图做什么、实际做了什么、看到了什么、得到了什么、依据什么继续、最后如何结束”所需的数据。heartbeat、Rich 刷新、callback、HTTP endpoint、重试、timeout、缓存、内部 graph state、observer 错误和 token 统计等纯工程信息不得进入 `audit_out`。隐藏 chain-of-thought 不作为可导出事实；只记录模型明确给出的可见 rationale/summary，不生成或猜测缺失内容。脱敏只递归处理嵌套 mapping/list 中的 secret-like key 和 API key 模式；不改写普通任务输入、可见模型文本、工具参数或工具结果。每条学术记录写入后 flush，成功和失败都必须有 `finish`；`result_out` 使用临时文件加 `os.replace` 原子写出，写盘失败返回 `audit_write_failed` 或 `json_export_failed`，不得伪造审计内容。

```bash
python -m utils.agent
python -m utils.agent.demo --profile gpt-5.5 --renderer rich --log-level INFO \
  --audit-out /tmp/agent-audit.jsonl \
  --result-out /tmp/agent-result.json </dev/null
python -m utils.agent.demo --profile gpt-5.5 --renderer rich --log-level DEBUG </dev/null
python -m utils.agent.demo --profile gpt-5.5 --max-model-calls 20 --max-tool-calls 50 \
  --max-turns 30 --max-seconds 900 </dev/null
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
