from __future__ import annotations

import argparse
import json
from pathlib import Path

from .lowering import PAPER_ROOT, export_selected, sync_selected_fcstm_snapshots


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R4.5 canonical STM JSON -> pyfcstm .fcstm exporter")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("export-selected", help="Export the committed selected seed examples to .fcstm reports")
    p.add_argument("--reports-dir", type=Path, default=PAPER_ROOT / "representation/reports")
    p.add_argument("--conversion-reports-dir", type=Path, default=PAPER_ROOT / "conversion/reports")
    p_sync = sub.add_parser("sync-selected-fcstm", help="Copy R4.5 .fcstm snapshots into selected_seed_examples")
    p_sync.add_argument("--reports-dir", type=Path, default=PAPER_ROOT / "representation/reports")
    p_sync.add_argument("--selected-dir", type=Path, default=PAPER_ROOT / "selected_seed_examples")
    args = parser.parse_args(argv)
    if args.cmd == "export-selected":
        report = export_selected(args.reports_dir, args.conversion_reports_dir)
        print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "sync-selected-fcstm":
        report = sync_selected_fcstm_snapshots(reports_dir=args.reports_dir, selected_dir=args.selected_dir)
        print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
        return 0
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
