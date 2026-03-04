# Webnovel Writer Codex Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不改写核心写作逻辑的前提下，把 `webnovel-writer` 从 Claude 插件运行方式迁移为 Codex 可独立运行，并保持核心链路功能等价。

**Architecture:** 采用“兼容层优先”的迁移方式：先冻结基线并建立对照，再引入运行时路径/配置兼容层，随后迁移 CLI、Skills/Agents 语义，最后补齐文档安装与回归发布。整个过程保持双栈兜底（`.codex` 优先，`.claude` 兼容）以降低切换风险。

**Tech Stack:** Python CLI、Markdown 文档、Shell 脚本、pytest、SQLite（现有数据链）。

---

## 执行前提

- 目标仓库根目录：`webnovel-writer/`
- 上游基线 commit：`af21db4580fec34ab69cf5e646c14a96dc30d7a2`
- 当前计划文件：`docs/plans/2026-03-05-codex-migration-execution.md`

### Task 1: 基线冻结与对照基准（P0）

**Files:**
- Create: `docs/migration/baseline.md`
- Create: `docs/migration/smoke-baseline.md`
- Modify: `codex-migration-checklist.md`

**Step 1: 锁定上游基线并创建分支**
Run: `git checkout -b codex/migrate-runtime`
Expected: `Switched to a new branch 'codex/migrate-runtime'`

**Step 2: 记录目录结构快照**
Run: `find skills agents scripts references -maxdepth 3 -type f | sort > docs/migration/baseline-structure.txt`
Expected: 快照文件生成且非空。

**Step 3: 运行原逻辑冒烟并保存结果**
Run: `python scripts/webnovel.py --help > docs/migration/smoke-baseline.md`
Expected: 输出包含子命令帮助。

**Step 4: 写入基线文档**
- 在 `docs/migration/baseline.md` 记录 commit、执行环境、命令与输出摘要。

**Step 5: Commit**
Run:
```bash
git add docs/migration/baseline.md docs/migration/baseline-structure.txt docs/migration/smoke-baseline.md
git commit -m "chore: freeze migration baseline for codex runtime"
```

### Task 2: 运行时路径兼容层（P1-环境变量与目录）

**Files:**
- Create: `scripts/data_modules/runtime_paths.py`
- Modify: `scripts/data_modules/config.py`
- Test: `tests/test_runtime_paths.py`

**Step 1: 先写失败测试（优先级与兜底）**
- 覆盖：`CODEX_HOME` 优先、`WEBNOVEL_RUNTIME_ROOT` 覆盖、`.claude` 回退。

**Step 2: 运行单测确认失败**
Run: `pytest tests/test_runtime_paths.py -q`
Expected: FAIL（缺少实现或优先级不符）。

**Step 3: 最小实现 `runtime_paths.py`**
- 提供：`get_runtime_root()`、`get_workspace_root()`、`get_user_config_dir()`。

**Step 4: 接入 `config.py` 搜索链路**
- 实现优先级：进程环境 > 项目 `.env` > `~/.codex/webnovel-writer/.env` > `~/.claude/...`。

**Step 5: 重跑测试验证通过**
Run: `pytest tests/test_runtime_paths.py -q`
Expected: PASS。

**Step 6: Commit**
Run:
```bash
git add scripts/data_modules/runtime_paths.py scripts/data_modules/config.py tests/test_runtime_paths.py
git commit -m "feat: add codex-first runtime path resolution"
```

### Task 3: 项目定位与指针兼容（P1-定位）

**Files:**
- Modify: `scripts/project_locator.py`
- Test: `tests/test_project_locator.py`

**Step 1: 写失败测试**
- 覆盖：`.codex/.webnovel-current-project` 读取。
- 覆盖：`.claude/.webnovel-current-project` 兼容回退。
- 覆盖：`where/use` 输出一致性。

**Step 2: 运行测试确认失败**
Run: `pytest tests/test_project_locator.py -q`
Expected: FAIL。

**Step 3: 最小改造 `project_locator.py`**
- 按优先级读取指针并统一错误提示。

**Step 4: 重跑测试**
Run: `pytest tests/test_project_locator.py -q`
Expected: PASS。

**Step 5: Commit**
Run:
```bash
git add scripts/project_locator.py tests/test_project_locator.py
git commit -m "feat: support codex project pointer with claude fallback"
```

