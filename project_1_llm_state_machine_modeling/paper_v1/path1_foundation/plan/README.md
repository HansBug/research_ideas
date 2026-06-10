# plan/：任务状态、review 记录与执行包

本目录维护当前 foundation PR 的任务状态、review 记录和后续 agent 可接续的 task packet。它不是论文正文，也不是实验结果目录。

## 文件说明

| 文件 / 目录 | 作用 |
|---|---|
| [progress.md](./progress.md) | 记录 foundation PR 当前进度、已完成动作、review log、验证命令与剩余风险。 |
| [task-packets/foundation.md](./task-packets/foundation.md) | 当前 PR 的任务合同，包括允许改动范围、拒收检查和验证命令。 |

## 使用规则

1. 每次结构调整、资产迁移、review 或 C/I 修复后，都应更新 [progress.md](./progress.md)。
2. 后续如果拆出新的 paper 子任务，应在 `task-packets/` 下新增对应 task packet。
3. 不要把用户过程指令直接写进 manuscript；应先落到本目录或对应 planning 文件中。
