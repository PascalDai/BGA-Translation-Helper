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
- 💾 自动保存翻译进度
- 📊 支持 JSON 和 Markdown 格式的翻译文件
- 🔍 详细的日志记录

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
└── translations/    # 翻译相关文件
```

### 2. 📊 获取游戏元数据

```bash
python -m src.main fetch-game-info <game_name>
```

这将在 `metadata` 目录下生成：
- 📝 `game_info.json`：游戏的详细信息，包括游戏ID、名称、描述等

### 3. 🔍 获取翻译内容

```bash
python -m src.main fetch-translation <game_name>
```

这将在 `translations` 目录下生成以下文件：
- 📝 `all_translations.json`：所有翻译内容的JSON数据
- 📝 `all_translations.md`：所有翻译内容的对照表（包含已翻译内容）
- 📝 `untranslated.json`：未翻译内容的JSON数据
- 📝 `untranslated.md`：未翻译内容的对照表（用于填写新翻译）

### 4. 📝 提交翻译

1. 在 `untranslated.md` 文件中填写译文，格式如下：
```markdown
| 原文 | 原文出处 | 译文 |
|------|----------|------|
| Original text | Context | 中文翻译 |
```

2. 运行翻译提交命令：
```bash
python -m src.main submit-translations <game_name>
```

脚本会自动执行以下操作：
- ✅ 自动登录 BGA 账号
- 🔄 跳转到翻译页面
- 📝 自动填写翻译内容
- ⏭️ 自动翻页继续处理
- 🔄 自动保存翻译内容

## 📁 文件说明

- 📊 `game_info.json`：游戏元数据，包含游戏ID、名称、描述等信息
- 📝 `all_translations.json`：所有翻译内容，包括已翻译和未翻译的条目
- 📝 `all_translations.md`：所有翻译内容的对照表，方便查看现有翻译
- 📝 `untranslated.json`：未翻译内容，用于程序处理
- 📝 `untranslated.md`：未翻译内容的对照表，用于填写新翻译

## 🔍 注意事项

1. 翻译提交前：
   - 确保 `untranslated.md` 中的原文与网页上的完全一致
   - 检查翻译内容是否符合游戏术语规范
   - 建议先小范围测试，确认无误后再批量提交

2. 翻译过程中：
   - 程序会自动处理变量占位符（如 `${player_name}`）
   - 保持格式标记（如 HTML 标签）不变
   - 注意保留原文中的空格和标点符号

3. 错误处理：
   - 如遇到错误，查看控制台输出的详细日志
   - 确保网络连接稳定
   - 检查 BGA 账号登录状态

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！让我们一起完善这个工具，帮助更多的中文桌游玩家。

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Board Game Arena](https://boardgamearena.com/) - 优秀的在线桌游平台
- 所有为 BGA 平台贡献翻译的志愿者们
