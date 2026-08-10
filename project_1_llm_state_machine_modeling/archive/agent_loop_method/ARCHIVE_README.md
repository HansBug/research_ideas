# `agent_loop_method/` 复活导引（ARCHIVE_README）

> 本文件是**归档后新增**的复活导引，不覆盖冻结时的四份原件：
> [README.md](./README.md)（功能入口地图与证据边界）、
> [ARCHITECTURE.md](./ARCHITECTURE.md)（LG-M1 架构事实、命名 provenance、模块/测试边界）、
> [STATUS.md](./STATUS.md)（顶部 current overlay + Phase A-J 历史 sprint 记录）、
> [EXAMPLES.md](./EXAMPLES.md)（历史示例）。
>
> 上级入口：[../README.md](../README.md)。
>
> ⚠️ 那四份是**冻结时的原件**。本轮归档已同步修正其中的路径与模块名，但**内容与数字未复核**
> （尤其测试基线数字已过时）。先读本文件 §7「已知文档腐烂项」，再读它们。

## 0. 是什么

NL → pyfcstm / FCSTM 状态机建模的 **16-stage LangGraph agent loop**。默认 stage graph：

```text
SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13
```

默认 repair 主链：

```text
SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local_check_evidence) -> SC-11 -> SD-2 full revalidation
```

（两张图取自 [README.md](./README.md) §1 与 [ARCHITECTURE.md](./ARCHITECTURE.md) §2.1，不在此重画。）

命名前缀含义：`SL-*` = LLM 阶段，`SD-*` = deterministic 检查阶段，`SC-*` = 控制 / 收口阶段。

曾服务的对象：Path-1 hard comparison、Path-2 differentiation、repo-local skill 与 ref-model 生产。

规模（`git ls-files` 实测）：**211 个被跟踪文件**；Python 源码（不含 `__pycache__`）
合计约 **51.3k 行**，其中顶层 `.py` 约 **10.7k 行**（最大单文件
[staged_runtime.py](./staged_runtime.py) 5751 行）。

## 1. 为什么弃用

论文任务从 `NL -> STM` **生成**转向 `<NL, STM_0> -> issue discover`，这条 loop 的问题设定
不再对应论文主线。两条硬证据：

1. **与当前实现零代码耦合。** 当前 discover 实现是
   [../../paper_stm_issue_discover/pipeline/feedback_loop/](../../paper_stm_issue_discover/pipeline/feedback_loop/)，
   其中没有任何 import 指向本目录（`grep -rn "agent_loop_method\|from method\|import method"`
   在该目录下无 import 命中）。反向也一样：本目录不知道 discover 的存在。
   另有一处**反向防护**：
   [../../paper_stm_issue_discover/pipeline/feedback_loop/tests/test_import_boundaries.py](../../paper_stm_issue_discover/pipeline/feedback_loop/tests/test_import_boundaries.py)
   把 `archive.agent_loop_method.loop` 与 `archive.agent_loop_method.run_record`
   列入 `FORBIDDEN_RUNTIME_IMPORT_PREFIXES`，主动禁止当前 discover 运行时加载本目录。
   **也就是说：想让 discover 复用这里的代码，必须先改那道门。**
2. **自 2026-06-08 起休眠。** 最后一次内容变更是 `1a66e7e9`（2026-06-08 17:37:26，
   PR39 / LG-M1-G 收口），此后到归档为止无功能改动。

## 2. 不要在这里找什么（防误认）

| 你想找 | 不在这里，去这里 |
|---|---|
| 当前 discover 实现 | [../../paper_stm_issue_discover/pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/](../../paper_stm_issue_discover/pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/) |
| 当前运行入口 | `python -m paper_stm_feedback_loop.discover --pair-id ...` |
| 当前评测矩阵 / 判定 | [../../paper_stm_issue_discover/discover_matrix/](../../paper_stm_issue_discover/discover_matrix/) |
| 当前语料 | [../../paper_stm_issue_discover/selected_seed_examples/](../../paper_stm_issue_discover/selected_seed_examples/) |
| 当前谓词 / prompt | `paper_stm_feedback_loop/discover/predicates.py`、`prompts.py` |

