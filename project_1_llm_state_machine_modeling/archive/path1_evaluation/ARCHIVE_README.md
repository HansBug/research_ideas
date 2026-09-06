# `path1_evaluation/` 复活导引（ARCHIVE_README）

> 本文件是**归档后新增**的复活导引，不覆盖冻结时的原件。
> 原始文档：[README.md](./README.md)（原 `eval/README.md`，标题「`eval/` — Path 1 评测基础设施」）、
> [PROTOCOL.md](./PROTOCOL.md)（中文评测协议 + paper-claim + 评审规则）。
>
> 上级入口：[../README.md](../README.md)。

## 0. 是什么

**Path-1 评测链**：一条「LLM 初审 + 人类签字」的 5 阶段流水线，产出 **component-level P/R/F1**。

```text
1.选样 -> 2.建 ref(人工签字) -> 3.跑预测 -> 4.双 LLM 标注 -> 5.汇总 P/R/F1 + macro
```

评测对象是 5 类 component：`states` / `transitions` / `guards` / `actions` /
`hierarchical_states`（见 [extract/schema.py](./extract/schema.py) 的 `COMPONENT_KINDS`）。
**不评** `parallel_regions` / `history_states`——这与 [../../../CLAUDE.md](../../../CLAUDE.md)
里 project_1 排除并发/时间的建模边界一致。

核心方法学资产（即使不复活也值得读）：

- **双标注者一致性自动预勾选**：claude 与 codex 完全一致的行自动勾选，只把不一致 / 单票 /
  双方未提案的行推给人类复议。这是把人工评测成本压下来的具体做法。
- **拒绝在评审不完整时出数**：[aggregate.py](./aggregate.py) 只计 `user_final_status` 行，
  未签字行单独报告；[report.py](./report.py) 用 `UnsignedRowsError` 硬拦。
- **标注 prompt 与协议分离**：[annotate/prompts/annotate.txt](./annotate/prompts/annotate.txt)
  对应 paper §IV 协议，[PROTOCOL.md](./PROTOCOL.md) 是人类侧规则。

## 1. 为什么弃用

**语料完全不同，这是它与当前工作无关的最硬证据。**

| | path1_evaluation | 当前 discover |
|---|---|---|
| 语料 | `abs-fsm-brake-control`、`automatic-elevator-controller` 两个 mock case | `llms_emp_feedback_final_0000..0059`，共 60 pair（评测网格 54 pair） |
| 位置 | [data/sources/](./data/sources/) | [../../paper_stm_issue_discover/selected_seed_examples/](../../paper_stm_issue_discover/selected_seed_examples/) |
| 指标 | component-level P/R/F1 + macro | issue 台账命中制，按 `hit@1` / `hit@3` / `hit@all` 报 |
| 判定 | 双 LLM 初审 + 人类签字 | 人工判定 + 机械代理定位 |

两边的 case 集合**零交集**。此外任务口径也换了：Path-1 评的是「生成出的 STM 与 ref STM 有多像」，
当前论文评的是「给定 `<NL, STM_0>` 能不能发现 STM 里的 issue」。

冻结时间：创建于 `ff1e90ff`（2026-05-27 00:05:26），最后一次内容变更是
`52535008`（2026-06-01 13:43:01，`extract/pyfcstm.py` 签字组件字段兼容性），
此后到归档为止无改动。

## 2. ⚠️ 它不是死代码——动它会影响 CI

**这是本导引最重要的一条。** 以下活测试仍在 import / 读取本目录：

