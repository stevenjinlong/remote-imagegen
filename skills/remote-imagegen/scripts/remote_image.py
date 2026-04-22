#!/usr/bin/env python3

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, List, NamedTuple, Optional, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


DEFAULT_CONFIG_PATH = Path.home() / ".codex" / "config.toml"
DEFAULT_AUTH_PATH = Path.home() / ".codex" / "auth.json"
DEFAULT_BASE_URL = "https://api.openai.com"
ENV_BASE_URL_KEYS = ("REMOTE_IMAGE_BASE_URL", "OPENAI_BASE_URL")
ENV_API_KEY_KEYS = ("REMOTE_IMAGE_API_KEY", "OPENAI_API_KEY")
AUTH_API_KEY_KEYS = ("OPENAI_API_KEY",)
CONFIG_SECRET_KEYS = ("api_key", "key", "token", "bearer_token", "openai_api_key")


class RuntimeConfig(NamedTuple):
    base_url: str
    api_key: str
    provider_name: str


def read_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse JSON file: {path}") from exc


def read_toml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise RuntimeError(f"Failed to parse TOML file: {path}") from exc


def first_non_empty_env(keys: Tuple[str, ...]) -> Optional[str]:
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value.strip()
    return None


def extract_provider_name(config: dict[str, Any], explicit_provider: Optional[str] = None) -> str:
    if explicit_provider:
        return explicit_provider
    provider_name = config.get("model_provider")
    if isinstance(provider_name, str) and provider_name.strip():
        return provider_name.strip()
    model_providers = config.get("model_providers")
    if isinstance(model_providers, dict):
        for key, value in model_providers.items():
            if isinstance(key, str) and isinstance(value, dict):
                return key
    return "OpenAI"


def lookup_provider_section(config: dict[str, Any], provider_name: str) -> dict[str, Any]:
    model_providers = config.get("model_providers")
    if not isinstance(model_providers, dict):
        return {}
    provider = model_providers.get(provider_name)
    if isinstance(provider, dict):
        return provider
    return {}


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def build_api_url(base_url: str, endpoint: str) -> str:
    clean_base = normalize_base_url(base_url)
    if clean_base.endswith("/v1") and endpoint.startswith("/v1/"):
        return f"{clean_base}{endpoint[3:]}"
    return f"{clean_base}{endpoint}"


def extract_config_secret(config: dict[str, Any], provider_name: str) -> Optional[str]:
    provider_section = lookup_provider_section(config, provider_name)
    for key in CONFIG_SECRET_KEYS:
        value = provider_section.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    model_providers = config.get("model_providers")
    if isinstance(model_providers, dict):
        for value in model_providers.values():
            if not isinstance(value, dict):
                continue
            for key in CONFIG_SECRET_KEYS:
                secret = value.get(key)
                if isinstance(secret, str) and secret.strip():
                    return secret.strip()
    return None


def extract_base_url(config: dict[str, Any], provider_name: str) -> str:
    provider_section = lookup_provider_section(config, provider_name)
    value = provider_section.get("base_url")
    if isinstance(value, str) and value.strip():
        return normalize_base_url(value.strip())

    model_providers = config.get("model_providers")
    if isinstance(model_providers, dict):
        for provider in model_providers.values():
            if not isinstance(provider, dict):
                continue
            base_url = provider.get("base_url")
            if isinstance(base_url, str) and base_url.strip():
                return normalize_base_url(base_url.strip())

    return DEFAULT_BASE_URL


def resolve_runtime_config(
    config_path: Path = DEFAULT_CONFIG_PATH,
    auth_path: Path = DEFAULT_AUTH_PATH,
    provider_name: Optional[str] = None,
) -> RuntimeConfig:
    env_base_url = first_non_empty_env(ENV_BASE_URL_KEYS)
    env_api_key = first_non_empty_env(ENV_API_KEY_KEYS)

    config = read_toml_file(config_path)
    auth = read_json_file(auth_path)
    resolved_provider = extract_provider_name(config, explicit_provider=provider_name)

    base_url = env_base_url or extract_base_url(config, resolved_provider)

    api_key = env_api_key
    if not api_key:
        for key in AUTH_API_KEY_KEYS:
            value = auth.get(key)
            if isinstance(value, str) and value.strip():
                api_key = value.strip()
                break
    if not api_key:
        api_key = extract_config_secret(config, resolved_provider)
    if not api_key:
        raise RuntimeError(
            "Unable to resolve an API key. Set REMOTE_IMAGE_API_KEY or OPENAI_API_KEY, "
            "or configure ~/.codex/auth.json."
        )

    return RuntimeConfig(
        base_url=normalize_base_url(base_url),
        api_key=api_key,
        provider_name=resolved_provider,
    )


def resolve_mode(mode: str, input_image: Optional[Path]) -> str:
    if mode == "auto":
        return "edit" if input_image else "generate"
    if mode == "edit" and input_image is None:
        raise RuntimeError("Edit mode requires --image.")
    return mode


def endpoint_for_mode(mode: str) -> str:
    if mode == "edit":
        return "/v1/images/edits"
    return "/v1/images/generations"


