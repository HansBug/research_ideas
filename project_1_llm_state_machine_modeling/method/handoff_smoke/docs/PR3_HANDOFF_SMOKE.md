# PR-3 Path1/Path2 agent-loop handoff smoke

本目录是 issue #14 的 PR-3 收官交付：证明已合并的 agent-loop 基础设施可以被 Path 1 / Path 2 后续工作接入，并且每次 representative smoke 都能写出 schema-valid、可单文件复盘的 `AgentLoopRunRecord`。

## 边界声明

- 本 smoke 是 **infrastructure compatibility / handoff**，不是 Path 1 / Path 2 正式实验。
- 不计算 Path 1 的 5-component P/R/F1。
- 不计算 Path 2 的 feature utilization、per-C-axis lift 或 Loop-* ablation。
- 正式指标、paper-facing report 和大规模样本运行应在 Path 1 / Path 2 后续 issue / PR 中完成。

## 代表性输入

| 路径 | 配置 | 上游数据来源 | 本 PR 检查点 |
|---|---|---|---|
| Path 1 | [`../configs/path1_representative.json`](../configs/path1_representative.json) | PR #13 Path 1 snapshot `sources_path1.parquet` + CARA signed reference DSL / `ref_components.json` | signed-reference 风格 case 可进入完整 loop；保留 snapshot/case provenance；不算 F1 |
| Path 2 | [`../configs/path2_representative.json`](../configs/path2_representative.json) | PR #13 Path 2 snapshot `sources_path2.parquet` + `008.fcstm` draft | intrinsic-style representative case 可进入完整 loop；保留 bucket/source provenance；不算 Path2 指标 |

两个配置都通过 `git show <snapshot>:<path>` 读取上游固定 snapshot，避免把 Path1/Path2 正式数据全集复制进 PR-3。

## 本地运行

在仓库根目录运行：

```bash
source .env
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m method.handoff_smoke.runner \
  --real-llm \
  --out runs/pr3_handoff_smoke \
  --summary runs/pr3_handoff_smoke/summary.json \
  --max-retries 2
```

说明：

1. 代码不直接读取 `.env` 文件；必须由 shell `source .env` 把 `LLM_ENDPOINT`、`LLM_API_KEY`、`LLM_MODEL` 注入环境变量。
2. `--real-llm` 会在 `SL-7 Lightweight Model Review` 阶段直接调用 `.env` 指定的 OpenAI-compatible provider，并把 prompt、raw output、parsed output、usage、provider/model metadata 写入 run record。
3. LLM stage 允许 bounded retry：provider/network error、JSON/schema-invalid output 默认最多重试 `2` 次；每次 attempt 的 `status`、raw output hash、usage、error、parsed output 都进入 `llm_interactions[*].attempts`，最终 `ReviewRunMeta.retry_count` / summary `llm_review_retry_count` 记录实际重试次数。
4. Retry 只处理低概率外部抖动或格式失败；超过上限仍为 schema-invalid/provider failure，run record 会被标为 `invalid`，不得进入 Path1/Path2 主结果。
5. API key / token 不会进入 run record；如 NL、path context、prompt、response 或日志中出现疑似 secret，会被脱敏并写入 `redaction_report`。
6. 若只想跑离线结构 smoke，可去掉 `--real-llm`；此时 `SL-7` 使用 fake replay，不作为 PR-3 真实 LLM 验收证据。

## 产物解释

每个代表性 case 产出：

```text
runs/pr3_handoff_smoke/<run_id>.agent_loop.json.gz
```

单文件内至少可复盘：

- 输入 NL、Path1/Path2 snapshot commit、case id、source metadata；
- stage DAG 与实际执行顺序；
- parse / semantic / design / scenario freeze / sim / SL-7 review stage record；
- `SL-7` prompt、raw output、parsed output、provider/model、usage、schema validation、retry count 与每次 attempt；
- deterministic feedback、scenario history、final DSL hash、eligibility filter；
- redaction report 与 replay index。

Path 1 / Path 2 后续主结果统计只应纳入：

```text
record.status == "success" and record.final_artifacts["main_result_eligible"] == true
```

schema-invalid、provider failure、invalid LLM output、replay miss 或被标记为 `invalid` 的 run 不得进入主结果。

## 下游交接建议

### Path 1

Path 1 merge main 后，建议先复用本 runner 验证自己的 selected cases：

1. 将 `path1_representative.json` 的 `source_snapshot` 改成当前 Path 1 branch 的数据 commit / artifact path；
2. 保留 `ref_components_path`，额外检查 signed reference row-wise compatibility；
3. smoke 通过后再进入正式 5-component eval pipeline。

### Path 2

Path 2 merge main 后，建议先复用本 runner 验证 representative buckets：

1. 将 `path2_representative.json` 的 `source_snapshot` 改成当前 Path 2 branch 的 selection/parquet/draft artifact；
2. 至少覆盖一个 `FSM-basic`、一个 `EFSM-interlock`、一个 `HSM-layered`；
3. smoke 通过后再计算 feature utilization / per-C-axis lift / Loop-* ablation。
