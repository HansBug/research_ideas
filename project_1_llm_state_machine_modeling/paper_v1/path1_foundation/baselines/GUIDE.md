# Path-1 S1a Baseline 专项工作指南

本指南约束 [`README.md`](./README.md)、[`SUMMARY.md`](./SUMMARY.md) 与 [`papers/`](./papers/) 的后续维护。S1a 是 Path-1 第一篇论文 novelty、baseline fairness、Related Work 定位和实验路线冻结的事实底座；任何更新都必须按高风险学术审计任务处理。

## 1. 目标与边界

### 1.1 目标

1. 对九个五绿 direct baseline 形成可追溯的事实吸收。
2. 明确每篇 prior work 的输入、任务、方法、LLM 模型、输出 STM 类型、人在回路、流程内反馈、事后评测、artifact 和可复现路径。
3. 为 S1b competitor matrix 与 S3 executable / approximate baseline 设计提供事实依据。
4. 防止 Path-1 第一篇论文出现会被 reviewer 直接打穿的 novelty claim。

### 1.2 非目标

1. 不替代 [`../../../baselines/`](../../../baselines/) 原始 baseline corpus。
2. 不写最终 Related Work 成稿。
3. 不把不可复现、私有数据或 artifact 缺失写成 prior work 的学术弱点；这些只作为 comparability / reproduction blocker。
4. 不把 post-hoc evaluation 写成 LLM 生成流程内 feedback。

## 2. 阅读与更新顺序

维护本目录时默认顺序如下：

1. 先读 [`README.md`](./README.md)，确认目录定位和关键口径。
2. 再读本 [`GUIDE.md`](./GUIDE.md)，确认字段合同和验收标准。
3. 再读 [`SUMMARY.md`](./SUMMARY.md)，把握总账和风险。
4. 对目标论文，按原始目录中的 `bibtex.bib -> paper_content.txt -> DESC.md -> ASSETS.md` 顺序核验。
5. 更新对应 [`papers/*.md`](./papers/) 后，回填 [`SUMMARY.md`](./SUMMARY.md)。
6. 如果更新影响 S1b/S3，应同步检查 [`../evidence/baseline_and_related_work_matrix.md`](../evidence/baseline_and_related_work_matrix.md)、[`../experiment_design/execution_plan.md`](../experiment_design/execution_plan.md) 与 [`../story/paper_outline.md`](../story/paper_outline.md)。

## 3. 单篇文件字段合同

每个 [`papers/*.md`](./papers/) 默认必须包含以下章节：

1. `## 0. 元信息与 source pointer`
2. `## 1. 阅读审计`
3. `## 2. 表 A：方法框架与任务定位`
4. `## 3. 表 B：资产状态与可复现性`
5. `## 4. 表 C：生成流程内反馈`
6. `## 5. 表 D：事后评测、指标与证据强度`
7. `## 6. 表 E：同样本近似与可比性决策`
8. `## 7. 表 F：Claim 风险与 handoff`
9. `## 8. 待补与风险`

关键判断必须包含 source pointer。若 source pointer 只能指向既有 `DESC.md` 或 `ASSETS.md`，必须说明原文证据是否已核验；不得用派生文件替代全文依据。

## 4. 六类表格口径

### 4.1 表 A：方法框架与任务定位

必须覆盖：输入 NL 类型、任务目标、agent / prompt 模式、LLM 模型四元组、输出 STM 类型与能力、人在回路角色、输出后人工改动。

`agent / prompt 模式` 可多选，但必须附解释，例如 `single-shot`、`few-shot`、`prompt chaining`、`RAG`、`fine-tuning`、`tool-feedback loop`、`ensemble`。

`输出 STM 类型` 不能只写 UML / Mermaid / Umple / SysML 名称，必须说明其语义能力、可执行性、guard/action/hierarchy/time/concurrency 支持和与本项目 `pyfcstm` schema 的差距。

### 4.2 表 B：资产状态与可复现性

必须区分：公开数据、论文内可重建、仅专家评审、作者私有、未见公开证据、本地已冻结资产、本地 reproduction smoke。

