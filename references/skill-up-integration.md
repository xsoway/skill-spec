# Skill-up 集成规范

Skill-up 用于评测和回归，不是包结构检查的替代品。

| 阶段 | 命令 | 证据含义 |
|---|---|---|
| 静态包 | `validate_skill_package.py` | 工件与本地约束正确 |
| Eval 结构 | `skill_up.py validate <skill>` | 外部 CLI 可用时验证 eval schema；不可用时明确 `NOT_INSTALLED` |
| 运行时 | `skill_up.py run <skill> --execute` | 指定引擎、数据、版本和输出目录下的真实观测 |

运行产物必须位于项目根 `.skill-up-workspaces/`，不得污染 Skill 包。不得在没有显式 `--execute` 的情况下触发模型调用。
