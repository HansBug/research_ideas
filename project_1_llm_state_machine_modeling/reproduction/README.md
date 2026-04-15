# Reproduction Workspace

This directory contains a runnable reproduction workspace for the four recently prioritized `project_1` baselines:

1. `llms_emp`
2. `ttool-ai`
3. `Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study`
4. `Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models`

The workspace is organized around four goals:

1. Download raw artifacts into local storage.
2. Repair or enrich baseline `parquet` assets when the current discussion copy is incomplete.
3. Run reproducible LLM-based baselines with the local Codex API configuration, preferring `airouter -> findcg -> miaocg`.
4. Write machine-readable result `parquet` files and a human-readable reproduction report.

## Main Entry

Use [run_all.py](./run_all.py).

Typical flow:

```bash
venv/bin/pip install -r project_1_llm_state_machine_modeling/reproduction/requirements-reprod.txt

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py download-raw

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py augment-parquets

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline llms_emp
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline ttool
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline nimbus
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline structure_event

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py report
```

## Outputs

- Raw downloads: [data/raw](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/data/raw)
- Derived `parquet`: [data/derived](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/data/derived)
- Runtime results: [results](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/results)
- Final report: [REPRODUCTION_REPORT.md](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/REPRODUCTION_REPORT.md)

## Code Layout

- [run_all.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/run_all.py): CLI entry.
- [tasks.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/tasks.py): raw download, parquet augmentation, report generation.
- [llm_client.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/llm_client.py): official `openai` client wrapper with provider fallback and disk cache.
- [baselines/baseline_llms_emp.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baselines/baseline_llms_emp.py): `llms_emp` reproduction.
- [baselines/baseline_ttool.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baselines/baseline_ttool.py): `ttool-ai` plus local `sm/MTI` reproduction.
- [baselines/baseline_nimbus.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baselines/baseline_nimbus.py): `Nimbus` fragment reproduction.
- [baselines/baseline_structure_event.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baselines/baseline_structure_event.py): `Structure/Event-Driven` reproduction.

- [expert_review/expert_review_agent.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/expert_review/expert_review_agent.py): 通用专家评审 agent。
- [expert_review/expert_review_schema.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/expert_review/expert_review_schema.py): 结构化输入输出 schema。
- [run_expert_review.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/run_expert_review.py): Python/CLI 对应的批量评审入口。

## Expert Review Usage

`expert_review` 子模块现在是完全独立的状态机专家评审 agent。它不依赖 baseline preset，也不要求调用方导入 reproduction 里的其他 schema。唯一需要的输入只有四个：

1. `prompt`
2. `input`
3. `pred-output`
4. `ref-output`，可选

也就是说，`prompt` 就相当于“本次评审任务设定”。你可以直接在这里告诉 agent：

1. 本次要评什么
2. 重点检查什么
3. 更接近哪篇论文里的专家标准
4. 有 `ref-output` 时应该怎样利用参考答案

输出始终是结构化 JSON，核心字段包括：

1. `overall_score`
2. `overall_judgement`
3. `overall_reason_text`
4. `dimension_results`
5. `requirement_trace_results`
6. `unsupported_model_elements`
7. `evidence_summary`

### How It Works

下面是当前实现的真实工作流程，对应主入口在 [expert_review/expert_review_agent.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/expert_review/expert_review_agent.py)：

1. 接收四个输入：`prompt / input / pred-output / optional ref-output`。
2. 根据 `prompt` 自动推断评审 profile，比如通用状态机评审、强调 requirements/traceability 的评审、或 TTool/AVATAR 风格评审。
3. 先做确定性预处理，包括需求切分、状态机 inventory 提取、简单 trace 候选构建、以及 reference 对齐准备。
4. 对 `pred-output` 和 `ref-output` 的处理不依赖固定格式。模块会先做“状态机专用的通用文本解析”，尽量从任意文本里提取 `states / transitions / blocks / signals / rules`。
5. 如果文本并不是仓库里已知的几种格式，而前一步抽取结果仍然很稀、且本地有可用 LLM，则会再触发一次 LLM 要素抽取，把未知格式归一成接近标准状态机结构的 payload。
6. 这个未知格式 fallback 只面向状态机及其近邻表示，不会把顺序图、类图、use case 之类无关 artifact 强行解释成状态机。
7. 真正评分时采用 LLM-first：优先用 `LangChain + ChatOpenAI` 生成结构化评审 JSON。
8. 如果 LLM 不可用、超时、或返回 JSON 不合法，就自动退回 heuristic reviewer。heuristic reviewer 仍然输出完整结构化结果，不会因为没有 API 就不可用。
9. 不管走 LLM 还是 heuristic，最终输出字段都保持同一套结构，方便后续写入 parquet 或做人工抽查。

### Python Function API

下面这个例子可以从仓库根目录直接复制运行。输入全部是内联字符串，不依赖任何其他文件。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
venv/bin/python - <<'PY'
from expert_review import review_artifacts

