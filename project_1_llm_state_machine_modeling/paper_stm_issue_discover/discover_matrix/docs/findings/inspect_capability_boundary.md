# inspect 的能力边界：73 个码为什么只有 14 个开火

本文件固化 2026-08-13 一轮调查的长期研究事实：`pyfcstm inspect` 在本语料上到底能看见什么、看不见什么、以及**看不见的原因分别属于哪一层**。⛔ 施工进度、issue 状态、谁在做哪一项**不在这里**——按 [CLAUDE.md](../../../../../CLAUDE.md) §9 留在 GitHub。

调查的直接起因是一个猜想：inspect 可能是方法的核心突破点，故想知道该新增哪些静态检查项。⭐ **实测结论与出发假设相反：值得新增的检查项接近于没有，而未被消费的既有产出很多。** 这个反转本身是本文件要固化的结论。

## 〇、三个数，先给判据

| 事实 | 数 | 怎么复算 |
| :-- | :-- | :-- |
| `codes.yaml` 定义的诊断码 | **73**（error 22 / warning 43 / info 8） | 见 §五 |
| inspect **结构上**可能输出的 | **48**（全为 warning / info） | 22 个 `E_*` 经 strict sink 抛 `ModelValidationError`，另 3 个 combo 解析期码与 2 个 catalog-only 码被过滤 |
| 在 54 个 pair 上**实际开火**的 | **14** | §二的两组配置 |

⚠️ **「59 个码静默」不等于「59 个码没用」。** 静默的原因分三层，学术含义完全不同，⛔ 不可混为一谈：

1. **结构不可达**（22 个 `E_*`）——它们在**可解析**模型上按构造不会出现。⚠️ 这里面含领域文献点名的条款：`E_DUPLICATE_STATE` 对应 SDMetrics 的 `DupName`（标 `Correctness` + WFR）、`E_DANGLING_TRANSITION` 对应 Stateflow 的 dangling transition。**能力已实现，只是走致命通道、首个 error 即退出。**
2. **未被调用**（8 个 SMT 码）——见 §二，这是一个 CLI 参数问题。
3. **按构造空转**（守卫 / 数据流一族）——见 §三，这是语料属性，不是工具缺陷。

## 一、FCSTM 的父态出边不是成组迁移（本轮最重要的语义事实）

`pyfcstm/verify/topology.py` 的模块内注释逐字：

> "Parent-level transitions **are followed only when a descendant leaf explicitly exits to that parent; they are not copied onto every active descendant leaf.**"

⭐ 即：**在 FCSTM 里，复合态的出边对其活动子态不可用**；子态必须自己显式 `-> [*]` 退出到父态，才能接上父态的出边。这与 UML 的成组迁移语义**相反**——UML 里复合态的出边对全部子态可用。

最小验证（`Root.Outer.B` 是叶态、自身无出边，其父 `Outer` 有出边 `Outer -> Done : /Esc`）：

```
state Root {
    event Ev named "Ev";  event Esc named "Esc";
    state Outer named "Outer" { state A named "A"; state B named "B"; [*] -> A; A -> B : /Ev; }
    state Done named "Done";
    [*] -> Outer;  Outer -> Done : /Esc;
}
```

`pyfcstm inspect` 对 `Root.Outer.B` 报 `W_DEADLOCK_LEAF`，且 `--enable-verify` 下拓扑层独立报 `W_TOPOLOGICAL_NOEXIT` 且 `counterexample_kind = deadlock`。⭐ **两套独立分析一致**，故该报警**是正确的**。

### 1.1 由此更正一条曾被写成事实的错误断言

⛔ 此前 [inspectfindings.py](../../manual_review/relabel/inspectfindings.py) 的 `DEADLOCK_LEAF_CAVEAT` 断言 `W_DEADLOCK_LEAF` 有「**系统性假阳性**」，理由是 `analyzers/structural.py` 只数叶态自身出边、不做祖先遍历。**前半（代码不做祖先遍历）为真，后半（因此会误报）为假**——因为 FCSTM 里根本不存在可供子态使用的祖先边。

实测两侧都否掉它：

