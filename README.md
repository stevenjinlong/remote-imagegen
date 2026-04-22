# Remote Imagegen For Codex

`remote-imagegen` is a standalone Codex skill for raster image generation through a user-configured OpenAI-compatible endpoint.

Use it when a local Codex installation sends model traffic through a custom `base_url`, not the official OpenAI endpoint, and image generation must go through that same remote provider instead of the built-in image pipeline.

## What It Does

- Generates new images with `/v1/images/generations`
- Edits reference images with `/v1/images/edits`
- Reads `base_url` from the user's local Codex config
- Reads API credentials from the user's local Codex auth/config or environment variables
- Installs as an independent skill named `remote-imagegen`

This skill does **not** replace the built-in `imagegen` skill.

## Install

From this repository root:

```bash
python3 scripts/install_local.py --mode symlink
```

If you prefer copying instead of symlinking:

```bash
python3 scripts/install_local.py --mode copy
```

The installer links or copies:

- `skills/remote-imagegen`
- to `~/.codex/skills/remote-imagegen`

After installation, restart Codex.

## Config Resolution

The runner resolves configuration in this order.

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

## Example Direct Use

Generate:

```bash
python3 skills/remote-imagegen/scripts/remote_image.py \
  --prompt "A cinematic mountain observatory at dawn, photoreal, crisp atmosphere." \
  --out ./generated/observatory.png
```

Edit:

```bash
python3 skills/remote-imagegen/scripts/remote_image.py \
  --prompt "Complete this character into a full-body standing illustration and keep the reference design." \
  --image ./references/character.png \
  --out ./generated/character-fullbody.png
```

## Automatic Invocation

The skill is marked with `allow_implicit_invocation: true`, so Codex can load it automatically when the prompt matches its description.

Typical trigger situations:

- "My local Codex is using a non-official OpenAI-compatible URL and I need image generation"
- "Use the remote image endpoint configured in my Codex to generate a poster"
- "Generate this image through my custom OpenAI-compatible base URL"
- "Edit this reference image through the configured remote provider"

Because this is an independent skill and not a built-in override, exact invocation is still model-selected rather than forced.
