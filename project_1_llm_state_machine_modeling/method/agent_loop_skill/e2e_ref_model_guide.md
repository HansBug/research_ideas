# PR-E2 e2e ref-model skill 使用指南

本文件用于 PR-E2：让 Codex / Claude Code 类 agent 在**不调用顶层 agent-loop runtime** 的前提下，基于 repo-local skill / toolbox 自主完成“NL + 论文子路径 -> FCSTM/pyfcstm ref model 候选”的 e2e 建模、验证、修复和留痕。

## 1. 硬性边界

1. **禁止调用顶层 agent-loop runtime**：不得调用 `method.loop.run_agent_loop(...)`、PR-D representative runner 或任何一键 full staged runner。
2. **允许调用底层工具箱**：可以调用 `SD-*` deterministic tools、`SL-*` prompt generators、pyfcstm parse/build/inspect/sim utilities，以及仓库内只读论文材料。
3. **修改范围**：若需要改 skill，本 PR 只允许改 `project_1_llm_state_machine_modeling/method/agent_loop_skill/` 及其子路径。
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

如果任务要求严格按仓库论文阅读规范重新生成派生文件，则应按根级规范先读 `bibtex.bib` 再通读 `paper_content.txt`；PR-E2 的 ref-model 实测可以先利用现有 `STM.md` / `DESC.md` 作为人工整理过的线索，但必须说明是否回看了原文提取文本。

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

优先运行下列检查。若某个工具入口不可用，应记录不可用原因，不要静默跳过。

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
scenario = TestScenario(name="sanity", description="hot-start sanity", steps=[])
coverage, coverage_meta = run_sd5a_scenario_coverage(current_dsl, [scenario])
scenario_set, freeze_meta = freeze_scenario_set(
    [scenario],
    source_dsl=current_dsl,
    inspect_json=context.inspect_json or {},
    grounding_map=context.grounding_map,
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

每个样本最终必须能汇总成 PR comment，至少包含：

- 样本编号、Path 类别、NL 来源、论文路径；
- 使用的 agent / CLI / skill 入口；
- 实际读取文件；
- 禁止调用项检查结论；
- 最终模型候选；
- deterministic checks / review checks 结果；
- repair 轨迹；
- 最终状态与质量分类；
- skill 改进建议。

## 4. PR comment 记录模板

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

### Grounding 摘要

| 元素 | 证据 | 说明 |
|---|---|---|
| state/action/guard | `...` | ... |

### 最终候选模型

```fcstm
...
```

### 检查与修复轨迹

| 轮次 | 动作 | 反馈 | 修复 |
|---|---|---|---|
| 0 | initial candidate | ... | ... |

### 最终判断

- 状态：可用 / 部分可用 / 不可用
- 主要质量问题：...
- skill 改进建议：...
````

## 5. 常见误用与分级

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
