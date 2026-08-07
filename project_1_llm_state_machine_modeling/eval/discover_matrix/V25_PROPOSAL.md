# v25 提案：两处改动 —— ⛔ **均已撤销**（两份运行前 review 各判禁止开跑）

`git revert 709d8125`。**第三次 v25 尝试失败。** 两份 review 各自独立给出决定性理由，我全部接受。

## 一、代码正确性侧的四条 C

### C1 我声称的「没有任何一处调和」是假的 —— 调和在我编辑处**下方 6 行**

`prompts.py` L110–127 是 `RESULT_ADJUDICATOR_PROMPT` 的追加块，**同一个字符串变量**：

| 位置 | 逐字 | 我的新句 |
| :-- | :-- | :-- |
| L110 | Grouping across Requirements is what makes the published count **a count of defects rather than of Requirements** | —— |
| L119 rule 2 | 判据：**would fixing that one place make both False results go away?** 是则并组 | 「即使一次模型修改能同时修好，也要分成两条」 |
| L126 worked example | **both primary assertions are False** … **One issue**，`requirement_ids` 同列两条 | 「it **never** merges two False primaries into one issue」 |

**逐字互斥**，且我的改动实质上**废除了整个跨需求归组功能**（`nodes.py:4290` 只把 False primary 留在
issue 引用里，故「多需求 issue」按构造必然含 ≥2 个 False primary）。四处配套设施一处都没同步：
`schemas.py:586`、`nodes.py:4417-4431`（强制 `shared_root_cause`）、`nodes.py:4256-4268`
（`thin_merge_warnings`）、`renderer.py:466`（`_merge_candidates` 已算好塞进裁决者输入）。

⛔ **我在提案里写的是「这三条都是无条件祈使句，且我读了各自的完整行文」。** 我读了三行就宣称不存在
调和，**没有往下看 6 行**。这是本会话第**三**次「声称某跨阶段矛盾存在而它不存在」，前两次都在 L379。

### C2 判定侧的修法已经存在，而且是我自己在同一次会话里写的

`ONEPASS_JUDGE_INSTRUCTIONS.md` §158 标题逐字：**「⚠️ 已知装置限制：一条 issue 陈述多条台账缺陷时会被
结构性低估」**；§187 规则：**「一条 issue 可以命中多条期望缺陷，写成 `hits:X+Y`」**；
`onepass_merge.py` 的 `hits_aliases()` 已支持；commit **`cd74380a`**。

⛔ **改动 ① 是改被测系统去迁就一个已经不存在的判定限制。** 我在正确的地方修好了，然后忘了，
又在错误的地方修了一遍。

### C3 改动 ② 的可计入上限实测为 **0**

全台账 126 条中，期望断言真正需要「无触发边声明」的只有 **3 条**：

| 记录 | 格 | 在 11 格内 | 状态 |
| :-- | :-- | :-- | :-- |
| `EIS-0018-02` | 0018 | 是 | **BURNED** |
| `EIS-0038-02` | 0038 | 是 | **BURNED** |
| `EIS-0058-01` | 0058 | **否** | —— |

4 个可报留出格（0032/0035/0043/0047）里 **0 条**；以 primary 身份出现 **0 条**。
而提案 §三 自己已排除 `EIS-0038-02`。**净可计入上限 = 0。**

⛔ 按我自己写进记忆的「**先算上限再做相关分析**」：**上限为 0 则假设自动失败。**
我那个「12 位」是从**漏检清单**数出来的，不是从可报集算出来的 —— §零 说它是「当前最大的杠杆」，
§三 说构成它的记录不计入能力，**两节互相抵消**。

### C4 改动 ② 从另一条通路复现了我整节论证要避开的失效模式

实测（真实语料，非 docstring）：

    pair 0043   initial_target(PumpControl, Region1.PumpState)       = False  ← 现有发现
                untriggered_edge_declared("[*]", Region1.PumpState)  = True   ← 发现消失
    pair 0032   initial_target(AccelerateRegion, CruisingState)      = False  ← 现有发现
                untriggered_edge_declared("[*]", CruisingState)      = True   （该边守卫 R45RouteToken == 6）

语义根因：**我把 untriggered 与 unconditional 混为一谈。** `has_event=False` 只表示「无触发」，
而我的 `meaning` 写「a missing **unconditional** step」。语料 134 条无触发边里 **46 条带守卫**，
谓词对它们一律 True。

且产出方会选错的通路是敞开的：`caveat` 写「Use this only when the NL names no event for the step」——
入口类 NL（「上电后从 X 开始」）恰恰不点名事件；`field_specs` 主动广告 `"[*]"`；新条目在词表里
**紧挨 `initial_target` 之后**。回归闸只钉了 `edge_declared`，`initial_target` 这条通路零覆盖。

