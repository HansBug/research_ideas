# 证据发现模块化重构计划

## 1. 目标和边界

把历史上集中在 `prototype.py`（约 1.5 万行）和 `graph.py` 中的职责拆成可测试的
模块。重构后的正式包名是 `evidence_discovery`，正式方法名不再含 `prototype`。
本计划只迁移发现链路的职责，不改输入语料、台账分母或既有实验结果；新实现未通过
全部测试门前，旧代码只作历史复现。

重构必须先落地 19 个谓词注册表和 W1 语义命中契约，再逐步接入后端。任何旧的
containment、cardinality、并发运行时、层级优先级或轨迹变量差分逻辑，都不能因为
迁移方便而重新成为核心谓词。

### 1.1 效果对齐目标

这次迁移不追求逐格复刻历史实现，但要以历史 v27 正式结果作为工程量级参照：在冻结
相同台账、54 个 pair、最终 D1/D2 发布边界、独立 judge 和统计分母后，新实现应取得与
v27 **大体相当或更好**的 hit 和 FP/precision 表现。达到大体相当即可，不要求绝对完美或
逐格相同；若超过 v27 则记录为改进。该目标是“不能出现无解释的明显回退”，不是新增
谓词、放宽 soundness 或把 W1/W0/`UNKNOWN` 伪装成 W2/violation 的理由。

对齐评估至少要同时看整体、L2、D2×L2 的 `hit@1`/`hit@3`/`hit@all`、release
emission FP、precision、eligible rate、W0/W1/W2/`UNKNOWN` 分布和成本；不要求逐 pair、
逐轮或每个谓词的使用量完全相同。v27 参照报告、台账版本、judge 和比较容差必须在
正式运行前登记，不能运行后按结果选择参照物。若差异来自新四族的学术边界或 W1 fallback，
必须在对账中说明，不能用 benchmark 覆盖率反向改定义。

## 2. 目标目录树

```text
pipeline/evidence_discovery/
├── __init__.py
├── cli.py                         # 唯一命令行入口
├── registry/
│   ├── __init__.py
│   ├── model.py                   # 注册表、谓词、族和版本的数据模型
│   ├── loader.py                  # JSON 加载、哈希和版本选择
│   └── validation.py              # 19 行、族计数、唯一 ID、变更门校验
├── predicate_registry.json        # 机器可读唯一注册表（迁移前置真源）
├── inputs/
│   ├── models.py                  # NL、源模型、轨迹和绑定输入类型
│   ├── context.py                 # v27 输入闭包、manifest 和自有事实算法
│   ├── loaders.py                 # pair、PlantUML、fcstm、工作合同和事实加载
│   └── provenance.py              # 输入哈希、源位置和绑定回执
├── semantics/
│   ├── obligations.py             # 需求义务拆分和语义类型
│   ├── binding.py                 # NL 原句到模型元素的精确绑定
│   └── adjudication.py            # 方法自裁 D2/D1/D0、W0/W1/W2 资格与 UNKNOWN 传播
├── compiler/
│   ├── lowering.py                # 义务到 19 个原子/派生宏的编译
│   ├── support.py                 # 谓词支持、W1 fallback 和不支持原因
│   └── plans.py                   # 可执行检查计划及契约校验
├── orchestration/
│   ├── runner.py                  # 单 pair / 批量运行编排，不做语义裁决
│   └── runtime.py                 # 公共 runtime、超时、重试、usage 和计费
├── backends/
│   ├── source_static.py           # S1-S6 的封闭源模型检查
│   ├── topology.py                # G1-G4 的图投影检查
│   ├── trajectory.py              # R1-R4 的单轨迹仿真
│   └── bounded_verification.py    # V1-V5 的有界守卫/状态空间检查
├── evidence/
│   ├── receipts.py                # 终止回执、反例和 UNKNOWN 的统一格式
│   ├── witness_levels.py          # W0/W1/W2 计算和不可升级规则
│   ├── source_attribution.py       # 需求、模型元素、执行回执的四段归因
│   └── audit_bundle.py             # W2 完整谓词、编译源码、哈希、结果和理由审计包
├── reporting/
│   ├── findings.py                # issue、断言和证据链输出
│   ├── coverage.py               # expressibility、semantic_hit、W2 分开统计
│   └── export.py                  # JSON、审计包和人读报告
├── compatibility/
│   ├── legacy_reader.py           # 只读旧运行结果，不暴露旧谓词为新 API
│   └── schema_adapter.py          # 旧记录到内部记录的显式版本适配
└── tests/
    ├── test_registry.py
    ├── test_w1_hit_contract.py
    ├── test_lowering.py
    ├── test_backend_contracts.py
    ├── test_provenance.py
    ├── test_coverage_accounting.py
    └── test_prose_non_interference.py
```

