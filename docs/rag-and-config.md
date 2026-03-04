# RAG 与配置说明

## RAG 检索架构

```text
查询 → QueryRouter(auto) → vector / bm25 / hybrid / graph_hybrid
                     └→ RRF 融合 + Rerank → Top-K
```

默认模型：

- Embedding：`Qwen/Qwen3-Embedding-8B`
- Reranker：`jina-reranker-v3`

## 环境变量加载顺序

1. 进程环境变量（最高优先级）
2. 书项目根目录下的 `.env`
3. 用户级全局：`~/.codex/webnovel-writer/.env`
4. 兼容兜底：`~/.claude/webnovel-writer/.env`

说明：推荐每本书单独配置 `${PROJECT_ROOT}/.env`，避免多项目串配置。

## `.env` 最小配置

```bash
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_embed_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_rerank_api_key
```

## Codex 运行时变量

```bash
WEBNOVEL_RUNTIME_ROOT=~/.codex/webnovel-writer/runtime
WEBNOVEL_WORKSPACE_ROOT=/path/to/workspace
CODEX_HOME=~/.codex
```

兼容变量（可选）：

```bash
CLAUDE_PROJECT_DIR=/path/to/workspace
CLAUDE_HOME=~/.claude
WEBNOVEL_CLAUDE_HOME=~/.claude
```

## 常见回退行为

- 未配置 Embedding Key 时，语义检索会回退到 BM25。
- `WEBNOVEL_WORKSPACE_ROOT` 未设置时，默认使用当前目录。
- `.codex` 配置缺失时，会自动回退到 `.claude` 兼容目录读取。