### 复算否证的一条附带主张

提案 §三「11/11 个 pair 都有无触发边」成立但**空洞**。分解 134 条：

| 形态 | 条数 | 归属 |
| :-- | --: | :-- |
| `[*] ->` 伪初始边 | 41 | `initial_target` 的地盘（见 C4） |
| 带守卫（多为编译器路由 `R45RouteToken`） | 46 | 谓词忽略守卫，**恒 True** |
| **普通 状态→状态 无触发边**（提案描述的形态） | **57** | 新谓词 |

而这 57 条中 **53 条在三个已 burned 格**（0018/0038/0048），4 个可报留出格里 **0 条**。

## 二、公平性侧的两条 C（均为文档，不需改代码）

### C1 provenance 锚错了，而更干净的出处早已存在且已裁定

`RULE_PROVENANCE.md` 逐字：「**照着漏检清单写规则就是把答案喂进去的一种形态**」。
而 `V23_REPORT_SKELETON.md` §十二之二 早已从**拒答统计**给出同一结论：

> `unsupported_binding` **92 条**，全部是 `'trigger' must be a non-empty path`，76/92 集中在伪状态族 pair
> …「该模型大量迁移**本就无触发**（伪状态间流转不带事件），生产者只能填空」
> **是否消耗 hold-out 资格：不消耗 —— 它是谓词表的设计问题，不针对任何具体样本**

⛔ **我用一个弱的、自证有罪的框架（照漏检清单数 12 位）替换了一个强的、已裁定的框架。**

### C2 上限低于已确立的噪声底，而预注册一行都没提

`V25_INSTRUMENT_ABLATION_PREREG.md` 已写死噪声底 **7.4pp**（v24 逐轮 `hit@1` 极差）。
我的上限：① 约 1–3 位、② 12 位，合计 **15/204 = 7.4pp**，恰好等于噪声底；② 单独 5.9pp，**低于**噪声底。

⛔ 「先测噪声底再谈效果」也是我自己写进记忆的判据。**本会话第三次「有规则、没用上」。**

## 三、由此得到的实际结论

| 杠杆 | 状态 |
| :-- | :-- |
| issue 粒度 | **判定侧已修**（`hits:X+Y`，commit `cd74380a`）—— 不需要动 pipeline |
| 无触发边谓词 | 可报留出集上上限 **0**，且会抹掉 `initial_target` 的现有发现 —— **不应作为一个代次的变量** |
| 其余全 0 记录 | 词表扩张（伪状态 kind / `event_cardinality` / 存在性否定），均需独立设计 |

📌 **所以 v25 没有可做的 pipeline 改动，而唯一已修好的杠杆在判定侧。**
下一步不是再找一处 src 改动，而是**按已修好的判定装置重判 v24**，看真实数字是多少 ——
这件事我在几小时前就识别为「唯一有依据的下一步」，随后却转去追 src 改动了。

---

📌 以下保留原提案供追溯。**其中每一处「拟改动」「预注册」「杠杆量化」都已作废。**

---

## 零、先给上限：为什么这两处是当前最大的杠杆

按层拆当前覆盖（干净装置两标注者保守合并，204 位）：

| 层 | 命中 | 位数 | `hit@1` |
| :-- | --: | --: | --: |
| `nl_named` | 62 | 102 | 60.8% |
| `wellformedness` | 28 | 72 | 38.9% |
| `over_specification` | 6 | 12 | 50.0% |
| `nl_contradiction` | 14 | 18 | 77.8% |
| **合计** | **110** | **204** | **53.9%** |

9 条记录全 0（54 位）= 当前词表下的能力上限之外，故**天花板 = 150/204 = 73.5%**。

我逐条人工读了这 9 条与 12 条部分命中记录，并把三个候选杠杆量化到位：

| 候选杠杆 | 实测位数 | 结论 |
| :-- | --: | :-- |
| 判据：合并 issue 造成的低估 | ~1–3 | 改动 ① 针对它 |
| 判据：`boundary` 过宽 | **2**（9 条候选里 7 条是计时主张，**判对了**） | 小，本轮不改判据 |
| **词表：无触发边不可断言** | **12（≈6pp）**，且解锁语料 **134/290 = 46%** 的迁移 | 改动 ② |

## 一、改动 ①：`prompts.py` L104 消歧（issue 粒度）

### 实测依据

追踪 `EIS-0043-02` 在 pair 0043 的 claude/R1 与 R3：**同一条封存断言逐字相同**，但