⚠️ 特别容易混的一点：`paper_stm_issue_discover/pipeline/` 下**也有**一个叫
`agent_loop/` 的目录（包 `paper_stm_repair_loop`）。它与本目录不是同一套东西，
且它自己也已经是当前 discover 的 legacy 层（同样在上面那道 import 门的禁止名单里）。
**目录名叫 `agent_loop` 的有三处，只有 `feedback_loop/` 是活的。**

## 3. 复活前置条件

### 3.1 环境变量（三个必需，全部 fail-loud）

```text
LLM_ENDPOINT  — OpenAI-compatible proxy base URL
LLM_API_KEY   — Bearer token
LLM_MODEL     — 默认调用的模型名
```

缺任何一个立即抛 `KeyError`，**没有静默 fallback**——这是刻意设计：静默默认值会让一次运行
在样本之间悄悄混用 `LLM_MODEL`，直接毁掉实验。约定用法是 shell 里
`set -a; source .env; set +a`，代码只读 `os.environ`，**从不解析 `.env` 文件本身**。

⚠️ **仓库里没有 `.env.example`，连 `.env` 本身也不在**（`.env` 被 gitignore）。
这三个键名的唯一书面记录是 [gpt_client.py](./gpt_client.py) 的模块 docstring 和本文件。
**所以这一节不能删——它是这份格式知识的仅存副本。**

可选变量（实测在源码中出现的全部 `LLM_*` / `AGENT_LOOP_*` / `CODEX_*` 键）：

| 变量 | 作用 |
|---|---|
| `LLM_REQUEST_TIMEOUT_SECONDS` | 请求超时，默认 `600` 秒；设 `0` 或 `none` 关闭 |
| `LLM_STREAM` | 是否走 streaming |
| `LLM_STREAM_INCLUDE_USAGE` | streaming 时是否要 usage |
| `LLM_PROGRESS_LOG` / `AGENT_LOOP_PROGRESS_LOG` | 长跑进度日志落点 |
| `CODEX_BIN` | `codex exec` 实验用的二进制路径 |
| `CODEX_EXEC_DEFAULT_CONFIG` / `CODEX_EXEC_OVERRIDE_CONFIG` / `CODEX_EXEC_EXTRA_CONFIG` | `codex exec` skill 实验的配置注入 |

[gpt_client.py](./gpt_client.py) 是仓库中**唯一**允许实例化 OpenAI-compatible client 的位置。

### 3.2 `PYTHONPATH` 与模块名

调用时**必需** `PYTHONPATH=project_1_llm_state_machine_modeling`。

