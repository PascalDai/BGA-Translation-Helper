# 工作流程说明

## 1. 初始化新游戏

### 1.1 创建游戏目录

```bash
python main.py init-game <game_name>
```

### 1.2 目录结构

```mermaid
graph TD
    A[game_name] --> B[rules]
    A --> C[translations]
    A --> D[metadata]

    B --> B1[original.pdf]
    B --> B2[extracted.md]

    C --> C1[bga_translations.md]
    C --> C2[my_translations.md]

    D --> D1[game_info.json]
```

## 2. 规则书处理

### 2.1 准备规则书

1. 将规则书 PDF 放入 `rules/original.pdf`
2. 确保 PDF 清晰可读

### 2.2 运行 OCR

```bash
python main.py extract-text <game_name>
```

- 自动提取文本
- 保存到 `rules/extracted.md`

## 3. 获取 BGA 翻译

### 3.1 配置 BGA 账号

```bash
python main.py config-bga --username <username> --password <password>
```

### 3.2 获取翻译

```bash
python main.py fetch-translations <game_name>
```

- 自动登录 BGA
- 抓取已有翻译
- 保存到 `translations/bga_translations.md`

## 4. 翻译工作

### 4.1 开始翻译

```bash
python main.py start-translation <game_name>
```

- 显示待翻译内容
- 提供已有翻译参考
- 支持实时保存

### 4.2 翻译界面

```mermaid
graph LR
    A[原文] --> B[翻译界面]
    C[BGA翻译] --> B
    D[我的翻译] --> B
    E[状态] --> B
```

### 4.3 保存翻译

- 自动保存到 `translations/my_translations.md`
- 支持导出为其他格式

## 5. 提交翻译

### 5.1 准备提交

```bash
python main.py prepare-submission <game_name>
```

- 检查翻译完整性
- 生成提交格式

### 5.2 提交到 BGA

- 手动复制翻译内容
- 在 BGA 平台提交

## 6. 日常维护

### 6.1 更新翻译

```bash
python main.py update-translations <game_name>
```

- 获取最新 BGA 翻译
- 合并到本地文件

### 6.2 备份数据

```bash
python main.py backup <game_name>
```

- 创建数据备份
- 导出翻译历史

## 完整工作流程

```mermaid
flowchart TD
    A[开始] --> B[初始化游戏]
    B --> C[准备规则书]
    C --> D[OCR处理]
    D --> E[获取BGA翻译]
    E --> F[开始翻译]
    F --> G{翻译完成?}
    G -->|否| F
    G -->|是| H[准备提交]
    H --> I[提交到BGA]
    I --> J[更新维护]
    J --> K[结束]

    subgraph 日常维护
    L[定期备份] --> M[更新翻译]
    M --> N[检查完整性]
    end
```

## 注意事项

1. 定期备份数据
2. 保持 BGA 账号信息更新
3. 注意遵守 BGA 平台规则
4. 及时保存翻译进度
