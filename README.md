<p align="center">
  <img src="https://img.shields.io/badge/skill--spec-1.0-blue" alt="skill-spec version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/status-stable-success" alt="status">
</p>

<h1 align="center">skill-spec</h1>

<p align="center">
  <strong>Engineering standard for Codex Skill packages</strong>
</p>

<p align="center">
  <a href="./README.zh-CN.md">中文</a>
</p>

---

## English

A unified engineering standard for building **Codex Skill packages** that are discoverable, independently installable, evaluable, and safely evolvable — with local, executable validation. It takes "writing a skill" from a single `SKILL.md` up to "submitting a complete, verifiable, safety-bounded package", with bundled engineering guidelines and runnable validation scripts.

### Why

| Only a `SKILL.md` (anti-pattern) | This standard |
|---|---|
| Entry point only, no execution logic | Lightweight entry + full logic in `prompts/` |
| No structured evaluation | Three eval cases + schema pin a regression contract |
| No safety-boundary checks | `validate_skill_package.py` scans for secrets & absolute paths |
| Cannot evolve under control | Skill-up regression baseline + SkillOpt held-out + human gate |

This standard solves 5 engineering pain points:

1. **Discoverable** — `agents/openai.yaml` provides key-consistent metadata.
2. **Installable** — each package is self-contained; deep rules live on-demand in `references/` and still work after independent copy.
3. **Evaluable** — evals distinguish `validate` (structure) from real model `run` (behavior); static checks are never claimed as verified model behavior.
4. **Evolvable** — SkillOpt promotes a candidate only when held-out is non-degraded and a human approves.
5. **Safe** — a package never ships real secrets, personal data, or absolute local paths.

### Structure

```text
skill-spec/
├── SKILL.md                        # activation entry: routing / hard constraints / lazy loading
├── prompts/skill-spec.md           # full execution spec: input, judgement, rules, min coverage, output
├── agents/openai.yaml              # discovery metadata (metadata.key matches directory / frontmatter name)
├── references/
│   ├── package-contract.md         # package contract: required artifacts, independence, safety, validation levels
│   ├── skill-up-integration.md     # Skill-up evaluation / eval-schema validation
│   └── skillopt-integration.md     # SkillOpt controlled optimization: isolation, held-out, promotion gate
├── examples/skill-package-tree.md  # standard package skeleton (incl. optional optimization/)
├── evals/
│   ├── eval.yaml                   # schema / engine / timings / assertion defaults
│   └── cases/
│       ├── basic-success.yaml          # happy path
│       ├── edge-incomplete-input.yaml  # missing information
│       └── edge-scope-boundary.yaml    # scope / risk boundary
├── scripts/
│   ├── validate_skill_package.py   # structural, safety, link validation
│   ├── skill_up.py                 # safe Skill-up adapter (no model calls by default)
│   └── skillopt.py                 # safe SkillOpt adapter (preflight first)
├── tests/test_skill_spec.py        # local unit tests (unittest)
├── DIRECTORY_GUIDE.md              # minimal deliverable structure for a new package
├── SKILL_AUTHORING.md              # authoring & acceptance standard
├── SKILL_STYLE_GUIDE.md            # writing-style conventions
└── EXTERNAL_SNAPSHOT_POLICY.md     # external material / tool boundaries
```

### Quick Start

**Validate the package contract**

```bash
python3 scripts/validate_skill_package.py .
# → PASS: skill-spec package contract
```

**Run local unit tests**

```bash
python3 -m unittest discover -s tests
```

**Structurally validate a new skill**

```bash
python3 scripts/validate_skill_package.py <your-skill-dir>
```

Validation covers: required artifacts, `SKILL.md` frontmatter `name` matching the directory, `agents/openai.yaml` `metadata.key`, required headings, and secret / absolute-path scanning.

### Integrations

#### Skill-up (evaluation / regression)

| Stage | Command | Evidence meaning |
|---|---|---|
| Static package | `validate_skill_package.py` | Artifacts & local constraints correct |
| Eval structure | `skill_up.py validate <skill>` | Validates eval schema when CLI is available; else `SKILL_UP_NOT_INSTALLED` |
| Runtime | `skill_up.py run <skill> --execute` | Real model observation only under explicit authorization |

⚠️ `run` **requires** an explicit `--execute` or it is refused. Output goes to `.skill-up-workspaces/` outside the package, never polluting it.

#### SkillOpt (controlled optimization)

- `skillopt.py preflight <skill>`: checks that `optimization/` contract, seed, data, config, and promotion record are all present.
- `skillopt.py run <skill> --execute`: trains only when the Python `skillopt` package is installed, config is given, and explicit authorization is granted. Training only produces candidates and **never overwrites** `SKILL.md` / prompts / the stable version.
- Promotion requires: non-degraded held-out set + human approval.

### Principles

- **Lightweight entry, complete prompt, deep rules on demand** — `SKILL.md` only routes & hard-constrains; details sink to `references/`.
- **Layered evidence** — static validation, `validate`, model `run`, SkillOpt training, production deployment are reported separately and never impersonate each other.
- **Safety boundary** — no real secrets, no unauthorized external actions, no fabricated run conclusions.
- **Rollback-friendly** — back up the stable version before optimizing; never promote a degraded candidate or one that fails the gate.

---

## License

[MIT](./LICENSE)

## Maintainer

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>