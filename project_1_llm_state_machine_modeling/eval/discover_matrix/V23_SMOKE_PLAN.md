# v23 单格试跑方案（复审通过后执行，先于 66 格）

两份 v23 review 都建议：**这道门从未在回路里被测过**，而它会触及历史上 63% 的 containment 绑定。
直接铺 66 格，若门造成大面积隔离，代价是整代次数据。

## 选格：`0029`

| pair | 自前缀 containment | 资格 |
| :-- | --: | :-- |
| `0047` | 64 | ⛔ 承载可报记录 `EIS-0047-03`，**不可用** |
| **`0029`** | **63** | ✅ **历史格（共演化），不消耗任何资格** |
| `0048` | 55 | ✅ 已整格烧毁 |
| `0032` | 26 | ⚠️ 可报 pair，记录已烧 |

选 `0029`：激活面几乎与最高的 `0047` 相同，而它是历史格 —— 试跑它不消耗 hold-out 资格，也不会
因为「看了它的行为」而烧掉任何可报记录。

两条臂各跑一轮（claude + gpt），`BASE` 指向 `/tmp`，**不写进 `runs/`** —— 试跑不是代次数据，
混进去会污染 `run_grid.py` 与历代对比表的口径。

## 要看的三件事（只有活体能答）

1. **生产者第一轮填不填 `source_context.nl_parent`。** 历史里该字段出现 0 次，v23 才教。
2. **若不填、被门拒后，第二轮填不填。** 这是 v22 未接线所担心的形态：「被要求补一个从未被描述过
   的字段，耗尽修复预算，整格被隔离」。
3. **几轮收敛、有没有触发隔离。** 修复预算 5 次且与其它契约错误共用。

## 判据（先于试跑写死）

| 结果 | 判定 | 下一步 |
| :-- | :-- | :-- |
| 两臂都 `coverage=full`，修订 ≤5 | **通过** | 铺 66 格 |
| 某臂 `partial` 且成因是 `revision_budget_exhausted` + 门拒 | **不通过** | 门需再改：或降级为警告（不 raise），或补 reviewer 侧的对应指引 |
| 两臂都填了 `nl_parent` 但门仍拒 | **不通过** | 门的判据有误，回查 |
| 门一次都没触发 | **存疑** | 说明改动 1 已把生产者推向跨层，门是冗余的 —— 那也要如实记，不能当成「通过」 |

第四行值得单说：**门不触发不等于门有用**。若改动 1（修 prompt 矛盾）已经让生产者不再写自前缀
绑定，那门就没有起作用的机会 —— 这时该报的是「改动 1 有效、门未被验证」，而不是「门通过验证」。

## 命令

```bash
cd /home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop
R=/home/zhangshaoang/oo-projects/research_ideas
for prof in claude-opus-4-7 gpt-5.5; do
  PYTHONPATH="$PWD/src:$R" LLM_CONFIG_FILE="$R/.llmconfig.yml" \
    "$R/venv/bin/python" -u -m paper_stm_feedback_loop.discover \
    --pair-id llms_emp_feedback_final_0029 --profile "$prof" \
    --content-language zh-CN --llm-config "$R/.llmconfig.yml" --transport-retries 4 \
    --output-dir "/tmp/v23smoke/0029-${prof%%-*}" > "/tmp/v23smoke/0029-${prof%%-*}.log" 2>&1 &
done; wait
```

复算：

```bash
python3 -c "
import json, glob
for f in sorted(glob.glob('/tmp/v23smoke/*/discover-completed.json')):
    d = json.load(open(f))
    print(f.split('/')[-2], d.get('coverage_status'), len(d.get('issues') or []))
"
grep -c 'nl_parent' /tmp/v23smoke/*/records/*split-requirements-state-update/record.json
grep -oE 'revision=[0-9]+' /tmp/v23smoke/*.log | sort -u | tail -2
```

---

# 试跑结果

## 三个问题的答案

| 问题 | 答 | 依据 |
| :-- | :-- | :-- |
| ① 第一轮填不填 `nl_parent` | **填了**，两臂 `revision=0` 即填 | 结构化字段，非 prompt 回显（逐个 JSON 路径核过） |
| ② 被门拒后第二轮填不填 | **无从得知** | 门 0 次触发 |
| ③ 几轮收敛 | claude `full`，无隔离、无预算耗尽 | 见下 |

