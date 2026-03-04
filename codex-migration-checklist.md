# webnovel-writer → Codex 迁移清单（v1）

更新时间：2026-03-05
目标仓库：`https://github.com/MrBadCoder/codexnovelwrite.git`

---

## 0. 迁移目标与边界

- [ ] 明确迁移目标：**Codex 下功能等价**（非 Claude 插件机制 1:1 复制）
- [ ] 保留核心能力：`init / plan / write / review / query / resume / dashboard`
- [ ] 保留核心数据链：`.webnovel/state.json + index.db + vectors.db + summaries`
- [ ] 约束：不先改写作逻辑，只做“运行时/工具链/安装方式”适配

---

## 1. 基线冻结（P0）

- [x] 锁定上游基线 commit（建议记录：`af21db4580fec34ab69cf5e646c14a96dc30d7a2`）
- [x] 建立迁移分支：`codex/migrate-runtime`
- [x] 记录上游结构快照：`skills/`、`agents/`、`scripts/`、`references/`
- [x] 先跑一轮基线冒烟（在原逻辑下）并保存结果

**验收标准**
- [x] 可复现“上游当前行为”作为对照基准

---

## 2. 运行时兼容层（P1）

### 2.1 环境变量与目录抽象
- [ ] 新增统一运行时变量（建议）：`WEBNOVEL_RUNTIME_ROOT`、`WEBNOVEL_WORKSPACE_ROOT`
- [ ] 支持 Codex 环境优先（如 `CODEX_HOME`/当前工作区），并兼容旧 `CLAUDE_*`
- [ ] 将用户级配置目录扩展为：`~/.codex/webnovel-writer/`（保留 `~/.claude/...` 兜底）

### 2.2 指针与项目定位
- [ ] 改造 `webnovel-writer/scripts/project_locator.py`：支持 `.codex/.webnovel-current-project`
- [ ] 保留 `.claude/.webnovel-current-project` 兼容读取
- [ ] `where/use` 命令输出统一、可追踪

### 2.3 配置加载
- [ ] 改造 `webnovel-writer/scripts/data_modules/config.py`：新增 Codex 全局 `.env` 搜索路径
- [ ] 明确优先级：进程环境 > 项目 `.env` > `~/.codex/webnovel-writer/.env` > 旧路径兜底

**验收标准**
- [ ] 在无 `.claude` 目录时也能正确定位项目并运行 CLI

---

## 3. CLI 与脚本入口适配（P2）

### 3.1 统一入口
- [ ] 保留 `webnovel-writer/scripts/webnovel.py` 与 `data_modules/webnovel.py` 双入口
- [ ] 去除文档中的“必须 Claude Plugin”假设，改为“本地脚本可直接调用”

### 3.2 命令映射
- [ ] 定义 Codex 侧命令映射（示例）：
  - `webnovel where`
  - `webnovel use <project_root>`
  - `webnovel init ...`
  - `webnovel context/index/state/rag ...`
- [ ] 视需要补充 `Makefile` / `npm scripts` / `bin/webnovel` 启动器

### 3.3 工作流恢复
- [ ] 验证 `workflow_manager.py` 在 Codex 会话中可独立工作
- [ ] 保证 `start-task/start-step/complete-step` 不依赖 Claude 专属上下文

**验收标准**
- [ ] 使用终端命令可完成 `where -> init -> write链路` 的核心步骤

---

## 4. Skills/Agents 语义迁移（P3）

### 4.1 Skills frontmatter/tool 映射
- [ ] 批量扫描 `webnovel-writer/skills/*/SKILL.md`
- [ ] 工具语义映射：
  - `Read/Write/Edit/Grep/Bash` → 保留
  - `Task` → 改为 Codex 子流程（串行/并行脚本调用）
  - `AskUserQuestion` → 改为普通交互提问
  - `WebSearch/WebFetch` → 改为 Codex Web 工具调用

### 4.2 Agents 执行语义
- [ ] 扫描 `webnovel-writer/agents/*.md` 中 `CLAUDE_PLUGIN_ROOT` 假设
- [ ] 替换为统一变量（例如 `WEBNOVEL_RUNTIME_ROOT`）
- [ ] 保留 `model: inherit` 思路，但去除 Claude 特定枚举描述

### 4.3 优先迁移顺序（建议）
- [ ] `webnovel-init`
- [ ] `webnovel-plan`
- [ ] `webnovel-write`
- [ ] `webnovel-review`
- [ ] `webnovel-query`
- [ ] `webnovel-resume`
- [ ] `webnovel-dashboard`

**验收标准**
- [ ] 每个 Skill 在 Codex 中都有可执行替代流程（不依赖 Claude 私有工具）

---

## 5. 文档与安装方式改造（P4）

### 5.1 文档改造
- [ ] 更新 `README.md`：新增 Codex 安装与启动章节
- [ ] 更新 `docs/operations.md`：目录层级改为 Codex 运行时描述
- [ ] 更新 `docs/commands.md`：补充 Codex 命令调用示例
- [ ] 更新 `docs/rag-and-config.md`：补充 `~/.codex/webnovel-writer/.env`

### 5.2 安装流程
- [ ] 新增 Codex 安装脚本（示例：`scripts/install_codex.sh`）
- [ ] 明确“无插件市场”的本地安装路径与升级方式
- [ ] 保留可选 Claude 兼容模式（若你需要双栈）

**验收标准**
- [ ] 新用户按 README（Codex 路径）可在 15 分钟内跑通首个项目

---

## 6. 测试与回归（P5）

### 6.1 自动化测试
- [ ] 修复并执行 Python 测试（重点：`project_locator`、`context_manager`、`extract_context`）
- [ ] 增加 Codex 场景测试：无 `.claude` 前提下定位/写作流程

### 6.2 端到端回归（手工）
- [ ] 场景 A：全新项目（`init -> plan -> write`）
- [ ] 场景 B：已有项目续写（`where/use -> write -> review`）
- [ ] 场景 C：中断恢复（`workflow/resume`）

### 6.3 兼容性
- [ ] Windows 路径兼容（含空格路径）
- [ ] macOS/Linux 目录兼容
- [ ] 旧 `.claude` 用户数据不丢失

**验收标准**
- [ ] 关键链路回归通过率 100%，无阻断级错误

---

## 7. 发布与切换（P6）

- [ ] 发布 `codex-preview` 版本标签
- [ ] 提供迁移指南：Claude 用户如何迁移到 Codex（配置、指针、命令）
- [ ] 设定 1 个版本周期双栈兼容（可选）
- [ ] 收集反馈后再移除 Claude 专属依赖

**验收标准**
- [ ] 至少 2 个真实项目跑通完整写作链路

---

## 8. 高风险点清单（需优先盯防）

- [ ] 路径解析错误导致写到错误目录（尤其是 workspace 与 project_root 混淆）
- [ ] `Task` 语义替换不当导致审查/数据回写流程断裂
- [ ] 参考资料路径仍硬编码 `.claude/references`
- [ ] 全局 `.env` 冲突导致多项目串配置

---

## 9. 完成定义（DoD）

- [ ] 不依赖 Claude Plugin 安装机制
- [ ] Codex 终端可独立跑通核心链路
- [ ] 文档、脚本、配置路径与运行时一致
- [ ] 老项目数据可读、可续写、可恢复
