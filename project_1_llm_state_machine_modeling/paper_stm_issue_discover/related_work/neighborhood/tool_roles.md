# 确定性成分的角色:逐项分类

> ⭐ **本文件是分类结果。** ⛔ 判据与协议在 [`TOOL_ROLE_TAXONOMY.md`](./TOOL_ROLE_TAXONOMY.md),⛔ **本文件不重复定义,也不修改判据。**
>
> ⛔⛔ **防火墙照旧**:本目录一切是**方法素材**,⛔ **不是论文证据**。
>
> **分类单位**:一次 **(成分 × 位置)** 三元组,⛔ 不是一篇论文。⭐ 同一成分在不同阶段占不同角色则拆成多行。

---

## 1. ⭐⭐ 我们自己(v46)—— **从源码分类,不是从卡**

⭐ 这一格用源码而非卡片作依据,⛔ 因为卡是摘要。⭐ 若某 agent 从卡分类的结果与本节不一致,**以本节为准并把差异记入 §1.2**。

### 1.1 逐项表

| 成分 | 它算出什么 | 输出到哪一步 | **角色** | 处置 | 有无对照 | 级别 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-: |
| `renderer._model_vocabulary()` | 已声明 states / events / variables · `-> [*]` 终止边(带 `ends_run`)· 复合退出边按 scope 计数 · 复合态声明入口(带 `converter_generated`)· 编译器自造变量 | `split_requirements` · `review_requirements` · `convert_assertions` | ⭐⭐ **表示变换 + 规则建立**(双重,§7 边界 4) | — | ⛔ **无对照** | M |
| pyfcstm `inspect_digest` | `parse_status` / `semantic_status` / `inspect_status` / `diagnostics` / `metrics` / `model_type` | `split_requirements` | ⛔ **零角色** —— ⭐ 逐字 `orientation evidence only` + `never turn a tool warning into a requirement` | — | ⛔ **无对照** | M |
| ⭐⭐⭐ **同一份 `inspect_digest`** | 同上 | ⭐⭐ **`convert_assertions`** | ⭐⭐⭐ **信息探索** —— ⛔ 该 prompt **7,709 字符里 `diagnostic` / `warning` / `orientation` 各 0 次**,⭐ 而它逐字**要求使用**:`when **structured inspect shows** that an operation/termination event exits an active child to "[*]" ... do not assert a nonexistent child-event-final direct edge` | — | ⛔⛔ **无对照 —— ⭐ 而装置就在我们手里** | M |
| NL 分段(`nl_segments`) | 把 NL 切成段 | `split_requirements` | ⭐ **表示变换** | — | ⛔ 无对照 | M |
| `renderer._source_context()` | `source_trace` 的 `attribution_boundary` 投影(`source_level_claim_allowed` / `representation_related` / `conversion_or_lowering_related`) | 三个 LLM 角色 | ⭐ **表示变换**(⚠️ 含少量规则性字段) | — | ⛔ 无对照 | M / S |
| Pydantic `StrictBaseModel` | 结构合规 | 解析失败原地重试 | ⭐ **求值** | **回灌** | ⛔ 无对照 | M |
| 断言契约门(`assertion_checker`) | 断言**可执行性** | `precheck_and_seal` → `review_assertions` | ⭐ **求值** | ⭐⭐ **回灌(可执行性)+ 封存(真值)** | ⛔ 无对照 | M |
| **19 条谓词求值**(pyfcstm parse / semantic / design / sim facade) | 每条断言的 `truth_value` | ⛔⛔ **不进任何 LLM** | ⭐ **求值** | ⭐⭐⭐ **封存 → 解封后记录** | ⛔ 无对照 | M |
| `bind_attribution` | 归因边界 `status` | 闭合 issue 集 | ⭐ **求值** | **拦截** | ⛔ 无对照 | M |
| `adjudicate_results` 的闭合 | issue 集对已发布结果闭合(`truth_value is False` ∩ `role ∈ {primary, precondition}` ∩ 归因 `safe`) | 限制裁决者的权限 | ⭐ **求值** | **拦截** | ⛔ 无对照 | M |

