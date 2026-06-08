# Skill stage index policy

本目录是 `agent_loop_skill` 暴露给 Codex / Claude Code 的 stage 索引。
多数 `*.md` 文件是指向共享 `project_1_llm_state_machine_modeling/method/stages/docs/`
的符号链接；在 PR-skill-fix 中这些 symlink target 默认视为**只读共享
runtime/stage 文档**，不要为了修 skill 健康而直接改写 `method/stages/docs/`。

## 默认主链

PR-E1 后，skill 使用者应按下面的 repair 主链理解 stage：

```text
SD-8 FixRequestBatch
-> SL-9 per-request accept/reject + repair
-> SL-10(NL + FixLog + local evidence)
-> SC-11
-> SD-2
```

其中：

- `SD-8`：把 selected feedback 转成 `FixRequestBatch`，但不做最终修复决策。
- `SL-9`：必须读取 `FixRequestBatch` 与完整 `FixLog`，对每个 request 给出
  accept/reject/waiver，并在至少 accept 一个 request 时产出 candidate DSL。
- `SL-10`：默认 repair review；必须输入 NL、FixLog、SL-9 decisions、diff 与
  local deterministic evidence。
- `SC-11`：只接受候选并触发回到 `SD-2` 的完整重验，不代表 final success。

## Legacy / local-evidence 链接

- `SD-10.md` 当前仍作为 legacy deterministic repair-review / `SL-10`
  `local_check_evidence` 的文档线索存在；它**不是** PR-E1 后 E2 skill 的默认
  repair review 主链。
- `SL-10B.md` 只保留为 legacy / ablation delta review 线索；E2 skill smoke 不应
  把它当成默认准出 gate。

如果 stage symlink target 的历史措辞与以上 policy 发生张力，本 PR 的处理方式是：
在 `agent_loop_skill/` 内通过本 README、`tools.md`、`prompts.md`、
`e2e_ref_model_guide.md` 或 `health_check.py` 遮蔽误导；不要在本 PR 中直接突破
skill 路径去修改共享 stage docs。

## 程序化调用入口

本目录中的 stage 文档索引是**人类可读**入口，用于快速跳转到共享 stage 文档；它不是程序化调用 API。
Codex / Claude Code / toolbox 若需要调用工具，应从 Python facade 导入：

- `method.stages.api`：skill-facing 总入口，汇总 SD deterministic tools、SL prompt builders 与 SC summary helpers。
- `method.stages.sc_control`：no-provider SC/control 摘要与 stage order helper。
- `method.stages.sl_prompt_api`：SL prompt generator facade；不是 standalone prompt implementation，底层共享工具仍在 `sl_prompt_common.py`。

这些 facade 不读取 `.env`、不调用 provider、不得调用 `method.loop.run_agent_loop(...)`。