## 2.1 最小数据契约

模块之间先传结构化记录，再接入真实后端。字段名是内部接口的冻结草案；实现阶段若要
修改，必须同步 schema、迁移说明和测试。

当前 v27 等价输入闭包由 ContextManifest 固定，至少覆盖编号 NL、PlantUML、canonical
source IR、exact source/transition inventory、working contract/mapping、source trace、
FCSTM/ModelIR、v27 inspect-derived facts、owned inspection-equivalent facts、verify
facts 和 SMT summary。每个 artifact reference 都记录哈希、schema/algorithm version、
producer、source role、reason 和 basis；缺失闭包时不得降级为三文件 prompt。

方法阶段固定为 prepare、NL contract extraction、两个互补 grounding 分支、exact
binding、19-predicate compiler/backend、execution receipt、D adjudication 和
deterministic W publication。case report 的历史 lineage、LLM、comparison 和 review
payload 只保留在 receipt，prompt 只接收身份/状态 projection。

| 记录 | 必填字段 | 生产者 → 消费者 | 不能承载的含义 |
|---|---|---|---|
| ContextManifest | pair_id、artifacts、sections、forbidden_inputs、manifest_hash | inputs → semantics / orchestration | 不得省略 v27 source/model/fact closure 或混用来源角色 |
| StageReceipt | stage_id、stage_name、input_manifest_hash、output_hash、context_budget、reason、basis | orchestration → audit/reporting | 不得把 provider/schema 诊断改写成 D/W 结论 |
| `NLContract` | `contract_id`、source quote、locus kind/names、property、expected/violation direction、evidence types、binding hints、reason、basis | NL contract extraction → 两个 grounding 分支 | 不得读取闭模型结果、提前声称 violation 或把复合句留成一个义务 |
| `GroundingDisposition` | `contract_id`、status、candidate_count、reason、basis | 两个 grounding 分支 → stage receipt | 漏项只能确定性补 unresolved，不得补 satisfied/miss/FP |
| `CandidateIssue` | exact contract semantic key、predicate_id?、predicate_inputs、element/source refs、expected/observed、reason、basis | model grounding → binding / compiler / reporting | 不得改写 contract 的 locus/property/direction，不能用邻近可执行事实替代原义务 |
| `ModelBinding` | `obligation_id`、`model_hash`、`element_refs`、`binding_kind`、`binding_status` | `semantics` → `compiler` / `evidence` | 不得把字符串相似当精确绑定 |
| `PredicatePlan` | `predicate_id`、`inputs`、`registry_version`、`soundness_fragment`、`assumptions` | `compiler` → `backends` | 不得写入旧谓词名或自行扩义 |
| `RawReceipt` | `plan_id`、`backend`、`terminal_state`、`verdict`、`counterexample`、`run_metadata` | `backends` → `evidence` | 不得自行决定 W 等级或发布 issue |
| `EvidenceRecord` | `obligation_id`、`binding`、`predicate_id?`、`witness_level`、`attribution`、`reason` | `evidence` → `reporting` | `UNKNOWN`、超时和错误不能改成 violation |
| `FindingReport` | `issue_id`、`obligation_id`、`disposition`、`witness_level`、`coverage_class`、`source_chain` | `reporting` → 导出 | 不得把 expressibility 当 W2 或把 W1 丢弃 |

其中 `element_refs` 必须包含源文件、稳定 ID 或路径和模型哈希；`source_chain` 至少能
回到需求原句、模型元素、计划和回执四段。`predicate_id` 可以为空：这正是没有适用谓词
时仍然输出 W1 的合法路径。

exact binding 同时检查候选是否引用一个已供应的 `contract_id`，以及 typed
`locus_kind/locus_names/property/violation_direction` 是否逐字段保持。该检查只处理 exact
ID 与封闭枚举，不解释自由文本；任何不一致都进入 W0/D_UNRESOLVED。开放世界的 NL
拆分、概念对应和义务方向仍由 LLM contract/grounding 节点判断。