### 1.2 ⭐⭐⭐ 三条从源码读出的结论

1. ⚠️⛔ **首版写「我们没有任何一个信息探索角色」—— ⛔⛔ 那是错的,已更正。** ⭐ 机械核实:`inspect_digest` 进**两个** `render_*` 函数(`render_requirement_split_input` · `render_assertion_conversion_input`),⛔ 而零角色框定**只在第一个里有**。⭐⭐⭐ **`convert_assertions` 不但没有禁令,⭐ 还逐字要求使用 structured inspect 做层次完成判断** —— ⭐ 故按判据它是**信息探索**。

   ⛔ **三处修正连带**:(a) ⛔ `inspect diagnostics alone are not sufficient evidence` 那句在 `review_assertions` 的 prompt 里,⛔ **而该阶段根本收不到 `inspect_digest`**(`render_assertion_review_input` 无该键)—— ⭐ 那句话框的是审查者看不到的东西;(b) ⭐ 所以我们**有一个信息探索通道**,⛔ 但它**窄**(只服务层次完成判断,⛔ 不服务一般缺陷发现);(c) ⛔⛔ **它从未被量过** —— ⭐ 若有人问「你们的发现里有多少是模型照着 pyfcstm 诊断报出来的」,⛔ **我们现在答不上来**。

   ⭐⭐ **而这一格的对照装置就在我们手里**:⭐ `prompt_json` 的 payload 是逐键装配的,⛔ 去掉 `inspect_digest` 是一行改动,⭐ 而全网格 324 格的跑法已经存在。⭐⭐⭐ **这是 §2.4 那个「信息探索加法未测」的空白里,唯一一个可立即执行的填法。**
2. ⭐⭐⭐ **「封存」是类型系统保证的,不是约定。** ⭐ 放给审查者的 `AssertionExecutionPublic` 字段只有 `status: Literal["executable", "invalid", "blocked"]` 与 `error` —— ⛔ **结构上没有 `truth_value`**;真值只在 `AssertionResult` 上,⭐ 经 `SealedAssertionReceipt`(只含 `sealed_hash` / `result_count` / `sealed_payload_ref`)间接引用。
3. ⭐⭐ **有一处「记录 vs 回灌」的显式取舍**,源码注释逐字:`blocked means a prerequisite did not hold... It is not an execution failure and **must not send the script back for repair -- the prerequisite's own False is the finding**.`

### 1.3 ⛔ 一个必须一起说的事实:**九项全部无对照**

⭐ 上表 9 行,**「有无对照」列全部是「无对照」**。⛔ 即我们**从未测过任何一个成分的有无**。⚠️ 这不是本轮的疏忽,⭐ 是既有状态 —— ⛔ 但它意味着**我们对自己流水线里每个确定性成分的贡献都没有数字**。

---

## 2. ⭐⭐ 已核实的角色 × 效果证据(⛔ 逐条带分母)

### 2.1 ⛔⛔ 规则建立:三个独立团队报负面

⭐ 三个团队、三种不同制品、同一现象:**往发现阶段注入规则目录,召回被重新分配而非增加**。

| 团队 | 逐字 | 级别 |
| :-- | :-- | :-: |
| **Télécom Paris**(MODELS 2024 + SoSyM 2026,⚠️ **同团队算 1 次独立观察**) | `when these rules are incorporated into the knowledge database injected in the consistency request, **the LLM tends to exclusively focus on these rules, thus ignoring other consistency aspects**`。⭐ 期刊版给的对策:`it is beneficial to run the detection process **twice, once with formal rules embedded and once without**, to take advantage of a broader detection basis` | M |
| **北航**(Internetware 2025) | `As rule complexity increases, **LLMs may lose focus on the original requirements**, and fixing one issue can introduce new ones` | M |
| **RFSeek** | 见 §2.2 逐条 | M |

### 2.2 ⭐⭐⭐ RFSeek 的四条 prompt 变更:按本分类学**恰好 2-2 分裂,且两类行为模式不同**

⭐ 这是本文件最强的一条 —— ⭐ **单篇论文内部的自然对照**,⛔ 不是跨篇拼的。

