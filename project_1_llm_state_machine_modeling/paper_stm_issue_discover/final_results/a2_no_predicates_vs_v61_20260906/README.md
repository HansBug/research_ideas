# A2 no-predicates 与冻结 v61：完整结果归档

冻结日期：2026-09-06。A2 的 54 pair × 3 round = 162 个唯一格、942 份最终报告已全部裁定，435 个 expected-round 无缺失。对照只读引用 [v61 原始归档](../v61_source_divergence_vs_x1v2_baseline/README.md)，没有新增 full method 或 full judge。中文解释、逐层分析与审计附录见[结果报告](../../reports/2026-09-06-20-24-24-a2-no-predicates-v61-results-cn.md)。

| 指标 | frozen v61 | A2 no-predicates |
| --- | --- | --- |
| FULL hit@1 | 323/435 | 328/435 |
| FULL hit@3 | 130/145 | 127/145 |
| FULL hit@all | 82/145 | 92/145 |
| L2 hit@1 / @3 / @all | 97/117；36/39；28/39 | 100/117；37/39；31/39 |
| K / N / I | 561 / 198 / 144 | 582 / 218 / 142 |
| report precision | 759/903 | 800/942 |
| D1/D2-only precision | 678/903 | 706/942 |

`hit@1` 是三轮 expected-round 平均命中率；`hit@3` 是至少一轮命中，`hit@all` 是三轮均命中。唯一台账仍为 145 条。N 包含重叠的有效报告，不等于独立新缺陷数。主口径与严格 D1/D2-only 口径均保留全部发布报告作为 precision 分母。

## 归档内容

| 路径 | 用途 |
| --- | --- |
| [derived/analysis.json](./derived/analysis.json) | 两臂逐格、逐报告、435 个 expected-round、全部指标、九簇 bootstrap、逐簇留出、provider 配对子集与相同核心文本审计 |
| [derived/change_audit.json](./derived/change_audit.json) | 44 gained / 39 lost 的全部 83 条变化及原始候选定位；agent 判读，不改裁定 |
| [derived/case_audit.json](./derived/case_audit.json) | 六个解释与裁定风险案例，包含 A2 和历史 v61 的反例 |
| [derived/judge_input_audit.json](./derived/judge_input_audit.json) | 162 格的输入回执和文档字段 fingerprint；2106 次证据文档投递与 v61 对应字段一致 |
| [raw/source_runs/](./raw/source_runs/) | 三段 method 来源、冻结选择表、完整格和被替代旧格的结构化原件 |
| [raw/judge/](./raw/judge/) | 11 个 judge 批次的 manifest、输入、最终裁定及保留的结构化中间件；共 162 个唯一最终裁定 |
| [raw/inputs/](./raw/inputs/) · [raw/ledger.json](./raw/ledger.json) | 648 份输入文件及冻结 145 条台账 |
| [raw/checks/](./raw/checks/) · [raw/transport_audit.json](./raw/transport_audit.json) | 配置身份、依赖、三段机制审计、切换证据和 provider 流的 hash、usage、错误、重试索引 |
| [provenance.json](./provenance.json) · [archive_manifest.json](./archive_manifest.json) | 来源位置、选择身份、保留政策及逐文件 SHA-256 清单 |

## 离线复验

在仓库根、已有依赖的 venv 中运行。以下命令不读取凭据、不调用模型：

```bash
P=project_1_llm_state_machine_modeling/paper_stm_issue_discover
G=$P/discover_matrix/docs/generations/a2_no_predicates_20260906
export PYTHONPATH=.:$P/method/src:$P/evaluation/src:$P/judge/src:$G
venv/bin/python "$G/archive.py" validate
```

从归档重算全部统计并与冻结结果逐项比较：

```bash
venv/bin/python - <<'PY'
from pathlib import Path
import json, subprocess, tempfile
import archive
root = archive.DESTINATION.resolve()
frozen = json.loads((root / 'derived/analysis.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
    output = Path(tmp) / 'analysis.json'
    subprocess.run(archive.analysis_command(root, output), check=True, stdout=subprocess.DEVNULL)
    fresh = json.loads(output.read_text())
for arm in ('a2', 'v61'):
    for key in ('metrics', 'coverage', 'expected', 'per_round', 'per_cluster', 'per_pair', 'per_provider_segment'):
        assert fresh[arm][key] == frozen[arm][key], (arm, key)
for key in ('changes', 'paired_uncertainty', 'provider_paired_sensitivity'):
    assert fresh[key] == frozen[key], key
for key in ('matched_text_groups', 'classification_changed_groups', 'full_targets_changed_groups'):
    assert fresh['shared_report_text_audit'][key] == frozen['shared_report_text_audit'][key], key
print('All frozen counts, rates, changes and paired uncertainty reproduced exactly.')
PY
```

## 解释与复现边界

本批使用当前 12 谓词软件基线关闭整个谓词机制；v61 保留历史 19 谓词身份。源码、prompt/schema、provider 与调用日期不同，因此这是用户指定的历史比较。九簇区间描述本批差值，不消除这些混杂，不证明等效、优越或单因素因果效应。A2 的 W2=0 是开关设计，不是效果指标。

Method 选择保留旧站点 37 格/271 报告和新站点 125 格/671 报告；judge 为旧站点 7 格/51 报告、新站点 155 格/891 报告。新站点 `aizzz-luna-eval` 使用 `https://api.aizzz.xyz/v1`、`gpt-5.6-luna`，原生 16 workers，批次串行。共享私有配置未改。三段源码、私有配置的无凭据 hash 和切换政策见 [preregistered.md](../../discover_matrix/docs/generations/a2_no_predicates_20260906/preregistered.md)。

最终选样全部 eligible/completed，但其中仍有 280 条内部 D_UNRESOLVED evidence。旧 `0009:r2` 的 HTTP 520 降级零报告格另存为 predecessor，未冒充正常零报告或被删除。三段机制审计的 1762 处上下文检查均标 `partial=true`，不覆盖全部中断流。

原始 provider `llm/`、`.part` 流和完整 v61 judge 输入留在本地 ignored runs；归档保留其 hash、可观测 usage/error/retry，以及历史输入文档的字段 fingerprint。远端可重算冻结裁定、重新投影报告并校验 A2 输入，不能重读全部历史请求或重新完成独立语义裁定。`raw/checks` 内历史 live launcher 只作来源证据，不能当作本归档的直接 live 重跑入口；中断请求的未知 usage 不按零计，也不从重复快照累计价格。

本次新结果的人工确认数为 0。全部自动裁定和 agent 审计均保留原身份；分析没有回流 method、改台账或按质量重裁。统计解释状态为 ANALYZED，离线算术与结构核验另有上述可执行检查。
