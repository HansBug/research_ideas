# Expert Review

本目录包含独立的 `expert_review` 专家评审模块。

## 模块定位

它负责接收：

1. `prompt`
2. `input_text`
3. `pred_output`
4. 可选 `ref_output`

然后输出结构化的专家评审结果。

## 当前代码入口

- [__init__.py](./__init__.py)：公开 Python API。
- [__main__.py](./__main__.py)：命令行入口。
- [expert_review_agent.py](./expert_review_agent.py)：当前实现主入口。
- [expert_review_schema.py](./expert_review_schema.py)：输入输出 schema。
- [test_expert_review.py](./test_expert_review.py)：最小测试集。

## 文档入口

设计与演化文档统一放在：

- [designs/README.md](./designs/README.md)

其中：

- `v0` 基线资料见 [designs/v0/README.md](./designs/v0/README.md)
- `v1` 重构设计见 [designs/v1/README.md](./designs/v1/README.md)

## 推荐阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再读 [designs/README.md](./designs/README.md)
3. 如需了解现状，读 [designs/v0/README.md](./designs/v0/README.md)
4. 如需了解重构方向，读 [designs/v1/README.md](./designs/v1/README.md)
5. 最后回看代码实现

## 仍保持不变的外部接口

当前对外入口仍以这四个字段为核心：

1. `prompt`
2. `input_text`
3. `pred_output`
4. `ref_output`

这是后续重构时优先保持兼容的接口层。

## 当前使用方式

### Python API

最直接的入口是：

- [__init__.py](./__init__.py) 里的 `review_artifacts()`
- [__init__.py](./__init__.py) 里的 `review_model()`

示例：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
venv/bin/python - <<'PY'
from expert_review import review_artifacts

result = review_artifacts(
    prompt=(
        "As a state-machine modeling expert, review the predicted printer model. "
        "重点检查是否遗漏关键需求，以及是否引入了没有需求依据的额外状态或迁移。"
    ),
    input_text=(
        "R1: When an authorized user logs in, the system becomes ready.\n"
        "R2: When start is pressed in ready mode, printing begins.\n"
        "R3: A paper jam suspends printing and allows resume.\n"
        "R4: Logoff is not allowed during active printing."
    ),
    pred_output='{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"},{"name":"Maintenance"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""},{"source":"Ready","target":"Maintenance","event":"selfCheck","guard":"","action":""}]}',
    ref_output='{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""}]}',
)

print(result.overall_score)
print(result.overall_judgement)
print(result.overall_reason_text)
PY
```

### CLI

单次命令行入口由 [__main__.py](./__main__.py) 提供：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
venv/bin/python -m expert_review \
  --prompt '帮我给这个状态机模型进行评价，重点检查需求覆盖、行为一致性、以及是否引入了没有依据的额外状态。' \
  --input 'R1: 用户登录且授权后系统进入Ready。 R2: 纸张卡住时打印进入Suspended，并可恢复。 R3: 打印中不允许退出登录。' \
  --ref-output '{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""}]}' \
  --pred-output '{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"},{"name":"Maintenance"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"authorized","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""},{"source":"Ready","target":"Maintenance","event":"selfCheck","guard":"","action":""}]}'
```

## 想看更详细的现状说明时

如果你想看：

1. 当前系统到底怎么工作的
2. 为什么会形成现在这套实现
3. 与 TTool-AI 人类评分对齐到了什么程度

请直接进入：

- [designs/v0/EXPERT_REVIEW_RESEARCH.md](./designs/v0/EXPERT_REVIEW_RESEARCH.md)
- [designs/v0/EXPERT_REVIEW_ARCHITECTURE.md](./designs/v0/EXPERT_REVIEW_ARCHITECTURE.md)
- [designs/v0/EXPERT_ALIGNMENT_REPORT.md](./designs/v0/EXPERT_ALIGNMENT_REPORT.md)
