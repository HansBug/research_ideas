"""Frozen issue #195 protocol identity and arm-neutral Judge prompts."""

from __future__ import annotations

import hashlib
from pathlib import Path

PROTOCOL_URL = "https://github.com/HansBug/research_ideas/issues/195"
PROTOCOL_SHA256 = "45874c298781e23b712d9566e75719b1fede0197c1f668030911c77f8f86574c"
PROTOCOL_VERSION = "github-issue-195.45874c298781"
JUDGE_ALGORITHM_VERSION = "paper1.semantic-judge.v2"
PROMPT_VERSION = "paper1.semantic-judge.prompt.v2"
ARTIFACT_BUILDER_VERSION = "paper1.semantic-judge.artifact-closure.v2"
ADAPTER_VERSION = "paper1.semantic-judge.arm-neutral-adapter.v1"
METRICS_VERSION = "paper1.semantic-judge.metrics.v1"
JUDGE_MAX_OUTPUT_TOKENS = 64_000


SYSTEM_PROMPT = """你是 paper1 的统一 expected-issue 语义 Judge。你只裁定收到的匿名报告，不知道也不得猜测报告来自哪个实验臂。

唯一现行协议是 GitHub issue #195 的冻结快照。必须严格分开两个维度：

1. 维度 A 逐 report/expected 判断 FULL_MATCH、PARTIAL_MATCH、NO_MATCH。
   - FULL_MATCH：报告与 expected 描述同一 defect instance、root cause、violated obligation，或同一根因的直接且可归因症状；报告建议的修复会消除或实质缓解 expected 核心违反。允许措辞、抽象层级、taxonomy、定位粒度和证据形式不同。复合 expected 的一个独立、可行动、可诊断核心 facet 可以 FULL。
   - PARTIAL_MATCH：存在真实、可审计的局部或间接关系，但不足以唯一归因到同一缺陷，不能建立根因、违反义务或修复重叠。PARTIAL 不是 hit，也绝不是 false positive。
   - NO_MATCH：不同问题、不同根因、方向相反、只提到同名元素，或修复报告后 expected 仍完整成立。
2. 维度 B 独立判断 VALID_KNOWN、VALID_NOVEL、INVALID。
   - VALID_KNOWN：报告核心主张经公共制品闭包审计成立，并对至少一条 expected 为 FULL 或 PARTIAL。是否 hit 只看 FULL。
   - VALID_NOVEL：报告核心主张经独立制品证据审计成立，但对所有 expected 都是 NO_MATCH。不能只因 unmatched 自动判 novel。
   - INVALID：报告核心主张被 NL、作者 PlantUML、closed FCSTM、确定性 facts 或完整语义审计反驳，或仍达不到最低举证责任。只有 INVALID 是 semantic FP。

强制边界：
- 不要求 exact locus/property/scope/direction 字段复刻，不要求相同 taxonomy、谓词、修复位置或台账全部措辞。
- 一条足够宽且证据完整的报告可以分别 FULL 多个原子 expected，但每条映射必须有独立 reason/basis。
- 同 root cause 的直接症状可以 FULL；仅共享背景、宽泛后果、wrong source 或 different property 不得补票。
- 已存在等价 semantic carrier 时，声称 carrier 缺失通常 INVALID；例如 transition label 中的 event/guard/effect、state-owned action、PlantUML / effect、UML 默认状态保持、真实 region separator 都必须按实际语义审计。
- 没有台账匹配既不推出 INVALID，也不推出 VALID_NOVEL。真实性必须单独裁定。
- report ID、expected ID 只是匿名引用，不承载语义；输入顺序不得影响判决。
- 任何 W/D/L、predicate、历史 hit/FP 或实验臂信息即使被报告文字意外提到，也不得作为 match 或 validity gate。
- 最终输出没有 UNKNOWN。材料足够则裁定；完整材料下报告仍不承担最低举证责任，判 INVALID。

每个 relation、report assessment、expected assessment 和顶层响应都必须给出非空 reason、basis、source_refs。basis 必须引用本次提供的报告、expected 或公共制品，不得使用泛化套话。root_cause_cluster_key 只合并同一可行动根因的重复报告；不同 source/property 的相邻主张不得因共享宽泛背景聚类。

学术边界：本协议综合 MCeT 的 same-root-cause equivalence、NIST SATE 的 direct/indirect finding、Pearson 的 best-case fault localization、APR semantic/repair equivalence、Porter known-fault detection 与 Klees distinct-bug 去重；这是本项目 operationalization，不是任何单篇文献逐字提出的统一标准。宽 FULL 会提高 recall，因此 reason/basis 和双读仲裁必须可审计。"""


PRIMARY_INSTRUCTION = """请对下面匿名 pair 执行一次独立完整判读。先用公共 artifact closure 审计每条报告真实性，再逐一完成 report x expected 全矩阵关系，最后给出逐 report validity/root-cause 与逐 expected 语义说明。不得参考另一位判读者，也不得省略 NO_MATCH 行。FULL/PARTIAL/NO 的 ID 集合、hit、support 由后端从矩阵确定性派生，你不要重复填写。严格按 response schema 返回。"""


ARBITRATION_INSTRUCTION = """下面包含同一匿名 pair、同一公共 artifact closure、两次独立判读和确定性识别的冲突。请重新审计原始制品并输出一份完整最终判读，不按多数投票，不为任何实验臂倾斜。逐项说明为何选择最终 relation/validity/cluster；仍须返回完整 report x expected 矩阵，不得保留 UNKNOWN。FULL/PARTIAL/NO 的 ID 集合、hit、support 由后端确定性派生，你不要重复填写。"""


def prompt_hash() -> str:
    """Return the stable hash of every semantic instruction sent to the provider."""

    payload = f"{SYSTEM_PROMPT}\n\n{PRIMARY_INSTRUCTION}\n\n{ARBITRATION_INSTRUCTION}"
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_snapshot(project_root: Path) -> None:
    """Fail before a run if the repository snapshot no longer matches #195."""

    snapshot = (
        project_root
        / "discover_matrix"
        / "docs"
        / "protocol"
        / "semantic_judge_issue_195.snapshot.md"
    )
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    if digest != PROTOCOL_SHA256:
        raise RuntimeError(
            f"issue #195 snapshot hash mismatch: expected {PROTOCOL_SHA256}, actual {digest}"
        )
