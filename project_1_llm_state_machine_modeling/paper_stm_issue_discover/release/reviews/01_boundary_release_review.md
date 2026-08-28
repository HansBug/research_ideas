# 边界与发布白名单独立审查

## 范围与方法

独立 reviewer 在 `8d6881c530527fcf31cbe21af157e6bc094050d8` 上只读审查
method、Judge、evaluation、顶层 `utils`、method release allowlist 及 native
projection scan。检查包含静态 import、资源定位、独立安装路径和发布泄漏边界；
没有调用 provider，也没有改动任何冻结制品。

## 发现与处理

| 严重度 | 发现 | 处理 |
| --- | --- | --- |
| 高 | Judge `scale_audit.py` 对 algorithm hash 读取已迁移前的 `evidence_discovery` 路径，独立 Judge 包会失败。 | 改为哈希实际安装的 `utils.structured_runtime` 与 `utils.stm_artifacts` 模块；新增 provider-free 回归测试。 |
| 高 | method 发布包不含 `.git`，runner 因 provenance 不可解析拒绝所有 live run。 | 保留 Git checkout 的原有优先路径；仅在 Git 不可见时接受经 40-hex 校验的 `PAPER_STM_RELEASE_SOURCE_COMMIT`，并记录它与生成的 `release_manifest.json` 的对应关系。无该变量仍 fail-closed。 |
| 高 | method 源码没有明确许可证，当前 `NOTICE.md` 也明确不授予再分发许可。 | 未擅自添加或伪造许可证。公开再分发前必须由权利人选择并提交许可证；这是最终公开 release 的非技术阻塞项。 |
| 中 | release builder 可将输出写进源 checkout，违背其 byte-copy-only 隔离声明。 | 输出目录在创建前必须位于 checkout 之外；新增回归测试。 |

## 结论

前三项技术边界问题已在本次 refactor 后续提交中修正，并由 provider-free
测试覆盖。method/Judge 的算法、prompt、schema、谓词、冻结归档和实验口径未修改。
独立开源发布仍取决于权利人提供 method source 的许可证；在此之前只能称为
内部可复现的 release candidate，而不能声称可公开再分发。
