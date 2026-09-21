# Skill-up 集成规范

Skill-up 用于评测和回归，不是包结构检查的替代品。本项目将 **skill-upper**（skill-up CLI 评测技能）vendored 到 `skills/skill-upper/`，作为评测方法论与命令参考；实际评测入口统一走 `scripts/skill_up.py` 安全封装。

## 证据分层

| 阶段 | 命令 | 证据含义 |
|---|---|---|
| 静态包 | `validate_skill_package.py` | 工件与本地约束正确 |
| Eval 结构 | `skill_up.py validate <skill>` | 外部 CLI 可用时验证 eval schema；不可用时明确 `NOT_INSTALLED` |
| 运行时 | `skill_up.py run <skill> --execute` | 指定引擎、数据、版本和输出目录下的真实观测 |

运行产物必须位于项目根 `.skill-up-workspaces/`，不得污染 Skill 包。不得在没有显式 `--execute` 的情况下触发模型调用。

## 1. 安装 skill-up CLI

`skill-up` 是 Alibaba 出品的预编译单二进制，仅支持 **macOS / Linux**：

```bash
# 官方安装脚本 → 默认装到 ~/.local/bin/skill-up
curl -fsSL https://raw.githubusercontent.com/alibaba/skill-up/main/install.sh | bash

# 固定版本
export SKILL_UP_VERSION=v0.1.0
curl -fsSL https://raw.githubusercontent.com/alibaba/skill-up/main/install.sh | bash
```

验证：

```bash
command -v skill-up && skill-up --version   # 本机实测: 0.12.0
```

若 `command not found`：把 `~/.local/bin` 加入 PATH（macOS/Linux 见 `skills/skill-upper/references/install.md`）；macOS 拦截时 `xattr -d com.apple.quarantine "$(which skill-up)"`。手动下载 / 代理 / 源码构建排错均见该文件。

## 2. 调用方式（统一通过安全适配器）

项目内推荐通过 `scripts/skill_up.py` 调用，它先跑包契约，再调外部 CLI，且**默认不做模型调用**：

```bash
# 结构校验：先 validate_skill_package，再 validate eval schema
python3 scripts/skill_up.py validate <skill-dir>

# 真实模型评测：必须 --execute（会消耗模型资源）
python3 scripts/skill_up.py run <skill-dir> --execute [--engine codex]

# 不传 --execute 直接 run → REFUSED(2)
```

| 情况 | 行为 | 退出码 |
|---|---|---|
| CLI 缺失 + `validate` | 打印 `SKILL_UP_NOT_INSTALLED`（静态检查已过） | 0 |
| `run` 无 `--execute` | `REFUSED: ... requires --execute` | 2 |
| `run --execute` + CLI 缺失 | `SKILL_UP_NOT_INSTALLED` | 2 |
| `run --execute` | 跑真实评测到 `.skill-up-workspaces/<name>/` | 0/1 |

### 直接调 skill-up（超越适配器时）

完整命令与 flags 见 `skills/skill-upper/references/cli.md`。核心：

```bash
skill-up validate evals/eval.yaml                 # schema 校验
skill-up list-cases evals/eval.yaml               # 列出用例
skill-up run evals/eval.yaml --engine codex       # 运行（输出到工作区）
skill-up run evals/eval.yaml --include-case-name "basic-*"
skill-up run evals/eval.yaml --format html --format junit
skill-up run evals/eval.yaml --iteration 3        # 稳定性/flakiness 采样
skill-up report result.json --format html         # 重生成报告，不重跑
skill-up import <evals.json>                      # Anthropic 格式迁移
```

退出码：`0` = 全部通过，`1` = 有失败/错误（可作 CI 门禁）。

## 3. 如何评测一个 Skill（step-by-step）

1. **确认 CLI**：`skill-up --version`（缺失则执行第 1 节安装）。
2. **定位目标 Skill**：含 `SKILL.md` 的目录；读其 `SKILL.md` 了解 scope / triggers。
3. **确认 evals**：
   - `evals/eval.yaml` 存在 → 直接跑；
   - `evals/evals.json`（Anthropic）→ `skill-up import` 或 `skill-up run --auto`；
   - 无 evals → 用 `skills/skill-upper/assets/*.tmpl` 脚手架（`eval.yaml.tmpl` + `case.yaml.tmpl`）。
4. **校验 schema**：`python3 scripts/skill_up.py validate <dir>`（或 `skill-up validate <dir>/evals/eval.yaml`），期望 `✓ eval.yaml is valid (loaded N case(s))`。
5. **准备凭据**：优先 `--api-key` > `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` 等环境变量 > `~/.skill-up/credentials.yaml`；缺失则停下询问，**不把密钥写进 YAML**。
6. **运行**：`python3 scripts/skill_up.py run <dir> --execute --engine codex`。
7. **读报告**：产物在 `<skill-name>-workspace/iteration-N/` 下 `result.json` / `benchmark.json` / `report.html` 与各 case 的 `grading.json`；关注 pass rate、失败 case 的 assertion `text` 与 `evidence`。
8. **按需演化**：仅当用户要求修复/改进时才进入迭代循环——诊断失败 → 改 `SKILL.md`/补 case → 先重跑失败项再全量。不削弱有效断言去凑通过。

## 4. Judge 与模板速查

- `judge.type`：`rule_based`（首选）< `script` < `agent_judge`（昂贵）。语义判断用 `agent_judge`，需显式 `model` 与 `criteria`、可设 `pass_threshold`。
- 多轮对话用 `input.turns`（含 `post_condition` / `capture`），单轮用 `input.prompt`。
- 细节：`skills/skill-upper/references/eval-yaml.md`（eval schema）、`case-yaml.md`（case 字段）、`judge-types.md`（评判策略）。
- 模板：`skills/skill-upper/assets/eval.yaml.tmpl`、`case.yaml.tmpl`。

## 5. vendored 来源说明

`skills/skill-upper/` 是 `~/.agents/skills/skill-upper` 的完整快照，vendored 日期 2026-09-21，对应 skill-up `0.12.0`。上游 <https://github.com/alibaba/skill-up>。见 `skills/skill-upper/VENDORED.md`。更新方式：`cp -R ~/.agents/skills/skill-upper skills/skill-upper` 后重跑 validator + tests。