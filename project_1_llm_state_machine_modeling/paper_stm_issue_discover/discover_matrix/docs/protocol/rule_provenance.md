# 规则来源纪律：让「若我没见过样本会不会写这条」从辩解变成构造事实

## 问题

§3.5 的动机审计判据是：

> 最可靠的判据是查引入动机，不是列举形态：把每条规则的引入 commit 翻出来，看它是不是因为某个具体
> 样本没被发现才写的。

这条判据很强，但它只能**事后**判。而一旦我已经详细分析过「哪些缺陷没被发现」，我写的任何新规则都
落在它的射程内 —— **即使那条规则确实来自规范**。因为动机审计查的是 commit 的时间与上下文，而我的分析
就在那儿。

具体到本轮：裁定要求预注册 ≤6 条合式性公理，并要求「公理表在见到任何样本之前冻结」。但我已经查明
`0032` / `0047` / `0048` 的 6 条漏检全是「复合态缺默认入口」。我若此时写下

$$\forall C \in \mathrm{Composite},\ |\mathrm{children}(C)| \ge 1 \Rightarrow \exists c.\ \mathrm{initial\_target}(C, c)$$

无论我怎么论证它出自 UML 规范，**动机审计都会判它疑似特化，而且判得对**。

## 处置：让盲态成为构造事实，而不是声明

**由一位对失败分析完全盲的执行者从规范推导该表。** 隔离清单如下，
**一律按目录写，不按文件名通配**（理由见下一小节）：

| 类别 | 禁止 |
| :-- | :-- |
| 分析与协议文档 | `discover_matrix/docs/` **整个目录**（`findings/`、`generations/`、`protocol/`、`judges/` 全在其下，本文件自身也在内） |
| 代次报告 | `discover_matrix/` 下的**全部代次目录** `v*/`（当前为 `v46/`；新开一代即自动落入本条，无需改名单） |
| 判定与样本 | `manual_review/`、`verdicts/`、`onepass_sample/`、`blind_sample/`、`telemetry/` |
| 结果性数据 | `discover_matrix/` **顶层的全部 `*.json`**（台账重建、已发布运行清单、已知假阳性、校准矩阵都在这一层） |
| 运行产物 | 仓库根 `runs/` |

**应当读**：`CLAUDE.md` 的建模对象边界、`pyfcstm` DSL 规约与 `diagnostics/codes.yaml`、现有谓词词表、
UML 规范条款。

### 为什么改成按目录（2026-08-11）

本条此前写的是**按文件名通配**：「含 `EXPECTED`、`ISSUE`、`BOTTLENECK`、`LIMITATION`、`HIT_` 的任何
文件」。文档树化把这些文件改成小写并移进 `docs/` 子目录后，**五个通配符同时失配**。实测（2026-08-11，
在 `discover_matrix/` 下，排除 `__pycache__` 与 `manual_review/eis_bundle/`）：

```bash
# 旧名单实际命中：0
find . -type f \( -name '*EXPECTED*' -o -name '*ISSUE*' -o -name '*BOTTLENECK*' \
                  -o -name '*LIMITATION*' -o -name '*HIT_*' \) | wc -l
# 它们的小写同物：20
find . -type f \( -iname '*expected*' -o -iname '*issue*' -o -iname '*bottleneck*' \
                  -o -iname '*limitation*' -o -iname '*hit_*' \) | wc -l
```

那 20 个里就包括 [ground_truth_limitations.md](../protocol/ground_truth_limitations.md)、
[hit_criterion.md](../protocol/hit_criterion.md)、
[predicate_bottleneck.md](../generations/v24/predicate_bottleneck.md)、
`manual_review/expected_issue_set.json`。**名单看上去仍然完整，防护已经全死。**

这与 [blind_judge_prompt.md](../judges/blind_judge_prompt.md) 改动日志 v3 记的是同一次事故的同一个
教训：那份文件的 `V2*.md` / `OVERREPORT_*.md` 两个通配符也在同一次重组中失配，已改为按目录。
**「按形态列举永远漏」在路径层的形态就是「按文件名通配永远漏」** —— 目录不会因文件改名而漏，
文件名会。新增禁读对象时若只能想到文件名，说明它缺一个该归进去的目录。

### ⚠️ 「结果邻接」类文件：必读，但用途受限

