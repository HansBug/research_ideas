# Paper STM Method

`paper-stm-method` 是 Paper1 类型化证据发现架构的当前实现。架构以 FCSTM 为分析工作表示，并通过语言适配器接收作者源状态机；本发行包提供的是 PlantUML 适配器，而不是把 PlantUML 设为方法前提。原则上，能在声明的源语言子集内形成可追溯 FCSTM 投影的状态机建模语言都可接入。新适配器必须保留作者源属追踪，说明规则相关能力到 FCSTM 的映射，对不能可靠映射的特征失败关闭，并接受独立评测；完成这些工作后，才可报告该语言的方法结果。当前实现读取完整输入闭包，生成具体发现和方法证据，并把结果写到调用者指定的新目录。它不包含人工裁定接口、evaluation、ledger、expected answer、baseline、final_results、历史运行记录或旧实现。

## 输入与输出

方法读取的输入闭包包括 `pairs/`、`canonical/`、`parse_inspect/`、`source_traces/`、`working_contracts/` 与 `case_reports/`。在当前实现中，NL 和作者 PlantUML 是问题与定位的来源；canonical source IR 保持作者源的规范化映射；FCSTM 与 native/inspection facts 用于确定性执行；working contract 和 source trace 限制跨表示映射及归因。方法不会把 inspection fact 当作新增义务，也不会从输入之外读取 ledger、Judge、expected answer 或历史 report。

输出是 method-native artifact，包括 stage receipt、候选、类型化谓词绑定、compiler/backend receipt 和 W 证据。流程中名为 `d_adjudication` 的内部阶段只保留候选筛选与审计信息，不构成 Paper1 的 D/A 裁定；事实、义务、D/A、有效性和关系由独立人工评测完成。调用者必须提供新 `--output-dir`；方法不修改输入闭包或冻结制品。

## 运行流程

1. `prepare` 校验输入闭包及其 provenance。
2. `contract_extraction` 从 NL 提取可追溯 contract；仅在固定条件满足时，`contract_completion` 执行一次有界补全。
3. `discovery_grounding` 以两个互补 lens 产生并定位候选。
4. `execute_batch` 运行确定性 frontier、route、typed binding、predicate compiler 和 native backend。
5. `d_adjudication` 及其受限 correction 执行候选筛选并保留审计和降级信息，不产生 Paper1 的 D/A 裁定。
6. `publish` 输出方法发现，并按 exact typed identity 去重；Paper1 的发布级 D2/D1 处置来自独立人工评测。

当前注册表 `four-family-12-core.v1` 提供连续编号的四类 12 种谓词：`S1–S5 / G1–G3 / R1–R3 / V1`。这些谓词按工作流证据需求选择，为适用发现提供类型化绑定和执行入口。W2 同时要求受支持片段、精确实例绑定、pair/obligation/plan/model/program/receipt 的精确身份链、非空且可核验的需求引文/来源引用/绑定引用，以及完成的原生 backend `true`/`false` 回执。输入缺失、资格未闭合、timeout 或 backend failure 不会成为 W2；仍在 Paper1 声明范围内且具体但未闭合的发现仍可为 W1，无法具体定位的主张为 W0。来源归属不完整只降低 W2 资格，不得把已经完成的执行改写为 `failed`、`blocked` 或空布尔值。谓词/极性元数据限制论文可对完成回执作出的最强语义主张，例如有界检查不能充当无界证明；它们不降低来源绑定且已完成 Boolean 执行的 W2。全局范围外的语言或模型语义不进入 finding。D2/D1 的 Paper1 发布级处置来自人工评测；L 只属于 ledger，不由方法生成。

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

方法条件统一通过 `--ablation none|no-inspect|no-predicates` 传递，省略时为 `none`，保持完整方法行为。`no-inspect` 使用 method-local 受限视图：前置检查事实、诊断摘要及其派生候选/预检/D 校验关闭；保留作者源、FCSTM、转换追踪、源码分歧和当前 12 条谓词的候选专属执行。原输入在 `input_audits/` 保留，仅作审计，不传入发现流程。主动关闭记录为 `disabled_by_ablation`，不是检查通过。

`no-predicates` 保留完整输入及检查事实、NL 契约与两路 grounding、普通语义绑定、源码分歧、内部 D 和发布归并。其实际 provider schema 不含谓词字段，首轮、补全和纠错不要求谓词计划或执行结果。候选路由、谓词参数绑定、执行专属探针（含运行时 post-state frontier）、编译、backend 和 true 回执过滤整体关闭；`predicate_execution_receipts=[]`，语义证据使用 `semantic_evidence_record.v1`、W0/W1 和空 plan/receipt，不伪造执行失败。原有 native 初始迁移领域不变量、缺边发现和 guard 归并继续使用普通契约/模型引用；没有执行回执本身不使 cell 无效。

具体关闭/保留边界遵守[消融公约](../discover_matrix/docs/protocol/ablation_design_and_parallel_contract.md)。条件进入 manifest、worker、cell、pair status、summary 与 resume 合同；新 envelope 使用 manifest/status/summary v4 和 cell v10。旧 v3、cell v8/v9 可作为历史 full 只读解析，不满足新运行的恢复条件。模型/endpoint/token 配置以无凭据 hash 参与运行身份，不把 profile 名称相同视作配置相同。

本发布结构是可复用的 method package，不绑定任何单一实验运行或评测对照。具体运行的 input、resource、prompt/schema、run contract 和 source provenance 由调用方的 run manifest 与相应归档保存；这些外部评测材料不属于 method package 的输入读取路径。方法 source 的正式公开再分发仍需要权利人指定 LICENSE；[NOTICE.md](./NOTICE.md) 不构成此授权。

## 版本边界

本包只包含当前 12 条定义与实现，不提供旧编号别名或历史后端。历史运行的编号映射由论文工作区的 `evaluation` 处理；旧执行语义按对应历史 commit 复现，说明见[版本记录](../related_work/provenance/archive/pre_p1_20260905/README.md)。
