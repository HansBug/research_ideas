# 19 条谓词的引入动机审计：词表是不是照着 54 个 pair 的期望缺陷反推的

> ⭐ **本文件与 [predicate_provenance.md](./predicate_provenance.md) 回答的是两个不同问题。** 那份问「这 19 条谓词**凭什么成立**」（外部领域出处，三类分级）；本文件问「这 19 条谓词**当初为什么被写下来**」（引入动机，A/B/C/D 分级）。⛔ 两者不可互相替代：一条谓词可以有完美的领域出处，同时是照着某个样本的答案反推出来的。

> ⭐ **判据来自 `CLAUDE.md` §3.5.-1，逐字**：「最可靠的判据是查引入动机，不是列举形态：把每条规则的引入 commit 翻出来，看它是不是**因为某个具体样本没被发现才写的**。commit message 往往自己就交代了。」

> ⚠️ **本文件补的是一处真实缺口。** [../../discover_matrix/docs/generations/v23/motive_audit.md](../../../../discover_matrix/docs/generations/v23/motive_audit.md) 只审 v23 的三处 prompt 改动，[../../discover_matrix/docs/protocol/rule_provenance.md](../../../../discover_matrix/docs/protocol/rule_provenance.md) 只管合式性公理的盲态推导纪律 —— ⛔ **两份都不覆盖 19 条谓词自身的来源**。

## 一句话结论

⭐ **A 类 19 条 · B 类 0 条 · C 类 0 条 · D 类 0 条** —— ⭐ 19 条谓词全部由**两个** commit 引入，两个 commit body 都**机械可验地**不含任何 pair 编号、`EIS-` 或 `EXP-` 标识符，其自陈理由分别是「闭合词表 + S/B/P 三族组织」与「Family S 存在性维度的不对称」，⛔ 都不指向任何具体样本。

⚠️ ⛔ **但「commit body 干净」不等于「词表与台账无接触」，而这正是本审计最重要的发现。** 代码 docstring 逐字写着「See issue #170 for the derivation」，⛔ 而那份被指认为**derivation** 的设计文档 §2 谓词表里，**17 行中有 12 行**在「能证明的问题」列上挂了一个具体 pair 编号或一条台账记录 ID，覆盖 pair `0000` `0005` `0006` `0029` 共 **13 条 `in_scope=True`** 的现行台账记录。⭐ 这**不是 C**（详见 §C 专节的三条反证），⛔ 但它是**设计期台账可见性**，必须登记。

## 逐条表

⭐ 表按引入顺序排。⭐ 「#170 §2 挂钩」列是我机械扫描 Issue #170 §2 谓词表各行得到的（脚本见 §局限），⛔ 它**不是**分类依据，⭐ 而是同一条谓词的污染面披露。

