"""Fixed denominators and valid-known/novel/invalid arithmetic, no provider."""

import unittest

from analyze_a1 import calculate, validate


class MetricTests(unittest.TestCase):
    def test_global_report_count_cannot_hide_missing_cell_reports(self):
        items = {str(i): {"L": "L0" if i < 71 else "L1" if i < 106 else "L2"} for i in range(145)}
        cells = [{"pair_id": str(p), "round": rnd, "reports": int(p == 0 and rnd < 3)}
                 for p in range(54) for rnd in (1, 2, 3)]
        arm = {"cells": cells, "coverage": {"planned_cells": 162, "eligible_cells": 162,
               "judged_cells": 162, "planned_expected_rounds": 435, "unjudged_reports": 0},
               "reports": [{"original_report_id": str(i), "pair_id": "0", "round": 1} for i in range(2)]}
        with self.assertRaisesRegex(AssertionError, "per-cell report coverage"):
            validate({"a1": arm, "v61": arm}, items)

    def test_repeated_hit_does_not_replace_missing_issues_or_invalid_reports(self):
        items = {"e0": {"L": "L0"}, "e1": {"L": "L1"}, "e2": {"L": "L2"}}
        rows = [{"validity": "VALID_KNOWN", "round": rnd, "pair_id": "0000",
                 "full_ledger_ids": ["e0"], "partial_ledger_ids": [], "d_tier": "D1",
                 "a0_subtype": None, "original_report_id": str(rnd)} for rnd in (1, 2, 3)]
        rows += [{**rows[0], "original_report_id": "novel", "validity": "VALID_NOVEL", "full_ledger_ids": []},
                 {**rows[0], "original_report_id": "invalid", "validity": "INVALID", "full_ledger_ids": [], "d_tier": None}]
        result = calculate(rows, items)
        self.assertEqual((result["K"], result["N"], result["I"]), (3, 1, 1))
        self.assertEqual(result["precision"]["rate"], 4 / 5)
        self.assertEqual(result["hit1"]["denominator"], 9)
        self.assertEqual(result["hit1"]["numerator"], 3)
        self.assertEqual(result["hitall"]["numerator"], 1)
        self.assertEqual(result["tiers"]["L2"]["hit1"]["numerator"], 0)

    def test_partial_is_support_not_full_hit_and_d0_is_not_strict(self):
        items = {"e": {"L": "L2"}}
        row = {"validity": "VALID_KNOWN", "round": 1, "pair_id": "0000", "full_ledger_ids": [],
               "partial_ledger_ids": ["e"], "d_tier": "D0", "a0_subtype": None, "original_report_id": "a"}
        result = calculate([row], items)
        self.assertEqual(result["hit1"]["numerator"], 0)
        self.assertEqual(result["supported"]["hit1"]["numerator"], 1)
        self.assertEqual(result["precision"]["rate"], 1)
        self.assertEqual(result["strict"]["precision"]["rate"], 0)


if __name__ == "__main__":
    unittest.main()
