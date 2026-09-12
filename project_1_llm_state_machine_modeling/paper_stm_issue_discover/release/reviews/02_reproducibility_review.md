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

## 最终复核追加

独立 reviewer 在 `0377c74f376653025cb752f0eec941fb7663c721` 复核：本地 HEAD 与
`origin/paper1/m-witness-discovery` 一致。远端 annotated tag
`paper1-v60-method-66b5d71ae` 的 peel target 为
`66b5d71aecd73f6eeddac082037f7c34e04da057`，
`paper1-semantic-judge-05cf0da6f` 的 peel target 为
`05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`；冻结实验引用与远端 ref 已闭合。

`validate_release_structure.py` 再次通过：2671/2671 冻结归档文件、465/465 历史
pytest node ID、registry/source catalog/Judge protocol hash 和 AST import boundary 均
一致，无 boundary violation；provider/billable calls 均为 0。两个 archive validator
入口仍均返回 `final-results archive validation passed`，仅出现既有 Pydantic `schema`
shadow warnings。工作树无 tracked 改动，且本次复核没有调用 provider 或启动实验。

冻结复现和远端引用已闭合。公开再分发的剩余硬阻塞是权利人提供并授权 method-source
`LICENSE`；许可证解决后，仍应按 release-candidate 协议完成最终离线/clean-install 验收，
才可执行唯一允许的 15x1 回归。

## 2026-08-28 后续裁定

本节记录后续范围裁定，不改变上文当时的审查结论。method-source 的权利人 LICENSE 仍是正式公开再分发和法律声明的前置条件，但不是内部技术验收的前置条件。

在该裁定下，internal RC 的发布包、clean-install、固定 15-pair x 1 method + Judge 回归及其对照审计均已完成，材料见 [release_validation/](../../release_validation/README.md)。这不表示 method source 已获得对外再分发许可；公开发布前仍需权利人明确提交 LICENSE。

## 2026-08-30 v4 复核追加

后续 current re-audit v4 增加了 10 个已提交的 v2 manual-adjudication contract tests。原始
release baseline `bebcd749ef7d283675971b8ad3c185596f2c878c` 的 465 个 node 保持不变；
`release/documentation_audit/test_universe_change.json` 逐项记录了新增 node、源码 SHA-256
和引入提交 `5f70a12b5797da19d1b5c963fcfd00683b477840`。因此当前精确集合为
`465 + 10 = 475`，不是对历史基线的静默重写；validator 只接受这 10 个 additions，任何
其他 node 漂移仍失败。

在该例外记录下，release structure validator 通过（2671/2671 冻结归档文件、475 当前
pytest node、资源 hash、AST import boundary），精确 release test universe 的 provider-free
测试为 `475 passed`。
本追加没有调用 provider，也没有运行 method/Judge 或修改 raw、reference 和冻结结果。
