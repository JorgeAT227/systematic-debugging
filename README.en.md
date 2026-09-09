# systematic-debugging Skill 🐛

[Versión en español](README.md)

Skill to resolve **complex bugs and performance issues** using the scientific method: deterministic reproduction, refutable hypotheses, minimal surgical fixes, and regression verification. Replaces chaotic "trial and error" with a verifiable 4-step process.

## 🎯 Goal

Turn debugging into a reproducible, auditable process: every bug is resolved with a **minimal test that fails before and passes after** (reverse TDD), a **root cause confirmed by evidence** (not intuition), and a **minimal diff with no side effects**.

## 🧭 The 4 Steps

1. **Deterministic reproduction and minimal isolated test** — If it doesn't reproduce, it's not a bug (ghost rule). Write a RED test and use `git bisect` for regressions.
2. **Causal analysis and refutable hypotheses** — One falsifiable hypothesis at a time, ruling out layers (frontend, backend, data, configuration) with minimal experiments. For performance: measure before touching anything.
3. **Minimal surgical fix** — Smallest possible diff, no opportunistic refactoring, until the test goes GREEN.
4. **Regression verification** — Related suite green, same pattern reviewed elsewhere in the code, and lessons learned documented.

## ⚡ Quick Start

```bash
# 1. Reproduce: write the failing test
pytest tests/unit/test_bug_reproduction.py -k "test_reproduce_bug" -v

# 2. If it's a regression, locate the culprit commit
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>

# 3. Fix with the minimal diff and verify
pytest tests/unit/ -v
```

## 🚫 Anti-Patterns (Forbidden)

- "Trial and error" without reproduction or hypothesis.
- Fix without a test protecting the regression.
- Opportunistic refactoring inside a fix.
- Optimization without prior profiling.
- Calling it done without running the suite.

## 🏛️ Skill Structure

```
systematic-debugging/
├── SKILL.md            # 4-step methodology, checklist, and anti-patterns
├── README.md           # Spanish documentation
├── README.en.md        # English documentation
├── metadata.json       # Skill manifest and tags
└── LICENSE             # MIT — ATX
```

---

**License**: MIT — ATX