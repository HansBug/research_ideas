from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from expert_review import ExpertReviewAgent, ExpertReviewRequest, result_to_flat_row
from expert_review.expert_review_schema import to_dict
from io_utils import baseline_result_dir, write_json, write_parquet


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _first_present(row: pd.Series, *columns: str) -> str:
    for column in columns:
        value = _normalize_text(row.get(column))
        if value is not None:
            return value
    return ""


def _preferred_artifact(row: pd.Series, *columns: str) -> str | None:
    for column in columns:
        value = _normalize_text(row.get(column))
        if value is not None:
            return value
    return None


def _baseline_prompt(baseline: str, row: pd.Series) -> str:
    case_name = _normalize_text(row.get("case_name")) or _normalize_text(row.get("fragment_title")) or "this case"
    if baseline == "ttool":
        return (
            f"Help me evaluate the TTool/AVATAR model for {case_name}. "
            "Use expert-style grading close to the paper's human review: adequacy to specification, "
            "behavioral plausibility, reasonableness of exchanges between blocks, readability and naming discipline, "
            "and notation well-formedness. Give traceable reasons for both strengths and defects."
        )
    if baseline == "nimbus":
        return (
            f"Help me evaluate the requirements-oriented state model for {case_name}. "
            "Focus on requirement completeness, traceability, exception and malfunction handling, "
            "and whether the prediction introduces unsupported rules or states."
        )
    if baseline == "llms_emp":
        return (
            f"Help me evaluate the generated behavior model for {case_name}. "
            "Focus on whether the predicted diagram preserves the intended process logic, control branches, "
            "and overall modeling clarity relative to the requirements."
        )
    return (
        f"Help me evaluate the generated state-machine artifact for {case_name}. "
        "Focus on modeling correctness, behavioral consistency, requirement coverage, and unnecessary invented structure."
    )


def _request_from_payload(payload: dict[str, Any]) -> ExpertReviewRequest:
    prompt = _normalize_text(payload.get("prompt")) or _normalize_text(payload.get("review_prompt")) or ""
    input_text = _normalize_text(payload.get("input_text")) or _normalize_text(payload.get("input")) or ""
    pred_output = (
        _normalize_text(payload.get("pred_output"))
        or _normalize_text(payload.get("prediction_output_json"))
        or _normalize_text(payload.get("prediction_output_text"))
        or _normalize_text(payload.get("prediction_output"))
        or ""
    )
    ref_output = (
        _normalize_text(payload.get("ref_output"))
        or _normalize_text(payload.get("reference_output_json"))
        or _normalize_text(payload.get("reference_output_text"))
        or _normalize_text(payload.get("reference_output"))
    )
    return ExpertReviewRequest(
        prompt=prompt,
        input_text=input_text,
        pred_output=pred_output,
        ref_output=ref_output,
    )


def _request_columns(request: ExpertReviewRequest) -> dict[str, Any]:
    return {
        "prompt": request.prompt,
        "input_text": request.input_text,
        "pred_output": request.pred_output,
        "ref_output": request.ref_output,
    }


def review_request(request: ExpertReviewRequest) -> dict[str, Any]:
    agent = ExpertReviewAgent()
    result = agent.review(request)
    return {
        "result": result,
        "flat_row": {
            **_request_columns(request),
            **result_to_flat_row(result),
        },
    }


def _load_request(path: Path) -> ExpertReviewRequest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _request_from_payload(payload)


def _load_baseline_requests(baseline: str, max_samples: int | None = None) -> list[ExpertReviewRequest]:
    root = Path(__file__).resolve().parent / "results" / baseline
    pred_path = root / "predictions.parquet"
    df = pd.read_parquet(pred_path)
    if max_samples is not None:
        df = df.head(max_samples).copy()
    requests: list[ExpertReviewRequest] = []
    for _, row in df.iterrows():
        requests.append(
            ExpertReviewRequest(
                prompt=_baseline_prompt(baseline, row),
                input_text=_first_present(row, "input_text", "requirements_description", "input_requirement_text"),
                pred_output=_preferred_artifact(
                    row,
                    "prediction_output_json",
                    "prediction_json",
                    "prediction_output_text",
                )
                or "",
                ref_output=_preferred_artifact(
                    row,
                    "reference_output_json",
                    "reference_output_text",
                ),
            )
        )
    return requests


def run_baseline_reviews(baseline: str, max_samples: int | None = None) -> tuple[pd.DataFrame, dict[str, Any]]:
    requests = _load_baseline_requests(baseline, max_samples=max_samples)
    pred_path = Path(__file__).resolve().parent / "results" / baseline / "predictions.parquet"
    source_df = pd.read_parquet(pred_path)
    if max_samples is not None:
        source_df = source_df.head(max_samples).copy()
    rows = []
    full_payload = []
    for request, (_, source_row) in zip(requests, source_df.iterrows()):
        reviewed = review_request(request)
        rows.append(
            {
                "baseline_name": source_row.get("baseline_name", baseline),
                "sample_id": source_row.get("sample_id"),
                "case_id": source_row.get("case_id"),
                "case_name": source_row.get("case_name"),
                "variant_id": source_row.get("variant_id"),
                "variant_name": source_row.get("variant_name"),
                "sample_kind": source_row.get("sample_kind"),
                "strategy_name": source_row.get("strategy_name"),
                "input_modality": source_row.get("input_modality"),
                "reference_output_format": source_row.get("reference_output_format"),
                "prediction_output_format": source_row.get("prediction_output_format"),
                "evaluation_method": source_row.get("evaluation_method"),
                "primary_metric_name": source_row.get("primary_metric_name"),
                "primary_metric_value": source_row.get("primary_metric_value"),
                "component_metrics_json": source_row.get("component_metrics_json"),
                **reviewed["flat_row"],
            }
        )
        full_payload.append(to_dict(reviewed["result"]))
    df = pd.DataFrame(rows)
    summary = {
        "baseline": baseline,
        "review_count": len(full_payload),
        "overall_score_mean": float(df["overall_score"].mean()) if not df.empty else None,
        "overall_score_min": float(df["overall_score"].min()) if not df.empty else None,
        "overall_score_max": float(df["overall_score"].max()) if not df.empty else None,
        "reviews": full_payload,
    }
    return df, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    file_parser = sub.add_parser("review-file")
    file_parser.add_argument("--request-json", required=True)
    file_parser.add_argument("--output-json")

    baseline_parser = sub.add_parser("review-baseline")
    baseline_parser.add_argument("--baseline", required=True, choices=["structure_event", "llms_emp", "ttool", "nimbus"])
    baseline_parser.add_argument("--max-samples", type=int, default=None)

    args = parser.parse_args()

    if args.command == "review-file":
        request = _load_request(Path(args.request_json))
        reviewed = review_request(request)
        payload = to_dict(reviewed["result"])
        if args.output_json:
            Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "review-baseline":
        df, summary = run_baseline_reviews(args.baseline, max_samples=args.max_samples)
        result_dir = baseline_result_dir(args.baseline) / "expert_review"
        result_dir.mkdir(parents=True, exist_ok=True)
        write_parquet(df, result_dir / "reviews.parquet")
        write_json(summary, result_dir / "summary.json")
        print(
            json.dumps(
                {
                    "baseline": args.baseline,
                    "output_parquet": str(result_dir / "reviews.parquet"),
                    "output_summary": str(result_dir / "summary.json"),
                    "review_count": len(df),
                    "overall_score_mean": summary["overall_score_mean"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