| 谓词 | 引入 commit | 日期 | 类 | commit body 逐字依据 | ⚠️ #170 §2 挂钩 |
| :-- | :-- | :-- | :-: | :-- | :-- |
| `state_declared` | `3a5cb966` | 2026-07-27 | **A** | 「新增 discover/predicates.py：**17 个谓词的封闭词表作为唯一真源**，按 S（制品声明）/ B（运行时行为）/ P（量化性质）三族组织…」 | ⚠️ pair `0000`（引的是 **NL 原句**，非缺陷记录） |
| `containment` | `3a5cb966` | 2026-07-27 | **A** | 同上（同一 commit 引入 17 条） | ⛔ `EXP-0029-SH-001` |
| `initial_target` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⛔ 「**0029** 的『HighwayMode / UrbanMode 初始入口唯一性』**失败**即此类」 |
| `edge_declared` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⭐ **无** |
| `effect_declared` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⛔ `EXP-0006-EA-001` |
| `action_declared` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0005`（NL 原句） |
| `guard_distinguishable` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⛔ `EXP-0029-GC-001` |
| `cardinality` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0006`（NL 原句 `operates within three different state areas`） |
| `occupancy_after` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⛔ `EXP-0029-IT-001` + `EXP-0000-IT-001` + pair `0006` |
| `event_consumed` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⭐ **无** |
| `stays_in` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0005`（NL 原句 `在 DoorShut 执行 Cancel 时必须保持在 DoorShut`） |
| `variable_delta_after` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⭐ **无** |
| `reaches` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⭐ **无**（⚠️ 该行的 pair 痕迹只在**基础设施 caveat** 列：`path()` 守卫盲的实测） |
| `terminates` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0000`（`topology().root_exit_reachable` **实测值**，非缺陷记录） |
| `invariant` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0029`（**反面**例：「对同一顺序区域的兄弟状态写恒真式…0029 Claude 实际写过」） |
| `response_within` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⭐ **无** |
| `persists_until` | `3a5cb966` | 2026-07-27 | **A** | 同上 | ⚠️ pair `0006`（NL 原句「任务完成之前持续执行目标搜索」） |
| `variable_declared` | `c54974d8` | 2026-07-28 | **A** | 「此前 `variable` 只出现在 effect_declared / variable_delta_after 的**关系语境**，`trigger` 只在 edge_declared 中，**两者都没有纯存在性检查，而 state_declared 有**；**这个不对称**正是『NL 要求一个模型没有的量』无可检查形式、只能靠 `<undeclared>` 夹带的根源（Issue #170 §11.3）」 | ⭐ **无** |
| `event_declared` | `c54974d8` | 2026-07-28 | **A** | 同上（同一 commit 引入 2 条） | ⭐ **无** |

⭐ **同一 commit 引入多条的如实记录**：`3a5cb966` **一次引入 17 条**，`c54974d8` **一次引入 2 条**。⛔ 因此逐条的「引入动机」在字面上不可能彼此不同 —— ⭐ 这一点本身既是好消息（词表是**成套设计**的，不是逐条累加出来的，而逐条累加恰是反推的典型形态），⛔ 也是坏消息（**逐条 A 类的证据强度被摊薄**：真正被审计的只有 2 段理由，不是 19 段）。

### 两个引入 commit 的机械核验

⭐ 我没有只靠读，⭐ 而是对两个 body 做了标识符扫描，⭐ 结果为空集：

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2
for c in 3a5cb966 c54974d8; do
  git show --format='%b' --no-patch $c | grep -oE '(EIS|EXP)-[0-9]{4}[-A-Z0-9]*|\b00[0-9][0-9]\b' | sort -u
done
# 两个 commit 均无任何输出
```

### 引入 commit 的认定过程（为什么不是「后来修它的那个」）

⭐ 认定用的是 `git log -S<谓词名> --all --reverse` **限定到谓词文件**，取最早那个：

```bash
git log -S"<谓词名>" --format='%h %ai %s' --all --reverse -- '*predicates.py' '*predicate_api.py'
```

⚠️ **不限定路径会被噪声淹没**：`containment` `reaches` `terminates` `invariant` `cardinality` `initial_target` `stays_in` 都是普通英文词，在 `related_work/` 的论文正文与 project_ex1 的旧代码里早在 2026-03 就出现，⛔ 与词表无关。⭐ 仓库 2026-08-11 做过 `paper_stm_repair` → `paper_stm_issue_discover` 改名（`35eba126`），⭐ `--follow` 与 `--all` 已覆盖，⭐ 两个文件的完整历史都能连贯回溯到引入点。

⭐ **另查了前身概念，结论是不改分类**：`containment` 与 `cardinality` 在命名词表之前以「散文措辞」与「gate dimension」形态存在过 —— `92d74d94`（2026-07-21，`dimension == "cardinality"` 门）与 `6c3bcc41`（2026-07-26，splitter prompt 的 `Containment language:` 一段）。⭐ 前者 body 全篇无样本（「以 CoverageUnit、Root 和逐条断言替换旧批量检查协议」）。⚠️ **后者 body 末条逐字写着「增加断言、状态图和真实 0029 归因回归测试」** —— ⭐ 但同一 body 首条把该段能力描述为「补齐结构、关系、效果与层次行为的**通用**断言语义」，⭐ 且我对该 commit 全 diff 扫 `0029` **命中 0 次**，⭐ 落地的 prompt 文本是纯词法的（「phrases such as substate, inside, within, belongs to, or contains are structural obligations」）。⭐ 故记为**A 类，附一条 0029 邻接披露**。

## C 类专节

⭐ **C 类 0 条。** ⛔ 但本节不能就此结束 —— ⭐ 上表「#170 §2 挂钩」列披露的接触面是真实的，⭐ 下面把它量化，⭐ 并说明为什么它**不构成** C、⛔ 以及在什么口径下仍应折算。

### 接触面的精确范围

