# Paper1 Scripts

本目录只保留薄命令行适配器。业务逻辑分别属于 method、Judge 或 evaluation 包；脚本不会重写冻结 run、final_results、ledger 或 protocol。下表中的所有 `--help` 示例均不调用 provider。

| 脚本 | 用途 | provider 与写入边界 | 示例 |
| --- | --- | --- | --- |
| [release/build_method_release.py](./release/build_method_release.py) | 按 allowlist 复制 method 发布树并写逐文件 manifest/hash | 无 provider；只写 checkout 外的空输出目录 | `python scripts/release/build_method_release.py --output /tmp/paper-stm-method-release` |
| [release/build_judge_release.py](./release/build_judge_release.py) | 按 allowlist 构建独立 Judge 发布树 | 无 provider；只写 checkout 外的空输出目录 | `python scripts/release/build_judge_release.py --output /tmp/paper-stm-judge-release` |
| [release/capture_release_baseline.py](./release/capture_release_baseline.py) | 记录冻结 hash、测试 node 与发布结构基线 | 无 provider；只写显式 `--output` | `python scripts/release/capture_release_baseline.py --help` |
| [release/validate_release_structure.py](./release/validate_release_structure.py) | 校验 import boundary、allowlist、冻结 hash 和历史 node | 无 provider；只读仓库和显式 Python 环境 | `python scripts/release/validate_release_structure.py --help` |
| [method/replay.py](./method/replay.py) | 从已保存制品复算 W-state replay | 无 provider；只写调用者指定的新 replay 目录 | `python scripts/method/replay.py --help` |
| [method/route_replay.py](./method/route_replay.py) | 复算保存候选的确定性 primary route | 无 provider；只写显式输出 | `python scripts/method/route_replay.py --help` |
| [method/frontier_replay.py](./method/frontier_replay.py) | 复算 typed frontier 与其 receipt | 无 provider；只写显式输出 | `python scripts/method/frontier_replay.py --help` |
| [method/execution_probe_replay.py](./method/execution_probe_replay.py) | 复算保存执行 probe 的确定性结果 | 无 provider；只写显式输出 | `python scripts/method/execution_probe_replay.py --help` |
| [method/structural_rebind_replay.py](./method/structural_rebind_replay.py) | 用当前 typed 逻辑重新绑定保存的结构候选 | 无 provider；只写显式输出 | `python scripts/method/structural_rebind_replay.py --help` |
| [method/native_projection_audit.py](./method/native_projection_audit.py) | 审计 pyfcstm native projection 与输入闭包 | 无 provider；只写显式 JSON 输出 | `python scripts/method/native_projection_audit.py --help` |

真实 method 或 Judge 执行不是本目录脚本的隐式副作用：必须直接使用各包 CLI，并显式给出 profile、输出目录和 `--allow-live`。历史 frozen artifact 的复算入口在 [evaluation/](../evaluation/README.md)；旧 `pipeline` compatibility namespace 不应用于新脚本。
