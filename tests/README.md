# Test Rationale — molecule-superpowers

## What this plugin does

`molecule-superpowers` provides 5 prose skills covering core agent engineering
practices: `executing-plans`, `systematic-debugging`, `test-driven-development`,
`verification-before-completion`, and `writing-plans`. Both adapters
(`adapters/claude_code.py`, `adapters/deepagents.py`) are thin re-exports of
`AgentskillsAdaptor` from `plugins_registry.builtins` — no business logic, no
network calls, no side effects.

## What is tested

- `plugin.yaml` is valid YAML with required fields (name, version, runtimes, skills)
- Each of the 5 skills has valid YAML frontmatter and a body with a `#` heading
- Both adapters exist and re-export `AgentskillsAdaptor`
- `validate-plugin.py` (`.molecule-ci/scripts/`) exits zero

## What is NOT unit-tested (and why)

All 5 skills are prose guidance inside `SKILL.md` files — no Python functions to
call. Testing the actual debugging/TDD/planning workflow would require a full
workspace runtime with a real agent session. Smoke tests cover the artifact
structure; full evaluation requires integration tests.

## Running tests

```bash
python -m pytest tests/ -v
```
