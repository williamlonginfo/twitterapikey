"""
Twitter API 授权服务配置文件
请在下方填入你的 Twitter Developer Portal 中的 API 凭证
"""

# Twitter Developer Portal 申请的 Consumer Key (API Key)
API_KEY = "DLYOSZMo8x6HofSPDwDkRhMYw"

# Twitter Developer Portal 申请的 Consumer Secret (API Secret)
API_SECRET = "jgn838O0owhN0xtDP7p2RpDOrpdNVh0sH84hsuyuyJVc666vol"

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
