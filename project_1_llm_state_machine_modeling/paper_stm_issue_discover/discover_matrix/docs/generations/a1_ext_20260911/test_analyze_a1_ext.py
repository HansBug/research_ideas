"""Fixed denominators, strict interval determinism, real-archive verification and a tamper counterexample; no provider."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from a1ext_common import content_breakdown, expected_rows, strict_cluster_bootstrap
import analyze_a1_ext


def item(eid, pair, level, element, cluster):
    return {"id": eid, "pair": pair, "L": level, "axes": {"defect_element": element, "defect_logic_kind": None},
            "pair_context": {"nl_sha8": cluster}}


def report(rid, pair, rnd, validity, full=(), d_tier="D2", cluster="c0"):
    return {"original_report_id": rid, "pair_id": pair, "round": rnd, "validity": validity, "d_tier": d_tier,
            "a0_subtype": None, "full_ledger_ids": list(full), "partial_ledger_ids": [], "nl_cluster": cluster}


class ArithmeticTests(unittest.TestCase):
    def setUp(self):
        self.items = {f"e{i}": item(f"e{i}", f"p{i % 3}", ("L0", "L1", "L2")[i % 3], ("trigger", "state")[i % 2], f"c{i % 9}") for i in range(9)}

    def test_expected_rows_cover_every_item_round_and_flag_only_valid_known_full_support(self):
        reports = [report("a", "p0", 1, "VALID_KNOWN", ["e0"]), report("b", "p0", 1, "INVALID", ["e0"], d_tier=None),
                   report("c", "p0", 2, "VALID_NOVEL", [])]
        rows = expected_rows(reports, self.items)
        self.assertEqual(len(rows), 27)
        hit = {(r["ledger_id"], r["round"]): r for r in rows}
        self.assertTrue(hit["e0", 1]["hit"] and hit["e0", 1]["full_report_ids"] == ["a"])
        self.assertFalse(hit["e0", 2]["hit"] or hit["e3", 1]["hit"])

    def test_content_split_denominators_are_three_rounds_per_item(self):
        reports = [report("a", "p1", 1, "VALID_KNOWN", ["e1"]), report("b", "p1", 3, "VALID_KNOWN", ["e1"])]
        split = content_breakdown(reports, self.items)["defect_element"]
        self.assertEqual(split["state"]["denominator"], 3 * 4)
        self.assertEqual(split["state"]["numerator"], 2)
        self.assertEqual(split["trigger"]["numerator"], 0)

    def test_strict_interval_is_deterministic_and_contains_the_point_difference(self):
        a = {"reports": [report(f"a{i}", f"p{i % 3}", 1, "VALID_KNOWN", [f"e{i}"], d_tier="D1", cluster=f"c{i % 9}") for i in range(9)]}
        b = {"reports": [report(f"b{i}", f"p{i % 3}", 1, "VALID_KNOWN", [f"e{i}"], d_tier="D0", cluster=f"c{i % 9}") for i in range(9)]}
        first = strict_cluster_bootstrap(a, b, self.items, replicates=300)
        second = strict_cluster_bootstrap(a, b, self.items, replicates=300)
        self.assertEqual(first, second)
        delta = first["delta_pp"]["strict_precision"]
        self.assertEqual(delta, 100.0)
        ci = first["cluster_bootstrap_95pct"]["strict_precision"]
        self.assertLessEqual(ci["percentile_2_5"], delta)
        self.assertGreaterEqual(ci["percentile_97_5"], delta)


class ArchiveTests(unittest.TestCase):
    def test_frozen_archive_verifies_offline(self):
        data, items, luna = analyze_a1_ext.verify()
        self.assertEqual(set(data["models"]), {"sonnet", "muse", "qwen"})
        for model in data["models"]:
            for arm in ("a1ext", "full"):
                self.assertEqual(data["models"][model][arm]["coverage"]["judged_cells"], 162)

    def test_tampered_label_is_rejected_even_with_refreshed_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "archive"
            shutil.copytree(analyze_a1_ext.ARCHIVE, archive)
            data = json.loads((archive / "results.json").read_text())
            target = next(r for r in data["models"]["sonnet"]["a1ext"]["reports"] if r["validity"] == "VALID_KNOWN")
            target["validity"] = "INVALID"
            (archive / "results.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
            manifest = json.loads((archive / "archive_manifest.json").read_text())
            manifest["files"]["results.json"] = "sha256:" + hashlib.sha256((archive / "results.json").read_bytes()).hexdigest()
            (archive / "archive_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
            with self.assertRaises(AssertionError):
                analyze_a1_ext.verify(archive)


if __name__ == "__main__":
    unittest.main()
