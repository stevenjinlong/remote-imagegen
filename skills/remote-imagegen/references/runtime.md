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

## Output Behavior

- The raw API response is always saved as JSON.
- Generated image bytes are written into the requested output path.
- If multiple images are returned, the runner appends `-1`, `-2`, and so on before the file extension.
