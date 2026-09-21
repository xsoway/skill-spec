<p align="center">
  <img src="https://img.shields.io/badge/skill--spec-1.0-blue" alt="skill-spec version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/status-stable-success" alt="status">
  <img src="https://img.shields.io/badge/python-3.9+-informational" alt="python version">
</p>

<h1 align="center">skill-spec</h1>

<p align="center">
  <strong>Engineering standard for building Codex Skill packages</strong>
</p>

<p align="center">
  <a href="./README.zh-CN.md">中文</a>
</p>

<p align="center">
<b>Discoverable · Installable · Evaluable · Safely Evolvable</b>
</p>

---

## Table of Contents

- [What is skill-spec?](#what-is-skill-spec)
- [Why do we need it](#why-do-we-need-it)
- [Core concepts](#core-concepts)
- [Repository structure](#repository-structure)
- [Package contract (required artifacts)](#package-contract-required-artifacts)
- [Quick start](#quick-start)
- [CLI reference](#cli-reference)
- [Evaluation contract](#evaluation-contract)
- [End-to-end workflows](#end-to-end-workflows)
- [Safety boundary](#safety-boundary)
- [FAQ](#faq)
- [Design principles](#design-principles)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Maintainer](#maintainer)

---

## What is skill-spec?

`skill-spec` is a **unified engineering standard** for building **Codex Skill packages**. It turns "writing a skill" from dumping a single `SKILL.md` into "submitting a complete, verifiable, safety-bounded package".

A **Codex Skill** is a self-contained, reusable capability bundle that an AI coding agent (e.g. Codex) can load on demand to change how it makes key judgements on a class of tasks. A naive skill is just one Markdown file; under this standard, a skill becomes a **package** with:

- a lightweight activation entry (`SKILL.md`),
- a complete execution spec (`prompts/<name>.md`),
- machine-readable discovery metadata (`agents/openai.yaml`),
- a pinned regression contract (`evals/eval.yaml` + cases),
- an executable structural/safety validator (`scripts/validate_skill_package.py`).

The result is a skill that is **discoverable**, **independently installable**, **evaluable**, and **safely evolvable** — with local, offline, executable validation that never claims static checks as verified model behavior.

> This repository is the *spec* and the reference implementation of the tooling around the spec. Use it as the authoritative standard for every skill you create in your workspace.

---

## Why do we need it

| Only a `SKILL.md` (anti-pattern) | This standard |
|---|---|
| Entry point only, no execution logic | Lightweight entry + full logic in `prompts/` |
| No structured evaluation | Three eval cases + schema pin a regression contract |
| No safety-boundary checks | `validate_skill_package.py` scans secrets & absolute paths |
| Cannot evolve under control | Skill-up regression baseline + SkillOpt held-out + human gate |
| Hard to discover | `agents/openai.yaml` key-consistent metadata |

This standard solves **5 engineering pain points**:

1. **Discoverable** — `agents/openai.yaml` exposes key-consistent metadata so the agent's runtime can find and route to the skill.
2. **Installable** — every package is self-contained. Deep rules are pulled in *on demand* from `references/`, so a package copied on its own still works.
3. **Evaluable** — the eval setup distinguishes **`validate` (structure)** from a real **model `run` (behavior observation)**, so a static check is never falsely reported as "verified model behavior".
4. **Evolvable** — SkillOpt only promotes a candidate when the **held-out set is non-degraded** *and* a human approves. No silent auto-overwrite.
5. **Safe** — validation enforces that a package never ships real secrets, personal data, cookie/private keys, or absolute local paths.

---

## Core concepts

Four ideas underpin the whole standard. Understanding them makes the rest obvious.

### 1. Entry / Prompt / References (Layered content)

- **`SKILL.md`** — the *activation entry*. It only routes and hard-constrains: when to use the skill, output format options, how to use it, references, common misconceptions, best practices.
- **`prompts/<name>.md`** — the *complete execution spec*: inputs, judgement, rules, minimum coverage, outputs, quality requirements.
- **`references/`** — *deep rules* loaded only when a task needs them (package contract, skill-up/skillopt integration notes).

Why? A small entry loads fast and never drowns the agent; the heavy detail is fetched lazily.

### 2. Layered evidence

Not all "passes" have the same meaning. The standard forces you to report **each layer separately** and never let one impersonate another:

| Layer | What it proves | How |
|---|---|---|
| Static validation | Directory, metadata, YAML, links, secret/absolute-path scan are correct | `validate_skill_package.py` |
| `validate` (skill-up) | The eval *schema* is structured correctly | `skill_up.py validate` |
| `run` (skill-up) | Actual model behavior under a given engine/data/version | `skill_up.py run --execute` |
| SkillOpt training | A *candidate* text is trained; not yet released | `skillopt.py run --execute` |
| Production deployment | A candidate is promoted after gates | manual, gated |

### 3. Evidence vs. conclusion

A static validator, an eval structure check, a model run, a training run, and a production deployment are **different things**. Saying "the eval passed" is not the same as "the model is verified", which is not the same as "we shipped it". This standard keeps those lines crisp.

### 4. Optimize ≠ auto-publish

SkillOpt is a *candidate text optimizer*, **not** an auto-releaser. Training only ever produces a candidate; promotion requires a non-degraded held-out set plus a human approver, and it must be rollback-able.

---

## Repository structure

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

### File-by-file responsibilities

| File | When it exists / What it does |
|---|---|
| `SKILL.md` | Always. Activation entry, routing, hard constraints. Frontmatter `name` must equal the directory name. |
| `prompts/<name>.md` | Always. Full execution spec. Name must match the directory. |
| `agents/openai.yaml` | Always. Discovery metadata; `metadata.key` must equal the directory name. |
| `references/*` | Only when deep rules exist. Package contract + integration notes. |
| `examples/` | Only when a concrete example reduces misuse. |
| `evals/eval.yaml` + 3 cases | Always. Regression contract: happy path, missing info, scope/risk boundary. |
| `scripts/validate_skill_package.py` | Always. Executable structural, safety & link validation. |
| `optimization/` | **Optional** — only for skills with an explicit SkillOpt training plan (contract, seed, data manifest, config, promotion record). |

---

## Package contract (required artifacts)

A conformant package **must** contain:

| Artifact | Purpose |
|---|---|
| `SKILL.md` | Lightweight entry, routing, hard constraints, lazy loading, delivery self-check |
| `prompts/<name>.md` | Full execution spec: inputs, judgement, rules, minimum coverage, output, quality |
| `agents/openai.yaml` | Discovery metadata; key must match directory / frontmatter name |
| `evals/eval.yaml` + 3 cases | Regression contract: success, missing info, scope/risk boundary |
| `scripts/validate_skill_package.py` | Independent executable structural, safety & link validation |

The validator checks the following **invariants**:

1. Required artifacts exist (`SKILL.md`, `prompts/<name>.md`, `agents/openai.yaml`, `evals/eval.yaml`, three cases, the validator itself).
2. `SKILL.md` frontmatter has `name: <directory>`.
3. `agents/openai.yaml` has `metadata.key: "<directory>"`.
4. `SKILL.md` contains the six required headings: `## 何时使用`, `## 输出格式选项`, `## 如何使用`, `## 参考文件`, `## 常见误区`, `## 最佳实践`.
5. No `.md`/`.yaml` file matches the credential pattern (`sk-…`, `authorization:`, `api key`, `bearer …`).
6. No `.md`/`.yaml` file contains an absolute local path (`/Users/…`, `/home/…`).

**Independence & safety**: package Markdown may only link to same-package relative files or official external links — never another local skill's internals.

---

## Quick start

**Requirements**: Python 3.9+ (no third-party dependencies for the core scripts). Tests use the stdlib `unittest`; Skill-up / SkillOpt CLIs are optional integrations and are *not* auto-installed.

### Validate this package's contract

```bash
python3 scripts/validate_skill_package.py .
# → PASS: skill-spec package contract
```

### Run the local unit tests

```bash
python3 -m unittest discover -s tests
```

### Validate a new skill package

```bash
python3 scripts/validate_skill_package.py <your-skill-dir>
```

Validation covers: required artifacts, directory/frontmatter `name` consistency, `metadata.key`, required headings, and credential / absolute-path scanning.

---

## CLI reference

### `validate_skill_package.py`

```bash
python3 scripts/validate_skill_package.py [skill-dir]
```

- Defaults to `.` when `skill-dir` is omitted.
- Exit `0` + `PASS: <name> package contract` on success; exit `1` with a `FAIL: ...` line per problem on failure.

### `skill_up.py` — safe Skill-up adapter

```bash
python3 scripts/skill_up.py {validate|run} <skill-dir> [--execute] [--engine codex]
```

| Action | Behavior | Exit code |
|---|---|---|
| `validate <dir>` | Runs the package contract first, then validates the eval schema via the external `skill-up` CLI. If the CLI is absent, prints `SKILL_UP_NOT_INSTALLED` (static checks already passed). | `0` |
| `run <dir>` *without* `--execute` | **Refused** — `REFUSED: ... requires --execute` (may consume model resources). | `2` |
| `run <dir> --execute` | Runs a real model evaluation into `.skill-up-workspaces/<name>/` (outside the package). Fails with `SKILL_UP_NOT_INSTALLED` if the CLI is missing. | `0`/`1` |

- `--engine` defaults to `codex`.
- `run` output directory is `skill-dir.parent / .skill-up-workspaces / <name>` — never pollutes the package.

### `skillopt.py` — safe SkillOpt adapter

```bash
python3 scripts/skillopt.py {preflight|run} <skill-dir> [--execute]
```

| Action | Behavior | Exit code |
|---|---|---|
| `preflight <dir>` | Checks all seven `optimization/` artifacts exist (contract, seed, train/validation/heldout data, config, promotion record). Prints `SKILLOPT_NOT_READY: ...` listing missing files, or `SKILLOPT_READY: ...` when complete. | `0` |
| `run <dir>` *without* `--execute` | **Refused** — `REFUSED: ... requires --execute`. | `2` |
| `run <dir> --execute` | Runs training **only** if the Python `skillopt` package is importable; otherwise `SKILLOPT_NOT_INSTALLED`. Never overwrites `SKILL.md`, prompts, or stable versions — output lands in `.skillopt-workspaces/<name>/`. | `0`/`2` |

The seven required `optimization/` artifacts:

```
optimization/contract.md
optimization/seed_skill.md
optimization/train.jsonl
optimization/validation.jsonl
optimization/heldout.jsonl
optimization/config.yaml
optimization/promotion-record.md
```

---

## Evaluation contract

`evals/eval.yaml` pins the regression contract. Three case types are **mandatory** for every new or materially changed skill:

| Case | File | What it verifies |
|---|---|---|
| Happy path | `basic-success.yaml` | A complete request produces a full package (`SKILL.md`, `prompts`, `evals`, validation). |
| Missing info | `edge-incomplete-input.yaml` | Under-specified requests must surface gaps / assumptions instead of guessing. |
| Scope / risk boundary | `edge-scope-boundary.yaml` | Requests that overstep (e.g. auto-overwrite production) must be blocked (held-out, human, no auto-overwrite). |

Assertions use `must_contain` on required concepts, not fixed phrasing, so reasonable paraphrases still pass. Defaults: `timeout_seconds: 180`, `max_turns: 8`, `expect.exit_code: 0`, `expect.must_not_contain: ["TODO", "我无法"]`. Reports are emitted as JSON.

> Skill-up `validate` proves the eval *schema*; only a `run` produces *behavior* observations. The two are never conflated.

---

## End-to-end workflows

### 1. Create a new skill

1. Read `prompts/skill-spec.md`, then `references/package-contract.md`.
2. Decide: new skill vs. extend existing vs. fix prompt/eval only. Avoid duplicates by name.
3. Scaffold the full directory: entry + main prompt + metadata + evals + (optional) references/examples + validator.
4. Keep the entry small; put inputs, judgement, minimum coverage, output, quality in `prompts/`.
5. Provide three eval cases; keep `SKILL.md` `name`, directory name, and `metadata.key` identical.
6. Run `python3 scripts/validate_skill_package.py <dir>`; iterate until `PASS`.

### 2. Evaluate / regression-test a skill (Skill-up)

1. `skill_up.py validate <dir>` — structural eval check.
2. Establish a baseline with fixed evals.
3. `skill_up.py run <dir> --execute` — real model observation into `.skill-up-workspaces/`.
4. Interpret only as "behavior under this engine/data/version" — never as general capability.

### 3. Optimize a skill under control (SkillOpt)

1. Version the stable baseline.
2. Separate non-trainable contract from trainable seeds; sanitize & approve data; isolate train/validation/held-out sets.
3. Define a repeatable score function and promotion threshold.
4. `skillopt.py preflight <dir>` until `SKILLOPT_READY`.
5. `skillopt.py run <dir> --execute` to produce a **candidate** (never overwrites the stable version).
6. Promote only after: held-out non-degraded + human approval. Record baseline version, candidate version, set IDs, metric comparison, degradation check, approver, rollback location, and date in `promotion-record.md`.

---

## Safety boundary

- **No secrets**: no real keys, tokens, cookies, or private keys in any artifact.
- **No personal data** and **no absolute local paths** (`/Users/…`, `/home/…`).
- **No unauthorized external actions**: a model run only happens under explicit `--execute`; training never auto-publishes.
- **No fabricated run conclusions**: if a CLI is missing or a run is not authorized, report the *not-run* state honestly — never pretend it succeeded.
- **Optimize ≠ publish**: candidates require held-out + human gate and must be rollback-able.

---

## FAQ

**Q: Do I need the `skill-up` / `skillopt` CLIs installed?**
No. They are *optional* integrations. Without them the adapters return honest `NOT_INSTALLED` / `NOT_READY` statuses and never fake a run.

**Q: Why is a package validator different from a test?**
The validator checks *structure, safety, and links* offline. A test asserts *behavior*. Skill-up `run` observes *model behavior*. These prove different things; the standard reports them separately.

**Q: When do I need `optimization/`?**
Only when you have an explicit SkillOpt training plan. It is not a required directory for every skill.

**Q: Can SkillOpt overwrite my stable `SKILL.md`?**
No. Training only produces candidates; promotion is a separate, human-gated, rollback-able step.

**Q: Language of the docs?**
The standard's skill content is authored in Chinese (`SKILL.md`, prompts, references), and this README is bilingual (this English file + `README.zh-CN.md`).

---

## Design principles

- **Lightweight entry, complete prompt, deep rules on demand** — `SKILL.md` only routes & hard-constrains; details sink to `references/`.
- **Layered evidence** — static validation, `validate`, model `run`, SkillOpt training, and production deployment are reported separately and never impersonate each other.
- **Safety boundary** — no real secrets, no unauthorized external actions, no fabricated run conclusions.
- **Rollback-friendly** — back up the stable version before optimizing; never promote a degraded candidate or one that fails the gate.
- **Reuse, don't copy** — reference official docs / maintained rules rather than duplicating whole foreign repositories and installer scripts (see `EXTERNAL_SNAPSHOT_POLICY.md`).

---

## Roadmap

- [x] Unified package contract + validator
- [x] Mandatory three-case evaluation contract
- [x] Safe Skill-up adapter (validate vs. run separation)
- [x] Safe SkillOpt adapter (preflight + gated promotion)
- [ ] CI workflow to run validation + unit tests on every push/PR
- [ ] Template scaffolder (`skill-spec new <name>`) to bootstrap a conformant package
- [ ] More example packages under `examples/`

---

## Contributing

- Keep each new/edited skill's three eval cases updated.
- Run `python3 scripts/validate_skill_package.py .` and `python3 -m unittest discover -s tests` before committing.
- Do not copy external repos' directory taxonomy, bilingual publishing, installers, CI, or release conventions unless clearly needed.
- External CLIs are optional; never auto-install or auto-train them, and never fabricate a successful run.

---

## License

[MIT](./LICENSE)

## Maintainer

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>