# v22 跑完之后才能动的项

`runs/paper1/matrix-v22` 在跑期间，pipeline 的 `src/` **冻结**：每个格子是一个新起的
`python -m` 进程，中途改源码会让后启动的格子用另一份代码，产出一次异质运行且没有任何提示。
由 [check_run_homogeneity.py](./check_run_homogeneity.py) 守住。

下列各项来自本轮三份 review，全部落在 `src/` 或依赖它，因此推迟到 v22 落盘之后。
**推迟不等于降级** —— 每条都写明了它属于哪一级、以及为什么现在不做。

## 必须在 v22 **报告发布前**解决（I 级）

### I-3 run record 不记录本仓库 commit，v21 与 v22 的记录无法区分

`vars_hash`（`assertions/runtime.py:357`）覆盖 model / inspect / source_mappings /
source_exclusions / registered_vars，**不覆盖** `exclusion_roles`，也**不覆盖** `inserted_states`。
实测 0047：带与不带这两者，`tool_env_hash` 都是 `9ab85ed7…`。`discover-run-started` 有
`pyfcstm_version`，没有本仓库的 commit。

所以尽管 `cardinality` 在 16 个 scope 上变了答案，**没有任何字段能把 v22 的记录与 v21 的区分开**。

- 现在的替代：`run_manifests.json` 在 eval 侧记下开跑 commit，`--verify` 核验运行期间源码未变。
  这够支撑 v22 的报告，但它是外部记账，不是记录自带的证据。
- 正解：在 `discover-run-started` 里记 `git rev-parse HEAD`。**不要**动 `vars_hash` —— 那会改变
  断言哈希，使历史 bundle 无法比对，代价大于收益。

### I-4 已在本轮解决

eval 全量自 `8f5cb3ba` 起就是红的（`test_a_false_resting_on_a_converter_owned_element_is_reported`
断言的是政策反转前的行为），而每个 commit body 都写「eval 侧 N passed」—— 那只跑了
`test_holdout_stays_clean.py`。已修，现 215 passed。**教训记这里**：报测试数时必须说清跑的是
哪个范围。

## M 级，不阻塞（按代价从低到高）

| 项 | 内容 | 为什么不是 I |
| :-- | :-- | :-- |
| M-6 | `vacuous_containment_findings` 在 `nodes.py:50` 被 import 却从不调用 | 按 import 数会数出 8 道门、实跑 7 道，只影响门数统计的读法 |
| M-2 | `if self.inserted_states:` 使「契约里零插入态」（格集内 `0000`/`0018`）与「无契约」不可区分 | 实测两条路径在全 60 pair / 627 个 state 上零分歧；改 `None` 哨兵更干净 |
| M-3 | `_ref_lookup_keys` 有 52 个退化短键（`segment:1`、`1`），`setdefault` 先到先得 | 实测 0/1712 走到它们 —— 键序「最具体优先」使长键总是先命中。但**那个顺序现在是正确性依赖，docstring 没写** |
| M-1 | `test_exclusion_roles.py` 的 fixture 对 `synthetic_state` 已按真实形状写，另三种 kind 仍是裸名（真实是 `variable:<n>` 33/33、`event:<n>` 387/387、`state:<n>` 60/60） | 后缀索引把它掩盖了 —— 而这正是它抓不到前缀回归的原因。同一类错误让 V4/V5 死代码活了一整轮 |
| M-7 | `test_verify_still_fails_on_a_burn_that_was_not_recorded` 原地改冻结的 `holdout.json` 再 `finally` 还原；SIGKILL 会毁掉一个写一次的制品 | monkeypatch `holdout.FROZEN` 到 tmp 路径即可 |
| M-1（公平性） | `_inserted_state_role` 兜底返回 `omission_surrogate`（可采），理由写的是「丢失发现的代价更大」—— 那是拿**自己的指标**当判据，不是中立的 fail-closed | 实测兜底命中 28 次全是 `UnspecifiedInitial`（语义上正确，是设计路径），**「配对失败」的真兜底命中 0 次**。理由不当、影响为零 |
| M-2（公平性） | `prompts.py:16` 的 `"exit the current mode/road/region"` 是所有 prompt 里最后一个带领域气味的词 | 不含元素名、不含期望真值、对所有 pair 一律生效（无集中度可解释）。但 vehicle 域横跨 `0029`/`0050`（调优格）与 `0032`/`0047`（留出格），换中性词更稳 |