`assertions/predicate_api.py` 与 `discover/predicates.py` 是**必读**（公理必须能用现有谓词表达），但它们
当前的 docstring 与注释**含实验结果性内容** —— 具体 pair 编号、代次名（`matrix-v16/v17/v20/v22+v23`）、
条目 ID（`EXP-0000-IT-001`）、语料统计（"51 of 219 False results"、"704 bindings across 58 of the 60
pairs"、"22 of the corpus's 169 composites"）。

⛔ **判断某段文本是否进入实验，不能只 grep `__doc__` / `inspect.getsource`。**
pydantic 会把类 docstring 折进 `model_json_schema()`，而结构化输出的 schema 契约正由它生成——
这条通道在源码里搜不到，它在库内部。**因此：凡是 schema 类的 docstring，一律视同 prompt 文本；
普通函数/模块的 docstring 与 `#:` 注释不进 payload。**

判定方式只有一种可靠：**在末端拦截真实 payload**（system message 全文 + tool schema），
逐条扫描，而不是静态推断。除此之外的结果邻接文本污染的是规则编写侧，不是实验侧。

**用途限制（推导者必须遵守并自查）**：

1. 只把它们当作「某个谓词能否表达某个断言」的**可执行性证据**
2. **不用它们决定收录哪条公理**
3. 产出时必须附一份「哪些判断受结果邻接文本影响」的自查清单

首次盲态推导的执行者**自发做到了这三点**，并因此正确剔除了一条候选公理（「默认入口不得指向 pseudo」——
因为语料的 `pseudo` 标注不一致，该公理的命中分布是语料生产方式的属性而非方法能力）。**但下一位可能
不会自发做到，所以固化为要求。**

📌 长期处置是把结果邻接文本从 docstring 移入 `eval/discover_matrix/` 下的专门文件（docstring 只留机制
说明并链接过去），而**不是删掉** —— 它们记录了真实的发现过程与教训。

这比「我自己写完再论证其实是从规范推的」强，原因是它改变了主张的**类型**：

| | 主张形态 | 可核验性 |
| :-- | :-- | :-- |
| 我自己写 + 事后论证 | 「若我没见过样本也会写这条」 | **不可核验**（我见过了，反事实不可观测） |
| 盲态执行者写 | 「一位没见过样本的人写出了这条」 | **可核验**（隔离清单可查，产出可复核） |

## 每条公理必须带的字段

1. **形式化陈述** —— 全称量化式，**不得含任何具体状态名 / 事件名 / pair 编号**
2. **规范出处** —— UML 条款号或 FCSTM DSL 规约位置，精确到条款，不是「UML 要求」这种泛指
3. **可执行形式** —— 用现有谓词，具体到函数名与参数槽位
4. **界内论证** —— 不涉时钟、不涉不变式、不涉正交区并发
5. **与 pyfcstm 诊断码的关系** —— 若上游已可靠检出，说明为什么方法仍需独立推出（否则建议不收录）

## 冻结后的规矩

- **≤ 6 条**，宁少勿滥 —— 每多一条都是一次特化嫌疑
- 见任何 v25 结果**之前**冻结，60 个 pair 共用一份
- **不允许运行后追加**。追加一条即一次特判嫌疑，须重新走盲态推导
- 激活分布必须可查：公理在已命中格与未命中格上**都**实例化，不集中于任一格

## 与「按构造留出」的关系

[ground_truth_limitations.md](./ground_truth_limitations.md) 与 §3.5.-1 记的「按构造留出」管的是**数据
侧**：在从未参与规则编写的样本上跑。本文件管的是**规则侧**：让编写规则的人从未见过结果。

两者是同一条纪律的两个方向，且**都不可用声明替代**：

    数据侧    留出集不参与规则编写      ← 用 holdout.py --verify 机械核验
    规则侧    规则编写者不见结果        ← 用隔离清单 + 产出复核

⚠️ 本仓库的 hold-out 带划分已按用户裁定**废止**（理由：它服务泛化性声明，而本研究的贡献是从真实模型
归纳问题类型与判定能力，语料即研究对象）。**但规则侧纪律不随之废止** —— 用户保留的红线正是「不得把
答案或不该可见的信息喂进去」，而「照着漏检清单写规则」就是把答案喂进去的一种形态。

## 一条自我提醒

我写这份文件时，公理表还没回来。**这个顺序是有意的**：若先看到表再写纪律，我会不自觉地把纪律写成
「刚好允许那张表」的形状。
