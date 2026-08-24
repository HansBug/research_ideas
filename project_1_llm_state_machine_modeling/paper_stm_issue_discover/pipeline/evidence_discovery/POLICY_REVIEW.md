# 当前方法口径审计记录

**审计日期：** 2026-08-21  
**审计对象：** `four-family-19-core.v1`、W1/W2/W0 契约、现行入口、旧内容归档和模块化重构计划

## 1. 当前唯一入口

| 内容 | 唯一来源 |
|---|---|
| 机器可读谓词注册表 | [`predicate_registry.json`](predicate_registry.json) |
| 人读谓词表 | [`PREDICATE_REGISTRY.md`](PREDICATE_REGISTRY.md) |
| 学术优先、W1/W2/W0 和变更门 | [`METHOD_PRINCIPLES.md`](METHOD_PRINCIPLES.md) |
| 来源三分类与出处政策 | [`method_provenance_policy.md`](../../discover_matrix/docs/protocol/method_provenance_policy.md) |
| 模块化施工顺序 | [`REFACTOR_PLAN.md`](REFACTOR_PLAN.md) |

当前配置为结构 6、拓扑 4、轨迹仿真 4、有界验证 5，共 19 个谓词。没有适用谓词时仍
提出问题并输出 W1；W1 可以进入外置 v3.2 评测且可被判为 FULL。W0 是无法精确绑定的覆盖缺口；
`UNKNOWN` 永远不能转成 violation。

现行 method/evaluation 边界已物理拆分：`evidence_discovery` 只负责发现、D/W、release、
W2 audit 和 method cost；L 只来自台账；正式 validity/relation/hit/FP/precision 只来自独立
冻结 `semantic-judge.two-stage.v3.2`。历史 run 中的内置 Judge artifacts 与数字保持不可变，
但不再进入新实验正式聚合。

## 2. 已完成的归档处理

- 旧 `witness_search_prototype` 及其旧设计已移入 `pipeline/archive/`。
- 旧出处政策、旧出处表和旧 contingency 预案已移入各自的
  `archive/legacy_20260821/`。
- 早期 `story/blueprint_proposal.md` 已移入 `story/archive/legacy_20260821/`，原路径只保留指针。
- 已作废且从未落地的 `wellformedness_attribution` 裁定、旧 `conditional_activation` 规则已移入
  `discover_matrix/docs/protocol/archive/legacy_20260821/`，原路径只保留指针。
- 历史 `fused_event_policy` 策略复盘也已移入同一归档目录，原路径只保留指针；其中关于
  `event_cardinality` 的历史扩张讨论不属于当前 19 个谓词。

归档材料可以追溯历史，但不能作为当前谓词、来源门、台账分母或新结果的定义来源。

## 3. 仍然存在但已明确隔离的旧材料

1. `pipeline/feedback_loop/` 在新包通过测试门之前仍是迁移期运行实现。其旧 S/B/P 词表和
   旧 API 只用于回放，不能生成当前四族结果，也不能作为新增谓词的依据。
2. `discover_matrix/docs/protocol/` 中的命中判定、人工台账和多报侧文件可能引用旧台账
   断言名。这些名称属于评测侧历史编码，已在相应文件顶部标明，不是公开谓词表。
3. `story/paper_outline.md`、`story/model_scope.md` 和相关出处审计仍保留历史迭代片段。
   它们现在以全局说明标出历史范围；其中的数字和旧谓词不能解释为新实现实测。

这些残留不是当前政策入口，也没有被注册表或新重构模块读取。

## 4. 学术叙事审查结论

- 四族按证据形态划分，不按台账类别反向切分。
- 台账或历史参考实现出场量只用于冻结后的表达力映射，不是来源证据或普遍率。
- 图路径不写成运行可行性，单条轨迹不写成全称性质，有限搜索不写成无界证明。
- `containment`、精确基数、并发运行时、层级优先级和轨迹变量差分保留 W1-only，不通过
  改名包装进入核心表。
