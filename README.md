# 🎲 BGA 翻译助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

帮助翻译 Board Game Arena (BGA) 平台上的桌游内容，让更多中文玩家能够享受桌游的乐趣！

## ✨ 特性

- 🔄 自动获取 BGA 游戏元数据
- 📝 获取现有翻译内容作为参考
- 📊 生成结构化的翻译数据
- 📖 支持规则书文本提取
- 🤖 支持使用 AI 辅助翻译

## 🛠️ 安装

1. 克隆仓库：
```bash
git clone https://github.com/PascalDai/BGA-Translation-Helper.git
cd BGA-Translation-Helper
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
SAVE_RAW_HTML=true
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

### 4. 📖 处理规则书

1. 将规则书 PDF 放入 `rules/original.pdf`
2. 运行文本提取：
```bash
python -m src.main process-rulebook <game_name>
```

### 5. 🎯 翻译流程

1. 📖 查看 `translation_table.md` 了解现有翻译
2. 📑 阅读 `extracted.md` 中的规则书文本
3. 🤖 使用 AI 辅助翻译：
   - 提供已有翻译作为参考
   - 保持术语翻译一致性
   - 保存到 `my_translations.md`

## 📌 注意事项

- ⚠️ 请确保正确配置 `.env` 文件
- 🔄 保持游戏术语翻译的一致性
- 📚 参考 BGA 平台的官方翻译
- ✨ 保持翻译的专业性和准确性

## 📁 文件说明

- 📊 `game_info.json`：游戏元数据
- 📝 `translation_table.md`：翻译对照表
- 🗃️ `translation_data.json`：结构化翻译数据
- 📄 `raw.html`：原始 HTML 内容（可选）
- 📚 `bga_translations.md`：BGA 官方翻译
- ✍️ `my_translations.md`：个人翻译内容
- 📖 `extracted.md`：规则书提取文本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！让我们一起完善这个工具，帮助更多的中文桌游玩家。

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Board Game Arena](https://boardgamearena.com/) - 优秀的在线桌游平台
- 所有为 BGA 平台贡献翻译的志愿者们
