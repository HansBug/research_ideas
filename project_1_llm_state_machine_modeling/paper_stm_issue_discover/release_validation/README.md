# Internal RC Release Validation

本目录保存 release-structure refactor 的一次内部技术回归，不是新的论文主实验，也不属于冻结的 `final_results/`。它被 method release allowlist 排除。

固定样本为 15 个 pair：`0001, 0002, 0004, 0010, 0012, 0013, 0023, 0024, 0029, 0035, 0046, 0049, 0053, 0054, 0056`。`v60_15pair_reference.json` 在 live run 前从永久 v60 归档机械抽取 45 个 method/Judge cells；`validation_manifest.json` 预先限定仅能运行一轮 method 和一次后续 Judge。

目录内容：

- `raw/method/b3502e6aa068493596472f98f57f9b49/`：internal RC 实际构建并独立安装的 method 包的 15x1 原始审计制品。
- `raw/judge/e3e95eb94f6c45289d7b32b7b865ccfb/`：同一 RC 的独立 Judge 包对上述 method output 的唯一 issue #195 Judge 原始制品。
- `v60_15pair_reference.json` 与 `v60_15pair_reference_cn.md`：v60 三轮的逐 cell SHA-256 引用和派生参考。
- `release_15x1_comparison.json` 与 `release_15x1_comparison_cn.md`：provider-free 的对照结果、合同检查、carrier 三分类、W/K/N/I/D/stage-loss 与成本审计。
- `derived/`：只读 raw inputs 的 stage-loss 和 metrics 派生结果。
- `provenance/`：method/Judge 发布包在 live run 前构建时的 manifest。
- `reviews/`：独立只读审查记录及其更正。

`input_closure_preflight.json` 与 `input_closure_post_method.json` 对固定 v60 cells 的 540 个 `ContextManifest` ArtifactRef 做 SHA-256 检查。顶部 `input_data_hash` 和 `run_contract_hash` 分别包含所选 pair 集、round 数和 RC provenance，不能与 v60 的 54-pair x 3 合同逐字相同；决定性的实验输入不变量是 15 个 `pair_input_hashes` 与 ArtifactRef 文件哈希。

从仓库根目录可离线重算比较：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src \
venv/bin/python -m paper_stm_evaluation.release_validation compare \
  --reference project_1_llm_state_machine_modeling/paper_stm_issue_discover/release_validation/v60_15pair_reference.json \
  --method-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/release_validation/raw/method/b3502e6aa068493596472f98f57f9b49 \
  --judge-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/release_validation/raw/judge/e3e95eb94f6c45289d7b32b7b865ccfb \
  --ledger project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/ledger.json \
  --output-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/release_validation
```

该命令不调用 provider。它只读取归档和本目录 raw artifacts，并重生 comparison JSON、中文对照及 `derived/release_15x1_*`。

正式对外公开再分发仍需要权利人明确指定 method-source `LICENSE`。本目录只证明内部技术 RC 的结构、安装和回归验收，不构成该法律授权。
