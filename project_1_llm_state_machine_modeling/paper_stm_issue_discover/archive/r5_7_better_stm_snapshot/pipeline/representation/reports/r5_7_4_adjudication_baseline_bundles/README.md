# R5.7.4 裁决 baseline bundle 逻辑入口

本目录是 R5.7.4 / R5.7.5 专用的 **baseline `.fcstm` bundle 逻辑入口**。它把 R5.7.4 静态裁决用到的 4 个 `llms-emp` baseline bundle 收拢到同一处，便于后续 R5.7.5 构造 `STM_k` 时稳定定位 `STM_0` 的内部实验介质。

> 关键纪律：本目录只做 symlink fan-in 与索引，不移动、不复制、不重写权威产物；`.fcstm` 仍只是内部实验介质，不是论文贡献；conversion / normalization / parse inspect 成功都不能计入 repair gain。

## 1. 为什么需要这个目录

R5.7.4 四个裁决样例的 baseline bundle 原本分散在两个阶段目录中：

1. `0000` / `0045` 已经在 R4.5 selected smoke export 中存在，权威目录是 [../fcstm_exports/](../../../../../../pipeline/representation/reports/fcstm_exports)。
2. `0001` / `0018` 是 R5.7.4 为静态裁决和 R5.7.5 handoff 新物化的 standalone baseline bundle，权威目录是 [../r5_7_4_adjudication_fcstm_exports/](../r5_7_4_adjudication_fcstm_exports/)。

如果把两类产物物理混到一个目录，会模糊 R4.5 selected smoke 与 R5.7.4 adjudication evidence 的阶段边界；如果只保留原路径，又会让 R5.7.5 消费四例时来回查找。因此本目录采用“**权威产物不动 + 相对 symlink 逻辑收拢 + JSON 总账**”的方式。

## 2. 目录结构

```text
r5_7_4_adjudication_baseline_bundles/
├── README.md
├── bundle_index.json
└── bundles/
    ├── llms_emp_stm_results_0000__llms-emp-gpt4o-hldcs -> ../../fcstm_exports/llms-emp-gpt4o-hldcs
    ├── llms_emp_stm_results_0001__llms-emp-gpt4o-hstbs -> ../../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4o-hstbs
    ├── llms_emp_stm_results_0018__llms-emp-gpt4-digital-camera -> ../../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4-digital-camera
    └── llms_emp_stm_results_0045__llms-emp-deepseek-microwave -> ../../fcstm_exports/llms-emp-deepseek-microwave
```

`bundles/` 下的 4 个条目都是相对 symlink。若要读机器可消费总账，优先读 [bundle_index.json](./bundle_index.json)。

## 3. 四例统一入口

| pair id | 逻辑入口 | 权威来源阶段 | 权威 bundle | R5.7.4 角色 | selected smoke? | hash 口径 |
|---|---|---|---|---|---|---|
| `llms_emp_stm_results_0000` | [bundles/llms_emp_stm_results_0000__llms-emp-gpt4o-hldcs](./bundles/llms_emp_stm_results_0000__llms-emp-gpt4o-hldcs) | R4.5 | [../fcstm_exports/llms-emp-gpt4o-hldcs/](../../../../../../pipeline/representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs) | T0 / HSM / condition-like guard target sanity check | 是 | 以 R4.5 committed baseline hash 为 R5.7.5 authoritative baseline；seed-sweep hash 作 audit trail，可能不同。 |
| `llms_emp_stm_results_0001` | [bundles/llms_emp_stm_results_0001__llms-emp-gpt4o-hstbs](./bundles/llms_emp_stm_results_0001__llms-emp-gpt4o-hstbs) | R5.7.4 | [../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4o-hstbs/](../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4o-hstbs/) | T0 / FSM / low-noise no-target control | 否 | R5.7.4 物化 bundle hash 与 seed-sweep hash 一致。 |
| `llms_emp_stm_results_0018` | [bundles/llms_emp_stm_results_0018__llms-emp-gpt4-digital-camera](./bundles/llms_emp_stm_results_0018__llms-emp-gpt4-digital-camera) | R5.7.4 | [../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4-digital-camera/](../r5_7_4_adjudication_fcstm_exports/llms-emp-gpt4-digital-camera/) | T1 / supplementary stress / limitation case | 否 | R5.7.4 物化 bundle hash 与 seed-sweep hash 一致。 |
| `llms_emp_stm_results_0045` | [bundles/llms_emp_stm_results_0045__llms-emp-deepseek-microwave](./bundles/llms_emp_stm_results_0045__llms-emp-deepseek-microwave) | R4.5 | [../fcstm_exports/llms-emp-deepseek-microwave/](../../../../../../pipeline/representation/reports/fcstm_exports/llms-emp-deepseek-microwave) | T0.5 / microwave / timer-like caveat | 是 | 以 R4.5 committed baseline hash 为 R5.7.5 authoritative baseline；seed-sweep hash 作 audit trail，可能不同。 |

