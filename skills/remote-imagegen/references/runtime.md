# Runtime Notes

## Resolution Order

The bundled runner resolves request target and auth in this order.

### Base URL

1. `REMOTE_IMAGE_BASE_URL`
2. `OPENAI_BASE_URL`
3. Current provider `base_url` from `~/.codex/config.toml`
4. First provider `base_url` found in `~/.codex/config.toml`
5. `https://api.openai.com`

### API Key

1. `REMOTE_IMAGE_API_KEY`
2. `OPENAI_API_KEY`
3. `OPENAI_API_KEY` from `~/.codex/auth.json`
4. Provider-local fields such as `api_key`, `key`, `token`, or `bearer_token` from `~/.codex/config.toml`

## Mode Selection

- No `--image`: `/v1/images/generations`
- With `--image`: `/v1/images/edits`
- `--mode generate` ignores `--image`; `--mode edit` requires `--image`; `--mode auto` selects based on `--image`.

## Output Behavior

- The raw API response is stored in a temporary JSON file and deleted by default.
- The raw API response is persisted only when `--response-json <path>` is explicitly passed.
- Generated image bytes are written into the requested output path.
- If `--out` is omitted, the default image path is `./tmp/figs/image-<timestamp>.<ext>`.
- If multiple images are returned, the runner appends `-1`, `-2`, and so on before the file extension.

## Prompt and Quality Options

- Use `--prompt "..."` for short prompts.
- Use `--prompt-file <path>` for dense technical prompts that include components, connectors, labels, constraints, and avoid lists.
- Use only one prompt source per request.
- `--quality` is optional. Pass values supported by the configured provider, commonly `low`, `medium`, `high`, or `auto`.
- Technical documentation diagrams should usually request `--size 3840x2160 --quality high --output-format png`.