- **语料侧**：54 pair 上真实的 57 条 `W_DEADLOCK_LEAF`，其中「某个祖先有出边」的为 **0 条**。
- **语义侧**：上引 `topology.py` 注释 + §一的最小验证。

⚠️ **该错误未损伤既有数据**：57 条的 verdict 分布是 intrinsic 36 / projection_artifact 21 / **refuted 0**；全部 34 条 `refuted` 里 `W_DEADLOCK_LEAF` 一条都没有，且**零条**使用祖先论据。判读者确实执行了那道检查（`evidence` 字段里有「trap-1 外层出边检查」），它只是从未改变过任一结论。**故这是文档缺陷，不是数据缺陷。**

⛔ 但它已造成一次实际污染：本轮一个独立评审方原样引用该 caveat 当既有事实。**错误断言不会自我暴露，会被下游继承。**

### 1.2 与缺陷类型学的分工（⛔ 两条不要互相覆盖）

[defect_taxonomy.md](../protocol/defect_taxonomy.md) §3.5 对 `unintended_terminal` 写「判定测试必须把祖先的群迁移算进去」。⭐ **那一条是对的，不要改**——因为类型学的判定测试按 §3.0 全部落在**作者源 PlantUML** 上，而 PlantUML 读作 UML，成组迁移语义成立。

于是形成一条必须记住的分工：

| 判定对象 | 语义 | 「叶态无出边、父态有出边」 |
| :-- | :-- | :-- |
| 作者源 `stm0.puml` | UML（成组迁移**成立**） | **不是** terminal，须查祖先 |
| 编译产物 `model.fcstm` | FCSTM（父态出边**不下传**） | **是** terminal，无须查祖先 |

⛔ **不得用 UML 侧的祖先论据去推翻 FCSTM 侧的诊断。** 同一个叶状态在两种语义下的 terminal 性**相反**，这是表示债务（见 [representation_debt.md](./representation_debt.md)）在终止性这一维上的表现。

## 二、配置天花板：579，且 `smt_linear` 已经够

⛔ `--enable-verify` **单独只跑 6 个结构算法**；8 个 SMT 检查另需 `--max-complexity-tier smt_linear`。

54 pair 实测：

| 配置 | 诊断总数 |
| :-- | --: |
| `--enable-verify` | **454** |
| `--enable-verify --max-complexity-tier smt_linear --smt-timeout-ms 10000` | **579** |
| 再加 `--max-complexity-tier smt_nonlinear_decidable` | 579（**零增**） |
| 再加 `--max-call-count-scaling linear_in_leaves` | 579（**零增**） |

⭐ **454 这个数与既有 [inspect_findings.json](../../manual_review/relabel/inspect_findings.json) 的 454 条逐码吻合**，故既有记录可复算；同时说明**该次运行漏了 SMT 档**。

净增 125 条只来自三个码，⛔ 而三者价值差异极大，**不可合并成一个「+125」来报**：

| 码 | 条数 | 性质 |
| :-- | --: | :-- |
| `I_EFFECT_GUARD_CONTRADICT` | 86 | ⛔ **纯表示债务**：86/86 的守卫皆形如 `R45RouteToken == <整数>`，效应皆为 `R45RouteToken = 0`（去掉该名后无任何其它标识符残留，取值跨 26 个常量）。这是投影路由方案的确定性指纹 |
| `W_COMPOSITE_INIT_INCOMPLETE` | 18 | ⛔ **零新增主体**：其 18 个 `composite_path` 与既有 `W_INITIAL_UNCONDITIONAL_MISSING` 的 18 个**完全相同**（交集 18、两侧差集均空）。属同一批的第二次观察，**非独立证据** |
| `W_TRANSITION_SHADOWED` | 21 | ⭐ **唯一真新增**，不涉令牌。落 7 个 pair（0019/0034/0039/0047/0050/0056/0059），成因 `duplicate_event` 11 / `unconditional_catchall` 10 |

### 2.1 `W_TRANSITION_SHADOWED` 与台账的关系：同一处，⛔ 但判词相反

台账与候选里记了 `nondeterminism` 或 `priority_conflict` 的 pair 是 `{0013, 0019, 0029, 0034, 0039, 0056, 0059}`（7 条记录）。pair 层面与上述 7 个重合 **5** 个，⛔ 但**逐条核对后只有 3 处指向同一状态**：

