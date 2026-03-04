# GitHub Release Body (codex-preview)

Use this content when creating a GitHub Release for tag `codex-preview`.

## Title

`codex-preview: Codex-first runtime migration`

## Release Notes (CN)

本版本完成了 `webnovel-writer` 运行时从 Claude 插件假设到 Codex-first 模式的迁移收敛，目标是在不改写核心写作逻辑前提下，实现独立终端可运行与双栈兼容。

### 主要更新

- 引入 Codex-first 路径与配置解析：
  - `.codex` 优先
  - `.claude` 兼容回退
- 统一 CLI 入口与命令映射，降低参数与路径调用误差。
- `workflow_manager` 去除 Claude 专属上下文隐式依赖。
- 核心 skills/agents 文档语义迁移为 Codex 可执行描述。
- 新增 Codex 安装脚本与运行文档。
- 补齐回归测试与迁移报告（E2E + compatibility）。

### 兼容性说明

- 旧 `.claude` 指针与用户配置仍可读取。
- 推荐新路径：`~/.codex/webnovel-writer/`。
- 支持空格路径与跨平台路径场景。

### 验证结果

- 自动化回归：
  - `PYTHONPATH=webnovel-writer/scripts pytest -q -o addopts='' webnovel-writer/scripts/data_modules/tests/test_project_locator.py webnovel-writer/scripts/data_modules/tests/test_context_manager.py webnovel-writer/scripts/data_modules/tests/test_extract_chapter_context.py webnovel-writer/scripts/data_modules/tests/test_codex_runtime_e2e.py`
  - 结果：`39 passed`
- 手工回归日志：`/tmp/webnovel-codex-e2e-task10`

### 相关文档

- `docs/migration/release-notes-codex-preview.md`
- `docs/migration/e2e-report.md`
- `docs/migration/compatibility-report.md`
- `docs/migration/claude-to-codex-guide.md`

## Release Notes (EN, short)

This release finalizes a Codex-first runtime migration for `webnovel-writer` while preserving backward compatibility with existing `.claude` data paths.

### Highlights

- Codex-first runtime/config/project pointer resolution with Claude fallback.
- Unified CLI entrypoints and command mapping.
- Workflow manager decoupled from Claude-specific assumptions.
- Core skills/agents semantics migrated for Codex execution.
- Added install/runtime docs plus migration/e2e/compatibility reports.

### Validation

- Target regression suite passed (`39 passed`).
- Manual e2e and compatibility scenarios completed and documented.
