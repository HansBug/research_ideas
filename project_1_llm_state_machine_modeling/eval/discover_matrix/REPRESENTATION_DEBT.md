# 表示债务（representation debt）：现象、机理、以及在 paper 里怎么写

本文件把 v46 意外发现裁定中最重要的一项结论固化为长期研究事实。
实测数据与逐簇判据见 [V46_UNEXPECTED_ADJUDICATION.md](./v46/unexpected_adjudication.md)、
[V46_UNEXPECTED_EVIDENCE.md](./v46/unexpected_evidence.md)、
[V46_UNEXPECTED_MERGED.md](./v46/unexpected_merged.md)。

## 〇、定义

> **表示债务（representation debt）**：源制品到分析用中间表示（IR）的编译过程中丢失的语义，
> 在 IR 上表现为可被自动检测器命中的「缺陷」，但在源制品上并不存在。

本现象在既有文献中已有名字：模型检查中因抽象过粗产生、在具体系统上不存在的报警称为
**spurious counterexample**（CEGAR，Clarke et al. 2000）；静态分析框架因程序表示构建不当
产生的假阳称为 **program representation fault**（ISSTA 2024）；MDE 中转换是否保语义的属性称为
**semantics / behavior preservation**，其在层次状态机上的具体形态即 **state machine flattening**
的信息损失。术语 *representation debt* 本身检索未见占用，但**现象不是新的**。

本文只对既有概念作三点限定：

1. **不是过近似。** CEGAR 的伪反例来自 over-approximation（抽象允许了具体系统做不到的行为）；
   此处相反，是 **under-expressive re-encoding**——目标 IR 表达力**低于**源语言，源制品的合法
   结构被压成单一标识符。因此不存在 CEGAR 意义上的 refinement 回路：细化到底也无法恢复，
   只能回读源制品。
2. **不是工具 bug。** R4.5 的行为是设计内的、确定性的、且**自申报**的。
3. **落点在评测归因，不在转换正确性。** 既有工作问「转换保不保语义」；
   本文问「不保语义的那部分，在下游评测里被记到了谁头上」。

⚠️ 命名沿用 technical debt 家族中的 **self-admitted** 分支（债由编译器自身在
`fcstm_meta.json` 中声明）。**须与 Lano 等人的 "technical debt in model transformation
specifications" 区分**——后者指转换规约自身的质量缺陷，本文指转换**造成的**下游归因负债。

**操作化判据**：一条产出被判为表示债务，当且仅当

1. 该产出所陈述的事实在 IR（`model.fcstm`）上**客观为真**；且
2. 该义务在源制品（`stm0.puml`）上**已被作者逐字表达**；且
3. 编译器已在 `fcstm_meta.json` → `source_static_reason_codes` 中登记对应债务码。

⚠️ **只有条件 1、3 可机械判定；条件 2 需人工回读源制品**——词法检索在本语料上已被证实不可靠
（按 `front_distance` 检索 0010 得出「作者源亦无」，作者实写 `Front Distance > 10`，逐行读原文才改正）。

⚠️ **条件 3 绑死在自申报编译器上**。若编译链不自申报，条件 3 不可用，判定退化为 1+2 的人工回读
——**这正是本文主张「有损编译器必须自申报损失清单」的原因：没有清单，这一份额不可测。**

三条缺一不可（条件 3 在自申报编译器下）。第 2 条是与「真缺陷」的分界线：0036 的 `/ UAV Count Decreased` 作者写了 → 债务；
0006 的作者源里连递减文本都没有 → 真缺陷。

## 一、机理：为什么必然发生

```
作者手写 stm0.puml  ──[R4.5 转换 / 下沉]──▶  model.fcstm  ──▶  discover 流水线读这一份
   PlantUML，真原件         有损编译              FCSTM，编译产物
```

**根因是表达力落差**：PlantUML 的迁移标签是一段**自由文本**，可写 `trigger [guard] / effect`，
guard 内允许任意布尔表达式；FCSTM 的 `event` 是**一个原子标识符**。自由文本装不进原子标识符时，
R4.5 的做法是把整段文本清洗成一个合法标识符充当事件名。

⚠️ **「下沉（lowering）」是编译动作，与 discover 流水线的置信度 / 降级 / 成熟度分级毫无关系。**
这是最容易的误读，此处钉死。

全语料债务码分布：

