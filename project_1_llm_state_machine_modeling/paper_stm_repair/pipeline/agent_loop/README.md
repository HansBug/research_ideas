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
5. 仅针对 eligible batch 的明确证据缺口调用一次合并后的轨迹或 source-trace
   microscope；若调用后修改 drafts，必须重新执行最终完整 batch。
6. 对完整 check batch 给出 `confirmed / candidate_only / rejected` 理由。
7. 最后一轮通过结构化终止工具，一次性提交与某次 eligible `evaluate_checks` 调用
   完全一致的 drafts、roots 和
   rejected propositions。

Agent 获得七个 bounded 工具：

| 工具 | 用途 | 调用条件 |
|---|---|---|
| `read_fcstm_guide` | 读取 `pyfcstm.llm` 中完整、带版本与 SHA-256 的 FCSTM guide | 必用，且必须是首次业务工具调用 |
| `read_fbmcq_guide` | 读取 `pyfcstm.llm` 中完整、带版本与 SHA-256 的 FBMCQ guide | 首次构造、修订或提交 property 前必用 |
| `read_task` | 首次读取同一 attempt 的六字段冻结上下文 | FCSTM guide 后必用；重复调用只返回 hash 与 `no_new_task_fact` |
| `query_model` | 查询分页结构化 inspect 事实 | 存在明确的结构证据缺口时 |
| `observe_trace` | 探索一条最短有限事件轨迹 | eligible batch 之后；每个不同 drafts hash 最多完成一次，重复同一 batch 不重置 |
| `lookup_source_trace` | 合并查询 source 与 fcstm 元素映射 | eligible batch 之后；一次传入该 batch 全部 refs，每个不同 drafts hash 最多完成一次 |
| `evaluate_checks` | 绑定并执行完整 check draft batch | 最终 batch 必须调用且通过机械 gate |

初始 provider input 不包含 FCSTM 正文，只包含 run/model 身份和 hash。Controller 通过
内容隔离、工具前置条件和 run 后顺序复核三层机制强制执行
`read_fcstm_guide -> read_task -> model work`；property batch 另强制
`read_fbmcq_guide -> property work`。任何先违规后补读的 attempt 仍会 fail-closed。
三项冻结资源读取都只在首次调用返回完整大文本；同一 run 内重复调用只返回稳定
资源身份、SHA-256 与 `no_new_*_fact`，防止完全相同的 NL/STM/guide 被反复注入上下文。
结构化终止工具的物理名称与 prompt 一致，固定为 `submit_discovery`。若 provider
结束当前 graph 路径却未返回结构化结果，Discover 会保留完整且满足 provider
tool-message 协议的可见历史，并启用一次可审计恢复路径，要求先补齐遗漏的 mandatory
business tool，再结构化提交。若末尾 assistant 消息只包含 provider 无法解析的
`submit_discovery` 调用，该失败提交会作为 `rejected` 证据保留，但不会再次发送给
provider。若末尾 assistant 消息只包含一个参数无法解析、从未执行且名称属于当前
allowlist 的业务工具调用，runtime 会同样保留拒绝审计、排除该条畸形消息，并在同一
Agent run 内继续强制尚未完成的 mandatory 工具；正常业务调用缺少结果、未知工具、
混合调用或历史中段损坏仍直接 fail-closed。恢复路径不限制
整次运行的模型调用、工具调用、时间或 token，也不会从普通文本伪造结果或工具结果。

`evaluate_checks` 内部固定调用 `run_scenarios`、`verify_properties`、
`verify_static_consistency` 和 `validate_discovery_checks`，但不调用 LLM、不修改模型、
不产生 issue verdict。Controller 在 Agent 结束后要求最终 `check_drafts` 与本 attempt
中某次 eligible 调用的完整输入一致，然后才发布 method records。结构化输出 schema
同时绑定本次 run 已发生的 `evaluate_checks` 调用：如果最终 drafts 从未作为完整 batch
执行、root 引用了最终 batch 之外的 check、root 把
`expected_outcome_match_status=matches` 的 NL-grounded 通过项写成问题、check 没有被 root 或 rejected
proposition 完整覆盖，或者在没有任何一对一 source trace 的 run 中声称 `confirmed`，
provider 会在同一个 `AgentApp.run` 内收到 schema validation error 并重试结构化提交，
而不是先结束 Agent 再由外层报错。Controller 在 Agent 结束后仍会独立复验 records、
逐项 source refs、guide 顺序和全部发布门，动态 schema 不是对最终审计的替代。每个 Agent 工具的
注册后 docstring 都定义 Purpose、Parameters、Returns、Execution、Failure semantics、
Evidence limitations、Permissions 与 Example，并由合同测试直接检查。

