#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def test_runtime_root_prefers_codex_env(monkeypatch, tmp_path):
    _ensure_scripts_on_path()

    from data_modules.runtime_paths import get_runtime_root

    codex_home = tmp_path / "codex-home"
    claude_home = tmp_path / "claude-home"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    monkeypatch.setenv("CLAUDE_HOME", str(claude_home))
    monkeypatch.delenv("WEBNOVEL_RUNTIME_ROOT", raising=False)

    assert get_runtime_root() == codex_home.resolve()


def test_runtime_root_override_with_webnovel_runtime_root(monkeypatch, tmp_path):
    _ensure_scripts_on_path()

    from data_modules.runtime_paths import get_runtime_root

    override_root = tmp_path / "runtime-root"
    codex_home = tmp_path / "codex-home"
    monkeypatch.setenv("WEBNOVEL_RUNTIME_ROOT", str(override_root))
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    assert get_runtime_root() == override_root.resolve()


def test_user_config_dirs_include_codex_then_claude(monkeypatch, tmp_path):
    _ensure_scripts_on_path()

    from data_modules.runtime_paths import get_user_config_dirs

    codex_home = tmp_path / "codex"
    claude_home = tmp_path / "claude"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    monkeypatch.setenv("CLAUDE_HOME", str(claude_home))
    monkeypatch.delenv("WEBNOVEL_RUNTIME_ROOT", raising=False)
    monkeypatch.delenv("WEBNOVEL_CLAUDE_HOME", raising=False)

    config_dirs = get_user_config_dirs()
    assert config_dirs[0] == (codex_home / "webnovel-writer").resolve()
    assert config_dirs[1] == (claude_home / "webnovel-writer").resolve()


def test_workspace_root_prefers_webnovel_workspace_root(monkeypatch, tmp_path):
    _ensure_scripts_on_path()

    from data_modules.runtime_paths import get_workspace_root

    ws = tmp_path / "workspace"
    monkeypatch.setenv("WEBNOVEL_WORKSPACE_ROOT", str(ws))
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "legacy-workspace"))

    assert get_workspace_root(cwd=tmp_path / "unused") == ws.resolve()
