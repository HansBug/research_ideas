# quality_model/ — 质量模型入口

本目录维护 STM repair 结果的质量判定模型。当前核心文件是 [better_stm_definition.md](./better_stm_definition.md)。

## 当前约束

1. Better STM 五条件是 RQ4 的最低必要条件。
2. 质量模型不得因后续真实结果好坏而反向改写。
3. converter / normalization 收益必须与 repair-loop 收益分开统计。
