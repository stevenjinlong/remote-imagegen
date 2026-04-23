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

<h1 align="center">Remote Imagegen</h1>

<p align="center">
  在 Codex 里直接使用 <code>$remote-imagegen</code>，把图片生成或图片编辑请求发到你本地配置的 OpenAI-compatible endpoint。
</p>

<p align="center">
  <img src="./assets/cute-kitten.png" alt="使用 $remote-imagegen 生成的小猫示例图" width="520" />
</p>

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
