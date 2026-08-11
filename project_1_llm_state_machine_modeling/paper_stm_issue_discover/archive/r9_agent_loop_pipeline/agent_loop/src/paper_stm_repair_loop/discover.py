from __future__ import annotations

from .agents.discover import main, run_discover

__all__ = ["main", "run_discover"]


if __name__ == "__main__":
    raise SystemExit(main())
