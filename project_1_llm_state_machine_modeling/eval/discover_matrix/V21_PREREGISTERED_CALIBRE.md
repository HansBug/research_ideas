# v21 报告口径 —— 在结果产生之前写死

写作时间点：v21 的 33 格已开跑、**尚无任何一格产出可读结果**。代码 `fc25c232`。

这份文件存在的唯一理由是 [CLAUDE.md §3.5 第 4 条](../../../CLAUDE.md)：中途放宽命中判据、更改分母或剔除不利样本，属于「评测口径迁就结果」。v21 引入的 A1 会**系统性地改变分母**，所以它的记账方式必须先于结果确定，否则事后无论怎么选都无法自证清白。

---

## 一、A1 使三个 hold-out 格丧失能力主张资格

**事实**（`measure_rule_surface.py`，真 parser + NL 组归并）：

| | 结果 |
| :-- | :-- |
| A1 触发的 pair | `0018`、`0038`、`0058`（3 / 60）|
| 其中 hold-out | `0018`、`0038` |
| A1 的引入动机 | commit `e85dd257` 正文自陈：看着这两格在 v20 的 17 条恒假发现写的 |
| NL 组 `53d65d24` | `0008 0018 0028 0038 0048 0058` —— hold-out 成员 `0018` `0038` `0048` |
| 样本外触发证据 | **零**。唯一非 hold-out 的触发样本 `0058` 与前两者同需求文本、同参考模型 |

`holdout.py` 规则 3 的原话说明了为什么这里要按组而不按 pair id 算：*同一组意味着同一份需求文本与同一份参考模型，针对其一成员写的规则会作用于每一个成员 —— 这是 pair-id 拼写检查看不见的*。

**口径**：

1. hold-out 的能力主张收缩到 **4 格**：`0032` `0035` `0043` `0047`。
2. `0018` `0038` `0048` 的结果照常全量报出，但归入「**方法 + 样本共演化观测**」，与调优四格并列，**不进入任何能力主张**。
3. A1 的正当性只以两项陈述：机制论证（它是 `_reject_undiscriminating_root` 恒真拒绝的恒假镜像）与单元测试负控。**报告中不得引用任何 pair 数字为 A1 的通用性背书。**
4. 主口径仍按全量 33 格 / 34 条报，分解表须同时给「能力主张 4 格」与「共演化 7 格」两栏。

> 这不是把 hold-out 缩小以让数字好看 —— 收缩后能力主张的样本量下降，对结果只会更不利。

## 二、v20 基线必须机械重导出，并与原值并列双报

> ⚠️ **本节相对初版已反转。** 初版写「不重算」，理由是「用新门控回溯改写旧代次不是同一次运行」。经独立裁决推翻：不重算，v21 与 v20 就跑在两套断言可采性规则上，`hit@k` 的差值把「方法变好」与「判据变了」混在一起 —— 那正是 §3.5 条款 4 直指的 C 级形态。改写发生在**分析层**，不回写 `runs/`，所以「不是同一次运行」的顾虑不成立。

**口径**：

1. v20 的命中表与多报表各出两列：`v20 as published` 与 `v20 re-derived under v21 predicates`。**不静默替换。**
2. 重导出走 `build_gist.py <round_dir> <out>` → `detect_fabrications.py <out>/audit`（后者有 SystemExit 守卫，直接指向 raw round dir 会拒跑）。被击落条目按 `issue_id` + 断言表达式**逐条列出**，不给汇总数。
3. **重导出结果标为 v20 的下界。** §3.5 条款 3：回测量的是误伤面，不是通用性。它只回答「A1 会击落 v20 多少条已发布发现」，不回答「v20 在 A1 之下会不会改写出一条正确断言」—— 被拒的断言本会进入修订预算，producer 可能补出对的。不标注就等于让 v21 白占便宜。
4. 被击落的每一条按 [`HIT_CRITERION.md`](./HIT_CRITERION.md) §1 做**三分人工裁决**：(a) 捏造，从来不是命中；(b) **缺陷定位对、编码成了恒假谓词**，v20 仍记命中，且它是 A1 将付出召回代价的证据；(c) 存疑。**(b) 必须单独立账** —— 这是这次重算不至于自利的唯一保证。
5. `coverage_status` full→partial 只在分析层重算，**不回写 `runs/`**：§3.6 管的是已发布结论，不是原始运行记录。
6. ⚠️ **`62/196 = 31.6%` 与 `36/184 = 19.6%` 这两个数当前不可复算** —— 全仓不存在产生它们的脚本。在 `count_refusals.py` 落库并复现出来之前，报告里不得出现。

