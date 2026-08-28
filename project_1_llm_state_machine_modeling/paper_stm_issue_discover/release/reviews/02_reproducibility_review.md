# 冻结复现独立审查

## 范围与方法

独立 reviewer 在 `8d6881c530527fcf31cbe21af157e6bc094050d8` 上只读核对
`release/baseline_manifest.json`、冻结归档、历史 pytest node universe、资源 hash、
新旧 archive validator、实验 tags 和未跟踪路径。检查不读取或改写 `runs/`，没有
provider 调用。

## 结果

- 基线为 `d31a8d171c08c2cc32650d0c08c4e8ac6b43818c`，记录 465 个历史 pytest node ID。
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

## 限制与结论

结构 validator 的 `provider_call_count=0` 是本次离线验证的声明，不能单独证明过去的
外部网络历史。Git 历史、无新增 tracked run/release_validation/final_results 及本次命令
记录共同支持“当前 refactor 尚未运行 provider”的结论。`.omx/goals/`、`.worktrees/` 和
`paper_stm_issue_discover/runs/` 保持用户未跟踪状态且未触碰。

冻结资源、归档与测试 universe 均无漂移；最终阶段仍须在 release candidate 后重新运行
同一组离线验证，并推送 tags。
