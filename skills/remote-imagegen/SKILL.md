---
name: remote-imagegen
description: Generate or edit raster images through the OpenAI-compatible image endpoint configured in the user's local Codex installation. Use when the current Codex environment relies on a custom or self-hosted `base_url`, not the official OpenAI endpoint, and image generation should go through that remote provider rather than the built-in image pipeline. This skill is especially relevant for text-to-image posters, illustrations, sprites, mockups, product shots, and reference-image edits sent through the configured remote endpoint.
---

# Remote Imagegen

## Overview

This is an independent Codex skill for environments that route model traffic through a custom OpenAI-compatible endpoint. It uses the local Codex configuration to find the active `base_url` and API key, then calls the remote image API for either text-to-image generation or reference-image edits.

## When To Use

- The local Codex `base_url` is not the official OpenAI endpoint and the task needs image generation.
- The user wants image generation through the remote provider configured in local Codex.
- The current Codex setup uses a custom or self-hosted `base_url`.
- The task needs a raster asset such as a poster, concept image, UI mockup, sprite, product render, or edited reference image.

## When Not To Use

- The output should be SVG, HTML/CSS, canvas, or another code-native artifact.
- The built-in `imagegen` path is preferred and no remote endpoint is required.
- The user only wants prompt help without actually generating an image.

## Workflow

1. Confirm the task needs remote image generation rather than the built-in image path.
2. Collect the prompt, output path, and optional input image path.
3. Run `scripts/remote_image.py`.
4. If there is no input image, the runner calls `/v1/images/generations`.
5. If there is an input image, the runner calls `/v1/images/edits`.
6. Save the output image into the project workspace when the result is part of the task output.

## Command Pattern

Text-to-image:

```bash
python3 skills/remote-imagegen/scripts/remote_image.py \
  --prompt "A cinematic science-fiction city street at dusk, rain reflections, dense detail." \
  --out ./generated/city-street.png
```

Repeat text-to-image generation with the same endpoint settings:

```bash
python3 skills/remote-imagegen/scripts/remote_image.py \
  --prompt "Replace this with the new image prompt." \
  --size 2160x3840 \
  --out ./generated/new-image-name.png
```

For repeat requests, the prompt and output path are usually the only values that need to change.
Keep `--size 2160x3840` for vertical 4K output, or try `--size 3840x2160` for horizontal
4K output when the configured provider supports those sizes. If the provider rejects a 4K
size, use the highest supported generation size and upscale afterward.

Image edit:

```bash
python3 skills/remote-imagegen/scripts/remote_image.py \
  --prompt "Complete this character into a full-body standing illustration and keep the reference design." \
  --image ./references/character.jpg \
  --out ./generated/character-fullbody.png
```

## Config Resolution

The runner resolves configuration in this order:

1. Environment variables:
   - Base URL: `REMOTE_IMAGE_BASE_URL`, `OPENAI_BASE_URL`
   - API key: `REMOTE_IMAGE_API_KEY`, `OPENAI_API_KEY`
2. `~/.codex/config.toml`
3. `~/.codex/auth.json`

See `references/runtime.md` for the exact resolution order.

## Rules

- Do not hardcode secrets into commands or files.
- Do not invent a custom curl snippet when the bundled runner already covers the task.
- Keep prompts faithful to the user's subject and constraints.
- If the user asks for multiple variants, pass `--n` explicitly.
