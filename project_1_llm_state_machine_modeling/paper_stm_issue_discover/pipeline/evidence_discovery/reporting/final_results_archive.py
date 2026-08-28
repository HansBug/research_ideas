"""Deprecated executable compatibility wrapper for final-results validation."""

from paper_stm_evaluation import final_results_archive as _implementation

main = _implementation.main


def __getattr__(name: str):
    """Forward public and historical private helpers without duplicating logic."""

    return getattr(_implementation, name)


if __name__ == "__main__":
    raise SystemExit(main())
