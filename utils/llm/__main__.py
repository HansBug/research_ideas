from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any

import click
import yaml

from .registry import load_llm_registry, resolve_config_path


def _write_config(target: Path, data: dict[str, Any], *, force: bool) -> None:
    if target.exists() and not force:
        raise click.ClickException(f"config_error: file exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            yaml.safe_dump(data, stream, sort_keys=False, allow_unicode=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        target.chmod(stat.S_IRUSR | stat.S_IWUSR)
        load_llm_registry(target)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _summary(registry: Any, name: str | None = None) -> dict[str, Any]:
    return registry.public_summary(name)


@click.group("python -m utils.llm")
def cli() -> None:
    """管理根目录 .llmconfig.yml，不访问模型。"""


@cli.command("init")
@click.option("--from-env", is_flag=True, help="读取已经 source 的 LLM_ENDPOINT/LLM_API_KEY/LLM_MODEL。")
@click.option("--profile", default="gpt-5.5", show_default=True)
@click.option("--context-window-tokens", type=click.IntRange(min=1), default=None)
@click.option("--max-output-tokens", type=click.IntRange(min=1), default=None)
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--force", is_flag=True, help="允许覆盖已有配置文件。")
def init_command(from_env: bool, profile: str, context_window_tokens: int | None, max_output_tokens: int | None, config: Path | None, force: bool) -> None:
    if not from_env:
        raise click.ClickException("config_error: init currently requires --from-env")
    values = {key: os.environ.get(key) for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL")}
    if any(not value for value in values.values()):
        raise click.ClickException("config_error: source LLM_ENDPOINT, LLM_API_KEY and LLM_MODEL first")
    profile_values: dict[str, Any] = {
        "base_url": values["LLM_ENDPOINT"],
        "api_key": values["LLM_API_KEY"],
        "model": values["LLM_MODEL"],
    }
    if context_window_tokens is not None:
        profile_values["context_window_tokens"] = context_window_tokens
    if max_output_tokens is not None:
        profile_values["max_output_tokens"] = max_output_tokens
    target = resolve_config_path(config)
    _write_config(target, {"default": profile, "profiles": {profile: profile_values}}, force=force)
    click.echo(f"initialized profile={profile} model={values['LLM_MODEL']}")


@cli.command("validate")
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--require-credentials", is_flag=True)
def validate_command(config: Path | None, require_credentials: bool) -> None:
    registry = load_llm_registry(config)
    if require_credentials and (registry.default.api_key is None or registry.default.base_url is None):
        raise click.ClickException("config_error: default profile lacks credentials")
    click.echo(f"valid profiles={len(registry)} default={registry.default_name}")


@cli.command("list")
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--format", "output_format", type=click.Choice(("table", "json")), default="table", show_default=True)
def list_command(config: Path | None, output_format: str) -> None:
    registry = load_llm_registry(config)
    if output_format == "json":
        click.echo(json.dumps([_summary(registry, name) for name in registry.names()], ensure_ascii=False, sort_keys=True))
    else:
        for name in registry.names():
            click.echo(name)


@cli.command("show")
@click.argument("name")
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--format", "output_format", type=click.Choice(("table", "json")), default="table", show_default=True)
def show_command(name: str, config: Path | None, output_format: str) -> None:
    registry = load_llm_registry(config)
    summary = _summary(registry, name)
    if output_format == "json":
        click.echo(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    else:
        for key, value in summary.items():
            click.echo(f"{key}: {value}")


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, prog_name="python -m utils.llm", standalone_mode=False)
    except click.ClickException as exc:
        click.echo(str(exc), err=True)
        return 2
    except ValueError as exc:
        click.echo(str(exc), err=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