**另一处必须先说清的事实**：v20 **不是 33 格基线**。实测 `v20run1` 10 格、`v20run2` 8 格、`v20run3` 8 格 = **26 格**。历代对比必须逐格标出有效轮数；`n=1` 的格上 `hit@all` 不构成稳定性证据。

## 三、`over@k` 必须并列拒答率，`unsupported` 必须落盘

**问题**：A1 把原本 `False`（会发布为发现）的断言变成 `UnsupportedEvidence` → `outcome=invalid` → 走修复预算 → quarantine 成 `CoverageGap`。而 `over@1` / `over@any` 的分母是「格 × 轮」，不是发现条数。于是**精度侧指标单调改善而能力毫无提高**。全流程此前没有任何地方计 `unsupported`。

**口径**：

1. `over@1` / `over@any` 旁必须并列 **`refused@1`**：同分母（格 × 轮）下每轮平均被 gate 拒绝的断言条数。精度改善若伴随 `refused@1` 同步上升，则该改善**不得**表述为能力提升。
2. 每格的 `UnsupportedEvidence` 计数与拒绝理由分布写进 audit bundle，字段：

```json
"gate_refusals": {
  "total": 0,
  "by_rule": {"transient_subject": 0, "undiscriminating_root": 0, "vacuous_conjunction": 0},
  "requirements_losing_all_primaries": []
}
```

3. `coverage_status: partial` 的格数与 `coverage_gaps` 条数进总表。**A1 把发现变成缺口，缺口必须和发现一样显眼。**

## 四、烧毁记账落成可执行事实，而不是一份文档

> ⚠️ **本节相对初版已改。** 初版说「接受测试为红」。经裁决推翻：报告要诚实解释为什么排除 `0018`，就必然写下 `0018`，于是拼写检测器会永远翻红 —— 那个红色随即不再表示「有新情况」，检测器等于报废。更根本的是，一份文档挡不住 `metrics_at_k.py` 继续把三个烧毁格算进能力主张带；**口径必须是代码读得到的事实，不是散文**。

已落地：

| 位置 | 内容 |
| :-- | :-- |
| `holdout.json` | 新增 `burned`（逐 pair 记 mechanism / since_commit / evidence / records）、`reportable_holdout`、`reportable_judgeable_total`、`reportable_layer_coverage`、`reportable_layers_at_k`、`replacement_available` / `replacement_note`。**已冻结字段一字未动** —— 移动已冻结分母本身就是口径迁就 |
| `holdout.py --verify` | 改为与 `burned` 对账：已记录的烧毁通告后 exit 0，**未记录的命名仍 exit 1**；另加反向检查「burned 不得同时在 reportable_holdout 中」 |
| `test_holdout_stays_clean.py` | 命名检查主语改 `reportable_holdout`；新增 4 条 —— 二者划分冻结集、缩小后的分母可加和、每条烧毁必须有机制与证据、**未记录的烧毁必须 exit 1**（正控用已知被点名的 `0018`，否则绿灯与「检测器坏了」无法区分）|
| `metrics_at_k.py` | 两带改三带：能力主张 / **已烧毁 hold-out（共演化观测）** / 历史四格 |
| `cli.py` | A1 写入 `gate_ablation.non_ablatable_pair_motivated_gates`，附注它为何在措辞通用的前提下仍属 pair-motivated |

**代价如实记录**：hold-out 可判定条目 **23 → 9**，分层为 `wellformedness` 5、`nl_contradiction` 2、`nl_named` 1、`over_specification` 1 —— 按 `layers_reportable_at_k` 的 ≥4 阈值，**只有 `wellformedness` 一层仍可报，`nl_named` 从 10 条掉到 1 条，直接掉出报告资格**。

**无替补，且是结构性的**：候选池重算后只剩 `0058`，而它就属同一 NL 组；`--freeze` 会以 undersized 拒绝。本语料内不存在可用的替补 hold-out —— 这要写成方法学限制，不是本轮的运气问题。

---

