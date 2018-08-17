# 湿度データを取得し、DynamoDBにinsertする
import sys
import traceback
from datetime import datetime, timedelta, timezone
import boto3

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('humidity')


# lambdaのハンドラ
def handle(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": insertHumidity(event['queryStringParameters']['humidity'])
    }
# DynamoDBのKeyとして使用する日付と時刻を計算する
def calcDateTime():
    # JSTを指定しないと、たぶんUNIX標準時になる
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now.strftime("%Y%m%d_%H%M%S")

# DynamoDBに気温をputする
def insertHumidity(humidityValue):
    key = calcDateTime()
    try:
        table.put_item(
            Item={
                "datetime_key": key,
                "value": humidityValue
            }
        )
        return key + ":" + humidityValue + "\n"
    except :
        return key + ":" + "NG\n"
