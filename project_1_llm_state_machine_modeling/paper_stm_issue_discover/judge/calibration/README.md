# Judge 校准工作区（v3.4 起；当前 v3.9 / prompt v13）

本目录服务于一个明确而有限的目标：让 issue #195 语义 Judge 的 K/N/I 划分（尤其是 N 与 I 的边界）在**趋势上**与 paper1 当前的人工终态一致，使它能作为后续消融或补充实验的**初筛**，再由人工逐条确认。论文对外口径不变：validity、relation、D/A、K/N/I 由人工完成；Judge 只是缩小人工改判量的工具，不是结果的事实源，也不改动任何已冻结数据。

## 为什么要校准

实跑冻结结果的 Judge 版本是 v3.2（提交 `05cf0da6f`）。与人工终态逐条对齐后，current 的 1271 条里 246 条被人工改判（444 条 N 中 204 条改 I：110 条 D0、93 条 NOT_A_DEFECT_CLAIM），baseline 的 512 条里 147 条改判且双向都错（134 条 N 中 68 条改 I；102 条 I 中 75 条改回有效）。三条根因：v3.2 的最低举证门只测「可审计」而不测「有被违反义务」；事实校验以 typed / lowered 表示为准而不是作者源；把 reason 里的解释性错误当成 INDISPENSABLE_MECHANISM 一票否决。08-29 的 v3.3 只在 gate 描述里加了「D0/A0 → REFUTED」，从未实跑，且保留了「非执行载体不满足义务」的段落。

## v3.4 改了什么

1. **作者源基准**：承重事实只看 NL 与作者 PlantUML 原文；FCSTM、typed carrier、投影、分析状态只能佐证，不能建立或反驳作者源事实。作者在 transition label 上写的自由文本条件视为作者已表达。
2. **显式 D/A 输出**：validity 响应新增 `defect_adjudication.defect_class ∈ {D2, D1, D0, A0_FALSE_POSITIVE, A0_NOT_A_DEFECT_CLAIM}`，后端由它确定性派生 minimum-evidence gate（D2/D1 满足，其余否决），并把 `defect_class / d_tier / a0_subtype` 写进 `report_outcomes`，与人工 v4 决策表同构。两次读数的 defect_class 不一致会触发仲裁。
3. **收窄 INDISPENSABLE_MECHANISM**：只有「去掉它结论就不成立」的前提才算；解释性错误进 auxiliary warning。
4. **载体纪律写成通用原则**：NL 称 signal/event/trigger 且作者作 trigger 承载 → D0；NL 给布尔条件、作者只用 label 文本承载 → D1；只在 typed/投影槽位上为空 → A0_NOT_A_DEFECT_CLAIM；作者源含该元素却称缺失 → A0_FALSE_POSITIVE。提示词中不出现 pair 编号、台账 ID 或臂名称，由测试钉住。
5. **schema 级一致性**：D2/D1 与被反驳的 CORE_CLAIM / INDISPENSABLE_MECHANISM clause 互斥；A0_FALSE_POSITIVE 必须有被反驳的硬 clause。校验失败由运行时带错误信息原地重试。
6. **`--report-filter`**：CLI 新增本地 allowlist，只判定被选中的已发布报告，匿名 ID 与 ID 映射不变；manifest 记录 allowlist 路径与哈希。

## 文件

| 路径 | 作用 |
| :-- | :-- |
| [scripts/build_calibration_subset.py](./scripts/build_calibration_subset.py) | 从冻结归档按分层抽 301 条（current 201 / baseline 100），产出 allowlist 与 gold 表；只读、标准库、固定 seed |
| [scripts/compare_calibration_run.py](./scripts/compare_calibration_run.py) | 把一次 Judge 运行与 gold 逐条对齐，输出矩阵、分层一致率、方向偏差与逐条分歧（含 Judge 的 reason / basis） |
| [subset_v1/](./subset_v1/) | `report_filter_current.json`、`report_filter_baseline.json`、`gold_v1.tsv`、`summary.md` |
| [preregistered.md](./preregistered.md) | 运行前登记的验收判据与迭代政策 |
| [results/](./results/) | 每次迭代一个目录（`iterN_<版本>_<提交>`），含 README（判据对照、红旗、分歧模式、下一轮调整）与两侧的 `summary.md`、`disagreements.md`、`all_rows.tsv`；原始 LLM 制品在被忽略的 `runs/` 下 |

## 运行

