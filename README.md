<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://nonebot.dev/logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
</div>

<div align="center">

# nonebot-plugin-helper-plus

_✨ NoneBot 带有阻断（屏蔽）指定群聊 消息/指令 功能的helper。 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fR0Z863xF/nonebot-plugin-helper-plus.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-helper-plus">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-helper-plus.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

一个带有阻断（屏蔽）指定群聊消息/指令功能的helper。对启用阻断（屏蔽）的群聊，按照在/data/helper/群号.json中的规则进行黑/白名单控制。（到底叫阻断好还是叫屏蔽好呢🤔）  

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-helper-plus

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-helper-plus
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-helper-plus
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-helper-plus
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-helper-plus
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-helper-plus"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| rule_group | 是 | List[str] | 空列表 | 启用屏蔽规则的群聊（请先写好配置文件） |

 

## TODO

- [ ] 完善正则匹配，考虑加入完全匹配匹配和部分匹配两种规则。