`NLContract` 的原子性准入只使用结构化且可完美判定的规则：一个 transition property
至多一个 source/target/transition hint，guard/effect 各自只有一个规范化表达，且
property 与 violation-direction 的封闭枚举组合必须一致。多个 endpoint、初始化与行为、
endpoint 与 consumer/reachability 等独立性质必须拆成不同 contract。validator 不读取
quote、normative statement、名称或自由文本 reason；这些语义拆分由 contract LLM 完成，
错误时通过同一 structured call 的定向 schema feedback 修订。

所有模型辅助节点的输出 schema 都必须把 `reason` 或 `basis` 设为必填非空字段；该字段
只记录本步的依据和边界，D/W 等级仍由方法裁定器计算。`EvidenceRecord` 还必须记录
`d_level`（D2/D1/D0/D_UNRESOLVED），但不得包含方法生成的 `l_level`。

每个 LLM stage 的 `context_budget` 记录精确 prompt 字符数、调用前 token 估计、provider
实际 input tokens（可得时）、profile context window、max output、projection version 和
是否发生 runtime truncation。当前只允许显式 `stage-context-projection.v4` 和
`contract-grounding-projection.v1` 压缩重复材料；后者保留 typed semantic key、NL 锚点、
scope 和 binding hint 值，并用完整 contract stage output 的 hash 代替重复 reason/basis。
不得静默删节；确定性 stage 也必须记录 `deterministic-no-prompt`，不能用
`context_budget_exceeded` 伪装业务 miss。

每条 W2 的 `audit_bundle` 是可独立复核的最小闭包，至少包含：谓词 ID 与注册表版本、
完整谓词逻辑和绑定后的输入、编译后的 assertion/formal program 源码及其哈希、模型与
程序哈希、实际后端运行结果、terminal state、counterexample/trace、四段 source
attribution、运行/重试记录以及 `reason`/`basis`。后端不能只返回“模型说是 W2”。

## 2.2 W 状态转换和不可升级规则

```text
需求义务
  ├─ 无精确可复现绑定 ───────────────→ W0 / coverage_gap
  └─ 已精确绑定
       ├─ 无适用 sound 谓词或后端 ───→ W1 / semantic_hit
       └─ 有计划并执行
            ├─ 终止且回执满足 fragment ─→ W2
            ├─ UNKNOWN / 超时 / 工具错误 ─→ 保留 UNKNOWN 或执行失败
            └─ 反例 ─────────────────→ violation（仅在谓词契约允许时）
```

W1 不能升级为 W2，除非同一条记录补齐注册表版本、计划、封闭输入、终止回执和来源归因；
`UNKNOWN`、资源耗尽和后端异常也不能通过重命名或聚合器变成 violation。`semantic_hit`、
`expressibility` 和 `W2` 必须使用不同字段和分母。

`D2/D1/D0` 由方法自己的裁定模块给出，不能复制台账 D 标签；只有 D2/D1 进入 release
issue、hit 和 FP，D0 仅保留审计。D2 是明确违反义务且最强反驳不成立，D1 是两种与事实
相容的称职读法并立，D0 是设计选择或没有可陈述的违反义务。`L` 完全由台账侧提供，
方法不生成 L。

## 3. 依赖方向和职责边界

依赖只能向下流动：

```text
inputs → semantics → compiler → backends → evidence → reporting
             ↑           ↑          ↑
          registry ──────┴──────────┘
```

- `registry` 不依赖任何后端，也不读取台账；它只定义公开语义和变更门。
- `inputs` 只负责读取和溯源，不做语义裁决。
- `semantics` 不调用模型检查器；它只决定绑定是否足够精确以及是否进入 W1，并由方法
  自己裁定 D2/D1/D0。它不得读取台账 D/L 作为裁定输入。
- `compiler` 只能引用注册表中的 ID；不支持时返回结构化原因，不抛弃义务。
- `backends` 只产生原始回执，不能直接发布 issue 或修改 W/D 等级；后端禁止使用 Python
  `inspect` 或旧 `inspect_*` 后端，需要类似能力时使用自有、可测试、有版本的算法。