| 引用方 | 引用内容 |
|---|---|
| [../../tests/test_pyfcstm_feedback_migration.py](../../tests/test_pyfcstm_feedback_migration.py) | `from archive.path1_evaluation.extract.pyfcstm import extract_pyfcstm`（3 个 `test_extract_pyfcstm_*` 用它）；另有 `test_locally_available_core_dataset_artifacts_remain_readable` 把 [data/sources_path1.parquet](./data/) / [data/sources_path2.parquet](./data/) 列为候选路径；另有 `test_existing_eval_demo_json_fixtures_are_unchanged` **无条件读** [data/refs/](./data/refs/) 与 [data/preds/](./data/preds/) 下 4 个 JSON（两个 `ref_components.json` + 两个 `pred_perfect.json`），断言 `states >= 3`、`transitions >= 4` |
| [../../tests/helpers/path_branch_smoke.py](../../tests/helpers/path_branch_smoke.py) | `from archive.path1_evaluation.extract.pyfcstm import extract_pyfcstm`。⚠️ 它**不是 pytest 测试**（是个带 `main()` 的 helper，由 CI 的 "Smoke Path 1/Path 2 representative artifacts" 步骤调用），读的 parquet 在 `/tmp/pr13_artifacts/` 下，由 CI 前一步 `git show` 导出，不读本目录的 `data/` |

它们用 `extract/pyfcstm.py` 测 pyfcstm 的**迁移契约**（pyfcstm 升级后 DSL → 5-component IR
的抽取行为是否还稳定）。所以：

- 删除本目录 = 直接弄坏 CI。
- 改 `extract/pyfcstm.py` 的公开行为 = 改的是 pyfcstm 升级门，必须同步跑上述两个测试。
- 删或改 [data/refs/](./data/refs/) 与 [data/preds/](./data/preds/) 下那 4 个 JSON 也会直接红——
  它们是**无条件**依赖，没有存在性守卫。

⚠️ **关于两个 `sources_path*.parquet`：它们在工作树里不存在**
（[data/](./data/) 下只有 `sources/` `refs/` `preds/` 三个子目录）。
但**对应测试并不是 pytest skip**，说法要准确：

```python
present = [p for p in candidates if p.exists()]
assert present, "expected at least one path1/path2/core dataset artifact"
```

它是 **present-filter + `assert present`**：4 个候选路径里前 2 个在本目录（缺失），
后 2 个在 [../../reproduction/data/derived/](../../reproduction/data/derived/)（存在），
所以 `present` 非空、测试通过，而**本目录那两个 parquet 一行都没被读到**。
含义上的区别很重要：这个测试**不保护本目录的任何东西**，别把它算成本目录的覆盖；
反过来，若哪天 `reproduction/data/derived/` 也空了，它会**直接 fail 而不是 skip**。

## 3. 复活前置条件

1. **pyfcstm submodule**：`git submodule update --init --recursive` +
   `venv/bin/pip install -e ./pyfcstm`。当前 pin `901f30e981c29eb8e304b33d61985652d2e85b2e`
   （`v0.6.0-181-g901f30e9`）。`extract/pyfcstm.py` 依赖
   `pyfcstm.dsl.parse_with_grammar_entry` 与 `pyfcstm.model.parse_dsl_node_to_state_machine`。
2. **pandas / parquet**：`aggregate.py`、`report.py`、`review/load.py` 全部走 `pandas`，
   `results/` 与 `review/loaded/` 是 parquet。需要 `pyarrow` 一类的 parquet 引擎。
3. **env 契约与 `agent_loop_method` 完全不同**——这条最容易踩错。
   本目录**不用** `LLM_ENDPOINT` / `LLM_API_KEY` / `LLM_MODEL`，而是 subprocess 调 CLI：

   ```bash
   export CLAUDE_CMD=claude          # annotate/claude.py：claude -p ... --output-format json
   export CLAUDE_MODEL=claude-opus-4-7
   export CODEX_CMD=codex            # annotate/codex.py：codex exec --json --skip-git-repo-check -m <model>
   export CODEX_MODEL=gpt-5.5
   ```

   两个 annotator 都只读 `os.environ`，不直接解析 `.env`。codex 侧的 provider 路由由
   `~/.codex/config.toml` 决定，代码只钉 model 名——所以**换机器就换了 provider**，
   复活时必须显式记录当时实际路由到哪个后端，否则数字不可比。
   ⚠️ 仓库里既没有 `.env` 也没有 `.env.example`；上面这四个键名的记录只存在于
   [README.md](./README.md) 末节和本文件，别让它随目录一起消失。

