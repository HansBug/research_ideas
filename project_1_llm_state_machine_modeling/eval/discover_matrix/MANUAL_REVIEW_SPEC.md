# 逐 pair 人工审阅规范

## 你在判断什么

对每个 pair，判断**作者生成的 STM_0**（`pairs/<case>-author.puml`）相对**参考 STM_0**
（`refs/<group>-reference.puml`）有哪些**真实问题**。

**核心要求：不做机械的元素存在性比对。** 名字不同、结构不同、拆分方式不同，只要**语义上说得通**，
就必须标为 `correct` 或 `similar`，不能算问题。例如：

- `human_mode` vs `HumanDrivingMode` → 同一状态，`similar`（仅命名风格差异）
- `avoid_frontend_collision` vs `F` → 同一状态，`similar`（缩写）
- 参考用两条边 `A→B`、`B→C`，生成用一条 `A→C` 并把 B 的语义并入 → 判断这是否丢失了 NL 要求的中间状态；
  若 NL 未要求 B 可观测，标 `similar`
- 参考把三个区域写成 `--` 并发区，生成写成三个顺序子状态 → 这是**语义差异**（并发 vs 顺序），标为问题，
  但要注明它属于正交并发类
- 参考 `[*] --> A : power_on`，生成 `[*] --> A`（无触发）→ **真问题**（丢失触发条件）

## 判定档位（每条差异一个）

| 档位 | 含义 |
| --- | --- |
| `correct` | 生成方与参考在该点语义等价，写法不同而已 |
| `similar` | 有差异但语义上说得通、不违反 NL；记录差异内容 |
| `problem` | 真实问题：违反 NL 或丢失参考模型所承载的语义 |
| `extra` | 生成方多出参考模型没有、NL 也未要求的元素（over-specification） |
| `uncertain` | 证据不足以判定，说明卡在哪 |

## 每个 pair 必须产出

1. **逐条差异清单**：每条给出 `档位` + 参考侧内容 + 生成侧内容 + **理由**（为什么这样判）
2. **该 pair 的问题总数**（只数 `problem` 与 `extra`）
3. **每个 `problem` 的可断言性**：能否用当前 19 个谓词写出一条正向断言（给出建议的断言形式；
   不必实测，但要说明该谓词是否存在）
4. **与三份既有记录的对照**：
   - 论文的 per-case 记录（`paper_reported_problems.json` 里该 case 的
     `format_hallucinations` / `grammar_hallucinations` / `semantic_hallucinations` 与各 `resolved`）
   - 论文的 Phase-I / Phase-II F1（同文件的 `f1_phase1` / `f1_phase2`）
   - 台帐的 E1（`ledger.json` 的 `findings` 中 `issue_id` 含该 case 号的条目）
   逐条说明：你判的 `problem` 里哪些已被论文记录、哪些已被台帐记为 E1、哪些**两者都没有**

## 重要背景（避免误判）

- 语料的 `pairs/<case>-author.puml` 是论文 **Phase-II 语义检查后**的产物（workbook 列 AE），
  不是 Phase-I 原始生成。所以论文 `semantic_hallucinations` 里记的问题**可能已在这份制品中被修好**，
  `semantic_resolved = 1.0` 即论文声称已修。你审的是**这份最终制品**。
- 参考模型是论文作者**人工重建**的，论文 §7 自认 "we manually created them, which is subjective"，
  §4.2(4) 说 "we **assume** the reference model is semantically correct"——其正确性未经独立验证。
  **若你认为参考模型本身有问题或与 NL 不一致，必须记录**（档位用 `uncertain` 并说明）。
  已知一例：HLDCS 的 `in (auto final)` 参考模型写成三条独立迁移，但方向与 NL 相反。
- 本研究的建模对象是 **FSM / HSM / EFSM**，不含时钟与正交并发。所以并发类与时间类差异要
  **照实记录**，但在档位后额外标 `out_of_scope: concurrency` 或 `out_of_scope: timing`，
  以便汇总时能分开统计。

## 输出格式

对你负责的每个 pair，输出一个 JSON 对象（全部 pair 汇成一个 JSON 数组），字段：

```json
{
  "case": "0000",
  "group": "NL08",
  "llm": "GPT-4o",
  "diffs": [
    {"verdict": "problem", "ref": "human_mode --> [*] : power_off",
     "gen": "[*] --> FinalState : Power Off",
     "reason": "NL 第5句要求运行模式在断电时进入终态；生成模型唯一的 Power_Off 边从伪初始发出，任何运行态都无断电出边",
     "assertable": "occupancy_after(source=HumanDrivingMode, trigger=Power_Off, target=FinalState)",
     "predicate_exists": true, "out_of_scope": null}
  ],
  "problem_count": 3, "extra_count": 1,
  "vs_paper": "论文语法栏记 transition does not connect two state（已 resolved）；语义栏 None。我判的 3 个 problem 中 0 个被论文记录",
  "vs_ledger": "台帐有 EXP-0000-IT-001，对应我的第 1 条 problem",
  "notes": "自由文本，记录你对该 pair 的整体判断与任何存疑处"
}
```

同时输出一段**该组的总体分析**（自由文本）：这 6 个 LLM 在同一份 NL 上的表现差异、
共性问题、参考模型本身的可疑处。
