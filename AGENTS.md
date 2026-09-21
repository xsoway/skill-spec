# Skill Spec Local Rules

本目录是当前工作区的 Skill 工程规范源。修改后必须运行本包的结构校验和测试；不得复制外部项目的目录分类、双语发布、安装器、CI 或发布约定，除非当前用户明确要求。

`skills/skill-upper/` 是 vendored 的 skill-up CLI 评测技能快照（来源与更新方式见 `skills/skill-upper/VENDORED.md`），仅作评测方法论与命令参考；评测入口统一走 `scripts/skill_up.py`。更新该目录后必须重跑结构校验与测试。

外部工具是可选集成：`skill-up`/`skillopt` 不存在时只报告静态结果，不能伪造运行成功，也不要自动安装或发起训练。
