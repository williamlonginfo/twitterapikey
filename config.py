"""
Twitter API 授权服务配置文件
请在下方填入你的 Twitter Developer Portal 中的 API 凭证
"""

# Twitter Developer Portal 申请的 Consumer Key (API Key)
API_KEY = "你的API_KEY"

# Twitter Developer Portal 申请的 Consumer Secret (API Secret)
API_SECRET = "你的API_SECRET"

# OAuth 回调地址，必须与 Twitter App 设置中的一致
CALLBACK_URL = "http://127.0.0.1:5000/callback"

# 服务运行端口
PORT = 5000

# 服务运行主机地址
HOST = "127.0.0.1"

# 存储授权凭证的文件路径
TOKENS_FILE = "tokens.json"

# 服务密钥（用于 Flask session）
SECRET_KEY = "your-secret-key-change-this-in-production"