从仓库根执行，每一侧每一轮一次调用（六次）。运行前必须 commit：CLI 拒绝在有未提交改动的树上做真实调用。**并发纪律（第八轮事故后）**：同时处理的 pair 控制在 14 左右（每个 pair 的两次读数并行，在途请求约为 pair 数的两倍；current 8 个 worker + baseline 6 个，或四路各 4 / 3），多轮多臂串行或按通路补跑，不要同时启动十几条 CLI——42 个 pair 并发时单次调用从 60 s 涨到 120 s 以上、触发 300 s 超时耗尽预留而整格失败，降回 14 后出格速度反升三倍。CLI 拒绝写入已存在的 run 目录，补跑缺失格用 `--pair-id` 加新的 run-id（如 `current-r2-resume`），对比脚本接受多个 `--run-dir`。启动前用 `ps -eo pid,ppid,etime,args | grep spawn_main` 清理孤儿 worker；停进程按 pid 杀，`pkill -f` 的模式若含在自己的命令行里会把自己杀掉。最新 result.json 停滞超过 10 分钟而进程存活，多半是网关挂住了流式请求，用一条最小探针确认后重启。

```bash
P1=project_1_llm_state_machine_modeling/paper_stm_issue_discover
FR=$P1/final_results/v60_current_vs_x1v2_baseline
export PYTHONPATH=$P1/judge/src:.
for r in 1 2 3; do
  venv/bin/python -m paper_stm_judge.cli --allow-live --profile gpt-5.6-luna --round $r \
    --source-format evidence_discovery_release --source-root $FR/raw/v60_current/method \
    --report-root $P1/pipeline/representation/reports/llms_emp_r45_java_60 \
    --ledger $P1/discover_matrix/ledger_v2/ledger.json \
    --report-filter $P1/judge/calibration/subset_v1/report_filter_current.json \
    --output-dir runs/paper1/judge-calibration-<tag> --run-id current-r$r
  venv/bin/python -m paper_stm_judge.cli --allow-live --profile gpt-5.6-luna --round $r \
    --source-format x1v2_record --source-root $FR/raw/x1v2_baseline/method/run$r \
    --report-root $P1/pipeline/representation/reports/llms_emp_r45_java_60 \
    --ledger $P1/discover_matrix/ledger_v2/ledger.json \
    --report-filter $P1/judge/calibration/subset_v1/report_filter_baseline.json \
    --output-dir runs/paper1/judge-calibration-<tag> --run-id baseline-r$r
done
python3 $P1/judge/calibration/scripts/compare_calibration_run.py --side current --gold $P1/judge/calibration/subset_v1/gold_v1.tsv \
  --run-dir runs/paper1/judge-calibration-<tag>/current-r1 --run-dir runs/paper1/judge-calibration-<tag>/current-r2 --run-dir runs/paper1/judge-calibration-<tag>/current-r3 \
  --out $P1/judge/calibration/results/<tag>/current
```

## 现状（2026-09-03，七轮之后）

七轮迭代（逐轮说明见 [results/](./results/)，跨轮表见 [results/iterations_summary.md](./results/iterations_summary.md)）。第六轮的 relation-first 闭合把两侧 K→K 层抬到 86–88%，按冻结全量加权后新 judge 与 gold 的一致率 current 80.3%、baseline 72.6%，追平 / 超过冻结 judge 的 80.6% / 71.3%（[scripts/population_weighted.py](./scripts/population_weighted.py)）。第七轮的 prompt v12 把 current 的 +20 pp 过度有效化修成了 −5 pp 过度无效化，全量加权回退到 61.9% / 64.2%，K→K 层跌到 68–73%；逐条读 reason 归因到六个来源，落为 prompt v13。第八轮起同一提示词跑双臂：A 臂沿用全部闭包（质量参照），B 臂只展示作者源闭包并收窄仲裁触发（效率），效率合格线与采纳条件见 [preregistered.md](./preregistered.md)。事前登记的 85% 子集门槛仍未达到：同一提示词两次采样的自洽度 79–83%，gold 在 D0↔D1 边界上自身不一致且两侧宽严不同（同一类报告 current 判 D0、baseline 判 D1 / D2）。判据本身未改。

## 边界

不重跑 v60 / X1v2 的全量结果，不改 `final_results/`、`method/`、`evaluation/`、台账或协议快照；gold 只用于校验 Judge 的趋势，不反向写回任何冻结数据。baseline 的 279 条冻结 K 未经 v3 重审，比对时只当「K 不能丢」的下界。
