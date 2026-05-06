# Local Development Setup

This runbook covers setting up a local development environment for `superpowers`.

---

## Prerequisites

- Python 3.11+
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-superpowers`

---

## Clone & Bootstrap

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-superpowers.git
cd molecule-ai-plugin-superpowers
```

---

## Validating Plugin Structure

```bash
# YAML structure
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
echo "plugin.yaml OK"

# Check all skill paths exist
python3 -c "
import yaml, os
with open('plugin.yaml') as f:
    data = yaml.safe_load(f)
for skill in data.get('skills', []):
    path = f'skills/{skill}/SKILL.md'
    exists = os.path.exists(path)
    print(f'[{\"OK\" if exists else \"MISSING\"}] {path}')
"
```

---

## Testing Skills Locally

The harness wrapper (`builtin_tools/`) is not in this repo — it is provided
by the Molecule AI platform at runtime. To test:

1. Install the plugin in a test workspace via the platform UI or CLI
2. Trigger each skill and verify output against expected behaviour
3. For `verification-before-completion`: verify it fires after a deliberate bug
   is left in the code

---

## Troubleshooting

### plugin.yaml fails to load

```bash
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
# If this throws, your YAML is malformed
```

### Skill not appearing in workspace

- Verify the skill name in `plugin.yaml` matches the directory name in `skills/`
- Check the workspace runtime is in `plugin.yaml.runtimes`
- Restart the workspace to pick up plugin changes

---

## Related

- `skills/executing-plans/SKILL.md` — plan execution skill
- `skills/systematic-debugging/SKILL.md` — debugging skill
- `skills/test-driven-development/SKILL.md` — TDD skill
- `skills/verification-before-completion/SKILL.md` — verification skill
- `skills/writing-plans/SKILL.md` — planning skill
