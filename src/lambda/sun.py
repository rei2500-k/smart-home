import base64
import boto3
import datetime
import json
import os
import requests


RISE_TARGET = os.environ['rise_target']
SET_TARGET = os.environ['set_target']
ROLE = os.environ['role_arn']

# 緯度経度取得
ENCRYPTED = os.environ['lat']
LAT = boto3.client('kms').decrypt(
    CiphertextBlob=base64.b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

ENCRYPTED = os.environ['lng']
LNG = boto3.client('kms').decrypt(
    CiphertextBlob=base64.b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

def sunset_sunrise(date: datetime.datetime, lat: float, lng: float) -> tuple:
    """日の出、日の入り時刻を取得

    Args:
        date (datetime.datetime): 日付
        lat (float): 緯度
        lng (float): 経度

    Returns:
        tuple(str, str): 日の出、日の入り時刻

    """    
    HOST = 'http://labs.bitmeister.jp/ohakon/json/'
    params = {
        'mode': 'sun_rise_set',
        'year': date.year,
        'month': date.month,
        'day': date.day,
        'lat': lat,
        'lng': lng,
    }
    response = requests.get(HOST, params=params)
    
    sunrise = response.json()['rise_and_set']['sunrise_hm']
    sunset = response.json()['rise_and_set']['sunset_hm']

    return sunrise, sunset

def scheduler(name: str, target_arn: str, schedule: datetime.datetime):
    client = boto3.client('scheduler')
    client.create_schedule(
        Name=name,
        ActionAfterCompletion='DELETE',
        FlexibleTimeWindow={'Mode': 'OFF'},
        GroupName='switchbot',
        ScheduleExpression=f'at({schedule.strftime("%Y-%m-%dT%H:%M:%S")})',
        ScheduleExpressionTimezone='Asia/Tokyo',
        State='ENABLED',
        Target={
            'Arn': target_arn,
            'RoleArn': ROLE,
            'Input': json.dumps({'hoge': 'test'}),
        }
    )

def lambda_handler(event, context):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    sunrise, sunset = sunset_sunrise(now, LAT, LNG)

    sunrise = sunrise.split(':')
    rise_time = datetime.datetime(now.year, now.month, now.day, int(sunrise[0]), int(sunrise[1]))
    sunset = sunset.split(':')
    set_time = datetime.datetime(now.year, now.month, now.day, int(sunset[0]), int(sunset[1]))

    rise_name = 'curtain_open'
    set_name = 'curtain_close'
    scheduler(rise_name, RISE_TARGET, rise_time)
    scheduler(set_name, SET_TARGET, set_time)