| 债务码 | 带该码的制品数 /60 | 含义 |
| :-- | --: | :-- |
| `opaque_transition_label_semantics` | 58 | 整条迁移标签被压成一个不透明事件名 |
| `composite_source_activation_dispatch` | 28 | 复合态出边的激活派发被改写 |
| `opaque_state_body_semantics` | 27 | 状态体描述行被压进状态名 |
| `missing_explicit_initial` | 16 | 缺显式初始，注入伪初始态 |
| `concurrent_region_semantics` | 9 | 并发区语义被改写 |
| `multiple_initial_fanout` | 9 | 多初始扇出 |
| `composite_source_external_reentry` | 7 | 复合态外部重入 |
| `ambiguous_unlabeled_fanout` | 6 | 无标签扇出歧义 |
| `invalid_source_initial_target` | 5 | 非法初始目标 |
| `explicit_concurrency_pseudostate` | 3 | 显式并发伪态 |
| `invalid_source_final_scope` | 2 | 非法终态作用域 |
| `source_input_normalization` | 1 | 源输入归一化 |

⚠️ **该码是制品级存在标志，不是实例计数。** 一份制品里发生了多少处损失不体现在此表；
写「N 条迁移标签被压平」是凭空的实例数。
⚠️ **每个码在 `source_static_reason_codes` 与 `simulation_reason_codes` 两个数组里各列一次。**
正确命令：`grep -l <code> */fcstm_meta.json | wc -l`。

## 二、三个实例

### 例 1：析取守卫 → 一个事件名（70 类，最大一块）

`llms_emp_feedback_final_0029/stm0.puml:33`，作者原文：

```
collision_avoidance_deactive --> collision_avoidance_active :
    pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode
```

对照 NL 12「…such as detecting pedestrians (`pedestrian_detected`), the rear distance…, **or** the front
distance…」——作者一字不差地写全了四个替代激活源，用 `|` 表 or、`&` 表 and，**建模完全正确**。

下沉后：

```
event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_highway_dist_to_front_10_in_urban
```

discover 于是报告「四个激活源被压成一个融合事件，模型无法只凭检测到行人激活」。
**这句话对 `model.fcstm` 字字属实，对作者的建模完全冤枉。**

### 例 2：变量 → 烧进事件名（42 类）

**PlantUML 没有变量声明语法**——无法写 `int front_distance;`，量只能写进守卫文本。
0000 的作者写 `front_distance > 10`，下沉后成为 `event front_distance_10 named "front_distance > 10"`。
（0010 的作者写的是大小写不同的 `Front Distance > 10`，下沉为 `Front_Distance_10_2`；
两者是同一机理的两个实例，**不要把 0010 的作者文本与 0000 的下沉名拼成一条**。）

后果：`variable_declared(front_distance)` 返回 False。而该谓词在**全语料 60 份制品上恒为 False**
——33 份的唯一 `def` 是转换器注入的 `R45RouteToken`，另 27 份连一行 `def` 都没有，
**作者变量 0/60**。即它在本语料上不携带任何判别信息。

### 例 3：`trigger / effect` 焊死（9 类）

作者写 `Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count`。
UML 记法里 `/` 前是触发、后是效果，**作者分得清清楚楚**。下沉未切分 `/`，
产出 `event Attack_Finished_Decrease_UAV_swarm_count`。discover 报「触发与效果被焊在一个事件名里」
——正是 R4.5 干的事。

## 三、归因表：没有任何一方在撒谎

| 环节 | 做对了吗 | 说明 |
| :-- | :-- | :-- |
| 作者建模 | ✅ | 析取源写全、量写在守卫里、触发效果分槽 |
| R4.5 下沉 | ⚠️ 有损但**如实登记** | 债务码写在 `fcstm_meta.json` 里 |
| discover 发现 | ✅ | 它读 `model.fcstm`，看到什么报什么 |
| **评测归因** | ❌ | **把这类报告计入「模型缺陷」——错在这一环** |

**这解释了它为何藏得住，但要准确表述**：本轮八个判定组中，只有一组回读了作者的 `stm0.puml`，
也只有那一组识别出编译债务；其余七组均在编译产物上完成判定并一致判为模型缺陷。

可以主张的是更弱也更准确的一条：**只要评审入口是 IR，这类误归因就会系统性发生，且不会自我暴露。**

仓库其实早有相关裁定未被执行到评测侧——[FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md)：
断言阶段必须接受合并事件并记录表示限制，而「表示限制被如实记录、但记录本身不构成发现」。

## 四、在 paper 里怎么写

**基本立场：这不是要藏起来的瑕疵，也不是要道歉的缺陷——它应当被写成方法论贡献。**

### 4.1 与既有工作的分界，以及外部效度的边界

**与静态分析中久已讨论的 IR 层误报（SSA、去糖、优化引入的伪缺陷）相比，本文的新点不在于
「IR 会引入误报」——那是已知的——而在于这条链把损失写成了机器可读的清单**
（`fcstm_meta.json` 的债务码），于是「多报中有多少不是被测对象的错」第一次成为**可扣除量**，
而非只能定性描述的威胁。本文的贡献是这个扣除动作及其实测规模，不是现象本身。

