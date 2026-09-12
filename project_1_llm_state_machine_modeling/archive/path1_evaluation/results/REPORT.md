# Path 1 评审结果 audit-trail 报告

生成时间：`2026-05-26 23:56:04`

本报告是 `full_annotations.parquet` 的 human-readable 浓缩版。每一项 P/R/F1 都可以反向追溯到具体的 `(case_id, condition, component_kind, row_id)` + 两 annotator 的 rationale + 你的签字行为。

## 1. 数据完成度

- **总行数**：67
- **已签字**：67
- **未签字**：0（>0 视为未完成评审）
- **自动预勾选（两边一致 ✅）**：61 行 — 这些行人工已默认采纳
- **需人工裁定的行**：6 行（含 🔴 / 🟡 单票 / 双方未提案）

## 2. 签字选择分布

| user_choice | 行数 | 占比 |
| --- | ---: | ---: |
| 采纳 Claude（`accept_claude`） | 63 | 94.0% |
| 采纳 gpt-5.5（`accept_codex`） | 4 | 6.0% |

## 3. 双 annotator 一致性分布

| agreement | 行数 | 占比 | 说明 |
| --- | ---: | ---: | --- |
| ✅ 一致 | 61 | 91.0% | 两边给同一 TP/FP/FN 标签，默认 ✅ 采纳 Claude |
| 🟡 仅 gpt-5.5 | 4 | 6.0% | 仅 gpt-5.5 给提案；可能 Claude 把这对解构成两条单边行 |
| 🟡 仅 Claude | 2 | 3.0% | 仅 Claude 给提案；可能 gpt-5.5 把这对解构成两条单边行 |

## 4. 最终 P/R/F1（基于 `user_final_status` 计算）

### 4.1 按 case × condition × component

| case_id | condition | component | TP | FP | FN | P | R | F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| abs-fsm-brake-control | pred_buggy | 守卫（`guards`） | 4 | 2 | 1 | 0.667 | 0.800 | **0.727** |
| abs-fsm-brake-control | pred_buggy | 状态（`states`） | 3 | 1 | 0 | 0.750 | 1.000 | **0.857** |
| abs-fsm-brake-control | pred_buggy | 迁移（`transitions`） | 4 | 2 | 1 | 0.667 | 0.800 | **0.727** |
| abs-fsm-brake-control | pred_perfect | 守卫（`guards`） | 4 | 0 | 0 | 1.000 | 1.000 | **1.000** |
| abs-fsm-brake-control | pred_perfect | 状态（`states`） | 3 | 0 | 0 | 1.000 | 1.000 | **1.000** |
| abs-fsm-brake-control | pred_perfect | 迁移（`transitions`） | 4 | 0 | 0 | 1.000 | 1.000 | **1.000** |
| automatic-elevator-controller | pred_buggy | 状态（`states`） | 6 | 1 | 1 | 0.857 | 0.857 | **0.857** |
| automatic-elevator-controller | pred_buggy | 迁移（`transitions`） | 9 | 1 | 2 | 0.900 | 0.818 | **0.857** |
| automatic-elevator-controller | pred_perfect | 状态（`states`） | 7 | 0 | 0 | 1.000 | 1.000 | **1.000** |
| automatic-elevator-controller | pred_perfect | 迁移（`transitions`） | 11 | 0 | 0 | 1.000 | 1.000 | **1.000** |

### 4.2 按 case × condition 的 macro F1（5-component 平均）

| case_id | condition | components_scored | macro F1 |
| --- | --- | ---: | ---: |
| abs-fsm-brake-control | pred_buggy | 3 | **0.771** |
| abs-fsm-brake-control | pred_perfect | 3 | **1.000** |
| automatic-elevator-controller | pred_buggy | 2 | **0.857** |
| automatic-elevator-controller | pred_perfect | 2 | **1.000** |

### 4.3 按 condition 的 overall F1（aggregate TP/FP/FN）

| condition | TP | FP | FN | P | R | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pred_buggy | 26 | 7 | 5 | 0.788 | 0.839 | **0.812** |
| pred_perfect | 29 | 0 | 0 | 1.000 | 1.000 | **1.000** |

## 5. 用户介入热点（auto_marked=False 的行）

共 6 行需要你亲自审核，签字分布如下：

| pack | row_id | agreement | claude→codex | user_choice | final | note |
| --- | --- | --- | --- | --- | --- | --- |
| `packs/abs-fsm-brake-control/pred_buggy/guards.md` | row001 | 🟡 仅 Claude | TP→— | 采纳 Claude | TP |  |
| `packs/abs-fsm-brake-control/pred_buggy/guards.md` | row005 | 🟡 仅 gpt-5.5 | —→FN | 采纳 gpt-5.5 | FN |  |
| `packs/abs-fsm-brake-control/pred_buggy/guards.md` | row006 | 🟡 仅 gpt-5.5 | —→FP | 采纳 gpt-5.5 | FP |  |
| `packs/abs-fsm-brake-control/pred_buggy/transitions.md` | row001 | 🟡 仅 Claude | TP→— | 采纳 Claude | TP |  |
| `packs/abs-fsm-brake-control/pred_buggy/transitions.md` | row005 | 🟡 仅 gpt-5.5 | —→FN | 采纳 gpt-5.5 | FN |  |
| `packs/abs-fsm-brake-control/pred_buggy/transitions.md` | row006 | 🟡 仅 gpt-5.5 | —→FP | 采纳 gpt-5.5 | FP |  |

## 6. 反向追溯字段说明 (`full_annotations.parquet` 列字典)

| 列 | 含义 |
| --- | --- |
| `case_id`, `condition`, `component_kind`, `row_id` | 行定位四元组 |
| `ref_id` / `ref_name` / `ref_text` | ref 实例 id + 名字 + 原文片段（指回 `data/refs/<case>/ref_components.json`）|
| `pred_id` / `pred_name` / `pred_text` | pred 实例 id + 名字 + 原文片段（指回 `data/preds/<case>/<condition>.json`）|
| `claude_status` / `claude_match_kind` / `claude_confidence` / `claude_rationale` | Claude annotator 完整提案 |
| `codex_status` / `codex_match_kind` / `codex_confidence` / `codex_rationale` | gpt-5.5 annotator 完整提案 |
| `agreement` | both_agree / disagree / claude_only / codex_only / neither |
| `auto_marked` | 该行是否被自动 ✅ 预勾选（两边完全一致才会 True） |
| `user_choice` | accept_claude / accept_codex / amend / reject / unsigned |
| `user_final_status` | 你最终签字的 TP / FP / FN（aggregate 唯一信源）|
| `user_note` | 你写的备注 |
| `pack_path` | 该行所在的中文 markdown 包路径 |
| `raw_claude_path` / `raw_codex_path` | 两个 annotator 的原始 JSON 全文路径 |

## 7. 审计追溯链

1. paper 写 "manually evaluated" → 证据来源是本表 `user_final_status` 列
2. 任何 reviewer 可对任一行追问 "为啥这条是 TP" → 直接打开 `pack_path` 看 ref/pred 原文 + 双 annotator rationale + 你的签字行
3. 任何对 metric 的复盘 → P/R/F1 公式见 §4，全部从 `user_final_status` 列重算可复现