| 轮 | 发布的 issue |
| :-- | :-- |
| R1 | ① 三个业务子状态被错误嵌入 Region1 并发区域层<br>② PumpControl 的初始目标不是 PumpState，而是 UnspecifiedInitial |
| R3 | ① 引入了多余的 Region 层级…**且默认入口被替换为 UnspecifiedInitial** ← 两条并入一条 |

**R3 报了这个缺陷，只是打包了。** 一标签制度下另一条被记漏检。

### 这是一处真的跨阶段矛盾（三条都读了完整原文）

| 行 | 阶段 | 逐字 |
| --: | :-- | :-- |
| 360 | Splitter | Split independently violable mixed modalities into separate Requirements… **"X is a substate of Y and entering Y starts at X" is two claims (`containment`, `initial_target`) and must become two Requirements** |
| 437 | Adjudicator | a False assertion whose role is `primary`… may create a confirmed issue — **and must** |
| 104 | Adjudicator | **group evidence that reports the same underlying model defect** |

L360 的例子**逐字就是 0043 那一对**。L437 用 `must`，L104 用 `group`，**没有任何一处调和它们**。
R3 的合并是在遵守 L104。

⚠️ **与前两次「跨阶段矛盾」主张的区别**：那两次我漏读了 L379 的析取支，矛盾是我造的；
**这三条都是无条件祈使句，且我读了各自的完整行文。**

### 改法：改 L104 自己那一句，不新增第六处

> …supporting evidence is routed by the deterministic layer and must not appear in an issue.
> **Grouping operates on the evidence inside one issue; it never merges two False primaries into
> one issue. Requirements were split upstream precisely because their claims are independently
> violable, so two such primaries stay two issues even when a single model edit would repair
> both: a shared root cause is not the same claim.**

**是消歧，不是改政策** —— L437 已用 `must` 要求每个 False primary 建 issue。

## 二、改动 ②：新增谓词 `untriggered_edge_declared(source, target)`

### 实测依据

| 检查 | 结果 |
| :-- | :-- |
| `edge_declared` 签名 | `(source, trigger, target)`，**三者必填** |
| 无触发哨兵 `""` / `None` | `UnsupportedEvidence: must be a non-empty path` |
| `"[*]"` | 保留给伪初始，拒 |
| `"-"` / `"None"` | 名字不合式，拒 |
| 省略参数 | `TypeError` |
| **矩阵语料无触发迁移** | **134 / 290 = 46%** |
| 19 谓词中不需 trigger 又能定位单条边的 | **无**（`reaches` 是传递可达，表达不了「哪条边」） |

即：**声明里近一半的迁移不能成为任何声明类谓词的主体。**

### ⛔ 为什么不给 `edge_declared` 传 `event=None`（那是更小的改动，也是错的）

`structure.transitions` 把 `None` 过滤器当作**未设置**，于是该调用会匹配**任意**触发的边 ——
把 False 变成 True，**静默撤回当前成立的发现**。这正是上一轮 review 的 C2 那一类。
**新名字使现有调用一字不动。**

### 极性写死（上一轮 C1 的直接回应）

docstring 逐字：「As with every declaration predicate the **False** is the finding」。
三个对照已实测：

    真实无触发边            -> True   （正对照）
    未声明的边              -> False  （负对照，即发现）
    存在但**带触发**的边     -> False  （⭐ 关键负对照：不得把带触发边算进来）

### 五个登记点全部落实（仓库合同测试逐个逼出）

`predicate_api.py` 实现 → `PREDICATE_FAMILIES`（求值命名空间）→ `predicates.py` 词表 →
`capability.py` 归因 → 三份合同 fixture。

**`make test`：1645 passed / 4 skipped**（基线 1599，新增 46 条含合同参数化）。

### 端到端可达性与可归因性（登记 ≠ 可调用 ≠ 可归因，三件事分别验过）

| 检查 | 结果 |
| :-- | :-- |
| 在求值命名空间 `globals` / `locals` 内 | ✅ / ✅ |
| 在 `allowed_names` 白名单内 | ✅ |
| 从断言脚本表达式端到端求值 | ✅ `untriggered_edge_declared(source=…, target=…) is True` → True |
| 命中分支留下 attribution refs | ✅ 8 条 |
| ⭐ **False 分支**留下 refs（含近失锚点） | ✅ **6 条**，含 `…Join2` |

📌 **最后一行最要紧。** `_note_transitions` 的 docstring 写明：「a query that matches nothing still
needs an anchor: without a near miss a negative structural answer has no model identity to attribute,
which is how a real defect ends up merely `unattributed`」。若 False 分支不记账，本改动会**静默无效**
—— 断言照写、发现照被排除、覆盖率不动，而没有任何报错。

### 开跑前置闸（本轮新增，与改动同一批推送）

