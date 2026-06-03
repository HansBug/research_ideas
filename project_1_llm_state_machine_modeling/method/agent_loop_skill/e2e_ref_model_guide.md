# PR-E2 e2e ref-model skill 使用指南

本文件用于 PR-E2：让 Codex / Claude Code 类 agent 在**不调用顶层 agent-loop runtime** 的前提下，基于 repo-local skill / toolbox 自主完成“NL + 论文子路径 -> FCSTM/pyfcstm ref model 候选”的 e2e 建模、验证、修复和留痕。

## 1. 硬性边界

1. **禁止调用顶层 agent-loop runtime**：不得调用 `method.loop.run_agent_loop(...)`、PR-D representative runner 或任何一键 full staged runner。
2. **允许调用底层工具箱**：可以调用 `SD-*` deterministic tools、`SL-*` prompt generators、pyfcstm parse/build/inspect/sim utilities，以及仓库内只读论文材料。
3. **修改范围**：若需要改 skill，本 PR 默认只允许改 `project_1_llm_state_machine_modeling/method/agent_loop_skill/` 及其子路径。若发现来自上游语法 prompt / grammar digest 的硬伤会直接误导 skill 使用者（例如实际 parser 不支持却在 grammar 中要求的语法），可作为特例修改 `project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md`；此类改动必须先核对相邻 PR（尤其 PR-E1）已有 diff，尽量采用相同修正以避免 merge 后冲突。
4. **质量优先**：允许 Codex / Claude Code 长时间运行。时间限制只用于防止死锁或 CLI 挂死，不应用来牺牲论文阅读、验证或 repair 质量。
5. **证据留痕**：每个样本的输入、读取路径、候选模型、检查反馈、修复轨迹和最终判断都必须能写入 PR comment。

## 2. 推荐输入格式

每个 e2e 样本至少提供：

```text
Path 类别: Path-1 或 Path-2
样本编号: P1-01 / P1-02 / P2-01 / P2-02 ...
NL 片段: 可来自 eval/data/sources/<case>/nl.md 或 sources/<case>/STM.md / DESC.md 中整理出的需求片段
论文子路径: project_1_llm_state_machine_modeling/sources/<case>/
目标: 产出 FCSTM/pyfcstm ref model 候选，并记录验证/修复轨迹
禁止: 不得调用 method.loop.run_agent_loop 或一键 runner
```

论文子路径通常应包含：

```text
paper.pdf
paper_content.txt
bibtex.bib
DESC.md
STM.md
```

优先阅读顺序：

```text
bibtex.bib -> STM.md / DESC.md -> paper_content.txt -> paper.pdf（必要时核对）
```

`STM.md` / `DESC.md` 可以作为人工整理过的索引，但不能替代论文证据。每个正式样本默认应至少抽读 `paper_content.txt` 中与状态机、状态表、流程图、控制算法、结果解释直接相关的章节；如果没有回看 `paper_content.txt`，必须在 PR comment 中明确说明原因，并把该样本标为 grounding 风险，reviewer 可按影响评为 I。

## 3. 推荐 e2e 流程

### E0. Skill discovery

读取：

```text
project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md
project_1_llm_state_machine_modeling/method/agent_loop_skill/stages/
```

输出记录：列出实际读取的 skill 文件。

### E1. Evidence grounding

从 NL 与论文材料抽取：

- 控制对象与边界；
- 状态 / 阶段 / 模式；
- 输入事件或传感信号；
- 输出动作；
- guard / 阈值 / 定时；
- 异常、复位、回退或非法状态；
- 原文证据位置或整理文件位置。

输出记录：一张简短 grounding 表，说明每个状态/转移来自哪里。

### E2. Initial candidate modeling

可以使用 `SL-1` prompt generator 作为提示蓝本，也可以由 agent 自行建模，但必须遵守 pyfcstm/FCSTM 语法，并输出候选 DSL。

禁止把论文无关背景、连续控制公式或硬件清单机械塞进状态机；优先保留可验证的离散控制骨架。

### E3. Deterministic checks