⭐ 代码 docstring 逐字：「**See issue #170 for the derivation**, per-predicate implementation notes and the infrastructure caveats.」 ⭐ 该 issue（`[paper1] Discover 谓词系统`，创建于 2026-07-27T11:10:37Z）§2 的三张谓词表里，**12 / 17** 行在「含义与能证明的问题」列挂了具体样本。⭐ 涉及 pair 仅 **4 个**：`0000` `0005` `0006` `0029`。

⭐ 旧 `EXP-xxxx-XX-nnn` 编号出自一份**已丢失并被重建**的台账（`152ecffd`：「建立 expected issue set —— 129 条可审计记录取代已丢失的旧台帐」），⭐ 但映射有台账自身的逐字背书 —— `EIS-0006-02` 的 statement 末句：「**与台帐 `EXP-0006-EA-001` 一致**」。⭐ 据此可定位到的现行记录如下，⛔ **13 条全部 `in_scope=True`，即全部计入现行能力分母**：

| pair | 现行记录 | `primary_predicate` | #170 §2 的挂钩形态 |
| :-- | :-- | :-- | :-- |
| `0000` | `EIS-0000-01` | `occupancy_after` | ⛔ `EXP-0000-IT-001` 被逐字引为 `occupancy_after` 能证明的缺陷 |
| `0000` | `EIS-0000-02` | `stays_in` | ⭐ 未被 §2 引用 |
| `0005` | `EIS-0005-01` | `edge_declared` | ⚠️ `stays_in` 行引其 NL 原句（DoorShut / Cancel 自环） |
| `0005` | `EIS-0005-02` | `containment` | ⭐ 未被 §2 引用 |
| `0005` | `EIS-0005-03` | `None` | ⚠️ `action_declared` 行引其 NL 原句（显示并更新烹饪时间） |
| `0006` | `EIS-0006-01` | `cardinality` | ⚠️ `cardinality` 行引其 NL 原句（three different state areas） |
| `0006` | `EIS-0006-02` | `effect_declared` | ⛔ `EXP-0006-EA-001` 被逐字引为 `effect_declared` 能证明的缺陷 |
| `0006` | `EIS-0006-03` | `terminates` | ⚠️ `persists_until` 行引其 NL 原句（任务完成之前持续搜索） |
| `0029` | `EIS-0029-01` | `containment` | ⛔ `EXP-0029-SH-001` 被逐字引为 `containment` 能证明的缺陷 |
| `0029` | `EIS-0029-02` | `guard_distinguishable` | ⛔ `EXP-0029-GC-001` 被逐字引为 `guard_distinguishable` 能证明的缺陷 |
| `0029` | `EIS-0029-03` | `edge_declared` | ⛔ `EXP-0029-IT-001` 被逐字引为 `occupancy_after` 能证明的缺陷 |
| `0029` | `EIS-0029-04` | `initial_target` | ⛔ `initial_target` 行逐字引「0029 的初始入口唯一性**失败**」 |
| `0029` | `EIS-0029-05` | `containment` | ⭐ 未被 §2 引用 |

### 为什么它不构成 C：三条反证

⭐ C 的定义是「**因为某个具体样本没被发现**才写的」。⭐ 三条事实与之相反。

**反证一：被引的记录当时不是「没被发现」，而是「被命中」。** ⭐ 同一份 issue 的 §10.10「8 格验收矩阵」把**全部 5 条**被 §2 引用的 `EXP` 记录列为**命中**，逐字：「期望缺陷判定 **10 / 10 命中**」，并逐行给出「命中所依据的谓词」（`EXP-0029-SH-001` → `containment`、`EXP-0029-GC-001` → `guard_distinguishable`、`EXP-0000-IT-001` → `occupancy_after`…）。⭐ 也就是说这些引用出现在**验收**语境，⛔ 不是漏检清单语境。

**反证二：时序上，验收矩阵在词表之后。** ⭐ Issue #170 创建 07-27 19:10（+0800）→ 词表 commit `3a5cb966` 07-27 21:28 → 8 格矩阵跑在 `048baafa`（07-28 20:59）。⭐ §2 的挂钩是设计期**预言**「这条谓词应当能抓住那个」，⛔ 不是事后按漏检清单补洞。

