# 边界与发布白名单独立审查

## 范围与方法

独立 reviewer 在 `a3e2bad40091fbba467e208ad0ac74ac9c29231b` 上只读审查
method、Judge、evaluation、顶层 `utils`、两个 release allowlist 与 native
projection scan。检查包含静态 import、资源定位、独立安装路径、发布泄漏边界和
installed-package provenance；没有调用 provider，也没有改动任何冻结制品。

## 发现与处理

| 严重度 | 发现 | 处理 |
| --- | --- | --- |
| 高 | Judge `scale_audit.py` 对 algorithm hash 读取已迁移前的 `evidence_discovery` 路径，独立 Judge 包会失败。 | 已改为哈希实际安装的 `utils.structured_runtime` 与 `utils.stm_artifacts` 模块，并有 provider-free 回归测试。 |
| 高 | method 发布包不含 `.git`，runner 因 provenance 不可解析拒绝所有 live run。 | 已改为校验嵌入的 `release_manifest.json`：逐文件 SHA-256 与 source commit 均通过才接受；不再依赖环境变量，无 manifest 仍 fail-closed。 |
| 高 | Judge 发布包也曾只从 Git checkout 取得 code commit，脱离 checkout 的 `--allow-live` 在输入前失败。 | `0a87639e2` 增加同样的嵌入 manifest hash 验证；独立安装的空输入 preflight 已越过 provenance 并在 source-path 检查停止，未初始化 runtime/provider。 |
| 中 | Judge builder 复用 method 专属 `paper-stm-method.release-manifest.v1`。 | `0a87639e2` 将 builder 参数化，Judge 输出 `paper-stm-judge.release-manifest.v1`；回归测试覆盖两个命名空间。 |
| 高 | method 源码没有明确许可证，当前 `NOTICE.md` 也明确不授予再分发许可。 | 未擅自添加或伪造许可证。公开再分发前必须由权利人选择并提交许可证；这是最终公开 release 的非技术阻塞项。 |
| 中 | release builder 可将输出写进源 checkout，违背其 byte-copy-only 隔离声明。 | 输出目录在创建前必须位于 checkout 之外；新增回归测试。 |

## 结论

所有已发现的技术边界问题均已在后续提交中修正，并由 provider-free 测试或独立安装
preflight 覆盖。审查时 method release 为 71 个 allowlisted 文件、Judge release 为 38 个
allowlisted 文件；二者均无 method/Judge 交叉业务 import、ledger/baseline/final-results
路径、凭据或本机绝对路径。method/Judge 的算法、prompt、schema、谓词、冻结归档和实验
口径未修改。

独立开源发布仍取决于权利人提供 method source 的许可证；在此之前只能称为内部可复现的
release structure，而不能声称可公开再分发，也不能创建最终 release candidate 或启动
15x1 live regression。

## 最终只读复核

独立 reviewer 在 `0377c74f376653025cb752f0eec941fb7663c721` 对修复后的发布树复核：

- 独立安装的 Judge 从非 Git 目录读取包内 `release_manifest.json`，逐文件 SHA-256 校验后
  返回提交 `0377c74f376653025cb752f0eec941fb7663c721`。`--allow-live` 已越过 provenance
  前置检查，只因刻意提供的不存在 method cell 在输入加载处报 `FileNotFoundError`；未再出现
  Git-only 失败，也未初始化 provider。
- Judge 发布 manifest 为 `paper-stm-judge.release-manifest.v1`，顶层与嵌入副本字节一致，
  38 个 payload 文件均存在且 SHA-256 匹配。新构建的 method/Judge 发布树分别含 71/38 个
  allowlisted 文件。
- 除测试后产生的瞬态缓存外，manifest payload 无额外文件、无 hash 差异、无
  method/Judge/evaluation/pipeline 跨边界 import、无 secret 或本机绝对路径。
- `validate_release_structure.py` 通过：冻结归档 `2671/2671`、历史 pytest node `465/465`、
  boundary violation `0`、provider/billable calls `0/0`。Judge fixture 与结构测试为
  `9 passed, 7 warnings`。

除 method source 的权利人许可证授权外，未发现仍存的技术高严重度发布问题。本复核没有
修改文件、调用 provider 或启动实验。
