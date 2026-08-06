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
- **Q2**（新增 `inserted_state_paths`，独立函数、独立字段）：剔除面 12 → **51**（全语料），v22 十一格受影响 scope **22 个**。
- 矛盾消除：`RearEnd` / `Pedestrian` 作者声明数现为 **0**，`cardinality(...,1)` 返回 False。

v22 十一格逐 scope（全部子态数 → 作者声明数）：

| pair | scope | → | pair | scope | → |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `0006` | root | 2→1 | `0047` | CollisionAvoidanceSystem | 4→3 |
| `0029` | HighwayMode | 6→5 | `0047` | CAS.RearEnd | **1→0** |
| `0029` | UrbanMode | 6→5 | `0047` | CAS.Pedestrian | **1→0** |
| `0032` | AccelerateRegion | 3→2 | `0048` | fork1 | 3→2 |
| `0032` | BrakeRegion | 2→1 | `0048` | Fork2 / Join2 | 2→1（各）|
| `0032` | IdleRegion | 2→1 | `0050` | AutonomousMode | 4→3 |
| `0035` | root | 7→6 | `0058` | 六个 scope | 2→1（各）|
| `0038` | Terminate | **1→0** | `0043` | PumpControl | 3→2 |

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
