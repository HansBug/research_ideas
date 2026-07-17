# Paper1 Discover Agent

本目录实现 paper1 的第一个完整阶段：在 A 阶段已经准备好的
`NL + raw/source STM_0 + fcstm STM_0` 上运行一次 `B-discover`，发布不可变的
检查集、root issue batch、方法记录与人类可读报告。Discover 只读，不修改模型，
也不执行 Repair、Confirm 或 C 阶段源层闭合判断。

## 运行模型

一次真实 `B-discover` 只创建并运行一个 `AgentApp`。Controller 在启动前只完成
FCSTM parse/semantic/inspect、能力清单、输入与上下文冻结；不再启动 NL producer、
source producer 或其他 Agent。唯一的 Discover Agent 在同一次 run 内完成：

1. 首先读取 `pyfcstm.llm` 提供且经完整性校验的 FCSTM guide。
2. 再读取 `NL + raw/source STM_0 + fcstm STM_0` 和冻结 inspect/source trace。
3. 形成一批完整的 typed check drafts，并明确每项预期结果与依据；若包含 property，
   必须先读取 `pyfcstm.llm` 提供的 FBMCQ guide。
4. 调用 `evaluate_checks`，由确定性代码完成 binding、scenario、bounded property、
   static consistency 和 mechanical eligibility。
5. 仅针对明确证据缺口调用结构、轨迹或 source-trace 查询工具。
6. 对完整 check batch 给出 `confirmed / candidate_only / rejected` 理由。
7. 一次性提交与某次 eligible `evaluate_checks` 调用完全一致的 drafts、roots 和
   rejected propositions。

Agent 获得七个 bounded 工具：

| 工具 | 用途 | 调用条件 |
|---|---|---|
| `read_fcstm_guide` | 读取 `pyfcstm.llm` 中完整、带版本与 SHA-256 的 FCSTM guide | 必用，且必须是首次业务工具调用 |
| `read_fbmcq_guide` | 读取 `pyfcstm.llm` 中完整、带版本与 SHA-256 的 FBMCQ guide | 首次构造、修订或提交 property 前必用 |
| `read_task` | 读取或重读同一 attempt 的六字段冻结上下文 | FCSTM guide 后必用；Compact 后或需复核时可重读 |
| `query_model` | 查询分页结构化 inspect 事实 | 存在明确的结构证据缺口时 |
| `observe_trace` | 探索一条有限事件轨迹 | 存在明确的轨迹问题时 |
| `lookup_source_trace` | 查询 source 与 fcstm 元素映射 | 引用边界不清楚时 |
| `evaluate_checks` | 绑定并执行完整 check draft batch | 最终 batch 必须调用且通过机械 gate |

初始 provider input 不包含 FCSTM 正文，只包含 run/model 身份和 hash。Controller 通过
内容隔离、工具前置条件和 run 后顺序复核三层机制强制执行
`read_fcstm_guide -> read_task -> model work`；property batch 另强制
`read_fbmcq_guide -> property work`。任何先违规后补读的 attempt 仍会 fail-closed。

`evaluate_checks` 内部固定调用 `run_scenarios`、`verify_properties`、
`verify_static_consistency` 和 `validate_discovery_checks`，但不调用 LLM、不修改模型、
不产生 issue verdict。Controller 在 Agent 结束后要求最终 `check_drafts` 与本 attempt
中某次 eligible 调用的完整输入一致，然后才发布 method records。每个 Agent 工具的
注册后 docstring 都定义 Purpose、Parameters、Returns、Execution、Failure semantics、
Evidence limitations、Permissions 与 Example，并由合同测试直接检查。

`confirmed` root 还必须通过独立的确定性归因门：每个引用都要在冻结的元素级 source
trace 中形成严格一对一映射。仅在 inspect 中存在、仅被 check binder 使用，或只有
ambiguous/untraceable mapping，都不能进入 Repair，只能降为 `candidate_only` 或
`rejected`。唯一不需要逐元素 trace entry 的情况是 raw/source 与 fcstm 文本确实相同的
custom identity input。

## 真实 Demo

Demo 只提供真实 provider 模式，不存在伪装成成功运行的离线 demo。先在当前 shell
加载本地配置：

```bash
source .env
make discover-demo
```

默认参数：

```text
pair       llms_emp_stm_results_0000
profile    gpt-5.5
language   zh-CN
renderer   rich
outdir     runs/paper1/discover/demo
```

