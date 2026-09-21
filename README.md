<p align="center">
  <img src="https://img.shields.io/badge/skill--spec-1.0-blue" alt="skill-spec version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/status-stable-success" alt="status">
</p>

# skill-spec

> **Codex Skill 包工程规范 · Engineering standard for Codex Skill packages**

A unified engineering standard for building **Codex Skill packages** that are discoverable, independently installable, evaluable, and safely evolvable — with local, executable validation.
It takes "writing a skill" from a single `SKILL.md` up to "submitting a complete, verifiable, safety-bounded package", with bundled Chinese engineering guidelines and runnable validation scripts.

一套统一、可独立安装、可评测、可演进的 **Codex Skill 包工程规范**。它把"创建一个 Skill"从"只写一个 `SKILL.md`"升级为"提交一个完整、可验证、安全边界清晰的包"，并提供了配套的中文工程准则与可执行校验脚本。

---

## Why（为什么需要）

| Only a `SKILL.md` (anti-pattern) / 只用 SKILL.md（反例） | This standard / 本规范（正例） |
|---|---|
| Entry point only, no execution logic / 只有入口，缺少完整执行逻辑 | Lightweight entry + full logic in `prompts/` / 入口轻量 + `prompts/` 承载完整规范 |
| No structured evaluation / 无法结构化评测 | Three eval cases + schema pin a regression contract / 三类 `eval` case + eval schema 固化回归契约 |
| No safety-boundary checks / 无安全边界校验 | `validate_skill_package.py` scans for secrets & absolute paths / 扫描密钥与绝对路径 |
| Cannot evolve under control / 无法受控演进 | Skill-up regression baseline + SkillOpt held-out + human gate / Skill-up 回归基线 + SkillOpt 留出集人工晋升门禁 |

This standard solves 5 engineering pain points:
本规范解决 5 个工程痛点:

1. **Discoverable / 可发现** — `agents/openai.yaml` provides key-consistent metadata / 提供键一致的元数据。
2. **Installable / 可安装** — each package is self-contained; deep rules live on-demand in `references/` and still work after independent copy / 每个包自包含，深规则按需放在 `references/`，独立复制后仍可工作。
3. **Evaluable / 可评测** — evals distinguish `validate` (structure) from real model `run` (behavior); static checks are never claimed as verified model behavior / Eval 区分 `validate`（结构）与真实模型 `run`（行为观测），绝不把静态检查说成模型已验证。
4. **Evolvable / 可演进** — SkillOpt promotes a candidate only when held-out is non-degraded and a human approves / 只在留出集非退化且有人工审批时才晋升候选。
5. **Safe / 安全** — enforces that a package never ships real secrets, personal data, or absolute local paths / 强调检查包内不得出现真实密钥、个人数据与绝对本机路径。

---

## Structure（目录结构）

```text
skill-spec/
├── SKILL.md                        # activation entry: routing / hard constraints / lazy loading | 激活入口：路由、硬约束、按需加载
├── prompts/skill-spec.md           # full execution spec: input, judgement, rules, min coverage, output | 完整执行规范
├── agents/openai.yaml              # discovery metadata (metadata.key matches directory / frontmatter name) | 可发现元数据
├── references/
│   ├── package-contract.md         # package contract: required artifacts, independence, safety, validation levels | 包契约
│   ├── skill-up-integration.md     # Skill-up evaluation / eval-schema validation | Skill-up 集成规范
│   └── skillopt-integration.md     # SkillOpt controlled optimization: isolation, held-out, promotion gate | SkillOpt 受控优化
├── examples/skill-package-tree.md  # standard package skeleton (incl. optional optimization/) | 标准包骨架
├── evals/
│   ├── eval.yaml                   # schema / engine / timings / assertion defaults | 评测默认
│   └── cases/
│       ├── basic-success.yaml          # happy path | 成功路径
│       ├── edge-incomplete-input.yaml  # missing information | 信息缺失
│       └── edge-scope-boundary.yaml    # scope / risk boundary | 范围/风险边界
├── scripts/
│   ├── validate_skill_package.py   # structural, safety, link validation | 结构、安全、链接校验
│   ├── skill_up.py                 # safe Skill-up adapter (no model calls by default) | Skill-up 安全适配器
│   └── skillopt.py                 # safe SkillOpt adapter (preflight first) | SkillOpt 安全适配器
├── tests/test_skill_spec.py        # local unit tests (unittest) | 本地单测
├── DIRECTORY_GUIDE.md              # minimal deliverable structure for a new package | 新包最小结构
├── SKILL_AUTHORING.md              # authoring & acceptance standard | 编写与验收规范
├── SKILL_STYLE_GUIDE.md            # Chinese writing-style conventions | 中文写作风格约定
└── EXTERNAL_SNAPSHOT_POLICY.md     # external material / tool boundaries | 外部资料/工具边界
```

