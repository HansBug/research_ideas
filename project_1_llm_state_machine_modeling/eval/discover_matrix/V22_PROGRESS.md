# v22 实施进度与剩余工作

代码 `23315498`。全量 **1577 passed / 4 skipped**。**实验尚未开跑** —— 待过第 2 步的两份 review。

> ⚠️ **本文件初版有一处判断错误，已更正。** 初版称 V4/V5 被「需要把 working contract 的
> `elements` 接进 discover 层」阻塞。**那个阻塞不存在** —— `frozen.working_contract` 早已
> 在 `schemas.py:151` 定义，真实运行里就带 73 条 `elements`。核实后直接实施，见 §1 的 V4。
> 记在这里是因为「以为被阻塞」比「真的被阻塞」更容易让一条修法无限期搁置。

设计来源：[v21 根因分析 comment](https://github.com/HansBug/research_ideas/pull/169#issuecomment-5205900480)（三个独立 agent，每条过 `generality_check`）。

---

## 1. 已落库（三条，均在真实数据上验证过效果）

| id | 内容 | 实测效果 | commit |
| :-- | :-- | :-- | :-- |
| **V1** | 机器根外壳在祖先归因中透明：前缀回溯耗尽时锚到该前缀下的**直接**子元素 | 与 V2 合计救回 v21 三轮 24 条 `unattributed` 中的 **13** 条 | `935aa3ac` |
| **V2** | precondition 由自己的 expression 归因，不由所属 requirement | 同上；并消除「一条发现能否浮现取决于 dependent 是否被改写掉」这一不稳定性 | `c05587f8` |
| **V6** | 计数类谓词的外延剔除编译器插入的成员 | 8 个 scope 受影响，**双向**：`0043 PumpControl` 3→2（掩盖的缺陷浮出）、`0047 CAS` 4→3（三轮多报消失）| `0eb36a06` |
| **V4 + V5 前半** | 排除元素的角色由契约 `source_refs` 决定，替换两项叶名表 | 叶名表的**两个方向错误都在语料上量到**：10 个 `FinalWaittr_*` 被误判为占位（实为 carrier，会误免）、28 个 `synthetic:segment:N` 被漏判（实为替身，永远拿不到免除）| `23315498` |

V1+V2 的 13 条分布：`run1/0018 ×2`、`run1/0038 ×7`、`run2/0018 ×1`、`run2/0038 ×1`、`run3/0018 ×1`、`run3/0038 ×1` —— 与根因分析报的 M1 逐条吻合。

## 2. 已实现但**未接线**（一条）

**containment 空洞门**（`capability.vacuous_containment_findings` + 8 条测试）。

`containment(parent=P, child=P.X)` 恒真（全语料 567/567 True；v21 三轮嵌套写法 28 True / 0 False，跨层写法 0 True / 25 False）。

⚠️ **两次实现失败的记录，比修法本身更值得留**：

1. **谓词层拒绝是错的。** 我按设计在 `predicate_api.containment` 里加了拒绝，4 个既有契约测试立刻红 —— **直接子状态的路径必然是 `parent + "." + 段`，拒绝这个形态等于让 `containment` 永远无法返回 True**。形态不是缺陷。
2. **需求阶段的门不能单独接线。** 它要求 `source_context.nl_parent`，而没有任何 prompt 教过这个字段。实测接线后 **14 个绿测试转红**，全部报 `revised RequirementSet revision must increase` —— 生产者被要求补一个从未被描述过的字段，修复预算耗尽，整格被隔离。这正是本仓库撞过的「两道互斥的门夹死生产者」。

**接线前置**：① `prompts.py` 前置扫描补 `nl_parent` 的三值判定（sentence 的层级 / root / null）与两个方向的 worked example（模型比 NL 浅、模型比 NL 深）；② reviewer 加一条拒绝 `nl_parent` 缺失；③ 更新约十四个 fixture 的 requirement 契约。

## 3. 剩余修法与它们的硬依赖

| id | 内容 | 阻塞原因 |
| :-- | :-- | :-- |
| **V5 后半** | fail-closed 替身对**位置型**主张也是可采信证据 | 独立，可先做。前半（角色判据）已落在 `23315498` |
| **V7** | 拆 `unresolved_segment` 与 `taint_disagreement`；taint 判定移到归因之后 | 独立，可先做 |
| **V8** | 排除词表闭合性 | **必须在 V4 之后** —— 单独修匹配器会把 143 条 `safe` 里的 74 条（52%）当场变成 `representation_debt`，砍掉一半发布量 |
| **D2/D3/D4** | splitter 禁止性需求判据、reviewer 引文核查、极性段 + `stays_in` 假阳性 | 独立，可先做 |

### V4 的判据已在契约里验证成立

`working_contracts/*.json` 的 `elements[]` 带 `kind` / `source_refs` / `metadata.generated_role`。实测（pair `0032`）：

| kind | `source_refs` 非空 | 角色 |
| :-- | :--: | :-- |
| `opaque_event_projection` / `route_control_variable` / `transition_segment` / `state_body_text` / `transition_macro_root` | ✅ | **carrier**（作者写的东西的降级）|
| `synthetic_state` / `synthetic_transition` | ❌ | **omission_surrogate**（作者没写时的兜底替身）|
| `root_wrapper` | ❌ | **naming_wrapper**（无语义）|

全语料 1712 条零例外。**这不是新发明的判据，是契约生成器已经写在盘上的事实，只是被 `attribution_exclusions` 拍平成裸字符串时扔掉了。**

而现有的替代判据 `nodes.py:3474` 的 `_OMISSION_PLACEHOLDERS = ("UnspecifiedInitial", "FinalWait")` **两个方向都错**：`FinalWait` 的 `source_refs` 非空（是 carrier），当成遗漏占位会**误免**（`0050` 是唯一含它的 pair 且 v21 里 0 条 False，属**潜伏缺陷**）；`InvalidInitial*`（9 例）不在表里，**永远拿不到免除**。

## 4. v22 实验配置（runner 已备好，未跑）

- **11 pair × 2 模型 × 3 轮 = 66 格**。`gpt-5.5` 额度已恢复，**仅限实验用途**（见 memory `gpt-only-for-matrix-experiments`）
- 并行 8，失败自动重试 6 次、每次退避 90 秒
- 口径沿用 [`V21_PREREGISTERED_CALIBRE.md`](./V21_PREREGISTERED_CALIBRE.md)，另需**先于结果**追加三条：
  1. **V6 会同时改变已发布数与命中数且方向相反**（−3 多报 / +3 候选），必须双报
  2. **V8 会把 74 条 finding 的归因锚点从裸事件名迁到源迁移** —— 发布量不降但归因内容变了，历代对比表要标注
  3. **D2/D3 组改动在冻结 hold-out 上不可测**（`reportable_layers_at_k.over_specification = false`，实有 1 条 < 阈值 4）。可产出的证据只有机制论证 + 单元负控 + 共演化观测，**不得进能力主张**

⚠️ 根因分析给了一条具体建议：NL 组 `0505e363`（成员 `0004 0014 0024 0034 0044 0054`）同时含枚举闭合与 `remains…until`，携带 22 条 surplus 面里的 6 条，且与 `HELD ∪ TUNED` **交集为空**。其中 `0014/0024/0034` 已在 `holdout.json:run_pairs` 里，**跑它们不消耗任何 hold-out 资格**。要测「能不能表达多出物」，v22 格集应把其中一格加进来 —— 只跑现 11 格，这组改动的可观测面就是 1 条，等于测不了。（`0004/0044/0054` 未跑过，留作未来 hold-out 材料，不要动。）

## 5. 复算入口

```bash
eval/discover_matrix/measure_rule_surface.py            # 规则触发面 + NL 组归并
eval/discover_matrix/count_refusals.py <matrix_dir>     # gate 拒答与覆盖率代价
eval/discover_matrix/holdout.py --verify                # 与 burned 对账
eval/discover_matrix/present_for_judgment.py <代次前缀> # 并列呈现，供人工判定
eval/discover_matrix/metrics_at_k.py <verdicts.json>    # 只做算术，判定由人工给
```
