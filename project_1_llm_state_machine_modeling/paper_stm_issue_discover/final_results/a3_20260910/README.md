# A3 一次生成逻辑式报告：冻结结果

2026-09-10，Sonnet/Luna 各54 pair × 3 round = 162格，合计324格、1354条发布报告全部完成外部裁定。未运行 Qwen/Muse A3，不表示四模型或 O2 前置全部完成。方法为 `NL + 作者原始 STM + inspection -> 一个 LLM 直接生成 report/可选谓词 -> 执行 -> 确定性发布`；unsupported 的具体来源主张继续作为 W1。

| 模型 | A3 K/N/I | A3 precision | Full precision | A3 / Full hit@1 |
| --- | --- | --- | --- | --- |
| Sonnet | 463/91/130 | 554/684，80.99% | 719/823，87.36% | 230/435 / 291/435 |
| Luna | 404/90/176 | 494/670，73.73% | 759/903，84.05% | 245/435 / 323/435 |

完整逐轮、分层、配对区间、漏斗、内容案例与历史限制见[中文结果报告](../../reports/2026-09-10-a3-direct-report-results-cn.md)；方法/模型身份与异常恢复合同见[事前协议](../../discover_matrix/docs/generations/a3_20260910/preregistered.md)。N 是台账外有效报告数，不是独立新缺陷数；新增人工确认数为0。

## 文件与证据边界

| 文件 | 内容 |
| --- | --- |
| [results.json](results.json) | 两模型 A3/Full 的逐报告冻结判定、逐格生成到发布映射、来源哈希、完整主表/分层/逐轮指标、九簇重采样、命中增减与五轴及执行交叉表 |
| [full_source_manifest.json](full_source_manifest.json) | 原 Full 324格的逐文件哈希、输入一致性与独立重算指标；未新增 Full 或重裁 |
| [raw_index.json](raw_index.json) | 受限 raw 的逐文件大小与SHA-256、配置凭据精确匹配检查、历史未完成流名单 |
| [archive_manifest.json](archive_manifest.json) | 上述三个文件与145条台账的SHA-256；脱敏 profile、endpoint origin、费率与官方来源链接 |

完整 raw 位于本工作区 ignored `runs/paper1/a3_20260910/raw/`，上层目录权限700。原 `/tmp/paper1-a3-runs` 保留；归档用 `rsync -aL` 展开来源符号链接，内容字节不变。历史中断的15份 `.part` 流保留为失败证据，不能升级为成功阶段或据此把未知 usage 计为零；只排除锁文件。原失败格及恢复 manifest 均保留，最终成功选择以 results.json 的 source/hash 为准。

公开归档足以在不调用 provider、不读取凭据、不取得私有流的情况下重算已冻结标签的算术。原始输入/执行/流的全量复核另需本地 raw 与冻结 Full 原件；不声称 fresh clone 可以独立重裁全部私有请求，或复现 provider 的随机输出。

## 无 provider 复算

从仓库根执行，公开结果校验只需 Python 标准库：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/verify_archive.py
```

检查文件/台账哈希、每模型162个唯一格、每格报告分母、全部关系的 pair 归属、生成到发布映射、K/N/I与严格口径、逐轮/分层、完整命中增减与既有九NL簇10000次 bootstrap。任何缺格、漏报告或保存指标不一致都会失败。

真实 dry-run 已覆盖完整归档和篡改反例：将 Sonnet 的 K 加1、同时更新 results.json 的SHA-256，仍被逐报告算术重算拒绝。完整 raw 共9540个文件，含15份历史中断流；凭据精确匹配检查为0。Full来源清单与执行前清单逐字一致。

取得 raw 后，可额外核验每个文件；路径可迁移：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/verify_archive.py \
  --raw-root runs/paper1/a3_20260910/raw
```

在仓库既有 venv、pyfcstm 依赖和 Full 原件齐备时，从原始格重新生成所有分析：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover:pyfcstm:. \
python -W ignore project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/analyze_a3.py \
  --run-root runs/paper1/a3_20260910/raw --output /tmp/a3-recomputed.json
```

此命令不需要 `.llmconfig.yml` 或 live 标志。最终复算已从上述独立 raw 归档通过，不依赖其原先指向 `/tmp` 的符号链接。运行参数为完整模式，未使用 `--allow-partial`。

## 实现检查

A3 定向检查为22项通过，JUnit原件见 raw 的 `verification/a3-tests.xml`。同目录保留原基线/当前广域回归 XML：两者均133 passed、16 failed、6 errors，149个唯一用例结果一致；不宣称全仓库全绿。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover:pyfcstm:. \
python -W ignore -m pytest -q \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/tests/test_direct_report.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/tests/test_direct_report_bindings.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/tests/test_a3_batches.py
```

正常单次生成及全部关闭消费者的不可达检查、真实后端true/false/unknown、全部十二谓词绑定、发布映射、零报告/失败降级、Full/A1对拍和节点阶段复用均有定向证据。算术核验不证明自动裁判没有语义错误，已发现的 relation-first 标签/根因粒度风险和严格D1/D2敏感性保留在中文报告中。
