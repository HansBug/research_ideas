# 表示债务（representation debt）：现象、机理、以及在 paper 里怎么写

本文件把 v46 意外发现裁定中最重要的一项结论固化为长期研究事实。
实测数据与逐簇判据见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)、
[V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)、
[V46_UNEXPECTED_MERGED.md](./V46_UNEXPECTED_MERGED.md)。

## 〇、定义

> **表示债务（representation debt）**：源制品到分析用中间表示（IR）的编译过程中丢失的语义，
> 在 IR 上表现为可被自动检测器命中的「缺陷」，但在源制品上并不存在。

**定义类型**：本研究新造。

**rationale**：既有概念里最近的是 model-driven engineering 的 *transformation fidelity* 与
*semantic gap*，但那两个词描述的是「转换保不保语义」这一转换自身的属性；本研究要命名的是
**它的下游后果**——转换损失被下游自动检测器当成被测对象的缺陷报告出来，从而系统性污染评测。
据目前所见，这一后果没有被量化过，故另立名目。

**操作化判据**（可机械执行）：一条产出被判为表示债务，当且仅当

1. 该产出所陈述的事实在 IR（`model.fcstm`）上**客观为真**；且
2. 该义务在源制品（`stm0.puml`）上**已被作者逐字表达**；且
3. 编译器已在 `fcstm_meta.json` → `source_static_reason_codes` 中登记对应债务码。

三条缺一不可。第 2 条是与「真缺陷」的分界线：0036 的 `/ UAV Count Decreased` 作者写了 → 债务；
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

全语料债务码分布（`grep -ho 'R45\.DEBT\.[a-z_]*' */fcstm_meta.json | sort | uniq -c`）：

| 债务码 | 次数 | 含义 |
| :-- | --: | :-- |
| `opaque_transition_label_semantics` | 116 | 整条迁移标签被压成一个不透明事件名 |
| `composite_source_activation_dispatch` | 56 | 复合态出边的激活派发被改写 |
| `opaque_state_body_semantics` | 54 | 状态体描述行被压进状态名 |
| `missing_explicit_initial` | 32 | 缺显式初始，注入伪初始态 |
| `multiple_initial_fanout` | 18 | 多初始扇出 |
| `concurrent_region_semantics` | 18 | 并发区语义被改写 |
| `composite_source_external_reentry` | 14 | 复合态外部重入 |
| `ambiguous_unlabeled_fanout` | 12 | 无标签扇出歧义 |
| `invalid_source_initial_target` | 10 | 非法初始目标 |
| `explicit_concurrency_pseudostate` | 6 | 显式并发伪态 |
| `invalid_source_final_scope` | 4 | 非法终态作用域 |
| `source_input_normalization` | 2 | 源输入归一化 |

## 二、三个实例

### 例 1：析取守卫 → 一个事件名（64 簇，最大一块）

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

### 例 2：变量 → 烧进事件名（38 簇）

作者写 `Front Distance > 10` 作为守卫文本。**PlantUML 没有变量声明语法**——
无法写 `int front_distance;`。下沉后成为 `event front_distance_10`。

后果：`variable_declared(front_distance)` 返回 False。而该谓词在**全语料 33 份制品上恒为 False**
（唯一的 `def` 是转换器注入的 `R45RouteToken`），即它在本语料上不携带任何判别信息。

### 例 3：`trigger / effect` 焊死（7 簇）

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

这也解释了它为何藏得住：八个独立判定组里有七组读了 `model.fcstm` 原件、逐条核对，全判成真缺陷；
**只有回到 `stm0.puml` 才看得见**。

仓库其实早有相关裁定未被执行到评测侧——[FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md)：
断言阶段必须接受合并事件并记录表示限制，而「表示限制被如实记录、但记录本身不构成发现」。

## 四、在 paper 里怎么写

**基本立场：这不是要藏起来的瑕疵，也不是要道歉的缺陷——它应当被写成方法论贡献。**

