# `datasets/` — 导出脚本产物落地目录

## 用途

本目录是 [`../scripts/`](../scripts/) 中 4 个 benchmark 范式导出脚本的**默认持久化目标位置**。需要把跨数据集的 NL→STM 样本固化为 jsonl / parquet 时，统一放在这里，**禁止写入 `/tmp` 等仓库外、不可追溯路径**。

## 与上游 parquet 的差别

- 上游 [`../`](../) 下的 21 个 parquet 是**原始解析产物**（一行一个数据集 catalog / 一行一个生成样本 / 一行一个人评记录等），由 [`../../../discussions/2026-04-15-01-03-52-...parquet化.md`](../../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md) 中的 `build_*.py` 脚本生成
- 本目录下的 jsonl / parquet 是**下游派生产物**，由 [`../scripts/`](../scripts/) 中的 4 个导出脚本对上游 parquet 做字段重组、跨数据集对齐、benchmark 范式切片之后生成
- 上游是真源，下游可随时按脚本重生 —— 因此本目录里的产物**不进 git**（见本目录 `.gitignore`）

## 生成方式（示例）

```bash
# 在 baselines_double_green/ 目录下执行
python scripts/export_nl_input.py --dataset all -o datasets/nl_inputs.jsonl
python scripts/export_nl_to_stm.py --dataset all -o datasets/nl2stm.jsonl
python scripts/export_human_review.py --paper llms_emp -o datasets/hr_llms_emp.jsonl
python scripts/export_unified_benchmark.py --strict-alignable-only --drop-no-ref \
    --format parquet -o datasets/unified.parquet
```

每个脚本都接 `--help`。

## 可追溯性约束

1. 任何下游派生产物必须能**通过当前 `../scripts/` 在原始 21 parquet 之上一键重生**；如果某个产物无法重生（依赖临时手工后处理），必须把后处理逻辑沉淀进 `../scripts/`，不要让产物变成不可追溯的孤儿
2. 不要把上游 parquet 复制进本目录；下游产物要引用上游时，在脚本里用 `pd.read_parquet("../<file>.parquet")` 读，不要 `cp`
3. 本目录内的产物不进 git，但**本目录本身（含本 README + `.gitignore`）必须进 git**，作为"产物落地约定"的占位
