# 标准包示例

```text
invoice-reconciliation/
├── SKILL.md                         # 激活入口
├── prompts/invoice-reconciliation.md # 完整执行规范
├── agents/openai.yaml               # discovery metadata
├── evals/eval.yaml
├── evals/cases/
│   ├── basic-success.yaml
│   ├── edge-incomplete-input.yaml
│   └── edge-scope-boundary.yaml
├── scripts/validate_skill_package.py
├── references/domain-rules.md
└── examples/input-output.md
```

若进入 SkillOpt 优化，再额外加入 `optimization/contract.md`、`seed_skill.md`、数据清单、配置和 `promotion-record.md`。示例不代表这些文件默认存在或可直接训练。
