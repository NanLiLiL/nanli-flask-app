import hmac
import hashlib
import json
import requests
import os
from flask import Flask, jsonify

# 设置Webhook Secret
WEBHOOK_SECRET = 'your_webhook_secret'

# 设置ECS实例上的Flask应用程序URL
FLASK_APP_URL = 'http://120.55.51.66:443/'

# 处理Webhook请求
def handle_webhook(event_data):
    # 验证Webhook Secret
    if not verify_webhook_signature(event_data, WEBHOOK_SECRET):
        return jsonify({'status': 'failure', 'message': 'Invalid signature'}), 403

    # 获取提交信息
    commit_sha = event_data['after']

    # 克隆仓库
    os.system(f'git clone https://github.com/NanLiLiL/nanli-flask-app.git')

    # 切换到新分支
    os.chdir(f'nanli-flask-app')
    os.system(f'git checkout {commit_sha}')

    # 安装新依赖
    os.system('pip install -r requirements.txt')

    # 启动Flask应用程序
    os.system(f'{FLASK_APP_URL}run')

    return jsonify({'status': 'success', 'message': 'Deployment successful'}), 200

# 验证Webhook签名
def verify_webhook_signature(event_data, secret):
    if 'X-Hub-Signature' not in event_data['headers']:
        return False

    signature = event_data['headers']['X-Hub-Signature']
    signature_components = signature.split('=')
    if len(signature_components) != 2 or signature_components[0] != 'sha1':
        return False

    expected_signature = hmac.new(secret.encode(), event_data['payload'].encode(), hashlib.sha1).hexdigest()
    return hmac.compare_digest(expected_signature, signature_components[1])