### 4.1 命名一个普遍现象

任何「把半形式化制品（PlantUML / SysML / Simulink）编译成形式化 IR 再自动分析」的工作都会遇到它。
我们给出名字、操作化判据（§〇）与**实测占比 111/293 = 37.9%**。占比数字是本研究的独有贡献。

### 4.2 导出一条方法论主张

> **只在 IR 层做 grounding 是不够的：断言的真值必须相对「源制品 + 编译债务清单」求值，
> 而不是相对 IR 求值。**

两种可操作化实现（论文可只主张原则，实现留作 future work）：

- **强形式**：断言阶段同时可见源制品，谓词在源制品上求值。
- **弱形式**（改动小）：谓词返回三值而非二值——`存在` / `作者未表达` /
  **`作者已表达但编译未保留`**，第三种计入债务报告而非缺陷。
  所需信息编译器已写在债务码里，**不需要改谓词一行代码**。

### 4.3 一条有因果解释的设计准则（最硬的一张表）

| 谓词族 | 簇数 | 有效率（真漏记占比） |
| :-- | --: | --: |
| `reaches`（可达性） | 7 | **86%** |
| `event_declared`（存在性） | 159 | 11% |
| `variable_declared`（存在性） | 49 | **0%** |

**存在性谓词几乎全是噪声，可达性 / 结构谓词才有产出，而原因可推导**：
存在性问的是「某标识符在不在」，标识符恰是编译压平时最先失真的东西；
可达性问的是图结构，图结构在编译中保形。由此得到设计准则：

> 在存在表示债务的编译链下，应优先选用**对编译保形**的谓词族（可达性、结构、时序），
> 慎用对**标识符敏感**的存在性谓词。

⛔ **注意：这条准则是给「未来设计谓词词表的人」的，不是给本轮实验的整改指令。**
本研究的谓词词表**保持不动**，理由见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md) 表 B 下方：
失真源在编译不在谓词；中途改词表会作废 v37→v46 全部跨代次可比性；且 0% 有效率这一行**本身就是证据**。

### 4.4 诚实性叙述

**建议明写「我们一开始归因错了」**，理由二：

1. 这正是该现象**难以察觉**的证据——八组独立人工判定里七组栽在同一处，只有回读作者源才发现。
   比空口说「容易误判」有力得多。
2. 审稿人若自行发现你把编译债务算作模型缺陷，杀伤力远大于你自己说。

### 4.5 必须一并交代的实验口径修正

- **多报率必须分解**为「真多报 / 表示债务 / NL 无依据」三类。只报总多报率会同时
  高估模型的乱报程度、又掩盖编译链的问题。
- **命中率 `hit@k` 不受影响**——真漏记只有 6 条且台账分母不变。这一点要明说，
  否则读者会以为整个结果都动摇了。

### 4.6 一并交代的负面结果

[V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md) 表 A 第一行：
**26 条真漏记全部 ≤3/6 格，无一达到 ≥4 格；而唯二的 6/6 全满格是表示债务。**

> 模型确实能找到台账外的真缺陷，但**找不稳**；它稳定重复报出的，反而是编译债务。

这条不好听，但它是「`hit@3` 与 `hit@all` 必须分开报」这一口径的最强辩护——
只报单轮数字，这个区别根本看不见。

## 五、复算命令

```bash
cd project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples
grep -h "^\s*def " */model.fcstm | sort | uniq -c                  # 33× R45RouteToken，无作者变量
grep -ho 'R45\.DEBT\.[a-z_]*' */fcstm_meta.json | sort | uniq -c | sort -rn
sed -n '33p' llms_emp_feedback_final_0029/stm0.puml                # 合法析取守卫
grep -n "Front Distance" llms_emp_feedback_final_0010/stm0.puml    # 量写在守卫文本里（9/12/18 行）
grep -n "Attack Finished" llms_emp_feedback_final_0016/stm0.puml   # trigger / effect 已用 / 分槽（34 行）
```
