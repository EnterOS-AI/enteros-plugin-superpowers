# superpowers — Agent Capability Extensions

`superpowers` is a **capability-extension plugin** that provides five
high-level skills covering the full development lifecycle: systematic debugging,
test-driven development, planning, plan execution, and pre-completion verification.

**Version:** 1.0.0
**Runtime:** `claude_code`, `hermes`

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
- Write access to `molecule-ai/molecule-ai-plugin-superpowers` in Gitea

### Setup

```bash
git clone https://git.moleculesai.app/molecule-ai/molecule-ai-plugin-superpowers.git
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

1. Create a release branch and bump `version` in `plugin.yaml` (semver).
2. Review changes: `git log origin/main..HEAD --oneline`.
3. Commit the bump and merge it through a reviewed, green Gitea PR.
4. Fetch the merged `main`, tag the exact reviewed merge commit, and push only
   that tag: `git tag vX.Y.Z <merge-sha> && git push origin vX.Y.Z`.
5. If a release page is needed, create the Gitea release from that tag with the
   reviewed changelog.

---

## Known Issues

See `known-issues.md` at the repo root.