不可复现只写成 comparability / artifact blocker；不得写成 prior work 的方法弱点。

### 4.3 表 C：生成流程内反馈

只统计会影响 LLM 生成、抽取、修复或再生成的反馈。以下内容默认不算流程内 feedback：

1. GT F1、precision、recall、METEOR、CodeBLEU、Pass@K。
2. 专家评分、SME comments、Likert、Wilcoxon 等事后评测。
3. 生成后人工核对且没有再注入 LLM 的判断。
4. 工具背景能力，除非论文明确将其输出反馈给 LLM。

### 4.4 表 D：事后评测、指标与证据强度

必须说明 GT / reference 来源、公开性、指标性质和证据强度。不要把指标高低直接解释成可作为同样本 baseline，除非输入、输出、模型预算、人力预算和 feedback budget 均可对齐。

### 4.5 表 E：同样本近似与可比性决策

必须把决策写成互斥口径之一：

1. `external same-sample approximate candidate`
2. `Path-1 main-sample approximate candidate`
3. `near / component comparison`
4. `evidence-only`
5. `not eligible`

如果输入来自模型反向补写、私有工业需求、协议长规格、小样本 prompt demo 或人工重构数据，必须写纳入 / 排除标记。

### 4.6 表 F：Claim 风险与 handoff

必须回答：

1. 哪些 `first` / `novel` / `automatic` / `agentic` / `tool-feedback` claim 会被 prior work 打穿。
2. 哪些弱化表述仍可保留。
3. S1b 应如何引用或分组。
4. S3 是否需要 executable baseline、approximate baseline、component baseline 或只作为 evidence-only。
5. 风险等级是 C / I / M 中哪一种。

## 5. 关键红线

1. `llms_emp`：作者使用过 model-checking rules / formal verification wording 时，本文引用必须落到 rule-based checking feedback；不得写成完整模型检查、counterexample trace 或可执行仿真反馈。
2. `ttool-ai`：TTool 的 verification / simulation 是工具背景能力；只有论文明确进入 LLM generation loop 的 JSON / syntax / constraints 才算流程内 feedback。
3. `designing-fsm`：已有 trace / oracle / repair feedback 和 SAT-based fault-model mining；Path-1 不能写“首次 trace/repair feedback”。
4. `structure/event SMF`：已有非结构化 NL 到 UML state machine 的 prompt-framework baseline；Path-1 不能写“首次 NL 到 UML/state machine 生成”。
5. `req`：已有汽车 NL requirements 到 statechart + fine-tuning + expert evaluation；私有数据只影响可比性，不削弱其 related-work 地位。
6. `umple`：本地 NuSMV / Alloy smoke 是本仓库 reproduction 资产，不是原 thesis 的 Llama3/RAG/pass@k 复现。

## 6. Review Gate

PR review 必须执行以下检查：

1. reviewer 至少核验目标论文的 `paper_content.txt` 关键章节；不能只读本目录摘要。
2. `structure/event SMF`、`llms_emp`、`ttool-ai`、`designing-fsm` 是 mandatory closest works，reviewer 必须全文核验方法、评测、威胁和结论。
3. `req`、`umple` 至少核验方法、结果、资产边界和人在回路章节。
4. reviewer 必须检查 source pointer 是否支撑结论；事实错误、source pointer 不支撑、反馈类型混淆、formal verification 误写、prior capability 弱化或夸大，均可给 C/I。
5. 本 PR / 本目录不需要运行四个 agent-loop 例子；这是文档与学术事实盘点任务。

## 7. 本地检查命令

建议每轮提交前运行：

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import re
root = Path('project_1_llm_state_machine_modeling/paper_v1/path1_foundation')
for p in root.rglob('*.md'):
    text = p.read_text()
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        target = m.group(2)
        if target.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        path = target.split('#', 1)[0]
        if not path or '*' in path:
            continue
        if not (p.parent / path).resolve().exists():
            print(f'MISSING {p}:{text[:m.start()].count(chr(10)) + 1}: {target}')
PY
grep -R -E "baseline[_-]?refresh[_-]?report" -n project_1_llm_state_machine_modeling/paper_v1/path1_foundation || true
```