## 复算入口

```bash
eval/discover_matrix/measure_rule_surface.py            # 两条规则的触发面与 NL 组归并
eval/discover_matrix/count_refusals.py <matrix_dir>     # 每格每轮的 gate 拒答计数与分桶（待建）
eval/discover_matrix/holdout.py --verify                # 与 burned 对账；已记录的烧毁通告后 exit 0
eval/discover_matrix/present_for_judgment.py v21        # 逐格并列呈现，供人工判定
eval/discover_matrix/metrics_at_k.py <verdicts.json>    # 只做算术，判定由人工给
```

---

# v22 追加口径 —— 同样先于任何 v22 结果写死

写作时间点：v22 代码已落但**尚未开跑**（`runs/paper1/matrix-v22/` 为空）。

## 五、⚠️ v22 已无能力主张带

按 §3.5.-1 手段 1（查引入动机而非拼写）逐条裁定后，四个可报 pair 中有三条记录参与了修法设计：

| 记录 | 烧于 | 动机证据 |
| :-- | :-- | :-- |
| `EIS-0043-01` | `0eb36a06`（V6）| commit 正文给了**期望结果**「0043 PumpControl 3 → 2 ← 三轮全 True 掩盖的缺陷会浮出」，而该记录的断言集里含 `cardinality(scope=PumpControl, count=3)`（作为 `recovered_unverified`；primary 是 `containment`）—— 规则改的正是那个调用的返回值。<br>⚠️ 上一版此处写「primary 断言逐字就是 cardinality」，不实 |
| `EIS-0047-02` | `0eb36a06`（V6）| 同 commit「0047 CAS 4 → 3 ← 三轮全发的多报会消失」—— 而判断「0047 发的是误报」本身需要台账 |
| `EIS-0032-01` | `23315498`（V4/V5）| 动机是根因分析的 M4，唯一落点是 0032 的四条 `representation_debt` 排除；该记录的 statement 明写那三条 compiler exclusion「这是缺陷的机器证据」 |

| `EIS-0043-02` | `3d0049c1`（initial_target 归因盲）| commit 正文自陈动机「0019 的缺初始边被采信…0019/0043/0053 只有一个走了不记录分支」，规则文本在 `predicate_api.py` 与其测试两处注释里点名 0043；而该记录的 primary 恰是 `initial_target(PumpControl, Region1)`，statement 写的就是「与 0019 标准不一致」 |
| `EIS-0047-01` | `fc25c232`（B1）+ `e45e01e0`（V6 角色边界）| 两处独立污染。① B1 正文与 `capability.py` 注释「0047 有真实三项条件」，用来划定 B1 不该拒绝的形状 —— 而该记录的 primary 正是 `all([state_declared(RearEnd.Idle), state_declared(Pedestrian.Idle)])` 这种跨非嵌套路径的合取；② `e45e01e0` 正文给出方向性期望「0047 RearEnd/Pedestrian 1 → 0」并据此改了角色边界，而该记录 statement 逐字点名 `InvalidInitialtr_0005 / tr_0009` |

`0035` 判**未污染**并显式记录裁定：它只出现在 V6 的受影响 scope 清单里（根 7→6），无方向性主张、不指向任何台账记录。**点名一个 pair 以记账它受某规则影响，与看着它的失败写规则，不是同一件事。**

**代价：**

| | v21 | v22 |
| :-- | --: | --: |
| 可报记录 | 9 | **4** |
| `wellformedness` | 5 | 1 |
| `nl_named` | 1 | 1 |
| `over_specification` | 1 | 1 |
| `nl_contradiction` | 2 | 1 |
| 达 `≥4` 阈值的层 | 1 | **0** |

⚠️ **首版此处写 6，漏了两条**，原因是对账按 pair 粒度：一旦某 pair 有任一记录被烧，该 pair 此后**任何**动机、指向**任何**其他记录的点名都自动过关。改为逐点名归属后 `EIS-0043-02` 与 `EIS-0047-01` 浮出。两条在科学上都是零成本 —— 6 条时同样无层达阈值 —— 这正是记录而非争论的理由。