- `evidence` 统一处理终止、归因、UNKNOWN 和 W1/W2，不让单个后端自行发明等级。
- `reporting` 只消费已裁决的记录；覆盖率、semantic hit 和 W2 必须使用不同字段和分母。
- `orchestration` 只负责调用顺序、预算、隔离和落盘，不决定语义、不修改 W/D 等级；
  必须复用公共 `utils.agent` 的 respond/LangGraph runtime 和 `utils.llm` 的 registry、
  pricing、usage 基础设施，不从 `feedback_loop` 私有模块反向导入或复制计费/调度。
  `utils.agent` 内部为通用工具适配而存在的反射实现不属于证据后端；证据后端和输入解析
  不得直接依赖或间接调用这些反射结果来产生谓词证据。
- `compatibility` 只读旧结果并保留版本标签，不能把旧谓词注册为新 API，也不能反向依赖
  benchmark 或台账。

禁止反向依赖 `reporting → backends`、`registry → benchmark`，也禁止用字符串匹配在模块
之间偷偷传递谓词语义。

## 4. 从历史实现到新模块的迁移映射

历史 `prototype.py` 的模型类（`ElementObligation`、`GraphObligation`、
`TemporalObligation`、`EvidenceGoal` 等）迁移到 `inputs/models.py` 与
`semantics/obligations.py`，并改为引用注册表 ID；旧的五类 typed obligation 不保留为
现行概念。加载、哈希和 `load_pair` 迁移到 `inputs/loaders.py` / `inputs/provenance.py`。

`inspect_fcstm`、`compact_inspect` 等旧检查器不能迁移为新后端调用；源位置、字段和签名
解析必须在 `inputs` 中用不依赖 Python `inspect` 的自有算法实现，并记录算法版本；
`validate_semantic_grounding`、`validate_discovery_grounding`、NL 锚点和合同展开迁移到
`semantics/binding.py`；`derive_support_disposition`、`compile_evidence_goal`、
`compile_check`、计划校验迁移到 `compiler/`。

以 `_source_*_certificate` 开头的函数按谓词族迁移：元素/迁移/触发/守卫/效果到
`backends/source_static.py`，路径和可达性到 `backends/topology.py`，完整场景执行到
`backends/trajectory.py`，守卫和状态空间证明到 `backends/bounded_verification.py`。
containment、child count、consumer scope、正交区和 trace delta 的旧证书只保留在
归档回放适配层，不能接入新 registry。

`build_execution_certificate`、`normalize_check`、`select_finding_outcomes`、
`build_finding_records` 等迁移到 `evidence/` 与 `reporting/`；D 档裁决和历史实验协议
留在 archive 适配器，现行发布只接受统一回执和 W 等级。

`graph.py` 中的 `build_prototype_graph`、`run_graph` 和重试/预算控制拆为 `cli.py`、
`orchestration/runner.py`、`orchestration/budgets.py` 与 `evidence/receipts.py`；它们不能
再通过“prototype graph”作为正式 API 暴露。旧结果如需读取，必须经过
`compatibility/legacy_reader.py`，且适配过程不能把旧谓词名写回新记录。

## 5. 分阶段施工顺序

### 阶段 0：输入闭包和阶段边界

- 恢复完整 v27 source/model/fact closure，并明确 PlantUML/source、FCSTM/closed model
  和 inspection/verify/SMT facts 的不相混角色。
- 用 ContextManifest 固定每项哈希、版本、来源角色和 prompt 排除项。
- 让 fixture 证明每个 grounding 分支实际收到完整闭包；每个阶段产出 Pydantic
  StageReceipt 和非空 reason/basis。
- 用自有、版本化的 inspection-equivalent、finite verification 和 SMT normalization
  算法替代禁用的 inspect API。

退出条件：缺失闭包不能进入 method；角色边界、prompt 非干扰和 stage receipt 均有测试。

### 阶段 A：注册表先行

- 完成 JSON schema、19 行/6-4-4-5 计数、版本哈希和来源 ID 校验。
- 加载器拒绝重复 ID、未知族、缺少最小输入或覆盖字段的条目。
- 建立变更门测试，确保 benchmark 数据不能被 registry 读取。

退出条件：注册表测试全绿，所有现行文档只指向 `four-family-19-core.v1`。

### 阶段 B：语义绑定和 W1 fallback

- 先迁移 NL 锚点、模型元素绑定和语义裁决。
- 对无适用谓词、来源未过门或后端不支持的义务，输出完整 W1 记录。
- 为 W0、W1、W2、UNKNOWN 编写互斥测试，特别测试 UNKNOWN 不会变成 violation。

退出条件：即使所有后端关闭，需求仍能产生可追溯的 W1 semantic hit；没有义务被静默丢弃。

