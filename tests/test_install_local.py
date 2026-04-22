import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install_local.py"


def load_module():
    spec = importlib.util.spec_from_file_location("install_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallerTests(unittest.TestCase):
    def test_build_skill_target_shape(self):
        module = load_module()

        target = module.build_skill_target(Path("/home/test/.codex/skills"), "remote-imagegen")

        self.assertEqual(Path("/home/test/.codex/skills/remote-imagegen"), target)

    def test_default_source_points_at_public_skill_dir(self):
        module = load_module()

        source = module.default_skill_source(Path("/repo"))

        self.assertEqual(Path("/repo/skills/remote-imagegen"), source)

    def test_validate_source_requires_skill_md(self):
        module = load_module()

        with self.assertRaises(RuntimeError):
            module.validate_skill_source(Path("/tmp/not-a-skill"))


if __name__ == "__main__":
    unittest.main()
