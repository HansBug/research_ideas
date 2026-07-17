# Paper1 Discover Agent

本目录实现 paper1 的第一个完整阶段：在 A 阶段已经准备好的
`NL + raw/source STM_0 + fcstm STM_0` 上运行一次 `B-discover`，发布不可变的
检查集、root issue batch、方法记录与人类可读报告。Discover 只读，不修改模型，
也不执行 Repair、Confirm 或 C 阶段源层闭合判断。

## 运行模型

一次真实 `B-discover` 只创建并运行一个 `AgentApp`。Controller 在启动前只完成
FCSTM parse/semantic/inspect、能力清单、输入与上下文冻结；不再启动 NL producer、
source producer 或其他 Agent。唯一的 Discover Agent 在同一次 run 内完成：

1. 读取 `NL + raw/source STM_0 + fcstm STM_0` 和冻结 inspect/source trace。
2. 形成一批完整的 typed check drafts，并明确每项预期结果与依据。
3. 调用 `evaluate_checks`，由确定性代码完成 binding、scenario、bounded property、
   static consistency 和 mechanical eligibility。
4. 仅针对明确证据缺口调用结构、轨迹或 source-trace 查询工具。
5. 对完整 check batch 给出 `confirmed / candidate_only / rejected` 理由。
6. 一次性提交与某次 eligible `evaluate_checks` 调用完全一致的 drafts、roots 和
   rejected propositions。

Agent 获得五个 bounded 工具：

| 工具 | 用途 | 调用条件 |
|---|---|---|
| `read_task` | 重读同一 attempt 的六字段冻结上下文 | Compact 后、记忆不确定或需要复核 hash/record 时 |
| `query_model` | 查询分页结构化 inspect 事实 | 存在明确的结构证据缺口时 |
| `observe_trace` | 探索一条有限事件轨迹 | 存在明确的轨迹问题时 |
| `lookup_source_trace` | 查询 source 与 fcstm 元素映射 | 引用边界不清楚时 |
| `evaluate_checks` | 绑定并执行完整 check draft batch | 最终 batch 必须调用且通过机械 gate |

`evaluate_checks` 内部固定调用 `run_scenarios`、`verify_properties`、
`verify_static_consistency` 和 `validate_discovery_checks`，但不调用 LLM、不修改模型、
不产生 issue verdict。Controller 在 Agent 结束后要求最终 `check_drafts` 与本 attempt
中某次 eligible 调用的完整输入一致，然后才发布 method records。每个 Agent 工具的
注册后 docstring 都定义 Purpose、Parameters、Returns、Execution、Failure semantics、
Evidence limitations、Permissions 与 Example，并由合同测试直接检查。

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

Replay 文件只通过隐藏的测试参数用于确定性合同测试，产物会明确写
`real_llm=false`、`academic_eligible=false`，不能作为真实 demo 或论文实验结果。

## 验证

```bash
make discover-test
```

测试覆盖 system prompt 六步协议、单次 `AgentApp.run`、五工具 allowlist、详细
docstring、严格输入 schema、BMC/replay 义务、append-only records、zero-root 发布、
reference/gold 防泄漏、自定义输入和确定性报告。