⚠️ **模块名已随归档改变**：原来是 `method.X`，现在是 `archive.agent_loop_method.X`。
归档时全量重写了内部 import（涉及 90 个文件、约 407 处 import 语句），
[tests/fixtures/lg_m1_a_baseline.json](./tests/fixtures/) 里的
`runtime_identity.environment.runner` / `loop_entrypoint` 等字符串也一并改了。
冒烟验证：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -c "import archive.agent_loop_method.loop as L; print(L.run_agent_loop)"
```

### 3.3 依赖缺口：`tiktoken`

[llm_stages.py](./llm_stages.py) 在 `prompt_token_estimator == "tiktoken_optional"` 时
懒加载 `tiktoken`，但 **`tiktoken` 不在 [../../../requirements.txt](../../../requirements.txt) 里**。

**失败模式是静默降级，不是报错**：`except Exception: pass` 之后回落到 chars/4 的粗估
（`ESTIMATED_CHARS_PER_TOKEN = 4.0`）。也就是说，你以为在用 tokenizer 精确估 token
做 budget gating，实际上在用一个 4 倍粗估——而 budget gating 会决定是否截断 prompt。
复活并需要精确估计时，先 `pip install tiktoken`，并**显式验证** estimator 真的走到了
tiktoken 分支。

### 3.4 pyfcstm submodule

```bash
git submodule update --init --recursive
venv/bin/pip install -e ./pyfcstm
```

当前 pin：`901f30e981c29eb8e304b33d61985652d2e85b2e`（`v0.6.0-181-g901f30e9`）。

实测用到的 pyfcstm API 符号（跨 6 个模块）：

| 模块 | 符号 |
|---|---|
| `pyfcstm.dsl` | `parse_with_grammar_entry` |
| `pyfcstm.dsl.error` | `GrammarParseError` |
| `pyfcstm.model` | `parse_dsl_node_to_state_machine` |
| `pyfcstm.utils.validate` | `ModelValidationError` |
| `pyfcstm.diagnostics` | `inspect_model` |
| `pyfcstm.diagnostics.codes` | `CODE_REGISTRY` |
| `pyfcstm.simulate` | `SimulationRuntime`、`SimulationRuntimeDfsError` |

⚠️ `CODE_REGISTRY` 是最危险的一个：它是诊断码注册表，**上游若重编号或改分类，
本目录的 gate 语义会静默变化**（代码不报错，只是判定结果变了）。升级 pyfcstm 后
必须重跑 §5 的离线 gate，并逐条比对诊断码分类，而不是只看测试是否绿。

## 4. 入口：没有 CLI

**本目录不提供 CLI。**「跑一次 loop」的语义是一次 Python 调用：

```python
from archive.agent_loop_method.loop import run_agent_loop, LoopConfig
record = run_agent_loop(nl, LoopConfig())
```

`LoopConfig()` 默认解析为 `experiment_default/full_staged_v1`，走 LangGraph full staged path，
用真实 provider（由进程环境变量提供），并写出完整 `AgentLoopRunRecord`。

最接近 turnkey 的入口是 real run matrix：

```bash
set -a; source .env; set +a
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m archive.agent_loop_method.experiments.real_run_matrix
```

其他带 `__main__` 的模块：
[experiments/checkpoint_resume.py](./experiments/checkpoint_resume.py)、
[experiments/representative_cases.py](./experiments/representative_cases.py)、
[experiments/codex_exec_skill_runs.py](./experiments/codex_exec_skill_runs.py)、
[handoff_smoke/runner.py](./handoff_smoke/runner.py)、
[agent_loop_skill/health_check.py](./agent_loop_skill/health_check.py)，
以及四个纯 compatibility shim（`pr_e1_real_runs.py` / `pr_lg_f1_resume_experiment.py` /
`pr_d_representative.py` / `pr2a_loop.py`——新代码不要用这四个）。

不想跑整条 loop、只想复用确定性工具或 prompt 的话，走 facade：
[stages/api.py](./stages/api.py)、[stages/sc_control.py](./stages/sc_control.py)、
[stages/sl_prompt_api.py](./stages/sl_prompt_api.py)。这三个**不读 `.env`、不调 provider**。

## 5. 验证方式（离线，无需 provider）

测试树**完全离线**：108 处 `monkeypatch`，**零** network marker
（唯一出现的 pytest marker 是一个 `@pytest.mark.parametrize`）。gate 命令：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m pytest -q project_1_llm_state_machine_modeling/archive/agent_loop_method/tests
```

**归档后实测基线：`2 failed, 414 passed, 6 warnings`（416 collected）。**
（2026-08-11 02:36 本地实测；与搬迁前基线一致。）

那 2 个失败是**搬迁前就存在的**，与归档无关，且**在干净 clone 上必然失败**：

| 失败测试 | 原因 |
|---|---|
| `tests/crosscutting/test_lg_m1_inventory_characterization.py::test_lg_m1_a_graph_contract_and_runtime_identity_are_stable_without_provider` | 断言 `runs/2026-06-08-052552-pr39-.../*.agent_loop.json.gz` 存在 |
| `tests/langgraph/test_instrumentation.py::test_lg_m1_d2_historical_evidence_read_only_drift_gate` | 同一份 retained evidence 文件 |