> 我们在**一条**编译链（PlantUML → FCSTM，R4.5）、**一个**语料、**一个**检测器、**一套**谓词词表
> 上量化了这一现象：278 类去重多报中，129 类（46.1%）源于编译损失而非被测模型。
> 这一比例**不宜外推**到其他源语言、其他目标 IR 或其他检测器；它给出的是**存在性证明与量级参考**
> ——在源语言表达力严格强于目标 IR 时，编译损失在下游多报中的份额可以超过四成，
> 因而不能默认忽略。我们主张的是**审查动作**（凡涉有损编译，须核算这一份额），不是这个具体数字。

⚠️ **单位必须写清**：46.1% 是**去重后的多报类型**份额，不是 issue 条数份额。
按出现格次加权约为 36–40%；按 issue 条数加权的份额本轮未计算。

### 4.2 导出一条方法论主张

> **只在 IR 层做 grounding 是不够的：断言的真值必须相对「源制品 + 编译债务清单」求值，
> 而不是相对 IR 求值。**

两种可操作化实现（论文可只主张原则，实现留作 future work）：

- **强形式**：断言阶段同时可见源制品，谓词在源制品上求值。
- **弱形式（改动最小，不改谓词）**：在**归因侧**对已产出的断言结果打标——凡 `*_declared`
  返回 False，查该制品的债务码，命中则计入债务报告而非缺陷。
  所需信息编译器已写好，**该实现不触及谓词层**。
- **中间形式**：谓词返回三值——`存在` / `作者未表达` / **`作者已表达但编译未保留`**。
  ⚠️ **此形式确实需要改谓词**：返回类型、全部调用点、满足性统计、以及评审端对 `False` 的解释
  都要同步改。本文只主张原则，**未实现**。

### 4.3 ⚠️ 一条**待验证的假设**（不是可发表的设计准则）

| 谓词族 | 未匹配簇中判为漏记 | 合计 |
| :-- | --: | --: |
| `reaches` | 6 | 7 |
| `event_declared` | 17 | 159 |
| `variable_declared` | 0 | 49 |
| `edge_declared` / `persists_until` / 结构类 | 0 | 21 |

⛔ **这张表不能支撑「应优先选用某谓词族」。两处硬伤：**

1. **分母是按结果筛出的子总体。** 它只统计「未匹配到台账」的簇；谓词真正有用时产生的是
   **匹配上的命中**，而命中按构造被排除在这个分母之外。所以它度量的是
   **「该谓词误触发时，误触发的性质是什么」，不度量检出效用**。
2. **命中侧的实测直接反证。** v46 的人工判定理由里，存在性谓词恰是命中主力
   （`initial_target`、`containment`、`cardinality`、`state_declared` 均高频出现），
   而 `reaches` 只对应个位数命中。按本表去砍存在性谓词，会砍掉绝大部分真实检出。

**另外：`reaches` 的 6/7 点估计 95% CI 约为 [0.49, 0.97]**，且原准则写的「可达性、结构、时序」
三族中，**结构（`edge_declared` 0/11、`containment` 0/1）与时序（`persists_until` 0/5）在同一张表里都是 0**
——原表只搬了最高、中、最低三行，恰好略去了反证自己的三行。

**本表支持的、且成立的结论只有一条**：

> **存在性谓词的误触发中，编译债务占绝对多数**（`event_declared` 76/159、`variable_declared` 45/49），
> **而可达性谓词的误触发几乎不含债务成分**（`reaches` 1/7）。
> 这是「债务沿标识符通道传播」的证据，**不是谓词选型建议**。

**若要把它变成选型建议，必须先做词表消融**（以可达性/结构为主的替代词表重跑，比 `hit@k`
与多报构成）。本轮**未做**，故此节归 Future Work。

⛔ 另注意 [METHOD_PROVENANCE_POLICY.md](./METHOD_PROVENANCE_POLICY.md) 的 R1/R3：
「因为我们这条链会压平标识符，所以少用存在性谓词」是**引入动机**，不是**领域出处**，
不得以「方法的一部分」写进方法章节。

⛔ **本研究的谓词词表保持不动**，理由见
[V46_UNEXPECTED_ADJUDICATION.md](./v46/unexpected_adjudication.md) 表 B 下方。

### 4.4 诚实性叙述：写成机制陈述，不写成忏悔

**放 Discussion 的具名小节，不放 Threats。** Threats 的读者预期是「作者列举可能削弱结论的因素」，
把一个**已完成的量化修正**放进去会读成认错，且与 §4.1 的贡献主张自相矛盾——
同一件事不能既是 contribution 又是 threat。Threats 里只留一句指针。

**篇幅**：3–5 句正文 + §三 那张四行归因表。**不写过程叙事，不写「我们一开始归因错了」这类
第一人称忏悔句**，改写成机制陈述：把「我们」换成「任何采用该入口的评审」。