对应地，规则 1（不得在 pipeline 源码 / 测试中被点名）此前**已被违反且检测不到**：`--verify` 的源码分支仍用枚举式匹配器。实测全六十个 id：裸 id 命中 269 处 / 18 个 id，枚举式只命中 6 个 id，**只有裸 id 能抓到的 139 处里零误伤**。所担心的 `L000-000018-`、`tr_0043` 因前导数字与下划线是 word char，`\b` 本就不成立。已统一为单一匹配器。

**所以 v22 不产出任何能力主张。** 全部数字只能作为「方法 + 样本共演化观测」报出。这条写在跑之前，不是跑完才发现。

记账已落成代码读得到的事实：`holdout.json` 的 `burned_records` / `motive_adjudicated` / `reportable_records`（已冻结字段一字未动）、`--verify` 按记录级对账（未裁定的点名仍 exit 1）、`metrics_at_k.py` 三带按记录级排除、`test_holdout_stays_clean.py` 新增三条断言把「无能力主张带」钉住。

## 六、V1 / V2 / V4 / V5 都改断言可采性，必须双报

`status == "safe"` 是进入 `issues` 的唯一闸门。这四条把 `unattributed` / `representation_debt` 转 `safe`，**直接抬高 `hit@k` 的分子而分母不变** —— 这是 §三（精度单调改善而能力未提高）的**召回侧镜像**。

按 §二对 v20→v21 的既有裁定，必须：

1. v21 用 v22 谓词**机械重导出**（`build_gist.py runs/paper1/matrix-v21/run{1,2,3} <out>` → `detect_fabrications.py <out>/audit`），与原值**并列双报**，并标为 v21 的**下界**（回测不模拟修订路径）
2. 历代对比表按修法逐条标注哪一代次起生效
3. `refuse@1` 与 `over@1` 并列，否则「归因层少吃发现」会被读成生产侧能力提升

## 八、V6 二次返工：计数与归因分家（`§七` 的口径已作废）

`§七` 按 `role == "omission_surrogate"` 过滤，仍然是错的 —— 它用**归因层的答案**回答**计数层的问题**。两者是不同的问题：

- **Q1 归因**：「基于这个元素的证据，能不能说作者的事？」→ 决定可采性
- **Q2 计数**：「作者**声明**了这个元素吗？」→ 决定外延成员

两者在 `FinalWait*` 上分道扬镳：它是作者写的嵌套 final 的忠实降级，所以证据**不可采**（carrier）；而作者在那里没有声明任何状态，所以计入会虚增。反过来在 `InvalidInitial*` 上也错：它的**存在本身就是缺陷**，证据应当可采。

实测代价（返工前）：`cardinality(0047.RearEnd, 1)` 返回 **True** —— 而 `EIS-0047-01` 的 statement 原话是「后两个复合状态实际为空」，并逐字点名那两个 `InvalidInitial` 作为空的机器证据。**谓词与冻结台账直接矛盾。**

### 契约里的正确判据

| 判据 | 对 Q1 | 对 Q2 | 实测 |
| :-- | :-- | :-- | :-- |
| `source_refs` 非空 | 对 1590 条降级正确，对 51 条插入态错 | 错 | 23/51 插入态有 refs，指的是**触发注入的源行** |
| `origin == compiler_owned` | 错（会毁掉 1131 个 `transition_segment` carrier）| **对** | 51/51 插入态皆 `compiler_owned`，0 条 `source_owned` |
| 配对段的 `generated_role` | **对** | 过细 | 23/23 可唯一定，零歧义 |

`synthetic_state` 自身不带 `generated_role`，它在配对的 `transition_segment` 上，而插入态名字里嵌着迁移 id，配对是机械的：

    invalid_source_initial_surrogate   9   InvalidInitial*      存在即缺陷 → omission_surrogate
    invalid_source_final_surrogate     4   InvalidFinal*        存在即缺陷 → omission_surrogate
    nested_final_completion_hold      10   FinalWait*           普通降级   → carrier
    （无配对段、名字无迁移 id）       28   UnspecifiedInitial   作者没写   → omission_surrogate

### 落地与量到的效果

- **Q1**（`exclusion_roles`）改读配对段 role：13 条角色翻转（`InvalidInitial` 9 + `InvalidFinal` 4，`carrier` → `omission_surrogate`）。⚠️ 这是**放宽可采性**，与 §六 同族，必须双报。
- **Q2**（新增 `inserted_state_paths`，独立函数、独立字段）：剔除面 12 → **51**（全语料），v22 十一格受影响 scope **16 个**。
- 矛盾消除：`RearEnd` / `Pedestrian` 作者声明数现为 **0**，`cardinality(...,1)` 返回 False。

