#!/usr/bin/env python3
"""
Smoke tests for molecule-superpowers.

See tests/README.md for rationale on limited test coverage.

Run: python -m pytest tests/ -v
"""
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILLS = [
    "executing-plans",
    "systematic-debugging",
    "test-driven-development",
    "verification-before-completion",
    "writing-plans",
]


class TestPluginManifest(unittest.TestCase):
    """Verify plugin.yaml is well-formed."""

    @classmethod
    def setUpClass(cls):
        import yaml
        manifest_path = os.path.join(REPO_ROOT, 'plugin.yaml')
        with open(manifest_path) as f:
            cls.manifest = yaml.safe_load(f)

    def test_plugin_yaml_loads(self):
        self.assertIsInstance(self.manifest, dict)

    def test_name(self):
        self.assertEqual(self.manifest['name'], 'superpowers')

    def test_version_semver(self):
        v = self.manifest['version']
        self.assertRegex(v, r'^\d+\.\d+\.\d+$')

    def test_description_present(self):
        self.assertGreater(len(self.manifest.get('description', '')), 10)

    def test_runtimes_include_claude_code(self):
        self.assertIn('claude_code', self.manifest.get('runtimes', []))

    def test_all_five_skills_declared(self):
        skills = self.manifest.get('skills', [])
        for skill in SKILLS:
            self.assertIn(skill, skills, f"skill {skill!r} not declared in plugin.yaml")


class TestSkillFrontmatter(unittest.TestCase):
    """Verify each skill's SKILL.md has valid frontmatter and body."""

    def test_skill_file_exists(self):
        for skill in SKILLS:
            path = os.path.join(REPO_ROOT, 'skills', skill, 'SKILL.md')
            self.assertTrue(os.path.isfile(path), f"SKILL.md not found for {skill}")

    def test_skill_frontmatter_name(self):
        import yaml
        for skill in SKILLS:
            path = os.path.join(REPO_ROOT, 'skills', skill, 'SKILL.md')
            with open(path) as f:
                content = f.read()
            self.assertTrue(content.startswith('---'), f"{skill}: missing frontmatter")
            parts = content.split('---', 2)
            self.assertEqual(len(parts), 3, f"{skill}: malformed frontmatter")
            _, frontmatter, _ = parts
            data = yaml.safe_load(frontmatter)
            self.assertIsInstance(data, dict, f"{skill}: frontmatter is not a dict")
            self.assertEqual(data.get('name'), skill, f"{skill}: frontmatter name mismatch")

    def test_skill_body_has_heading(self):
        for skill in SKILLS:
            path = os.path.join(REPO_ROOT, 'skills', skill, 'SKILL.md')
            with open(path) as f:
                content = f.read()
            parts = content.split('---', 2)
            _, _, body = parts
            self.assertRegex(
                body.lstrip(), r'^# ',
                f"{skill}: body must start with a # heading"
            )

    def test_skill_body_has_overview(self):
        for skill in SKILLS:
            path = os.path.join(REPO_ROOT, 'skills', skill, 'SKILL.md')
            with open(path) as f:
                content = f.read()
            # Every skill documents its core principle / overview
            self.assertTrue(
                any(kw in content.lower() for kw in ['overview', 'principle', 'when to']),
                f"{skill}: body should document overview or core principle"
            )


class TestAdapters(unittest.TestCase):
    """Verify both runtime adapters re-export AgentskillsAdaptor."""

    def test_claude_code_adapter_exists(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')
        self.assertTrue(os.path.isfile(path))

    def test_deepagents_adapter_exists(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'deepagents.py')
        self.assertTrue(os.path.isfile(path))

    def test_claude_code_re_exports_agentskills_adaptor(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')
        with open(path) as f:
            content = f.read()
        self.assertIn('AgentskillsAdaptor', content)

    def test_deepagents_re_exports_agentskills_adaptor(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'deepagents.py')
        with open(path) as f:
            content = f.read()
        self.assertIn('AgentskillsAdaptor', content)


class TestValidatePlugin(unittest.TestCase):
    """Smoke-test validate-plugin.py if present."""

    def test_validate_plugin_exits_zero(self):
        import subprocess
        val_path = os.path.join(REPO_ROOT, '.molecule-ci', 'scripts', 'validate-plugin.py')
        if not os.path.isfile(val_path):
            self.skipTest("validate-plugin.py not found")
        result = subprocess.run(
            [sys.executable, val_path],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode, 0,
            f"validate-plugin.py failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        self.assertIn('superpowers', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
