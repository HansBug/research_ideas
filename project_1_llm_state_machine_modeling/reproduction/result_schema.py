from __future__ import annotations

import pandas as pd


COMMON_RESULT_COLUMNS = [
    "baseline_name",
    "dataset_id",
    "sample_id",
    "case_id",
    "case_name",
    "variant_id",
    "variant_name",
    "sample_kind",
    "strategy_name",
    "input_modality",
    "input_text",
    "input_payload_json",
    "reference_output_text",
    "reference_output_json",
    "prediction_output_text",
    "prediction_output_json",
    "reference_output_format",
    "prediction_output_format",
    "reference_counts_json",
    "prediction_counts_json",
    "llm_provider",
    "llm_model_name",
    "llm_raw_mode",
    "is_repaired",
    "evaluation_method",
    "primary_metric_name",
    "primary_metric_value",
    "component_metrics_json",
]


def finalize_result_df(df: pd.DataFrame) -> pd.DataFrame:
    aligned = df.copy()
    for column in COMMON_RESULT_COLUMNS:
        if column not in aligned.columns:
            aligned[column] = None
    ordered_columns = COMMON_RESULT_COLUMNS + [
        column for column in aligned.columns if column not in COMMON_RESULT_COLUMNS
    ]
    return aligned[ordered_columns]