启动器现在在 launch **之前**写 `BASE/CODE_VERSION.txt`（commit / branch / 是否启动前写入 /
src 脏文件数），并在 pipeline src 脏或有未推送提交时**拒绝开跑**。两个方向都用对照验过：
往 src 放一个未跟踪文件即被拒；干净树下写出的 commit 与 `git rev-parse HEAD` 一致。

理由是可追溯性而非备份：run record 没有代码版本字段，v22/v23 都只有事后反推件，而
`full_tables.py` 早已在缺该文件时警告 —— 但此前没有任何东西保证它被写。

## 三、公平性自审

### 抽象化测试

- 改动 ① 陈述的是**两个已有阶段之间的契约**（拆开的义务不得在裁决时并回），不含 pair 号、状态名、
  期望缺陷、期望真值、判定结论。
- 改动 ② 是一个**谓词签名**，其 docstring 讲的是工具行为与极性，**不讲任何缺陷在哪**。

### ⛔ 按引入动机反向标注

| 改动 | 动机 | 不可计入能力的记录 |
| :-- | :-- | :-- |
| ① | pipeline **自相矛盾**（R1 做对、R3 做错，同模型同断言）—— 不是「某条记录没被发现」 | 保守起见排除 `EIS-0043-02` |
| ② | 探测 `edge_declared` 哨兵处理时测出 46% 缺口；但**探测由 `EIS-0048-04` / `EIS-0038-02` 引起** | 排除 `EIS-0048-04`、`EIS-0038-02` |

**这三条记录在 v25 的结果不计入发现能力**，只作「方法 + 样本共同演化」观测。
改动 ② 的能力主张落在其余无触发边上（134 条迁移横跨全部 11 pair）。

### 激活面（⚠️ 回测，测误伤面不测通用性）

无触发迁移逐 pair：`0000` 2/8、`0006` 7/11、`0018` 13/22、`0029` 15/70、`0032` 16/37、`0035` 1/16、
`0038` 13/21、`0043` 4/10、`0047` 9/26、`0048` 48/52、`0050` 6/17 —— **11/11 个 pair 都有**。
按记忆纪律，这只说明它不会只在一个 pair 上生效，**不证明通用**；通用性只能由活体运行判定。

## 四、⚠️ 这是**两变量**运行，但两个变量的可观测签名互斥

| 变量 | 独立签名 | 归因方式 |
| :-- | :-- | :-- |
| ① L104 消歧 | **每格 issue 数上升**，且新增 issue 与已有 issue 共享根因 | 比对 v24/v25 同格 issue 数与引用的 primary id |
| ② 新谓词 | **`untriggered_edge_declared` 出现在断言脚本中** | 计数该谓词的调用；v24 为 0（谓词不存在） |

**若覆盖率上升而该谓词调用数为 0，则增益全部归 ①；反之可分离。**

## 五、预注册判读条件（跑之前写死，含上一轮漏掉的那一行）

| 观察 | 判读 |
| :-- | :-- |
| ⭐ **任何当前命中的记录变为漏检** | **净负面**，须逐条定位；上一轮预注册漏了这一行 |
| `untriggered_edge_declared` 调用数仍为 0 | 改动 ② **未生效**，是词表说明或 prompt 引导问题，非能力问题 |
| 三条动机记录命中上升 | **不计入能力证据**（动机已烧掉） |
| 非动机记录出现新命中 | 弱正面信号 |
| 每格 issue 数上升而多报（`fabricated` / `grounded-extra`）同步上升 | 改动 ① **过宽**，拆得太碎，须收窄 |
| 修订轮数显著上升 | 规则制造了 reviewer 争议，净负面 |
| 覆盖率上升但集中在 1 个 pair | 疑特化，须逐 pair 报 |

## 六、不在本轮范围内（已定位，留待后续）

| 项 | 需要什么 |
| :-- | :-- |
| `wellformedness` 层「工具已报」子类：**9/12**（含 `InvalidInitial*`）或 **6/12**（只算 `UnspecifiedInitial`） | 收窄能力分母，见 [WELLFORMEDNESS_ATTRIBUTION_RULING.md](./WELLFORMEDNESS_ATTRIBUTION_RULING.md)；需独立核验 + 报双份数 |
| 伪状态 join/junction 类型错配（`EIS-0038-07` / `EIS-0048-05`） | `state_declared` 的 kind 词表扩张 |
| 事件粒度（`EIS-0000-02`） | `event_cardinality`，见 [FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md) §四 |
| over-specification 的存在性否定（`EIS-0018-03`） | 词表只有正向存在性谓词 |
| `boundary` 过宽 2 位 | 判据措辞，本轮不动判据以免与运行结果混淆 |