⚠️ **首版此处写 22，错的**。测量脚本把 `0058` 当成 v22 格集成员（6 个 scope）、漏了 `0000`（0 个）。v22 的十一格是 `0000 0006 0018 0029 0032 0035 0038 0043 0047 0048 0050`，与 v21 实跑一致；`0058` 从未在这个格集里。这是「手写数字」被 §一 禁止的原因的又一次演示 —— 该脚本的格集是我打字打进去的，不是从 `holdout.json` 或 v21 run 目录读的。

v22 十一格逐 scope（全部子态数 → 作者声明数），共 16 个，`0000` 与 `0018` 无插入态因此不受影响：

| pair | scope | → | pair | scope | → |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `0006` | root | 2→1 | `0043` | PumpControl | 3→2 |
| `0029` | HighwayMode | 6→5 | `0047` | CollisionAvoidanceSystem | 4→3 |
| `0029` | UrbanMode | 6→5 | `0047` | CAS.RearEnd | **1→0** |
| `0032` | AccelerateRegion | 3→2 | `0047` | CAS.Pedestrian | **1→0** |
| `0032` | BrakeRegion | 2→1 | `0048` | fork1 | 3→2 |
| `0032` | IdleRegion | 2→1 | `0048` | Fork2 / Join2 | 2→1（各）|
| `0035` | root | 7→6 | `0050` | AutonomousMode | 4→3 |
| `0038` | Terminate | **1→0** | | | |

家族分布：`UnspecifiedInitial` 12、`InvalidInitial` 3（`0038` 1 + `0047` 2）、`FinalWait` 1（`0050`）。所以本轮 Q1 的 13 条角色翻转在这十一格里只触及 **3 条**，`FinalWait` 侧只有 `0050` 一格 —— 换言之两个修法在 v22 上的可观测面都很窄，这必须写在跑之前。

### 上一版被撤回的判断，撤回本身是错的

两轮前 docstring 说 `InvalidInitialtr_*` 是被剥夺豁免的替身；上一轮以「它们 `source_refs` 非空」为由撤回。**语义上第一次是对的**，错的是机械代理。教训不是「那个主张为假」，而是**一个机械代理在语料的一部分上与语义主张吻合，会被读成对该主张的确认**。

---

## 七、V6 的触发面按角色过滤后重测（⚠️ 已被 §八 作废，保留以便对照）

旧口径（按「在 `source_exclusions` 里」）报 8 个受影响 scope，实为 16，其中 **4 个剔掉的是 carrier**（`0038.Terminate`、`0047.RearEnd`、`0047.Pedestrian`、`0050.AutonomousMode`）—— 会就作者确实写了的元素数发布发现。

改按 `role == "omission_surrogate"` 过滤后重测：**12 个 scope，剔除的全部是 `UnspecifiedInitial`，零 carrier**。

| pair | scope | old → new |
| :-- | :-- | :-- |
| `0006` | root | 2 → 1 |
| `0029` | HighwayMode / UrbanMode | 6 → 5（各）|
| `0032` | 三个 Region | 2/3/2 → 1/2/1 |
| `0035` | root | 7 → 6 |
| `0043` | PumpControl | 3 → 2 |
| `0047` | CollisionAvoidanceSystem | 4 → 3 |
| `0048` | fork1 / Join2 / Fork2 | 3→2 / 2→1 / 2→1 |

⚠️ **「双向」是单调过滤器的一个可能后果，不是已证性质。** 规则严格单调（计数只会下降）；翻转方向取决于 LLM 选的 `want` 落在 old 还是 new 上，而 `want` 来自 NL。v21 全部 9 次 `cardinality` 调用 `want=3`，实际被触及的只有 2 个 scope，一正一反纯属两个 `want`/count 对齐的巧合，n=2 证不了性质。

---

# 九、v22 开跑前的最后三条（写于 `runs/paper1/matrix-v22/` 仍不存在时）

## 9.1 ⚠️ `EIS-0047-03` 被门结构性封死 —— 三条可报记录里有一条不可达

它的两条台账编码都绑 `source="[*]"`：