## 4. 入口与复活方式

原设计入口（见 [README.md](./README.md)「跑演习」一节）：

| 阶段 | 脚本 |
|---|---|
| 3+4：跑 annotation + 渲染中文评审包 | [demo/run_demo.py](./demo/run_demo.py) |
| 5：解析签字包 → parquet → 算 metric | [demo/finalize_after_signoff.py](./demo/finalize_after_signoff.py) |
| 重渲染评审包（不重跑 LLM） | [demo/rerender_packs.py](./demo/rerender_packs.py) ⛔ **会覆写人工签字，跑前必读下一节** |

### ⛔ 跑 `rerender_packs.py` 之前必读：它会静默销毁人工签字

**本节是本导引唯一造成过实际损坏的一条，优先级高于其它所有内容。**

[demo/rerender_packs.py](./demo/rerender_packs.py) 的作用是「不重跑 LLM、只重渲染评审包」，
它**直接覆写** [review/packs/](./review/packs/) 下的 10 份 markdown。
那些文件里含**人工签字**——`- [x] 采纳 Claude` / `- [x] 采纳 gpt-5.5` 形式的勾选。
重渲染只从 [review/raw/](./review/raw/) 的 annotator JSON 重建，**人类的勾选无从恢复**，
于是已勾选被回退成 `- [ ]`，**不提示、不备份、退出码 0**。

2026-08-11 的一次归档审计照本导引跑了它一次，**6 行签字被清空**，靠 `git checkout` 才复原。
（同口径的警告已写进 [demo/rerender_packs.py](./demo/rerender_packs.py) 的文件头注释。）

实测损失面（把 `PACKS_DIR` 改指 `/tmp` 做的无损干跑，逐行 diff）：

| 项 | 数字 |
|---|---|
| 工作树 packs 里的 `- [x]` 行 | **67** |
| 全新渲染后的 `- [x]` 行 | **61** |
| 会被回退的行 | **6** |
| 受影响文件 | 只有 2 份：`abs-fsm-brake-control/pred_buggy/guards.md`、`同目录/transitions.md`（各 3 行：1 行 `采纳 Claude` + 2 行 `采纳 gpt-5.5`） |

为什么只有 6 行而不是 67 行：渲染器对**两个 annotator 完全一致**的行会
自动预勾 `[x] 采纳 Claude`（见 [review/render.py](./review/render.py) `claude_box = "[x]"` 分支），
这部分重渲染能原样重建；**只有人类在「两边不一致 / 单票 / 双方都没提案」的行上做的裁定会丢**。
也就是说：**丢掉的恰好是唯一不可再生的那部分**——需要人判断的那些行。

后果不止于 markdown：[aggregate.py](./aggregate.py) 只计 `user_final_status` 行，
[report.py](./report.py) 对任何未签字行抛 `UnsignedRowsError` 硬拦。所以签字被清空后，
`finalize_after_signoff.py` 要么直接报错，要么（若有人绕过硬拦）算出与
[results/](./results/) 不一致的 P/R/F1。

**跑它之前 / 之后：**

1. 先 `git status --short` 确认工作树干净（否则你分不清哪些改动是它造成的）。
2. 跑完立刻
   `git diff -- project_1_llm_state_machine_modeling/archive/path1_evaluation/review/packs/`
   **逐行看**。
3. 只要看到 `- [x]` 变 `- [ ]`，一律
   `git checkout -- <那些文件>` 回滚，**不要提交**。
4. 真需要重渲染排版时，正确做法是**先把 `PACKS_DIR` 指到 `/tmp` 下的临时目录**，
   对比满意后再决定要不要覆盖，并手工把签字补回去。

### import 与路径：**已经修好了，不要再改**

