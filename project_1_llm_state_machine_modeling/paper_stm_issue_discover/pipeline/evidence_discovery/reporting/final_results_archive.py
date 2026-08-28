"""Deprecated executable compatibility wrapper for final-results validation."""

from paper_stm_evaluation.final_results_archive import *  # noqa: F403
from paper_stm_evaluation.final_results_archive import main


if __name__ == "__main__":
    raise SystemExit(main())