- primary：`edge_declared(source="[*]", trigger=…Collision_Detected, target=…CollisionAvoidanceSystem)`
- recovered：`event_consumed(source="[*]", trigger=…Collision_Detected)`

`initialization_anchored_findings` 不按谓词豁免，放行条件是 `anchors_at_initialization(...) and _trigger_can_fire_from_initial(...)`，后者要求 trigger 尾名命中 `_POWER_ON_HINTS = ("poweron", "start", "boot", "init", "reset")`。`collisiondetected` 不命中。实测四种 `behavior_phase` × 两种编码 **八种组合全部被拒**，而对照组 `Power_On` + `initialization` 放行：

| phase | 编码 | 触发可上电 | 被拒 |
| :-- | :-- | :--: | :--: |
| `initialization` / `operation` / `structure` / 未设 | `edge_declared` | ✗ | ✅ |
| 同上 | `event_consumed` | ✗ | ✅ |
| `initialization` | `edge_declared` + `Power_On`（对照）| ✓ | ✗ |

**该门的「误伤面 0」是回测假象。** `33f43b3f` 声称「全 19 轮语料核实…误伤面 0」，但那是在**已产出的绑定**上回测的 —— 历史上没有一轮在 `0047` 上写过这个形状，所以回测看不见它。这正是 §3.5 条款 3「回测测误伤面、活体才测通用性」的教科书演示，也是本仓库第二次在同一处栽跟头。`33f43b3f` 的那句断言须按 §3.6 就地更正。

**后果**：`nl_contradiction` 层的可报条目实际可达数为 **0**。所以

| | 记账上 | 扣掉不可达后 |
| :-- | --: | --: |
| 可报记录 | 3 | **2** |
| `over_specification`（`EIS-0032-02`）| 1 | 1 |
| `nl_named`（`EIS-0035-02`）| 1 | 1 |
| `nl_contradiction`（`EIS-0047-03`）| 1 | **0** |
| `wellformedness` | 0 | 0 |

**若 v22 在 `EIS-0047-03` 上报「未命中」，那不是能力缺口，是这道门的抑制。** 这条写在跑之前，跑完再写与事后找借口无法区分。

## 9.2 Q2 的基线必须是 v21 实跑口径，不是任何中间提交

| 口径 | 是否实跑过 | 剔除面 |
| :-- | :-- | :-- |
| **v21 实跑**（08-06 20:18）| ✅ | **无过滤** |
| `0eb36a06` V6（22:33）| ❌ 仅提交 | 51 元素（≡ 新口径）|
| `e45e01e0` 角色过滤（23:19）| ❌ 仅提交 | 28 元素 |
| `02539b82` 新口径 | 待跑 | 51 元素 / 格集内 **16 scope** |

实测：契约 `synthetic_state` 与排除表 `compiler:state:*` **两侧各 51，对称差为零**。所以相对 `0eb36a06` 新口径确是空操作 —— 但 `0eb36a06` 从未跑过，拿它作基线等于对着假想敌宣布战果。

**报告要比的是 v21 → v22，即 `0 → 51 元素 / 格集内 16 scope`。** §八 首版写的「12 → 51」两头都不是实跑口径，且单位不齐（12 是 scope、51 是元素），已就地更正为本表。归因通道的风险是实的：若 v22 与 v21 有差，「12 → 51」会诱导把它记到 Q2 头上，而 Q2 相对中间提交为空操作、相对 v21 才有效。

另如实记录一笔：为「消除」`cardinality(0047.RearEnd,1)` 的矛盾而去读 `EIS-0047-01` 的 statement，代价是烧掉了一条可报记录。矛盾是真的（相对 v21 实跑口径，`RearEnd` 的计数里确实含 `InvalidInitial`），但发现它的路径本身消耗了 hold-out 资格。

## 9.3 对账粒度第三次收紧：类别名 → 具体位置

三轮橡皮图章，每次都是同一错误的更弱版本：

1. **per-pair**：问「该 pair 是否有任一记录被烧」→ 一旦有，此后任何点名免检。
2. **per-site-name**：问「该类别是否被认领」→ 一条 `named_at: ["commit_body"]` 吸收该 pair 过去与未来**所有** commit-body 点名。
3. **per-location**（现行）：每处点名是一个 `commit:<sha>` 或 `src:<path>`，各自要一条带理由的认领。

