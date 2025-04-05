# 🎲 BGA 翻译助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

帮助翻译 Board Game Arena (BGA) 平台上的桌游内容，让更多中文玩家能够享受桌游的乐趣！

## ✨ 特性

- 🔄 自动获取 BGA 游戏元数据
- 📝 获取现有翻译内容
- 🤖 自动填写翻译内容
- 🔄 支持分页自动翻译
- 🚀 自动登录和导航
- 📖 规则书文本提取

## 🛠️ 安装

1. 克隆仓库：
```bash
git clone https://github.com/PascalDai/BGATranslatehelper.git
cd BGATranslatehelper
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 填写您的 BGA 账号信息：
```ini
BGA_USERNAME=your_username
BGA_PASSWORD=your_password
```

## 📋 使用方法

### 1. 🎮 初始化游戏目录

```bash
python -m src.main init-game <game_name>
```

这将创建以下目录结构：
```
data/games/<game_name>/
├── metadata/        # 游戏元数据
├── rules/          # 规则书相关文件
└── translations/   # 翻译相关文件
```

### 2. 📊 获取游戏元数据

```bash
python -m src.main fetch-game-info <game_name>
```

### 3. 🔍 获取翻译内容

```bash
python -m src.main fetch-translation <game_name>
```

这将生成以下文件：
- 📝 `translation_table.md`：翻译对照表
- 🗃️ `translation_data.json`：结构化数据
- 📄 `raw.html`：原始 HTML（可选）
- 📚 `bga_translations.md`：BGA 官方翻译
- ✍️ `my_translations.md`：个人翻译

### 4. 📝 提交翻译

1. 确保翻译对照表 `translation_table.md` 已经准备好
2. 运行翻译提交脚本：
```bash
python test_translation_submitter.py
```

脚本会自动执行以下操作：
- ✅ 自动登录 BGA 账号
- 🔄 跳转到翻译页面
- 📝 自动填写翻译内容
- ⏭️ 自动翻页继续处理
- 🔄 自动保存翻译内容

注意事项：
- 确保翻译对照表中的原文与网页上的完全一致
- 建议先小范围测试，确认无误后再批量提交
- 如遇到错误，查看日志文件了解详情

## 📁 文件说明

- 📊 `game_info.json`：游戏元数据
- 📝 `translation_table.md`：翻译对照表
- 🗃️ `translation_data.json`：结构化翻译数据
- 📄 `raw.html`：原始 HTML 内容（可选）
- 📚 `bga_translations.md`：BGA 官方翻译
- ✍️ `my_translations.md`：个人翻译
- 📖 `extracted.md`：规则书文本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！让我们一起完善这个工具，帮助更多的中文桌游玩家。

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Board Game Arena](https://boardgamearena.com/) - 优秀的在线桌游平台
- 所有为 BGA 平台贡献翻译的志愿者们
