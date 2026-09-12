# 历史实现归档说明

本目录是 `witness_search_prototype` 的历史快照，归档日期为 2026-08-21。

- 仅用于复现旧实验、核对迁移行为和追溯历史决策；
- 不属于当前运行路径，不是现行方法名，也不是新结果的证据来源；
- 其中的五类 typed obligation、旧 relation、旧谓词和 `prototype.py` 单体结构均已淘汰；
- 不得从本目录直接新增或恢复谓词。任何候选变更必须通过现行
  [`METHOD_PRINCIPLES.md`](../../evidence_discovery/METHOD_PRINCIPLES.md) 的独立来源、
  命题匹配、兼容性和测试门；
- 新实现的唯一规范入口是
  [`pipeline/evidence_discovery/`](../../evidence_discovery/)。

归档不删除历史代码，但历史代码中的数字、来源计数和实验报告不能自动转成当前结论。