第 2 版放过的实例：`EIS-0032-01` 的烧毁记 `since_commit: 23315498`，而**该 commit 正文里 `0032` 出现 0 次**（动机来自 v21 根因 M4）。这个错标的类别顺手吸收了 `0eb36a06` 正文里的「`0032` 三个 Region 2/3/2 → 1/2/1」—— 另一条规则、另一个动机，全仓没有任何裁定看过它。

逐位置裁定后，四个可报 pair 共 **39 处**点名全部认领，其中：

- **动机污染**（已烧对应记录）：`0eb36a06`→0043/0047、`3d0049c1`→0043、`fc25c232`+`e45e01e0`→0047、`f73d6dd8`→0035，外加四个源码/测试落点
- **台账构建**：`79aabb7a`、`d6889d16`（分母与缺口）、`ba77c8c3`（合并键 bug）、`94074e4e`（命中判据）—— 台账是评分标准本身，记录它对某 pair 说了什么不是对方法的污染，前提是冻结先于结果（已核）
- **记账**：`588184f6`、`8977f454`、`dbc2e265`、`52295b3c`、`02539b82`、`e75fcc9a` —— 记账本身必须点名，否则无法审计

### 两条实质裁定

**① `0eb36a06` 对 `0032` 不构成污染。** 公平性 review 判它「指向 `EIS-0032-02` 的主体」，按机械论证不成立：该 commit 改的是 `AccelerateRegion`/`BrakeRegion`/`IdleRegion`，而 `EIS-0032-02` 的三个 `cardinality` 调用全在 **`OperateState`** 上。`OperateState` 的直接子态就是那三个 Region（作者所写），插入的 `UnspecifiedInitial` 在 Region **内部**，所以 `OperateState` 的计数不变；其 primary 是 `containment`，Q2 过滤不触及。`EIS-0032-02` 因此保留可报。

**② `EIS-0035-01` 应当烧毁 —— 元素名泄漏，任何基于 id 的扫描都看不见。** `tests/test_root_anchored_gate.py:119` 写着 `initial_target(composite=MODEL_ROOT, child=f"{MODEL_ROOT}.DoorShut")`，而 `MODEL_ROOT = "llms_emp_feedback_final_0000"` —— **`0000` 没有 `DoorShut`**。全台账 `DoorShut` 只出现在 `0005`/`0025`/`0028`/`0035` 的八条记录里，而 `EIS-0035-01` 的 primary 逐字就是 `initial_target(composite=<root>, child=<root>.DoorShut)`。`f73d6dd8` 正文自陈该门是拿「台账里 12 条绑裸 root 的 assertion」校准的。

机械上该门不触及 `initial_target` 的 `composite`/`child` 绑定，所以实体结论不变；但**边界是看着这条记录划的**。代价：`wellformedness` 层可报条目归零。

这一类不能靠加检查抓 —— 泄漏的是元素名而非 pair id。落成的纪律是：**台账内容不得用于划定 gate 边界**，并在 `holdout.json` 里对每处点名要求带理由的认领（`test_every_claimed_location_carries_a_reason` / `test_the_detector_reports_locations_not_categories` 两条负控把它钉住）。

## 9.4 匹配器第七次收窄：裸 id 漏掉本仓库最常用的拼写

`\b0018\b` 在 `llms_emp_feedback_final_0018` 里**不成立**，因为 `_` 是 word char —— 正是上一版 docstring 用来否定 `L000-000018-` 的同一事实，反过来打在仓库自己的规范 pair id 上（`cli._formal_pair` 构造它、launcher 传它）。被删掉的枚举式本来显式带 `feedback_final_{pair}\b`。已改为 `(\b{pair}\b|_{pair}\b)`。

同时更正一个不可复算的数：上一版 docstring 报「裸 269 处/18 id、枚举式 6 id、只有裸 id 能抓 139 处」。这些数字在本 commit 与此前四个 commit 上、按 span/行/仅 src/仅 tests 四种计法**都不复现**。重测：

| 计法 | 处数 / id 数 |
| :-- | :-- |
| 裸 `\b{pair}\b` | 354 / 19 |
| 现行 `(\b{pair}\b\|_{pair}\b)` | 460 / 21 |
| 被删的枚举式 | 219 / 7 |
| 枚举式能抓、裸 id 抓不到的 span | 52 |

