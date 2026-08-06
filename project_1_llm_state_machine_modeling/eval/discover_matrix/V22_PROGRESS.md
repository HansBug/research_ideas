# v22 实施进度与剩余工作

代码 `02539b82`。全量 **1580 passed / 4 skipped**，eval 侧 **21 passed**。**实验尚未开跑** —— 待过第 2 步的两份 review（前三轮均判「禁止进入运行」）。

口径与预注册以 [V21_PREREGISTERED_CALIBRE.md](./V21_PREREGISTERED_CALIBRE.md) 为准，本文件只记实施进度。

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
| **V6** | 计数类谓词的外延剔除编译器插入的成员 | 三轮返工后：全语料剔除面 **51**、v22 十一格受影响 scope **16**。见下方「V6 的三次口径」| `0eb36a06` → `e45e01e0` → `02539b82` |
| **V4 + V5 前半** | 排除元素的角色由契约决定，替换两项叶名表 | 判据经两次返工：`source_refs` → 配对段 `generated_role`。10 个 `FinalWaittr_*` 被叶名表误判为占位（实为 carrier）、28 个 `synthetic:segment:N` 被漏判（实为替身）、13 个 `InvalidInitial*`/`InvalidFinal*` 被 `source_refs` 误判为 carrier（实为替身）| `23315498` → `e45e01e0` → `02539b82` |

V1+V2 合计救回 13 条，分布 `run1/0018 ×2`、`run1/0038 ×7`、`run2/0018 ×1`、`run2/0038 ×1`、`run3/0018 ×1`、`run3/0038 ×1` —— 与根因分析报的 M1 逐条吻合。

⚠️ **三处数字更正**：① 13 条是 **V1+V2 合计**，V1 单独是 8 条 —— 上一版把合计写成了 V1 的功劳；② 13 条**全部落在 `0018` 与 `0038`**，而这两格已按动机烧毁，所以这 13 条不能计入能力主张，只能作为共演化观测；③ 契约 elements 是 **3125** 条 `model_refs` 解析、**1712** 条 `attribution_exclusions`，上一版把这两个数混用了。

### V6 的三次口径（前两次都错，记录以免再犯）

| 轮次 | 过滤判据 | 剔除面 | 错在哪 |
| :-- | :-- | --: | :-- |
| `0eb36a06` | 在 `source_exclusions` 里 | 16 scope | 表里也有 carrier，4 个 scope 会就作者确实写了的元素数报缺口 |
| `e45e01e0` | `role == "omission_surrogate"` | 12 scope | 用**归因层的答案**回答**计数层的问题**；`FinalWait*` 因证据不可采而被当成成员，`cardinality(0047.RearEnd, 1)` 返回 True 而台账说该 scope 是空的 |
| `02539b82` | 独立函数 `inserted_state_paths`，`kind == "synthetic_state"` | **51 全语料 / 16 在格集** | —— |

`FinalWait` 出现在 **5 个 pair**（`0002 0017 0026 0039 0050`），不是上一版写的「`0050` 是唯一含它的 pair」；`InvalidInitial` 出现在 `0004 0016 0033 0038 0047`。v22 十一格里只有 `0050` 含 `FinalWait`、`0038`/`0047` 含 `InvalidInitial`，所以 Q1 的 13 条翻转在格集内只触及 **3 条** —— 两个修法在 v22 上的可观测面都很窄。

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

### V4 的判据（⚠️ 下表的 `source_refs` 口径已被 `02539b82` 作废，保留以便对照）

`working_contracts/*.json` 的 `elements[]` 带 `kind` / `source_refs` / `metadata.generated_role`。实测（pair `0032`）：

| kind | `source_refs` 非空 | 角色 |
| :-- | :--: | :-- |
| `opaque_event_projection` / `route_control_variable` / `transition_segment` / `state_body_text` / `transition_macro_root` | ✅ | **carrier**（作者写的东西的降级）|
| `synthetic_state` / `synthetic_transition` | ❌ | **omission_surrogate**（作者没写时的兜底替身）|
| `root_wrapper` | ❌ | **naming_wrapper**（无语义）|

⚠️ **「零例外」只对降级类成立，对插入态不成立。** 51 条 `synthetic_state` 全是 `compiler_owned`，其中 23 条带 `source_refs`（指向**触发注入的源行**，不是声明）。正确判据是配对 `transition_segment` 的 `generated_role`，23/23 唯一可定 —— 见 [V21_PREREGISTERED_CALIBRE.md](./V21_PREREGISTERED_CALIBRE.md) §八。

**判据本身仍不是新发明的，是契约生成器已经写在盘上的事实**；错的是我读了盘上错的那个字段。

而现有的替代判据 `nodes.py:3474` 的 `_OMISSION_PLACEHOLDERS = ("UnspecifiedInitial", "FinalWait")` **两个方向都错**：`FinalWait` 的 `source_refs` 非空（是 carrier），当成遗漏占位会**误免**（`0050` 是唯一含它的 pair 且 v21 里 0 条 False，属**潜伏缺陷**）；`InvalidInitial*`（9 例）不在表里，**永远拿不到免除**。

## 4. v22 实验配置（runner 已备好，未跑）

- **11 pair × 2 模型 × 3 轮 = 66 格**。`gpt-5.5` 额度已恢复，**仅限实验用途**
- 格集**从盘上读**（[run_grid.py](./run_grid.py)），runner 与测量脚本都不再自带列表。上一版两处都是字面量，其中一处写进了 `0058`（从未在格集里）、漏了 `0000`，产出的错数进了预注册文档
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
