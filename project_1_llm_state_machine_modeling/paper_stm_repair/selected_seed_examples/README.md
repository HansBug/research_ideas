# smoke 用代表性种子样例迷你文库

本目录从 [corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md) 已登记的一手资源中抽取少量代表性 `<NL, STM_0>` 样例，供后续转换器、诊断器、修正循环和评价协议做 **smoke / 最小连通性自检**。这里维护的是可长期复用的静态输入样例，不是 PR 进度表，不是 seed registry 全量事实源，也不是最终实验集合或主结果样本上限。

换言之：本目录回答“后续工具链先拿哪几个静态样例做最小跑通检查”；最终实验池规模、抽样策略、纳入 / 排除统计和主结论仍以 [corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)、后续实验协议和 run record 为准。

## 1. 边界

- 本目录位于 `paper_stm_repair/` 根路径下，故意不放在 `corpora/seed_library/` 内；`seed_library` 继续只负责上游 seed 方法 / 来源事实总账，本目录只负责 smoke 用静态样例。
- 每个子目录只保存一个已经选中的样例。
- 每个样例必须至少包含：`README.md`、`nl.txt`、一个 `stm0.*` 源文件，以及 `source_meta.json`。
- `nl.txt` 必须是作者一手资源中参与生成的原始自然语言输入；不能使用本仓库旧缓存、二手 parquet、人工改写摘要或后续复跑时新写的 NL。
- `stm0.*` 必须是与该 NL 对齐的作者一手生成输出；不能混入 reference model、checking 后结果、人工修正版或本项目后续修正输出。
- `source_meta.json` 必须保存从原始 `pairs.jsonl` 抽出的定位、哈希、生成方式、格式和 trace 字段，便于自动核验；至少包含 `pair_id`、`pair_set_id`、`seed_id`、`generation_actor`、`generation_model_or_method`、`stm_format`、`source_asset_id`、`source_local_path`、`source_locator_type`、`source_locator`、`source_sha256`、`source_pairs_jsonl`、`source_nl_sha256`、`source_stm0_sha256`、`nl_sha256`、`stm0_sha256`、`eligibility_state`、`trace_verified` 和 `hash_scope`。其中 `nl_sha256` 与 `stm0_sha256` 必须能直接校验本目录内 `nl.txt` 与 `stm0.*` 的 UTF-8 字节；`source_nl_sha256` 与 `source_stm0_sha256` 记录来源 `pairs.jsonl` 的原文哈希。若二者不同，必须仅限于 Git 清洁所需的空白规范化，并在 `hash_scope` 中明示，不能发生语义编辑。
- 如果某个样例后续被替换，必须优先在对应一手条目的 `assets/` 与 [corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md) 中修正证据，再同步本目录；不得静默替换文件内容。

## 2. 当前样例清单

| 样例 | 原始条目 | NL 文件 | STM 文件 | 系统 / 场景 | smoke 用途与限制 |
|---|---|---|---|---|---|
| [高层驾驶模块 PlantUML](./llms-emp-gpt4o-hldcs/README.md) | [llms-emp-stm-subset](../corpora/seed_library/llms-emp-stm-subset/) | [nl.txt](./llms-emp-gpt4o-hldcs/nl.txt) | [stm0.puml](./llms-emp-gpt4o-hldcs/stm0.puml) | 人工驾驶 / 自动驾驶模式切换的高层驾驶模块 | 强相关 LLM + SysML / PlantUML 样例；必须隔离 reference 与 checking 列。 |
| [自助结账系统 Umple](./sefm-ssc7-umple/README.md) | [sefm-llm-state-machine](../corpora/seed_library/sefm-llm-state-machine/) | [nl.txt](./sefm-ssc7-umple/nl.txt) | [stm0.ump](./sefm-ssc7-umple/stm0.ump) | 超市自助结账机 SSC7 的交互式 reactive system | 真实长系统描述 + Umple 输出；当前该论文制品中只有 SSC7 有生成输出。 |
| [微波炉控制 PlantUML](./llms-emp-deepseek-microwave/README.md) | [llms-emp-stm-subset](../corpora/seed_library/llms-emp-stm-subset/) | [nl.txt](./llms-emp-deepseek-microwave/nl.txt) | [stm0.puml](./llms-emp-deepseek-microwave/stm0.puml) | 微波炉门、物品、烹饪时间、启动 / 取消 / 计时器到期控制 | EMP empirical 中较复杂的控制系统样例；R3.1 仅在进入官方 SCXML 前去除 PlantUML `stm ...` 标题，raw STM_0 不覆盖，不计 repair gain。 |
| [自主驾驶与碰撞规避 PlantUML](./llms-emp-kimi-autonomous-collision/README.md) | [llms-emp-stm-subset](../corpora/seed_library/llms-emp-stm-subset/) | [nl.txt](./llms-emp-kimi-autonomous-collision/nl.txt) | [stm0.puml](./llms-emp-kimi-autonomous-collision/stm0.puml) | 自动驾驶高速 / 城市模式切换与碰撞规避 | 较高难度 LLM PlantUML 样例；官方 SCXML 可导出，条件标签只作转换/表示桥 smoke，不自动解释为严格 guard。 |