三个 demo 脚本冻结时把包名和数据根硬编码成 `eval`
（`PROJ = HERE.parent.parent.parent`、`from eval.X import ...`、`EVAL_ROOT = PROJ / "eval"`）。
**本轮归档已经全部改完**，当前工作树的实际写法是：

```python
HERE = Path(__file__).resolve()           # 注意：resolve() 的是文件本身，不是目录
PROJ = HERE.parent.parent.parent.parent   # = project_1_llm_state_machine_modeling
sys.path.insert(0, str(PROJ))
from archive.path1_evaluation.annotate.orchestrate import annotate_pair
EVAL_ROOT = PROJ / "archive" / "path1_evaluation"
```

⛔ **`PROJ` 已经是正确层数，不要再"上推一级"。** `HERE` 是文件路径不是目录路径，
所以四层 `.parent` 恰好落在 `project_1_llm_state_machine_modeling`；再加一层会落到**仓库根**，
`EVAL_ROOT` 随之变成不存在的 `research_ideas/archive/path1_evaluation`，
而 `sys.path` 里也没有了 `archive` 包的父目录——`from archive.path1_evaluation...` 直接
`ModuleNotFoundError`。历史版本的本导引在这里写反了，照它改会把已修好的脚本改坏。

复活时无需改这三个脚本，也**不要**建 `eval` 符号链接（那会让 `eval` 这个名字重新出现在
import 路径里，与 `paper_stm_issue_discover/discover_matrix`——历史上也曾住在 `eval/` 下——混淆）。
唯一仍需注意的是 `EVAL_ROOT` 同时决定 `review/raw/`、`review/packs/`、`results/` 的**写入**位置，
改它等于改产物落点，而且不报错。

冒烟验证（不调 LLM、不写盘）：

```bash
cd <repo root>
PYTHONPATH=project_1_llm_state_machine_modeling venv/bin/python -c "
import archive.path1_evaluation.demo.run_demo as m
print(m.PROJ); print(m.EVAL_ROOT, m.EVAL_ROOT.exists())"
```

实测（2026-08-11）：三个 demo 模块 + `aggregate` / `report` / `extract.*` / `review.*` /
`annotate.*` 共 13 个模块全部 import 通过，`EVAL_ROOT.exists()` 为 `True`。

注意 `README.md` 里那段 `PYTHONPATH=. python eval/demo/run_demo.py` 仍是**冻结时的命令**，
现在照着敲会失败（`eval/` 这个目录已不存在）。正确形式是
`PYTHONPATH=project_1_llm_state_machine_modeling venv/bin/python -m archive.path1_evaluation.demo.run_demo`
——⚠️ 但那会**真的调 LLM**（8 次调用），且需要 §3 的四个环境变量。

### 已有的历史产物

[results/](./results/) 里保留着冻结时演习的完整产出（`detail.parquet` /
`macro_per_case.parquet` / `overall_per_condition.parquet` / `full_annotations.parquet` /
`summary.csv` / `REPORT.md`），[review/packs/](./review/packs/) 保留着**已签字**的中文评审包
（10 份 markdown，含 67 行 `- [x]`），
[review/loaded/reviewed.parquet](./review/loaded/) 保留着解析后的统一表。
**只想看方法学效果、不想重跑 LLM 的话，直接读这些产物即可。**

⛔ 但请注意：`review/packs/` 既是**资产**也是**易损件**——它是本目录里唯一含人工判断、
且唯一无法由代码重建的东西。上面那条 `rerender_packs.py` 警告针对的正是它。

这些数字属于两个 mock case 的演习，**不得作为任何论文结论**（见 [../README.md](../README.md) §0）。

## 5. 离线 gate（[../README.md](../README.md) §3 第 3 步在本目录的落法）

**本目录自己没有测试**（[tests/](./tests/) 目录存在但 git 里 0 个被跟踪文件），
所以「先跑本目录的测试」这条指令在这里**无从执行**。可用的离线 gate 是**项目级**测试树：