| # | 改了什么 | ⭐ **改的是哪个角色** | 逐字结果 | ⭐ 召回怎么变 |
| :-: | :-- | :-- | :-- | :-- |
| **1** | 只喂「最相关」的章节 | ⭐⭐ **信息探索 ↓** | `it reproduced the transitions already depicted in the diagrams and **did not yield any new or implicit protocol behaviors**` | ⛔ **下降** |
| **2** | 去掉 RFC 自带的 ASCII 图 | ⭐⭐ **信息探索 ↓**(去掉一个**模态 / 视角**) | `When the diagram was absent, **certain transitions were missing**... transitions described exclusively in diagrams **may be overlooked**` | ⛔ **下降** |
| **3** | 要求抽「**precise and accurate** FSM」 | ⭐⭐ **规则建立** | `it **completely omitted some edges it had previously identified**`(⛔ 删掉的正是促成 **RFC 9293 errata** 的那条边) | ⛔ **重排** |
| **4** | 加「抽出摘要提到的**所有**迁移」 | ⭐⭐ **规则建立** | `**this did not increase the total number** of transitions identified; **rather, the set of extracted transitions shifted**` | ⛔ **总数守恒,集合重排** |

⭐⭐⭐ **两类的行为模式不同**:⭐ 信息探索**减少** → 召回**真的下降**;⭐ 规则建立**变更** → **总数守恒、集合重新分配**。

### 2.3 ⭐⭐ 它顺手排除了一个竞争机制

⛔ 本来最可能的替代解释是**上下文预算**:也许失败来自 context 被占,⭐ 那 信息探索 也会受害,⛔ 角色区分就没意义。

⭐⭐⭐ **变量 1 / 2 把它排除了**:它们是**减少**输入而召回**下降**。⛔ 若机制是「context 稀缺、越少越好」,减少输入应当**改善**;⭐ 结果相反 —— **所以机制是角色特异的,不是预算通用的**。

### 2.4 ⚠️ 信息探索的加法:唯一形态无测量 + 一条异构加法

| 项 | 内容 | 级别 |
| :-- | :-- | :-: |
| ⭐ **唯一做了这个形态的工作** | ⭐ MBD(conflict set + minimal hitting set + 执行序位置约束 + AST 归一化剪枝)算出 **2 个 gateway** → **定位到元素后进 prompt** → LLM 只负责「把 gateway 翻译成原文片段 + 写两种竞争解释」。⭐ 主结果模型 `GPT-5.1`,**与我方同代** | M |
| ⛔⛔ **它的对照** | ⭐ **artifact 里有装置**(prompt 两个变体:含 MBD / `_without_diagnosis`),⛔ **正文一字未提结果**。⛔ 另:全文**无任何 $H_{norm}$ 数值**、$n=2$、⭐ 样本按「高 variability」筛出且无对照组、⛔ **被优化量与宣告成功量是同一个** | M |
| ⭐ **一条异构加法** | ⭐ 把配置的常量名与性质名告诉模型:**18.7%** vs 让模型自己还原 **10.0%** = **+8.7pp**,⭐ 当代模型。⛔ **但该档是重新采样(不同批)**,⛔ 且测的是「产出正确规约」不是「发现缺陷」 | M |

---

## 3. ⭐⭐⭐ 语料逐项分类:**约 277 行 (成分 × 位置)**

⭐ 三路**上下文独立** agent 各分 10 张卡,⭐ 全部照冻结定义填 8 个字段。⛔ 三路互不可见,⭐ 故凡三路独立得到同一结论的,证据最硬。

### 3.1 角色分布总表

