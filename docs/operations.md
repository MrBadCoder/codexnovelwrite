# 项目结构与运维（Codex 运行时）

## 目录层级（推荐）

在 Codex 本地脚本模式下，建议区分 4 层：

1. `WORKSPACE_ROOT`（你的工作区根）
2. `PROJECT_ROOT`（真实小说项目根，包含 `.webnovel/state.json`）
3. `WEBNOVEL_RUNTIME_ROOT`（运行时代码根，默认 `~/.codex/webnovel-writer/runtime`）
4. `~/.codex/webnovel-writer/`（用户级配置与 registry）

### A) 工作区与书项目

```text
workspace-root/
├── 小说A/
│   ├── .webnovel/
│   ├── 正文/
│   ├── 大纲/
│   └── 设定集/
├── 小说B/
└── ...
```

### B) 运行时目录

```text
${WEBNOVEL_RUNTIME_ROOT}/
├── agents/
├── skills/
├── scripts/
├── references/
└── dashboard/
```

### C) 用户级配置目录

```text
~/.codex/webnovel-writer/
├── .env
└── workspaces.json
```

兼容读取（兜底）：

```text
~/.claude/webnovel-writer/
├── .env
└── workspaces.json
```

## 常用运维命令

统一前置：

```bash
export WEBNOVEL_WORKSPACE_ROOT="${WEBNOVEL_WORKSPACE_ROOT:-$PWD}"
export WEBNOVEL_RUNTIME_ROOT="${WEBNOVEL_RUNTIME_ROOT:-$HOME/.codex/webnovel-writer/runtime}"
export SCRIPTS_DIR="${WEBNOVEL_RUNTIME_ROOT}/scripts"
export PROJECT_ROOT="$(python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WEBNOVEL_WORKSPACE_ROOT}" where)"
```

### 索引重建

```bash
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index process-chapter --chapter 1
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index stats
```

### 健康报告

```bash
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus all
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus urgency
```

### 向量重建

```bash
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag index-chapter --chapter 1
python3 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag stats
```

### 测试入口

```bash
pwsh "${WEBNOVEL_RUNTIME_ROOT}/scripts/run_tests.ps1" -Mode smoke
pwsh "${WEBNOVEL_RUNTIME_ROOT}/scripts/run_tests.ps1" -Mode full
```

## Claude 双栈兼容说明

- 若你仍使用 Claude 插件，可继续沿用旧工作流。
- 当前迁移策略是 Codex 优先、Claude 兼容读取，不会主动删除旧 `.claude` 数据。