原因：`runs/` 被 [../../../.gitignore](../../../.gitignore)（`/runs/`）整目录排除，
那两份 PR39 retained evidence **从来没进过仓库**，两个测试也**没有 skip 守卫**。
所以「复活时看到 2 failed」是**预期状态**，不是你弄坏了什么。若要让它们通过，
需要先把对应 run record 恢复到 `runs/` 下。

⚠️ 顺带一条：CI（[../../../.github/workflows/project1-pyfcstm-feedback.yml](../../../.github/workflows/project1-pyfcstm-feedback.yml)）
的 "Run pyfcstm feedback migration smoke tests" 步骤会跑这整棵测试树，因此**该步骤在
CI 上也会因这 2 个测试而红**。这不是归档引入的（改路径前跑的是同一棵树），
但它意味着**不能把「CI 绿」当作本目录健康的判据**。

## 6. ⚠️ 复活地雷（最重要的一节）

### 6.1 `handoff_smoke` 依赖 git 历史，而不是工作树

[handoff_smoke/configs/path1_representative.json](./handoff_smoke/configs/) 与
`path2_representative.json` 里的 `source_snapshot.parquet_path` /
`fcstm_path` / `ref_components_path` 指向的文件**在工作树里根本不存在**
（它们是 `project_1_llm_state_machine_modeling/eval/data/...` 与
`project_1_llm_state_machine_modeling/paper_v1/selection/...` 这类旧路径，
`eval/` 与 `paper_v1/` 都已随本轮归档消失）。

[handoff_smoke/runner.py](./handoff_smoke/runner.py) 靠 `_git_show` 从 **pin 死的 commit**
里取内容：

```python
def _git_show(ref: str, repo_path: str, *, cwd=None) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{repo_path}"], cwd=cwd)
```

| config | pin 的 commit |
|---|---|
| `path1_representative.json` | `b4ad12205bccf686a61671d1bdc7c28b1a22bab3` |
| `path2_representative.json` | `bdb25d93408f0a86f8dde8238e67c1f2bfdbbb59` |

**推论：浅克隆（`--depth`）、history rewrite、`filter-branch` / `filter-repo`
会直接杀死 handoff smoke，而且报错是 `git show` 的 "unknown revision"，
看起来完全不像"数据缺失"。** 迁移仓库或做历史清理前，先把这两个 commit 的
相关 blob 导出成真实文件，或至少确认 fetch 了这两个 ref
（CI 里就是显式 `git fetch origin <ref>:refs/remotes/...` + `git cat-file -e` 做可达性检查的）。

⚠️ 同一批 pin 也出现在 CI 的 "Export Path 1/Path 2 representative artifacts" 步骤里，
那里的 `git show ${PATH1_REF}:project_1_llm_state_machine_modeling/eval/data/...`
用的**是旧路径且必须保持旧路径**——它读的是历史 commit 的内容，不是当前工作树。
**不要"顺手"把那些路径改成 `archive/path1_evaluation/...`，那会立刻让 CI 取不到东西。**

### 6.2 `agent_loop_skill/` 的 20 个符号链接

[agent_loop_skill/](./agent_loop_skill/) 下有 **20 个符号链接**：
`SKILL.md` 与 `CLAUDE.md` 指向 `AGENT_LOOP_SKILL.md`，另外 18 个在
`agent_loop_skill/stages/` 下指向 [stages/docs/](./stages/docs/) 的 per-stage 规范。

[agent_loop_skill/health_check.py](./agent_loop_skill/health_check.py) 会断言它们
**是 symlink 且解析到预期目标**（`_check_entry_symlinks` / `_check_stage_symlinks`：
`if not link.is_symlink(): failures.append(...)`、
`elif link.resolve() != target.resolve(): failures.append(...)`）。

