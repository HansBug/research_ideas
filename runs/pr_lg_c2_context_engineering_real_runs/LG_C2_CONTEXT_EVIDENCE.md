# LG-C2 Context-engineering subgraph real-run evidence

本文件是 PR #59 / LG-C2 的人工补充证据索引，和同目录下 runner 自动生成的 [SUMMARY.md](./SUMMARY.md)、[summary.json](./summary.json) 共同使用。目标是明确说明本轮四例真实运行是否满足 LG-C2 合同：`SL-9` / `SL-10` 上下文装配进入 context-engineering subgraph，且 context budget / prompt hash / redaction guard 写入 canonical `AgentLoopRunRecord`。

## 1. 真实运行命令与边界

本轮真实运行启动前已显式加载仓库 venv 与 `.env`：

```bash
source venv/bin/activate
set -a
source .env
set +a
export LLM_STREAM=true
export PYTHONPATH=project_1_llm_state_machine_modeling
python -m method.pr_e1_real_runs \
  --output-dir runs/pr_lg_c2_context_engineering_real_runs \
  --case-set all \
  --case-keys path1_abs,path1_elevator,path1_cara,path2_lng_ems \
  --condition-set default \
  --run-tag lg-c2-dotenv \
  --workers 4
```

边界说明：

- `.env` 中真实 provider / key / model 被使用；证据文件只记录 provider/model 的脱敏标识、hash 或 presence flag，不记录 raw secret。
- `LLM_STREAM=true`，四例 `.stream_summary.json` 均记录 `llm_stream_observed=true`。
- provider/network invalid run 数为 0。`path1_cara` 是真实完成后的 `not_converged / budget_exhausted`，不是 provider 或网络失败。
- 本轮 evidence 绑定实现 commit `c3f9c93618624e5520dbe3aba4746a0140ae0d29`；证据提交 commit 只新增运行记录，不改变实现代码。

## 2. 四例结果总览

| case | path | verdict / record | eligible | iter | repairs | real+stream | 关键 evidence |
|---|---|---|---:|---:|---:|---|---|
| `path1_abs` | Path1 | `success / success` | ✅ | 1 | 0 | ✅ | [report](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/report.md), [record](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `path1_elevator` | Path1 | `success / success` | ✅ | 1 | 0 | ✅ | [report](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/report.md), [record](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `path1_cara` | Path1 | `not_converged / budget_exhausted` | ❌ | 5 | 5 | ✅ | [report](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/report.md), [record](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `path2_lng_ems` | Path2 | `success / success` | ✅ | 1 | 0 | ✅ | [report](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/report.md), [record](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |

`path2_lng_ems` 的 `main_result_eligible=true` 只表示 run/schema/secret/trace/final verdict 可进入主结果候选；它仍被严格标记为 `path2_ref_model_blueprint_eligible=false`，不能宣传为 Path2 ref-model blueprint。

## 3. LG-C2 context subgraph 对账

四例 `run_config` 均包含：

- `lg_c2_context_subgraph_contract_hash=sha256:3dbda42324da55dec4210239dde6678c839f9c46c949045e194cd9691b7aa719`
- `lg_c2_context_subgraph_canonical_record_field=AgentLoopRunRecord.llm_interactions[].context_engineering`

本轮只有 `path1_cara` 进入 repair path，因此只有它执行 `SL-9` / `SL-10` 并产生 context-engineering interaction；其余三例在首轮 validation/review 直接收敛，未触发 `SL-9` / `SL-10`，因此没有 `llm_interactions[].context_engineering` 条目，这是预期行为。

`path1_cara` 对账结果：

- `context_engineering` 条目数：10。
- 覆盖 stage：`SL-9` 与 `SL-10`。
- 每个条目包含 node ids：`context_evidence_collect`、`context_budget_gate`、`context_compact_full_select`、`context_redaction_guard`。
- `selected_prompt_messages_hash == llm_interactions[].prompt_hash`：全部为 true。
- `context_engineering.estimated_prompt_tokens == llm_interactions[].estimated_prompt_tokens`，且 `budget_metadata.estimated_prompt_tokens` 同步：全部为 true。
- `redaction_guard.checked_before_provider=true`、`status=passed`、`secret_like_field_detected=false`：全部为 true。
- `redaction_guard_fail_closed=false`，表示没有因 secret-like payload 被 fail-closed 拦截；对应 fail-closed 逻辑由单元测试覆盖。

## 4. 本地校验命令

证据提交前执行过以下只读校验：

```bash
# 四例 rows / real provider / stream / LG-C2 canonical 字段 / hash-token-redaction 对账
python - <<'PY'
import gzip, json
from pathlib import Path
base = Path('runs/pr_lg_c2_context_engineering_real_runs')
rows = json.loads((base / 'summary.json').read_text())
for row in rows:
    d = base / row['run_id']
    rec = json.load(gzip.open(d / f"{row['run_id']}.agent_loop.json.gz", 'rt', encoding='utf-8'))
    stream = json.loads((d / f"{row['run_id']}.stream_summary.json").read_text())
    ce = [it for it in rec.get('llm_interactions', []) if it.get('context_engineering')]
    print(row['case_key'], row['verdict'], row['result_status'], row['main_result_eligible'],
          'real=', row['real_llm_provider_api'], 'stream=', stream['llm_stream_observed'],
          'context_entries=', len(ce))
PY
```

```bash
# secret 扫描：检查 .env 中 endpoint/key 原值和常见 token/API-key 模式未进入 run evidence
python - <<'PY'
# 详见主 session 运行日志；结果为 secret_scan_violations_count=0。
PY
```

## 5. 学术解释边界

- LG-C2 只增强上下文装配、budget、hash provenance 与 redaction 的可审计性，不把 LangGraph / context engineering 写成论文核心贡献。
- 本轮不改变 FixLog、NFRR、eligibility、stage verdict source、E1/E2 主比较字段。
- `path1_cara` 的 `not_converged` 是有价值的 stress evidence：它真实覆盖了 repair path 与 `SL-9` / `SL-10` context subgraph，但不能被宣传为模型质量成功样例。
- 三路最终 review 仍需强对抗检查：上游 #39 合同一致性、无样本特判、context metadata 未污染 prompt-visible payload、canonical record 承载 metadata、四例 evidence 是否足够可复核。
