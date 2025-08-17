import datetime
import json
import os

import switchbot
from postgres import PG


# デバイス情報取得
heder = switchbot.make_header()
response = switchbot.device_list(heder).json()
device_list = response['body']['deviceList']

# DB接続情報取得
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config/config.json', 'r') as f:
    config = json.load(f)
access_info = config['db_connection']

# DB接続
pg = PG(access_info)

TH_DEVICE = ['WoIOSensor', 'Hub 2']
LOG_TIME = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
for device in device_list:
    if device['deviceType'] in TH_DEVICE:
        # デバイスがマスタに存在するか確認
        cur = pg.conn.cursor()
        cur.execute(
            "select * from devices where device_id = %s",
            (device['deviceId'],)
        )
        # 無ければ登録
        cur.fetchone()
        if cur.rowcount == 0:
            pg.insert(
                'devices',
                ['device_id', 'device_name', 'device_type'],
                (device['deviceId'], device['deviceName'], device['deviceType'])
            )

        # デバイス値取得
        status = switchbot.device_status(device['deviceId'], heder).json()
        # 登録
        pg.insert(
            'temperature_humidity_logs',
            ['device_id', 'log_time', 'temperature', 'humidity'],
            (
                status['body']['deviceId'],
                LOG_TIME,
                status['body']['temperature'],
                status['body']['humidity']
            )
        )

# コネクション切断
pg.close()
