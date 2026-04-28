---
name: remote-imagegen
description: Generate or edit detailed raster images through the OpenAI-compatible image endpoint configured in the user's local Codex installation. Use when image generation must go through a custom or self-hosted `base_url` rather than the built-in image pipeline, especially for Chinese technical architecture diagrams, workflow diagrams, UI mockups, posters, illustrations, sprites, product renders, reference-image edits, and 2K/4K documentation assets.
---

# Remote Imagegen

## Core Rule

Use this skill to create bitmap images through the locally configured remote image endpoint. Do not satisfy these requests by drawing SVG, HTML/CSS, canvas, Mermaid CLI output, or other programmatic diagrams unless the user explicitly asks for that format.

The bundled runner reads the active Codex endpoint and API key, calls `/v1/images/generations` for text-to-image, calls `/v1/images/edits` when `--image` is provided, and writes only image files by default. It writes raw response JSON only when `--response-json` is explicitly passed.

## Workflow

1. Classify the request before writing the prompt:
   - `technical-architecture`: layered systems, services, repositories, queues, hardware links.
   - `workflow-sequence`: user/service/device/API interactions over time.
   - `state-machine`: states, transitions, guards, retry paths, terminal states.
   - `data-model`: tables, entities, relationships, key fields.
   - `ui-mockup`: realistic application screens and controls.
   - `infographic-diagram`: explanatory business or technical summary graphic.
2. Expand the user request into a concrete prompt with layout, named components, connectors, labels, color semantics, constraints, and an avoid list.
3. For technical documentation diagrams, prefer 16:9 4K unless the user asks otherwise:
   - `--size 3840x2160 --quality high --output-format png`
   - For 2K horizontal use `--size 2048x1152`.
   - For vertical 4K use `--size 2160x3840`.
4. Generate with `scripts/remote_image.py`.
5. Verify the created image path and dimensions when the asset will be committed or linked in a document.
6. If inserting into Markdown, add image links with stable relative paths and short captions.

## Prompt Schema

For documentation diagrams, use this structure in the prompt. Prefer a prompt file when the prompt is long.

```text
Use case: technical-architecture
Asset type: 中文软件详细设计文档配图，4K 分辨率，3840x2160，16:9 横版，高清，适合 PDF/Word 导出。
Primary request: 生成一张专业商务风格的“<主题>”技术架构图。
Layout: <从左到右/从上到下/泳道/分层/中心辐射>，说明每个区域的空间占比。
Components: <逐项列出真实模块、类名、服务名、表名、线程、外部系统、硬件链路>。
Connectors: <逐项列出箭头方向、同步/异步、读写、事件广播、失败回退、重试>。
Color semantics: 蓝色=Presentation，绿色=Application，紫色=Kernel，橙色=Infrastructure，红色=异常/审计，灰色=预留或外部系统。
Text labels: 中文为主，类名/接口名/枚举值保留英文，所有关键节点都有清晰标签。
Detail level: 信息密度高但可读，每个分区 4-8 个关键节点，连接线清晰不交叉，使用图例。
Constraints: 专业、商务、干净、白底或浅灰底、细线条、统一字体、无卡通、无 3D、无装饰性背景。
Avoid: 随机乱码、伪代码块、无意义图标、空泛云朵、模糊文字、过度渐变、SVG 矢量感、程序化绘制感。
```

## Technical Diagram Guidance

- Do not ask the model to draw a generic “architecture diagram”. Name the actual modules, state names, database tables, and cross-layer dependencies.
- Include edge semantics. Examples: `QObject signal`, `Repository write`, `statusChanged broadcast`, `retry with exponential backoff`, `read-only compatibility path`.
- Put source-to-target direction in the prompt. Example: `CounterQueueTab -> QueueService -> IDeviceService -> MockBusDriver -> 状态广播`.
- For state machines, require terminal states, recovery paths, guard conditions, and forbidden transitions.
- For sequence diagrams, specify swimlanes and the chronological order of calls, events, database writes, and UI updates.
- For dense Chinese labels, request `高清、清晰中文标签、无乱码、适合文档印刷`.
- If the first image is too simple, regenerate with more named nodes and stricter connector requirements instead of switching to programmatic drawing.

## Command Patterns

Long prompt through a prompt file:

```bash
python D:/tmp/remote-imagegen/skills/remote-imagegen/scripts/remote_image.py \
  --prompt-file ./tmp/prompts/02_7_application_lifecycle.txt \
  --size 3840x2160 \
  --quality high \
  --output-format png \
  --out ./docs/详设生成/v2/assets/imagegen/architecture/02_7_application_lifecycle.png
```

Inline text-to-image:

```bash
python D:/tmp/remote-imagegen/skills/remote-imagegen/scripts/remote_image.py \
  --prompt "Use case: technical-architecture. Asset type: 中文软件详细设计文档配图，4K 分辨率，3840x2160，16:9 横版，高清。Primary request: 生成一张专业商务风格的 ApplicationHost 4 阶段生命周期技术流程图。Components: configureServices, initializeServices, createViewModels, startUserInterface, ServiceContainer, DatabaseService, LoggerFactory, QQmlApplicationEngine. Connectors: 主启动箭头、失败回滚箭头、显式析构顺序。Avoid: 随机乱码、卡通、SVG感。" \
  --size 3840x2160 \
  --quality high \
  --output-format png \
  --out ./generated/application-lifecycle.png
```

Reference-image edit:

```bash
python D:/tmp/remote-imagegen/skills/remote-imagegen/scripts/remote_image.py \
  --prompt "保持原图布局，重绘为中文软件详细设计文档插图，增强模块标签、箭头和图例，专业商务风格，高清。" \
  --image ./references/source.png \
  --size 3840x2160 \
  --quality high \
  --output-format png \
  --out ./generated/source-redesigned.png
```

Use `--n` for variants. If the provider rejects a 4K size, retry with the highest supported size and keep the same detailed prompt.

## Config Resolution

The runner resolves configuration in this order:

1. Environment variables:
   - Base URL: `REMOTE_IMAGE_BASE_URL`, `OPENAI_BASE_URL`
   - API key: `REMOTE_IMAGE_API_KEY`, `OPENAI_API_KEY`
2. `~/.codex/config.toml`
3. `~/.codex/auth.json`

See `references/runtime.md` for exact resolution behavior.

## QA Checklist

- The output file exists and has the requested extension.
- Dimensions match the requested size when the provider supports it.
- No `.json` response file was created unless `--response-json` was requested.
- Chinese labels are readable enough for the document context.
- The image contains the requested named modules and logical connectors.
- The diagram is not a generic poster: it communicates architecture, flow, state, or data relationships.
- Markdown references use relative paths that remain valid after moving or committing the document.

## Rules

- Do not hardcode secrets into commands or files.
- Do not invent custom curl commands when the runner covers the task.
- Keep prompts faithful to the user's subject, vocabulary, resolution, language, and style constraints.
- Do not replace user-requested image generation with Mermaid CLI, SVG, HTML, CSS, canvas, or Python drawing.