**反证三：词表的成套来源是语料聚合，不是台账。** ⭐ §1.1 的推导逐字是从 splitter **自发产出**读出来的：750 条需求上 `coverage_obligation.domain` 有「**317 个不同原值 / 归一化后 289 个**」，⭐ 而头部高频值本身就是谓词名 —— `transition`(147) `source event target transition`(87) `initial`(20) `state containment`(15) `guard distinguishability`(8) `declared effect`(7)。⭐ 该节结论逐字：「**把 `domain` 收成闭合枚举，不是让 LLM 学新东西，而是给它已经在做的事一个词表。**」 ⭐ 这是 B 类形态的聚合统计（⛔ 不含 pair 编号），⭐ 且它解释了词表的**成员构成**，⛔ 台账解释不了。

⭐ 同理，`c54974d8` 那 2 条的上位动机（§11.1）也是聚合统计 + **假阳性**治理，⛔ 不是漏检治理：「**60 / 60 pair 的作者自有变量表全空**…唯一的证据是『变量表为空』，而它对 60 个 pair 全都成立，**不区分任何东西**…**一条纯误报走完全流程，每道门都是绿的**」。⭐ 这条谓词是为了**堵住一个误报通道**才加的 —— ⭐ 方向与「反推答案以提高命中」正好相反。

### ⛔ 仍应登记的折算口径（交裁定，⛔ 我不自裁）

⛔ 上述三条反证消解的是「C 类」这一指控，⛔ **消解不了「设计期台账可见性」这一事实**。⭐ 严格按 §3.5.-1 的精神（「把答案喂进去」的形态不止一种），⭐ 有一条最小折算口径值得考虑：**对那 5 条被 §2 逐字挂为「本谓词能证明」的记录，其对应谓词的能力证据打折**。⭐ 精确清单是 `EIS-0000-01`（`occupancy_after`）· `EIS-0006-02`（`effect_declared`）· `EIS-0029-01`（`containment`）· `EIS-0029-02`（`guard_distinguishable`）· `EIS-0029-03`（挂在 `occupancy_after` 名下）· ⭐ 外加 `EIS-0029-04`（`initial_target`，§2 逐字用了「失败」二字，⛔ 是全表唯一带负面结果措辞的挂钩）。

⛔ **这 6 条不得作为「该谓词在盲态下也会被写出来」的证据。** ⚠️ 但是否从 `hit@k` 分母中剔除，⛔ 是另一个问题：剔除会同时改变分母口径，⭐ 而 `CLAUDE.md` 的两项永久裁定明确区分了「按构造越界剔除」（`00x8`）与「按样本表现剔除」（禁止）。⭐ 本条属于第三种情形 —— **按设计期可见性剔除** —— ⛔ 现行 protocol 未定义它，⭐ 故我只登记、不执行。⭐ 若裁定为需折算，落点应是 [../../discover_matrix/docs/protocol/method_provenance_policy.md](../../../../discover_matrix/docs/protocol/archive/legacy_20260821/method_provenance_policy.md)，⛔ 不是本文件。

### ⭐ 一条对我方有利、但必须同时报告的观察

⭐ **接触面与证据强度呈反向分布。** ⛔ 上表 5 个 `EXP` 挂钩集中在 `containment` `effect_declared` `guard_distinguishable` `occupancy_after` `initial_target`；⭐ 而 [predicate_provenance.md](./predicate_provenance.md) 里领域证据最弱的两条 ③ 类是 `containment`（文献 1 源）与 `cardinality`（文献 0 源）。⭐ 二者只在 `containment` 上重合。⭐ 反过来，**5 条完全无挂钩的谓词**（`edge_declared` `event_consumed` `variable_delta_after` `reaches` `response_within`）里，`edge_declared` 有 15 个界内真实系统来源、`response_within` 有 19 篇文献 —— ⛔ 即「最干净的谓词恰好也是证据最厚的」这一说法**不成立**，⭐ 两个维度基本独立。⭐ 这与 [evidence_distribution.md](./evidence_distribution.md) 报的秩相关 **−0.562**（⚠️ ⛔ **该表述已作废** —— ⭐ 那个 rho 与语体解释共线、⛔ 无鉴别力，⭐ 见 [evidence_distribution.md](./evidence_distribution.md) §1.1）方向一致，⛔ 但那份用的是台账用量，本文件用的是设计文档引用量，⭐ 是两个不同的量，⛔ 不可互相引证。

## v25 那次 revert 的始末：纪律被真正执行过的证据

