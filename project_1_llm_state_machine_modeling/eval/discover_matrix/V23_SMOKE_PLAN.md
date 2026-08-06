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