| 角色 | A 路 | B 路 | C 路 | **合计** | 一句话 |
| :-- | --: | --: | --: | --: | :-- |
| ⭐⭐ **评测端** | 15 | 15 | **31** | ⭐⭐⭐ **61** | **最大的单一类别** |
| **求值** | 22 | 12 | 15 | **49** | 处置见 §3.2 |
| **规则建立** | 15 | 15 | 14 | **44** | ⭐ **10/10 篇满命中** |
| ⭐⭐ **表示变换 / 定域** | 7 | **19** | 12 | ⭐⭐ **38** | ⛔ 分类学首版记「3 处」 |
| **不进 LLM** | 16 | 10 | 6 | **32** | |
| **人在回路** | 7 | 5 | 2 | **14** | |
| ⭐ **信息探索** | 3 | 6 | 3 | ⛔ **12** | ⛔ **可用两侧数字 0 处** |
| **待分类** | 5 | 2 | 3 | **10** | 新形态见 §3.5 |
| **执行操作** | 1 | 2 | 6 | **9** | |
| **训练端** | 0 | 1 | 6 | **7** | |
| **聚合** | 1 | 3 | 1 | **5** | |
| ⛔ **零角色** | 0.5 | 2 | 1 | ⛔ **3.5** | ⭐ 见 §3.4 |

⭐⭐⭐ **第一条读数(三路独立同向)**:**「这个领域用了很多确定性工具」这句话成立,⛔ 但 61/277 用在给方法打分、32/277 根本不进 LLM、14/277 回灌给人。⭐ 即约 **39%** 的确定性成分对模型决策过程的作用是零。**

### 3.2 求值的处置分布

| 处置 | 合计 | 备注 |
| :-- | --: | :-- |
| **回灌** | ~21 | 主流 |
| **拦截** | ~12 | |
| **丢弃** | ~8 | ⭐ 有一处用它换掉整套修订机器 |
| ⭐ **记录** | **~5** | ⛔ 其中真把真值当产物的**只有我们** |
| ⭐ **择优** | 1 | ⛔ 首版无此格,由 A 路查出 |
| ⭐⭐⭐ **封存** | ⛔ **1(我们)** | ⛔ **语料零例** |

⭐⭐ **B、C 两路独立确认**:9 篇 / 10 篇外部工作里**没有一篇把确定性真值本身当成产物** —— ⭐ 它们全部拿去控制流程或打分。⚠️ C 路找到一个边缘第二例(某合并器「矛盾则打 flag」),⛔ **但论文从未报有多少 flag、也没把 flag 当任何结论**。

### 3.3 ⭐⭐⭐ 信息探索:**12 处,可用两侧数字 0 处**

⭐ 三路各自独立走到同一结论。逐处状态:

| 处 | 是什么 | 对照 |
| :-- | :-- | :-- |
| ⭐ MBD 诊断 → 2 个可疑 gateway | ⭐ 唯一「LLM 只负责整理归纳」的形态 | ⛔⛔ **装置在 artifact 里(`_without_diagnosis` 变体),⛔ 正文一字未提结果** |
| ⭐ cfg 常量名与性质名注入 | +8.7pp(18.7% vs 10.0%,分母 300) | ⛔ 该档**重新采样**;⛔ 作者自报二项区间 **±4–7pp** —— **+8.7pp 与误差带边缘相接**;⛔ 测的是产出正确性不是发现 |
| ⭐ VSS 信号目录检索 | 18% → 34% | ⛔ **n=1 场景 · 无重复 · 摘要自称 0% 与表格 34% 自相矛盾** |
| ⭐ RFC 自带的 ASCII 图 | ⭐ **有对照装置**(有图 / 无图) | ⛔ **两侧都没有数字**,⭐ 且作者自限 `we did not systematically assess this` |
| ⭐ 差分 oracle 的失败报告 | 信号名 + 波形图 | ⛔ **oracle 不可消融**(没 oracle 就没任务) |
| ⭐ 外部权威材料 / SysML 规约 / 范例库 / agent 主动检索 / 拓扑采样器 | 见 §3.5 N5、N6 | ⛔ 全部无对照 |
| ⭐⭐ **我们的 `inspect_digest` → `convert_assertions`** | — | ⛔⛔ **无对照,⭐ 而装置就在我们手里** |

⭐⭐⭐ **A 路给出的最尖锐一句**:⛔ **不是「没人做过信息探索」,⭐ 而是「做过的人手里都有对照装置,却都没报」** —— ⭐ 两篇,两次,独立发生。

### 3.4 ⭐⭐⭐ 零角色:**我们的做法在语料里没有先例**

⭐ C 路逐字:

> ⛔ 我没有找到 taxonomy §5 那种「工具输出确实进了 prompt、但被 prompt 明令框成不可据以形成义务」的典型零角色案例。**这批 10 张卡里一个都没有。** ⭐ 这本身是个发现:`orientation evidence only` 那种框定方式**在邻域里没有先例**。

⭐ A 路只找到**半个**(某篇剥夺了 reference/target 标签的正确性含义,⛔ 而诊断本身照常生效)。⭐ C 路那 1 处是**处置执行装置**(路由节点),⛔ 不是框定。

⭐⭐ **含义有两面**:⭐ 一面是我们那条禁令**独特**;⛔ 另一面是它**没有先例可引** —— ⭐ 若要在论文里为它辩护,只能靠自己的论证。

### 3.5 ⭐⭐ 新形态:三路共报 **9 类**(⛔ 去重后)

⭐ 分类学 §7 原有 6 类。⭐ 三路各自撞到 §7 装不下的形态,⭐ 去重后 9 类:

| # | 新形态 | 谁报的 | 为什么 §7 装不下 | ⭐ 处置 |
| :-: | :-- | :-: | :-- | :-- |
| **N1** | ⭐⭐⭐ **构造端 / 生成期强制** —— 使违反**不可表达** | A | ⭐ 三种强度:解码期掩码 · 求解期硬约束 · **表示层吸收**。⛔ 且它**既非前置也非后置**,证伪了 §2 的推论 | ⭐⭐ **已升为第六个角色**(分类学 §3.6) |
| **N2** | ⭐⭐ **处置「择优」** —— 在多候选间排序并交付最好的 | A | ⛔ 记录/回灌/拦截/丢弃四者皆非。⭐ 绝对判据 vs 相对判据 | ⭐⭐ **已加为第五种处置**(§4) |
| **N3** | ⭐⭐ **处置「转交」** —— 真值送进一个**下游 LLM** 当输入 | B | ⛔ 不是回灌(接收者不是生产者、不被要求修订),⛔ 也不是记录(它**是**下游决策依据) | ⭐ **待加**;⭐ 我们的 `adjudicate_results` 就是 |
| **N4** | ⭐⭐ **求值·回灌,⛔ 但接收者既非 LLM 也非人** | B | ⭐ §7 #3 只有「回灌给人」。⛔ 某篇回灌给决策树 Learner,⭐ 整个循环零 LLM | ⭐ 记求值·回灌 + 标注「不作用于任何 LLM」 |
| **N5** | ⭐⭐⭐ **检索到的在原输入外,⛔ 但内容是「怎么写」而非「制品的事实」** | B | ⭐ §7 #5 只看语料位置,⭐ §3.3 只看内容性质 —— ⛔ **两条判据给出相反答案** | ⭐⭐ **§7 #5 应加第二个判据轴** |
| **N6** | ⭐ **确定性成分产出的是**任务输入本身** | B | ⭐ §3.1 的判定动作预设有一个独立于该成分的输入,⛔ 撤掉它就没有输入了 | ⭐ 记信息探索 + 标注 |
| **N7** | ⭐⭐ **不进任何 prompt,⛔ 却改变另一道门的严格度** | B | ⭐ 二阶效应经门到达模型。⛔ §2 的轴指向「另一个确定性成分的策略」,⛔ 那不是五个部件之一 | ⭐ 记不进 LLM + 标注二阶 |
| **N8** | ⭐ **输出是关于**流程**而非关于**制品** | B | ⭐ 如「你上次发的版本号是 3,这次必须发 4」—— ⛔ 既非制品事实,也非纯规定,⭐ 是**协议状态** | ⭐ 按主导记 + 标注 |
| **N9** | ⭐⭐ **人手写死在 prompt 里的、关于被测制品的事实断言** | C | ⭐ 如「脚本里的值都是对的」。⛔ **没有任何工具产出它,也不随制品变化** —— ⭐ 五个角色都预设有一个成分在算东西 | ⭐⭐ **值得单立类**:它等于设计者对被测者的一次**真值披露** |