正式样本必须至少尝试 `SD-2 -> SD-3 -> SD-4 -> SD-6`。`SD-6` 不是可随意省略的 optional polish：P1/P2 ref model 候选只有在行为 scenario 上跑过仿真，才有足够证据交给下游。若场景尚未充分，只能标记为 `部分可用 / oracle weak`，不能声称 ready。

若某个工具入口不可用，应记录命令、错误摘要和影响分类，不要静默跳过。

当前 pyfcstm parser 注意事项：

- 变量类型以实际 parser 为准；当前已验证支持 `def int` / `def float`，不支持 `def bool`、`true`、`false`。布尔量请用 `int` flag（如 `0/1`）表达，并在注释中说明语义。
- `// @external` / `// @input` 注释可作为人工/下游静态验证的语义标记，但当前 `run_sd4_design(..., policy_profile="generated_candidate")` 不消费该注释；因此它不能自动消除 `W_UNWRITTEN_READ_VAR` / `W_GUARD_VARS_NEVER_CHANGE`。
- 外部传感输入优先用显式事件更新、环境采样 aspect、或 `int/float` 变量 + 清晰 PR comment 说明来建模；不要用无意义 self-assignment 只为消警。

```python
from method.schema import StageContext, TestScenario, ScenarioSet
from method.stages.sd_tools import (
    freeze_scenario_set,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)

context = StageContext(nl=nl, current_dsl=current_dsl)
parse_feedback, parse_meta = run_sd2_parse(current_dsl, context)
if parse_feedback.ok:
    semantic_feedback, semantic_meta, build = run_sd3_semantic(current_dsl, context)
if semantic_feedback.ok:
    design_feedback, design_meta = run_sd4_design(context, policy_profile="generated_candidate")
```

如需构造最小 scenario，可使用：

```python
import hashlib

scenario = TestScenario(
    name="sanity",
    description="hot-start sanity",
    initial_vars={"some_flag": 0},  # hot-start 时显式给出所需变量初值；不要依赖隐式环境
    steps=[],
)
coverage, coverage_meta = run_sd5a_scenario_coverage(current_dsl, [scenario])
scenario_set, freeze_meta = freeze_scenario_set(
    [scenario],
    source_dsl_hash="sha256:" + hashlib.sha256(current_dsl.encode("utf-8")).hexdigest(),
    source_inspect_hash="sha256:" + hashlib.sha256(repr(context.inspect_json or {}).encode("utf-8")).hexdigest(),
    source_grounding_hash="sha256:" + hashlib.sha256(repr(context.grounding_map).encode("utf-8")).hexdigest(),
    coverage_report=coverage,
)
sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
```

### E4. Repair loop

若 parse / semantic / design / sim / review 任一失败：

1. 选择最早 blocking feedback；
2. 用 `SD-8 FixPlan` 产出结构化修复计划；
3. 使用 `SL-9` prompt generator 或 agent 自行修复；
4. 用 `SD-10 RepairReview` 或等价本地检查确认未引入漂移；
5. 回到 E3 重新从 parse 开始检查。

注意：`suggested_fix` 只是规则诊断的参考 hint，不是必须照抄的编辑命令。agent 可以基于 NL 与全局约束提出更合理的修复方案。

### E5. Optional lightweight review

可以使用 `SL-7` / `SL-10B` prompt generator 组织外部 LLM 评审，但必须记录：

- 输入摘要；
- provider / CLI；
- 输出 decision / findings；
- 是否 blocking；
- 对模型质量的影响。

### E6. Final evidence package

每次 skill 修改并 push 后，必须重新跑一轮 4 个样本（Path-1 至少 2 个、Path-2 至少 2 个），并把每个样本作为独立 PR comment 留痕。PR-E2 不要求完全复制 PR-E1 的 run-record 格式，但每个样本 comment 至少应接近 PR-E1 报告的信息密度，包含：

- 样本编号、Path 类别、NL 来源、论文路径；
- 使用的 agent / CLI / skill 入口；
- 实际读取文件；
- 禁止调用项检查结论；
- 输入 NL 原文；
- 输入 NL 中文翻译 / 中文释义；
- 最终 FCSTM/pyfcstm 候选模型全文；
- 全流程真实摘要表：stage、是否 LLM、轮次、结果、获取的信息/反馈、本阶段做了什么、DSL 修改、artifact/命令；
- deterministic checks / review checks 结果；
- repair 轨迹与每次修复依据；
- 作为 ref model 的学术质量评审：覆盖、抽象、未覆盖语义、是否 `main_result_eligible`、仍需人工签核的问题；
- skill 改进建议。

