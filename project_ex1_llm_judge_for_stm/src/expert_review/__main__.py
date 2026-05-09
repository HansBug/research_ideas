"""``python -m expert_review`` 命令行入口。

**作用**：

提供一个最小可用的 CLI：从命令行接收 ``--prompt`` / ``--input`` /
``--pred-output`` / ``--ref-output`` 4 个参数，跑一次 review 后把
结果以 JSON 字符串打印到 stdout。常用于 dry-run 与小批量手动验证。

**设计思路**：

* 走 :mod:`.compatibility` 的 ``review_model`` 入口（与历史
  ``heuristic_expert_review`` 形态一致），避免直接暴露
  :class:`agent.ExpertReviewAgent`；
* 对结果使用 :func:`schema.to_json` 序列化，保留中文 (
  ``ensure_ascii=False``) 与缩进 2 空格；
* 不读取 stdin 或文件——用户应通过 shell 把文件内容用
  ``"$(cat file.txt)"`` 传入，或改用 :func:`batch.run_batch_review`。

**关键约束 / caveat**：

* 本 CLI **不带 strict-llm 选项**——若没有可用 provider，
  ``review_model`` 会走 deterministic 路径；
* 不适合大批量评审；批量请用
  ``python -m expert_review.batch`` (经 :mod:`.batch.main`)。
"""

from __future__ import annotations

import argparse

from .compatibility import review_model
from .schema import to_json


def main() -> None:
    """CLI 主入口：解析参数 → 跑评审 → 打印 JSON。

    命令行示例::

        python -m expert_review \\
            --prompt "请评估状态机是否覆盖需求" \\
            --input "R1: 启动后进入空闲态" \\
            --pred-output "@startuml\\n[*] --> Idle\\n@enduml"

    :raises SystemExit: 当必填参数缺失时（由 argparse 抛 SystemExit(2)）
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--input", required=True, dest="input_text")
    parser.add_argument("--pred-output", required=True, dest="pred_output")
    parser.add_argument("--ref-output", default=None, dest="ref_output")
    args = parser.parse_args()

    result = review_model(
        prompt=args.prompt,
        input_text=args.input_text,
        pred_output=args.pred_output,
        ref_output=args.ref_output,
    )
    print(to_json(result))


if __name__ == "__main__":
    main()