⭐ **另有两类是 §7 已覆盖但报出了新实例**:⭐ 「LLM 自己此前的输出当跨阶段上下文」(C 路,⭐ 判表示变换,⛔ 因为信息量没增加)· ⭐ 「同一确定性算子既在产出侧又在判分侧」(C 路 3 例,⭐ 自我防护强度递减)。

### 3.6 ⭐⭐⭐ 本轮最有解释力的一条:**同一个检查器,加工方向相反,结果相反**

⭐ B 路把两篇放在一起读出来的。⭐ 两篇都有真检查器,⭐ 都把输出加工后注入 prompt,⛔ **加工方向相反**:

| 篇 | 把求值输出加工成 | 角色 | 结果 |
| :-- | :-- | :-- | :-- |
| ⭐⭐ A 篇 | **哪个动作最可疑**(反例定位启发式:越靠后越可疑 · 越频繁越可疑) | ⭐ **表示变换 / 定域** | ⭐⭐ 逐轮 R1–R4 **全部为正**,5 轮共 **+25.00pp** |
| ⛔ B 篇 | **祈使句规则**(如 `Don't miss out State in requirements`) | ⛔ **规则建立** | ⛔ 语义层解决率 **37–43%**,⛔ **6 条规则解决率恰好为 0** |

⭐⭐⭐ **而 B 篇自己的归因与这个读法一致**,逐字:`One key reason is the lack of an optimal model-checking feedback mechanism in our study` + `These counterexamples can be provided as feedback to the LLM`。

⭐⭐ **即它自己点名要的,正是 A 篇已经做了的那一步:把求值输出做成定域,而不是做成规则。**

⭐ **同向旁证(B 篇自己的逐规则表)**:⭐ 凡「点名缺了哪个具体元素类型」的规则解决率接近满分(**30/30 · 8/8 · 2/2 · 9/9**);⛔ 凡「要求判断合理性」的规则接近零(**0/6 · 1/13 · 12/45**)。⭐⭐ **前者形态上更像定域(告诉模型看哪里),⛔ 后者是纯规则建立。**

⚠️⛔ **必须带的限定**:⛔ 两篇任务不同(修复 vs 生成)、模型代次不同、⛔ **没有任何人做过「定域式反馈 vs 祈使句式反馈」的受控对照**。⭐ 这条读法级别 **I**,⛔ 不是任何一篇的结论。

### 3.7 ⭐⭐⭐ 一条新轴:**反馈定位粒度 × 收敛率**

⭐ C 路读出来的,⭐ 而它把三篇放在同一条轴上:

| 反馈粒度 | 实例 | 结果 |
| :-- | :-- | :-- |
| ⛔ **无定位**(只说「哪条性质没满足」) | ERTS 2026 | ⛔⛔ **6 格里 5 格撞满 20 轮不收敛**,⭐ 最贵一格 224,078 token 后仍剩 6 条未满足 |
| ⭐ **信号级**(失败信号名 + ref/test 对比波形 + 异常原文) | zenodo | ⭐ fix rate **74.7%**,⛔ 但 **41.1% 的格撞 600 秒墙钟** |
| ⭐⭐ **元件级** | ⛔⛔ **无案例** | — |

⭐⭐⭐ **而 ERTS 那篇手里就有元件级的东西**:模型检查器的**反例回溯**在 TTool GUI 里对人可见(图注逐字 `Green backtracing shows that all states satisfy the safety properties.`),⛔ **但从未进 prompt** —— ⭐ 进去的只有真值清单。⭐ 作者自己的归因逐字:`Further refinement of prompt engineering (particularly improving the feedback provided to the LLM regarding each unsatisfied property) would likely enhance the effectiveness of the auto-correction mechanism`。

⚠️ **限定**:⛔ 三篇任务不同、模型不同、⛔ 无人做过粒度的受控对照;⛔ 且 zenodo 每格只跑一次、41.1% 的耗尽格**没有任何结构化诊断**说明卡在哪。⭐ 级别 **I**。

### 3.8 ⭐⭐ 「手里有工具却没那么用」:三路共 **13 处**,⛔ 只有 1 处给了理由