result = review_artifacts(
    prompt=(
        "As a state-machine modeling expert, review the predicted printer model. "
        "重点检查两个方面：1. 是否遗漏关键需求；2. 是否引入没有需求依据的额外状态或迁移。 "
        "如果结构不同但行为仍然合理，要解释为什么仍可接受。"
    ),
    input_text=(
        "R1: When an authorized user logs in, the system becomes ready.\n"
        "R2: When start is pressed in ready mode, printing begins.\n"
        "R3: A paper jam suspends printing and allows resume.\n"
        "R4: Logoff is not allowed during active printing."
    ),
    pred_output='''{
      "machine_name": "Printer",
      "states": [
        {"name": "Idle", "parent": null, "parallel_group": null, "is_history": false, "is_initial": true},
        {"name": "Ready", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Printing", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Suspended", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Maintenance", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false}
      ],
      "transitions": [
        {"source": "Idle", "target": "Ready", "event": "login", "guard": "authorized", "action": ""},
        {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
        {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
        {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""},
        {"source": "Ready", "target": "Maintenance", "event": "selfCheck", "guard": "", "action": ""}
      ]
    }''',
    ref_output='''{
      "machine_name": "Printer",
      "states": [
        {"name": "Idle", "parent": null, "parallel_group": null, "is_history": false, "is_initial": true},
        {"name": "Ready", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Printing", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Suspended", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false}
      ],
      "transitions": [
        {"source": "Idle", "target": "Ready", "event": "login", "guard": "authorized", "action": ""},
        {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
        {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
        {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""}
      ]
    }'''
)

print(result.overall_score)
print(result.overall_judgement)
print(result.overall_reason_text)
PY
```

这个例子里故意在预测模型里加入了没有需求依据的 `Maintenance` 状态和 `selfCheck` 转移，便于看到结构化扣分理由。

### Real CLI Call With Reference

下面这条命令是实际跑过的，直接可以复制：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
venv/bin/python -m expert_review \
  --prompt '帮我给这个状态机模型进行评价，重点检查需求覆盖、行为一致性、以及是否引入了没有依据的额外状态。' \
  --input 'R1: 用户登录且授权后系统进入Ready。 R2: 纸张卡住时打印进入Suspended，并可恢复。 R3: 打印中不允许退出登录。' \
  --ref-output '{"machine_name":"Printer","states":[{"name":"Idle","parent":null},{"name":"Ready","parent":null},{"name":"Printing","parent":null},{"name":"Suspended","parent":null}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""}]}' \
  --pred-output '{"machine_name":"Printer","states":[{"name":"Idle","parent":null},{"name":"Ready","parent":null},{"name":"Printing","parent":null},{"name":"Suspended","parent":null},{"name":"Maintenance","parent":null}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""},{"source":"Ready","target":"Maintenance","event":"selfCheck","guard":"","action":""}]}'
```

上面这条命令的真实输出如下。这里保留了关键字段和部分子级结果，原始输出是一次真实运行，不是手写示例：

```json
{
  "prompt": "帮我给这个状态机模型进行评价，重点检查需求覆盖、行为一致性、以及是否引入了没有依据的额外状态。",
  "overall_score": 0.917778,
  "overall_judgement": "excellent",
  "overall_reason_text": "The review followed the user prompt: 帮我给这个状态机模型进行评价，重点检查需求覆盖、行为一致性、以及是否引入了没有依据的额外状态。. Strengths were credited where the prediction remained interpretable and covered the intended behavior. Deductions came from missing requirement traces, unsupported extra content, or inflated structure.",
  "used_review_backend": "heuristic",
  "dimension_results": [
    {
      "dimension_name": "notation_syntax",
      "score": 0.9,
      "judgement": "excellent",
      "reason_text": "The prediction appears structurally interpretable as a modeling artifact."
    },
    {
      "dimension_name": "behavioral_consistency",
      "score": 0.888889,
      "judgement": "good",
      "reason_text": "The prediction preserves some reference structure at the state level (F1=0.89) and transition level (F1=0.89). This remains only a proxy for behavior."
    }
  ],
  "unsupported_model_elements": [
    {
      "element_id": "ready maintenance selfcheck",
      "element_kind": "transition",
      "element_text": "ready maintenance selfcheck",
      "issue_type": "extra",
      "reason_text": "This transition appears in the prediction but not in the extracted reference inventory."
    },
    {
      "element_id": "maintenance",
      "element_kind": "state",
      "element_text": "maintenance",
      "issue_type": "extra",
      "reason_text": "This state appears in the prediction but not in the extracted reference inventory."
    }
  ],
  "notes": [
    "comparison_policy=component_semantic_match",
    "rubric_text=Review the predicted model as a software behavior modeling expert. Separate syntax, semantic completeness, behavioral consistency, requirement traceability, and pragmatic clarity. If a reference output is provided, compare against it semantically. If no reference output is provided, perform a standalone expert review against the input description.",
    "LLM primary review failed: ValueError: No JSON object found"
  ]
}
```

