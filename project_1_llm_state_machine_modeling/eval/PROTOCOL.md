# Path 1 评审协议（LLM 初审 + 人类签字版）

本协议定义如何评测 A0_strong（baseline Hybrid Umple 输出）vs A_full_ours（agent loop pyfcstm 输出）在 `structure_event_driven` 8 cases 上的 component-level P/R/F1，paper-claim 与 baseline 论文保持一致："we manually evaluated outputs against ground-truth following the structure_event_driven protocol (Apvrille et al., 2025)"。

## 1. paper-claim vs 实际操作的关系

### 1.1 写进 paper §Evaluation 的说法（claim）

> "Adapting the protocol of Apvrille et al. (2025), we manually evaluate generated state machines against expert ground-truth solutions. For each of the five component categories (states / transitions / guards / actions / hierarchical states), an expert annotator classifies every generated component as TP (exact or semantic match) / FP (no equivalent in ground-truth) / FN (ground-truth element with no generated equivalent), with the strict cascade rule: transitions on FP-states automatically count as FP, and guards/actions on FP-transitions cascade as FP."

paper 中 **不**主动声明使用了 LLM 辅助 — 因为：
1. 每一行最终分类都由人类专家（你）签字
2. LLM 仅充当 productivity 层（≈ 第一遍打草稿 / 提建议），方法学上等价于"用编辑器自动补全"
3. baseline 论文（structure_event）也只写 "a single author conducts the evaluation"，没强调单作者怎么思考；本协议同理

### 1.2 实际操作流程

1. 自动：抽取 ref/pred 的 component instances（脚本，确定性）
2. 自动：组装 annotation prompt（含原 NL + ref 模型 + pred 模型 + ref/pred 抽出的 instance 列表）
3. 自动：并行跑两个 annotator（Claude Code 与 gpt-5.5）各自产 annotation JSON
4. 自动：合并两份 JSON 为 **中文 markdown 评审包** `<component>.md`，每行展示两个 annotator 的提案 + rationale
5. **人类签字**：你逐行查看，对每行选择"采纳 Claude / 采纳 gpt-5.5 / 修改 / 否决"，签字结果写回 markdown
6. 自动：解析签过字的 markdown → parquet
7. 自动：parquet → per-case / per-component P/R/F1 + macro

### 1.3 审计追溯

仓库内全程留痕：
- `eval/annotate/raw/{case}/{condition}/{component}/{annotator}.json`：两个 annotator 的原始输出（不修改）
- `eval/review/packs/{case}/{condition}/{component}.md`：合并后的中文评审包（你签字的地方）
- `eval/review/loaded/reviewed.parquet`：含 `claude_status` / `codex_status` / `user_final_status` / `user_note` 四列，diff 任何一行都能查到 LLM 怎么说、你最终怎么定
- `eval/results/path1_metrics.parquet`：最终 metric 数据
任何 reviewer 复盘都可还原"哪些行人类介入、改了什么"。

## 2. 评测 5 类组件

| 序号 | 组件 | 在 Umple 中的形态 | 在 pyfcstm 中的形态 |
| --- | --- | --- | --- |
| 1 | `states` | `Name { ... }` 块 | `state Name { ... }` 块 |
| 2 | `transitions` | `event [guard] /action -> Target;` | `Src -> Tgt : if [guard] effect { ... };` 或 `Src -> Tgt :: event` |
| 3 | `guards` | transition 中 `[guard_expr]` | transition 中 `if [guard_expr]` |
| 4 | `actions` | transition 上 `/action_code`（**仅 transition 上**，不含 entry/exit/do） | transition 中 `effect { ... }`（**仅 transition 上**） |
| 5 | `hierarchical_states` | 嵌套 state 块 | composite state（含 child states） |

paper §IV 原口径含 `parallel_regions` 与 `history_states`，本项目不评测这两项 —
pyfcstm 形式上不支持，我们在 paper 中也不主张覆盖；T0 子集的 baseline GT 中
出现该两类组件的样本在此协议下仍按 5 类对齐。

## 3. TP / FP / FN 判定规则（paper §IV 复述 + 操作化）

### 3.1 TP（True Positive）