```bash
cd <repo root>
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m pytest -q project_1_llm_state_machine_modeling/tests
```

**实测基线（2026-08-11）：`40 passed`，约 16 秒，全程不联网、不调 LLM、不需要 `.env`。**
若看到非 40 或有 failed，说明动了本目录 / [../path1_path2_guides/](../path1_path2_guides/) /
[../agent_loop_method/](../agent_loop_method/) 的公开行为，先查再往下走。

第二条更便宜的 gate（只验 import 与路径解析，1 秒内）：

```bash
cd <repo root>
PYTHONPATH=project_1_llm_state_machine_modeling venv/bin/python -c "
import importlib
for m in ['aggregate','report','extract.pyfcstm','extract.schema','extract.umple',
          'review.load','review.render','annotate.claude','annotate.codex',
          'annotate.orchestrate','demo.run_demo','demo.finalize_after_signoff',
          'demo.rerender_packs']:
    importlib.import_module('archive.path1_evaluation.'+m)
import archive.path1_evaluation.demo.run_demo as d
assert d.EVAL_ROOT.exists(), d.EVAL_ROOT
print('13 modules OK, EVAL_ROOT =', d.EVAL_ROOT)"
```

### 它验了什么 / 没验什么

**这条 gate 的覆盖面很窄，必须知道边界，否则会把「40 passed」误读成本目录健康。**

| | 内容 |
|---|---|
| ✅ **验了** | 40 个测试里只有 **4 个**碰本目录：3 个 `test_extract_pyfcstm_*`（`extract/pyfcstm.py` + 它依赖的 `extract/schema.py`，即 pyfcstm 迁移契约）与 1 个 `test_existing_eval_demo_json_fixtures_are_unchanged`（[data/refs/](./data/refs/) 与 [data/preds/](./data/preds/) 的 4 份 JSON 未被改动） |
| ✅ **验了**（第二条 gate） | 13 个模块 import 通畅、`EVAL_ROOT` 解析正确——即 §4 那套归档后 import 重写没有回归 |
| ❌ **没验** | 18 个 `.py` 里其余 14 个：[aggregate.py](./aggregate.py)、[report.py](./report.py)、[review/load.py](./review/load.py)、[review/render.py](./review/render.py)、[extract/umple.py](./extract/umple.py)、`annotate/*`、`demo/*` 的**行为**全部无测试覆盖（只有 import 级冒烟） |
| ❌ **没验** | 5 阶段流水线端到端是否还跑得通；签字包解析、P/R/F1 计算、`UnsignedRowsError` 硬拦是否仍正确 |
| ❌ **没验** | 任何**与 provider 有关**的东西：两个 CLI annotator 是否可调、`CLAUDE_CMD` / `CODEX_CMD` 是否存在、codex 侧实际路由到哪个后端（见 §3） |
| ❌ **没验** | [results/](./results/) 里的历史数字能否复现（它们依赖当时的 CLI provider，见 §3） |

所以真正复活时，`40 passed` 只够说明「代码没烂、路径没错」；
**「流水线还能出数」必须靠一次真实 5 阶段跑通来证明**，而那一步就要接 provider 了。
⛔ 并且在跑第 3 阶段之前，请先读完 §4 开头那条 `rerender_packs.py` 警告。

## 6. 已知文档腐烂项

冻结时的原件未随归档更新，以下内容读时需自行折算：

1. [README.md](./README.md) 的目录树以 `eval/` 为根；`## 跑演习` 一节的命令
   （`source ../../.env`、`cd project_1_llm_state_machine_modeling`、
   `PYTHONPATH=. python eval/demo/run_demo.py`、`eval/review/packs/...`、`eval/results/summary.csv`）
   **全部失效**——`eval/` 这个目录已不存在。可用形式见 §4 与 §5。
   附带一条：那里的 `source ../../.env` 是**从 `eval/` 出发**算的路径；
   本目录下沉一层后，同一个仓库根 `.env` 要写成 `../../../.env`。
