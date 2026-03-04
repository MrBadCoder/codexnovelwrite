#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path

import pytest


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def _load_webnovel_module():
    _ensure_scripts_on_path()
    import data_modules.webnovel as webnovel_module

    return webnovel_module


@pytest.mark.parametrize(
    ("tool", "module_name", "tail_args"),
    [
        ("index", "index_manager", ["stats"]),
        ("state", "state_manager", ["dump"]),
        ("rag", "rag_adapter", ["query", "主角"]),
        ("context", "context_manager", ["build", "--chapter", "3"]),
    ],
)
def test_cli_forwards_core_tools_with_resolved_project_root(monkeypatch, tmp_path, tool, module_name, tail_args):
    module = _load_webnovel_module()

    book_root = (tmp_path / "book").resolve()
    called = {}

    monkeypatch.setattr(module, "_resolve_root", lambda _explicit_project_root=None: book_root)

    def _fake_run_data_module(name, argv):
        called["name"] = name
        called["argv"] = list(argv)
        return 0

    monkeypatch.setattr(module, "_run_data_module", _fake_run_data_module)
    monkeypatch.setattr(sys, "argv", ["webnovel", tool, *tail_args])

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0
    assert called["name"] == module_name
    assert called["argv"][:2] == ["--project-root", str(book_root)]
    assert called["argv"][2:] == tail_args


def test_cli_where_prints_resolved_path(monkeypatch, tmp_path, capsys):
    module = _load_webnovel_module()

    book_root = (tmp_path / "book").resolve()
    monkeypatch.setattr(module, "_resolve_root", lambda _explicit_project_root=None: book_root)
    monkeypatch.setattr(sys, "argv", ["webnovel", "where"])

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0
    assert capsys.readouterr().out.strip() == str(book_root)


def test_cli_use_writes_pointer_and_registry(monkeypatch, tmp_path, capsys):
    module = _load_webnovel_module()

    workspace_root = (tmp_path / "workspace").resolve()
    project_root = (workspace_root / "book").resolve()
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    pointer_file = workspace_root / ".codex" / ".webnovel-current-project"
    registry_file = tmp_path / "home" / ".codex" / "webnovel-writer" / "workspaces.json"

    called = {}

    def _fake_write_pointer(project_root_arg, *, workspace_root=None):
        called["pointer_project_root"] = project_root_arg
        called["pointer_workspace_root"] = workspace_root
        return pointer_file

    def _fake_update_registry(*, workspace_root, project_root):
        called["registry_workspace_root"] = workspace_root
        called["registry_project_root"] = project_root
        return registry_file

    monkeypatch.setattr(module, "write_current_project_pointer", _fake_write_pointer)
    monkeypatch.setattr(module, "update_global_registry_current_project", _fake_update_registry)
    monkeypatch.setattr(
        sys,
        "argv",
        ["webnovel", "use", str(project_root), "--workspace-root", str(workspace_root)],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0
    assert called["pointer_project_root"] == project_root
    assert called["pointer_workspace_root"] == workspace_root
    assert called["registry_workspace_root"] == workspace_root
    assert called["registry_project_root"] == project_root

    output = capsys.readouterr().out
    assert str(pointer_file) in output
    assert str(registry_file) in output


def test_scripts_entrypoint_help_works():
    scripts_dir = Path(__file__).resolve().parents[2]
    script_path = scripts_dir / "webnovel.py"

    proc = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0
    assert "where" in proc.stdout
    assert "init" in proc.stdout


def test_bin_launcher_exists_and_is_executable():
    repo_root = Path(__file__).resolve().parents[4]
    launcher = repo_root / "bin" / "webnovel"

    assert launcher.is_file()
    assert os.access(launcher, os.X_OK)