可用的表述：

> 本轮八个判定组中，只有一组回读了作者的源制品，也只有那一组识别出编译债务；
> 七组共享同一个缺失输入，其一致性不构成难度的独立证据。可以主张的是更弱也更准确的一条：
> **只要评审入口是 IR，这类误归因就会系统性发生且不会自我暴露。**

**防御「连带质疑命中率」**（会被问，且路径具体，见 §4.7）。三条隔离证据应写进 Threats：
(1) 命中侧有不依赖人工口径的子集——A 层自动判定要求谓词与绑定逐字相符，可单独报其 `hit@1` 作下界；
(2) 同形态横向复检已做（`adjudication_recheck` 对同形态两种结果逐对复核）；
(3) 判定全部可审计，逐条带 `argument`，随论文公开。

### 4.5 必须一并交代的实验口径修正

- **多报率必须分解**为「真多报 / 表示债务 / NL 无依据」三类。只报总多报率会同时
  高估模型的乱报程度、又掩盖编译链的问题。
- **命中率的敏感性必须量化，不能只说「不受影响」。** 「台账分母不变」是同义反复；
  科学问题是「若把这 4 条补进台账会怎样」。⚠️ **`hit@1` / `hit@3` 的变动很小，
  但 `hit@all` 只会下降**——因为这些真漏记**每一簇都 ≤3/6**，按定义会稀释稳定性指标。
  这与 §4.6 是同一事实的两面，**必须同时给出三个口径的区间**，不得只说「不受影响」。
- **oracle 不完备性首次被量化**：4 条漏记同时构成
  [GROUND_TRUTH_LIMITATIONS.md](./GROUND_TRUTH_LIMITATIONS.md) §6「台账非完备集」的经验确认。
  据此 `hit@k` 应读作**对已知缺陷集的覆盖率**，而非召回率。
  另须履行 [HIT_CRITERION.md](./HIT_CRITERION.md) §4.5 的双读法并列义务。

### 4.6 一并交代的负面结果

[V46_UNEXPECTED_ADJUDICATION.md](./v46/unexpected_adjudication.md) 表 A 第一行：
**23 条真漏记全部 ≤3/6 格，无一达到 ≥4 格；而唯二的 6/6 全满格是表示债务。**

> 模型确实能找到台账外的真缺陷，但**找不稳**；它稳定重复报出的，反而是编译债务。

这条不好听，但它是「`hit@3` 与 `hit@all` 必须分开报」这一口径的最强辩护——
只报单轮数字，这个区别根本看不见。

### 4.7 ⚠️ 对称审计：台账侧尚未查（本轮缺口）

本轮的债务判定**只覆盖了未匹配的 293 类产出**。对称的问题是：
**参与度量的台账记录中，是否有记录本身编码的是编译产物？** 若有，则相应的「命中」是命中在
债务上，`hit@k` 的分子分母同时失真。

已知张力一处：`variable_declared` 在本语料上恒为 False（作者变量 0/60），
而 [HIT_CRITERION.md](./HIT_CRITERION.md) 曾把「模型未声明某变量」列为合法命中形态。
**一个在全语料恒为 False 的谓词，其 `False` 不能作为检出证据**——同一条断言在一个完美模型上
也会「命中」。两份文件对同一谓词给出了不相容的地位。

**待办**：对参与度量的台账记录逐条回读 `stm0.puml`，产出「命中位中有多少条其证据依赖
在全语料恒真/恒假的谓词」的表。**在该表完成前，`hit@k` 只能作为上界报告。**

⚠️ 两侧的失效模式**方向相同**（都偏乐观），所以不能用「命中侧判据更严」搪塞。

## 五、复算命令

```bash
cd project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples
ls */model.fcstm | wc -l                                           # 60 份制品
grep -l "^\s*def " */model.fcstm | wc -l                           # 33 份含 def（其余 27 份无）
grep -h "^\s*def " */model.fcstm | sort | uniq -c                  # 唯一 def 是注入的 R45RouteToken
# ⚠️ 债务码必须按【制品数】数，不能用 uniq -c —— 每码在两个数组里各列一次，会得到 2 倍
for c in opaque_transition_label_semantics concurrent_region_semantics; do
  echo "$c $(grep -l "R45.DEBT.$c" */fcstm_meta.json | wc -l)/60"; done
sed -n '33p' llms_emp_feedback_final_0029/stm0.puml                # 合法析取守卫
grep -n "Front Distance" llms_emp_feedback_final_0010/stm0.puml    # 量写在守卫文本里（9/12/18 行）
grep -n "Attack Finished" llms_emp_feedback_final_0016/stm0.puml   # trigger / effect 已用 / 分槽（34 行）
```