## 判定：落在判据表**第四行**

门一次没触发 → **存疑，不是通过**。按试跑前写死的口径，该报的是「改动 1 有效、门未被验证」。

改动 1 的有效性有实测支撑：

| | v22 gpt（同格 6 格） | v23 gpt（试跑） |
| :-- | --: | --: |
| 自前缀 containment（结构上恒真） | 9–11 | **0** |
| 跨层 containment（可判假） | 1–2 | 1 |
| 带 `nl_parent` | 0 / 79 | 1 / 1 |

## 一个推翻了选格依据一半的发现

该 pair 的 63 条自前缀绑定**全部来自 gpt 臂**，claude 臂 0 条 —— claude 本来就在正确跨层锚定。
选格时量的是 pair 级聚合，**聚合把臂间 63/0 分裂抹平了**。所以 claude 臂这一跑对门几乎零信息量；
它的 6 条发现四代次完全同一组（措辞不同、实质一致），是稳定性证据而非改动效果证据。

## 一个我原本会误判的发现

gpt 的 containment 需求从 10–12 掉到 1，**看数字像「需求丢了」** —— 而那正是本轮修改要防的失败
模式。读原文后是**合并**：9 条逐元素自前缀 containment 换成 3 条 `cardinality` 打包（如
「enter_hwy、cruise、lane_change、exit_hwy 应为 HighwayMode 的直接子状态」）。13 个 NL 段两臂全
覆盖，一个没丢。

换来的检查**更强**（自前缀 containment 结构上永远 True；`cardinality` 少一个多一个都失败），但有
真实代价：**只查数量不查身份**，数量对而命名错会漏过。

而需求评审员抓得比我更全 —— 它 `revise` 的理由指出 `count: '5'` 还**凭空引入了 NL 从未声明的
「恰好数量」**。这一条我漏了。报告里两面都要写，不能只报「可判假条数上升」。

## 改动 1 在评审层的直接证据

claude 臂 `decision: accept`，评审员用自己的话背书了 v22 prompt 曾禁止的推断：

> REQ-002 正确地把 InitialState 放在 AutonomousMode 之下（NL 明确称其为 substate），**即使模型
> 将其置于根下，这一 False 正是需求要暴露的问题**，符合 containment 规则。

⚠️ 但**不能**据此说「评审员由攻转守」：v22 的 55 份含 containment 的评审记录里，51 份已有辩护性
措辞，仅 4 份带攻击性措辞。改进在生成侧，不在评审侧。

---

# 66 格运行期观察（滚动记录，第 4 步逐条读时的优先级清单）

## 优先级 1：`0018-claude` 三件事同时发生

| 量 | v22 同格 | v23 run1 |
| :-- | :-- | :-- |
| coverage | `full` | **`partial`** |
| issues | 10 | **5** |
| `coverage_gaps` | 0 | **0** ← 与 partial 自相矛盾 |
| `reported_satisfied` vs `deterministic` | 相等 | **15 vs 14** |
| `unaccounted_safe_false_assertions` | —— | **1** |

`partial` 却 `coverage_gaps = []` 这个组合本身需要解释。而 v22 的 Q3 分析明确记录过
「`reported == deterministic`，无记账偏差 —— 问题不在裁决」，**现在这个等式破了**。

`0018` 是 fork/join 伪状态族，也正是 A1 规则的编写来源。单格单轮不足以定性，但它是本次运行最需要
逐条读的格。`unaccounted_safe_false_assertions` 属「丢发现」类，且是早前呈现里根本没印的两个键之一。

## 已排除的担忧：`EIS-0035-02` 仍命中

`0035-claude` 的 issue 数 5 → 4，但**台账命中未丢**：v23 第 2 条「缺失 DoorOpen 在 Door_Closed 下
回到 DoorShut 的迁移」与台账 statement 语义同一。差别在第 5 条 —— v22 报 `timer_running` 变量未
声明，v23 改报 `during` 动作缺失，是不同的多报项，不是丢了命中。

**这条必须人工读原文才能判**：只看 issue 数会得出「命中丢了」的相反结论。

## 十格同格对照：非系统性回归

