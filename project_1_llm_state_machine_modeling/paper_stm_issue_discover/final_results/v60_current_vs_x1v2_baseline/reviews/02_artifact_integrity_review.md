# 独立 artifact 完整性审查

## 范围和方法

审查者只读检查本归档的 side manifest、顶层 manifest、schema、source-run provenance、排除规则和离线复算入口；从 `/tmp` 的空环境执行 `final_results_archive validate`，未调用 provider，未编辑任何文件。

## 已验证内容

- `raw/v60_current/archive_manifest.json` 覆盖 `1,508` 个文件，`raw/x1v2_baseline/archive_manifest.json` 覆盖 `842` 个文件；逐项字节数和 SHA-256 一致。
- 归档原始面共 `2,356` 个数据文件；side manifests 与 `paper1.final-results-archive.v1` schema 正确。`derived/recomputed_summary.json` 使用 `paper1.final-results-summary.v1`。
- v60 的 3 个、baseline 的 7 个 Judge source run 均已归档，composite 声明的 manifest hash 与 terminal hash 可以核对。
- 未发现 `llm/`、provider cache、`.lock`、`.part`、`launcher.log`、secret 或认证头。离线复算仅从 archive root 的 `raw/`、`reference/`、`derived/` 读取；不依赖原始 `runs/` 路径。

## 发现与处理

- C（审查时的中间状态）：顶层 `archive_manifest.json` 尚未覆盖新加入的 `README.md` 与 `SCHEMA.md`，也尚未有 report/reviews 的发布级 manifest。该缺口不影响 raw side manifest 或离线数值复算，但不能作为最终发布归档放行。
- I：raw JSON 保留 `190,544` 个原始绝对 provenance 路径。这些字段不参与离线复算，但人工迁移时需要稳定的 archive-relative 映射。
- I：X1v2 legacy method schema 不保存 source commit；必须披露，不能补造。

处理决定：`final_results_archive finalize` 生成 `publication_manifest.json`，覆盖报告、review、README、SCHEMA、raw、reference 与 derived；同时生成 `provenance_path_mapping.json`，把每个 source root 映射到 archive-relative 目录。完成后必须再次运行 `validate`。这一处理保留 raw JSON 原件，不改写其 provenance 字段。
