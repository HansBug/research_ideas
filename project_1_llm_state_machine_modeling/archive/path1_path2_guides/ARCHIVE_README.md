# `path1_path2_guides/` 复活导引（ARCHIVE_README）

> 本文件是**归档后新增**的复活导引，不覆盖冻结时的原件。
> 原始文档：[README.md](./README.md)（原 `paper_v1/README.md`，"第一篇论文工作区"）、
> [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md)、
> [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md)。
>
> 上级入口：[../README.md](../README.md)。

## 0. 是什么

原 `project_1_llm_state_machine_modeling/paper_v1/`，共 **7 个被跟踪文件**
（3 份 Markdown + 3 个 `__init__.py` + 1 个 Python 脚本）：

| 文件 | 内容 |
|---|---|
| [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md) | Path-1「**硬刚路线**」接管指引，11 节 |
| [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md) | Path-2「**差异化路线**」接管指引 |
| [README.md](./README.md) | 旧第一篇论文工作区总览 + 2026-06-12 转舵说明 |
| [selection/ref_stms/verify_pyfcstm_static.py](./selection/ref_stms/verify_pyfcstm_static.py) | 基于 `inspect_model` 的 pyfcstm 静态设计健康检查器 |

两条路线的分歧点是**评测有没有 reference**：

- **Path-1（硬刚）**：与 baseline 论文同 protocol（component-level manual eval），
  在自建 `sources/` T0+🟢 子集上，相对 `structure_event_driven` 的最强 strategy（Hybrid）
  跑出更高的 5-component manual-eval F1。**需要 ref STM。**
- **Path-2（差异化）**：主张控制系统真实语料上不存在规模化的 canonical ref STM
  （同一需求可对应多个等价 STM），因此改打 **reference-free 4-intrinsic 评测** +
  可选的小规模 audit-trail 人工校准。**不需要 ref STM。**

冻结时间：`4d46b7ea`（2026-06-12 23:44:52，"落地主线与范围冻结文档"）；
同日 `f8bc3408`（23:58:43）移除旧路径并收敛主线入口。

## 1. 为什么弃用