## 4. 每个 bundle 应包含什么

后续 R5.7.5 / R6 / R7 读取这里时，应至少核对：

1. `model.fcstm`：baseline 的内部实验介质。
2. `name_mapping.json`：raw label 与 emitted identifier 的映射。
3. `lowering_inventory.json`：lowering / timing / hierarchy / source traceability 审计账。
4. `parse_inspect_report.json`：pyfcstm parse / inspect 结构化诊断。
5. `canonical_stm.json`、`bundle_meta.json`、`fcstm_export_loss_ledger.jsonl`：仅 R5.7.4 新物化的 `0001` / `0018` bundle 当前具备；R4.5 selected smoke 两例则回到 [../fcstm_export_report.json](../../../../../../pipeline/representation/reports/fcstm_export_report.json) 与 [../fcstm_export_loss_ledger.jsonl](../fcstm_export_loss_ledger.jsonl)。

## 5. 使用纪律

1. **不要通过 symlink 手工改模型**：本目录不是新的权威产物目录；如需重生成，必须回到对应阶段的 exporter / report。
2. **不要复制 bundle**：复制会形成第二事实源，导致 hash、loss ledger 和 parse inspect report 漂移。
3. **不要扩充 selected smoke panel**：`0001` / `0018` 不进入 [../../../../selected_seed_examples/](../../../../../../selected_seed_examples)；本目录只为 R5.7.4 / R5.7.5 裁决服务。
4. **不要改写 R4.5 总账语义**：[../fcstm_export_report.json](../../../../../../pipeline/representation/reports/fcstm_export_report.json) 仍只描述 R4.5 selected smoke 四例，不因为本目录的逻辑收拢而变成 R5.7.4 四例总账。
5. **不要把 representation readiness 写成 repair gain**：`.fcstm` 可解析、diagnostic 可读、hash 可追溯，只说明 baseline 介质准备完成；真正 Better 裁决需要 R5.7.5 或之后的 `STM_k`、change ledger 与 semantic gate。
6. **R5.7.5 必须声明 authoritative baseline hash**：`0000` / `0045` 使用本目录指向的 R4.5 committed baseline hash；seed-sweep hash 保留为 audit trail。`0001` / `0018` 使用 R5.7.4 物化 bundle hash。

## 6. 快速复验

```bash
python - <<'PY'
import json
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles')
index = json.loads((root / 'bundle_index.json').read_text())
for item in index['items']:
    link = Path(item['logical_symlink_path'])
    auth = Path(item['authoritative_bundle_path'])
    fcstm = Path(item['authoritative_fcstm_path'])
    print(item['pair_id'], link.is_symlink(), link.resolve() == auth.resolve(), fcstm.exists(), item['parse_status'], item['inspect_status'])
PY
```

预期：4 行均显示 symlink 解析到权威目录，`model.fcstm` 存在，`parse_status=ok`，`inspect_status=ok`。
