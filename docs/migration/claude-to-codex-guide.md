# Claude -> Codex Migration Guide (Task 11)

- Date: 2026-03-05
- Target branch: `codex/migrate-runtime`
- Preview tag: `codex-preview`

## 1. Migration Goal

把运行时从 Claude 插件目录迁移到 Codex 本地运行方式，同时保持老项目可读、可续写、可恢复。

## 2. Directory and Config Migration

### Runtime root

- New recommended root: `~/.codex/webnovel-writer/runtime`
- Legacy fallback root: `~/.claude/webnovel-writer/runtime`（可继续保留）

### User config

- New preferred config: `~/.codex/webnovel-writer/.env`
- Legacy fallback config: `~/.claude/webnovel-writer/.env`

配置优先级：

1. 进程环境变量  
2. 项目根 `.env`  
3. `~/.codex/webnovel-writer/.env`  
4. `~/.claude/webnovel-writer/.env`

## 3. Project Pointer Migration

当前支持的项目指针文件：

- `.codex/.webnovel-current-project`（优先）
- `.claude/.webnovel-current-project`（兼容）

建议迁移步骤：

1. 在工作区创建 `.codex/` 目录。
2. 使用 `webnovel use <project_root> --workspace-root <workspace_root>` 重写当前项目指针。
3. 用 `webnovel where` 校验指针是否生效。

## 4. Command Mapping

### 4.1 Claude 习惯命令到 Codex 语义

| Claude slash command | Codex 等价语义 |
|---|---|
| `/webnovel-init` | `webnovel init -- <project_dir> <title> <genre>` |
| `/webnovel-plan` | skills/workflow 规划链路（当前非直接 CLI 子命令） |
| `/webnovel-write` | skills/workflow 写作链路（当前非直接 CLI 子命令） |
| `/webnovel-review` | `webnovel status -- --focus ...` + skills review 语义 |
| `/webnovel-query` | `webnovel context/index/state/rag ...` 查询链路 |
| `/webnovel-resume` | `webnovel workflow detect/clear/...` |
| `/webnovel-dashboard` | dashboard 相关服务脚本（按部署文档） |

### 4.2 推荐 Codex CLI 基础链路

```bash
webnovel init -- /path/to/book 小说名 xuanhuan
webnovel use /path/to/book --workspace-root /path/to/workspace
webnovel where
webnovel context -- --chapter 1
webnovel workflow detect
```

## 5. Rollback Plan

如果切换后需快速回退到旧行为：

1. 保留/恢复 `.claude/.webnovel-current-project` 指针。
2. 恢复 `~/.claude/webnovel-writer/.env` 为主配置。
3. 将运行时脚本入口切回旧目录（如你的原 Claude 运行路径）。
4. 使用 `webnovel where` + `webnovel workflow detect` 验证恢复状态。

说明：当前迁移实现是双栈兼容，不会主动删除 `.claude` 数据。
