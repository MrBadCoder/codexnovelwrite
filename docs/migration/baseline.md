# Codex Migration Baseline (P0)

- Date: 2026-03-05
- Workspace: `/Users/liuxiangmiao/.config/superpowers/worktrees/codexnovelwrite/codex-migrate-runtime`
- Target repo: `https://github.com/MrBadCoder/codexnovelwrite.git`
- Upstream source: `https://github.com/lingfengQAQ/webnovel-writer`
- Baseline commit: `af21db4580fec34ab69cf5e646c14a96dc30d7a2`
- Migration branch: `codex/migrate-runtime`

## Captured Artifacts

- Structure snapshot: `docs/migration/baseline-structure.txt`
- CLI smoke output: `docs/migration/smoke-baseline.md`
- Test collection baseline: `docs/migration/pytest-baseline.txt`

## Baseline Smoke Command

```bash
python3 webnovel-writer/scripts/webnovel.py --help
```

Result: exit code `0`, command list is printed as expected (where/use/index/state/rag/.../init/extract-context).

## Baseline Test Command

```bash
pytest -q
```

Result: exit code `2` with upstream pre-existing test collection errors.

Main issue observed:
- `ModuleNotFoundError: No module named 'runtime_compat'`
- Triggered while importing `webnovel-writer/scripts/security_utils.py` during test collection.

This baseline failure is recorded as upstream behavior prior to Codex runtime migration changes.
