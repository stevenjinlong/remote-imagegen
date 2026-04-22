import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "remote-imagegen"
    / "scripts"
    / "remote_image.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("remote_image", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ResolveRuntimeConfigTests(unittest.TestCase):
    def write_temp_files(self, config_text: str, auth_payload: dict[str, str]):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        config_path = root / "config.toml"
        auth_path = root / "auth.json"
        config_path.write_text(config_text, encoding="utf-8")
        auth_path.write_text(json.dumps(auth_payload), encoding="utf-8")
        return temp_dir, config_path, auth_path

    def test_prefers_skill_specific_environment_values(self):
        module = load_module()
        temp_dir, config_path, auth_path = self.write_temp_files(
            """
model_provider = "OpenAI"

[model_providers.OpenAI]
base_url = "https://config.example"
""".strip(),
            {"OPENAI_API_KEY": "from-auth"},
        )
        self.addCleanup(temp_dir.cleanup)

        old_env = os.environ.copy()
        self.addCleanup(lambda: (os.environ.clear(), os.environ.update(old_env)))
        os.environ["REMOTE_IMAGE_BASE_URL"] = "https://env.example"
        os.environ["REMOTE_IMAGE_API_KEY"] = "from-env"

        resolved = module.resolve_runtime_config(config_path=config_path, auth_path=auth_path)

        self.assertEqual("https://env.example", resolved.base_url)
        self.assertEqual("from-env", resolved.api_key)

    def test_reads_provider_base_url_and_auth_json(self):
        module = load_module()
        temp_dir, config_path, auth_path = self.write_temp_files(
            """
model_provider = "OpenAI"

[model_providers.OpenAI]
base_url = "https://images.example"
requires_openai_auth = true
""".strip(),
            {"OPENAI_API_KEY": "from-auth"},
        )
        self.addCleanup(temp_dir.cleanup)

        old_env = os.environ.copy()
        self.addCleanup(lambda: (os.environ.clear(), os.environ.update(old_env)))
        os.environ.pop("REMOTE_IMAGE_BASE_URL", None)
        os.environ.pop("REMOTE_IMAGE_API_KEY", None)
        os.environ.pop("OPENAI_BASE_URL", None)
        os.environ.pop("OPENAI_API_KEY", None)

        resolved = module.resolve_runtime_config(config_path=config_path, auth_path=auth_path)

        self.assertEqual("https://images.example", resolved.base_url)
        self.assertEqual("from-auth", resolved.api_key)
        self.assertEqual("OpenAI", resolved.provider_name)

    def test_reads_key_from_provider_section_when_needed(self):
        module = load_module()
        temp_dir, config_path, auth_path = self.write_temp_files(
            """
model_provider = "Custom"

[model_providers.Custom]
base_url = "https://custom.example"
api_key = "provider-key"
""".strip(),
            {},
        )
        self.addCleanup(temp_dir.cleanup)

        old_env = os.environ.copy()
        self.addCleanup(lambda: (os.environ.clear(), os.environ.update(old_env)))
        os.environ.pop("REMOTE_IMAGE_BASE_URL", None)
        os.environ.pop("REMOTE_IMAGE_API_KEY", None)
        os.environ.pop("OPENAI_BASE_URL", None)
        os.environ.pop("OPENAI_API_KEY", None)

        resolved = module.resolve_runtime_config(config_path=config_path, auth_path=auth_path)

        self.assertEqual("provider-key", resolved.api_key)


class RequestConstructionTests(unittest.TestCase):
    def test_generation_mode_uses_generations_endpoint(self):
        module = load_module()
        config = module.RuntimeConfig(base_url="https://images.example", api_key="k", provider_name="OpenAI")

        command = module.build_curl_command(
            runtime=config,
            prompt="draw a castle",
            model="gpt-image-2",
            size="1536x1024",
            n=1,
            output_format="png",
            response_path=Path("/tmp/response.json"),
            trace_path=None,
            input_image=None,
        )

        self.assertIn("https://images.example/v1/images/generations", command)
        self.assertNotIn("image=@/tmp/source.png", command)

    def test_edit_mode_uses_edits_endpoint_and_image_form(self):
        module = load_module()
        config = module.RuntimeConfig(base_url="https://images.example", api_key="k", provider_name="OpenAI")

        command = module.build_curl_command(
            runtime=config,
            prompt="extend the character to full body",
            model="gpt-image-2",
            size="1536x1024",
            n=1,
            output_format="png",
            response_path=Path("/tmp/response.json"),
            trace_path=Path("/tmp/trace.txt"),
            input_image=Path("/tmp/source.png"),
        )

        self.assertIn("https://images.example/v1/images/edits", command)
        self.assertIn("image=@/tmp/source.png", command)
        self.assertIn("/tmp/trace.txt", command)


class OutputPathTests(unittest.TestCase):
    def test_default_output_path_uses_relative_tmp_figs_directory(self):
        module = load_module()

        output_path = module.default_output_path("png")

        self.assertEqual(Path("tmp/figs"), output_path.parent)
        self.assertFalse(output_path.is_absolute())
        self.assertEqual(".png", output_path.suffix)
        self.assertTrue(output_path.name.startswith("image-"))


if __name__ == "__main__":
    unittest.main()
