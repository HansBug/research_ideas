# v23 进度

开跑 commit `c7281b5f2`（环境指纹已落，见 `run_manifests.json`）。运行期间 pipeline `src` 零改动。

## 运行

| 项 | 值 |
| :-- | :-- |
| 落盘 | **66/66** |
| 重试 / 耗尽 | 3 / **0** |
| 门拒格 / 隔离格 | 0 / 0 |
| 模型漂移 | **零**（claude 223 + gpt 434 次调用逐次一致） |
| 运行同质 | ✅ `check_run_homogeneity.py v23 --verify` |
| coverage | `full` 59 / `partial` 7 |

三次重试成因：2 次瞬时 schema（`ValidationError: RequirementSet` 收到 `None`）、1 次门致命 raise
（`anchored against frozen model`；该门触发面两代次持平 74/15 vs 76/18，与本轮改动无因果关系）。

## 判定：两位独立盲判者判同一批

固化指令 `BLIND_JUDGE_PROMPT.md` v1 + 预注册判据 `HIT_CRITERION.md`。

| 量 | 值 |
| :-- | --: |
| 配对判定位 | 204 |
| 一致 | **202/204 = 99.0%** |
| **Cohen $\kappa$** | **0.980** |
| 分歧 | 2 处，**都在已烧毁带** |

因此可报带与历史格在 `conservative` / `optimistic` 两策略下完全相同，**无需双报区间**。

## 结果（两代次口径完全对齐：盲判 + 预注册判据 + 100% 覆盖）

| 带 | 指标 | v22 | **v23** | 变化 |
| :-- | :-- | --: | --: | --: |
| **可报** | `hit@1` | 91.7% | **83.3%**（10/12） | −8.4 |
| | `hit@3` | 100.0% | **100.0%**（4/4） | 0 |
| | `hit@all` | 75.0% | **50.0%**（2/4） | −25.0 |
| 已烧毁 | `hit@1` | 34.1% | 34.9~36.5% | +0.8~2.4 |
| 历史格 | `hit@1` | 77.3% | **77.3%**（51/66） | **0** |

逐条：`EIS-0035-02` 双臂三轮全中（① direct）；`EIS-0047-03[claude]` `[1,0,1]`（③ dual）、
`[gpt]` `[1,1,1]`（④ implies）。

**83.3% 与 91.7% 差一个位。** κ = 0.980 说明这不是判定噪声，是轮间波动；历史格两代次逐字相同的
77.3% 印证改动没有系统性移动覆盖率。

## 效率侧（66 格对 66 格，无需任何判定）

| 量（每格） | v22 | **v23** | 变化 |
| :-- | --: | --: | --: |
| 谓词调用总数 | 183.3 | **157.8** | **−13.9%** |
| `occupancy_after` | 50.67 | **38.32** | **−24.4%** |
| `containment` | 10.45 | 9.48 | −9.3% |
| `edge_declared` | 37.65 | 36.65 | −2.7% |
| `reaches` | 33.39 | 31.85 | −4.6% |
| **已发布 issue** | 3.62 | **3.77** | **+4.1%** |
| `coverage_gaps` | 0.06 | **0.18** | +200% |

**机制的直接证据是选择性**：`occupancy_after` 独降 24.4%，声明存在性与可达性几乎不动。

`anchor_shift.py` 独立印证：自前缀 containment 需求占比 **62.2% → 35.1%**、
`source_context.nl_parent` 填充 **0/227 → 37**。

## 已发布

- comment：https://github.com/HansBug/research_ideas/pull/169#issuecomment-5210459691
- 可读 gist：https://gist.github.com/HansBug/3233923a86eed3f9f7ae99a6067e9c30（68 文件）
- 可审计 gist：https://gist.github.com/HansBug/2d5ea968f4325a60d201b13bdbe15cb0（67 文件）

两份均含 66 格 × 3 轮、无截断。⚠️ 各 `README.md` 头部的 `Cells completed: 22/22` 是**单轮**口径，
以 `00-V23-OVERVIEW.md` 为准。

## 未达成项

1. **两个层的可报记录数为 0**（`wellformedness` / `over_specification`），其「70%」在字面上无定义
2. `ambiguous_ground_truth`：NL 第 11 句的顺序读法（台账用）与包含读法（`prompts.py:17` 要求）
   冲突，同时影响两个 pair，需外部裁定
3. 多报核验批间零重叠 → 核验者间一致性未测
4. L-4：单格耗时无上限（一次 splitter 调用流式接收 37 分钟后返回空输出）

## 运行后已修

- **L-1**（日志被重试截断）：`>` 改 `>>` + 尝试分隔行，已 stub 实测三项符合预期
- **`build_gist.py` 未排除 `.try`**：导致 README 写出第三条臂 `claude.try2`、格数 66→24、
  issue 246→82 且无报错。**这是按 `"try"` 排除作废目录的第 7 处**，而我决定「不改 `.try` 命名」时
  只查到 6 处 —— 不完整性本身正是不该改名的核心理由
- **L-2**（`.try<N>` off-by-one）：**决定不改**，理由写进代码注释