阶段 B 还必须实现 D 自裁定：台账 D 只用于评测切片，不能进入方法裁定；D0 只审计，
D1/D2 才允许发布。所有模型节点和结构化项都要通过 `reason`/`basis` schema 门。

### 阶段 C：结构与拓扑后端

- 先迁移 S1-S6，再迁移 G1-G4。
- 每个回执记录封闭输入、源位置、假设和终止状态。
- 增加 mutation 测试：改变元素、端点、触发、守卫或路径时只影响相应谓词。

退出条件：静态和图后端与历史 fixture 的语义等价性通过，且不把图路径写成执行证据。

### 阶段 D：轨迹与有界验证后端

- 迁移 R1-R4，明确单轨迹和调度局限。
- 迁移 V1-V5，明确输入域、搜索界限、反例和证明条件。
- 对 `deadlock_free`、`state_retained`、`response_within` 做边界回归，防止终止/保持/响应混义。

退出条件：每个 W2 回执可独立复核；工具错误、超时、UNKNOWN 和反例不可混淆。

### 阶段 E：归因、报告和兼容性切换

- 把 issue、断言、NL 原句、源模型元素和回执拆成独立字段。
- 分开输出 expressibility、semantic_hit、W1/W2 比例和后端失败原因。
- 加入 schema、来源归因、重复 issue、覆盖分母和 prose non-interference 测试。
- 编写旧结果读取适配器，但禁止新运行写入旧 schema 或旧谓词名。

退出条件：新包在固定 fixture、mutation、来源和报告测试上达到门槛；完成一次新旧
结果只读对账，证明旧归档结果没有被静默改写。

阶段 E 的新旧对账还必须包含 v27 量级对齐表：同一分母下列出新实现与 v27 的
hit/FP/precision、W 分布、eligible 和成本；“大体相当”按运行前登记的比较容差判定，
不以逐格相等或绝对完美为门；若新实现超过 v27，应同时报告改进。不允许只挑 L2 或只挑
precision 较好的切片报告。

阶段 E 还必须完成公共基础设施切换：新入口通过 `utils.agent`/LangGraph/respond 调度，
通过 `utils.llm` 统一 registry、pricing、usage 和 retry 记录；禁止从 `feedback_loop`
引用私有计费实现。provider error 只在同请求原地重试时免除前序 attempt 费用；若 provider
error 使格子死亡，原地重试该格一次；其它错误及由此触发的 retry 全部计费并作为实现缺陷
修复，不能通过整格冷重跑掩盖。

阶段 E 完成后立即使用 `gpt-5.6-luna` 对冻结的 54 pair 做一次全量实验。实验输出必须
落盘每个 pair/cell 的 W/D、reason/basis、重试和成本；随后修复错误并迭代，直至整体 hit
显著高于 baseline、L2 大部分成功命中、FP 不高于 baseline，且总体达到 v27 大体相当量级。
超过 v27 如实记录；不要求逐格复刻，也不允许为达指标新增谓词或放宽学术边界。

当前施工安全门分两级：任意真实 Luna 调用都必须显式通过 `allow_live`；诊断阶段必须
显式传入 pair IDs，且最多运行六个 pair。冻结 54-pair 三轮全量还必须额外通过
`allow_full_live`，该门只可在 provider-free 契约检查与 0004/0023/0029/0035/0046/0053
六 pair 单次复测完成 review 后打开。每次运行在用户给定目录下新建 `run_id` 子目录；
manifest 冻结 commit、registry/prompt/schema/input hash、workers、retry 和 stream 模式，
不兼容旧格移入 `stale/` 并重新生成，不能静默 resume，也不能以冷重跑替代故障修复。

效果对账必须把重构前 v27 与 X1v2 baseline 分开。v27 量级参考为 overall hit@1
276/435、overall hit@3 107/145、L2 hit@3 35/39、D2xL2 hit@3 30/34、release
precision 45.74%；X1v2 baseline precision 为 41.60%。这些值是第一轮稳定运行后的能力
分析参照，不是 provider-free 或六 pair 诊断的通过条件，也不能用来改写 19 谓词语义。

### 阶段 F：退役历史运行入口

只有阶段 A-E 全部通过，并完成一次完整 smoke run 后，才把旧目录标为不可运行的
历史复现包。归档代码可执行但不进入 Makefile、论文报告或新结果目录。

## 6. 必须保留的测试门

