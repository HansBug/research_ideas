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

**这是本导引最重要的一条。** 以下活测试仍在 import 本目录：

| 引用方 | 引用内容 |
|---|---|
| [../../tests/test_pyfcstm_feedback_migration.py](../../tests/test_pyfcstm_feedback_migration.py) | `from archive.path1_evaluation.extract.pyfcstm import extract_pyfcstm`；另外还直接读 [data/sources_path1.parquet](./data/) / [data/sources_path2.parquet](./data/) 两个路径 |
| [../../tests/helpers/path_branch_smoke.py](../../tests/helpers/path_branch_smoke.py) | `from archive.path1_evaluation.extract.pyfcstm import extract_pyfcstm` |

它们用 `extract/pyfcstm.py` 测 pyfcstm 的**迁移契约**（pyfcstm 升级后 DSL → 5-component IR
的抽取行为是否还稳定）。所以：

- 删除本目录 = 直接弄坏 CI。
- 改 `extract/pyfcstm.py` 的公开行为 = 改的是 pyfcstm 升级门，必须同步跑上述两个测试。
- ⚠️ 上表提到的 `data/sources_path1.parquet` / `data/sources_path2.parquet` **在工作树里不存在**
  （[data/](./data/) 下只有 `sources/` `refs/` `preds/` 三个子目录）；对应测试是按「文件缺失就跳过」
  的方式写的，不要以为它们应该在那里。

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
| 重渲染评审包（不重跑 LLM） | [demo/rerender_packs.py](./demo/rerender_packs.py) |

### ⚠️ 复活地雷：三个 demo 脚本目前是坏的

它们把包名和数据根**硬编码成 `eval`**：

```python
PROJ = HERE.parent.parent.parent      # 冻结时 = project_1_llm_state_machine_modeling
sys.path.insert(0, str(PROJ))
from eval.annotate.orchestrate import annotate_pair
EVAL_ROOT = PROJ / "eval"
```

归档后 `HERE.parent.parent.parent` 变成了 `.../project_1_llm_state_machine_modeling/archive`，
而 `eval` 这个包已经不存在。三个脚本（`run_demo.py` 3 处、`finalize_after_signoff.py` 3 处、
`rerender_packs.py` 1 处，共 **7 处 `from eval.X import ...`**，外加 3 处
`EVAL_ROOT = PROJ / "eval"`）都会 `ModuleNotFoundError` 或指向不存在的目录。
⚠️ 注意本轮归档的 import 重写**没有覆盖这三个脚本**——它只改了 `method.` 前缀，
`eval.` 前缀原样留着。

复活时二选一：

- **改脚本**：把 `PROJ` 上推一级、`from eval.X` 改成 `from archive.path1_evaluation.X`、
  `EVAL_ROOT` 改成本目录。改完必须重跑一次完整 5 阶段，因为 `EVAL_ROOT` 同时决定
  `review/raw/`、`review/packs/`、`results/` 的写入位置，改错会把产物写到别处而不报错。
- **临时 shim**：在 `project_1_llm_state_machine_modeling/` 下建一个指向本目录的
  `eval` 符号链接。省事，但会让 `eval` 这个名字重新出现在 import 路径里，容易和
  `paper_stm_issue_discover/discover_matrix`（历史上也曾住在 `eval/` 下）混淆，不推荐长期用。

注意 `README.md` 里那段 `PYTHONPATH=. python eval/demo/run_demo.py` 是**冻结时的命令**，
现在照着敲会直接失败。

### 已有的历史产物

[results/](./results/) 里保留着冻结时演习的完整产出（`detail.parquet` /
`macro_per_case.parquet` / `overall_per_condition.parquet` / `full_annotations.parquet` /
`summary.csv` / `REPORT.md`），[review/packs/](./review/packs/) 保留着已签字的中文评审包，
[review/loaded/reviewed.parquet](./review/loaded/) 保留着解析后的统一表。
**只想看方法学效果、不想重跑 LLM 的话，直接读这些产物即可。**
但这些数字属于两个 mock case 的演习，**不得作为任何论文结论**（见 [../README.md](../README.md) §0）。

## 5. 已知文档腐烂项

冻结时的原件未随归档更新，以下内容读时需自行折算：

1. [README.md](./README.md) 的目录树以 `eval/` 为根，`## 跑演习` 一节的命令
   （`source ../../.env`、`PYTHONPATH=. python eval/demo/run_demo.py`）全部失效。
2. [README.md](./README.md) 提到 `demo/aggregate_after_signoff.py`
   （在 `demo/run_demo.py` 的模块 docstring 里），实际文件名是
   [demo/finalize_after_signoff.py](./demo/finalize_after_signoff.py)。
3. [tests/](./tests/) 目录存在但**是空的**（git 里没有任何被跟踪的文件）。本目录自己
   没有测试；对它的唯一自动化保护来自 §2 那两个项目级测试。
4. 原件里指向 `../method/`、`../paper_v1/`、`../../CLAUDE.md` 一类的相对链接，
   因为目录下沉了一层而全部偏移一级。
5. 本轮归档只改动了本目录的一处内容：[extract/pyfcstm.py](./extract/pyfcstm.py) 里
   `extract_pyfcstm` 的 docstring，把 "pre-gate with `method.feedback.parse`"
   改为 `archive.agent_loop_method.feedback.parse`。其余文件（含
   [README.md](./README.md) 与 [PROTOCOL.md](./PROTOCOL.md)）**未改动**，
   所以它们里的路径与命令仍是冻结时的写法。
