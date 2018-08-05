# 気温データを取得し、DynamoDBにinsertする
from datetime import datetime, timedelta, timezone
import boto3

# lambdaのハンドラ
def lambda_handler(event, context):
    # ToDo POSTを受け取る
    print("print log.")
    return {
        "message": "Hello World",
    }

# DynamoDBのKeyとして使用する日付と時刻を計算する
def calcDateTime():
    # JSTを指定しないと、たぶんUNIX標準時になる
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now.strftime("%Y%m%d_%H%M%S")

# DynamoDBに気温をinsertする
def insertTemperature(temperature):
    key = calcDateTime()
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('temperature')
    table.put_item = {
        key:temperature
    }
