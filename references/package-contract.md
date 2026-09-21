# Skill 包契约

## 必需工件

| 工件 | 目的 |
|---|---|
| `SKILL.md` | 轻量入口、路由、硬约束、按需加载和交付自检 |
| `prompts/<name>.md` | 完整执行规范：输入、判断、规则、最低覆盖、输出、质量 |
| `agents/openai.yaml` | 可发现元数据；key 必须与目录/前置 name 一致 |
| `evals/eval.yaml` + 3 cases | 回归契约：成功、信息缺失、范围/风险边界 |
| `scripts/validate_skill_package.py` | 独立可执行的结构、安全与链接校验 |

## 独立性与安全

包内 Markdown 只允许链接同包相对文件或官方外部链接；不得链接其他本地 Skill 的内部文件。不得包含真实凭据、个人数据、绝对本机路径或未授权运行命令。

## 最小验证层级

1. 静态：目录、元数据、YAML、链接、秘密扫描、脚本单测。
2. Skill-up：`validate` 证明 Eval 结构；`run` 才产生指定引擎/样本的行为观测。
3. SkillOpt：preflight 证明训练条件；训练仅产出候选；留出集与人工门禁通过后才可晋升。
