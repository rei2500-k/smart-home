import base64
import hashlib
import hmac
import json
import os
import requests
import time
import uuid


HOST = 'https://api.switch-bot.com'

# トークン、シークレット取得
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config/config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['switch-bot']['token']
SECRET = config['switch-bot']['secret']

def make_header():
    """API用リクエストヘッダ作成

    Returns:
        dict: APIヘッダ
    """    
    apiHeader = {}
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = f'{TOKEN}{t}{nonce}'

    string_to_sign = bytes(string_to_sign, 'utf-8')
    sec = bytes(SECRET, 'utf-8')

    sign = base64.b64encode(
        hmac.new(
            sec,
            msg=string_to_sign,
            digestmod=hashlib.sha256
        ).digest())

    apiHeader['Authorization'] = TOKEN
    apiHeader['Content-Type'] = 'application/json'
    apiHeader['charset'] = 'utf-8'
    apiHeader['t'] = str(t)
    apiHeader['sign'] = str(sign, 'utf-8')
    apiHeader['nonce'] = str(nonce)

    return apiHeader

def device_list(header: dict):
    """デバイス一覧取得

    Returns:
        _type_: _description_
    """    
    response = requests.get(f'{HOST}/v1.1/devices', headers=header)
    
    return response

def device_status(device: str, header: dict):
    response = requests.get(f'{HOST}/v1.1/devices/{device}/status', headers=header)

    return response

if __name__ == '__main__':
    header = make_header()
    print(device_list(header).json())
