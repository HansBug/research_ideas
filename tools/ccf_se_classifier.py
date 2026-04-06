#!/usr/bin/env python3
"""Classify yearly CCF papers into SE / non-SE and SE field paths.

This tool is intentionally offline: it reads the generated yearly
metadata under ``frontier_index/ccf_history/<year>/metadata/*.json``,
combines venue-level priors from ``frontier_index/CCF_SE_A_B_C.md`` and
the current SE field tree, then writes back:

1. per-paper macro area and SE inclusion fields
2. x.x.x primary path and label for SE papers
3. a re-rendered yearly README with the new classification columns
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from tools.ccf_se_index_builder import CCF_MD, ROOT, Venue


@dataclass(frozen=True)
class PhdVenueFit:
    grade: str
    rationale: str


TREE_MD = ROOT / "frontier_index" / "SOFTWARE_ENGINEERING_FIELD_TREE.md"
MANUAL_REVIEW_DIRNAME = "manual_review"
MANUAL_OVERRIDE_FILENAME = "overrides.json"
MANUAL_BATCH_DIRNAME = "batches"


SE_LEVEL_PRIOR = {
    "完全属于软工": 3,
    "大部分属于软工": 2,
    "部分属于软工": 0,
    "大部分不属于软工": -2,
    "完全不属于软工": -3,
}


MACRO_DISPLAY_ORDER = (
    "软件工程",
    "跨域/待判定",
    "程序设计语言与形式化基础",
    "系统软件",
    "待补",
)


SE_DECISION_DISPLAY_ORDER = (
    "属于软件工程",
    "跨域但软工主导",
    "不属于软件工程",
    "待判定",
    "待补",
)


PHD_GRADE_EMOJI = {
    "A": "🔥",
    "B": "🟢",
    "C": "🟡",
    "D": "⚪",
}


PHD_GRADE_LABEL = {
    "A": "强相关",
    "B": "较相关",
    "C": "可补链",
    "D": "低相关",
}


PHD_GRADE_DISPLAY_ORDER = ("A", "B", "C", "D")


PHD_VENUE_RELEVANCE: Dict[Tuple[str, str, str], PhdVenueFit] = {
    ("ASE", "A", "会议"): PhdVenueFit("A", "自动化软件工程 / LLM for SE / 建模-验证-修复主场"),
    ("FM", "A", "会议"): PhdVenueFit("A", "形式化方法 / timed automata / 工业与控制系统验证邻近"),
    ("FSE", "A", "会议"): PhdVenueFit("A", "broad SE + LLM/需求建模/测试验证/修复主线"),
    ("ICSE", "A", "会议"): PhdVenueFit("A", "broad SE 主会，需求-建模-验证-修复全链可见"),
    ("ISSTA", "A", "会议"): PhdVenueFit("A", "测试分析 / 形式化验证 / 缺陷定位与修复主场"),
    ("OOPSLA", "A", "会议"): PhdVenueFit("C", "软件结构 / 程序分析 / 重构与验证偶发贴题"),
    ("OSDI", "A", "会议"): PhdVenueFit("D", "系统实现 / 平台机制为主，仅极少验证个案"),
    ("PLDI", "A", "会议"): PhdVenueFit("C", "程序分析 / 软件验证 / repair 邻近但需严格筛选"),
    ("POPL", "A", "会议"): PhdVenueFit("D", "语义 / 类型 / 逻辑证明主场，低概率直接贴题"),
    ("SOSP", "A", "会议"): PhdVenueFit("D", "操作系统机制主场，低概率直接贴题"),
    ("TOPLAS", "A", "期刊"): PhdVenueFit("D", "语言 / 语义 / 编译与理论为主"),
    ("TOSEM", "A", "期刊"): PhdVenueFit("A", "软件工程方法 / 需求建模 / 测试验证 / AI for SE"),
    ("TSC", "A", "期刊"): PhdVenueFit("C", "服务工作流 / 平台 orchestration 邻近，可补性质工程"),
    ("TSE", "A", "期刊"): PhdVenueFit("A", "broad SE 主刊 / 建模验证修复与 LLM 子题持续出现"),
    ("CAiSE", "B", "会议"): PhdVenueFit("B", "信息系统与过程/模型工程，适合补需求-建模-规约链"),
    ("CC", "B", "会议"): PhdVenueFit("D", "编译构造主场"),
    ("CP", "B", "会议"): PhdVenueFit("D", "约束求解主场，仅少量可借工具思想"),
    ("ECOOP", "B", "会议"): PhdVenueFit("C", "OO 程序结构 / 分析与重构邻近"),
    ("ESEM", "B", "会议"): PhdVenueFit("B", "实证方法 / 评测设计 / LLM-SE 实验口径重要"),
    ("ETAPS", "B", "会议"): PhdVenueFit("B", "TACAS/FASE 等 formal methods 线对验证与工具很有用"),
    ("HotOS", "B", "会议"): PhdVenueFit("D", "系统热点想法为主"),
    ("ICFP", "B", "会议"): PhdVenueFit("D", "函数式语言理论主场"),
    ("ICPC", "B", "会议"): PhdVenueFit("B", "程序理解 / 缺陷分析 / 修复解释与人因辅助"),
    ("ICSME", "B", "会议"): PhdVenueFit("B", "维护演化 / 修复 / 回归验证 / 工程闭环邻近"),
    ("ICSOC", "B", "会议"): PhdVenueFit("C", "服务组合 / 流程 / 性质与治理偶有贴题"),
    ("ICWS", "B", "会议"): PhdVenueFit("C", "Web services / orchestration / 性质验证偶有贴题"),
    ("ISSRE", "B", "会议"): PhdVenueFit("A", "可靠性 / assurance / 安全关键验证与缺陷检测很近"),
    ("LCTES", "B", "会议"): PhdVenueFit("C", "嵌入式 / 实时软件邻近，可补控制系统实现背景"),
    ("Middleware", "B", "会议"): PhdVenueFit("D", "中间件与平台机制为主"),
    ("MoDELS", "B", "会议"): PhdVenueFit("A", "模型驱动 / 状态机-SysML / 形式化建模主场"),
    ("RE", "B", "会议"): PhdVenueFit("A", "需求工程 / 规约抽取 / 性质生成 / 需求到模型"),
    ("SANER", "B", "会议"): PhdVenueFit("B", "代码分析 / 逆向 / 演化与 reengineering"),
    ("SAS", "B", "会议"): PhdVenueFit("C", "静态分析与抽象解释对验证/修复有方法借鉴"),
    ("VMCAI", "B", "会议"): PhdVenueFit("A", "程序验证 / 模型检查 / 抽象解释直接支撑验证框架"),
    ("ASE", "B", "期刊"): PhdVenueFit("A", "自动化软件工程 / LLM for SE / 建模-验证-修复主场"),
    ("ESE", "B", "期刊"): PhdVenueFit("B", "实证研究 / 数据集 / benchmark / 人因与评测设计"),
    ("IETS", "B", "期刊"): PhdVenueFit("C", "broad SE 期刊，可筛少量建模/验证论文"),
    ("IST", "B", "期刊"): PhdVenueFit("B", "broad SE / 建模测试 / AI4SE 论文较常见"),
    ("JFP", "B", "期刊"): PhdVenueFit("D", "函数式编程理论主场"),
    ("JSEP", "B", "期刊"): PhdVenueFit("B", "演化 / 过程 / 迭代闭环与工程实践邻近"),
    ("JSS", "B", "期刊"): PhdVenueFit("B", "系统与软件工程综合刊，常见建模/验证/CPS 个案"),
    ("RE", "B", "期刊"): PhdVenueFit("A", "需求工程 / 规约抽取 / 性质生成 / 需求到模型"),
    ("SCP", "B", "期刊"): PhdVenueFit("B", "软件程序与形式化/验证/程序分析交叉，贴题概率中高"),
    ("SPE", "B", "期刊"): PhdVenueFit("C", "工程实践 / 系统实现为主，偶有 runtime/verification"),
    ("STVR", "B", "期刊"): PhdVenueFit("A", "测试 / 验证 / 可靠性与 formal properties 非常贴题"),
    ("SoSyM", "B", "期刊"): PhdVenueFit("A", "软件与系统建模 / DSL / 状态机与模型分析主场"),
    ("APLAS", "C", "会议"): PhdVenueFit("D", "程序设计语言理论主场"),
    ("APSEC", "C", "会议"): PhdVenueFit("B", "broad SE / 亚洲社区，LLM-SE/测试/建模可见"),
    ("ATVA", "C", "会议"): PhdVenueFit("B", "自动验证与分析 / 模型检查工具链直接邻近"),
    ("COMPSAC", "C", "会议"): PhdVenueFit("C", "覆盖过宽，需按建模/验证/AI4SE 子题筛选"),
    ("EASE", "C", "会议"): PhdVenueFit("B", "评测与实验设计 / benchmark / replication 有用"),
    ("ICECCS", "C", "会议"): PhdVenueFit("B", "复杂系统建模与验证 / safety-critical / CPS 邻近"),
    ("ICFEM", "C", "会议"): PhdVenueFit("A", "formal engineering / 规约建模 / 验证与证明"),
    ("ICSR", "C", "会议"): PhdVenueFit("C", "复用 / 组件资产，可补模型资产与可复用工件"),
    ("ICSSP", "C", "会议"): PhdVenueFit("C", "软件过程 / 团队与流程，对主问题较间接"),
    ("ICST", "C", "会议"): PhdVenueFit("A", "测试 / 形式化验证 / 缺陷检测与修复直接相关"),
    ("ICWE", "C", "会议"): PhdVenueFit("D", "Web 工程主场"),
    ("ISPASS", "C", "会议"): PhdVenueFit("D", "性能分析主场"),
    ("Internetware", "C", "会议"): PhdVenueFit("C", "平台 / 网络化软件 / 运行治理邻近"),
    ("LOPSTR", "C", "会议"): PhdVenueFit("D", "逻辑程序综合与变换主场"),
    ("MEMOCODE", "C", "会议"): PhdVenueFit("B", "协同设计 / 嵌入式与形式化模型，控制/CPS 邻近"),
    ("MSR", "C", "会议"): PhdVenueFit("B", "仓库挖掘 / benchmark / LLM-SE 证据与数据建设有用"),
    ("PASTE", "C", "会议"): PhdVenueFit("B", "程序分析与软件工具工程，对验证/修复较近"),
    ("PEPM", "C", "会议"): PhdVenueFit("D", "部分求值与程序变换主场"),
    ("QRS", "C", "会议"): PhdVenueFit("A", "质量 / 可靠性 / 安全 / assurance 与验证链很近"),
    ("REFSQ", "C", "会议"): PhdVenueFit("A", "需求质量 / 需求规约 / 需求到性质非常贴题"),
    ("RV", "C", "会议"): PhdVenueFit("A", "运行时验证 / 监测 / 时序性质 / 工具链直接邻近"),
    ("SCAM", "C", "会议"): PhdVenueFit("B", "源码分析与变换 / 缺陷修复 / 程序理解邻近"),
    ("SEKE", "C", "会议"): PhdVenueFit("C", "SE+知识工程混合，AI/建模偶有贴题"),
    ("SPIN", "C", "会议"): PhdVenueFit("A", "软件模型检查 / state-based verification / UPPAAL 邻近"),
    ("SSE", "C", "会议"): PhdVenueFit("C", "软件服务工程混合"),
    ("TASE", "C", "会议"): PhdVenueFit("B", "软件工程名下的 formal verification / assurance 邻近"),
    ("WICSA", "C", "会议"): PhdVenueFit("B", "软件架构 / 设计决策 / 模型结构与演化有用"),
    ("CL", "C", "期刊"): PhdVenueFit("C", "语言/结构与偶发程序分析，可补方法链"),
    ("IJSEKE", "C", "期刊"): PhdVenueFit("C", "SE+知识工程混合，AI/建模可补链但不稳定"),
    ("JLAMP", "C", "期刊"): PhdVenueFit("D", "逻辑与代数程序方法理论主场"),
    ("JWE", "C", "期刊"): PhdVenueFit("D", "Web 工程主刊，与主问题距离较远"),
    ("PACM PL", "C", "期刊"): PhdVenueFit("C", "PL 主刊，程序验证/分析个案可补链"),
    ("SOCA", "C", "期刊"): PhdVenueFit("C", "服务计算与应用为主"),
    ("SQJ", "C", "期刊"): PhdVenueFit("B", "质量 / 度量 / assurance 视角可支撑验证评价"),
    ("STTT", "C", "期刊"): PhdVenueFit("A", "验证工具 / formal methods tool transfer / UPPAAL 邻近"),
    ("TPLP", "C", "期刊"): PhdVenueFit("D", "逻辑程序设计理论与实践主场"),
}


GENERIC_TREE_KEYWORDS = {
    "testing",
    "contracts",
    "benchmarking",
    "planning",
    "architecture",
}


EDITORIAL_LIKE_PATTERNS = [
    "editorial",
    "guest editorial",
    "corrigendum",
    "state of the journal",
    "former editor-in-chief",
]


SYNTHESIS_LIKE_PATTERNS = [
    "roadmap",
    "research agenda",
    "retrospective",
    "reflection",
    "vision and roadmap",
]


DATASET_LIKE_PATTERNS = [
    "dataset",
    "benchmark dataset",
    "benchmark suite",
    "corpus",
    "artifact package",
]


AI_FOR_SE_PREFIX_HINTS: Dict[str, List[str]] = {
    "7.1.1": [
        "code generation",
        "code completion",
        "code translation",
        "program synthesis",
        "code transformation",
        "code review comment generation",
    ],
    "7.1.2": [
        "testing",
        "test generation",
        "fuzzing",
        "bug detection",
        "fault localization",
        "program repair",
        "repair",
        "static analysis",
        "dynamic analysis",
        "vulnerability detection",
    ],
    "7.1.3": [
        "requirements",
        "traceability",
        "summarization",
        "documentation",
        "comment generation",
        "domain model",
    ],
    "7.1.4": [
        "architecture",
        "design",
        "decision support",
        "planning",
    ],
    "7.1.5": [
        "human-ai workflow",
        "trust",
        "calibration",
        "developer study",
        "user study",
        "copilot workflow",
    ],
}


MANUAL_LEAF_KEYWORDS: Dict[str, List[str]] = {
    "1.1.1": [
        "requirements elicitation",
        "requirement elicitation",
        "requirements extraction",
        "requirement extraction",
        "stakeholder",
        "user story",
        "user feedback",
        "feedback mining",
        "interview study",
        "use case",
        "use case description",
        "requirements specification",
    ],
    "1.1.2": [
        "requirements prioritization",
        "requirement prioritization",
        "goal model",
        "goal-oriented",
        "stakeholder negotiation",
        "priority ranking",
    ],
    "1.1.3": [
        "requirements quality",
        "requirement quality",
        "requirements ambiguity",
        "ambiguity detection",
        "requirement inconsistency",
        "requirements consistency",
        "requirements inconsistency",
        "inconsistency in requirements",
        "inconsistencies in requirements",
        "ambiguous requirement",
    ],
    "1.1.4": [
        "traceability",
        "trace link",
        "requirements traceability",
        "impact analysis",
        "change impact",
        "rationale recovery",
    ],
    "1.1.5": [
        "requirements reuse",
        "requirement reuse",
        "requirements debt",
        "requirement debt",
        "requirements pattern",
        "pattern library",
    ],
    "1.2.1": [
        "formal specification",
        "formal specifications",
        "contract-based",
        "software contract",
        "invariant inference",
    ],
    "1.2.2": [
        "natural language to",
        "specification mining",
        "property mining",
        "property extraction",
        "nl2ltl",
    ],
    "1.2.3": [
        "specification consistency",
        "specification completeness",
        "satisfiability",
        "consistency checking",
        "specification inconsistency",
        "specification inconsistencies",
    ],
    "1.2.4": [
        "assurance case",
        "safety case",
        "compliance rule",
        "regulatory requirement",
    ],
    "1.3.1": [
        "modeling language",
        "modeling framework",
        "state machine",
        "statechart",
        "behavior model",
        "domain-specific language",
    ],
    "1.3.2": [
        "model transformation",
        "model synchronization",
        "model co-evolution",
        "round-trip engineering",
    ],
    "1.3.3": [
        "model analysis",
        "model simulation",
        "model verification",
        "model checking",
    ],
    "1.3.4": [
        "model-based testing",
        "model based testing",
        "digital twin",
        "code generation from models",
    ],
    "1.3.5": [
        "model repository",
        "model management",
        "model quality",
        "repository mining for models",
    ],
    "1.4.1": [
        "feature model",
        "product configuration",
        "software product line",
        "variability model",
    ],
    "1.4.2": [
        "software product line",
        "core asset",
        "family architecture",
        "reuse asset",
    ],
    "1.4.3": [
        "config-aware",
        "family-based testing",
        "variability-aware",
    ],
    "1.4.4": [
        "variability evolution",
        "option interaction",
        "configurable system",
    ],
    "2.1.1": [
        "software architecture",
        "architecture reconstruction",
        "architecture recovery",
        "architecture documentation",
    ],
    "2.1.2": [
        "architecture evaluation",
        "trade-off analysis",
        "quality attribute reasoning",
        "architecture debt",
    ],
    "2.1.3": [
        "microservice migration",
        "service decomposition",
        "architecture refactoring",
        "monolith to microservice",
    ],
    "2.1.4": [
        "microservice architecture",
        "service-oriented architecture",
        "serverless",
        "platform engineering",
    ],
    "2.1.5": [
        "architecture decision",
        "architecture rationale",
        "adr",
        "architectural decision record",
    ],
    "2.2.1": [
        "design pattern",
        "anti-pattern",
        "design heuristic",
    ],
    "2.2.2": [
        "modularity",
        "coupling",
        "cohesion",
        "dependency structure",
        "decoupling",
    ],
    "2.2.3": [
        "api design",
        "api usability",
        "api versioning",
        "protocol evolution",
        "interface design",
    ],
    "2.2.4": [
        "design smell",
        "design debt",
        "maintainability",
    ],
    "2.3.1": [
        "code generator",
        "low-code",
        "low code",
        "language workbench",
        "scaffolding",
    ],
    "2.3.2": [
        "build system",
        "toolchain",
        "ide",
        "workspace automation",
    ],
    "2.3.3": [
        "component assembly",
        "package engineering",
        "integration pipeline",
    ],
    "2.3.4": [
        "pair programming",
        "review assistant",
        "ide assistant",
        "coding assistant",
    ],
    "3.1.1": [
        "test generation",
        "test amplification",
        "oracle generation",
        "automated testing",
    ],
    "3.1.2": [
        "regression testing",
        "test prioritization",
        "test selection",
        "test impact analysis",
    ],
    "3.1.3": [
        "fuzzing",
        "fuzzer",
        "fuzz test",
        "differential fuzzing",
        "differential testing",
        "search-based testing",
        "mutation testing",
        "metamorphic testing",
        "property-based testing",
    ],
    "3.1.4": [
        "gui testing",
        "web testing",
        "mobile testing",
        "cps testing",
        "ai system testing",
    ],
    "3.1.5": [
        "flaky test",
        "test debt",
        "test smell",
        "test suite maintenance",
    ],
    "3.2.1": [
        "static analysis",
        "abstract interpretation",
        "dataflow analysis",
        "taint analysis",
        "symbolic execution",
        "pointer analysis",
        "alias analysis",
        "bytecode analysis",
    ],
    "3.2.2": [
        "dynamic analysis",
        "trace analysis",
        "instrumentation",
        "hybrid analysis",
    ],
    "3.2.3": [
        "vulnerability analysis",
        "reliability analysis",
        "compliance analysis",
        "security analysis",
    ],
    "3.2.4": [
        "analysis-guided refactoring",
        "analysis-guided repair",
        "analysis-guided synthesis",
    ],
    "3.3.1": [
        "software verification",
        "formal verification",
        "model checking",
        "theorem proving",
        "smt-based verification",
        "bounded model checking",
        "deductive verification",
    ],
    "3.3.2": [
        "runtime verification",
        "runtime monitoring",
        "online checking",
        "monitor synthesis",
    ],
    "3.3.3": [
        "compliance verification",
        "certification evidence",
        "safety assurance",
        "assurance evidence",
    ],
    "3.3.4": [
        "tool competition",
        "verification benchmark",
        "reproducibility",
        "benchmark suite",
    ],
    "3.4.1": [
        "bug triage",
        "root cause analysis",
        "debugging",
        "fault diagnosis",
    ],
    "3.4.2": [
        "fault localization",
        "program repair",
        "automatic program repair",
        "patch generation",
        "bug fixing",
    ],
    "3.4.3": [
        "patch validation",
        "repair assessment",
        "regression prevention",
        "patch correctness",
    ],
    "3.4.4": [
        "rollback",
        "self-healing",
        "error recovery",
        "recovery strategy",
    ],
    "4.1.1": [
        "maintenance",
        "bug fixing",
        "hotfix",
        "backport",
    ],
    "4.1.2": [
        "refactoring",
        "remodularization",
        "code cleanup",
        "code restructuring",
    ],
    "4.1.3": [
        "api evolution",
        "dependency upgrade",
        "library migration",
        "version compatibility",
    ],
    "4.1.4": [
        "legacy modernization",
        "cloud migration",
        "language migration",
        "legacy system",
    ],
    "4.1.5": [
        "technical debt",
        "code clone",
        "clone management",
        "maintainability governance",
    ],
    "4.2.1": [
        "code search",
        "code navigation",
        "code summarization",
        "binary code summarization",
        "method name",
        "program summarization",
    ],
    "4.2.2": [
        "trace recovery",
        "documentation mining",
        "knowledge graph",
        "documentation recovery",
    ],
    "4.2.3": [
        "system reconstruction",
        "dependency recovery",
        "architecture recovery",
        "repository reconstruction",
    ],
    "4.2.4": [
        "clone detection",
        "similarity search",
        "program comprehension",
        "comprehension aid",
    ],
    "4.2.5": [
        "documentation engineering",
        "comment evolution",
        "design rationale",
        "rationale recovery",
        "explanation generation",
    ],
    "4.3.1": [
        "configuration management",
        "version management",
        "build reproducibility",
        "build engineering",
    ],
    "4.3.2": [
        "ci/cd",
        "continuous integration",
        "continuous delivery",
        "release engineering",
        "rollback pipeline",
    ],
    "4.3.3": [
        "infrastructure as code",
        "iac",
        "pipeline engineering",
        "devops automation",
    ],
    "4.3.4": [
        "package management",
        "dependency governance",
        "software supply chain",
        "package ecosystem",
        "sbom",
    ],
    "4.4.1": [
        "observability",
        "log analytics",
        "telemetry",
        "anomaly detection",
    ],
    "4.4.2": [
        "incident response",
        "incident diagnosis",
        "sre diagnosis",
        "root cause analysis",
        "service recovery",
    ],
    "4.4.3": [
        "autoscaling",
        "runtime reconfiguration",
        "adaptive operation",
    ],
    "4.4.4": [
        "runtime governance",
        "policy enforcement",
        "continuous assurance",
    ],
    "5.1.1": [
        "fault prediction",
        "failure analysis",
        "incident mining",
    ],
    "5.1.2": [
        "fault tolerance",
        "resilience engineering",
        "graceful degradation",
    ],
    "5.1.3": [
        "release reliability",
        "availability analysis",
        "slo engineering",
        "service availability",
    ],
    "5.1.4": [
        "recoverability",
        "business continuity",
        "disaster response",
    ],
    "5.1.5": [
        "functional safety",
        "hazard analysis",
        "safety case",
        "safety assurance",
    ],
    "5.2.1": [
        "secure sdlc",
        "vulnerability management",
        "security patch",
        "secure development",
        "vulnerability",
    ],
    "5.2.2": [
        "privacy engineering",
        "privacy compliance",
        "privacy requirement",
        "data governance",
    ],
    "5.2.3": [
        "sbom",
        "provenance",
        "dependency trust",
        "supply chain security",
    ],
    "5.2.4": [
        "fairness",
        "accountability",
        "regulatory compliance",
        "ai audit",
    ],
    "5.3.1": [
        "performance diagnosis",
        "performance engineering",
        "benchmarking",
        "profiling",
    ],
    "5.3.2": [
        "capacity planning",
        "cost optimization",
        "resource scheduling",
    ],
    "5.3.3": [
        "energy-aware",
        "carbon-aware",
        "green software",
    ],
    "5.3.4": [
        "scalability",
        "latency",
        "throughput",
        "performance regression",
    ],
    "5.4.1": [
        "developer experience",
        "developer ux",
        "api usability",
        "tool usability",
    ],
    "5.4.2": [
        "accessibility",
        "inclusive ui",
        "ux quality",
    ],
    "5.4.3": [
        "usability study",
        "human-centered evaluation",
        "user study",
    ],
    "5.4.4": [
        "inclusive practice",
        "developer accommodation",
        "neurodiversity",
        "diversity support",
    ],
    "6.1.1": [
        "agile",
        "lean development",
        "devops",
        "continuous improvement",
    ],
    "6.1.2": [
        "process mining",
        "conformance checking",
        "process improvement",
    ],
    "6.1.3": [
        "process traceability",
        "auditability",
        "process governance",
    ],
    "6.1.4": [
        "coordination mechanism",
        "workflow design",
        "handoff",
        "socio-technical coordination",
    ],
    "6.2.1": [
        "effort estimation",
        "project planning",
        "scheduling",
        "cost estimation",
    ],
    "6.2.2": [
        "risk management",
        "prioritization",
        "value-driven",
    ],
    "6.2.3": [
        "roi",
        "productivity analysis",
        "cost modeling",
    ],
    "6.2.4": [
        "portfolio management",
        "decision support",
        "governance analytics",
    ],
    "6.3.1": [
        "case study",
        "controlled experiment",
        "survey",
        "empirical study",
    ],
    "6.3.2": [
        "mixed methods",
        "qualitative coding",
        "human study",
        "interview study",
    ],
    "6.3.3": [
        "systematic literature review",
        "systematic mapping study",
        "meta-analysis",
        "slr",
        "sms",
    ],
    "6.3.4": [
        "replication package",
        "benchmarking",
        "open science",
        "artifact package",
        "reproducibility package",
        "dataset",
        "benchmark dataset",
        "corpus",
    ],
    "6.3.5": [
        "research roadmap",
        "roadmap",
        "research agenda",
        "retrospective",
        "reflection on",
        "vision and roadmap",
    ],
    "6.4.1": [
        "repository mining",
        "commit mining",
        "issue mining",
        "pull request",
        "github",
    ],
    "6.4.2": [
        "code review analytics",
        "ci mining",
        "team analytics",
        "review comment",
    ],
    "6.4.3": [
        "defect prediction",
        "risk modeling",
        "software metrics",
    ],
    "6.4.4": [
        "oss evolution",
        "ecosystem analysis",
        "dependency analytics",
        "registry",
    ],
    "6.5.1": [
        "developer productivity",
        "developer wellbeing",
        "developer cognition",
        "stress",
        "fatigue",
    ],
    "6.5.2": [
        "knowledge sharing",
        "collaboration",
        "code review",
        "team communication",
    ],
    "6.5.3": [
        "community health",
        "oss governance",
        "open source governance",
        "diversity",
    ],
    "6.5.4": [
        "software engineering education",
        "training",
        "curriculum",
        "onboarding",
        "novice",
    ],
    "7.1.1": [
        "code generation",
        "code completion",
        "code transformation",
        "copilot",
        "llm for code",
    ],
    "7.1.2": [
        "ai-based testing",
        "bug detection",
        "apr",
        "ai-based repair",
        "llm-assisted testing",
        "llm-assisted analysis",
        "llm-based program repair",
        "llm-guided fuzzing",
    ],
    "7.1.3": [
        "requirements summarization",
        "model completion",
        "doc generation",
        "trace generation",
    ],
    "7.1.4": [
        "architecture assistance",
        "design assistance",
        "engineering decision support",
        "planning support",
    ],
    "7.1.5": [
        "ai coding assistant",
        "human-ai workflow",
        "trust calibration",
        "pairing with llm",
        "user perception on ai coding assistants",
    ],
    "7.2.1": [
        "data pipeline",
        "feature pipeline",
        "model lifecycle",
        "model pipeline",
    ],
    "7.2.2": [
        "requirements for ai systems",
        "model card",
        "system modeling for ai",
    ],
    "7.2.3": [
        "ai testing",
        "robustness assurance",
        "drift monitoring",
        "ml verification",
    ],
    "7.2.4": [
        "mlops",
        "model deployment",
        "deployment pipeline",
        "model rollback",
    ],
    "7.2.5": [
        "ai governance",
        "ai safety case",
        "regulatory assurance",
        "responsible ai",
    ],
    "7.3.1": [
        "mape-k",
        "feedback loop",
        "adaptive planning",
        "self-adaptive system",
    ],
    "7.3.2": [
        "agent orchestration",
        "multi-agent workflow",
        "agent debugging",
    ],
    "7.3.3": [
        "self-healing",
        "self-optimization",
        "autonomic operation",
    ],
    "7.3.4": [
        "adaptive assurance",
        "runtime assurance",
        "policy safety",
    ],
    "8.1.1": [
        "industrial control",
        "automotive software",
        "avionics",
        "medical device software",
    ],
    "8.1.2": [
        "robot software",
        "autonomous robotics",
        "ros",
    ],
    "8.1.3": [
        "iot software",
        "edge platform",
        "digital twin engineering",
    ],
    "8.1.4": [
        "iso 26262",
        "do-178c",
        "certification-oriented assurance",
    ],
    "8.2.1": [
        "web application",
        "mobile app",
        "gui engineering",
        "web engineering",
    ],
    "8.2.2": [
        "cloud-native",
        "serverless",
        "platform engineering",
    ],
    "8.2.3": [
        "service composition",
        "api ecosystem",
        "service governance",
        "web service",
    ],
    "8.2.4": [
        "sre at scale",
        "distributed application operations",
        "large-scale distributed application",
    ],
    "8.3.1": [
        "mission critical",
        "safety critical",
        "formal assurance",
    ],
    "8.3.2": [
        "enterprise system",
        "business-critical",
    ],
    "8.3.3": [
        "system-of-systems",
        "interoperability",
        "integration assurance",
    ],
    "8.3.4": [
        "regulated domain",
        "compliance engineering",
        "auditability",
    ],
    "8.4.1": [
        "open source ecosystem",
        "community evolution",
        "dependency commons",
    ],
    "8.4.2": [
        "package registry",
        "platform governance",
        "supply chain ecosystem",
    ],
    "8.4.3": [
        "citizen development",
        "crowd engineering",
        "low-code engineering",
    ],
    "8.4.4": [
        "software policy",
        "ecosystem governance",
        "ethical engineering",
    ],
    "8.5.1": [
        "ai-enabled system",
        "ai-native software",
        "copilot-enabled product",
    ],
    "8.5.2": [
        "quantum program",
        "quantum software",
        "quantum testing",
    ],
    "8.5.3": [
        "llm-native",
        "agentic workflow",
        "tool-using system",
    ],
    "8.5.4": [
        "heterogeneous platform",
        "gpu",
        "edge platform",
        "classical-quantum",
    ],
    "8.5.5": [
        "scientific software",
        "hpc",
        "high-performance computing",
        "data-intensive software",
    ],
}


TAG_PREFIX_BOOSTS: Dict[str, List[str]] = {
    "需求工程": ["1.1.", "1.2.", "1.4."],
    "建模/模型驱动": ["1.3.", "1.4.", "2.1.", "8.1."],
    "测试与验证": ["3.1.", "3.3.", "5.1."],
    "形式化方法": ["1.2.", "3.3.", "3.2.", "8.3."],
    "程序分析": ["3.2.", "4.2."],
    "程序修复": ["3.4.", "4.1."],
    "维护与演化": ["4.1.", "4.2.", "4.3.", "6.4."],
    "可靠性/安全": ["5.1.", "5.2.", "3.2.3", "3.3.3"],
    "经验软件工程": ["6.3.", "6.4.", "6.5."],
    "LLM/AI for SE": ["7.1.", "7.2.", "7.3.", "8.5.3"],
    "运行时监测": ["3.3.2", "4.4.", "5.1."],
}


TAG_FALLBACK_PRIMARY: Dict[str, str] = {
    "需求工程": "1.1.2",
    "建模/模型驱动": "1.3.1",
    "测试与验证": "3.1.1",
    "形式化方法": "3.3.1",
    "程序分析": "3.2.1",
    "程序修复": "3.4.2",
    "维护与演化": "4.1.1",
    "可靠性/安全": "5.1.1",
    "经验软件工程": "6.3.1",
    "LLM/AI for SE": "7.1.1",
    "运行时监测": "3.3.2",
}


THEME_PREFIXES: Dict[str, List[str]] = {
    "requirements": ["1.1.", "1.2.", "1.4."],
    "modeling": ["1.3.", "1.4.", "8.1."],
    "architecture": ["2.1.", "2.2.", "8.2.3"],
    "testing": ["3.1.", "3.4."],
    "analysis": ["3.2.", "4.2."],
    "verification": ["3.3.", "1.2.", "8.3."],
    "maintenance": ["4.1.", "4.2.", "4.3."],
    "operations": ["4.4.", "5.1.", "5.3.", "8.2.4"],
    "quality": ["5.1.", "5.2.", "5.3.", "5.4."],
    "process": ["6.1.", "6.2."],
    "empirical": ["6.3.", "6.4.", "6.5."],
    "ai_for_se": ["7.1.", "7.3."],
    "se_for_ai": ["7.2.", "8.5.1", "8.5.3"],
}


THEME_PATTERNS: Dict[str, List[str]] = {
    "requirements": [
        "requirements",
        "requirement",
        "user story",
        "stakeholder",
        "traceability",
        "goal model",
        "goal-oriented",
        "ambiguity",
        "requirement debt",
        "requirement reuse",
    ],
    "modeling": [
        "state machine",
        "statechart",
        "uml",
        "sysml",
        "model-driven",
        "metamodel",
        "model transformation",
        "digital twin",
        "feature model",
    ],
    "architecture": [
        "software architecture",
        "microservice",
        "service architecture",
        "architecture decision",
        "api design",
        "modularity",
        "design pattern",
        "component-based",
    ],
    "testing": [
        "test generation",
        "testing",
        "test suite",
        "regression test",
        "fuzzing",
        "mutation testing",
        "oracle generation",
        "gui testing",
        "web testing",
    ],
    "analysis": [
        "static analysis",
        "dynamic analysis",
        "program analysis",
        "taint analysis",
        "dataflow analysis",
        "abstract interpretation",
        "trace analysis",
        "program comprehension",
        "code search",
    ],
    "verification": [
        "formal verification",
        "software verification",
        "model checking",
        "runtime verification",
        "runtime monitoring",
        "safety case",
        "assurance case",
        "compliance verification",
    ],
    "maintenance": [
        "maintenance",
        "software evolution",
        "refactoring",
        "technical debt",
        "library migration",
        "legacy system",
        "documentation",
        "code clone",
        "program repair",
        "patch generation",
    ],
    "operations": [
        "release engineering",
        "continuous integration",
        "continuous delivery",
        "ci/cd",
        "devops",
        "deployment pipeline",
        "dependency management",
        "observability",
        "incident response",
        "autoscaling",
        "runtime governance",
    ],
    "quality": [
        "reliability engineering",
        "fault tolerance",
        "resilience",
        "vulnerability management",
        "privacy engineering",
        "performance engineering",
        "usability study",
        "developer experience",
        "functional safety",
        "hazard analysis",
    ],
    "process": [
        "agile",
        "lean development",
        "process mining",
        "workflow",
        "effort estimation",
        "risk management",
        "project planning",
        "coordination",
    ],
    "empirical": [
        "empirical software engineering",
        "repository mining",
        "mining software repositories",
        "pull request",
        "code review",
        "case study",
        "survey",
        "controlled experiment",
        "developer productivity",
        "onboarding",
        "software engineering education",
        "benchmarking",
        "open science",
    ],
    "ai_for_se": [
        "large language model",
        "llm",
        "ai coding assistant",
        "copilot",
        "code generation",
        "code completion",
        "ai-based testing",
        "human-ai workflow",
    ],
    "se_for_ai": [
        "ai system",
        "machine learning system",
        "model lifecycle",
        "model card",
        "mlops",
        "drift monitoring",
        "robustness assurance",
        "ai governance",
        "model deployment",
    ],
}


ARTIFACT_GROUPS: Dict[str, List[str]] = {
    "requirements": [
        "requirements",
        "requirement",
        "user story",
        "stakeholder",
        "traceability",
    ],
    "models": [
        "state machine",
        "statechart",
        "model",
        "uml",
        "sysml",
        "metamodel",
    ],
    "architecture_design": [
        "architecture",
        "component",
        "api",
        "interface",
        "microservice",
        "design pattern",
    ],
    "code_tests": [
        "codebase",
        "repository",
        "test suite",
        "test case",
        "source code",
        "binary code",
        "bytecode",
        "smart contract",
        "compilation error",
        "code summarization",
        "comment generation",
        "method name",
        "bug",
        "patch",
        "commit",
        "pull request",
        "issue",
    ],
    "runtime_process": [
        "ci/cd",
        "pipeline",
        "deployment",
        "configuration",
        "log",
        "incident",
        "developer",
        "team",
        "workflow",
    ],
    "ai_system": [
        "model card",
        "dataset pipeline",
        "model deployment",
        "mlops",
        "drift",
    ],
}


METHOD_GROUPS: Dict[str, List[str]] = {
    "requirements": ["elicitation", "prioritization", "goal modeling", "traceability"],
    "modeling": ["model-driven", "model transformation", "simulation"],
    "testing": ["testing", "fuzzing", "mutation testing", "oracle generation"],
    "analysis": ["static analysis", "dynamic analysis", "trace analysis"],
    "verification": ["model checking", "formal verification", "runtime verification", "theorem proving"],
    "repair": ["debugging", "fault localization", "repair", "patch generation", "refactoring"],
    "empirical": ["case study", "survey", "experiment", "repository mining", "code review analytics"],
    "ops": ["devops", "deployment", "observability", "autoscaling", "incident response"],
    "ai": ["llm", "large language model", "mlops", "agent orchestration"],
}


EVALUATION_PATTERNS = [
    "experiment",
    "empirical",
    "case study",
    "survey",
    "benchmark",
    "dataset",
    "repository",
    "open-source",
    "open source",
    "evaluate",
    "evaluation",
    "participants",
    "industrial",
    "real-world",
    "real world",
]


NON_SE_PL_PATTERNS = [
    "compiler",
    "compilation",
    "type system",
    "type inference",
    "programming language",
    "operational semantics",
    "denotational semantics",
    "lambda calculus",
    "session type",
    "effect system",
    "proof assistant",
    "certified compiler",
    "register allocation",
    "parser",
    "partial evaluation",
    "e-graph",
    "kleene algebra",
    "constraint programming",
    "probabilistic programming",
    "ownership",
    "borrow",
]


NON_SE_SYSTEM_PATTERNS = [
    "operating system",
    "kernel",
    "filesystem",
    "storage system",
    "cache",
    "throughput",
    "latency",
    "packet-switched",
    "network switch",
    "distributed system",
    "virtualization",
    "memory reclamation",
    "lock-free",
    "gpu",
    "qpu",
    "accelerator",
    "processor",
    "middleware",
    "garbage collection",
    "quantum circuit",
    "cryptographic",
    "homomorphic encryption",
    "data structure",
    "model serving",
    "llm serving",
    "inference",
    "quantization",
    "parallelism",
    "hypervisor",
    "serverless",
    "dbms",
]


NON_SE_OTHER_PATTERNS = [
    "hardware",
    "circuit",
    "electrical",
    "control theory",
    "numerical program",
    "floating-point",
    "cryptography",
]


SPECIAL_NON_SE_OVERRIDES = [
    "compiler optimization",
    "type inference",
    "type system",
    "programming language semantics",
    "operating systems principle",
    "constraint programming",
]


@dataclass(frozen=True)
class VenuePrior:
    abbr: str
    rank: str
    kind: str
    subject: str
    se_level: str
    typical_paths: Tuple[str, ...]


@dataclass(frozen=True)
class LeafDef:
    code: str
    label: str
    keywords: Tuple[str, ...]


@dataclass(frozen=True)
class ManualOverrideIndex:
    by_key: Dict[str, Dict[str, Any]]
    by_doi: Dict[str, Dict[str, Any]]
    by_title: Dict[str, Dict[str, Any]]
    entry_count: int


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def keyword_regex(keyword: str) -> re.Pattern[str]:
    escaped = re.escape(normalize_text(keyword))
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")


_KEYWORD_RE_CACHE: Dict[str, re.Pattern[str]] = {}


def has_keyword(text: str, keyword: str) -> bool:
    keyword = normalize_text(keyword)
    if not keyword:
        return False
    pattern = _KEYWORD_RE_CACHE.get(keyword)
    if pattern is None:
        pattern = keyword_regex(keyword)
        _KEYWORD_RE_CACHE[keyword] = pattern
    return bool(pattern.search(text))


def count_hits(text: str, keywords: Iterable[str]) -> Tuple[int, List[str]]:
    hits: List[str] = []
    for keyword in keywords:
        if has_keyword(text, keyword):
            hits.append(keyword)
    return len(hits), hits


def score_keywords(title_text: str, body_text: str, keywords: Iterable[str]) -> Tuple[int, List[str]]:
    score = 0
    hits: List[str] = []
    for keyword in keywords:
        keyword = normalize_text(keyword)
        if not keyword:
            continue
        in_title = has_keyword(title_text, keyword)
        in_body = in_title or has_keyword(body_text, keyword)
        if in_title:
            score += 3
            hits.append(keyword)
        elif in_body:
            score += 1
            hits.append(keyword)
    deduped: List[str] = []
    for hit in hits:
        if hit not in deduped:
            deduped.append(hit)
    return score, deduped


def parse_leaf_defs() -> Dict[str, LeafDef]:
    text = TREE_MD.read_text(encoding="utf-8")
    block = text.split("```text", 1)[1].split("```", 1)[0]
    leaf_defs: Dict[str, LeafDef] = {}
    for line in block.splitlines():
        match = re.search(r"(\d+\.\d+\.\d+)\s+([^（(]+)[（(]([^）)]*)[）)]", line)
        if not match:
            continue
        code, label, example_text = match.groups()
        if code in leaf_defs:
            continue
        parsed_keywords: List[str] = []
        for part in re.split(r"[、，,;/]", example_text):
            part = normalize_text(part)
            if re.search(r"[a-z]", part) and len(part) >= 3 and part not in GENERIC_TREE_KEYWORDS:
                parsed_keywords.append(part)
        keywords: List[str] = list(parsed_keywords)
        keywords.extend(MANUAL_LEAF_KEYWORDS.get(code, []))
        deduped: List[str] = []
        for keyword in keywords:
            keyword = normalize_text(keyword)
            if keyword and keyword not in deduped:
                deduped.append(keyword)
        leaf_defs[code] = LeafDef(code=code, label=label.strip(), keywords=tuple(deduped))
    return leaf_defs


def parse_typical_paths(cell: str) -> Tuple[str, ...]:
    matches = re.findall(r"\d+\.(?:x|\d+)\.(?:x|\d+)", cell)
    deduped: List[str] = []
    for item in matches:
        if item not in deduped:
            deduped.append(item)
    return tuple(deduped)


def manual_override_path(target_dir: Path) -> Path:
    return target_dir / MANUAL_REVIEW_DIRNAME / MANUAL_OVERRIDE_FILENAME


def manual_override_candidate_paths(target_dir: Path) -> List[Path]:
    candidates: List[Path] = []
    batch_dir = target_dir / MANUAL_REVIEW_DIRNAME / MANUAL_BATCH_DIRNAME
    if batch_dir.exists():
        candidates.extend(sorted(path for path in batch_dir.rglob("*.json") if path.is_file()))

    root_override = manual_override_path(target_dir)
    if root_override.exists():
        candidates.append(root_override)

    return candidates


def load_manual_override_index(target_dir: Path) -> ManualOverrideIndex:
    paths = manual_override_candidate_paths(target_dir)
    if not paths:
        return ManualOverrideIndex(by_key={}, by_doi={}, by_title={}, entry_count=0)

    by_key: Dict[str, Dict[str, Any]] = {}
    by_doi: Dict[str, Dict[str, Any]] = {}
    by_title: Dict[str, Dict[str, Any]] = {}
    unique_entries: Set[str] = set()

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries = payload.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            paper_key = str(entry.get("paper_key") or "").strip()
            doi = normalize_text(str(entry.get("doi") or ""))
            title = normalize_text(str(entry.get("title") or ""))
            if paper_key:
                by_key[paper_key] = entry
            if doi:
                by_doi[doi] = entry
            if title:
                by_title[title] = entry
            unique_marker = paper_key or doi or title
            if unique_marker:
                unique_entries.add(unique_marker)

    return ManualOverrideIndex(
        by_key=by_key,
        by_doi=by_doi,
        by_title=by_title,
        entry_count=len(unique_entries),
    )


def find_manual_override(
    paper: Dict[str, Any], override_index: ManualOverrideIndex
) -> Optional[Dict[str, Any]]:
    paper_key = str(paper.get("key") or "").strip()
    if paper_key and paper_key in override_index.by_key:
        return override_index.by_key[paper_key]

    doi = normalize_text(str(paper.get("doi") or ""))
    if doi and doi in override_index.by_doi:
        return override_index.by_doi[doi]

    title = normalize_text(str(paper.get("title") or ""))
    if title and title in override_index.by_title:
        return override_index.by_title[title]

    return None


def normalize_secondary_paths(value: Any) -> List[str]:
    if isinstance(value, list):
        raw_items = value
    elif isinstance(value, str):
        raw_items = re.split(r"[;；]", value)
    elif value is None:
        raw_items = []
    else:
        raw_items = [value]

    normalized: List[str] = []
    for item in raw_items:
        text = str(item).strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def parse_venue_priors() -> Dict[Tuple[str, str, str], VenuePrior]:
    text = CCF_MD.read_text(encoding="utf-8")
    priors: Dict[Tuple[str, str, str], VenuePrior] = {}
    rank = ""
    kind = ""
    for line in text.splitlines():
        match = re.match(r"##\s+\d+\.\s+([ABC])\s+类(会议|期刊)", line)
        if match:
            rank, kind = match.groups()
            continue
        if not line.startswith("| `") or rank == "" or kind == "":
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 7:
            continue
        abbr = parts[0].strip("`")
        subject = parts[2]
        se_level = parts[3].strip("`")
        typical_paths = parse_typical_paths(parts[5])
        priors[(abbr, rank, kind)] = VenuePrior(
            abbr=abbr,
            rank=rank,
            kind=kind,
            subject=subject,
            se_level=se_level,
            typical_paths=typical_paths,
        )
    return priors


def path_matches_prefix(code: str, prefix: str) -> bool:
    code_parts = code.split(".")
    prefix_parts = prefix.split(".")
    if len(prefix_parts) != 3:
        return False
    for code_part, prefix_part in zip(code_parts, prefix_parts):
        if prefix_part == "x":
            continue
        if code_part != prefix_part:
            return False
    return True


def subject_to_macro(subject: str) -> str:
    if subject == "软件工程":
        return "软件工程"
    if subject == "系统软件":
        return "系统软件"
    if subject == "程序设计语言与形式化基础":
        return "程序设计语言与形式化基础"
    return "跨域/待判定"


def top_theme(theme_scores: Dict[str, int]) -> str:
    if not theme_scores:
        return ""
    return sorted(theme_scores.items(), key=lambda item: (-item[1], item[0]))[0][0]


def first_matching_default(tags: List[str], leaf_defs: Dict[str, LeafDef]) -> str:
    for tag in tags:
        path = TAG_FALLBACK_PRIMARY.get(tag)
        if path and path in leaf_defs:
            return path
    return ""


def choose_primary_path(
    paper: Dict[str, Any],
    prior: VenuePrior,
    leaf_defs: Dict[str, LeafDef],
    title_text: str,
    body_text: str,
    theme_scores: Dict[str, int],
) -> Tuple[str, List[str]]:
    tags = [str(tag) for tag in paper.get("tags", [])]
    leaf_scores: Dict[str, int] = {}
    direct_scores: Dict[str, int] = {}
    direct_hit_counts: Dict[str, int] = {}
    tag_boosts: Dict[str, int] = {}
    prior_boosts: Dict[str, int] = {}
    theme_boosts: Dict[str, int] = {}
    for code, leaf in leaf_defs.items():
        score, hits = score_keywords(title_text, body_text, leaf.keywords)
        direct_scores[code] = score
        direct_hit_counts[code] = len(hits)
        if score:
            leaf_scores[code] = score

    for tag in tags:
        for prefix in TAG_PREFIX_BOOSTS.get(tag, []):
            for code in leaf_defs:
                if path_matches_prefix(code, prefix):
                    tag_boosts[code] = tag_boosts.get(code, 0) + 1
                    leaf_scores[code] = leaf_scores.get(code, 0) + 1

    for prefix in prior.typical_paths:
        for code in leaf_defs:
            if path_matches_prefix(code, prefix):
                boost = 2 if "x" not in prefix else 1
                prior_boosts[code] = prior_boosts.get(code, 0) + boost
                leaf_scores[code] = leaf_scores.get(code, 0) + boost

    dominant_theme = top_theme(theme_scores)
    for prefix in THEME_PREFIXES.get(dominant_theme, []):
        for code in leaf_defs:
            if path_matches_prefix(code, prefix):
                theme_boosts[code] = theme_boosts.get(code, 0) + 1
                leaf_scores[code] = leaf_scores.get(code, 0) + 1

    if dominant_theme == "ai_for_se":
        for prefix, hints in AI_FOR_SE_PREFIX_HINTS.items():
            if not any(has_keyword(body_text, hint) for hint in hints):
                continue
            for code in leaf_defs:
                if path_matches_prefix(code, prefix):
                    theme_boosts[code] = theme_boosts.get(code, 0) + 2
                    leaf_scores[code] = leaf_scores.get(code, 0) + 2

    if "6.3.4" in leaf_defs and any(has_keyword(body_text, keyword) for keyword in DATASET_LIKE_PATTERNS):
        direct_scores["6.3.4"] = direct_scores.get("6.3.4", 0) + 2
        direct_hit_counts["6.3.4"] = direct_hit_counts.get("6.3.4", 0) + 1
        leaf_scores["6.3.4"] = leaf_scores.get("6.3.4", 0) + 2

    if "6.3.5" in leaf_defs and any(has_keyword(body_text, keyword) for keyword in SYNTHESIS_LIKE_PATTERNS):
        direct_scores["6.3.5"] = direct_scores.get("6.3.5", 0) + 2
        direct_hit_counts["6.3.5"] = direct_hit_counts.get("6.3.5", 0) + 1
        leaf_scores["6.3.5"] = leaf_scores.get("6.3.5", 0) + 2

    if not leaf_scores:
        fallback = first_matching_default(tags, leaf_defs)
        if not fallback and prior.typical_paths:
            for path in prior.typical_paths:
                if "x" not in path and path in leaf_defs:
                    fallback = path
                    break
            if not fallback:
                for path in prior.typical_paths:
                    for code in sorted(leaf_defs):
                        if path_matches_prefix(code, path):
                            fallback = code
                            break
                    if fallback:
                        break
        return fallback, []

    ranked = sorted(
        leaf_scores.items(),
        key=lambda item: (
            -item[1],
            -direct_scores.get(item[0], 0),
            -theme_boosts.get(item[0], 0),
            -tag_boosts.get(item[0], 0),
            -prior_boosts.get(item[0], 0),
            -direct_hit_counts.get(item[0], 0),
            item[0],
        ),
    )
    primary = ranked[0][0]
    primary_score = ranked[0][1]
    if primary.startswith("8."):
        for alt_code, alt_score in ranked[1:]:
            if not alt_code.startswith("8.") and alt_score >= ranked[0][1] - 1:
                primary = alt_code
                break
    if dominant_theme == "ai_for_se":
        ai_ranked = [(code, score) for code, score in ranked if code.startswith("7.1.")]
        if ai_ranked and ai_ranked[0][1] >= primary_score - 1:
            primary = ai_ranked[0][0]
    if primary.startswith("6.3.") and not any(path_matches_prefix(primary, prefix) for prefix in prior.typical_paths):
        for alt_code, alt_score in ranked[1:]:
            if not alt_code.startswith("6.") and alt_score >= 2:
                primary = alt_code
                break

    secondary: List[str] = []
    for code, score in ranked:
        if code == primary or score <= 0:
            continue
        display = f"{code} {leaf_defs[code].label}"
        if display not in secondary:
            secondary.append(display)
        if len(secondary) >= 3:
            break

    return primary, secondary


def apply_manual_override(
    paper: Dict[str, Any],
    override: Dict[str, Any],
    leaf_defs: Dict[str, LeafDef],
) -> Dict[str, Any]:
    updated = dict(paper)
    override_fields = [
        "macro_area",
        "se_inclusion_decision",
        "cross_domain_flag",
        "se_primary_path",
        "se_primary_label",
        "se_decision_basis",
    ]
    for field in override_fields:
        if field in override:
            updated[field] = override[field]

    if "se_secondary_paths" in override:
        updated["se_secondary_paths"] = normalize_secondary_paths(override.get("se_secondary_paths"))
    else:
        updated["se_secondary_paths"] = normalize_secondary_paths(updated.get("se_secondary_paths"))

    primary_path = str(updated.get("se_primary_path") or "").strip()
    decision = str(updated.get("se_inclusion_decision") or "").strip()
    if decision == "不属于软件工程":
        updated["se_primary_path"] = ""
        updated["se_primary_label"] = ""
        updated["se_secondary_paths"] = []
    elif primary_path:
        if primary_path not in leaf_defs:
            raise ValueError(f"Unknown manual review primary path: {primary_path}")
        override_label = str(override.get("se_primary_label") or "").strip()
        updated["se_primary_label"] = override_label or leaf_defs[primary_path].label
    else:
        updated["se_primary_label"] = ""

    updated["manual_review_status"] = "已人工复核"
    updated["classification_source"] = "人工复核"
    updated["manual_review_note"] = str(override.get("manual_review_note") or "")
    updated["manual_review_reviewer"] = str(override.get("manual_review_reviewer") or "")
    updated["manual_review_updated_at"] = str(override.get("manual_review_updated_at") or "")
    return updated


def classify_paper(
    paper: Dict[str, Any],
    prior: VenuePrior,
    leaf_defs: Dict[str, LeafDef],
) -> Dict[str, Any]:
    title = str(paper.get("title") or "")
    abstract = str(paper.get("abstract") or "")
    summary = str(paper.get("summary") or "")
    tags = [str(tag) for tag in paper.get("tags", [])]

    title_text = normalize_text(title)
    body_text = normalize_text(" ".join([title, abstract, summary, " ".join(tags)]))

    if any(has_keyword(title_text, keyword) for keyword in EDITORIAL_LIKE_PATTERNS):
        updated = dict(paper)
        subject_macro = subject_to_macro(prior.subject)
        updated["macro_area"] = "跨域/待判定" if subject_macro == "软件工程" else subject_macro
        updated["se_inclusion_decision"] = "不属于软件工程"
        updated["cross_domain_flag"] = "是" if "交叉" in prior.subject else "否"
        updated["se_primary_path"] = ""
        updated["se_primary_label"] = ""
        updated["se_secondary_paths"] = []
        updated["se_decision_basis"] = "X1=是; D1=0; D2=0; D3=0; D4=0; genre=editorial-like"
        updated["manual_review_status"] = "未人工复核"
        updated["classification_source"] = "启发式初判"
        updated["manual_review_note"] = ""
        updated["manual_review_reviewer"] = ""
        updated["manual_review_updated_at"] = ""
        return updated

    theme_scores: Dict[str, int] = {}
    for theme, keywords in THEME_PATTERNS.items():
        score, _ = score_keywords(title_text, body_text, keywords)
        theme_scores[theme] = score

    artifact_groups = 0
    for keywords in ARTIFACT_GROUPS.values():
        hits, _ = count_hits(body_text, keywords)
        if hits > 0:
            artifact_groups += 1

    method_groups = 0
    for keywords in METHOD_GROUPS.values():
        hits, _ = count_hits(body_text, keywords)
        if hits > 0:
            method_groups += 1

    eval_hits, _ = count_hits(body_text, EVALUATION_PATTERNS)
    pl_hits, pl_keywords = count_hits(body_text, NON_SE_PL_PATTERNS)
    sys_hits, sys_keywords = count_hits(body_text, NON_SE_SYSTEM_PATTERNS)
    other_hits, other_keywords = count_hits(body_text, NON_SE_OTHER_PATTERNS)
    prior_bias = SE_LEVEL_PRIOR.get(prior.se_level, 0)

    dominant_theme = top_theme(theme_scores)
    dominant_theme_score = theme_scores.get(dominant_theme, 0)

    d1 = 0
    if dominant_theme_score >= 6:
        d1 = 3
    elif dominant_theme_score >= 3:
        d1 = 2
    elif dominant_theme_score >= 1 or prior_bias >= 2:
        d1 = 1

    d2 = 0
    if artifact_groups >= 2:
        d2 = 2
    elif artifact_groups == 1 or (d1 >= 2 and prior_bias >= 2):
        d2 = 1

    d3 = 0
    if method_groups >= 2:
        d3 = 2
    elif method_groups == 1 or any(tag in TAG_PREFIX_BOOSTS for tag in tags):
        d3 = 1

    d4 = 1 if eval_hits > 0 else 0

    non_se_score = max(pl_hits, sys_hits, other_hits)
    x1 = (
        non_se_score >= 2
        and d2 == 0
        and d1 <= 1
        and dominant_theme not in {"requirements", "maintenance", "process", "empirical", "ai_for_se", "se_for_ai"}
    )
    if any(has_keyword(body_text, override) for override in SPECIAL_NON_SE_OVERRIDES) and d2 == 0:
        x1 = True
    if prior_bias <= -2 and sys_hits >= 2 and artifact_groups == 0 and dominant_theme not in {"testing", "analysis", "verification"}:
        x1 = True

    weighted_total = d1 * 3 + d2 * 2 + d3 * 2 + d4 + max(prior_bias, 0)

    decision = "不属于软件工程"
    if d1 >= 2 and d2 >= 1 and weighted_total >= 7 and not x1:
        decision = "属于软件工程"
    elif d1 >= 2 and weighted_total >= 6:
        decision = "跨域但软工主导"
    elif prior_bias >= 2 and d1 >= 1 and d2 >= 1 and weighted_total >= 6 and not x1:
        decision = "属于软件工程"
    elif prior_bias >= 3 and d1 >= 1 and d3 >= 1 and not x1:
        decision = "属于软件工程"
    elif prior_bias <= -2 and non_se_score >= 1:
        decision = "不属于软件工程"

    cross_domain = (
        "交叉" in prior.subject
        or (decision != "不属于软件工程" and non_se_score >= 1)
        or (decision == "跨域但软工主导")
        or (prior.se_level == "部分属于软工" and decision != "不属于软件工程")
    )

    if decision != "不属于软件工程":
        macro_area = "软件工程"
    else:
        if sys_hits > max(pl_hits, other_hits):
            macro_area = "系统软件"
        elif pl_hits > 0 or "程序设计语言" in prior.subject or "形式化" in prior.subject:
            macro_area = "程序设计语言与形式化基础"
        else:
            subject_macro = subject_to_macro(prior.subject)
            macro_area = "跨域/待判定" if subject_macro == "软件工程" else subject_macro

    primary_path = ""
    primary_label = ""
    secondary_paths: List[str] = []
    if decision != "不属于软件工程":
        primary_path, secondary_paths = choose_primary_path(paper, prior, leaf_defs, title_text, body_text, theme_scores)
        if primary_path:
            primary_label = leaf_defs[primary_path].label
        else:
            decision = "待判定"
            macro_area = "跨域/待判定"

    basis_parts = [
        f"X1={'是' if x1 else '否'}",
        f"D1={d1}",
        f"D2={d2}",
        f"D3={d3}",
        f"D4={d4}",
        f"venue={prior.se_level}",
    ]
    if cross_domain:
        basis_parts.append("cross=是")
    if pl_keywords and macro_area != "软件工程":
        basis_parts.append("PL=" + ",".join(pl_keywords[:2]))
    if sys_keywords and macro_area != "软件工程":
        basis_parts.append("SYS=" + ",".join(sys_keywords[:2]))
    if other_keywords and macro_area != "软件工程":
        basis_parts.append("OTHER=" + ",".join(other_keywords[:2]))

    updated = dict(paper)
    updated["macro_area"] = macro_area
    updated["se_inclusion_decision"] = decision
    updated["cross_domain_flag"] = "是" if cross_domain else "否"
    updated["se_primary_path"] = primary_path
    updated["se_primary_label"] = primary_label
    updated["se_secondary_paths"] = secondary_paths
    updated["se_decision_basis"] = "; ".join(basis_parts)
    updated["manual_review_status"] = "未人工复核"
    updated["classification_source"] = "启发式初判"
    updated["manual_review_note"] = ""
    updated["manual_review_reviewer"] = ""
    updated["manual_review_updated_at"] = ""
    return updated


def render_year_readme(
    year: int,
    payloads: List[Dict[str, Any]],
    verification: Dict[str, Any],
    full_manual_coverage: bool,
) -> str:
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    priors = parse_venue_priors()
    venue_count = len(payloads)
    total_papers = verification["total_actual"]
    abbr_counts = Counter(payload["venue"].abbr for payload in payloads)

    rank_kind_counts: Counter[Tuple[str, str]] = Counter()
    for payload in payloads:
        rank_kind_counts[(payload["venue"].rank, payload["venue"].kind)] += payload["actual_total"]

    macro_counts = Counter(
        paper.get("macro_area", "待补") for payload in payloads for paper in payload["papers"]
    )
    se_counts = Counter(
        paper.get("se_inclusion_decision", "待补") for payload in payloads for paper in payload["papers"]
    )
    review_counts = Counter(
        paper.get("manual_review_status", "未人工复核") for payload in payloads for paper in payload["papers"]
    )
    source_counts = Counter(
        paper.get("classification_source", "启发式初判") for payload in payloads for paper in payload["papers"]
    )
    path_counts = Counter(
        f"{paper['se_primary_path']} {paper['se_primary_label']}".strip()
        for payload in payloads
        for paper in payload["papers"]
        if paper.get("se_primary_path")
    )
    phd_venue_grade_counts: Counter[str] = Counter()
    phd_paper_grade_counts: Counter[str] = Counter()
    for payload in payloads:
        phd_fit = get_phd_venue_fit(payload["venue"])
        phd_venue_grade_counts[phd_fit.grade] += 1
        phd_paper_grade_counts[phd_fit.grade] += payload["actual_total"]

    lines: List[str] = []
    lines.append(f"# `{year}` 年度汇总")
    lines.append("")
    lines.append("## 1. 年份说明")
    lines.append("")
    lines.append(f"- 年份：`{year}`")
    lines.append("- 覆盖范围：`CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议")
    lines.append(f"- 当前覆盖的 venue 数量：`{venue_count}`")
    lines.append(f"- 当前已入表论文数量：`{total_papers}`")
    lines.append(f"- 更新时间：`{ts}`")
    lines.append(
        f"- 人工复核覆盖文件：[manual_review/README.md]({MANUAL_REVIEW_DIRNAME}/README.md) / "
        f"[manual_review/{MANUAL_OVERRIDE_FILENAME}]({MANUAL_REVIEW_DIRNAME}/{MANUAL_OVERRIDE_FILENAME}) / "
        f"[manual_review/{MANUAL_BATCH_DIRNAME}/]({MANUAL_REVIEW_DIRNAME}/{MANUAL_BATCH_DIRNAME})"
    )
    if full_manual_coverage:
        lines.append("- 说明：本年度条目已实现全量人工复核；本页由 `tools/ccf_se_index_builder.py` 提供基础元数据，再由 `tools/ccf_se_classifier.py` 直接读取 `manual_review/overrides.json` 与 `manual_review/batches/*.json` 中的人工终判结果进行回填与渲染，不再依赖启发式分类结果。")
    else:
        lines.append("- 说明：本页先由 `tools/ccf_se_index_builder.py` 生成基础元数据，再由 `tools/ccf_se_classifier.py` 做启发式初判；若 `manual_review/overrides.json` 或 `manual_review/batches/*.json` 中存在逐篇人工复核结果，则人工复核优先覆盖脚本结果。")
    lines.append("")
    lines.append("## 2. 年度汇总统计")
    lines.append("")
    for rank in ["A", "B", "C"]:
        for kind in ["会议", "期刊"]:
            lines.append(f"- {rank} 类{kind}：`{rank_kind_counts.get((rank, kind), 0)}`")
    lines.append(f"- 期望总条目数：`{verification['total_expected']}`")
    lines.append(f"- 实际总条目数：`{verification['total_actual']}`")
    lines.append("- 一级总判定分布：" + " / ".join(f"{name} ({count})" for name, count in macro_counts.most_common()))
    lines.append("- 软工纳入判定分布：" + " / ".join(f"{name} ({count})" for name, count in se_counts.most_common()))
    lines.append("- 判定来源分布：" + " / ".join(f"{name} ({count})" for name, count in source_counts.most_common()))
    lines.append("- 人工复核状态分布：" + " / ".join(f"{name} ({count})" for name, count in review_counts.most_common()))
    lines.append("- 本博士研究相关性（氛围 A/B/C/D，按 venue 数）：" + format_phd_grade_summary(phd_venue_grade_counts))
    lines.append("- 本博士研究相关性（氛围 A/B/C/D，按 2025 论文数）：" + format_phd_grade_summary(phd_paper_grade_counts))
    if path_counts:
        lines.append("- 高频软工主路径：" + " / ".join(f"{name} ({count})" for name, count in path_counts.most_common(12)))
    lines.append("")
    lines.append("## 3. 覆盖 venue 列表")
    lines.append("")
    lines.append("- 本博士研究相关性口径：综合 [AGENTS.md](../../../AGENTS.md)、[TARGET.md](../../../TARGET.md)、[project_1_llm_state_machine_modeling/README.md](../../../project_1_llm_state_machine_modeling/README.md)、[open_explore/README.md](../../../open_explore/README.md)、[open_explore/uppaal_tech/README.md](../../../open_explore/uppaal_tech/README.md)、[open_explore/uppaal_apps/README.md](../../../open_explore/uppaal_apps/README.md)、开题报告 [sec_2.tex](../../../phd_proposal/phd_proposal_report/content/sec_2.tex) 与文献综述 [sec_1.tex](../../../phd_proposal/phd_proposal_literature_review/content/sec_1.tex) / [sec_3.tex](../../../phd_proposal/phd_proposal_literature_review/content/sec_3.tex) 的研究问题边界。")
    lines.append("- 分级：`A 🔥` = 高度贴题、值得长期重点跟踪；`B 🟢` = 较高相关、常能补方法链或评测链；`C 🟡` = 间接相关、只建议按子题筛选；`D ⚪` = 低相关、通常只保留极少数特例。")
    lines.append("- 口径：`venue 判定` 按 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 的 `软工归属级别` 折叠而来：`完全属于软工 / 大部分属于软工 -> 软工 venue`，`部分属于软工 -> 混合 venue`，`大部分不属于软工 / 完全不属于软工 -> 非软工 venue`。")
    lines.append("- `主体归属` 与 `典型软工路径（先验）` 来自 venue 级先验；`2025 一级总判定`、`2025 软工纳入` 与 `2025 高频软工主路径` 直接按本年度逐篇人工复核结果统计。")
    lines.append("- `典型软工路径（先验）` 与 `2025 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。")
    lines.append("")
    lines.append("| venue | 全称 | 等级 | 类型 | 论文数 | venue 判定 | 主体归属 | 博士研究相关性（氛围） | 本研究贴题点 | 典型软工路径（先验） | 2025 一级总判定 | 2025 软工纳入 | 2025 高频软工主路径 | 数据文件 | 备注 |")
    lines.append("|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|")
    for payload in payloads:
        venue = payload["venue"]
        files = payload["files"]
        display_abbr = display_abbr_for_venue(venue, abbr_counts[venue.abbr] > 1)
        prior = priors[(venue.abbr, venue.rank, venue.kind)]
        phd_fit = get_phd_venue_fit(venue)
        venue_bucket, venue_bucket_score = summarize_prior_bucket(prior.se_level)
        venue_judgement = f"{venue_bucket}（{prior.se_level}）"

        venue_macro_counts = Counter(paper.get("macro_area", "待补") for paper in payload["papers"])
        venue_se_counts = Counter(
            paper.get("se_inclusion_decision", "待补") for paper in payload["papers"]
        )
        venue_path_counts = Counter(
            f"{paper['se_primary_path']} {paper['se_primary_label']}".strip()
            for paper in payload["papers"]
            if paper.get("se_primary_path")
        )

        macro_summary = format_counter_summary(
            venue_macro_counts,
            order=MACRO_DISPLAY_ORDER,
            empty_text="无 2025 条目",
        )
        se_summary = format_counter_summary(
            venue_se_counts,
            order=SE_DECISION_DISPLAY_ORDER,
            empty_text="无 2025 条目",
        )
        path_summary = format_top_paths(
            venue_path_counts,
            limit=2,
            empty_text="无纳入软工主路径",
        )
        note = compare_prior_and_data_side(
            expected_total=payload["expected_total"],
            actual_total=payload["actual_total"],
            prior_score=venue_bucket_score,
            se_counts=venue_se_counts,
        )
        lines.append(
            "| `{abbr}` | {full} | `{rank}` | `{kind}` | {count} | {judgement} | {subject} | {phd_grade} | {phd_rationale} | {paths} | {macro} | {se} | {path_summary} | [metadata]({meta}) / [bib]({bib}) | {note} |".format(
                abbr=md_escape(display_abbr),
                full=md_escape(venue.full_name),
                rank=venue.rank,
                kind=venue.kind,
                count=payload["actual_total"],
                judgement=md_escape(venue_judgement),
                subject=md_escape(prior.subject),
                phd_grade=md_escape(format_phd_grade(phd_fit.grade)),
                phd_rationale=md_escape(phd_fit.rationale),
                paths=md_escape(" / ".join(prior.typical_paths) if prior.typical_paths else "-"),
                macro=md_escape(macro_summary),
                se=md_escape(se_summary),
                path_summary=md_escape(path_summary),
                meta=md_escape(files["metadata"]),
                bib=md_escape(files["bib"]),
                note=md_escape(note),
            )
        )
    lines.append("")
    lines.append("## 4. Venue Sections")
    lines.append("")

    for payload in payloads:
        venue = payload["venue"]
        key_pages = payload["key_pages"]
        files = payload["files"]
        phd_fit = get_phd_venue_fit(venue)
        display_abbr = display_abbr_for_venue(venue, abbr_counts[venue.abbr] > 1)
        lines.append("---")
        lines.append("")
        lines.append(f"## `{display_abbr}`")
        lines.append("")
        lines.append("### 4.1 基本信息")
        lines.append("")
        lines.append(f"- 全称：{venue.full_name}")
        lines.append(f"- `CCF` 等级：`{venue.rank}`")
        lines.append(f"- 类型：`{venue.kind}`")
        lines.append(f"- 年份：`{year}`")
        lines.append(f"- 条目数：`{payload['actual_total']}`")
        lines.append(f"- 与本博士研究相关性（氛围）：`{format_phd_grade_with_label(phd_fit.grade)}`")
        lines.append(f"- 贴题点：{phd_fit.rationale}")
        lines.append(f"- 数据文件：[metadata]({files['metadata']}) / [bib]({files['bib']})")
        lines.append("")
        lines.append("### 4.2 关键信息页面")
        lines.append("")
        if venue.kind == "期刊":
            homepage = key_pages.get("journal_homepage") or "待补"
            lines.append(f"- 期刊主页：{homepage}")
            lines.append(f"- 学术索引页：{venue.index_url}")
            lines.append("- 2025 年官方 article page：见下表 `官方落地页` 列")
        else:
            homepage = key_pages.get("homepage") or "待补"
            lines.append(f"- 年主页：{homepage}")
            lines.append(f"- 学术索引页：{venue.index_url}")
            carrier = key_pages.get("carrier_homepage")
            if carrier:
                lines.append(f"- 正式发布载体页：{carrier}")
            procs = key_pages.get("proceedings_pages") or []
            if procs:
                lines.append(f"- 官方论文集页：{' / '.join(procs[:3])}")
            if key_pages.get("note"):
                lines.append(f"- 说明：{key_pages['note']}")
            lines.append("- `CFP`：待补")
        lines.append("")
        lines.append("### 4.3 论文名录")
        lines.append("")
        lines.append("- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已写入对应 `metadata` / `bib` 文件。")
        lines.append("")
        lines.append("| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for idx, paper in enumerate(payload["papers"], start=1):
            authors = ", ".join(paper["authors"])
            doi_cell = f"[{paper['doi']}](https://doi.org/{paper['doi']})" if paper.get("doi") else ""
            official_cell = f"[link]({paper['official_url']})" if paper.get("official_url") else ""
            primary = ""
            if paper.get("se_primary_path"):
                primary = f"{paper['se_primary_path']} {paper.get('se_primary_label', '')}".strip()
            secondary = "；".join(paper.get("se_secondary_paths") or [])
            notes: List[str] = []
            if paper.get("cross_domain_flag") == "是" and paper.get("se_inclusion_decision") != "不属于软件工程":
                notes.append("跨域")
            if paper.get("manual_review_note"):
                notes.append(str(paper.get("manual_review_note")))
            note = "；".join(notes)
            lines.append(
                "| {idx} | {title} | {authors} | {summary} | {macro} | {decision} | {source} | {review} | {primary} | {secondary} | {basis} | {doi} | {official} | {screening} | {pdf} | `{bib}` | {note} |".format(
                    idx=idx,
                    title=md_escape(str(paper.get("title") or "")),
                    authors=md_escape(authors),
                    summary=md_escape(str(paper.get("summary") or "")),
                    macro=md_escape(str(paper.get("macro_area") or "")),
                    decision=md_escape(str(paper.get("se_inclusion_decision") or "")),
                    source=md_escape(str(paper.get("classification_source") or "")),
                    review=md_escape(str(paper.get("manual_review_status") or "")),
                    primary=md_escape(primary),
                    secondary=md_escape(secondary),
                    basis=md_escape(str(paper.get("se_decision_basis") or "")),
                    doi=doi_cell,
                    official=official_cell,
                    screening=md_escape(str(paper.get("initial_screening") or "")),
                    pdf=md_escape(str(paper.get("pdf_followup") or "")),
                    bib=md_escape(str(paper.get("bibtex_key") or paper.get("key") or "")),
                    note=md_escape(note),
                )
            )
        lines.append("")
        lines.append("### 4.4 本 venue 年度观察")
        lines.append("")
        if payload["papers"]:
            decision_counts = Counter(paper.get("se_inclusion_decision", "待补") for paper in payload["papers"])
            macro_counts_local = Counter(paper.get("macro_area", "待补") for paper in payload["papers"])
            review_counts_local = Counter(paper.get("manual_review_status", "未人工复核") for paper in payload["papers"])
            source_counts_local = Counter(paper.get("classification_source", "启发式初判") for paper in payload["papers"])
            top_paths_local = Counter(
                f"{paper['se_primary_path']} {paper['se_primary_label']}".strip()
                for paper in payload["papers"]
                if paper.get("se_primary_path")
            )
            top_tags = Counter(tag for paper in payload["papers"] for tag in paper.get("tags", [])).most_common(5)
            lines.append("- 一级总判定分布：" + " / ".join(f"{name} ({count})" for name, count in macro_counts_local.most_common()))
            lines.append("- 软工纳入判定分布：" + " / ".join(f"{name} ({count})" for name, count in decision_counts.most_common()))
            lines.append("- 判定来源分布：" + " / ".join(f"{name} ({count})" for name, count in source_counts_local.most_common()))
            lines.append("- 人工复核状态分布：" + " / ".join(f"{name} ({count})" for name, count in review_counts_local.most_common()))
            if top_paths_local:
                lines.append("- 高频软工主路径：" + " / ".join(f"{name} ({count})" for name, count in top_paths_local.most_common(8)))
            if top_tags:
                lines.append("- 主题标签补充：" + " / ".join(f"{name} ({count})" for name, count in top_tags))
        else:
            lines.append("- 本年度未检出直接归属该 venue 的主论文条目。")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 5. 本年度总体观察")
    lines.append("")
    lines.append("- 一级总判定分布：" + " / ".join(f"{name} ({count})" for name, count in macro_counts.most_common()))
    lines.append("- 软工纳入判定分布：" + " / ".join(f"{name} ({count})" for name, count in se_counts.most_common()))
    lines.append("- 判定来源分布：" + " / ".join(f"{name} ({count})" for name, count in source_counts.most_common()))
    lines.append("- 人工复核状态分布：" + " / ".join(f"{name} ({count})" for name, count in review_counts.most_common()))
    if path_counts:
        lines.append("- 高频软工主路径：" + " / ".join(f"{name} ({count})" for name, count in path_counts.most_common(15)))
    lines.append("- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。")
    lines.append(
        f"- 分类终判状态：以 [./{MANUAL_REVIEW_DIRNAME}/{MANUAL_OVERRIDE_FILENAME}](./{MANUAL_REVIEW_DIRNAME}/{MANUAL_OVERRIDE_FILENAME}) "
        f"与 [./{MANUAL_REVIEW_DIRNAME}/{MANUAL_BATCH_DIRNAME}/](./{MANUAL_REVIEW_DIRNAME}/{MANUAL_BATCH_DIRNAME}) 为准；"
        "未进入覆盖文件的条目仍只是启发式初判。"
    )
    lines.append("- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。")
    lines.append("")
    return "\n".join(lines)


def display_abbr_for_venue(venue: Venue, duplicated: bool) -> str:
    if not duplicated:
        return venue.abbr
    return f"{venue.abbr} / {venue.kind} / {venue.rank}"


def get_phd_venue_fit(venue: Venue) -> PhdVenueFit:
    key = (venue.abbr, venue.rank, venue.kind)
    fit = PHD_VENUE_RELEVANCE.get(key)
    if fit is None:
        raise KeyError(f"Missing PhD venue relevance for: {key}")
    return fit


def format_phd_grade(grade: str) -> str:
    return f"{grade} {PHD_GRADE_EMOJI[grade]}"


def format_phd_grade_with_label(grade: str) -> str:
    return f"{grade} {PHD_GRADE_EMOJI[grade]}（{PHD_GRADE_LABEL[grade]}）"


def format_phd_grade_summary(counter: Counter[str]) -> str:
    return " / ".join(
        f"{format_phd_grade(grade)} ({counter.get(grade, 0)})"
        for grade in PHD_GRADE_DISPLAY_ORDER
        if counter.get(grade, 0)
    )


def summarize_prior_bucket(se_level: str) -> Tuple[str, int]:
    if se_level in {"完全属于软工", "大部分属于软工"}:
        return "软工 venue", 2
    if se_level == "部分属于软工":
        return "混合 venue", 1
    return "非软工 venue", 0


def format_counter_summary(
    counter: Counter[str],
    order: Iterable[str],
    empty_text: str,
) -> str:
    order_index = {key: idx for idx, key in enumerate(order)}
    items = [
        (key, count)
        for key, count in counter.items()
        if count
    ]
    if items:
        items.sort(key=lambda item: (-item[1], order_index.get(item[0], len(order_index)), item[0]))
        return " / ".join(f"{key} {count}" for key, count in items)
    return empty_text


def format_top_paths(counter: Counter[str], limit: int, empty_text: str) -> str:
    if not counter:
        return empty_text
    return " / ".join(f"{name} ({count})" for name, count in counter.most_common(limit))


def summarize_data_side_bucket(se_counts: Counter[str], actual_total: int) -> int:
    if actual_total <= 0:
        return -1
    soft_total = se_counts.get("属于软件工程", 0) + se_counts.get("跨域但软工主导", 0)
    soft_ratio = soft_total / actual_total
    if soft_ratio >= 0.7:
        return 2
    if soft_ratio >= 0.25:
        return 1
    return 0


def compare_prior_and_data_side(
    expected_total: int,
    actual_total: int,
    prior_score: int,
    se_counts: Counter[str],
) -> str:
    count_note = "计数一致" if expected_total == actual_total else "计数需复核"
    data_side_score = summarize_data_side_bucket(se_counts, actual_total)
    if data_side_score < 0:
        return f"{count_note}；2025 无条目，暂以先验为准"
    if data_side_score == prior_score:
        return f"{count_note}；2025 与先验一致"
    if data_side_score > prior_score:
        return f"{count_note}；2025 比先验更偏软工"
    return f"{count_note}；2025 比先验更偏非软工"


def load_payloads(target_dir: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    verification_path = target_dir / "verification.json"
    verification = json.loads(verification_path.read_text(encoding="utf-8"))
    payloads: List[Dict[str, Any]] = []
    for item in verification["venues"]:
        metadata_path = target_dir / item["files"]["metadata"]
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        payloads.append(
            {
                "venue": Venue(
                    abbr=payload["venue"]["abbr"],
                    full_name=payload["venue"]["full_name"],
                    rank=payload["venue"]["rank"],
                    kind=payload["venue"]["kind"],
                    index_url=payload["venue"]["index_url"],
                ),
                "mode": payload["source"]["mode"],
                "expected_total": payload["source"]["expected_total"],
                "actual_total": len(payload["papers"]),
                "key_pages": payload["source"]["key_pages"],
                "papers": payload["papers"],
                "files": item["files"],
            }
        )
    return payloads, verification


def classify_year(target_dir: Path, year: int) -> Dict[str, int]:
    priors = parse_venue_priors()
    leaf_defs = parse_leaf_defs()
    override_index = load_manual_override_index(target_dir)
    payloads, verification = load_payloads(target_dir)

    total_manual_hits = 0
    for payload in payloads:
        for paper in payload["papers"]:
            if find_manual_override(paper, override_index) is not None:
                total_manual_hits += 1
    full_manual_coverage = total_manual_hits == verification["total_actual"]

    counters: Counter[str] = Counter()
    counters["manual_override_entries"] = total_manual_hits
    for payload in payloads:
        venue = payload["venue"]
        prior = priors[(venue.abbr, venue.rank, venue.kind)]
        metadata_path = target_dir / payload["files"]["metadata"]
        original = json.loads(metadata_path.read_text(encoding="utf-8"))
        updated_papers: List[Dict[str, Any]] = []
        for paper in original["papers"]:
            override = find_manual_override(paper, override_index)
            if full_manual_coverage:
                if override is None:
                    raise ValueError(f"Expected full manual coverage but no manual review entry found for: {paper.get('key')}")
                updated = apply_manual_override(dict(paper), override, leaf_defs)
                counters["review:已人工复核"] += 1
                counters["source:人工复核"] += 1
            else:
                updated = classify_paper(paper, prior, leaf_defs)
                if override is not None:
                    updated = apply_manual_override(updated, override, leaf_defs)
                    counters["review:已人工复核"] += 1
                    counters["source:人工复核"] += 1
                else:
                    counters["review:未人工复核"] += 1
                    counters["source:启发式初判"] += 1
            updated_papers.append(updated)
            counters["papers"] += 1
            counters[f"macro:{updated['macro_area']}"] += 1
            counters[f"decision:{updated['se_inclusion_decision']}"] += 1
            if updated["se_primary_path"]:
                counters["with_primary_path"] += 1
        original["papers"] = updated_papers
        metadata_path.write_text(json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["papers"] = updated_papers
        payload["actual_total"] = len(updated_papers)

    readme_text = render_year_readme(year, payloads, verification, full_manual_coverage)
    (target_dir / "README.md").write_text(readme_text, encoding="utf-8")
    return dict(counters)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify yearly CCF papers into SE / non-SE paths.")
    parser.add_argument("--year", type=int, required=True, help="Target year, e.g. 2025")
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to frontier_index/ccf_history/<year>/",
    )
    args = parser.parse_args()

    target_dir = args.target_dir or (ROOT / "frontier_index" / "ccf_history" / str(args.year))
    counters = classify_year(target_dir=target_dir, year=args.year)

    print(json.dumps(counters, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