issue 净变化 **−2**（0038 +3、0006 +1、0043 +1 vs 0018 −5、0029 −1、0035 −1），coverage 状态变化
1 格。**不是系统性回归**，是噪声加 `0018` 一处大降。

## 优先级 1 的定性结论：归因层把并发造成的 False 标成了 `safe`

追完整条链，`0018-claude` 的记账偏差成因确定，**而它是一条边界类缺陷，不是丢失的发现**。

### 链条

```
REQ-009            「当 Charged=true 时 ChargedFlash 应转移到 Junction3」（NL-L006）
AST-REQ-009-1 主   occupancy_after(ChargedFlash --Charged_true--> TakePicture, ≤5)  → False
AST-REQ-009-2 辅   edge_declared(ChargedFlash --Charged_true--> Junction3)          → True
bind_attribution   status: safe          ← 语义是「这个 False 归因于模型」
裁决器             未发 issue（正确），但把 REQ-009 记为已满足（错）
对账层             抓住：unaccounted_safe_false_assertions=["AST-REQ-009-1"]
                   确定性重算剔除 REQ-009 → 顶层 satisfied 用重算值 14，自报 15
coverage_status    partial（正确反映「有一条需求无法裁决」）
```

### 为什么 False 与模型无关

`join2` 是伪状态且有**两条入边**：`Junction3 -> join2`（闪光分支）与 `choice2 -> join2 : /sunny_false`
（测光分支）；`fork1` 分出 `AutoFocus` / `DetLight` 两条并行分支。从 `ChargedFlash` 单独出发到
`TakePicture` 必须等另一条分支也到达 join —— **这是正交区并发语义**。

按 [CLAUDE.md](../../../CLAUDE.md) 的硬约束，并发语义**排除在 project_1 的断言对象之外**，且
「不得把并发类问题在 project_1 的评测中记为『方法未能检出』」。

**所以真缺陷是：`bind_attribution` 把一条由并发语义造成的 False 标成 `safe`。** 正确处置是识别为
边界外 —— 既不该是 `safe`，也不该落进 `unaccounted` 这个本不该有东西的类别。

### 发生率：罕见且非本代次引入

| 代次 | 有未记账判假断言的格 | 占比 |
| :-- | :-- | --: |
| v21 | 1 / 33 | 3.0% |
| v22 | **0 / 66** | 0% |
| v23（进行中） | 1 / 13 | 7.7% |

1/13 与 1/33 在这个量级不可区分。**不是 v23 回归。** 且对账层抓住了记账错误、确定性重算胜出，
所以**数字没被污染**。

### 追这一条我连错三次，序列本身要记下来

| 判断 | 为什么错 |
| :-- | :-- |
| 「这是丢失的发现」 | 它在边界外，不发布是正确的 |
| 「A1 漏了目标位」 | `_reject_transient_subject` 遍历**全部** bindings；且此处目标 `TakePicture` 本就不是伪状态 |
| 「事件放在 effect 位是真缺陷」 | `chain_id : isabs=SLASH? ID (DOT ID)*` —— 前导 `/` 是**绝对路径标记**。我拿 UML/SCXML 的约定套了这个 DSL |

三次都是**读一行原文就下结论，没查该行所属的约定**。第三次尤其典型：整个模型每条带事件的迁移都写
`: /X`，若 `/` 真是 effect 位，这模型一条 trigger 都没有 —— **那个反证当时就在眼前**。

教训与「机械代理只能定位不能裁定」是同一条的延伸：**人工读原文也需要先确认原文的约定**，否则
「人工读过」只是把错误换了个来源。

## 中期结论（18 格）：形状变了，产量没变 —— 且这是自洽的

| 量 | v22 | v23 | 口径 |
| :-- | --: | --: | :-- |
| 自前缀率（恒真形状） | 62.2% | **35.1%** | 需求层末份，各自全量 |
| 跨层 containment 需求 / 格 | 0.68 | **1.00** | 同上 |
| issue / 格 | 2.83 | 2.72 | **同 18 格** |
| containment issue / 格 | 0.278 | 0.167 | **同 18 格**，n 太小不可解读 |
| 逐格 issue 变化 | —— | 6 升 6 降 6 平 | 同 18 格 |
| `nl_parent` 填充 | 0 / 227 | **37** | 需求层末份 |