**2026-06-12 导师讨论后论文整体转舵，两条路线的 framing 均作废。**
第一篇论文从早期 `NL -> STM` 生成 / hard comparison 口径，转向
`<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动路线，最终落到当前的 STM issue discover。
转舵依据见 [../../talks/](../../talks/)（`2026-06-12-导师-两篇论文转向与模型修正定调`）。

这份归档是**论文转舵前**的路线资料。它的 paper 主卖点、contribution 列表、baseline 对照口径
都建立在"我们生成的 STM 比 baseline 生成的更好"这个已被放弃的命题上，
**不得直接搬进当前论文**。

## 2. ⚠️ 两份 GUIDE 里的实验命令本来就是死的

[PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md) §5 与
[PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md) §5 分别叫
"实验脚本 `run_path1.py` / `run_path2.py`"，并给出：

```bash
python -m archive.agent_loop_method.run_path1 ...   # 原文写作 python -m method.run_path1
python -m archive.agent_loop_method.run_path2 ...   # 原文写作 python -m method.run_path2
```

**这两个脚本从来没有存在过。**
`git log --all -- project_1_llm_state_machine_modeling/method/run_path1.py`
与 `run_path2.py` 均为空——它们在仓库全部历史中都不存在。这两节写的是
**计划中的接口**，不是已实装的入口。

（本轮归档把这两条命令里的 `method.` 前缀改成了 `archive.agent_loop_method.`，
所以现在看起来更像真命令了。**它们依然是死的。** 不要照着敲，也不要因为敲不通
就去 `archive/agent_loop_method/` 里找——那里没有。）

要真跑 loop，唯一入口见 [../agent_loop_method/ARCHIVE_README.md](../agent_loop_method/ARCHIVE_README.md) §4：
`archive.agent_loop_method.loop.run_agent_loop(nl, LoopConfig())`，或
`python -m archive.agent_loop_method.experiments.real_run_matrix`。

## 3. ⚠️ `verify_pyfcstm_static.py` 仍被活测试 import

| 引用方 | 引用内容 |
|---|---|
| [../../tests/test_pyfcstm_feedback_migration.py](../../tests/test_pyfcstm_feedback_migration.py) | `from archive.path1_path2_guides.selection.ref_stms.verify_pyfcstm_static import _EXTERNAL_RE, _severity, analyze` |
| [../../tests/helpers/path_branch_smoke.py](../../tests/helpers/path_branch_smoke.py) | `from archive.path1_path2_guides.selection.ref_stms.verify_pyfcstm_static import analyze` |

注意第一处连 `_EXTERNAL_RE` 和 `_severity` 两个**私有符号**都 import 了，
所以内部实现也不能随便改名。

**推论：这个文件不是死代码。** 删除或改动它会直接弄坏 CI 的
"Run pyfcstm feedback migration smoke tests" 与
"Smoke Path 1/Path 2 representative artifacts" 两个步骤
（见 [../../../.github/workflows/project1-pyfcstm-feedback.yml](../../../.github/workflows/project1-pyfcstm-feedback.yml)）。

### 它自己是个可独立使用的 CLI

```bash
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python project_1_llm_state_machine_modeling/archive/path1_path2_guides/selection/ref_stms/verify_pyfcstm_static.py <path.fcstm> [--strict]
```

退出码：`0` 无 error / `1` 有 error（`--strict` 时任何 warning 也算）/ `2` 用法错误。

依赖 pyfcstm 的 `dsl.parse_with_grammar_entry`、`dsl.error.GrammarParseError`、
`model.parse_dsl_node_to_state_machine`、`utils.validate.ModelDiagnostic` /
`ModelValidationError`、`diagnostics.inspect_model`。

**它是本目录最值得留的资产**，因为它把「上游报告什么」和「本项目认为什么阻塞」
分成了两层，并且给未知诊断码留了一个 fail-closed 的阀门：

- `DOWNSTREAM_STRICT_ERROR_CODES` —— pyfcstm 报 warning 但本项目当 error 的三个码
  （`W_UNWRITTEN_READ_VAR` / `W_FORCED_NEVER_EXPANDS` / `W_GUARD_CONST_FALSE`）。
- `DOWNSTREAM_ADVISORY_WARNING_CODES` —— 明确判定为 advisory 的白名单。
- **两张表都没有的新 `W_*` 码，一律先升级为 error**，直到项目显式归类。
  这正是 [../../../CLAUDE.md](../../../CLAUDE.md) §7「未知 diagnostic code 不能静默放过」
  的一份可执行实现，pyfcstm 升级时的审计阀门就在这里。

## 4. 其它值得保留的内容

即使路线作废，两份 GUIDE 里下面这些**仍然有效**，做 related work 或写第二篇时可直接取用：

1. **6-baseline 方法学全景表** ——
   [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md) §1.1：
   `structure_event_driven` / `llms_emp` / IEC 61499 / Automated Statechart (Automotive) /
   Llama3 Umple / `ttool-ai` 六家，逐家标出任务与输出形式、LLM、方法核心、
   prompt-engineering 强度、**simulation 反馈强度**、**formal verification 反馈强度**。
   这张表是判断"哪家真的做了 in-loop feedback"的现成依据。
2. **"我们 first to do in-loop feedback 不成立"这个诚实结论** ——
   同文件 §1.2 开头就点明 6 家里有 3 家（`llms_emp` / IEC 61499 / `ttool-ai`）
   已有 in-loop feedback，然后才逐条论证真正的差异在哪。**这个 framing 纪律
   （先承认对手做过什么，再定位增量）比它的具体结论更值得继承。**
3. **sprint 范围声明表** ——
   [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md) §1.2：
   逐个 baseline 写"为什么这一轮不复现"和"方向定后怎么补"。这是向 reviewer
   解释复现范围的现成模板。
4. **一次有据可查的 dataset 排除裁定** —— 同文件 §1 的 v4 修订说明：
   原计划锁定 `structure_event_driven` 的 8 个 case，实查 ground truth 后发现
   **8/8 都含 history pseudo-state（`.H`）**，而 pyfcstm 形式上不支持，
   按"排除含 parallel/history 的 NL"规则会把整个 dataset 排空，于是换语料。
   这与当前论文的 `00x8` 系列永久排除（见
   [../../paper_stm_issue_discover/](../../paper_stm_issue_discover/) 与
   [../../../CLAUDE.md](../../../CLAUDE.md)）是**同一类先验裁定**：
   判据只读输入与建模对象边界，与运行结果无关。想论证"这类排除不是剔除不利样本"时，
   这里有一个更早的先例。
5. **评测组件从 7 类收到 5 类的理由** —— 剔除 `parallel_regions` / `history_states`，
   因为 pyfcstm 不主张覆盖。这条与 project_1 的建模对象边界一致，至今有效。

## 5. 复活方式

这三份 Markdown **没有可执行依赖**，读即可用；`verify_pyfcstm_static.py` 的用法见 §3。

若要真正重启这两条路线，除本目录外还需要另外两块：

- **生成侧**：[../agent_loop_method/](../agent_loop_method/)，
  先读 [其 ARCHIVE_README.md](../agent_loop_method/ARCHIVE_README.md)（尤其 §6 复活地雷）。
- **评测侧**：[../path1_evaluation/](../path1_evaluation/)，
  先读 [其 ARCHIVE_README.md](../path1_evaluation/ARCHIVE_README.md)（三个 demo 脚本目前是坏的）。

⚠️ 两份 GUIDE 的 §2「接管前自检」写的是 `dev/path1-hard-comparison` /
`dev/path2-differentiation` 两个分支上的 fork 状态，那是 2026-05 sprint 的现场，
现在照着自检必然对不上。**只把它当"复活需要凑齐哪些前置条件"的清单读，
不要当"当前状态应该长什么样"的断言读。**

## 6. 已知文档腐烂项

冻结时的原件未随归档更新，读时需自行折算：

1. **相对链接全部偏移一级。** 目录从 `paper_v1/` 下沉到 `archive/path1_path2_guides/`，
   原件里 `../sources/`、`../baselines/`、`../reproduction/`、`../discussions/`、
   `../talks/`、`../../CLAUDE.md`、`../../project_ex1_llm_judge_for_stm/`
   这类链接现在都少了一级 `../`。正确写法应是 `../../sources/`、`../../../CLAUDE.md` 等。
2. [README.md](./README.md) 第 5 行指向 `../paper_stm_repair/README.md` ——
   该目录已在 `35eba126` 更名为 `paper_stm_issue_discover`，正确路径是
   [../../paper_stm_issue_discover/README.md](../../paper_stm_issue_discover/README.md)。
3. **`../eval/` 系列链接全部失效**：[PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md)
   里有 10 处（§1.3、§4、§5、§6、§7.2 等，指向 `../eval/PROTOCOL.md`、
   `../eval/extract/umple.py`、`../eval/extract/pyfcstm.py`、`../eval/review/render.py`、
   `../eval/demo/finalize_after_signoff.py` 等）。这些现在都在
   [../path1_evaluation/](../path1_evaluation/) 下，例如
   [../path1_evaluation/PROTOCOL.md](../path1_evaluation/PROTOCOL.md)、
   [../path1_evaluation/extract/pyfcstm.py](../path1_evaluation/extract/pyfcstm.py)。
4. §5 的 `run_path1` / `run_path2` 命令是死命令，见本文件 §2。
5. 两份 GUIDE 提到的 `PATH1_REPORT.md` / `PATH2_REPORT.md` / `OUTLINE.md`
   等产出物**在本目录里不存在**——路线在产出这些之前就转舵了。
   本目录只有 §0 表格里那 7 个文件。

> 这些链接**未就地修复**，原因是原件属于冻结件；腐烂项集中登记在本节，
> 修与不修由复活者按需决定。