- 来源登记尚未等于严格准入全部通过；未通过的命题保持 W1-only，不因覆盖率压力扩义或新增。
- 当前来源 ID 已逐条落到 [`related_work/provenance/CURRENT_SOURCE_AUDIT.md`](../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)
  和机器目录；G4、V1、V3、V4、R3 的保守状态已明确，不能把候选或超界资料写成 W2 来源门。

## 5. 可复核检查

本轮应至少执行：

```bash
python -m json.tool pipeline/evidence_discovery/predicate_registry.json
python -m pytest pipeline/evidence_discovery/tests/test_registry_contract.py -q
git diff --check
python tools/check_md_links.py project_1_llm_state_machine_modeling/paper_stm_issue_discover
```

局部 W2 或诊断集结果不能冒充 54x3 全量结论；正式全量能力数字必须由清理后冻结 method
产物与外置 v3.2 Judge 的独立 manifests 共同支撑。

## 6. 本轮 active 文档审计结论

2026-08-21 已对现行方法入口和会被论文/评测读者直接打开的协议做定向审计。结论如下：

| 审计项 | 结果 | 处理方式 |
|---|---|---|
| 当前注册表和人读表是否唯一 | 通过 | 只指向 `predicate_registry.json` / `PREDICATE_REGISTRY.md`，版本固定为 `four-family-19-core.v1` |
| W1 是否保留为合法发布证据 | 通过 | `METHOD_PRINCIPLES.md` 和测试均明确 W1 不因缺少谓词被丢弃，且 W 等级不作为 v3.2 FULL/validity 门 |
| W0 与 `UNKNOWN` 是否被误升格 | 通过 | 统一写明 W0 是 coverage gap，`UNKNOWN` 不得变成 violation；测试覆盖该边界 |
| 旧谓词和旧三族数字是否仍被当作当前方法 | 通过（历史文件除外） | active 叙事/协议在顶部标历史边界；旧设计、来源表和单体实现已移入 archive；评测侧旧断言仅保留为历史编码 |
| `prototype` 是否仍是正式方法名 | 通过 | 正式名只用 `evidence_discovery`；旧目录只能由 legacy replay / archive reader 访问 |
| 入口句是否把历史迭代数字冒充当前结果 | 已修正 | story 入口改为“历史报告只支撑历史结果；当前数字回到对应版本正式报告” |
| 来源严格门是否全部通过 | 未通过，且已显式保守 | 机器目录保留 `candidate` / `w1_only_*` 状态；未闭合命题只能 W1-only，不能写成 W2 来源依据 |
| 新四族代码是否已实跑 | 已完成局部冻结证据 | 新 `evidence_discovery` 已形成 method-only receipt 与不可变 release，质量结论由外置 v3.2 产生；历史 `feedback_loop` 不再是现行入口 |
| 新实现的效果目标 | 已按统一评测边界验证 | 在同台账、同发布边界、冻结 v3.2 和同分母下比较；参考实现不是逐格相等硬门，也不能靠放宽学术口径追平 |

本轮审计的自动门包括：注册表/来源目录解析、19 个谓词和四族计数、W1/W0/`UNKNOWN`
契约、来源路径、历史归档指针以及 active 入口政策标记。它们只证明口径没有被静默改写，
不替代逐条学术来源 review，也不把设计表达力快照变成运行结果。

## 7. 本轮新增硬约束审计

本轮已将以下要求冻结进 [`METHOD_PRINCIPLES.md`](METHOD_PRINCIPLES.md)、
[`REFACTOR_PLAN.md`](REFACTOR_PLAN.md) 和最终输出协议：

- 后端禁止 Python `inspect` 及旧 `inspect_*` 后端；类似能力必须由新包自有算法实现并
  记录算法版本与输入哈希。
- 谓词不支持不阻止发 issue；精确绑定但无法表达时必须降级 W1，W1 仍可进入外置评测；
  19 个公开谓词继续冻结。
- D2/D1/D0 由方法按照冻结语义裁定合同自行裁定；只有 D2/D1 参与 release，hit 和 FP 由
  外置 v3.2 产生，D0 只保留审计。W2/W1/W0 由确定性状态机计算，不能由模型口头指定。
