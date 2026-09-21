# Skill 包目录指南

每个新 Skill 采用下列最小可交付结构：

```text
<skill-name>/
├── SKILL.md
├── prompts/<skill-name>.md
├── agents/openai.yaml
├── evals/eval.yaml
├── evals/cases/{basic-success,edge-incomplete-input,edge-scope-boundary}.yaml
├── scripts/validate_skill_package.py
├── references/                 # 仅在有深规则时创建
└── examples/                   # 仅在示例能降低误用时创建
```

可选的 `optimization/` 只服务有明确 SkillOpt 训练计划的 Skill，包含不可训练合同、可训练种子、数据清单、训练配置和晋升记录。它不是所有 Skill 的必需目录。
