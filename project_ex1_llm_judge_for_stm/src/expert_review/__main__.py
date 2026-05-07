from __future__ import annotations

import argparse

from .compatibility import review_model
from .schema import to_json


def main() -> None:
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
