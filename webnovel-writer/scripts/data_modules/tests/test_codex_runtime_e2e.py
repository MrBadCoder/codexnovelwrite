#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys
from pathlib import Path


def test_codex_runtime_cli_chain_without_claude(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    cli = scripts_dir / "webnovel.py"

    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / ".codex").mkdir(parents=True, exist_ok=True)

    project_root = workspace / "book"
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    home = tmp_path / "home"
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["CODEX_HOME"] = str(home / ".codex")
    env["WEBNOVEL_WORKSPACE_ROOT"] = str(workspace)
    env.pop("CLAUDE_PROJECT_DIR", None)
    env.pop("WEBNOVEL_PROJECT_ROOT", None)

    use_proc = subprocess.run(
        [sys.executable, str(cli), "use", str(project_root), "--workspace-root", str(workspace)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert use_proc.returncode == 0, use_proc.stderr

    where_proc = subprocess.run(
        [sys.executable, str(cli), "--project-root", str(workspace), "where"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert where_proc.returncode == 0, where_proc.stderr
    assert where_proc.stdout.strip() == str(project_root.resolve())

    start_task = subprocess.run(
        [sys.executable, str(cli), "--project-root", str(workspace), "workflow", "start-task", "--command", "webnovel-write", "--chapter", "1"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert start_task.returncode == 0, start_task.stderr

    start_step = subprocess.run(
        [sys.executable, str(cli), "--project-root", str(workspace), "workflow", "start-step", "--step-id", "Step 1", "--step-name", "Context"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert start_step.returncode == 0, start_step.stderr

    complete_step = subprocess.run(
        [
            sys.executable,
            str(cli),
            "--project-root",
            str(workspace),
            "workflow",
            "complete-step",
            "--step-id",
            "Step 1",
            "--artifacts",
            '{"state_json_modified":true}',
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert complete_step.returncode == 0, complete_step.stderr

    workflow_state = project_root / ".webnovel" / "workflow_state.json"
    assert workflow_state.is_file()
    state = json.loads(workflow_state.read_text(encoding="utf-8"))
    assert state.get("current_task") is not None
    assert state["current_task"]["completed_steps"][-1]["id"] == "Step 1"

    registry_path = home / ".codex" / "webnovel-writer" / "workspaces.json"
    assert registry_path.is_file()
