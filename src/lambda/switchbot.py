import base64
import boto3
import hashlib
import hmac
import json
import os
import time
import uuid

from curtain import Curtain


# トークン、シークレット取得
ENCRYPTED = os.environ['token']
DECRYPTED_TOKEN = boto3.client('kms').decrypt(
    CiphertextBlob=base64.b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

ENCRYPTED = os.environ['secret']
DECRYPTED_SECRET = boto3.client('kms').decrypt(
    CiphertextBlob=base64.b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

HOST = 'https://api.switch-bot.com'

def make_header():
    """API用リクエストヘッダ作成

    Returns:
        dict: APIヘッダ
    """    
    apiHeader = {}
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = f'{DECRYPTED_TOKEN}{t}{nonce}'

    string_to_sign = bytes(string_to_sign, 'utf-8')
    sec = bytes(DECRYPTED_SECRET, 'utf-8')

    sign = base64.b64encode(
        hmac.new(
            sec,
            msg=string_to_sign,
            digestmod=hashlib.sha256
        ).digest())

    apiHeader['Authorization'] = DECRYPTED_TOKEN
    apiHeader['Content-Type'] = 'application/json'
    apiHeader['charset'] = 'utf-8'
    apiHeader['t'] = str(t)
    apiHeader['sign'] = str(sign, 'utf-8')
    apiHeader['nonce'] = str(nonce)

    return apiHeader


def lambda_handler(event, context):
    header = make_header()

    curtain = Curtain('sample_id')
    curtain.open(header).json()