Scenario 不是“从全局初始态直接点击一个任意事件”。每个 scenario draft 必须给出完整
`event_labels` 和 `precondition_state_label`：前 $n-1$ 个事件是从模型初始态出发的 setup，
最后一个事件才是被测事件。确定性 Controller 绑定后记录 `setup_events`、`tested_event` 和
`precondition_state`；setup 中存在未消费事件或没有到达前置状态时，结果固定为
`invalid_precondition`，该 check 不计入 executed checks，完整 batch 的 gate 也不会通过。
例如要检查只在 `Armed` 中有效的 `fire`，draft 应提供 `['arm', 'fire']` 和前置状态
`Armed`；只提交 `['fire']` 不能用其失败来声称模型存在行为错误。
此外，前置状态不能只靠 Agent 自报：每个 NL-grounded check 必须至少提供一条
`nl_basis.quote`，且每条 quote 必须能在冻结 NL 中核验，
每条 `source_basis` 必须能在冻结 raw/source `STM_0` 中核验，并且 scenario 至少有一条
已核验依据同时出现前置状态与最后的被测事件。比如 NL 明确写的是“在 `Armed` 收到
`fire`”，却把 `Idle` 声明为前置状态，即使 `Idle` 恰好是全局初始状态，也会在 binding
阶段被拒绝，不能产生 eligible 的 `contradicts` 证据。若 NL 没有写出前置状态，可以由
raw/source transition 提供 operational precondition；但 raw/source 不能替代 NL 依据。

`confirmed` root 还必须通过独立的确定性归因门：每个引用都要在冻结的元素级 source
trace 中形成严格一对一映射。仅在 inspect 中存在、仅被 check binder 使用，或只有
ambiguous/untraceable mapping，都不能进入 Repair，只能降为 `candidate_only` 或
`rejected`。唯一不需要逐元素 trace entry 的情况是 raw/source 与 fcstm 文本确实相同的
custom identity input。

最终输出严格区分 `model_element_refs`（FCSTM 中的 state/event/transition/variable 定位）
与 `source_element_refs`（raw/source 模型侧定位），禁止把 `state:*` 等 FCSTM 引用混进
source 字段。每个 final check 必须恰好归属一个 root 或一个 rejected proposition。
每个 proposition 的 `model_element_refs` 还必须来自它自己拥有的 checks 的
`binding_refs`；不能拿另一个无关 state/event 的合法 source trace 来凑齐 confirmed 归因。
Rejected proposition 还必须给出结构化 `rejection_reason`：`expectation_matched`、
`check_semantically_invalid`、`out_of_scope`、`representation_only` 或
`insufficient_evidence`；自然语言 rationale 继续解释具体逻辑。NL check 已产生
`contradicts` 结果时，不能用“预期已满足”或笼统“证据不足”把它静默丢弃。

真实 Agent 调用抛异常或收到中断时，Controller 会先追加 `agent_attempt_finished` 与
`run_failed` 两个终态记录，再原样抛出异常；不会留下只有 `agent_attempt_started` 的
方法记录前缀，也不会把 `.part` audit 当作成功 receipt。

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

资源预算与必用工具协议是两套独立机制。默认无限制不等于允许 Agent 跳过方法步骤：
`paper1-discover-mandatory-v1` 会在同一个 `AgentApp.run()` 内依次强制
`read_fcstm_guide -> read_task -> evaluate_checks`。如果首次 property batch 在尚未读取
FBMCQ guide 时提交，下一轮强制 `read_fbmcq_guide`，随后继续强制
`evaluate_checks`，直至得到一个 `gate.eligible=true` 的完整批次。该策略只选择合同中
已经标为必用的工具，并在该轮临时把 provider 可见工具面收窄到这一个工具，防止不完整
的 `tool_choice` 实现绕过必用步骤。执行入口还会再次核对当前 mandatory tool；即使
provider 幻觉调用了全局注册但本轮未暴露的其他工具，底层工具逻辑也不会执行，audit 会
把该动作记录为 `rejected`、`tool_executed=false`。它不生成检查内容、不决定 issue verdict。获得
eligible batch 后，完整工具面与结构化终止面恢复，Agent 重新自由选择可选 post-batch
工具或提交结构化结果。

事件条件行为不能降格成只检查目标状态可达的 property。例如“在 `Autonomous` 中收到
`Human_Steering_Cmd_or_Brake_Pressed` 后回到 `InitialState`”不能只写成
“`InitialState` 在 3 步内可达”；后者没有编码前置状态和触发事件。Controller 会确定性
拒绝这种 draft，并要求改用包含完整 setup、precondition 和 tested event 的 scenario。
纯状态命题（例如“`Done` 可达”或“`Done` 是 simple state”）仍可使用 property。

每次到达执行边界的 `evaluate_checks` attempt 都会进入 append-only 的
`evaluate_checks_attempts_completed` record：既包括因指南前置条件而明确未执行的调用，
也包括真正执行的 batch；后者会保留原始 draft、绑定拒绝、gate reason、实际执行的
check ID，以及最终是否被 structured submission 选用。确定性 renderer 会把
这些尝试写入 `loops/discover.md`，因此 zero-root 运行不会只剩 Agent 的笼统自述。

`manifest.json.code_provenance` 记录精确 git commit、分支和 tracked-worktree dirty
状态。未跟踪的 `runs/paper1/` 输出不计入代码 dirty 判定；正式可比较运行仍应使用
`tracked_worktree_dirty=false` 的提交态。capability preflight 还会比较父仓库
`HEAD:pyfcstm` gitlink 与本地 submodule worktree `HEAD`；任一侧不可读或 commit 不一致时
写入 `run_failed` 并停止，避免同版本号下的 pyfcstm 语义漂移混入可比较运行。

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