| pair | 诊断指向 | 台账点名 | 判定 |
| :-- | :-- | :-- | :-: |
| 0019 | `enter_hwy`，`duplicate_event` | `EIS-0019-01`：同一状态 `enter_hwy` 两条出边 | **同一处** |
| 0034 | `InMotion`，4 条 catchall | `EIS-0034-02`：三条完成迁移同出 `InMotion` | **同一处** |
| 0056 | `NoIntercept->Intercepted` | `EIS-0056-01` 逐字点名同一对边 | **同一处**（⚠️ 4 条里仅此 1 条机理吻合） |
| 0039 | `InitialState` 出边 | `DIFF-0039-04`：**根**的两条初始边 | 不同处 |
| 0059 | `enter_hwy`（HighwayMode） | `VU-0059-02`：`enter_urban`（UrbanMode） | 不同处 |

⛔⛔ **而这 3 处「同一处」的语义方向是相反的**：台账主张「两条边同时使能 → 不确定 / 优先级冲突」，`W_TRANSITION_SHADOWED` 主张「后声明那条被完全覆盖、**永不可选**」，即按声明序**确定地**只走一条。0034 最明显：台账说「不确定地落到三个阶段中任意一个」，工具说「后两条永远进不去」。

⭐ **定位重合，判决不重合。** 根因是 FCSTM 采用有序选择的确定语义，而 UML 允许真冲突。⛔ 故**不得**表述为「inspect 独立复现了台账的非确定性缺陷」；可表述的是「同一处被两种语义各自判为缺陷，但缺陷类型不同」。

⚠️ 0029 的漏检工具自己知道原因，但**不输出**：`result_kind = undecidable_skip`，`reason = "Prior transition trigger coverage does not prove runtime shadowing because a predecessor transition lacks a locally proven stable continuation."` ⛔ verify 层把 `unknown` / `timeout` / `undecidable_skip` 的结果**整体丢弃**，于是「零结果」与「零能力」在输出里不可区分。

## 三、守卫与数据流一族按构造空转（语料属性，不是工具缺陷）

| 事实 | 54 pair 口径 | 60 pair 口径 |
| :-- | --: | --: |
| `model.fcstm` 含 `def` 声明的份数 | **30** | 33 |
| 其中作者自己声明的变量 | **0** | **0** |
| 作者源 `stm0.puml` 迁移行带方括号的份数 | **7** | 10 |
| `model.fcstm` 带守卫的迁移 / 迁移总数 | 131 / 984 | — |
| 其中作者写的守卫 | **0** | **0** |

⚠️ 全部 33 条 `def` 行**逐字全同**：`def int R45RouteToken = 0;`；该名在 60 份 `stm0.puml` 中出现 **0** 次。故它是投影注入量，见 [representation_debt.md](./representation_debt.md) 例 2。

⭐ 直接后果：`W_DEAD_GUARD` / `W_GUARD_TAUTOLOGY` / `W_EFFECT_SMT_NO_OP` / `W_FORCED_GUARD_UNSAT` 在两种配置下**均为 0**，且这是**按构造**的——没有作者守卫可供求解。⛔ 因此在本语料上给 inspect 增加任何守卫语义检查（守卫两两可满足性、d-完备性推广）的收益**恒为零**，与实现质量无关。

⚠️ 对照：pyfcstm 自带 428 份 `.fcstm` 资产中 **83% 含变量声明**、19.2% 的迁移带守卫。故守卫类检查对 pyfcstm 的目标使用场景有真实价值。⛔ 但该批是**测试 fixture**，为触发各项检查而刻意构造，相对真实用户模型高估了变量密度——方向可用，绝对值不可用。

## 四、可触及面：74 / 165，不是 22 / 165

按 [defect_taxonomy.md](../protocol/defect_taxonomy.md) 的 `defect_reference` 轴，165 条可映射条目的分布是 `requirement` 138 / `language` 22 / `other` 5。