**推论：用会 dereference symlink 的方式打包（`tar -h`、`cp -L`、`rsync -L`、
某些 zip / 网盘同步、Docker `COPY` 的部分行为）会把它们变成 20 份重复正文，
health check 立刻失败，而内容看起来"完全正常"。** 归档/搬运本目录时用
`tar` 默认行为或 `git archive`，别加 dereference。

### 6.3 `tests/fixtures/lg_m1_a_baseline.json` 是表征快照，改测试就会打破它

它记录的是**路径清单快照 + 硬编码 collection delta**：`stage_api_scan.modules`、
`experiment_cli_import_baseline.modules`、`facade_reexport_scan.reexporter_paths_checked`
是模块路径列表；`collection` 则记录 `count = 382`（LG-M1-A 时刻）加上一串
具名 delta（`lg_m1_c1_experiments_entrypoints: 5`、`lg_m1_d1_langgraph_foundation: 5`、
`lg_m1_d2_langgraph_instrumentation: 5`、`lg_m1_d3_langgraph_nodes_subgraphs_core: 7`、
`lg_m1_g_final_integration_stabilization: 4`），最终 `current_expected_count_after_c1_d1_b_d2_c2_d3_and_g = 416`。
实测当前 `pytest --collect-only` 恰为 **416**。

**推论：增删任何一个测试函数都会让
`test_lg_m1_a_pytest_collection_baseline_plus_registered_c1_d1_and_b_deltas_is_current`
失败。** 这是有意的漂移门，不是 bug。复活并要加测试时，**必须同时在 fixture 里
登记一条新的具名 delta**，而不是去改 `count`——改 `count` 等于把历史基线抹掉。
同理，重命名模块也必须同步 fixture 里的路径清单（本轮归档就是这样处理的）。

### 6.4 顶层调用别写成双前缀

[tests/langgraph/test_nodes_subgraphs_core.py](./tests/langgraph/) 里的
`METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "archive" / "agent_loop_method"`
这类常量是相对**仓库根**解析的；而 `PYTHONPATH` 又是
`project_1_llm_state_machine_modeling`。搬迁期间实际发生过一次
`.../project_1_llm_state_machine_modeling/project_1_llm_state_machine_modeling/archive/...`
的双前缀 `FileNotFoundError`。改路径常量时先确认它的基准是仓库根还是 project 根。

## 7. 已知文档腐烂项

本轮归档已把四份原件里的**路径与模块名**同步改过了（`method/` → `archive/agent_loop_method/`、
`method.X` → `archive.agent_loop_method.X`），所以它们的入口地图、gate 命令、目录树
路径都是可用的。**仍然失准的是下面这些与内容/数字有关的项：**

1. [README.md](./README.md) §4 的目录树声称 `eval/` 是 "component extraction/evaluation
   helpers"，但 [eval/](./eval/) 实际**只有一个空的 `__init__.py`**，没有任何 helper。
2. **测试基线数字全部过时。** [README.md](./README.md) 引言、
   [ARCHITECTURE.md](./ARCHITECTURE.md) §1 表格、[STATUS.md](./STATUS.md) §1
   都称"最终验证基线为 `432 passed, 6 warnings`"（并把 `412 passed` 记为 LG-M1-F 历史值），
   与实测的 416 collected / `2 failed, 414 passed` 不符。那些是 PR39 时刻带着
   `runs/` retained evidence 跑出来的数，**在干净 clone 上复现不出来**；
   以本文件 §5 的实测为准。
3. [stages/docs/](./stages/docs/) 实有 **18** 份 per-stage 规范，
   [stages/fixtures/](./stages/fixtures/) 实有 **22** 份 I/O 契约
   （18 个正例 + 4 个负例 `NEG-ADVISORY` / `NEG-BUDGET-EXHAUSTED` / `NEG-ERROR` / `NEG-SKIPPED`）。
   若别处看到 20 / 21 之类的数字，以此处实测为准。
   （注意 `stages/docs/` 含 `SD-10-repair-review.md` 与 `SL-10B-delta-review.md`，
   它们不在 §0 那条 16-stage 主链上——主链之外还有 delta review 与 repair review 分支。）

