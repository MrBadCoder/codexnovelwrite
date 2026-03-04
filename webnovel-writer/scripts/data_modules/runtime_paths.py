#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runtime path helpers shared by project locator and config loading.

Codex-first priority:
1) WEBNOVEL_RUNTIME_ROOT / WEBNOVEL_WORKSPACE_ROOT
2) CODEX_HOME
3) Legacy CLAUDE_* compatibility
"""

from __future__ import annotations

import os
from pathlib import Path

from runtime_compat import normalize_windows_path

ENV_WEBNOVEL_RUNTIME_ROOT = "WEBNOVEL_RUNTIME_ROOT"
ENV_WEBNOVEL_WORKSPACE_ROOT = "WEBNOVEL_WORKSPACE_ROOT"
ENV_CODEX_HOME = "CODEX_HOME"
ENV_WEBNOVEL_CLAUDE_HOME = "WEBNOVEL_CLAUDE_HOME"
ENV_CLAUDE_HOME = "CLAUDE_HOME"
ENV_CLAUDE_PROJECT_DIR = "CLAUDE_PROJECT_DIR"


def _resolve_env_path(env_name: str) -> Path | None:
    raw = os.environ.get(env_name)
    if not raw:
        return None
    try:
        return normalize_windows_path(raw).expanduser().resolve()
    except Exception:
        return normalize_windows_path(raw).expanduser()


def get_runtime_root() -> Path:
    for env_name in (
        ENV_WEBNOVEL_RUNTIME_ROOT,
        ENV_CODEX_HOME,
        ENV_WEBNOVEL_CLAUDE_HOME,
        ENV_CLAUDE_HOME,
    ):
        candidate = _resolve_env_path(env_name)
        if candidate is not None:
            return candidate
    return (Path.home() / ".codex").resolve()


def get_workspace_root(*, cwd: Path | None = None) -> Path:
    for env_name in (ENV_WEBNOVEL_WORKSPACE_ROOT, ENV_CLAUDE_PROJECT_DIR):
        candidate = _resolve_env_path(env_name)
        if candidate is not None:
            return candidate
    return (cwd or Path.cwd()).resolve()


def _get_codex_root() -> Path:
    return _resolve_env_path(ENV_WEBNOVEL_RUNTIME_ROOT) or _resolve_env_path(ENV_CODEX_HOME) or (
        Path.home() / ".codex"
    ).resolve()


def _get_claude_root() -> Path:
    return _resolve_env_path(ENV_WEBNOVEL_CLAUDE_HOME) or _resolve_env_path(ENV_CLAUDE_HOME) or (
        Path.home() / ".claude"
    ).resolve()


def get_user_config_dirs() -> list[Path]:
    """Return config directory candidates in read-order (codex first, claude fallback)."""
    results: list[Path] = []
    seen: set[str] = set()
    for root in (_get_codex_root(), _get_claude_root()):
        candidate = root / "webnovel-writer"
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        results.append(candidate)
    return results


def get_user_config_dir() -> Path:
    """Primary writable config directory (Codex-first)."""
    return get_user_config_dirs()[0]

