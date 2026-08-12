# X1 · 朴素基线对照臂（naive baseline arm）

本目录是 paper1 有效性实验的**对照组**：同样两个执行模型、同样 54 个 pair、同样 3 轮，⛔ **不走八阶段循环**，一个提示直接让它列出模型相对需求的不符之处。它存在的唯一理由是——主臂的 $\mathrm{hit@1} \le 355/588 = 60.4\%$ 至今**没有任何参照系**。

> ⭐ **它不是新设计，是执行一个排了很久的第一优先项**：[../experiment_design/next_round.md](../experiment_design/next_round.md) §B1「朴素基线」被 v46 报告列为第一项，且那一节挂着的 `TODO(后续PR)` 逐字写明缺三样——**(1) 基线 prompt 本身 · (2) 自由文本产出如何进入现有判定链 · (3) 判定预算的分配决定**。⛔ 本目录就是把这三样做掉，⛔ 不在别处另建一份设计。

⛔ **主臂一格都不重跑。** 588 冻结完全成立：X1 **新增一个臂**，⛔ 不改主臂的分母、不改门、不动主臂任何数字。

## 1. 与主臂共用什么、⛔ 不共用什么

〔用户明确裁定 2026-08-11〕**「真正两类公用的只有一条，那就是得是同一份输入源头，甚至是否都输入 fcstm stm0 也是不必的，因为模型转换也是我们的方法的一部分」「如果是有效性实验的话那三个都别用，就最朴素」。**

⭐⭐ **这条裁定的来历值得记住**：最初提的三条「公平性要求」——给同一份 `model.fcstm`、给证据链字段、给闭合谓词词表——⛔ 恰好就是本文的三条 contribution。把它们给对照臂等于把贡献白送。

| 项 | 主臂（feedback loop） | X1 朴素臂 | 归属 |
| :-- | :-: | :-: | :-- |
| `nl.txt`（原始需求文本） | ✅ | ✅ | ⭐ **唯一共用项** |
| `plantuml.puml`（上游原始 stm0） | ✅ | ✅ | ⭐ **唯一共用项** |
| `model.fcstm` / 中间表示 / 工作契约 | ✅ | ⛔ 不给 | **C-①**（模型转换是方法的一部分） |
| 19 条闭合谓词词表 / 断言 schema | ✅ | ⛔ 不给 | **C-②** |
| 证据链字段（`named_elements` / 需求条目绑定 / 定位 trace） | ✅ | ⛔ 不给 | **C-③** |
| 8 阶段循环（② 需求审查 / ④ 静态预检 / ⑤ 断言审查 / ⑦⑧ 裁决） | ✅ | ⛔ 不给（单次调用） | **C-①** |
| pyfcstm 的 parse / inspect / sim 任何输出 | ✅ | ⛔ 不给 | **C-①** |

⛔ **消融臂（三条各消融各自）不在本目录范围内**，它归 [../experiment_design/next_round.md](../experiment_design/next_round.md) §B2，且 §B2 自己写明依赖 B1 先落地。⚠️ X1 只做**有效性对照臂**这一件事。

### 1.1 ⭐ 这条边界由一条测试机械保证，⛔ 不靠注释

[tests/test_isolation.py](./tests/test_isolation.py) 断言 `src/` **一个 `paper_stm_feedback_loop` 模块都不引入**（连 `pyfcstm` 也禁——它的 parse / inspect / sim 按 §4B.1 归 C-①）。

⭐ 判据刻意取最强形态：⛔ 不是「不 import 谓词 / schema / 证据链模块」（那要枚举模块名，漏一个就失效），而是「一个都不进来」。代价是 transport 重试要自己写约 50 行。⚠️ 理由是实测数据：**靠约定隔离的遵守率 0/2，物理隔离 2/2。**

四层检查：静态 AST（源码里没有那条 import）· 动态绕道（⛔ 无 `importlib` / `__import__`）· 依赖面白名单（新增依赖必须先改断言，那一步就是审查点）· 干净子进程（`sys.modules` 里没有它）。

## 2. 「最低限度」的下限在哪

⭐ 用户的目标有两层，⛔ 二者不可互换顺序：**① 在学术上说得通；② 在 ① 的前提下尽可能低配**。所以「低配」是**受 ① 约束的优化**，⛔ 不是独立目标。

⛔ **稻草人是本子 PR 的头号学术风险。** 逐条对照表（给了什么 / 省了什么 / 为什么省了仍说得通）在 [prompt/README.md](./prompt/README.md) §2，泄漏审查的两个方向在同文件 §4。

⭐ 可判定的下限判据：**对照臂必须是「一个称职的实践者手上只有一个 LLM、没有我们的方法时，会真的这么做」的那个东西。**

## 3. 目录

```
baseline_arm/
├── README.md                 ← 本文件
├── preregistered.md          ← ⭐ 事前登记；⛔ 跑格之前已 push，远端时间戳可证
├── judging_instructions.md   ← ⭐ 判定指令，发给每个判定组的**物理同一份**文本
├── prompt/
│   ├── naive_v1.txt          ← ⭐ prompt 唯一真源（代码从这里读，⛔ 不内联副本）
│   └── README.md             ← 设计说明 + 三栏表 + 泄漏审查记录
├── src/          ← ⭐ **对照臂实现**（被测对象）。⛔ 零 import 主臂
│   ├── schema.py             ← 最小输出契约：issue / where / reason 三个自由文本字段
│   ├── runner.py             ← 单格执行
│   └── launch.py             ← 324 格编排，幂等、可中断续跑
├── analysis/     ← ⭐ **评测分析**（测量工具）。⭐ 与主臂**共用判定链**
│   ├── present.py            ← 判定材料生成（并列呈现，⛔ 不匹配、⛔ 不判定）
│   ├── verdicts.py           ← 判定表骨架 / C 层闸 / 格式 A→B 转换
│   ├── merge_verdicts.py     ← 合并各判定组结果并过闸
│   └── recheck.py            ← 横向复核（同形态判出两种结果的定位）
├── tests/
└── results/
    ├── smoke/                ← ⭐ prompt 冻结证据（见 §5）
    ├── verdicts_x1.json      ← 逐位人工判定表（与 `v46_human.json` 同构）
    └── ...                   ← 指标、多报侧裁定、与主臂并排的对照表
```

