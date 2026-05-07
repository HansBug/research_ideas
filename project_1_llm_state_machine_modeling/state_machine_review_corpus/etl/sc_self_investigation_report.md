# SC Median-Aggregation Pipeline 自查报告

> 触发：用户在 [PR #6 issue-comment-thread](https://github.com/HansBug/research_ideas/pull/6) 提出"为什么 SC 多次运行结果一致但 median 聚合后某些指标严重下滑？这是不是说明 W1.5 baseline 只是个偶然结果？"
>
> 时间：2026-05-07
> 关联 commit：`ca2aeff9`（patch 前）→ patch 后（本报告）

## 一、问题陈述

W2 Q3 self-consistency 在 62-task slice 实测：

| 指标 | W1.5 baseline (单跑) | rerun_0 (T=0+V1) | rerun_1 (T=0.3+V2) | rerun_2 (T=0.5+V3) | SC median 聚合 |
|---|---:|---:|---:|---:|---:|
| HAI | 81.76 | 83.55 | 83.60 | 83.66 | **79.88** |
| SAS | 69.21 | 71.16 | 71.16 | 71.37 | **62.16** |
| record_Calib | 90.20 | 79.94 | 70.82 | 70.82 | **45.35** |
| PDS | 100.00 | 100.00 | 100.00 | 100.00 | **85.00** |
| summary_EvDisc | 55.00 | 100.00 | 100.00 | 100.00 | **55.00** |

**核心矛盾**：3 个 rerun 个体的 HAI 高度一致（σ=0.05），且都比 W1.5 高 1.84；但 median 聚合后 HAI 反而塌到 79.88，比 W1.5 还低 1.88。**LLM 不在分歧 → median 聚合本身却造成大幅下滑** —— 这必然是 aggregation pipeline 本身的 bug 或设计缺陷。

## 二、调查方法

1. 提取 3 个 rerun 与 SC final 的全量指标对照
2. 提取 W1.5 baseline 同 slice 同 task 数据
3. 跨 rerun 计算每个 task 的 agent_score / dim_score / judgement 一致性
4. 根据数据回溯 SC aggregation 代码路径

## 三、根因（Root Cause）

**`_aggregate_runs` 的 confidence 公式 `clip(1 - α·max_dim_std, 0.10, 0.99)`（α=2）与 benchmark.py 已有的 confidence-阈值启发式不兼容**。

### 3.1 数据机制

Stage 1+3 实测：3 个 rerun 在 rubric+iter_b 锁定下高度一致：

- 62/62 个任务里 **55/62（88.7%）** agent_score 跨 3 rerun 完全相同（std<0.001）
- 跨 rerun max-dim-std 中位 = 0.0000，平均 = 0.0039
- 推论：`max_dim_std ≈ 0` → confidence 公式 → `1 - 2·0 = 1.0`，clip 到 **0.99**

### 3.2 公式与下游启发式的冲突

benchmark.py 中三处使用 confidence 阈值：

| 函数 | 代码（伪） | 阈值 | SC=0.99 时 |
|---|---|---:|:---:|
| `_summary_discipline_metrics`<br>(EvidenceDiscipline) | `self_awareness = (conf ≤ 0.70 ∧ ev ≥ 0.60)` | 0.70 | ✗ 永远 False |
| `_protocol_metrics`<br>(confidence_discipline → PDS) | `confidence_discipline = (conf ≤ 0.55)` | 0.55 | ✗ 永远 False |
| `_calibration_metrics`<br>(record_Calib) | 高置信度+错误判断 → 严重惩罚 | n/a | 大量 high-confidence 错误 |

### 3.3 量化级联

| 指标 | rerun (LLM 输出 conf≈0.21) | SC final (强制 conf=0.99) | 差异源 |
|---|---:|---:|---|
| EvidenceDiscipline | 0.55·(1−ECR) + 0.45·1.0 ≈ **100** | 0.55·(1−ECR) + 0.45·0.0 ≈ **55** | `self_awareness` 因 conf>0.70 全失败 |
| PDS | base + 0.20·1.0 = **100** | base + 0.20·0.0 = **80~85** | `confidence_discipline` 因 conf>0.55 全失败 |
| record_Calib | LLM 真实 conf 与正确率匹配 = **80** | 0.99 high conf + 错误判断 → **45** | 校准误差爆炸 |

代入 SAS 公式 `0.40·SA + 0.25·RankAlign + 0.20·EvDisc + 0.15·Stab`：
- EvDisc 100→55 → SAS 损失 0.20·(100-55) = **9.0pp**（与实测 71.16→62.16 = -9.0pp 完全吻合 ✓）

## 四、修复（Fix）

`reproduction/expert_review` 中已有的 confidence 阈值是与 LLM 自然 confidence 区间（≈0.21~0.50）契合的设计。SC 强行覆盖到 0.99 破坏这套设计。

**修复策略（最小变更）**：

```python
# Before (bug):
confidence = max(0.10, min(0.99, 1.0 - confidence_alpha * max_dim_std))

# After (fix):
median_confidence = statistics.median([r.confidence for r in runs])
sc_consistency_confidence = max(0.10, min(0.99, 1.0 - confidence_alpha * max_dim_std))
return {
    "confidence": median_confidence,                  # 写入 agent_confidence (downstream-compatible)
    "sc_consistency_confidence": sc_consistency_confidence,  # 辅助字段，留作分析
    ...
}
```

**实施位置**：
- `state_machine_review_corpus/etl/run_self_consistency_config.py::_aggregate_runs`
- `state_machine_review_corpus/etl/run_self_consistency_config.py::_recompute_aggregated_metrics`

## 五、修复前后对比

### 5.1 总指标（62-task）

| 指标 | W1.5 baseline | Q3 修复前 | Q3 修复后 | 修复后 ΔW1.5 |
|---|---:|---:|---:|---:|
| HAI | 81.76 | 79.88 | **83.60** | **+1.85 ✓** |
| RAS | 77.48 | 78.07 | **80.62** | **+3.14 ✓** |
| SAS | 69.21 | 62.16 | **71.16** | **+1.95 ✓** |
| record_ScoreAlign | 61.69 | 76.04 | 76.04 | +14.35 ✓ |
| record_Calib | 90.20 | 45.35 | **70.82** | -19.38 |
| summary_ScoreAlign | 63.75 | 53.95 | 53.95 | -9.80 |
| summary_RankAlign | 70.83 | 58.33 | 58.33 | -12.50 |
| summary_Spearman | 0.606 | 0.255 | 0.255 | -0.35 |
| summary_EvDisc | 55.00 | 55.00 | **100.00** | +45.00 ✓ |
| weighted_kappa | 0.618 | 0.695 | 0.695 | +0.077 ✓ |

### 5.2 Acceptance Gates（7 项）

| Gate | target | W1.5 | Q3 修复前 | Q3 修复后 |
|---|---:|:---:|:---:|:---:|
| HAI ≥ 85 | 85.0 | ✗ 81.76 | ✗ 79.88 | ✗ **83.60**（差 1.4）|
| record_ScoreAlign ≥ 65 | 65.0 | ✗ 61.69 | ✓ 76.04 | ✓ **76.04** |
| summary_ScoreAlign ≥ 60 | 60.0 | ✓ 63.75 | ✗ 53.95 | ✗ 53.95 |
| summary_RankAlign ≥ 70 | 70.0 | ✓ 70.83 | ✗ 58.33 | ✗ 58.33 |
| summary_Spearman ≥ 0.45 | 0.45 | ✓ 0.606 | ✗ 0.255 | ✗ 0.255 |
| weighted_kappa ≥ 0.65 | 0.65 | ✗ 0.618 | ✓ 0.695 | ✓ **0.695** |
| crit_issue_recall ≥ 0.90 | 0.90 | ✓ 0.99 | ✓ 0.99 | ✓ 0.99 |
| **小计** | | **4/7** | 4/7（trade-off）| **4/7（regime 偏移仍在）**|

## 六、修复完之后的真实结论

1. ✅ **Q3 SC 不是 trade-off，是 regime-偏移的 partial improvement**：HAI +1.85、kappa +0.08、record regime 显著强化
2. ⚠️ **但 summary regime 仍然显著弱化**：RankAlign −12.5 / Spearman −0.35 / SA −9.8
3. 🔬 **summary regime 弱化不是 SC median 的产物** — 在每个**单 rerun**（包括 rerun_0 = T=0+V1，名义上等价于 W1.5 baseline）里就已经存在
4. 🔬 这指向 **SC parallel pipeline (`_evaluate_task_bundle_parallel`) 与 standard pipeline (`_evaluate_task_bundle`) 之间的 post-LLM 评分链路存在差异**，或者 LLM API 在不同时间窗口的非确定性 — **此为待确认的下一阶段调查项**（用户决定暂时跳过）
5. 📊 修复后的 4/7 acceptance gates 仍不能直接判 W1.5 vs Q3 优劣 —— 通过的 gate 集合不同，需要先建立 baseline noise floor 才能判断

## 七、后续 TODO（已与用户对齐）

- [x] **修复 confidence formula** — 已落实（本 commit）
- [x] **重新聚合 4 个 SC report**（不重新调 LLM，从 checkpoint 重算）— `sc_reaggregate_from_checkpoints.py` 已落地
- [x] **重新生成 slim reports** + **重渲染 6 张图表**
- [x] **更新 PR comment + plan comment + checklist comment**
- [ ] ⏳ **rerun_0 vs W1.5 1.84 HAI gap 调查** — 用户暂时跳过，会在合适时机回填
- [ ] ⏳ **summary regime 弱化的根因分析**（SC parallel pipeline vs standard pipeline）— 同上

## 八、可追溯文件

| 类型 | 路径 |
|---|---|
| 修复后的 main code | `state_machine_review_corpus/etl/run_self_consistency_config.py`（`_aggregate_runs` + `_recompute_aggregated_metrics`）|
| 离线重聚合工具 | `state_machine_review_corpus/etl/sc_reaggregate_from_checkpoints.py` |
| 自查脚本 | `state_machine_review_corpus/etl/sc_self_investigation.py` |
| 自查数据快照 | `state_machine_review_corpus/etl/sc_self_investigation_data.json` |
| 修复后 SC reports | `state_machine_review_corpus/etl/out/phase14_combined/week2/report_q3_*.json`<br>（注：`out/` 是 gitignored，但通过 `git add -f` 与 checkpoint 一同存档）|
| Per-rerun checkpoints | `.../week2/checkpoints/week2_q3_q3_*_rerun{0,1,2}.json` |