2. [README.md](./README.md) 提到 `demo/aggregate_after_signoff.py`
   （出处是 `demo/run_demo.py` 的模块 docstring，那句 docstring 也仍是旧名），
   实际文件名是 [demo/finalize_after_signoff.py](./demo/finalize_after_signoff.py)。
3. [tests/](./tests/) 目录存在但**是空的**（git 里 0 个被跟踪文件）。本目录自己没有测试；
   对它的唯一自动化保护是 §2 那两个引用方 + §5 的项目级 gate。
4. **Markdown 链接本身不腐烂了**——这一条与历史版本的说法相反，别照旧版再补 `../`：
   - [PROTOCOL.md](./PROTOCOL.md) 的 3 个相对链接**本轮已就地修好**
     （`../sources/` → `../../sources/` 两处、`../discussions/...` → `../../discussions/...` 一处），
     实测已无 `](../sources` / `](../discussions` 形式的 target。
   - [README.md](./README.md) 全文只有 **1 个** Markdown 链接（`./PROTOCOL.md`），同目录、可达。
   - 仍然错的是**正文里的裸路径与命令**（不是链接），即上面第 1、2 条。

## 7. 本轮归档在本目录实际改了什么

以下是**实测**结果：以 `50e6d050`（2026-08-11 01:38:51，归档前最后一个含 `eval/` 的 commit）
的 `project_1_llm_state_machine_modeling/eval/<f>` 为基准，逐文件比对当前
`archive/path1_evaluation/<f>` 的 blob hash，**73 个同名文件里有 5 个内容变了**
（`ARCHIVE_README.md` 本身是新增，不计入）：

| 文件 | 改了什么 | 处数 |
|---|---|---|
| [PROTOCOL.md](./PROTOCOL.md) | 相对链接补一级 `../`：`../sources/` → `../../sources/`（2 处）、`../discussions/...` → `../../discussions/...`（1 处） | 3 |
| [demo/run_demo.py](./demo/run_demo.py) | `PROJ` 多一级 `.parent`（+注释）、`from eval.X` → `from archive.path1_evaluation.X`（2 处）、`EVAL_ROOT` 改指 `archive/path1_evaluation` | 4 |
| [demo/finalize_after_signoff.py](./demo/finalize_after_signoff.py) | 同上（import 3 处） | 5 |
| [demo/rerender_packs.py](./demo/rerender_packs.py) | 同上（import 1 处），**外加文件头 10 行签字覆写危险警告**（见 §4） | 3 + 警告 |
| [extract/pyfcstm.py](./extract/pyfcstm.py) | `extract_pyfcstm` docstring：`method.feedback.parse` → `archive.agent_loop_method.feedback.parse` | 1 |

**未改动**的包括 [README.md](./README.md)（所以它的命令仍是冻结时写法，见 §6）、
[data/](./data/) 全部、[results/](./results/) 全部、[review/](./review/) 全部
（含 `packs/` 的 67 行人工签字——**这些必须保持未改动**）、
`aggregate.py` / `report.py` / `review/load.py` / `review/render.py` /
`extract/schema.py` / `extract/umple.py` / `annotate/*`。

复核命令：

```bash
cd <repo root>/project_1_llm_state_machine_modeling
for f in $(cd archive/path1_evaluation && git ls-files . | grep -v ARCHIVE_README.md); do
  a=$(git rev-parse 50e6d050:project_1_llm_state_machine_modeling/eval/$f 2>/dev/null)
  b=$(git hash-object archive/path1_evaluation/$f)
  [ "$a" != "$b" ] && echo "CHANGED: $f"
done
```

⚠️ 别用 `git diff 50e6d050 -- archive/path1_evaluation/` 来数——目录移动发生在 `50e6d050`
**之后**，那条命令会把 74 个文件**全部报成新增**（`A`），什么也说明不了。
必须像上面那样跨旧路径 `eval/` 比对。