## 3. 覆盖关系

| 覆盖维度 | 当前覆盖 | 仍需注意的限制 |
|---|---|---|
| 来源形态 | 四个可直接回溯的一手 `NL + generated STM_0` 来源 | 不包含只有源码可复跑、但作者未公开生成输出的条目。 |
| STM 方言 | PlantUML、Umple | 尚未覆盖作者一手公开的 FSM JSON / CSV generated pair；TTool XML 暂不进入四例正向 smoke。 |
| 数据形态 | EMP 1×N 多模型输出、单例长 NL、较复杂微波炉控制、较高难度自动驾驶多条件 PlantUML | 四例只是 smoke 用最小静态样例，不是主实验池规模上限。 |
| 风险覆盖 | reference/checking 泄漏隔离、长 NL、timer-like 语法、R3.1 pre-SCXML normalization 回灌、层次化 PlantUML、条件标签降级、较高难度多条件 PlantUML | TTool XML 与 Unified synthetic 仍保留在 seed registry / 历史 evidence 中作为后续专项对象，但不再作为当前四例 smoke。 |

## 4. 维护纪律

1. 本目录不复制 [corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md) 的全量事实表；每个样例只保存最小可读输入、源文件和中文解释。
2. 逐条资源数量、哈希、locator、raw 文件和 validator 结果以 [corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)、单条目 `seed_resource_registry.json` 与对应 `assets/README.md` 为准。
3. 子目录 `README.md` 必须包含：系统说明、NL 文件说明、STM 文件说明、NL 中文完整翻译、原始论文 PDF / 全文提取 / BibTeX / 文库相对路径、生成关系和 caveat。
4. 后续真实运行应另建 run record，记录使用的样例版本、输入、输出、错误、工具版本和 eligibility；不要把运行状态写回本目录作为流程台账。

## 5. 结构与哈希一致性自检

维护者新增或替换样例后，至少应执行下列检查，确认每个样例具备必需文件，且 `source_meta.json` 中的 hash 能直接校验当前 `nl.txt` / `stm0.*`：

```bash
# 请在仓库根目录运行。
python - <<'PY'
from pathlib import Path
import hashlib, json
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples')
for d in sorted(p for p in base.iterdir() if p.is_dir()):
    for name in ['README.md', 'nl.txt', 'source_meta.json']:
        assert (d / name).exists(), f'{d}: missing {name}'
    stms = [p for p in d.iterdir() if p.name.startswith('stm0.')]
    assert len(stms) == 1, f'{d}: expected exactly one stm0.* file, got {stms}'
    meta = json.loads((d / 'source_meta.json').read_text())
    assert hashlib.sha256((d / 'nl.txt').read_bytes()).hexdigest() == meta['nl_sha256'], d
    assert hashlib.sha256(stms[0].read_bytes()).hexdigest() == meta['stm0_sha256'], d
    for field in ['generation_actor', 'generation_model_or_method', 'stm_format', 'source_pairs_jsonl', 'source_local_path']:
        assert meta.get(field), f'{d}: missing {field}'
    source_pairs = (d / meta['source_pairs_jsonl']).resolve()
    assert source_pairs.exists(), f'{d}: missing source pairs {source_pairs}'
    assert any(json.loads(line).get('pair_id') == meta['pair_id'] for line in source_pairs.read_text().splitlines()), \
        f'{d}: pair_id not found in {source_pairs}'
    assert meta['trace_verified'] is True, d
    print(d.name, stms[0].name, meta['stm_format'], 'ok')
PY
```
