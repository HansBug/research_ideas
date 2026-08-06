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