## 8. 核心设计资产（即使不复活也值得读）

1. **16-stage graph 与 repair chain** —— 见 §0 的两张图，出处
   [README.md](./README.md) §1 / [ARCHITECTURE.md](./ARCHITECTURE.md) §2.1。
   把「LLM 阶段 / 确定性检查阶段 / 控制阶段」三类职责分开命名（`SL` / `SD` / `SC`）
   这一点，当前 discover 的 LangGraph 节点划分仍在沿用同一思路。
2. **per-stage 规范 + I/O 契约 fixture** —— [stages/docs/](./stages/docs/) 18 份 +
   [stages/fixtures/](./stages/fixtures/) 22 份。**4 个负例 fixture 是最值得抄的部分**：
   `NEG-BUDGET-EXHAUSTED` / `NEG-SKIPPED` / `NEG-ADVISORY` / `NEG-ERROR` 把"配额耗尽"、
   "被跳过"、"只给建议"、"真错了"当成**四种不同的一等状态**写进契约，而不是统统抛异常。
   这与 [../../../CLAUDE.md](../../../CLAUDE.md) §10「除两类情况外一律降级」是同一条纪律的早期形态。
3. **四条证据边界纪律** —— [README.md](./README.md) §1 结尾：
   (a) 默认入口不回退 fake / mock / replay provider，缺配置或 retry 耗尽时写出
   `AgentLoopRunRecord` 并以 `provider_error` / `invalid` 退出；
   (b) run record 必须记 resolved config、condition hash、environment、脱敏 provider/model、
   stage/iteration/repair/scenario/LLM trace、eligibility、redaction report、final artifacts；
   (c) 非默认 / weak oracle / provider error / schema invalid / write failure **不得进入主结果**；
   (d) 消融必须显式声明非默认 `condition_id` 与 `changed_factors`，不得污染 `LoopConfig()` 默认路径。
   这四条后来演化成了仓库级的 run record 与 eligibility 规范。
4. **`scenariogen_validate.py` 的 M1-M6 mutation 自校验** ——
   [scenariogen_validate.py](./scenariogen_validate.py)：对模型施加 6 类典型 LLM bug 突变
   （如 `M1` guard 阈值 off-by-one、`M2` 迁移目标改成另一个已声明状态、
   `M6` effect 里的赋值常量 +100），然后看生成的 scenario 集能不能**检出**它们；
   某一类突变**没有任何 scenario 能检出**就记为覆盖缺口并反馈给 scenariogen 补 probe。
   思路的价值在于：它用「能不能发现人为注入的缺陷」反向度量 scenario 的充分性，
   而不是用 scenario 数量或覆盖率的表面统计。
5. **Phase G 的结论** —— [STATUS.md](./STATUS.md)：单靠 sim 跑空 cycle **只能**验证
   "不死锁 / 状态可达"；要验证"模型行为是否符合 NL 需求"，**必须构造
   `NL 需求 -> expected behavior scenario -> sim 执行验证` 的 oracle 链**。
   这条负面结论直接决定了后续 `SD-6` 与 NFRR scenario provenance 的学术边界，
   对研究内容三尤其有参考价值。

## 9. 本次归档同步改了什么

以下是**实测 `git diff` 得到的**改动范围（截至 2026-08-11 02:37）。搬迁由
`c13033d2`（`refactor(paper1): 实验资产归入论文目录，旧路线整体归档`）完成目录移动，
配套的引用修复在工作树中随后完成。

