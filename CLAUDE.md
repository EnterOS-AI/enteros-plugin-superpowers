# superpowers — Agent Capability Extensions

`superpowers` is a **capability-extension plugin** that provides five
high-level skills covering the full development lifecycle: systematic debugging,
test-driven development, planning, plan execution, and pre-completion verification.

**Version:** 1.0.0
**Runtime:** `claude_code`, `deepagents`, `hermes`

---

## Repository Layout

```
superpowers/
├── plugin.yaml          — Plugin manifest
├── skills/
│   ├── executing-plans/
│   ├── systematic-debugging/
│   ├── test-driven-development/
│   ├── verification-before-completion/
│   └── writing-plans/
└── adapters/           — Harness adaptors (thin wrappers)
```

---

## Skills

| Skill | Purpose |
|---|---|
| `executing-plans` | Execute a pre-written plan step by step, adapting to obstacles |
| `systematic-debugging` | Hypothesis → isolate → verify → fix, with session logging |
| `test-driven-development` | Red → Green → Refactor cycle, coverage-gated |
| `verification-before-completion` | Self-check before reporting done: tests, lint, build |
| `writing-plans` | Break a complex task into ordered, testable steps |

---

## Development

### Prerequisites

- Node.js >= 18 (for markdownlint, if editing `.md` files)
- Python 3.11+ (for YAML validation)
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-superpowers`

### Setup

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-superpowers.git
cd molecule-ai-plugin-superpowers

# Validate plugin.yaml
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
echo "plugin.yaml OK"
```

### Pre-Commit Checklist

```bash
# YAML structure
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"

# Credential scan
python3 -c "
import re, sys
with open('plugin.yaml') as f:
    content = f.read()
patterns = [r'sk.ant', r'ghp.', r'AKIA[A-Z0-9]']
if any(re.search(p, content) for p in patterns):
    print('FAIL: possible credentials found')
    sys.exit(1)
print('No credentials: OK')
"
```

---

## Release Process

1. Review changes: `git log origin/main..HEAD --oneline`
2. Bump `version` in `plugin.yaml` (semver)
3. Commit: `chore: bump version to X.Y.Z`
4. Tag and push: `git tag vX.Y.Z && git push origin main --tags`
5. Create GitHub Release with changelog

---

## Known Issues

See `known-issues.md` at the repo root.