⛔ **不得把 22/165 = 13.3% 当作 inspect 的能力上限。** 因为 138 条 `requirement` 里有 **52 条**落在 inspect 已能算出**静态前件**的座标格上——典型如 `unintended_terminal`：终止性本身是静态可判的，只有「是否**有意**终止」要问 NL（SDMetrics 自己就把这一判断留给人）。

故：

| 口径 | 数 | 含义 |
| :-- | --: | :-- |
| 完全静态可判（`language` 且落已覆盖格） | 6 | inspect 独立即可结案 |
| `language` 但现有码未覆盖 | 16 | 静态可判，当前漏 |
| `requirement` 但静态前件可算 | 52 | ⭐ inspect 出前件、LLM 出定性 |
| `requirement` 且前件也不可算 | 86 | 纯 NL 侧 |

⭐ **可触及面 = 6 + 16 + 52 = 74 / 165 = 44.8%。** 这支撑一条比「谁找得多」更强的定位：**inspect 承担语言可判的那一片与语义前件，LLM 承担 NL 绑定那一片**，两者互补而非替代。

⚠️ 那 16 条「未覆盖」里最大的一格是 `element/trigger/extraneous` **6 条**，全部是同一缺陷类：初始迁移带触发，违反 UML 2.5.1 `Pseudostate::outgoing_from_initial` 逐字条款「The outgoing Transition from an initial vertex may have a behavior, but **not a trigger or a guard**」。⛔ **但它在 pair 层面零新增召回**：作者源上带触发初始边的 12 个 pair 是 `W_INITIAL_UNCONDITIONAL_MISSING` 的 13 个 pair 的**严格子集**，台账那 6 条所在的 5 个 pair **全部**已被后者覆盖。差别只在**座标归属**（现有码映到 `element/transition/missing`，而缺陷实为 `element/trigger/extraneous`）与**主体粒度**（主体层面另有 8 个复合态未被覆盖）。

## 五、复算命令

```bash
source venv/bin/activate     # pyfcstm 0.6.0
cd project_1_llm_state_machine_modeling/paper_stm_issue_discover/selected_seed_examples

# §二 两组配置（54 pair，排除末位为 8 的六个）
for d in llms_emp_feedback_final_*; do s=${d##*_}
  case $s in 0008|0018|0028|0038|0048|0058) continue;; esac
  pyfcstm inspect -i $d/model.fcstm --format json --enable-verify -o /tmp/a/$s.json
  pyfcstm inspect -i $d/model.fcstm --format json --enable-verify \
    --max-complexity-tier smt_linear --smt-timeout-ms 10000 -o /tmp/b/$s.json
done

# §三 作者变量为 0
grep -h "def " llms_emp_feedback_final_*/model.fcstm | sort | uniq -c   # 唯一一行 R45RouteToken
grep -l "R45RouteToken" llms_emp_feedback_final_*/stm0.puml | wc -l     # 0

# §一 最小验证：把上面那段 DSL 存成 t.fcstm
pyfcstm inspect -i t.fcstm --format json --enable-verify --max-complexity-tier smt_linear
```

⚠️ **本轮四方（主 session + 三个独立核算方）各自都在得出「0 / 从未 / 全部」之前算错过一次分母**：`glob` 匹配到 0 个目录而报「0 次出现」· `DupName` 假报 54 条（真值 0）· 方括号 52→7 · skip 24→3。⭐ **任何「0」结论前先打印分母**，这条已经不是偶发。

## 六、取证档位

| 结论 | 档位 |
| :-- | :-- |
| §一 的 FCSTM 父态出边语义 | **源码注释逐字 + 最小模型实测 + 两套分析交叉**（最高） |
| §一.1 的 57/0 与 refuted 分布 | **机械复算**，两个独立方各自跑出同一数 |
| §二 的 454 / 579 与三码构成 | **机械复算**，且 454 与既有记录逐码吻合 |
| §二.1 的「同一处 3 个」 | **人工逐条回原文**；⛔ 不得由 pair 号相同推得 |
| §三 的变量与守卫计数 | **机械复算**（两口径分列） |
| §四 的 74/165 | **机械复算**（座标格归属为我方推断，非文献判定） |
| pyfcstm 自带资产 83% 含变量 | **机械复算**，⚠️ 但样本是测试 fixture，有构造偏差 |