### Task 4: CLI 入口与命令映射（P2）

**Files:**
- Modify: `scripts/webnovel.py`
- Modify: `scripts/data_modules/webnovel.py`
- Create: `bin/webnovel`（如已有则修改）
- Test: `tests/test_cli_commands.py`

**Step 1: 写失败测试**
- 覆盖命令：`where/use/init/context/index/state/rag`。

**Step 2: 运行测试确认失败**
Run: `pytest tests/test_cli_commands.py -q`
Expected: FAIL。

**Step 3: 保持双入口并统一参数解析**
- 两个入口行为一致，错误码一致。

**Step 4: 增加本地启动器**
- `bin/webnovel` 调用 Python 主入口，支持 `chmod +x` 直接运行。

**Step 5: 重跑测试**
Run: `pytest tests/test_cli_commands.py -q`
Expected: PASS。

**Step 6: Commit**
Run:
```bash
git add scripts/webnovel.py scripts/data_modules/webnovel.py bin/webnovel tests/test_cli_commands.py
git commit -m "feat: align codex cli entrypoints and command mapping"
```

### Task 5: workflow_manager 脱离 Claude 专属上下文（P2）

**Files:**
- Modify: `scripts/workflow_manager.py`
- Test: `tests/test_workflow_manager.py`

**Step 1: 写失败测试**
- 覆盖：`start-task/start-step/complete-step` 在纯终端环境可运行。

**Step 2: 运行测试确认失败**
Run: `pytest tests/test_workflow_manager.py -q`
Expected: FAIL。

**Step 3: 最小改造实现**
- 移除对 Claude 会话上下文的隐式依赖，改为显式参数/本地状态。

**Step 4: 重跑测试**
Run: `pytest tests/test_workflow_manager.py -q`
Expected: PASS。

**Step 5: Commit**
Run:
```bash
git add scripts/workflow_manager.py tests/test_workflow_manager.py
git commit -m "refactor: decouple workflow manager from claude-specific context"
```

### Task 6: Skills 语义迁移（P3-第一批核心技能）

**Files:**
- Modify: `skills/webnovel-init/SKILL.md`
- Modify: `skills/webnovel-plan/SKILL.md`
- Modify: `skills/webnovel-write/SKILL.md`
- Modify: `skills/webnovel-review/SKILL.md`
- Modify: `skills/webnovel-query/SKILL.md`
- Modify: `skills/webnovel-resume/SKILL.md`
- Modify: `skills/webnovel-dashboard/SKILL.md`

**Step 1: 扫描私有工具语义**
Run: `rg -n "\b(Task|AskUserQuestion|WebSearch|WebFetch)\b" skills/*/SKILL.md`
Expected: 输出待迁移位置列表。

**Step 2: 按映射替换语义**
- `Task` → Codex 子流程（串/并行脚本）。
- `AskUserQuestion` → 普通交互问答。
- `WebSearch/WebFetch` → Codex Web 工具。

**Step 3: 自检无遗漏**
Run: `rg -n "\b(Task|AskUserQuestion|WebSearch|WebFetch)\b" skills/webnovel-*/SKILL.md`
Expected: 仅保留被允许的说明文本，无旧依赖描述。

**Step 4: Commit**
Run:
```bash
git add skills/webnovel-*/SKILL.md
git commit -m "docs: migrate core webnovel skills semantics for codex"
```

### Task 7: Agents 执行语义迁移（P3-Agents）

**Files:**
- Modify: `agents/*.md`

**Step 1: 扫描 Claude 假设**
Run: `rg -n "CLAUDE_PLUGIN_ROOT|Claude" agents/*.md`
Expected: 输出所有待迁移行。

**Step 2: 统一变量与描述**
- `CLAUDE_PLUGIN_ROOT` → `WEBNOVEL_RUNTIME_ROOT`。
- 保留 `model: inherit` 思路，删除 Claude 特定枚举。

**Step 3: 复扫确认**
Run: `rg -n "CLAUDE_PLUGIN_ROOT" agents/*.md`
Expected: 无结果。

**Step 4: Commit**
Run:
```bash
git add agents/*.md
git commit -m "docs: migrate agents runtime assumptions to codex"
```