## 结构性的一条，不是缺陷但要记住

**`initialization_anchored` 门把 `EIS-0047-03` 封死**（预注册 §9.1）。修法显然（把门收窄到行为类
谓词，因为 `edge_declared` 问的是模型**声明**了什么，而模型可以声明任何触发的 `[*]` 出边 ——
0047 的缺陷恰恰就是这个）。

**故意不在本轮修**：那会是「在准备运行的中途、由一条台账记录驱动的规则变更」。改为预注册，使
v22 若在该记录上未命中可归因到门而非能力。**下一代次可以改，但改之前要先想清楚它是否因此把
`EIS-0047-03` 烧掉** —— 修一道被某条记录暴露的门，与看着那条记录写规则，界线很细。

---

# v22 运行期间观察到的现象（run1，19 格）

**运行期间不得据此改代码**，这里只记录，供第 6 步根因分析与下一代次使用。

## 观察 1：`coverage=full` 33/33，零 coverage gap

v21 有 5 个 partial 格、15 条 coverage gap；v22 run1 **全部 full、零 gap**，`refuse@1`
2.45 → 2.23。这是测量能力的实质改善 —— 每一格都跑完了，没有格子因预算耗尽而只交出半份答案。

## 观察 2：`reaches(source=<伪状态>)` 在 fork/join 模型上大量发布

run1 的 62 条已发布 issue 里，**22 条**标题含伪状态名（`choice2`、`Junction1`、`fork2`、
`join2` 等），分布：

| pair | 条数 | 说明 |
| :-- | --: | :-- |
| `0018` | 18（claude 9 + gpt 9）| fork/join 家族 |
| `0038` | 3 | 同 NL 组 `53d65d24` |
| `0048` | 1 | 同上 |
| 其余八个 pair | **0** | |

**集中度有解释，所以不是特化的证据**：`0018`/`0038`/`0048` 就是 fork/join 家族，别的 pair 里
根本没有这些节点。这与「规则只在一个 pair 上生效」是两回事。

### 机制假说（未验证）

A1（`_reject_transient_subject`）挂在**主张槽**上：`occupancy_after` / `reaches` /
`response_within` / `persists_until` 的 target，以及 `stays_in` 的 source（那是它主张所在处）。
它**不拦** `reaches(source=<伪状态>, target=<真状态>)`。

而「从 `choice2` 出发能否到达 `TakePicture`」问的是一条**起点为伪状态的运行**，可伪状态在进入
的同一步就被离开，没有任何配置停在那里 —— 这与 A1 拦下的形态是同一个道理，只是落在 source 上。

### ⚠️ 若下一代次要动这里，先记清动机归属

这个观察**来自 `0018`/`0038`/`0048` 的产出**。那三格已按 A1 的动机烧毁（`e85dd257`），所以
据此写规则不会**新增**污染代价 —— 但动机必须如实记在规则的 commit body 里，否则下一轮的
灼烧审计会把它当成干净来源。按 §3.5.-1 手段 1，判据是动机而非拼写。

另外要先回答一个问题再动手：这 22 条**是多报吗**？标题看着像伪状态可达性主张，但
`0018` 的参考模型确实要求 fork 的两个分支都能落地。**先做人工判定，再谈修法** —— 上一代次
「先诊断后核验」的顺序反了一次，代价是根因诊断整条作废。

---

# v22 发布规格（第 5 步）

v21 的两个 gist 是完整的 —— `gh gist list` 显示「10 files」只是**列表页截断**，
`gh api gists/<id> --jq '.files | length'` 实为 34 与 43，三轮各 11 格齐全。核实过才敢照做。

v22 是 66 格，所以：

| gist | 文件数 | 内容 |
| :-- | --: | :-- |
| 可读 | 1 + 66 = **67** | `README.md` + `run{N}-<pair>-<profile>-readable.md` |
| 审计 | 1 + 66 + 附件 = **76±** | `README.md` + `*-audit.json` + `_*.json` 附件 |

审计 gist 的 `_*.json` 附件（沿用 v21 的构成并按本轮新增）：

    _verdicts_manual.json          人工判定表（含 direction 形态）
    _gate_refusals.json            count_refusals 输出
    _rule_surface.json             measure_rule_surface 输出
    _holdout_with_burn_record.json 冻结的 holdout.json
    _run_manifest.json             开跑 commit + 同质性核验结果      ← 本轮新增
    _model_drift.json              两条臂的模型代换审计              ← 本轮新增
    _rederived_admissibility.json  双报加法侧                        ← 本轮新增
    _v21_as_published.json         双报对照：v21 原值
    _v21_rederived.json            双报对照：v21 在当前谓词下重导出

