#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export PATH="$HOME/.jenv/bin:$HOME/bin:$HOME/.local/bin:$PATH"
if command -v jenv >/dev/null 2>&1; then
  set +u
  export PROMPT_COMMAND="${PROMPT_COMMAND-}"
  eval "$(jenv init - bash)"
  set -u
fi

UMPLE_JAR="${UMPLE_JAR:-$BASE_DIR/tooling/umple.jar}"
NUSMV_BIN="${NUSMV_BIN:-$BASE_DIR/tooling/nusmv-2.6.0-linux64/bin/NuSMV}"
ALLOY_BIN="${ALLOY_BIN:-$BASE_DIR/tooling/alloy-6.2.0-linux-amd64/bin/alloy}"
TXL_BIN_DIR="${TXL_BIN_DIR:-}"

if [ -z "$TXL_BIN_DIR" ]; then
  for candidate in \
    "$BASE_DIR/txl/txl10.8b.linux64/bin" \
    "$BASE_DIR/txl/bin"
  do
    if [ -x "$candidate/txl" ]; then
      TXL_BIN_DIR="$candidate"
      break
    fi
  done
fi
if [ -n "$TXL_BIN_DIR" ]; then
  export PATH="$TXL_BIN_DIR:$PATH"
fi

if [ ! -f "$UMPLE_JAR" ]; then
  echo "Missing UMPLE_JAR at $UMPLE_JAR" >&2
  echo "Set UMPLE_JAR=/path/to/umple.jar, populate $BASE_DIR/tooling/umple.jar, or run ./verification/bootstrap_tooling.sh" >&2
  exit 1
fi

if [ ! -x "$NUSMV_BIN" ] && command -v NuSMV >/dev/null 2>&1; then
  NUSMV_BIN="$(command -v NuSMV)"
fi
if [ ! -x "$NUSMV_BIN" ] && [ -x "$BASE_DIR/tooling/NuSMV-2.6.0-Linux/bin/NuSMV" ]; then
  NUSMV_BIN="$BASE_DIR/tooling/NuSMV-2.6.0-Linux/bin/NuSMV"
fi
if [ ! -x "$NUSMV_BIN" ]; then
  echo "Missing NuSMV binary at $NUSMV_BIN" >&2
  echo "Set NUSMV_BIN=/path/to/NuSMV, populate $BASE_DIR/tooling/nusmv-2.6.0-linux64/bin/NuSMV, or run ./verification/bootstrap_tooling.sh" >&2
  exit 1
fi

if [ ! -x "$ALLOY_BIN" ] && command -v alloy >/dev/null 2>&1; then
  ALLOY_BIN="$(command -v alloy)"
fi
if [ ! -x "$ALLOY_BIN" ] && [ -x "$BASE_DIR/tooling/alloy-6.2.0/bin/alloy" ]; then
  ALLOY_BIN="$BASE_DIR/tooling/alloy-6.2.0/bin/alloy"
fi
if [ ! -x "$ALLOY_BIN" ]; then
  echo "Missing Alloy binary at $ALLOY_BIN" >&2
  echo "Set ALLOY_BIN=/path/to/alloy, populate $BASE_DIR/tooling/alloy-6.2.0-linux-amd64/bin/alloy, or run ./verification/bootstrap_tooling.sh" >&2
  exit 1
fi

if ! command -v txl >/dev/null 2>&1; then
  echo "Missing txl in PATH" >&2
  echo "Set TXL_BIN_DIR=/path/to/txl/bin, populate $BASE_DIR/txl/txl10.8b.linux64/bin, or run ./verification/bootstrap_tooling.sh" >&2
  exit 1
fi

cd "$BASE_DIR"

rm -rf logs
mkdir -p logs verification/alloysrc/Reproduction
rm -rf models/generated/python driver_license_check

java -version 2>&1 | tee logs/00_java_version.log

java -jar "$UMPLE_JAR" -g Nothing models/driver_license_system.ump \
  > logs/01_parse_driver_license.log 2>&1
java -jar "$UMPLE_JAR" -g Python --path generated/python models/driver_license_system.ump \
  > logs/02_generate_python.log 2>&1
java -jar "$UMPLE_JAR" -g NuSMV models/driver_license_system.ump \
  > logs/03_generate_nusmv.log 2>&1
java -jar "$UMPLE_JAR" -g Alloy models/driver_license_system.ump \
  > logs/04_generate_alloy.log 2>&1

python3 -m py_compile models/generated/python/Reproduction/DriverLicense/*.py
python3 verification/run_driver_license_python_demo.py | tee logs/07_python_demo_run.log

"$NUSMV_BIN" verification/driver_license_verified.smv \
  | tee logs/08_nusmv_verified_run.log

cp models/driver_license_system.als verification/alloysrc/Reproduction/DriverLicense.als
"$ALLOY_BIN" commands verification/alloysrc/driver_license_check.als \
  | tee logs/09_alloy_commands.log
"$ALLOY_BIN" exec verification/alloysrc/driver_license_check.als \
  | tee logs/10_alloy_exec.log

java -jar "$UMPLE_JAR" -g Python --path generated/python models/garage_door_direct.ump \
  > logs/11_generate_garage_python.log 2>&1
java -jar "$UMPLE_JAR" -g NuSMV models/garage_door_direct.ump \
  > logs/12_generate_garage_nusmv.log 2>&1
python3 -m py_compile models/generated/python/Reproduction/DirectGarageDoor/*.py
python3 verification/run_garage_door_python_demo.py | tee logs/13_garage_python_demo_run.log
"$NUSMV_BIN" models/garage_door_direct.smv \
  | tee logs/14_garage_nusmv_raw_run.log
"$NUSMV_BIN" -source verification/garage_door_direct_nusmv_commands.txt models/garage_door_direct.smv \
  | tee logs/15_garage_nusmv_direct_properties.log

echo "reproduction_ok"
