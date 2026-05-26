# `eval/` — Path 1 评测基础设施

LLM-初审 + 人类签字 的 5-component manual-eval pipeline，用于 paper §Evaluation 的 component-level P/R/F1。

## 数据范围

- 5 类 component：`states / transitions / guards / actions / hierarchical_states`
- 不评 `parallel_regions` / `history_states`（pyfcstm 形式上不支持，paper 不主张覆盖）
- 数据来源：`project_1_llm_state_machine_modeling/sources/` T0+🟢 子集，人工小规模评测集

## 工作流（5 阶段）

```
┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐
│ 1.选样   │→ │ 2.建 ref │→ │ 3.跑预测   │→ │ 4.标注   │→ │ 5.汇总   │
│sources/  │  │手工/LLM  │  │A0_baseline │  │claude+   │  │P/R/F1    │
│T0🟢分层  │  │+ 你签字  │  │A_full_ours │  │codex 提案│  │macro F1  │
└──────────┘  └──────────┘  └────────────┘  └──────────┘  └──────────┘
                                                  ↓
                                          中文 markdown
                                          评审包（你签字）
```

### 一致性自动预勾选

每行评审：
- ✅ **claude + codex 完全一致** → 自动勾选 `[x] 采纳 Claude`，你不用看
- 🔴 **两边不一致** → 留空 + heading 🔴 `需复议`，请你亲自判
- 🟡 **仅一方有提案** → heading 🟡 `单票`
- 🔴 **两方都没提案** → heading 🔴 `双方未提案`

详见 [PROTOCOL.md](./PROTOCOL.md)。

## 目录结构

```
eval/
├── PROTOCOL.md                  # 协议（中文，paper-claim + 评审规则）
├── README.md                    # 本文件
├── extract/                     # 5-component IR extractor
│   ├── schema.py
│   ├── umple.py                 # Umple → IR
│   └── pyfcstm.py               # pyfcstm DSL → IR
├── annotate/                    # 两个 annotator + orchestrator
│   ├── prompts/annotate.txt     # paper §IV 协议提示
│   ├── claude.py                # subprocess `claude` CLI
│   ├── codex.py                 # subprocess `codex` CLI
│   └── orchestrate.py           # 并跑两个，存 raw JSON
├── review/
│   ├── render.py                # JSON → 中文 markdown 包
│   ├── load.py                  # markdown → parquet
│   ├── raw/                     # 两个 annotator 的原始 JSON
│   ├── packs/                   # 中文评审包（你签字这里）
│   └── loaded/reviewed.parquet  # 解析后的统一表
├── aggregate.py                 # parquet → P/R/F1 + macro
├── results/                     # detail / macro / overall + summary.csv
├── data/
│   ├── sources/<case>/nl.md     # NL 来源（拷自 sources/）
│   ├── refs/<case>/             # ref_components.json + ref_model.txt（你签字）
│   └── preds/<case>/            # pred_*.json + pred_*_model.txt（baseline/ours 输出）
└── demo/
    ├── run_demo.py              # 阶段 3+4：跑 annotation + 渲染评审包
    └── finalize_after_signoff.py  # 阶段 5：parquet + 算 metric
```

## 演习（已跑通）

2 cases × 2 conditions × `states` × 2 annotators = 8 LLM calls，~2 min wall-clock：

| case | condition | TP | FP | FN | F1 |
|---|---|---|---|---|---|
| automatic-elevator-controller | pred_perfect | 7 | 0 | 0 | 1.00 |
| automatic-elevator-controller | pred_buggy | 6 | 1 | 1 | 0.857 |
| abs-fsm-brake-control | pred_perfect | 3 | 0 | 0 | 1.00 |
| abs-fsm-brake-control | pred_buggy | 3 | 1 | 0 | 0.857 |

两个 annotator 在全 22 行上完全一致 → 22/22 auto-marked ✅。

## 跑演习

```bash
source ../../.env             # 加载 CLAUDE_CMD / CLAUDE_MODEL / CODEX_CMD / CODEX_MODEL
cd project_1_llm_state_machine_modeling
PYTHONPATH=. python eval/demo/run_demo.py

# 你打开 eval/review/packs/<case>/<cond>/states.md 签字，然后：
PYTHONPATH=. python eval/demo/finalize_after_signoff.py

# 结果：eval/results/summary.csv
```

## .env 依赖

```bash
export CLAUDE_CMD=claude
export CLAUDE_MODEL=claude-opus-4-7
export CODEX_CMD=codex
export CODEX_MODEL=gpt-5.5
```

`source .env` 后跑 demo 即可。代码不直接读 `.env` 文件，只读 `os.environ`。