⚠️ **我第一次算这个对比时用了「v22 全 66 格 3.62 vs v23 18 格 2.72」，那是取样构成造成的假差异。**
v22 的 66 格均值里含产出更多 issue 的格；同 18 格上 v22 是 **2.83**，不是 3.62。这是本轮同一类错误
（跨不同格集比较聚合量）的第**九**次。

### 为什么「形状改善、产量不变」是自洽的

自前缀 containment **结构上恒真**，本来就从不产出 issue —— 删掉它们不减少发现。而跨层断言只在
**模型真的放错了位置**时判假：改动**暴露**已有缺陷，不**创造**缺陷。若模型很少放错层级，产量自然
不动。

### 这加强了 D-1，而不是削弱

D-1 原本要求声明「containment 增量来自修指令缺陷、不是能力提升」。实测把它**加强成「可能根本没有
增量」**。诚实表述：

> 改动移除了一类恒真断言，使 containment 检查真正可判假；但在本语料上，**可判假并未转化为更多已
> 发布发现**。

18 格仍偏向 run1，最终结论须用全 66 格重算。

## 29 格：因果链最后一环得到验证，但出现一个待验的方差疑点

### 改动 1 的机制在 Q3 诊断的那一格上直接验证

某 pair 的一个格，v22 是**零产出**（`full`、0 issue、12 需求全满足）—— Q3 的诊断是「断言全部返回
True，因为锚在了模型自己声明的层级上」。v23 同格出 **5 条 issue，其中四条正是 containment 发现**：
四个子状态未被正确包含于其应属的复合态（NL 要求直接包含，模型套了一层 `Region`，v22 的自前缀锚定
使断言恒真）。

**这是因果链的最后一环**：锚点位移 → 断言可判假 → 发现被发布。落在当初诊断失败的同一格上。

### 但聚合仍是「不变」，且逐格几乎完全对称

| 量 | v22 | v23 | 变化 |
| :-- | --: | --: | --: |
| issue / 格 | 3.45 | 3.31 | −4 总 |
| containment issue / 格 | 0.276 | **0.345** | **+2**（18 格时是 −2，已转正） |
| 逐格 | —— | —— | 10 升 / 9 降 / 10 平 |

### 待验疑点：两个 pair 上出现臂间反向的大幅变动

```
某 pair  claude +5   gpt −4
另 pair  claude +3   gpt −6
```

同一 pair、同一模型文本、同一 prompt，两条臂朝**相反方向**大幅移动。这不像改动的系统效应，更像
**改动放大了轮间 / 臂间方差**。

⚠️ 若真是方差放大，「产量不变」这个结论就不够：**均值不动而方差变大，对 `hit@all`（三轮全中）是净
损失** —— 稳定性下降直接压低 `hit@all`，即使 `hit@1` 不变。

~~这条只能等三轮全部落盘后用逐轮方差判定。~~

### ⚠️ 已否证 —— 对照 v22 自身噪声后这个疑点站不住

不必等三轮：**v22 自己的逐轮方差已经足够回答它**。

| 量 | 值 |
| :-- | --: |
| v22 自身逐格轮间 SD（均值 / 中位 / 最大） | 1.02 / 0.58 / **2.65** |
| v22 自身逐格轮间极差（中位 / 最大） | 1.0 / **5** |
| v23−v22 同格 \|差\|（均值 / 最大） | 1.64 / **6** |
| 落在 v22 自身极差最大值以内的格 | **21 / 22** |

`round_variance.py` 另给出定性证据：v22 的 22 格里 **18 格被标为不稳定**，逐轮 issue 数如
`13,11,8`、`4,8,7`、`5,0,1`。

所以「臂间反向移动 4–6 条」很可能只是**两次单轮抽样落在各自噪声分布的两端**。

**错误的形状**：我用「单轮 vs 单轮」的差去推断「方差是否变化」，而方差至少需要三轮才能估计。
被混淆的是**位置参数与尺度参数** —— 单轮差反映位置加噪声，推断不出尺度。

📌 值得记住的是：若不做这个对照，我会把一个纯噪声现象写进报告作为「改动的潜在净损失」，而它听起来
相当有说服力（同 pair 同 prompt 反向移动确实反直觉）。**能自我批评的结论同样需要证据。**
