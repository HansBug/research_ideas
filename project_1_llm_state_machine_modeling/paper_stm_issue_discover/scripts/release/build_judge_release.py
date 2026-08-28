"""Build the independent Semantic Judge release by allowlisted byte copies only.

Input: a clean repository checkout and ``judge/release_allowlist.json``.
Output: an empty external directory with the Judge, its byte-identical protocol
snapshot, and only the neutral shared ``utils`` modules it imports. This command
does not call a provider, does not copy method/evaluation data, and does not
write into the source checkout.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build_method_release import build


def main(argv: list[str] | None = None) -> int:
    """Run the provider-free byte-copy Judge release builder."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build(output=args.output, allowlist_relative="judge/release_allowlist.json")
    print(manifest.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