### Task 8: 文档与安装改造（P4）

**Files:**
- Modify: `README.md`
- Modify: `docs/operations.md`
- Modify: `docs/commands.md`
- Modify: `docs/rag-and-config.md`
- Create: `scripts/install_codex.sh`

**Step 1: 写 Codex 安装与启动章节**
- 覆盖本地安装、升级、双栈兼容说明。

**Step 2: 更新命令示例**
- 增加 `where -> use -> init -> write` 端到端示例。

**Step 3: 新增安装脚本并赋权**
Run: `chmod +x scripts/install_codex.sh`
Expected: 脚本可直接执行。

**Step 4: Commit**
Run:
```bash
git add README.md docs/operations.md docs/commands.md docs/rag-and-config.md scripts/install_codex.sh
git commit -m "docs: add codex install and runtime usage guide"
```

### Task 9: 自动化测试与无 .claude 场景回归（P5）

**Files:**
- Modify: `tests/test_project_locator.py`
- Modify: `tests/test_context_manager.py`
- Modify: `tests/test_extract_context.py`
- Create: `tests/test_codex_runtime_e2e.py`

**Step 1: 为 Codex 场景补充失败测试**
- 无 `.claude` 目录条件下完成定位与写作流程。

**Step 2: 执行目标测试集**
Run: `pytest tests/test_project_locator.py tests/test_context_manager.py tests/test_extract_context.py tests/test_codex_runtime_e2e.py -q`
Expected: 全部 PASS。

**Step 3: Commit**
Run:
```bash
git add tests/test_project_locator.py tests/test_context_manager.py tests/test_extract_context.py tests/test_codex_runtime_e2e.py
git commit -m "test: cover codex runtime scenarios without claude directory"
```

### Task 10: 手工端到端回归与兼容性记录（P5）

**Files:**
- Create: `docs/migration/e2e-report.md`
- Create: `docs/migration/compatibility-report.md`

**Step 1: 场景 A（新项目）**
Run: `webnovel init ... && webnovel plan ... && webnovel write ...`
Expected: 链路完成且状态文件更新。

**Step 2: 场景 B（续写）**
Run: `webnovel where && webnovel use <project_root> && webnovel write ... && webnovel review ...`
Expected: 续写与评审可用。

**Step 3: 场景 C（恢复）**
Run: `webnovel resume ...`
Expected: 中断恢复成功。

**Step 4: 兼容性验证**
- Windows 空格路径。
- macOS/Linux 路径。
- 旧 `.claude` 数据可读。

**Step 5: Commit**
Run:
```bash
git add docs/migration/e2e-report.md docs/migration/compatibility-report.md
git commit -m "test: add e2e and compatibility migration reports"
```

### Task 11: 发布与迁移切换（P6）

**Files:**
- Create: `docs/migration/claude-to-codex-guide.md`
- Modify: `CHANGELOG.md`（若存在）

**Step 1: 编写迁移指南**
- 包含配置迁移、指针迁移、命令对照表、回滚方案。

**Step 2: 发布预览标签**
Run: `git tag codex-preview`
Expected: `codex-preview` 标签存在。

**Step 3: 提交发布文档**
Run:
```bash
git add docs/migration/claude-to-codex-guide.md CHANGELOG.md || true
git commit -m "release: prepare codex preview migration guide"
```

---

## 顺序与依赖

1. `Task 1` 必须先完成（基线对照）。
2. `Task 2-3` 完成后再做 `Task 4-5`（CLI/工作流依赖运行时兼容）。
3. `Task 6-7` 可在 `Task 4-5` 后并行。
4. `Task 8` 在语义迁移后执行，避免文档反复改。
5. `Task 9-10` 必须在全部代码改造后执行。
6. `Task 11` 仅在 `Task 9-10` 全绿后执行。

## 每日执行节奏（建议）

- Day 1: `Task 1-3`
- Day 2: `Task 4-5`
- Day 3: `Task 6-8`
- Day 4: `Task 9-10`
- Day 5: `Task 11`

## DoD 对齐检查

- 不依赖 Claude Plugin 安装机制。
- Codex 终端可独立跑通 `where -> init -> write` 主链路。
- 文档、脚本、配置路径一致。
- 老项目数据可读、可续写、可恢复。