发布前核对：`gh auth status` 的 token scopes 含 `gist`（已核）、活动账号是 `HansBug`（已核）、
PR #169 可访问（已核）。

## 观察 3：run1 完整（22/22），两臂 issue 数差异明显

    claude 33 条    gpt 48 条

除 `run1/0047-gpt`（partial）外全部 `coverage=full`。逐 pair：

| pair | claude iss/exc/obs | gpt iss/exc/obs |
| :-- | :-- | :-- |
| `0000` | 1/0/2 | 1/0/9 |
| `0006` | 2/0/0 | 3/0/0 |
| `0018` | 10/0/0 | 9/1/1 |
| `0029` | 6/0/1 | 5/0/0 |
| `0032` | **1/5/0** | 5/2/2 |
| `0035` | 5/0/1 | 4/0/0 |
| `0038` | 4/2/0 | **13/3/0** |
| `0043` | 2/0/0 | **0/0/0** |
| `0047` | 1/1/0 | 2/0/0（partial）|
| `0048` | **1/6/0** | 4/2/2 |
| `0050` | **0/0/0** | 2/0/0 |

## 观察 4：`EIS-0032-02` 在 run1 的唯一已发布 issue 上（**不是判定**）

`0032-claude` run1 只发布一条，而它的标题是

> Idle/Accelerating/Cruising/Braking 叶子状态并非直接位于 OperateState 之下，而是被多余的
> Region 中间层包裹

台账 `EIS-0032-02` 的 statement 是「NL 第 3 句只许一层子态…多出的 Region 包装层是 NL 与参考都
没有的元素，属过度规约」。**逐字对应，方向一致**。v21 run1 在这条上是未命中（`[0,1,0]`）。

⚠️ **这不是判定。** 判定要三轮齐、两臂齐，且要按 `HIT_CRITERION.md` §3 写出形态。这里只记录
一个结构性事实：那条记录在这一格出现在 `issues` 而非 `excluded_findings` 里。

同格另有 5 条 `representation_debt`，全是「X 收到 Y 后未占据 Z 叶子」的行为类主张 —— 正是 §十
量到「当前语义下 0/42 会被重新采信」的那一类（有 `exclusion_refs` 但不全是遗漏替身）。它们在
判定者眼里若只看 `issues` 会表现为「没发现」，而实际是「发现了但归因层判为表示债务」。这正是
`present_for_judgment.py` 被修好去呈现的东西。

## 观察 5：修订轮数分布健康

已完成格的最大修订轮数分布 `{0:3, 1:5, 2:9, 3:9, 4:10, 5:3, 6:2, 8:1, 9:1}`，平均 **3.1 轮**，
无格子耗尽预算被隔离。最久的 `0048-gpt` 跑 45 分钟、5 轮修订后走到 `bind_attribution` ——
慢在修订多，不是卡住。

## 观察 6：v21 run1 与 v22 run1 的同轮同臂对照

这是本代次唯一可直接对比的切面：同一轮次、同一条臂（claude）、同一格集。

| pair | v21 run1 claude | v22 run1 claude | Δissues |
| :-- | :-- | :-- | --: |
| `0000` | 1 iss / 0 exc / 0 gap · full | 1 iss / 0 exc / 0 gap · full | +0 |
| `0006` | 2 / 0 / 0 · full | 2 / 0 / 0 · full | +0 |
| `0018` | 4 / 2 / **9** · **partial** | **10** / 0 / **0** · **full** | **+6** |
| `0029` | 6 / 0 / 0 · full | 6 / 0 / 0 · full | +0 |
| `0032` | 1 / 0 / 0 · full | 1 / **5** / 0 · full | +0 |
| `0035` | 2 / 0 / 0 · full | **5** / 0 / 0 · full | **+3** |
| `0038` | 1 / **8** / **5** · **partial** | 4 / 2 / **0** · **full** | **+3** |
| `0043` | 2 / 0 / 0 · full | 2 / 0 / 0 · full | +0 |
| `0047` | 2 / 0 / 0 · **partial** | 1 / 1 / 0 · **full** | −1 |
| `0048` | 1 / 7 / 0 · full | 1 / 6 / 0 · full | +0 |
| `0050` | 0 / 0 / 0 · full | 0 / 0 / 0 · full | +0 |
| **合计** | **22** | **33** | **+11** |

