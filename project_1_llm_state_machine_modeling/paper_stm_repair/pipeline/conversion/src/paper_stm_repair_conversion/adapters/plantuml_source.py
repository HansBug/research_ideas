from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PLANTUML_VERSION = "1.2024.7"
PLANTUML_SHA256 = "e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24"
JAVA_MAIN = "researchideas.plantuml.PlantUmlStateFrontend"
BUILD_FINGERPRINT_SCHEMA = "paper1.plantuml_java_build.v1"


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in (current, *current.parents):
        if (parent / "project_1_llm_state_machine_modeling").is_dir() and (
            parent / ".git"
        ).exists():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
JAVA_ROOT = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion"
    / "java/plantuml-state-frontend"
)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _javac_version() -> str:
    completed = subprocess.run(["javac", "-version"], text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "javac is unavailable for the PlantUML source frontend.\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return (completed.stderr or completed.stdout).strip()


def _java_version() -> str:
    completed = subprocess.run(["java", "-version"], text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "java is unavailable for the PlantUML source frontend.\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return (completed.stderr or completed.stdout).strip()


def _java_compilation_input_identity(jar: Path) -> dict[str, Any]:
    source_root = JAVA_ROOT / "src/main/java"
    sources = sorted(source_root.rglob("*.java"))
    if not sources:
        raise RuntimeError(f"Java frontend sources are missing: {source_root}")
    rows = [
        {
            "path": path.relative_to(JAVA_ROOT).as_posix(),
            "sha256": _sha256_file(path),
        }
        for path in sources
    ]
    makefile = JAVA_ROOT / "Makefile"
    identity = {
        "plantuml_version": PLANTUML_VERSION,
        "plantuml_jar_sha256": _sha256_file(jar),
        "java_version": _java_version(),
        "javac_version": _javac_version(),
        "makefile_sha256": _sha256_file(makefile),
        "source_inventory": rows,
    }
    identity["input_sha256"] = _sha256_json(identity)
    return identity


def _java_class_tree_identity() -> dict[str, Any]:
    classes_root = JAVA_ROOT / "build/classes"
    rows = [
        {
            "path": path.relative_to(classes_root).as_posix(),
            "sha256": _sha256_file(path),
        }
        for path in sorted(classes_root.rglob("*.class"))
        if path.is_file()
    ]
    if not rows:
        raise RuntimeError(f"Java frontend class tree is empty: {classes_root}")
    return {
        "class_inventory": rows,
        "class_tree_sha256": _sha256_json(rows),
    }


def _build_fingerprint_path() -> Path:
    return JAVA_ROOT / "build/frontend-build.json"


def _read_build_fingerprint() -> dict[str, Any] | None:
    path = _build_fingerprint_path()
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def _write_build_fingerprint(value: dict[str, Any]) -> None:
    path = _build_fingerprint_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def resolve_plantuml_jar(plantuml_jar: Path | None = None) -> Path:
    candidates = []
    if plantuml_jar is not None:
        candidates.append(plantuml_jar)
    if os.environ.get("PLANTUML_JAR"):
        candidates.append(Path(os.environ["PLANTUML_JAR"]))
    candidates.extend(
        [
            JAVA_ROOT / f".cache/plantuml-{PLANTUML_VERSION}.jar",
            REPO_ROOT / f"tools/plantuml-{PLANTUML_VERSION}.jar",
            REPO_ROOT / "tools/plantuml.jar",
        ]
    )
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if not candidate.is_file():
            continue
        actual = _sha256_file(candidate)
        if actual != PLANTUML_SHA256:
            raise RuntimeError(
                f"PlantUML jar identity mismatch: {candidate}; "
                f"expected {PLANTUML_SHA256}, got {actual}"
            )
        return candidate
    raise FileNotFoundError(
        f"Pinned PlantUML {PLANTUML_VERSION} jar not found. Set PLANTUML_JAR or run "
        f"`make fetch` in {JAVA_ROOT}."
    )


def compile_java_frontend(
    *, plantuml_jar: Path | None = None, force: bool = False
) -> Path:
    jar = resolve_plantuml_jar(plantuml_jar)
    class_file = (
        JAVA_ROOT / "build/classes/researchideas/plantuml/PlantUmlStateFrontend.class"
    )
    compilation_input = _java_compilation_input_identity(jar)
    fingerprint = _read_build_fingerprint()
    stale = force or not class_file.is_file() or fingerprint is None
    if not stale:
        try:
            class_tree = _java_class_tree_identity()
        except RuntimeError:
            stale = True
        else:
            stale = (
                fingerprint.get("schema_version") != BUILD_FINGERPRINT_SCHEMA
                or fingerprint.get("input_sha256") != compilation_input["input_sha256"]
                or fingerprint.get("class_tree_sha256")
                != class_tree["class_tree_sha256"]
            )
    if stale:
        completed = subprocess.run(
            ["make", "clean", "compile", f"PLANTUML_JAR={jar}"],
            cwd=JAVA_ROOT,
            text=True,
            capture_output=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "Java PlantUML frontend compilation failed.\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )
    if not class_file.is_file():
        raise RuntimeError(f"Java frontend class was not produced: {class_file}")
    class_tree = _java_class_tree_identity()
    fingerprint = {
        "schema_version": BUILD_FINGERPRINT_SCHEMA,
        **compilation_input,
        **class_tree,
    }
    _write_build_fingerprint(fingerprint)
    return jar


def java_frontend_build_identity(
    *, plantuml_jar: Path | None = None, force: bool = False
) -> dict[str, Any]:
    compile_java_frontend(plantuml_jar=plantuml_jar, force=force)
    fingerprint = _read_build_fingerprint()
    if fingerprint is None:
        raise RuntimeError("Java frontend build fingerprint was not produced")
    return fingerprint


def run_java_frontend(
    source_path: Path,
    *,
    example_id: str,
    source_name: str | None = None,
    official_source_path: Path | None = None,
    plantuml_jar: Path | None = None,
) -> dict[str, Any]:
    jar = compile_java_frontend(plantuml_jar=plantuml_jar)
    command = [
        "java",
        "-cp",
        f"{JAVA_ROOT / 'build/classes'}{os.pathsep}{jar}",
        JAVA_MAIN,
        "--source",
        str(source_path.resolve()),
        "--example-id",
        example_id,
        "--source-name",
        source_name or source_path.name,
    ]
    if official_source_path is not None:
        command.extend(["--official-source", str(official_source_path.resolve())])
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Java PlantUML frontend failed for {example_id}.\n"
            f"command: {command}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Java PlantUML frontend emitted invalid JSON for {example_id}: {error}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        ) from error
    if result.get("tool", {}).get("plantuml_version") != PLANTUML_VERSION:
        raise RuntimeError(
            f"Unexpected PlantUML runtime version: {result.get('tool', {}).get('plantuml_version')}"
        )
    return result


def parse_plantuml_source(
    text: str,
    *,
    example_id: str,
    source_name: str = "stm0.puml",
    plantuml_jar: Path | None = None,
) -> dict[str, Any]:
    """Call the pinned Java frontend and return its scope-aware canonical JSON."""

    with tempfile.TemporaryDirectory(prefix="plantuml-source-frontend-") as tmp:
        source_path = Path(tmp) / source_name
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(text, encoding="utf-8")
        result = run_java_frontend(
            source_path,
            example_id=example_id,
            source_name=source_name,
            plantuml_jar=plantuml_jar,
        )
    canonical = result["canonical"]
    canonical["metadata"]["official_model"] = result["official_model"]
    canonical["metadata"]["official_validation"] = result["official_validation"]
    canonical["metadata"]["frontend_tool"] = result["tool"]
    return canonical
