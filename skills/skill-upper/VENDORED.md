# Vendored: skill-upper (skill-up evaluation skill)

> 本目录是**外部技能快照**，vendored 进 skill-spec 仅供项目内评测工作流直接读取与复用其方法论。遵守 `EXTERNAL_SNAPSHOT_POLICY.md`：保留最小可决策内容、标注来源、不当作已被验证的产物。

## 来源

- **源技能**：`~/.agents/skills/skill-upper`（Agent Skill：skill-up CLI 评测）
- **上游**：Alibaba skill-up —— <https://alibaba.github.io/skill-up/> · GitHub <https://github.com/alibaba/skill-up>
- **vendored 日期**：2026-09-21
- **对应 CLI 版本**：skill-up `0.12.0`（本机 `~/.local/bin/skill-up`）

## 用途（在本项目内的角色）

- 提供 `skill-up` CLI 评测的**方法论与命令参考**：`SKILL.md` 主流程、`references/*.md`（install / cli / eval-yaml / case-yaml / judge-types / migrate-anthropic）、`assets/*.tmpl` 模板（`eval.yaml.tmpl`、`case.yaml.tmpl`）、`evals/` 自评测示例。
- 项目内的实际评测入口是 `../scripts/skill_up.py`（封装 skill-up CLI，静态校验默认、模型运行需 `--execute`）。
- **评测对象**：本 skill-spec 的 eval 契约在 `../evals/eval.yaml` + `../evals/cases/`。

## 如何调用（一句话）

```bash
# 结构校验（默认，不消耗模型）
python3 scripts/skill_up.py validate .
# 真实模型评测（需 --execute 且本机有 skill-up）
python3 scripts/skill_up.py run . --execute --engine codex
```

完整用法见 `references/skill-up-integration.md`。

## 更新方式

替换此目录内容时：`cp -R ~/.agents/skills/skill-upper skills/skill-upper`，并更新上方日期与 CLI 版本；随后重跑 `python3 scripts/validate_skill_package.py .` 与 `python3 -m unittest discover -s tests` 确认契约仍在。