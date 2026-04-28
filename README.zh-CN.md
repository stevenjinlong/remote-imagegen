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
  在 Codex 里直接使用 <code>$remote-imagegen</code>，把图片生成或图片编辑请求发到你本地配置的 OpenAI-compatible endpoint。
</p>

<table align="center">
  <tr>
    <td align="center">
      <img src="./assets/cute-kitten.png" alt="使用 $remote-imagegen 生成的小猫示例图" width="360" />
    </td>
    <td align="center">
      <img src="./assets/cute-kitten-portrait-4k.png" alt="使用 $remote-imagegen 生成的 4K 小猫肖像示例图" width="360" />
    </td>
  </tr>
  <tr>
    <td align="center">原始示例图</td>
    <td align="center">4K 竖版示例图（2160x3840）</td>
  </tr>
</table>

<p align="center">
  <a href="./README.md">English</a>
</p>

> 提示：想让这个 skill 更容易被命中，直接在提示词里写上 `$remote-imagegen`、`OpenAI-compatible endpoint`、`custom base_url` 或 `self-hosted provider`。

## 下载

```bash
git clone https://github.com/stevenjinlong/remote-imagegen.git
cd remote-imagegen
python3 scripts/install_local.py --mode symlink
```

如果你更想直接复制而不是软链接：

```bash
python3 scripts/install_local.py --mode copy
```

安装后重启 Codex。

## 使用

在 Codex 里直接带上 skill 名称：

```text
用 $remote-imagegen 通过我配置的 OpenAI-compatible endpoint 生成一张可爱的小猫肖像。
```

```text
用 $remote-imagegen 通过我的 custom base_url 编辑这张图，并保持原始角色设计不变。
```

```text
用 $remote-imagegen 通过我自托管的图片接口生成 4 张商品图。
```

如果你的 Codex 已经指向自定义的 OpenAI-compatible `base_url`，这个 skill 会把图片请求发到那个提供方，而不是走内置图片路径。

## 分辨率提示

如果想生成 2K 或 4K 图片，需要直接在提示词里写清楚目标分辨率，以及需要横版还是竖版。

- 2K 横版：“2048x1152，横版”
- 2K 竖版：“1152x2048，竖版”
- 4K 横版：“3840x2160，横版”
- 4K 竖版：“2160x3840，竖版”，上方新增示例图使用该尺寸

实际可用性仍取决于你配置的图片 provider 和模型。

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
