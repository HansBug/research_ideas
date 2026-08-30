# Paper STM Method

`paper-stm-method` 是 Paper1 当前的 typed evidence-discovery method。它面向需要审计 NL 与作者状态机是否一致的使用者：读取完整输入闭包，生成具体发现和方法证据，并把结果写到调用者指定的新目录。它不包含 Semantic Judge、evaluation、ledger、expected answer、baseline、final_results、历史运行记录或旧实现。

## 输入与输出

方法读取的输入闭包包括 `pairs/`、`canonical/`、`parse_inspect/`、`source_traces/`、`working_contracts/` 与 `case_reports/`。其中 NL 和作者 PlantUML 是问题与定位的来源；canonical source IR 保持作者源的规范化映射；FCSTM 与 native/inspection facts 用于确定性执行；working contract 和 source trace 限制跨表示映射及归因。方法不会把 inspection fact 当作新增义务，也不会从输入之外读取 ledger、Judge、expected answer 或历史 report。

输出是 method-native artifact，包括 stage receipt、候选、typed predicate binding、compiler/backend receipt、D/W 裁定和 D1/D2 publication。调用者必须提供新 `--output-dir`；方法不修改输入闭包或冻结制品。

## 运行流程

1. `prepare` 校验输入闭包及其 provenance。
2. `contract_extraction` 从 NL 提取可追溯 contract；仅在固定条件满足时，`contract_completion` 执行一次有界补全。
3. `discovery_grounding` 以两个互补 lens 产生并定位候选。
4. `execute_batch` 运行确定性 frontier、route、typed binding、predicate compiler 和 native backend。
5. `d_adjudication` 及其受限 correction 对问题主张作方法内裁定；`validate_d` 保留审计和降级信息。
6. `publish` 仅发布 D2/D1，并按 exact typed identity 去重。

四族 19 个冻结谓词为可执行证据提供 route，不是发现或 publication 的准入门。W2 要求精确制品、合法 typed input、真实 backend terminal `true`/`false` 和完整 receipt。输入缺失、fragment 外、timeout 或 backend failure 不会成为 W2；具体但未闭合的发现仍可为 W1，无法具体定位的主张为 W0。D2/D1 才进入发布面，D0 不发布；L 只属于 ledger，不由方法生成。

## 安装与命令

从干净 checkout 构建最小 method 发布树。构建器只复制 allowlist 文件并生成逐文件 hash，不改写源码、prompt、schema、资源或 import。

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/build_method_release.py \
  --output /tmp/paper-stm-method-release
python -m pip install "/tmp/paper-stm-method-release[test]"
paper-stm-method --help
```

发布树随包提供 `predicate_registry.json`、`current_source_catalog.json` 和所需的中立 `utils` 子模块；安装元数据固定 `pyfcstm` 兼容 revision。真实运行需要操作方显式提供 `utils.llm` profile 和 `--allow-live`，凭据不进入发布包或运行记录。provider-free 资源检查可在任意工作目录执行：

```bash
python -c "from paper_stm_method.inputs import parse_fcstm; print(parse_fcstm('state Root { state A; [*] -> A; }').algorithm_version)"
```

## 实验引用与边界

本发布结构是可复用的 method package，不绑定任何单一实验运行或评测对照。具体运行的 input、resource、prompt/schema、run contract 和 source provenance 由调用方的 run manifest 与相应归档保存；这些外部评测材料不属于 method package 的输入读取路径。方法 source 的正式公开再分发仍需要权利人指定 LICENSE；[NOTICE.md](./NOTICE.md) 不构成此授权。
