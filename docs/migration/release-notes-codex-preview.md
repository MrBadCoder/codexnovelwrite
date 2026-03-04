# Codex Preview Release Notes

- Release date: 2026-03-05
- Release tag: `codex-preview`
- Base branch: `master`

## Highlights

- Migrated runtime model to Codex-first resolution (`.codex` first, `.claude` fallback).
- Unified CLI entrypoints and command mapping for Codex terminal usage.
- Decoupled workflow manager from Claude-specific runtime assumptions.
- Migrated core skills and agents documentation semantics to Codex tooling.
- Added Codex install/runtime docs and migration guides.
- Added Codex runtime regression tests and e2e/compatibility reports.

## Key Changes

- Runtime/config/project pointer compatibility:
  - `webnovel-writer/scripts/data_modules/runtime_paths.py`
  - `webnovel-writer/scripts/data_modules/config.py`
  - `webnovel-writer/scripts/project_locator.py`
- CLI/runtime entrypoints:
  - `webnovel-writer/scripts/webnovel.py`
  - `webnovel-writer/scripts/data_modules/webnovel.py`
  - `bin/webnovel`
- Docs and migration reports:
  - `README.md`
  - `docs/commands.md`
  - `docs/operations.md`
  - `docs/rag-and-config.md`
  - `docs/migration/e2e-report.md`
  - `docs/migration/compatibility-report.md`
  - `docs/migration/claude-to-codex-guide.md`

## Validation

- Automated:
  - `PYTHONPATH=webnovel-writer/scripts pytest -q -o addopts='' webnovel-writer/scripts/data_modules/tests/test_project_locator.py webnovel-writer/scripts/data_modules/tests/test_context_manager.py webnovel-writer/scripts/data_modules/tests/test_extract_chapter_context.py webnovel-writer/scripts/data_modules/tests/test_codex_runtime_e2e.py`
  - Result: `39 passed`
- Manual:
  - E2E and compatibility logs captured under `/tmp/webnovel-codex-e2e-task10`

## Upgrade Notes

- Existing `.claude` project pointers and user config remain readable.
- Recommended runtime/user config path is now under `~/.codex/webnovel-writer/`.
- Command workflows continue to support dual-stack transition during migration period.
