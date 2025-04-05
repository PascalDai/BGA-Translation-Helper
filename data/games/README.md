# 游戏数据目录

此目录用于存储各个游戏的数据，包括游戏信息、规则书、翻译内容等。

## 目录结构

每个游戏都有一个独立的目录，使用游戏的英文名称作为目录名。例如：

```
games/
├── splendor/              # 游戏目录
│   ├── metadata/         # 元数据目录
│   │   └── game_info.json
│   ├── rules/           # 规则书目录
│   │   ├── original.pdf
│   │   └── extracted.md
│   └── translations/    # 翻译目录
│       └── translations.json
└── azul/                # 另一个游戏目录
    ├── metadata/
    ├── rules/
    └── translations/
```

## 目录说明

### metadata/

存储游戏的基本信息：

- `game_info.json`：包含游戏 ID、名称、URL 等信息

### rules/

存储游戏规则书相关文件：

- `original.pdf`：原始规则书 PDF 文件
- `extracted.md`：从 PDF 提取的文本内容

### translations/

存储翻译相关文件：

- `translations.json`：翻译内容，包含原文和译文

## 注意事项

1. 此目录不会被 Git 版本控制，请妥善备份重要数据。
2. 建议使用游戏的英文名称作为目录名，以保持一致性。
3. 请保持目录结构的整洁，不要添加无关文件。 