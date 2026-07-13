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

限制键只有 `model_calls`、`tool_calls`、`turns`、`seconds`。未设置限制时不因为调用次数、轮数或时间主动失败。`tools` 同时是 allowlist：未知工具、多于一个工具请求、业务工具与结构化终止混合时，在执行前直接失败；工具异常和结构化输出校验失败也按运行错误处理。这些是行为边界，不是复杂预算策略。

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

`from_registry` 是下游实验首选入口；省略 `profile` 使用默认 profile。`model_options` 只在构造 `ChatOpenAI` 时使用，例如 `streaming=True`、`stream_usage=True`、`timeout=600`、`max_retries=0`，不写入 YAML。

```python
app.run(
    input_text: str,
    *,
    context: Sequence[str | Mapping[str, Any]] | None = None,
    renderer: str = "auto",
    on_event: Callable[[AgentEvent], None] | None = None,
    audit_out: Path | None = None,
    result_out: Path | None = None,
    model_call_options: Mapping[str, Any] | None = None,
) -> AgentRunResult

await app.arun(input_text, same_options) -> AgentRunResult
```

`renderer` 使用 `auto`、`rich`、`jsonl` 或 `quiet`。`auto` 会按终端环境选择适合的人类可读输出；`arun` 是已有 event loop 时的入口；`run` 只用于普通同步脚本。`model_call_options` 只作用于当前推理，不能携带 secret 或覆盖 profile 身份。

`context` 是本次运行的有序上下文页面，不需要额外的上下文类：

```python
context = [
    {"id": "record-001", "hash": "sha256:...", "text": "不可变事实一"},
    {"id": "record-002", "hash": "sha256:...", "text": "不可变事实二"},
]
result = app.run("分析这些事实", context=context, renderer="rich")
```

也可以直接传字符串，运行时会按顺序编号。页面边界、顺序、`id` 和 `hash`（若提供）会被保留。运行时根据 `LLMConfig.context_window_tokens` 与 `max_output_tokens` 装配当前请求；接近窗口时从同一组页面开启新的 attempt，并重放原始输入、已完成的结构化工具/动作记录和精确页面，不做静默截断、自动摘要或 provider compact。没有足够 token 配置、单页本身超限或无法无损继续时返回 `context_budget_exceeded`。paper1 只需把自己的 immutable record pager 转成上述页面，不需要让根级 `utils` 认识 issue、DSL 或 trace。

上下文装配会产生 `context_loaded`、`context_rollover`、`context_failed` 观察事件；这些事件可以显示在 Rich 中，但学术 `audit_out` 只记录实际交给模型的页面及其顺序/hash，不记录上下文管理器的内部调试状态。若实验需要分析决策依据，可在 system prompt 或输出 schema 中要求简短、可见的 rationale；审计只保存模型实际给出的这类摘要，不声称拥有隐藏思维链。

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
)
```

事件 `kind` 使用简单字符串：`run_started`、`heartbeat`、`model_started`、`model_text`、`model_completed`、`tool_started`、`tool_completed`、`tool_failed`、`structured_output`、`completed`、`failed`。`seq` 从 1 递增，普通观察事件的 data 不得包含 key、headers、raw response 或 hidden reasoning。

`tool_calls` 是普通 JSON 列表，每条记录至少有 `kind`、`name`、`arguments`、`status`、开始/结束时间，以及成功时的 `result` 或失败时的安全错误；业务工具使用 `kind="business"`，结构化提交使用 `kind="structured"`。不再定义额外的 record 类型。`usage` 未知时为 `None` 或字段值为 `None`，不能把未知伪造成 0。`error` 至少包含 `code` 和 `message`。

```python
result.require_output() -> T
result.to_dict() -> dict[str, JSONValue]
result.to_json() -> str
```

`require_output` 在失败、取消或没有 output 时抛出 `AgentError`。完整内容从 result 读取，不从终端抓取。

`AgentError` 是运行期间唯一需要下游捕获的公开异常，至少提供安全的 `code` 和 `message`；`AgentRunResult.error` 使用相同的两个字段。错误消息不得包含 key、headers、完整 endpoint、prompt 或 traceback。
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

启动 provider 请求前立即输出 `run_started`；静默期间每秒输出 `heartbeat`，实际观察间隔不超过约 1.5 秒。Rich 和 callback 消费实时 `AgentEvent`，用于操作员观察；`audit_out` 是另一条只面向学术分析的行为轨迹通道，`result_out` 保存最终结果。

`audit_out` 是可选的 JSONL 文件，不新增审计包装类，也不复制工程事件。它只按行为顺序写入四类普通 JSON 记录：

1. `context`：任务输入、system prompt、Agent 名称、可用工具名称/描述/schema、输出 schema、模型标识，以及每个 attempt 实际交给模型的页面顺序、`id`、`hash` 和文本，说明 Agent 当时能做什么、看到了什么。
2. `decision`：每一轮模型可见的输出、请求调用的工具及参数、结构化提交，以及 provider 明确返回的 `reasoning_summary`/`rationale`（没有就写 `null`）。
3. `action`：每次工具尝试的目标、参数、是否被 allowlist 接受、实际返回值或错误；未知工具、拒绝执行和重复调用也必须记录。
4. `finish`：最终文本/结构化结果、结束原因（如 `final_answer`、`structured_output`、`error`、`cancelled`、`limit`）和成功/失败状态。

审计记录只保留回答“Agent 试图做什么、实际做了什么、看到了什么、得到了什么、依据什么继续、最后如何结束”所需的数据。heartbeat、Rich 刷新、callback、HTTP endpoint、重试、timeout、缓存、内部 graph state、observer 错误和 token 统计等纯工程信息不得进入 `audit_out`。隐藏 chain-of-thought 不作为可导出事实；只记录模型明确给出的可见 rationale/summary，不生成或猜测缺失内容。key、authorization、headers 和明确标记为 secret 的字段统一脱敏；其余任务输入、可见模型文本、工具参数和工具结果不截断。每条学术记录写入后 flush，成功和失败都必须有 `finish`；文件写入失败只影响运行状态，不得伪造审计内容。

```bash
python -m utils.agent.demo --config .llmconfig.yml --profile gpt-5.5 --renderer rich
python -m utils.agent.demo --profile gpt-5.5 --renderer rich \
  --audit-out /tmp/agent-audit.jsonl \
  --result-out /tmp/agent-result.json </dev/null
```

demo 必须调用无参数 `read_demo_context` 业务工具一次，完成一次结构化输出，校验 evidence ID，并且永远使用真实 `gpt-5.5`。没有 fake、offline、deterministic、replay 或人工输入。

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
