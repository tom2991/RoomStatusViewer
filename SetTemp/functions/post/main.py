# 気温データを取得し、DynamoDBにinsertする
import sys
import traceback
from datetime import datetime, timedelta, timezone
import boto3

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('temperature')


# lambdaのハンドラ
def handle(event, context):
    # ToDo POSTを受け取る
    print("print log.")
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": insertTemperature('37.5')
    }
# DynamoDBのKeyとして使用する日付と時刻を計算する
def calcDateTime():
    # JSTを指定しないと、たぶんUNIX標準時になる
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now.strftime("%Y%m%d_%H%M%S")

# DynamoDBに気温をputする
def insertTemperature(temperatureValue):
    key = calcDateTime()
    try:
        table.put_item(
            Item={
                "datetime_key": key,
                "value": temperatureValue
            }
        )
        return "OK"
    except :
        return "NG"
