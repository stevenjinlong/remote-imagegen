import unittest
from pathlib import Path


SKILL_MD_PATH = Path(__file__).resolve().parents[1] / "skills" / "remote-imagegen" / "SKILL.md"
OPENAI_YAML_PATH = Path(__file__).resolve().parents[1] / "skills" / "remote-imagegen" / "agents" / "openai.yaml"


class SkillMetadataTests(unittest.TestCase):
    def test_skill_uses_independent_name(self):
        text = SKILL_MD_PATH.read_text(encoding="utf-8")

        self.assertIn("name: remote-imagegen", text)
        self.assertNotIn("name: imagegen", text)

    def test_skill_allows_implicit_invocation(self):
        text = OPENAI_YAML_PATH.read_text(encoding="utf-8")

        self.assertIn("allow_implicit_invocation: true", text)

    def test_skill_explicitly_targets_non_official_remote_image_requests(self):
        text = SKILL_MD_PATH.read_text(encoding="utf-8").lower()

        self.assertIn("not the official openai endpoint", text)
        self.assertIn("image generation", text)


if __name__ == "__main__":
    unittest.main()