- L 是台账侧属性，方法不生成 L；模型每一步、每条结构化输出必须带非空 `reason` 或
  `basis`。
- 新入口必须复用公共 `utils.agent`/`utils.llm` 与现有 respond/LangGraph，不能从
  `feedback_loop` 私有实现反向依赖；provider error 的原地重试和计费豁免、格子重试一次、
  其它错误计费的合同已经写入施工计划。
- 每条 W2 必须落盘完整谓词逻辑、绑定输入、编译源码及哈希、真实后端结果、终止状态、
  反例/轨迹、来源归因和 `reason`/`basis`，并在完成代码后用 `gpt-5.6-luna` 跑冻结的
  完整评测集，全量迭代到冻结历史参考实现量级验收门。

### 7.1 输入闭包和运行安全门

当前新包已恢复完整的 method 输入闭包和阶段骨架：编号 NL、PlantUML、
canonical source IR、exact source/transition inventory、working contract/mapping、
source trace、FCSTM/ModelIR、reference inspection-derived facts、owned inspection-equivalent
facts、verify facts 和 SMT summary 均进入 ContextManifest，并在每个 stage receipt
记录 manifest hash、artifact hashes 和版本。

PlantUML/source 与 FCSTM/closed model、inspection/verify/SMT facts 的角色分离已写入
prompt 和测试。case report 的完整历史阶段与 LLM/comparison/review payload 不进入
method prompt，只保留身份/状态 projection；完整文件仍以 hash 留在输入 receipt。
method 流程为 `prepare -> contract-extraction -> discovery-grounding -> execute-batch ->
d-adjudication -> validate-d -> publish`；structure/contrast 与 behavior/consequence 是 discovery-grounding 内两个同 schema、同 cross-view closure 的互补 lens，
exact binding、compiler/backend 与 execution receipt 是 execute-batch 内部审计。

live runner 使用双门：任意真实 provider 调用要求 `allow_live`；预先登记的小规模诊断
复测只通过第一门。完整评测集的多轮全量还要求 `allow_full_live`，只能在 provider-free
契约检查及诊断集 review 后打开。既有 provider 与 audit
产物是只读诊断快照，不删除、不覆盖、不冷重跑；新结果进入独立 `run_id` 子目录。

method run manifest 冻结 commit、19 谓词 registry hash、method prompt/schema hash、pair
ContextManifest hash、workers、stream/timeout 和 retry policy；外置 v3.2 另有独立 Judge
manifest，冻结 Judge commit/protocol/prompt/schema、ledger 与 release source hash。
resume 同时校验 run ID、contract hash、schema、source provenance 与 pair input hash；不
兼容文件显式保存为 `stale_incompatible` 后重跑，不能混入指标。所有 JSON/Markdown
终态使用同目录临时文件加原子 rename，避免并发 worker 留下半写制品。

能力报告必须明确区分历史参考实现与 baseline 实现。冻结指标及其 provenance 只保存在
实验记录中；它们是全量结束后的对账参照，不是改变谓词、W/D 口径或隐藏失败格的理由。

### 7.2 确定性边界复核

采用冻结职责边界：NL 同义、指代、义务成立性、条件作用域、语义到 formal element
的对应和最强反驳属于 LLM semantic grounding / D adjudication；parser、AST、精确
mapping、图可达性、trace、SMT、hash、预算和终止状态才属于确定性代码。禁止用正则、
关键词、substring、词干、编辑距离、embedding 或字符串相似度从自由文本推出语义结论。
现行 `adjudication.py` 只消费 D LLM 输出的封闭 typed facts，再机械映射 D；不得读取或
比较 `expected`、`observed`、`strongest_rebuttal` 散文。

这些是契约和施工门，不代表 54 pair 实验已经完成或效果已经达标。旧
`feedback_loop` 中可见的 `inspect_model` 只属于 legacy replay，不能被新
`evidence_discovery` 入口调用；新包只消费已落盘的 reference facts，并以自有版本化
parser/AST/有限图算法产生 inspection-equivalent、verify 和 SMT 输入事实。