### 3.1 ⭐⭐ `src/` 与 `analysis/` 的分界是**学术边界**，⛔ 不是文件组织偏好

| | `src/` | `analysis/` |
| :-- | :-- | :-- |
| 角色 | **被测对象** | **测量工具** |
| 隔离 | ⛔ **零 import 主臂**（`paper_stm_feedback_loop` / `pyfcstm` 一个模块都不许进） | ⭐ **共用主臂判定链**（`adjudication_recheck` 的 `element_forms` / `coverage`、`metrics_at_k` 的分母口径） |
| 理由 | 它是「三条 contribution 一条都没给」这句话的**唯一机械证据** | 两臂必须用**同一把尺子**量；各写一份实现会漂移，⚠️ 而那比违反隔离更严重——它会让两臂的分母或元素抽取悄悄不同 |
| 由谁钉住 | [tests/test_isolation.py](./tests/test_isolation.py) 四层检查 | [tests/test_denominator_matches_authority.py](./tests/test_denominator_matches_authority.py) 与权威实现逐条对拍 |

⚠️ **方向也是硬的**：`analysis/` → `src/` 的 import 合理（分析要读实现声明的语料位置，⛔ 且不能复制一份路径常量——那会让两臂读到不同输入而看不出来）；⛔ 反方向不许。

⭐ 按仓库根 [CLAUDE.md](../../../CLAUDE.md) §9.5「顶层只放公共资产」：X1 的资产**只服务这一篇论文**，⛔ 故收在论文 subdir 内，⛔ 不放 project_1 顶层。

⚠️ 逐格原始产出落 `runs/paper1/x1-baseline-v1/`（该目录被 `.gitignore` 整目录排除）；⭐ **判定表、指标、报告一律入库**。

## 4. 怎么复现

⛔ **不需要也不应该 `source .env`**——仓库没有 `.env`，配置真源是仓库根的 `.llmconfig.yml`，凭据由 `--profile` 决议（[CLAUDE.md](../../../CLAUDE.md) §5.1）。

```bash
# cwd = 仓库根
python -m pytest project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm/tests -q

# 单格
python .../baseline_arm/src/runner.py --case 0000 --profile gpt-5.5 --output-dir /tmp/probe

# 全网格（54 × 2 × 3 = 324），16 并发
python .../baseline_arm/src/launch.py \
    --output-root runs/paper1/x1-baseline-v1 --parallel 16
```

⚠️ `launch.py` 在开跑前会主动查一次残留工作进程，⛔ 有残留就拒绝启动。理由见该文件 docstring：两个写者写进同一输出目录会产出**静默污染**的记录，而症状看起来像刚改的代码引入的回归。

## 5. ⭐ prompt 冻结证据

[results/smoke/](./results/smoke/) 存着两份真实 smoke record（`0000-gpt` / `0000-claude`，2026-08-11 20:53 UTC）。它们的意义**不是**「代码能跑」，而是**冻结时刻的锚**：

⚠️ smoke 跑完后，那两格的产出**已经被查看过**。所以从那一刻起改 prompt 就等于「按结果调 prompt」，属 §3.5 条款「评测口径迁就结果」的同类问题。⭐ 冻结可核验：两份 record 都带 `prompt_sha256 = 17e5067b…`，与 `prompt/naive_v1.txt` 当前哈希逐字符一致；正式网格每一格的 record 里同样有这个字段。⛔ 若正式网格的哈希与它不同，那次运行作废。

## 6. 判定与分析

| 项 | 口径 |
| :-- | :-- |
| 分母 | ⭐ **同一份台账的 98 条 REPORTABLE**，⛔ 不另立分母。网格恒为 54 × 2 × 3 = **324 格** |
| 覆盖侧 | ⭐ 同一套 `hit@1` / `hit@3` / `hit@all` 三口径同报 |
| 多报侧 | ⭐ 同主臂的五类裁定 + 双分母（条目 / 去重） |
| 判定方式 | ⭐ **全人工逐位**，与 v46 那轮同判定者、同判据（[hit_criterion.md](../discover_matrix/docs/protocol/hit_criterion.md) · [verdict_methodology.md](../discover_matrix/docs/protocol/verdict_methodology.md)，⛔ 一字不改） |
| 机械代理的边界 | ⭐ 脚本**只许并列呈现**，⛔ 裁定必须人工读原文 |
| 读哪份制品 | ⭐ 判定时读 `plantuml.puml`（作者源），⛔ 不读 `model.fcstm`（编译产物）——否则会把编译债务当成模型缺陷 |

⚠️ **两臂之间已知的口径不对称**（必须放正文、⛔ 不放脚注）与 X1 做不了的分析项，逐条列在 [preregistered.md](./preregistered.md)。

## 7. ⛔ 不得声称超出数字支持的范围

⚠️ v46 的逐轮 `hit@1` 极差是 **2.0pp**，⛔ **任何小于这个量级的臂间差异都不可归因**。且这 2.0pp **不是方差估计**（$n = 3$、未计需求族聚类）——⛔ 事前登记必须显式承认这把尺子的局限。

⛔ 并且：`60.4%` 一位不动，主臂的任何数字不因本臂而改。
