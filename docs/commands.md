# 命令详解

## Codex 终端命令（推荐）

统一入口：

```bash
webnovel <子命令> [参数]
```

### `webnovel where`

用途：解析并打印当前实际 `PROJECT_ROOT`。

```bash
webnovel where
```

### `webnovel use <project_root>`

用途：绑定当前工作区使用的书项目（写指针/registry）。

```bash
webnovel use /path/to/book-project
webnovel use /path/to/book-project --workspace-root /path/to/workspace
```

### `webnovel init ...`

用途：初始化小说项目（目录、设定模板、状态文件）。

```bash
webnovel init -- /path/to/workspace 小说名 题材
```

### `webnovel plan ...`

用途：生成卷级规划与节拍。

```bash
webnovel plan -- 1
webnovel plan -- 2-3
```

### `webnovel write ...`

用途：执行章节创作流水线（上下文 → 草稿 → 审查 → 数据回写）。

```bash
webnovel write -- 1
webnovel write -- 45
webnovel write -- 45 --fast
webnovel write -- 45 --minimal
```

### `webnovel review ...`

用途：对章节进行多维质量审查。

```bash
webnovel review -- 1-5
webnovel review -- 45
```

### `webnovel query ...`

用途：查询角色、伏笔、节奏、状态等运行时信息。

```bash
webnovel query -- 萧炎
webnovel query -- 伏笔
webnovel query -- 紧急
```

### `webnovel workflow ...`

用途：工作流状态管理（中断检测、恢复、清理）。

```bash
webnovel workflow detect
webnovel workflow clear
webnovel workflow cleanup --chapter 12 --confirm
```

### `webnovel context/index/state/rag ...`

用途：底层模块透传调用。

```bash
webnovel context -- --chapter 12
webnovel index -- stats
webnovel state -- dump
webnovel rag -- stats
```

## Claude Slash 命令（兼容）

如果你在 Claude 插件工作流中，仍可使用：

- `/webnovel-init`
- `/webnovel-plan [卷号]`
- `/webnovel-write [章号]`
- `/webnovel-review [范围]`
- `/webnovel-query [关键词]`
- `/webnovel-resume`
- `/webnovel-dashboard`
