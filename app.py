"""
Twitter API 授权服务主程序
提供网页界面进行 Twitter OAuth 1.0a 授权流程
自动获取用户账号的 Access Token 和 Access Token Secret
"""

import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from requests_oauthlib import OAuth1Session
import config


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def load_tokens():
    """
    从本地 JSON 文件加载已保存的授权凭证
    如果文件不存在或数据损坏，返回空字典
    """
    if os.path.exists(config.TOKENS_FILE):
        try:
            with open(config.TOKENS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_tokens(tokens):
    """
    将授权凭证保存到本地 JSON 文件
    tokens: dict, 包含所有账号的授权信息
    """
    with open(config.TOKENS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    """
    首页路由，显示已授权账号列表和添加新账号按钮
    展示每个账号的基本信息和授权状态
    """
    tokens = load_tokens()
    return render_template('index.html', tokens=tokens)


@app.route('/authorize')
def authorize():
    """
    启动 Twitter OAuth 授权流程
    创建 OAuth1Session 并重定向用户到 Twitter 授权页面
    如果配置错误或授权失败，返回错误信息
    """
    try:
        oauth_session = OAuth1Session(
            client_key=config.API_KEY,
            client_secret=config.API_SECRET,
            callback_uri=config.CALLBACK_URL
        )

        # 获取授权 URL
        request_token_url = "https://api.x.com/oauth/request_token"
        oauth_session.fetch_request_token(request_token_url)

        # 保存 request_token 到 session，供 callback 使用
        session['request_token'] = oauth_session.token

        # 生成授权 URL 并重定向
        authorization_url = oauth_session.authorization_url(
            "https://api.x.com/oauth/authorize"
        )
        return redirect(authorization_url)

    except Exception as e:
        return f"<h2>授权初始化失败</h2><p>{str(e)}</p><a href='/'>返回首页</a>"


@app.route('/callback')
def callback():
    """
    OAuth 授权回调路由
    接收 Twitter 返回的验证结果，交换得到正式的 Access Token
    保存凭证到本地文件，然后显示授权成功信息
    """
    # 从 URL 参数中获取 oauth_verifier
    oauth_verifier = request.args.get('oauth_verifier')

    if not oauth_verifier:
        return "<h2>授权失败：未收到验证信息</h2><a href='/'>返回首页</a>"

    try:
        # 从 session 中恢复 request_token
        request_token = session.get('request_token')

        if not request_token:
            return "<h2>授权失败：会话已过期</h2><a href='/'>返回首页</a>"

        # 创建新的 OAuth1Session，使用 request_token 和 verifier 交换 Access Token
        oauth_session = OAuth1Session(
            client_key=config.API_KEY,
            client_secret=config.API_SECRET,
            resource_owner_key=request_token.get('oauth_token'),
            resource_owner_secret=request_token.get('oauth_token_secret'),
            verifier=oauth_verifier
        )

        # 交换得到正式的 Access Token
        access_token_url = "https://api.x.com/oauth/access_token"
        oauth_session.fetch_access_token(access_token_url)

        # 获取 access_token 信息
        access_token = oauth_session.token
        owner_key = access_token.get('oauth_token')
        owner_secret = access_token.get('oauth_token_secret')

        # 加载现有凭证，添加新账号
        tokens = load_tokens()

        # 生成账号标识（使用 token 的后几位作为简化标识）
        account_id = f"account_{len(tokens) + 1}"

        # 保存账号信息
        tokens[account_id] = {
            'oauth_token': owner_key,
            'oauth_token_secret': owner_secret
        }

        # 写入文件
        save_tokens(tokens)

        # 清理 session
        session.pop('request_token', None)

        return render_template('success.html',
                             oauth_token=owner_key,
                             oauth_token_secret=owner_secret,
                             account_id=account_id)

    except Exception as e:
        return f"<h2>授权回调处理失败</h2><p>{str(e)}</p><a href='/'>返回首页</a>"


@app.route('/accounts')
def list_accounts():
    """
    API 路由：获取所有已授权账号的列表
    返回 JSON 格式的账号信息（不含完整 token）
    """
    tokens = load_tokens()
    accounts = []
    for account_id, info in tokens.items():
        accounts.append({
            'id': account_id,
            'token_prefix': info['oauth_token'][:10] + '...',
            'has_secret': bool(info.get('oauth_token_secret'))
        })
    return jsonify({'accounts': accounts, 'total': len(accounts)})


@app.route('/account/<account_id>')
def get_account(account_id):
    """
    API 路由：获取指定账号的完整凭证信息
    用于查看和复制 Access Token
    """
    tokens = load_tokens()
    if account_id in tokens:
        return jsonify({'account': account_id, **tokens[account_id]})
    return jsonify({'error': '账号不存在'}), 404


@app.route('/delete/<account_id>', methods=['POST'])
def delete_account(account_id):
    """
    删除指定账号的授权凭证
    从本地文件中移除该账号的记录
    """
    tokens = load_tokens()
    if account_id in tokens:
        del tokens[account_id]
        save_tokens(tokens)
        return jsonify({'success': True, 'message': f'账号 {account_id} 已删除'})
    return jsonify({'error': '账号不存在'}), 404


@app.route('/export')
def export_tokens():
    """
    导出所有授权凭证为 JSON 格式
    方便用户备份或转移到其他应用
    """
    tokens = load_tokens()
    response = jsonify(tokens)
    response.headers['Content-Disposition'] = 'attachment; filename=tokens.json'
    return response


if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════════╗
║           Twitter API Key 授权服务                         ║
║                                                        ║
║  服务地址：http://127.0.0.1:{config.PORT}                       ║
║                                                        ║
║  请在浏览器中打开上述地址开始授权流程                       ║
║                                                        ║
║  按 Ctrl+C 可停止服务                                   ║
╚════════════════════════════════════════════════════════════╝
    """)
    app.run(host=config.HOST, port=config.PORT, debug=True)
