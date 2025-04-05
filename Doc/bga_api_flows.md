# BGA API 流程

## 登录流程

1. 访问登录页面
   ```
   GET https://boardgamearena.com/account/account/login.html
   ```

2. 提交登录表单
   ```
   POST https://boardgamearena.com/account/account/login.html
   Content-Type: application/x-www-form-urlencoded
   
   email={username}&password={password}&rememberme=1&redirect=&submit=submit
   ```

## 游戏元数据获取

1. 获取游戏列表
   ```
   GET https://boardgamearena.com/gamelist
   ```

2. 获取游戏详情
   ```
   GET https://boardgamearena.com/gamepanel?game={game_name}
   ```

## 翻译页面操作

### 1. 访问翻译页面

```
GET https://boardgamearena.com/translation/translation/module.html?id={module_id}
```

参数说明：
- `module_id`：模块 ID，从游戏元数据中获取

### 2. 获取翻译内容

```
GET https://boardgamearena.com/translation/translation/getmodulestrings.html?id={module_id}&language=zh&page={page_number}
```

参数说明：
- `module_id`：模块 ID
- `language`：目标语言（zh 为中文）
- `page_number`：页码，从 1 开始

### 3. 提交翻译

页面操作流程：
1. 定位原文输入框
   ```javascript
   document.querySelector(`#original_{text_id}`)
   ```

2. 定位翻译输入框
   ```javascript
   document.querySelector(`#translated_{text_id}`)
   ```

3. 填写翻译内容
   ```javascript
   element.value = translation
   ```

4. 自动保存
   - 系统会自动保存修改的内容
   - 无需手动点击保存按钮

### 4. 翻页操作

1. 检查是否有下一页
   ```javascript
   document.querySelector('.pagination-next')
   ```

2. 点击下一页按钮
   ```javascript
   nextPageButton.click()
   ```

## 错误处理

### HTTP 状态码

- 200：成功
- 401：未授权，需要重新登录
- 403：无权限访问
- 404：页面不存在
- 500：服务器错误

### 常见错误

1. 登录失败
   ```json
   {
     "status": "error",
     "error": "Invalid credentials"
   }
   ```

2. 无权限访问
   ```json
   {
     "status": "error",
     "error": "Access denied"
   }
   ```

3. 翻译保存失败
   ```json
   {
     "status": "error",
     "error": "Failed to save translation"
   }
   ```

## 最佳实践

1. 请求间隔
   - 登录：至少 2 秒
   - 页面加载：至少 1 秒
   - 翻译提交：至少 0.5 秒

2. 错误重试
   - 网络错误：最多重试 3 次
   - 登录失败：最多重试 2 次
   - 保存失败：立即重试 1 次

3. 会话管理
   - 定期检查登录状态
   - 超时自动重新登录
   - 保持会话活跃

4. 性能优化
   - 批量获取翻译内容
   - 缓存已获取的数据
   - 避免频繁页面刷新

## 安全注意事项

1. 账号保护
   - 使用环境变量存储凭据
   - 避免明文存储密码
   - 定期更新登录信息

2. 请求限制
   - 遵守平台访问频率
   - 避免过度频繁的请求
   - 合理设置超时时间

3. 数据安全
   - 本地加密存储敏感数据
   - 及时清理临时文件
   - 保护用户隐私信息 