| 篇 | 手里有 | 实际当什么用 | 本可当什么 |
| :-- | :-- | :-- | :-- |
| ⛔ 某协议工作 | ⭐ **能编译能跑、自带测试套件的 C 实现** + fuzzer | ⛔ 编译器 / 类型检查 / 测试执行**一个都没进环** | 求值·回灌 · 信息探索 |
| ⛔ 某 SysML 工作 | ⭐ 块类型是**确定性可得的字段** | ⛔ **未导出到文本格式,让 LLM 猜** —— ⭐ 而三条规则全建立在这个推断属性上 | 表示变换(⭐ 一行导出) |
| ⛔ 同篇第二处 | ⭐ 自家工具链有 SysML 直接模型检查 | ⛔ 只在 related work 提一句 | 求值 |
| ⛔ 某多智能体工作 | ⭐ 一个可当门的确定性引用检查(自称 `definitively indicates a cross-phase structural hallucination`) | ⛔ **只拿来算分** —— ⭐ 拦幻觉的是 LLM 自评 | 求值·拦截 |
| ⛔ 某状态机工作 | ⭐ `umple.jar` **3,134,073 字节就躺在 `backend/resources/`**,⭐ 而单提示输出恰好是 Umple 代码 | ⛔⛔ **连求值都没接** | 求值 |
| ⛔ 某一致性工作 | ⭐ 一个**双向**残差信号(需求侧缺口 + 模型侧多余) | ⛔ **三条规则全写成单向,修复方向永远是改需求** | 双向都用 |
| ⛔ 某比对工作 | ⭐ textX 文法可确定性判结构合规;⭐ 且投票是**纯计数任务** | ⛔⛔ **投票计数交给 LLM** 做(花一次全上下文调用数字符串出现次数) | 求值 · 聚合 |
| ⛔ ERTS | ⭐ 模型检查器的**反例回溯** | ⛔ 只进 GUI 给人看 | ⭐⭐ **信息探索**(见 §3.7) |
| ⭐ **唯一给了理由的** | ⭐ Spin + SMT + model counting | ⛔ 全在评测端 | — |

⭐ 唯一给理由那篇逐字:`without invoking a model checker/theorem prover for validation`,⭐ 理由是 `makes these approaches depend on the scalability of the verification tools`。

⭐⭐ **而 A 路记了一条重要区分**:⛔ 有三处是**纯工程遗漏**(一行导出 / 一个 `Counter` / 装一个检查器),⛔ 修法成本极低,⛔ **但它们各自污染了论文的一个核心结果**。

### 3.9 ⛔⛔ 有效性主张压在零角色 / 评测端成分上:三路共 **14 处**

⭐ A 路给出的横跨规律:

> ⛔⛔ **凡是「循环收敛率」「合规率」类的漂亮数字,只要裁决者与指标是同一个装置,那个数字就是定义性的。**

⭐ 最严重的三例:

| 篇 | 主张 | ⛔ 实际压在哪 |
| :-- | :-- | :-- |
| ⛔⛔⛔ 某谓词发现工作 | ⭐ **署名贡献 (iv)「LLM 辅助谓词提示」** | ⛔⛔ **三个有效性指标全部由评测端的 Spin + SMT + model counting 产出,⛔ 而 LLM 那一步从未被单独消融** —— ⭐ 唯一的对照换掉的是 **Learner**,⛔ 不是 LLM。⭐⭐ **即该署名贡献在实验里没有任何证据** |
| ⛔⛔ 某 PLC 工作 | ⭐ 标题写 `Compiler-Ready` | ⛔⛔ **整条流水线里没有编译器**(自陈 future work);⭐ 主判定是 **5 个 LLM 检查 1 个 LLM**,⛔ 而它批评的正是 LLM 自检。⚠️ 另:其批评的**唯一文献依据经实测是伪造引用** |
| ⛔⛔ 某多智能体工作 | ⭐ 摘要 `eradicated` / `zero-error` / `This proves` | ⛔⛔ **它自己的判据否证了主张**:自称 `below 100% definitively indicates a cross-phase structural hallucination`,⭐ 而其 Proposed Workflow 是 **97%** |