### 最清楚的信号：partial → full，覆盖缺口 14 → 0

三个 partial 格（`0018` / `0038` / `0047`）全部变 full，覆盖缺口从 14 条降到 **0**。而 issue 数的
增长几乎全部来自这三格中的两格（`0018` +6、`0038` +3）—— 也就是说**多出来的发现主要是原本因
预算耗尽而没被交出的那批**，不是新的发现能力。

⚠️ 这**不等于**「命中变多」。`0018` 与 `0038` 都是**已烧毁格**，它们的发现进不了能力主张。而
`0035` 的 +3 在可报 pair 上，但要三轮齐才能判是能力还是采样。

### 八格 issue 数完全不变

`0000` `0006` `0029` `0032` `0043` `0048` `0050` 七格 +0，`0047` −1。这是有信息量的：本代次的修法
（Q1 角色翻转、Q2 计数外延、匹配器、对账）**在这些格上没有改变已发布数** —— 与 §十 量到的
「0/42 会被重新采信」一致，两条独立路径互印。

### `0032` 的 5 条排除是 v21 没有的

v21 run1 该格 0 条排除，v22 有 5 条 `representation_debt`。这不是「v22 多排除了」——v21 那一格
根本没产出这些断言（issue 数同为 1）。所以是**生产侧写出了更多行为类主张，而归因层判它们是表示
债务**。这条要在根因分析里追：多写出来的主张为什么全落在债务侧。

## 观察 7：两条臂的修订负担差近两倍，且集中在 `convert_assertions`

| 臂 | 格 | 平均最大修订轮数 | `convert_assertions` failed | `split_requirements` failed |
| :-- | --: | --: | --: | --: |
| claude | 33 | **2.4** | 18（0.5/格）| 14（0.4/格）|
| gpt | 33 | **4.6** | 26（0.8/格）| 8（0.2/格）|

两次触发 launcher 重试的格（`run1/0047-gpt`、`run2/0038-gpt`）都是 gpt 且都停在
`convert_assertions`。但**该阶段失败在两条臂上都常见**（claude 10 格、gpt 14 格的日志里出现过），
所以它不是 gpt 特有的失败模式，差别在**收敛速度**：gpt 需要更多轮才写出通过 precheck 的断言。

反过来，`split_requirements` 的失败 claude 更多（0.4 vs 0.2/格）——两条臂卡在不同环节。

### 与判定结果对照，这个差异有解释

gpt 在 `convert_assertions` 上多花的轮次，与它反复产出「要求一个自造具名元素」的形态一致
（`Inactive`、`Target_Search_Tasks`、`Accelerating_or_Cruising`、三个类别化 `*_Collision_Detected`）：
那些路径在模型里不存在，于是 precheck 拒、修订、再拒。而当它要求的名字**确实来自 NL**
（`auto_final`、`Join1`、`choice3`）时就一次通过并命中。

**所以「gpt 修订更多」与「gpt 命名施压」很可能是同一根因的两个面**：缺少一步「这个名字是 NL 给的
还是我造的」的区分。这条把观察 2（伪状态）、0050 的反例、以及这里的修订负担串成了一条线，是第 6 步
最值得先验的假设。

⚠️ 仍是**假设**。要验它需要看 `convert_assertions` 的 revision feedback 内容，逐条确认被拒的断言
是否绑了自造路径 —— 那是第 6 步的工作，不在运行期间做。

## 观察 8：Q2 的效果按预注册两个方向都落地了

预注册 §十一 在跑之前写死了推论：「v22 若仍报同形态的 `cardinality` 多报，那说明 Q2 没生效；
若不再报，那是 Q2 生效。两个方向都不触及 `EIS-0047-03` 的命中与否。」

实测（v22 三轮六格）：

| 扫描 | v21 | v22 |
| :-- | --: | --: |
| `detect_fabrications`：按当前谓词重算后站不住的已发布 issue | **3 条** | **0 条** |
| `0047` 各格里 `cardinality` 形态的多报 | 三轮全有 | **六格全无** |

v21 那 3 条是同一条 `0047-claude REQ-001` 在三轮里各一次，标题自己写着「含合成的
UnspecifiedInitial 子状态」。v22 该形态**彻底消失**，而 `0047` 六格仍各有 1–4 条已发布 issue ——
不是整格不产出，是那一类不再产出。