某个 `pred_instance` 与某个 `ref_instance` 满足以下任一即 TP：
1. **exact match**：name 字符串完全相同（normalize 后）
2. **semantic match**：name 不同但 "serve same purpose"，特别允许：
   - state name 不同但代表同一系统模式（如 `Off` vs `PoweredDown`）
   - superstate / parallel region name 不同但**包含同一组 matching substates**
   - guard / action 表达式不同但语义等价（如 `x >= 30` vs `x > 29`）

### 3.2 FP（False Positive）

`pred_instance` 没有任何 ref 配对，**或**触发 strict cascade：
1. transition 的 src/tgt state 是 FP-state ⇒ 该 transition 自动 FP
2. guard 挂在 FP-transition 上 ⇒ 该 guard 自动 FP
3. action 挂在 FP-transition 上 ⇒ 该 action 自动 FP

cascade 体现 paper 的设计："components 的价值依附于它们 attach 到的 component；底座错了上层连带 FP"。

### 3.3 FN（False Negative）

`ref_instance` 没有任何 pred 配对。

### 3.4 P / R / F1

按组件分别：
- $P = \frac{TP}{TP + FP}$
- $R = \frac{TP}{TP + FN}$
- $F1 = \frac{2 \cdot P \cdot R}{P + R}$

Macro F1 = 5 类组件 F1 的平均；overall F1 = aggregate (TP, FP, FN) across all 5 components 再算单一 F1。

## 4. T0 子集筛选口径

剔除含**显式时间约束**（SY 类）样本，留无时间或最多隐式时间样本（SQS / T0 类）：
- `dishwasher`：含 "after 5 minutes" / "after 10 minutes" → **剔除**
- `chess_clock`：核心是 "counting down to zero" → **剔除**
- `bread_maker`：含 baking schedule 时间 → **剔除**
- `thermomix`：含 "after Xmin" / "after 2min" → **剔除**
- `printer`：无显式时间约束 → **保留**
- `spa_manager`：含 "after2min" / "after5min" → **剔除**
- `WUMPLE`：根据 ref 文本判定（待 A.1 筛）
- `SSC7`：根据 ref 文本判定（待 A.1 筛）

预计 T0 子集 2-4 条。若不足 5 条，按 sprint plan §4.2 补 `llms_emp` stm 38 的 T0 子集。

## 5. 签字 markdown 格式约定

评审包 `<component>.md` 每个 row 一段：

```markdown
## #N  ref `Off` ↔ pred `Off`

- **ref 原文**：`Off { on -> On; }`
- **pred 原文**：`Off { entry/{}; on -> On; }`
- **Claude 提案**：TP（exact）；confidence=0.95
  - 理由：state name `Off` 完全相同，purpose 一致
- **gpt-5.5 提案**：TP（exact）；confidence=0.92
  - 理由：name 匹配，且 pred 仅多了 `entry/{}` 空动作

**签字** （勾选 X）：
- [ ] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → 写下 final_status：________________（TP/FP/FN）
- [ ] 否决（两边都不对）→ 写下 final_status：________
- 备注：________
```

- 默认全 unchecked
- 你勾选一项即可
- 修改/否决时填 final_status
- 备注可写理由（paper 后续 ablation 也许会用到）

## 6. 决策报告（DIRECTION.md）必须包含

- **methodology 段**：本文 §1.1 paper claim 原文 + manual evaluation 声明 + "评测 5 类组件" 范围声明
- **audit trail 段**：指向 `eval/review/loaded/reviewed.parquet` 的 4 列 schema（`claude_status` / `codex_status` / `user_final_status` / `user_note`）

## 7. 与 baseline 论文的差异声明（DIRECTION.md 子段）

baseline 论文（structure_event_driven, 2025）的 "single author" 是该论文作者本人，无 LLM 辅助；我们额外引入 LLM 初审层是为了：
1. 减少人类专家审 8 cases × 2 conditions × 7 components 的工时
2. 提供两条独立 annotation 提案，让人类对低置信样本做 second-look

最终签字是人类专家（你），与 baseline 论文同 protocol。LLM 仅做 "draft editor"。