⭐ 这是本审计里**唯一**一次「有人试图新增一条谓词，且当场按引入动机做了自我排除，随后整个改动被否决」的完整记录。⭐ 它的价值在于：⭐ 它证明该纪律**不是事后叙述**，⭐ 而是当时就在运行、⛔ 并且真的拦下了东西。

### 时间线

| 时刻（+0800） | commit | 事件 |
| :-- | :-- | :-- |
| 2026-08-07 15:46 | `38f63681` | ⛔ v25 **第二次**尝试被撤：「撤销 v25 prompts.py L77 改动 —— **两份 review 各自独立判禁止开跑**」 |
| 2026-08-07 16:16 | `709d8125` | ⭐ v25 **第三次**尝试落地：issue 粒度消歧 + 新增谓词 `untriggered_edge_declared(source, target)` |
| 2026-08-07 16:34 | `3a60045c` | ⛔ **整个 commit 被 revert**（间隔 **18 分钟**） |

### 引入动机的自我排除（`709d8125` body 末段，逐字）

> 预注册补上了上一轮漏掉的「任何当前命中变漏检 → 净负面」一行；两变量的可观测签名互斥（每格 issue 数 vs 新谓词调用数），可分离归因；**按引入动机排除 EIS-0043-02 / EIS-0048-04 / EIS-0038-02 三条不计入能力**

⭐ 同一 body 里该谓词的正面理由是 B 类形态的聚合统计，逐字：「**矩阵语料 134/290 = 46% 的迁移不带触发**，无任何声明类谓词可作其主体」。⭐ 所以作者当时同时握着一条 B 类理由和一条 C 类污染，⭐ 并主动把后者对应的 3 条记录排除出能力口径。

### revert 的理由（`V25_PROPOSAL.md`，该文件即 revert 记录）

⭐ 该文件首行逐字：「**v25 提案：两处改动 —— ⛔ 均已撤销（两份运行前 review 各判禁止开跑）**」；第三行：「`git revert 709d8125`。**第三次 v25 尝试失败。两份 review 各自独立给出决定性理由，我全部接受。**」 ⭐ 六条 C 分两侧，⭐ 与本审计相关的是这四条：

**① 代码正确性侧 C3 —— 可计入上限实测为 0。** 逐字：「全台账 126 条中，期望断言真正需要『无触发边声明』的只有 **3 条**」，其中 `EIS-0018-02` **BURNED**、`EIS-0038-02` **BURNED**、`EIS-0058-01` 不在格内；「4 个可报留出格里 **0 条**；以 primary 身份出现 **0 条**。**净可计入上限 = 0。**」 ⛔ 并直指自证循环：「我那个『12 位』是从**漏检清单**数出来的，不是从可报集算出来的 —— §零 说它是『当前最大的杠杆』，§三 说构成它的记录不计入能力，**两节互相抵消**。」

⚠️ **注意这里有一处出入，我如实记录**：`709d8125` body 排除的是 `EIS-0043-02 / EIS-0048-04 / EIS-0038-02`，⛔ 而 revert 记录 C3 列出的三条是 `EIS-0018-02 / EIS-0038-02 / EIS-0058-01`。⭐ 两份清单只在 `EIS-0038-02` 上重合。⛔ 我未能查清这处不一致的成因（提案原文已被后续文档树化移除，只能从 `3a60045c` 的树对象里读到），⭐ 但两份清单**都**指向 `00x8` 族（`0018` `0038` `0048` `0058`），⭐ 而该族已按 `CLAUDE.md` 的永久裁定整体排除出评测网格 —— ⭐ 这与 C3 的结论「净可计入上限 = 0」方向一致。

**② 公平性侧 C1 —— provenance 锚错了。** ⭐ 这一条是本审计的直接先例，逐字：

> `RULE_PROVENANCE.md` 逐字：「**照着漏检清单写规则就是把答案喂进去的一种形态**」。而 `V23_REPORT_SKELETON.md` §十二之二 早已从**拒答统计**给出同一结论：`unsupported_binding` **92 条**，全部是 `'trigger' must be a non-empty path`，76/92 集中在伪状态族 pair …「该模型大量迁移**本就无触发**（伪状态间流转不带事件），生产者只能填空」**是否消耗 hold-out 资格：不消耗 —— 它是谓词表的设计问题，不针对任何具体样本**
>
> ⛔ **我用一个弱的、自证有罪的框架（照漏检清单数 12 位）替换了一个强的、已裁定的框架。**

