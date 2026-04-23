<p align="center">
  <a href="https://github.com/stevenjinlong/remote-imagegen/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/stevenjinlong/remote-imagegen?style=for-the-badge" />
  </a>
  <a href="https://github.com/stevenjinlong/remote-imagegen/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/stevenjinlong/remote-imagegen?style=for-the-badge" />
  </a>
  <a href="https://github.com/stevenjinlong/remote-imagegen/commits/main">
    <img alt="Last commit" src="https://img.shields.io/github/last-commit/stevenjinlong/remote-imagegen?style=for-the-badge" />
  </a>
  <img alt="Codex skill" src="https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge" />
</p>

<p align="center">
  <a href="https://linux.do/t/topic/1777230">
    <img
      alt="LINUX DO"
      src="https://img.shields.io/badge/LINUX-DO-FFB003.svg?logo=data:image/svg%2bxml;base64,DQo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiPjxwYXRoIGQ9Ik00Ni44Mi0uMDU1aDYuMjVxMjMuOTY5IDIuMDYyIDM4IDIxLjQyNmM1LjI1OCA3LjY3NiA4LjIxNSAxNi4xNTYgOC44NzUgMjUuNDV2Ni4yNXEtMi4wNjQgMjMuOTY4LTIxLjQzIDM4LTExLjUxMiA3Ljg4NS0yNS40NDUgOC44NzRoLTYuMjVxLTIzLjk3LTIuMDY0LTM4LjAwNC0yMS40M1EuOTcxIDY3LjA1Ni0uMDU0IDUzLjE4di02LjQ3M0MxLjM2MiAzMC43ODEgOC41MDMgMTguMTQ4IDIxLjM3IDguODE3IDI5LjA0NyAzLjU2MiAzNy41MjcuNjA0IDQ2LjgyMS0uMDU2IiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZWNlY2VjO2ZpbGwtb3BhY2l0eToxIi8+PHBhdGggZD0iTTQ3LjI2NiAyLjk1N3EyMi41My0uNjUgMzcuNzc3IDE1LjczOGE0OS43IDQ5LjcgMCAwIDEgNi44NjcgMTAuMTU3cS00MS45NjQuMjIyLTgzLjkzIDAgOS43NS0xOC42MTYgMzAuMDI0LTI0LjM4N2E2MSA2MSAwIDAgMSA5LjI2Mi0xLjUwOCIgc3R5bGU9InN0cm9rZTpub25lO2ZpbGwtcnVsZTpldmVub2RkO2ZpbGw6IzE5MTkxOTtmaWxsLW9wYWNpdHk6MSIvPjxwYXRoIGQ9Ik03Ljk4IDcwLjkyNmMyNy45NzctLjAzNSA1NS45NTQgMCA4My45My4xMTNRODMuNDI2IDg3LjQ3MyA2Ni4xMyA5NC4wODZxLTE4LjgxIDYuNTQ0LTM2LjgzMi0xLjg5OC0xNC4yMDMtNy4wOS0yMS4zMTctMjEuMjYyIiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZjlhZjAwO2ZpbGwtb3BhY2l0eToxIi8+PC9zdmc+"
    />
  </a>
</p>

<h1 align="center">Remote Imagegen</h1>

<p align="center">
  Use <code>$remote-imagegen</code> in Codex to generate or edit images through your configured OpenAI-compatible endpoint.
</p>

<p align="center">
  <img src="./assets/cute-kitten.png" alt="Cute kitten generated with $remote-imagegen" width="520" />
</p>

<p align="center">
  <a href="./README.zh-CN.md">简体中文</a>
</p>

> Tip: For more reliable triggering, mention `$remote-imagegen`, `OpenAI-compatible endpoint`, `custom base_url`, or `self-hosted provider` directly in your prompt.

## Download

```bash
git clone https://github.com/stevenjinlong/remote-imagegen.git
cd remote-imagegen
python3 scripts/install_local.py --mode symlink
```

If you prefer a copied install instead of a symlink:

```bash
python3 scripts/install_local.py --mode copy
```

Restart Codex after installation.

## Use

Ask Codex with the skill name explicitly:

```text
Use $remote-imagegen to generate a cute kitten portrait through my configured OpenAI-compatible endpoint.
```

```text
Use $remote-imagegen to edit this image through my custom base_url and keep the same character design.
```

```text
Use $remote-imagegen to generate 4 product shots through my self-hosted image endpoint.
```

If your Codex setup already points to a custom OpenAI-compatible `base_url`, the skill will send image generation to that provider instead of the built-in image path.

## Star History

<a href="https://www.star-history.com/#stevenjinlong/remote-imagegen&Date">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/svg?repos=stevenjinlong/remote-imagegen&type=Date&theme=dark"
    />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/svg?repos=stevenjinlong/remote-imagegen&type=Date"
    />
    <img
      alt="Star History Chart"
      src="https://api.star-history.com/svg?repos=stevenjinlong/remote-imagegen&type=Date"
    />
  </picture>
</a>