---

## Quick Start（快速开始）

**Validate the package contract / 校验当前包契约**

```bash
python3 scripts/validate_skill_package.py .
# → PASS: skill-spec package contract
```

**Run local unit tests / 运行本地单测**

```bash
python3 -m unittest discover -s tests
```

**Structurally validate a new skill / 对新 Skill 做静态包校验**

```bash
python3 scripts/validate_skill_package.py <your-skill-dir>
```

Validation covers: required artifacts, `SKILL.md` frontmatter `name` matching the directory, `agents/openai.yaml` `metadata.key`, required headings, and secret / absolute-path scanning.
校验覆盖：必需工件、`SKILL.md` 前置 `name` 与目录一致性、`agents/openai.yaml` 的 `metadata.key`、必备章节、密钥/绝对路径扫描。

---

## Integrations（集成）

### Skill-up (evaluation / regression · 评测 / 回归)

| Stage / 阶段 | Command / 命令 | Evidence meaning / 证据含义 |
|---|---|---|
| Static package / 静态包 | `validate_skill_package.py` | Artifacts & local constraints correct / 工件与本地约束正确 |
| Eval structure / Eval 结构 | `skill_up.py validate <skill>` | Validates eval schema when CLI is available; else `SKILL_UP_NOT_INSTALLED` / 外部 CLI 可用时校验；否则输出对应提示 |
| Runtime / 运行时 | `skill_up.py run <skill> --execute` | Real model observation only under explicit authorization / 仅显式授权下产生真实模型观测 |

⚠️ `run` **requires** an explicit `--execute` or it is refused. Output goes to `.skill-up-workspaces/` outside the package, never polluting it.
⚠️ `run` 必须显式传 `--execute`，否则被拒。运行产物写入项目根外的 `.skill-up-workspaces/`，不污染包本身。

### SkillOpt (controlled optimization · 受控优化)

- `skillopt.py preflight <skill>`: checks that `optimization/` contract, seed, data, config, and promotion record are all present / 检查 `optimization/` 的合同、种子、数据、配置与晋升记录是否齐备。
- `skillopt.py run <skill> --execute`: trains only when the Python `skillopt` package is installed, config is given, and explicit authorization is granted. Training only produces candidates and **never overwrites** `SKILL.md` / prompts / the stable version / 仅在本机安装 Python `skillopt`、给出配置且显式授权时训练。训练只产出候选，**绝不自动覆盖** `SKILL.md` / Prompt / 稳定版本。
- Promotion requires: non-degraded held-out set + human approval / 晋升必须通过：留出集非退化 + 人工审批。

---

## Principles（设计原则）

- **Lightweight entry, complete prompt, deep rules on demand / 入口轻量、Prompt 完整、深规则按需** — `SKILL.md` only routes & hard-constrains; details sink to `references/` / `SKILL.md` 只管路由与硬约束，细节下沉 `references/`。
- **Layered evidence / 证据分层** — static validation, `validate`, model `run`, SkillOpt training, production deployment are reported separately and never impersonate each other / 静态校验、`validate`、模型 `run`、SkillOpt 训练、生产部署——五件事分开报告，不互相冒充。
- **Safety boundary / 安全边界** — no real secrets, no unauthorized external actions, no fabricated run conclusions / 无真实密钥、无未授权外部动作、无伪造运行结论。
- **Rollback-friendly / 可回滚** — back up the stable version before optimizing; never promote a degraded candidate or one that fails the gate / 优化前备份稳定版本，候选退化或门禁未过即不晋升。

---

## License

[MIT](./LICENSE)

---

## Maintainer（维护者）

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>