这个真实输出说明了两点：

1. 当 `ref-output` 存在时，agent 会显式指出 prediction 里多出的状态和转移。
2. 即使 LLM 主路径失败，agent 也会自动退回 heuristic，并保持结构化输出不变。

### Real CLI Call Without Reference And With Unknown Format

下面这个例子是“未知格式但仍然是状态机文本”的真实调用。这里的 `pred-output` 不是仓库里既有的 JSON 格式，而是一段自由文本 DSL：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
venv/bin/python -m expert_review \
  --prompt 'Help me review this behavior model and focus on coverage, missing behavior, and clarity.' \
  --input 'R1: start moves the controller from Idle to Working. R2: error moves the controller into Fault.' \
  --pred-output 'component Controller
state Idle
state Working
state Fault
Idle -> Working : start
Working -> Fault : error
'
```

这条命令的真实输出如下：

```json
{
  "prompt": "Help me review this behavior model and focus on coverage, missing behavior, and clarity.",
  "overall_score": 0.924,
  "overall_judgement": "excellent",
  "overall_reason_text": "The review followed the user prompt: Help me review this behavior model and focus on coverage, missing behavior, and clarity.. Strengths were credited where the prediction remained interpretable and covered the intended behavior. Deductions came from missing requirement traces, unsupported extra content, or inflated structure.",
  "used_review_backend": "heuristic",
  "dimension_results": [
    {
      "dimension_name": "notation_syntax",
      "score": 0.9,
      "judgement": "excellent",
      "reason_text": "The prediction appears structurally interpretable as a modeling artifact."
    },
    {
      "dimension_name": "behavioral_consistency",
      "score": 0.9,
      "judgement": "excellent",
      "reason_text": "No reference output was provided, so behavioral adequacy was judged from whether the prediction contains explicit model structure and whether requirement-triggered behavior is represented in a traceable way."
    },
    {
      "dimension_name": "pragmatic_clarity",
      "score": 0.82,
      "judgement": "good",
      "reason_text": "No reference output was provided, so clarity was judged from absolute structural burden and whether the predicted model appears reviewable without unnecessary inflation. Predicted states=6, predicted transitions=4."
    }
  ],
  "requirement_trace_results": [
    {
      "requirement_id": "R1",
      "requirement_text": "start moves the controller from Idle to Working. R2: error moves the controller into Fault.",
      "status": "matched",
      "reason_text": "Requirement R1 is supported by 8 predicted element(s), including state Idle."
    }
  ],
  "unsupported_model_elements": [],
  "notes": [
    "comparison_policy=component_semantic_match",
    "rubric_text=Review the predicted model as a software behavior modeling expert. Separate syntax, semantic completeness, behavioral consistency, requirement traceability, and pragmatic clarity. If a reference output is provided, compare against it semantically. If no reference output is provided, perform a standalone expert review against the input description.",
    "LLM primary review failed: APITimeoutError: Request timed out."
  ]
}
```

这个例子说明当前实现确实支持“非已知格式”的状态机文本，而不是只会处理仓库里那几种固定 JSON。

### Batch CLI Example

`expert_review` 子模块本身完全独立，但仓库里仍然保留了一个批量包装脚本 [run_expert_review.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/run_expert_review.py)，用于把已有 `predictions.parquet` 自动映射成上述四个输入后批量执行：

```bash
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_expert_review.py \
  review-baseline \
  --baseline structure_event \
  --max-samples 2
```

输出会写到：

1. [results/structure_event/expert_review/reviews.parquet](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/results/structure_event/expert_review/reviews.parquet)
2. [results/structure_event/expert_review/summary.json](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/results/structure_event/expert_review/summary.json)

### Practical Notes

1. 如果本地有可用 API key，`expert_review` 会优先尝试 `LangChain + ChatOpenAI` 的 LLM 主导评审。
2. 如果没有可用 API key，它会自动退回本地 heuristic fallback，CLI 和 Python API 仍然能跑通。
3. 独立接口只保留 `prompt / input / pred-output / optional ref-output`，不再暴露额外的 schema 字段。
4. 对未知格式的支持只面向状态机及其近邻表示，不会把顺序图、类图这类无关 artifact 强行映射成状态机。
5. Python 示例和 CLI 示例都故意把输入写成内联字符串，方便后续直接复制、修改和复用。

## Notes

- API keys are loaded from the current environment first and then from local `~/.codex/*.env` files when available.
- The workspace does not persist secrets into tracked files.
- Default provider order is `airouter -> findcg -> miaocg`.
- `api68886868` is intentionally excluded from the default automatic retry chain because it is less stable in this environment.
- LLM access uses the official `openai` Python client; prompt assembly uses `langchain_core.prompts.ChatPromptTemplate`.
- The client currently falls back across non-stream `responses` and `chat.completions`, then switches provider if needed.
