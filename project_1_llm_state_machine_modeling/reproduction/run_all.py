from __future__ import annotations

import argparse

from config import ensure_runtime_dirs


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("download-raw")
    subparsers.add_parser("augment-parquets")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "--baseline",
        required=True,
        choices=["llms_emp", "ttool", "nimbus", "structure_event", "all"],
    )

    subparsers.add_parser("report")

    args = parser.parse_args()
    ensure_runtime_dirs()

    if args.command == "download-raw":
        from tasks import download_raw_data

        download_raw_data()
        return

    if args.command == "augment-parquets":
        from tasks import augment_parquets

        augment_parquets()
        return

    if args.command == "report":
        from tasks import write_report

        write_report()
        return

    if args.command == "run":
        from tasks import run_baseline

        if args.baseline == "all":
            for baseline in ("llms_emp", "ttool", "nimbus", "structure_event"):
                run_baseline(baseline)
            return
        run_baseline(args.baseline)


if __name__ == "__main__":
    main()
