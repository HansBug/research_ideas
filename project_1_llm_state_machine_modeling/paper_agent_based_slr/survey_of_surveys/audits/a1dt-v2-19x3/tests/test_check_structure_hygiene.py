#!/usr/bin/env python3
"""A1-DT v2 evidence-consumption phrase regression tests.

These tests protect the academic evidence-chain gate in ``check_structure.py``.
They are intentionally small and local: every newly discovered bypass phrase
from PR #132 review should become a positive example here, and every permitted
negative warning should become a negative example here before the gate changes.
"""
from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

CHECK_STRUCTURE_PATH = Path(__file__).resolve().parents[1] / "check_structure.py"


def load_check_structure_module():
    spec = importlib.util.spec_from_file_location("a1dt_v2_check_structure", CHECK_STRUCTURE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load check_structure module from {CHECK_STRUCTURE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvidenceConsumptionPhraseGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = load_check_structure_module()
        cls.phrases = cls.gate.FORBIDDEN_CONSUMABLE_SOURCE_PHRASES
        cls.patterns = [re.compile(pattern) for pattern in cls.gate.FORBIDDEN_CONSUMABLE_SOURCE_PATTERNS]

    def assert_blocked(self, text: str) -> None:
        blocked_by_phrase = any(phrase in text for phrase in self.phrases)
        blocked_by_pattern = any(pattern.search(text) for pattern in self.patterns)
        self.assertTrue(blocked_by_phrase or blocked_by_pattern, msg=f"应拦截但未拦截: {text}")

    def assert_allowed(self, text: str) -> None:
        blocked_by_phrase = [phrase for phrase in self.phrases if phrase in text]
        blocked_by_pattern = [pattern.pattern for pattern in self.patterns if pattern.search(text)]
        self.assertFalse(
            blocked_by_phrase or blocked_by_pattern,
            msg=f"应放行但被拦截: {text}; phrases={blocked_by_phrase}; patterns={blocked_by_pattern}",
        )

    def test_positive_direct_consumption_phrases_are_blocked(self) -> None:
        positive_examples = [
            "可直接迁回 SUMMARY",
            "可直接引用该结论",
            "可直接复用为 A.2 证据",
            "可直接写入 review.md",
            "可直接作为 Paper2 事实源",
            "直接迁入 review.md §0 卡片",
            "直接写入 SUMMARY 总账",
            "直接作为 Paper2 单论文模式设计参考",
            "直接驱动返修",
            "直接统计进入主统计池",
            "直接使用该字段表",
            "直接用于重写 review.md",
            "直接采信该候选发现",
            "直接消费历史草案",
            "直接落地为最终发现",
            "Paper2 trace 模式 直接落点",
            "直接沉淀到 SUMMARY",
            "直接归档为事实真源",
            "直接输出到论文草稿",
            "直接抄进主树取值空间列",
            "直接填充证据账本",
            "直接可用清单",
            "直接可统计的候选发现",
            "直接可迁移到 Paper2 的方法学纪律",
            "直接可写入 review.md",
            "直接可入账",
            "直接可回填 SUMMARY",
        ]
        for example in positive_examples:
            with self.subTest(example=example):
                self.assert_blocked(example)

    def test_negative_warnings_are_allowed(self) -> None:
        negative_examples = [
            "不可直接外推为最终发现",
            "不能直接升级为 verified",
            "不得直接写成论文结论",
            "不应直接作为 Paper2 事实源",
            "禁止直接采信该历史草案",
            "严禁直接引用为既定事实",
            "未直接使用该技能文件",
            "不直接迁入 SUMMARY",
            "不能直接进入主统计池",
            "不得直接使用该候选发现",
            "禁止直接可用的误导性表述",
            "严禁直接可统计入池",
        ]
        for example in negative_examples:
            with self.subTest(example=example):
                self.assert_allowed(example)


class ReviewHistoryResidueGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = load_check_structure_module()

    def test_skill_and_rework_process_residue_are_forbidden_in_review(self) -> None:
        forbidden_examples = [
            "技能文件",
            "/.codex/skills",
            "reviewer-self-review",
            "v2 后已挂三路审计返修块",
            "返修块",
        ]
        for example in forbidden_examples:
            with self.subTest(example=example):
                self.assertIn(example, self.gate.FORBIDDEN_REVIEW_HISTORY_PHRASES)



if __name__ == "__main__":
    unittest.main()
