<p align="center">
  <img src="https://img.shields.io/badge/skill--spec-1.0-blue" alt="skill-spec version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/status-stable-success" alt="status">
</p>

# skill-spec · Codex Skill 工程规范

一套统一、可独立安装、可评测、可演进的 **Codex Skill 包工程规范**。
它把"创建一个 Skill"从"只写一个 `SKILL.md`"升级为"提交一个完整、可验证、安全边界清晰的包",
并提供了配套的中文工程准则与可执行校验脚本。

> This repository defines a unified engineering standard for building **Codex Skill packages**:
> discoverable, independently installable, evaluable, and safely evolvable — with local, executable validation.

---

## 为什么需要它（Why）

| 只用 SKILL.md（反例） | 本规范（正例） |
|---|---|
| 只有入口，缺少完整执行逻辑 | 入口轻量 + `prompts/` 承载完整规范 |
| 无法结构化评测 | 三类 `eval` case + eval schema 固化回归契约 |
| 无安全边界校验 | `validate_skill_package.py` 扫描密钥与绝对路径 |
| 无法受控演进 | Skill-up 回归基线 + SkillOpt 留出集人工晋升门禁 |

本规范解决 5 个工程痛点:

1. **可发现** `agents/openai.yaml` 提供键一致的元数据。
2. **可安装** 每个包自包含，深规则按需放在 `references/`，独立复制后仍可工作。
3. **可评测** Eval 区分 `validate`（结构）与真实模型 `run`（行为观测），绝不把静态检查说成模型已验证。
4. **可演进** SkillOpt 只在留出集非退化且有人工审批时才晋升候选。
5. **安全** 强迫检查包内不得出现真实密钥、个人数据与绝对本机路径。

---

## 目录结构（Structure）

```text
skill-spec/
├── SKILL.md                        # 激活入口：路由、硬约束、按需加载
├── prompts/skill-spec.md           # 完整执行规范：输入、判断、规则、最低覆盖、输出
├── agents/openai.yaml              # 可发现元数据（metadata.key 与目录/前置 name 一致）
├── references/
│   ├── package-contract.md         # 包契约：必需工件、独立性、安全、最小验证层级
│   ├── skill-up-integration.md     # Skill-up 评测/eval schema 校验集成规范
│   └── skillopt-integration.md     # SkillOpt 受控优化：隔离、留出集、晋升门禁
├── examples/skill-package-tree.md  # 标准包骨架（含可选 optimization/）
├── evals/
│   ├── eval.yaml                   # schema/engine/超时/断言默认
│   └── cases/
│       ├── basic-success.yaml          # 成功路径
│       ├── edge-incomplete-input.yaml  # 信息缺失
│       └── edge-scope-boundary.yaml    # 范围/风险边界
├── scripts/
│   ├── validate_skill_package.py   # 结构、安全、链接独立校验
│   ├── skill_up.py                 # Skill-up 安全适配器（默认不触发模型）
│   └── skillopt.py                 # SkillOpt 安全适配器（preflight 前置）
├── tests/test_skill_spec.py        # 本地单测（unittest）
├── DIRECTORY_GUIDE.md              # 新包最小可交付结构
├── SKILL_AUTHORING.md              # 编写与验收规范
├── SKILL_STYLE_GUIDE.md            # 中文写作风格约定
└── EXTERNAL_SNAPSHOT_POLICY.md     # 外部资料/工具边界
```

---

## 快速开始（Quick Start）

### 校验当前包契约

```bash
python3 scripts/validate_skill_package.py .
# → PASS: skill-spec package contract
```

### 运行本地单测

```bash
python3 -m unittest discover -s tests
```

### 对新 Skill 做静态包校验

```bash
python3 scripts/validate_skill_package.py <your-skill-dir>
```

校验覆盖：必需工件、`SKILL.md` 前置 `name` 与目录一致性、`agents/openai.yaml` 的 `metadata.key`、必备章节、密钥/绝对路径扫描。

---

## 集成（Integrations）

### Skill-up（评测 / 回归）

| 阶段 | 命令 | 证据含义 |
|---|---|---|
| 静态包 | `validate_skill_package.py` | 工件与本地约束正确 |
| Eval 结构 | `skill_up.py validate <skill>` | 外部 CLI 可用时校验 eval schema；否则输出 `SKILL_UP_NOT_INSTALLED` |
| 运行时 | `skill_up.py run <skill> --execute` | 仅显式授权下产生真实模型观测 |

⚠️ `run` 必须显式传 `--execute`，否则被拒。运行产物写入项目根外的 `.skill-up-workspaces/`，不污染包本身。

### SkillOpt（受控优化）

- `skillopt.py preflight <skill>`：检查 `optimization/` 的合同、种子、数据、配置与晋升记录是否齐备。
- `skillopt.py run <skill> --execute`：仅在本机安装 Python `skillopt`、给出配置且显式授权时训练。训练只产出候选，**绝不自动覆盖** `SKILL.md` / Prompt / 稳定版本。
- 晋升必须通过：留出集非退化 + 人工审批。

---

## 设计原则（Principles）

- **入口轻量、Prompt 完整、深规则按需**：`SKILL.md` 只管路由与硬约束，细节下沉 `references/`。
- **证据分层**：静态校验、`validate`、模型 `run`、SkillOpt 训练、生产部署——五件事分开报告，不互相冒充。
- **安全边界**：无真实密钥、无未授权外部动作、无伪造运行结论。
- **可回滚**：优化前备份稳定版本，候选退化或门禁未过即不晋升。

---

## License

[MIT](./LICENSE)

---

## Maintainer

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>