若本轮 skill 修改后 4 个样本没有重跑，不能声称“本轮已 ready”；只能标为局部修复或文档修正。

## 4. 建模习语与边界模板

### 4.1 外部输入变量

控制系统论文常把传感器、环境量或连续控制器输出作为状态机 guard 输入。PR-E2 推荐按以下优先级建模：

1. **事件更新模式**：用事件表达外部输入变化，例如 `BPUpdated`、`RefreshSensors`，并在转移或 aspect 中更新变量。
2. **环境采样 aspect 模式**：对每个控制周期都会刷新的输入，用 root-level aspect 表达采样意图；不要用无意义 self-assignment 伪造内部写入。
3. **人工标记模式**：可在变量声明后写 `// @external` 或 `// @input` 辅助人工审计，但必须说明当前 SD-4 不消费该注释，不能把它当作自动通过依据。

若 SD-4 因外部输入给出 blocking warning，producer 必须在 PR comment 中解释：这是模型错误、工具策略不匹配、还是需要补事件/aspect 的真实问题。

### 4.2 事件作用域与初始 cycle

复杂/层次模型中，局部事件、forced transition 与初始 transition 很容易造成“看起来能 parse，但 scenario 不触发”的假阳性。PR-E2 producer 必须遵守：

- 在 scenario 中注入事件时，说明它是 root event 还是 nested/local event；必要时参考 `stages/SD-6.md` 和 pyfcstm 文档确认事件路径。
- 对 composite state 的初始 transition，至少设置一个 hot-start sanity scenario，并在 comment 中说明初始 cycle 后实际落到哪个 leaf state。
- 若模型使用 forced transition 或 local event，必须至少有一个 scenario 覆盖该边；否则标记为 `oracle weak`。
- 若 scenario 需要 hot-start 到某个 nested state，必须显式提供 `initial_state` 与所需 `initial_vars`，不要依赖隐式变量默认值。

### 4.3 Path-2 candidate 边界

PR-E2 产物默认是 `ref model 候选`，不是 signed reference model。尤其是 Path-2 能源管理、医疗设备这类复杂论文，若只覆盖主链、抽象时间、或把连续时间条件事件化，必须写明：

- 覆盖了哪些状态/转移/输出；
- 没覆盖哪些子链、优先级、异常或连续控制语义；
- 是否 `main_result_eligible` 只作为候选观察而非正式主结果；
- 后续人工签核前需要补哪些证据。

### 4.4 不可达/非法状态

论文中的 illegal / invalid / fallback 状态可能被设计为“理论上不应进入，但必须有恢复边”。这类状态不应简单删除。推荐在 PR comment 中说明：

- 它是 paper-defined abnormal state 还是模型误造的 dead state；
- 是否有显式恢复边；
- 若 SD-4 报 `W_UNREACHABLE_STATE`，该 warning 是合理提示还是需要 policy waiver / scenario 覆盖。

## 5. 每轮修改后的四例闭环协议

PR-E2 的验收对象不是“skill 文档看起来合理”，而是“skill 能驱动 Codex/Claude 类 agent 产出足以作为 Path1/Path2 ref-model 蓝本的模型”。因此每轮迭代必须按以下顺序闭环：

```text
修改 skill / 上游 grammar prompt 硬伤
-> push
-> 4 个样本重新由 Codex 调用 skill 生成真实 ref-model 候选
-> 每个样本各自 new PR comment 留痕
-> 3 reviewer 同时 review 当前 skill + 4 个生成结果
-> reviewer 可对 skill 与模型质量提出 C/I/M
-> 修复 C/I，尽量吸收不拖进度的 M
-> 再次 4 样本真实生成
```

reviewer 的 review 范畴包括：