1. **注册表门**：19 个唯一 ID、四族计数、版本和来源字段完整。
2. **W1 合同门**：无谓词仍发布 W1 并计 `semantic_hit`，W0 不计命中。
3. **后端 soundness 门**：后端不得越过声明 fragment；UNKNOWN 不得升级。
4. **溯源门**：每条 W2 都有需求、模型元素、计划和终止回执四段链接。
5. **覆盖记账门**：118/145、35/39、603/741 只能作为冻结设计快照；实测分母另存。
6. **变异门**：修改一个模型事实不得让无关谓词或族产生同样回执。
7. **学术叙事门**：扫描文档，禁止把台账频率写成来源、把图路径写成运行保证、把旧谓词写成核心。
8. **兼容性门**：旧归档可回放，新入口不依赖旧 `prototype` 模块名。
9. **v27 量级门**：在预先冻结的同分母、同 judge 对账中，hit 与 FP/precision 没有
   无解释的明显回退；差异必须能由 W1/W2、来源边界、后端能力或表示债务解释。
10. **D/W/L 门**：D2/D1/D0 由方法自裁，只有 D2/D1 计入 release/hit/FP；W 由确定性
    状态机计算；方法不输出 L。
11. **解释与审计门**：每条模型输出有非空 `reason`/`basis`；每条 W2 有完整审计包，
    包含谓词逻辑、编译源码、哈希和真实运行结果。
12. **后端与基础设施门**：代码树无 Python `inspect`/旧 inspect 后端调用，新入口只复用
    公共 respond/LangGraph 与 `utils.agent`/`utils.llm` 基础设施。
13. **重试计费门**：provider error 原地重试且前序 attempt 不计费；provider error 致格子
    死亡时原地重试格子一次；其它错误和 retry 计费并留下可修复缺陷记录。

## 7. 第一阶段最小可运行夹具

阶段 A/B 不等待完整后端，先提交一组固定夹具，确保新包的接口可以开工：

```text
tests/fixtures/minimal_pair/
├── requirement.json       # 两条可绑定义务，一条无谓词义务
├── model.fcstm.json       # 一个状态、两条迁移、一个守卫和一条效果
├── expected_w1.json       # 无后端时的 W1 semantic_hit
└── expected_w0.json       # 缺失元素时的 W0 coverage_gap
```

最小夹具必须覆盖：结构谓词计划、一个拓扑计划、无谓词 W1、精确绑定失败 W0、后端
`UNKNOWN`、D0/D1/D2 自裁定和一个带四段归因及完整审计字段的 W2 假回执。后续 mutation
只改一个模型事实，并验证无关谓词不产生同样结果。

## 8. 新旧入口和 Makefile 切换条件

迁移期保留旧 `pipeline/feedback_loop/` 仅作只读历史回放。Makefile/CLI 的新入口必须
满足以下条件后才能成为默认入口：

1. 阶段 A-E 的测试门全部通过，且 `predicate_registry.json` 与来源目录校验通过；
2. 固定夹具、mutation、W1/W2、来源归因和 prose non-interference 测试全部通过；
3. 新旧结果完成一次只读对账，差异按版本和 W 等级显式落盘；
4. 新入口连续两次 smoke run 不把 `UNKNOWN` 变成 violation，也不丢失 W1；
5. 论文/报告入口已经只读取新 schema，旧 `prototype` 名称只能由 archive reader 读取。

在这些条件满足前，禁止把旧运行结果标成当前四族 W2，也禁止让旧模块被新包反向导入。

## 9. 每阶段开工模板

每个模块簇都按同一顺序施工，避免先复制旧单体再重新解释：

1. 先写该簇的输入/输出数据类和失败状态测试；
2. 从旧实现抽取一个职责簇，保留旧结果只读适配，不把旧命名带入新注册表；
3. 对正常、反例、超时和 `UNKNOWN` 各写一个 fixture，并运行 mutation 检查无关族不受影响；
4. 通过本阶段测试门后再接入编排器；
5. 记录新旧结果只读对账，确认旧归档文件没有被静默改写。

## 10. 开工顺序

实际施工从 `registry/model.py`、`registry/loader.py` 和 `registry/validation.py` 开始，
然后实现 `semantics/adjudication.py` 的 W1 fallback；不要先复制整份旧
`prototype.py`。每一步都先写契约测试，再迁移一个职责簇，最后删除新包对旧模块的依赖。