def build_curl_command(
    runtime: RuntimeConfig,
    prompt: str,
    model: str,
    size: str,
    n: int,
    output_format: str,
    response_path: Path,
    trace_path: Optional[Path],
    input_image: Optional[Path],
) -> List[str]:
    mode = "edit" if input_image else "generate"
    endpoint = endpoint_for_mode(mode)
    command = [
        "curl",
        "-sS",
        "-L",
        "-X",
        "POST",
        build_api_url(runtime.base_url, endpoint),
        "-H",
        f"Authorization: Bearer {runtime.api_key}",
        "-F",
        f"model={model}",
        "-F",
        f"prompt={prompt}",
        "-F",
        f"n={n}",
        "-F",
        f"size={size}",
        "-F",
        f"output_format={output_format}",
    ]
    if input_image is not None:
        command.extend(["-F", f"image=@{input_image}"])
    if trace_path is not None:
        command.extend(["--trace-ascii", str(trace_path)])
    command.extend(["-o", str(response_path)])
    return command


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def normalize_output_path(output_path: Path, output_format: str) -> Path:
    if output_path.suffix:
        return output_path
    return output_path.with_suffix(f".{output_format}")


def default_output_path(output_format: str) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return Path.cwd() / "generated-images" / f"image-{stamp}.{output_format}"


def output_paths(base_path: Path, count: int) -> List[Path]:
    if count <= 1:
        return [base_path]
    return [
        base_path.with_name(f"{base_path.stem}-{index}{base_path.suffix}")
        for index in range(1, count + 1)
    ]


def parse_response_payload(path: Path) -> dict[str, Any]:
    payload = read_json_file(path)
    if not payload:
        raise RuntimeError(f"Empty API response: {path}")
    error = payload.get("error")
    if isinstance(error, dict):
        message = error.get("message") or error
        raise RuntimeError(f"Image API returned an error: {message}")
    if "data" not in payload:
        raise RuntimeError(f"Unexpected image response shape: {path}")
    return payload


def write_image_record(record: dict[str, Any], destination: Path) -> None:
    ensure_parent(destination)
    b64_json = record.get("b64_json")
    if isinstance(b64_json, str) and b64_json:
        destination.write_bytes(base64.b64decode(b64_json))
        return

    url = record.get("url")
    if isinstance(url, str) and url:
        with urllib.request.urlopen(url) as response:  # nosec B310
            destination.write_bytes(response.read())
        return

    raise RuntimeError("Image response did not contain b64_json or url data.")


def materialize_images(payload: dict[str, Any], output_path: Path) -> List[Path]:
    records = payload.get("data")
    if not isinstance(records, list) or not records:
        raise RuntimeError("Image response did not contain any image records.")

    destinations = output_paths(output_path, len(records))
    for record, destination in zip(records, destinations):
        if not isinstance(record, dict):
            raise RuntimeError("Image response record had an invalid shape.")
        write_image_record(record, destination)
    return destinations


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run remote image generation through the Codex-configured OpenAI-compatible endpoint.")
    parser.add_argument("--prompt", required=True, help="Prompt for the image request.")
    parser.add_argument("--image", type=Path, help="Optional source image path for edit mode.")
    parser.add_argument(
        "--mode",
        choices=("auto", "generate", "edit"),
        default="auto",
        help="Request mode. Defaults to auto: edit when --image is set, otherwise generate.",
    )
    parser.add_argument("--model", default="gpt-image-2", help="Image model name.")
    parser.add_argument("--n", type=int, default=1, help="Number of images to request.")
    parser.add_argument("--size", default="1536x1024", help="Requested image size.")
    parser.add_argument("--output-format", default="png", help="Requested output format.")
    parser.add_argument("--out", type=Path, help="Output image path. Defaults to ./generated-images/...")
    parser.add_argument("--response-json", type=Path, help="Where to save the raw JSON response.")
    parser.add_argument("--trace-file", type=Path, help="Optional curl trace file path.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="Codex config TOML path.")
    parser.add_argument("--auth", type=Path, default=DEFAULT_AUTH_PATH, help="Codex auth JSON path.")
    parser.add_argument("--provider", help="Optional explicit provider name from config.toml.")
    parser.add_argument("--base-url", help="Optional explicit base URL override.")
    parser.add_argument("--api-key", help="Optional explicit API key override.")
    return parser.parse_args(argv)


def run(argv: Optional[List[str]] = None) -> int:
    if shutil.which("curl") is None:
        raise RuntimeError("curl is required but was not found in PATH.")

    args = parse_args(argv)

    input_image = args.image.expanduser() if args.image else None
    if input_image is not None and not input_image.is_file():
        raise RuntimeError(f"Input image does not exist: {input_image}")

    mode = resolve_mode(args.mode, input_image)
    runtime = resolve_runtime_config(config_path=args.config, auth_path=args.auth, provider_name=args.provider)
    if args.base_url:
        runtime = runtime._replace(base_url=normalize_base_url(args.base_url))
    if args.api_key:
        runtime = runtime._replace(api_key=args.api_key)

    output_path = normalize_output_path((args.out or default_output_path(args.output_format)).expanduser(), args.output_format)
    response_path = (args.response_json or output_path.with_suffix(".json")).expanduser()
    trace_path = args.trace_file.expanduser() if args.trace_file else None
    ensure_parent(output_path)
    ensure_parent(response_path)
    if trace_path is not None:
        ensure_parent(trace_path)

    effective_input = input_image if mode == "edit" else None
    command = build_curl_command(
        runtime=runtime,
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        n=args.n,
        output_format=args.output_format,
        response_path=response_path,
        trace_path=trace_path,
        input_image=effective_input,
    )

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "curl request failed.")

    payload = parse_response_payload(response_path)
    images = materialize_images(payload, output_path)
    summary = {
        "mode": mode,
        "provider_name": runtime.provider_name,
        "endpoint": endpoint_for_mode(mode),
        "response_json": str(response_path),
        "images": [str(path) for path in images],
    }
    print(json.dumps(summary, indent=2))
    return 0


def main() -> int:
    try:
        return run()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
