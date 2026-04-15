#!/usr/bin/env python3

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
PYTHON_OUT = BASE_DIR / "models" / "generated" / "python"
sys.path.insert(0, str(PYTHON_OUT))

from Reproduction.DirectGarageDoor.GarageDoor import GarageDoor


def dump(label: str, door: GarageDoor) -> None:
    print(f"{label}: state={door.getStatusFullName()}")


def main() -> None:
    door = GarageDoor()
    dump("initial", door)

    door.buttonOrObstacle()
    dump("after_close_start", door)

    door.reachBottom()
    dump("after_closed", door)

    door.buttonOrObstacle()
    dump("after_open_start", door)

    door.buttonOrObstacle()
    dump("after_halfopen", door)

    door.buttonOrObstacle()
    dump("after_reopen", door)

    door.reachTop()
    dump("after_open", door)

    print("garage_python_demo_ok")


if __name__ == "__main__":
    main()