⭐ 这段给出了 **B 类与 C 类同题异构**的教科书式对照：**同一条谓词需求**既可以从「漏检清单里有 12 位」（⛔ C 类，自证有罪）论证，⭐ 也可以从「92 条拒答全是同一条报错、76/92 集中在同族」（⭐ B 类聚合统计，不针对任何样本）论证。⭐ 后者更强，⭐ 且早已存在。

**③ 公平性侧 C2 —— 上限低于噪声底。** 逐字：「`V25_INSTRUMENT_ABLATION_PREREG.md` 已写死噪声底 **7.4pp**…合计 **15/204 = 7.4pp**，**恰好等于噪声底**；② 单独 5.9pp，**低于**噪声底。」

**④ 语义根因（C4）—— 新谓词会抹掉现有发现。** 逐字：「**我把 untriggered 与 unconditional 混为一谈。** `has_event=False` 只表示『无触发』，而我的 `meaning` 写『a missing **unconditional** step』。语料 134 条无触发边里 **46 条带守卫**，谓词对它们一律 True。」 ⭐ 实测两格：`pair 0043 initial_target(...) = False ← 现有发现` 而 `untriggered_edge_declared(...) = True ← 发现消失`。

### 这段历史对本审计的意义

1. ⭐ **19 条谓词之外的第 20 条曾被尝试，且没能进来。** ⭐ 词表在 `c54974d8`（2026-07-28）之后**十天**里保持 19 条不变，⭐ 而这十天里唯一一次扩表尝试留下了完整的否决记录。⭐ 「闭合词表」不是事后命名，⭐ 是真的闭合过。
2. ⭐ **纪律的执行方向是收紧而非放松。** ⭐ 作者主动排除了 3 条记录，⛔ 然后 review 进一步指出「排除之后上限归零、假设自动失败」。⛔ 没有出现「排除了就可以继续」的软着陆。
3. ⚠️ **但它同时暴露了一个反面事实：那次动机污染是真实发生过的。** ⭐ 若非两份运行前 review 拦下，⛔ 一条从漏检清单反推出来的谓词会进入词表。⭐ 这说明本审计对 19 条给出的 A 类结论，⛔ **不能被读成「这套流程不会产生 C 类」** —— ⭐ 它产生过，⭐ 只是被拦住了。

## 审计自身的局限

⛔ 以下每一条都会削弱上文结论，⭐ 按削弱程度降序。

