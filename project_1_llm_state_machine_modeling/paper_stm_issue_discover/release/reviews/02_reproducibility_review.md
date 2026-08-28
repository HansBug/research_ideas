# 冻结复现独立审查

## 范围与方法

独立 reviewer 在 `a3e2bad40091fbba467e208ad0ac74ac9c29231b` 上只读核对
`release/baseline_manifest.json`、冻结归档、历史 pytest node universe、资源 hash、
新旧 archive validator、实验 tags 和未跟踪路径。检查不读取或改写 `runs/`，没有
provider 调用。

## 结果

- 基线为 `d31a8d171c08c2cc32650d0c08c4e8ac6b43818c`，记录 465 个历史 pytest node ID；
  当前收集仍为 `465/465`。
- `final_results/v60_current_vs_x1v2_baseline` 的 2671/2671 个冻结文件 SHA-256 与字节数
  与基线 manifest 一致。
- 465/465 历史 node ID 仍被收集；归一化 node 集合 hash 为
  `sha256:182e0e0ebd831be5424bffae5a5cb1a7c83c80f1f38a12293048da2d8a404143`。
- registry、source catalog、Judge protocol 分别保持
  `38fa2e…15ca`、`45ee60…5647`、`d774d9…b210`。
- 新入口 `paper_stm_evaluation.final_results_archive` 和兼容入口
  `pipeline.evidence_discovery.reporting.final_results_archive` 都返回
  `final-results archive validation passed`。
- 两个 immutable experiment tag 在本地正确指向 `66b5d71a…` 与 `05cf0da6…`，但审查时
  尚未推送到 `origin`；最终交付必须推送它们与 refactor 分支。

## 发现与处理

| 严重度 | 发现 | 处理或 gate |
| --- | --- | --- |
| 高 | `method/NOTICE.md` 明确未授予 method source 再分发许可，且尚无权利人批准的 source license。 | 不能由 refactor 或测试替代；在授权和提交许可证前不得声称公开发布完成，也不得创建最终 release candidate 或启动 15x1。 |
| 高 | 远端尚未包含 refactor 分支和两枚 immutable experiment tag。 | 在最终 release-candidate commit 之后推送分支和 tags，并以 `git ls-remote` 复核。 |
| 中 | 旧审查记录只覆盖 `8d6881c...`，不能证明后续 release provenance 修复。 | 本记录更新为 `a3e2bad4...` 审计截点；`0a87639e2` 已修复 Judge packaged provenance，最终 candidate 仍须重跑完整 provider-free、clean-install 和重复构建验收。 |

## 限制与结论

结构 validator 的 `provider_call_count=0` 是本次离线验证的声明，不能单独证明过去的
外部网络历史。Git 历史、无新增 tracked run/release_validation/final_results 及本次命令
记录共同支持“当前 refactor 尚未运行 provider”的结论。`.omx/goals/`、`.worktrees/` 和
`paper_stm_issue_discover/runs/` 保持用户未跟踪状态且未触碰。

冻结资源、归档与测试 universe 均无漂移。许可证授权、最终 candidate 后的完整离线验收和
远端 ref 复核完成前，不得启动唯一允许的 15x1 live regression。
