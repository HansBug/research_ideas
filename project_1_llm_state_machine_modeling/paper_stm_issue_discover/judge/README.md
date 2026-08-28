# Paper STM Semantic Judge

`paper-stm-semantic-judge` 实现冻结的 issue #195 Semantic Judge。它接收 arm-neutral method report 和只读状态机制品闭包，对 report 的语义有效性及其与 expected issue 的关系作独立裁定。它不 import method discovery、predicate routing、evaluation、baseline 或历史运行代码；method 也不读取 Judge 输出。

## 两阶段判定

第一阶段为 validity：Judge 对单个 report 作证据和主张审查，产生 expected-isolated `FrozenValidityCertificate` 及其 `core_truth`。只有证书冻结为 valid 的 report 才进入第二阶段。第二阶段为 relation：Judge 在冻结 certificate 的约束下将 report 与显式提供的 expected issue 比较，给出 `FULL`、`PARTIAL` 或 `NONE`。最终 backend 依据 validity 与 relation closure materialize `VALID_KNOWN`、`VALID_NOVEL` 或 `INVALID`。两轴不能互相替代：`FULL/PARTIAL/NONE` 是 expected relation，`VALID_KNOWN/VALID_NOVEL/INVALID` 是 report validity，只有 `INVALID` 进入 report semantic FP。

Judge 的 expected material 是由调用方以受控输入投影提供的评测数据，不会回传给 method，也不构成 method 包的依赖或答案泄漏。Judge 的输出不控制 method 的 candidate、predicate、W、D 或发布路径；W 是 arm-generated finding 的证据形态，Judge 的事后核验不会自动创造 W2。

## 协议、输入与输出

包内的 `semantic_judge_issue_195.snapshot.md` 与冻结 protocol snapshot byte-identical，运行前由 SHA-256 校验。输入包含方法发布 report、状态机制品闭包和 Judge 所需的明确定义投影；输出是带 prompt/schema/provenance hash、certificate、relation/validity decision 和 reason/basis 的审计制品。Judge 只写调用者指定的新输出目录。

## 安装与命令

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/build_judge_release.py \
  --output /tmp/paper-stm-judge-release
python -m pip install "/tmp/paper-stm-judge-release[test]"
paper-stm-semantic-judge --help
```

发布树只包含 Judge、稳定 protocol resource 和 manifest 列出的中立 `utils` 子模块；不包含 method、evaluation、ledger、baseline、final_results、run 或 legacy 数据。真实 Judge 调用需要操作方显式配置 profile 并给出 `--allow-live`；`--help`、安装和资源读取不调用 provider。

v60/current 的 Judge 实验提交为 `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`，协议标识为 `github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`。完整输入、输出和独立复算见 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md)。