1. ⛔ **最重的一条：19 条谓词只有 2 段引入理由，逐条 A 类是「成套推断」而非「逐条核验」。** ⭐ 我无法对 `event_consumed` 与 `containment` 给出**不同**的动机证据 —— ⭐ 它们共享 `3a5cb966` 的同一段 body。⭐ 因此「19 条全 A」的真实证据量是 **2 条**，⛔ 不是 19 条。⭐ 若要逐条硬证，需要的材料（每条谓词的独立设计推导）**不存在**。
2. ⛔ **`git log -S` 只能追踪字符串，追不到「概念先于命名」的情形。** ⭐ 我已查出 `containment` / `cardinality` 的散文与 gate 前身，⛔ 但**没有把 19 条逐一做这项前身排查** —— ⭐ 只对 `-S` 在谓词文件外命中过的 8 条做了。⭐ 其余 11 条的前身若以完全不同的措辞存在（例如某条 prompt 说「检查是否声明了 entry 动作」而不含 `action_declared` 字样），⛔ 我的方法看不见。
3. ⛔ **Issue #170 的 §2 是我读出来的接触面，⛔ 但我没有审它的**全部** 906 行。** ⭐ 我完整读了 §0.1 §1 §2 §8 §9 §10.10 §11.1–11.4，⭐ 机械扫描了 §2 谓词表全部 17 行；⛔ §3–§7、§10.1–10.9、§12 只读了标题。⛔ 那些节里可能有更多样本挂钩，⛔ 也可能有推翻我结论的内容。
4. ⛔ **`EXP-*` → `EIS-*` 的映射不是机械的。** ⭐ 旧台账已丢失（`152ecffd`）。⭐ 我的 6 条映射里只有 `EXP-0006-EA-001` → `EIS-0006-02` 有台账自身的逐字背书；⚠️ 其余 5 条是我按 statement 内容比对得出的（例如 `EXP-0029-SH-001` → `EIS-0029-01`，依据是「InitialState / HighwayMode / UrbanMode 未归属 AutonomousMode」与该记录 statement 同指）。⛔ 这些映射**须人工复核**，⛔ 若映射错了，§C 的折算清单就错了。
5. ⛔ **我没有查 prompt 通道里谓词**说明文本**的动机，只查了谓词**本身**的引入。** ⭐ 一条谓词的 `nl_index` / `nl_cue` / `examples` 是进 prompt 的，⛔ 而它们的改动动机可以是样本特化的。⭐ 实例已在手：`dfd4887e`（`reaches` 的 nl_index 重写）body 自陈「v38 实测：reaches 是全量 ① 类最大的一格（159 位里占 39）」⭐ 属 B 类聚合，⭐ 且明写「内容只从谓词语义推导，不引用任何语料元素、pair id 或台账措辞；diff 已过机械泄漏扫描」；⛔ 但其 revert `174c696d` 的 body 里出现了 `0007` `0005` `0027` `EIS-0007-01` 等具体样本。⭐ 两者都已回退，⛔ 故不影响当前词表 —— ⚠️ **但这说明「谓词说明文本」是一个独立于「谓词本身」的、我未系统审计的动机面。**
6. ⚠️ **`stays_in` 与 `persists_until` 在 2026-08-10 被做过实质语义修订**（`46beaff6` + `1befeed1`），⛔ 即当前这两条谓词的**判定语义**不是引入时的语义。⭐ 我核了这两个 commit 的 body，⭐ 动机是纯语义缺陷（「原编码 `check invariant <= N: (release) || active(state)` **不是 until**」、「在 A1->A2->A3 链上它答 True 而 occupancy_after 答 False，两个谓词对同一次运行给相反事实」），⛔ 无样本挂钩；⭐ 且 `e43a7b59` 事后补挂了领域出处（UML 2.5.1 §14.2.3.9.1 / Pnueli 1977 / Biere 2003）。⭐ 判 **A**。⛔ 但严格说，「引入动机干净」与「当前语义的修订动机干净」是两个命题，⭐ 我只对这 2 条查了后者，⛔ 其余 17 条没查。
7. ⛔ **本审计**自己**是在见过全部结果之后做的。** ⭐ 按 [rule_provenance.md](../../../../discover_matrix/docs/protocol/rule_provenance.md) 的逻辑，⛔ 事后审计无法产生「若我没见过样本会不会这样判」的反事实。⭐ 我能提供的只是**可复算的 commit 事实**（上文每条都附了命令或逐字引文），⛔ 不是盲态判断。

## 复算命令

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2

# 引入 commit 认定
for p in state_declared variable_declared event_declared containment initial_target \
         edge_declared effect_declared action_declared guard_distinguishable cardinality \
         occupancy_after event_consumed stays_in variable_delta_after reaches terminates \
         invariant response_within persists_until; do
  echo "### $p"
  git log -S"$p" --format='%h %ai %s' --all --reverse -- '*predicates.py' '*predicate_api.py' | head -2
done

# 两个引入 commit 的 body 标识符扫描（应为空）
for c in 3a5cb966 c54974d8; do
  git show --format='%b' --no-patch $c | grep -oE '(EIS|EXP)-[0-9]{4}[-A-Z0-9]*|\b00[0-9][0-9]\b' | sort -u
done

# 确认词表恰为 19 条
python3 - <<'PY'
import re
p='project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/predicates.py'
n=re.findall(r'Predicate\(\s*\n\s*"([a-z_]+)"',open(p).read())
print(len(n), n)
PY

# #170 §2 逐行挂钩扫描
gh issue view 170 --json body -q .body > /tmp/issue170.md   # 只读

# v25 revert 记录（文件已被后续文档树化移除，须从树对象读）
git show 3a60045c:project_1_llm_state_machine_modeling/eval/discover_matrix/V25_PROPOSAL.md | sed -n '1,135p'
```

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | 建立。19 条逐条引入动机审计：A 19 / B 0 / C 0 / D 0；披露 Issue #170 §2 的设计期台账可见性（12/17 行、4 个 pair、13 条 `in_scope` 记录）；记录 v25 `untriggered_edge_declared` 的自我排除与 18 分钟后的整体 revert。 |