| 范畴 | 需要判断的问题 | 可给 C/I 的情形 |
|---|---|---|
| skill 全流程可用性 | agent 能否独立发现输入、工具、prompt、stage、repair、report 规则 | skill 会系统性误导 agent 或证据无法复现 |
| 语法/工具一致性 | grammar digest、SD tools、pyfcstm runtime 是否一致 | 文档要求的 DSL 会被实际 parser/semantic 拒绝 |
| ref model 学术质量 | 状态/变量/guard/action 是否忠实覆盖 NL/论文证据 | 模型缺失核心状态链、关键 guard/action，或抽象导致 Path1/Path2 结论不可靠 |
| scenario / sim oracle | 是否至少覆盖关键 nominal/abnormal/edge 转移 | 未仿真关键行为却声称 ready |
| fake/real 边界 | 是否绕过 skill、调用顶层 runtime、或把 hot-start/replay 冒充主结果 | 证据污染 PR-E2 主结论 |

只有当三路 reviewer 均确认 `C: 无 / I: 无`，且最新一轮 4 个样本的 ref-model 候选达到“可作为后续 Path1/Path2 ref model 蓝本”的质量，PR-E2 才能进入 ready-to-merge。

## 6. PR comment 记录模板

建议每个样本按下列结构写 PR comment；若模型过长，仍应保留最终候选模型全文或可审查摘录，并给出最小复现命令。

````markdown
## PR-E2 样本实测：<样本编号> <case_id>

- 身份：<codex/claude/...> skill-driven e2e producer
- Path 类别：Path-1 / Path-2
- 论文子路径：`project_1_llm_state_machine_modeling/sources/<case>/`
- NL 来源：`...`
- skill 入口：`agent_loop_skill/SKILL.md` 或 `agent_loop_skill/CLAUDE.md`
- 禁止调用检查：未调用 `method.loop.run_agent_loop(...)` / 未调用一键 runner

### 读取材料

| 类型 | 路径 | 用途 |
|---|---|---|
| skill | `...` | ... |
| paper | `...` | ... |

### 输入 NL 原文

```text
...
```

### 输入 NL 中文翻译 / 中文释义

```text
...
```

### Grounding 摘要

| 元素 | 证据 | 说明 |
|---|---|---|
| state/action/guard | `...` | ... |

### 最终候选模型

```fcstm
...
```

### 全流程真实摘要表

| Stage | 是否 LLM | 轮次 | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/命令 |
|---|---:|---:|---|---|---|---|---|
| E0/Skill discovery | 否 | - | ✅/❌ | ... | ... | 无 | `...` |
| E1/Grounding | 是/否 | 0 | ✅/❌ | ... | ... | 无/有 | `...` |
| E2/Modeling | 是 | 0 | ✅/❌ | ... | 生成 initial DSL | 生成 DSL | `...` |
| SD-2/3/4/6 | 否 | 0 | ✅/❌ | ... | 本地检查 | 无 | `...` |
| Repair/Review | 是/否 | 1 | ✅/❌ | ... | 修复/评审 | ... | `...` |

### 检查与修复轨迹

| 轮次 | 动作 | 反馈 | 修复 |
|---|---|---|---|
| 0 | initial candidate | ... | ... |

### ref model 学术评审

| 维度 | 结论 | 问题/证据 |
|---|---|---|
| NL fidelity | ... | ... |
| 状态/变量/guard/action 覆盖 | ... | ... |
| scenario/sim 覆盖 | ... | ... |
| main_result_eligible | true/false | ... |
| 人工签核前待补 | ... | ... |

### 最终判断

- 状态：可用 / 部分可用 / 不可用
- 主要质量问题：...
- skill 改进建议：...
````

## 7. 常见误用与分级

| 误用 | 影响 | review 等级 |
|---|---|---|
| 调用 `method.loop.run_agent_loop(...)` 产出模型 | 不是 PR-E2 skill evidence | C |
| 未读取 skill，只凭 issue comment 工作 | 无法证明 repo-local skill 可用 | I |
| 未读取论文路径或 NL 来源不清 | ref-model grounding 不可信 | I |
| 不运行任何 parse/semantic/design/sim/review 检查 | 质量证据不足 | I |
| 只给摘要不给候选模型 | 无法审计 | I |
| comment 缺少局部命令或关键输出 | 可复现性弱 | I/M，视影响而定 |
| 文案不够美观但证据完整 | 不影响学术目标 | M |
```
