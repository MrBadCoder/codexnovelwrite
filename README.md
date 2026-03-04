# Webnovel Writer

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Codex](https://img.shields.io/badge/Codex-Ready-1f6feb.svg)](https://github.com/openai/codex)

## 项目简介

`Webnovel Writer` 是面向长篇连载创作的工程化写作系统，目标是降低 AI 写作中的遗忘与幻觉，支持“初始化 → 规划 → 写作 → 审查 → 回写 → 恢复”的完整链路。

当前推荐运行时：**Codex 本地脚本模式**（不依赖插件市场）。

详细文档：
- 架构与模块：`docs/architecture.md`
- 命令详解：`docs/commands.md`
- RAG 与配置：`docs/rag-and-config.md`
- 题材模板：`docs/genres.md`
- 运维与恢复：`docs/operations.md`
- 文档导航：`docs/README.md`

## 快速开始（Codex 推荐）

### 1) 克隆仓库

```bash
git clone https://github.com/MrBadCoder/codexnovelwrite.git
cd codexnovelwrite
```

### 2) 安装依赖并创建启动器

```bash
bash scripts/install_codex.sh
```

默认会：
- 安装 Python 依赖
- 将运行时目录链接到 `~/.codex/webnovel-writer/runtime`
- 生成全局命令 `~/.local/bin/webnovel`

### 3) 初始化项目

```bash
webnovel init -- project-root 小说名 题材
```

或先绑定已有项目：

```bash
webnovel use /path/to/your/book-project
webnovel where
```

### 4) 配置 RAG 环境（必做）

在书项目根目录创建 `.env`（建议每本书单独配置）：

```bash
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_embed_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_rerank_api_key
```

### 5) 开始创作链路

```bash
webnovel plan -- 1
webnovel write -- 1
webnovel review -- 1-5
```

## 运行时变量（Codex）

- `WEBNOVEL_RUNTIME_ROOT`：运行时根目录（默认 `~/.codex/webnovel-writer/runtime`）
- `WEBNOVEL_WORKSPACE_ROOT`：工作区根目录（可选，优先于旧变量）
- `CODEX_HOME`：Codex 用户目录（可作为 runtime root 推断来源）

兼容变量（可选）：
- `CLAUDE_PROJECT_DIR`
- `CLAUDE_HOME`
- `WEBNOVEL_CLAUDE_HOME`

## Claude 兼容模式（可选）

如果你仍在 Claude Plugin 工作流中使用本项目，可继续沿用原有命令；迁移建议见 `docs/operations.md`。

## 更新简介

| 版本 | 说明 |
|------|------|
| **v5.5.0 (当前)** | 新增只读可视化 Dashboard Skill（`/webnovel-dashboard`）与实时刷新能力 |
| **v5.4.4** | Plugin Marketplace 安装机制与统一 CLI 调用 |
| **v5.3** | 追读力系统（Hook / Cool-point / 微兑现 / 债务追踪） |

## 开源协议

本项目使用 `GPL v3` 协议，详见 `LICENSE`。

## 致谢

本项目使用 Claude Code + Gemini CLI + Codex 协作开发。