⭐ **一条反向的(⭐ 唯一没犯这毛病的)**:某篇最漂亮的数(`0 误报 0 漏检`)**来自一条零 LLM 的确定性臂**,⭐ 而论文**明确把它归给那条臂**,⛔ 没挂到 LLM 上;⭐ 且自认 `there is a potential for confirmation bias`。⚠️ 但那个满分建立在 **n = 3** 上。

### 3.10 ⭐ 同一成分占两个角色:三路共 **21 处**

⭐ 最有价值的一处(A 路):**同一份约束目录,交给算法做求值·回灌是 0%,交给 LLM 当规则清单自评是 18.34/19.48%(基线 21.80%),后者还多烧 2.5 倍调用** —— ⭐⭐ **同 backbone 同数据集,这是分类学 §5「角色是工具输出 + prompt 框定的联合属性」在外部语料上的直接实证。**

⚠️⛔ **但那个 0% 是定义出来的**(该变体的接受判据就是那道检查),⭐ 所以**准确性侧信息量为零,⭐ 信息全在成本侧**(1.87 vs 4.65 次调用)。

⭐ 另有 **3 处「确定性算子既在产出/参赛侧又在判分侧」**(C 路),⭐ 自我防护强度递减:⭐ 一篇另跑 26 人排序作交叉验证并自评 `only moderate`;⭐ 一篇只在正文承认「类似策略」;⛔ 一篇完全没有独立判据 —— ⭐ **而它的评分器正是被对比的那一方。**

### 3.11 ⛔ 分类学要按本轮结果改的四处

| # | 分类学原文 | 本轮实况 | 状态 |
| :-: | :-- | :-- | :-- |
| 1 | §8「表示变换:⭐ 语料里 **3 处使用**」 | ⭐⭐ **38 处** | ⛔ **须改** |
| 2 | §8「表示变换:**0 对照**」 | ⭐ 仍是 0 处**可用**对照 —— ⚠️ 唯一有数的两处:一处违反「只算纯自动」硬门、⛔ 一处是「两种表示互比」而非「有/无」且其反向那列**消融已泄漏**(16/32 文件仍在用被消融的工具) | ⭐ **结论保留,分母改** |
| 3 | §3.2「表示变换只能让本来看得见的更容易看见」 | ⛔ **只写了上界**。⭐ 实测下界:一次收窄式定域把新发现打到 **零** | ⭐ **已改** |
| 4 | §7 边界 5「检索按语料位置二分」 | ⛔ 与 §3.3(事实 vs 规定)冲突 —— ⭐ 见 N5 | ⛔ **须加第二判据轴** |

---

## 4. ⭐⭐ 用本分类学查出的新缺陷

⭐ 见 [`discover_matrix/docs/findings/predicate_routing_defects.md`](../../discover_matrix/docs/findings/predicate_routing_defects.md)。

⭐ 一句话:**`occupancy_after` 的 `trigger` 字段说明宣称「本谓词也验证事件被消费」,⛔ 而它的签名有必填的 `target` 而 `event_consumed` 没有** —— ⭐ 故该主张只在完整指定的迁移上成立,⛔ 对「点名刺激但不点名去向」的句子不可表达。⭐ `event_consumed` 被问 **0.0%**、Δ **+55.6pp**,⛔ 而已有的修法只覆盖 `edge_declared`。

⭐⭐ **该条有独立的领域出处**(⛔ 两个函数签名的事实,只读 `predicates.py` 可核,⛔ 不引用台账),⭐ 故与那个 oracle-informed 的四扫描块**性质不同**。

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。⭐ §1 从**源码**给我们自己的 9 个确定性成分分类(⛔ 不是从卡),⭐ 查出「封存」是类型系统保证的、以及一处「记录 vs 回灌」的显式取舍;⛔ 并记下**九项全部无对照**这个既有状态。⭐ §2 落三团队负面证据与 RFSeek 的 2-2 分裂(⭐ 后者是单篇内部的自然对照,⛔ 且排除了上下文预算这个竞争机制)。⭐ §4 记用本分类学查出的新缺陷。⏳ §3 语料逐项分类进行中。 |