⚠️ **按 §十一 的限定，这只能算「精度侧的共演化观测」**：它证明 Q2 消除了一条已知多报，而「那是
多报」这个判断本身来自台账。作为方法有效性说明可以，作为样本外证据不行。且 `EIS-0047-03`
的命中（`run1/claude`）走的是 `event_consumed`，与 `cardinality` 不相干，两件事不互相支撑。

## 观察 9：加法侧在 v22 自己的产物上仍是 0

    被排除发现（断言级）56    当前语义下会被重新采信 0
      representation_debt / 至少一条排除项是 carrier   35
      unattributed / 有 refs 但不全是遗漏替身          20
      unattributed / 无 exclusion_refs                 1

与 v21 的 42 条相比，v22 的被排除面涨到 56 条，但**无 `exclusion_refs` 的只剩 1 条**（v21 是 13
条）。那 13 条正是 V1/V2 要救的对象 —— 现在几乎不再产生，与 `EIS-0018-01` 从 `unattributed` 迁到
`safe` 的逐格证据一致：**它们不是被重新采信了，是压根不再落到那个类别里。**

这解释了为什么回测式的 `rederive_admissibility` 两代次都报 0：它问的是「已产出的排除项是否会被
重新采信」，而 V1/V2 的实际作用发生在更早 —— 让发现根本不进排除项。回测看不见这种改变，只有
活体运行能看见。**这是本代次第三次撞上「回测测误伤面、活体测通用性」**（前两次是 0047 的门与
V1/V2 的下界解读）。


---

# ⚠️ 观察 10：更正 —— 「系统性方向反转」的判断是错的，那 27 条**有据**

上一轮我把 `0018` / `0038` / `0048` 三格反复出现的「Fork2 未被声明为 Join2 的直接子状态」判成
「模型系统性要求更多嵌套，而台账要求更少」，并称之为本轮最大的单一多报来源。**那个判断是错的。**

查 NL 原文（三格属同一 NL 组 `53d65d24`，第 11 句**逐字相同**）：

> 11. In the Fork2 state, **which is part of the Join2 substate**, the system can either proceed
>     to Junction2 or Flash. If the Flash state is activated, it transitions to Terminate.

**NL 明确说 Fork2 是 Join2 substate 的一部分。** 所以「Fork2 应是 Join2 的子状态」这条主张
**直接来自 NL 原文**，按 §13 的三分口径是**有据额外**，不是虚构。

## 我错在哪里

我拿台账当成了 NL 的代理。台账 `EIS-0018-02` 把 NL 11 读成「Join2 先进入 Fork2」（迁移关系），
而 NL 的字面是「part of ... substate」（包含关系）。**NL 这一句本身措辞含混，两种读法都站得住** ——
台账选了迁移读法，模型选了包含读法。

我先前的推理是「台账说 X 是缺陷 → 模型要求 X → 模型判反了」。这个推理把**台账的解释**当成了
**NL 的事实**。而 §13 的判据写的是「对着**模型文本与 NL**站得住」，不是「与台账一致」——
判据我自己写的，用的时候却换了个标准。

## 更正后的账

- 那 27 条「要求嵌套/包含关系」形态：**有据额外**，不计入 `over@1`
- `0048` 那条我标为「方向存疑待裁定」的，现在裁定为**有据**
- `EIS-0038-07` 的情形另论：台账说 Join2 的 pseudo 类型正确，而模型要求它是复合态 —— 但 NL 11
  说 Fork2 在 Join2 之内，一个 pseudo state 不能有子状态。**这是 NL 自身的不一致**（NL 8 让 Join2
  当汇合点，NL 11 让它当容器），不是模型的错。这条应记为**台账/NL 的已知缺口**，而不是模型多报。

## 方法学教训（比这条更正本身重要）

**判多报时唯一的依据是 NL 与模型文本，台账只是「已知缺陷清单」，不是「NL 的权威解释」。**
台账记的是它当时能支持的缺陷；它对某句 NL 的读法可以是众多合理读法之一。把台账当解释权威，会
把模型的另一种合理读法记成噪声 —— 而这恰好是 §13 那条「不采用的捷径」的变形：我没有用「台账外
= 多报」，但用了「与台账读法不同 = 多报」，效果一样。

已在 `verdicts/v22_manual.json` 与本文件就地更正（§3.6：改原件，不发更正件）。
