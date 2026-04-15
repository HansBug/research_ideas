#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLING_DIR="$BASE_DIR/tooling"
TXL_ROOT="$BASE_DIR/txl"
JENV_ROOT="${JENV_ROOT:-$HOME/.jenv}"
TARGET_JDK_HOME="${TARGET_JDK_HOME:-$HOME/.local/jdks/temurin-17.0.18+8}"

TEMURIN_URL="${TEMURIN_URL:-https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.18%2B8/OpenJDK17U-jdk_x64_linux_hotspot_17.0.18_8.tar.gz}"
UMPLE_JAR_URL="${UMPLE_JAR_URL:-https://try.umple.org/scripts/umple.jar}"
NUSMV_URL="${NUSMV_URL:-https://nusmv.fbk.eu/distrib/NuSMV-2.6.0-linux64.tar.gz}"
ALLOY_URL="${ALLOY_URL:-https://github.com/AlloyTools/org.alloytools.alloy/releases/download/v6.2.0/alloy-6.2.0-linux-amd64.tar.gz}"
TXL_DOWNLOAD_PAGE="${TXL_DOWNLOAD_PAGE:-https://www.txl.ca/cgi-bin/txl-download.cgi}"

mkdir -p "$TOOLING_DIR" "$TXL_ROOT" "$(dirname "$TARGET_JDK_HOME")"

download_to() {
  local url="$1"
  local output="$2"
  curl -fsSL -o "$output" "$url"
}

ensure_jenv_shell_init() {
  local file
  local marker='__JENV_INITIALIZED'
  local block
  block=$'if [ -z "${__JENV_INITIALIZED:-}" ] && [ -d "$HOME/.jenv" ]; then\n  export PATH="$HOME/.jenv/bin:$PATH"\n  if command -v jenv >/dev/null 2>&1; then\n    eval "$(jenv init -)"\n    export __JENV_INITIALIZED=1\n  fi\nfi'

  for file in "$HOME/.bash_profile" "$HOME/.bashrc"; do
    touch "$file"
    if ! rg -F "$marker" "$file" >/dev/null 2>&1; then
      printf '\n%s\n' "$block" >> "$file"
    fi
  done
}

init_jenv() {
  export PATH="$JENV_ROOT/bin:$PATH"
  if [ ! -d "$JENV_ROOT" ]; then
    git clone https://github.com/jenv/jenv.git "$JENV_ROOT"
  fi
  ensure_jenv_shell_init
  set +u
  export PROMPT_COMMAND="${PROMPT_COMMAND-}"
  eval "$(jenv init - bash)"
  set -u
}

install_temurin() {
  local jdk_home
  jdk_home="${TARGET_JDK_HOME:-$HOME/.local/jdks/temurin-17.0.18+8}"

  if [ ! -x "$jdk_home/bin/java" ]; then
    local tmpdir
    tmpdir="$(mktemp -d)"
    download_to "$TEMURIN_URL" "$tmpdir/jdk.tar.gz"
    tar xzf "$tmpdir/jdk.tar.gz" -C "$tmpdir"
    local extracted
    extracted="$(find "$tmpdir" -maxdepth 1 -mindepth 1 -type d -name 'jdk-*' | head -n 1)"
    rm -rf "$jdk_home"
    mv "$extracted" "$jdk_home"
    rm -rf "$tmpdir"
  fi

  init_jenv
  if ! jenv versions --bare | rg -x '17\.0\.18' >/dev/null 2>&1; then
    jenv add "$jdk_home"
  fi
  jenv rehash
}

install_umple() {
  if [ ! -f "$TOOLING_DIR/umple.jar" ]; then
    download_to "$UMPLE_JAR_URL" "$TOOLING_DIR/umple.jar"
  fi
}

install_nusmv() {
  if [ ! -x "$TOOLING_DIR/nusmv-2.6.0-linux64/bin/NuSMV" ] && [ ! -x "$TOOLING_DIR/NuSMV-2.6.0-Linux/bin/NuSMV" ]; then
    local tmpdir
    tmpdir="$(mktemp -d)"
    download_to "$NUSMV_URL" "$tmpdir/nusmv.tar.gz"
    tar xzf "$tmpdir/nusmv.tar.gz" -C "$TOOLING_DIR"
    rm -rf "$tmpdir"
  fi
  if [ -d "$TOOLING_DIR/NuSMV-2.6.0-Linux" ]; then
    ln -sfn NuSMV-2.6.0-Linux "$TOOLING_DIR/nusmv-2.6.0-linux64"
  fi
}

install_alloy() {
  if [ ! -x "$TOOLING_DIR/alloy-6.2.0-linux-amd64/bin/alloy" ] && [ ! -x "$TOOLING_DIR/alloy-6.2.0/bin/alloy" ]; then
    local tmpdir
    tmpdir="$(mktemp -d)"
    download_to "$ALLOY_URL" "$tmpdir/alloy.tar.gz"
    tar xzf "$tmpdir/alloy.tar.gz" -C "$TOOLING_DIR"
    rm -rf "$tmpdir"
  fi
  if [ -d "$TOOLING_DIR/alloy-6.2.0" ]; then
    ln -sfn alloy-6.2.0 "$TOOLING_DIR/alloy-6.2.0-linux-amd64"
  fi
}

resolve_txl_url() {
  curl -fsSL -d 'Platform=linux64&Submit=I+Agree' "$TXL_DOWNLOAD_PAGE" \
    | sed -n "s#.*HREF='\\([^']*txl10\\.8b\\.linux64\\.tar\\.gz\\)'.*#https://www.txl.ca/\\1#p" \
    | head -n 1
}

install_txl() {
  if [ ! -x "$TXL_ROOT/txl10.8b.linux64/bin/txl" ]; then
    local tmpdir txl_url
    tmpdir="$(mktemp -d)"
    txl_url="$(resolve_txl_url)"
    if [ -z "$txl_url" ]; then
      echo "Unable to resolve FreeTXL download URL" >&2
      exit 1
    fi
    download_to "$txl_url" "$tmpdir/txl.tar.gz"
    tar xzf "$tmpdir/txl.tar.gz" -C "$TXL_ROOT"
    rm -rf "$tmpdir"
  fi
}

install_temurin
install_umple
install_nusmv
install_alloy
install_txl

cd "$BASE_DIR"
echo "java_home=$TARGET_JDK_HOME"
java -version
java -jar "$TOOLING_DIR/umple.jar" -version
"$TOOLING_DIR/nusmv-2.6.0-linux64/bin/NuSMV" -h 2>&1 | sed -n '1,3p' || true
"$TOOLING_DIR/alloy-6.2.0-linux-amd64/bin/alloy" --help 2>&1 | sed -n '1,3p' || true
"$TXL_ROOT/txl10.8b.linux64/bin/txl" 2>&1 | sed -n '1,2p' || true
