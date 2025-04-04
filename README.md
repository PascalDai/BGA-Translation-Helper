# BGA 翻译助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

一个帮助翻译 Board Game Arena 游戏规则的工具。

## 功能特点

- 自动提取规则书文本
- 使用 Mistral OCR 进行文本识别
- 支持多种格式的规则书
- 提供翻译界面
- 自动保存翻译进度
- 自动获取 BGA 游戏元数据

## 安装

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
```bash
cp .env.example .env
# 编辑 .env 文件，填入您的配置信息
```

## 配置说明

在项目根目录下创建 `.env` 文件，包含以下配置项：

```env
# Mistral AI API 配置
MISTRAL_API_KEY=your_api_key_here

# BGA 账号配置
BGA_USERNAME=your_bga_username
BGA_PASSWORD=your_bga_password

# 日志配置
LOG_LEVEL=INFO
```

注意：`.env` 文件包含敏感信息，请勿将其提交到版本控制系统。

## 使用方法

1. 初始化游戏目录：
```bash
python -m src.main init-game <game_name>
```

2. 获取游戏元数据：
```bash
python -m src.main fetch-game-info <game_name>
```

3. 将规则书 PDF 文件放入 `data/games/<game_name>/rules/original.pdf`

4. 处理规则书：
```bash
python -m src.main process-rulebook <game_name>
```

5. 开始翻译：
```bash
python -m src.main start-translation <game_name>
```

## 目录结构

```
BGA-Translation-Helper/
├── data/
│   └── games/
│       └── <game_name>/
│           ├── rules/
│           │   ├── original.pdf
│           │   └── extracted.md
│           ├── translations/
│           │   └── translation.md
│           └── metadata/
│               └── game_info.json
├── src/
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── ocr_processor.py
│   │   ├── pdf_processor.py
│   │   └── text_formatter.py
│   ├── bga_login.py
│   ├── bga_translator.py
│   └── main.py
├── Doc/
│   ├── architecture.md
│   ├── workflow.md
│   └── bga_api_flows.md
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

- [Board Game Arena](https://boardgamearena.com/)
- [Mistral OCR](https://mistral.ai/)
