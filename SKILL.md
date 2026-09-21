---
name: skill-spec
description: Use this skill when creating, restructuring, reviewing, evaluating, or optimizing a Codex Skill package; triggers include 创建skill、重构skill、Skill规范、skill-up评测 and SkillOpt优化.
---

# Skill Spec

这是本工作区后续 Skill 的统一工程规范：让 Skill 可发现、可独立安装、可评测、可演进，同时不把静态检查写成模型效果或生产结果。

## 何时使用

- 新建、重构或代码审阅一个 Codex Skill。
- 为现有 Skill 补主 Prompt、元数据、评测用例、验证脚本或结构测试。
- 需要用 Skill-up 做回归评测，或以 SkillOpt 受控优化一个已有 Skill。

## 输出格式选项

- 默认产物为一个完整 Skill 目录和 Markdown 验证记录。
- Skill-up 运行结果输出到项目外的 `.skill-up-workspaces/`；SkillOpt 运行结果输出到项目外的 `.skillopt-workspaces/`。

## 如何使用

1. 先读 `prompts/skill-spec.md`，再读取 `references/package-contract.md` 和任务匹配的集成规则。
2. 创建或修改包后运行 `python3 scripts/validate_skill_package.py <skill-dir>`；不要只检查 `SKILL.md`。
3. Skill-up 评测读取 `references/skill-up-integration.md`，使用 `scripts/skill_up.py validate` 或显式 `run --execute`。
4. SkillOpt 优化读取 `references/skillopt-integration.md`，先 `preflight`，通过保留集和人工晋升门禁后才能显式训练或替换候选。

## 参考文件

- 包结构、入口/Prompt 分层、元数据、评测和安全边界：`references/package-contract.md`。
- Skill-up 的静态校验、实际运行与证据边界：`references/skill-up-integration.md`。
- SkillOpt 的可训练边界、数据隔离、留出集和晋升门禁：`references/skillopt-integration.md`。
- 目录骨架参考：`examples/skill-package-tree.md`。

## 常见误区

- 只有 `SKILL.md`，没有主 Prompt、元数据、评测与可执行验证。
- 把 YAML/静态结构通过说成模型行为已验证。
- 把 SkillOpt 直接作用于未隔离的数据，或自动覆盖当前稳定 Skill。
- 在文档、示例、评测数据或日志中放入真实密钥、用户数据或绝对本机路径。

## 最佳实践

- 入口轻量、Prompt 完整、深规则按需放 `references/`，每个包独立复制后仍可工作。
- 新/改 Skill 至少有成功、信息不完整和范围/风险边界三类 Eval。
- 先用固定评测建立基线；优化仅接受留出集非退化且人工复核的候选版本。
