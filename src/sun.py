import base64
import boto3
import datetime
import json
import os
import requests


# 緯度経度取得
LAT = config['switch-bot']['sample_lat']
LNG = config['switch-bot']['sample_lng']

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


if __name__ == '__main__':
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    sunrise, sunset = sunset_sunrise(now, LAT, LNG)

    sunrise = sunrise.split(':')
    rise_time = datetime.datetime(now.year, now.month, now.day, int(sunrise[0]), int(sunrise[1]))
    sunset = sunset.split(':')
    set_time = datetime.datetime(now.year, now.month, now.day, int(sunset[0]), int(sunset[1]))