| 类别 | 改动 |
|---|---|
| 目录移动 | `project_1_llm_state_machine_modeling/method/` → `archive/agent_loop_method/`（`c13033d2`，纯 rename，0 行内容变更） |
| 归档区包声明 | 新增 [../\_\_init\_\_.py](../__init__.py)（5 行 docstring，写明"已停用但完整保留、不参与当前论文结论"） |
| 内部 import 全量重写 | `method.*` → `archive.agent_loop_method.*`。改动前实测有 **407 处** `method.` import 语句散落在 **90 个文件**；改动后本目录下 **100 个 `.py` + 31 个非 `.py`** 文件被改，新增行中含 `archive.agent_loop_method` 的共 **767 行**。非 `.py` 那 31 个是四份原件（`README.md` / `ARCHITECTURE.md` / `STATUS.md` / `EXAMPLES.md`）、`agent_loop_skill/` 的 6 份文档、`handoff_smoke/` 的 2 份文档、[stages/docs/](./stages/docs/) 的 18 份 per-stage 规范，以及 [tests/fixtures/lg_m1_a_baseline.json](./tests/fixtures/)（`runtime_identity.environment.runner` / `loop_entrypoint`、`run_config.runtime_implementation`、`collection.command` / `collection.scope` 等字符串） |
| skill 文档与 health check | [agent_loop_skill/](./agent_loop_skill/) 下 `AGENT_LOOP_SKILL.md`、`health_check.py`、`test_health.py`、`codex_exec_experiment.py`、`codex_exec_experiment_guide.md`、`e2e_ref_model_guide.md`、`prompts.md`、`tools.md`、`stages/README.md` 同步改模块名。⚠️ `health_check.py` 会断言 skill 文档里出现 `archive.agent_loop_method.stages.api`，**所以文档与代码必须同批改**——搬迁中途只改了代码没改文档时，`tests/agent_loop_skill/test_stage_api_health.py` 的两个测试立刻失败 |
| CI workflow | [../../../.github/workflows/project1-pyfcstm-feedback.yml](../../../.github/workflows/project1-pyfcstm-feedback.yml) 的 "Run pyfcstm feedback migration smoke tests" 步骤：`method/tests` → `archive/agent_loop_method/tests`。⚠️ 同文件里 "Export Path 1/Path 2 representative artifacts" 步骤的 `git show ${PATH*_REF}:.../eval/data/...` 与 `.../paper_v1/...` **保持旧路径未动**——那是历史 commit 内容，改了就取不到（见 §6.1） |
| 项目级 tests 的 import | [../../tests/test_pyfcstm_feedback_migration.py](../../tests/test_pyfcstm_feedback_migration.py)、[../../tests/helpers/path_branch_smoke.py](../../tests/helpers/path_branch_smoke.py) 改为 `from archive.path1_evaluation.extract.pyfcstm import ...` / `from archive.path1_path2_guides.selection.ref_stms.verify_pyfcstm_static import ...`（这两处属 [../path1_evaluation/](../path1_evaluation/) 与 [../path1_path2_guides/](../path1_path2_guides/) 的引用，见各自导引） |
| import 边界门的禁止名单 | [../../paper_stm_issue_discover/pipeline/feedback_loop/tests/test_import_boundaries.py](../../paper_stm_issue_discover/pipeline/feedback_loop/tests/test_import_boundaries.py) 的 `FORBIDDEN_RUNTIME_IMPORT_PREFIXES`：`method.loop` / `method.run_record` → `archive.agent_loop_method.loop` / `archive.agent_loop_method.run_record`（两处：模块顶层常量 + 子进程 sentinel 内联副本，必须一起改，漏一处门就形同虚设） |
| `.gitignore` | `c13033d2` 中有 20 行路径前缀随目录迁移调整 |

**只改路径不改论述**：本目录原有的 [README.md](./README.md) /
[ARCHITECTURE.md](./ARCHITECTURE.md) / [STATUS.md](./STATUS.md) /
[EXAMPLES.md](./EXAMPLES.md) 四份正文只做了机械的路径与模块名替换，
论述、结论、历史 provenance 与**测试基线数字均按冻结原样保留**。
因此它们的数字不代表当前状态——过时项集中登记在本文件 §7，不就地改写。