「零误伤」那半**确实复现**。教训是更锋利的那条：**一个未经测量的断言被一个经过测量的断言替换，而那个测量不可复算** —— 与它所修的失败同型。

---

# 十、双报的路径修好了，而它给出的答案是「没有变化」

## 10.1 上一版的双报路径结构上办不到

`detect_fabrications.py` 的 `scan()` 开头就是 `issues = artifact.get("issues") or []` 后接
`if not issues: continue` —— **只遍历已发布 issue**，没有任何分支读 `excluded_findings`。而双报
要测的恰恰是「条目从 `excluded_findings` 搬进 `issues`」这个方向。v21 三十三格实测：

    issues 88 | excluded_findings 42（unattributed 24 + representation_debt 18）
    excluded_observations 22 | coverage_gaps 15

那 42 条候选一条都进不了重导出结果。所以这条被预注册为公平性控制的路径**只能把 v21 的分子往下
调**，方向与它要控制的机制相反。§六 写「标为 v21 的下界」结论对（`v21' ≤ v21-under-current`），
但理由不对：写的是「回测不模拟修订路径」，那是 §二.3 对 A1 这类**收紧**规则的论证；这里的主因
更硬 —— 重导出器**没有任何机制**重新采信被排除项。

新增 [rederive_admissibility.py](./rederive_admissibility.py) 补上这条路径。

## 10.2 答案：**0 / 42**

| status（as published） | 重算原因 | 条数 | 当前语义下会被采信？ |
| :-- | :-- | --: | :--: |
| `representation_debt` | 至少一条排除项是 carrier，仍为债务 | 18 | ✗ |
| `unattributed` | 有 refs 但不全是遗漏替身 | 11 | ✗ |
| `unattributed` | **无 exclusion_refs**，需 V1/V2 的祖先/前置条件回退 | 13 | 本脚本不算 |
| | **合计会被重新采信** | **0** | |

这与代码正确性 review 独立算出的结论一致：13 条角色翻转在 v21 实际产物上**零判定变化** ——
含被翻转元素的绑定全部是 `unattributed`，由更早的分支就决定了，根本走不到角色判据那一步。

**所以 V4/V5 与 Q1 角色翻转的双报列，会与 as-published 列完全相同。放宽只是前向风险，不是
回溯性的抬高。** 这条写在 v22 出结果之前。

## 10.3 那 13 条无 refs 的，分布恰好落在已烧毁格上

    无 exclusion_refs：13 条，分布 0018: 4、0038: 9

而 [V22_PROGRESS.md](./V22_PROGRESS.md) 记的 V1+V2 救回 13 条，逐轮分布是
`run1/0018 ×2`、`run1/0038 ×7`、`run2/0018 ×1`、`run2/0038 ×1`、`run3/0018 ×1`、`run3/0038 ×1`
—— 合计 0018 共 4、0038 共 9。两条独立路径给出同一组数。

**这 13 条全部落在已按动机烧毁的 `0018` / `0038` 上，因此一条都不能计入能力主张。** V1/V2 在
可报记录上的效果，只能由 v22 的活体运行回答。

## 10.4 双报的正确命令

    build_gist.py runs/paper1/matrix-v21/run1 runs/paper1/matrix-v21/run2 \
                  runs/paper1/matrix-v21/run3 /tmp/v21-rederived
    detect_fabrications.py /tmp/v21-rederived/audit      # 减法侧：不再为 False 的已发布 issue
    rederive_admissibility.py /tmp/v21-rederived/audit   # 加法侧：会被重新采信的被排除发现

⚠️ §六.1 原来那条 `build_gist.py runs/.../run{1,2,3} <out>` 会被 shell 展开成三个路径，而旧版
`main()` 只读 `argv[1]` 与 `argv[2]` —— **run2 变成输出目录**、run3 被丢弃、`<out>` 从未创建，
且打印的是成功信息。已修（多轮 + 三种写入 `runs/` 的形态各一条负控）。

两条界的理由必须一起说，只说一条会被读成完整重表达：

1. 只在**已经产出的**排除项上重算。当前语义下生产者会走不同的修订路径，可能产出另一批断言。
2. 只重算可采性判定这一步。谓词返回值沿用冻结产物，不重新求值。
