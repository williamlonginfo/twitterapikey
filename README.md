# Twitter API Key 授权服务

本地搭建一套 X (Twitter) 授权网页服务，用来：本地网页一键授权、自动获取第三方账号的 Access Token / Secret ，全程在电脑本地跑，有网页界面、不用手动复制验证码，完美解决「开发者 App、多个发布账号授权」问题。

## 功能特性

- 🌐 **网页一键授权** - 通过浏览器点击即可完成授权，无需手动复制验证码
- 🔒 **全程本地运行** - 所有授权流程在本地执行，数据不经过第三方服务器
- 📊 **多账号管理** - 支持同时管理多个 Twitter 账号的授权信息
- 💾 **本地存储** - 授权凭证安全存储在本地文件中
- 🎯 **简单易用** - 提供直观的网页界面，无需命令行操作

## 环境要求

- Python 3.7+
- Flask
- requests-oauthlib

## 安装步骤

1. 安装依赖包：

```bash
pip install -r requirements.txt
```

2. 配置 Twitter API 凭证：

打开 `config.py` 文件，填入你的 Twitter Developer Portal 中的 API Key 和 Secret：

```python
API_KEY = "你的API_KEY"
API_SECRET = "你的API_SECRET"
CALLBACK_URL = "http://127.0.0.1:5000/callback"
```

3. 获取 Twitter API 凭证：

- 访问 [Twitter Developer Portal](https://developer.twitter.com/)
- 创建或登录你的开发者账号
- 创建或选择一个 App
- 在 App 设置中启用 OAuth 1.0a
- 设置回调 URL 为 `http://127.0.0.1:5000/callback`
- 复制 Consumer Key (API Key) 和 Consumer Secret (API Secret)

## 使用方法

1. 启动服务：

```bash
python app.py
```

2. 打开浏览器访问：

```
http://127.0.0.1:5000
```

3. 点击"开始授权"按钮，跳转到 Twitter 授权页面

4. 在 Twitter 页面确认授权

5. 授权成功后，自动跳回本地页面，显示 Access Token 和 Access Token Secret

6. 可以在"已授权账号"页面查看和管理所有已授权的账号

## 文件结构

```
twitterapikey/
├── app.py              # 主程序
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── tokens.json         # 授权凭证存储文件（自动生成）
└── README.md          # 项目说明文档
```

## 注意事项

- 请妥善保管你的 API Key 和 Secret，不要泄露给他人
- Access Token 和 Secret 是账号的敏感信息，请妥善保管
- 建议定期检查已授权的账号状态
- 如果需要撤销授权，请前往 Twitter 设置页面操作

## 常见问题

### Q: 启动时报错 "Connection refused"
A: 请确保 5000 端口未被占用，或修改 `config.py` 中的 `PORT` 配置

### Q: 授权页面打不开
A: 请确保使用 `http://127.0.0.1:5000` 而非 `http://localhost:5000`

### Q: 如何添加多个账号？
A: 在首页点击"添加新账号"按钮即可，每次授权一个账号

## 技术栈

- **Web 框架**: Flask
- **OAuth 库**: requests-oauthlib
- **前端**: HTML + CSS + JavaScript
- **数据存储**: JSON 文件

## 许可证

MIT License