`rich` renderer 会直接显示与 `utils.agent.demo` 同类的流式模型、工具调用和完成事件，
不会隐藏主 Agent 交互。输出目录必须为空；再次运行应指定新目录：

```bash
make discover-demo \
  DISCOVER_OUT=runs/paper1/discover/demo-0001 \
  DISCOVER_PROFILE=gpt-5.5 \
  DISCOVER_LANGUAGE=zh-CN
```

直接使用模块入口：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python -m paper_stm_repair_loop.discover \
  --pair-id llms_emp_stm_results_0000 \
  --profile gpt-5.5 \
  --content-language zh-CN \
  --renderer rich \
  --output-dir runs/paper1/discover/manual-0000
```

Agent 默认不设置 model call、tool call、turn 或 wall-clock 上限，避免真实 Discover
因为隐藏的固定预算被截断。需要做受限 smoke、故障注入或成本控制时，可通过 CLI
显式传入任意一项或多项正数限制：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python -m paper_stm_repair_loop.discover \
  --pair-id llms_emp_stm_results_0000 \
  --profile gpt-5.5 \
  --content-language zh-CN \
  --renderer rich \
  --max-model-calls 24 \
  --max-tool-calls 80 \
  --max-turns 40 \
  --max-seconds 1800 \
  --output-dir runs/paper1/discover/limited-0000
```

四个选项彼此独立；未传入的维度保持无限制。显式值必须是正数，
其中秒数还必须是有限数（拒绝 `NaN` 与正负无穷）。通过校验的值会写入
`manifest.json.agent_limits`，便于复现实验预算。Make 入口可通过
`DISCOVER_ARGS="--max-model-calls 24 --max-seconds 1800"` 透传相同选项。

## 自定义输入

只有 `NL + fcstm` 时使用 identity source mode：

```bash
make discover-custom \
  DISCOVER_CASE=custom-case \
  DISCOVER_NL=/path/to/nl.txt \
  DISCOVER_FCSTM=/path/to/model.fcstm \
  DISCOVER_OUT=runs/paper1/discover/custom-case
```

如果 raw/source STM 与 fcstm 不同，必须同时提供 source trace，不能猜测映射：

```bash
make discover-custom \
  DISCOVER_CASE=custom-source-case \
  DISCOVER_NL=/path/to/nl.txt \
  DISCOVER_FCSTM=/path/to/model.fcstm \
  DISCOVER_RAW_SOURCE=/path/to/raw-model.puml \
  DISCOVER_SOURCE_TRACE=/path/to/source-trace.json \
  DISCOVER_OUT=runs/paper1/discover/custom-source-case
```

## 输出与审计边界

所有输入、上下文、LLM audit 和方法记录都写在同一个不可覆盖目录：

```text
outdir/
├── manifest.json
├── capability_manifest.json
├── inputs/
│   ├── nl.txt
│   ├── raw_stm_0.txt
│   ├── STM_0.fcstm
│   └── source_trace_base.json
├── agent_audit/
│   └── discover/
│       ├── audit.jsonl
│       ├── result.json
│       ├── receipt.json
│       └── redaction_report.json
├── contexts/discover-attempt-001/
│   ├── prompt.md
│   ├── context.json
│   ├── context.md
│   └── context_manifest.json
├── records/
│   └── L000-<sequence>-<record-type>/record.json
└── loops/discover.md
```

`records/` 是唯一机器事实源；每笔记录按全局 sequence 和 hash chain 追加，写后不改。
`loops/discover.md` 由确定性 renderer 一次生成，包含 NL、raw/source STM、fcstm
STM_0、检查集、root issues 和指向原始记录/audit 的链接。

成功运行还会追加 `guide_access_completed`，记录 FCSTM/FBMCQ guide 的读取顺序、
版本和 SHA-256。`capability_manifest.json` 同时记录 `pyfcstm` source/distribution
版本、submodule commit 和两份 prompt resource metadata；版本不一致时运行失败，
不得进入正式结果。

Replay 文件只通过隐藏的测试参数用于确定性合同测试，产物会明确写
`real_llm=false`、`academic_eligible=false`，不能作为真实 demo 或论文实验结果。

## 验证

```bash
make discover-test
```

测试覆盖 system prompt 六步协议、单次 `AgentApp.run`、七工具 allowlist、guide-first
门禁与顺序审计、默认无限制与 CLI 显式限制、详细 docstring、严格输入 schema、
BMC/replay 义务、append-only records、zero-root 发布、reference/gold 防泄漏、
自定义输入和确定性报告。
